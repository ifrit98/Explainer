# How greenhouse gases warm the Earth

**The short answer:** The Earth gets energy from sunlight and loses it as infrared radiation to space. A few gases in the air, mainly water vapour and carbon dioxide, absorb that infrared. Because of them, the radiation that reaches space comes mostly from high, cold layers of the atmosphere rather than from the warm surface. Cold things radiate less. To get rid of all the energy it receives, the planet has to be warmer than it would be without those gases. Adding more of them pushes the radiating layer higher, where it is colder. The planet then loses less energy than it takes in, and it warms until the two match again.

The rest of this document builds that answer one step at a time. Each step is a small piece of physics you can check with a calculator. The companion page `index.html` lets you change the inputs of the two models below and see what happens.

---

## 1. The planet is a budget: energy in = energy out

Leave the atmosphere out at first. The Earth sits in sunlight and gains energy. It also radiates energy away into space. If it gains more than it loses, it warms up. A warmer body radiates more, so the warming continues until the losses equal the gains. That balanced state sets the planet's temperature.

**Energy in.** At Earth's distance from the Sun, sunlight carries about **S = 1361 W/m²** through a surface facing it. The Earth catches this on a disc of area πR², but it is a sphere of area 4πR². Averaged over the whole surface, day and night, that gives S/4 ≈ 340 W/m². About 30% of it is reflected straight back by clouds, ice and bright surfaces (this fraction is the *albedo*, α ≈ 0.3). What is actually absorbed is

```
absorbed = S (1 − α) / 4 ≈ 1361 × 0.7 / 4 ≈ 238 W/m²
```

**Energy out.** Every object radiates according to its temperature. For an ideal emitter (a "black body") the **Stefan–Boltzmann law** gives

```
emitted = σ T⁴,      σ = 5.67 × 10⁻⁸ W m⁻² K⁻⁴
```

Note the fourth power. A small rise in temperature makes a body radiate quite a lot more.

**Balance.** Set the two equal and solve for T:

```
σ T⁴ = 238   →   T = (238 / 5.67e-8)^(1/4) ≈ 255 K ≈ −18 °C
```

The measured average surface temperature is about **288 K (+15 °C)**. That leaves a gap of roughly **33 K**. This gap is the greenhouse effect, and the rest of the document explains where it comes from.

## 2. Sunlight and earthlight are different colours

The radiation a body gives off peaks at a wavelength set by its temperature (**Wien's law**: peak ≈ 2898 µm·K / T).

| Emitter | Temperature | Peak wavelength | Kind of light |
|---|---|---|---|
| Sun's surface | ~5800 K | ~0.5 µm | visible |
| Earth's surface | ~288 K | ~10 µm | thermal infrared |

The two spectra hardly overlap. This is what makes the greenhouse effect possible. Air can be almost transparent to incoming sunlight and still be largely opaque to outgoing infrared. The air acts on the energy going out and does little to the energy coming in.

## 3. Why only some gases absorb infrared

About 99% of dry air is nitrogen (N₂) and oxygen (O₂), and these barely absorb thermal infrared. The reason is molecular.

A molecule absorbs or emits infrared by changing how it vibrates or rotates. It can only do this if the motion **changes the molecule's electric dipole**, because the dipole is what the light's oscillating electric field can push on. N₂ and O₂ are two identical atoms. However they stretch, the molecule stays symmetric and has no dipole, so infrared light has almost nothing to act on.

Molecules with three or more atoms, or with two different atoms, behave differently:

- **CO₂** (O=C=O) is straight and symmetric at rest. When it **bends**, or when it stretches asymmetrically, a dipole appears. The bending mode absorbs strongly near **15 µm**, close to the peak of Earth's emission.
- **H₂O** is bent to begin with and absorbs across wide ranges of the infrared.
- **CH₄** (methane), **N₂O** (nitrous oxide) and **O₃** (ozone) each have their own absorption bands.

Together these absorb most outgoing infrared at most wavelengths. The main exception is a gap between about 8 and 13 µm, the **atmospheric window**, where clear air is fairly transparent. Through that window the surface radiates fairly directly to space.

One detail matters for later. In the lower atmosphere, a CO₂ molecule that absorbs a photon nearly always collides with neighbouring molecules (mostly N₂ and O₂) before it can re-emit. Collisions happen roughly every nanosecond, and the excited state would take much longer than that to radiate. So the absorbed energy turns into ordinary heat in the surrounding air. Separately, CO₂ is constantly excited by collisions and **emits** at a rate set by the *local air temperature*. Remember this point: **what a layer of air emits depends on how warm that layer is.**

## 4. The simplest model: one absorbing layer

Model the atmosphere as a single layer. It is transparent to sunlight and absorbs a fraction ε of the surface's infrared, with 0 ≤ ε ≤ 1. A layer that absorbs a fraction ε also emits ε times the black-body amount (Kirchhoff's law). It emits from both faces, so the same amount goes up and down.

