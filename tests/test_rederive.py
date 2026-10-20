"""The rederivation stage, without calling the claude CLI."""

import json

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
