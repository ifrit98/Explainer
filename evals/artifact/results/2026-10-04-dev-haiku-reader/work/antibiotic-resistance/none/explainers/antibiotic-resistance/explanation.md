# How bacteria become resistant to an antibiotic

## The short answer

Individual bacteria don't learn to resist a drug, and they don't adapt because they've been exposed to it. What happens is this:

1. **Variation already exists.** A large bacterial population almost always contains a few cells that differ genetically from the rest. They differ because of random mutations, or because they picked up genes from other bacteria. A few of those differences happen to make a cell harder to kill with a particular drug.
2. **The antibiotic does the selecting.** The drug kills or stops the susceptible cells. The resistant few survive, and they now have food and space to themselves.
3. **The survivors multiply.** Bacteria divide fast, so within hours or days the population is mostly made of the resistant type.

This is natural selection, and it runs fast because bacteria have huge populations and short generation times. The rest of this document explains each step, with rough numbers so you can see why it is so reliable.

---

## 1. How antibiotics work, briefly

An antibiotic is a molecule that interferes with something a bacterium needs and that our own cells either don't have or have in a different form. Common targets:

| Target | Example drugs | What goes wrong for the bacterium |
|---|---|---|
| Cell wall construction | penicillins, cephalosporins (β-lactams); vancomycin | The wall is built badly, and the cell bursts under its own internal pressure |
| Ribosome (protein synthesis) | tetracyclines, macrolides, aminoglycosides | The cell can't make proteins, or makes faulty ones |
| DNA copying (DNA gyrase/topoisomerase) | fluoroquinolones such as ciprofloxacin | DNA gets tangled and broken |
| RNA polymerase | rifampicin | Genes can't be read |
| Folate synthesis (a metabolic pathway) | sulfonamides, trimethoprim | The cell can't make the building blocks for DNA |

Every one of these works the same basic way: the drug molecule has to **get into or onto the cell** and then **bind its target tightly enough** to jam it. That gives the bacterium several possible ways to resist.

## 2. What resistance looks like at the molecular level

A resistant bacterium has some trait that breaks that chain. There are five main strategies:

- **Destroy or disable the drug.** Some bacteria make enzymes that chemically inactivate the antibiotic. The best-known are the **β-lactamases**, which cut open the ring structure that penicillin-type drugs need in order to work. Other enzymes stick chemical groups onto aminoglycosides so they no longer bind the ribosome.
- **Change the target.** If the target's shape changes slightly, the drug no longer fits, but the target can still do its normal job. Examples: a single amino-acid change in RNA polymerase gives rifampicin resistance. A few changes in DNA gyrase give fluoroquinolone resistance. MRSA (methicillin-resistant *Staphylococcus aureus*) carries an extra cell-wall-building enzyme, PBP2a, that β-lactams barely bind.
- **Pump the drug out.** **Efflux pumps** are membrane proteins that push molecules out of the cell. If a cell makes more of them, or makes a version that recognises the drug, the drug's concentration inside the cell stays too low to work.
- **Keep the drug out.** Some bacteria (the "Gram-negative" group, such as *E. coli*) have an outer membrane with channels called porins. Losing or narrowing those channels slows the drug's entry.
- **Bypass the blocked step.** A cell can gain an alternative enzyme that does the same job but ignores the drug. Some trimethoprim-resistance genes work this way: they encode a different version of the enzyme the drug inhibits.

Resistance is usually a **matter of degree**. It is measured as the **MIC (minimum inhibitory concentration)**: the lowest drug concentration that stops the bacteria from growing in a lab test. A resistant strain has a higher MIC, sometimes slightly higher and sometimes thousands of times higher. In a clinic, a strain is labelled "resistant" when its MIC is above what can be safely reached in a patient's body.

## 3. Where the variation comes from

### 3a. Mutation (passed from parent to offspring)

Every time a bacterium copies its DNA, errors creep in. A typical rate is about 1 error per 10⁹–10¹⁰ base pairs copied. That is very accurate, but consider the numbers:

- A particular resistance-causing change, such as one specific letter in one specific gene, might arise roughly once per **10⁸–10⁹ cell divisions**. The exact figure varies a lot by gene and drug.
- A serious infection can contain **10⁹–10¹¹** bacteria. One millilitre of a dense lab culture has around 10⁹.

So a large population **very likely already contains** a few resistant mutants before any drug is given. The drug doesn't create them. It reveals them, by removing everyone else.

> Quick estimate: if 10¹⁰ cells exist and 1 in 10⁸ carries a resistance mutation, about 10¹⁰ / 10⁸ = **100 resistant cells** are present at the start of treatment.

