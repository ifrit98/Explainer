# Narrative: odd-squares

> Pass 3. `model.md` says what is true. This file says the path a first-time viewer takes to it.
> The scene follows these beats. Check with `explainer coldread odd-squares --rendering narrative`.

## 1. Reader before and after

- **Before:** odd numbers, square numbers (1, 4, 9, 16, …), and school arithmetic. Nothing else counts as known: not a letter, not a name, not a color.
- **After:** "Each odd number is an L of tiles that grows a square by one, and each L is two bigger than the last, so the first n odd numbers fill an n by n square: they add up to n × n."

## 2. Question and motive

- **Question:** why do the odd numbers, added in order, always give a square number? The result is said in words in beat 2: the first n odd numbers add up to n × n.
- **Why care:** odd numbers and square numbers have no clear reason to be related, and five lucky cases prove nothing. A reason that works for every n is a proof.
- **Why this approach:** a square number is a square of tiles. Each sum adds one more odd number. So ask what one more odd number adds to a square of tiles. The answer is an L.

## 3. Introduction ledger

| Reference | Means | Grounded by (a concrete instance) | Beat |
|---|---|---|---|
| sum colors | each odd number has its own color | 1 blue, 3 teal | 1 |
| n | the count of odd numbers added; from beat 6, also the number of Ls and the side of the square (the same number) | for 1 + 3 + 5, n is 3 | 2, 6 |
| n × n | n times n | 3 × 3 = 9 | 2 |
| tile | one small unit square ("square" never means a tile) | the first tile on screen | 4 |
| side, "3 by 3" | a square with 3 rows of 3 tiles has side 3 | 9 tiles in 3 rows of 3 | 4 |
| L | the tiles that go around a square to make the next square: a row, a column, a corner. The first tile is the first L. | the 3 tiles around the first tile | 5 |
| L colors | each L has the color of its odd number in the sums | the second L and the 3, both teal | 5 |
| a term lights up | that number is the L being added | the 3 lights up as the second L appears | 5 |
| braces with 4, 4, 1 | the row, the column, and the corner of an L | the L around the 4 by 4 square | 7 |
| ⋯ | "and so on, in order" | 1 + 3 + 5 + ⋯ | 8 |
| ? on the rule card | not proved yet; it goes when the rule is proved | the card after beat 3 | 3, 8 |
| n² | n × n, said "n squared": n with a small two | 5² = 25 | 8 |
| 2n | two times n | n = 5: 10 | 12 |
| 2n − 1 | two times n, minus one: the size of the L that makes side n | n = 5: 9; n = 10: 19; n = 1: 1 | 12 |
| L shape | a column on the left and a row along the bottom, sharing the corner tile | the second L, 3 tiles | 5 |

## 4. Beats

