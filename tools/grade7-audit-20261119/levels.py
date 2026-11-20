"""Grade 7 levels, whole-site audit 2 #3 (2026-11-20): Standard and Advanced items stop reusing lower-level templates.
(Adapted from tools/grade6-audit-20261119/levels.py.)

In each skill, up to CAP Standard (cp1) items whose prompt is a CP2 prompt with different numbers are rewritten in place
as a Standard item with an added step (one generator per skill, below). Up to CAP Advanced (honors) items that reuse a
CP2 or CP1 template are rewritten in place from that skill's Advanced multi-step generator (honors.py).
Only text items are rewritten: multiple choice and short answer without a diagram. An item keeps its id, skill, level,
format and standards; a multiple-choice item gets distractors from the solution's intermediate values.
Keys are recomputed from the printed prompts by verify_levels.py. Idempotent: rerunning changes nothing."""
import math, os, random, re, sys
from fractions import Fraction as Fr
sys.path.insert(0, os.path.dirname(__file__))
import lib
import honors as H

CAP = 5
N = H.N
R = lambda r, a, b: r.randint(a, b)
T = {}


def t(u, n):
    def deco(fn):
        T[(u, n)] = fn
        return fn
    return deco


def fs(x):
    x = Fr(x)
    return str(x.numerator) if x.denominator == 1 else f'{x.numerator}/{x.denominator}'


def dz(x, p=2):
    v = Fr(x) * 10 ** p
    v = int(v + Fr(1, 2)) if v >= 0 else -int(-v + Fr(1, 2))
    return f'{v / 10 ** p:.{p}f}'.rstrip('0').rstrip('.')


def pf(r):
    d = R(r, 2, 9)
    return Fr(R(r, 1, d - 1), d)


def money(x):
    v = Fr(x) * 100
    v = int(v + Fr(1, 2))
    return f'${v // 100:,}.{v % 100:02d}'


# ---------------------------------------------------------------- Unit 1: Algebraic Expressions and Integers
U = 'algebraic-expressions-integers'


@t(U, 1)
def _(r, nm):
    d, p = r.choice([(3, 'hundredths'), (4, 'thousandths'), (5, 'ten-thousandths')])
    digit = R(r, 2, 9)
    whole = R(r, 100, 999)
    s = f'{whole}.' + ''.join(str(R(r, 0, 9)) if i != d - 2 else str(digit) for i in range(d))
    pos = d - 1
    val = Fr(digit, 10 ** (pos))
    return (f'In the number {s}, what is the value of the digit in the {p} place, multiplied by 1,000?',
            dz(val * 1000, 6), [f'The {p} place is position {pos} after the decimal point, so that digit is {digit}.', f'Its value is {dz(val, 6)}.', f'{dz(val, 6)} × 1,000 = {dz(val * 1000, 6)}.'])


@t(U, 3)
def _(r, nm):
    a, b, c, d = R(r, 2, 9), R(r, 2, 9), R(r, 2, 6), R(r, 2, 9)
    v = (a + b) * c - d * d
    return (f'Evaluate: ({a} + {b}) × {c} − {d}²', str(v),
            [f'Parentheses first: {a} + {b} = {a + b}.', f'Exponent: {d}² = {d * d}.', f'Multiply: {a + b} × {c} = {(a + b) * c}.', f'Subtract: {(a + b) * c} − {d * d} = {v}.'])


@t(U, 6)
def _(r, nm):
    a, b, c = R(r, 3, 15), R(r, 5, 20), R(r, 4, 12)
    v = -a + b - c
    return (f'At 6 a.m. the temperature was −{a}°F. It rose {b}°F by noon and then fell {c}°F by evening. What was the evening temperature, in °F?',
            str(v), [f'Start: −{a}.', f'Noon: −{a} + {b} = {-a + b}.', f'Evening: {-a + b} − {c} = {v}.'])


@t(U, 7)
def _(r, nm):
    a, b, c = R(r, 2, 15), R(r, 2, 15), R(r, 2, 15)
    v = -a - (-b) - c
    return (f'Find the value: −{a} − (−{b}) − {c}', str(v),
            [f'Subtracting −{b} is adding {b}: −{a} + {b} = {-a + b}.', f'Then {-a + b} − {c} = {v}.'])


@t(U, 9)
def _(r, nm):
    a, d = R(r, 3, 20), R(r, 4, 13)
    n = R(r, 8, 15)
    seq = [a + d * i for i in range(4)]
    return (f'The pattern {", ".join(map(str, seq))}, … continues by adding the same number. What is the {n}th term?', str(a + d * (n - 1)),
            [f'Each term adds {d}.', f'The {n}th term is {a} + {n - 1} × {d}.', f'= {a} + {d * (n - 1)} = {a + d * (n - 1)}.'])


@t(U, 10)
def _(r, nm):
    a, d = R(r, 3, 12), R(r, 3, 8)
    tot = R(r, 60, 150)
    k = (tot - a) // d + 1
    need = a + d * (k - 1)
    return (f'Figure 1 uses {a} tiles, and each new figure uses {d} more tiles than the one before. What is the largest figure number that uses no more than {tot} tiles?',
            str(k), [f'Figure n uses {a} + {d}(n − 1) tiles.', f'{a} + {d}(n − 1) ≤ {tot} gives n − 1 ≤ {fs(Fr(tot - a, d))}.', f'The largest whole number is n = {k} (Figure {k} uses {need} tiles).'])


@t(U, 11)
def _(r, nm):
    k, s = R(r, 3, 6), R(r, 2, 8)
    tot = k * s
    extra = R(r, 2, 9)
    return (f'A submarine descended {tot} feet in {k} equal stages, then rose {extra} feet. What was its total change in depth, in feet? (Use a negative number for down.)',
            str(-tot + extra), [f'Each stage: −{tot} ÷ {k} = −{s} feet.', f'After the descent: −{tot}.', f'Then −{tot} + {extra} = {-tot + extra}.'])


@t(U, 12)
def _(r, nm):
    x, y = R(r, 1, 9) * r.choice([-1, 1]), R(r, 1, 9) * r.choice([-1, 1])
    dx, dy = R(r, 2, 9) * r.choice([-1, 1]), R(r, 2, 9) * r.choice([-1, 1])
    X, Y = x + dx, y + dy
    if X == 0 or Y == 0:
        X, Y = X or 1, Y or 1
        dx, dy = X - x, Y - y
    q = 'I' if X > 0 and Y > 0 else 'II' if X < 0 < Y else 'III' if X < 0 and Y < 0 else 'IV'
    mv = lambda v, a, b: f'{abs(v)} units {a if v > 0 else b}'
    return (f'A point starts at ({x}, {y}). It moves {mv(dx, "right", "left")} and {mv(dy, "up", "down")}. In which quadrant does it end?',
            f'Quadrant {q}', [f'New x: {x} + ({dx}) = {X}; new y: {y} + ({dy}) = {Y}.', f'({X}, {Y}) has x {"positive" if X > 0 else "negative"} and y {"positive" if Y > 0 else "negative"}: Quadrant {q}.'])


# ---------------------------------------------------------------- Unit 2: One-Step Equations and Inequalities
U = 'one-step-equations-inequalities'


@t(U, 1)
def _(r, nm):
    a, b, c = R(r, 2, 20), R(r, 2, 20), R(r, 2, 20)
    kind = r.choice(['comm', 'assoc'])
    if kind == 'comm':
        return (f'{nm} rewrites {a} + {b} + {c} as {a} + {c} + {b} so that two numbers are easy to add first. The Commutative Property of Addition allows this. What is the sum?',
                str(a + b + c), [f'Only the order of {b} and {c} changed: Commutative Property of Addition.', f'Sum: {a} + {c} + {b} = {a + b + c}.'])
    return (f'{nm} rewrites ({a} × {b}) × {c} as {a} × ({b} × {c}) using the Associative Property of Multiplication. What is the product?',
            str(a * b * c), [f'Only the grouping changed: Associative Property of Multiplication.', f'Product: {a} × {b * c} = {a * b * c}.'])


