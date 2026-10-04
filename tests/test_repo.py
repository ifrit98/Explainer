"""Repository integrity: links resolve, the plugin is well formed, every example passes its model check."""

import json
import re
from pathlib import Path

import pytest

from explainer_kit.model import check

ROOT = Path(__file__).resolve().parent.parent
SKIP = {".venv", "media", "models", "node_modules", ".playwright-mcp", ".git", ".pytest_cache"}


def markdown_files():
    return [p for p in ROOT.rglob("*.md") if not SKIP & set(p.relative_to(ROOT).parts)]


@pytest.mark.parametrize("md", markdown_files(), ids=lambda p: str(p.relative_to(ROOT)))
def test_relative_links_resolve(md):
    text = re.sub(r"```.*?```", "", md.read_text(), flags=re.S)
    targets = re.findall(r"\]\(([^)\s]+)\)", text) + re.findall(r'(?:href|src)="([^"]+)"', text)
    broken = [t for t in targets
              if not t.startswith(("http", "#", "mailto")) and t.split("#")[0]
              and not (md.parent / t.split("#")[0]).exists()]
    assert not broken, f"broken links: {broken}"
    # GitHub's web UI does not follow symlinks: link to plugin/skills, not .claude/skills
    via_symlink = [t for t in targets if ".claude/skills/" in t]
    assert not via_symlink, f"links through the .claude/skills symlinks break on GitHub: {via_symlink}"


def test_plugin_manifest_and_skills():
    manifest = json.loads((ROOT / "plugin/.claude-plugin/plugin.json").read_text())
    market = json.loads((ROOT / ".claude-plugin/marketplace.json").read_text())
    assert manifest["name"] == market["plugins"][0]["name"] == "explainer"
    assert (ROOT / market["plugins"][0]["source"]).resolve() == (ROOT / "plugin").resolve()
    version = re.search(r'^version = "(.+)"', (ROOT / "pyproject.toml").read_text(), re.M).group(1)
    assert manifest["version"] == version, "plugin.json and pyproject.toml versions differ"
    assert f"@v{version}" in (ROOT / "plugin/bin/explainer").read_text(), "bin/explainer pins another release"
    for skill in ("explain", "video", "verify"):
        text = (ROOT / "plugin/skills" / skill / "SKILL.md").read_text()
        assert re.search(rf"^name: {skill}$", text, re.M)
        assert (ROOT / ".claude/skills" / skill / "SKILL.md").exists(), f".claude/skills/{skill} link is missing"
    for ref in re.findall(r"`(references/[\w.-]+)`", (ROOT / "plugin/skills/explain/SKILL.md").read_text()):
        assert (ROOT / "plugin/skills/explain" / ref).exists(), ref


@pytest.mark.parametrize("folder", sorted(d for d in (ROOT / "explainers").iterdir() if (d / "model.yaml").exists()),
                         ids=lambda p: p.name)
def test_example_matches_its_model(folder):
    rep = check(folder)
    assert rep.ok, "\n".join(rep.problems)
