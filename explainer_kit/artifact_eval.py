"""Artifact eval: on subjects it was never tuned on, does the toolkit help an agent build an explainer that a
reader understands with less effort?

For each subject in evals/artifact/questions.yaml and each condition, three fresh `claude -p` agents run:

1. The builder gets the question and the reader, and writes an explanation (prose, diagram, or page) in an
   empty project folder. The conditions differ only in the guidance it gets: none, the principles appended
   to its system prompt, or the explain skill (plugin) at the quick or published tier.
2. The reader sees only the finished renderings (no model.md) and answers the subject's fixed quiz. Each
   answer must quote the passage it rests on; an answer whose quote is not in the renderings scores 0, so a
   reader that answers from its own knowledge earns nothing. It also lists where it would stop or reread,
   and what it did not need.
3. The grader sees, per subject, every condition's answers and visible text under shuffled labels. It scores
   each answer against the expected one and checks the text for the misconception and for factual errors.

Every stage saves its output and is skipped when the output exists, so a failed run resumes.
"""

from __future__ import annotations

import json
import os
import random
import re
import shutil
import tempfile
from concurrent.futures import ThreadPoolExecutor
from datetime import date
from pathlib import Path

import yaml

from explainer_kit import agent
from explainer_kit.evals import system_prompt, words
from explainer_kit.model import visible_html, visible_markdown
from explainer_kit.paths import CHECKOUT, display, project_root

RENDERINGS = {"explanation.md": "prose", "diagram.md": "diagram", "index.html": "html"}
PLUGIN = CHECKOUT / "plugin"

TASK = """Explain this subject to a reader, as a file the reader will read on their own.

Question: {q}
The reader: {reader}

Write the explanation as one or more of: explainers/{id}/explanation.md (prose), explainers/{id}/diagram.md (Mermaid
diagrams with their text), explainers/{id}/index.html (an interactive page). Choose the form that serves this reader
best; make more than one only if each adds something. Do not make a video. Do not search the web.
{extra}
When done, reply with one line: the files you made, and why that form."""

SKILL_TIER = {
    "quick": "Use the explain skill (explainer:explain) at the Quick artifact tier, with the slug {id}.",
    "published": "Use the explain skill (explainer:explain) at the Published tier, with the slug {id}: run the probe, "
                 "the cold read, and the blind test with --run, and fix what they find before you finish.",
}
TIMEOUT = {"quick": 2400, "published": 5400}

READER_SYSTEM = "You are a careful reader taking a test on an explanation. Reply with JSON only."
GRADER_SYSTEM = "You are a strict technical editor and a careful scientist. You grade explanations. Reply with JSON only."


def questions_file() -> Path:
    return project_root() / "evals" / "artifact" / "questions.yaml"


def load(split: str = "dev", only: list[str] | None = None) -> tuple[str, list[dict]]:
    spec = yaml.safe_load(questions_file().read_text())
    subjects = [s for s in spec["subjects"] if (split == "all" or s["split"] == split) and (not only or s["id"] in only)]
    return spec["reader"], subjects


def condition(name: str, source: str) -> dict:
    """quick and published use the plugin; any other source is a system-prompt source (evals.system_prompt):
    none, principles, git:<rev>, or a file."""
    if source in SKILL_TIER:
        return {"kind": "skill", "tier": source}
    return {"kind": "prompt", "append": None if source == "none" else system_prompt(source)}


# ---------------------------------------------------------------- 1. build

_SHIM: Path | None = None


def shim() -> Path:
    """A bin folder whose `explainer` runs this checkout, so the plugin uses the code under test, not a release.
    It lives in a private temp folder (mkdtemp: mode 0700, unpredictable name), made once per process: a fixed
    name in a shared /tmp would let another user plant the executable. It holds a local path, which does not
    belong in the results."""
    global _SHIM
    if _SHIM is not None:
        return _SHIM
    bin_dir = Path(tempfile.mkdtemp(prefix="explainer-eval-bin-"))
    exe = bin_dir / "explainer"
    exe.write_text(f'#!/bin/sh\nexec uv run --quiet --project "{CHECKOUT}" explainer "$@"\n')
    exe.chmod(0o700)
    _SHIM = bin_dir
    return bin_dir


def inside_project(path: Path) -> Path | None:
    """The first folder at or above `path` that would give an agent instructions (CLAUDE.md or .claude/)."""
    for d in (path, *path.parents):
        if (d / "CLAUDE.md").exists() or (d / ".claude").is_dir():
            return d
    return None


