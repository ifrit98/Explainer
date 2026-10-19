# Semantic model: how a heat pump delivers more heat than the electricity it uses

> Source of truth. Every rendering (prose, diagram, page, video) derives from this file.
> If a rendering needs a new fact, add it here first.

## Central question

How can a heat pump put 3 kWh of heat into a home for each 1 kWh of electricity, when energy cannot be created?

## Audience and prior knowledge

A technical reader: school mathematics and science (energy conservation, temperature, kelvin, pressure, boiling and condensing, heat flows from hot to cold), basic programming. New to thermodynamic cycles. Does not know: refrigerant, evaporator, compressor, condenser, expansion valve, COP, entropy, that boiling temperature depends on pressure well enough to use it, the ideal limit (Carnot).

## Entities

| Entity | Definition (one sentence) | Status |
|---|---|---|
| Electric heater | A resistor that converts electricity into heat, 1 kWh in, 1 kWh out. | fact |
| Heat pump | A machine that uses electricity to move heat from a cold place (outdoor air) to a warmer place (home water). | fact |
| Outdoor air | The cold source; at 0 °C (273 K) it still holds thermal energy that can be taken out. | fact |
| Home water | The hot side: water at 35 °C that flows through underfloor pipes or radiators. | assumption (typical) |
| Refrigerant | A fluid in a closed loop that boils and condenses at useful temperatures (for example propane). | fact |
| Evaporator | Outdoor heat exchanger where the cold, low-pressure refrigerant boils and takes heat from the air. | fact |
| Compressor | Electric pump that squeezes the refrigerant vapour to high pressure; the work done on the gas makes it hot (as a bicycle pump gets warm). | fact |
| Condenser | Indoor heat exchanger where the hot, high-pressure refrigerant condenses and gives heat to the home water. | fact |
| Expansion valve | Narrow opening that drops the refrigerant pressure; part of the liquid boils at once, and that boiling cools the rest. | fact |
| COP | Coefficient of performance: heat delivered ÷ electricity used. | definition |
| Temperature lift | Home water temperature minus outdoor air temperature (35 K in the example). | definition |
| Refrigerant lift | Condensing temperature minus boiling temperature of the refrigerant (50 K in the example); larger than the temperature lift because heat exchangers need a temperature gap. | definition |
| Entropy | Bookkeeping quantity: heat Q passing at absolute temperature T carries Q/T of entropy; entropy can be created but never destroyed. | established fact |

## Relationships

| From | Relationship (verb) | To | Notes |
|---|---|---|---|
| Outdoor air | gives heat to | Evaporator | because the refrigerant there (−10 °C) is colder than the air (0 °C) |
| Evaporator | sends low-pressure vapour to | Compressor | |
| Compressor | sends hot high-pressure vapour to | Condenser | electricity enters here |
| Condenser | gives heat to | Home water | because the refrigerant there (40 °C) is hotter than the water (35 °C) |
| Condenser | sends high-pressure liquid to | Expansion valve | |
| Expansion valve | sends a cold low-pressure mix of liquid and vapour to | Evaporator | |
| Temperature lift | sets the minimum electricity per kWh of heat | COP | larger lift → lower COP |

## Dependencies (learning order)

1. Energy conservation: heat delivered = electricity + outdoor heat.
2. Heat flows only from hot to cold by itself.
3. Boiling temperature rises with pressure.
4. The refrigerant loop uses (3) to make the refrigerant colder than outdoor air and hotter than home water, so (2) works for it at both ends.
5. Moving heat from cold to hot costs work; the work grows with the temperature lift.

## Causal chain

```text
Expansion valve drops pressure → refrigerant boils at −10 °C → colder than 0 °C air → heat flows in (2 kWh)
Compressor adds 1 kWh of work → pressure and temperature rise → condenses at 40 °C → hotter than 35 °C water → heat flows out (3 kWh)
```

## Temporal sequence

1. Evaporator: cold refrigerant at about 3.5 bar boils at −10 °C and takes 2 kWh from 0 °C outdoor air.
2. Compressor: uses 1 kWh of electricity to squeeze the vapour from about 3.5 bar to about 14 bar (the air around us is 1 bar). The work ends up as heat in the vapour, which leaves at about 60 °C.
3. Condenser: the vapour cools to 40 °C, condenses at 40 °C, and gives 3 kWh to 35 °C home water.
4. Expansion valve: pressure drops from about 14 bar to about 3.5 bar. At 3.5 bar the 40 °C liquid is far above its −10 °C boiling point, so about a third of it boils at once. That boiling takes heat from the rest of the liquid and cools everything to −10 °C. The valve adds and removes no energy. The loop repeats.

