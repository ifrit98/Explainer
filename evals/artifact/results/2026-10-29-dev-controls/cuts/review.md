# Review of the cuts, before the controls run

Each diff was read against the PRD-002a cut rule: the removed text states the cut block or lets the reader recover it, nothing more is gone, and the rest is unchanged. Written before any reading or grading of the cut copies.

| subject | cut | result | attempts | review |
|---|---|---|---|---|
| bloom-filter | B1 | fail (dropped) | 3 | The checker judged the block recoverable every time: the worked example, the false-positive maths and "a 0 proves the item is absent" all imply that adding sets bits to 1 and never clears them. |
| float-sum | B1 | pass | 1 | Accepted. Removed the prime-factor rule, "integer × power of 2" and its table column, "only the power of 2 changes", and the sentence on power-of-2 denominators. |
| greenhouse | B1 | pass | 1 | Accepted. About 500 words removed, every sentence naming or resting on the emission level. B2 (raising the emission height cuts outgoing radiation) is mostly gone with it, because it presupposes B1; B2 is not in the clean set. |
| heat-pump | B2 | pass | 3 | Accepted. Removed the entropy derivation, the bound, and the worked ratios (318/50, 318/70, 308/40). |
| key-exchange | B3 | pass | 2 | Accepted. Removed "hard to undo", the section on why Eve cannot do the same, and summary step 4. B1 and B2 intact. |
| two-tides | B2 | pass | 1 | Accepted. Removed the Sun-to-Moon ratio and the spring and neap sentences. The cutter also added one sentence restating B1 for the Sun, beyond rewording where a removal broke a sentence; it does not carry B2. |

## What the cuts left that a reader might use

No cut was redone: none removed more than its block. Under-cutting is what the leak check after the run is for, and a failed redo would have dropped a subject below the floor of five.

- **heat-pump.** The table still pairs a 318 K condensing temperature and a 50 K lift with an ideal COP of 6.4 (and a 70 K lift with 4.5), a numeric path back to T_hot ÷ (T_hot − T_cold).
- **key-exchange.** The headings "hide the private number with multiplication / with exponentiation" and "So multiplication fails" imply that exponentiation cannot be undone.
- **float-sum.** "Here 1/2, 1/4, and 3/4 are all grid points" in section 6.
- **two-tides.** "Because the effect goes as 1/d³" stays; with remembered masses and distances it leads to the ratio.

## The floor

Five cuts pass, exactly the floor. A confirmed leak in any of them leaves four counted, and the verdict is then inconclusive whatever the catches.
