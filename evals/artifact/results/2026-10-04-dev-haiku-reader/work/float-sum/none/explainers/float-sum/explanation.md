# Why 0.1 + 0.2 ≠ 0.3

Type this into Python, JavaScript, Java, C, Ruby, Go, or most other languages:

```
0.1 + 0.2 == 0.3      →  false
0.1 + 0.2             →  0.30000000000000004
```

This isn't a bug in the language or in your CPU. The computer is doing exactly what it was designed to do. The surprise comes from two facts that work together:

1. The computer stores numbers in **binary**, and **0.1, 0.2 and 0.3 can't be written exactly in binary**. Each one gets rounded to the nearest number that *can* be stored.
2. Those three small rounding errors don't cancel out.

The rest of this document explains both facts and then what to do about them.

---

## 1. A familiar version of the problem: 1/3 in decimal

Before binary, look at something you already know. In decimal, 1/3 has no finite form:

```
1/3 = 0.3333333333...   (the 3s never end)
```

Say you could only keep 4 decimal places. You'd store 1/3 as `0.3333`. Then:

```
0.3333 + 0.3333 + 0.3333 = 0.9999   ≠ 1
```

Nothing went wrong with the addition. The error was already there once you rounded 1/3 to fit the space you had.

Which fractions end and which repeat depends on the **base**. In base 10, a fraction has a finite form only if its denominator (after simplifying) has no prime factors other than 2 and 5, the prime factors of 10. So 1/2, 1/4, 1/5 and 1/8 end, while 1/3, 1/6 and 1/7 repeat forever.

## 2. The same problem in binary

Base 2 has only one prime factor: 2. So in binary, a fraction has a finite form **only if its denominator is a power of 2**: 1/2, 1/4, 3/8, 5/16, and so on.

Now look at our numbers as fractions:

| Decimal | Fraction | Denominator a power of 2? |
|---|---|---|
| 0.5 | 1/2 | yes, exact in binary |
| 0.25 | 1/4 | yes, exact |
| 0.1 | 1/10 | no (10 = 2 × **5**) |
| 0.2 | 1/5 | no |
| 0.3 | 3/10 | no |

So 0.1 repeats forever in binary, the same way 1/3 does in decimal:

```
0.1 (decimal) = 0.0001100110011001100110011...  (binary, "0011" repeats forever)
```

You can check this by repeated doubling, which is how you convert a fraction to binary. Double the number. If the result is 1 or more, write a 1 and subtract 1. Otherwise write a 0.

```
0.1 × 2 = 0.2  → 0
0.2 × 2 = 0.4  → 0
0.4 × 2 = 0.8  → 0
0.8 × 2 = 1.6  → 1   (keep 0.6)
0.6 × 2 = 1.2  → 1   (keep 0.2)
0.2 × 2 = 0.4  → 0   ← we've been at 0.2 before, so the pattern repeats
...
```

The digits come out `0.0001 1001 1001 1001 ...`, and they never stop.

## 3. How much room the computer has

Most languages store non-integer numbers in the **IEEE 754 double-precision** format (a "double", or `float` in Python and `number` in JavaScript). It's scientific notation in base 2:

```
value = ± (1.xxxxxxxx...) × 2^exponent
```

The digits after the point (the *significand*) get a fixed budget: **53 significant binary digits**. That's roughly 15–17 significant decimal digits. Whatever doesn't fit is rounded off, to the *nearest* number that can be stored.

So "0.1" in your source code is never stored as 0.1. It's stored as the closest double to 0.1. Here are the exact stored values, written out in full decimal. Every double has a finite decimal expansion, because its denominator is a power of 2.

| You wrote | What is actually stored | Error |
|---|---|---|
| `0.1` | 0.1000000000000000055511151231257827… | a little **too big** |
| `0.2` | 0.2000000000000000111022302462515654… | a little **too big** |
| `0.3` | 0.2999999999999999888977697537484345… | a little **too small** |

That already explains most of the surprise. The 0.1 and 0.2 you add are both slightly too big. The 0.3 you compare against is slightly too small. They're about to land on different sides of the true 0.3.

## 4. The addition itself

The computer adds the two stored values. The exact mathematical sum is:

```
  0.1000000000000000055511151231257827…
+ 0.2000000000000000111022302462515654…
= 0.3000000000000000166533453693773481…
```

That result also has to be stored as a double, so it gets rounded again. Near 0.3, the doubles are spaced about 5.55 × 10⁻¹⁷ apart. The two candidates on either side of our sum are:

```
lower:  0.29999999999999998889776975…   (this is the double we call "0.3")
sum:    0.30000000000000001665334536…
upper:  0.30000000000000004440892098…
```

