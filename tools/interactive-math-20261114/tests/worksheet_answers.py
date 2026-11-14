"""Recomputes the numerical answers printed in the 2026-11-14 worksheets and keys (python3 worksheet_answers.py)."""
import math
from fractions import Fraction as F
def ok(cond, msg): assert cond, msg
d = math.degrees; s = lambda A: math.sin(math.radians(A))
# rational exponents
ok(round(27 ** (2 / 3)) == 9 and round(32 ** 0.6) == 8 and 32 ** 3 == 32768 and abs(4 ** -1.5 - 1 / 8) < 1e-12 and abs(125 ** (-2 / 3) - 1 / 25) < 1e-12 and round(16 ** 1.5) == 64 and round(9 ** 1.5) == 27, "exponents")
# ambiguous case, b = 10
ok(abs(10 * s(35) - 5.74) < 0.005, "h 35")
B = d(math.asin(10 * s(35) / 7)); ok(round(B, 1) == 55.0 and round(180 - B, 1) == 125.0, "B 35/7")
B = d(math.asin(10 * s(30) / 8)); ok((round(B, 1), round(180 - B, 1)) == (38.7, 141.3) and 30 + 141.3 < 180, "a=8")
B = d(math.asin(10 * s(30) / 12)); ok(round(B, 1) == 24.6 and 30 + 180 - B > 180, "a=12 one")
ok(round(d(math.asin(10 * s(120) / 12)), 1) == 46.2, "obtuse")
ok(abs(12 * s(40) - 7.71) < 0.005, "apply h")
B = d(math.asin(18 * s(30) / 12)); ok((round(B, 1), round(180 - B, 1)) == (48.6, 131.4), "apply B")
# matrices
ok((3 * 2 + 1 * -1, 0 * 2 + 2 * -1) == (5, -2) and 2 * 3 - 1 * 1 == 5, "matrix")
# box
V = lambda W, Lg, x: x * (W - 2 * x) * (Lg - 2 * x)
xs = lambda W, Lg: ((W + Lg) - math.sqrt((W + Lg) ** 2 - 3 * W * Lg)) / 6
for W_, L_, x_, v_ in [(12, 12, 2, 128), (6, 6, 1, 16), (10, 16, 2, 144), (9, 24, 2, 200)]:
    ok(abs(xs(W_, L_) - x_) < 1e-12 and V(W_, L_, x_) == v_, (W_, L_))
ok(abs(xs(8, 15) - 5 / 3) < 1e-12 and abs(V(8, 15, 5 / 3) - 2450 / 27) < 1e-9 and round(2450 / 27, 2) == 90.74, "8x15")
dV = lambda x: 12 * x * x - 96 * x + 144
ok((dV(1), dV(2), dV(3)) == (60, 0, -36), "dV")
ok(2 ** 3 - 24 == -16 and 27 - 36 == -9, "x^3-12x")
# area and volume (midpoint error and exact values by numeric integration)
def integ(f, a, b, n=200000):
    h = (b - a) / n; return sum(f(a + (i + .5) * h) for i in range(n)) * h
for f, g, a, b, A, Vv in [(lambda x: x, lambda x: x * x, 0, 1, 1 / 6, 2 * math.pi / 15), (lambda x: 2 * x, lambda x: x * x, 0, 2, 4 / 3, 64 * math.pi / 15),
                          (math.sqrt, lambda x: x / 2, 0, 4, 4 / 3, 8 * math.pi / 3), (lambda x: 4 - x * x, lambda x: 0, -2, 2, 32 / 3, 512 * math.pi / 15)]:
    ok(abs(integ(lambda x: f(x) - g(x), a, b) - A) < 1e-8 and abs(math.pi * integ(lambda x: f(x) ** 2 - g(x) ** 2, a, b) - Vv) < 1e-7, A)
mid10 = sum(((i + .5) / 10 - ((i + .5) / 10) ** 2) / 10 for i in range(10)); ok(abs(mid10 - 1 / 6) < 0.001, "n=10")
ok(abs(math.pi * integ(lambda x: x, 0, 9) - 81 * math.pi / 2) < 1e-7 and abs(math.pi * integ(lambda x: 1 - x ** 4, -1, 1) - 8 * math.pi / 5) < 1e-7, "apply vol")
# Euler
ok(1.5 ** 4 == 5.0625 and round(1.05 ** 40, 2) == 7.04 and round(1.1 ** 20, 2) == 6.73 and abs(1.05 ** 40 - math.e ** 2) < 0.5 and abs(1.1 ** 20 - math.e ** 2) > 0.5, "euler y")
x, y, rows = 0, 1, []
for _ in range(4):
    sl = x + y; ny = y + .5 * sl; rows.append((x, y, sl, ny)); x, y = x + .5, ny
ok(rows == [(0, 1, 1, 1.5), (0.5, 1.5, 2.0, 2.5), (1.0, 2.5, 3.5, 4.25), (1.5, 4.25, 5.75, 7.125)], rows)
ok(abs(3 + .1 * (2 - 3) - 2.9) < 1e-12, "euler apply")
print("all worksheet answers check")
