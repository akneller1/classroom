"""Calculus audit #3 (2026-11-18): worked solutions that show the work between the method and the answer.

For the computational families (definite integrals and their applications, derivatives by rule, limits at infinity,
L'Hôpital's Rule, limits by factoring, table sums, Riemann sums, FTC with the chain rule, verifying differential
equations, indefinite integrals) the solution is rebuilt from the prompt with sympy: the antiderivative and its values,
each piece of a total distance, the rule and its parts, and so on. Every rebuilt chain is recomputed and must end at the
item's own key, or the item keeps its old steps. A find-the-mistake item keeps its diagnosis and closing line.
Idempotent: the rebuilt steps are generated from the prompt, not from the old steps.
"""
import re, sys, os, signal, math
import sympy as sp
sys.path.insert(0, os.path.dirname(__file__))
import lib
from bankfmt import bt
import verify_keys as V

x, t, y = V.x, V.t, V.y


class TO(Exception):
    pass


def _alarm(*a):
    raise TO()


signal.signal(signal.SIGALRM, _alarm)


def num(v):
    v = sp.nsimplify(sp.simplify(v))
    return bt(v)


def par(v):
    s = num(v)
    return f'({s})' if s.startswith('-') else s


def antideriv_lines(f, var, a, b, name='F'):
    F = sp.integrate(f, var)
    Fa, Fb = sp.simplify(F.subs(var, a)), sp.simplify(F.subs(var, b))
    v = sp.simplify(Fb - Fa)
    return F, v, [f'Antiderivative: {name}({var}) = {bt(F)}.',
                  f'{name}({num(b)}) = {num(Fb)} and {name}({num(a)}) = {num(Fa)}.',
                  f'{name}({num(b)}) − {name}({num(a)}) = {num(Fb)} − {par(Fa)} = {num(v)}.']


# ---------------------------------------------------------------- generators: return (steps, value) or None
G = []


def gen(rx):
    def d(f):
        G.append((re.compile(rx), f))
        return f
    return d


@gen(r'^Evaluate ∫ from (\S+) to (\S+) (.+) dx\.$')
def _(m, q):
    a, b, f = V.P(m.group(1)), V.P(m.group(2)), V.P(m.group(3))
    F, v, lines = antideriv_lines(f, x, a, b)
    keep = [s for s in q['solutionSteps'] if re.search(r'substitution|Let u|u = ', s)][:1]
    return keep + lines, v


@gen(r'^A particle moves with velocity v\(t\) = (.+?) (m/s|ft/s)\. Find its displacement from t = (\S+) to t = (\S+?)\.$')
def _(m, q):
    v_, a, b, u = V.P(m.group(1)), V.P(m.group(3)), V.P(m.group(4)), m.group(2)[:-2]
    F, val, lines = antideriv_lines(v_.subs(t, x).subs(x, t), t, a, b, 's')
    return [f'Displacement = ∫ from {num(a)} to {num(b)} v(t) dt.'] + [l.replace('s(t) =', 'an antiderivative is s(t) =').replace('Antiderivative: ', '') for l in lines[:1]] + lines[1:] + [f'Displacement = {num(val)} {u}.'], val


@gen(r'^A particle moves with velocity v\(t\) = (.+?) (?:m/s|ft/s) and is at s\(0\) = (\S+) (?:m|ft)\. Find its position at t = (\S+?)\.$')
def _(m, q):
    v_, s0, b = V.P(m.group(1)), V.P(m.group(2)), V.P(m.group(3))
    F, d, lines = antideriv_lines(v_, t, 0, b)
    pos = s0 + d
    return [f's({num(b)}) = s(0) + ∫ from 0 to {num(b)} v(t) dt.'] + lines + [f's({num(b)}) = {num(s0)} + {par(d)} = {num(pos)}.'], pos


@gen(r'^A particle moves with velocity v\(t\) = (.+?) (m/s|ft/s)\. Find the total distance traveled from t = (\S+) to t = (\S+?)\.$')
def _(m, q):
    v_, a, b, u = V.P(m.group(1)), V.P(m.group(3)), V.P(m.group(4)), m.group(2)[:-2]
    zs = sorted([z for z in sp.solve(v_, t) if z.is_real and a < z < b])
    F = sp.integrate(v_, t)
    pts = [a] + zs + [b]
    steps = [f'v(t) = 0 at t = {", ".join(num(z) for z in zs)}, so the particle changes direction there.' if zs else 'v(t) does not change sign on the interval.',
             f'Antiderivative: s(t) = {bt(F)}.']
    tot, pieces = 0, []
    for p0, p1 in zip(pts, pts[1:]):
        piece = sp.simplify(F.subs(t, p1) - F.subs(t, p0))
        tot += abs(piece)
        steps.append(f'From t = {num(p0)} to t = {num(p1)}: s({num(p1)}) − s({num(p0)}) = {num(piece)}.')
        pieces.append(num(abs(piece)))
    steps.append(f'Total distance = {" + ".join(pieces)} = {num(tot)} {u}.')
    return steps, tot


