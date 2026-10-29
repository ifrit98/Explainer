# PRD-002a: Does the rederivation test catch a missing block?

Status: approved, 2026-10-29 · Amends PRD-002, before PRD-003 (Olah-compass principles)

## Why

PRD-002's dev baseline came out near the ceiling. Every condition was credited with 90–100% of the expected steps in every pass. The one separation, none > published, rests on half of one compound building block in one subject (two-tides), and it follows word count (`docs/evals.md`, "Rederivation").

That result has two readings, and they lead to different next steps:

- **The test works, and the explanations really do contain the blocks.** Then PRD-003 can use the test, and the near-ceiling score is a fact about the v0.8 builds.
- **The test is blind.** A strong model reader may fill in a missing fact from its own knowledge, and the grader may credit it. Then the near-ceiling score says nothing, and the test must be fixed before PRD-003 relies on it.

Tuning the test until the four conditions come out different would fit it to the answer we want. This PRD checks the test against cases where the right answer is known instead: explanations with one building block cut out on purpose. A test we can trust marks the cut block as not supported.

## Goals

### 1. Six cut explanations, frozen before any run

**The starting build.** The saved v0.8 `principles` build in `evals/artifact/results/2026-10-04-dev/work/<id>/principles/`. Each is a single `explanation.md` with no page or script, so a cut fact cannot survive somewhere else in what the reader is shown.

**Which blocks can be cut.** A cut is a fair test only if a working test must then withhold credit. That is true only of a block the explanation alone can supply. So a block is eligible when all four of these hold:

1. the target question neither states nor takes it for granted;
2. it is not background at the reader's level (the `reader` line in `questions.yaml`);
3. it does not follow from the subject's other blocks plus that background;
4. the intact `principles` build was marked supported for it in all three passes of the PRD-002 baseline (`evals/artifact/results/2026-10-20-dev-rederive/`). Otherwise the cut would be a free catch.

In each subject, the last eligible block is cut. A subject with no eligible block is left out. Claude classified the 20 dev blocks against this rule, using only the targets and results that already exist.

| subject | cut | the block, in short |
|---|---|---|
| bloom-filter | 1 of 1 | adding an item sets its k bits to 1, and bits are never cleared |
| float-sum | 1 of 2 | doubles are binary fractions: a value is exact only if its denominator is a power of 2 |
| greenhouse | 1 of 2 | the Earth radiates to space from the height where infrared escapes, and more CO2 raises that height |
| heat-pump | 2 of 2 | the ideal heating limit is COP = T_hot ÷ (T_hot − T_cold), in kelvin |
| key-exchange | 3 of 3 | recovering an exponent from g^x mod p is infeasible for large p |
| two-tides | 2 of 2 | the Sun's tidal effect is about half the Moon's, and in line the two add |

| left out | why |
|---|---|
| antibiotic-resistance | The question gives the pre-existing resistant mutations (block 1). Selection (block 2) is school biology, and the question takes for granted that one drug alone ends in resistance. |
| gps-relativity | The question states the receiver's clock error as a fourth unknown (block 2). It ties a satellite's clock error to its distance, and distance = speed × time is school physics (block 1). |
| quorum | The question states the write group and the committed write (block 1). Block 2 was marked unsupported in two of the three baseline passes. |
| vaccine-memory | The question's model states both blocks: matching cells multiply until there are enough, and vaccination leaves 1,000 times more of them. |

Float-sum's block 2 and greenhouse's block 2 are not eligible either. Each follows from block 1 or leans on it.

**The cut.** A fresh `claude -p` cutter gets the explanation and the block.

- It removes every sentence that states the block or lets a reader recover it, including a stated derived step that gives the block away.
- It keeps the rest word for word, rewording only where a removal breaks a sentence.

**The check.** A separate fresh `claude -p` checker sees the cut copy, the target question, the reader line, and the subject's building blocks. It quotes any passage behind its answers.

- It confirms that this reader cannot get the cut block from the cut copy, the question, or background. This also re-checks the eligibility rule.
- It confirms that every block in the clean set (Goal 3) is still in the copy.
- A cut that fails is redone, at most twice.
- A subject whose cut still fails leaves the count, and the report lists it.

**The diff** of each cut is saved. Claude reads every diff before the freeze, and redoes (as one of the two retries) any cut that removed more than the block and what implies it.

**Freeze.** The cut copies, the checks, the diffs, and the bar in Goal 3 are committed in one commit before any rederivation run on a cut copy.

### 2. A controls run

A new results folder, `evals/artifact/results/<date>-dev-controls/`, holds a builds folder laid out like an artifact run, so the PRD-002 rederive stage takes it unchanged:

- the six subjects' `none`, `quick`, and `published` builds, copied from v0.8;
- the cut copy in place of each `principles` build.

**Reads.** The run reuses the PRD-002 baseline's reader chains for `none`, `quick`, and `published`, pass for pass. Only the cut copy is read again.

