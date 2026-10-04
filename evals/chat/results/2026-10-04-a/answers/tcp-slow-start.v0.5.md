# Why does a new TCP connection send slowly at first?

_v0.5_

A new TCP connection sends slowly at first because the sender does not know how much data the network path can carry. It starts with a small amount and doubles the amount on each round trip until it sees a sign of congestion. This mechanism is called **slow start**.

## The problem

- A **segment** is one TCP packet of data, typically about 1,460 bytes.
- The **round-trip time (RTT)** is the time for a segment to reach the receiver and for its acknowledgment to come back.
- The **congestion window (cwnd)** is the number of segments the sender may have in flight before it must wait for acknowledgments.

The path between two hosts crosses routers. Each router has a finite buffer. If the sender sends more than the slowest link can forward, the buffer fills and the router drops packets. The sender cannot see the routers. It learns the capacity only from acknowledgments and losses.

## Why not send everything at once?

Suppose a 1 MB file is about 685 segments, and a router on the path can queue 100 packets. If the sender sends all 685 segments at once, the router drops most of them. The sender must then retransmit them. Every connection that shares the router does the same, so the network carries mostly retransmissions and delivers little useful data.

This failure happened in practice. In 1986, the link between LBL and UC Berkeley fell from 32 kbit/s to about 40 bit/s (observation). Van Jacobson added slow start to TCP in 1988 to stop it (established fact).

## How slow start works

1. Start with a small cwnd. Modern TCP uses 10 segments (RFC 6928), about 14.6 KB.
2. For each acknowledged segment, increase cwnd by one segment. As a result, cwnd doubles each RTT.
3. Stop doubling when cwnd reaches a threshold (ssthresh) or when a packet is lost. After that, TCP grows cwnd slowly, by about one segment per RTT. This phase is called **congestion avoidance**.

**Worked example:** 1 MB (685 segments), RTT 50 ms, no loss.

| RTT | cwnd (segments) | Total sent |
|---|---|---|
| 1 | 10 | 10 |
| 2 | 20 | 30 |
| 3 | 40 | 70 |
| 4 | 80 | 150 |
| 5 | 160 | 310 |
| 6 | 320 | 630 |
| 7 | 640 | 685 ✓ |

The transfer takes 7 RTTs, which is 350 ms. On a 100 Mbit/s link, the same bytes need only 80 ms of transmission time. The difference is the cost of slow start.

## Why doubling, and not +1 per RTT?

Doubling finds capacity in a few steps, because the number of steps grows with log₂ of the capacity. If cwnd grew by one segment each RTT (10, 11, 12, …), the same 685 segments would take 29 RTTs, which is 1.45 s instead of 350 ms. Slow start is "slow" only compared with sending everything at once. It is the fastest safe way to probe the path.

## Consequences

- **Short transfers suffer most.** A small web page can finish in 2–3 RTTs, during which the connection never reaches full speed. For short transfers, latency matters more than bandwidth.
- **High-RTT paths suffer more.** Each doubling costs one RTT. A 200 ms satellite path ramps up four times slower than a 50 ms path.
- **Connection reuse helps.** HTTP keep-alive and HTTP/2 reuse a connection after its cwnd has grown, so they skip the ramp-up.

**Out of scope:** the receive window (the receiver's limit, separate from cwnd), loss recovery details (fast retransmit), and newer controllers such as BBR, which estimate bandwidth directly instead of waiting for loss. QUIC uses the same slow-start idea over UDP.
