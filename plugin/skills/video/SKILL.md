---
name: video
description: Make a 3Blue1Brown-style animated explainer with synchronized local voiceover (Manim + Kokoro, no API keys). Use when the user asks for an explainer video, animation, 3b1b-style video, or narrated walkthrough of a concept, or invokes /video <topic>.
---

# Video — 3b1b-style explainer with voiceover

This is the explain pipeline with the stage fixed to 4. Read `../explain/references/principles.md` and `../explain/references/video.md` first.

If the subject has no dynamic change (no transformation, motion, iteration, or propagation), say so in one line and propose a lower stage. Make the video anyway if the user confirms.

A video costs the viewer its full length; they cannot skim it. Aim for the shortest video that carries the argument: the default budget is 150 s. Above that, set `budget.video` with a reason in `model.yaml`.

**CLI.** `explainer <command>` with the plugin; `uv run explainer <command>` inside the Explainer repo. Run `explainer setup` once: it downloads the voice and reports whether LaTeX is available for `MathTex`.

## Procedure

1. **Scaffold.** `explainer new <slug> --stage 4`.
2. **Model.** Fill `model.md` and `model.yaml` (values the narration and labels use, `claims`, `require`, `quiz`). Run `explainer probe <slug>` with a fresh subagent before you storyboard; recompute its numbers.
3. **Narrative.** Fill `narrative.md` (principles §11): question and motive, the introduction ledger, and the beats with what is shown and said. Run `explainer coldread <slug> --rendering narrative` with a fresh subagent. Fix what blocks and cut what is excess before you storyboard.
4. **Storyboard.** Fill `video/storyboard.md` from the beats: scene table with bookmarks, object inventory, timing, predict pauses. Write the narration in STE-80.
5. **Scene code.** Write `video/scene.py` on `ExplainerScene`. Read values with `load_model(__file__)`. One voiceover block per statement; time animations to the tracker and bookmarks. Use `explainer_kit.components` (TrackerBars, LiveNumber, LabeledNumberLine, stagger_labels) before writing your own. Add `self.predict(...)` before the result a learner should predict. Call `self.claim("id")` where each claim is shown, with its case on screen.
6. **Check.** `explainer check <slug>`. Fix every number the model does not explain.
7. **Draft.** `explainer render <slug> --draft --review`. Read `draft-review.png`. Fix every layout issue it lists (overlap, covered, off-frame), every pace issue (a claim with no pause after it, or a long line over one picture: split it, one step per bookmark), and every frame where the visual evidence is late or missing. Silent drafts speak a little slower than the voice, so the final render decides pace.
8. **Final.** `explainer render <slug> --review`. Read `review.png` and `captions.srt`. At each claim frame, check that the screen shows what the narration says. Fix any pace issue it still reports.
9. **Verify.** Follow the `verify` skill: the cold read of the video, then the blind understanding test when the video will be published.
10. **Deliver.** On a page, play the video with `Explainer.video` so it stops at the predict pauses (`explainer check` fails a plain `<video>`). Give the path to `out.mp4`, the length, the voice, the number of predict pauses, and one line on what the viewer can now predict.

Reference implementations: `explainers/softmax-temperature/` (one tracker drives everything), `explainers/odd-squares/` (a proof compiled from `narrative.md`, beat by beat, with a predict pause), `explainers/dijkstra/` (an algorithm replayed from the model).
