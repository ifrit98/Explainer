# Rederivation Eval Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add a rederivation stage to the artifact eval, give all 30 subjects a frozen, model-checked target, and report a three-pass dev baseline on the saved v0.8 builds, whatever it shows.

**Architecture:**
- One new module, `explainer_kit/rederive.py`, holds the targets (validation, hashing, checker), the reader, the grader, scoring, the run, the report, and the grading of a human chain.
- `artifact_eval.py` changes only where the reader's file copies are made: that code is extracted into `copy_for_reader` so both stages share it.
- The CLI gains three `eval` suites (`targets`, `rederive`, `human`), and `eval artifact` runs the rederive stage after it grades.
- The stage reads builds from a `--builds` folder and writes only to `--out`. That is how the baseline reuses the v0.8 builds without touching them.
- Work happens on branch `prd-002-rederivation` from `main`.

**Tech Stack:** Python 3 / uv, pytest, PyYAML, the `claude` CLI through `explainer_kit.agent.ask`.

**Spec:** `docs/prds/PRD-002-rederivation-eval.md`

## Global Constraints

- **Measured text does not change:** `git diff --stat main -- plugin/skills explainers` is empty at every commit.
- **The builder never sees a target.** In `artifact_eval.py`, `TASK`, `SKILL_TIER` and `build()` are unchanged: `git diff main -- explainer_kit/artifact_eval.py` touches only `read()` and the new `copy_for_reader`.
- **The v0.8 record stays byte-identical:** `git status --porcelain -- evals/artifact/results/2026-10-04-dev evals/artifact/results/2026-10-04-dev-haiku-reader` is empty at every commit.
- **Targets are frozen at the Task 2 commit.** Afterwards, `rederive` blocks in `evals/artifact/questions.yaml` never change. A test (Task 5) fails if a results folder's snapshot differs from the file.
- **The repo is public.** No committed file holds an absolute path, a username, an email address, a key, or private-project context.
- **The reader prompt and the grader prompt contain the same constant, `OUTSIDE_RULE`:**
  > Background that this reader already has (see the reader above) may be used without a citation. Every fact about the subject must come from a part of the explanation that the reader names.
- **The separation rule, verbatim:** "Condition A beats condition B when A's supported score is higher than B's in all three passes."
- **A pass** is a fresh reader run over every build, then one grading per subject under its own label shuffle (`random.Random(k)` for pass `k`).
- **Tests run offline.** They stub `agent.ask` and `agent.subprocess.run` and never call the `claude` CLI.
- **The baseline uses the `claude` CLI's default model,** so no `--model` and no `--reader-model`.

## Review Focus

1. **A build with no renderings** (a failed build). Expect the reader to be skipped and every step marked missing. The run must not crash, and the report shows it. The test is in Task 3, `test_read_chain_skips_a_build_with_no_renderings`.
2. **A rerun after the targets changed.** Expect the run to refuse, naming the changed subjects, so no folder mixes two target versions. The test is in Task 5, `test_rerun_refuses_changed_targets`.
3. **Absolute paths leaking into saved output** (public repo). Expect the source folder saved relative to `--out`, and no prompt or temp path saved. The test is in Task 5, `test_outputs_hold_no_absolute_paths`.
4. **Grader replies that don't fit:** too few or too many marks, an unknown word, "stated" on a building block, or a missing label. Expect normalisation, not a crash or a skewed score. The test is in Task 4, `test_marks_are_normalised`.
5. **A page whose idea lives in a control.** Expect the grader to see the page's script as well as its visible text, so a reader citing a slider can be checked. The test is in Task 4, `test_grader_text_includes_page_scripts`.

---

### Task 0: Branch

- [ ] **Step 1:** Create the branch. In the PRD, change `Status: draft, 2026-10-19` to `Status: approved, 2026-10-20`; committing it before any run is what pre-registers the separation rule. Commit the spec and the plan.

```bash
git switch -c prd-002-rederivation
git add docs/prds/PRD-002-rederivation-eval.md docs/superpowers/plans/2026-10-20-rederivation-eval.md
git commit -m "PRD-002: a rederivation eval, and its plan"
```

