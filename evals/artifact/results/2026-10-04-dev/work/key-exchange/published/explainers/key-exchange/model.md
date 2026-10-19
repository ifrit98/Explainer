# Semantic model: Diffie–Hellman key exchange

> Source of truth. Every rendering (prose, diagram, page, video) derives from this file.
> If a rendering needs a new fact, add it here first.

## Central question

How can two people who have never met agree on a secret key over a channel that anyone can read?

## Audience and prior knowledge

A technical reader: school mathematics (powers, exponent rules such as (x^a)^b = x^(ab), logarithms, remainders) and basic programming. New to cryptography. Does not know modular arithmetic by that name, the discrete logarithm, or the idea of a one-way function. Knows that a "key" is the secret that an encryption method needs. Renderings do not explain exponent rules or what encryption is.

## Entities

| Entity | Definition (one sentence) | Status |
|---|---|---|
| Alice, Bob | The two people who want a shared key; they have never met and share no secret. | setup |
| Eve | An eavesdropper who reads every message on the channel but does not change any. | assumption (passive attacker) |
| Public channel | A channel where every message is visible to everyone. | setup |
| Modulus p | A large prime number, public, that everyone agrees on. Example: 23. | fact |
| Base g | A public number that is raised to powers. Example: 5. | fact |
| "mod p" | The remainder after division by p. 100 mod 23 = 8. | definition |
| Private number (a, b) | A random number that each person picks and never sends. Example: a = 6, b = 15. | fact |
| Public number (A, B) | g raised to the private number, mod p; each person sends it on the channel. A = 5^6 mod 23 = 8, B = 5^15 mod 23 = 19. | fact |
| Shared secret s | The number both compute: the other's public number raised to one's own private number, mod p. s = 2. It becomes the key. | fact |
| One-way operation | An operation that is fast to compute and has no known fast reverse. g^x mod p is one. | assumption (believed, not proven) |
| Discrete logarithm | The reverse problem: given g, p, and g^x mod p, find x. | fact (definition) |

## Relationships

| From | Relationship (verb) | To | Notes |
|---|---|---|---|
| Alice | keeps | a | never sent |
| Alice | sends | A = g^a mod p | Eve sees it |
| Bob | sends | B = g^b mod p | Eve sees it |
| Alice | computes | B^a mod p = s | |
| Bob | computes | A^b mod p = s | same s |
| Eve | sees | p, g, A, B | not a, b, s |
| Eve | must solve | discrete logarithm | to get a or b |

## Dependencies (learning order)

1. The problem: any message can be read, so the key itself can never be sent.
2. The idea: each side mixes a public value with a private value, and both mixes come out equal.
3. Powers give this: (g^a)^b = (g^b)^a.
4. Plain powers are reversible (logarithm), so wrap them: mod p.
5. Eve's view and why she is stuck (discrete logarithm).
6. Size of p sets how stuck she is.
7. Limit: an active attacker (man in the middle).

## Causal chain

```text
private a, b never sent → only A, B, p, g are public
→ both compute g^(ab) mod p because (g^a)^b = (g^b)^a
→ Eve needs a or b → discrete logarithm → no fast method known at large p → s stays secret
```

## Temporal sequence

1. Alice and Bob agree in public on p = 23 and g = 5.
2. Alice picks a = 6; Bob picks b = 15. They keep these.
3. Alice sends A = 8. Bob sends B = 19.
4. Alice computes 19^6 mod 23 = 2. Bob computes 8^15 mod 23 = 2.
5. They use s = 2 as the key for ordinary encryption.

## Quantities

- Worked example: p = 23, g = 5, a = 6, b = 15 → A = 8, B = 19, s = 2.
- Check: 5^6 = 15625; 15625 mod 23 = 8. 19^6 mod 23: 19^2 = 361 → 16; 19^4 = 16^2 = 256 → 3; 19^6 = 3 × 16 = 48 → 2. 8^15 mod 23: 8^2 = 64 → 18; 8^4 = 18^2 = 324 → 2; 8^8 = 4; 15 = 8 + 4 + 2 + 1, so 8^15 = 4 × 2 × 18 × 8 = 1152 → 2.
- Powers of 5 mod 23, for k = 1…22: 5, 2, 10, 4, 20, 8, 17, 16, 11, 9, 22, 18, 21, 13, 19, 3, 15, 6, 7, 12, 14, 1. All 22 non-zero remainders appear once; the order looks scrambled.
- Size of p in practice: 2048 bits, about 617 decimal digits. a and b are random numbers between 1 and p − 2 (a small range would let Eve try them all, whatever p is). With p = 23, Eve finds a by trying exponents 1, 2, 3, … : the 6th try gives 8. With a 617-digit p, trying every exponent is out of the question, and the best known methods still cost about 2^112 ≈ 5 × 10^33 operations (estimate); at 10^12 operations per second that is about 10^14 years.
- Alice's work: repeated squaring needs about 2 × 2048 multiplications mod p for a 2048-bit exponent. Reducing mod p after each step keeps numbers small and gives the same remainder: 5^2 = 25 → 2; 5^3 = 2 × 5 = 10 (and 125 mod 23 = 10); 5^6 = 10^2 = 100 → 8.
- Meaning of p's size: small p (23) → Eve tries every exponent in a moment; large p (617 digits) → no known method finishes in any useful time.

## Alternative states

