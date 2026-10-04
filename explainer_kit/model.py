"""The machine-readable model, and the check that keeps renderings consistent with it.

Each explainer has `model.md` (prose for people) and `model.yaml` (data for tools):

    values:      # nested numbers and strings: the facts that renderings show
    allow:       # structural numbers that are not model values (counts, slider ends, ...)
    require:     # values each listed rendering must show, unless it loads the model
      - {path: logits, in: [prose, diagram, html, video]}  # '/' nests: probabilities/T=1.0
    quiz:        # blind understanding test: questions with expected answers
    claims:      # the ideas the explanation must convey, each marked where a rendering covers it
      - {id: why-exp, kind: why, about: [exp], statement: ..., alternative: ..., counterexample: ...}
    accept_unjustified: {log: "reason"}   # functions deliberately left without a why claim
    terms:       # one word per concept: phrases a rendering must not use for it
      - {term: estimate, means: ..., avoid: [smallest distance]}

Renderings are found by name: explanation.md (prose), diagram.md (diagram),
index.html (html), video/scene.py (video). A rendering *loads the model* when
the scene calls `load_model(...)`, or the page has a synced
`<script type="application/json" id="explainer-model">` block.

`explainer check` reports:
1. numbers a reader sees that no model value or allowance explains;
2. required values that a rendering does not show;
3. pages whose embedded model block is out of date (fix: `explainer sync`);
4. incomplete claims: a `why` without the alternative it beats, a `guarantee` without an example and a
   counterexample, a `mechanism` without a worked example;
5. claims a rendering does not cover (markers: `<!-- claim: id -->` in Markdown, `data-claim="id"` in
   HTML, `self.claim("id")` in a scene);
6. functions in model.md (exp, log, sqrt, …) that no `why` claim justifies;
7. a phrase a `terms` entry avoids (a second name for one concept);
8. a page that embeds this explainer's video with plain <video> although the video has predict pauses
   (use `Explainer.video`, which stops at them);
9. with a `narrative.md`: a symbol on screen in the video that its introduction ledger does not list.
"""

from __future__ import annotations

import ast
import html
import json
import os
import re
from dataclasses import dataclass, field
from pathlib import Path

import yaml

RENDERINGS = {"prose": "explanation.md", "diagram": "diagram.md", "html": "index.html", "video": "video/scene.py"}
MODEL_BLOCK = re.compile(r'(<script type="application/json" id="explainer-model">)(.*?)(</script>)', re.S)


# ---------------------------------------------------------------- loading

def find_model_file(start: str | Path | None = None) -> Path:
    """model.yaml for a scene file, an explainer folder, or EXPLAINER_SLUG_DIR."""
    if start is None:
        start = os.environ.get("EXPLAINER_SLUG_DIR") or Path.cwd()
    p = Path(start).resolve()
    for d in ([p] if p.is_dir() else []) + list(p.parents):
        if (d / "model.yaml").exists():
            return d / "model.yaml"
    raise FileNotFoundError(f"no model.yaml at or above {p}")


def load_model(start: str | Path | None = None) -> dict:
    """The `values` of the nearest model.yaml. In a scene: `M = load_model(__file__)`."""
    return read_model(find_model_file(start)).get("values", {})


def read_model(path: Path) -> dict:
    data = yaml.safe_load(path.read_text()) or {}
    data.setdefault("values", {})
    data.setdefault("allow", [])
    data.setdefault("require", [])
    data.setdefault("quiz", [])
    data.setdefault("claims", [])
    data.setdefault("accept_unjustified", {})
    data.setdefault("terms", [])
    data.setdefault("budget", {})
    return data


def get_path(values: dict, path: str):
    """Look up 'a/b/0' in nested values. '/' separates keys, so keys may contain dots (e.g. 'T=1.0')."""
    node = values
    for key in path.split("/"):
        node = node[int(key)] if isinstance(node, list) else node[key]
    return node


