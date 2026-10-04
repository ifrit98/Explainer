# Narrative: sky-blue

> Pass 3. `model.md` says what is true. This file says the path a reader takes to it.
> The prose follows these beats; the diagram shows beats 3 to 6 at once.

## 1. Reader before and after

- **Before:** A technical reader. They know that light is an electromagnetic wave with a wavelength, that visible light runs from about 400 nm (violet) to 700 nm (red), that white light is a mix of all visible wavelengths, that molecules contain electrons, and school mechanics (force, acceleration, oscillation). They do not know how light scatters.
- **After:** "Air molecules scatter blue light about six times more than red, because the electrons they shake radiate with the square of their acceleration; the sky is that scattered light, and a low Sun is what is left after a long path has lost its blue."

## 2. Question and motive

- **Question:** why is the daytime sky blue, and why is the setting Sun red? The answer in words first: the sky is sunlight that air molecules have scattered toward you, and molecules scatter blue far more than red.
- **Why care:** both colors come from one mechanism, and the same mechanism says why clouds are white and why the sky on the Moon is black.
- **Why this approach:** a molecule can only send light toward you if something in it moves. So ask what light does to the electrons in a molecule, and what a moving electron sends out.

## 3. Introduction ledger

| Reference | Means | Grounded by (a concrete instance) | Beat |
|---|---|---|---|
| scattering | a molecule takes light out of the beam and sends it out in other directions | sky light reaching you from a part of the sky away from the Sun | 1 |
| beam / sky light | light straight from the Sun / scattered light from other directions | looking at the Sun vs. looking away from it | 1 |
| ω | the light's angular frequency; ω = 2πc / λ, so a shorter wavelength means a larger ω | blue's ω is 1.56 times red's | 3 |
| scattered power | the power one molecule sends out of the beam | blue 5.86 times red | 3 |
| air mass | path length through air, relative to the Sun overhead | 1 overhead, 38 at the horizon | 5 |

## 4. Beats

| # | Kind | Reader's question | Bridge | Shown | Said | Reader now knows |
|---|---|---|---|---|---|---|
| 1 | answer | Why is the sky blue and the low Sun red? | — | — | The sky is sunlight scattered toward you by air molecules. Molecules scatter blue 5.86 times more than red. A low Sun has lost its blue on a long path through the air. | the answer, in words |
| 2 | approach | How does a molecule send light sideways? | so | — | The light's electric field pushes the electrons back and forth at the light's frequency. A molecule is 1,500 times smaller than the wavelength, so its electrons move together. | the driven electron |
| 3 | mechanism | Why more for blue? | but why | the chain in the diagram | The electrons move about as far for every color. But acceleration is ω² times that distance, and a moving charge radiates power ∝ acceleration². So scattered power ∝ ω⁴ ∝ 1/λ⁴. Blue's ω is 1.56 times red's: 2.42 times the acceleration, 5.86 times the power. | 1/λ⁴, from first principles |
| 4 | objection | Isn't it the amplitude that matters? | but | — | If power followed the amplitude, blue would scatter only 1.06 times more than red, and the sky would be nearly white. | why acceleration |
| 5 | consequence | So what color is the sky and the low Sun? | therefore | two paths: overhead and horizon | Away from the Sun you see only scattered light, mostly blue. Overhead the beam keeps 80% of its blue. At the horizon the path is 38 times longer: 0.02% of the blue gets through, 25% of the red. | sky and sunset from one cause |
| 6 | limit | Does every particle do this? | but | droplet vs molecule | Only particles much smaller than the wavelength. A cloud droplet, 10 µm, is 22 times larger than 450 nm; it scatters every color about equally, so clouds are white. | the assumption |
| 7 | confusion | Why not violet? Isn't blue absorbed? | — | — | Violet scatters 1.60 times more than blue, but sunlight has less violet, and the eye sees the scattered mix as pale blue. Air does not absorb the blue; on the Moon, with no air, the sky is black. | two misconceptions removed |

## 5. Concrete to symbol

- 1/λ⁴ comes after the chain in words, and is checked at once with 450 and 700 nm: 5.86.

## 6. Links between representations

- The diagram's chain uses the same names as the prose: beam, sky light, scattered power, air mass.

## 7. Close the loop

- **Answer:** the first paragraph, and the last sentence: the sky is scattered sunlight, the low Sun is what the scattering leaves.
- **General argument:** power ∝ acceleration², acceleration ∝ ω², valid when the scatterer is much smaller than λ.
- **Payoff:** white clouds and the black Moon sky from the same rule. Scope: polarization, Mie theory, color science.
