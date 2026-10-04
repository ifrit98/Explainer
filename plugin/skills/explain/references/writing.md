# STE-80 writing mode

An ASD-STE100-inspired house style, about 80% of strict STE. Strict STE uses a controlled dictionary. These rules do not check against that dictionary, so never claim formal STE compliance.

Optimize for precision and low cognitive load, not literary style.

## Sentence rules

- Prefer short sentences.
- Use one principal idea per sentence.
- Prefer active voice.
- Prefer simple present tense.
- Use imperative verbs for procedures.
- Put the instruction before its explanation.
- Prefer concrete verbs to abstract noun constructions ("decide", not "make a decision").
- Avoid long subordinate clauses.

## Word rules

- Use the same word for the same concept throughout. Do not use synonyms for variety. When two concepts are close (a value that can still change, and its final value), give each its own word and never swap them. Record the wrong phrases under `terms` in `model.yaml`; `explainer check` fails a rendering that uses one.
- Give each quantity its meaning when you first show it: what the number tells the reader, and what is different at a low value and a high one.
- Define each technical term when you first introduce it.
- Keep noun clusters to about three words. Break longer clusters with "of", "for", or a relative clause.
- Avoid a pronoun when its antecedent could be ambiguous. Repeat the noun.
- Avoid unnecessary qualifiers ("quite", "somewhat", "relatively", "fairly").
- Avoid idioms and rhetorical flourishes.

## Substitutions

| Avoid | Use |
|---|---|
| utilize | use |
| prior to | before |
| commence | start |
| in order to | to |
| approximately | about (unless precision requires "approximately") |
| subsequent to | after |
| in the event that | if |
| facilitate | help, let, make possible |
| it is imperative that | must |
| a number of | some, several, or the exact number |
| due to the fact that | because |

## Structure rules

- Break complex procedures into numbered steps.
- Break complex comparisons into tables.
- Break complex relationships into diagrams.

## Readability targets

| Unit | Target |
|---|---|
| Procedural sentence | ≤ 20 words |
| Descriptive sentence | ≤ 25 words |
| Noun cluster | ≤ 3 words |
| Paragraph | ≤ 6 sentences |

These are targets, not absolute limits. Break a target when technical accuracy requires it.

## Semantic compression

STE reduces grammatical complexity. It does not reduce conceptual density. Also minimize semantic indirection: do not make the reader decode abstract language when a direct causal statement is possible.

| Indirect | Direct |
|---|---|
| The relationship between A and B can be understood in the context of C. | A causes B because C. |
| One potential limitation concerns situations in which X may become relatively large compared with Y. | The model fails when X exceeds Y. |

## Worked example

- **Before:** It is imperative that the operator ensures the hydraulic reservoir is replenished prior to commencing operation.
- **Better:** Make sure that the hydraulic reservoir is full before you start the operation.
- **Best:** Fill the hydraulic reservoir before you start the machine.

The best version removes the most linguistic machinery and keeps the full meaning.
