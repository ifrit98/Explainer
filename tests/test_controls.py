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


def project(monkeypatch, tmp_path, cuts=None, bar=None, left_out=None):
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
        "source": "src", "baseline": "baseline", "condition": "principles", "cuts": cuts, "left_out": left_out or {},
        "bar": bar or {"catch": 0.8, "min_counted": 5, "clean_losses": 1}}))
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



# ---------------------------------------------------------------- the controls run

CHAIN = {"steps": [{"step": "The Moon stretches.", "part": "Section 'Tides'", "idea": "stretching"}],
         "result": "Neap tides.", "gap": ""}
CUT_TEXT = controls.apply_edits(TEXT, GOOD["edits"])
SMALL = {"catch": 0.5, "min_counted": 1, "clean_losses": 1}
CAUGHT = {"s1": ["supported", "missing", "supported"], "s2": ["unsupported", "supported", "supported"]}


def baseline_folder(tmp_path, sids=("s1", "s2")):
    stage = tmp_path / "baseline" / "rederive"
    for k in (1, 2, 3):
        for sid in sids:
            for cond in CONDS:
                f = stage / f"pass-{k}" / "read" / sid / f"{cond}.json"
                f.parent.mkdir(parents=True, exist_ok=True)
                f.write_text(json.dumps({**CHAIN, "result": f"{cond} pass {k}"}))
            g = stage / f"pass-{k}" / "grades" / f"{sid}.json"
            g.parent.mkdir(parents=True, exist_ok=True)
            g.write_text(json.dumps({"key": {}, "grades": {c: {"marks": ["supported"] * 3, "result_right": True,
                                                                "result_stated": False} for c in CONDS}}))
    return tmp_path / "baseline"


class Stage:
    """agent.ask for the controls run: the reader must see the cut copy; the grader gives every label the marks set
    for (subject, pass); the leak checker gives one reply."""

    def __init__(self, marks=None, leak=None):
        self.marks, self.leak = marks or {}, leak or {"leak": False, "quote": ""}
        self.calls, self.prompts, self.graded = [], [], {}

    def __call__(self, system, prompt, model=None, read=None, **kw):
        self.calls.append(system)
        self.prompts.append(prompt)
        if system == ae.READER_SYSTEM:
            texts = [f.read_text() for d in read for f in Path(d).rglob("*") if f.is_file()]
            assert texts == [CUT_TEXT]
            return json.dumps(CHAIN)
        if system == ae.GRADER_SYSTEM:
            sid = "s1" if "Question s1?" in prompt else "s2"
            k = self.graded[sid] = self.graded.get(sid, 0) + 1
            m = self.marks.get((sid, k), CAUGHT[sid])
            return json.dumps({"grades": {lab: {"marks": m, "result_right": True, "result_stated": False}
                                          for lab in "ABCD"}})
        assert system == controls.LEAK_SYSTEM
        return json.dumps(self.leak)

    def count(self, system):
        return self.calls.count(system)


def cut_folder(monkeypatch, tmp_path, **kw):
    src = project(monkeypatch, tmp_path, bar=SMALL, left_out={"s9": "Its question gives the block away."}, **kw)
    base, out = baseline_folder(tmp_path), tmp_path / "out"
    monkeypatch.setattr(agent, "ask", Agent())
    controls.make_cuts(out)
    return src, base, out


def outputs(out):
    return {str(f.relative_to(out)): f.read_text() for f in out.rglob("*") if f.is_file() and f.suffix in (".json", ".md")}


def test_controls_end_to_end(monkeypatch, tmp_path):
    src, base, out = cut_folder(monkeypatch, tmp_path)
    stage = Stage()
    monkeypatch.setattr(agent, "ask", stage)
    report = controls.run(out, workers=1)
    assert report == out / "controls.md"
    assert stage.count(ae.READER_SYSTEM) == 6 and stage.count(ae.GRADER_SYSTEM) == 6
    for k in (1, 2, 3):
        for cond in ("none", "quick", "published"):
            rel = Path("rederive") / f"pass-{k}" / "read" / "s1" / f"{cond}.json"
            assert (out / rel).read_text() == (base / rel).read_text()
    result = json.loads((out / "controls.json").read_text())
    expected = controls.verdict({"s1": True, "s2": True}, {"s1": 0, "s2": 0}, [], [], SMALL)
    assert {k: result[k] for k in expected} == expected and result["verdict"] == "trusted"
    md = report.read_text()
    assert "s9" in md and "Its question gives the block away." in md and "trusted" in md
    assert "shuffle" in md
    assert all("principles-cut" not in p for p in stage.prompts)
    for name, text in outputs(out).items():
        assert str(tmp_path) not in text and str(Path.home()) not in text, name


