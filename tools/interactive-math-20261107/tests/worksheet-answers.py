"""Independently recomputes the numeric answers printed in the 2026-11-07 teacher keys.
Usage (repository root): python3 tools/interactive-math-20261107/tests/worksheet-answers.py"""
import math, itertools, statistics, sys, os
from fractions import Fraction as Fr
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from worksheets_content import W
fails = 0
def ok(c, m):
    global fails
    if not c: fails += 1; print('FAIL', m)
def cell(slug, ti, r, c): return W[slug]['record'][ti]['rows'][r][c].lstrip('?')
# Ratio tables
s = 'math6-ratio-double-number-line'
ok(cell(s, 0, 1, 1) == '10' and cell(s, 0, 2, 0) == '12' and cell(s, 0, 3, 1) == '{5/2}' and cell(s, 0, 4, 0) == '{3/5}', 'ratio table')
ok(Fr(7, 2) == Fr(7, 2) * 1 and cell(s, 1, 0, 3) == '3{1/2}', 'road trip unit rate')
# Fraction division pieces (L = lcm of denominators)
def pieces(an, ad, dn, dd):
    L = ad * dd // math.gcd(ad, dd); return an * L // ad, dn * L // dd, Fr(an, ad) / Fr(dn, dd)
for row, args in zip(W['math6-fraction-division-groups']['record'][0]['rows'], [(2, 1, 1, 4), (3, 1, 3, 4), (3, 4, 1, 2), (4, 1, 5, 2)]):
    A, D, q = pieces(*args); ok(row[1] == '?' + str(A) and row[2] == '?' + str(D), 'pieces ' + row[0])
ok(Fr(7, 8) / Fr(1, 4) == Fr(7, 2) and Fr(3, 2) / Fr(3, 8) == 4 and 4 / Fr(2, 3) == 6, 'fraction apply')
# Dot plot stats with exclusive quartiles
def st(d):
    d = sorted(d); n = len(d); h = n // 2; lo, hi = d[:h], d[h + (n % 2):]; m = sum(d) / n
    return m, statistics.median(d), d[-1] - d[0], statistics.median(hi) - statistics.median(lo), sum(abs(x - m) for x in d) / n
for row in W['math6-balance-point-dot-plot']['record'][0]['rows']:
    d = [int(x) for x in row[0].split(', ')]; got = [float(c.lstrip('?')) for c in row[1:]]
    ok(all(abs(a - b) < 1e-9 for a, b in zip(st(d), got)), 'dot plot ' + row[0] + ' ' + str(st(d)))
ok(abs(sum([5, 6, 6, 7, 8, 8, 9, 10, 20]) / 9 - 79 / 9) < 1e-12, 'outlier mean')
# Proportional table
for row, (p, f) in zip(W['prealgebra7-proportional-relationships']['record'][0]['rows'], [(1.5, 0), (2, 3), (4, 0), (0.5, 6)]):
    ok(row[3] == '?$' + ('%g' % (6 * p + f)), 'prop cost ' + row[0]); ok((row[4] == '?yes') == (f == 0), 'prop yes/no')
ok([(2.5 * x + 4) / x for x in (1, 2, 4)] == [6.5, 4.5, 3.5], 'prop y/x with fee')
# Percent table
for row, (A, ms) in zip(W['prealgebra7-percent-change-bar']['record'][0]['rows'], [(60, [0.85]), (40, [1.3, 0.9]), (120, [0.75, 1.25]), (200, [1.1, 1.1])]):
    fin = A * math.prod(ms); ok(row[3] == '?$%.2f' % fin, 'percent final ' + row[0] + ' %.2f' % fin)
    ov = (math.prod(ms) - 1) * 100; ok(row[4].lstrip('?') == ('+' if ov > 0 else '−') + ('%g' % round(abs(ov), 4)) + '%', 'percent overall ' + row[4])
ok(round(250 * 0.7 * 1.06, 2) == 185.5 and round(36 * 1.15, 2) == 41.4 and 32 / 0.8 == 40, 'percent apply')
# Spinner table
for row in W['prealgebra7-spinner-probability-lab']['record'][0]['rows']:
    parts = [int(x) for x in row[0].split(', ')]; p = Fr(parts[0], sum(parts))
    fs = lambda f: str(f.numerator) if f.denominator == 1 else '{%d/%d}' % (f.numerator, f.denominator)
    ok(row[1] == '?' + fs(p) and row[2] == '?' + fs(1 - p) and row[3] == '?' + str(p * 300), 'spinner ' + row[0])
# Pythagorean rows: classification and buildable on the tool's grid (corners 0..10 × 0..8)
pts = [(x, y) for x in range(11) for y in range(9)]
def buildable(a2, b2, c2):
    for A in [(0, 0), (3, 3)]:
        for B in pts:
            if (B[0] - A[0]) ** 2 + (B[1] - A[1]) ** 2 != a2: continue
            for C in pts:
                s2 = sorted([a2, (C[0] - A[0]) ** 2 + (C[1] - A[1]) ** 2, (C[0] - B[0]) ** 2 + (C[1] - B[1]) ** 2])
                if s2 == sorted([a2, b2, c2]) and (B[0] - A[0]) * (C[1] - A[1]) != (B[1] - A[1]) * (C[0] - A[0]): return True
    return False
for row in W['prealgebra-pythagorean-squares']['record'][0]['rows']:
    a2, b2, c2 = int(row[0]), int(row[1]), int(row[2].lstrip('?')); kind = 'right' if a2 + b2 == c2 else 'acute' if a2 + b2 > c2 else 'obtuse'
    ok(row[4].lstrip('?').startswith(kind), 'pythag type ' + str((a2, b2, c2))); ok(buildable(a2, b2, c2), 'pythag buildable ' + str((a2, b2, c2)))
