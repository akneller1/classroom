"""Calculus audit #9 (2026-11-18): Honors items harder than CP2, CP2 items with a hint.

In the computational families that used the same kind of function at every level, the Honors items (not the
find-the-mistake or practice-set items) are replaced by versions with trig, exponential, logarithmic, radical or
rational functions, interior zeros and non-integer answers. CP2 items in the same families get a one-line hint.
Answers are computed with sympy; worked steps come from expand_steps.py (run it after this script).
Deterministic and idempotent: a replaced item is recognized by its family name ending in "_h".
"""
import random, re, sys, os
import sympy as sp
sys.path.insert(0, os.path.dirname(__file__))
import lib
from bankfmt import bt
from author import mc, record

x, t = sp.symbols('x t')
C = sp.Symbol('C')
E, pi = sp.E, sp.pi


def P(s):
    import verify_keys as V
    return V.P(s)


def interval(a, b):
    f = lambda v: '∞' if v == sp.oo else ('-∞' if v == -sp.oo else bt(v))
    return f'({f(a)}, {f(b)})'


# ---------------------------------------------------------------- Honors pools: (prompt text, answer text, steps, distractors)
def disp(rng):
    v, b = rng.choice([('2sin(πt/4)', 2), ('4cos(πt/2) + 1', 1), ('6e^(-t/2)', 2), ('3√t - 1', 4), ('1/(t + 1)', 3), ('t·e^(-t)', 1), ('2cos(t) + t', sp.pi)])
    ve = P(v)
    val = sp.simplify(sp.integrate(ve, (t, 0, b)))
    bs = bt(b)
    p = f'A particle moves with velocity v(t) = {v} m/s. Find its displacement from t = 0 to t = {bs}.'
    return p, f'{bt(val)} m', [f'{bt(val * 2)} m', f'{bt(ve.subs(t, b))} m', f'{bt(-val)} m', f'{bt(val + 1)} m']


def total(rng):
    v, b = rng.choice([('3cos(πt/3)', 6), ('2sin(πt/2)', 3), ('t² - 5t + 4', 5), ('t³ - 4t', 3), ('4cos(πt/4)', 4), ('t² - 6t + 5', 6)])
    ve = P(v)
    zs = sorted([z for z in sp.solve(ve, t) if z.is_real and 0 < z < b], key=float)
    pts = [0] + zs + [b]
    val = sp.nsimplify(sp.simplify(sum(sp.Abs(sp.integrate(ve, (t, p0, p1))) for p0, p1 in zip(pts, pts[1:]))))
    disp_ = sp.simplify(sp.integrate(ve, (t, 0, b)))
    p = f'A particle moves with velocity v(t) = {v} ft/s. Find the total distance traveled from t = 0 to t = {b}.'
    return p, f'{bt(val)} ft', [f'{bt(sp.Abs(disp_))} ft', f'{bt(val * 2)} ft', f'{bt(val + 1)} ft', f'{bt(sp.Abs(disp_) + 2)} ft']


def intervals_pool(rng):
    k = rng.choice([1, 2, 3])
    a = rng.choice([2, 3, 4])
    items = [
        (f'xe^(-{k}x)' if k != 1 else 'xe^(-x)', [interval(-sp.oo, sp.Rational(1, k))], [interval(sp.Rational(1, k), sp.oo)]),
        ('x²e^x', [interval(-sp.oo, -2), interval(0, sp.oo)], [interval(-2, 0)]),
        (f'x - {a}ln(x)', [interval(a, sp.oo)], [interval(0, a)]),
        (f'x + {a * a}/x', [interval(-sp.oo, -a), interval(a, sp.oo)], [interval(-a, 0), interval(0, a)]),
        (f'ln(x² + {a})', [interval(0, sp.oo)], [interval(-sp.oo, 0)]),
    ]
    f, inc, dec = rng.choice(items)
    want = rng.choice(['increasing', 'decreasing'])
    ans = ' ∪ '.join(inc if want == 'increasing' else dec)
    other = ' ∪ '.join(dec if want == 'increasing' else inc)
    p = f'On what interval(s) is f(x) = {f} {want}?'
    return p, ans, [other, '(-∞, ∞)', interval(0, sp.oo) if ans != interval(0, sp.oo) else interval(-sp.oo, 0), interval(-sp.oo, 1)]


