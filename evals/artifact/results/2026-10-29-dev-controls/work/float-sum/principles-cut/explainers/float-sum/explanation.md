# Why 0.1 + 0.2 is not 0.3

In Python, JavaScript, Java, C, and most other languages:

```python
>>> 0.1 + 0.2
0.30000000000000004
>>> 0.1 + 0.2 == 0.3
False
```

**Short answer:** the computer cannot store 0.1, 0.2, or 0.3 exactly. It stores the nearest value it can hold. The sum of the stored 0.1 and the stored 0.2 lands on a different stored value than the stored 0.3. This is not a bug. It is how the standard number format works, and the same thing happens with decimals on paper.

This matters because equality tests on decimal fractions fail silently, and money calculations drift by fractions of a cent.

## 1. The same problem in decimal

Imagine a calculator that keeps only 4 decimal digits.

- 1/3 is stored as 0.3333 (rounded down).
- 2/3 is stored as 0.6667 (rounded up).
- 1/3 + 1/3 = 0.3333 + 0.3333 = 0.6666.

So on this calculator, 1/3 + 1/3 ≠ 2/3. Each number was rounded on its own, and the rounding errors do not cancel. Computers have exactly this problem, but in base 2, and 1/10 plays the role of 1/3.

## 2. Why 0.1 has no exact binary form

In base 10, 1/4 = 0.25 ends, but 1/3 repeats.

In base 2, the expansion of 1/10 repeats forever:

```
0.1 (decimal) = 0.0001100110011001100110011...  (binary, "0011" repeats)
```

The computer must cut this off somewhere, so it must round.

## 3. What the computer actually stores

Most languages use the **double** format (IEEE 754 binary64), which the processor supports in hardware. A double holds a limited number of binary digits, so the values a double can hold form a grid. Between 0.25 and 0.5, the grid step is 2⁻⁵⁴ ≈ 5.55 × 10⁻¹⁷. Every literal you type is rounded to the nearest grid point:

| You type | Exact stored value | Error |
|---|---|---|
| `0.1` | 0.1000000000000000055511151231… | slightly high |
| `0.2` | 0.2000000000000000111022302462… | slightly high |
| `0.3` | 0.2999999999999999888977697537… | slightly low |

Note that the stored 0.2 is exactly twice the stored 0.1. Doubling is exact in binary.

The errors already point in different directions. 0.1 and 0.2 are a little too high. 0.3 is a little too low.

## 4. The addition, step by step

Write everything in units of 2⁻⁵⁴, the grid step near 0.3:

- stored 0.1 = 1801439850948198.5 units
- stored 0.2 = 3602879701896397 units
- exact sum = **5404319552844595.5** units

The exact sum is not a grid point. The processor must round it again. It sits exactly halfway between two grid points:

```
          stored 0.3                         result
     5404319552844595      exact sum     5404319552844596
  ───────────●─────────────────○─────────────────●───────────
   0.29999999999999998890    0.30000000000000001665    0.30000000000000004441
                       ←— half a step —→←— half a step —→
```

For an exact tie, the IEEE 754 rule is **round half to even**: choose the grid point whose integer is even. 5404319552844596 is even, so the result goes up.

The result is therefore one grid step above the stored 0.3. The two doubles differ, so `==` returns `False`.

## 5. Why it prints as 0.30000000000000004

This step explains a common confusion: if 0.1 is not stored exactly, why does `print(0.1)` show `0.1`?

Languages print the **shortest decimal string that rounds back to the same double**. For the stored 0.1, the string `0.1` is enough, because no other double is nearer to 0.1. This hides the error.

For the result of the addition, `0.3` is not enough. The string `0.3` rounds to the other grid point, the stored 0.3. The shortest string that identifies the result is `0.30000000000000004`. The printed form reveals the error only because the error moved the value to a different grid point.

## 6. When addition is exact

Some additions are exact:

```python
>>> 0.5 + 0.25 == 0.75
True
```

Here 1/2, 1/4, and 3/4 are all grid points, so no rounding happens.

## 7. What to do in code

- **Compare with a tolerance**, not with `==`: `math.isclose(0.1 + 0.2, 0.3)` in Python, or `abs(a - b) < 1e-9` with a tolerance that suits your data.
- **Use integers for money**: store 10 cents as `10`, not `0.10`.
- **Use a decimal type** when the decimal digits must be exact: `decimal.Decimal("0.1")` in Python, `BigDecimal` in Java. These types store base-10 digits, so 0.1 is exact. They are slower than doubles.

## Summary

0.1, 0.2, and 0.3 each have a repeating binary expansion, so each is rounded to the nearest double. The stored 0.1 and 0.2 are slightly high and the stored 0.3 is slightly low. Their exact sum falls halfway between two doubles, and the tie rule rounds it up, one step above the stored 0.3. The values differ, so the comparison is false.

Not covered: 32-bit floats, special values (NaN, infinity), and how errors grow across long chains of operations.
