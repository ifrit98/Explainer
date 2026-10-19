"""The artifact eval, without calling the claude CLI."""

import json
from pathlib import Path

from explainer_kit import agent, artifact_eval as ae

ROOT = Path(__file__).resolve().parent.parent


def test_subjects_are_held_out_and_complete():
    reader, subjects = ae.load("all")
    assert reader
    ids = [s["id"] for s in subjects]
    assert len(ids) == len(set(ids)) >= 30
    assert {s["split"] for s in subjects} == {"dev", "test"}
    assert not set(ids) & {p.name for p in (ROOT / "explainers").iterdir()}   # never an example the toolkit was tuned on
    for s in subjects:
        assert s["q"] and s["misconception"] and len(s["quiz"]) >= 3
        assert s["quiz"][-1].get("kind") == "predict"
        assert all(item["q"] and item["expect"] for item in s["quiz"])


def test_conditions():
    assert ae.condition("none", "none") == {"kind": "prompt", "append": None}
    assert "explanation compiler" in ae.condition("p", "principles")["append"]
    assert ae.condition("q", "quick") == {"kind": "skill", "tier": "quick"}


def test_grounded_quotes(tmp_path):
    md = tmp_path / "explanation.md"
    md.write_text("# Sum\n\n**0.1 has no finite binary expansion**, so it is stored as the nearest double.\n")
    html = tmp_path / "index.html"
    html.write_text("<p>The rounded sum <b>prints as</b> 0.30000000000000004.</p>")
    files = [md, html]
    assert ae.grounded("0.1 has no finite binary expansion, so it is stored", files)
    assert ae.grounded("The rounded sum prints as 0.30000000000000004", files)        # across tags
    assert ae.grounded("Because 0.1 has no finite binary expansion, so it is stored as the nearest", files)
    assert not ae.grounded("IEEE 754 rounds to nearest, ties to even", files)          # outside knowledge
    assert not ae.grounded("", files)


def test_renderings_found_outside_the_expected_folder(tmp_path):
    (tmp_path / "explainers" / "x").mkdir(parents=True)
    (tmp_path / "explainers" / "x" / "model.md").write_text("model")
    (tmp_path / "out").mkdir()
    (tmp_path / "out" / "explanation.md").write_text("text")
    assert [p.name for p in ae.renderings(tmp_path, "x")] == ["explanation.md"]
    (tmp_path / "explainers" / "x" / "diagram.md").write_text("d")
    assert [p.name for p in ae.renderings(tmp_path, "x")] == ["diagram.md"]


def test_reader_and_grader_prompts_are_blind(tmp_path):
    _, subjects = ae.load("dev")
    s = subjects[0]
    rp = ae.reader_prompt([tmp_path / "explanation.md"], "a reader", s["quiz"])
    assert all(item["q"] in rp for item in s["quiz"])
    assert all(item["expect"] not in rp for item in s["quiz"])     # the reader never sees the expected answers
    assert "quote" in rp and "not covered" in rp
    gp = ae.grade_prompt(s, "a reader", {"A": {"answers": {"1": {"answer": "x"}}, "text": "body"},
                                         "B": {"answers": {}, "text": "other"}})
    assert "=== Explanation A ===" in gp and "=== Explanation B ===" in gp
    assert "principles" not in gp.lower() and "skill" not in gp.lower()   # the grader does not know the conditions
    assert s["misconception"] in gp and "rank" in gp and "least effort" in gp


def test_work_passes_tools_plugin_and_reads_json(monkeypatch, tmp_path):
    seen = {}

    class Done:
        returncode, stderr = 0, ""
        stdout = json.dumps({"result": "made explanation.md", "total_cost_usd": 0.5, "duration_ms": 61000,
                             "num_turns": 7, "is_error": False})

    def fake_run(cmd, **kw):
        seen.update(kw, cmd=cmd)
        return Done()

    monkeypatch.setattr(agent.subprocess, "run", fake_run)
    r = agent.work("task", tmp_path, ["Read", "Bash"], ["Read", "Bash(explainer:*)"], plugin_dir=tmp_path)
    assert r == {"result": "made explanation.md", "error": None, "cost": 0.5, "seconds": 61, "turns": 7}
    cmd = seen["cmd"]
    assert cmd[:3] == ["claude", "-p", "task"] and seen["stdin"] is agent.subprocess.DEVNULL
    assert cmd[cmd.index("--tools") + 1] == "Read,Bash" and "--plugin-dir" in cmd and seen["cwd"] == tmp_path