def crit(rng):
    f, ans = rng.choice([('x²e^(-x)', 'x = 0 or x = 2'), ('xe^(-x²/2)', 'x = -1 or x = 1'), ('x - 2ln(x)', 'x = 2'),
                         ('ln(x² + 1) - x', 'x = 1'), ('x³e^x', 'x = -3 or x = 0'), ('(x² - 3)e^x', 'x = -3 or x = 1')])
    return f'Find the critical numbers of f(x) = {f}.', ans, ['x = 0', 'x = 1 or x = 2', 'x = -1', 'x = 3']


def absolute(rng):
    f, a, b, kind = rng.choice([('xe^(-x)', 0, 3, 'maximum'), ('x - 2ln(x)', 1, 'e²', 'minimum'), ('sin(x) + cos(x)', 0, 'π', 'maximum'),
                                ('x²e^x', -3, 1, 'maximum'), ('x + 4/x', 1, 4, 'minimum'), ('2√x - x', 0, 4, 'maximum')])
    fe, ae, be = P(f), P(str(a)), P(str(b))
    cands = [ae, be] + [c for c in sp.solve(sp.diff(fe, x), x) if c.is_real and ae <= c <= be]
    vals = [(sp.simplify(fe.subs(x, c)), c) for c in cands]
    best = (max if kind == 'maximum' else min)(vals, key=lambda z: float(z[0]))
    worst = (min if kind == 'maximum' else max)(vals, key=lambda z: float(z[0]))
    ans = f'{bt(best[0])} at x = {bt(best[1])}'
    return f'Find the absolute {kind} of f(x) = {f} on [{a}, {b}]. Give the value and where it occurs.', ans, [f'{bt(worst[0])} at x = {bt(worst[1])}', f'{bt(best[0])} at x = {bt(ae)}' if best[1] != ae else f'{bt(best[0])} at x = {bt(be)}', f'{bt(sp.simplify(fe.subs(x, be)))} at x = {bt(be)}', f'{bt(best[0] + 1)} at x = {bt(best[1])}']


def mvt(rng):
    f, a, b, ans = rng.choice([('√x', 1, 4, '9/4'), ('ln(x)', 1, 'e', 'e - 1'), ('1/x', 1, 3, '√3'), ('e^x', 0, 1, 'ln(e - 1)'), ('x + 1/x', 1, 4, '2'), ('√x', 0, 9, '9/4')])
    return f'Find the value of c guaranteed by the Mean Value Theorem for f(x) = {f} on [{a}, {b}].', f'c = {ans}', [f'c = {x_}' for x_ in ['5/2', '3/2', '2', '1', '√2', 'e/2'] if x_ != ans]


def general(rng):
    de, ans = rng.choice([('y′ = xy²', 'y = -2/(x² + C)'), ('y′ = e^(x - y)', 'y = ln(e^x + C)'), ('y′ = ycos(x)', 'y = Ce^(sin(x))'),
                          ('y′ = 1 + y²', 'y = tan(x + C)'), ('y′ = 2x√y', 'y = ((x² + C)/2)²'), ('y′ = y/x', 'y = Cx')])
    return f'Find the general solution of {de}.', ans, ['y = Ce^x', 'y = x² + C', 'y = Ce^(x²)', 'y = 1/(x + C)']


def infty(rng):
    e, d, ans, why = rng.choice([
        ('3x/√(4x² + 1)', '∞', '3/2', 'Divide the top and bottom by x (for x > 0, x = √(x²)): 3/√(4 + 1/x²) → 3/√4 = 3/2.'),
        ('√(9x² + x)/(x + 1)', '∞', '3', 'Divide by x: √(9 + 1/x)/(1 + 1/x) → √9/1 = 3.'),
        ('√(x² + 1)/x', '-∞', '-1', 'For x < 0, x = -√(x²); dividing gives -√(1 + 1/x²) → -1.'),
        ('(2x² - x)/e^x', '∞', '0', 'e^x grows faster than any polynomial (L’Hôpital twice gives 4/e^x → 0).'),
        ('ln(x)/x', '∞', '0', 'ln(x) grows more slowly than x (L’Hôpital: (1/x)/1 → 0).'),
        ('(5x - sin(x))/x', '∞', '5', 'Split: 5 - sin(x)/x, and -1/x ≤ sin(x)/x ≤ 1/x → 0 by the Squeeze Theorem.')])
    return f'Evaluate lim (x → {d}) {e}.', ans, why


