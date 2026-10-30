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
import random
import re
import shutil
import tempfile
from concurrent.futures import ThreadPoolExecutor
from datetime import date
from pathlib import Path

import yaml

from explainer_kit import agent
from explainer_kit import artifact_eval as ae
from explainer_kit.evals import words
from explainer_kit.paths import display, project_root

KINDS = ("block", "derived")
MARKS = ("supported", "unsupported", "missing", "stated")
CHECKER_SYSTEM = "You are a careful scientist and teacher. You check test questions. Reply with JSON only."
CHECKS = ("correct", "blocks", "derived_follow", "steps", "not_stated")
# The same words in the reader's prompt and the grader's: what the reader may bring, and what must come from the text.
OUTSIDE_RULE = ("Background that this reader already has (see the reader above) may be used without a citation. Every "
                "fact about the subject must come from a part of the explanation that the reader names.")


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


# ---------------------------------------------------------------- 2. read

def reader_prompt(files: list[Path], reader: str, question: str) -> str:
    return "\n".join([
        "You are reading an explanation for the first time, as this reader: " + reader,
        "",
        "Read ONLY these files. Do not open any other file, and do not search the web:",
        *[f"- {f}" for f in files],
        "",
        "An .html file is an interactive page: read its visible text, and its script to learn what the controls show.",
        "",
        "Then work out this question from what the explanation gives you. The explanation may not answer it directly:",
        question,
        "",
        "Work it out step by step. For each step give: step (what it establishes); part (the part of the explanation "
        "it rests on: a heading, a paragraph, a figure or diagram, or a control on a page; or the number of an "
        "earlier step; or \"background\"); and idea (what that part gives you, in your own words).",
        OUTSIDE_RULE,
        "If the explanation lacks an idea you need, say which in gap and stop there: do not fill it from your own "
        "knowledge. A gap is useful evidence. Otherwise end with your result.",
        "",
        'Reply with JSON only: {"steps": [{"step": "...", "part": "...", "idea": "..."}], "result": "...", '
        '"gap": ""}',
    ])


def chain_reply(text: str) -> dict:
    """The reader's chain in a fixed shape, whatever the reply looked like."""
    try:
        reply = agent.parse_json(text)
    except ValueError:
        reply = {}
    reply = reply if isinstance(reply, dict) else {}
    steps = reply.get("steps") if isinstance(reply.get("steps"), list) else []
    return {"steps": [{k: str(s.get(k) or "") for k in ("step", "part", "idea")} for s in steps if isinstance(s, dict)],
            "result": str(reply.get("result") or ""), "gap": str(reply.get("gap") or "")}


def chain_text(chain: dict) -> str:
    lines = [f"{i}. {s['step']} (rests on: {s['part']}; {s['idea']})" for i, s in enumerate(chain.get("steps", []), 1)]
    if chain.get("gap"):
        lines.append(f"Gap: {chain['gap']}")
    return "\n".join([*lines, f"Result: {chain.get('result', '')}"])


def read_chain(subject: dict, cond: str, reader: str, builds: Path, out: Path, k: int, model: str | None) -> dict:
    """One reader's chain for one build in pass k. The builds folder is only read: copies go to a temp folder."""
    saved = out / "rederive" / f"pass-{k}" / "read" / subject["id"] / f"{cond}.json"
    if saved.exists():
        return json.loads(saved.read_text())
    files = ae.renderings(builds / "work" / subject["id"] / cond, subject["id"])
    if not files:
        result = {**chain_reply(""), "missing": True}
    else:
        tmp = Path(tempfile.mkdtemp(prefix="explainer-rederive-"))
        try:
            shown = tmp / "explanation"
            prompt = reader_prompt(ae.copy_for_reader(files, shown), reader, subject["rederive"]["q"])
            for _ in range(2):  # a broken JSON shape gets one more try
                result = chain_reply(agent.ask(ae.READER_SYSTEM, prompt, model=model, read=[shown]))
                if result["steps"] or result["gap"]:
                    break
        finally:
            shutil.rmtree(tmp, ignore_errors=True)
    saved.parent.mkdir(parents=True, exist_ok=True)
    saved.write_text(json.dumps(result, indent=2, ensure_ascii=False))
    return result


