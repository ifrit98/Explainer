"""Positive controls for the rederivation test: does it notice a missing building block?

PRD-002's dev baseline credited every condition with 90–100% of the expected steps. That is either a fact about the
explanations or a blind test. The controls check the test where the right answer is known: an explanation with one
building block cut out should no longer get credit for it.

1. `explainer eval cuts` copies the v0.8 builds of the subjects in evals/artifact/controls.yaml, cuts one block from
   each `principles` explanation (a fresh `claude -p` cutter), and has a separate checker confirm the cut. The cut
   copies, checks and diffs are frozen before any run.
2. `explainer eval controls` reuses the PRD-002 baseline's reader chains for the uncut conditions, runs the unchanged
   rederivation stage on the folder, checks uncaught cuts for leaks, and reports the verdict under the bar in
   controls.yaml.
"""

from __future__ import annotations

import difflib
import hashlib
import json
import math
import re
import shutil
from datetime import date
from pathlib import Path

import yaml

from explainer_kit import agent
from explainer_kit import artifact_eval as ae
from explainer_kit import rederive
from explainer_kit.paths import project_root

MAX_ATTEMPTS = 3                 # a cut that fails its check is redone at most twice
CUT = "principles-cut"           # the cut copy's condition in the controls folder, so no report shows it as principles
UNCUT = ("none", "quick", "published")
CUTTER_SYSTEM = ("You are a careful editor. You remove one idea from an explanation and change nothing else. Reply "
                 "with JSON only.")
CHECKER_SYSTEM = "You are a careful scientist and teacher. You check edited explanations. Reply with JSON only."
LEAK_SYSTEM = ("You are a careful scientist and teacher. You check where a reader's facts came from. Reply with JSON "
               "only.")
PASSES = 3


def controls_file() -> Path:
    return project_root() / "evals" / "artifact" / "controls.yaml"


def load_controls() -> dict:
    """The cut list and the bar, with the source and baseline folders resolved against the project."""
    c = yaml.safe_load(controls_file().read_text())
    return {**c, "source": project_root() / c["source"], "baseline": project_root() / c["baseline"]}


# ---------------------------------------------------------------- 1. cuts

def apply_edits(text: str, edits: list[dict]) -> str:
    """The text with each edit applied in turn; each old text must occur exactly once when its turn comes."""
    if not isinstance(edits, list) or not edits:
        raise ValueError("no edits")
    for e in edits:
        if not isinstance(e, dict) or not str(e.get("old") or ""):
            raise ValueError(f"not an edit: {str(e)[:60]!r}")
        old, new = str(e["old"]), str(e.get("new") or "")
        n = text.count(old)
        if n != 1:
            raise ValueError(f"{'not found' if n == 0 else f'found {n} times'}: {old[:60]!r}")
        text = text.replace(old, new, 1)
    return re.sub(r"\n{3,}", "\n\n", text)


def cut_prompt(subject: dict, reader: str, spec: dict, text: str) -> str:
    steps = subject["rederive"]["steps"]
    keep = [steps[i - 1]["text"] for i in spec["clean"]]
    return "\n".join([
        f"Here is an explanation written for this reader: {reader}",
        f"After reading it, the reader will be asked: {subject['rederive']['q']}",
        "",
        f"Remove this idea from the explanation: {steps[spec['cut'] - 1]['text']}",
        "",
        "Remove every sentence that states it, and every sentence that would let this reader recover it, including "
        "a conclusion that gives it away. Keep everything else word for word; reword only where a removal breaks a "
        "sentence. Do not mark or mention any removal: the result must read as an explanation that never had the "
        "idea.",
        *(["", "These ideas must stay in the explanation:", *[f"- {k}" for k in keep]] if keep else []),
        "",
        "=== Explanation ===",
        text,
        "=== End ===",
        "",
        'Reply with JSON only: {"edits": [{"old": "<text copied exactly from the explanation>", "new": "<what '
        'replaces it, or empty to delete>"}]}. Each old must occur exactly once in the explanation.',
    ])


