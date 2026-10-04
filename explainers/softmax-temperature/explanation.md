# Softmax temperature — Stage 1: controlled prose

> Rendered from [`model.md`](model.md) in STE-80. Other renderings: [diagram](diagram.md) · [interactive](index.html) · [video](video/out.mp4).

**Temperature T controls how spread out a model's next-token probabilities are.** A low T makes the top token almost certain. A high T makes the candidates almost equal. T never changes which token is ranked first.

## How it works

A language model gives each candidate token a raw score. This score is the *logit*. To turn logits into probabilities, the sampler does these steps:

1. Divide each logit by T.
2. Apply the exponential function (exp) to each result.
3. Divide each result by the sum of all results. Now the values are probabilities that sum to 1.
4. Pick one token at random, with these probabilities.

Steps 2 and 3 together are the *softmax* function:

```text
pᵢ = exp(zᵢ / T) / Σⱼ exp(zⱼ / T)
```

## Why it works

The ratio of two probabilities depends only on the gap between their logits, divided by T:

```text
pᵢ / pⱼ = exp((zᵢ − zⱼ) / T)
```

This follows from the softmax formula. Both probabilities have the same denominator Σⱼ exp(zⱼ / T), so it cancels in the ratio. What remains is exp(zᵢ / T) / exp(zⱼ / T), which equals exp((zᵢ − zⱼ) / T).

A small T makes the gap large, so the ratio becomes very large. A large T makes the gap small, so the ratio goes toward 1.

## Example

The context is "The ___ sat on the mat." The model gives four logits: cat 2.0, dog 1.0, fox 0.5, owl −1.0.

| T | cat | dog | fox | owl | cat : dog |
|---|---|---|---|---|---|
| 0.5 | 0.842 | 0.114 | 0.042 | 0.002 | 7.39 |
| 1.0 | 0.609 | 0.224 | 0.136 | 0.030 | 2.72 |
| 2.0 | 0.434 | 0.263 | 0.205 | 0.097 | 1.65 |

At every T, cat is first and owl is last. Only the spread changes.

## Limits

- At T = 0 the division is undefined. APIs use greedy decoding instead: they always pick the top token.
- As T increases without limit, all probabilities go to the same value (0.25 for four tokens).
- Many APIs also apply top-k or top-p filtering after temperature. This explanation does not include them.
- "Temperature controls creativity" is a loose description. Temperature controls spread only. It does not add knowledge.
