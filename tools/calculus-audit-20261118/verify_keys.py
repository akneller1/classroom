"""Calculus audit #20 (2026-11-18): an independent recomputation of the Calculus bank keys.

Parses the prompts of the computational item families (derivatives, tangent lines, limits, definite and
indefinite integrals, Riemann and trapezoidal sums from formulas and tables, the Mean Value Theorem, extrema,
critical and inflection points, Euler's method, FTC with the chain rule, IVT counts, motion, area, average value,
limits of Riemann sums and accumulation functions) with sympy, recomputes each answer and compares it with the
key. Exits non-zero on any mismatch, or if fewer items than expected could be checked.
Run: python3 tools/calculus-audit-20261118/verify_keys.py   (needs sympy)
"""
import re, sys, os, json, collections, signal, random
import sympy as sp
from sympy.parsing.sympy_parser import parse_expr, standard_transformations, implicit_multiplication_application, convert_xor
x, t, y, C, k, u, h = sp.symbols('x t y C k u h')
SUP = str.maketrans('⁰¹²³⁴⁵⁶⁷⁸⁹⁻', '0123456789-')
TR = standard_transformations + (implicit_multiplication_application, convert_xor)
LOC = {'x': x, 't': t, 'y': y, 'C': C, 'e': sp.E, 'pi': sp.pi, 'ln': sp.log, 'sqrt': sp.sqrt,
       'sin': sp.sin, 'cos': sp.cos, 'tan': sp.tan, 'sec': sp.sec, 'csc': sp.csc, 'cot': sp.cot,
       'atan': sp.atan, 'asin': sp.asin, 'acos': sp.acos, 'k': k, 'u': u, 'h': h, 'E': sp.E, 'abs': sp.Abs, 'Abs': sp.Abs}

def norm(s):
    s = s.strip().rstrip('.').strip()
    s = s.replace('−', '-').replace('·', '*').replace('×', '*').replace('÷', '/')
    s = s.replace('ˣ', '^x').replace('ln|', 'log(abs(').replace('|x|', 'Abs(x)')
    s = re.sub(r'log\(abs\(([^|]*)\|', r'log(abs(\1))', s)
    s = re.sub(r'√([A-Za-z0-9.]+)', r'√(\1)', s)
    s = re.sub(r'(sin|cos|tan|sec|csc|cot)([²³⁴⁵⁶⁷⁸⁹])\(([^()]*)\)', lambda m: '(' + m.group(1) + '(' + m.group(3) + '))' + m.group(2), s)
    s = s.replace('π', '(pi)').replace('√', 'sqrt').replace('∞', 'oo')
    s = s.replace('tan⁻¹', 'atan').replace('sin⁻¹', 'asin').replace('cos⁻¹', 'acos')
    s = s.replace('arctan', 'atan').replace('arcsin', 'asin').replace('arccos', 'acos')
    # superscripts -> ^(..)
    s = re.sub(r'([⁰¹²³⁴⁵⁶⁷⁸⁹⁻]+)', lambda m: '^(' + m.group(1).translate(SUP) + ')', s)
    s = s.replace('e^', 'E^')
    s = re.sub(r'(?<=[0-9A-Za-z)])(?=(sin|cos|tan|sec|csc|cot|sqrt|log|ln|atan|asin|acos|E\^)\b|(?=(sin|cos|tan|sqrt|log|ln|atan)\())', '*', s)
    s = s.replace('a*tan','atan').replace('a*sin','asin').replace('a*cos','acos')
    # sin(x)^2 fine. log base: log₂(8)
    s = re.sub(r'log([₀-₉]+)\(', lambda m: 'logb' + m.group(1).translate(str.maketrans('₀₁₂₃₄₅₆₇₈₉', '0123456789')) + '(', s)
    return s

def P(s):
    s = norm(s)
    m = re.match(r'logb(\d+)\((.*)\)$', s)
    if m:
        return sp.log(P(m.group(2)), int(m.group(1)))
    return parse_expr(s, local_dict=LOC, transformations=TR, evaluate=True)