def sign(rng):
    fp, inc, dec = rng.choice([('x²(x - 3)', '(3, ∞)', '(-∞, 0) ∪ (0, 3)'), ('(x + 1)²(x - 2)', '(2, ∞)', '(-∞, -1) ∪ (-1, 2)'),
                               ('x(x - 4)e^(-x)', '(-∞, 0) ∪ (4, ∞)', '(0, 4)'), ('(x - 1)/(x² + 1)', '(1, ∞)', '(-∞, 1)'), ('cos(x) on (0, 2π)', '(0, π/2) ∪ (3π/2, 2π)', '(π/2, 3π/2)')])
    want = rng.choice(['increasing', 'decreasing'])
    ans = inc if want == 'increasing' else dec
    dom = '' if ' on ' not in fp else ' on ' + fp.split(' on ')[1]
    return f'f′(x) = {fp.split(" on ")[0]}{dom}. On what interval(s) is f {want}?', ans, [dec if want == 'increasing' else inc, '(-∞, ∞)', '(0, ∞)', '(-∞, 0)']


def motion(rng):
    s, c, kind = rng.choice([('4sin(πt/6)', 3, 'velocity'), ('4sin(πt/6)', 1, 'acceleration'), ('t²e^(-t)', 1, 'velocity'), ('6√t + t', 4, 'velocity'),
                             ('3cos(2t) + t²', 'π/4', 'acceleration'), ('ln(t + 1) + 2t', 1, 'velocity')])
    se, ce = P(s), P(str(c))
    n = 1 if kind == 'velocity' else 2
    val = sp.simplify(sp.diff(se, t, n).subs(t, ce))
    un = 'm/s' if n == 1 else 'm/s²'
    return f'A particle moves along a line with position s(t) = {s} meters at time t seconds, for t ≥ 0. Find the {kind} at t = {c}.', f'{bt(val)} {un}', [f'{bt(sp.simplify(sp.diff(se, t, 3 - n).subs(t, ce)))} {un}', f'{bt(sp.simplify(se.subs(t, ce)))} {un}', f'{bt(-val)} {un}', f'{bt(val + 1)} {un}']


def formula(rng):
    a, f = rng.choice([(0, 'cos(t) + 2t'), (1, '1/t'), (0, 'e^(2t)'), (0, 'sin(3t)'), (4, '1/√t'), (0, '2te^(t²)')])
    fe = P(f)
    g = sp.simplify(sp.integrate(fe.subs(t, sp.Symbol('u')), (sp.Symbol('u'), a, x)))
    return f'Find a formula for g(x) = ∫ from {a} to x {f if len(f) < 4 else "(" + f + ")"} dt.', f'g(x) = {bt(g)}', [f'g(x) = {bt(sp.diff(fe.subs(t, x), x))}', f'g(x) = {bt(fe.subs(t, x))}', f'g(x) = {bt(sp.integrate(fe.subs(t, x), x))} + 1', f'g(x) = {bt(-g)}']


def accel(rng):
    s, c = rng.choice([('3sin(2t) + t²', 'π/4'), ('e^(-t) + 4t', 0), ('t³ - 6ln(t)', 1), ('2cos(πt)', 1), ('√t', 4)])
    se, ce = P(s), P(str(c))
    val = sp.simplify(sp.diff(se, t, 2).subs(t, ce))
    return f"A particle's position is s(t) = {s} meters. Find its acceleration at t = {c} seconds.", f'{bt(val)} m/s²', [f'{bt(sp.simplify(sp.diff(se, t).subs(t, ce)))} m/s²', f'{bt(-val)} m/s²', f'{bt(val + 2)} m/s²', f'{bt(sp.simplify(se.subs(t, ce)))} m/s²']


