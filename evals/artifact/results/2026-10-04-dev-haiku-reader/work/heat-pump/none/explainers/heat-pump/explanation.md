# How can a heat pump deliver three times more heat than the electricity it uses?

## The short answer

A heat pump doesn't turn electricity into heat. It uses electricity to **move** heat that already exists, taking it from somewhere cold (the outside air, the ground) and releasing it somewhere warm (your house).

So in a typical hour:

```
  1 kWh of electricity   (drives the machine)
+ 2 kWh of heat          (taken from the outside air, for free)
= 3 kWh of heat          (released into the house)
```

Energy is conserved exactly. Nothing is created. The "3×" compares the heat delivered with only the part you pay for. That ratio is called the **coefficient of performance (COP)**:

```
COP = heat delivered / electrical work put in = 3 kWh / 1 kWh = 3
```

The rest of this explanation answers the three questions that usually come next:

1. How can cold outside air contain heat you can extract?
2. How does the machine actually move heat "uphill", from cold to warm?
3. Why is the answer about 3, and not 1 or 100?

---

## 1. Cold air still holds plenty of heat

"Cold" only means "colder than us". Air at 0 °C is at 273 K, which is 273 degrees above absolute zero, where molecular motion stops. Its molecules are still moving fast and carry a lot of thermal energy. Cooling 1 kg of air from 0 °C to −5 °C releases about 5 kJ. A heat pump blows thousands of kilograms of air across its outdoor coil every hour, so it can collect kilowatts of heat from air that feels freezing.

There's one catch. Heat flows on its own only from hot to cold. The outside air will never warm a 20 °C room by itself. Something has to push the heat the "wrong" way. That push is what the electricity pays for.

A useful analogy is a water pump. Lifting water from a low tank into a high tank takes energy, but the energy depends on **how high** you lift it, not on how much water was in the low tank to begin with. The water was already there. A heat pump lifts heat across a temperature difference, and the work needed depends on the size of that difference.

---

## 2. How the machine moves heat uphill

The trick uses one fact about liquids: **the boiling point depends on pressure.** Water boils at 100 °C at sea level, at about 70 °C on top of Everest, and at 120 °C inside a pressure cooker. Lower the pressure and a liquid boils at a lower temperature. Raise it and the liquid condenses at a higher temperature.

A heat pump circulates a **refrigerant**, a fluid chosen so that its boiling point at sensible pressures falls in a useful range. (Propane, sold as R290, is a common one.) The refrigerant goes round a closed loop with four parts:

```
          OUTSIDE (cold, e.g. 0 °C)                 INSIDE (warm, e.g. 35 °C water for radiators)

        ┌──────────────────────┐                   ┌──────────────────────┐
        │  1. EVAPORATOR       │   cold, low-      │  3. CONDENSER        │
 heat → │  low pressure;       │   pressure gas    │  high pressure;      │ → heat
 from   │  refrigerant boils   │ ───────────────┐  │  refrigerant         │   into
 air    │  at about −8 °C      │                │  │  condenses at ~40 °C │   house
        └──────────────────────┘                │  └──────────────────────┘
                   ▲                            ▼             │
                   │                   ┌─────────────────┐    │ warm, high-
     cold, low-    │                   │ 2. COMPRESSOR   │    │ pressure
     pressure      │                   │ (electricity    │────┘ liquid
     liquid        │                   │  goes in here)  │  hot, high-pressure gas
                   │                   └─────────────────┘
        ┌──────────────────────┐                                  │
        │ 4. EXPANSION VALVE   │ ◄────────────────────────────────┘
        │ pressure drops,      │
        │ liquid gets very cold│
        └──────────────────────┘
```

Follow one bit of refrigerant round the loop:

1. **Evaporator (outdoors).** The refrigerant is at low pressure, so it boils at about −8 °C. That's colder than the 0 °C outside air, so heat flows naturally *from the air into the refrigerant*, and the refrigerant boils. Boiling soaks up a lot of energy (latent heat) without the temperature changing. **This is where the free heat enters.**
2. **Compressor.** An electric motor squeezes the gas to high pressure. Compressing a gas heats it, the same way a bicycle pump gets warm. The gas leaves hotter than the house water, say 60 °C. **This is where the electricity enters.**
3. **Condenser (indoors).** At high pressure the refrigerant condenses at about 40 °C. That's warmer than the 35 °C radiator water, so heat flows naturally *from the refrigerant into the water*. Condensing releases all the latent heat picked up outdoors, plus the energy added by the compressor.
4. **Expansion valve.** The warm, high-pressure liquid passes through a narrow restriction. Its pressure drops sharply, part of it flashes to vapour, and it cools to about −8 °C again, ready to go back outdoors.

Notice that **heat only ever flows downhill**: at each heat exchanger, from the hotter thing to the colder thing. The machine cheats by changing the refrigerant's temperature between the two exchangers. It makes the refrigerant colder than the outside air when it needs to absorb heat, then hotter than the house when it needs to release it. The compressor's job is to raise the refrigerant from the cold level to the hot level.

