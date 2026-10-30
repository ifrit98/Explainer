# Rederivation Controls Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Find out whether the rederivation test notices a missing building block. Cut one block from six saved v0.8 `principles` explanations, run the unchanged PRD-002 stage on them, and report a verdict under a bar fixed in advance.

**Architecture:** A new module, `explainer_kit/controls.py`, works in two stages and uses `rederive.py` as an unchanged library.
- `eval cuts` makes the cut copies, checks them, and writes a builds folder laid out like an artifact run.
- `eval controls` copies in the baseline's reader chains for the three uncut conditions, then calls `rederive.run` on that folder. After the run it checks for leaks, computes the verdict, and writes `controls.md` and `controls.json`.

**Tech Stack:** Python 3.12 via uv, pytest (offline, `agent.ask` stubbed), PyYAML, difflib, the `claude` CLI through `explainer_kit.agent`.

**Spec:** `docs/prds/PRD-002a-rederivation-controls.md` (approved 2026-10-29). Built on PRD-002 (`docs/prds/PRD-002-rederivation-eval.md`) and `explainer_kit/rederive.py`.

## Global Constraints

- The repo is public (MIT). No personal or private-project context, and no absolute paths in any committed output.
- `evals/artifact/results/2026-10-04-dev/`, `2026-10-04-dev-haiku-reader/` and `2026-10-20-dev-rederive/` stay byte-identical: `git diff --exit-code` on them is clean.
- The targets stay frozen. `test_targets_are_the_frozen_ones` and `test_frozen_targets_match_every_results_folder` pass unchanged.
- No code change to the test: `explainer_kit/rederive.py` is not modified, and neither are its prompts, `OUTSIDE_RULE`, `marks`, or `tally`.
- Neither the reader nor the grader is told that any build was cut. The cut copy is a plain `explanation.md`: no marker, and no note in any file the reader is shown.
- In the controls folder the cut copy's condition is named `principles-cut`, in the `principles` slot of `conditions.json`, so no report there shows a cut copy as `principles`. The name only reaches paths and result keys: `read_chain` copies files to a temp `explanation/` folder, and the grader sees only labels.
- Every stage saves its output, and a rerun skips what exists.
- Tests run offline, without the `claude` CLI.
- The reader, grader, cutter, and checkers use the `claude` CLI's default model. Three passes.
- The bar: caught means raw `unsupported` or `missing` in all three passes. Trusted means caught in ≥ ceil(0.8 × counted), at most 1 clean-set block lost, and at least 5 subjects counted.
- Commits end with the attribution lines from the session's system reminder.

## Review Focus

1. **A grader reply with no raw mark for the cut block** (`raw` is None, or the list is short) counts as not caught, never as a catch. Test: `test_absent_raw_mark_is_not_a_catch` (Task 3).
2. **A cut copy that changed after its check,** by hand or by a rerun, makes `eval controls` refuse to run. Test: `test_run_refuses_a_changed_cut_copy` (Task 4).
3. **A cut copy that shows where text was removed** (a marker, or a reference to a passage that is gone) fails its check and is redone. Test: `test_a_marked_copy_fails_its_check` (Task 2).
4. **A rerun after a crash** makes no repeat calls for saved reads, grades, or leak checks. Test: `test_controls_rerun_makes_no_calls` (Task 4).
5. **Absolute paths** (temp folders, the home folder) never appear in records, diffs, or reports. Test: `test_cut_outputs_hold_no_absolute_paths` (Task 2), and the same assertion in `test_controls_end_to_end` (Task 4).

---

### Task 1: The cut list and the bar as data

**Files:**
- Create: `evals/artifact/controls.yaml`
- Create: `explainer_kit/controls.py` (module docstring, `controls_file`, `load_controls`)
- Test: `tests/test_controls.py`

**Interfaces:**
- Produces: `controls_file() -> Path`, which is `project_root()/"evals"/"artifact"/"controls.yaml"`.
- Produces: `load_controls() -> dict` with these keys:
  - `source: Path` and `baseline: Path`, resolved against `project_root()`;
  - `condition: str`;
  - `cuts: dict[str, {"cut": int, "clean": list[int]}]`, with 1-based step numbers;
  - `left_out: dict[str, str]`;
  - `bar: {"catch": float, "min_counted": int, "clean_losses": int}`.