@gen(r'^Find the average value of f\(x\) = (.+) on \[(.+), (.+)\]\.$')
def _(m, q):
    f, a, b = V.P(m.group(1)), V.P(m.group(2)), V.P(m.group(3))
    F, v, lines = antideriv_lines(f, x, a, b)
    avg = sp.simplify(v / (b - a))
    return ['f_avg = (1/(b − a))∫ from a to b f(x) dx.'] + lines + [f'f_avg = {num(v)} ÷ {par(b - a)} = {num(avg)}.'], avg


@gen(r'^Find the area of the region bounded by y = (.+) and y = (.+)\.$')
def _(m, q):
    f, g = V.P(m.group(1)), V.P(m.group(2))
    r = sorted([s for s in sp.solve(sp.Eq(f, g), x) if s.is_real])
    if len(r) != 2:
        return None
    a, b = r
    mid = (a + b) / 2
    top, bot, ts, bs = (f, g, m.group(1), m.group(2)) if (f - g).subs(x, mid) > 0 else (g, f, m.group(2), m.group(1))
    diff = sp.expand(top - bot)
    F, v, lines = antideriv_lines(diff, x, a, b)
    return [f'The curves meet where {m.group(1)} = {m.group(2)}: x = {num(a)} and x = {num(b)}.',
            f'At x = {num(mid)} (between them), y = {ts} is on top.', f'Area = ∫ from {num(a)} to {num(b)} [({ts}) − ({bs})] dx = ∫ from {num(a)} to {num(b)} ({bt(diff)}) dx.'] + lines + [f'Area = {num(v)}.'], v


@gen(r'^The region under y = (.+) from x = 0 to x = (\S+) is revolved about the x-axis\. Find the volume\.$')
def _(m, q):
    f, b = V.P(m.group(1)), V.P(m.group(2))
    sq = sp.expand(f ** 2)
    F, v, lines = antideriv_lines(sq, x, 0, b)
    return [f'Disk method: V = π∫ from 0 to {num(b)} [f(x)]² dx = π∫ from 0 to {num(b)} ({bt(sq)}) dx.'] + lines + [f'V = π · {par(v)} = {num(sp.pi * v)}.'], sp.pi * v


@gen(r'^The region between y = (.+) and y = (.+) \(from x = (\S+) to x = (\S+)\) is revolved about the x-axis\. Find the volume\.$')
def _(m, q):
    f, g, a, b = V.P(m.group(1)), V.P(m.group(2)), V.P(m.group(3)), V.P(m.group(4))
    mid = (a + b) / 2
    R, r = (f, g) if f.subs(x, mid) > g.subs(x, mid) else (g, f)
    integrand = sp.expand(R ** 2 - r ** 2)
    F, v, lines = antideriv_lines(integrand, x, a, b)
    return [f'Washer method: outer radius R = {bt(R)}, inner radius r = {bt(r)}.', f'V = π∫ from {num(a)} to {num(b)} (R² − r²) dx = π∫ from {num(a)} to {num(b)} ({bt(integrand)}) dx.'] + lines + [f'V = π · {par(v)} = {num(sp.pi * v)}.'], sp.pi * v


def accumulate(start, rate, a, b, var, unit):
    F, v, lines = antideriv_lines(rate, var, a, b, 'A')
    return lines, v


@gen(r'^(?:A tank holds|A reservoir holds) (\d+) (thousand gallons|L) at t = 0\. Water (?:flows in|enters) at (?:r|E)\(t\) = (.+?) (?:thousand gallons per day|L/min)(?: and leaves at a constant (\d+) L/min)?\. How much (?:water )?is in the (?:tank|reservoir) at t = (\d+) (?:days|minutes)\?$')
def _(m, q):
    start, unit, rate, out, b = int(m.group(1)), m.group(2), V.P(m.group(3)), m.group(4), V.P(m.group(5))
    net = rate - (int(out) if out else 0)
    F, v, lines = antideriv_lines(sp.expand(net), t, 0, b, 'A')
    total = start + v
    return [f'Amount at t = {num(b)} = {start} + ∫ from 0 to {num(b)} ({"rate in − rate out" if out else "rate in"}) dt = {start} + ∫ from 0 to {num(b)} ({bt(sp.expand(net))}) dt.'] + lines + [f'Amount = {start} + {par(v)} = {num(total)} {unit}.'], total


