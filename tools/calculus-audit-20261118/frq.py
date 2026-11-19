"""Calculus audit #5 (2026-11-18): AP-style free-response problems.

The open-response item of every skill and level (slot 015, until now a set of four short answers of one type)
becomes a free-response problem: a context, a table, a graph or a formula, three or four parts that build on each
other, at least one part that asks for a justification, and scoring notes for the teacher (points per part).
Twelve problem types are mapped to the 70 skills; numbers come from the level (CP2 gentler, Honors with
exponential, trig and log functions). Answers are computed exactly with sympy. Deterministic and idempotent.
"""
import math, os, random, re, sys
from fractions import Fraction as Fr
import sympy as sp
sys.path.insert(0, os.path.dirname(__file__))
import lib
from bankfmt import bt
from author import record

x, t = sp.symbols('x t')
NOTE = 'Free response'


def n(v):
    return bt(sp.nsimplify(v))


def line(m, a, b):
    """Tangent line through (a, b) with slope m, in slope-intercept form."""
    return 'y = ' + bt(sp.expand(sp.nsimplify(b) + sp.nsimplify(m) * (x - a)))


def P(s):
    import verify_keys as V
    return V.P(s)


def frq(base, skill_name, stem, parts, diagram=None, fam='frq'):
    """parts: list of (prompt, answer, work, points, scoring)."""
    labels = 'abcd'
    steps = []
    total = 0
    for i, (pp, a, work, pts, score) in enumerate(parts):
        total += pts
        steps.append(f'({labels[i]}) {work}')
        steps.append(f'({labels[i]}) Scoring, {pts} point{"s" if pts > 1 else ""}: {score}')
    steps.append(f'Total: {total} points.')
    q = record(base, fam, f'{NOTE} ({skill_name}). {stem}', '; '.join(f'({labels[i]}) {p[1]}' for i, p in enumerate(parts)), steps,
               fmt='open-response', parts=[{'label': labels[i], 'prompt': p[0], 'answer': p[1]} for i, p in enumerate(parts)], diagram=diagram)
    return q


# ---------------------------------------------------------------- 1. rate in a table (accumulation, IVT, estimates)
def t_table(lv, rng):
    times = [0, 2, 5, 7, 10] if lv != 'cp2' else [0, 2, 4, 6, 8]
    base = rng.choice([8, 10, 12])
    vals = [base + rng.randint(-3, 6) for _ in times]
    while len(set(vals)) < 4 or vals[2] == vals[3]:
        vals = [base + rng.randint(-3, 6) for _ in times]
    i = 2
    slope = Fr(vals[i + 1] - vals[i - 1], times[i + 1] - times[i - 1])
    trap = sum(Fr(times[k + 1] - times[k]) * Fr(vals[k] + vals[k + 1], 2) for k in range(len(times) - 1))
    lo, hi = sorted([vals[0], vals[1]])
    target = Fr(lo + hi, 2) if lo != hi else Fr(lo)
    start = rng.choice([200, 300, 500])
    T = times[-1]
    table = '; '.join(f'R({a}) = {b}' for a, b in zip(times, vals))
    stem = f'Water flows into a tank at a rate R(t) gallons per hour, where R is differentiable and t is in hours. Selected values: {table}. The tank holds {start} gallons at t = 0.'
    parts = [
        (f'Use the data to estimate R′({times[i]}). Show the computation and give units.', f'{n(slope)} gallons per hour per hour',
         f'R′({times[i]}) ≈ (R({times[i + 1]}) − R({times[i - 1]}))/({times[i + 1]} − {times[i - 1]}) = ({vals[i + 1]} − {vals[i - 1]})/{times[i + 1] - times[i - 1]} = {n(slope)} gallons per hour per hour.', 1,
         'a difference quotient using values on either side of the point, with units.'),
        (f'Use a trapezoidal sum with the four subintervals in the table to approximate ∫ from 0 to {T} R(t) dt. Explain what it means in context.', f'{n(trap)} gallons; about {n(trap)} gallons flow in from t = 0 to t = {T}',
         'Trapezoids: ' + ' + '.join(f'{times[k + 1] - times[k]}({vals[k]} + {vals[k + 1]})/2' for k in range(len(times) - 1)) + f' = {n(trap)}. It estimates the gallons that flow in during the first {T} hours.', 2,
         '1 point for the trapezoidal sum, 1 point for the meaning with units.'),
        (f'Must there be a time t in (0, {times[1]}) when R(t) = {n(target)}? Justify your answer.' if lo != hi else f'Must there be a time t in (0, {times[1]}) when R′(t) = 0? Justify your answer.',
         'Yes' if lo != hi else 'Yes',
         (f'R is differentiable, so it is continuous on [0, {times[1]}]. {n(target)} is between R(0) = {vals[0]} and R({times[1]}) = {vals[1]}, so by the Intermediate Value Theorem, yes.' if lo != hi else
          f'R is differentiable and R(0) = R({times[1]}) = {vals[0]}, so by the Mean Value Theorem (Rolle) some c has R′(c) = 0.'), 2,
         '1 point for continuity (or differentiability), 1 point for naming the theorem and the values that satisfy it.'),
        (f'Use your answer to part (b) to estimate the amount of water in the tank at t = {T}.', f'{n(start + trap)} gallons',
         f'Amount ≈ {start} + {n(trap)} = {n(start + trap)} gallons.', 1, 'the starting amount plus the estimate from (b).'),
    ]
    return stem, parts, None


# ---------------------------------------------------------------- 2. particle motion from a formula
def t_motion(lv, rng):
    if lv == 'honors':
        v, T = rng.choice([('2cos(πt/2)', 3), ('t² - 5t + 4', 5), ('3sin(πt/3)', 5), ('t³ - 6t² + 9t', 4), ('sin(t)', 4), ('t² - 6t + 8', 5), ('4cos(πt/4)', 3)])
    else:
        a = rng.randint(1, 3)
        b = a + rng.randint(2, 4)
        v, T = f'(t - {a})(t - {b})', b + 1
    ve = P(v)
    zs = sorted([z for z in sp.solve(ve, t) if z.is_real and 0 < z < T], key=float)
    acc = sp.diff(ve, t)
    t0 = rng.choice([s for s in [sp.Rational(1, 2), 1, 2, 3, sp.Rational(9, 2)] if s < T and ve.subs(t, s) != 0 and acc.subs(t, s) != 0])
    vt0, at0 = sp.simplify(ve.subs(t, t0)), sp.simplify(acc.subs(t, t0))
    speeding = (vt0 > 0) == (at0 > 0)
    disp = sp.simplify(sp.integrate(ve, (t, 0, T)))
    pts = [0] + zs + [T]
    dist = sp.nsimplify(sp.simplify(sum(sp.Abs(sp.integrate(ve, (t, p0, p1))) for p0, p1 in zip(pts, pts[1:]))))
    stem = f'A particle moves along the x-axis with velocity v(t) = {v} meters per second for 0 ≤ t ≤ {T}.'
    parts = [
        ('At what time(s) does the particle change direction? Justify your answer.', ', '.join(f't = {n(z)}' for z in zs) or 'never',
         f'v(t) = 0 at {", ".join("t = " + n(z) for z in zs)}, and v changes sign there.', 2, '1 point for the times, 1 point for "v changes sign" as the reason.'),
        (f'Is the particle speeding up or slowing down at t = {n(t0)}? Give a reason.', 'speeding up' if speeding else 'slowing down',
         f'v({n(t0)}) = {n(vt0)} and a({n(t0)}) = v′({n(t0)}) = {n(at0)}; they have {"the same sign" if speeding else "opposite signs"}, so it is {"speeding up" if speeding else "slowing down"}.', 2,
         '1 point for a(t) at the time, 1 point for comparing the signs of v and a.'),
        (f'Find the displacement of the particle from t = 0 to t = {T}.', f'{n(disp)} m', f'∫ from 0 to {T} v(t) dt = {n(disp)} m.', 1, 'the definite integral of v with its value.'),
        (f'Find the total distance the particle travels from t = 0 to t = {T}.', f'{n(dist)} m', f'∫ from 0 to {T} |v(t)| dt: split at {", ".join(n(z) for z in zs)} and add the absolute values: {n(dist)} m.', 2,
         '1 point for using |v| (or splitting at the zeros), 1 point for the value.'),
    ]
    return stem, parts, None


# ---------------------------------------------------------------- 3. g(x) = ∫ f from a graph of f
GRAPHS = {'cp2': [[(-2, 2), (0, -2), (2, 2), (4, 2), (6, 0)], [(-2, -2), (0, 2), (2, 2), (4, -2), (6, -2)], [(-1, 1), (1, 3), (3, -1), (5, -1), (7, 1)], [(-2, 0), (0, 2), (2, 2), (4, -2), (6, 2)]],
          'cp1': [[(-3, 0), (-1, 2), (1, -2), (3, -2), (5, 2)], [(-3, -2), (-1, 2), (1, 2), (3, -2), (5, 0)], [(-4, 2), (-2, -2), (0, 2), (2, 2), (4, -2)], [(-2, 3), (0, 1), (2, -3), (4, -1), (6, 3)]],
          'honors': [[(-4, -2), (-2, 2), (0, 2), (2, -2), (4, 0), (6, 2)], [(-3, 3), (-1, -1), (1, -1), (3, 3), (5, -1), (7, -1)], [(-4, 0), (-2, -3), (0, 1), (2, 3), (4, -1), (6, -1)], [(-2, -1), (0, 3), (2, 1), (4, -3), (6, 1), (8, 1)]]}


def seg_area(pts, a, b):
    s = Fr(0)
    for (x0, y0), (x1, y1) in zip(pts, pts[1:]):
        lo, hi = max(a, x0), min(b, x1)
        if lo >= hi:
            continue
        f = lambda z: Fr(y0) + Fr(y1 - y0, x1 - x0) * (z - x0)
        s += (hi - lo) * (f(lo) + f(hi)) / 2
    return s