| # | Kind | Reader's question | Bridge | Shown | Said | Reader now knows |
|---|---|---|---|---|---|---|
| 1 | hook | What happens when I add the odd numbers? | — | five sum rows; each odd number in its own color | Add the odd numbers in order, each in its own color: 1; 1 + 3 = 4; 1 + 3 + 5 = 9; add 7: 16; add 9: 25. | five sums |
| 2 | notice, name | Is there a pattern? | so | "= 1 × 1" … "= 5 × 5" beside the sums; then the rule card, in the same words | One is 1 × 1, four is 2 × 2, nine is 3 × 3, sixteen is 4 × 4, twenty-five is 5 × 5. Every sum is a square number. Count the odd numbers: three of them give 3 × 3. Call that count n. For 1 + 3 + 5, n is 3. So it seems that the first n odd numbers add up to n × n. | the claim, with n as a count |
| 3 | objection, motive | Do five cases prove it? | but | "?" after the rule card | Why should odd numbers make squares at all? Five examples show a pattern. They do not prove it for every n. The question mark means: not proved yet. We need a reason. | a proof is needed |
| 4 | approach | Where would a reason come from? | so | 3 rows of 3 tiles, then only one tile | A square number is a square of tiles. Nine tiles make 3 rows of 3: a 3 by 3 square, with side 3. Each sum adds one more odd number. So ask: what does one more odd number add to a square of tiles? Start with the first odd number, 1: one tile, a square with side 1. | tile, side, the question that leads to the L |
| 5 | name, instance | What does 3 add? | — | 3 teal tiles around the first tile: a column on the left, a row along the bottom; the 3 in the sums lights up | Add the next odd number, 3: three tiles go around it, to the left, below, and in the corner. Together they make an L, and the square now has side 2. One plus three is four tiles, the same 4 as in the sums. Each L has the color of its odd number, and its number lights up in the sums. The first tile counts as the first L: an L with nothing inside it is only its corner. | L, the color and highlight links |
| 6 | instance | Does it keep working? | therefore | Ls of 5, 7, 9; each term lights up | The next L has 5 tiles and makes side 3. Seven make side 4. Nine make side 5. Each L adds one to the side. So after n Ls the side is n. | n Ls → side n |
| 7 | mechanism | Why is each L the next odd number? | but why | braces 4, 4, 1 on the L around 4 by 4; then the next L drawn faintly around 5 by 5 | Look at the L around the 4 by 4 square: a row of 4, a column of 4, and one corner. 4 + 4 + 1 = 9. The next L goes around 5 by 5 and makes 6 by 6: 5 + 5 + 1 = 11. Each L is two bigger than the one before: one more in its row, one more in its column. The first L is 1, so the Ls are 1, 3, 5, 7, and so on: the odd numbers, in order. | Ls = the odd numbers in order |
| 8 | close | So why does it hold for every n? | therefore | each L lights up with its term; the question mark goes; the rule card becomes 1 + 3 + 5 + ⋯ = n² (n odd numbers) | So adding the odd numbers in order is adding the Ls in order. After n Ls the square has side n. So the first n odd numbers add up to n × n. The question mark can go. We write n × n as n squared, n with a small two, and the dots mean: and so on, in order. | the proof, in words |
| 9 | test | Can I use it? | — | predict pause | What is the sum of the first ten odd numbers? | — |
| 10 | instance | — | — | ten Ls make a 10 by 10 square; the full sum with all ten odd numbers in their L colors; 1 + 9 × 2 = 19 | Ten Ls make a square with side 10: one hundred tiles. The five new Ls are 11, 13, 15, 17, and 19, each in its own color. The tenth L is nine steps of two past 1: 1 + 9 × 2 = 19. So the first ten odd numbers add up to 100. | the rule applied |
| 11 | objection | Does any list of odd numbers work? | but | 3 + 5 = 8: not a square; the first tile leaves a hole in the corner | The first tile matters. Start at 3: 3 + 5 = 8, which is not a square. Without the first tile, the Ls go around a hole. | the assumption: start at 1 |
| 12 | payoff | Which odd number comes in place n, without counting up? | and | "n = 5"; brace labels change from 4 to n − 1; (n − 1) + (n − 1) + 1 = 2n − 2 + 1 = 2n − 1; checks n = 1, 5, 10 | One more thing: which odd number is in place n, without counting up? The Ls tell us. The L that makes side n goes around a square of side n − 1. Here n is 5, and n − 1 is 4. So it has n − 1, plus n − 1, plus 1 tiles. That is two n minus two, plus one: two n minus one, where 2n means two times n. Check: n = 5 gives 9, n = 10 gives 19, n = 1 gives 1, the first tile. | 2n − 1, checked |
| 13 | recap | — | — | the rule card | So, the answer: the first n odd numbers add up to n squared. Every odd number is an L, and the Ls build squares. | the takeaway |

## 5. Concrete to symbol

- n first appears as a count, with an instance: "for 1 + 3 + 5, n is 3" (beat 2). Beat 6 says aloud that the same n is the number of Ls and the side.
- 2n − 1 appears only in the payoff, after 4 + 4 + 1 = 9, with "here n is 5" said aloud, and the brace labels change from 4 to n − 1 in place (beat 12). The middle step 2n − 2 + 1 is shown, and the result is checked at n = 1, 5, and 10.

## 6. Links between representations

- Sum rows ↔ Ls: the same color for an odd number and its L; the term lights up when its L appears (beats 5, 6, 8).
- Tiles ↔ sums: "one plus three is four tiles, the same 4 as in the sums" (beat 5).
- 4 + 4 + 1 ↔ (n − 1) + (n − 1) + 1: the brace labels change in place (beat 12).

## 7. Close the loop

- **Answer:** "the first n odd numbers add up to n × n" is said in beat 2 as a claim, and in beat 8 as a result.
- **General argument:** said in beats 7 and 8: the Ls start at 1 and grow by 2, so they are the odd numbers in order; n Ls make side n.
- **Payoff:** the first ten odd numbers without adding them (beat 10); the n-th odd number is 2n − 1 (beat 12). Scope: proof by induction in symbols; n² − (n − 1)² = 2n − 1 (the big square minus the old square is the L); sums that do not start at 1 (beat 11 shows why they fail).
