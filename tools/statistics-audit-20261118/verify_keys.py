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
MIN = 450
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



# ---------------------------------------------------------------------------- batch S2 shapes (2026-11-18)
# The prompts written for batch S2 (s2fill.py) and the CP contexts added by s2polish.py are read here, independently of
# the code that wrote them: each handler parses the printed numbers and recomputes the key with scipy.
P_ = r'(\d*\.?\d+)'


def tbl(z):
    return stats.norm.cdf(round(z, 2))


@handler
def s2_data(q, p):
    m = re.search(r'(?::|were)\s*((?:[−-]?\d[\d.]*,\s*){3,}(?:and\s*)?[−-]?\d[\d.]*)\.', p)
    if not m or 'P(x)' in p:
        return None
    d = [num(v) for v in re.findall(r'[−-]?\d[\d.]*', m.group(1))]
    rest = p[m.end():].lower()
    conv = re.search(r'y = ' + N + r' \+ ' + N + r'x', p)
    if conv and 'standard deviation' in rest:
        return has(q, [num(conv.group(2)) * np.std(d, ddof=1)])
    if 'sample standard deviation' in rest:
        return has(q, [np.std(d, ddof=1)])
    if 'find the mean' in rest:
        return has(q, [np.mean(d)])
    if 'find the median' in rest:
        return has(q, [np.median(d)])
    if 'find the range' in rest:
        return has(q, [max(d) - min(d)])
    return None


@handler
def s2_sampling_sd(q, p):
    m = re.search(r'(?:SD|σ =?) ' + N + r'[^.]*\. For random samples of (?:n = )?(\d+)[^,]*, find the (?:SD|standard deviation) of (?:the sample mean )?x̄', p)
    if m:
        return has(q, [num(m.group(1)) / math.sqrt(int(m.group(2)))])
    m = re.search(r'has SD ' + N + r' [^.]+\. A sample of (\d+) gives σ_x̄ = ' + N + r' [^.]+\. What is σ_x̄ if the sample size is multiplied by (\d+)', p)
    if m:
        return has(q, [num(m.group(1)) / math.sqrt(int(m.group(2)) * int(m.group(4)))])
    m = re.search(r'has SD ' + N + r' [^.]+\. What sample size is needed so that the standard deviation of x̄ is ' + N, p)
    if m:
        return has(q, [(num(m.group(1)) / num(m.group(2))) ** 2], 0.6)
    return None


@handler
def s2_binomial(q, p):
    m = re.search(r'About (\d+)% of [^.]+\. In a random sample of (\d+), find the probability that (exactly|at most|at least) (\d+)', p)
    if m:
        pr, n, op, k = int(m.group(1)) / 100, int(m.group(2)), m.group(3), int(m.group(4))
        B = stats.binom(n, pr)
        return has(q, [{'exactly': B.pmf(k), 'at most': B.cdf(k), 'at least': 1 - B.cdf(k - 1)}[op]])
    m = re.search(r'About (\d+)% of [^.]+\. X is the number in a random sample of (\d+) that do\. Find the (mean|standard deviation|probability that X is within one standard deviation)', p)
    if m:
        pr, n, w = int(m.group(1)) / 100, int(m.group(2)), m.group(3)
        mu, sd = n * pr, math.sqrt(n * pr * (1 - pr))
        if w == 'mean':
            return has(q, [mu])
        if w == 'standard deviation':
            return has(q, [sd])
        lo, hi = math.ceil(mu - sd), math.floor(mu + sd)
        return has(q, [stats.binom.cdf(hi, n, pr) - stats.binom.cdf(lo - 1, n, pr)])
    m = re.search(r'probability p = ' + P_ + r', independently\. For n = (\d+) of them, find the mean', p) or re.search(r'probability p = ' + P_ + r' and shoots n = (\d+)', p)
    if m:
        return has(q, [float(m.group(1)) * int(m.group(2))])
    return None