def cut_check_prompt(subject: dict, reader: str, spec: dict, text: str) -> str:
    t = subject["rederive"]
    blocks = [f"  {i}. {s['text']}" for i, s in enumerate(t["steps"], 1) if s["kind"] == "block"]
    clean = ", ".join(str(i) for i in spec["clean"])
    present = ", ".join(f'"{i}": true' for i in spec["clean"])
    return "\n".join([
        f"The reader: {reader}",
        f"After reading the explanation below, this reader will be asked: {t['q']}",
        "",
        "The building blocks of the answer, numbered as in the answer's steps:",
        *blocks,
        "",
        f"Block {spec['cut']} was meant to be removed from this explanation."
        + (f" Blocks {clean} must still be in it." if clean else ""),
        "",
        "=== Explanation ===",
        text,
        "=== End ===",
        "",
        "Answer each:",
        f"- recoverable: could this reader get block {spec['cut']} from this explanation, from the question, or from "
        "background this reader already has? If the explanation still carries it, quote the passage in quote.",
        "- present: for each block that must stay, is it still in the explanation?",
        "- marked: does the explanation show that text was removed: a marker, a note, or a reference to something "
        "that is no longer there?",
        "",
        f'Reply with JSON only: {{"recoverable": false, "quote": "", "present": {{{present}}}, "marked": false, '
        '"reason": "..."}',
    ])


def cut_passes(reply: dict, spec: dict) -> bool:
    present = reply.get("present") if isinstance(reply.get("present"), dict) else {}
    return (reply.get("recoverable") is False and reply.get("marked") is False
            and all(present.get(str(i)) is True for i in spec["clean"]))


def digest(text: str) -> str:
    return hashlib.sha256(text.encode()).hexdigest()[:16]


def reply_of(system: str, prompt: str, model: str | None) -> dict:
    try:
        reply = agent.parse_json(agent.ask(system, prompt, model=model))
    except ValueError:
        reply = {}
    return reply if isinstance(reply, dict) else {}


def attempt_cut(subject: dict, reader: str, spec: dict, text: str, model: str | None) -> tuple[dict, str | None]:
    """One attempt: a cut (a reply whose edits do not apply is asked once more) and, if one was made, its check."""
    attempt: dict = {"edits": [], "error": "", "check": {}, "passed": False}
    prompt, cut = cut_prompt(subject, reader, spec, text), None
    for _ in range(2):
        edits = reply_of(CUTTER_SYSTEM, prompt, model).get("edits")
        attempt["edits"] = edits if isinstance(edits, list) else []
        try:
            cut, attempt["error"] = apply_edits(text, edits), ""
            break
        except ValueError as e:
            attempt["error"] = str(e)
    if cut is None:
        return attempt, None
    attempt["check"] = reply_of(CHECKER_SYSTEM, cut_check_prompt(subject, reader, spec, cut), model)
    attempt["passed"] = cut_passes(attempt["check"], spec)
    return attempt, cut


def cut_subject(subject: dict, spec: dict, reader: str, c: dict, out: Path, redo: bool, model: str | None) -> dict:
    sid, src = subject["id"], c["source"] / "work" / subject["id"]
    for cond in UNCUT:   # the uncut builds, as the source run has them
        for f in ae.renderings(src / cond, sid):
            dst = out / "work" / sid / cond / f.relative_to(src / cond)
            if not dst.exists():
                dst.parent.mkdir(parents=True, exist_ok=True)
                shutil.copyfile(f, dst)
    originals = ae.renderings(src / c["condition"], sid)
    if len(originals) != 1:
        raise SystemExit(f"{sid}: expected one {c['condition']} rendering, found {len(originals)}")
    rel, text = originals[0].relative_to(src / c["condition"]), originals[0].read_text()
    copy, saved = out / "work" / sid / CUT / rel, out / "cuts" / f"{sid}.json"
    rec = json.loads(saved.read_text()) if saved.exists() else {
        "subject": sid, "cut": spec["cut"], "clean": spec["clean"], "verdict": "pending", "attempts": []}
    if (rec["verdict"] == "pass" and not redo) or len(rec["attempts"]) >= MAX_ATTEMPTS:
        return rec
    saved.parent.mkdir(parents=True, exist_ok=True)
    while len(rec["attempts"]) < MAX_ATTEMPTS:
        attempt, cut = attempt_cut(subject, reader, spec, text, model)
        rec["attempts"].append(attempt)
        rec.pop("hash", None)
        if attempt["passed"]:
            copy.parent.mkdir(parents=True, exist_ok=True)
            copy.write_text(cut)
            label = f"{c['condition']}/{rel.name}"
            (out / "cuts" / f"{sid}.diff").write_text("".join(difflib.unified_diff(
                text.splitlines(keepends=True), cut.splitlines(keepends=True), label, f"{label} (cut)")))
            rec.update(verdict="pass", hash=digest(cut))
        else:
            rec["verdict"] = "pending" if len(rec["attempts"]) < MAX_ATTEMPTS else "fail"
            if rec["verdict"] == "fail":
                copy.unlink(missing_ok=True)
                (out / "cuts" / f"{sid}.diff").unlink(missing_ok=True)
        saved.write_text(json.dumps(rec, indent=2, ensure_ascii=False) + "\n")
        if rec["verdict"] != "pending":
            break
    return rec


