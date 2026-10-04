"""softmax-temperature — one tracker T drives every object. See ../model.md and storyboard.md.

Render:  uv run explainer render softmax-temperature --draft
         uv run explainer render softmax-temperature
"""

from math import exp

from manim import *

from explainer_kit import ExplainerScene, Role, label, load_model

M = load_model(__file__)
TOKENS = M["tokens"]
LOGITS = [M["logits"][t] for t in TOKENS]
COLORS = [BLUE_C, GOLD_C, TEAL_C, MAROON_C]  # token identity; color follows the token
BAR_X = [-2.4, -0.8, 0.8, 2.4]
BAR_BASE = -3.0
BAR_MAX = 2.7  # height of p = 1


def softmax(t: float) -> list[float]:
    e = [exp(z / t) for z in LOGITS]
    s = sum(e)
    return [x / s for x in e]


class SoftmaxTemperature(ExplainerScene):
    voice = "af_heart"

    def construct(self):
        T = ValueTracker(1.0)
        grow = ValueTracker(0.0)  # bars grow in once, then follow T

        # 1 — the task
        context = label("The  ___  sat on the mat.", size=34).to_corner(UL)
        names = VGroup(*[label(n, size=30, color=c) for n, c in zip(TOKENS, COLORS)])
        for name, x in zip(names, BAR_X):
            name.move_to([x, BAR_BASE - 0.4, 0])
        with self.voiceover(text="A language model must pick the next word. "
                                 "Here it has four candidates: cat, dog, fox, and owl."):
            self.play(FadeIn(context, shift=DOWN * 0.2))
            self.play(LaggedStart(*[FadeIn(n, shift=UP * 0.2) for n in names], lag_ratio=0.3))

        # 2 — logits on a number line
        line = NumberLine(x_range=[-4.5, 8.5, 1], length=11, include_numbers=False, color=Role.RELATION,
                          stroke_width=2).move_to(UP * 1.2)
        ticks = VGroup(*[label(str(v), size=20, color=Role.RELATION).next_to(line.n2p(v), DOWN, buff=0.2)
                         for v in (-4, 0, 4, 8)])
        axis_name = label("z / T", size=24, color=Role.RELATION).next_to(line, RIGHT, buff=0.25)
        dots = VGroup(*[Dot(line.n2p(z), radius=0.11, color=c) for z, c in zip(LOGITS, COLORS)])
        for dot, z in zip(dots, LOGITS):
            dot.add_updater(lambda d, z=z: d.move_to(line.n2p(z / T.get_value())))
        dot_names = VGroup(*[label(f"{n} {z:+.1f}", size=22, color=c).next_to(line.n2p(z), UP, buff=buff)
                             for n, z, c, buff in zip(TOKENS, LOGITS, COLORS, (0.25, 0.65, 0.25, 0.25))])  # dog on row 2
        with self.voiceover(text="The model gives each candidate a score. <bookmark mark='line'/> "
                                 "The score is called a logit. Cat has the highest logit.") as tracker:
            self.play(Create(line), FadeIn(ticks), FadeIn(axis_name))
            self.wait_until_bookmark("line")
            self.play(LaggedStart(*[GrowFromCenter(d) for d in dots], lag_ratio=0.25),
                      LaggedStart(*[FadeIn(n) for n in dot_names], lag_ratio=0.25))

        # 3 — softmax → bars
        def make_bar(i):
            def build():
                h = max(softmax(T.get_value())[i] * BAR_MAX * grow.get_value(), 1e-3)
                return Rectangle(width=0.9, height=h, stroke_width=0, fill_color=COLORS[i],
                                 fill_opacity=0.9).move_to([BAR_X[i], BAR_BASE + h / 2, 0])
            return always_redraw(build)

        bars = VGroup(*[make_bar(i) for i in range(4)])
        values = VGroup(*[always_redraw(lambda i=i: label(
            f"{softmax(T.get_value())[i]:.2f}", size=24).next_to(bars[i], UP, buff=0.12)) for i in range(4)])
        t_readout = always_redraw(lambda: label(f"T = {T.get_value():.2f}", size=36).to_corner(UR))
        with self.voiceover(text="Softmax turns the logits into probabilities. <bookmark mark='bars'/> "
                                 "At temperature one, cat gets sixty-one percent.") as tracker:
            self.wait_until_bookmark("bars")
            self.add(bars, values)
            self.play(grow.animate.set_value(1), FadeIn(t_readout), run_time=1.5)

        # 4 — low T
        with self.voiceover(text="Temperature divides every logit before softmax. <bookmark mark='cold'/> "
                                 "At T equal to one half, the logits move apart. Cat now gets eighty-four percent.") as tracker:
            self.wait_until_bookmark("cold")
            self.play(FadeOut(dot_names), T.animate.set_value(0.5), run_time=2.5)

        # 5 — high T
        with self.voiceover(text="Now raise the temperature. <bookmark mark='hot'/> At T equal to two, "
                                 "the logits move together. The probabilities become more equal.") as tracker:
            self.wait_until_bookmark("hot")
            self.play(T.animate.set_value(2.0), run_time=3)

        # 6 — why: distance between dots sets the ratio
        def gap_marker():
            t = T.get_value()
            a, b = line.n2p(LOGITS[1] / t) + DOWN * 0.75, line.n2p(LOGITS[0] / t) + DOWN * 0.75
            seg = Line(a, b, color=Role.FOCUS, stroke_width=4)
            ends = VGroup(*[Line(p + UP * 0.12, p + DOWN * 0.12, color=Role.FOCUS, stroke_width=4) for p in (a, b)])
            text = label(f"p(cat) / p(dog) = {exp((LOGITS[0] - LOGITS[1]) / t):.2f}", size=26,
                         color=Role.FOCUS).next_to(seg, DOWN, buff=0.15)
            return VGroup(seg, ends, text)

        gap = always_redraw(gap_marker)
        with self.voiceover(text="Why does this happen? <bookmark mark='gap'/> The ratio of two probabilities "
                                 "depends only on the distance between their dots. <bookmark mark='move'/> "
                                 "A larger distance gives a larger ratio. A smaller distance gives a ratio "
                                 "closer to one.") as tracker:
            self.wait_until_bookmark("gap")
            self.play(FadeIn(gap))
            self.wait_until_bookmark("move")
            self.play(T.animate.set_value(0.5), run_time=2.5)
            self.play(T.animate.set_value(4.0), run_time=2.5)

        # 7 — limits
        with self.voiceover(text="At a very low temperature, the top token takes almost all the probability. "
                                 "<bookmark mark='uni'/> At a very high temperature, every token gets almost "
                                 "the same probability.") as tracker:
            gap.clear_updaters()  # freeze before fading: its glyph count changes with T
            self.play(FadeOut(gap), run_time=0.5)
            self.play(T.animate.set_value(0.25), run_time=2.5)
            self.wait_until_bookmark("uni")
            self.play(T.animate.set_value(10.0), run_time=3)

        # 8 — the ranking never changes
        formula = label("p = exp(z / T) ÷ Σ exp(z / T)", size=34, color=Role.ENTITY).to_corner(UL)
        with self.voiceover(text="In every case, the order stays the same. Cat is always first, and owl is "
                                 "always last. <bookmark mark='formula'/> Temperature changes only the spread.") as tracker:
            self.play(T.animate.set_value(1.0), run_time=2)
            self.play(Indicate(names[0], color=Role.FOCUS), Indicate(names[3], color=Role.FOCUS))
            self.wait_until_bookmark("formula")
            self.play(ReplacementTransform(context, formula))
        self.wait(1.5)
