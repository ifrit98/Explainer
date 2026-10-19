# Narrative: heat-pump

> Pass 3. `model.md` says what is true. This file says the path a first-time reader takes to it.

## 1. Reader before and after

- **Before:** a technical reader who knows energy conservation, kelvin, pressure, boiling and condensing, and that heat flows from hot to cold by itself. New to heat pumps, refrigerant loops, COP, and entropy.
- **After:** "A heat pump does not make heat, it moves it: 1 kWh of electricity carries 2 kWh of heat from the cold outdoor air into the home, so 3 kWh arrives. It does this by changing the refrigerant's pressure, which changes its boiling temperature, and the colder it is outside the more electricity each kWh costs."

## 2. Question and motive

- **Question:** How can a heat pump give 3 kWh of heat for 1 kWh of electricity, when energy cannot be created? Result in words: it does not create the 2 extra kWh; it moves them from the outdoor air into the home, and the electricity pays for the move.
- **Why care:** an electric heater gives 1 kWh of heat for 1 kWh. A ratio of 3 sounds like it breaks conservation of energy, so the answer must be about where the energy comes from.
- **Why this approach:** first balance the energy (it shows where the extra comes from), then ask how heat can flow from cold air to warm water (that question leads to the loop), then ask how much the move must cost (that leads to the ideal limit).

## 3. Introduction ledger

| Reference | Means | Grounded by (a concrete instance) | Beat |
|---|---|---|---|
| COP | heat delivered ÷ electricity used | heater 1 / 1 = 1; heat pump 3 / 1 = 3 | 1 |
| outdoor heat | heat taken from the outdoor air | 2 kWh from 0 °C air | 2 |
| refrigerant | fluid in the closed loop | propane | 4 |
| evaporator, compressor, condenser, expansion valve | the four parts of the loop | each with its temperature and pressure in the diagram | 5 |
| bar | pressure; the air around us is 1 bar | 3.5 bar and 14 bar | 4 |
| temperature lift | home water minus outdoor air | 35 − 0 = 35 K | 7 |
| ideal limit (Carnot) | highest COP physics allows for two temperatures | 308.15 / 35 = 8.8 | 8 |
| entropy | heat Q at kelvin temperature T carries Q/T; never destroyed | 2 / 273.15 = 0.00732 kWh/K | 9 |
| Q_hot, Q_cold, W | heat delivered, outdoor heat, electricity | 3, 2, 1 kWh | 9 |
| refrigerant lift | condensing minus boiling temperature | 40 − (−10) = 50 K | 10 |
| diagram colours | blue = cold side, red = hot side, yellow = electricity | the loop diagram | 5 |

## 4. Beats

