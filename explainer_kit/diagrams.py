"""Mermaid validation: render every Mermaid block once, so a syntax error fails a check, not a reader.

Blocks are found in Markdown (```mermaid fences) and HTML (<pre class="mermaid">). Each block is rendered
with the Mermaid CLI: `mmdc` on PATH, else `npx` with a pinned version (Node is the only requirement).
"""

from __future__ import annotations

import html
import json
import re
import shutil
import subprocess
import tempfile
from dataclasses import dataclass
from pathlib import Path

MERMAID_CLI = "@mermaid-js/mermaid-cli@11.17.0"
HTML_BLOCK = re.compile(r'<pre class="mermaid"[^>]*>(.*?)</pre>', re.S)


@dataclass
class Block:
    path: Path
    line: int
    source: str


def markdown_blocks(path: Path) -> list[Block]:
    blocks, current, start = [], None, 0
    for i, line in enumerate(path.read_text().splitlines(), 1):
        stripped = line.strip()
        if current is None and re.fullmatch(r"```+\s*mermaid\s*", stripped):
            current, start = [], i
        elif current is not None and re.fullmatch(r"```+", stripped):
            blocks.append(Block(path, start, "\n".join(current)))
            current = None
        elif current is not None:
            current.append(line)
    return blocks


def html_blocks(path: Path) -> list[Block]:
    raw = path.read_text()
    return [Block(path, raw[:m.start()].count("\n") + 1, html.unescape(m.group(1)))
            for m in HTML_BLOCK.finditer(raw)]


def mermaid_blocks(folder: Path) -> list[Block]:
    blocks = []
    for path in sorted(folder.rglob("*")):
        if path.suffix == ".md":
            blocks += markdown_blocks(path)
        elif path.suffix == ".html":
            blocks += html_blocks(path)
    return blocks


def mermaid_command() -> list[str] | None:
    if shutil.which("mmdc"):
        return ["mmdc"]
    if shutil.which("npx"):
        return ["npx", "-y", MERMAID_CLI]
    return None


def validate(blocks: list[Block]) -> list[tuple[Block, str]]:
    """(block, first error line) for each block that does not render. Raises when no Mermaid CLI exists."""
    cmd = mermaid_command()
    if cmd is None:
        raise FileNotFoundError("no Mermaid CLI: install Node (for npx) or @mermaid-js/mermaid-cli")
    failures = []
    with tempfile.TemporaryDirectory() as tmp:
        config = Path(tmp) / "puppeteer.json"
        config.write_text(json.dumps({"args": ["--no-sandbox"]}))  # CI runners have no user namespace sandbox
        for i, block in enumerate(blocks):
            src, out = Path(tmp) / f"{i}.mmd", Path(tmp) / f"{i}.svg"
            src.write_text(block.source)
            run = subprocess.run([*cmd, "-q", "-p", str(config), "-i", str(src), "-o", str(out)],
                                 capture_output=True, text=True)
            if run.returncode != 0 or not out.exists():
                lines = [ln.strip() for ln in (run.stderr + run.stdout).splitlines()]
                error = next((ln for ln in lines if ln.startswith(("Error", "Parse error", "UnknownDiagramError"))),
                             next((ln for ln in lines if ln and not ln.startswith("at ")), "render failed"))
                failures.append((block, error))
    return failures