## Quantities

- Symbols, mapped once: Q_hot = heat delivered (3 kWh), Q_cold = outdoor heat (2 kWh), W = electricity (1 kWh).
- Energy balance (0 °C outside, 35 °C water): heat delivered 3 kWh = electricity 1 kWh + outdoor heat 2 kWh.
- COP = heat delivered / electricity = 3 / 1 = 3. Electric heater COP = 1.
- Ideal limit (Carnot): ideal COP = T_hot / (T_hot − T_cold), temperatures in kelvin. At 35 °C (308.15 K) and 0 °C (273.15 K): 308.15 / 35 = 8.8.
- Propane boiling pressures (approximate): −10 °C at about 3.5 bar; 40 °C at about 14 bar.
- Effect of outdoor temperature (water 35 °C):

| Outdoor | Temperature lift | Ideal COP | Typical real COP |
|---|---|---|---|
| 10 °C | 25 K | 12.3 | about 4 |
| 0 °C | 35 K | 8.8 | about 3 |
| −15 °C | 50 K | 6.2 | about 2 |

- Water at 55 °C (old radiators), 0 °C outside: lift 55 K, ideal 328.15 / 55 = 6.0, typical real about 2.2.
- Why real is about a third of ideal: heat flows through a heat exchanger only across a temperature gap, and a bigger gap moves heat faster through a smaller coil. So the refrigerant boils at −10 °C (10 K below the air) and condenses at 40 °C (5 K above the water). Its refrigerant lift is 50 K, not 35 K: ideal 313.15 / 50 = 6.3. The compressor, fans, and pumps lose about half of the rest.
- Very cold weather: at −25 °C outside, lift 60 K, ideal 308.15 / 60 = 5.1, typical real about 1.5 (estimate). Real COP stays above 1 in most winters; many units add a backup electric heater (COP 1) for the coldest days.

## Alternative states

| State / scenario | What changes | Why |
|---|---|---|
| Colder outside | COP falls | larger lift needs more work per kWh moved |
| Hotter water (radiators) | COP falls | larger lift |
| No compressor (just a pump circulating fluid) | no heating | fluid cannot be hotter than the air it came from |

## Why this form

| Operation | Simplest alternative | What the alternative breaks (with numbers) |
|---|---|---|
| Compress the refrigerant (spend work) | Just circulate a fluid between outside and inside | Fluid warmed by 0 °C air reaches at most 0 °C; in a 20 °C home heat flows from home to fluid, so the home loses heat. |
| Change pressure to change boiling temperature | Use a fixed-pressure fluid | At one pressure the fluid boils and condenses at one temperature; it cannot be both below 0 °C outside and above 35 °C inside. |
| Ideal limit uses kelvin | Use Celsius in T_hot / (T_hot − T_cold) | 35 / (35 − 0) = 1, which says a heat pump cannot beat a heater. Kelvin gives 308.15 / 35 = 8.8. |
| COP above 1 | "Energy out cannot exceed energy in" | It does not: 3 kWh out = 1 kWh electricity + 2 kWh outdoor heat. The heater has COP 1 because electricity is its only input. |

## Concrete cases

| Claim | Holds here (numbers) | Breaks here, without its assumption (numbers) |
|---|---|---|
| COP above 1 because heat is moved, not made | 0 °C outside, 35 °C water: 1 kWh in, 2 kWh from air, 3 kWh out | Electric heater makes heat from electricity only: 1 kWh in, 1 kWh out, COP 1 |
| Larger lift → lower COP | 10 °C outside: lift 25 K, COP about 4 | −15 °C outside: lift 50 K, COP about 2 |
| Heat flows in at the evaporator because refrigerant is colder than the air | refrigerant −10 °C, air 0 °C | if the refrigerant were at 5 °C, heat would flow from refrigerant to air |
| No machine beats the ideal limit | COP 3: entropy taken 2 / 273.15 = 0.00732 kWh/K ≤ given 3 / 308.15 = 0.00974 kWh/K | claimed COP 12: taken 11 / 273.15 = 0.0403 > given 12 / 308.15 = 0.0389, so entropy would be destroyed |

## Terms

