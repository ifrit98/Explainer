# Semantic model: two high tides a day

> Source of truth. Every rendering derives from this file.

## Central question

Why does a place on the coast get two high tides a day, when there is only one Moon pulling on one side of the Earth?

## Audience and prior knowledge

A technical reader: school mathematics and science (Newton's law of gravity, inverse-square law, acceleration, vectors, free fall), basic programming. New to tides. Knows the Moon causes tides and that the Earth spins once a day. Does not know the idea of a tidal acceleration, or why the far side of the Earth has a bulge.

## Entities

| Entity | Definition (one sentence) | Status |
|---|---|---|
| Earth | A ball of rock of radius 6371 km, covered mostly by ocean. | fact |
| Moon | The body that causes most of the tide, 384,400 km from Earth's centre on average. | fact |
| Moon's pull | The acceleration the Moon's gravity gives an object at a point; it points at the Moon and falls with the square of distance. | established fact (Newton) |
| near side | The point on Earth's surface that faces the Moon, 6371 km closer than the centre. | definition |
| far side | The point on Earth's surface opposite the Moon, 6371 km farther than the centre. | definition |
| side point | A surface point 90° from the near side; 384,453 km from the Moon. | definition |
| tidal acceleration | The Moon's pull at a point minus the Moon's pull at Earth's centre (a vector subtraction). | definition |
| bulge | Water gathered on the Earth–Moon line, because there the tidal acceleration points outward and along the surface it points toward the line. There are two: under the Moon and opposite the Moon. | model output (ideal ocean) |
| high tide | The time when a place passes through a bulge and its water level is highest. | observation |
| lunar day | 24 h 50 min: the time for the Moon to come back to the same place in the sky. | fact |

## Relationships

| From | Relationship (verb) | To | Notes |
|---|---|---|---|
| Moon's pull | accelerates | the whole Earth | Earth falls freely toward the Moon (as part of its orbit around the shared centre of mass). |
| Earth's free fall | cancels | the Moon's pull at the centre (33.19 µm/s²) | Earth's centre accelerates at 33.19 µm/s²; relative to the centre, each point feels only its own pull minus 33.19. |
| tidal acceleration | points away from Earth's centre at | near side and far side | Stretches Earth along the Earth–Moon line. |
| tidal acceleration | points toward Earth's centre at | the sides (90° from the Moon) | Squeezes in the other direction. Half the size. |
| tidal acceleration | moves water toward | the two bulges | Its sideways part along the surface moves the water. |
| Earth's rotation | carries a place through | both bulges each lunar day | Two high tides. |

## Dependencies (learning order)

1. The Moon's pull is weaker farther from the Moon (inverse square).
2. The whole Earth falls toward the Moon, so the pull it shares with every part does nothing to its shape.
3. Tidal acceleration = pull at a point − pull at the centre.
4. The tidal acceleration points away from the centre on both the near side and the far side → two bulges.
5. The Earth turns under the two bulges → two high tides per lunar day.

## Causal chain

```text
pull falls with distance → near side pulled more than centre, centre more than far side
→ Earth falls as a whole, so only the tidal acceleration acts
→ near side pulled ahead of centre; far side left behind centre
→ water stretched into two bulges on the Earth–Moon line
→ Earth turns under both bulges → two high tides each 24 h 50 min
```

## Temporal sequence

1. A place passes under the Moon: high tide (near-side bulge).
2. About 6 h 12 min later the place is 90° away: low tide.
3. About 12 h 25 min after the first, the place is on the far side: second high tide (far-side bulge).
4. About 24 h 50 min after the first, the place is under the Moon again.

## Quantities

Constants: GM of Moon = 4.905 × 10¹² m³/s²; Earth–Moon distance d = 384,400 km; Earth radius R = 6371 km; GM of Sun = 1.327 × 10²⁰ m³/s²; Earth–Sun distance 1.496 × 10⁸ km.

Moon's pull, a = GM/r², in µm/s² (1 µm/s² = 10⁻⁶ m/s²):

| Point | Distance to Moon (km) | Moon's pull (µm/s²) | Pull minus centre's pull (µm/s²) |
|---|---|---|---|
| near side | 378,029 | 34.32 | +1.13 (toward Moon) |
| centre | 384,400 | 33.19 | 0 |
| far side | 390,771 | 32.12 | 1.07 away from Moon (−1.07) |
| side point | 384,453 | 33.18, tilted 0.95° toward the centre | 0.55 toward Earth's centre |

- Side point: its pull has almost the same size as the centre's, but it points at the Moon, so it is tilted by R/d = 0.0166 rad toward Earth's centre. The vector difference is 33.19 × 0.0166 = 0.55 µm/s², pointing down.
- On the Earth–Moon line, GM/(d−R)² − GM/d² ≈ (GM/d²)(2R/d) = 2GMR/d³ = 1.10 µm/s². The exact values 1.13 and 1.07 differ from this by about 3%. The factor 1/d³ means the tidal acceleration falls with the cube of distance.
- Sideways part (along the surface): (3/2)(GMR/d³) sin 2θ, θ the angle from the near side. 0 at 0° and 90°; largest at 45°, 0.82 µm/s², pointing toward the nearer bulge. This part moves water.
- Meaning: 1.1 µm/s² is about one ten-millionth (1.1 × 10⁻⁷) of g = 9.81 m/s². Up or down, it changes weight by a negligible amount. Sideways, nothing opposes it except the slope of the sea, so over a whole ocean it gathers water into the bulges. Low value: zero at the centre. High value: near and far sides (up), 45° points (sideways).
- Sun: pull on Earth 5930 µm/s², about 179 times the Moon's pull. Sun's tidal acceleration ≈ 0.51 µm/s², about 0.46 of the Moon's, because the Sun is 389 times farther and the tidal acceleration falls as 1/d³. Check: tidal acceleration ≈ pull × 2R/d, so Sun/Moon ≈ 179 / 389 = 0.46.
- Why the vertical part does nothing and the sideways part acts: vertically the tidal acceleration adds to g = 9.81 m/s² and changes weight by 1 part in 10 million. Along a level surface gravity has no component, so the tidal acceleration is the only sideways push; water flows until the slope of the sea balances it.
- Near/far asymmetry: 1.13 vs 1.07, about 5% apart, because the pull changes faster closer to the Moon. Too small to matter here.
- Lunar day: the Earth turns about 15° an hour; the Moon moves about 12° per day along its orbit, in the same direction Earth turns, so Earth needs about 50 min more than 24 h to face the Moon again: 24 h 50 min. Two high tides per lunar day → one each 12 h 25 min.

## Alternative states

| State / scenario | What changes | Why |
|---|---|---|
| Earth held fixed (not falling toward the Moon) | One bulge only, under the Moon. The far side pull (32.12 µm/s²) points toward the Moon, that is down into the Earth. | Nothing subtracts the centre's pull; every point is pulled Moonward. |
| Uniform pull (same at every point) | No tide at all. | Every part falls together; 33.19 − 33.19 = 0 at every point. |
| Sun instead of Moon | Smaller tide (0.46×) despite 179× stronger pull. | Tide follows the tidal acceleration, which falls as 1/d³. |
| Earth falls straight at the Moon (no orbit) | Same two bulges: +1.13 and −1.07. | The pulls at the three points depend only on distance, not on orbital motion. |

## Why this form

| Operation | Simplest alternative | What the alternative breaks (with numbers) |
|---|---|---|
| Subtract the centre's pull | Use the Moon's pull itself as the cause of the tide | Predicts one bulge (all three points pulled Moonward: 34.32, 33.19, 32.12 µm/s²), and predicts the Sun's tide 179× the Moon's. Observed: two bulges, Sun's tide about half the Moon's. |

## Concrete cases

| Claim | Holds here (numbers) | Breaks here, without its assumption (numbers) |
|---|---|---|
| The far side is stretched away from the Moon (assumption: Earth falls freely toward the Moon) | Centre pulled 33.19, far side 32.12 µm/s²: the far side is left behind by 1.07 µm/s². | Earth held fixed: far side pulled 32.12 µm/s² toward the Moon and into the Earth; no far bulge. |
| Two bulges give two high tides a day (assumption: Earth turns under the Moon) | Earth turns once per 24 h 50 min relative to the Moon → high tide every 12 h 25 min. | — (the rotation is an observation; no alternative needed) |
| Mechanism: subtraction | 34.32 − 33.19 = +1.13; 32.12 − 33.19 = −1.07; side 0.55 inward. | — |

## Terms

- **Moon's pull**: the acceleration toward the Moon at a point, from Newton's law. Example 33.19 µm/s² at Earth's centre.
- **tidal acceleration**: Moon's pull at a point minus Moon's pull at the centre. Zero at the centre; +1.13 µm/s² at the near side.
- **near side / far side**: the surface points nearest to / farthest from the Moon.
- **bulge**: raised ocean on the Earth–Moon line; two of them.
- **high tide**: the time a place passes through a bulge.
- **side point**: a surface point 90° from the near side; tidal acceleration 0.55 µm/s² toward the centre.
- **lunar day**: 24 h 50 min; the time for the Moon to come back to the same place in the sky.

## Epistemic status

- **Observed / established:** Most coasts have two high tides per 24 h 50 min. Newton's law of gravity.
- **Mathematical consequence:** The tidal acceleration points outward on both near and far sides, with nearly equal size (1.13 vs 1.07).
- **Assumed:** Equilibrium tide: ocean covers the Earth and responds at once to the tidal acceleration. Real oceans do not; see Scope.
- **Estimated:** Equilibrium bulge height about 0.36 m above the mean at its peak (range about 0.5 m).

## Confusion points

- "The Moon pushes the far side away" → No. The Moon pulls the far side, but less than it pulls the centre. The far side is left behind.
- "The far bulge comes from centrifugal force of the Earth–Moon spin" → An unnecessary and misleading story. The tidal acceleration alone gives both bulges; it would exist even if Earth fell straight at the Moon with no orbit.
- "Stronger pull means bigger tide" → No; the Sun pulls 179× harder but raises a tide 0.46× the Moon's. The tidal acceleration matters, not the pull.
- "High tides come every 12 h" → Every 12 h 25 min, because the Moon moves on in its orbit.

## Scope

- **Out of scope:** Why real tides are often metres high, lag the Moon, or happen once a day at some places (for example the Gulf of Mexico) — the ocean basins respond as resonating bodies; continents block the bulges; the Moon's tilt makes the two bulges unequal at a given latitude. Look up "dynamic theory of tides" and "amphidromic points".
- **Out of scope:** How high the bulges are — in an ideal ocean, about 0.36 m above the mean at the peak (an estimate); real coasts amplify this. Look up "equilibrium tide".
- **Out of scope:** Spring and neap tides — the Sun's bulges add to or partly cancel the Moon's.
- **Out of scope:** The solid Earth also stretches, by a few tens of centimetres; the ocean tide is measured relative to the land. Look up "Earth tide".

## Representation decision

- **Stage:** 1 (prose)
- **Reason:** The argument is a short chain: three numbers, one subtraction, one rotation. A table of the three points carries the comparison; a small text figure carries the geometry. Nothing needs exploration with a parameter.
- **Levels:** L1 the answer / L2 the subtraction at three points / L3 why subtract (free fall; Sun case) / L4 not needed.
