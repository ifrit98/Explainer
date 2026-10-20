# PRD-002: A rederivation eval

Status: approved, 2026-10-20 · Part 2 of 3 (PRD-001: ship v0.8; PRD-003: Olah-compass principles)

## Why

The v0.8 quiz is at its ceiling. Every condition scores 94–100%, because a model reader answers from any competent explanation (`docs/evals.md`). So the quiz cannot tell PRD-003 whether a change to the principles helps.

An explanation here aims for the reader to grok the subject: once they hold its building blocks, they can work out results nobody told them. Rederivation tests exactly that.

An example from outside the 30 subjects: an explanation of entropy as "the average length of the best code for a source" never mentions KL divergence, but a reader who holds that idea can derive it.

- Messages from p sent with a code built for q cost −log q each instead of −log p.
- So the average extra cost is Σ p log(p/q).
- Its properties follow without being taught:
  - it is never negative, because no code beats the one built for the real source;
  - it is zero only when p = q;
  - it is not symmetric;
  - it is infinite when q gives zero probability to something p produces.

Each quiz already ends with a one-step "predict" item. This PRD adds the several-step version and grades the chain of reasoning, not only the answer.

The reader is a model that already knows most results, so a right answer alone proves nothing. The fix: every step must rest on a part of the explanation that the reader names, and the grader checks that the part carries the idea.

## Goals

### 1. A rederivation target for every subject, frozen before any run

Each of the 30 subjects in `evals/artifact/questions.yaml` gets a target with three parts:

- **the question** the reader works out;
- **the expected steps:** 3–6 of them, one sentence each. Each step is an idea that any valid derivation needs, not the bookkeeping of one route. Each is marked as one of:
  - a **building block**, which a good explanation gives;
  - a **derived step**, which the reader works out from earlier steps.
- **the result:** the expected conclusion, specific enough to be right or wrong.

Each target passes three tests:

1. **Allowed building blocks only.** Every step uses one of:
   - an idea from the subject's question;
   - an idea from the quiz's expected answers;
   - background at the reader's level. That level is set by the `reader` line in `questions.yaml`: school mathematics and science, and basic programming.

   A target that needs an idea a focused explanation can leave out rewards length, not understanding. The conditions average from 606 to 1,689 words, so that bias would be large. PRD-003 would then tune the principles toward length, the opposite of their aim.
2. **Several steps:** at least three.
3. **Not stated:** a good answer to the subject's question would not state the result.

Claude drafts the targets. A fresh `claude -p` checker sees the subject's question, its quiz with the expected answers, and the target, then applies the three tests and returns pass or fail with a reason.

- A failed target is rewritten and checked again, at most twice.
- A subject whose target still fails gets no target, and the report lists it.
- The checker's verdicts are saved with the targets.

All 30 targets, test subjects included, are committed in one commit before the first rederivation run. Writing them now means the PRD-003 changes cannot shape them. The owner may skim them; nothing waits on that.

### 2. A rederive stage in the artifact eval

**Reader.** The reader gets the renderings only, as today, and the target's question. It does not see the expected steps or the result. It works the question out step by step. For each step it gives:

- the idea the step uses;
- the part of the explanation that idea comes from: a heading, a paragraph, a figure or diagram, or a control on a page;
- that idea in its own words.

If the explanation lacks an idea the reader needs, it says so and stops there. A gap is evidence.

**Outside-knowledge rule.** The same text goes in the reader prompt and the grader prompt:

- background at the reader's level may be used without citing anything;
- any fact about the subject must come from a part of the explanation that the reader names.

**Grader.** The grader works blind, under shuffled labels, as today. For each explanation it sees the text, the reader's chain, and the target's expected steps and result. The expected steps are a checklist of ideas, not a script. A step counts when the reader's chain establishes the same idea in any order, whether merged with another step, split in two, or reached by an equivalent route. The grader marks each expected step as one of:

- **supported:** the reader made the step, and either the cited parts carry the ideas it rests on, or it uses only reader-level background on top of earlier steps;
- **unsupported:** the reader made the step from its own knowledge, or from a part that does not carry the idea;
- **missing;**
- **stated:** a derived step that the explanation states outright, so the reader looked it up instead of working it out.

The grader also marks whether the result is right, and whether the explanation states the result outright.

**Scores.** Each condition gets three scores:

- **supported:** the share of expected steps that are supported;
- **raw:** the share made at all;
- **result right.**

These mirror the quiz's grounded and raw scores.

A stated derived step, or a stated result, is left out of that explanation's score: out of both the count and the total. The report counts these per condition. That way a long explanation is neither rewarded nor penalized for spelling out what the reader was meant to derive.

**Passes.** Every run of the stage makes three passes. In each pass, a fresh reader works through every build, and the grader grades it once under its own label shuffle. The spread across passes then covers both the reader's variation and the grader's.

The stage runs in every `eval artifact` run from now on, because PRD-003 needs it on new builds. It can also run alone on the saved builds of an earlier run.

### 3. A dev baseline on the saved v0.8 builds

