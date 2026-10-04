# Storyboard: odd-squares

> Derived from `../model.md`.

## 1. Learning objective

After the video, the viewer can explain why 1 + 3 + … + (2n − 1) = n² for every n, and compute the sum of the first ten odd numbers without adding them.

## 2. Conceptual sequence

1. The sums 1, 4, 9, 16, 25 are squares: a pattern.
2. Examples do not prove a rule.
3. Each odd number is an L that wraps the previous square.
4. An L has one row, one column, and one corner: 2n − 1 cells.
5. Predict: the first ten odd numbers.
6. The rule for every n.

## 3. Scenes

| # | Question the scene answers | Visual transformation | Bookmarks |
|---|---|---|---|
| 1 | What is the pattern? | Sum rows appear one at a time | `r1`–`r5` |
| 2 | Is a pattern a proof? | All sums flash | — |
| 3 | What does each odd number add? | L shapes wrap a growing square; matching term flashes | `g2`–`g5` |
| 4 | Why is an L always 2n − 1? | Row, column, corner recolor; braces; two equations | `parts`, `law` |
| 5 | What about ten? | Predict pause; square shrinks, five more Ls; 100 | `ten` |
| 6 | What is the rule? | The general identity | — |

## 4. Visual-object inventory

| Object | Color | First scene | Persists through |
|---|---|---|---|
| Sum rows | term colors match L colors | 1 | 1–6 |
| L shapes 1–5 | one color per odd number | 3 | 3–6 |
| L shapes 6–10 | ENTITY | 5 | 5–6 |
| Equations | TEXT (LaTeX) | 4 | 4 |

## 5. Rendering plan

Manim CE + explainer_kit, Kokoro `af_heart`, LaTeX for the equations. One predict pause.