@gen(r'^(?:Oil leaks from a tank at r\(t\) = (.+?) liters per hour\. How many liters leak during the first (\d+) hours\?|Rain falls at R\(t\) = (.+?) inches per hour\. How much rain falls in the first (\d+) hours\?|Cars pass a sensor at a rate of C\(t\) = (.+?) cars per hour\. How many cars pass in the first (\d+) hours?\?(?: Round[^.]*\.)?)$')
def _(m, q):
    g = [x_ for x_ in m.groups() if x_ is not None]
    rate, b = V.P(g[0]), V.P(g[1])
    F, v, lines = antideriv_lines(rate, t, 0, b)
    tail = [f'{num(v)} = {q["answer"]}.'] if '.' in q['answer'] or 'Round' in q['prompt'] else [f'Total = {q["answer"]}.']
    if 'Round' in q['prompt']:
        tail = [f'{num(v)} ≈ {float(v):.2f}, so about {q["answer"]}.']
        return [f'Total = ∫ from 0 to {num(b)} (rate) dt = ∫ from 0 to {num(b)} ({g[0]}) dt.'] + lines + tail, ('word', q['answer'].strip().rstrip('.')) if abs(float(v) - float(re.sub(r'[^\d.-]', '', q['answer']))) <= 0.5 else None
    return [f'Total = ∫ from 0 to {num(b)} (rate) dt = ∫ from 0 to {num(b)} ({g[0]}) dt.'] + lines + tail, v


# derivatives by rule ----------------------------------------------------------
def deriv_lines(f):
    args = sp.Mul.make_args(f)
    xs = [a for a in args if a.has(x)]
    num_, den = sp.fraction(sp.together(f)) if f.is_Mul or f.is_Pow else (f, 1)
    d = sp.diff(f, x)
    if den != 1 and den.has(x) and num_.has(x) and not f.is_Add:
        u, v = num_, den
        return [f'Quotient rule with u = {bt(u)} and v = {bt(v)}: u′ = {bt(sp.diff(u, x))}, v′ = {bt(sp.diff(v, x))}.',
                'f′(x) = (u′v − uv′) ÷ v².'], d
    if f.is_Mul and len(xs) >= 2:
        c = sp.Mul(*[a for a in args if not a.has(x)])
        u, v = xs[0], sp.Mul(*xs[1:])
        cpre = '' if c == 1 else f'{bt(c)} times '
        return [f'Product rule ({cpre}u·v) with u = {bt(u)} and v = {bt(v)}: u′ = {bt(sp.diff(u, x))}, v′ = {bt(sp.diff(v, x))}.',
                'f′(x) = u′v + uv′.'], d
    core = f
    if f.is_Mul and len(xs) == 1:
        core = xs[0]
    inner = None
    if core.is_Pow and core.base.has(x) and not core.base.is_Symbol:
        inner = core.base
    elif core.is_Function and core.args[0].has(x) and not core.args[0].is_Symbol:
        inner = core.args[0]
    elif core.is_Pow and core.base is sp.E and not core.exp.is_Symbol:
        inner = core.exp
    if inner is not None:
        return [f'Chain rule: the inside is u = {bt(inner)}, with u′ = {bt(sp.diff(inner, x))}.',
                'Differentiate the outside, keep the inside, then multiply by u′.'], d
    if f.is_Add:
        terms = f.as_ordered_terms()
        return ['Differentiate term by term: ' + '; '.join(f'd/dx[{bt(tm)}] = {bt(sp.diff(tm, x))}' for tm in terms) + '.'], d
    return [f'd/dx[{bt(f)}] = {bt(d)}.'], d


@gen(r'^Find f′\(x\) for f\(x\) = (.+)\.$')
def _(m, q):
    f = V.P(m.group(1))
    lines, d = deriv_lines(f)
    return lines + [f'f′(x) = {q["answer"].replace("f′(x) = ", "")}.'], d


@gen(r'^Find f′\((-?[\d/]+)\) for f\(x\) = (.+)\.$')
def _(m, q):
    c, f = V.P(m.group(1)), V.P(m.group(2))
    lines, d = deriv_lines(f)
    val = sp.simplify(d.subs(x, c))
    return lines + [f'f′(x) = {bt(sp.simplify(d))}.', f'f′({num(c)}) = {num(val)}.'], val


