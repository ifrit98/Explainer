# Animated explainer mode (3b1b style + voiceover)

Create an animated explainer when the subject depends on dynamic change: movement, time, transformation, emergence, an algorithm executing, geometry changing, a signal propagating, data flowing, or repeated iteration.

Do not make a narrated slide deck.

The default stack runs on one machine with no API keys:

| Layer | Tool |
|---|---|
| Animation | Manim Community (`manim`), LaTeX optional (TinyTeX, found automatically) |
| Voice sync | `manim-voiceover` (`with self.voiceover(...)`, bookmarks) |
| Voice | Kokoro-82M, local, via `explainer_kit.KokoroService` |
| House style | `ExplainerScene`, `Role` colors, `label()`, `words.sentence()` / `words.morph()` |
| Components | `explainer_kit.components`: `TrackerBars`, `LiveNumber`, `LabeledNumberLine`, `stagger_labels` |
| Assembly | `explainer render` → join scenes, -16 LUFS, soft captions (.srt + .vtt), chapters, timeline, contact sheet |
| Review | `explainer review` → one frame per narration line, bookmark, and predict pause, with layout issues |

CLI: `explainer <command>` with the plugin; `uv run explainer <command>` in the Explainer repo.

## 1. Visual language

- Persistent visual objects. An object that represents one entity stays the same object for the whole video.
- Transformations, not slide changes. Move, morph, recolor. Do not clear the screen between ideas.
- Spatial reasoning. Position encodes structure (left → right = sequence, up → down = level).
- Minimal on-screen text. The narration carries the words; the screen carries the evidence.
- Color encodes meaning through `Role` (ENTITY, FOCUS, RELATION, MUTED, GOOD, BAD, ASSUMPTION, QUANTITY). One meaning per color for the whole video. Categorical identities (tokens, players, odd numbers) get their own fixed colors.
- Progressive construction. Introduce no object before the viewer needs it.
- Deliberate pacing. Leave about 0.5 s of stillness after each important change.

Every scene must answer one specific conceptual question.

## 2. Pre-production (before any scene code)

1. `explainer new <slug> --stage 4`.
2. Fill `model.md` and `model.yaml`. Every number the narration speaks or a label shows goes in `values`.
3. Fill `video/storyboard.md`: objective, conceptual sequence, scene table with bookmarks, object inventory, timing (about 2.6 words per second), predict pauses, rendering plan.
4. Write the narration in STE-80. Short sentences read well aloud, and sentence ends are natural bookmark points.

## 3. Scene code

```python
from manim import *
from explainer_kit import ExplainerScene, Role, label, load_model
from explainer_kit.components import LiveNumber, TrackerBars

M = load_model(__file__)                   # values from model.yaml: the scene cannot drift from the model

class MyTopic(ExplainerScene):
    voice = "af_heart"                     # explainer voices
    lexicon = {"QKᵀ": "Q K transpose"}     # spoken form for TTS; captions keep the written form

    def construct(self):
        T = ValueTracker(1.0)
        with self.voiceover(text="Each token asks a question. <bookmark mark='q'/> The question is a vector.") as tracker:
            self.play(FadeIn(tokens))
            self.wait_until_bookmark("q")
            self.play(GrowArrow(q_arrow), run_time=tracker.get_remaining_duration())
        self.predict("What happens to the weights when T doubles?")   # predict-first pause
```

Rules:

- One `with self.voiceover(...)` block per narration statement. The animation inside the block is the visual evidence for that statement.
- Time animations to the voice: `run_time=tracker.duration`, `tracker.time_until_bookmark("x")`, `self.wait_until_bookmark("x")`, `tracker.get_remaining_duration()`. Do not hard-code durations that must match speech.
- Bookmark and sentence times are exact: `KokoroService` synthesizes each bookmark segment and each sentence separately. Put bookmarks at clause or sentence boundaries; a split inside a phrase breaks the intonation.
- Drive related objects from one `ValueTracker`. Use `TrackerBars` and `LiveNumber` instead of hand-written `always_redraw` code.
- Call `.freeze()` (or `clear_updaters()`) on a live label before `FadeOut` or `Transform` while its text is changing. Otherwise the animation fails on a changing glyph count.
- Use `words.sentence()` and `words.morph()` when text changes. Kept words move, removed words fade out, added words fade in.
- `self.predict(question)` dims the frame, shows a "Pause and predict" card, speaks the question, and records a predict event. Players built with the web toolkit pause there; the MP4 gets a chapter.
- Several `class X(ExplainerScene)` in one `scene.py` render in file order and are joined. Use one class per chapter for long videos.
- LaTeX: `MathTex`, `Tex`, `DecimalNumber`, `BraceLabel`, and `NumberLine(include_numbers=True)` need it (`Brace` alone does not). `explainer setup` reports whether LaTeX is available and how to install TinyTeX without a password. Without LaTeX, use `label()` and `LabeledNumberLine`.
- If a scene raises an exception, `ExplainerScene` prints it and exits at once. (Plain manim can hang after an error inside an animation.)

## 4. Render loop

```bash
explainer check <slug>                     # narration and labels against model.yaml
explainer render <slug> --draft --review   # 480p15, silent estimated timing: layout and pacing
explainer render <slug> --review           # 1080p60, Kokoro voice, mastered audio, captions, chapters
explainer render <slug> --scene Intro -q m # one chapter at 720p
explainer say "Test this line." --voice am_michael   # audition a voice or a pronunciation
```

Output in `explainers/<slug>/video/`: `out.mp4` (soft captions, chapters), `captions.srt` and `.vtt`, `timeline.json` (lines, bookmarks, predict pauses), `contact.png`, `review.png`. Drafts write `draft-*` files. Voice clips are cached in `media/voiceovers/`; a re-render synthesizes only changed lines.

## 5. Review (always, before delivery)

1. Read `review.png`: one frame at each narration line, bookmark, and predict pause, with the spoken text under it. Check that each frame shows the evidence for its line, and that objects persist instead of reappearing.
2. Fix every layout issue that `render` and `review` list. The scene checks visible text at each bookmark and at the end of each line: `overlap` (text on text), `covered` (an opaque panel from another group over text), `off-frame`. The check does not see text crossing lines or arrows; look for that in the frames.
3. Read `captions.srt` against the narration.
4. For published videos, run the blind understanding test (`verify` skill).

## 6. Voice

| Option | When |
|---|---|
| Kokoro (default) | After `explainer setup`. Good voices: `af_heart`, `af_bella`, `am_michael`, `am_fenrir`, `bm_george`. |
| `EXPLAINER_TTS=silent` | Layout drafts (`--draft` sets it). |
| manim-voiceover cloud services (`ElevenLabsService`, `OpenAIService`, `AzureService`) | Only when the user asks and the key is set. Call `self.set_speech_service(...)` in `setup()` after `super().setup()`. |

Use the lexicon for acronyms, symbols, and names that Kokoro mispronounces. Test them with `explainer say`. Word-level timing inside a sentence is not available: the ONNX Kokoro model returns audio without durations.

## 7. Optional: showtime

[showtime](https://github.com/FavioVazquez/showtime) is a user-level Claude Code plugin for local video production (HTML/canvas motion graphics in headless Chrome, Manim, Kokoro/Piper voices with forced-alignment word timings, audio mastering, footage editing). Install: `/plugin marketplace add FavioVazquez/showtime` then `/plugin install showtime@showtime`.

Use this pipeline by default: it is pinned and checks renderings against the model. Use showtime when the user asks for it or when the video needs what this pipeline lacks: HTML motion graphics, music or sound effects, word-level timing, or real footage.