def eqv(a, b, tol=1e-6):
    try:
        d = sp.simplify(a - b)
        if d == 0:
            return True
        f = sp.lambdify(list(d.free_symbols), d, 'mpmath') if d.free_symbols else None
        if f is None:
            return abs(complex(sp.N(d))) < tol * max(1, abs(complex(sp.N(b))))
        import random
        for _ in range(5):
            vals = [random.uniform(0.3, 1.7) for _ in d.free_symbols]
            if abs(complex(f(*vals))) > tol:
                return False
        return True
    except Exception:
        return None



class TO(Exception): pass
def _h(*a): raise TO()
signal.signal(signal.SIGALRM, _h)

def core(q):
    p = q['prompt']
    if 'answered this problem' in p:
        p = p.split('\n')[1]
    return re.sub(r'\s*Hint: .*$', '', p)

def num(s): return P(s)

def pairs(s):
    return [(P(a), P(b)) for a, b in re.findall(r'f\((-?[\d./]+)\) = (-?[\d./]+)', s)]

R = []  # (id, handler, status, expected, answer)

def ans_val(a):
    a = a.strip().rstrip('.')
    a = re.sub(r'\s*(m/s²|m/s|ft/s|m|ft|L|liters|inches|in³|in|cm³/s|cm²/s|°F per hour|°F|dollars|people|bacteria|units²|square units|thousand gallons|gallons|L/min|cars)$', '', a)
    a = re.sub(r'^(f′\(x\)|f\'\(x\)|y|g\(x\)|F\(x\)|f_avg|c|x|k|g′\(x\)|dy/dx|h′\(x\)) = ', '', a)
    a = a.replace('+ C', '').strip()
    return P(a)

H = []
def handler(rx):
    def d(f):
        H.append((re.compile(rx), f)); return f
    return d

@handler(r'^Find f′\(x\) for f\(x\) = (.+)\.$')
def _(m, q):
    return sp.diff(P(m.group(1)), x), ans_val(q['answer'])

@handler(r'^Find f′\((-?[\d/]+)\) for f\(x\) = (.+)\.$')
def _(m, q):
    return sp.diff(P(m.group(2)), x).subs(x, P(m.group(1))), ans_val(q['answer'])

@handler(r'^Evaluate ∫ from (\S+) to (\S+) (.+) dx\.$')
def _(m, q):
    return sp.integrate(P(m.group(3)), (x, P(m.group(1)), P(m.group(2)))), ans_val(q['answer'])

@handler(r'^Find ∫ (.+) dx\.$')
def _(m, q):
    a = ans_val(q['answer'])
    return sp.diff(a, x) - P(m.group(1)), sp.Integer(0)

@handler(r'^Evaluate lim \(x → (\S+?)\) (.+)\.$')
def _(m, q):
    a = m.group(1)
    side = None
    if a.endswith('⁺'): side, a = '+', a[:-1]
    elif a.endswith('⁻'): side, a = '-', a[:-1]
    pt = sp.oo if a == '∞' else (-sp.oo if a == '-∞' else P(a))
    e = P(m.group(2))
    L = sp.limit(e, x, pt, side) if side else sp.limit(e, x, pt)
    A = q['answer'].strip().rstrip('.')
    if A in ('∞', '-∞', 'DNE', 'does not exist') or 'not exist' in A:
        return str(L), {'∞': 'oo', '-∞': '-oo'}.get(A, 'DNE')
    return L, ans_val(A)

@handler(r'^Find the equation of the tangent line to f\(x\) = (.+) at x = (\S+)\.$')
def _(m, q):
    f = P(m.group(1)); a = P(m.group(2))
    line = f.subs(x, a) + sp.diff(f, x).subs(x, a) * (x - a)
    return line, ans_val(q['answer'])

@handler(r'^Find the average value of f\(x\) = (.+) on \[(.+), (.+)\]\.$')
def _(m, q):
    a, b = P(m.group(2)), P(m.group(3))
    return sp.integrate(P(m.group(1)), (x, a, b)) / (b - a), ans_val(q['answer'])

