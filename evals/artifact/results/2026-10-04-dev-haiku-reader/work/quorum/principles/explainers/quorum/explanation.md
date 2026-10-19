# Why 5 servers survive 2 failures, but 4 servers survive only 1

**Short answer.** A cluster accepts a decision only when a strict majority of *all* its servers agree. A majority of 5 is 3, so 2 servers can fail and 3 remain. A majority of 4 is also 3, so only 1 server can fail. The 4th server raises the number of votes you need, but not the number of failures you can absorb.

The rest of this page explains why the rule must be "a majority of all servers", and not something cheaper.

## The problem: one server cannot see why another went silent

A **cluster** is a group of servers that keep identical copies of some data, for example a bank balance. Copies stay identical only if all servers apply the same writes in the same order. So the cluster must *agree* on each write before it accepts it.

Suppose server A stops getting replies from server B. Two different situations produce exactly this observation:

1. B has crashed.
2. B is healthy, but the network between A and B is broken. This is a **partition**: the network splits the servers into groups that cannot reach each other.

A cannot tell these cases apart. In case 2, B may be accepting writes in its own group right now. So any safe rule must assume that silent servers might be alive and making decisions.

## The simplest rule fails

**Rule 1: "Servers that can reach each other decide together."**

Take 5 servers and a balance of $100. The network splits them into a group of 3 and a group of 2.

- The group of 3 accepts "withdraw $80". Its balance is $20.
- The group of 2 accepts "withdraw $90". Its balance is $10.

Each group thinks it is the whole surviving cluster. The two copies now disagree, and $170 left an account that held $100. This failure is called **split brain**.

## The fix: any two deciding groups must share a server

Split brain needs two groups that decide independently. Prevent it like this: require every deciding group to be large enough that **any two such groups share at least one server**. That shared server votes for at most one of two conflicting writes, so at most one of them can pass.

Call the required group size the **quorum**, q. Two groups of size q, inside n servers, must overlap when their sizes add up to more than n:

    q + q > n,   so   q > n/2

The smallest whole number above n/2 is

    q = floor(n/2) + 1          (a strict majority)

Check with 5 servers: q = 3. Two groups of 3 need 6 seats but only 5 exist, so they share at least one server. In the 3|2 split above, only the group of 3 can decide. The group of 2 refuses the $90 withdrawal.

## Why "half" is not enough

**Rule 2: "Half the servers is enough" (q = n/2).**

Take 4 servers split 2|2. Each half has 2 servers, which equals n/2. Both halves decide, and split brain returns. Two groups of 2 fit inside 4 servers with no overlap. So 4 servers need q = 3, the same as 5 servers.

## From quorum to failure tolerance

The cluster keeps working while at least q servers are alive and connected. So it tolerates

    f = n − q   failures.

> **Predict before you read the table:** how many failures does a 6-server cluster tolerate?

| Servers n | Quorum q | Failures tolerated f |
|---|---|---|
| 3 | 2 | 1 |
| **4** | **3** | **1** |
| **5** | **3** | **2** |
| 6 | 4 | 2 |
| 7 | 4 | 3 |

Each step from an odd n to the next even n adds 1 to q and 0 to f. This is the answer to the original question: going from 4 to 5 servers adds a server without raising q, so f rises from 1 to 2.

## What "survive" means, and where it stops

- **Holds:** 5 servers, 2 crash. 3 remain, which equals q. The cluster keeps accepting writes.
- **Breaks:** 5 servers, 3 crash. 2 remain, fewer than q. The cluster stops accepting writes until a server returns.

In the second case the cluster is *unavailable*, but it is still *correct*. It refuses to decide rather than risk split brain. A majority quorum trades availability for consistency on purpose.

## What the even server costs you

An even server does not just fail to help. It adds one more machine that can fail, and the tolerance stays the same. Assume each server is down 1% of the time, independently (an illustrative assumption). The chance that the cluster lacks a quorum is then:

| Servers | Down when | P(no quorum) |
|---|---|---|
| 3 | 2 or more down | ≈ 0.030% |
| 4 | 2 or more down | ≈ 0.059% |
| 5 | 3 or more down | ≈ 0.001% |

A 4-server cluster loses its quorum about twice as often as a 3-server cluster. This is why production clusters (etcd, ZooKeeper, Consul) normally use 3, 5, or 7 servers.

## Scope

This page assumes servers fail by stopping. Servers that send false messages (**Byzantine faults**) need a larger cluster: n ≥ 3f + 1, so 4 servers to survive 1 such server. The algorithms that run the votes, such as Raft and Paxos, are also out of scope; they all rest on the majority-overlap rule above.
