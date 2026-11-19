"""Grade 7 audit #2 (2026-11-19): recompute Grade 7 answer keys from the printed prompts.

The authoring verifier (tools/middle-grades-authoring/gverify.py) checks items against specs saved when the banks were
first built, and many items were rewritten after that. This checker needs no saved specs: it reads each prompt as a
student sees it, works the problem with sympy (exact rational arithmetic), and compares the result with the key.
Error-analysis items are checked on the problem they quote. Multiple-choice items must key the option that equals the
answer. Items whose prompt shape is not recognised are skipped and counted; at least MIN keys must be checked.

Usage: python3 tools/grade7-audit-20261119/verify_keys.py [--list]
"""
import glob, json, math, os, re, sys
from fractions import Fraction as F
import sympy as sp
from sympy.parsing.sympy_parser import parse_expr, standard_transformations, implicit_multiplication_application, convert_xor, rationalize

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
MIN = 2250
TR = standard_transformations + (implicit_multiplication_application, convert_xor, rationalize)
SUP = str.maketrans('⁰¹²³⁴⁵⁶⁷⁸⁹⁻ˣ', '0123456789-x')


class Skip(Exception):
    pass


def sup_to_pow(s):
    return re.sub(r'([⁰¹²³⁴⁵⁶⁷⁸⁹⁻ˣ]+)', lambda m: '**(' + m.group(1).translate(SUP) + ')', s)


def mixed(s):
    return re.sub(r'(?<![\d.\/])(-?)(\d+) (\d+)/(\d+)(?![\d/])', lambda m: f'{m.group(1)}({m.group(2)}+{m.group(3)}/{m.group(4)})', s)


def clean(s):
    s = s.replace('−', '-').replace('–', '-').replace('×', '*').replace('·', '*').replace('÷', '/').replace('[', '(').replace(']', ')')
    s = s.replace('$', '').replace(',', '') if re.fullmatch(r'[\s\d$,.\-+*/()]+', s) else s
    s = re.sub(r'(\d),(\d{3})', r'\1\2', s)
    s = mixed(s)
    s = re.sub(r'(?<![\w)./])(\d+(?:\.\d+)?)/(\d+(?:\.\d+)?)(?![\w(./])', r'(\1/\2)', s)
    s = sup_to_pow(s)
    s = re.sub(r'∛\(([^)]*)\)', r'cbrt(\1)', s); s = re.sub(r'∛(-?\d+)', r'cbrt(\1)', s)
    s = re.sub(r'√\(([^)]*)\)', r'sqrt(\1)', s); s = re.sub(r'√(\d+)', r'sqrt(\1)', s)
    s = re.sub(r'\|([^|]+)\|', r'Abs(\1)', s)
    s = s.replace('π', 'pi')
    return s.strip()


def cbrt(v):
    v = sp.nsimplify(v)
    r = sp.real_root(v, 3)
    return sp.nsimplify(r)


def ex(s):
    s = clean(s)
    if not s or re.search(r'[a-zA-Z]{3,}', re.sub(r'\b(sqrt|cbrt|Abs|pi)\b', '', s)):
        raise Skip('words')
    return parse_expr(s, transformations=TR, local_dict={'cbrt': cbrt, 'Abs': sp.Abs, 'pi': sp.pi}, evaluate=True)


def num(s):
    """A key or option as an exact number: '−3', '2 1/2', '$7.11', '57 m²', '16π cm²', '7√3', '1/12'."""
    t = str(s).replace('−', '-').strip().rstrip('.')
    t = re.sub(r'^\$', '', t).replace(',', '')
    t = re.sub(r'\s*(%|°|square units|cubic units|units|[a-zA-Z][a-zA-Z .²³]*)$', '', t).strip()
    if not t:
        raise Skip('no number')
    return exact(ex(t))


def exact(v):
    v = sp.sympify(v)
    return v.xreplace({f: sp.Rational(str(f)) for f in v.atoms(sp.Float)})


def same(a, b, tol=None):
    a, b = exact(a), exact(b)
    if tol is not None:
        return abs(float(a) - float(b)) <= tol + 1e-9
    return sp.simplify(a - b) == 0


def rounding_tol(prompt):
    p = prompt.lower()
    for k, v in [('nearest hundredth', 0.005), ('two decimal', 0.005), ('nearest tenth', 0.05), ('one decimal', 0.05),
                 ('nearest whole', 0.5), ('nearest foot', 0.5), ('nearest meter', 0.5), ('nearest cent', 0.005),
                 ('nearest degree', 0.5), ('three decimal', 0.0005), ('nearest thousandth', 0.0005)]:
        if k in p:
            return v + 1e-9
    return None


VAR = re.compile(r'(?<![a-zA-Z])([a-z])(?![a-zA-Z])')


