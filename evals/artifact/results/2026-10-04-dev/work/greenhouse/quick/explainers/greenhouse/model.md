# Semantic model: the greenhouse effect

> Source of truth. Every rendering derives from this file.

## Central question

How do greenhouse gases make the Earth's surface warmer than it would be without them?

## Audience and prior knowledge

A technical reader: school mathematics and physics (energy, temperature in kelvin, wavelength, molecules), basic programming. New to the subject. Does not know Stefan–Boltzmann, lapse rate, or emission height. Renderings define those terms.

## Entities

| Entity | Definition (one sentence) | Status |
|---|---|---|
| sunlight | Radiation from the Sun, mostly visible light, peak near 0.5 µm. | fact |
| infrared | Radiation that the Earth emits, peak near 10 µm, invisible. | fact |
| greenhouse gas | A gas whose molecules absorb and emit infrared: H2O, CO2, CH4, N2O, O3. | fact |
| energy balance | The state in which the planet emits to space as much energy as it absorbs. | fact |
| emission height | The average altitude from which infrared escapes to space, about 5 km. | estimate |
| lapse rate | The fall of air temperature with altitude in the lower atmosphere, about 6.5 K per km. | observed average |

## Causal chain

```text
sunlight passes through air → surface warms → surface emits infrared
→ greenhouse gas absorbs infrared, re-emits it in all directions
→ infrared escapes to space only from the emission height (~5 km, 255 K)
→ more greenhouse gas → higher emission height → colder emitter → less infrared out
→ energy balance broken → planet gains energy → whole column warms
→ surface warms by the same amount until energy balance returns
```

## Quantities

- Solar constant S = 1361 W/m². Albedo (fraction reflected) a = 0.30.
- Absorbed sunlight per m² of surface, averaged: S(1 − a)/4 = 238 W/m² (about 240).
- Stefan–Boltzmann: emitted power per m² = σT⁴, σ = 5.67×10⁻⁸ W m⁻² K⁻⁴.
- Temperature for energy balance: T = (238 / σ)^(1/4) = 255 K (−18 °C).
- Observed mean surface temperature: 288 K (15 °C). Difference: 33 K.
- Surface emission at 288 K: σ·288⁴ = 390 W/m². Outgoing to space: about 240 W/m². The atmosphere holds back 150 W/m².
- Emission height: (288 − 255) / 6.5 ≈ 5 km.
- CO2 doubling: radiative forcing (imbalance before any warming) ≈ 5.35·ln 2 = 3.7 W/m².
- Emission height rise for that forcing: about 150 m → emitter 1 K colder → 4σT³·1 K = 3.8 W/m² less out.
- Warming with no feedbacks: 3.7 / 3.2 ≈ 1.2 K. With feedbacks (water vapour, ice, clouds): likely 2.5–4 K (IPCC AR6 estimate).

## Alternative states

| State | What changes | Why |
|---|---|---|
| No greenhouse gas | Surface emits straight to space; surface ≈ 255 K | Emission height = 0 km |
| Today | Surface 288 K | Emission height ≈ 5 km, lapse rate 6.5 K/km |
| Doubled CO2 | Surface ≈ 1.2 K warmer before feedbacks | Emission height ≈ 150 m higher |
| No lapse rate (isothermal air) | No greenhouse warming, however much gas | Higher emitter is not colder |

## Why this form

| Operation | Simplest alternative | What the alternative breaks |
|---|---|---|
| Divide sunlight by 4 | Use 1361 W/m² × 0.7 directly | Gives T = 360 K. The Earth intercepts sunlight on a disc (πr²) but emits from a sphere (4πr²). |
| Emitted power ∝ T⁴ | Proportional to T | The 1 K colder emitter would lose only 0.4% = 0.9 W/m²; real loss is 4 × 0.4% = 1.6% = 3.8 W/m². |

## Concrete cases

| Claim | Holds here | Breaks here |
|---|---|---|
| More gas warms the surface | Lapse rate 6.5 K/km: 150 m higher → 1 K colder emitter → 3.8 W/m² deficit | Isothermal air: higher emitter has same T, no deficit, no warming |
| N2 and O2 do not absorb infrared | 99% of dry air, yet transparent to infrared | CO2 (0.04%) absorbs strongly near 15 µm |

## Terms

sunlight, infrared, greenhouse gas, energy balance, emission height, lapse rate, radiative forcing (the energy imbalance in W/m² that a change causes before the planet warms; 0 = balanced, 3.7 = doubled CO2).

## Epistemic status

- **Established:** absorption bands of CO2 and H2O; 255 K and 288 K; Stefan–Boltzmann.
- **Estimate:** emission height 5 km (an average over wavelengths); 150 m rise; feedback range 2.5–4 K.

## Confusion points

- "Gases trap heat like greenhouse glass" → a glass greenhouse works mainly by stopping warm air from rising. Greenhouse gases change where the planet emits from.
- "CO2 absorption is saturated, so more CO2 does nothing" → near the surface, yes. The escape point still moves up, so forcing grows with the logarithm of CO2, not zero.
- "The gas makes energy" → no. It slows energy loss; the source is sunlight.

## Scope

- **Out of scope:** feedbacks in detail, clouds, the one-layer model, ocean heat uptake — see IPCC AR6 WG1 chapter 7.

## Representation decision

- **Stage:** 2
- **Reason:** the answer is a flow of energy plus a causal chain with a temperature profile; the reader must hold the surface, the gas, the emission height, and space at once.
- **Levels:** L1 energy flow / L2 emission-height mechanism / L3 why only some molecules.
