"""Review tools: a frame-by-event review sheet, and the blind understanding test.

Review sheet: one frame at each narration line, bookmark, and predict pause, with
the spoken text under it and any layout issue (overlap, off-frame) in red.

Blind test: a fresh agent sees only one rendering and answers the seven
understanding questions plus the model's quiz. Its answers are scored against the
quiz's expected answers. The prompt never includes model.md or model.yaml.
"""

from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import textwrap
from pathlib import Path

from explainer_kit.model import read_model
from explainer_kit.paths import display, explainer_dir

UNDERSTANDING = [
    "Name the main objects (entities) of the subject.",
    "Explain how those objects relate to each other.",
    "State the central causal chain in one or two sentences.",
    "Predict what changes when the most important variable changes, and why.",
    "Name one assumption or simplification, and one observation or established fact.",
    "Rebuild the whole explanation in your own words in at most five sentences.",
    "Which part was hardest to follow, and what would have made it easier?",
]

# Audit: what a blind reviewer reports beyond its answers. Each finding is a gap to fix or to dismiss
# with a reason in review/understanding.md.
AUDIT = {
    "terms": "Every concept named by two or more different words (quote each word and where it appears).",
    "unexplained": "Every number, score, or measure shown without saying what it means for the reader "
                   "(what would be different at a higher or lower value).",
    "missing_why": "Every formula or step stated without why it has this form.",
}
AUDIT_VIDEO = {
    "pace": "Every point where the narration moves on before the screen shows what it says, or where a key "
            "result gets no pause to absorb it (give the time from the review sheet).",
}

# Pace: a key claim needs a picture per step and a pause after it. Measured from the timeline.
HOLD_AFTER_CLAIM = 1.0     # s of silence after the line that makes a claim
ONE_PICTURE_LIMIT = 10.0   # s of narration after a claim mark with no further bookmark

BLIND_FILES = {
    "prose": ["explanation.md"],
    "diagram": ["diagram.md"],
    "html": ["index.html"],
    "video": ["video/captions.srt", "video/review.png"],
}


# ---------------------------------------------------------------- review sheet

