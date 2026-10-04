"""A fresh agent for one task: one `claude -p` call that sees only what it is given.

The call runs in an empty folder with no settings files, no MCP servers, and no stdin, so no CLAUDE.md,
plugin, connector, or piped text reaches it. With `read`, it may use the Read tool on the given folders
only; without it, it has no tools at all.
"""

from __future__ import annotations

import json
import re
import subprocess
import tempfile
from pathlib import Path


def ask(system: str, prompt: str, model: str | None = None, read: list[Path] | None = None,
        timeout: int = 900) -> str:
    # The prompt goes right after -p: --tools, --allowedTools, and --add-dir take several values each and would
    # swallow a prompt placed after them.
    cmd = ["claude", "-p", prompt, "--setting-sources", "project", "--strict-mcp-config", "--system-prompt", system]
    if read:
        cmd += ["--tools", "Read", "--allowedTools", "Read"]
        for folder in sorted({str(Path(p).resolve()) for p in read}):
            cmd += ["--add-dir", folder]
    else:
        cmd += ["--tools", ""]
    if model:
        cmd += ["--model", model]
    with tempfile.TemporaryDirectory() as empty:
        out = subprocess.run(cmd, cwd=empty, capture_output=True, text=True, timeout=timeout,
                             stdin=subprocess.DEVNULL)
    if out.returncode != 0:
        raise RuntimeError(f"claude -p failed: {out.stderr.strip()[:300]}")
    return out.stdout.strip()


def parse_json(text: str) -> dict:
    """The largest JSON object in a reply. Replies sometimes add prose, a fenced block, or a second object."""
    decoder, best = json.JSONDecoder(), None
    for m in re.finditer(r"\{", text):
        try:
            obj, end = decoder.raw_decode(text, m.start())
        except json.JSONDecodeError:
            continue
        if isinstance(obj, dict) and (best is None or end - m.start() > best[0]):
            best = (end - m.start(), obj)
    if best is None:
        raise ValueError(f"no JSON in reply: {text[:200]}")
    return best[1]