def zeros(pts):
    zs = []
    for (x0, y0), (x1, y1) in zip(pts, pts[1:]):
        if y0 * y1 < 0:
            zs.append(Fr(x0) - Fr(y0) * (x1 - x0) / (y1 - y0))
    for i in range(1, len(pts) - 1):
        if pts[i][1] == 0 and pts[i - 1][1] * pts[i + 1][1] < 0:
            zs.append(Fr(pts[i][0]))
    return sorted(set(zs))


def draw_f(pts, path, ylabel='f(x)'):
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    fig, ax = plt.subplots(figsize=(4.8, 3.0), dpi=150)
    xs, ys = zip(*pts)
    ax.plot(xs, ys, color='#1f3b73', lw=2.2)
    ax.plot(xs, ys, 'o', color='#1f3b73', ms=4)
    ax.axhline(0, color='black', lw=1)
    ax.axvline(0, color='black', lw=1)
    ax.set_xlim(min(xs) - 0.3, max(xs) + 0.3)
    ax.set_ylim(min(min(ys), 0) - 1, max(max(ys), 0) + 1)
    ax.set_xticks(list(range(min(xs), max(xs) + 1)))
    ax.set_xticklabels([str(v) for v in range(min(xs), max(xs) + 1)])
    ylo, yhi = min(min(ys), 0) - 1, max(max(ys), 0) + 1
    ax.set_yticks(list(range(ylo, yhi + 1)))
    ax.set_yticklabels([str(v).replace('-', '−') for v in range(ylo, yhi + 1)])
    ax.set_xticklabels([str(v).replace('-', '−') for v in range(min(xs), max(xs) + 1)])
    ax.grid(True, color='#d8dde6', lw=0.6)
    ax.set_xlabel('x')
    ax.set_ylabel(ylabel)
    fig.tight_layout()
    os.makedirs(os.path.dirname(path), exist_ok=True)
    fig.savefig(path)
    plt.close(fig)


def t_accum(lv, rng, qid, unit):
    pts = rng.choice(GRAPHS[lv])
    if rng.random() < 0.5:
        pts = [(p, -q) for p, q in pts]
    a = rng.choice([0, 0, 1, -1])
    xs = [p[0] for p in pts]
    lo, hi = xs[0], xs[-1]
    zs = zeros(pts)
    g = lambda z: seg_area(pts, a, z) if z >= a else -seg_area(pts, z, a)
    b1 = hi
    fn = f'{qid}.png'
    src = f'question-banks/assets/calculus/{unit}/{fn}'
    draw_f(pts, os.path.join(lib.ROOT, src))
    alt = 'Graph of f made of line segments through ' + ', '.join(f'({p}, {q})' for p, q in pts) + '.'
    cuts = [Fr(lo)] + zs + [Fr(hi)]
    sign = lambda c0, c1: (Fr(1) if f_at(pts, (c0 + c1) / 2) > 0 else Fr(-1))
    incs = [f'({n(c0)}, {n(c1)})' for c0, c1 in zip(cuts, cuts[1:]) if sign(c0, c1) > 0]
    maxes = [z for z in zs if f_at(pts, z - Fr(1, 100)) > 0 and f_at(pts, z + Fr(1, 100)) < 0]
    # inflection points of g: where f changes from increasing to decreasing (vertices with slope sign change)
    infl = [Fr(pts[i][0]) for i in range(1, len(pts) - 1) if (pts[i][1] - pts[i - 1][1]) * (pts[i + 1][1] - pts[i][1]) < 0]
    stem = f'The function f is defined on [{lo}, {hi}] and its graph, made of line segments, is shown. Let g(x) = ∫ from {a} to x f(t) dt.'
    parts = [
        (f'Find g({b1}) and g({lo}).', f'g({b1}) = {n(g(b1))}; g({lo}) = {n(g(lo))}',
         f'g({b1}) = signed area from {a} to {b1} = {n(g(b1))}; g({lo}) = −(signed area from {lo} to {a}) = {n(g(lo))}.', 2, '1 point each; the second needs the sign change for a reversed interval.'),
        (f'On what open interval(s) in ({lo}, {hi}) is g increasing? Justify your answer.', ' ∪ '.join(incs) or 'none',
         f'g′(x) = f(x), so g increases where f > 0: {" ∪ ".join(incs)}.', 2, '1 point for the intervals, 1 point for "g′ = f > 0".'),
        (f'At what x-value(s) in ({lo}, {hi}) does g have a relative maximum? Justify your answer.', ', '.join(f'x = {n(z)}' for z in maxes) or 'none',
         f'g′ = f changes from positive to negative at {", ".join("x = " + n(z) for z in maxes) or "no point"}.', 2, '1 point for the x-value(s), 1 point for the sign change of g′ = f.'),
        (f'Find the x-coordinate(s) of the points of inflection of the graph of g in ({lo}, {hi}). Explain your reasoning.', ', '.join(f'x = {n(z)}' for z in infl) or 'none',
         f'g″ = f′ changes sign where f changes from increasing to decreasing or back: {", ".join("x = " + n(z) for z in infl)}.', 2, '1 point for the x-values, 1 point for "g″ = f′ changes sign".'),
    ]
    return stem, parts, {'type': 'image', 'spec': {'src': src, 'alt': alt}}


def f_at(pts, z):
    for (x0, y0), (x1, y1) in zip(pts, pts[1:]):
        if x0 <= z <= x1:
            return Fr(y0) + Fr(y1 - y0, x1 - x0) * (Fr(z) - x0)
    return Fr(0)


# ---------------------------------------------------------------- 4. analysis of a function from its formula
def t_analysis(lv, rng):
    if lv == 'honors':
        f, a, b = rng.choice([('xe^(-x)', 0, 3), ('x²e^(-x)', -1, 4), ('x - 2ln(x)', 1, 4), ('x - 4ln(x)', 1, 6), ('x³e^(-x)', 0, 5), ('x + 2cos(x)', 0, sp.pi)])
    else:
        r1 = rng.randint(-3, 2)
        r2 = r1 + rng.choice([2, 4, 6])
        f = bt(sp.expand(sp.integrate(3 * (x - r1) * (x - r2), x) + rng.randint(-2, 3)))
        a, b = r1 - 1, r2 + 1
    fe = P(f)
    d1, d2 = sp.diff(fe, x), sp.diff(fe, x, 2)
    cs = sorted([c for c in sp.solve(d1, x) if c.is_real and a < c < b], key=float)
    cls = []
    for c in cs:
        s2 = d2.subs(x, c)
        cls.append(f'relative {"minimum" if s2 > 0 else "maximum"} at x = {n(c)}')
    cands = [(sp.simplify(fe.subs(x, c)), c) for c in [a] + cs + [b]]
    mx = max(cands, key=lambda z: float(z[0]))
    inf = sorted([c for c in sp.solve(d2, x) if c.is_real and a < c < b], key=float)
    stem = f'Let f(x) = {f} on the closed interval [{bt(a)}, {bt(b)}].'
    parts = [
        ('Find f′(x) and the critical numbers of f in the open interval.', f'f′(x) = {bt(sp.factor(d1))}; ' + ', '.join(f'x = {n(c)}' for c in cs),
         f'f′(x) = {bt(sp.factor(d1))}, which is 0 at {", ".join(n(c) for c in cs)}.', 2, '1 point for f′, 1 point for the critical numbers.'),
        ('Classify each critical number as a relative maximum, a relative minimum or neither. Justify your answer.', '; '.join(cls),
         'Second derivative test: f″(x) = ' + bt(sp.simplify(d2)) + '; ' + '; '.join(f'f″({n(c)}) = {n(sp.simplify(d2.subs(x, c)))}' for c in cs) + '.', 2,
         '1 point for each classification with a correct reason (sign change of f′ or sign of f″).'),
        (f'Find the absolute maximum value of f on [{bt(a)}, {bt(b)}]. Justify your answer.', f'{n(mx[0])} at x = {n(mx[1])}',
         'Candidates test: ' + '; '.join(f'f({n(c)}) = {n(v)}' for v, c in cands) + '.', 2, '1 point for evaluating every candidate (critical numbers and endpoints), 1 point for the answer.'),
        ('Find the x-coordinate(s) of any points of inflection. Justify your answer.', ', '.join(f'x = {n(c)}' for c in inf) or 'none',
         f'f″ changes sign at {", ".join(n(c) for c in inf) or "no point in the interval"}.', 1, 'the x-value(s) with "f″ changes sign".'),
    ]
    return stem, parts, None