def problem_text(q):
    """The problem a student must solve: error-analysis items quote it between the name line and '<Name>'s answer'."""
    p = q['prompt']
    if 'answered this problem incorrectly' in p:
        lines = [l for l in p.split('\n') if l.strip()]
        body = [l for l in lines[1:] if not re.search(r"'s answer:|Identify the mistake", l)]
        return ' '.join(body)
    return p.replace('\n', ' ')


def solve_eq(text, key):
    m = re.match(r'^(?:Solve(?: the equation)?|Solve for \w)\s*[:.]?\s*(.+?)\s*$', text)
    if not m:
        raise Skip('not solve')
    body = re.split(r'\.\s+(?=If |Check|Round|Write)', m.group(1))[0].rstrip('.')
    rel = re.search(r'(≤|≥|<=|>=|<|>|=)', body)
    if not rel:
        raise Skip('no relation')
    vs = sorted(set(VAR.findall(re.sub(r'\b(sqrt|cbrt|Abs)\b', '', body))))
    if len(vs) != 1:
        raise Skip('vars')
    v = sp.Symbol(vs[0])
    op = rel.group(1)
    L, R = body.split(op, 1)
    L, R = ex(L), ex(R)
    k = str(key).replace('−', '-').strip().rstrip('.')
    if op == '=':
        sol = sp.solve(sp.Eq(L, R), v)
        if sp.simplify(L - R) == 0:
            return re.search(r'infinite|all real', k, re.I) is not None
        if not sol:
            return re.search(r'no solution', k, re.I) is not None
        km = re.match(r'^(?:' + vs[0] + r'\s*=\s*)?(.+)$', k)
        return any(same(s, num(km.group(1))) for s in sol)
    # inequality: compare solution sets
    rel_s = {'<': sp.Lt, '>': sp.Gt, '≤': sp.Le, '<=': sp.Le, '≥': sp.Ge, '>=': sp.Ge}
    want = sp.solve_univariate_inequality(rel_s[op](L, R), v, relational=False)
    km = re.match(r'^\s*([a-z])\s*(≤|≥|<=|>=|<|>)\s*(.+)$', k)
    if not km or km.group(1) != vs[0]:
        return False
    got = sp.solve_univariate_inequality(rel_s[km.group(2)](v, num(km.group(3))), v, relational=False)
    return want == got


def evaluate(text, key):
    m = re.match(r'^(?:Evaluate|Find the (?:sum|difference|product|quotient)|Simplify|Find the value of the expression|Compute)\s*[:.]\s*(.+?)\s*$', text)
    if not m:
        raise Skip('not evaluate')
    body = m.group(1).rstrip('.')
    if VAR.search(re.sub(r'\b(sqrt|cbrt|Abs)\b', '', clean(body))):
        raise Skip('has variable')
    v = ex(body)
    tol = rounding_tol(text)
    return same(v, num(key), tol)


def simplify_expr(text, key):
    m = re.match(r'^(?:Simplify|Multiply|Expand|Add|Subtract|Combine like terms|Simplify\. Assume x ≠ 0\.|Use the Distributive Property to simplify)\s*[:.]?\s*(.+?)\s*$', text)
    if not m or not VAR.search(m.group(1)):
        raise Skip('not expr')
    body = re.sub(r'^Assume [a-z] ≠ 0\.\s*', '', m.group(1)).rstrip('.')
    if '=' in body or '=' in str(key):
        raise Skip('equation')
    return sp.simplify(ex(body) - ex(str(key))) == 0


def as_power(text, key):
    m = re.match(r'^Simplify\. Write your answer as a power\s*:\s*(.+)$', text)
    if not m:
        raise Skip('not power')
    k = str(key)
    if not re.fullmatch(r'-?\(?-?\d+\)?[⁰¹²³⁴⁵⁶⁷⁸⁹⁻]+', k.replace('−', '-')):
        return False
    return same(ex(m.group(1)), ex(k))


UNITS = {'mg': ('g', F(1, 1000)), 'g': ('g', 1), 'kg': ('g', 1000), 'mm': ('m', F(1, 1000)), 'cm': ('m', F(1, 100)), 'm': ('m', 1),
         'km': ('m', 1000), 'mL': ('L', F(1, 1000)), 'L': ('L', 1), 'kL': ('L', 1000), 'inches': ('in', 1), 'inch': ('in', 1), 'in.': ('in', 1),
         'feet': ('in', 12), 'foot': ('in', 12), 'ft': ('in', 12), 'yards': ('in', 36), 'yard': ('in', 36), 'yd': ('in', 36), 'miles': ('in', 63360),
         'mile': ('in', 63360), 'ounces': ('oz', 1), 'oz': ('oz', 1), 'pounds': ('oz', 16), 'pound': ('oz', 16), 'lb': ('oz', 16), 'tons': ('oz', 32000),
         'ton': ('oz', 32000), 'cups': ('c', 1), 'cup': ('c', 1), 'pints': ('c', 2), 'pint': ('c', 2), 'quarts': ('c', 4), 'quart': ('c', 4),
         'gallons': ('c', 16), 'gallon': ('c', 16), 'fluid ounces': ('c', F(1, 8))}


