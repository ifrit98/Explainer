# Why is a hash table lookup fast on average, and when is it slow?

_v0.5_

A hash table is fast because it **computes** where a key lives instead of **searching** for it. It is slow when many keys compute to the same place.

## The mechanism

A hash table stores entries in an array of **buckets**. Each bucket is one slot in the array.

1. Run the key through a **hash function**, which turns any key into a large integer.
2. Reduce that integer to a bucket index, for example `hash % number_of_buckets`.
3. Go straight to that bucket and compare the key with the few entries stored there.

**Why not just search?** A plain list has to compare the key with entry after entry. With 1,000 entries, a successful lookup takes about 500 comparisons on average. A hash table skips the search. Step 2 picks the bucket directly, so only the entries in that one bucket need comparing.

## Why "on average": collisions and load factor

Two different keys can map to the same bucket. This is a **collision**. Collisions cannot be avoided, because there are more possible keys than buckets.

The **load factor** (α) is the number of entries divided by the number of buckets. It sets the expected work per lookup.

**Worked example (chaining, where each bucket holds a short list):** store 1,000 keys in 2,000 buckets, so α = 0.5.
- A lookup for a missing key checks about α = **0.5** entries on average.
- A lookup for a present key checks about 1 + α/2 = **1.25** entries.

Compare that with 500 for a plain list. The cost depends on α and not on the total number of entries. This holds if the hash function spreads keys evenly, which is an *assumption*. Under that assumption, the result is a *mathematical consequence*. It is why lookup is called O(1), or constant time, on average.

The table keeps α low by **resizing**. When α passes a threshold (often 0.75), the table doubles its bucket count and moves every entry. That single insert costs O(n), meaning time that grows with the number of entries n. The copies total 1 + 2 + 4 + … + n < 2n over all inserts, so the average cost per insert stays constant. This average over a sequence of operations is called **amortized** cost.

## When it is slow

| Cause | What happens | Numbers |
|---|---|---|
| **All keys collide** (bad hash, or adversarial keys) | One bucket holds everything, and lookup becomes a list scan | 1,000 keys in 1 bucket gives about 500 comparisons per successful lookup, the same as no hashing |
| **High load factor** (open addressing with linear probing, where a collision moves to the next free slot) | Occupied slots form clusters, so probes run longer | Failed lookup: about 2.5 probes at α = 0.5, about **50.5** at α = 0.9 |
| **Resize in progress** | The one insert that triggers the resize copies the whole table | O(n) for that operation, which is a latency spike even though the amortized cost is constant |
| **Expensive hash or compare** | Each step is "constant" but costly | Long string keys must be read in full to hash them |

**The guarantee, held and broken.** Hold: keys spread evenly at α = 0.5 give about 1.25 comparisons. Break: remove the even-spread assumption, for example with a hash that returns `len(key)` and keys that all have 8 characters. Every key lands in one bucket, and the cost becomes O(n). Attackers use this deliberately (*established fact*: "hash flooding" attacks on web servers, 2011). For this reason, many languages use randomized hash seeds, and Java converts long chains into balanced trees, which caps the worst case at O(log n).

## Summary

Lookup is fast because the hash function points straight at one bucket. If keys spread evenly and the load factor stays bounded, that bucket holds a constant number of entries on average. Lookup is slow when keys pile into the same buckets, because the table then degrades into a linear search.

**Out of scope:** cuckoo and Robin Hood hashing (bounded or smoothed probe lengths), cache effects (open addressing is often faster in practice than chaining, despite similar O-costs), and universal hashing (the formal basis for the "even spread" assumption).
