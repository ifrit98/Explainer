# Why does a new TCP connection send slowly at first?

_none_

Because of **TCP slow start**, a congestion-control mechanism that makes a new connection probe the network's capacity instead of assuming it.

### The core problem
When a connection opens, the sender knows nothing about the path: how much bandwidth is available, how many other flows share the bottleneck, or how big the router buffers are. If every new connection immediately sent at full speed, it could overflow buffers and cause heavy packet loss, a pattern that produced real "congestion collapse" on the Internet in the mid-1980s. Van Jacobson's 1988 fixes, including slow start, came out of that.

### How it works
- The sender keeps a **congestion window (cwnd)**, the amount of unacknowledged data it may have in flight. This is separate from the receiver's advertised window.
- cwnd starts small. Modern stacks use an **initial window of 10 segments** (about 14 KB, per RFC 6928). Older stacks used 1 to 4.
- For every ACK received, cwnd grows by one segment. This **roughly doubles cwnd every round-trip time**, which is exponential growth, so "slow" refers to the start point, not the growth rate.
- Growth continues until one of these happens:
  - cwnd reaches the **slow-start threshold (ssthresh)**. TCP then switches to **congestion avoidance**, where growth is linear, about +1 segment per RTT.
  - **Packet loss** is detected (or ECN marks arrive). cwnd and ssthresh are reduced.
  - It hits the receiver's window limit.

### Why you notice it
Throughput is about cwnd / RTT. Early on, cwnd is small, so:
- **Short transfers** (small web pages, API calls) may finish before cwnd ever grows large. They are limited by round trips, not bandwidth.
- **High-latency links** suffer more, because each doubling takes one full RTT.
- Example: reaching a ~1 MB window from 10 segments takes about 6 to 7 RTTs. On a 100 ms path, that is over half a second before reaching full speed.

### Related details
- **Slow start after idle:** many stacks reset cwnd after a connection sits idle, because the old estimate may be stale. On Linux this is `net.ipv4.tcp_slow_start_after_idle`.
- **Algorithm differences:** CUBIC (Linux and macOS default) and BBR handle the post-slow-start phase differently. BBR models bandwidth and RTT directly instead of reacting only to loss.

### Common mitigations
- **Reuse connections** (HTTP keep-alive, connection pooling, HTTP/2 multiplexing) so you pay the ramp-up once.
- **Reduce RTT** with CDNs and edge servers near users.
- **Larger initial windows** where appropriate (e.g., `ip route ... initcwnd` on Linux).
- **Fewer handshake round trips** with TLS 1.3, TCP Fast Open, or QUIC/HTTP/3. QUIC still does congestion control but starts sending sooner.
- Disable slow-start-after-idle for long-lived, bursty connections.

In short: TCP starts conservatively because it can't know the network's capacity in advance, then ramps up quickly while watching for signs of congestion.