def build(subject: dict, name: str, cond: dict, reader: str, out: Path, model: str | None) -> dict:
    """Builds in a temporary folder outside every project, then copies the result into out/work/<id>/<name>.
    Inside a project, Claude Code would load that project's CLAUDE.md (in this repo: the principles) whatever
    the condition."""
    dest = out / "work" / subject["id"] / name
    done = dest / "run.json"
    if done.exists():
        return json.loads(done.read_text())
    ws = Path(tempfile.mkdtemp(prefix=f"explainer-eval-{subject['id']}-{name}-")).resolve()
    if found := inside_project(ws):
        raise SystemExit(f"the build folder {ws} is inside {found}, which has CLAUDE.md or .claude/; set TMPDIR "
                         f"to a folder outside every project")
    (ws / "explainers").mkdir(parents=True)
    tools = ["Read", "Write", "Edit", "Glob", "Grep"]
    allowed = list(tools)
    env = {**os.environ, "EXPLAINER_ROOT": str(ws)}
    extra, kwargs = "", {}
    if cond["kind"] == "skill":
        extra = SKILL_TIER[cond["tier"]].format(id=subject["id"])
        tools += ["Bash", "Skill"]
        allowed += ["Bash(explainer:*)", "Skill"]
        env["PATH"] = f"{shim()}{os.pathsep}{env['PATH']}"
        kwargs = {"plugin_dir": PLUGIN, "timeout": TIMEOUT[cond["tier"]]}
    else:
        kwargs = {"append_system": cond["append"], "timeout": 1200}
    prompt = TASK.format(q=subject["q"], reader=reader, id=subject["id"], extra=extra)
    run = agent.work(prompt, ws, tools, allowed, env=env, model=model, **kwargs)
    run["files"] = [display_rel(p, ws) for p in renderings(ws, subject["id"])]
    # The reviews a published build runs are separate claude -p calls; their cost is in each saved run.
    reviews = [json.loads(f.read_text()).get("usage", {}) for f in ws.glob("explainers/*/review/runs/*.json")]
    run["review_cost"] = round(sum(u.get("cost", 0) for u in reviews), 4)
    run["reviews"] = len(reviews)
    if dest.exists():
        shutil.rmtree(dest)
    shutil.copytree(ws, dest)
    shutil.rmtree(ws, ignore_errors=True)
    done.write_text(json.dumps(run, indent=2, ensure_ascii=False))
    return run


def display_rel(path: Path, root: Path) -> str:
    return str(path.relative_to(root))


def renderings(ws: Path, sid: str) -> list[Path]:
    """The renderings the builder made: in explainers/<id>/, else anywhere in its folder."""
    folder = ws / "explainers" / sid
    found = [folder / f for f in RENDERINGS if (folder / f).exists()]
    if not found:
        found = sorted(p for f in RENDERINGS for p in ws.rglob(f))
    return found


# ---------------------------------------------------------------- 2. read

def visible(path: Path) -> str:
    """What a reader sees, for counting words: Markdown without code, styling, and comments; a page's text."""
    text = path.read_text()
    return visible_html(text) if path.suffix == ".html" else visible_markdown(text)


def shown_text(path: Path) -> str:
    """What the grader reads: Markdown as written (formulas, code, and Mermaid included), minus comments the
    reader never sees; a page's visible text."""
    text = path.read_text()
    return visible_html(text) if path.suffix == ".html" else re.sub(r"<!--.*?-->", "", text, flags=re.S)


def reader_prompt(files: list[Path], reader: str, quiz: list[dict]) -> str:
    return "\n".join([
        "You are reading an explanation for the first time, as this reader: " + reader,
        "",
        "Read ONLY these files. Do not open any other file, and do not search the web:",
        *[f"- {f}" for f in files],
        "",
        "An .html file is an interactive page: read its visible text, and its script to learn what the controls show.",
        "",
        "Answer each question from the explanation alone, as this reader would after reading it once. For each, give "
        "your answer and the exact passage (a quote of at most 40 words, copied character for character from the "
        "files) that your answer rests on. If the explanation does not answer the question, say \"not covered\" "
        "and leave the quote empty. Do not fill gaps with your own knowledge; a gap is useful evidence. Some "
        "questions ask about a case the explanation does not mention: reason from what it does say, and quote the "
        "passage your reasoning uses.",
        "",
        "Questions:",
        *[f"{i}. {item['q']}" for i, item in enumerate(quiz, 1)],
        "",
        "Then list, each with a short quote, at most 10 of each:",
        "- stops: places where this reader would stop, reread, or lose the thread (an undefined term, a step "
        "without its reason, an ambiguous reference).",
        "- excess: passages this reader did not need (already known, said before, or off the question).",
        "",
        'Reply with JSON only: {"answers": {"1": {"answer": "...", "quote": "..."}, ...}, "stops": ["..."], '
        '"excess": ["..."]}',
    ])


