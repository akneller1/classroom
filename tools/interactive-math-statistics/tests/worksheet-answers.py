"""Independently recomputes the numeric answers in the Statistics teacher keys, using only the Python standard library
(so it runs in CI): normal distribution from statistics.NormalDist, t quantiles by numerical integration of the t density,
and the tools' fixed populations rebuilt with a Python copy of the same seeded generator (mulberry32).
Usage (repository root): python3 tools/interactive-math-statistics/tests/worksheet-answers.py"""
import math, os, sys, statistics
from statistics import NormalDist
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from worksheets_content import W
N = NormalDist(); fails = 0
def ok(c, m):
    global fails
    if not c: fails += 1; print('FAIL', m)
def num(s):   # first number in a key string
    import re; s = s.replace('−', '-').replace(',', ''); m = re.search(r'-?\d+(\.\d+)?', s); return float(m.group()) if m else None
def cell(slug, r, c): return W[slug]['record'][0]['rows'][r][c].lstrip('?')
# --- t distribution by Simpson integration of the density (independent of lab-stats.js)
def tpdf(x, df): return math.exp(math.lgamma((df + 1) / 2) - math.lgamma(df / 2)) / math.sqrt(df * math.pi) * (1 + x * x / df) ** (-(df + 1) / 2)
def tcdf(x, df, steps=4000):
    h = x / steps; s = tpdf(0, df) + tpdf(x, df)
    for i in range(1, steps): s += (4 if i % 2 else 2) * tpdf(i * h, df)
    return 0.5 + s * h / 3
def tq(p, df):
    lo, hi = 0.0, 50.0
    for _ in range(60):
        mid = (lo + hi) / 2
        if tcdf(mid, df) < p: lo = mid
        else: hi = mid
    return (lo + hi) / 2
# --- mulberry32 and Box–Muller, same operations as lab-stats.js
def rng(seed):
    a = [seed & 0xFFFFFFFF]
    def imul(x, y): return ((x & 0xFFFFFFFF) * (y & 0xFFFFFFFF)) & 0xFFFFFFFF
    def nxt():
        a[0] = (a[0] + 0x6D2B79F5) & 0xFFFFFFFF; t = a[0]
        t = imul(t ^ (t >> 15), t | 1); t ^= (t + imul(t ^ (t >> 7), t | 61)) & 0xFFFFFFFF
        return ((t ^ (t >> 14)) & 0xFFFFFFFF) / 4294967296
    return nxt
def rnorm(r):
    u = 0
    while u == 0: u = r()
    v = r(); return math.sqrt(-2 * math.log(u)) * math.cos(2 * math.pi * v)
def jsround1(x): return math.floor(x * 10 + 0.5) / 10
# Sampling distribution lab: skewed and uniform populations
def pop(kind):
    r = rng(20261108); v = []
    for i in range(1000):
        if kind == 'skew':
            while True:
                x = 1 + -6 * math.log(1 - r())
                if x <= 39: break
        else: x = 2 + 20 * r()
        v.append(max(0.05, jsround1(x)))
    return v
