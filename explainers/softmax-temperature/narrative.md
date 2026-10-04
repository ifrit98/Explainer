# Narrative: softmax-temperature

> Pass 3. Written after the renderings (v0.6.0 backfill); the prose, page, and video follow these beats.

## 1. Reader before and after

- **Before:** Developers who use LLM APIs and see a `temperature` parameter. They know what a probability is. They do not know the softmax formula.
- **After:** "Temperature divides every logit before softmax, so it scales every gap and every probability ratio: a low T lets the top token dominate, a high T evens the tokens out, and the most likely token never changes."

## 2. Question and motive

- **Question:** what does `temperature` do to the next-token probabilities? Answer first, in words.
- **Why care:** it is why one prompt gives the same answer at a low temperature and varied answers at a high one.
- **Why this approach:** follow four logits through the steps, at three temperatures, then ask why each step has its form.

## 3. Introduction ledger

| Reference | Means | Grounded by | Beat |
|---|---|---|---|
| logit, z | the model's raw score for a token | cat 2.0, dog 1.0, fox 0.5, owl −1.0 | 2 |
| T | temperature: every logit is divided by it | T = 2: z / T = 1.0, 0.5, 0.25, −0.5 | 2 |
| p, i, j | the probability of token i; j runs over all tokens in the sum | the formula under the steps | 2 |
| e | the base of exp, about 2.718 | step 2 | 2 |
| a, b | any two logits, in e^(a−b) = e^a / e^b | the "why exp" list | 3 |
| scaled gap | the gap between two logits divided by T | cat : dog 2.72 at T = 1, 1.65 at T = 2 | 4 |
| entropy, surprise, bits | the average surprise of one draw; −log₂ p | 1.46 bits ≈ 2.76 equally likely tokens | 6 |

## 4. Beats

| # | Kind | Reader's question | Bridge | Said | Reader now knows |
|---|---|---|---|---|---|
| 1 | answer | What does T do? | — | low T: top token near certain; high T: near equal; order never changes | the answer |
| 2 | mechanism | How are the probabilities made? | so | divide by T, exp, normalize, sample; worked at T = 2; the table at three T | the steps, in numbers |
| 3 | why | Why exp? | but why | positive, order kept, gaps become ratios; divide-by-sum gives owl −0.4 | the form |
| 4 | why | Why divide by T? | so | pᵢ / pⱼ = exp((zᵢ − zⱼ) / T): T scales the gap | the scaled gap |
| 5 | guarantee | What changes the result? | but | adding cancels; multiplying acts like 1/T; order holds for T > 0, breaks at T = −1 | invariances |
| 6 | meaning | How spread out is it? | so | entropy in bits, and as equally likely tokens | the measure |
| 7 | limits, close | — | — | T = 0, T → ∞, no zero probability; in short | the takeaway |

## 7. Close the loop

- **Answer:** the "In short" paragraph restates the opening in the same words, with the reason.
