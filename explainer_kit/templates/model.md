# Semantic model: <subject>

> Source of truth. Every rendering (prose, diagram, page, video) derives from this file.
> If a rendering needs a new fact, add it here first.

## Central question

<One sentence.>

## Audience and prior knowledge

<Who reads this. What they already know. What they do not know. Default: a technical reader (school mathematics and science, basic programming) who is new to this subject. Renderings define what this reader does not know, and do not explain what they do.>

## Entities

| Entity | Definition (one sentence) | Status |
|---|---|---|
| | | fact / assumption / estimate / … |

## Relationships

| From | Relationship (verb) | To | Notes |
|---|---|---|---|
| | | | |

## Dependencies (learning order)

1. <Concept that must be understood first>
2. …

## Causal chain

```text
A → B → C
```

## Temporal sequence

1. <What happens first>
2. …

## Quantities

<Equations, magnitudes, ratios, thresholds, tradeoffs. Give units.>

## Alternative states

| State / scenario | What changes | Why |
|---|---|---|
| | | |

## Why this form

For each formula, function, or operation: why this form and not the simplest alternative? Show the alternative failing with numbers. Each entry becomes a `why` claim in model.yaml.

| Operation | Simplest alternative | What the alternative breaks (with numbers) |
|---|---|---|
| | | |

## Concrete cases

For each guarantee or "always / never" claim: one instance with numbers where it holds, and one where removing its assumption breaks it. For each mechanism step: one worked example with numbers. Each entry becomes a `guarantee` or `mechanism` claim.

| Claim | Holds here (numbers) | Breaks here, without its assumption (numbers) |
|---|---|---|
| | | |

## Terms

Every term a rendering uses, defined in one sentence, in the order a reader meets them. One word per concept: when two concepts are close (a tentative value and its final value), give each its own word and list the wrong uses under `terms` in model.yaml. Every quantity a rendering shows says what it means for the reader, with a value from the example (what is different at a low value and a high one).

## Epistemic status

- **Observed / established:** …
- **Mathematical consequence:** …
- **Assumed:** …
- **Estimated / model output:** …
- **Disputed:** …
- **Unknown / speculative:** …

## Confusion points

- <Likely misunderstanding> → <correction>

## Scope

What this explanation deliberately leaves out, and where a reader should look next. A learner's next question should land here or in the model, never in silence.

- **Out of scope:** <topic> — <one-line pointer>

## Representation decision

- **Stage:** 1 / 2 / 3 / 4
- **Reason:** <Which structure in this model needs that medium.>
- **Levels:** L1 … / L2 … / L3 … / L4 …
