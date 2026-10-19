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
        timeout: int = 900, usage: dict | None = None) -> str:
    """With `usage`, the call's cost (USD) and seconds are added to that dict."""
    # The prompt goes right after -p: --tools, --allowedTools, and --add-dir take several values each and would
    # swallow a prompt placed after them.
    cmd = ["claude", "-p", prompt, "--setting-sources", "project", "--strict-mcp-config", "--system-prompt", system]
    if usage is not None:
        cmd += ["--output-format", "json"]
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
    if usage is None:
        return out.stdout.strip()
    data = json.loads(out.stdout)
    usage["cost"] = usage.get("cost", 0) + (data.get("total_cost_usd") or 0)
    usage["seconds"] = usage.get("seconds", 0) + round((data.get("duration_ms") or 0) / 1000)
    return (data.get("result") or "").strip()


def work(prompt: str, cwd: Path, tools: list[str], allowed: list[str], append_system: str | None = None,
         plugin_dir: Path | None = None, env: dict[str, str] | None = None, model: str | None = None,
         timeout: int = 1800) -> dict:
    """One fresh agent that does a task in `cwd` with the given tools, under Claude Code's own system prompt
    (plus `append_system`). Still no settings files, no MCP servers, and no stdin; `plugin_dir` loads one
    plugin. Returns the reply, cost, seconds, and turns (from --output-format json)."""
    cmd = ["claude", "-p", prompt, "--setting-sources", "project", "--strict-mcp-config", "--output-format", "json",
           "--tools", ",".join(tools), "--allowedTools", *allowed]
    if append_system:
        cmd += ["--append-system-prompt", append_system]
    if plugin_dir:
        cmd += ["--plugin-dir", str(plugin_dir)]
    if model:
        cmd += ["--model", model]
    try:
        out = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, timeout=timeout,
                             stdin=subprocess.DEVNULL, env=env)
    except subprocess.TimeoutExpired:
        return {"result": "", "error": f"timeout after {timeout} s", "cost": None, "seconds": timeout, "turns": None}
    try:
        data = json.loads(out.stdout)
    except json.JSONDecodeError:
        return {"result": out.stdout[-2000:], "error": out.stderr.strip()[:500] or "no JSON reply", "cost": None,
                "seconds": None, "turns": None}
    return {"result": data.get("result", ""), "error": data.get("is_error") and data.get("subtype", "error") or None,
            "cost": data.get("total_cost_usd"), "seconds": round((data.get("duration_ms") or 0) / 1000),
            "turns": data.get("num_turns")}


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
