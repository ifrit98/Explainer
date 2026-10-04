"""Chat eval: does a system prompt make chat answers about phenomena better for a technical reader?

Each question in evals/chat/questions.yaml is answered once per condition (a system prompt) by the `claude`
CLI, run in an empty folder with no tools and no settings, so no CLAUDE.md or plugin reaches it. A grader,
also a fresh `claude -p`, sees the answers of one question under shuffled labels and scores each: the
points a good answer must make, the misconception, whether the answer comes first, and excess (what this
reader did not need). Both directions count: a missing mechanism and a padded answer both cost the reader.
"""

from __future__ import annotations

import json
import random
import re
import subprocess
import tempfile
from concurrent.futures import ThreadPoolExecutor
from datetime import date
from pathlib import Path

import yaml

from explainer_kit.paths import display, project_root

NEUTRAL = "You are Claude, a helpful assistant. Answer the user's question."
PRINCIPLES = Path(__file__).resolve().parent.parent / "plugin" / "skills" / "explain" / "references" / "principles.md"
GRADER = "You are a strict technical editor and a careful scientist. You grade explanations. Reply with JSON only."


def questions_file() -> Path:
    return project_root() / "evals" / "chat" / "questions.yaml"


def load_questions(path: Path | None = None) -> dict:
    return yaml.safe_load((path or questions_file()).read_text())


def system_prompt(source: str) -> str:
    """'none' (a neutral prompt), 'principles' (the current principles.md), 'git:<rev>' (principles.md at a
    tag or commit), or a file path."""
    if source == "none":
        return NEUTRAL
    if source == "principles":
        return PRINCIPLES.read_text()
    if source.startswith("git:"):
        rel = PRINCIPLES.relative_to(project_root())
        return subprocess.run(["git", "show", f"{source[4:]}:{rel}"], cwd=project_root(), check=True,
                              capture_output=True, text=True).stdout
    return Path(source).read_text()


def ask(system: str, prompt: str, model: str | None = None, timeout: int = 300) -> str:
    """One fresh `claude -p` call in an empty folder: no tools, no settings files, no MCP servers, no CLAUDE.md,
    and no stdin (claude -p appends piped input to the prompt)."""
    cmd = ["claude", "-p", "--setting-sources", "project", "--strict-mcp-config", "--tools", "",
           "--system-prompt", system]
    if model:
        cmd += ["--model", model]
    with tempfile.TemporaryDirectory() as empty:
        out = subprocess.run(cmd + [prompt], cwd=empty, capture_output=True, text=True, timeout=timeout,
                             stdin=subprocess.DEVNULL)
    if out.returncode != 0:
        raise RuntimeError(f"claude -p failed: {out.stderr.strip()[:300]}")
    return out.stdout.strip()


def grade_prompt(reader: str, item: dict, answers: dict[str, str]) -> str:
    must = "\n".join(f"  {i}. {m}" for i, m in enumerate(item["must"], 1))
    blocks = "\n\n".join(f"=== Answer {label} ===\n{text}" for label, text in answers.items())
    labels = ", ".join(answers)
    return "\n".join([
        f"Question: {item['q']}",
        f"The reader: {reader}",
        "",
        "A good answer for this reader makes these points (in any words):",
        must,
        f"It must not teach this misconception: {item['misconception']}",
        f"Word budget: about {item['budget']} words. Length alone is not a fault; text the reader did not need is.",
        "",
        blocks,
        "",
        "Grade each answer on its own. For each:",
        "- must: a list with one score per point above: 0 missing, 1 vague or partly wrong, 2 clear and correct.",
        "- misconception: 'taught' (it states or implies it), 'corrected' (it names and refutes it), or 'absent'.",
        "- answer_first: true if the first one or two sentences answer the question.",
        "- errors: every factual error, quoted.",
        "- excess: every sentence or passage this reader did not need (already known, repeated, off the question, "
        "filler, or a detour), quoted.",
        "- unclear: every passage this reader would have to read twice (undefined term, ambiguous pronoun, "
        "abstract noun phrase where a direct causal statement would do), quoted.",
        "- score: 0-10, how well the answer lets this reader build an accurate mental model with the least effort.",
        f"Then rank the answers from best to worst (labels {labels}), and say in one sentence why the best is best.",
        "",
        'Reply with JSON only: {"grades": {"<label>": {"must": [0,1,2], "misconception": "...", "answer_first": '
        'true, "errors": ["..."], "excess": ["..."], "unclear": ["..."], "score": 0}}, "rank": ["<label>", ...], '
        '"why_best": "..."}',
    ])


