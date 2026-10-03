"""Word-level text that keeps object identity across rewrites.

sentence() lays out text as one VGroup per word, with real kerning and baselines.
diff_words() matches words between two sentences. morph() moves the kept words,
fades out the removed words, and fades in the added words — so the viewer can
track which words survive a rewrite.
"""

from __future__ import annotations

import difflib
import re

from manim import DOWN, UP, FadeIn, FadeOut, ReplacementTransform, Text, VGroup

from explainer_kit.scene import FONT, Role


def _norm(word: str) -> str:
    return re.sub(r"[^\w]", "", word.lower())


def sentence(text: str, size: float = 36, width: float = 11.0, color=Role.TEXT, line_buff: float = 0.3) -> VGroup:
    """Return a VGroup of words (each a VGroup of glyphs), wrapped to `width`, centered at ORIGIN.

    Each word has a `.word` attribute with its text.
    """
    tokens = text.split()
    lines: list[list[str]] = [[]]
    for token in tokens:
        trial = " ".join(lines[-1] + [token])
        if lines[-1] and Text(trial, font=FONT, font_size=size).width > width:
            lines.append([token])
        else:
            lines[-1].append(token)

    rows = VGroup()
    words = VGroup()
    for line in lines:
        row = Text(" ".join(line), font=FONT, font_size=size, color=color)
        glyphs = list(row.submobjects)  # whitespace has no glyphs
        start = 0
        for token in line:
            word = VGroup(*glyphs[start:start + len(token)])
            word.word = token
            words.add(word)
            start += len(token)
        rows.add(row)
    rows.arrange(DOWN, buff=line_buff)  # moves the glyphs, so the word groups follow
    words.move_to([0, 0, 0])
    return words


def diff_words(old: VGroup, new: VGroup) -> tuple[list[tuple[int, int]], list[int], list[int]]:
    """Return (kept (old_i, new_j) pairs, removed old indices, added new indices)."""
    a = [_norm(w.word) for w in old]
    b = [_norm(w.word) for w in new]
    kept, removed, added = [], [], []
    for tag, i1, i2, j1, j2 in difflib.SequenceMatcher(a=a, b=b, autojunk=False).get_opcodes():
        if tag == "equal":
            kept += list(zip(range(i1, i2), range(j1, j2)))
        else:
            removed += list(range(i1, i2))
            added += list(range(j1, j2))
    return kept, removed, added


def removed_words(old: VGroup, new: VGroup) -> VGroup:
    """The words of `old` that the rewrite to `new` deletes."""
    return VGroup(*(old[i] for i in diff_words(old, new)[1]))


def added_words(old: VGroup, new: VGroup) -> VGroup:
    return VGroup(*(new[j] for j in diff_words(old, new)[2]))


def morph(old: VGroup, new: VGroup) -> list:
    """Animations that rewrite `old` into `new`. Kept words move; others fade."""
    kept, removed, added = diff_words(old, new)
    anims = [ReplacementTransform(old[i], new[j]) for i, j in kept]
    anims += [FadeOut(old[i], shift=DOWN * 0.15) for i in removed]
    anims += [FadeIn(new[j], shift=UP * 0.15) for j in added]
    return anims
