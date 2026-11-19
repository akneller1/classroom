"""Grade 7 audit #3 (2026-11-19): Remedial, Standard and Advanced really differ.
 * Advanced (Honors): two new multi-step items in a real-world context for every one of the 114 skills
   (ids ...-honors-hNN). Each needs at least two connected steps; answers are numbers so the practice test grades them.
 * Remedial (CP2): a "First step:" hint from the item's own solution, unless that step already gives the answer away
   or the item is an error-analysis item (its first step names the mistake).
Idempotent: earlier h-items and hints are rebuilt."""
import math, os, random, re, sys
from fractions import Fraction as Fr
sys.path.insert(0, os.path.dirname(__file__))
import lib

N = ['Maya', 'Leo', 'Priya', 'Diego', 'Ana', 'Owen', 'Nia', 'Raj', 'Zoe', 'Sam', 'Lena', 'Kai', 'Iris', 'Theo', 'Rosa', 'Eli']
HE = {'Leo': 'he', 'Diego': 'he', 'Owen': 'he', 'Raj': 'he', 'Sam': 'he', 'Kai': 'he', 'Theo': 'he', 'Eli': 'he'}


def pr(n):
    return HE.get(n, 'she')


def m(x):
    return f'${x:,.2f}'


def fs(x):
    x = Fr(x)
    return str(x.numerator) if x.denominator == 1 else f'{x.numerator}/{x.denominator}'


def dz(x, p=2):
    """Exact decimal text with at most p places (half up)."""
    v = Fr(x) * 10 ** p
    v = int(v + Fr(1, 2)) if v >= 0 else -int(-v + Fr(1, 2))
    s = f'{v / 10 ** p:.{p}f}'.rstrip('0').rstrip('.')
    return s


def mixed(x):
    x = Fr(x)
    w, r = divmod(x.numerator, x.denominator)
    return str(w) if r == 0 else (f'{w} {r}/{x.denominator}' if w else f'{r}/{x.denominator}')


T = {}


def t(unit, n):
    def deco(f):
        T[(unit, n)] = f
        return f
    return deco


# ---------- Unit 1: Algebraic Expressions and Integers ----------
@t('algebraic-expressions-integers', 2)
def _(r, nm):
    f, c, n = r.randint(20, 60), r.randint(8, 25), r.randint(4, 12)
    return (f'A gym charges a ${f} joining fee plus ${c} per month. Write an expression for the cost of n months, then find the cost of {n} months for {nm}.',
            str(f + c * n), [f'Cost = {f} + {c}n.', f'Substitute n = {n}: {f} + {c} × {n}.', f'= {f} + {c * n} = {f + c * n} dollars.'])


@t('algebraic-expressions-integers', 3)
def _(r, nm):
    a, c, na, nc, cp = r.randint(9, 15), r.randint(5, 8), r.randint(2, 3), r.randint(2, 4), r.choice([5, 6, 8])
    return (f'{nm} buys {na} adult tickets at ${a} each and {nc} child tickets at ${c} each, then uses a ${cp} coupon. Write one expression for the total and evaluate it.',
            str(na * a + nc * c - cp), [f'Expression: {na} × {a} + {nc} × {c} - {cp}.', f'Multiply first: {na * a} + {nc * c} - {cp}.', f'Add and subtract left to right: {na * a + nc * c - cp} dollars.'])


@t('algebraic-expressions-integers', 4)
def _(r, nm):
    b, g = r.randint(15, 35), r.randint(4, 9)
    us = [r.randint(2, 6) for _ in range(3)]
    tot = sum(b + g * u for u in us)
    return (f'A phone plan costs ${b} per month plus ${g} for each GB of data. {nm} uses {us[0]} GB, {us[1]} GB and {us[2]} GB in three months. Use the expression {b} + {g}d to find the total for the three months.',
            str(tot), [f'Month costs: {b} + {g}({us[0]}) = {b + g * us[0]}, {b} + {g}({us[1]}) = {b + g * us[1]}, {b} + {g}({us[2]}) = {b + g * us[2]}.', f'Total = {b + g * us[0]} + {b + g * us[1]} + {b + g * us[2]}.', f'= {tot} dollars.'])


@t('algebraic-expressions-integers', 5)
def _(r, nm):
    a, b, c = r.randint(20, 90), r.randint(30, 150), r.randint(10, 80)
    return (f'A diver is at -{a} ft, a bird is at {b} ft and a submarine is at -{c * 3} ft (0 ft is sea level). How far apart are the bird and the submarine, and how much farther is the submarine from sea level than the diver? Give the second answer.',
            str(c * 3 - a), [f'Distance from sea level is the absolute value: |-{a}| = {a} and |-{c * 3}| = {c * 3}.', f'The bird and submarine are {b} + {c * 3} = {b + c * 3} ft apart.', f'{c * 3} - {a} = {c * 3 - a} ft farther.'])


@t('algebraic-expressions-integers', 6)
def _(r, nm):
    s, u, d, u2 = -r.randint(3, 12), r.randint(5, 15), r.randint(4, 18), r.randint(2, 9)
    return (f'At 6 a.m. the temperature was {s}°F. It rose {u}°F by noon, fell {d}°F by evening and rose {u2}°F overnight. What was the temperature the next morning, in °F?',
            str(s + u - d + u2), [f'Write the changes as integers: {s} + {u} + (-{d}) + {u2}.', f'{s} + {u} = {s + u}; {s + u} + (-{d}) = {s + u - d}.', f'{s + u - d} + {u2} = {s + u - d + u2}°F.'])


@t('algebraic-expressions-integers', 7)
def _(r, nm):
    a, b, c = r.randint(200, 900), -r.randint(20, 280), -r.randint(300, 1200)
    return (f'A mountain trail starts at {a} ft. One cave is at {b} ft and a mine shaft bottom is at {c} ft. How many feet lower is the mine shaft bottom than the cave, and what is the total drop from the trail to the shaft bottom? Give the total drop.',
            str(a - c), [f'Drop from cave to shaft: {b} - ({c}) = {b - c} ft.', f'Drop from trail to shaft: {a} - ({c}) = {a} + {-c}.', f'= {a - c} ft.'])


@t('algebraic-expressions-integers', 8)
def _(r, nm):
    p = [round(r.uniform(2, 9) + r.choice([0.19, 0.49, 0.79, 0.95]), 2) for _ in range(3)]
    budget = sum(round(x) for x in p) + r.randint(2, 6)
    est = sum(round(x) for x in p)
    return (f'{nm} has ${budget}. {pr(nm).capitalize()} wants to buy items costing {", ".join(m(x) for x in p)}. Round each price to the nearest dollar to estimate the total, then estimate how much money will be left.',
            str(budget - est), [f'Round: {", ".join(str(round(x)) for x in p)}.', f'Estimated total: {est} dollars.', f'Estimated money left: {budget} - {est} = {budget - est} dollars.'])


@t('algebraic-expressions-integers', 9)
def _(r, nm):
    a, d, target = r.randint(3, 15), r.randint(4, 9), r.randint(150, 400)
    n = (target - a) // d + 2
    first = next(k for k in range(1, 1000) if a + (k - 1) * d > target)
    return (f'A pattern of tiles starts {a}, {a + d}, {a + 2 * d}, {a + 3 * d}, … and keeps adding {d}. Which is the first term number whose value is greater than {target}?',
            str(first), [f'Term n = {a} + {d}(n - 1).', f'Solve {a} + {d}(n - 1) > {target}: n - 1 > {fs(Fr(target - a, d))}.', f'The first whole number that works is n = {first} (value {a + (first - 1) * d}).'])


@t('algebraic-expressions-integers', 10)
def _(r, nm):
    s, d = r.randint(4, 9), r.randint(3, 7)
    fig = r.randint(12, 30); total = s + d * (fig - 1)
    return (f'Figure 1 of a toothpick pattern uses {s} toothpicks, and each new figure adds {d}. Which figure uses exactly {total} toothpicks?',
            str(fig), [f'Toothpicks in Figure n: {s} + {d}(n - 1).', f'{s} + {d}(n - 1) = {total}, so {d}(n - 1) = {total - s}.', f'n - 1 = {fig - 1}, so Figure {fig}.'])


@t('algebraic-expressions-integers', 11)
def _(r, nm):
    rate, t1, up, t2 = r.randint(4, 12), r.randint(3, 8), r.randint(3, 9), r.randint(2, 6)
    return (f'A diver descends {rate} ft per minute for {t1} minutes, then rises {up} ft per minute for {t2} minutes. Starting at the surface (0 ft), what is the diver\'s final position, in feet?',
            str(-rate * t1 + up * t2), [f'Descending: {t1} × (-{rate}) = {-rate * t1} ft.', f'Rising: {t2} × {up} = {up * t2} ft.', f'Final: {-rate * t1} + {up * t2} = {-rate * t1 + up * t2} ft.'])


@t('algebraic-expressions-integers', 12)
def _(r, nm):
    x1, y1 = -r.randint(2, 6), -r.randint(2, 6); w, h = r.randint(4, 9), r.randint(3, 8)
    return (f'Three corners of a rectangle are ({x1}, {y1}), ({x1 + w}, {y1}) and ({x1 + w}, {y1 + h}). Find the fourth corner, then find the area of the rectangle in square units. Give the area.',
            str(w * h), [f'The fourth corner is ({x1}, {y1 + h}).', f'Width = |{x1 + w} - ({x1})| = {w}; height = |{y1 + h} - ({y1})| = {h}.', f'Area = {w} × {h} = {w * h} square units.'])


# ---------- Unit 2: One-Step Equations and Inequalities ----------
@t('one-step-equations-inequalities', 1)
def _(r, nm):
    a, b = r.choice([(25, 4), (20, 5), (50, 2), (125, 8)]); c = r.randint(13, 47)
    return (f'A school orders {a} boxes. Each box holds {b} packs, and each pack has {c} stickers. Use the commutative and associative properties to find the total number of stickers, {a} × {c} × {b}, mentally.',
            str(a * b * c), [f'Reorder: ({a} × {b}) × {c}.', f'{a} × {b} = {a * b}.', f'{a * b} × {c} = {a * b * c}.'])


@t('one-step-equations-inequalities', 2)
def _(r, nm):
    k, p, q = r.randint(4, 8), r.randint(9, 19), r.choice([0.5, 1.5, 2.5, 3.5])
    tot = Fr(k) * (Fr(p) + Fr(str(q)))
    return (f'{k} friends each buy a ${p} ticket and a ${q:.2f} drink. Use the distributive property to find the total cost.',
            m(tot), [f'Total = {k}({p} + {q:.2f}).', f'= {k} × {p} + {k} × {q:.2f} = {k * p} + {dz(k * Fr(str(q)))}.', f'= {m(tot)}.'])


