# Semantic model: Bloom filter

> Source of truth. Every rendering (prose, diagram, page, video) derives from this file.
> If a rendering needs a new fact, add it here first.

## Central question

How does a Bloom filter answer "have I seen this before?" with little memory, and how can it be wrong?

## Audience and prior knowledge

A technical reader: school mathematics (powers, probability of independent events, e ≈ 2.718), basic programming (arrays, bits, functions, what a hash set is). New to Bloom filters. Knows that a hash function turns any input into a number that looks random, and that the same input always gives the same number; does not know how a Bloom filter uses several of them.

## Entities

| Entity | Definition (one sentence) | Status |
|---|---|---|
| bit array | A row of m bits, all 0 at the start; the only storage the filter has. | fact |
| hash function | A function that maps an item to one position in the bit array; the same item always gets the same position. | fact |
| k | The number of hash functions; each item gets k positions. | fact |
| m | The number of bits in the bit array. | fact |
| n | The number of items added so far. | fact |
| add | Set the item's k bits to 1. | fact |
| query | Look at the item's k bits; any 0 → "definitely not seen"; all 1 → "probably seen". | fact |
| false positive | The filter says "probably seen" for an item that was never added. | fact |
| false negative | The filter says "definitely not seen" for an item that was added. Impossible while bits only go 0 → 1. | mathematical consequence |
| false-positive rate p | The chance that a query for an item never added gives "probably seen". | mathematical consequence (under the random-hash assumption) |
| bits per item m/n | Memory spent per added item. | fact |

## Relationships

| From | Relationship (verb) | To | Notes |
|---|---|---|---|
| add | sets to 1 | k bits | never sets a bit to 0 |
| query | reads | the same k bits | same hash functions as add |
| other items' bits | can cover | all k bits of a new item | cause of false positives |
| n / m | raises | fraction of bits that are 1 | fuller array → more false positives |
| k | raises the bits each query checks, and raises the fill | p | two opposite effects → a best k |

## Dependencies (learning order)

1. Hash function gives a fixed position per item.
2. Bit array, add (k bits set to 1).
3. Query; the 0 → "definitely not" rule.
4. Why a 0 proves absence (bits never go back to 0).
5. False positive: all k bits set by other items.
6. Rate p, its dependence on m/n and k; best k.
7. What breaks: overfilling; deleting.

## Causal chain

```text
add item → its k bits become 1 → bits never become 0
  → a later query on the item finds all 1 → "probably seen" is always right for added items (no false negatives)
other items fill bits → a never-added item's k bits can all be 1 already → false positive
more items per bit → more 1s → higher p
```

## Temporal sequence

1. Start: m bits, all 0.
2. Add each item: compute k positions, set them to 1.
3. Query: compute k positions, read them.

## Quantities

