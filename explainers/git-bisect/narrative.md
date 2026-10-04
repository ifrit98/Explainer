# Narrative: git-bisect

> Pass 3. The prose follows these beats.

## 1. Reader before and after

- **Before:** Developers who use git daily. They know commits and checkout. They have not used bisect.
- **After:** "git bisect finds the first bad commit in about log₂ n tests: mark one good and one bad commit, test each midpoint git checks out, and it narrows the range by half each time, as long as the bug appeared once and stayed."

## 2. Question and motive

- **Question:** which commit introduced this bug? Answer first: bisect finds it by binary search.
- **Why care:** 1,000 commits take about 10 tests, not up to 1,000.
- **Why this approach:** each test tells you which half holds the first bad commit.

## 3. Introduction ledger

| Reference | Means | Grounded by | Beat |
|---|---|---|---|
| good / bad | the bug is absent / present at that commit | "the current commit is often the bad one" | 2 |
| first bad commit | the earliest commit where the bug is present | the line git prints at the end | 1, 3 |
| midpoint | the commit git checks out halfway between the last good and bad | step 3 | 3 |

## 4. Beats

| # | Kind | Reader's question | Bridge | Said | Reader now knows |
|---|---|---|---|---|---|
| 1 | answer | How do I find the commit? | — | Binary search; 1,000 commits take about 10 tests. | the idea and its payoff |
| 2 | setup | What do I need? | so | One good and one bad commit. | the inputs |
| 3 | procedure | What do I type? | — | start, bad, good, test, mark, repeat, reset. | the procedure |
| 4 | edge case | What if a commit cannot be tested? | but | `git bisect skip`. | the escape |
| 5 | shortcut | Can a script do the testing? | so | `git bisect run`, with exit codes. | automation |
| 6 | limit | When does it give the wrong answer? | but | A bug that comes and goes: present 300–400, back from 900; bisect names 900. | the assumption |

## 7. Close the loop

- **Answer:** the procedure ends at "the first bad commit"; the limit says when that answer can be wrong.
