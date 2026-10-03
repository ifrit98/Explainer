"""Base scene and visual language for 3b1b-style explainers.

Colors encode meaning. Use each role for one meaning in the whole video, and
use the same entity names as model.md.
"""

from __future__ import annotations

import re

from manim import (BLUE_C, GOLD_C, GREEN_C, GREY_A, GREY_B, GREY_D, PURPLE_B, RED_C, TEAL_C, YELLOW_C,
                   ManimColor, Text, config)
from manim_voiceover import VoiceoverScene

from explainer_kit.voice import make_speech_service

BACKGROUND = ManimColor("#0E0E12")
FONT = "Avenir Next"


class Role:
    """Semantic color roles."""

    ENTITY = BLUE_C        # the main objects of the model
    SECONDARY = TEAL_C     # a second class of objects
    FOCUS = YELLOW_C       # the object the narration is about right now
    RELATION = GREY_B      # arrows, connectors
    MUTED = GREY_D         # context that is present but not in focus
    TEXT = GREY_A
    GOOD = GREEN_C         # correct, preferred, result
    BAD = RED_C            # wrong, avoided, failure
    ASSUMPTION = PURPLE_B  # assumed, not observed
    QUANTITY = GOLD_C      # numbers, magnitudes


def label(text: str, size: float = 32, color=Role.TEXT, **kwargs) -> Text:
    """On-screen text in the house font. Keep on-screen text minimal."""
    return Text(text, font=FONT, font_size=size, color=color, **kwargs)


class ExplainerScene(VoiceoverScene):
    """VoiceoverScene with the house background and the local TTS service.

    Class attributes:
        voice:   Kokoro voice id (None = EXPLAINER_VOICE or af_heart).
        lexicon: written form -> spoken form, for TTS only. Captions keep the written form.
        speed:   Kokoro speaking rate.
    """

    voice: str | None = None
    lexicon: dict[str, str] = {}
    speed: float = 1.0

    def setup(self) -> None:
        super().setup()
        config.background_color = BACKGROUND
        self.camera.background_color = BACKGROUND
        self.set_speech_service(make_speech_service(voice=self.voice, lexicon=self.lexicon, speed=self.speed))

    def add_wrapped_subcaption(self, subcaption: str, duration: float, subcaption_buff: float = 0.1,
                               max_subcaption_len: int = 80) -> None:
        """Split captions at sentence (then clause) boundaries, not every N characters."""
        chunks = caption_chunks(subcaption, max_subcaption_len)
        total = sum(len(c) for c in chunks)
        offset = 0.0
        for chunk in chunks:
            chunk_duration = duration * len(chunk) / total
            self.add_subcaption(chunk, duration=max(chunk_duration - subcaption_buff, 0), offset=offset)
            offset += chunk_duration


def caption_chunks(text: str, max_len: int = 80) -> list[str]:
    """Group whole sentences into chunks of at most max_len characters.

    A sentence longer than max_len is split at commas, then at word boundaries.
    """
    pieces: list[str] = []
    for sent in re.split(r"(?<=[.!?:])\s+", " ".join(text.split())):
        if len(sent) <= max_len:
            pieces.append(sent)
            continue
        line = ""
        for part in re.split(r"(?<=[,;])\s+|\s+", sent):
            if line and len(line) + 1 + len(part) > max_len:
                pieces.append(line)
                line = part
            else:
                line = f"{line} {part}".strip()
        pieces.append(line)

    chunks: list[str] = []
    for piece in pieces:
        if chunks and len(chunks[-1]) + 1 + len(piece) <= max_len:
            chunks[-1] += " " + piece
        else:
            chunks.append(piece)
    return chunks
