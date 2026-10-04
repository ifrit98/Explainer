# Semantic model: why a CDN makes a request faster

## Central question

Why does a content delivery network (CDN) cut the time of a web request, and when does it not help?

## Audience and prior knowledge

Developers who deploy web apps. They know HTTP. They have not modeled latency.

## Entities

| Entity | Definition | Status |
|---|---|---|
| Client | The browser that makes the request. | given |
| Edge server | A CDN server near the client. It keeps cached copies of responses. | definition |
| Origin server | The server that holds the real content. | definition |
| Round trip (RTT) | Time for a message to go to a server and for the reply to come back. | definition |
| Cache hit / miss | The edge has a fresh copy / must fetch from the origin. | definition |
| TTL | How long a cached copy stays fresh (set by Cache-Control). | definition |

## Causal chain

```text
a new HTTPS request costs several round trips (TCP, TLS, request)
→ each round trip costs time proportional to distance
→ an edge near the client makes those round trips short
→ on a hit, the long trip to the origin never happens; on a miss, it happens once, over a connection the edge keeps open
```

## Quantities (estimates — the model, not measurements)

| Quantity | Value | Status |
|---|---|---|
| RTT per distance in fiber | 1 ms per 100 km | estimate: light in fiber ≈ 200,000 km/s, straight path |
| Round trips for a new HTTPS request | 3 (TCP 1, TLS 1.3 1, request 1) | fact for TLS 1.3 without 0-RTT |
| Edge processing | 1 ms | assumption |
| Origin processing | 20 ms | assumption |

Default scenario: client 300 km from the edge, origin 6,000 km away.

| Path | Formula | Time |
|---|---|---|
| No CDN | 3 × 60 ms + 20 ms | 200 ms |
| CDN, cache miss | 3 × 3 ms + 1 ms + 60 ms + 20 ms | 90 ms |
| CDN, cache hit | 3 × 3 ms + 1 ms | 10 ms |

## Alternative states

| State | Effect |
|---|---|
| Cache hit | Origin not contacted. Time depends only on the client–edge distance. |
| Cache miss | One extra origin round trip, on the edge's open connection (no new handshakes). |
| Client far from every edge | Little gain: the edge is not much closer than the origin. |
| Uncacheable response (personal data) | Every request is a miss. |

## Epistemic status

- **Fact:** light in fiber travels at about two thirds of its speed in vacuum.
- **Assumption:** straight-line paths. Real routes are longer, so real RTTs are larger.
- **Assumption:** the client to origin distance is about the edge to origin distance (the edge is near the client).
- **Simplification:** DNS lookup, bandwidth, and TLS session resumption are left out.

## Confusion points

- "A CDN only helps with bandwidth." → The larger effect for small requests is round trips: handshakes happen on the short path.
- "A miss is as slow as no CDN." → No. The edge already has a connection to the origin, so a miss adds one long round trip, not three.

## Representation decision

- **Stage:** 3 (interactive). **Reason:** two distances and one cache state set the result. The reader learns by moving them and comparing the three paths side by side. Levels: L1 what / L2 how (the steps) / L3 why (round trips × distance) / L4 implementation (cache keys, TTL, anycast).