def measure(s):
    m = re.fullmatch(r'\s*(-?[\d.,]+(?: \d+/\d+)?)\s*(fluid ounces|[a-zA-Z.]+)\s*', s)
    if not m or m.group(2) not in UNITS:
        return None
    base, f = UNITS[m.group(2)]
    return base, num(m.group(1)) * sp.nsimplify(f)


def compare(text, key):
    m = re.match(r'^Compare using <, >, or =\s*:\s*(.+?)\s*___\s*(.+?)\s*$', text)
    if not m:
        raise Skip('not compare')
    ma, mb = measure(m.group(1)), measure(m.group(2))
    if ma and mb:
        if ma[0] != mb[0]:
            raise Skip('units')
        a, b = ma[1], mb[1]
        want = '<' if a < b else '>' if a > b else '='
        return str(key).strip() == want
    try:
        a, b = num(m.group(1)), num(m.group(2))
    except Exception:
        a, b = ex(m.group(1)), ex(m.group(2))
    want = '<' if a < b else '>' if a > b else '='
    return str(key).strip() == want


def system(text, key):
    m = re.match(r'^Solve the system by (?:substitution|elimination|graphing)\s*:\s*(.+?)\s+and\s+(.+?)\.?$', text)
    if not m:
        raise Skip('not system')
    x, y = sp.symbols('x y')
    eqs = []
    for e in (m.group(1), m.group(2)):
        L, R = e.split('=')
        eqs.append(sp.Eq(ex(L), ex(R)))
    sol = sp.solve(eqs, [x, y], dict=True)
    k = str(key).replace('−', '-')
    km = re.match(r'^\(\s*(.+?)\s*,\s*(.+?)\s*\)$', k)
    if not sol or not km:
        return bool(re.search(r'no solution', k, re.I)) and not sol
    return same(sol[0][x], num(km.group(1))) and same(sol[0][y], num(km.group(2)))


# Word templates: (regex on the problem text, function of the match groups → expected value, comparison)
def d(s):
    return sp.Rational(s.replace(',', ''))


