# Compile the narrative

Principles §11 in full. The model says what is true. It does not say the path a reader takes to it. A correct model with every claim covered can still lose the reader: the odd-squares video passed its blind test while it used "the n-th L" without saying what n is, and never said its own result aloud. After the model, write `narrative.md` (Pass 3): the beats a reader goes through, in order. An explainer's power comes from the model and the narrative together, not from the animation.

- **Question first, in words.** State the question, and the result itself, in words before you explain it. Answer it again at the end in the same words.
- **Motive.** Give a reason to care, and a reason for the approach. ("A square number is a square of tiles. Each sum adds one odd number. So ask what one more odd number adds to a square.")
- **Earn every new reference.** Each term, symbol, name, and visual convention (a color, a highlight, a brace) that is new *to this reader* is shown, named, and grounded by an instance before its first use. Keep one meaning per letter. If n is a count, it stays a count, or the narration says aloud that the count and the side are the same number.
- **Do not explain what the reader knows.** The audience in `model.md` sets the baseline. A developer does not need "2n means two times n"; a first-year student may. Each line spent on something known delays the next idea.
- **Concrete, then symbol.** Work an instance with numbers, say the binding aloud ("here n is 5"), then write the symbol.
- **Say what you show; show what you say.** Read or explain every label and formula on screen, or remove it. Give everything you say a picture.
- **Names match pictures, and each case gets its own picture.** If you call a shape an L, draw an L. Show a counterexample on its own small picture, not on the large one from another beat.
- **Each beat answers the question the last one raised.** Write the bridge: so, but, therefore.
- **Do not prove with examples.** After "five examples do not prove it", each general step needs a reason, not three more cases.
- **Close the loop.** Answer the opening question with the general argument said aloud, then give the payoff and one connection.

## The cold read

Run `explainer coldread <slug>` on the narrative before you render, and on each rendering after. A fresh agent reads as the audience in `model.md`, meets the explanation for the first time, and reports, in order:

- **unresolved:** a reference this reader was not given;
- **unsaid:** something shown but not said;
- **leap:** a step without its reason;
- **excess:** something this reader already knows, something said again with nothing new, or something the argument does not need.

It marks the findings that block the main line. Fix every blocking finding. Fix an edge finding when the fix is short. Cut excess unless it carries a step of the argument. `explainer check` fails a scene that shows a symbol the narrative's introduction ledger does not list.

The cold read stops when no finding blocks the main line. It does not need to reach zero findings: each round of fixes adds words, and past that point the added words cost more than the gaps they close.
