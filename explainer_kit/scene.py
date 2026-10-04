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
import os
import re
import sys
import traceback
from pathlib import Path

from manim import (BLUE_C, DOWN, GOLD_C, GREEN_C, GREY_A, GREY_B, GREY_D, PURPLE_B, RED_C, TEAL_C, UP, YELLOW_C,
                   FadeIn, FadeOut, ManimColor, MathTex, MarkupText, Rectangle, SingleStringMathTex, SurroundingRectangle,
                   Tex, Text, VGroup, VMobject, config)
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

    def render(self, *args, **kwargs):
        """Fail fast. An exception during an animation leaves manim's frame-writer thread waiting,
        so the process never exits. Print the error and exit hard instead."""
        try:
            return super().render(*args, **kwargs)
        except BaseException as exc:  # noqa: BLE001 — includes KeyboardInterrupt on purpose
            if isinstance(exc, SystemExit) and not exc.code:
                raise
            traceback.print_exc()
            sys.stderr.flush()
            os._exit(1)

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

    def predict(self, question: str, narration: str | None = None, hold: float = 2.0) -> None:
        """Stop for a prediction before the scene reveals the answer.

        Dims the frame, shows a centered "Pause and predict" card, speaks the question, and records a
        predict event. Players built with the web toolkit pause here and ask for a commitment.
        """
        backdrop = Rectangle(width=config.frame_width + 1, height=config.frame_height + 1, stroke_width=0)
        backdrop.set_fill(BACKGROUND, opacity=0.86)
        head = label("PAUSE AND PREDICT", size=22, color=Role.FOCUS)
        body = label(question, size=32)
        if body.width > config.frame_width - 2:
            body.scale_to_fit_width(config.frame_width - 2)
        card = VGroup(head, body).arrange(DOWN, buff=0.22)
        frame = SurroundingRectangle(card, color=Role.FOCUS, buff=0.3, corner_radius=0.12, stroke_width=2)
        frame.set_fill(BACKGROUND, opacity=1)
        group = VGroup(backdrop, frame, card).set_z_index(100)  # above live labels that redraw every frame
        group.explainer_overlay = True  # covers the scene on purpose; the layout check skips it
        self._timeline.append({"kind": "predict", "t": round(self.renderer.time, 3), "question": question})
        with self.voiceover(text=narration or f"Pause here and predict. {question}"):
            self.play(FadeIn(group))
        self.wait(hold)
        self.play(FadeOut(group))

    # ------------------------------------------------------------ layout check

    def layout_issues(self, min_overlap: float = 0.2) -> list[str]:
        """Visible text that overlaps other text, is covered by another group's opaque panel,
        or is partly outside the frame. Groups marked `explainer_overlay` are skipped."""
        texts, panels = [], []  # (top-level index, name, box)
        for k, top in enumerate(self.mobjects):
            if getattr(top, "explainer_overlay", False):
                continue
            for mob in _outer_texts(top):
                if mob.family_members_with_points() and _opacity(mob) >= 0.2:  # Text keeps its points in glyphs
                    texts.append((k, _name(mob), _box(mob)))
            for mob in _panels(top):
                panels.append((k, type(mob).__name__, _box(mob)))
        issues = []
        hw, hh = config.frame_width / 2, config.frame_height / 2
        for _, name, (x0, y0, x1, y1) in texts:
            if x0 < -hw - 0.01 or x1 > hw + 0.01 or y0 < -hh - 0.01 or y1 > hh + 0.01:
                issues.append(f"off-frame: {name!r}")
        for i, (_, a_name, a) in enumerate(texts):
            for _, b_name, b in texts[i + 1:]:
                if _covered(a, b) > min_overlap:
                    issues.append(f"overlap: {a_name!r} × {b_name!r}")
        for pk, p_name, p in panels:
            for tk, t_name, t in texts:
                if pk != tk and _covered(t, p, of_first=True) > min_overlap:
                    issues.append(f"covered: {t_name!r} under a {p_name}")
        return issues


def _box(mob):
    return (mob.get_left()[0], mob.get_bottom()[1], mob.get_right()[0], mob.get_top()[1])


def _covered(a, b, of_first: bool = False) -> float:
    """Overlap area as a share of the smaller box (or of box `a` when of_first)."""
    w = min(a[2], b[2]) - max(a[0], b[0])
    h = min(a[3], b[3]) - max(a[1], b[1])
    if w <= 0 or h <= 0:
        return 0.0
    area = lambda r: (r[2] - r[0]) * (r[3] - r[1])  # noqa: E731
    base = area(a) if of_first else min(area(a), area(b))
    return w * h / base if base > 0 else 0.0


def _panels(mob):
    """Filled, mostly opaque shapes (not text): they hide whatever is under them."""
    if isinstance(mob, TEXT_TYPES) or not isinstance(mob, VMobject):  # e.g. ValueTracker
        return
    if mob.has_points() and not mob.submobjects and mob.get_fill_opacity() >= 0.6 and mob.width > 0.5 and mob.height > 0.3:
        yield mob
    for sub in mob.submobjects:
        yield from _panels(sub)


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
    text = (getattr(mob, "original_text", None) or getattr(mob, "tex_string", None) or getattr(mob, "text", None)
            or type(mob).__name__)
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
