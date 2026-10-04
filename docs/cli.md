# CLI reference

With the plugin installed, run `explainer <command>` from any project. In the Explainer repo, run `uv run explainer <command>`. Explainers live in `<project>/explainers/<slug>/`; the project root is the nearest folder above the working directory that has `explainers/` or `.git` (override with `--root` or `EXPLAINER_ROOT`).

| Command | Does |
|---|---|
| `explainer setup` | Download the Kokoro voice (about 350 MB) and report which tools are present, including LaTeX. |
| `explainer new <slug> [--stage 1 2 3 4]` | Create `model.md`, `model.yaml`, and the chosen renderings from templates. Default stage: 4. Existing files are kept. |
| `explainer check [slug ...]` | Hold renderings to `model.yaml`. No slug: every explainer. Exit code 1 on any problem. `-v` lists notes. |
| `explainer sync <slug>` | Write the model's values and the current web toolkit into the slug's HTML pages. |
| `explainer render <slug> [options]` | Render the video: voice, mastered audio, captions, chapters, timeline, contact sheet. |
| `explainer review <slug> [--draft]` | Build the review sheet: one frame at each narration line, bookmark, and predict pause. |
| `explainer quiz <slug> --rendering R` | Print the blind-test prompt for one rendering (`prose`, `diagram`, `html`, `video`). |
| `explainer quiz <slug> --rubric` | Print the expected answers, for scoring a blind test. |
| `explainer voices [--all]` | List Kokoro voices. English by default. |
| `explainer say "<text>" [--voice V] [--speed S]` | Synthesize one line and play it. Use it to choose a voice or test a lexicon spelling. |
| `explainer frames <slug> [--draft] [--every N]` | Rebuild the contact sheet from an existing render. |

## `check`

`check` reads each rendering the way a reader meets it:

| Rendering | What counts |
|---|---|
| `explanation.md`, `diagram.md` | visible text and Mermaid labels and data. Not code blocks, link targets, or Mermaid styling. |
| `index.html` | visible text. The page loads the model when it has a synced `explainer-model` block. |
| `video/scene.py` | string constants: narration, labels, on-screen math. Spoken numbers count ("sixty-one percent" is 61%). The scene loads the model when it calls `load_model(...)`. |

It reports three kinds of problem:

1. **A number the model does not explain.** Compared at the shown precision: 0.84 matches 0.842, 84% matches 0.842, 2 does not stand for 2.5. Stage, step, rule, and section numbers, years, and identifiers (STE-80, v2.3.0, SHA-256) are skipped.
2. **A required value that a rendering does not show.** From `require` in `model.yaml`. A rendering that loads the model passes by construction.
3. **A stale page.** The embedded model or the inlined toolkit differs from the current one. Fix with `explainer sync`.

## `render` options

| Option | Default | Meaning |
|---|---|---|
| `--draft` | off | 480p15 and silent narration with estimated timing. Writes `draft*` files. |
| `-q {l,m,h,k}` | `h` (`l` with `--draft`) | 480p15, 720p30, 1080p60, 2160p60 |
| `--scene NAME` | all | Render one scene class only. |
| `--review` | off | Also build the review sheet. |
| `--every N` | `4` | Seconds between contact-sheet frames. |

`render` prints any layout issue the scene found: text that overlaps text, text covered by another group's opaque panel, or text outside the frame.

## Output of a video

```text
explainers/<slug>/video/
  out.mp4          final video: soft captions, chapters (one per predict pause)
  captions.srt     sidecar captions, sentence-timed; captions.vtt for <track>
  timeline.json    narration lines, bookmarks, predict pauses, layout issues, with times
  review.png       review sheet
  contact.png      one frame every --every seconds
  media/           Manim cache, scene renders, voice clips (git-ignored)
```

## Environment variables

| Variable | Meaning |
|---|---|
| `EXPLAINER_ROOT` | Project root (same as `--root`). |
| `EXPLAINER_TTS` | `kokoro` (default) or `silent`. |
| `EXPLAINER_VOICE` | Default voice, e.g. `am_michael`. |
| `EXPLAINER_KOKORO_DIR` | Where the voice model lives. Default: `models/` in a checkout, else `~/.cache/explainer/models`. |
| `EXPLAINER_SOURCE` | For the plugin's `bin/explainer`: a local checkout or git URL to run instead of the pinned release. |

## Voices

The best English voices are `af_heart`, `af_bella`, `am_michael`, `am_fenrir`, and `bm_george`. Prefix: `a` = American, `b` = British; `f` = female, `m` = male.
