# Narrative: greenhouse

> Pass 3. Every rendering follows these beats.

## 1. Reader before and after

- **Before:** a technical reader (school maths and science, basic programming), new to climate physics. Knows watts, kelvin, molecules, wavelengths, that hotter things radiate more, that a gas cools when it expands.
- **After:** "The Earth must emit 240 W/m² to space, which fixes the temperature of the air that emits it at 255 K. Greenhouse gases move that emitting air up to about 5 km, and the surface is 6.5 K warmer per km below it. More gas raises the emitting air, so the surface warms."

## 2. Question and motive

- **Question:** How do greenhouse gases warm the Earth? Result in words: they make the Earth emit its infrared to space from high, cold air instead of from the warm surface; to emit enough from cold air, the whole column (and the surface) must be warmer.
- **Why care:** the familiar "trapping heat" picture cannot say how much, and it suggests the effect stops once CO₂ absorbs everything. The correct picture gives numbers and answers that objection.
- **Why this approach:** start from energy conservation, the one thing no reader doubts. It gives a temperature (255 K) that disagrees with the measured 288 K. The 33 K gap is the thing to explain.

## 3. Introduction ledger

| Reference | Means | Grounded by (a concrete instance) | Beat |
|---|---|---|---|
| W/m² | power per square metre of the Earth's surface | 1361 W/m² of sunlight on a panel facing the Sun | 2 |
| albedo | fraction of sunlight reflected | 0.30 → 30% of 340 W/m² reflected | 2 |
| energy balance | absorbed = emitted | 240 in, 240 out | 2 |
| σT⁴ (Stefan–Boltzmann) | power per m² a body emits at temperature T | 255 K → 240 W/m²; 288 K → 390 W/m² | 2 |
| emission temperature | 255 K, the temperature that emits 240 W/m² | σ·255⁴ ≈ 240 | 2 |
| infrared | radiation the Earth emits, near 10 µm | sunlight peaks near 0.5 µm, 20× shorter | 3 |
| greenhouse gas | gas that absorbs and emits infrared | CO₂, water vapour, methane; not N₂, O₂ | 3 |
| emission height | average height from which infrared escapes to space | ≈ 5 km | 4 |
| lapse rate | temperature drop per km of height, 6.5 K/km | 288 − 6.5 × 5 ≈ 255 | 4 |
| radiative forcing | imbalance right after a change, before warming | 3.7 W/m² for doubled CO₂ | 5 |

## 4. Beats

| # | Kind | Reader's question | Bridge | Shown | Said | Reader now knows |
|---|---|---|---|---|---|---|
| 1 | hook | How do greenhouse gases warm the Earth? | — | answer in two sentences | gases move the emission of infrared up into cold air; the surface must be warmer so that cold air emits enough | the result in words |
| 2 | instance | What temperature would the Earth have without them? | start from energy | sunlight 1361 W/m² on a panel facing the Sun; ÷4 because a disc πR² catches it and a sphere 4πR² emits (without ÷4: 360 K); albedo 0.30 reflected → 240 W/m² absorbed; σT⁴ = power per m² a body emits at temperature T; σT⁴ = 240 → 255 K. Measured surface: 288 K | energy balance fixes 255 K for whatever emits to space; the measured surface is 288 K | 33 K to explain |
| 3 | name | What is different about greenhouse gases? | so the atmosphere must change where the emission comes from | sunlight 0.5 µm vs infrared 10 µm (a cooler body emits at longer wavelengths); CO₂, water vapour, methane absorb infrared; N₂, O₂ do not | the gases pass sunlight, absorb and re-emit infrared | the gases act on outgoing infrared only |
| 4 | mechanism | Then where does the 240 W/m² leave from? | but absorbed infrared is re-emitted in all directions; only infrared emitted where little gas remains above gets out | table: height vs temperature | the air that emits to space must emit 240 W/m², so it must be 255 K. Measured air reaches 255 K about 5 km up: the emission height. Air cools 6.5 K/km because rising air expands and cools, and convection keeps this profile. 255 + 6.5 × 5 ≈ 288 | the 33 K is the lapse rate times the emission height |
| 5 | objection | The surface emits σ·288⁴ ≈ 390 W/m², but only 240 leaves the top. Where does the rest go? | but | surface budget, each term named | the air emits 330 W/m² of infrared down. Surface gains 160 sunlight + 330 from the air; loses 390 infrared + 100 carried up by rising warm air and evaporation | the numbers add up |
| 6 | test (predict) | What happens when CO₂ doubles (280 → 560 ppm)? | therefore | prediction prompt, then: emission height rises ≈ 150 m; that air is 1 K colder; it emits 3.7 W/m² less, the radiative forcing; the Earth warms until the emitting air is 255 K: surface ≈ 1 K warmer. One line: water vapour and other feedbacks raise this to ≈ 3 K (out of scope) | more gas → higher → colder → less out → warm | the causal chain with numbers |
| 7 | test | Does more gas always warm? | but the mechanism needs colder air above | isothermal case | if air had the same temperature at every height, the higher emitting air would still be 255 K: outgoing unchanged, no warming | the assumption that matters |
| 8 | objection | Isn't CO₂ already saturated? | so | 280 → 560 ppm: 3.7 W/m²; 560 → 1120 ppm: 3.7 W/m² again | saturation near the ground does not matter, because escape happens high up, where the gas is thin; more gas still lifts the emission height. Each doubling adds about the same forcing | the saturation answer |
| 9 | close | — | so | recap | "Greenhouse gases move the Earth's emission to space up to about 5 km, where the air is 33 K colder than the surface. Energy balance holds that air at 255 K, so the surface sits at 288 K. More gas lifts the emission height and warms the surface." Scope: feedbacks, carbon cycle, timing | the "after" sentence |

## 5. Concrete to symbol

σT⁴: first 255 K → 240 W/m² and 288 K → 390 W/m², then the symbol with σ = 5.67×10⁻⁸. Surface = 255 + 6.5 × h: first with h = 5 km (288 K), then h = 5.15 km (289 K).

## 6. Links between representations

The height-temperature table and the sentence "255 K at 5 km" use the same numbers; the doubled-CO₂ row repeats the table with the emission height moved.

## 7. Close the loop

- **Answer:** Greenhouse gases make the Earth emit to space from high, cold air. Energy balance holds that air at 255 K, and the lapse rate makes the surface warmer by 6.5 K per km below it.
- **General argument:** any change that raises the emission height, while temperature falls with height, warms the surface.
- **Payoff:** the reader can predict the effect of more CO₂, of no lapse rate, and answer the saturation objection. Scope: feedbacks, carbon cycle, timing.
