"""ste-80 — one sentence, three STE rules. See ../model.md and storyboard.md.

Render:  uv run explainer render ste-80 --draft
         uv run explainer render ste-80
"""

from manim import *

from explainer_kit import ExplainerScene, Role, label, load_model
from explainer_kit.words import added_words, morph, removed_words, sentence

M = load_model(__file__)
S = M["sentences"]
RULES = [f"{i}   {rule}" for i, rule in enumerate(M["rules"], 1)]
SENTENCE_POS = DOWN * 0.1
WORD_UNIT = 0.35  # meter width per word


class Ste80(ExplainerScene):
    voice = "af_heart"
    lexicon = {"STE-80": "S T E eighty", "ASD-STE100": "A S D, S T E one hundred"}

    def construct(self):
        # 1 — What is STE-80?
        title = label("STE-80", size=80, color=Role.ENTITY)
        subtitle = label("a writing style for technical text", size=32).next_to(title, DOWN, buff=0.35)
        with self.voiceover(text="This is STE-80. It is a writing style for technical text.") as tracker:
            self.play(Write(title), run_time=1.5)
            self.play(FadeIn(subtitle, shift=UP * 0.2))
        source = VGroup(label("ASD-STE100: Simplified Technical English", size=30),
                        label("a standard for aircraft maintenance manuals", size=26, color=Role.MUTED),
                        ).arrange(DOWN, buff=0.18).next_to(subtitle, DOWN, buff=0.6)
        readers = label("read under time pressure, often in a second language", size=26, color=Role.FOCUS
                        ).next_to(source, DOWN, buff=0.45)
        with self.voiceover(text="It comes from ASD-STE100, Simplified Technical English, a standard for aircraft "
                                 "maintenance manuals. The eighty means about eighty percent of the way to strict "
                                 "STE: it keeps the writing rules and drops the approved dictionary. "
                                 "<bookmark mark='who'/> "
                                 "Manuals are read under time pressure, often in a second language, so every word "
                                 "must help.") as tracker:
            self.play(FadeIn(source, shift=UP * 0.15))
            self.wait_until_bookmark("who")
            self.play(FadeIn(readers, shift=UP * 0.15))
        self.play(title.animate.scale(0.4).to_corner(UL), FadeOut(subtitle), FadeOut(source), FadeOut(readers))

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
                                 "It has sixteen words: the orange bar counts them. Some of the words do not help the reader.") as tracker:
            self.play(LaggedStart(*[FadeIn(w, shift=UP * 0.1) for w in words], lag_ratio=0.08),
                      run_time=tracker.time_until_bookmark("count"))
            self.wait_until_bookmark("count")
            self.add(bar, number)
            self.play(self.count.animate.set_value(len(words)), run_time=1.5)

        # 3–5 — One rule per rewrite
        self.tags = VGroup(*[label(r, size=26, color=Role.FOCUS) for r in RULES])
        self.tags.arrange(DOWN, aligned_edge=LEFT, buff=0.22).next_to(title, DOWN, aligned_edge=LEFT, buff=0.45)

        words = self.rewrite(words, S[1], 0,
                             "Rule one. Use simple words: the common word, not the formal one. "
                             "<bookmark mark='mark'/> The words in red change. "
                             "<bookmark mark='swap'/> Replenished becomes full. Prior to becomes before. "
                             "Commencing becomes starting. Only one word goes, but each word is easier to read.",
                             claim=lambda: self.claim("limit-length"))
        words = self.rewrite(words, S[2], 1,
                             "Rule two. Give the instruction directly. <bookmark mark='mark'/> "
                             "Cut the opening that only says the instruction matters. <bookmark mark='swap'/> "
                             "Tell the reader what to do instead: make sure, before you start. Thirteen words.")
        words = self.rewrite(words, S[3], 2,
                             "Rule three. Use concrete words. <bookmark mark='mark'/> "
                             "The phrase make sure that it is full asks the reader to check a result. "
                             "<bookmark mark='swap'/> The verb fill names the action, and the machine names what you "
                             "start. Nine words.",
                             claim=lambda: self.claim("why-concrete-verb"))

        # 6 — What changed overall?
        before = sentence(S[0], size=26, color=Role.TEXT).set_opacity(0.4).move_to(UP * 2.0)
        with self.voiceover(text="Sixteen words became nine. <bookmark mark='compare'/> "
                                 "The reader still fills the reservoir before starting the machine, with less "
                                 "work to read it.") as tracker:
            self.play(FadeOut(self.tags), run_time=0.6)
            self.wait_until_bookmark("compare")
            self.claim("mechanism-rules")
            self.play(FadeIn(before, shift=DOWN * 0.2), words.animate.scale(1.15).move_to(DOWN * 0.4))
        self.wait(1)
        with self.voiceover(text="The bar counts words, but the goal is less work: rule one cut only one word and "
                                 "still helped."):
            self.play(Indicate(number, color=Role.FOCUS, scale_factor=1.2), run_time=1.2)
        self.wait(0.5)
        more = label("more STE-80 rules: short sentences · one meaning per word · no filler", size=24,
                     color=Role.MUTED).move_to(DOWN * 1.9)
        with self.voiceover(text="STE-80 has more rules than these three: short sentences, one meaning per word, "
                                 "and no filler."):
            self.play(FadeIn(more, shift=UP * 0.1))
        self.wait(1)

    def rewrite(self, old: VGroup, new_text: str, rule: int, narration: str, claim=None) -> VGroup:
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
            if claim:
                claim()   # marks the claim this rewrite shows
            self.play(*morph(old, new), self.count.animate.set_value(len(new)), run_time=1.5)
        self.play(added.animate.set_color(Role.TEXT), run_time=0.5)
        if claim:
            self.wait(1)   # a pause after a claim
        return new