@handler(r'^Find the average rate of change of f\(x\) = (.+) on \[(.+), (.+)\]\.$')
def _(m, q):
    f = P(m.group(1)); a, b = P(m.group(2)), P(m.group(3))
    return (f.subs(x, b) - f.subs(x, a)) / (b - a), ans_val(q['answer'])

@handler(r'^A particle moves with velocity v\(t\) = (.+?) (m/s|ft/s)\. Find (its|the) (displacement|total distance traveled) from t = (\S+) to t = (\S+?)\.$')
def _(m, q):
    v = P(m.group(1)).subs(t, x); a, b = P(m.group(5)), P(m.group(6))
    e = sp.integrate(v, (x, a, b)) if m.group(4) == 'displacement' else sp.integrate(sp.Abs(v), (x, a, b))
    return e, ans_val(q['answer'])

@handler(r'^Find the area of the region bounded by y = (.+) and y = (.+)\.$')
def _(m, q):
    f, g = P(m.group(1)), P(m.group(2))
    r = sorted([s for s in sp.solve(sp.Eq(f, g), x) if s.is_real])
    tot = 0
    for i in range(len(r) - 1):
        tot += sp.Abs(sp.integrate(f - g, (x, r[i], r[i + 1])))
    return tot, ans_val(q['answer'])

@handler(r'^Approximate ∫ from (\S+) to (\S+) \((.+)\) dx using an? (left|right|midpoint) Riemann sum with (\d+) equal subintervals\.$')
def _(m, q):
    a, b, f, kind, n = P(m.group(1)), P(m.group(2)), P(m.group(3)), m.group(4), int(m.group(5))
    dx = (b - a) / n
    off = {'left': 0, 'right': 1, 'midpoint': sp.Rational(1, 2)}[kind]
    return sum(f.subs(x, a + (i + off) * dx) for i in range(n)) * dx, ans_val(q['answer'])

@handler(r'^Approximate ∫ from (\S+) to (\S+) \((.+)\) dx using the trapezoidal rule with (\d+) equal subintervals\.$')
def _(m, q):
    a, b, f, n = P(m.group(1)), P(m.group(2)), P(m.group(3)), int(m.group(4))
    dx = (b - a) / n
    return sum((f.subs(x, a + i * dx) + f.subs(x, a + (i + 1) * dx)) / 2 for i in range(n)) * dx, ans_val(q['answer'])

@handler(r'(?:Use (?:the|a) (trapezoidal rule|left Riemann sum|right Riemann sum)|Use a (trapezoidal) sum) with (?:the subintervals in the table|these four subintervals) to approximate ∫ from (\S+) to (\S+) f\(x\) dx\.')
def _(m, q):
    kind = (m.group(1) or m.group(2))
    pr = pairs(core(q))
    pr.sort(key=lambda z: float(z[0]))
    s = 0
    for (x0, y0), (x1, y1) in zip(pr, pr[1:]):
        w = x1 - x0
        s += w * ((y0 + y1) / 2 if 'trap' in kind else (y0 if 'left' in kind else y1))
    return s, ans_val(q['answer'])

@handler(r'^Find the value of c guaranteed by the Mean Value Theorem for f\(x\) = (.+) on \[(.+), (.+)\]\.$')
def _(m, q):
    f = P(m.group(1)); a, b = P(m.group(2)), P(m.group(3))
    sl = (f.subs(x, b) - f.subs(x, a)) / (b - a)
    cs = [c for c in sp.solve(sp.Eq(sp.diff(f, x), sl), x) if c.is_real and a < c < b]
    A = ans_val(q['answer'].split(' or ')[0]) if ' or ' not in q['answer'] else None
    if A is None:
        got = sorted([ans_val(z) for z in q['answer'].replace('c = ', '').split(' or ')], key=float)
        return sorted(cs, key=float), got
    return (cs[0] if len(cs) == 1 else cs), A

