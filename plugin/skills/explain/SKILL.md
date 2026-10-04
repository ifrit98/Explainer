---
name: explain
description: Explanation-compiler pipeline. Use when the user asks to explain, teach, visualize, or break down a subject, concept, system, algorithm, or architecture — or invokes /explain <topic>. Builds a semantic model first, then renders it as controlled prose, a diagram, an interactive HTML explainer, or an animated video, escalating only when the richer medium improves understanding, and checks every rendering against the model.
---

# Explain — explanation compiler pipeline

Read `references/principles.md` first. It holds the rules that apply to every explanation: model first, the four stages, STE-80 writing, epistemic labels, predict-first, and the understanding test. This skill is the procedure.

**CLI.** With the plugin installed, run `explainer <command>`. Inside the Explainer repo, run `uv run explainer <command>`. The first plugin run downloads the toolkit with uv. Video needs `explainer setup` once (Kokoro voice, about 350 MB).

## Step 0 — Choose the tier

Match the process to the stakes (principles §12). Choose the lowest tier that fits, and say which one in a word when you start.

| Tier | When | Steps |
|---|---|---|
| **Answer** | A question in chat. The default. | Build the model in your head (Step 1, no files), choose the stage, answer in STE-80. A Mermaid block or a table inline is fine. |
| **Quick artifact** | A diagram, page, or video for this person, now. | `explainer new <slug> --stage <n> --quick`; Step 1 items 1–4 and 9; Step 2; Step 3; `explainer check <slug>`. |
| **Published** | An example in a repo, course material, anything many people will read. | Every step below: probe, narrative, cold read, blind test. |

Every tier: a named reader (default: a technical reader new to this subject), the answer first, a why for each operation the reader does not already trust, and nothing this reader already knows.

## Step 1 — Build the semantic model

1. Write the central question in one sentence, and the audience: who reads this and what they already know.
2. Choose the stage (Step 2), then scaffold: `explainer new <slug> --stage <stages>`. This creates `explainers/<slug>/model.md`, `model.yaml`, `narrative.md` (not with `--quick`), and the chosen renderings from templates.
3. Fill `model.md`: entities, relationships, causal chain, quantities, alternative states, epistemic status, confusion points, representation decision.
4. Fill `model.yaml`: every number a rendering will show goes in `values`. Add `require` for values each rendering must show. Published tier: 2–3 `quiz` items (question, expected answer, likely misconception) for the blind test.
5. Fill the completeness sections of `model.md` (`references/completeness.md`): **Why this form**, **Concrete cases**, **Terms**, **Scope**. One case per idea is enough.
6. **Probe.** Run `explainer probe <slug>` and give the prompt, unchanged, to a fresh subagent. Recompute every number it suggests. Turn each finding into a claim, a Scope entry, or nothing: a question this audience would not ask is nothing.
7. Record the ideas as `claims` in `model.yaml` (`why`, `guarantee`, `mechanism`, `definition`, …) with their required fields. Add `ask` to the claims a learner most needs; they become blind-test questions.
8. Give each concept one word. Where two concepts are close (a tentative value and its final value), add a `terms` entry with the phrases renderings must not use. Give every quantity a reader will see its meaning, with a low and a high value.
9. Reduce the model. Remove each entity that the explanation does not need. Set the length: the defaults are 600 words of prose and 150 s of video. If the subject needs more, set `budget` in `model.yaml` with the reason.

## Step 1b — Compile the narrative (published tier)

Fill `narrative.md` (`references/narrative.md`) before any rendering:

1. **Before and after:** the reader (from the model's audience) and the one sentence they can say afterwards.
2. **Question and motive:** the question and the result in words; why care; why this approach.
3. **Introduction ledger:** every term, symbol, name, and visual convention that is new to this reader, with the instance that grounds it and the beat that introduces it.
4. **Beats:** in order, each with the reader's question, the bridge (so, but, therefore), what is shown, what is said, and what the reader now knows.
5. **Cold read:** run `explainer coldread <slug> --rendering narrative` and give the prompt, unchanged, to a fresh subagent. Fix every blocking finding. Cut what it marks as excess. Fix an edge finding when the fix is short. A finding can change the argument itself; change the model too when it does.

## Step 2 — Select the stage

Use the routing table and decision tests in `references/principles.md` §3. Tell the user the stage and the reason in one line. Example:

> Stage 3 (interactive): the behavior depends on two parameters that interact, and a static diagram can show only one case.

If two stages fit, choose the lower stage and offer the higher one.

## Step 3 — Render from the model

Load the playbook for the medium. Render only what is in the model.

| Stage | Playbook | Notes |
|---|---|---|
| 1 Prose | `references/writing.md` | `explanation.md` |
| 2 Diagram | `references/diagrams.md` + `references/writing.md` | `diagram.md` with Mermaid; load `artifact-diagramming` for SVG pages |
| 3 Interactive | `references/html.md` + `references/diagrams.md` | `index.html` from the template, on the web toolkit; load `artifact-design` |
| 4 Animation | `references/video.md` + `references/diagrams.md` | follow the `video` skill |

Follow the beats of `narrative.md` in order, when there is one. Use the exact entity names from the model in every label, caption, heading, and narration line. Present each claim with its case (the alternative failing, the counterexample, the worked numbers), and mark it: `<!-- claim: id -->`, `data-claim="id"`, or `self.claim("id")`. Scenes read values with `load_model(__file__)`. Pages read `Explainer.model`, filled by `explainer sync <slug>`.

## Step 4 — Progressive disclosure and predict-first

Organize anything above Stage 1 into levels: L1 what it is, L2 how it works, L3 why it works, L4 how it is implemented. Show L1 first; reveal deeper levels on demand.

When the reader is learning, put a prediction before each important result (principles §8).

## Step 5 — Verify

Quick artifact: `explainer check <slug>`, plus the review sheet for video and a browser check for pages. Published: the whole `verify` skill, including the cold read and the blind understanding test.

## Step 6 — Deliver

- Stage 1: the answer in chat, or `explanation.md`.
- Stage 2: Mermaid inline in chat, or `diagram.md`.
- Stage 3: `index.html`. Publish it with the Artifact tool when the user wants a link, or serve it from the repo (GitHub Pages).
- Stage 4: `explainers/<slug>/video/out.mp4` with `captions.srt`.

End with two lines: the stage chosen, and what the reader can now do or predict.
