# Why is a hash table lookup fast on average, and when is it slow?

_none_

## Why it's fast on average

A hash table turns a key into an array index:

```
index = hash(key) % capacity
```

Arrays support **O(1) random access**, so if the hash sends you to the right slot, you skip searching entirely. A lookup costs:

1. **Compute the hash.** This is constant time for fixed-size keys, or O(k) for a key of length k, such as a string.
2. **Jump to the bucket.** This is a single memory access.
3. **Compare against the few entries there.** This is needed because different keys can share a slot.

The average cost depends on the **load factor** α = n / capacity. With a good hash function, keys spread roughly uniformly, so each bucket holds about α entries. Hash tables keep α bounded, typically around 0.5–1.0, by **resizing**: when the table gets too full, they allocate a larger array (usually 2×) and rehash everything. A single resize costs O(n), but spread over the insertions that triggered it, the **amortized** cost per operation stays O(1).

Result: expected O(1) lookup, insert, and delete.

## When it's slow

**1. Many collisions (the worst case is O(n)).**
If many keys hash to the same slot, a lookup becomes a linear scan:
- **Separate chaining:** one bucket's linked list holds everything.
- **Open addressing:** long probe sequences form. Linear probing is especially prone to *primary clustering*, where occupied runs grow and merge.

Common causes:
- **A poor hash function.** Examples include hashing strings by length only, or using `x % capacity` when keys share a common factor with the capacity (e.g., all even keys with a power-of-two table).
- **Adversarial input (hash flooding).** An attacker who knows your hash function can craft keys that all collide, turning O(1) into O(n) per operation and O(n²) overall, which is a denial-of-service attack. This is why Python, Rust, and others use **randomized/keyed hashes** like SipHash. Java's `HashMap` converts long chains into balanced trees, capping the worst case at O(log n).

**2. A high load factor.**
In open addressing, the expected probes for an unsuccessful search grow roughly like 1/(1−α)². At α = 0.9 that is about 50 probes. Performance degrades sharply as the table approaches full.

**3. Resize spikes.**
Amortized O(1) still means an individual insert can take O(n) when it triggers a rehash. That matters for latency-sensitive systems. Some implementations rehash incrementally to avoid the pause; Redis is one example.

**4. Expensive hashing or comparison.**
Hashing a long string or a deep composite key costs O(k) every time. If equality checks are also expensive, collisions hurt even more. Caching hash values (Java's `String` does this) helps.

**5. Poor cache behavior.**
In the constant factors, chaining with linked lists causes pointer-chasing and cache misses. Open addressing with flat arrays tends to be much faster in practice. That is why modern designs like Swiss Tables (Abseil, Rust's `hashbrown`) use them.

**6. Operations hash tables aren't built for.**
Ordered iteration, range queries ("all keys between 10 and 20"), and min/max require scanning everything, O(n). A balanced BST or B-tree is the right tool there.

## Summary

| Case | Lookup cost | Cause |
|---|---|---|
| Average | O(1) expected | Good hash + bounded load factor |
| Worst | O(n) | All keys collide (bad hash or adversarial input) |
| Worst (treeified buckets) | O(log n) | Java 8+ `HashMap` mitigation |
| Single insert during resize | O(n) | Rehashing; still O(1) amortized |

The speed comes from converting a search problem into direct array indexing. The slowness appears whenever the hash stops spreading keys evenly.
