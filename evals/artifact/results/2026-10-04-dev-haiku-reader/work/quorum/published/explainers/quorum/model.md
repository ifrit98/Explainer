# Semantic model: quorum (majority voting in a replicated cluster)

> Source of truth. Every rendering (prose, diagram, page, video) derives from this file.
> If a rendering needs a new fact, add it here first.

## Central question

Why does a cluster of 5 servers keep working after 2 servers fail, but a cluster of 4 servers keeps working after only 1?

## Audience and prior knowledge

A technical reader: school mathematics and science, basic programming. Knows what a server and a network are, and that a database can keep copies on several machines. New to distributed consensus: does not know the words quorum, partition, or split brain. Does not know Raft or Paxos. Floor and integer division are known.

## Entities

| Entity | Definition (one sentence) | Status |
|---|---|---|
| cluster | n servers that each keep a copy of the same data and must agree on every change to it. | definition |
| accept | a server stores a proposed change on disk and replies "yes". | definition |
| position | the place of a change in the order the cluster decides changes (change 1, change 2, …); a server accepts only one change per position, e.g. change 7. | definition |
| decide | a change becomes final because a quorum accepted it. | definition |
| failure | a server stops answering: it crashed, or the network cannot reach it. | assumption (crash failures only; no server lies; disks survive a restart) |
| quorum size | the number of servers that must accept a change before it is decided. Here always the majority size of n. | definition |
| quorum | any group of at least quorum-size servers, e.g. {A, B, C} in a 5-server cluster. | definition |
| majority size | more than half of all n configured servers: floor(n/2) + 1. | definition |
| partition | the network splits the servers into groups that cannot reach each other, while every server keeps running. | definition |
| split brain | two groups each decide a different change, so the copies disagree. | definition |
| tolerance | the number of failed servers the cluster can lose and still decide new changes. | definition |

## Relationships

| From | Relationship (verb) | To | Notes |
|---|---|---|---|
| quorum size | is set to | majority size | so any two quorums share at least one server |
| shared server | blocks | split brain | it already accepted the first change and refuses a conflicting one |
| failure | removes a vote from | quorum | cluster stops deciding if fewer than quorum size servers answer |
| n | sets | majority size, tolerance | tolerance = n − majority size |

## Dependencies (learning order)

1. A change is decided only when a quorum accepts it.
2. A server cannot tell a crashed server from a cut-off one.
3. So the quorum size must be a majority; two majorities always share a server, and that server blocks a second, conflicting change.
4. Tolerance = n − majority size. Count for 5 and for 4.
5. Generalize: the table for n = 3..7; the even server adds nothing to tolerance.

## Causal chain

```text
a server cannot tell a crash from a partition
  → each group must assume the missing servers may still run and decide
  → quorum size must be a majority, so two groups cannot both decide
  → majority size of 5 is 3, and majority size of 4 is also 3
  → cluster of 5 can lose 5 − 3 = 2; cluster of 4 can lose 4 − 3 = 1
```

## Temporal sequence

1. A client sends change x = 1 to a 5-server cluster.
2. A accepts (1 vote), B accepts (2), C accepts (3 = quorum size). x = 1 is decided. D and E can catch up later.
3. In a 4-server cluster with C and D down, only A and B accept: 2 < 3, so x = 1 waits. No decided change is lost; no new change is decided until C or D returns.

## Quantities

- majority size(n) = floor(n/2) + 1. n = 4 → 3; n = 5 → 3.
- tolerance(n) = n − majority size(n). n = 4 → 1; n = 5 → 2.
- Table: n = 3, 4, 5, 6, 7 → majority size 2, 3, 3, 4, 4 → tolerance 1, 1, 2, 2, 3.
- Overlap of two quorums is at least 2 × majority size − n: n = 5 → 3 + 3 − 5 = 1.
- Meaning of tolerance: at 1, a second failure stops the cluster from deciding; at 2, the cluster can lose one server while another is down for an upgrade.
- Cost of the even server: n = 6 waits for 4 acceptances per change instead of 3, and tolerance stays 2.

## Alternative states

| State / scenario | What changes | Why |
|---|---|---|
| 5 servers, 2 failed | 3 answer = majority size 3 → keeps deciding | 3 ≥ 3 |
| 4 servers, 1 failed | 3 answer → keeps deciding | 3 ≥ 3 |
| 4 servers, 2 failed | 2 answer < 3 → stops deciding | 2 < 3 |
| 5 servers, partition {A,B,C} / {D,E} | left side decides, right side stops; copies cannot disagree | 3 ≥ 3, 2 < 3 |
| 4 servers, partition {A,B} / {C,D} | neither side decides | 2 < 3 on both sides |
| 4 servers, quorum size lowered to 2, partition {A,B} / {C,D} | both sides decide different changes → split brain | 2 + 2 = 4, no shared server |

