"""Rederivation: can a reader of an explainer work out a result it never states?

Each subject in evals/artifact/questions.yaml has a target: a question, the steps a derivation needs (building
blocks a good explanation gives, and derived steps the reader works out), and the result. The quiz checks what an
explanation says; a target checks whether its building blocks let the reader go further. A model reader already
knows most results, so a right answer proves little: every step must rest on a part of the explanation the reader
names, and the grader checks that the part carries the idea.

1. Targets are drafted by hand and checked by a fresh `claude -p` agent (`explainer eval targets`), then frozen.
2. The reader sees only the renderings and the target's question, and works it out step by step.
3. The grader sees each subject's explanations and chains under shuffled labels, and marks each expected step.

A pass is a fresh reader run over every build, graded once under its own shuffle; a run makes three.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

from explainer_kit import agent
from explainer_kit import artifact_eval as ae
from explainer_kit.paths import project_root

KINDS = ("block", "derived")
CHECKER_SYSTEM = "You are a careful scientist and teacher. You check test questions. Reply with JSON only."
CHECKS = ("correct", "blocks", "derived_follow", "steps", "not_stated")


def checks_file() -> Path:
    return project_root() / "evals" / "artifact" / "rederive-checks.json"


# ---------------------------------------------------------------- 1. targets

def target_problems(t: dict) -> list[str]:
    """What makes a target malformed: 3–6 steps, each a block or derived, at least one derived, a question and a
    result."""
    problems = []
    if not str(t.get("q") or "").strip():
        problems.append("no question")
    if not str(t.get("result") or "").strip():
        problems.append("no result")
    steps = t.get("steps")
    if not isinstance(steps, list) or not 3 <= len(steps) <= 6:
        return problems + ["needs 3–6 steps"]
    for i, s in enumerate(steps, 1):
        if not isinstance(s, dict) or s.get("kind") not in KINDS or not str(s.get("text") or "").strip():
            problems.append(f"step {i}: needs a kind ({' or '.join(KINDS)}) and a text")
    if not any(isinstance(s, dict) and s.get("kind") == "derived" for s in steps):
        problems.append("no derived step")
    return problems


def target_hash(t: dict) -> str:
    return hashlib.sha256(json.dumps(t, sort_keys=True, ensure_ascii=False).encode()).hexdigest()[:12]


def check_prompt(subject: dict, reader: str) -> str:
    t = subject["rederive"]
    quiz = "\n".join(f"  - {item['q']}\n    Expected: {item['expect']}" for item in subject["quiz"])
    steps = "\n".join(f"  {i}. ({s['kind']}) {s['text']}" for i, s in enumerate(t["steps"], 1))
    return "\n".join([
        f"Subject: {subject['q']}",
        f"The reader: {reader}",
        "",
        "An explanation of this subject will be written for this reader. A good one gives the ideas in the quiz's "
        "expected answers:",
        quiz,
        "",
        "After reading it, the reader is asked to work out a result the explanation was never asked to state:",
        f"Question: {t['q']}",
        "Expected steps (block: an idea a good explanation gives; derived: worked out from the steps before it):",
        steps,
        f"Expected result: {t['result']}",
        "",
        "Check this target. Answer each with true or false:",
        "- correct: every step and the result are true.",
        "- blocks: every block step is an idea from the subject's question, from the quiz's expected answers, or "
        "background this reader already has. A block that needs any other idea makes the target reward long "
        "explanations instead of understanding.",
        "- derived_follow: every derived step follows from the steps before it plus background this reader "
        "already has, and brings in no new fact about the subject.",
        "- steps: there are at least three steps, and each is an idea any valid derivation needs, not the "
        "bookkeeping of one route.",
        "- not_stated: a good answer to the subject's question would not state the result.",
        "",
        "Then give one sentence of reason that names any step that fails.",
        "",
        'Reply with JSON only: {"tests": {"correct": true, "blocks": true, "derived_follow": true, "steps": true, '
        '"not_stated": true}, "reason": "..."}',
    ])


def check_targets(only: list[str] | None = None, model: str | None = None) -> Path:
    """Checks every target whose text changed since its last check; a verdict passes only when all five tests do.
    A subject without a target keeps its last entry, so a target dropped after failing stays listed."""
    path = checks_file()
    saved = json.loads(path.read_text()) if path.exists() else {}
    reader, subjects = ae.load("all", only)
    for s in subjects:
        t = s.get("rederive")
        if not t:
            continue
        h, before = target_hash(t), saved.get(s["id"], {})
        if before.get("hash") == h:
            continue
        reply = agent.parse_json(agent.ask(CHECKER_SYSTEM, check_prompt(s, reader), model=model))
        tests = {k: reply.get("tests", {}).get(k) is True for k in CHECKS}
        saved[s["id"]] = {"verdict": "pass" if all(tests.values()) else "fail", "tests": tests,
                          "reason": reply.get("reason", ""), "hash": h, "attempt": before.get("attempt", 0) + 1}
        path.write_text(json.dumps(dict(sorted(saved.items())), indent=2, ensure_ascii=False) + "\n")
    return path
