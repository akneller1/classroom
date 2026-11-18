"""Precalculus audit #7: fuller worked solutions.

1. steps/single-step.json: hand-written steps for the 28 single-step items.
2. For thin items (under 60 characters of solution) in common computational families, generate the substitution and
   arithmetic between the formula and the answer. Every generated chain is recomputed here and must end at the
   item's own key (compared numerically) or the item is left unchanged and reported.
Find-the-mistake items keep their first "Mistake:" step and their last "The correct answer is …" step.
Idempotent: items whose solution is already 60+ characters are not touched.
usage: python3 expand_steps.py [--report]
"""
import json, math, os, re, sys
from fractions import Fraction as F
from lib import load, save, items

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE))
from mathx import ev  # noqa: E402

D = math.pi / 180
SUB = str.maketrans('0123456789', '₀₁₂₃₄₅₆₇₈₉')


def fnum(v):
    v = F(v).limit_denominator(10000)
    return str(v.numerator) if v.denominator == 1 else f"{v.numerator}/{v.denominator}"


def g(x, dp=4):
    s = f"{x:.{dp}f}".rstrip('0').rstrip('.')
    return '0' if s in ('-0', '') else s


def keyval(a):
    s = str(a).replace('−', '-').replace('$', '').replace(',', '').strip().rstrip('.')
    s = re.sub(r'^[a-zA-Zθ]\w*\s*[≈=]\s*', '', s).replace('≈', '').strip()
    s = re.sub(r'\s*(°|%|cm²|m²|units²|cm|km/h|mph|ft|m|km|N|J|hours?|years?)\.?$', '', s)
    return ev(s, {})


def inner(q):
    p = q['prompt']
    if 'answered this problem incorrectly' in p:
        lines = p.split('\n')
        return '\n'.join(l for l in lines[1:] if not re.search(r"'s answer:|Identify the mistake", l)).strip()
    return p.strip()


FAMS = []


def fam(rx):
    def deco(fn):
        FAMS.append((re.compile(rx), fn))
        return fn
    return deco


@fam(r'^Evaluate f\((-?\d+)\) for f\(x\) = ([\d.]+)\(([\d.]+)\)ˣ\.')
def _(m, key):
    n, a, b = int(m[1]), F(m[2]), F(m[3])
    p = b ** n
    return [f"Substitute x = {n}: f({n}) = {m[2]}({m[3]})^{n}.", f"({m[3]})^{n} = {g(float(p), 8)}.", f"f({n}) = {m[2]} · {g(float(p), 8)} = {g(float(a * p), 8)}."], float(a * p)


@fam(r'^Find the (\d+)(?:st|nd|rd|th) term of the sequence (-?[\d/]+), (-?[\d/]+), (-?[\d/]+), (-?[\d/]+), …')
def _(m, key):
    n = int(m[1]); t = [F(x) for x in m.groups()[1:]]
    if t[1] - t[0] == t[2] - t[1] == t[3] - t[2]:
        d = t[1] - t[0]; v = t[0] + (n - 1) * d
        return [f"The terms change by the same amount each time: d = {fnum(t[1])} - ({fnum(t[0])}) = {fnum(d)} (arithmetic).",
                f"aₙ = a₁ + (n - 1)d, so a{str(n).translate(SUB)} = {fnum(t[0])} + ({n} - 1)({fnum(d)}) = {fnum(t[0])} + ({fnum((n - 1) * d)}).", f"a{str(n).translate(SUB)} = {fnum(v)}."], float(v)
    r = t[1] / t[0]; v = t[0] * r ** (n - 1)
    return [f"Each term is the previous one times r = {fnum(t[1])} ÷ ({fnum(t[0])}) = {fnum(r)} (geometric).",
            f"aₙ = a₁·r^(n - 1), so a{str(n).translate(SUB)} = {fnum(t[0])}·({fnum(r)})^{n - 1} = {fnum(t[0])}·{fnum(r ** (n - 1))}.", f"a{str(n).translate(SUB)} = {fnum(v)}."], float(v)


@fam(r'^Use the Remainder Theorem to find the remainder when P\(x\) = (.+?) is divided by x ([+-]) (\d+)\.')
def _(m, key):
    c = int(m[3]) * (1 if m[2] == '-' else -1)
    expr = m[1].replace('−', '-')
    sub = re.sub(r'(?<![a-zA-Z])x', f'({c})', expr)
    v = ev(expr, {'x': c})
    return [f"By the Remainder Theorem, the remainder when P(x) is divided by x {m[2]} {m[3]} is P({c}).",
            f"P({c}) = {sub}.", f"= {fnum(v)}. The remainder is {fnum(v)}."], v


