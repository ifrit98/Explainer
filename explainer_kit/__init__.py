"""Explainer toolkit: Manim + local Kokoro voiceover for 3b1b-style explainers."""

from explainer_kit.scene import BACKGROUND, FONT, ExplainerScene, Role, label
from explainer_kit.voice import KokoroService, SilentService, make_speech_service

__all__ = ["BACKGROUND", "FONT", "ExplainerScene", "KokoroService", "Role", "SilentService", "label",
           "make_speech_service"]