### Task 1: Targets — format, validation, and the checker

**Files:**
- Create: `explainer_kit/rederive.py`
- Modify: `explainer_kit/cli.py`. Add `targets` to the `eval` suite choices; `cmd_eval` dispatches it.
- Create: `tests/test_rederive.py`

**Interfaces:**
- Produces:
  - `checks_file() -> Path`, which returns `project_root()/"evals"/"artifact"/"rederive-checks.json"`.
  - `target_problems(t: dict) -> list[str]`.
  - `target_hash(t: dict) -> str`: the first 12 hex digits of the sha256 of `json.dumps(t, sort_keys=True, ensure_ascii=False)`.
  - `check_prompt(subject: dict, reader: str) -> str`.
  - `check_targets(only: list[str] | None = None, model: str | None = None) -> Path`.
- The target format in `questions.yaml`, under each subject:

  ```yaml
  rederive:
    q: "…"
    steps:
      - {kind: block, text: "…"}
      - {kind: derived, text: "…"}
    result: "…"
  ```

- The checks file maps `{subject_id: {"verdict": "pass"|"fail", "tests": {...}, "reason": str, "hash": str, "attempt": int}}`.

- [ ] **Step 1: Write the failing tests** in `tests/test_rederive.py`.
  - `test_target_problems`:
    - a valid target (3 steps, at least one `derived`, non-empty `q` and `result`) gives `[]`;
    - each of these gives a non-empty list: 2 steps; 7 steps; no `derived` step; kind `"lemma"`; empty `result`; missing `q`.
  - `test_target_hash_is_stable_and_sensitive`: the same dict in a different key order hashes the same, and changing one step's text changes the hash.
  - `test_check_prompt_shows_the_building_blocks`. For the first dev subject, given a target, the prompt contains:
    - every quiz `expect`, the reader line, every step text with its kind, and the result;
    - the phrases `"any valid derivation needs"`, `"would not state"`, and `"no new fact about the subject"`.
  - `test_check_targets_records_and_resumes`. Monkeypatch `rederive.checks_file` to a tmp file and `ae.questions_file` to a tmp YAML with two subjects that have targets, and a stub `agent.ask` that returns:

    ```json
    {"tests": {"correct": true, "blocks": true, "derived_follow": true, "steps": true, "not_stated": true}, "reason": "ok"}
    ```

    for one subject, and `"derived_follow": false` for the other. Assert:
    - verdicts `pass` and `fail` (the verdict is computed in code as all five tests true, never read from the reply);
    - each `hash` equals `target_hash`, and `attempt == 1`;
    - a second call makes **no** `agent.ask` call;
    - after editing the failing target and calling again, that subject has `attempt == 2` and only it was asked.
- [ ] **Step 2: Run them to verify they fail.**
  Run: `uv run pytest tests/test_rederive.py -q`
  Expected: FAIL. The module is not found.
- [ ] **Step 3: Implement the four functions in `explainer_kit/rederive.py`.**
  - Module docstring style matches `artifact_eval.py`.
  - `CHECKER_SYSTEM = "You are a careful scientist and teacher. You check test questions. Reply with JSON only."`
  - The checker prompt asks for five booleans:
    - `correct`: the steps and the result are true;
    - `blocks`: every `block` step is an idea from the subject's question, from the quiz's expected answers, or background this reader already has;
    - `derived_follow`: every `derived` step follows from the steps before it plus background this reader already has, and introduces no new fact about the subject (otherwise only explanations that happen to contain that fact could support it, and length wins);
    - `steps`: there are at least three steps, and each is an idea any valid derivation needs, not one route's bookkeeping;
    - `not_stated`: a good answer to the subject's question would not state the result.

    It also asks for a one-sentence `reason` that names any failing step.
  - `check_targets` walks `ae.load("all", only)[1]`. It skips subjects without `rederive` and subjects whose saved hash matches. It sets `attempt` to the saved attempt plus 1 when the hash changed. It writes the file sorted by id, with a trailing newline.
  - `cmd_eval` with `suite == "targets"` calls `check_targets(args.only, args.model)` and prints a count of pass and fail.
