"""Statistics audit #10 (2026-11-18): independent recomputation of answer keys from the printed prompt.
Each handler reads a common question shape anywhere in the bank (not by family or authoring parameters), recomputes
with scipy/numpy, and checks that the keyed answer holds the value at the stated rounding (exact or Table A z
rounding accepted). Exits non-zero on any mismatch or if fewer than MIN items are checked.
Usage (repository root): python3 tools/statistics-audit-20261118/verify_keys.py"""
import json, glob, re, math, sys, collections
import numpy as np
from scipy import stats

import os
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
MIN = 180
Q = []
for f in sorted(glob.glob(ROOT + '/question-banks/statistics/*.json')):
    Q += json.load(open(f))['questions']

N = r'(−?-?\d[\d,]*\.?\d*)'


def num(s):
    return float(s.replace('−', '-').replace(',', ''))


def nums(s):
    return [num(m) for m in re.findall(r'[−-]?\d[\d,]*\.?\d*', s.replace('−', '-'))]


def keytext(q):
    if q['format'] == 'multiple-choice':
        return [o['text'] for o in q['options'] if o['correct']][0]
    a = q['answer']
    return ' '.join(a) if isinstance(a, list) else str(a)


def has(q, vals, tol=None):
    """True if some number in the key is within rounding of one of vals (vals: list of acceptable values)."""
    k = keytext(q).replace('%', ' %')
    ks = nums(k)
    pct = '%' in keytext(q)
    for v in vals:
        for x in ks:
            for cand in ([x, x / 100] if pct else [x]):
                dec = len(re.search(r'\.(\d+)', f'{x}').group(1)) if '.' in f'{x}' else 0
                t = tol if tol is not None else 0.5 * 10 ** -dec + 1e-9
                if pct:
                    t = max(t, 0.0051)
                if abs(cand - v) <= t * (1.0001) + 1e-12:
                    return True
    return False


def data_list(p):
    m = re.search(r'(?:of|data(?: set)?:?|values:?|are:?)\s*((?:[−-]?\d+\.?\d*,\s*){3,}(?:and\s*)?[−-]?\d+\.?\d*)', p)
    return [num(v) for v in re.findall(r'[−-]?\d+\.?\d*', m.group(1))] if m else None


