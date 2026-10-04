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

    shots = []  # (time, heading, text, issues)
    for e in timeline["events"]:
        if e["kind"] == "voiceover":
            shots.append((e["t"] + min(0.8, e["duration"] / 2), "line", e["text"], []))
        elif e["kind"] == "bookmark":
            shots.append((e["t"] + 0.5, f"bookmark '{e['mark']}'", "", e.get("issues", [])))
        elif e["kind"] == "predict":
            shots.append((e["t"] + 1.0, "PREDICT", e["question"], []))
        elif e["kind"] == "claim":
            shots.append((e["t"] + 0.6, f"claim '{e['id']}'", "", []))
        elif e["kind"] == "voiceover_end" and e.get("issues"):
            shots.append((max(e["t"] - 0.05, 0), "end of line", "", e["issues"]))
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
            color = (255, 210, 90) if heading == "PREDICT" else (230, 230, 230)
            draw.text((x, y + th + 4), f"{t:6.2f}s  {heading}", fill=color, font=bold)
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
    return out


# ---------------------------------------------------------------- probe (before rendering)

PROBE_RULES = [
    "Why this form. For every formula, function, or operation, does the model say why it is this form and not "
    "a simpler alternative? Name the most natural alternative and what would go wrong with it.",
    "Guarantees. For every guarantee, invariant, or 'always / never' claim, does the model give a concrete "
    "instance with numbers where it holds, AND a concrete instance where removing its assumption breaks it?",
    "Terms. Is every term defined before it is used?",
    "Worked examples. Does every mechanism step have a worked example with real numbers?",
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
        'Reply with JSON only: {"gaps": [{"rule": 1-5, "about": "...", "why_it_matters": "...", '
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
    lines += [
        "",
        "Answer from the explanation alone. If it does not let you answer, say so: that is useful evidence.",
        "Do not use outside knowledge to fill gaps, even when you know the subject.",
        "",
        "Questions:",
        *[f"{i}. {q}" for i, q in enumerate(questions, 1)],
        "",
        'Reply with JSON only: {"answers": {"1": "...", "2": "...", ...}, "gaps": ["..."]}',
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
    lines += ["", "A rendering passes when every quiz item scores 2 and no general item scores 0."]
    return "\n".join(lines)
