# How greenhouse gases warm the Earth

**Short answer.** Earth loses heat to space only as infrared light. Greenhouse gases absorb infrared light. To send out as much energy as it gets from the Sun, the whole lower atmosphere and the surface must become warmer.

The sections below build this answer step by step, with numbers.

## 1. The puzzle: Earth is 33 K too warm

Energy that enters a planet must leave it, or the planet keeps warming. Start with the energy that enters.

- Sunlight at Earth's distance delivers **1361 W/m²** to a surface that faces the Sun.
- Earth intercepts sunlight with a disc of area πR², but it has a surface of area 4πR². Spread over the whole sphere, the mean input is 1361 / 4 ≈ **340 W/m²**.
- Clouds, ice, and other bright surfaces reflect about 30% of it. Earth absorbs 340 × 0.70 ≈ **238 W/m²**.

Now the energy that leaves. Every object emits thermal radiation. The **Stefan–Boltzmann law** gives the power per square metre from an object at absolute temperature T:

  P = σT⁴, with σ = 5.67 × 10⁻⁸ W m⁻² K⁻⁴.

The T⁴ makes emission very sensitive to temperature: 10% warmer means about 46% more emission.

Set emission equal to absorption and solve for T:

  T = (238 / 5.67 × 10⁻⁸)^(1/4) ≈ **255 K** (−18 °C).

The measured mean surface temperature is **288 K** (15 °C). The surface is 33 K warmer than the simple balance predicts. A surface at 288 K emits σ × 288⁴ ≈ **390 W/m²**, but only about 238 W/m² leaves the top of the atmosphere. The atmosphere stops about **150 W/m²** of the surface emission from reaching space. The rest of this explanation shows how.

## 2. Sunlight and Earth-light are different colours

The wavelength at which an object emits most strongly falls as the object gets hotter (**Wien's law**: peak wavelength ≈ 2898 µm·K / T).

| Emitter | Temperature | Peak wavelength | Type |
|---|---|---|---|
| Sun | 5800 K | 2898 / 5800 ≈ 0.5 µm | visible light |
| Earth | 288 K | 2898 / 288 ≈ 10 µm | infrared |

The two bands hardly overlap. So the atmosphere can be nearly transparent to the incoming energy and nearly opaque to the outgoing energy. The gases that do this are the greenhouse gases.

## 3. Why CO2 and water absorb infrared, but N2 and O2 do not

A molecule absorbs light when the light's electric field can push its charges into a new motion. For infrared, that motion is a vibration of the atoms. The push works only if the vibration changes the molecule's **dipole**, the separation of its positive and negative charge.

- **N2 and O2** (99% of dry air) have two identical atoms. When they stretch, the charge stays symmetric, so the dipole stays zero. They are almost transparent to infrared.
- **CO2** is O=C=O. When it bends, the carbon moves off the line of the oxygens and a dipole appears. This bend absorbs strongly near **15 µm**, close to the peak of Earth's emission.
- **H2O** is already bent and has many vibration and rotation modes. It absorbs across much of the infrared. CH4 and N2O act in the same way.

A gas that absorbs at a wavelength also emits at that wavelength, at a rate set by its own temperature. Greenhouse gases do not reflect infrared. They absorb it, share the energy with the surrounding air through collisions, and emit new infrared in all directions.

## 4. A first model: one absorbing layer

Take the simplest version. Put one layer of air above the surface. It is transparent to sunlight and absorbs all infrared.

*Predict before you read on: will the surface be warmer than 255 K, colder, or the same?*

- Space sees only the layer. The layer must emit 238 W/m² upward, so the layer is at 255 K.
- The layer emits equally up and down. It sends 238 W/m² down to the surface as well.
- The surface receives 238 (Sun) + 238 (layer) = 476 W/m². It must emit that much: T = (476 / σ)^(1/4) ≈ **303 K**.

So the absorbing layer warms the surface. But 303 K is 15 K too warm. The model fails for two reasons:

1. Real air does not absorb all infrared. Between about 8 and 13 µm, few gases absorb, and some surface emission escapes directly through this **window**.
2. Warm surface air rises, so **convection** carries heat upward. Radiation is not the only path.

The one-layer model shows *that* absorption warms the surface. It cannot show why *more* CO2 warms it further. If the layer already absorbs everything, extra CO2 would change nothing.

## 5. The lapse rate

**Air gets colder with height.** Rising air expands as pressure falls, and expansion cools it. Convection keeps mixing the lower atmosphere (the **troposphere**), so its temperature falls at a nearly fixed rate, the **lapse rate**. The mean lapse rate is about **6.5 K per km**.

## 6. Why adding CO2 warms the surface

*Predict: the centre of the CO2 band already absorbs almost all 15 µm light within the lowest few hundred metres. Does adding more CO2 still matter?*

It does. Less energy leaves than arrives, so the planet gains energy. This imbalance is the **radiative forcing**. A fit to detailed radiation calculations gives:

  ΔF ≈ 5.35 × ln(C / C₀) W/m², where C is the CO2 concentration and C₀ the starting value.

The logarithm appears because the band centre is already opaque. Extra CO2 acts mostly at the edges of the band, where absorption is weaker, and each doubling widens the band by a similar amount.

**Worked example: double CO2.**

- Forcing: 5.35 × ln 2 ≈ **3.7 W/m²** less energy leaving.
- How much warming removes this? Differentiate P = σT⁴: dP/dT = 4σT³ = 4 × 5.67 × 10⁻⁸ × 255³ ≈ **3.8 W/m² per K**.
- Warming needed: 3.7 / 3.8 ≈ **1 K**, with nothing else changed. (Detailed calculations give about 1.2 K.)

**Feedbacks amplify this.** Warmer air holds about 7% more water vapour per K, and water vapour is a greenhouse gas, so warming adds more absorption. Ice loss and clouds also respond. Water vapour cannot start a warming by itself, because extra water condenses and rains out within days; its amount follows temperature. CO2 stays in the air for centuries, so CO2 sets the level and water vapour amplifies it. Including feedbacks, the warming for doubled CO2 is *estimated* at **2.5 to 4 K** (IPCC AR6 likely range).

## 7. The stratosphere

Above about 12 km, ozone absorbs sunlight and temperature *rises* with height. Satellites observe stratospheric cooling at the same time as surface warming. A brighter Sun would warm both, so this pattern points to greenhouse gases as the cause.

## 8. What the numbers mean

- **238 W/m²** — the energy Earth must shed. It is fixed by sunlight and reflectivity, not by greenhouse gases.
- **3.7 W/m²** — about 1.5% of 238 W/m². A small change in the energy balance, held for decades, is enough to warm the surface by several kelvin.

**Not covered here:** cloud effects in detail, how fast the oceans take up heat (the delay between forcing and warming), and the carbon cycle that sets CO2 levels. A glass greenhouse also works differently: it warms mostly because the glass stops convection, not because of infrared absorption.
