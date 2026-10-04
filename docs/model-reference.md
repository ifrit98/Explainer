# Model reference

Every explainer has two model files in `explainers/<slug>/`:

| File | For | Holds |
|---|---|---|
| `model.md` | people (and the probe) | the semantic model in prose and tables |
| `model.yaml` | tools | the values, claims, and quiz that renderings are checked against |

`explainer new <slug>` creates both from templates, and a third file, `narrative.md`: the path a first-time reader takes through the model (see below).

## `model.md` sections

| Section | Answers | Notes |
|---|---|---|
| Central question | What does the explanation answer? | One sentence. |
| Audience and prior knowledge | Who reads it, and what do they already know? | Sets which terms need definitions. |
| Entities | The minimum concepts, one sentence each, with status. | |
| Relationships, dependencies | What interacts? What must come first? | |
| Causal chain, temporal sequence | What causes what? In what order? | |
| Quantities | Numbers, equations, worked tables. | Every number here goes into `values`. |
| Alternative states | Cases that behave differently. | |
| **Why this form** | For each operation: the simplest alternative, and what it breaks, with numbers. | Becomes `why` claims. |
| **Concrete cases** | For each guarantee: a case where it holds and a case where it breaks without its assumption. For each mechanism: a worked example. | Becomes `guarantee` and `mechanism` claims. |
| **Terms** | Every term a rendering uses, defined in reading order. | |
| Epistemic status | Observed, derived, assumed, estimated, disputed, unknown. | |
| Confusion points | Likely misunderstandings and their corrections. | |
| **Scope** | What is deliberately left out, with a pointer. | A learner's next question should land here or in the model. |
| Representation decision | Stage, reason, levels. | |

## `model.yaml` keys

```yaml
values:            # the facts renderings show: nested numbers and strings
  logits: {cat: 2.0, dog: 1.0, fox: 0.5, owl: -1.0}
  probabilities:
    "T=1.0": {cat: 0.609, dog: 0.224, fox: 0.136, owl: 0.030}

allow: [4, 60]     # numbers renderings may show that are not model facts (counts, sample sizes)

budget: {prose: 850, reason: "six claims, each with a case in numbers"}   # optional; see below

require:           # values each listed rendering must show, unless it loads the model
  - path: logits                   # '/' nests: probabilities/T=1.0
    in: [prose, diagram, html, video]

claims:            # the ideas the explanation must convey (see below)
  - id: why-exp
    kind: why
    about: [exp, softmax]
    statement: "exp turns every logit into a positive weight, keeps the order, and turns a gap into a ratio."
    alternative: "Divide each logit by the sum of the logits."
    counterexample: "The sum is 2.5, so owl gets −1.0 / 2.5 = −0.4: a negative probability."
    ask: "Why does softmax use exp, instead of dividing by the sum of the logits?"

accept_unjustified:   # functions in model.md that deliberately have no why claim, with the reason
  log: "only the out-of-scope running time uses it"   # a debt: `explainer check -v` lists it

terms:             # one word per concept; a rendering that uses an avoided phrase fails
  - term: estimate
    means: "the shortest length found so far; 'distance' means only the final value"
    avoid: [has distance, smallest distance, shorter distance]

quiz:              # blind-test questions with expected answers
  - q: "If T rises from 1 to 3, what happens to the top probability, and does the order change?"
    expect: "It falls toward 0.25; the order does not change."
    misconception: "A different token becomes the most likely one."
```

### Budget

`budget` sets the length a rendering may have: `prose` in words (the visible words of `explanation.md`) and `video` in seconds (from the final `timeline.json`). Without it, `explainer check` warns above 600 words or 150 s. With it, the check fails above the declared length, and the budget needs a `reason`.

A reader pays for every sentence. Review rounds add words: each gap a reviewer finds is fixed by saying more. The budget is the counterweight. When a fix pushes a rendering over its budget, cut something this reader does not need.

### Claims

A claim is one idea a reader must take away. Its kind decides which fields it needs:

| Kind | Required fields | Use it for |
|---|---|---|
| `why` | statement, alternative, counterexample | why an operation has this form and not a simpler one |
| `guarantee` | statement, example, counterexample | an invariant or "always / never" claim: where it holds, and where it breaks without its assumption |
| `mechanism` | statement, example | a step, with a worked example in numbers |
| `definition` | statement | a term the renderings rely on |
| `limit` | statement | a boundary of the model |
| `misconception` | statement, correction | a wrong belief the explanation must prevent |

Optional fields: `about` (functions the claim justifies), `ask` (a blind-test question; the rubric expects the statement and the cases), `in` (renderings that must cover it; default: every rendering present).

### Coverage marks

A rendering covers a claim by marking the place where it presents it:

| Rendering | Mark |
|---|---|
| `explanation.md`, `diagram.md` | `<!-- claim: why-exp -->` before the passage |
| `index.html` | `data-claim="why-exp"` on the element |
| `video/scene.py` | `self.claim("why-exp")` at the moment it is shown (it also appears on the review sheet) |

A mark is a promise, not proof: the blind understanding test checks that the idea actually lands.

## `narrative.md` sections

| Section | Answers | Checked by |
|---|---|---|
| Reader before and after | What may the reader assume? What can they say afterwards? | the cold read uses "Before" as its prior knowledge |
| Question and motive | The question and the result in words; why care; why this approach. | the cold read |
| Introduction ledger | Every term, symbol, name, and visual convention: what it means, the instance that grounds it, the beat that introduces it. | `explainer check` (scene symbols), the cold read |
| Beats | In order: the reader's question, the bridge, what is shown, what is said, what the reader now knows. | the cold read (`--rendering narrative`) |
| Concrete to symbol | For each general statement: the instance, the binding said aloud, the symbol. | |
| Links between representations | How two views of one quantity are linked at the same moment. | |
| Close the loop | The answer, the general argument in words, the payoff. | the cold read |

## What `explainer check` reports

| Problem | Example message | Fix |
|---|---|---|
| A visible number the model does not contain | `explanation.md: '0.619' is not a model value` | correct the rendering, or add the value to `values` / `allow` |
| A required value a rendering does not show | `diagram.md: does not show logits/cat = 2.2` | update the rendering, or make it load the model |
| A stale page | `index.html: embedded model is out of date` | `explainer sync <slug>` |
| An incomplete claim | `model.yaml: guarantee claim 'x' has no counterexample` | add the missing field, with numbers |
| An uncovered claim | `explanation.md: does not cover claim 'why-exp'` | present the idea there and mark it, or narrow `in` |
| An unknown mark | `index.html: marks unknown claim 'nope'` | fix the id |
| A function with no why | `model.md uses exp but no 'why' claim says why` | add a `why` claim with `about: [exp]`, or `accept_unjustified` with a reason |
| A second name for a concept | `video/scene.py: says 'has distance'; the model's term is 'estimate'` | use the term; avoid phrases match whole words, ignoring case and line breaks |
| A video without its predict pauses | `index.html: plays the video with a plain <video>, which skips its 1 predict pause(s)` | play it with `Explainer.video` |
| A symbol the narrative does not introduce | `video/scene.py: shows the symbol 'n', which the introduction ledger in narrative.md does not introduce` | add it to the ledger with its grounding instance, and introduce it in that beat |
| A Mermaid syntax error (with `--diagrams`) | `diagram.md:24: Error: Parse error on line 3` | fix the block; the line is where the block starts |
| Over a declared length budget | `explanation.md: 702 words, over its budget of 650 words` | cut what this reader does not need |
| A budget with no reason | `model.yaml: budget needs a reason` | say why this explanation needs this length |
| Over the default length (a warning, `!`) | `video: 208 s, over the default budget of 150 s` | cut, or declare `budget` with a reason |

Numbers are compared at the precision shown: 0.84 matches 0.842, "84%" and "eighty-four percent" match 0.842, 6.0 × 10⁻⁶ is one number, and 2 never stands for 2.5. Stage, step, and section numbers, years, versions, and hash fragments are skipped.

**Limit: value collisions.** The check matches values, not meanings. If a changed value happens to equal another value the rendering shows for a different reason (a logit of 2.5 and a sum of 2.5), the check cannot tell them apart. Renderings that load the model (`load_model`, `Explainer.model`) avoid the problem.
