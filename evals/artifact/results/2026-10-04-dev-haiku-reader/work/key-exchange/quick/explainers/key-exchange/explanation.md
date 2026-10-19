# How can two strangers agree on a secret key in public?

**Each person keeps one number private and sends a value computed from it. Each person then combines the other person's value with their own private number. Both get the same shared key, but the shared key is never sent. An eavesdropper sees every message and still cannot compute it, because one step is easy to do and, as far as anyone knows, very hard to undo.**

The method is the Diffie–Hellman key exchange. Below, Alice and Bob want a shared key. Eve reads every message on the channel.

"x mod p" means the remainder after you divide x by p. For example, 25 mod 23 = 2.

## How it works

<!-- claim: mech-exchange -->

1. Agree in public on a prime p and a base g. Here, p = 23 and g = 5. Eve knows them too.
2. Each person picks a **private number** at random and never sends it. Alice picks a = 6. Bob picks b = 15.
3. Each person computes a **public value**, g to the power of their private number, mod p, and sends it:
   - Alice: A = 5^6 mod 23 = 8.
   - Bob: B = 5^15 mod 23 = 19.
4. Each person raises the *other* public value to their *own* private number:
   - Alice: 19^6 mod 23 = **2**.
   - Bob: 8^15 mod 23 = **2**.

The two results are equal because 19 = 5^15 and 8 = 5^6, so both people compute 5^(6·15) mod 23. Order does not matter: (g^b)^a = (g^a)^b = g^(ab). The **shared key** is 2.

## Why Eve fails

<!-- claim: guarantee-eve -->

Eve sees 23, 5, 8 and 19. To get the key she needs a or b. That means solving 5^a mod 23 = 8 for a. This problem is the **discrete logarithm**.

At p = 23 Eve can try every exponent: 5^1, 5^2, … mod 23 gives 5, 2, 10, 4, 20, 8. She finds a = 6 on try 6. So p must be large. Real systems use a p of 2048 bits (about 617 digits). The best known methods then need about 2^112 operations, far beyond any computer (NIST estimate). Alice and Bob still compute their values quickly, because repeated squaring needs only about 2 × 2048 multiplications.

Eve cannot combine 8 and 19 directly either. 8 × 19 gives 5^(6+15), not 5^(6·15).

## Why this form

<!-- claim: why-exp -->

**Why powers, not multiplication?** Suppose Alice sent A = g·a mod p = 5·6 mod 23 = 7. Eve multiplies 7 by 14, because 5·14 mod 23 = 1. She gets 7·14 mod 23 = 6, which is a. Division undoes multiplication fast. No similar shortcut is known for powers mod p.

<!-- claim: why-mod -->

**Why mod p?** Without it, Alice sends 5^6 = 15625. Eve computes log base 5 of 15625 = 6. Plain powers grow smoothly, so an ordinary logarithm undoes them. Mod p scrambles the order: the list 5, 2, 10, 4, 20, 8 above has no pattern to follow.

## Limits

<!-- claim: limit-mitm -->

- **Eve must only read (assumption).** Suppose Mallory can also replace messages. Mallory picks 3 and sends 5^3 mod 23 = 10 to Alice in place of 19. Alice computes 10^6 mod 23 = 6. Mallory computes 8^3 mod 23 = 6. Alice now shares key 6 with Mallory and believes it is Bob. Mallory does the same with Bob. The fix is to authenticate the public values, for example with signatures and certificates, as HTTPS does.
- **Hardness is assumed, not proven.** No fast method for the discrete logarithm is known on ordinary computers. A large quantum computer would break it (Shor's algorithm), so newer systems add post-quantum key exchange.
- Most systems today use the same idea on elliptic curves (X25519), which gives equal security with much smaller numbers.