# limits -------------------------------------------------------------------------
@gen(r'^Evaluate lim \(x → ∞\) (.+)\.$')
def _(m, q):
    e = V.P(m.group(1))
    n_, d_ = sp.fraction(sp.together(e))
    pn, pd = sp.degree(n_, x), sp.degree(d_, x)
    ln, ld = sp.LC(sp.Poly(n_, x)), sp.LC(sp.Poly(d_, x))
    L = sp.limit(e, x, sp.oo)
    if pn == pd:
        why = f'Both have degree {pn}, so the limit is the ratio of leading coefficients: {par(ln)} ÷ {par(ld)} = {num(L)}.'
    elif pn < pd:
        why = f'The numerator has lower degree ({pn} < {pd}); dividing by x^{pd} sends every term on top to 0, so the limit is 0.'
    else:
        why = f'The numerator has higher degree ({pn} > {pd}); the quotient behaves like ({bt(ln)}/{bt(ld)})x^{pn - pd}, so it goes to {"∞" if L == sp.oo else "-∞"}.'
    return [f'Leading terms: {bt(ln * x ** pn)} on top, {bt(ld * x ** pd)} on the bottom.', why], (L if L.is_finite else None)


@gen(r'^Evaluate lim \(x → (-?[\d/]+)\) \((.+)\)/\((.+)\)\.$')
def _(m, q):
    a, n_, d_ = V.P(m.group(1)), V.P(m.group(2)), V.P(m.group(3))
    if not (n_.subs(x, a) == 0 and d_.subs(x, a) == 0):
        return None
    fn, fd = sp.factor(n_), sp.factor(d_)
    red = sp.cancel(n_ / d_)
    L = red.subs(x, a)
    return [f'Direct substitution gives 0/0, an indeterminate form.', f'Factor: ({bt(n_)}) = {bt(fn)} and ({bt(d_)}) = {bt(fd)}.',
            f'Cancel the common factor: the expression equals {bt(red)} for x ≠ {num(a)}.', f'Substitute x = {num(a)}: {num(L)}.'], L


@gen(r"^Use L'Hôpital's Rule to evaluate lim \(x → (\S+)\) (.+)\.$")
def _(m, q):
    a = sp.oo if m.group(1) == '∞' else V.P(m.group(1))
    e = V.P(m.group(2))
    n_, d_ = sp.fraction(sp.together(e))
    steps = []
    for k in range(3):
        nv, dv = sp.limit(n_, x, a), sp.limit(d_, x, a)
        form = '0/0' if nv == 0 and dv == 0 else ('∞/∞' if (not nv.is_finite and not dv.is_finite) else None)
        if not form:
            L = sp.limit(n_ / d_, x, a)
            steps.append(f'Now substitute: {num(nv)} ÷ {par(dv)} = {num(L)}.' if dv != 0 else f'The limit is {num(L)}.')
            return steps, L
        n_, d_ = sp.diff(n_, x), sp.diff(d_, x)
        steps.append(f'{"Substitution gives" if k == 0 else "Still"} {form}; differentiate the top and bottom: ({bt(n_)}) ÷ ({bt(d_)}).')
    return None


# FTC with the chain rule ------------------------------------------------------------
@gen(r'^Find d/dx \[∫ from (\(.+?\)|\S+) to (\(.+?\)|\S+) (.+) dt\]\.$')
def _(m, q):
    lo, up, f = V.P(m.group(1)), V.P(m.group(2)), V.P(m.group(3))
    res = f.subs(t, up) * sp.diff(up, x) - f.subs(t, lo) * sp.diff(lo, x)
    steps = [f'FTC with the chain rule: d/dx ∫ from a to u(x) f(t) dt = f(u(x))·u′(x).', f'Here f(t) = {bt(f)}, u(x) = {bt(up)}, u′(x) = {bt(sp.diff(up, x))}.']
    if lo.has(x):
        steps.append(f'The lower limit {bt(lo)} also depends on x, so subtract f({bt(lo)})·{bt(sp.diff(lo, x))}.')
    else:
        steps.append(f'The lower limit {num(lo)} is a constant, so it adds nothing.')
    steps.append(f'Result: {q["answer"]}.')
    return steps, res


# indefinite integrals, term by term ------------------------------------------------
@gen(r'^Find ∫ \((.+)\) dx\.$')
def _(m, q):
    f = V.P(m.group(1))
    if not f.is_Add:
        return None
    terms = f.as_ordered_terms()
    pieces = [f'∫ {bt(tm)} dx = {bt(sp.integrate(tm, x))}' for tm in terms]
    F = sp.integrate(f, x)
    return ['Integrate term by term: ' + '; '.join(pieces) + '.', f'Add the constant of integration: {q["answer"]}.'], F


