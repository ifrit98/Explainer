# Agreeing on a secret in public

Alice and Bob have never met. They want to send each other encrypted messages, and encryption needs a shared secret key. The only way they can talk is a channel that anyone can read: the internet, a radio link, a postcard. Call the listener Eve. Eve sees every message Alice and Bob send.

At first this looks impossible. Anything Alice sends, Eve also gets. If Alice simply sends a key, Eve has the key too. Alice could encrypt the key first, but that needs another key, which brings back the same problem.

Two ideas solve it:

1. **Each person keeps a secret that is never sent.** Only *results computed from* the secrets go over the channel.
2. **Use a calculation that is easy to do but very hard to undo.** Eve sees the results but can't work back to the secrets.

The method below is called **Diffie–Hellman key exchange** (Whitfield Diffie and Martin Hellman, 1976). Almost every secure web connection still uses it or a close variant.

---

## An analogy: mixing paint

Assume that mixing two paints is easy, and that separating a mixture back into the paints that made it is practically impossible.

1. Alice and Bob agree on a common colour in public, say **yellow**. Eve knows it.
2. Alice privately picks a secret colour, **red**. Bob privately picks **blue**. Neither one ever sends their secret colour.
3. Alice mixes yellow + red and sends the result (orange). Bob mixes yellow + blue and sends the result (green). Eve sees orange and green.
4. Alice adds her red to Bob's green, which gives **yellow + blue + red**. Bob adds his blue to Alice's orange, which gives **yellow + red + blue**.

Both now hold the same muddy brown. Order doesn't matter when you mix paint. Eve has yellow, orange and green. If she mixes orange and green she gets *yellow + red + yellow + blue*, which has too much yellow and isn't the same colour. To make the brown, she would need to pull red out of orange or blue out of green, and we assumed that can't be done.

The real method replaces paint with arithmetic that has the same two properties:

- **The order of combining doesn't matter**, so Alice and Bob end up with the same result.
- **Combining can't feasibly be undone**, so Eve can't recover the secrets.

---

## The arithmetic: powers on a clock

### Modular arithmetic

"x mod p" means the remainder when x is divided by p. It is the arithmetic of a clock with p positions, numbered 0 to p − 1. When you go past the top, you wrap around:

- 17 mod 12 = 5 (17 o'clock is 5 o'clock)
- 25 mod 23 = 2

Remainders behave well under multiplication. You can reduce at every step and the final answer comes out the same:

(a × b) mod p = ((a mod p) × (b mod p)) mod p

This means the numbers never need to grow large. To compute 5¹⁵ mod 23, you can multiply by 5 fifteen times and take the remainder after each step. Every intermediate value stays below 23.

### The easy direction

Choose a prime p and a number g. Given a secret x, computing

  **g^x mod p**

is fast, even when the numbers are hundreds of digits long. The trick is **repeated squaring**. Square g to get g², square that to get g⁴, then g⁸, g¹⁶, and so on, reducing mod p each time. Then multiply together the powers you need: g¹⁵ = g⁸ · g⁴ · g² · g¹. A 600-digit exponent needs only a few thousand multiplications.

### The hard direction

Going backwards means: given p, g and the result y = g^x mod p, find x. This is the **discrete logarithm problem**. With ordinary numbers, logarithms are easy. You can watch 5^x grow and stop when it reaches the right size. On a clock, the values jump around with no visible pattern:

| x | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 |
|---|---|---|---|---|---|---|---|---|---|----|
| 5^x mod 23 | 5 | 2 | 10 | 4 | 20 | 8 | 17 | 16 | 11 | 9 |

No method is known that solves this quickly when p is large and chosen well. The best known algorithms are much faster than trying every x, but they are still far too slow for primes about 2048 bits (≈ 617 digits) long. This difference between easy and hard is the "paint can't be unmixed" property.

---

## The protocol

**Public, known to everyone including Eve:** a large prime p and a number g.

| Step | Alice | Channel (Eve sees this) | Bob |
|---|---|---|---|
| 1 | picks secret **a** | | picks secret **b** |
| 2 | computes A = g^a mod p | A →  | |
| 3 | | ← B | computes B = g^b mod p |
| 4 | computes s = B^a mod p | | computes s = A^b mod p |

Both get the same s:

- Alice: B^a = (g^b)^a = g^(ba)
- Bob: A^b = (g^a)^b = g^(ab)

Since ab = ba, the two values are equal, and the mod-p reduction doesn't change that. This is the "order of mixing doesn't matter" property.