- [ ] **Step 4: Run the tests to verify they pass.**
  Run: `uv run pytest tests/test_rederive.py -q`
  Expected: 4 passed.
- [ ] **Step 5: Commit.**
  `git add explainer_kit/rederive.py explainer_kit/cli.py tests/test_rederive.py && git commit -m "rederive: target format, validation, and the checker"`

### Task 2: Draft, check and freeze all 30 targets

This task is content work plus live checker calls (`claude -p`), about 30–60 calls. Nothing from Tasks 3–5 may exist in the working tree yet. The targets are written before the reader or grader prompts exist, and stay unchanged afterwards.

**Files:**
- Modify: `evals/artifact/questions.yaml`. Add a `rederive` block to every subject, and add a header paragraph explaining the block and that the builder and reader never see the steps or the result.
- Create: `evals/artifact/rederive-checks.json` (generated).
- Modify: `tests/test_rederive.py` (one test).

**How to draft a target.** The worked example below is from outside the 30 subjects and is not added to the file:

```yaml
rederive:
  q: "A code was built for the letter frequencies q of one language and is used for text from another, with frequencies p. How many extra bits per letter does it cost on average, and can that cost ever be negative?"
  steps:
    - {kind: block, text: "In the best code, a symbol of probability p gets a codeword of about -log2 p bits."}
    - {kind: block, text: "Entropy is the average codeword length of the best code: the sum of -p log2 p."}
    - {kind: derived, text: "With q's code, each letter costs -log2 q instead of -log2 p, so the average extra cost is the sum of p log2(p/q)."}
    - {kind: derived, text: "No code beats the one built for the true source, so the extra cost is never negative, and it is zero only when p = q."}
  result: "The sum of p log2(p/q) bits per letter (the KL divergence); never negative, zero only when p = q."
```

- A `block` step restates an idea from the subject's `q`, from a quiz `expect`, or from background at the reader's level. If you cannot point to one, the step is not a block, and the target likely rewards length: redraft it.
- Derived steps follow from the steps before them plus reader-level background, and bring in no new fact about the subject. The result follows from those steps.
- The question names a concrete case, quantity, sign, or limit that is not one of the quiz questions.

- [ ] **Step 1: Write the failing test** `test_every_subject_has_a_checked_target`. For each subject in `ae.load("all")`, with `checks = json.loads(rederive.checks_file().read_text())`:
  - if the subject has a `rederive` block: `target_problems(...) == []`, `checks[id]["verdict"] == "pass"`, and `checks[id]["hash"] == target_hash(...)`;
  - otherwise: `checks[id]["verdict"] == "fail"` and `checks[id]["attempt"] == 3`. This is the "listed as having none" case.
- [ ] **Step 2: Run it to verify it fails.**
  Run: `uv run pytest tests/test_rederive.py::test_every_subject_has_a_checked_target -q`
  Expected: FAIL, because the checks file is missing.
- [ ] **Step 3: Draft the 30 `rederive` blocks** in `questions.yaml`, using the guidance above, and run the checker.
  Run: `uv run explainer eval targets`
  Expected: one verdict per subject in `evals/artifact/rederive-checks.json`.
- [ ] **Step 4: Rewrite failures, at most twice.**
  - For each `fail`, rewrite the target using the checker's `reason`, then rerun the checker. The attempt count reaches 2, then 3.
  - If a subject still fails at attempt 3, delete its `rederive` block and keep its `fail` entry.
  - Ledger each deletion as a ruling.
- [ ] **Step 5: Run the test to verify it passes.**
  Run: `uv run pytest tests/test_rederive.py -q`
  Expected: all pass.
- [ ] **Step 6: Commit. This is the freeze commit.**
  - `git add evals/artifact/questions.yaml evals/artifact/rederive-checks.json tests/test_rederive.py && git commit -m "Freeze the rederivation targets: 30 subjects, model-checked"`
  - Ledger the commit hash as `FREEZE`.

### Task 3: The reader

