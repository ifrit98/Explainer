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
