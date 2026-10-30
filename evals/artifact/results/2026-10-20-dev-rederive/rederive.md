# Rederivation, 2026-10-20 (dev, 10 subjects)

Builds: `evals/artifact/results/2026-10-04-dev`. Reader and grader: fresh `claude -p` agents. The reader saw only the renderings and the target's question; the grader saw each subject's explanations and the readers' working under shuffled labels. 3 passes: each a fresh reader run over every build, graded once under its own shuffle.

| condition | supported | raw | result right | stated steps | stated results | words | quiz (grounded) |
|---|---|---|---|---|---|---|---|
| none | 100%, 100%, 100% | 100%, 100%, 100% | 100%, 100%, 100% | 2, 2, 3 | 0, 0, 1 | 1689 | 100% |
| principles | 95%, 100%, 97% | 97%, 100%, 100% | 89%, 89%, 100% | 4, 4, 5 | 1, 1, 2 | 1006 | 99% |
| quick | 92%, 100%, 90% | 100%, 100%, 92% | 100%, 100%, 89% | 2, 2, 2 | 1, 1, 1 | 606 | 95% |
| published | 95%, 95%, 95% | 97%, 97%, 100% | 89%, 78%, 89% | 3, 3, 3 | 1, 1, 1 | 1016 | 95% |

Separation (higher supported score in all three passes): none > published.

Each cell lists the passes in order. Supported: the share of expected steps the reader made and grounded in a part of the explanation it named (or in background this reader has); raw: the share made at all; result right: the share of results that match. Stated steps and stated results: derived steps and results the explanation states outright, left out of the shares above. Words: visible words per explanation. Quiz: the grounded quiz score of the same builds.

## Per subject (supported/counted steps, per pass)

| subject | none | principles | quick | published |
|---|---|---|---|---|
| gps-relativity | 3/3, 3/3, 2/2 | 3/3, 3/3, 2/2 | 4/4, 4/4, 4/4 | 3/3, 3/3, 3/3 |
| vaccine-memory | 4/4, 4/4, 4/4 | 4/4, 4/4, 4/4 | 4/4, 4/4, 4/4 | 4/4, 4/4, 4/4 |
| key-exchange | 5/5, 5/5, 5/5 | 5/5, 5/5, 5/5 | 5/5, 5/5, 5/5 | 5/5, 5/5, 5/5 |
| two-tides | 3/3, 3/3, 3/3 | 3/3, 3/3, 3/3 | 3/4, 4/4, 1/4 | 3/4, 2/4, 2/4 |
| bloom-filter | 4/4, 4/4, 4/4 | 4/4, 4/4, 4/4 | 4/4, 4/4, 4/4 | 4/4, 4/4, 4/4 |
| heat-pump | 4/4, 4/4, 4/4 | 4/4, 4/4, 4/4 | 4/4, 4/4, 4/4 | 4/4, 4/4, 4/4 |
| quorum | 4/4, 4/4, 4/4 | 3/4, 4/4, 3/4 | 3/4, 4/4, 3/4 | 4/4, 4/4, 4/4 |
| antibiotic-resistance | 4/4, 4/4, 4/4 | 4/4, 4/4, 4/4 | 4/4, 4/4, 4/4 | 4/4, 4/4, 4/4 |
| float-sum | 4/4, 4/4, 4/4 | 3/4, 4/4, 4/4 | 3/4, 4/4, 4/4 | 3/4, 4/4, 4/4 |
| greenhouse | 4/4, 4/4, 4/4 | 2/2, 2/2, 2/2 | 2/2, 2/2, 2/2 | 2/2, 2/2, 2/2 |
