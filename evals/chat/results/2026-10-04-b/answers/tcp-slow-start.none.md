# Why does a new TCP connection send slowly at first?

_none_

A new TCP connection starts slowly because of **slow start**, part of TCP's congestion control.

## The core problem

When a connection opens, the sender has no idea how much bandwidth is available along the path. The bottleneck could be a 10 Gbps fiber link or a congested Wi-Fi hop. If it immediately sent as fast as it could, it might flood a router's buffers, causing packet loss for itself and everyone sharing that link. This actually happened in the mid-1980s, when the early Internet suffered "congestion collapse," with throughput dropping by orders of magnitude. Van Jacobson's 1988 fixes, including slow start, were the response.

## How slow start works

The sender keeps a **congestion window (cwnd)**, which limits how much unacknowledged data it can have in flight. This is separate from the receiver's advertised window.

1. **Start small.** The initial window (initcwnd) is typically 10 segments (about 14 KB) on modern systems, per RFC 6928. Older stacks used 1 to 4 segments.
2. **Grow on each ACK.** For every acknowledged segment, cwnd increases by about one segment. In practice this **doubles cwnd every round-trip time**, so growth is exponential, despite the name "slow."
3. **Stop at a threshold or on loss.**
   - When cwnd reaches the **slow start threshold (ssthresh)**, TCP switches to **congestion avoidance**, growing roughly linearly (about +1 segment per RTT).
   - If packet loss is detected, TCP takes it as a sign of congestion, cuts cwnd (and sets ssthresh lower), and backs off.

## Why it feels slow

Throughput is roughly **cwnd / RTT**, so ramping up takes several round trips. For example, with a 100 ms RTT and a 14 KB initial window:

| RTT # | cwnd | Approx. throughput |
|---|---|---|
| 1 | 14 KB | ~1.1 Mbps |
| 2 | 28 KB | ~2.2 Mbps |
| 3 | 56 KB | ~4.5 Mbps |
| 4 | 112 KB | ~9 Mbps |
| ... | ... | ... |

Reaching hundreds of Mbps can take many RTTs. Most web transfers are small and finish **while still in slow start**, so for them latency matters more than raw bandwidth.

## Related factors

- **The handshake.** Before any data flows, the TCP 3-way handshake costs one RTT, and TLS adds one or two more.
- **Slow start after idle.** Many stacks reset cwnd after a connection sits idle (on Linux, `net.ipv4.tcp_slow_start_after_idle`), so even a reused connection can start slowly again.
- **Algorithm choice.** CUBIC, the default on Linux, macOS, and Windows, and BBR handle the post-slow-start phase differently. BBR probes bandwidth and RTT directly instead of relying only on loss.

## Mitigations

- **Reuse connections**: HTTP keep-alive, HTTP/2 multiplexing, connection pooling.
- **Raise the initial window**: on Linux, `ip route change ... initcwnd 10`, or higher for controlled environments.
- **Reduce RTT**: CDNs and edge servers put content closer to users, so each doubling happens faster.
- **Use QUIC/HTTP/3**: it still uses congestion control but combines the transport and TLS handshakes, and supports 0-RTT resumption.
- **Disable slow-start-after-idle** on servers with long-lived connections.

In short, TCP starts slowly as a safety mechanism. It probes the network's capacity instead of assuming it, trading a little startup latency for stability across the whole Internet.
