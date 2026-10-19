# How bacteria become resistant to an antibiotic

**Short answer.** A single bacterium does not learn to resist a drug. A population becomes resistant through selection. A few cells already carry a gene that protects them. The antibiotic kills the other cells, and the protected cells multiply to replace them. The protective genes come from two sources: random copying errors (mutation) and genes passed from other bacteria (gene transfer).

This matters in practice. An infection can improve on treatment and then return, and the drug no longer works on the bacteria that come back.

The rest of this file builds that answer in four steps. It shows how a drug kills a cell, how a cell can block the drug, where the blocking genes come from, and how the drug itself makes those genes common.

## 1. How an antibiotic kills a cell

An antibiotic is a molecule that binds to a **target**: a part of the bacterial cell that the cell needs to live or divide. Two examples:

- Penicillin binds the enzymes that build the cell wall. The wall weakens, and the cell bursts.
- Streptomycin binds the ribosome, the machine that makes proteins. The cell makes faulty proteins and dies.

Human cells do not have these exact targets, so the drug harms bacteria much more than it harms the patient.

To work, the drug must do three things: get into the cell, stay intact, and bind its target.

## 2. How a cell blocks the drug

Each of those three requirements can fail. Each failure is a resistance **mechanism**, and a gene controls each one.

| Requirement | How the cell blocks it | Example |
|---|---|---|
| Get in | Make fewer entry channels in the outer membrane | Fewer porin channels in *E. coli* |
| Get in (and stay in) | Pump the drug out faster than it enters (an **efflux pump**) | Tetracycline pumps |
| Stay intact | Make an enzyme that destroys the drug | Beta-lactamase cuts penicillin |
| Bind the target | Change the target shape so the drug no longer fits | A changed ribosome protein blocks streptomycin |

Resistance is usually a matter of degree, not all or nothing. Microbiologists measure it as the **MIC** (minimum inhibitory concentration): the lowest drug concentration that stops a strain from growing. A low MIC, such as 1 mg/L, means a little drug stops the strain. A high MIC, such as 64 mg/L, means the strain grows at drug levels that a patient's blood may never safely reach. "Resistant" means the MIC is above the level that treatment can achieve.

## 3. Where the resistance genes come from

### Mutation

Each time a bacterium copies its DNA to divide, it makes rare errors. Most errors do nothing or cause harm. A few change a target or switch on a pump, and these give resistance.

Worked example (illustrative numbers; real rates vary by drug and species from about 1 in a million to 1 in 10 billion per division):

- A serious infection contains about 10¹⁰ bacteria (estimate).
- To grow from one cell to 10¹⁰ cells takes about 10¹⁰ cell divisions.
- Suppose a specific resistance mutation occurs once per 10⁸ divisions.
- Expected resistant cells: 10¹⁰ × 1/10⁸ = **about 100**, present *before* the first dose.

So in a large population, resistant cells usually already exist. The drug does not create them.

The obvious alternative idea is that the drug makes bacteria change to survive. Luria and Delbrück tested this in 1943. They grew many separate cultures and then exposed them to a killer (a virus, in their case). If the exposure caused resistance, every culture would have a similar, small number of survivors. Instead, most cultures had none and a few had hundreds. That pattern only fits mutations that happened at random times *before* exposure: an early mutation has many generations to multiply, a late one has few.

### Gene transfer

Bacteria can also receive resistance genes that evolved in other bacteria. This is **horizontal gene transfer**: genes move between living cells, not only from parent to offspring. There are three routes:

- **Conjugation:** one cell passes a **plasmid** (a small, separate DNA circle) to another through direct contact.
- **Transformation:** a cell takes up free DNA from a dead cell nearby.
- **Transduction:** a virus that infects bacteria carries a piece of DNA from one cell to the next.

Gene transfer is the main reason resistance spreads fast in hospitals. One plasmid can carry genes for several mechanisms, so one transfer event can make a cell resistant to several drugs at once. Transfer also crosses species: a harmless gut bacterium can give a gene to a dangerous one.

## 4. How the drug makes resistance common

Return to the infection with 10¹⁰ bacteria, of which about 100 are resistant. That is 1 resistant cell in 100 million.

Treatment starts. The drug kills the susceptible cells. Suppose the immune system and the drug together reduce them to about 10⁴ within two days. The 100 resistant cells are not affected by the drug. Suppose they double once per hour in the body (estimate). After one day, which is 24 doublings:

100 × 2²⁴ ≈ 100 × 1.7 × 10⁷ ≈ **1.7 × 10⁹ resistant cells**

The resistant fraction has gone from 1 in 100 million to nearly 100%. No cell changed. The drug removed the competition. This is natural selection, and it runs fast because bacteria divide in hours, not years.

### Dose controls which cells survive

Suppose the susceptible strain has an MIC of 1 mg/L and a partly resistant mutant has an MIC of 8 mg/L (illustrative).

- At **16 mg/L**, the drug stops both strains. Nothing is selected.
- At **4 mg/L**, the drug stops the susceptible strain but not the mutant. This concentration selects for resistance most strongly.
- At **0.5 mg/L**, the drug stops neither. It selects only weakly.

The range between the two MICs is the **mutant selection window**. Low doses, missed doses, and drug levels that fall slowly after a course all keep bacteria in this window. This is one reason a prescribed course has a set dose and length. It is also why some treatments use two drugs at once: a cell would need two independent mutations, about 1 in 10⁸ × 1 in 10⁸ = 1 in 10¹⁶ divisions, which is larger than the whole infection.

### What happens when the drug is removed

Resistance often has a cost. A pump uses energy, and a changed target can work less well. Suppose a resistant strain grows 5% slower per generation than the susceptible strain. Without the drug, after 100 generations its share falls by a factor of 0.95¹⁰⁰ ≈ 0.006, about 170 times. In this case, stopping use of the drug makes resistance rare again.

That reversal often fails in practice. Resistant strains acquire further **compensatory mutations** that remove most of the cost but keep the resistance. Some resistance genes cost almost nothing from the start. Then resistance stays in the population for years after the drug is no longer used.

## Summary

Bacteria become resistant to an antibiotic in two steps. First, variation: a few cells carry a gene that keeps the drug out, pumps it out, destroys it, or changes its target. These genes arise from random mutation or arrive by gene transfer from other bacteria. Second, selection: the drug kills the cells without the gene, and the cells with it multiply until they make up most of the population.

**Not covered here:** *tolerance* and *persistence* (cells that survive a drug by growing slowly, without a resistance gene), biofilms, and the spread of resistant bacteria between people and animals.