- [ ] **Step 1: Write `evals/artifact/controls.yaml`**, with a header comment naming PRD-002a and saying the file is frozen with the cut copies. Exact values:

```yaml
source: evals/artifact/results/2026-10-04-dev
baseline: evals/artifact/results/2026-10-20-dev-rederive
condition: principles
cuts:
  bloom-filter: {cut: 1, clean: []}
  float-sum: {cut: 1, clean: []}
  greenhouse: {cut: 1, clean: []}
  heat-pump: {cut: 2, clean: [1]}
  key-exchange: {cut: 3, clean: [1, 2]}
  two-tides: {cut: 2, clean: [1]}
left_out:            # the reasons, word for word from the PRD's "left out" table
  antibiotic-resistance: "..."
  gps-relativity: "..."
  quorum: "..."
  vaccine-memory: "..."
bar: {catch: 0.8, min_counted: 5, clean_losses: 1}
```

- [ ] **Step 2: Write the failing tests**

```python
def test_controls_follow_the_eligibility_rule():
    c = controls.load_controls()
    dev = {s["id"]: s for s in ae.load("dev")[1] if "rederive" in s}
    assert sorted(c["cuts"]) == ["bloom-filter", "float-sum", "greenhouse", "heat-pump", "key-exchange", "two-tides"]
    assert set(c["cuts"]) | set(c["left_out"]) == set(dev)
    assert not set(c["cuts"]) & set(c["left_out"])
    for sid, spec in c["cuts"].items():
        kinds = [s["kind"] for s in dev[sid]["rederive"]["steps"]]
        assert spec["cut"] not in spec["clean"]
        for i in [spec["cut"], *spec["clean"]]:
            assert kinds[i - 1] == "block"
            for k in (1, 2, 3):   # reliably credited when intact (rule 4)
                g = json.loads((c["baseline"] / "rederive" / f"pass-{k}" / "grades" / f"{sid}.json").read_text())
                assert g["grades"]["principles"]["marks"][i - 1] == "supported", (sid, i, k)
    assert sum(len(s["clean"]) for s in c["cuts"].values()) == 4

def test_the_bar_is_the_prds():
    assert controls.load_controls()["bar"] == {"catch": 0.8, "min_counted": 5, "clean_losses": 1}
```

- [ ] **Step 3: Run them.** `uv run pytest tests/test_controls.py -q`. Expected: FAIL, `controls` does not exist.
- [ ] **Step 4: Implement `controls_file` and `load_controls`** in `explainer_kit/controls.py`. The module docstring follows `rederive.py`'s style: what the controls answer, and the two stages.
- [ ] **Step 5: Run them.** Expected: 2 passed.
- [ ] **Step 6: Commit** `evals/artifact/controls.yaml explainer_kit/controls.py tests/test_controls.py` with the message "controls: the PRD-002a cut list and bar, as data".

### Task 2: Cutting and checking (`eval cuts`)

**Files:**
- Modify: `explainer_kit/controls.py`
- Test: `tests/test_controls.py`

**Interfaces:**
- Consumes: `load_controls()` (Task 1). From PRD-002, unchanged:
  - `ae.load`, `ae.renderings`;
  - `agent.ask(system, prompt, model=None)` and `agent.parse_json`.
- Produces:
  - `MAX_ATTEMPTS = 3`, and `CUT = "principles-cut"` (the condition name in the controls folder).
  - `CUTTER_SYSTEM` and `CHECKER_SYSTEM` strings.
  - `apply_edits(text: str, edits: list[dict]) -> str`. Raises `ValueError` when `edits` is empty, or when an `old` is not found exactly once. Applies the edits in order, then collapses 3+ newlines to 2.
  - `cut_prompt(subject: dict, reader: str, spec: dict, text: str) -> str`.
  - `cut_check_prompt(subject: dict, reader: str, spec: dict, text: str) -> str`.
  - `cut_passes(reply: dict, spec: dict) -> bool`. True only when all hold:
    - `reply["recoverable"] is False`;
    - `reply["marked"] is False`;
    - `reply["present"][str(i)] is True` for every clean `i`.
  - `make_cuts(out: Path, only: list[str] | None = None, redo: bool = False, model: str | None = None) -> dict[str, dict]`.
