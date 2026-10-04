# Narrative: git-objects

> Pass 3. The diagram page follows these beats.

## 1. Reader before and after

- **Before:** Developers who use git commands but think of a commit as "a diff".
- **After:** "A commit points to a full snapshot (a tree of blobs), named by the hash of its content; unchanged files cost nothing because the new tree points to the same blob, and diffs are computed when you ask."

## 2. Question and motive

- **Question:** what does git store when you commit? Answer first: four kinds of objects, each named by the hash of its content.
- **Why care:** the "commit is a diff" picture predicts the wrong cost and the wrong behavior of history.
- **Why this approach:** the answer is topology: which object points to which. One diagram holds it.

## 3. Introduction ledger

| Reference | Means | Grounded by | Beat |
|---|---|---|---|
| blob, tree, commit, tag | the four object types | the table and the diagram | 1, 2 |
| hash (ID) | the name of an object, computed from its content | "commit 7f3a…" | 1 |
| ref, HEAD | a name that points to an object, not an object | HEAD → main → commit | 2 |
| dashed node, thick border | a ref; a blob shared by two trees | HEAD and main; README's blob | 2 |

## 4. Beats

| # | Kind | Reader's question | Bridge | Shown | Said | Reader now knows |
|---|---|---|---|---|---|---|
| 1 | answer | What is stored? | — | — | Four object types, named by content hash; a commit is a full snapshot, and an unchanged file costs nothing. | the answer |
| 2 | structure | How do they connect? | so | the diagram | HEAD → main → commit → tree → blobs and trees; parent commits. | the topology |
| 3 | instance | Why is an unchanged file free? | but | the shared blob | both trees point to blob a3f2…; a changed file gets a new blob and new trees above it. | snapshot without copying |
| 4 | misconception | So where are the diffs? | but | — | `git show` computes them; packfiles store deltas, but that is storage, not the model. | the correction |

## 7. Close the loop

- **Answer:** the misconception line answers "a commit is a diff" directly.
