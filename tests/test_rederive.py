"""The rederivation stage, without calling the claude CLI."""

import hashlib
import json
import re
import sys
from pathlib import Path

import pytest
import yaml

from explainer_kit import agent, artifact_eval as ae, rederive

TARGET = {"q": "What follows?",
          "steps": [{"kind": "block", "text": "Idea one."}, {"kind": "block", "text": "Idea two."},
                    {"kind": "derived", "text": "So three."}],
          "result": "Three."}


def target(**change):
    return {**json.loads(json.dumps(TARGET)), **change}


def test_target_problems():
    assert rederive.target_problems(target()) == []
    steps = TARGET["steps"]
    assert rederive.target_problems(target(steps=steps[:2]))
    assert rederive.target_problems(target(steps=steps + steps + steps[:1]))                  # 7 steps
    assert rederive.target_problems(target(steps=[{**s, "kind": "block"} for s in steps]))     # nothing derived
    assert rederive.target_problems(target(steps=[{"kind": "lemma", "text": "x"}, *steps[1:]]))
    assert rederive.target_problems(target(result=""))
    assert rederive.target_problems({k: v for k, v in TARGET.items() if k != "q"})


def test_target_hash_is_stable_and_sensitive():
    reordered = {"result": TARGET["result"], "steps": TARGET["steps"], "q": TARGET["q"]}
    assert rederive.target_hash(reordered) == rederive.target_hash(TARGET)
    assert len(rederive.target_hash(TARGET)) == 12
    changed = target(steps=[{"kind": "block", "text": "Idea one!"}, *TARGET["steps"][1:]])
    assert rederive.target_hash(changed) != rederive.target_hash(TARGET)


def test_check_prompt_shows_the_building_blocks():
    reader, subjects = ae.load("dev")
    s = {**subjects[0], "rederive": TARGET}
    p = rederive.check_prompt(s, reader)
    assert reader in p and s["q"] in p and TARGET["q"] in p and TARGET["result"] in p
    assert all(item["expect"] in p for item in s["quiz"])
    assert all(f"({step['kind']}) {step['text']}" in p for step in TARGET["steps"])
    assert "any valid derivation needs" in p and "would not state" in p and "no new fact about the subject" in p


def subjects_file(tmp_path, targets):
    spec = {"reader": "A reader.", "subjects": [
        {"id": sid, "split": "dev", "q": f"Question {sid}?", "misconception": "m",
         "quiz": [{"q": "a?", "expect": "b"}], "rederive": t} for sid, t in targets.items()]}
    path = tmp_path / "questions.yaml"
    path.write_text(yaml.safe_dump(spec, sort_keys=False))
    return path


def test_check_targets_records_and_resumes(monkeypatch, tmp_path):
    checks = tmp_path / "checks.json"
    monkeypatch.setattr(rederive, "checks_file", lambda: checks)
    monkeypatch.setattr(ae, "questions_file", lambda: subjects_file(tmp_path, {"s1": target(), "s2": target(q="Why?")}))
    asked = []

    def ask(system, prompt, model=None, **kw):
        sid = "s2" if "Question s2?" in prompt else "s1"
        asked.append(sid)
        tests = {"correct": True, "blocks": True, "derived_follow": sid == "s1", "steps": True, "not_stated": True}
        return json.dumps({"verdict": "pass", "tests": tests, "reason": "ok"})   # the verdict is computed, not read

    monkeypatch.setattr(agent, "ask", ask)
    rederive.check_targets()
    saved = json.loads(checks.read_text())
    assert saved["s1"]["verdict"] == "pass" and saved["s2"]["verdict"] == "fail"
    assert saved["s1"]["hash"] == rederive.target_hash(target())
    assert saved["s2"]["hash"] == rederive.target_hash(target(q="Why?"))
    assert saved["s1"]["attempt"] == saved["s2"]["attempt"] == 1
    assert checks.read_text().endswith("\n") and list(saved) == ["s1", "s2"]

    asked.clear()
    rederive.check_targets()
    assert asked == []                                           # unchanged targets are not checked again

    monkeypatch.setattr(ae, "questions_file", lambda: subjects_file(tmp_path, {"s1": target(), "s2": target(q="How?")}))
    rederive.check_targets()
    saved = json.loads(checks.read_text())
    assert asked == ["s2"] and saved["s2"]["attempt"] == 2 and saved["s1"]["attempt"] == 1


def test_every_subject_has_a_checked_target():
    # Targets are frozen once checked: a target that changed since its check, or a subject with neither a passing
    # target nor a record of three failed attempts, fails here.
    checks = json.loads(rederive.checks_file().read_text())
    for s in ae.load("all")[1]:
        c = checks.get(s["id"], {})
        if "rederive" in s:
            assert rederive.target_problems(s["rederive"]) == [], s["id"]
            assert c.get("verdict") == "pass" and c.get("hash") == rederive.target_hash(s["rederive"]), s["id"]
        else:
            assert c.get("verdict") == "fail" and c.get("attempt") == 3, s["id"]