| State / scenario | What changes | Why |
|---|---|---|
| No mod (plain powers) | Eve sees A = 15625, computes log₅ 15625 = 6 | ordinary powers grow in order, so the logarithm reverses them |
| Alice picks the key k = 6 and sends a one-way image of it, 5^6 mod 23 = 8 | Bob is as stuck as Eve: getting 6 from 8 is the same reverse problem | one secret is not enough; each side must finish the other's half without learning it, so both need a private number |
| Multiplication instead of powers: A = g·a mod p | A = 30 mod 23 = 7, B = 75 mod 23 = 6, s = 5·6·15 mod 23 = 13. Eve multiplies A by 14 (because 5 × 14 = 70 = 3 × 23 + 1) and gets 7·14 mod 23 = 6 = a; then B·a = 6·6 = 36 mod 23 = 13 = s | multiplication mod p has a fast reverse: Euclid's algorithm finds the undoing number (14 here) quickly even for a 617-digit p |
| Eve multiplies the public numbers | A·B mod 23 = 152 mod 23 = 14 = 5^(6+15) mod 23, not s = 2 | combining public numbers adds the exponents; the secret needs their product |
| Small p | Eve tries all 22 exponents | brute force is cheap |
| Bad g = 22 | 22^k mod 23 is only 1 or 22 | g must produce many different values; then s can be only 1 or 22 |
| Active attacker (Mallory) | Mallory replaces A and B with 5^3 mod 23 = 10. Alice gets s = 10^6 mod 23 = 6; Bob gets 10^15 mod 23 = 5; Mallory computes both (8^3 mod 23 = 6, 19^3 mod 23 = 5) and relays messages | the exchange does not prove who sent a public number |

## Why this form

| Operation | Simplest alternative | What the alternative breaks (with numbers) |
|---|---|---|
| Two private numbers | Alice picks the key and sends 5^k mod 23 | Bob cannot undo it either; he is as stuck as Eve. |
| Raise to a power (g^a) | Multiply (g·a mod p) | A = 7; Eve multiplies by 14, the number that undoes ×5 mod 23, and gets a = 6; then B·6 mod 23 = 13 = s. |
| Take mod p | Plain powers | A = 15625; log₅ 15625 = 6 gives a at once. |
| Each side raises the other's public number | Combine the two public numbers | A·B = 14 = g^(a+b); s = g^(ab) = 2. Eve can compute A·B, but it is not s. |
| p large | p = 23 | Eve tries 5, 2, 10, 4, 20, 8 and finds a = 6 on the 6th try. |

## Concrete cases

| Claim | Holds here (numbers) | Breaks here, without its assumption (numbers) |
|---|---|---|
| Both compute the same s | 19^6 mod 23 = 2 and 8^15 mod 23 = 2, both equal 5^90 mod 23 | (holds always: exponent rule; reducing mod p at each step does not change the remainder) |
| Eve cannot get s from p, g, A, B | p of 617 digits: no known method finds a | p = 23: 6 tries |
| s is shared with the right person | passive Eve: Alice and Bob both hold 2 | active Mallory: Alice holds 6, Bob holds 5, Mallory holds both |

## Terms

- **Public channel**: every message on it is visible to everyone.
- **Eve**: the eavesdropper; reads, does not change.
- **mod p**: the remainder after division by p. 100 mod 23 = 8.
- **Modulus p** and **base g**: public numbers fixed before the exchange.
- **Private number**: a or b; picked at random, never sent.
- **Public number**: A or B; g to the private number, mod p; sent.
- **Shared secret**: s; what both compute. It becomes the key.
- **One-way operation**: easy forward, no known fast reverse.
- **Discrete logarithm**: given g, p, and g^x mod p, find x.

## Epistemic status

- **Established:** the computation and the agreement on s (a mathematical consequence of exponent rules).
- **Assumed:** that the discrete logarithm has no fast algorithm for well-chosen large p. Not proven; decades of work have found methods faster than trying every exponent, but none fast enough for 2048-bit p on ordinary computers.
- **Assumed:** that no shortcut gives g^(ab) mod p from g^a and g^b without, in effect, finding a or b. Also believed, not proven. The obvious shortcut fails: A·B = 14, s = 2.
- **Assumed:** Eve is passive. The exchange alone does not stop an active attacker.

## Confusion points

- "They send the key, encrypted" → no message ever contains s, encrypted or not; each side computes it.
- "Eve can combine A and B" → A·B gives g^(a+b), not g^(ab).
- "If it's hard to reverse, it's hard to compute" → Alice computes fast by repeated squaring; only the reverse is slow.
- "This proves I'm talking to Bob" → no; man in the middle.
- "The private number is the key" → the key is s; a and b are each known only to one person.

## Scope

- **Out of scope:** authentication (digital signatures, certificates) — how TLS defeats the man in the middle.
- **Out of scope:** elliptic-curve Diffie–Hellman (X25519) — the same idea in a different number system, with smaller numbers for the same security; used in most TLS connections today.
- **Out of scope:** how s becomes a key — in practice s is first scrambled by a hash function; a cipher such as AES then uses it to encrypt the data.
- **Out of scope:** choosing p and g safely (why p is prime; why g must produce many values) and algorithms for the discrete logarithm.
- **Out of scope:** quantum computers — Shor's algorithm would solve the discrete logarithm fast; post-quantum key exchange replaces this method.

## Representation decision

- **Stage:** 1
- **Reason:** The argument is a short sequence of steps with small worked numbers. One table (who sees what) covers the only multi-relationship structure. A diagram or page would repeat the prose.
- **Levels:** L1 the idea / L2 the steps with numbers / L3 why Eve is stuck / L4 real sizes and the limit.
