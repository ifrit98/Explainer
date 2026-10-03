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
| `explainers/<slug>/` | Output: `model.md`, `index.html`, `video/` |

## Usage

Open Claude Code in this folder and run `/explain <topic>`, or ask for an explanation. Claude builds the model, states which stage it chose and why, renders, and checks the result against the understanding test.

## Escalation stages

1. **Controlled prose** — sequential, definitional, procedural material.
2. **Static diagram** — topology, flow, architecture, causality.
3. **Interactive HTML** — parameters, scenarios, drill-down, simulation.
4. **Animated explainer** — transformation, propagation, state A → state B.

Escalate only when the richer medium reduces the reader's mental work.
