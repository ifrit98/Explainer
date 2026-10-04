# Web toolkit reference (Stage 3)

Interactive pages are single self-contained HTML files. The shared CSS and JS live in `explainer_kit/web/`; `explainer sync <slug>` inlines them into the page, together with the model's values, so a page works offline, from GitHub Pages, or as a published Artifact.

## Start a page

```bash
explainer new my-topic --stage 3     # index.html from the template, already synced
explainer sync my-topic              # after you change model.yaml or update the toolkit
explainer check my-topic             # fails on a stale toolkit or model block
```

A page opts in with three tags; `sync` fills them:

```html
<style id="explainer-toolkit-css"></style>                          <!-- in <head> -->
<script type="application/json" id="explainer-model"></script>       <!-- before the scripts -->
<script id="explainer-toolkit-js"></script>
```

Wrap the content in `<main class="ex">`. Page-specific colors go in the page's own `<style>`, as tokens with dark values too (see `cdn-request`).

## API

### `Explainer.model`

The `values` of `model.yaml`. Compute from these; never retype a model number in the script.

```js
const M = Explainer.model;
const rtt = (km) => (km / 100) * M.rtt_ms_per_100km;
```

### `Explainer.tracker(initial)`

One shared value. Every view subscribes to it.

```js
const T = Explainer.tracker(1.0);
T.on((v) => render(v));   // called now and on every change
T.set(0.5);
```

### `Explainer.slider(el, tracker, options)`

A labeled range input bound to a tracker.

| Option | Meaning |
|---|---|
| `label`, `min`, `max` | required |
| `log` | move in log10 space (for ranges like 0.1–10) |
| `presets` | values or `{value, label}`; a preset sets the **exact** value, not the nearest slider step |
| `format` | value → text for the readout and `aria-valuetext` |
| `thermal` | cold-to-hot track (for temperatures) |
| `scale` | labels under the track |

### `Explainer.bars(el, options)` → `update(values)`

Bars that keep their identity as values change. Options: `labels`, `sublabels`, `colors` (CSS colors per bar), `max`, `format`, `tip(i, value)`. Each bar is focusable and shows a tooltip.

### `Explainer.predict(el, options)`

A predict-first gate. Elements with `data-after="<id>"` stay hidden until the reader commits a prediction.

| Option | Meaning |
|---|---|
| `id` | the gate id (used by `data-after`) |
| `question` | author text (may contain markup) |
| `type` | `number`, `text`, or `choice` |
| `choices`, `answer` | for `choice`: the options and the index of the right one |
| `answer`, `judge(guess)`, `unit` | for `number`: the result and a tolerance test |
| `explain` | shown after the reveal |

The prediction is kept per reader (local storage, never required), and the element fires a `predicted` event. Redraw anything measured while hidden in that event: an SVG sized while hidden gets the wrong text size.

### `Explainer.video(el, {src, poster, captions, timeline})`

A video player that pauses at every predict event of the render's `timeline.json` and asks for a prediction before it continues. Chapter buttons jump to each pause. `explainer check` fails a page that plays a video with predict pauses through a plain `<video>`.

The [landing page](../index.html) uses the player outside an explainer folder: it loads `explainer_kit/web/explainer.js` with a `<script src>` and styles the player with its own tokens, because the toolkit CSS defines page-level tokens of its own. Seeking needs a server that answers HTTP range requests (GitHub Pages does; `python -m http.server` does not, so test locally with `npx http-server`).

### CSS pieces

| Class | Use |
|---|---|
| `.ex-panel`, `.ex-row` | the instrument card; a chart beside readouts |
| `.ex-readout`, `.ex-meter` | label, value, meter |
| `.ex-table-wrap`, `.ex-law`, `.ex-live` | scrollable tables; a formula line with live values |
| `.ex-tag.fact` · `.derived` · `.assumption` · `.estimate` · `.loose` | epistemic labels |
| `.ex-cards`, `.ex-card` | limits and labels |
| `details.ex-level` | progressive disclosure, Levels 2–4 |

## Mark the claims

Put `data-claim="<id>"` on the element that presents each claim from `model.yaml` (see the [model reference](model-reference.md#coverage-marks)). `explainer check` fails while a claim the page should cover has no mark.

## Pitfalls

- **Selector collisions.** A page's own button group must not reuse a class that another handler selects. In `softmax-temperature`, normalizer buttons placed in a `.presets` group were picked up by the temperature-preset handler and set T to NaN. Give each group its own class.
- **Hidden SVGs.** Content inside a gated section has no size until it is revealed. Draw it in the gate's `predicted` event.
- **Reader input.** Typed predictions are escaped before display. Keep it that way in page code: never put reader text into `innerHTML` unescaped.
- **Numbers.** Visible numbers are checked against the model. A number computed at runtime is not, so compute it from `Explainer.model`, not from a typed constant.
