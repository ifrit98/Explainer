"""Explainer toolkit: Manim + local Kokoro voiceover for 3b1b-style explainers, plus model checks.

Imports are lazy: `from explainer_kit import ExplainerScene` loads Manim, but the CLI's
non-video commands (new, check, sync, quiz) never pay for Manim or the voice stack.
"""

from importlib import import_module

_EXPORTS = {
    "load_model": "explainer_kit.model",
    "BACKGROUND": "explainer_kit.scene", "FONT": "explainer_kit.scene", "ExplainerScene": "explainer_kit.scene",
    "Role": "explainer_kit.scene", "label": "explainer_kit.scene",
    "KokoroService": "explainer_kit.voice", "SilentService": "explainer_kit.voice",
    "make_speech_service": "explainer_kit.voice",
}

__all__ = sorted(_EXPORTS)


def __getattr__(name: str):
    if name in _EXPORTS:
        return getattr(import_module(_EXPORTS[name]), name)
    raise AttributeError(f"module 'explainer_kit' has no attribute {name!r}")
