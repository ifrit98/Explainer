# Understanding tests: attention

Stage 3, published tier, built with the v0.6.0 process. Every number in the page's text is in `model.yaml`; the instrument computes the rest live from the same values.

## Blind test (page)

Run 2026-10-04 with the v0.6.0 prompt (reads as the audience; audits excess too). Every quiz item scored 2: the place query gives street 0.808; the mask gives "tired" weight 0 because a decoder may not look ahead; without √d the weights saturate (0.996 at d = 64); equal weights tie at 0.25; query = x ties at 0.313. No general item scored 0. **Pass.**

Real audit findings, fixed: "score" named both q · k and q · k / √d (so "scores 1 and 1, weights 0.313" did not reproduce); the softmax card's failure case did not fail (4, 0, 1, 0 divided by its sum is a valid set of weights); the four base scores of the √d demo were never shown; the output of "it" sums to 0.904 without saying why (the value of "it" is zero).

## Cold read (page)

Run 2026-10-04. **Blocking:** Level 1 was an instrument with no words: q, k, the coordinates (animate, place), score, d, and v were used before anything defined them; the prediction came before any of them; the output meter for street's value was labeled "place"; "vector length" for d read as the Euclidean length.

Fixed: two short paragraphs before the instrument name q, k, the coordinates, score, d, weight, and v, and the prediction now follows them and states the query as numbers; the output meters are labeled by token; d is "the number of entries in q and k"; the header states the problem (the vector of "it" is the same in every sentence); the mask gives its reason; the summary answers the "it" example in words; the footer meta line and the unargued "weights are not importance" line went.

Not applied (edge): numbers for x and W_Q; making the mask on by default; repeating less between the Level 1 notes and the Level 3 cards (the notes are live, the cards give the reason).