# ---------------------------------------------------------------- 3. grade

def grader_text(path: Path) -> str:
    """What the grader reads: as for the quiz, plus a page's scripts, so a step that cites a control can be checked."""
    text = ae.shown_text(path)
    if path.suffix == ".html":
        scripts = [s.strip() for s in re.findall(r"<script\b[^>]*>(.*?)</script>", path.read_text(), flags=re.S | re.I)]
        if any(scripts):
            text += "\n\n--- page script ---\n" + "\n\n".join(s for s in scripts if s)
    return text


def grade_prompt(subject: dict, reader: str, entries: dict[str, dict]) -> str:
    t = subject["rederive"]
    steps = "\n".join(f"  {i}. ({s['kind']}) {s['text']}" for i, s in enumerate(t["steps"], 1))
    blocks = [f"=== Explanation {label} ===\n{e['text'][:ae.TEXT_LIMIT]}\n\n--- Reader's working from {label} ---\n"
              f"{e['chain']}" for label, e in entries.items()]
    return "\n".join([
        f"Subject: {subject['q']}",
        f"The reader: {reader}",
        "",
        "A reader read each explanation once, then worked out this question, which the explanation was not asked to "
        "answer:",
        f"Question: {t['q']}",
        "Expected steps (block: an idea a good explanation gives; derived: worked out from the steps before it):",
        steps,
        f"Expected result: {t['result']}",
        "",
        "The reader was told: " + OUTSIDE_RULE,
        "",
        *blocks,
        "",
        "Grade each reader's working on its own, against its own explanation. The expected steps are a checklist of "
        "ideas, not a script: credit a step when the working establishes the same idea, in any order, merged with "
        "another step, split in two, or by an equivalent route. For each expected step, in order, give one mark:",
        "- supported: the reader made the step, and either the parts of the explanation it names carry the ideas it "
        "rests on, or it uses only background this reader already has on top of earlier steps;",
        "- unsupported: the reader made the step, but from its own knowledge of the subject, or from a part of the "
        "explanation that does not carry the idea;",
        "- missing: the reader did not make the step;",
        "- stated: a derived step that the explanation itself states outright, so the reader looked it up instead of "
        "working it out. Use stated for derived steps only; building blocks are meant to be in the explanation.",
        "Then give result_right (the reader's result matches the expected result) and result_stated (the explanation "
        "itself states the expected result outright).",
        "",
        'Reply with JSON only: {"grades": {"<label>": {"marks": ["supported", ...], "result_right": true, '
        '"result_stated": false}}}',
    ])


def marks(raw: object, kinds: list[str]) -> list[str]:
    """One mark per expected step: unknown or absent marks are missing, and "stated" on a building block (which
    is meant to be in the explanation) is supported."""
    raw = raw if isinstance(raw, list) else []
    out = []
    for i, kind in enumerate(kinds):
        m = str(raw[i]).strip().lower() if i < len(raw) else "missing"
        m = m if m in MARKS else "missing"
        out.append("supported" if m == "stated" and kind == "block" else m)
    return out


def tally(marks: list[str], kinds: list[str], right: bool, stated: bool) -> dict[str, int]:
    """Counts for one chain. A stated derived step, or a stated result, is left out of the score: neither rewarded
    nor penalized."""
    n_stated = sum(m == "stated" for m in marks)
    supported = sum(m == "supported" for m in marks)
    return {"supported": supported, "made": supported + sum(m == "unsupported" for m in marks),
            "counted": len(marks) - n_stated, "stated": n_stated, "right": int(right and not stated),
            "results": int(not stated), "results_stated": int(stated)}


