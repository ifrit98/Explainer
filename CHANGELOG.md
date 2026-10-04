# Changelog

## 0.5.0 — 2026-10-04

The narrative pass: an explanation is a model plus the path a first-time reader takes through it.

- **`narrative.md`** (Pass 3, principles §11), scaffolded by `explainer new`: the reader before and after; the question and the result in words; a motive and a reason for the approach; an introduction ledger of every term, symbol, name, and visual convention; the beats in order, each with its bridge, what is shown, and what is said; concrete to symbol; links between representations; the close.
- **`explainer coldread <slug> --rendering R`**: a fresh agent meets the narrative or one rendering for the first time and reports, in order, every reference it was not given, everything shown but unsaid, every leap, and whether the question, motive, and close are there. `--rubric` prints the pass rule. The `verify` skill runs it before the blind test.
- **Ledger check:** with a `narrative.md`, `explainer check` fails a scene symbol (on-screen math, a math label, "the n-th" in speech) that the ledger does not introduce. `check -v` notes explainers with no claims or no narrative.
- **Layout:** a `crowded` issue for text closer than 0.1 units to other text. `stagger_labels` spaces its rows by label height (it fixes two touching labels in the softmax video).
- **odd-squares, rebuilt from a narrative:** the old video passed its blind test and failed its cold read (n never introduced, the result never said aloud, two formulas never read). The narrative's own cold read, before rendering, changed the argument: each L is two bigger than the one before, and the first L is one tile, so the Ls are the odd numbers in order. The Ls are now real L shapes, the next L is drawn, the full sum to 19 is shown in the L colors, and the video ends on the answer. Claims and terms added.
- **Docs:** principles §11, a narrative step in the `explain` and `video` skills, a cold-read step in `verify`, the authoring guide's narrative section with the odd-squares case, concepts, CLI, and model reference.

## 0.4.0 — 2026-10-04

Review findings become rules. Each finding from the v0.3.0 blind tests is fixed in its example and turned into a check, a probe rule, or a template line that applies to every explanation.

- **Terms:** `terms` in `model.yaml` lists the phrases a rendering must not use for a concept. `explainer check` fails on one. Probe rule 3 now asks for one name per concept.
- **Meaning of quantities:** probe rule 6 asks what each number shown means for the reader. `check -v` lists each `accept_unjustified` function as a debt.
- **Pace:** `render` and `review` report a claim with less than 1 s of pause after its line, or more than 10 s of narration over one picture after its mark.
- **Blind-test audit:** the reviewer also lists concepts with two names, numbers without a meaning, steps without a why, and (video) rushed points. The rubric treats each as a gap.
- **Pages keep predict pauses:** `explainer check` fails a page that plays a video with predict pauses through a plain `<video>`. The landing page now uses `Explainer.video`.
- **Mermaid:** `explainer check --diagrams` renders every Mermaid block with the pinned Mermaid CLI (`mmdc` or `npx`). CI runs it.
- **Examples:** `dijkstra` uses "estimate" for the tentative value and "distance" only for the final one; the finality argument is three lines, one step per picture, with pauses; relax is shown as a test. `softmax-temperature` replaces the entropy definition with a `why-entropy` claim (surprise in bits, why a log and not a count, live per-token surprise on the page), and pauses after why exp.
- **Second-round fixes from the audit:** softmax "scaled gap" (a `terms` entry, which also caught the page); Dijkstra's finality argument now draws the settled region as A and C, exits through D and E, and says why reaching D costs at least its estimate; the narration says each relaxation's sum. Probe rule 2 checks each step of an argument as written. Review-sheet headings show event times.
- **Principles:** §10 adds one name per concept, a meaning for each quantity, time for each claim, and "turn each review finding into a rule".

## 0.3.0 — 2026-10-04

Completeness: explanations must not omit the connections a learner needs.

- **Claims** in `model.yaml`: `why`, `guarantee`, `mechanism`, `definition`, `limit`, `misconception`, each with required fields (a `why` needs the simplest alternative and its failure; a `guarantee` needs an example and a counterexample). Renderings mark where they cover each claim (`<!-- claim: id -->`, `data-claim`, `self.claim()`), and `explainer check` fails on incomplete or uncovered claims.
- **Function rule:** a function named in `model.md` (exp, log, sqrt, sigmoid, …) with no `why` claim fails the check, unless `accept_unjustified` gives a reason.
- **`explainer probe`:** a prompt for a fresh agent that reads only `model.md` and lists omissions before rendering. On the existing examples it found "why exp" and the Dijkstra negative-edge counterexample.
- **Model template:** new sections Why this form, Concrete cases, Terms, Scope. Principle 10, "Complete the chain".
- **Blind test:** claims with `ask` become quiz questions; the rubric expects their cases.
- **Examples:** `softmax-temperature` now explains why exp (with the divide-by-sum and squares counterexamples, live on the page and in the video), why divide by T, shift versus scale, and a worked T = 2 step. `dijkstra` adds why the smallest estimate, finality with this run's numbers, path reconstruction, and a negative-edge chapter. `git-bisect` adds the halving trace and a case where bisect names the wrong commit.
- **Checks:** scientific notation is one number (6.0 × 10⁻⁶); hash fragments like `4e10` stay identifiers; `render` reports repeated narration lines.
- **Docs:** authoring guide, model reference, web toolkit reference, docs index, contributing guide.

## 0.2.0 — 2026-10-04

- Claude Code plugin (`explain`, `video`, `verify` skills; `bin/explainer`) and marketplace.
- `model.yaml` and `explainer check`; `load_model` and `explainer sync`.
- Review tooling: timelines, layout check, `explainer review`, `explainer quiz`.
- Stage 3 web toolkit and page template; predict-first gates, video predict pauses, MP4 chapters.
- Video components, LaTeX via TinyTeX, sentence-timed captions, fail-fast scenes.
- Examples: `odd-squares`, `dijkstra`, `cdn-request`. CI.

## 0.1.0 — 2026-10-03

- Explanation-compiler workflow (`CLAUDE.md`, `explain` and `video` skills).
- Video pipeline: Manim, manim-voiceover, local Kokoro voice with exact bookmark timing.
- Examples: `softmax-temperature` at four stages, `ste-80`, `git-bisect`, `git-objects`. GitHub Pages site.
