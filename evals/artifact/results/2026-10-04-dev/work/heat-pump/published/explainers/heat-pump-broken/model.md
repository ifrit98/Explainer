# Semantic model: heat pump (broken-copy test; the model is correct, the rendering is not)

## Audience and prior knowledge

A technical reader: school mathematics and science, basic programming. New to heat pumps.

## Key facts

- Energy balance: 3 kWh heat delivered = 1 kWh electricity + 2 kWh outdoor heat. COP = 3; electric heater COP = 1.
- Loop: evaporator (refrigerant boils at −10 °C, 3.5 bar, colder than 0 °C air, takes 2 kWh); compressor (1 kWh, raises to 14 bar); condenser (condenses at 40 °C, hotter than 35 °C water, gives 3 kWh); expansion valve (drops pressure, refrigerant cools to −10 °C). Boiling temperature rises with pressure.
- Temperature lift = home water − outdoor air. Larger lift → lower COP: 10 °C outside, lift 25 K, COP about 4; 0 °C, 35 K, about 3; −15 °C, 50 K, about 2.
- Ideal limit T_hot / (T_hot − T_cold) in kelvin: 8.8 at 0 °C → 35 °C.

## Epistemic status

- Established: energy conservation, heat flows hot to cold, boiling point rises with pressure.
- Assumed: 0 °C outside, 35 °C water.
- Estimated: typical real COPs; propane pressures.
