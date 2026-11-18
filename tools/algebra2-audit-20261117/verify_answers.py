"""Independent recomputation of Algebra 2 bank answers (Algebra 2 audit, 2026-11-17).

Shares no code with the authoring scripts: mathx.py parses the printed problem and the key, and each family
re-derives the answer (expression equivalence, substitution into equations with a numeric search for missed real
roots, systems, sigma sums, evaluations, select-all solutions and points). Exits non-zero on any disagreement.
usage: python3 tools/algebra2-audit-20261117/verify_answers.py [--min N]"""
import json, re, random, math, cmath, collections, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mathx import ev, close, ParseError
from lib import load, items as bank_items

I = [q for _, q in bank_items(load())]
random.seed(7)
PTS = [-3.7, -2.3, -1.1, 0.6, 1.9, 2.8, 4.3, 5.6]
res = collections.Counter()
flags = []
checked = collections.defaultdict(set)


def flag(x, why, extra=''):
    flags.append((x['id'], why, x['prompt'][:160].replace('\n', ' '), str(x['answer'])[:100], extra))


def clean(s):
    s = s.strip().rstrip('.').strip()
    return s


def equiv(a, b, var='x', pts=PTS, extra_env=None):
    ok = 0
    for t in pts:
        env = {var: t}
        if extra_env:
            env.update(extra_env)
        try:
            va = ev(a, env); vb = ev(b, env)
        except ZeroDivisionError:
            continue
        except (ValueError, OverflowError):
            continue
        if not close(va, vb, 1e-6):
            return False
        ok += 1
    return ok >= 3


def two_var_equiv(a, b, vs):
    ok = 0
    for _ in range(8):
        env = {v: random.uniform(-4, 4) for v in vs}
        try:
            va = ev(a, env); vb = ev(b, env)
        except (ZeroDivisionError, ValueError, OverflowError):
            continue
        if not close(va, vb, 1e-6):
            return False
        ok += 1
    return ok >= 3


def vars_in(s):
    s2 = re.sub(r'(sqrt|cbrt|sin|cos|tan|log|ln|abs|pi)', '', s)
    return sorted(set(re.findall(r'[a-hj-z]', s2)) - {'e'})


def inner_problem(x):
    """For find-the-mistake items return (problem text, student answer) or (prompt, None)."""
    p = x['prompt']
    m = re.match(r"^\w+ answered this problem incorrectly\.\s*(.*?)\s*\w+'s answer:\s*(.*?)\s*Identify the mistake and give the correct answer\.?$", p, re.S)
    if m:
        return m.group(1).strip(), m.group(2).strip()
    return p, None


def split_or(ans):
    a = clean(ans)
    a = re.sub(r'^x\s*=\s*', '', a)
    parts = re.split(r'\s*(?:,|\bor\b|\band\b|;)\s*(?:x\s*=\s*)?', a)
    return [p for p in parts if p]


def roots_real(f, lo=-40, hi=40, n=8000):
    """numeric real roots of f on [lo,hi] (sign changes + near-zero minima)."""
    xs = [lo + (hi - lo) * k / n for k in range(n + 1)]
    vals = []
    for t in xs:
        try:
            v = f(t)
            if isinstance(v, complex):
                v = v.real if abs(v.imag) < 1e-9 else None
        except (ZeroDivisionError, ValueError, OverflowError):
            v = None
        vals.append(v)
    roots = []
    for k in range(n):
        a, b = vals[k], vals[k + 1]
        if a is None or b is None:
            continue
        if a == 0:
            roots.append(xs[k])
        elif a * b < 0 and abs(a) < 1e3 and abs(b) < 1e3:
            lo_, hi_ = xs[k], xs[k + 1]
            for _ in range(60):
                mid = (lo_ + hi_) / 2
                try:
                    vm = f(mid)
                except Exception:
                    break
                if isinstance(vm, complex):
                    vm = vm.real
                if (vm < 0) == (a < 0):
                    lo_ = mid
                else:
                    hi_ = mid
            roots.append((lo_ + hi_) / 2)
    # tangent roots: local min of |f| near zero
    for k in range(1, n):
        a, b, c = vals[k - 1], vals[k], vals[k + 1]
        if None in (a, b, c):
            continue
        if abs(b) < 1e-6 and abs(b) <= abs(a) and abs(b) <= abs(c):
            roots.append(xs[k])
    out = []
    for r in sorted(roots):
        if not out or abs(r - out[-1]) > 1e-3:
            out.append(r)
    return out


