"""Independent recomputation of Precalculus bank answers (audit 2026-11-18).

Parses the printed problem, recomputes the answer with its own formulas, and compares it with the key
(and, for find-the-mistake items, checks that the student's answer is wrong). No code is shared with the
authoring scripts; mathx.ev evaluates exact display forms such as (√3)/2 or 7π/2.

Usage: python3 tools/precalculus-audit-20261118/checker/pc_verify.py [--min N] [items.json]
With no items file it reads question-banks/precalculus/*.json. Exits 1 if any key, option or student answer
disagrees, or if fewer than N items were recomputed (CI runs it with --min 2000, audit #11).
"""
import glob, json, os, re, math, cmath, collections, itertools, sys
from fractions import Fraction as Fr
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mathx import ev  # noqa: E402

_args = sys.argv[1:]
MIN = 0
if '--min' in _args:
    MIN = int(_args[_args.index('--min') + 1])
    del _args[_args.index('--min'):_args.index('--min') + 2]
if _args:
    I = json.load(open(_args[0]))
else:
    _root = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..'))
    I = [q for f in sorted(glob.glob(os.path.join(_root, 'question-banks', 'precalculus', '*.json'))) for q in json.load(open(f, encoding='utf-8'))['questions']]
res = collections.Counter()
flags = []
D = math.pi / 180


def N(s):
    """Number from a key: strips ≈, x =, units, $, %, degree signs, commas."""
    s = str(s).strip().rstrip('.')
    s = s.replace('−', '-').replace('$', '').replace(',', '')
    s = re.sub(r'^[a-zA-Zθ]\w*\s*[≈=]\s*', '', s)
    s = s.replace('≈', '').strip()
    s = re.sub(r'\s*(°|%|in²|cm²|m²|ft²|units²|square units|cm|km/h|mph|ft|m|km|N|hours?|units?|L|years?|seconds?|s|in|mi)\.?$', '', s)
    return ev(s.strip(), {})


def close(a, b, tol=1e-6, rel=True):
    return abs(a - b) <= tol * max(1, abs(a) if rel else 1, abs(b) if rel else 1)


def rclose(a, key):
    """a computed exactly; key possibly rounded: match to the key's own decimal places."""
    k = str(key)
    m = re.search(r'-?\d+\.(\d+)', k.replace(',', ''))
    dp = len(m.group(1)) if m else None
    v = N(key)
    if dp is None:
        return close(a, v, 1e-6)
    return abs(a - v) <= 0.5 * 10 ** -dp + 1e-9


def tup(s):
    s = str(s).replace('−', '-')
    m = re.search(r'[(⟨]([^()⟨⟩]*(?:\([^()]*\)[^()⟨⟩]*)*)[)⟩]\s*$', s.strip().rstrip('.'))
    if not m:
        return None
    parts = split_top(m.group(1))
    return [ev(p.strip(), {}) for p in parts]


def split_top(s, sep=','):
    out, depth, cur = [], 0, ''
    for ch in s:
        if ch in '([⟨{':
            depth += 1
        elif ch in ')]⟩}':
            depth -= 1
        if ch == sep and depth == 0:
            out.append(cur); cur = ''
        else:
            cur += ch
    out.append(cur)
    return out


def mat(s):
    s = str(s).replace('−', '-')
    m = re.search(r'\[([^\[\]]+)\]', s)
    rows = [split_top(r) for r in m.group(1).split(';')]
    return [[ev(x.strip(), {}) for x in r] for r in rows]


def roots_list(s):
    s = str(s).replace('−', '-')
    s = re.sub(r'\bx\s*=\s*', '', s)
    parts = re.split(r'\s+or\s+|,\s*|\s+and\s+', s)
    out = []
    for p in parts:
        p = p.strip().rstrip('.')
        if p:
            out.append(complex(ev(p.replace('i', '*1j') if re.search(r'\di|\bi\b', p) else p, {})) if 'i' in p and not re.search(r'[a-hj-z]', p) else ev(p, {}))
    return out


def flag(q, why, extra=''):
    flags.append((q['id'], why, q['prompt'][:150].replace('\n', ' '), str(q['answer'])[:80], str(extra)[:80]))


def inner(q):
    p = q['prompt']
    if 'answered this problem incorrectly' in p:
        lines = p.split('\n')
        body = [l for l in lines[1:] if not re.search(r"'s answer:|Identify the mistake", l)]
        stu = next((l.split("'s answer:")[1].strip() for l in lines if "'s answer:" in l), None)
        return '\n'.join(body), stu
    return p, None


def key_of(q):
    return q['answer'] if not isinstance(q['answer'], list) else q['answer']


# ------------------------------------------------------------------ families: each returns (match, check(fn) -> bool for a candidate)
FAM = []


def fam(rx):
    def deco(fn):
        FAM.append((re.compile(rx, re.S), fn))
        return fn
    return deco


def E(s):
    return ev(s.replace('−', '-'), {})


@fam(r'Find the center of the circle \(x ([+-]) (\d+)\)² \+ \(y ([+-]) (\d+)\)² = (\d+)')
def _(m, p):
    h = -int(m[2]) if m[1] == '+' else int(m[2]); k = -int(m[4]) if m[3] == '+' else int(m[4])
    return lambda a: (t := tup(a)) and close(t[0], h) and close(t[1], k)


