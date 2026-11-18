"""Calculus audit #8 (2026-11-18): items that practice what their skill names.

- Converting Riemann Sums to Integral Notation (antiderivatives skill 04): the 36 finite Riemann-sum items
  become limit-of-sum items: evaluate a limit by writing it as an integral, pick the limit that equals an
  integral, find a missing limit of integration; with matching find-the-mistake and practice-set items.
- Analyzing Functions Defined by Integrals (FTC skill 03): the 27 items copied from skill 02 become
  g(x) = ∫ from a to x f(t) dt analysis from a formula (increasing, extrema, concavity, g′ and g″).
- Definite Integrals as Limits of Riemann Sums (antiderivatives skill 03): items 001-004 at each level use a
  limit of a Riemann sum instead of a finite sum.
Deterministic (seeded by item id) and idempotent.
"""
import math, random, re, sys, os
from fractions import Fraction as F
sys.path.insert(0, os.path.dirname(__file__))
import lib
from author import fr, par, poly, peval, pint, pdiff, interval, union, mc, record, error_item, open_set

NAMES = ['Ava', 'Ben', 'Chloe', 'Dev', 'Elena', 'Femi', 'Hiro', 'Isla', 'Kai', 'Lena', 'Marco', 'Nia', 'Omar', 'Priya', 'Quinn', 'Rosa', 'Sam', 'Tariq', 'Uma', 'Vic', 'Wren', 'Yusuf', 'Zoe']
CONV = ['AP LIM-5.B', 'AP LIM-5.C']
LIMSUM = ['AP LIM-5.A', 'AP LIM-5.B']
ACC = ['AP FUN-5.A', 'AP FUN-4.A']

# ---------------------------------------------------------------- converting Riemann sums (int skill 04)
# an integrand: text with {u} for the inside, a function value, an antiderivative value, a text for f(x)


def integrand(kind, c=1):
    if kind == 'x':
        return dict(tpl=('{c}{u}' if c != 1 else '{u}'), f='x' if c == 1 else f'{c}x', F=lambda x: F(c) * F(x) ** 2 / 2, Ft=poly({2: F(c, 2)}))
    if kind == 'x2':
        return dict(tpl='{u}²', f='x²', F=lambda x: F(x) ** 3 / 3, Ft='(1/3)x³')
    if kind == 'x3':
        return dict(tpl='{u}³', f='x³', F=lambda x: F(x) ** 4 / 4, Ft='(1/4)x⁴')
    if kind == 'x2c':
        return dict(tpl='({u}² + ' + str(c) + ')', f=f'x² + {c}', F=lambda x: F(x) ** 3 / 3 + c * F(x), Ft=poly({3: F(1, 3), 1: c}))
    if kind == 'sqrt':
        return dict(tpl='√{u}', f='√x', F=lambda x: F(2, 3) * F(x) * F(round(math.sqrt(x))), Ft='(2/3)x√x')
    raise ValueError(kind)


def inside(a, w, left=False):
    k = '(k - 1)' if left else 'k'
    step = f'{k}/n' if w == 1 else f'{w}{k}/n'
    if a == 0:
        return '(' + step + ')'
    return f'({a} + {step})' if a > 0 else f'({a} + {step})'


def sumtext(g, a, w, left=False):
    u = inside(a, w, left)
    body = g['tpl'].replace('{c}', '' if '{c}' not in g['tpl'] else '').replace('{u}', u)
    if '{c}' in g['tpl']:
        pass
    lo = '1'
    dx = '(1/n)' if w == 1 else f'({w}/n)'
    return f'lim (n → ∞) Σ (k = {lo} to n) {body} · {dx}'


def conv_params(level, rng, i):
    if level == 'cp2':
        kind = ['x', 'x2', 'x', 'x2'][i % 4]
        c = rng.choice([2, 3, 4]) if kind == 'x' else 1
        return kind, c, 0, rng.choice([2, 3, 4]), False
    if level == 'cp1':
        kind = ['x2', 'x2c', 'x', 'x2'][i % 4]
        c = rng.choice([1, 2, 3]) if kind != 'x2' else 1
        return kind, c, rng.choice([1, 2]), rng.choice([1, 2, 3]), False
    kind = ['sqrt', 'x3', 'x2c', 'sqrt'][i % 4]
    c = rng.choice([1, 2, 4])
    if kind == 'sqrt':
        a, b = rng.choice([(1, 4), (4, 9), (1, 9), (0, 4)])
        return kind, 1, a, b - a, rng.random() < 0.5
    return kind, c, rng.choice([0, 1, 2]), rng.choice([1, 2]), rng.random() < 0.5