sk, un = pop('skew'), pop('uniform')
mu, sg, su = statistics.fmean(sk), statistics.pstdev(sk), statistics.pstdev(un)
s = 'statistics-sampling-distribution-lab'
ok(abs(mu - 6.85) < 0.005 and abs(sg - 5.66) < 0.005, 'skewed μ, σ: %.4f %.4f' % (mu, sg)); ok(abs(su - 5.68) < 0.005, 'uniform σ %.4f' % su)
g = sum(((x - mu) / sg) ** 3 for x in sk) / len(sk); ok(math.ceil((g / 0.35) ** 2) == 25, 'n for skewness < 0.35: %d' % math.ceil((g / 0.35) ** 2))
ok(abs(num(cell(s, 0, 2).split('≈')[1]) - sg / 2) < 0.006 and abs(num(cell(s, 1, 2).split('≈')[1]) - sg / 6) < 0.006 and abs(num(cell(s, 2, 2).split('≈')[1]) - su / 2) < 0.006, 'SD of x̄ rows')
ok(abs(num(cell(s, 3, 2).split('≈')[1]) - math.sqrt(0.09 / 20)) < 0.0005 and abs(num(cell(s, 4, 2).split('=')[1]) - 0.03) < 1e-9, 'SD of p̂ rows')
ok(abs((1 - N.cdf(1)) - 0.1587) < 5e-5 and abs(math.sqrt(0.08 * 0.92 / 150) - 0.0222) < 5e-5, 'sampling apply')
# Confidence intervals
s = 'statistics-confidence-interval-lab'; se40 = math.sqrt(0.24 / 40)
ok(abs(N.inv_cdf(0.95) * se40 - 0.127) < 0.0006 and abs(N.inv_cdf(0.995) * se40 - 0.200) < 0.0006 and abs(1.959964 * se40 - 0.152) < 0.0005, 'ME at 90/95/99%')
ok(abs(tq(0.975, 4) - 2.776) < 0.001 and abs(tq(0.975, 29) - 2.045) < 0.001 and abs(tq(0.975, 11) - 2.201) < 0.001, 't* values')
ok(abs(tq(0.975, 4) * 10 / math.sqrt(5) - 12.42) < 0.01 and abs(tq(0.975, 29) * 10 / math.sqrt(30) - 3.734) < 0.002, 't margins')
ok(abs((tcdf(1.959964, 4) - 0.5) * 2 - 0.8784) < 0.001, 'z* with s coverage at n = 5 ≈ 0.878')
se = math.sqrt(0.56 * 0.44 / 500); ok(abs(0.56 - 1.959964 * se - 0.5165) < 5e-5 and abs(0.56 + 1.959964 * se - 0.6035) < 5e-5, 'proportion CI apply')
ok(math.ceil((1.959964 / 0.03) ** 2 * 0.25) == 1068, 'sample size 1068')
me = tq(0.975, 11) * 2.4 / math.sqrt(12); ok(abs(501.2 - me - 499.68) < 0.006 and abs(501.2 + me - 502.72) < 0.006, 't interval apply')
# Significance and power (normal approximation)
s = 'statistics-significance-power-explorer'
pv = lambda x, n: 1 - N.cdf((x / n - 0.5) / math.sqrt(0.25 / n))
ok(round(pv(59, 100), 4) == 0.0359 and round(pv(58, 100), 4) == 0.0548 and round(2 * pv(59, 100), 4) == 0.0719, 'smallest significant count 59')
ok([round(pv(0.55 * n, n), 4) for n in (100, 200, 400)] == [0.1587, 0.0786, 0.0228], 'p̂ = 0.55 at three n')
def power(n, a, pa):
    c = 0.5 + N.inv_cdf(1 - a) * math.sqrt(0.25 / n); return 1 - N.cdf((c - pa) / math.sqrt(pa * (1 - pa) / n))
for r, (n, a, pa) in zip(W[s]['record'][0]['rows'], [(100, .05, .6), (150, .05, .6), (100, .01, .6), (100, .05, .55)]):
    ok(abs(num(r[3]) - power(n, a, pa)) < 6e-5 and abs(num(r[4]) - (1 - power(n, a, pa))) < 6e-5, 'power row %s' % r[:3])
ok(min(n for n in range(10, 1001, 10) if power(n, .05, .6) >= .8) == 160, 'smallest n with power ≥ 0.80 is 160')
z = (0.36 - 0.3) / math.sqrt(0.21 / 200); ok(abs(z - 1.85) < 0.005 and abs((1 - N.cdf(z)) - 0.032) < 0.0005, 'significance apply')
# Sampling methods: population rebuilt with the same generator
GR = [12, 12, 11, 11, 10, 10, 9, 9]; GM = {9: 8.0, 10: 7.5, 11: 7.0, 12: 6.5}; r = rng(20261108); P = []
for row in range(8):
    for col in range(20): g_ = GR[row]; P.append((g_, jsround1(GM[g_] + 0.6 * rnorm(r))))
