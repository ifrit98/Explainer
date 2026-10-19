# Semantic model: two high tides a day

> Source of truth. Every rendering derives from this file.

## Central question

Why does a point on the coast get two high tides a day, not one, when the Moon is on only one side of Earth?

## Audience and prior knowledge

A technical reader: school mathematics and science (Newton's law of gravity, inverse-square, acceleration), basic programming. New to tides. Knows that the Moon causes tides. Does not know that only the *difference* in pull matters, or why there is a bulge on the side away from the Moon.

## Entities

| Entity | Definition (one sentence) | Status |
|---|---|---|
| Moon's pull | Gravitational acceleration toward the Moon, GM/r², at a given point. | fact |
| Earth's centre | The point whose acceleration describes how Earth as a whole falls toward the Moon. | fact |
| Tidal acceleration | Moon's pull at a point minus Moon's pull at Earth's centre. | definition |
| Near bulge | Ocean bulge on the side facing the Moon. | fact (idealized) |
| Far bulge | Ocean bulge on the side away from the Moon. | fact (idealized) |
| Lunar day | Time for a point on Earth to return under the Moon: 24 h 50 min. | fact |

## Relationships

| From | Relationship | To | Notes |
|---|---|---|---|
| Moon's pull | falls off with distance (1/r²) | near side > centre > far side | |
| Earth's centre | sets the pull that the whole Earth follows | tidal acceleration | uniform part gives no tide |
| Tidal acceleration | points away from Earth's centre on both sides | near bulge, far bulge | |
| Earth's rotation | carries a point through both bulges | two high tides per lunar day | |

## Causal chain

```text
pull falls with distance → near side pulled more than centre, far side less
→ relative to Earth's centre, near water moves toward Moon, far water lags behind (away)
→ two bulges on opposite sides → Earth rotates under both → two high tides per 24 h 50 min
```

## Quantities

Constants: G = 6.674e-11, Moon mass 7.35e22 kg, distance 384,400 km, Earth radius 6,371 km.

| Point | Distance to Moon | Moon's pull (m/s²) | Minus centre (m/s²) |
|---|---|---|---|
| Near side | 378,029 km | 3.433e-5 | +1.13e-6 (toward Moon) |
| Centre | 384,400 km | 3.320e-5 | 0 |
| Far side | 390,771 km | 3.213e-5 | −1.07e-6 (away from Moon, relative) |

Approximation: tidal acceleration ≈ 2GMR/d³ = 1.10e-6 m/s², about one ten-millionth of g (9.81).

Sun check: Sun's pull on Earth 5.93e-3 m/s², 179× the Moon's; Sun's tidal acceleration 5.05e-7 m/s², 0.46 of the Moon's. Tide follows 1/d³, the difference, not 1/d², the pull.

Timing: Moon moves about 12.2° per day along its orbit, so a lunar day is 24 h 50 min, and high tides come every 12 h 25 min.

## Why this form

| Operation | Simplest alternative | What the alternative breaks |
|---|---|---|
| Subtract the pull at Earth's centre | Use the raw pull: water flows toward the Moon | Raw pull is toward the Moon everywhere (3.2e-5 to 3.4e-5), predicting one bulge and one high tide a day. Observation: two. Also predicts Sun tides 179× the Moon's; observed is about 0.46×. |

## Concrete cases

| Claim | Holds here | Breaks here |
|---|---|---|
| Uniform pull makes no tide | Whole Earth accelerates at 3.320e-5 toward Moon; that part moves water and rock together. | If pull were the same at all points (no 1/r² fall-off), the difference would be 0: no bulges. |
| Two bulges → two highs | Rotation of 360° relative to the Moon in 24 h 50 min passes two bulges 180° apart: highs 12 h 25 min apart. | Real basins: some coasts (parts of the Gulf of Mexico) get one high tide a day, because basin shape and Moon's tilt change the response. |

## Terms

- **Pull**: the Moon's gravitational acceleration at one point.
- **Tidal acceleration**: pull at a point minus pull at Earth's centre. Small value (1e-6 m/s²) yet enough to raise water about half a metre in the idealized ocean.
- **Bulge**: region where water is higher than average.
- **Lunar day**: 24 h 50 min.

## Epistemic status

- **Established:** two bulges in the equilibrium model; lunar day 24 h 50 min; Sun/Moon ratio 0.46.
- **Mathematical consequence:** near/far tidal accelerations from Newton's law.
- **Assumed:** idealized ocean covering Earth, responding instantly (equilibrium tide).
- **Estimate:** idealized lunar tide range about 0.5 m.

## Confusion points

- "The Moon pulls water toward it, so one bulge." → Earth is pulled too; only the difference shapes the water.
- "Far bulge is from centrifugal force of Earth spinning." → Earth's daily spin is the same everywhere around the equator; it shapes Earth's equator, not the tides. The cause is the pull difference.
- "Far side is pushed away." → Nothing pushes. The far side is pulled toward the Moon, but less than Earth's centre, so it falls behind.

## Scope

- **Out of scope:** spring and neap tides (Sun and Moon aligned or at right angles) — pointer: add the Sun's bulges, 0.46 of the Moon's.
- **Out of scope:** real tide heights and timing (resonance, continents, Bay of Fundy) — pointer: dynamic tide theory, harmonic tide prediction.
- **Out of scope:** unequal pairs of highs (diurnal inequality) from the Moon's tilt.

## Representation decision

- **Stage:** 1
- **Reason:** A short causal chain with one table of numbers; the geometry fits in one small text figure.
- **Levels:** L1 two bulges, Earth turns under them / L2 pull differs across Earth / L3 subtract the centre's pull, Sun check.
