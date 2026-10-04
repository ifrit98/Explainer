# Chat eval, 2026-10-04

Answers and grades by `claude -p` (fresh, no tools, no settings). The grader saw each question's answers under shuffled labels.

Conditions: **none** = `none`; **v0.5** = `git:v0.5.0`; **v0.6** = `principles`

| condition | score /10 | must points | misconception taught | corrected | answer first | errors | excess / answer | unclear / answer | words | ranked best |
|---|---|---|---|---|---|---|---|---|---|---|
| none | 6.3 | 94% | 0 | 2 | 4/6 | 1 | 4.7 | 3.0 | 399 | 0 |
| v0.5 | 7.2 | 100% | 0 | 5 | 6/6 | 2 | 5.0 | 1.8 | 544 | 1 |
| v0.6 | 7.8 | 94% | 0 | 4 | 6/6 | 1 | 1.5 | 1.5 | 292 | 5 |

## Per question

- **ice-floats**: ranked v0.6 > v0.5 > none. B covers density, the hydrogen-bond lattice mechanism and the rarity of the effect with correct numbers and a clear buoyancy link, close to the word budget and with the least detour.
- **tcp-slow-start**: ranked v0.6 > v0.5 > none. A covers the reason, the doubling mechanism, and exponential growth, with one correct worked example and close to the word budget, giving the newcomer an accurate model with almost no surplus text.
- **wing-lift**: ranked v0.5 > none > v0.6. B gives a clear causal chain linking downwash and pressure difference. It makes 'pressure × area = lift' concrete with a worked Cessna example, covers angle of attack, v² and stall, and refutes equal transit time with evidence, though it is well over the word budget.
- **hash-table**: ranked v0.6 > v0.5 > none. B covers all three required points correctly, with concrete numbers and plain definitions, in close to the word budget and without detours.
- **moon-face**: ranked v0.6 > none > v0.5. B covers all three required points and explicitly refutes the 'Moon does not rotate' misconception with a simple thought experiment, while staying closest to the word budget with little detour.
- **road-salt**: ranked v0.6 > v0.5 > none. C gives the clearest causal chain: dilution slows refreezing while melting continues. It then adds one worked number and the −21 °C floor, and refutes the heat misconception, all with almost no detours.
