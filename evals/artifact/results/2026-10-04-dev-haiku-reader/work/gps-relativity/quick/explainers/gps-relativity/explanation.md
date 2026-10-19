# How does GPS find your position, and why does it need relativity?

<!-- Stage 1, rendered from model.md in STE-80. -->

**GPS finds your position by timing radio signals. Each satellite sends the time it transmitted. Your receiver measures how long each signal took to arrive, and multiplies by the speed of light to get a distance. Four distances fix your position. Relativity matters because the satellite clocks tick faster than ground clocks by 38 microseconds per day. At the speed of light, that error is about 11 km of distance per day.**

## Step 1: time becomes distance

About 30 GPS satellites orbit at 20,200 km altitude. Each satellite carries an atomic clock. Each satellite continuously broadcasts a **signal**: a radio message that says "I sent this at time t, and I was at position (x, y, z)".

Your receiver notes when the signal arrives. The **travel time** is receive time minus send time. For a satellite straight overhead, the travel time is about 67 ms (20,200 km ÷ 299,792,458 m/s).

Distance = travel time × c. Light travels about 30 cm per nanosecond, so the clocks must agree to within a few nanoseconds for metre-level accuracy. <!-- claim: time-to-distance -->

## Step 2: why four satellites, not three

One distance puts you somewhere on a sphere around one satellite. Three spheres meet at a point. So three satellites should be enough.

But your phone has a cheap quartz clock, not an atomic clock. Suppose the phone clock is 1 ms wrong. Then every distance is wrong by 1 ms × c = 300 km. The three spheres no longer meet at your true position. <!-- claim: why-four -->

GPS solves this by treating the clock error as a fourth unknown. The **receiver clock bias** b is the offset of your clock from GPS time. Each measured distance is a **pseudorange** ρ: the true distance plus the same error c·b. For satellite i at (xᵢ, yᵢ, zᵢ):

```text
ρᵢ = √((x − xᵢ)² + (y − yᵢ)² + (z − zᵢ)²) + c·b
```

There are four unknowns (x, y, z, b), so the receiver needs four equations: four satellites. It solves them by iteration: guess a position, compute the predicted pseudoranges, and correct the guess until the predicted values match the measured ones. A side effect: your phone gets the time accurate to nanoseconds.

This method works only if the satellite clocks all keep GPS time. Relativity says that they do not, if nobody corrects them.

## Step 3: two effects change the satellite clock rate

**Predict first:** a satellite moves fast and sits high above Earth. Does its clock run fast or slow compared with a clock on the ground?

Two effects pull in opposite directions. <!-- claim: two-effects -->

1. **Speed slows the clock (special relativity).** A moving clock ticks slower by a fraction of about v²/(2c²). The orbit speed is 3.87 km/s, which gives 8.3 × 10⁻¹¹. Over one day (86,400 s), the satellite clock loses about 7 µs.
2. **Weaker gravity speeds the clock up (general relativity).** A clock deeper in a gravity well ticks slower. A ground clock sits at 6,371 km from Earth's center. A satellite sits at 26,560 km, where gravity is weaker. The fraction is about (GM/c²)(1/R_Earth − 1/r) = 5.3 × 10⁻¹⁰. Over one day, the satellite clock gains about 45 µs.

The gravity effect wins. Net: the satellite clock gains about 38 µs per day.

## Step 4: why 38 µs matters

38 µs looks small. Multiply by c: 38 µs × 300 m per µs ≈ 11 km. <!-- claim: drift-size --> The system needs agreement to a few nanoseconds. The drift is 0.44 ns per second, so after one minute it is 26 ns, or 8 m. After one day, the satellite time stamps would be off by the light-travel time of 11 km.

The fix is simple. Engineers set each satellite clock to tick slow before launch. The nominal frequency is 10.23 MHz; the clock is set to 10.22999999543 MHz. In orbit, relativity speeds the clock up to exactly 10.23 MHz as seen from the ground. <!-- claim: the-fix -->

## Limits

- **Estimate:** "11 km per day" is the light-travel distance of 38 µs. The actual position error would grow in a more complex way, because the bias b absorbs part of an error that all satellites share. The drift would still break the system within hours.
- **Out of scope:** Earth's rotation during signal travel (the Sagnac effect), a small extra correction for slightly elliptical orbits (tens of ns, computed by the receiver), and signal delay in the ionosphere.
