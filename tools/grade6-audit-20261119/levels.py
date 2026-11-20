"""Grade 6 audit, whole-site audit #9 (2026-11-20): Standard and Honors items stop reusing lower-level templates.
In each skill, up to CAP Standard (cp1) items whose prompt is a CP2 prompt with different numbers are rewritten in place
as a Standard item with an added step (one generator per skill, below). Up to CAP Honors items that reuse a CP2 or CP1
template are rewritten in place from that skill's Honors multi-step generator (honors.py).
Only text items are rewritten: multiple choice and short answer without a diagram. An item keeps its id, skill, level,
format and standards; a multiple-choice item gets distractors from the solution's intermediate values.
Keys are recomputed from the printed prompts by verify_levels.py. Idempotent: rerunning changes nothing."""
import math, os, random, re, sys
from fractions import Fraction as Fr
sys.path.insert(0, os.path.dirname(__file__))
import lib
import honors as H

CAP = 5
N, m, mixed, dz, sup = H.N, H.m, H.mixed, H.dz, H.sup
R = lambda rng, a, b: rng.randint(a, b)
T = {}


def t(u, n):
    def deco(fn):
        T[(u, n)] = fn
        return fn
    return deco


def dl(xs):
    return ', '.join(str(x) for x in xs)


def med(xs):
    xs = sorted(xs); k = len(xs)
    return Fr(xs[k // 2]) if k % 2 else Fr(xs[k // 2 - 1] + xs[k // 2], 2)


# ---------------------------------------------------------------- Ratios, Rates, Percent, Proportions
U = 'ratios-rates-percent-proportions'


@t(U, 1)
def _(rng, nm):
    a, b = rng.choice([(2, 3), (3, 5), (4, 7), (5, 2), (3, 4), (7, 3)]); k = R(rng, 4, 12)
    return (f'In a bag, the ratio of red marbles to blue marbles is {a} : {b}. There are {(a + b) * k} marbles in all. How many blue marbles are there?',
            str(b * k), [f'Each group of {a} red and {b} blue has {a + b} marbles.', f'Number of groups: {(a + b) * k} ÷ {a + b} = {k}.', f'Blue marbles: {b} × {k} = {b * k}.'])


@t(U, 2)
def _(rng, nm):
    r, h = R(rng, 9, 18), R(rng, 3, 8); h2 = rng.choice([x for x in range(2, 13) if x != h])
    return (f'{nm} earns ${r * h} for {h} hours of work. At the same rate, how many dollars does {nm} earn in {h2} hours?',
            str(r * h2), [f'Unit rate: ${r * h} ÷ {h} = ${r} per hour.', f'{h2} hours: {h2} × ${r} = ${r * h2}.'])


@t(U, 3)
def _(rng, nm):
    a, b = rng.choice([(2, 3), (3, 2), (4, 3), (2, 5), (3, 4)]); k = R(rng, 3, 9); extra = R(rng, 2, 9)
    return (f'A lemonade recipe uses {b} scoops of mix for every {a} cups of water. {nm} has {a * k} cups of water and {b * k + extra} scoops of mix. If {nm} uses all of the water, how many scoops of mix are left over?',
            str(extra), [f'{a * k} cups of water is {a * k} ÷ {a} = {k} batches.', f'Scoops used: {b} × {k} = {b * k}.', f'Left over: {b * k + extra} − {b * k} = {extra}.'])


@t(U, 4)
def _(rng, nm):
    ua, ub = rng.sample(range(12, 41), 2); pa, pb = rng.sample([8, 10, 12, 16, 20, 24], 2)
    ca, cb = Fr(ua * pa, 100), Fr(ub * pb, 100)
    return (f'Store A sells {pa} ounces of cereal for {m(ca)}. Store B sells {pb} ounces for {m(cb)}. How many cents less per ounce is the better buy?',
            str(abs(ua - ub)), [f'Store A: {m(ca)} ÷ {pa} = {ua}¢ per ounce.', f'Store B: {m(cb)} ÷ {pb} = {ub}¢ per ounce.', f'Difference: {abs(ua - ub)}¢ per ounce.'])


@t(U, 5)
def _(rng, nm):
    a, b = rng.choice([(1, 15), (2, 25), (1, 20), (3, 40), (2, 30)]); spd = rng.choice([30, 40, 45, 50, 60]); hrs = R(rng, 2, 6)
    miles = spd * hrs
    while (miles * a) % b:
        hrs += 1; miles = spd * hrs
    inch = Fr(miles * a, b)
    return (f'On a map, {a} inch{"es" if a > 1 else ""} represent{"" if a > 1 else "s"} {b} miles. Two towns are {mixed(inch)} inches apart on the map. A car drives between them at {spd} miles per hour. How many hours does the trip take?',
            str(hrs), [f'Set up the proportion {a}/{b} = {mixed(inch)}/d, so d = {mixed(inch)} × {b} ÷ {a} = {miles} miles.', f'Time: {miles} ÷ {spd} = {hrs} hours.'])


@t(U, 6)
def _(rng, nm):
    p = rng.choice([15, 20, 25, 30, 35, 40, 45, 60, 65, 70, 75, 80]); n = 20 * R(rng, 10, 40)
    ride = n * p // 100
    return (f'{p}% of the {n} students at a school ride the bus. How many students do not ride the bus?',
            str(n - ride), [f'Riders: {p}% of {n} = {p}/100 × {n} = {ride}.', f'Not riding: {n} − {ride} = {n - ride}.'])


@t(U, 7)
def _(rng, nm):
    b = rng.choice([4, 5, 10, 20, 25, 50]); a = R(rng, 1, b - 1); pc = Fr(a * 100, b)
    return (f'In a class survey, {a} out of {b} students chose pizza as their favorite lunch. What percent of the students did not choose pizza?',
            f'{dz(100 - pc)}%', [f'{a}/{b} = {dz(pc)}/100 = {dz(pc)}%.', f'Not pizza: 100% − {dz(pc)}% = {dz(100 - pc)}%.'])


@t(U, 8)
def _(rng, nm):
    p = rng.choice([3, 4, 6, 8, 9]); n = R(rng, 4, 20)
    while (p * n) % 12:
        n += 1
    f = p * n // 12
    return (f'A ribbon is {f} feet long. {nm} cuts it into pieces that are each {p} inches long. How many pieces does {nm} get?',
            str(n), [f'Convert to inches: {f} × 12 = {f * 12} inches.', f'Pieces: {f * 12} ÷ {p} = {n}.'])


# ---------------------------------------------------------------- Fractions, Decimals, Operations
U = 'fractions-decimals-operations'


@t(U, 1)
def _(rng, nm):
    a, b = rng.choice([(1, 2), (3, 4), (2, 3), (1, 3), (3, 8), (5, 6)]); c, d = rng.choice([(1, 8), (1, 6), (1, 4), (1, 12), (1, 16)]); k = R(rng, 2, 6)
    tot = k * Fr(a, b); n = tot / Fr(c, d)
    return (f'Each jug holds {a}/{b} gallon of juice. Each glass holds {c}/{d} gallon. How many glasses can be filled from {k} full jugs?',
            mixed(n), [f'Juice in all: {k} × {a}/{b} = {mixed(tot)} gallons.', f'Glasses: {mixed(tot)} ÷ {c}/{d} = {mixed(tot)} × {d}/{c} = {mixed(n)}.'])


@t(U, 2)
def _(rng, nm):
    w = R(rng, 3, 9); a, b = rng.choice([(2, 3), (3, 4), (3, 5), (2, 5), (4, 5), (5, 8)])
    q = Fr(w) / Fr(a, b); full = q.numerator // q.denominator; left = w - full * Fr(a, b)
    if left == 0:
        w += 1; q = Fr(w) / Fr(a, b); full = q.numerator // q.denominator; left = w - full * Fr(a, b)
    return (f'{nm} has {w} cups of flour. Each batch of muffins needs {a}/{b} cup. After making as many full batches as possible, how many cups of flour are left? Write the answer in simplest form.',
            mixed(left), [f'{w} ÷ {a}/{b} = {w} × {b}/{a} = {mixed(q)}, so {full} full batches.', f'Flour used: {full} × {a}/{b} = {mixed(full * Fr(a, b))} cups.', f'Left: {w} − {mixed(full * Fr(a, b))} = {mixed(left)} cup.'])


@t(U, 3)
def _(rng, nm):
    L = Fr(R(rng, 5, 12)) + rng.choice([Fr(1, 2), Fr(1, 4), Fr(3, 4), Fr(1, 3), Fr(2, 3)]); p = rng.choice([Fr(3, 4), Fr(5, 6), Fr(1, 1) + Fr(1, 2), Fr(1, 1) + Fr(1, 4), Fr(2, 3)])
    q = L / p; full = q.numerator // q.denominator
    return (f'A board is {mixed(L)} feet long. {nm} cuts as many pieces as possible that are each {mixed(p)} feet long. How many full pieces does {nm} get?',
            str(full), [f'Divide: {mixed(L)} ÷ {mixed(p)} = {L.numerator}/{L.denominator} × {p.denominator}/{p.numerator} = {mixed(q)}.', f'Only whole pieces count, so {nm} gets {full} pieces.'])


@t(U, 4)
def _(rng, nm):
    s, tch, c = R(rng, 300, 1400), R(rng, 12, 60), rng.choice([36, 42, 48, 52, 56, 60])
    tot = s + tch; buses = -(-tot // c)
    return (f'{s} students and {tch} teachers are going on a field trip. Each bus holds {c} people. How many buses are needed?',
            str(buses), [f'People in all: {s} + {tch} = {tot}.', f'{tot} ÷ {c} = {tot // c} R {tot % c}.', f'The extra {tot % c} people need one more bus: {buses} buses.' if tot % c else f'Exactly {buses} buses.'])


@t(U, 5)
def _(rng, nm):
    a, b = R(rng, 250, 1899), R(rng, 250, 1899); have = (a + b) // 100 * 100 + rng.choice([500, 1000, 1500, 2000])
    A, B, Hv = Fr(a, 100), Fr(b, 100), Fr(have, 100)
    return (f'{nm} has {m(Hv)}. {nm} buys a book for {m(A)} and a backpack for {m(B)}. How much money does {nm} have left?',
            m(Hv - A - B), [f'Total spent: {m(A)} + {m(B)} = {m(A + B)}.', f'Left: {m(Hv)} − {m(A + B)} = {m(Hv - A - B)}.'])


@t(U, 6)
def _(rng, nm):
    p = Fr(R(rng, 289, 499), 100); g = Fr(R(rng, 16, 30), 2); cost = p * g
    cost_c = Fr(math.floor(cost * 100 + Fr(1, 2)), 100); bill = 50 if cost_c < 50 else 100
    return (f'Gas costs {m(p)} per gallon. {nm} buys {dz(g, 1)} gallons and pays with a ${bill} bill. How much change does {nm} get?',
            m(bill - cost_c), [f'Cost: {dz(g, 1)} × {m(p)} = {m(cost_c)}' + ('.' if cost == cost_c else ' (rounded to the nearest cent).'), f'Change: ${bill} − {m(cost_c)} = {m(bill - cost_c)}.'])


@t(U, 7)
def _(rng, nm):
    a, b = rng.choice([(8, 6), (10, 8), (12, 8), (6, 4), (10, 12), (8, 12), (6, 10)]); L = math.lcm(a, b)
    return (f'Hot dogs come in packs of {a} and buns come in packs of {b}. {nm} wants the same number of hot dogs and buns with none left over. What is the least number of packs of buns {nm} must buy?',
            str(L // b), [f'The number of hot dogs and buns must be a common multiple of {a} and {b}.', f'LCM({a}, {b}) = {L}.', f'Packs of buns: {L} ÷ {b} = {L // b}.'])


@t(U, 8)
def _(rng, nm):
    k = R(rng, 3, 9); a = Fr(R(rng, 150, 499), 100); b = Fr(R(rng, 50, 199), 100)
    return (f'Each of {k} students buys a notebook for {m(a)} and a pen for {m(b)}. Use the Distributive Property to find the total cost in dollars.',
            m(k * (a + b)), [f'Total = {k}({m(a)} + {m(b)}) = {k} × {m(a)} + {k} × {m(b)}.', f'= {m(k * a)} + {m(k * b)} = {m(k * (a + b))}.'])


# ---------------------------------------------------------------- Rational Numbers
U = 'rational-numbers'


@t(U, 1)
def _(rng, nm):
    d, r = R(rng, 20, 60), R(rng, 5, 18)
    return (f'A diver is {d} feet below sea level. She swims up {r} feet. Write an integer for her new position, in feet, relative to sea level.',
            str(-d + r), [f'{d} feet below sea level is -{d}.', f'Up {r} feet: -{d} + {r} = {-d + r}.'])


@t(U, 2)
def _(rng, nm):
    a, b = R(rng, 4, 12), R(rng, 1, 3)
    while a == b:
        b += 1
    return (f'On a number line, point A is at -{a}. Point B is {b} units to the right of A. Point C is the opposite of B. What number is at point C?',
            str(a - b), [f'B: -{a} + {b} = {-a + b}.', f'The opposite of {-a + b} is {a - b}.'])


@t(U, 3)
def _(rng, nm):
    xs = rng.sample(range(-15, 12), 5)
    return (f'The low temperatures (°F) for five days were {dl(xs)}. How many degrees warmer was the warmest day than the coldest day?',
            str(max(xs) - min(xs)), [f'Order: {dl(sorted(xs))}.', f'Warmest {max(xs)}, coldest {min(xs)}: {max(xs)} − ({min(xs)}) = {max(xs) - min(xs)}.'])


@t(U, 4)
def _(rng, nm):
    a, b = rng.sample(range(-14, 6), 2); c = R(rng, 2, 6)
    w = max(a, b)
    return (f'The low temperature was {a}°C in Town A and {b}°C in Town B. Town C was {c} degrees colder than the warmer of the two towns. What was the temperature in Town C, in °C?',
            str(w - c), [f'Compare: {min(a, b)} < {w}, so the warmer town was at {w}°C.', f'Town C: {w} − {c} = {w - c}.'])


@t(U, 5)
def _(rng, nm):
    a, b, c = R(rng, 3, 15), R(rng, 2, 15), R(rng, 1, 9)
    return (f'Evaluate: |-{a}| + |{b}| − |-{c}|',
            str(a + b - c), [f'|-{a}| = {a}, |{b}| = {b}, |-{c}| = {c}.', f'{a} + {b} − {c} = {a + b - c}.'])


@t(U, 6)
def _(rng, nm):
    a, b = rng.sample(range(15, 95), 2); c = R(rng, 10, 90)
    return (f'Three account balances are -${a}, -${b} and ${c}. How many more dollars does the person who owes the most owe than the person who owes the least?',
            str(abs(a - b)), [f'Only the negative balances are debts: |-{a}| = {a} and |-{b}| = {b}; ${c} is not owed.', f'{max(a, b)} − {min(a, b)} = {abs(a - b)}.'])


@t(U, 7)
def _(rng, nm):
    x, y = rng.choice([-1, 1]) * R(rng, 1, 9), rng.choice([-1, 1]) * R(rng, 1, 9)
    return (f'Point ({x}, {y}) is reflected across the x-axis, and then the image is reflected across the y-axis. What are the coordinates of the final image?',
            f'({-x}, {-y})', [f'Across the x-axis: ({x}, {-y}).', f'Across the y-axis: ({-x}, {-y}).'])


@t(U, 8)
def _(rng, nm):
    x, y, a, b = R(rng, -6, 6), R(rng, -6, 6), R(rng, 2, 8), R(rng, 2, 8)
    return (f'A robot starts at ({x}, {y}). It moves {a} units left and then {b} units up. What are its final coordinates?',
            f'({x - a}, {y + b})', [f'{a} units left: x = {x} − {a} = {x - a}.', f'{b} units up: y = {y} + {b} = {y + b}.'])


@t(U, 9)
def _(rng, nm):
    x1, x2 = sorted(rng.sample(range(-8, 9), 2)); y1, y2 = sorted(rng.sample(range(-8, 9), 2))
    return (f'A rectangle has vertices ({x1}, {y1}), ({x2}, {y1}), ({x2}, {y2}) and ({x1}, {y2}). What is its area in square units?',
            str((x2 - x1) * (y2 - y1)), [f'Width: |{x2} − ({x1})| = {x2 - x1}.', f'Height: |{y2} − ({y1})| = {y2 - y1}.', f'Area: {x2 - x1} × {y2 - y1} = {(x2 - x1) * (y2 - y1)}.'])


# ---------------------------------------------------------------- Expressions and Equations
U = 'expressions-equations'


@t(U, 1)
def _(rng, nm):
    a, b = R(rng, 3, 12), R(rng, 2, 5)
    return (f'Evaluate: {a}^2 + {b}^3', str(a * a + b ** 3), [f'{a}^2 = {a * a} and {b}^3 = {b ** 3}.', f'{a * a} + {b ** 3} = {a * a + b ** 3}.'])


@t(U, 2)
def _(rng, nm):
    p, f, n = R(rng, 6, 15), R(rng, 2, 9), R(rng, 3, 9)
    return (f'Concert tickets cost ${p} each, plus a ${f} fee for the whole order. Write an expression for the cost of t tickets, and use it to find the cost in dollars of {n} tickets.',
            str(p * n + f), [f'Expression: {p}t + {f}.', f'For t = {n}: {p} × {n} + {f} = {p * n + f}.'])


@t(U, 3)
def _(rng, nm):
    a, b = R(rng, 1, 6), R(rng, 1, 6); c = rng.choice([x for x in (2, 3, 4) if ((a + b) ** 2) % x == 0] or [1]); d = R(rng, 1, 9)
    return (f'Evaluate: ({a} + {b})^2 ÷ {c} − {d}', str((a + b) ** 2 // c - d),
            [f'Parentheses: {a} + {b} = {a + b}.', f'Exponent: {a + b}^2 = {(a + b) ** 2}.', f'Divide, then subtract: {(a + b) ** 2} ÷ {c} − {d} = {(a + b) ** 2 // c} − {d} = {(a + b) ** 2 // c - d}.'])


@t(U, 4)
def _(rng, nm):
    a, b, c = R(rng, 2, 9), R(rng, 2, 9), R(rng, 2, 9)
    return (f'Simplify: {a}(x + {b}) + {c}x', f'{a + c}x + {a * b}', [f'Distribute: {a}(x + {b}) = {a}x + {a * b}.', f'Combine like terms: {a}x + {c}x = {a + c}x, so {a + c}x + {a * b}.'])


@t(U, 5)
def _(rng, nm):
    a, x, b = R(rng, 2, 9), R(rng, 2, 12), R(rng, 1, 20); c = a * x + b
    opts = sorted({x, x + 1, x - 1, x + 2} - {0})
    return (f'Which value from the set {{{dl(opts)}}} makes {a}x + {b} = {c} true?', str(x),
            [f'Test x = {x}: {a} × {x} + {b} = {a * x} + {b} = {c}. ✓', 'The other values give ' + ', '.join(str(a * v + b) for v in opts if v != x) + f', not {c}.'])


@t(U, 6)
def _(rng, nm):
    k, x, d = R(rng, 3, 12), R(rng, 3, 15), R(rng, 2, 20)
    return (f'Solve {k}x = {k * x}. Then find the value of x + {d}.', str(x + d), [f'Divide both sides by {k}: x = {k * x} ÷ {k} = {x}.', f'x + {d} = {x} + {d} = {x + d}.'])


@t(U, 7)
def _(rng, nm):
    r, H_ = R(rng, 9, 20), R(rng, 6, 15)
    return (f'A table shows hours worked (h): 1, 2, 3 and pay in dollars (p): {r}, {2 * r}, {3 * r}. Write an equation for p in terms of h, and use it to find the pay in dollars for {H_} hours.',
            str(r * H_), [f'Pay goes up ${r} for each hour, so p = {r}h.', f'For h = {H_}: p = {r} × {H_} = {r * H_}.'])


# ---------------------------------------------------------------- Inequalities
U = 'inequalities'


@t(U, 1)
def _(rng, nm):
    Hh = rng.choice([42, 44, 46, 48, 52, 54]); k = Hh - R(rng, 2, 9)
    return (f'Riders on a roller coaster must be at least {Hh} inches tall. {nm} is {k} inches tall. Write an inequality for the height h of a rider, and find how many more inches {nm} must grow to ride.',
            str(Hh - k), [f'Inequality: h ≥ {Hh}.', f'{nm} needs {Hh} − {k} = {Hh - k} more inches.'])


@t(U, 2)
def _(rng, nm):
    a = R(rng, 3, 12); b = a * R(rng, 4, 15) + R(rng, 1, a - 1)
    return (f'Solve {a}x ≤ {b}. What is the greatest whole number that is a solution?', str(b // a),
            [f'Divide both sides by {a}: x ≤ {b}/{a} = {mixed(Fr(b, a))}.', f'The greatest whole number not more than {mixed(Fr(b, a))} is {b // a}.'])


@t(U, 3)
def _(rng, nm):
    a, n = R(rng, 3, 15), R(rng, 18, 30)
    return (f'How many whole numbers from 0 to {n} are solutions of x > {a}?', str(n - a),
            [f'x > {a} means x = {a + 1}, {a + 2}, …, {n}.', f'Count: {n} − {a} = {n - a} whole numbers.'])


@t(U, 4)
def _(rng, nm):
    a = R(rng, -8, 8); strict = rng.random() < 0.5
    return (f'A number line graph has {"an open" if strict else "a closed"} circle at {a} and an arrow pointing right. What is the least integer that is a solution?',
            str(a + 1 if strict else a), [f'The graph shows x {">" if strict else "≥"} {a}.', f'{"An open circle leaves out " + str(a) + ", so the least integer is " + str(a + 1) if strict else "A closed circle includes " + str(a) + ", so the least integer is " + str(a)}.'])


@t(U, 5)
def _(rng, nm):
    W, b = rng.choice([1500, 2000, 2500, 3000]), R(rng, 40, 95)
    while W % b == 0:
        b += 1
    return (f'An elevator can carry at most {W} pounds. Each box weighs {b} pounds. Write an inequality for the number of boxes x, and find the greatest number of boxes the elevator can carry.',
            str(W // b), [f'Inequality: {b}x ≤ {W}.', f'x ≤ {W} ÷ {b} = {mixed(Fr(W, b))}.', f'Only whole boxes: at most {W // b} boxes.'])


# ---------------------------------------------------------------- Geometry
U = 'geometry'


@t(U, 1)
def _(rng, nm):
    a, b, h = R(rng, 4, 14), R(rng, 4, 14), R(rng, 2, 10)
    A = Fr((a + b) * h, 2); c = rng.choice([x for x in range(3, 13) if (A / x).denominator == 1] or [1])
    return (f'A trapezoid has bases {a} cm and {b} cm and height {h} cm. A parallelogram with base {c} cm has the same area. What is the height of the parallelogram, in cm?',
            mixed(A / c), [f'Trapezoid: ({a} + {b}) × {h} ÷ 2 = {mixed(A)} cm².', f'Parallelogram height: {mixed(A)} ÷ {c} = {mixed(A / c)} cm.'])


@t(U, 2)
def _(rng, nm):
    a, b, c, d = R(rng, 3, 14), R(rng, 3, 14), R(rng, 2, 10), R(rng, 2, 10)
    A1, A2 = Fr(a * b, 2), Fr(c * d, 2)
    if A1 == A2:
        a += 1; A1 = Fr(a * b, 2)
    return (f'Right triangle P has legs {a} ft and {b} ft. Right triangle Q has legs {c} ft and {d} ft. How many square feet greater is the area of the larger triangle?',
            mixed(abs(A1 - A2)), [f'P: {a} × {b} ÷ 2 = {mixed(A1)} ft².', f'Q: {c} × {d} ÷ 2 = {mixed(A2)} ft².', f'Difference: {mixed(abs(A1 - A2))} ft².'])


@t(U, 3)
def _(rng, nm):
    b, h, c = R(rng, 4, 16), R(rng, 4, 16), rng.choice([2, 3, 4, 5, 6])
    A = Fr(b * h, 2)
    return (f'A triangular sail has a base of {b} ft and a height of {h} ft. The fabric costs ${c} per square foot. How many dollars does the fabric for the sail cost?',
            mixed(A * c), [f'Area: {b} × {h} ÷ 2 = {mixed(A)} ft².', f'Cost: {mixed(A)} × ${c} = ${mixed(A * c)}.'])


@t(U, 4)
def _(rng, nm):
    W, Hh = R(rng, 10, 20), R(rng, 8, 16); a, b = R(rng, 2, W - 4), R(rng, 2, Hh - 4)
    A = W * Hh - Fr(a * b, 2)
    return (f'A garden is a {W} m by {Hh} m rectangle with a right-triangle corner cut off. The cut-off triangle has legs {a} m and {b} m. What is the area of the garden, in m²?',
            mixed(A), [f'Rectangle: {W} × {Hh} = {W * Hh} m².', f'Triangle: {a} × {b} ÷ 2 = {mixed(Fr(a * b, 2))} m².', f'Garden: {W * Hh} − {mixed(Fr(a * b, 2))} = {mixed(A)} m².'])


@t(U, 5)
def _(rng, nm):
    l, w, h = R(rng, 4, 12), R(rng, 3, 9), R(rng, 3, 10); d = R(rng, 1, h - 1)
    return (f'A fish tank is {l} in. long, {w} in. wide and {h} in. tall. It is filled with water to a depth of {d} in. How many cubic inches of the tank are empty?',
            str(l * w * (h - d)), [f'Empty height: {h} − {d} = {h - d} in.', f'Empty volume: {l} × {w} × {h - d} = {l * w * (h - d)} in³.'])


@t(U, 6)
def _(rng, nm):
    x1, x2 = sorted(rng.sample(range(-7, 8), 2)); y1, y2 = sorted(rng.sample(range(-7, 8), 2))
    return (f'Three vertices of a rectangle are ({x1}, {y1}), ({x2}, {y1}) and ({x2}, {y2}). Find the fourth vertex, and then the perimeter of the rectangle in units.',
            str(2 * ((x2 - x1) + (y2 - y1))), [f'The fourth vertex is ({x1}, {y2}).', f'Sides: {x2 - x1} and {y2 - y1} units.', f'Perimeter: 2({x2 - x1} + {y2 - y1}) = {2 * ((x2 - x1) + (y2 - y1))}.'])


@t(U, 7)
def _(rng, nm):
    s = R(rng, 3, 10); w = R(rng, 1, 2 * s - 1)
    while w == s:
        w = R(rng, 1, 2 * s - 1)
    l = 2 * s - w
    return (f'A rectangle has vertices (0, 0), ({l}, 0), ({l}, {w}) and (0, {w}). A square has the same perimeter as the rectangle. What is the area of the square, in square units?',
            str(s * s), [f'Rectangle perimeter: 2({l} + {w}) = {4 * s}.', f'Square side: {4 * s} ÷ 4 = {s}.', f'Square area: {s} × {s} = {s * s}.'])


@t(U, 8)
def _(rng, nm):
    l, w, h = R(rng, 4, 14), R(rng, 3, 10), R(rng, 2, 9)
    sa = l * w + 2 * l * h + 2 * w * h
    return (f'A box with no top is {l} in. long, {w} in. wide and {h} in. tall. How many square inches of cardboard cover its outside?',
            str(sa), [f'Bottom: {l} × {w} = {l * w}.', f'Front and back: 2 × {l} × {h} = {2 * l * h}; sides: 2 × {w} × {h} = {2 * w * h}.', f'Total (no top): {l * w} + {2 * l * h} + {2 * w * h} = {sa} in².'])


# ---------------------------------------------------------------- Data Displays
U = 'data-displays'


@t(U, 2)
def _(rng, nm):
    xs = [R(rng, 1, 30) for _ in range(rng.choice([10, 20]))]; lo = rng.choice([1, 6, 11, 16, 21]); hi = lo + 9
    k = sum(lo <= x <= hi for x in xs)
    return (f'Data: {dl(xs)}. A histogram uses the interval {lo}–{hi}. What percent of the data values are in that interval?',
            f'{dz(Fr(k * 100, len(xs)))}%', [f'Values from {lo} to {hi}: {k} of {len(xs)}.', f'{k}/{len(xs)} = {dz(Fr(k * 100, len(xs)))}%.'])


@t(U, 3)
def _(rng, nm):
    xs = [R(rng, 60, 99) for _ in range(4)]; v = R(rng, 60, 99)
    while (sum(xs) + v) % 5:
        v += 1
    return (f"{nm}'s first four quiz scores are {dl(xs)}. {nm} scores {v} on the fifth quiz. What is the mean of all five scores?",
            str((sum(xs) + v) // 5), [f'Sum: {" + ".join(str(x) for x in xs + [v])} = {sum(xs) + v}.', f'Mean: {sum(xs) + v} ÷ 5 = {(sum(xs) + v) // 5}.'])


@t(U, 4)
def _(rng, nm):
    while True:
        xs = sorted(R(rng, 10, 60) for _ in range(8))
        if (xs[1] + xs[2]) % 2 == 0 and (xs[5] + xs[6]) % 2 == 0:
            break
    q1, q3 = (xs[1] + xs[2]) // 2, (xs[5] + xs[6]) // 2
    return (f'Data: {dl(xs)}. How much greater is the range than the interquartile range?',
            str((xs[-1] - xs[0]) - (q3 - q1)), [f'Range: {xs[-1]} − {xs[0]} = {xs[-1] - xs[0]}.', f'Q1 = ({xs[1]} + {xs[2]}) ÷ 2 = {q1}; Q3 = ({xs[5]} + {xs[6]}) ÷ 2 = {q3}; IQR = {q3 - q1}.', f'{xs[-1] - xs[0]} − {q3 - q1} = {(xs[-1] - xs[0]) - (q3 - q1)}.'])


@t(U, 5)
def _(rng, nm):
    def ds():
        while True:
            xs = [R(rng, 2, 20) for _ in range(4)]
            if sum(xs) % 4 == 0:
                return xs
    A, B = ds(), ds()
    ma = sum(abs(Fr(x) - Fr(sum(A), 4)) for x in A) / 4; mb = sum(abs(Fr(x) - Fr(sum(B), 4)) for x in B) / 4
    if ma == mb:
        return _(rng, nm)
    return (f'Data set A: {dl(A)}. Data set B: {dl(B)}. How much greater is the larger mean absolute deviation (MAD) than the smaller one?',
            dz(abs(ma - mb)), [f'A: mean {sum(A) // 4}, MAD = {dz(ma)}.', f'B: mean {sum(B) // 4}, MAD = {dz(mb)}.', f'Difference: {dz(abs(ma - mb))}.'])


@t(U, 6)
def _(rng, nm):
    A, B = [R(rng, 5, 40) for _ in range(5)], [R(rng, 5, 40) for _ in range(5)]
    ra, rb = max(A) - min(A), max(B) - min(B)
    if ra == rb:
        A[0] = min(A) - 1 if min(A) > 1 else max(A) + 1; ra = max(A) - min(A)
    return (f'Points scored — Team A: {dl(A)}; Team B: {dl(B)}. How much greater is the larger range than the smaller range?',
            str(abs(ra - rb)), [f'Team A range: {max(A)} − {min(A)} = {ra}.', f'Team B range: {max(B)} − {min(B)} = {rb}.', f'Difference: {abs(ra - rb)}.'])


@t(U, 7)
def _(rng, nm):
    while True:
        xs = sorted([R(rng, 1, 6) for _ in range(6)] + [R(rng, 18, 28)])
        if sum(xs) % 7 == 0:
            break
    mean = sum(xs) // 7
    return (f'Data: {dl(xs)}. The data are skewed right. How much greater is the mean than the median?',
            str(mean - xs[3]), [f'Mean: {sum(xs)} ÷ 7 = {mean}.', f'Median (4th value): {xs[3]}.', f'{mean} − {xs[3]} = {mean - xs[3]}.'])


@t(U, 8)
def _(rng, nm):
    xs = sorted(R(rng, 20, 40) for _ in range(6)); out = R(rng, 90, 130); ys = sorted(xs + [out])
    m1, m2 = med(ys), med(xs)
    return (f'Data: {dl(ys)}. The value {out} is an outlier. By how much does the median change when the outlier is removed?',
            dz(abs(m1 - m2)), [f'Median with the outlier (4th of 7): {dz(m1)}.', f'Median without it (mean of the 3rd and 4th of 6): {dz(m2)}.', f'Change: {dz(abs(m1 - m2))}.'])


# ---------------------------------------------------------------- rewriting
SIG = lambda q: re.sub(r'\d+(?:\.\d+)?', '#', q['prompt']).strip()
NUM = re.compile(r'-?\d[\d,]*(?:\.\d+)?(?: \d+/\d+)?(?:/\d+)?')


def distractors(ans, steps, rng):
    """Three wrong options in the answer's own form, preferring intermediate values from the solution."""
    pair = re.fullmatch(r'\((-?\d+), (-?\d+)\)', ans)
    if pair:
        x, y = int(pair.group(1)), int(pair.group(2))
        pool = [f'({a}, {b})' for a, b in ((y, x), (-x, y), (x, -y), (-x, -y), (-y, -x))]
        return [p for p in dict.fromkeys(pool) if p != ans][:3]
    m_ = re.fullmatch(r'(\$?)(.*?)(%?)', ans); pre, core, suf = m_.groups()
    if 'x' in core:   # an expression like 7x + 12
        a, b = re.fullmatch(r'(\d+)x \+ (\d+)', core).groups(); a, b = int(a), int(b)
        return [f'{a}x + {b + 1 + i}' if i == 0 else f'{a + i}x + {b}' if i == 1 else f'{a - 1}x + {b}' for i in range(3)]
    def val(s):
        s = s.replace(',', '')
        mm = re.fullmatch(r'(-?)(\d+) (\d+)/(\d+)', s)
        return (int(mm.group(2)) + Fr(int(mm.group(3)), int(mm.group(4)))) * (-1 if mm.group(1) else 1) if mm else Fr(s)
    def fmt(v):
        if pre == '$':
            return m(v)
        if '.' in core:
            return dz(v, len(core.split('.')[1])) + suf
        return (mixed(v) if v.denominator > 1 else str(v.numerator)) + suf
    a = val(core); seen, out = {ans}, []
    for s in steps:
        for tok in NUM.findall(s.replace('−', '-')):
            try:
                v = val(tok)
            except (ValueError, ZeroDivisionError):
                continue
            o = fmt(v)
            if ((v > 0) == (a > 0) or a == 0) and v != 0 and o not in seen and v != a:
                seen.add(o); out.append(o)
    rng.shuffle(out)
    out = out[:3]
    k = 1
    while len(out) < 3:
        for v in (a + k, a - k, a * 2 if k == 1 else a + 10 * k):
            o = fmt(v)
            if len(out) < 3 and o not in seen and (v > 0 or a <= 0):
                seen.add(o); out.append(o)
        k += 1
    return out


def rewrite(q, fn, rng, nm, fam, note, used):
    used.discard(q['prompt'])
    for _ in range(60):
        prompt, ans, steps = (sup(x) if isinstance(x, str) else [sup(y) for y in x] for x in fn(rng, nm))
        if prompt not in used:
            break
    used.add(prompt)
    q['prompt'], q['answer'], q['solutionSteps'] = prompt, ans, steps
    for k in ('hint', 'diagram'):
        q.pop(k, None)
    if q['format'] == 'multiple-choice':
        opts = [ans] + distractors(ans, steps, rng); rng.shuffle(opts)
        q['options'] = [{'text': o, 'correct': o == ans} for o in opts]
    else:
        q.pop('options', None)
    q['sourceNotes'] = lib.SOURCE.format(fam=fam) + note


def pinned():
    """Ids that other audit scripts or tests rely on: never rewritten."""
    txt = ''.join(open(os.path.join(d, f), encoding='utf-8').read() for d, fs in ((lib.HERE, os.listdir(lib.HERE)), (os.path.join(lib.ROOT, 'scripts'), ['test-grade6-audit.cjs', 'test-grade6-c.cjs', 'test-grade6-plot.cjs']))
                  for f in fs if f.endswith(('.py', '.cjs')) and f not in ('levels.py', 'verify_levels.py') and os.path.isfile(os.path.join(d, f)))
    return set(re.findall(r'm6-[a-z]+-s\d\d-(?:cp1|cp2|honors)-\w+', txt))


def main():
    banks = lib.load()
    keep = pinned()
    NOTE9 = ' Rewritten in place: whole-site audit #9 (2026-11-20), {lv} item that reused a {low} template (was: “{old}”); keys rechecked by verify_levels.py.'
    done = {'cp1': 0, 'honors': 0}
    for u in lib.UNITS:
        qs = banks[u]['questions']
        for sid in sorted({q['skillId'] for q in qs}):
            n = int(sid.rsplit('-', 1)[1]); a = lib.ABBR[u]
            used = {q['prompt'] for q in qs}
            for lv, lows, fn, fam in (('cp1', ('cp2',), T.get((u, n)), f'g6_cp1_added_step_{a}_s{n:02d}'),
                                      ('honors', ('cp2', 'cp1'), H.T.get((u, n)), f'g6_honors_multistep_{a}_s{n:02d}')):
                if not fn:
                    continue
                low = {SIG(q) for q in qs if q['skillId'] == sid and q['level'] in lows and 'audit #9' not in q['sourceNotes']}
                cand = [q for q in qs if q['skillId'] == sid and q['level'] == lv and q['format'] in ('multiple-choice', 'short-answer')
                        and not q.get('diagram') and q['id'] not in keep and ('Grade 6 audit' not in q['sourceNotes'] or 'audit #9' in q['sourceNotes'])
                        and (SIG(q) in low or 'audit #9' in q['sourceNotes'])]
                cand.sort(key=lambda q: ('audit #9' not in q['sourceNotes'], q['id']))
                for i, q in enumerate(cand[:CAP]):
                    rng = random.Random(f'g6-a9-{q["id"]}')
                    old = re.search(r'\(was: “(.*?)”\)', q['sourceNotes'])
                    old = old.group(1) if old else re.sub(r'\s+', ' ', q['prompt'])[:70]
                    rewrite(q, fn, rng, N[(n * 5 + i * 3 + lib.UNITS.index(u)) % len(N)], fam,
                            NOTE9.format(lv='Standard' if lv == 'cp1' else 'Honors', low='Support' if lv == 'cp1' else 'lower-level', old=old.replace('“', '"').replace('”', '"')), used)
                    done[lv] += 1
    lib.save(banks)
    print('levels: rewrote', done['cp1'], 'Standard and', done['honors'], 'Honors items')


if __name__ == '__main__':
    main()
