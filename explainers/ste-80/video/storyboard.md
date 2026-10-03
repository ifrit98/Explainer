# Storyboard: ste-80

> Derived from `../model.md`.

## 1. Learning objective

After the video, the viewer can apply three STE rules to a sentence and predict which words each rule removes.

## 2. Conceptual sequence

1. STE-80 is a writing style for technical text.
2. A typical manual sentence has words that do not help the reader.
3. Rule 1 replaces formal words. Length stays the same.
4. Rule 2 makes the instruction direct. Length drops.
5. Rule 3 uses a concrete verb. Length drops again.
6. Same instruction, less decoding work.

## 3. Scenes

| # | Question the scene answers | Visual transformation | Bookmarks |
|---|---|---|---|
| 1 | What is STE-80? | Title writes, then moves to the corner | — |
| 2 | What is the problem? | S0 appears; word meter grows to 16 | `count` |
| 3 | What does rule 1 do? | Rule tag 1 appears; formal words turn red; morph to S1 | `mark`, `swap` |
| 4 | What does rule 2 do? | Rule tag 2; frame words turn red; morph to S2; meter → 13 | `mark`, `swap` |
| 5 | What does rule 3 do? | Rule tag 3; state words turn red; morph to S3; meter → 9 | `mark`, `swap` |
| 6 | What changed overall? | S0 returns muted above S3 for comparison | `compare` |

## 4. Visual-object inventory

| Object | Role color | First scene | Persists through | Becomes |
|---|---|---|---|---|
| Title "STE-80" | ENTITY | 1 | 1–6 | corner label |
| Sentence words | TEXT | 2 | 2–6 | kept words move; others fade (BAD out, GOOD in) |
| "hydraulic reservoir" | TEXT | 2 | 2–6 | never changes — the anchor |
| Word meter (bar + number) | QUANTITY | 2 | 2–6 | 16 → 16 → 13 → 9 |
| Rule tags 1–3 | ENTITY / MUTED | 3, 4, 5 | to 6 | active tag in FOCUS, older tags MUTED |

## 5. Timing

Target length: about 50 s.

## 6. Rendering plan

- Engine: Manim CE + explainer_kit (Kokoro voice `af_heart`).
- Lexicon: STE-80 → "S T E eighty"; ASD-STE100 → "A S D, S T E one hundred".
- MathTex: no.
