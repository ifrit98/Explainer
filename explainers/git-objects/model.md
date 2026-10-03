# Semantic model: git's object model

## Central question

What does git actually store when you commit?

## Audience and prior knowledge

Developers who use git commands but think of a commit as "a diff".

## Entities

| Entity | Definition | Status |
|---|---|---|
| Blob | The content of one file. No name, no path. | fact |
| Tree | One directory: a list of names, each pointing to a blob or a tree. | fact |
| Commit | A snapshot: one root tree, zero or more parent commits, author, message. | fact |
| Ref (branch) | A name that points to one commit. | fact |
| HEAD | A pointer to the current branch (or to a commit, when detached). | fact |
| Object ID | The hash of an object's content. It is the object's address. | fact |

## Relationships

commit → tree (1) · commit → parent commit (0..n) · tree → blob / tree (n) · branch → commit · HEAD → branch.

## Causal chain

Content-addressed storage → identical content has the same ID → an unchanged file in a new commit reuses the old blob → a commit is a full snapshot that costs only the changed objects.

## Epistemic status

- **Fact:** a commit stores a snapshot (a tree), not a diff. Diffs are computed when you ask for them.
- **Implementation detail:** packfiles store objects as deltas on disk. This is compression, not the data model.
- **Fact:** the hash is SHA-1 by default; repositories can use SHA-256.

## Confusion points

- "A commit is a diff." → A commit points to a whole tree. `git show` computes the diff against the parent.
- "Each commit copies every file." → Unchanged files reuse the same blob.

## Representation decision

- **Stage:** 2 (static diagram).
- **Reason:** the subject is topology: five object types and four pointer relationships. The reader must hold all of them at once. Nothing moves, so no animation; no parameter, so no interactive page.
