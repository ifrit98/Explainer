# Contributing

## Set up

```bash
git clone https://github.com/ifrit98/Explainer.git && cd Explainer
brew install uv cairo pango pkgconf ffmpeg     # Linux: libcairo2-dev libpango1.0-dev pkg-config ffmpeg
uv sync && uv run explainer setup
uv run pytest -q
```

`claude` in this folder loads the same skills as the plugin (`.claude/skills/` links to `plugin/skills/`).

## Add an example

1. `uv run explainer new <slug> --stage …`
2. Fill `model.md`, including Why this form, Concrete cases, Terms, and Scope ([authoring guide](docs/authoring.md)).
3. Run `uv run explainer probe <slug>` with a fresh agent. Recompute every number it suggests; turn findings into claims or Scope entries.
4. Fill `model.yaml`: values, claims, quiz.
5. Render only the stages the representation decision justifies. Mark each claim where a rendering covers it.
6. `uv run explainer check <slug>` must pass. For video, read the review sheet. For a page, test it at 390 px and in both themes.
7. Run the blind test on at least one rendering and record it in `review/understanding.md`.
8. Add the example to `explainers/README.md`.

## Change the toolkit

- Add a test in `tests/` for every fix. Several checks in this repo first failed silently (a layout check that examined no text; integers that stood for fractions); a test is what keeps a check honest.
- Update the matching page in `docs/` and the playbooks in `plugin/skills/explain/references/`.
- If the change affects plugin users, bump the version in `pyproject.toml`, `plugin/.claude-plugin/plugin.json`, and the pin in `plugin/bin/explainer` together (a test checks that they match), and add a `CHANGELOG.md` entry.

## Pull requests

CI runs the tests (toolkit, links, plugin manifest, every example against its model), `explainer check`, and a draft render. Keep this repository free of private material: course content or learner records from projects that use the toolkit belong in those projects.