Write E_s = σT_s⁴ for the surface emission and E_a = σT_a⁴ for the black-body emission at the layer's temperature. At equilibrium every part must balance:

```
Atmosphere layer:   absorbs ε·E_s   =  emits ε·E_a up + ε·E_a down
                    →  E_a = E_s / 2

Top of atmosphere:  238 (in)  =  (1 − ε)·E_s  +  ε·E_a      (out)
                               =  E_s (1 − ε/2)

So:                 T_s = [ 238 / (σ (1 − ε/2)) ]^(1/4)
```

Some values:

| ε | T_s |
|---|---|
| 0 (no greenhouse gases) | 255 K |
| 0.78 | ≈ 288 K, today's value |
| 1 (fully opaque) | 255 × 2^(1/4) ≈ 303 K |

This shows the mechanism directly. The surface now gets sunlight **plus** downward infrared from the warm air, so it has to warm up until its own emission gets rid of both. The downward infrared is real and measurable: instruments on the ground record about 340 W/m² of it on average, which is more than the surface receives from the Sun.

The model has a problem, though. In it, the effect stops growing once the layer is fully opaque (ε = 1). The real atmosphere is already opaque at the centre of the CO₂ band, yet adding CO₂ still causes warming. Explaining that needs a better picture.

## 5. The better picture: the height at which Earth radiates to space

Two facts about the real atmosphere matter here.

1. **It gets colder with height.** In the lowest ~10–15 km (the troposphere), air rising and expanding cools by about **6.5 K per km** on average. This rate of cooling with height is called the *lapse rate*. Convection keeps this profile in place.
2. **It is thick in infrared.** At a wavelength the gases absorb strongly, a photon emitted low down is absorbed again almost immediately. Only photons emitted from fairly **high up**, where there is little absorbing gas above them, get out to space.

So at each wavelength there is an **effective emission height**, roughly the level above which the air is too thin to stop the radiation. Space receives radiation at the *temperature of that height*, not the temperature of the surface.

Averaged over all wavelengths, the Earth radiates to space like a black body at 255 K. In the real atmosphere, 255 K is found at about **5 km** up. Starting from the emission height and going down at the lapse rate:

```
T_surface ≈ T_emission + Γ × H ≈ 255 K + 6.5 K/km × 5 km ≈ 288 K
```

The same 33 K appears again, this time explained through altitude.

**Now add CO₂.** With more absorber, the air becomes opaque higher up, so the emission height rises. A higher level is colder, and colder air radiates less (T⁴ again). For a while the planet sends out **less** than the 238 W/m² it absorbs. This shortfall is called **radiative forcing**. The planet keeps gaining energy and warms until the whole temperature profile has shifted up enough that the new, higher emission level is back at 255 K. Because the lapse rate holds the profile together, the surface ends up warmer by about Γ × (rise in emission height).

This also deals with the "CO₂ is already saturated" objection. Being saturated at the band centre means that **surface** radiation at those wavelengths cannot escape. That was never the source of the effect. The emission level can always move higher. At the edges of the band, where absorption is weaker, extra CO₂ also moves those wavelengths from "escapes from low and warm" to "escapes from high and cold". As a result the effect grows roughly with the **logarithm** of concentration, not linearly, but it does not stop.

## 6. Putting numbers on it

A widely used fit from detailed radiation calculations gives the forcing from CO₂ as

