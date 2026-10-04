# Understanding tests: git-bisect

## Cold read (prose, v0.6.0)

Run 2026-10-04, reading as "developers who use git daily and have not used bisect". `narrative.md` was written first, from the existing prose.

- **Blocking, fixed:** "each test halves the range" had no mechanism (which half is kept, and why); the remedy for a bug that comes and goes did not work: in the document's own example, the commits just before 900 are good, so testing them never finds 300. Now: test commits spread across the earlier history; in the example 350 is bad, and a second bisect between the good commit and 350 names 300. `git bisect start <bad> <good>` now says which argument is which.
- **Excess, cut:** the build-metadata blockquote under the title.
- **Added (short):** "first bad commit" defined; `git bisect bad <commit>` for when the current commit is not the bad one; the test command must fail only for this bug; a two-sentence close.
- **Not applied (edge):** exit codes above 127; a skip near the boundary.

## v0.7.0 review runs

- Cold read, round 2 (`--run`): nothing blocks. Adopted 3 of 16 findings: bisect takes you off your branch; a commit cannot be tested when it does not build; the good commit must be before 300 for the second bisect to find it.
- Blind test: **pass** after the rubric fix (the first grade failed a correct answer for not repeating the rendering's own example).
