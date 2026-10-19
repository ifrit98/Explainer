# Semantic model: heat pump

> Source of truth. Every rendering (prose, diagram, page, video) derives from this file.
> If a rendering needs a new fact, add it here first.

## Central question

How can a heat pump deliver three times more heat than the electricity it uses?

## Audience and prior knowledge

A technical reader: school mathematics and science (energy conservation, temperature in kelvin, boiling point depends on pressure), basic programming. New to heat pumps and refrigeration. Does not know: the refrigerant cycle, COP, the Carnot limit.

## Entities

| Entity | Definition (one sentence) | Status |
|---|---|---|
| heat pump | A machine that uses electricity to move heat from a cold place (outdoor air) to a warm place (the house). | fact |
| electricity | The work input; it drives the compressor. | fact |
| outdoor air | The cold source; air at 0 °C still contains thermal energy that can be extracted. | fact |
| refrigerant | A fluid that boils at a low temperature and circulates in a closed loop; it carries the heat. | fact |
| evaporator | Outdoor heat exchanger; refrigerant boils there, colder than the air, and absorbs heat. | fact |
| compressor | Squeezes the refrigerant gas to a high pressure, which raises its temperature; uses the electricity. | fact |
| condenser | Indoor heat exchanger; hot refrigerant condenses there, hotter than the house water, and releases heat. | fact |
| expansion valve | Drops the refrigerant pressure, which drops its temperature below the outdoor air again. | fact |
| COP | Coefficient of performance: heat delivered ÷ electricity used. | definition |
| temperature lift | Condenser temperature minus evaporator temperature. | definition |

## Relationships

| From | Relationship (verb) | To | Notes |
|---|---|---|---|
| outdoor air | gives heat to | evaporator | because the refrigerant there is colder (−10 °C vs 0 °C) |
| electricity | drives | compressor | the only paid energy input |
| compressor | raises pressure and temperature of | refrigerant | 3.5 bar → 14 bar, −10 °C → 40 °C condensing |
| condenser | gives heat to | house | because the refrigerant there is hotter (40 °C vs 35 °C) |
| expansion valve | lowers pressure and temperature of | refrigerant | closes the loop |
| temperature lift | sets the minimum work per unit heat | COP | larger lift → lower COP |

## Causal chain

```text
refrigerant boils colder than outdoor air → heat flows in (2 kWh)
→ compressor (1 kWh electricity) makes it hotter than the house
→ heat flows out (2 + 1 = 3 kWh) → valve makes it cold again → repeat
```

## Quantities

- Energy balance (conservation): Q_out = Q_in + W. Worked: 3 kWh = 2 kWh + 1 kWh.
- COP = Q_out / W = 3 / 1 = 3.
- Electric resistance heater: COP = 1 (1 kWh → 1 kWh).
- Carnot limit (ideal machine): COP_max = T_hot / (T_hot − T_cold), temperatures in kelvin.
  - Typical day: evaporator −10 °C (263 K), condenser 40 °C (313 K), lift 50 K → COP_max = 313/50 ≈ 6.3. Real ≈ 3.
  - Mild day: outdoor 10 °C, evaporator 0 °C (273 K), lift 40 K → COP_max ≈ 7.8. Real ≈ 4.
  - Cold day: outdoor −15 °C, evaporator −25 °C (248 K), lift 65 K → COP_max ≈ 4.8. Real ≈ 2.
- Refrigerant R290 (propane): boils at about −10 °C at 3.5 bar and condenses at about 40 °C at 14 bar.

## Alternative states

| State / scenario | What changes | Why |
|---|---|---|
| Mild day (10 °C) | COP ≈ 4 | smaller lift, less work per kWh moved |
| Cold day (−15 °C) | COP ≈ 2 | larger lift, more work per kWh moved |
| Resistance heater | COP = 1 | converts electricity to heat; moves none |

## Why this form

| Operation | Simplest alternative | What the alternative breaks (with numbers) |
|---|---|---|
| Move heat instead of making it | Turn electricity into heat (resistance heater) | 1 kWh in → 1 kWh out, COP 1, never more: conservation of energy caps it. |
| Compress the refrigerant | Just pump the refrigerant round without compressing | Refrigerant at −10 °C cannot heat 35 °C water; heat flows only hot → cold. |
| Use the valve to drop pressure | Keep the refrigerant at high pressure | At 40 °C it is hotter than 0 °C air, so it gives heat to the outdoors instead of taking it. |

## Concrete cases

| Claim | Holds here (numbers) | Breaks here, without its assumption (numbers) |
|---|---|---|
| COP > 1 does not break energy conservation | 2 kWh from air + 1 kWh electricity = 3 kWh out | If you count only electricity as input, 3 out of 1 looks like 300% "efficiency" — the 2 kWh from the air is omitted. |
| COP falls as lift grows | lift 40 K → ≈ 4; 50 K → ≈ 3 | lift 65 K (−15 °C day) → ≈ 2 |

## Terms

- **heat pump**: moves heat from cold outdoor air to the warm house using electricity.
- **refrigerant**: the circulating fluid that carries heat.
- **evaporator / condenser**: where the refrigerant takes in / gives out heat.
- **compressor**: raises refrigerant pressure and temperature; the electricity goes here.
- **COP**: heat delivered ÷ electricity used. 1 = no better than a resistance heater; 3 = typical; 5 = mild weather, low lift.
- **temperature lift**: how far the heat is lifted in temperature. 40 K = easy; 65 K = hard.

## Epistemic status

- **Observed / established:** energy conservation; heat flows only hot → cold spontaneously; boiling point rises with pressure.
- **Mathematical consequence:** Q_out = Q_in + W; Carnot limit formula.
- **Assumed:** the example temperatures (0 °C outdoor, 35 °C water, 5–10 K differences at the heat exchangers).
- **Estimated / model output:** real COPs (≈ 2, 3, 4) — rule of thumb: real machines reach about half the Carnot limit.

## Confusion points

- "COP 3 means 300% efficient, which is impossible" → the machine does not create energy; 2 of the 3 kWh come from outdoor air.
- "0 °C air has no heat in it" → 0 °C is 273 K; the air holds a lot of thermal energy. Only a colder refrigerant is needed to pull it out.
- "The compressor's heat is the output" → compressor work is only 1 of the 3 kWh.

## Scope

- **Out of scope:** defrost cycles, ground-source vs air-source, refrigerant choice and safety, sizing — see any HVAC design guide.
- **Out of scope:** derivation of the Carnot limit — see entropy and the second law in a thermodynamics text.

## Representation decision

- **Stage:** 2
- **Reason:** the mechanism is a closed loop of four components with energy flows in and out; the reader must hold the loop, the temperatures at each point, and the energy balance at once.
- **Levels:** L1 energy balance / L2 the refrigerant loop / L3 why lift sets the limit
