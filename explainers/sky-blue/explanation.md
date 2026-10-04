# Why is the sky blue, and the setting Sun red?

<!-- Stage 1, rendered from model.md in STE-80. -->

**The sky is sunlight that air molecules scatter toward you, and molecules scatter blue light 5.86 times more than red.** A low Sun is red because its long path through the air scatters the blue out of its beam.

*Scattering* means that a molecule takes light out of the *beam* (the light coming straight from the Sun) and sends it out in other directions.

## How a molecule scatters light

<!-- claim: mechanism-dipole -->
1. The light's electric field pushes the electrons in N₂ and O₂ back and forth at the light's frequency. A molecule is about 0.3 nm across, 1,500 times smaller than a 450 nm wavelength, so all its electrons move together.
2. An electron is held in the molecule like a mass on a spring, with a natural frequency in the ultraviolet. Driven far below that frequency, the spring force dominates and the electron follows the field. So for the same field it moves about the same distance for every color.
3. An accelerating charge radiates. Its radiated field is proportional to its acceleration, so the *scattered power* is proportional to the acceleration squared.
4. The acceleration of an oscillation is ω² times its amplitude, where ω = 2πc / λ is the angular frequency. So the scattered power is proportional to ω⁴, which is 1/λ⁴.

Worked for blue (450 nm) and red (700 nm): blue's ω is 700 / 450 = 1.56 times red's. Its electrons accelerate 1.56² = 2.42 times more, and radiate 2.42² = 5.86 times the power.

## Why acceleration, and not amplitude

<!-- claim: why-acceleration -->
A natural guess is that electrons that move farther send out more light. With the natural frequency at a 100 nm wavelength (an estimate), the amplitude is 1.052 times its value under a steady field for blue, and 1.021 times for red. If scattered power followed the amplitude, blue would scatter only (1.052 / 1.021)² = 1.06 times more than red. The sky would be nearly white. The color comes from the acceleration: the same distance, covered faster.

## The sky, and the setting Sun

<!-- claim: guarantee-path -->
The light scattered out of the beam is the *sky light*. With the Sun overhead, the beam loses 20% of its blue and 4% of its red, so the sky light has about six times more blue than red, close to the 5.86 ratio. It still contains every color, so the sky is pale blue, not deep blue.

<!-- claim: why-multiply -->
How much the beam loses depends on the *air mass*, the length of its path relative to the path with the Sun overhead: 1 overhead, 38 at the horizon. Each air mass keeps the same fraction of the light still in the beam, 80% of the blue, so the losses multiply: 0.80³⁸ ≈ 0.02%. Added losses would remove more than all the blue. Estimates for clean, dry air, computed before rounding:

| Sun | Air mass | Blue (450 nm) gets through | Green (550 nm) | Red (700 nm) |
|---|---|---|---|---|
| overhead | 1 | 80% | 91% | 96% |
| on the horizon | 38 | 0.02% | 2.5% | 25% |

Overhead the Sun looks white; at the horizon almost no blue is left, and it looks red. Dust and smoke add scattering, so real sunsets differ in detail.

## When the rule fails: clouds

<!-- claim: guarantee-small-scatterer -->
The 1/λ⁴ rule holds only for particles much smaller than the wavelength, where all the electrons move together and their waves add. A cloud droplet, 10 µm across, is 22 times larger than 450 nm. Waves from its different parts interfere, the color dependence averages out, and clouds are white.

## Two wrong explanations

<!-- claim: misconception-absorb -->
- **"Air absorbs the other colors."** Air scatters visible light; it does not absorb it. On the Moon, with no air to scatter light, the sky is black in full daylight.

<!-- claim: misconception-violet -->
- **"Then the sky should be violet."** Violet (400 nm) scatters 1.60 times more than blue. But sunlight contains less violet than blue, and the eye is less sensitive to it. The eye sees the scattered mix as pale blue.

## In short

Blue light shakes the electrons in air faster, and scattered power goes with acceleration squared: 5.86 times red's. The scattered light is the sky; what stays in the beam is the Sun's color.

## Not covered here

- Polarization of sky light.
- Mie theory: scattering by particles near the wavelength in size.
