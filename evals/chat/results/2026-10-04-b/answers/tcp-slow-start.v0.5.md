# Why does a new TCP connection send slowly at first?

_v0.5_

A new TCP connection sends slowly at first because the sender does not know how much data the network path can carry. The sender starts with a small amount, then increases it fast until the network signals that it is full. This mechanism is called **slow start**.

## The mechanism

1. The sender keeps a **congestion window** (cwnd). This is the amount of unacknowledged data it may have in flight.
2. A new connection starts with a small cwnd. Modern Linux and most servers use 10 segments, about 14.6 KB (RFC 6928).
3. Each acknowledgment that comes back increases cwnd by one segment. In practice, cwnd doubles every round-trip time (RTT).
4. Growth continues until one of these events occurs:
   - A packet is lost. The sender treats this as a congestion signal and cuts cwnd.
   - cwnd reaches a threshold (ssthresh). Growth then becomes linear (**congestion avoidance**).
   - cwnd reaches the receiver's advertised window. That is a separate limit set by the receiver, not by the network.

## Worked example

Assume a path that can carry 100 segments per RTT.

| RTT | cwnd (segments) | Result |
|---|---|---|
| 1 | 10 | fits |
| 2 | 20 | fits |
| 3 | 40 | fits |
| 4 | 80 | fits |
| 5 | 160 | exceeds 100 → router buffer overflows → loss |

After the loss, the sender reduces cwnd and grows it slowly. It has found the capacity in 5 RTTs.

## Why not start at full speed?

The sender cannot see the bottleneck. The sender's own link may be 1 Gbit/s while a link in the middle carries far less. Suppose it sends 1,000 segments at once into the 100-segment path above. The bottleneck router queues what it can and drops the rest. Every other connection through that router also loses packets. In 1986, this behavior caused **congestion collapse** on the early Internet: links were fully busy, but most traffic was retransmissions, and useful throughput fell by about 1000×. Slow start (Van Jacobson, 1988) was the fix.

## Why double, and not add one segment per RTT?

Linear growth from 10 segments needs 90 RTTs to reach 100 segments. Doubling needs about 4. Exponential growth finds the capacity in a number of RTTs that grows with log₂(capacity). The start is careful, but the search is fast.

## What this costs you

Short transfers spend most of their time in slow start. Take a 1 MB file, about 685 segments of 1,460 bytes:

- Segments delivered after each RTT: 10, 30, 70, 150, 310, 630, then the rest in RTT 7.
- With a 100 ms RTT, that is about 700 ms, plus one RTT for the TCP handshake, even on a fast link.

So for small transfers, latency (RTT) limits speed more than bandwidth does. This is why HTTP reuses connections, and why servers raised the initial cwnd from 1–4 segments to 10.

## Where the assumption breaks

Slow start assumes that **loss means congestion**. On a wired network, this is usually true. On lossy Wi-Fi or cellular links, packets can be lost from radio noise while the path has spare capacity. The sender then shrinks cwnd for no good reason, and throughput drops.

## Not covered here

- Congestion avoidance and fast recovery after a loss (Reno, CUBIC).
- Model-based algorithms such as BBR, which estimate bandwidth and RTT instead of reacting only to loss.
- QUIC, which runs similar congestion control over UDP.
