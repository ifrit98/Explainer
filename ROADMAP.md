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
| 9 | [Open items from reviews](#9-open-items-from-reviews) | done (v0.4.0) |
| 10 | [Complete the chain: claims and the probe](#10-complete-the-chain-claims-and-the-probe) | done (v0.3.0) |
| 11 | [Review findings become rules](#11-review-findings-become-rules) | done (v0.4.0) |
| 12 | [The narrative pass](#12-the-narrative-pass) | done (v0.5.0), with open items |

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

Done in v0.4.0, each one also turned into a general rule (item 11):

- `dijkstra`: one word per concept. "Estimate" is the value that can still drop; "distance" is only the final value. The finality argument is now three lines, one step per picture, with a pause after it (about 20 s instead of 12 s over one picture).
- `softmax-temperature`: entropy as average surprise. −log₂ p is the number of fair yes/no questions; the log makes surprises add; a count of possible tokens says 4 at T = 0.25, where cat wins 98% of draws, and entropy says 1.11 choices.
- Mermaid blocks render in CI (`explainer check --diagrams`).
- The landing page plays the videos with the predict-pause player.

## 10. Complete the chain: claims and the probe

**Problem.** An explanation can pass every number check and still omit the idea that makes it click. The first softmax prose never said why it uses exp; the first Dijkstra video stated a guarantee without showing it hold or fail. The blind test only noticed these as side notes, after rendering.

**Built.**

- **Claims** in `model.yaml`, with required fields per kind: a `why` needs the simplest alternative and its failure; a `guarantee` needs an example and a counterexample; a `mechanism` needs a worked example. Renderings mark where they cover each claim; `explainer check` fails on an incomplete or uncovered claim.
- **The function rule:** a function in `model.md` (exp, log, sqrt, …) with no `why` claim fails the check. This rule alone would have caught "why exp".
- **`explainer probe`:** a fresh agent reads only `model.md` and lists omissions, before anything is rendered. On the old softmax model its first finding was "why exp", with the divide-by-sum counterexample; on the old Dijkstra model it proposed the same negative-edge graph used in the video. Its numbers are suggestions: in one run it gave two different values for one probability, so every number is recomputed.
- **Model template** sections Why this form, Concrete cases, Terms, Scope; principle 10.

**Done when** — met. The updated softmax prose and Dijkstra video pass blind re-tests that include the claim questions; the reviewers now answer "why exp" and "why is a settled distance final" with the counterexamples.

## 11. Review findings become rules

**Problem.** Each blind test found gaps in one example. Fixing only that example leaves the same gap in the next explanation.

**Built.** For each finding, the rule that would have caught it anywhere:

| Finding | Rule |
|---|---|
| "distance" for a value that can still drop | `terms` in `model.yaml`, checked; probe rule 3; audit `terms` |
| "1.46 bits" with no meaning; `log` excused | probe rule 6 (meaning of each quantity); audit `unexplained`; `check -v` lists excused functions |
| a guarantee told in 12 s over one picture | pace issues from the timeline: a pause after each claim, one picture per step |
| a page that skipped the video's predict pauses | `check` fails a plain `<video>` when the timeline has predict pauses |
| Mermaid checked by hand | `check --diagrams`, in CI |

The `verify` skill now ends with the same question for every real gap: which check, probe rule, or template line would have caught it?

**Done when** — met. Each check fails on a small copy of its problem (`tests/test_discipline.py`). On the real examples, the terms check failed the old Dijkstra narration five times, and the pace check flagged the old finality line and five claims with no pause; all pass now. The blind re-tests of the changed renderings are in each example's `review/understanding.md`.

**Second round.** The blind re-tests passed (every quiz item 2/2), and their audit found three more gaps. Each was fixed and generalized:

| Finding | Fix | Rule |
|---|---|---|
| Softmax prose used "gap" for the logit gap and for the gap divided by T. | "scaled gap" for the second | a `terms` entry; it then found the same mix-up on the page, which the reviewer never saw |
| Dijkstra's finality argument drew B inside the "settled" box while arguing about paths that leave the box, named F as an exit, and skipped "reaching D costs at least its estimate". The model had the same flaw. | the box holds A and C; the exits are D and E; the step is said; B settles after the argument | probe rule 2 now checks each step of an argument as written |
| Review-sheet headings showed the frame time, 0.5–1 s after the event. | headings show the event time, which matches the captions | — |

Still open from the audit: the predict card covers the estimates a viewer needs to answer; colors are not explained; Bellman-Ford is named without a why (a scope pointer).

**Next candidates.**

- Pace thresholds are fixed numbers (1 s, 10 s). Calibrate them against more videos and viewer feedback.
- `terms` catches listed phrases only. A term drift no one listed still needs the audit to find it.

## 12. The narrative pass

**Problem.** A correct model with every claim covered can still lose the reader on the way. The odd-squares video passed its blind test while it used "the n-th L" without saying what n is, and never said its own result aloud. The model says what is true; nothing said how a first-time reader gets there. That path is what gives a 3Blue1Brown video its power, more than the animation.

**Built.**

- `narrative.md`, Pass 3 (principles §11): the reader before and after; the question and the result in words; a motive and a reason for the approach; an introduction ledger (every term, symbol, name, and visual convention, with the instance that grounds it); the beats in order, each with its bridge, what is shown, and what is said; concrete to symbol; links between representations; the close. `explainer new` scaffolds it.
- `explainer coldread <slug> --rendering R`: a fresh agent meets the narrative or a rendering for the first time and reports, in order, every reference it was not given, everything shown but unsaid, every leap, and whether the question, the motive, and the close are there. It runs on the narrative before rendering and on each rendering after.
- `explainer check` fails a scene symbol (on-screen math, a math label, "the n-th" in speech) that the ledger does not introduce.
- The layout check reports `crowded` text (closer than 0.1 units). It found two touching labels in the softmax video; `stagger_labels` now spaces rows by label height.

**Evidence so far.** On the old odd-squares video, the blind test passed and the cold read found the undefined n, the unnamed L, three meanings of "square", two unread formulas, and a result never said. The narrative's own cold read, before rendering, then changed the argument: n had three meanings, and one general step rested on examples. The new argument (each L is two bigger than the last) came from that read.

**Done when** — met, with a caveat. The rebuilt odd-squares video passes its blind test (every item 2, including the two new claim questions). Three rounds of cold reads converged: round 1 still found that the shape was ⌝ and not an L, an unexplained "?", and an unmotivated coda; round 3 found only edge items (a highlight color explained four seconds late, one remark in the wrong order). By the strict pass rule it is not a pass yet. Record: [`odd-squares/review/understanding.md`](explainers/odd-squares/review/understanding.md).

Rounds 2 and 3 also produced general rules: names match pictures (call it an L only if it is drawn as an L), and each case gets its own picture (the start-at-3 hole on its own small square).

**Next.**

- Backfill `narrative.md` for the other examples (softmax-temperature, dijkstra, git-bisect, ste-80, git-objects, cdn-request), and cold-read each rendering.
- The ledger check covers video symbols only. Prose and pages rely on the cold read.
- The rebuilt video is 4 min 21 s, up from 59 s. Measure whether a shorter cut keeps the cold read clean.
- odd-squares edge items from round 3: say what yellow and the colors mean at their first use; call the first tile an L when it appears; give the "where does the sum stop" section a stronger reason, or end the rule card in (2n − 1).
- The review sheet captures some frames mid-animation, and cold readers report them as overlaps. Take each frame after the animation it starts has finished.
- The cold read never runs out of findings. Grade findings by whether they are on the main line of the argument, and stop when only edge items remain.
