"""Positive controls for the rederivation test (PRD-002a), without calling the claude CLI."""

import hashlib
import json
from pathlib import Path

import pytest
import yaml

from explainer_kit import agent, artifact_eval as ae, controls


def test_controls_follow_the_eligibility_rule():
    c = controls.load_controls()
    dev = {s["id"]: s for s in ae.load("dev")[1] if "rederive" in s}
    assert sorted(c["cuts"]) == ["bloom-filter", "float-sum", "greenhouse", "heat-pump", "key-exchange", "two-tides"]
    assert set(c["cuts"]) | set(c["left_out"]) == set(dev)
    assert not set(c["cuts"]) & set(c["left_out"])
    for sid, spec in c["cuts"].items():
        kinds = [s["kind"] for s in dev[sid]["rederive"]["steps"]]
        assert spec["cut"] not in spec["clean"]
        for i in [spec["cut"], *spec["clean"]]:
            assert kinds[i - 1] == "block"
            for k in (1, 2, 3):   # reliably credited when intact (rule 4)
                g = json.loads((c["baseline"] / "rederive" / f"pass-{k}" / "grades" / f"{sid}.json").read_text())
                assert g["grades"]["principles"]["marks"][i - 1] == "supported", (sid, i, k)
    assert sum(len(s["clean"]) for s in c["cuts"].values()) == 4


def test_the_bar_is_the_prds():
    assert controls.load_controls()["bar"] == {"catch": 0.8, "min_counted": 5, "clean_losses": 1}


# ---------------------------------------------------------------- cutting

STEPS = [{"kind": "block", "text": "The Moon stretches the oceans."},
         {"kind": "block", "text": "The Sun's effect is about half the Moon's."},
         {"kind": "derived", "text": "So at right angles they work against each other."}]
TEXT = "# Tides\n\nThe Moon stretches the oceans. The Sun's effect is about half the Moon's.\n\nSo tides vary.\n"
GOOD = {"edits": [{"old": " The Sun's effect is about half the Moon's.", "new": ""}]}
BAD = {"edits": [{"old": "a sentence that is not there", "new": ""}]}
PASS = {"recoverable": False, "quote": "", "present": {"1": True}, "marked": False, "reason": "ok"}
CONDS = ("none", "principles", "quick", "published")


def tree(root):
    return {str(p.relative_to(root)): hashlib.sha256(p.read_bytes()).hexdigest() for p in root.rglob("*") if p.is_file()}


def project(monkeypatch, tmp_path, cuts=None):
    """A project in tmp_path: questions.yaml, controls.yaml, and a source run with all four conditions."""
    cuts = cuts or {"s1": {"cut": 2, "clean": [1]}, "s2": {"cut": 1, "clean": []}}
    spec = {"reader": "A reader.", "subjects": [
        {"id": sid, "split": "dev", "q": f"Question {sid}?", "misconception": "m", "quiz": [{"q": "a?", "expect": "b"}],
         "rederive": {"q": f"What follows for {sid}?", "steps": STEPS, "result": "Neap tides."}} for sid in cuts]}
    (tmp_path / "questions.yaml").write_text(yaml.safe_dump(spec, sort_keys=False))
    src = tmp_path / "src"
    for sid in cuts:
        for cond in CONDS:
            folder = src / "work" / sid / cond / "explainers" / sid
            folder.mkdir(parents=True)
            (folder / "explanation.md").write_text(TEXT if cond == "principles" else f"# {cond}\n\nOther text.\n")
            (src / "work" / sid / cond / "run.json").write_text("{}")
    (src / "conditions.json").write_text(json.dumps({c: c for c in CONDS}))
    (tmp_path / "controls.yaml").write_text(yaml.safe_dump({
        "source": "src", "baseline": "baseline", "condition": "principles", "cuts": cuts, "left_out": {},
        "bar": {"catch": 0.8, "min_counted": 5, "clean_losses": 1}}))
    monkeypatch.setattr(controls, "project_root", lambda: tmp_path)
    monkeypatch.setattr(controls, "controls_file", lambda: tmp_path / "controls.yaml")
    monkeypatch.setattr(ae, "questions_file", lambda: tmp_path / "questions.yaml")
    return src


class Agent:
    """agent.ask, routed on the system prompt: cutter and checker replies are taken in order, then the defaults."""

    def __init__(self, cuts=(), checks=()):
        self.cuts, self.checks, self.calls = list(cuts), list(checks), []

    def __call__(self, system, prompt, model=None, **kw):
        self.calls.append(system)
        if system == controls.CUTTER_SYSTEM:
            return json.dumps(self.cuts.pop(0) if self.cuts else GOOD)
        assert system == controls.CHECKER_SYSTEM
        return json.dumps(self.checks.pop(0) if self.checks else PASS)

    def count(self, system):
        return self.calls.count(system)


def record(out, sid):
    return json.loads((out / "cuts" / f"{sid}.json").read_text())


def copy_of(out, sid):
    return out / "work" / sid / controls.CUT / "explainers" / sid / "explanation.md"


