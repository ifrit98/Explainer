# Why does 0.1 + 0.2 not equal 0.3?

<!-- Stage 1, rendered from model.md in STE-80. -->

**The computer never holds 0.1, 0.2, or 0.3. It holds the nearest binary fractions, and those small errors add up to a result that is a different number from the stored 0.3.** In most languages, `0.1 + 0.2` prints `0.30000000000000004`, so `0.1 + 0.2 == 0.3` is false.

## The same problem in base 10

Suppose a calculator keeps 3 decimal digits. It cannot hold 1/3, so it stores 0.333. Add two of them: 0.333 + 0.333 = 0.666. But the calculator stores 2/3 as 0.667. So "1/3 + 1/3 == 2/3" is false on this calculator.

The calculator adds correctly. The inputs were already wrong, because 1/3 has no finite decimal form.

## Why 0.1 has the same problem in base 2

Most languages store a decimal number as a **double**: a binary fraction with 53 significant bits (the IEEE 754 standard). A binary fraction is a sum of powers of 2: 1/2, 1/4, 1/8, and so on.

<!-- claim: why-binary-inexact -->
In base 2, 0.1 is like 1/3 in base 10. Its binary form, 0.000110011001100…, repeats forever. A double keeps only 53 bits, so it stores the nearest binary fraction. Call this the **stored value**:

| Written | Stored value (first 34 digits) |
|---|---|
| 0.1 | 0.1000000000000000055511151231257827 |
| 0.2 | 0.2000000000000000111022302462515654 |
| 0.3 | 0.2999999999999999888977697537484345 |

The stored 0.1 and 0.2 are slightly too high. The stored 0.3 is slightly too low.

## What happens in the addition

<!-- claim: mech-sum -->
1. The computer adds the two stored values. The exact sum is 0.3000000000000000166533453693773481.
2. That sum is not a double either, so the computer rounds it to the nearest double. The sum is exactly halfway between two doubles; the tie rule picks the upper one: 0.3000000000000000444089209850062616.
3. The stored 0.3 is the double just below that result. The two differ by 5.551115123125783e-17, the gap between neighbouring doubles near 0.3.
4. `==` compares the doubles bit for bit. They differ, so the answer is false.

## When addition is exact

<!-- claim: guarantee-exact -->
Before you read on, predict: is `0.5 + 0.25 == 0.75` true?

It is true. 0.5 is 1/2 and 0.25 is 1/4, so both are short binary fractions. Their sum, 0.75, is also one. No step rounds, so no error appears. The problem comes only from numbers that have no short binary form, such as 0.1, 0.2, and 0.3.

## "But print(0.1) shows 0.1"

<!-- claim: misc-print -->
Languages print the shortest decimal that maps back to the same double. For the stored 0.1, that decimal is "0.1". For the result of 0.1 + 0.2, the shortest such decimal is 0.30000000000000004, because "0.3" maps to a different double. The print hides the error; it does not remove it.

## What to do

<!-- claim: why-tolerance -->
- Compare with a tolerance, not `==`. `abs(0.1 + 0.2 - 0.3) < 1e-9` is true.
- For money, count in integer cents: 10 + 20 == 30 is always true.
- If you need exact decimal arithmetic, use a decimal type, for example Python `Decimal` or Java `BigDecimal`. These are slower than doubles.

This behaviour is not a bug and not random. Every language that uses IEEE 754 doubles (JavaScript, Python, Java, C, and most others) gives the same result every time.
