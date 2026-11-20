"""Whole-site audit 2 #3 (2026-11-20), Grade 5 part: Standard items stop reusing Support
templates and Advanced items stop reusing Support or Standard templates.

Grade 5 comes from a pinned release, so this script does not edit it. It reads the Grade 5 banks of a local site build
(_site/question-banks/grade5), finds the Standard (cp1) multiple-choice and short-answer items without a diagram whose
prompt is a Support (cp2) prompt with different numbers, and the Advanced (honors) items whose prompt is a Support or
not-rewritten Standard prompt with different numbers, and writes a rewrite for every such item (CAP per skill and level) to
content-updates/2026-11-20/grade5-levels.json. Each rewrite keeps the item's id, skill, level, format and standards;
the new problem adds a step (Advanced: a multi-step problem from the TH generators). scripts/apply-grade5-levels.mjs applies the file at deploy (after checking each item's
current prompt), and verify.py recomputes every new key from its printed prompt.

Usage (repository root, after a local site build): python3 tools/site-audit-20261120/grade5_levels/build.py
"""
import glob, json, math, os, random, re
from fractions import Fraction as Fr

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..', '..'))
SITE = os.path.join(ROOT, '_site', 'question-banks', 'grade5')
OUT = os.path.join(ROOT, 'content-updates', '2026-11-20', 'grade5-levels.json')
CAP = 1000  # per skill and level; high enough that every eligible item is rewritten (was 5)
N = ['Maya', 'Leo', 'Priya', 'Diego', 'Ana', 'Owen', 'Nia', 'Raj', 'Zoe', 'Sam', 'Lena', 'Kai', 'Iris', 'Theo', 'Rosa', 'Eli']
R = lambda r, a, b: r.randint(a, b)
T = {}


def t(u, n):
    def deco(fn):
        T[f'{u}-skill-{n:02d}'] = fn
        return fn
    return deco


def fs(x):
    x = Fr(x)
    return str(x.numerator) if x.denominator == 1 else f'{x.numerator}/{x.denominator}'


def mixed(x):
    x = Fr(x)
    w, r_ = divmod(x.numerator, x.denominator)
    return str(w) if r_ == 0 else (f'{w} {r_}/{x.denominator}' if w else f'{r_}/{x.denominator}')


def dz(x, p=3):
    v = Fr(x) * 10 ** p
    v = int(v + Fr(1, 2))
    s = f'{v // 10 ** p}.{v % 10 ** p:0{p}d}'.rstrip('0').rstrip('.')
    return s


def com(n):
    return f'{n:,}'


def money(x):
    v = int(Fr(x) * 100 + Fr(1, 2))
    return f'${v // 100:,}.{v % 100:02d}'


def pf(r, dens=(2, 3, 4, 5, 6, 8, 10, 12)):
    d = r.choice(dens)
    return Fr(R(r, 1, d - 1), d)


# ---------------------------------------------------------------- Classifying Two-Dimensional Figures
U = 'classifying-two-dimensional-figures'


@t(U, 2)
def _(r, nm):
    a = R(r, 20, 80)
    b = R(r, 20, 150 - a)
    c = 180 - a - b
    kind = 'right' if 90 in (a, b, c) else 'obtuse' if max(a, b, c) > 90 else 'acute'
    return (f'A triangle has angles of {a}° and {b}°. Find the third angle, then classify the triangle by its angles: acute, right, or obtuse.', kind,
            [f'The angles of a triangle add to 180°: 180 − {a} − {b} = {c}°.', f'The largest angle is {max(a, b, c)}°, so the triangle is {kind}.'])


@t(U, 3)
def _(r, nm):
    w, l = R(r, 3, 12), R(r, 13, 25)
    return (f'A rectangle is {l} inches long. Its width is {l - w} inches shorter than its length. What is its perimeter?', f'{2 * (l + w)} inches',
            [f'Width: {l} − {l - w} = {w} inches.', f'Perimeter: 2 × ({l} + {w}) = {2 * (l + w)} inches.'])


@t(U, 4)
def _(r, nm):
    k = R(r, 2, 4)
    s = R(r, k + 2, 12)
    return (f'A square has sides of {s} cm. A rectangle that is not a square has the same perimeter and is {s + k} cm long. How wide is the rectangle?', f'{s - k} cm',
            [f'Square perimeter: 4 × {s} = {4 * s} cm.', f'Rectangle: 2 × ({s + k} + w) = {4 * s}, so {s + k} + w = {2 * s}.', f'w = {s - k} cm.'])


# ---------------------------------------------------------------- Coordinate Plane Graphing
U = 'coordinate-plane-graphing'


@t(U, 1)
def _(r, nm):
    a, b, d = R(r, 2, 9), R(r, 2, 9), R(r, 1, 9)
    c = R(r, 1, a)
    return (f'Start at the origin. Move {a} units right and {b} units up. Then move {c} unit{"s" if c > 1 else ""} left and {d} unit{"s" if d > 1 else ""} up. What ordered pair names the point?', f'({a - c}, {b + d})',
            [f'After the first moves: ({a}, {b}).', f'Then x: {a} − {c} = {a - c}; y: {b} + {d} = {b + d}.', f'The point is ({a - c}, {b + d}).'])


@t(U, 2)
def _(r, nm):
    x1, y1 = R(r, 0, 5), R(r, 0, 5)
    x2, y3 = x1 + R(r, 2, 9), y1 + R(r, 2, 9)
    return (f'A path goes from A({x1}, {y1}) to B({x2}, {y1}) and then to C({x2}, {y3}). How many units long is the whole path?', f'{x2 - x1 + y3 - y1} units',
            [f'A to B: {x2} − {x1} = {x2 - x1} units.', f'B to C: {y3} − {y1} = {y3 - y1} units.', f'Total: {x2 - x1 + y3 - y1} units.'])


@t(U, 3)
def _(r, nm):
    d1, g1 = R(r, 2, 6), R(r, 6, 20)
    d2, g2 = d1 + R(r, 2, 5), g1 + R(r, 3, 15)
    return (f'On a graph, x is the number of days and y is the number of centimeters a plant has grown. The points ({d1}, {g1}) and ({d2}, {g2}) are on the graph. How many centimeters did the plant grow from day {d1} to day {d2}?',
            f'{g2 - g1} centimeters', [f'(x, y) = (days, centimeters).', f'From day {d1} to day {d2}: {g2} − {g1} = {g2 - g1} centimeters.'])


@t(U, 4)
def _(r, nm):
    m, b = R(r, 2, 9), R(r, 1, 9)
    x = R(r, 8, 15)
    return (f'The points (0, {b}), (1, {b + m}), (2, {b + 2 * m}), (3, {b + 3 * m}) follow a pattern. If the pattern continues, what is y when x = {x}?', str(b + m * x),
            [f'y starts at {b} and grows by {m} each time x grows by 1.', f'y = {b} + {m} × {x} = {b + m * x}.'])


# ---------------------------------------------------------------- Data, Line Plots and Problem Solving
U = 'data-line-plots-problem-solving'


@t(U, 2)
def _(r, nm):
    vals = [Fr(R(r, 4, 12), 4) for _ in range(7)]
    k = r.choice(vals)
    more = sum(1 for v in vals if v > k)
    return (f'Data: {", ".join(mixed(v) for v in vals)}. On a line plot, how many X marks are to the right of {mixed(k)}?', str(more),
            [f'Values greater than {mixed(k)}: ' + (', '.join(mixed(v) for v in vals if v > k) or 'none') + '.', f'That is {more} X marks.'])


@t(U, 3)
def _(r, nm):
    vals = [Fr(R(r, 8, 24), 8) for _ in range(5)]
    tot = sum(vals)
    return (f'Data: {", ".join(mixed(v) for v in vals)}. If the total is shared equally among the {len(vals)} values, what does each get?', mixed(tot / len(vals)),
            [f'Total: {mixed(tot)}.', f'Share equally: {mixed(tot)} ÷ {len(vals)} = {mixed(tot / len(vals))}.'])


@t(U, 4)
def _(r, nm):
    n, p, c, g = R(r, 25, 40), Fr(R(r, 125, 300), 100), Fr(R(r, 800, 1500), 100), R(r, 3, 8)
    prof = n * p - c - g
    return (f'A class sells {n} muffins for {money(p)} each. They spent {money(c)} on ingredients and ${g} on bags. How much money did they make after paying for both?', money(prof),
            [f'Sales: {n} × {money(p)} = {money(n * p)}.', f'Costs: {money(c)} + ${g} = {money(c + g)}.', f'Profit: {money(n * p)} − {money(c + g)} = {money(prof)}.'])