OPS = r'(Add|Subtract|Multiply|Expand|Simplify|Factor completely|Factor|Multiply and simplify|Divide and simplify|Divide|Add and simplify|Subtract and simplify|Rewrite|Write in vertex form|Write in standard form|Combine)'


def check_equiv_family(x, prob, key, student):
    m = re.match(OPS + r'(?: completely)?(?: and simplify)?\s*:?\s*(.+?)\.?$', prob, re.S)
    if not m:
        return None
    expr = m.group(2).strip().rstrip('.')
    if re.search(r'state|excluded|assume|where|for x|in terms', expr, re.I):
        return None
    words = set(re.findall(r'[A-Za-z]{2,}', expr + ' ' + key)) - {'sqrt', 'cbrt', 'sin', 'cos', 'tan', 'csc', 'sec', 'cot', 'ln', 'log', 'abs', 'pi'}
    if words:
        return None
    if '÷' in expr:
        a_, b_ = expr.split('÷', 1)
        expr = '(' + a_ + ')/(' + b_ + ')'
    if re.search(r'[=<>]', expr) or re.search(r'[=<>]', key):
        return None
    if 'i' in vars_in(expr + key):
        pass
    vs = sorted(set(vars_in(expr)) | set(vars_in(key)))
    try:
        if len(vs) <= 1:
            good = equiv(expr, key, vs[0] if vs else 'x')
        else:
            good = two_var_equiv(expr, key, vs)
    except ParseError:
        return None
    if not good:
        return 'key not equivalent to expression'
    if student:
        try:
            sgood = equiv(expr, student, vs[0] if vs else 'x') if len(vs) <= 1 else two_var_equiv(expr, student, vs)
        except ParseError:
            return 'ok'
        if sgood:
            return 'student answer is also correct'
    return 'ok'


def parse_eq(eq):
    if eq.count('=') != 1:
        return None
    l, r = eq.split('=')
    return l.strip(), r.strip()


def check_solve(x, prob, key, student):
    m = re.match(r'(?:Solve|Find all (?:real )?solutions of|Find all solutions:?)\s*(?:for x:?\s*)?(.+?)(?:\.\s|\.$|$)(.*)', prob, re.S)
    if not m:
        return None
    eq = m.group(1).strip().rstrip('.')
    tail = m.group(2)
    if ' and ' in eq or ',' in eq or 'system' in prob.lower():
        return None
    pe = parse_eq(eq)
    if not pe:
        return None
    l, r = pe
    v = vars_in(l + r)
    if len(v) != 1:
        return None
    var = v[0]
    k = clean(key)
    if re.search(r'no (real )?solution', k, re.I):
        sols = []
    else:
        k2 = re.sub(r'^' + var + r'\s*=\s*', '', k)
        sols = re.split(r'\s*(?:,|\bor\b|\band\b)\s*(?:' + var + r'\s*=\s*)?', k2)
        sols = [s for s in sols if s]
    vals = []
    for s in sols:
        if '±' in s:
            a = s.replace('±', '+', 1); b = s.replace('±', '-', 1)
            vals += [ev(a), ev(b)]
        else:
            vals.append(ev(s))
    f = lambda t: ev(l, {var: t}) - ev(r, {var: t})
    for val in vals:
        try:
            fv = f(val)
        except ZeroDivisionError:
            return 'key value %s makes a denominator zero' % val
        except ValueError:
            return 'key value undefined %s' % val
        if not close(fv, 0, 1e-5) and abs(fv) > 1e-5:
            return 'key value %r does not satisfy equation (residual %.3g)' % (val, abs(fv))
    complex_key = any(isinstance(v_, complex) and abs(v_.imag) > 1e-9 for v_ in vals)
    if not complex_key and 'interval' not in tail.lower() and '[0' not in prob and not re.search(r'sin|cos|tan', eq):
        try:
            rr = roots_real(f)
        except ParseError:
            rr = None
        if rr is not None:
            realvals = sorted(v_.real if isinstance(v_, complex) else v_ for v_ in vals)
            missing = [r_ for r_ in rr if not any(abs(r_ - v_) < 1e-3 * max(1, abs(r_)) for v_ in realvals)]
            if missing and 'real' not in tail and not re.search(r'complex|exact', prob, re.I) and not any(isinstance(v_, complex) for v_ in vals):
                return 'equation has real root(s) %s not in key' % [round(t, 4) for t in missing]
    if student:
        try:
            ss = re.sub(r'^' + var + r'\s*=\s*', '', clean(student))
            ss = re.split(r'\s*(?:,|\bor\b|\band\b)\s*(?:' + var + r'\s*=\s*)?', ss)
            svals = []
            for s in ss:
                if '±' in s:
                    svals += [ev(s.replace('±', '+', 1)), ev(s.replace('±', '-', 1))]
                else:
                    svals.append(ev(s))
            if len(svals) == len(vals) and all(any(close(a, b, 1e-6) for b in vals) for a in svals):
                return 'student answer equals key'
        except Exception:
            pass
    return 'ok'


