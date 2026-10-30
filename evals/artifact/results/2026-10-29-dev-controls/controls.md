# Rederivation controls, 2026-10-29 (PRD-002a)

Source builds: `evals/artifact/results/2026-10-04-dev`. Baseline: `evals/artifact/results/2026-10-20-dev-rederive`. Each subject's `principles` explanation had one building block cut (`principles-cut` here); the reader read only the cut copy, the baseline's chains for the other three conditions were reused, and the grader graded all four fresh, blind, in three passes.

**Verdict: trusted.** Caught in 4 of 5 counted subjects (needs 4); clean-set blocks lost: 0 (at most 1); subjects counted: 5 (at least 5). Counting every leaked cut as a miss instead: trusted.

Marks per pass (the grader's own marks): s supported, u unsupported, m missing, t stated, – none given. Caught: the cut block is u or m in all three passes.

| subject | cut block | intact (baseline) | cut | caught | uncut blocks | derived, intact → cut | supported, intact → cut | gap named | leak check |
|---|---|---|---|---|---|---|---|---|---|
| float-sum | 1 | s, s, s | s, s, s | no | 2: s, s, s | 3: s, s, s → s, s, s; 4: m, s, s → s, s, s | 3/4, 4/4, 4/4 → 4/4, 4/4, 4/4 | no, no, yes | pass 1: no leak; pass 2: no leak; pass 3: no leak |
| greenhouse | 1 | s, s, s | m, m, m | yes | 2: m, m, m | 3: t, t, t → m, m, m; 4: t, t, t → m, m, u | 2/2, 2/2, 2/2 → 0/4, 0/4, 0/4 | yes, yes, yes | – |
| heat-pump | 2 | s, s, s | u, u, u | yes | 1: s, s, s | 3: s, s, s → s, s, s; 4: s, s, s → s, s, s | 4/4, 4/4, 4/4 → 3/4, 3/4, 3/4 | no, no, yes | – |
| key-exchange | 3 | s, s, s | m, m, m | yes | 1: s, s, s; 2: s, s, s | 4: s, s, s → s, s, s; 5: s, s, s → m, m, m | 5/5, 5/5, 5/5 → 3/5, 3/5, 3/5 | yes, yes, yes | – |
| two-tides | 2 | s, s, s | m, m, m | yes | 1: s, s, s | 3: t, t, t → s, s, s; 4: s, s, s → m, m, m | 3/3, 3/3, 3/3 → 2/4, 2/4, 2/4 | yes, yes, yes | – |

Intact marks are the baseline's recorded marks, in which `stated` on a block had already been turned into `supported`; the cut copy's are the grader's own.

Passes with no grader mark for the cut block (counted as not caught): none.

Labels: the stage shuffles labels once per subject from one generator per pass, and this run covers fewer subjects than the baseline, so each subject's label shuffle differs from its baseline pass.

Dropped (the cut failed its check 3 times): bloom-filter.
Leaked (a confirmed passage still carries the cut block): none.

## Left out

- **antibiotic-resistance.** The question gives the pre-existing resistant mutations (block 1). Selection (block 2) is school biology, and the question takes for granted that one drug alone ends in resistance.
- **gps-relativity.** The question states the receiver's clock error as a fourth unknown (block 2). It ties a satellite's clock error to its distance, and distance = speed × time is school physics (block 1).
- **quorum.** The question states the write group and the committed write (block 1). Block 2 was marked unsupported in two of the three baseline passes.
- **vaccine-memory.** The question's model states both blocks: matching cells multiply until there are enough, and vaccination leaves 1,000 times more of them.