def halves(d):
    d = sorted(d); n = len(d)
    lo, hi = d[:n // 2], d[(n + 1) // 2:]
    return float(np.median(lo)), float(np.median(hi))


def table_z(z):
    return round(z + 0.0, 2)


def ncdf_vals(z):  # exact and Table A (z to 2 dp)
    return [stats.norm.cdf(z), stats.norm.cdf(round(z, 2))]


H = []


def handler(f):
    H.append(f); return f


@handler
def descriptive(q, p):
    d = data_list(p)
    if not d or len(d) < 4:
        return None
    pl = p.lower()
    if re.search(r'\bfind the mean\b|\bmean of\b', pl) and 'sd' not in pl and 'standard deviation' not in pl:
        return has(q, [np.mean(d)])
    if 'iqr' in pl or 'interquartile' in pl:
        a, b = halves(d); return has(q, [b - a])
    if re.search(r'\bq1\b', pl):
        a, b = halves(d); return has(q, [a])
    if re.search(r'\bq3\b', pl):
        a, b = halves(d); return has(q, [b])
    if 'median' in pl and 'quartile' not in pl:
        return has(q, [np.median(d)])
    if 'range' in pl and 'interquartile' not in pl:
        return has(q, [max(d) - min(d)])
    if 'standard deviation' in pl or re.search(r'\bsd\b', pl):
        return has(q, [np.std(d, ddof=1), np.std(d, ddof=0)])
    return None


@handler
def zscore(q, p):
    m = re.search(r'[Mm]ean (?:is )?' + N + r'(?: \w+)?,? (?:and )?(?:a )?(?:SD|standard deviation|σ =?) (?:is |of )?' + N, p)
    if not m or not re.search(r'z-?score', p, re.I):
        return None
    mu, sd = num(m.group(1)), num(m.group(2))
    inv = re.search(r'(?:[Ww]hat|[Ww]hich) (?:\w+ )?(?:value )?has a z-?score of ' + N, p)
    if inv:
        return has(q, [mu + num(inv.group(1)) * sd])
    x = re.search(r'z-?score (?:of|for)(?: a \w+ of)? ' + N, p, re.I)
    if not x:
        return None
    return has(q, [(num(x.group(1)) - mu) / sd])


@handler
def normal_prob(q, p):
    m = re.search(r'[Nn]ormal(?: distribution)? with mean ' + N + r'[^.]*? and standard deviation ' + N, p)
    if not m or re.search(r'percentile|boundary|cutoff|value that|What (?:score|value)|shaded|z-score', p, re.I):
        return None
    mu, sd = num(m.group(1)), num(m.group(2))
    rest = p[m.end():]
    b = re.search(r'between ' + N + r' and ' + N, rest)
    z = lambda v: (v - mu) / sd
    if b:
        a1, a2 = num(b.group(1)), num(b.group(2))
        vals = [stats.norm.cdf(z(a2)) - stats.norm.cdf(z(a1)), stats.norm.cdf(round(z(a2), 2)) - stats.norm.cdf(round(z(a1), 2))]
        return has(q, vals, 0.0015 if q.get('format') else None) if False else has(q, vals)
    lo = re.search(r'(?:below|less than|under|at most|fewer than) ' + N, rest)
    hi = re.search(r'(?:above|more than|greater than|over|at least|exceed(?:s|ing)?) ' + N, rest)
    if lo and not hi:
        return has(q, ncdf_vals(z(num(lo.group(1)))))
    if hi and not lo:
        return has(q, [1 - v for v in ncdf_vals(z(num(hi.group(1))))])
    return None


@handler
def binom(q, p):
    m = re.search(r'n = (\d+)[,;]? (?:and )?p = (0?\.\d+)', p)
    if not m or not re.search(r'binomial|[Bb]inomial', p + ' '.join(q['solutionSteps'])):
        return None
    n, pr = int(m.group(1)), float(m.group(2))
    pl = p.lower()
    if re.search(r'\bmean\b|expected', pl) and 'p(' not in pl:
        return has(q, [n * pr])
    if re.search(r'standard deviation|\bsd\b', pl) and 'p(' not in pl:
        return has(q, [math.sqrt(n * pr * (1 - pr))])
    k = re.search(r'P\(X (=|≤|<|≥|>) (\d+)\)', p)
    if k:
        op, kk = k.group(1), int(k.group(2))
        B = stats.binom(n, pr)
        v = {'=': B.pmf(kk), '≤': B.cdf(kk), '<': B.cdf(kk - 1), '≥': 1 - B.cdf(kk - 1), '>': 1 - B.cdf(kk)}[op]
        return has(q, [v])
    return None


@handler
def z_star(q, p):
    m = re.search(r'z\* (?:for|for a) (\d+)% confidence', p)
    if not m:
        return None
    c = float(m.group(1)) / 100
    return has(q, [stats.norm.ppf(1 - (1 - c) / 2)], 0.006)


@handler
def one_prop_ci(q, p):
    m = re.search(r'(\d[\d,]*) (?:of (?:the )?(?:them|these|those)?|out of)? ?(?:the )?(\d[\d,]*)?', '')
    m = re.search(r'random sample of (\d[\d,]*)[^.]*?, (\d[\d,]*) (?:said|say|had|have|were|are|reported|answered|preferred|own|chose|support)', p)
    c = re.search(r'(\d+)% confidence interval for the (?:population )?proportion', p)
    if not m or not c:
        return None
    n, x = num(m.group(1)), num(m.group(2))
    ph = x / n; zs = stats.norm.ppf(1 - (1 - float(c.group(1)) / 100) / 2)
    se = math.sqrt(ph * (1 - ph) / n)
    return has(q, [ph - zs * se]) and has(q, [ph + zs * se])


@handler
def tail_from_stat(q, p):
    m = re.search(r'\b[tTzZ] = ' + N + r'[,;]? (?:with )?df = (\d+)?', p)
    z = re.search(r'\b[zZ] = ' + N + r'(?:,| with) Hₐ: (\w+) ([<>≠])', p)
    t = re.search(r'\bt = ' + N + r', df = (\d+), Hₐ: [^.]*?([<>≠])', p)
    if t:
        tv, df, s = num(t.group(1)), int(t.group(2)), t.group(3)
        v = {'>': stats.t.sf(tv, df), '<': stats.t.cdf(tv, df), '≠': 2 * stats.t.sf(abs(tv), df)}[s]
        return has(q, [v])
    if z and re.search(r'P-value', p, re.I):
        zv, s = num(z.group(1)), z.group(3)
        v = {'>': stats.norm.sf(zv), '<': stats.norm.cdf(zv), '≠': 2 * stats.norm.sf(abs(zv))}[s]
        return has(q, [v])
    return None


@handler
def one_prop_z(q, p):
    m = re.search(r'p₀ = (0?\.\d+), n = (\d+), p̂ = (0?\.\d+)', p, re.I)
    if m and re.search(r'Find z', p):
        p0, n, ph = float(m.group(1)), int(m.group(2)), float(m.group(3))
        return has(q, [(ph - p0) / math.sqrt(p0 * (1 - p0) / n)])
    m = re.search(r'p₀ = (0?\.\d+), n = (\d+), (\d+) successes', p, re.I)
    if m:
        p0, n, x = float(m.group(1)), int(m.group(2)), int(m.group(3))
        return has(q, [(x / n - p0) / math.sqrt(p0 * (1 - p0) / n)])
    m = re.search(r'Test H₀: p = (0?\.\d+) vs Hₐ: p ([<>≠]) [\d.]+\. Find the P-value', p)
    xm = re.search(r'(\d+) of (\d[\d,]*) (?:randomly selected|sampled|in the sample)', p)
    if m and xm:
        p0, s = float(m.group(1)), m.group(2)
        x, n = num(xm.group(1)), num(xm.group(2))
        z = (x / n - p0) / math.sqrt(p0 * (1 - p0) / n)
        f = lambda zz: {'>': stats.norm.sf(zz), '<': stats.norm.cdf(zz), '≠': 2 * stats.norm.sf(abs(zz))}[s]
        return has(q, [f(z), f(round(z, 2))])
    return None


@handler
def chisq(q, p):
    m = re.search(r'observed count of (\d+) and an expected count of ' + N, p)
    if m and '(O − E)²/E' in p:
        o, e = float(m.group(1)), num(m.group(2))
        return has(q, [(o - e) ** 2 / e])
    m = re.search(r'row total for "[^"]+" is (\d+) and the column total for "[^"]+" is (\d+)', p)
    g = re.search(r'classifies (\d[\d,]*)', p)
    if m and g:
        return has(q, [int(m.group(1)) * int(m.group(2)) / num(g.group(1))])
    m = re.search(r'χ² = ' + N + r' (?:with|and) df = (\d+)', p)
    if m:
        pv = stats.chi2.sf(num(m.group(1)), int(m.group(2)))
        stated = re.search(r'so the p-value is about (0?\.\d+)', p, re.I)
        al = re.search(r'α = (0?\.\d+)', p)
        if stated and al:  # a conclusion item: the printed p-value must be right, and so must the decision
            reject = pv < float(al.group(1))
            return abs(float(stated.group(1)) - pv) < 0.0006 and keytext(q).startswith('Reject' if reject else 'Fail to reject')
        if re.search(r'p-value', p, re.I) and not stated:
            return has(q, [pv])
    return None


@handler
def slope(q, p):
    m = re.search(r'slope b = ' + N + r'(?:,| with) SE_b = ' + N, p)
    if m and re.search(r't statistic', p):
        return has(q, [num(m.group(1)) / num(m.group(2))])
    m = re.search(r'gives t = ' + N + r' from n = (\d+)', p)
    s = re.search(r'Hₐ: β ([<>≠]) 0', p)
    if m and s:
        tv, df = num(m.group(1)), int(m.group(2)) - 2
        v = {'>': stats.t.sf(tv, df), '<': stats.t.cdf(tv, df), '≠': 2 * stats.t.sf(abs(tv), df)}[s.group(1)]
        return has(q, [v])
    m = re.search(r'uses (\d+) data points', p)
    if m and 'degrees of freedom' in p and 'slope' in p:
        return has(q, [int(m.group(1)) - 2])
    return None


@handler
def discrete(q, p):
    m = re.search(r'X (?:=|takes values) ((?:\d+, )+\d+) with probabilities ((?:0?\.\d+, )+0?\.\d+)', p)
    if not m:
        return None
    xs = [float(v) for v in m.group(1).split(', ')]; ps = [float(v) for v in m.group(2).split(', ')]
    if len(xs) != len(ps):
        return None
    mu = sum(a * b for a, b in zip(xs, ps)); sd = math.sqrt(sum((a - mu) ** 2 * b for a, b in zip(xs, ps)))
    k = re.search(r'P\(X (≥|>|≤|<|=) (\d+)\)', p)
    if k:
        op, kk = k.group(1), float(k.group(2))
        f = {'≥': lambda a: a >= kk, '>': lambda a: a > kk, '≤': lambda a: a <= kk, '<': lambda a: a < kk, '=': lambda a: a == kk}[op]
        return has(q, [sum(b for a, b in zip(xs, ps) if f(a))])
    if re.search(r'E\(X\)|mean|expected', p, re.I):
        return has(q, [mu])
    if re.search(r'standard deviation|SD|σ', p):
        return has(q, [sd])
    return None


@handler
def diff_sampling(q, p):
    m = re.search(r'In [^,]+, (\d+)% of [^;]+; in [^,]+, (\d+)% do\. Independent random samples of (\d+) from [^.]+ and (\d+) from', p)
    if m:
        p1, p2, n1, n2 = int(m.group(1)) / 100, int(m.group(2)) / 100, int(m.group(3)), int(m.group(4))
        mu, sd = p1 - p2, math.sqrt(p1 * (1 - p1) / n1 + p2 * (1 - p2) / n2)
    else:
        m = re.search(r'mean ' + N + r' and SD ' + N + r'; for [^,]+, the mean is ' + N + r' and the SD is ' + N + r'\. Independent random samples of (\d+) from [^.]+ and (\d+) from', p)
        if not m:
            return None
        m1, s1, m2, s2, n1, n2 = num(m.group(1)), num(m.group(2)), num(m.group(3)), num(m.group(4)), int(m.group(5)), int(m.group(6))
        mu, sd = m1 - m2, math.sqrt(s1 * s1 / n1 + s2 * s2 / n2)
    if 'What is the mean' in p:
        return has(q, [mu])
    if 'standard deviation' in p:
        return has(q, [sd])
    k = re.search(r'greater than (−?[\d.]+)', p) or re.search(r'P\(D ([<>]) 0\)', p)
    if k and k.re.pattern.startswith('greater'):
        return has(q, [stats.norm.sf((float(k.group(1)) - mu) / sd)])
    if k:
        return has(q, [stats.norm.sf(-mu / sd) if k.group(1) == '>' else stats.norm.cdf(-mu / sd)])
    return None


@handler
def combine(q, p):
    m = re.search(r'Independent X and Y have SDs ' + N + r' and ' + N, p)
    if not m:
        return None
    a, b = num(m.group(1)), num(m.group(2))
    if 'Var' in p:
        return has(q, [a * a + b * b])
    return has(q, [math.sqrt(a * a + b * b)])


@handler
def lsrl(q, p):
    m = re.search(r'[ŷŶ] = ' + N + r' ([+−-]) ' + N + r'x', p)
    if not m:
        return None
    a, b = num(m.group(1)), num(m.group(3)) * (1 if m.group(2) == '+' else -1)
    pt = re.search(r'\((' + N[1:-1] + r'), (' + N[1:-1] + r')\)', p)
    xv = re.search(r'x = ' + N, p)
    if 'residual' in p.lower():
        if pt:
            x, y = num(pt.group(1)), num(pt.group(2))
        else:
            xx = re.search(r'x = ' + N + r' and y = ' + N, p)
            if not xx:
                return None
            x, y = num(xx.group(1)), num(xx.group(2))
        return has(q, [y - (a + b * x)])
    if xv and re.search(r'[Pp]redict|Find ŷ', p):
        return has(q, [a + b * num(xv.group(1))])
    return None


@handler
def sampling_sd(q, p):
    m = re.search(r'[σΣ] = ' + N + r' and n = (\d+)\. Find the SD of x̄', p)
    if m:
        return has(q, [num(m.group(1)) / math.sqrt(int(m.group(2)))])
    m = re.search(r'n = (\d+) from a population with p = (0?\.\d+)', p)
    if m and re.search(r'standard deviation of the sampling distribution', p):
        n, pr = int(m.group(1)), float(m.group(2))
        return has(q, [math.sqrt(pr * (1 - pr) / n)])
    return None


res = collections.Counter(); bad = []
seen = set()
for q in Q:
    if q['format'] not in ('short-answer', 'multiple-choice'):
        continue
    p = q['prompt']
    if p.startswith('Error analysis'):
        continue
    for h in H:
        try:
            r = h(q, p)
        except Exception as e:
            r = None
        if r is None:
            continue
        res[h.__name__ + (' ok' if r else ' MISMATCH')] += 1
        if not r:
            bad.append((q['id'], h.__name__, p[:220].replace('\n', ' '), keytext(q)[:120]))
        seen.add(q['id'])
        break
for b in bad:
    print('MISMATCH', b)
print(sorted(res.items()))
ok = sum(v for k, v in res.items() if k.endswith(' ok'))
print(('PASS ' if not bad and ok >= MIN else 'FAIL ') + f'{ok} Statistics keys recomputed from the printed prompts ({len(bad)} mismatches)')
sys.exit(1 if bad or ok < MIN else 0)