def copy_for_reader(files: list[Path], shown: Path) -> list[Path]:
    """The reader gets copies of the renderings alone, so it cannot open model.md or the review runs."""
    if shown.exists():
        shutil.rmtree(shown)
    shown.mkdir(parents=True)
    for f in files:
        shutil.copy(f, shown / f.name)
    return [shown / f.name for f in files]


def read(subject: dict, name: str, reader: str, out: Path, model: str | None) -> dict:
    ws = out / "work" / subject["id"] / name
    saved = ws / "read.json"
    if saved.exists():
        return json.loads(saved.read_text())
    files = renderings(ws, subject["id"])
    if not files:
        result = {"answers": {}, "stops": [], "excess": [], "missing": True}
    else:
        shown = out / "shown" / subject["id"] / name
        copies = copy_for_reader(files, shown)
        prompt = reader_prompt(copies, reader, subject["quiz"])
        for _ in range(2):  # a smaller reader model sometimes breaks the JSON shape; ask once more
            result = reader_reply(agent.ask(READER_SYSTEM, prompt, model=model, read=[shown]), len(subject["quiz"]))
            if len(result["answers"]) == len(subject["quiz"]):
                break
        shutil.rmtree(shown)  # copies of files kept in work/
    result["grounded"] = {k: grounded(v.get("quote", ""), files) for k, v in result.get("answers", {}).items()}
    saved.write_text(json.dumps(result, indent=2, ensure_ascii=False))
    return result


def reader_reply(text: str, n: int) -> dict:
    """The reader's JSON, with answers under "answers" even when the reply put them at the top level."""
    try:
        reply = agent.parse_json(text)
    except ValueError:
        reply = {}
    answers = reply.get("answers")
    if not isinstance(answers, dict):
        answers = {k: v for k, v in reply.items() if k.isdigit()}
    answers = {k: v for k, v in answers.items() if isinstance(v, dict) and k.isdigit() and 1 <= int(k) <= n}
    return {"answers": answers, "stops": reply.get("stops", []), "excess": reply.get("excess", [])}


def norm(text: str) -> list[str]:
    text = text.lower().replace("’", "'").replace("‘", "'").replace("“", '"').replace("”", '"')
    return re.findall(r"[a-z0-9]+", text)


def grounded(quote: str, files: list[Path]) -> bool:
    """True when the quote, or a run of 6 of its words in order, is in a rendering (raw or as rendered)."""
    q = norm(quote)
    if not q:
        return False
    hay = " " + " ".join(w for f in files for t in (f.read_text(), visible(f)) for w in norm(t)) + " "
    n = min(6, len(q))
    return any(" " + " ".join(q[i:i + n]) + " " in hay for i in range(len(q) - n + 1))


# ---------------------------------------------------------------- 3. grade

TEXT_LIMIT = 60_000  # characters per explanation shown to the grader (line breaks kept: tables, Mermaid)


def grade_prompt(subject: dict, reader: str, entries: dict[str, dict]) -> str:
    quiz = "\n".join(f"  {i}. {item['q']}\n     Expected: {item['expect']}" for i, item in enumerate(subject["quiz"], 1))
    blocks = []
    for label, e in entries.items():
        answers = "\n".join(f"  {k}. {a.get('answer', '')}" for k, a in sorted(e["answers"].items()))
        text = e["text"][:TEXT_LIMIT]
        blocks.append(f"=== Explanation {label} ===\n{text}\n\n--- Reader's answers from {label} ---\n{answers}")
    return "\n".join([
        f"Subject: {subject['q']}",
        f"The reader: {reader}",
        "",
        "A reader read each explanation once and answered this quiz from it:",
        quiz,
        f"The explanation must not teach this misconception: {subject['misconception']}",
        "",
        *blocks,
        "",
        "Grade each explanation on its own. For each:",
        "- quiz: one score per question: 0 wrong or not covered, 1 vague or partly right, 2 correct and specific "
        "(the answer may use other words or another example than the expected one).",
        "- misconception: 'taught' (the text states or implies it), 'corrected' (it names and refutes it), or 'absent'.",
        "- errors: every factual error in the explanation's text, quoted.",
        f"Then rank the explanations (labels {', '.join(entries)}) from the one that lets this reader build an "
        "accurate mental model with the least effort to the one that costs the most. Effort comes from what is "
        "missing (a step, a reason, a term left undefined) and from what is extra (what the reader knows, "
        "repeats, detours). Say in one sentence why the first is first.",
        "",
        'Reply with JSON only: {"grades": {"<label>": {"quiz": [0, 1, 2], "misconception": "...", "errors": ["..."]}}, '
        '"rank": ["<label>", ...], "why_best": "..."}',
    ])


