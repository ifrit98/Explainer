# Semantic model: Bloom filter

## Central question

How does a Bloom filter answer "have I seen this before?" with little memory, and how can it be wrong?

## Audience and prior knowledge

A technical reader: school mathematics (powers, e^x), basic programming (arrays, functions). Knows what a set is. Does not know what a hash function is in detail, or what a Bloom filter is.

## Entities

| Entity | Definition (one sentence) | Status |
|---|---|---|
| bit array | A row of m bits, all 0 at the start. | fact |
| hash function | A function that turns an item into a position 0..m−1; the same item always gives the same position, different items give positions that look random. | fact (assumed uniform) |
| add | Set the k bits at the item's k positions to 1. | fact |
| query | Check the item's k positions; "no" if any bit is 0, "probably yes" if all are 1. | fact |
| false positive | A "probably yes" for an item that was never added. | fact |

## Causal chain

```text
item → k hash functions → k positions → (add: set to 1) / (query: all 1? → probably yes; any 0 → no)
other items' bits overlap → all k positions 1 by chance → false positive
```

## Quantities

- m = number of bits; n = number of items added; k = number of hash functions.
- False-positive rate p ≈ (1 − e^(−kn/m))^k (assumes independent uniform hashes).
- Best k ≈ (m/n)·ln 2.
- n = 1,000,000, m = 9,600,000 bits (1.2 MB), k = 7 → p ≈ 1%. About 9.6 bits per item.
- Same data as a set of 50-byte strings: about 50 MB.
- Same m and n, k = 1 → p ≈ 9.9%. k = 20 → p ≈ 7%.
- Same m, k = 7, n = 3,000,000 → p ≈ 43%.

## Why this form

| Operation | Simplest alternative | What the alternative breaks |
|---|---|---|
| k hashes, not one | k = 1 | at 9.6 bits per item, p ≈ 9.9% instead of 1% |
| not too many hashes | k = 20 | array fills with 1s; p ≈ 7% |
| store bits, not items | a set of the strings | 50 MB instead of 1.2 MB for 1,000,000 items |

## Concrete cases

| Claim | Holds here | Breaks here |
|---|---|---|
| No false negatives | added "dog" → bits 3, 6 are 1 forever → query says probably yes | delete "cat" by clearing bits 1, 6 → bit 6 is 0 → "dog" gets "no" |
| False positives exist | "owl" → bits 3, 5; bit 5 is 0 → no | "fox" → bits 1, 3; both set by cat and dog → probably yes |

Worked example: m = 10, k = 2. cat → 1, 6. dog → 3, 6.

## Terms

- bit array, hash function, position, add, query, false positive, false-positive rate (p: 1% means 1 in 100 unseen items gets "probably yes"; at 43% the filter is close to useless).

## Epistemic status

- **Mathematical consequence:** no false negatives (bits only go 0 → 1).
- **Estimate:** the p formula; it assumes independent uniform hashes and is a close approximation.

## Confusion points

- "Probably yes" means certain → no; it can be a false positive.
- You can remove items by clearing bits → no; that creates false negatives.
- More hashes are always better → no; there is a best k.

## Scope

- **Out of scope:** counting Bloom filters (allow deletion); cuckoo filters; how to build k hashes from two (double hashing).

## Representation decision

- **Stage:** 1
- **Reason:** The mechanism is a short sequence of steps; one 10-bit worked example and one formula carry it. A static table shows the bit array.
- **Levels:** L1 what it answers / L2 add and query / L3 why errors are one-sided / L4 sizing.