def numeric_leaves(node) -> list[float]:
    if isinstance(node, bool):
        return []
    if isinstance(node, (int, float)):
        return [float(node)]
    if isinstance(node, dict):
        return [x for v in node.values() for x in numeric_leaves(v)]
    if isinstance(node, list):
        return [x for v in node for x in numeric_leaves(v)]
    if isinstance(node, str):  # keys like "T=0.5" are labels; string values may hold numbers too
        return []
    return []


def numeric_keys(node) -> list[float]:
    """Numbers inside dict keys such as 'T=0.5' count as model values too."""
    out = []
    if isinstance(node, dict):
        for k, v in node.items():
            out += [n.value for n in extract_numbers(str(k))]
            out += numeric_keys(v)
    elif isinstance(node, list):
        for v in node:
            out += numeric_keys(v)
    return out


# ---------------------------------------------------------------- number extraction

@dataclass
class Num:
    value: float
    decimals: int
    percent: bool
    text: str
    where: str = ""


NUM_RE = re.compile(r"(?<![\w.\-−])([-−]?(?:\d{1,3}(?:,\d{3})+|\d+))(\.\d+)?(?!\w)(?!\.\d)")
IGNORE_BEFORE = re.compile(r"(?:stage|level|step|rule|unit|scene|figure|table|item|phase|part|chapter|§|#)s?\s*"
                           r"(?:\d+\s*(?:[–-]|,|and|or|to)\s*)*$", re.I)
UNITS = {w: i for i, w in enumerate("zero one two three four five six seven eight nine ten eleven twelve thirteen "
                                    "fourteen fifteen sixteen seventeen eighteen nineteen".split())}
TENS = {w: 10 * i for i, w in enumerate("_ _ twenty thirty forty fifty sixty seventy eighty ninety".split()) if i >= 2}
WORD_RE = re.compile(r"\b(?:(?:%s)(?:[-\s]+(?:%s|hundred|thousand|and|point|half))*)\b(\s+percent)?"
                     % ("|".join([*UNITS, *TENS, "a half"]), "|".join([*UNITS, *TENS])), re.I)


SUPERSCRIPT = str.maketrans("⁰¹²³⁴⁵⁶⁷⁸⁹⁻⁺", "0123456789-+")
# 6.0 × 10⁻⁶, 6.0e-6, 2e-3. The e-form needs a decimal point or a signed exponent, so hash fragments
# such as "4e10" stay identifiers.
SCI_RE = re.compile(r"(?<![\w.])([-−]?\d+(?:\.\d+)?)\s*[×x·]\s*10([⁻⁺]?[⁰¹²³⁴⁵⁶⁷⁸⁹]+)"
                    r"|(?<![\w.])([-−]?\d+\.\d+[eE][-+]?\d+|[-−]?\d+[eE][-+]\d+)(?!\w)")


def extract_numbers(text: str, where: str = "", words: bool = False) -> list[Num]:
    """Numbers a reader sees in `text`. Skips stage/step/rule numbers, years, and identifiers."""
    found = []
    for m in SCI_RE.finditer(text):  # 6.0 × 10⁻⁶ and 6.0e-6 are one number each
        if m.group(1):
            mant, exponent = m.group(1).replace("−", "-"), int(m.group(2).translate(SUPERSCRIPT))
        else:
            mant, exp_text = re.split(r"[eE]", m.group(3).replace("−", "-"))
            exponent = int(exp_text)
        value = float(mant) * 10 ** exponent
        decimals = max(0, -exponent + (len(mant.split(".")[1]) if "." in mant else 0))
        found.append(Num(value, decimals, False, m.group(0), where))
    text = SCI_RE.sub(" ", text)
    for m in NUM_RE.finditer(text):
        before = text[max(0, m.start() - 24):m.start()]
        if IGNORE_BEFORE.search(before):
            continue
        whole = m.group(1).replace(",", "").replace("−", "-")
        frac = m.group(2) or ""
        value = float(whole + frac)
        if not frac and 1900 <= value <= 2100:  # a year
            continue
        after = text[m.end():m.end() + 9].lstrip()
        found.append(Num(value, len(frac) - 1 if frac else 0, after.startswith(("%", "percent")),
                         m.group(0), where))
    if words:
        found += extract_number_words(text, where)
    return found


