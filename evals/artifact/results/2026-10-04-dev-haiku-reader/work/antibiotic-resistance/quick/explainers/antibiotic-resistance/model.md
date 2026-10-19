# Semantic model: antibiotic resistance

> Source of truth. Every rendering derives from this file.

## Central question

How do bacteria become resistant to an antibiotic?

## Audience and prior knowledge

A technical reader: school mathematics and science (cells, DNA, genes code for proteins, exponential growth), basic programming. New to microbiology. Does not know: what an antibiotic targets, mutation rates, plasmids, horizontal gene transfer, selection as a mechanism.

## Entities

| Entity | Definition (one sentence) | Status |
|---|---|---|
| Antibiotic | A molecule that kills bacteria or stops their growth by binding a target that bacteria need. | fact |
| Target | The bacterial protein or structure that the antibiotic binds (for penicillin: the enzymes that build the cell wall). | fact |
| Population | The bacteria in one infection: about 10^10 cells, all descended from a few cells. | estimate |
| Resistance gene | A version of a gene whose protein stops the antibiotic from working on that cell. | fact |
| Mutation | A random copying error in DNA when a cell divides. | fact |
| Gene transfer | One bacterium passes DNA to another, usually on a plasmid (a small circle of DNA). | fact |
| Selection | The antibiotic kills the susceptible cells, so the resistant cells make up the next population. | fact |

## Relationships

| From | Relationship | To | Notes |
|---|---|---|---|
| Mutation, gene transfer | create | resistance gene in a few cells | before or during treatment, at random |
| Resistance gene | blocks | antibiotic action | four mechanisms |
| Antibiotic | kills | susceptible cells | not resistant cells |
| Selection | enriches | resistant cells | they divide into the space left |

## Causal chain

```text
random variation (mutation or gene transfer) → a few resistant cells
→ antibiotic kills susceptible cells → resistant cells survive and divide
→ resistant population
```

## Quantities

- Mutation rate for one specific resistance mutation: about 10^-9 per cell division (illustrative; real values range about 10^-6 to 10^-10).
- Population in a serious infection: about 10^10 cells.
- Expected resistant cells before any drug: 10^10 × 10^-9 = 10 cells.
- Regrowth: 10 cells × 2^30 ≈ 10^10 cells. 30 doublings at 30 min each ≈ 15 hours (lab rate; slower in a body).
- Two drugs with independent targets: chance per cell 10^-9 × 10^-9 = 10^-18; expected cells in 10^10: 10^-8, so effectively none.

## Alternative states

| State | What changes | Why |
|---|---|---|
| No antibiotic | resistant cells stay rare | resistance often costs growth rate; no selection |
| Antibiotic present | resistant cells take over | selection |
| Two drugs together | resistance very unlikely | a cell needs two independent rare events |
| Resistance gene on a plasmid | spreads between cells and species | gene transfer, not only division |

## Why this form

| Operation | Simplest alternative | What the alternative breaks |
|---|---|---|
| Resistance comes from pre-existing random variation, then selection | Each cell "learns" or adapts when it meets the drug | If cells adapted on contact, all 10^10 would survive or none would; observed: a fixed rare fraction (about 10 in 10^10) survives, and those cells existed before exposure (Luria–Delbrück, 1943) |

## Concrete cases

| Claim | Holds here | Breaks here |
|---|---|---|
| Selection enriches resistance | 10^10 cells with drug: 10 resistant survive, regrow to 10^10 in about 30 doublings | Small population of 10^7 cells: expected resistant cells = 0.01, so the drug usually clears it |
| Combination therapy prevents resistance | Two independent drugs: 10^-18 per cell, 10^-8 expected | A plasmid carrying both resistance genes gives both at once, so the multiplication no longer applies |

## Terms

- **Susceptible:** the antibiotic kills or stops this cell.
- **Resistant:** the cell survives a dose that kills susceptible cells.
- **Plasmid:** a small DNA circle, separate from the chromosome, that cells copy and pass to each other.
- **Selection:** see Entities.

## Epistemic status

- **Established:** four mechanisms; mutation and gene transfer as sources; resistance arises before exposure (Luria–Delbrück).
- **Illustrative:** the specific numbers 10^-9, 10^10, 30 min.

## Confusion points

- "The antibiotic causes the mutation" → the mutation is random and usually exists already; the antibiotic only selects. (Some antibiotics raise mutation rates a little; out of scope.)
- "The patient becomes resistant" → the bacteria do, not the person.
- "Resistant cells are stronger in general" → they often grow slower without the drug.

## Scope

- **Out of scope:** tolerance and persister cells (survive without a resistance gene) — see "antibiotic persistence".
- **Out of scope:** stress-induced mutagenesis (SOS response).
- **Out of scope:** clinical policy (stewardship, dosing) beyond one line.

## Representation decision

- **Stage:** 1
- **Reason:** a short causal sequence plus a four-row list of mechanisms; prose with one table and worked numbers carries it.
- **Levels:** L1 answer / L2 the two steps / L3 why it is selection, not adaptation / L4 mechanisms.
