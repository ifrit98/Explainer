# Why are there two high tides a day, not one?

**Short answer.** The Moon does not just pull the ocean toward itself. It pulls the near side of the Earth harder than the centre, and the centre harder than the far side. That *difference* in pull stretches the Earth's water along the Earth–Moon line. The result is two bulges: one facing the Moon and one facing away. The Earth turns under both bulges each day, so most coastlines get two high tides.

## The obvious model fails

The simplest idea is "the Moon's gravity pulls the water toward the Moon." That gives one bulge, on the side that faces the Moon. A place on the Earth would pass under it once per rotation: one high tide a day.

Most coasts have two high tides a day, about 12 h 25 min apart. So the simple model is missing something. The missing part is that the Moon pulls on the *whole Earth*, not only on the water.

## Step 1: the whole Earth falls toward the Moon

The Earth and the Moon orbit their common centre of mass. In practice, the Earth is in free fall toward the Moon. The Moon's gravity accelerates the Earth's centre toward the Moon all the time.

We live on the Earth and move with it. So what we see is not the Moon's pull itself. We see how the pull at each point **differs from** the pull at the centre. This difference is the **tidal acceleration**.

> Before you read on: the far side is pulled toward the Moon less than the centre. Relative to the centre, which way does far-side water move?

## Step 2: compute the pull at three points

Gravity weakens with distance: acceleration = GM / d². Use the Moon's values:

- GM of the Moon = 4.90 × 10¹² m³/s²
- Earth–Moon distance d = 384,400 km
- Earth radius R = 6,371 km

| Point | Distance to Moon | Moon's pull (m/s²) | Minus pull at centre |
|---|---|---|---|
| Near side | d − R = 378,029 km | 3.429 × 10⁻⁵ | **+1.13 × 10⁻⁶** (toward Moon) |
| Centre | d = 384,400 km | 3.316 × 10⁻⁵ | 0 |
| Far side | d + R = 390,771 km | 3.209 × 10⁻⁵ | **−1.07 × 10⁻⁶** (away from Moon) |

```text
Moon's pull on each point (longer arrow = stronger pull):

   far side          centre          near side              Moon
      •──>             •───>            •────>               ●

Subtract the pull at the centre (the whole Earth already has this motion):

     <•                  •                  •>
  1.07e-6 away         zero         1.13e-6 toward
```

The near-side water moves toward the Moon faster than the Earth does, so it bulges toward the Moon. The far-side water moves toward the Moon *slower* than the Earth does. The Earth falls away from it, so it bulges away from the Moon. The two values are almost equal. Both are close to 2GMR/d³ = 1.10 × 10⁻⁶ m/s².

At the two sides (90° from the Moon), the Moon's pull points slightly inward, toward the Earth–Moon line. This squeezes the water there by about GMR/d³ = 0.55 × 10⁻⁶ m/s². Water flows from the squeezed sides toward the stretched ends:

```text
                    squeeze
                       ↓
       bulge  ←   (   Earth   )   →  bulge              Moon ●
                       ↑
                    squeeze
```

**Why the far side is not pushed by "centrifugal force from the Earth's spin":** the spin is symmetric about the Earth's axis. It does not know where the Moon is, so it cannot make a bulge that points away from the Moon. The far bulge comes only from the difference in the Moon's pull.

## Step 3: what the number means

1.1 × 10⁻⁶ m/s² is about one ten-millionth of the Earth's gravity (9.8 m/s²). It cannot lift water vertically in any useful way. It works because part of it points *along* the surface, and nothing opposes horizontal flow except the slope of the water itself. The ocean flows until the slope of its surface balances the horizontal tidal pull, over a distance of thousands of kilometres.

For an ideal ocean that covers the whole Earth, the result is a difference of about half a metre between bulge and squeeze (model output, "equilibrium tide"). A larger tidal acceleration would give taller bulges. Because the effect goes as 1/d³, a Moon at half the distance would give 8 times the tidal acceleration.

## Step 4: the Earth turns under the bulges

The two bulges stay aligned with the Moon. The Earth turns under them. A point on the coast passes through bulge, squeeze, bulge, squeeze in one turn. That is two high tides and two low tides.

The cycle is 24 h 50 min, not 24 h. In one day the Moon moves about 13° along its orbit, in the same direction as the Earth turns. The Earth needs about 50 more minutes to face the Moon again. So high tides come every 12 h 25 min, and they are about 50 minutes later each day.

## The Sun does the same thing

The Sun produces tidal bulges by the same mechanism. Its pull is much stronger than the Moon's, but tides depend on the *difference* across the Earth, which goes as M/d³. For the Sun, the result is about 46% of the Moon's effect. When the Sun and Moon line up (new and full moon), their bulges add: large **spring tides**. When they are at 90° (quarter moons), they partly cancel: small **neap tides**.

## What this model leaves out

This is the idealized model: an ocean that covers the Earth and responds at once. Real tides are also shaped by continents, ocean depth, and resonance of ocean basins. These change the timing and the height a lot (for example, more than 15 m in the Bay of Fundy). In some places, such as parts of the Gulf of Mexico, basin shape and the Moon's tilt relative to the equator make one of the two daily tides dominate, so the coast sees one high tide a day. The two bulges are still the cause; local geography decides how they show up.
