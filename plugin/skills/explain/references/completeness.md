# Complete the chain

Principles §10 in full. An explanation fails most often by omission: it states a formula without saying why that form, or a guarantee without showing it hold and fail. Before rendering, check the model against each rule.

- **Every operation has a why.** Name the simplest alternative and show it failing with numbers. (Why does softmax use exp? Dividing by the sum of logits gives owl −1 / 2.5 = −0.4, a negative probability, and T cancels out.)
- **Every guarantee has two cases.** One instance with numbers where it holds, and one where its assumption is removed and it breaks. (Dijkstra with a negative edge: A→B 2, A→C 3, C→B −2 settles B at 2; the true distance is 1.)
- **Every mechanism step has a worked example** with real numbers.
- **Every term is defined** before a rendering uses it, and **one concept has one name**. Close concepts get different words, and renderings keep them apart. (Dijkstra: an *estimate* can still drop; the *distance* is final. "A has distance zero" mixes them.)
- **Every quantity has a meaning.** A number the reader sees comes with what it tells them, at a low value and a high one. (Entropy 1.46 bits: the average surprise of one draw, like a choice between 2.76 equally likely tokens; 0.15 bits at T = 0.25, where cat wins 98% of draws.)
- **Every key claim gets time.** In a video, one picture per step of the argument, and a pause after the claim. A guarantee told in one 12-second line over one picture does not land.
- **Scope is declared.** What the explanation leaves out is listed with a pointer, so a learner's next question lands somewhere.

## Completeness is not length

Each rule asks for the one case that carries the idea, not every case. One counterexample with numbers beats three. A why for an operation the reader already trusts (addition, an average) is excess: skip it. Check the result against the length budget (`budget` in `model.yaml`): when a fix pushes a rendering over budget, cut something the argument does not need.

## The probe

Run `explainer probe <slug>` and give the prompt to a fresh agent that sees only `model.md`. Recompute every number it suggests before you add it. Then record the ideas as `claims` in `model.yaml`, and the one-word rules as `terms`; `explainer check` fails while a claim is incomplete, a rendering does not cover it, or a rendering uses a term's avoided phrase.

Not every probe finding belongs in the explanation. A next question that this audience would not ask goes into Scope, or nowhere.

## Turn each review finding into a rule

When a blind test or a reader finds a gap, fix the rendering, then ask which check, probe rule, or template line would have caught it in any explanation. Add that too. A finding fixed only in one example comes back in the next one.

The same holds for excess. When a reader finds a passage they did not need, ask which rule made you write it, and narrow that rule.
