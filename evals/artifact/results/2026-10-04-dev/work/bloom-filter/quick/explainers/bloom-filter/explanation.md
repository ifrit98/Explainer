# How does a Bloom filter remember what it has seen, and when does it get it wrong?

**A Bloom filter does not store the items. It stores a row of bits, and each item switches on a few of them. To ask "have I seen this?", you check the item's bits. If any bit is off, the answer is a sure "no". If all are on, the answer is "probably yes", because other items can switch on the same bits.**

## The parts

- A **bit array**: m bits, all 0 at the start.
- k **hash functions**. A hash function turns an item into a position from 0 to m − 1. The same item always gives the same position; different items give positions that look random.

## How it works

<!-- claim: mech-add-query -->
Take a toy filter with m = 10 bits and k = 2 hash functions.

1. **Add** an item: compute its k positions and set those bits to 1. "cat" gives positions 1 and 6. "dog" gives positions 3 and 6.
2. **Query** an item: compute its k positions and look at those bits. If any bit is 0, answer "no". If all are 1, answer "probably yes".

After adding cat and dog, the array is:

| position | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 |
|---|---|---|---|---|---|---|---|---|---|---|
| bit | 0 | **1** | 0 | **1** | 0 | 0 | **1** | 0 | 0 | 0 |

Query "owl": its positions are 3 and 5. Bit 5 is 0, so owl was never added: a certain "no".

## Why "no" is always right

<!-- claim: no-false-negatives -->
Adding an item only changes bits from 0 to 1. Nothing changes a bit back to 0. So every item you added still has all its bits set, and it always gets "probably yes".

This guarantee breaks if you try to delete. Suppose you remove cat by clearing bits 1 and 6. Dog also uses bit 6. Now a query for dog finds bit 6 at 0 and answers "no", which is wrong. For this reason, a plain Bloom filter does not support deletion.

## How "yes" can be wrong

<!-- claim: false-positive -->
Query "fox": its positions are 1 and 3. Cat set bit 1 and dog set bit 3. Both bits are 1, so the filter answers "probably yes" for an item it never saw. This is a **false positive**.

The filter cannot tell which item set a bit. As you add more items, more bits become 1, and an unseen item is more likely to find all its bits already on.

## How much memory, and how often wrong

<!-- claim: why-bits -->
With n items in m bits and k hash functions, the **false-positive rate** p (the fraction of unseen items that get "probably yes") is about:

p ≈ (1 − e^(−kn/m))^k

This formula assumes the hash positions are independent and uniform.
Store 1,000,000 web addresses of about 50 bytes each: as a normal set, about 50 MB. A Bloom filter with 9,600,000 bits (1.2 MB, or 9.6 bits per item) and k = 7 gives p ≈ 1%. So 1 in 100 unseen addresses gets a wrong "probably yes". The filter size depends on n and the accepted rate, not on item length.

<!-- claim: why-k -->
Why several hash functions? Each extra hash makes a false positive need one more lucky bit. But each extra hash also sets more bits to 1. At 9.6 bits per item:

| k | false-positive rate |
|---|---|
| 1 | 9.9% |
| 7 | 1% |
| 20 | 7% |

The best k is about (m/n) × ln 2, which is 9.6 × 0.69 ≈ 7 here.

The rate also depends on how full the filter is. Put 3,000,000 items into the same 1.2 MB filter, and p rises to about 43%. Choose m from the largest n you expect.

## When to use one

Use a Bloom filter in front of a slow lookup, such as a disk or a network call. A "no" lets you skip the slow lookup. A "probably yes" sends you to the slow lookup, which gives the true answer. A false positive then costs one wasted lookup, not a wrong result.

*Not covered: counting Bloom filters (they allow deletion by storing small counters instead of bits) and cuckoo filters.*
