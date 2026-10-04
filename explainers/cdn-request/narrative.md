# Narrative: cdn-request

> Pass 3. The page follows these beats, top to bottom.

## 1. Reader before and after

- **Before:** Developers who deploy web apps. They know HTTP. They have not modeled latency.
- **After:** "A new HTTPS request costs about 3 round trips, and each costs time in proportion to distance; a CDN puts them on the short path to a nearby edge, and a miss adds only one long round trip on a connection that is already open."

## 2. Question and motive

- **Question:** why does a CDN cut the time of a request, and when does it not help? Answer in the lede.
- **Why care:** distance, not bandwidth, sets the time of a small request.
- **Why this approach:** count round trips, and price each one by distance.

## 3. Introduction ledger

| Reference | Means | Grounded by | Beat |
|---|---|---|---|
| round trip | one message there and its reply back | 1 ms per 100 km of fiber | 1, 4 |
| edge, origin | the CDN server near the client; the app's own server | 300 km and 6,000 km | 2 |
| hit, miss | the edge has a fresh copy / must ask the origin | the three paths | 3 |
| TTL | how long a cached copy stays fresh | `Cache-Control: max-age` | 4 |

## 4. Beats

| # | Kind | Reader's question | Bridge | Shown | Reader now knows |
|---|---|---|---|---|---|
| 1 | answer | Why is it faster? | — | lede | round trips move onto a short path |
| 2 | picture | Where are the distances? | so | client, edge, origin | the two distances |
| 3 | test | How long without a CDN? | — | predict gate, then the three paths | the cost of 3 long round trips |
| 4 | mechanism | What happens in order? | so | Level 2 steps | the sequence |
| 5 | why | Why does distance multiply? | but why | Level 3 | 3 × distance |
| 6 | implementation | What makes a hit? | — | Level 4 | cache key, TTL, uncached pages |
| 7 | limits | What do the numbers leave out? | but | tags | the assumptions |
| 8 | recap | — | — | three facts | the takeaway |

## 7. Close the loop

- **Answer:** the summary repeats the lede, and adds when a CDN does not help (a miss, uncached pages).