WORD = [
    (r'A value changes from ([\d.,]+) to ([\d.,]+)\. Find the percent of change', lambda g, k: (lambda a, b: same(abs(b - a) / a * 100, num(k.split('%')[0]), 0.05) and (('increase' in k) == (b > a)))(d(g[0]), d(g[1]))),
    (r'What is ([\d.]+)% of ([\d.,]+)\?', lambda g, k: same(d(g[0]) / 100 * d(g[1]), num(k), 0.005)),
    (r'Write ([\d.]+)% as a decimal', lambda g, k: same(d(g[0]) / 100, num(k))),
    (r'A \$([\d.,]+) item is on sale for ([\d.]+)% off\. What is the sale price', lambda g, k: same(d(g[0]) * (1 - d(g[1]) / 100), num(k), 0.005)),
    (r'A store buys an item for \$([\d.,]+) and marks it up ([\d.]+)%\. What is the selling price', lambda g, k: same(d(g[0]) * (1 + d(g[1]) / 100), num(k), 0.005)),
    (r'After a ([\d.]+)% discount, a (?:\w+ )+costs \$([\d.,]+)\. What was the original price', lambda g, k: same(d(g[1]) / (1 - d(g[0]) / 100), num(k), 0.005)),
    (r'Find the simple interest earned on \$([\d.,]+) at ([\d.]+)% per year for (\d+) years', lambda g, k: same(d(g[0]) * d(g[1]) / 100 * d(g[2]), num(k), 0.005)),
    (r'\$([\d.,]+) is invested at ([\d.]+)% interest compounded annually\. What is the balance after (\d+) years', lambda g, k: same(d(g[0]) * (1 + d(g[1]) / 100) ** int(g[2]), num(k), 0.006)),
    (r'A town of ([\d,]+) people grows ([\d.]+)% per year\. What is the population after (\d+) years', lambda g, k: int(sp.floor(d(g[0]) * (1 + d(g[1]) / 100) ** int(g[2]) + sp.Rational(1, 2))) == int(num(k))),
    (r'Find the area of the parallelogram\. Base = ([\d.]+) \w+, height = ([\d.]+)', lambda g, k: same(d(g[0]) * d(g[1]), num(k))),
    (r'Find the area of a parallelogram with base ([\d.]+) \w+ and height ([\d.]+)', lambda g, k: same(d(g[0]) * d(g[1]), num(k))),
    (r'Find the area of a trapezoid with bases ([\d.]+) \w+ and ([\d.]+) \w+ and height ([\d.]+)', lambda g, k: same((d(g[0]) + d(g[1])) / 2 * d(g[2]), num(k))),
    (r'Find the area of a triangle with base ([\d.]+) \w+ and height ([\d.]+)', lambda g, k: same(d(g[0]) * d(g[1]) / 2, num(k))),
    (r'A triangle has area ([\d.]+) \w+² and base ([\d.]+) \w+\. Find its height', lambda g, k: same(2 * d(g[0]) / d(g[1]), num(k))),
    (r'A circle has a radius of ([\d.]+) \w+\. Find its area in terms of π', lambda g, k: same(d(g[0]) ** 2 * sp.pi, num(k))),
    (r'A circle has a diameter of ([\d.]+) \w+\. Find its area in terms of π', lambda g, k: same((d(g[0]) / 2) ** 2 * sp.pi, num(k))),
    (r'Find the volume of a cylinder with radius ([\d.]+) \w+ and height ([\d.]+) \w+\. Write the answer in terms of π', lambda g, k: same(d(g[0]) ** 2 * d(g[1]) * sp.pi, num(k))),
    (r'Find the volume of a sphere with radius ([\d.]+) \w+\. Write the answer in terms of π', lambda g, k: same(sp.Rational(4, 3) * d(g[0]) ** 3 * sp.pi, num(k))),
    (r'Find the volume of a rectangular prism ([\d.]+) \w+\.? long, ([\d.]+) \w+\.? wide, and ([\d.]+) \w+\.? (?:high|tall)', lambda g, k: same(d(g[0]) * d(g[1]) * d(g[2]), num(k))),
    (r'Find the surface area of a rectangular prism ([\d.]+) \w+ long, ([\d.]+) \w+ wide, and ([\d.]+) \w+ (?:high|tall)', lambda g, k: (lambda l, w, h: same(2 * (l * w + l * h + w * h), num(k)))(d(g[0]), d(g[1]), d(g[2]))),
    (r'A square pyramid has base edge ([\d.]+) \w+ and slant height ([\d.]+) \w+\. Find its surface area', lambda g, k: same(d(g[0]) ** 2 + 2 * d(g[0]) * d(g[1]), num(k))),
    (r'Find the volume of a square pyramid with base edge ([\d.]+) \w+ and height ([\d.]+)', lambda g, k: same(d(g[0]) ** 2 * d(g[1]) / 3, num(k))),
    (r'A rectangular prism has volume ([\d.,]+) \w+³, length ([\d.]+) \w+, and width ([\d.]+) \w+\. Find its height', lambda g, k: same(d(g[0]) / (d(g[1]) * d(g[2])), num(k))),
    (r'Can the side lengths ([\d.]+), ([\d.]+), and ([\d.]+) form a right triangle', lambda g, k: (sorted(map(d, g))[0] ** 2 + sorted(map(d, g))[1] ** 2 == sorted(map(d, g))[2] ** 2) == k.strip().lower().startswith('yes')),
    (r'Find the slope of the line through \((-?[\d.]+), (-?[\d.]+)\) and \((-?[\d.]+), (-?[\d.]+)\)', lambda g, k: same((d(g[3]) - d(g[1])) / (d(g[2]) - d(g[0])), num(k))),
    (r'Find the midpoint of the segment with endpoints \((-?[\d.]+), (-?[\d.]+)\) and \((-?[\d.]+), (-?[\d.]+)\)', lambda g, k: (lambda m: m and same((d(g[0]) + d(g[2])) / 2, num(m.group(1))) and same((d(g[1]) + d(g[3])) / 2, num(m.group(2))))(re.match(r'\((.+?), (.+?)\)', k.replace('−', '-')))),
    (r'Find the distance between \((-?[\d.]+), (-?[\d.]+)\) and \((-?[\d.]+), (-?[\d.]+)\)', lambda g, k: same(sp.sqrt((d(g[2]) - d(g[0])) ** 2 + (d(g[3]) - d(g[1])) ** 2), num(k))),
    (r'Find the GCF of ([\d, and]+)\.', lambda g, k: math.gcd(*[int(x) for x in re.findall(r'\d+', g[0])]) == int(num(k))),
    (r'Find the greatest common factor \(GCF\) of (\d+) and (\d+)', lambda g, k: math.gcd(int(g[0]), int(g[1])) == int(num(k))),
    (r'Write ([\d,]+) in scientific notation', lambda g, k: same(d(g[0]), ex(k)) and re.fullmatch(r'[1-9](\.\d+)? × 10[⁰¹²³⁴⁵⁶⁷⁸⁹⁻]+', k.strip()) is not None),
    (r'Write ([\d.]+) × 10([⁰¹²³⁴⁵⁶⁷⁸⁹⁻]+) in standard form', lambda g, k: same(d(g[0]) * sp.Integer(10) ** int(g[1].translate(SUP)), num(k))),
    (r'√(\d+) is closest to which whole number', lambda g, k: abs(math.sqrt(int(g[0])) - int(num(k))) < 0.5),
    (r'Between which two consecutive whole numbers is √(\d+)', lambda g, k: (lambda n: [int(x) for x in re.findall(r'\d+', k)] == [math.isqrt(n), math.isqrt(n) + 1])(int(g[0]))),
    (r'Write (\d+)/(\d+) in simplest form', lambda g, k: same(sp.Rational(int(g[0]), int(g[1])), num(k)) and math.gcd(*[int(x) for x in re.findall(r'\d+', k)][-2:]) == 1),
    (r'Write (\d+)/(\d+) as a decimal\.', lambda g, k: True if 'repeat' in k else same(sp.Rational(int(g[0]), int(g[1])), num(k))),
    (r'In a (?:30°-60°-90°|30-60-90) triangle, the shorter leg is ([\d.]+)\. Find the longer leg', lambda g, k: same(d(g[0]) * sp.sqrt(3), num(k))),
    (r'In a (?:30°-60°-90°|30-60-90) triangle, the shorter leg is ([\d.]+)\. Find the hypotenuse', lambda g, k: same(2 * d(g[0]), num(k))),
    (r'In a 45°-45°-90° triangle, each leg is ([\d.]+)\. Find the hypotenuse', lambda g, k: same(d(g[0]) * sp.sqrt(2), num(k))),
    (r'Two angles are supplementary\. One measures ([\d.]+)°\. What is the other', lambda g, k: same(180 - d(g[0]), num(k))),
    (r'Two angles are complementary\. One measures ([\d.]+)°\. What is the other', lambda g, k: same(90 - d(g[0]), num(k))),
    (r'A triangle has angles ([\d.]+)°, ([\d.]+)°, and x°\. Find x', lambda g, k: same(180 - d(g[0]) - d(g[1]), num(re.search(r'x = (-?[\d.]+)', k).group(1)))),
    (r'Use d = rt to find the distance traveled at ([\d.]+) miles per hour for ([\d.]+) hours', lambda g, k: same(d(g[0]) * d(g[1]), num(k))),
    (r'Find the probability of getting a (\d) on a number cube and a (\d) on a number cube', lambda g, k: same(sp.Rational(1, 36), num(k))),
    (r'A bag has (\d+) (\w+), (\d+) (\w+), (\d+) (\w+) marbles\. One marble is picked at random\. What is P\((\w+)\)', lambda g, k: same(sp.Rational(int(dict([(g[1], g[0]), (g[3], g[2]), (g[5], g[4])])[g[6]]), int(g[0]) + int(g[2]) + int(g[4])), num(k))),
    (r'A bag has (\d+) red and (\d+) blue marbles\. You draw a marble, do NOT replace it, and draw again\. What is P\(red, then red\)', lambda g, k: (lambda r, b: same(sp.Rational(r, r + b) * sp.Rational(r - 1, r + b - 1), num(k)))(int(g[0]), int(g[1]))),
    (r'In (\d+) trials, .* (\d+) times\. What is the experimental probability', lambda g, k: same(sp.Rational(int(g[1]), int(g[0])), num(k))),
    (r'How many different (\d+)-person committees can be chosen from (\d+)', lambda g, k: math.comb(int(g[1]), int(g[0])) == int(num(k))),
    (r'Write the prime factorization of (\d+) using exponents', lambda g, k: same(ex(k), d(g[0])) and all(sp.isprime(int(b)) for b in re.findall(r'(\d+)(?:[⁰¹²³⁴⁵⁶⁷⁸⁹]*)', k))),
    (r'Find the value of y when x = (-?[\d.]+) for the equation (.+?)\.?$', lambda g, k: (lambda x, y: same(sp.solve(sp.Eq(*[ex(t).subs(x, d(g[0])) for t in g[1].split('=')]), y)[0], num(k.split('=')[-1])))(sp.Symbol('x'), sp.Symbol('y'))),
    (r'In right triangle ABC, ∠C is the right angle, BC = (\d+), AC = (\d+), and AB = (\d+)\. Find (sin|cos|tan) A', lambda g, k: same({'sin': sp.Rational(int(g[0]), int(g[2])), 'cos': sp.Rational(int(g[1]), int(g[2])), 'tan': sp.Rational(int(g[0]), int(g[1]))}[g[3]], num(k))),
    (r'A trend line for a scatter plot .* is y = (.+?)\. Predict the .* for ([\d.]+) ', lambda g, k: same(ex(g[0]).subs(sp.Symbol('x'), d(g[1])), num(k))),
    (r'^Write ([\d.]+) as a fraction in simplest form', lambda g, k: same(d(g[0]), num(k)) and (lambda f: math.gcd(int(f[0]), int(f[1])) == 1)(re.findall(r'\d+', k.split(' ')[-1])[-2:]) if '/' in k else same(d(g[0]), num(k))),
    (r'From a point ([\d.]+) ft from the base of a building, the angle of elevation to the top is ([\d.]+)°\. (?:\w+\'s eyes are ([\d.]+) ft above the ground\. )?How tall is the building, to the nearest foot', lambda g, k: abs(float(d(g[0])) * math.tan(math.radians(float(g[1]))) + (float(g[2]) if g[2] else 0) - float(num(k))) <= 0.5 + 1e-9),
    (r'From the top of a ([\d.]+)-ft lighthouse, the angle of depression to a boat is ([\d.]+)°\. How far is the boat from the base of the lighthouse, to the nearest foot', lambda g, k: abs(float(g[0]) / math.tan(math.radians(float(g[1]))) - float(num(k))) <= 0.5 + 1e-9),
    (r'In a right triangle, an acute angle measures ([\d.]+)° and the side adjacent to it is ([\d.]+) \w+\. Find the side opposite the angle, to the nearest tenth', lambda g, k: abs(float(g[1]) * math.tan(math.radians(float(g[0]))) - float(num(k))) <= 0.05 + 1e-9),
    (r'Estimate ([\d.]+) × ([\d.]+) by rounding each factor to the nearest whole number', lambda g, k: round_half(d(g[0])) * round_half(d(g[1])) == num(k)),
    (r'Estimate by rounding each number to the nearest whole number: ((?:[\d.]+ [+−-] )+[\d.]+)', lambda g, k: sum((-1 if sgn == '−' or sgn == '-' else 1) * round_half(d(v)) for sgn, v in re.findall(r'(^|[+−-]) ?([\d.]+)', g[0])) == num(k)),
    (r'Adult tickets cost \$(\d+) and child tickets cost \$(\d+)\. A group bought (\d+) tickets for \$(\d+)\. How many adult tickets', lambda g, k: (lambda a, c, n, t: same(sp.Rational(t - c * n, a - c), num(k)))(*map(int, g))),
    (r'A theater sold (\d+) tickets for \$(\d+)\. Adult tickets cost \$(\d+) and child tickets cost \$(\d+)\. How many adult tickets', lambda g, k: (lambda n, t, a, c: same(sp.Rational(t - c * n, a - c), num(k)))(*map(int, g))),
    (r'A jar has (\d+) quarters and dimes worth \$([\d.]+)\. How many quarters', lambda g, k: (lambda n, cents: same(sp.Rational(cents - 10 * n, 15), num(k)))(int(g[0]), int(round(float(g[1]) * 100)))),
    (r'Write and solve an equation: What is ([\d.]+)% of ([\d.,]+)\?', lambda g, k: same(d(g[0]) * d(g[1]) / 100, num(k.split('=')[-1]))),
    (r'(?:Write and solve an equation: )?([\d.]+) is ([\d.]+)% of what number\?', lambda g, k: same(d(g[0]) * 100 / d(g[1]), num(k.split('=')[-1]))),
    (r'(?:Write and solve an equation: )?([\d.]+) is what percent of ([\d.]+)\?', lambda g, k: same(d(g[0]) * 100 / d(g[1]), num(k.split('=')[-1].replace('%', '')))),
    (r'In a 45°-45°-90° triangle, the hypotenuse is ([\d.]+)√2\. Find the length of each leg', lambda g, k: same(d(g[0]), num(k))),
    (r'There are (\d+) points, and no three of them lie on the same line\. How many different lines', lambda g, k: math.comb(int(g[0]), 2) == int(num(k))),
    (r'Use inductive reasoning to find the next term: ((?:-?\d+, )+-?\d+), …', lambda g, k: next_term([int(x) for x in g[0].split(', ')]) == int(num(k))),
    (r'A bag has (\d+) red and (\d+) blue marbles\. You draw a marble, replace it, and draw again\. What is P\(red, then red\)', lambda g, k: same(sp.Rational(int(g[0]), int(g[0]) + int(g[1])) ** 2, num(k))),
    (r'The (?:triangles|rectangles) are similar\. The small one has sides ([\d.]+) cm and ([\d.]+) cm\. The corresponding sides of the large one are ([\d.]+) cm and x cm', lambda g, k: same(d(g[1]) * d(g[2]) / d(g[0]), num(k.split('=')[-1]))),
    (r'Is the relationship proportional\? x: ([\d, .-]+); y: ([\d, .-]+)$', lambda g, k: (len({d(b) / d(a) for a, b in zip(g[0].split(', '), g[1].split(', '))}) == 1) == k.strip().lower().startswith('yes')),
    (r'The table shows a proportional relationship \(x: ([\d, .]+); y: ([\d, .?]+)\)\. What is the missing y-value', lambda g, k: (lambda xs, ys: same(d(xs[ys.index('?')]) * [d(b) / d(a) for a, b in zip(xs, ys) if b != '?'][0], num(k)))(g[0].split(', '), g[1].split(', '))),
    (r'Ray BD bisects ∠ABC, which measures ([\d.]+)°\. What is m∠ABD', lambda g, k: same(d(g[0]) / 2, num(k))),
    (r'Point M lies on the perpendicular bisector of segment AB\. MA = ([\d.]+) cm\. What is MB', lambda g, k: same(d(g[0]), num(k))),
    (r'What is the value of the digit (\d) in ([\d,]+)\?', lambda g, k: (lambda n: same(int(g[0]) * 10 ** (len(n) - 1 - n.index(g[0])), num(k)))(g[1].replace(',', ''))),
    (r'Use compatible numbers to estimate ([\d.]+) ÷ ([\d.]+)\.', lambda g, k: True if num(k) > 0 and abs(float(d(g[0]) / d(g[1])) - float(num(k))) / float(num(k)) < 0.25 else False),
    (r'Twice a number increased by (\d+) is (\d+)\. Find the number', lambda g, k: same(sp.Rational(int(g[1]) - int(g[0]), 2), num(k))),
    (r'Point A\((-?\d+), (-?\d+)\) is rotated (90|180|270)° counterclockwise about the origin', lambda g, k: (lambda x, y, a, m: m is not None and (int(num(m.group(1))), int(num(m.group(2)))) == {90: (-y, x), 180: (-x, -y), 270: (y, -x)}[a])(int(g[0]), int(g[1]), int(g[2]), re.match(r'\((.+?), (.+?)\)', k.replace('−', '-')))),
    (r'A frequency table shows the number of values in each interval: (.+?)\. How many values are there in all', lambda g, k: sum(int(x) for x in re.findall(r': (\d+)', g[0])) == int(num(k))),
    (r'Use P = 2l \+ 2w to find the perimeter of a rectangle with l = ([\d.]+) \w+ and w = ([\d.]+)', lambda g, k: same(2 * d(g[0]) + 2 * d(g[1]), num(k))),
    (r'A train travels ([\d.]+) miles in ([\d.]+) hours\. Use d = rt to find its rate', lambda g, k: same(d(g[0]) / d(g[1]), num(k))),
    (r'A rectangle has width (\d+)x and length \(x \+ (\d+)\)\. Write a simplified expression for its area', lambda g, k: sp.expand(int(g[0]) * sp.Symbol('x') * (sp.Symbol('x') + int(g[1])) - ex(k)) == 0),
    (r'A (?:mother|father) is (\d+) times as old as (?:her|his) (?:son|daughter)\. The sum of their ages is (\d+)\. How old is the', lambda g, k: same(sp.Rational(int(g[1]), int(g[0]) + 1), num(k))),
    (r'(?:\w+) is (\d+) times as old as (?:his|her|their) cousin\. The sum of their ages is (\d+)\. How old is the cousin', lambda g, k: same(sp.Rational(int(g[1]), int(g[0]) + 1), num(k))),
    (r'Subtract\. Write the answer in simplest form: (.+?)$', lambda g, k: same(ex(g[0]), num(k))),
    (r'Add\. Write the answer in simplest form: (.+?)$', lambda g, k: same(ex(g[0]), num(k))),
    (r'Multiply\. Write the answer in simplest form: (.+?)$', lambda g, k: same(ex(g[0]), num(k))),
    (r'Divide\. Write the answer in simplest form: (.+?)$', lambda g, k: same(ex(g[0]), num(k))),
    (r'A right triangle has legs ([\d.]+) \w+ and ([\d.]+) \w+\. How long is the hypotenuse', lambda g, k: same(sp.sqrt(d(g[0]) ** 2 + d(g[1]) ** 2), num(k))),
    (r'How many factors does (\d+) have', lambda g, k: len(sp.divisors(int(g[0]))) == int(num(k))),
    (r'Does y = ([\d.]+)\(([\d.]+)\)ˣ show exponential growth or exponential decay', lambda g, k: ('growth' in k) == (d(g[1]) > 1)),
    (r'Order from least to greatest: (.+?)$', lambda g, k: sorted(num(x) for x in g[0].split(', ')) == [num(x) for x in k.split(', ')] and sorted(g[0].split(', ')) == sorted(k.split(', '))),
    (r'A rectangle has length \((\d+)x \+ (\d+)\) cm and width x cm\. Its perimeter is (\d+) cm\. Find x', lambda g, k: same(sp.Rational(int(g[2]) - 2 * int(g[1]), 2 * int(g[0]) + 2), num(k.split('=')[-1]))),
    (r'Trees are planted in a row, (\d+) meters apart\. There are (\d+) trees\. How far', lambda g, k: int(g[0]) * (int(g[1]) - 1) == int(num(k))),
    (r'Round ([\d.]+) to the nearest (whole number|tenth|hundredth)', lambda g, k: round_half(d(g[0]), {'whole number': 0, 'tenth': 1, 'hundredth': 2}[g[1]]) == num(k)),
    (r'What is the value of the digit (\d) in ([\d,]*\.\d+)\?', lambda g, k: (lambda n: same(int(g[0]) * sp.Integer(10) ** (n.index('.') - n.index(g[0]) - (1 if n.index(g[0]) < n.index('.') else 0)), num(k)))(g[1].replace(',', ''))),
    (r'Write the number in standard form: (.+)$', lambda g, k: same(ex(g[0]), num(k))),
    (r'Find the value: (.+)$', lambda g, k: same(ex(g[0]), num(k))),
    (r'Write (?:([\d,.]+)|1/([\d,]+)) as a power of 10\.', lambda g, k: re.fullmatch(r'10[⁰¹²³⁴⁵⁶⁷⁸⁹⁻]+', k.strip()) is not None and same(ex(k), d(g[0]) if g[0] else 1 / d(g[1]))),
    (r'How many times as large as (.+?) is (.+?)\?', lambda g, k: same(ex(g[1]) / ex(g[0]), num(k))),
    (r'The digit \d appears in ([\d,.]+) and in ([\d,.]+)\. The value of the \d in [\d,.]+ is how many times the value', lambda g, k: same(d(g[0]) / d(g[1]), num(k))),
    (r'How many \w+ \(\$([\d.]+) each\) have the same value as \$([\d,.]+)\?', lambda g, k: same(d(g[1]) / d(g[0]), num(k))),
    (r'of about (\d) × 10([⁰¹²³⁴⁵⁶⁷⁸⁹⁻]+) \w+, and .+ of about (\d) × 10([⁰¹²³⁴⁵⁶⁷⁸⁹⁻]+) \w+\. About how many times as large', lambda g, k: same(sp.Integer(int(g[2])) * sp.Integer(10) ** int(g[3].translate(SUP)) / (sp.Integer(int(g[0])) * sp.Integer(10) ** int(g[1].translate(SUP))), num(k))),
    (r'A ([\d.]+)-\w+ \w+ (?:costs|is priced at) \$([\d.]+)\.', lambda g, k: (_ for _ in ()).throw(Skip('ambiguous'))),
]


