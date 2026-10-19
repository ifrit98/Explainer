# Evals

The checks and reviews in Explainer test one explainer at a time. They make that explainer better; they do not show that the toolkit helps on the next subject. Tuning the principles and the review prompts against the same ten examples fits them to those examples. Two evals measure the toolkit itself, on subjects it was never tuned on:

- `explainer eval chat`: a question in chat, answered with the principles and no files (the most common use).
- `explainer eval artifact`: an explainer built from scratch by a fresh agent, under each condition, then read and graded blind.

## The artifact eval

`evals/artifact/questions.yaml` holds 30 subjects that are neither examples nor chat-eval questions, from GPS to rent caps: 10 `dev`, 20 `test`. Each has the question, the misconception to avoid, and a fixed quiz of four questions with expected answers. The last is a prediction: a case the explanation need not mention, which the reader answers from the mechanism it gives. The quiz does not depend on what the builder chose to cover.

```bash
uv run explainer eval artifact --split dev                          # none, principles, quick, published
uv run explainer eval artifact --only float-sum --conditions none quick
uv run explainer eval artifact --conditions none old=git:v0.6.0 principles
```

For each subject and condition, three fresh `claude -p` agents run, with no settings files, no MCP servers, and no stdin:

1. **Build.** The builder gets the question and the reader, and writes `explanation.md`, `diagram.md`, or `index.html` (no video) in an empty project folder. Conditions differ only in guidance: `none`; `principles` (principles.md appended to the system prompt; also `git:<rev>` or a file); `quick` and `published` (the plugin loaded and the explain skill at that tier, running this checkout's CLI).
2. **Read.** The reader gets copies of the renderings only (no `model.md`) and answers the quiz. Each answer quotes the passage it rests on. An answer whose quote is not in the renderings scores 0, so a reader that answers from its own knowledge earns nothing. The reader also lists where it would stop or reread, and what it did not need.
3. **Grade.** The grader sees each subject's explanations and answers under shuffled labels, scores each answer 0–2 against the expected one, and checks the text for the misconception and for factual errors.

Every stage saves its output, and a rerun into the same folder skips what exists. The report (`evals/artifact/results/<date>-<split>/report.md`) gives, per condition: the grounded quiz score, the raw score, ungrounded answers, misconceptions taught and corrected, errors, stops and excess per explanation, words, the forms chosen, and the builder's cost and time.

**How to use it.** Change the principles or a skill only for a failure that appears in at least three `dev` subjects. Then run `test` to confirm the change before a release. Do not change anything in response to one test subject, and remove a rule when removing it costs nothing on `dev`.

## What the artifact eval found

Dev baseline, 2026-10-04, v0.7.0 principles and skills; builder, reader, and grader on the `claude` CLI's default model. [Report](../evals/artifact/results/2026-10-04-dev/report.md); the same builds read by Haiku: [report](../evals/artifact/results/2026-10-04-dev-haiku-reader/report.md).

| condition | effort rank (1–4) | quiz, strong reader | quiz, Haiku reader | words | errors | cost | minutes |
|---|---|---|---|---|---|---|---|
| none | 3.1–3.3 | 100% | 95% | 1,689 | 3–4 | $0.28 | 1.5 |
| principles | 1.7–1.9 | 99% | 98% | 1,006 | 1–4 | $0.21 | 1.0 |
| quick (skill) | 2.5–2.9 | 95% | 94% | 606 | 6–9 | $0.46 | 1.6 |
| published (skill) | 2.2–2.5 | 95% | 95% | 1,016 | 1–2 | $2.81 | 11.8 |

Effort rank: the grader's ranking of each subject's four explanations by the reader's effort, averaged over 10 subjects; the range covers three grading passes. Errors: factual errors the grader found, in all 10 explanations. Cost: the builder plus the reviews it ran.

- **The quiz is at its ceiling.** Every condition scores 94–100%, with a strong reader and with Haiku. A model reader answers from any competent explanation, so the quiz cannot rank the conditions. The published tier's own blind test is the same kind of instrument, so it is weak for the same reason.
- **The principles carry the measurable value.** Appended to the system prompt, they cut length by 40% (1,689 → 1,006 words), came first in the effort ranking in all three passes, and cost the least: a shorter explanation is cheaper to write.
- **The skill adds cost without a measured gain over the principles.** The quick tier is the shortest (606 words) but ranks below the principles and has the most errors, several from compression ("three spheres meet at a point"; they meet at two). The published tier costs 13 times as much as the principles and takes 12 times as long, for a lower rank and the same length.
- **Almost everything is prose.** With no guidance, 5 of 10 builders made a page; with the principles, none did; the skill made 3 diagrams in 20 builds. These subjects may simply be prose-shaped; the eval does not test video.
- **The ranking is a model's taste, and it is noisy.** Changing only what the grader saw (Markdown as written instead of stripped of inline code) moved the quick tier from 2.5 to 2.9. The principles-first and none-last results held in every pass; the order of quick and published did not. A person's ranking of a sample has to confirm it before it steers a change.

Two faults in the first run, both fixed: builders ran inside this repo, so Claude Code loaded its CLAUDE.md (and the principles) in every condition, including `none`; and the grader read Markdown with inline code removed, so formulas looked like blanks. Builds now run in a temp folder outside every project, with a guard.

## The chat eval

`evals/chat/questions.yaml` holds six questions about phenomena (why ice floats, why TCP starts slowly, how a wing makes lift, why a hash table is fast, why we see one side of the Moon, why salt melts ice). For each one it lists:

- **must:** the points a good answer makes for the reader, in any words;
- **misconception:** the wrong idea the answer must not teach;
- **budget:** a word count; an answer is not marked down for length alone, but the grader lists everything this reader did not need.

```bash
uv run explainer eval chat                                   # none, v0.5.0 principles, current principles
uv run explainer eval chat --conditions none mine=notes.md   # any system prompt in a file
```

Each answer comes from a fresh `claude -p` call in an empty folder, with no tools, no settings, no MCP servers, and no stdin, so no CLAUDE.md, plugin, or connector reaches it. The only difference between conditions is the system prompt. A second fresh call grades the answers to one question together, under shuffled labels, so it does not know which prompt wrote which answer. It scores the must points, the misconception, whether the answer comes first, factual errors, excess, and unclear passages, gives each answer 0–10, and ranks them.

The report goes to `evals/chat/results/<date>/report.md`, with every answer and `grades.json`.

## What the chat eval found

Two runs on 2026-10-04 (answers and grades by the `claude` CLI's default model). Run a: the principles before the chat rule. Run b: after it. Each run is graded on its own, so compare conditions within a run.

**Run a.** The principles raised the score from 6.5 to 7.2, put the answer first in every case, and cut unclear passages from 3.5 to 2.3–2.5 per answer. They also made the answers about 50% longer (393 → 580–590 words), and v0.6.0's rebalance changed nothing here: it acted on artifacts, not on chat. The excess the grader quoted showed why: the answers applied the artifact rules in chat. They had a Scope section, an epistemic tag on textbook facts, a list of predictions, a second guarantee case, and related phenomena nobody asked about.

**The rule it produced** (principles §12): a chat answer is not a small artifact. Apply §10 to the central question only, with no Scope section, no tags on settled facts, no headings under about 300 words, and usually 150–300 words.

**Run b**, with the rule:

| condition | score /10 | must points | answer first | excess / answer | unclear / answer | words | ranked best |
|---|---|---|---|---|---|---|---|
| none | 6.3 | 94% | 4/6 | 4.7 | 3.0 | 399 | 0 |
| v0.5 principles | 7.2 | 100% | 6/6 | 5.0 | 1.8 | 544 | 1 |
| current principles | 7.8 | 94% | 6/6 | 1.5 | 1.5 | 292 | 5 |

The current principles now give the shortest answers of the three (292 words, against 399 with no system prompt), with a third of the excess and the best score; the grader ranked them best on five of six questions. The cost: the wing answer left out how lift grows with angle and speed (one must point), the one question whose answer needs more than 300 words.

Reports: [run a](../evals/chat/results/2026-10-04-a/report.md), [run b](../evals/chat/results/2026-10-04-b/report.md).

## Limits of the chat eval

- Six questions, one grader, one model. Treat a difference of a few tenths of a point as noise.
- The grader is a model with its own taste. It sees the reader and the must points, not the principles.
- The answers come from a fresh CLI with no project context. Inside Claude Code the principles arrive together with other instructions, so behavior can differ.

## Review adoption

The review tools (probe, cold read, blind test) report findings; the author decides what to do with each. `explainer probe|coldread|quiz <slug> --run` runs a review with a fresh `claude -p` agent and saves it with numbered findings, `explainer decide` records the decision on each, and `explainer findings --stats` reports, per tool and severity, how many findings authors adopt. A tool whose findings are mostly declined over-reports: its prompt asks for more than this reader needs.

First measurement, across the v0.7.0 review rounds on nine examples (2026-10-04):

| Tool | Severity | Findings | Adopted |
|---|---|---|---|
| cold read | blocking | 17 | 100% of 15 decided |
| cold read | edge | 286 | 3% |
| cold read | excess | 36 | 6% |
| probe | main | 6 | 83% |
| probe | edge | 6 | 50% |
| blind-test audit | gap | 233 | 9% |
| blind-test audit | excess | 37 | 4% |

Blocking findings and the probe's main gaps are well calibrated. The cold read's per-unit edge lists and the blind-test audit were mostly noise. The prompts changed in response: an edge finding only where this reader would stop or reread (most units have none), at most five audit findings per list, and a rubric that treats an audit finding as a candidate, not a defect.

The blind-test grader needed the same correction. Its first rubric asked a full answer to repeat the rendering's own example and counterexample, and it failed correct answers for that: three of three blind tests "failed" on the same item. The rubric now scores a correct, specific statement as 2; `explainer quiz <slug> --regrade <run>` scores saved answers again under a changed rubric.
