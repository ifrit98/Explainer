# Blind understanding test — softmax-temperature, prose

Run 2026-10-03 with `explainer quiz softmax-temperature --rendering prose`. Each reviewer was a fresh agent that saw only one file. `model.md` and `model.yaml` were removed from its copy.

| Quiz item | Rendering as published | Deliberately broken copy |
|---|---|---|
| 8 · T rises 1 → 3: top token, order? | 2: falls toward 0.25; order unchanged | 1: notices a contradiction, then says the order "might change" |
| 9 · Meaning of T = 0 | 2: greedy, always the top token | 0: "fully random" (the listed misconception) |
| 10 · Mechanism | 2: T divides logits; ratio exp(gap / T) | 2 |
| General items 1–7 | none scored 0 | none scored 0 |
| **Result** | **pass** | **fail** |

The broken copy changed four sentences: a high T "can move a different token into first place", the lower tokens "can overtake cat", the ratio "depends on the model", and T = 0 is "fully random".

## Gaps the reviewer of the published version reported

- The ratio law was stated without showing why it follows from softmax. **Fixed:** `explanation.md` now shows that the shared denominator cancels.
- No intuition for why exp is used. Open.
- No T = 3 value, so the reviewer had to extrapolate. Accepted: the question tests prediction.

## Re-test after v0.3.0 (completeness)

Run 2026-10-04 on the rewritten prose, with the claim question added (item 11).

| Item | Score | Answer (short) |
|---|---|---|
| 8 · T 1 → 3 | 2 | the top probability falls; the order holds for T > 0 |
| 9 · T = 0 | 2 | greedy decoding |
| 10 · mechanism | 2 | T scales the gaps; exp turns gaps into ratios; each ratio is its T = 1 value to the power 1/T |
| 11 · why exp (claim `why-exp`) | 2 | positive weights, order kept, gaps → ratios; divide-by-sum gives owl −0.4 and cancels T; squares break the order and also cancel T |
| **Result** | **pass** | |

The gap "no intuition for why exp" is closed. Remaining reviewer notes: "table below" pointed forward (fixed: it now names the Example section); the entropy definition is brief; why T exists at all is out of scope.