CHAIN = {"steps": [{"step": "One holds.", "part": "Section 'Adding'", "idea": "bits are set"},
                   {"step": "So three.", "part": "step 1", "idea": "follows"}], "result": "Three.", "gap": ""}


def tree(root):
    return {str(p.relative_to(root)): hashlib.sha256(p.read_bytes()).hexdigest() for p in root.rglob("*") if p.is_file()}


def builds_folder(tmp_path, sid="s1", texts=None):
    builds = tmp_path / "builds"
    for cond, text in (texts or {"a": "ALPHA explains it.", "b": "BETA explains it."}).items():
        folder = builds / "work" / sid / cond / "explainers" / sid
        folder.mkdir(parents=True)
        if text is not None:
            (folder / "explanation.md").write_text(f"# Title\n\n{text}\n")
        (builds / "work" / sid / cond / "run.json").write_text("{}")
    return builds


def test_reader_prompt_is_blind_to_steps_and_result(tmp_path):
    reader, subjects = ae.load("dev")
    t = subjects[0]["rederive"]
    files = [tmp_path / "explanation.md", tmp_path / "index.html"]
    p = rederive.reader_prompt(files, reader, t["q"])
    assert t["q"] in p and rederive.OUTSIDE_RULE in p and all(str(f) in p for f in files)
    assert '"gap"' in p and '"part"' in p
    assert all(s["text"] not in p for s in t["steps"]) and t["result"] not in p


def test_chain_reply_tolerates_shapes():
    assert rederive.chain_reply(json.dumps(CHAIN)) == CHAIN
    assert rederive.chain_reply(json.dumps({"steps": "x", "result": "r"}))["steps"] == []
    assert rederive.chain_reply("no json") == {"steps": [], "result": "", "gap": ""}
    mixed = {"steps": ["loose text", CHAIN["steps"][0]], "result": "r", "gap": ""}
    assert rederive.chain_reply(json.dumps(mixed))["steps"] == [CHAIN["steps"][0]]


def test_chain_text_numbers_steps():
    lines = rederive.chain_text(CHAIN).splitlines()
    assert lines[0].startswith("1. One holds.") and "Section 'Adding'" in lines[0] and "bits are set" in lines[0]
    assert lines[1].startswith("2. So three.")
    assert lines[-1] == "Result: Three."


def test_read_chain_uses_copies_and_leaves_builds_untouched(monkeypatch, tmp_path):
    builds, out = builds_folder(tmp_path), tmp_path / "out"
    before, seen = tree(builds), []

    def ask(system, prompt, model=None, read=None, **kw):
        seen.append(read)
        return json.dumps(CHAIN)

    monkeypatch.setattr(agent, "ask", ask)
    s = {"id": "s1", "rederive": TARGET}
    assert rederive.read_chain(s, "a", "A reader.", builds, out, 1, None)["steps"] == CHAIN["steps"]
    assert len(seen) == 1 and all(builds.resolve() not in Path(d).resolve().parents for d in seen[0])
    assert (out / "rederive" / "pass-1" / "read" / "s1" / "a.json").exists()
    rederive.read_chain(s, "a", "A reader.", builds, out, 1, None)
    assert len(seen) == 1                                          # saved: not read again
    assert tree(builds) == before


def test_read_chain_skips_a_build_with_no_renderings(monkeypatch, tmp_path):
    builds = builds_folder(tmp_path, texts={"a": None})
    monkeypatch.setattr(agent, "ask", lambda *a, **k: pytest.fail("no explanation, so no reader"))
    r = rederive.read_chain({"id": "s1", "rederive": TARGET}, "a", "A reader.", builds, tmp_path / "out", 1, None)
    assert r["missing"] is True and r["steps"] == []


def test_grader_text_includes_page_scripts(tmp_path):
    html = tmp_path / "index.html"
    html.write_text("<p>Drag the slider</p><script>const loss = x => x * x</script>")
    assert "const loss" not in ae.shown_text(html)                 # the visible text alone misses what a control shows
    text = rederive.grader_text(html)
    assert "Drag the slider" in text and "const loss" in text
    md = tmp_path / "explanation.md"
    md.write_text("# T\n\nBody `x = 1`.\n<!-- note -->\n")
    assert rederive.grader_text(md) == ae.shown_text(md)