# ---------------------------------------------------------------- Decimal Operations
U = 'decimal-operations'


@t(U, 1)
def _(r, nm):
    a, b, c = Fr(R(r, 1000, 9999), 100), Fr(R(r, 10, 99), 10), Fr(R(r, 100, 999), 100)
    return (f'Add and subtract from left to right: {dz(a, 2)} + {dz(b, 1)} − {dz(c, 2)}', dz(a + b - c, 2),
            [f'{dz(a, 2)} + {dz(b, 1)} = {dz(a + b, 2)}.', f'{dz(a + b, 2)} − {dz(c, 2)} = {dz(a + b - c, 2)}.'])


@t(U, 2)
def _(r, nm):
    k, p, s = R(r, 3, 9), Fr(R(r, 101, 499), 100), R(r, 10, 50)
    return (f'{nm} buys {k} notebooks for {money(p)} each and pays with a ${s} bill. How much change does {nm} get?' if k * p < s else
            f'{nm} buys {k} notebooks for {money(p)} each and a backpack for ${s}. What is the total cost?', money(s - k * p) if k * p < s else money(s + k * p),
            [f'Notebooks: {k} × {money(p)} = {money(k * p)}.', (f'Change: ${s} − {money(k * p)} = {money(s - k * p)}.' if k * p < s else f'Total: {money(k * p)} + ${s} = {money(s + k * p)}.')])


@t(U, 3)
def _(r, nm):
    l, w = Fr(R(r, 11, 49), 10), Fr(R(r, 2, 9), 10)
    return (f'A rectangle is {dz(l, 1)} meters long and {dz(w, 1)} meters wide. What is its area plus its length, in square meters plus meters? Find {dz(l, 1)} × {dz(w, 1)} + {dz(l, 1)}.', dz(l * w + l, 2),
            [f'{dz(l, 1)} × {dz(w, 1)} = {dz(l * w, 2)}.', f'{dz(l * w, 2)} + {dz(l, 1)} = {dz(l * w + l, 2)}.'])


@t(U, 4)
def _(r, nm):
    k, q = R(r, 3, 9), Fr(R(r, 101, 999), 100)
    extra = Fr(R(r, 1, 9), 10)
    tot = k * q
    return (f'{nm} pays {money(tot + extra)} for {k} equal tickets plus a {money(extra)} fee. How much does each ticket cost?', money(q),
            [f'Without the fee: {money(tot + extra)} − {money(extra)} = {money(tot)}.', f'Each ticket: {money(tot)} ÷ {k} = {money(q)}.'])


@t(U, 5)
def _(r, nm):
    a, b = Fr(R(r, 2, 9), 10), R(r, 3, 12)
    tot = a * b
    return (f'A ribbon is {dz(tot, 1)} meters long. How many pieces that are each {dz(a, 1)} meters long can be cut from it?', str(b),
            [f'Divide: {dz(tot, 1)} ÷ {dz(a, 1)}.', f'Multiply both by 10: {dz(tot * 10, 1)} ÷ {dz(a * 10, 1)} = {b}.'])


@t(U, 6)
def _(r, nm):
    p, k, d = Fr(R(r, 150, 999), 100), R(r, 3, 9), R(r, 1, 3)
    return (f'Each sticker sheet costs {money(p)}. {nm} buys {k} sheets and uses a ${d} coupon. What is the cost?', money(k * p - d),
            [f'{k} × {money(p)} = {money(k * p)}.', f'{money(k * p)} − ${d} = {money(k * p - d)}.'])


# ---------------------------------------------------------------- Fraction Addition and Subtraction
U = 'fraction-addition-subtraction'


@t(U, 1)
def _(r, nm):
    a, b = r.sample([2, 3, 4, 5, 6, 8, 9, 10, 12], 2)
    l = a * b // math.gcd(a, b)
    return (f'Find the least common denominator of 1/{a} and 1/{b}, then add the fractions.', fs(Fr(1, a) + Fr(1, b)),
            [f'LCD of {a} and {b}: {l}.', f'1/{a} = {l // a}/{l} and 1/{b} = {l // b}/{l}.', f'Sum: {fs(Fr(1, a) + Fr(1, b))}.'])


@t(U, 2)
def _(r, nm):
    a, b, c = pf(r), pf(r), pf(r)
    return (f'Add: {fs(a)} + {fs(b)} + {fs(c)}', mixed(a + b + c), [f'{fs(a)} + {fs(b)} = {mixed(a + b)}.', f'{mixed(a + b)} + {fs(c)} = {mixed(a + b + c)}.'])


@t(U, 3)
def _(r, nm):
    a = pf(r)
    b, c = pf(r), pf(r)
    while b + c >= a:
        a = a + 1
    return (f'Subtract: {mixed(a)} − {fs(b)} − {fs(c)}', mixed(a - b - c), [f'{mixed(a)} − {fs(b)} = {mixed(a - b)}.', f'{mixed(a - b)} − {fs(c)} = {mixed(a - b - c)}.'])


@t(U, 4)
def _(r, nm):
    a, b = R(r, 1, 4) + pf(r), R(r, 1, 4) + pf(r)
    if a < b:
        a, b = b, a
    return (f'Subtract: {mixed(a)} − {mixed(b)}', mixed(a - b), [f'Rename with a common denominator.', f'{mixed(a)} − {mixed(b)} = {mixed(a - b)}.'])


@t(U, 5)
def _(r, nm):
    a, b = pf(r, (5, 6, 7, 8, 9, 10, 12)), pf(r, (5, 6, 7, 8, 9, 10, 12))
    s = a + b
    near = min([Fr(0), Fr(1, 2), Fr(1), Fr(3, 2), Fr(2)], key=lambda x: (abs(s - x), x))
    return (f'Estimate {fs(a)} + {fs(b)}. Is the sum closest to 0, 1/2, 1, 1 1/2, or 2?', mixed(near),
            [f'{fs(a)} + {fs(b)} = {mixed(s)}.', f'{mixed(s)} is closest to {mixed(near)}.'])


@t(U, 6)
def _(r, nm):
    a, b = Fr(1, r.choice([4, 5, 6, 8])), Fr(1, r.choice([3, 4, 6, 10]))
    c = Fr(1, r.choice([5, 8, 12]))
    if a + b + c >= 1:
        c = Fr(1, 12)
    return (f'In a garden, {fs(a)} is tomatoes, {fs(b)} is peppers and {fs(c)} is beans. What fraction of the garden is left to plant?', fs(1 - a - b - c),
            [f'Planted: {fs(a)} + {fs(b)} + {fs(c)} = {fs(a + b + c)}.', f'Left: 1 − {fs(a + b + c)} = {fs(1 - a - b - c)}.'])


# ---------------------------------------------------------------- Fraction Multiplication and Division
U = 'fraction-multiplication-division'


@t(U, 1)
def _(r, nm):
    a, b = R(r, 20, 90), R(r, 3, 9)
    if a % b == 0:
        a += 1
    return (f'{a} pounds of rice are shared equally among {b} families. How many pounds does each family get? Write a mixed number.', mixed(Fr(a, b)),
            [f'{a} ÷ {b} = {a}/{b}.', f'{a}/{b} = {mixed(Fr(a, b))}.'])


@t(U, 2)
def _(r, nm):
    f, k, j = pf(r), R(r, 3, 12), R(r, 2, 5)
    return (f'Multiply: {fs(f)} × {k} × {j}', mixed(f * k * j), [f'{fs(f)} × {k} = {mixed(f * k)}.', f'{mixed(f * k)} × {j} = {mixed(f * k * j)}.'])


@t(U, 3)
def _(r, nm):
    a, b = pf(r), pf(r)
    k = R(r, 2, 4)
    return (f'Multiply: {fs(a)} × {fs(b)} × {k}', mixed(a * b * k), [f'{fs(a)} × {fs(b)} = {fs(a * b)}.', f'{fs(a * b)} × {k} = {mixed(a * b * k)}.'])


@t(U, 4)
def _(r, nm):
    a, b = Fr(1, r.choice([2, 3, 4])), Fr(1, r.choice([2, 3, 4, 6]))
    L, W = R(r, 2, 4), R(r, 1, 3)
    return (f'How many tiles that are {fs(a)} foot by {fs(b)} foot are needed to cover a rectangle that is {L} feet by {W} {"foot" if W == 1 else "feet"}?', str(int(L * W / (a * b))),
            [f'Each tile covers {fs(a)} × {fs(b)} = {fs(a * b)} square foot.', f'The rectangle covers {L * W} square feet.', f'{L * W} ÷ {fs(a * b)} = {int(L * W / (a * b))} tiles.'])