def test_run_refuses_unfinished_cuts(monkeypatch, tmp_path):
    _, _, out = cut_folder(monkeypatch, tmp_path)
    (out / "cuts" / "s2.json").unlink()
    with pytest.raises(SystemExit, match="s2"):
        controls.run(out)
    r = json.loads((out / "cuts" / "s1.json").read_text())
    (out / "cuts" / "s1.json").write_text(json.dumps({**r, "verdict": "pending"}))
    with pytest.raises(SystemExit, match="s1"):
        controls.run(out)


def test_run_refuses_a_changed_cut_copy(monkeypatch, tmp_path):     # Review Focus 2
    _, _, out = cut_folder(monkeypatch, tmp_path)
    copy = copy_of(out, "s1")
    copy.write_text(copy.read_text() + "One more line.\n")
    monkeypatch.setattr(agent, "ask", lambda *a, **k: pytest.fail("no calls before the cuts are checked"))
    with pytest.raises(SystemExit, match="s1"):
        controls.run(out)


def test_leak_needs_a_quote_found_in_the_copy():
    assert controls.quote_in("a  b\n c", "x a b c y")
    assert not controls.quote_in("", "x a b c y") and not controls.quote_in("  ", "x a b c y")
    assert not controls.quote_in("not there", "x a b c y")
    p = controls.leak_prompt("The Sun is half.", CHAIN, "EXPLANATION TEXT")
    assert "The Sun is half." in p and "EXPLANATION TEXT" in p and "Section 'Tides'" in p and '"quote"' in p


def test_leak_check_runs_only_for_uncaught_passes(monkeypatch, tmp_path):
    _, _, out = cut_folder(monkeypatch, tmp_path)
    stage = Stage(marks={("s2", 2): ["supported", "supported", "supported"]},
                  leak={"leak": True, "quote": "The Moon   stretches the oceans."})
    monkeypatch.setattr(agent, "ask", stage)
    controls.run(out, workers=1)
    assert stage.count(controls.LEAK_SYSTEM) == 1
    saved = json.loads((out / "controls" / "leaks" / "s2-pass-2.json").read_text())
    assert saved["confirmed"] is True
    result = json.loads((out / "controls.json").read_text())
    assert result["leaked"] == ["s2"] and result["counted"] == ["s1"]


def test_an_unconfirmed_leak_is_a_miss(monkeypatch, tmp_path):
    _, _, out = cut_folder(monkeypatch, tmp_path)
    stage = Stage(marks={("s2", 2): ["supported", "supported", "supported"]},
                  leak={"leak": True, "quote": "a passage that is not in the copy"})
    monkeypatch.setattr(agent, "ask", stage)
    controls.run(out, workers=1)
    result = json.loads((out / "controls.json").read_text())
    assert result["leaked"] == [] and result["counted"] == ["s1", "s2"] and result["caught"] == 1


def test_controls_rerun_makes_no_calls(monkeypatch, tmp_path):     # Review Focus 4
    _, _, out = cut_folder(monkeypatch, tmp_path)
    stage = Stage(marks={("s2", 1): ["supported", "supported", "supported"]})
    monkeypatch.setattr(agent, "ask", stage)
    controls.run(out, workers=1)
    assert stage.count(controls.LEAK_SYSTEM) == 1
    monkeypatch.setattr(agent, "ask", lambda *a, **k: pytest.fail("everything is saved"))
    controls.run(out, workers=1)


def test_baseline_and_source_are_untouched(monkeypatch, tmp_path):
    src, base, out = cut_folder(monkeypatch, tmp_path)
    before = (tree(src), tree(base))
    monkeypatch.setattr(agent, "ask", Stage())
    controls.run(out, workers=1)
    assert (tree(src), tree(base)) == before


