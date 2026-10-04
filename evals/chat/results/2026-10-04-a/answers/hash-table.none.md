# Why is a hash table lookup fast on average, and when is it slow?

_none_

## Why it's fast on average

A hash table turns a key into an array index:

1. **Hash the key**: a hash function maps the key to an integer, e.g. `hash("apple") → 2837461`.
2. **Reduce to an index**: `index = hash % capacity` (or a bitmask if capacity is a power of two).
3. **Jump straight there**: array access by index is O(1), because the address is computed with arithmetic rather than found by searching.

So no matter how many items the table holds, you don't scan them. You compute where the item *should* be and look there.

This only works if two conditions hold:
- **The hash function spreads keys evenly** across buckets.
- **The load factor stays bounded**. The load factor is items ÷ buckets. Tables resize, usually doubling, when it passes a threshold such as 0.75.

Under those conditions, each bucket holds about a constant number of items, so the expected lookup cost is **O(1)**.

## When it's slow

**1. Collisions pile up (worst case O(n))**
Different keys can land in the same bucket. Tables handle this in one of two ways:
- *Chaining*: each bucket holds a list.
- *Open addressing*: probe nearby slots.

If many keys collide, lookup degrades into a linear scan. In the extreme, when every key hashes to the same bucket, lookup is O(n).

Common causes:
- **A bad hash function**, e.g. one that hashes strings by length only, or ignores most of the key's bits.
- **Patterned keys interacting with the modulus**, e.g. keys that are all multiples of 16 in a table with 16 buckets.
- **Adversarial input (hash flooding)**: an attacker crafts keys that all collide in order to DoS a server. This is why languages like Python, Rust, and Ruby use randomized or keyed hashes such as SipHash. Java's `HashMap` instead converts long chains into balanced trees, capping the worst case at O(log n).

**2. Resizing**
When the load factor is exceeded, the table allocates a bigger array and rehashes every element, which is O(n) for that one insert. Amortized over all inserts it's still O(1), but individual operations can spike. That matters for latency-sensitive systems. Some designs resize incrementally to avoid it.

**3. High load factor with open addressing**
As the table fills, probe sequences get long. With linear probing, *clustering* makes runs of occupied slots grow and merge. Performance degrades sharply as the load factor approaches 1.

**4. Expensive hashing or comparison**
"O(1)" counts operations, not time. Hashing a 10 MB string or comparing deep objects for equality costs time proportional to their size. Some languages cache string hashes to soften this.

**5. Cache behavior**
Hash tables scatter data randomly in memory, so each lookup may be a cache miss. Chaining with linked lists is especially bad because of pointer chasing. For small n, a linear scan of a compact array can beat a hash table in practice. This is why modern designs such as Swiss tables (Abseil, Rust's `HashMap`) use flat, cache-friendly layouts with SIMD probing.

## Summary

| Situation | Lookup cost |
|---|---|
| Good hash, bounded load factor | O(1) expected |
| Many collisions (bad hash/adversarial keys) | O(n) worst case (O(log n) with treeified buckets) |
| Insert that triggers resize | O(n) for that op, O(1) amortized |
| Huge keys | O(key size) to hash/compare |

The O(1) is a *probabilistic, average-case* guarantee. It depends on the hash distributing keys well and the table staying sparse enough.