A fridge is exactly this machine. Its evaporator is inside the box and its condenser is the warm grille on the back. A heat pump is a fridge whose "inside" is the outdoors, and whose warm grille is your house.

---

## 3. Why about 3? The temperature lift sets the limit

How much work does it take to lift a given amount of heat from a cold temperature to a hot one? Thermodynamics gives an exact lower bound. Here is the derivation, which needs only some algebra.

**Entropy bookkeeping.** When heat *Q* moves in or out of something at absolute temperature *T*, it carries entropy *Q / T*. The second law of thermodynamics says that the total entropy can't decrease. A machine running in a steady cycle can't store entropy, so it must give out at least as much entropy as it takes in.

- Heat taken from outside, at *T*_cold: *Q*_cold, which brings in entropy *Q*_cold / *T*_cold
- Heat released indoors, at *T*_hot: *Q*_hot, which carries out entropy *Q*_hot / *T*_hot
- Electrical work *W* carries no entropy.

The second law requires:

```
Q_hot / T_hot  ≥  Q_cold / T_cold
```

Energy conservation gives *Q*_cold = *Q*_hot − *W*. Substitute that in and rearrange:

```
W  ≥  Q_hot × (1 − T_cold / T_hot)

COP = Q_hot / W  ≤  T_hot / (T_hot − T_cold)        (the Carnot limit)
```

The maximum COP depends only on the two **absolute** temperatures, and it shrinks as the gap between them grows. The work needed is a fraction of the heat moved, and that fraction is just the temperature lift divided by the hot temperature.

**Plugging in numbers.** Outside is 0 °C (273 K) and radiator water is 35 °C (308 K):

```
COP_max = 308 / (308 − 273) = 308 / 35 ≈ 8.8
```

So the laws of physics would allow almost 9 units of heat per unit of electricity. Real machines lose energy in several ways. The refrigerant has to be several degrees colder than the air and hotter than the water, or heat won't flow fast enough, so the real lift is larger than 35 K. The compressor and motor have friction and electrical losses. The expansion valve wastes some energy. Fans and pumps also use power. Good machines reach roughly 40–50 % of the Carnot limit, which puts them at around **3.5–4**. Averaged over a winter, which includes colder days and defrosting the outdoor coil, a seasonal COP of about **3** is typical.

This also explains the practical advice given about heat pumps:

| Outside | Water temp | Carnot COP | Realistic COP (≈ 45 % of Carnot) |
|---|---|---|---|
| 10 °C | 35 °C | 12.3 | ~5.5 |
| 0 °C | 35 °C | 8.8 | ~4.0 |
| 0 °C | 55 °C | 6.0 | ~2.7 |
| −10 °C | 35 °C | 6.8 | ~3.1 |
| −10 °C | 55 °C | 5.0 | ~2.3 |

- **Colder weather means a lower COP.** The lift is bigger. But it stays above 1, so the heat pump still beats an electric heater.
- **Lower water temperatures help a lot.** That's why heat pumps pair well with large radiators or underfloor heating, which can heat a room with 35 °C water rather than 55 °C.
- **Ground-source heat pumps** draw from soil that stays around 10 °C all winter, so they keep a smaller lift and a higher COP.

If you want to play with the numbers, this snippet reproduces the table:

```python
def carnot_cop(t_out_c, t_water_c):
    t_cold = t_out_c + 273.15
    t_hot = t_water_c + 273.15
    return t_hot / (t_hot - t_cold)

for out, water in [(10, 35), (0, 35), (0, 55), (-10, 35), (-10, 55)]:
    c = carnot_cop(out, water)
    print(f"{out:>4} °C → {water} °C: Carnot {c:5.1f}, realistic ~{0.45 * c:.1f}")
```

---

## Why this isn't too good to be true

- **It's not perpetual motion.** No energy is created. The heat delivered equals the electricity plus the heat removed from outdoors, exactly. The outside air ends up slightly colder.
- **Compare with an electric heater.** A resistive heater converts 1 kWh of electricity into exactly 1 kWh of heat (COP = 1). That is already 100 % efficient as a *converter*, and no converter can do better. A heat pump isn't a better converter. It's a different kind of device, a mover, and movers aren't limited to 1.
- **The "3×" is a ratio, not an efficiency.** Efficiency compares output with *total* energy input, and that's always 100 % here (energy is conserved). COP compares output with the *paid-for* input only. Calling it "300 % efficient" is a loose way of saying COP = 3.
- **Run backwards, it's an air conditioner.** Swap which coil is inside and which is outside (most heat pumps do this with a reversing valve) and the same machine moves heat out of your house in summer.

**In one sentence:** electricity is spent to raise heat across a temperature gap, not to create it. When the gap is small compared with the absolute temperature, a little work moves a lot of heat.