ys = [y for _, y in P]; MU = statistics.fmean(ys)
ok(abs(MU - 7.32) < 0.005 and abs(statistics.fmean(ys[:16]) - 6.66) < 0.005 and abs(statistics.fmean(ys[:64]) - 6.80) < 0.005, 'μ and convenience means: %.4f %.4f %.4f' % (MU, statistics.fmean(ys[:16]), statistics.fmean(ys[:64])))
N0, s2 = 160, statistics.pvariance(ys); srs16 = math.sqrt(s2 / 16 * (N0 - 16) / (N0 - 1)); srs64 = math.sqrt(s2 / 64 * (N0 - 64) / (N0 - 1))
strat = math.sqrt(sum(statistics.pvariance([y for g_, y in P if g_ == gg]) / 4 * (40 - 4) / 39 for gg in GM) / 16)
ok(abs(srs16 - 0.19) < 0.006 and abs(srs64 - 0.08) < 0.005 and abs(strat - 0.145) < 0.005, 'SD of x̄, exact formulas: SRS16 %.4f SRS64 %.4f strat %.4f' % (srs16, srs64, strat))
rooms = {}
for i, (g_, y) in enumerate(P): rooms.setdefault((g_, (i % 20) // 4), []).append(y)
rm = [statistics.fmean(v) for v in rooms.values()]; R = len(rm); clus = math.sqrt(statistics.pvariance(rm) / 2 * (R - 2) / (R - 1))
ok(abs(clus - 0.39) < 0.006, 'cluster SD of x̄ (2 of 20 homerooms) %.4f' % clus)
# Conditional probability
def ppv(p, se_, sp): return p * se_ / (p * se_ + (1 - p) * (1 - sp)), p * (1 - se_) / (p * (1 - se_) + (1 - p) * sp)
s = 'statistics-conditional-probability-explorer'
for row in W[s]['record'][0]['rows']:
    a, b = ppv(num(row[0]) / 100, num(row[1]) / 100, num(row[2]) / 100)
    ok(abs(100 * a - num(row[3].split('≈')[-1])) < 0.06 and abs(100 * b - num(row[4].split('≈')[-1])) < 0.006, 'PPV row %s: %.3f %.4f' % (row[:3], 100 * a, 100 * b))
ok(abs(ppv(.1, .99, .99)[0] - 0.9167) < 5e-5 and abs(ppv(.05, .99, .99)[0] - 0.8390) < 5e-5 and abs(ppv(.05, 1, .99)[0] - 0.8403) < 5e-5 and abs(ppv(.05, .99, .995)[0] - 0.9124) < 5e-5, 'explore PPVs')
ok(abs(0.12 / 0.26 - 0.4615) < 5e-5 and abs(0.38 / 0.392 - 0.969) < 5e-4 and 45 / 75 == 0.6, 'probability apply')
# Regression (closed-form least squares)
x = [0, 1, 1, 2, 3, 4, 4, 5, 6, 7, 8, 9]; y = [48, 55, 60, 58, 66, 62, 71, 70, 77, 74, 85, 83]
def fit(x, y):
    n = len(x); mx, my = sum(x) / n, sum(y) / n; sxx = sum((a - mx) ** 2 for a in x); sxy = sum((a - mx) * (b - my) for a, b in zip(x, y)); syy = sum((b - my) ** 2 for b in y)
    b = sxy / sxx; a = my - b * mx; res = [bb - (a + b * aa) for aa, bb in zip(x, y)]
    return a, b, sxy / math.sqrt(sxx * syy), math.sqrt(sum(e * e for e in res) / (n - 2)), res
a, b, rr, ss, _ = fit(x, y)
ok(abs(a - 51.97) < 0.005 and abs(b - 3.706) < 0.0005 and abs(rr - 0.9543) < 5e-5 and abs(rr * rr - 0.9107) < 5e-5 and abs(ss - 3.552) < 5e-4, 'study LSRL')
ag = [2, 4, 6, 8, 10, 12, 14, 16, 18]; hg = [36, 42, 47, 51, 55, 58, 61, 63, 65]; ok(abs(fit(ag, hg)[2] - 0.985) < 0.0005, 'growth r')
mx = sum(x) / len(x); sx = statistics.stdev(x)
for row in W['statistics-regression-influence-lab']['record'][0]['rows']:
    ex, ey = [float(v) for v in row[0].strip('()').split(', ')]
    a2, b2, r2, s2_, res = fit(x + [ex], y + [ey]); d = (b2 - b) / abs(b)
    flags = ['yes' if abs(res[-1]) > 2 * s2_ else 'no', 'yes' if abs(ex - mx) / sx > 2 else 'no', 'yes' if abs(d) >= 0.5 else 'no']
    ok(abs(num(row[1]) - res[-1]) < 0.006 and abs(num(row[2]) - 100 * d) < 0.06 and [c.lstrip('?') for c in row[3:6]] == flags, 'extra point %s' % row[0])
ok(abs(51.973 + 3.7064 * 30 - 163.2) < 0.05 and 0.8 ** 2 == 0.6400000000000001, 'regression apply')
# Random assignment lab: exact values for the fixed 20-student data
from itertools import combinations
G = [2.06, 2.12, 2.07, 2.32, 2.5, 2.55, 2.63, 2.8, 2.9, 3.05, 3.14, 3.07, 3.25, 3.25, 3.59, 3.47, 3.64, 3.85, 3.78, 4.0]; B = [10 * v for v in G]
rand_sd = math.sqrt(0.2 * statistics.variance(B) + 9 * 0.2)
o = sorted(range(20), key=lambda k: (G[k], k)); pair_sd = math.sqrt(sum((B[o[2 * k + 1]] - B[o[2 * k]]) ** 2 for k in range(10)) / 100 + 9 * 0.2)
tot = sum(G); imb = sum(1 for c in combinations(range(20), 10) if sum(G[i] for i in c) / 10 - (tot - sum(G[i] for i in c)) / 10 >= 0.3 - 1e-9) / 184756
ok(abs(rand_sd - 3.04) < 0.01 and abs(pair_sd - 1.40) < 0.01 and abs(imb - 0.1406) < 0.0005, 'random assignment SD %.3f, pairs SD %.3f, P(imbalance ≥ 0.3) %.4f' % (rand_sd, pair_sd, imb))
ok(abs(9 / 500 - 0.018) < 1e-12, 'randomization apply')
print('statistics worksheet answers:', 'all checks passed' if not fails else '%d failed' % fails); sys.exit(1 if fails else 0)
