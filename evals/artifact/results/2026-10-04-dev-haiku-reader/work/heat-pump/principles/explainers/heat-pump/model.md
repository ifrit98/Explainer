# Model: heat pump COP

## Central question
How can a heat pump deliver 3 kWh of heat for 1 kWh of electricity without breaking energy conservation?

## Answer in one line
The electricity does not make the heat. It moves heat from cold outdoor air into the house. Heat delivered = heat taken from outside + electrical work: 3 = 2 + 1.

## Reader
Technical, school physics and maths, new to thermodynamics of heat pumps. Knows energy conservation, kelvin, that boiling absorbs heat. Probably does not know entropy or the pressure dependence of boiling point in a usable way.

## Entities
- Refrigerant: working fluid in a closed loop.
- Evaporator (outdoor coil), compressor, condenser (indoor coil), expansion valve.
- Outdoor air (heat source), house water/air (heat sink).
- W: electrical work. Q_C: heat taken from outside. Q_H: heat delivered inside.
- COP = Q_H / W.

## Causal chain
1. Heat flows only from hot to cold unaided (second law).
2. Boiling point of a fluid rises with pressure (propane: ~ -5 C at ~4 bar, ~45 C at ~15 bar).
3. At low pressure the refrigerant boils at -5 C, colder than 5 C outdoor air: heat flows in.
4. Compressor raises pressure, so the vapour can condense at 45 C, hotter than 35 C heating water: heat flows out.
5. Expansion valve drops pressure back; loop repeats.
6. Energy balance: Q_H = Q_C + W.

## Why this form (limit)
Entropy: heat Q at temperature T carries entropy Q/T; total cannot decrease. So Q_H/T_H >= Q_C/T_C, giving COP <= T_H/(T_H - T_C) (kelvin). Work grows with temperature lift.

## Cases (numbers)
- Simplest alternative: resistance heater, COP = 1.
- Mild: refrigerant -5 C -> 45 C, ideal 318/50 = 6.4, real ~ 47% -> ~3.0.
- Cold: refrigerant -25 C -> 45 C, ideal 318/70 = 4.5, real ~2.1.

## Epistemic status
- Energy balance, second law, Carnot bound: established.
- 47% of ideal, specific pressures: estimates / typical values.

## Confusion points
- "Over 100% efficient" sounds like free energy. It is not; the outside air supplies the extra.
- Cold air still holds heat; it just needs something colder than it to give heat to.
- Refrigerant temperatures, not room/air temperatures, set the real lift.

## Scope (left out)
Defrost cycles, ground-source units, refrigerant choice, cost and CO2 comparison.