# ---------------------------------------------------------------- 5. piecewise: limits, continuity, differentiability
def t_piecewise(lv, rng):
    c = rng.choice([1, 2, 3, 4])
    if lv == 'honors':
        left = rng.choice([f'e^(x - {c})', f'ln(x - {c - 1})' if c > 1 else 'ln(x)', f'√(x + {5 - c})' if c != 5 else '√x'])
    else:
        p = rng.randint(-4, 3)
        left = bt(x ** 2 + p * x + rng.randint(-2, 2))
    lname = P(left)
    m = rng.choice([1, 2, 3, 4])
    ls = sp.diff(lname, x).subs(x, c)
    if ls.is_Integer and ls > 0 and rng.random() < 0.4:
        m = int(ls)
    k = sp.simplify(lname.subs(x, c) - m * c)
    right = f'{m}x + k' if m != 1 else 'x + k'
    dl, dr = sp.diff(lname, x).subs(x, c), m
    stem = f'f(x) = {left} for x < {c}, and f(x) = {right} for x ≥ {c}, where k is a constant.'
    parts = [
        (f'Find lim (x → {c}⁻) f(x).', n(lname.subs(x, c)), f'Use the left piece: {n(lname.subs(x, c))}.', 1, 'the left-hand limit.'),
        (f'Find lim (x → {c}⁺) f(x) in terms of k.', f'{bt(m * c)} + k', f'Use the right piece: {"" if m == 1 else m}({c}) + k = {bt(m * c)} + k.', 1, 'the right-hand limit in terms of k.'),
        (f'Find the value of k that makes f continuous at x = {c}. Use the definition of continuity.', f'k = {n(k)}',
         f'Continuity needs lim (x → {c}⁻) f(x) = f({c}): {n(lname.subs(x, c))} = {'' if m == 1 else m}({c}) + k, so k = {n(k)}.', 2, '1 point for setting the one-sided limit equal to f(c), 1 point for k.'),
        (f'With that k, is f differentiable at x = {c}? Justify your answer.', 'Yes' if sp.simplify(dl - dr) == 0 else 'No',
         f'Left slope {n(dl)}, right slope {dr}: {"equal, so f is differentiable" if sp.simplify(dl - dr) == 0 else "different, so f is not differentiable (a corner)"}.', 2,
         '1 point for both one-sided derivatives, 1 point for the conclusion.'),
    ]
    return stem, parts, None


# ---------------------------------------------------------------- 6. related rates
def t_related(lv, rng):
    L, xr, rate = rng.choice([(13, 5, 2), (10, 6, 3), (25, 7, 4), (17, 8, 1)])
    yv = int(math.isqrt(L * L - xr * xr))
    yr = Fr(-xr * rate, yv)
    stem = f'A {L}-ft ladder leans against a vertical wall. The bottom slides away from the wall at {rate} ft/s.'
    area_rate = Fr(1, 2) * (rate * yv + xr * yr)
    parts = [
        ('Write an equation relating x, the distance from the wall to the bottom, and y, the height of the top.', f'x² + y² = {L * L}', 'The ladder, wall and ground form a right triangle.', 1, 'the equation.'),
        (f'How fast is the top sliding down when the bottom is {xr} ft from the wall? Give units.', f'{n(abs(yr))} ft/s',
         f'2x·dx/dt + 2y·dy/dt = 0. At x = {xr}, y = {yv}: dy/dt = −({xr})({rate})/{yv} = {n(yr)}, so down at {n(abs(yr))} ft/s.', 3,
         '1 point for differentiating with respect to t, 1 point for y, 1 point for the rate with units.'),
        ('Let θ be the angle between the ladder and the ground. How fast is θ changing at that moment?', f'{n(Fr(-rate, yv))} radians per second',
         f'cos θ = x/{L}, so −sin θ·dθ/dt = (1/{L})dx/dt. With sin θ = {yv}/{L}: dθ/dt = −{rate}/{yv} = {n(Fr(-rate, yv))} rad/s (the angle is decreasing).', 2, '1 point for differentiating a trig relation, 1 point for the rate.'),
        ('Is the area of the triangle formed by the ladder, wall and ground increasing or decreasing at that moment? Justify your answer.',
         'increasing' if area_rate > 0 else 'decreasing',
         f'A = (1/2)xy, so dA/dt = (1/2)(dx/dt·y + x·dy/dt) = (1/2)({rate}·{yv} + {xr}·({n(yr)})) = {n(area_rate)} ft²/s.', 2, '1 point for dA/dt with the product rule, 1 point for the sign and conclusion.'),
    ]
    return stem, parts, None


# ---------------------------------------------------------------- 7. optimization
def t_optim(lv, rng):
    side = rng.choice([12, 18, 24, 30])
    xs = Fr(side, 6)
    V = xs * (side - 2 * xs) ** 2
    stem = f'Equal squares of side x inches are cut from the corners of a {side}-in by {side}-in sheet of cardboard, and the sides are folded up to make an open box.'
    parts = [
        ('Write the volume V(x) and give its domain.', f'V(x) = x({side} - 2x)², 0 < x < {side // 2}', f'Length and width {side} − 2x, height x.', 1, 'V(x) with the domain.'),
        ('Find the value of x that gives the largest volume. Justify that it is a maximum.', f'x = {n(xs)} in',
         f'V′(x) = ({side} − 2x)({side} − 6x) = 0 at x = {n(xs)} (x = {side // 2} gives V = 0). V′ changes from + to − at x = {n(xs)}.', 3, '1 point for V′, 1 point for the critical number, 1 point for the justification.'),
        ('Give the dimensions of the box with the largest volume.', f'{n(side - 2 * xs)} in by {n(side - 2 * xs)} in by {n(xs)} in', f'Base {side} − 2({n(xs)}) = {n(side - 2 * xs)} on each side, height {n(xs)}.', 1, 'all three dimensions.'),
        ('Find the maximum volume.', f'{n(V)} in³', f'V({n(xs)}) = {n(xs)}({side} − {n(2 * xs)})² = {n(V)} in³.', 1, 'the value with units.'),
    ]
    return stem, parts, None


# ---------------------------------------------------------------- 8. differential equation
def t_de(lv, rng):
    if lv == 'honors':
        k = rng.choice([2, 3, 4])
        de, x0, y0 = f'xy/{k}', 1, rng.randint(2, 6)
        rhs = x * sp.Symbol('y') / k
    else:
        k = rng.randint(1, 5)
        x0, y0 = rng.choice([1, 2]), rng.randint(2, 6)
        if y0 * y0 == k * x0 * x0:
            y0 += 1
        de = f'{k}x/y' if k != 1 else 'x/y'
        rhs = k * x / sp.Symbol('y')
    Y = sp.Symbol('y')
    slope0 = rhs.subs({x: x0, Y: y0})
    est = y0 + slope0 * Fr(1, 10)
    if lv == 'honors':
        sol = f'{y0}e^((x² - 1)/{2 * k})'
        sole = y0 * sp.exp((x ** 2 - 1) / (2 * k))
    else:
        Cc = y0 * y0 - k * x0 * x0
        sol = f'√({bt(k * x ** 2 + Cc)})'
        sole = sp.sqrt(k * x ** 2 + Cc)
    yy = sp.diff(rhs, x) + sp.diff(rhs, Y) * rhs
    d2 = sp.simplify(yy.subs({x: x0, Y: y0}))
    x1 = x0 + 1
    fx1 = sp.simplify(sole.subs(x, x1))
    stem = f'Consider the differential equation dy/dx = {de}. Let y = f(x) be the solution with f({x0}) = {y0}.'
    parts = [
        (f'Write an equation of the line tangent to the graph of f at x = {x0}, and use it to approximate f({x0 + 0.1:g}).', f'{line(slope0, x0, y0)}; f({x0 + 0.1:g}) ≈ {n(est)}',
         f'dy/dx at ({x0}, {y0}) is {n(slope0)}; L({x0 + 0.1:g}) = {y0} + ({n(slope0)})(0.1) = {n(est)}.', 2, '1 point for the tangent line, 1 point for the approximation.'),
        (f'Find d²y/dx² at ({x0}, {y0}). Is the approximation in part (a) an overestimate or an underestimate? Explain.',
         f'{n(d2)}; ' + ('an underestimate' if d2 > 0 else ('an overestimate' if d2 < 0 else 'cannot tell from concavity')),
         f'd²y/dx² = ∂/∂x(dy/dx) + ∂/∂y(dy/dx)·dy/dx = {n(d2)} at the point; ' + ('concave up, so the tangent line lies below the curve.' if d2 > 0 else 'concave down, so the tangent line lies above the curve.' if d2 < 0 else ''), 2,
         '1 point for d²y/dx², 1 point for the conclusion from concavity.'),
        ('Use separation of variables to find y = f(x).', f'y = {sol}',
         ('Separate: (1/y) dy = (x/' + str(k) + ') dx; ln|y| = x²/' + str(2 * k) + ' + C; y(1) = ' + str(y0) + ' gives y = ' + sol + '.') if lv == 'honors' else
         (f'Separate: y dy = {bt(k * x)} dx; y²/2 = {bt(k * x ** 2 / 2)} + C; y² = {bt(k * x ** 2 + y0 * y0 - k * x0 * x0)}, so y = {sol} (positive because f({x0}) > 0).'), 4,
         '1 point for separating, 1 point for the antiderivatives, 1 point for the constant from the initial condition, 1 point for solving for y.'),
        (f'Use your solution to find f({x1}) exactly.', bt(fx1), f'Substitute x = {x1} into y = {sol}.', 1, 'the exact value.'),
    ]
    return stem, parts, None


# ---------------------------------------------------------------- 9. area and volume
def t_region(lv, rng):
    if lv == 'cp2':
        f, g, a, b = rng.choice([('x', 'x²', 0, 1), ('2x', 'x²', 0, 2), ('3x', 'x²', 0, 3), ('1', 'x²', -1, 1)])
    elif lv == 'cp1':
        f, g, a, b = rng.choice([('2x', 'x²', 0, 2), ('4', 'x²', -2, 2), ('x + 2', 'x²', -1, 2), ('4x', 'x²', 0, 4), ('9', 'x²', -3, 3)])
    else:
        f, g, a, b = rng.choice([('√x', 'x²', 0, 1), ('x', 'x³', 0, 1), ('√x', 'x/2', 0, 4), ('2√x', 'x', 0, 4), ('x²', 'x³', 0, 1)])
    fe, ge = P(f), P(g)
    area = sp.integrate(fe - ge, (x, a, b))
    wash = sp.pi * sp.integrate(fe ** 2 - ge ** 2, (x, a, b))
    sq = sp.integrate((fe - ge) ** 2, (x, a, b))
    stem = f'Let R be the region enclosed by the graphs of y = {f} and y = {g} for {a} ≤ x ≤ {b}.'
    parts = [
        ('Find the area of R.', n(area), f'∫ from {a} to {b} [({f}) − ({g})] dx = {n(area)}.', 2, '1 point for the integrand (top minus bottom), 1 point for the value.'),
        ('Find the volume of the solid formed when R is revolved about the x-axis. Explain why each cross section is a washer.', n(wash), f'The region lies between y = {g} and y = {f}, not against the axis of rotation, so each slice is a disk with a hole: outer radius {f}, inner radius {g}. Washers: π∫ from {a} to {b} [({f})² − ({g})²] dx = {n(wash)}.', 2, '1 point for R² − r² (not (R − r)²), 1 point for the value.'),
        ('Write, but do not evaluate, an integral for the volume of the solid formed when R is revolved about the line y = −1.', f'π∫ from {a} to {b} [({f} + 1)² − ({g} + 1)²] dx',
         'Each radius grows by 1: outer radius (top + 1), inner radius (bottom + 1).', 1, 'the integrand with both radii shifted by 1, with π and the limits.'),
        ('R is the base of a solid whose cross sections perpendicular to the x-axis are squares. Find the volume.', n(sq), f'Side = {f} − {g}: ∫ from {a} to {b} ({f} − {g})² dx = {n(sq)}.', 2, '1 point for the area of a square cross section, 1 point for the value.'),
    ]
    return stem, parts, None


