# Semantic model: GPS positioning and relativity

> Source of truth. Every rendering derives from this file.

## Central question

How does a GPS receiver find its position from satellite signals, and why must the system correct for relativity?

## Audience and prior knowledge

A technical reader: school mathematics and science (speed = distance / time, the speed of light, gravity, solving simultaneous equations), basic programming. New to GPS and to relativity. Knows that light speed is about 300,000 km/s. Does not know what a pseudorange is, why four satellites are needed, or what time dilation is in numbers.

## Entities

| Entity | Definition (one sentence) | Status |
|---|---|---|
| Satellite | One of about 30 GPS satellites, orbiting at about 20,200 km altitude, each carrying atomic clocks. | fact |
| Satellite clock | An atomic clock on a satellite; it stamps each signal with its send time. | fact |
| Signal | A radio message from a satellite that says "I am satellite k, at position P, and I sent this at time t". | fact (simplified) |
| Receiver | The GPS chip in a phone or car; it only listens, it never transmits. | fact |
| Receiver clock | A cheap quartz clock in the receiver; its error is not known in advance. | fact |
| Range | The true distance from a satellite to the receiver. | definition |
| Pseudorange | Light speed × (receive time on the receiver clock − send time on the satellite clock): a range plus an unknown error from the receiver clock. | definition |
| Clock bias | b: how far the receiver clock is ahead of GPS time, times light speed (in metres). | definition |
| GPS time | The reference time kept by atomic clocks at ground stations; satellite clocks are steered to it. | definition |
| Time dilation | Clocks in different motion or at different heights in gravity tick at different rates. A moving clock ticks slower than a clock at rest, by a fraction ≈ v²/2c². A clock higher above Earth ticks faster than one on the ground. | established fact (measured: Pound–Rebka 1959, Hafele–Keating 1971, GPS clocks) |
| Rate offset | The built-in setting that makes each satellite clock tick slow before launch: 10.23 MHz → 10.22999999543 MHz. 10.23 MHz is the nominal tick frequency of the satellite clock; the signal is derived from it. | fact |

## Relationships

| From | Relationship | To | Notes |
|---|---|---|---|
| Signal travel time | times light speed gives | range | 1 µs ↔ 300 m |
| Receiver clock bias | adds the same error b to | every pseudorange | same instant, same clock |
| Four pseudoranges | determine | x, y, z, b | four equations, four unknowns |
| Orbit speed | slows | satellite clock | special relativity, −7 µs/day |
| Weaker gravity at altitude | speeds up | satellite clock | general relativity, +45 µs/day |
| Satellite clock rate error | grows into | range error | 38 µs/day ↔ 11 km/day |

## Dependencies (learning order)

1. Time of flight gives distance (range).
2. Several ranges fix a point (intersection of spheres).
3. The receiver clock is wrong, so each range is a pseudorange; add b as a fourth unknown, use four satellites.
4. The method needs satellite clocks that agree with ground time to nanoseconds.
5. Relativity makes satellite clocks run 38 µs/day fast; the system corrects it.

## Causal chain

```text
satellite sends time stamp → receiver measures travel time → × c → pseudorange
4 pseudoranges → solve x, y, z, b → position (and exact time)
satellite clock error of 1 ns → range error of 0.3 m
orbit: speed (−7 µs/day) + weaker gravity (+45 µs/day) → +38 µs/day → 11 km/day of range error if not corrected
→ rate offset: clocks set to tick slow before launch (10.23 MHz → 10.22999999543 MHz)
```

Why the drift would not cancel: b absorbs only an error that is the same in every pseudorange. All satellite clocks drift at the same rate, but each one was last set to GPS time on a different day. Satellite A set on day 0 and satellite B set on day 3: on day 5, A is 190 µs (57 km) off and B is 76 µs (22.8 km) off. The 34 km difference cannot go into one b. If all clocks were off by exactly the same 38 µs, b would absorb it: the position would be right and only the reported time would be wrong.

## Temporal sequence

1. Before launch: engineers set each satellite clock slightly slow.
2. In orbit: each satellite broadcasts its position and send time continuously.
3. The receiver records the receive time of signals from 4+ satellites.
4. The receiver computes pseudoranges and solves for x, y, z, b.

## Quantities

- Light speed c = 299,792,458 m/s ≈ 0.3 m per nanosecond ≈ 300 m per microsecond.
- Orbit radius ≈ 26,560 km (altitude ≈ 20,200 km); orbit speed ≈ 3.9 km/s.
- Accuracy target: a position error of about 5 m needs satellite clocks within about 17 ns of GPS time (5 m / 0.3 m per ns). 1 µs gives 300 m.
- Signal travel time ≈ 67 ms from directly overhead.
- Special relativity (speed): satellite clock loses ≈ 7 µs/day (v²/2c² ≈ 8.3 × 10⁻¹¹).
- General relativity (gravity): satellite clock gains ≈ 45 µs/day (GM(1/R_earth − 1/r)/c² ≈ 5.3 × 10⁻¹⁰).
- Net: gains ≈ 38 µs/day (fractional rate ≈ 4.465 × 10⁻¹⁰). 38 µs × c ≈ 11.4 km.
- Factory offset: 10.23 MHz × (1 − 4.465 × 10⁻¹⁰) = 10.22999999543 MHz.
- Receiver quartz clock: easily off by 1 ms → 300 km.

