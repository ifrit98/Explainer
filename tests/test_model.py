import shutil
from pathlib import Path

import pytest

from explainer_kit.model import (check, extract_numbers, matches, scene_strings, visible_markdown,
                                 words_to_number)

ROOT = Path(__file__).resolve().parent.parent
SOFTMAX = ROOT / "explainers" / "softmax-temperature"


@pytest.mark.parametrize("phrase,value", [
    ("sixty-one", 61), ("eighty four", 84), ("one half", 0.5), ("a half", 0.5), ("thirteen", 13),
    ("two and a half", 2.5), ("one hundred", 100), ("three point one four", 3.14), ("one thousand", 1000),
])
def test_words_to_number(phrase, value):
    assert words_to_number(phrase) == value


def test_extract_skips_identifiers_years_and_stage_numbers():
    text = "STE-80 and v2.3.0 in 2026. Stage 3, steps 4–5, steps 2 and 3. SHA-256 hash 7f3a. Real: 0.842 and −1.0."
    assert [n.value for n in extract_numbers(text)] == [0.842, -1.0]


def test_extract_number_at_sentence_end_and_percent():
    nums = extract_numbers("Cat gets 84%. The logit is 2.0.")
    assert [(n.value, n.percent) for n in nums] == [(84, True), (2.0, False)]


def test_spoken_numbers_count_in_narration():
    nums = extract_numbers("Rule two. At T equal to one half, cat gets sixty-one percent.", words=True)
    assert sorted((n.value, n.percent) for n in nums) == [(0.5, False), (61, True)]


@pytest.mark.parametrize("text,ok", [("0.84", True), ("84%", True), ("0.85", False), ("2", False), ("0.842", True)])
def test_matching_respects_shown_precision(text, ok):
    assert matches(extract_numbers(text)[0], [0.842]) is ok


def test_integer_does_not_stand_for_fraction():
    assert not matches(extract_numbers("2")[0], [2.5])


def test_visible_markdown_keeps_mermaid_data_drops_styling_and_code():
    md = "```mermaid\n---\nconfig:\n  h: 260\n---\nxychart-beta\n  bar [0.5]\n  classDef a stroke:4 3\n```\n" \
         "```bash\nrun --n 77\n```\nText 9.\n"
    nums = [n.value for n in extract_numbers(visible_markdown(md))]
    assert nums == [0.5, 9]


def test_scene_strings_skip_docstrings_and_lexicon():
    src = '"""Doc 42."""\nclass S:\n    lexicon = {"STE-80": "S T E eighty"}\n    def f(self):\n        say("nine words")\n'
    assert scene_strings(src) == ["nine words"]


@pytest.fixture
def softmax_copy(tmp_path):
    dest = tmp_path / "softmax-temperature"
    shutil.copytree(SOFTMAX, dest, ignore=shutil.ignore_patterns("media", "*.mp4", "*.png"))
    return dest


def test_examples_pass(softmax_copy):
    assert check(softmax_copy).ok


def test_changed_model_value_fails_until_renderings_follow(softmax_copy):
    model = softmax_copy / "model.yaml"
    model.write_text(model.read_text().replace("logits: {cat: 2.0,", "logits: {cat: 2.5,"))
    problems = check(softmax_copy).problems
    assert any("explanation.md: does not show logits/cat = 2.5" in p for p in problems)
    assert any("diagram.md: does not show logits/cat = 2.5" in p for p in problems)
    assert any("index.html: embedded model is out of date" in p for p in problems)


def test_corrupted_rendering_number_fails(softmax_copy):
    prose = softmax_copy / "explanation.md"
    prose.write_text(prose.read_text().replace("| 1.0 | 0.609 |", "| 1.0 | 0.619 |"))
    assert any("'0.619' is not a model value" in p for p in check(softmax_copy).problems)