# ---------------------------------------------------------------- 10. derivative definition, tangent line, approximation
def t_tangent(lv, rng):
    if lv == 'honors':
        f, a = rng.choice([('√x', 4), ('√x', 9), ('ln(x)', 1), ('e^(2x)', 0), ('1/x', 2), ('xln(x)', 1), ('e^(-x)', 0)])
    else:
        f = bt(rng.choice([1, 2]) * x ** rng.choice([2, 3]) + rng.randint(-4, 4) * x)
        a = rng.choice([-1, 1, 2, 3])
    fe = P(f)
    fa, fpa, f2 = sp.simplify(fe.subs(x, a)), sp.simplify(sp.diff(fe, x).subs(x, a)), sp.simplify(sp.diff(fe, x, 2).subs(x, a))
    xa = a + sp.Rational(1, 10)
    L = fa + fpa * sp.Rational(1, 10)
    stem = f'Let f(x) = {f}.'
    parts = [
        (f'Write f′({a}) as a limit of a difference quotient, and find its value.', f'lim (h → 0) (f({a} + h) − f({a}))/h = {n(fpa)}', f'Definition of the derivative at x = {a}; the value is f′({a}) = {n(fpa)}.', 2, '1 point for the limit, 1 point for the value.'),
        (f'Write an equation for the line tangent to the graph of f at x = {a}.', line(fpa, a, fa), f'Point ({a}, {n(fa)}), slope {n(fpa)}.', 1, 'the line.'),
        (f'Use the tangent line to approximate f({n(xa)}). Is it an overestimate or an underestimate? Justify your answer.', f'{n(L)}; ' + ('an underestimate' if f2 > 0 else 'an overestimate'),
         f'L({n(xa)}) = {n(L)}. f″({a}) = {n(f2)}, so f is concave {"up" if f2 > 0 else "down"} near x = {a} and the tangent line lies {"below" if f2 > 0 else "above"} the graph.', 2,
         '1 point for the approximation, 1 point for the concavity reason.'),
        (f'Write an equation for the line normal to the graph of f at x = {a}.', line(-1 / fpa, a, fa) if fpa != 0 else f'x = {a}',
         'The normal line is perpendicular to the tangent line: its slope is the negative reciprocal of f′(' + str(a) + ').', 1, 'the normal line.'),
    ]
    return stem, parts, None


# ---------------------------------------------------------------- 11. Riemann sums and the definite integral
def t_riemann(lv, rng):
    if lv == 'honors':
        f, a, b, nn = rng.choice([('√x', 0, 4, 4), ('e^x', 0, 2, 4), ('1/x', 1, 3, 4), ('e^(-x)', 0, 2, 4), ('√x', 1, 9, 4)])
    else:
        f, a, b, nn = rng.choice([('x² + 1', 0, 4, 4), ('x²', 1, 3, 4), ('3x', 0, 4, 2), ('x² + 2', 0, 2, 4), ('2x + 1', 1, 5, 4), ('x³', 0, 2, 4), ('10 - x²', 0, 3, 3), ('8 - 2x', 0, 4, 4)])
    fe = P(f)
    dx = sp.Rational(b - a, nn)
    right = sum(fe.subs(x, a + (k + 1) * dx) for k in range(nn)) * dx
    exact = sp.integrate(fe, (x, a, b))
    inc = sp.diff(fe, x).subs(x, (a + b) / 2) > 0
    trap = sp.nsimplify(sum((fe.subs(x, a + k * dx) + fe.subs(x, a + (k + 1) * dx)) / 2 for k in range(nn)) * dx)
    inside = f'{a} + {n(b - a)}k/n' if a else f'{n(b - a)}k/n'
    term = '[' + f.replace('x', f'({inside})') + ']'
    stem = f'Let f(x) = {f} on [{a}, {b}].'
    parts = [
        (f'Approximate ∫ from {a} to {b} f(x) dx with a right Riemann sum using {nn} equal subintervals.', n(sp.nsimplify(right)) + ('' if sp.nsimplify(right).is_Rational else f' ≈ {float(right):.3f}'), f'Δx = {n(dx)}; right endpoints {", ".join(n(a + (k + 1) * dx) for k in range(nn))}; sum = {n(sp.nsimplify(right))}.', 2, '1 point for Δx and the endpoints, 1 point for the value.'),
        ('Is the right Riemann sum an overestimate or an underestimate? Justify your answer.', 'an overestimate' if inc else 'an underestimate',
         f'f is {"increasing" if inc else "decreasing"} on [{a}, {b}], so each right endpoint is the {"largest" if inc else "smallest"} value on its subinterval.', 2, '1 point for monotonicity, 1 point for the conclusion.'),
        (f'Approximate ∫ from {a} to {b} f(x) dx with a trapezoidal sum using the same {nn} subintervals.', n(trap) + ('' if trap.is_Rational else f' ≈ {float(trap):.3f}'),
         f'(Δx/2)[f(x₀) + 2f(x₁) + … + 2f(x₍ₙ₋₁₎) + f(xₙ)] = {n(trap)}.', 1, 'the trapezoidal sum.'),
        (f'Write ∫ from {a} to {b} f(x) dx as the limit of a right Riemann sum, and evaluate the integral exactly.', f'lim (n → ∞) Σ (k = 1 to n) {term}·({n(b - a)}/n); {n(exact)}',
         f'Δx = {n(b - a)}/n and xₖ = {inside}. By the Fundamental Theorem, the integral is {n(exact)}.', 2, '1 point for the limit of the sum, 1 point for the exact value.'),
    ]
    return stem, parts, None


# ---------------------------------------------------------------- 12. justification with theorems (MVT / IVT / EVT)
def t_theorems(lv, rng):
    xs = [0, 2, 5, 7]
    vals = [rng.randint(-4, 8) for _ in xs]
    while vals[0] == vals[-1] or not any(vals[k] * vals[k + 1] < 0 for k in range(3)):
        vals = [rng.randint(-4, 8) for _ in xs]
    avg = Fr(vals[-1] - vals[0], 7)
    sc = sum(1 for k in range(3) if vals[k] * vals[k + 1] < 0)
    table = '; '.join(f'f({a}) = {b}' for a, b in zip(xs, vals))
    stem = f'The function f is differentiable on (−∞, ∞). Selected values: {table}.'
    parts = [
        ('Must there be a value c in (0, 7) with f′(c) = ' + n(avg) + '? Justify your answer.', 'Yes',
         f'f is differentiable, so continuous on [0, 7] and differentiable on (0, 7). By the Mean Value Theorem some c has f′(c) = (f(7) − f(0))/7 = {n(avg)}.', 2,
         '1 point for the hypotheses, 1 point for the theorem and the average rate.'),
        ('What is the least number of zeros f must have on [0, 7]? Justify your answer.', str(sc),
         f'f is continuous; f changes sign {sc} time(s) between consecutive table values, so by the Intermediate Value Theorem it has at least {sc} zero(s).', 2,
         '1 point for counting sign changes, 1 point for continuity and the IVT.'),
        ((f'Must there be a value c in (2, 5) with f(c) = {n(Fr(vals[1] + vals[2], 2))}? Justify your answer.' if vals[1] != vals[2] else 'Must there be a value c in (2, 5) with f′(c) = 0? Justify your answer.'), 'Yes',
         (f'f is continuous on [2, 5] and {n(Fr(vals[1] + vals[2], 2))} is between f(2) = {vals[1]} and f(5) = {vals[2]}, so by the Intermediate Value Theorem, yes.' if vals[1] != vals[2] else
          'f(2) = f(5) and f is differentiable, so by the Mean Value Theorem (Rolle) some c has f′(c) = 0.'), 2, '1 point for the hypotheses, 1 point for the theorem with the values.'),
        ('Must f have an absolute maximum on [0, 7]? Justify your answer.', 'Yes',
         'f is continuous on the closed interval [0, 7], so by the Extreme Value Theorem it has an absolute maximum there.', 1, 'continuity on a closed interval and the EVT.'),
    ]
    return stem, parts, None