| # | Kind | Reader's question | Bridge | Shown | Said | Reader now knows |
|---|---|---|---|---|---|---|
| 1 | hook | How can 1 kWh give 3 kWh? | — | heater vs heat pump numbers | "An electric heater turns 1 kWh of electricity into 1 kWh of heat. A heat pump gives about 3 kWh of heat for the same 1 kWh. Energy cannot be created, so where do the other 2 kWh come from? COP (heat delivered ÷ electricity used) is 1 for the heater and 3 for the heat pump." Answer up front: it moves heat, it does not make it. | the puzzle, the answer in one line, the word COP |
| 2 | notice | Is energy created? | so | L1 energy diagram: 1 + 2 = 3; caption explains colours (blue cold side, red hot side, yellow electricity) | "No. 2 kWh is outdoor heat, taken from the outdoor air. 0 °C air is 273 K above absolute zero and still holds heat. The 3 kWh goes into the home water: the 35 °C water that flows through the floor pipes or radiators." | the heat is moved, not made; the home water |
| 3 | objection | Heat flows only from hot to cold. How can it go from 0 °C air into 35 °C water? | but | — | "To carry heat from outside to inside, pipe a fluid between the two. With no other step, the fluid warms to at most 0 °C outside. Inside, the 35 °C water is hotter, so heat flows from the water into the fluid: the home gets colder. The fluid must be colder than the air outside and hotter than the water inside." | the problem the machine must solve |
| 4 | approach | How can one fluid be both? | therefore | — | "Change its pressure. Propane, the fluid used here, boils at −10 °C at 3.5 bar and at 40 °C at 14 bar (the air around us is 1 bar). We call this fluid the refrigerant." | the loop runs at two pressures |
| 5 | mechanism | How does the loop use this? | so | L2 loop diagram, same colours and the same kWh as L1 | the four parts in order: "Evaporator (outdoor coil): refrigerant at 3.5 bar boils at −10 °C, colder than the 0 °C air, so 2 kWh flows in. Compressor: an electric pump squeezes the vapour to 14 bar; the work heats it to about 60 °C, as a bicycle pump gets warm. Condenser (indoor coil): the vapour condenses at 40 °C, hotter than the 35 °C water, so 3 kWh flows out. Expansion valve: a narrow opening drops the pressure to 3.5 bar; about a third of the liquid boils at once, and that boiling cools the rest to −10 °C." | the full loop; the compressor raises the pressure, the valve lowers it |
| 6 | notice | Where does the electricity go? | and | same diagram, compressor | "The compressor's 1 kWh heats the vapour, so it reaches the water too: 1 + 2 = 3 kWh at the condenser." | 3 = 1 + 2 at the condenser |
| 7 | test (predict) | What happens on a colder day? | so | predict prompt: "Outside drops from 10 °C to −15 °C. Does the COP rise, fall, or stay the same?" Then the table. | "The temperature lift is home water minus outdoor air: 35 K at 0 °C. COP is about 4 at 10 °C (lift 25 K), about 3 at 0 °C, about 2 at −15 °C (lift 50 K). Old radiators need 55 °C water: lift 55 K at 0 °C, COP about 2.2." | larger lift → lower COP; why comes next |
| 8 | approach | Why does a larger lift cost more? Is there a limit? | so | formula with the instance first | "Physics sets an ideal limit (the Carnot limit): 308.15 / 35 = 8.8 for 35 °C water and 0 °C air. In symbols, ideal COP = T_hot / (T_hot − T_cold), where T_hot is the home water (308.15 K) and T_cold the outdoor air (273.15 K). Use kelvin: in Celsius 35 / (35 − 0) = 1, which would say a heat pump can never beat a heater. A larger lift makes the bottom bigger, so the limit falls." | the limit, its numbers, why kelvin |
| 9 | mechanism | Why that formula? | because | L3: rule, two cases, steps | "Heat Q that passes at kelvin temperature T carries entropy Q/T. Heat flowing by itself from hot to cold makes entropy: 1 kWh from 308.15 K to 273.15 K loses 1/308.15 and gains 1/273.15, net +0.00042 kWh/K. Nothing can destroy entropy; that is the same law that stops heat flowing from cold to hot by itself. The loop ends each cycle where it started, so it cannot store entropy. So the water must get at least as much entropy as the air loses. Name Q_hot = heat delivered, Q_cold = outdoor heat, W = electricity. COP 3: air loses 2/273.15 = 0.00732, water gets 3/308.15 = 0.00974. Allowed. COP 12 (11 kWh from air): air loses 0.0403, water gets 0.0389. Forbidden. Put Q_cold = Q_hot − W into Q_hot/T_hot ≥ Q_cold/T_cold and solve for Q_hot/W, step by step: you get the limit." | where the limit comes from |
| 10 | notice | Why is a real one 3, not 8.8? | but | — | "Heat flows through a coil only across a temperature gap. So the refrigerant boils 10 K below the air and condenses 5 K above the water. Its own lift, the refrigerant lift, is 40 − (−10) = 50 K, and 313.15 / 50 = 6.3. The compressor, fans, and pumps lose about half of the rest." | the gap's two causes |
| 11 | close | — | so | — | "A heat pump does not make 3 kWh from 1 kWh. It moves 2 kWh of outdoor heat into the home, and the 1 kWh of electricity pays for the move and ends up as heat too. Pressure sets the boiling temperature, so the refrigerant is colder than the air outside and hotter than the water inside, and heat flows the normal way at both ends. The colder the day, the more each kWh costs." Connection: a fridge is the same loop, with the cold coil inside the fridge. Not covered here: a short list. | the after-sentence |

## 5. Concrete to symbol

COP: 3 kWh / 1 kWh = 3, then the word. Ideal limit: 308.15 / 35 = 8.8 first, then T_hot / (T_hot − T_cold), with "here T_hot is 308.15 K, the 35 °C water". Entropy: 2 kWh at 273.15 K → 0.00732 kWh/K, then Q/T.

## 6. Links between representations

The kWh numbers in the L1 diagram are the same numbers on the evaporator, compressor, and condenser in the L2 diagram. Blue nodes are the cold side, red the hot side, yellow the electricity, in both diagrams; the text says so under the first.

## 7. Close the loop

- **Answer:** the heat pump does not make 3 kWh from 1 kWh. It moves 2 kWh of outdoor heat into the home, and the 1 kWh of electricity both pays for the move and ends up as heat.
- **General argument:** changing the pressure changes the boiling temperature, so the refrigerant is colder than the air outside and hotter than the water inside; heat flows the normal way at both ends. The cost per kWh grows with the temperature lift.
- **Payoff:** the reader can predict the COP falls in cold weather and with hot radiators. Connection: a fridge is the same loop. Scope list.
