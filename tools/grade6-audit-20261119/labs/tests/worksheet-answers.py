"""Independently recomputes the numbers printed in the Grade 6 audit lab teacher keys (#16).
Usage (repository root): python3 tools/grade6-audit-20261119/labs/tests/worksheet-answers.py"""
import os, re, sys
from fractions import Fraction as Fr
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from worksheets_content import W
fails = 0


def ok(c, m):
    global fails
    if not c:
        fails += 1
        print('FAIL', m)


def F(s):
    s = s.lstrip('?').split(' ')[0]
    m = re.fullmatch(r'(\d*)\{(\d+)/(\d+)\}', s)
    return (int(m[1] or 0) + Fr(int(m[2]), int(m[3]))) if m else Fr(s)


for r in W['grade6-fraction-cubes-lab']['record'][0]['rows']:
    l, w, h = F(r[0]), F(r[1]), F(r[2])
    n = [int(x * 2) for x in (l, w, h)]
    ok(r[3].lstrip('?') == ', '.join(map(str, n)), f'{r[:3]} cubes per edge')
    ok(int(r[4].lstrip('?')) == n[0] * n[1] * n[2], f'{r[:3]} number of cubes')
    ok(F(r[5]) == Fr(n[0] * n[1] * n[2], 8) == F(r[6]) == l * w * h, f'{r[:3]} volume')
ok(2 * Fr(3, 2) * 1 == 3 and 4 * 3 * 2 == 24 and 24 * Fr(1, 8) == 3 and 5 * 4 * 3 == 60 and 60 * Fr(1, 8) == Fr(15, 2) and 4 ** 3 == 64, 'cubes explore')
ok(Fr(5, 2) * Fr(3, 2) == Fr(15, 4) and 8 * 5 * 6 == 240 and Fr(27, 4) * 2 == Fr(27, 2) and 15 / (3 * Fr(5, 2)) == 2, 'cubes apply')

for r in W['grade6-nets-lab']['record'][0]['rows']:
    l, w, h = int(r[0]), int(r[1]), int(r[2].split()[0])
    op = 'open' in r[2]
    ok(int(r[3].lstrip('?')) == l * w and int(r[4].lstrip('?')) == l * h and int(r[5].lstrip('?')) == w * h, f'{r[:3]} faces')
    ok(int(r[6].lstrip('?')) == 2 * (l * w + l * h + w * h) - (l * w if op else 0), f'{r[:3]} SA')
ok(2 * (12 + 8 + 6) == 52 and 6 * 9 == 54 and 2 * (20 + 15 + 12) - 20 == 74 and 2 * (12 + 12 + 4) == 56, 'nets explore')
ok(2 * (16 + 96 + 24) == 272 and 6 * 25 == 150 and 2 * (8 + 4 + 2) - 8 == 20 and 2 * (60 + 40 + 24) == 248, 'nets apply')
print('FAIL' if fails else 'PASS', 'Grade 6 lab worksheet answers', '(%d failures)' % fails if fails else '')
sys.exit(1 if fails else 0)
