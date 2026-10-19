# How GPS finds your position, and why it needs relativity

The short version: GPS is a clock system. Each satellite says what time it is. Your receiver works out how long each message took to arrive, and those delays tell it where it is. Light covers about 30 cm in a nanosecond, so the clocks have to agree to within a few billionths of a second. At that level of precision, Einstein's two theories of relativity both change how fast the satellite clocks tick, and the change is large enough that it has to be designed out.

The rest of this file explains that in four steps:

1. Distance from time
2. Why you need four satellites, not three
3. How the receiver actually solves for position (with code)
4. Relativity: what changes the satellite clocks' rate, by how much, and what the system does about it

---

## 1. Distance from time

About 30 GPS satellites orbit roughly 20,200 km above the ground, and each goes round about twice a day. Each one carries atomic clocks and constantly broadcasts a radio signal containing, in effect:

> "I am satellite #12. This part of the signal left me at exactly time *t*ₛ. At that moment I was at position (*x*, *y*, *z*)."

The satellite knows its own position because ground stations track every satellite and regularly upload a precise description of its orbit, called the *ephemeris*.

Your receiver notes the time *t*ᵣ when that part of the signal arrives. Radio waves travel at the speed of light, *c* ≈ 299,792,458 m/s, so

```
distance to satellite = c × (t_r − t_s)
```

The signal takes about 67–86 milliseconds to arrive. Getting a distance accurate to a metre means measuring that delay to about 3 nanoseconds. **Every nanosecond of timing error is about 30 cm of position error.** Keep that conversion in mind, because the rest of the story depends on it.

One distance puts you somewhere on a sphere centred on that satellite. With a second satellite you are on the circle where two spheres meet. A third sphere cuts that circle at two points. One of those points is usually far out in space or deep underground, so in principle three satellites give you a position.

In practice, three is not enough.

## 2. Why four satellites: your receiver's clock is bad

The satellites have atomic clocks that cost a lot and are steered against a master time scale on the ground. Your phone has a cheap quartz oscillator. It may easily be off by a millisecond, and a millisecond is 300 km.

So *t*ᵣ in the formula above isn't the true arrival time. It is the true arrival time plus an unknown receiver clock error δ*t*. That error is the **same for every satellite**, because all the measurements are made with the same clock. Each measured distance is therefore wrong by the same amount, *b* = *c*·δ*t*. These measured distances are called **pseudoranges**:

```
ρᵢ = |sᵢ − p| + b
```

Here `sᵢ` is satellite *i*'s known position, `p` = (*x*, *y*, *z*) is your unknown position, and `b` is your unknown clock error expressed in metres.

That makes **four unknowns**: *x*, *y*, *z* and *b*. Four unknowns need four equations, so you need four satellites. A useful side effect is that once the receiver has solved for *b*, it knows the time to within tens of nanoseconds. That is why GPS is also one of the world's main sources of precise time, used by phone networks, power grids and financial systems.

Usually 8–12 satellites are visible. With more than four, the receiver does a least-squares fit, which averages out noise.

## 3. Solving the equations

The equations are non-linear because of the square root inside |sᵢ − p|. The standard method is to guess, linearise and repeat:

1. Start with a rough guess, such as the centre of the Earth with *b* = 0.
2. For each satellite, predict the pseudorange from the current guess and compare it with the measured one.
3. Work out how much each prediction would change if you nudged *x*, *y*, *z* or *b*. For the position this is the unit vector pointing from the satellite to you. For *b* it is simply 1.
4. Solve the resulting *linear* least-squares problem for the correction, apply it, and go back to step 2.

This usually converges in 4–6 iterations, even from the centre of the Earth.

```python
import numpy as np

def solve_position(sat_pos, pseudoranges, iters=10):
    """sat_pos: (N,3) array of satellite positions in metres (N >= 4).
    pseudoranges: (N,) measured pseudoranges in metres.
    Returns (receiver position, receiver clock bias in metres)."""
    x = np.zeros(4)                      # [x, y, z, b], starting at Earth's centre
    for _ in range(iters):
        diff = sat_pos - x[:3]
        ranges = np.linalg.norm(diff, axis=1)
        predicted = ranges + x[3]
        residual = pseudoranges - predicted
        # Jacobian: d(predicted)/d(x,y,z) = -unit vector to satellite; d/db = 1
        J = np.hstack([-diff / ranges[:, None], np.ones((len(ranges), 1))])
        dx, *_ = np.linalg.lstsq(J, residual, rcond=None)
        x += dx
        if np.linalg.norm(dx) < 1e-4:
            break
    return x[:3], x[3]
```

Real receivers also correct for several known sources of error: the signal slowing down in the ionosphere and the troposphere, reflections off buildings, small errors in the broadcast orbits, and the effects described below. All of this together gives a typical phone accuracy of a few metres.

