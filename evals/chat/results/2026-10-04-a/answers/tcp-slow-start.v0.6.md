# Why does a new TCP connection send slowly at first?

_v0.6_

# Why a new TCP connection starts slowly

A new TCP connection starts slowly because the sender does not know how much data the network path can carry. It starts with a small amount and doubles that amount each round trip until it finds the limit. This mechanism is called **slow start**.

## The problem: the sender does not know the path capacity

Between sender and receiver are links and routers that other traffic also uses. Each router has a queue of limited size. If packets arrive faster than the router can forward them, the queue fills and the router drops packets.

The sender cannot see these queues. It can only observe two signals:

- **Acknowledgments (ACKs).** The receiver sends an ACK for data that arrived.
- **Losses.** Data that gets no ACK was probably dropped.

## The mechanism: a congestion window that grows

The sender keeps a **congestion window** (cwnd). This is the maximum amount of unacknowledged data it allows itself to have in flight.

1. Start with a small cwnd. Modern systems use 10 segments, about 14.6 KB (10 × 1460-byte segments; RFC 6928).
2. For each ACK that arrives, add 1 segment to cwnd.
3. A full window of ACKs arrives each round-trip time (RTT), so cwnd **doubles every RTT**: 10 → 20 → 40 → 80 …
4. Stop doubling when a packet is lost or when cwnd reaches a threshold (ssthresh). After that, grow by only 1 segment per RTT. This phase is called congestion avoidance.

The ACKs act as a probe. Each ACK shows that the path delivered one more packet, so the sender can safely add more.

## Worked example

Take a path with 100 Mbit/s capacity and a 50 ms RTT. To keep this path full, the sender needs this much data in flight:

> 100,000,000 bit/s × 0.05 s ÷ 8 = 625,000 bytes ≈ 428 segments

This value is the **bandwidth-delay product**. Slow start reaches it as follows:

| RTT | cwnd (segments) | Throughput (approx.) |
|---|---|---|
| 1 | 10 | 2.3 Mbit/s |
| 2 | 20 | 4.7 Mbit/s |
| 3 | 40 | 9.3 Mbit/s |
| 4 | 80 | 19 Mbit/s |
| 5 | 160 | 37 Mbit/s |
| 6 | 320 | 75 Mbit/s |
| 7 | 640 → capped by path | 100 Mbit/s |

The connection takes about 7 RTTs (≈ 350 ms) to reach full speed. During that time it uses only part of the link. This delay is the "slow" in slow start.

## Why not a different start?

**Alternative 1: send at full speed immediately.** Suppose the sender puts 428 segments in flight at once, but another flow already uses half the link. The bottleneck router then gets about twice the traffic it can forward. If its queue holds 100 packets, it drops hundreds of packets. The sender retransmits them, which adds still more traffic. In 1986, this behavior caused congestion collapse on the early Internet: throughput on some links fell by a factor of about 1000. Van Jacobson introduced slow start in 1988 to stop it. *(Historical fact.)*

**Alternative 2: grow slowly, by 1 segment per RTT.** This approach is safe but too slow. To grow from 10 to 428 segments takes 418 RTTs, about 21 seconds on the example path.

Doubling is the compromise. It reaches any capacity in a number of RTTs proportional to the logarithm of that capacity. Its overshoot past the limit is at most one window, so a loss gives a fast and bounded signal.

## Where the cost shows

- **Short transfers rarely reach full speed.** A 100 KB web response needs 70 segments. Slow start sends 10 + 20 + 40 = 70, which takes 3 RTTs. The link speed has almost no effect, and latency sets the transfer time. This is one reason why HTTP/2 and HTTP/3 reuse one connection, and why CDNs place servers close to users.
- **High-latency paths suffer most.** On a 200 ms satellite or intercontinental path, each doubling step costs 200 ms.

## Scope

This answer leaves out these topics:

- The receiver's own limit (the receive window). The sender uses the smaller of the two windows.
- Fast retransmit and fast recovery.
- Other congestion-control algorithms. CUBIC, the Linux default, keeps slow start but changes the growth after it. BBR estimates bandwidth and RTT directly and has its own start-up phase.
