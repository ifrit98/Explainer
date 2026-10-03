"""{{slug}} — 3b1b-style explainer.

Render:  uv run explainer render {{slug}} --draft   (layout pass, silent)
         uv run explainer render {{slug}}           (final, Kokoro voice)

Rules (see .claude/skills/explain/references/video.md):
- One `with self.voiceover(...)` block per narration statement. The animation inside
  the block is the visual evidence for that statement.
- Time animations to the voice: run_time=tracker.duration, or
  self.wait_until_bookmark("x") for a <bookmark mark='x'/> inside the text.
- Transform existing objects. Do not clear the screen between ideas.
- Entity names and colors come from model.md and Role.
"""

from manim import *

from explainer_kit import ExplainerScene, Role, label


class {{ClassName}}(ExplainerScene):
    voice = "af_heart"
    lexicon = {}  # written form -> spoken form, for example {"QKᵀ": "Q K transpose"}

    def construct(self):
        title = label("{{slug}}", size=48, color=Role.ENTITY)

        with self.voiceover(text="This video explains one idea.") as tracker:
            self.play(Write(title), run_time=tracker.duration)

        with self.voiceover(text="First we show the object. <bookmark mark='move'/> Then we move it.") as tracker:
            dot = Dot(color=Role.FOCUS).next_to(title, DOWN, buff=1)
            self.play(FadeIn(dot))
            self.wait_until_bookmark("move")
            self.play(dot.animate.shift(RIGHT * 3), run_time=tracker.get_remaining_duration())

        self.wait(0.5)
