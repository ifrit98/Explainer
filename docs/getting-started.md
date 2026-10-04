# Getting started

Explainer is a Claude Code plugin plus a small toolkit. You ask for an explanation; the agent builds a semantic model, picks the simplest representation that keeps its structure (controlled prose, a diagram, an interactive page, or a narrated animation), renders it, and checks the rendering against the model.

## 1. Install the plugin

In Claude Code:

```text
/plugin marketplace add ifrit98/Explainer
/plugin install explainer@explainer
```

Restart the session. You now have three skills:

| Skill | Use it for |
|---|---|
| `/explainer:explain <topic>` | the full pipeline: model, stage choice, rendering, checks |
| `/explainer:video <topic>` | straight to a 3b1b-style video with voiceover |
| `/explainer:verify <slug>` | check an existing explainer, including a blind understanding test |

The plugin puts an `explainer` command on the agent's PATH. On first use it fetches the toolkit with [uv](https://docs.astral.sh/uv/) (install uv first: `brew install uv`).

Stages 1–3 (prose, diagrams, interactive pages) need nothing else.

## 2. Requirements for video

| Need | Why | Install (macOS) |
|---|---|---|
| Cairo, Pango, pkg-config | Manim text and vector rendering | `brew install cairo pango pkgconf` |
| FFmpeg | encoding, captions, chapters, review sheets | `brew install ffmpeg` |
| Kokoro voice model | local narration, no API key | `explainer setup` (about 350 MB, once) |
| LaTeX | optional: `MathTex`, `Tex` | TinyTeX, no password: see `explainer setup` |
| SoX | optional: silences a manim-voiceover warning | `brew install sox` |

On Linux, install `libcairo2-dev libpango1.0-dev pkg-config ffmpeg`. Manim's [installation guide](https://docs.manim.community/en/stable/installation.html) lists the details per platform.

## 3. Ask for an explanation

```text
/explainer:explain how does a bloom filter work
/explainer:video why the derivative of sin is cos
```

The agent drafts the model, has a fresh agent probe it for omissions, states the stage it chose and why, renders, and checks every rendering against the model. It writes `explainers/<slug>/` in your project:

```text
explainers/<slug>/
  model.md          the semantic model, in prose
  model.yaml        the values every rendering must agree with
  explanation.md    Stage 1
  diagram.md        Stage 2 (Mermaid; GitHub renders it)
  index.html        Stage 3 (one self-contained page)
  video/out.mp4     Stage 4
```

## 4. Work with the toolkit directly

```bash
explainer new my-topic --stage 3 4     # scaffold the model, a page, and a video scene
explainer probe my-topic               # a prompt for a fresh agent: what does the model omit?
explainer check my-topic               # renderings against model.yaml: numbers and claims
explainer sync my-topic                # inline the web toolkit and the model into the page
explainer render my-topic --draft      # 480p, silent narration: check the layout
explainer render my-topic --review     # 1080p60, Kokoro voice, captions, chapters, review sheet
```

The scaffolds are working files. Read [video-pipeline.md](video-pipeline.md) for the scene API and [concepts.md](concepts.md) for the model and the checks.

## 5. Develop Explainer itself

```bash
git clone https://github.com/ifrit98/Explainer.git && cd Explainer
uv sync && uv run explainer setup
uv run pytest -q                         # toolkit tests, links, plugin, every example against its model
claude                                   # the repo loads the same skills from plugin/skills/
```

To test the plugin wrapper against your checkout from another project, set `EXPLAINER_SOURCE=/path/to/Explainer`.

## Next

- [Concepts](concepts.md): the explanation compiler, the model and its checks, predict-first, STE-80.
- [Authoring guide](authoring.md): how to write an explanation that does not omit the important connections.
- [Model reference](model-reference.md) and [web toolkit](web-toolkit.md).
- [Video pipeline](video-pipeline.md): how narration and animation stay in sync.
- [CLI reference](cli.md)
- [Troubleshooting](troubleshooting.md)
