"""Repository integrity: links resolve, the plugin is well formed, every example passes its model check."""

import json
import re
from pathlib import Path

import pytest

from explainer_kit.model import check

ROOT = Path(__file__).resolve().parent.parent
SKIP = {".venv", "media", "models", "node_modules", ".playwright-mcp", ".git", ".pytest_cache"}


def markdown_files(root=ROOT):
    # Eval output (evals/*/results/*/work and shown) is generated, kept as a record; it is not documentation.
    parts = lambda p: set(p.relative_to(root).parts)  # noqa: E731 — relative, so the checkout path never matches
    return [p for p in root.rglob("*.md") if not SKIP & parts(p)
            and not ("results" in parts(p) and {"work", "shown"} & parts(p))]


def test_markdown_files_ignore_where_the_repo_is_checked_out(tmp_path):
    # GitHub runners check out to /home/runner/work/<repo>/<repo>: "work" above the repo must not hide its eval reports.
    root = tmp_path / "work" / "repo"
    report = root / "evals/artifact/results/2026-10-04-dev/report.md"
    generated = root / "evals/artifact/results/2026-10-04-dev/work/subject/explanation.md"
    for f in (report, generated):
        f.parent.mkdir(parents=True)
        f.write_text("# x\n")
    files = markdown_files(root)
    assert report in files
    assert generated not in files


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


def test_agents_md_is_self_contained():
    """AGENTS.md is read by agents other than Claude Code: no @ imports, no paths that do not exist."""
    text = (ROOT / "AGENTS.md").read_text()
    assert not re.search(r"^@", text, re.M), "AGENTS.md uses Claude Code @ imports, which other agents ignore"
    paths = [p for p in re.findall(r"`([\w.\-/]+/[\w.\-/]*)`", text) if not p.startswith("http")]
    missing = [p for p in paths if not (ROOT / p.rstrip("/")).exists()]
    assert not missing, f"AGENTS.md names paths that do not exist: {missing}"
    assert "plugin/skills/explain/references/principles.md" in text
    assert "claude -p" in text


def test_agents_md_names_only_real_commands():
    subcommands = set(re.findall(r'sub\.add_parser\("(\w+)"', (ROOT / "explainer_kit/cli.py").read_text()))
    text = (ROOT / "AGENTS.md").read_text()
    named = set(re.findall(r"\bexplainer (\w+)", text))
    claude_line = next(line for line in text.splitlines() if "call the Claude CLI" in line)
    named |= set(re.findall(r"`([a-z]+)`", claude_line))
    assert not named - subcommands, f"AGENTS.md names commands the CLI does not have: {sorted(named - subcommands)}"


@pytest.mark.parametrize("folder", sorted(d for d in (ROOT / "explainers").iterdir() if (d / "model.yaml").exists()),
                         ids=lambda p: p.name)
def test_example_matches_its_model(folder):
    rep = check(folder)
    assert rep.ok, "\n".join(rep.problems)


@pytest.mark.skipif(__import__("explainer_kit.diagrams", fromlist=["x"]).mermaid_command() is None,
                    reason="no Mermaid CLI (Node or mmdc)")
def test_mermaid_in_readme_and_docs_renders():
    from explainer_kit.diagrams import markdown_blocks, validate

    blocks = [b for f in [ROOT / "README.md", *sorted((ROOT / "docs").glob("*.md"))] for b in markdown_blocks(f)]
    assert blocks and validate(blocks) == []