def pass_scores(tallies: dict[str, list[dict]]) -> dict[str, dict]:
    """Per condition, pooled over subjects: supported and raw shares of the counted steps, and the share of results
    right (None when nothing was counted)."""
    def share(key: str, of: str, ts: list[dict]) -> float | None:
        total = sum(t[of] for t in ts)
        return sum(t[key] for t in ts) / total if total else None
    return {c: {"supported": share("supported", "counted", ts), "raw": share("made", "counted", ts),
                "result": share("right", "results", ts)} for c, ts in tallies.items()}


def separations(passes: list[dict[str, dict]]) -> list[tuple[str, str]]:
    """Pairs (a, b) where a's supported score is higher than b's in every pass: the separation rule."""
    if not passes:
        return []
    names = list(passes[0])
    return [(a, b) for a in names for b in names if a != b and all(
        p[a]["supported"] is not None and p[b]["supported"] is not None and p[a]["supported"] > p[b]["supported"]
        for p in passes)]


def grade_subject(subject: dict, key: dict[str, str], reader: str, builds: Path, out: Path, k: int,
                  model: str | None) -> dict:
    """One grading of a subject's chains in pass k, under the labels in `key` (label -> condition)."""
    saved = out / "rederive" / f"pass-{k}" / "grades" / f"{subject['id']}.json"
    if saved.exists():
        return json.loads(saved.read_text())
    kinds = [s["kind"] for s in subject["rederive"]["steps"]]
    entries, missing = {}, set()
    for label, cond in key.items():
        chain = json.loads((out / "rederive" / f"pass-{k}" / "read" / subject["id"] / f"{cond}.json").read_text())
        if chain.get("missing"):
            missing.add(label)
        files = ae.renderings(builds / "work" / subject["id"] / cond, subject["id"])
        entries[label] = {"text": "\n\n".join(grader_text(f) for f in files) or "(no explanation)",
                          "chain": "(no chain)" if chain.get("missing") else chain_text(chain)}

    def fits(g: object) -> bool:
        return isinstance(g, dict) and isinstance(g.get("marks"), list) and len(g["marks"]) == len(kinds)

    reply: dict = {}
    if len(missing) < len(key):  # nothing to grade when no build has an explanation
        prompt = grade_prompt(subject, reader, entries)
        for _ in range(2):  # a reply missing a label, or with the wrong number of marks, gets one more try
            reply = agent.parse_json(agent.ask(ae.GRADER_SYSTEM, prompt, model=model))
            if all(fits((reply.get("grades") or {}).get(label)) for label in key if label not in missing):
                break
    grades = {}
    for label, cond in key.items():
        g = (reply.get("grades") or {}).get(label)
        g = g if isinstance(g, dict) and label not in missing else {}
        grades[cond] = {"marks": marks(g.get("marks"), kinds), "result_right": g.get("result_right") is True,
                        "result_stated": g.get("result_stated") is True, "raw": g.get("marks")}
        if label in missing:  # a failed build scores nothing, whatever a grader says about "(no explanation)"
            grades[cond]["missing"] = True
    result = {"key": key, "grades": grades}
    saved.parent.mkdir(parents=True, exist_ok=True)
    saved.write_text(json.dumps(result, indent=2, ensure_ascii=False))
    return result


# ---------------------------------------------------------------- run and report