- Writes:
  - `out/cuts/<id>.json`, the record:

    ```
    {"subject", "cut", "clean", "verdict": "pass"|"pending"|"fail",
     "attempts": [{"edits", "error", "check", "passed"}],
     "hash": sha256 of the cut copy, first 16 hex}
    ```

  - `out/cuts/<id>.diff`, a unified diff labelled `principles/explanation.md` and `principles/explanation.md (cut)`;
  - `out/work/<id>/<cond>/…`, with the cut copy under `out/work/<id>/principles-cut/`;
  - `out/conditions.json`: `{"none": "none", "principles-cut": "principles, one block cut (PRD-002a)", "quick": "quick", "published": "published"}`, in that order.

**Prompt content (wording left to the implementer):**
- **The cutter** sees the reader line, the target question, the block to cut (its text), the clean blocks (their text, "keep these"), and the explanation. It is told to:
  - remove every sentence that states the block or lets this reader recover it, including a stated conclusion that gives it away;
  - keep everything else word for word, rewording only where a removal breaks a sentence;
  - never mark or mention a removal.

  It replies `{"edits": [{"old": "<exact text>", "new": "<replacement, may be empty>"}]}`.
- **The checker** sees the reader line, the target question, every block numbered, which one was cut and which must stay, and the cut copy. It replies:

  ```
  {"recoverable": bool, "quote": "", "present": {"<i>": bool},
   "marked": bool, "reason": ""}
  ```

  - `recoverable`: could this reader get the cut block from the copy, the question, or their background?
  - `marked`: does the copy show that text was removed?

**Behaviour of `make_cuts`:**
- It runs over the subjects in `cuts` (filtered by `only`). For each one:
  - copy the files `ae.renderings` returns for `none`, `quick`, and `published` into `out/work/<id>/<cond>/`, keeping their paths relative to the source condition folder;
  - require exactly one `principles` rendering, and raise `SystemExit` otherwise;
  - try at most `MAX_ATTEMPTS` attempts in total, counting earlier ones;
  - a cutter reply whose edits don't apply (`apply_edits` raises) is asked once more within the same attempt, as `grade_subject` does for a reply that doesn't fit. No cut was made, so it is not a redo. The attempt fails, with its `error` recorded, only if the second reply doesn't apply either.
- **The record is saved after every attempt.** It holds `verdict: pending` while attempts remain without a pass, so a crashed run resumes.
- **On a pass:** write the cut copy at the source's relative path, the diff, and `verdict: pass` with its hash, then stop.
- **After the last failed attempt:** `verdict: fail`, and remove any cut copy for that subject.
- **On a rerun:** continue `pending` subjects. Skip a subject whose record has `verdict: pass` or has no attempts left. With `redo=True` and attempts left, make a new attempt even after a pass.
- The source folder is only read.

- [ ] **Step 1: Write the failing tests.** Use a `subjects_file`-style fixture with two subjects and a source run folder with all four conditions, in the shape of `builds_folder` in `tests/test_rederive.py`. Stub `agent.ask` and route on `system`.