@fam(r'Find the radius of the circle x² \+ y² ([+-]) (\d*)x ([+-]) (\d*)y ([+-]) (\d+) = 0')
def _(m, p):
    D_ = int(m[2] or 1) * (1 if m[1] == '+' else -1); E_ = int(m[4] or 1) * (1 if m[3] == '+' else -1); F_ = int(m[6]) * (1 if m[5] == '+' else -1)
    r = math.sqrt(D_ * D_ / 4 + E_ * E_ / 4 - F_)
    return lambda a: close(N(a), r)


@fam(r'length of the major axis of the ellipse \(?x[^/]*\)?²/(\d+) \+ \(?y[^/]*\)?²/(\d+) = 1')
def _(m, p):
    v = 2 * math.sqrt(max(int(m[1]), int(m[2])))
    return lambda a: close(N(a), v)


@fam(r'major axis length (\d+) and minor axis length (\d+)\. Find its eccentricity')
def _(m, p):
    a, b = int(m[1]) / 2, int(m[2]) / 2
    return lambda x: close(N(x), math.sqrt(a * a - b * b) / a)


@fam(r'Find the foci of the hyperbola \(x ([+-]) (\d+)\)²/(\d+) - \(y ([+-]) (\d+)\)²/(\d+) = 1')
def _(m, p):
    h = -int(m[2]) if m[1] == '+' else int(m[2]); k = -int(m[5]) if m[4] == '+' else int(m[5]); c = math.sqrt(int(m[3]) + int(m[6]))
    want = sorted([(h + c, k), (h - c, k)])
    def chk(a):
        pts = re.findall(r'\(([^()]+)\)', str(a))
        got = sorted(tuple(E(x) for x in pt.split(',')) for pt in pts)
        return len(got) == 2 and all(close(g[0], w[0]) and close(g[1], w[1]) for g, w in zip(got, want))
    return chk


@fam(r'line through \((-?\d+), (-?\d+)\) and \((-?\d+), (-?\d+)\)\.')
def _(m, p):
    x1, y1, x2, y2 = map(int, m.groups())
    if x1 == x2: return None
    s = Fr(y2 - y1, x2 - x1); b = y1 - s * x1
    return lambda a: lineq(a, s, b)


def lineq(a, s, b):
    t = str(a).replace('−', '-').replace(' ', '')
    mm = re.fullmatch(r'y=(.*)', t)
    if not mm: return False
    f = mm.group(1)
    try:
        return all(close(ev(f, {'x': x}), float(s * x + b)) for x in (-2.5, 0.0, 1.7))
    except Exception:
        return False


@fam(r'Write (-?\d*)x ([+-]) (\d*)y = (-?\d+) in slope-intercept form')
def _(m, p):
    A = int(m[1]) if m[1] not in ('', '-') else (1 if m[1] == '' else -1); B = int(m[3] or 1) * (1 if m[2] == '+' else -1); C = int(m[4])
    return lambda a: lineq(a, Fr(-A, B), Fr(C, B))


@fam(r'through \((-?\d+), (-?\d+)\) that is (parallel|perpendicular) to y = (.+?)\.$')
def _(m, p):
    x1, y1 = int(m[1]), int(m[2]); f = m[4]
    sl = ev(f, {'x': 1}) - ev(f, {'x': 0})
    s = Fr(sl).limit_denominator(100)
    if m[3] == 'perpendicular': s = -1 / s
    return lambda a: lineq(a, s, y1 - s * x1)


@fam(r'Solve the system: (-?\d*)x ([+-]) (\d*)y = (-?\d+) and (-?\d*)x ([+-]) (\d*)y = (-?\d+)\.')
def _(m, p):
    c = lambda s: 1 if s == '' else -1 if s == '-' else int(s)
    a1, b1, r1 = c(m[1]), c(m[3]) * (1 if m[2] == '+' else -1), int(m[4]); a2, b2, r2 = c(m[5]), c(m[7]) * (1 if m[6] == '+' else -1), int(m[8])
    det = a1 * b2 - a2 * b1
    if not det: return None
    x, y = (r1 * b2 - r2 * b1) / det, (a1 * r2 - a2 * r1) / det
    return lambda a: (t := tup(a)) and close(t[0], x) and close(t[1], y)


def lin3(eq):
    eq = eq.replace('−', '-').replace(' ', '')
    l, r = eq.split('=')
    co = {'x': 0, 'y': 0, 'z': 0}
    for sgn, c, v in re.findall(r'([+-]?)(\d*)([xyz])', l):
        co[v] += (-1 if sgn == '-' else 1) * (int(c) if c else 1)
    return [co['x'], co['y'], co['z']], int(r)


@fam(r'Solve the system: ([^;]+); ([^;]+); ([^.]+?)\. Give the answer as \(x, y, z\)')
def _(m, p):
    rows = [lin3(m[i]) for i in (1, 2, 3)]
    import numpy as np
    A = np.array([r[0] for r in rows], float); b = np.array([r[1] for r in rows], float)
    sol = np.linalg.solve(A, b)
    return lambda a: (t := tup(a)) and all(close(t[i], sol[i]) for i in range(3))