def test_apply_edits_needs_each_old_exactly_once():
    assert controls.apply_edits("a b c\n\n\n\nd", [{"old": "b ", "new": ""}]) == "a c\n\nd"
    for bad in ([], [{"old": "x", "new": ""}], [{"old": "a", "new": ""}], ["loose text"], None):
        with pytest.raises(ValueError):
            controls.apply_edits("a a b", bad)


def test_cut_prompt_names_the_block_and_what_stays():
    s = {"id": "s1", "q": "Why tides?", "rederive": {"q": "How big are neap tides?", "steps": STEPS, "result": "A third."}}
    spec = {"cut": 2, "clean": [1]}
    p = controls.cut_prompt(s, "A reader.", spec, TEXT)
    assert STEPS[1]["text"] in p and STEPS[0]["text"] in p and "A reader." in p and "How big are neap tides?" in p
    assert "word for word" in p and TEXT in p
    assert "A third." not in p and STEPS[2]["text"] not in p
    c = controls.cut_check_prompt(s, "A reader.", spec, "CUT COPY")
    assert "CUT COPY" in c and STEPS[0]["text"] in c and STEPS[1]["text"] in c and "How big are neap tides?" in c
    assert '"recoverable"' in c and '"marked"' in c and '"present"' in c


def test_cut_passes_needs_every_check():
    spec = {"cut": 2, "clean": [1]}
    assert controls.cut_passes(PASS, spec)
    assert not controls.cut_passes({**PASS, "recoverable": True}, spec)
    assert not controls.cut_passes({**PASS, "marked": True}, spec)
    assert not controls.cut_passes({**PASS, "present": {"1": False}}, spec)
    assert not controls.cut_passes({**PASS, "present": {}}, spec)
    assert not controls.cut_passes({}, spec)


def test_make_cuts_writes_copy_diff_and_record(monkeypatch, tmp_path):
    src, out = project(monkeypatch, tmp_path), tmp_path / "out"
    before = tree(src)
    monkeypatch.setattr(agent, "ask", Agent())
    records = controls.make_cuts(out)
    assert sorted(records) == ["s1", "s2"]
    copy = copy_of(out, "s1")
    assert copy.read_text() == controls.apply_edits(TEXT, GOOD["edits"])
    r = record(out, "s1")
    assert r["verdict"] == "pass" and len(r["attempts"]) == 1 and r["cut"] == 2 and r["clean"] == [1]
    assert r["hash"] == hashlib.sha256(copy.read_bytes()).hexdigest()[:16]
    diff = (out / "cuts" / "s1.diff").read_text()
    assert "principles/explanation.md (cut)" in diff and "-The Moon stretches" in diff and str(tmp_path) not in diff
    for cond in ("none", "quick", "published"):
        f = Path("work") / "s1" / cond / "explainers" / "s1" / "explanation.md"
        assert (out / f).read_bytes() == (src / f).read_bytes()
    assert not (out / "work" / "s1" / "principles").exists()
    assert list(json.loads((out / "conditions.json").read_text()).items()) == [
        ("none", "none"), ("principles-cut", "principles, one block cut (PRD-002a)"), ("quick", "quick"),
        ("published", "published")]
    assert tree(src) == before


def test_a_failed_check_is_redone_then_dropped(monkeypatch, tmp_path):
    project(monkeypatch, tmp_path)
    out, fake = tmp_path / "out", Agent(checks=[{**PASS, "recoverable": True}] * 3)
    monkeypatch.setattr(agent, "ask", fake)
    controls.make_cuts(out, only=["s1"])
    r = record(out, "s1")
    assert r["verdict"] == "fail" and len(r["attempts"]) == 3 and not any(a["passed"] for a in r["attempts"])
    assert fake.count(controls.CUTTER_SYSTEM) == 3 and fake.count(controls.CHECKER_SYSTEM) == 3
    assert not copy_of(out, "s1").exists() and "hash" not in r


def test_edits_that_do_not_apply_are_asked_again_within_the_attempt(monkeypatch, tmp_path):
    project(monkeypatch, tmp_path)
    out, fake = tmp_path / "out", Agent(cuts=[BAD, GOOD])
    monkeypatch.setattr(agent, "ask", fake)
    controls.make_cuts(out, only=["s1"])
    r = record(out, "s1")
    assert r["verdict"] == "pass" and len(r["attempts"]) == 1 and fake.count(controls.CUTTER_SYSTEM) == 2

    out, fake = tmp_path / "out2", Agent(cuts=[BAD, BAD, GOOD])
    monkeypatch.setattr(agent, "ask", fake)
    controls.make_cuts(out, only=["s1"])
    r = record(out, "s1")
    assert r["verdict"] == "pass" and len(r["attempts"]) == 2
    assert r["attempts"][0]["error"] and not r["attempts"][0]["passed"] and r["attempts"][0]["check"] == {}
    assert fake.count(controls.CHECKER_SYSTEM) == 1                  # an attempt with no cut is not checked


