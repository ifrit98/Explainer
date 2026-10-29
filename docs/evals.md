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
| quick (skill) | 2.5–2.9 | 95% | 94% | 606 | 4–9 | $0.46 | 1.6 |
| published (skill) | 2.2–2.5 | 95% | 95% | 1,016 | 1–2 | $2.81 | 11.8 |

Effort rank: the grader's ranking of each subject's four explanations by the reader's effort, averaged over 10 subjects; the range covers three grading passes. Errors: factual errors the grader found, in all 10 explanations; the range covers the same three grading passes. Cost: the builder plus the reviews it ran.

- **The quiz is at its ceiling.** Every condition scores 94–100%, with a strong reader and with Haiku. A model reader answers from any competent explanation, so the quiz cannot rank the conditions. The published tier's own blind test is the same kind of instrument, so it is weak for the same reason.
- **The principles carry the measurable value.** Appended to the system prompt, they cut length by 40% (1,689 → 1,006 words), came first in the effort ranking in all three passes, and cost the least: a shorter explanation is cheaper to write.
- **The skill adds cost without a consistent measured gain over the principles.** The quick tier is the shortest (606 words) but ranks below the principles and has the most errors, several from compression ("three spheres meet at a point"; they meet at two). The published tier costs 13 times as much as the principles and takes 12 times as long, for a lower rank and the same length; its errors (1–2) overlap the principles' (1–4), fewer in one pass and more in another.
- **Almost everything is prose.** With no guidance, 5 of 10 builders made a page; with the principles, none did; the skill made 3 diagrams in 20 builds. These subjects may simply be prose-shaped; the eval does not test video.
- **The ranking is a model's taste, and it is noisy.** Changing only what the grader saw (Markdown as written instead of stripped of inline code) moved the quick tier from 2.5 to 2.9. The principles-first and none-last results held in every pass; the order of quick and published did not. A person's ranking of a sample has to confirm it before it steers a change.

Two faults in the first run, both fixed: builders ran inside this repo, so Claude Code loaded its CLAUDE.md (and the principles) in every condition, including `none`; and the grader read Markdown with inline code removed, so formulas looked like blanks. Builds now run in a temp folder outside every project, with a guard.

## Rederivation

The quiz checks what an explanation says. A reader who has grokked a subject can do more: from its building blocks, work out a result nobody told them. An explanation of entropy as "the average length of the best code for a source" never mentions KL divergence, yet a reader who holds that idea can derive it: messages from p sent with a code built for q cost −log q each instead of −log p, so the average extra cost is Σ p log(p/q), never negative, because no code beats the one built for the true source. The rederivation stage tests that, on the same held-out subjects.

**Targets.** Each subject in `evals/artifact/questions.yaml` has a `rederive` target: a question the explanation was never asked to answer, 3–6 expected steps, and the result. Each step is a building block (an idea a good explanation gives) or a derived step (worked out from the steps before it). A fresh agent checked every target (`explainer eval targets`, verdicts in `evals/artifact/rederive-checks.json`) against five tests: every step and the result are true; every building block comes from the subject's question, the quiz's expected answers, or background this reader already has; every derived step follows from earlier steps plus that background and brings in no new fact about the subject; each step is one any valid derivation needs; and a good answer to the subject's question would not state the result. The second and third tests matter most: a target that needs an idea a focused explanation may leave out would reward length, not understanding. All 30 passed (two after a revision) and were frozen in one commit before the first run; a test fails if a results folder's targets differ from the file.

**Reader and grader.** The reader gets the renderings and the target's question, never the steps or the result. It works the question out step by step, and for each step names the part of the explanation it rests on (a heading, paragraph, figure, or a control on a page) and says what that part gives it. Reader and grader get the same rule: background this reader already has may be used without a citation; every fact about the subject must come from a part the reader names. The grader sees each subject's explanations and the readers' working under shuffled labels, and marks each expected step, credited in any order, merged, split, or by an equivalent route:

- **supported:** made, and the cited parts carry the ideas it rests on (or it uses only background on top of earlier steps);
- **unsupported:** made from the reader's own knowledge, or from a part that does not carry the idea;
- **missing;**
- **stated:** a derived step the explanation states outright, so the reader looked it up. A stated step, or a stated result, is left out of the score and counted, so a long explanation is neither rewarded nor penalized for spelling out what the reader was meant to derive.

The headline is the **supported** share of expected steps; **raw** is the share made at all; **result right** the share of results that match. A run makes three **passes**: each is a fresh reader run over every build, graded once under its own label shuffle, so the spread covers both the reader's and the grader's variation. **The separation rule**, fixed before the first run: condition A beats condition B when A's supported score is higher than B's in all three passes.

```bash
uv run explainer eval rederive --builds evals/artifact/results/2026-10-04-dev   # the stage alone, on saved builds
uv run explainer eval artifact --split dev                                     # builds, quiz, then this stage
```

### What the dev baseline found

