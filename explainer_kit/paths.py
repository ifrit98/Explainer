"""Where things live, so the toolkit works from any project, not only this repo.

Project root: EXPLAINER_ROOT, else the nearest ancestor of the working directory
that has an `explainers/` folder, else the nearest one with `.git`, else the
working directory. Explainers live in `<root>/explainers/<slug>/`.

Kokoro model: EXPLAINER_KOKORO_DIR, else `models/` in an Explainer checkout,
else the user cache (`$XDG_CACHE_HOME/explainer/models` or `~/.cache/...`).
"""

from __future__ import annotations

import os
import shutil
from pathlib import Path

PACKAGE = Path(__file__).resolve().parent
TEMPLATES = PACKAGE / "templates"
WEB = PACKAGE / "web"
CHECKOUT = PACKAGE.parent  # meaningful only when running from a source checkout


def project_root() -> Path:
    if env := os.environ.get("EXPLAINER_ROOT"):
        return Path(env).expanduser().resolve()
    cwd = Path.cwd().resolve()
    for marker in ("explainers", ".git"):
        for d in (cwd, *cwd.parents):
            if (d / marker).exists():
                return d
    return cwd


def explainers_dir() -> Path:
    return project_root() / "explainers"


def explainer_dir(slug: str) -> Path:
    return explainers_dir() / slug


def display(path: Path) -> str:
    """Path relative to the project root when possible, for readable output."""
    try:
        return str(path.resolve().relative_to(project_root()))
    except ValueError:
        return str(path)


def model_dir() -> Path:
    if env := os.environ.get("EXPLAINER_KOKORO_DIR"):
        return Path(env).expanduser()
    if (CHECKOUT / "pyproject.toml").exists() and (CHECKOUT / "explainer_kit").is_dir():
        return CHECKOUT / "models"
    cache = Path(os.environ.get("XDG_CACHE_HOME", Path.home() / ".cache"))
    return cache / "explainer" / "models"


def latex_bin() -> Path | None:
    """A LaTeX bin directory: on PATH already, or a user-level TinyTeX install."""
    if shutil.which("latex") and shutil.which("dvisvgm"):
        return Path(shutil.which("latex")).parent
    for base in (Path.home() / "Library/TinyTeX/bin", Path.home() / ".TinyTeX/bin"):
        if base.is_dir():
            for arch in sorted(base.iterdir()):
                if (arch / "latex").exists():
                    return arch
    return None


def tool_env(base: dict[str, str] | None = None) -> dict[str, str]:
    """Environment for subprocesses: adds a found LaTeX to PATH."""
    env = dict(os.environ if base is None else base)
    if (tex := latex_bin()) and str(tex) not in env.get("PATH", ""):
        env["PATH"] = f"{tex}{os.pathsep}{env.get('PATH', '')}"
    return env