# ---------------------------------------------------------------- 13. interpretation and notation in context
def t_context(lv, rng):
    ctx = rng.choice([('W', 'the amount of water in the pond', 'gallons', 'days'), ('P', 'the number of people in the museum', 'people', 'hours'), ('H', 'the height of a plant', 'centimeters', 'weeks')])
    S, name, u, tu = ctx
    a, b = rng.choice([(2, 6), (1, 5), (3, 9)])
    v = rng.choice([-4, -2, 3, 5])
    stem = f'{S}(t) is {name}, in {u}, t {tu} after a start time. {S} is twice differentiable.'
    parts = [
        (f'Interpret {S}′({a}) = {v} in context, with units.', f'At t = {a} {tu if a != 1 else tu[:-1]}, {name} is {"increasing" if v > 0 else "decreasing"} at {abs(v)} {u} per {tu[:-1]}',
         'A derivative is an instantaneous rate; the sign gives the direction.', 2, '1 point for the meaning at the instant, 1 point for the units.'),
        (f'Interpret ∫ from {a} to {b} {S}′(t) dt in context.', f'the net change in {name.replace("the ", "", 1)} from t = {a} to t = {b}, in {u}',
         'The integral of a rate is a net change.', 1, 'net change with the time interval and units.'),
        (f'Write an expression for the average value of {S} on {a} ≤ t ≤ {b}. Explain why its units are {u}.', f'(1/{b - a})∫ from {a} to {b} {S}(t) dt, in {u}',
         f'Average value = (1/(b − a))∫ from a to b. The integral has units {u}·{tu}, and dividing by the length of the interval ({tu}) leaves {u}.', 1, 'the expression with the units explained.'),
        (f'What are the units of {S}″(t)?', f'{u} per {tu[:-1]} per {tu[:-1]}', f'{S}″ is the rate of change of {S}′.', 1, 'the units.'),
    ]
    return stem, parts, None


# ---------------------------------------------------------------- 14. precalculus review (exponential model)
def t_precalc(lv, rng):
    a, k, c = rng.choice([(50, 2, 300), (20, 3, 100), (100, 2, 500), (40, 3, 200)])
    T = sp.log(sp.Rational(c, a)) / sp.log(k) if lv != 'cp2' else None
    stem = f'A culture has f(t) = {a}·{k}^t bacteria after t hours.'
    t1, t2 = 1, 3
    aroc = sp.Rational(a * k ** t2 - a * k ** t1, t2 - t1)
    parts = [
        (f'Find the average rate of change of f from t = {t1} to t = {t2}, with units.', f'{n(aroc)} bacteria per hour', f'(f({t2}) − f({t1}))/({t2} − {t1}) = ({a * k ** t2} − {a * k ** t1})/2 = {n(aroc)}.', 2, '1 point for the setup, 1 point for the value with units.'),
        (f'Solve f(t) = {c} exactly. Explain the step that brings t down from the exponent.', f't = ln({n(sp.Rational(c, a))})/ln({k})', f'{k}^t = {n(sp.Rational(c, a))}. Take ln of both sides: t·ln({k}) = ln({n(sp.Rational(c, a))}), so t = ln({n(sp.Rational(c, a))})/ln({k}) ≈ {float(sp.log(sp.Rational(c, a)) / sp.log(k)):.3f}.', 2, '1 point for isolating the power, 1 point for the logarithm.'),
        ('Find f′(2), the instantaneous rate of change at t = 2, with units.', f'{a * k * k}ln({k}) bacteria per hour', f'f′(t) = {a}·{k}^t·ln({k}), so f′(2) = {a * k * k}ln({k}) ≈ {a * k * k * math.log(k):.1f}.', 1, 'the derivative of an exponential with the ln factor.'),
        ('Rewrite f(t) in the form f(t) = a·e^(rt).', f'f(t) = {a}e^(t·ln({k}))', f'{k} = e^(ln {k}), so {k}^t = e^(t ln {k}).', 1, 'the base-e form.'),
    ]
    return stem, parts, None


# ---------------------------------------------------------------- 15. rational expressions: factor, simplify, holes
def t_algebra(lv, rng):
    a, b = rng.choice([(2, 3), (3, 1), (1, 4), (2, 5), (4, 1)] if lv != 'honors' else [(2, 3), (3, 1), (1, 4)])
    if lv == 'honors':
        num, den = sp.expand((x - a) * (x + b) * x), sp.expand((x - a) * x * x)
    else:
        num, den = sp.expand((x - a) * (x + b)), sp.expand((x - a) * (x + 2 * b))
    f = sp.cancel(num / den)
    hole_y = sp.simplify(f.subs(x, a))
    zs = sorted(sp.solve(sp.denom(sp.together(f)), x), key=float)
    stem = f'Let f(x) = ({bt(num)})/({bt(den)}).'
    parts = [
        ('Factor the numerator and the denominator completely.', f'{bt(sp.factor(num))}; {bt(sp.factor(den))}', f'Numerator {bt(sp.factor(num))}, denominator {bt(sp.factor(den))}.', 2, '1 point for each factorization.'),
        ('Simplify f(x) and state the values of x excluded from the domain.', f'{bt(f)}; x ≠ ' + ', '.join(n(r) for r in sorted(set(sp.solve(den, x)), key=float)),
         f'Cancel the common factor (x - {a}). The original denominator is 0 at ' + ', '.join(n(r) for r in sorted(set(sp.solve(den, x)), key=float)) + '.', 2, '1 point for the simplified form, 1 point for every excluded value (including the cancelled one).'),
        (f'Find lim (x → {a}) f(x). Is there a hole or a vertical asymptote at x = {a}? Explain.', f'{n(hole_y)}; a hole',
         f'The factor (x - {a}) cancels, so the limit is the simplified form at x = {a}: {n(hole_y)}. A finite limit where f is undefined is a removable discontinuity (a hole).', 2, '1 point for the limit, 1 point for the reason.'),
        ('Find the equation(s) of the vertical asymptote(s) of the graph of f.', ', '.join(f'x = {n(z)}' for z in zs),
         'Zeros of the simplified denominator that are not zeros of the numerator: ' + ', '.join(n(z) for z in zs) + '.', 1, 'every vertical asymptote.'),
    ]
    return stem, parts, None


# ---------------------------------------------------------------- 16. logarithmic function: domain, zero, inverse, derivative
def t_log(lv, rng):
    A, h, k = rng.choice([(2, 1, 4), (3, -2, 6), (1, 3, 2), (2, -1, -2), (4, 2, 8)])
    sh = f'x - {h}' if h > 0 else f'x + {-h}'
    fe = A * sp.log(x - h) + k
    zero = sp.simplify(h + sp.exp(sp.Rational(-k, A)))
    y = sp.Symbol('y')
    stem = f'Let f(x) = {"" if A == 1 else A}ln({sh}) {"+" if k > 0 else "-"} {abs(k)}.'
    parts = [
        ('State the domain of f and the equation of its vertical asymptote. Explain.', f'x > {h}; x = {h}', f'The argument {sh} must be positive.', 1, 'domain and asymptote.'),
        ('Find the exact zero of f.', f'x = {bt(zero)}', f'ln({sh}) = {n(sp.Rational(-k, A))}, so {sh} = {bt(sp.exp(sp.Rational(-k, A)))} and x = {bt(zero)}.', 2, '1 point for isolating the logarithm, 1 point for the exact value.'),
        ('Find the inverse function f⁻¹(x).', f'f⁻¹(x) = {bt(sp.exp((x - k) / A) + h)}', f'Swap x and y: x = {"" if A == 1 else A}ln({sh.replace("x", "y")}) {"+" if k > 0 else "-"} {abs(k)}' + f'; y = {bt(sp.exp((x - k) / A) + h)}.', 2, '1 point for exponentiating, 1 point for the inverse.'),
        (f'Find f′(x) and the slope of the graph at x = {h + 1}.', f'f′(x) = {bt(sp.diff(fe, x))}; {n(sp.diff(fe, x).subs(x, h + 1))}', f'd/dx ln(u) = u′/u.', 1, 'the derivative and the slope.'),
    ]
    return stem, parts, None


# ---------------------------------------------------------------- 17. trigonometric function on [0, 2π]
def t_trig(lv, rng):
    A, c, fn = rng.choice([(2, 1, 'sin'), (2, -1, 'sin'), (2, 1, 'cos'), (2, -1, 'cos'), (2, sp.sqrt(3), 'cos'), (2, sp.sqrt(2), 'sin')])
    F = sp.sin if fn == 'sin' else sp.cos
    fe = A * F(x) + c
    sols = sorted(sp.solveset(fe, x, sp.Interval(0, 2 * sp.pi)), key=float)
    cs = sorted(sp.solveset(sp.diff(fe, x), x, sp.Interval.open(0, 2 * sp.pi)), key=float)
    pts = [sp.pi / 6, sp.pi / 4, sp.pi / 3, 2 * sp.pi / 3, 3 * sp.pi / 4, 5 * sp.pi / 6, 7 * sp.pi / 6, 5 * sp.pi / 4, 4 * sp.pi / 3]
    p = rng.choice(pts)
    stem = f'Let f(x) = {A}{fn}(x) {"+" if c > 0 else "-"} {bt(abs(c))} for 0 ≤ x ≤ 2π.'
    parts = [
        (f'Find the exact value of f({bt(p)}).', bt(sp.nsimplify(fe.subs(x, p))), f'{fn}({bt(p)}) = {bt(F(p))}, so f({bt(p)}) = {bt(sp.nsimplify(fe.subs(x, p)))}.', 1, 'the exact value from the unit circle.'),
        ('Solve f(x) = 0 on [0, 2π].', ', '.join(f'x = {bt(s_)}' for s_ in sols), f'{fn}(x) = {bt(-c / A)}: reference angle and the quadrants where {fn} has that sign give ' + ', '.join(bt(s_) for s_ in sols) + '.', 2, '1 point for the equation in fn(x), 1 point for every solution.'),
        ('Find f′(x) and the x-values in (0, 2π) where the graph of f has a horizontal tangent line.', f'f′(x) = {bt(sp.diff(fe, x))}; ' + ', '.join(f'x = {bt(s_)}' for s_ in cs),
         f'f′(x) = {bt(sp.diff(fe, x))} = 0 at ' + ', '.join(bt(s_) for s_ in cs) + '.', 2, '1 point for f′, 1 point for the x-values.'),
        ('Find the range of f. Explain.', f'[{bt(c - A)}, {bt(c + A)}]', f'{fn}(x) runs from −1 to 1, so f runs from {bt(c - A)} to {bt(c + A)}.', 1, 'the range with a reason.'),
    ]
    return stem, parts, None


