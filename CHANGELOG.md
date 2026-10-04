# Changelog

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
