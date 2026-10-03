# Animated explainer mode (3b1b style + voiceover)

Create an animated explainer when the subject depends on dynamic change: movement, time, transformation, emergence, an algorithm executing, geometry changing, a signal propagating, data flowing, or repeated iteration.

Do not make a narrated slide deck.

The default stack runs on one machine with no API keys:

| Layer | Tool |
|---|---|
| Animation | Manim Community (`manim`) |
| Voice sync | `manim-voiceover` (`with self.voiceover(...)`, bookmarks) |
| Voice | Kokoro-82M, local, via `explainer_kit.KokoroService` |
| House style | `explainer_kit.ExplainerScene`, `Role` colors, `label()`, `words.sentence()` / `words.morph()` |
| Assembly | `uv run explainer render` → FFmpeg concat, -16 LUFS mastering, soft captions, contact sheet |

Reference implementation: `explainers/ste-80/` (model → storyboard → scene → out.mp4).

## 1. Visual language

- Persistent visual objects. An object that represents one entity stays the same object for the whole video.
- Transformations, not slide changes. Move, morph, recolor. Do not clear the screen between ideas.
- Spatial reasoning. Position encodes structure (left → right = sequence, up → down = level).
- Minimal on-screen text. The narration carries the words; the screen carries the evidence.
- Color encodes meaning through `Role` (ENTITY, FOCUS, RELATION, MUTED, GOOD, BAD, ASSUMPTION, QUANTITY). One meaning per color for the whole video.
- Progressive construction. Introduce no object before the viewer needs it.
- Deliberate pacing. Leave about 0.5 s of stillness after each important change.

Every scene must answer one specific conceptual question.

## 2. Pre-production (before any scene code)

1. Update `explainers/<slug>/model.md`. Set the stage to 4 and give the reason.
2. Fill in `explainers/<slug>/video/storyboard.md`:
   1. learning objective;
   2. conceptual sequence (from the model's dependencies and causal chain);
   3. scene table: question, visual transformation, bookmarks;
   4. visual-object inventory: role color, first scene, persistence, what it becomes;
   5. timing (narration is about 2.6 words per second);
   6. rendering plan: voice, lexicon entries, MathTex yes/no.
3. Write the narration in STE-80. Short sentences read well aloud, and sentence ends are natural bookmark points.

## 3. Scene code

Scaffold with `uv run explainer new <slug>`. Then edit `video/scene.py`:

```python
from manim import *
from explainer_kit import ExplainerScene, Role, label
from explainer_kit.words import sentence, morph

class MyTopic(ExplainerScene):
    voice = "af_heart"                     # uv run explainer voices
    lexicon = {"QKᵀ": "Q K transpose"}     # spoken form for TTS; captions keep the written form

    def construct(self):
        with self.voiceover(text="Each token asks a question. <bookmark mark='q'/> The question is a vector.") as tracker:
            self.play(FadeIn(tokens))
            self.wait_until_bookmark("q")
            self.play(GrowArrow(q_arrow), run_time=tracker.get_remaining_duration())
```

Rules:

- One `with self.voiceover(...)` block per narration statement. The animation inside the block is the visual evidence for that statement.
- Time animations to the voice: `run_time=tracker.duration`, `tracker.time_until_bookmark("x")`, `self.wait_until_bookmark("x")`, `tracker.get_remaining_duration()`. Do not hard-code durations that must match speech.
- Put bookmarks at clause or sentence boundaries. `KokoroService` synthesizes each bookmark segment separately, so the bookmark times are exact, but a bookmark in the middle of a phrase breaks the prosody.
- Use `words.sentence()` and `words.morph()` when text changes. Kept words move, removed words fade out, added words fade in.
- Several `class X(ExplainerScene)` in one `scene.py` render in file order and are joined. Use one class per chapter for long videos; each chapter re-renders independently.
- `MathTex` / `Tex` need LaTeX (not installed by default; `brew install --cask basictex`). Use `label()` / `Text` when LaTeX is missing.
- `DecimalNumber`, `Integer`, `BraceLabel`, and `NumberLine(include_numbers=True)` also need LaTeX (`Brace` alone does not). For a live number, use `always_redraw(lambda: label(f"{tracker.get_value():.0f}"))`.

## 4. Render loop

```bash
uv run explainer render <slug> --draft   # 480p15, silent estimated narration: layout and pacing
uv run explainer render <slug>           # 1080p60, Kokoro voice, mastered audio, captions
uv run explainer render <slug> --scene Intro -q m   # one chapter at 720p
uv run explainer say "Test this line." --voice am_michael   # audition a voice or a pronunciation
```

Output in `explainers/<slug>/video/`: `out.mp4` (captions muxed as a soft track), `captions.srt`, `contact.png`. Voice clips are cached in `media/voiceovers/`; a re-render synthesizes only changed lines.

## 5. Review (always, before delivery)

1. Read `contact.png` (one frame every `--every` seconds). Check layout, overlaps, legibility, and that objects persist instead of reappearing.
2. Check sync: for each bookmark, extract the frame just after it (`ffmpeg -ss <t> -i out.mp4 -frames:v 1 f.png`) and confirm the visual evidence is on screen. Bookmark times are in `media/voiceovers/cache.json` (`word_boundaries`, units of 1e-7 s).
3. Read `captions.srt`. Every caption must match the narration.
4. Run the seven understanding questions from `CLAUDE.md` §7.

## 6. Voice

| Option | When |
|---|---|
| Kokoro (default) | Always available after `uv run explainer setup`. Good voices: `af_heart`, `af_bella`, `am_michael`, `am_fenrir`, `bm_george`. |
| `EXPLAINER_TTS=silent` | Layout drafts (`--draft` sets it). |
| manim-voiceover cloud services (`ElevenLabsService`, `OpenAIService`, `AzureService`) | Only when the user asks and the key is set. Call `self.set_speech_service(...)` in `setup()` after `super().setup()`. |

Use the lexicon for acronyms, symbols, and names that Kokoro mispronounces. Test them with `explainer say`.

## 7. Optional: showtime

[showtime](https://github.com/FavioVazquez/showtime) is a user-level Claude Code plugin for local video production (HTML/canvas motion graphics in headless Chrome, Manim, Kokoro/Piper voices with forced-alignment word timings, audio mastering, footage editing). Install: `/plugin marketplace add FavioVazquez/showtime` then `/plugin install showtime@showtime`.

Use the in-repo pipeline by default: it is pinned in `uv.lock` and works from a fresh clone. Use showtime when the user asks for it or when the video needs what this pipeline lacks: HTML motion graphics, music or sound effects, or real footage.