def lp(cons, obj=None):
    lines = []
    for c in cons:
        c = c.replace(' ', '')
        mm = re.fullmatch(r'(\d*)x\+(\d*)y≤(\d+)', c)
        if mm: lines.append((int(mm[1] or 1), int(mm[2] or 1), int(mm[3])))
    pts = [(0, 0)]
    for a, b, c in lines:
        pts += [(c / a, 0), (0, c / b)]
    for (a1, b1, c1), (a2, b2, c2) in itertools.combinations(lines, 2):
        d = a1 * b2 - a2 * b1
        if d: pts.append(((c1 * b2 - c2 * b1) / d, (a1 * c2 - a2 * c1) / d))
    feas = [p for p in pts if p[0] >= -1e-9 and p[1] >= -1e-9 and all(a * p[0] + b * p[1] <= c + 1e-9 for a, b, c in lines)]
    return lines, feas


@fam(r'Find the (maximum|minimum) value of P = (\d*)x ([+-]) (\d*)y subject to x ≥ 0, y ≥ 0, (.+?)\.$')
def _(m, p):
    cx, cy = int(m[2] or 1), int(m[4] or 1) * (1 if m[3] == '+' else -1)
    _, feas = lp([c.strip() for c in m[5].split(',')])
    vals = [cx * a + cy * b for a, b in feas]
    v = max(vals) if m[1] == 'maximum' else min(vals)
    return lambda a: close(N(a), v)


@fam(r'The region x ≥ 0, y ≥ 0, (\d*)x \+ (\d*)y ≤ (\d+), (\d*)x \+ (\d*)y ≤ (\d+) has a corner where the two slanted boundary lines meet')
def _(m, p):
    a1, b1, c1, a2, b2, c2 = [int(x or 1) for x in m.groups()]
    d = a1 * b2 - a2 * b1
    x, y = (c1 * b2 - c2 * b1) / d, (a1 * c2 - a2 * c1) / d
    return lambda a: (t := tup(a)) and close(t[0], x) and close(t[1], y)


@fam(r'Let f\(x\) = (.+?) and g\(x\) = (.+?)\. Find \((f|g) ∘ (f|g)\)\((-?\d+)\)\.')
def _(m, p):
    F = {'f': m[1], 'g': m[2]}
    v = ev(F[m[3]], {'x': ev(F[m[4]], {'x': int(m[5])})})
    return lambda a: close(N(a), v)


@fam(r'Let f\(x\) = (.+?) and x₀ = (-?\d+)\. Find the third iterate')
def _(m, p):
    x = int(m[2])
    for _ in range(3): x = ev(m[1], {'x': x})
    return lambda a: close(N(a), x)


@fam(r'^f\(x\) = (.+?) if x (<|≤) (-?\d+); f\(x\) = (.+?) if x (≥|>) (-?\d+)\. Find f\((-?\d+)\)\.')
def _(m, p):
    x, c = int(m[7]), int(m[3])
    left = x < c if m[2] == '<' else x <= c
    v = ev(m[1] if left else m[4], {'x': x})
    return lambda a: close(N(a), v)


@fam(r'Evaluate the greatest integer function: ⌊(-?[\d.]+)⌋')
def _(m, p):
    v = math.floor(float(m[1]))
    return lambda a: close(N(a), v)


@fam(r'For f\(x\) = (.+?), find f⁻¹\((-?\d+)\)\.')
def _(m, p):
    t = int(m[2]); f = lambda x: ev(m[1], {'x': x})
    lo, hi = -1e4, 1e4
    flo = f(lo) - t
    for _ in range(200):
        mid = (lo + hi) / 2
        if (f(mid) - t) * flo > 0: lo = mid; flo = f(lo) - t
        else: hi = mid
    return lambda a: close(N(a), lo, 1e-5)


@fam(r'y varies (directly|inversely) with x, and y = (\S+) when x = (\S+)\. Find y when x = (\S+?)\.$')
def _(m, p):
    y1, x1, x2 = E(m[2]), E(m[3]), E(m[4])
    v = y1 / x1 * x2 if m[1] == 'directly' else y1 * x1 / x2
    return lambda a: close(N(a), v)


@fam(r'Solve (x² .+?) = 0\. Give exact solutions\.')
def _(m, p):
    e = m[1]
    a = ev(e, {'x': 0}); b1 = ev(e, {'x': 1}); c1 = ev(e, {'x': -1})
    c0 = a; B = (b1 - c1) / 2; A = (b1 + c1) / 2 - c0
    disc = B * B - 4 * A * c0
    r = sorted([(-B + cmath.sqrt(disc)) / (2 * A), (-B - cmath.sqrt(disc)) / (2 * A)], key=lambda z: (z.real, z.imag))
    def chk(ans):
        s = str(ans).replace('−', '-')
        parts = [x.strip().rstrip('.') for x in re.split(r'\s+or\s+|,', re.sub(r'\bx\s*=\s*', '', s)) if x.strip()]
        got = []
        for x in parts:
            if 'i' in x:
                x2 = re.sub(r'(\d)i', r'\1*1j', x).replace('√', 'SQ')
                x2 = re.sub(r'(?<![\w*])i\b', '1j', x2)
                x2 = re.sub(r'SQ(\d+)', r'math.sqrt(\1)', x2)
                got.append(complex(eval(x2, {'math': math})))
            else:
                got.append(complex(ev(x, {})))
        got = sorted(got, key=lambda z: (round(z.real, 6), round(z.imag, 6)))
        if len(set((round(z.real, 6), round(z.imag, 6)) for z in r)) == 1: return len(got) >= 1 and abs(got[0] - r[0]) < 1e-6
        return len(got) == 2 and all(abs(g - w) < 1e-6 for g, w in zip(got, r))
    return chk


