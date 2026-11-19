"""Calculus audit #10 (2026-11-18): AP Calculus AB topics the bank did not practice.

Items in existing skills are replaced (same ids, so every activity keeps working):
- Tangent Lines and Their Slopes (derivatives 06), slots 003/007/011: local linear approximation (CHA-3.F).
- Implicit Differentiation (derivatives 09), slots 003/007/012: second derivatives of implicit relations at a point.
- Approximating Definite Integrals (antiderivatives 05), slots 003/011: calculator-active integrals.
- Motion and Displacement (applications of integrals 04), slots 003/007/010/011: motion read from a velocity graph
  (the graphs are drawn into question-banks/assets/calculus/applications-integrals/).
- Volumes of Solids (applications of integrals 07), slots 003/007/011: washers about a horizontal line other than the axis.
- Initial Conditions and Particular Solutions (differential equations 06), slots 004/007/012: exponential growth and
  decay models dy/dt = ky (FUN-7.G).
Calculator-active items are tagged "calculator-active" in the unit's meta tags file.
Deterministic and idempotent.
"""
import json, math, os, random, re, sys
from fractions import Fraction as Fr
import sympy as sp
sys.path.insert(0, os.path.dirname(__file__))
import lib
from bankfmt import bt
from author import mc, record

x, t = sp.symbols('x t')
ROOT = lib.ROOT
ASSETS = os.path.join(ROOT, 'question-banks', 'assets', 'calculus', 'applications-integrals')


def num(v):
    return bt(sp.nsimplify(v))


def dec(v, places):
    return f'{float(v):.{places}f}'


# ---------------------------------------------------------------- local linearization
def linear(q, rng):
    lv = q['level']
    if lv == 'cp2':
        a, fa, fpa = rng.choice([2, 3, 4, 5]), rng.randint(-6, 9), rng.choice([-4, -3, -2, 2, 3, 5])
        h = rng.choice([Fr(1, 10), Fr(2, 10), Fr(-1, 10)])
        approx = fa + fpa * h
        p = f'f({a}) = {fa} and f′({a}) = {fpa}. Use the tangent line at x = {a} to approximate f({float(a + h):g}).'
        ans = f'{float(approx):g}'
        pf = f'({fpa})' if fpa < 0 else str(fpa)
        steps = [f'Tangent line: L(x) = f({a}) + f′({a})(x − {a}) = {fa} + {pf}(x − {a}).', f'L({float(a + h):g}) = {fa} + {pf}({float(h):g}) = {ans}.']
        dis = [f'{float(fa + fpa * h * 10):g}', f'{float(fa - fpa * h):g}', f'{float(fpa + fa * h):g}', f'{float(approx + 1):g}']
    elif lv == 'cp1':
        a, xv = rng.choice([(9, Fr(93, 10)), (16, Fr(164, 10)), (4, Fr(42, 10)), (25, Fr(255, 10))])
        r = int(math.isqrt(a))
        approx = r + (xv - a) / (2 * r)
        p = f'Use the tangent line to f(x) = √x at x = {a} to approximate √{float(xv):g}. Give your answer as a decimal.'
        ans = f'{float(approx):g}'
        steps = [f'f({a}) = {r} and f′(x) = 1/(2√x), so f′({a}) = 1/{2 * r}.', f'L(x) = {r} + (1/{2 * r})(x − {a}).',
                 f'L({float(xv):g}) = {r} + ({float(xv - a):g})/{2 * r} = {ans}.', f'(The true value is √{float(xv):g} ≈ {math.sqrt(xv):.4f}; the tangent line lies above the concave-down graph, so this is an overestimate.)']
        dis = [f'{float(r + (xv - a) / r):g}', f'{float(r + (xv - a) * 2 * r):g}', f'{float(r - (xv - a) / (2 * r)):g}', f'{float(r + (xv - a)):g}']
    else:
        f, a, xv, fa, fpa, conc = rng.choice([('ln(x)', 1, '1.2', 0, 1, 'down'), ('e^x', 0, '0.1', 1, 1, 'up'), ('√x', 4, '4.4', 2, Fr(1, 4), 'down'), ('1/x', 1, '0.9', 1, -1, 'up'), ('sin(x)', 0, '0.2', 0, 1, 'down')])
        xd = Fr(xv)
        approx = fa + fpa * (xd - a)
        val = f'{float(approx):g}'
        word = 'an overestimate' if conc == 'down' else 'an underestimate'
        other = 'an underestimate' if conc == 'down' else 'an overestimate'
        p = f'Use the tangent line to f(x) = {f} at x = {a} to approximate f({xv}). Is the approximation an overestimate or an underestimate?'
        ans = f'{val}, {word}'
        steps = [f'f({a}) = {fa} and f′({a}) = {num(fpa)}, so L(x) = {fa} + {num(fpa)}(x − {a}).', f'L({xv}) = {val}.',
                 f'f″ is {"negative" if conc == "down" else "positive"} near x = {a}, so the graph is concave {conc} and the tangent line lies {"above" if conc == "down" else "below"} it: {word}.']
        dis = [f'{val}, {other}', f'{float(approx + Fr(1, 10)):g}, {word}', f'{float(approx - Fr(1, 10)):g}, {other}']
        return record(q, 'lin_approx', p, ans, steps, fmt='multiple-choice', options=mc(rng, ans, dis), standards=['AP CHA-3.F'])
    if q['format'] == 'multiple-choice':
        return record(q, 'lin_approx', p, ans, steps, fmt='multiple-choice', options=mc(rng, ans, [d for d in dis if d != ans]), standards=['AP CHA-3.F'])
    return record(q, 'lin_approx', p, ans, steps, standards=['AP CHA-3.F'])