- **No new builds.** The results go in a new folder that reuses the 40 builds saved in `evals/artifact/results/2026-10-04-dev/` (10 subjects × 4 conditions).
- **Models.** The reader and the grader use the `claude` CLI's default model, as the v0.8 baseline did.
- **Three passes,** as defined in Goal 2, each reported. The v0.8 ranges came from three different gradings, one of them the faulty first run, so they are no model to copy.
- **The report** gives, per condition, the three scores (with their range across passes), next to words and the v0.8 quiz score, plus a table per subject.

### 4. The result is written up, whatever it is

`docs/evals.md` gets a "Rederivation" section. It says what the eval measures and gives the three target tests. Then it reports what the dev baseline found, judged by the rule below.

**The separation rule, fixed before the first run.** Condition A beats condition B when A's supported score is higher than B's in all three passes.

The section says:

- which pairs of conditions separate;
- whether the order follows word count, which would mean the score measures length;
- if no pair separates, that the eval does not yet rank the conditions, and that PRD-003 should not adopt it as its measure without changes.

The "Next" list in ROADMAP §15 and the "Unreleased" section of `CHANGELOG.md` record the stage and its result.

### 5. A human check that does not block

`evals/artifact/human-check.md` is a one-page brief for a person who reads one explanation and works out its target on paper, before seeing the expected steps. Their chain is graded with the same rubric. `docs/evals.md` then records whether the person's score and the model reader's score on that explanation agree.

PRD-002 is done without any human results; they are added when they come in.

## Non-goals

- **No change to the principles, the skills, or other measured text.** That is PRD-003.
- **No new builds and no run on the test split.** A test run needs new builds for all 20 test subjects. It runs when PRD-003 confirms a change.
- **No changed-world variants and no reader run without an explanation.** They were cut to keep this simple.
- **No change to the quiz, its scoring, or the v0.8 reports.**

## Anti-goals

- Changing a target, its steps, or the separation rule after seeing any rederivation score.
- A target that rewards length because it needs an idea outside the allowed building blocks.
- Claiming a separation the rule does not support, or presenting a 10-subject dev run as more than that.

## Constraints

- **The repo is public (MIT).** Targets and docs contain no personal or private-project context.
- **The shipped v0.8 record stays as it is.** `evals/artifact/results/2026-10-04-dev/` and `2026-10-04-dev-haiku-reader/` stay byte-identical: `git diff --exit-code` on them is clean.
- **The builder never sees a target.** Build prompts are unchanged.
- **The reader never sees** the expected steps or the result.
- **Grading stays blind** under shuffled labels.
- **Every stage saves its output,** and a rerun skips what exists, as today.
- **Tests run offline,** without the `claude` CLI, like the existing artifact eval tests.

## Decided

All decided by the owner on 2026-10-19.

- **Rederivation is the test of grokking.** Once the reader has the building blocks, they can rederive the results and the rest of the theory from first principles.
- **A citation names a part of the explanation and restates its idea.** Word-for-word quotes are too strict, and an idea carried by a figure cannot be quoted.
- **The owner's time is not required.** Claude drafts the targets, a model checks them, and the owner may skim.
- **Simpler beats complete.** No changed-world variants and no control run without an explanation.
- **Human calibration happens when a tester is free.** It blocks nothing.
- **Targets are frozen before the first run.**

## Calls made by Claude (check these)

Approving this PRD approves these calls. Nothing else waits on the owner.

- **The allowed-building-blocks test:** the question, the quiz's expected answers, and reader-level background. This keeps the score from rewarding length.
- **Targets for all 30 subjects now;** only dev runs in this PRD.
- **The separation rule:** higher in all three passes.
- **A pass is a fresh reader run, graded once under its own shuffle.** This triples the reader calls in every run. Reads are cheap next to builds, and only this design tests whether a difference survives the reader's own variation.
- **Credit for other routes.** Expected steps are a checklist of ideas, credited in any order or form. Each step must be one that any valid derivation needs.
- **Stated derived steps and stated results are left out of the score and counted.** They are neither rewarded nor penalized.
- **Scores:** supported, raw and result-right, mirroring the quiz.
- **The rederive stage joins every artifact eval run** from now on.
- **No release is decided here.** The owner decides at the end whether PRD-002 ships as v0.9.0 or waits for PRD-003.

## Left to the builder

- Field names in `questions.yaml`, and the prompt wording beyond the outside-knowledge rule.
- The CLI form for running the stage on an earlier run's builds.
- How the new folder reuses the builds, by copy or by reference, provided the v0.8 folders stay unchanged.
- Whether the grader sees a subject's four explanations in one call, as today, or one at a time, provided the labels stay shuffled.

## Done when

- Each of the 30 subjects has a target whose checker verdict is pass, or is listed as having none. The targets were committed before any rederivation result.
- The dev baseline is in a new results folder with three passes. Its report shows the scores next to word count and the quiz.
- `docs/evals.md` states the result under the separation rule, including "no separation" if that is the outcome.
- The v0.8 results folders are unchanged.
- `evals/artifact/human-check.md` exists.
- Tests pass offline, `explainer check` passes, and CI is green.