@fam(r'Find the horizontal asymptote of f\(x\) = \((-?\d*)x ([+-]) (\d+)\)/\((-?\d*)x ([+-]) (\d+)\)\.')
def _(m, p):
    a = int(m[1]) if m[1] not in ('', '-') else (1 if m[1] == '' else -1); c = int(m[4]) if m[4] not in ('', '-') else (1 if m[4] == '' else -1)
    return lambda x: close(N(x), a / c)


@fam(r'remainder when P\(x\) = (.+?) is divided by x ([+-]) (\d+)\.')
def _(m, p):
    r = int(m[3]) * (1 if m[2] == '-' else -1)
    v = ev(m[1], {'x': r})
    return lambda a: close(N(a), v)


@fam(r'x = (-?\d+) is a zero of P\(x\) = (.+?)\. Find the other two zeros\.')
def _(m, p):
    f = lambda x: ev(m[2], {'x': x})
    def chk(a):
        rs = [ev(x, {}) for x in re.split(r'\s+or\s+|,', re.sub(r'x\s*=\s*', '', str(a).replace('−', '-'))) if x.strip()]
        return len(rs) == 2 and all(abs(f(x)) < 1e-6 for x in rs) and all(abs(x - int(m[1])) > 1e-9 for x in rs)
    return chk


@fam(r'Evaluate f\((-?\d+)\) for f\(x\) = ([\d.]+)\(([\d.]+)\)ˣ\.')
def _(m, p):
    v = float(m[2]) * float(m[3]) ** int(m[1])
    return lambda a: close(N(a), v)


@fam(r'\$([\d,]+) is invested at ([\d.]+)% interest compounded continuously\. Find the balance after (\d+) years')
def _(m, p):
    v = float(m[1].replace(',', '')) * math.exp(float(m[2]) / 100 * int(m[3]))
    return lambda a: abs(N(a) - v) <= 0.005 + 1e-9


@fam(r'^Evaluate log(?:_)?([₀₁₂₃₄₅₆₇₈₉]+)\(([\d/]+)\)\.')
def _(m, p):
    b = int(m[1].translate(str.maketrans('₀₁₂₃₄₅₆₇₈₉', '0123456789')))
    v = math.log(E(m[2])) / math.log(b)
    return lambda a: close(N(a), v)


@fam(r'^Solve (\d+)\^\((.+?)\) = (\d+)\.')
def _(m, p):
    b, t = int(m[1]), int(m[3])
    def chk(a):
        x = N(a)
        return close(b ** ev(m[2], {'x': x}), t)
    return chk


@fam(r'^Solve e\^x = ([\d.]+)\. Round to the nearest thousandth')
def _(m, p):
    return lambda a: rclose(math.log(float(m[1])), a)


@fam(r'In triangle ABC, A = (\d+)° and B = (\d+)°\. Find angle C\.')
def _(m, p):
    return lambda a: close(N(a), 180 - int(m[1]) - int(m[2]))


@fam(r'area of a triangle with sides ([\d.]+) \w+ and ([\d.]+) \w+ and included angle (\d+)°\. Round to the nearest tenth')
def _(m, p):
    return lambda a: rclose(0.5 * float(m[1]) * float(m[2]) * math.sin(int(m[3]) * D), a)


@fam(r'How many triangles have A = (\d+)°, a = ([\d.]+), and b = ([\d.]+)\?')
def _(m, p):
    A, a, b = int(m[1]) * D, float(m[2]), float(m[3])
    h = b * math.sin(A)
    if A >= math.pi / 2: n = 1 if a > b else 0
    elif a < h - 1e-12: n = 0
    elif abs(a - h) < 1e-12 or a >= b: n = 1
    else: n = 2
    return lambda x: close(N(x), n)


@fam(r'A triangle has sides a = ([\d.]+), b = ([\d.]+), and c = ([\d.]+)\. Find angle ([ABC]) to the nearest tenth')
def _(m, p):
    a, b, c = map(float, m.groups()[:3])
    s = {'A': (a, b, c), 'B': (b, a, c), 'C': (c, a, b)}[m[4]]
    v = math.degrees(math.acos((s[1] ** 2 + s[2] ** 2 - s[0] ** 2) / (2 * s[1] * s[2])))
    return lambda x: rclose(v, x)


@fam(r'One walks ([\d.]+) km and the other walks ([\d.]+) km; the angle between their paths is (\d+)°')
def _(m, p):
    a, b, C = float(m[1]), float(m[2]), int(m[3]) * D
    v = math.sqrt(a * a + b * b - 2 * a * b * math.cos(C))
    return lambda x: rclose(v, x)


@fam(r"Heron's formula to find the area of a triangle with sides (\d+), (\d+), and (\d+)")
def _(m, p):
    a, b, c = map(int, m.groups()); s = (a + b + c) / 2
    v = math.sqrt(s * (s - a) * (s - b) * (s - c))
    return lambda x: rclose(v, x)


