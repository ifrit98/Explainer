# Why does a new TCP connection send slowly at first?

_v0.6_

A new TCP connection sends slowly because the sender does not yet know how much data the network path can carry. It finds out by probing, and the probe starts small. This mechanism is called **slow start**.

The sender limits itself with a **congestion window** (cwnd): the number of unacknowledged bytes it may have in flight. The receiver also advertises a window, and the sender uses the smaller of the two.

**Why not send at full speed immediately?** The receiver's window says only how much the *receiver* can buffer. It says nothing about the slowest link on the path. Suppose a server sends a 1 MB burst into a path whose bottleneck router can queue only 100 KB. The router drops most of the burst, and the sender must retransmit it. If many senders do this, the links fill with retransmissions and useful throughput collapses. This **congestion collapse** happened on the early Internet in 1986, and slow start was introduced to prevent it.

**How the probe grows:** Each ACK that comes back increases cwnd by one segment. A full window of ACKs arrives in one round-trip time (RTT), so cwnd doubles every RTT. Growth is exponential, so "slow" describes only the starting point.

**Example with numbers:**
- Initial cwnd = 10 segments × 1460 bytes ≈ 14.6 KB. This is the common modern default (RFC 6928).
- RTT = 100 ms.
- cwnd after each RTT: 10, 20, 40, 80, 160, 320, 640, 1280 segments.
- After about 7 RTTs (0.7 s), cwnd passes 1000 segments ≈ 1.46 MB per RTT ≈ 117 Mbit/s.

Slow start ends when a packet is lost or cwnd reaches a threshold (ssthresh). The sender then grows cwnd linearly, by about one segment per RTT. This is why short transfers on high-latency links rarely reach full link speed: they finish before the window has grown.

If useful, I can explain what happens to cwnd after a loss.