**Files:**
- Modify: `explainer_kit/artifact_eval.py`. Extract `copy_for_reader(files: list[Path], shown: Path) -> list[Path]` from `read()`. It empties `shown`, then copies each file into it and returns the copies. `read()` calls it, and its behaviour is unchanged.
- Modify: `explainer_kit/rederive.py`
- Modify: `tests/test_rederive.py`

**Interfaces:**
- Consumes: `ae.renderings(ws, sid)` and `ae.copy_for_reader`.
- Produces:
  - `OUTSIDE_RULE: str`, the exact text in Global Constraints;
  - `reader_prompt(files: list[Path], reader: str, question: str) -> str`;
  - `chain_reply(text: str) -> dict`, which returns `{"steps": [{"step": str, "part": str, "idea": str}], "result": str, "gap": str}`;
  - `chain_text(chain: dict) -> str`;
  - `read_chain(subject: dict, cond: str, reader: str, builds: Path, out: Path, k: int, model: str | None) -> dict`, which saves to `out/"rederive"/f"pass-{k}"/"read"/<id>/f"{cond}.json"`.

- [ ] **Step 1: Write the failing tests.**
  - `test_reader_prompt_is_blind_to_steps_and_result`:
    - it contains the target `q`, `OUTSIDE_RULE`, every file path, `"gap"` and `"part"`;
    - it contains no step text and no result text from a real dev target.
  - `test_chain_reply_tolerates_shapes`:
    - valid JSON round-trips;
    - `{"steps": "x"}` gives `steps == []`;
    - `"no json"` gives `{"steps": [], "result": "", "gap": ""}`;
    - step items that are not dicts are dropped.
  - `test_chain_text_numbers_steps`: two steps give lines starting `1.` and `2.`, each with its part and idea, then a `Result:` line.
  - `test_read_chain_uses_copies_and_leaves_builds_untouched`. Use a tmp builds folder with `work/<id>/a/explanation.md` and a stub `agent.ask` that captures `read=` and returns a chain. Assert:
    - every `read` folder lies outside `builds`;
    - the saved file exists at the path above;
    - a second call makes no `agent.ask` call;
    - the sha256 of every file under `builds` is unchanged.
  - `test_read_chain_skips_a_build_with_no_renderings`: there is no `agent.ask` call, and the result has `"missing": True` and `steps == []`.
  - The existing `tests/test_artifact_eval.py` must still pass.
- [ ] **Step 2: Run them to verify they fail.**
  Run: `uv run pytest tests/test_rederive.py -q`
  Expected: the new tests FAIL with `AttributeError`.
- [ ] **Step 3: Implement.**
  - The reader prompt states, in order:
    - the reader line;
    - "Read ONLY these files" and the file list;
    - the `.html` rule from `ae.reader_prompt`;
    - the question;
    - "work it out step by step from the explanation";
    - per step: what it establishes (`step`), the part it rests on (`part`: a heading, paragraph, figure or diagram, a page control, an earlier step number, or `background`), and that part's idea in its own words (`idea`);
    - `OUTSIDE_RULE`;
    - "if the explanation lacks an idea you need, say which in `gap` and stop there";
    - the JSON shape.
  - Reuse `ae.READER_SYSTEM`.
  - Make copies in `tempfile.mkdtemp()` and remove them afterwards.
  - Retry the call once if `steps` comes back empty and `gap` is empty, as `ae.read` does.
- [ ] **Step 4: Run the tests to verify they pass.**
  Run: `uv run pytest tests/test_rederive.py tests/test_artifact_eval.py -q`
  Expected: all pass.
- [ ] **Step 5: Commit.**
  `git add -u && git commit -m "rederive: the reader works the target out and cites the parts it rests on"`

### Task 4: The grader and the scores

**Files:** modify `explainer_kit/rederive.py` and `tests/test_rederive.py`.