def review_sheet(slug: str, draft: bool = False) -> Path:
    from PIL import Image, ImageDraw, ImageFont

    video = explainer_dir(slug) / "video"
    prefix = "draft-" if draft else ""
    movie = video / ("draft.mp4" if draft else "out.mp4")
    timeline_file = video / f"{prefix}timeline.json"
    if not movie.exists() or not timeline_file.exists():
        sys.exit(f"render first: explainer render {slug}{' --draft' if draft else ''}")
    timeline = json.loads(timeline_file.read_text())

    # (frame time, heading, text, issues). The frame is taken a moment after the event, so the animation it
    # starts is visible; the heading shows the event's own time, which matches captions.srt.
    shots = []
    for e in timeline["events"]:
        at = f"{e['t']:6.2f}s"
        if e["kind"] == "voiceover":
            shots.append((e["t"] + min(0.8, e["duration"] / 2), f"{at}  line", e["text"], []))
        elif e["kind"] == "bookmark":
            shots.append((e["t"] + 0.5, f"{at}  bookmark '{e['mark']}'", "", e.get("issues", [])))
        elif e["kind"] == "predict":
            shots.append((e["t"] + 1.0, f"{at}  PREDICT", e["question"], []))
        elif e["kind"] == "claim":
            shots.append((e["t"] + 0.6, f"{at}  claim '{e['id']}'", "", []))
        elif e["kind"] == "voiceover_end" and e.get("issues"):
            shots.append((max(e["t"] - 0.05, 0), f"{at}  end of line", "", e["issues"]))
    shots.sort(key=lambda s: s[0])

    tw, th, pad, text_h, cols = 480, 270, 10, 118, 3
    rows = (len(shots) + cols - 1) // cols
    sheet = Image.new("RGB", (cols * (tw + pad) + pad, rows * (th + text_h + pad) + pad), (24, 26, 31))
    draw = ImageDraw.Draw(sheet)
    try:
        font = ImageFont.load_default(size=15)
        bold = ImageFont.load_default(size=16)
    except TypeError:
        font = bold = ImageFont.load_default()

    with tempfile.TemporaryDirectory() as tmp:
        for i, (t, heading, text, issues) in enumerate(shots):
            frame = Path(tmp) / f"{i}.png"
            subprocess.run(["ffmpeg", "-y", "-v", "error", "-ss", f"{t:.3f}", "-i", str(movie), "-frames:v", "1",
                            "-vf", f"scale={tw}:{th}", str(frame)], check=True)
            x = pad + (i % cols) * (tw + pad)
            y = pad + (i // cols) * (th + text_h + pad)
            if frame.exists():
                sheet.paste(Image.open(frame), (x, y))
            color = (255, 210, 90) if heading.endswith("PREDICT") else (230, 230, 230)
            draw.text((x, y + th + 4), heading, fill=color, font=bold)
            lines = textwrap.wrap(text, 62)[:3]
            lines += [f"⚠ {iss}" for iss in issues][:4 - len(lines) if lines else 4]
            for j, line in enumerate(lines):
                fill = (255, 110, 100) if line.startswith("⚠") else (190, 194, 200)
                draw.text((x, y + th + 26 + j * 21), line, fill=fill, font=font)
    out = video / f"{prefix}review.png"
    sheet.save(out)

    issues = [(round(s[0], 2), i) for s in shots for i in s[3]]
    print(f"review    {display(out)}  ({len(shots)} frames)")
    print(f"layout    {'no issues' if not issues else f'{len(issues)} issue(s)'}")
    for t, i in issues:
        print(f"  {t:6.2f}s  {i}")
    pace = pace_issues(timeline["events"])
    print(f"pace      {'no issues' if not pace else f'{len(pace)} issue(s)'}")
    for i in pace:
        print(f"  {i}")
    return out


def pace_issues(events: list[dict]) -> list[str]:
    """Claims the viewer gets no time for: no pause after the claim's line, or a long stretch of
    narration over one picture after the claim mark."""
    voice = [e for e in events if e["kind"] == "voiceover"]
    ends = [e for e in events if e["kind"] == "voiceover_end"]
    issues = []
    for c in (e for e in events if e["kind"] == "claim"):
        line = max((v for v in voice if v["t"] <= c["t"] + 1e-6), key=lambda v: v["t"], default=None)
        if line is None:
            continue
        end = line["t"] + line["duration"]
        end = min((e["t"] for e in ends if e["t"] >= c["t"] - 1e-6), default=end)
        nxt = min((v["t"] for v in voice if v["t"] > line["t"]), default=None)
        hold = (nxt if nxt is not None else end + HOLD_AFTER_CLAIM) - end
        if hold < HOLD_AFTER_CLAIM - 0.05:
            issues.append(f"pace: claim '{c['id']}' at {c['t']:.1f}s has "
                          f"{max(hold, 0):.1f}s of pause after its line (< {HOLD_AFTER_CLAIM:.0f}s); add self.wait()")
        marks = [t for t in (line.get("bookmarks") or {}).values() if t > c["t"] + 0.05]
        talk = (min(marks) if marks else end) - c["t"]
        if talk > ONE_PICTURE_LIMIT:
            issues.append(f"pace: claim '{c['id']}' at {c['t']:.1f}s talks {talk:.0f}s over one picture; split the "
                          f"line, one step per line or bookmark")
    return issues


# ---------------------------------------------------------------- probe (before rendering)

PROBE_RULES = [
    "Why this form. For every formula, function, or operation, does the model say why it is this form and not "
    "a simpler alternative? Name the most natural alternative and what would go wrong with it.",
    "Guarantees. For every guarantee, invariant, or 'always / never' claim, does the model give a concrete "
    "instance with numbers where it holds, AND a concrete instance where removing its assumption breaks it? "
    "Check each step of its argument as written: does it name the right objects (which set, which nodes, which "
    "value), and is any step left implicit?",
    "Terms. Is every term defined before it is used, and does each concept have exactly one name? List "
    "each concept the file names in two ways (for example a tentative value and a final value both called "
    "'distance').",
    "Worked examples. Does every mechanism step have a worked example with real numbers?",
    "Meaning. For every quantity, score, or measure the explanation will show, does the model say what the "
    "number means for the reader, with a value from the example (what is different at a low value and a high "
    "one)?",
    "Next questions. What are the next five questions a learner would ask, most important first? Mark each one "
    "the model cannot answer, and each one its Scope section already declares out of scope.",
]


def probe_prompt(slug: str) -> str:
    """Prompt for a fresh agent that reads only model.md and lists what the explanation will omit."""
    model_md = explainer_dir(slug) / "model.md"
    if not model_md.exists():
        sys.exit(f"missing {display(model_md)}")
    return "\n".join([
        "You are a curious, careful learner and a skeptical reviewer. The file below is the semantic model for "
        "an explanation: the plan that its renderings will follow. Find what it omits BEFORE anything is rendered.",
        "",
        "Read ONLY this file. Do not open other files and do not search the web:",
        f"- {model_md}",
        "",
        "Check it against these rules:",
        *[f"{i}. {r}" for i, r in enumerate(PROBE_RULES, 1)],
        "",
        "Use your own knowledge of the subject to judge what is missing, but report only gaps in the file. "
        "Give numbers in every suggested addition; they will be recomputed before use.",
        "",
        'Reply with JSON only: {"gaps": [{"rule": 1-6, "about": "...", "why_it_matters": "...", '
        '"suggested_addition": "..."}], "next_questions": [{"q": "...", "answered_by_model": true|false, '
        '"declared_out_of_scope": true|false}]}',
    ])


# ---------------------------------------------------------------- blind test

def quiz_prompt(slug: str, rendering: str) -> str:
    folder = explainer_dir(slug)
    model = read_model(folder / "model.yaml")
    files = [folder / f for f in BLIND_FILES[rendering]]
    missing = [display(f) for f in files if not f.exists()]
    if missing:
        sys.exit(f"missing for a {rendering} blind test: {', '.join(missing)}"
                 + (f" (run: explainer review {slug})" if rendering == "video" else ""))
    questions = UNDERSTANDING + [q["q"] for q in model["quiz"]] + [c["ask"] for c in model["claims"] if c.get("ask")]
    lines = [
        "You are a blind reviewer for an explanation. You know nothing about it except the files below.",
        "",
        "Read ONLY these files. Do not open any other file, and do not search the web:",
        *[f"- {f}" for f in files],
    ]
    if rendering == "video":
        lines += ["", "The video is given as its transcript (captions.srt) and a review sheet (review.png): one frame "
                  "at each narration line, with the spoken text under it. Look at the image."]
    if rendering == "html":
        lines += ["", "The page is interactive. Read its visible text and its script to learn what the controls do."]
    audit = {**AUDIT, **(AUDIT_VIDEO if rendering == "video" else {})}
    lines += [
        "",
        "Answer from the explanation alone. If it does not let you answer, say so: that is useful evidence.",
        "Do not use outside knowledge to fill gaps, even when you know the subject.",
        "",
        "Questions:",
        *[f"{i}. {q}" for i, q in enumerate(questions, 1)],
        "",
        "Then audit the explanation. List, with quotes and locations (an empty list when there are none):",
        *[f"- {k}: {v}" for k, v in audit.items()],
        "",
        'Reply with JSON only: {"answers": {"1": "...", "2": "...", ...}, "audit": {'
        + ", ".join(f'"{k}": ["..."]' for k in audit) + '}, "gaps": ["..."]}',
    ]
    return "\n".join(lines)


def quiz_rubric(slug: str) -> str:
    model = read_model(explainer_dir(slug) / "model.yaml")
    n = len(UNDERSTANDING)
    lines = [f"Rubric for {slug}. Questions 1–{n} are the general understanding test: score each 0 (wrong or "
             "missing), 1 (partial), 2 (correct and specific) against model.md.", ""]
    for i, q in enumerate(model["quiz"], n + 1):
        lines += [f"{i}. {q['q']}", f"   expect: {q['expect']}"]
        if q.get("misconception"):
            lines.append(f"   wrong if it says: {q['misconception']}")
    for i, c in enumerate([c for c in model["claims"] if c.get("ask")], n + len(model["quiz"]) + 1):
        lines += [f"{i}. {c['ask']}", f"   expect: {c['statement']}"]
        for field in ("example", "counterexample"):
            if c.get(field):
                lines.append(f"   a full answer also gives the {field}: {c[field]}")
    lines += ["", "A rendering passes when every quiz item scores 2 and no general item scores 0.",
              "Each audit finding is a gap: fix it in the rendering, or record in review/understanding.md why it "
              "stands."]
    return "\n".join(lines)
