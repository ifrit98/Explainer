# Semantic model: why the sky is blue

> Source of truth. Every rendering (prose, diagram) derives from this file.
> If a rendering needs a new fact, add it here first.

## Central question

Why is the daytime sky blue, and why is the setting Sun red?

## Audience and prior knowledge

A technical reader. They know that light is an electromagnetic wave with a wavelength, that visible light runs from about 400 nm (violet) to 700 nm (red), that white light is a mix of all visible wavelengths, that atoms and molecules contain electrons, and school mechanics (force, acceleration, oscillation). They do not know how light scatters.

## Entities

| Entity | Definition (one sentence) | Status |
|---|---|---|
| sunlight | a mix of all visible wavelengths that looks white | observation |
| air molecule | N₂ or O₂, about 0.3 nm across, 1,500 times smaller than a 450 nm wavelength | established fact |
| bound electron | an electron held in a molecule like a mass on a spring, with a natural frequency in the ultraviolet | model (the Lorentz oscillator) |
| scattering | a molecule takes light out of the beam and sends it out in other directions; no energy turns into heat | established fact |
| scattered power | the power one molecule sends out; proportional to 1/λ⁴ for molecules | established fact |
| air mass | the length of the Sun's path through the air, relative to the path with the Sun overhead | established fact |
| cloud droplet | a water drop about 10 µm across, 22 times larger than a 450 nm wavelength | observation |

## Causal chain

```text
light's electric field pushes the bound electrons
  → the electrons oscillate at the light's frequency, with about the same amplitude for every color
  → acceleration = ω² × amplitude (ω = 2πc / λ), so electrons driven by blue light accelerate more
  → the radiated field ∝ acceleration, and power ∝ field², so scattered power ∝ ω⁴ ∝ 1/λ⁴
  → blue (450 nm) scatters 5.86 times more than red (700 nm)
  → the light scattered out of the beam is the sky light: overhead, the beam loses 20% of its blue and 4% of its red, so the sky light has about five times more blue than red, with every color present (pale blue)
  → each air mass keeps the same fraction of what is left (80% of the blue), so losses multiply: 0.80³⁸ ≈ 0.02% at the horizon; the low Sun is red
```

## Quantities

- Scattered power ∝ 1/λ⁴. Blue 450 nm vs red 700 nm: (700 / 450)⁴ = 5.86. Violet 400 nm vs blue 450 nm: (450 / 400)⁴ = 1.60. Violet vs red: 9.38.
- Larmor formula (established): a charge q with acceleration a radiates P = q² a² / (6π ε₀ c³).
- Driven electron (model): amplitude x = (qE/m) / (ω₀² − ω²). With ω₀ at a 100 nm wavelength (estimate), the amplitude is 1.052 times its zero-frequency value at 450 nm and 1.021 times at 700 nm.
- Rayleigh optical depth of a clean, dry atmosphere at sea level (Hansen & Travis 1974 fit; estimate): τ = 0.22 at 450 nm, 0.097 at 550 nm, 0.037 at 700 nm. The fraction of a beam that gets through is e^(−τ × air mass).
- Air mass: 1 with the Sun overhead, 38 at the horizon (Kasten–Young formula; a flat-air secant would give infinity).
- Losses multiply: each air mass keeps the same fraction of the light still in the beam. Blue keeps 80% per air mass: 0.80³⁸ ≈ 0.02%. A loss that added up instead (20% per air mass, 38 times) would remove more than all of it.
- 5.86 is the pure 1/λ⁴ law. The Lorentz model with ω₀ at 100 nm gives about 6.2; the measured optical depths give 0.22 / 0.037 = 5.9. All round to about 6.

| Sun | Air mass | Blue 450 nm through | Green 550 nm through | Red 700 nm through |
|---|---|---|---|---|
| overhead | 1 | 80% | 91% | 96% |
| on the horizon | 38 | 0.02% | 2.5% | 25% |

## Alternative states

| State | What changes | Result |
|---|---|---|
| Sun high | short path: air mass 1 | the beam keeps 80% of its blue; the Sun looks white-yellow; the sky around it is blue |
| Sun on the horizon | air mass 38 | 0.02% of the blue gets through, 25% of the red; the Sun looks red |
| no air (the Moon) | no scatterers | no scattered light; the sky is black in full daylight |
| cloud droplets | scatterer 22 times larger than the wavelength | every color scatters about equally; clouds look white |

## Why this form

