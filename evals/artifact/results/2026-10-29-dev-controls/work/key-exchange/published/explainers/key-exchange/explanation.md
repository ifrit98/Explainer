# How can two strangers agree on a secret key when anyone can read their messages?

**They never send the key. Each person keeps a private number and sends a public number computed from it. Each then combines the other person's public number with their own private number, and both get the same result. An eavesdropper sees only the public numbers, and no known fast method gets the private numbers back from them.**

This method is the Diffie–Hellman key exchange. A version of it starts most HTTPS connections.

## The problem

Alice and Bob want to encrypt their messages. Encryption needs a key that both of them know. They have never met, so every message goes over a public channel. Eve, an eavesdropper, reads every message but does not change any. So the key itself can never be sent.

The calculations below use one piece of notation. "mod 23" means "the remainder after division by 23". For example, 100 mod 23 = 8, because 100 = 4 × 23 + 8.

<!-- claim: two-privates -->
A first idea fails. Alice chooses a key, the number 6, and sends 5^6 mod 23 = 8. This operation is hard to reverse (later sections show why). Bob receives 8, and so does Eve. If Eve cannot get 6 back from 8, Bob cannot either. So each side needs its own private number. Each side then does one half of a calculation, and the other side finishes it without undoing it.

## The exchange, with small numbers

<!-- claim: agreement -->
1. Alice and Bob agree in public on two numbers: a prime **modulus** p = 23 (the number after "mod") and a **base** g = 5.
2. Each picks a **private number** at random and never sends it. Alice picks a = 6. Bob picks b = 15.
3. Each sends a **public number**: g raised to their private number, mod p. Alice sends A = 5^6 mod 23 = 15625 mod 23 = 8. Bob sends B = 5^15 mod 23 = 19.
4. Each raises the other's public number to their own private number, mod p. Alice computes 19^6 mod 23 = 2. Bob computes 8^15 mod 23 = 2.

The result, s = 2, is the **shared secret**. Alice and Bob both feed s into the same hash function, a fixed scrambling recipe, and the output is the key for ordinary encryption.

**Why both get 2.** Alice computed (5^15)^6, and Bob computed (5^6)^15. By the exponent rule, both equal 5^(6×15). Both also took remainders along the way, and that does not change the final remainder. Replacing a factor with its remainder removes a multiple of 23 from that factor, so it removes a multiple of 23 from the product: (x + 23k) × y = x × y + 23ky, for any whole number k. A power is a chain of products, so the rule holds at every step. Example: 5^3 = 125, and 125 mod 23 = 10. Reducing first gives (25 mod 23) × 5 = 2 × 5 = 10.

## What Eve sees

<!-- claim: eve-stuck -->
| Who | p, g | a = 6 | b = 15 | A = 8, B = 19 | s = 2 |
|---|---|---|---|---|---|
| Alice | yes | yes | no | yes | yes |
| Bob | yes | no | yes | yes | yes |
| Eve | yes | no | no | yes | no |

*Predict before you read on:* Eve has 8 and 19. Can Eve combine them into 2?

Multiplying fails: 8 × 19 mod 23 = 152 mod 23 = 14. Multiplying powers adds the exponents, so 14 = 5^(6+15) mod 23. The shared secret needs the exponents multiplied: 5^(6×15). No one knows a way from A and B to s other than, in effect, finding a or b first. That problem, getting 6 back from 8, is the discrete logarithm, and the next section shows why no fast method for it is known.

## Why powers, and why mod

Each choice blocks a simpler way for Eve to find a private number.

<!-- claim: why-mod -->
- **Without mod**, A = 5^6 = 15625. Eve takes the logarithm base 5 of 15625 and gets 6. Plain powers grow in order, so a logarithm reverses them.

<!-- claim: why-power -->
- **With multiplication instead of a power**, A = 5 × 6 mod 23 = 7. Multiplying by 14 undoes multiplying by 5, because 5 × 14 = 70 = 3 × 23 + 1. A standard fast method (Euclid's algorithm) finds this undoing number even for a huge p. So Eve computes 7 × 14 mod 23 = 6 = a, then computes the shared secret as Alice does.
- **With powers mod p**, the results jump around. For exponents 1 to 22, 5^x mod 23 gives: 5, 2, 10, 4, 20, 8, 17, 16, 11, 9, 22, 18, 21, 13, 19, 3, 15, 6, 7, 12, 14, 1. A result near 8 says nothing about where 6 is.

So g^x mod p is a **one-way operation**: fast to compute, with no known fast reverse. The reverse problem (given g, p, and g^x mod p, find x) is the **discrete logarithm** named above.

## Why real numbers are huge

With p = 23, Eve can try exponents in order: 5, 2, 10, 4, 20, 8. The 6th try gives 8, so a = 6. Real exchanges use a p of 2048 bits, about 617 decimal digits. They pick a and b at random from that whole range. Then trying exponents one by one is hopeless. The best known methods are faster, but still need about 2^112 operations (an estimate). At a trillion operations per second, that is about 10^14 years.

Alice's own work stays small. Alice squares or multiplies by 5, and takes the remainder at each step (→ marks the remainder): 5^2 = 25 → 2, 5^3 = 2 × 5 = 10, 5^6 = 10^2 = 100 → 8. Each squaring doubles the exponent, so a 2048-bit exponent needs about 2048 squarings plus at most 2048 multiplications: about 4,000 steps.

<!-- claim: assumption -->
**Assumption, not proof.** No one has proven that the discrete logarithm is hard, or that Eve cannot get s from A and B some other way. The security rests on decades of failed attempts.

## The limit: an attacker who changes messages

<!-- claim: mitm -->
The exchange stops a reader. It does not stop Mallory, an attacker who can replace messages. Mallory picks 3, and sends 5^3 mod 23 = 10 to Alice and to Bob in place of their public numbers.

- Alice computes 10^6 mod 23 = 6. Mallory computes 8^3 mod 23 = 6 from Alice's public number.
- Bob computes 10^15 mod 23 = 5. Mallory computes 19^3 mod 23 = 5 from Bob's public number.

Alice shares 6 with Mallory, and Bob shares 5 with Mallory. Mallory decrypts each message, reads it, and encrypts it again for the other side. Nothing in the exchange tells Alice who sent a public number. Real systems add **authentication**: Bob attaches to B a value that only Bob can produce and anyone can check (a digital signature).

## Answer

The two strangers never send the key. Each sends g raised to a private number, mod p. Each raises the other's public number to their own private number, and both get g^(ab) mod p. Eve sees only g^a and g^b mod p. To get further, Eve must find a or b, and no fast method is known for a large p.

## Scope

- **Authentication**: digital signatures and certificates, which is how HTTPS stops Mallory.
- **Elliptic-curve Diffie–Hellman**: the same idea with points on a curve in place of powers mod p.
- **Using the key**: a cipher such as AES encrypts the messages with it.
- **Choosing p and g safely**: a prime p lets a good g reach every non-zero remainder, as 5 does for 23. A bad g fails: for example, with g = 22 the powers mod 23 are only 1 and 22, so s has only two possible values.
- **Quantum computers**: a large quantum computer could solve the discrete logarithm fast. Post-quantum key exchange methods are designed to resist that.
