# Semantic model: STE-80 rewrite

> Source of truth. Every rendering (prose, diagram, page, video) derives from this file.

## Central question

How does STE-80 make one technical sentence easier to read without changing its meaning?

## Audience and prior knowledge

People who write technical text. They know grammar. They do not know ASD-STE100.

## Entities

| Entity | Definition (one sentence) | Status |
|---|---|---|
| ASD-STE100 | A controlled language for technical text, with a fixed dictionary and writing rules. | fact |
| STE-80 | This repo's house style: about 80% of ASD-STE100, without the dictionary check. | definition |
| Sentence | The unit that the reader decodes. Each version has the same instruction. | fact |
| Word count | The number of words in the sentence. A proxy for reading effort. | assumption: shorter is easier when meaning is kept |
| Rule 1 — simple words | Replace a formal word with a common word. | fact (STE rule) |
| Rule 2 — direct instruction | Write the instruction to the reader. Remove the abstract frame. | fact (STE rule) |
| Rule 3 — concrete verb | Use a verb for the action, not a state plus a helper verb. | fact (STE rule) |

## Causal chain

```text
formal words + abstract frame + state verb  →  more decoding work  →  slower, less reliable reading
each rule removes one source of decoding work  →  same instruction, fewer words
```

## Temporal sequence (the rewrite)

| Step | Sentence | Words |
|---|---|---|
| S0 original | It is imperative that the operator ensures the hydraulic reservoir is replenished prior to commencing operation. | 16 |
| S1 rule 1 | It is imperative that the operator ensures the hydraulic reservoir is full before starting the operation. | 16 |
| S2 rule 2 | Make sure that the hydraulic reservoir is full before you start the operation. | 13 |
| S3 rule 3 | Fill the hydraulic reservoir before you start the machine. | 9 |

## Quantities

16 → 15 → 13 → 9 words. Rule 1 removes one word (prior to → before); its point is easier words. Rules 2 and 3 shorten the sentence.

## Epistemic status

- **Established:** the three rules are ASD-STE100 writing rules.
- **Assumption:** word count is a proxy for reading effort only when the meaning stays the same.
- **Simplification:** S3 says "machine" for "operation". That is a small change of reference, accepted in the source example.

## Confusion points

- "Shorter is always better" → No. Rule 1 keeps the length and still helps. The target is less decoding, not fewer words.
- "STE-80 is STE" → No. STE-80 does not check words against the STE dictionary.

## Representation decision

- **Stage:** 4 (animated explainer).
- **Reason:** the idea is a transformation. The viewer must see which words survive each rewrite. Object identity across steps carries the meaning.
- **Levels:** L1 what STE-80 is / L2 the three rewrites / L3 why each rewrite reduces decoding work.
