# Blind understanding test — dijkstra, video

Run 2026-10-04 with `explainer quiz dijkstra --rendering video`. The reviewer was a fresh agent that saw only `captions.srt` and `review.png` (one frame per narration line, with the spoken text).

| Item | Score | Answer (short) |
|---|---|---|
| 8 · B first 4, final 3? | 2 | after C settles at 2, A→C→B = 2 + 1 = 3 < 4 |
| 9 · settled after D? | 2 | E at 10: smallest unsettled estimate (E 10, F 14) |
| 10 · assumption | 2 | lengths ≥ 0; otherwise a settled distance can be too large |
| General 1–7 | 1–2 | item 4 partial: the video names no single variable to vary |
| **Result** | **pass** | |

## Gaps the reviewer reported (open)

- The finality argument is spoken over a static frame. Show the settled region and one competing path that leaves through an unsettled node, with numbers.
- The video does not show what goes wrong with a negative length. A one-edge counterexample would show it.
- "Relax" is used in the on-screen rule but not defined in the narration.

## Re-test after v0.3.0 (completeness)

Run 2026-10-04 on the re-rendered video (main run plus the negative-edge chapter), with the claim questions added (items 11–12).

| Item | Score | Answer (short) |
|---|---|---|
| 8 · B 4 → 3 | 2 | via C: 2 + 1 = 3 < 4 |
| 9 · after D | 2 | E at 10, the smallest unsettled estimate |
| 10 · assumption | 2 | lengths ≥ 0; with C→B −2, B settles at 2 but the true distance is 1 |
| 11 · why smallest (claim `why-smallest`) | 2 | settling B at 4 when A reached it would be wrong; via C it costs 3 |
| 12 · finality with numbers (claim `guarantee-final`) | 2 | B at 3 while D 10, E 12, F ∞; the negative-edge graph as the counterexample |
| **Result** | **pass** | |

Closed: the finality argument now has this run's numbers on screen; the negative-edge counterexample is shown; "relax" is defined in the narration. Still open: the narration uses "distance" and "estimate" for the same thing; the finality segment is quick (about ten seconds).
