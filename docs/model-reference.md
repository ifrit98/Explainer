# Model reference

Every explainer has two model files in `explainers/<slug>/`:

| File | For | Holds |
|---|---|---|
| `model.md` | people (and the probe) | the semantic model in prose and tables |
| `model.yaml` | tools | the values, claims, and quiz that renderings are checked against |

`explainer new <slug>` creates both from templates.

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
  log: "log₂ only defines entropy, a readout"

quiz:              # blind-test questions with expected answers
  - q: "If T rises from 1 to 3, what happens to the top probability, and does the order change?"
    expect: "It falls toward 0.25; the order does not change."
    misconception: "A different token becomes the most likely one."
```

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

Numbers are compared at the precision shown: 0.84 matches 0.842, "84%" and "eighty-four percent" match 0.842, 6.0 × 10⁻⁶ is one number, and 2 never stands for 2.5. Stage, step, and section numbers, years, versions, and hash fragments are skipped.

**Limit: value collisions.** The check matches values, not meanings. If a changed value happens to equal another value the rendering shows for a different reason (a logit of 2.5 and a sum of 2.5), the check cannot tell them apart. Renderings that load the model (`load_model`, `Explainer.model`) avoid the problem.
