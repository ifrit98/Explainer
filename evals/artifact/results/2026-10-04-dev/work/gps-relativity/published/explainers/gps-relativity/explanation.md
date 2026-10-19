# How does GPS find your position, and why does it need relativity?

**A GPS receiver times radio signals from four satellites and solves for its position and its own clock error. This works only if the satellite clocks agree to a few billionths of a second. Relativity makes those clocks gain 38 µs a day on ground clocks. Light covers 11.4 km in 38 µs, so engineers build the clocks to tick slow.**

## 1. Time gives distance

About 30 GPS satellites orbit 20,200 km above Earth. Each one carries atomic clocks and broadcasts a signal that says: "I am satellite k, I am at position P, and I sent this at time t." Your receiver (the GPS chip in a phone) only listens.

The receiver notes when each signal arrives. Then:

- travel time = receive time − send time
- range = travel time × c, where c is light speed and the range is the true distance to the satellite.

From a satellite directly overhead, the travel time is about 67 ms. Light covers 300 m in one microsecond (1 µs = 10⁻⁶ s) and 0.3 m in one nanosecond (1 ns = 10⁻⁹ s). So every timing error becomes a range error at that rate.

One range puts you somewhere on a sphere around the satellite: every point at that distance. Three spheres meet in two points. The receiver rejects the one far out in space. Three satellites would be enough, if every clock were perfect.

## 2. The receiver's clock is wrong, so it uses a fourth satellite

<!-- claim: why-fourth-unknown -->
Your phone's clock is quartz, not atomic. It can easily be off by 1 ms, and 1 ms × c = 300 km.

<!-- claim: def-pseudorange -->
So the receiver does not compute a range. It computes a **pseudorange**: light speed × (receive time on the receiver clock − send time on the satellite clock). A pseudorange equals the range plus **b**, the receiver clock error expressed in metres. One clock makes every measurement, so b is the same in every pseudorange. That makes b one more unknown to solve for, next to the position.

<!-- claim: mech-bias-1d -->
**Worked example, on a line.** Put beacon A at 0 km and beacon B at 30 km. The receiver is at 12 km, so the true travel times are 40 µs and 60 µs. The receiver clock is 5 µs fast, so it measures 45 µs and 65 µs. Those give pseudoranges of 13.5 km and 19.5 km.

The receiver lies between the beacons, so the two ranges must add up to 30 km. The pseudoranges add up to 33 km. The excess, 3 km, is b counted twice, so b = 1.5 km (5 µs × c). Subtract b from each: 12 km and 18 km. The receiver is at 12 km. With only beacon A, the receiver could not detect the 1.5 km error.

In three dimensions the unknowns are x, y, z, and b. Four unknowns need four equations, so the receiver needs four satellites.
## 3. The satellite clocks must be almost perfect

<!-- claim: mech-clock-to-range -->
The receiver can solve for its own clock error because every pseudorange shares it. A satellite clock error sits in only one pseudorange, so no unknown absorbs it. Each satellite clock must therefore match **GPS time**, the time kept by atomic clocks at ground stations.

How close? Each nanosecond of satellite clock error is 0.3 m of range error. For a fix within about 5 m, the satellite clocks must agree with GPS time to about 17 ns.

## 4. Relativity moves the satellite clocks by microseconds a day

<!-- claim: mech-two-effects -->
**Time dilation** means that clocks in different motion, or at different heights in gravity, tick at different rates. It is measured, not only predicted. Two effects act on a satellite clock, compared with a clock on the ground:

| Cause | Theory | Effect on the satellite clock |
|---|---|---|
| Speed: 3.9 km/s in orbit | special relativity: a moving clock ticks slower | loses 7 µs per day |
| Height: gravity is weaker 20,200 km up | general relativity: a clock higher above Earth ticks faster | gains 45 µs per day |
| **Net** | | **gains 38 µs per day** |

The gravity effect is larger, so the clock runs fast. 38 µs is only 4.5 × 10⁻¹⁰ of a day, but light covers 11.4 km in 38 µs. Each uncorrected satellite clock would move 11.4 km of range further from GPS time every day.

## 5. Why the receiver's b does not cancel the drift

<!-- claim: guar-bias-absorbs-shared -->
Every satellite clock drifts at the same rate. Why does b not absorb the drift?

Only if every clock had the same error at the same moment. If every satellite clock were exactly 38 µs fast, b would absorb 11.4 km, and the position would come out right.

But each satellite clock is set to GPS time at a different moment. Suppose satellite A is set on day 0 and satellite B on day 3. On day 5, A is 190 µs fast (57 km) and B is 76 µs fast (22.8 km). The 34 km difference is not shared, so no single b can absorb it, and the position fix fails. Every clock set on a different day carries a different error.

## 6. The remedy: make the clocks tick slow before launch

<!-- claim: fix-rate-offset -->
Each satellite clock counts the ticks of a 10.23 MHz signal. Before launch, engineers set it to 10.22999999543 MHz: slower by 4.5 × 10⁻¹⁰, the fraction the clock gains in orbit. On the ground the clock runs slow. In orbit, relativity speeds it up to the rate of GPS time. Ground stations upload small corrections for what remains; the built-in offset keeps those corrections small instead of growing by 38 µs a day.

## Summary

Four pseudoranges give x, y, z, and the receiver's clock error, but only if satellite clocks stay within about 17 ns of GPS time. Relativity makes them gain 38 µs a day, so each clock is built to tick slow.

## Not covered here

- **Atmosphere:** charged and humid layers of the atmosphere slow the signal. These delays are the largest remaining errors.
- **Earth's rotation during the 67 ms flight (Sagnac effect)** and the **orbit-shape correction** (orbits are slightly elliptical, so each satellite clock error swings by up to about 23 ns): receivers correct both. See N. Ashby, "Relativity in the Global Positioning System", *Living Reviews in Relativity* (2003).
- **Why a moving clock ticks slow:** see the "light clock" argument in special relativity.
- **How the receiver solves the equations:** iteration from a guess, with a best fit when it hears more than four satellites.