# ---------------------------------------------------------------- implicit second derivatives
def implicit2(q, rng):
    a, b, (px, py) = rng.choice([(1, 1, (3, 4)), (1, 1, (6, 8)), (1, 1, (-5, 12)), (4, 1, (1, 4)), (1, 4, (4, 1)), (9, 1, (1, 3)), (1, 1, (8, -6))])
    if rng.random() < 0.5:  # more curves, so no two levels share an item
        a, b, (px, py) = rng.choice([1, 2, 4, 9]), rng.choice([1, 2, 4]), (rng.choice([-3, -2, -1, 1, 2, 3]), rng.choice([-3, -2, -1, 1, 2, 3, 4]))
    c = a * px * px + b * py * py
    lhs = ('' if a == 1 else str(a)) + 'x² + ' + ('' if b == 1 else str(b)) + 'y²'
    y1 = Fr(-a * px, b * py)
    y2 = Fr(-a * c, b * b * py ** 3)
    p = f'For {lhs} = {c}, find d²y/dx² at the point ({px}, {py}).'
    ans = num(sp.Rational(y2.numerator, y2.denominator))
    ca, cb = ('' if a == 1 else str(a)), ('' if b == 1 else str(b))
    yp = f'-{ca}x/{cb}y' if b == 1 else f'-{ca}x/({cb}y)'
    steps = [f'Differentiate: {2 * a}x + {2 * b}y·y′ = 0, so y′ = {yp}.',
             f'At ({px}, {py}): y′ = {num(sp.Rational(y1.numerator, y1.denominator))}.',
             f'Differentiate y′ = {yp} with the quotient rule: y″ = -{ca}(y − x·y′)/({cb}y²).',
             f'At ({px}, {py}): y″ = -{ca}({py} − ({px})({num(sp.Rational(y1.numerator, y1.denominator))}))/({cb + "·" if cb else ""}{py * py}) = {ans}.']
    dis = [num(sp.Rational(y1.numerator, y1.denominator)), num(sp.Rational(-y2.numerator, y2.denominator)), num(sp.Rational(y2.numerator * 2, y2.denominator)), num(sp.Rational(-a, b * py))]
    if q['format'] == 'multiple-choice':
        return record(q, 'im_second', p, ans, steps, fmt='multiple-choice', options=mc(rng, ans, [d for d in dis if d != ans] + ['0', '1']), standards=['AP FUN-3.D', 'AP FUN-3.F'])
    return record(q, 'im_second', p, ans, steps, standards=['AP FUN-3.D', 'AP FUN-3.F'])


# ---------------------------------------------------------------- calculator-active integrals
CALC = [('e^(-x²)', 0, 1), ('√(1 + x³)', 0, 2), ('sin(x²)', 0, 1), ('1/(1 + x⁴)', 0, 1), ('cos(√x)', 0, 4), ('ln(1 + x²)', 0, 2), ('√(4 - x²)·cos(x)', 0, 2)]