# ---------------------------------------------------------------- 18. limits of a rational function
def t_limits(lv, rng):
    a, b, m = rng.randint(1, 4), rng.randint(1, 5), rng.randint(1, 4)
    num = sp.expand(m * (x - a) * (x + b)) if lv != 'cp2' else sp.expand((x - a) * (x + b))
    den = sp.expand((x - a) * (x - (a + b)))
    if lv == 'cp2':
        m = 1
    f = sp.cancel(num / den)
    v = a + b
    L = sp.limit(f, x, a)
    lr, ll = sp.limit(f, x, v, '+'), sp.limit(f, x, v, '-')
    inf = sp.limit(f, x, sp.oo)
    stem = f'Let f(x) = ({bt(num)})/({bt(den)}).'
    sym = lambda z: '∞' if z == sp.oo else ('−∞' if z == -sp.oo else n(z))
    parts = [
        (f'Find lim (x → {a}) f(x). Show the algebra.', n(L), f'Factor and cancel (x - {a}): f(x) = {bt(f)} for x ≠ {a}; substitute x = {a}: {n(L)}.', 2, '1 point for factoring and cancelling, 1 point for the value.'),
        (f'Find lim (x → {v}⁺) f(x) and lim (x → {v}⁻) f(x).', f'{sym(lr)}; {sym(ll)}', f'Near x = {v} the numerator is about {n(sp.numer(sp.together(f)).subs(x, v))} and the denominator x - {v} changes sign.', 2, '1 point for each one-sided limit with a sign analysis.'),
        ('Find lim (x → ∞) f(x) and the horizontal asymptote.', f'{n(inf)}; y = {n(inf)}', 'Divide by the highest power of x: the ratio of leading coefficients.', 1, 'the limit and the asymptote.'),
        (f'Classify the discontinuities of f at x = {a} and x = {v}. Justify your answer.', f'x = {a}: removable; x = {v}: infinite (vertical asymptote)',
         f'At x = {a} the limit exists but f({a}) is undefined; at x = {v} the one-sided limits are infinite.', 2, '1 point for each classification with its limit reason.'),
    ]
    return stem, parts, None


# ---------------------------------------------------------------- 19. L'Hôpital's Rule
def t_lhop(lv, rng):
    pool = [('(e^x - 1)/x', 0), ('sin(3x)/x', 0), ('(x² - 4)/(x - 2)', 2), ('ln(x)/(x - 1)', 1), ('(1 - cos(x))/x²', 0), ('x/e^x', sp.oo), ('ln(x)/x', sp.oo), ('(3x² + 1)/(e^x)', sp.oo), ('(e^(2x) - 1)/sin(x)', 0), ('(x - 1)/ln(x)', 1)]
    picks = rng.sample(pool, 3)
    parts = []
    for i, (e, a) in enumerate(picks):
        fe = P(e)
        L = sp.limit(fe, x, a)
        num, den = sp.fraction(sp.together(fe))
        nd, dd = sp.diff(num, x), sp.diff(den, x)
        at = '∞' if a == sp.oo else n(a)
        form = '∞/∞' if a == sp.oo else '0/0'
        parts.append((f'Find lim (x → {at}) {e}. Name the indeterminate form before using L\'Hôpital\'s Rule.', f'{n(L)} ({form})',
                      f'Direct substitution gives {form}. Differentiate top and bottom separately: lim ({bt(nd)})/({bt(dd)}) = {n(L)}' + (' (apply the rule again if the form is still indeterminate).' if sp.limit(nd, x, a) in (0, sp.oo) else '.'), 2,
                      '1 point for checking the indeterminate form, 1 point for the limit.'))
    parts.append(('Explain why L\'Hôpital\'s Rule cannot be used for lim (x → 0) (x + 1)/(x + 2), and find the limit.', '1/2; the form is 1/2, not indeterminate',
                  'Substitution gives 1/2, which is not 0/0 or ∞/∞, so the rule does not apply; the limit is 1/2.', 1, 'the reason and the value.'))
    return "Evaluate each limit.", parts, None


# ---------------------------------------------------------------- 20. implicit differentiation
def t_implicit(lv, rng):
    Y = sp.Symbol('y')
    k, (px, py) = rng.choice([(7, (1, 2)), (13, (1, 3)), (19, (2, 3)), (7, (2, 1)), (21, (1, 4))])
    F = x ** 2 + x * Y + Y ** 2 - k
    dy = -sp.diff(F, x) / sp.diff(F, Y)
    m = dy.subs({x: px, Y: py})
    hx = sp.sqrt(sp.Rational(k, 3))
    stem = f'Consider the curve x² + xy + y² = {k}.'
    parts = [
        ('Show that dy/dx = −(2x + y)/(x + 2y).', 'dy/dx = −(2x + y)/(x + 2y)', '2x + y + x·dy/dx + 2y·dy/dx = 0, so (x + 2y)dy/dx = −(2x + y).', 2, '1 point for the product rule on xy, 1 point for solving for dy/dx.'),
        (f'Write an equation of the line tangent to the curve at ({px}, {py}).', line(m, px, py), f'Slope at ({px}, {py}): −(2·{px} + {py})/({px} + 2·{py}) = {n(m)}.', 2, '1 point for the slope, 1 point for the line.'),
        ('Find the points on the curve where the tangent line is horizontal. Explain how you found them.', f'({bt(hx)}, {bt(-2 * hx)}) and ({bt(-hx)}, {bt(2 * hx)})',
         f'dy/dx = 0 when y = −2x. Substitute: x² − 2x² + 4x² = 3x² = {k}, so x = ±{bt(hx)}.', 3, '1 point for y = −2x, 1 point for substituting into the curve, 1 point for both points.'),
    ]
    if lv != 'honors':
        parts.append(('Find dy/dx at each point of the curve where x = 0.', '−1/2 at both points', f'At x = 0, y² = {k}, so y = ±{bt(sp.sqrt(k))}; dy/dx = −y/(2y) = −1/2 at both.', 1, 'both points and the slope.'))
    if lv == 'honors':
        d2 = sp.simplify(sp.diff(dy, x) + sp.diff(dy, Y) * dy).subs({x: px, Y: py})
        parts.append((f'Find d²y/dx² at ({px}, {py}).', n(sp.nsimplify(d2)), 'Differentiate dy/dx with the quotient rule, replace dy/dx, and substitute the point.', 2, '1 point for the quotient rule with dy/dx, 1 point for the value.'))
    return stem, parts, None


# ---------------------------------------------------------------- 21. derivative of an inverse function
def t_inverse(lv, rng):
    a, c = rng.choice([(1, 1), (2, 1), (1, 3), (3, 1)])
    fe = x ** 3 + a * x + c
    x0 = rng.choice([1, 2, -1])
    y0 = fe.subs(x, x0)
    fp = sp.diff(fe, x).subs(x, x0)
    gp = sp.Rational(1, fp)
    stem = f'Let f(x) = {bt(fe)}, and let g be the inverse function of f.'
    parts = [
        ('Explain why f has an inverse function.', 'f′(x) > 0 for all x, so f is increasing and one-to-one', f'f′(x) = 3x² + {a} > 0 for every x.', 1, 'f′ > 0 (or f one-to-one) as the reason.'),
        (f'Find g({n(y0)}).', str(x0), f'f({x0}) = {n(y0)}, so g({n(y0)}) = {x0}.', 1, 'the value.'),
        (f'Find g′({n(y0)}).', n(gp), f'g′({n(y0)}) = 1/f′(g({n(y0)})) = 1/f′({x0}) = 1/{n(fp)}.', 2, '1 point for the inverse derivative formula, 1 point for the value.'),
        (f'Write an equation of the line tangent to the graph of g at x = {n(y0)}.', line(gp, y0, x0), f'Point ({n(y0)}, {x0}), slope {n(gp)}.', 1, 'the line.'),
    ]
    return stem, parts, None


# ---------------------------------------------------------------- 22. derivative rules from a table (chain, product, quotient)
def t_rules(lv, rng):
    while True:
        F = [rng.randint(-3, 5) for _ in range(3)]
        G = [rng.randint(1, 3) for _ in range(3)]
        Fp = [rng.randint(-4, 4) for _ in range(3)]
        Gp = [rng.randint(-3, 3) for _ in range(3)]
        h1, p2 = Fp[G[0] - 1] * Gp[0], Fp[1] * G[1] + F[1] * Gp[1]
        if 0 not in G and h1 and p2 and Fp[1] * G[1] - F[1] * Gp[1]:
            break
    vals = {k + 1: (F[k], G[k], Fp[k], Gp[k]) for k in range(3)}
    a = 1
    ga = G[a - 1]
    h1 = Fp[ga - 1] * Gp[a - 1]
    p2 = Fp[1] * G[1] + F[1] * Gp[1]
    q3 = sp.Rational(Fp[1] * G[1] - F[1] * Gp[1], G[1] ** 2)
    table = '; '.join(f'f({k}) = {v[0]}, g({k}) = {v[1]}, f′({k}) = {v[2]}, g′({k}) = {v[3]}' for k, v in vals.items())
    stem = f'Differentiable functions f and g have these values: {table}.'
    parts = [
        ('Let h(x) = f(g(x)). Find h′(1).', str(h1), f'Chain rule: h′(1) = f′(g(1))·g′(1) = f′({ga})·({Gp[0]}) = {Fp[ga - 1]}·({Gp[0]}) = {h1}.', 2, '1 point for the chain rule, 1 point for the value.'),
        ('Let p(x) = f(x)g(x). Find p′(2).', str(p2), f'Product rule: f′(2)g(2) + f(2)g′(2) = ({Fp[1]})({G[1]}) + ({F[1]})({Gp[1]}) = {p2}.', 2, '1 point for the product rule, 1 point for the value.'),
        ('Let q(x) = f(x)/g(x). Find q′(2).', n(q3), f'Quotient rule: (f′(2)g(2) − f(2)g′(2))/g(2)² = ({Fp[1] * G[1]} − ({F[1] * Gp[1]}))/{G[1] ** 2} = {n(q3)}.', 2, '1 point for the quotient rule, 1 point for the value.'),
        ('Is the graph of p increasing or decreasing at x = 2? Give a reason.', 'increasing' if p2 > 0 else ('decreasing' if p2 < 0 else 'neither: p′(2) = 0'),
         f'p′(2) = {p2}.', 1, 'the sign of p′(2) as the reason.'),
    ]
    return stem, parts, None


