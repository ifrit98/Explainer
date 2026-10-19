# How can two strangers agree on a secret key when anyone can read their messages?

**They never send the key. Each person keeps a private number and sends a public number computed from it. Each then combines the other person's public number with their own private number, and both get the same result.**

## The problem

Alice and Bob want to encrypt their messages. Eve reads every message. So the key itself can never be sent.

"mod 23" means "the remainder after division by 23". For example, 100 mod 23 = 8.

## The exchange, with small numbers

<!-- claim: agreement -->
1. Alice and Bob agree in public on p = 23 and g = 5.
2. Alice picks a private number a = 6. Bob picks b = 15.
3. Alice sends A = 5^6 mod 23 = 8. Bob sends B = 5^15 mod 23 = 19.
4. Alice computes 19^6 mod 23 = 2. Bob computes 8^15 mod 23 = 2.

The result, s = 2, is the shared secret.

## Why mod

<!-- claim: why-mod -->
The mod only keeps the numbers small, so that computers can store them. Plain 5^6 = 15625 would work just as well in principle.

<!-- claim: eve-stuck -->
Eve sees 8 and 19. Eve cannot get s because the numbers are too large to try.

## Who you are talking to

<!-- claim: mitm -->
Because only Bob knows b = 15, only Bob can compute s = 2. So the exchange also proves to Alice that Alice is talking to Bob. No extra authentication is needed.