def extract_number_words(text: str, where: str = "") -> list[Num]:
    out = []
    for m in WORD_RE.finditer(text):
        phrase = m.group(0)
        before = text[max(0, m.start() - 24):m.start()]
        if IGNORE_BEFORE.search(before):
            continue
        value = words_to_number(re.sub(r"\s+percent$", "", phrase, flags=re.I))
        if value is None:
            continue
        out.append(Num(value, 2 if value != int(value) else 0, bool(m.group(1)), phrase, where))
    return out


def words_to_number(phrase: str) -> float | None:
    tokens = [t for t in re.split(r"[-\s]+", phrase.lower()) if t and t != "and"]
    if tokens in (["a", "half"], ["one", "half"], ["half"]):
        return 0.5
    if tokens[-1:] == ["half"] and len(tokens) > 1:  # "two and a half"
        base = words_to_number(" ".join(t for t in tokens[:-1] if t != "a"))
        return None if base is None else base + 0.5
    if "point" in tokens:
        i = tokens.index("point")
        whole = words_to_number(" ".join(tokens[:i])) if i else 0
        digits = [UNITS.get(t) for t in tokens[i + 1:]]
        if whole is None or None in digits or any(d > 9 for d in digits):
            return None
        return float(f"{int(whole)}." + "".join(map(str, digits)))
    total, current = 0, 0
    for t in tokens:
        if t in UNITS:
            current += UNITS[t]
        elif t in TENS:
            current += TENS[t]
        elif t == "hundred":
            current = max(current, 1) * 100
        elif t == "thousand":
            total += max(current, 1) * 1000
            current = 0
        else:
            return None
    return float(total + current)


def matches(n: Num, candidates: list[float]) -> bool:
    for v in candidates:
        if n.percent:
            if round(v * 100, n.decimals) == round(n.value, n.decimals) or round(v, n.decimals) == n.value:
                return True
        elif n.decimals == 0 and abs(v - round(v)) > 1e-9:
            continue  # a bare integer does not stand for a non-integer value (2.5 is not "2")
        elif round(v, n.decimals) == round(n.value, n.decimals):
            return True
    return False


# ---------------------------------------------------------------- what a reader sees

def visible_markdown(text: str) -> str:
    """Markdown as a reader sees it: mermaid labels and data kept; other code, styling, links dropped."""
    out, fence, kind, front = [], None, "", False
    for line in text.splitlines():
        stripped = line.strip()
        if fence is None:
            if m := re.match(r"(`{3,}|~{3,})\s*(\w*)", stripped):
                fence, kind, front = m.group(1), m.group(2), False
                continue
            out.append(line)
            continue
        if stripped.startswith(fence) and stripped.strip("`~") == "":
            fence = None
            continue
        if kind != "mermaid":
            continue
        if stripped == "---":  # mermaid front matter (config) opens and closes with ---
            front = not front
            continue
        if front or re.match(r"(classDef|class|style|linkStyle|%%)\b", stripped):
            continue
        out.append(line)
    text = "\n".join(out)
    text = re.sub(r"`[^`\n]*`", " ", text)
    text = re.sub(r"\]\([^)]*\)", "]", text)
    text = re.sub(r"<!--.*?-->", " ", text, flags=re.S)
    text = re.sub(r"^\s*(?:\d+\.|[-*>])\s+", " ", text, flags=re.M)
    return text


def visible_html(text: str) -> str:
    text = re.sub(r"<(script|style)\b.*?</\1>", " ", text, flags=re.S | re.I)
    text = re.sub(r"<!--.*?-->", " ", text, flags=re.S)
    text = re.sub(r"<head\b.*?</head>", " ", text, flags=re.S | re.I)
    text = re.sub(r"<[^>]+>", " ", text)
    return html.unescape(text)