# tables -------------------------------------------------------------------------------
@gen(r'(?:Use (?:the|a) (trapezoidal rule|left Riemann sum|right Riemann sum)|Use a (trapezoidal) sum) with (?:the subintervals in the table|these four subintervals) to approximate ∫ from (\S+) to (\S+) f\(x\) dx\.')
def _(m, q):
    kind = m.group(1) or m.group(2)
    pr = sorted(V.pairs(V.core(q)), key=lambda z: float(z[0]))
    lines, total = [], 0
    for (x0, y0), (x1, y1) in zip(pr, pr[1:]):
        w = x1 - x0
        if 'trap' in kind:
            piece = w * (y0 + y1) / 2
            lines.append(f'[{num(x0)}, {num(x1)}]: {num(w)} × ({num(y0)} + {par(y1)})/2 = {num(piece)}')
        else:
            h = y0 if 'left' in kind else y1
            piece = w * h
            lines.append(f'[{num(x0)}, {num(x1)}]: {num(w)} × {par(h)} = {num(piece)}')
        total += piece
    lead = 'Each trapezoid: width × average of the two heights.' if 'trap' in kind else f'Each rectangle: width × the {"left" if "left" in kind else "right"} endpoint value.'
    return [lead, '; '.join(lines) + '.', f'Sum = {num(total)}.'], total


# differential equations --------------------------------------------------------------
@gen(r'^Is y = (.+) a solution of (.+)\?$')
def _(m, q):
    yy = V.P(m.group(1))
    lhs, rhs = m.group(2).split(' = ')
    dy = sp.diff(yy, x)
    env = lambda s: V.P(s.replace('y″', '(Y2)').replace('y′', '(Y1)').replace('y', '(Y0)')).subs({sp.Symbol('Y2'): sp.diff(yy, x, 2), sp.Symbol('Y1'): dy, sp.Symbol('Y0'): yy})
    try:
        L, R = sp.simplify(env(lhs)), sp.simplify(env(rhs))
    except Exception:
        return None
    ok = sp.simplify(L - R) == 0
    ans = 'Yes' if ok else 'No'
    if q['answer'].strip().rstrip('.') not in ('Yes', 'No'):
        return None
    return [f'y = {bt(yy)}, so y′ = {bt(dy)}.', f'Left side {lhs}: {bt(L)}. Right side {rhs}: {bt(R)}.',
            f'{"The sides match for every x" if ok else "The sides do not match"}, so the answer is {ans}.'], ('word', ans)



# properties of definite integrals ---------------------------------------------------------
@gen(r'^Given ∫ from (\S+) to (\S+) f\(x\) dx = (\S+), ∫ from (\S+) to (\S+) f\(x\) dx = (\S+), and ∫ from (\S+) to (\S+) g\(x\) dx = (\S+), find ∫ from (\S+) to (\S+) (.+) dx\.$')
def _(m, q):
    a, b, F1, b2, c, F2, ga, gb, G1, lo, hi, expr = m.groups()
    F1, F2, G1 = V.P(F1), V.P(F2), V.P(G1)
    known = {(a, b): ('f', F1), (b2, c): ('f', F2), (ga, gb): ('g', G1)}
    steps, total = [], None
    e = expr.strip()
    if e.startswith('(') and e.endswith(')'):
        e = e[1:-1]
    if e == 'f(x)':
        if (lo, hi) in known and known[(lo, hi)][0] == 'f':
            return None
        if (hi, lo) in known:
            v = -known[(hi, lo)][1]
            return [f'Reversing the limits changes the sign: ∫ from {lo} to {hi} f(x) dx = −∫ from {hi} to {lo} f(x) dx.', f'= −({num(known[(hi, lo)][1])}) = {num(v)}.'], v
        if lo == a and hi == c and b == b2:
            v = F1 + F2
            return [f'Adjacent intervals add: ∫ from {a} to {c} = ∫ from {a} to {b} + ∫ from {b} to {c}.', f'= {num(F1)} + {par(F2)} = {num(v)}.'], v
        return None
    mm = re.match(r'^(-?\d*)f\(x\) ([+-]) (\d*)(g\(x\)|)$', e)
    if mm and (lo, hi) == (a, b) and (ga, gb) == (a, b):
        cf = int(mm.group(1)) if mm.group(1) not in ('', '-') else (-1 if mm.group(1) == '-' else 1)
        sign = 1 if mm.group(2) == '+' else -1
        if mm.group(4):
            cg = sign * (int(mm.group(3)) if mm.group(3) else 1)
            v = cf * F1 + cg * G1
            return [f'Linearity: ∫ ({e}) dx = {cf}∫ f(x) dx {"+" if cg > 0 else "−"} {abs(cg)}∫ g(x) dx.', f'= {cf}({num(F1)}) {"+" if cg > 0 else "−"} {abs(cg)}({num(G1)}) = {num(v)}.'], v
        k = sign * int(mm.group(3))
        w = V.P(b) - V.P(a)
        v = cf * F1 + k * w
        return [f'Split the integral: ∫ ({e}) dx = {"" if cf == 1 else cf}∫ f(x) dx {"+" if k > 0 else "−"} ∫ {abs(k)} dx.', f'∫ from {a} to {b} {abs(k)} dx = {abs(k)} × ({b} − {par(V.P(a))}) = {num(abs(k) * w)}.', f'= {num(cf * F1)} {"+" if k > 0 else "−"} {num(abs(k) * w)} = {num(v)}.'], v
    mm = re.match(r'^(-?\d+)f\(x\)$', e)
    if mm and lo == a and hi == c and b == b2:
        k = int(mm.group(1)); v = k * (F1 + F2)
        return [f'∫ from {a} to {c} f(x) dx = {num(F1)} + {par(F2)} = {num(F1 + F2)}.', f'Multiply by {k}: {k} × {par(F1 + F2)} = {num(v)}.'], v
    return None