- Toy: m = 16, k = 3. Positions are stipulated (stand-ins for hash outputs), numbered 0–15.
  - "cat" → 1, 6, 11. "dog" → 3, 9, 14. After both: bits 1, 3, 6, 9, 11, 14 are 1 (6 of 16).
  - Query "fox" → 2, 6, 14: bit 2 is 0 → definitely not seen. Correct.
  - Query "owl" → 3, 6, 11: all 1 (3 from dog; 6, 11 from cat) → probably seen. Wrong: false positive.
  - Estimate from the observed fill: (6/16)³ ≈ 0.053, about 5%. (The formula's average fill for m = 16, n = 2, k = 3 is 0.31, giving 3.1%; the toy positions were picked with no collisions, so the toy is fuller than average.)
- Hash output → position: a hash function gives a large number; take it mod m. Illustrative: h1("cat") = 3,141,593; 3,141,593 mod 16 = 9.
- Fill f: the fraction of bits that are 1.
- Formula (assumption: hash positions behave like independent uniform random choices):
  1. One bit-set misses a given bit with probability 1 − 1/m.
  2. n adds make kn bit-sets, so the bit is still 0 with probability (1 − 1/m)^(kn) ≈ e^(−kn/m). (Toy check: (15/16)^6 = 0.679 vs e^(−0.375) = 0.687.)
  3. So f ≈ 1 − e^(−kn/m).
  4. A never-added item gives a false positive when all k of its positions land on 1 bits: p ≈ f^k.
  - Main example m/n = 10, k = 7: kn/m = 0.7, e^(−0.7) = 0.497, f = 0.503, p = 0.503^7 = 0.0082.
- Use: put the filter in front of a slow exact lookup (disk, database, network). "Definitely not seen" skips the lookup; "probably seen" does the lookup, which settles the answer. A false positive costs one wasted lookup, never a wrong final answer. 1,000,000 queries for absent items at p = 0.82% → about 8,200 wasted lookups; at p = 40% → about 400,000.
- At m/n = 10 bits per item:
  - k = 1: p ≈ 9.5%
  - k = 7: p ≈ 0.82% (best; (m/n)·ln 2 = 6.9)
  - k = 20: p ≈ 5.5%
- Best k = (m/n)·ln 2. At best k, f ≈ 0.5. Why half: at k = 1, f = 0.095, but the query checks only one bit; at k = 20, f = 0.865, so almost every bit is 1 and a query rarely finds a 0. Between, more checks and a fuller array balance near f = 0.5. At best k, p ≈ 0.5^k = 0.6185^(m/n); this gives "each ~4.8 bits per item cuts p by 10×" (ln 10 / (ln 2)² = 4.79).
- Sizing: m = −n·ln p / (ln 2)². n = 1 M, p = 0.82% → m ≈ 10 M bits.
- Bits per item meaning: 5 bits/item (k = 3) → p ≈ 9.2%; 10 → 0.82%; 20 (k = 14) → about 0.0067%. Each extra ~4.8 bits per item cuts p by about 10×.
- Memory, 1 million items: 10 bits each = 10 million bits = 1.25 MB. Storing 1 million URLs of about 50 bytes each = about 50 MB (estimate; the URL length is assumed), before hash-set overhead.
- Overfill: filter sized for 1 million items (m = 10 million, k = 7). With 2 million items p ≈ 13.8%; with 3 million, p ≈ 40%.
- The memory does not depend on item size: a 2 KB document and a 5-byte word each cost the same k bit-sets.

## Alternative states

| State / scenario | What changes | Why |
|---|---|---|
| Overfilled (n above plan) | p rises from 0.82% to 40% at 3× | most bits become 1 |
| Delete by clearing bits | false negatives appear | a cleared bit can belong to another item |
| k too small | p high (k = 1: 9.5%) | each query checks only one bit |
| k too large | p high (k = 20: 5.5%) | each add sets many bits, the array fills |

## Why this form

| Operation | Simplest alternative | What the alternative breaks (with numbers) |
|---|---|---|
| store bits, not items | a hash set of the items | 1 million URLs ≈ 50 MB vs 1.25 MB for the filter at 0.82% |
| k > 1 hash functions | one hash function (k = 1) | at 10 bits/item: 9.5% false positives vs 0.82% at k = 7 |
| not too many hash functions | k = 20 | 5.5%: each add sets 20 bits, so the array fills up |
| never clear bits (no delete) | clear the k bits to delete | add owl too, delete cat by clearing 1, 6, 11 → owl's bits 6, 11 are 0 → "definitely not seen" for owl, which is in the filter |

## Concrete cases

| Claim | Holds here (numbers) | Breaks here, without its assumption (numbers) |
|---|---|---|
| "definitely not seen" is always correct (no false negatives) | cat → 1, 6, 11 set; query cat later finds all 1 | delete allowed: clearing cat's bits makes owl (added) read as absent |
| p ≈ (1 − e^(−kn/m))^k stays small | 1 M items, 10 M bits, k = 7: 0.82% | 3 M items in the same filter: 40% |
| mechanism: add/query | toy: cat, dog, fox, owl | — |

## Terms

- **bit array**: the m bits.
- **position**: an index into the bit array, 0 to m − 1, given by a hash function.
- **add**: set the k positions to 1. (Not "insert" or "store": the item itself is not kept.)
- **query**: read the k positions.
- **definitely not seen** / **probably seen**: the two answers.
- **false positive**: "probably seen" for an item never added.
- **false negative**: "definitely not seen" for an item that was added.
- **false-positive rate p**: low 0.0067% (20 bits/item) means almost never wrong; 0.82% (10 bits/item) about 1 in 120 never-added queries; 40% (overfilled) nearly useless.
- **bits per item m/n**: 10 in the main example.
- **fill f**: fraction of bits that are 1; 0.503 in the main example; near 0 the filter wastes memory, near 1 nearly every query says "probably seen".
- **capacity**: the n used to choose m and k (1 million in the main example). Overfilling = adding more than capacity.

## Epistemic status

- **Established:** the add/query rules; no false negatives without deletion.
- **Mathematical consequence (under an assumption):** p formula and best k, assuming hash positions act as independent uniform random choices. The formula is an approximation; the true rate is close for large m.
- **Estimated:** 50 bytes per URL.

## Confusion points

- "The filter stores the items" → it stores only bits; you cannot list or recover items.
- "It can say no wrongly" → no; a 0 bit proves the item was never added.
- "More hash functions is always better" → no; past (m/n)·ln 2 the array fills and p rises.
- "p is the chance an added item is reported wrongly" → p applies only to items never added.
- "Remove an item by clearing its bits" → causes false negatives.

## Scope

- **Out of scope:** counting Bloom filters (counters instead of bits, allow deletion) — search "counting Bloom filter".
- **Out of scope:** cuckoo filters, quotient filters — alternatives that support deletion.
- **Out of scope:** deriving k from two hashes (double hashing, Kirsch–Mitzenmacher) — how real code gets k positions cheaply.
- **Out of scope:** the exact (non-approximate) false-positive formula.
- **Out of scope:** growing a filter when n is unknown — changing m changes every position (hash mod m), so a resized filter gives false negatives; see "scalable Bloom filter".

## Why this form (representation)

Prose with one small bit-array table. The mechanism is a short sequence (add, query) and the failure is one case; a table of the toy array carries the picture. The parameter trade-off has three values, so a small table is enough; a slider page would add little.

## Representation decision

- **Stage:** 1
- **Reason:** sequential mechanism + one counterexample + a 3-row trade-off; a table in prose shows all of it.
- **Levels:** L1 what it answers / L2 add and query / L3 why no false negatives, why false positives, the rate / L4 sizing and limits.