def round_half(v, places=0):
    q = sp.Integer(10) ** places
    return sp.floor(exact(v) * q + sp.Rational(1, 2)) / q


def next_term(xs):
    d1 = [b - a for a, b in zip(xs, xs[1:])]
    if len(set(d1)) == 1:
        return xs[-1] + d1[0]
    if all(a != 0 for a in xs) and len({F(b, a) for a, b in zip(xs, xs[1:])}) == 1:
        r = F(xs[1], xs[0]); v = xs[-1] * r
        if v.denominator == 1:
            return int(v)
    if all(xs[i] == xs[i - 1] + xs[i - 2] for i in range(2, len(xs))):
        return xs[-1] + xs[-2]
    d2 = [b - a for a, b in zip(d1, d1[1:])]
    if len(set(d2)) == 1:
        return xs[-1] + d1[-1] + d2[0]
    raise Skip('pattern')


def word(text, key):
    for pat, fn in WORD:
        m = re.search(pat, text)
        if m:
            return fn(m.groups(), str(key))
    raise Skip('no template')


CHECKERS = [solve_eq, system, compare, as_power, evaluate, simplify_expr, word]


def check(q):
    key = q.get('answer')
    if not isinstance(key, str):
        raise Skip('non-string key')
    text = problem_text(q)
    last = None
    for fn in CHECKERS:
        try:
            return fn(text, key)
        except Skip as e:
            last = e
        except (sp.SympifyError, SyntaxError, TypeError, ValueError, ZeroDivisionError, AttributeError, IndexError, KeyError) as e:
            last = Skip(type(e).__name__)
    raise last or Skip('none')