# graphs made of line segments: the alt text lists the points --------------------------------
def seg_points(q):
    alt = ((q.get('diagram') or {}).get('spec') or {}).get('alt', '')
    pts = [(V.P(a), V.P(b)) for a, b in re.findall(r'\((-?[\d./]+), (-?[\d./]+)\)', alt)]
    return sorted(pts, key=lambda z: float(z[0]))


@gen(r'^The graph of f consists of line segments through the marked points\. Evaluate ∫ from (\S+) to (\S+) f\(x\) dx\.$')
def _(m, q):
    a, b = V.P(m.group(1)), V.P(m.group(2))
    pts = seg_points(q)
    if len(pts) < 2:
        return None
    parts, total = [], 0
    for (x0, y0), (x1, y1) in zip(pts, pts[1:]):
        lo, hi = max(x0, a), min(x1, b)
        if lo >= hi:
            continue
        f = lambda z: y0 + (y1 - y0) * (z - x0) / (x1 - x0)
        fl, fh = f(lo), f(hi)
        if fl * fh < 0:   # crosses the axis: split into two triangles
            z = lo - fl * (hi - lo) / (fh - fl)
            p1, p2 = (z - lo) * fl / 2, (hi - z) * fh / 2
            parts.append(f'[{num(lo)}, {num(hi)}]: crosses at x = {num(z)}, triangles {num(p1)} and {num(p2)}')
            total += p1 + p2
        else:
            p = (hi - lo) * (fl + fh) / 2
            parts.append(f'[{num(lo)}, {num(hi)}]: width {num(hi - lo)}, heights {num(fl)} and {num(fh)}, signed area {num(p)}')
            total += p
    return ['Split the region at the marked points; area below the x-axis counts as negative.', '; '.join(parts) + '.', f'Total = {num(total)}.'], total


# second derivatives ----------------------------------------------------------------------
@gen(r'^Find f″\(x\) for f\(x\) = (.+)\.$')
def _(m, q):
    f = V.P(m.group(1))
    d1, d2 = sp.diff(f, x), sp.diff(f, x, 2)
    return [f'f′(x) = {bt(sp.simplify(d1))}.', f'Differentiate again: f″(x) = {q["answer"]}.'], d2


# slope of a solution curve ----------------------------------------------------------------
@gen(r'^For y′ = (.+), find the slope of the solution curve through \((\S+), (\S+)\)\.$')
def _(m, q):
    rhs, x0, y0 = m.group(1), V.P(m.group(2)), V.P(m.group(3))
    e = V.P(rhs)
    v = e.subs({x: x0, y: y0})
    sub = re.sub(r'\by\b', f'({num(y0)})', re.sub(r'\bx\b', f'({num(x0)})', rhs.replace('x²', 'x^2').replace('y²', 'y^2')))
    return [f'The slope of the solution curve at a point is y′ evaluated there.', f'y′ = {sub.replace("^2", "²")} = {num(v)}.'], v


# can L'Hôpital be applied ------------------------------------------------------------------
@gen(r"^Can L'Hôpital's Rule be applied directly to lim \(x → (\S+)\) \((.+)\)/\((.+)\)\?$")
def _(m, q):
    a, n_, d_ = V.P(m.group(1)), V.P(m.group(2)), V.P(m.group(3))
    nv, dv = n_.subs(x, a), d_.subs(x, a)
    ok = nv == 0 and dv == 0
    if (q['answer'].startswith('Yes')) != ok:
        return None
    return [f'Substitute x = {num(a)}: the numerator is {num(nv)} and the denominator is {num(dv)}.',
            'That is 0/0, so the rule applies.' if ok else f'That is not 0/0 or ∞/∞, so the rule does not apply (the limit is just {num(nv)} ÷ {par(dv)}).' if dv != 0 else 'That is not 0/0 or ∞/∞, so the rule does not apply.'], None