@fam(r'In triangle ABC, b = ([\d.]+) and A = (\d+)°\. Find the length of the altitude from C to side AB')
def _(m, p):
    v = float(m[1]) * math.sin(int(m[2]) * D)
    return lambda x: rclose(v, x)


@fam(r'exact value of (sin|cos|tan)\((-?\d+)°\) = (sin|cos|tan)\((-?\d+)° ([+-]) (-?\d+)°\)')
def _(m, p):
    f = {'sin': math.sin, 'cos': math.cos, 'tan': math.tan}[m[1]]
    lhs = f(int(m[2]) * D)
    rhs_angle = int(m[4]) + (int(m[6]) if m[5] == '+' else -int(m[6]))
    if rhs_angle != int(m[2]): return lambda x: False
    return lambda x: close(N(x), lhs)


@fam(r'Rotate the point \((-?\d+), (-?\d+)\) by (\d+)° counterclockwise about the origin')
def _(m, p):
    x, y, t = int(m[1]), int(m[2]), int(m[3]) * D
    v = (x * math.cos(t) - y * math.sin(t), x * math.sin(t) + y * math.cos(t))
    return lambda a: (u := tup(a)) and close(u[0], v[0]) and close(u[1], v[1])


@fam(r'Write the 2 × 2 matrix that rotates points (\d+)° counterclockwise')
def _(m, p):
    t = int(m[1]) * D
    R = [[math.cos(t), -math.sin(t)], [math.sin(t), math.cos(t)]]
    return lambda a: all(close(x, y) for r1, r2 in zip(mat(a), R) for x, y in zip(r1, r2))


@fam(r'For A = \[([^\]]+)\], find the entry a([₁₂₃₄])([₁₂₃₄])')
def _(m, p):
    A = mat('[' + m[1] + ']'); t = '₁₂₃₄'
    v = A[t.index(m[2])][t.index(m[3])]
    return lambda a: close(N(a), v)


def mm(A, B):
    return [[sum(A[i][k] * B[k][j] for k in range(len(B))) for j in range(len(B[0]))] for i in range(len(A))]


def meq(A, B):
    return len(A) == len(B) and all(len(r) == len(s) and all(close(x, y) for x, y in zip(r, s)) for r, s in zip(A, B))


@fam(r'A = \[([^\]]+)\] and B = \[([^\]]+)\]\. Find (A \+ B|A - B|B - A|AB|BA)\.')
def _(m, p):
    A, B = mat('[' + m[1] + ']'), mat('[' + m[2] + ']')
    op = m[3]
    if op == 'AB': R = mm(A, B)
    elif op == 'BA': R = mm(B, A)
    else:
        X, Y = (A, B) if op != 'B - A' else (B, A)
        s = 1 if '+' in op else -1
        R = [[x + s * y for x, y in zip(r1, r2)] for r1, r2 in zip(X, Y)]
    return lambda a: meq(mat(a), R)


@fam(r'Find the determinant of \[([^\]]+)\]\.')
def _(m, p):
    A = mat('[' + m[1] + ']')
    import numpy as np
    v = float(np.linalg.det(np.array(A, float)))
    return lambda a: close(N(a), v, 1e-6)


@fam(r'Find the inverse of A = \[([^\]]+)\]\.')
def _(m, p):
    import numpy as np
    A = np.array(mat('[' + m[1] + ']'), float)
    Inv = np.linalg.inv(A).tolist()
    return lambda a: meq(mat(a), Inv)


@fam(r'Apply the row operation R([₁₂₃]) → R([₁₂₃]) ([+-]) (\d*)R([₁₂₃]) to \[([^\]]+)\]\.')
def _(m, p):
    A = mat('[' + m[6] + ']'); t = '₁₂₃'
    i, j, k = t.index(m[1]), t.index(m[2]), t.index(m[5]); c = int(m[4] or 1) * (1 if m[3] == '+' else -1)
    R = [r[:] for r in A]; R[i] = [x + c * y for x, y in zip(A[j], A[k])]
    return lambda a: meq(mat(a), R)


@fam(r'Write the system as AX = B and solve with X = A⁻¹B: ([^;]+); (.+?)\.$|reduced row-echelon form of the augmented matrix \(technology allowed\) to solve: ([^;]+); (.+?)\.$')
def _(m, p):
    e1, e2 = (m[1], m[2]) if m[1] else (m[3], m[4])
    eqs = [e1] + e2.split('; ') if ';' in e2 else [e1, e2]
    if len(eqs) == 3:
        import numpy as np
        rows = [lin3(e) for e in eqs]
        sol = np.linalg.solve(np.array([r[0] for r in rows], float), np.array([r[1] for r in rows], float))
        return lambda a: (t := tup(a)) and len(t) == 3 and all(close(t[i], sol[i]) for i in range(3))
    r1, r2 = lin3(e1), lin3(e2)
    a1, b1, c1 = r1[0][0], r1[0][1], r1[1]; a2, b2, c2 = r2[0][0], r2[0][1], r2[1]
    d = a1 * b2 - a2 * b1
    x, y = (c1 * b2 - c2 * b1) / d, (a1 * c2 - a2 * c1) / d
    return lambda a: (t := tup(a)) and close(t[0], x) and close(t[1], y)