def make_cuts(out: Path, only: list[str] | None = None, redo: bool = False, model: str | None = None) -> dict[str, dict]:
    """Cuts one block from each listed subject's principles explanation into `out`, with the uncut builds beside it.
    The source run is only read; a rerun continues pending cuts and skips finished ones, unless `redo`."""
    c = load_controls()
    reader, subjects = ae.load("dev", list(c["cuts"]))
    out.mkdir(parents=True, exist_ok=True)
    names = {"none": "none", CUT: "principles, one block cut (PRD-002a)", "quick": "quick", "published": "published"}
    (out / "conditions.json").write_text(json.dumps(names, indent=2) + "\n")
    return {s["id"]: cut_subject(s, c["cuts"][s["id"]], reader, c, out, redo, model)
            for s in subjects if not only or s["id"] in only}


# ---------------------------------------------------------------- 2. the verdict

def mark_at(raw: object, i: int) -> str | None:
    """The grader's own mark for step i (1-based) in one pass, or None when it gave none."""
    return str(raw[i - 1]).strip().lower() if isinstance(raw, list) and len(raw) >= i else None


def caught(raws: list[object], i: int) -> bool:
    """The cut block was withheld in every pass. A pass with no mark from the grader is not a catch."""
    return bool(raws) and all(mark_at(r, i) in ("unsupported", "missing") for r in raws)


def kept(raws: list[object], i: int) -> bool:
    return bool(raws) and all(mark_at(r, i) == "supported" for r in raws)


def verdict(caught_by: dict[str, bool], lost_by: dict[str, int], dropped: list[str], leaked: list[str],
            bar: dict) -> dict:
    """The verdict under the bar fixed in PRD-002a, with leaked cuts left out of the count and, to show what the
    exclusions did, counted as misses. Exclusions alone cannot make the test trusted."""
    def need(counted: list[str]) -> int:
        return math.ceil(round(bar["catch"] * len(counted), 9))

    def judge(counted: list[str]) -> str:
        if len(counted) < bar["min_counted"]:
            return "inconclusive"
        if sum(caught_by[s] for s in counted) < need(counted):
            return "blind"
        return "inconclusive" if sum(lost_by.get(s, 0) for s in counted) > bar["clean_losses"] else "trusted"

    counted = [s for s in caught_by if s not in dropped and s not in leaked]
    with_leaks = [s for s in caught_by if s not in dropped]
    v, without = judge(counted), judge(with_leaks)
    return {"verdict": "inconclusive" if v == "trusted" and without == "blind" else v,
            "without_leak_exclusions": without, "counted": counted, "caught": sum(caught_by[s] for s in counted),
            "need": need(counted), "clean_losses": sum(lost_by.get(s, 0) for s in counted)}


# ---------------------------------------------------------------- 3. the run

def leak_prompt(block: str, chain: dict, text: str) -> str:
    return "\n".join([
        "A reader read the explanation below once, then worked out a question, naming the part of the explanation "
        "each step rests on.",
        f"This idea is not meant to be in the explanation: {block}",
        "",
        "=== Explanation ===",
        text,
        "=== End ===",
        "",
        "--- The reader's working ---",
        rederive.chain_text(chain),
        "",
        "Does a part the reader names, as it stands in this explanation, carry that idea? If it does, set leak to true "
        "and copy that passage word for word from the explanation into quote.",
        "",
        'Reply with JSON only: {"leak": false, "quote": ""}',
    ])


def quote_in(quote: str, text: str) -> bool:
    """The quote occurs in the text, ignoring differences in whitespace; an empty quote never does."""
    q = " ".join(str(quote).split())
    return bool(q) and q in " ".join(text.split())


def cut_copy(out: Path, sid: str) -> Path | None:
    found = ae.renderings(out / "work" / sid / CUT, sid)
    return found[0] if len(found) == 1 else None


def named(path: Path) -> str:
    """A folder named relative to the project, or by its name: never a path through the home folder."""
    try:
        return str(path.resolve().relative_to(project_root().resolve()))
    except ValueError:
        return path.name


