# Semantic model: how a vaccine prepares the immune system

> Source of truth. Every rendering derives from this file.

## Central question

How does a vaccine prepare the immune system for a disease it has never met?

## Audience and prior knowledge

A technical reader (school science, basic programming) new to immunology. Knows cells divide, proteins have shapes, exponential growth. Does not know lymphocyte, antigen, receptor diversity, clonal selection, memory cell.

## Entities

| Entity | Definition (one sentence) | Status |
|---|---|---|
| antigen | A molecular shape on a pathogen (for example, a virus surface protein) that a receptor can bind. | fact |
| lymphocyte | A white blood cell (B cell or T cell) that carries one receptor type on its surface. | fact |
| receptor | The binding protein of one lymphocyte; its shape is made by random gene shuffling before any infection. | fact |
| repertoire | The full set of different receptors across all lymphocytes in one body. | fact |
| clonal expansion | Rapid division of a lymphocyte whose receptor binds an antigen, making a clone of identical cells. | fact |
| memory cell | A long-lived lymphocyte left after a response; it keeps the matching receptor. | fact |
| antibody | A soluble copy of a B cell receptor; it binds the antigen and blocks or marks the pathogen. | fact |
| vaccine | A harmless source of the antigen, plus an alarm signal (adjuvant or the vaccine's own components). | fact |

## Relationships

| From | Relationship | To |
|---|---|---|
| random gene shuffling | makes | repertoire |
| antigen | selects | lymphocyte with a matching receptor |
| selected lymphocyte | undergoes | clonal expansion |
| clonal expansion | leaves | memory cells |
| memory cells | shorten | the second response |

## Causal chain

```text
random receptors (before exposure) → vaccine antigen binds the rare match → clonal expansion (~1 week)
→ memory cells remain → real pathogen → large, fast response in days → pathogen stopped early
```

## Quantities (estimates, order of magnitude)

- Matching naive lymphocytes: about 1 in 100,000 to 1 in 1,000,000 lymphocytes.
- Repertoire size: more than 10^11 possible receptors (gene shuffling); about 10^8 or more distinct receptors present at once.
- First response: useful antibody after about 7–14 days.
- Second response: useful antibody after about 2–4 days, at 10–100 times higher levels.
- Memory cells: present in about 10–100 times more cells than the naive match; last years to decades.
- Illustrative race: a pathogen that multiplies 10× per day grows 10^7-fold in 7 days, but only 10^3-fold in 3 days.

## Alternative states

| Scenario | What changes | Why |
|---|---|---|
| No vaccine, first infection | Response needs ~7–14 days | Few matching cells; expansion must start from them |
| Vaccinated, infection | Response in ~2–4 days | Memory cells start from a larger, better-fitting clone |
| Variant with a changed antigen | Weaker protection | Memory receptors fit the old shape less well |
| Years later, no booster | Weaker protection for some vaccines | Antibody levels and memory decline |

## Why this form

| Operation | Simplest alternative | What it breaks |
|---|---|---|
| Make receptors at random, in advance | Design a receptor after seeing the pathogen | The body has no mechanism to design a protein from a shape; it can only select from what exists |
| Use a harmless antigen | Use the real pathogen | The first response takes ~7 days, while a 10×/day pathogen grows 10^7-fold |

## Concrete cases

| Claim | Holds | Breaks |
|---|---|---|
| Memory gives a faster response | Vaccinated: response at day ~3, pathogen grew ~10^3-fold | Variant with a changed antigen: memory fits less well; response is slower |

## Terms

antigen, lymphocyte, receptor, repertoire, clonal expansion, memory cell, antibody, vaccine — as above. "Learn" is used only with the meaning "select and amplify", never "design".

## Epistemic status

- **Established:** clonal selection, random receptor generation, memory, faster secondary response.
- **Estimated:** all frequencies and days are typical orders of magnitude; they vary by antigen and person.
- **Assumed (illustration):** the 10×/day pathogen growth rate.

## Confusion points

- The immune system "studies" the pathogen and designs a counter → no; matching receptors already exist by chance; the vaccine selects them.
- A vaccine contains a weak dose of the disease → many contain only one protein, or instructions (mRNA) to make one.
- Antibodies are the memory → antibodies decline; memory cells are the durable record.

## Scope

- **Out of scope:** T cell killing, affinity maturation detail, self-tolerance (why receptors that bind your own body are removed), herd immunity — see an immunology text (for example, Janeway's *Immunobiology*).

## Representation decision

- **Stage:** 1
- **Reason:** One sequential causal chain; one comparison table holds the two responses.
- **Levels:** L1 the answer / L2 the steps / L3 why it works (the race) / L4 limits.
