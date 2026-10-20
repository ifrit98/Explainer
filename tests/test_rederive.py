"""The rederivation stage, without calling the claude CLI."""

import hashlib
import json
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