```
ΔF ≈ 5.35 × ln(C / C₀)  W/m²
```

Doubling CO₂ (C/C₀ = 2) gives ΔF ≈ **3.7 W/m²**. Before industrialisation C₀ was about 280 ppm. By the mid-2020s it was above 420 ppm.

How much warming does that cause? Differentiate σT⁴ at 255 K:

```
d(σT⁴)/dT = 4σT³ ≈ 3.8 W/m² per K
```

That is how much more a black body at 255 K radiates for each degree of warming. Detailed models give about 3.2 W/m² per K for the real Earth (this is called the *Planck response*). On its own, then, doubling CO₂ warms the planet by about

```
ΔT ≈ 3.7 / 3.2 ≈ 1.2 K
```

Using the lapse rate, that corresponds to the emission height rising by only about 1.2 / 6.5 ≈ 0.18 km, under 200 metres.

## 7. Feedbacks: the planet responds to its own warming

The 1.2 K figure assumes nothing else changes. Several other things do change:

- **Water vapour (strongly amplifies).** Warmer air can hold about 7% more water vapour per kelvin (the Clausius–Clapeyron relation). Water vapour is itself a greenhouse gas, so this adds to the warming.
- **Lapse rate (partly offsets).** In the tropics, warming is greater aloft than at the surface. That lets the planet radiate a little more easily, which damps the warming somewhat.
- **Ice and snow (amplifies).** Melting replaces bright surfaces with darker ones, so the albedo falls and more sunlight is absorbed.
- **Clouds (uncertain, probably amplifying overall).** Clouds both reflect sunlight, which cools, and absorb infrared, which warms. How they change is the largest single source of uncertainty.

Feedbacks can be included by replacing the 3.2 with a smaller net "restoring" value λ. Then ΔT = ΔF / λ. Current assessments put the long-term warming from doubled CO₂ (the *equilibrium climate sensitivity*) **likely between about 2.5 and 4 K, with about 3 K as the best estimate**. That is roughly 2–3 times the no-feedback value.

**Why CO₂ and not water vapour?** Water vapour contributes the largest share of today's greenhouse effect, around half. Clouds contribute about a quarter, and CO₂ about a fifth. But the amount of water vapour is set by temperature: if there is too much, it rains out within days. CO₂ does not condense, and it stays in the air for centuries. CO₂ therefore acts as the control setting, and water vapour amplifies whatever change CO₂ makes.

## 8. Common misconceptions

- **"It works like a glass greenhouse."** Not really. A real greenhouse stays warm mainly because the glass stops warm air from rising away by convection. The name stuck anyway.
- **"The gases reflect heat back down."** They absorb it and then emit according to their own temperature. The emission-height picture explains the effect better than "trapping" does.
- **"It's to do with the ozone hole."** The ozone hole is a separate problem. Ozone is a greenhouse gas, but the ozone hole does not drive global warming.
- **"Extra CO₂ can't matter if the band is saturated."** See Section 5: the emission height keeps rising.

## 9. A fingerprint you can check

If the Sun were causing the warming, the whole atmosphere would warm. Greenhouse warming predicts something different: the **troposphere warms while the stratosphere cools**. Above about 15 km, extra CO₂ mainly helps the air radiate its energy to space, so that layer cools. Observations since the 1960s show this pattern: a warming troposphere under a cooling stratosphere.

---

### Summary

1. In equilibrium, absorbed sunlight (~238 W/m²) equals emitted infrared (σT⁴), which gives 255 K for a planet with no greenhouse gases.
2. Sunlight is visible and earthlight is infrared, so a gas can affect one and not the other.
3. Only molecules whose vibrations change their dipole (CO₂, H₂O, CH₄, …) absorb infrared. N₂ and O₂ do not.
4. These gases make the planet radiate to space from about 5 km up, where it is 255 K. The lapse rate then puts the surface 33 K warmer.
5. More CO₂ raises the emission height, into colder air. Less energy leaves than arrives, and the planet warms until balance returns. Doubling CO₂ gives about 3.7 W/m² of forcing and 1.2 K of warming directly, and about 3 K once feedbacks are included.