@t('one-step-equations-inequalities', 3)
def _(r, nm):
    a, b, c, x = r.randint(2, 5), r.randint(1, 9), r.randint(2, 6), r.randint(3, 9)
    per = (a + 1 + c) * x + b - 2
    return (f'A garden has sides of length {a}x + {b}, x - 2, {c}x and x feet. Write the perimeter as a simplified expression, then find it when x = {x}.',
            str(per), [f'Add the sides: ({a}x + {b}) + (x - 2) + {c}x + x.', f'Combine like terms: {a + 2 + c}x + {b - 2}.', f'When x = {x}: {a + 2 + c} × {x} + {b - 2} = {(a + 2 + c) * x + b - 2}.']) if False else (
        f'A garden has sides of length {a}x + {b}, x - 2, {c}x and x feet. Write the perimeter as a simplified expression, then find it when x = {x}.',
        str((a + 2 + c) * x + b - 2), [f'Add the sides: ({a}x + {b}) + (x - 2) + {c}x + x.', f'Combine like terms: {a + 2 + c}x + {b - 2}.', f'When x = {x}: {a + 2 + c} × {x} + {b - 2} = {(a + 2 + c) * x + b - 2} feet.'])


@t('one-step-equations-inequalities', 4)
def _(r, nm):
    p, n, tot = r.randint(3, 9), r.randint(4, 12), None
    tot = p * n + r.randint(1, 3)
    return (f'Pens cost ${p} each. {nm} says {pr(nm)} can buy n pens with ${tot} and have ${tot - p * n} left. Write an equation for n and find n.',
            str(n), [f'Equation: {p}n + {tot - p * n} = {tot}.', f'Subtract {tot - p * n}: {p}n = {p * n}.', f'Divide by {p}: n = {n}.'])


@t('one-step-equations-inequalities', 5)
def _(r, nm):
    s, e, left = r.randint(15, 40), r.randint(10, 35), r.randint(20, 90)
    return (f'{nm} spent ${s} on Monday and then earned ${e} on Tuesday. Now {pr(nm)} has ${left}. Write and solve an equation to find how much {pr(nm)} had at the start.',
            str(left + s - e), [f'Let x be the starting amount: x - {s} + {e} = {left}.', f'Combine: x + {e - s} = {left}.' if e >= s else f'Combine: x - {s - e} = {left}.', f'x = {left + s - e} dollars.'])


@t('one-step-equations-inequalities', 6)
def _(r, nm):
    serv, cups, want = r.choice([4, 6, 8]), r.choice([3, 6, 9, 12]), r.choice([10, 14, 18])
    per = Fr(cups, serv)
    return (f'A recipe for {serv} servings uses {cups} cups of rice. Write and solve an equation to find the cups for 1 serving, then find the cups needed for {want} servings.',
            mixed(per * want), [f'{serv}c = {cups}, so c = {cups}/{serv} = {mixed(per)} cup per serving.', f'For {want} servings: {want} × {mixed(per)}.', f'= {mixed(per * want)} cups.'])


@t('one-step-equations-inequalities', 7)
def _(r, nm):
    a, b = r.randint(7, 15), r.randint(3, 9)
    while a == b:
        b += 1
    return (f'Two whole numbers have a sum of {a + b} and a product of {a * b}. Guess, check and revise to find the greater number.',
            str(max(a, b)), [f'List factor pairs of {a * b} and check their sums.', f'{a} × {b} = {a * b} and {a} + {b} = {a + b}.', f'The greater number is {max(a, b)}.'])


@t('one-step-equations-inequalities', 8)
def _(r, nm):
    lim, used = r.randint(40, 80), r.randint(10, 30)
    return (f'A ride allows at most {lim} riders. {used} riders are already on. Write an inequality for the number r of riders who can still get on, and give the greatest value of r.',
            str(lim - used), [f'{used} + r ≤ {lim}.', f'Subtract {used}: r ≤ {lim - used}.', f'The greatest value is {lim - used}.'])


@t('one-step-equations-inequalities', 9)
def _(r, nm):
    need, have = r.randint(60, 150), r.randint(15, 55)
    return (f'{nm} needs at least {need} points to reach the next level. {pr(nm).capitalize()} already has {have}. Write and solve an inequality for the points p still needed, and give the least value of p.',
            str(need - have), [f'{have} + p ≥ {need}.', f'Subtract {have}: p ≥ {need - have}.', f'The least value is {need - have}.'])