@fam(r'Use the matrix for .+?, \[([^\]]+)\], to find the image of \((-?\d+), (-?\d+)\)\.')
def _(m, p):
    A = mat('[' + m[1] + ']'); v = [int(m[2]), int(m[3])]
    R = [A[0][0] * v[0] + A[0][1] * v[1], A[1][0] * v[0] + A[1][1] * v[1]]
    return lambda a: (t := tup(a)) and close(t[0], R[0]) and close(t[1], R[1])


@fam(r'Find Av for A = \[([^\]]+)\] and v = ⟨(-?\d+), (-?\d+)⟩\.')
def _(m, p):
    A = mat('[' + m[1] + ']'); v = [int(m[2]), int(m[3])]
    R = [A[0][0] * v[0] + A[0][1] * v[1], A[1][0] * v[0] + A[1][1] * v[1]]
    return lambda a: (t := tup(a)) and close(t[0], R[0]) and close(t[1], R[1])


@fam(r'In how many ways can (\d+) runners finish first through \w+ in a race with (\d+) runners')
def _(m, p):
    return lambda a: close(N(a), math.perm(int(m[2]), int(m[1])))


@fam(r'A trial succeeds with probability ([\d/.]+)\. In (\d+) independent trials, find P\(exactly (\d+) success')
def _(m, p):
    pp, n, k = E(m[1]), int(m[2]), int(m[3])
    return lambda a: rclose(math.comb(n, k) * pp ** k * (1 - pp) ** (n - k), a)


@fam(r'A random variable X has (P\(X = .+?)\. Find the expected value E\(X\)\.')
def _(m, p):
    pairs = re.findall(r'P\(X = (-?\d+)\) = ([\d/]+)', m[1])
    v = sum(int(x) * E(pr) for x, pr in pairs)
    return lambda a: close(N(a), v)


@fam(r'A game costs \$(\d+) to play\. (A player wins .+?) \(prizes do not include the cost\)')
def _(m, p):
    v = sum(int(w) * E(pr) for w, pr in re.findall(r'wins \$(\d+) with probability ([\d/]+)', m[2])) - int(m[1])
    return lambda a: close(N(a), v)


@fam(r'mean ([\d.]+) and standard deviation ([\d.]+)\. Find the z-score of ([\d.]+)\. Round to the nearest hundredth')
def _(m, p):
    return lambda a: rclose((float(m[3]) - float(m[1])) / float(m[2]), a)


@fam(r'Find the (\d+)(?:st|nd|rd|th) term of the sequence (-?[\d/]+), (-?[\d/]+), (-?[\d/]+), (-?[\d/]+), …')
def _(m, p):
    n = int(m[1]); t = [E(m[i]) for i in (2, 3, 4, 5)]
    if close(t[1] - t[0], t[2] - t[1]) and close(t[2] - t[1], t[3] - t[2]): v = t[0] + (n - 1) * (t[1] - t[0])
    else: v = t[0] * (t[1] / t[0]) ** (n - 1)
    return lambda a: close(N(a), v)


@fam(r'Find the sum of the first (\d+) terms of the series (.+?) \+ …')
def _(m, p):
    n = int(m[1]); s = m[2].replace(' ', '')
    terms = [E(x) for x in re.findall(r'[+-]?[\d/]+', s)]
    d = terms[1] - terms[0]
    if close(terms[2] - terms[1], d): v = sum(terms[0] + i * d for i in range(n))
    else:
        r = terms[1] / terms[0]; v = sum(terms[0] * r ** i for i in range(n))
    return lambda a: close(N(a), v)


@fam(r'Find the sum of the infinite geometric series (.+?) [+-] …')
def _(m, p):
    s = m[1].replace(' ', '')
    terms = [E(x) for x in re.findall(r'[+-]?\d+(?:/\d+)?', s)]
    r = terms[1] / terms[0]
    return lambda a: close(N(a), terms[0] / (1 - r))


@fam(r'Evaluate Σ from k = (-?\d+) to (\d+) of \((.+?)\)\.')
def _(m, p):
    v = sum(ev(m[3], {'k': k}) for k in range(int(m[1]), int(m[2]) + 1))
    return lambda a: close(N(a), v)


@fam(r'Evaluate lim \(x → (-?\d+)\) \((.+?)\)/\((.+?)\)\.')
def _(m, p):
    c = int(m[1]); f = lambda x: ev(m[2], {'x': x}) / ev(m[3], {'x': x})
    v = (f(c + 1e-6) + f(c - 1e-6)) / 2
    return lambda a: close(N(a), v, 1e-4)


@fam(r'Find the exact value of (sin|cos|tan|sec|csc|cot)\((-?\d+)°\)\.')
def _(m, p):
    t = int(m[2]) * D
    f = {'sin': math.sin, 'cos': math.cos, 'tan': math.tan, 'sec': lambda z: 1 / math.cos(z), 'csc': lambda z: 1 / math.sin(z), 'cot': lambda z: 1 / math.tan(z)}[m[1]]
    return lambda a: close(N(a), f(t), 1e-6)