def grade(subject: dict, key: dict[str, str], reader: str, out: Path, model: str | None) -> dict:
    saved = out / "grades" / f"{subject['id']}.json"
    if saved.exists():
        return json.loads(saved.read_text())
    entries = {}
    for lab, n in key.items():
        ws = out / "work" / subject["id"] / n
        r = json.loads((ws / "read.json").read_text())
        entries[lab] = {"answers": r.get("answers", {}),
                        "text": "\n\n".join(shown_text(f) for f in renderings(ws, subject["id"])) or "(no explanation)"}
    reply = agent.parse_json(agent.ask(GRADER_SYSTEM, grade_prompt(subject, reader, entries), model=model))
    result = {"key": key, "grades": {key[lab]: g for lab, g in reply["grades"].items() if lab in key},
              "rank": [key[lab] for lab in reply.get("rank", []) if lab in key], "why_best": reply.get("why_best", "")}
    saved.parent.mkdir(parents=True, exist_ok=True)
    saved.write_text(json.dumps(result, indent=2, ensure_ascii=False))
    return result


# ---------------------------------------------------------------- run and report

def run(conditions: dict[str, str], out: Path, split: str = "dev", only: list[str] | None = None,
        model: str | None = None, workers: int = 4, seed: int = 0, reader_model: str | None = None) -> Path:
    reader, subjects = load(split, only)
    if not subjects:
        raise SystemExit(f"no subjects for split {split!r}" + (f" and ids {only}" if only else ""))
    conds = {n: condition(n, s) for n, s in conditions.items()}
    out.mkdir(parents=True, exist_ok=True)
    (out / "conditions.json").write_text(json.dumps(conditions, indent=2))
    jobs = [(s, n) for s in subjects for n in conds]

    def build_job(job):
        s, n = job
        r = build(s, n, conds[n], reader, out, model)
        print(f"build   {s['id']:22} {n:12} {', '.join(Path(f).name for f in r['files']) or 'NO FILES':34} "
              f"{r.get('seconds') or 0:5}s  ${r.get('cost') or 0:.2f}{'  ' + r['error'] if r.get('error') else ''}",
              flush=True)
        return r

    def read_job(job):
        s, n = job
        r = read(s, n, reader, out, reader_model or model)
        ok = sum(r["grounded"].values())
        print(f"read    {s['id']:22} {n:12} {ok}/{len(s['quiz'])} grounded", flush=True)
        return r

    with ThreadPoolExecutor(workers) as pool:
        list(pool.map(build_job, jobs))
    with ThreadPoolExecutor(workers) as pool:
        list(pool.map(read_job, jobs))
    rng, keys = random.Random(seed), {}
    for s in subjects:
        labels = list(conds)
        rng.shuffle(labels)
        keys[s["id"]] = {chr(ord("A") + i): n for i, n in enumerate(labels)}
    with ThreadPoolExecutor(workers) as pool:
        futures = [pool.submit(grade, s, keys[s["id"]], reader, out, model) for s in subjects]
        grades = {s["id"]: f.result() for s, f in zip(subjects, futures)}
    report = out / "report.md"
    report.write_text(summary(conditions, subjects, out, grades, split, model, reader_model))
    print(f"\nreport  {display(report)}")
    return report


def collect(subjects: list[dict], names: list[str], out: Path, grades: dict) -> dict:
    rows: dict[str, dict] = {}
    for n in names:
        per = []
        for s in subjects:
            ws = out / "work" / s["id"] / n
            b, r = json.loads((ws / "run.json").read_text()), json.loads((ws / "read.json").read_text())
            g = grades[s["id"]]["grades"].get(n, {"quiz": [0] * len(s["quiz"]), "misconception": "absent", "errors": []})
            raw = list(g["quiz"])[:len(s["quiz"])] + [0] * max(0, len(s["quiz"]) - len(g["quiz"]))
            ok = [r["grounded"].get(str(i), False) for i in range(1, len(s["quiz"]) + 1)]
            files = renderings(ws, s["id"])
            per.append({
                "id": s["id"], "raw": raw, "score": [x if k else 0 for x, k in zip(raw, ok)], "grounded": ok,
                "predict": [i for i, item in enumerate(s["quiz"]) if item.get("kind") == "predict"],
                "misconception": g.get("misconception", "absent"), "errors": g.get("errors", []),
                "stops": len(r.get("stops", [])), "excess": len(r.get("excess", [])),
                "words": sum(words(visible(f)) for f in files), "forms": [RENDERINGS[f.name] for f in files],
                "rank": (grades[s["id"]].get("rank") or []).index(n) + 1 if n in (grades[s["id"]].get("rank") or []) else None,
                "cost": (b.get("cost") or 0) + (b.get("review_cost") or 0), "seconds": b.get("seconds") or 0,
                "failed": bool(b.get("error")),
            })
        rows[n] = {"subjects": per}
    return rows


