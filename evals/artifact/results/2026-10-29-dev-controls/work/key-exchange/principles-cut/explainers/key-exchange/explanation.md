# Agreeing on a secret key over a public channel

**The question.** Alice and Bob have never met. They can talk only over a channel that an eavesdropper, Eve, reads in full. How can they end up with the same secret number that Eve does not know?

**The answer in one paragraph.** Each person picks a private number and never sends it. Each person sends a *public value* made from their private number. Each person then combines their own private number with the other person's public value. The rules of arithmetic make both results equal. Eve sees only the two public values. This method is the **Diffie–Hellman key exchange** (1976).

**Why it matters.** Your browser does this each time it opens an `https://` connection. The shared number becomes the key for a fast cipher that encrypts the rest of the conversation.

## The tool: arithmetic "mod p"

"x mod p" means the remainder when you divide x by p. For example, 30 mod 23 = 7. Arithmetic mod p keeps every number between 0 and p − 1, however large the calculation becomes. A clock does the same with 12.

## First attempt: send the key

Alice picks a key and sends it to Bob. Eve reads it. This fails at once, so neither person can ever send the secret itself or anything that reveals it.

## Second attempt: hide the private number with multiplication

Alice and Bob agree in public on a prime **p = 23** and a base **g = 5**. Alice picks a private number **a = 6** and sends **g × a mod p** = 30 mod 23 = **7**.

*Before you read on: can Eve get 6 back from 7?*

Yes. Eve knows g = 5 and p = 23. She finds the number that undoes "× 5" mod 23. That number is 14, because 5 × 14 = 70 = 3 × 23 + 1. Then 7 × 14 = 98, and 98 mod 23 = **6**. Eve has Alice's private number. A method called the extended Euclidean algorithm finds this "undo" number quickly, even when p has hundreds of digits. So multiplication fails.

## The working method: hide the private number with exponentiation

Use powers instead of products. Everything else stays the same.

| Step | Alice (private: a = 6) | Public channel (Eve sees this) | Bob (private: b = 15) |
|---|---|---|---|
| 1. Agree on public settings | | p = 23, g = 5 | |
| 2. Make a public value | A = 5⁶ mod 23 = **8** | A = 8, B = 19 | B = 5¹⁵ mod 23 = **19** |
| 3. Combine with the other's value | 19⁶ mod 23 = **2** | | 8¹⁵ mod 23 = **2** |

Alice and Bob both get **2**. Eve saw 23, 5, 8 and 19. She never saw 6, 15 or 2.

**Why the two results are equal.** Alice computes (g^b)^a. Bob computes (g^a)^b. Both equal g^(a×b), because the order of the exponents does not matter. Taking "mod p" at each step does not change this. Here, both are 5⁹⁰ mod 23 = 2.

## Where the guarantee breaks: an attacker who can change messages

The method defeats Eve, who only reads. It does not defeat Mallory, who can intercept and replace messages.

Mallory picks her own private number m = 3 and computes M = 5³ mod 23 = **10**. She blocks A = 8 and B = 19, and sends 10 to both Alice and Bob instead.

- Alice computes 10⁶ mod 23 = **6**. Mallory computes 8³ mod 23 = **6**. They share a key.
- Bob computes 10¹⁵ mod 23. Mallory computes 19³ mod 23. They share a different key.

Alice and Bob each think they talk to the other. Mallory decrypts each message, reads it, re-encrypts it, and passes it on. This is a **man-in-the-middle attack**.

The fix is **authentication**: Bob signs his public value with a digital signature, and Alice checks the signature against a key she already trusts. On the web, a certificate authority vouches for that key. So "never met" is not quite free: key exchange removes the need to share a *secret* in advance, but each side still needs a trusted way to check *who* the other side is.

## Summary

1. Agree in public on p and g.
2. Each person keeps a private exponent and sends g^(private) mod p.
3. Each person raises the other's public value to their own private exponent. Both get g^(a×b) mod p.
4. Authenticate the public values, or an active attacker can sit in the middle.

**Not covered here:** elliptic-curve Diffie–Hellman (the same idea on a different group, with shorter keys and the same structure), how to choose safe p and g, and how digital signatures work.
