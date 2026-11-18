# Extra families (loaded by pc_verify.py before the run section).


@fam(r'In triangle ABC, A = (\d+)°, B = (\d+)°, and a = ([\d.]+)\. Find (b|c) to the nearest tenth')
def _(m, p):
    A, B, a = int(m[1]) * D, int(m[2]) * D, float(m[3]); C = math.pi - A - B
    v = a * math.sin(B if m[4] == 'b' else C) / math.sin(A)
    return lambda x: rclose(v, x)


@fam(r'flying ([\d.]+) ft above the ground and its string makes a (\d+)° angle with the ground\. How long is the string')
def _(m, p):
    return lambda x: rclose(float(m[1]) / math.sin(int(m[2]) * D), x)


@fam(r'A ramp rises ([\d.]+) ft over a horizontal distance of ([\d.]+) ft\. Find the angle')
def _(m, p):
    return lambda x: rclose(math.degrees(math.atan(float(m[1]) / float(m[2]))), x)


def solve_lin(eq):
    l, r = eq.replace('−', '-').split('=')
    f = lambda x: ev(l, {'x': x}) - ev(r, {'x': x})
    a = f(1) - f(0)
    return -f(0) / a


@fam(r'^Use the graph to solve (.+?=.+?)\.$')
def _(m, p):
    l, r = m[1].replace('−', '-').split('=')
    f = lambda x: ev(l, {'x': x}) - ev(r, {'x': x})
    xs = [i / 100 for i in range(-3000, 3001)]
    want = []
    for a, b in zip(xs, xs[1:]):
        fa, fb = f(a), f(b)
        if abs(fa) < 1e-12: want.append(a)
        elif fa * fb < 0:
            lo, hi = a, b
            for _ in range(60):
                mid = (lo + hi) / 2
                if f(lo) * f(mid) <= 0: hi = mid
                else: lo = mid
            want.append(lo)
    def chk(ans):
        got = sorted(E(x) for x in re.split(r'\s+or\s+|,\s*', re.sub(r'x\s*=\s*', '', str(ans).replace('−', '-'))) if x.strip())
        return len(got) == len(want) and all(abs(g - w) < 1e-6 for g, w in zip(got, want))
    return chk


@fam(r'Find the vertex of the parabola \((x|y) ([+-]) (\d+)\)² = (-?\d+)\(?(y|x)(?: ([+-]) (\d+)\))?\.')
def _(m, p):
    a = (-1 if m[2] == '+' else 1) * int(m[3]); b = 0 if not m[6] else (-1 if m[6] == '+' else 1) * int(m[7])
    v = (a, b) if m[1] == 'x' else (b, a)
    return lambda x: (t := tup(x)) and close(t[0], v[0]) and close(t[1], v[1])


def interval_set(s):
    """Interval-notation text → membership function."""
    s = s.replace('−', '-').replace(' ', '').rstrip('.')
    parts = s.split('∪')
    iv = []
    for pt in parts:
        mm_ = re.fullmatch(r'([\[(])(-?∞|-?[\d/.]+),(∞|-?[\d/.]+)([\])])', pt)
        if not mm_: raise ValueError(pt)
        if ('∞' in mm_[2] and mm_[1] == '[') or ('∞' in mm_[3] and mm_[4] == ']'): raise ValueError('bracket on infinity')
        lo = -math.inf if '∞' in mm_[2] else E(mm_[2]); hi = math.inf if '∞' in mm_[3] else E(mm_[3])
        ENDS.update(v for v in (lo, hi) if abs(v) != math.inf)
        iv.append((lo, mm_[1] == '[', hi, mm_[4] == ']'))
    return lambda x: any((x > lo or (lc and x == lo)) and (x < hi or (hc and x == hi)) for lo, lc, hi, hc in iv)


TESTS = [i / 4 for i in range(-200, 201)]
ENDS = set()


def same_set(f, g):
    pts = TESTS + [e + d for e in ENDS for d in (-1e-7, 0, 1e-7)]
    return all(bool(f(x)) == bool(g(x)) for x in pts)


OPS = {'<': lambda a, b: a < b, '>': lambda a, b: a > b, '≤': lambda a, b: a <= b, '≥': lambda a, b: a >= b}


@fam(r'^Solve (.+?)\. Write the answer in interval notation\.')
def _(m, p):
    e = m[1].replace('−', '-')
    toks = re.split(r'\s*(<|>|≤|≥)\s*', e)
    def truth(x):
        vals = [ev(t, {'x': x}) for t in toks[0::2]]
        return all(OPS[o](vals[i], vals[i + 1]) for i, o in enumerate(toks[1::2]))
    def chk(a):
        ENDS.clear()
        try: f = interval_set(str(a))
        except ValueError: return False
        return same_set(f, truth)
    return chk