# factoring -------------------------------------------------------------------------------------
@gen(r'^Factor completely: (.+)$')
def _(m, q):
    e = V.P(m.group(1).rstrip('.'))
    poly = sp.Poly(e, x)
    cs = poly.all_coeffs()
    g = sp.gcd_list([c for c in cs if c != 0])
    steps = []
    if g != 1 or (len(cs) > 1 and cs[-1] == 0):
        gx = g * x ** min(i for i, c in enumerate(reversed(cs)) if c != 0)
        steps.append(f'Factor out the GCF {bt(gx)}: {bt(gx)}({bt(sp.expand(e / gx))}).')
    rest = sp.factor(e)
    if poly.degree() == 2 and cs[0] == 1 and len(steps) == 0:
        r = [-z for z in sp.solve(e, x)]
        if all(z.is_integer for z in r):
            steps.append(f'Find two numbers with product {num(cs[2])} and sum {num(cs[1])}: {num(r[0])} and {num(r[1])}.')
    if poly.degree() == 3 and len(cs) == 4 and cs[0] != 0 and cs[1] != 0 and not steps:
        steps.append(f'Group: ({bt(cs[0] * x ** 3 + cs[1] * x ** 2)}) + ({bt(cs[2] * x + cs[3])}) and factor each group.')
    if poly.degree() == 3 and cs[1] == 0 and cs[2] == 0:
        steps.append('Use the sum or difference of cubes: a³ ± b³ = (a ± b)(a² ∓ ab + b²).')
    if not steps:
        steps.append('Look for a GCF, then a pattern (trinomial, difference of squares, sum or difference of cubes, grouping).')
    steps.append(f'{m.group(1).rstrip(".")} = {q["answer"]}.')
    steps.append(f'Check by multiplying out: {bt(sp.expand(rest))}.')
    return steps, rest


# central-difference estimates from a table -------------------------------------------------
@gen(r'^A differentiable function has (.+)\. Estimate f′\((\S+)\) using the nearest values on either side\.$')
def _(m, q):
    pr = sorted(V.pairs(V.core(q)), key=lambda z: float(z[0])); c = V.P(m.group(2))
    xs = [z[0] for z in pr]; i = xs.index(c)
    (x0, y0), (x1, y1) = pr[i - 1], pr[i + 1]
    v = (y1 - y0) / (x1 - x0)
    return [f'Use the values on either side of x = {num(c)}: x = {num(x0)} and x = {num(x1)}.', f'f′({num(c)}) ≈ (f({num(x1)}) − f({num(x0)})) ÷ ({num(x1)} − {par(x0)}) = ({num(y1)} − {par(y0)}) ÷ {num(x1 - x0)} = {num(v)}.'], v



# volumes with known cross sections -----------------------------------------------------------
@gen(r'^A solid has base bounded by y = (.+), the x-axis, and x = (\S+) to x = (\S+)\. Cross sections perpendicular to the x-axis are (squares|semicircles) with a (?:side|diameter) in the base\. Find the volume\.$')
def _(m, q):
    f, a, b, kind = V.P(m.group(1)), V.P(m.group(2)), V.P(m.group(3)), m.group(4)
    A = sp.expand(f ** 2) if kind == 'squares' else sp.expand(sp.pi * f ** 2 / 8)
    area_txt = f's² = ({m.group(1)})²' if kind == 'squares' else f'(1/2)π(s/2)² = (π/8)s² with s = {m.group(1)}'
    inner = sp.expand(f ** 2)
    F, v, lines = antideriv_lines(inner, x, a, b)
    vol = v if kind == 'squares' else sp.pi * v / 8
    return [f'Each cross section has side (or diameter) s = {m.group(1)}, so its area is A(x) = {area_txt}.',
            f'V = ∫ from {num(a)} to {num(b)} A(x) dx = {"" if kind == "squares" else "(π/8)"}∫ from {num(a)} to {num(b)} {bt(inner) if inner.is_Symbol else "(" + bt(inner) + ")"} dx.'] + lines + [f'V = {num(vol)}.'], vol