**Interfaces:**
- Consumes: `chain_text`, `OUTSIDE_RULE`, `ae.shown_text`, `ae.renderings`, and `ae.GRADER_SYSTEM`.
- Produces:
  - `MARKS = ("supported", "unsupported", "missing", "stated")`;
  - `grader_text(path: Path) -> str`;
  - `grade_prompt(subject: dict, reader: str, entries: dict[str, dict]) -> str`, where `entries` maps a label to `{"text": str, "chain": str}`;
  - `marks(raw: object, kinds: list[str]) -> list[str]`;
  - `tally(marks: list[str], kinds: list[str], right: bool, stated: bool) -> dict[str, int]`, with keys `supported, made, counted, stated, right, results, results_stated`;
  - `pass_scores(tallies: dict[str, list[dict]]) -> dict[str, dict]`. It maps a condition to `{"supported": float, "raw": float, "result": float | None}`, pooled over subjects;
  - `separations(passes: list[dict[str, dict]]) -> list[tuple[str, str]]`;
  - `grade_subject(subject: dict, key: dict[str, str], reader: str, builds: Path, out: Path, k: int, model: str | None) -> dict`. It saves `out/"rederive"/f"pass-{k}"/"grades"/f"{id}.json"` as `{"key": key, "grades": {cond: {"marks": [...], "result_right": bool, "result_stated": bool}}}`.

- [ ] **Step 1: Write the failing tests.**
  - `test_grader_text_includes_page_scripts`. `<p>Drag the slider</p><script>const loss = x => x * x</script>` gives text containing both `"Drag the slider"` and `"const loss"`. A `.md` file gives the same as `ae.shown_text`.
  - `test_grade_prompt_is_blind_and_carries_the_rule`. The prompt contains:
    - `OUTSIDE_RULE`;
    - each expected step with its kind;
    - the result;
    - `"=== Explanation A ==="` and the chain text;
    - the words `"any order"` and `"stated"`.

    It does not contain `"principles"` or `"skill"`, in any case.
  - `test_marks_are_normalised`:
    - `marks(["supported", "stated", "bogus"], ["block", "block", "derived", "derived"]) == ["supported", "supported", "missing", "missing"]`;
    - `marks("x", ["block"]) == ["missing"]`;
    - extra marks are dropped.
  - `test_tally`:
    - `tally(["supported", "unsupported", "stated", "missing"], ["block", "derived", "derived", "derived"], True, False)` gives `{"supported": 1, "made": 2, "counted": 3, "stated": 1, "right": 1, "results": 1, "results_stated": 0}`;
    - with `stated=True`, it gives `right == 0`, `results == 0` and `results_stated == 1`.
  - `test_pass_scores_pool_subjects`. For condition `a`, tallies `{"supported": 1, "made": 2, "counted": 2, …, "right": 1, "results": 1}` and `{"supported": 2, "made": 2, "counted": 3, …, "right": 0, "results": 1}` give supported `0.6`, raw `0.8` and result `0.5`. A condition with `results == 0` everywhere gives `result is None`.
  - `test_separations_need_every_pass`.

    ```python
    separations([
        {"a": {"supported": .7}, "b": {"supported": .5}, "c": {"supported": .6}},
        {"a": {"supported": .7}, "b": {"supported": .5}, "c": {"supported": .4}},
        {"a": {"supported": .6}, "b": {"supported": .6}, "c": {"supported": .3}},
    ]) == [("a", "c")]
    ```
  - `test_grade_subject_maps_labels_back_and_fills_missing`. Use a stub grader reply that grades label `A` only:
    - the saved grades are keyed by condition;
    - the condition whose label is missing gets all `missing` marks and `result_right: False`;
    - a rerun makes no call.
- [ ] **Step 2: Run them to verify they fail.**
  Run: `uv run pytest tests/test_rederive.py -q`
  Expected: the new tests FAIL.
- [ ] **Step 3: Implement.**
  - `grader_text`: for `.html`, `ae.shown_text(path)` plus the text of each `<script>…</script>` under a `--- page script ---` line; otherwise `ae.shown_text(path)`. Each explanation is truncated at `ae.TEXT_LIMIT`.
  - The grader prompt states:
    - the subject `q`, the reader, and the target `q`;
    - the expected steps, numbered, with kind, and the expected result;
    - `OUTSIDE_RULE`;
    - "the expected steps are a checklist of ideas: credit a step when the chain establishes the same idea in any order, merged, split, or by an equivalent route";
    - the four marks as the PRD defines them, adding that `stated` applies to derived steps only and that building blocks are meant to be in the explanation;
    - `result_right`, and `result_stated` (the explanation states the result outright);
    - the reply shape `{"grades": {"<label>": {"marks": [...], "result_right": bool, "result_stated": bool}}}`.
  - A missing build's entry text is `"(no explanation)"`, and its chain is `"(no chain)"`.
