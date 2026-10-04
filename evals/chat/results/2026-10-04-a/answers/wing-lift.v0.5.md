# How does an airplane wing make lift?

_v0.5_

# How a wing makes lift

**Short answer:** A wing turns the air that flows past it downward. To turn the air, the wing must push on it. The air pushes back on the wing with an equal force, and that force points mostly up. We call it **lift**.

Lift has two descriptions, a pressure description and a momentum description. Both describe the same event.

## The mechanism, step by step

1. **The wing meets the air at an angle.** The **angle of attack** is the angle between the wing and the oncoming air. It is usually a few degrees. A curved wing (**camber**) has a similar effect.
2. **The air follows the wing's shape.** Air flowing over the top follows the curved upper surface, and it leaves the trailing edge pointing downward. Air below the wing is also deflected down.
3. **Curved flow needs a pressure difference.** Air moves in a curve only when the pressure on the outside of the curve is higher than the pressure on the inside. The flow over the top curves around the wing, so the pressure next to the upper surface drops below atmospheric pressure. The pressure under the wing rises a little above it.
4. **The pressure difference pushes the wing up.** There is more pressure below than above, so the net force on the wing points up. The low pressure on top usually gives most of the lift.
5. **The air goes down, so the wing goes up.** The wing sends a large mass of air downward each second. This flow is called **downwash**. By Newton's third law, the force that pushes the air down equals the force that pushes the wing up.

```text
   lower pressure  ↑ lift
   ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
 → ──────────╭──────────────╮_______                →  air leaves
 →          (       wing          ‾‾‾‾‾‾──__            pointing down
 → ──────────╰─────────────────────────────‾‾──     ↘  (downwash)
   higher pressure
```

Steps 3–4 (pressure) and step 5 (momentum) are not two separate sources of lift. They are two ways to count one force. If you add both, you count the force twice.

## How big is the effect? (worked numbers)

The lift equation summarizes the mechanism:

**L = ½ · ρ · v² · S · C_L**

- ρ is the air density, 1.225 kg/m³ at sea level.
- v is the airspeed.
- S is the wing area.
- C_L is the **lift coefficient**. It increases with angle of attack and camber.

**Example: a Cessna 172** (established values, rounded):
- The weight is about 1,100 kg × 9.8 m/s² ≈ 10,800 N.
- The wing area is 16.2 m². The cruise speed is about 50 m/s.
- ½ · 1.225 · 50² = 1,531 Pa. Multiply by 16.2 m² to get 24,800 N.
- The lift must equal the weight, so C_L = 10,800 / 24,800 ≈ **0.44**. This is a gentle angle of attack.

**What the numbers tell you:**
- **Speed has a strong effect.** Lift increases with v². If you double the airspeed, you get four times the lift. A slow aircraft must fly at a higher angle of attack to stay up.
- **The pressure difference is small.** A Boeing 747 weighs about 3.9 MN at takeoff and has 525 m² of wing. The mean pressure difference is about 7,500 Pa, or about 7% of atmospheric pressure. A small pressure difference over a large area holds the aircraft up.

## Where the guarantee breaks: stall

A larger angle of attack gives more lift, **but only up to a limit**. At about 15° on a typical wing, the air can no longer follow the steep upper surface. The flow separates and becomes turbulent. The wing then turns less air downward, and lift drops suddenly. This event is a **stall**. A stall depends on angle, not on speed. But a slow aircraft needs a high angle, so a slow aircraft is close to the stall angle.

## A common wrong explanation

The **equal transit time** explanation says this: "Air over the top must meet the air below at the trailing edge. The top path is longer, so the air on top goes faster." This explanation is false.

- Nothing forces the two parcels of air to meet again. Measurements and smoke tests show that air over the top arrives at the trailing edge **earlier** than air below. (Observation.)
- The explanation cannot explain why an aircraft can fly upside down, or why a flat sheet at an angle makes lift.

The air on top *does* move faster, and Bernoulli's principle does connect the higher speed to the lower pressure. The error is only the claimed *reason* for the higher speed. The true reason is the curved flow and the pressure field in step 3.

## Out of scope

This answer does not cover these topics:
- **Circulation and the Kutta condition.** These give the mathematical model that predicts lift exactly.
- **Induced drag and wingtip vortices.** These are the cost of making downwash.
- **Flaps and slats.** These increase C_L for takeoff and landing.
- **Compressibility effects** near the speed of sound.
