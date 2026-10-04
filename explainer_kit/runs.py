"""Review runs: the probe, the cold read, and the blind test, run by a fresh agent and saved.

`explainer probe|coldread|quiz <slug> ... --run` gives the printed prompt, unchanged, to one fresh `claude -p`
call that may read only the explainer's folder (explainer_kit.agent). The reply is saved as
explainers/<slug>/review/runs/<stamp>-<tool>[-<rendering>].json. A blind test is then scored by a second call
that sees the rubric and model.md.

Each run's findings are numbered. The author records what they did with each in review/decisions.yaml
(`explainer decide`), and `explainer findings --stats` reports, per tool and severity, how many findings
authors adopt. A tool whose findings are mostly declined over-reports: tune its prompt.
"""

from __future__ import annotations

import hashlib
import json
from collections import Counter, defaultdict
from datetime import datetime
from pathlib import Path

import yaml

from explainer_kit.agent import ask, parse_json
from explainer_kit.paths import display, explainer_dir, explainers_dir
from explainer_kit.review import BLIND_FILES, coldread_prompt, probe_prompt, quiz_prompt, quiz_rubric

REVIEWER = ("You are a careful reviewer. Follow the instructions in the message exactly. Use the Read tool only on "
            "the files it names. Reply with JSON only.")
GRADER = ("You score a blind reviewer's answers against a rubric. Be strict and fair: score what the answer says, "
          "not what the reviewer may have meant. Reply with JSON only.")
SEVERITIES = ["blocking", "main", "edge", "excess", "gap"]


def _files(slug: str, tool: str, rendering: str | None) -> list[Path]:
    folder = explainer_dir(slug)
    return [folder / "model.md"] if tool == "probe" else [folder / f for f in BLIND_FILES[rendering]]


def _prompt(slug: str, tool: str, rendering: str | None) -> str:
    if tool == "probe":
        return probe_prompt(slug)
    if tool == "coldread":
        return coldread_prompt(slug, rendering)
    return quiz_prompt(slug, rendering)


def grade_prompt(slug: str, answers: dict) -> str:
    model_md = (explainer_dir(slug) / "model.md").read_text()
    return "\n".join([
        quiz_rubric(slug), "", "model.md, for the general items:", "", model_md, "",
        "The reviewer's answers:", json.dumps(answers, indent=1, ensure_ascii=False), "",
        'Reply with JSON only: {"scores": {"1": 0, "2": 1, ...}, "reasons": {"<item>": "why it lost points"}, '
        '"pass": true}',
    ])


def run_review(slug: str, tool: str, rendering: str | None = None, model: str | None = None) -> Path:
    folder = explainer_dir(slug)
    prompt = _prompt(slug, tool, rendering)
    files = _files(slug, tool, rendering)
    reply = parse_json(ask(REVIEWER, prompt, model=model, read=sorted({f.parent for f in files})))
    record = {
        "tool": tool, "rendering": rendering, "slug": slug, "at": datetime.now().isoformat(timespec="seconds"),
        "model": model or "default", "prompt_sha": hashlib.sha1(prompt.encode()).hexdigest()[:12], "reply": reply,
    }
    if tool == "quiz":
        record["grade"] = parse_json(ask(GRADER, grade_prompt(slug, reply.get("answers", {})), model=model))
    record["findings"] = extract(record)   # frozen: decisions refer to these numbers
    out = folder / "review" / "runs" / f"{datetime.now():%Y-%m-%dT%H%M%S}-{tool}{f'-{rendering}' if rendering else ''}.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(record, indent=1, ensure_ascii=False) + "\n")
    return out


def regrade(slug: str, run: str, model: str | None = None) -> Path:
    """Score a saved blind test again with the current rubric (the reviewer's answers stay as they were)."""
    path = explainer_dir(slug) / "review" / "runs" / f"{run.removesuffix('.json')}.json"
    record = json.loads(path.read_text())
    if record["tool"] != "quiz":
        raise SystemExit(f"{path.stem} is not a blind test")
    record.setdefault("earlier_grades", []).append(record.get("grade"))
    record["grade"] = parse_json(ask(GRADER, grade_prompt(slug, record["reply"].get("answers", {})), model=model))
    path.write_text(json.dumps(record, indent=1, ensure_ascii=False) + "\n")
    return path


# ---------------------------------------------------------------- findings

def findings(record: dict) -> list[dict]:
    """The run's findings as saved with it; decisions refer to their numbers."""
    return record.get("findings") or extract(record)


