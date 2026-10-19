# Why does 0.1 + 0.2 not equal 0.3?

In Python, JavaScript, and most other languages, `0.1 + 0.2 == 0.3` is `false`, and `0.1 + 0.2` prints `0.30000000000000004`.

**The computer never holds 0.1, 0.2, or 0.3. It holds the nearest numbers it can store in binary. The addition is correct, but its result rounds to the next storable number above the one that 0.3 rounds to.**

## What the computer holds

A literal such as `0.1` becomes a **double**: the 64-bit binary format that most languages use for numbers with a decimal point. A double is a whole number of at most 53 binary digits, times a power of two. The other 11 bits hold the sign and the power. For example, 0.75 = 3 × 2^-2, so a double holds 0.75 exactly.

## Why 0.1 must be rounded

A whole number times a power of two is a fraction whose denominator is a power of two. <!-- claim: tenth-not-binary --> A fraction like that ends in binary: 3/8 = 0.011. The denominator of 1/10 has a factor 5. No power of two is divisible by 5, so 1/10 never ends in binary:

    1/10 = 0.000110011001100110011…   (0011 repeats forever)

This is the same as 1/3 = 0.3333… in decimal. A machine that keeps only a fixed number of digits must cut the expansion, so it rounds. With 4 decimal digits, 1/3 becomes 0.3333, and 0.3333 + 0.3333 = 0.6666, but 2/3 becomes 0.6667. The same thing happens with 0.1, 0.2, and 0.3 in binary.

## The stored values

The **stored value** of a literal is the double nearest to it. The **gap** is the distance between two neighboring doubles.

The gap depends on the size of the number. Doubles between 0.25 and 0.5 are whole numbers from 2^52 up to 2^53, times 2^-54. The ends check: 2^52 × 2^-54 = 0.25, and 2^53 × 2^-54 = 0.5. Neighboring whole numbers differ by 1, so neighboring doubles here differ by u = 2^-54 ≈ 5.55e-17. Between 0.125 and 0.25 the multiplier is 2^-55, so the gap is u/2. Between 0.0625 and 0.125 the gap is u/4.

To see the rounding, count each number in units of u. For example, 0.3 × 2^54 = 5404319552844595.2, so 0.3 is 5404319552844595.2 u. The nearest doubles are at 5404319552844595 u and 5404319552844596 u. The nearer one is …595 (short for 5404319552844595), so 0.3 rounds down. 0.1 is in the range where the gap is u/4, so its stored value is a multiple of u/4, such as …198.5.

The **error** is the stored value minus the decimal: 0.1 and 0.2 round up, and 0.3 rounds down. <!-- claim: stored-values -->

| Number | Exact, in u | Gap here | Stored, in u | Stored, in decimal | Error |
|---|---|---|---|---|---|
| 0.1 | 1801439850948198.4 | u/4 | 1801439850948198.5 | 0.10000000000000000555 | +5.55e-18 |
| 0.2 | 3602879701896396.8 | u/2 | 3602879701896397 | 0.20000000000000001110 | +1.11e-17 |
| 0.3 | 5404319552844595.2 | u | 5404319552844595 | 0.29999999999999998890 | −1.11e-17 |
## What `+` does

The `+` operation first finds the **exact sum** of the two stored values. Then it rounds that exact sum to a double, as every arithmetic operation does. The result is the **rounded sum**. <!-- claim: sum-rounds-up -->

    exact sum   = 1801439850948198.5 + 3602879701896397 = 5404319552844595.5 u

The exact sum is exactly halfway between the doubles at …595 u and …596 u. This case is a **tie**. The IEEE 754 standard, which sets these rules, sends a tie to the neighbor whose count of u is even. 5404319552844596 is even, so the rounded sum is 5404319552844596 u, which is 0.30000000000000004441.

Stored 0.3 is at …595 u. The rounded sum and stored 0.3 are neighboring doubles, one gap (5.55e-17) apart. They are different numbers, so `==` is false.

The addition did not make a mistake. The rounded sum is the nearest double to the exact sum of its inputs. The inputs were not 0.1 and 0.2.

## Why `print(0.1)` shows `0.1`

<!-- claim: printing-hides -->
Languages print the shortest decimal that rounds back to the same double. The text "0.1" rounds back to stored 0.1, so one digit is enough. The text "0.3" rounds back to …595 u, not to the rounded sum at …596 u. The shortest decimal that rounds back to …596 u is 0.30000000000000004, with 17 significant digits.

## When it works

<!-- claim: exact-when-binary -->
`0.5 + 0.25 == 0.75` is true. All three are fractions with power-of-two denominators (1/2, 1/4, 3/4), so each is stored with error 0, and the exact sum is itself a double. The failure needs a decimal whose denominator has a factor 5, such as 0.1.

A decimal type also avoids the problem. Python's `Decimal("0.1") + Decimal("0.2") == Decimal("0.3")` is true, because `Decimal` stores base-10 digits, and 1/10 ends in base 10.

## What to do

<!-- claim: why-tolerance -->
Do not compare doubles with `==` when they come from decimal literals or from arithmetic. Compare with a tolerance instead: `abs((0.1 + 0.2) - 0.3) < 1e-9` is true, because the rounded sum and stored 0.3 are one gap (5.55e-17) apart. Choose a tolerance much larger than the gap, but smaller than any difference that matters to you; for values near 1, 1e-9 meets both conditions. For money, count whole cents as integers, or use a decimal type.

## Not covered here

- The sign and exponent bits of a double: see IEEE 754, or Goldberg, "What Every Computer Scientist Should Know About Floating-Point Arithmetic" (1991).
- How errors grow over many operations, such as adding 0.1 ten times: see a numerical analysis text.
- How to choose between an absolute and a relative tolerance: see the documentation for Python's `math.isclose`.