def check_eval_logs(x, prob, key, student):
    m = re.match(r'Evaluate (.+?)\.?$', prob)
    if not m or 'Σ' in prob:
        return None
    e = m.group(1).rstrip('.')
    e = re.sub(r'\s*(in radians|in degrees|exactly|without a calculator)$', '', e)
    if '=' in e or vars_in(e):
        return None
    try:
        a = ev(e)
    except (ParseError, ZeroDivisionError, ValueError):
        return None
    k = clean(key)
    deg = k.endswith('°')
    try:
        b = ev(k.rstrip('°'))
    except (ParseError, ZeroDivisionError, ValueError):
        return None
    if deg:
        a = math.degrees(a.real) if re.search(r'asin|acos|atan|⁻¹', e + norm_(e)) else a
    if not close(a, b, 1e-4):
        return 'evaluated %r != key %r' % (a, b)
    return 'ok'


def norm_(s):
    return s


def check_sigma(x, prob, key, student):
    m = re.search(r'Σ from (\w) = (-?\d+) to (\d+|∞) of \(?(.+?)\)?\.?$', prob)
    if not m:
        return None
    v, a, b, body = m.group(1), int(m.group(2)), m.group(3), m.group(4)
    if b == '∞':
        b = 400
    else:
        b = int(b)
    try:
        s = sum(ev(body, {v: k}) for k in range(a, b + 1))
        kv = ev(clean(key))
    except (ParseError, ZeroDivisionError, ValueError, OverflowError):
        return None
    if not close(s, kv, 1e-4):
        return 'sum %r != key %r' % (s, kv)
    return 'ok'


def check_system(x, prob, key, student):
    m = re.search(r'(?:Solve(?: the system)?(?: by \w+)?:?)\s*(.+?) and (.+?)\.?$', prob)
    if not m:
        return None
    e1, e2 = m.group(1).strip(), m.group(2).strip().rstrip('.')
    km = re.match(r'\(\s*(-?[\d./]+)\s*,\s*(-?[\d./]+)\s*\)$', clean(key))
    if not km:
        return None
    X, Y = ev(km.group(1)), ev(km.group(2))
    for e in (e1, e2):
        pe = parse_eq(e)
        if not pe:
            return None
        try:
            l = ev(pe[0], {'x': X, 'y': Y}); r = ev(pe[1], {'x': X, 'y': Y})
        except ParseError:
            return None
        if not close(l, r):
            return 'key (%s,%s) fails %s' % (X, Y, e)
    if student:
        sm = re.match(r'\(\s*(-?[\d./]+)\s*,\s*(-?[\d./]+)\s*\)$', clean(student))
        if sm and close(ev(sm.group(1)), X) and close(ev(sm.group(2)), Y):
            return 'student answer equals key'
    return 'ok'