@t(U, 5)
def _(r, nm):
    f = r.choice([Fr(R(r, 1, 4), 5), Fr(R(r, 6, 9), 5), Fr(1)])
    n = R(r, 20, 90)
    rel = 'less than' if f < 1 else 'greater than' if f > 1 else 'equal to'
    return (f'Without multiplying, is {mixed(f)} × {n} greater than, less than, or equal to {n}? Then find the product.', f'{rel}; {mixed(f * n)}',
            [f'{mixed(f)} is {rel} 1, so the product is {rel} {n}.', f'{mixed(f)} × {n} = {mixed(f * n)}.'])


@t(U, 6)
def _(r, nm):
    f, k, j = pf(r), R(r, 2, 6), R(r, 2, 4)
    return (f'Divide, then multiply: {fs(f)} ÷ {k} × {j}', fs(f / k * j), [f'{fs(f)} ÷ {k} = {fs(f / k)}.', f'{fs(f / k)} × {j} = {fs(f / k * j)}.'])


@t(U, 7)
def _(r, nm):
    f, k = pf(r, (2, 3, 4, 5)), R(r, 2, 6)
    return (f'{k} kids share {fs(f)} of a cake equally. What fraction of the whole cake does each kid get?', fs(f / k),
            [f'Expression: {fs(f)} ÷ {k}.', f'{fs(f)} ÷ {k} = {fs(f)} × 1/{k} = {fs(f / k)}.'])


# ---------------------------------------------------------------- Measurement Conversions
U = 'measurement-conversions'


@t(U, 1)
def _(r, nm):
    ft, inch = R(r, 3, 9), R(r, 1, 11)
    return (f'Convert: {ft} feet {inch} {"inch" if inch == 1 else "inches"} = ? inches', f'{12 * ft + inch} inches', [f'{ft} feet = {ft} × 12 = {12 * ft} inches.', f'{12 * ft} + {inch} = {12 * ft + inch} inches.'])


@t(U, 2)
def _(r, nm):
    g, q = R(r, 2, 9), R(r, 5, 40)
    tot = 4 * g + q
    return (f'A tank holds {g} gallons and a jug holds {q} quarts. How many quarts do they hold together?', f'{tot} quarts', [f'{g} gallons = {g} × 4 = {4 * g} quarts.', f'{4 * g} + {q} = {tot} quarts.'])


@t(U, 3)
def _(r, nm):
    L = Fr(R(r, 15, 95), 10)
    ml = R(r, 200, 900)
    return (f'A bottle holds {dz(L, 1)} liters. {nm} pours out {ml} milliliters. How many milliliters are left?', f'{com(int(L * 1000) - ml)} milliliters',
            [f'{dz(L, 1)} liters = {com(int(L * 1000))} milliliters.', f'{com(int(L * 1000))} − {ml} = {com(int(L * 1000) - ml)} milliliters.'])


@t(U, 4)
def _(r, nm):
    L, c, left = R(r, 2, 6), r.choice([200, 250, 500]), None
    n = L * 1000 // c
    k = R(r, 2, n - 2)
    return (f'A pitcher holds {L} liters of water. {nm} fills {k} cups of {c} milliliters. How many more cups can be filled?', f'{n - k} cups',
            [f'{L} liters = {L * 1000} milliliters.', f'Cups in all: {L * 1000} ÷ {c} = {n}.', f'Still to fill: {n} − {k} = {n - k} cups.'])


# ---------------------------------------------------------------- Multi-Digit Multiplication and Division
U = 'multi-digit-multiplication-division'


@t(U, 1)
def _(r, nm):
    a, b, c = R(r, 100, 499), R(r, 11, 59), R(r, 100, 999)
    return (f'Multiply, then add: {a} × {b} + {c}', com(a * b + c), [f'{a} × {b} = {com(a * b)}.', f'{com(a * b)} + {c} = {com(a * b + c)}.'])


@t(U, 2)
def _(r, nm):
    a, b = R(r, 120, 480), R(r, 12, 48)
    ra = round(a, -2)
    rb = round(b, -1)
    return (f'Estimate {a} × {b} by rounding {a} to the nearest hundred and {b} to the nearest ten.', com(ra * rb),
            [f'{a} rounds to {ra}; {b} rounds to {rb}.', f'{ra} × {rb} = {com(ra * rb)}.'])


@t(U, 3)
def _(r, nm):
    q, d, rem = R(r, 100, 900), R(r, 3, 9), None
    rem = R(r, 1, d - 1)
    return (f'Fill in the blank: ___ ÷ {d} = {q} R{rem}', com(q * d + rem), [f'Dividend = quotient × divisor + remainder.', f'{q} × {d} + {rem} = {com(q * d + rem)}.'])


@t(U, 4)
def _(r, nm):
    a, b = R(r, 2, 9), R(r, 2, 9)
    p = R(r, 2, 3)
    return (f'Use the basic fact {a * b} ÷ {b} = {a}. What is {com(a * b * 10 ** p)} ÷ {b * 10}?', com(a * 10 ** (p - 1)),
            [f'{com(a * b * 10 ** p)} = {a * b} × {10 ** p:,} and {b * 10} = {b} × 10.', f'Quotient: {a} × {10 ** p:,} ÷ 10 = {com(a * 10 ** (p - 1))}.'])


@t(U, 5)
def _(r, nm):
    n, k = R(r, 300, 900), R(r, 12, 25)
    q, rem = divmod(n, k)
    if rem == 0:
        n += 1; q, rem = divmod(n, k)
    return (f'A florist has {n} roses. Each bouquet uses {k} roses. After making as many complete bouquets as possible, how many roses are left?', f'{rem} roses',
            [f'{n} ÷ {k} = {q} R{rem}.', f'{q} complete bouquets use {q * k} roses, leaving {rem}.'])


# ---------------------------------------------------------------- Numerical Expressions and Patterns
U = 'numerical-expressions-patterns'


@t(U, 1)
def _(r, nm):
    a, b, c, d = R(r, 2, 9), R(r, 2, 9), R(r, 2, 9), R(r, 2, 6)
    v = a * (b + c) - d
    return (f'Evaluate: {a} × ({b} + {c}) − {d}', str(v), [f'Parentheses: {b} + {c} = {b + c}.', f'{a} × {b + c} = {a * (b + c)}.', f'{a * (b + c)} − {d} = {v}.'])


@t(U, 2)
def _(r, nm):
    a, b, c = R(r, 2, 9), R(r, 2, 20), R(r, 2, 20)
    return (f'Write an expression for "add {b} and {c}, then multiply by {a}" and evaluate it.', str(a * (b + c)),
            [f'Expression: {a} × ({b} + {c}).', f'{a} × {b + c} = {a * (b + c)}.'])


@t(U, 3)
def _(r, nm):
    a, b = R(r, 12, 60), R(r, 2, 9)
    return (f'In {a} × {b}, {a} is replaced by {a * 10} and {b} is replaced by {b * 10}. How many times as large is the new product as the old one?', '100',
            [f'{a * 10} is 10 times {a} and {b * 10} is 10 times {b}.', f'The product is 10 × 10 = 100 times as large.'])


@t(U, 4)
def _(r, nm):
    s, d, n = R(r, 2, 20), R(r, 3, 15), R(r, 6, 12)
    terms = [s + d * i for i in range(n)]
    return (f'A pattern starts at {s}. The rule is "Add {d}." What is the sum of terms 1 and {n}?', str(terms[0] + terms[-1]),
            [f'Term {n}: {s} + {n - 1} × {d} = {terms[-1]}.', f'Sum: {s} + {terms[-1]} = {terms[0] + terms[-1]}.'])


@t(U, 5)
def _(r, nm):
    a, k, n = R(r, 2, 6), R(r, 2, 4), R(r, 4, 8)
    return (f'Pattern A: start at 0, add {a}. Pattern B: start at 0, add {a * k}. For term {n}, how much greater is the B term than the A term?', str(a * k * (n - 1) - a * (n - 1)),
            [f'Term {n} of A: {a} × {n - 1} = {a * (n - 1)}.', f'Term {n} of B: {a * k} × {n - 1} = {a * k * (n - 1)}.', f'Difference: {a * k * (n - 1) - a * (n - 1)}.'])


# ---------------------------------------------------------------- Place Value and Number Sense
U = 'place-value-number-sense'


