# Narrative: vaccine-memory

## 1. Reader before and after

- **Before:** A technical reader: school science (cells, DNA, genes, proteins with shapes, exponential growth) and basic programming. Knows "immune system" and "antibody" only as everyday words. Does not know lymphocyte, receptor, antigen, clone, memory cell, adjuvant.
- **After:** "My body already holds, by chance, a few cells that fit almost any germ; a vaccine makes those few multiply once, safely, and leaves many more of them behind, so the real infection is stopped in about 3 days instead of about 7."

## 2. Question and motive

- **Question:** How can a vaccine prepare the body for a disease it has never met? Result in words: the vaccine does not teach a shape. The body already has a matching cell by chance. The vaccine multiplies it once, safely, and the extra cells stay.
- **Why care:** It sounds impossible: the body cannot know the shape of a virus that evolved last year.
- **Why this approach:** Treat infection as a race between two exponential growths. Then ask what changes the result of the race.

## 3. Introduction ledger

| Reference | Means | Grounded by | Beat |
|---|---|---|---|
| pathogen | virus or bacterium that multiplies and causes disease | 100 particles, ×10 per day | 2 |
| antigen | molecular shape on the pathogen that a receptor binds | the spike protein of SARS-CoV-2 | 3 |
| lymphocyte | white blood cell (B or T cell) carrying one kind of receptor | — one cell, one receptor kind | 3 |
| receptor | binding protein on a lymphocyte, made at random | >100 million kinds in one person | 3 |
| clone | a lymphocyte and its descendants, same receptor | 100 cells → 1,000,000 | 4 |
| clonal selection | antigen makes only matching lymphocytes divide | 100 of 100 million kinds divide | 4 |
| effector cell | activated lymphocyte that fights now | plasma cell, killer T cell | 4 |
| antibody | released copy of a B cell receptor | thousands per second from one plasma cell | 4 |
| precursor count | lymphocytes able to respond at the start | 100 naive vs 10,000 memory | 5 |
| memory cell | long-lived lymphocyte left after a response | 10,000 = 1% of 1,000,000 | 6 |
| danger signal / adjuvant | second signal "this is a threat" / vaccine ingredient giving it | food proteins do not trigger a response | 7 |

## 4. Beats

| # | Kind | Reader's question | Bridge | Shown | Said | Reader now knows |
|---|---|---|---|---|---|---|
| 1 | hook | How can it prepare for something unknown? | — | answer in bold | "The vaccine does not teach the body a new shape. The body already has a few cells that fit it, made at random. The vaccine makes those cells multiply once, without the disease, and many of them stay. So the next time, the body controls the germ in about 3 days instead of about 7." | the result, in words |
| 2 | approach | What decides if I get sick? | so | pathogen numbers | "A pathogen (a virus or bacterium) multiplies in the body. Illustrative: it starts at 100 particles and grows 10× per day; symptoms start above 100 million particles. Immune cells multiply too. Whichever side gets big enough first wins: infection is a race between the pathogen's growth and the immune cells' growth." | the race and both runners |
| 3 | mechanism | Which immune cells, and how can one fit an unknown germ? | but | library numbers | "A lymphocyte is a white blood cell with one kind of receptor: a protein that binds one family of similar molecular shapes. The shape it binds on a pathogen is an antigen (e.g. the spike protein of a coronavirus). Each new lymphocyte assembles its receptor by joining gene pieces at random, so one person has more than 100 million kinds. The ~20,000 genes could not list them one by one. Because each receptor fits a family of shapes, and a pathogen shows many antigens, a few lymphocytes fit almost any new pathogen by chance." | lymphocyte, receptor, antigen; the library exists in advance |
| 4 | mechanism | What happens when the antigen arrives? | so | clone arithmetic | "Only the lymphocytes whose receptors bind the antigen activate (clonal selection). For one antigen, about 1 in 100,000 to 1 in 1,000,000 lymphocytes fit: illustrative, 100 cells. Each divides every 8 hours. A clone is a cell and all its descendants, with the same receptor. The clone's cells become effector cells: plasma cells release antibodies (free copies of the receptor), killer T cells kill infected cells. Each effector cell removes many particles, so about 1,000,000 effector cells (illustrative) clear the pathogen faster than it grows." | clonal selection, clone, effector cell, antibody, target 1,000,000 |
| 5 | mechanism | Why is the first time slow? | but | 100 × 2^n = 1,000,000; 7 days; 1 billion particles | "Here n is the number of divisions: 100 × 2^n = 1,000,000 gives n ≈ 13.3, which is 4.4 days at 8 hours each. Finding the antigen and activating take about 2.5 days more: about 7 days. By then the pathogen is at 100 × 10^7 = 1 billion particles, above the 100-million symptom level: the person is sick." | primary response |
| 6 | mechanism | What is left after? | therefore | 99% die, 1% stay: 10,000 | "After the pathogen is gone, about 99% of the effector cells die. About 1% stay for years as memory cells: 10,000, which is 100× the original 100. Next time, 10,000 × 2^n = 1,000,000 gives n ≈ 6.6 divisions, 2.2 days; memory cells also activate in under a day: about 3 days. The pathogen reaches only 100,000 particles, 1,000× below the symptom level." | memory cell, secondary response |
| 7 | name | So what does the vaccine do? | therefore | vaccine = antigen + adjuvant, no disease | "A vaccine contains the antigen, or instructions to make it, but no pathogen that can multiply to disease. It also needs a danger signal: lymphocytes activate only if other immune cells also signal 'threat'; this stops attacks on harmless food proteins. The vaccine ingredient that gives this signal is an adjuvant. So the vaccine runs the slow first response (beats 4–6) safely, and leaves the memory cells." | the answer |
| 8 | objection | When does it fail? | but | flu vs measles | "Memory works only for the same antigen. Influenza changes its surface antigens each year, so old receptors fit poorly and the response falls back toward the slow first one; flu vaccines prevent about 40–60% of cases and are updated yearly. Measles antigens stay the same: two doses prevent about 97% of cases for decades." | limit |
| 9 | close | — | so | recap | answer in the opening words; each 2× more precursors saves one 8-hour division | after-sentence |

## 5. Concrete to symbol

100 × 2^n = 1,000,000 → n ≈ 13.3. Said: "here n is the number of divisions". 10,000 × 2^n = 1,000,000 → n ≈ 6.6.

## 6. Links between representations

One table: first meeting vs vaccinated, same rows (precursor count, divisions, days, pathogen peak, sick?).

## 7. Close the loop

- **Answer:** A vaccine prepares the body by running the slow first response safely, so the cells that fit are already many when the disease arrives.
- **General argument:** Memory cuts the precursor gap; each 2× more precursors saves one 8-hour division.
- **Payoff:** Predict when a vaccine will fail (antigen change) and why boosters or yearly updates exist. Scope pointers.
