"""Reusable scene components. None of them need LaTeX.

TrackerBars       bars whose heights follow a function of one or more ValueTrackers
LiveNumber        on-screen number that follows a function; freeze() before you fade it
LabeledNumberLine number line with plain-text tick labels and an axis name
stagger_labels    move labels that would overlap onto a second (or third) row
"""

from __future__ import annotations

from typing import Callable, Sequence

from manim import DOWN, RIGHT, UP, NumberLine, Rectangle, VGroup, VMobject, always_redraw

from explainer_kit.scene import Role, label


def LiveNumber(fn: Callable[[], str], size: float = 28, color=Role.TEXT,
               place: Callable[[VMobject], VMobject] | None = None) -> VMobject:
    """A label redrawn from `fn` each frame, e.g. LiveNumber(lambda: f"T = {T.get_value():.2f}").

    It is an always_redraw label (not a wrapper), so FadeIn and other animations see a stable structure
    while the text stays the same. Call .freeze() before FadeOut or Transform when the text is changing:
    the glyph count of a live label changes from frame to frame, and the animation then fails.
    """
    def build() -> VMobject:
        mob = label(fn(), size=size, color=color)
        return place(mob) if place else mob

    mob = always_redraw(build)
    mob.freeze = lambda: mob.clear_updaters() or mob
    return mob


class TrackerBars(VGroup):
    """Bars at fixed x positions; heights = values() * max_height, values in [0, 1] by default.

    Each bar keeps its identity (and color) as values change. Value labels sit on the bars,
    names sit under the baseline. `grow` (a ValueTracker or None) scales heights for a grow-in.
    """

    def __init__(self, values: Callable[[], Sequence[float]], names: Sequence[str], colors: Sequence,
                 xs: Sequence[float] | None = None, base_y: float = -3.0, max_height: float = 2.7,
                 width: float = 0.9, scale: float = 1.0, value_format: str = "{:.2f}", grow=None,
                 name_size: float = 30, value_size: float = 24):
        super().__init__()
        n = len(names)
        xs = list(xs) if xs is not None else [(i - (n - 1) / 2) * 1.6 for i in range(n)]
        self.values, self.base_y = values, base_y

        def height(i):
            g = grow.get_value() if grow is not None else 1.0
            return max(values()[i] / scale * max_height * g, 1e-3)

        def bar(i):
            return always_redraw(lambda: Rectangle(
                width=width, height=height(i), stroke_width=0, fill_color=colors[i], fill_opacity=0.9,
            ).move_to([xs[i], base_y + height(i) / 2, 0]))

        self.bars = VGroup(*[bar(i) for i in range(n)])
        self.value_labels = VGroup(*[
            LiveNumber(lambda i=i: value_format.format(values()[i]), size=value_size,
                       place=lambda m, i=i: m.next_to(self.bars[i], UP, buff=0.12))
            for i in range(n)])
        self.names = VGroup(*[label(name, size=name_size, color=c).move_to([x, base_y - 0.4, 0])
                              for name, c, x in zip(names, colors, xs)])
        self.add(self.bars, self.value_labels, self.names)

    def freeze(self) -> "TrackerBars":
        for m in self.get_family():
            m.clear_updaters()
        return self


class LabeledNumberLine(VGroup):
    """NumberLine with plain-text tick labels (no LaTeX) and an axis name at the right end."""

    def __init__(self, x_range: Sequence[float], length: float, labels: Sequence[float] = (),
                 axis_name: str = "", color=Role.RELATION, label_size: float = 20, **kwargs):
        super().__init__()
        self.line = NumberLine(x_range=list(x_range), length=length, include_numbers=False, color=color,
                               stroke_width=2, **kwargs)
        self.tick_labels = VGroup(*[
            label(f"{v:g}", size=label_size, color=color).next_to(self.line.n2p(v), DOWN, buff=0.2)
            for v in labels])
        self.axis_name = label(axis_name, size=label_size + 4, color=color).next_to(self.line, RIGHT, buff=0.25) \
            if axis_name else VGroup()
        self.add(self.line, self.tick_labels, self.axis_name)

    def n2p(self, x: float):
        return self.line.n2p(x)


def stagger_labels(labels: Sequence[VMobject], anchors: Sequence, direction=UP, buff: float = 0.25,
                   row_gap: float = 0.38, pad: float = 0.12) -> VGroup:
    """Place each label next to its anchor point; move a label to the next row when it would overlap.

    Rows are filled left to right, so the result is deterministic. Returns the labels as a VGroup.
    """
    order = sorted(range(len(labels)), key=lambda i: anchors[i][0])
    rows: list[list[tuple[float, float]]] = []
    for i in order:
        lab = labels[i]
        lab.next_to(anchors[i], direction, buff=buff)
        left, right = lab.get_left()[0] - pad, lab.get_right()[0] + pad
        for r, spans in enumerate(rows + [[]]):
            if all(right <= a or left >= b for a, b in spans):
                if r == len(rows):
                    rows.append([])
                rows[r].append((left, right))
                lab.shift(direction * row_gap * r)
                break
    return VGroup(*labels)
