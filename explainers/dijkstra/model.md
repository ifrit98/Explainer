# Semantic model: Dijkstra's shortest paths

## Central question

How does Dijkstra's algorithm find the shortest distance from one node to every other node, and why is each distance final when the algorithm settles it?

## Audience and prior knowledge

Developers who know what a graph is. No proof background.

## Entities

| Entity | Definition | Status |
|---|---|---|
| Graph | Nodes A–F joined by edges with lengths (weights). | given |
| Distance estimate | The shortest length found so far from A to a node. Starts at ∞ (A starts at 0). | definition |
| Settled node | A node whose estimate is final. | definition |
| Relaxation | Through node u, if dist(u) + w(u, v) < dist(v), set dist(v) to the smaller value. | definition |
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

## Causal chain (why a settled distance is final)

Every other path to the settled node must leave the settled region through some unsettled node, whose estimate is already at least as large. With no negative edge lengths, the rest of that path cannot make it shorter.

## Epistemic status

- **Assumption (required):** every edge length is ≥ 0. With a negative length, a settled distance can be wrong.
- **Mathematical fact:** under that assumption, each settled estimate equals the true shortest distance.
- **Implementation:** a priority queue finds the smallest estimate quickly; this video shows the order, not the data structure.

## Confusion points

- "The first path found is the shortest." → No: B is first reached at 4, then improved to 3 through C.
- "Dijkstra works with negative lengths." → No.

## Representation decision

- **Stage:** 4. **Reason:** an algorithm that runs. The viewer must see estimates change and nodes settle in order, with the graph fixed in place.
