# How do greenhouse gases warm the Earth?

<!-- Stage 1, rendered from model.md in STE-80. -->

**Greenhouse gases make the Earth radiate its energy to space from high, cold air instead of from the warm surface. Cold air emits less, so the whole lower atmosphere, and the surface with it, must be warmer before enough energy leaves.**

The rest of this page puts numbers on each step.

## 1. Without greenhouse gases: 255 K

<!-- claim: balance-255 -->
Start from conservation of energy. Over years, the Earth must emit as much power to space as it absorbs from the Sun. This is the **energy balance**.

- Sunlight delivers 1361 W/m² to a panel that faces the Sun.
- The Earth catches sunlight on a disc of area πR², but it emits from its whole sphere, of area 4πR². Per square metre of surface, the average input is 1361 / 4 = 340 W/m².
- The **albedo** is the fraction of sunlight that clouds, ice, and ground reflect straight back to space: 0.30. The Earth absorbs 340 × 0.70 ≈ 240 W/m².

A body at temperature T emits σT⁴ watts per square metre (the Stefan–Boltzmann law, σ = 5.67 × 10⁻⁸ W m⁻² K⁻⁴). Emission grows fast with temperature: 255 K emits 240 W/m², and 288 K emits 390 W/m².

Set σT⁴ = 240 W/m² and solve: T = 255 K (−18 °C). This is the **emission temperature**: whatever emits the Earth's energy to space must be at 255 K. If the surface emitted directly to space, the surface would be at 255 K.

<!-- claim: why-divide-4 -->
The division by 4 matters: with 1361 × 0.70 instead, T = 360 K (87 °C), as if every point on Earth faced the noon Sun all day.

The measured average surface temperature is 288 K (15 °C). The surface is 33 K warmer than the emission temperature. The greenhouse gases cause that 33 K.

## 2. What greenhouse gases do

<!-- claim: which-gases -->
Sunlight peaks near 0.5 µm, in the visible. The Earth is far cooler than the Sun, so it emits at longer wavelengths, near 10 µm. This is **infrared**: invisible radiation from the ground and the air.

A **greenhouse gas** lets most sunlight pass but absorbs and emits infrared. Water vapour, CO₂, and methane are greenhouse gases. Nitrogen and oxygen, 99% of dry air, are not: they barely absorb infrared at all.

So sunlight reaches the ground. But infrared from the ground is absorbed by the air above it and emitted again, in all directions, at the temperature of that air.

## 3. Where the infrared escapes: 5 km up

<!-- claim: emission-height -->
Infrared reaches space only from air that has little greenhouse gas above it. Lower down, the air above absorbs it again. Infrared really escapes from a spread of heights, which differ by wavelength. Call their average the **emission height**.

The air at the emission height must emit 240 W/m², so it must be at the emission temperature, 255 K.

The air gets colder with height. Rising air expands and cools, and convection keeps mixing the lower atmosphere. The measured fall is about 6.5 K per km, the **lapse rate**. At this rate, the air reaches 255 K about 5 km up. That is the emission height.

| Height | Temperature |
|---|---|
| 0 km (surface) | 288 K |
| 5 km (emission height) | 255 K |

Now the 33 K has a cause: 255 K + 6.5 K/km × 5 km ≈ 288 K. The surface is warmer than the emitting air because it sits 5 km below it.

<!-- claim: surface-budget -->
The surface at 288 K emits 390 W/m², more than the 240 W/m² that leaves the top. The surface does not lose that much, because the warm air just above it emits about 330 W/m² of infrared back down (a measured value).

## 4. Adding CO₂

**Predict first:** CO₂ doubles, from its pre-industrial 280 ppm to 560 ppm. What happens to the emission height, and then to the surface?

<!-- claim: more-gas-warms -->
1. More gas means the infrared must start higher before little gas remains above it. The emission height rises, on average by about 150 m (a result of radiation calculations).
2. The air 150 m higher is about 1 K colder (6.5 K/km × 0.15 km).
3. Colder air emits less: σ·254⁴ ≈ 236 W/m², against 240 W/m² at 255 K. The Earth now emits about 3.7 W/m² less than it absorbs. This imbalance, just after the change and before any warming, is the **radiative forcing**. It is small next to 240 W/m², but it persists every second until something changes.
4. The Earth gains energy and warms. Convection still sets the lapse rate, so the temperature at every height rises by the same amount. (This assumes the lapse rate stays at 6.5 K/km; in reality it changes a little, one of the feedbacks below.)
5. Warming stops when the air at the new emission height is back at 255 K. The surface is then about 1 K warmer, because it now sits 150 m further below the emitting air.

This 1 K counts only this mechanism. Warmer air holds more water vapour, which is itself a greenhouse gas; with this and other feedbacks, the estimated warming per doubling is about 3 K, likely 2.5–4 K (assessment of the Intergovernmental Panel on Climate Change, IPCC, from models and observations).

## 5. The condition: colder air above

<!-- claim: why-not-blanket -->
The usual picture, "greenhouse gases trap heat like a blanket", says more gas always warms. A test case shows that it does not.

Suppose the atmosphere had the same temperature at every height (a lapse rate of 0). Add CO₂. The emission height still rises, but the air there is still 255 K. It emits the same 240 W/m². There is no imbalance and no warming.

So the warming depends on two things together: the gas lifts the emission height, and the air is colder higher up.

## 6. "But CO₂ is already saturated"

<!-- claim: saturation -->
Near the ground, CO₂ already absorbs almost all infrared at its main wavelength (15 µm). People conclude that more CO₂ can do nothing. But what reaches space is decided high up, not near the ground. High up, the air is thin, and infrared emitted there still escapes. Add CO₂, and that thin air absorbs more, so the escape moves up again, to colder air. Each doubling adds about the same forcing: 280 → 560 ppm gives 3.7 W/m², and 560 → 1120 ppm gives 3.7 W/m² again. Today's 420 ppm gives about 2.2 W/m².

## Summary

Energy balance requires the Earth to emit 240 W/m² to space, which holds the emitting air at 255 K. Greenhouse gases move that emitting air up to about 5 km. The lapse rate of 6.5 K/km makes the surface 33 K warmer, at 288 K. More greenhouse gas lifts the emission height and warms the surface.

## Not covered here

- Feedbacks in detail (water vapour, clouds, ice): IPCC AR6 Working Group I, Chapter 7.
- Why only some molecules absorb infrared: a molecular spectroscopy text.
- Why each doubling gives the same forcing: Pierrehumbert, *Principles of Planetary Climate*.
- Where added CO₂ goes (the carbon cycle), and how fast the ocean lets the surface warm.
