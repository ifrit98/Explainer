# How GPS finds your position, and why it needs relativity

**The short answer.** A GPS receiver does not send anything. It only listens. Each satellite broadcasts its position and the exact time it sent its signal. The receiver measures how long each signal took to arrive. Then it multiplies that time by the speed of light to get a distance. With distances to four satellites, it can solve for where it is.

This works only if the satellite clocks are correct to a few billionths of a second (nanoseconds). Relativity says a clock in orbit ticks at a different rate from a clock on the ground: about 38 microseconds per day faster. GPS builds that correction into every satellite and every receiver.

Below, each step follows from the one before it.

---

## 1. Time becomes distance

Radio signals travel at the speed of light, *c* ≈ 300,000 km/s. The distance to a satellite is:

```
distance = c × (time received − time sent)
```

**Example.** GPS satellites orbit about 20,200 km above the ground. A signal from a satellite directly overhead takes about 0.067 s (67 ms) to arrive. A satellite near the horizon is farther away, so its signal takes up to about 86 ms.

This conversion is unforgiving. Light travels **30 cm in one nanosecond**. A timing error of 10 ns gives a distance error of 3 m. A timing error of 1 microsecond (1,000 ns) gives 300 m. So GPS is really a system for distributing very precise time.

## 2. Distances become a position

One distance tells you that you are somewhere on a sphere around that satellite.

- Two spheres intersect in a circle.
- A third sphere cuts that circle at two points. One point is near the Earth. The other is far out in space, so the receiver discards it.

So three exact distances give a position. A flat version of the same idea: if you are 3 km from tower A, 4 km from tower B, and 5 km from tower C, only one spot on the map fits all three.

## 3. The receiver's clock is the weak link, so use a fourth satellite

Each satellite carries atomic clocks. Your phone has a cheap quartz clock. Suppose the quartz clock is wrong by 1 millisecond. Then every distance is wrong by 300 km, and the three spheres do not meet at a sensible point.

The simplest fix is an atomic clock in every receiver. That fails on cost, size, and power. GPS uses a better trick: treat the receiver clock error *b* as a fourth unknown. The receiver's error adds the same amount, *c·b*, to every measured distance. For each satellite *i* at known position (*xᵢ, yᵢ, zᵢ*):

```
measured_distanceᵢ = √((x − xᵢ)² + (y − yᵢ)² + (z − zᵢ)²) + c·b
```

There are four unknowns (*x, y, z, b*), so the receiver needs four satellites. It solves the equations numerically, usually with more than four satellites to average out noise. A bonus: once it knows *b*, the receiver knows the true time to within tens of nanoseconds.

**What this trick cannot fix.** The term *c·b* removes only an error that is **the same for every signal**. If one satellite's clock is off by 30 ns and the others are not, that satellite's distance is off by 9 m, and the solve cannot detect it. So every satellite clock must agree with one shared time scale, called **GPS time**, to within a few nanoseconds. Relativity enters here.

## 4. Clocks in orbit do not tick at ground rate

*Before you read on, predict: does a satellite clock run fast or slow compared with a clock on the ground?*

Two established effects act on the satellite clock. Both are measured in experiments, not only predicted. They act in opposite directions.

**Effect 1: speed (special relativity).** A moving clock ticks slower than a clock at rest, as seen by the clock at rest. For speeds much less than *c*, the clock loses a fraction *v²/2c²* of its time. A GPS satellite moves at about 3.87 km/s:

```
v² / 2c² = (3,870 m/s)² / (2 × (3.0×10⁸ m/s)²) ≈ 8.3 × 10⁻¹¹
× 86,400 s per day ≈ 7.2 µs per day slower
```

**Effect 2: gravity (general relativity).** A clock deeper in a gravitational field ticks slower. The ground clock sits closer to the Earth's centre (6,371 km) than the satellite (26,560 km). So the satellite clock ticks *faster*. The fraction is the difference in gravitational potential divided by *c²*:

```
(GM/c²) × (1/R_earth − 1/r_orbit)
= 4.43 mm × (1/6,371 km − 1/26,560 km) ≈ 5.29 × 10⁻¹⁰
× 86,400 s per day ≈ 45.7 µs per day faster
```

(*GM/c²* for the Earth is a length, about 4.43 mm. It sets how strong the effect is.)

**Net result.** Gravity wins:

```
+45.7 µs/day − 7.2 µs/day ≈ +38.5 µs/day
```

**What that number means.** 38.5 µs × 30 cm/ns ≈ **11.5 km**. That is the distance error that one day of uncorrected drift represents. Compare it with the few-nanosecond budget from section 3. The drift is about 0.45 ns per second, so it uses up that budget in about 10 seconds.

## 5. How GPS corrects it

**Before launch.** Engineers set each satellite clock slightly slow on the ground. The nominal clock frequency is 10.23 MHz. The factory setting is **10.22999999543 MHz**, which is lower by the net fraction 4.46 × 10⁻¹⁰. In orbit, the two relativistic effects speed the clock up by exactly that fraction. Seen from the ground, it then ticks at 10.23 MHz.

**In the receiver.** The fixed offset assumes a perfectly circular orbit. Real orbits are slightly elliptical. As a satellite moves closer to the Earth and then farther away, its speed and gravity change, so its clock rate changes too. For an orbit with eccentricity 0.02, this swings the clock by up to about ±46 ns (±14 m). The amount differs for each satellite, so the fourth-satellite trick cannot absorb it. The receiver calculates this term from the broadcast orbit data and subtracts it.

**From the ground.** Control stations track every satellite clock and upload small corrections for the remaining drift. Relativity is built into the model that these corrections assume.

## 6. What if relativity were ignored?

You often read that GPS would "drift 10 km per day" without relativity. That figure assumes the receiver trusts the satellite clocks. It is a fair measure of the size of the effect. It is not an exact forecast:

- **The part common to all satellites** would partly cancel. It shifts every distance equally, so the receiver would absorb it into *b*, like its own clock error. The *time* the receiver reports would still drift by 38.5 µs per day. Power grids, phone networks, and financial exchanges use GPS time and would fail.
- **The parts that differ between satellites** would not cancel. Each satellite's eccentricity term alone produces errors of up to about 14 m. Satellite clocks would also drift away from GPS time, and from the ground stations that track them.

Either way, GPS cannot meet its metre-level accuracy without relativity.

---

## Summary

1. The receiver measures signal travel time; time × *c* = distance. 1 ns = 30 cm.
2. Three distances fix a point. A fourth satellite removes the receiver's own clock error.
3. That trick removes only a shared error, so satellite clocks must agree to nanoseconds.
4. In orbit, speed slows the clock by 7.2 µs/day and weaker gravity speeds it up by 45.7 µs/day: net +38.5 µs/day, or 11.5 km of light travel.
5. GPS sets the clocks slow before launch and corrects the per-satellite orbit effect in the receiver.

**Not covered here:** signal delays in the atmosphere, the Sagnac effect (the Earth rotates while the signal travels), how orbits are predicted, and centimetre-level methods such as RTK.