# growth from a rate -------------------------------------------------------------------------------
@gen(r'^A culture starts with (\d+) bacteria and grows at N′\(t\) = \((\d+)/(\d+)\)e\^\(([\d.]+)t\) bacteria per hour\. How many are present at t = (\d+)\? Round to the nearest whole number\.$')
def _(m, q):
    n0, a, b, k, T = int(m.group(1)), int(m.group(2)), int(m.group(3)), m.group(4), int(m.group(5))
    c = sp.Rational(a, b); kk = sp.Rational(k)
    A = c / kk
    grow = float(A) * (math.exp(float(kk) * T) - 1)
    tot = n0 + grow
    if abs(round(tot) - float(V.ans_val(q['answer']))) > 0.5:
        return None
    kt = f'{k}t'
    return [f'N({T}) = N(0) + ∫ from 0 to {T} N′(t) dt.',
            f'An antiderivative of ({a}/{b})e^({kt}) is ({a}/{b}) ÷ {k} · e^({kt}) = {num(A)}e^({kt}).',
            f'∫ from 0 to {T} N′(t) dt = {num(A)}(e^({float(kk) * T:g}) − 1) ≈ {grow:.2f}.',
            f'N({T}) ≈ {n0} + {grow:.2f} = {tot:.2f}, which rounds to {round(tot)}.'], ('word', q['answer'].strip().rstrip('.'))


# ---------------------------------------------------------------- apply
def rebuild(q):
    p = V.core(q)
    for rx, f in G:
        m = rx.search(p)
        if not m:
            continue
        signal.alarm(10)
        try:
            out = f(m, q)
        except (TO, Exception):
            out = None
        finally:
            signal.alarm(0)
        if not out:
            return None
        steps, val = out
        if isinstance(val, tuple) and val[0] == 'word':
            if val[1] != q['answer'].strip().rstrip('.'):
                return None
        elif val is not None:
            try:
                ok = V.eqv(sp.nsimplify(val) if val.is_number else val, V.ans_val(q['answer']))
            except Exception:
                ok = False
            if not ok:
                return None
        return steps
    return None


EXPLAIN = [
    (r'Which theorem gives lim', ['The function g is trapped between two functions that have the same limit.', 'Both -|x| and |x| approach 0 as x → 0, so g must approach 0 too: the Squeeze Theorem.']),
    (r'Which theorem guarantees a zero', ['f is continuous on the closed interval, and 0 lies between the endpoint values (one negative, one positive).', 'So the Intermediate Value Theorem guarantees a zero in the open interval.']),
    (r'Why does the Extreme Value Theorem not apply', ['The EVT needs f continuous on the closed interval.', 'f has a vertical asymptote where its denominator is 0, and that x-value lies inside the interval, so f is not continuous there.']),
    (r'Which theorem guarantees f has an absolute maximum and minimum', ['f is continuous on a closed interval.', 'The Extreme Value Theorem guarantees an absolute maximum and minimum there.']),
    (r'A left Riemann sum is used to approximate', ['For an increasing f, each left endpoint is the lowest value on its subinterval, so a left sum underestimates.', 'For a decreasing f, each left endpoint is the highest value on its subinterval, so a left sum overestimates.']),
    (r'what does ∫₀', ['∫ of a rate over a time interval adds up rate × time.', 'So it gives the total change in the quantity over that interval, in the quantity\'s units.']),
    (r'instantaneous rate of change of f at x = a', ['The instantaneous rate of change is the limit of average rates over shorter and shorter intervals.', 'That is the derivative: lim (h → 0) (f(a + h) - f(a))/h.']),
    (r'average value of f on', ['Average value = (1/(b − a)) times the integral of f over [a, b].']),
    (r'total distance traveled from t = \S+ to t = \S+ with velocity', ['Distance counts motion in both directions as positive.', 'So integrate the speed |v(t)|, not v(t).']),
    (r'average rate of change of f on', ['The average rate of change is the slope between the endpoints: (f(b) − f(a))/(b − a).']),
    (r'second derivative of y with respect to x', ['The second derivative is the derivative of y′.', 'It is written y″ or d²y/dx².']),
]


def explain(q):
    if len(q['solutionSteps']) >= 2 or q['format'] == 'open-response':
        return False
    for rx, lines in EXPLAIN:
        if re.search(rx, q['prompt']):
            q['solutionSteps'] = lines + q['solutionSteps']
            return True
    return False


def main():
    banks = lib.load()
    for u, d in banks.items():
        for q in d['questions']:
            explain(q)
    n = 0
    for u, d in banks.items():
        for q in d['questions']:
            if q['format'] == 'open-response':
                continue
            new = rebuild(q)
            if not new:
                continue
            if 'answered this problem incorrectly' in q['prompt']:
                mistake = [s for s in q['solutionSteps'] if s.startswith('Mistake:')]
                new = mistake + new + [q['solutionSteps'][-1]]
            if new != q['solutionSteps']:
                q['solutionSteps'] = new
                n += 1
    lib.save(banks)
    print('rebuilt', n)


if __name__ == '__main__':
    main()
