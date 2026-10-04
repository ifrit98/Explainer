# Storyboard: dijkstra

> Derived from `../model.md`. The scene replays `run` from `../model.yaml`; it computes nothing itself.

## 1. Learning objective

After the video, the viewer can run Dijkstra's algorithm by hand on a small graph, say which node is settled next and why, and name the assumption it needs.

## 2. Conceptual sequence

1. The task and the non-negative length rule.
2. Terms: an *estimate* is the shortest length found so far; a settled estimate is the final *distance*. The two-step loop; relax, defined and shown as a test.
3. Settle A, then C (B improves 4 → 3). Why the smallest estimate settles first: B at 4 would be wrong.
4. Settle B. Why B's estimate is final, one step per line: the unsettled estimates (D 10, E 12, F ∞); any other path leaves the settled region through them and costs at least 10; so B is final. Pause.
5. Settle D (D improves 10 → 8). Predict: which node is settled next?
6. Settle E (F improves 14 → 13), then F.
7. Read the path back through the predecessors: A, C, B, D, E, F, length 13.
8. Chapter 2: one negative edge (A→B 2, A→C 3, C→B −2). The algorithm answers 2; the true distance is 1.

## 3. Scenes

| # | Question the scene answers | Visual transformation | Bookmarks |
|---|---|---|---|
| 1 | What is the task? | Graph builds; edge lengths appear | `rule` |
| 2 | How does it start, and what repeats? | Estimate tags appear; rule card; relax test and "keep it" line | `loop`, `relax`, `keep` |
| 3 | What does one step do? | Ring on the settled node; edges flash; tags change; best edge stays highlighted | `r0`–`r2` per step |
| 4 | Why the smallest estimate? | A–B flashes red; A–C–B flashes green | `w`, `via` |
| 5 | Why is B final? | Settled region; D, E, F tags pulse one by one; exit edges flash; "any other path to B costs ≥ 10 > 3"; B pulses | `d`, `e`, `f`, `leave`, `grow`, `final` |
| 6 | Which node is next? | Predict pause | — |
| 7 | What is the result? | Non-tree edges mute; tree edges turn green; nodes pulse back from F; the path flashes | `back`, `path` |
| 8 | What breaks it? | Three-node directed graph; B settles at 2; C→B gives 1 too late; "true: 1" | `g`, `c`, `late`, `wrong` |

Each claim line is followed by a pause of at least 1 s (`explainer render` reports pace issues).

## 4. Visual-object inventory

| Object | Color | Persists through |
|---|---|---|
| Nodes | ENTITY; settled: GOOD fill | all |
| Edges | RELATION; current best: FOCUS; tree: GOOD | all |
| Estimate tags | QUANTITY, outside the graph | all |
| Settled region | GOOD, dashed | scene 5 |

## 5. Rendering plan

Manim CE + explainer_kit, Kokoro `af_heart`, no LaTeX. One predict pause before E is settled. Narration uses "estimate" for the tentative value and "distance" only for the final one (`terms` in `model.yaml`).
