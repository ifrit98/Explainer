# Understanding tests: odd-squares

## Before the narrative pass (v0.4.0 video, 59 s)

Run 2026-10-04. Two fresh agents saw the same video (captions and review sheet).

**Blind test: pass.** Every quiz item scored 2. The reviewer explained the n-th L correctly, because it filled the gaps from context. Its audit listed n as undefined and "square" with three meanings, but the pass rule does not count audit findings.

**Cold read (first viewing, in order): many findings.**

| At | Finding |
|---|---|
| 0:00–0:08 | The colors of the odd numbers are never explained; "+ 7" and "+ 9" are shown but not said. |
| 0:12 | "They do not prove a rule": which rule? The rule is never stated in words, anywhere in the video. |
| 0:15 | "Square" means a tile here, a square of tiles at 0:15, and a square number at 0:08. |
| 0:27 | "L" is used for the first time, with no introduction. |
| 0:31 | "The fifth square": the fifth L, the 5 × 5 square, or the fifth square number? |
| 0:34 | "The n-th L": n is never introduced. The braces say "n − 1" while the narration said "four". The jump from 4 + 4 + 1 to 2n − 1 is only on screen. |
| 0:38 | n² − (n − 1)² = 2n − 1 is on screen and never mentioned. Why 2n − 1 is the n-th odd number is not given. |
| 0:42 | To answer the prediction, the viewer needs the rule, which has not been said. |
| 0:48 | 19 is never said to be the tenth odd number; Ls 6–10 share one color and cannot be counted. |
| 0:53 | "The rule holds for every n because each step adds the same kind of L": the rule and the step are still not said; the formula is still being written when the video ends. |

Motive: a reason to use a picture was given; no reason to care about the question and no reason for L shapes.

## Narrative cold read (before rendering)

`narrative.md` was written from these findings, then cold-read before any scene code. The reader found a structural problem: n meant the count of odd numbers (beat 2), the side of the square (beat 8), and a position in the list (beat 9), and "2n − 1 is the odd number in position n" was supported by three examples, after the video said examples do not prove anything. The reviewer's suggestion became the new argument: each L is two bigger than the one before, and the first L is one tile, so the Ls are the odd numbers in order. n keeps one meaning: the count of odd numbers, which is also the number of Ls and the side.

## After the narrative pass (v0.5.0)

Each round: a fresh cold read of the rendered video, fixes in `narrative.md` first, then the scene.

| Round | Blind test | Cold read: main findings | Fixed by |
|---|---|---|---|
| 1 (3 min 19 s) | pass, every item 2 (incl. the two new claim questions) | the shape was ⌝, not an L (the square grew from the bottom left); the "?" was never explained; the 11-tile L was only described; Ls 6–10 had colors with no number; the 2n − 1 coda had no motive, an undefined "2n", and no numeric check; the video ended on the coda | grow from the top right (a column on the left, a row along the bottom); say what "?" means and when it goes; draw the next L faintly; the full sum to 19 in the L colors; a motive, the middle step, and checks at n = 1, 5, 10; end on the answer |
| 2 (3 min 52 s) | — | main line clean (captions 1–54); remaining at the edges: no purpose for the opening sums; yellow and the underbrace never explained; "the first tile is an L" before an L had been split into row, column, and corner; the hole shown on the 10 × 10 square, not on 3 + 5; the coda algebra shown at once | a purpose line; "yellow marks what to look at"; "the brace marks the n odd numbers"; the first-tile remark moved after row + column + corner; the 3 + 5 Ls alone with a dashed hole (9 − 1 = 8); the algebra revealed step by step as it is said |
| 3 (4 min 21 s) | — | 78 captions, nearly all with nothing unresolved. Strongest: the mechanism (1:50–2:29) and the start-at-3 hole. Remaining: yellow and the color link explained a few seconds after they first appear; "after n Ls" said before the first tile is called an L; the row-and-column description switches from "sharing a corner" to "plus one corner" unsaid; the "where does the sum stop" section has a weak motive; several reported overlaps are frames captured mid-animation | recorded, not fixed (below) |

**Result: converged, not a strict pass.** Round 3 meets every part of the pass rule except "no reference unresolved, nothing shown but unsaid": a handful of edge items remain, listed in the roadmap. Each round finds less, and smaller: the old video's cold read found the result never said and n never introduced; round 3 finds a highlight color explained four seconds late.

The question, the result in words, the motive, the reason for the approach, and the close were present from round 1 on. The strongest moment in every round was the mechanism (row + column + corner, then "two bigger").
