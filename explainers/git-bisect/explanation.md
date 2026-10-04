# Find the commit that introduced a bug

<!-- Stage 1, rendered from model.md: a linear procedure, so numbered steps. -->

<!-- claim: why-halving -->
`git bisect` finds the first bad commit, the earliest commit where the bug is present, by binary search. You test the commit halfway between a good one and a bad one. If it is bad, the first bad commit is at or before it; if it is good, the first bad commit is after it. Either way half the suspects are gone. For 1,000 commits you test about 10 times: 1,000 → 500 → 250 → 125 → 63 → 32 → 16 → 8 → 4 → 2 → 1, against up to 1,000 tests one by one.

## Before you start

Find one commit where the bug is absent (*good*) and one where it is present (*bad*). The current commit is often the bad one.

## Procedure

1. Start the session:
   ```bash
   git bisect start
   ```
2. Mark the current commit as bad (or name a bad commit: `git bisect bad <commit>`):
   ```bash
   git bisect bad
   ```
3. Mark a known good commit:
   ```bash
   git bisect good v2.3.0
   ```
   Git checks out a commit halfway between the two, so you are no longer on your branch.
4. Test this commit.
5. Mark the result:
   ```bash
   git bisect good    # the bug is absent
   git bisect bad     # the bug is present
   ```
   Git checks out the next midpoint.
6. Repeat steps 4–5 until git prints `<hash> is the first bad commit`.
7. Return to your branch:
   ```bash
   git bisect reset
   ```

## If a commit cannot be tested

Skip it, for example when it does not build. Git selects a nearby commit.

```bash
git bisect skip
```

## Automate the test

Give git a command. Git runs it at each step and marks the result from the exit code. `git bisect start <bad> <good>` does steps 1–3 in one line. The command must fail only for this bug: a test that fails for another reason marks a commit bad.

```bash
git bisect start HEAD v2.3.0
git bisect run npm test
```

| Exit code | Meaning |
|---|---|
| 0 | good |
| 125 | skip |
| 1–127, except 125 | bad |

## Limit

<!-- claim: guarantee-first-bad -->
Bisect assumes that the bug appears once and stays. If the bug comes and goes, bisect can name the wrong commit.

Example: across 1,000 commits, the bug is present in commits 300–400, gone, and back from 900. The first test, at 500, is good. Bisect now searches only 500–1,000 and names 900. The bug first appeared at 300. Testing next to 900 does not reveal this: those commits are good. If you suspect it, test a few commits spread across the earlier history. In the example, 350 is bad; bisect again between a good commit before 300 and 350, and it names 300.

## In short

Each good or bad mark rules out half the suspects, because a bug that appears once stays. About 10 tests find the first bad commit among 1,000.
