# Semantic model: how bacteria become resistant to an antibiotic

> Source of truth. Every rendering (prose, diagram, page, video) derives from this file.
> If a rendering needs a new fact, add it here first.

## Central question

How does a population of bacteria that an antibiotic used to kill become a population that the antibiotic no longer kills?

## Audience and prior knowledge

A technical reader: school mathematics and science, basic programming, new to microbiology. Knows: cells, DNA and genes (a gene codes for a protein), enzymes, that a mutation is a change in DNA, exponential growth and doubling, powers of ten, expected value, the idea of natural selection in outline. Does not know: how antibiotics act on a cell, what a plasmid is, horizontal gene transfer, minimum inhibitory concentration (MIC), fitness cost, the Luria–Delbrück result.

## Entities

| Entity | Definition (one sentence) | Status |
|---|---|---|
| Bacterium | A single-cell organism that copies its DNA and divides in two. | fact |
| Antibiotic | A molecule that kills bacteria or stops their growth by binding to a target in the cell. | fact |
| Target | The molecule in the bacterium that the antibiotic binds to, usually a protein the cell needs (for example, the enzymes that build the cell wall). | fact |
| Resistance gene | A gene, changed by mutation or gained from another bacterium, that lets the cell grow at a drug concentration that stops normal cells. | fact |
| Susceptible cell | A cell that the drug stops at the concentration reached in the patient. | definition |
| Resistant cell | A cell that grows at the concentration reached in the patient. | definition |
| Mutation | A random copying error in DNA, made at a division, independently of the drug. | fact |
| Plasmid | A small circle of DNA, separate from the chromosome, that a bacterium can copy and pass to another bacterium. | fact |
| Horizontal gene transfer | A bacterium gets a gene from another bacterium, not from its parent cell. Main route: conjugation (two cells touch and one copies a plasmid into the other). | fact |
| Selection | The drug removes susceptible cells; resistant cells survive and divide, so their fraction in the population rises. | fact |
| MIC (minimum inhibitory concentration) | The lowest drug concentration that stops a strain's growth, measured in mg/L. | definition |
| Fitness cost | A resistant cell often grows more slowly than a susceptible cell when there is no drug, because it makes an extra protein or its changed target works less well. | fact (size varies) |

## Relationships

| From | Relationship (verb) | To | Notes |
|---|---|---|---|
| Mutation | makes (at random, before any drug) | resistance gene | about 1 in 10^8 divisions for one given resistance mutation |
| Horizontal gene transfer | gives | resistance gene | in one step, can cross species |
| Plasmid | carries | resistance genes | often several at once |
| Antibiotic | stops | susceptible cell | |
| Resistance gene | blocks | antibiotic action | four ways: destroy, change target, pump out, keep out |
| Antibiotic | selects | resistant cell | by removing its competitors |
| Fitness cost | slows | resistant cell, when there is no drug | |

## Resistance mechanisms (what the resistance gene does)

| Way | Example |
|---|---|
| Destroy the drug | A beta-lactamase enzyme cuts penicillin before it reaches the cell-wall enzymes. |
| Change the target | One DNA letter change in the rpoB gene changes the target protein, so rifampicin no longer binds. |
| Pump the drug out | An efflux pump (a membrane protein) exports tetracycline faster than it enters. |
| Keep the drug out | Loss of a porin (an entry channel in the outer membrane) lets less drug in. |

Each way raises the MIC. Illustrative: beta-lactamase raises a strain's MIC from 0.5 to 32 mg/L.

## Dependencies (learning order)

1. An antibiotic works by binding a target in the cell.
2. A resistance gene stops that binding or its effect (four ways, with examples).
3. Resistance genes appear at random (mutation) or arrive from other bacteria (horizontal gene transfer), before the drug.
4. The drug removes the susceptible cells; the resistant ones remain and multiply (selection).
5. Without the drug, the fitness cost works against resistant cells.

## Causal chain

```text
random variation (mutation or gene transfer) → a few resistant cells among many susceptible ones
→ antibiotic stops the susceptible cells → resistant cells grow into the space and nutrients left
→ the population is now resistant → resistant cells spread to other hosts, and plasmids spread to other species
```

## Temporal sequence