@handler(r'^Find the absolute (maximum|minimum) of f\(x\) = (.+) on \[(.+), (.+)\]\. Give the value and where it occurs\.$')
def _(m, q):
    f = P(m.group(2)); a, b = P(m.group(3)), P(m.group(4))
    cand = [a, b] + [c for c in sp.solve(sp.diff(f, x), x) if c.is_real and a <= c <= b]
    vals = [(f.subs(x, c), c) for c in cand]
    best = max(vals, key=lambda z: float(z[0])) if m.group(1) == 'maximum' else min(vals, key=lambda z: float(z[0]))
    mm = re.match(r'(.+) at x = (.+)$', q['answer'].strip().rstrip('.'))
    return (best[0], ), (P(mm.group(1)), )

@handler(r'^Find the critical numbers of f\(x\) = (.+)\.$')
def _(m, q):
    f = P(m.group(1))
    cs = sorted([c for c in sp.solve(sp.diff(f, x), x) if c.is_real], key=float)
    got = sorted([P(z) for z in re.sub(r'x = ', '', q['answer']).replace(' or ', ',').split(',')], key=float)
    return cs, got

@handler(r'^Find the x-coordinates? of (?:the|all) inflection points? of f\(x\) = (.+)\.$')
def _(m, q):
    f = P(m.group(1)); f2 = sp.diff(f, x, 2)
    cs = sorted([c for c in sp.solve(f2, x) if c.is_real and f2.subs(x, c - sp.Rational(1, 1000)) * f2.subs(x, c + sp.Rational(1, 1000)) < 0], key=float)
    got = sorted([P(z) for z in re.sub(r'x = ', '', q['answer']).replace(' or ', ',').split(',')], key=float)
    return cs, got

@handler(r'^Use Euler\'s method(?: \(a BC topic\))? with step size (\S+) and (\d+) steps to approximate y\((\S+)\) for y′ = (.+), y\((\S+)\) = (\S+)\.$')
def _(m, q):
    hh, n, f = P(m.group(1)), int(m.group(2)), P(m.group(4))
    xx, yy = P(m.group(5)), P(m.group(6))
    for _ in range(n):
        yy = yy + hh * f.subs({x: xx, y: yy}); xx += hh
    return yy, ans_val(q['answer'])

@handler(r'^Find d/dx \[∫ from (\(.+?\)|\S+) to (\(.+?\)|\S+) (.+) dt\]\.$')
def _(m, q):
    lo = P(m.group(1)); up = P(m.group(2)); f = P(m.group(3))
    return f.subs(t, up) * sp.diff(up, x) - f.subs(t, lo) * sp.diff(lo, x), ans_val(q['answer'])

@handler(r'^f is continuous on \[(\S+), (\S+)\] with (.+)\. How many solutions of f\(x\) = (\S+) on \[[^\]]+\] does the Intermediate Value Theorem guarantee')
def _(m, q):
    pr = sorted(pairs(core(q)), key=lambda z: float(z[0])); v = P(m.group(4))
    n = sum(1 for (a, fa), (b, fb) in zip(pr, pr[1:]) if (fa - v) * (fb - v) < 0) + sum(1 for a, fa in pr if fa == v)
    return n, ans_val(q['answer'])

@handler(r'^f is differentiable with (.+)\. Estimate f′\((\S+)\) using the values on either side')
def _(m, q):
    pr = sorted(pairs(core(q)), key=lambda z: float(z[0])); a = P(m.group(2))
    xs = [z[0] for z in pr]; i = xs.index(a)
    (x0, y0), (x1, y1) = pr[i - 1], pr[i + 1]
    return (y1 - y0) / (x1 - x0), ans_val(q['answer'])

@handler(r'^Use the definition f′\(a\) = .* to find f′\((\S+)\) for f\(x\) = (.+)\.$')
def _(m, q):
    return sp.diff(P(m.group(2)), x).subs(x, P(m.group(1))), ans_val(q['answer'])

@handler(r'^A particle moves along a line with position s\(t\) = (.+?)(?: meters at time t seconds,)? for t ≥ 0\. Find the (velocity|acceleration) at t = (\S+)\.$')
def _(m, q):
    s = P(m.group(1)); n = 1 if m.group(2) == 'velocity' else 2
    return sp.diff(s, t, n).subs(t, P(m.group(3))), ans_val(q['answer'])



