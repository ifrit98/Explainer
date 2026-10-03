# Explainer

A Claude Code workspace that acts as an **explanation compiler**: build one semantic model of a subject, then render it in the simplest medium that preserves its structure.

```text
                  ┌─ controlled prose
Question → Model ─┼─ diagram
                  ├─ interactive HTML
                  └─ animated explainer
```

## Contents

| Path | Purpose |
|---|---|
| `CLAUDE.md` | Always-on rules: model first, escalation protocol, STE-80 writing, epistemic clarity, understanding test |
| `.claude/skills/explain/SKILL.md` | The six-step pipeline (`/explain <topic>`) |
| `.claude/skills/explain/templates/model.md` | Semantic model template — the source of truth for every rendering |
| `.claude/skills/explain/references/` | Playbooks: `writing.md`, `diagrams.md`, `html.md`, `video.md` |
| `.claude/skills/video/SKILL.md` | `/video <topic>`: go straight to a 3b1b-style animated explainer |
| `explainer_kit/` | Manim + Kokoro toolkit: `ExplainerScene`, semantic colors, word morphs, `explainer` CLI |
| `explainers/<slug>/` | Output: `model.md`, `index.html`, `video/` |

## Usage

Open Claude Code in this folder and run `/explain <topic>`, or ask for an explanation. Claude builds the model, states which stage it chose and why, renders, and checks the result against the understanding test.

## 3b1b-style video with voiceover

Manim Community for animation, [manim-voiceover](https://github.com/ManimCommunity/manim-voiceover) for sync, and [Kokoro-82M](https://github.com/thewh1teagle/kokoro-onnx) for a local voice. No API keys.

```bash
brew install cairo pango pkgconf ffmpeg sox   # macOS system libraries
uv sync                                       # Python env (3.12)
uv run explainer setup                        # download Kokoro model (~350 MB) and check tools

uv run explainer new my-topic                 # scaffold model.md, storyboard.md, scene.py
uv run explainer render my-topic --draft      # fast silent layout pass
uv run explainer render my-topic              # 1080p60, voice, -16 LUFS, captions, contact sheet
```

Bookmarks in the narration (`<bookmark mark='x'/>`) get exact times without Whisper: the Kokoro service synthesizes each segment separately and records where it starts.

Example: [`explainers/ste-80/video/out.mp4`](explainers/ste-80/video/out.mp4). It shows one manual sentence going through three STE rules, 16 → 9 words, narrated in STE-80.

`MathTex` needs LaTeX (`brew install --cask basictex`).

## Escalation stages

1. **Controlled prose** — sequential, definitional, procedural material.
2. **Static diagram** — topology, flow, architecture, causality.
3. **Interactive HTML** — parameters, scenarios, drill-down, simulation.
4. **Animated explainer** — transformation, propagation, state A → state B.

Escalate only when the richer medium reduces the reader's mental work.