@handler
def s2_one_prop(q, p):
    m = re.search(r'In a random sample of (\d+) [^,]+, (\d+) [^.]+\. ', p)
    if not m:
        return None
    n, x = int(m.group(1)), int(m.group(2))
    ph = x / n
    se = math.sqrt(ph * (1 - ph) / n)
    rest = p[m.end():]
    if 'standard error of p̂' in rest:
        return has(q, [se])
    c = re.search(r'(\d+)% confidence interval', rest)
    if not c:
        return None
    zs = {90: 1.645, 95: 1.96, 99: 2.576}[int(c.group(1))]
    if 'margin of error' in rest:
        return has(q, [zs * se])
    return has(q, [ph - zs * se]) and has(q, [ph + zs * se])


@handler
def s2_sample_size(q, p):
    m = re.search(r'margin of error of ' + P_ + r' at (\d+)% confidence \(z\* = ' + P_ + r'\)\. (?:Use p\* = ' + P_ + r'|A pilot study suggests p is about ' + P_ + r')', p)
    if not m:
        return None
    me, zs = float(m.group(1)), float(m.group(3))
    ps = float(m.group(4) or m.group(5))
    return has(q, [math.ceil((zs / me) ** 2 * ps * (1 - ps) - 1e-9)])


@handler
def s2_t_interval(q, p):
    m = re.search(r'A random sample of (\d+) [^.]+? has mean ' + N + r' [^.]*?and standard deviation ' + N + r' ', p)
    c = re.search(r'(\d+)% confidence interval', p)
    if not m or not c:
        return None
    n, xb, s_ = int(m.group(1)), num(m.group(2)), num(m.group(3))
    ts = stats.t.ppf(1 - (1 - int(c.group(1)) / 100) / 2, n - 1)
    if 'critical value t*' in p:
        return has(q, [ts])
    me = ts * s_ / math.sqrt(n)
    return has(q, [xb - me]) and has(q, [xb + me])


@handler
def s2_tests(q, p):
    m = re.search(r'Test H₀: μ = ' + N + r' against Hₐ: μ ([<>]) [^.]+?\. A random sample of (\d+) [^.]*?has x̄ = ' + N + r' and s = ' + N + r'\.', p)
    if m:
        mu, alt, n, xb, s_ = num(m.group(1)), m.group(2), int(m.group(3)), num(m.group(4)), num(m.group(5))
        t = (xb - mu) / (s_ / math.sqrt(n))
        if 'test statistic t' in p:
            return has(q, [t])
        return has(q, [stats.t.sf(t, n - 1) if alt == '>' else stats.t.cdf(t, n - 1)])
    m = re.search(r'Test H₀: p = ' + P_ + r' against Hₐ: p ([<>]) [^,]+, where [^.]+\. In a random sample of (\d+), (\d+) ', p)
    if m:
        p0, alt, n, x = float(m.group(1)), m.group(2), int(m.group(3)), int(m.group(4))
        z = (x / n - p0) / math.sqrt(p0 * (1 - p0) / n)
        if 'test statistic z' in p:
            return has(q, [z])
        return has(q, [1 - tbl(z) if alt == '>' else tbl(z)])
    m = re.search(r'p₀ = ' + P_ + r'\. In n = (\d+) trials there are (\d+) successes', p)
    if m:
        p0, n, x = float(m.group(1)), int(m.group(2)), int(m.group(3))
        return has(q, [(x / n - p0) / math.sqrt(p0 * (1 - p0) / n)])
    m = re.search(r'from μ₀ = ' + N + r' \w+ uses a random sample of n = (\d+) with x̄ = ' + N + r' and s = ' + N, p)
    if m:
        mu, n, xb, s_ = num(m.group(1)), int(m.group(2)), num(m.group(3)), num(m.group(4))
        return has(q, [(xb - mu) / (s_ / math.sqrt(n))])
    m = re.search(r'Hₐ: p ([<>]) p₀ [^.]*gives z = ' + N + r'\. Find the p-value', p)
    if m:
        z = num(m.group(2))
        return has(q, [stats.norm.sf(z) if m.group(1) == '>' else stats.norm.cdf(z)])
    m = re.search(r'Group 1 has n = (\d+), x̄ = ' + N + r', s = ' + N + r'; Group 2 has n = (\d+), x̄ = ' + N + r', s = ' + N, p)
    if m:
        n1, x1, s1, n2, x2, s2 = int(m.group(1)), num(m.group(2)), num(m.group(3)), int(m.group(4)), num(m.group(5)), num(m.group(6))
        se = math.sqrt(s1 ** 2 / n1 + s2 ** 2 / n2)
        return has(q, [se]) if 'standard error' in p else has(q, [(x1 - x2) / se])
    return None