ok(abs(math.degrees(math.acos((5 + 10 - 13) / (2 * math.sqrt(50)))) - 81.87) < 0.01, 'near-right angle')
ok(13 ** 2 - 12 ** 2 == 25 and 81 + 1600 == 41 ** 2, 'pythag apply')
# Square roots
for row in W['prealgebra-square-roots-number-line']['record'][0]['rows']:
    A = int(row[0]); r = math.isqrt(A)
    if r * r == A: ok('exactly' in row[1] and row[3] == '?rational', 'sqrt perfect ' + row[0]); continue
    lo = math.floor(math.sqrt(A) * 10) / 10
    ok(row[1] == '?%d and %d' % (r, r + 1) and row[2] == '?%.1f and %.1f' % (lo, lo + 0.1) and row[3] == '?irrational', 'sqrt row ' + row[0])
ok(6.32 ** 2 < 40 < 6.33 ** 2 and 4.47 ** 2 > 19.95 and 4.48 ** 2 > 20.05 and 4.46 ** 2 < 19.95, 'sqrt explore')
# Vectors
for row in W['precalculus-vector-explorer']['record'][0]['rows']:
    u = [float(x.replace('−', '-')) for x in row[0].strip('⟨⟩').split(', ')]; v = [float(x.replace('−', '-')) for x in row[1].strip('⟨⟩').split(', ')]
    f = lambda w: '⟨' + ', '.join(('%g' % c).replace('-', '−') for c in w) + '⟩'
    ok(row[2] == '?' + f([u[0] + v[0], u[1] + v[1]]) and row[3] == '?' + f([u[0] - v[0], u[1] - v[1]]) and row[4] == '?' + f([2 * u[0], 2 * u[1]]) and row[5] == '?%g' % math.hypot(u[0] + v[0], u[1] + v[1]), 'vector row ' + row[0])
ok(abs(math.hypot(260, 30) - 261.7) < 0.05, 'plane speed')
# Secant table
for row, (f, a) in zip(W['calculus-secant-to-tangent']['record'][0]['rows'], [(lambda x: x * x, 2), (lambda x: x ** 3 - 3 * x, 1), (math.exp, 0), (math.sin, 0)]):
    q = lambda h: (f(a + h) - f(a)) / h
    ok(row[2] == '?%.4f' % q(0.01) or row[2] == '?%g' % round(q(0.01), 4), 'secant + ' + row[0] + ' %.4f' % q(0.01))
    ok(row[3].replace('−', '-') == '?%.4f' % q(-0.01) or row[3].replace('−', '-') == '?%g' % round(q(-0.01), 4), 'secant − ' + row[0] + ' %.4f' % q(-0.01))
# Riemann
def R(f, a, b, n, m):
    dx = (b - a) / n; xs = [a + i * dx for i in range(n)]
    return sum((f(x) if m == 'l' else f(x + dx) if m == 'r' else f(x + dx / 2) if m == 'm' else (f(x) + f(x + dx)) / 2) * dx for x in xs)
up = lambda x: x * x / 4 + 1; cap = lambda x: 4 - x * x; cub = lambda x: x ** 3 / 8 - x
ok([round(R(up, 0, 4, n, 'l'), 4) for n in (4, 20, 100)] == [7.5, 8.94, 9.2536], 'riemann left sums'); ok(R(up, 0, 4, 4, 'm') == 9.25, 'riemann mid')
rows = W['calculus-riemann-sum-lab']['record'][0]['rows']
for row, val in zip(rows, [R(up, 0, 4, 4, 'r'), R(cap, 0, 2, 4, 'l'), R(cap, 0, 2, 4, 'm'), R(cub, -2, 2, 4, 't')]): ok(abs(float(row[3].lstrip('?')) - val) < 1e-9, 'riemann row ' + row[0])
ok(abs((4 * 4 - 64 / 3) - (8 - 8 / 3) + 32 / 3) < 1e-12, '∫ 4 − x² on [2, 4] = −32/3')
# Accumulation
pw = [(0, -1), (1, -1), (3, 2), (5, 2), (6, -1)]
def pwA(x):
    s = 0
    for (x0, y0), (x1, y1) in zip(pw, pw[1:]):
        if x <= x0: break
        e = min(x, x1); ye = y0 + (y1 - y0) * (e - x0) / (x1 - x0); s += (y0 + ye) / 2 * (e - x0)
    return s
vals = [(lambda x, a: (2 * x - x * x / 2) - (2 * a - a * a / 2), 0, 3), (lambda x, a: -2 * math.cos(x) + 2 * math.cos(a), 0, 2), (lambda x, a: pwA(x) - pwA(a), 0, 1), (lambda x, a: pwA(x) - pwA(a), 0, 3), (lambda x, a: (2 * x - x * x / 2) - (2 * a - a * a / 2), 1, 3)]
for row, (A, a, x) in zip(W['calculus-accumulation-ftc']['record'][0]['rows'], vals): ok(abs(float(row[3].lstrip('?').replace('−', '-')) - round(A(x, a), 2)) < 1e-9, 'A row %s %g' % (row[0], A(x, a)))
ok(abs(2 * math.sin(4) + 1.51) < 0.01 and abs(2 * math.sin(1.6) - 2) < 0.005, 'wave slopes')
print('worksheet answers:', 'all checks passed' if not fails else str(fails) + ' failed'); sys.exit(1 if fails else 0)