@t(U, 1)
def _(r, nm):
    d = R(r, 2, 9)
    p1, p2 = r.choice([(1000, 1), (100, Fr(1, 10)), (10, Fr(1, 100)), (1000, Fr(1, 10))])
    return (f'In a number, a {d} is in the {"thousands" if p1 == 1000 else "hundreds" if p1 == 100 else "tens"} place and another {d} is in the {"ones" if p2 == 1 else "tenths" if p2 == Fr(1, 10) else "hundredths"} place. How many times as large is the value of the first {d} as the second?',
            com(int(p1 / p2)), [f'Values: {d} × {p1} and {d} × {fs(p2)}.', f'{p1} ÷ {fs(p2)} = {com(int(p1 / p2))}.'])


@t(U, 2)
def _(r, nm):
    a = R(r, 1000, 9999)
    p = r.choice([10, 100, 1000])
    return (f'{com(a)} ÷ {com(p)} × 10 = ?', dz(Fr(a, p) * 10, 3), [f'{com(a)} ÷ {com(p)} = {dz(Fr(a, p), 3)}.', f'× 10 = {dz(Fr(a, p) * 10, 3)}.'])


@t(U, 3)
def _(r, nm):
    w, t_, h, th = 10 * R(r, 2, 9) + R(r, 2, 9), R(r, 2, 9), R(r, 2, 9), R(r, 2, 9)
    v = w + Fr(t_, 10) + Fr(h, 100) + Fr(th, 1000)
    return (f'What number is {w // 10} tens + {w % 10} ones + {t_} tenths + {h} hundredths + {th} thousandths?', dz(v, 3),
            [f'{w // 10 * 10} + {w % 10} + {dz(Fr(t_, 10), 1)} + {dz(Fr(h, 100), 2)} + {dz(Fr(th, 1000), 3)}.', f'= {dz(v, 3)}.'])


@t(U, 4)
def _(r, nm):
    xs = sorted({Fr(R(r, 1000, 9999), 1000) for _ in range(3)})
    order = list(xs)
    r.shuffle(order)
    return (f'Order from least to greatest: {", ".join(dz(x, 3) for x in order)}', ', '.join(dz(x, 3) for x in xs),
            ['Compare digit by digit from the left.', f'Least to greatest: {", ".join(dz(x, 3) for x in xs)}.'])


@t(U, 5)
def _(r, nm):
    a, b = Fr(R(r, 1000, 9999), 1000), Fr(R(r, 1000, 9999), 1000)
    s = a + b
    rs = Fr(math.floor(s * 10 + Fr(1, 2)), 10)
    return (f'Add {dz(a, 3)} + {dz(b, 3)} and round the sum to the nearest tenth.', dz(rs, 1),
            [f'{dz(a, 3)} + {dz(b, 3)} = {dz(s, 3)}.', f'Rounded to the nearest tenth: {dz(rs, 1)}.'])


# ---------------------------------------------------------------- Volume and Three-Dimensional Figures
U = 'volume-three-dimensional-figures'


@t(U, 1)
def _(r, nm):
    a, b, h = R(r, 2, 6), R(r, 2, 6), R(r, 2, 8)
    return (f'A box is packed with unit cubes. Each layer is {a} cubes by {b} cubes, and there are {h} layers. What is the volume of the box?', f'{a * b * h} cubic units',
            [f'One layer: {a} × {b} = {a * b} cubes.', f'{h} layers: {a * b} × {h} = {a * b * h} cubic units.'])


@t(U, 2)
def _(r, nm):
    l, w, h = R(r, 2, 8), R(r, 2, 6), R(r, 2, 6)
    full = l * w * h
    inside = R(r, 1, full - 1)
    return (f'A box holds {l} × {w} × {h} unit cubes when full. {inside} cubes are already inside. How many more cubes are needed to fill it?', str(full - inside),
            [f'Full: {l} × {w} × {h} = {full} cubes.', f'More needed: {full} − {inside} = {full - inside}.'])


@t(U, 3)
def _(r, nm):
    l, w, h = R(r, 3, 12), R(r, 2, 9), R(r, 2, 9)
    return (f'The base of a rectangular prism is {l} feet by {w} feet. The height is {h} feet. What is the volume?', f'{l * w * h} cubic feet',
            [f'Base area: {l} × {w} = {l * w} square feet.', f'Volume: {l * w} × {h} = {l * w * h} cubic feet.'])


@t(U, 4)
def _(r, nm):
    a, b, c = R(r, 2, 9), R(r, 2, 9), R(r, 2, 9)
    d, e, f = R(r, 2, 9), R(r, 2, 9), R(r, 2, 9)
    return (f'Two boxes are stacked. One is {a} by {b} by {c} feet. The other is {d} by {e} by {f} feet. How much greater is the volume of the larger box?', f'{abs(a * b * c - d * e * f)} cubic feet',
            [f'First: {a * b * c} cubic feet. Second: {d * e * f} cubic feet.', f'Difference: {abs(a * b * c - d * e * f)} cubic feet.'])


@t(U, 5)
def _(r, nm):
    l, w, h = R(r, 2, 9), R(r, 2, 6), R(r, 2, 5)
    return (f'A sandbox is {l} feet long and {w} feet wide. It holds {l * w * h} cubic feet of sand. How deep is the sand?', f'{h} feet',
            [f'Base area: {l} × {w} = {l * w} square feet.', f'Depth: {l * w * h} ÷ {l * w} = {h} feet.'])


# ================================================================ Advanced (honors): two- and three-step problems
TH = {}


def h(u, n):
    def deco(fn):
        TH[f'{u}-skill-{n:02d}'] = fn
        return fn
    return deco


U = 'classifying-two-dimensional-figures'


@h(U, 1)
def _(r, nm):
    a, b, c = R(r, 2, 6), R(r, 2, 6), R(r, 2, 6)
    return (f'An art kit has {a} triangles, {b} pentagons and {c} octagons. How many sides do all the shapes have together?', str(3 * a + 5 * b + 8 * c),
            [f'Triangles: {a} × 3 = {3 * a}. Pentagons: {b} × 5 = {5 * b}. Octagons: {c} × 8 = {8 * c}.', f'Total: {3 * a + 5 * b + 8 * c} sides.'])


@h(U, 2)
def _(r, nm):
    a = R(r, 25, 65)
    return (f'In a right triangle, one acute angle measures {a}°. What is the measure of the other acute angle?', f'{90 - a}°',
            ['The right angle is 90°, so the two acute angles add to 180 − 90 = 90°.', f'Other angle: 90 − {a} = {90 - a}°.'])


@h(U, 3)
def _(r, nm):
    s = R(r, 4, 15)
    k = R(r, 1, 6)
    tot = 4 * s + 3 * k
    return (f'{nm} bends a wire into a square with sides of {s} cm. Then {nm} adds {3 * k} cm of wire and bends all of it into an equilateral triangle. How long is each side of the triangle?',
            f'{tot // 3} cm' if tot % 3 == 0 else f'{mixed(Fr(tot, 3))} cm',
            [f'Wire in the square: 4 × {s} = {4 * s} cm.', f'All the wire: {4 * s} + {3 * k} = {tot} cm.', f'Each side: {tot} ÷ 3 = {mixed(Fr(tot, 3))} cm.'])


@h(U, 4)
def _(r, nm):
    l, w = R(r, 6, 15), R(r, 2, 5)
    return (f'A rectangle is {l} m by {w} m. A square has the same perimeter. What is the side length of the square, in meters?', mixed(Fr(l + w, 2)),
            [f'Rectangle perimeter: 2 × ({l} + {w}) = {2 * (l + w)} m.', f'Square side: {2 * (l + w)} ÷ 4 = {mixed(Fr(l + w, 2))} m.'])


U = 'coordinate-plane-graphing'


@h(U, 1)
def _(r, nm):
    x, y, k = R(r, 2, 8), R(r, 2, 8), R(r, 2, 3)
    return (f'Point P is at ({x}, {y}). Point Q has an x-coordinate {k} times as large as P and the same y-coordinate. How many units apart are P and Q?', str((k - 1) * x),
            [f'Q = ({k * x}, {y}).', f'Same y, so subtract the x-coordinates: {k * x} − {x} = {(k - 1) * x} units.'])


@h(U, 2)
def _(r, nm):
    x1, y1, w, l = R(r, 1, 4), R(r, 1, 4), R(r, 2, 7), R(r, 2, 7)
    return (f'A rectangle has corners at ({x1}, {y1}), ({x1 + w}, {y1}), ({x1 + w}, {y1 + l}) and ({x1}, {y1 + l}). What is its perimeter, in units?', str(2 * (w + l)),
            [f'Width: {x1 + w} − {x1} = {w}. Height: {y1 + l} − {y1} = {l}.', f'Perimeter: 2 × ({w} + {l}) = {2 * (w + l)} units.'])