- **Heat pump**: moves heat from a cold place to a warmer place, using electricity.
- **Refrigerant**: the working fluid in the closed loop.
- **Evaporator / compressor / condenser / expansion valve**: the four parts of the loop, as above.
- **COP**: heat delivered ÷ electricity used. COP 1: no better than a heater. COP 3: three times the heat. COP 8.8: the ideal limit at 0 °C → 35 °C.
- **Outdoor heat**: the heat taken from the air (2 kWh). Not "free energy".
- **Temperature lift**: home water minus outdoor air. 25 K: easy, COP about 4. 50 K: hard, COP about 2.
- **Refrigerant lift**: refrigerant condensing minus boiling temperature; 50 K in the example. Used only to explain why real COP is below ideal.
- **Ideal limit** (ideal COP): the highest COP physics allows for a given pair of temperatures. Not "efficiency"; "Carnot" only at first mention.
- **Entropy**: Q/T for heat Q at kelvin temperature T; never destroyed. Used only in L3.

## Epistemic status

- **Observed / established:** energy conservation; heat flows hot to cold; boiling point rises with pressure; entropy is never destroyed; the Carnot limit.
- **Mathematical consequence:** COP = 1 + outdoor heat / electricity; ideal-limit values.
- **Assumed:** 0 °C outside, 35 °C water, refrigerant at −10 °C and 40 °C.
- **Estimated:** typical real COPs (about 4, 3, 2, 2.2, 1.5); propane pressures (about 3.5 and 14 bar); vapour at about 60 °C after the compressor; about a third of the liquid boils in the valve.

## Confusion points

- "COP 3 breaks energy conservation" → 3 kWh out = 1 kWh electricity + 2 kWh outdoor heat.
- "0 °C air has no heat to give" → 0 °C is 273 K; air holds thermal energy far above absolute zero; it gives heat to anything colder, such as −10 °C refrigerant.
- "The COP is a fixed property of the machine" → it depends on the temperature lift; the same unit gives about 4 at 10 °C and about 2 at −15 °C.
- "The compressor's electricity is lost" → the compressor's work also ends up as heat in the home; it is part of the 3 kWh.

## Why the ideal limit has this form (L3)

Heat Q passing at absolute temperature T carries entropy Q/T. Entropy can be created but never destroyed; heat flowing by itself from hot to cold creates it (1 kWh from 308.15 K to 273.15 K: −1/308.15 + 1/273.15 = +0.00042 kWh/K). The loop returns to its start each cycle, so it cannot store entropy, and electricity (work) carries no entropy. So the entropy given to the home water must be at least the entropy taken from the air: Q_hot / T_hot ≥ Q_cold / T_cold.

- Holds: COP 3. Taken: 2 / 273.15 = 0.00732 kWh/K. Given: 3 / 308.15 = 0.00974 kWh/K. 0.00974 ≥ 0.00732.
- Breaks: a claimed COP 12 (1 kWh electricity, 11 kWh from air, 12 kWh out). Taken: 11 / 273.15 = 0.0403. Given: 12 / 308.15 = 0.0389. Entropy would be destroyed, so no machine can do it.
- Algebra: put Q_cold = Q_hot − W into the inequality: Q_hot / T_hot ≥ (Q_hot − W) / T_cold, so W ≥ Q_hot × (T_hot − T_cold) / T_hot, so COP = Q_hot / W ≤ T_hot / (T_hot − T_cold) = 308.15 / 35 = 8.8.
- Meaning: the minimum electricity for 3 kWh is 3 × 35 / 308.15 = 0.34 kWh. The real machine uses 1 kWh.

## Scope

- **Out of scope:** ground-source and water-source heat pumps — same cycle, warmer and steadier cold side, so higher COP.
- **Out of scope:** defrost cycles below about 5 °C, where frost on the evaporator is melted.
- **Out of scope:** cost and CO₂ comparisons with gas boilers — depend on electricity and gas prices and the grid mix.
- **Out of scope:** seasonal COP (SCOP) — the average COP over a heating season.
- **Out of scope:** refrigerant choice and safety — propane, R32, CO₂.
- **Out of scope:** why a boiling fluid and not a warmed gas — boiling takes much heat at one fixed temperature, so the coils can be small.
- **Connection:** a fridge and an air conditioner use the same loop, with the cold side inside.

## Representation decision

- **Stage:** 2
- **Reason:** the mechanism is a closed loop of four parts with two heat exchanges; the reader must hold the loop, the temperature at each point, and the energy balance at once. A diagram shows the loop; a table shows how the lift changes the COP.
- **Levels:** L1 energy balance (where the 3 kWh comes from) / L2 the refrigerant loop / L3 why moving heat from cold to hot costs work, and how much / Scope.
