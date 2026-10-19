# Semantic model: how a vaccine prepares the immune system

> Source of truth. Every rendering derives from this file.

## Central question

How does a vaccine prepare the immune system for a disease it has never met?

## Audience and prior knowledge

A technical reader: school mathematics and science (cells, DNA and genes, proteins have shapes, exponential growth), basic programming (lookup, cache, random generation). New to immunology. Does not know: antigen, lymphocyte, receptor, clone, antibody, memory cell, adjuvant, primary/secondary response.

## Entities

| Entity | Definition (one sentence) | Status |
|---|---|---|
| pathogen | A virus or bacterium that multiplies in the body and causes the disease. | fact |
| antigen | A molecular shape on a pathogen (usually part of a surface protein) that a receptor can bind. | fact |
| lymphocyte | A white blood cell (B cell or T cell) that carries one kind of receptor, many copies of it. | fact |
| receptor | The protein on a lymphocyte surface that binds one antigen shape; each lymphocyte has a different, randomly generated receptor. | fact |
| naive lymphocyte | A lymphocyte that has not yet bound its antigen. | fact |
| clone | All lymphocytes descended from one lymphocyte; they share its receptor. | fact |
| clonal selection | Antigen activates only the lymphocytes whose receptors bind it; those multiply. | fact |
| effector cell | An activated lymphocyte that fights now: plasma cells release antibodies; killer T cells kill infected cells. | fact |
| antibody | A free-floating copy of a B cell receptor; it sticks to the antigen and blocks or tags the pathogen. | fact |
| memory cell | A long-lived lymphocyte left after a response, from an expanded clone, that responds fast to the same antigen. | fact |
| danger signal | A second signal from innate (built-in, non-specific) immune cells that says "this is a threat"; a lymphocyte needs it to activate. | fact (simplified) |
| adjuvant | An ingredient in a vaccine that triggers the danger signal. | fact |
| vaccine | A preparation that shows the antigen (and a danger signal) to the immune system without the pathogen's ability to cause disease. | fact |
| primary response | The response to an antigen met for the first time; it starts from naive lymphocytes. | fact |
| secondary response | The response to an antigen met again; it starts from memory cells and existing antibodies. | fact |

## Relationships

| From | Relationship | To | Notes |
|---|---|---|---|
| gene-segment shuffling | generates, before any infection | receptor library | random; not guided by any pathogen |
| antigen + danger signal | activates | matching naive lymphocyte | clonal selection |
| activated lymphocyte | divides into | clone of effector cells | and some memory cells |
| memory cells | outnumber | naive precursors | illustrative 100× (estimate range 10–1,000×) |
| vaccine | runs | primary response | without disease |
| pathogen with same antigen | meets | secondary response | fast, large |

## Dependencies (learning order)

1. The pathogen grows exponentially; the defence is a race.
2. The receptor library exists before any infection (random generation).
3. Clonal selection: antigen picks the matching lymphocytes; they multiply.
4. The primary response is slow because the matching clone starts small.
5. After the response, memory cells remain, more of them than before.
6. A vaccine runs step 3–5 without the disease.
7. Memory protects only while the antigen stays the same.

## Causal chain

```text
random receptor library (before birth onward)
  → vaccine shows antigen + danger signal
  → matching rare lymphocytes activate and multiply (≈1 week)
  → most effector cells die; memory cells + long-lived plasma cells remain
  → real pathogen arrives → memory cells + antibodies respond in ≈3 days
  → pathogen controlled before it grows enough to cause disease
```

## Temporal sequence

1. Lymphocytes form continuously in bone marrow and thymus, each with a random receptor.
2. Day 0: vaccine. Days 0–3: antigen reaches lymph nodes, rare matching cells find it and activate.
3. Days 3–7: clone divides about every 8 hours.
4. Days 7–14: response peaks.
5. Weeks after: about 99% of effector cells die; memory cells remain for years to decades.
6. Later infection: secondary response in about 2–4 days.

## Quantities

All "illustrative" numbers are a round-number model to show the race, labelled as such.

- Receptor library: more than 100 million different receptors in one person (estimate; true diversity likely higher). Built by randomly joining gene segments and editing the joins.
- Human genes: about 20,000. So one gene per receptor is impossible.
- Coverage: one receptor binds a family of similar shapes, and a pathogen carries many different antigens; so a random library of >10^8 receptors almost always contains some that fit.
- Self-binding: most new lymphocytes whose receptors bind the body's own molecules are removed before release (established; detail out of scope).
- Naive precursors for one antigen: roughly 1 in 100,000 to 1 in 1,000,000 lymphocytes (estimate). Illustrative precursor count: 100 cells.
- Division time of an activated lymphocyte: about 8 hours (3 per day).
- Why fewer cells can beat more virus: the response does not need to outnumber the pathogen. One plasma cell releases thousands of antibodies per second; one killer T cell kills many infected cells. Illustrative: 1,000,000 effector cells clear the pathogen faster than it grows ("control").
- Primary: 100 × 2^n = 10^6 → n ≈ 13.3 divisions ≈ 4.4 days, + about 2.5 days to find antigen and activate ≈ 7 days.
- Contraction: about 99% of the 10^6 effector cells die; about 1% remain as memory cells (illustrative 10,000 = 100× the naive count; real ratio estimates 10–1,000×).
- Memory: 10,000 → 2^n = 100 → n ≈ 6.6 divisions ≈ 2.2 days, + about 0.5–1 day to activate (memory cells already sit in tissues and lymph nodes and need less stimulation) ≈ 3 days.
- Illustrative pathogen: starts at 100 particles, grows 10× per day; symptoms appear above about 10^8 particles. Primary: 7 days → 100 × 10^7 = 10^9 (sick; symptoms from day 6). Secondary: 3 days → 100 × 10^3 = 10^5, 1,000× below the symptom level.
- Meaning of the precursor count: low (100) → about 7 days to control; high (10,000) → about 3 days. Every 2× more precursors saves one division (8 h).
- Effectiveness: the percentage drop in disease among vaccinated people compared with unvaccinated people (e.g. 97%: 90 of 100 unvaccinated get measles after exposure, about 3 of 100 vaccinated do).
- Measles: two vaccine doses give about 97% protection, for decades (established).
- Influenza: vaccine effectiveness about 40–60% in a typical season, and a new vaccine each year (established range).

