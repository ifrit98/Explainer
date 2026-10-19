# Model: vaccine memory

## Central question
How does a vaccine prepare the immune system for a disease it has never met?

## Answer in one line
The immune system does not design a defense after it sees a pathogen. It already holds a huge random library of receptor shapes. A vaccine shows harmless pathogen shapes, and the few cells that match them multiply and leave a large, long-lived memory pool.

## Reader
Technical, school science, new to immunology. Knows cells divide, proteins have shapes, exponential growth.

## Entities
- Antigen: a molecular shape on a pathogen that a receptor can bind.
- Lymphocyte: white blood cell with one receptor shape. B cells (make antibodies) and T cells (kill infected cells, help B cells).
- Antibody: soluble copy of a B-cell receptor; binds antigen and blocks or marks the pathogen.
- Memory cell: lymphocyte left after a response; more numerous and faster to activate than the naive precursor.
- Long-lived plasma cell: B-cell descendant in bone marrow; secretes antibody for years.
- Adjuvant / danger signal: innate-immune activation that tells lymphocytes the antigen matters.

## Causal chain
1. Random gene recombination makes each new lymphocyte carry a random receptor. Self-reactive ones are mostly removed.
2. Vaccine delivers antigen + danger signal.
3. Matching rare cells (~1 per 10^5–10^6, estimate) bind antigen and are activated (clonal selection).
4. Activated cells divide every ~8 h (clonal expansion).
5. B cells mutate receptors and the better binders are selected (affinity maturation).
6. Antigen is gone; ~90–95% of the expanded cells die (contraction); 5–10% stay as memory.
7. Real infection: memory pool is ~1000x larger and pre-tuned; preexisting antibody acts at once.

## Worked numbers (illustrative)
- 100 naive matching cells, 15 doublings (5 days) → ~3.3 million; keep 5% → ~164,000 memory cells.
- Re-expansion to 3.3 million from 164,000 needs ~4.3 doublings ≈ 1.5 days, vs 5 days.
- Virus race: 100 particles doubling every 8 h → ~51,000 at day 3, ~2×10^8 at day 7.

## Why each step
- Why a library and not design: receptors are made before exposure; no mechanism builds a receptor from the antigen.
- Why a danger signal: antigen alone is often ignored (tolerance); purified protein without adjuvant gives weak responses.
- Why harmless: inactivated, attenuated, protein subunit, mRNA, or viral vector give the shape without the disease.
- Why boosters: a second exposure expands memory further and adds affinity maturation.

## Failure case
Memory binds specific shapes. Influenza changes its surface protein (antigenic drift); old antibodies bind poorly; new vaccine each year. Antibody levels also wane over time.

## Confusion points
- "The vaccine teaches the body": no, it selects from what exists.
- Random library would attack self: developmental deletion (tolerance) removes most self-reactive cells.
- Memory does not always prevent infection; often it prevents severe disease.

## Epistemic labels
- Precursor frequencies, % surviving contraction, division times: estimates, vary by antigen and person.
- Virus race numbers: illustrative model.

## Scope (left out)
Antigen presentation (MHC) detail, herd immunity, side effects, specific vaccine schedules.
