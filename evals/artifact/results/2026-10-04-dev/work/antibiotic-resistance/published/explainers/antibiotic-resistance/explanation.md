# How do bacteria become resistant to an antibiotic?

<!-- Stage 1, rendered from model.md in STE-80. -->

**The drug does not change the bacteria. In a large infection, a few bacteria already carry a resistance gene, made by a random copying error or received from another bacterium. The drug removes the susceptible bacteria around them, and the resistant bacteria multiply.** The bacteria become resistant, not the patient's body.

## What a cell must block

An antibiotic is a molecule that kills bacteria or stops their growth. It does this by binding a **target**: a molecule the cell needs. For example, penicillin binds the enzymes that build the cell wall.

A **resistance gene** is a gene, changed by mutation or received from another bacterium, that blocks this. It works in one of four ways: <!-- claim: mechanisms -->

| Way | Example |
|---|---|
| Destroy the drug | A beta-lactamase enzyme cuts penicillin before penicillin reaches its target. |
| Change the target | One DNA letter change alters the target protein, so rifampicin no longer binds. |
| Pump the drug out | An efflux pump, a membrane protein, exports tetracycline faster than it enters. |
| Keep the drug out | The cell loses a porin, an entry channel in its surface, so less drug gets in. |

Each way means the cell needs more drug to stop it. The lowest concentration that stops a strain's growth is its **MIC** (minimum inhibitory concentration). <!-- claim: mic --> Suppose a drug reaches 8 mg/L in the blood. A strain with an MIC of 0.5 mg/L is stopped: it is **susceptible**. A strain with an MIC of 32 mg/L grows: it is **resistant**. (Illustrative values.)

## Resistant cells are there before the drug

A given resistance mutation (a mutation that turns a normal gene into a resistance gene) happens about once per 10⁸ cell divisions. <!-- claim: preexisting --> A serious infection can hold 10¹⁰ cells. Each division adds one cell, so growing to that size took about 10¹⁰ divisions. Expect

10¹⁰ × 10⁻⁸ = **100** resistance mutations, before anyone gives a drug.

Early mutants have divided since, so there are at least 100 resistant cells. Compare a small infection of 10⁶ cells: it expects 0.01 mutations, so there is only about a 1% chance that even one resistant cell exists.

## The drug selects them

<!-- claim: selection-not-induction -->
1. The drug stops the susceptible cells: it kills them or halts their growth, and the immune system clears the halted cells.
2. The resistant cells keep dividing. The immune system removes some, but alone it cannot keep up with a population that keeps doubling. The drug did most of the work.
3. 100 cells need **27** doublings to reach 10¹⁰ again (100 × 2²⁷ ≈ 100 × 1.3 × 10⁸ ≈ 10¹⁰). At a lab doubling time of 30 minutes, that is 13 hours.
4. The infection returns, and almost every cell is resistant.

This is **selection**: the drug did not make resistant cells, it removed the susceptible cells.

**How do we know the drug did not cause the change?** If exposure caused resistance, each cell would have the same small chance when it met the drug. Equal cultures would then give similar counts. Luria and Delbrück tested this in 1943. They used a virus that kills bacteria; the test asks only whether resistance arose before contact, so it applies to drugs too. They grew 20 equal cultures of bacteria, then exposed each one and counted the resistant colonies. The mean was about 11. For independent rare events with a mean of 11, the random scatter is about √11 ≈ 3.3, so the "drug causes it" idea predicts most cultures between 5 and 18. They found 11 cultures with 0 and one with **107**. Random mutation before exposure explains this spread: a mutant that appears early leaves many resistant descendants, and a late one leaves few.

## Genes from other bacteria

<!-- claim: hgt -->
A cell does not have to wait for its own rare mutation. A **plasmid** is a small circle of DNA, separate from the chromosome. In **conjugation**, two bacteria touch and one copies a plasmid into the other. This is **horizontal gene transfer**: a gene from another bacterium, not from the parent cell.

Plasmids carry complete working genes, such as the beta-lactamase gene, which one letter change could never build. The same plasmid gene turns up in different species, which shows that the gene moved between them. One plasmid often carries several resistance genes at once.

## Without the drug, resistance usually costs

<!-- claim: takeover-needs-drug -->
Resistant cells take over only while the drug is present. Without the drug, resistance often has a **fitness cost**: the extra protein, or the changed target, makes the cell grow more slowly.

Suppose resistant cells grow 5% slower: each time the susceptible cells double, the resistant cells grow only 0.95 times as much. So each doubling multiplies the ratio of resistant to susceptible cells by 0.95. The effect compounds: after 100 doublings the ratio is 0.95¹⁰⁰ ≈ **0.006** of its start value.

But resistance rarely vanishes, for two reasons:

- A **compensatory mutation** is a second change, in another gene, that restores growth; the first change and the resistance stay. If it cuts the cost to 1%, then 0.99¹⁰⁰ ≈ 0.37 of the ratio remains after 100 doublings.
- Plasmids persist. One plasmid often carries resistance genes for several drugs, so any one of those drugs still selects the whole plasmid.

## What this predicts

- Large infections are the risk, because they hold resistant cells before treatment.
- <!-- claim: combination --> Two drugs with independent targets need two mutations in one cell. The two are independent events, so their chances multiply: 10⁻⁸ × 10⁻⁸ = 10⁻¹⁶. In 10¹⁰ cells, expect 10⁻⁶ such cells: a one-in-a-million chance. The treatment clears the infection. This fails if one event gives resistance to both drugs, for example one plasmid with both genes, or one pump that exports both molecules. Then about 100 cells survive again.

**In short:** resistance genes come first, by chance or from other bacteria. The drug removes the susceptible cells, and the resistant cells multiply.

## Not covered

- Persister cells, which survive a drug without a resistance gene ("antibiotic persistence").
- Other routes of gene transfer: transformation and transduction.
- Drugs that raise the mutation rate ("SOS response").
- Course length, prescribing policy, farm use, biofilms.
