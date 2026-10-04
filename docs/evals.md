# Evals

The checks and reviews in Explainer test artifacts: one explainer at a time. The most common use is different: a question in chat, answered with the principles and no files. `explainer eval chat` measures that use.

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

## What it found

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

## Limits

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