@fam(r'^Find the sum of the first (\d+) terms of the series (.+?) [+-] …')
def _(m, key):
    n = int(m[1]); terms = [F(x) for x in re.findall(r'[+-]?\d+(?:/\d+)?', m[2].replace(' ', ''))]
    if terms[1] - terms[0] == terms[2] - terms[1]:
        d = terms[1] - terms[0]; an = terms[0] + (n - 1) * d; S = F(n) * (terms[0] + an) / 2
        N = str(n).translate(SUB)
        return [f"Arithmetic: a₁ = {fnum(terms[0])}, d = {fnum(d)}.", f"a{N} = {fnum(terms[0])} + ({n} - 1)({fnum(d)}) = {fnum(an)}.",
                f"S{N} = n(a₁ + aₙ)/2 = {n}({fnum(terms[0])} + ({fnum(an)}))/2 = {n}({fnum(terms[0] + an)})/2 = {fnum(S)}."], float(S)
    r = terms[1] / terms[0]; S = terms[0] * (1 - r ** n) / (1 - r)
    N = str(n).translate(SUB)
    return [f"Geometric: a₁ = {fnum(terms[0])}, r = {fnum(r)}.", f"S{N} = a₁(1 - rⁿ)/(1 - r) = {fnum(terms[0])}(1 - ({fnum(r)})^{n})/(1 - ({fnum(r)})).",
            f"= {fnum(terms[0])}({fnum(1 - r ** n)})/({fnum(1 - r)}) = {fnum(S)}."], float(S)


@fam(r'^\$([\d,]+) is invested at ([\d.]+)% interest compounded continuously\. Find the balance after (\d+) years')
def _(m, key):
    P, r, t = float(m[1].replace(',', '')), float(m[2]) / 100, int(m[3])
    A = P * math.exp(r * t)
    return [f"A = Pe^(rt) with P = {m[1]}, r = {g(r)} and t = {t}.", f"rt = {g(r)} · {t} = {g(r * t)}, and e^{g(r * t)} ≈ {math.exp(r * t):.6f}.",
            f"A ≈ {m[1]} · {math.exp(r * t):.6f} ≈ ${A:,.2f}."], A


@fam(r'^Find c, the distance from the center to each focus, for (.+?) = 1\.')
def _(m, key):
    eq = m[1]
    den = [int(x) for x in re.findall(r'²/(\d+)', eq)]
    if len(den) != 2: return None
    hyper = bool(re.search(r'²/\d+\s*-\s*', eq))
    a2, b2 = (den[0], den[1]) if hyper else (max(den), min(den))
    c2 = a2 + b2 if hyper else a2 - b2
    c = math.sqrt(c2)
    o, i_ = 1, c2
    for f_ in range(2, int(math.isqrt(c2)) + 1):
        while i_ % (f_ * f_) == 0: i_ //= f_ * f_; o *= f_
    cs = str(o) if i_ == 1 else (f"√{i_}" if o == 1 else f"{o}√{i_}")
    if hyper:
        return [f"For a hyperbola, c² = a² + b², where a² is under the positive term.", f"c² = {a2} + {b2} = {c2}.", (f"c = √{c2} = {cs}." if cs != f"√{c2}" else f"c = √{c2}.")], c
    return [f"For an ellipse, c² = a² - b², where a² is the larger denominator.", f"c² = {a2} - {b2} = {c2}.", (f"c = √{c2} = {cs}." if cs != f"√{c2}" else f"c = √{c2}.")], c


@fam(r'^Find the area of a triangle with sides ([\d.]+) (\w+) and ([\d.]+) \w+ and included angle (\d+)°\. Round to the nearest tenth')
def _(m, key):
    a, b, C = float(m[1]), float(m[3]), int(m[4])
    A = 0.5 * a * b * math.sin(C * D)
    return [f"Area = (1/2)ab·sin C with a = {m[1]}, b = {m[3]} and C = {C}°.", f"sin {C}° ≈ {math.sin(C * D):.4f}.",
            f"Area = (1/2)({m[1]})({m[3]})({math.sin(C * D):.4f}) ≈ {A:.1f} {m[2]}²."], A


@fam(r'^Solve e\^\((\d+)x\) = (\d+)\. Give an exact answer\.')
def _(m, key):
    k, c = int(m[1]), int(m[2])
    return [f"Take the natural log of both sides: ln(e^({k}x)) = ln({c}).", f"{k}x = ln({c}).", f"x = ln({c})/{k}."], math.log(c) / k


@fam(r'^Convert (.+?) radians to degrees\.')
def _(m, key):
    v = ev(m[1].replace('−', '-'), {})
    return [f"Multiply by 180°/π.", f"{m[1]} · 180°/π = {fnum(F(v / math.pi).limit_denominator(1000) * 180)}°."], math.degrees(v)


