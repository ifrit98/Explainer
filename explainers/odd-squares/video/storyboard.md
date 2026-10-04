# Storyboard: odd-squares

> The visual plan for the beats in `../narrative.md`. The scene comments carry the beat numbers.

## 1. Learning objective

After the video, the viewer can say why the first n odd numbers add up to n × n for every n (each odd number is an L that grows the square by one, and each L is two bigger than the last), and compute the sum of the first ten odd numbers without adding them.

## 2. Scenes (beats from the narrative)

| Beat | Visual transformation | Bookmarks |
|---|---|---|
| 1 hook | Sum rows appear one at a time, each odd number in its own color | `r1`–`r5` |
| 2 notice, name | "= n × n" beside each sum; three odd numbers light up with 3 × 3; the rule card | `s1`–`s5`, `count`, `rule` |
| 3 objection | "?" after the rule card | `q` |
| 4 approach | A grey 3 by 3 square with "side 3"; then one tile | `nine`, `ask`, `t` |
| 5 name the L | Three teal tiles go around the first; the sum 4 and the 3 light up | `l2`, `color` |
| 6 build | Ls of 5, 7, 9; each term lights up | `g3`–`g5` |
| 7 mechanism | Old 4 by 4 outlined; braces 4, 4 and corner 1; "around 5 by 5: 5 + 5 + 1 = 11"; "each L is two bigger"; all terms light up in order | `old`, `parts`, `col`, `corner`, `next`, `two`, `odd` |
| 8 close | Each L lights up with its term; the rule card becomes 1 + 3 + 5 + ⋯ = n² (n odd numbers) | `build`, `done`, `sq`, `dots` |
| 9 test | Predict pause | — |
| 10 apply | Square halves; Ls 6–10 in five more colors; 1 + 3 + ⋯ + 19 = 100 | `tenth`, `ten` |
| 11 objection | "3 + 5 = 8: not a square"; the first tile pulses | `s3`, `need` |
| 12 payoff | The 5 by 5 again; "n = 5"; brace labels 4 → n − 1; (n − 1) + (n − 1) + 1 = 2n − 1 | `n`, `sym`, `law` |
| 13 recap | The rule card pulses | — |

## 3. Visual-object inventory

| Object | Color | Persists through |
|---|---|---|
| Sum rows | each odd number in its L's color | 1–13 |
| Ls 1–10 | one color per odd number | 4–11, 12 (1–5) |
| Rule card | ENTITY; "?" in BAD until beat 8 | 2–13 |
| Braces and labels | RELATION; numbers TEXT; corner FOCUS | 7, 12 |

## 4. Rendering plan

Manim CE + explainer_kit, Kokoro `af_heart`, LaTeX for the rule and the payoff formula. One predict pause. A claim pause of at least 1 s after each claim line.
