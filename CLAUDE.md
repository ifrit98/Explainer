# Explainer — operating instructions

In this folder, act as an explanation compiler. These principles always apply, also to short answers:

@plugin/skills/explain/references/principles.md

For a non-trivial explanation, use the `explain` skill. Use `video` to go straight to an animated explainer, and `verify` to check an existing explainer. The skills live in `plugin/skills/`; `.claude/skills/` links to them, so the repo and the published plugin use the same files.

## This repo

The repo is three things: the toolkit (`explainer_kit/`), the Claude Code plugin (`plugin/`, listed by `.claude-plugin/marketplace.json`), and the examples (`explainers/`). Human-facing docs live in `docs/`. When you change the toolkit or the workflow, update the matching doc page and `ROADMAP.md`.

Run the CLI through uv here: `uv run explainer <command>`. Plugin users run `explainer <command>` (the plugin's `bin/explainer` wrapper).

```bash
uv run explainer new <slug> --stage 1 2 3 4   # scaffold model.md, model.yaml, narrative.md, and the chosen renderings (--quick: no narrative.md)
uv run explainer check                        # every example against its model.yaml
uv run explainer coldread <slug> --run        # first-viewing read by a fresh agent (claude -p), saved with numbered findings
uv run explainer findings --stats             # how many review findings authors adopt, per tool
uv run explainer eval chat                    # chat answers under each system prompt, graded blind (needs the claude CLI)
uv run explainer render <slug> --draft        # fast silent layout pass
uv run explainer render <slug> --review       # 1080p60, voice, captions, chapters, review sheet
uv run pytest -q                              # toolkit tests
```

Reference implementations by stage are indexed in `explainers/README.md`.

## Folder layout

```text
explainer_kit/      toolkit: CLI, model check, scene base, components, voice, web toolkit, templates
plugin/             Claude Code plugin: skills (explain, video, verify) and bin/explainer
explainers/<slug>/  model.md, model.yaml, renderings (explanation.md, diagram.md, index.html, video/)
docs/               documentation for people
tests/              pytest suite
models/             Kokoro model files (git-ignored; `uv run explainer setup` downloads them)
```

## Local toolchain (checked 2026-10-04)

- Python env: `uv` project, Python 3.12 (`.python-version`).
- Available: Manim CE 0.21, manim-voiceover 0.4, kokoro-onnx, `ffmpeg`, `sox`, Cairo/Pango, `node`, LaTeX via user-level TinyTeX (`~/Library/TinyTeX`, found automatically; not on PATH).
- Not installed: `mmdc` (Mermaid CLI), `dot` (Graphviz). Use `npx` / `uvx` for them, or ask before you install them.
- This repo is public. Never copy material from private projects that use the toolkit (course content, learner records) into it.
