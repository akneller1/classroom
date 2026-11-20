"""Grade 6 audit #4 (2026-11-19): CP2, CP1 and Honors really differ.
 * Honors: two new multi-step items in a real-world context for every one of the 53 skills (ids ...-honors-hNN).
   Each needs at least two connected steps; answers are numbers (or an ordered pair) so the practice test grades them.
 * CP2: a "First step:" hint from the item's own solution, unless that step already gives the answer away or the item is an
   error-analysis item (its first step names the mistake).
Idempotent: earlier h-items and hints are rebuilt. Keys are rechecked by verify_honors.py from the printed prompts."""
import math, os, random, re, sys
from collections import Counter
from fractions import Fraction as Fr
sys.path.insert(0, os.path.dirname(__file__))
import lib

N = ['Maya', 'Leo', 'Priya', 'Diego', 'Ana', 'Owen', 'Nia', 'Raj', 'Zoe', 'Sam', 'Lena', 'Kai', 'Iris', 'Theo', 'Rosa', 'Eli']
HE = {'Leo', 'Diego', 'Owen', 'Raj', 'Sam', 'Kai', 'Theo', 'Eli'}


def pr(n):
    return 'he' if n in HE else 'she'


def m(x):
    return f'${Fr(x).numerator / Fr(x).denominator:,.2f}'


def mixed(x):
    x = Fr(x)
    w, r = divmod(abs(x.numerator), x.denominator)
    s = '-' if x < 0 else ''
    return s + (str(w) if r == 0 else (f'{w} {r}/{x.denominator}' if w else f'{r}/{x.denominator}'))


def dz(x, p=2):
    v = Fr(x) * 10 ** p
    v = int(v + Fr(1, 2)) if v >= 0 else -int(-v + Fr(1, 2))
    return f'{v / 10 ** p:.{p}f}'.rstrip('0').rstrip('.')


R = lambda rng, a, b: rng.randint(a, b)
T = {}


def t(u, n):
    def deco(fn):
        T[(u, n)] = fn
        return fn
    return deco


# ---------------------------------------------------------------- Ratios, Rates, Percent, Proportions
U = 'ratios-rates-percent-proportions'


@t(U, 1)
def _(rng, nm):
    a, b = rng.choice([(5, 3), (7, 4), (4, 3), (9, 5), (3, 2)]); k = R(rng, 3, 8); T_ = (a + b) * k
    boys, girls = a * k, b * k
    return (f'In a club, the ratio of boys to girls is {a} : {b}. There are {T_} members. How many more girls would have to join for the numbers of boys and girls to be equal?',
            str(boys - girls), [f'Total parts: {a} + {b} = {a + b}; each part is {T_} ÷ {a + b} = {k} members.', f'Boys: {a} × {k} = {boys}; girls: {b} × {k} = {girls}.', f'{boys} − {girls} = {boys - girls} more girls.'])


@t(U, 2)
def _(rng, nm):
    q1, q2 = rng.choice([(3, 5), (4, 6), (2, 5), (3, 4)]); u1, u2 = Fr(R(rng, 230, 320), 100), Fr(R(rng, 230, 320), 100)
    while u1 == u2:
        u2 = Fr(R(rng, 230, 320), 100)
    p1, p2 = u1 * q1, u2 * q2; n = 12 * rng.choice([1, 2])
    cheap = min(u1, u2)
    return (f'Store A sells {q1} pounds of apples for {m(p1)}. Store B sells {q2} pounds for {m(p2)}. {nm} needs {n} pounds. How much does {pr(nm)} save by buying them all at the store with the lower unit price?',
            m(abs(u1 - u2) * n), [f'Store A: {m(p1)} ÷ {q1} = {m(u1)} per pound. Store B: {m(p2)} ÷ {q2} = {m(u2)} per pound.', f'{n} pounds cost {m(u1 * n)} at A and {m(u2 * n)} at B.',
                                  f'Savings: {m(abs(u1 - u2) * n)}.'])


@t(U, 3)
def _(rng, nm):
    a, b = rng.choice([(2, 3), (3, 5), (4, 5), (3, 4)]); k = R(rng, 3, 9); J = a * k
    return (f'A punch recipe mixes {a} cups of juice with {b} cups of sparkling water. {nm} has {J} cups of juice and uses it all, keeping the same ratio. How many cups of punch does {pr(nm)} make?',
            str(J + b * k), [f'Scale factor: {J} ÷ {a} = {k}.', f'Sparkling water: {b} × {k} = {b * k} cups.', f'Punch: {J} + {b * k} = {J + b * k} cups.'])


@t(U, 4)
def _(rng, nm):
    a1, w1 = rng.choice([(2, 3), (3, 4), (2, 5), (3, 5)]); w2 = w1 * R(rng, 2, 4); a2 = a1 * w2 // w1 - R(rng, 1, 3)
    need = Fr(a1 * w2, w1) - a2
    return (f'Mix A uses {a1} cups of blue paint for every {w1} cups of white. Mix B has {a2} cups of blue and {w2} cups of white. How many cups of blue paint must be added to Mix B so it is the same shade as Mix A?',
            mixed(need), [f'Mix A: {Fr(a1, w1)} cup of blue per cup of white.', f'For {w2} cups of white, Mix A uses {w2} × {a1}/{w1} = {mixed(Fr(a1 * w2, w1))} cups of blue.', f'Add {mixed(Fr(a1 * w2, w1))} − {a2} = {mixed(need)} cups.'])