@h(U, 3)
def _(r, nm):
    m, d1, d2 = R(r, 3, 9), R(r, 2, 5), R(r, 6, 10)
    return (f'A graph of saved dollars (y) after weeks (x) passes through (0, 0), ({d1}, {m * d1}) and ({d2}, {m * d2}). At the same rate, how many dollars are saved after {d2 + 3} weeks?', str(m * (d2 + 3)),
            [f'Rate: {m * d1} ÷ {d1} = {m} dollars per week.', f'After {d2 + 3} weeks: {m} × {d2 + 3} = {m * (d2 + 3)} dollars.'])


@h(U, 4)
def _(r, nm):
    m, b, x = R(r, 2, 6), R(r, 1, 9), R(r, 6, 15)
    y = b + m * x
    return (f'Points (0, {b}), (1, {b + m}), (2, {b + 2 * m}), … follow a pattern. For which x is y = {y}?', str(x),
            [f'y starts at {b} and grows by {m} for each 1 added to x.', f'{y} − {b} = {y - b}, and {y - b} ÷ {m} = {x}.'])


U = 'data-line-plots-problem-solving'


@h(U, 2)
def _(r, nm):
    vals = [Fr(R(r, 8, 24), 8) for _ in range(6)]
    big = [v for v in vals if v >= 2]
    if not big:
        vals[0] = Fr(9, 4); big = [v for v in vals if v >= 2]
    return (f'Ribbon lengths in feet: {", ".join(mixed(v) for v in vals)}. What is the total length of the pieces that are at least 2 feet long?', mixed(sum(big)),
            [f'Pieces at least 2 feet: {", ".join(mixed(v) for v in big)}.', f'Total: {mixed(sum(big))} feet.'])


@h(U, 3)
def _(r, nm):
    vals = [Fr(R(r, 4, 16), 4) for _ in range(4)]
    tot = sum(vals)
    return (f'Four beakers hold {", ".join(mixed(v) for v in vals)} liters. All the water is poured together and shared equally among the 4 beakers. How many liters are in each?', mixed(tot / 4),
            [f'Total: {mixed(tot)} liters.', f'Each: {mixed(tot)} ÷ 4 = {mixed(tot / 4)} liters.'])


@h(U, 4)
def _(r, nm):
    n, p, c = R(r, 20, 40), Fr(R(r, 150, 300), 100), Fr(R(r, 1000, 2500), 100)
    prof = n * p - c
    goal = int(prof) + R(r, 10, 40)
    k = math.ceil((goal - prof) / p)
    return (f'A class sold {n} muffins at {money(p)} each and spent {money(c)} on ingredients. They want a profit of at least ${goal}. How many more muffins must they sell at the same price?', str(k),
            [f'Profit so far: {n} × {money(p)} − {money(c)} = {money(prof)}.', f'Still needed: ${goal} − {money(prof)} = {money(goal - prof)}.', f'{money(goal - prof)} ÷ {money(p)} ≈ {dz((goal - prof) / p, 2)}, so {k} more muffins.'])


U = 'decimal-operations'


@h(U, 1)
def _(r, nm):
    a, b, c = Fr(R(r, 2000, 4000), 100), Fr(R(r, 100, 999), 100), Fr(R(r, 500, 1900), 100)
    return (f'{nm} had {money(a)}, earned {money(b)} and then spent {money(c)}. How much money is left?', money(a + b - c),
            [f'{money(a)} + {money(b)} = {money(a + b)}.', f'{money(a + b)} − {money(c)} = {money(a + b - c)}.'])


@h(U, 2)
def _(r, nm):
    w, p = Fr(R(r, 15, 45), 10), Fr(R(r, 199, 699), 100)
    return (f'Apples cost {money(p)} per pound. {nm} buys {dz(w, 1)} pounds. What is the cost to the nearest cent?', money(w * p),
            [f'{dz(w, 1)} × {money(p)} = ${dz(w * p, 3)}.', f'To the nearest cent: {money(w * p)}.'])


@h(U, 3)
def _(r, nm):
    l, w, d = Fr(R(r, 11, 49), 10), Fr(R(r, 11, 39), 10), Fr(R(r, 2, 9), 10)
    return (f'A garden bed is {dz(l, 1)} m long and {dz(w, 1)} m wide. It is covered with soil {dz(d, 1)} m deep. How many cubic meters of soil is that?', dz(l * w * d, 3),
            [f'Area: {dz(l, 1)} × {dz(w, 1)} = {dz(l * w, 2)} square meters.', f'Volume: {dz(l * w, 2)} × {dz(d, 1)} = {dz(l * w * d, 3)} cubic meters.'])


@h(U, 4)
def _(r, nm):
    k, each, tip = R(r, 3, 8), Fr(R(r, 305, 999), 100), Fr(R(r, 50, 300), 100)
    return (f'{k} friends split a {money(k * each)} bill equally. {nm} also leaves a {money(tip)} tip. How much does {nm} pay in all?', money(each + tip),
            [f'Share: {money(k * each)} ÷ {k} = {money(each)}.', f'With the tip: {money(each)} + {money(tip)} = {money(each + tip)}.'])


@h(U, 5)
def _(r, nm):
    piece, k = Fr(R(r, 2, 9), 10), R(r, 6, 15)
    left = Fr(R(r, 1, int(piece * 10) - 1), 10) if piece > Fr(1, 10) else Fr(0)
    tot = piece * k + left
    return (f'A {dz(tot, 1)}-meter rope is cut into as many {dz(piece, 1)}-meter pieces as possible. How many meters are left over?', dz(left, 1) if left else '0',
            [f'{dz(tot, 1)} ÷ {dz(piece, 1)} = {k} pieces with some left over.', f'{k} pieces use {k} × {dz(piece, 1)} = {dz(piece * k, 1)} meters.', f'Left: {dz(tot, 1)} − {dz(piece * k, 1)} = {dz(left, 1) if left else "0"} meters.'])


@h(U, 6)
def _(r, nm):
    a, pa = R(r, 2, 6), Fr(R(r, 150, 600), 100)
    b = a * R(r, 2, 4)
    pb = pa * b / a - Fr(R(r, 5, 60), 100)
    ua, ub = pa / a, pb / b
    return (f'Pack A has {a} bars for {money(pa)}. Pack B has {b} bars for {money(pb)}. How many cents per bar do you save with the cheaper pack? Round to the nearest tenth of a cent.',
            dz(Fr(math.floor(abs(ua - ub) * 1000 + Fr(1, 2)), 10), 1),
            [f'A: {money(pa)} ÷ {a} ≈ ${dz(ua, 4)} per bar. B: {money(pb)} ÷ {b} ≈ ${dz(ub, 4)} per bar.', f'Difference ≈ {dz(abs(ua - ub) * 100, 3)} cents ≈ {dz(Fr(math.floor(abs(ua - ub) * 1000 + Fr(1, 2)), 10), 1)} cents.'])


U = 'fraction-addition-subtraction'


