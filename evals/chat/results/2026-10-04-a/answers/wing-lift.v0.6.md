# How does an airplane wing make lift?

_v0.6_

**Short answer:** A wing pushes air downward. The air pushes the wing upward with an equal force (Newton's third law). The upward push takes the form of a pressure difference: lower pressure above the wing, higher pressure below it. "The wing deflects air down" and "the pressure is lower on top" are two descriptions of one event. They are not two competing theories.

## The causal chain

1. **The wing meets the air at an angle.** This angle is the *angle of attack*: the angle between the wing's chord (the line from its front edge to its back edge) and the oncoming air. A curved (*cambered*) wing adds to the effect, so it can make lift even at zero angle.

2. **The air follows the wing's surfaces and leaves the back edge moving downward.** This downward flow is called *downwash*. The sharp trailing edge makes the flow from the top and the bottom leave smoothly in the same direction.

3. **Air bends only if a pressure difference pushes it.** A fluid moves in a curve only when the pressure on the outside of the curve is higher than the pressure on the inside. Above the wing, the air curves down over the surface. So the pressure next to the upper surface must be *lower* than the pressure in the surrounding air. Below the wing, the air is pushed down and aside, so the pressure there is *higher*.

4. **The pressure difference, summed over the wing area, is the lift force.** At the same time, the wing has given the air downward momentum each second. These two quantities are equal (momentum conservation).

5. **Speed follows from pressure.** Air that moves from high pressure into low pressure speeds up (Bernoulli's principle). So the air over the top moves faster *because* the pressure there is low. The speed is a consequence of the bending, not the original cause.

## A common wrong explanation

Many textbooks claim that air over the longer top surface must "meet up" with the air underneath at the trailing edge, so it has to go faster. No physical law requires this. Measurements show the opposite: the upper air arrives at the trailing edge *before* the lower air. This explanation also fails to account for flat wings, paper airplanes, and aircraft flying upside down. All of these make lift through angle of attack.

## Worked example: a small aircraft in level flight

Take a Cessna 172 (established values, rounded):

| Quantity | Value |
|---|---|
| Weight | ≈ 9,800 N (1,000 kg) |
| Wing area *S* | 16.2 m² |
| Cruise speed *v* | 60 m/s |
| Air density *ρ* (sea level) | 1.225 kg/m³ |

**Average pressure difference** = weight ÷ area = 9,800 / 16.2 ≈ **600 Pa**.
Atmospheric pressure is about 101,000 Pa, so a difference of only **0.6%** holds the aircraft up. A small pressure difference over a large area makes a large force.

**Lift equation (a definition plus a measured coefficient):** L = ½ρv² · S · C_L.
- ½ρv² = 0.5 × 1.225 × 60² ≈ 2,200 Pa. This is the *dynamic pressure*, the pressure the oncoming air can supply.
- To lift 9,800 N: C_L = 9,800 / (2,200 × 16.2) ≈ **0.27**.

C_L (the *lift coefficient*) measures how effectively the wing turns airflow into lift. Below the stall, it grows roughly in proportion to angle of attack, by about 0.1 per degree for a typical wing. A value of 0.27 means a few degrees of angle at cruise.

**What changes when variables change:**
- **Halve the speed** → dynamic pressure falls to ¼. To keep the lift, the pilot must make C_L 4× larger, which requires a much larger angle. This is why aircraft fly nose-high at slow speed and extend flaps on landing (flaps add camber and raise C_L).
- **Fly at higher altitude** → the air is less dense, so the aircraft must fly faster or at a larger angle.

## Where it breaks: the stall

Lift rises with angle of attack only to about **15°** for a typical wing. Above that angle, the air cannot follow the sharply curved upper surface. It separates from the surface into a turbulent wake. The air no longer bends down over the top, so the low pressure there collapses and lift drops suddenly. This is a *stall*. It depends on angle, not speed. A wing can stall at any speed if the angle is too large.

**Scope:** I left out how lift is distributed along the span, wingtip vortices, induced drag, and the math of circulation (Kutta–Joukowski theorem). Any aerodynamics textbook covers these next. Anderson's *Introduction to Flight* is one example.