@t(U, 5)
def _(rng, nm):
    k = rng.choice([5, 10, 20]); c1, c2 = R(rng, 3, 9), R(rng, 3, 9); s = rng.choice([40, 50, 60])
    dist = (c1 + c2) * k
    return (f'On a map, 1 cm represents {k} km. A road goes {c1} cm from Ashby to Bell and then {c2} cm from Bell to Carver. A bus averages {s} km per hour. How many hours does the trip from Ashby to Carver take?',
            mixed(Fr(dist, s)), [f'Map distance: {c1} + {c2} = {c1 + c2} cm.', f'Actual distance: {c1 + c2} × {k} = {dist} km.', f'Time: {dist} ÷ {s} = {mixed(Fr(dist, s))} hours.'])


@t(U, 6)
def _(rng, nm):
    T_ = 20 * R(rng, 20, 40); p = rng.choice([25, 40, 45, 60]); q = rng.choice([25, 50, 75])
    bus = T_ * p // 100; rest = T_ - bus
    while (T_ * p) % 100 or (rest * q) % 100:   # keep every count whole
        T_ += 20; bus = T_ * p // 100; rest = T_ - bus
    return (f'A school has {T_} students. {p}% ride the bus. Of the students who do not ride the bus, {q}% walk. How many students walk?',
            str(rest * q // 100), [f'Bus riders: {p}% of {T_} = {bus}.', f'Not on the bus: {T_} − {bus} = {rest}.', f'Walkers: {q}% of {rest} = {rest * q // 100}.'])


@t(U, 7)
def _(rng, nm):
    g1, g2 = rng.choice([(12, 8), (15, 5), (14, 6), (16, 24)]); w1 = R(rng, 3, g1 - 1); w2 = rng.choice([x for x in range(1, g2) if Fr((w1 + x) * 100, g1 + g2).denominator == 1] or [g2 // 2])
    pc = Fr((w1 + w2) * 100, g1 + g2)
    return (f'A team won {w1} of its first {g1} games and {w2} of its last {g2} games. What percent of all its games did the team win?',
            f'{dz(pc, 1)}%', [f'Games won: {w1} + {w2} = {w1 + w2}. Games played: {g1} + {g2} = {g1 + g2}.', f'{w1 + w2}/{g1 + g2} = {dz(Fr(w1 + w2, g1 + g2), 3)}.', f'{dz(pc, 1)}%.'])


@t(U, 8)
def _(rng, nm):
    c = rng.choice([Fr(3, 2), Fr(5, 2), 3, 2]); b = rng.choice([4, 6, 8]); tot = c * b
    return (f'A soup recipe uses {mixed(c)} cups of broth per batch. {nm} makes {b} batches. How many quarts of broth is that? (1 quart = 4 cups)',
            mixed(tot / 4), [f'Broth: {mixed(c)} × {b} = {mixed(tot)} cups.', f'Quarts: {mixed(tot)} ÷ 4 = {mixed(tot / 4)}.'])


# ---------------------------------------------------------------- Fractions and Decimals
U = 'fractions-decimals-operations'


@t(U, 1)
def _(rng, nm):
    q = rng.choice([Fr(1, 8), Fr(1, 6), Fr(1, 4), Fr(1, 10)]); n = R(rng, 4, 9); p = q * n
    return (f'A walking path is {mixed(p)} mile long. A marker stands at the start and then every {q} mile, including the end. How many markers are there?',
            str(n + 1), [f'Spaces between markers: {mixed(p)} ÷ {q} = {n}.', f'Markers: {n} spaces + 1 marker at the start = {n + 1}.'])


@t(U, 2)
def _(rng, nm):
    f = rng.choice([Fr(3, 4), Fr(2, 3), Fr(1, 2), Fr(3, 8)]); L = R(rng, 3, 6); extra = R(rng, 4, 10); n = f * (L + extra)
    while n.denominator != 1:
        extra += 1; n = f * (L + extra)
    return (f'A bakery has {n} cups of flour. Each loaf uses {f} cup. After baking {L} loaves for one order, how many more loaves can the bakery make with the flour that is left?',
            str(extra), [f'Flour used: {L} × {f} = {mixed(L * f)} cups.', f'Left: {n} − {mixed(L * f)} = {mixed(n - L * f)} cups.', f'Loaves: {mixed(n - L * f)} ÷ {f} = {extra}.'])


@t(U, 3)
def _(rng, nm):
    a, b = rng.choice([(Fr(15, 2), Fr(5, 4)), (Fr(33, 4), Fr(3, 2)), (Fr(21, 2), Fr(7, 4)), (Fr(29, 4), Fr(3, 2))])
    full = int(a // b); left = a - full * b
    return (f'A board is {mixed(a)} feet long. {nm} cuts as many {mixed(b)}-foot shelves from it as possible. How many feet of board are left over?',
            mixed(left), [f'{mixed(a)} ÷ {mixed(b)} = {mixed(a / b)}, so {full} full shelves.', f'Used: {full} × {mixed(b)} = {mixed(full * b)} feet.', f'Left over: {mixed(a)} − {mixed(full * b)} = {mixed(left)} feet.'])


@t(U, 4)
def _(rng, nm):
    s = R(rng, 300, 900); cap = rng.choice([44, 48, 52]); c = rng.choice([325, 350, 410])
    buses = -(-s // cap)
    return (f'{s} students are going on a field trip. Each bus holds {cap} students and costs ${c} to rent. What is the total cost of the buses?',
            f'${buses * c:,}', [f'{s} ÷ {cap} = {s // cap} R{s % cap}, so {buses} buses are needed.', f'Cost: {buses} × ${c} = ${buses * c:,}.'])


@t(U, 5)
def _(rng, nm):
    xs = [Fr(R(rng, 150, 1999), 100) for _ in range(3)]; bill = 50 if sum(xs) < 50 else 100
    return (f'{nm} buys a book for {m(xs[0])}, a game for {m(xs[1])} and a snack for {m(xs[2])}, and pays with a ${bill} bill. How much change does {pr(nm)} get?',
            m(bill - sum(xs)), [f'Total: {m(xs[0])} + {m(xs[1])} + {m(xs[2])} = {m(sum(xs))}.', f'Change: ${bill}.00 − {m(sum(xs))} = {m(bill - sum(xs))}.'])


@t(U, 6)
def _(rng, nm):
    p = Fr(R(rng, 289, 389), 100); mpg = rng.choice([25, 28, 30, 32]); M = mpg * R(rng, 6, 15)
    gal = Fr(M, mpg)
    return (f'Gas costs {m(p)} per gallon. A car goes {mpg} miles per gallon. How much does the gas cost for a {M}-mile trip? Round to the nearest cent.',
            m(Fr(round(p * gal * 100), 100)), [f'Gallons: {M} ÷ {mpg} = {mixed(gal)}.', f'Cost: {mixed(gal)} × {m(p)} = {m(p * gal)}.'])


@t(U, 7)
def _(rng, nm):
    a, b = rng.choice([(10, 8), (8, 6), (12, 8), (6, 4)]); pa, pb = Fr(R(rng, 299, 599), 100), Fr(R(rng, 199, 399), 100)
    L = a * b // math.gcd(a, b)
    return (f'Hot dogs come in packs of {a} for {m(pa)}. Buns come in packs of {b} for {m(pb)}. {nm} buys the fewest packs that give the same number of hot dogs and buns. How much does {pr(nm)} spend?',
            m(L // a * pa + L // b * pb), [f'LCM of {a} and {b}: {L}.', f'{L // a} packs of hot dogs and {L // b} packs of buns.', f'Cost: {L // a} × {m(pa)} + {L // b} × {m(pb)} = {m(L // a * pa + L // b * pb)}.'])


@t(U, 8)
def _(rng, nm):
    n = R(rng, 4, 9); x, y = Fr(R(rng, 899, 1499), 100), Fr(R(rng, 401, 899), 100)
    return (f'{nm} buys {n} T-shirts at {m(x)} each and {n} hats at {m(y)} each. Use the Distributive Property to find the total cost.',
            m(n * (x + y)), [f'{n} × {m(x)} + {n} × {m(y)} = {n}({m(x)} + {m(y)}).', f'{n} × {m(x + y)} = {m(n * (x + y))}.'])


# ---------------------------------------------------------------- Rational Numbers
U = 'rational-numbers'


@t(U, 1)
def _(rng, nm):
    a, b, c = R(rng, 20, 60), R(rng, 5, 15), R(rng, 8, 25)
    return (f'A diver is {a} m below sea level. She rises {b} m and then dives down {c} m. What integer gives her final position relative to sea level?',
            str(-a + b - c), [f'Start: −{a}.', f'Rise {b}: −{a} + {b} = {-a + b}.', f'Dive {c}: {-a + b} − {c} = {-a + b - c}.'])


@t(U, 2)
def _(rng, nm):
    lo, hi, d = R(rng, 3, 15), R(rng, 2, 20), R(rng, 3, 9)
    return (f'At 6 a.m. the temperature was −{lo}°F. By noon it was {hi}°F, and by night it fell {d} degrees from the noon temperature. How many degrees warmer was the night temperature than the 6 a.m. temperature?',
            str(hi - d + lo), [f'Night: {hi} − {d} = {hi - d}°F.', f'From −{lo} to {hi - d}: {hi - d} − (−{lo}) = {hi - d + lo} degrees.'])


@t(U, 3)
def _(rng, nm):
    vals = rng.sample([-14, -9, -6, -3, -1, 2, 5, 8, 11], 4)
    return (f'The low temperatures for four days were {", ".join(f"{v}°C" for v in vals)}. How many degrees warmer was the warmest day than the coldest day?',
            str(max(vals) - min(vals)), [f'Order: {", ".join(str(v) for v in sorted(vals))}.', f'Warmest {max(vals)}, coldest {min(vals)}.', f'{max(vals)} − ({min(vals)}) = {max(vals) - min(vals)}.'])


@t(U, 4)
def _(rng, nm):
    a, b = -R(rng, 10, 40), R(rng, 5, 30)
    return (f"{nm}'s account balance is ${a} and Ben's is ${b}. What is the least whole number of dollars {nm} must deposit so that {pr(nm)} has more money than Ben?",
            str(b - a + 1), [f'{nm} needs a balance greater than {b}: {a} + d > {b}.', f'd > {b} − ({a}) = {b - a}.', f'The least whole number is {b - a + 1}.'])


@t(U, 5)
def _(rng, nm):
    a, b = R(rng, 30, 90), R(rng, 100, 300)
    return (f'A submarine is at −{b} m and a fish is at −{a} m. How many meters apart are they? Use absolute value.',
            str(b - a), [f'|−{b}| = {b} and |−{a}| = {a}.', f'Both are below sea level, so the distance is {b} − {a} = {b - a} m.'])


@t(U, 6)
def _(rng, nm):
    a, b, c = R(rng, 20, 60), R(rng, 20, 60), R(rng, 10, 30)
    return (f'{nm} owes $' + f'{a} (balance −${a}) and Ben owes ${b} (balance −${b}). {nm} then borrows ${c} more. How much more does the person who now owes more owe than the other?',
            str(abs(a + c - b)), [f"{nm}'s balance: −{a} − {c} = −{a + c}.", f'Debts: ${a + c} and ${b}.', f'Difference: |{a + c} − {b}| = {abs(a + c - b)}.'])


@t(U, 7)
def _(rng, nm):
    x, y = rng.choice([-1, 1]) * R(rng, 2, 9), rng.choice([-1, 1]) * R(rng, 2, 9)
    return (f'Point P({x}, {y}) is reflected across the x-axis to point Q. How far apart are P and Q?',
            str(2 * abs(y)), [f'Reflecting across the x-axis keeps x and changes the sign of y: Q({x}, {-y}).', f'P and Q have the same x-coordinate, so the distance is |{y} − ({-y})| = {2 * abs(y)}.'])


@t(U, 8)
def _(rng, nm):
    x, y, l, d = R(rng, -5, 5), R(rng, -5, 5), R(rng, 2, 8), R(rng, 2, 8)
    return (f'A robot starts at ({x}, {y}). It moves {l} units left and then {d} units down. What are its new coordinates?',
            f'({x - l}, {y - d})', [f'Left {l}: x = {x} − {l} = {x - l}.', f'Down {d}: y = {y} − {d} = {y - d}.', f'({x - l}, {y - d}).'])


@t(U, 9)
def _(rng, nm):
    a, b, c, d = R(rng, -6, -1), R(rng, -5, 0), R(rng, 1, 6), R(rng, 1, 7)
    return (f'{nm} walks from ({a}, {b}) to ({a}, {c}) and then to ({d}, {c}). Each unit is 1 block. How many blocks does {pr(nm)} walk?',
            str((c - b) + (d - a)), [f'First leg (same x): |{c} − ({b})| = {c - b} blocks.', f'Second leg (same y): |{d} − ({a})| = {d - a} blocks.', f'Total: {c - b} + {d - a} = {c - b + d - a} blocks.'])


# ---------------------------------------------------------------- Expressions and Equations
U = 'expressions-equations'


@t(U, 1)
def _(rng, nm):
    n, h = rng.choice([25, 40, 50, 75]), R(rng, 3, 6)
    return (f'A colony of bacteria starts with {n} cells and doubles every hour. Write the number of cells after {h} hours as {n} × 2^{h} and evaluate it.',
            f'{n * 2 ** h:,}', [f'2^{h} = {2 ** h}.', f'{n} × {2 ** h} = {n * 2 ** h:,} cells.'])


@t(U, 2)
def _(rng, nm):
    a, b, c, d, g = R(rng, 20, 35), R(rng, 3, 8), R(rng, 40, 60), R(rng, 1, 3), R(rng, 5, 12)
    pa, pb = a + b * g, c + d * g
    return (f'Plan A costs {a} + {b}g dollars and Plan B costs {c} + {d}g dollars for g gigabytes of data. How much less does the cheaper plan cost for {g} gigabytes?',
            str(abs(pa - pb)), [f'Plan A: {a} + {b} × {g} = {pa}.', f'Plan B: {c} + {d} × {g} = {pb}.', f'Difference: {abs(pa - pb)} dollars.'])


@t(U, 3)
def _(rng, nm):
    p, k, g, s = R(rng, 3, 5), rng.choice([10, 12]), R(rng, 2, 6), 4
    while (p * k - g) % s:
        g += 1
    return (f'{nm} buys {p} boxes of {k} markers, gives away {g} markers, and shares the rest equally among {s} friends. Evaluate ({p} × {k} − {g}) ÷ {s} to find how many each friend gets.',
            str((p * k - g) // s), [f'{p} × {k} = {p * k}.', f'{p * k} − {g} = {p * k - g}.', f'{p * k - g} ÷ {s} = {(p * k - g) // s}.'])


@t(U, 4)
def _(rng, nm):
    a, b, c, x = R(rng, 2, 6), R(rng, 2, 9), R(rng, 2, 9), R(rng, 3, 9)
    return (f'Two rectangular gardens are each {a} m wide. One is (x + {b}) m long and the other is (x + {c}) m long. Write the total area as one expression without parentheses, then find it when x = {x}.',
            str(a * (2 * x + b + c)), [f'{a}(x + {b}) + {a}(x + {c}) = {2 * a}x + {a * (b + c)}.', f'When x = {x}: {2 * a} × {x} + {a * (b + c)} = {a * (2 * x + b + c)} m².'])


@t(U, 5)
def _(rng, nm):
    c, p, x = R(rng, 10, 30), R(rng, 3, 9), R(rng, 4, 12); tot = c + p * x
    opts = sorted({x - 2, x, x + 1, x + 3})
    return (f'A gym charges a ${c} sign-up fee plus ${p} per class. {nm} paid ${tot} in all. Which of these numbers of classes, {", ".join(map(str, opts))}, is a solution of {c} + {p}n = {tot}?',
            str(x), [f'Try n = {x}: {c} + {p} × {x} = {tot}. ✓', 'The other values give different totals.'])


@t(U, 6)
def _(rng, nm):
    a, b, p, k = R(rng, 6, 15), R(rng, 5, 20), R(rng, 6, 14), 3
    c = a + b + k * p
    return (f'{nm} had ${c}. {pr(nm).capitalize()} spent ${a} on lunch and bought {k} books that each cost the same amount. Now {pr(nm)} has ${b}. Write and solve an equation to find the price of one book.',
            str(p), [f'Money spent on books: {c} − {a} − {b} = {c - a - b}.', f'{k}p = {c - a - b}.', f'p = {c - a - b} ÷ {k} = {p} dollars.'])


@t(U, 7)
def _(rng, nm):
    f, r, h = R(rng, 20, 50), R(rng, 15, 35), R(rng, 3, 8)
    return (f'A plumber charges c = {f} + {r}h dollars for h hours. h is the independent variable. How much more does a {h + 2}-hour job cost than a {h}-hour job?',
            str(2 * r), [f'c({h + 2}) = {f} + {r} × {h + 2} = {f + r * (h + 2)}.', f'c({h}) = {f} + {r} × {h} = {f + r * h}.', f'Difference: {2 * r} dollars (2 more hours × {r}).'])


# ---------------------------------------------------------------- Inequalities
U = 'inequalities'


@t(U, 1)
def _(rng, nm):
    cap, ppl, w, box = rng.choice([1500, 2000, 2500]), R(rng, 4, 8), R(rng, 140, 180), rng.choice([40, 50, 60])
    left = cap - ppl * w
    return (f'An elevator can carry at most {cap:,} pounds. {ppl} people with a total weight of {ppl * w:,} pounds get on. What is the greatest number of {box}-pound boxes that can also be loaded?',
            str(left // box), [f'{ppl * w} + {box}b ≤ {cap}.', f'{box}b ≤ {left}, so b ≤ {mixed(Fr(left, box))}.', f'The greatest whole number is {left // box}.'])


@t(U, 2)
def _(rng, nm):
    goal, have, rate = R(rng, 200, 400), R(rng, 20, 80), rng.choice([9, 11, 12, 13])
    return (f'{nm} wants at least ${goal} for a bike. {pr(nm).capitalize()} has ${have} and earns ${rate} per hour. What is the least whole number of hours {pr(nm)} must work?',
            str(-(-(goal - have) // rate)), [f'{have} + {rate}h ≥ {goal}.', f'{rate}h ≥ {goal - have}, so h ≥ {mixed(Fr(goal - have, rate))}.', f'Least whole number: {-(-(goal - have) // rate)} hours.'])


@t(U, 3)
def _(rng, nm):
    a, b, c = R(rng, 2, 5), R(rng, 1, 9), R(rng, 20, 40)
    sol = [x for x in range(1, 21) if a * x + b > c]
    return (f'How many whole numbers from 1 to 20 are solutions of {a}x + {b} > {c}?',
            str(len(sol)), [f'{a}x > {c - b}, so x > {mixed(Fr(c - b, a))}.', f'The whole numbers from {sol[0]} to 20 work.', f'Count: {len(sol)}.'])


@t(U, 4)
def _(rng, nm):
    a, b = R(rng, 2, 9), R(rng, 3, 12)
    return (f'A freezer must stay at a temperature t (°C) with −{a} < t ≤ {b}. How many whole-number temperatures are allowed?',
            str(b + a), [f'The allowed integers go from −{a - 1} up to {b}.', f'Count: {b} − (−{a - 1}) + 1 = {b + a}.'])


@t(U, 5)
def _(rng, nm):
    tk, fee, bud = R(rng, 8, 15), R(rng, 5, 12), R(rng, 90, 160)
    return (f'Concert tickets cost ${tk} each, plus one ${fee} service fee for the whole order. {nm} can spend at most ${bud}. What is the greatest number of tickets {pr(nm)} can buy?',
            str((bud - fee) // tk), [f'{tk}x + {fee} ≤ {bud}.', f'{tk}x ≤ {bud - fee}, so x ≤ {mixed(Fr(bud - fee, tk))}.', f'Greatest whole number: {(bud - fee) // tk}.'])


# ---------------------------------------------------------------- Geometry
U = 'geometry'


@t(U, 1)
def _(rng, nm):
    a, b, h, c = R(rng, 10, 20), R(rng, 22, 36), R(rng, 8, 16), rng.choice([50, 60, 80])
    A = Fr((a + b) * h, 2)
    return (f'A garden is a trapezoid with parallel sides {a} ft and {b} ft and height {h} ft. One bag of seed covers {c} square feet. How many bags are needed?',
            str(-(-A.numerator // (A.denominator * c))), [f'Area: ½ × ({a} + {b}) × {h} = {mixed(A)} ft².', f'{mixed(A)} ÷ {c} = {mixed(A / c)}.', f'Round up: {-(-A.numerator // (A.denominator * c))} bags.'])


@t(U, 2)
def _(rng, nm):
    a, b, p = R(rng, 6, 14), R(rng, 8, 20), Fr(R(rng, 150, 450), 100)
    return (f'A sail is a right triangle with legs {a} ft and {b} ft. The fabric costs {m(p)} per square foot. How much does the fabric for 2 sails cost?',
            m(a * b * p), [f'One sail: ½ × {a} × {b} = {mixed(Fr(a * b, 2))} ft².', f'Two sails: {a * b} ft².', f'Cost: {a * b} × {m(p)} = {m(a * b * p)}.'])


@t(U, 3)
def _(rng, nm):
    b, h, n = R(rng, 10, 24), R(rng, 8, 18), rng.choice([12, 15, 20])
    return (f'A class makes {n} triangular flags, each with a base of {b} in. and a height of {h} in. How many square inches of fabric do the flags use?',
            f'{n * b * h // 2:,}' if (n * b * h) % 2 == 0 else mixed(Fr(n * b * h, 2)), [f'One flag: ½ × {b} × {h} = {mixed(Fr(b * h, 2))} in².', f'{n} flags: {n} × {mixed(Fr(b * h, 2))} = {mixed(Fr(n * b * h, 2))} in².'])


@t(U, 4)
def _(rng, nm):
    L, W, l, w = R(rng, 18, 26), R(rng, 14, 20), R(rng, 5, 9), R(rng, 4, 8); p = Fr(R(rng, 250, 550), 100)
    A = L * W - l * w
    return (f'A room is an L shape: a {L} ft by {W} ft rectangle with a {l} ft by {w} ft corner cut out. Carpet costs {m(p)} per square foot. How much does carpet for the room cost?',
            m(A * p), [f'Area: {L} × {W} − {l} × {w} = {L * W} − {l * w} = {A} ft².', f'Cost: {A} × {m(p)} = {m(A * p)}.'])


@t(U, 5)
def _(rng, nm):
    l, w, h = Fr(R(rng, 9, 15) * 2 + 1, 2), R(rng, 6, 10), R(rng, 8, 12)
    V = l * w * h
    return (f'A fish tank is {mixed(l)} in. long, {w} in. wide and {h} in. tall. It is filled with water to 3/4 of its height. How many cubic inches of water are in the tank?',
            mixed(V * Fr(3, 4)), [f'Water height: 3/4 × {h} = {mixed(Fr(3 * h, 4))} in.', f'Volume: {mixed(l)} × {w} × {mixed(Fr(3 * h, 4))} = {mixed(V * Fr(3, 4))} in³.'])


@t(U, 6)
def _(rng, nm):
    x1, y1, x2, y2 = -R(rng, 2, 9), -R(rng, 2, 9), R(rng, 2, 9), R(rng, 2, 9); c = rng.choice([4, 6, 8])
    P = 2 * ((x2 - x1) + (y2 - y1))
    return (f'A park on a map has corners ({x1}, {y1}), ({x2}, {y1}), ({x2}, {y2}) and ({x1}, {y2}). Each unit is 10 m. Fencing costs ${c} per meter. How much does fencing the park cost?',
            f'${P * 10 * c:,}', [f'Side lengths: {x2 - x1} and {y2 - y1} units.', f'Perimeter: 2({x2 - x1} + {y2 - y1}) = {P} units = {P * 10} m.', f'Cost: {P * 10} × ${c} = ${P * 10 * c:,}.'])


@t(U, 7)
def _(rng, nm):
    a, b, c, d = R(rng, 2, 6), R(rng, 3, 7), R(rng, 2, 5), R(rng, 2, 6)
    return (f'Rectangle 1 has corners (0, 0), ({a}, 0), ({a}, {b}) and (0, {b}). Rectangle 2 has corners ({a}, 0), ({a + c}, 0), ({a + c}, {d}) and ({a}, {d}). What is the total area of the two rectangles in square units?',
            str(a * b + c * d), [f'Rectangle 1: {a} × {b} = {a * b}.', f'Rectangle 2: {c} × {d} = {c * d}.', f'Total: {a * b + c * d} square units.'])


@t(U, 8)
def _(rng, nm):
    l, w, h, cov = R(rng, 8, 16), R(rng, 5, 10), R(rng, 4, 9), rng.choice([60, 80, 100])
    S = 2 * (l * w + l * h + w * h)
    return (f'{nm} paints every face of a box {l} in. long, {w} in. wide and {h} in. tall. One bottle of paint covers {cov} square inches. How many bottles does {pr(nm)} need?',
            str(-(-S // cov)), [f'Surface area: 2({l}×{w} + {l}×{h} + {w}×{h}) = {S} in².', f'{S} ÷ {cov} = {mixed(Fr(S, cov))}.', f'Round up: {-(-S // cov)} bottles.'])


# ---------------------------------------------------------------- Data Displays
U = 'data-displays'


def dl(xs):
    return ', '.join(str(x) for x in xs)


@t(U, 1)
def _(rng, nm):
    xs = [R(rng, 2, 12) for _ in range(5)]; new = R(rng, 1, 15)
    while (sum(xs) + new) % 6:
        new += 1
    return (f'To answer "How many hours do students in our class read each week?", {nm} collected 5 responses: {dl(xs)}. One more student answered {new}. What is the mean of all 6 responses?',
            str((sum(xs) + new) // 6), [f'Sum of the first 5: {sum(xs)}.', f'Add {new}: {sum(xs) + new}.', f'Mean: {sum(xs) + new} ÷ 6 = {(sum(xs) + new) // 6}.'])


@t(U, 2)
def _(rng, nm):
    mn = R(rng, 20, 40); q1 = mn + R(rng, 5, 15); md = q1 + R(rng, 3, 12); q3 = md + R(rng, 3, 12); mx = q3 + R(rng, 5, 20)
    return (f'A box plot of test scores has minimum {mn}, lower quartile {q1}, median {md}, upper quartile {q3} and maximum {mx}. How much greater is the range than the interquartile range?',
            str((mx - mn) - (q3 - q1)), [f'Range: {mx} − {mn} = {mx - mn}.', f'IQR: {q3} − {q1} = {q3 - q1}.', f'Difference: {mx - mn - q3 + q1}.'])


@t(U, 3)
def _(rng, nm):
    xs = [R(rng, 70, 98) for _ in range(4)] + [R(rng, 40, 60)]
    while (sum(xs) - min(xs)) % 4:
        xs[0] += 1
    return (f"{nm}'s five test scores are {dl(xs)}. The teacher drops the lowest score. What is {nm}'s new mean?",
            str((sum(xs) - min(xs)) // 4), [f'Lowest score: {min(xs)}.', f'Sum of the other four: {sum(xs) - min(xs)}.', f'New mean: {sum(xs) - min(xs)} ÷ 4 = {(sum(xs) - min(xs)) // 4}.'])


@t(U, 4)
def _(rng, nm):
    xs = sorted(R(rng, 10, 60) for _ in range(8))
    lo, hi = xs[:4], xs[4:]
    q1, q3 = Fr(lo[1] + lo[2], 2), Fr(hi[1] + hi[2], 2)
    return (f'Data: {dl(xs)}. How much greater is the range than the interquartile range?',
            mixed((xs[-1] - xs[0]) - (q3 - q1)), [f'Range: {xs[-1]} − {xs[0]} = {xs[-1] - xs[0]}.', f'Q1 = {mixed(q1)}, Q3 = {mixed(q3)}, IQR = {mixed(q3 - q1)}.', f'Difference: {mixed((xs[-1] - xs[0]) - (q3 - q1))}.'])


@t(U, 5)
def _(rng, nm):
    base = rng.choice([[2, 4, 6, 8, 10], [1, 3, 5, 7, 9], [3, 4, 5, 6, 7]]); s = R(rng, 10, 40)
    other = [s + x * 2 - 5 for x in base]
    ma = Fr(sum(abs(x - Fr(sum(base), 5)) for x in base), 5); mb = Fr(sum(abs(x - Fr(sum(other), 5)) for x in other), 5)
    A = [x + s for x in base]
    return (f'Class A scored {dl(A)} and Class B scored {dl(other)} on a quiz. How much greater is the mean absolute deviation of Class B than of Class A?',
            dz(mb - ma, 2), [f'Mean of A: {mixed(Fr(sum(A), 5))}; MAD of A: {dz(ma, 2)}.', f'Mean of B: {mixed(Fr(sum(other), 5))}; MAD of B: {dz(mb, 2)}.', f'Difference: {dz(mb - ma, 2)}.'])


@t(U, 6)
def _(rng, nm):
    A = sorted(R(rng, 20, 50) for _ in range(7)); B = sorted(R(rng, 30, 60) for _ in range(7))
    return (f'Points scored by two teams in 7 games. Team A: {dl(A)}. Team B: {dl(B)}. How much greater is the larger median than the smaller median?',
            str(abs(B[3] - A[3])), [f'Median of A (4th value): {A[3]}.', f'Median of B: {B[3]}.', f'Difference: {abs(B[3] - A[3])}.'])


@t(U, 7)
def _(rng, nm):
    xs = sorted([R(rng, 2, 6) for _ in range(6)] + [R(rng, 20, 30)])
    mean = Fr(sum(xs), 7)
    return (f'The number of pets owned by 7 families is {dl(xs)}. The data are skewed right. How much greater is the mean than the median? Round to the nearest tenth.',
            dz(mean - xs[3], 1), [f'Mean: {sum(xs)} ÷ 7 = {dz(mean, 2)}.', f'Median: {xs[3]}.', f'Difference: {dz(mean - xs[3], 1)}.'])


@t(U, 8)
def _(rng, nm):
    xs = [R(rng, 20, 30) for _ in range(7)]; out = R(rng, 80, 110)
    while (sum(xs) + out) % 8 or sum(xs) % 7:
        xs[0] += 1
    return (f'Data: {dl(xs + [out])}. The value {out} is an outlier. By how much does the mean decrease when the outlier is removed?',
            str((sum(xs) + out) // 8 - sum(xs) // 7), [f'Mean with the outlier: {sum(xs) + out} ÷ 8 = {(sum(xs) + out) // 8}.', f'Mean without it: {sum(xs)} ÷ 7 = {sum(xs) // 7}.', f'Decrease: {(sum(xs) + out) // 8 - sum(xs) // 7}.'])


def sup(s):
    return re.sub(r'\^(\d+)', lambda mm: mm.group(1).translate(str.maketrans('0123456789', '⁰¹²³⁴⁵⁶⁷⁸⁹')), s)


def hint_for(q):
    st = q.get('solutionSteps') or []
    if q['level'] != 'cp2' or len(st) < 2 or q['format'] in ('open-response', 'select-all', 'plot') or 'answered this problem incorrectly' in q['prompt']:
        return None
    s0 = st[0].strip()
    ans = str(q.get('answer', ''))
    nums = re.findall(r'-?\d+(?:\.\d+)?', ans)
    if ans and (ans in s0 or (nums and any(re.search(r'(?<![\d.])' + re.escape(n) + r'(?![\d.])', s0) for n in nums[:1]) and '=' in s0 and s0.rstrip('.').endswith(nums[0]))):
        return None
    if re.search(r'grouping symbols', s0, re.I) and not re.search(r'[(\[]', q['prompt']):
        return None
    if len(s0) > 160 or s0.lower().startswith(('answer', 'the answer', 'mistake')):
        return None
    return 'First step: ' + s0


def main():
    banks, tags = lib.load(), lib.load_tags()
    HID = re.compile(r'-honors-h\d{2}$')
    for u in lib.UNITS:
        banks[u]['questions'] = [q for q in banks[u]['questions'] if not HID.search(q['id'])]
        tags[u] = {k: v for k, v in tags[u].items() if not HID.search(k)}
    made = 0
    for (u, n), fn in sorted(T.items(), key=lambda kv: (lib.UNITS.index(kv[0][0]), kv[0][1])):
        sid = f'{u}-skill-{n:02d}'
        std = list(Counter(tuple(q['standards']) for q in banks[u]['questions'] if q['skillId'] == sid and q['level'] == 'honors').most_common(1)[0][0])
        rng = random.Random(f'g6-honors-{sid}')
        qs = banks[u]['questions']
        last = max(i for i, x in enumerate(qs) if x['skillId'] == sid and x['level'] == 'honors')
        seen = set()
        for k in range(2):
            for _ in range(40):
                prompt, ans, steps = (sup(x) if isinstance(x, str) else [sup(y) for y in x] for x in fn(rng, N[(n * 3 + k * 7 + lib.UNITS.index(u)) % len(N)]))
                if prompt not in seen:
                    break
            seen.add(prompt)
            qid = f'm6-{lib.ABBR[u]}-s{n:02d}-honors-h{k + 1:02d}'
            q = dict(id=qid, skillId=sid, level='honors', format='short-answer', prompt=prompt, answer=ans, solutionSteps=steps, standards=std,
                     sourceNotes=lib.SOURCE.format(fam=f'g6_honors_multistep_{lib.ABBR[u]}_s{n:02d}') + ' Teacher review pending.')
            qs.insert(last + 1 + k, q)
            tags[u][qid] = ['multistep', 'connections']
            made += 1
    hints = 0
    for u, q in lib.items(banks):
        h = hint_for(q)
        if h:
            q['hint'] = h
            hints += 1
        else:
            q.pop('hint', None)
    lib.save(banks)
    lib.save_tags(tags)
    print('honors multi-step items:', made, '; CP2 hints:', hints)


if __name__ == '__main__':
    main()
