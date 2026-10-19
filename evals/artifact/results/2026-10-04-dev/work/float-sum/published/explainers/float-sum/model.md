# Semantic model: why 0.1 + 0.2 != 0.3 in floating point

> Source of truth. Every rendering derives from this file.

## Central question

Why does `0.1 + 0.2 == 0.3` evaluate to false in most programming languages?

## Audience and prior knowledge

A technical reader: school mathematics and science, basic programming. Knows decimals, fractions, powers, that computers store numbers in binary, and what `==` does. Does not know how a float is stored, which fractions end in binary, what rounding to a fixed number of bits does, or how languages print floats.

## Entities

| Entity | Definition (one sentence) | Status |
|---|---|---|
| double | The 64-bit binary floating-point format (IEEE 754 binary64) that most languages use for a number with a decimal point. | fact |
| significant bits | A double keeps 53 binary digits: every double is a whole number below 2^53 times a power of two. | fact |
| gap | The distance between two neighboring doubles. Because the 53 bits are fixed, the gap halves each time the size of the number halves. | fact |
| stored value | The double nearest to the decimal you wrote; what the program holds for `0.1`. | fact |
| error | stored value − written decimal; + means the stored value is above the decimal. | definition |
| exact sum | The true sum of two stored values, before rounding. | definition |
| rounded sum | The exact sum after rounding to the nearest double; this is the result of `+`. | fact |
| rounding | Replacing an exact number with the nearest double. A tie (exactly halfway) goes to the neighbor whose whole number is even. | fact |
| printed value | The shortest decimal that rounds back to the same double; what `print` shows. | fact (Python, JavaScript, and most modern languages) |

## Relationships

| From | Relationship | To | Notes |
|---|---|---|---|
| decimal 0.1 | is rounded to | stored value | 1/10 does not end in binary |
| stored 0.1, stored 0.2 | add to | exact sum | |
| exact sum | is rounded to | rounded sum | every arithmetic operation rounds its result |
| rounded sum | is one gap above | stored 0.3 | so `==` is false |
| printed value | hides | the error of stored 0.1 | |

## Dependencies (learning order)

1. A fixed number of digits cannot hold every fraction (decimal: 1/3 → 0.3333).
2. A fraction ends in binary only if its denominator (in lowest terms) is a power of two; 1/10 has a factor 5.
3. So 0.1, 0.2, 0.3 each become the nearest double, with their own error.
4. Measured in the gap near 0.3, the exact sum falls at a half; it rounds up, while 0.3 rounded down.
5. Printing shows the shortest decimal that picks out the double, so 0.1 looks exact and the sum does not.

## Causal chain

```text
1/10 has a factor 5 in its denominator → no finite binary expansion
→ 0.1 and 0.2 round up, 0.3 rounds down (errors +5.55e-18, +1.11e-17, −1.11e-17)
→ exact sum = stored 0.3 + half a gap → tie → rounds to the even neighbor, the double above
→ rounded sum and stored 0.3 are neighboring, different doubles → == is false
```

## Quantities

Unit u = 2^-54 ≈ 5.55e-17, the gap between doubles from 0.25 to 0.5. From 0.125 to 0.25 the gap is u/2; from 0.0625 to 0.125 it is u/4.

| Number | Exact, in u | Allowed steps | Stored, in u | Stored, in decimal | Error |
|---|---|---|---|---|---|
| 0.1 | 1801439850948198.4 | u/4 | 1801439850948198.5 | 0.10000000000000000555 | +5.55e-18 |
| 0.2 | 3602879701896396.8 | u/2 | 3602879701896397 | 0.20000000000000001110 | +1.11e-17 |
| exact sum | 5404319552844595.5 | — | — | 0.30000000000000001665 | +1.67e-17 |
| rounded sum | — | u | 5404319552844596 | 0.30000000000000004441 | +4.44e-17 |
| 0.3 | 5404319552844595.2 | u | 5404319552844595 | 0.29999999999999998890 | −1.11e-17 |

