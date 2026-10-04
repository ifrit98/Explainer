# Semantic model: self-attention

> Source of truth. Every rendering derives from this file.

## Central question

How does a token in a transformer use information from the other tokens, and why is attention built from queries, keys, values, a dot product, a division by √d, and softmax?

## Audience and prior knowledge

Developers who use LLMs. They know vectors, the dot product, and matrix multiplication; that a model turns each token into a vector (an embedding); and softmax (see the softmax-temperature example). They do not know how attention works.

## Entities

| Entity | Definition (one sentence) | Status |
|---|---|---|
| token vector x | the vector that represents one token at this layer | fact |
| query q | what this token looks for: q = x W_Q | fact (the formula); the meaning is an interpretation |
| key k | what this token offers to be found by: k = x W_K | fact; interpretation as above |
| value v | what this token passes on when it is attended to: v = x W_V | fact |
| score | q · k / √d: how well one token's query matches another token's key | fact |
| weight | softmax of a row of scores: positive, and the row sums to 1 | mathematical consequence |
| output | Σ weight × v: the new vector for the token, a weighted average of value vectors | fact |
| head | one set of W_Q, W_K, W_V; a layer runs several heads in parallel | fact |
| causal mask | in a decoder (GPT-style), a token may only attend to itself and earlier tokens | fact |

## Causal chain

```text
token vectors x
  → each token makes a query, a key, and a value (three learned matrices)
  → score of token i for token j = qᵢ · kⱼ / √d
  → softmax over j turns the scores into weights (positive, sum 1)
  → output of token i = Σⱼ weightᵢⱼ × vⱼ
  → the output goes on to the next layer
```

## The worked example (constructed)

Sentence: "The animal didn't cross the street because it was too tired." Four tokens: animal, street, it, tired (in that order). The vectors are made by hand, 2 numbers for keys and queries (d = 2) and 3 for values, so that each number has a name. A trained model learns its vectors, uses d = 64 per head, and its dimensions have no names.

| Token | key k (animate, place) | value v (animal, place, tired) |
|---|---|---|
| animal | (2, 0) | (1, 0, 0) |
| street | (0, 2) | (0, 1, 0) |
| it | (0.5, 0.5) | (0, 0, 0) |
| tired | (0, 0) | (0, 0, 1) |

The query of "it" looks for something animate: q = (2, 0).

| | animal | street | it | tired |
|---|---|---|---|---|
| q · k | 4 | 0 | 1 | 0 |
| ÷ √2 | 2.83 | 0 | 0.71 | 0 |
| weight | 0.808 | 0.048 | 0.097 | 0.048 |

Output of "it" = 0.808 × (1, 0, 0) + 0.048 × (0, 1, 0) + 0.048 × (0, 0, 1) = (0.808, 0.048, 0.048): after attention, "it" carries 81% of the animal's value. A query that looks for a place, q = (0, 2), gives street 0.808 instead.

## Quantities

- d: the length of query and key vectors. Toy: 2. GPT-2 small: 64 per head, 12 heads, 12 × 64 = 768 = the token vector length.
- Score spread: if the d numbers in q and k are independent with mean 0 and variance 1, q · k has variance d, so its standard deviation is √d (8 at d = 64). Dividing by √d brings it back to 1.
- The same four scores, spread as at dimension d, with the top weight after softmax: d = 1: 0.543; d = 4: 0.763; d = 16: 0.94; d = 64: 0.996; d = 128: 1.000 (to three places). Scaled by √d, the top weight is 0.543 at every d.

## Alternative states (toggles on the page)

| Change | What happens in the example | Why |
|---|---|---|
| Equal weights (no scores) | "it" gets 0.25 of every value: no more animal than street | weights that ignore content cannot pick |
| Query = key = x (no separate W_Q, W_K) | "it" scores animal 1 and street 1: a tie, 0.313 each | the vector of "it" says what "it" is, not what it looks for |
| No division by √d | toy: animal 0.92; at d = 64 the top weight is 0.996 | the scores spread with √d, and softmax saturates |
| Causal mask on | "it" cannot see "tired" (later); its weights become 0.848, 0.050, 0.102 | a decoder predicts the next token, so it may not look ahead |

## Why this form

| Operation | Simplest alternative | What the alternative breaks (with numbers) |
|---|---|---|
| weights from scores (content-based) | equal weights, 1 / n each | "it" gets 0.25 animal and 0.25 street: it cannot resolve which noun it means |
| separate query and key | use the token vector x as both | "it" scores animal 1 and street 1 (x = (0.5, 0.5) matches both equally): 0.313 each, a tie |
| dot product score | — | the dot product measures how well two vectors point the same way, and for all tokens at once it is one matrix product, QKᵀ |
| softmax | divide each score by the row sum | scores can be 0 or negative; a weight of 0 / 0 or below 0 is not a weight. Softmax gives positive weights that sum to 1, so the output is a weighted average of values |
| divide by √d | no division | at d = 64 the top weight is 0.996: almost all weight on one token, and the gradient through softmax nearly vanishes, so training stalls |

## Epistemic status

- **Fact:** the formulas (Vaswani et al., 2017); GPT-2 small sizes.
- **Mathematical consequence:** weights are positive and sum to 1; score variance d under the independence assumption.
- **Constructed:** every vector in the worked example, and the names of its dimensions.
- **Interpretation:** "a query is what a token looks for". It describes what the math allows; a trained head need not use it this way.
- **Observation (in some trained models):** some heads track a clear relation, such as the previous token or the noun a pronoun refers to. Many heads have no simple description.

## Confusion points

- "Attention weights say which words the model thinks are important." → They say how much of each value one token mixes in, in one head of one layer. Importance for the output needs more analysis.
- "Q, K, V are three copies of the token." → They are three different learned projections of it.
- "Softmax picks the best match." → It mixes; the scale sets how sharp the mix is (a temperature, as in the softmax-temperature example: here T = √d).

## Scope

- **Out of scope:** how W_Q, W_K, W_V are learned (backpropagation).
- **Out of scope:** positional information (how the model knows token order) — see positional encodings, RoPE.
- **Out of scope:** the MLP layer, residual connections, and layer norm.
- **Out of scope:** efficient attention (KV cache, FlashAttention).

## Representation decision

- **Stage:** 3 (interactive).
- **Reason:** the reader must see one mechanism under several alternatives (remove a part, see what breaks) and at four levels (what it is, how, why, implementation). A static diagram shows one state.
- **Levels:** L1 a token mixes in other tokens' values / L2 query · key → softmax → weighted sum / L3 why each part, as toggles / L4 matrices, heads, mask, sizes.