def tpl_with_c(kind, c):
    g = integrand(kind, c)
    if kind == 'x':
        g['tpl'] = ('' if c == 1 else str(c)) + '{u}'
    return g


def conv_value(g, a, w):
    return g['F'](a + w) - g['F'](a)


def conv_steps(g, a, w, left):
    b = a + w
    dx = f'Δx = {w}/n' if w != 1 else 'Δx = 1/n'
    start = f'xₖ = {a} + {"(k − 1)" if left else "k"}Δx' if a else f'xₖ = {"(k − 1)" if left else "k"}Δx'
    return [f'{dx}, so the interval has width b − a = {w}.',
            f'{start} starts at x = {a}{" (left endpoints, k − 1)" if left else ""}, so a = {a} and b = {a} + {w} = {b}.',
            f'The function applied to xₖ is f(x) = {g["f"]}, so the limit equals ∫ from {a} to {b} {g["f"] if len(g["f"]) < 3 or g["f"].startswith("√") else "(" + g["f"] + ")"} dx.',
            f'Antiderivative: F(x) = {g["Ft"]}. F({b}) = {fr(g["F"](b))} and F({a}) = {fr(g["F"](a))}.',
            f'{fr(g["F"](b))} − {par(g["F"](a))} = {fr(conv_value(g, a, w))}.']


def intg(g):
    return g['f'] if (len(g['f']) <= 2 or g['f'].startswith('√')) else '(' + g['f'] + ')'


def conv_item(q, i, rng, name):
    lv, slot = q['level'], int(q['id'][-3:])
    kind, c, a, w, left = conv_params(lv, rng, i)
    g = tpl_with_c(kind, c)
    b = a + w
    s = sumtext(g, a, w, left)
    val = conv_value(g, a, w)
    if slot == 15:
        parts = []
        for j in range(4):
            kind2, c2, a2, w2, l2 = conv_params(lv, rng, i + j + 1)
            g2 = tpl_with_c(kind2, c2)
            v2 = conv_value(g2, a2, w2)
            parts.append((f'Evaluate {sumtext(g2, a2, w2, l2)} by writing it as a definite integral.', fr(v2),
                          f'∫ from {a2} to {a2 + w2} {intg(g2)} dx = {fr(g2["F"](a2 + w2))} − {par(g2["F"](a2))} = {fr(v2)}.'))
        return open_set(q, 'conv_open', 'Converting Riemann Sums to Integral Notation', parts)
    if slot in (14, 16):
        if a == 0:
            wrong = g['F'](1) - g['F'](0)
            mistake = f'Used Δx = 1/n and the interval [0, 1]. The factor ({w}/n) means Δx = {w}/n, so the interval is [0, {w}].'
        else:
            wrong = g['F'](w) - g['F'](0)
            mistake = f'Used the interval [0, {w}]. The sum starts at x = {a}, so the interval is [{a}, {b}].'
        if wrong == val:
            wrong = val * 2
            mistake = 'Doubled the antiderivative value; evaluate F(b) − F(a) once.'
        return error_item(q, 'conv_eval_error', name, f'Evaluate {s} by writing it as a definite integral.', fr(wrong), fr(val), mistake,
                          conv_steps(g, a, w, left), CONV)
    if q['format'] == 'multiple-choice':
        right = f'lim (n → ∞) Σ (k = 1 to n) {g["tpl"].replace("{u}", inside(a, w))} · ({w}/n)'
        d1 = f'lim (n → ∞) Σ (k = 1 to n) {g["tpl"].replace("{u}", inside(a, w))} · (1/n)' if w != 1 else f'lim (n → ∞) Σ (k = 1 to n) {g["tpl"].replace("{u}", inside(a, 2))} · (1/n)'
        d2 = f'lim (n → ∞) Σ (k = 1 to n) {g["tpl"].replace("{u}", inside(a, 1 if w != 1 else 2))} · ({w}/n)'
        d3 = f'lim (n → ∞) Σ (k = 1 to n) {g["tpl"].replace("{u}", inside(b if a == 0 else 0, w))} · ({w}/n)'
        right = right.replace('(1/n)', '(1/n)')
        opts = mc(rng, right, [d1, d2, d3])
        return record(q, 'conv_to_sum', f'Which limit of a right Riemann sum equals ∫ from {a} to {b} {intg(g)} dx?', right,
                      [f'Δx = (b − a)/n = {w}/n.', f'Right endpoints: xₖ = {a} + k·Δx = {inside(a, w)[1:-1]}.',
                       f'The sum is Σ f(xₖ)Δx with f(x) = {g["f"]}, so the term is {g["tpl"].replace("{u}", inside(a, w))} · ({w}/n).',
                       'The other choices use the wrong Δx, the wrong step inside f, or the wrong starting point.'],
                      fmt='multiple-choice', options=opts, standards=CONV)
    if slot % 3 == 0:
        return record(q, 'conv_find_b', f'{s} = ∫ from {a} to b {intg(g)} dx. Find b.', str(b),
                      [f'The factor ({w}/n) is Δx, so b − a = {w}.' if w != 1 else 'The factor (1/n) is Δx, so b − a = 1.',
                       f'The inside starts at x = {a}, so a = {a}.', f'b = {a} + {w} = {b}.'], standards=CONV)
    return record(q, 'conv_eval', f'Evaluate {s} by writing it as a definite integral.', fr(val), conv_steps(g, a, w, left), standards=CONV)