## Why this form

| Operation | Simplest alternative | What the alternative breaks (with numbers) |
|---|---|---|
| quorum size = majority size (more than half) | quorum size = half (2 of 4), so 2 survivors can go on | partition {A,B} / {C,D}: A, B decide x = 1, C, D decide x = 2. Both groups have 2 = quorum size. Copies disagree: split brain. |
| count the majority of all n configured servers | count the majority of the servers each side can reach | 5 servers split {A,B,C} / {D,E}: D, E reach 2 servers, majority of 2 is 2, so they decide x = 2 while A, B, C decide x = 1: split brain. |
| quorum size = majority, not all n | quorum size = 5 of 5 | one failure stops the cluster: tolerance 0. |

## Concrete cases

| Claim | Holds here (numbers) | Breaks here, without its assumption (numbers) |
|---|---|---|
| Two quorums of majority size always share a server (guarantee) | n = 5: {A,B,C} and {C,D,E}: 3 + 3 = 6 > 5, so at least 1 server (C) is in both. | Size 2 of 5 or 4: {A,B} and {C,D} share nothing (2 + 2 = 4). |
| The shared server blocks split brain (mechanism) | A, B, C accept x = 1. Then C, D, E are asked to accept x = 2. C already accepted x = 1 and refuses; x = 2 has 2 votes < 3. | If C restarts with an empty disk and accepts x = 2, then C, D, E decide x = 2 too: split brain. So the assumption "a server keeps what it accepted" matters. |
| A server cannot tell crash from partition (mechanism) | A sends to D and gets no reply, however long it waits. Case 1: D crashed. Case 2: the link A–D is cut and D still accepts changes from E. In both cases A sees the same thing: no reply. | — |
| 5 servers tolerate 2 failures (mechanism) | 5 − 2 = 3 answering ≥ 3. | Third failure: 2 answering < 3 → stops. |
| 4 servers tolerate 1 failure (mechanism) | 4 − 1 = 3 ≥ 3. | 4 − 2 = 2 < 3 → stops. |

## Terms

- **cluster:** n servers keeping copies of the same data.
- **accept:** a server stores a proposed change on disk and replies "yes".
- **decide:** a change becomes final because a quorum accepted it. "Keeps working" means "can still decide new changes". Use "decide", not "write" or "commit".
- **stops:** the cluster still holds every decided change but decides no new change until enough servers return.
- **failure:** a server stops answering (crash or unreachable).
- **quorum size:** a number, e.g. 3. **quorum:** a group of servers, e.g. {A, B, C}. Never swap them.
- **majority size:** more than half of all n configured servers, counting failed servers too: floor(n/2) + 1.
- **partition:** the network splits the servers into groups that cannot reach each other.
- **split brain:** two groups decide different changes.
- **tolerance:** how many failed servers the cluster can lose and still decide. At 1, a second failure stops it; at 2, it can lose one server while another is down for an upgrade.

## Epistemic status

- **Mathematical consequence:** two majorities overlap; tolerance = n − (floor(n/2) + 1).
- **Assumed:** crash failures only (a server stops or is unreachable; it never sends a false "yes"). A server keeps what it accepted across a restart. Quorum size is fixed by the configured n.
- **Simplification:** "the shared server refuses x = 2" stands in for the real protocol step, in which the shared server reports x = 1 to the new group and the group keeps x = 1 (Raft, Paxos).

## Confusion points

- "With 2 of 4 alive, why not just continue?" → the 2 cannot know whether the other 2 crashed or are cut off and still deciding.
- "Majority of the servers still running" → no: majority of all n configured servers. Otherwise each side of a partition counts itself a majority.
- "More servers is always safer" → going from 5 to 6 raises quorum size to 4; tolerance stays 2.
- "Survive" does not mean "lose no data": a stopped cluster keeps its decided changes; it only stops deciding new ones.

## Scope

- **Out of scope:** servers that lie (Byzantine failures) need more servers: 4 servers to tolerate 1 liar. See PBFT.
- **Out of scope:** how a leader is elected, how a server detects a timeout, and how a minority side catches up after the partition heals. See the Raft paper ("In Search of an Understandable Consensus Algorithm").
- **Out of scope:** reasons to use even n anyway (read load, a tie-breaker "witness" server), and reads that skip the quorum.
- **Out of scope:** weighted votes and flexible quorums (different sizes for reads and changes).
- **Practice:** Raft and Paxos systems such as etcd and ZooKeeper use majority quorums and recommend odd n.

## Representation decision

- **Stage:** 1
- **Reason:** the argument is a short chain of counting; one table (n, majority size, tolerance) carries the comparison. Nothing to explore or animate.
- **Levels:** L1 the answer / L2 the counting / L3 why majority (partition) / L4 general table.