def test_a_dropped_cut_is_not_run(monkeypatch, tmp_path):
    project(monkeypatch, tmp_path, bar=SMALL)
    baseline_folder(tmp_path)
    out = tmp_path / "out"
    monkeypatch.setattr(agent, "ask", Agent(checks=[{**PASS, "recoverable": True}] * 3))
    controls.make_cuts(out, only=["s2"])
    monkeypatch.setattr(agent, "ask", Agent())
    controls.make_cuts(out, only=["s1"])
    stage = Stage()
    monkeypatch.setattr(agent, "ask", stage)
    controls.run(out, workers=1)
    result = json.loads((out / "controls.json").read_text())
    assert result["dropped"] == ["s2"] and result["counted"] == ["s1"] and stage.count(ae.READER_SYSTEM) == 3


def test_cli_cuts_and_controls_call_the_module(monkeypatch, tmp_path, capsys):
    import sys

    from explainer_kit import cli

    seen = []

    def make_cuts(out, only=None, redo=False, model=None):
        seen.append(("cuts", out, only, redo, model))
        return {"s1": {"verdict": "pass", "attempts": [{}]}}

    def run(out, model=None, reader_model=None, workers=4):
        seen.append(("controls", out, model, reader_model, workers))
        (out / "controls.json").write_text(json.dumps({"verdict": "trusted", "caught": 5, "counted": ["a"] * 6,
                                                       "need": 5, "without_leak_exclusions": "trusted"}))
        return out / "controls.md"

    monkeypatch.setattr(controls, "make_cuts", make_cuts)
    monkeypatch.setattr(controls, "run", run)
    o = tmp_path / "o"
    o.mkdir()
    monkeypatch.setattr(sys, "argv", ["explainer", "eval", "cuts", "--only", "s1", "--redo", "--out", str(o)])
    cli.main()
    monkeypatch.setattr(sys, "argv", ["explainer", "eval", "controls", "--out", str(o), "--reader-model", "r",
                                      "--workers", "2"])
    cli.main()
    assert seen == [("cuts", o, ["s1"], True, None), ("controls", o, None, "r", 2)]
    printed = capsys.readouterr().out
    assert "s1" in printed and "pass" in printed and "trusted" in printed
    monkeypatch.setattr(sys, "argv", ["explainer", "eval", "controls"])
    with pytest.raises(SystemExit, match="needs --out"):
        cli.main()


# ---------------------------------------------------------------- the real cuts, frozen before the controls run

ROOT = Path(__file__).resolve().parent.parent
CONTROLS = ROOT / "evals" / "artifact" / "results" / "2026-10-29-dev-controls"
FROZEN_CUTS = "f634b324da00c71c"   # controls.yaml plus every cut record and copy, as frozen before the controls run


def frozen_digest() -> str:
    h = hashlib.sha256(controls.controls_file().read_bytes())
    for sid in sorted(controls.load_controls()["cuts"]):
        rec = json.loads((CONTROLS / "cuts" / f"{sid}.json").read_text())
        copy = controls.cut_copy(CONTROLS, sid)
        h.update(f"{sid}\0{rec['verdict']}\0{rec.get('hash', '')}\0".encode())
        h.update(copy.read_bytes() if copy else b"")
    return h.hexdigest()[:16]


def test_cuts_are_the_frozen_ones():
    assert frozen_digest() == FROZEN_CUTS, "a cut changed after the freeze"


def test_uncut_builds_match_the_source():
    c = controls.load_controls()
    for sid in c["cuts"]:
        if json.loads((CONTROLS / "cuts" / f"{sid}.json").read_text())["verdict"] != "pass":
            continue
        for cond in controls.UNCUT:
            src, ours = c["source"] / "work" / sid / cond, CONTROLS / "work" / sid / cond
            theirs = {f.relative_to(src): f.read_bytes() for f in ae.renderings(src, sid)}
            assert theirs and {f.relative_to(ours): f.read_bytes() for f in ae.renderings(ours, sid)} == theirs, \
                (sid, cond)
