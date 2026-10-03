# Troubleshooting

## `uv sync` fails building `pycairo`: "Dependency lookup for cairo with method 'pkg-config' failed"

pkg-config is missing.

```bash
brew install pkgconf cairo pango
uv sync
```

## "Kokoro model not found … using silent narration"

The model files are not in `models/`. Download them:

```bash
uv run explainer setup
```

To keep the model elsewhere, set `EXPLAINER_KOKORO_DIR`.

## `MathTex`, `Tex`, `DecimalNumber`, or `BraceLabel` fails with a LaTeX error

These Manim objects need LaTeX. Install it:

```bash
brew install --cask basictex     # asks for your password
```

Or avoid them: use `label()` for text and numbers, and `NumberLine(include_numbers=False)` with your own tick labels.

## `ValueError: zip() argument 2 is shorter than argument 1`

An animation (usually `FadeOut` or `Transform`) acts on an `always_redraw` group whose number of glyphs changes from frame to frame. Freeze it first:

```python
group.clear_updaters()
self.play(FadeOut(group))
```

## "SoX could not be found!"

manim-voiceover prints this at import. It is harmless unless you use `global_speed`. To remove it: `brew install sox`.

## A word sounds wrong

Add a spoken form to the scene's lexicon. The captions keep the written form.

```python
lexicon = {"STE-80": "S T E eighty", "QKᵀ": "Q K transpose", "nginx": "engine x"}
```

Test the spelling with `uv run explainer say "S T E eighty"`.

## A bookmark fires at the wrong moment

Check the bookmark times in `video/media/voiceovers/cache.json`. Each `word_boundaries[].audio_offset` is in units of 10⁻⁷ s from the start of that voiceover block. If the time is right but the animation is late, the animation before `wait_until_bookmark` runs longer than the time to the bookmark. Shorten it, or give it `run_time=tracker.time_until_bookmark("x")`.

## The font looks different

The house font is Avenir Next (macOS). Pango falls back to another sans-serif font when it is missing. Change `explainer_kit.scene.FONT` to a font that you have.

## Rendering is slow

- Iterate with `--draft` (480p15, no TTS).
- Render one chapter with `--scene Name -q m`.
- `always_redraw` rebuilds its object every frame. Keep the redraw function small.
