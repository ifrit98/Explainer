# Narrative: key-exchange

## 1. Reader before and after

- **Before:** A technical reader: school mathematics (powers, the rule (x^a)^b = x^(ab), logarithms, remainders) and basic programming. Knows a key is the secret an encryption method needs. New to cryptography: does not know "mod", one-way operations, or the discrete logarithm.
- **After:** "Each side keeps a private number and sends g to that power, mod p. Each raises the other's public number to its own private number, and both get g^(ab) mod p. An eavesdropper sees only g^a and g^b, and no known fast method gets a or b back from them. It stops readers, not attackers who change messages."

## 2. Question and motive

- **Question:** How can two people who have never met agree on a secret key when everything they send can be read? Result in words: they never send the key. Each sends half of a calculation; each finishes it with a number they kept; both reach the same number; a reader cannot finish it.
- **Why care:** every HTTPS connection starts with a stranger (a web server) and an open network. Encryption needs a shared key first.
- **Why this approach:** the key cannot travel, so it must be computed on both sides from what travels plus something that does not.

## 3. Introduction ledger

| Reference | Means | Grounded by (a concrete instance) | Beat |
|---|---|---|---|
| Alice, Bob, Eve | the two parties; the eavesdropper who reads everything | — | 1 |
| mod p | remainder after division by p | 100 mod 23 = 8 | 4 |
| p, g | public modulus (prime) and base | p = 23, g = 5 | 4 |
| private number a, b | kept, never sent | a = 6, b = 15 | 4 |
| public number A, B | g^a mod p, g^b mod p; sent | A = 8, B = 19 | 4 |
| shared secret s | what both compute; becomes the key | s = 2 | 5 |
| one-way operation | fast forward, no known fast reverse | 5^x mod 23 | 7 |
| discrete logarithm | finding x from g^x mod p | find 6 from 8 | 7 |
| repeated squaring | computing a power by squaring and reducing at each step | 5^6 via 5^2 → 2, 5^3 → 10, 5^6 → 8 | 8 |
| Mallory | an attacker who changes messages | replaces A and B with 10 | 9 |

## 4. Beats

| # | Kind | Reader's question | Bridge | Shown | Said | Reader now knows |
|---|---|---|---|---|---|---|
| 1 | hook | How can strangers share a secret in public? | — | the setting | Everything sent is read by Eve. So the key can never be sent. | the constraint |
| 2 | close (answer first) | So what do they do? | therefore | — | They compute it: each sends half a calculation, finishes the other's half with a kept number; both reach the same number; Eve cannot finish it. | the shape of the answer |
| 3 | objection | Why not one secret, hidden by a one-way operation? | but | Alice picks the key 6 and sends a scrambled form, 8 | Bob gets only 8, the same as Eve, so Bob would be as stuck as Eve. Each side needs a private number, and an operation where each can finish the other's half. | why two private numbers |
| 4 | name / instance | What operation? | so | numbers, then letters | "mod 23" means the remainder after division by 23 (100 mod 23 = 8). Public: p = 23, g = 5. Alice keeps a = 6, sends A = 5^6 mod 23 = 15625 mod 23 = 8. Bob keeps b = 15, sends B = 5^15 mod 23 = 19. | the protocol |
| 5 | mechanism | Do they really get the same number? | then | 19^6 mod 23 = 2; 8^15 mod 23 = 2 | Yes. Both are 5^(6×15) mod 23 by (g^a)^b = (g^b)^a. Taking the remainder early does not change the final remainder: dropping a multiple of 23 from a factor drops a multiple of 23 from the product (125 mod 23 = 10 = 2 × 5). | agreement |
| 6 | notice | What does Eve have? | but | table: who knows what, walked through | p, g, A, B. Not a, b, s. A × B mod 23 = 14 = 5^(6+15), not 2. | Eve's view |
| 7 | why | Why powers, why mod? | so | two failing alternatives, then the list | If A = 5 × 6 mod 23 = 7: multiply by 14 (since 5 × 14 = 70 = 3 × 23 + 1) to get 6. If A = 5^6 = 15625 with no mod: log₅ = 6. With both: the list of 5^1 … 5^22 mod 23 jumps around, so Eve can only try exponents one by one. Name: one-way operation; the reverse is the discrete logarithm. | one-way operation |
| 8 | quantity | Then p = 23 falls in 6 tries — so? | but | sizes | Real p: 617 digits; best known methods ~10^14 years (estimate). Alice computes fast by squaring and reducing (5^6: 5^2 → 2, 5^3 → 10, 5^6 → 8). Hardness is believed, not proven. | size matters, assumption |
| 9 | limit | Am I safe from everyone? | but | Mallory numbers | Mallory picks 3 and sends 5^3 mod 23 = 10 to both. Alice gets 10^6 mod 23 = 6, Bob gets 10^15 mod 23 = 5. Mallory computes 8^3 mod 23 = 6 and 19^3 mod 23 = 5, so Mallory decrypts and re-encrypts. Fix: authentication (out of scope). | limit |
| 10 | close | — | so | — | They never send the key. Each sends g to a private power, mod p; each finishes the other's half; both get g^(ab) mod p. Eve sees only g^a and g^b. Next: authentication, elliptic curves. | recap |

## 5. Concrete to symbol

Numbers first (5^6 mod 23 = 8), then "here g = 5, a = 6, p = 23", then A = g^a mod p.

## 6. Links between representations

The who-knows-what table matches the numbers in beat 4–5.

## 7. Close the loop

- **Answer:** They never send the key. Each sends g^(private) mod p, and each raises the other's public number to its own private number. Both get g^(ab) mod p.
- **General argument:** exponent rule gives agreement; discrete logarithm hardness (assumed) keeps Eve out.
- **Payoff:** this is how HTTPS starts (today mostly an elliptic-curve version). Next: authentication, elliptic curves.