**Grading.** The grader grades all four explanations fresh, blind under shuffled labels, exactly as in the baseline. So the only differences from the baseline's pass k are:

- the cut copy;
- its fresh read;
- a fresh grading call.

The reader and grader prompts are word for word those of the baseline run. The grading code has changed since in two ways that touch only the calling: a reply that doesn't fit is asked again once, and the raw marks are kept.

**Passes and models.** Three passes. The reader, grader, cutter, and checker use the `claude` CLI's default model, as the baseline did.

**The leak check, after the run.** A cut the checker passed may still leave the block in a passage it missed. Such a passage would let the reader cite the block and the grader credit it, which would look like a blind test. So for each subject whose cut block is not caught (Goal 3):

- a fresh `claude -p` checker sees the reader's chain and the cut copy;
- it says whether a part the reader cited, as it stands in the copy, carries the cut block, and if so quotes that passage word for word.

A leak counts only when code confirms that the quote appears in the cut copy, ignoring differences in whitespace. If a confirmed leak is found in any pass, that subject leaves the count, and the report lists it with the quote. Otherwise the subject counts as a miss.

This check can only ever turn a miss into an exclusion, and it asks much the same question the grader answered. So Goal 3 limits what it can do to the verdict.

### 3. The bar, fixed in the freeze commit

The bar uses the grader's raw marks, before `stated` on a block is turned into `supported`.

**Caught.** The cut block is marked unsupported or missing in all three passes. Any other mark in any pass, `supported` or `stated`, means it was not caught.

**Clean.** An uncut block stays supported in all three passes when two things are true: the intact build was marked supported for it in all three baseline passes, and it does not rest on the cut block. There are 4 such blocks:

- heat-pump block 1;
- key-exchange blocks 1 and 2;
- two-tides block 1.

**Counted subjects.** The six subjects in Goal 1, minus any whose cut failed its check and any whose cut leaked.

**The verdict:**

- **Trusted:** caught in at least 80% of the counted subjects, rounded up (5 of 6, or 4 of 5), and at most one of the clean-set blocks loses support.
- **Blind:** caught in fewer than that.
- **Inconclusive:** any of these:
  - fewer than 5 subjects are counted;
  - the catch bar is met, but more than one clean-set block loses support. The cuts or the reads then damaged more than the cut block, so the catches may come from that damage;
  - the verdict is trusted only because of leak exclusions: counting every leaked subject as a miss would make it blind.

The report gives the verdict both ways: with the leak exclusions, and with every leaked subject counted as a miss.

### 4. A report and a write-up, whatever the result

A controls report next to `rederive.md` gives, per subject:

- the cut block's raw mark in each pass, next to the intact build's baseline marks;
- the marks of the uncut blocks;
- the marks of the derived steps, intact and cut. Derived steps that stay supported after their base is cut are direct evidence for making a derived step's credit depend on the blocks it rests on;
- the supported share, intact and cut;
- whether the reader named a gap;
- the leak check's answer, where one ran;
- the four subjects left out, and why.

`docs/evals.md` gets a subsection under "Rederivation". It gives the verdict under the bar and what it means for PRD-003:

- **Trusted:** on targets with an eligible block, the test notices a missing block. On those six subjects, the baseline's near-ceiling score is then a fact about the v0.8 builds, not a sign of a blind test. PRD-003 may use the test, but only on targets with an eligible block.
- **Blind or inconclusive:** PRD-003 does not use the test as it is.

Either way, the subsection notes what the eligibility rule found. In four of the ten dev targets, the question or background supplies every block, or every block the intact build was reliably credited with. Those targets can't show a missing block in any condition, so on them the ceiling comes from the target, not the builds. PRD-002's blocks test allowed blocks from the question on purpose, so the 20 test-split targets may share the problem.

ROADMAP §15 ("Next") and the "Unreleased" section of `CHANGELOG.md` record the result. "Next" also gets one item: before PRD-003 relies on the test-split targets, classify them by the same eligibility rule.

### 5. Only if the verdict is blind: fix the test against the controls

This part gets its own plan after Goal 4's result, because the report's diagnostics say which fix is needed. Its rules are fixed now:

- **A new scoring version.** The frozen targets, the PRD-002 scoring, and every reported result stay as they are. A change to a target, such as splitting a two-fact block, makes a new versioned target set. That set passes the PRD-002 checker and is frozen before any run.
- **The candidate fixes:**
  - a derived step counts only when the blocks it rests on count;
  - blocks that hold two facts are split;
  - a weaker or constrained reader;
  - a stricter grader rule for outside knowledge.
- **Tuned only against the cut copies,** where the right answer is known. Never against the four conditions.
- **Confirmed on held-out controls.** A second set of cut copies is made the same way from another condition's builds and frozen before the fixed test sees it. It must pass the same bar.
- **Then one fresh four-condition dev run** with the fixed test, judged by the PRD-002 separation rule and written up whatever it shows.