@t('one-step-equations-inequalities', 10)
def _(r, nm):
    price, budget = r.choice([4, 6, 7, 9, 12]), r.randint(50, 120)
    return (f'Tickets cost ${price} each. {nm} can spend at most ${budget}. Write and solve an inequality for the number of tickets t, and give the greatest whole number of tickets.',
            str(budget // price), [f'{price}t ≤ {budget}.', f'Divide by {price}: t ≤ {fs(Fr(budget, price))}.', f'The greatest whole number is {budget // price}.'])


# ---------- Unit 3: Decimals and Equations ----------
@t('decimals-equations', 1)
def _(r, nm):
    p = [round(r.uniform(3, 12), 2) for _ in range(3)]
    est = sum(round(x) for x in p); act = Fr(str(round(sum(p), 2)))
    return (f'{nm} buys items for {", ".join(m(x) for x in p)}. Estimate the total by rounding each price to the nearest dollar. How far is the estimate from the exact total? Give the difference in dollars.',
            m(abs(Fr(est) - act)), [f'Rounded: {" + ".join(str(round(x)) for x in p)} = {est}.', f'Exact: {" + ".join(f"{x:.2f}" for x in p)} = {m(act)}.', f'Difference: {m(abs(Fr(est) - act))}.'])


@t('decimals-equations', 2)
def _(r, nm):
    pr_, w = round(r.uniform(2, 6), 2), round(r.uniform(3, 9), 1)
    est = round(pr_) * round(w)
    return (f'Apples cost {m(pr_)} per pound. {nm} buys {w} pounds. Estimate the cost by rounding both numbers to the nearest whole number, then find the exact cost to the nearest cent. Give the exact cost.',
            m(Fr(str(pr_)) * Fr(str(w))), [f'Estimate: {round(pr_)} × {round(w)} = {est} dollars.', f'Exact: {pr_:.2f} × {w} = {dz(Fr(str(pr_)) * Fr(str(w)), 3)}.', f'Rounded to the cent: {m(Fr(str(pr_)) * Fr(str(w)))}.'])


@t('decimals-equations', 3)
def _(r, nm):
    sc = [r.randint(70, 98) for _ in range(4)]; want = r.randint(84, 92)
    need = want * 5 - sum(sc)
    return (f'{nm}\'s first four quiz scores are {", ".join(map(str, sc))}. What score on the fifth quiz makes the mean exactly {want}?',
            str(need), [f'A mean of {want} for 5 quizzes means a total of {want} × 5 = {want * 5}.', f'The first four add to {sum(sc)}.', f'Fifth score = {want * 5} - {sum(sc)} = {need}.'])


@t('decimals-equations', 4)
def _(r, nm):
    r1, t1, r2, t2 = r.randint(40, 65), r.choice([1.5, 2, 2.5]), r.randint(25, 45), r.choice([0.5, 1, 1.5])
    d = Fr(r1) * Fr(str(t1)) + Fr(r2) * Fr(str(t2))
    return (f'{nm} drives {t1} hour{"s" if t1 != 1 else ""} at {r1} mi/h and then {t2} hour{"s" if t2 != 1 else ""} at {r2} mi/h. Use d = rt for each part to find the total distance in miles.',
            dz(d), [f'Part 1: {r1} × {t1} = {dz(Fr(r1) * Fr(str(t1)))} miles.', f'Part 2: {r2} × {t2} = {dz(Fr(r2) * Fr(str(t2)))} miles.', f'Total = {dz(d)} miles.'])


@t('decimals-equations', 5)
def _(r, nm):
    b, d1, w, d2 = round(r.uniform(20, 80), 2), round(r.uniform(5, 40), 2), round(r.uniform(10, 50), 2), round(r.uniform(3, 15), 2)
    end = Fr(str(b)) + Fr(str(d1)) - Fr(str(w)) - Fr(str(d2))
    return (f'{nm}\'s account had {m(b)}. {pr(nm).capitalize()} deposited {m(d1)}, spent {m(w)} and paid a {m(d2)} fee. Write an equation for the final balance x and solve it.',
            m(end), [f'x = {b:.2f} + {d1:.2f} - {w:.2f} - {d2:.2f}.', f'{b:.2f} + {d1:.2f} = {dz(Fr(str(b)) + Fr(str(d1)))}; subtract {w:.2f} and {d2:.2f}.', f'x = {m(end)}.'])


@t('decimals-equations', 6)
def _(r, nm):
    a, pa, b, pb = r.choice([12, 16, 20]), round(r.uniform(2.5, 5), 2), r.choice([24, 28, 32]), round(r.uniform(4.5, 8), 2)
    ua, ub = Fr(str(pa)) / a, Fr(str(pb)) / b
    better = f'{a} oz' if ua < ub else f'{b} oz'
    return (f'A {a}-ounce box of cereal costs {m(pa)} and a {b}-ounce box costs {m(pb)}. Solve {a}u = {pa:.2f} and {b}v = {pb:.2f} to find each price per ounce. How much less per ounce, in cents rounded to the nearest tenth, is the better buy?',
            dz(abs(ua - ub) * 100, 1), [f'u = {pa:.2f} ÷ {a} ≈ ${float(ua):.4f} per ounce.', f'v = {pb:.2f} ÷ {b} ≈ ${float(ub):.4f} per ounce.', f'The {better} box is cheaper by about {dz(abs(ua - ub) * 100, 1)} cents per ounce.'])


@t('decimals-equations', 7)
def _(r, nm):
    L, cup = r.choice([1.5, 2, 2.4, 3]), r.choice([250, 300, 350])
    ml = int(Fr(str(L)) * 1000)
    return (f'{nm} has {L} L of juice and pours it into {cup} mL cups. How many full cups can {pr(nm)} pour, and how many milliliters are left over? Give the number left over.',
            str(ml % cup), [f'{L} L = {ml} mL.', f'{ml} ÷ {cup} = {ml // cup} full cups with a remainder.', f'Left over: {ml} - {ml // cup} × {cup} = {ml % cup} mL.'])


# ---------- Unit 4: Factors, Fractions and Exponents ----------
@t('factors-fractions-exponents', 1)
def _(r, nm):
    rows = r.choice([12, 14, 16, 18]); n = rows * r.randint(8, 15) + r.choice([0, r.randint(1, rows - 1)])
    return (f'{n} students line up in rows of {rows} for a photo. How many more students are needed so that every row is full?',
            str((-n) % rows), [f'{n} ÷ {rows} = {n // rows} rows with remainder {n % rows}.', f'A full extra row needs {rows} students.' if n % rows else 'There is no remainder.', f'Students needed: {(-n) % rows}.'])


@t('factors-fractions-exponents', 2)
def _(r, nm):
    s, h = r.randint(2, 6), r.randint(4, 8)
    return (f'A culture starts with {s} bacteria, and the number doubles every hour. Write an expression with an exponent for the number after {h} hours and evaluate it.',
            str(s * 2 ** h), [f'After h hours: {s} × 2^h.', f'2^{h} = {2 ** h}.', f'{s} × {2 ** h} = {s * 2 ** h} bacteria.'])


@t('factors-fractions-exponents', 3)
def _(r, nm):
    g = r.choice([6, 8, 9, 12]); a, b = g * r.randint(4, 9), g * r.randint(3, 8)
    gg = math.gcd(a, b)
    return (f'{nm} makes identical gift bags from {a} pencils and {b} erasers, using every item. What is the greatest number of bags, and how many pencils go in each? Give the number of bags.',
            str(gg), [f'The number of bags must divide both {a} and {b}.', f'GCF({a}, {b}) = {gg}.', f'{gg} bags, each with {a // gg} pencils and {b // gg} erasers.'])


@t('factors-fractions-exponents', 4)
def _(r, nm):
    tot, part = r.choice([(84, 36), (90, 54), (120, 45), (72, 30)]); big = r.choice([140, 210, 280])
    f = Fr(part, tot)
    return (f'In a survey, {part} of {tot} students walk to school. Write this as a fraction in simplest form. At the same rate, how many of {big} students walk?',
            dz(f * big, 1), [f'{part}/{tot} = {fs(f)} in simplest form.', f'{fs(f)} × {big}.', f'= {dz(f * big, 1)} students.'])


@t('factors-fractions-exponents', 5)
def _(r, nm):
    temps = sorted(r.sample([-7.5, -3.25, -1.5, 0.5, 2.75, 4.5, -5, 1.25], 5))
    r.shuffle(temps)
    srt = sorted(temps)
    return (f'Five noon temperatures (°C) were {", ".join(f"{x:g}" for x in temps)}. Order them from least to greatest and find the median.',
            f'{srt[2]:g}', [f'Ordered: {", ".join(f"{x:g}" for x in srt)}.', 'The median is the middle (3rd) value.', f'Median = {srt[2]:g} °C.'])


@t('factors-fractions-exponents', 6)
def _(r, nm):
    A = r.choice([50, 70, 90, 110, 130])
    s = math.sqrt(A)
    return (f'A square garden has an area of {A} m². Between which two whole numbers is its side length? Estimate the fence needed for all four sides to the nearest meter.',
            str(round(4 * s)), [f'Side = √{A}, between {math.isqrt(A)} and {math.isqrt(A) + 1} because {math.isqrt(A)}² = {math.isqrt(A) ** 2} and {math.isqrt(A) + 1}² = {(math.isqrt(A) + 1) ** 2}.',
                                f'√{A} ≈ {s:.2f}.', f'Fence ≈ 4 × {s:.2f} ≈ {round(4 * s)} m.'])


@t('factors-fractions-exponents', 7)
def _(r, nm):
    a, b, p, q, x = r.randint(2, 4), r.randint(2, 5), r.randint(2, 3), r.randint(1, 3), r.choice([2, 3])
    return (f'A box has length {a}x^{p} and width {b}x^{q}. Write its area as a single monomial, then evaluate it for x = {x}.',
            str(a * b * x ** (p + q)), [f'({a}x^{p})({b}x^{q}) = {a * b}x^{p + q} (multiply coefficients, add exponents).', f'x^{p + q} = {x}^{p + q} = {x ** (p + q)}.', f'{a * b} × {x ** (p + q)} = {a * b * x ** (p + q)}.'])


@t('factors-fractions-exponents', 8)
def _(r, nm):
    d, f = r.randint(30, 40), r.randint(18, 26)
    return (f'A drive holds 2^{d} bytes and each video file is 2^{f} bytes. How many files fit on the drive? Write the answer as a power of 2, then as a whole number.',
            str(2 ** (d - f)), [f'2^{d} ÷ 2^{f} = 2^{d - f} (subtract exponents).', f'2^{d - f} = {2 ** (d - f):,}.', f'{2 ** (d - f):,} files.'])


@t('factors-fractions-exponents', 9)
def _(r, nm):
    dist, sp_ = r.choice([(1.5, 3), (2.4, 3), (6, 3), (4.5, 3)]), None
    d_km, e = r.choice([(1.5, 8), (2.4, 9), (3.6, 8)])
    t = Fr(str(d_km)) * 10 ** e / (3 * 10 ** 5)
    return (f'A space probe is {d_km} × 10^{e} km from Earth. A radio signal travels about 3 × 10^5 km per second. How many seconds does a signal take to reach the probe?',
            f'{int(t):,}', [f'Time = distance ÷ speed = ({d_km} × 10^{e}) ÷ (3 × 10^5).', f'= ({d_km} ÷ 3) × 10^{e - 5} = {Fr(str(d_km)) / 3} × 10^{e - 5}.'.replace(str(Fr(str(d_km)) / 3), dz(Fr(str(d_km)) / 3)), f'= {int(t):,} seconds.'])


@t('factors-fractions-exponents', 10)
def _(r, nm):
    s = r.randint(3, 9)
    return (f'A cube-shaped box has a volume of {s ** 3} cm³. Find its edge length, then find its total surface area in square centimeters.',
            str(6 * s * s), [f'Edge = ∛{s ** 3} = {s} cm.', f'One face: {s} × {s} = {s * s} cm².', f'Surface area = 6 × {s * s} = {6 * s * s} cm².'])


# ---------- Unit 5: Operations with Fractions ----------
@t('operations-fractions', 1)
def _(r, nm):
    xs = [Fr(-3, 4), Fr(2, 5), Fr(-1, 3), Fr(5, 8), Fr(-1, 6)]
    r.shuffle(xs)
    best = min(xs, key=abs)
    return (f'Five changes in a stock price (in dollars) were {", ".join(fs(x) for x in xs)}. Which change was closest to 0? Write it as a fraction.',
            fs(best), ['Compare absolute values: ' + ', '.join(f'|{fs(x)}| = {fs(abs(x))}' for x in xs) + '.', 'Write them with a common denominator or as decimals to compare.', f'The smallest absolute value belongs to {fs(best)}.'])


@t('operations-fractions', 2)
def _(r, nm):
    a, b = r.choice([(Fr(3, 8), 0.4), (Fr(5, 8), 0.25), (Fr(1, 4), 0.35), (Fr(3, 5), 0.15)])
    tot = a + Fr(str(b))
    return (f'{nm} ate {fs(a)} of one pizza and {b} of another pizza of the same size. Write the total amount eaten as a decimal.',
            dz(tot, 3), [f'{fs(a)} = {dz(a, 3)}.', f'{dz(a, 3)} + {b} = {dz(tot, 3)}.', f'Total: {dz(tot, 3)} of a pizza.'])


@t('operations-fractions', 3)
def _(r, nm):
    L = Fr(r.randint(7, 10)) + Fr(r.choice([1, 3]), 4); a = Fr(r.randint(2, 3)) + Fr(1, 2); b = Fr(r.randint(1, 3)) + Fr(2, 3)
    return (f'A board is {mixed(L)} ft long. {nm} cuts off pieces of {mixed(a)} ft and {mixed(b)} ft. How long is the piece that is left? Write a fraction or mixed number.',
            mixed(L - a - b), [f'Total cut: {mixed(a)} + {mixed(b)} = {mixed(a + b)} ft.', f'Use a common denominator: {mixed(L)} - {mixed(a + b)}.', f'= {mixed(L - a - b)} ft.'])


@t('operations-fractions', 4)
def _(r, nm):
    per = Fr(3, 4); have = Fr(r.randint(4, 7)) + Fr(r.choice([1, 3]), 4)
    while (have / per).denominator == 1:
        have += Fr(1, 2)
    n = int(have // per)
    return (f'Each batch of muffins uses 3/4 cup of milk. {nm} has {mixed(have)} cups. How many full batches can {pr(nm)} make, and how much milk is left? Give the milk left as a fraction of a cup.',
            fs(have - n * per), [f'{mixed(have)} ÷ 3/4 = {fs(have)} × 4/3 = {mixed(have / per)}.', f'So {n} full batches use {mixed(n * per)} cups.', f'Left: {mixed(have)} - {mixed(n * per)} = {fs(have - n * per)} cup.'])


@t('operations-fractions', 5)
def _(r, nm):
    ft, inch, k = r.randint(10, 20), r.choice([3, 4, 6, 8]), r.choice([3, 4, 6])
    tot = ft * 12 + inch
    return (f'A ribbon is {ft} ft {inch} in. long. {nm} cuts it into {k} equal pieces. How long is each piece, in inches?',
            mixed(Fr(tot, k)) + ' in.', [f'{ft} ft {inch} in. = {ft} × 12 + {inch} = {tot} in.', f'{tot} ÷ {k}.', f'= {mixed(Fr(tot, k))} in.'])


@t('operations-fractions', 6)
def _(r, nm):
    a = Fr(r.randint(1, 3)) + Fr(r.choice([1, 3]), 4); tot = Fr(r.randint(6, 9)) + Fr(r.choice([1, 5, 7]), 8)
    return (f'A puppy gained {mixed(a)} lb this month and now weighs {mixed(tot)} lb. Write and solve an equation for its weight w last month. Write a mixed number.',
            f'w = {mixed(tot - a)}', [f'w + {mixed(a)} = {mixed(tot)}.', f'Subtract {mixed(a)} from both sides, using a common denominator of 8.', f'w = {mixed(tot - a)} lb.'])


@t('operations-fractions', 7)
def _(r, nm):
    f = r.choice([Fr(2, 3), Fr(3, 4), Fr(3, 5)]); s = r.choice([120, 180, 240, 300])
    part = f * s; spent = Fr(1, 4)
    return (f'{nm} has saved {fs(f)} of the cost of a bike, which is ${part}. Write and solve an equation for the cost of the bike. If {pr(nm)} then spends 1/4 of the savings on a helmet, how much savings are left? Give the savings left.',
            str(part * (1 - spent)), [f'({fs(f)})c = {part}, so c = {part} × {fs(1 / f)} = {s} dollars.', f'Helmet: 1/4 × {part} = {part * spent}.', f'Left: {part} - {part * spent} = {part * (1 - spent)} dollars.'])


@t('operations-fractions', 8)
def _(r, nm):
    a, b, p = r.choice([(2, 3), (3, 4), (1, 2)])[0], None, None
    a, b = r.choice([(2, 3), (3, 4), (3, 2)])
    p, q = r.choice([(3, 2), (2, 3), (4, 2)])
    v = Fr(a, b) ** p * Fr(b, a) ** q
    return (f'Evaluate ({a}/{b})^{p} × ({b}/{a})^{q} by first using the power rules.',
            fs(v), [f'({b}/{a})^{q} = 1 ÷ ({a}/{b})^{q}, so the product is ({a}/{b})^{p - q}.', f'({a}/{b})^{p - q} = {a ** (p - q) if p >= q else b ** (q - p)}/{b ** (p - q) if p >= q else a ** (q - p)}.', f'= {fs(v)}.'])


# ---------- Unit 6: Ratios, Proportions and Percentages ----------
@t('ratios-proportions-percentages', 1)
def _(r, nm):
    a, pa, b, pb = r.choice([(12, 3.48), (16, 4.32), (20, 5.2)])[0], None, None, None
    a, pa = r.choice([(12, 3.48), (16, 4.32), (20, 5.6)]); b, pb = r.choice([(32, 7.68), (24, 6.48), (28, 7.84)])
    ua, ub = Fr(str(pa)) / a, Fr(str(pb)) / b
    while ua == ub:
        b, pb = 30, 7.5; ub = Fr(str(pb)) / b
    return (f'Store A sells {a} oz of trail mix for {m(pa)}. Store B sells {b} oz for {m(pb)}. Find each unit price. How many cents per ounce do you save at the cheaper store?',
            dz(abs(ua - ub) * 100, 1), [f'A: {pa:.2f} ÷ {a} = ${dz(ua, 4)} per ounce.', f'B: {pb:.2f} ÷ {b} = ${dz(ub, 4)} per ounce.', f'Savings: {dz(abs(ua - ub) * 100, 1)} cent{"" if dz(abs(ua - ub) * 100, 1) == "1" else "s"} per ounce at Store {"A" if ua < ub else "B"}.'])


@t('ratios-proportions-percentages', 2)
def _(r, nm):
    a, b, n, join = r.choice([3, 2, 5]), r.choice([8, 5, 9]), None, r.randint(5, 20)
    n = b * r.randint(12, 25)
    return (f'At a camp, {a} of every {b} campers swim. There are {n} campers. How many swim? If {join} more campers join and all of them swim, how many campers swim then?',
            str(a * n // b + join), [f'{a}/{b} = s/{n}.', f's = {a} × {n} ÷ {b} = {a * n // b}.', f'{a * n // b} + {join} = {a * n // b + join}.'])


@t('ratios-proportions-percentages', 3)
def _(r, nm):
    sc, w, h = r.choice([4, 6, 8]), Fr(r.choice([5, 7, 9]), 2), Fr(r.choice([3, 4, 6]))
    W, H = w * sc, h * sc
    return (f'A floor plan uses the scale 1 in. : {sc} ft. A room is {dz(w, 1)} in. by {dz(h, 1)} in. on the plan. What is the actual area of the room in square feet?',
            dz(W * H, 1), [f'Actual length: {dz(w, 1)} × {sc} = {dz(W, 1)} ft.', f'Actual width: {dz(h, 1)} × {sc} = {dz(H, 1)} ft.', f'Area = {dz(W, 1)} × {dz(H, 1)} = {dz(W * H, 1)} ft².'])


@t('ratios-proportions-percentages', 4)
def _(r, nm):
    red, blue, green, n = r.randint(3, 8), r.randint(2, 7), r.randint(4, 9), r.choice([60, 90, 120])
    tot = red + blue + green
    p = Fr(tot - red, tot)
    return (f'A bag has {red} red, {blue} blue and {green} green marbles. A marble is drawn and replaced {n} times. What is P(not red)? About how many of the {n} draws should not be red? Give the expected number.',
            dz(p * n, 1), [f'P(not red) = {tot - red}/{tot} = {fs(p)}.', f'Expected number = {fs(p)} × {n}.', f'= {dz(p * n, 1)} draws.'])


@t('ratios-proportions-percentages', 5)
def _(r, nm):
    xs = [('3/8', Fr(3, 8)), ('0.4', Fr(2, 5)), ('35%', Fr(7, 20)), ('0.36', Fr(9, 25))]
    r.shuffle(xs)
    hi, lo = max(xs, key=lambda x: x[1]), min(xs, key=lambda x: x[1])
    return (f'Four classes reported the fraction of students who bike: {", ".join(x[0] for x in xs)}. Write each as a percent. How many percentage points apart are the greatest and least values?',
            dz((hi[1] - lo[1]) * 100, 1), ['As percents: ' + ', '.join(f'{x[0]} = {dz(x[1] * 100, 1)}%' for x in xs) + '.', f'Greatest {dz(hi[1] * 100, 1)}%, least {dz(lo[1] * 100, 1)}%.', f'Difference: {dz((hi[1] - lo[1]) * 100, 1)} percentage points.'])


@t('ratios-proportions-percentages', 6)
def _(r, nm):
    n, p1, p2 = r.choice([250, 400, 500, 600]), r.choice([40, 60, 30]), r.choice([25, 30, 45])
    a = Fr(p1, 100) * n
    return (f'In a survey of {n} students, {p1}% play a sport. Of those, {p2}% play soccer. How many students play soccer?',
            dz(a * p2 / 100, 1), [f'{p1}% of {n} = {dz(a, 1)} students play a sport.', f'{p2}% of {dz(a, 1)} = {dz(a * p2 / 100, 1)}.', f'{dz(a * p2 / 100, 1)} students play soccer.'])


@t('ratios-proportions-percentages', 7)
def _(r, nm):
    pr_, tax = r.choice([24, 36, 48, 75]), r.choice([5, 6.25, 7])
    disc = r.choice([10, 15, 20])
    sale = Fr(pr_) * (100 - disc) / 100; tot = sale * (1 + Fr(str(tax)) / 100)
    return (f'A ${pr_} game is {disc}% off, and then {tax:g}% sales tax is added to the sale price. Write and solve equations to find the final cost to the nearest cent.',
            m(tot), [f'Sale price: {pr_} × {fs(Fr(100 - disc, 100))} = {m(sale)}.', f'Tax: {tax:g}% of {m(sale)} = {m(sale * Fr(str(tax)) / 100)}.', f'Final cost: {m(tot)}.'])


@t('ratios-proportions-percentages', 8)
def _(r, nm):
    a, b = r.choice([(40, 50), (80, 60), (25, 30), (120, 90), (64, 80)])
    c = Fr(b - a, a) * 100
    return (f'A school recycled {a} kg of paper last year and {b} kg this year. Find the percent change. Is it an increase or a decrease? If the same percent change happens next year, how many kilograms will the school recycle? Give the kilograms next year.',
            dz(b * (1 + c / 100), 1), [f'Percent change: ({b} - {a}) ÷ {a} × 100% = {dz(c, 1)}%.', f'{"Increase" if b > a else "Decrease"}.', f'Next year: {b} × {dz(1 + c / 100, 4)} = {dz(b * (1 + c / 100), 1)} kg.'])


@t('ratios-proportions-percentages', 9)
def _(r, nm):
    cost, mu, md = r.choice([20, 40, 50, 80]), r.choice([40, 50, 60]), r.choice([20, 25, 30])
    p1 = Fr(cost) * (100 + mu) / 100; p2 = p1 * (100 - md) / 100
    return (f'A store pays ${cost} for a jacket, marks it up {mu}%, and later marks the new price down {md}%. What is the final price, and what is the store\'s profit? Give the profit.',
            m(p2 - cost), [f'Marked-up price: {cost} × {fs(Fr(100 + mu, 100))} = {m(p1)}.', f'Sale price: {m(p1)} × {fs(Fr(100 - md, 100))} = {m(p2)}.', f'Profit: {m(p2)} - {m(cost)} = {m(p2 - cost)}.'])


@t('ratios-proportions-percentages', 10)
def _(r, nm):
    k, xs = r.choice([3, 4, 6, 7]), sorted(r.sample(range(2, 12), 4)); want = r.randint(15, 30)
    return (f'A table shows hours worked x: {", ".join(map(str, xs))} and pay y: {", ".join(str(k * x) for x in xs)} dollars. Show the relationship is proportional, write an equation, and find the pay for {want} hours.',
            str(k * want), [f'Every y/x is {k}, so the relationship is proportional with k = {k}.', f'y = {k}x.', f'For x = {want}: y = {k * want} dollars.'])


@t('ratios-proportions-percentages', 11)
def _(r, nm):
    p, b = r.choice([5, 8, 12, 15]), r.choice([40, 60, 80, 120])
    return (f'A price b increases by {p}%. {nm} writes the new price as b + {Fr(p, 100) if False else p / 100:g}b. Rewrite this as a single term, and use it to find the new price of a ${b} item.',
            m(Fr(b) * (100 + p) / 100), [f'b + {p / 100:g}b = (1 + {p / 100:g})b = {1 + p / 100:g}b.', f'For b = {b}: {1 + p / 100:g} × {b}.', f'= {m(Fr(b) * (100 + p) / 100)}.'])


# ---------- Unit 7: Solving Equations and Inequalities ----------
@t('solving-equations-inequalities', 1)
def _(r, nm):
    base, per, miles, tip = r.choice([3, 4, 5]), r.choice([2, 3]), r.randint(6, 15), r.choice([4, 5, 6])
    tot = base + per * miles + tip
    return (f'A taxi charges ${base} plus ${per} per mile. {nm} paid ${tot}, which included a ${tip} tip. Write and solve an equation for the number of miles.',
            str(miles), [f'{base} + {per}m + {tip} = {tot}.', f'{per}m = {tot - base - tip}.', f'm = {miles} miles.'])


@t('solving-equations-inequalities', 2)
def _(r, nm):
    a, b, x = r.randint(2, 4), r.randint(3, 9), r.randint(6, 15)
    P = 2 * (a * x + b) + 2 * x
    return (f'A rectangle\'s length is {b} cm more than {a} times its width w. Its perimeter is {P} cm. Write and solve an equation for w, then find the area. Give the area in square centimeters.',
            str(x * (a * x + b)), [f'2({a}w + {b}) + 2w = {P}, so {2 * a + 2}w + {2 * b} = {P}.', f'w = {x} cm, length = {a * x + b} cm.', f'Area = {x} × {a * x + b} = {x * (a * x + b)} cm².'])


@t('solving-equations-inequalities', 3)
def _(r, nm):
    rate, fee, x = r.choice([0.15, 0.25, 0.35]), r.choice([2.5, 3.5, 4.75]), r.randint(12, 40)
    tot = Fr(str(rate)) * x + Fr(str(fee))
    return (f'A printing service charges {m(fee)} per order plus {m(rate)} per page. {nm}\'s bill was {m(tot)}. Write and solve an equation for the number of pages.',
            str(x), [f'{rate:.2f}p + {fee:.2f} = {dz(tot)}.', f'{rate:.2f}p = {dz(tot - Fr(str(fee)))}.', f'p = {x} pages.'])


@t('solving-equations-inequalities', 4)
def _(r, nm):
    k, c, ago = 3, r.randint(11, 14), r.randint(1, 3)
    s = (k * (c - ago) + ago) if True else 0
    return (f'{ago} year{"s" if ago != 1 else ""} ago, {nm}\'s mother was {k} times as old as {nm}. {nm} is {c} now. Write and solve an equation to find the mother\'s age now.',
            str(k * (c - ago) + ago), [f'{ago} years ago {nm} was {c - ago}.', f'Mother then: m - {ago} = {k}({c - ago}) = {k * (c - ago)}.', f'm = {k * (c - ago) + ago}.'])


@t('solving-equations-inequalities', 5)
def _(r, nm):
    fa, ra, rb = r.choice([30, 45, 60]), r.choice([4, 5, 6]), r.choice([8, 9, 10])
    while fa % (rb - ra):
        fa += 1
    n = fa // (rb - ra)
    return (f'Gym A charges ${fa} plus ${ra} per visit. Gym B charges ${rb} per visit with no fee. For how many visits do the gyms cost the same, and what is that cost? Give the number of visits.',
            str(n), [f'{fa} + {ra}v = {rb}v.', f'{fa} = {rb - ra}v, so v = {n}.', f'Both cost {rb * n} dollars at {n} visits.'])


@t('solving-equations-inequalities', 6)
def _(r, nm):
    need, have, wk = r.randint(200, 400), r.randint(30, 90), r.choice([15, 20, 25])
    w = -(-(need - have) // wk)
    return (f'{nm} has ${have} and saves ${wk} each week. {pr(nm).capitalize()} needs at least ${need}. Write and solve an inequality for the number of weeks w, and give the least whole number of weeks.',
            str(w), [f'{have} + {wk}w ≥ {need}.', f'{wk}w ≥ {need - have}, so w ≥ {fs(Fr(need - have, wk))}.', f'The least whole number is {w}.'])


@t('solving-equations-inequalities', 7)
def _(r, nm):
    P, l = r.randint(40, 90) * 2, r.randint(12, 30)
    return (f'Solve P = 2l + 2w for w. Then find the width of a rectangle with perimeter {P} m and length {l} m.',
            str(P // 2 - l), ['P - 2l = 2w.', 'w = (P - 2l)/2.', f'w = ({P} - {2 * l})/2 = {P // 2 - l} m.'])


@t('solving-equations-inequalities', 8)
def _(r, nm):
    p, rt, y = r.choice([1000, 1500, 2000]), r.choice([3, 4, 5]), r.choice([2, 3])
    si = Fr(p * rt * y, 100); ci = Fr(p) * (1 + Fr(rt, 100)) ** y - p
    return (f'{nm} invests ${p:,} at {rt}% for {y} years. How much more interest does compound interest (compounded once a year) earn than simple interest? Round to the nearest cent.',
            m(ci - si), [f'Simple: {p} × {rt / 100:g} × {y} = {m(si)}.', f'Compound: {p} × {1 + rt / 100:g}^{y} - {p} = {m(ci)}.', f'Difference: {m(ci - si)}.'])


# ---------- Unit 8: Linear Functions and Graphing ----------
@t('linear-functions-graphing', 1)
def _(r, nm):
    f, c, tot = r.choice([12, 15, 20]), r.choice([3, 4, 5]), None
    x = r.randint(8, 20); tot = f + c * x
    return (f'A rental cost is a function of hours: C(h) = {c}h + {f}. What input h gives an output of C = {tot}? Is the answer a sensible number of hours?',
            str(x), [f'{c}h + {f} = {tot}.', f'{c}h = {tot - f}.', f'h = {x}, a sensible number of hours.'])


@t('linear-functions-graphing', 2)
def _(r, nm):
    m_, b, y = r.randint(2, 6), r.randint(1, 9), None
    x = r.randint(3, 12); y = m_ * x + b
    return (f'The cost y of x tickets is y = {m_}x + {b} (in dollars). {nm} paid ${y}. How many tickets did {pr(nm)} buy, and is ({x}, {y}) a solution of the equation? Give the number of tickets.',
            str(x), [f'{y} = {m_}x + {b}.', f'{m_}x = {y - b}, so x = {x}.', f'Check: {m_}({x}) + {b} = {y}, so ({x}, {y}) is a solution.'])


@t('linear-functions-graphing', 3)
def _(r, nm):
    x1, y1, m_, b = r.randint(1, 4), None, r.randint(2, 5), r.randint(-6, 6)
    y1 = m_ * x1 + b; x2 = x1 + r.randint(2, 4); y2 = m_ * x2 + b
    return (f'A line passes through ({x1}, {y1}) and ({x2}, {y2}). Find its slope and y-intercept, then find y when x = 10.',
            str(m_ * 10 + b), [f'Slope = ({y2} - {y1})/({x2} - {x1}) = {m_}.', f'y-intercept: {y1} = {m_}({x1}) + b, so b = {b}.', f'y = {m_}(10) {"+" if b >= 0 else "-"} {abs(b)} = {m_ * 10 + b}.'])


@t('linear-functions-graphing', 4)
def _(r, nm):
    f, c = r.choice([25, 30, 40]), r.choice([12, 15, 18])
    xs = [1, 2, 4, 5]
    return (f'A plumber\'s charges are shown: hours x: {", ".join(map(str, xs))}; cost y: {", ".join(str(f + c * x) for x in xs)}. Write a rule for the cost, then find the cost of a 7.5-hour job.',
            m(Fr(f) + Fr(c) * Fr(15, 2)), [f'Rate of change: ({f + 2 * c} - {f + c}) ÷ 1 = {c} per hour.', f'Rule: y = {c}x + {f}.', f'y = {c}(7.5) + {f} = {m(Fr(f) + Fr(c) * Fr(15, 2))}.'])


@t('linear-functions-graphing', 5)
def _(r, nm):
    a, b, x, actual = r.choice([2, 2.5, 3]), r.randint(40, 55), r.randint(6, 14), None
    pred = Fr(str(a)) * x + b; actual = pred + r.choice([-4, -3, 3, 5])
    return (f'A trend line for test score y and hours studied x is y = {a}x + {b}. {nm} studied {x} hours and scored {dz(actual)}. What is the predicted score, and how far above or below the prediction is {nm}\'s actual score? Give the actual minus the predicted score.',
            dz(actual - pred), [f'Predicted: {a}({x}) + {b} = {dz(pred)}.', f'Actual - predicted = {dz(actual)} - {dz(pred)}.', f'= {dz(actual - pred)} points.'])


@t('linear-functions-graphing', 6)
def _(r, nm):
    a, ra, rb = r.choice([20, 30, 40]), r.choice([5, 6]), r.choice([9, 10, 11])
    while a % (rb - ra):
        a += 1
    x = a // (rb - ra)
    return (f'Plan A costs ${a} plus ${ra} per class; Plan B costs ${rb} per class. Graph y = {ra}x + {a} and y = {rb}x. At what number of classes do the lines intersect, and what does that mean? Give the number of classes.',
            str(x), [f'Set equal: {ra}x + {a} = {rb}x.', f'{a} = {rb - ra}x, so x = {x}.', f'At {x} classes both plans cost {rb * x} dollars; the intersection is ({x}, {rb * x}).'])


@t('linear-functions-graphing', 7)
def _(r, nm):
    n, a, c = r.randint(80, 200), r.choice([8, 10, 12]), r.choice([5, 6])
    k = r.randint(20, n - 20)
    tot = a * k + c * (n - k)
    return (f'A play sold {n} tickets for ${tot}. Adult tickets cost ${a} and student tickets cost ${c}. Solve the system x + y = {n} and {a}x + {c}y = {tot} by substitution. How many adult tickets were sold?',
            str(k), [f'y = {n} - x.', f'{a}x + {c}({n} - x) = {tot}, so {a - c}x = {tot - c * n}.', f'x = {k} adult tickets.'])


@t('linear-functions-graphing', 8)
def _(r, nm):
    a, b, budget = r.choice([4, 5, 6]), r.choice([2, 3]), r.choice([60, 72, 90])
    x = r.randint(3, budget // a - 2)
    ymax = (budget - a * x) // b
    return (f'Pizzas cost ${a} and drinks cost ${b}. The budget is at most ${budget}, so {a}x + {b}y ≤ {budget}. If x = {x} pizzas are bought, what is the greatest number of drinks y?',
            str(ymax), [f'{a}({x}) + {b}y ≤ {budget}.', f'{b}y ≤ {budget - a * x}, so y ≤ {fs(Fr(budget - a * x, b))}.', f'The greatest whole number of drinks is {ymax}.'])


# ---------- Unit 9: Spatial Thinking ----------
@t('spatial-thinking', 1)
def _(r, nm):
    x = r.randint(4, 12); a, b, c, d = r.randint(2, 4), r.randint(1, 9), r.randint(1, 3), r.randint(2, 8)
    while c * x - d <= 2:
        x += 2
    cx = 'x' if c == 1 else f'{c}x'
    return (f'Point B is between A and C. AB = {a}x + {b}, BC = {cx} - {d} and AC = {(a + c) * x + b - d}. Find x, then find AB.',
            str(a * x + b), [f'AB + BC = AC: {a}x + {b} + {cx} - {d} = {(a + c) * x + b - d}.', f'{a + c}x + {b - d} = {(a + c) * x + b - d}, so x = {x}.', f'AB = {a}({x}) + {b} = {a * x + b}.'])


@t('spatial-thinking', 2)
def _(r, nm):
    x = r.randint(8, 20); a, b = r.randint(2, 4), r.randint(5, 20)
    other = 180 - (a * x + b)
    while other <= 0:
        x -= 2; other = 180 - (a * x + b)
    return (f'Two angles form a linear pair. One measures ({a}x + {b})° and the other is {other}°. Find x, then find the measure of the angle vertical to the ({a}x + {b})° angle.',
            f'{a * x + b}°', [f'Linear pair: ({a}x + {b}) + {other} = 180.', f'{a}x = {180 - other - b}, so x = {x}.', f'The vertical angle has the same measure as ({a}x + {b})°: {a * x + b}°.'])


@t('spatial-thinking', 3)
def _(r, nm):
    n = r.choice([5, 6, 7, 8]); known = [r.randint(100, 150) for _ in range(n - 1)]
    S = (n - 2) * 180; miss = S - sum(known)
    while miss <= 0 or miss >= 360:
        known = [r.randint(100, 150) for _ in range(n - 1)]; miss = S - sum(known)
    return (f'A {n}-sided polygon has angles {", ".join(map(str, known))} degrees and one unknown angle. Find the sum of the interior angles, then the unknown angle.',
            f'{miss}°', [f'Sum = ({n} - 2) × 180 = {S}°.', f'Known angles add to {sum(known)}°.', f'Unknown = {S} - {sum(known)} = {miss}°.'])


@t('spatial-thinking', 4)
def _(r, nm):
    L, W, g = r.choice([24, 30, 36, 40]), r.choice([12, 15, 18, 20]), r.choice([3, 4, 6])
    while L % g or W % g:
        g = 3 if L % 3 == 0 and W % 3 == 0 else 2
    return (f'A rectangular yard is {L} ft by {W} ft. Fence posts go at every corner and every {g} ft along the sides. Draw a diagram. How many posts are needed?',
            str(2 * (L + W) // g), [f'Perimeter = 2({L} + {W}) = {2 * (L + W)} ft.', f'Around a closed loop, the number of posts equals the number of gaps: {2 * (L + W)} ÷ {g}.', f'= {2 * (L + W) // g} posts.'])


@t('spatial-thinking', 5)
def _(r, nm):
    x = r.randint(3, 9); a, b = r.randint(2, 4), r.randint(1, 6); s2, s3 = r.randint(8, 15), r.randint(9, 16)
    return (f'△ABC ≅ △DEF. AB = {a}x + {b}, DE = {a * x + b} and the other sides of △DEF are {s2} and {s3}. Find x, then find the perimeter of △ABC.',
            str(a * x + b + s2 + s3), [f'Corresponding sides are equal: {a}x + {b} = {a * x + b}, so x = {x}.', f'△ABC has the same side lengths: {a * x + b}, {s2} and {s3}.', f'Perimeter = {a * x + b + s2 + s3}.'])


@t('spatial-thinking', 6)
def _(r, nm):
    d, dist = r.choice([20, 24, 26, 28]), r.choice([500, 1000, 1200])
    C = Fr(314, 100) * d
    rev = Fr(dist * 12) / C
    return (f'A bike wheel has a diameter of {d} in. Use 3.14 for π. About how many full turns does the wheel make in {dist} ft?',
            str(int(rev)), [f'Circumference = πd ≈ 3.14 × {d} = {dz(C)} in.', f'{dist} ft = {dist * 12} in.', f'{dist * 12} ÷ {dz(C)} ≈ {dz(rev, 1)}, so {int(rev)} full turns.'])


@t('spatial-thinking', 7)
def _(r, nm):
    a, b = r.randint(6, 15), r.randint(8, 20)
    lo, hi = abs(a - b), a + b
    return (f'{nm} has sticks of {a} cm and {b} cm and wants a third stick to make a triangle. The third stick is a whole number of centimeters. What are the shortest and longest possible lengths? Give the sum of the two.',
            str(lo + 1 + hi - 1), [f'Triangle inequality: {lo} < x < {hi}.', f'Shortest whole length {lo + 1} cm; longest {hi - 1} cm.', f'Sum: {lo + 1} + {hi - 1} = {hi + lo}.'])


@t('spatial-thinking', 8)
def _(r, nm):
    x, y, a, b = r.randint(-6, 6), r.randint(-6, 6), r.choice([-5, -4, 3, 4, 6]), r.choice([-3, 2, 4, -6])
    return (f'Point P({x}, {y}) is translated {abs(a)} units {"right" if a > 0 else "left"} and then {abs(b)} units {"up" if b > 0 else "down"}. Then the image is translated back {abs(a)} units {"left" if a > 0 else "right"}. What are the final coordinates?',
            f'({x}, {y + b})', [f'First image: ({x + a}, {y + b}).', f'Moving back {abs(a)} units undoes the horizontal move.', f'Final: ({x}, {y + b}).'])


@t('spatial-thinking', 9)
def _(r, nm):
    n = r.choice([5, 6, 8, 9, 10, 12])
    return (f'A logo is a regular {n}-sided polygon. What is the smallest rotation (in degrees) that maps it onto itself, and how many rotations less than 360° do so? Give the smallest angle.',
            f'{360 // n}°' if 360 % n == 0 else f'{fs(Fr(360, n))}°', [f'A regular {n}-gon has rotational symmetry of order {n}.', f'Smallest angle = 360° ÷ {n} = {fs(Fr(360, n))}°.', f'{n - 1} rotations between 0° and 360° map it onto itself.'])


@t('spatial-thinking', 10)
def _(r, nm):
    x, y = r.randint(1, 8), -r.randint(1, 8)
    return (f'Point A({x}, {y}) is rotated 90° counterclockwise about the origin, and then the image is rotated another 90° counterclockwise. What are the final coordinates?',
            f'({-x}, {-y})', [f'90° counterclockwise: (x, y) → (-y, x), so A′ = ({-y}, {x}).', f'Again: ({-y}, {x}) → ({-x}, {-y}).', f'Two 90° turns make 180°: ({-x}, {-y}).'])


# ---------- Unit 10: Area and Volume ----------
@t('area-volume', 1)
def _(r, nm):
    b, h, c = r.choice([2.5, 3, 4.5]), r.choice([1.5, 2, 2.4]), r.choice([8, 12, 15])
    A = Fr(str(b)) * Fr(str(h))
    return (f'A parallelogram-shaped banner has base {b} m and height {h} m. Fabric costs ${c} per square meter. What does the fabric cost?',
            m(A * c), [f'A = bh = {b} × {h} = {dz(A)} m².', f'Cost = {dz(A)} × {c}.', f'= {m(A * c)}.'])


@t('area-volume', 2)
def _(r, nm):
    b1, b2, h, tb, th = r.randint(8, 14), r.randint(4, 7), r.randint(4, 8), r.randint(4, 8), r.randint(3, 6)
    A = Fr(b1 + b2, 2) * h + Fr(tb * th, 2)
    return (f'A garden is a trapezoid with bases {b1} m and {b2} m and height {h} m, plus a triangle with base {tb} m and height {th} m on one side. What is the total area?',
            f'{dz(A, 1)} m²', [f'Trapezoid: ({b1} + {b2})/2 × {h} = {dz(Fr(b1 + b2, 2) * h, 1)} m².', f'Triangle: ½ × {tb} × {th} = {dz(Fr(tb * th, 2), 1)} m².', f'Total = {dz(A, 1)} m².'])


@t('area-volume', 3)
def _(r, nm):
    R, rr = r.randint(5, 10), r.randint(2, 4)
    return (f'A circular patio has radius {R} ft with a circular fountain of radius {rr} ft in the center. What is the area of the patio around the fountain? Give the answer in terms of π.',
            f'{R * R - rr * rr}π ft²', [f'Big circle: π({R})² = {R * R}π.', f'Fountain: π({rr})² = {rr * rr}π.', f'Patio: {R * R}π - {rr * rr}π = {R * R - rr * rr}π ft².'])


@t('area-volume', 4)
def _(r, nm):
    l, w, h = r.randint(6, 12), r.randint(4, 9), r.randint(5, 10)
    return (f'A rectangular prism is {l} cm by {w} cm by {h} cm. One slice is parallel to the {l} cm by {w} cm base, and another is perpendicular to the base and parallel to the {l} cm edge. How much greater is the larger cross-section area than the smaller? Give the difference in cm².',
            f'{abs(l * w - l * h)} cm²', [f'Parallel slice: {l} × {w} = {l * w} cm².', f'Perpendicular slice: {l} × {h} = {l * h} cm².', f'Difference: {abs(l * w - l * h)} cm².'])


@t('area-volume', 5)
def _(r, nm):
    l, w, h, cov = r.randint(8, 14), r.randint(6, 10), r.randint(4, 8), r.choice([100, 120, 150])
    S = 2 * (l * w + l * h + w * h)
    return (f'A wooden chest is a rectangular prism {l} dm by {w} dm by {h} dm. One can of paint covers {cov} dm². How many cans are needed to paint the whole outside?',
            str(-(-S // cov)), [f'Surface area = 2({l}·{w} + {l}·{h} + {w}·{h}) = {S} dm².', f'{S} ÷ {cov} = {dz(Fr(S, cov), 2)}.', f'Round up: {-(-S // cov)} cans.'])


@t('area-volume', 6)
def _(r, nm):
    b, l, n = r.randint(4, 10), r.randint(6, 14), r.randint(3, 8)
    S = b * b + 2 * b * l
    return (f'A gift box is a square pyramid with base edge {b} cm and slant height {l} cm. How much paper covers {n} boxes completely, including the bases?',
            f'{S * n} cm²', [f'Base: {b}² = {b * b} cm²; 4 triangles: 4 × ½ × {b} × {l} = {2 * b * l} cm².', f'One box: {S} cm².', f'{n} boxes: {S * n} cm².'])


@t('area-volume', 7)
def _(r, nm):
    rr, h, rate = r.choice([2, 3, 4]), r.choice([5, 6, 8]), r.choice([2, 3, 4])
    V = Fr(314, 100) * rr * rr * h
    return (f'A cylinder-shaped tank has radius {rr} ft and height {h} ft. Use 3.14 for π. Water fills it at {rate} ft³ per minute. How many minutes does it take to fill, to the nearest tenth?',
            dz(V / rate, 1), [f'V = πr²h ≈ 3.14 × {rr}² × {h} = {dz(V)} ft³.', f'Time = {dz(V)} ÷ {rate}.', f'≈ {dz(V / rate, 1)} minutes.'])


@t('area-volume', 8)
def _(r, nm):
    rr, h = r.choice([2, 3, 4]), r.choice([6, 9, 12])
    return (f'A cone and a cylinder have the same radius {rr} cm and height {h} cm. How many full cones of water fill the cylinder, and what is the cylinder\'s volume in terms of π? Give the cylinder\'s volume.',
            f'{rr * rr * h}π cm³', [f'Cone: (1/3)π({rr})²({h}) = {fs(Fr(rr * rr * h, 3))}π cm³.', f'Cylinder: π({rr})²({h}) = {rr * rr * h}π cm³.', 'The cylinder holds exactly 3 cones.'])


# ---------- Unit 11: Right Triangles in Algebra ----------
@t('right-triangles-algebra', 1)
def _(r, nm):
    A = r.choice([45, 60, 75, 90, 120])
    s = math.sqrt(A)
    return (f'A square tile has area {A} in². Between which two whole numbers is its side? Find the side to the nearest tenth, then the perimeter to the nearest tenth. Give the perimeter.',
            dz(4 * Fr(round(s * 10), 10), 1), [f'{math.isqrt(A)}² = {math.isqrt(A) ** 2} and {math.isqrt(A) + 1}² = {(math.isqrt(A) + 1) ** 2}, so the side is between {math.isqrt(A)} and {math.isqrt(A) + 1}.',
                                                  f'√{A} ≈ {s:.1f} in.', f'Perimeter ≈ 4 × {s:.1f} = {dz(4 * Fr(round(s * 10), 10), 1)} in.'])


@t('right-triangles-algebra', 2)
def _(r, nm):
    a, b, c = r.choice([(6, 8, 10), (9, 12, 15), (5, 12, 13), (8, 15, 17)])
    up = r.choice([1, 2])
    return (f'A {c}-ft ladder leans against a wall with its base {a} ft from the wall. How high does it reach? If the base is moved {up} ft closer to the wall, how much higher does it reach, to the nearest tenth of a foot? Give the increase.',
            dz(Fr(round(math.sqrt(c * c - (a - up) ** 2) * 10), 10) - b, 1), [f'Height = √({c}² - {a}²) = {b} ft.', f'New height = √({c}² - {a - up}²) ≈ {math.sqrt(c * c - (a - up) ** 2):.1f} ft.', f'Increase ≈ {dz(Fr(round(math.sqrt(c * c - (a - up) ** 2) * 10), 10) - b, 1)} ft.'])


@t('right-triangles-algebra', 3)
def _(r, nm):
    x1, y1, dx, dy = r.randint(-5, 2), r.randint(-4, 3), r.choice([3, 6, 5, 8]), r.choice([4, 8, 12, 6])
    d = math.sqrt(dx * dx + dy * dy)
    return (f'On a map grid in blocks, {nm} walks from ({x1}, {y1}) to ({x1 + dx}, {y1 + dy}). Find the midpoint of the trip and the straight-line distance, to the nearest tenth of a block. Give the distance.',
            dz(Fr(round(d * 10), 10), 1), [f'Midpoint: ({fs(Fr(2 * x1 + dx, 2))}, {fs(Fr(2 * y1 + dy, 2))}).', f'Distance = √({dx}² + {dy}²) = √{dx * dx + dy * dy}.', f'≈ {dz(Fr(round(d * 10), 10), 1)} blocks.'])


@t('right-triangles-algebra', 4)
def _(r, nm):
    p, s, t2 = r.choice([5, 6]), r.choice([2, 3, 4]), r.randint(8, 24)
    return (f'{nm} is {p} ft tall and casts a {s}-ft shadow. At the same time, a flagpole casts a {t2}-ft shadow. Write and solve a proportion for the flagpole\'s height, then find how much taller the flagpole is than {nm}. Give the difference.',
            dz(Fr(p * t2, s) - p, 1), [f'{p}/{s} = h/{t2}.', f'h = {p} × {t2} ÷ {s} = {dz(Fr(p * t2, s), 1)} ft.', f'Difference: {dz(Fr(p * t2, s), 1)} - {p} = {dz(Fr(p * t2, s) - p, 1)} ft.'])


@t('right-triangles-algebra', 5)
def _(r, nm):
    s = r.randint(5, 15)
    return (f'A square park has sides of {s} m. A path runs along a diagonal. Using a 45°-45°-90° triangle, how much shorter is the diagonal path than walking along two sides, to the nearest tenth of a meter?',
            dz(Fr(round((2 * s - s * math.sqrt(2)) * 10), 10), 1), [f'Diagonal = {s}√2 ≈ {s * math.sqrt(2):.2f} m.', f'Two sides = {2 * s} m.', f'Difference ≈ {dz(Fr(round((2 * s - s * math.sqrt(2)) * 10), 10), 1)} m.'])


@t('right-triangles-algebra', 6)
def _(r, nm):
    ang, rise = r.choice([5, 6, 8, 10]), r.choice([2, 2.5, 3])
    L = rise / math.sin(math.radians(ang))
    return (f'A wheelchair ramp makes a {ang}° angle with the ground and rises {rise} ft. Use sine to find the length of the ramp to the nearest tenth of a foot.',
            dz(Fr(round(L * 10), 10), 1), [f'sin {ang}° = opposite/hypotenuse = {rise}/L.', f'L = {rise} ÷ sin {ang}° ≈ {rise} ÷ {math.sin(math.radians(ang)):.4f}.', f'≈ {dz(Fr(round(L * 10), 10), 1)} ft.'])


@t('right-triangles-algebra', 7)
def _(r, nm):
    d, a1, a2 = r.randint(60, 150), r.randint(25, 35), r.randint(40, 55)
    h1, h2 = d * math.tan(math.radians(a1)), d * math.tan(math.radians(a2))
    return (f'From {d} ft away, the angle of elevation to the top of a tower is {a2}°, and to a window on the tower it is {a1}°. How far is the window below the top, to the nearest foot?',
            str(round(h2 - h1)), [f'Top: {d} × tan {a2}° ≈ {h2:.1f} ft.', f'Window: {d} × tan {a1}° ≈ {h1:.1f} ft.', f'Difference ≈ {round(h2 - h1)} ft.'])


# ---------- Unit 12: Data Analysis and Probability ----------
@t('data-analysis-probability', 1)
def _(r, nm):
    f = [r.randint(2, 9) for _ in range(5)]
    return (f'A frequency table of reading minutes shows 0–9: {f[0]}, 10–19: {f[1]}, 20–29: {f[2]}, 30–39: {f[3]}, 40–49: {f[4]}. What percent of the students read at least 20 minutes, to the nearest whole percent?',
            f'{round(100 * sum(f[2:]) / sum(f))}%', [f'Total students: {sum(f)}.', f'At least 20 minutes: {f[2]} + {f[3]} + {f[4]} = {sum(f[2:])}.', f'{sum(f[2:])} ÷ {sum(f)} ≈ {round(100 * sum(f[2:]) / sum(f))}%.'])


@t('data-analysis-probability', 2)
def _(r, nm):
    A = sorted(r.sample(range(40, 100), 8)); B = sorted(r.sample(range(45, 100), 8))
    q = lambda d: (Fr(d[1] + d[2], 2), Fr(d[5] + d[6], 2))
    qa, qb = q(A), q(B)
    return (f'Class A scores: {", ".join(map(str, A))}. Class B scores: {", ".join(map(str, B))}. Find each IQR. How much greater is the larger IQR?',
            dz(abs((qa[1] - qa[0]) - (qb[1] - qb[0])), 1), [f'Class A: Q1 = {dz(qa[0], 1)}, Q3 = {dz(qa[1], 1)}, IQR = {dz(qa[1] - qa[0], 1)}.', f'Class B: Q1 = {dz(qb[0], 1)}, Q3 = {dz(qb[1], 1)}, IQR = {dz(qb[1] - qb[0], 1)}.', f'Difference: {dz(abs((qa[1] - qa[0]) - (qb[1] - qb[0])), 1)}.'])


@t('data-analysis-probability', 3)
def _(r, nm):
    d = sorted(r.sample(range(12, 69), 9))
    stems = {}
    for x in d:
        stems.setdefault(x // 10, []).append(x % 10)
    plot = '; '.join(f'{s} | {" ".join(map(str, v))}' for s, v in stems.items())
    return (f'The stem-and-leaf plot (key: 2 | 4 means 24) shows ages: {plot}. Find the median and the range. Give the median plus the range.',
            str(d[4] + d[-1] - d[0]), [f'Ordered values: {", ".join(map(str, d))}.', f'Median (5th of 9) = {d[4]}; range = {d[-1]} - {d[0]} = {d[-1] - d[0]}.', f'{d[4]} + {d[-1] - d[0]} = {d[4] + d[-1] - d[0]}.'])


@t('data-analysis-probability', 4)
def _(r, nm):
    s, p, sh = r.randint(3, 6), r.randint(2, 5), r.randint(2, 4)
    return (f'{nm} has {s} shirts, {p} pairs of pants and {sh} pairs of shoes. How many outfits are possible, and what is the probability that a random outfit uses one particular shirt? Give the number of outfits.',
            str(s * p * sh), [f'Counting principle: {s} × {p} × {sh}.', f'= {s * p * sh} outfits.', f'Each shirt appears in {p * sh} outfits, so P = {p * sh}/{s * p * sh} = 1/{s}.'])


@t('data-analysis-probability', 5)
def _(r, nm):
    g, b = r.randint(3, 7), r.randint(3, 7)
    tot = g + b
    pr_ = Fr(g, tot) * Fr(g - 1, tot - 1); pw = Fr(g, tot) ** 2
    return (f'A box has {g} green and {b} blue pens. Two pens are drawn. How much greater is P(green, green) when the first pen is replaced than when it is not? Write a fraction in simplest form.',
            fs(pw - pr_), [f'With replacement: ({g}/{tot})² = {fs(pw)}.', f'Without: {g}/{tot} × {g - 1}/{tot - 1} = {fs(pr_)}.', f'Difference: {fs(pw - pr_)}.'])


@t('data-analysis-probability', 6)
def _(r, nm):
    n, k = r.randint(6, 10), r.choice([2, 3])
    return (f'{n} students run for a club. First, {k} officers are chosen with different jobs (order matters). Separately, a {k}-person committee is chosen (order does not matter). How many more ways are there to choose the officers than the committee?',
            str(math.perm(n, k) - math.comb(n, k)), [f'Officers: {n}P{k} = {math.perm(n, k)}.', f'Committee: {n}C{k} = {math.comb(n, k)}.', f'Difference: {math.perm(n, k) - math.comb(n, k)}.'])


@t('data-analysis-probability', 7)
def _(r, nm):
    n, hits = r.choice([60, 80, 120]), None
    hits = n // 6 + r.choice([-4, 3, 6])
    return (f'A number cube was rolled {n} times and showed a 6 on {hits} rolls. Find the experimental probability of a 6 and the theoretical probability. How many more (or fewer) 6s came up than the theoretical expected number? Give actual minus expected.',
            str(hits - n // 6), [f'Experimental: {hits}/{n} = {fs(Fr(hits, n))}.', f'Theoretical: 1/6, so expected = {n} ÷ 6 = {n // 6}.', f'{hits} - {n // 6} = {hits - n // 6}.'])


@t('data-analysis-probability', 8)
def _(r, nm):
    s, yes, pop = r.choice([40, 50, 60]), None, r.choice([600, 900, 1200])
    yes = r.randint(int(s * 0.2), int(s * 0.6))
    return (f'In a random sample of {s} students, {yes} want a later start time. Predict how many of the school\'s {pop} students want a later start, then how many do not. Give the number who do not.',
            dz(pop - Fr(yes, s) * pop, 1), [f'Sample proportion: {yes}/{s} = {fs(Fr(yes, s))}.', f'Predicted yes: {fs(Fr(yes, s))} × {pop} = {dz(Fr(yes, s) * pop, 1)}.', f'Predicted no: {pop} - {dz(Fr(yes, s) * pop, 1)} = {dz(pop - Fr(yes, s) * pop, 1)}.'])


@t('data-analysis-probability', 9)
def _(r, nm):
    A = [r.randint(40, 60) for _ in range(6)]; shift = r.choice([10, 12, 15])
    B = [x + shift for x in A]
    mean = Fr(sum(A), 6); mad = sum(abs(Fr(x) - mean) for x in A) / 6
    return (f'Group A: {", ".join(map(str, A))}. Group B: {", ".join(map(str, B))}. Both groups have the same mean absolute deviation (MAD). Find the MAD and the difference of the means. The difference is how many MADs? Round to the nearest tenth.',
            dz(Fr(shift) / mad, 1), [f'Mean A = {dz(mean, 2)}; mean B = {dz(mean + shift, 2)}; difference = {shift}.', f'MAD = {dz(mad, 2)} (average distance from the mean).', f'{shift} ÷ {dz(mad, 2)} ≈ {dz(Fr(shift) / mad, 1)} MADs.'])


# ---------- Unit 13: Nonlinear Functions and Polynomials ----------
@t('nonlinear-functions-polynomials', 1)
def _(r, nm):
    a, d, n, s = r.randint(3, 12), r.randint(3, 8), r.randint(20, 40), None
    return (f'Seats in a theater form an arithmetic sequence: row 1 has {a} seats and each row has {d} more. How many seats are in row {n}, and how many in rows 1–{n} together? Give the total.',
            str(n * (2 * a + (n - 1) * d) // 2), [f'Row {n}: {a} + {d}({n} - 1) = {a + (n - 1) * d}.', f'Total = (first + last) × {n} ÷ 2.', f'= ({a} + {a + (n - 1) * d}) × {n} ÷ 2 = {n * (2 * a + (n - 1) * d) // 2}.'])


@t('nonlinear-functions-polynomials', 2)
def _(r, nm):
    k, x1, x2 = r.choice([2, 3, 4]), r.randint(2, 4), r.randint(5, 7)
    return (f'The area of a square garden is y = x², where x is the side in meters. How much does the area increase when the side grows from {x1} m to {x2} m? Is the change the same for each 1 m increase?',
            f'{x2 * x2 - x1 * x1} m²', [f'y({x1}) = {x1 * x1}, y({x2}) = {x2 * x2}.', f'Increase = {x2 * x2} - {x1 * x1} = {x2 * x2 - x1 * x1} m².', 'No: each 1 m increase adds more area than the last, so the function is nonlinear.'])


@t('nonlinear-functions-polynomials', 3)
def _(r, nm):
    p0, rt, y = r.choice([1200, 2500, 4000]), r.choice([6, 8, 10]), r.choice([3, 4, 5])
    v = p0 * (1 - rt / 100) ** y
    return (f'A car worth ${p0:,} loses {rt}% of its value each year. Write y = {p0}({1 - rt / 100:g})^t and find its value after {y} years, to the nearest dollar. Is this growth or decay?',
            f'${round(v):,}', [f'Decay factor: 1 - {rt / 100:g} = {1 - rt / 100:g} (less than 1, so decay).', f'y = {p0} × {1 - rt / 100:g}^{y} ≈ {v:.2f}.', f'≈ ${round(v):,}.'])


@t('nonlinear-functions-polynomials', 4)
def _(r, nm):
    a, b, c, t = r.choice([-16]), r.randint(40, 80), r.randint(4, 30), r.randint(1, 2)
    h = a * t * t + b * t + c
    return (f'A ball\'s height in feet after t seconds is h = {a}t² + {b}t + {c}. What is the degree of the polynomial, and what is the height at t = {t}? Give the height.',
            f'{h} ft', ['The highest power of t is 2, so the degree is 2.', f'h = {a}({t})² + {b}({t}) + {c}.', f'= {a * t * t} + {b * t} + {c} = {h} ft.'])


@t('nonlinear-functions-polynomials', 5)
def _(r, nm):
    a, b, c, d, x = r.randint(2, 5), r.randint(1, 9), r.randint(1, 4), r.randint(1, 8), r.randint(3, 8)
    return (f'A triangle has sides {a}x + {b}, {c}x - 1 and x + {d}. Write the perimeter as a polynomial, then find it when x = {x}.',
            str((a + c + 1) * x + b - 1 + d), [f'Add: ({a}x + {b}) + ({c}x - 1) + (x + {d}).', f'= {a + c + 1}x + {b - 1 + d}.', f'x = {x}: {a + c + 1}({x}) + {b - 1 + d} = {(a + c + 1) * x + b - 1 + d}.'])


@t('nonlinear-functions-polynomials', 6)
def _(r, nm):
    a, b, c, x = r.randint(2, 4), r.randint(1, 5), r.randint(1, 6), r.randint(2, 5)
    return (f'A rectangle has width {a}x and length x² + {b}x + {c}. Write its area as a polynomial, then find the area when x = {x}.',
            str(a * x ** 3 + a * b * x * x + a * c * x), [f'{a}x(x² + {b}x + {c}) = {a}x³ + {a * b}x² + {a * c}x.', f'x = {x}: {a}({x ** 3}) + {a * b}({x * x}) + {a * c}({x}).', f'= {a * x ** 3 + a * b * x * x + a * c * x}.'])


@t('nonlinear-functions-polynomials', 7)
def _(r, nm):
    s, a, b = r.randint(6, 12), r.randint(2, 4), r.randint(1, 3)
    return (f'A square photo has sides x inches. A frame adds {a} in. to the length and {b} in. to the width, making a (x + {a}) by (x + {b}) rectangle. Write the area as a polynomial, and find how much area the frame adds when x = {s}.',
            str((a + b) * s + a * b), [f'(x + {a})(x + {b}) = x² + {a + b}x + {a * b}.', f'Added area = (x² + {a + b}x + {a * b}) - x² = {a + b}x + {a * b}.', f'x = {s}: {a + b}({s}) + {a * b} = {(a + b) * s + a * b} in².'])


@t('nonlinear-functions-polynomials', 8)
def _(r, nm):
    q, dm = r.randint(5, 15), r.randint(5, 20)
    tot = 25 * q + 10 * dm
    return (f'A jar has {q + dm} quarters and dimes worth {m(Fr(tot, 100))}. Use an equation or a table to find the number of quarters.',
            str(q), [f'Let q be quarters: 25q + 10({q + dm} - q) = {tot}.', f'15q + {10 * (q + dm)} = {tot}, so 15q = {tot - 10 * (q + dm)}.', f'q = {q} quarters.'])


SUPD = str.maketrans('0123456789-t', '⁰¹²³⁴⁵⁶⁷⁸⁹⁻ᵗ')


def sup(s):
    s = s.replace('−', '-')
    s = re.sub(r'([a-z])\^1(?![\d])', r'\1', s)
    return re.sub(r'\^(\d+|[a-z])', lambda m: m.group(1).translate(SUPD) if m.group(1) != 'h' else 'ʰ', s)


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
    names = lib.skill_names()
    made = 0
    for (u, n), fn in sorted(T.items(), key=lambda kv: (lib.UNITS.index(kv[0][0]), kv[0][1])):
        sid = f'{u}-skill-{n:02d}'
        if (u, n) == ('algebraic-expressions-integers', 1):
            continue  # Place Value was rebuilt at grade level by place_value.py, with powers-of-ten contexts at Honors
        from collections import Counter
        std = list(Counter(tuple(q['standards']) for q in banks[u]['questions'] if q['skillId'] == sid and q['level'] == 'honors').most_common(1)[0][0])
        rng = random.Random(f'g7-honors-{sid}')
        qs = banks[u]['questions']
        last = max(i for i, x in enumerate(qs) if x['skillId'] == sid and x['level'] == 'honors')
        seen = set()
        for k in range(2):
            for _ in range(40):
                prompt, ans, steps = (sup(x) if isinstance(x, str) else [sup(y) for y in x] for x in fn(rng, N[(n * 3 + k * 7 + lib.UNITS.index(u)) % len(N)]))
                if prompt not in seen:
                    break
            seen.add(prompt)
            qid = f'pa7-{lib.ABBR[u]}-s{n:02d}-honors-h{k + 1:02d}'
            q = dict(id=qid, skillId=sid, level='honors', format='short-answer', prompt=prompt, answer=ans, solutionSteps=steps, standards=std,
                     sourceNotes=lib.SOURCE.format(fam=f'g7_honors_multistep_{lib.ABBR[u]}_s{n:02d}') + ' Teacher review pending.')
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