## Alternative states

| State | What changes | Why |
|---|---|---|
| no vaccine, first infection | primary response, ≈7 days | pathogen grows ≈10^7×; disease likely |
| vaccinated, same antigen | secondary response, ≈3 days, antibodies already present | pathogen grows ≈10^3× at most; often no disease |
| vaccinated, antigen changed (flu drift) | memory receptors bind poorly | response falls back toward primary |
| antigen without adjuvant | weak or no activation | missing danger signal |

## Why this form

| Operation | Simplest alternative | What the alternative breaks (with numbers) |
|---|---|---|
| random receptor library | one gene per pathogen receptor | ~20,000 genes vs >100 million receptors needed; genes cannot list unknown future pathogens |
| clonal selection (multiply only the matching clone) | make all lymphocytes multiply | 100 million kinds × growth: the body cannot hold it; and most would attack nothing or self |
| need for danger signal / adjuvant | activate on any binding | would attack harmless food proteins and self; pure protein vaccines often give weak responses |
| vaccine runs the first response | wait for the real infection | real primary response takes ~7 days while pathogen grows 10^7× |

## Concrete cases

| Claim | Holds here (numbers) | Breaks here, without its assumption (numbers) |
|---|---|---|
| memory makes the response fast | 10,000 vs 100 starting cells: 6.6 vs 13.3 divisions; ≈3 vs ≈7 days | if the antigen changes (flu drift), memory receptors no longer bind well; effectiveness 40–60% and a yearly new vaccine |
| memory lasts | measles: 2 doses ≈97% protection for decades | influenza: shape change, not memory loss, needs yearly update |
| clonal expansion math | 100 × 2^13.3 ≈ 10^6 | — |

## Terms

- pathogen: the thing that causes the disease (virus, bacterium).
- antigen: the molecular shape that a receptor binds (e.g. the SARS-CoV-2 spike protein).
- lymphocyte: B cell or T cell; each carries one kind of receptor.
- receptor: shape-binding protein on a lymphocyte; random; one kind per lymphocyte.
- naive lymphocyte: has not met its antigen.
- clone: a lymphocyte and its descendants, same receptor.
- clonal selection: antigen activates only matching lymphocytes, which multiply.
- effector cell: activated lymphocyte fighting now (plasma cell, killer T cell).
- antibody: a released copy of a B cell receptor.
- memory cell: long-lived lymphocyte that remains after a response.
- danger signal / adjuvant: the "this is a threat" second signal / the vaccine ingredient that provides it.
- primary / secondary response.
- precursor count: number of lymphocytes able to respond at the start (100 naive, illustrative; 10,000 memory). Low → slow response; high → fast.

## Epistemic status

- **Observed / established:** clonal selection; V(D)J recombination; memory cells; primary ≈1–2 weeks vs secondary ≈days; measles and flu effectiveness ranges.
- **Mathematical consequence:** division counts from 2^n.
- **Estimated:** library size, precursor frequency, memory-to-naive ratio.
- **Illustrative model:** 100 cells, 10^6 needed, pathogen 10×/day.
- **Simplified:** the danger signal (in reality several signals and T-cell help).

## Confusion points

- "The vaccine teaches the body the shape / the body builds an antibody to fit it." → No instruction: the matching receptor already exists by chance; the vaccine selects and multiplies it.
- "A vaccine is a weak infection that the body fights off, and immunity is the antibodies." → Antibodies fade; the lasting part is the larger pool of memory cells (plus long-lived plasma cells).
- "Vaccinated means you cannot be infected." → The pathogen can still enter; memory shortens the race so it is controlled sooner.
- "Flu vaccine fails because memory wears off." → Mainly the antigen changes.

## Scope

- **Out of scope:** antibody decay over months; why some vaccines need boosters.
- **Out of scope:** affinity maturation (B-cell receptors improve their fit over weeks) — germinal centres, immunology textbook (Janeway's Immunobiology).
- **Out of scope:** T-cell help, MHC presentation — same textbook.
- **Out of scope:** vaccine types (live attenuated, inactivated, subunit, mRNA) — they differ in how the antigen is delivered, not in the memory mechanism.
- **Out of scope:** herd immunity, boosters' exact schedule, safety.

## Representation decision

- **Stage:** 1
- **Reason:** One causal chain with one before/after comparison; a table holds the two races. No parameter needs exploring beyond the one comparison.
- **Levels:** L1 answer / L2 the steps / L3 why random library, why memory is fast / L4 limits.
