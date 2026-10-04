# Semantic model: sums of odd numbers

## Central question

Why does 1 + 3 + 5 + … + (2n − 1) always equal n²?

## Audience and prior knowledge

Readers who know odd numbers, square numbers (1, 4, 9, 16, …), and school arithmetic. A letter that stands for a number is known only after the explanation introduces it.

## Entities

| Entity | Definition | Status |
|---|---|---|
| Odd number | The k-th odd number is 2k − 1: 1, 3, 5, 7, 9, … | definition |
| Partial sum | The sum of the first n odd numbers. | definition |
| Tile | One small unit square. | definition |
| Square of side n | n rows of n tiles: n × n tiles, written n². | definition |
| L (gnomon) | The tiles added to a square of side n − 1 to make a square of side n: one new row of n − 1, one new column of n − 1, and their shared corner. | definition |

## Causal chain

```text
an (n−1)×(n−1) square + one L of (n−1) + (n−1) + 1 = 2n − 1 cells → an n×n square
the first L is 1 tile, and each L is 2 bigger than the last (one more in its row and in its column)
→ the Ls are 1, 3, 5, …: the odd numbers in order → n of them make an n×n square → the first n odd numbers make n²
```

## Quantities

| n | n-th odd number | Sum of first n odd numbers |
|---|---|---|
| 1 | 1 | 1 |
| 2 | 3 | 4 |
| 3 | 5 | 9 |
| 4 | 7 | 16 |
| 5 | 9 | 25 |
| 10 | 19 | 100 |

Algebra (mathematical consequence): n² − (n − 1)² = 2n − 1.

## Why this form

| Step | Simplest alternative | Why the step is needed |
|---|---|---|
| Use a picture of tiles | check more examples | Examples show a pattern only. n = 1 … 5 work, but no number of checks covers every n. The tile step works for any size. |
| Grow the square by an L | add whole rows | A square of side n − 1 needs a row and a column, and they share one corner tile: n − 1 + n − 1 + 1, not 2n. |

Why L shapes: a square number counts the tiles in a square. So the natural question is how many tiles make a square one size bigger. The answer is an L.

## Concrete cases

| Claim | Holds here | Breaks here, without its assumption |
|---|---|---|
| The first n odd numbers add up to n × n. | n = 5: 1 + 3 + 5 + 7 + 9 = 25 = 5 × 5. n = 10: 1 + 3 + … + 19 = 100. | Start at 3, not 1: 3 + 5 = 8, not a square. Without the first tile, the Ls have no square to grow. |
| An L has 2n − 1 tiles. | From 4 × 4 to 5 × 5: 4 + 4 + 1 = 9. | — |
| Each L is two bigger than the one before, so the Ls are the odd numbers in order. | Around 4 × 4: 4 + 4 + 1 = 9; around 5 × 5: 5 + 5 + 1 = 11. The tenth L is 1 + 9 × 2 = 19. | — |

## Terms

- **Tile:** one small unit square. "Square" never means a tile.
- **Square of side n:** n rows of n tiles.
- **n:** the count of odd numbers added. It is also the number of Ls and the side of the square: one number, said aloud. Introduced with an instance: for 1 + 3 + 5, n is 3.
- **Side:** a square with 3 rows of 3 tiles has side 3 ("3 by 3").
- **n²:** n × n.

## Scope

- **Out of scope:** proof by induction in symbols (the L step is the induction step, said in words); sums that do not start at 1.
- **Shown as a payoff:** the n-th odd number is 2n − 1, from (n − 1) + (n − 1) + 1.
- **Out of scope:** n² − (n − 1)² = 2n − 1 (the big square minus the old square is the L).

## Epistemic status

- **Mathematical fact:** the identity holds for every positive integer n (proof by induction, or by the picture).
- **Pattern vs proof:** checking n = 1…5 shows a pattern only. The L-shape argument proves it for every n, because it uses no particular n.

## Confusion points

- "Five examples prove it." → No. The proof is the L-shape step, which works for any n.

## Representation decision

- **Stage:** 4 (animated). **Reason:** the proof is a transformation. Each L wraps the previous square, and the viewer must see the square grow while keeping its identity.
