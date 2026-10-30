# Why are there two high tides a day, not one?

Most coasts get two high tides a day. One comes when the Moon is high in the sky. The other comes when the Moon is on the opposite side of the Earth. If the Moon simply pulls water toward itself, the second high tide makes no sense.

**The Moon does not lift the ocean toward itself. It stretches the ocean along the Earth–Moon line, and a stretch has two ends. The Earth turns through both ends, so a place gets two high tides.**

## The pull at three points

The Moon's pull is the acceleration that the Moon's gravity gives at a point. Take three points on the Earth–Moon line: the **near side** (the surface point that faces the Moon), Earth's **centre**, and the **far side** (the surface point opposite the Moon). The unit is µm/s², one millionth of a m/s².

| Point | Distance to Moon | Moon's pull (toward the Moon) |
|---|---|---|
| near side | 378,029 km | 34.32 µm/s² |
| centre | 384,400 km | 33.19 µm/s² |
| far side | 390,771 km | 32.12 µm/s² |

All three pulls point toward the Moon. So why does the far-side water not move toward the Moon?

## Only the part that differs from the centre's pull acts

<!-- claim: mech-subtract -->
The Earth and the Moon orbit their shared centre of mass. An orbit is free fall: the whole Earth falls toward the Moon, and Earth's centre accelerates at 33.19 µm/s². An acceleration that every part shares does not change the shape of a falling body.

So subtract the centre's pull. The remainder is the **tidal acceleration**: the Moon's pull at a point minus the Moon's pull at Earth's centre. Here + means toward the Moon.

- Near side: 34.32 − 33.19 = +1.13. The near-side water falls toward the Moon faster than the centre, so it moves ahead of the centre, toward the Moon.
- Far side: 32.12 − 33.19 = −1.07. The far-side water falls toward the Moon slower than the centre, so it is left behind, away from the Moon.

<!-- claim: misc-push -->
Both results point away from Earth's centre. The Moon does not push the far side away. It pulls the far side less than it pulls the centre, and the centre's fall sets the reference. The near value is about 5% larger because the pull changes faster closer to the Moon.

Now take a **side point**, 90° from the near side. Its pull has almost the same size as the centre's, 33.18 µm/s², so along the Earth–Moon line the two cancel. But the pull points at the Moon, from 6371 km off the line, so it tilts by R/d = 6371 / 384,400 = 0.0166 rad (0.95°) toward Earth's centre. That tilt leaves 33.19 × 0.0166 = 0.55 µm/s², pointing toward Earth's centre. So the tidal acceleration stretches the Earth along the Earth–Moon line and squeezes it across that line.

## How a tiny acceleration moves an ocean

1.1 µm/s² is about one ten-millionth of g (9.81 m/s²). Up or down, the tidal acceleration changes the weight of the water by 1 part in 10 million, which does nothing. But Earth's gravity has no part along a level surface, so the tidal acceleration is the only sideways push. It is largest 45° from the near side, at 0.82 µm/s², and points toward the nearer end of the line. Water flows until the sea surface slopes just enough that gravity along the slope balances this push. The water gathers into two **bulges**: one under the Moon, one opposite it. A **high tide** is the time when a place passes through a bulge.

```text
                     side point: 0.55 µm/s² down, low water
                                  |
                       ↙          v          ↘
                         . - ~~~~~~~~~~~ - .
     far-side bulge  <--(       Earth       )-->  near-side bulge   ----->  Moon
     (-1.07 µm/s²)       ' - ~~~~~~~~~~~ - '      (+1.13 µm/s²)
                       ↖          ^          ↗
                                  |
                     side point

  ↙ ↘ ↖ ↗ : sideways push along the surface, 0.82 µm/s² at 45°, toward the nearer bulge
```

## Why subtract: two tests

<!-- claim: why-subtract -->
The simplest idea, that the Moon's pull itself raises the tide, fails two tests.

<!-- claim: guar-far-bulge -->
First, imagine that something held the Earth still, so that it did not fall toward the Moon. Then nothing subtracts the centre's 33.19. The far side's 32.12 µm/s² points toward the Moon, which on the far side is down into the Earth. That Earth has one bulge, not two. The far bulge exists because the Earth falls.

Second, the Sun. Its pull on the Earth is 179 times the Moon's, so the pull alone predicts solar tides 179 times larger. But a pull GM/r² changes by about 2R/d of itself across one Earth radius R, at distance d. So the tidal acceleration is about the pull times 2R/d. For the Moon: 33.19 × 2 × 6371 / 384,400 = 1.10, between 1.13 and 1.07. The Sun is 389 times farther than the Moon, so its tidal acceleration is about 179 / 389 = 0.46 times the Moon's. Observed solar tides are about half the Moon's.

## Two high tides per turn

<!-- claim: mech-rotation -->
The bulges stay on the Earth–Moon line, and the Earth turns under them. The Moon also moves about 12° a day along its orbit, in the same direction that the Earth turns. The Earth turns about 15° an hour, so it needs about 50 minutes more than 24 hours to face the Moon again: a **lunar day** of 24 h 50 min. A place passes through both bulges in each lunar day, so high tides come every half lunar day: 12 h 25 min. A high tide at 8 in the morning gives the next at about 8:25 in the evening.

## The answer

The Moon pulls the near side more than Earth's centre, and the centre more than the far side. The Earth falls with its centre, so these differences stretch the ocean into two bulges, and the Earth turns through both each lunar day. No centrifugal force is needed. The pulls depend only on distance, so an Earth that fell straight at the Moon, with no orbit, would get the same +1.13 and −1.07 and the same two bulges.

## Scope

- **Height:** in an ideal ocean, the bulges rise about 0.36 m above the mean (an estimate). Look up "equilibrium tide".
- **Real oceans:** continents and basin shapes make tides lag the Moon, reach metres on some coasts, and come once a day on others. Look up "dynamic theory of tides".