def test_grade_prompt_is_blind_and_carries_the_rule():
    reader, subjects = ae.load("dev")
    s = subjects[0]
    p = rederive.grade_prompt(s, reader, {"A": {"text": "body", "chain": rederive.chain_text(CHAIN)},
                                          "B": {"text": "other", "chain": "(no chain)"}})
    assert rederive.OUTSIDE_RULE in p and s["rederive"]["result"] in p
    assert all(f"({step['kind']}) {step['text']}" in p for step in s["rederive"]["steps"])
    assert "=== Explanation A ===" in p and "=== Explanation B ===" in p and rederive.chain_text(CHAIN) in p
    assert "any order" in p and "stated" in p
    assert "principles" not in p.lower() and "skill" not in p.lower()   # the grader does not know the conditions


def test_marks_are_normalised():
    assert rederive.marks(["supported", "stated", "bogus"], ["block", "block", "derived", "derived"]) == \
        ["supported", "supported", "missing", "missing"]                # "stated" on a building block is supported
    assert rederive.marks("x", ["block"]) == ["missing"]
    assert rederive.marks(["supported", "unsupported", "supported"], ["block", "derived"]) == ["supported", "unsupported"]


def test_tally():
    marks, kinds = ["supported", "unsupported", "stated", "missing"], ["block", "derived", "derived", "derived"]
    assert rederive.tally(marks, kinds, True, False) == \
        {"supported": 1, "made": 2, "counted": 3, "stated": 1, "right": 1, "results": 1, "results_stated": 0}
    t = rederive.tally(marks, kinds, True, True)                     # a stated result is left out of the result score
    assert t["right"] == 0 and t["results"] == 0 and t["results_stated"] == 1


def test_pass_scores_pool_subjects():
    base = {"stated": 0, "results_stated": 0}
    scores = rederive.pass_scores({
        "a": [{**base, "supported": 1, "made": 2, "counted": 2, "right": 1, "results": 1},
              {**base, "supported": 2, "made": 2, "counted": 3, "right": 0, "results": 1}],
        "b": [{**base, "supported": 0, "made": 0, "counted": 2, "right": 0, "results": 0, "results_stated": 1}],
    })
    assert scores["a"] == {"supported": 0.6, "raw": 0.8, "result": 0.5}
    assert scores["b"]["result"] is None


def test_separations_need_every_pass():
    assert rederive.separations([
        {"a": {"supported": .7}, "b": {"supported": .5}, "c": {"supported": .6}},
        {"a": {"supported": .7}, "b": {"supported": .5}, "c": {"supported": .4}},
        {"a": {"supported": .6}, "b": {"supported": .6}, "c": {"supported": .3}},
    ]) == [("a", "c")]


def test_grade_subject_maps_labels_back_and_fills_missing(monkeypatch, tmp_path):
    builds, out = builds_folder(tmp_path), tmp_path / "out"
    s = {"id": "s1", "q": "Question?", "rederive": TARGET}
    for cond in ("a", "b"):
        f = out / "rederive" / "pass-1" / "read" / "s1" / f"{cond}.json"
        f.parent.mkdir(parents=True, exist_ok=True)
        f.write_text(json.dumps(CHAIN))
    calls = []

    def ask(system, prompt, model=None, **kw):
        calls.append(prompt)
        return json.dumps({"grades": {"A": {"marks": ["supported", "supported", "stated"], "result_right": True,
                                            "result_stated": False}}})

    monkeypatch.setattr(agent, "ask", ask)
    g = rederive.grade_subject(s, {"A": "b", "B": "a"}, "A reader.", builds, out, 1, None)
    assert g["grades"]["b"] == {"marks": ["supported", "supported", "stated"], "result_right": True, "result_stated": False}
    assert g["grades"]["a"] == {"marks": ["missing"] * 3, "result_right": False, "result_stated": False}
    assert "BETA" in calls[0].split("=== Explanation A ===")[1].split("=== Explanation B ===")[0]
    assert (out / "rederive" / "pass-1" / "grades" / "s1.json").exists()
    rederive.grade_subject(s, {"A": "b", "B": "a"}, "A reader.", builds, out, 1, None)
    assert len(calls) == 1


ROOT = Path(__file__).resolve().parent.parent


def run_fixture(monkeypatch, tmp_path):
    """One subject, two conditions (a: ALPHA, b: BETA), a stub reader, and a grader that supports every step of the
    ALPHA explanation and none of the other. Returns builds, out, and the list of calls."""
    monkeypatch.setattr(ae, "questions_file", lambda: subjects_file(tmp_path, {"s1": target()}))
    builds = builds_folder(tmp_path)
    (builds / "conditions.json").write_text(json.dumps({"a": "none", "b": "quick"}))
    (builds / "scores.json").write_text(json.dumps({
        "a": {"subjects": [{"id": "s1", "score": [2, 2, 1, 2], "raw": [2, 2, 2, 2]}]},
        "b": {"subjects": [{"id": "s1", "score": [1, 0, 0, 0], "raw": [1, 0, 2, 0]}]}}))
    calls = []

    def ask(system, prompt, model=None, **kw):
        calls.append(system)
        if system == ae.READER_SYSTEM:
            return json.dumps(CHAIN)
        blocks = dict(re.findall(r"=== Explanation (\w) ===\n(.*?)(?==== Explanation|\Z)", prompt, re.S))
        return json.dumps({"grades": {lab: {"marks": ["supported" if "ALPHA" in b else "missing"] * 3,
                                            "result_right": "ALPHA" in b, "result_stated": False}
                                      for lab, b in blocks.items()}})

    monkeypatch.setattr(agent, "ask", ask)
    return builds, tmp_path / "out", calls


