# Interactive HTML explainer mode

Create a self-contained HTML explainer when exploration communicates the material better than static prose or a static diagram.

Treat the page as an educational instrument, not as a decorated document.

Start from the template: `explainer new <slug> --stage 3` creates `index.html` on the **web toolkit** (`explainer_kit/web/`), then `explainer sync <slug>` inlines the toolkit and the model's values. The page stays one self-contained file.

| Toolkit piece | Use |
|---|---|
| `Explainer.model` | the values from `model.yaml`. Compute from these; never retype a model number in the script. |
| `Explainer.tracker(v)` | one shared value; every view subscribes with `.on(fn)` |
| `Explainer.slider(el, t, {min, max, log, presets, format})` | range input bound to a tracker. Presets set the exact value. |
| `Explainer.bars(el, {labels, colors, format})` | bars that keep their identity; returns `update(values)` |
| `Explainer.predict(el, {id, question, type, answer, judge, explain})` | predict-first gate; hides `[data-after=id]` until the reader commits |
| `Explainer.video(el, {src, captions, timeline})` | video that pauses at each predict event of the render's `timeline.json` |
| `.ex-level` details, `.ex-tag` (fact, derived, assumption, estimate, loose) | progressive disclosure, epistemic labels |

The toolkit CSS defines light and dark tokens. Page-specific colors go in the page's own `<style>`, as tokens with dark values too.

Load the `artifact-design` skill before you write the page. It defines the page contract (title, theming tokens, allowed CDNs, phone layout). If the page includes a diagram, also load `artifact-diagramming`. If it includes charts, load `dataviz`.

## 1. Page structure

A page normally contains:

1. A one-screen conceptual overview (Level 1).
2. An interactive primary visualization.
3. Controls for meaningful variables, where appropriate.
4. Progressive disclosure of deeper detail (Levels 2–4).
5. Short explanatory text beside the relevant visual.
6. Concrete examples.
7. Edge cases or failure modes.
8. A compact summary.

Large architectures use drill-down navigation:

```text
overview → (click) subsystem → (click) component → (click) implementation detail
```

## 2. Interaction rules

Every interaction must teach something. Before you add a control, write down what the reader learns by using it.

Good interactions:

- Sliders that change meaningful parameters.
- Toggles between competing models.
- Animation controls (play, pause, step, scrub).
- Hover annotations.
- Clickable components that reveal the next level.
- Timeline scrubbing.
- Before/after comparisons.
- Layer visibility.
- Simulation controls.

Do not add interaction whose only purpose is visual novelty.

## 3. Epistemic controls

Show the epistemic status of claims visibly (for example a small tag: *fact*, *assumption*, *estimate*).

Where practical, expose assumptions as toggles and let the visualization react:

```text
Assumptions
[x] fixed interest rates
[x] constant demand
[ ] supply shock
```

## 4. Engineering rules

- Prefer one self-contained `index.html` with embedded CSS and JavaScript. Use external libraries only when they materially improve the explanation (for example D3 or KaTeX from an allowed CDN).
- Make the layout responsive. Check it at phone width.
- Make controls keyboard accessible. Give them visible labels.
- Make the explanation understandable without animation. Respect `prefers-reduced-motion`.
- Preserve object identity during transitions. If a node is the same object before and after a change, animate it moving. Do not replace it with a new-looking node.
- Compute values from the model's equations in code. Do not hard-code outputs that a slider is supposed to change.
- The page is disposable. Optimize for correctness and clarity, not maintainability.

## 5. Verify and deliver

Run `explainer check <slug>` first: it fails on any visible number the model does not explain, and on a stale model or toolkit block.

1. Open the page with Playwright. Use every control once. Check the console for errors.
2. Take screenshots at desktop and phone width. Look at them.
3. Run the seven understanding questions from `principles.md` §7, and the `verify` skill before you publish.
4. Publish with the Artifact tool and give the user the link.
