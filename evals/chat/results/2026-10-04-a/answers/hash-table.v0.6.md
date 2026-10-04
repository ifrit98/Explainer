# Why is a hash table lookup fast on average, and when is it slow?

_v0.6_

# Why hash table lookups are fast on average, and when they are slow

**Short answer:** A hash table converts a key directly into an array position, so a lookup checks a few items instead of searching through all of them. A lookup becomes slow when many keys go to the same position, because the table must then compare those keys one at a time.

## The mechanism

Searching an unsorted list requires comparing the target with each item. With 1,000,000 items, a successful search needs about 500,000 comparisons on average.

A hash table avoids that search:

1. **Hash the key.** A *hash function* turns the key into a large integer. For example, `"cat"` might become `1234567`.
2. **Reduce it to an index.** Take the integer mod the array size *m*. With *m* = 8, `1234567 mod 8 = 7`.
3. **Check that slot only.** The key is in slot 7 or nowhere. Each array slot is called a *bucket*.

Steps 1 and 2 take the same time for 10 items or 10 million. Step 3 is the only part that can grow with the number of items.

## Why the average is constant

Two keys can map to the same bucket. This is a *collision*. Collisions cannot be avoided, so the real question is how many keys share a bucket.

The **load factor** α = n/m is the number of items divided by the number of buckets. If the hash function spreads keys uniformly, each bucket holds α keys on average. This follows mathematically from the uniform-hashing assumption.

The table keeps α bounded. When α passes a threshold (often 0.75), the table doubles *m* and moves every key to a new bucket. Because of this, the work in step 3 does not grow with *n*.

The cost of a lookup depends on α. This table uses open addressing with linear probing, which places a colliding key in the next free slot:

| α | Expected probes for a key that is absent |
|---|---|
| 0.5 | 2.5 |
| 0.75 | 8.5 |
| 0.9 | 50.5 |

Cost rises sharply as the table fills, so tables resize long before they are full.

## When it is slow

| Cause | What happens | Cost |
|---|---|---|
| **Bad hash function** | Keys cluster. For example, with `h(k) = k mod 8` and keys 0, 8, 16, 24, …, every key lands in bucket 0. | Worst case O(n): a list search again |
| **Adversarial keys** ("hash flooding") | An attacker chooses keys that all collide. In 2011, this attack slowed web servers that put request parameters in hash tables. | O(n) per lookup, O(n²) to insert n keys |
| **High load factor** | The table resizes late, or deleted entries fill an open-addressing table. | Grows as shown in the table above |
| **Resize** | The insert that triggers a resize moves all n keys. | O(n) for that one insert, but O(1) averaged over all inserts |
| **Expensive keys** | Hashing and comparing a 1 MB string reads 1 MB. "O(1)" counts key operations, not bytes. | O(key length) |

**Defenses.** Languages use seeded, randomized hash functions such as SipHash, so attackers cannot predict collisions. Java 8 also turns a crowded bucket into a balanced tree, which caps the worst case at O(log n).

**Scope.** This answer leaves out cache effects. For example, chaining follows pointers, which is slower in practice than probing a contiguous array, even when both take O(1) steps. It also leaves out perfect hashing and cuckoo hashing, which guarantee O(1) worst-case lookups for fixed or carefully managed key sets.