def mc_consistent(q):
    if q.get('format') != 'multiple-choice':
        return True
    keyed = [o['text'] for o in q.get('options', []) if o.get('correct')]
    return len(keyed) == 1 and keyed[0].strip() == str(q.get('answer')).strip()


def main():
    items = []
    for f in sorted(glob.glob(os.path.join(ROOT, 'question-banks', 'prealgebra7', '*.json'))):
        items += json.load(open(f, encoding='utf-8'))['questions']
    checked, bad, skipped, mcbad = 0, [], {}, []
    for q in items:
        if not mc_consistent(q):
            mcbad.append(q['id'])
        if q.get('format') not in ('short-answer', 'multiple-choice'):
            continue
        try:
            ok = check(q)
        except Skip as e:
            skipped[str(e)] = skipped.get(str(e), 0) + 1
            continue
        checked += 1
        if not ok:
            bad.append((q['id'], problem_text(q)[:110], q['answer']))
    for b in bad:
        print('MISMATCH', *b)
    for i in mcbad:
        print('MC KEY', i)
    if '--list' in sys.argv:
        print('skipped:', sorted(skipped.items(), key=lambda x: -x[1])[:15])
    ok = not bad and not mcbad and checked >= MIN
    print(f"{'PASS' if ok else 'FAIL'} {checked} Grade 7 keys recomputed from the printed prompts ({len(bad)} mismatches); "
          f"{sum(1 for q in items if q.get('format') == 'multiple-choice')} multiple-choice keys match their options")
    return 0 if ok else 1


if __name__ == '__main__':
    sys.exit(main())