@t(U, 2)
def _(r, nm):
    w, a, b = R(r, 3, 12), R(r, 2, 9), R(r, 2, 9)
    return (f'A garden is {w} m wide. Its length is {a} m of lettuce plus {b} m of beans. Use the Distributive Property to write the area as two products, then find the total area in square meters.',
            str(w * (a + b)), [f'{w}({a} + {b}) = {w} × {a} + {w} × {b}.', f'= {w * a} + {w * b}.', f'= {w * (a + b)} square meters.'])


@t(U, 3)
def _(r, nm):
    a, b, c, d = R(r, 2, 8), R(r, 2, 9), R(r, 2, 9), R(r, 2, 9)
    return (f'Simplify: {a}(x + {b}) + {c}x − {d}', f'{a + c}x + {a * b - d}' if a * b - d >= 0 else f'{a + c}x - {d - a * b}',
            [f'Distribute: {a}x + {a * b}.', f'Combine like terms: {a}x + {c}x = {a + c}x and {a * b} − {d} = {a * b - d}.'])


@t(U, 4)
def _(r, nm):
    a, b = R(r, 5, 40), R(r, 5, 40)
    x = R(r, 2, 9)
    return (f'Is the equation true, false, or open? {a} + {b} = {a + b + x} − {x}', 'true',
            [f'Left side: {a} + {b} = {a + b}.', f'Right side: {a + b + x} − {x} = {a + b}.', 'Both sides are equal and there is no variable, so it is true.'])


@t(U, 5)
def _(r, nm):
    s, up, down = R(r, 20, 60), R(r, 10, 30), R(r, 5, 15)
    end = s + up - down
    return (f'The temperature rose {up}°F and then fell {down}°F, ending at {end}°F. Write and solve an equation to find t, the starting temperature.',
            f't = {s}', [f't + {up} − {down} = {end}.', f't + {up - down} = {end}.', f't = {end} − {up - down} = {s}.'])


@t(U, 6)
def _(r, nm):
    k, each, left = R(r, 3, 9), R(r, 4, 15), R(r, 2, 9)
    return (f'{nm} cut a ribbon into {k} equal pieces of {each} cm and had {left} cm left over. Write and solve an equation to find r, the original length in cm.',
            f'r = {k * each + left}', [f'r − {left} = {k} × {each}.', f'r − {left} = {k * each}.', f'r = {k * each + left}.'])


@t(U, 7)
def _(r, nm):
    a, c = R(r, 6, 12), R(r, 2, 5)
    n = R(r, 8, 15)
    x = R(r, 2, n - 2)
    tot = a * x + c * (n - x)
    return (f'Adult tickets cost ${a} and child tickets cost ${c}. A group bought {n} tickets for ${tot}. How many child tickets did they buy?', str(n - x),
            [f'If x tickets are adult, {a}x + {c}({n} − x) = {tot}.', f'{a - c}x + {c * n} = {tot}, so x = {x} adult tickets.', f'Child tickets: {n} − {x} = {n - x}.'])


@t(U, 8)
def _(r, nm):
    lim, sp = R(r, 25, 65), R(r, 3, 12)
    return (f'The speed limit is {lim} miles per hour and {nm} is driving {sp} mph under it. Let s be a legal speed. Write the inequality for s, then give the greatest legal speed in mph.',
            str(lim), [f'Legal speeds are at most the limit: s ≤ {lim}.', f'{nm} is at {lim - sp} mph, which is legal.', f'The greatest legal speed is {lim} mph.'])


