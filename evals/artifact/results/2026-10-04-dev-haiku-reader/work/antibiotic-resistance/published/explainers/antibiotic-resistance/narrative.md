# Narrative: antibiotic-resistance

> Pass 3. `model.md` says what is true. This file says the path a first-time reader takes to it.

## 1. Reader before and after

- **Before:** a technical reader (school science and mathematics, basic programming) who knows cells, genes, mutation, exponential growth, and natural selection in outline, and nothing of how antibiotics act or how bacteria exchange genes.
- **After:** "Resistance genes appear at random or arrive from other bacteria before the drug; the drug removes the susceptible cells, so the resistant ones are left to multiply."

## 2. Question and motive

- **Question:** How does an infection that a drug used to clear become one it cannot clear? Result in words first: the drug does not change the bacteria. A few bacteria already carry a resistance gene; the drug removes their competitors.
- **Why care:** the common picture ("bacteria get used to the drug") predicts the wrong things: that resistance appears in every infection, that it needs the drug to arise, and that it is in the patient.
- **Why this approach:** start from what the drug does to one cell, because resistance is a way to block that. Then count: how many cells could already have a resistance gene? The count is the surprise.

## 3. Introduction ledger

| Reference | Means | Grounded by (a concrete instance) | Beat |
|---|---|---|---|
| target | the molecule the antibiotic binds | penicillin binds the enzymes that build the cell wall | 2 |
| resistance gene | gene, mutated or gained, that lets the cell grow in the drug | beta-lactamase gene | 3 |
| beta-lactamase, efflux pump, porin, rpoB | the four mechanism examples | one row each in the table | 3 |
| MIC | lowest concentration that stops a strain's growth | 0.5 vs 32 mg/L against 8 mg/L in blood | 3 |
| resistant / susceptible | grows / stopped at the concentration reached | the two MIC strains | 3 |
| mutation rate per division | chance that one division makes this mutation | 10^-8 | 4 |
| selection | drug removes susceptible cells, resistant fraction rises | 100 survivors regrow | 5 |
| doubling | every cell divides once | 100 → 10^10 in 27 doublings | 5 |
| Luria–Delbrück | the experiment that separates selection from induction | 20 cultures, 0 to 107 | 6 |
| plasmid, horizontal gene transfer, conjugation | gene from another bacterium | beta-lactamase gene on a plasmid in different species | 7 |
| fitness cost, compensatory mutation | slower growth without drug; a second mutation that reduces it | 0.95^100 ≈ 0.006; 0.99^100 ≈ 0.37 | 8 |

## 4. Beats

| # | Kind | Reader's question | Bridge | Shown | Said | Reader now knows |
|---|---|---|---|---|---|---|
| 1 | hook | How does an infection that a drug used to clear become one it cannot clear? | — | the question as title, bold answer | The drug does not change the bacteria. A few bacteria already carry a resistance gene, by chance or from other bacteria; the drug removes their competitors, and they multiply. The bacteria are resistant, not the patient's body. | the answer |
| 2 | mechanism | What does a drug do to a cell? | so, to resist, a cell must block this | — | An antibiotic binds a target, a molecule the cell needs: penicillin binds the enzymes that build the cell wall. | target |
| 3 | mechanism | How can a cell stop that? | therefore | table: four ways, each with one example in words | Destroy the drug (beta-lactamase enzyme cuts penicillin); change the target so the drug no longer fits (one letter in rpoB, rifampicin); pump it out (efflux pump); keep it out (lose a porin, an entry channel). Each way means a higher concentration is needed to stop growth. That concentration is the MIC, minimum inhibitory concentration. Blood reaches about 8 mg/L: a strain with MIC 0.5 is stopped (susceptible), a strain with MIC 32 grows (resistant). | mechanisms, MIC, resistant |
| 4 | instance | Where does a resistance gene come from in an infection that never met the drug? | but the drug was never there… | arithmetic | A copying error at one division makes a given resistance mutation about once per 10^8 divisions. An infection of 10^10 cells took about 10^10 divisions to grow, so expect 10^10 × 10^-8 = 100 mutations. Early mutants have divided since, so resistant cells number at least 100. An infection of 10^6 cells expects 0.01 mutations: about a 1% chance that even one resistant cell exists. | variants exist before the drug |
| 5 | mechanism | What does the drug do to that mix? | so | numbered steps | The drug stops the susceptible cells; the immune system clears those, but it does not keep up with a population that doubles. The 100 resistant cells divide: 27 doublings (every cell divides once) take them back to 10^10, about 13 hours at a lab doubling time of 30 min. This is selection. | selection |
| 6 | objection | How do we know the drug did not cause the change? | but | the numbers of one experiment | If the drug caused the change (induction), each cell would have the same small chance when exposed, so equal cultures would show similar counts. Luria and Delbrück (1943) grew 20 equal cultures and then exposed them; mean 11 resistant colonies, so induction predicts most cultures between 5 and 18. They found 11 cultures with 0 and one with 107. An early mutant leaves many descendants, a late one few: that spread means the mutations happened before exposure. | evidence |
| 7 | generalize | Must every lineage wait for its own rare mutation? | but | — | A plasmid is a small circle of DNA, separate from the chromosome. In conjugation, two bacteria touch and one copies a plasmid into the other. So a cell gets a complete working gene, such as the beta-lactamase gene, in one step, even from another species. One letter change cannot build a whole new enzyme; this is how such genes spread. | second source |
| 8 | test | Does resistance stay after the drug stops? | therefore: takeover needs the drug | numbers | Resistance often has a fitness cost: the extra protein or the changed target makes the cell grow slower when there is no drug. With 5% slower growth, the ratio of resistant to susceptible cells is multiplied by 0.95 each generation: after 100 generations, 0.006. But a compensatory mutation (a second change that cuts the cost to 1%) gives 0.99^100 ≈ 0.37, so resistance can persist. | takeover needs the drug, and its limit |
| 9 | payoff | What does this predict? | so | two lines | Large infections are the risk, by the count in beat 4. Two drugs with independent targets need two mutations in one cell: 10^-8 × 10^-8 = 10^-16, so 10^10 cells expect 10^-6. This fails if one plasmid or pump resists both: 100 survivors again. | predictions |
| 10 | close | — | — | — | Resistance genes come first, by chance or from other bacteria; the drug removes the competitors; the resistant cells multiply. A short "not covered" list follows, outside the argument. | — |

## 5. Concrete to symbol

Expected count = cells × rate: "here 10^10 cells and 10^-8 per division give 100". Checked at 10^6 → 0.01.

## 6. Links between representations

The MIC numbers (0.5, 8, 32) appear in the table caption and in the definition of resistant.

## 7. Close the loop

- **Answer:** resistance genes come first, by chance or from other bacteria; the drug removes the competitors; the resistant cells multiply.
- **General argument:** any heritable variant that grows under the drug while others are stopped takes over while the drug is present.
- **Payoff:** predicts when resistance appears (large populations, single drugs, long use) and why it persists. Scope: persisters, other transfer routes, SOS mutagenesis, policy.
