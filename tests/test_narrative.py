"""The narrative pass: the introduction ledger, scene symbols, and the cold-read prompt."""

from pathlib import Path

from explainer_kit.model import check, ledger_references, scene_symbols
from explainer_kit.review import coldread_prompt

ROOT = Path(__file__).resolve().parents[1]

SCENE = '''
from manim import *
class S(ExplainerScene):
    def construct(self):
        x = 0.123
        law = MathTex(r"(n-1) + (n-1) + 1 = 2n - 1")
        t = label(f"T = {x:.2f}")
        words = label("the first odd numbers")
        with self.voiceover(text="In general, the k-th L has two n minus one tiles."):
            pass
'''

LEDGER = """# Narrative: x

## 3. Introduction ledger

| Reference | Means | Grounded by | Beat |
|---|---|---|---|
| n | the side | n is 5 | 8 |
| tile, L | ... | ... | 4 |

## 4. Beats
"""


def test_scene_symbols_come_from_math_labels_and_spoken_nth():
    # n from MathTex, T from a math label, k from "the k-th"; not 'f' from the format code or words from a sentence
    assert scene_symbols(SCENE) == {"n", "T", "k"}


def test_ledger_references_read_the_first_column():
    assert ledger_references(LEDGER) == {"n", "tile", "L"}


def make(tmp_path: Path, ledger: str | None) -> Path:
    d = tmp_path / "x"
    (d / "video").mkdir(parents=True)
    (d / "model.md").write_text("# m\n")
    (d / "model.yaml").write_text("values: {}\nallow: [1, 2, 5, 8]\n")
    (d / "video" / "scene.py").write_text(SCENE)
    if ledger is not None:
        (d / "narrative.md").write_text(ledger)
    return d


def test_symbol_missing_from_the_ledger_fails(tmp_path):
    problems = check(make(tmp_path, LEDGER)).problems
    assert any("shows the symbol 'k'" in p for p in problems)
    assert not any("symbol 'n'" in p for p in problems)


def test_without_a_narrative_the_ledger_is_not_checked(tmp_path):
    rep = check(make(tmp_path, None))
    assert not any("symbol" in p for p in rep.problems)
    assert any("no narrative.md" in n for n in rep.notes)


def test_coldread_prompt_walks_in_order_from_prior_knowledge():
    narrative = coldread_prompt("odd-squares", "narrative")
    assert "one beat at a time" in narrative and "Beats table" in narrative
    assert "square numbers (1, 4, 9, 16, …)" in narrative           # Before line of narrative.md
    assert '"unsaid"' in narrative                                   # beats have a Shown column
    prose = coldread_prompt("softmax-temperature", "prose")
    assert "one paragraph" in prose and '"unsaid"' not in prose
    assert "Audience" not in prose and "Nothing else counts as known" in prose


def test_reference_examples_with_a_narrative_introduce_every_symbol():
    for narrative in ROOT.glob("explainers/*/narrative.md"):
        rep = check(narrative.parent)
        assert not [p for p in rep.problems if "introduction ledger" in p], narrative.parent.name
