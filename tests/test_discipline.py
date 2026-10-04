"""One word per concept, time for each claim, predict pauses kept on pages, and Mermaid that renders."""

import json
from pathlib import Path

import pytest

from explainer_kit.diagrams import html_blocks, markdown_blocks, mermaid_command, validate
from explainer_kit.model import avoided_phrases, check, plain_video_with_pauses
from explainer_kit.review import pace_issues, quiz_prompt

ROOT = Path(__file__).resolve().parents[1]


def make(tmp_path: Path, yaml: str, prose: str | None = None, page: str | None = None) -> Path:
    d = tmp_path / "x"
    d.mkdir()
    (d / "model.md").write_text("# m\n")
    (d / "model.yaml").write_text(yaml)
    if prose is not None:
        (d / "explanation.md").write_text(prose)
    if page is not None:
        (d / "index.html").write_text(page)
    return d


TERMS = """values: {}
terms:
  - term: estimate
    means: the shortest length found so far
    avoid: [smallest distance, has distance]
"""


# ---------------------------------------------------------------- terms

def test_avoided_phrase_fails_and_names_the_term(tmp_path):
    d = make(tmp_path, TERMS, "Settle the node with the smallest\ndistance.")
    problems = check(d).problems
    assert any("says 'smallest distance'; the model's term is 'estimate'" in p for p in problems)


def test_allowed_uses_of_the_word_pass(tmp_path):
    d = make(tmp_path, TERMS, "Settle the node with the smallest estimate. Its final distance is fixed.")
    assert check(d).ok


def test_avoided_phrases_match_whole_words_only():
    assert avoided_phrases("it has distances", ["has distance"]) == []
    assert avoided_phrases("A Has  Distance zero", ["has distance"]) == ["has distance"]


# ---------------------------------------------------------------- pages keep the video's predict pauses

def test_plain_video_with_predict_pauses_fails(tmp_path):
    d = make(tmp_path, "values: {}\n", page='<video src="video/out.mp4"></video>')
    (d / "video").mkdir()
    (d / "video" / "timeline.json").write_text(json.dumps({"events": [{"kind": "predict", "t": 3, "question": "?"}]}))
    assert any("skips its 1 predict pause(s)" in p for p in check(d).problems)


def test_explainer_video_or_no_pauses_passes():
    assert not plain_video_with_pauses('<div id="v"></div><script>Explainer.video(v, {})</script>', 2)
    assert not plain_video_with_pauses('<video src="a.mp4"></video>', 0)
    # the inlined toolkit mentions Explainer.video; that does not count as using it
    page = '<video src="a.mp4"></video><script id="explainer-toolkit-js">/* Explainer.video(el) */</script>'
    assert plain_video_with_pauses(page, 1)


def test_landing_page_uses_the_predict_pause_player():
    page = (ROOT / "index.html").read_text()
    for slug in ("softmax-temperature", "odd-squares", "dijkstra", "ste-80"):
        timeline = json.loads((ROOT / "explainers" / slug / "video" / "timeline.json").read_text())
        pauses = sum(e["kind"] == "predict" for e in timeline["events"])
        if pauses:
            assert f"explainers/{slug}/video/timeline.json" in page, f"{slug}: landing page skips its pauses"
    assert not plain_video_with_pauses(page, 1)


# ---------------------------------------------------------------- pace

def voice(t, duration, bookmarks=None):
    return [{"kind": "voiceover", "t": t, "duration": duration, "bookmarks": bookmarks or {}},
            {"kind": "voiceover_end", "t": t + duration}]


def test_claim_without_a_pause_is_flagged():
    events = voice(0, 5, {"c": 1}) + [{"kind": "claim", "t": 1, "id": "why"}] + voice(5.3, 2)
    assert any("claim 'why'" in i and "pause" in i for i in pace_issues(events))


def test_claim_with_a_pause_passes():
    events = voice(0, 5, {"c": 1}) + [{"kind": "claim", "t": 1, "id": "why"}] + voice(6.5, 2)
    assert pace_issues(events) == []


def test_long_talk_over_one_picture_is_flagged():
    events = voice(0, 15, {"c": 1}) + [{"kind": "claim", "t": 1, "id": "g"}] + voice(17, 2)
    assert any("talks 14s over one picture" in i for i in pace_issues(events))
    split = voice(0, 15, {"c": 1, "step": 6}) + [{"kind": "claim", "t": 1, "id": "g"}] + voice(17, 2)
    assert pace_issues(split) == []


def test_published_videos_give_each_claim_time():
    for timeline in sorted((ROOT / "explainers").glob("*/video/timeline.json")):
        assert pace_issues(json.loads(timeline.read_text())["events"]) == [], timeline.parent.parent.name


# ---------------------------------------------------------------- blind-test audit

def test_quiz_prompt_asks_for_the_audit():
    prose = quiz_prompt("softmax-temperature", "prose")
    assert '"audit": {"terms"' in prose and "unexplained" in prose and "pace" not in prose
    assert '"pace"' in quiz_prompt("dijkstra", "video")


# ---------------------------------------------------------------- Mermaid

def test_blocks_are_found_in_markdown_and_html(tmp_path):
    md = tmp_path / "d.md"
    md.write_text("text\n```mermaid\nflowchart LR\n  A --> B\n```\n```python\nx = 1\n```\n")
    page = tmp_path / "p.html"
    page.write_text('<p>x</p>\n<pre class="mermaid">flowchart LR\n  A --&gt; B</pre>')
    [b] = markdown_blocks(md)
    assert (b.line, b.source) == (2, "flowchart LR\n  A --> B")
    [h] = html_blocks(page)
    assert (h.line, h.source) == (2, "flowchart LR\n  A --> B")


@pytest.mark.skipif(mermaid_command() is None, reason="no Mermaid CLI (Node or mmdc)")
def test_broken_mermaid_fails_and_valid_passes(tmp_path):
    md = tmp_path / "d.md"
    md.write_text("```mermaid\nflowchart LR\n  A --> B\n```\n\n```mermaid\nflowchart LR\n  A --> B[[[\n```\n")
    blocks = markdown_blocks(md)
    failures = validate(blocks)
    assert [b.line for b, _ in failures] == [6]
    assert "Parse error" in failures[0][1]
