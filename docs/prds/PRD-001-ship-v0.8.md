# PRD-001: Ship v0.8, the toolkit eval and what it found

Status: draft, 2026-10-19 · Part 1 of 3 (PRD-002: a rederivation eval; PRD-003: Olah-compass principles)

## Why

ROADMAP §15 ("Measure the toolkit, not the examples") is built but not shipped. The artifact eval runs, the dev baseline exists, and it found something that matters:

- the reader quiz is at its ceiling;
- plain principles beat the skill tiers on effort;
- the published tier costs up to 13× as much for no measured gain.

None of it is committed, so nobody else can see it, and the public repo still implies the v0.7 workflow is the measured best.

Shipping it now does three things:

- **Puts an honest negative result on the record** before the next round of work changes the principles. PRD-002 and PRD-003 build on this baseline, so it has to be fixed in history first.
- **Shows readers what was measured, including what didn't work.**
- **Clears the working tree,** so PRD-002 starts from a clean, tagged state.

## Goals

### 1. Release v0.8.0 containing the artifact eval and its results

- **New files:** `explainer_kit/artifact_eval.py`, `tests/test_artifact_eval.py`, and `evals/artifact/`. The last holds the questions and both result sets, `2026-10-04-dev` and `2026-10-04-dev-haiku-reader`.
- **Modified files:**
  - code: `agent.py`, `cli.py`, `runs.py`, and their tests;
  - docs and plans: `docs/cli.md`, `docs/evals.md`, `CHANGELOG.md`, `ROADMAP.md`, `CLAUDE.md`, and `docs/prds/`.
- **Changelog:** the "Unreleased" section in `CHANGELOG.md` becomes `0.8.0 — <release date>`.
- **Tag and release:** tag `v0.8.0`, and publish a GitHub release in the same style as the earlier ones (title, one-line summary, bullets).
- **Version bumps** follow the v0.7.0 commit: `pyproject.toml`, `plugin/.claude-plugin/plugin.json`, and the version pin in `plugin/bin/explainer`.

### 2. The release notes state the negative result plainly

Use the repo's own words from `docs/evals.md` and ROADMAP §15. The notes must say:

- the quiz is at its ceiling;
- the principles alone rank first on effort, at the lowest cost;
- the quick tier makes the most errors;
- the published tier costs 13× as much for no measured gain.

They also say the first run was invalid and why. Builders loaded the repo's CLAUDE.md in every condition, and the grader read Markdown with inline code stripped (`docs/evals.md`).

### 3. Fix the drift found on 2026-10-19, without touching measured text

`plugin/skills/` and `plugin/skills/explain/references/principles.md` are the text the eval measures: the `principles` condition appends `principles.md` word for word. They stay unchanged in this release, so the v0.8.0 tag holds exactly the baseline PRD-002 and PRD-003 build on.

- **AGENTS.md (currently untracked).** It is a copy of CLAUDE.md with "Claude" replaced by "Codex". That broke real paths (`.Codex/skills/`, `.Codex-plugin/marketplace.json`) and a command (`Codex -p`). Replace it with a short file that is accurate for any coding agent:
  - read `plugin/skills/explain/references/principles.md` before writing an explanation;
  - the skills live in `plugin/skills/`;
  - the review and eval commands call the Claude CLI (`claude -p`).

  It must not depend on Claude Code's `@` imports, which other agents do not follow.
- **Question counts in the docs.** There are two different sets of understanding questions:
  - the author's test in `principles.md` §7 has eight; the eighth is "Could anything be cut with no loss?";
  - the blind test in `explainer_kit/review.py:24-32` asks seven, and its seventh ("Which part was hardest to follow…") is not one of the author's eight.

  `docs/concepts.md:148` says "seven" and lists the author's first seven. Rewrite that passage so each set is described correctly, with its count and where it lives.

  Two related mismatches sit in measured skill text and stay as they are: "seven" in `plugin/skills/explain/references/html.md:89`, and the blind test not asking question 8. Record both in ROADMAP §15 for PRD-003.
- **The change rule.** ROADMAP §15 says a principle changes only for a failure seen in "at least three dev subjects"; `docs/evals.md:26` says "several". Use "at least three" in both.
- **ROADMAP index.** Add a §15 row to the index table. It currently ends at §14.

### 4. Tests, checks and CI pass

All tests pass, `explainer check` passes for every example, and CI is green on the release commit.

## Non-goals

- **No change to the principles, the skills, or the objective.** The README still says "least effort" after this release. The move to "least *wasted* effort" belongs to PRD-003, so the README, `principles.md`, and the graders change together.
- **No new eval subjects, no new eval runs, and no changes to scoring.** The results ship as they are.
- **No human calibration yet** (ROADMAP §15 "Next"). PRD-002 covers it.

## Anti-goals

- Softening the negative result, or presenting the dev baseline as more than a 10-subject dev run. The release must not read as a success story about the skill tiers.
- Shipping anything that changes what an existing example renders.

## Constraints

- **The repo is public (MIT).**
  - `evals/artifact/` was scanned on 2026-10-19: no absolute paths, usernames, emails, API keys, or session IDs. Re-check it if anything is regenerated before the commit.
  - Documents in `docs/prds/` hold no personal or private-project context.
- **Keep the release style** of v0.3.0–v0.7.0.

## Decided

- **The order:** this PRD ships first, then PRD-002 (eval), then PRD-003 (principles). (Owner, 2026-10-19.)
- **The negative result is published,** not held back. (Owner, 2026-10-19.)
- **The PRDs live in `docs/prds/` in this public repo.** (Owner, 2026-10-19.)

## Calls made by Claude (check these)

- **Measured skill text stays frozen in v0.8.** The doc fixes touch `docs/` and ROADMAP only. The two mismatches in skill text wait for PRD-003, which rewrites those files anyway.
- **AGENTS.md becomes a short, separate file, not a symlink.** A symlink to CLAUDE.md would pass along Claude Code `@` imports that other agents ignore, so they would still miss the principles.
- **The "least wasted effort" wording waits for PRD-003.** Changing only the README now would make it disagree with `principles.md` and the graders.

## Left to the builder

- The release title and summary line.
- Commit granularity before the tag: one commit, or one per goal.
- Whether to add a short "What the artifact eval found" paragraph to the README, linking to `docs/evals.md`.

## Done when

- `v0.8.0` is tagged and released on GitHub, and the release notes contain the four findings in Goal 2.
- `git status` is clean.
- `AGENTS.md` names no path or command that does not exist, and uses no `@` imports.
- `docs/concepts.md` describes both sets of questions correctly. ROADMAP §15 records the two skill-text mismatches for PRD-003.
- Docs and ROADMAP agree on "at least three".
- Tests, `explainer check`, and CI pass.

## Follow-up outside the code

- Pin Explainer on the GitHub profile by hand. GitHub has no API for profile pins.
