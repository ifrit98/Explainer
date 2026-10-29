# Why are there two high tides a day, not one?

If the Moon's gravity pulls the ocean toward it, you would expect one heap of water on the side facing the Moon. As the Earth turns, each place would pass under that heap once a day, so you would get one high tide a day.

In fact most coasts get two high tides a day, about 12 hours 25 minutes apart. So there must be a second heap of water on the side of the Earth facing *away* from the Moon. This explainer shows where that second heap comes from.

The short answer is this: **tides are not caused by the Moon's pull. They are caused by the *difference* in the Moon's pull between one part of the Earth and another.** That difference points toward the Moon on the near side and away from the Moon on the far side. So the ocean is stretched in both directions.

There is an interactive companion, [`index.html`](index.html), where you can switch between "the pull" and "the difference in pull" and watch the two bulges form. It's worth opening once you reach section 2.

---

## 1. The whole Earth is falling toward the Moon

The Moon's gravity acts on all of the Earth, not just the oceans. It pulls on the rock, the core, you, and the water. As a result the Earth as a whole accelerates toward the Moon. (That acceleration is what keeps the Earth and Moon orbiting their common centre of mass. If neither was moving sideways, they would simply fall together.)

The Earth is in free fall toward the Moon, in the same way an astronaut in orbit is in free fall toward the Earth. An astronaut in the space station doesn't feel the Earth's gravity as a force, because they and the station are falling together. In the same way, the Earth's surface does not "feel" the Moon's average pull. Everything on and in the Earth gets that average pull, so it moves along with the planet and nothing shifts relative to anything else.

What *can* be felt is any part of the Moon's pull that is **different from the average**. The average here means the pull at the Earth's centre.

## 2. Gravity weakens with distance, so the pull is uneven

Gravity falls off as 1/r². The Earth is about 12,700 km across, and the Moon is about 384,000 km away. So different parts of the Earth are at noticeably different distances from the Moon:

| Location | Distance to Moon | Moon's pull compared with the centre |
|---|---|---|
| Near side (Moon overhead) | d − R | a bit **stronger** |
| Earth's centre | d | the reference |
| Far side (Moon underfoot) | d + R | a bit **weaker** |

Here *d* is the Earth–Moon distance and *R* is the Earth's radius.

Now subtract the pull at the centre from the pull at each point. What is left over is called the **tidal acceleration**:

- **Near side:** the pull is stronger than at the centre, so the leftover points *toward* the Moon. Water there is pulled toward the Moon a bit more than the Earth is, and it rises.
- **Far side:** the pull is weaker than at the centre, so the leftover points *away* from the Moon. The Earth is pulled toward the Moon a bit more than the water on the far side is. The water is left behind, and it rises too.
- **The two sides at 90°:** these points are about as far from the Moon as the centre is. But the pull there is aimed at the Moon, which is not quite parallel to the pull at the centre. The pulls at those points tilt slightly inward toward the Earth–Moon line, so the leftover points *inward*. Water there is squeezed down.

The result is a stretch along the Earth–Moon line and a squeeze across it. The ocean takes on a slightly rugby-ball shape, with **two bulges: one under the Moon and one opposite it.**

```
                 squeeze
                    ↓
          ←  ( · · · · · )  →            ● Moon
        bulge       ↑        bulge
                 squeeze
   (leftover pull points AWAY      (leftover pull points TOWARD
    from the Moon on the far side)  the Moon on the near side)
```

The far-side bulge is often explained as a "centrifugal effect" of the Earth–Moon orbit. You can get the right answer that way if you are careful about reference frames, but you don't need it. The two bulges would still appear if the Earth and Moon fell straight toward each other with no orbit at all. Uneven gravity combined with free fall is enough.

## 3. A little algebra

Write *GM* for the Moon's mass times the gravitational constant.

At the near-side point, the leftover pull is:

```
GM/(d−R)² − GM/d²
```

Factor out GM/d², and use the approximation (1 − x)⁻² ≈ 1 + 2x for small x (here x = R/d ≈ 1/60):

```
GM/d² · [ (1 − R/d)⁻² − 1 ]  ≈  GM/d² · 2R/d  =  2GMR/d³   (toward the Moon)
```

On the far side the same steps give about 2GMR/d³ *away* from the Moon. That is the same size in the opposite direction, so the two bulges are nearly equal.

On the sides, the pull tilts inward by an angle of about R/d. That gives an inward leftover of about GMR/d³, half as large.

Two things stand out:

1. **The tidal effect goes as 1/d³, not 1/d².** It is the *gradient* of gravity, and taking a gradient adds another power of distance. This will matter for the Sun in section 6.
2. **It is tiny.** With the real numbers (GM_Moon ≈ 4.9×10¹² m³/s², R ≈ 6.37×10⁶ m, d ≈ 3.84×10⁸ m), GMR/d³ ≈ 5.5×10⁻⁷ m/s². That is about one ten-millionth of the Earth's surface gravity.