def test_run_end_to_end(monkeypatch, tmp_path):
    builds, out, calls = run_fixture(monkeypatch, tmp_path)
    report = rederive.run(out, builds).read_text()
    assert calls.count(ae.READER_SYSTEM) == 3 * 2 and calls.count(ae.GRADER_SYSTEM) == 3
    assert ("| condition | supported | raw | result right | stated steps | stated results | words | quiz (grounded) |"
            in report)
    assert "| a | 100%, 100%, 100% | 100%, 100%, 100% |" in report
    assert "| b | 0%, 0%, 0% | 0%, 0%, 0% |" in report
    assert "Separation (higher supported score in all three passes): a > b." in report
    assert "| s1 | 3/3, 3/3, 3/3 | 0/3, 0/3, 0/3 |" in report
    scores = json.loads((out / "rederive-scores.json").read_text())
    assert scores["separations"] == [["a", "b"]] and len(scores["passes"]) == 3


def test_rerun_makes_no_calls(monkeypatch, tmp_path):
    builds, out, calls = run_fixture(monkeypatch, tmp_path)
    first = rederive.run(out, builds).read_text()
    calls.clear()
    assert rederive.run(out, builds).read_text() == first and calls == []


def test_rerun_refuses_changed_targets(monkeypatch, tmp_path):
    builds, out, _ = run_fixture(monkeypatch, tmp_path)
    rederive.run(out, builds)
    monkeypatch.setattr(ae, "questions_file", lambda: subjects_file(tmp_path, {"s1": target(result="Four.")}))
    with pytest.raises(SystemExit, match="targets changed since this run: s1"):
        rederive.run(out, builds)


def test_outputs_hold_no_absolute_paths(monkeypatch, tmp_path):
    builds, out, _ = run_fixture(monkeypatch, tmp_path)
    rederive.run(out, builds)
    leaks = [p for p in out.rglob("*") if p.is_file() and str(tmp_path) in p.read_text()]
    assert not leaks, leaks
    assert json.loads((out / "rederive" / "source.json").read_text()) == {"builds": "builds"}   # outside the project: its name


def test_source_names_builds_inside_the_project_relative_to_it(monkeypatch, tmp_path):
    # A path relative to --out climbs through the home folder when --out is elsewhere (a scratch folder).
    builds, _, _ = run_fixture(monkeypatch, tmp_path)
    monkeypatch.setattr(rederive, "project_root", lambda: tmp_path)
    out = tmp_path.parent / f"{tmp_path.name}-elsewhere" / "deep" / "out"
    rederive.run(out, builds)
    assert json.loads((out / "rederive" / "source.json").read_text()) == {"builds": "builds"}
    assert "Builds: `builds`." in (out / "rederive.md").read_text()


def test_builds_folder_is_untouched(monkeypatch, tmp_path):
    builds, out, _ = run_fixture(monkeypatch, tmp_path)
    before = tree(builds)
    rederive.run(out, builds)
    assert tree(builds) == before


def test_frozen_targets_match_every_results_folder():
    # A results folder records the targets it ran; they must still be the targets in questions.yaml (the freeze).
    current = {s["id"]: s.get("rederive") for s in ae.load("all")[1]}
    for snap in (ROOT / "evals" / "artifact" / "results").glob("*/rederive/targets.json"):
        for sid, t in json.loads(snap.read_text()).items():
            assert current.get(sid) == t, f"{snap.parent.parent.name}: the target for {sid} changed after the run"


def test_cli_rederive_and_artifact_call_the_stage(monkeypatch, tmp_path):
    from explainer_kit import cli

    seen = []
    monkeypatch.setattr(rederive, "run", lambda out, builds, **kw: seen.append(("rederive", out, builds)))
    monkeypatch.setattr(ae, "run", lambda conditions, out, **kw: seen.append(("artifact", out)))
    b, o = tmp_path / "b", tmp_path / "o"
    monkeypatch.setattr(sys, "argv", ["explainer", "eval", "rederive", "--builds", str(b), "--out", str(o)])
    cli.main()
    assert seen == [("rederive", o, b)]
    seen.clear()
    monkeypatch.setattr(sys, "argv", ["explainer", "eval", "artifact", "--out", str(o)])
    cli.main()
    assert seen == [("artifact", o), ("rederive", o, o)]
