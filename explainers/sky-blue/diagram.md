# Why is the sky blue, and the setting Sun red?

<!-- Stage 2, rendered from model.md. Same names as the prose: beam, sky light, scattered power, air mass. -->

**Air molecules scatter blue light about six times more than red. The scattered light is the blue sky; what stays in the Sun's beam is the Sun's color.**

Terms: the *beam* is the light coming straight from the Sun. ω = 2πc / λ is the light's angular frequency, larger for shorter wavelengths. *Air mass* is the length of the beam's path through the air: 1 with the Sun overhead, 38 at the horizon.

<!-- claim: mechanism-dipole -->
<!-- claim: guarantee-path -->
```mermaid
flowchart TD
    S["Sunlight"] --> M["Air molecule, 0.3 nm<br/>the light's field drives its electrons"]
    M -->|"far below their ultraviolet natural frequency:<br/>nearly the same amplitude for every color"| A["acceleration = ω² × amplitude<br/>larger for blue"]
    A -->|"radiated field ∝ acceleration,<br/>power ∝ field²"| P["Scattered power ∝ ω⁴ ∝ 1/λ⁴<br/>blue 450 nm: 5.86 × red 700 nm"]
    P -->|"scattered out of the beam"| K["Sky light<br/>mostly blue: a blue sky"]
    P -->|"what stays in the beam;<br/>each air mass keeps the same fraction"| B["Sun's color"]
    B --> N["overhead, air mass 1<br/>blue 80%, red 96% get through: white"]
    B --> H["horizon, air mass 38<br/>blue 0.02%, red 25% get through: red"]
```

## Why acceleration, not amplitude

<!-- claim: why-acceleration -->
```mermaid
flowchart LR
    A["If scattered power followed the amplitude<br/>(1.052 for blue, 1.021 for red)"] --> A2["blue only 1.06 × red<br/>a nearly white sky"]
```

## When the rule fails: large scatterers

<!-- claim: guarantee-small-scatterer -->
```mermaid
flowchart LR
    D["Cloud droplet, 10 µm<br/>22 × larger than 450 nm"] -->|"waves from its different parts<br/>arrive out of step and interfere"| D2["every color scatters about equally<br/>white clouds"]
```

A molecule is 1,500 times smaller than the wavelength, so all its electrons move together and their waves add. So the sky is blue because the scatterers are small and their power follows the acceleration; the low Sun is red because a long path removes the blue from its beam.