## Alternative states

| State | What changes | Why |
|---|---|---|
| Receiver clock perfect | 3 satellites suffice | no b to solve |
| Receiver clock off by 5 µs, 3D, only 3 satellites | position wrong by km, no way to detect | 4 unknowns, 3 equations |
| No relativity correction | ranges drift ≈ 11 km per day | clocks gain 38 µs/day |
| Only the speed effect corrected | clocks gain 45 µs/day → 13.5 km/day | the speed correction cancels −7 µs/day; the +45 µs/day gravity gain remains |

## Why this form

| Operation | Simplest alternative | What the alternative breaks (with numbers) |
|---|---|---|
| Solve for receiver clock bias b as a fourth unknown | Trust the receiver clock | Quartz clock off by 1 ms → every range off by 300 km. Even 1 µs → 300 m. |
| Use 4 satellites | Use 3 (three spheres meet at two points; the one far from Earth is rejected) | With b unknown, 3 equations, 4 unknowns: any b gives a different point. |
| Pre-set satellite clocks slow | Let them run at the nominal 10.23 MHz | They gain 38 µs/day; ranges drift 11.4 km per day. |

## Concrete cases

| Claim | Holds here (numbers) | Breaks here (numbers) |
|---|---|---|
| Inconsistent pseudoranges reveal the clock bias (1D worked example) | Beacons at 0 and 30 km, receiver at 12 km. True travel times 40 µs and 60 µs. Receiver clock 5 µs fast: measured 45 and 65 µs → pseudoranges 13.5 and 19.5 km. Sum 33 km ≠ 30 km → excess 3 km = 2b → b = 1.5 km = 5 µs. Subtract: 12 and 18 km → x = 12 km. (Assumes the receiver lies between the beacons, as satellites surround a receiver.) | With one beacon only: 13.5 km, no check → position off by 1.5 km, undetected. |
| Satellite clock error becomes range error | 1 ns → 0.3 m | 38 µs → 11.4 km |
| b absorbs a shared error only | all clocks 38 µs off → b absorbs 11.4 km, position right | clocks set on day 0 and day 3, read on day 5: 57 km vs 22.8 km, 34 km difference survives |
| The two relativity effects oppose | at GPS altitude: −7 + 45 = +38 µs/day | — |

## Terms

- **Range:** true distance satellite–receiver.
- **Pseudorange:** measured travel time × c, using the receiver clock; equals range + b. Never call it "distance".
- **Clock bias (b):** receiver clock error expressed in metres (error in seconds × c). 5 µs ↔ 1.5 km. Low b (1 ns) → 0.3 m; high (1 ms) → 300 km.
- **GPS time:** the reference time kept by ground stations; satellite clocks are steered to it.
- **Time dilation:** the rate difference between clocks. 38 µs/day is a fraction 4.5 × 10⁻¹⁰: tiny as a fraction, large as distance.

## Epistemic status

- **Established:** both relativistic effects are measured on GPS clocks and match theory; the clock offset has been built in since the first satellites.
- **Mathematical consequence:** 11.4 km/day = 38 µs/day × c.
- **Simplification:** the "11 km/day position error" is the growth of the range error if satellite clocks were left uncorrected against GPS time. b absorbs the part shared equally by all satellites, so the position error comes from how the clock errors differ between satellites; that difference grows by tens of km within days. The ground stations also upload small clock corrections.

## Confusion points

- "Relativity is about the satellite's speed, so the clock runs slow" → gravity effect is larger and opposite; net is fast.
- "GPS needs 3 satellites" → 3 is enough only with a perfect receiver clock; real receivers need 4.
- "The phone sends a signal to the satellite" → receiver only listens.
- "The receiver clock bias would absorb the relativity drift" → only the part shared equally by all satellites; clocks set on different days carry different errors.
- "38 µs is negligible" → light goes 11.4 km in 38 µs.

## Scope

- **Out of scope:** atmospheric delays (ionosphere, troposphere) — the largest remaining error sources; dual-frequency receivers remove most of the ionospheric part.
- **Out of scope:** Sagnac effect (Earth rotates during the 67 ms flight) — receivers correct it; see Ashby, "Relativity in the Global Positioning System", Living Reviews in Relativity (2003).
- **Out of scope:** the eccentricity correction (the receiver removes a periodic clock error up to about 23 ns, 7 m, from slightly elliptical orbits) and the forms of the time-dilation formulas — Ashby (2003).
- **Out of scope:** more than four satellites (a least-squares fit) and satellite geometry (bunched satellites amplify errors).
- **Out of scope:** why one-way ranging (unlimited users, receivers never transmit) and why atomic clocks on satellites.
- **Out of scope:** how the receiver solves the nonlinear equations (iterative least squares from a guess).
- **Out of scope:** satellite orbit data (ephemeris) and how the ground segment computes it.

## Representation decision

- **Stage:** 1
- **Reason:** the subject is one sequential causal argument with worked numbers; there is no parameter space a reader must explore, and the 1D worked example fits in text.
- **Levels:** L1 answer / L2 positioning with pseudoranges / L3 why clocks must agree / L4 relativity numbers and the fix.
