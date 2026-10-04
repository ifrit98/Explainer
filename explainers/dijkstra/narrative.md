# Narrative: dijkstra

> Pass 3. Written after the video (v0.6.0 backfill); the video follows these beats.

## 1. Reader before and after

- **Before:** Developers who know what a graph is. No proof background.
- **After:** "Dijkstra settles the unsettled node with the smallest estimate, then relaxes its edges; a settled estimate is final because any other path must leave the settled nodes somewhere and already costs at least that much, as long as no length is negative."

## 2. Question and motive

- **Question:** how does Dijkstra find the shortest distance to every node, and why is it safe to make the smallest estimate final?
- **Why care:** routing and maps run on it, and its one assumption (no negative lengths) is the one people break.
- **Why this approach:** run it on one six-node graph, step by step, then stop at one settle step and check why it is safe.

## 3. Introduction ledger

| Reference | Means | Grounded by | Beat |
|---|---|---|---|
| estimate | the shortest length found so far; can still drop | A 0, others ∞ | 1 |
| distance | the final value of an estimate | "a settled estimate is final: it is the node's distance" | 1 |
| settle, relax | make an estimate final; check whether a path through the settled node is shorter | the two-line rule list | 1 |
| u, v | the settled node and its neighbor in the relax test | estimate(u) + length < estimate(v)? | 1 |
| orange number, green fill, yellow ring, yellow edge | an estimate; settled; the current node; the remembered "came from" edge | the first settle step | 2 |
| dashed box | the settled nodes | A and C, before B settles | 4 |

## 4. Beats

| # | Kind | Reader's question | Bridge | Said | Reader now knows |
|---|---|---|---|---|---|
| 1 | setup | What does it do? | — | start node A, lengths ≥ 0, estimates, the two steps | the rule |
| 2 | instance | What happens first? | so | settle A; C at two; B drops to three through C | relaxing |
| 3 | why | Why the smallest estimate? | but why | settling B at four would be wrong | the order |
| 4 | guarantee | Can a later path beat three? | but | follow a path to its first node outside {A, C}: B itself, or D (≥ 10) or E (≥ 12) | finality |
| 5 | instance, test | And then? | so | D at eight, predict E at ten, F at thirteen | the run |
| 6 | payoff | Where is the path? | so | follow the remembered edges back from F | the path |
| 7 | counterexample | Why lengths ≥ 0? | but | C→B −2 gives one after B is final at two | the assumption |

## 7. Close the loop

- **Answer:** the run gives every distance; the counterexample shows the one assumption the finality argument used.
