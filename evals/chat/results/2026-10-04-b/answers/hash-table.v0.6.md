# Why is a hash table lookup fast on average, and when is it slow?

_v0.6_

A hash table is fast because it computes where a key lives instead of searching for it.

The table is an array of m slots, called buckets. A hash function turns the key into a number, and `hash(key) mod m` gives a bucket index. Reading an array slot by index takes the same time at any array size. A lookup is therefore one hash computation plus one jump, with no scan of the other keys.

Compare a sorted array with binary search. For 1,000,000 keys, binary search needs about 20 comparisons (log₂ 1,000,000 ≈ 20). A hash table needs about 1 or 2.

**Why "on average":** two keys can hash to the same bucket. This is a collision. With chaining, each bucket holds a short list, and a lookup scans that list. The average list length is the load factor α = n/m (keys per bucket). Example: 1,000 keys in 2,000 buckets gives α = 0.5. A successful lookup then checks about 1 + α/2 ≈ 1.25 keys. The table keeps α small by resizing. When α passes a threshold (often 0.75), the table doubles m and re-inserts every key. This keeps the cost constant as n grows.

**When it is slow:**

- **Many keys share a bucket.** A weak hash function, or input chosen by an attacker, can send all 1,000 keys to one bucket. A lookup then scans about 500 keys on average. This is a linear search, O(n). Some languages use randomized hash seeds to block this attack.
- **During a resize.** The insert that triggers a resize re-inserts all n keys. That one operation is O(n). Spread over all inserts, the cost is still O(1) each ("amortized"), but a single call can stall.
- **High load factor with open addressing.** Here a collision makes the lookup probe the next slots instead of a list. As the array fills, the probe sequences grow sharply.

A possible follow-up is how a good hash function spreads keys evenly.