def finished_cuts(out: Path, cuts: dict) -> dict[str, dict]:
    """Every cut's record, refusing a run while any cut is unfinished or a cut copy changed after its check."""
    records = {}
    for sid in cuts:
        path = out / "cuts" / f"{sid}.json"
        rec = json.loads(path.read_text()) if path.exists() else {}
        if rec.get("verdict") not in ("pass", "fail"):
            raise SystemExit(f"{sid}: its cut is not finished; run explainer eval cuts first")
        if rec["verdict"] == "pass":
            copy = cut_copy(out, sid)
            if copy is None or digest(copy.read_text()) != rec.get("hash"):
                raise SystemExit(f"{sid}: the cut copy changed after its check")
        records[sid] = rec
    return records


def leak_checked(out: Path, sid: str, k: int, block: str, model: str | None) -> dict:
    saved = out / "controls" / "leaks" / f"{sid}-pass-{k}.json"
    if saved.exists():
        return json.loads(saved.read_text())
    chain = json.loads((out / "rederive" / f"pass-{k}" / "read" / sid / f"{CUT}.json").read_text())
    text = cut_copy(out, sid).read_text()
    reply = reply_of(LEAK_SYSTEM, leak_prompt(block, chain, text), model)
    quote = str(reply.get("quote") or "")
    result = {"leak": reply.get("leak") is True, "quote": quote,
              "confirmed": reply.get("leak") is True and quote_in(quote, text)}
    saved.parent.mkdir(parents=True, exist_ok=True)
    saved.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n")
    return result


def run(out: Path, model: str | None = None, reader_model: str | None = None, workers: int = 4) -> Path:
    """Runs the unchanged rederivation stage on the cut copies in `out`, checks uncaught cuts for leaks, and reports
    the verdict. The baseline's chains for the uncut conditions are reused, so only the cut copies are read."""
    c = load_controls()
    by_id = {s["id"]: s for s in ae.load("dev", list(c["cuts"]))[1]}
    records = finished_cuts(out, c["cuts"])
    passing = [sid for sid in c["cuts"] if records[sid]["verdict"] == "pass"]
    dropped = [sid for sid in c["cuts"] if records[sid]["verdict"] == "fail"]
    for k in range(1, PASSES + 1):
        for sid in passing:
            for cond in UNCUT:
                rel = Path("rederive") / f"pass-{k}" / "read" / sid / f"{cond}.json"
                if not (out / rel).exists():
                    (out / rel).parent.mkdir(parents=True, exist_ok=True)
                    shutil.copyfile(c["baseline"] / rel, out / rel)
    if passing:   # an empty `only` would mean every subject
        rederive.run(out, out, split="dev", only=passing, model=model, reader_model=reader_model, workers=workers,
                     passes=PASSES)
    detail, caught_by, lost_by, leaked = {}, {}, {}, []
    for sid in passing:
        spec, steps = c["cuts"][sid], by_id[sid]["rederive"]["steps"]
        kinds = [s["kind"] for s in steps]
        grades = [json.loads((out / "rederive" / f"pass-{k}" / "grades" / f"{sid}.json").read_text())["grades"][CUT]
                  for k in range(1, PASSES + 1)]
        intact = [json.loads((c["baseline"] / "rederive" / f"pass-{k}" / "grades" / f"{sid}.json").read_text())
                  ["grades"][c["condition"]] for k in range(1, PASSES + 1)]
        raws = [g.get("raw") for g in grades]
        caught_by[sid] = caught(raws, spec["cut"])
        lost_by[sid] = sum(not kept(raws, i) for i in spec["clean"])
        leaks = {}
        if not caught_by[sid]:
            for k, raw in enumerate(raws, 1):
                if mark_at(raw, spec["cut"]) not in ("unsupported", "missing"):
                    leaks[k] = leak_checked(out, sid, k, steps[spec["cut"] - 1]["text"], model)
            if any(r["confirmed"] for r in leaks.values()):
                leaked.append(sid)
        chains = [json.loads((out / "rederive" / f"pass-{k}" / "read" / sid / f"{CUT}.json").read_text())
                  for k in range(1, PASSES + 1)]

        def share(g: dict) -> str:
            t = rederive.tally(g["marks"], kinds, g.get("result_right") is True, g.get("result_stated") is True)
            return f"{t['supported']}/{t['counted']}"

        detail[sid] = {
            "cut": spec["cut"], "clean": spec["clean"], "kinds": kinds, "caught": caught_by[sid],
            "clean_lost": lost_by[sid], "intact_marks": [g["marks"] for g in intact], "cut_raw": raws,
            "no_mark_passes": [k for k, raw in enumerate(raws, 1) if mark_at(raw, spec["cut"]) is None],
            "supported_intact": [share(g) for g in intact], "supported_cut": [share(g) for g in grades],
            "gap": [bool(ch.get("gap")) for ch in chains], "leaks": {str(k): v for k, v in leaks.items()}}
    v = verdict(caught_by, lost_by, dropped, leaked, c["bar"])
    result = {**v, "bar": c["bar"], "dropped": dropped, "leaked": leaked, "left_out": c["left_out"],
              "subjects": detail}
    (out / "controls.json").write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n")
    report = out / "controls.md"
    report.write_text(summary(result, c))
    return report


