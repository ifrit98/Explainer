# Why 5 servers survive 2 failures, but 4 servers survive only 1

At first this looks wrong. Four servers are more than three, so surely they should survive more failures. They don't. A 4-server cluster tolerates exactly as many failures as a 3-server cluster: one. To see why, you need one rule that these clusters follow and the reason the rule exists.

## The setting

Many systems keep several copies of the same data on different machines. Databases, configuration stores (etcd, ZooKeeper, Consul) and coordination services all do this. The copies are there so that if a machine dies, the data and the service carry on.

Copies create a new problem, though: **the servers have to agree**. Suppose a client says "set the balance to £50" and, a moment later, another client says "set the balance to £80". Every server has to end up with the same answer, applied in the same order. If some servers think the balance is £50 and others think it is £80, the system is broken, and broken in a quiet way that nobody notices until later.

Protocols such as Raft and Paxos solve this. They differ in detail, but they share one rule:

> **A decision only counts once a majority of the servers have accepted it.**

A majority means *more than half of all the servers in the cluster*, counting the ones that are currently down. That set of servers is called a **quorum**.

## Why a majority, and not "whoever is still up"?

When a server stops responding, the others **cannot tell whether it has crashed or whether the network between them has broken**. Both cases look the same from the outside: messages go out and nothing comes back.

That matters because of the dangerous case, a **network partition**. All the servers are running fine, but the network splits them into groups that can't talk to each other. Each group sees the other group as "dead".

Suppose the rule were "the servers that are still reachable carry on". After a partition, *both* groups would carry on. One side accepts "balance = £50", the other accepts "balance = £80", and each side believes it is the real cluster. This is called **split brain**, and it is exactly the disagreement the system exists to prevent.

The majority rule prevents it with a simple fact about counting:

> **Two majorities of the same group always share at least one member.**

If each of two groups contained more than half the servers, together they would contain more than all of them, which is impossible unless some server is in both. So at most one side of any partition can hold a majority. That side keeps working and the other side stops and waits. Because any two quorums overlap, every decision is seen by at least one server that also took part in the previous decision, and that server is what makes later decisions consistent with earlier ones.

So the majority rule is not an arbitrary choice. It is the smallest group size that guarantees two groups can never both act independently.

## Now count

A cluster keeps working as long as a majority of its servers are still up and can reach each other. So:

- **quorum size** = the smallest number that is more than half of *n*, which is ⌊n/2⌋ + 1
- **failures tolerated** = n − quorum size

**5 servers.** More than half of 5 (2.5) is **3**. You can lose 5 − 3 = **2** servers and still have 3 left, which is a majority. ✅

**4 servers.** More than half of 4 (2) is **3**. Exactly half is *not* a majority, because two groups of 2 could both claim to be "half". You can lose 4 − 3 = **1** server. Lose 2 and only 2 remain, which is not more than half, so the cluster stops accepting writes. ❌

| Servers (n) | Quorum (majority) | Failures tolerated |
|:-----------:|:-----------------:|:------------------:|
| 1 | 1 | 0 |
| 2 | 2 | 0 |
| 3 | 2 | **1** |
| 4 | 3 | **1** |
| 5 | 3 | **2** |
| 6 | 4 | **2** |
| 7 | 4 | **3** |

The pattern is that the number of failures tolerated only goes up when you go from an even number of servers to an odd one. Adding a 4th server to a 3-server cluster raises the quorum from 2 to 3, so the extra server is used up by the larger quorum.

## "But with 4, can't the 2 survivors just carry on?"

This is the natural objection, so here it is in concrete form. Four servers, A, B, C and D. The network splits into {A, B} and {C, D}.

```
   [A] [B]   ║   [C] [D]
             ║
   "C and D  ║   "A and B
    are dead"║    are dead"
```

If 2 out of 4 were enough to continue, both halves would continue. Both would accept writes and their data would diverge. Nobody in either half can tell that the other half is alive, so neither half can safely decide that it is the one to keep going. The only safe behaviour is for **both halves to stop**.

Now try 5 servers split 3–2:

```
   [A] [B] [C]   ║   [D] [E]
   3 of 5:       ║   2 of 5:
   majority,     ║   not a majority,
   keeps going   ║   waits
```

However you split 5, one side always has at least 3, so exactly one side carries on. An odd number can never be divided into two equal halves, and that is the whole difference.

A crash is handled the same way as a partition, because from the inside the two look the same. With 4 servers and 2 crashed, the 2 survivors are in exactly the position of the {A, B} group above. They cannot know the other two aren't alive somewhere, so they must stop.

## What this means in practice

- **Clusters are usually built with odd sizes: 3, 5, sometimes 7.** A 4th or 6th server costs money and adds one more machine that has to acknowledge each write, but it adds no extra failure tolerance.
- **To survive *f* failures you need 2f + 1 servers.** That is 3 servers for 1 failure, 5 for 2 and 7 for 3.
- **Even sizes aren't useless.** The extra server can spread out read load or act as a warm spare. It just doesn't help the cluster stay up.
- **Bigger isn't automatically better.** Every write has to wait for a majority, so larger clusters mean more servers to wait for on each write. Most production systems stop at 5.

## One caveat

All of this assumes that a failed server simply **stops**: it crashes or becomes unreachable, but it never lies. If servers might send wrong or malicious messages (called *Byzantine* failures), the arithmetic gets stricter. Surviving *f* such servers needs 3f + 1 machines. The reasoning is still based on overlapping groups. The overlap just has to be large enough to outvote the liars.

## Summary

A cluster may only act when **more than half** of its servers agree, because any two such groups overlap and so two halves of a broken network can never both make decisions. With 5 servers, more than half is 3, so 2 can fail. With 4 servers, more than half is still 3, so only 1 can fail. Exactly half doesn't count, since the other half could make the same claim.
