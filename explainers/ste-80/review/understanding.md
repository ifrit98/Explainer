# Understanding tests: ste-80

## Cold read (video, v0.6.0)

Run 2026-10-04, reading as "people who write technical text, know grammar, and do not know ASD-STE100".

- **Blocking, fixed:** "the length does not change" after rule one was false as shown: "prior to" (two words) became "before" (one), and a silently added "the" kept the count at 16. Rule one now goes 16 → 15 and says so. ASD-STE100 was named and never explained; now one line on screen and in the narration: Simplified Technical English, a standard for aircraft maintenance manuals. "Operation becomes machine" sat under a verb rule with no reason; now "the vague noun operation becomes the machine you start". "The instruction did not change" overclaimed; now "the reader still fills the reservoir before starting the machine".
- **Added (short):** the motive (manuals are read under time pressure, often in a second language); what the orange bar and the red words mean; a scope line (full STE also limits sentence length, keeps one meaning per word, and uses an approved dictionary).
- **Cost:** 57 s → 83 s, under the 150 s default. The opening, which first ran 21 s over the title alone, was split so the standard and the readers appear on screen as they are said.
- **Not applied (edge):** naming the imperative mood in rule two.

## v0.7.0 review runs

Six cold-read rounds in all. Each of the first five found two or three blocking items, smaller each time:

1. (v0.6.0) the length after rule one; ASD-STE100 unexplained; "operation becomes machine" without a reason; an overclaimed close.
2. "about eighty percent of the rules" without saying which; the closing scope line listed rules STE-80 keeps as if they were left out; a quoted phrase that is unclear when spoken.
3. "drops the approved dictionary", then "use simple words" with no test for simple; "the goal is less work, not fewer words" next to a word-count bar.
4. A spoken quotation without a marker; a noun change under a rule about verbs (an edge finding since round 1). Rule three is now "use concrete words".
5. Nothing blocks.

Also adopted: the narration named each swap about 5 s before the screen showed it; the swap bookmarks now come first, so each word changes as it is said. Claims added; blind test **pass**. 57 s → 97 s.
