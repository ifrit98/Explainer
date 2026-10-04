# Softmax temperature

> Also as a [diagram](diagram.md), an [interactive page](https://ifrit98.github.io/Explainer/explainers/softmax-temperature/), and a [video](video/out.mp4).

**Temperature T controls how spread out a model's next-token probabilities are.** A low T makes the top token almost certain. A high T makes the candidates almost equal. For any T above 0, T never changes which token is most likely.

This is why the same prompt gives the same answer at a low `temperature` and varied answers at a high one.

## How it works

<!-- claim: mechanism-step -->
A language model gives each candidate token a raw score, the *logit*. For the context "The ___ sat on the mat." the logits are cat 2.0, dog 1.0, fox 0.5, owl −1.0. The sampler (the code that picks the next token) then does these steps:

1. Divide each logit by T.
2. Apply the exponential function exp (e^x, with e ≈ 2.718) to each result.
3. Divide each result by the sum of all results. The values are now probabilities.
4. Pick one token at random with these probabilities. A random pick lets the output vary; T sets how much.

Steps 1 to 3 are softmax with temperature. For token i with logit zᵢ, summing over all tokens j:

```text
pᵢ = exp(zᵢ / T) / Σⱼ exp(zⱼ / T)
```

Worked at T = 2:

| Step | cat | dog | fox | owl |
|---|---|---|---|---|
| z / T | 1.0 | 0.5 | 0.25 | −0.5 |
| exp | 2.718 | 1.649 | 1.284 | 0.607 |
| ÷ sum (6.258) | 0.434 | 0.263 | 0.205 | 0.097 |

The same steps at three temperatures:

| T | cat | dog | fox | owl | cat : dog |
|---|---|---|---|---|---|
| 0.5 | 0.842 | 0.114 | 0.042 | 0.002 | 7.39 |
| 1.0 | 0.609 | 0.224 | 0.136 | 0.030 | 2.72 |
| 2.0 | 0.434 | 0.263 | 0.205 | 0.097 | 1.65 |

## Why exp

<!-- claim: why-exp -->
Exp does three jobs at once:

1. It turns every logit, positive or negative, into a positive weight.
2. It keeps the order: a larger logit always gives a larger weight.
3. It turns a difference of logits into a ratio of weights: e^(a−b) = e^a / e^b. The next section uses this.

The simpler alternatives fail. Divide each logit by the sum of the logits: 2.0 + 1.0 + 0.5 − 1.0 = 2.5, so owl gets −1.0 / 2.5 = −0.4, a negative probability. T also cancels: (z/T) / Σ(z/T) = z / Σz. Square the logits instead: the result is 0.64, 0.16, 0.04, 0.16. Owl now ties dog and beats fox, so the order breaks, and T cancels again.

## Why divide by T

<!-- claim: why-divide-t -->
The ratio of two probabilities depends only on the gap between their logits, divided by T:

```text
pᵢ / pⱼ = exp((zᵢ − zⱼ) / T)
```

Both probabilities have the same denominator, so it cancels in the ratio. T does not change the gap between two logits. It changes the *scaled gap*, the gap divided by T. A small T makes the scaled gap large, so the ratio becomes very large. A large T makes the scaled gap small, so the ratio goes toward 1. In the table, cat : dog is 2.72 at T = 1 and 2.72^(1/2) = 1.65 at T = 2.

Adding T to every logit would do nothing, because a shift cancels in every ratio.

## What changes the result, and what does not

<!-- claim: guarantee-shift -->
- **Adding** the same number to every logit changes nothing. Add 10: the logits 12, 11, 10.5, 9 give 0.609, 0.224, 0.136, 0.030 at T = 1, the same as before.
- **Multiplying** every logit changes the result. Multiply by 2: the logits 4, 2, 1, −2 give 0.842, 0.114, 0.042, 0.002, the T = 0.5 row. Doubling the logits doubles every gap, the same as halving T.

<!-- claim: guarantee-order -->
- **The order never changes for T above 0.** Dividing by a positive T keeps the order of the logits, and exp keeps the order of its inputs. Cat is first and owl is last in every row of the table. A negative T would reverse it: at T = −1 the scaled logits are −2, −1, −0.5, 1, and owl becomes the most likely token (0.71). APIs do not allow a negative T.

## How spread out: entropy

<!-- claim: why-entropy -->
*Entropy* measures the spread: how much you do not know before the draw.

- A token with probability p has a *surprise* of −log₂ p bits. One bit is one fair yes/no question. At T = 1, cat surprises you by 0.71 bits; owl by 5.04 bits.
- Entropy is the average surprise of one draw: H = −Σ p log₂ p.
- 2^H is the number of equally likely tokens with the same entropy. n equally likely tokens each surprise you by log₂ n bits, so 2^H = n.

| T | entropy | like a choice between |
|---|---|---|
| 0.5 | 0.78 bits | 1.71 tokens |
| 1.0 | 1.46 bits | 2.76 tokens |
| 2.0 | 1.82 bits | 3.54 tokens |

Why a log, and not a count of the possible tokens? At T = 0.25 all four tokens are still possible, so a count says 4. But cat wins 98% of draws. Entropy says 0.15 bits, about 1.11 tokens, which matches what you see.

## Limits

- At T = 0 the division is undefined. APIs use greedy decoding instead: they always pick the top token.
- As T increases without limit, all probabilities go to the same value (0.25 for four tokens).
- For finite T, no probability is exactly 0. Owl at T = 0.25 is 6.0 × 10⁻⁶.
- "Temperature controls creativity" is a loose description. Temperature controls spread only. It does not add knowledge.

## In short

Temperature divides every logit before softmax. That scales every gap between logits, so it scales every ratio between probabilities: a low T lets the top token dominate, a high T makes the tokens nearly equal. Dividing by a positive number and exp both keep the order, so the most likely token stays the same.

## Not covered here

- Which T to choose for a task. API defaults are usually near 1; extraction and code often use 0 to 0.3.
- Top-k and top-p filtering, and their order relative to temperature. See your provider's sampling documentation.
- Why T = 0 can still vary in practice (ties, nondeterministic GPU arithmetic).