def scene_strings(source: str) -> list[str]:
    """String constants a viewer sees or hears: skips docstrings, lexicon, and file paths."""
    tree = ast.parse(source)
    skip: set[int] = set()
    for node in ast.walk(tree):
        if isinstance(node, (ast.Module, ast.ClassDef, ast.FunctionDef)) and node.body:
            first = node.body[0]
            if isinstance(first, ast.Expr) and isinstance(first.value, ast.Constant):
                skip.add(id(first.value))
        if isinstance(node, ast.Assign) and any(isinstance(t, ast.Name) and t.id == "lexicon" for t in node.targets):
            skip.update(id(n) for n in ast.walk(node.value))
        if isinstance(node, ast.Call) and getattr(node.func, "id", getattr(node.func, "attr", "")) in (
                "load_model", "Path", "open"):
            skip.update(id(n) for n in ast.walk(node))
    return [n.value for n in ast.walk(tree)
            if isinstance(n, ast.Constant) and isinstance(n.value, str) and id(n) not in skip]


def rendering_text(kind: str, path: Path) -> tuple[str, bool]:
    """(visible text, words-count-as-numbers) for one rendering file."""
    raw = path.read_text()
    if kind in ("prose", "diagram"):
        return visible_markdown(raw), False
    if kind == "html":
        return visible_html(raw), False
    return "\n".join(scene_strings(raw)), True  # narration: "sixty-one percent" counts


def loads_model(kind: str, path: Path) -> bool:
    raw = path.read_text()
    if kind == "video":
        return "load_model(" in raw
    if kind == "html":
        return bool(MODEL_BLOCK.search(raw))
    return False


def shows_value(text: str, value, words: bool) -> bool:
    if isinstance(value, str):
        return " ".join(value.split()) in " ".join(text.split())
    nums = extract_numbers(text, words=words)
    return any(matches(n, [float(value)]) for n in nums)


# ---------------------------------------------------------------- check and sync

# ---------------------------------------------------------------- completeness

CLAIM_KINDS = {
    "why": ("statement", "alternative", "counterexample"),   # why this form, and what the simpler form breaks
    "guarantee": ("statement", "example", "counterexample"),  # holds here (numbers); fails when the assumption goes
    "mechanism": ("statement", "example"),                     # a step, with a worked example
    "definition": ("statement",),
    "limit": ("statement",),
    "misconception": ("statement", "correction"),
}
FUNCTION_WORDS = ["exp", "log", "ln", "sqrt", "√", "sigmoid", "tanh", "softmax", "argmax", "relu"]


def claim_marked(kind: str, text: str, claim_id: str) -> bool:
    cid = re.escape(claim_id)
    if kind in ("prose", "diagram"):
        return bool(re.search(rf"<!--\s*claim:\s*{cid}\s*-->", text))
    if kind == "html":
        return bool(re.search(rf'data-claim="{cid}"', text))
    return bool(re.search(rf"""\.claim\(\s*["']{cid}["']""", text))


def all_markers(kind: str, text: str) -> set[str]:
    if kind in ("prose", "diagram"):
        return set(re.findall(r"<!--\s*claim:\s*([\w-]+)\s*-->", text))
    if kind == "html":
        return set(re.findall(r'data-claim="([\w-]+)"', text))
    return set(re.findall(r"""\.claim\(\s*["']([\w-]+)["']""", text))


def functions_used(model_md: str) -> set[str]:
    """Named functions that model.md uses in formulas or prose (exp(…), log₂, √, softmax, …)."""
    found = set()
    for f in FUNCTION_WORDS:
        pattern = re.escape(f) if f == "√" else rf"(?<![\w-]){re.escape(f)}(?=[\s(₂₁₀_^]|$)"
        if re.search(pattern, model_md, re.I | re.M):
            found.add(f.lower())
    return found