def calculator(q, rng):
    import verify_keys as V
    f, a, b = rng.choice(CALC)
    val = sp.Integral(V.P(f), (x, a, b)).evalf(15)
    ans = dec(val, 3)
    p = f'Calculator active. Use a calculator to evaluate ∫ from {a} to {b} {f if len(f) < 6 else "(" + f + ")"} dx. Round to three decimal places.'
    steps = [f'{f} has no elementary antiderivative{"" if "e^(-x²/2)" not in f else " in this form"}, so use the calculator’s numerical integration (fnInt or ∫ from the math menu).',
             f'Enter the integrand {f} with lower limit {a} and upper limit {b}.', f'The calculator gives {float(val):.6f}, which rounds to {ans}.']
    return record(q, 'calc_numeric', p, ans, steps, standards=['AP LIM-5.A', 'AP FUN-6.B'])


# ---------------------------------------------------------------- motion from a velocity graph
GRAPHS = {
    'cp2': [[(0, 4), (2, 4), (4, 0), (6, -2), (8, -2)], [(0, 0), (2, 6), (4, 6), (6, 0), (8, -3)], [(0, 6), (3, 0), (5, -4), (7, -4), (8, 0)]],
    'cp1': [[(0, -2), (1, 0), (3, 4), (5, 4), (7, 0), (8, -2)], [(0, 5), (2, 1), (3, 0), (5, -4), (7, 0)], [(0, 3), (2, -1), (4, -1), (5, 0), (7, 4)]],
    'honors': [[(0, 4), (1, 0), (3, -4), (4, -4), (6, 0), (8, 4)], [(0, -3), (2, 3), (3, 3), (6, -3), (7, 0)], [(0, 2), (2, 6), (4, 0), (5, -2), (8, 4)]],
}


def piece_area(p0, p1, lo, hi):
    (x0, y0), (x1, y1) = p0, p1
    lo, hi = max(lo, x0), min(hi, x1)
    if lo >= hi:
        return Fr(0), Fr(0)
    f = lambda z: Fr(y0) + Fr(y1 - y0, x1 - x0) * (z - x0)
    a, b = f(lo), f(hi)
    if a * b < 0:
        z = lo - a * (hi - lo) / (b - a)
        s1, s2 = (z - lo) * a / 2, (hi - z) * b / 2
        return s1 + s2, abs(s1) + abs(s2)
    s = (hi - lo) * (a + b) / 2
    return s, abs(s)


def draw(pts, path, T):
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    fig, ax = plt.subplots(figsize=(4.8, 3.0), dpi=150)
    xs, ys = zip(*pts)
    ax.plot(xs, ys, color='#1f3b73', lw=2.2)
    ax.plot(xs, ys, 'o', color='#1f3b73', ms=4)
    ax.axhline(0, color='black', lw=1)
    ax.axvline(0, color='black', lw=1)
    ax.set_xlim(-0.3, max(xs) + 0.5)
    lo, hi = min(min(ys), 0) - 1, max(max(ys), 0) + 1
    ax.set_ylim(lo, hi)
    ax.set_xticks(list(range(0, int(max(xs)) + 1)))
    ax.set_xticklabels([str(v) for v in range(0, int(max(xs)) + 1)])
    ax.set_yticks(range(int(lo) + (0 if int(lo) % 1 == 0 else 1), int(hi) + 1))
    ax.grid(True, color='#d8dde6', lw=0.6)
    ax.set_xlabel('t (seconds)')
    ax.set_ylabel('v(t) (m/s)')
    fig.tight_layout()
    os.makedirs(os.path.dirname(path), exist_ok=True)
    fig.savefig(path)
    plt.close(fig)


