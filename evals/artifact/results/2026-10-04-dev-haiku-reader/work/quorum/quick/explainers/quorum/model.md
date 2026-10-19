# Semantic model: majority quorums and failure tolerance

## Central question

Why does a cluster of 5 servers survive 2 failures, but a cluster of 4 survives only 1?

## Audience and prior knowledge

A technical reader: school mathematics, basic programming. Knows what a server and a network are. Does not know consensus, quorum, network partition, or split brain.

## Entities

| Entity | Definition (one sentence) | Status |
|---|---|---|
| cluster | n servers that keep copies of the same data and must agree on each change. | fact |
| decision | a change that the cluster accepts, such as "x = 7". | fact |
| quorum | the minimum number of servers that must agree before the cluster makes a decision; here a majority, floor(n/2) + 1. | fact (design rule) |
| failure | a server that does not reply: crashed, or cut off by the network. | fact |
| partition | a network fault that splits the servers into groups that cannot reach each other. | fact |
| split brain | two groups each make a decision, and the decisions conflict. | fact |

## Relationships

| From | Relationship (verb) | To | Notes |
|---|---|---|---|
| quorum | prevents | split brain | two majorities always share a server |
| failure | reduces | servers that can reply | cluster stops when replies < quorum |
| n | sets | quorum | q = floor(n/2) + 1 |

## Dependencies (learning order)

1. A silent server can be dead or only cut off; the others cannot tell which.
2. So a group must be sure that no other group can decide at the same time.
3. Majority guarantees this; it sets the quorum.
4. Failures tolerated = n − quorum.

## Causal chain

```text
crash looks like partition → each group must assume the others are alive
→ only one group may decide → quorum must be a majority (two majorities overlap)
→ tolerated failures = n − majority → 5 gives 2, 4 gives 1
```

## Quantities

- quorum q = floor(n/2) + 1. n=3 → 2, n=4 → 3, n=5 → 3, n=6 → 4, n=7 → 4.
- failures tolerated f = n − q. n=3 → 1, n=4 → 1, n=5 → 2, n=6 → 2, n=7 → 3.
- servers needed to tolerate f failures: n = 2f + 1.
- Overlap test: two groups of size q both fit without sharing a server only if 2q ≤ n. Majority makes 2q > n.

## Alternative states

| State / scenario | What changes | Why |
|---|---|---|
| 4 servers, quorum 2 (half) | partition 2 + 2: both sides decide | 2 + 2 = 4 is not > 4; no shared server |
| 4 servers, quorum 3 | partition 2 + 2: neither side decides; cluster stops | safe, but 2 failures stop it |
| 5 servers, quorum 3 | partition 3 + 2: only the 3 side decides | 3 + 3 = 6 > 5 |

## Why this form

| Operation | Simplest alternative | What the alternative breaks (with numbers) |
|---|---|---|
| quorum = majority | quorum = half (2 of 4) | split 2 + 2: side A writes x = 7, side B writes x = 9; both have a quorum; split brain |
| quorum = majority | "count the servers still alive" | a crash and a partition look the same; each side of a 2 + 2 split sees 2 alive and decides |

## Concrete cases

| Claim | Holds here (numbers) | Breaks here, without its assumption (numbers) |
|---|---|---|
| tolerance = n − majority | 5 servers, 2 fail: 3 reply ≥ 3, cluster continues | 4 servers, 2 fail: 2 reply < 3, cluster stops |
| even n adds no tolerance | 3 → 1, 4 → 1 | — |

## Terms

- cluster, decision, quorum, failure, partition, split brain: as in Entities.

## Epistemic status

- **Mathematical consequence:** overlap of majorities; f = n − q.
- **Assumed:** servers fail by stopping or going silent, not by lying.

## Confusion points

- "With 4 servers, 3 are left after 1 failure, so 2 more could go" → quorum is 3, not "any survivors".
- "The 4th server is useless" → it adds read capacity and a spare copy; it adds no failure tolerance, and it adds one more server that can fail.

## Scope

- **Out of scope:** servers that lie (Byzantine faults) need n = 3f + 1 — see PBFT.
- **Out of scope:** how Raft and Paxos use quorums for leader election and log replication.

## Representation decision

- **Stage:** 1
- **Reason:** the argument is a short chain plus one comparison table; no topology the reader must hold.
- **Levels:** L1 the rule / L2 failures vs quorum / L3 why majority / L4 n = 2f + 1.