- [ ] **Step 4: Run the tests to verify they pass.**
  Run: `uv run pytest tests/test_rederive.py -q`
  Expected: all pass.
- [ ] **Step 5: Commit.**
  `git add -u && git commit -m "rederive: blind grading of each chain, scores, and the separation rule"`

### Task 5: The run, the report, and the CLI

**Files:** modify `explainer_kit/rederive.py`, `explainer_kit/cli.py` and `tests/test_rederive.py`.

**Interfaces:**
- Consumes: everything above, plus `ae.load`, `ae.visible`, `evals.words`, and `ae.RENDERINGS`.
- Produces: `run(out: Path, builds: Path, split: str = "dev", only: list[str] | None = None, model: str | None = None, reader_model: str | None = None, workers: int = 4, passes: int = 3) -> Path`. It returns `out/"rederive.md"` and also writes the following.
  - `out/"rederive-scores.json"`:
    - `{"passes": [pass_scores…], "tallies": {...}, "separations": [[a, b], …]}`.
  - `out/"rederive"/"targets.json"`:
    - `{id: target}` for the subjects run;
    - if it already exists and differs from the current targets, `SystemExit("targets changed since this run: <ids>")`.
  - `out/"rederive"/"source.json"`:
    - `{"builds": os.path.relpath(builds, out)}`.
  - The conditions are the keys of `builds/"conditions.json"`, in file order.
  - Only subjects with a `rederive` block run.

- [ ] **Step 1: Write the failing tests.** They use one fixture: a tmp `questions.yaml` with one subject and target, monkeypatched in through `ae.questions_file`. The builds folder holds `conditions.json` `{"a": "none", "b": "quick"}`, explanations containing `ALPHA` and `BETA`, and a `scores.json` like `fake_run_folder`'s. The stub `agent.ask` returns a chain for reader calls. For grader calls, it finds which label's block contains `ALPHA`, marks every step `supported` for it and `missing` for the other, and counts its calls.
  - `test_run_end_to_end`. There are 3 × 2 reader calls plus 3 grader calls. The report contains:
    - the table header `| condition | supported | raw | result right | stated steps | stated results | words | quiz (grounded) |`;
    - a row starting `| a | 100%, 100%, 100% | 100%, 100%, 100% |`;
    - the line `Separation (higher supported score in all three passes): a > b.`
  - `test_rerun_makes_no_calls`: a second `run` makes zero calls and gives an identical report.
  - `test_rerun_refuses_changed_targets`: edit the target's result, then `pytest.raises(SystemExit, match="targets changed")`.
  - `test_outputs_hold_no_absolute_paths`: no file under `out` contains `str(tmp_path)`, and `source.json` gives a relative path.
  - `test_builds_folder_is_untouched`: the sha256 of every file under `builds` is the same before and after `run`.
  - `test_frozen_targets_match_every_results_folder`. For every `evals/artifact/results/*/rederive/targets.json` in the repo, each entry equals the current target in `questions.yaml`. This passes vacuously until Task 6.
  - `test_cli_rederive_and_artifact_call_the_stage`. Monkeypatch `sys.argv` and the stage functions:
    - `explainer eval rederive --builds B --out O` calls `rederive.run(O, B, …)`;
    - `explainer eval artifact --out O` calls `artifact_eval.run`, then `rederive.run(O, O, …)`.
- [ ] **Step 2: Run them to verify they fail.**
  Run: `uv run pytest tests/test_rederive.py -q`
  Expected: the new tests FAIL.
