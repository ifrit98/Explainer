"""Positive controls for the rederivation test: does it notice a missing building block?

PRD-002's dev baseline credited every condition with 90–100% of the expected steps. That is either a fact about the
explanations or a blind test. The controls check the test where the right answer is known: an explanation with one
building block cut out should no longer get credit for it.

1. `explainer eval cuts` copies the v0.8 builds of the subjects in evals/artifact/controls.yaml, cuts one block from
   each `principles` explanation (a fresh `claude -p` cutter), and has a separate checker confirm the cut. The cut
   copies, checks and diffs are frozen before any run.
2. `explainer eval controls` reuses the PRD-002 baseline's reader chains for the uncut conditions, runs the unchanged
   rederivation stage on the folder, checks uncaught cuts for leaks, and reports the verdict under the bar in
   controls.yaml.
"""

from __future__ import annotations

from pathlib import Path

import yaml

from explainer_kit.paths import project_root


def controls_file() -> Path:
    return project_root() / "evals" / "artifact" / "controls.yaml"


def load_controls() -> dict:
    """The cut list and the bar, with the source and baseline folders resolved against the project."""
    c = yaml.safe_load(controls_file().read_text())
    return {**c, "source": project_root() / c["source"], "baseline": project_root() / c["baseline"]}
