# How do bacteria become resistant to an antibiotic?

**A few bacteria in a large population already carry a gene that protects them, by random chance. The antibiotic kills the other bacteria, and the protected ones divide to replace them. The bacteria do not learn; the drug selects.**

## What an antibiotic does

An antibiotic is a molecule that binds a **target**: a protein or structure that the bacterium needs. Penicillin, for example, blocks the enzymes that build the cell wall, so the cell bursts. A cell is **susceptible** if the drug kills it or stops its growth. A cell is **resistant** if it survives a dose that kills susceptible cells. The bacteria become resistant, not the patient.

## Step 1: random variation makes a few resistant cells

Resistance needs a **resistance gene**: a version of a gene whose protein stops the drug from working on that cell. A cell gets one in two ways. <!-- claim: sources -->

1. **Mutation.** Each time a cell copies its DNA, it makes rare random errors. A specific error that changes the target has a chance of about 10^-9 per division: once per billion divisions.
2. **Gene transfer.** Bacteria pass DNA to each other, often on a **plasmid**: a small circle of DNA, separate from the chromosome, that cells copy and hand over. One plasmid can carry several resistance genes and move between species, so one transfer can give resistance to several drugs.

## Step 2: the antibiotic selects the resistant cells

Worked numbers (illustrative): <!-- claim: selection-worked -->

- A serious infection holds about 10^10 bacteria.
- Expected resistant cells before any drug: 10^10 × 10^-9 = 10.
- The antibiotic kills the susceptible cells. The 10 resistant cells survive.
- Each survivor divides. 10 × 2^30 ≈ 10^10, so 30 doublings rebuild the population. At 30 minutes per doubling (a lab rate; slower in a body), that takes about 15 hours.

The new population is almost all resistant. This process is **selection**: the drug removes one kind of cell, and the remaining kind fills the space.

Predict before you read on: what happens with a small population of 10^7 cells? Expected resistant cells = 10^7 × 10^-9 = 0.01. Usually no resistant cell exists, so the drug clears the infection.

## Why selection, and not adaptation

<!-- claim: selection-not-adaptation -->
The simplest alternative idea is that each cell meets the drug and adapts. Then every cell would have the same chance to survive. Instead, a rare fraction survives, and those cells were resistant before they met the drug. Luria and Delbrück showed this in 1943: the number of resistant bacteria varied between cultures in a way that only fits mutations that occurred before exposure. So the antibiotic does not cause resistance. It reveals and enriches resistance that random variation already made.

## How a resistance gene protects the cell

<!-- claim: mechanisms -->
Each resistance gene works in one of four ways:

| Mechanism | What the cell does | Example |
|---|---|---|
| Destroy the drug | An enzyme cuts or changes the drug | Beta-lactamase cuts penicillin |
| Change the target | The target protein changes shape, so the drug cannot bind | MRSA makes a cell-wall enzyme that penicillin-type drugs do not bind |
| Pump the drug out | A membrane pump removes the drug faster than it enters | Efflux pumps against tetracycline |
| Keep the drug out | The cell makes fewer entry channels in its outer membrane | Fewer porins against several drugs |

## What follows from this

- **Two drugs at once help.** <!-- claim: combination --> A cell needs two independent rare events: 10^-9 × 10^-9 = 10^-18 per cell. In 10^10 cells, that is 10^-8 expected cells, so effectively none. This fails if one plasmid carries both resistance genes.
- **Resistance is often a cost.** Without the drug, resistant cells often grow slower, so they stay rare. Every use of the drug gives them the advantage.

**Not covered here:** persister cells, which survive a drug without a resistance gene; and stress responses that raise mutation rates.
