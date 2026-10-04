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

## Why this form

| Operation | Simplest alternative | What the alternative breaks |
|---|---|---|
| exp before normalizing | divide each logit by the sum of the logits | Logits 2.0, 1.0, 0.5, −1.0 sum to 2.5, so owl gets −1.0 / 2.5 = −0.4: a negative probability. With z/T in place of z, T cancels: (z/T) / Σ(z/T) = z / Σz, so temperature would do nothing. |
| exp before normalizing | square each logit, then normalize | z² / Σz² gives 0.64, 0.16, 0.04, 0.16: owl (−1)² ties dog and beats fox. The order of the tokens breaks. T cancels here too: (z/T)² / Σ(z/T)² = z² / Σz². |
| divide the logits by T | add T to every logit | Adding one number to every logit changes nothing (shift invariance), so T would have no effect. |
| entropy H = −Σ p log₂ p | count the tokens with p > 0 | At T = 0.25 all four tokens have p > 0 (owl 6.0 × 10⁻⁶), so the count says 4, but cat wins 98% of draws. Entropy gives 0.15 bits ≈ 1.11 choices. At T = 10 the count is still 4; entropy gives 1.99 bits ≈ 3.98 choices. |

Why the log in entropy: −log₂ p is the surprise of one token, in bits; one bit is one fair yes/no question. The log makes surprises add when probabilities multiply (two fair coins: p = 1/4, 2 bits = 1 + 1). Entropy is the average surprise, and 2^H is the number of equally likely tokens with the same average. At T = 1: cat 0.71 bits, dog 2.16, fox 2.88, owl 5.04; the average is 1.46 bits ≈ 2.76 equally likely tokens.

Why exp works: it turns every logit, positive or negative, into a positive weight; it keeps the order; and it turns a difference of logits into a ratio of weights, e^(a−b) = e^a / e^b. That ratio property is the whole temperature law: pᵢ / pⱼ = exp((zᵢ − zⱼ) / T). Dividing by T scales each gap by 1/T, so every ratio becomes its T = 1 value raised to the power 1/T: p(T) ∝ p(1)^(1/T). Example: (0.609 / 0.224)^(1/2) = 1.65, the cat : dog ratio at T = 2.

Origin of the name: physics writes the Boltzmann distribution as p ∝ exp(−E / kT). A logit plays the role of −E, and T is the temperature.

## Concrete cases

| Claim | Holds here | Breaks here, without its assumption |
|---|---|---|
| For T > 0 the order of the tokens never changes. | cat > dog > fox > owl in every row of the table. | T = −1: z/T = −2, −1, −0.5, 1, and owl becomes the most likely token (0.71). |
| Adding the same number to every logit changes nothing. | +10: logits 12, 11, 10.5, 9 still give 0.609, 0.224, 0.136, 0.030 at T = 1. | Multiplying is different: ×2 gives logits 4, 2, 1, −2 and the T = 0.5 row, 0.842, 0.114, 0.042, 0.002. |
| One decoding step (mechanism), worked at T = 2. | z/T = 1.0, 0.5, 0.25, −0.5 → exp = 2.718, 1.649, 1.284, 0.607 → sum 6.258 → p = 0.434, 0.263, 0.205, 0.097. | — |
| Entropy measures spread as average surprise. | 1.46 bits at T = 1 equals the spread of 2^1.46 = 2.76 equally likely choices. | A count of possible tokens says 4 at T = 0.25, where cat wins 98% of draws; entropy says 1.11 choices. |

Probabilities are never exactly 0 for finite T: owl at T = 0.25 is 6.0 × 10⁻⁶, shown as 0.000 after rounding.

## Terms

- **Token:** one unit of text the model can output (a word or part of a word).
- **Logit:** the raw score the model gives one candidate token.
- **exp:** the exponential function e^x, with e ≈ 2.718.
- **Softmax:** exp of each scaled logit, divided by the sum of those values.
- **Greedy decoding:** always pick the most likely token.
- **Surprise (bits):** −log₂ p for one token. One bit is one fair yes/no question.
- **Entropy (bits):** H = −Σ p log₂ p, the average surprise of one draw. 0 bits = certain; 2 bits = four equally likely tokens.

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

## Scope

- **Out of scope:** which T to choose for a task — API defaults are usually near 1; extraction and code often use 0 to 0.3.
- **Out of scope:** top-k and top-p filtering and their order relative to temperature — see the provider's sampling documentation.
- **Out of scope:** why T = 0 can still vary in practice (ties, nondeterministic GPU arithmetic).

## Representation decision

- **Normal routing:** Stage 3 (interactive). The behavior depends on one continuous parameter, and the reader learns most by moving it.
- **This folder:** a compiler demo. The same model is rendered at all four stages to show that the renderings agree.
- **Levels:** L1 what T does (flatter vs sharper) / L2 how (division before softmax) / L3 why (ratios depend on gaps divided by T) / L4 implementation (T = 0 as greedy, top-k/top-p order).
