"""Base scene and visual language for 3b1b-style explainers.

Colors encode meaning. Use each role for one meaning in the whole video, and
use the same entity names as model.md.

ExplainerScene adds four things to VoiceoverScene:
- captions timed to the real start of each sentence (not estimated from length);
- a timeline of voiceovers, bookmarks, and predict pauses, for `explainer review`;
- a layout check: on-screen text that overlaps other text or leaves the frame;
- predict(): a predict-first pause that players and `review` understand.
"""

from __future__ import annotations

import json
import re
from pathlib import Path

from manim import (BLUE_C, DOWN, GOLD_C, GREEN_C, GREY_A, GREY_B, GREY_D, PURPLE_B, RED_C, TEAL_C, UP, YELLOW_C,
                   FadeIn, FadeOut, ManimColor, MathTex, MarkupText, SingleStringMathTex, SurroundingRectangle,
                   Tex, Text, VGroup, config)
from manim_voiceover import VoiceoverScene
from manim_voiceover.helper import remove_bookmarks

from explainer_kit.voice import make_speech_service

BACKGROUND = ManimColor("#0E0E12")
FONT = "Avenir Next"
TEXT_TYPES = (Text, MarkupText, MathTex, SingleStringMathTex, Tex)


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
        self._timeline: list[dict] = []

    # ------------------------------------------------------------ captions

    def add_wrapped_subcaption(self, subcaption: str, duration: float, subcaption_buff: float = 0.1,
                               max_subcaption_len: int = 70) -> None:
        """Split captions at sentence boundaries and start each at its sentence's real audio time."""
        chunks = caption_chunks(subcaption, max_subcaption_len)
        starts = self._chunk_starts(chunks, duration)
        for i, chunk in enumerate(chunks):
            end = starts[i + 1] if i + 1 < len(chunks) else duration
            self.add_subcaption(chunk, duration=max(end - starts[i] - subcaption_buff, 0), offset=starts[i])

    def _chunk_starts(self, chunks: list[str], duration: float) -> list[float]:
        """Audio time where each chunk starts. Exact at sentence starts; proportional as a fallback."""
        total = sum(len(c) for c in chunks)
        proportional, acc = [], 0.0
        for c in chunks:
            proportional.append(duration * acc / total)
            acc += len(c)
        tracker = getattr(self, "current_tracker", None)
        interp = getattr(tracker, "time_interpolator", None)
        if interp is None:
            return proportional
        content = remove_bookmarks(tracker.data["input_text"])
        starts, pos = [], 0
        for chunk, fallback in zip(chunks, proportional):
            m = re.compile(r"\s+".join(map(re.escape, chunk.split()))).search(content, pos)
            if not m:
                return proportional
            starts.append(min(max(interp.interpolate(m.start()), 0.0), duration))
            pos = m.end()
        return starts

    # ------------------------------------------------------------ timeline

    def _add_voiceover_text(self, text, *args, **kwargs):
        tracker = super()._add_voiceover_text(text, *args, **kwargs)
        self._timeline.append({
            "kind": "voiceover", "t": round(tracker.start_t, 3), "duration": round(tracker.duration, 3),
            "text": " ".join(remove_bookmarks(text).split()),
            "bookmarks": {k: round(v, 3) for k, v in getattr(tracker, "bookmark_times", {}).items()},
        })
        return tracker

    def wait_until_bookmark(self, mark: str) -> None:
        super().wait_until_bookmark(mark)
        self._timeline.append({"kind": "bookmark", "t": round(self.renderer.time, 3), "mark": mark,
                               "issues": self.layout_issues()})

    def wait_for_voiceover(self) -> None:
        super().wait_for_voiceover()
        self._timeline.append({"kind": "voiceover_end", "t": round(self.renderer.time, 3),
                               "issues": self.layout_issues()})

    def tear_down(self) -> None:
        super().tear_down()
        out = Path(config.media_dir) / "timeline" / f"{type(self).__name__}.json"
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(json.dumps({"scene": type(self).__name__, "events": self._timeline}, indent=1))

    # ------------------------------------------------------------ predict-first

    def predict(self, question: str, narration: str | None = None, hold: float = 2.0, position=UP) -> None:
        """Stop for a prediction before the scene reveals the answer.

        Shows a "Pause and predict" card, speaks the question, and records a predict
        event. Players built with the web toolkit pause here and ask for a commitment.
        """
        head = label("PAUSE AND PREDICT", size=22, color=Role.FOCUS)
        body = label(question, size=30)
        if body.width > config.frame_width - 2:
            body.scale_to_fit_width(config.frame_width - 2)
        card = VGroup(head, body).arrange(DOWN, buff=0.18).to_edge(position, buff=0.45)
        frame = SurroundingRectangle(card, color=Role.FOCUS, buff=0.25, corner_radius=0.12, stroke_width=2)
        frame.set_fill(BACKGROUND, opacity=0.92)
        group = VGroup(frame, card)
        self._timeline.append({"kind": "predict", "t": round(self.renderer.time, 3), "question": question})
        with self.voiceover(text=narration or f"Pause here and predict. {question}"):
            self.play(FadeIn(group, shift=DOWN * 0.15 if position is UP else UP * 0.15))
        self.wait(hold)
        self.play(FadeOut(group))

    # ------------------------------------------------------------ layout check

    def layout_issues(self, min_overlap: float = 0.2) -> list[str]:
        """Visible text that overlaps other text, or that is partly outside the frame."""
        boxes = []
        for top in self.mobjects:
            for mob in _outer_texts(top):
                if not mob.has_points() or _opacity(mob) < 0.2:
                    continue
                boxes.append((_name(mob), mob.get_left()[0], mob.get_bottom()[1], mob.get_right()[0], mob.get_top()[1]))
        issues = []
        hw, hh = config.frame_width / 2, config.frame_height / 2
        for name, x0, y0, x1, y1 in boxes:
            if x0 < -hw - 0.01 or x1 > hw + 0.01 or y0 < -hh - 0.01 or y1 > hh + 0.01:
                issues.append(f"off-frame: {name!r}")
        for i, a in enumerate(boxes):
            for b in boxes[i + 1:]:
                w = min(a[3], b[3]) - max(a[1], b[1])
                h = min(a[4], b[4]) - max(a[2], b[2])
                if w > 0 and h > 0:
                    smaller = min((a[3] - a[1]) * (a[4] - a[2]), (b[3] - b[1]) * (b[4] - b[2]))
                    if smaller > 0 and w * h / smaller > min_overlap:
                        issues.append(f"overlap: {a[0]!r} × {b[0]!r}")
        return issues


def _outer_texts(mob):
    if isinstance(mob, TEXT_TYPES):
        yield mob
        return
    for sub in mob.submobjects:
        yield from _outer_texts(sub)


def _opacity(mob) -> float:
    values = [sm.get_fill_opacity() for sm in mob.family_members_with_points()]
    return max(values) if values else 0.0


def _name(mob) -> str:
    text = getattr(mob, "text", None) or getattr(mob, "tex_string", None) or type(mob).__name__
    text = " ".join(str(text).split())
    return text if len(text) <= 40 else text[:37] + "…"


def caption_chunks(text: str, max_len: int = 70) -> list[str]:
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
