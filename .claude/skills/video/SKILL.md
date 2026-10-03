---
name: video
description: Make a 3Blue1Brown-style animated explainer with synchronized local voiceover (Manim + Kokoro, no API keys). Use when the user asks for an explainer video, animation, 3b1b-style video, or narrated walkthrough of a concept, or invokes /video <topic>.
---

# Video — 3b1b-style explainer with voiceover

This is the explain pipeline with the stage fixed to 4. The rules are in `CLAUDE.md` and `.claude/skills/explain/references/video.md`. Read `video.md` first.

If the subject has no dynamic change (no transformation, motion, iteration, or propagation), say so in one line and propose a lower stage. Make the video anyway if the user confirms.

## Procedure

1. **Scaffold.** `uv run explainer new <slug>`. If `models/` is empty, run `uv run explainer setup` first.
2. **Model.** Fill `explainers/<slug>/model.md` (template sections). Keep it minimal.
3. **Storyboard.** Fill `video/storyboard.md`: objective, sequence, scene table with bookmarks, object inventory, timing. Write the narration in STE-80.
4. **Scene code.** Write `video/scene.py` on `ExplainerScene`. One voiceover block per statement; time animations to the tracker and bookmarks.
5. **Draft.** `uv run explainer render <slug> --draft`. Read `draft-contact.png`. Fix layout and pacing.
6. **Final.** `uv run explainer render <slug>`. Read `contact.png` and `captions.srt`. Check frames at bookmark times.
7. **Verify.** Run the seven understanding questions in `CLAUDE.md` §7. Revise and re-render if one fails. Voice clips are cached, so re-renders are cheap.
8. **Deliver.** Give the path to `out.mp4` (open it with `open <path>` on macOS if the user wants), the length, the voice, and one line on what the viewer can now predict.

Reference implementation: `explainers/ste-80/`.