@fam(r'Convert (.+?) radians to degrees\.')
def _(m, p):
    return lambda a: close(N(a), math.degrees(E(m[1])))


@fam(r'Convert (-?\d+)° to radians\.')
def _(m, p):
    return lambda a: close(N(a), int(m[1]) * D)


@fam(r'angle between 0° and 360° that is coterminal with (-?\d+)°')
def _(m, p):
    return lambda a: close(N(a), int(m[1]) % 360)


@fam(r'A circle has radius (\d+) cm\. Find the exact length of the arc intercepted by a central angle of (.+?) radians')
def _(m, p):
    return lambda a: close(N(a), int(m[1]) * E(m[2]))


@fam(r'Find the amplitude of y = (-?\d*)(?:sin|cos)')
def _(m, p):
    a = 1 if m[1] in ('', '-') else abs(int(m[1]))
    return lambda x: close(N(x), a)


@fam(r'Find the exact value of (sin|cos|tan)⁻¹\((.+?)\) in degrees\.')
def _(m, p):
    f = {'sin': math.asin, 'cos': math.acos, 'tan': math.atan}[m[1]]
    return lambda a: close(N(a), math.degrees(f(E(m[2]))), 1e-6)


@fam(r'Use a calculator to find (sin|cos|tan)⁻¹\((-?[\d.]+)\) in radians, to the nearest thousandth')
def _(m, p):
    f = {'sin': math.asin, 'cos': math.acos, 'tan': math.atan}[m[1]]
    return lambda a: rclose(f(float(m[2])), a)


@fam(r'Given (sin|cos|tan) θ = (-?[\d/]+) and θ is in Quadrant (I|II|III|IV), find (sin|cos|tan|sec|csc|cot)(?: θ|\(2θ\))')
def _(m, p):
    q = {'I': 1, 'II': 2, 'III': 3, 'IV': 4}[m[3]]
    v = E(m[2]); sx = 1 if q in (1, 4) else -1; sy = 1 if q in (1, 2) else -1
    if m[1] == 'sin': s = v; c = sx * math.sqrt(1 - v * v)
    elif m[1] == 'cos': c = v; s = sy * math.sqrt(1 - v * v)
    else:
        h = math.sqrt(1 + v * v); c = sx / h; s = v * c
    double = '(2θ)' in m.group(0)
    if double: s, c = 2 * s * c, c * c - s * s
    w = {'sin': s, 'cos': c, 'tan': s / c, 'sec': 1 / c, 'csc': 1 / s, 'cot': c / s}[m[4]]
    return lambda a: close(N(a), w, 1e-6)


@fam(r'Simplify \((-?\d+) ([+-]) (\d*)i\) · \((-?\d+) ([+-]) (\d*)i\)')
def _(m, p):
    z1 = complex(int(m[1]), int(m[3] or 1) * (1 if m[2] == '+' else -1)); z2 = complex(int(m[4]), int(m[6] or 1) * (1 if m[5] == '+' else -1))
    z = z1 * z2
    def chk(a):
        s = str(a).replace('−', '-').replace(' ', '')
        if re.fullmatch(r'-?\d+', s): return close(int(s), z.real) and abs(z.imag) < 1e-9
        mm_ = re.fullmatch(r'(-?\d+)([+-])(\d*)i', s)
        return bool(mm_) and close(int(mm_[1]), z.real) and close(int(mm_[3] or 1) * (1 if mm_[2] == '+' else -1), z.imag)
    return chk


@fam(r'Find the distance between (-?\d+) ([+-]) (\d*)i and (-?\d+) ([+-]) (\d*)i in the complex plane')
def _(m, p):
    z1 = complex(int(m[1]), int(m[3] or 1) * (1 if m[2] == '+' else -1)); z2 = complex(int(m[4]), int(m[6] or 1) * (1 if m[5] == '+' else -1))
    return lambda a: close(N(a), abs(z1 - z2))


@fam(r'component form of the vector from P\((-?\d+), (-?\d+)\) to Q\((-?\d+), (-?\d+)\)')
def _(m, p):
    x1, y1, x2, y2 = map(int, m.groups())
    return lambda a: (t := tup(a)) and close(t[0], x2 - x1) and close(t[1], y2 - y1)


@fam(r'u = ⟨(-?\d+), (-?\d+)⟩ and v = ⟨(-?\d+), (-?\d+)⟩\. Find (u \+ v|u - v|v - u)')
def _(m, p):
    u, v = (int(m[1]), int(m[2])), (int(m[3]), int(m[4]))
    r = {'u + v': (u[0] + v[0], u[1] + v[1]), 'u - v': (u[0] - v[0], u[1] - v[1]), 'v - u': (v[0] - u[0], v[1] - u[1])}[m[5]]
    return lambda a: (t := tup(a)) and close(t[0], r[0]) and close(t[1], r[1])


@fam(r'Find u · v for u = ⟨(-?\d+), (-?\d+)⟩ and v = ⟨(-?\d+), (-?\d+)⟩')
def _(m, p):
    a, b, c, d = map(int, m.groups())
    return lambda x: close(N(x), a * c + b * d)


@fam(r'Find the magnitude of v = ⟨(-?\d+), (-?\d+)⟩')
def _(m, p):
    return lambda a: close(N(a), math.hypot(int(m[1]), int(m[2])))