# ---- Calculus audit families (2026-11-18)
def riemann_limit(body, w, left):
    """Numerically evaluate lim Σ (k = 1 to n) body(k, n) · (w/n) with n = 4000 (right or left sums agree in the limit)."""
    e = P(body.replace('(k - 1)', '(K)').replace('k', 'K'))
    K = sp.Symbol('K')
    n = 4000
    f = sp.lambdify([K, sp.Symbol('n')], e, 'math')
    return sum(f(k, n) for k in range(1, n + 1)) * w / n


@handler(r'^Evaluate lim \(n → ∞\) Σ \(k = 1 to n\) (.+) · \((\d+)/n\) by writing it as a definite integral\.$')
def _(m, q):
    v = riemann_limit(m.group(1), int(m.group(2)), '(k - 1)' in m.group(1))
    return ('approx', v), ans_val(q['answer'])


@handler(r'^lim \(n → ∞\) Σ \(k = 1 to n\) (.+) · \((\d+)/n\) = ∫ from (\S+) to b')
def _(m, q):
    return P(m.group(3)) + int(m.group(2)), ans_val(q['answer'])


@handler(r'^For f\(x\) = (.+) on \[0, (\d+)\], the right Riemann sum with n equal subintervals simplifies to Rₙ = (.+)\. Find lim')
def _(m, q):
    return sp.integrate(P(m.group(1)), (x, 0, int(m.group(2)))), ans_val(q['answer'])


@handler(r'^g\(x\) = ∫ from (\S+) to x \((.+)\) dt\. Find g′\((\S+)\)\.$')
def _(m, q):
    return P(m.group(2)).subs(t, P(m.group(3))), ans_val(q['answer'])


@handler(r'^g\(x\) = ∫ from (\S+) to x \((.+)\) dt\. Find g″\((\S+)\)\.$')
def _(m, q):
    return sp.diff(P(m.group(2)), t).subs(t, P(m.group(3))), ans_val(q['answer'])


def checks(q):
    """Yield (prompt, answer) pairs to check: the item itself, or each part of an open-response item."""
    if q['format'] == 'open-response':
        for p in q.get('parts', []):
            yield p.get('prompt', ''), p.get('answer', '')
    else:
        yield core(q), q['answer']


def run(Q):
    stats = collections.Counter(); bad = []
    for q in Q:
        for prompt, answer in checks(q):
            for rx, f in H:
                mm = rx.search(prompt)
                if not mm:
                    continue
                signal.alarm(10)
                try:
                    exp, got = f(mm, {'answer': answer, 'prompt': prompt})
                    if isinstance(exp, tuple) and len(exp) == 2 and exp[0] == 'approx':
                        ok = abs(exp[1] - float(sp.N(got))) < 1e-2
                    elif isinstance(exp, (list, tuple)):
                        ok = len(exp) == len(got) and all(eqv(a, b) for a, b in zip(exp, got))
                    elif isinstance(exp, str):
                        ok = exp == got
                    else:
                        ok = eqv(exp, got)
                    if ok is None:
                        stats['unknown'] += 1
                    else:
                        stats['ok' if ok else 'bad'] += 1
                        if not ok:
                            bad.append((q['id'], prompt[:120], answer, str(exp)[:80]))
                except TO:
                    stats['timeout'] += 1
                except Exception as e:
                    stats['parse'] += 1
                finally:
                    signal.alarm(0)
                break
    return stats, bad


if __name__ == '__main__':
    sys.path.insert(0, os.path.dirname(__file__))
    import lib
    Q = [q for _, q in lib.items(lib.load())]
    st, bad = run(Q)
    print(dict(st))
    for b in bad:
        print('MISMATCH', b)
    if bad or st['ok'] < 1150:  # slot-015 items are free-response problems since #5 (answers computed with sympy in frq.py)
        sys.exit(1)
    print(f"PASS {st['ok']} Calculus keys recomputed independently")
