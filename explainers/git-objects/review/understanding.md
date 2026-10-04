# Understanding tests: git-objects

## Cold read (diagram, v0.6.0)

Run 2026-10-04, reading as "developers who use git commands but think of a commit as a diff".

- **Blocking, fixed:** why a changed file gives every tree above it a new ID was never said, and the table hid the reason (a tree stores "names and modes", not the IDs of its entries); "same content, same ID, same object" was never said aloud; the reader's belief ("a commit is a diff") was addressed only at the end; the header said five object types and the text four.
- Now: the page opens with the belief and the answer, says the mechanism in one sentence, explains the visual conventions before the diagram (rectangles are objects, dashed rounded boxes are refs, a thick border is a shared blob), and step 5 follows the new IDs up to the commit. The table lists the IDs each object stores, and when a commit has zero, one, or several parents.
- **Excess, cut:** the build-metadata line; HEAD-points-to-main, which this reader knows; a repeat of "a commit points to a whole tree".
- **Not applied (edge):** an unchanged directory in the example; the lightweight tag.