@t(U, 9)
def _(r, nm):
    has, goal, wk = R(r, 15, 60), R(r, 90, 200), R(r, 5, 15)
    need = goal - has
    w = -(-need // wk)
    return (f'{nm} has ${has} and wants at least ${goal}. {nm} saves ${wk} each week. What is the least number of whole weeks needed?',
            str(w), [f'{has} + {wk}w ≥ {goal}.', f'{wk}w ≥ {need}, so w ≥ {fs(Fr(need, wk))}.', f'The least whole number is {w}.'])


@t(U, 10)
def _(r, nm):
    m, c, fee = R(r, 40, 120), R(r, 6, 15), R(r, 3, 10)
    n = (m - fee) // c
    return (f'{nm} has ${m} to spend on shirts that cost ${c} each, plus a one-time ${fee} shipping fee. What is the greatest number of shirts {nm} can buy?',
            str(n), [f'{c}s + {fee} ≤ {m}.', f'{c}s ≤ {m - fee}, so s ≤ {fs(Fr(m - fee, c))}.', f'The greatest whole number is {n}.'])


# ---------------------------------------------------------------- Unit 3: Decimals and Equations
U = 'decimals-equations'


@t(U, 1)
def _(r, nm):
    a, b = Fr(R(r, 1000, 9999), 100), Fr(R(r, 1000, 9999), 1000)
    s = a + b
    return (f'Add {dz(a)} + {dz(b, 3)}, then round the sum to the nearest tenth.', dz(Fr(math.floor(s * 10 + Fr(1, 2)), 10), 1),
            [f'Sum: {dz(s, 3)}.', f'Look at the hundredths digit to round to the nearest tenth.', f'Rounded: {dz(Fr(math.floor(s * 10 + Fr(1, 2)), 10), 1)}.'])


@t(U, 2)
def _(r, nm):
    a, b, c = Fr(R(r, 21, 99), 10), Fr(R(r, 21, 99), 10), Fr(R(r, 21, 99), 10)
    ra, rb, rc = [math.floor(x + Fr(1, 2)) for x in (a, b, c)]
    return (f'Estimate {dz(a)} × {dz(b)} + {dz(c)} by rounding each number to the nearest whole number.', str(ra * rb + rc),
            [f'Round: {ra}, {rb} and {rc}.', f'{ra} × {rb} = {ra * rb}.', f'{ra * rb} + {rc} = {ra * rb + rc}.'])


@t(U, 3)
def _(r, nm):
    xs = [Fr(R(r, 10, 99), 10) for _ in range(5)]
    mean = sum(xs) / 5
    srt = sorted(xs)
    need_ = (mean - srt[2])
    return (f'Data: {", ".join(dz(x) for x in xs)}. How much greater is the mean than the median? (Use a negative number if the mean is less.)', dz(need_, 2),
            [f'Mean: {dz(sum(xs))} ÷ 5 = {dz(mean, 2)}.', f'Median (middle of {", ".join(dz(x) for x in srt)}): {dz(srt[2])}.', f'Difference: {dz(mean, 2)} − {dz(srt[2])} = {dz(need_, 2)}.'])


@t(U, 4)
def _(r, nm):
    r1, t1, r2, t2 = R(r, 30, 65), R(r, 2, 5), R(r, 30, 65), R(r, 2, 5)
    return (f'{nm} drives {r1} miles per hour for {t1} hours and then {r2} miles per hour for {t2} hours. Use d = rt for each part to find the total distance in miles.',
            str(r1 * t1 + r2 * t2), [f'First part: {r1} × {t1} = {r1 * t1} miles.', f'Second part: {r2} × {t2} = {r2 * t2} miles.', f'Total: {r1 * t1 + r2 * t2} miles.'])


@t(U, 5)
def _(r, nm):
    n, a, b = Fr(R(r, 100, 999), 100), Fr(R(r, 100, 999), 100), Fr(R(r, 100, 999), 100)
    tot = n + a - b
    return (f'Solve: n + {dz(a)} − {dz(b)} = {dz(tot)}', f'n = {dz(n)}',
            [f'Combine: {dz(a)} − {dz(b)} = {dz(a - b)}.', f'n + ({dz(a - b)}) = {dz(tot)}.', f'n = {dz(tot)} − ({dz(a - b)}) = {dz(n)}.'])


@t(U, 6)
def _(r, nm):
    p, g, cp = Fr(R(r, 30, 49), 10), Fr(R(r, 30, 90), 10), R(r, 2, 6)
    spent = p * g - cp
    return (f'Gas costs ${dz(p)} per gallon. {nm} used a ${cp} coupon and paid ${dz(spent)}. Solve {dz(p)}g − {cp} = {dz(spent)} to find g, the number of gallons.',
            f'g = {dz(g)}', [f'Add {cp}: {dz(p)}g = {dz(spent + cp)}.', f'Divide: g = {dz(spent + cp)} ÷ {dz(p)} = {dz(g)}.'])


@t(U, 7)
def _(r, nm):
    L, ml = Fr(R(r, 120, 990), 100), R(r, 150, 900)
    tot = L * 1000 + ml
    return (f'A jug holds {dz(L)} liters and a bottle holds {ml} milliliters. How many milliliters do they hold together?', f'{int(tot):,} milliliters' if tot.denominator == 1 else f'{dz(tot)} milliliters',
            [f'1 liter = 1,000 milliliters, so {dz(L)} L = {dz(L * 1000)} mL.', f'{dz(L * 1000)} + {ml} = {dz(tot)} mL.'])


# ---------------------------------------------------------------- Unit 4: Factors, Fractions and Exponents
U = 'factors-fractions-exponents'


@t(U, 1)
def _(r, nm):
    a, b = r.sample([2, 3, 4, 5, 6, 9, 10], 2)
    lo, hi = R(r, 10, 60), R(r, 100, 200)
    l = a * b // math.gcd(a, b)
    k = sum(1 for x in range(lo, hi + 1) if x % l == 0)
    return (f'How many whole numbers from {lo} to {hi} are divisible by both {a} and {b}?', str(k),
            [f'Divisible by both {a} and {b} means divisible by their least common multiple, {l}.', f'Multiples of {l} from {lo} to {hi}: {k}.'])


@t(U, 3)
def _(r, nm):
    p = r.choice([[2, 2, 3, 5], [2, 3, 3, 7], [2, 2, 2, 3, 5], [3, 3, 5, 7], [2, 5, 5, 7], [2, 2, 3, 3, 11]])
    q = r.choice([[2, 3, 5], [2, 2, 7], [3, 5, 7], [2, 3, 3, 5]])
    a, b = math.prod(p), math.prod(q)
    g = math.gcd(a, b)
    return (f'Use the prime factorizations of {a} and {b} to find their greatest common factor.', str(g),
            [f'{a} = {" · ".join(map(str, p))} and {b} = {" · ".join(map(str, q))}.', f'Multiply the shared prime factors: GCF = {g}.'])


@t(U, 4)
def _(r, nm):
    a, b, k = R(r, 2, 9), R(r, 10, 20), R(r, 2, 6)
    if math.gcd(a, b) != 1:
        a, b = 3, 14
    return (f'{nm} answered {a * k} of {b * k} questions correctly. Write the fraction correct in simplest form, then the fraction incorrect in simplest form. Give the fraction incorrect.',
            fs(Fr(b - a, b)), [f'Correct: {a * k}/{b * k} = {a}/{b}.', f'Incorrect: {b * k - a * k} of {b * k} = {fs(Fr(b - a, b))}.'])


@t(U, 5)
def _(r, nm):
    xs = r.choice([(['−4', '0', '7', '3/5'], 2), (['12', '−9', '0.25', '0'], 2), (['5', '−1', '2/3', '8'], 2), (['0', '6', '−2', '1.5'], 2)])
    lst = xs[0]
    ints = [x for x in lst if re.fullmatch(r'−?\d+', x)]
    return (f'How many of these numbers are integers: {", ".join(lst)}?', str(len(ints)),
            ['Integers are the whole numbers and their opposites (no fractions or decimals).', f'Integers here: {", ".join(ints)}.', f'Count: {len(ints)}.'])


@t(U, 6)
def _(r, nm):
    sq = r.choice([4, 9, 16, 25, 36, 49, 64, 81, 100])
    non = r.sample([2, 3, 5, 6, 7, 8, 10, 11, 12, 13, 15], 2)
    vals = [f'√{sq}', f'√{non[0]}', f'√{non[1]}', f'{R(r, 2, 9)}/{R(r, 2, 9)}']
    r.shuffle(vals)
    return (f'How many of these numbers are irrational: {", ".join(vals)}?', '2',
            [f'√{sq} = {math.isqrt(sq)} is rational, and a fraction is rational.', f'√{non[0]} and √{non[1]} are not perfect squares, so they are irrational.', 'Count: 2.'])


@t(U, 9)
def _(r, nm):
    a, e1 = R(r, 11, 99), R(r, 5, 8)
    b = R(r, 11, 99)
    e2 = e1 - R(r, 1, 2)
    A, B = a * 10 ** (e1 - 1), b * 10 ** (e2 - 1)
    tot = A + B
    e = len(str(tot)) - 1
    m = Fr(tot, 10 ** e)
    return (f'Add {dz(Fr(a, 10))} × 10^{e1} and {dz(Fr(b, 10))} × 10^{e2}. Write the sum in scientific notation.', f'{dz(m, 6)} × 10^{e}',
            [f'{dz(Fr(a, 10))} × 10^{e1} = {A:,} and {dz(Fr(b, 10))} × 10^{e2} = {B:,}.', f'Sum: {tot:,}.', f'Scientific notation: {dz(m, 6)} × 10^{e}.'])


@t(U, 10)
def _(r, nm):
    a, b = R(r, 2, 9), R(r, 2, 12)
    return (f'Evaluate: ∛{a ** 3} + √{b * b}', str(a + b), [f'∛{a ** 3} = {a} because {a}³ = {a ** 3}.', f'√{b * b} = {b}.', f'{a} + {b} = {a + b}.'])


# ---------------------------------------------------------------- Unit 5: Operations with Fractions
U = 'operations-fractions'


@t(U, 1)
def _(r, nm):
    fr_ = sorted({Fr(R(r, 1, 9), R(r, 2, 10)) for _ in range(3)})
    while len(fr_) < 3:
        fr_ = sorted({Fr(R(r, 1, 9), R(r, 2, 10)) for _ in range(3)})
    order = list(fr_)
    r.shuffle(order)
    return (f'Order from least to greatest: {", ".join(fs(x) for x in order)}', ', '.join(fs(x) for x in fr_),
            ['Compare with a common denominator or decimals: ' + ', '.join(f'{fs(x)} ≈ {dz(x, 3)}' for x in order) + '.', f'Least to greatest: {", ".join(fs(x) for x in fr_)}.'])


@t(U, 2)
def _(r, nm):
    a, b = r.choice([(1, 8), (3, 8), (5, 8), (7, 16), (3, 20), (7, 25), (9, 40)]), R(r, 2, 9)
    v = Fr(a[0], a[1]) + b
    return (f'Write {b} {a[0]}/{a[1]} as a decimal.', dz(v, 4), [f'{a[0]}/{a[1]} = {a[0]} ÷ {a[1]} = {dz(Fr(a[0], a[1]), 4)}.', f'{b} + {dz(Fr(a[0], a[1]), 4)} = {dz(v, 4)}.'])


@t(U, 3)
def _(r, nm):
    a, b, c = pf(r), pf(r), pf(r)
    v = a + b - c
    return (f'Simplify: {fs(a)} + {fs(b)} − {fs(c)}. Write the answer in simplest form.', fs(v),
            [f'{fs(a)} + {fs(b)} = {fs(a + b)}.', f'{fs(a + b)} − {fs(c)} = {fs(v)}.'])


@t(U, 4)
def _(r, nm):
    a, b, c = pf(r), pf(r), pf(r)
    v = a * b / c
    return (f'Simplify: {fs(a)} × {fs(b)} ÷ {fs(c)}. Write the answer in simplest form.', fs(v),
            [f'{fs(a)} × {fs(b)} = {fs(a * b)}.', f'Dividing by {fs(c)} is multiplying by {fs(1 / c)}: {fs(a * b)} × {fs(1 / c)} = {fs(v)}.'])


@t(U, 6)
def _(r, nm):
    m, a, b = pf(r), pf(r), pf(r)
    tot = m + a - b
    return (f'Solve: m + {fs(a)} − {fs(b)} = {fs(tot)}', f'm = {fs(m)}',
            [f'Combine: {fs(a)} − {fs(b)} = {fs(a - b)}.', f'm = {fs(tot)} − ({fs(a - b)}) = {fs(m)}.'])


@t(U, 7)
def _(r, nm):
    fr_ = r.choice([Fr(1, 2), Fr(1, 3), Fr(2, 3), Fr(3, 4), Fr(2, 5), Fr(3, 8)])
    p = fr_.denominator * R(r, 6, 30)
    left = p - fr_ * p
    return (f'{nm} has read {fs(fr_)} of a book and has {int(left)} pages left. Solve to find p, the total number of pages.', f'p = {p}',
            [f'Pages left are {fs(1 - fr_)} of the book: ({fs(1 - fr_)})p = {int(left)}.', f'p = {int(left)} ÷ {fs(1 - fr_)} = {p}.'])


@t(U, 8)
def _(r, nm):
    a, b, e = R(r, 1, 3), R(r, 2, 5), R(r, 2, 3)
    v = Fr(a, b) ** e * b
    return (f'Evaluate: ({a}/{b})^{e} × {b}. Write the answer in simplest form.', fs(v),
            [f'({a}/{b})^{e} = {fs(Fr(a, b) ** e)}.', f'× {b} = {fs(v)}.'])


# ---------------------------------------------------------------- Unit 6: Ratios, Proportions and Percentages
U = 'ratios-proportions-percentages'


@t(U, 1)
def _(r, nm):
    a, b = R(r, 8, 16), R(r, 3, 7)
    pa, pb = Fr(R(r, 300, 900), 100), Fr(R(r, 120, 400), 100)
    ua, ub = pa / a, pb / b
    need = ua != ub
    better = f'{a} ounces' if ua < ub else f'{b} ounces'
    diff = abs(ua - ub) * 100
    return (f'Store A sells {a} ounces for ${dz(pa)} and Store B sells {b} ounces for ${dz(pb)}. How many cents per ounce do you save with the better buy? Round to the nearest tenth of a cent.',
            dz(Fr(math.floor(diff * 10 + Fr(1, 2)), 10), 1), [f'A: ${dz(pa)} ÷ {a} ≈ ${dz(ua, 4)} per ounce.', f'B: ${dz(pb)} ÷ {b} ≈ ${dz(ub, 4)} per ounce.', f'Difference ≈ {dz(diff, 3)} cents ≈ {dz(Fr(math.floor(diff * 10 + Fr(1, 2)), 10), 1)} cents.'])


@t(U, 2)
def _(r, nm):
    a, b, k = R(r, 2, 9), R(r, 3, 12), R(r, 2, 6)
    return (f'Find x so that {a}/{b} = x/{b * k}, then find x + {k}.', str(a * k + k), [f'{b} × {k} = {b * k}, so x = {a} × {k} = {a * k}.', f'x + {k} = {a * k + k}.'])


@t(U, 3)
def _(r, nm):
    s1, k = R(r, 3, 9), R(r, 2, 5)
    s2 = s1 + R(r, 1, 6)
    return (f'Two triangles are similar. The small one has sides {s1} cm and {s2} cm. The longer of those sides on the large triangle is {s2 * k} cm. Find the sum of the large triangle\'s two sides that correspond to these, in cm.',
            str((s1 + s2) * k), [f'Scale factor: {s2 * k} ÷ {s2} = {k}.', f'Other side: {s1} × {k} = {s1 * k} cm.', f'Sum: {s1 * k} + {s2 * k} = {(s1 + s2) * k} cm.'])


@t(U, 5)
def _(r, nm):
    p = R(r, 3, 95)
    n = R(r, 2, 20) * 10
    return (f'Change {p}% to a decimal, then use the decimal to find {p}% of {n}.', dz(Fr(p * n, 100)), [f'{p}% = {dz(Fr(p, 100))}.', f'{dz(Fr(p, 100))} × {n} = {dz(Fr(p * n, 100))}.'])


@t(U, 6)
def _(r, nm):
    p = r.choice([10, 20, 25, 40, 50])
    whole = R(r, 4, 20) * (100 // math.gcd(100, p))
    part = whole * p // 100
    return (f'{part} students, which is {p}% of the grade, signed up for band. How many students in the grade did not sign up?', str(whole - part),
            [f'Whole: {part} ÷ {dz(Fr(p, 100))} = {whole}.', f'Not signed up: {whole} − {part} = {whole - part}.'])


@t(U, 7)
def _(r, nm):
    p, n = r.choice([5, 10, 15, 20, 25, 30, 40]), R(r, 4, 30) * 4
    v = Fr(p * n, 100)
    return (f'Write and solve an equation: What number is {p}% more than {n}?', f'n = {dz(n + v)}',
            [f'{p}% of {n} = {dz(v)}.', f'n = {n} + {dz(v)} = {dz(n + v)}.'])


@t(U, 8)
def _(r, nm):
    a = R(r, 4, 20) * 10
    p1, p2 = r.choice([10, 20, 25, 50]), r.choice([10, 20, 25, 50])
    b = a * (100 + p1) // 100
    c = b * (100 - p2) / 100
    return (f'A price of ${a} rises {p1}% and then the new price falls {p2}%. What is the final price?', money(Fr(c)),
            [f'Rise: ${a} × {dz(Fr(100 + p1, 100))} = ${b}.', f'Fall: ${b} × {dz(Fr(100 - p2, 100))} = {money(Fr(c))}.'])


@t(U, 9)
def _(r, nm):
    pr, off, tax = Fr(R(r, 2000, 9000), 100), r.choice([10, 15, 20, 25, 30]), r.choice([5, 6, 6.25, 7])
    sale = pr * (100 - off) / 100
    tot = sale * (100 + Fr(str(tax))) / 100
    return (f'A {money(pr)} item is on sale for {off}% off. Sales tax of {tax}% is added to the sale price. What is the total cost? Round to the nearest cent.', money(tot),
            [f'Sale price: {money(pr)} × {dz(Fr(100 - off, 100))} = {money(sale)}.', f'With tax: {money(sale)} × {dz((100 + Fr(str(tax))) / 100, 4)} ≈ {money(tot)}.'])


@t(U, 10)
def _(r, nm):
    k = R(r, 2, 9)
    xs = sorted(r.sample(range(2, 13), 3))
    x4 = R(r, 13, 20)
    return (f'y is proportional to x. When x = {xs[0]}, y = {k * xs[0]}. Find the constant of proportionality, then find y when x = {x4}.', str(k * x4),
            [f'k = y/x = {k * xs[0]} ÷ {xs[0]} = {k}.', f'y = {k} × {x4} = {k * x4}.'])


@t(U, 11)
def _(r, nm):
    g = R(r, 2, 9)
    a, b = r.choice([(1, 2), (2, 3), (3, 4), (1, 5), (2, 5), (3, 5), (4, 5), (5, 6), (1, 3), (5, 7), (3, 7)])
    return (f'Factor out the greatest common factor: {g * a}x + {g * b}', f'{g}({a if a > 1 else ""}x + {b})',
            [f'GCF of {g * a} and {g * b} is {g}.' if math.gcd(a, b) == 1 else f'Factor out {g}.', f'{g * a}x ÷ {g} = {a if a > 1 else ""}x and {g * b} ÷ {g} = {b}.'])


# ---------------------------------------------------------------- Unit 7: Solving Equations and Inequalities
U = 'solving-equations-inequalities'


@t(U, 1)
def _(r, nm):
    base, per, m, tip = R(r, 3, 9), R(r, 2, 4), R(r, 3, 15), R(r, 2, 6)
    tot = base + per * m + tip
    return (f'A taxi charges ${base} plus ${per} per mile. {nm} also gave a ${tip} tip and paid ${tot} in all. How many miles was the ride?', str(m),
            [f'{base} + {per}m + {tip} = {tot}.', f'{per}m = {tot - base - tip}.', f'm = {m}.'])


@t(U, 3)
def _(r, nm):
    a, b, x = Fr(R(r, 11, 49), 10), Fr(R(r, 11, 99), 10), R(r, 3, 15)
    c = R(r, 2, 5)
    rhs = c * (a * x + b)
    return (f'Solve: {c}({dz(a)}t + {dz(b)}) = {dz(rhs)}', f't = {x}', [f'Divide by {c}: {dz(a)}t + {dz(b)} = {dz(rhs / c)}.', f'{dz(a)}t = {dz(rhs / c - b)}.', f't = {x}.'])


@t(U, 4)
def _(r, nm):
    a, b, n = R(r, 2, 9), R(r, 3, 20), R(r, 3, 15)
    c = a * n - b
    n = Fr(n)
    return (f'"{b} less than {a} times a number is {c}." Write the equation and solve for the number.', f'n = {fs(n)}',
            [f'{a}n − {b} = {c}.', f'{a}n = {c + b}.', f'n = {fs(n)}.'])


@t(U, 7)
def _(r, nm):
    d1, r1, d2, r2 = R(r, 2, 6) * 30, 30 * R(r, 1, 2), R(r, 2, 6) * 40, 40
    t1, t2 = Fr(d1, r1), Fr(d2, r2)
    return (f'Use t = d/r: {nm} drives {d1} miles at {r1} mph, then {d2} miles at {r2} mph. How many hours in all?', f'{fs(t1 + t2)} hours',
            [f'First: {d1} ÷ {r1} = {fs(t1)} h.', f'Second: {d2} ÷ {r2} = {fs(t2)} h.', f'Total: {fs(t1 + t2)} hours.'])


@t(U, 8)
def _(r, nm):
    p, rate, y = R(r, 10, 60) * 100, r.choice([2, 2.5, 3, 3.5, 4, 4.5]), R(r, 2, 8)
    i = Fr(p) * Fr(str(rate)) / 100 * y
    return (f'{nm} deposits ${p:,} at {rate}% simple interest per year. What is the balance after {y} years?', money(p + i),
            [f'I = prt = {p:,} × {dz(Fr(str(rate)) / 100, 4)} × {y} = {money(i)}.', f'Balance: ${p:,} + {money(i)} = {money(p + i)}.'])


# ---------------------------------------------------------------- Unit 8: Linear Functions and Graphing
U = 'linear-functions-graphing'


@t(U, 3)
def _(r, nm):
    m, b = R(r, 2, 6) * r.choice([-1, 1]), R(r, 1, 9) * r.choice([-1, 1])
    x0 = Fr(-b, m)
    return (f'For the line y = {m}x {"+" if b > 0 else "−"} {abs(b)}, find the y-intercept and the x-intercept. Give the x-intercept.', fs(x0),
            [f'y-intercept: {b}.', f'x-intercept: set y = 0: {m}x = {-b}.', f'x = {fs(x0)}.'])


@t(U, 4)
def _(r, nm):
    h, b = R(r, 40, 90), R(r, 3, 8)
    x = R(r, 2, h // b - 1)
    return (f'A candle is {h} cm tall and burns {b} cm per hour. Write a rule for its height y after x hours, then find the height after {x} hours.', f'{h - b * x} cm',
            [f'y = −{b}x + {h}.', f'y = −{b}({x}) + {h} = {h - b * x} cm.'])


@t(U, 5)
def _(r, nm):
    m, b, goal = Fr(R(r, 5, 30), 10), R(r, 5, 20), R(r, 30, 70)
    x = (goal - b) / m
    return (f'A trend line for hours practiced (x) and points scored (y) is y = {dz(m)}x + {b}. About how many hours of practice predict {goal} points? Round to the nearest tenth.',
            dz(Fr(math.floor(x * 10 + Fr(1, 2)), 10), 1), [f'{dz(m)}x + {b} = {goal}.', f'{dz(m)}x = {goal - b}.', f'x ≈ {dz(Fr(math.floor(x * 10 + Fr(1, 2)), 10), 1)} hours.'])


@t(U, 6)
def _(r, nm):
    m1, m2 = r.sample([-3, -2, -1, 1, 2, 3], 2)
    x = R(r, -4, 4)
    b1, b2 = R(r, -6, 6), None
    y = m1 * x + b1
    b2 = y - m2 * x
    ln = lambda m, b: ('' if m == 1 else '−' if m == -1 else str(m)) + 'x' + (f' + {b}' if b > 0 else f' − {-b}' if b < 0 else '')
    return (f'Solve the system: y = {ln(m1, b1)} and y = {ln(m2, b2)}. Write the solution as an ordered pair.', f'({x}, {y})',
            [f'Set equal: {ln(m1, b1)} = {ln(m2, b2)}.', f'{m1 - m2}x = {b2 - b1}, so x = {x}.', f'y = {m1}({x}) + ({b1}) = {y}.'])


@t(U, 8)
def _(r, nm):
    m, b = R(r, 1, 4) * r.choice([-1, 1]), R(r, -6, 6)
    x, y = R(r, -5, 5), R(r, -9, 9)
    val = m * x + b
    rel = 'yes' if y < val else 'no'
    ln = ('' if m == 1 else '−' if m == -1 else str(m)) + 'x' + (f' + {b}' if b > 0 else f' − {-b}' if b < 0 else '')
    return (f'Is the point ({x}, {y}) a solution of y < {ln}? Answer yes or no.', rel,
            [f'Substitute x = {x}: {m}({x}) + ({b}) = {val}.', f'Is {y} < {val}? {"Yes" if rel == "yes" else "No"}.'])


# ---------------------------------------------------------------- Unit 9: Spatial Thinking
U = 'spatial-thinking'


@t(U, 1)
def _(r, nm):
    n = R(r, 5, 12)
    return (f'There are {n} points, and no three lie on the same line. How many triangles can be drawn using three of the points as vertices?', str(math.comb(n, 3)),
            [f'Each triangle is a choice of 3 points from {n}, order not mattering.', f'{n} × {n - 1} × {n - 2} ÷ 6 = {math.comb(n, 3)}.'])


@t(U, 2)
def _(r, nm):
    a = R(r, 25, 155)
    return (f'Two lines intersect. One angle measures {a}°. Find its vertical angle plus twice an adjacent angle, in degrees.', f'{a + 2 * (180 - a)}°',
            [f'The vertical angle equals {a}°.', f'An adjacent angle is {180 - a}°.', f'{a} + 2 × {180 - a} = {a + 2 * (180 - a)}°.'])


@t(U, 3)
def _(r, nm):
    n = r.choice([5, 6, 8, 9, 10, 12])
    s = (n - 2) * 180
    return (f'A regular polygon has interior angles that add to {s}°. How many sides does it have?', str(n),
            [f'Angle sum = (n − 2) × 180.', f'(n − 2) × 180 = {s}, so n − 2 = {n - 2}.', f'n = {n}.'])


@t(U, 4)
def _(r, nm):
    g = r.choice([4, 5, 6, 8, 10])
    L, W = g * R(r, 4, 12), g * R(r, 2, 8)
    p = 2 * (L + W)
    return (f'A rectangular yard is {L} feet by {W} feet. A fence post stands at every corner and every {g} feet along the edge. How many posts are there?',
            str(p // g), [f'Perimeter: 2({L} + {W}) = {p} feet.', f'Around a closed loop, posts = gaps: {p} ÷ {g} = {p // g}.'])


@t(U, 6)
def _(r, nm):
    d = R(r, 4, 30) * 2
    return (f'A circle has diameter {d} in. Find its circumference. Use 3.14 for π.', f'{dz(Fr(314, 100) * d)} in.', [f'C = πd.', f'3.14 × {d} = {dz(Fr(314, 100) * d)} in.'])


@t(U, 10)
def _(r, nm):
    x, y = R(r, 1, 9) * r.choice([-1, 1]), R(r, 1, 9) * r.choice([-1, 1])
    return (f'Point A({x}, {y}) is rotated 90° counterclockwise about the origin. What are the coordinates of A′?', f'({-y}, {x})',
            [f'A 90° counterclockwise rotation maps (x, y) to (−y, x).', f'({x}, {y}) → ({-y}, {x}).'])


# ---------------------------------------------------------------- Unit 10: Area and Volume
U = 'area-volume'


@t(U, 1)
def _(r, nm):
    b, h, k = R(r, 4, 15), R(r, 3, 12), R(r, 2, 4)
    return (f'A parallelogram has base {b} in. and height {h} in. A second parallelogram has the same height and {k} times the base. What is the area of the second one, in square inches?',
            str(b * k * h), [f'Second base: {b} × {k} = {b * k} in.', f'Area: {b * k} × {h} = {b * k * h} in².'])


@t(U, 2)
def _(r, nm):
    b1, b2, h = R(r, 4, 14), R(r, 4, 14), R(r, 2, 10) * 2
    return (f'A trapezoid has bases {b1} ft and {b2} ft and height {h} ft. A rectangle has the same area and width {h // 2} ft. How long is the rectangle, in feet?',
            str((b1 + b2)), [f'Trapezoid area: ½({b1} + {b2})({h}) = {(b1 + b2) * h // 2} ft².', f'Length: {(b1 + b2) * h // 2} ÷ {h // 2} = {b1 + b2} ft.'])


@t(U, 3)
def _(r, nm):
    R1, R2 = R(r, 2, 6), R(r, 7, 12)
    v = Fr(314, 100) * (R2 * R2 - R1 * R1)
    return (f'A ring is the region between circles of radius {R2} cm and {R1} cm with the same center. Find its area. Use 3.14 for π and round to the nearest tenth.', f'{dz(v, 1)} cm²',
            [f'Big circle: 3.14 × {R2}² = {dz(Fr(314, 100) * R2 * R2)}.', f'Small circle: 3.14 × {R1}² = {dz(Fr(314, 100) * R1 * R1)}.', f'Difference: {dz(v, 1)} cm².'])


@t(U, 4)
def _(r, nm):
    n = R(r, 3, 8)
    return (f'A prism has two congruent bases that are {n}-sided polygons. How many faces, edges and vertices does it have? Give the number of edges.', str(3 * n),
            [f'Faces: 2 bases + {n} rectangles = {n + 2}.', f'Edges: {n} on each base + {n} joining them = {3 * n}.', f'Vertices: 2 × {n} = {2 * n}.'])


@t(U, 6)
def _(r, nm):
    b, s = R(r, 4, 14), R(r, 4, 14)
    return (f'A square pyramid has base edge {b} ft and slant height {s} ft. How many square feet of material cover only its four triangular faces?', f'{2 * b * s} ft²',
            [f'Each triangle: ½ × {b} × {s} = {fs(Fr(b * s, 2))} ft².', f'Four triangles: 4 × {fs(Fr(b * s, 2))} = {2 * b * s} ft².'])


@t(U, 8)
def _(r, nm):
    b, h = R(r, 3, 12), R(r, 2, 10) * 3
    return (f'A square pyramid has base edge {b} cm and height {h} cm. A prism with the same base and height holds how many more cubic centimeters than the pyramid?',
            f'{2 * b * b * h // 3} cm³', [f'Prism: {b}² × {h} = {b * b * h} cm³.', f'Pyramid: ⅓ × {b * b * h} = {b * b * h // 3} cm³.', f'Difference: {2 * b * b * h // 3} cm³.'])


# ---------------------------------------------------------------- Unit 11: Right Triangles and Algebra
U = 'right-triangles-algebra'


@t(U, 1)
def _(r, nm):
    k = R(r, 5, 15)
    n = k * k + R(r, 1, 2 * k)
    near = k if n - k * k < (k + 1) ** 2 - n else k + 1
    return (f'Which whole number is closest to √{n}? Use the perfect squares just below and above {n}.', str(near),
            [f'{k}² = {k * k} and {k + 1}² = {(k + 1) ** 2}, so √{n} is between {k} and {k + 1}.', f'{n} is {n - k * k} above {k * k} and {(k + 1) ** 2 - n} below {(k + 1) ** 2}, so it is closer to {near}.'])


@t(U, 2)
def _(r, nm):
    a, b, c = r.choice([(3, 4, 5), (5, 12, 13), (8, 15, 17), (7, 24, 25), (6, 8, 10), (9, 12, 15)])
    k = R(r, 1, 3)
    return (f'A {c * k}-foot ladder leans against a wall with its base {a * k} feet from the wall. How high up the wall does it reach, in feet?', f'{b * k} feet',
            [f'h² + {a * k}² = {c * k}².', f'h² = {c * c * k * k} − {a * a * k * k} = {b * b * k * k}.', f'h = {b * k} feet.'])


@t(U, 3)
def _(r, nm):
    a, b, c = r.choice([(3, 4, 5), (5, 12, 13), (8, 15, 17), (6, 8, 10)])
    x, y = R(r, -6, 6), R(r, -6, 6)
    p2 = (x + a, y + b)
    return (f'Find the perimeter of the right triangle with vertices ({x}, {y}), ({p2[0]}, {y}) and ({p2[0]}, {p2[1]}).', str(a + b + c),
            [f'Legs: {a} and {b}.', f'Hypotenuse: √({a}² + {b}²) = {c}.', f'Perimeter: {a} + {b} + {c} = {a + b + c}.'])


@t(U, 4)
def _(r, nm):
    p, m, M = R(r, 3, 9), R(r, 2, 6), R(r, 5, 12)
    return (f'A machine makes {p * m} parts in {m} minutes. How many parts does it make in {M} minutes, and how many minutes does it need for {p * M + p * m} parts? Give the minutes.',
            str(M + m), [f'Rate: {p * m} ÷ {m} = {p} parts per minute.', f'{p * M + p * m} ÷ {p} = {M + m} minutes.'])


@t(U, 5)
def _(r, nm):
    s = R(r, 2, 12)
    return (f'In a 30°-60°-90° triangle, the shorter leg is {s}. Find the hypotenuse and the longer leg. Give the hypotenuse.', str(2 * s),
            [f'Hypotenuse = 2 × shorter leg = {2 * s}.', f'Longer leg = {s}√3.'])


@t(U, 6)
def _(r, nm):
    a, b, c = r.choice([(3, 4, 5), (5, 12, 13), (8, 15, 17), (7, 24, 25), (20, 21, 29)])
    return (f'In right triangle ABC, ∠C is the right angle, BC = {a} and AC = {b}. Find AB, then tan A as a fraction.', fs(Fr(a, b)),
            [f'AB = √({a}² + {b}²) = {c}.', f'tan A = opposite/adjacent = BC/AC = {fs(Fr(a, b))}.'])


@t(U, 7)
def _(r, nm):
    d, ang = R(r, 30, 120), r.choice([20, 25, 30, 35, 40, 45, 50, 55])
    h = d * math.tan(math.radians(ang))
    eye = R(r, 4, 6)
    tot = h + eye
    return (f'{nm}\'s eyes are {eye} ft above the ground. From {d} ft away, the angle of elevation to the top of a tree is {ang}°. How tall is the tree, to the nearest foot?', f'{round(tot)} feet',
            [f'Height above eye level: {d} × tan {ang}° ≈ {h:.2f} ft.', f'Add eye height: {h:.2f} + {eye} ≈ {tot:.2f}.', f'≈ {round(tot)} feet.'])


# ---------------------------------------------------------------- Unit 12: Data Analysis and Probability
U = 'data-analysis-probability'


@t(U, 1)
def _(r, nm):
    c = [R(r, 1, 9) for _ in range(4)]
    return (f'A frequency table shows: 1–5: {c[0]}; 6–10: {c[1]}; 11–15: {c[2]}; 16–20: {c[3]}. What percent of the values are greater than 10? Round to the nearest whole percent.',
            f'{round(100 * (c[2] + c[3]) / sum(c))}%', [f'Total: {sum(c)}.', f'Greater than 10: {c[2]} + {c[3]} = {c[2] + c[3]}.', f'{c[2] + c[3]}/{sum(c)} ≈ {round(100 * (c[2] + c[3]) / sum(c))}%.'])


@t(U, 2)
def _(r, nm):
    xs = sorted(R(r, 10, 60) for _ in range(9))
    q1 = Fr(xs[1] + xs[2], 2)
    q3 = Fr(xs[6] + xs[7], 2)
    return (f'Data: {", ".join(map(str, xs))}. Find the interquartile range.', fs(q3 - q1),
            [f'Median: {xs[4]}. Lower half {", ".join(map(str, xs[:4]))}; upper half {", ".join(map(str, xs[5:]))}.', f'Q1 = {fs(q1)}, Q3 = {fs(q3)}.', f'IQR = {fs(q3 - q1)}.'])


@t(U, 5)
def _(r, nm):
    a, b = R(r, 2, 8), R(r, 2, 8)
    n = a + b
    return (f'A bag has {a} red and {b} blue marbles. You draw one marble, do not replace it, and draw again. What is P(red, then red)? Write a fraction in simplest form.',
            fs(Fr(a * (a - 1), n * (n - 1))), [f'P(red first) = {a}/{n}.', f'P(red second) = {a - 1}/{n - 1}.', f'Multiply: {fs(Fr(a * (a - 1), n * (n - 1)))}.'])


@t(U, 6)
def _(r, nm):
    n = R(r, 5, 10)
    return (f'In how many ways can 1st, 2nd and 3rd place be awarded among {n} runners?', str(n * (n - 1) * (n - 2)),
            [f'{n} choices for 1st, {n - 1} for 2nd, {n - 2} for 3rd.', f'{n} × {n - 1} × {n - 2} = {n * (n - 1) * (n - 2)}.'])


@t(U, 7)
def _(r, nm):
    tr, k = R(r, 2, 8) * 10, None
    k = R(r, 1, tr - 1)
    fut = R(r, 2, 10) * tr
    return (f'In {tr} trials, the bus was late {k} times. Based on this, how many late arrivals would you predict in {fut} trips?', fs(Fr(k * fut, tr)),
            [f'Experimental probability: {fs(Fr(k, tr))}.', f'Prediction: {fs(Fr(k, tr))} × {fut} = {fs(Fr(k * fut, tr))}.'])


@t(U, 9)
def _(r, nm):
    ma, mb, mad = R(r, 30, 60), None, R(r, 2, 6)
    mb = ma + mad * R(r, 1, 4)
    return (f'Class A has a mean of {ma} push-ups and Class B a mean of {mb}. Both have a mean absolute deviation of {mad}. How many MADs apart are the means?', str((mb - ma) // mad),
            [f'Difference of means: {mb} − {ma} = {mb - ma}.', f'{mb - ma} ÷ {mad} = {(mb - ma) // mad} MADs.'])


# ---------------------------------------------------------------- Unit 13: Nonlinear Functions and Polynomials
U = 'nonlinear-functions-polynomials'


@t(U, 1)
def _(r, nm):
    a, d, n = R(r, 2, 20), R(r, 2, 9), R(r, 20, 60)
    s = n * (2 * a + (n - 1) * d) // 2
    return (f'For the arithmetic sequence {a}, {a + d}, {a + 2 * d}, …, find term {n}, then add it to the first term.', str(a + a + (n - 1) * d),
            [f'Term {n}: {a} + {n - 1} × {d} = {a + (n - 1) * d}.', f'Sum: {a} + {a + (n - 1) * d} = {a + a + (n - 1) * d}.'])


@t(U, 2)
def _(r, nm):
    a, x = R(r, 2, 5), R(r, 2, 5)
    return (f'For f(x) = {a}x², find f({x}) and f({2 * x}). How many times larger is f({2 * x})?', '4',
            [f'f({x}) = {a * x * x}.', f'f({2 * x}) = {a * 4 * x * x}.', f'{a * 4 * x * x} ÷ {a * x * x} = 4.'])


@t(U, 3)
def _(r, nm):
    v, p, y = R(r, 3, 40) * 100, r.choice([5, 8, 10, 12, 15]), R(r, 2, 4)
    val = Fr(v) * Fr(100 - p, 100) ** y
    return (f'A ${v:,} item loses {p}% of its value each year. How much value does it lose in total over {y} years? Round to the nearest cent.', money(v - val),
            [f'Value after {y} years: {v:,} × {dz(Fr(100 - p, 100))}^{y} ≈ {money(val)}.', f'Loss: ${v:,} − {money(val)} = {money(v - val)}.'])


@t(U, 7)
def _(r, nm):
    a, b, c = R(r, 1, 6), R(r, 1, 6) * r.choice([-1, 1]), R(r, 1, 6) * r.choice([-1, 1])
    b2 = a + b
    # (x + a)(x + b) + c x
    lin = a + b + c
    con = a * b
    sgn = lambda v: (f'+ {v}' if v > 0 else f'- {-v}')
    return (f'Multiply and simplify: (x + {a})(x {sgn(b)}) {sgn(c)}x', f'x² {sgn(lin)}x {sgn(con)}'.replace('+ 1x', '+ x').replace('- 1x', '- x') if lin else f'x² {sgn(con)}',
            [f'(x + {a})(x {sgn(b)}) = x² {sgn(a + b)}x {sgn(con)}.', f'Add {c}x: x² {sgn(lin)}x {sgn(con)}.'])


@t(U, 8)
def _(r, nm):
    q, d = R(r, 4, 20), R(r, 4, 20)
    tot = q * 25 + d * 10
    return (f'A jar has {q + d} quarters and dimes worth {money(Fr(tot, 100))}. How many dimes are there?', str(d),
            [f'0.25q + 0.10({q + d} − q) = {dz(Fr(tot, 100))}.', f'0.15q = {dz(Fr(tot, 100))} − {dz(Fr((q + d) * 10, 100))}, so q = {q}.', f'Dimes: {q + d} − {q} = {d}.'])


SIG = lambda q: re.sub(r'\d+(?:\.\d+)?', '#', q['prompt']).strip()
NUM = re.compile(r'-?\d[\d,]*(?:\.\d+)?(?:/\d+)?')


def distractors(ans, steps, rng):
    pair = re.fullmatch(r'\((-?\d+), (-?\d+)\)', ans)
    if pair:
        x, y = int(pair.group(1)), int(pair.group(2))
        return [p for p in dict.fromkeys(f'({a}, {b})' for a, b in ((y, x), (-x, y), (x, -y), (-x, -y), (x + 1, y))) if p != ans][:3]
    m = re.fullmatch(r'(.*?)(-?\d[\d,]*(?:\.\d+)?(?:/\d+)?)(.*)', ans)
    if not m:
        # worded answer: other worded answers would need a bank; build from swaps
        return [ans + ' (only the first step)', 'cannot be determined', 'none of these'][:3]
    pre, num, post = m.groups()
    def val(s):
        s = s.replace(',', '')
        return Fr(s) if '/' in s or '.' not in s else Fr(s)
    a = val(num)
    pool = []
    for s in steps:
        for x in NUM.findall(s.replace('−', '-')):
            try:
                v = val(x)
            except Exception:
                continue
            if v != a and v not in pool:
                pool.append(v)
    out, seen = [], {ans}
    fmt = lambda v: pre + (fs(v) if '/' in num else (f'{v.numerator / v.denominator:,.2f}' if (',' in num and '.' in num) else (f'{int(v):,}' if (',' in num and v.denominator == 1) else (dz(v, 4) if '.' in num else fs(v))))) + post
    for v in pool[::-1]:
        o = fmt(v)
        if o not in seen and len(out) < 3:
            seen.add(o); out.append(o)
    k = 1
    while len(out) < 3:
        for v in (a + k, a - k, a * 2 if k == 1 else a + 10 * k):
            o = fmt(v)
            if len(out) < 3 and o not in seen:
                seen.add(o); out.append(o)
        k += 1
    return out


def rewrite(q, fn, rng, nm, fam, note, used):
    """Rewrite q in place with a prompt not in used; leave it unchanged (return False) if none is found."""
    for _ in range(80):
        prompt, ans, steps = (H.sup(x) if isinstance(x, str) else [H.sup(y) for y in x] for x in fn(rng, nm))
        if prompt not in used:
            break
    else:
        return False
    used.add(prompt)
    q['prompt'], q['answer'], q['solutionSteps'] = prompt, ans, steps
    for k in ('hint', 'diagram'):
        q.pop(k, None)
    if q['format'] == 'multiple-choice':
        opts = [ans] + distractors(ans, steps, rng)
        rng.shuffle(opts)
        q['options'] = [{'text': o, 'correct': o == ans} for o in opts]
    else:
        q.pop('options', None)
    q['sourceNotes'] = lib.SOURCE.format(fam=fam) + note if hasattr(lib, 'SOURCE') else f'Original Claude-authored item (family: {fam}).' + note
    return True


def pinned():
    """Ids that other audit scripts or tests rely on: never rewritten."""
    srcs = []
    for d, fs_ in ((lib.HERE, os.listdir(lib.HERE)), (os.path.join(lib.ROOT, 'scripts'), [f for f in os.listdir(os.path.join(lib.ROOT, 'scripts')) if 'grade7' in f or 'prealgebra7' in f or 'g7' in f])):
        for f in fs_:
            p = os.path.join(d, f)
            if f.endswith(('.py', '.cjs', '.json')) and f not in ('levels.py', 'verify_levels.py', 'practice-tests.json') and os.path.isfile(p):   # the practice tests are picked after this runs
                srcs.append(open(p, encoding='utf-8').read())
    ids = set(re.findall(r'pa7-[a-z]+-s\d\d-(?:cp1|cp2|honors)-\w+', ''.join(srcs)))
    for f in os.listdir(lib.BANKS):
        if f.endswith('.json'):
            ids |= set(re.findall(r'Partner-check companion to (\S+) ', open(os.path.join(lib.BANKS, f), encoding='utf-8').read()))
    return ids


def main():
    banks = lib.load()
    keep = pinned()
    NOTE = ' Rewritten in place: whole-site audit 2 #3 (2026-11-20), {lv} item that reused a {low} template (was: “{old}”); keys rechecked by verify_levels.py.'
    done = {'cp1': 0, 'honors': 0}
    TAG = 'audit 2 #3'
    ok = lambda q, lv: (q['level'] == lv and q['format'] in ('multiple-choice', 'short-answer') and not q.get('diagram')
                        and q['id'] not in keep and not re.search(r'-(?:h|pc)\d\d$', q['id']) and 'Partner-check companion' not in q.get('sourceNotes', ''))
    for u in lib.UNITS:
        qs = banks[u]['questions']
        for sid in sorted({q['skillId'] for q in qs}):
            n = int(sid.rsplit('-', 1)[1]); a = lib.ABBR[u]
            sk = [q for q in qs if q['skillId'] == sid]
            fn1, fnh = T.get((u, n)), (None if (u, n) == ('algebraic-expressions-integers', 1) else H.T.get((u, n)))
            # Choose the items to rewrite from the bank as it was before any rewrite, so reruns choose the same ones:
            # an item rewritten earlier carries the TAG note and stays chosen.
            low1 = {SIG(q) for q in sk if q['level'] == 'cp2'}
            c1 = sorted((q for q in sk if fn1 and ok(q, 'cp1') and (TAG in q['sourceNotes'] or SIG(q) in low1)), key=lambda q: (TAG not in q['sourceNotes'], q['id']))[:CAP]
            ids1 = {q['id'] for q in c1}
            lowh = low1 | {SIG(q) for q in sk if q['level'] == 'cp1' and q['id'] not in ids1}
            ch = sorted((q for q in sk if fnh and ok(q, 'honors') and (TAG in q['sourceNotes'] or SIG(q) in lowh)), key=lambda q: (TAG not in q['sourceNotes'], q['id']))[:CAP]
            chosen = ids1 | {q['id'] for q in ch}
            used = {q['prompt'] for q in sk if q['id'] not in chosen}
            for lv, cand, fn, fam in (('cp1', c1, fn1, f'g7_cp1_added_step_{a}_s{n:02d}'), ('honors', ch, fnh, f'g7_honors_multistep_{a}_s{n:02d}')):
                for i, q in enumerate(cand):
                    rng = random.Random(f'g7-a2-3-{q["id"]}')
                    old = re.search(r'\(was: “(.*?)”\)', q['sourceNotes'])
                    old = old.group(1) if old else re.sub(r'\s+', ' ', q['prompt'])[:70]
                    base = q['sourceNotes'].split(' Rewritten in place: whole-site audit 2 #3')[0]
                    if TAG in q['sourceNotes']:
                        q['sourceNotes'] = base
                    if rewrite(q, fn, rng, N[sum(map(ord, q['id'])) % len(N)], fam,
                               NOTE.format(lv='Standard' if lv == 'cp1' else 'Advanced', low='Support' if lv == 'cp1' else 'lower-level', old=old.replace('“', '"').replace('”', '"')), used):
                        done[lv] += 1
    lib.save(banks)
    print('levels: rewrote', done['cp1'], 'Standard and', done['honors'], 'Advanced items')


if __name__ == '__main__':
    main()
