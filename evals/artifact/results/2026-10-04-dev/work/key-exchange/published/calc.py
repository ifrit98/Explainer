p, g, a, b = 23, 5, 6, 15
A = pow(g, a, p); B = pow(g, b, p)
print("A B sA sB", A, B, pow(B, a, p), pow(A, b, p))
print("powers", [pow(g, k, p) for k in range(1, 23)])
print("plain", 5**6, 5**15, "A*B", A * B % p, "g^(a+b)", pow(g, a + b, p))
print("mult", g * a % p, g * b % p, "inv g", pow(g, -1, p), "g*a*b", g * a * b % p)
print("bits 2048 digits", len(str(2**2048)))