If you'd like to check the vector picture yourself, this short Python script computes the leftover pull at points around the Earth:

```python
import math

GM = 4.9e12        # Moon, m^3/s^2
R  = 6.37e6        # Earth radius, m
d  = 3.84e8        # Earth–Moon distance, m

def pull(x, y):
    """Moon's gravitational acceleration at (x, y); Moon sits at (d, 0)."""
    dx, dy = d - x, -y
    r = math.hypot(dx, dy)
    return GM * dx / r**3, GM * dy / r**3

cx, cy = pull(0, 0)                      # pull on Earth's centre
for deg in range(0, 360, 45):
    a = math.radians(deg)
    px, py = pull(R * math.cos(a), R * math.sin(a))
    tx, ty = px - cx, py - cy            # tidal = local pull − centre pull
    radial = tx * math.cos(a) + ty * math.sin(a)   # + = outward (up)
    print(f"{deg:3d}°  tidal {radial:+.2e} m/s² ({'up' if radial > 0 else 'down'})")
```

The output shows "up" at 0° (facing the Moon) and at 180° (facing away), and "down" at 90° and 270°. That is two bulges.

## 4. How can such a tiny force move an ocean?

At the near and far points, the tidal acceleration points straight up, against gravity that is ten million times stronger. Up there it does almost nothing.

What actually moves the water is the **sideways (horizontal) part** of the tidal acceleration. This part is largest about 45° away from the Moon's direction. Nothing opposes it directly. Gravity is vertical, so it cannot hold water in place sideways. Across thousands of kilometres of ocean, this small, steady sideways push herds water toward the two points on the Earth–Moon line. The water piles up there until the slope of the sea surface balances the push.

If the Earth were covered in a deep ocean that could keep up with the Moon instantly, the result is called the **equilibrium tide**. At its high points the water would be about 0.36 m above average. Halfway between them it would be about 0.18 m below average. The range from high to low would be roughly half a metre.

## 5. The Earth turns under the two bulges

The bulges stay lined up with the Moon while the Earth rotates beneath them. A spot on the coast therefore passes:

> under the near bulge (high) → the side (low) → under the far bulge (high) → the other side (low) → back to the start

That is **two highs and two lows for each turn of the Earth relative to the Moon.**

One turn relative to the Moon takes slightly more than 24 hours. While the Earth spins, the Moon moves about 13° along its orbit in the same direction, so the Earth needs about 50 extra minutes to catch up. This "lunar day" lasts about **24 h 50 min**. That is why high tides come about **12 h 25 min** apart, and why high tide is about 50 minutes later each day.

## 6. The Sun does the same thing, more weakly

The Sun pulls on the Earth about 180 times harder than the Moon does. But the tidal effect depends on mass/distance³, not mass/distance². The Sun is about 390 times farther away than the Moon, and that wipes out most of its advantage. **The Sun's tidal effect is about 46% of the Moon's.**

The Sun makes its own pair of bulges, which line up with the Sun. When the Sun, Earth and Moon are in a line (at new and full moon), the two sets of bulges add together and you get larger **spring tides**. When the Sun and Moon are at right angles (at the quarter moons), the Sun's bulges partly fill in the Moon's lows, and you get smaller **neap tides**. This happens twice a month.

## 7. What real coasts add

The two-bulge picture explains *why* the basic rhythm is twice a day. Real tides are shaped by much more:

- **Continents get in the way.** Water can't flow freely around the planet. Instead, each ocean basin sloshes like water in a bathtub, driven twice a day by the tidal push. The size of the tide depends on whether a basin's natural sloshing period is close to 12.4 hours. That is why the Bay of Fundy has ranges over 15 m while the Mediterranean has only a few tens of centimetres.
- **High tide is usually not when the Moon is overhead.** Water takes time to respond, so high tide can lag the Moon by hours. In some basins the tide circulates around a point where the height hardly changes at all.
- **Some places get one tide a day.** The Moon is usually north or south of the equator, which tilts the bulges. A location off the equator then passes through one bulge more squarely than the other, so its two daily highs are unequal. In some basins, such as parts of the Gulf of Mexico, the basin's response strengthens that once-a-day part until it dominates.

These are complications layered on top of the basic mechanism. The basic mechanism is still a stretch in two opposite directions, caused by gravity that varies across the Earth.

## Summary

- The Earth as a whole falls toward the Moon, so the Moon's *average* pull has no effect on the oceans.
- What remains is the *difference* between the pull at each point and the pull at the centre. It points toward the Moon on the near side and away from it on the far side.
- So the ocean bulges on both sides. Each place rotates through both bulges, which gives two high tides per 24 h 50 min.
- The effect goes as 1/d³, which is why the nearby Moon beats the much more massive Sun, about 2 to 1.
