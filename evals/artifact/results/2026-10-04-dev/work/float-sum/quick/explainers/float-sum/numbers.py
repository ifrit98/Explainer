from decimal import Decimal as D
import math

for x in [0.1, 0.2, 0.3, 0.1 + 0.2]:
    print(repr(x), D(x), x.hex())
print("errors", D(0.1) - D("0.1"), D(0.2) - D("0.2"), D(0.3) - D("0.3"))
print("exact sum", D(0.1) + D(0.2))
print("gap", D(0.1 + 0.2) - D(0.3))
print("ulp(0.3)", D(math.ulp(0.3)))
print(0.5 + 0.25 == 0.75, abs(0.1 + 0.2 - 0.3) < 1e-9, 0.1 + 0.2 - 0.3)