```python
def test_apply_edits_needs_each_old_exactly_once():
    assert controls.apply_edits("a b c\n\n\n\nd", [{"old": "b ", "new": ""}]) == "a c\n\nd"
    for bad in ([], [{"old": "x", "new": ""}], [{"old": "a", "new": ""}]):   # empty, absent, and (on "a a") twice
        with pytest.raises(ValueError):
            controls.apply_edits("a a b", bad)

def test_cut_prompt_names_the_block_and_what_stays(): ...   # cut block text, clean block texts, reader, question,
                                                           # "word for word" in prompt; target result not in prompt
def test_make_cuts_writes_copy_diff_and_record(monkeypatch, tmp_path): ...
    # copy (under principles-cut/) == apply_edits(original, edits); diff file names no tmp path; record verdict "pass",
    # 1 attempt, hash matches copy; none/quick/published renderings byte-identical to source; conditions.json as above;
    # source tree hash unchanged
def test_a_failed_check_is_redone_then_dropped(monkeypatch, tmp_path): ...
    # checker says recoverable three times -> 3 attempts, verdict "fail", no principles copy in out/work
def test_edits_that_do_not_apply_are_asked_again_within_the_attempt(monkeypatch, tmp_path): ...
    # first cutter reply's old text absent, second applies -> 1 attempt, 2 cutter calls, verdict "pass";
    # both replies bad -> the attempt fails with its error recorded, and attempt 2 is made
def test_a_marked_copy_fails_its_check(monkeypatch, tmp_path): ...     # marked=True -> attempt 2 is made
def test_a_missing_clean_block_fails_its_check(monkeypatch, tmp_path): ...  # present={"1": False} -> attempt 2
def test_rerun_skips_passing_cuts_and_redo_makes_one_more(monkeypatch, tmp_path): ...
    # second make_cuts: no calls; make_cuts(redo=True, only=[sid]): exactly one cutter call and one checker call,
    # attempts == 2; after attempts reach 3, redo makes no call
def test_cut_outputs_hold_no_absolute_paths(monkeypatch, tmp_path): ...
    # str(tmp_path) and str(Path.home()) appear in no file under out/cuts
```

- [ ] **Step 2: Run them.** `uv run pytest tests/test_controls.py -q`. Expected: FAIL, the names are not defined.
- [ ] **Step 3: Implement** the Produces list above. Use `difflib.unified_diff` for the diff and `hashlib.sha256` for the hash.
- [ ] **Step 4: Run them.** Expected: all of `tests/test_controls.py` passes. Then `uv run pytest -q`: the whole suite passes.
- [ ] **Step 5: Commit** with the message "controls: cut a block, check the cut, keep the diff".

### Task 3: The verdict

**Files:**
- Modify: `explainer_kit/controls.py`
- Test: `tests/test_controls.py`

**Interfaces:**
- Produces:
  - `caught(raws: list[object], i: int) -> bool`. True only when every pass's raw list has a mark at index `i - 1` and, stripped and lower-cased, it is `unsupported` or `missing`.
  - `kept(raws: list[object], i: int) -> bool`. True only when every pass's raw mark at `i - 1` is `supported`.
  - `verdict(caught_by: dict[str, bool], lost_by: dict[str, int], dropped: list[str], leaked: list[str], bar: dict) -> dict`. It returns:

    ```
    {"verdict", "without_leak_exclusions", "counted": [...], "caught": int,
     "need": int, "clean_losses": int}
    ```

**The algorithm:**

```
def judge(counted):
    need = ceil(bar["catch"] * len(counted))
    n_caught = sum(caught_by[s] for s in counted)
    losses = sum(lost_by.get(s, 0) for s in counted)   # clean blocks of uncounted subjects are ignored
    if len(counted) < bar["min_counted"]: return "inconclusive"
    if n_caught < need: return "blind"
    if losses > bar["clean_losses"]: return "inconclusive"
    return "trusted"
```

- `counted` is the subjects in `caught_by` minus `dropped` and `leaked`.
- `without_leak_exclusions = judge(counted + leaked)`.
- `verdict` is `judge(counted)`, except that it becomes `"inconclusive"` when it is `"trusted"` and `without_leak_exclusions == "blind"`.

- [ ] **Step 1: Write the failing tests:**

```python
def test_caught_needs_every_pass(): ...       # ["missing"]x3 True; [..., "supported"] False; "stated" False
def test_absent_raw_mark_is_not_a_catch():    # Review Focus 1
    assert not controls.caught([["missing"], None, ["missing"]], 1)
    assert not controls.caught([["missing"], [], ["missing"]], 1)
def test_verdict_trusted_blind_and_floor(): ... # 6 subjects: 5 caught -> trusted; 4 -> blind;
                                                # 2 dropped + 4 of 4 caught -> inconclusive (floor)
def test_verdict_clean_damage_is_inconclusive(): ...  # 6 caught, lost 2 -> inconclusive; lost 1 -> trusted
def test_leak_exclusions_cannot_decide_trusted():
    v = controls.verdict({**{f"s{i}": True for i in range(4)}, "s4": False, "s5": False}, {}, [], ["s5"], BAR)
    assert (v["verdict"], v["without_leak_exclusions"]) == ("inconclusive", "blind")
def test_leak_exclusion_stands_when_not_decisive(): ...  # 5 caught, the miss leaked -> trusted both ways
def test_clean_losses_of_uncounted_subjects_are_ignored(): ...
```

