# How does an airplane wing make lift?

_v0.5_

# How a wing makes lift

**Short answer:** A wing pushes air downward. The air pushes the wing upward with an equal force. This force shows up as a pressure difference: the air pressure on the top of the wing is lower than the pressure on the bottom.

## The mechanism, step by step

1. **The wing meets the air at an angle.** This angle is the *angle of attack*: the angle between the wing and the oncoming airflow. Most wings also have a curved top surface.
2. **The air follows the wing's shape.** Air that flows over the top curves down along the surface. Air that flows under the bottom is deflected down by the tilted surface.
3. **Curved flow needs a pressure difference.** Air moves in a curve only when a force pushes it toward the inside of the curve. Above the wing, the curve bends toward the wing. So the pressure next to the top surface must be lower than the pressure farther away.
4. **The wing has low pressure on top and higher pressure below.** The difference, multiplied by the wing area, is the lift force.
5. **The air leaves the wing moving downward.** This downward flow is *downwash*. The wing gives the air downward momentum, so the air gives the wing upward force (Newton's third law).

Steps 4 and 5 are not two separate causes. They describe the same force. The pressure difference is how the wing pushes on the air, and the downwash is the result. (Established fact.)

## A worked example

A Cessna 172 (a small four-seat airplane) in level flight:

| Quantity | Value |
|---|---|
| Weight | about 1,100 kg → about 10,800 N |
| Wing area | 16.2 m² |
| Lift needed per m² | 10,800 / 16.2 ≈ **670 Pa** |
| Normal air pressure at sea level | 101,325 Pa |

So the wing needs a pressure difference of only about **0.7%** of normal air pressure. A very small pressure difference, spread over a large area, holds up the airplane.

## What controls the amount of lift

Engineers use this equation:

**L = ½ × ρ × v² × S × C_L**

- *ρ* (rho): air density. Thinner air at altitude gives less lift.
- *v*: airspeed. Lift grows with the **square** of speed. Twice the speed gives four times the lift.
- *S*: wing area.
- *C_L*: lift coefficient, a number that depends mainly on angle of attack and wing shape.

For the Cessna at about 55 m/s: ½ × 1.225 × 55² ≈ 1,850 Pa. The wing needs 670 Pa, so C_L ≈ 0.36. When the airplane flies slower (for example, to land), the pilot must increase C_L. The pilot raises the nose (more angle of attack) or extends flaps.

## Where the rule fails: stall

More angle of attack gives more lift, **up to a limit**.

- **Holds:** From 0° to about 15°, each extra degree adds lift.
- **Fails:** Above about 15° (the exact value depends on the wing), the air cannot follow the curved top surface. The flow separates and becomes turbulent. The low-pressure region collapses, and lift drops suddenly. This is a *stall*.

## A common wrong explanation

Many books say: "Air on top travels farther, so it must go faster to meet the bottom air at the trailing edge." This *equal transit time* idea is **false**.

- Air on top does go faster. But it goes much faster than the "meet again" rule predicts. In wind tunnels, it arrives at the trailing edge **before** the air from below. (Observation.)
- No physical law requires the two parcels of air to meet again.
- A flat, uncurved plate also makes lift at an angle of attack. Paper airplanes and aerobatic airplanes that fly upside down show this. So the curved shape helps, but it is not the root cause.

The faster air on top and the lower pressure on top occur together. Bernoulli's principle connects them correctly. The equal-transit argument only gives a wrong reason for the speed.

## What this explanation leaves out

- **Why the air follows the curved surface, and how much lift results.** The full answer uses *circulation* and the *Kutta condition* (the rule that flow leaves the sharp trailing edge smoothly). Look up "Kutta–Joukowski theorem."
- **Wingtip vortices and induced drag.** These are a cost of making lift with a wing of finite length.
- **Supersonic flight**, where air compressibility changes the picture.