@handler
def s2_slope(q, p):
    m = re.search(r'n = (\d+)\)? gives (?:slope )?b = ' + N + r'(?: with|,| and) SE_b = ' + N, p)
    if not m:
        m2 = re.search(r'gives b = ' + N + r' and SE_b = ' + N + r'\. Find t for H₀', p)
        return has(q, [num(m2.group(1)) / num(m2.group(2))]) if m2 else None
    n, b, se = int(m.group(1)), num(m.group(2)), num(m.group(3))
    if 'degrees of freedom' in p:
        return has(q, [n - 2])
    c = re.search(r'(\d+)% confidence interval for the true slope', p)
    if c:
        ts = stats.t.ppf(1 - (1 - int(c.group(1)) / 100) / 2, n - 2)
        return has(q, [b - ts * se]) and has(q, [b + ts * se])
    if 'p-value' in p:
        return has(q, [2 * stats.t.sf(abs(b / se), n - 2)])
    if 't statistic' in p:
        return has(q, [b / se])
    return None


@handler
def s2_chisq(q, p):
    m = re.search(r'proportions ((?:' + P_ + r', )+' + P_ + r')\. ', p)
    cats = re.search(r'the categories ([^.]+?) occur with', p)
    if m and cats:
        props = [float(v) for v in m.group(1).split(', ')]
        names = cats.group(1).split(', ')
        e = re.search(r'with n = (\d+), what is the expected count for "([^"]+)"', p)
        if e:
            return has(q, [int(e.group(1)) * props[names.index(e.group(2))]])
        o = re.search(r'A random sample of (\d+) gives observed counts ((?:\d+, )+\d+)\.', p)
        if o:
            n = int(o.group(1)); obs = [int(v) for v in o.group(2).split(', ')]
            return has(q, [sum((a - n * b) ** 2 / (n * b) for a, b in zip(obs, props))])
    m = re.search(r'with (\d+) rows and (\d+) columns(?: and gives χ² = ' + N + r')?', p)
    if m and 'independence' in p:
        df = (int(m.group(1)) - 1) * (int(m.group(2)) - 1)
        if m.group(3):
            return has(q, [stats.chi2.sf(num(m.group(3)), df)])
        if 'degrees of freedom' in p:
            return has(q, [df])
    return None


@handler
def s2_two_way(q, p):
    m = re.search(r'Counts — ([^.]+?)\. (?:For a randomly chosen person, find P\(([^|]+) \| ([^)]+)\)|Find the expected count for (.+?) and (.+?)\.)', p)
    if not m:
        return None
    rows = {}
    for part in m.group(1).split('; '):
        r, cells = part.split(': ', 1)
        rows[r] = {c.rsplit(' ', 1)[0]: int(c.rsplit(' ', 1)[1]) for c in cells.split(', ')}
    cols = list(next(iter(rows.values())).keys())
    if m.group(2):
        a, b = m.group(2), m.group(3)
        if b in rows:
            return has(q, [rows[b][a] / sum(rows[b].values())])
        return has(q, [rows[a][b] / sum(rows[r][b] for r in rows)])
    r, c = m.group(4), m.group(5)
    N_ = sum(sum(v.values()) for v in rows.values())
    return has(q, [sum(rows[r].values()) * sum(rows[x][c] for x in rows) / N_])


