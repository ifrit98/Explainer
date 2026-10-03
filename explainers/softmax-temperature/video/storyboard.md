# Storyboard: softmax-temperature

> Derived from `../model.md`. Every number on screen is computed from the model's logits.

## 1. Learning objective

After the video, the viewer can predict how the next-token distribution changes when T goes up or down, and explain why the ranking never changes.

## 2. Conceptual sequence

1. The model scores four candidates (logits).
2. Softmax turns logits into probabilities.
3. T divides every logit before softmax.
4. Low T spreads the scaled logits apart → sharper distribution.
5. High T pulls them together → flatter distribution.
6. Why: the distance between two scaled logits sets their probability ratio.
7. Limits: T → 0 is greedy; T → ∞ is uniform; the order never changes.

## 3. Scenes

| # | Question the scene answers | Visual transformation | Bookmarks |
|---|---|---|---|
| 1 | What is the task? | Context sentence and four token names appear | — |
| 2 | What does the model output? | Number line draws; dots land at the logits | `line` |
| 3 | What is softmax? | Bars grow to p at T = 1 | `bars` |
| 4 | What does a low T do? | T 1 → 0.5: dots spread, cat bar rises to 0.84 | `cold` |
| 5 | What does a high T do? | T 0.5 → 2: dots gather, bars flatten | `hot` |
| 6 | Why? | Gap marker between dog and cat dots with live ratio; T sweeps 2 → 0.5 → 4 | `gap`, `move` |
| 7 | What are the limits? | T → 0.25 (near greedy), then T → 10 (near uniform) | `uni` |
| 8 | What never changes? | T → 1; cat and owl bars flash; formula replaces context | `formula` |

## 4. Visual-object inventory

| Object | Color | First scene | Persists through | Driven by |
|---|---|---|---|---|
| Token identity (cat, dog, fox, owl) | blue, gold, teal, maroon | 1 | 1–8 | fixed: color follows the token |
| Number line "z / T" | RELATION | 2 | 2–8 | — |
| Dots (one per token) | token color | 2 | 2–8 | position = z / T |
| Bars (one per token) | token color | 3 | 3–8 | height = softmax(z / T) |
| T readout | TEXT | 3 | 3–8 | T |
| Gap marker + ratio | FOCUS | 6 | 6–7 | exp((2 − 1) / T) |

## 5. Timing

Target length: about 75 s.

## 6. Rendering plan

- Manim CE + explainer_kit, Kokoro `af_heart`.
- One `ValueTracker` for T drives every moving object (`always_redraw` / updaters).
- No LaTeX: tick labels and numbers use `label()`; NumberLine has `include_numbers=False`.
