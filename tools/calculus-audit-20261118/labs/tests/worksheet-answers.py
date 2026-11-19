"""Independently recomputes the numeric answers printed in the Calculus audit lab teacher keys (#16).
Usage (repository root): python3 tools/calculus-audit-20261118/labs/tests/worksheet-answers.py"""
import math, os, sys
from fractions import Fraction as Fr
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from worksheets_content import W
fails = 0


def ok(c, m):
    global fails
    if not c:
        fails += 1
        print('FAIL', m)


def num(s):
    return float(s.lstrip('?').replace('−', '-'))


# Related rates table: y = √(L² − x²), dy/dt = −x·r/y, dA/dt = (r/2)(y − x²/y)
for row in W['calculus-related-rates-lab']['record'][0]['rows']:
    L, r, x = (float(v) for v in row[:3])
    y = math.sqrt(L * L - x * x)
    for got, want in zip(row[3:], [y, -x * r / y, r / 2 * (y - x * x / y)]):
        ok(abs(num(got) - want) < 6e-4, f'ladder {row[:3]}: {got} vs {want:.4f}')
ok(abs(13 * 2 / math.sqrt(5) - 11.63) < 0.005 and abs(13 / math.sqrt(2) - 9.19) < 0.005, 'ladder special points')
ok(Fr(-8 * 3, 2 * 6) == -2 and abs(-1.5 / 6 + 0.25) < 1e-12 and abs(30 * math.pi - 94.2) < 0.05 and Fr(2, 3) * 4 == Fr(8, 3), 'ladder apply')

# Particle motion: exact antiderivatives and distance split at the zeros of v
FN = {'t² − 5t + 4': (lambda t: t * t - 5 * t + 4, lambda t: 2 * t - 5, lambda t: t ** 3 / 3 - 5 * t * t / 2 + 4 * t, [1, 4]),
      '4 − 2t': (lambda t: 4 - 2 * t, lambda t: -2, lambda t: 4 * t - t * t, [2]),
      '3 sin(πt/3)': (lambda t: 3 * math.sin(math.pi * t / 3), lambda t: math.pi * math.cos(math.pi * t / 3), lambda t: -9 / math.pi * math.cos(math.pi * t / 3), [3])}


def motion(name, T):
    v, a, V, zs = FN[name]
    cuts = [0] + [z for z in zs if z < T] + [T]
    return V(T) - V(0), v(T), a(T), V(T) - V(0), sum(abs(V(q) - V(p)) for p, q in zip(cuts, cuts[1:]))


for row in W['calculus-particle-motion-lab']['record'][0]['rows']:
    want = motion(row[0], float(row[1]))
    for got, w in zip(row[2:], want):
        ok(abs(num(got) - w) < 6e-4, f'motion {row[:2]}: {got} vs {w:.4f}')
V = FN['t² − 5t + 4'][2]
ok(abs(V(1) - 11 / 6) < 1e-12 and abs(V(4) + 8 / 3) < 1e-12 and abs(V(6) - 6) < 1e-12, 'motion explore x values')
ok(motion('4 − 2t', 4)[0] == 0 and motion('4 − 2t', 4)[4] == 8, 'back at start')
d = motion('3 sin(πt/3)', 6)
ok(abs(d[0]) < 1e-12 and abs(d[4] - 36 / math.pi) < 1e-12 and abs(36 / math.pi - 11.459) < 5e-4, 'wave distance')
ok(5 + (27 - 36) == -4 and abs(8 - 24) + abs((27 - 36) - (8 - 24)) == 23, 'apply 3t² − 12')
ok(abs(math.sin(math.pi)) < 1e-12, 'cos displacement')
print('PASS lab worksheet answers' if not fails else f'{fails} failures')
sys.exit(1 if fails else 0)