- [ ] **Step 2: Run them.** Expected: FAIL, not defined.
- [ ] **Step 3: Implement.**
- [ ] **Step 4: Run** `uv run pytest -q`. Expected: all pass.
- [ ] **Step 5: Commit** with the message "controls: the verdict under the bar fixed in PRD-002a".

### Task 4: The controls run, leak check, and report (`eval controls`)

**Files:**
- Modify: `explainer_kit/controls.py`
- Test: `tests/test_controls.py`

**Interfaces:**
- Consumes:
  - `load_controls`, `make_cuts`'s records, `caught`, `kept`, `verdict`;
  - `rederive.run(out, builds, split, only, model, reader_model, workers, passes)`;
  - `rederive.chain_text`, `rederive.tally`, `rederive.marks`.
- Produces:
  - `LEAK_SYSTEM`;
  - `leak_prompt(block: str, chain: dict, text: str) -> str`;
  - `quote_in(quote: str, text: str) -> bool`. True when the quote, stripped and with whitespace runs collapsed, is non-empty and occurs in the text treated the same way;
  - `run(out: Path, model: str | None = None, reader_model: str | None = None, workers: int = 4) -> Path`. Returns `out/controls.md`.
- Writes:
  - `out/controls/leaks/<id>-pass-<k>.json`, as `{"leak": bool, "quote": str, "confirmed": bool}`;
  - `out/controls.json`, holding the verdict dict plus per-subject detail;
  - `out/controls.md`.

**Behaviour of `run`:**
1. **Refuse,** with `SystemExit` naming the subject, when either is true:
   - any subject in `cuts` has no record, or a record with `verdict` not in (`pass`, `fail`);
   - a passing record's hash differs from its copy on disk.
2. **Copy in the baseline's reads.** For k in 1–3, each passing subject, and each condition in (`none`, `quick`, `published`): copy `baseline/rederive/pass-k/read/<id>/<cond>.json` to the same place under `out`, unless it already exists.
3. **Run the stage:** `rederive.run(out, out, split="dev", only=<passing ids>, model=model, reader_model=reader_model, workers=workers, passes=3)`.
4. **For each passing subject,** read `raw = grades["principles-cut"]["raw"]` from each pass, then:
   - `caught_by[sid] = caught(raws, cut)`;
   - `lost_by[sid]` = the number of clean `i` with `not kept(raws, i)`.
5. **Leak check,** for each subject that was not caught. For each pass k whose raw mark is not `unsupported` or `missing`:
   - ask `LEAK_SYSTEM` with `leak_prompt(cut block text, out/rederive/pass-k/read/<id>/principles-cut.json, the cut copy's text)`;
   - `confirmed = reply["leak"] is True and quote_in(reply["quote"], copy text)`;
   - save the result, and skip the call if the file already exists;
   - the subject is leaked if any pass is confirmed.
6. **Compute the verdict.** `verdict(caught_by, lost_by, dropped=<fail ids>, leaked=…, bar)`.
7. **Write `controls.md`.** It covers:
   - per subject: the cut block number; the intact marks from the baseline grades (`marks`, per pass); the cut raw marks per pass; caught or not; the uncut blocks' raw marks; the derived steps' marks, intact and cut; the supported share, intact and cut, from `tally` on normalised marks; whether the reader named a gap (`chain["gap"]` non-empty, per pass); the leak result where one ran;
   - any pass with no grader mark for the cut block (it counts as not caught), flagged so a reader sees whether a verdict rests on one;
   - that each subject's label shuffle differs from its baseline pass, since `rederive.run` shuffles once per subject from one `random.Random(k)` and this run covers six subjects, not ten;
   - the dropped subjects;
   - the left-out subjects with their reasons;
   - the verdict both ways, and the counts against the bar.

   Name the source and baseline folders relative to the project root, as `rederive.run` does.

