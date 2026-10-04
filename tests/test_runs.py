"""Review runs and the adoption log, without calling the claude CLI."""

import json

from explainer_kit import runs


def _record(tool="coldread"):
    reply = {"blocking": ["Nothing blocks the main line.", "line 3: 'n' is never defined"],
             "cuts": ["the aside in line 9"],
             "paragraphs": [{"at": "line 3", "unresolved": ["n"], "leap": [], "excess": ["x"]}]}
    return {"tool": tool, "rendering": "prose", "reply": reply}


def test_coldread_findings_skip_an_empty_blocking_answer():
    found = runs.extract(_record())
    assert [f["severity"] for f in found] == ["blocking", "excess", "edge"]
    assert "never defined" in found[0]["text"]


def test_decisions_and_stats(tmp_path, monkeypatch):
    folder = tmp_path / "explainers" / "x"
    (folder / "review" / "runs").mkdir(parents=True)
    rec = _record()
    rec["findings"] = runs.extract(rec)
    (folder / "review" / "runs" / "2026-01-01T000000-coldread-prose.json").write_text(json.dumps(rec))
    monkeypatch.setattr(runs, "explainer_dir", lambda slug: folder)
    runs.decide("x", "2026-01-01T000000-coldread-prose", adopt=[1], decline=[], decline_rest=True)
    table = runs.stats(tmp_path / "explainers")
    assert "coldread   blocking          1        1        1      100%" in table
    assert "coldread   edge              1        1        0        0%" in table
    assert "adopted" in runs.show("x")


def test_reviewer_reads_only_the_explainer_folder(monkeypatch, tmp_path):
    seen = {}
    monkeypatch.setattr(runs, "ask", lambda system, prompt, model=None, read=None: (seen.update(read=read), '{"gaps": []}')[1])
    folder = tmp_path / "explainers" / "x"
    (folder / "review").mkdir(parents=True)
    (folder / "model.md").write_text("# x\n")
    monkeypatch.setattr(runs, "explainer_dir", lambda slug: folder)
    monkeypatch.setattr(runs, "probe_prompt", lambda slug: "probe")
    path = runs.run_review("x", "probe")
    assert seen["read"] == [folder] and json.loads(path.read_text())["findings"] == []
