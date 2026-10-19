# Semantic model: the greenhouse effect

> Source of truth. Every rendering derives from this file.

## Central question

How do greenhouse gases make the Earth's surface warmer than it would be without them?

## Audience and prior knowledge

A technical reader: school mathematics and science (energy, power in watts, temperature in kelvin, molecules, light as a spectrum of wavelengths, gases cool when they expand), basic programming. New to this subject. Knows that hot objects glow and that hotter objects radiate more. Does not know the Stefan–Boltzmann law, albedo, emission height, the lapse rate, or radiative forcing.

## Entities

| Entity | Definition (one sentence) | Status |
|---|---|---|
| Sunlight | Radiation from the Sun, mostly visible light, wavelengths near 0.5 µm. | established |
| Infrared | Radiation that the Earth (ground and air) emits, wavelengths near 10 µm, invisible to the eye. | established |
| Albedo | The fraction of sunlight the Earth reflects straight back to space: 0.30. | observed |
| Energy balance | In a steady state, the power the Earth absorbs from sunlight equals the power it emits to space as infrared. | established (conservation of energy) |
| Stefan–Boltzmann law | A surface at temperature T emits power σT⁴ per square metre (σ = 5.67×10⁻⁸ W m⁻² K⁻⁴). | established |
| Emission temperature | The temperature that emits 240 W/m² by σT⁴: 255 K. Energy balance fixes it. | mathematical consequence |
| Greenhouse gas | A gas that absorbs and emits infrared: water vapour, CO₂, methane. N₂ and O₂ (99% of dry air) do not. | established |
| Emission height | The average altitude from which infrared escapes to space; above it, too little greenhouse gas remains to absorb it again. ≈ 5 km today. | established (a simplification of a spread of heights across wavelengths) |
| Lapse rate | The fall of air temperature with height in the lower atmosphere: about 6.5 K per km. | observed average |
| Radiative forcing | The imbalance (W/m²) at the top of the atmosphere just after a change, such as added CO₂, before the Earth warms. | established; value is model output |

## Relationships

| From | Relationship (verb) | To | Notes |
|---|---|---|---|
| Sunlight | passes through | atmosphere | greenhouse gases absorb little of it |
| Surface | emits | infrared | σT⁴ |
| Greenhouse gas | absorbs and re-emits in all directions | infrared | part goes back down to the surface |
| Greenhouse gas amount | sets | emission height | more gas → higher emission height |
| Convection | holds | lapse rate at ≈ 6.5 K/km | rising air expands and cools |
| Energy balance | fixes | air at emission height at 255 K | |
| Lapse rate × emission height | adds to 255 K to give | surface temperature | 255 + 6.5 × 5.08 ≈ 288 K |

## Dependencies (learning order)

1. Energy balance and Stefan–Boltzmann → emission temperature 255 K; surface would be 255 K with no greenhouse gas.
2. Sunlight vs infrared; which gases absorb infrared.
3. Infrared escapes from the emission height, not the surface.
4. Lapse rate ties the surface to the air at the emission height.
5. Adding gas raises emission height → imbalance → warming.

## Causal chain

```text
more greenhouse gas → infrared escapes from higher up → the air there is colder → it emits less to space
→ Earth absorbs more than it emits (radiative forcing) → Earth warms
→ warming stops when the air at the new emission height is back at 255 K
→ the lapse rate holds, so the surface is warmer by (6.5 K/km × rise in emission height)
```

## Temporal sequence

1. CO₂ is added. Emission height rises at once.
2. Outgoing infrared drops; the Earth gains energy (forcing ≈ 3.7 W/m² for doubled CO₂).
3. Surface and air warm over years to decades (the ocean slows it). The imbalance shrinks as they warm.
4. Balance returns when the air at the emission height is at 255 K again.

## Quantities

- Solar constant: 1361 W/m² on a surface facing the Sun.
- Average over the sphere: 1361 / 4 = 340 W/m².
- Albedo 0.30. Absorbed: 340 × 0.70 ≈ 240 W/m².
- Emission temperature: σT⁴ = 240 → T ≈ 255 K (−18 °C).
- Observed mean surface temperature: 288 K (15 °C). Difference: 33 K.
- Surface at 288 K emits σ·288⁴ ≈ 390 W/m²; only 240 W/m² leaves to space.
- Surface budget (rounded, observed estimates): gains 160 W/m² sunlight + 330 W/m² infrared from the air = 490; loses 390 W/m² infrared + 100 W/m² convection and evaporation = 490.
- Peak wavelengths: Sun (5800 K) ≈ 0.5 µm; Earth (288 K) ≈ 10 µm.
- Lapse rate 6.5 K/km (dry rising air cools 9.8 K/km; condensing water releases heat and reduces it). 33 K / 6.5 K/km ≈ 5 km: average emission height.
- Doubling CO₂: forcing ≈ 5.35 × ln 2 ≈ 3.7 W/m². 280 → 420 ppm: 5.35 × ln 1.5 ≈ 2.2 W/m².
- Air 1 K colder (254 K vs 255 K) emits about 3.8 W/m² less. 1 K at 6.5 K/km is about 150 m of rise.
- Warming that restores balance, no feedbacks: 3.7 / 3.76 ≈ 1 K, where 3.76 W/m² per K = 4σ·255³ is the extra emission per 1 K of warming.
- With feedbacks (mainly water vapour): about 3 K per doubling (IPCC AR6 best estimate; likely 2.5–4 K).
- CO₂: about 280 ppm in 1750, about 420 ppm in 2024.

## Alternative states