def completeness(folder: Path, model: dict, present: dict[str, Path], rep: "Report") -> None:
    claims = model["claims"]
    ids = [c.get("id") for c in claims]
    for c in claims:
        cid, kind = c.get("id"), c.get("kind")
        if not cid or kind not in CLAIM_KINDS:
            rep.problems.append(f"model.yaml: claim {cid!r} needs an id and a kind ({', '.join(CLAIM_KINDS)})")
            continue
        missing = [f for f in CLAIM_KINDS[kind] if not str(c.get(f, "")).strip()]
        if missing:
            rep.problems.append(f"model.yaml: {kind} claim '{cid}' has no {' or '.join(missing)}")
        for r in c.get("in", list(present)):
            path = present.get(r)
            if path is not None and not claim_marked(r, path.read_text(), cid):
                rep.problems.append(f"{path.relative_to(folder)}: does not cover claim '{cid}'")
    for r, path in present.items():
        for marker in all_markers(r, path.read_text()) - set(ids):
            rep.problems.append(f"{path.relative_to(folder)}: marks unknown claim '{marker}'")
    md = folder / "model.md"
    if md.exists():
        justified = {str(a).lower() for c in claims if c.get("kind") == "why"
                     for a in ([c.get("about")] if isinstance(c.get("about"), str) else c.get("about") or [])}
        accepted = {str(k).lower() for k in model["accept_unjustified"]}
        for f in sorted(functions_used(md.read_text()) - justified - accepted):
            rep.problems.append(f"model.md uses {f} but no `why` claim says why (add one, or accept_unjustified "
                                f"with a reason)")
    for f, reason in model["accept_unjustified"].items():
        rep.notes.append(f"accepted without a why: {f} ({reason})")


def avoided_phrases(text: str, avoid: list[str]) -> list[str]:
    """The `avoid` phrases that occur in text, as whole words, ignoring case and line breaks."""
    flat = " ".join(text.split())
    return [a for a in avoid if re.search(rf"(?<!\w){re.escape(' '.join(str(a).split()))}(?!\w)", flat, re.I)]


def terminology(folder: Path, model: dict, present: dict[str, Path], rep: "Report") -> None:
    for t in model["terms"]:
        term, avoid = t.get("term"), t.get("avoid") or []
        if not term:
            rep.problems.append(f"model.yaml: terms entry {t!r} needs a term")
            continue
        for kind, path in present.items():
            text, _ = rendering_text(kind, path)
            for phrase in avoided_phrases(text, avoid):
                rep.problems.append(f"{path.relative_to(folder)}: says '{phrase}'; the model's term is "
                                    f"'{term}' (terms in model.yaml)")


ON_SCREEN_CALLS = {"MathTex", "Tex", "label", "Text", "MarkupText"}
TEX_COMMAND = re.compile(r"\\[A-Za-z]+")
SYMBOL = re.compile(r"(?<![A-Za-z])[A-Za-z](?![A-Za-z])")
SPOKEN_SYMBOL = re.compile(r"\b(?:the\s+)?([a-zA-Z])-th\b")


def scene_symbols(source: str) -> set[str]:
    """Single-letter symbols a viewer meets in a scene: in on-screen math and labels, and as 'the n-th' in speech."""
    found: set[str] = set()
    tree = ast.parse(source)
    specs = {id(n) for f in ast.walk(tree) if isinstance(f, ast.FormattedValue) and f.format_spec
             for n in ast.walk(f.format_spec)}  # f"{x:.2f}": the format code is not on screen
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue
        name = getattr(node.func, "id", getattr(node.func, "attr", ""))
        texts = [n.value for a in node.args for n in ast.walk(a)
                 if isinstance(n, ast.Constant) and isinstance(n.value, str) and id(n) not in specs]
        if name in ON_SCREEN_CALLS:
            for t in texts:
                found.update(SYMBOL.findall(TEX_COMMAND.sub(" ", t)) if name in ("MathTex", "Tex")
                             or not re.search(r"[a-z]{2}", t) else [])
        if name == "voiceover":
            texts += [n.value for k in node.keywords if k.arg == "text" for n in ast.walk(k.value)
                      if isinstance(n, ast.Constant) and isinstance(n.value, str)]
            for t in texts:
                found.update(SPOKEN_SYMBOL.findall(t))
    return found