def check_func_eval(x, prob, key, student):
    m = re.match(r'(?:Let |For |If )?f\(x\) = (.+?)[.,;]\s*(?:Find|Evaluate|What is)\s+f\((-?[\d./]+)\)\.?\??$', prob)
    if not m:
        return None
    try:
        a = ev(m.group(1), {'x': ev(m.group(2))}); b = ev(clean(key).split('=')[-1])
    except (ParseError, ZeroDivisionError, ValueError):
        return None
    if not close(a, b):
        return 'f(%s)=%r != key %r' % (m.group(2), a, b)
    return 'ok'


def check_comb(x, prob, key, student):
    m = re.search(r'\b([PC])\((\d+),\s*(\d+)\)|ₙ?(\d+)([PC])(\d+)', prob)
    return None


FAMS = [('equiv', check_equiv_family), ('solve', check_solve), ('system', check_system), ('eval', check_eval_logs),
        ('sigma', check_sigma), ('feval', check_func_eval)]

for x in I:
    if x['format'] not in ('short-answer', 'multiple-choice'):
        continue
    if not isinstance(x['answer'], str):
        continue
    prob, student = inner_problem(x)
    prob = ' '.join(prob.split())
    key = x['answer']
    for name, fn in FAMS:
        try:
            r = fn(x, prob, key, student)
        except (ParseError, ZeroDivisionError, ValueError, OverflowError, TypeError, IndexError) as e:
            r = None
        if r is None:
            continue
        res[(name, 'ok' if r == 'ok' else 'FLAG')] += 1
        checked[name].add(x['id'])
        if r != 'ok':
            flag(x, name + ': ' + r)
        break


# select-all: every choice of "Select ALL solutions of <equation>" / "Select ALL points on <curve>" re-checked
T = lambda o: o['text'] if isinstance(o, dict) else o
for x in I:
    if x['format'] != 'select-all':
        continue
    p = ' '.join(x['prompt'].split())
    m = re.match(r'Select ALL (?:real )?solutions (?:of|to) (.+?)\.?$', p)
    try:
        if m and m.group(1).count('=') == 1 and not re.search(r'sin|cos|tan|\[|on ', m.group(1)):
            l, r = m.group(1).split('=')
            for o in x['options']:
                t = re.sub(r'^x\s*=\s*', '', T(o).strip())
                v = ev(t)
                try:
                    fv = ev(l, {'x': v}) - ev(r, {'x': v}); sat = abs(fv) < 1e-6
                except ZeroDivisionError:
                    sat = False
                if sat != o['correct']:
                    flag(x, 'select-all: option %s marked %s but satisfies=%s' % (t, o['correct'], sat))
            res[('selectall', 'ok')] += 1; checked['selectall'].add(x['id'])
            continue
        m = re.match(r'Select ALL points on (?:the (?:circle|graph of|parabola|ellipse|hyperbola) )?(.+?)\.$', p)
        if m and m.group(1).count('=') == 1:
            l, r = m.group(1).split('=')
            for o in x['options']:
                pm = re.match(r'\((.+?),\s*(.+?)\)$', T(o).strip())
                X, Y = ev(pm.group(1)), ev(pm.group(2))
                try:
                    sat = abs(ev(l, {'x': X, 'y': Y}) - ev(r, {'x': X, 'y': Y})) < 1e-6
                except ZeroDivisionError:
                    sat = False
                if sat != o['correct']:
                    flag(x, 'select-all: point %s marked %s but on curve=%s' % (T(o), o['correct'], sat))
            res[('selectall', 'ok')] += 1; checked['selectall'].add(x['id'])
    except (ParseError, AttributeError, ValueError, TypeError):
        pass

print(sorted(res.items()))
n = len(set().union(*checked.values()))
print('distinct checked', n)
for f in flags:
    print('FLAG', f)
mn = int(sys.argv[sys.argv.index('--min') + 1]) if '--min' in sys.argv else 0
if flags or n < mn:
    sys.exit(1)
print('PASS independent Algebra 2 answer check')
