# Rederivation, 2026-10-29 (dev, 5 subjects)

Builds: `evals/artifact/results/2026-10-29-dev-controls`. Reader and grader: fresh `claude -p` agents. The reader saw only the renderings and the target's question; the grader saw each subject's explanations and the readers' working under shuffled labels. 3 passes: each a fresh reader run over every build, graded once under its own shuffle.

| condition | supported | raw | result right | stated steps | stated results | words | quiz (grounded) |
|---|---|---|---|---|---|---|---|
| none | 100%, 100%, 100% | 100%, 100%, 100% | 100%, 100%, 100% | 1, 1, 1 | 0, 0, 0 | 1683 | – |
| principles-cut | 57%, 57%, 57% | 62%, 62%, 67% | 20%, 40%, 40% | 0, 0, 0 | 0, 0, 0 | 791 | – |
| quick | 95%, 100%, 79% | 100%, 100%, 84% | 100%, 100%, 75% | 2, 2, 2 | 1, 1, 1 | 616 | – |
| published | 95%, 89%, 89% | 100%, 100%, 100% | 75%, 50%, 50% | 2, 2, 2 | 1, 1, 1 | 1053 | – |

Separation (higher supported score in all three passes): none > principles-cut, none > published, quick > principles-cut, published > principles-cut.

Each cell lists the passes in order. Supported: the share of expected steps the reader made and grounded in a part of the explanation it named (or in background this reader has); raw: the share made at all; result right: the share of results that match. Stated steps and stated results: derived steps and results the explanation states outright, left out of the shares above. Words: visible words per explanation. Quiz: the grounded quiz score of the same builds.

## Per subject (supported/counted steps, per pass)

| subject | none | principles-cut | quick | published |
|---|---|---|---|---|
| key-exchange | 5/5, 5/5, 5/5 | 3/5, 3/5, 3/5 | 5/5, 5/5, 5/5 | 5/5, 5/5, 5/5 |
| two-tides | 3/3, 3/3, 3/3 | 2/4, 2/4, 2/4 | 3/4, 4/4, 0/4 | 3/4, 2/4, 2/4 |
| heat-pump | 4/4, 4/4, 4/4 | 3/4, 3/4, 3/4 | 4/4, 4/4, 4/4 | 4/4, 4/4, 4/4 |
| float-sum | 4/4, 4/4, 4/4 | 4/4, 4/4, 4/4 | 4/4, 4/4, 4/4 | 4/4, 4/4, 4/4 |
| greenhouse | 4/4, 4/4, 4/4 | 0/4, 0/4, 0/4 | 2/2, 2/2, 2/2 | 2/2, 2/2, 2/2 |