@fam(r'^Find the angle between 0° and 360° that is coterminal with (-?\d+)°\.')
def _(m, key):
    a = int(m[1]); k = -(a // 360); r = a % 360
    op = f"{a}° + {k}(360°)" if k > 0 else f"{a}° - {-k}(360°)"
    return [f"Coterminal angles differ by multiples of 360°.", f"{op} = {r}°, which is between 0° and 360°."], r


@fam(r'^A vector has magnitude (\d+) and direction angle (\d+)°\. Write it in component form, rounding to the nearest hundredth')
def _(m, key):
    r, t = int(m[1]), int(m[2])
    x, y = r * math.cos(t * D), r * math.sin(t * D)
    return [f"v = ⟨|v|cos θ, |v|sin θ⟩ with |v| = {r} and θ = {t}°.", f"cos {t}° ≈ {math.cos(t * D):.4f} and sin {t}° ≈ {math.sin(t * D):.4f}.",
            f"v ≈ ⟨{r}({math.cos(t * D):.4f}), {r}({math.sin(t * D):.4f})⟩ ≈ ⟨{x:.2f}, {y:.2f}⟩."], (x, y)


@fam(r'^Find the determinant of \[(-?\d+), (-?\d+); (-?\d+), (-?\d+)\]\.')
def _(m, key):
    a, b, c, d = map(int, m.groups())
    return [f"For [a, b; c, d], det = ad - bc.", f"det = ({a})({d}) - ({b})({c}) = {a * d} - ({b * c}) = {a * d - b * c}."], a * d - b * c


@fam(r'^A random variable X has (P\(X = .+?)\. Find the expected value E\(X\)\.')
def _(m, key):
    pairs = re.findall(r'P\(X = (-?\d+)\) = ([\d/]+)', m[1])
    terms = [f"({x})({p})" for x, p in pairs]
    v = sum(F(int(x)) * F(p) for x, p in pairs)
    return [f"E(X) = Σ x·P(x).", f"E(X) = {' + '.join(terms)}.", f"= {' + '.join(fnum(F(int(x)) * F(p)) for x, p in pairs)} = {fnum(v)}."], float(v)


@fam(r'How many ways can a club of (\d+) members choose a president and a vice president')
def _(m, key):
    n = int(m[1])
    return [f"Order matters (president and vice president are different jobs), so count permutations.", f"{n} choices for president, then {n - 1} for vice president.",
            f"{n} · {n - 1} = {n * (n - 1)}."], n * (n - 1)


@fam(r'^Find u · v for u = ⟨(-?\d+), (-?\d+)⟩ and v = ⟨(-?\d+), (-?\d+)⟩\.')
def _(m, key):
    a, b, c, d = map(int, m.groups())
    return [f"u · v = u₁v₁ + u₂v₂.", f"= ({a})({c}) + ({b})({d}) = {a * c} + ({b * d}) = {a * c + b * d}."], a * c + b * d


@fam(r'^Find the magnitude of v = ⟨(-?\d+), (-?\d+)⟩\.(?: Give an exact answer\.)?')
def _(m, key):
    a, b = int(m[1]), int(m[2]); s = a * a + b * b
    o, i_ = 1, s
    for f_ in range(2, int(math.isqrt(s)) + 1):
        while i_ % (f_ * f_) == 0: i_ //= f_ * f_; o *= f_
    cs = str(o) if i_ == 1 else (f"√{i_}" if o == 1 else f"{o}√{i_}")
    return [f"|v| = √(a² + b²).", f"= √(({a})² + ({b})²) = √({a * a} + {b * b}) = √{s}."] + ([f"= {cs}."] if cs != f"√{s}" else []), math.sqrt(s)


@fam(r'^Let f\(x\) = (.+?) and x₀ = (-?\d+)\. Find the third iterate')
def _(m, key):
    x = F(int(m[2])); out = []
    for i in (1, 2, 3):
        y = F(ev(m[1].replace('−', '-'), {'x': float(x)})).limit_denominator(100000)
        out.append(f"x{str(i).translate(SUB)} = f({fnum(x)}) = {fnum(y)}.")
        x = y
    return out, float(x)


@fam(r'^A population follows P\(t\) = (\d+)/\(1 \+ (\d+)e\^\((-?[\d.]+)t\)\)\. What is the (carrying capacity|initial population P\(0\))')
def _(m, key):
    L, A = int(m[1]), int(m[2])
    if 'carrying' in m[4]:
        return [f"As t grows, e^({m[3]}t) → 0, so the denominator 1 + {A}e^({m[3]}t) → 1.", f"P(t) → {L}/1 = {L}: the carrying capacity is {L}."], L
    v = L / (1 + A)
    return [f"At t = 0, e⁰ = 1, so P(0) = {L}/(1 + {A}).", f"= {L}/{1 + A} ≈ {v:.4g}."], v


@fam(r'^Evaluate lim \(x → (-?\d+)\) \(x² ([+-]) (\d*)x ([+-]) (\d+)\)/\(x ([+-]) (\d+)\)\.')
def _(m, key):
    c = int(m[1]); b = int(m[3] or 1) * (1 if m[2] == '+' else -1); k = int(m[5]) * (1 if m[4] == '+' else -1)
    r = -int(m[7]) if m[6] == '+' else int(m[7])
    if r != c or c * c + b * c + k != 0: return None
    other = -(b + c)   # x² + bx + k = (x - c)(x - other)
    f1 = f"x {'+' if -c > 0 else '-'} {abs(c)}" if c else "x"
    f2 = f"x {'+' if -other > 0 else '-'} {abs(other)}" if other else "x"
    v = c - other
    return [f"Substituting x = {c} gives 0/0, so factor the numerator: x² {m[2]} {m[3]}x {m[4]} {m[5]} = ({f1})({f2}).".replace(' 1x', ' x'),
            f"Cancel the common factor ({f1}): for x ≠ {c}, the expression equals {f2}.", f"The limit is {c} {'+' if -other >= 0 else '-'} {abs(other)} = {v}."], v


@fam(r'^A trial succeeds with probability ([\d./]+)\. In (\d+) independent trials, find P\(exactly (\d+) success')
def _(m, key):
    p = F(m[1]); n, k = int(m[2]), int(m[3])
    v = math.comb(n, k) * p ** k * (1 - p) ** (n - k)
    show = lambda x: fnum(x) if '/' in m[1] else g(float(x), 6)
    return [f"Binomial: P(X = {k}) = C({n}, {k})·p^{k}·(1 - p)^{n - k} with p = {m[1]}.",
            f"C({n}, {k}) = {math.comb(n, k)}, p^{k} = {show(p ** k)} and (1 - p)^{n - k} = {show((1 - p) ** (n - k))}.",
            f"P = {math.comb(n, k)} · {show(p ** k)} · {show((1 - p) ** (n - k))} = {fnum(v) if '/' in m[1] else f'{float(v):.6f}'}" + (f" ≈ {float(v):.4f}." if '/' not in m[1] else ".")], float(v)


def chain_ok(val, key, text=''):
    try:
        k = keyval(key) if not isinstance(val, tuple) else None
    except Exception:
        k = None
    if isinstance(val, tuple):
        nums = [float(x) for x in re.findall(r'-?\d+(?:\.\d+)?', str(key))]
        return len(nums) == 2 and all(abs(a - b) < 0.006 for a, b in zip(nums, val))
    if k is None:
        return False
    m = re.search(r'\.(\d+)', str(key).replace(',', ''))
    tol = 0.5 * 10 ** -len(m.group(1)) + 1e-9 if m else (0.5 + 1e-9 if re.search(r'nearest (whole|person|integer)', text) else 1e-6 * max(1, abs(k)))
    return abs(k - val) <= tol


def main():
    single = json.load(open(os.path.join(HERE, 'steps', 'single-step.json')))
    banks = load()
    stats = {'single': 0, 'generated': 0, 'mismatch': 0}
    report = []
    for _, q in items(banks):
        if q['id'] in single and len(q.get('solutionSteps') or []) < 2:
            q['solutionSteps'] = single[q['id']]; stats['single'] += 1; continue
        steps = q.get('solutionSteps') or []
        if len(' '.join(steps)) >= 60 or q['format'] not in ('short-answer', 'multiple-choice'):
            continue
        text = inner(q)
        for rx, fn in FAMS:
            m = rx.search(text)
            if not m:
                continue
            got = fn(m, q['answer'])
            if not got:
                break
            new, val = got
            if not chain_ok(val, q['answer'], text):
                stats['mismatch'] += 1; report.append((q['id'], q['answer'], val)); break
            if steps and steps[0].startswith('Mistake:'):
                tail = [s for s in steps if s.startswith('The correct answer') or s.startswith('Correct answer')]
                new = [steps[0]] + new + tail
            else:
                new = new + [f"Answer: {q['answer']}."] if not str(q['answer']).strip() in new[-1] else new
            q['solutionSteps'] = new
            stats['generated'] += 1
            break
    save(banks)
    print(stats)
    for r in report[:30]:
        print('mismatch', r)


if __name__ == '__main__':
    main()