This was shown directly in classic experiments in the 1940s and 50s (Luria–Delbrück, and the Lederbergs' replica plating). Resistant mutants turned up in cultures that had **never touched** the selecting agent. Their numbers also fluctuated from culture to culture in the way you'd expect if the mutations happened randomly at earlier times, rather than as a response to exposure.

Some antibiotics, and stress in general, can raise mutation rates somewhat. That speeds things up, but the basic logic of random variation followed by selection is unchanged.

### 3b. Horizontal gene transfer (getting genes from other bacteria)

Bacteria can also acquire **ready-made resistance genes** from other bacteria, even from different species. This is a major reason resistance spreads so fast in hospitals. There are three main routes:

- **Conjugation.** One cell builds a bridge to another and passes over a **plasmid**: a small, circular piece of DNA, separate from the main chromosome, that can copy itself. Plasmids often carry several resistance genes together.
- **Transformation.** Some bacteria can take up loose DNA from their surroundings, for example DNA released by dead cells, and stitch it into their own genome.
- **Transduction.** Viruses that infect bacteria (**bacteriophages**) sometimes accidentally package a piece of bacterial DNA and deliver it to the next cell they infect.

Within a genome, **transposons** ("jumping genes") and **integrons** (gene-capture systems) let resistance genes move between chromosome and plasmid and gather into clusters. As a result, one transfer event can make a cell resistant to several drug classes at once.

If you program, here is a loose analogy. Mutation is like random bit-flips in your own source code. Horizontal transfer is like importing a tested library someone else already wrote.

## 4. Selection: why the resistant cells take over

With no drug present, resistant and susceptible cells grow at similar rates. Resistant ones are often slightly *slower* (see section 6). Add the drug and the picture flips.

### A toy calculation

Suppose:

- Start of treatment: 10¹⁰ susceptible cells and 100 resistant cells.
- The drug kills susceptible cells quickly, so their numbers fall about 10-fold every hour or two.
- Resistant cells keep dividing every ~30 minutes, which means doubling twice per hour.

After 10 hours:

- Susceptible: 10¹⁰ shrinks to roughly 10⁵ or fewer.
- Resistant: 100 × 2²⁰ ≈ 100 × 10⁶ = **10⁸**.

The population has gone from 1 resistant cell in 10⁸ to almost entirely resistant in less than half a day. It doesn't matter much how rare the resistant cells were to start with. Exponential growth makes up the difference quickly.

In a real infection, the immune system also kills bacteria and nutrients run out, so growth is slower than this. Often the immune system mops up the small number of resistant survivors. Resistance becomes a clinical problem when that doesn't happen: in severe infections, in people with weakened immune systems, or when resistant bacteria settle in and spread to other people.

### The "selection window"

Drug concentration matters, and in a way that isn't obvious. Let MIC_S be the susceptible strain's MIC and MIC_R the resistant strain's MIC.

- **Below MIC_S:** both types grow. The drug barely affects them, though even low concentrations can give resistant cells a slight edge.
- **Between MIC_S and MIC_R:** susceptible cells die and resistant cells grow. This range is the **mutant selection window**, and it is where resistance is selected most strongly.
- **Above MIC_R:** both types are suppressed. Resistance gains a foothold only if a cell gets a *second*, bigger resistance step.

Inside a patient, drug levels rise and fall between doses and differ from one tissue to another. So bacteria somewhere often spend time inside the window. A low dose that nevertheless kills the susceptible cells is the textbook recipe for selecting resistance.

The interactive page (`index.html`) lets you move the drug concentration through these zones and watch the effect.

## 5. Stepwise resistance

Often a single mutation gives only a small rise in MIC. Each extra mutation pushes the MIC higher: for example, one change in DNA gyrase, then a second, then a change that switches on an efflux pump. Each step lets the bacteria survive in a slightly higher concentration, where the next mutation can then be selected. Repeated or prolonged treatment can therefore climb a ladder from slightly resistant to highly resistant.

## 6. Why resistance doesn't simply disappear

Resistance often has a **fitness cost**. An altered target may work a bit less well, and running pumps or making extra enzymes uses energy. With no drug around, resistant cells may then be slowly outcompeted by susceptible ones.

In practice, though, resistance tends to stick around:

- **Compensatory mutations.** Later mutations can restore the lost growth rate *without* removing the resistance, so the cost shrinks to nearly zero.
- **Co-selection.** If a plasmid carries genes for resistance to drug A, drug B and a heavy metal, then using *any* of those keeps the whole plasmid around.
- **Low-cost mechanisms.** Some resistance genes cost very little from the start.
- **Ongoing exposure.** Antibiotics are used widely in medicine and in farming, and they turn up at low levels in the environment, so selection pressure rarely stops completely.

## 7. Related ideas that are *not* resistance

- **Tolerance.** The bacteria die more *slowly* under the drug, but the MIC doesn't change. Slow-growing or dormant cells are often tolerant, because many antibiotics attack processes that are only busy in actively growing cells.
- **Persistence.** A small fraction of genetically identical cells happen to be dormant when the drug arrives. They survive, then regrow into a population that is just as susceptible as before. Persisters can lead to infections that keep coming back, and they give resistance mutations more time and more chances to appear.
- **Biofilms.** Communities of bacteria stuck to a surface inside a slimy matrix. Drugs penetrate them poorly and many of the cells grow slowly, so biofilms survive treatment even without resistance genes.

## 8. What this implies

The mechanism suggests these strategies:

- **Use antibiotics only when they're needed.** Every use selects for resistance somewhere, including among the harmless bacteria in your gut, which can later pass genes to harmful ones.
- **Use enough drug, for a suitable time.** The goal is to get above the selection window and clear the infection. The best course length is still being researched. For many infections, shorter courses turn out to work as well as longer ones, and the old blanket rule "always finish the course" is now debated. Follow the prescriber's advice for your situation.
- **Combine drugs, sometimes.** If resistance to drug A arises in roughly 1 in 10⁸ cells, and resistance to drug B in roughly 1 in 10⁸, then a cell resistant to both by chance is about 1 in 10¹⁶, more cells than are in the infection. This is why tuberculosis and HIV are treated with combinations.
- **Stop transmission.** Hand hygiene, infection control and sanitation stop resistant strains spreading from person to person, which matters as much as how the drugs are used.

## Summary

- Bacterial populations are huge and varied. Random mutation and gene swapping mean a few cells are already resistant before any drug is given.
- Resistance mechanisms work in one of five ways: break the drug, change the target, pump the drug out, keep the drug out, or bypass the blocked step.
- The antibiotic doesn't cause resistance. It **selects** for it, by removing the competition. Exponential growth then turns a handful of survivors into the whole population.
- Drug concentrations between the susceptible and resistant MICs select resistance most strongly.
- Fitness costs, compensatory mutations and co-selection decide whether resistance fades or persists once the drug is gone.