If the verdict is inconclusive, the PRD reports it and stops. The owner decides what follows.

## Non-goals

- **No change to the principles, the skills, or other measured text.** That is PRD-003.
- **No new builds and no run on the test split.**
- **No change to the frozen targets, the PRD-002 scoring, or any reported result.**
- **No code change to the test in Goals 1–4.** Only Goal 5 may change it.
- **No human check here.** It comes next, from `evals/artifact/human-check.md`.

## Anti-goals

- Choosing the cut blocks, the bar, or the verdict wording after seeing any control result.
- Tuning anything against the four conditions.
- Counting a cut that leaks, or one that removed more than its block, as a catch.
- Calling the test trusted on a run that missed the bar.

## Constraints

- **The repo is public (MIT).** No personal or private-project context.
- **Earlier results stay as they are.** `evals/artifact/results/2026-10-04-dev/`, `2026-10-04-dev-haiku-reader/` and `2026-10-20-dev-rederive/` stay byte-identical: `git diff --exit-code` on them is clean.
- **The targets stay frozen.** `test_targets_are_the_frozen_ones` passes unchanged.
- **Neither the reader nor the grader is told that any build was cut.** The reader never sees the target's steps or result. The grader stays blind under shuffled labels.
- **Every stage saves its output,** and a rerun skips what exists.
- **Tests run offline,** without the `claude` CLI.

## Decided

All decided by the owner.

- **The trust test is a set of explanations with one building block cut out** (2026-10-22). The test is trusted if it reliably catches them, even if the four conditions still come out close.
- **One cut per eligible dev subject,** made from the `principles` builds by a model, confirmed by a separate check and a diff (2026-10-22).
- **Only blocks the explanation alone can supply are cut, which leaves six subjects. The bar is at least 5 caught of the 6** (2026-10-24). This replaces the earlier 8 of 10, after the builder check found four chosen blocks that the reader gets from elsewhere.
- **The known fixes come only if the controls fail** (2026-10-22). They are tuned on the controls, never on the conditions, and are followed by one fresh four-condition run.
- **Small first** (2026-10-22). This PRD, then the human checks, then PRD-003.

## Calls made by Claude (check these)

Approving this PRD approves these calls.

- **The name PRD-002a,** so the Olah-compass PRD stays PRD-003 and existing references still hold.
- **The classification of the 20 dev blocks** in the two tables of Goal 1. The checker re-checks every chosen block before the freeze.
- **Bloom-filter stays,** though its only block is its mechanism, so the cut removes most of the explanation. It still tests whether a reader who knows Bloom filters well gets credit without the explanation.
- **Caught means unsupported or missing in all three passes,** on raw marks.
- **The leak check after the run.** A leaked cut leaves the count instead of counting as a miss, but only on a word-for-word quote that code finds in the cut copy. The verdict is reported both ways. A verdict that is trusted only because of leak exclusions is inconclusive.
- **"Trusted" covers only targets with an eligible block.** PRD-003 may use the test only on those, and the test-split targets get classified first.
- **At least 5 counted subjects are needed for a verdict.** Below that, the result is inconclusive.
- **The clean set of 4 blocks and the inconclusive verdict.** At most one clean-set block may lose support.
- **The eligibility rule reads the baseline's recorded marks,** which turn `stated` on a block into `supported`. The baseline predates the saving of raw marks.
- **The cut copy is graded among the other three conditions,** as in a real run, and not next to its own intact twin, which would let the grader spot the difference.
- **The baseline's reader chains are reused** for the three uncut conditions, so only the cut copy is read again.
- **The cutter and the checkers are fresh `claude -p` calls** with the default model, with at most two retries for a cut. Claude reads every diff before the freeze.
- **The held-out controls in Goal 5** come from another condition's builds.
- **Branch `prd-002a-controls` is stacked on `prd-002-rederivation`,** because PR #2 is not merged.
- **No release is decided here.**

## Left to the builder

- The CLI form: a new `eval` suite or a flag on an existing one.
- File names and layout in the controls folder, the prompt wording, and the report layout.
- How the builds folder copies the v0.8 builds, provided the v0.8 folders stay unchanged.

## Done when

- The cut copies, checks, diffs, and bar were committed before any control rederivation result.
- The controls run is in a new results folder, with three passes, the leak checks, and its report.
- `docs/evals.md` states the verdict under the bar, including "blind" or "inconclusive" if that is the outcome. ROADMAP and CHANGELOG record it.
- The three earlier results folders are unchanged, and the frozen-targets test passes.
- Tests pass offline, `explainer check` passes, and CI is green once pushed.
- If the verdict is blind, Goal 5 has its own plan and is done when either:
  - the fixed test passes the bar on the held-out controls and the fresh four-condition run is written up; or
  - the write-up says that no candidate fix passed.
