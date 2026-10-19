# Model: GPS and relativity

**Central question.** How does a receiver find its position from satellite signals, and why must relativity be included?

**Reader.** Technical, school physics and maths, basic programming. New to GPS and to relativity.

**Entities.** Satellite (atomic clock, known position), signal (carries send time and orbit data), receiver (cheap quartz clock), GPS time (the shared time scale).

**Causal chain.**
1. Distance = c × travel time. 1 ns of timing error = 30 cm of distance error.
2. One distance → sphere. Three spheres → a point (plus one point far in space).
3. Receiver clock is unknown → add unknown b → need four satellites.
4. Step 3 removes only an error common to all signals. Each satellite clock must agree with GPS time to ~ns.
5. Satellite clocks run at a different rate from ground clocks: −7.2 µs/day (speed, special relativity) + 45.7 µs/day (weaker gravity, general relativity) = +38.5 µs/day.
6. Fix: set the clock to 10.22999999543 MHz before launch; receiver adds a per-satellite eccentricity term (up to ~46 ns ≈ 14 m for e = 0.02).

**Epistemic notes.** Both effects are established and measured. The popular "10 km/day of position error" assumes the receiver trusts the satellite clocks; a drift common to all satellites partly cancels in the four-unknown solve. Per-satellite differences and the time output do not cancel.

**Confusion points.** "Doesn't the 4th satellite fix all clock errors?" — only the shared one. "Fast or slow?" — two effects with opposite sign; gravity wins.

**Scope (out).** Atmospheric delay, Sagnac effect, ephemeris fitting, carrier-phase / RTK, other GNSS.
