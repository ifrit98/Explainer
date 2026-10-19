# Model: majority quorum and failure tolerance

## Central question
Why does a 5-server cluster survive 2 failures, but a 4-server cluster survives only 1?

## Reader
Technical, new to distributed systems. Knows integer division, basic probability, what a server and a network are.

## Entities and definitions
- Cluster: n servers that must agree on one sequence of decisions (for example, writes to a database).
- Failure (crash): a server stops responding. It does not send wrong messages.
- Partition: the network splits the servers into groups that cannot reach each other.
- Quorum: the minimum number of servers that must agree before the cluster accepts a decision.
- Majority quorum: q = floor(n/2) + 1.
- Tolerated failures: f = n - q = floor((n-1)/2).

## Central causal chain
1. A server cannot tell a crashed peer from a peer that is cut off by a partition.
2. So the rule must stay safe if the "missing" servers are alive and deciding on their own.
3. Safety requires that two groups which can each decide must share at least one server. That server refuses to approve conflicting decisions.
4. Two groups of size q always share a server only if q + q > n, so q > n/2. The smallest such q is floor(n/2) + 1.
5. The cluster keeps working while at least q servers are alive, so it survives n - q failures.
6. n = 5: q = 3, f = 2. n = 4: q = 3, f = 1. The 4th server raises q but not f.

## Alternative (fails)
- "Any connected group decides": 5 servers split 3|2; both sides accept conflicting writes (split brain).
- "Half is enough" (q = n/2): 4 servers split 2|2; both halves have 2 = q; both decide.

## Guarantee, two cases
- Holds: 5 servers, 2 crash; 3 remain = q; cluster continues.
- Breaks: 5 servers, 3 crash; 2 remain < q; cluster stops accepting decisions. It stays consistent but unavailable.

## Quantity meaning
Independent failure probability p = 0.01 per server; P(cluster lacks quorum):
- n=3: ~0.00030; n=4: ~0.00059 (worse than 3); n=5: ~0.0000099.

## Epistemic status
- Steps 3–6: mathematical consequence.
- Crash-only failures: assumption.
- Independent failures with p = 0.01: assumption for illustration.

## Scope
Not covered: servers that lie (Byzantine faults, need n >= 3f + 1); leader election details (Raft, Paxos); weighted or flexible quorums.
