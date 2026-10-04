# Narrative: attention

> Pass 3. The page follows these beats, top to bottom.

## 1. Reader before and after

- **Before:** Developers who use LLMs. They know vectors, the dot product, and matrix multiplication; that a model turns each token into a vector (an embedding); and softmax. They do not know how attention works.
- **After:** "Each token's output is a weighted average of all tokens' values, with weights softmax(query · key / √d); the query decides what it finds, a separate key lets it look for something other than itself, and √d keeps softmax from saturating."

## 2. Question and motive

- **Question:** how does a token use information from other tokens? Answer in the lede, in words.
- **Why care:** this is how "it" can carry what it refers to; every transformer layer does it.
- **Why this approach:** one token, one sentence, hand-made vectors, so every number is visible; then remove one part at a time to see why it is there.

## 3. Introduction ledger

| Reference | Means | Grounded by | Beat |
|---|---|---|---|
| query, key, value | what a token looks for, what it offers, what it passes on | the lede, then q = (2, 0) and the key column | 1, 3 |
| score | query · key / √d | the table's score column | 3 |
| weight | softmax of the scores | the bars | 3 |
| d | the length of query and key vectors | d = 2 here, 64 per head in GPT-2 small | 4 |
| causal mask | a token sees only itself and earlier tokens | "tired" struck out | 3 |
| highlight on a word | its weight | "animal" filled most | 3 |

## 4. Beats

| # | Kind | Reader's question | Bridge | Shown | Said | Reader now knows |
|---|---|---|---|---|---|---|
| 1 | answer | What does attention do? | — | lede | Each token builds its new vector as a weighted average of the values; weights from query · key. | the answer |
| 2 | test | Does the query decide? | so | predict gate | Turn the query to "place": which token wins? | committed a guess |
| 3 | instance | What are the numbers? | — | instrument: sentence, slider, bars, table, output | scores 4, 0, 1, 0 → weights 0.808 … → output 81% animal | the mechanism, live |
| 4 | objection | Why each part? | but | four toggles; Level 3 cards; the d slider | equal weights tie; query = x ties; no √d saturates (0.996 at d = 64); softmax keeps weights positive | why each part |
| 5 | implementation | What runs in a real model? | so | Level 4 | the matrix form, heads (12 × 64 = 768), the mask | how it scales |
| 6 | trust | What is real here? | — | epistemic cards | formulas are fact; vectors are constructed; "looks for" is interpretation | the status of each claim |
| 7 | recap | — | — | summary | four lines | the takeaway |

## 7. Close the loop

- **Answer:** the summary repeats the lede.
- **Payoff:** the reader can predict what a change in the query, the scale, or the mask does to the weights.
