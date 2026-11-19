"""Independently recomputes the numeric answers printed in the Grade 7 audit lab teacher keys (#15).
Usage (repository root): python3 tools/grade7-audit-20261119/labs/tests/worksheet-answers.py"""
import math, os, re, sys
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


# Integer chips: answer, zero pairs (pairs of opposite chips after rewriting as a sum), distance
for r in W['grade7-integer-chips-lab']['record'][0]['rows']:
    m = re.fullmatch(r'(−?\d+) ([+−]) \(?(−?\d+)\)?', r[0]); a, b = num(m.group(1)), num(m.group(3))
    s = -b if m.group(2) == '−' else b
    pos, neg = max(a, 0) + max(s, 0), max(-a, 0) + max(-s, 0)
    want = r[1].lstrip('?').replace('(', '').replace(')', '')
    got = ('%d' % a).replace('-', '−') + (' + ' + ('%d' % s).replace('-', '−'))
    ok(want == got, f'{r[0]} rewritten: {want} vs {got}')
    ok(num(r[2]) == min(pos, neg), f'{r[0]} zero pairs')
    ok(num(r[3]) == a + s, f'{r[0]} answer')
    ok(num(r[4]) == abs(a - b), f'{r[0]} distance')
ok(-3 + 5 == 2 and -4 + -6 == -10 and 4 - (-2) == 6 and -7 + 7 == 0, 'integer explore')
ok(-8 + 15 == 7 and -120 - 45 == -165 and 12 - (-9) == 21 and abs(-14 - 6) == 20, 'integer apply')

# Circles
pi_ = lambda s: float(s.lstrip('?').rstrip('π') or 1)
for r in W['grade7-circles-lab']['record'][0]['rows']:
    R = float(r[0])
    ok(num(r[1]) == 2 * R, f'r={R} d')
    ok(abs(pi_(r[2]) - 2 * R) < 1e-12 and abs(num(r[3]) - round(2 * math.pi * R, 2)) < 1e-9, f'r={R} C')
    ok(abs(pi_(r[4]) - R * R) < 1e-12 and abs(num(r[5]) - round(math.pi * R * R, 2)) < 1e-9, f'r={R} A')
ok(round(6 * math.pi, 2) == 18.85 and round(4 * math.pi, 2) == 12.57 and round(8 * math.pi, 2) == 25.13, 'circle explore C')
ok(round(16 * math.pi, 2) == 50.27 and round(25 * math.pi, 2) == 78.54 and abs(2 * math.pi * 5 - 31.4) < 0.1, 'circle explore A')
ok(abs(3.14 * 26 - 81.64) < 1e-9 and abs(3.14 * 9 - 28.26) < 1e-9 and abs(18.84 / 3.14 - 6) < 1e-9 and (12 ** 2) / (6 ** 2) == 4, 'circle apply')
# Scale drawings: the room is 24 ft by 18 ft, 360 square feet
for r in W['grade7-scale-drawing-lab']['record'][0]['rows']:
    sc = float(r[0].split(': ')[1].split()[0])
    ok(num(r[1]) == 24 / sc and num(r[2]) == 18 / sc and abs(num(r[3]) - 360 / sc ** 2) < 1e-9, f'scale {r[0]}')
ok(24 * 12 + 12 * 6 == 360 and 360 / 16 == 22.5 and 360 / 4 / (360 / 16) == 4 and 6 / 4 == 1.5 and 360 / 9 == 40, 'scale explore')
ok(abs(3.2 * 25 - 80) < 1e-9 and (30 / 5, 20 / 5) == (6, 4) and 5 / 2 == 2.5 and 2.5 ** 2 == 6.25 and abs(4.2 / 24 * 100 - 17.5) < 1e-9, 'scale apply')
print('FAIL' if fails else 'PASS', 'Grade 7 lab worksheet answers', '(%d failures)' % fails if fails else '')
sys.exit(1 if fails else 0)