@h(U, 1)
def _(r, nm):
    a, b = r.sample([3, 4, 5, 6, 8, 9, 10, 12], 2)
    na = r.choice([x for x in range(1, a) if math.gcd(x, a) == 1])
    nb = r.choice([x for x in range(1, b) if math.gcd(x, b) == 1])
    l = a * b // math.gcd(a, b)
    return (f'Rewrite {na}/{a} and {nb}/{b} with their least common denominator. What is the sum of the two new numerators?', str(na * l // a + nb * l // b),
            [f'LCD of {a} and {b}: {l}.', f'{na}/{a} = {na * l // a}/{l} and {nb}/{b} = {nb * l // b}/{l}.', f'{na * l // a} + {nb * l // b} = {na * l // a + nb * l // b}.'])


@h(U, 2)
def _(r, nm):
    a, b = pf(r), pf(r)
    k = R(r, 1, 3)
    return (f'{nm} walked {fs(a)} mile to school, {fs(b)} mile to the library and {k} mile{"s" if k > 1 else ""} home. How far did {nm} walk in all?', f'{mixed(a + b + k)} miles',
            [f'{fs(a)} + {fs(b)} = {mixed(a + b)}.', f'{mixed(a + b)} + {k} = {mixed(a + b + k)} miles.'])


@h(U, 3)
def _(r, nm):
    a, b, c = pf(r), pf(r), pf(r)
    if a < b:
        a, b = b, a
    if a == b:
        b = b / 2
    return (f'A jar was {fs(a)} full of rice. {nm} used {fs(b)} of a jar and then added {fs(c)} of a jar. How full is the jar now?', mixed(a - b + c),
            [f'After using: {fs(a)} − {fs(b)} = {fs(a - b)}.', f'After adding: {fs(a - b)} + {fs(c)} = {mixed(a - b + c)}.'])


@h(U, 4)
def _(r, nm):
    a, b, c = R(r, 1, 4) + pf(r), R(r, 1, 4) + pf(r), R(r, 1, 3) + pf(r)
    if a + b <= c:
        a += 3
    return (f'A board is {mixed(a)} ft long. {nm} adds a {mixed(b)} ft board, then cuts off {mixed(c)} ft. How long is the board now?', f'{mixed(a + b - c)} ft',
            [f'{mixed(a)} + {mixed(b)} = {mixed(a + b)} ft.', f'{mixed(a + b)} − {mixed(c)} = {mixed(a + b - c)} ft.'])


@h(U, 5)
def _(r, nm):
    a, b, c = pf(r, (6, 8, 10, 12)), pf(r, (6, 8, 10, 12)), pf(r, (6, 8, 10, 12))
    s = a + b + c
    near = min([Fr(k, 2) for k in range(0, 7)], key=lambda x: (abs(s - x), x))
    return (f'Estimate {fs(a)} + {fs(b)} + {fs(c)} to the nearest half (0, 1/2, 1, 1 1/2, 2, 2 1/2 or 3).', mixed(near),
            [f'Exact sum: {mixed(s)}.', f'The nearest half is {mixed(near)}.'])


@h(U, 6)
def _(r, nm):
    a, b = Fr(1, r.choice([3, 4, 5, 6])), Fr(r.choice([1, 2]), r.choice([5, 8, 9]))
    if a + b >= 1:
        b = Fr(1, 8)
    rest = 1 - a - b
    return (f'{nm} read {fs(a)} of a book on Monday and {fs(b)} of it on Tuesday. On Wednesday {nm} read half of what was left. What fraction of the book is still unread?', fs(rest / 2),
            [f'Read Monday and Tuesday: {fs(a)} + {fs(b)} = {fs(a + b)}.', f'Left: 1 − {fs(a + b)} = {fs(rest)}.', f'Half of that is read, so {fs(rest / 2)} is still unread.'])


U = 'fraction-multiplication-division'


@h(U, 1)
def _(r, nm):
    a, b = R(r, 25, 95), R(r, 3, 8)
    if a % b == 0:
        a += 1
    t = Fr(R(r, 1, 3), 2)
    return (f'{a} cups of soup are poured equally into {b} pots. Then {mixed(t)} {"cup is" if t == 1 else "cups are"} taken out of each pot. How many cups are left in each pot? Write a mixed number.', mixed(Fr(a, b) - t),
            [f'Each pot gets {a} ÷ {b} = {mixed(Fr(a, b))} cups.', f'{mixed(Fr(a, b))} − {mixed(t)} = {mixed(Fr(a, b) - t)} cups.'])


@h(U, 2)
def _(r, nm):
    f, n = pf(r, (3, 4, 5, 6, 8)), R(r, 12, 40)
    return (f'A class has {n} students. {fs(f)} of them walk to school. How many students do not walk? (Round down to a whole student if needed.)', str(n - math.floor(f * n)),
            [f'Walk: {fs(f)} × {n} = {mixed(f * n)}, so {math.floor(f * n)} students.', f'Do not walk: {n} − {math.floor(f * n)} = {n - math.floor(f * n)}.'])


@h(U, 3)
def _(r, nm):
    a, b = pf(r), pf(r)
    w = R(r, 2, 6)
    return (f'A rectangle is {fs(a)} m by {fs(b)} m. {nm} makes {w} of them. What is their total area, in square meters?', mixed(a * b * w),
            [f'One rectangle: {fs(a)} × {fs(b)} = {fs(a * b)} square meter.', f'{w} rectangles: {w} × {fs(a * b)} = {mixed(a * b * w)} square meters.'])


@h(U, 4)
def _(r, nm):
    l1, w1 = R(r, 2, 4) + pf(r, (2, 4)), R(r, 2, 4) + pf(r, (2, 4))
    l2, w2 = R(r, 2, 4) + pf(r, (2, 4)), R(r, 2, 4) + pf(r, (2, 4))
    a1, a2 = l1 * w1, l2 * w2
    return (f'Garden A is {mixed(l1)} m by {mixed(w1)} m. Garden B is {mixed(l2)} m by {mixed(w2)} m. How many more square meters is the larger garden?', mixed(abs(a1 - a2)),
            [f'A: {mixed(l1)} × {mixed(w1)} = {mixed(a1)} square meters.', f'B: {mixed(l2)} × {mixed(w2)} = {mixed(a2)} square meters.', f'Difference: {mixed(abs(a1 - a2))}.'])


@h(U, 5)
def _(r, nm):
    f, g, n = Fr(R(r, 1, 4), 5), Fr(R(r, 6, 9), 5), R(r, 20, 60)
    return (f'Without multiplying, {mixed(g)} × {n} is greater than {mixed(f)} × {n} because {mixed(g)} is greater than 1 and {mixed(f)} is less than 1. How much greater is it?', mixed((g - f) * n),
            [f'{mixed(f)} < 1 < {mixed(g)}, so {mixed(g)} × {n} is greater.', f'Difference: ({mixed(g)} − {mixed(f)}) × {n} = {mixed((g - f) * n)}.'])


@h(U, 6)
def _(r, nm):
    f, k = pf(r, (2, 3, 4, 5)), R(r, 2, 6)
    return (f'{fs(f)} of a pan of brownies is shared equally by {k} friends. If every friend always gets that same amount, how many friends could share a whole pan?',
            mixed(k / f), [f'Each friend: {fs(f)} ÷ {k} = {fs(f / k)}.', f'Whole pan: 1 ÷ {fs(f / k)} = {mixed(k / f)} friends.'])


@h(U, 7)
def _(r, nm):
    L, d = R(r, 3, 10), r.choice([2, 3, 4, 6, 8])
    used = R(r, 1, L * d - 1)
    return (f'A {L}-foot board is cut into pieces that are 1/{d} foot long. {nm} uses {used} pieces. How many feet of pieces are left?', f'{mixed(Fr(L * d - used, d))} ft',
            [f'Pieces in all: {L} ÷ 1/{d} = {L * d}.', f'Left: {L * d} − {used} = {L * d - used} pieces.', f'{L * d - used} × 1/{d} = {mixed(Fr(L * d - used, d))} ft.'])


U = 'measurement-conversions'


@h(U, 1)
def _(r, nm):
    ft, inch = R(r, 3, 9), R(r, 1, 11)
    cut = R(r, 5, 30)
    tot = 12 * ft + inch - cut
    if tot % 12 == 0:
        cut += 1; tot -= 1
    return (f'A rope is {ft} ft {inch} in. long. {nm} cuts off {cut} inches. How long is the rope now, in feet and inches?', f'{tot // 12} ft {tot % 12} in.',
            [f'{ft} ft {inch} in. = {12 * ft + inch} inches.', f'{12 * ft + inch} − {cut} = {tot} inches.', f'{tot} inches = {tot // 12} ft {tot % 12} in.'])


@h(U, 2)
def _(r, nm):
    n, oz = R(r, 3, 9), R(r, 5, 14)
    tot = n * oz
    return (f'{nm} packs {n} cans that weigh {oz} ounces each. What is the total weight in pounds and ounces?', f'{tot // 16} lb {tot % 16} oz',
            [f'{n} × {oz} = {tot} ounces.', f'16 ounces = 1 pound: {tot} = {tot // 16} × 16 + {tot % 16}, so {tot // 16} lb {tot % 16} oz.'])


@h(U, 3)
def _(r, nm):
    kg, g, n = R(r, 2, 9), R(r, 100, 900), R(r, 3, 8)
    tot = kg * 1000 + g
    return (f'A bag holds {kg} kg {g} g of flour. It is split equally into {n} containers. How many grams go in each? Round to the nearest gram.', f'{round(tot / n):,} g',
            [f'{kg} kg {g} g = {tot:,} g.', f'{tot:,} ÷ {n} ≈ {tot / n:.2f}, which rounds to {round(tot / n):,} g.'])


@h(U, 4)
def _(r, nm):
    L, c, k = R(r, 2, 8), r.choice([150, 200, 250, 400]), R(r, 2, 6)
    tot = L * 1000 * k
    return (f'{k} pitchers each hold {L} liters. How many full {c}-milliliter cups can be filled from all of them?', f'{tot // c} cups',
            [f'{k} × {L} liters = {k * L} liters = {tot:,} milliliters.', f'{tot:,} ÷ {c} = {tot // c} full cups.'])


U = 'multi-digit-multiplication-division'


@h(U, 1)
def _(r, nm):
    a, b, c = R(r, 120, 480), R(r, 12, 48), R(r, 12, 48)
    return (f'A theater has {a} seats in each section. Section A is sold out on {b} nights and section B on {c} nights. How many tickets were sold in all?', com(a * (b + c)),
            [f'{a} × {b} = {com(a * b)} and {a} × {c} = {com(a * c)}.', f'Total: {com(a * b)} + {com(a * c)} = {com(a * (b + c))}.'])


@h(U, 2)
def _(r, nm):
    a, b = R(r, 212, 489), R(r, 21, 49)
    ra, rb = round(a, -2), round(b, -1)
    return (f'Estimate {a} × {b} by rounding each factor to its greatest place value, then find the exact product. How much greater or less is the estimate? Give the size of the difference.', com(abs(ra * rb - a * b)),
            [f'Estimate: {ra} × {rb} = {com(ra * rb)}.', f'Exact: {a} × {b} = {com(a * b)}.', f'Difference: {com(abs(ra * rb - a * b))}.'])


@h(U, 3)
def _(r, nm):
    d, q, rem = R(r, 4, 9), R(r, 150, 900), None
    rem = R(r, 1, d - 1)
    n = q * d + rem
    return (f'{n:,} stickers are put into packs of {d}. How many full packs are there, and how many stickers are left over? Give the number of full packs.', com(q),
            [f'{n:,} ÷ {d} = {q} R{rem}.', f'{q} full packs, {rem} left over.'])


@h(U, 4)
def _(r, nm):
    d, q = R(r, 21, 48), R(r, 25, 95)
    extra = R(r, 1, d - 1)
    n = d * q + extra
    return (f'{n:,} students ride buses that each hold {d} students. How many buses are needed so that everyone rides?', str(q + 1),
            [f'{n:,} ÷ {d} = {q} R{extra}.', f'The {extra} extra students need one more bus: {q + 1} buses.'])


@h(U, 5)
def _(r, nm):
    yd, k = R(r, 10, 40), R(r, 3, 9)
    if yd % k == 0:
        yd += 1
    return (f'{yd} yards of ribbon are shared equally by {k} friends. How many feet does each friend get? Write a mixed number.', f'{mixed(Fr(3 * yd, k))} feet',
            [f'Each gets {yd} ÷ {k} = {mixed(Fr(yd, k))} yards.', f'1 yard = 3 feet: {mixed(Fr(yd, k))} × 3 = {mixed(Fr(3 * yd, k))} feet.'])


U = 'numerical-expressions-patterns'


@h(U, 1)
def _(r, nm):
    a, b, c, e = R(r, 2, 6), R(r, 2, 9), R(r, 2, 9), R(r, 2, 9)
    d = R(r, 1, c - 1)
    v = a * (b + (c - d)) + e
    return (f'Evaluate: {a} × [{b} + ({c} − {d})] + {e}', str(v), [f'Parentheses: {c} − {d} = {c - d}.', f'Brackets: {b} + {c - d} = {b + c - d}.', f'{a} × {b + c - d} + {e} = {v}.'])


@h(U, 2)
def _(r, nm):
    a, b, k = R(r, 20, 60), R(r, 2, 18), r.choice([2, 3, 4])
    if (a - b) % k:
        a += k - (a - b) % k
    word = {2: 'half', 3: 'one third', 4: 'one fourth'}[k]
    return (f'Write an expression for "{word} of the difference of {a} and {b}" and evaluate it.', str((a - b) // k),
            [f'Expression: ({a} − {b}) ÷ {k}.', f'{a - b} ÷ {k} = {(a - b) // k}.'])


@h(U, 3)
def _(r, nm):
    a, b, k = R(r, 100, 999), R(r, 100, 999), R(r, 3, 9)
    return (f'{a} + {b} = {com(a + b)}. Use this, without adding again, to find {k} × ({a} + {b}).', com(k * (a + b)),
            [f'{k} × (the sum) is {k} times as large as the sum.', f'{k} × {a + b} = {com(k * (a + b))}.'])


@h(U, 4)
def _(r, nm):
    s, m, n = R(r, 1, 6), r.choice([2, 3]), R(r, 5, 8)
    terms = [s * m ** i for i in range(n)]
    return (f'A pattern starts at {s}. The rule is "Multiply by {m}." What is the sum of the first {n} terms?', com(sum(terms)),
            [f'Terms: {", ".join(map(str, terms))}.', f'Sum: {com(sum(terms))}.'])


@h(U, 5)
def _(r, nm):
    a, k, n = R(r, 2, 6), R(r, 2, 4), R(r, 4, 9)
    return (f'Pattern A: start at 0, add {a}. Pattern B: start at 0, add {a * k}. When the A term is {a * (n - 1)}, what is the B term?', str(a * k * (n - 1)),
            [f'Each B term is {k} times the matching A term.', f'B term: {k} × {a * (n - 1)} = {a * k * (n - 1)}.'])


U = 'place-value-number-sense'


@h(U, 1)
def _(r, nm):
    d = R(r, 2, 9)
    i, j = r.sample(range(0, 6), 2)
    names = ['thousands', 'hundreds', 'tens', 'ones', 'tenths', 'hundredths']
    vals = [Fr(1000), Fr(100), Fr(10), Fr(1), Fr(1, 10), Fr(1, 100)]
    hi, lo = (i, j) if vals[i] > vals[j] else (j, i)
    return (f'One number has a {d} in the {names[hi]} place. Another has a {d} in the {names[lo]} place. How many times as large is the value of the first {d}?', com(int(vals[hi] / vals[lo])),
            [f'Values: {d} × {fs(vals[hi])} and {d} × {fs(vals[lo])}.', f'{fs(vals[hi])} ÷ {fs(vals[lo])} = {com(int(vals[hi] / vals[lo]))}.'])


@h(U, 2)
def _(r, nm):
    a = Fr(R(r, 1000, 9999), 100)
    p, q = r.choice([(100, 10), (1000, 10), (1000, 100)])
    return (f'{dz(a, 2)} × {com(p)} ÷ {q} = ?', dz(a * p / q, 3), [f'{dz(a, 2)} × {com(p)} = {dz(a * p, 2)}.', f'÷ {q} = {dz(a * p / q, 3)}.'])


@h(U, 3)
def _(r, nm):
    v = Fr(R(r, 100000, 999999), 1000)
    digits = f'{int(v * 1000):06d}'
    return (f'In {dz(v, 3)}, how much greater is the value of the hundreds digit than the value of the tenths digit?', dz(int(digits[0]) * 100 - Fr(int(digits[3]), 10), 1),
            [f'Hundreds digit {digits[0]}: value {int(digits[0]) * 100}. Tenths digit {digits[3]}: value {dz(Fr(int(digits[3]), 10), 1)}.', f'{int(digits[0]) * 100} − {dz(Fr(int(digits[3]), 10), 1)} = {dz(int(digits[0]) * 100 - Fr(int(digits[3]), 10), 1)}.'])


@h(U, 4)
def _(r, nm):
    xs = sorted({Fr(R(r, 1000, 9999), 1000) for _ in range(4)})
    return (f'Four runners finished in {", ".join(dz(x, 3) for x in sorted(xs, key=lambda x: (x * 7) % 1))} minutes. What is the difference between the fastest and slowest times?', dz(xs[-1] - xs[0], 3),
            [f'Fastest (least): {dz(xs[0], 3)}. Slowest (greatest): {dz(xs[-1], 3)}.', f'{dz(xs[-1], 3)} − {dz(xs[0], 3)} = {dz(xs[-1] - xs[0], 3)}.'])


@h(U, 5)
def _(r, nm):
    a, b = Fr(R(r, 1000, 9999), 100), Fr(R(r, 1000, 9999), 100)
    ra, rb = round(a), round(b)
    return (f'Round {dz(a, 2)} and {dz(b, 2)} to the nearest whole number, then add. How far is that estimate from the exact sum? Give the difference to the nearest hundredth.', dz(abs(ra + rb - a - b), 2),
            [f'Rounded: {ra} + {rb} = {ra + rb}. Exact: {dz(a + b, 2)}.', f'Difference: {dz(abs(ra + rb - a - b), 2)}.'])


U = 'volume-three-dimensional-figures'


@h(U, 1)
def _(r, nm):
    a, b, h_, k = R(r, 2, 6), R(r, 2, 6), R(r, 2, 6), R(r, 2, 4)
    return (f'A box is {a} cubes long, {b} cubes wide and {h_} cubes tall. A second box has {k} times as many layers. How many unit cubes fill both boxes?', str(a * b * h_ * (1 + k)),
            [f'First box: {a} × {b} × {h_} = {a * b * h_}.', f'Second box: {a * b * h_} × {k} = {a * b * h_ * k}.', f'Both: {a * b * h_ * (1 + k)} cubes.'])


@h(U, 2)
def _(r, nm):
    l, w, h_ = R(r, 4, 12), R(r, 3, 10), R(r, 3, 8)
    full = l * w * h_
    layers = R(r, 1, h_ - 1)
    return (f'A box holds {l} × {w} × {h_} unit cubes when full. {layers} full layers are already packed. How many more cubes are needed to fill it?', str(full - l * w * layers),
            [f'One layer: {l} × {w} = {l * w}. Packed: {l * w} × {layers} = {l * w * layers}.', f'Full: {full}. More needed: {full - l * w * layers}.'])


@h(U, 3)
def _(r, nm):
    l, w, h_ = R(r, 3, 15), R(r, 2, 9), R(r, 2, 9)
    return (f'A rectangular prism has a volume of {l * w * h_} cubic inches. Its length is {l} inches and its height is {h_} inches. What is its width?', f'{w} inches',
            [f'V = l × w × h: {l * w * h_} = {l} × w × {h_}.', f'{l} × {h_} = {l * h_}, so w = {l * w * h_} ÷ {l * h_} = {w} inches.'])


@h(U, 4)
def _(r, nm):
    a, b, c, d, e, f = (R(r, 2, 9) for _ in range(6))
    k = R(r, 2, 3)
    return (f'A shelf unit is {k} boxes that are {a} by {b} by {c} cm and one box that is {d} by {e} by {f} cm. What is its total volume?', f'{k * a * b * c + d * e * f} cubic centimeters',
            [f'Small boxes: {k} × {a * b * c} = {k * a * b * c}.', f'Big box: {d * e * f}.', f'Total: {k * a * b * c + d * e * f} cubic centimeters.'])


@h(U, 5)
def _(r, nm):
    l, w, h_ = R(r, 8, 20), R(r, 6, 12), R(r, 6, 14)
    fill = R(r, 2, h_ - 2)
    return (f'A fish tank is {l} in. long, {w} in. wide and {h_} in. tall. It is filled to {fill} in. below the top. How many cubic inches of water are in it?', f'{l * w * (h_ - fill)} cubic inches',
            [f'Water depth: {h_} − {fill} = {h_ - fill} in.', f'Volume: {l} × {w} × {h_ - fill} = {l * w * (h_ - fill)} cubic inches.'])


SIG = lambda q: re.sub(r'\d+(?:\.\d+)?', '#', str(q['prompt'])).strip()
NUM = re.compile(r'-?\d[\d,]*(?:\.\d+)?(?: \d+/\d+)?(?:/\d+)?')


SING = {'feet': 'foot', 'inches': 'inch', 'cups': 'cup', 'pounds': 'pound', 'miles': 'mile', 'liters': 'liter', 'meters': 'meter', 'yards': 'yard', 'ounces': 'ounce', 'grams': 'gram', 'hours': 'hour', 'minutes': 'minute', 'milliliters': 'milliliter', 'kilograms': 'kilogram', 'centimeters': 'centimeter', 'gallons': 'gallon', 'quarts': 'quart', 'pints': 'pint'}


def options(ans, steps, rng):
    """The key plus three wrong options of the same form, preferring numbers from the solution."""
    if ans in ('acute', 'right', 'obtuse'):
        return ['acute', 'right', 'obtuse', 'straight']
    m = re.fullmatch(r'(\$?)(\d+ \d+/\d+|\d+/\d+|\(\d+, \d+\)|[\d,]+(?:\.\d+)?)(.*)', ans)
    if not m:
        return None
    pre, num, post = m.groups()
    if num.startswith('('):
        x, y = map(int, num[1:-1].split(', '))
        return [ans] + [f'({a}, {b})' for a, b in ((y, x), (x + 1, y), (x, y + 1))]
    val = lambda s: Fr(s.replace(',', '').split(' ')[0]) + (Fr(s.split(' ')[1]) if ' ' in s else 0)
    a = val(num)
    fmt = lambda v: pre + (mixed(v) if '/' in num else (f'{v.numerator // v.denominator:,}.{(v * 100).numerator // (v * 100).denominator % 100:02d}' if pre == '$' else (com(int(v)) if ',' in num else (dz(v, 3) if '.' in num else str(v))))) + post
    pool = []
    for s in steps:
        for x in NUM.findall(s):
            try:
                v = val(x)
            except Exception:
                continue
            if v > 0 and v != a and v not in pool:
                pool.append(v)
    out = [ans]
    for v in pool[::-1] + [a + 1, a + 2, a * 2, a + 10]:
        o = fmt(v)
        if v == 1 and post.split(' ')[-1] in SING:
            o = o[:len(o) - len(post.split(' ')[-1])] + SING[post.split(' ')[-1]]
        if o not in out and len(out) < 4 and v > 0:
            out.append(o)
    return out


def main():
    items = {}
    for f in sorted(glob.glob(os.path.join(SITE, '*.json'))):
        for q in json.load(open(f, encoding='utf-8'))['questions']:
            items[q['id']] = q
    # A site already built with these rewrites: read each rewritten item as it was before (prompt and answer).
    if os.path.exists(OUT):
        for qid, e in json.load(open(OUT, encoding='utf-8'))['items'].items():
            if qid in items and items[qid]['prompt'] == e['to']['prompt']:
                items[qid] = dict(items[qid], prompt=e['from']['prompt'], answer=e['from']['answer'], solutionSteps=[], sourceNotes=items[qid].get('sourceNotes', '').split(' Rewritten at deploy')[0])
    cp2 = {}
    for q in items.values():
        if q['level'] == 'cp2':
            cp2.setdefault(q['skillId'], set()).add(SIG(q))
    out, made = {}, {'cp1': 0, 'honors': 0}
    for sid in sorted({q['skillId'] for q in items.values()}):
        sk = [q for q in items.values() if q['skillId'] == sid]
        ok = lambda q, lv: q['level'] == lv and q['format'] in ('multiple-choice', 'short-answer') and not q.get('diagram')
        c1 = sorted((q for q in sk if T.get(sid) and ok(q, 'cp1') and SIG(q) in cp2.get(sid, set())), key=lambda q: q['id'])[:CAP]
        ids1 = {q['id'] for q in c1}
        lowh = cp2.get(sid, set()) | {SIG(q) for q in sk if q['level'] == 'cp1' and q['id'] not in ids1}
        ch = sorted((q for q in sk if TH.get(sid) and ok(q, 'honors') and SIG(q) in lowh), key=lambda q: q['id'])[:CAP]
        chosen = ids1 | {q['id'] for q in ch}
        used = {q['prompt'] for q in items.values() if q['id'] not in chosen}
        for lv, cand, fn in (('cp1', c1, T.get(sid)), ('honors', ch, TH.get(sid))):
            for i, q in enumerate(cand):
                rng = random.Random(f'g5-levels-{lv}-' + q['id'])
                for _ in range(80):
                    prompt, ans, steps = fn(rng, N[sum(map(ord, q['id'])) % len(N)])
                    if prompt not in used:
                        break
                else:
                    continue
                new = dict(prompt=prompt, answer=ans, solutionSteps=steps)
                if q['format'] == 'multiple-choice':
                    opts = options(ans, steps, rng)
                    if not opts or len(set(opts)) != 4:
                        continue
                    rng.shuffle(opts)
                    new['options'] = [{'text': o, 'correct': o == ans} for o in opts]
                used.add(prompt)
                what = 'a Standard item that reused a Support template now adds a step' if lv == 'cp1' else 'an Advanced item that reused an easier template is now a multi-step problem'
                new['sourceNotes'] = (q.get('sourceNotes', '') + f' Rewritten at deploy: whole-site audit 2 #3 (2026-11-20), {what}; '
                                      'key recomputed by tools/site-audit-20261120/grade5_levels/verify.py.').strip()
                out[q['id']] = {'from': {'prompt': q['prompt'], 'answer': q['answer']}, 'to': new}
                made[lv] += 1
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    json.dump({'about': 'Grade 5 Standard items rewritten at deploy (whole-site audit 2 #3). Applied by scripts/apply-grade5-levels.mjs.', 'items': out},
              open(OUT, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    print(f'Grade 5 levels: {made["cp1"]} Standard and {made["honors"]} Advanced rewrites')


if __name__ == '__main__':
    main()
