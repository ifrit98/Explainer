# Model: why 0.1 + 0.2 != 0.3

Reader: technical, school maths, basic programming; new to floating point.

Central question: why does `0.1 + 0.2 == 0.3` give false?

Answer in one line: the computer stores each number as the nearest binary fraction,
and the three roundings (0.1, 0.2, and the sum) do not land on the same stored value as 0.3.

Entities
- double (IEEE 754 binary64): a 53-bit integer significand times a power of two.
- grid: the set of values a double can hold; near 0.3 the spacing is 2^-54.
- rounding: each literal and each operation result goes to the nearest grid point; ties go to the even significand.
- printing: languages print the shortest decimal that maps back to the same double.

Causal chain
1. 1/10 has a factor 5 in its denominator, so its binary expansion repeats (0.000110011...).
2. Storage rounds 0.1 and 0.2 slightly up; 0.3 is rounded slightly down.
3. The exact sum of the stored 0.1 and 0.2 lies exactly halfway between two grid points.
4. Round-half-to-even picks the upper point, one grid step above stored 0.3.
5. Shortest-round-trip printing shows that point as 0.30000000000000004.

Analogy: 4-digit decimal, 1/3 + 1/3 -> 0.3333 + 0.3333 = 0.6666, but 2/3 is stored as 0.6667.

Holds / breaks: 0.5 + 0.25 == 0.75 is exact (denominators are powers of 2).

Confusion points: "0.1 prints as 0.1, so it is stored exactly" (false: printing hides it);
"it is a bug in the language" (false: it is the hardware number format).

Scope: no float32, no NaN/infinity, no error analysis of long sums.