| State / scenario | What changes | Why |
|---|---|---|
| No greenhouse gas | surface 255 K | surface emits straight to space |
| Present atmosphere | surface 288 K | emission height ≈ 5 km, 33 K colder than surface |
| Doubled CO₂, no feedbacks | ≈ +1 K | emission height rises ≈ 150 m |
| Isothermal atmosphere (no lapse rate) | added gas causes no warming | emission height rises but the air there is not colder |
| Stratosphere (above ≈ 12 km, temperature rises with height) | added CO₂ cools the stratosphere | observed |

## Why this form

| Operation | Simplest alternative | What the alternative breaks (with numbers) |
|---|---|---|
| Divide solar constant by 4 | Use 1361 W/m² directly | σT⁴ = 1361 × 0.7 → T ≈ 360 K (87 °C). The Earth intercepts sunlight on a disc of area πR² but emits from a sphere of area 4πR². |
| Explain by emission height + lapse rate | "Gases trap heat like a blanket" | A blanket picture says more gas always warms and gives no number. Isothermal air is a counterexample: emission height rises, emitting air is still 255 K, outgoing stays 240 W/m², no warming. The trapping picture also suggests saturation ends the effect; it does not. |

## Concrete cases

| Claim | Holds here (numbers) | Breaks here, without its assumption (numbers) |
|---|---|---|
| More greenhouse gas warms the surface (assumes temperature falls with height) | Emission height 5.08 → 5.23 km; air there 1 K colder emits ≈ 3.7 W/m² less; Earth warms until that air is 255 K; surface 288 → 289 K | Isothermal air: emitting air is 255 K at any height → no imbalance, no warming. Stratosphere, where temperature rises with height: added CO₂ cools it. |
| Mechanism: energy balance sets 255 K | 340 × 0.7 = 238 ≈ 240 W/m²; σ·255⁴ ≈ 240 W/m² | — |
| Mechanism: more gas raises emission height | infrared escapes where little gas remains above; with twice the gas, that amount of gas above lies higher | at wavelengths no gas absorbs (8–13 µm "window", mostly) the surface emits straight to space and nothing changes; averaged over all wavelengths the rise is ≈ 150 m |
| Saturation does not end the effect | 280 → 560 ppm: 3.7 W/m²; 560 → 1120 ppm: again 3.7 W/m² | — |

## Terms

- **Sunlight:** short-wave radiation from the Sun (near 0.5 µm).
- **Infrared:** long-wave radiation the Earth emits (near 10 µm). Here, "infrared" always means the Earth's.
- **Albedo:** fraction of sunlight reflected. 0.30 → 240 W/m² absorbed; at 0, 340 W/m² would be absorbed.
- **Greenhouse gas:** a gas that absorbs and emits infrared.
- **Energy balance:** absorbed power = emitted power.
- **Emission temperature:** 255 K, the temperature that emits 240 W/m². One name only; not "balance temperature", not "no-atmosphere temperature".
- **Emission height:** the average altitude from which infrared escapes to space; ≈ 5 km today. 0 km: no greenhouse gas, surface 255 K. Each extra km: surface 6.5 K warmer.
- **Lapse rate:** 6.5 K drop per km. If 0, added gas does nothing; if larger, the same rise warms more.
- **Radiative forcing:** the imbalance just after a change, before the Earth warms. 3.7 W/m² for doubled CO₂ (compare 240 W/m² absorbed). It shrinks to 0 as the Earth warms.

## Epistemic status

- **Observed / established:** solar constant, albedo, surface 288 K, CO₂ concentrations, absorption spectra, lapse rate average, stratospheric cooling, surface budget (rounded).
- **Mathematical consequence:** 255 K from σT⁴ = 240; ≈ 1 K no-feedback warming.
- **Assumed:** a single emission height (really a spread across wavelengths); a fixed lapse rate.
- **Estimated / model output:** 3.7 W/m² forcing (radiation models); 3 K with feedbacks (IPCC assessment, likely 2.5–4 K).
- **Disputed:** that the effect exists is not disputed; the size of cloud feedback is the main uncertainty.

## Confusion points

- "CO₂ already absorbs all the infrared at its main wavelength, so more does nothing" → more gas still raises the emission height; each doubling adds about the same 3.7 W/m².
- "Greenhouse gases trap heat like a blanket" → the gases absorb and re-emit; warming comes from escape at a colder height. (A real glass greenhouse works mainly by stopping warm air from rising: a different mechanism.)
- "N₂ and O₂ are most of the air, so they matter most" → they do not absorb infrared.
- "390 W/m² leaves the surface but only 240 reaches space — energy is lost" → the air sends 330 W/m² back down; the surface budget balances.

## Scope

- **Out of scope:** feedbacks in detail (water vapour, clouds, ice) — IPCC AR6 WG1 Chapter 7.
- **Out of scope:** why a molecule must change its charge separation when it vibrates to absorb infrared — a molecular spectroscopy text.
- **Out of scope:** the carbon cycle and where added CO₂ goes.
- **Out of scope:** why forcing is logarithmic in CO₂ — Pierrehumbert, *Principles of Planetary Climate*.
- **Out of scope:** how fast warming happens (ocean heat uptake).

## Representation decision

- **Stage:** 1
- **Reason:** The argument is a short causal chain with arithmetic. One table of numbers carries the comparison. No parameter needs exploration that a worked example with numbers does not give.
- **Levels:** L1 gases make the surface 33 K warmer / L2 emission from a colder height / L3 energy balance and lapse rate / L4 forcing numbers.