1. Before treatment: the infection grows to 10^10 cells. About 10^10 divisions made it, so about 100 resistance mutations happened. Early mutants have divided since, so resistant cells number at least 100, typically several hundred.
2. Treatment: the drug stops the susceptible cells, and the immune system clears them; the resistant cells keep dividing.
3. Regrowth: 100 cells double about 27 times to reach 10^10 again (2^27 ≈ 1.3 × 10^8 ≈ 10^10 / 100). Assumption: the immune system removes some cells but does not keep up with a population that doubles. Weakened patients clear fewer.
4. The infection returns, and the same drug no longer works on it.

## Quantities

- Rate of one given resistance mutation: about 10^-8 per division (order of magnitude; real values span about 10^-6 to 10^-10).
- Doubling: every cell in the population divides once. Growing from 1 cell to N cells takes about N divisions.
- Cells in a serious infection: 10^9 to 10^10 or more (estimate). Example uses 10^10.
- Expected resistance mutations before treatment: 10^10 × 10^-8 = 100. Resistant cells ≥ 100, because early mutants divide (mean about μN ln N ≈ 2,300; typical several hundred; heavy spread between infections).
- Small infection, 10^6 cells: 10^6 × 10^-8 = 0.01 expected mutations. Probability of at least one resistant cell = 1 − e^-0.01 ≈ 1%. For 10^10 cells, probability ≈ 1.
- Regrowth: 100 → 10^10 needs log2(10^8) ≈ 26.6, so about 27 doublings. At 30 min per doubling (laboratory, ideal) that is about 13 hours; in a patient, doublings are slower.
- MIC example (illustrative): susceptible strain 0.5 mg/L, resistant strain 32 mg/L, concentration reached in blood 8 mg/L. 8 > 0.5: the drug stops the first strain. 8 < 32: the second strain grows.
- Fitness cost (illustrative): resistant cells grow 5% slower, no drug: each time the susceptible cells double, the resistant cells grow 0.95 times as much. The resistant-to-susceptible ratio is multiplied by 0.95 each doubling, because both groups compound: after 10 doublings 0.95^10 ≈ 0.60, after 100 doublings 0.95^100 ≈ 0.006. (Not 1 − 100 × 0.05, which goes negative.)
- Compensatory mutation: a second mutation, in another gene, that cuts the cost from 5% to 1% without losing resistance: 0.99^100 ≈ 0.37 after 100 doublings.
- Plasmid persistence: one plasmid often carries resistance genes for several drugs, so any one of those drugs still selects the whole plasmid.
- Luria–Delbrück scatter: independent rare events with mean 11 have a spread of about √11 ≈ 3.3; mean ± 2 spreads ≈ 5 to 18.

## Alternative states

| State / scenario | What changes | Why |
|---|---|---|
| Drug present | resistant fraction rises from about 10^-8 to near 1 | susceptible cells are removed |
| Drug absent | resistant fraction falls slowly, or stays | fitness cost; compensatory mutations reduce it |
| Small population (10^6) | about 1% chance of any resistant cell; drug clears it | 10^6 × 10^-8 = 0.01 |
| Two drugs with independent targets | needs two independent mutations: 10^-16 | 10^10 × 10^-16 = 10^-6 expected double-resistant cells |
| Two drugs, one plasmid or pump resists both | one event, about 10^-8 | 10^10 × 10^-8 = 100: the combination fails |
| Plasmid gene | one transfer gives a whole resistance gene, even to another species | not a rare copying error |

## Why this form

| Operation | Simplest alternative | What the alternative breaks (with numbers) |
|---|---|---|
| Explain resistance as selection of variants that existed before the drug | "The drug makes the bacteria change" | Luria and Delbrück (1943) grew 20 parallel cultures and plated each on a killing agent (a virus, not an antibiotic; same logic). Mean about 11 resistant colonies. If the agent caused resistance, every culture would show about 11 (most between 5 and 18). Observed: 11 cultures had 0, one had 107. That spread fits mutations at random times before exposure: an early mutant leaves many resistant descendants, a late one few. |
| Count horizontal gene transfer as a second source | "Every resistance must be a new mutation in that lineage" | A beta-lactamase is a complete enzyme; one letter change does not build a new enzyme. Bacteria get such genes on plasmids, and the same plasmid gene turns up in different species. |

