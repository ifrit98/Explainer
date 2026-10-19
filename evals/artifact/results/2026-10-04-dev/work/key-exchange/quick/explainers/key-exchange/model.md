# Semantic model: Diffie–Hellman key exchange

> Source of truth. Every rendering derives from this file.

## Central question

How can two people who have never met agree on a secret key over a channel that anyone can read?

## Audience and prior knowledge

A technical reader: school mathematics (powers, remainders), basic programming. Knows what encryption is in a general way. Does not know modular arithmetic as a tool, one-way functions, or Diffie–Hellman.

## Entities

| Entity | Definition (one sentence) | Status |
|---|---|---|
| Alice, Bob | The two people who want a shared key. | — |
| Eve | An eavesdropper who reads every message on the channel but does not change messages. | assumption (passive) |
| Mallory | An attacker who can read and replace messages. | used for the limit case |
| public numbers p, g | A large prime p and a base g, known to everyone. | fact |
| private number | A number each person picks at random and never sends (a for Alice, b for Bob). | fact |
| public value | g raised to the private number, mod p (A = g^a mod p, B = g^b mod p); sent in the open. | fact |
| shared key | g^(ab) mod p, which both compute and Eve cannot. | fact |
| mod p | The remainder after division by p. | definition |

## Causal chain

```text
pick private number → send public value → raise the other's public value to your private number → same shared key
(B^a = g^(ba) = g^(ab) = A^b)
Eve has g, p, A, B but needs a or b → finding a from A = g^a mod p (discrete logarithm) is infeasible for large p
```

## Quantities

Worked example: p = 23, g = 5, a = 6, b = 15.
- A = 5^6 mod 23 = 8. B = 5^15 mod 23 = 19.
- Alice: 19^6 mod 23 = 2. Bob: 8^15 mod 23 = 2. Shared key = 2.
- Size of p: at p = 23 Eve tries all 22 exponents at once. At 2048 bits (about 617 digits) the best known methods need about 2^112 operations (NIST estimate).

## Why this form

| Operation | Simplest alternative | What the alternative breaks (with numbers) |
|---|---|---|
| exponentiation | multiply: A = g·a mod p | A = 5·6 mod 23 = 7. Eve multiplies by the inverse of 5 (14): 7·14 mod 23 = 6 = a. Division undoes multiplication fast. |
| mod p | plain powers, no mod | 5^6 = 15625; Eve computes log base 5 of 15625 = 6. Plain powers grow smoothly, so a logarithm undoes them. Mod p scrambles the order: 5^1..5^6 mod 23 = 5, 2, 10, 4, 20, 8. |

## Concrete cases

| Claim | Holds here | Breaks here |
|---|---|---|
| Eve cannot get the key | Eve sees 23, 5, 8, 19; to get 2 she needs a or b. For a 2048-bit p no known method finds them. | Small p: at p = 23 Eve tries 5^1, 5^2, … until she gets 8, and finds a = 6 within 22 tries. |
| The key is shared only with the intended person | Passive Eve only reads. | Active Mallory replaces B with M = 5^3 mod 23 = 10. Alice computes 10^6 mod 23 = 6; Mallory computes 8^3 mod 23 = 6. Alice shares key 6 with Mallory and thinks it is Bob. Fix: authenticate public values (signatures, certificates). |

## Terms

- mod p: remainder after division by p. 
- private number: never sent. public value: sent. shared key: computed, never sent.
- discrete logarithm: finding a from g^a mod p.

## Epistemic status

- **Mathematical consequence:** B^a = A^b mod p.
- **Assumed:** the discrete logarithm is hard for large p. Not proven; no fast classical method is known. A large quantum computer would break it (Shor's algorithm).
- **Estimate:** 2^112 operations for 2048-bit p.

## Confusion points

- "The key is sent encrypted" → the shared key is never sent at all; each side computes it.
- "Eve can multiply A and B" → A·B = g^(a+b), not g^(ab).
- "This proves who you are talking to" → no; it needs authentication (Mallory case).

## Scope

- **Out of scope:** elliptic-curve Diffie–Hellman (X25519) — same idea in a different group, smaller numbers; used in TLS today.
- **Out of scope:** how the shared key then encrypts data (AES); post-quantum key exchange (ML-KEM).

## Representation decision

- **Stage:** 1
- **Reason:** a short sequence of steps with one worked example; no topology or parameter space to explore.
- **Levels:** L1 the answer / L2 the steps with numbers / L3 why Eve fails and why this form / L4 limits.
