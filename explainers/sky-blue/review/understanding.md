# Understanding tests: sky-blue

The first example built with the v0.6.0 process: an audience-aware probe and cold read that report excess as well as gaps, and a declared length budget (650 words of prose).

## Probe (model.md)

Run 2026-10-04. 16 gaps, 9 marked "main". Adopted 5, each as a clause or a replacement, not a section:

| Finding | Adopted as |
|---|---|
| "scattering" defined as absorb-and-re-emit in one row, "not absorption" in another | one definition everywhere: out of the beam, no heat |
| why losses multiply along the path | "each air mass keeps the same fraction": 0.80³⁸ ≈ 0.02%, and added losses would exceed 100% |
| the light lost from the beam is the sky light | one sentence, with 20% vs 4% |
| why power ∝ acceleration² | "its radiated field is proportional to its acceleration" |
| why size matters | "all the electrons move together and their waves add"; in a droplet they interfere |

Not adopted: the optical depth τ as a term (the multiply argument carries it without a new symbol); the Lorentz 6.2 vs 5.86 vs 5.9 reconciliation (in `model.md` only); the secant air mass; ozone; the angular pattern; solar spectrum and eye-sensitivity numbers (Scope). The probe also listed four model entries as excess; three were removed.

## Blind test (prose)

Run 2026-10-04. Every quiz item scored 2 (red-star sky, sunset vs noon, droplet-sized molecules, why acceleration, white clouds); no general item scored 0. **Pass.**

Its audit listed 30 items. Three were real and cheap: a rounding note on the table (0.96³⁸ gives 21%, the table 25%), "about 5 times" next to 5.86, and the undefined "zero-frequency value". The rest asked for derivations below this reader's level (why acceleration is ω² × amplitude, why a wave's power goes with its field squared), or flagged ordinary words as a second name ("noon" and "overhead"). That audit had no audience and no excess counterweight; v0.6.0 gives the blind test both.

## Cold read (prose)

Run 2026-10-04 with the v0.6.0 prompt. **Blocking:** the premise "the electron moves about the same distance for every color" had no reason; 5 vs 5.86; the air mass 38 used before it was given. Also: no close.

Fixed by replacement: step 2 now says why (far below its natural frequency the spring force dominates, and the electron follows the field) and the duplicate in the next section went; 38 is given with the definition of air mass; an "In short" close. The budget then failed at 695 words, and cuts brought it to 650: a shorter lead, the cloud paragraph, the absorb bullet, the close.

Not applied (edge): a formula for the driven amplitude; numbers for the solar spectrum and the eye; epistemic labels on each step.

## Cold read (diagram)

Run 2026-10-04. **Blocking:** the diagram did not stand alone. "Air mass", ω, and λ were never defined in it, and the beam only in an author comment; "power ∝ acceleration²" and "same amplitude for every color" had no reason; "1.06" contradicted "same amplitude"; the amplitude counterfactual sat under "When the rule fails" as if it were a real case.

Fixed: the answer in one bold line first; a three-term legend (beam, ω, air mass); a reason on each arrow (far below the ultraviolet natural frequency; radiated field ∝ acceleration, power ∝ field²; each air mass keeps the same fraction); "nearly the same amplitude" with the two factors; two headings, one for the counterfactual and one for the real failure; a closing sentence that answers the title.

Not applied (edge): why violet loses (in the prose); a rounding note on 25% (in the prose).