def vgraph(q, rng):
    lv = q['level']
    slot = int(q['id'][-3:])
    pts = GRAPHS[lv][(slot // 4) % 3]
    T = pts[-1][0]
    kind = {3: 'disp', 7: 'dist', 10: 'pos', 11: 'turn'}[slot]
    fn = f"{q['id']}.png"
    src = f'question-banks/assets/calculus/applications-integrals/{fn}'
    draw(pts, os.path.join(ASSETS, fn), T)
    alt = 'Graph of the velocity v(t), in meters per second, made of line segments through ' + ', '.join(f'({a}, {b})' for a, b in pts) + '.'
    diagram = {'type': 'image', 'spec': {'src': src, 'alt': alt}}
    pieces = [piece_area(p0, p1, 0, T) for p0, p1 in zip(pts, pts[1:])]
    signed = sum(p[0] for p in pieces)
    total = sum(p[1] for p in pieces)
    detail = '; '.join(f'[{p0[0]}, {p1[0]}]: {num(sp.Rational(pc[0].numerator, pc[0].denominator))}' for (p0, p1), pc in zip(zip(pts, pts[1:]), pieces))
    std = ['AP CHA-4.C', 'AP CHA-4.A']
    if kind == 'disp':
        p = f'The graph shows the velocity v(t) of a particle moving along a line for 0 ≤ t ≤ {T}. Find the displacement of the particle from t = 0 to t = {T}.'
        ans = f'{num(sp.Rational(signed.numerator, signed.denominator))} m'
        steps = ['Displacement = ∫ v(t) dt = signed area between the graph and the t-axis (below the axis counts as negative).', f'Signed areas: {detail}.', f'Displacement = {ans}.']
        dis = [f'{num(sp.Rational(total.numerator, total.denominator))} m', f'{num(-sp.Rational(signed.numerator, signed.denominator))} m', f'{pts[-1][1]} m', f'{num(sp.Rational(signed.numerator, signed.denominator) + 2)} m']
    elif kind == 'dist':
        p = f'The graph shows the velocity v(t) of a particle moving along a line for 0 ≤ t ≤ {T}. Find the total distance the particle travels from t = 0 to t = {T}.'
        ans = f'{num(sp.Rational(total.numerator, total.denominator))} m'
        steps = ['Total distance = ∫ |v(t)| dt: add the areas above and below the axis as positive amounts.', f'Signed areas: {detail}.', f'Total distance = {ans}.']
        dis = [f'{num(sp.Rational(signed.numerator, signed.denominator))} m']
    elif kind == 'pos':
        s0 = rng.choice([-3, -2, 1, 2, 5])
        pos = s0 + signed
        p = f'The graph shows the velocity v(t) of a particle moving along a line for 0 ≤ t ≤ {T}. The particle is at x = {s0} when t = 0. Where is the particle at t = {T}?'
        ans = f'x = {num(sp.Rational(pos.numerator, pos.denominator))}'
        steps = [f'Position at t = {T} = starting position + ∫ from 0 to {T} v(t) dt.', f'Signed areas: {detail}; total {num(sp.Rational(signed.numerator, signed.denominator))}.', f'x = {s0} + ({num(sp.Rational(signed.numerator, signed.denominator))}) = {num(sp.Rational(pos.numerator, pos.denominator))}.']
        dis = [f'x = {num(sp.Rational(signed.numerator, signed.denominator))}', f'x = {num(sp.Rational((s0 + total).numerator, (s0 + total).denominator))}', f'x = {num(sp.Rational((s0 - signed).numerator, (s0 - signed).denominator))}', f'x = {s0 + pts[-1][1]}']
    else:
        turns = []
        for (x0, y0), (x1, y1) in zip(pts, pts[1:]):
            if y0 * y1 < 0:
                turns.append(Fr(x0) - Fr(y0) * (x1 - x0) / (y1 - y0))
        # a zero at a vertex where the sign changes
        for i in range(1, len(pts) - 1):
            if pts[i][1] == 0 and pts[i - 1][1] * pts[i + 1][1] < 0:
                turns.append(Fr(pts[i][0]))
        turns = sorted(set(turns))
        if not turns:
            return None
        p = f'The graph shows the velocity v(t) of a particle moving along a line for 0 < t < {T}. At what time(s) does the particle change direction?'
        ans = 't = ' + ' and t = '.join(num(sp.Rational(z.numerator, z.denominator)) for z in turns)
        steps = ['The particle changes direction where v(t) changes sign (crosses the t-axis), not just where it touches 0.',
                 f'v changes sign at {ans}.']
        dis = ['t = ' + str(pts[1][0]), 't = ' + ' and t = '.join(str(a) for a, b in pts if b == 0 and 0 < a < T) or 't = 1', f't = {T}']
    if q['format'] == 'multiple-choice':
        return record(q, 'vgraph_' + kind, p, ans, steps, fmt='multiple-choice', options=mc(rng, ans, [d for d in dis if d != ans] + [f'{num(sp.Rational(signed.numerator, signed.denominator) - 1)} m', '0 m']), diagram=diagram, standards=std)
    return record(q, 'vgraph_' + kind, p, ans, steps, diagram=diagram, standards=std)


# ---------------------------------------------------------------- washers about y = k
def washer(q, rng):
    lv = q['level']
    opts = {'cp2': [('x', 0, 2, -1), ('x', 0, 3, -2), ('2', 0, 3, -1)],
            'cp1': [('√x', 0, 4, -1), ('x²', 0, 2, -1), ('x', 0, 4, 5)],
            'honors': [('√x', 0, 4, 3), ('x²', 0, 1, 2), ('e^x', 0, 1, -1), ('√x', 1, 9, -2)]}
    f, a, b, k = rng.choice(opts[lv])
    import verify_keys as V
    fe = V.P(f)
    if k < 0:
        R, r = fe - k, -k
        where = 'below'
    else:
        R, r = k, k - fe
        where = 'above'
    integrand = sp.expand(R ** 2 - r ** 2)
    v = sp.simplify(sp.pi * sp.integrate(integrand, (x, a, b)))
    p = f'The region under y = {f} from x = {a} to x = {b} (above the x-axis) is revolved about the line y = {k}. Find the volume.'
    ans = bt(v)
    steps = [f'The line y = {k} is {where} the region, so each slice is a washer.',
             f'Outer radius R = {bt(R) if not isinstance(R, int) else R}, inner radius r = {bt(r) if not isinstance(r, int) else r} (distances from y = {k}).',
             f'V = π∫ from {a} to {b} (R² − r²) dx = π∫ from {a} to {b} ({bt(integrand)}) dx.',
             f'Antiderivative: {bt(sp.integrate(integrand, x))}; evaluated from {a} to {b} gives {bt(sp.simplify(v / sp.pi))}.', f'V = {ans}.']
    return record(q, 'washer_line', p, ans, steps, standards=['AP CHA-5.C'])


# ---------------------------------------------------------------- exponential models
def growth(q, rng):
    lv = q['level']
    if lv == 'cp2':
        p0, k = rng.choice([200, 300, 500, 800]), rng.choice(['0.02', '0.03', '0.05', '-0.04'])
        p = f'A quantity P changes at a rate proportional to its size: dP/dt = {k}P, with P(0) = {p0}. Write P(t).'
        ans = f'{p0}e^({k}t)'
        steps = ['dP/dt = kP has solutions P(t) = P(0)e^(kt).', f'Here k = {k} and P(0) = {p0}.', f'P(t) = {ans}.']
        return record(q, 'exp_model', p, ans, steps, standards=['AP FUN-7.G', 'AP FUN-7.E'])
    if lv == 'cp1':
        p0, ratio, t1, t2 = rng.choice([(400, (3, 2), 5, 10), (100, (2, 1), 3, 9), (250, (4, 5), 2, 6), (60, (3, 1), 4, 8)])
        p1 = p0 * ratio[0] // ratio[1]
        n = t2 // t1
        p2 = Fr(p0) * Fr(ratio[0], ratio[1]) ** n
        p = f'A population grows (or decays) at a rate proportional to its size. P(0) = {p0} and P({t1}) = {p1}. Find P({t2}).'
        ans = num(sp.Rational(p2.numerator, p2.denominator))
        steps = ['dP/dt = kP gives P(t) = P(0)e^(kt).', f'P({t1}) = {p0}e^({t1}k) = {p1}, so e^({t1}k) = {p1}/{p0} = {num(sp.Rational(ratio[0], ratio[1]))}.',
                 f'P({t2}) = {p0}e^({t2}k) = {p0}(e^({t1}k))^{n} = {p0}({num(sp.Rational(ratio[0], ratio[1]))})^{n} = {ans}.']
        dis = [num(p0 * n * Fr(ratio[0], ratio[1])), num(p1 * n), num(p0 + (p1 - p0) * n), num(p2 * 2)]
        if q['format'] == 'multiple-choice':
            return record(q, 'exp_model', p, ans, steps, fmt='multiple-choice', options=mc(rng, ans, [d for d in dis if d != ans]), standards=['AP FUN-7.G', 'AP FUN-7.E'])
        return record(q, 'exp_model', p, ans, steps, standards=['AP FUN-7.G', 'AP FUN-7.E'])
    m0, half, T = rng.choice([(50, 8, 20), (120, 5, 12), (80, 30, 75), (200, 6, 15)])
    rem = m0 * 2 ** (-T / half)
    p = f'Calculator active. A radioactive substance decays at a rate proportional to the amount present, with a half-life of {half} years. How much of a {m0}-gram sample remains after {T} years? Round to the nearest hundredth of a gram.'
    ans = f'{rem:.2f} g'
    steps = ['dA/dt = kA gives A(t) = A(0)e^(kt).', f'Half-life {half}: e^({half}k) = 1/2, so k = ln(1/2)/{half} = -ln(2)/{half}.',
             f'A({T}) = {m0}e^(-{T}ln(2)/{half}) = {m0}(1/2)^({num(sp.Rational(T, half))}) ≈ {rem:.4f}.', f'About {ans}.']
    dis = [f'{m0 * (1 - T / half / 2):.2f} g' if m0 * (1 - T / half / 2) > 0 else f'{m0 / 2:.2f} g', f'{m0 * 2 ** (-T // half):.2f} g', f'{m0 / (T / half):.2f} g', f'{m0 * math.exp(-T / half):.2f} g']
    if q['format'] == 'multiple-choice':
        return record(q, 'exp_model', p, ans, steps, fmt='multiple-choice', options=mc(rng, ans, [d for d in dis if d != ans]), standards=['AP FUN-7.G', 'AP FUN-7.E'])
    return record(q, 'exp_model', p, ans, steps, standards=['AP FUN-7.G', 'AP FUN-7.E'])


PLAN = {
    'derivatives-skill-06': ((3, 7, 11), linear),
    'derivatives-skill-09': ((3, 7, 12), implicit2),
    'antiderivatives-definite-integrals-skill-05': ((3, 11), calculator),
    'applications-integrals-skill-04': ((3, 7, 10, 11), vgraph),
    'applications-integrals-skill-07': ((3, 7, 11), washer),
    'differential-equations-skill-06': ((4, 7, 12), growth),
}


def main():
    banks = lib.load()
    tags = lib.tags()
    n = 0
    def target(q):
        return q['skillId'] in PLAN and re.search(r'-\d{3}$', q['id']) and int(q['id'][-3:]) in PLAN[q['skillId']][0]
    for u, d in banks.items():
        # a prompt never repeats word for word inside a skill (at any level): compare with the items this script
        # leaves alone and with the ones it has already written, so a rerun makes the same choices
        used = {(q['skillId'], q['prompt']) for q in d['questions'] if not target(q)}
        for i, q in enumerate(d['questions']):
            if not target(q):
                continue
            fn = PLAN[q['skillId']][1]
            for attempt in range(40):
                rng = random.Random('cal-audit-10-' + q['id'] + ('' if attempt == 0 else f'-{attempt}'))
                new = fn(q, rng)
                if new is None or (q['skillId'], new['prompt']) not in used:
                    break
            if new is None:
                continue
            used.add((q['skillId'], new['prompt']))
            d['questions'][i] = new
            n += 1
    # calculator-active tags: items that need a calculator to finish (rounded decimals from e, ln, trig or numerical integration)
    for u, d in banks.items():
        tg = tags[u]
        for q in d['questions']:
            needs = bool(re.search(r'Calculator active|Round to the nearest (tenth|hundredth|thousandth)|three decimal places', q['prompt'])) and bool(re.search(r'e\^|ln|sin|cos|∫|half-life|Euler', q['prompt']))
            cur = tg.setdefault(q['id'], [])
            if needs and 'calculator-active' not in cur:
                cur.append('calculator-active')
            if not needs and 'calculator-active' in cur:
                cur.remove('calculator-active')
        path = os.path.join(lib.BANKS, 'meta', u + '.tags.json')
        raw = open(path, encoding='utf-8').read()
        txt = json.dumps(tg, ensure_ascii=False, indent=0) + ('\n' if raw.endswith('\n') else '')
        if txt != raw:
            open(path, 'w', encoding='utf-8').write(txt)
    lib.save(banks)
    print('replaced', n)


if __name__ == '__main__':
    main()
