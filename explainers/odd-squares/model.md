# Semantic model: sums of odd numbers

## Central question

Why does 1 + 3 + 5 + … + (2n − 1) always equal n²?

## Audience and prior knowledge

Readers who know what a square number is. No algebra beyond expanding (n − 1)².

## Entities

| Entity | Definition | Status |
|---|---|---|
| Odd number | The k-th odd number is 2k − 1: 1, 3, 5, 7, 9, … | definition |
| Partial sum | The sum of the first n odd numbers. | definition |
| Square n² | An n × n grid of unit squares. | definition |
| Gnomon (L shape) | The cells added to an (n − 1) × (n − 1) square to make an n × n square: one new row, one new column, and their shared corner. | definition |

## Causal chain

```text
an (n−1)×(n−1) square + one L of (n−1) + (n−1) + 1 = 2n − 1 cells → an n×n square
so each odd number extends the square by one size → the first n odd numbers make n²
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

## Epistemic status

- **Mathematical fact:** the identity holds for every positive integer n (proof by induction, or by the picture).
- **Pattern vs proof:** checking n = 1…5 shows a pattern only. The L-shape argument proves it for every n, because it uses no particular n.

## Confusion points

- "Five examples prove it." → No. The proof is the L-shape step, which works for any n.

## Representation decision

- **Stage:** 4 (animated). **Reason:** the proof is a transformation. Each L wraps the previous square, and the viewer must see the square grow while keeping its identity.
