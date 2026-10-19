# Explainer — instructions for coding agents

This file is for agents other than Claude Code. Claude Code reads `CLAUDE.md`, which loads the same principles through an import that other agents do not follow.

In this folder, act as an explanation compiler. Before you write any explanation, also a short answer, read `plugin/skills/explain/references/principles.md` and follow it.

For a non-trivial explanation, follow the `explain` skill (`plugin/skills/explain/SKILL.md`). Use `plugin/skills/video/SKILL.md` to go straight to an animated explainer, and `plugin/skills/verify/SKILL.md` to check an existing explainer. Their reference files are in `plugin/skills/explain/references/`.

## This repo

The repo is three things: the toolkit (`explainer_kit/`), the Claude Code plugin (`plugin/`, listed by `.claude-plugin/marketplace.json`), and the examples (`explainers/`). Human-facing docs live in `docs/`. When you change the toolkit or the workflow, update the matching doc page and `ROADMAP.md`.

Run the CLI through uv: `uv run explainer <command>`.

```bash
uv run explainer new <slug> --stage 1 2 3 4   # scaffold model.md, model.yaml, narrative.md, and the chosen renderings
uv run explainer check                        # every example against its model.yaml
uv run explainer coldread <slug> --run        # first-viewing read by a fresh agent
uv run explainer findings --stats             # how many review findings authors adopt, per tool
uv run explainer eval chat                    # chat answers under each system prompt, graded blind
uv run explainer eval artifact --split dev    # held-out subjects built under each condition, read and graded blind
uv run explainer render <slug> --draft        # fast silent layout pass
uv run pytest -q                              # toolkit tests
```

The review and eval commands (`coldread`, `blindtest`, and `probe` with `--run`, and `eval`) call the Claude CLI (`claude -p`). They need it installed and signed in, whichever agent runs them.

Reference implementations by stage are indexed in `explainers/README.md`.

## Rules

- This repo is public. Never copy material from private projects that use the toolkit (course content, learner records) into it.
- The examples in `explainers/` are frozen as reference implementations and regression fixtures: `explainer check` must pass on them.
