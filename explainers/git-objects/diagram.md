# What git stores when you commit

> Stage 2 (static diagram), rendered from [`model.md`](model.md). Routing: topology with five object types → component diagram.

Git stores four kinds of objects. Each object's ID is the hash of its content. A commit is a full snapshot, but an unchanged file costs nothing: the new tree points to the same blob.

```mermaid
flowchart LR
    HEAD([HEAD]) --> main([main])
    main -->|points to| C2

    subgraph commits [Commits]
        C2["commit 7f3a…<br/>'Fix parser'"] -->|parent| C1["commit 2b91…<br/>'Initial commit'"]
    end

    C2 -->|root tree| T2["tree e41c…"]
    C1 -->|root tree| T1["tree 9d07…"]

    T2 -->|README.md| B1["blob a3f2…<br/>README content"]
    T2 -->|src/| S2["tree 51aa…"]
    T1 -->|README.md| B1
    T1 -->|src/| S1["tree 0c6e…"]

    S2 -->|parser.py| B3["blob c88d…<br/>parser v2"]
    S1 -->|parser.py| B2["blob 4e10…<br/>parser v1"]

    classDef ref fill:none,stroke-dasharray:4 3
    classDef shared stroke-width:3px
    class HEAD,main ref
    class B1 shared
```

**Read the diagram:**

1. `HEAD` points to the branch `main`. `main` points to a commit. Refs are names, not objects.
2. Each commit points to one root tree and to its parent commit.
3. A tree maps names to blobs (files) or to other trees (directories).
4. `README.md` did not change between the commits, so both trees point to the same blob `a3f2…` (thick border).
5. `parser.py` changed, so it has a new blob, and every tree above it gets a new ID: `src/` and the root tree.

| Object | Stores | Points to |
|---|---|---|
| blob | file content only (no name) | nothing |
| tree | names and modes | blobs and trees |
| commit | author, time, message | one tree, 0..n parents |
| tag (annotated) | tagger, message | one object, usually a commit |

**Common error:** "a commit is a diff." A commit points to a whole tree. `git show` computes the diff against the parent when you ask. On disk, packfiles compress objects as deltas, but that is storage, not the data model.

Hashes are shortened and illustrative.
