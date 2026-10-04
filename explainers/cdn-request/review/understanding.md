# Understanding tests: cdn-request

## Cold read (page, v0.6.0)

Run 2026-10-04, reading as "developers who deploy web apps, know HTTP, and have not modeled latency".

- **Blocking, fixed:** the prediction asked for a time in ms before the page gave the round-trip count, the cost per distance, or the origin's processing time, so it was a guess, not a prediction; the miss row depended on "a connection the edge keeps open", said only further down; the no-CDN distance (taken equal to the edge-to-origin distance) lived only in a script comment; with the edge farther than the origin, the bars showed the CDN slower while the text said "1× faster" and "the gain is small".
- Now: the inputs (3 round trips, about 1 ms per 100 km and back, 20 ms at the origin, the distance assumption) come before the prediction; the instrument opens with the open-connection fact and one line on what to try; the verdict says "slower" when a CDN row is slower; the summary's miss line has its condition; two limit cards state "a new connection for each request" (keep-alive and HTTP/2 need 1 round trip) and the distance assumption.
- **Not applied (edge):** formulas for the hit and miss next to the no-CDN law; the anycast line in Level 4; the log scale of the sliders.
