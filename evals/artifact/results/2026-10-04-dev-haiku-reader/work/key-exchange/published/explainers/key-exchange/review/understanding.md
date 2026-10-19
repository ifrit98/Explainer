# Review record: key-exchange (Published tier, Stage 1 prose)

## Checks run

| Check | Result |
|---|---|
| `explainer check key-exchange` | ok (final) |
| Probe (`2026-10-04T145920-probe`) | 16 findings; adopted 1 2 3 6 7 8 10 12 14 15 (two private numbers needed, Eve-shortcut assumption, multiplication case made concrete, remainder rule instance, range of a/b, one name per concept, 2^112 estimate, hash/quantum moved to Scope) |
| Cold read, narrative (`150134`) | 5 blocking (terse beats, remainder rule, unclear multiplication case, placeholder close): all fixed in narrative.md |
| Cold read, prose (`150411`, `150625`, `150725`) | round 2 had 1 blocking (mod used before defined, from a round-1 fix): fixed. Round 3: no blocking |
| Blind test, prose | runs `150452` PASS 15/15; `150823` item 12 = 1 (question asked for numbers, rubric wanted reason: question widened); `150941` item 13 = 1 (prose now links "find a or b" to discrete logarithm); `151044` item 10 = 1 (terse correct answer; grader variance); `151159` item 13 = 1 (question narrower than rubric: widened); final run PASS 15/15 |
| Broken copy (mod "only keeps numbers small"; exchange "proves identity") | FAIL — the test can fail |

## Declined findings (edge)

- Why p must be prime, in full: one line in Scope only.
- Where 2^112 comes from; how the faster discrete-log methods work: labeled estimate, out of scope.
- How Euclid's algorithm works: named as a fast standard method; detail not needed for the argument.
- Why scrambled outputs imply no fast reverse: stated as the assumption it is.
- Scope names (AES, elliptic curves, quantum): kept as pointers.

## Rule learned

A quiz `ask` must request everything its rubric `expect` requires (the reason, not only the numbers); two failures came from asks narrower than their expects.