Dev baseline, 2026-10-20: the 40 v0.8 builds (10 subjects × 4 conditions), read and graded three times by the `claude` CLI's default model; no new builds. [Report](../evals/artifact/results/2026-10-20-dev-rederive/rederive.md).

| condition | supported (3 passes) | result right | stated steps | words | quiz (grounded) |
|---|---|---|---|---|---|
| none | 100%, 100%, 100% | 100%, 100%, 100% | 2, 2, 3 | 1,689 | 100% |
| principles | 95%, 100%, 97% | 89%, 89%, 100% | 4, 4, 5 | 1,006 | 99% |
| quick (skill) | 92%, 100%, 90% | 100%, 100%, 89% | 2, 2, 2 | 606 | 95% |
| published (skill) | 95%, 95%, 95% | 89%, 78%, 89% | 3, 3, 3 | 1,016 | 95% |

**Under the separation rule, one pair separates: none > published** (100% against 95% in every pass). No other pair does.

**What that result is made of.** About 38 expected steps count per condition, so 95% is two steps short. The gap comes from one subject, two-tides, and from half of one building block. Block 2 bundles two ideas: the Sun's tide is about half the Moon's, and at new and full Moon the two line up and add. The published explanation gives the ratio but never says when the tides add (no spring or neap tides), so the grader marked the block unsupported in all three passes. That is the gap the quiz already found (published scored 6 of 8 on two-tides, 0 on the spring-tide question). The quick explanation also gives the ratio, and only mentions in a "not covered" line that the Sun's bulges add to or partly cancel the Moon's; the grader marked its block unsupported, supported, and missing in the three passes, so it does not separate.

**How much a single subject moves between passes.** The same quick two-tides build scored 3/4, 4/4, and 1/4 supported steps in the three passes. A difference of a step or two in one subject is within what one fresh reader and one grading change on their own.

**Known defects, found after the run** (the targets are frozen, so they stay and are reported):

