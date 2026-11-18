"""Election and weighted-voting engines for the Discrete Math audit (independent of tools/discrete-math)."""
import itertools, math, collections
from fractions import Fraction as Fr


def fs(x):
    x = Fr(x)
    return str(x.numerator) if x.denominator == 1 else f'{x.numerator}/{x.denominator}'


# ---------- preference schedules: rows = [(count, ['A', 'B', 'C'])] ----------
def first_place(rows):
    c = collections.Counter({x: 0 for x in rows[0][1]})
    for n, r in rows:
        c[r[0]] += n
    return c


def borda(rows):
    c = collections.Counter({x: 0 for x in rows[0][1]})
    for n, r in rows:
        for i, x in enumerate(r):
            c[x] += n * (len(r) - i)
    return c


def h2h(rows, a, b):
    return sum(n for n, r in rows if r.index(a) < r.index(b))


def pairwise(rows):
    pts = collections.Counter({x: Fr(0) for x in rows[0][1]})
    for a, b in itertools.combinations(sorted(rows[0][1]), 2):
        x, y = h2h(rows, a, b), h2h(rows, b, a)
        if x > y: pts[a] += 1
        elif y > x: pts[b] += 1
        else: pts[a] += Fr(1, 2); pts[b] += Fr(1, 2)
    return pts


def condorcet(rows):
    C = rows[0][1]
    for a in C:
        if all(h2h(rows, a, b) > h2h(rows, b, a) for b in C if b != a):
            return a
    return None


def irv(rows):
    """Return (winner or None, rounds) where rounds = list of first-place tallies."""
    C = list(rows[0][1]); tot = sum(n for n, _ in rows); rounds = []
    while True:
        c = collections.Counter({x: 0 for x in C})
        for n, r in rows:
            c[[x for x in r if x in C][0]] += n
        rounds.append(dict(c))
        for x, v in c.items():
            if 2 * v > tot:
                return x, rounds
        lo = min(c.values()); losers = [x for x in C if c[x] == lo]
        if len(losers) > 1 or len(C) <= 2:
            return None, rounds
        C = [x for x in C if x not in losers]


def unique_max(cnt):
    m = max(cnt.values()); w = [k for k, v in cnt.items() if v == m]
    return w[0] if len(w) == 1 else None


def fmt_schedule(rows):
    return '\n'.join(f'{n} voters: ' + ' > '.join(r) for n, r in rows)


def random_schedule(rng, ncand, nrows, lo=2, hi=15):
    cands = 'ABCDE'[:ncand]
    perms = [list(p) for p in itertools.permutations(cands)]
    rng.shuffle(perms)
    return [(rng.randint(lo, hi), perms[i]) for i in range(nrows)]


# ---------- weighted voting ----------
def coalitions(q, w):
    out = []
    for k in range(1, len(w) + 1):
        for S in itertools.combinations(range(len(w)), k):
            if sum(w[i] for i in S) >= q:
                out.append(S)
    return out


def critical_counts(q, w):
    c = [0] * len(w)
    for S in coalitions(q, w):
        s = sum(w[i] for i in S)
        for i in S:
            if s - w[i] < q:
                c[i] += 1
    return c


def pivotal_counts(q, w):
    c = [0] * len(w)
    for p in itertools.permutations(range(len(w))):
        s = 0
        for i in p:
            s += w[i]
            if s >= q:
                c[i] += 1
                break
    return c


def name(S):
    return '{' + ', '.join(f'P{i + 1}' for i in S) + '}'


def random_system(rng, n):
    while True:
        w = sorted(rng.sample(range(1, 13), n), reverse=True)
        T = sum(w); q = rng.randint(T // 2 + 1, T - 1)
        c = critical_counts(q, w)
        if sum(c) and 0 < c[0] and len(coalitions(q, w)) >= 2:
            return q, w
