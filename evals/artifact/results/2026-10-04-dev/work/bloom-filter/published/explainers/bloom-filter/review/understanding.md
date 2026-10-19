# Review: bloom-filter (prose, published tier)

## Probe (2026-10-04T150533)
Adopted 1, 2, 3, 6, 7, 8: worked derivation of p ≈ f^k, toy-vs-formula note, why best k is near half full, use case (filter before a slow lookup), fill and capacity terms, hash → position example. Declined: resize and identical-hash breaking cases (resizing went to Scope), byte-vs-bit slots, and the excess notes.

## Cold read, narrative
- Run 150725: 4 blocking (beats too terse: k undefined, "all 1 → probably seen" not said, derivation not spoken, close a placeholder). Rewrote every beat's "Said" as full sentences.
- Run 150831: no blocking. Adopted the short edge fixes (name p, (1 − 1/m)^m ≈ 1/e, 6.9 → 7, m and k fixed when overfilling, cut repeats).

## Cold read, prose (151003)
No blocking. Cut the "hash functions are deterministic" sentence and the estimate note; added reasons for best k ≈ half full and the 4.8-bit rule; reworded capacity. Declined: glosses for the Not-covered pointers (Scope only).

## Blind test, prose
- Run 151043: FAIL, 13/14 at 2; item 10 (why less memory) scored 1: the answer omitted the price. Fixed: "The price for the smaller memory is error" next to the memory numbers. Also unified the two answers' wording, added p = f for k = 1, and worked the 3× overfill number.
- Run 151208: PASS, all 14 items at 2.
- Remaining audit notes not applied: no derivation of the 2× (13.8%) figure, of the optimum f = 0.5 (needs calculus), or of the sizing formula (Scope pointer). Unified "new items" → "never-added items" after this run.
