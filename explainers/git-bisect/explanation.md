# Find the commit that introduced a bug

> Stage 1 (controlled prose), rendered from [`model.md`](model.md). Routing: a linear procedure → numbered steps. No diagram, page, or video is needed.

<!-- claim: why-halving -->
`git bisect` finds the first bad commit by binary search. Each test halves the range of suspect commits. For 1,000 commits you test about 10 times: 1,000 → 500 → 250 → 125 → 63 → 32 → 16 → 8 → 4 → 2 → 1. Testing the commits one by one could take 1,000 tests.

## Before you start

Find one commit where the bug is absent (*good*) and one where it is present (*bad*). The current commit is often the bad one.

## Procedure

1. Start the session:
   ```bash
   git bisect start
   ```
2. Mark the current commit as bad:
   ```bash
   git bisect bad
   ```
3. Mark a known good commit:
   ```bash
   git bisect good v2.3.0
   ```
   Git checks out a commit halfway between the two.
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

Skip it. Git selects a nearby commit.

```bash
git bisect skip
```

## Automate the test

Give git a command. Git runs it at each step and marks the result from the exit code.

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

Example: across 1,000 commits, the bug is present in commits 300–400, gone, and back from 900. The first test, at 500, is good. Bisect now searches only 500–1,000 and names 900. The bug first appeared at 300. If you suspect this, test a few commits before the named one by hand.
