# Narrative: float-sum

## 1. Reader before and after

- **Before:** A technical reader: school mathematics, basic programming. Knows binary integers, decimals, fractions, powers, and `==`. Has seen `0.1 + 0.2` print `0.30000000000000004` or heard of it. Does not know how a float is stored.
- **After:** "0.1 and 0.2 cannot be stored exactly in binary, so the computer adds two nearby numbers; their sum rounds to a different number than 0.3 does."

## 2. Question and motive

- **Question:** Why is `0.1 + 0.2 == 0.3` false? Result in words: the computer never holds 0.1, 0.2, or 0.3. It holds the nearest binary numbers. The addition is correct, but the nearest number to the sum is one step above the nearest number to 0.3.
- **Why care:** `==` on decimals silently fails in prices, loops, and tests.
- **Why this approach:** ask what number the computer actually holds for `0.1`; everything follows from that.

## 3. Introduction ledger

| Reference | Means | Grounded by | Beat |
|---|---|---|---|
| double | the 64-bit binary format for decimal-point numbers | `x = 0.1` in Python or JavaScript | 2 |
| 53 bits | a double is a whole number below 2^53 times a power of two | 0.75 = 3 × 2^-2 | 2 |
| binary fraction / ends in binary | denominator is a power of two | 3/8 = 0.011 | 3 |
| stored value | the nearest double to the literal | stored 0.1 = 0.10000000000000000555 | 4 |
| error | stored value − written decimal | +5.55e-18 for 0.1 | 4 |
| gap, u | distance between neighboring doubles; u = 2^-54 near 0.3 | 0.3 sits between …595 u and …596 u | 4 |
| exact sum / rounded sum | before / after rounding the result of + | …595.5 u / …596 u | 5 |
| tie, round half to even | exactly halfway → the even whole number | …595.5 → …596 | 5 |
| printed value | shortest decimal that rounds back to the same double | "0.1"; "0.30000000000000004" | 6 |

## 4. Beats

| # | Kind | Reader's question | Bridge | Shown | Said | Reader now knows |
|---|---|---|---|---|---|---|
| 1 | hook | Why is it false? | — | `0.1 + 0.2 == 0.3` → false; prints 0.30000000000000004 | "The computer never holds 0.1, 0.2, or 0.3. It holds the nearest binary numbers. The addition is correct, but the sum rounds to the number one step above the one that 0.3 rounds to." | the result in words |
| 2 | instance | What does the computer hold for `0.1`? | so | 0.75 = 3 × 2^-2 | "In Python, JavaScript, and most languages, a literal like 0.1 becomes a double: a whole number below 2^53 times a power of two. The whole number has at most 53 binary digits." | the format |
| 3 | mechanism | Can 0.1 be written that way? | but | 1/3 = 0.3333… in decimal; 3/8 = 0.011; 1/10 = 0.000110011… in binary | "A whole number times a power of two is a fraction whose denominator is a power of two. 1/10 has a factor 5 in its denominator, so it repeats forever in binary, as 1/3 does in decimal. The computer must round it." | 0.1 must be rounded |
| 4 | mechanism | How far off is it, and which way? | therefore | table: exact and stored values counted in u; errors | "Neighboring doubles are one gap apart. Between 0.25 and 0.5 the gap is u = 2^-54 ≈ 5.55e-17; for numbers half as big the gap halves (u/2 for 0.2, u/4 for 0.1). Count each number in u: 0.3 is 5404319552844595.2 u, between doubles at …595 and …596; nearest is …595, so 0.3 rounds down. 0.1 and 0.2 round up. The error is stored value minus decimal." | the three stored values |
| 5 | mechanism | Then what does + do? | so | 1801439850948198.5 + 3602879701896397 = 5404319552844595.5 → 5404319552844596 | "+ first finds the exact sum of the two stored values, then rounds it to a double, like every arithmetic operation. The exact sum is exactly halfway between …595 and …596: a tie. The rule sends ties to the even whole number, …596. Stored 0.3 is …595, one gap below." | why == is false |
| 6 | objection | Why does print(0.1) show 0.1? | but | "0.1" vs "0.30000000000000004" | "Printing shows the shortest decimal that rounds back to the same double. '0.1' rounds back to stored 0.1. '0.3' rounds back to …595, not …596, so the rounded sum needs 17 digits." | printing hides the error |
| 7 | test | Does it always fail? | so | 0.5 + 0.25 == 0.75 → true; Python Decimal('0.1') + Decimal('0.2') == Decimal('0.3') → true | "Doubles are exact when every denominator is a power of two. Decimal types store base-10 digits, where 1/10 ends." | when it holds |
| 8 | close | What do I do? | therefore | `abs(a - b) < 1e-9`; money in whole cents | "Compare with a tolerance much larger than the gap but smaller than any difference you care about. For money, count whole cents as integers, or use a decimal type." | the fix |

## 5. Concrete to symbol

u is introduced as "the gap near 0.3, 2^-54 ≈ 5.55e-17" with the instance 0.3 × 2^54 = 5404319552844595.2.

## 6. Links between representations

Each row of the table pairs the value in u with the decimal value; the prose names the row.

## 7. Close the loop

- **Answer:** The computer adds the nearest doubles to 0.1 and 0.2, not 0.1 and 0.2. Their exact sum rounds to the double above 0.3, while 0.3 itself rounded to the double below.
- **General argument:** any decimal whose denominator has a factor 5 is rounded; sums of rounded numbers can round to a different neighbor than the rounded decimal sum.
- **Payoff:** predict when `==` is safe; use tolerance or decimal types. Scope pointers.
