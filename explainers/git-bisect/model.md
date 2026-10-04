# Semantic model: git bisect

## Central question

How do I find the commit that introduced a bug, using `git bisect`?

## Audience and prior knowledge

Developers who use git daily. They know commits and checkout. They have not used bisect.

## Entities

| Entity | Definition | Status |
|---|---|---|
| Good commit | A commit where the bug is absent. | user observation |
| Bad commit | A commit where the bug is present. | user observation |
| Bisect session | A state in which git checks out commits between good and bad for you to test. | fact |
| First bad commit | The earliest commit where the bug is present. The output of bisect. | fact |
| Test | A command or manual check that decides good or bad. | user-supplied |

## Temporal sequence

1. Start the session. 2. Mark bad. 3. Mark good. 4. Git checks out the midpoint. 5. Test, mark. 6. Repeat 4–5 until git names the first bad commit. 7. Reset.

## Quantities

Steps ≈ log₂(N) for N commits between good and bad. 1,000 commits → about 10 steps.

## Alternative states

| State | Action |
|---|---|
| Commit cannot be tested (build broken) | `git bisect skip` |
| Test is a script | `git bisect run <cmd>`: exit 0 = good, 125 = skip, 1–127 except 125 = bad |

## Why this form

| Operation | Simplest alternative | What the alternative breaks |
|---|---|---|
| Test the midpoint and halve the range | test commits one by one, oldest first | 1,000 commits can take up to 1,000 tests one by one. Halving takes 10: 1,000 → 500 → 250 → 125 → 63 → 32 → 16 → 8 → 4 → 2 → 1. |

## Concrete cases

| Claim | Holds here | Breaks here, without its assumption |
|---|---|---|
| Bisect names the first bad commit, if the bug appears once and stays. | 1,000 commits, good at 0, bad from 300 on: the first test (500) is bad, and 10 tests later bisect names 300. | The bug is present in commits 300–400, absent again, and back from 900. The first test (500) is good, so bisect searches 500–1,000 and names 900. The bug first appeared at 300. |

## Epistemic status

- **Assumption:** the bug appears once and stays. If the bug comes and goes, bisect can name the wrong commit.
- **Fact:** the step count is logarithmic because each step halves the range.

## Confusion points

- Bisect changes your checkout. → Run `git bisect reset` to return to your branch.

## Representation decision

- **Stage:** 1 (controlled prose).
- **Reason:** the subject is a linear procedure with one loop and two exceptions. Numbered steps carry all of it. A diagram would add nothing that the step list does not show.