POOLS = {'s4_disp': disp, 's5_total': total, 's3_intervals': intervals_pool, 's2_crit': crit, 's4_absolute': absolute, 's10_mvt': mvt,
         's5_general': general, 'g6_s5_generals': general, 's5_infty': infty, 's7_sign': sign, 's8_motion': motion, 's2_formula': formula, 's4_accel': accel}

HINTS = {
    's4_disp': 'Hint: displacement is the integral of velocity.',
    's5_total': 'Hint: find where v(t) = 0 first, then add the distances on each piece.',
    's3_intervals': 'Hint: find where f′(x) = 0, then test the sign of f′ on each interval.',
    's2_crit': 'Hint: set f′(x) = 0 and solve.',
    's4_absolute': 'Hint: compare f at the critical numbers and at both endpoints.',
    's10_mvt': 'Hint: first find the average rate of change on the interval.',
    's5_general': 'Hint: separate the variables, then integrate both sides.',
    'g6_s5_generals': 'Hint: separate the variables, then integrate both sides.',
    's5_infty': 'Hint: compare the degrees of the top and bottom.',
    's7_sign': 'Hint: factor f′(x) and make a sign chart.',
    's8_motion': 'Hint: v(t) = s′(t) and a(t) = s″(t).',
    's2_formula': 'Hint: find an antiderivative, then evaluate from the lower limit to x.',
    's4_accel': 'Hint: differentiate twice.',
    's3_avg': 'Hint: f_avg = (1/(b − a))∫ from a to b f(x) dx.',
    's6_area': 'Hint: find where the curves meet, then integrate top minus bottom.',
}


def upgrade(q, rng):
    fam = lib.family(q)
    base = fam[:-2] if fam.endswith('_h') else fam
    out = POOLS[base](rng)
    if base == 's5_infty':
        prompt, ans, why = out
        steps = ['Look at how the top and bottom grow as x moves away from 0.', why, f'The limit is {ans}.']
        dis = ['0', '∞', '1', '-∞', '3', '2'] if ans != '0' else ['1', '∞', '-1', '2']
        dis = [d for d in dis if d != ans]
    else:
        prompt, ans, dis = out
        steps = [f'Answer: {ans}.']   # replaced by expand_steps.py where it can rebuild them
        if base in ('s3_intervals', 's7_sign', 's2_crit', 's5_general', 'g6_s5_generals', 's10_mvt', 's8_motion', 's4_accel', 's4_absolute', 's2_formula'):
            steps = level_steps(base, prompt, ans)
    if q['format'] == 'multiple-choice':
        dis = [d for d in dis if d != ans] + fallback(ans)
        return record(q, base + '_h', prompt, ans, steps, fmt='multiple-choice', options=mc(rng, ans, [d for d in dis if d != ans]))
    return record(q, base + '_h', prompt, ans, steps)


def fallback(ans):
    m = re.match(r'^(.*?)( (?:m/s²|m/s|m|ft))?$', ans)
    try:
        v = P(m.group(1)); u = m.group(2) or ''
        return [bt(sp.simplify(w)) + u for w in (v * 2, v + 1, v - 1, -v, v / 2) if sp.simplify(w - v) != 0]
    except Exception:
        return []


