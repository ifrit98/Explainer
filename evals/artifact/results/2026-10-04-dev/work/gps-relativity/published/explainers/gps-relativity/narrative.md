# Narrative: gps-relativity

## 1. Reader before and after

- **Before:** a technical reader: school mathematics and science (distance = speed × time, light speed ≈ 300,000 km/s, gravity, simultaneous equations), basic programming. New to GPS and to relativity.
- **After:** "A GPS receiver times signals from four satellites, turns each time into a distance, and solves for its position and its own clock error. This works only if the satellite clocks agree to nanoseconds, and relativity makes them gain 38 µs a day — 11 km of range — so they are set to tick slow before launch."

## 2. Question and motive

- **Question:** How does GPS find your position, and why does it need relativity? Result in words: the receiver measures how long signals take to arrive from four satellites; relativity makes the satellite clocks run fast by 38 µs a day, which would add about 11 km of range error per day, so the clocks are built to run slow.
- **Why care:** a phone with a cheap clock finds itself to a few metres, and the everyday device depends on Einstein's theory.
- **Why this approach:** distance = speed × time; the signal speed is known exactly (light speed), so measure time.

## 3. Introduction ledger

| Reference | Means | Grounded by | Beat |
|---|---|---|---|
| range | true distance from a satellite to the receiver | 67 ms of travel × light speed ≈ 20,200 km | 2 |
| pseudorange | travel time measured with the receiver clock × light speed; range + b | 1D example: 13.5 km where the range is 12 km | 4 |
| clock bias b | receiver clock error, in metres | 5 µs → 1.5 km | 4 |
| GPS time | reference time from atomic clocks at ground stations | satellites steered to it | 5 |
| time dilation | clocks in different motion or height tick at different rates | −7 and +45 µs/day | 6 |
| rate offset | satellite clock set to tick slow before launch | 10.23 → 10.22999999543 MHz | 8 |
| µs, ns | microsecond (10⁻⁶ s), nanosecond (10⁻⁹ s) | 1 µs ↔ 300 m, 1 ns ↔ 0.3 m | 2 |

## 4. Beats

| # | Kind | Reader's question | Bridge | Shown | Said | Reader now knows |
|---|---|---|---|---|---|---|
| 1 | hook | How does GPS work, and where does relativity come in? | — | answer paragraph (the result of §2 in words) | "The receiver times signals from four satellites and solves for its position and its own clock error. Relativity makes satellite clocks gain 38 µs a day, about 11 km of range, so they are built to tick slow." | the whole answer in outline |
| 2 | mechanism | How can a satellite tell you how far away it is? | so | the signal carries the satellite's position and its send time (the time stamp) | "Travel time = receive time − send time. Range = travel time × light speed c. From overhead, 67 ms × c ≈ 20,200 km. Light goes 300 m in 1 µs and 0.3 m in 1 ns, so a timing error becomes a range error at that rate." | timing gives range; timing must be precise |
| 3 | mechanism | How many ranges fix a point? | therefore | spheres | "One range puts the receiver somewhere on a sphere around the satellite (every point at that distance). Three spheres meet in two points; one is far from Earth and is rejected." | 3 satellites if all clocks were perfect |
| 4 | objection + instance | But my phone's clock is quartz, not atomic. | but | 1D worked example: beacons 0 and 30 km, receiver at 12 km, clock 5 µs fast; 13.5 + 19.5 = 33 km ≠ 30 km | "The receiver measures travel time with its own clock, so each result is a pseudorange: range + b, where b is the receiver clock error in metres (5 µs → 1.5 km). One clock makes every measurement, so b is the same in all of them. The excess 3 km = 2b gives b = 1.5 km. In 3D, b is a fourth unknown next to x, y, z, so the receiver needs a fourth satellite: four equations, four unknowns." | pseudorange, b, why four satellites |
| 5 | mechanism | So what accuracy do the satellite clocks need? | but | 17 ns ↔ 5 m | "The receiver can solve for its own clock error, because it is shared. Each satellite clock error is different and goes into only one pseudorange, so the receiver cannot solve for it. Satellite clocks must match GPS time — the time of atomic clocks at ground stations. For a 5 m fix (a typical phone), the error must be under about 17 ns." | satellite clocks must agree to ~10 ns |
| 6 | mechanism | What does relativity do to those clocks? | so | −7, +45, +38 µs/day vs ground clocks | "Time dilation: clocks in different motion or height tick at different rates (measured, not only predicted). The speed of 3.9 km/s makes a satellite clock lose 7 µs a day. The weaker gravity 20,200 km up makes it gain 45 µs a day. Net: it gains 38 µs a day, which is 11.4 km of range per day." | net fast 38 µs/day = 11.4 km/day |
| 7 | objection | Doesn't b absorb it, if every satellite drifts the same? | but | satellite A set to GPS time on day 0, B on day 3, read on day 5: 190 µs (57 km) vs 76 µs (22.8 km) | "b absorbs only an error that is equal in every pseudorange. The drift rate is equal, but each clock was set on a different day, so the accumulated errors differ: 34 km that no single b can absorb." | why the drift still ruins fixes |
| 8 | close | So what does GPS do? | therefore | 10.23 MHz → 10.22999999543 MHz | "Each satellite clock counts ticks of a 10.23 MHz signal. Before launch, engineers set it 4.5 × 10⁻¹⁰ slower — exactly the 38 µs/day gain as a fraction — so in orbit it ticks at the ground rate. Ground stations upload small remaining corrections." | the fix |
| 9 | recap | — | — | — | one-sentence answer; Scope list: atmosphere, Earth's rotation during flight, orbit-shape correction, more than four satellites | after-sentence |

## 5. Concrete to symbol

Pseudorange = range + b shown in the 1D example (13.5 = 12 + 1.5) before the general equation.

## 6. Links between representations

Times and distances always paired: µs with km via 0.3 km per µs.

## 7. Close the loop

- **Answer:** four time measurements give position and receiver clock error; relativity's 38 µs/day would add 11 km/day of range error, so satellite clocks tick slow by design.
- **Payoff:** the reader can turn any timing error into a range error, and predict which effect wins.
- **Scope:** atmosphere, Sagnac, eccentricity correction, least squares with more satellites.
