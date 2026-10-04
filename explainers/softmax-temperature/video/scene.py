"""softmax-temperature — one tracker T drives every object. See ../model.md and storyboard.md.

Render:  uv run explainer render softmax-temperature --draft
         uv run explainer render softmax-temperature
"""

from math import exp

from manim import *

from explainer_kit import ExplainerScene, Role, label, load_model
from explainer_kit.components import LabeledNumberLine, LiveNumber, TrackerBars, stagger_labels

M = load_model(__file__)
TOKENS = M["tokens"]
LOGITS = [M["logits"][t] for t in TOKENS]
COLORS = [BLUE_C, GOLD_C, TEAL_C, MAROON_C]  # token identity; color follows the token


def softmax(t: float) -> list[float]:
    e = [exp(z / t) for z in LOGITS]
    return [x / sum(e) for x in e]


class SoftmaxTemperature(ExplainerScene):
    voice = "af_heart"

    def construct(self):
        T = ValueTracker(1.0)
        grow = ValueTracker(0.0)  # bars grow in once, then follow T
        bars = TrackerBars(lambda: softmax(T.get_value()), TOKENS, COLORS, grow=grow)

        # 1 — the task
        context = label("The  ___  sat on the mat.", size=34).to_corner(UL)
        with self.voiceover(text="A language model must pick the next word. "
                                 "Here it has four candidates: cat, dog, fox, and owl."):
            self.play(FadeIn(context, shift=DOWN * 0.2))
            self.play(LaggedStart(*[FadeIn(n, shift=UP * 0.2) for n in bars.names], lag_ratio=0.3))

        # 2 — logits on a number line; each dot sits at z / T
        axis = LabeledNumberLine([-4.5, 8.5, 1], 11, labels=(-4, 0, 4, 8), axis_name="z / T").move_to(UP * 1.2)
        dots = VGroup(*[Dot(axis.n2p(z), radius=0.11, color=c) for z, c in zip(LOGITS, COLORS)])
        for dot, z in zip(dots, LOGITS):
            dot.add_updater(lambda d, z=z: d.move_to(axis.n2p(z / T.get_value())))
        dot_names = stagger_labels([label(f"{n} {z:+.1f}", size=22, color=c) for n, z, c in zip(TOKENS, LOGITS, COLORS)],
                                   [axis.n2p(z) for z in LOGITS])
        with self.voiceover(text="The model gives each candidate a score. <bookmark mark='line'/> "
                                 "The score is called a logit. Cat has the highest logit."):
            self.play(Create(axis.line), FadeIn(axis.tick_labels), FadeIn(axis.axis_name))
            self.wait_until_bookmark("line")
            self.play(LaggedStart(*[GrowFromCenter(d) for d in dots], lag_ratio=0.25),
                      LaggedStart(*[FadeIn(n) for n in dot_names], lag_ratio=0.25))

        # 3 — softmax → bars
        t_readout = LiveNumber(lambda: f"T = {T.get_value():.2f}", size=36, place=lambda m: m.to_corner(UR))
        with self.voiceover(text="Softmax turns the logits into probabilities. <bookmark mark='bars'/> "
                                 "At temperature one, cat gets sixty-one percent."):
            self.wait_until_bookmark("bars")
            self.add(bars.bars, bars.value_labels)
            self.play(grow.animate.set_value(1), FadeIn(t_readout), run_time=1.5)

        # 4 — low T
        with self.voiceover(text="Temperature divides every logit before softmax. <bookmark mark='cold'/> "
                                 "At T equal to one half, the logits move apart. Cat now gets eighty-four percent."):
            self.wait_until_bookmark("cold")
            self.play(FadeOut(dot_names), T.animate.set_value(0.5), run_time=2.5)

        # 5 — predict first, then high T
        self.predict("When T rises to 2, does cat stay the most likely token?")
        with self.voiceover(text="Now raise the temperature. <bookmark mark='hot'/> At T equal to two, "
                                 "the logits move together. The probabilities become more equal."):
            self.wait_until_bookmark("hot")
            self.play(T.animate.set_value(2.0), run_time=3)

        # 6 — why: the distance between two dots sets their probability ratio
        def gap_marker():
            t = T.get_value()
            a, b = axis.n2p(LOGITS[1] / t) + DOWN * 0.75, axis.n2p(LOGITS[0] / t) + DOWN * 0.75
            seg = Line(a, b, color=Role.FOCUS, stroke_width=4)
            ends = VGroup(*[Line(p + UP * 0.12, p + DOWN * 0.12, color=Role.FOCUS, stroke_width=4) for p in (a, b)])
            text = label(f"p(cat) / p(dog) = {exp((LOGITS[0] - LOGITS[1]) / t):.2f}", size=26,
                         color=Role.FOCUS).next_to(seg, DOWN, buff=0.15)
            return VGroup(seg, ends, text)

        gap = always_redraw(gap_marker)
        with self.voiceover(text="Why does this happen? <bookmark mark='gap'/> The ratio of two probabilities "
                                 "depends only on the distance between their dots. <bookmark mark='move'/> "
                                 "A larger distance gives a larger ratio. A smaller distance gives a ratio "
                                 "closer to one."):
            self.wait_until_bookmark("gap")
            self.play(FadeIn(gap))
            self.wait_until_bookmark("move")
            self.play(T.animate.set_value(0.5), run_time=2.5)
            self.play(T.animate.set_value(4.0), run_time=2.5)

        # 6b — why exp: the simpler normalizer fails; exp turns a gap into a ratio
        gap.clear_updaters()  # freeze before fading: its glyph count changes with T
        S = M["sum_normalization"]
        # each alternative value sits in its token's column, so −0.4 reads as owl's
        values = VGroup(*[label(f"{S[t]:.1f}", size=28, color=Role.BAD if S[t] < 0 else Role.TEXT)
                          .move_to([bars.names[i].get_x(), -0.15, 0]) for i, t in enumerate(TOKENS)])
        alt = VGroup(label("÷ sum of logits:", size=24).next_to(values, LEFT, buff=0.5), values)
        law = MathTex(r"\frac{e^{a}}{e^{b}} = e^{a-b}", color=Role.FOCUS).move_to(DOWN * 0.15)
        with self.voiceover(text="Why exp, and not something simpler? <bookmark mark='alt'/> Divide each logit "
                                 "by their sum, and owl gets minus zero point four. A probability cannot be "
                                 "negative. <bookmark mark='exp'/> Exp makes every weight positive and keeps "
                                 "the order. And it turns a gap into a ratio. That is why only the distance "
                                 "between the dots matters."):
            self.play(FadeOut(gap), run_time=0.5)
            self.wait_until_bookmark("alt")
            self.play(FadeIn(alt, shift=UP * 0.1))
            self.play(Indicate(alt[1][3], color=Role.BAD))
            self.wait_until_bookmark("exp")
            self.claim("why-exp")
            self.play(FadeOut(alt), Write(law))
        self.wait(1.2)
        self.play(FadeOut(law), run_time=0.5)

        # 7 — limits
        with self.voiceover(text="At a very low temperature, the top token takes almost all the probability. "
                                 "<bookmark mark='uni'/> At a very high temperature, every token gets almost "
                                 "the same probability."):
            self.play(T.animate.set_value(0.25), run_time=2.5)
            self.wait_until_bookmark("uni")
            self.play(T.animate.set_value(10.0), run_time=3)

        # 8 — the ranking never changes
        formula = MathTex(r"p_i = \frac{e^{z_i / T}}{\sum_j e^{z_j / T}}", color=Role.ENTITY).scale(0.8).to_corner(UL)
        with self.voiceover(text="In every case, the order stays the same. Cat is always first, and owl is "
                                 "always last. <bookmark mark='formula'/> Temperature changes only the spread."):
            self.play(T.animate.set_value(1.0), run_time=2)
            self.claim("guarantee-order")
            self.play(Indicate(bars.names[0], color=Role.FOCUS), Indicate(bars.names[3], color=Role.FOCUS))
            self.wait_until_bookmark("formula")
            self.play(FadeOut(context, shift=UP * 0.2), Write(formula))
        self.wait(1.5)
