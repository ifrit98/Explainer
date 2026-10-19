# Narrative: bloom-filter

## 1. Reader before and after

- **Before:** a technical reader (school maths incl. probability of independent events and e; arrays, bits, hash functions, hash sets). Has never seen a Bloom filter.
- **After:** "A Bloom filter sets k bits per item and checks those k bits later; a 0 proves the item is new, but all 1s can come from other items, so 'yes' is only probable, and it gets less reliable as the array fills."

## 2. Question and motive

- **Question:** How can a program answer "have I seen this before?" for millions of items without storing them, and when is the answer wrong?
- **Result in words:** keep a row of bits; each item turns on a few of them. If any of an item's bits is off, it is definitely new. If all are on, it is probably not new, and the filter is wrong only in that direction, with a rate you choose by memory per item.
- **Why care:** 1 million URLs take about 50 MB; the filter takes 1.25 MB and is wrong 0.82% of the time, only toward "probably seen".
- **Why this approach:** a hash function already turns an item into a fixed number. Turn the number into a bit position and remember only that the bit was hit.

## 3. Introduction ledger

| Reference | Means | Grounded by (a concrete instance) | Beat |
|---|---|---|---|
| bit array, m | row of m bits, all 0 at the start | m = 16, positions 0–15 | 2 |
| position | index in the bit array, from hash mod m | 3,141,593 mod 16 = 9 | 2 |
| k | number of hash functions per item | k = 3 | 2 |
| add | set the item's k positions to 1 | cat → 1, 6, 11 | 2 |
| query | read the item's k positions | fox → 2, 6, 14 | 3 |
| definitely not seen / probably seen | the two answers | fox / owl | 3, 4 |
| false positive | "probably seen" for an item never added | owl | 4 |
| false negative | "definitely not seen" for an added item | owl after clearing cat | 5 |
| n | number of items added | 1 million | 6 |
| fill f | fraction of bits that are 1 | 0.503 | 6 |
| p | false-positive rate | 0.82% | 6 |
| m/n, bits per item | memory per item | 10 | 6 |
| capacity | the n the filter was sized for | 1 million | 8 |

## 4. Beats

| # | Kind | Reader's question | Bridge | Shown | Said | Reader now knows |
|---|---|---|---|---|---|---|
| 1 | hook | Why not just a hash set? | — | 50 MB vs 1.25 MB | "A hash set of 1 million URLs (about 50 bytes each) takes about 50 MB. A Bloom filter keeps no URLs: it keeps a row of bits that each URL turned on, 10 bits per URL, 1.25 MB. It answers 'definitely not seen' or 'probably seen', and only the second answer can be wrong." | what the filter promises |
| 2 | mechanism | What does it store? | So | 16-bit table after cat, dog | "Start with m = 16 bits, all 0, numbered 0–15. Use k = 3 different hash functions. Each gives a large number; take it mod 16 to get a position (3,141,593 mod 16 = 9). To add an item, set its 3 positions to 1. cat → 1, 6, 11. dog → 3, 9, 14." | add, m, k, position |
| 3 | mechanism | How does it answer? | Then | fox query | "To query an item, compute the same 3 positions and read them. If any bit is 0, the answer is 'definitely not seen'. If all are 1, the answer is 'probably seen'. fox → 2, 6, 14; bit 2 is 0, so fox is definitely not seen." | query, both answers |
| 4 | notice | Can it be wrong? | But | owl query | "owl → 3, 6, 11, never added. Bit 3 came from dog; bits 6 and 11 from cat. All are 1, so the filter says 'probably seen'. This wrong 'probably seen' is a false positive." | false positive |
| 5 | guarantee | Can it be wrong the other way? | Therefore | cat query; delete case | "The other error, a false negative, is 'definitely not seen' for an item that was added. It cannot happen, because add only sets bits to 1 and nothing sets them back. But suppose you try to delete cat by clearing 1, 6, 11, after adding owl for real. Owl's bits 6 and 11 are now 0, so owl reads 'definitely not seen': a false negative. Bits are shared, so a Bloom filter has no delete." | one-sided error and why |
| 6 | mechanism | How often is it wrong? | So | 4-step derivation, 10 bits/item | "Let n be the number of items added, and assume each hash position is a uniform random choice, independent of the others. One bit-set misses a given bit with probability 1 − 1/m. n adds make kn bit-sets, so the bit stays 0 with probability (1 − 1/m)^(kn) ≈ e^(−kn/m). So the fill f, the fraction of bits that are 1, is about 1 − e^(−kn/m). A never-added item is a false positive when all k of its positions are 1: p ≈ f^k. With n = 1 million, m = 10 million (10 bits per item, m/n = 10) and k = 7: kn/m = 0.7, f = 0.503, p = 0.503^7 = 0.82%." | n, f, p, m/n |
| 7 | approach | Why k = 7, not 1 or 20? | But | 3-row table | "At 10 bits per item: k = 1 gives f = 0.095 but checks only one bit, p = 9.5%. k = 20 makes f = 0.865, so nearly every bit is 1, p = 5.5%. k = 7 gives f ≈ 0.5, the balance, p = 0.82%. The best k is (m/n)·ln 2." | k trade-off |
| 8 | limit | What if I add too many? | And | 2× → 13.8%, 3× → 40% | "The filter was sized for a capacity of 1 million items. Add 2 million and p is 13.8%; 3 million, 40%. Added items still always read 'probably seen'." | capacity |
| 9 | payoff | What is it good for? | So | filter before disk | "Check the filter before a slow lookup on disk. 'Definitely not seen' skips the lookup, safely, because there are no false negatives. 'Probably seen' does the lookup, which gives the true answer. Of 1,000,000 queries for absent items, about 8,200 do a wasted lookup." | use |
| 10 | close | Answered? | — | — | "A Bloom filter remembers only the bits each item turned on. A 0 bit proves an item is new. All 1s mean 'probably seen', wrong at rate p, which rises as the array fills." | after-sentence |

## 5. Concrete to symbol

Toy first (m = 16, k = 3, two items), then the symbols m, k, n bound aloud, then the formula with m/n = 10, k = 7.

## 6. Links between representations

The toy table shows bit numbers above, 0/1 below, and which item set each bit.

## 7. Close the loop

- **Answer:** It keeps only bits each item turned on. A 0 proves "new"; all 1s mean "probably seen", wrong at rate p.
- **General argument:** bits only go from 0 to 1, so added items always pass; other items' bits can cover a new item, with probability f^k.
- **Payoff:** a cheap pre-check before slow lookups. Scope: deletion (counting Bloom filters), growing, k from two hashes.
