# How a heat pump delivers three times more heat than the electricity it uses

**Short answer:** the electricity does not *make* the heat. It *moves* heat from the cold outdoor air into the house. The heat that comes out is the heat taken from outside plus the electricity:

```
heat delivered  =  heat taken from outside  +  electrical work
    3 kWh       =          2 kWh            +      1 kWh
```

Energy is conserved. Two of the three kWh were already in the outdoor air.

## Why this matters

An electric resistance heater turns 1 kWh of electricity into exactly 1 kWh of heat. It can do no better, because it can only convert the energy it is given. A heat pump also collects energy from outside, so it can deliver more heat than the electricity it uses. The ratio is the **coefficient of performance (COP)**:

```
COP = heat delivered / electrical work = 3 kWh / 1 kWh = 3
```

A COP of 1 is no better than a resistance heater. A COP of 3 means two thirds of the heat came from outside.

## The obstacle: heat flows downhill

Air at 5 °C still holds a lot of thermal energy. It is 278 K, far above absolute zero. But heat flows by itself only from a hotter body to a colder one (the second law of thermodynamics). The 5 °C air cannot warm a 20 °C room. So the machine must do two things:

1. Get colder than the outdoor air, so heat flows *in*.
2. Get hotter than the house, so heat flows *out*.

The same fluid does both, by changing its pressure.

## The trick: boiling point depends on pressure

A liquid boils at a lower temperature when the pressure is lower. Water boils below 100 °C on a mountain for this reason. A heat pump uses a fluid called a **refrigerant**, for example propane, in a closed loop. Propane boils at about −5 °C at 4 bar, and at about 45 °C at 15 bar (approximate values).

```
   OUTSIDE (air 5 °C)                              INSIDE (heating water 35 °C)

 ┌───────────────────────────┐   vapour     ┌────────────────────────────┐
 │ EVAPORATOR  ~4 bar        │              │ CONDENSER  ~15 bar         │
 │ boils at −5 °C            ├─►COMPRESSOR─►│ condenses at 45 °C         │
 │ heat flows IN  (2 kWh)    │  (1 kWh      │ heat flows OUT (3 kWh)     │
 │ air 5 °C → fluid −5 °C    │  electric)   │ fluid 45 °C → water 35 °C  │
 └───────────────────────────┘              └────────────────────────────┘
               ▲                                          │
               │                 liquid                   │
               └──────────── EXPANSION VALVE ◄────────────┘
                     15 bar → 4 bar, fluid cools to −5 °C
```

Follow one kilogram of refrigerant around the loop:

1. **Evaporator (outside).** The liquid is at 4 bar, so it boils at −5 °C. The outdoor air is 5 °C, which is hotter, so heat flows into the fluid. Boiling absorbs this heat as the liquid turns to vapour.
2. **Compressor.** An electric motor squeezes the vapour to 15 bar. This is the only place the electricity enters the loop. The work of compression also heats the vapour.
3. **Condenser (inside).** At 15 bar the fluid condenses at 45 °C. The heating water is 35 °C, which is colder, so heat flows out of the fluid. The fluid releases the heat it picked up outside *and* the compressor work.
4. **Expansion valve.** A narrow opening drops the pressure back to 4 bar. Part of the liquid flashes to vapour, which cools the rest to −5 °C. The loop starts again.

A refrigerator is the same machine. It takes heat from the food box and dumps it into the kitchen through the coil at the back.

## Why the COP is not unlimited

Moving heat from cold to hot costs work, and the cost grows with the **temperature lift**: the gap between the temperature where the fluid condenses and where it boils.

The second law sets the limit. Heat *Q* leaving or entering a body at absolute temperature *T* carries an amount of entropy *Q/T*, and total entropy cannot decrease (established fact). So the entropy dumped inside must be at least the entropy taken from outside:

```
Q_H / T_H  ≥  Q_C / T_C        and  W = Q_H − Q_C
⇒  COP = Q_H / W  ≤  T_H / (T_H − T_C)        (temperatures in kelvin)
```

The bound has lift in the denominator. A small lift gives a high possible COP; a large lift gives a low one.

| Case | Fluid boils | Fluid condenses | Lift | Ideal COP | Typical real COP (estimate, ~47% of ideal) |
|---|---|---|---|---|---|
| Mild day, air 5 °C | −5 °C (268 K) | 45 °C (318 K) | 50 K | 318/50 = 6.4 | ~3.0 |
| Cold day, air −15 °C | −25 °C (248 K) | 45 °C (318 K) | 70 K | 318/70 = 4.5 | ~2.1 |

Note that the lift the machine must do is larger than the gap between the air and the heating water. The fluid must be about 10 K colder than the air and about 10 K hotter than the water, so heat flows at a useful rate in both coils. Real machines also lose energy to friction, motor heat, and imperfect compression. That is why they reach only about half the ideal value.

**Predict:** what happens to the COP if the house uses underfloor heating, so the fluid only needs to condense at 35 °C instead of 45 °C? *(The lift falls to 40 K, the ideal COP rises to 308/40 = 7.7, and the real COP rises to about 3.6. This is why heat pumps work best with large, low-temperature radiators or floors.)*

## Summary

- A heat pump moves heat; it does not create it. Heat out = heat from outside + electricity.
- It moves heat "uphill" by changing the refrigerant's pressure, so the same fluid boils below outdoor temperature and condenses above indoor temperature.
- The work needed grows with the temperature lift. A mild day gives COP ≈ 3; a very cold day gives COP ≈ 2. Both beat a resistance heater's COP of 1.

*Not covered:* defrost cycles, ground-source heat pumps, refrigerant choice, and cost or CO₂ comparisons.