- [ ] **Step 1: Write the failing tests.** Build a `make_cuts` output with stubs, plus a fake baseline folder holding reads and grades for three passes.

```python
def test_controls_end_to_end(monkeypatch, tmp_path): ...
    # reader calls: exactly 3 x len(passing), all for the cut copy (the stub reads the files in its `read` folder and
    # finds the cut copy's text in every reader call); grader calls: 3 x len(passing); baseline reads for none/quick/published copied unchanged;
    # controls.json verdict matches verdict() on the stubbed marks; controls.md names every left-out subject and both
    # verdicts; no reader or grader prompt contains "principles-cut"; no str(tmp_path) or str(Path.home()) in any output
def test_run_refuses_unfinished_cuts(monkeypatch, tmp_path): ...
def test_run_refuses_a_changed_cut_copy(monkeypatch, tmp_path): ...      # Review Focus 2
def test_leak_needs_a_quote_found_in_the_copy(): ...
    # quote_in("a  b\n c", "x a b c y") True; quote_in("", ...) False; quote_in("not there", ...) False
def test_leak_check_runs_only_for_uncaught_passes(monkeypatch, tmp_path): ...
def test_controls_rerun_makes_no_calls(monkeypatch, tmp_path): ...       # Review Focus 4
def test_baseline_and_source_are_untouched(monkeypatch, tmp_path): ...   # tree hashes before and after
```

- [ ] **Step 2: Run them.** Expected: FAIL.
- [ ] **Step 3: Implement.**
- [ ] **Step 4: Run** `uv run pytest -q`. Expected: all pass.
- [ ] **Step 5: Commit** with the message "controls: run the unchanged stage on the cut copies, check leaks, report the verdict".

### Task 5: CLI and command docs

