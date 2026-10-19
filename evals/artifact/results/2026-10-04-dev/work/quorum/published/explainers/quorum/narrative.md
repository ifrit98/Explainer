# Narrative: quorum

> Pass 3. `model.md` says what is true. This file says the path a first-time reader takes to it.

## 1. Reader before and after

- **Before:** a technical reader (school maths and science, basic programming). Knows servers, networks, and that data can be copied to several machines. Does not know quorum, partition, split brain, Raft or Paxos.
- **After:** "A cluster decides a change only when more than half of all its servers accept it, because any two such groups share a server. 5 needs 3, so it can lose 2. 4 also needs 3, so it can lose only 1."

## 2. Question and motive

- **Question:** Why does a cluster of 5 servers survive 2 failures, but a cluster of 4 survives only 1? Result in words: both clusters need 3 servers to agree, because the rule is "more than half of all servers", and more than half of 4 is 3, the same as for 5.
- **Why care:** it is surprising: the 4th server costs money but buys nothing. It decides how you size etcd, ZooKeeper, or any Raft cluster.
- **Why this approach:** ask "why not let the 2 survivors go on?" The answer (they cannot tell a crash from a cut cable) forces the majority rule; the counting then follows.

## 3. Introduction ledger

| Reference | Means | Grounded by (a concrete instance) | Beat |
|---|---|---|---|
| cluster | n servers with copies of the same data that must agree on each change | 5 servers A–E | 1 |
| accept | a server stores a proposed change on disk and replies "yes" | A, B, C accept x = 1 | 2 |
| decide | a change becomes final because a quorum accepted it | x = 1 decided after 3 accepts | 2 |
| quorum size / quorum | the number needed (3) / a group that big ({A,B,C}) | n = 5 | 2 |
| majority size | floor(n/2) + 1 of all configured servers | 5 → 3, 4 → 3 | 4 |
| partition | network splits servers into groups that cannot reach each other | {A,B} / {C,D} | 3 |
| split brain | two groups decide different changes | x = 1 vs x = 2 | 3 |
| tolerance | failed servers the cluster can lose and still decide | 5 → 2, 4 → 1 | 6 |
| x = 1, x = 2 | two conflicting changes to one value | — | 2 |

## 4. Beats

| # | Kind | Reader's question | Bridge | Shown | Said | Reader now knows |
|---|---|---|---|---|---|---|
| 1 | hook | Why does a cluster of 5 servers survive 2 failures, but a cluster of 4 only 1? | — | question as title; answer in bold | "A cluster of n servers keeps copies of the same data. It decides a change only when more than half of all n servers accept it. For 5 servers that is 3, so 5 − 3 = 2 servers can fail. For 4 servers it is also 3, so only 4 − 3 = 1 can fail. The rest explains why the rule is 'more than half'." | the question and the result |
| 2 | name | What does "accept" and "decide" mean? | so | 5 servers A–E; change x = 1 accepted by A, B, C | "A client proposes the next change, for example x = 1. A server accepts it when it stores it on disk and replies yes. Once 3 servers (A, B, C) accept, the change is decided: final. The number needed (here 3) is the quorum size; a group that big ({A, B, C}) is a quorum. If too few servers answer, the cluster stops: it keeps every decided change but decides no new one. The cluster decides changes one at a time, in order: change 1, change 2, and so on. For each position in that order, a server accepts only one change." | accept, decide, quorum size, quorum, stop, one-per-position rule |
| 3 | objection | In a 4-server cluster with 2 down, why can't the other 2 go on? | but | 4 servers; A waits 500 ms for D; partition {A,B}/{C,D} | "Now take a cluster of 4 servers, A–D, where C and D stop answering. Why can A and B not go on? A sends to D and gets no reply in 500 ms. D may have crashed. Or the network between them is cut (a partition) and D still runs, talking to C. A sees the same silence in both cases. Letting A and B go on means quorum size 2. Then A, B decide x = 1 for change 7 while C, D decide x = 2 for change 7. The copies now disagree for good: split brain." | why a quorum of half breaks |
| 4 | mechanism | What quorum size is safe? | therefore | 5 servers: {A,B,C} and {C,D,E}; C refuses x = 2 | "Make the quorum size more than half of all n servers: the majority size, floor(n/2) + 1. Back to 5 servers. Two groups of 3 hold 6 memberships, but there are only 5 servers, so at least one server is in both groups, here C. C already accepted x = 1 for change 7, so it refuses x = 2 for change 7, and x = 2 gets only 2 of the 3 votes it needs." | the majority rule and why it works |
| 5 | test | (predict) 5 servers split into {A,B,C} and {D,E}: what does each side do? | so | prediction prompt, then answer | "A, B, C have 3 ≥ 3 and keep deciding. D, E have 2 < 3 and stop. The copies cannot disagree. Note: count more than half of all 5 configured servers. If D and E counted 'more than half of the 2 servers we can reach', they would decide too." | the rule applied |
| 6 | generalize | So how many failures can a cluster of n take? | therefore | table n = 3..7 with majority size and tolerance | "Tolerance is how many servers can fail while the cluster still decides: n − majority size. Read the table: 4 and 5 both need 3. Adding a 4th server to 3, or a 6th to 5, raises the majority size by one, so tolerance stays the same; each change must also wait for one more accept." | the general pattern |
| 7 | close | — | so | — | "5 survives 2 and 4 survives 1 because both need 3 servers, and 3 is the smallest group that must share a server with any other group. Use odd cluster sizes. This assumes servers crash but never lie." | the answer and its limits |

## 5. Concrete to symbol

floor(n/2) + 1 appears after the 5 → 3 and 4 → 3 instances; checked against 6 → 4, 7 → 4.

## 6. Links between representations

The table rows for n = 4 and n = 5 repeat the numbers from beats 1 and 4.

## 7. Close the loop

- **Answer:** both clusters need 3 servers to decide; 5 has 2 spare, 4 has 1 spare.
- **General argument:** more than half is the smallest quorum where any two quorums share a server; the shared server stops two groups deciding different changes.
- **Payoff:** choose odd cluster sizes. Scope: lying servers, leader election, reads.