def ledger_references(narrative_md: str) -> set[str]:
    """First-column entries of the introduction ledger table in narrative.md."""
    m = re.search(r"^## \d*\.?\s*Introduction ledger\s*$(.*?)(?=^## |\Z)", narrative_md, re.M | re.S)
    if not m:
        return set()
    refs = set()
    for line in m.group(1).splitlines():
        cells = [c.strip() for c in line.strip().strip("|").split("|")] if line.strip().startswith("|") else []
        if cells and cells[0] and not set(cells[0]) <= set("-: ") and cells[0] != "Reference":
            refs.update(r.strip(" `*") for r in re.split(r",|/", cells[0]))
    return refs


def narrative_ledger(folder: Path, present: dict[str, Path], rep: "Report") -> None:
    narrative = folder / "narrative.md"
    if not narrative.exists():
        if present:
            rep.notes.append("no narrative.md: the reader's path is not written down (explainer new adds one)")
        return
    refs = ledger_references(narrative.read_text())
    if "video" in present:
        for sym in sorted(scene_symbols(present["video"].read_text()) - refs):
            rep.problems.append(f"video/scene.py: shows the symbol '{sym}', which the introduction ledger in "
                                f"narrative.md does not introduce")


# Length is a cost too. A default budget asks whether a length was chosen; a declared budget is a commitment.
DEFAULT_BUDGET = {"prose": 600, "diagram": 9, "video": 150}
BUDGET_UNIT = {"prose": "words", "diagram": "nodes", "video": "s"}


def rendering_length(kind: str, folder: Path, path: Path) -> float | None:
    """Words a reader reads (prose), or seconds a viewer watches (video, from the final timeline)."""
    if kind == "prose":
        return len(re.findall(r"[A-Za-z][A-Za-z'’-]*", visible_markdown(path.read_text())))
    if kind == "diagram":   # the first-level view: 5-9 major objects
        from explainer_kit.diagrams import flowchart_nodes, markdown_blocks
        blocks = markdown_blocks(path)
        return len(flowchart_nodes(blocks[0].source)) if blocks else None
    if kind == "video":
        timeline = folder / "video" / "timeline.json"
        if timeline.exists():
            return round(json.loads(timeline.read_text()).get("duration", 0))
    return None


def length_budget(folder: Path, model: dict, present: dict[str, Path], rep: "Report") -> None:
    budget = model["budget"]
    if budget and not str(budget.get("reason", "")).strip():
        rep.problems.append("model.yaml: budget needs a reason (why this explanation needs this length)")
    for kind, default in DEFAULT_BUDGET.items():
        if kind not in present or (size := rendering_length(kind, folder, present[kind])) is None:
            continue
        rel = {"prose": present["prose"].relative_to(folder) if "prose" in present else "", "video": "video",
               "diagram": "diagram.md, first diagram"}[kind]
        unit = BUDGET_UNIT[kind]
        if kind in budget:
            if size > budget[kind]:
                rep.problems.append(f"{rel}: {size:g} {unit}, over its budget of {budget[kind]} {unit} (budget in "
                                    f"model.yaml); cut what this reader does not need")
        elif size > default:
            rep.warnings.append(f"{rel}: {size:g} {unit}, over the default budget of {default} {unit}; cut what "
                                f"this reader does not need, or set budget.{kind} with a reason in model.yaml")


def predict_pauses(folder: Path) -> int:
    timeline = folder / "video" / "timeline.json"
    if not timeline.exists():
        return 0
    try:
        return sum(e.get("kind") == "predict" for e in json.loads(timeline.read_text()).get("events", []))
    except (json.JSONDecodeError, AttributeError):
        return 0


def plain_video_with_pauses(page_source: str, pauses: int) -> bool:
    """True when a page plays a video with predict pauses through a bare <video> element."""
    from explainer_kit.web_toolkit import BLOCKS

    own = BLOCKS["js"][0].sub("", page_source)  # the inlined toolkit documents Explainer.video itself
    return pauses > 0 and "<video" in own and "Explainer.video(" not in own