- [ ] **Step 3: Implement `run` and its report.**
  - Read all passes in parallel (`ThreadPoolExecutor(workers)`), then grade.
  - Pass `k`'s label key per subject is built like `ae.run`'s, with `random.Random(k)`.
  - The report:
    - title `# Rederivation, <date> (<split>, <n> subjects)`;
    - one line on the builds folder (as saved in `source.json`) and the models;
    - the condition table, where every score cell lists the passes as `x%, y%, z%`. Words are the mean visible words per explanation. The quiz cell is that condition's grounded share from `builds/"scores.json"`, or `–` if the file is missing;
    - the separation line, or `Separation (…): none.`;
    - a table per subject whose cells are `supported/counted` per pass;
    - a short key explaining each column, in `ae.summary`'s style.
- [ ] **Step 4: Wire the CLI.**
  - Add `--builds` to the `eval` parser.
  - The `rederive` suite's default `--out` is `evals/artifact/results/<date>-<split>-rederive`.
  - `artifact` calls `rederive.run(out, out, …)` after `artifact_eval.run`.
- [ ] **Step 5: Run the tests to verify they pass.**
  Run: `uv run pytest -q`
  Expected: all pass, about 255 tests.
- [ ] **Step 6: Commit.**
  `git add -u && git commit -m "rederive: three-pass run, report, and the eval rederive command; eval artifact runs it"`

### Task 6: The dev baseline (live)

This step makes about 120 reader calls and 30 grader calls through the `claude` CLI, with no builds.

**Files:** create `evals/artifact/results/<YYYY-MM-DD>-dev-rederive/`, which is generated.

- [ ] **Step 0: Run a smoke test first.** Saved outputs are never redone, so a malformed reply saved in the real folder would stay there.
  Run: `uv run explainer eval rederive --builds evals/artifact/results/2026-10-04-dev --only bloom-filter --out <scratchpad>/smoke`
  Expected:
  - one `read/*.json` with a non-empty `steps` list of `{step, part, idea}`;
  - one `grades/*.json` with 4 conditions, each with one mark per expected step;
  - a report with 4 rows.

  Fix only mechanics (parsing, paths), never scoring or targets, and ledger any fix as a ruling. Delete the scratch folder.
- [ ] **Step 1: Run the baseline.**
  Run: `uv run explainer eval rederive --builds evals/artifact/results/2026-10-04-dev --out evals/artifact/results/$(date +%F)-dev-rederive`
  Expected:
  - `rederive.md` and `rederive-scores.json` exist;
  - three `pass-*` folders, each holding 40 reads and 10 grades;
  - the report table has 4 rows.
- [ ] **Step 2: Verify that the record and the targets are intact, and that the output is clean.**
  - `git status --porcelain -- evals/artifact/results/2026-10-04-dev evals/artifact/results/2026-10-04-dev-haiku-reader` prints nothing.
  - `git diff FREEZE -- evals/artifact/questions.yaml` prints nothing.
  - `grep -rlE '/Users/|/home/|@[a-z0-9-]+\.[a-z]|sk-[A-Za-z0-9]' evals/artifact/results/*-dev-rederive` prints nothing.
  - `uv run pytest -q` passes, including `test_frozen_targets_match_every_results_folder`, which is now non-vacuous.
- [ ] **Step 3: Commit.**
  `git add evals/artifact/results && git commit -m "Rederivation dev baseline on the v0.8 builds: three passes"`

### Task 7: The human check

**Files:**
- Create: `evals/artifact/human-check.md`
- Modify: `explainer_kit/rederive.py` and `explainer_kit/cli.py`. Add the `human` suite and `--chain`.
- Modify: `tests/test_rederive.py`

**Interfaces:**
- Consumes: `grade_prompt`, `grader_text`, `marks`, and `tally`.
- Produces: `grade_human(chain_file: Path, builds: Path, model: str | None = None) -> dict`.
  - The chain file is Markdown with front matter `subject: <id>` and `condition: <name>`. Its body is the person's working.
  - The function grades the body as the chain under the single label `A`.
  - It saves `{"subject", "condition", "marks", "result_right", "result_stated", "tally"}` to `chain_file.with_suffix(".grade.json")` and returns it.

