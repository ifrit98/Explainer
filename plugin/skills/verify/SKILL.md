---
name: verify
description: Check an explainer before it ships — renderings against model.yaml, the video review sheet, the page in a browser, and a blind understanding test run by a fresh agent. Use after building an explainer, before publishing one, or when the user asks to check, review, or test an explainer (/verify <slug>).
---

# Verify — is the explanation right, and does it teach?

Run the checks in order. Stop and fix at the first failure. A quick artifact needs §1 and §2 only; a published one needs all of them (principles §12). Record what you ran in `explainers/<slug>/review/understanding.md`.

**CLI.** `explainer <command>` with the plugin; `uv run explainer <command>` inside the Explainer repo.

## 1. Consistency with the model

```bash
explainer check <slug>
```

It fails when a rendering shows a number the model does not explain, is longer than its declared `budget`, omits a value that `require` lists, embeds an out-of-date model (`explainer sync <slug>` fixes that), leaves a claim incomplete or uncovered, uses a phrase a `terms` entry avoids, or plays the video without its predict pauses, or when `model.md` uses a function that no `why` claim justifies. A number that is right but missing from the model goes into `values` or `allow`. Never silence a real disagreement. A `!` line is a warning: a rendering over the default length (600 words of prose, 150 s of video). Cut it, or set `budget` with a reason.

Add `--diagrams` when the explainer has Mermaid blocks: each block is rendered once with the Mermaid CLI (`mmdc`, or `npx` with Node).

## 2. Each medium

- **Video.** `explainer review <slug>`, then read `video/review.png`: a frame at each line, bookmark, and predict pause, with the spoken text under it. Every layout and pace issue it lists must be fixed. Check that each frame shows the evidence for its line.
- **Page.** Open `index.html` in a browser (Playwright when available). Use every control once. Check: no console errors, no horizontal scroll at 390 px, both light and dark themes, the predict gate hides its result until a prediction is committed.
- **Prose and diagrams.** Read them against the STE-80 rules in `../explain/references/writing.md`. `explainer check --diagrams` renders each Mermaid block.

## 3. Cold read (first viewing, in order)

The blind test asks what a reader understood at the end. The cold read finds where, in order, the reader paid effort: for something missing (a reference not given, a step without its reason) or for something extra (what they already know, a repeat, a detour). A rendering can pass the blind test and fail the cold read: the reviewer fills gaps from context.

1. Print the prompt: `explainer coldread <slug> --rendering <narrative|prose|diagram|html|video>`. It plays the audience from `narrative.md` or `model.md`; set that audience first.
2. Give it, unchanged, to a fresh subagent.
3. Apply the pass rule (`explainer coldread <slug> --rubric`): no blocking finding; the question known early and the result stated in words; a motive and a reason for the approach; a close that answers the opening question.
4. Fix every blocking finding. Cut each excess finding unless it carries a step of the argument. Fix an edge finding only when the fix is short. Prefer fixes that replace words to fixes that add them. Fix in `narrative.md` first, then in the renderings.
5. Stop when nothing blocks. Record the findings and what you did not apply in `review/understanding.md`.

## 4. Blind understanding test

Use this for anything that will be published. A fresh agent sees only one rendering.

1. Print the prompt: `explainer quiz <slug> --rendering <prose|diagram|html|video>`. For video, run `explainer review <slug>` first: the reviewer reads the captions and the review sheet.
2. Start a fresh subagent with the prompt text exactly as printed (the Agent tool, general-purpose). Do not add context. It must not read `model.md` or `model.yaml`.
3. Score its answers with `explainer quiz <slug> --rubric`: each general item 0–2, each quiz item 0–2. Count an answer that states a listed misconception as 0.
4. Pass: every quiz item scores 2 and no general item scores 0.
5. Write the scores, the reviewer's "audit" (terms with two names, numbers without a meaning, steps without a why, and for video, rushed points) and its "gaps" to `review/understanding.md`. Fix real gaps in the rendering, then run the test again on the changed rendering.
6. For each real gap, ask which check, probe rule, or template line would have caught it in any explanation, and add it (principles §10). Record it in `ROADMAP.md`.

A blind test that a deliberately broken copy also passes proves nothing. When you change the quiz, run it once on a broken copy (one key claim reversed) to confirm that the test can fail.