@fam(r'^Write (.+?) in interval notation\.')
def _(m, p):
    e = m[1].replace('−', '-')
    toks = re.split(r'\s*(<|>|≤|≥)\s*', e)
    def truth(x):
        vals = [ev(t, {'x': x}) for t in toks[0::2]]
        return all(OPS[o](vals[i], vals[i + 1]) for i, o in enumerate(toks[1::2]))
    return lambda a: same_set(interval_set(str(a)), truth)


@fam(r'^Is \((-?\d+), (-?\d+)\) a solution of y (<|>|≤|≥) (.+?)\?')
def _(m, p):
    x, y = int(m[1]), int(m[2])
    t = OPS[m[3]](y, ev(m[4], {'x': x}))
    return lambda a: str(a).strip().rstrip('.').lower().startswith('yes' if t else 'no')


@fam(r'What is the y-intercept of f\(x\) = (.+?)\?')
def _(m, p):
    v = ev(m[1], {'x': 0})
    return lambda a: ((t := tup(a)) and close(t[0], 0) and close(t[1], v)) or (re.fullmatch(r'-?[\d/.]+', str(a).strip()) and close(N(a), v))


@fam(r'Find the slope of the line (-?\d*)x ([+-]) (\d*)y = (-?\d+)\.')
def _(m, p):
    A = 1 if m[1] == '' else -1 if m[1] == '-' else int(m[1]); B = int(m[3] or 1) * (1 if m[2] == '+' else -1)
    return lambda a: close(N(a), -A / B)


@fam(r'A population follows P\(t\) = (\d+)/\(1 \+ (\d+)e\^\((-?[\d.]+)t\)\)\. What is the (initial population P\(0\)|carrying capacity)')
def _(m, p):
    L, A = int(m[1]), int(m[2])
    v = L / (1 + A) if 'initial' in m[4] else L
    return lambda a: rclose(v, a) if '.' in str(a) else abs(N(a) - v) <= 0.5 + 1e-9


@fam(r'^Solve (\d+)ˣ = ([\d.]+)\. Round to the nearest thousandth')
def _(m, p):
    return lambda a: rclose(math.log(float(m[2])) / math.log(int(m[1])), a)


@fam(r'^Solve e\^\((\d+)x\) = ([\d.]+)\. Round to the nearest thousandth')
def _(m, p):
    return lambda a: rclose(math.log(float(m[2])) / int(m[1]), a)


@fam(r'Find the domain of f\(x\) = ln\((-?\d*)x ([+-]) (\d+)\)\.')
def _(m, p):
    a = 1 if m[1] == '' else -1 if m[1] == '-' else int(m[1]); b = int(m[3]) * (1 if m[2] == '+' else -1)
    return lambda s: same_set(interval_set(str(s)), lambda x: a * x + b > 0)


@fam(r'A circle has radius (\d+) in\. Find the exact area of the sector with central angle (.+?) radians')
def _(m, p):
    return lambda a: close(N(a), 0.5 * int(m[1]) ** 2 * E(m[2]))


@fam(r'Find the exact value of (sin|cos|tan)⁻¹\((.+?)\) in radians\.')
def _(m, p):
    f = {'sin': math.asin, 'cos': math.acos, 'tan': math.atan}[m[1]]
    return lambda a: close(N(a), f(E(m[2])))


@fam(r'A bag holds (\d+) (\w+), (\d+) (\w+), (\d+) (\w+) marbles\. One is drawn at random\. Find P\((not )?(\w+)\)')
def _(m, p):
    cnt = {m[2]: int(m[1]), m[4]: int(m[3]), m[6]: int(m[5])}; tot = sum(cnt.values())
    v = cnt[m[8]] / tot
    if m[7]: v = 1 - v
    return lambda a: close(N(a), v)


@fam(r'A bag holds (\d+) (\w+), (\d+) (\w+), (\d+) (\w+) marbles\. Two are drawn (with|without) replacement\. Find P\(first (\w+), then (\w+)\)')
def _(m, p):
    cnt = {m[2]: int(m[1]), m[4]: int(m[3]), m[6]: int(m[5])}; tot = sum(cnt.values())
    a, b = m[8], m[9]
    if m[7] == 'with': v = cnt[a] / tot * cnt[b] / tot
    else: v = cnt[a] / tot * (cnt[b] - (a == b)) / (tot - 1)
    return lambda x: close(N(x), v)


@fam(r'a club of (\d+) members choose a president and a vice president')
def _(m, p):
    return lambda a: close(N(a), math.perm(int(m[1]), 2))


@fam(r'How many different (\d+)-topping pizzas can be made from (\d+) toppings')
def _(m, p):
    return lambda a: close(N(a), math.comb(int(m[2]), int(m[1])))