| Operation | Simplest alternative | What the alternative breaks (with numbers) |
|---|---|---|
| power ∝ acceleration² (so ∝ ω⁴); the radiated field is proportional to the acceleration, and a wave's power is proportional to its field squared | power follows the amplitude of the electron's motion | the amplitude is nearly the same for every color (1.052 at 450 nm, 1.021 at 700 nm), so blue would scatter only (1.052 / 1.021)² = 1.06 times more than red: a nearly white sky |
| the sky color is the scattered light, not the beam | the sky is blue because air is blue | air does not absorb blue: overhead, 80% of the blue reaches the ground in the direct beam, and the sky on the Moon is black |

## Concrete cases

| Claim | Holds here (numbers) | Breaks here, without its assumption (numbers) |
|---|---|---|
| scattered power ∝ 1/λ⁴ when the scatterer is much smaller than λ | N₂, 0.3 nm, 1,500 times smaller than 450 nm: blue scatters 5.86 times more than red | a 10 µm cloud droplet, 22 times larger than 450 nm: waves from different parts of the droplet interfere, and all colors scatter about equally (Mie scattering), so clouds are white |
| a long path removes the blue from the beam (losses multiply) | at the horizon (air mass 38): 0.02% of the blue, 25% of the red gets through | with the Sun overhead (air mass 1): 80% of the blue, 96% of the red; the Sun looks white |
| mechanism: driven electron radiates | blue, ω about 1.56 times red's ω: acceleration 1.56² = 2.42 times larger, power 2.42² = 5.86 times larger | — |

## Terms

- **scattering:** a molecule takes light out of the beam and sends it out again in other directions. Not absorption: the light is not turned into heat.
- **scattered power:** the power one molecule sends out. One name; not "scattering strength" or "intensity".
- **air mass:** the length of the path through air, relative to overhead.
- **beam:** the light that comes straight from the Sun. **Sky light:** the scattered light that reaches you from other directions.
- **Rayleigh scattering:** scattering by particles much smaller than the wavelength, with power ∝ 1/λ⁴.

## Epistemic status

- **Observed:** the sky is blue; the low Sun is red or orange; clouds are white; the sky on the Moon is black in daylight.
- **Established fact:** the Larmor formula; scattered power ∝ 1/λ⁴ for particles much smaller than λ (Rayleigh scattering); Mie scattering for large particles.
- **Model:** the bound electron as a mass on a spring (the Lorentz oscillator). It gives the right wavelength dependence; quantum mechanics gives the same result.
- **Estimate:** the natural wavelength of 100 nm; the optical depths (a fit for clean, dry air; dust, smoke, and humidity add scattering that makes real sunsets less clean); the air mass at the horizon.

## Confusion points

- "The sky is blue because it reflects the ocean." → The sky is blue over deserts too; the cause is scattering by air molecules.
- "Air absorbs the other colors." → Air scatters; it does not absorb visible light. The red and green are still in the beam.
- "Then the sky should be violet." → Violet scatters 1.60 times more than blue, but sunlight has less violet than blue, and the eye is less sensitive to violet. The eye sees the scattered mix, which also contains green and red, as pale blue.

## Scope

- **Out of scope:** the color of the sky as a precise mix — see color science (CIE color matching).
- **Out of scope:** polarization of sky light (scattered light at 90° from the Sun is strongly polarized) — see Rayleigh scattering, polarization.
- **Out of scope:** why the electron's natural frequency is in the ultraviolet — see atomic absorption spectra.
- **Out of scope:** Mie scattering in detail — see Mie theory.
- **Out of scope:** the solar spectrum and the eye's sensitivity in numbers (why violet loses) — see the CIE luminosity function V(λ).
- **Out of scope:** why the horizon sky is paler than the sky overhead (multiple scattering) and the angular pattern 1 + cos²θ.
- **Out of scope:** ozone's weak absorption near 600 nm, which keeps the twilight sky blue.

## Representation decision

- **Stage:** 1 (prose), with a Stage 2 diagram.
- **Reason:** the argument is a causal chain of six links; prose carries a chain. The two light paths (overhead and horizon) and the two kinds of scatterer are a spatial comparison, which a diagram shows at a glance.
- **Levels:** L1 sky light is scattered sunlight / L2 molecules scatter blue 5.86 times more than red / L3 why: power ∝ acceleration², acceleration ∝ ω² / L4 the optical depth and air mass numbers.
