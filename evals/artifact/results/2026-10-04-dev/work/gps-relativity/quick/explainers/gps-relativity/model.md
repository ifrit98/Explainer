# Semantic model: GPS positioning and relativity

> Source of truth. Every rendering derives from this file.

## Central question

How does a GPS receiver find its position from satellite signals, and why must the system correct for relativity?

## Audience and prior knowledge

A technical reader: school mathematics and science (speed = distance / time, Pythagoras, simultaneous equations, gravity), basic programming. New to GPS and to relativity. Does not know: pseudorange, receiver clock bias, why four satellites, that clocks tick at different rates with speed and gravity.

## Entities

| Entity | Definition (one sentence) | Status |
|---|---|---|
| Satellite | One of about 30 GPS satellites at 20,200 km altitude, each with an atomic clock. | fact |
| Signal | A radio message that carries the satellite's send time and its position. | fact |
| Receiver | The device on the ground (phone) with a cheap quartz clock. | fact |
| Travel time | Receive time minus send time; about 67 ms for a satellite overhead. | fact |
| Pseudorange | Travel time × c; a distance that still contains the receiver clock error. | definition |
| Receiver clock bias | The unknown offset of the receiver's clock from GPS time. | definition |
| Clock rate shift | The change in how fast a satellite clock ticks compared with a ground clock. | fact (relativity) |

## Relationships

| From | Relationship | To |
|---|---|---|
| Satellite clock | stamps | Signal (send time) |
| Travel time × c | gives | Pseudorange |
| 4 pseudoranges | solve for | x, y, z, receiver clock bias |
| Orbit speed | slows | Satellite clock (special relativity) |
| Weaker gravity at altitude | speeds up | Satellite clock (general relativity) |
| Clock rate shift | becomes | Range error (× c) |

## Causal chain

```text
time stamp → travel time → × c → pseudorange → 4 equations → position + clock bias
satellite speed (−7 µs/day) + weaker gravity (+45 µs/day) → net +38 µs/day → ×c → ≈11 km/day range drift → so: tune satellite clocks slow before launch
```

## Quantities

- c = 299,792,458 m/s; light travels about 30 cm per ns, 300 m per µs.
- Altitude 20,200 km; orbit radius 26,560 km; Earth radius 6,371 km; orbit speed 3.87 km/s.
- Travel time overhead ≈ 20,200 km / c ≈ 67 ms.
- Special relativity: fractional rate ≈ −v²/(2c²) = −8.3 × 10⁻¹¹ → × 86,400 s ≈ −7 µs/day.
- General relativity: fractional rate ≈ (GM/c²)(1/R_E − 1/r) = +5.3 × 10⁻¹⁰ → ≈ +45 µs/day.
- Net ≈ +38 µs/day → 38 µs × 300 m/µs ≈ 11 km of light travel per day.
- Fix: nominal 10.23 MHz clock set to 10.22999999543 MHz before launch.
- Receiver clock 1 ms wrong → 300 km range error.

## Alternative states

| Scenario | What changes | Why |
|---|---|---|
| No relativity correction | Satellite clocks gain 38 µs/day on ground clocks | ranges drift by about 11 km per day |
| Only 3 satellites | cannot solve for clock bias | 4 unknowns, 3 equations |
| Perfect receiver clock | 3 satellites would suffice | bias is no longer unknown |

## Why this form

| Operation | Simplest alternative | What the alternative breaks |
|---|---|---|
| Use 4 satellites | 3 spheres meet at a point; use 3 | receiver quartz clock may be 1 ms off → every range wrong by 300 km |
| Measure time, then multiply by c | measure distance directly | no way to measure 20,200 km directly; time stamps are what a radio can carry |
| Correct the satellite clock rate | ignore relativity; effects are tiny (5 parts in 10¹⁰) | ×c turns 38 µs/day into ≈11 km/day |

## Concrete cases

| Claim | Holds | Breaks |
|---|---|---|
| Position from 4 pseudoranges | all clocks agree with GPS time to ns → metres | satellite clocks drift 38 µs/day → ≈11 km/day |

## Terms

- travel time, pseudorange, receiver clock bias, clock rate shift. "GPS time" = the common time the satellite clocks are kept to.

## Epistemic status

- **Established:** both rate shifts are measured on GPS clocks and match relativity.
- **Estimate:** "11 km per day" is the light-travel equivalent of 38 µs. Real position error would grow in a more complex way, because the receiver's bias term absorbs part of a shift common to all satellites. The drift would still break the system.

## Confusion points

- "Relativity makes satellite clocks slow" → speed slows them (7 µs/day), but gravity speeds them up more (45 µs/day). Net: fast.
- "GPS measures distance" → it measures time; distance is time × c.
- "Third satellite is enough in 3D" → only if the receiver clock is perfect.

## Scope

- **Out of scope:** Sagnac effect from Earth's rotation; orbit eccentricity correction (tens of ns, computed by the receiver); ionosphere delay; least-squares with more than 4 satellites.

## Representation decision

- **Stage:** 1
- **Reason:** a sequential argument with worked numbers; no state change or parameter space a reader must explore.
- **Levels:** L1 answer / L2 time → distance → 4 equations / L3 two clock effects with numbers / L4 the factory frequency offset.