**Files:**
- Modify: `explainer_kit/cli.py` (`cmd_eval`; the `eval` parser's `choices`, help, and a `--redo` flag)
- Modify: `docs/cli.md` (two rows after the `eval human` row), `CLAUDE.md` and `AGENTS.md` (one line each after the `eval rederive` line)
- Test: `tests/test_controls.py`

**Interfaces:**
- `explainer eval cuts [--only id ...] [--redo] [--out folder]` calls `controls.make_cuts(out, only, redo, model)`.
  - The default `out` is `evals/artifact/results/<date>-dev-controls`.
  - It prints one line per subject (`verdict`, attempts, and the diff path via `display`).
- `explainer eval controls --out <folder>` calls `controls.run(out, model, reader_model, workers)` and prints the verdict line and the report path.
  - Without `--out` it raises `SystemExit("eval controls needs --out <the folder eval cuts made>")`.

- [ ] **Step 1: Write the failing test.** `test_cli_cuts_and_controls_call_the_module`: monkeypatch `controls.make_cuts` and `controls.run`, then drive `sys.argv` as `test_cli_rederive_and_artifact_call_the_stage` does. Assert:
  - the arguments passed through;
  - the missing-`--out` error for `eval controls`.
- [ ] **Step 2: Run it.** Expected: FAIL (`invalid choice: 'cuts'`).
- [ ] **Step 3: Implement,** and add the doc rows and lines.
- [ ] **Step 4: Run** `uv run pytest -q && uv run explainer check`. Expected: all pass.
- [ ] **Step 5: Commit** with the message "cli: eval cuts and eval controls".

### Task 6: Make the real cuts, and freeze them (live: calls the `claude` CLI)

**Files:**
- Create: `evals/artifact/results/<date>-dev-controls/` (`cuts/`, `work/`, `conditions.json`)
- Modify: `tests/test_controls.py` (the pin test)

- [ ] **Step 1: Run** `uv run explainer eval cuts`. Expected: six lines, each `pass` or `fail`. Two-tides is the most likely `fail` (see the PRD).
- [ ] **Step 2: Read every diff** in `cuts/`, against the PRD's cut rule:
  - the removed text states the block or lets the reader recover it, and nothing more is gone;
  - the rest is unchanged.

  For a cut that removed more, run `uv run explainer eval cuts --only <id> --redo` once it has attempts left. Ledger each judgment as `Task 6: Ruling: <id> diff <accepted|redone> — <why> — <cost if wrong>`.
- [ ] **Step 3: Check the folder for the floor.** If fewer than 5 subjects pass, the result will be inconclusive whatever the run shows. Ledger that, and continue: the PRD runs and reports it anyway.
- [ ] **Step 4: Add the pin test, and a test that the uncut builds match on the real data,** then run `uv run pytest -q`. Expected: all pass. The second test is `test_uncut_builds_match_the_source`: for each passing subject and each of `none`, `quick`, `published`, `ae.renderings` on the controls folder returns the same paths (relative to the condition folder) and bytes as on the source. Heat-pump's `published` build relies on the rglob fallback.

```python
CONTROLS = ROOT / "evals" / "artifact" / "results" / "<date>-dev-controls"
FROZEN_CUTS = "<16 hex>"   # controls.yaml plus every cut record and copy, as frozen before the controls run

def test_cuts_are_the_frozen_ones():
    # sha256 over controls.yaml's text, then, for each subject sorted, its record's verdict and hash and its copy's text
    ...
    assert digest == FROZEN_CUTS, "a cut changed after the freeze"
```

- [ ] **Step 5: Freeze commit.**
  - Run `git diff --exit-code` on the three earlier results folders. Expected: clean.
  - Commit the folder and the pin test with the message "FREEZE: PRD-002a cut copies, checks and diffs, before any controls run".
  - This commit must come before Task 7 Step 1.

### Task 7: The controls run and the write-up (live)

**Files:**
- Create: `evals/artifact/results/<date>-dev-controls/rederive/…`, `controls/…`, `controls.md`, `controls.json`, `rederive.md`, `rederive-scores.json`
- Modify: `docs/evals.md` (a new `### Does the test catch a missing block?` subsection, after `### What the dev baseline found`), `ROADMAP.md` (§15 "Next"), `CHANGELOG.md` ("Unreleased")

- [ ] **Step 1: Run** `uv run explainer eval controls --out evals/artifact/results/<date>-dev-controls`. Expected: a verdict line (`trusted`, `blind`, or `inconclusive`) and `controls.md`.
- [ ] **Step 2: Read `controls.md`** and spot-check two subjects' grades and chains against it. If the report disagrees with the files, the code is wrong: use superpowers:systematic-debugging. The verdict is never edited by hand.
- [ ] **Step 3: Write the `docs/evals.md` subsection** from the PRD's Goal 4:
  - what was cut, and why only six subjects count;
  - the bar;
  - the verdict both ways, and the per-subject catches;
  - what the derived-step marks show;
  - that the label shuffles differ from the baseline's, an item missing from the PRD's list of differences;
  - the meaning, in the PRD's wording for the verdict reached. "Trusted" covers only targets with an eligible block;
  - that four of ten dev targets can't show a missing block, and that the test-split targets may share the problem.
- [ ] **Step 4: Record it in two places.**
  - ROADMAP §15 "Next": the verdict, plus the item "classify the 20 test-split targets by the PRD-002a eligibility rule before PRD-003 relies on them".
  - CHANGELOG "Unreleased": one bullet for the controls, linking the subsection.
- [ ] **Step 5: Verify.**
  - `uv run pytest -q && uv run explainer check`. Expected: all pass.
  - `git diff --exit-code` on the three earlier results folders. Expected: clean.
  - `grep -rn "/Users/\|/private/\|/tmp/" evals/artifact/results/<date>-dev-controls`. Expected: no output.
- [ ] **Step 6: Commit** with the message "PRD-002a: controls run and write-up: <verdict>".
- [ ] **Step 7: If the verdict is blind,** stop after the final review and tell the owner that Goal 5 needs its own plan. Don't start it.

Then run the final whole-branch review per the execution skill. Pushing, merging, and any release are the owner's calls.