@fam(r'moves straight from \((-?\d+), (-?\d+)\) to \((-?\d+), (-?\d+)\) on a grid in kilometers\. Find the magnitude')
def _(m, p):
    x1, y1, x2, y2 = map(int, m.groups())
    return lambda a: close(N(a), math.hypot(x2 - x1, y2 - y1))


@fam(r'A vector has magnitude (\d+) and direction angle (\d+)°\. Write it in exact component form')
def _(m, p):
    r, t = int(m[1]), int(m[2]) * D
    return lambda a: (u := tup(a)) and close(u[0], r * math.cos(t)) and close(u[1], r * math.sin(t))


@fam(r'Two forces of ([\d.]+) N and ([\d.]+) N act on an object with an angle of (\d+)° between them\. Find the magnitude')
def _(m, p):
    a, b, t = float(m[1]), float(m[2]), int(m[3]) * D
    return lambda x: rclose(math.sqrt(a * a + b * b + 2 * a * b * math.cos(t)), x)


@fam(r'A boat heads due east at ([\d.]+) km/h while the current flows due north at ([\d.]+) km/h\. Find the boat\'s resultant speed')
def _(m, p):
    return lambda x: rclose(math.hypot(float(m[1]), float(m[2])), x)


@fam(r'Convert the polar point \((-?\d+), (.+?)\) to rectangular coordinates')
def _(m, p):
    r, t = int(m[1]), E(m[2])
    return lambda a: (u := tup(a)) and close(u[0], r * math.cos(t)) and close(u[1], r * math.sin(t))


@fam(r'How many petals does the rose curve r = \d*(sin|cos)\((\d+)θ\) have')
def _(m, p):
    n = int(m[2])
    return lambda a: close(N(a), n if n % 2 else 2 * n)


@fam(r'Eliminate the parameter: x = (.+?), y = (.+?)\. Write an equation in x and y')
def _(m, p):
    def chk(a):
        s = str(a).replace('−', '-')
        mm_ = re.fullmatch(r'\s*y\s*=\s*(.+?)\s*\.?', s)
        if not mm_ and '=' in s:  # implicit equation: both sides agree along the curve
            l, r = s.split('=')
            pts = [(ev(m[1], {'t': t}), ev(m[2], {'t': t})) for t in (-1.3, 0.4, 2.2, 3.0)]
            return all(close(ev(l, {'x': x, 'y': y}), ev(r, {'x': x, 'y': y})) for x, y in pts)
        if not mm_: return False
        return all(close(ev(mm_[1], {'x': ev(m[1], {'t': t})}), ev(m[2], {'t': t})) for t in (-1.3, 0.4, 2.2))
    return chk


@fam(r'Solve (\d*)(sin|cos|tan)\(x\) = (.+?) for 0 ≤ x < 2π\.')
def _(m, p):
    f = {'sin': math.sin, 'cos': math.cos, 'tan': math.tan}[m[2]]; v = E(m[3]) / (int(m[1]) if m[1] else 1); m = [None, m[2]]
    xs = [i * math.pi / 12 for i in range(24)]
    want = [x for x in xs if abs(f(x) - v) < 1e-9 and not (m[1] == 'tan' and abs(math.cos(x)) < 1e-9)]
    def chk(a):
        got = sorted(ev(x, {}) for x in re.split(r'\s+or\s+|,\s*', re.sub(r'x\s*=\s*', '', str(a).replace('−', '-'))) if x.strip())
        return len(got) == len(want) and all(close(g, w) for g, w in zip(got, want))
    return chk


exec(open(__import__('os').path.join(__import__('os').path.dirname(__import__('os').path.abspath(__file__)), 'pc_verify_more.py')).read())

# ------------------------------------------------------------------ run
checked = 0
unparsed = []
for q in I:
    if q['format'] not in ('short-answer', 'multiple-choice'):
        continue
    body, stu = inner(q)
    text = body.strip()
    hit = None
    for rx, fn in FAM:
        mm_ = rx.search(text)
        if mm_:
            hit = (rx, fn, mm_); break
    if not hit:
        res['unmatched'] += 1
        continue
    try:
        chk = hit[1](hit[2], text)
    except Exception as e:  # noqa: BLE001
        res['family-error'] += 1; flag(q, 'family error', repr(e)); continue
    if chk is None:
        res['skipped'] += 1; continue
    try:
        ok = bool(chk(q['answer']))
    except Exception as e:  # noqa: BLE001
        ok = False
        res['key-parse-error'] += 1; unparsed.append((q['id'], q['answer'], repr(e))); continue  # a limit of this checker, not a wrong key
    checked += 1
    if not ok:
        flag(q, 'KEY DISAGREES')
    for o in q.get('options', []):
        try:
            if bool(chk(o['text'])) != o['correct']:
                flag(q, 'OPTION', o)
        except Exception:
            if o['correct']: flag(q, 'OPTION parse', o)
    if stu is not None:
        try:
            if chk(stu): flag(q, 'STUDENT ANSWER IS CORRECT', stu)
        except Exception:
            pass
    res['checked'] += 1
print(res)
for f in flags: print(f)
print('checked', checked, 'flags', len(flags), 'keys this checker cannot read', len(unparsed))
if flags or checked < MIN:
    sys.exit(1)
