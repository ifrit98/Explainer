# Why does a cluster of 5 servers survive 2 failures, but a cluster of 4 survives only 1?

**A cluster decides a change only when more than half of all its servers accept the change. For 5 servers, more than half is 3, so 5 − 3 = 2 servers can fail. For 4 servers, more than half is also 3, so only 4 − 3 = 1 server can fail.** <!-- claim: count-5-4 -->

The rest of this page explains why the rule must be "more than half".

## The rule

A *cluster* is a group of n servers that keep copies of the same data. Take 5 servers, A to E. A client proposes a change, for example x = 1.

- A server *accepts* the change when it stores the change on disk and replies "yes".
- When enough servers accept, the change is *decided*: it is final.
- The number of accepts needed is the *quorum size*. A group of that many servers, for example {A, B, C}, is a *quorum*.
- A server *fails* when it stops answering: it crashed, or the network cannot reach it.

The cluster decides changes one at a time, in order: change 1, change 2, and so on. For each position in that order, a server accepts only one change. The examples below use change 7, an arbitrary position.

If fewer than a quorum of servers answer, the cluster *stops*. It keeps every decided change, but it decides no new change until enough servers return. <!-- claim: stop-not-loss --> <!-- claim: quorum-rule -->

## Why not let the survivors go on?

Take a cluster of 4 servers, A to D. C and D fail. Why can A and B not go on alone?

A sends a message to D and gets no reply. Maybe D crashed. Or maybe the network between them is cut, and D still runs and talks to C. This split of the network into groups that cannot reach each other is a *partition*. A sees the same silence in both cases, however long it waits, so A cannot know which case is true. <!-- claim: cannot-tell -->

Letting A and B go on means quorum size 2. Now suppose the cause is a partition, {A, B} on one side and {C, D} on the other:

| Group | Change it accepts as change 7 | Number of accepts | Quorum size | Result |
|---|---|---|---|---|
| A, B | x = 1 | 2 | 2 | decided |
| C, D | x = 2 | 2 | 2 | decided |

Both groups decide, and the copies now disagree for good. This is *split brain*. It happens because two groups of 2 among 4 servers need not share a server. So the quorum size must be more than half of n: then two groups cannot both decide. <!-- claim: why-majority -->

## Why more than half works

More than half of all n servers is the *majority size*: floor(n/2) + 1. For 5 servers it is 3; for 4 servers it is also 3. Clusters set the quorum size to the majority size: a larger quorum is also safe, but it lets fewer servers fail.

Two quorums each hold more than half of the servers, so together they list more than n servers. Some server must therefore be in both. For 5 servers, {A, B, C} and {C, D, E} list 3 + 3 = 6 > 5, and C is in both. For 4 servers, two groups of 3 list 6 > 4. <!-- claim: overlap -->

The shared server blocks split brain. Suppose A, B, C accepted x = 1 for change 7, so x = 1 is decided. Later, C, D, E are asked to accept x = 2 for change 7. C already accepted x = 1 for that position, so C refuses. Then x = 2 gets only 2 accepts, from D and E, and it needs 3.

This depends on one assumption: a server remembers what it accepted, even after a restart. If C restarts with an empty disk and accepts x = 2, then C, D, E decide x = 2 too, and split brain returns.

**Predict:** the network splits 5 servers into {A, B, C} and {D, E}. What does each side do?

A, B, C have 3 accepts, and 3 ≥ 3, so they keep deciding. D and E have 2, and 2 < 3, so they stop. The copies cannot disagree.

Count more than half of *all* configured servers, failed or not. If D and E counted "more than half of the 2 servers we can reach", that would be 2, and they would decide x = 2 while A, B, C decide x = 1. <!-- claim: why-all-n -->

## Counting failures

*Tolerance* is how many servers can fail while the cluster still decides changes:

tolerance = n − majority size

| Servers n | Majority size | Tolerance |
|---|---|---|
| 3 | 2 | 1 |
| 4 | 3 | 1 |
| 5 | 3 | 2 |
| 6 | 4 | 2 |
| 7 | 4 | 3 |

With 4 servers and 2 failed, only 2 servers answer, and 2 < 3: the cluster stops.

A tolerance of 1 means a second failure stops the cluster. A tolerance of 2 means one server can be off for an upgrade while another one fails.

Going from an even n to the next odd n keeps the majority size (4 → 5: both 3), so tolerance grows by 1. Going from an odd n to the next even n raises the majority size by 1 (5 → 6: 3 → 4), so tolerance stays the same. The extra server only makes each change wait for one more accept. That is why clusters usually have an odd number of servers. <!-- claim: even-adds-nothing -->

## Answer

Both clusters need 3 accepts to decide a change, because 3 is more than half of 4 and of 5. Any two groups of more than half share a server, and that server stops them from deciding different changes. 5 servers have 2 to spare. 4 servers have only 1.

## Limits

- **Assumed:** servers crash or become unreachable, but never send a false "yes". Servers that lie need larger clusters.
- **Simplified:** in real protocols (Raft, Paxos), the shared server does more than refuse. It reports x = 1 to the new group, and the new group keeps x = 1.
- **Not covered:** how servers detect a failure, how the stopped side catches up when the network heals, and how reads work.
