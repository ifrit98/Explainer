# Bloom filters: "have I seen this before?" in a few bits per item

<!-- Stage 1, rendered from model.md in STE-80. -->

**A Bloom filter does not keep the items. It keeps a row of bits, and each item turns on a few of them. If any of an item's bits is still off, the answer is "definitely not seen". If all of them are on, the answer is "probably seen", because other items can turn on the same bits. So the filter can be wrong in one direction only: it can say "probably seen" for an item it never saw.**

<!-- claim: why-bits-not-items -->
The motive is memory. A hash set of 1 million URLs, at about 50 bytes per URL, takes about 50 MB. A Bloom filter for the same URLs takes 1.25 MB (10 bits per URL). The price for the smaller memory is error: the filter gives a wrong "probably seen" for 0.82% of URLs it never saw. The memory does not depend on how long the items are, because the filter never keeps them.

## How it works: add and query

<!-- claim: mechanism-add-query -->
Start with a **bit array** of m bits, all 0. In this small example, m = 16, with positions 0 to 15.

Choose k different hash functions; here k = 3. Take each hash output mod m to get a **position**. For example, a hash output of 3,141,593 gives position 3,141,593 mod 16 = 9. Each item thus gets k positions, one from each hash function.

To **add** an item, set its k positions to 1. Nothing else is kept. Add two items:

- cat → positions 1, 6, 11
- dog → positions 3, 9, 14

| Position | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 | 12 | 13 | 14 | 15 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Bit | 0 | **1** | 0 | **1** | 0 | 0 | **1** | 0 | 0 | **1** | 0 | **1** | 0 | 0 | **1** | 0 |
| Set by | | cat | | dog | | | cat | | | dog | | cat | | | dog | |

To **query** an item, compute the same k positions and read those bits:

- If any bit is 0, the answer is **definitely not seen**.
- If all bits are 1, the answer is **probably seen**.

Query fox → positions 2, 6, 14. Bit 2 is 0, so fox is definitely not seen. That answer is right.

## How it can be wrong: false positives

<!-- claim: mechanism-false-positive -->
Query owl → positions 3, 6, 11. Owl was never added. But bit 3 came from dog, and bits 6 and 11 came from cat. All three bits are 1, so the filter says "probably seen". A **false positive** is this error: "probably seen" for an item that was never added. The filter cannot tell owl from an added item, because it kept only bits, and bits do not record which item set them.

## Why it is never wrong the other way

<!-- claim: guarantee-no-false-negative -->
The other error, a **false negative**, is "definitely not seen" for an item that was added. A false negative cannot happen. Adding cat set bits 1, 6 and 11, and nothing ever sets a bit back to 0. So any later query for cat finds all three bits at 1.

This guarantee depends on bits never going back to 0. Suppose you add owl for real, and then try to delete cat by clearing bits 1, 6 and 11. Owl also uses bits 6 and 11, so they are now 0, and the filter says owl is definitely not seen. That is a false negative. Bits are shared between items, so a Bloom filter has no delete operation.

## How often it is wrong

<!-- claim: mechanism-rate -->
Let n be the number of items added. Assume that each hash position is a uniform random choice, independent of the others. Then:

1. Each time an add sets a bit, it misses a given bit with probability 1 − 1/m.
2. n adds set kn bits in total. So a given bit is still 0 with probability (1 − 1/m)^(kn). Because (1 − 1/m)^m ≈ 1/e for large m, this is about e^(−kn/m).
3. So the **fill** f, the fraction of bits that are 1, is about 1 − e^(−kn/m).
4. A never-added item gets k random positions. Each one is 1 with probability f. The **false-positive rate** p, the chance that a never-added item reads "probably seen", is the chance that all k are 1: **p ≈ f^k**.

Take n = 1 million items and m = 10 million bits: 10 bits per item (m/n = 10). With k = 7: kn/m = 0.7, e^(−0.7) = 0.497, so f = 0.503 and p = 0.503^7 = 0.0082, or 0.82%. That is about 1 wrong answer in 120 queries for never-added items.

<!-- claim: why-several-hashes -->
Why 7 hash functions? The number of hash functions k pulls in two directions, at 10 bits per item:

| k | Fill f | False-positive rate p | Why |
|---|---|---|---|
| 1 | 0.095 | 9.5% | Most bits are 0, but a query checks only one bit, so p = f. |
| 7 | 0.503 | 0.82% | About half the bits are 1; a query checks 7 of them. |
| 20 | 0.865 | 5.5% | Each add sets 20 bits, so almost every bit is 1. |

More hash functions make each query check more bits, but they also fill the array faster. Below half full, a query checks too few bits; above half full, almost every bit it checks is 1. The best balance is near f = 0.5, which the formula gives at k = (m/n)·ln 2, about 0.69 times the bits per item. Here 10 × 0.69 = 6.9, so k = 7. At the best k, p ≈ 0.5^k. Each extra bit per item adds 0.69 to k, so it multiplies p by 0.5^0.69 ≈ 0.62. Thus each extra 4.8 bits per item cuts p by about 10 times.

## Overfilling

<!-- claim: limit-overfill -->
The rate p stays at 0.82% only while n stays near the **capacity**: the number of items the filter was sized for. Keep the same filter (10 million bits, k = 7) and add more items. At 2 million items, p is 13.8%. At 3 million items, kn/m = 2.1, f = 1 − e^(−2.1) = 0.88, and p = 0.88^7 = 40%. The filter never forgets an added item, but its "probably seen" answer stops telling you much.

## What it is good for

<!-- claim: why-useful -->
Put the filter in front of a slow exact lookup, such as a database on disk. If the filter says "definitely not seen", skip the lookup; that is safe, because there are no false negatives. If the filter says "probably seen", do the lookup, which gives the true answer. A false positive thus costs one wasted lookup, never a wrong final answer. Of 1,000,000 queries for never-added items, about 8,200 do a wasted lookup at p = 0.82%; at p = 40%, about 400,000 do.

## Summary

A Bloom filter answers "have I seen this before?" by remembering only the bits each item turned on. A 0 bit proves an item is new. All 1s mean "probably seen", which is wrong at a rate p ≈ f^k that you choose with bits per item, and that rises when you add more items than the capacity.

## Not covered here

- **Deletion:** counting Bloom filters keep a small counter per position instead of a bit. Cuckoo filters are another option.
- **Growing:** changing m changes every position (hash mod m), so you cannot resize a filter in place. See "scalable Bloom filter".
- **Sizing:** for n items and a target p, m = −n·ln p / (ln 2)².
- **Cheap hash functions:** real code makes k positions from two hash values ("double hashing").
