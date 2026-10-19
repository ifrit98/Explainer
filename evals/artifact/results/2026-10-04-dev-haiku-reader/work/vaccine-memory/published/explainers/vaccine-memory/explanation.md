# How does a vaccine prepare the immune system for a disease it has never met?

<!-- Stage 1, rendered from model.md in STE-80. -->

**A vaccine does not teach the body a new shape. The body already has a few cells that bind the virus or bacterium, made at random long before. The vaccine makes those few cells multiply once, without the disease, and many of their descendants stay. So when the real infection arrives, the body controls it in about 3 days instead of about 7.**

Numbers marked *illustrative* are round numbers that show the mechanism; real values vary by disease and person.

## Infection is a race

A **pathogen** is a virus or bacterium that multiplies in the body and causes disease. Illustrative: an infection starts with 100 particles, the pathogen grows 10× per day, and symptoms start above 100 million particles.

Immune cells also multiply. The body **controls** the infection when its immune cells remove the pathogen faster than the pathogen grows. So ask: what does a vaccine change in this race?

## The matching cells exist before the pathogen does

<!-- claim: library-before -->
A **lymphocyte** is a white blood cell that carries many copies of one kind of **receptor**. A receptor is a protein that binds one family of similar molecular shapes. The shape that a receptor binds on a pathogen is an **antigen**; for example, the spike protein on the surface of a coronavirus.

Each new lymphocyte builds its receptor by joining pieces of genes in a random combination and adding random edits at the joins. So one person carries more than 100 million different receptors (estimate). One gene per receptor is impossible: humans have about 20,000 genes, and no gene list could anticipate a virus that evolved last year.

Because each receptor binds a family of shapes, and a pathogen shows many different antigens, a few lymphocytes bind almost any new pathogen by chance.

<!-- claim: selection-not-instruction -->
This is the central idea. The body does not design a receptor after it sees the pathogen. The pathogen selects from a random library that already exists.

## The first meeting is slow

<!-- claim: clonal-selection -->
When an antigen arrives, only the lymphocytes whose receptors bind it activate and divide. This is **clonal selection**. A **clone** is one lymphocyte and all its descendants; they share the same receptor.

For one antigen, about 1 in 100,000 to 1 in 1,000,000 lymphocytes bind it (estimate). Illustrative: 100 cells. Call this number the **precursor count**: the lymphocytes able to respond at the start. Each activated cell divides about every 8 hours.

<!-- claim: fewer-beats-more -->
The clone's cells become **effector cells**, which fight now. Some release **antibodies**: free copies of their receptor that stick to the pathogen and block it. Others kill infected cells. One effector cell can release thousands of antibodies per second, so the response does not need as many cells as the pathogen has particles. Illustrative: 1,000,000 effector cells control the pathogen. For simplicity, both cases below use this one target.

<!-- claim: primary-slow -->
How long does the first response take? Let n be the number of divisions. Then 100 × 2^n = 1,000,000, so 2^n = 10,000 and n ≈ 13.3. At 8 hours each, that is 4.4 days. The rare matching cells also need about 2.5 days to meet the antigen and activate. Total: about 7 days. This first response is the **primary response**. In 7 days the pathogen grows from 100 to 100 × 10^7 = 1 billion particles. That is above the symptom level of 100 million, so the person is sick.

## What stays behind

<!-- claim: memory-fast -->
After the pathogen is gone, about 99% of the effector cells die. About 1% stay for years or decades as **memory cells**. Illustrative: 1% of 1,000,000 is 10,000 memory cells, which is 100× the original precursor count of 100.

At the next meeting with the same antigen, 10,000 × 2^n = 1,000,000 gives 2^n = 100, so n ≈ 6.6 divisions, or 2.2 days. Memory cells already wait in the tissues and need less stimulation, so they activate in under a day. Total: about 3 days. This faster response, which starts from memory cells, is the **secondary response**.

| | First meeting | Same antigen again |
|---|---|---|
| Precursor count | 100 | 10,000 |
| Divisions to reach 1,000,000 | 13.3 | 6.6 |
| Days to control | about 7 | about 3 |
| Pathogen peak (from 100, ×10 per day) | 1 billion | 100,000 |
| Above 100 million (symptoms)? | yes | no, 1,000× below |

The rule behind the table: each doubling of the precursor count saves one division, which is 8 hours.

## What the vaccine does

<!-- claim: vaccine-role -->
A **vaccine** contains the antigen, or instructions for the body's cells to make it. It contains no pathogen that can multiply to disease. So the vaccine runs the slow first response while nothing is growing, and leaves the memory cells behind. When the real pathogen comes, the race starts with the secondary response, not the primary one.

<!-- claim: why-adjuvant -->
Antigen alone is often not enough. A lymphocyte activates only when it binds its antigen *and* receives a **danger signal** from other immune cells that sense a threat. This rule stops attacks on harmless shapes such as food proteins. A purified protein alone gives no danger signal and often only a weak response. So many vaccines contain an **adjuvant**: an ingredient that triggers the danger signal.

## When memory does not help

Memory cells bind only the antigen that made them. Measles keeps the same antigens: two doses of measles vaccine prevent about 97% of cases, for decades. Influenza changes its surface antigens from year to year. The old memory receptors bind poorly, so the response falls back toward the slow first one. That is why flu vaccines prevent only about 40–60% of cases in a typical season and are updated every year. The cause is a changed antigen, not memory cells that wear off.

A vaccine does not stop the pathogen from entering. It shortens the race.

## Summary

A vaccine prepares the body for a disease it has never met because the body does not need to have met it: the matching lymphocytes already exist by chance. The vaccine runs the slow primary response safely, so the real infection meets a secondary response that starts with 100× more cells.

**Not covered here:** how receptors improve their fit over weeks (affinity maturation), how T cells help B cells, how antibody levels fall over months and why some vaccines need boosters, the types of vaccine (live, inactivated, protein, mRNA), and herd immunity. A standard textbook such as *Janeway's Immunobiology* covers each.