def level_steps(base, prompt, ans):
    m = re.search(r'f\(x\) = (.+?) (increasing|decreasing)\?', prompt) or re.search(r'f\(x\) = (.+)\.$', prompt)
    if base == 's3_intervals':
        f = P(m.group(1)); d = sp.simplify(sp.diff(f, x))
        z = [r for r in sp.solve(d, x) if r.is_real]
        return [f'f′(x) = {bt(sp.factor(d))}.', f'f′(x) = 0 at x = {", ".join(bt(r) for r in sorted(z, key=float))}' + (' (and f′ or f is undefined at x = 0)' if '/x' in m.group(1) or 'ln' in m.group(1) and 'x²' not in m.group(1) else '') + '.',
                'Test the sign of f′ on each interval of the domain.', f'f is {m.group(2)} on {ans}.']
    if base == 's7_sign':
        return ['Find the zeros of f′ and make a sign chart. A squared factor does not change sign, and e^(-x) and x² + 1 are always positive.',
                f'f is increasing where f′ > 0 and decreasing where f′ < 0: {ans}.']
    if base == 's2_crit':
        f = P(m.group(1)); d = sp.diff(f, x)
        return [f'f′(x) = {bt(sp.factor(d))}.', f'f′ is defined for every x in the domain, so solve f′(x) = 0.', ans + '.']
    if base in ('s8_motion', 's4_accel'):
        mm = re.search(r's\(t\) = (.+?) meters.*Find (?:the|its) (velocity|acceleration) at t = (\S+?)(?: seconds)?\.$', prompt)
        se, ce = P(mm.group(1)), P(mm.group(3))
        v1, v2 = sp.diff(se, t), sp.diff(se, t, 2)
        lines = [f'v(t) = s′(t) = {bt(sp.simplify(v1))}.']
        if mm.group(2) == 'acceleration':
            lines.append(f'a(t) = v′(t) = {bt(sp.simplify(v2))}.')
            lines.append(f'a({mm.group(3)}) = {ans}.')
        else:
            lines.append(f'v({mm.group(3)}) = {ans}.')
        return lines
    if base == 's4_absolute':
        mm = re.search(r'f\(x\) = (.+) on \[(.+), (.+)\]\.', prompt)
        fe, ae, be = P(mm.group(1)), P(mm.group(2)), P(mm.group(3))
        d = sp.diff(fe, x)
        cs = [c for c in sp.solve(d, x) if c.is_real and ae <= c <= be]
        vals = '; '.join(f'f({bt(c)}) = {bt(sp.simplify(fe.subs(x, c)))}' for c in [ae] + cs + [be])
        return [f'f′(x) = {bt(sp.simplify(d))}; critical number(s) in the interval: {", ".join(bt(c) for c in cs) or "none"}.', f'Candidates test: {vals}.', f'Absolute {"maximum" if "maximum" in prompt else "minimum"}: {ans}.']
    if base == 's2_formula':
        mm = re.search(r'g\(x\) = ∫ from (\S+) to x \(?(.+?)\)? dt\.', prompt)
        a, fe = P(mm.group(1)), P(mm.group(2))
        F = sp.integrate(fe, t)
        return [f'An antiderivative of {mm.group(2)} is {bt(F)}.', f'g(x) = [{bt(F)}] evaluated from t = {mm.group(1)} to t = x = ({bt(F.subs(t, x))}) − ({bt(sp.simplify(F.subs(t, a)))}).', f'{ans}.']
    if base in ('s5_general', 'g6_s5_generals'):
        return ['Separate the variables: put every y on the left with dy and every x on the right with dx.', 'Integrate both sides and add one constant C.', f'Solve for y: {ans}.']
    if base == 's10_mvt':
        return ['The MVT applies: f is continuous on the closed interval and differentiable on the open interval.', 'Find the average rate (f(b) − f(a))/(b − a), then solve f′(c) = that rate.', f'{ans}, which is inside the interval.']
    return [f'Answer: {ans}.']


def main():
    banks = lib.load()
    n = {'honors': 0, 'hints': 0}
    for u, d in banks.items():
        for q in d['questions']:
            fam = lib.family(q) or ''
            base = fam[:-2] if fam.endswith('_h') else fam
            regular = 'answered this problem incorrectly' not in q['prompt'] and q['format'] != 'open-response'
            if q['level'] == 'honors' and regular and base in POOLS:
                rng = random.Random('cal-audit-9-' + q['id'])
                new = upgrade(q, rng)
                q.clear(); q.update(new); n['honors'] += 1
            if q['level'] == 'cp2' and regular and base in HINTS and 'Hint:' not in q['prompt']:
                q['prompt'] = q['prompt'] + ' ' + HINTS[base]; n['hints'] += 1
    lib.save(banks)
    print(n)


if __name__ == '__main__':
    main()