# ---------------------------------------------------------------- 23. antiderivatives and initial conditions
def t_antideriv(lv, rng):
    if lv == 'honors':
        fp, x0 = rng.choice([('6x² - 4x + 3', 1), ('e^x + 2x', 0), ('3cos(x) + 1', 0), ('4/x + 2', 1), ('2e^(2x) - 1', 0), ('1/x + 3x²', 1), ('2sin(x) + 4x', 0)])
        y0 = rng.randint(1, 6)
    else:
        while True:
            A, B, Cc = rng.randint(0, 3), rng.randint(-3, 3), rng.randint(-5, 5)
            if A or B:
                break
        fp = bt(3 * A * x ** 2 + 2 * B * x + Cc)
        x0, y0 = rng.choice([0, 1, 2]), rng.randint(-3, 6)
    fpe = P(fp)
    F = sp.integrate(fpe, x)
    C = y0 - F.subs(x, x0)
    sol = sp.simplify(F + C)
    a, b = (x0, x0 + 2)
    defi = sp.integrate(fpe, (x, a, b))
    stem = f'The function f satisfies f′(x) = {fp} and f({x0}) = {y0}.'
    parts = [
        ('Find the general antiderivative of f′(x).', bt(F) + ' + C', 'Power rule (and the basic rules) term by term, plus C.', 1, 'the antiderivative with + C.'),
        ('Find f(x).', f'f(x) = {bt(sol)}', f'f({x0}) = {y0} gives C = {n(C)}.', 2, '1 point for using the initial condition, 1 point for f(x).'),
        (f'Find ∫ from {a} to {b} f′(x) dx and explain what it tells you about f.', f'{n(defi)}; f({b}) − f({a}) = {n(defi)}',
         f'By the Fundamental Theorem, the integral of f′ is the net change in f: f({b}) − f({a}) = {n(sp.simplify(sol.subs(x, b) - sol.subs(x, a)))}.', 2, '1 point for the value, 1 point for the net-change interpretation.'),
        (f'Find the average value of f′ on [{a}, {b}].', bt(sp.simplify(defi / (b - a))), f'(1/({b} − {a}))∫ from {a} to {b} f′(x) dx = {bt(sp.simplify(defi / (b - a)))}.', 1, 'the average value.'),
    ]
    return stem, parts, None


# ---------------------------------------------------------------- 24. u-substitution
def t_subst(lv, rng):
    if lv == 'honors':
        e, u, du, Fs, a, b = rng.choice([('x·e^(x²)', 'x²', '2x dx', '(1/2)e^(x²)', 0, 1), ('cos(x)·sin³(x)', 'sin(x)', 'cos(x) dx', '(1/4)sin⁴(x)', 0, sp.pi / 2),
                                         ('ln(x)/x', 'ln(x)', '(1/x) dx', '(1/2)(ln(x))²', 1, sp.E), ('x/(x² + 1)', 'x² + 1', '2x dx', '(1/2)ln(x² + 1)', 0, 1)])
    else:
        e, u, du, Fs, a, b = rng.choice([('2x(x² + 1)³', 'x² + 1', '2x dx', '(1/4)(x² + 1)⁴', 0, 1), ('3x²(x³ - 1)⁴', 'x³ - 1', '3x² dx', '(1/5)(x³ - 1)⁵', 1, 2),
                                         ('x(x² + 4)²', 'x² + 4', '2x dx', '(1/6)(x² + 4)³', 0, 2), ('6x²(2x³ + 1)²', '2x³ + 1', '6x² dx', '(1/3)(2x³ + 1)³', 0, 1)])
    sym = {'x·e^(x²)': x * sp.exp(x ** 2), 'cos(x)·sin³(x)': sp.cos(x) * sp.sin(x) ** 3, 'ln(x)/x': sp.log(x) / x, 'x/(x² + 1)': x / (x ** 2 + 1)}
    fe = sym.get(e) or P(e)
    ue = P(u)
    Fsym = {'(1/2)e^(x²)': sp.exp(x ** 2) / 2, '(1/4)sin⁴(x)': sp.sin(x) ** 4 / 4, '(1/2)(ln(x))²': sp.log(x) ** 2 / 2, '(1/2)ln(x² + 1)': sp.log(x ** 2 + 1) / 2}
    F = Fsym.get(Fs) or P(Fs)
    assert sp.simplify(sp.diff(F, x) - fe) == 0, e
    val = sp.simplify(sp.integrate(fe, (x, a, b)))
    stem = f'Consider ∫ {e} dx.'
    ua, ub = sp.simplify(ue.subs(x, a)), sp.simplify(ue.subs(x, b))
    parts = [
        ('Choose u and write du in terms of dx.', f'u = {u}; du = {du}', 'Pick the inside function whose derivative appears as a factor.', 1, 'u and du.'),
        ('Find the indefinite integral.', Fs + ' + C', f'Rewrite in u, integrate, and substitute u = {u} back.', 2, '1 point for the integral in u, 1 point for the answer in x with + C.'),
        (f'Evaluate ∫ from {bt(a)} to {bt(b)} {e} dx by changing the limits of integration to u-values.', f'{bt(val)}',
         f'x = {bt(a)} gives u = {bt(ua)}; x = {bt(b)} gives u = {bt(ub)}. Evaluate the u-antiderivative from {bt(ua)} to {bt(ub)}: {bt(val)}.', 2, '1 point for the new limits, 1 point for the value.'),
        ('Explain why the limits of integration change in part (c).', 'the integral is now in u, so the limits must be u-values', 'After substitution the variable of integration is u.', 1, 'the reason.'),
    ]
    return stem, parts, None


# ---------------------------------------------------------------- 25. long division and completing the square
def t_division(lv, rng):
    c = rng.choice([1, 2, 3])
    num = sp.expand((x + c) * (x - 1) + rng.choice([2, 3, 5]))
    rd = sp.div(num, x + c)
    I1 = sp.integrate(num / (x + c), x)
    h, k = rng.choice([(1, 2), (2, 3), (1, 1), (3, 2)])
    den2 = sp.expand((x + h) ** 2 + k ** 2)
    I2 = sp.integrate(1 / den2, x)
    d = sp.simplify(sp.integrate(1 / den2, (x, -h, -h + k)))
    stem = 'Evaluate each integral.'
    parts = [
        (f'Use long division to rewrite ({bt(num)})/(x + {c}).', f'{bt(rd[0])} + {bt(rd[1])}/(x + {c})', f'Quotient {bt(rd[0])}, remainder {bt(rd[1])}.', 1, 'the quotient and the remainder term.'),
        (f'Find ∫ ({bt(num)})/(x + {c}) dx.', f'{bt(sp.integrate(rd[0], x))} + {bt(rd[1])}ln|x + {c}| + C',
         'Integrate term by term; the remainder term gives a natural log.', 2, '1 point for the polynomial part, 1 point for the ln term with + C.'),
        (f'Complete the square in {bt(den2)}, then find ∫ 1/({bt(den2)}) dx.', f'(x + {h})² + {k * k}; ' + (f'(1/{k})' if k != 1 else '') + (f'arctan((x + {h})/{k})' if k != 1 else f'arctan(x + {h})') + ' + C',
         f'{bt(den2)} = (x + {h})² + {k * k}; ∫ du/(u² + a²) = (1/a)arctan(u/a) + C.', 3, '1 point for completing the square, 1 point for the arctan form, 1 point for the constant 1/a.'),
        (f'Evaluate ∫ from {-h} to {-h + k} 1/({bt(den2)}) dx.', bt(d), f'(1/{k})[arctan(1) − arctan(0)] = {bt(d)}.', 1, 'the exact value.'),
    ]
    return stem, parts, None


