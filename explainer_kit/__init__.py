"""Explainer toolkit: Manim + local Kokoro voiceover for 3b1b-style explainers, plus model checks."""

from explainer_kit.model import load_model
from explainer_kit.scene import BACKGROUND, FONT, ExplainerScene, Role, label
from explainer_kit.voice import KokoroService, SilentService, make_speech_service

__all__ = ["BACKGROUND", "FONT", "ExplainerScene", "KokoroService", "Role", "SilentService", "label",
           "load_model", "make_speech_service"]
