# Roadmap

Each item names the problem it solves and how to tell that it is done.

Status: `proposed` · `next` · `in progress` · `done`

| # | Item | Status |
|---|---|---|
| 1 | [Enforce model consistency](#1-enforce-model-consistency) | done (v0.2.0) |
| 2 | [Automate review and the understanding test](#2-automate-review-and-the-understanding-test) | done (v0.2.0) |
| 3 | [Ship as a Claude Code plugin, with CI](#3-ship-as-a-claude-code-plugin-with-ci) | done (v0.2.0) |
| 4 | [Deepen the video toolkit](#4-deepen-the-video-toolkit) | done, except word-level timing |
| 5 | [Add a Stage 3 toolkit](#5-add-a-stage-3-toolkit) | done (v0.2.0) |
| 6 | [Broaden the gallery](#6-broaden-the-gallery) | done (v0.2.0) |
| 7 | [Predict-first renderings](#7-predict-first-renderings) | done (v0.2.0) |
| 8 | [A first real user outside this repo](#8-a-first-real-user-outside-this-repo) | done (v0.2.0) |
| 9 | [Open items from reviews](#9-open-items-from-reviews) | partly done (v0.3.0) |
| 10 | [Complete the chain: claims and the probe](#10-complete-the-chain-claims-and-the-probe) | done (v0.3.0) |

---

## 1. Enforce model consistency

**Problem.** The numbers in `softmax-temperature` were copied by hand into four renderings.

**Built.** `model.yaml` (values, allow, require, quiz). `explainer check` reads each rendering as a reader meets it and fails on a number the model does not explain, a required value that is missing, or a stale page. Scenes use `load_model(__file__)`; pages get the model through `explainer sync`.

**Done when** — met. Changing one logit in the model fails the prose and the diagram and flags the page as stale (`tests/test_model.py`). Building the check also exposed bugs in the check itself (fence parsing, integers standing in for fractions), each now covered by a test.

## 2. Automate review and the understanding test

**Built.** Scenes log a timeline and check visible text at every bookmark and line end (overlap, covered by an opaque panel, off-frame). `explainer review` makes a sheet with one frame per line, bookmark, and predict pause. `explainer quiz` prints a blind-test prompt and a rubric; the `verify` skill runs it with a fresh subagent.

**Done when** — met. The blind test passed the published softmax prose and failed a deliberately broken copy (0 on the misconception item). The layout check caught a real off-frame equation in `odd-squares` and a covered label in `softmax-temperature`.

## 3. Ship as a Claude Code plugin, with CI

**Built.** `plugin/` holds the skills (`explain`, `video`, `verify`) and `bin/explainer`, which runs the pinned toolkit release with uv. The repo root is the marketplace. `.claude/skills/` links to the plugin's skills, so the repo and the plugin share one copy. CI runs the tests (toolkit, links, plugin manifest, every example against its model), `explainer check`, and a draft render.

**Done when** — met for the CLI: the wrapper scaffolded, synced, and checked an explainer in an unrelated project. Install with `/plugin marketplace add ifrit98/Explainer`.

## 4. Deepen the video toolkit

**Built.** LaTeX through a user-level TinyTeX that the toolkit finds without a PATH change. `explainer_kit.components`: `TrackerBars`, `LiveNumber`, `LabeledNumberLine`, `stagger_labels`. The softmax scene uses them and is shorter. Captions start at each sentence's real audio time. Scenes fail fast instead of hanging after an animation error.

**Deferred: word-level timing.** The ONNX Kokoro model returns audio only, without phoneme durations. Word timing needs the PyTorch Kokoro build (a large dependency) or a forced aligner. Sentence and bookmark timing are exact.

## 5. Add a Stage 3 toolkit

**Built.** `explainer_kit/web/`: CSS with light and dark tokens, and JS for a shared tracker, a slider with exact presets, identity-preserving bars, a predict gate, a video player with predict pauses, progressive-disclosure levels, and epistemic tags. `explainer new --stage 3` starts from a working template.

**Done when** — met. `cdn-request` was built from the template and passed the phone-width and dark-mode checks; its only fix was a page-specific diagram size.

## 6. Broaden the gallery

**Built.** `odd-squares` (a proof, with LaTeX and a predict pause), `dijkstra` (an algorithm replayed from the model's run), `cdn-request` (a drill-down page with four levels).

## 7. Predict-first renderings

**Problem.** A learner who only watches a result learns less than one who predicts it first.

**Built.** `Explainer.predict` gates (pages), `self.predict` pauses (videos, with MP4 chapters), and `Explainer.video`, which stops at each pause and asks for a prediction. Principle 8 makes it the default for learners.

## 8. A first real user outside this repo

**Built.** A private curriculum project used the plugin wrapper, with no setup in that project, to build a predict-first companion page for one lesson. It surfaced three fixes: slow and noisy imports for non-video commands (now lazy), SVG text sizing in letterboxed diagrams, and the rule that curriculum renderings use worked examples, never the learner's own problem.

## 9. Open items from reviews

Done in v0.3.0:

- `softmax-temperature`: why softmax uses exp, in every rendering. The page lets the reader try divide-by-sum and squares; the video shows owl at −0.4. The blind re-test now answers "why exp" in full.
- `dijkstra`: finality shown with this run's numbers at the moment B settles; a negative-edge chapter; "relax" defined; why the smallest estimate settles first; the path read back through predecessors. Blind re-test: pass on all five quiz items.

Still open:

- `dijkstra`: use one word ("estimate") for one concept; the narration also says "distance". Slow down the finality segment (about ten seconds).
- `softmax-temperature`: a sentence of intuition for entropy beyond "2.76 equally likely choices".
- Validate Mermaid blocks in CI (today they are checked by hand in a browser).
- Landing page: play the videos with the predict-pause player.

## 10. Complete the chain: claims and the probe

**Problem.** An explanation can pass every number check and still omit the idea that makes it click. The first softmax prose never said why it uses exp; the first Dijkstra video stated a guarantee without showing it hold or fail. The blind test only noticed these as side notes, after rendering.

**Built.**

- **Claims** in `model.yaml`, with required fields per kind: a `why` needs the simplest alternative and its failure; a `guarantee` needs an example and a counterexample; a `mechanism` needs a worked example. Renderings mark where they cover each claim; `explainer check` fails on an incomplete or uncovered claim.
- **The function rule:** a function in `model.md` (exp, log, sqrt, …) with no `why` claim fails the check. This rule alone would have caught "why exp".
- **`explainer probe`:** a fresh agent reads only `model.md` and lists omissions, before anything is rendered. On the old softmax model its first finding was "why exp", with the divide-by-sum counterexample; on the old Dijkstra model it proposed the same negative-edge graph used in the video. Its numbers are suggestions: in one run it gave two different values for one probability, so every number is recomputed.
- **Model template** sections Why this form, Concrete cases, Terms, Scope; principle 10.

**Done when** — met. The updated softmax prose and Dijkstra video pass blind re-tests that include the claim questions; the reviewers now answer "why exp" and "why is a settled distance final" with the counterexamples.
