"""Independently recomputes the numeric answers printed in the Statistics audit lab teacher keys (#15) with scipy.
Usage (repository root): python3 tools/statistics-audit-20261118/labs/tests/worksheet-answers.py"""
import os, sys
import numpy as np
from scipy import stats
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from worksheets_content import W
fails = 0


def ok(c, m):
    global fails
    if not c:
        fails += 1
        print('FAIL', m)


def num(s):
    return float(s.lstrip('?').replace('−', '-').replace('±', ''))


N = stats.norm
tab = lambda z: round(N.cdf(round(z, 2)), 4)
rows = W['statistics-normal-curve-lab']['record'][0]['rows']
ok(abs(num(rows[0][3]) - N.sf(2)) < 6e-5 and abs(num(rows[0][4]) - (1 - tab(2))) < 1e-9, 'IQ > 130')
ok(abs(num(rows[1][3]) - N.cdf(-1.6)) < 6e-5 and abs(num(rows[1][4]) - tab(-1.6)) < 1e-9, 'height < 60')
ok(abs(num(rows[2][3]) - (N.cdf(1.5) - N.cdf(-1))) < 6e-5 and abs(num(rows[2][4]) - (tab(1.5) - tab(-1))) < 1e-9, 'scores 400–650')
ok(abs(num(rows[3][3]) - 2 * N.sf(1.96)) < 6e-5 and abs(num(rows[3][4]) - 2 * (1 - tab(1.96))) < 1e-9, 'tails 1.96')
ok(abs(100 + 15 * N.ppf(0.9) - 119.22) < 0.006, '90th percentile IQ')
ok(abs((1 - tab(1.5)) - 0.0668) < 1e-9 and abs(150 - 0.67 * 20 - 136.6) < 1e-9 and abs(tab(1) - tab(-0.5) - 0.5328) < 1e-9, 'apple apply')
ok((650 - 500) / 100 == 1.5 and (31 - 24) / 4 == 1.75, 'relative standing')


def gof(o, p):
    o = np.array(o, float); e = o.sum() * np.array(p); c = ((o - e) ** 2 / e).sum()
    return c, stats.chi2.sf(c, len(o) - 1)


claims = {'25% each': [0.25] * 4, '30%, 20%, 20%, 30%': [0.3, 0.2, 0.2, 0.3], '40%, 30%, 20%, 10%': [0.4, 0.3, 0.2, 0.1]}
for r in W['statistics-chi-square-lab']['record'][0]['rows']:
    if r[0] == 'Goodness of fit':
        c, p = gof([int(v) for v in r[2].split(', ')], claims[r[1]])
        ok(abs(num(r[3]) - c) < 6e-4 and num(r[4]) == 3 and abs(num(r[5]) - p) < 6e-5, f'gof {r[1]}: {c:.4f} {p:.5f}')
    else:
        t = np.array([[int(v) for v in half.split(', ')] for half in r[2].split(' / ')])
        c, p, d, _ = stats.chi2_contingency(t, correction=False)
        ok(abs(num(r[3]) - c) < 6e-4 and num(r[4]) == d and abs(num(r[5]) - p) < 6e-5, f'independence {c:.4f} {p:.5f}')
c, p = gof([60, 44, 56, 40], [0.25] * 4)
ok(abs(c - 5.44) < 1e-9 and abs(p - 0.1423) < 6e-5, 'doubled counts')
ok(abs((28 - 20) ** 2 / 20 - 3.2) < 1e-12 and abs(stats.chi2.ppf(0.95, 3) - 7.815) < 6e-4, 'chi-square apply')
print('FAIL' if fails else 'PASS', 'Statistics lab worksheet answers', '(%d failures)' % fails if fails else '')
sys.exit(1 if fails else 0)