The sum sits **exactly halfway** between them: 2.775 × 10⁻¹⁷ from each. IEEE 754's tie rule is "round half to even": pick the neighbour whose last binary digit is 0. That's the upper one. So the result is:

```
0.1 + 0.2  →  0.3000000000000000444089209850062616…
```

That's a *different double* from the one `0.3` gives you. They're neighbours, one step apart, but they aren't equal, so `==` returns `false`.

> For readers who like exact arithmetic: the double for 0.1 is exactly
> 3602879701896397 × 2⁻⁵⁵, and the double for 0.2 is twice that. Their sum is
> 10808639105689191 × 2⁻⁵⁵. Near 0.3 the stored values are whole multiples of
> 2⁻⁵⁴, and 10808639105689191 / 2 = 5404319552844595.5, an exact tie. Rounding to
> even gives 5404319552844596 × 2⁻⁵⁴. But `0.3` is stored as 5404319552844595 × 2⁻⁵⁴.

## 5. Why it *prints* as 0.30000000000000004, while 0.1 prints as 0.1

If 0.1 isn't stored exactly, why does `print(0.1)` show `0.1`?

Modern languages print the **shortest decimal string that maps back to the same double**. "0.1" is shorter than "0.1000000000000000055511…", and reading "0.1" back gives exactly the same stored value. So the language shows you "0.1". It hides the error, but nothing is lost.

For the sum, "0.3" would map back to the *other* double (the lower neighbour). The shortest string that identifies the upper one takes 17 significant digits: `0.30000000000000004`. That trailing `4` isn't noise. It's the shortest way to tell the two doubles apart.

Seeing the error at all is the exception. Most of the time the rounding stays hidden below the printed digits. For example, `0.1 + 0.7` happens to print `0.7999999999999999`, but `0.1 + 0.4` prints `0.5`, because the rounding happened to land on the double nearest 0.5.

## 6. Why computers use binary floating point anyway

- **Speed and hardware:** binary arithmetic is what the circuits do natively. Doubles are added and multiplied in a few nanoseconds by dedicated hardware.
- **Range:** the exponent lets one 64-bit format hold numbers from about 10⁻³⁰⁸ to 10³⁰⁸.
- **Bounded, predictable error:** IEEE 754 guarantees that each basic operation (+, −, ×, ÷, √) gives the exact result *correctly rounded* to the nearest double. The relative error per operation is at most about 1.1 × 10⁻¹⁶. That's far more precision than almost any physical measurement has.

The cost is the one you've seen: decimal fractions that look simple to us are not simple in base 2.

## 7. What to do about it

**Don't compare floats with `==`** when they come out of a calculation. Check whether they are *close enough*:

```python
import math
math.isclose(0.1 + 0.2, 0.3)          # True (default relative tolerance 1e-9)
abs((0.1 + 0.2) - 0.3) < 1e-9         # True, a hand-written version
```

What counts as "close enough" depends on your problem. A relative tolerance (a fraction of the numbers' size) usually works better than a fixed absolute one.

**For money and other exact decimal quantities, don't use binary floats.** Two common options:

- Store **integers in the smallest unit** (cents rather than dollars): `10 + 20 == 30` is exact.
- Use a **decimal type**, which stores digits in base 10: Python's `decimal.Decimal`, Java's `BigDecimal`, C#'s `decimal`, SQL's `NUMERIC`.

```python
from decimal import Decimal
Decimal("0.1") + Decimal("0.2") == Decimal("0.3")   # True
```

(Create the Decimal from the *string* `"0.1"`. `Decimal(0.1)` would faithfully copy the already-rounded binary value.)

**For exact rational arithmetic**, some languages provide fractions, such as Python's `fractions.Fraction(1, 10)`. They're slower, but never round.

**Whole numbers are safe.** Every integer up to 2⁵³ (about 9 × 10¹⁵) is stored exactly in a double, so integer arithmetic within that range has no rounding at all.

---

## Summary

- Binary can only write fractions with power-of-2 denominators exactly. 0.1, 0.2 and 0.3 are tenths and fifths, so they repeat forever in binary, like 1/3 does in decimal.
- A double keeps 53 binary digits, so each of those numbers is rounded to the nearest storable value. 0.1 and 0.2 round up slightly, and 0.3 rounds down slightly.
- Adding the rounded 0.1 and 0.2, then rounding the sum, lands one step above the stored 0.3. The two are different numbers, so `==` is false.
- That's correct IEEE 754 behaviour, not a bug. Compare with a tolerance, or use integers or decimal types when you need exact decimal results.