SHORT = {"supported": "s", "unsupported": "u", "missing": "m", "stated": "t"}


def summary(result: dict, c: dict) -> str:
    def marks_at(per_pass: list[object], i: int) -> str:
        return ", ".join(SHORT.get(mark_at(m, i) or "", "–") for m in per_pass)

    bar = result["bar"]
    lines = [
        f"# Rederivation controls, {date.today().isoformat()} (PRD-002a)", "",
        f"Source builds: `{named(c['source'])}`. Baseline: `{named(c['baseline'])}`. Each subject's "
        f"`{c['condition']}` explanation had one building block cut (`{CUT}` here); the reader read only the cut "
        "copy, the baseline's chains for the other three conditions were reused, and the grader graded all four "
        "fresh, blind, in three passes.", "",
        f"**Verdict: {result['verdict']}.** Caught in {result['caught']} of {len(result['counted'])} counted subjects "
        f"(needs {result['need']}); clean-set blocks lost: {result['clean_losses']} (at most {bar['clean_losses']}); "
        f"subjects counted: {len(result['counted'])} (at least {bar['min_counted']}). Counting every leaked cut as a "
        f"miss instead: {result['without_leak_exclusions']}.", "",
        "Marks per pass (the grader's own marks): s supported, u unsupported, m missing, t stated, – none given. "
        "Caught: the cut block is u or m in all three passes.", "",
        "| subject | cut block | intact (baseline) | cut | caught | uncut blocks | derived, intact → cut | "
        "supported, intact → cut | gap named | leak check |",
        "|---|---|---|---|---|---|---|---|---|---|",
    ]
    for sid, d in result["subjects"].items():
        blocks = [i for i, kd in enumerate(d["kinds"], 1) if kd == "block" and i != d["cut"]]
        derived = [i for i, kd in enumerate(d["kinds"], 1) if kd == "derived"]
        found = {(True, True): "leak, confirmed", (True, False): "leak, quote not found"}
        leak = "; ".join(f"pass {k}: {found.get((r['leak'], r['confirmed']), 'no leak')}"
                         for k, r in d["leaks"].items()) or "–"
        lines.append("| " + " | ".join([
            sid, str(d["cut"]), marks_at(d["intact_marks"], d["cut"]), marks_at(d["cut_raw"], d["cut"]),
            "yes" if d["caught"] else "no",
            "; ".join(f"{i}: {marks_at(d['cut_raw'], i)}" for i in blocks) or "–",
            "; ".join(f"{i}: {marks_at(d['intact_marks'], i)} → {marks_at(d['cut_raw'], i)}" for i in derived),
            f"{', '.join(d['supported_intact'])} → {', '.join(d['supported_cut'])}",
            ", ".join("yes" if g else "no" for g in d["gap"]), leak]) + " |")
    no_mark = [f"{sid} (pass {', '.join(map(str, d['no_mark_passes']))})"
               for sid, d in result["subjects"].items() if d["no_mark_passes"]]
    lines += [
        "",
        "Intact marks are the baseline's recorded marks, in which `stated` on a block had already been turned into "
        "`supported`; the cut copy's are the grader's own.",
        "",
        f"Passes with no grader mark for the cut block (counted as not caught): {', '.join(no_mark) or 'none'}.",
        "",
        "Labels: the stage shuffles labels once per subject from one generator per pass, and this run covers fewer "
        "subjects than the baseline, so each subject's label shuffle differs from its baseline pass.",
        "",
        f"Dropped (the cut failed its check {MAX_ATTEMPTS} times): {', '.join(result['dropped']) or 'none'}.",
        f"Leaked (a confirmed passage still carries the cut block): {', '.join(result['leaked']) or 'none'}.",
        "",
        "## Left out",
        "",
        *[f"- **{sid}.** {why}" for sid, why in result["left_out"].items()],
    ]
    return "\n".join(lines) + "\n"