## Concrete cases

| Claim | Holds here (numbers) | Breaks here, without its assumption (numbers) |
|---|---|---|
| Resistant cells exist before treatment (mechanism) | 10^10 cells × 10^-8 = 100 mutations: at least 100 resistant cells | 10^6 cells × 10^-8 = 0.01: about a 1% chance of any; the drug clears the infection |
| Resistance takes over only when the drug is present (guarantee) | With drug: fraction about 10^-8 → near 1 after regrowth (100 cells → 10^10 in 27 doublings) | Without drug, 5% cost: ratio × 0.95^100 ≈ 0.006 after 100 generations |
| Two drugs together prevent selection (guarantee, assumes independent resistance) | Independent: 10^-8 × 10^-8 = 10^-16; 10^10 cells give 10^-6 expected double-resistant cells | One plasmid or pump resists both: 10^10 × 10^-8 = 100 survivors |

## Terms

- **Antibiotic:** a molecule that kills bacteria or stops their growth by binding a target.
- **Target:** the molecule the antibiotic binds to.
- **Resistance gene:** a gene, changed by mutation or gained from another bacterium, that lets the cell grow in the drug.
- **Resistant / susceptible:** grows / is stopped at the concentration the drug reaches in the patient. Resistance is a property of the bacteria, not of the patient.
- **Mutation:** a random copying error in DNA at a division.
- **Plasmid:** a small circle of DNA, separate from the chromosome, that can pass between bacteria.
- **Horizontal gene transfer:** getting a gene from another bacterium, not from the parent.
- **Conjugation:** two bacteria touch, and one copies a plasmid into the other.
- **Selection:** the drug removes the susceptible cells, so the resistant fraction rises.
- **MIC:** the lowest concentration that stops a strain's growth. Low MIC (0.5 mg/L, below the 8 mg/L reached): the drug works. High MIC (32 mg/L, above it): the drug fails.
- **Fitness cost:** slower growth of a resistant cell when no drug is present.
- **Doubling:** every cell divides once. "Division" is one cell splitting.
- Mutation rate 10^-8 per division: one in a hundred million divisions makes this mutation. At 10^-6, resistance appears even in small populations; at 10^-10, only in very large ones.

## Epistemic status

- **Observed / established:** the four resistance mechanisms; mutations arise before exposure (Luria–Delbrück 1943); plasmids carry and transfer resistance genes; selection by antibiotic use.
- **Mathematical consequence:** expected counts (N × rate); doublings needed; product of independent rates.
- **Assumed:** the two resistances in combination therapy are independent; constant doubling time; the immune system does not keep up with growth.
- **Estimated / illustrative:** the 10^-8 rate, 10^10 cell count, 30 min doubling, 5% cost and MIC values are orders of magnitude.

## Confusion points

- "The patient becomes resistant" → the bacteria are resistant; the patient's body does not change.
- "The drug makes bacteria mutate / bacteria learn" → the variants exist before the drug; the drug removes their competitors.
- "Each cell slowly gets used to the drug" → a cell's resistance comes from its genes. The population changes because the fraction of resistant cells changes. Resistance can rise in steps (a first mutation raises MIC from 0.5 to 2 mg/L, a second to 16 mg/L), but each step is a new gene change, selected in turn.
- "Resistance disappears when we stop the drug" → it falls slowly at best; compensatory mutations reduce the cost, and plasmids persist.

## Scope

- **Out of scope:** tolerance and persister cells (survive without being resistant) — search "antibiotic persistence".
- **Out of scope:** transformation and transduction (other routes of gene transfer) — "horizontal gene transfer" in any microbiology text.
- **Out of scope:** stress-induced mutagenesis (some drugs raise the mutation rate via the SOS response) — search "SOS response antibiotic".
- **Out of scope:** course length, stewardship policy, agricultural use, biofilms.

## Representation decision

- **Stage:** 1
- **Reason:** the subject is a causal sequence (variation → selection → regrowth → spread) with one table of mechanisms and short arithmetic. Nothing needs a parameter explored or motion seen.
- **Levels:** L1 resistance is selection of variants that existed before the drug / L2 the four mechanisms and the two sources / L3 numbers: N × rate, doublings, cost.
