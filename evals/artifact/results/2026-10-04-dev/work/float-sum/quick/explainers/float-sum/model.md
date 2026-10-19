# Semantic model: why 0.1 + 0.2 != 0.3

> Source of truth. Every rendering derives from this file.

## Central question

Why does `0.1 + 0.2 == 0.3` evaluate to false in most programming languages?

## Audience and prior knowledge

A technical reader: school mathematics (fractions, powers, repeating decimals), basic programming (variables, `==`, printing). New to binary fractions and IEEE 754. Does not know that a float stores a binary fraction with a fixed number of bits.

## Entities

| Entity | Definition (one sentence) | Status |
|---|---|---|
| double | The default number type for decimals in most languages: a binary fraction with 53 significant bits (IEEE 754 binary64). | fact |
| stored value | The double nearest to the number written in the source code. | fact |
| rounding error | The difference between a written number and its stored value. | fact |
| spacing | The distance between two neighbouring doubles; 2^-54 ≈ 5.55e-17 for numbers between 0.25 and 0.5. | fact |

## Causal chain

```text
0.1 has an infinite binary expansion → the double keeps 53 bits → stored value ≠ 0.1
→ the errors of 0.1 and 0.2 add → the exact sum is rounded to a double
→ that double is one spacing above the stored value of 0.3 → == is false
```

## Quantities

- stored 0.1 = 0.1000000000000000055511151231257827… (error +5.55e-18)
- stored 0.2 = 0.2000000000000000111022302462515654… (error +1.11e-17)
- stored 0.3 = 0.2999999999999999888977697537484345… (error −1.11e-17)
- exact sum of stored 0.1 and 0.2 = 0.3000000000000000166533453693773481…
- result of 0.1 + 0.2 = 0.3000000000000000444089209850062616… (prints as 0.30000000000000004)
- difference result − stored 0.3 = 2^-54 ≈ 5.551115123125783e-17 = one spacing
- The exact sum lies exactly halfway between the two neighbouring doubles; round-half-to-even chooses the upper one.

## Why this form

| Operation | Simplest alternative | What the alternative breaks |
|---|---|---|
| Store a binary fraction | Store decimal digits | Binary hardware is faster and simpler; decimal types exist (Python `Decimal`, Java `BigDecimal`) but are slower. |
| Fixed 53 bits | Unlimited bits | 0.1 in binary is 0.000110011001100… and never ends, so no finite memory holds it exactly. |
| Compare with a tolerance | `==` | `0.1 + 0.2 == 0.3` is false; `abs(0.1 + 0.2 - 0.3) < 1e-9` is true. |

## Concrete cases

| Claim | Holds here | Breaks here |
|---|---|---|
| Sums of doubles are exact when every value is a sum of powers of 2 that fits in 53 bits | 0.5 + 0.25 == 0.75 is true | 0.1 + 0.2 == 0.3 is false |
| Decimal analogy: 3 decimal digits | 0.5 + 0.25 = 0.75 exact | 1/3 → 0.333; 0.333 + 0.333 = 0.666, but 2/3 → 0.667 |

## Terms

- **double**: as above.
- **stored value**: the double the computer actually holds. Never call it "the number 0.1".
- **rounding error**: written number minus stored value.
- **spacing**: gap between neighbouring doubles; small near 0, large for large numbers.

## Epistemic status

- **Established:** IEEE 754 binary64 values above; they follow mathematically from the standard.

## Confusion points

- "The computer adds badly." → The addition is correctly rounded. The inputs are already not 0.1 and 0.2.
- "But `print(0.1)` shows 0.1." → Languages print the shortest decimal that maps back to the same double. The stored value is still not 0.1.
- "The error is random." → It is deterministic: the same code gives the same result every time.

## Scope

- **Out of scope:** exponent field and bit layout — see IEEE 754; error accumulation in long sums (Kahan summation); NaN and infinities.

## Representation decision

- **Stage:** 1
- **Reason:** A short linear causal chain with worked numbers; a table carries the numbers. No parameters to explore.
- **Levels:** L1 the answer / L2 the stored values / L3 why binary cannot hold 0.1 / L4 what to do.
