# CLI reference

With the plugin installed, run `explainer <command>` from any project. In the Explainer repo, run `uv run explainer <command>`. Explainers live in `<project>/explainers/<slug>/`; the project root is the nearest folder above the working directory that has `explainers/` or `.git` (override with `--root` or `EXPLAINER_ROOT`).

| Command | Does |
|---|---|
| `explainer setup` | Download the Kokoro voice (about 350 MB) and report which tools are present, including LaTeX. |
| `explainer new <slug> [--stage 1 2 3 4] [--quick]` | Create `model.md`, `model.yaml`, `narrative.md`, and the chosen renderings from templates. Default stage: 4. Existing files are kept. `--quick` skips `narrative.md` (the quick-artifact tier, principles §12). |
| `explainer check [slug ...]` | Hold renderings to `model.yaml`: numbers, required values, claims, terms, length. No slug: every explainer. Exit code 1 on any problem; `!` lines are warnings. `-v` lists notes. |
| `explainer probe <slug>` | Print a prompt for a fresh agent that reads only `model.md` and lists what the explanation will omit, for the audience the model names: each gap main or edge, and model entries the audience does not need. |
| `explainer coldread <slug> [--rendering R]` | Print a first-viewing prompt: a fresh agent reads one rendering (`narrative` by default, or `prose`, `diagram`, `html`, `video`) in order, as the audience in `model.md`, and reports every reference it was not given, everything shown but unsaid, every leap, and every excess: what it already knew, a repeat, a detour. It marks the findings that block the main line. `--rubric` prints the pass rule. |
| `explainer sync <slug>` | Write the model's values and the current web toolkit into the slug's HTML pages. |
| `explainer render <slug> [options]` | Render the video: voice, mastered audio, captions, chapters, timeline, contact sheet. |
| `explainer review <slug> [--draft]` | Build the review sheet: one frame at each narration line, bookmark, and predict pause. |
| `explainer quiz <slug> --rendering R` | Print the blind-test prompt for one rendering (`prose`, `diagram`, `html`, `video`). |
| `explainer quiz <slug> --rubric` | Print the expected answers, for scoring a blind test. |
| `explainer voices [--all]` | List Kokoro voices. English by default. |
| `explainer say "<text>" [--voice V] [--speed S]` | Synthesize one line and play it. Use it to choose a voice or test a lexicon spelling. |
| `explainer frames <slug> [--draft] [--every N]` | Rebuild the contact sheet from an existing render. |
| `explainer eval chat [--conditions name=source ...]` | Answer the questions in `evals/chat/questions.yaml` under several system prompts with fresh `claude -p` calls, grade them blind, and write a report. See [Evals](evals.md). |

## `check`

`check` reads each rendering the way a reader meets it:

| Rendering | What counts |
|---|---|
| `explanation.md`, `diagram.md` | visible text and Mermaid labels and data. Not code blocks, link targets, or Mermaid styling. |
| `index.html` | visible text. The page loads the model when it has a synced `explainer-model` block. |
| `video/scene.py` | string constants: narration, labels, on-screen math. Spoken numbers count ("sixty-one percent" is 61%). The scene loads the model when it calls `load_model(...)`. |

It reports these problems (full list with fixes: [model reference](model-reference.md#what-explainer-check-reports)):

1. **A number the model does not explain.** Compared at the shown precision: 0.84 matches 0.842, 84% matches 0.842, 2 does not stand for 2.5. Stage, step, rule, and section numbers, years, and identifiers (STE-80, v2.3.0, SHA-256) are skipped.
2. **A required value that a rendering does not show.** From `require` in `model.yaml`. A rendering that loads the model passes by construction.
3. **A stale page.** The embedded model or the inlined toolkit differs from the current one. Fix with `explainer sync`.
4. **An incomplete or uncovered claim.** A `why` claim without its alternative and counterexample, a `guarantee` without an example and a counterexample, or a rendering that does not mark a claim it should cover.
5. **A function with no why.** `model.md` names exp, log, sqrt, sigmoid, … and no `why` claim justifies it (or `accept_unjustified` gives a reason; `-v` lists each one).
6. **A second name for a concept.** A rendering uses a phrase that a `terms` entry avoids.
7. **A video without its predict pauses.** `index.html` plays a video that has predict pauses through a plain `<video>`; use `Explainer.video`.
8. **A symbol the narrative does not introduce.** With a `narrative.md`, a single-letter symbol in the scene's on-screen math or labels, or spoken as "the n-th", must be listed in the introduction ledger.
9. **Length.** A warning (`!`) when the prose is over 600 words or the video over 150 s; a failure when a rendering exceeds a `budget` declared in `model.yaml`. Length is a cost to the reader too: cut what this reader does not need, or declare the length with a reason.

`--diagrams` also renders every Mermaid block (Markdown fences and `<pre class="mermaid">`) with the Mermaid CLI: `mmdc` on PATH, else `npx` with a pinned version. It needs Node. CI runs it.

## `probe`

`explainer probe <slug>` prints a prompt for a fresh agent with no other context. The agent reads only `model.md` and reports, against six rules (why this form, guarantees with two cases, terms and one name per concept, worked examples, the meaning of each quantity, next questions), what the explanation will omit for the audience the model names. It marks each gap main or edge, and lists model entries that audience does not need. Recompute every number it suggests, and adopt a finding only when this reader needs it: a probe always finds more than an explanation should say. See the [authoring guide](authoring.md#2-probe-the-model).

## `render` options

| Option | Default | Meaning |
|---|---|---|
| `--draft` | off | 480p15 and silent narration with estimated timing. Writes `draft*` files. |
| `-q {l,m,h,k}` | `h` (`l` with `--draft`) | 480p15, 720p30, 1080p60, 2160p60 |
| `--scene NAME` | all | Render one scene class only. |
| `--review` | off | Also build the review sheet. |
| `--every N` | `4` | Seconds between contact-sheet frames. |

`render` prints any layout issue the scene found (text that overlaps text, text covered by another group's opaque panel, text outside the frame) and any narration line spoken twice.

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
