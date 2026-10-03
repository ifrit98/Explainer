# Semantic model: softmax temperature

> Source of truth. `explanation.md`, `diagram.md`, `index.html`, and `video/` all derive from this file.
> Every number below comes from the worked example. Renderings must use these numbers.

## Central question

What does the temperature T do to a language model's next-token probabilities?

## Audience and prior knowledge

Developers who use LLM APIs and see a `temperature` parameter. They know what a probability is. They do not know the softmax formula.

## Entities

| Entity | Definition (one sentence) | Status |
|---|---|---|
| Logit z | The raw score that the model gives to one candidate token. Any real number. | fact |
| Temperature T | A positive number that divides every logit before softmax. | fact |
| Scaled logit z/T | The logit after division by T. | fact |
| Softmax | The function that turns scaled logits into probabilities: pᵢ = exp(zᵢ/T) / Σⱼ exp(zⱼ/T). | fact |
| Probability p | The chance that the sampler picks a token. All p are positive and sum to 1. | fact |
| Sampler | The step that picks one token at random, with chance p. | fact |
| Entropy H | The spread of the distribution, in bits. 0 = certain; log₂(n) = uniform. | fact |

## Relationships

| From | Relationship | To |
|---|---|---|
| T | divides | every logit z |
| scaled logits | go into | softmax |
| softmax | produces | probabilities p |
| probabilities p | drive | the sampler |
| T | controls | the gaps between scaled logits |
| gaps between scaled logits | set | the ratios between probabilities |

## Causal chain

```text
larger T → smaller gaps between scaled logits → smaller probability ratios → flatter distribution → higher entropy → more varied samples
smaller T → larger gaps → larger ratios → sharper distribution → lower entropy → more repeatable samples
```

Key law (mathematical consequence): pᵢ / pⱼ = exp((zᵢ − zⱼ) / T). Only the gap between logits matters, and T divides the gap.

## Temporal sequence (one decoding step)

1. The model outputs one logit per candidate token.
2. Divide each logit by T.
3. Apply exp to each scaled logit.
4. Divide each result by the sum. The results are the probabilities.
5. The sampler picks one token.

## Quantities — worked example

Context: "The ___ sat on the mat." Four candidate tokens. Logits: cat 2.0, dog 1.0, fox 0.5, owl −1.0.

| T | cat | dog | fox | owl | Entropy H | cat : dog ratio |
|---|---|---|---|---|---|---|
| 0.25 | 0.980 | 0.018 | 0.002 | 0.000 | 0.15 bits | 54.6 |
| 0.5 | 0.842 | 0.114 | 0.042 | 0.002 | 0.78 bits | 7.39 |
| 1.0 | 0.609 | 0.224 | 0.136 | 0.030 | 1.46 bits | 2.72 |
| 2.0 | 0.434 | 0.263 | 0.205 | 0.097 | 1.82 bits | 1.65 |
| 4.0 | 0.340 | 0.265 | 0.234 | 0.161 | 1.95 bits | 1.28 |

Maximum entropy for 4 tokens: log₂ 4 = 2 bits (all p = 0.25).

## Alternative states

| State | What happens | Why |
|---|---|---|
| T → 0 | All probability goes to the top token (greedy decoding). | Gaps become infinite. |
| T = 1 | Plain softmax. The model's own distribution. | Division by 1 changes nothing. |
| T → ∞ | Every token gets the same probability. | Gaps go to 0. |

## Epistemic status

- **Mathematical consequence:** the ranking of tokens never changes with T, because division by a positive T keeps the order of the logits.
- **Mathematical consequence:** adding the same constant to every logit changes nothing (shift invariance).
- **Implementation fact:** APIs treat T = 0 as greedy decoding, because division by 0 is undefined.
- **Simplification:** real vocabularies have about 10⁴–10⁵ tokens, not 4. The behavior is the same.
- **Simplification:** this model ignores top-k and top-p filtering, which many APIs apply after temperature.
- **Disputed / loose:** "temperature controls creativity." It controls spread only. A flatter distribution gives more varied output. It does not add knowledge or ideas.

## Confusion points

- "High T makes the model pick a different best token." → No. The ranking stays the same. Only the spread changes.
- "T = 0 means random." → No. T = 0 means greedy: always the top token.
- "Temperature changes the logits." → It changes only the scaled logits for this step. The model's output does not change.

## Representation decision

- **Normal routing:** Stage 3 (interactive). The behavior depends on one continuous parameter, and the reader learns most by moving it.
- **This folder:** a compiler demo. The same model is rendered at all four stages to show that the renderings agree.
- **Levels:** L1 what T does (flatter vs sharper) / L2 how (division before softmax) / L3 why (ratios depend on gaps divided by T) / L4 implementation (T = 0 as greedy, top-k/top-p order).