- [ ] **Step 1: Write the failing tests.**
  - `test_grade_human_uses_the_same_rubric`. With a stub `agent.ask`:
    - the prompt it receives contains `OUTSIDE_RULE` and the person's body text;
    - the saved JSON has a tally computed by `tally`.
  - `test_human_check_lists_only_questions`. For every dev subject that has a target, `human-check.md` contains its `q`, and none of its step texts or its result.
- [ ] **Step 2: Run them to verify they fail.**
  Run: `uv run pytest tests/test_rederive.py -q`
  Expected: FAIL.
- [ ] **Step 3: Implement `grade_human`, wire `explainer eval human --builds B --chain F`, and write `human-check.md`.** The brief is one page:
  - **Who:** a technical reader who is new to the subject.
  - **What to do:**
    1. Pick a dev subject.
    2. Read the explanation the owner sends (one condition's `explanation.md` or page from the baseline builds) once.
    3. Without looking anything up, work out that subject's question, listed below, on paper. Note which part of the explanation each step rests on.
  - **How to send it back:** as `evals/artifact/human/<id>-<condition>.md` with the front matter above, with no name or personal details.
  - **How it's graded:** `uv run explainer eval human --builds evals/artifact/results/2026-10-04-dev --chain <file>`. `docs/evals.md` records whether the person's marks agree with the model reader's on the same explanation.
  - **The 10 dev questions,** questions only.
- [ ] **Step 4: Run the tests to verify they pass.**
  Run: `uv run pytest -q`
  Expected: all pass.
- [ ] **Step 5: Commit.**
  `git add -A evals/artifact/human-check.md && git add -u && git commit -m "rederive: a human check graded with the same rubric"`

### Task 8: Write it up

**Files:**
- Modify: `docs/evals.md`, `docs/cli.md`, `ROADMAP.md` (§15), `CHANGELOG.md`, `CLAUDE.md` and `AGENTS.md` (command lists).

- [ ] **Step 1: Add a "Rederivation" section to `docs/evals.md`,** after "What the artifact eval found". It covers:
  - **What it measures and why the quiz couldn't.** Give the entropy → KL example in two sentences.
  - **The target format and the three tests,** plus the checker. Give the counts that passed and the subjects with no target.
  - **Reader, grader, `OUTSIDE_RULE`, the four marks, the "stated" exclusion, and a pass.**
  - **What the dev baseline found.**
    - Show the condition table from `rederive.md`, with a link to the report.
    - State the separation rule verbatim, then say which pairs separate.
    - Say whether the supported order follows the word counts (none 1,689; principles 1,006; published 1,016; quick 606).
    - If no pair separates, say that the eval does not yet rank the conditions, and that PRD-003 should not adopt it as its measure without changes.
    - Use plain statements and no softening, in the style of the v0.8 section.
  - **Human check:** pending, with a link to `evals/artifact/human-check.md`.
- [ ] **Step 2: Update the other docs.**
  - **`docs/cli.md`:** add rows for `eval targets`, `eval rederive --builds`, and `eval human --builds --chain`, and note that `eval artifact` now runs the stage.
  - **ROADMAP §15:**
    - add a **Built** bullet for the stage;
    - add an **Evidence** bullet giving the baseline result in one sentence;
    - under **Next**, record whether PRD-003 adopts it.
  - **`CHANGELOG.md`:** add a `## Unreleased` section above 0.8.0, with bullets in the 0.8.0 style.
  - **`CLAUDE.md` and `AGENTS.md`:** add one line, `uv run explainer eval rederive --builds <run>`.
- [ ] **Step 3: Verify.**
  - `uv run pytest -q` passes. This includes the link and AGENTS tests.
  - `uv run explainer check` passes.
  - `git diff --stat main -- plugin/skills explainers` is empty.
- [ ] **Step 4: Commit.**
  `git add -u && git commit -m "Docs: the rederivation eval and what its dev baseline found"`

### After the last task

Run the final whole-branch review per the execution skill, then stop. Pushing, merging, and whether this ships as v0.9.0 or waits for PRD-003 are the owner's calls.