# ---------------------------------------------------------------- analyzing g(x) = ∫ from a to x f(t) dt (FTC skill 03)


def fpoly(level, rng):
    s = rng.choice([1, -1])
    if level == 'cp2':
        r = rng.choice([-3, -2, -1, 1, 2, 3, 4])
        m = rng.choice([1, 2, 3])
        return {1: s * m, 0: -s * m * r}, [r], s
    r1 = rng.choice([-4, -3, -2, -1, 0, 1])
    r2 = r1 + rng.choice([2, 3, 4, 5])
    m = 1 if level == 'cp1' else rng.choice([1, 2])
    return {2: s * m, 1: -s * m * (r1 + r2), 0: s * m * r1 * r2}, [r1, r2], s


def sign_intervals(roots, s, positive=True):
    """Intervals where a polynomial with these simple roots and leading sign s is positive (or negative)."""
    pts = ['-oo'] + roots + ['oo']
    out = []
    n = len(roots)
    for i in range(len(pts) - 1):
        sign = s * (-1) ** (n - i)   # sign on the i-th interval from the left
        if (sign > 0) == positive:
            out.append(interval(pts[i], pts[i + 1]))
    return out


def acc_item(q, i, rng, name):
    lv, slot = q['level'], int(q['id'][-3:])
    co, roots, s = fpoly(lv, rng)
    a = rng.choice([-1, 0, 1, 2])
    ft = poly(co, 't')
    g = f'g(x) = ∫ from {a} to x ({ft}) dt'
    inc = union(sign_intervals(roots, s, True))
    dec = union(sign_intervals(roots, s, False))
    d1 = pdiff(co)
    vertex = -F(d1.get(0, 0)) / d1[1] if 1 in d1 else None
    cu = union([interval(vertex, 'oo') if d1.get(1, 0) > 0 else interval('-oo', vertex)]) if vertex is not None else 'none'
    cdn = union([interval('-oo', vertex) if d1.get(1, 0) > 0 else interval(vertex, 'oo')]) if vertex is not None else 'none'
    maxx = [r for r in roots if (s * (-1) ** (len(roots) - roots.index(r))) > 0]   # f changes + to - at r
    minx = [r for r in roots if r not in maxx]
    base_steps = [f'By the Fundamental Theorem of Calculus, g′(x) = {poly(co, "x")}.']
    fact = ''.join(f'(x {"-" if r >= 0 else "+"} {abs(r)})' if r else 'x' for r in sorted(roots, key=lambda r: r != 0))
    lead = abs(co[max(co)])
    sign_line = f'g′(x) = {"-" if s < 0 else ""}{"" if lead == 1 else lead}{fact}, which is zero at x = {", ".join(map(str, roots))}.'
    if slot == 15:
        parts = []
        for j, kind in enumerate(['inc', 'max' if maxx else 'min', 'gp', 'gpp' if lv != 'cp2' else 'dec']):
            co2, roots2, s2 = fpoly(lv, rng)
            a2 = rng.choice([0, 1])
            f2 = poly(co2, 't')
            p = f'g(x) = ∫ from {a2} to x ({f2}) dt. '
            mx2 = [r for r in roots2 if (s2 * (-1) ** (len(roots2) - roots2.index(r))) > 0]
            if kind == 'inc':
                parts.append((p + 'On what interval(s) is g increasing?', union(sign_intervals(roots2, s2, True)), f'g′(x) = {poly(co2)} > 0 on {union(sign_intervals(roots2, s2, True))}.'))
            elif kind == 'dec':
                parts.append((p + 'On what interval(s) is g decreasing?', union(sign_intervals(roots2, s2, False)), f'g′(x) = {poly(co2)} < 0 on {union(sign_intervals(roots2, s2, False))}.'))
            elif kind in ('max', 'min'):
                mn2 = [r for r in roots2 if r not in mx2]
                if kind == 'max' and mx2:
                    parts.append((p + 'At what x does g have a relative maximum?', f'x = {mx2[0]}', f'g′ = f changes from positive to negative at x = {mx2[0]}.'))
                else:
                    parts.append((p + 'At what x does g have a relative minimum?', f'x = {mn2[0]}', f'g′ = f changes from negative to positive at x = {mn2[0]}.'))
            elif kind == 'gp':
                c = rng.choice([-2, -1, 2, 3])
                parts.append((p + f'Find g′({c}).', fr(peval(co2, c)), f'g′({c}) = f({c}) = {fr(peval(co2, c))}.'))
            else:
                c = rng.choice([-2, -1, 2, 3])
                parts.append((p + f'Find g″({c}).', fr(peval(pdiff(co2), c)), f'g″(x) = f′(x) = {poly(pdiff(co2))}, so g″({c}) = {fr(peval(pdiff(co2), c))}.'))
        return open_set(q, 'acc_formula_open', 'Analyzing Functions Defined by Integrals', parts)
    if slot in (14, 16):
        if vertex is None:
            # linear f: student used where f is increasing (g concave up) instead of where f > 0
            wrong = 'all real numbers' if s > 0 else 'none'
        else:
            wrong = cu
        return error_item(q, 'acc_formula_error', name, f'{g}. On what interval(s) is g increasing?', wrong, inc,
                          'Found where f is increasing (that is where g is concave up). g is increasing where g′ = f is positive.',
                          base_steps + [sign_line, f'g′(x) > 0 on {inc}, so g is increasing there.'], ACC)
    kinds = ['inc', 'dec', 'ext', 'gp', 'cu', 'gpp'] if lv != 'cp2' else ['inc', 'dec', 'ext', 'gp', 'inc', 'gp']
    kind = kinds[(slot // 2) % len(kinds)]
    if kind == 'inc':
        ans, prompt, last = inc, f'{g}. On what interval(s) is g increasing?', f'g′(x) > 0 on {inc}, so g is increasing there.'
        dis = [dec, cu, union([interval(roots[0], 'oo')])]
    elif kind == 'dec':
        ans, prompt, last = dec, f'{g}. On what interval(s) is g decreasing?', f'g′(x) < 0 on {dec}, so g is decreasing there.'
        dis = [inc, cdn, union([interval('-oo', roots[-1])])]
    elif kind == 'ext':
        if maxx:
            ans, prompt, last = f'x = {maxx[0]}', f'{g}. At what x does g have a relative maximum?', f'g′ changes from positive to negative at x = {maxx[0]}, so g has a relative maximum there.'
        else:
            ans, prompt, last = f'x = {minx[0]}', f'{g}. At what x does g have a relative minimum?', f'g′ changes from negative to positive at x = {minx[0]}, so g has a relative minimum there.'
        dis = [f'x = {r}' for r in roots if f'x = {r}' != ans] + [f'x = {a}', f'x = {fr(vertex) if vertex is not None else roots[0] + 1}', f'x = {roots[0] - 1}']
    elif kind == 'gp':
        c = rng.choice([v for v in range(-3, 5) if v != a])
        ans, prompt, last = fr(peval(co, c)), f'{g}. Find g′({c}).', f'g′({c}) = f({c}) = {fr(peval(co, c))}.'
        dis = [fr(peval(pdiff(co), c)), fr(peval(pint(co), c) - peval(pint(co), a)), fr(-peval(co, c)), fr(peval(co, c) + 1)]
    elif kind == 'cu':
        ans, prompt, last = cu, f'{g}. On what interval is g concave up?', f'g″(x) = f′(x) = {poly(d1)} > 0 on {cu}, so g is concave up there.'
        dis = [cdn, inc, dec]
    else:
        c = rng.choice([v for v in range(-3, 5) if v != a])
        ans, prompt, last = fr(peval(d1, c)), f'{g}. Find g″({c}).', f'g″(x) = f′(x) = {poly(d1)}, so g″({c}) = {fr(peval(d1, c))}.'
        dis = [fr(peval(co, c)), fr(-peval(d1, c)), fr(peval(d1, c) + 2), fr(peval(d1, c) * 2)]
    steps = base_steps + ([sign_line] if kind in ('inc', 'dec', 'ext') else []) + [last]
    if q['format'] == 'multiple-choice':
        if kind in ('inc', 'dec', 'cu'):
            dis = dis + ['(-∞, ∞)', interval(roots[0] - 1, 'oo'), interval('-oo', roots[-1] + 1)]
        dis = [x for x in dis if x != 'none']
        return record(q, 'acc_formula', prompt, ans, steps, fmt='multiple-choice', options=mc(rng, ans, dis), standards=ACC)
    return record(q, 'acc_formula', prompt, ans, steps, standards=ACC)


# ---------------------------------------------------------------- limit of a Riemann sum (int skill 03)


def closed_form(level, rng):
    """Returns f text, b, R_n text pieces [(coef, power of 1/n)], limit value."""
    if level == 'cp2':
        c, b = rng.choice([2, 4, 6]), rng.choice([2, 3, 4])
        L = F(c * b * b, 2)
        return f'{c}x', b, [(L, 0), (L, 1)], L, f'the triangle under y = {c}x from 0 to {b}: (1/2)({b})({c * b}) = {fr(L)}'
    if level == 'cp1':
        b = rng.choice([3, 6])
        L = F(b ** 3, 3)
        return 'x²', b, [(L, 0), (F(b ** 3, 2), 1), (F(b ** 3, 6), 2)], L, f'∫ from 0 to {b} x² dx = {b}³/3 = {fr(L)}'
    b = rng.choice([2, 4])
    L = F(b ** 4, 4)
    return 'x³', b, [(L, 0), (F(b ** 4, 2), 1), (L, 2)], L, f'∫ from 0 to {b} x³ dx = {b}⁴/4 = {fr(L)}'


def rn_text(terms):
    out = []
    for c, p in terms:
        if p == 0:
            out.append(fr(c))
        else:
            den = 'n' if p == 1 else 'n²'
            out.append(f'{fr(c)}/{den}' if F(c).denominator == 1 else f'({fr(c)})/{den}')
    return ' + '.join(out)


def limsum_item(q, rng):
    f, b, terms, L, why = closed_form(q['level'], rng)
    rn = rn_text(terms)
    pre = f'For f(x) = {f} on [0, {b}], the right Riemann sum with n equal subintervals simplifies to Rₙ = {rn}.'
    steps = [f'Each term with n in the denominator goes to 0 as n → ∞.', f'So lim (n → ∞) Rₙ = {fr(L)}.',
             f'This limit is the definite integral ∫ from 0 to {b} {f} dx; check: {why}.']
    if q['format'] == 'multiple-choice':
        right = f'lim (n → ∞) Rₙ = {fr(L)}, which equals ∫ from 0 to {b} {f} dx'
        opts = mc(rng, right, [f'lim (n → ∞) Rₙ = {fr(L + terms[1][0])}, which equals ∫ from 0 to {b} {f} dx',
                               f'Rₙ is less than ∫ from 0 to {b} {f} dx for every n',
                               'lim (n → ∞) Rₙ does not exist because Rₙ changes with n'])
        return record(q, 'limsum_closed', pre + ' Which statement is true?', right,
                      steps + [f'f is increasing on [0, {b}], so each right sum overestimates: Rₙ is greater than the integral for every n.'],
                      fmt='multiple-choice', options=opts, standards=LIMSUM)
    return record(q, 'limsum_closed', pre + ' Find lim (n → ∞) Rₙ.', fr(L), steps, standards=LIMSUM)


def main():
    banks = lib.load()
    n = {'conv': 0, 'acc': 0, 'lim': 0}
    for u, d in banks.items():
        out = []
        for q in d['questions']:
            fam = lib.family(q)
            rng = random.Random('cal-audit-8-' + q['id'])
            name = NAMES[int(q['id'][-3:]) % len(NAMES)] if q['id'][-3:].isdigit() else 'Sam'
            if q['skillId'] == 'antiderivatives-definite-integrals-skill-04' and (fam or '').startswith(('s3_riemann', 'conv_')):
                q = conv_item(q, int(q['id'][-3:]), rng, name); n['conv'] += 1
            elif q['skillId'] == 'fundamental-theorem-calculus-skill-03' and (fam or '').startswith(('s2_accum', 's2_formula', 'acc_formula')):
                q = acc_item(q, int(q['id'][-3:]), rng, name); n['acc'] += 1
            elif q['skillId'] == 'antiderivatives-definite-integrals-skill-03' and q['id'][-3:] in ('001', '002', '003', '004'):
                q = limsum_item(q, rng); n['lim'] += 1
            out.append(q)
        d['questions'] = out
    lib.save(banks)
    print(n)


if __name__ == '__main__':
    main()