def run(out: Path, builds: Path, split: str = "dev", only: list[str] | None = None, model: str | None = None,
        reader_model: str | None = None, workers: int = 4, passes: int = 3) -> Path:
    """Reads and grades the builds in `builds` (an artifact run folder, only read) into `out`."""
    reader, subjects = ae.load(split, only)
    subjects = [s for s in subjects if s.get("rederive")]
    if not subjects:
        raise SystemExit(f"no subjects with a rederivation target for split {split!r}" + (f" and ids {only}" if only else ""))
    names = list(json.loads((builds / "conditions.json").read_text()))
    stage = out / "rederive"
    stage.mkdir(parents=True, exist_ok=True)
    # The targets this folder ran, so a rerun after a target changed cannot mix two versions in one folder.
    snapshot, targets = stage / "targets.json", {s["id"]: s["rederive"] for s in subjects}
    if snapshot.exists():
        before = json.loads(snapshot.read_text())
        changed = sorted(i for i in targets if i in before and before[i] != targets[i])
        if changed:
            raise SystemExit(f"targets changed since this run: {', '.join(changed)}")
        targets = {**before, **targets}
    snapshot.write_text(json.dumps(dict(sorted(targets.items())), indent=2, ensure_ascii=False) + "\n")
    # Named relative to the project, or by folder name: a path relative to --out can climb through the home folder.
    try:
        source = str(builds.resolve().relative_to(project_root().resolve()))
    except ValueError:
        source = builds.name
    (stage / "source.json").write_text(json.dumps({"builds": source}) + "\n")

    def read_job(job):
        k, s, n = job
        r = read_chain(s, n, reader, builds, out, k, reader_model or model)
        print(f"read    pass {k}  {s['id']:22} {n:12} {len(r['steps'])} steps{'  gap' if r['gap'] else ''}"
              f"{'  NO EXPLANATION' if r.get('missing') else ''}", flush=True)

    ks = range(1, passes + 1)
    with ThreadPoolExecutor(workers) as pool:
        list(pool.map(read_job, [(k, s, n) for k in ks for s in subjects for n in names]))
    keys = {}
    for k in ks:
        rng = random.Random(k)
        for s in subjects:
            labels = list(names)
            rng.shuffle(labels)
            keys[k, s["id"]] = {chr(ord("A") + i): n for i, n in enumerate(labels)}
    with ThreadPoolExecutor(workers) as pool:
        futures = {(k, s["id"]): pool.submit(grade_subject, s, keys[k, s["id"]], reader, builds, out, k, model)
                   for k in ks for s in subjects}
        grades = {key: f.result() for key, f in futures.items()}
    report = out / "rederive.md"
    report.write_text(summary(names, subjects, builds, out, grades, passes, split, source, model, reader_model))
    print(f"\nreport  {display(report)}")
    return report