Note what the whole method assumes: **the satellites' clocks agree with each other and with GPS system time.** The receiver can absorb an error in its own clock, because that error is the same for every satellite. It cannot absorb errors that differ from satellite to satellite. The receiver has no way to tell one satellite's clock being 10 ns fast from that satellite being 3 m farther away.

## 4. Where relativity comes in

Relativity says clocks don't all run at the same rate. Two effects matter for GPS, and they push in opposite directions.

### Effect 1: moving clocks run slow (special relativity)

A clock moving at speed *v* relative to you ticks slower by a fraction of roughly

```
v² / (2c²)
```

GPS satellites move at about 3.87 km/s:

```
(3874 m/s)² / (2 × (3.0×10⁸ m/s)²) ≈ 8.3 × 10⁻¹¹
```

Over one day (86,400 s) that adds up to about **7 microseconds slow**.

### Effect 2: clocks higher up run fast (general relativity)

Clocks deeper in a gravitational field run slower. A clock at the satellite's altitude feels weaker gravity than one on the ground, so it runs faster. The fractional difference is

```
(GM/c²) × (1/R_earth − 1/r_orbit)
```

Here *GM* = 3.986×10¹⁴ m³/s² is Earth's gravitational parameter, *R*_earth ≈ 6,371 km and *r*_orbit ≈ 26,560 km, measured from Earth's centre:

```
3.986×10¹⁴ × (1/6.371×10⁶ − 1/2.656×10⁷) / (3.0×10⁸)² ≈ 5.3 × 10⁻¹⁰
```

Over one day that is about **45 microseconds fast**.

### The net effect

```
+45 μs/day  (higher up → faster)
 −7 μs/day  (moving → slower)
───────────
+38 μs/day  satellite clocks gain on ground clocks
```

38 microseconds is 38,000 nanoseconds. At 30 cm per nanosecond, that much timing error is about **11 km of light travel per day**. The system needs nanosecond agreement, and relativity puts tens of thousands of nanoseconds of disagreement into it every day.

A note on the popular claim that "without relativity GPS would drift 11 km a day". That number shows the *scale* of the effect, but it isn't literally what would happen. If every satellite clock gained exactly the same amount, part of the error would end up in the receiver's *b*. The ground stations also already estimate each satellite's clock drift and broadcast corrections. A more accurate statement is this: if nobody had accounted for relativity, the satellite clocks would steadily drift away from ground time, and the parts of the effect that differ from satellite to satellite and moment to moment (next section) would put metre-level errors directly into your position. Relativity isn't an optional refinement. You have to account for it for the system to work.

### What GPS actually does about it

**1. Detune the clocks at the factory.** Each satellite's reference oscillator is meant to run at 10.23 MHz. It is deliberately set slightly slow, to 10.22999999543 MHz, a fractional offset of about 4.465×10⁻¹⁰. Once the satellite is in orbit, the relativistic speed-up brings it to exactly 10.23 MHz as seen from the ground. This one adjustment removes almost all of the 38 μs/day.

**2. Correct for the slightly elliptical orbit.** The orbits are not perfect circles. When a satellite is nearest Earth it moves faster and sits deeper in gravity, so its clock runs slower. When it is farthest away, its clock runs faster. The resulting periodic clock error reaches a few tens of nanoseconds, which means up to about 10 m of range error. A fixed factory offset can't remove a varying error, so the receiver calculates it from the broadcast orbit and subtracts it. In the GPS specification it appears as `Δt_r = F · e · √a · sin(E)`, where *e* is how elliptical the orbit is, *a* is the size of the orbit, *E* is where the satellite is in its orbit, and *F* = −4.4428×10⁻¹⁰ s/√m is a constant built from *G*, Earth's mass and *c*.

**3. Account for Earth turning while the signal travels (the Sagnac effect).** Positions are computed in a frame that rotates with Earth. During the roughly 70 ms the signal is in flight, the ground under you moves by up to about 30 m. The receiver handles this by rotating each satellite's position back by the angle Earth turns during the signal's flight. Leave this out and you get errors of tens of metres.

## Summary

- GPS measures **time**, not distance. A delay multiplied by the speed of light gives a range, and 1 ns of error gives 30 cm of range error.
- Your receiver's clock is unknown, so it solves for **four unknowns** (*x*, *y*, *z*, clock error) using **at least four satellites**, by repeatedly linearising and fitting.
- That only works if the **satellite clocks keep nanosecond agreement** with ground time.
- Relativity breaks that agreement by a lot. Orbital speed makes satellite clocks lose about 7 μs/day, and weaker gravity makes them gain about 45 μs/day, for a net gain of about **38 μs/day**, thousands of times the allowed error.
- GPS deals with this by **detuning the satellite clocks before launch**, having **receivers correct for elliptical orbits**, and **accounting for Earth's rotation** during signal travel. Each of these is engineering that relativity requires.