def summary(conditions: dict[str, str], subjects: list[dict], out: Path, grades: dict, split: str,
            model: str | None, reader_model: str | None = None) -> str:
    names = list(conditions)
    rows = collect(subjects, names, out, grades)
    (out / "scores.json").write_text(json.dumps(rows, indent=2, ensure_ascii=False))
    n = len(subjects)
    head = ["condition", "mean rank", "ranked best", "quiz (grounded)", "predict", "quiz (raw)", "ungrounded", "misconception taught", "corrected",
            "errors", "stops / expl.", "excess / expl.", "words", "forms", "cost / expl.", "min / expl."]
    table = ["| " + " | ".join(head) + " |", "|" + "---|" * len(head)]
    for name in names:
        per = rows[name]["subjects"]
        full = sum(2 * len(p["raw"]) for p in per)
        forms: dict[str, int] = {}
        for p in per:
            key = "+".join(p["forms"]) or "none"
            forms[key] = forms.get(key, 0) + 1
        ranks = [p["rank"] for p in per if p["rank"]]
        table.append("| " + " | ".join([
            name,
            f"{sum(ranks) / len(ranks):.1f}" if ranks else "–",
            f"{sum(r == 1 for r in ranks)}/{n}",
            f"{sum(sum(p['score']) for p in per) / full:.0%}",
            f"{sum(p['score'][i] for p in per for i in p['predict']) / max(1, 2 * sum(len(p['predict']) for p in per)):.0%}",
            f"{sum(sum(p['raw']) for p in per) / full:.0%}",
            str(sum(r > 0 and not k for p in per for r, k in zip(p["raw"], p["grounded"]))),
            str(sum(p["misconception"] == "taught" for p in per)),
            str(sum(p["misconception"] == "corrected" for p in per)),
            str(sum(len(p["errors"]) for p in per)),
            f"{sum(p['stops'] for p in per) / n:.1f}",
            f"{sum(p['excess'] for p in per) / n:.1f}",
            f"{sum(p['words'] for p in per) / n:.0f}",
            ", ".join(f"{k} {v}" for k, v in sorted(forms.items(), key=lambda kv: -kv[1])),
            f"${sum(p['cost'] for p in per) / n:.2f}",
            f"{sum(p['seconds'] for p in per) / n / 60:.1f}",
        ]) + " |")
    lines = [
        f"# Artifact eval, {date.today().isoformat()} ({split}, {n} subjects)", "",
        f"Builder, reader, and grader: fresh `claude -p`{f' --model {model}' if model else ''} agents"
        f"{f' (reader: --model {reader_model})' if reader_model else ''}. The reader saw "
        "only the renderings; an answer counts only when its quote is found in them (grounded). The grader saw each "
        "subject's explanations under shuffled labels.", "",
        "Conditions: " + "; ".join(f"**{k}** = `{v}`" for k, v in conditions.items()), "",
        *table, "",
        f"Mean rank: the grader's ranking of each subject's {len(names)} explanations by the reader's effort (1 is best). "
        "Quiz: fixed questions per subject, 0–2 each; predict: the last question of each, a case the explanation "
        "need not mention. Stops and excess: the reader's lists (at most 10 each). "
        "Words: visible words in all renderings. Cost: the builder and the reviews it ran; minutes: the builder.", "",
        "## Per subject (grounded quiz score, of 8)", "",
        "| subject | " + " | ".join(names) + " |", "|---|" + "---|" * len(names),
    ]
    for i, s in enumerate(subjects):
        cells = []
        for name in names:
            p = rows[name]["subjects"][i]
            mark = " ✗" if p["misconception"] == "taught" else ""
            cells.append(f"{sum(p['score'])}{mark} ({p['words']} w)" + (" FAILED" if p["failed"] else ""))
        lines.append(f"| {s['id']} | " + " | ".join(cells) + " |")
    lines += ["", "✗: the explanation teaches the misconception.", "", "## Why the best is best", ""]
    for s in subjects:
        g = grades[s["id"]]
        if g.get("rank"):
            lines.append(f"- **{s['id']}**: {' > '.join(g['rank'])}. {g.get('why_best', '')}")
    return "\n".join(lines) + "\n"
