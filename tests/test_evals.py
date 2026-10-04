"""The chat eval, without calling the claude CLI."""

from explainer_kit import evals


def test_questions_have_points_a_misconception_and_a_budget():
    spec = evals.load_questions()
    assert spec["reader"]
    assert len(spec["questions"]) >= 5
    for q in spec["questions"]:
        assert q["q"] and len(q["must"]) >= 2 and q["misconception"] and q["budget"] > 0


def test_system_prompts():
    assert evals.system_prompt("none") == evals.NEUTRAL
    assert "explanation compiler" in evals.system_prompt("principles")


def test_grade_prompt_is_blind_and_asks_for_excess():
    item = evals.load_questions()["questions"][0]
    prompt = evals.grade_prompt("a reader", item, {"A": "first answer", "B": "second answer"})
    assert "=== Answer A ===" in prompt and "=== Answer B ===" in prompt
    assert "principles" not in prompt.lower()          # the grader does not know the conditions
    assert "excess" in prompt and item["misconception"] in prompt


def test_summary_table():
    items = [{"id": "x", "must": ["a", "b"]}]
    grades = {"x": {"rank": ["p", "n"], "why_best": "shorter", "words": {"n": 300, "p": 200},
                    "grades": {n: {"must": [2, 2], "misconception": "absent", "answer_first": True, "errors": [],
                                   "excess": ["e"] if n == "n" else [], "unclear": [], "score": s}
                               for n, s in (("n", 6), ("p", 8))}}}
    report = evals.summary({"n": "none", "p": "principles"}, items, grades, None)
    assert "| p | 8.0 | 100% |" in report and "ranked p > n" in report


def test_answers_never_read_stdin(monkeypatch):
    seen = {}

    class Done:
        returncode, stdout, stderr = 0, "ok", ""

    def fake_run(cmd, **kw):
        seen.update(kw, cmd=cmd)
        return Done()

    monkeypatch.setattr(evals.subprocess, "run", fake_run)
    assert evals.ask("system", "question") == "ok"
    assert seen["stdin"] is evals.subprocess.DEVNULL
    assert "--strict-mcp-config" in seen["cmd"] and "--tools" in seen["cmd"]
