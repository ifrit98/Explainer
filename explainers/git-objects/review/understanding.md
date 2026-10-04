# Understanding tests: git-objects

## Cold read (diagram, v0.6.0)

Run 2026-10-04, reading as "developers who use git commands but think of a commit as a diff".

- **Blocking, fixed:** why a changed file gives every tree above it a new ID was never said, and the table hid the reason (a tree stores "names and modes", not the IDs of its entries); "same content, same ID, same object" was never said aloud; the reader's belief ("a commit is a diff") was addressed only at the end; the header said five object types and the text four.
- Now: the page opens with the belief and the answer, says the mechanism in one sentence, explains the visual conventions before the diagram (rectangles are objects, dashed rounded boxes are refs, a thick border is a shared blob), and step 5 follows the new IDs up to the commit. The table lists the IDs each object stores, and when a commit has zero, one, or several parents.
- **Excess, cut:** the build-metadata line; HEAD-points-to-main, which this reader knows; a repeat of "a commit points to a whole tree".
- **Not applied (edge):** an unchanged directory in the example; the lightweight tag.

## v0.7.0 review runs

- Claims added: `mechanism-content-id`, `guarantee-shared`, `misconception-diff`.
- Cold read, round 2: **blocking**, three, two of them introduced by the round-1 fixes: the page ended on "a commit stores only what changed", which reads as the diff model it set out to correct; "tree" and "blob" were used before they were defined; "same ID, so the same object" skipped that git stores objects by ID. Fixed: blob, tree, commit, and tag defined in the opening; "stored under its ID"; the close says each commit points to a complete tree and only new objects are written. From the blind-test audit: a blob has no name, so a renamed file is still one blob.
- Diagram budget: 11 nodes in the first diagram, declared in `model.yaml` (two snapshots side by side are needed to show the shared blob).
- Blind test: **pass** after the rubric fix (round 3; the round-2 run failed to parse and was rerun).
