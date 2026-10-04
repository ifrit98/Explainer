# Chat eval, 2026-10-04

Answers and grades by `claude -p` (fresh, no tools, no settings). The grader saw each question's answers under shuffled labels.

Conditions: **none** = `none`; **v0.5** = `git:v0.5.0`; **v0.6** = `principles`

| condition | score /10 | must points | misconception taught | corrected | answer first | errors | excess / answer | unclear / answer | words | ranked best |
|---|---|---|---|---|---|---|---|---|---|---|
| none | 6.5 | 100% | 0 | 4 | 5/6 | 1 | 4.5 | 3.5 | 393 | 1 |
| v0.5 | 7.2 | 97% | 0 | 5 | 6/6 | 4 | 5.0 | 2.3 | 590 | 2 |
| v0.6 | 7.2 | 97% | 0 | 3 | 6/6 | 3 | 4.7 | 2.5 | 580 | 3 |

## Per question

- **ice-floats**: ranked none > v0.5 > v0.6. A covers all three required points accurately and in the fewest words, close to the budget, and its detours are the shortest of the three answers.
- **tcp-slow-start**: ranked v0.5 > v0.6 > none. B defines segment, RTT, and cwnd before using them, grounds the reason in a concrete collapse example, shows exponential doubling with a correct worked table, and explicitly contrasts it with +1-per-RTT growth to explain why 'slow' only describes the start.
- **wing-lift**: ranked v0.6 > none > v0.5. C gives a clean causal chain from angle of attack to curved flow to the pressure difference, places Bernoulli correctly as a consequence, refutes equal transit time, and backs the speed-squared and angle dependence with correct worked numbers.
- **hash-table**: ranked v0.6 > v0.5 > none. B leads with a direct answer, builds the mechanism, the load factor, and the O(n) worst case with concrete numbers, and stays more focused than C and more grounded for this reader than A, though all three run well past the 220-word budget.
- **moon-face**: ranked v0.6 > v0.5 > none. B gives the most complete causal model: why a 1:1 match hides one side, the bulge-torque-friction mechanism with its zero-torque end state and stability, and a libration explanation that says why the Moon appears to rock (constant spin against varying orbital speed). It loses points for an off-topic Earth section and its annotation tags.
- **road-salt**: ranked v0.5 > v0.6 > none. A gives the correct two-rate mechanism, the −21 °C limit, and an explicit refutation of the heat misconception in a tight numbered sequence, with less detour and repetition than C.
