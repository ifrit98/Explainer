"""Completeness: claims must be complete, covered by each rendering, and every function needs a why."""

import os
from pathlib import Path

import pytest

from explainer_kit.model import check, functions_used


def make(tmp_path: Path, yaml: str, model_md: str = "# m\n", prose: str | None = None) -> Path:
    d = tmp_path / "x"
    d.mkdir()
    (d / "model.md").write_text(model_md)
    (d / "model.yaml").write_text(yaml)
    if prose is not None:
        (d / "explanation.md").write_text(prose)
    return d


WHY = """values: {}
claims:
  - id: why-exp
    kind: why
    about: [exp]
    statement: s
    alternative: a
    counterexample: c
"""


def test_complete_and_covered_claim_passes(tmp_path):
    d = make(tmp_path, WHY, "uses exp(z)", "<!-- claim: why-exp -->\nText.")
    assert check(d).ok


def test_uncovered_claim_fails(tmp_path):
    d = make(tmp_path, WHY, "uses exp(z)", "Text without the mark.")
    assert any("does not cover claim 'why-exp'" in p for p in check(d).problems)


@pytest.mark.parametrize("kind,missing", [("why", "counterexample"), ("guarantee", "counterexample"),
                                          ("mechanism", "example")])
def test_incomplete_claims_fail(tmp_path, kind, missing):
    fields = {"why": "alternative: a", "guarantee": "example: e", "mechanism": ""}[kind]
    d = make(tmp_path, f"values: {{}}\nclaims:\n  - id: c1\n    kind: {kind}\n    statement: s\n    {fields}\n")
    assert any(f"has no {missing}" in p for p in check(d).problems)


def test_unknown_marker_fails(tmp_path):
    d = make(tmp_path, "values: {}\n", prose="<!-- claim: nope -->")
    assert any("marks unknown claim 'nope'" in p for p in check(d).problems)


def test_function_without_why_fails_until_justified_or_accepted(tmp_path):
    d = make(tmp_path, "values: {}\n", "p = exp(z) / sum, entropy uses log₂ p")
    problems = check(d).problems
    assert any("uses exp but no `why` claim" in p for p in problems)
    assert any("uses log but no `why` claim" in p for p in problems)
    (d / "model.yaml").write_text("values: {}\naccept_unjustified: {exp: r, log: r}\n")
    assert check(d).ok


def test_function_detection_ignores_words_that_contain_names():
    assert functions_used("exponent, logic, blog, expire") == set()
    assert functions_used("p = exp(z/T); H = −Σ p log₂ p; √d") == {"exp", "log", "√"}


def test_probe_and_quiz_prompts(tmp_path):
    from explainer_kit.review import probe_prompt, quiz_prompt, quiz_rubric
    root = tmp_path / "proj"
    d = root / "explainers" / "x"
    d.mkdir(parents=True)
    (d / "model.md").write_text("# m")
    (d / "model.yaml").write_text(WHY.replace("    counterexample: c\n", "    counterexample: c\n    ask: Why exp?\n"))
    (d / "explanation.md").write_text("<!-- claim: why-exp -->")
    os.environ["EXPLAINER_ROOT"] = str(root)
    try:
        assert "Why this form" in probe_prompt("x") and str(d / "model.md") in probe_prompt("x")
        assert "Why exp?" in quiz_prompt("x", "prose") and "model.yaml" not in quiz_prompt("x", "prose").split("Questions:")[1]
        assert "a full answer also gives the counterexample: c" in quiz_rubric("x")
    finally:
        del os.environ["EXPLAINER_ROOT"]