def test_a_marked_copy_fails_its_check(monkeypatch, tmp_path):
    project(monkeypatch, tmp_path)
    out = tmp_path / "out"
    monkeypatch.setattr(agent, "ask", Agent(checks=[{**PASS, "marked": True}]))
    controls.make_cuts(out, only=["s1"])
    r = record(out, "s1")
    assert r["verdict"] == "pass" and len(r["attempts"]) == 2 and not r["attempts"][0]["passed"]


def test_a_missing_clean_block_fails_its_check(monkeypatch, tmp_path):
    project(monkeypatch, tmp_path)
    out = tmp_path / "out"
    monkeypatch.setattr(agent, "ask", Agent(checks=[{**PASS, "present": {"1": False}}]))
    controls.make_cuts(out, only=["s1"])
    assert len(record(out, "s1")["attempts"]) == 2


def test_rerun_skips_passing_cuts_and_redo_makes_one_more(monkeypatch, tmp_path):
    project(monkeypatch, tmp_path)
    out, fake = tmp_path / "out", Agent()
    monkeypatch.setattr(agent, "ask", fake)
    controls.make_cuts(out, only=["s1"])
    fake.calls.clear()
    controls.make_cuts(out, only=["s1"])
    assert fake.calls == []
    controls.make_cuts(out, only=["s1"], redo=True)
    assert fake.count(controls.CUTTER_SYSTEM) == 1 and fake.count(controls.CHECKER_SYSTEM) == 1
    assert len(record(out, "s1")["attempts"]) == 2 and record(out, "s1")["verdict"] == "pass"
    controls.make_cuts(out, only=["s1"], redo=True)
    assert len(record(out, "s1")["attempts"]) == 3
    fake.calls.clear()
    controls.make_cuts(out, only=["s1"], redo=True)
    assert fake.calls == []                                          # no attempts left


def test_cut_outputs_hold_no_absolute_paths(monkeypatch, tmp_path):
    project(monkeypatch, tmp_path)
    out = tmp_path / "out"
    monkeypatch.setattr(agent, "ask", Agent(cuts=[BAD, BAD]))
    controls.make_cuts(out)
    for f in (out / "cuts").iterdir():
        text = f.read_text()
        assert str(tmp_path) not in text and str(Path.home()) not in text, f.name


# ---------------------------------------------------------------- the verdict

BAR = {"catch": 0.8, "min_counted": 5, "clean_losses": 1}


def six(n_caught):
    return {f"s{i}": i < n_caught for i in range(6)}


def test_caught_needs_every_pass():
    assert controls.caught([["supported", "missing"], ["s", "MISSING "], ["x", "unsupported"]], 2)
    assert not controls.caught([["missing"], ["missing"], ["supported"]], 1)
    assert not controls.caught([["missing"], ["stated"], ["missing"]], 1)
    assert not controls.caught([["missing"], ["nonsense"], ["missing"]], 1)


def test_absent_raw_mark_is_not_a_catch():    # Review Focus 1
    assert not controls.caught([["missing"], None, ["missing"]], 1)
    assert not controls.caught([["missing"], [], ["missing"]], 1)
    assert not controls.caught([], 1)


def test_kept_needs_supported_in_every_pass():
    assert controls.kept([["supported"], [" Supported"], ["supported"]], 1)
    assert not controls.kept([["supported"], ["stated"], ["supported"]], 1)
    assert not controls.kept([["supported"], None, ["supported"]], 1)


def test_verdict_trusted_blind_and_floor():
    v = controls.verdict(six(5), {}, [], [], BAR)
    assert (v["verdict"], v["caught"], v["need"], len(v["counted"])) == ("trusted", 5, 5, 6)
    assert controls.verdict(six(4), {}, [], [], BAR)["verdict"] == "blind"
    floor = controls.verdict(six(6), {}, ["s0", "s1"], [], BAR)
    assert floor["verdict"] == "inconclusive" and floor["counted"] == ["s2", "s3", "s4", "s5"]
    assert controls.verdict(six(4), {}, ["s5"], [], BAR)["verdict"] == "trusted"   # 4 of 5


def test_verdict_clean_damage_is_inconclusive():
    assert controls.verdict(six(6), {"s0": 1, "s1": 1}, [], [], BAR)["verdict"] == "inconclusive"
    v = controls.verdict(six(6), {"s0": 1}, [], [], BAR)
    assert v["verdict"] == "trusted" and v["clean_losses"] == 1


def test_leak_exclusions_cannot_decide_trusted():
    v = controls.verdict({**{f"s{i}": True for i in range(4)}, "s4": False, "s5": False}, {}, [], ["s5"], BAR)
    assert (v["verdict"], v["without_leak_exclusions"]) == ("inconclusive", "blind")


def test_leak_exclusion_stands_when_not_decisive():
    v = controls.verdict(six(5), {}, [], ["s5"], BAR)
    assert (v["verdict"], v["without_leak_exclusions"]) == ("trusted", "trusted") and "s5" not in v["counted"]


def test_clean_losses_of_uncounted_subjects_are_ignored():
    assert controls.verdict(six(6), {"s0": 2}, ["s0"], [], BAR)["verdict"] == "trusted"
    assert controls.verdict(six(5), {"s5": 2}, [], ["s5"], BAR)["verdict"] == "trusted"
