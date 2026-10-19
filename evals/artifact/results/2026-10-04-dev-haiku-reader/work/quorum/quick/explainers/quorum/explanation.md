# Why do 5 servers survive 2 failures, but 4 servers survive only 1?

**Both clusters need 3 servers to agree before they make a decision. 5 − 3 = 2 servers can fail. 4 − 3 = 1 server can fail.** The number 3 comes from one rule: the agreeing group must be a majority. Without that rule, two halves of a cluster can decide different things at the same time.

## The setup

A **cluster** is a group of servers that keep copies of the same data. Each change, such as "x = 7", is a **decision**. All servers must end up with the same decisions in the same order.

A **quorum** is the minimum number of servers that must agree before the cluster makes a decision. A server that does not reply is a **failure**.

<!-- claim: tolerance -->
The cluster continues while at least a quorum of servers can reply. So the number of failures it tolerates is *servers − quorum*:

- 5 servers, quorum 3. Two servers fail. Three reply. 3 ≥ 3, so the cluster continues.
- 4 servers, quorum 3. Two servers fail. Two reply. 2 < 3, so the cluster stops.

The question is now: why is the quorum 3 for 4 servers, and not 2?

## Why the quorum must be a majority

<!-- claim: silent -->
A server cannot tell a crashed server from a server that it cannot reach. Both look the same: no reply. A **partition** is a network fault that splits the servers into groups that cannot reach each other.

<!-- claim: why-majority -->
Try quorum 2 with 4 servers. A partition splits them into group A (2 servers) and group B (2 servers). Each group sees two silent servers. Each group has 2 servers, which is a quorum. Group A decides x = 7. Group B decides x = 9. When the network heals, the cluster holds two conflicting values and has no correct way to choose. This is **split brain**.

The fix is to make two quorums impossible at the same time. Two groups of size *q* fit into *n* servers without a shared server only if 2*q* ≤ *n*. So choose 2*q* > *n*: the smallest such *q* is a majority, ⌊*n*/2⌋ + 1. Any two majorities then share at least one server, and that server refuses to agree to two conflicting decisions.

- 5 servers: 3 + 3 = 6 > 5. A split of 3 + 2 lets only the side with 3 decide.
- 4 servers: 2 + 2 = 4, not > 4. The quorum must rise to 3. A 2 + 2 split now stops both sides. That is safe, but it is the "2 failures stop the cluster" case from above.

## The pattern

| Servers | Quorum (majority) | Failures tolerated |
|---|---|---|
| 3 | 2 | 1 |
| 4 | 3 | 1 |
| 5 | 3 | 2 |
| 6 | 4 | 2 |
| 7 | 4 | 3 |

<!-- claim: even-n -->
Adding a server to an odd cluster raises the quorum by one, so the tolerance stays the same. Going from an even to an odd count adds one tolerated failure. To tolerate *f* failures, use 2*f* + 1 servers. The fourth server is not useless: it holds another copy and can serve reads. But it adds no failure tolerance, and it is one more server that can fail. This is why clusters (etcd, ZooKeeper, Consul) normally run 3, 5, or 7 servers.

## Limits

- **Assumption:** a failed server stops or goes silent. If servers can send false messages (Byzantine faults), the rule becomes 3*f* + 1 servers.
- This text does not cover how protocols such as Raft and Paxos use quorums to elect a leader and copy the log.
