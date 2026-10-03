"""ste-80 — one sentence, three STE rules. See ../model.md and storyboard.md.

Render:  uv run explainer render ste-80 --draft
         uv run explainer render ste-80
"""

from manim import *

from explainer_kit import ExplainerScene, Role, label
from explainer_kit.words import added_words, morph, removed_words, sentence

S = [
    "It is imperative that the operator ensures the hydraulic reservoir is replenished prior to commencing operation.",
    "It is imperative that the operator ensures the hydraulic reservoir is full before starting the operation.",
    "Make sure that the hydraulic reservoir is full before you start the operation.",
    "Fill the hydraulic reservoir before you start the machine.",
]
RULES = ["1   Use simple words", "2   Give the instruction directly", "3   Use a concrete verb"]
SENTENCE_POS = DOWN * 0.1
WORD_UNIT = 0.35  # meter width per word


class Ste80(ExplainerScene):
    voice = "af_heart"
    lexicon = {"STE-80": "S T E eighty", "ASD-STE100": "A S D, S T E one hundred"}

    def construct(self):
        # 1 — What is STE-80?
        title = label("STE-80", size=80, color=Role.ENTITY)
        subtitle = label("a writing style for technical text", size=32).next_to(title, DOWN, buff=0.35)
        with self.voiceover(text="This is STE-80. It is a writing style for technical text. "
                                 "It uses most of the rules of ASD-STE100.") as tracker:
            self.play(Write(title), run_time=1.5)
            self.play(FadeIn(subtitle, shift=UP * 0.2))
        self.play(title.animate.scale(0.4).to_corner(UL), FadeOut(subtitle))

        # 2 — What is the problem?
        words = sentence(S[0]).move_to(SENTENCE_POS)
        self.count = ValueTracker(0)
        bar = always_redraw(lambda: Rectangle(
            width=max(self.count.get_value() * WORD_UNIT, 1e-3), height=0.22, stroke_width=0,
            fill_color=Role.QUANTITY, fill_opacity=1,
        ).move_to(LEFT * 2.8 + DOWN * 2.9, aligned_edge=LEFT))
        number = always_redraw(lambda: label(f"{round(self.count.get_value())} words", size=28,
                                             color=Role.QUANTITY).next_to(bar, RIGHT, buff=0.25))
        with self.voiceover(text="Here is a typical sentence from a manual. <bookmark mark='count'/> "
                                 "It has sixteen words. Some of the words do not help the reader.") as tracker:
            self.play(LaggedStart(*[FadeIn(w, shift=UP * 0.1) for w in words], lag_ratio=0.08),
                      run_time=tracker.time_until_bookmark("count"))
            self.wait_until_bookmark("count")
            self.add(bar, number)
            self.play(self.count.animate.set_value(len(words)), run_time=1.5)

        # 3–5 — One rule per rewrite
        self.tags = VGroup(*[label(r, size=26, color=Role.FOCUS) for r in RULES])
        self.tags.arrange(DOWN, aligned_edge=LEFT, buff=0.22).next_to(title, DOWN, aligned_edge=LEFT, buff=0.45)

        words = self.rewrite(words, S[1], 0,
                             "Rule one. Use simple words. <bookmark mark='mark'/> Replenished becomes full. "
                             "Prior to becomes before. Commencing becomes starting. <bookmark mark='swap'/> "
                             "The length does not change. But each word is easier to read.")
        words = self.rewrite(words, S[2], 1,
                             "Rule two. Give the instruction directly. <bookmark mark='mark'/> "
                             "Remove the frame around the instruction, and talk to the reader. "
                             "<bookmark mark='swap'/> The sentence now has thirteen words.")
        words = self.rewrite(words, S[3], 2,
                             "Rule three. Use a concrete verb. <bookmark mark='mark'/> "
                             "The words make sure and is full describe a state. The verb fill names the action. Operation becomes machine. "
                             "<bookmark mark='swap'/> The sentence now has nine words.")

        # 6 — What changed overall?
        before = sentence(S[0], size=26, color=Role.TEXT).set_opacity(0.4).move_to(UP * 2.0)
        with self.voiceover(text="Sixteen words became nine. <bookmark mark='compare'/> "
                                 "The instruction did not change. The reader does less work.") as tracker:
            self.play(FadeOut(self.tags), run_time=0.6)
            self.wait_until_bookmark("compare")
            self.play(FadeIn(before, shift=DOWN * 0.2), words.animate.scale(1.15).move_to(DOWN * 0.4))
        self.wait(1)

    def rewrite(self, old: VGroup, new_text: str, rule: int, narration: str) -> VGroup:
        """Show rule tag, mark the words the rule removes, then morph into the new sentence."""
        new = sentence(new_text).move_to(SENTENCE_POS)
        removed = removed_words(old, new)
        added = added_words(old, new).set_color(Role.GOOD)
        with self.voiceover(text=narration):
            self.play(FadeIn(self.tags[rule], shift=RIGHT * 0.2),
                      *[t.animate.set_color(Role.MUTED) for t in self.tags[:rule]])
            self.wait_until_bookmark("mark")
            self.play(removed.animate.set_color(Role.BAD), run_time=0.6)
            self.wait_until_bookmark("swap")
            self.play(*morph(old, new), self.count.animate.set_value(len(new)), run_time=1.5)
        self.play(added.animate.set_color(Role.TEXT), run_time=0.5)
        return new