def fake_run_folder(tmp_path, subject, names):
    for n, score in zip(names, ([2, 2, 1], [1, 0, 0])):
        ws = tmp_path / "work" / subject["id"] / n
        (ws / "explainers" / subject["id"]).mkdir(parents=True)
        (ws / "explainers" / subject["id"] / "explanation.md").write_text("word " * (100 if n == "a" else 300))
        (ws / "run.json").write_text(json.dumps({"files": [], "cost": 1.0, "seconds": 120, "error": None}))
        (ws / "read.json").write_text(json.dumps({"answers": {}, "stops": ["s"] * score[0], "excess": [],
                                                  "grounded": {"1": True, "2": True, "3": n == "a", "4": True}}))
    return {subject["id"]: {"rank": ["a", "b"], "why_best": "shorter", "grades": {"a": {"quiz": [2, 2, 1, 2], "misconception": "corrected", "errors": []},
                                       "b": {"quiz": [1, 0, 2, 1], "misconception": "taught", "errors": ["e"]}}}}


def test_summary_counts_only_grounded_answers(tmp_path):
    _, subjects = ae.load("dev")
    s = subjects[0]
    grades = fake_run_folder(tmp_path, s, ["a", "b"])
    report = ae.summary({"a": "none", "b": "quick"}, [s], tmp_path, grades, "dev", None)
    # b's third answer scored 2 but its quote was not found: it counts as 0 and as one ungrounded answer
    assert "| a | 1.0 | 1/1 | 88% | 100% | 88% | 0 | 0 | 1 |" in report
    assert "| b | 2.0 | 0/1 | 25% | 50% | 50% | 1 | 1 | 0 | 1 |" in report
    assert "a > b. shorter" in report
    assert f"| {s['id']} | 7 (100 w) | 2 ✗ (300 w) |" in report



def test_builds_run_outside_every_project(tmp_path):
    # Inside a project, Claude Code loads its CLAUDE.md (here: the principles) whatever the condition.
    assert ae.inside_project(ROOT / "evals" / "artifact") == ROOT
    (tmp_path / "a" / "b").mkdir(parents=True)
    assert ae.inside_project(tmp_path / "a" / "b") is None
    (tmp_path / "CLAUDE.md").write_text("x")
    assert ae.inside_project(tmp_path / "a" / "b") == tmp_path


def test_ask_reports_usage(monkeypatch):
    class Done:
        returncode, stderr = 0, ""
        stdout = json.dumps({"result": " ok ", "total_cost_usd": 0.25, "duration_ms": 3000})

    seen = {}
    monkeypatch.setattr(agent.subprocess, "run", lambda cmd, **kw: seen.update(cmd=cmd) or Done())
    usage = {"cost": 0.5}
    assert agent.ask("s", "p", usage=usage) == "ok"
    assert usage == {"cost": 0.75, "seconds": 3} and "--output-format" in seen["cmd"]


def test_reader_reply_accepts_answers_at_the_top_level():
    a = {"answer": "x", "quote": "y"}
    assert ae.reader_reply(json.dumps({"answers": {"1": a}, "stops": ["s"]}), 4)["answers"] == {"1": a}
    assert ae.reader_reply(json.dumps({"1": a, "2": a, "stops": []}), 4)["answers"] == {"1": a, "2": a}
    assert ae.reader_reply(json.dumps(a), 4)["answers"] == {}          # one bare answer: no numbered answers
    assert ae.reader_reply("no json", 4) == {"answers": {}, "stops": [], "excess": []}