# ---------------------------------------------------------------- 26. average value
def t_avg(lv, rng):
    if lv == 'honors':
        T, a, b = rng.choice([('20 + 10sin(πt/12)', 0, 12), ('60 - 8e^(-t/2)', 0, 4), ('15 + 6cos(πt/6)', 0, 3)])
    else:
        T, a, b = rng.choice([('t² - 4t + 10', 0, 6), ('3t² - 12t + 20', 0, 4), ('40 - 2t', 0, 10), ('t² + 2t + 5', 0, 3)])
    te = P(T)
    avg = sp.simplify(sp.integrate(te, (t, a, b)) / (b - a))
    cs = [r for r in sp.solveset(sp.Eq(te, avg), t, sp.Interval(a, b))] if lv != 'honors' else []
    stem = f'The temperature in a greenhouse is T(t) = {T} degrees Celsius, t hours after 6 a.m., for {a} ≤ t ≤ {b}.'
    parts = [
        (f'Find the average temperature from t = {a} to t = {b}.', f'{bt(avg)} °C' + ('' if avg.is_Rational else f' ≈ {float(avg):.2f} °C'),
         f'(1/({b} − {a}))∫ from {a} to {b} T(t) dt = {bt(avg)}.', 2, '1 point for 1/(b − a) times the integral, 1 point for the value.'),
        ('Must there be a time in the interval when the temperature equals the average? Justify your answer.', 'Yes',
         'T is continuous on the closed interval, so by the Mean Value Theorem for Integrals (or the IVT between its minimum and maximum) T takes its average value.', 2, '1 point for continuity, 1 point for the theorem.'),
        (f'Find the average rate of change of T from t = {a} to t = {b}, and explain how it differs from the answer to part (a).',
         f'{bt(sp.simplify((te.subs(t, b) - te.subs(t, a)) / (b - a)))} °C per hour; part (a) is an average temperature, this is an average rate of change',
         f'(T({b}) − T({a}))/({b} − {a}).', 2, '1 point for the value with units, 1 point for the distinction.'),
    ]
    if not cs:
        d1 = sp.diff(te, t).subs(t, 1)
        parts.insert(2, ('Is the temperature increasing or decreasing at t = 1? Justify your answer.', 'increasing' if d1 > 0 else 'decreasing', f'T′(1) = {bt(sp.simplify(d1))} ≈ {float(d1):.3f}.', 1, 'the sign of T′(1).'))
    if cs:
        parts.insert(2, ('Find the time(s) when T(t) equals its average value.', ', '.join(f't = {bt(r)}' for r in sorted(cs, key=float)), f'Solve {T} = {bt(avg)}.', 1, 'the time(s).'))
    return stem, parts, None


# ---------------------------------------------------------------- 27. derivative of an accumulation function (FTC part 1)
def t_ftc1(lv, rng):
    if lv == 'honors':
        g, up, a0 = rng.choice([('√(1 + t³)', 'x²', 1), ('e^(-t²)', '3x', 0), ('cos(t²)', '2x', 0)])
    else:
        g, up, a0 = rng.choice([('t² + 1', 'x', 1), ('√(t + 3)', 'x', 1), ('t³ - 2t', 'x²', 0), ('(t + 1)²', 'x', 2)])
    ge, ue = P(g).subs(x, t) if 't' in g else P(g), P(up)
    ge = P(g.replace('t', 'x')).subs(x, t)
    F = sp.Integral(ge, (t, a0, ue))
    Fp = sp.simplify(ge.subs(t, ue) * sp.diff(ue, x))
    xs = sp.solve(sp.Eq(ue, a0), x)
    x0 = min([r for r in xs if r.is_real], key=lambda r: abs(float(r)))
    m = sp.simplify(Fp.subs(x, x0))
    stem = f'Let F(x) = ∫ from {a0} to {up} ' + (f'({g})' if (' + ' in g or ' - ' in g) and not g.startswith('(') and not g.startswith('√') else g) + ' dt.'
    parts = [
        ('Find F′(x).', f"F′(x) = {bt(Fp)}", f'Fundamental Theorem, part 1' + ('' if up == 'x' else f', with the chain rule: g({up})·({bt(sp.diff(ue, x))})') + '.', 2, '1 point for substituting the upper limit, 1 point for the chain-rule factor (or the result).'),
        (f'Find F({bt(x0)}) and F′({bt(x0)}).', f'F({bt(x0)}) = 0; F′({bt(x0)}) = {bt(m)}', f'At x = {bt(x0)} the limits are equal, so F = 0.', 2, '1 point for each value.'),
        (f'Write an equation of the line tangent to the graph of F at x = {bt(x0)}.', line(m, x0, 0), f'Point ({bt(x0)}, 0), slope {bt(m)}.', 1, 'the line.'),
        (f'Is F increasing or decreasing at x = {bt(x0 + 1)}? Justify your answer.', 'increasing' if Fp.subs(x, x0 + 1) > 0 else 'decreasing',
         f'F′({bt(x0 + 1)}) = {bt(sp.simplify(Fp.subs(x, x0 + 1)))}' + ('' if sp.simplify(Fp.subs(x, x0 + 1)).is_Rational else f' ≈ {float(Fp.subs(x, x0 + 1)):.3f}') + '.', 1, 'the sign of F′.'),
    ]
    return stem, parts, None

# ---------------------------------------------------------------- 11b. converting between Riemann sums and integrals
def t_rnotation(lv, rng):
    pool = [('x²', 0, 2), ('x³', 0, 1), ('√x', 0, 4), ('2x + 1', 1, 3), ('x² + 1', 0, 3)] if lv != 'honors' else [('√x', 1, 4), ('e^x', 0, 1), ('1/x', 1, 3), ('sin(x)', 0, sp.pi)]
    f, a, b = rng.choice(pool)
    g, a2, b2 = rng.choice([p for p in pool if p[0] != f])
    fe, ge = P(f), P(g)
    w = b - a
    inside = (f'{bt(a)} + ' if a else '') + (f'{bt(w)}k/n' if w != 1 else 'k/n')
    term = f.replace('x', f'({inside})')
    v1 = sp.integrate(fe, (x, a, b))
    w2 = b2 - a2
    in2 = (f'{bt(a2)} + ' if a2 else '') + (f'{bt(w2)}k/n' if w2 != 1 else 'k/n')
    stem = f'The limit L = lim (n → ∞) Σ (k = 1 to n) [{term}]·({bt(w)}/n) is a right Riemann sum.'
    parts = [
        ('Identify Δx and the right endpoint xₖ.', f'Δx = {bt(w)}/n; xₖ = {inside}', f'The factor {bt(w)}/n is the width; the expression inside f is the kth right endpoint.', 1, 'Δx and xₖ.'),
        ('Write L as a definite integral.', f'∫ from {bt(a)} to {bt(b)} {f} dx', f'x₀ = {bt(a)}, and the width {bt(w)} = b − a gives b = {bt(b)}.', 2, '1 point for the integrand, 1 point for the limits.'),
        ('Evaluate L.', bt(v1), f'Antiderivative and the Fundamental Theorem: {bt(v1)}.', 1, 'the value.'),
        (f'Write ∫ from {bt(a2)} to {bt(b2)} {g} dx as the limit of a right Riemann sum.', f'lim (n → ∞) Σ (k = 1 to n) [{g.replace("x", f"({in2})")}]·({bt(w2)}/n)',
         f'Δx = {bt(w2)}/n and xₖ = {in2}.', 2, '1 point for Δx, 1 point for f(xₖ) with the limit and sum.'),
    ]
    return stem, parts, None


MAP = {
    'precalculus-review': {1: t_algebra, 2: t_precalc, 3: t_log, 4: t_trig, 5: t_table},
    'limits-continuity': {1: t_piecewise, 2: t_piecewise, 3: t_limits, 4: t_piecewise, 5: t_limits, 6: t_piecewise, 7: t_limits, 8: t_theorems},
    'derivatives': {1: t_tangent, 2: t_table, 3: t_rules, 4: t_motion, 5: t_piecewise, 6: t_tangent, 7: t_analysis, 8: t_rules, 9: t_implicit, 10: t_inverse},
    'applications-derivatives': {1: t_context, 2: t_analysis, 3: t_analysis, 4: t_analysis, 5: t_analysis, 6: t_related, 7: t_optim, 8: t_motion, 9: t_context, 10: t_theorems, 11: t_tangent, 12: t_lhop},
    'antiderivatives-definite-integrals': {1: t_antideriv, 2: t_antideriv, 3: t_riemann, 4: t_rnotation, 5: t_table, 6: t_accum, 7: t_accum},
    'fundamental-theorem-calculus': {1: t_ftc1, 2: t_accum, 3: t_accum, 4: t_ftc1, 5: t_antideriv, 6: t_subst, 7: t_division},
    'applications-integrals': {1: t_context, 2: t_table, 3: t_avg, 4: t_motion, 5: t_motion, 6: t_region, 7: t_region, 8: t_table},
    'differential-equations': {1: t_de, 2: t_de, 3: t_de, 4: t_de, 5: t_de, 6: t_de},
    'ap-review': {1: t_piecewise, 2: t_analysis, 3: t_accum, 4: t_de, 5: t_table, 6: t_theorems, 7: t_context},
}


def main():
    import subprocess, json
    names = json.loads(subprocess.run(['node', '-e', "require(process.argv[1]);const C=globalThis.MK_COURSE_CATALOG,o={};for(const u of require(process.argv[2]).banks.filter(b=>b.courseId==='calculus'))C.getSkillRecords('calculus',u.unitId).forEach(s=>o[s.id]=s.name);console.log(JSON.stringify(o))",
                                       os.path.join(lib.ROOT, 'course-catalog.js'), os.path.join(lib.ROOT, 'question-banks/manifest.json')], capture_output=True, text=True, check=True).stdout)
    banks = lib.load()
    cnt = 0
    seen = set()
    for u, d in banks.items():
        for i, q in enumerate(d['questions']):
            if q['format'] != 'open-response' or not q['id'].endswith('-015'):
                continue
            k = int(re.search(r'skill-(\d+)', q['skillId']).group(1))
            fn = MAP[u][k]
            for attempt in range(40):
                rng = random.Random(f'cal-audit-5-{q["id"]}-{attempt}')
                stem, parts, diagram = fn(q['level'], rng, q['id'], u) if fn is t_accum else fn(q['level'], rng)
                sig = stem + '|' + parts[0][0] + '|' + str(diagram and diagram['spec']['alt'])
                if sig not in seen:
                    break
            seen.add(sig)
            new = frq(q, names[q['skillId']], stem, parts, diagram, fam='frq_' + fn.__name__[2:])
            new['standards'] = q['standards']
            d['questions'][i] = new
            cnt += 1
    lib.save(banks)
    print('free-response problems', cnt)


if __name__ == '__main__':
    main()
