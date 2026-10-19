# Artifact eval, 2026-10-04 (dev, 10 subjects)

Builder, reader, and grader: fresh `claude -p` agents. The reader saw only the renderings; an answer counts only when its quote is found in them (grounded). The grader saw each subject's explanations under shuffled labels.

Conditions: **none** = `none`; **principles** = `principles`; **quick** = `quick`; **published** = `published`

| condition | mean rank | ranked best | quiz (grounded) | predict | quiz (raw) | ungrounded | misconception taught | corrected | errors | stops / expl. | excess / expl. | words | forms | cost / expl. | min / expl. |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| none | 3.1 | 0/10 | 100% | 100% | 100% | 0 | 0 | 7 | 4 | 8.7 | 6.0 | 1689 | prose 5, prose+html 4, html 1 | $0.28 | 1.5 |
| principles | 1.8 | 3/10 | 99% | 95% | 99% | 0 | 0 | 7 | 1 | 7.7 | 4.3 | 1006 | prose 10 | $0.21 | 1.0 |
| quick | 2.9 | 2/10 | 95% | 95% | 95% | 0 | 0 | 5 | 6 | 7.1 | 3.8 | 606 | prose 8, diagram 2 | $0.46 | 1.6 |
| published | 2.2 | 5/10 | 95% | 100% | 95% | 0 | 0 | 7 | 1 | 7.9 | 5.0 | 1016 | prose 9, diagram 1 | $2.81 | 11.8 |

Mean rank: the grader's ranking of each subject's 4 explanations by the reader's effort (1 is best). Quiz: fixed questions per subject, 0–2 each; predict: the last question of each, a case the explanation need not mention. Stops and excess: the reader's lists (at most 10 each). Words: visible words in all renderings. Cost: the builder and the reviews it ran; minutes: the builder.

## Per subject (grounded quiz score, of 8)

| subject | none | principles | quick | published |
|---|---|---|---|---|
| gps-relativity | 8 (1500 w) | 8 (1158 w) | 8 (676 w) | 8 (999 w) |
| vaccine-memory | 8 (1953 w) | 8 (1067 w) | 7 (600 w) | 8 (992 w) |
| key-exchange | 8 (1822 w) | 8 (931 w) | 8 (506 w) | 8 (1086 w) |
| two-tides | 8 (1929 w) | 8 (884 w) | 6 (599 w) | 6 (948 w) |
| bloom-filter | 8 (1439 w) | 8 (1083 w) | 8 (599 w) | 8 (1059 w) |
| heat-pump | 8 (1339 w) | 7 (784 w) | 7 (814 w) | 8 (1437 w) |
| quorum | 8 (1072 w) | 8 (777 w) | 8 (502 w) | 8 (896 w) |
| antibiotic-resistance | 8 (2511 w) | 8 (1194 w) | 8 (600 w) | 8 (949 w) |
| float-sum | 8 (1056 w) | 8 (661 w) | 8 (412 w) | 8 (721 w) |
| greenhouse | 8 (2271 w) | 8 (1522 w) | 8 (749 w) | 6 (1072 w) |

✗: the explanation teaches the misconception.

## Why the best is best

- **gps-relativity**: published > principles > quick > none. D builds each idea in order with no detours: it says the receiver only listens, makes the clock bias b concrete with a small 1-D worked example, sets a nanosecond budget, and explains why a shared b cannot absorb satellite drift that differs between satellites.
- **vaccine-memory**: published > principles > none > quick. C carries one consistent worked model (rare precursors, division count, memory pool size, the race against a pathogen growing 10× per day) from start to finish, says explicitly that the vaccine contains no pathogen that can multiply, defines every term it uses, and leaves side topics to a short 'not covered' list, so the reader gets every quiz point without detours.
- **key-exchange**: quick > principles > published > none. B covers the operation, why it is hard, why both sides get the same key, the worked p=23 example and the man-in-the-middle fix in the fewest words, with no detours beyond what this reader needs.
- **two-tides**: principles > none > published > quick. A covers every quiz point and names and refutes the spin-centrifugal misconception, using compact worked numbers, without B's long detours (code, a broken companion-page dump) and without the spring-tide gap in C and D.
- **bloom-filter**: published > principles > quick > none. C states up front that the filter keeps only bits, and it runs one small example through add, a correct 'no', a false positive and a failed delete. It then derives the fill fraction f and the rate p ≈ f^k and shows overfilling numerically, so the reader can answer even the all-bits-set case straight from the text, without detours.
- **heat-pump**: published > none > principles > quick. A builds the model in clear steps: the energy balance, then the four-part loop with consistent numbers at every stage, then the kelvin formula with a worked entropy check of an allowed and a forbidden COP. That made all four answers exact, without D's detours (analogy, code, air-conditioning) or the refrigerant-temperature tables in B and C that led their readers to the wrong limit in Q4.
- **quorum**: quick > principles > published > none. A gives the counting rule up front, then derives the majority from a single split-brain example and the 2q > n overlap condition, and shows that an even-sized cluster adds no tolerance, all in the fewest words and with no detours.
- **antibiotic-resistance**: published > principles > quick > none. A covers variation, selection, and cross-species plasmid transfer in the fewest words, and its worked numbers and Luria–Delbrück variance argument show directly why the drug selects resistant cells rather than creating them.
- **float-sum**: principles > none > quick > published. A gives the full causal chain (the prime-factor rule, stored values as integer × power of 2, the tie rounding and the printing behaviour) in a short, exact form with no detours, so the reader gets a correct model with little effort.
- **greenhouse**: principles > none > quick > published. C builds every link the reader needs (energy balance, the wavelength split, the dipole reason, a one-layer model and why it fails, then emission height with the lapse rate, its limits, and worked numbers) in a tight order with prediction prompts, without A's extra detours and length or the gaps in D and B.
