# Roadmap

Proposed improvements, in priority order. Each item names the problem it solves and how to tell that it is done.

Status: `proposed` · `next` · `in progress` · `done`

| # | Item | Status |
|---|---|---|
| 1 | [Enforce model consistency](#1-enforce-model-consistency) | next |
| 2 | [Automate review and the understanding test](#2-automate-review-and-the-understanding-test) | next |
| 3 | [Ship as a Claude Code plugin, with CI](#3-ship-as-a-claude-code-plugin-with-ci) | proposed |
| 4 | [Deepen the video toolkit](#4-deepen-the-video-toolkit) | proposed |
| 5 | [Add a Stage 3 toolkit](#5-add-a-stage-3-toolkit) | proposed |
| 6 | [Broaden the gallery](#6-broaden-the-gallery) | proposed |

Items 1 and 2 go first. They test the central claim of the project, and they make every later example cheaper to build and verify.

---

## 1. Enforce model consistency

**Problem.** The project claims that every rendering agrees with `model.md`. Today that is a convention only. In `softmax-temperature`, the numbers were copied by hand into the prose, the diagrams, the HTML, and the scene.

**Proposal.**

- Add a machine-readable part to the model: `model.yaml` (or front matter in `model.md`) with entities, quantities, and worked values.
- Make `scene.py` and `index.html` read values from the model instead of restating them.
- Add `explainer check <slug>`: report each term or number in a rendering that the model does not contain.

**Done when.** `explainer check softmax-temperature` passes, and a changed logit in the model makes the check fail until each rendering is updated.

## 2. Automate review and the understanding test

**Problem.** Review is manual. For each video, frames at bookmark times were extracted and read by hand, captions were read, and pages were screenshotted at two widths. The seven-question understanding test is graded by the same agent that made the rendering.

**Proposal.**

- `explainer review <slug>`: one sheet with a frame at each bookmark, the narration line under each frame, and flags for overlapping text.
- Blind understanding test: give a fresh subagent only the rendering. Ask the seven questions and one prediction (for example, "what happens at T = 3?"). Score the answers against `model.md`.

**Done when.** Both checks run on every example, and the blind test catches a deliberately broken rendering.

## 3. Ship as a Claude Code plugin, with CI

**Problem.** To use the workflow, people must clone this repository. This limits reach.

**Proposal.**

- Package `/explain`, `/video`, the playbooks, and `explainer_kit` as an installable Claude Code plugin.
- Add CI: unit tests for bookmark segmentation, caption chunking, and word diffs; link checks; Mermaid validation; a draft render of one example.

**Done when.** A user installs the plugin in an unrelated project and makes a draft video with `/video`.

## 4. Deepen the video toolkit

**Problem.** Equations are the signature of 3b1b-style video, but LaTeX is not installed, so `MathTex` is not available. Common patterns from the softmax scene (bars driven by a tracker, live numbers, staggered labels) are written inline in that scene, not in the toolkit.

**Proposal.**

- LaTeX support. Install with `brew install --cask basictex` (the user runs this; it asks for a password).
- Reusable components in `explainer_kit`: tracker-driven bar chart, live number, labeled number line, camera moves.
- Word-level timing from the PyTorch Kokoro build: word-by-word captions and highlighting of words as they are spoken.

**Done when.** The softmax scene uses the shared components and gets shorter, and one example uses `MathTex`.

## 5. Add a Stage 3 toolkit

**Problem.** Stage 4 has `explainer_kit`. Stage 3 pages are written from zero. The slider bug in the softmax page (presets rounded to the slider step, so T = 0.5 showed 0.841) came from hand-written code.

**Proposal.** A shared HTML template: theme tokens for light and dark, a slider with exact presets, tracker-driven charts, epistemic tags, and a progressive-disclosure section pattern.

**Done when.** A new interactive page starts from the template and passes the phone-width and dark-mode checks with no fixes.

## 6. Broaden the gallery

**Problem.** The current examples cover machine learning, git, and writing. They do not show an algorithm that runs, a system with drill-down levels, or mathematics.

**Proposal.**

- An algorithm that runs: Dijkstra's shortest path (Stage 4).
- A drill-down system: a request through a CDN (Stage 3, four levels).
- A short proof, after LaTeX support (Stage 4).

**Done when.** The gallery has at least one example for each of these kinds.

---

## Pending suggestions

More suggestions from the maintainer will be added here.
