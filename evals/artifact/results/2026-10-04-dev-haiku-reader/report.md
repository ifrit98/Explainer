# Artifact eval, 2026-10-04 (dev, 10 subjects)

Builder, reader, and grader: fresh `claude -p` agents (reader: --model haiku). The reader saw only the renderings; an answer counts only when its quote is found in them (grounded). The grader saw each subject's explanations under shuffled labels.

Conditions: **none** = `none`; **principles** = `principles`; **quick** = `quick`; **published** = `published`

| condition | mean rank | ranked best | quiz (grounded) | predict | quiz (raw) | ungrounded | misconception taught | corrected | errors | stops / expl. | excess / expl. | words | forms | cost / expl. | min / expl. |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| none | 3.3 | 0/10 | 95% | 85% | 98% | 1 | 0 | 7 | 3 | 9.0 | 9.2 | 1689 | prose 5, prose+html 4, html 1 | $0.28 | 1.5 |
| principles | 1.7 | 5/10 | 98% | 95% | 98% | 0 | 0 | 7 | 4 | 9.2 | 8.5 | 1006 | prose 10 | $0.21 | 1.0 |
| quick | 2.5 | 3/10 | 94% | 95% | 94% | 0 | 0 | 5 | 9 | 7.9 | 6.9 | 606 | prose 8, diagram 2 | $0.46 | 1.6 |
| published | 2.5 | 2/10 | 95% | 95% | 95% | 0 | 0 | 6 | 2 | 8.5 | 8.5 | 1016 | prose 9, diagram 1 | $2.81 | 11.8 |

Mean rank: the grader's ranking of each subject's 4 explanations by the reader's effort (1 is best). Quiz: fixed questions per subject, 0–2 each; predict: the last question of each, a case the explanation need not mention. Stops and excess: the reader's lists (at most 10 each). Words: visible words in all renderings. Cost: the builder and the reviews it ran; minutes: the builder.

## Per subject (grounded quiz score, of 8)

| subject | none | principles | quick | published |
|---|---|---|---|---|
| gps-relativity | 8 (1500 w) | 8 (1158 w) | 8 (676 w) | 8 (999 w) |
| vaccine-memory | 8 (1953 w) | 8 (1067 w) | 8 (600 w) | 8 (992 w) |
| key-exchange | 8 (1822 w) | 8 (931 w) | 8 (506 w) | 8 (1086 w) |
| two-tides | 8 (1929 w) | 8 (884 w) | 6 (599 w) | 6 (948 w) |
| bloom-filter | 8 (1439 w) | 8 (1083 w) | 8 (599 w) | 8 (1059 w) |
| heat-pump | 7 (1339 w) | 7 (784 w) | 7 (814 w) | 7 (1437 w) |
| quorum | 6 (1072 w) | 8 (777 w) | 7 (502 w) | 8 (896 w) |
| antibiotic-resistance | 8 (2511 w) | 8 (1194 w) | 8 (600 w) | 8 (949 w) |
| float-sum | 8 (1056 w) | 8 (661 w) | 8 (412 w) | 8 (721 w) |
| greenhouse | 7 (2271 w) | 7 (1522 w) | 7 (749 w) | 7 (1072 w) |

✗: the explanation teaches the misconception.

## Why the best is best

- **gps-relativity**: published > principles > none > quick. D states that the receiver only listens and uses a small worked example on a line to make the shared clock error b concrete; it then shows why per-satellite clock errors cannot be absorbed, all in few words and without detours.
- **vaccine-memory**: quick > published > principles > none. D gives every link in the chain (random repertoire, selection, expansion, memory, race, and limits from antigen change) in the fewest words, with defined terms and a single comparison table, so this reader gets the full model with no detours.
- **key-exchange**: quick > principles > published > none. B covers every quiz point, including the operation, why both keys match, the worked p=23 example, the man-in-the-middle attack with its fix, and why powers mod p are needed, in the fewest words with no detours.
- **two-tides**: principles > none > published > quick. A gives the whole causal chain (free fall, subtracting the centre's pull with worked numbers, Earth turning under two bulges, the lunar-day timing, and Sun–Moon spring/neap tides) in a compact form, and it explicitly refutes the spin-centrifugal misconception without the length and stray interactive-page residue of B.
- **bloom-filter**: quick > published > principles > none. A gives every needed step in the fewest words: add and query on a tiny worked array, why a 'no' is certain, why deletion breaks that guarantee, and a concrete false positive, with correct numbers and no detours.
- **heat-pump**: principles > published > quick > none. B gives the energy balance, the pressure-dependent boiling trick, the four-step loop with numbers, and a short entropy derivation of the Carnot limit with a mild-versus-cold table, all without errors, detours or repetition.
- **quorum**: principles > quick > published > none. D shows the simple rule failing with a concrete split-brain example, derives q > n/2 from the overlap requirement in one step, and refutes the 'more servers is always better' idea with a checked availability table, so the reader gets every needed step without detours.
- **antibiotic-resistance**: published > principles > none > quick. A gives the reader every step in a short, error-free chain (pre-existing variation with worked numbers, selection with a regrowth calculation, a quantitative Luria-Delbrück refutation of the adaptation idea, and horizontal transfer across species) and defines each term once, without detours.
- **float-sum**: principles > quick > none > published. A gives every step the reader needs: why 0.1 repeats in binary, the stored values, the tie-rounded sum, why it prints as 0.30000000000000004, and the exact power-of-2 case, all with exact grid arithmetic and without B's detours or D's dense unit bookkeeping.
- **greenhouse**: principles > none > quick > published. C builds each step of the mechanism in order (energy balance, wavelength split, dipole reason, why the one-layer model fails, emission height and lapse rate, the isothermal test case), with worked numbers and prediction prompts, and adds nothing the reader does not need, while A covers the same ground at much greater length, D contradicts its own numbers, and B skips why N2 and O2 do not absorb.