@fam(r'Find the vertices of the hyperbola (?:\(x ([+-]) (\d+)\)|x)²/(\d+) - (?:\(y ([+-]) (\d+)\)|y)²/(\d+) = 1\.')
def _(m, p):
    h = 0 if not m[1] else (-1 if m[1] == '+' else 1) * int(m[2]); k = 0 if not m[4] else (-1 if m[4] == '+' else 1) * int(m[5]); a = math.sqrt(int(m[3]))
    want = sorted([(h + a, k), (h - a, k)])
    def chk(s):
        got = sorted(tuple(E(x) for x in pt.split(',')) for pt in re.findall(r'\(([^()]+)\)', str(s)))
        return len(got) == 2 and all(close(g[0], w[0]) and close(g[1], w[1]) for g, w in zip(got, want))
    return chk


def conic_check(s, pts, notpts):
    """Equation text with = : true on pts, false on notpts."""
    l, r = str(s).replace('−', '-').split('=')
    f = lambda x, y: ev(l, {'x': x, 'y': y}) - ev(r, {'x': x, 'y': y})
    return all(abs(f(*q)) < 1e-6 for q in pts) and all(abs(f(*q)) > 1e-6 for q in notpts)


@fam(r'equation of the ellipse with vertices \((-?\d+), (-?\d+)\), \((-?\d+), (-?\d+)\) and co-vertices \((-?\d+), (-?\d+)\), \((-?\d+), (-?\d+)\)')
def _(m, p):
    P = [(int(m[i]), int(m[i + 1])) for i in (1, 3, 5, 7)]
    cx, cy = (P[0][0] + P[1][0]) / 2, (P[0][1] + P[1][1]) / 2
    return lambda s: conic_check(s, P, [(cx, cy), (cx + 0.5, cy + 0.5)])


@fam(r'equation of the hyperbola with vertices \((-?\d+), (-?\d+)\), \((-?\d+), (-?\d+)\) and foci \((-?\d+), (-?\d+)\), \((-?\d+), (-?\d+)\)')
def _(m, p):
    V = [(int(m[1]), int(m[2])), (int(m[3]), int(m[4]))]; Fo = [(int(m[5]), int(m[6])), (int(m[7]), int(m[8]))]
    cx, cy = (V[0][0] + V[1][0]) / 2, (V[0][1] + V[1][1]) / 2
    a = math.dist(V[0], V[1]) / 2; c = math.dist(Fo[0], Fo[1]) / 2; b2 = c * c - a * a
    vert = V[0][0] == V[1][0]
    def onh(t):
        if vert: return (cx + math.sqrt(b2) * math.sinh(t), cy + a * math.cosh(t))
        return (cx + a * math.cosh(t), cy + math.sqrt(b2) * math.sinh(t))
    return lambda s: conic_check(s, V + [onh(0.7), onh(-1.1)], [(cx, cy)])


@fam(r'^A network has roads: (.+?)\. Write its adjacency matrix \(order ([A-Z, ]+)\)')
def _(m, p):
    order = [x.strip() for x in m[2].split(',')]
    A = [[0] * len(order) for _ in order]
    for e in m[1].split(','):
        a, b = e.strip().split('–'); i, j = order.index(a), order.index(b); A[i][j] = A[j][i] = 1
    return lambda s: meq(mat(s), A)


@fam(r'A game sprite at \((-?\d+), (-?\d+)\) undergoes a .+?\(matrix \[([^\]]+)\]\) and then moves by the translation ⟨(-?\d+), (-?\d+)⟩')
def _(m, p):
    A = mat('[' + m[3] + ']'); x, y = int(m[1]), int(m[2])
    R = (A[0][0] * x + A[0][1] * y + int(m[4]), A[1][0] * x + A[1][1] * y + int(m[5]))
    return lambda s: (t := tup(s)) and close(t[0], R[0]) and close(t[1], R[1])


@fam(r'Rotate v = ⟨(-?\d+), (-?\d+)⟩ by (\d+)° counterclockwise using the rotation matrix')
def _(m, p):
    x, y, t = int(m[1]), int(m[2]), int(m[3]) * D
    v = (x * math.cos(t) - y * math.sin(t), x * math.sin(t) + y * math.cos(t))
    return lambda a: (u := tup(a)) and close(u[0], v[0]) and close(u[1], v[1])


@fam(r'terminal side of θ = (.+?) intersects the unit circle')
def _(m, p):
    t = E(m[1].replace('°', '')) * (D if '°' in m[1] else 1)
    return lambda a: (u := tup(a)) and close(u[0], math.cos(t)) and close(u[1], math.sin(t))


@fam(r'Find the reference angle for θ = (.+?)\.$')
def _(m, p):
    deg = '°' in m[1]
    t = E(m[1].replace('°', '')) * (D if deg else 1)
    t %= 2 * math.pi
    r = min(t % math.pi, math.pi - t % math.pi)
    return lambda a: close(N(a) * (D if deg or '°' in str(a) else 1), r)


@fam(r'Is B = \[([^\]]+)\] the inverse of A = \[([^\]]+)\]\?')
def _(m, p):
    P_ = mm(mat('[' + m[2] + ']'), mat('[' + m[1] + ']'))
    t = meq(P_, [[1, 0], [0, 1]])
    return lambda a: str(a).strip().lower().startswith('yes' if t else 'no')
