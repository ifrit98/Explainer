# CLI reference

Run every command through `uv run` from the repo root.

| Command | Does |
|---|---|
| `explainer setup` | Download the Kokoro model files into `models/` and report which tools are installed. |
| `explainer new <slug>` | Create `explainers/<slug>/model.md`, `video/storyboard.md`, and a working `video/scene.py`. Existing files are kept. |
| `explainer voices [--all]` | List Kokoro voices. English voices by default; `--all` adds other languages. |
| `explainer say "<text>" [--voice V] [--speed S] [--out F] [--no-play]` | Synthesize one line and play it. Use it to choose a voice or test a lexicon spelling. |
| `explainer render <slug> [options]` | Render, join, master, caption, and write the contact sheet. |
| `explainer frames <slug> [--draft] [--every N]` | Rebuild the contact sheet from an existing render. |

## `render` options

| Option | Default | Meaning |
|---|---|---|
| `--draft` | off | 480p15, silent narration with estimated timing. Writes `draft.mp4` and `draft-contact.png`. |
| `-q {l,m,h,k}` | `h` (`l` with `--draft`) | 480p15, 720p30, 1080p60, 2160p60 |
| `--scene NAME` | all | Render one scene class only. |
| `--every N` | `4` | Seconds between contact-sheet frames. |

## Output

```text
explainers/<slug>/video/
  out.mp4         final video, captions as a soft track
  captions.srt    sidecar captions
  contact.png     review frames with timestamps
  draft.mp4       --draft output
  media/          Manim cache, scene renders, voice clips (git-ignored)
```

## Voices

The best English voices are `af_heart`, `af_bella`, `am_michael`, `am_fenrir`, and `bm_george`. Prefix: `a` = American, `b` = British; `f` = female, `m` = male.

```bash
uv run explainer say "Fill the hydraulic reservoir before you start the machine." --voice am_michael
```
