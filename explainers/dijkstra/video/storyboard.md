# Storyboard: dijkstra

> Derived from `../model.md`. The scene replays `run` from `../model.yaml`; it computes nothing itself.

## 1. Learning objective

After the video, the viewer can run Dijkstra's algorithm by hand on a small graph, say which node is settled next and why, and name the assumption it needs.

## 2. Conceptual sequence

1. The task and the non-negative length rule.
2. Start: A at 0, others ∞; the two-step loop.
3. Settle A, C, B, D (B improves 4 → 3; D improves 10 → 8).
4. Predict: which node is settled next?
5. Settle E (F improves 14 → 13), then F.
6. Why a settled distance is final.
7. The shortest-path tree; the path to F.

## 3. Scenes

| # | Question the scene answers | Visual transformation | Bookmarks |
|---|---|---|---|
| 1 | What is the task? | Graph builds; edge lengths appear | `rule` |
| 2 | How does it start, and what repeats? | Distance tags appear; rule card | `loop` |
| 3 | What does one step do? | Ring on the settled node; edges flash; tags change; best edge stays highlighted | `r0`–`r2` per step |
| 4 | Which node is next? | Predict pause | — |
| 5 | Why is a settled distance final? | Rule card flashes | — |
| 6 | What is the result? | Non-tree edges mute; tree edges turn green; the path to F flashes | `path` |

## 4. Visual-object inventory

| Object | Color | Persists through |
|---|---|---|
| Nodes | ENTITY; settled: GOOD fill | all |
| Edges | RELATION; current best: FOCUS; tree: GOOD | all |
| Distance tags | QUANTITY, outside the graph | all |

## 5. Rendering plan

Manim CE + explainer_kit, Kokoro `af_heart`, no LaTeX. One predict pause before E is settled.

## 6. Open (from the blind test)

Show the finality argument with a concrete competing path, and one negative-edge counterexample.