def extract(record: dict) -> list[dict]:
    """The findings of one reply, numbered from 1: severity, kind, text."""
    r, tool, out = record["reply"], record["tool"], []

    def add(severity, kind, text):
        out.append({"n": len(out) + 1, "severity": severity, "kind": kind, "text": str(text)})

    if tool == "probe":
        for g in r.get("gaps", []):
            add(g.get("severity", "main"), f"rule {g.get('rule', '?')}",
                f"{g.get('about', '')} → {g.get('suggested_addition', '')}")
        for e in r.get("excess", []):
            add("excess", "model entry", e)
    elif tool == "coldread":
        for b in r.get("blocking", []):
            if not str(b).lower().startswith(("none", "no finding", "nothing")):
                add("blocking", "blocking", b)
        for c in r.get("cuts", []):
            add("excess", "cut", c)
        units = next((v for k, v in r.items() if k.endswith("s") and isinstance(v, list)
                      and v and isinstance(v[0], dict) and "at" in v[0]), [])
        for u in units:
            for kind in ("unresolved", "unsaid", "leap"):
                for item in u.get(kind, []) or []:
                    add("edge", kind, f"{u.get('at', '')}: {item}")
    elif tool == "quiz":
        audit = r.get("audit", {})
        for kind, items in audit.items():
            for item in items or []:
                add("excess" if kind == "excess" else "gap", kind, item)
        for g in r.get("gaps", []):
            add("gap", "gap", g)
    return out


def _runs(folder: Path) -> list[Path]:
    return sorted((folder / "review" / "runs").glob("*.json"))


def _decisions(folder: Path) -> dict:
    path = folder / "review" / "decisions.yaml"
    return (yaml.safe_load(path.read_text()) or {}) if path.exists() else {}


def latest_runs(folder: Path) -> list[Path]:
    """The newest run of each tool and rendering."""
    newest = {}
    for path in _runs(folder):
        rec = json.loads(path.read_text())
        newest[(rec["tool"], rec.get("rendering"))] = path
    return sorted(newest.values())


def show(slug: str, run: str | None = None) -> str:
    folder = explainer_dir(slug)
    paths = [folder / "review" / "runs" / f"{run.removesuffix('.json')}.json"] if run else latest_runs(folder)
    if not paths:
        return f"no runs for {slug} (explainer coldread {slug} --run, …)"
    decided, lines = _decisions(folder), []
    for path in paths:
        rec = json.loads(path.read_text())
        lines.append(f"{path.stem}  ({rec['tool']}{', ' + rec['rendering'] if rec.get('rendering') else ''})")
        if rec["tool"] == "quiz" and "grade" in rec:
            g = rec["grade"]
            lines.append(f"  blind test: {'PASS' if g.get('pass') else 'FAIL'}  scores {g.get('scores')}")
        for f in findings(rec):
            d = decided.get(f"{path.stem}#{f['n']}", {}).get("decision", "·")
            lines.append(f"  {f['n']:>3} {f['severity']:<8} {d:<8} {f['kind']}: {f['text'][:150]}")
    return "\n".join(lines)


def decide(slug: str, run: str, adopt: list[int], decline: list[int], note: str = "",
           decline_rest: bool = False) -> Path:
    folder = explainer_dir(slug)
    stem = run.removesuffix(".json")
    path = folder / "review" / "runs" / f"{stem}.json"
    if not path.exists():
        raise SystemExit(f"no run {stem} in {display(folder / 'review' / 'runs')}")
    decided = _decisions(folder)
    if decline_rest:
        numbers = [f["n"] for f in findings(json.loads(path.read_text()))]
        decline = list(decline) + [n for n in numbers if n not in adopt and f"{stem}#{n}" not in decided]
    for n, decision in [(n, "adopted") for n in adopt] + [(n, "declined") for n in decline]:
        decided[f"{stem}#{n}"] = {"decision": decision, **({"note": note} if note else {})}
    path = folder / "review" / "decisions.yaml"
    path.write_text("# What the author did with each review finding (explainer decide). Read by findings --stats.\n"
                    + yaml.safe_dump(decided, sort_keys=True, allow_unicode=True))
    return path


def stats(root: Path | None = None) -> str:
    """Per tool and severity: findings, decided, adopted. A low adoption rate means the tool over-reports."""
    table: dict[tuple[str, str], Counter] = defaultdict(Counter)
    for folder in sorted((root or explainers_dir()).iterdir()):
        if not folder.is_dir():
            continue
        decided = _decisions(folder)
        for path in _runs(folder):
            rec = json.loads(path.read_text())
            for f in findings(rec):
                c = table[(rec["tool"], f["severity"])]
                c["findings"] += 1
                d = decided.get(f"{path.stem}#{f['n']}", {}).get("decision")
                if d:
                    c["decided"] += 1
                    c[d] += 1
    if not table:
        return "no review runs yet"
    lines = ["tool       severity   findings  decided  adopted  adoption",
             "---------  ---------  --------  -------  -------  --------"]
    for (tool, sev), c in sorted(table.items(), key=lambda kv: (kv[0][0], SEVERITIES.index(kv[0][1])
                                                                if kv[0][1] in SEVERITIES else 9)):
        rate = f"{c['adopted'] / c['decided']:.0%}" if c["decided"] else "—"
        lines.append(f"{tool:<9}  {sev:<9}  {c['findings']:>8}  {c['decided']:>7}  {c['adopted']:>7}  {rate:>8}")
    return "\n".join(lines)
