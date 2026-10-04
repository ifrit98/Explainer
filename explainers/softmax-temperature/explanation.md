# Softmax temperature — Stage 1: controlled prose

> Rendered from [`model.md`](model.md) in STE-80. Other renderings: [diagram](diagram.md) · [interactive](https://ifrit98.github.io/Explainer/explainers/softmax-temperature/) · [video](video/out.mp4).

**Temperature T controls how spread out a model's next-token probabilities are.** A low T makes the top token almost certain. A high T makes the candidates almost equal. For any T above 0, T never changes which token is ranked first.

## How it works

<!-- claim: mechanism-step -->
A language model gives each candidate token a raw score. This score is the *logit*. To turn logits into probabilities, the sampler does these steps:

1. Divide each logit by T.
2. Apply the exponential function exp (e^x, with e ≈ 2.718) to each result.
3. Divide each result by the sum of all results. Now the values are probabilities that sum to 1.
4. Pick one token at random, with these probabilities. A random pick, not always the top token, lets the output vary; T sets how much.

Steps 2 and 3 together are the *softmax* function:

```text
pᵢ = exp(zᵢ / T) / Σⱼ exp(zⱼ / T)
```

Worked at T = 2, with the logits cat 2.0, dog 1.0, fox 0.5, owl −1.0:

| Step | cat | dog | fox | owl |
|---|---|---|---|---|
| z / T | 1.0 | 0.5 | 0.25 | −0.5 |
| exp | 2.718 | 1.649 | 1.284 | 0.607 |
| ÷ sum (6.258) | 0.434 | 0.263 | 0.205 | 0.097 |

## Why exp

<!-- claim: why-exp -->
Exp does three jobs at once:

1. It turns every logit, positive or negative, into a positive weight.
2. It keeps the order: a larger logit always gives a larger weight.
3. It turns a difference of logits into a ratio of weights: e^(a−b) = e^a / e^b.

The simpler alternatives fail. Divide each logit by the sum of the logits: 2.0 + 1.0 + 0.5 − 1.0 = 2.5, so owl gets −1.0 / 2.5 = −0.4. A probability cannot be negative. Temperature also stops working: (z/T) / Σ(z/T) = z / Σz, so T cancels. Square the logits instead, then normalize: the result is 0.64, 0.16, 0.04, 0.16. Owl now ties dog and beats fox, so the order breaks. T cancels here too: (z/T)² / Σ(z/T)² = z² / Σz².

The name comes from physics. The Boltzmann distribution is p ∝ exp(−E / kT). A logit plays the role of −E, and T is the temperature.

## Why divide by T

<!-- claim: why-divide-t -->
The ratio of two probabilities depends only on the gap between their logits, divided by T:

```text
pᵢ / pⱼ = exp((zᵢ − zⱼ) / T)
```

This follows from the softmax formula. Both probabilities have the same denominator Σⱼ exp(zⱼ / T), so it cancels in the ratio. What remains is exp(zᵢ / T) / exp(zⱼ / T), which equals exp((zᵢ − zⱼ) / T).

T does not change the gap between two logits. It changes the *scaled gap*, the gap divided by T. A small T makes the scaled gap large, so the ratio becomes very large. A large T makes the scaled gap small, so the ratio goes toward 1. Put another way, every ratio becomes its T = 1 value raised to the power 1/T, because exp(gap / T) = exp(gap)^(1/T). Check it at T = 2: (0.609 / 0.224)^(1/2) = 1.65, the cat : dog ratio at T = 2 in the Example section below.

Adding T to every logit would not work. Adding one number to every logit changes nothing, as the next section shows.

## What changes the result, and what does not

<!-- claim: guarantee-shift -->
- **Adding** the same number to every logit changes nothing. Add 10: the logits 12, 11, 10.5, 9 still give 0.609, 0.224, 0.136, 0.030 at T = 1. The constant cancels in every ratio.
- **Multiplying** every logit changes the result. Multiply by 2: the logits 4, 2, 1, −2 give 0.842, 0.114, 0.042, 0.002. That is exactly the T = 0.5 row of the table in the Example section below, because doubling the logits doubles every gap, the same as halving T.

<!-- claim: guarantee-order -->
- **The order never changes for T above 0.** Dividing by a positive T keeps the order of the logits, and exp keeps the order of its inputs. Cat is first and owl is last in every row of the table below. A negative T would reverse it: at T = −1 the scaled logits are −2, −1, −0.5, 1, and owl becomes the most likely token (0.71). APIs do not allow a negative T.

## Example

The context is "The ___ sat on the mat." The model gives four logits: cat 2.0, dog 1.0, fox 0.5, owl −1.0.

| T | cat | dog | fox | owl | cat : dog | entropy |
|---|---|---|---|---|---|---|
| 0.5 | 0.842 | 0.114 | 0.042 | 0.002 | 7.39 | 0.78 bits (≈ 1.71 choices) |
| 1.0 | 0.609 | 0.224 | 0.136 | 0.030 | 2.72 | 1.46 bits (≈ 2.76 choices) |
| 2.0 | 0.434 | 0.263 | 0.205 | 0.097 | 1.65 | 1.82 bits (≈ 3.54 choices) |

<!-- claim: why-entropy -->
*Entropy* measures the spread: how much you do not know before the draw. It is the average *surprise*, in bits.

- A token with probability p has a surprise of −log₂ p bits. One bit is one fair yes/no question. At T = 1, cat surprises you by 0.71 bits; owl surprises you by 5.04 bits.
- Entropy is the average surprise of one draw: H = −Σ p log₂ p. At T = 1 it is 1.46 bits.
- 2^H is the number of equally likely tokens with the same entropy: n equally likely tokens each surprise you by log₂ n bits, so their entropy is log₂ n, and 2^H = n. 1.46 bits is like a choice between 2^1.46 ≈ 2.76 equally likely tokens. 0 bits means certain; 2 bits means four equally likely tokens.

Why a log, and not a count of the possible tokens? At T = 0.25 all four tokens are still possible, so a count says 4. But cat wins 98% of draws. Entropy says 0.15 bits, about 1.11 choices, which matches what you see. At T = 10 the count is still 4, and entropy says 1.99 bits, about 3.98 choices. The log also makes surprises add when probabilities multiply: two fair coins have p = 1/4, and 2 bits = 1 + 1.

## Limits

- At T = 0 the division is undefined. APIs use greedy decoding instead: they always pick the top token.
- As T increases without limit, all probabilities go to the same value (0.25 for four tokens).
- For finite T, no probability is exactly 0. Owl at T = 0.25 is 6.0 × 10⁻⁶; tables show it as 0.000.
- "Temperature controls creativity" is a loose description. Temperature controls spread only. It does not add knowledge.

## Not covered here

- Which T to choose for a task. API defaults are usually near 1; extraction and code often use 0 to 0.3.
- Top-k and top-p filtering, and their order relative to temperature. See your provider's sampling documentation.
- Why T = 0 can still vary in practice (ties, nondeterministic GPU arithmetic).