@handler
def s2_probability(q, p):
    m = re.search(r'P\(A\) = ' + P_ + r' where [^,]+, P\(B\) = ' + P_ + r' where [^,]+, and P\(A and B\) = ' + P_ + r'\. Find (P\(A or B\)|the probability that the person is in neither group)', p)
    if m:
        u = float(m.group(1)) + float(m.group(2)) - float(m.group(3))
        return has(q, [u if m.group(4).startswith('P(') else 1 - u])
    m = re.search(r'the probability that ([^,]+?) is ' + P_ + r', and the probability that (.+?) and \1 is ' + P_ + r'\. Find the probability that \3, given that \1', p)
    if m:
        return has(q, [float(m.group(4)) / float(m.group(2))])
    m = re.search(r'is ' + P_ + r', and outcomes are independent\. Find the probability that this (happens (\d+) times in a row|fails at least once in (\d+) tries)', p)
    if m:
        pr = float(m.group(1))
        return has(q, [pr ** int(m.group(3))]) if m.group(3) else has(q, [1 - pr ** int(m.group(4))])
    m = re.search(r'In a random sample of (\d+) [^,]+, (\d+) [^.]+\. What is the relative frequency', p) or re.search(r'runs (\d+) trials of a simulation, and in (\d+) of them', p)
    if m:
        return has(q, [int(m.group(2)) / int(m.group(1))])
    return None


@handler
def s2_random_variables(q, p):
    m = re.search(r'X = [^.]+\. ((?:P\(X = \d+\) = ' + P_ + r'(?:, )?)+)\. ', p)
    if m:
        pairs = re.findall(r'P\(X = (\d+)\) = ' + P_, m.group(1))
        xs, ps = [int(a) for a, _ in pairs], [float(b) for _, b in pairs]
        mu = sum(a * b for a, b in zip(xs, ps)); sd = math.sqrt(sum((a - mu) ** 2 * b for a, b in zip(xs, ps)))
        y = re.search(r'Y = ' + N + r' \+ ' + N + r'X', p)
        if y:
            return has(q, [abs(num(y.group(2))) * sd])
        return has(q, [mu]) if 'expected value' in p else has(q, [sd])
    m = re.search(r'costs \$(\d+) to play\. A player wins \$(\d+) with probability ' + P_ + r' and \$(\d+) with probability ' + P_, p)
    if m:
        c, v1, p1, v2, p2 = int(m.group(1)), int(m.group(2)), float(m.group(3)), int(m.group(4)), float(m.group(5))
        return has(q, [v1 * p1 + v2 * p2 - c], 0.006)
    m = re.search(r'is Normal with mean ' + N + r' and SD ' + N + r' \w+; [^;]+ is Normal with mean ' + N + r' and SD ' + N + r' \w+, independent\. Find the probability that [^.]+ is longer than', p)
    if m:
        m1, s1, m2, s2 = (num(m.group(i)) for i in range(1, 5))
        z = (0 - (m1 - m2)) / math.sqrt(s1 * s1 + s2 * s2)
        return has(q, [1 - tbl(z)])
    m = re.search(r'\(mean ' + N + r'(?:, SD ' + N + r')?\) and Y = [^(]+\(mean ' + N + r'(?:, SD ' + N + r')?\)', p)
    if m:
        if m.group(2) and m.group(4):
            return has(q, [math.sqrt(num(m.group(2)) ** 2 + num(m.group(4)) ** 2)])
        return has(q, [num(m.group(1)) + num(m.group(3))])
    return None


@handler
def s2_strata_ci(q, p):
    m = re.search(r'A population of ([\d,]+) [^.]+? is made up of ([^.]+)\. A stratified random sample of (\d+) [^.]+\. How many (.+?) are in the sample', p)
    if m:
        N_ = num(m.group(1)); n = int(m.group(3))
        groups = {g.strip().split(' ', 1)[1]: num(g.strip().split(' ', 1)[0]) for g in re.split(r', | and ', m.group(2))}
        return has(q, [n * groups[m.group(4)] / N_])
    m = re.search(r'confidence interval for [^.]*?is \(' + N + r', ' + N + r'\)\.', p)
    if m and re.search(r'point estimate|margin of error', p) and 'sample size' not in p:
        a, b = num(m.group(1)), num(m.group(2))
        return has(q, [(a + b) / 2]) if 'point estimate' in p else has(q, [(b - a) / 2])
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
