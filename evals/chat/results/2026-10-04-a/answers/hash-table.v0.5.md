# Why is a hash table lookup fast on average, and when is it slow?

_v0.5_

# Hash table lookups: why they are fast on average, and when they are slow

**Short answer:** A hash table computes where a key is stored, so it does not search for it. A lookup costs about the same with 10 keys or 10 million keys. This holds only if the hash function spreads keys evenly and the table stays sparse. When many keys land in the same place, a lookup degrades to a scan of every key.

## How a lookup works

A hash table is an array of **buckets** (slots). A **hash function** converts a key to a number. The table uses that number to pick a bucket.

1. Compute `h = hash(key)`.
2. Compute the bucket index: `i = h mod m`, where `m` is the number of buckets.
3. Go directly to bucket `i`.
4. Compare the key with each key stored in that bucket. Stop at a match.

Steps 1–3 take a fixed amount of work for any table size. Only step 4 can grow.

**Worked example.** Take 8 buckets and the key `"cat"`. Suppose `hash("cat") = 1,000,003`. Then `1,000,003 mod 8 = 3`, so the table looks in bucket 3 only. If bucket 3 holds one other key, the lookup does at most 2 comparisons.

## Why this is fast

The simpler alternatives must search. The hash table jumps to the right place.

| Method | Comparisons to find 1 key among 1,000,000 |
|---|---|
| Unsorted list, scan | about 500,000 on average |
| Sorted array, binary search | about 20 (log₂ 1,000,000) |
| Hash table, keys spread evenly | about 1–2 |

The number that controls step 4 is the **load factor**, α = keys ÷ buckets.

- **α = 0.5** (1,000 keys, 2,000 buckets): a bucket holds 0.5 keys on average, so a lookup checks about 1 key.
- **α = 5** (10,000 keys, 2,000 buckets): a bucket holds 5 keys on average, so a lookup checks several keys.

To keep α small, the table **resizes**. When α passes a threshold (often 0.75), the table allocates about twice as many buckets and moves every key. Because the table doubles each time, the total resize work spread over all inserts is a constant per insert. So the expected lookup cost stays constant as the table grows. Computer scientists write this as **O(1) on average**.

**Assumption:** "on average" means that the hash function spreads the keys evenly over the buckets. This is an assumption about the hash function and the input. It is not a guarantee.

## When a lookup is slow

### 1. Many keys collide in one bucket (the main failure)

A **collision** occurs when two keys go to the same bucket. A few collisions are normal. Many collisions remove the benefit.

- **Holds:** keys 1, 2, 3, …, 1000 with `hash(k) = k`, and 100 buckets. `k mod 100` spreads the keys 10 per bucket. A lookup checks at most 10 keys.
- **Breaks:** keys 100, 200, 300, …, 100,000 with the same hash and the same 100 buckets. Every key gives `k mod 100 = 0`, so all 1,000 keys go to bucket 0. A lookup can check all 1,000 keys. This is the same cost as an unsorted list, or **O(n)**.

Collisions like this come from two sources:
- **A weak hash function** that ignores part of the key, or that matches a pattern in the data, as in the example.
- **An attacker** who knows the hash function and sends keys chosen to collide. This is a real denial-of-service technique against web servers.

Mitigations: use a strong hash function with a random secret seed (Python and Rust do this with SipHash). Or store large buckets as balanced trees (Java's `HashMap` does this), which limits the worst case to about log₂ n comparisons.

### 2. The table is too full

If a table does not resize, α grows and every bucket gets longer. Some tables use **open addressing**: they store keys directly in the array and step to the next slot on a collision. In those tables the cost rises sharply as the array fills. For **linear probing** (stepping one slot at a time), the expected number of slots that a failed lookup checks is about ½(1 + 1/(1 − α)²) (an established result, from Knuth):

- α = 0.5 → about 2.5 slots
- α = 0.9 → about 50 slots

This is why tables resize well before they are full.

### 3. One insert triggers a resize

A resize moves every key, so that single insert costs O(n). The average per insert stays constant, but one operation can stall. This matters in latency-sensitive code. Lookups themselves are not slowed.

### 4. The constant is large

"Constant time" does not mean "cheap." A lookup must hash the whole key and compare whole keys. With a 10 KB string key, both steps read 10 KB. A chained table also follows pointers to scattered memory, and each cache miss can cost more than many comparisons. For small collections, a plain array scan is often faster in practice.

## Summary

| Condition | Lookup cost |
|---|---|
| Good hash, α kept small by resizing | about 1–2 comparisons, O(1) average |
| High load factor, no resize | grows with α, very steep near full with open addressing |
| Most keys in one bucket (weak hash or attack) | O(n), same as a list |
| Same, with tree buckets | O(log n) |

**Not covered here:** how specific hash functions work, other open-addressing schemes (quadratic probing, double hashing, cuckoo, Robin Hood), and the formal proof of the average-case bound. A standard algorithms text (CLRS, Chapter 11) covers all three.