def parse_json(text: str) -> dict:
    m = re.search(r"\{.*\}", text, re.S)
    if not m:
        raise ValueError(f"no JSON in grader reply: {text[:200]}")
    return json.loads(m.group(0))


def words(text: str) -> int:
    return len(re.findall(r"[A-Za-z][A-Za-z'’-]*", text))


def run(conditions: dict[str, str], out: Path, model: str | None = None, workers: int = 6, seed: int = 0) -> Path:
    spec = load_questions()
    reader, items = spec["reader"], spec["questions"]
    systems = {name: system_prompt(src) for name, src in conditions.items()}
    (out / "answers").mkdir(parents=True, exist_ok=True)

    jobs = [(item, name) for item in items for name in conditions]
    with ThreadPoolExecutor(workers) as pool:
        texts = list(pool.map(lambda j: ask(systems[j[1]], j[0]["q"], model), jobs))
    answers: dict[str, dict[str, str]] = {}
    for (item, name), text in zip(jobs, texts):
        answers.setdefault(item["id"], {})[name] = text
        (out / "answers" / f"{item['id']}.{name}.md").write_text(f"# {item['q']}\n\n_{name}_\n\n{text}\n")
        print(f"answer  {item['id']:16} {name:12} {words(text):4} words")

    rng = random.Random(seed)
    keys: dict[str, dict[str, str]] = {}
    prompts = []
    for item in items:
        names = list(conditions)
        rng.shuffle(names)
        key = {chr(ord("A") + i): n for i, n in enumerate(names)}
        keys[item["id"]] = key
        prompts.append(grade_prompt(reader, item, {lab: answers[item["id"]][n] for lab, n in key.items()}))
    with ThreadPoolExecutor(workers) as pool:
        replies = list(pool.map(lambda p: parse_json(ask(GRADER, p, model)), prompts))

    grades = {}
    for item, reply in zip(items, replies):
        key = keys[item["id"]]
        grades[item["id"]] = {
            "key": key, "why_best": reply.get("why_best", ""),
            "rank": [key[lab] for lab in reply["rank"] if lab in key],
            "grades": {key[lab]: g for lab, g in reply["grades"].items() if lab in key},
            "words": {n: words(answers[item["id"]][n]) for n in conditions},
        }
        print(f"grade   {item['id']:16} best: {grades[item['id']]['rank'][0]}")
    (out / "grades.json").write_text(json.dumps(grades, indent=2, ensure_ascii=False))
    report = out / "report.md"
    report.write_text(summary(conditions, items, grades, model))
    print(f"\nreport  {display(report)}")
    return report


def summary(conditions: dict[str, str], items: list[dict], grades: dict, model: str | None) -> str:
    rows = []
    for name in conditions:
        g = [grades[i["id"]]["grades"][name] for i in items]
        n = len(g)
        must = sum(sum(x["must"]) for x in g) / sum(2 * len(i["must"]) for i in items)
        rows.append([
            name, f"{sum(x['score'] for x in g) / n:.1f}", f"{must:.0%}",
            str(sum(x["misconception"] == "taught" for x in g)),
            str(sum(x["misconception"] == "corrected" for x in g)),
            f"{sum(bool(x['answer_first']) for x in g)}/{n}",
            str(sum(len(x["errors"]) for x in g)),
            f"{sum(len(x['excess']) for x in g) / n:.1f}",
            f"{sum(len(x['unclear']) for x in g) / n:.1f}",
            f"{sum(grades[i['id']]['words'][name] for i in items) / n:.0f}",
            str(sum(grades[i["id"]]["rank"][0] == name for i in items)),
        ])
    head = ["condition", "score /10", "must points", "misconception taught", "corrected", "answer first",
            "errors", "excess / answer", "unclear / answer", "words", "ranked best"]
    lines = [f"# Chat eval, {date.today().isoformat()}", "",
             f"Answers and grades by `claude -p`{f' --model {model}' if model else ''} (fresh, no tools, no settings). "
             "The grader saw each question's answers under shuffled labels.", "",
             "Conditions: " + "; ".join(f"**{n}** = `{s}`" for n, s in conditions.items()), "",
             "| " + " | ".join(head) + " |", "|" + "---|" * len(head)]
    lines += ["| " + " | ".join(r) + " |" for r in rows]
    lines += ["", "## Per question", ""]
    for i in items:
        gr = grades[i["id"]]
        lines.append(f"- **{i['id']}**: ranked {' > '.join(gr['rank'])}. {gr['why_best']}")
    return "\n".join(lines) + "\n"
