# Bloom filters: "have I seen this before?" in about 10 bits per item

**The short answer.** A Bloom filter does not store the items. It stores a row of bits. To add an item, it hashes the item to a few bit positions and sets those bits to 1. To check an item, it hashes the item the same way and looks at the same positions. If any of those bits is 0, the item was never added. If all of them are 1, the item was *probably* added. The bits for that item could also have been set by other items. That last case is the only way the filter is wrong. It can say "yes" to an item that it never saw. It never says "no" to an item that it did see.

**Why you would want this.** Suppose a database keeps keys on disk. A disk read is slow, and many lookups ask for keys that do not exist. A small Bloom filter in memory answers "definitely not here" for most of those lookups, so the database skips the disk read. A "probably here" answer costs one real disk read, and that read gives the true answer. So a rare wrong "yes" costs a little time. It never gives an incorrect result. Databases such as LevelDB, RocksDB, and Cassandra use Bloom filters in this way.

## The parts

- **Bit array**: `m` bits, all 0 at the start.
- **Hash function**: a function that turns an item into a number that looks random. The same item always gives the same number. Here, each hash gives a position from 0 to `m − 1`.
- **`k`**: the number of hash functions. Each item maps to `k` positions.
- **`n`**: the number of items added so far.

There are two operations:

1. **Add(x)**: compute the `k` positions for `x`. Set each bit to 1.
2. **Query(x)**: compute the `k` positions for `x`. If any bit is 0, answer "definitely not seen". If all bits are 1, answer "probably seen".

## A worked example

Use `m = 16` bits and `k = 3`. The hash outputs below are invented for the example. A real filter gets them from real hash functions.

| Step | Positions | Bits that are 1 after the step |
|---|---|---|
| Add "cat" | 1, 6, 11 | 1, 6, 11 |
| Add "dog" | 3, 6, 14 | 1, 3, 6, 11, 14 |

"cat" and "dog" share bit 6. That sharing is normal, and it is the source of every error.

Now query three items:

| Query | Positions | Bits at those positions | Answer | Correct? |
|---|---|---|---|---|
| "cat" | 1, 6, 11 | 1, 1, 1 | probably seen | yes, "cat" was added |
| "fox" | 2, 6, 11 | **0**, 1, 1 | definitely not seen | yes |
| "owl" | 1, 3, 14 | 1, 1, 1 | probably seen | **no: false positive** |

"owl" was never added. Its three bits were set by "cat" (bit 1) and "dog" (bits 3 and 14). The filter has no record of *which* item set a bit, so it cannot tell the difference.

## Why it never misses an item it saw

Add only changes bits from 0 to 1. Nothing changes a bit back to 0. When you add `x`, its `k` bits become 1, and they stay 1. A later query for `x` computes the same `k` positions, finds all 1s, and answers "probably seen". So a **false negative** (a "no" for an item that was added) cannot happen.

**Where this guarantee breaks.** The guarantee depends on "nothing clears a bit". Suppose you try to delete "cat" by clearing bits 1, 6, and 11. Bit 6 also belongs to "dog". A query for "dog" now finds bit 6 = 0 and answers "definitely not seen", which is wrong. For this reason a basic Bloom filter does not support delete. (A *counting Bloom filter* stores a small counter in place of each bit, so it can delete. It uses about 4 times the memory.)

## Why so little memory

A normal set stores each item. One million URLs of about 50 bytes each need about 50 MB, plus the overhead of the set structure. A Bloom filter stores only bits, and the number of bits does not depend on the size of an item. With 1 million items and a 1% false-positive target, the filter needs about 9.6 bits per item: about 1.2 MB in total. A long URL and a short URL cost the same.

The price is that the filter can only answer the membership question. It cannot list its items, count them, or give back an item.

## How often it is wrong

Each false positive happens when all `k` bits of a new item are already 1. So the error rate depends on how full the array is.

**Assumption:** each hash position is uniform and independent of the others. Good hash functions come close to this.

One hash sets one specific bit with probability `1/m`. After `n` adds, there were `k·n` bit-sets. The chance that a given bit is still 0 is

```
(1 − 1/m)^(k·n)  ≈  e^(−k·n/m)
```

The query for an item that was never added checks `k` bits. It is a false positive if all `k` of them are 1:

```
false-positive rate  p  ≈  (1 − e^(−k·n/m))^k
```

(This is a mathematical consequence of the assumption above, and it is a very close approximation for large `m`.)

**Example.** `m/n = 10` bits per item, `k = 7`. Then `k·n/m = 0.7`, and `e^(−0.7) = 0.497`. So about half the bits are 1. Then `p ≈ 0.503^7 ≈ 0.0082`, which is 0.82%: about 1 wrong "yes" in 120 queries for absent items.

### Why use several hash functions, not one

The simplest design uses one hash (`k = 1`). With 10 bits per item, that gives `p = 1 − e^(−0.1) ≈ 9.5%`. More hashes make each item's "fingerprint" harder to fake by accident. But each hash also sets more bits, so the array fills faster. These two effects pull in opposite directions:

| `k` (10 bits per item) | 1 | 2 | 4 | 7 | 10 | 20 |
|---|---|---|---|---|---|---|
| false-positive rate | 9.5% | 3.3% | 1.2% | **0.82%** | 1.0% | 5.5% |

The best value is `k = (m/n)·ln 2`, which is about 7 here. At that value, about half of the bits are 1. The array then carries as much information as possible: a bit is equally likely to be 0 or 1.

### What happens when the filter fills up

The size `m` is fixed when you create the filter. If you add more items than planned, the error rate climbs fast. Take `m` = 10 million bits (1.25 MB) and `k = 7`:

| items added `n` | 0.5 million | 1 million | 2 million | 5 million |
|---|---|---|---|---|
| false-positive rate | 0.02% | 0.82% | 14% | 81% |

At 5 million items, almost every bit is 1, so almost every query answers "probably seen". The filter then gives almost no information. The bits cannot be resized, because the filter does not keep the items it would need to hash again. So choose `m` from the largest `n` you expect.

### Sizing rule

For a target rate `p`, you need

```
bits per item  m/n  =  −ln(p) / (ln 2)²   ≈  1.44 · log2(1/p)
```

| target `p` | 10% | 1% | 0.1% |
|---|---|---|---|
| bits per item | 4.8 | 9.6 | 14.4 |
| best `k` | 3 | 7 | 10 |

Each 10× drop in the error rate costs about 4.8 more bits per item.

## Summary

A Bloom filter maps each item to `k` positions in a bit array and sets those bits. A query checks the same positions. A 0 proves the item is absent. All 1s mean "probably present", because other items can set the same bits. That shared use of bits is what makes the filter small, and it is also what makes it wrong sometimes. The error is one-sided (false "yes", never false "no"). Its rate depends only on bits per item and `k`, and about 10 bits per item gives about 1%.
