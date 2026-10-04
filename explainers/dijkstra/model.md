# Semantic model: Dijkstra's shortest paths

## Central question

How does Dijkstra's algorithm find the shortest distance from one node to every other node, and why is each distance final when the algorithm settles it?

## Audience and prior knowledge

Developers who know what a graph is. No proof background.

## Entities

| Entity | Definition | Status |
|---|---|---|
| Graph | Nodes A–F joined by undirected edges with lengths: A–B 4, A–C 2, B–C 1, B–D 5, C–D 8, C–E 10, D–E 2, D–F 6, E–F 3. | given |
| Distance estimate | The shortest length found so far from A to a node. Starts at ∞ (A starts at 0). | definition |
| Settled node | A node whose estimate is final. | definition |
| Relaxation | Through node u, if dist(u) + w(u, v) < dist(v), set dist(v) to the smaller value and record u as v's predecessor. If it is not smaller, keep dist(v). | definition |
| Settled region | The set of settled nodes. | definition |
| Predecessor | The neighbor that gave a node its current estimate. | definition |
| Shortest-path tree | For each node, the edge that last improved its estimate. | consequence |

## Temporal sequence

1. Set dist(A) = 0 and every other estimate to ∞.
2. Settle the unsettled node with the smallest estimate.
3. Relax every edge from it to an unsettled neighbor.
4. Repeat 2–3 until every node is settled.

## Quantities — the run on this graph

| Settle | at | Relaxations (new estimate) |
|---|---|---|
| A | 0 | B 4, C 2 |
| C | 2 | B 3 (was 4), D 10, E 12 |
| B | 3 | D 8 (was 10) |
| D | 8 | E 10 (was 12), F 14 |
| E | 10 | F 13 (was 14) |
| F | 13 | — |

Shortest path to F: A → C → B → D → E → F, length 2 + 1 + 5 + 2 + 3 = 13.

## Why this form

| Operation | Simplest alternative | What the alternative breaks |
|---|---|---|
| Settle the unsettled node with the smallest estimate | settle nodes in the order they are reached (breadth-first) | A reaches B with 4 and C with 2. Settling B first fixes it at 4; the path A → C → B = 2 + 1 = 3 is found too late. |
| Relax with dist(u) + w < dist(v) | take the first estimate a node gets | B's first estimate is 4; the relaxation through C lowers it to 3. |

## Concrete cases

| Claim | Holds here | Breaks here, without its assumption |
|---|---|---|
| A settled distance is final (lengths ≥ 0). | B settles at 3. The unsettled estimates are D 10, E 12, F ∞, all ≥ 3. Any other path to B leaves the settled region {A, C, B} through one of them and only adds lengths ≥ 0, so it costs at least 10. | Directed edges A→B 2, A→C 3, C→B −2. B settles at 2. Then C, at 3, gives 3 + (−2) = 1 < 2, after B is already final. The true distance to B is 1. |
| Relaxation, step by step. | Settle D at 8: E 8 + 2 = 10 < 12 → 10; F 8 + 6 = 14 < ∞ → 14. Settle E at 10: F 10 + 3 = 13 < 14 → 13. | — |
| Reading the path. | Follow predecessors back from F: E, D, B, C, A. Reversed: A → C → B → D → E → F, length 13. | — |

## Causal chain (why a settled distance is final)

Every other path to the settled node must leave the settled region through some unsettled node, whose estimate is already at least as large. With no negative edge lengths, the rest of that path cannot make it shorter.

## Epistemic status

- **Assumption (required):** every edge length is ≥ 0. With a negative length, a settled distance can be wrong.
- **Mathematical fact:** under that assumption, each settled estimate equals the true shortest distance.
- **Implementation:** a priority queue finds the smallest estimate quickly; this video shows the order, not the data structure.

## Confusion points

- "The first path found is the shortest." → No: B is first reached at 4, then improved to 3 through C.
- "Dijkstra works with negative lengths." → No.

## Scope

- **Out of scope:** running time. With a binary-heap priority queue it is O((V + E) log V).
- **Out of scope:** graphs with negative lengths. Use Bellman–Ford.
- **Out of scope:** A* search, which adds a distance-to-goal estimate to guide the order.
- **Stated, not shown:** ties may be settled in any order with the same final distances; a node that no path reaches keeps ∞.

## Representation decision

- **Stage:** 4. **Reason:** an algorithm that runs. The viewer must see estimates change and nodes settle in order, with the graph fixed in place.