- Check: 0.3 × 2^54 = 5404319552844595.2; 0.1 × 2^56 = 7205759403792793.6 → 7205759403792794 quarter-units = 1801439850948198.5 u.
- Exact sum: 1801439850948198.5 + 3602879701896397 = 5404319552844595.5. A tie between …595 and …596; …596 is even, so the rounded sum is …596. (Round half up would also give …596.)
- Difference rounded sum − stored 0.3 = 1 u ≈ 5.55e-17. Relative: 5.55e-17 / 0.3 ≈ 1.9e-16, so the first 16 significant digits agree and the difference shows in the 17th: 0.3000000000000000|4.
- Printing: "0.1" rounds to stored 0.1, so one digit is enough. For the rounded sum, "0.3" and every shorter decimal round to stored 0.3, the wrong double; the first that works is 0.30000000000000004 (17 significant digits).
- Binary of 1/10: 0.000110011001100110011… (0011 repeats).
- Gap meaning: near 0.3 the gap is 5.55e-17 (fine); near 10^16 it is 2, so 10^16 + 1 cannot be stored.

## Alternative states

| State / scenario | What changes | Why |
|---|---|---|
| 0.5 + 0.25 == 0.75 | true | 1/2, 1/4, 3/4 have power-of-two denominators: errors 0, exact sum is a double |
| decimal type (Python `Decimal("0.1")`) | 0.1 + 0.2 == 0.3 is true | digits stored in base 10, where 1/10 ends |
| 4-digit decimal calculator | 1/3 → 0.3333; 0.3333 + 0.3333 = 0.6666, but 2/3 → 0.6667 | the same effect in base 10 with 1/3 |

## Why this form

| Operation | Simplest alternative | What the alternative breaks (with numbers) |
|---|---|---|
| Fixed 53-bit binary storage | Store exact decimal digits | Exact storage of every fraction needs unbounded memory (1/3 has no finite decimal either); fixed-size binary is what the processor adds in one step. Decimal types exist and are slower. |
| Compare with a tolerance: abs(a − b) < 1e-9 | `==` | `0.1 + 0.2 == 0.3` is false though the difference is 5.55e-17. |

## Concrete cases

| Claim | Holds here (numbers) | Breaks here (numbers) |
|---|---|---|
| A sum of stored values equals the stored value of the decimal sum | 0.5 + 0.25 == 0.75: all errors 0 | 0.1 + 0.2: rounded sum …596 u, stored 0.3 …595 u |
| Only power-of-two denominators end in binary | 3/8 = 0.011 in binary | 1/10: 2^k / 10 is never whole, because no power of 2 is divisible by 5 |
| Fixed digits lose information (decimal analogy) | 1/4 = 0.25 | 1/3 → 0.3333; 0.3333 + 0.3333 = 0.6666 ≠ 0.6667 |

## Terms

- **double**: the 64-bit binary format for numbers with a decimal point.
- **gap**: the distance between neighboring doubles; u = 5.55e-17 near 0.3. Small gap = fine resolution; near 10^16 the gap is 2.
- **stored value**: the double the program holds for a literal like `0.1`. Never call it "0.1" alone.
- **error**: stored value − written decimal.
- **exact sum** vs **rounded sum**: before and after rounding. Never "the sum" alone.
- **tie**: an exact number exactly halfway between two doubles.
- **printed value**: the shortest decimal that rounds back to the same double.

## Epistemic status

- **Established:** IEEE 754 binary64, round half to even, the stored values above.
- **Mathematical consequence:** 1/10 has no finite binary expansion.
- **Observed:** Python and JavaScript print `0.30000000000000004` for `0.1 + 0.2`.

## Confusion points

- "The addition is buggy" → the addition is correct to the last bit; the inputs were never exactly 0.1 and 0.2.
- "0.1 is stored exactly, because it prints as 0.1" → printing shows the shortest decimal that picks out the double.
- "The result is random noise" → it is deterministic: the same on every IEEE 754 machine.
- "Floats are always inexact" → 0.5 + 0.25 == 0.75 is exact.

## Scope

- **Out of scope:** sign and exponent bits — IEEE 754; Goldberg, "What Every Computer Scientist Should Know About Floating-Point Arithmetic" (1991).
- **Out of scope:** error growth in long sums (adding 0.1 ten times) — numerical analysis texts.
- **Out of scope:** how to choose a tolerance (relative vs absolute) — `math.isclose` documentation.
- **Out of scope:** languages whose literals are not doubles by default (Raku uses exact fractions) and fused or extended-precision hardware.

## Representation decision

- **Stage:** 1 (prose)
- **Reason:** one sequential causal chain with worked numbers; nothing for the reader to explore or to see move. A table carries the numbers.
- **Levels:** L1 the answer / L2 stored values and the rounded sum / L3 why 1/10 does not end in binary / L4 bit layout (Scope).
