# Why are there two high tides a day, not one?

<!-- Stage 1, rendered from model.md in STE-80. -->

**The Moon raises two bulges of ocean on opposite sides of Earth: one facing the Moon and one facing away. Earth turns under both bulges, so a point on the coast passes through two high tides in each turn.**

## Predict first

The Moon pulls water toward it. If that were the whole story, how many bulges would you expect, and where? Decide before you read on.

## The Moon pulls every part of Earth by a different amount

The Moon's gravity gives an acceleration, here called the **pull**, of GM/r². The pull gets weaker with distance r. Earth is 12,742 km wide, so its near side is closer to the Moon than its far side. With the Moon at 384,400 km and Earth's radius 6,371 km:

| Point on Earth | Distance to Moon | Pull (m/s²) | Pull minus centre's pull (m/s²) |
|---|---|---|---|
| Near side | 378,029 km | 3.433e-5 | 1.13e-6 toward the Moon |
| Centre | 384,400 km | 3.320e-5 | 0 |
| Far side | 390,771 km | 3.213e-5 | 1.07e-6 away from the Moon |

All three pulls point toward the Moon. So why does the far water move away from the Moon?

## Only the difference in pull moves water

<!-- claim: why-subtract -->
Earth is not held in place. The whole Earth falls toward the Moon with the pull at its centre, 3.320e-5 m/s². (Earth and Moon orbit each other, so this fall never ends in a collision.) The common part of the pull moves rock and water together, so it changes nothing on the surface.
What moves water relative to Earth is the **tidal acceleration**: the pull at a point minus the pull at Earth's centre. That is the last column of the table.

<!-- claim: mech-bulges -->
- On the near side, the water is pulled more than Earth's centre. It falls toward the Moon a little faster than Earth does: a bulge toward the Moon.
- On the far side, the water is pulled less than Earth's centre. Earth falls toward the Moon a little faster than this water. The water falls behind: a bulge away from the Moon.

<!-- claim: misc-push -->
Nothing pushes the far water. It is pulled toward the Moon, but less than the rest of Earth.

```text
                far bulge        near bulge
                   ___             ___
   (relative)  <- /   \  EARTH    /   \ ->      ( MOON )
                  \___/  centre   \___/
   pulled less than centre        pulled more than centre
```

The tidal acceleration is about 1.1e-6 m/s², about one ten-millionth of g (9.81 m/s²). In an ideal ocean, it raises the water by about 0.5 m from low to high.

## Evidence that the difference is what counts: the Sun

The Sun's pull on Earth is 179 times the Moon's. If the raw pull made tides, solar tides would dwarf lunar tides. They do not: solar tides are 0.46 of lunar tides. A difference across a fixed width falls off as 1/d³, not 1/d², and that punishes the distant Sun.

## Why two highs, and why not exactly every 12 hours

<!-- claim: mech-rotation -->
The two bulges stay lined up with the Moon. Earth turns under them. A point on the coast passes the near bulge, then the far bulge half a turn later.

The Moon also moves along its orbit, about 12° per day, in the same direction as Earth turns. Earth must turn a little extra to bring the point back under the Moon. So the cycle is a **lunar day** of 24 h 50 min, and high tides come about every 12 h 25 min. High tide comes about 50 minutes later each day.

## Limits

- **Assumption:** this is the idealized "equilibrium tide": one ocean covers Earth and adjusts at once. Real oceans have continents and basins that resonate. Some coasts, such as parts of the Gulf of Mexico, get only one high tide a day.
- **Not covered:** spring and neap tides, where the Sun's smaller pair of bulges adds to or partly cancels the Moon's.
