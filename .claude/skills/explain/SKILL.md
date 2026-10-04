---
name: explain
description: Explanation-compiler pipeline. Use when the user asks to explain, teach, visualize, or break down a subject, concept, system, algorithm, or architecture — or invokes /explain <topic>. Builds a semantic model first, then renders it as controlled prose, a diagram, an interactive HTML explainer, or an animated video, escalating only when the richer medium improves understanding.
---

# Explain — explanation compiler pipeline

The governing rules are in the project `CLAUDE.md`. This skill is the procedure.

## Step 1 — Build the semantic model

1. Write the central question in one sentence.
2. Scaffold with `uv run explainer new <slug> --stage <stages>`. Fill in `model.md` (prose) and `model.yaml` (values, allowances, required values, quiz).
3. Reduce the model. Remove each entity that the explanation does not need to answer the central question.
4. Mark the epistemic status of each non-trivial claim.

For a Stage 1 answer in chat, do this step internally. For Stage 2–4, save the model to `explainers/<slug>/model.md`. Use a short kebab-case slug.

## Step 2 — Select the stage

Use the routing table and decision tests in `CLAUDE.md` §3. Tell the user the stage and the reason in one line. Example:

> Stage 3 (interactive HTML): the behavior depends on two parameters that interact, and a static diagram can show only one case.

If the stage is unclear between two options, choose the lower stage and offer the higher one.

## Step 3 — Render from the model

Load the playbook for the selected medium. Render only what is in the model.

| Stage | Playbook | Also load |
|---|---|---|
| 1 Prose | `references/writing.md` | — |
| 2 Diagram | `references/diagrams.md` + `references/writing.md` | `artifact-diagramming` skill if the diagram is an SVG/HTML page |
| 3 Interactive HTML | `references/html.md` + `references/diagrams.md` | `artifact-design` skill before you write the page |
| 4 Animation | `references/video.md` + `references/diagrams.md` | follow the `video` skill procedure (`uv run explainer …`) |

Use the exact entity names from the model in every label, caption, heading, and narration line.

## Step 4 — Apply progressive disclosure

Organize anything above Stage 1 into levels:

- **Level 1** — What is it?
- **Level 2** — How does it work?
- **Level 3** — Why does it work?
- **Level 4** — How is it implemented? (optional)

Show Level 1 first. Reveal deeper levels on demand (click, expand, scene progression) when the medium allows it.

## Step 5 — Verify

Run the seven questions in `CLAUDE.md` §7 against the rendered result, not against your intent. For HTML, open the page in a browser (Playwright) and check it at desktop and phone width. For video, read `contact.png` and `captions.srt`, and check frames at bookmark times.

Also check model consistency: every label in the rendering must exist in `model.md`, and no rendering may contradict another.

If a check fails, revise. If a revision cannot fix it, escalate one stage.

## Step 6 — Deliver

- Stage 1: the answer in chat.
- Stage 2: the diagram inline (Mermaid or ASCII) in chat, or an SVG/HTML page for complex diagrams.
- Stage 3: publish `index.html` with the Artifact tool and give the link. Keep the local file.
- Stage 4: give the path to `explainers/<slug>/video/out.mp4` and `captions.srt`.

End with a two-line summary: the stage chosen, and what the reader can now do or predict.