- **The float-sum target overclaims.** Its last derived step argues that adding 0.1 ten times cannot land exactly on 1.0 because each addition rounds. Rounding errors can cancel (`0.1` added five times does give exactly `0.5`), so the honest answer from the building blocks is "not guaranteed", which is what the principles and published readers said. They were marked wrong in passes 1 and 2; in pass 3 the published reader gave the same hedged answer and was marked right, so the grader was not consistent either. This lowers principles' and published's "result right" (published's also falls on two-tides in passes 2 and 3) and cost each one supported step in pass 1. The separation does not depend on it: two-tides alone carries none > published.
- **Real explanations stated derived steps outright in 3 of 10 subjects,** more often than the target checker predicted: the gps-relativity clock argument (three conditions), the greenhouse no-lapse-rate case (both derived steps, in principles, quick, and published), and the two-tides right-angle step (none and principles). Those steps are left out of the score, so for greenhouse three conditions were scored on building blocks alone.
- **Compound building blocks are graded inconsistently when half present.** The quorum block "any two majorities share a server, so the next group sees every committed write" is half present in the principles and quick explanations (they give the overlap, for conflicting writes, not for reads); the grader marked it unsupported in two of three passes. The two-tides block above is the same kind, and it carries the only separation.

**Does the order follow length?** Roughly. On the mean supported share the order is none (100%) > principles (97%) > published (95%) > quick (94%); by words it is none (1,689) > published (1,016) ≈ principles (1,006) > quick (606). The one separation goes in length's direction. The word count also leaves out what the grader reads in pages' scripts, and only none made pages (5 of 10).

**What we take from it (interpretation, not the rule).** With a strong model reader, rederivation mostly re-detects missing building blocks, which the quiz already catches; it does not yet show a difference in understanding between conditions. The one separation is small, comes from half of one building block in one subject, and favors the longest explanation. Whether PRD-003 adopts this stage, and what to change first (a weaker or constrained reader, harder targets with more derived steps, or human readers), is open: see ROADMAP §15.

**Human check:** none yet. A brief for testers is in [`evals/artifact/human-check.md`](../evals/artifact/human-check.md); results will be recorded here.

### Does the test catch a missing block?

PRD-002a, 2026-10-29. The baseline sat near its ceiling. That could mean the v0.8 builds are good, or that the test is blind: a strong reader fills in a missing block from its own knowledge and the grader credits it. To tell these apart, one building block was cut from saved `principles` explanations, and the unchanged stage was run on the cut copies. [Report](../evals/artifact/results/2026-10-29-dev-controls/controls.md). [The cuts and their review](../evals/artifact/results/2026-10-29-dev-controls/cuts/review.md), frozen before the run.

**What was cut, and why only six subjects.** A cut block can show up as missing only if the reader cannot get it elsewhere. So a block was eligible only if it is not in the target question or presupposed by it, is not background for this reader, cannot be derived from the other blocks, and was credited in all three baseline passes. Six dev targets have such a block. Four do not (antibiotic-resistance, gps-relativity, quorum, vaccine-memory): their questions or school background supply the blocks. For each of the six, a fresh agent removed the block and changed nothing else. A second agent checked three things: the block could not be recovered, the removal was not marked, and the other reliably credited blocks were still there (the clean set, 4 blocks). Each cut got at most three attempts. Bloom-filter's cut failed all three: its block (adding an item sets bits to 1, and bits are never cleared) is implied by the worked example and the error maths. So five subjects count.

**The bar, fixed before the run.** A cut is caught when the grader marks the cut block unsupported or missing in all three passes. Trusted needs three things: at least 80% of counted subjects caught, at most one clean-set block losing support, and at least five subjects counted. An uncaught cut can leave the count, but only if a leak checker quotes a passage that still carries the block and code finds that quote in the cut copy. The verdict is also given with every leaked cut counted as a miss. If only the exclusions make it trusted, it is inconclusive.

**Verdict: trusted, at the floor.** 4 of 5 cuts were caught, and 4 were needed. No clean-set block lost support, no leak was found, and the verdict is the same with leaks counted as misses. One more miss, or one more subject dropped or leaked, would have made it blind or inconclusive.

| subject | cut block | intact (baseline) | cut | caught | supported, intact → cut | result right, intact → cut |
|---|---|---|---|---|---|---|
| float-sum | 1: a value is exact only if its denominator is a power of 2 | s, s, s | s, s, s | no | 3/4, 4/4, 4/4 → 4/4, 4/4, 4/4 | 1 of 3 → 2 of 3 |
| greenhouse | 1: Earth radiates from the height where infrared escapes; CO2 raises it | s, s, s | m, m, m | yes | 2/2 → 0/4 in each pass | 3 of 3 → 0 of 3 |
| heat-pump | 2: ideal heating COP = T_hot ÷ (T_hot − T_cold) | s, s, s | u, u, u | yes | 4/4 → 3/4 in each pass | 3 of 3 → 3 of 3 |
| key-exchange | 3: the discrete logarithm is infeasible for large p | s, s, s | m, m, m | yes | 5/5 → 3/5 in each pass | 3 of 3 → 0 of 3 |
| two-tides | 2: the Sun's tide is about half the Moon's | s, s, s | m, m, m | yes | 3/3 → 2/4 in each pass | 3 of 3 → 0 of 3 |

Marks per pass: s supported, u unsupported, m missing. The supported counts change their denominators because stated steps are left out of the score.

- **The miss: float-sum.** The reader rebuilt the block from two sentences in the cut copy, plus its own knowledge of binary fractions. One sentence, the cutter's rewording of a sentence it removed, says a double holds a limited number of binary digits, so its values form a grid; the other says 1/10 repeats forever in binary. The grader credited the rebuilt block in every pass. The leak checker found no passage that carries the block, so the subject counts as a miss. This is either the blind case the controls exist to find, or a cut that left too much in; this run cannot tell which.
- **Caught does not mean the reader failed.** In heat-pump, the reader worked the formula out from the table the cut left: 318 K, a 50 K lift and an ideal COP of 6.4, a leftover the review named before the run. The reader got the result right in all three passes. The grader still marked the block unsupported, because the explanation does not give it. The test catches what an explanation leaves out, not what a reader cannot rebuild.
- **Derived steps.** Where a derived step rests on the cut block, it lost credit in three subjects: key-exchange step 5 (the eavesdropper needs a discrete logarithm) and two-tides step 4 (a third of a spring tide's range) went from supported to missing, and greenhouse steps 3–4 went from stated to missing or unsupported. In heat-pump it did not. Step 4 there is algebra on the cut formula, and it stayed supported in every pass. That is direct evidence for making a derived step's credit depend on the blocks it rests on.
- **Greenhouse's catch comes with a thinner explanation.** Block 2 presupposes block 1, so the cut removed most of block 2 as well. The design allows this, because block 2 is not in the clean set.

**Differences from the baseline.** The reader read only the cut copies. For none, quick and published, the baseline's chains were reused, and the grader graded all four fresh. One more difference was missing from the PRD's list. The stage shuffles labels once per subject, from one generator per pass, and this run covers five subjects, not ten. So each subject's label shuffle differs from its baseline pass.

**What it means.** On targets with an eligible block, the test notices a missing block. On the five counted subjects, the baseline's near-ceiling score is then a fact about the v0.8 builds, not a sign of a blind test. PRD-003 may use the test, but only on targets with an eligible block. The evidence is thin: five subjects, one model, a verdict at the floor, and one miss of the kind the controls look for.

**What the eligibility rule found.** In four of the ten dev targets, the question or background supplies every block, or every block the intact build was reliably credited with. Those targets cannot show a missing block in any condition, so on them the ceiling comes from the target, not from the builds. PRD-002's blocks test allowed blocks from the question on purpose, so the 20 test-split targets may share the problem. They need the same sort before PRD-003 relies on them.

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