Eve knows p, g, A and B. To get s, she needs a or b, which means solving a discrete logarithm. Multiplying A by B gives her g^(a+b), not g^(ab), just as mixing orange with green gave the wrong colour.

### A worked example with small numbers

Public values: p = 23, g = 5.

- Alice picks a = 6. She sends A = 5⁶ mod 23 = **8** (see the table above).
- Bob picks b = 15. He sends B = 5¹⁵ mod 23 = **19**.
- Alice computes 19⁶ mod 23. Since 19 ≡ −4, this is (−4)⁶ = 4096, and 4096 = 178 × 23 + 2, so the result is **2**.
- Bob computes 8¹⁵ mod 23 = **2**.

The shared secret is 2. Eve saw 23, 5, 8 and 19. With numbers this small she can find a by checking the table, so the example is only for illustration. With a 617-digit p, the table would have more rows than there are atoms in the universe.

### In code

Python's three-argument `pow` does fast modular exponentiation:

```python
import secrets

p = 23          # in reality: a standardised ~2048-bit prime
g = 5

a = secrets.randbelow(p - 2) + 1    # Alice's secret, never sent
b = secrets.randbelow(p - 2) + 1    # Bob's secret, never sent

A = pow(g, a, p)    # Alice sends this
B = pow(g, b, p)    # Bob sends this

alice_key = pow(B, a, p)
bob_key   = pow(A, b, p)
assert alice_key == bob_key
```

---

## The catch: Eve who only listens vs. Mallory who interferes

Everything above assumes the attacker **only reads**. Now suppose an attacker, Mallory, can also **change** messages in transit:

```
Alice --A--> [Mallory] --M--> Bob
Alice <--M-- [Mallory] <--B-- Bob
```

Mallory picks her own secret m. She replaces A and B with her own M = g^m mod p. Alice ends up with a key she shares with Mallory, and Bob ends up with a different key he shares with Mallory. Both think they're talking to each other. Mallory decrypts each message, reads it, re-encrypts it, and passes it on. This is a **man-in-the-middle attack**.

Diffie–Hellman alone answers "how do we agree on a secret that a *listener* can't learn?". It does not answer "am I really talking to Bob?". Answering that second question needs **authentication**: some way for Bob to prove that B came from him. On the web, this works as follows:

- The server signs its Diffie–Hellman value with a **digital signature**, using a private key that only the server holds.
- A **certificate** vouches that the matching public key belongs to, say, `bank.example`. The certificate is signed by a certificate authority, and your browser or operating system already trusts that authority.

So "never met" is true only up to a point. Alice and Bob don't share any secret in advance, but Alice must trust *something* in advance that tells her which public key belongs to Bob. That trust can be a certificate authority, a fingerprint checked in person, or a key pinned in an app. The key exchange removes the need for a shared *secret*. It doesn't remove the need for trusted *identity* information, which can be public.

---

## After the exchange

- The shared value s isn't used directly as a key. It goes through a **key derivation function** (a hash-based procedure). That turns it into uniformly random-looking keys of the right length for a fast symmetric cipher such as AES.
- Good practice is to pick **fresh a and b for every session** and then delete them. If the server's long-term signing key is stolen later, past sessions still can't be decrypted, because the secrets that produced their keys no longer exist. This property is called **forward secrecy**.

## Variants you'll meet

- **Elliptic-curve Diffie–Hellman (ECDH, e.g. X25519).** Same protocol, but on points of an elliptic curve instead of numbers mod p. "Raise g to the power a" becomes "add the point G to itself a times". The reverse problem is believed to be harder per bit, so 256-bit keys give security comparable to 3072-bit p. This is what most TLS connections use today.
- **Post-quantum key exchange (e.g. ML-KEM).** A large quantum computer running Shor's algorithm could solve discrete logarithms efficiently, which would break both kinds above. Newer schemes are based on different hard problems (lattices). Current systems often run a classical exchange and a post-quantum exchange together, and combine the results.

---

## Summary

- Each side keeps a secret that is never sent, and publishes g^secret mod p.
- Each side raises the other's public value to its own secret. Both get g^(ab) mod p, because exponents multiply in either order.
- An eavesdropper sees g^a and g^b. Getting g^(ab) from those appears to require solving a discrete logarithm, which is infeasible at real sizes.
- This protects against listeners only. To stop someone who swaps messages, the exchange must be authenticated, usually with signatures and certificates.
