# Getting started

Explainer is a [Claude Code](https://claude.com/claude-code) workspace. You open it, ask for an explanation, and the agent builds the representation that fits the subject: controlled prose, a diagram, an interactive page, or a narrated animation.

## 1. Requirements

| Need | Why | Install (macOS) |
|---|---|---|
| Claude Code | runs the workflow | [claude.com/claude-code](https://claude.com/claude-code) |
| `uv` | Python environment (3.12) | `brew install uv` |
| Cairo, Pango, pkg-config | Manim text and vector rendering | `brew install cairo pango pkgconf` |
| FFmpeg | video encoding, captions, contact sheets | `brew install ffmpeg` |
| SoX | optional; silences a manim-voiceover warning, needed for `global_speed` | `brew install sox` |
| LaTeX | optional; only for `MathTex`, `Tex`, `DecimalNumber` | `brew install --cask basictex` |

On Linux, install the same libraries with your package manager (`libcairo2-dev libpango1.0-dev pkg-config ffmpeg sox`). Manim's [installation guide](https://docs.manim.community/en/stable/installation.html) lists the details per platform.

Stages 1–3 (prose, diagrams, HTML) need only Claude Code. The Python setup is for Stage 4 video.

## 2. Install

```bash
git clone https://github.com/ifrit98/Explainer.git
cd Explainer
uv sync                    # creates .venv with Manim, manim-voiceover, kokoro-onnx
uv run explainer setup     # downloads the Kokoro voice model (~350 MB) into models/
```

`setup` also prints which optional tools are present.

## 3. Ask for an explanation

Start Claude Code in the folder:

```bash
claude
```

Then ask in plain words, or use a skill:

```text
/explain how does a bloom filter work
/video why the derivative of sin is cos
```

`/explain` runs the full pipeline. It builds a semantic model, chooses the stage, states the reason in one line, renders, and checks the result against the understanding test. `/video` fixes the stage at 4.

Output goes to `explainers/<slug>/`.

## 4. Make a video by hand

You can use the toolkit without the agent.

```bash
uv run explainer new my-topic             # scaffold model.md, storyboard.md, scene.py
$EDITOR explainers/my-topic/video/scene.py
uv run explainer render my-topic --draft  # 480p, silent narration with estimated timing: check layout
uv run explainer render my-topic          # 1080p60, Kokoro voice, mastered audio, captions
open explainers/my-topic/video/out.mp4
```

The scaffold is a working scene. Read [`video-pipeline.md`](video-pipeline.md) for the API, and [`explainers/softmax-temperature/video/scene.py`](../explainers/softmax-temperature/video/scene.py) for a complete example.

## 5. Next

- [Concepts](concepts.md): the explanation compiler, the four stages, and STE-80.
- [Video pipeline](video-pipeline.md): how narration and animation stay in sync.
- [CLI reference](cli.md)
- [Troubleshooting](troubleshooting.md)