@dataclass
class Report:
    slug: str
    problems: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    notes: list[str] = field(default_factory=list)

    @property
    def ok(self) -> bool:
        return not self.problems


def check(folder: Path) -> Report:
    rep = Report(folder.name)
    model_file = folder / "model.yaml"
    if not model_file.exists():
        rep.problems.append("missing model.yaml (machine-readable model)")
        return rep
    model = read_model(model_file)
    values = model["values"]
    candidates = numeric_leaves(values) + numeric_keys(values) + [float(a) for a in model["allow"]] + [0.0, 1.0]

    present = {k: folder / f for k, f in RENDERINGS.items() if (folder / f).exists()}
    if not present:
        rep.notes.append("no renderings yet")
    for kind, path in present.items():
        text, words = rendering_text(kind, path)
        rel = path.relative_to(folder)
        for n in extract_numbers(text, str(rel), words=words):
            if not matches(n, candidates):
                rep.problems.append(f"{rel}: '{n.text.strip()}' is not a model value (add it to values or allow)")
        if kind == "html" and (m := MODEL_BLOCK.search(path.read_text())):
            try:
                embedded = json.loads(m.group(2))
            except json.JSONDecodeError:
                embedded = None
            if embedded != json.loads(json.dumps(values)):
                rep.problems.append(f"{rel}: embedded model is out of date — run `explainer sync {folder.name}`")
        if kind == "html":
            from explainer_kit.web_toolkit import toolkit_current
            if not toolkit_current(path.read_text()):
                rep.problems.append(f"{rel}: inlined web toolkit is out of date — run `explainer sync {folder.name}`")

    completeness(folder, model, present, rep)
    if not model["claims"] and present:
        rep.notes.append("no claims: completeness is not checked (principles §10)")
    terminology(folder, model, present, rep)
    length_budget(folder, model, present, rep)
    narrative_ledger(folder, present, rep)
    if "html" in present and plain_video_with_pauses(present["html"].read_text(), n := predict_pauses(folder)):
        rep.problems.append(f"index.html: plays the video with a plain <video>, which skips its {n} predict "
                            f"pause(s); use Explainer.video")

    for req in model["require"]:
        try:
            value = get_path(values, req["path"])
        except (KeyError, IndexError, ValueError):
            rep.problems.append(f"model.yaml: require path '{req['path']}' does not exist in values")
            continue
        leaves = _require_leaves(value)
        for kind in req.get("in", list(RENDERINGS)):
            path = present.get(kind)
            if path is None:
                continue
            if loads_model(kind, path):
                rep.notes.append(f"{path.relative_to(folder)} loads the model: '{req['path']}' consistent by construction")
                continue
            text, words = rendering_text(kind, path)
            if kind == "html":  # values may live in the page's script, e.g. a data table
                text += "\n" + path.read_text()
            # video: only narration and on-screen strings count; scene code numbers (run_time=2.5) do not.
            for label, leaf in leaves:
                if not shows_value(text, leaf, words):
                    rep.problems.append(f"{path.relative_to(folder)}: does not show {req['path']}{label} = {leaf!r}")
    return rep


def _require_leaves(value, prefix=""):
    if isinstance(value, dict):
        return [x for k, v in value.items() for x in _require_leaves(v, f"{prefix}/{k}")]
    if isinstance(value, list):
        return [x for i, v in enumerate(value) for x in _require_leaves(v, f"{prefix}[{i}]")]
    return [(prefix, value)]


def sync(folder: Path) -> list[Path]:
    """Write the model's values into each page's explainer-model block, and inline the web toolkit."""
    from explainer_kit.web_toolkit import inline_toolkit

    values = read_model(folder / "model.yaml")["values"]
    changed = []
    for page in sorted(folder.rglob("*.html")):
        raw = page.read_text()
        new = MODEL_BLOCK.sub(lambda m: m.group(1) + json.dumps(values, ensure_ascii=False) + m.group(3), raw)
        new = inline_toolkit(new)
        if new != raw:
            page.write_text(new)
            changed.append(page)
    return changed