def summary(names: list[str], subjects: list[dict], builds: Path, out: Path, grades: dict, passes: int, split: str,
            source: str, model: str | None, reader_model: str | None) -> str:
    ks = range(1, passes + 1)
    tallies = {k: {n: [] for n in names} for k in ks}
    for k in ks:
        for s in subjects:
            kinds = [step["kind"] for step in s["rederive"]["steps"]]
            for n in names:
                g = grades[k, s["id"]]["grades"][n]
                tallies[k][n].append(tally(g["marks"], kinds, g["result_right"], g["result_stated"]))
    scores = [pass_scores(tallies[k]) for k in ks]
    seps = separations(scores)
    (out / "rederive-scores.json").write_text(json.dumps(
        {"passes": scores, "tallies": {str(k): v for k, v in tallies.items()}, "separations": [list(p) for p in seps]},
        indent=2, ensure_ascii=False) + "\n")
    pct = lambda x: "–" if x is None else f"{x:.0%}"  # noqa: E731
    ids = {s["id"] for s in subjects}
    quiz_file = builds / "scores.json"
    quiz = json.loads(quiz_file.read_text()) if quiz_file.exists() else {}

    def quiz_share(n: str) -> str:
        per = [p for p in quiz.get(n, {}).get("subjects", []) if p["id"] in ids]
        full = sum(2 * len(p["raw"]) for p in per)
        return f"{sum(sum(p['score']) for p in per) / full:.0%}" if full else "–"

    def mean_words(n: str) -> str:
        counts = [sum(words(ae.visible(f)) for f in ae.renderings(builds / "work" / s["id"] / n, s["id"])) for s in subjects]
        return f"{sum(counts) / len(counts):.0f}"

    head = ["condition", "supported", "raw", "result right", "stated steps", "stated results", "words", "quiz (grounded)"]
    table = ["| " + " | ".join(head) + " |", "|" + "---|" * len(head)]
    for n in names:
        table.append("| " + " | ".join([
            n,
            ", ".join(pct(sc[n]["supported"]) for sc in scores),
            ", ".join(pct(sc[n]["raw"]) for sc in scores),
            ", ".join(pct(sc[n]["result"]) for sc in scores),
            ", ".join(str(sum(t["stated"] for t in tallies[k][n])) for k in ks),
            ", ".join(str(sum(t["results_stated"] for t in tallies[k][n])) for k in ks),
            mean_words(n),
            quiz_share(n),
        ]) + " |")
    rule = "in all three passes" if passes == 3 else f"in all {passes} passes"
    sep = ", ".join(f"{a} > {b}" for a, b in seps) or "none"
    lines = [
        f"# Rederivation, {date.today().isoformat()} ({split}, {len(subjects)} subjects)", "",
        f"Builds: `{source}`. Reader and grader: fresh `claude -p`{f' --model {model}' if model else ''} agents"
        f"{f' (reader: --model {reader_model})' if reader_model else ''}. The reader saw only the renderings and the "
        "target's question; the grader saw each subject's explanations and the readers' working under shuffled "
        f"labels. {passes} passes: each a fresh reader run over every build, graded once under its own shuffle.", "",
        *table, "",
        f"Separation (higher supported score {rule}): {sep}.", "",
        "Each cell lists the passes in order. Supported: the share of expected steps the reader made and grounded in a "
        "part of the explanation it named (or in background this reader has); raw: the share made at all; result "
        "right: the share of results that match. Stated steps and stated results: derived steps and results the "
        "explanation states outright, left out of the shares above. Words: visible words per explanation. Quiz: the "
        "grounded quiz score of the same builds.", "",
        "## Per subject (supported/counted steps, per pass)", "",
        "| subject | " + " | ".join(names) + " |", "|---|" + "---|" * len(names),
    ]
    for i, s in enumerate(subjects):
        cells = [", ".join(f"{tallies[k][n][i]['supported']}/{tallies[k][n][i]['counted']}" for k in ks)
                 + (" NO EXPLANATION" if any(grades[k, s["id"]]["grades"][n].get("missing") for k in ks) else "")
                 for n in names]
        lines.append(f"| {s['id']} | " + " | ".join(cells) + " |")
    return "\n".join(lines) + "\n"


# ---------------------------------------------------------------- a person's working

def grade_human(chain_file: Path, builds: Path, model: str | None = None) -> dict:
    """Grades a person's working (evals/artifact/human-check.md) with the same rubric as a model reader's. The file
    is Markdown with front matter naming the subject and the condition whose explanation the person read."""
    m = re.match(r"---\n(.*?)\n---\n(.*)", chain_file.read_text(), re.S)
    meta = (yaml.safe_load(m.group(1)) or {}) if m else {}
    if not m or "subject" not in meta or "condition" not in meta:
        raise SystemExit(f"{chain_file.name}: needs front matter with subject and condition")
    reader, subjects = ae.load("all", [meta["subject"]])
    if not subjects or not subjects[0].get("rederive"):
        raise SystemExit(f"no subject {meta['subject']!r} with a rederivation target")
    s, cond = subjects[0], meta["condition"]
    files = ae.renderings(builds / "work" / s["id"] / cond, s["id"])
    if not files:
        raise SystemExit(f"no explanation for {s['id']} under {cond!r} in {builds.name}")
    entries = {"A": {"text": "\n\n".join(grader_text(f) for f in files), "chain": m.group(2).strip()}}
    reply = agent.parse_json(agent.ask(ae.GRADER_SYSTEM, grade_prompt(s, reader, entries), model=model))
    g = (reply.get("grades") or {}).get("A")
    g = g if isinstance(g, dict) else {}
    kinds = [step["kind"] for step in s["rederive"]["steps"]]
    mk, right, stated = marks(g.get("marks"), kinds), g.get("result_right") is True, g.get("result_stated") is True
    result = {"subject": s["id"], "condition": cond, "marks": mk, "result_right": right, "result_stated": stated,
              "tally": tally(mk, kinds, right, stated)}
    chain_file.with_suffix(".grade.json").write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n")
    return result
