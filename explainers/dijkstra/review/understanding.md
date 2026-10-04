# Blind understanding test — dijkstra, video

Run 2026-10-04 with `explainer quiz dijkstra --rendering video`. The reviewer was a fresh agent that saw only `captions.srt` and `review.png` (one frame per narration line, with the spoken text).

| Item | Score | Answer (short) |
|---|---|---|
| 8 · B first 4, final 3? | 2 | after C settles at 2, A→C→B = 2 + 1 = 3 < 4 |
| 9 · settled after D? | 2 | E at 10: smallest unsettled estimate (E 10, F 14) |
| 10 · assumption | 2 | lengths ≥ 0; otherwise a settled distance can be too large |
| General 1–7 | 1–2 | item 4 partial: the video names no single variable to vary |
| **Result** | **pass** | |

## Gaps the reviewer reported (open)

- The finality argument is spoken over a static frame. Show the settled region and one competing path that leaves through an unsettled node, with numbers.
- The video does not show what goes wrong with a negative length. A one-edge counterexample would show it.
- "Relax" is used in the on-screen rule but not defined in the narration.

## Re-test after v0.3.0 (completeness)

Run 2026-10-04 on the re-rendered video (main run plus the negative-edge chapter), with the claim questions added (items 11–12).

| Item | Score | Answer (short) |
|---|---|---|
| 8 · B 4 → 3 | 2 | via C: 2 + 1 = 3 < 4 |
| 9 · after D | 2 | E at 10, the smallest unsettled estimate |
| 10 · assumption | 2 | lengths ≥ 0; with C→B −2, B settles at 2 but the true distance is 1 |
| 11 · why smallest (claim `why-smallest`) | 2 | settling B at 4 when A reached it would be wrong; via C it costs 3 |
| 12 · finality with numbers (claim `guarantee-final`) | 2 | B at 3 while D 10, E 12, F ∞; the negative-edge graph as the counterexample |
| **Result** | **pass** | |

Closed: the finality argument now has this run's numbers on screen; the negative-edge counterexample is shown; "relax" is defined in the narration. Still open: the narration uses "distance" and "estimate" for the same thing; the finality segment is quick (about ten seconds).

## Re-tests in v0.4.0 (terms, pace, audit)

Run 2026-10-04 on the re-rendered video. The narration now uses "estimate" for the value that can still drop and "distance" only for the final value; the finality argument is three lines, one step per picture; the reviewer also returns an audit.

| Item | Round 1 | Round 2 | Answer (short) |
|---|---|---|---|
| 8 · B 4 → 3 | 2 | 2 | via C: 2 + 1 = 3 < 4 |
| 9 · after D | 2 | 2 | E at 10 < F 14 |
| 10 · assumption | 2 | 2 | lengths ≥ 0; with C→B −2 the algorithm answers 2, the true distance is 1 |
| 11 · why smallest (`why-smallest`) | 2 | 2 | B at 4 would be wrong; via C it costs 3 |
| 12 · finality (`guarantee-final`) | 2 | 2 | round 2: any other path leaves {A, C} through D (≥ 10) or E (≥ 12); plus the negative-edge graph |
| **Result** | **pass** | **pass** | |

Closed from v0.3.0: one word per concept; the finality segment is no longer rushed (no pace issues).

Round 1 audit, fixed before round 2: the "settled" box held B while the narration argued about paths leaving it, F was named as an exit, and "reaching D costs at least its estimate" was unstated (the model had the same flaw). Also added: A is the start node, infinity means no path found yet, edges work both ways, every relaxation's sum, the length rule on screen.

Round 2 audit, fixed after it (not re-tested): why each estimate is already the cheapest route through settled nodes (every settled node has relaxed its edges); why F is not an exit (no edge to A or C); the negative-edge graph is directed.

Open: the predict card covers the estimates a viewer needs to answer; the colors are not explained; the relax test on screen uses u and v, which the narration does not name; Bellman-Ford is named without a why (a scope pointer).

## Cold read with excess (v0.6.0, video)

Run 2026-10-04 with the v0.6.0 cold read (reads as the audience in `model.md`, reports excess, marks blocking findings). The blind tests above passed; this read found a flaw in the main argument.

- **Blocking:** at 1:44 "reaching D costs at least ten" is false as said: at 2:01 D becomes eight through B. The bound holds only for paths that leave the settled nodes {A, C} without passing through B. Also blocking: "any other path to B must leave the settled nodes through D or E" has no reason (the direct edges A–B and C–B also leave the set, and B's estimate already counts them); "the cheapest way there through settled nodes" adds a qualifier to "estimate" without notice; "a settled estimate is the final distance" at 0:30 sounds like a definition, not a claim the video will prove.
- **Excess (about 12 s):** the D, E, F estimates read aloud again at 1:24; "the path through C costs two plus one" repeats 0:52; "its estimate is its final distance" repeats 0:30; "D is settled" repeats 2:07.
- **Edge:** visual conventions never named (orange estimate, green settled, yellow current); green and red each carry two meanings; u and v on screen are never said; the final distances other than F are never said; the counterexample is not tied to the step it breaks.

**Fixed (v0.6.0).** The argument now follows a path to its first node outside {A, C}: if that node is B, B's estimate already counts the path; if it is D or E, the path so far costs at least D's estimate (10) or E's (12). All four exit edges flash, then D and E. Relaxing B adds "the bound of ten held only for paths that leave A and C at D", so D = 8 no longer reads as a contradiction. The model had the same flaw and has the same fix. "A settled estimate is final" is now announced as a claim checked later. Cuts: the D, E, F estimates read aloud again, the repeated "two plus one", the repeated "its estimate is its final distance". 208 s → 203 s; no layout or pace issues.

The v0.4.0 fix of this argument introduced the flaw: it named D and E as the only exits and forgot that a path can leave {A, C} straight to B. The blind tests passed both versions; the v0.6.0 cold read, reading as a developer with no proof background, found it.
