"""3rd Grade Math audit #8 (2026-11-19): on-skill select-all items with 2, 3 or 4 correct choices.

Before the audit all 113 Grade 3 select-all items used one template ("Select ALL the problems that are matched with
the correct answer") and had exactly 2 of 4 correct. Each is rewritten in place (ID, skill and level kept) by a family
that picks its correct and wrong choices from the skill itself: 5 choices, with the number correct cycling 2, 3, 4."""
import random
from fractions import Fraction as Fr
from lib import UNITS, n
import fams
from fams import DNAME, Skip, need, rnd, tm

NOTE = ('Original Claude-authored item (family: {fam}). 3rd Grade Math audit 2026-11-19 (#8, select-all with {k} correct); '
        'every choice recomputed by scripts/test-grade3-audit.cjs.')
G = {}


def sel(unit, i):
    def d(f):
        G[f'{unit}-skill-{i:02d}'] = f; return f
    return d


def pick(r, good, bad, k):
    good, bad = list(dict.fromkeys(good)), [b for b in dict.fromkeys(bad) if b not in good]
    need(len(good) >= k and len(bad) >= 5 - k)
    return r.sample(good, k), r.sample(bad, 5 - k)


MM, DV, PF, UP, AS, UF, EC, TM, GD, AR, PS = fams.MM, fams.DV, fams.PF, fams.UP, fams.AS, fams.UF, fams.EC, fams.TM, fams.GD, fams.AR, fams.PS


@sel(AS, 1)
def s_as1(r, L, k):
    t = r.randint([2, 10, 40][L], [9, 40, 99][L]) * 10
    near = list(range(t - 9, t + 10))
    g, b = pick(r, [n(x) for x in near if rnd(x, 10) == t], [n(x) for x in near if rnd(x, 10) != t], k)
    return ('as1_select_rounds_to', f'Select ALL the numbers that round to {t} when rounded to the nearest 10.', g, b, [f'Numbers from {t - 5} to {t + 4} round to {t}.'])


@sel(AS, 2)
def s_as2(r, L, k):
    t = r.randint(2, 9) * 100
    near = list(range(t - 90, t + 91, 10)) + [t - 51, t + 51, t - 50, t + 49]
    g, b = pick(r, [n(x) for x in near if rnd(x, 100) == t], [n(x) for x in near if rnd(x, 100) != t], k)
    return ('as2_select_rounds_to', f'Select ALL the numbers that round to {t} when rounded to the nearest 100.', g, b, [f'Numbers from {t - 50} to {t + 49} round to {t}.'])


@sel(AS, 3)
def s_as3(r, L, k):
    t = r.randint([300, 500, 700][L], [450, 650, 950][L])
    xs = r.sample(range(100, t - 99), 8)
    good = [f'{a} + {t - a}' for a in xs[:4]]
    bad = [f'{a} + {t - a + r.choice([-10, 10, -100, 100, 1, -1])}' for a in xs[4:]]
    g, b = pick(r, good, bad, k)
    return ('as3_select_sum_equals', f'Select ALL the sums that equal {t}.', g, b, ['Add each pair and compare with ' + str(t) + '.'])


@sel(AS, 4)
def s_as4(r, L, k):
    t = r.randint([100, 200, 300][L], [300, 400, 600][L]); good, bad = [], []
    for _ in range(40):
        a = r.randint(t + 50, 999)
        good.append(f'{a} − {a - t}'); bad.append(f'{a} − {a - t + r.choice([-10, 10, -100, 100, 1])}')
    g, b = pick(r, good, [x for x in bad if eval(x.replace('−', '-')) != t], k)
    return ('as4_select_difference_equals', f'Select ALL the differences that equal {t}.', g, b, ['Subtract each pair and compare with ' + str(t) + '.'])


@sel(AS, 5)
def s_as5(r, L, k):
    good, bad = [], []
    for _ in range(60):
        a, b = r.randint(110, 480), r.randint(110, 480); s = a + b
        good.append(f'{a} + {b} = {s}'); bad.append(f'{a} + {b} = {s + r.choice([100, -100, 200])}')
    g, b = pick(r, good, bad, k)
    return ('as5_select_reasonable', 'Select ALL the sums that are correct. Round to the nearest 100 to spot the ones that are not reasonable.', g, b,
            ['A correct sum is close to the estimate; a sum that is 100 or more away from the exact answer is wrong.'])


@sel(AR, 1)
def s_ar1(r, L, k):
    t = r.randint([8, 12, 16][L], [12, 20, 30][L])
    good = [f'covered by {t} unit squares with no gaps or overlaps', f'{n(t)} unit squares in rows with no gaps'] + [f'{a} rows of {t // a} unit squares' for a in range(2, 7) if t % a == 0]
    bad = [f'covered by {t + 2} unit squares with no gaps or overlaps', f'covered by {t} unit squares with some overlaps', f'covered by {t - 1} unit squares with no gaps or overlaps', f'covered by {t} unit squares with a gap', f'{t} unit lengths around the edge']
    g, b = pick(r, good, bad, k)
    return ('ar1_select_area_equals', f'Select ALL the shapes that have an area of {t} square units.', g, b, ['Area counts the unit squares that cover a shape with no gaps or overlaps.'])


@sel(AR, 3)
def s_ar3(r, L, k):
    t = r.choice([[12, 16, 18, 20, 24], [24, 30, 36, 40], [36, 42, 48, 56, 60]][L])
    good = [f'{a} by {t // a}' for a in range(1, 11) if t % a == 0 and t // a <= 12]
    bad = [f'{a} by {b}' for a in range(2, 9) for b in range(2, 9) if a * b != t and abs(a * b - t) <= 6]
    g, b = pick(r, good, bad, k)
    return ('ar3_select_rectangle_area', f'Select ALL the rectangles (side lengths in feet) with an area of {t} square feet.', g, b, ['Multiply the side lengths of each rectangle.'])


@sel(DV, 1)
def s_dv1(r, L, k):
    e = r.randint(2, 9)
    good = [f'{g * e} shared by {g}' for g in range(2, 11) if g * e <= 100]
    bad = [f'{g * e + d} shared by {g}' for g in range(2, 10) for d in (1, 2) if (g * e + d) % g == 0 and (g * e + d) // g != e] + [f'{g * (e + 1)} shared by {g}' for g in range(2, 10)]
    g, b = pick(r, good, bad, k)
    return ('dv1_select_each_gets', f'Select ALL the ways to share where each person gets {e}.', g, b, [f'Divide the total by the number of people and look for {e}.'])


@sel(DV, 2)
def s_dv2(r, L, k):
    g0 = r.randint(2, 9)
    good = [f'{s * g0} in groups of {s}' for s in range(2, 11) if s * g0 <= 100]
    bad = [f'{s * (g0 + d)} in groups of {s}' for s in range(2, 11) for d in (-1, 1) if 0 < s * (g0 + d) <= 100]
    g, b = pick(r, good, bad, k)
    return ('dv2_select_number_of_groups', f'Select ALL the ways to make exactly {g0} groups.', g, b, [f'Divide the total by the group size and look for {g0}.'])


@sel(DV, 3)
def s_dv3(r, L, k):
    a, b = r.randint(3, 9), r.randint(3, 9); need(a != b); p = a * b
    good = [f'{a} × {b} = {p}', f'{b} × {a} = {p}', f'{p} ÷ {a} = {b}', f'{p} ÷ {b} = {a}']
    bad = [f'{a} × {p} = {b}', f'{a} ÷ {p} = {b}', f'{a} + {b} = {p}', f'{p} − {a} = {b}', f'{b} ÷ {a} = {p}']
    g, bb = pick(r, good, bad, k)
    return ('dv3_select_fact_family', f'Select ALL the equations in the fact family for {a}, {b} and {p}.', g, bb, [f'A fact family uses {a} × {b} = {p} and the related facts.'])


@sel(DV, 4)
def s_dv4(r, L, k):
    e = r.randint(3, 9); good, bad = [], []
    for g in range(2, 10):
        if g * e <= 100:
            good.append(f'{g * e} seeds in {g} equal rows')
            bad.append(f'{g * e + g} seeds in {g} equal rows')
    g, b = pick(r, good, [x for x in bad if x not in good], k)
    return ('dv4_select_rows_of', f'Select ALL the gardens that have {e} seeds in each row.', g, b, [f'Divide the seeds by the rows and look for {e}.'])


@sel(EC, 2)
def s_ec2(r, L, k):
    a, b = r.choice([(1, 2), (1, 4), (3, 4), (1, 3), (2, 3)])
    good = [f'{a * m}/{b * m}' for m in (1, 2, 3, 4) if b * m <= 8 and b * m in (2, 3, 4, 6, 8)] + [f'{a * 2}/{b * 2}']
    bad = [f'{a + 1}/{b + 1}', f'{a}/{b * 2}', f'{a * 2}/{b}', f'{a + 2}/{b + 2}', f'{a + 1}/{b * 2}', f'{b - a}/{b}' if b - a != a else f'{a + 1}/{b}']
    g, bb = pick(r, good, [x for x in bad if Fr(*map(int, x.split('/'))) != Fr(a, b)], k)
    return ('ec2_select_equivalent', f'Select ALL the fractions equal to {a}/{b}.', g, bb, [f'Multiply the top and bottom of {a}/{b} by the same number.'])


@sel(EC, 3)
def s_ec3(r, L, k):
    w = r.randint(1, 4)
    good = [f'{w * d}/{d}' for d in (1, 2, 3, 4, 6, 8)]
    bad = [f'{w * d + 1}/{d}' for d in (2, 3, 4, 6)] + [f'{w}/{d}' for d in (2, 3, 4) if w != d * w] + [f'{d}/{w * d}' for d in (2, 3)]
    g, b = pick(r, good, [x for x in bad if Fr(*map(int, x.split('/'))) != w], k)
    return ('ec3_select_equal_whole', f'Select ALL the fractions equal to {w}.', g, b, [f'A fraction equals {w} when the numerator is {w} times the denominator.'])


@sel(EC, 4)
def s_ec4(r, L, k):
    d = r.choice([4, 6, 8]); t = r.randint(2, d - 2)
    good = [f'{x}/{d}' for x in range(t + 1, d + 2)]; bad = [f'{x}/{d}' for x in range(1, t + 1)]
    g, b = pick(r, good, bad, k)
    return ('ec4_select_greater_same_den', f'Select ALL the fractions greater than {t}/{d}.', g, b, [f'Same denominator: compare the numerators with {t}.'])


@sel(EC, 5)
def s_ec5(r, L, k):
    a = r.randint(1, 3); d = r.choice([x for x in (3, 4, 6) if x > a])
    good = [f'{a}/{x}' for x in (2, 3, 4, 6, 8) if x < d and x >= a] + [f'{a}/{a}'] * 0
    bad = [f'{a}/{x}' for x in (2, 3, 4, 6, 8) if x >= d and x >= a]
    good += [f'{a + 1}/{x}' for x in (2, 3, 4) if x < d and Fr(a + 1, x) > Fr(a, d)]
    g, b = pick(r, good, bad + [f'{a}/{d * 2}' if d * 2 <= 8 else f'{a}/8'], k)
    return ('ec5_select_greater_same_num', f'Select ALL the fractions greater than {a}/{d}.', g, b, [f'With the same numerator, fewer parts means bigger parts.'])


@sel(GD, 3)
def s_gd3(r, L, k):
    s = [2, 5, 10][L]
    good = [str(s * m) for m in range(1, 10)]; bad = [str(s * m + d) for m in range(1, 8) for d in (1, s // 2 if s > 2 else 3) if (s * m + d) % s]
    g, b = pick(r, good, bad, k)
    return ('gd3_select_whole_symbols', f'Each symbol in a picture graph stands for {s}. Select ALL the numbers you can show with whole symbols only.', g, b, [f'A number can be shown with whole symbols when it is a multiple of {s}.'])


@sel(MM, 1)
def s_mm1(r, L, k):
    g0, e = r.randint(2, 6), r.randint(2, 9); need(g0 != e)
    good = [f'{g0} groups of {e}', f'{g0} × {e}', ' + '.join([str(e)] * g0), f'{e} × {g0}']
    bad = [f'{g0} + {e}', f'{e} groups of {g0 + 1}', ' + '.join([str(g0)] * (e - 1)) if e > 2 else f'{g0} × {e + 1}', f'{g0} groups of {e + 1}', f'{g0 * e} groups of {e}']
    g, b = pick(r, good, bad, k)
    return ('mm1_select_same_total', f'Select ALL that show {g0 * e} as equal groups.', g, b, [f'{g0} groups of {e} is {g0} × {e} = {g0 * e}.'])


@sel(MM, 2)
def s_mm2(r, L, k):
    t = r.choice([12, 16, 18, 20, 24, 30, 36])
    good = [f'{a} rows of {t // a}' for a in range(2, 10) if t % a == 0 and t // a <= 12]
    bad = [f'{a} rows of {b}' for a in range(2, 8) for b in range(2, 8) if a * b != t and abs(a * b - t) <= 4]
    g, b = pick(r, good, bad, k)
    return ('mm2_select_array_total', f'Select ALL the arrays that have {t} tiles.', g, b, ['Multiply rows by the number in each row.'])


@sel(MM, 3)
def s_mm3(r, L, k):
    f = r.choice([2, 5, 10])
    good = [str(f * m) for m in range(2, 11)]
    bad = [str(f * m + d) for m in range(2, 10) for d in (1, 3) if (f * m + d) % f]
    g, b = pick(r, good, bad, k)
    return ('mm3_select_products_of', f'Select ALL the numbers that are products of {f} (that is, {f} × a whole number).', g, b, [{2: 'Products of 2 are even.', 5: 'Products of 5 end in 0 or 5.', 10: 'Products of 10 end in 0.'}[f]])


@sel(MM, 4)
def s_mm4(r, L, k):
    t = r.choice([24, 36, 40, 48])
    good = [f'{a} boxes of {t // a} crayons' for a in range(2, 10) if t % a == 0 and t // a <= 12]
    bad = [f'{a} boxes of {b} crayons' for a in range(2, 9) for b in range(2, 9) if a * b != t and abs(a * b - t) <= 5]
    g, b = pick(r, good, bad, k)
    return ('mm4_select_total_crayons', f'Select ALL the orders that have {t} crayons in all.', g, b, ['Multiply the boxes by the crayons in each box.'])


@sel(UP, 1)
def s_up1(r, L, k):
    x = r.randint(3, 9)
    good = [f'{a} × ? = {a * x}' for a in range(2, 10)] + [f'{a * x} ÷ ? = {a}' for a in range(2, 10)]
    bad = [f'{a} × ? = {a * (x + 1)}' for a in range(2, 10)] + [f'{a * (x - 1)} ÷ ? = {a}' for a in range(2, 10)]
    g, b = pick(r, good, bad, k)
    return ('up1_select_unknown_is', f'Select ALL the equations where the unknown ? is {x}.', g, b, [f'Put {x} in place of ? and check each equation.'])


@sel(UP, 2)
def s_up2(r, L, k):
    t, g0 = r.choice([(24, 6), (24, 4), (36, 6), (36, 4), (40, 8), (30, 5)]); e = t // g0
    good = [f'{g0} × {e} = {t}', f'{t} ÷ {g0} = {e}', f'{e} × {g0} = {t}', f'{t} ÷ {e} = {g0}']
    bad = [f'{t} + {g0} = {t + g0}', f'{t} − {g0} = {t - g0}', f'{t} × {g0} = {t * g0}', f'{g0} + {e} = {g0 + e}']
    gg, b = pick(r, good, bad, k)
    return ('up2_select_story_equation', f'{t} students sit in {g0} equal rows. Select ALL the equations that match the story.', gg, b, [f'There are {g0} groups of {e}: {g0} × {e} = {t}.'])


@sel(UP, 3)
def s_up3(r, L, k):
    t = r.choice([120, 160, 180, 240, 280, 360, 420])
    good = [f'{a} × {t // a}' for a in range(2, 10) if t % a == 0 and (t // a) % 10 == 0 and t // a <= 90]
    bad = [f'{a} × {t // a + 10}' for a in range(2, 10) if t % a == 0 and (t // a) % 10 == 0] + [f'{a} × {t // a - 10}' for a in range(2, 10) if t % a == 0 and (t // a) % 10 == 0 and t // a > 10]
    g, b = pick(r, good, bad, k)
    return ('up3_select_tens_product', f'Select ALL the products equal to {t}.', g, b, [f'Think in tens: {t} is {t // 10} tens.'])


@sel(UP, 5)
def s_up5(r, L, k):
    k0, e, s = r.randint(3, 6), r.randint(3, 8), r.randint(2, 9)
    good = [f'{k0} × {e} − {s}', f'({k0} × {e}) − {s}', f'{e} × {k0} − {s}']
    bad = [f'{k0} + {e} − {s}', f'{k0} × ({e} − {s})' if e > s else f'{k0} × {e} + {s}', f'{s} − {k0} × {e}', f'{k0} × {e} + {s}', f'{k0} × {s} − {e}']
    good += [f'{k0 * e} − {s}']
    g, b = pick(r, good, [x for x in bad if x not in good], k)
    return ('up5_select_expression', f'A baker makes {k0} trays of {e} rolls and sells {s}. Select ALL the expressions for the rolls left.', g, b, [f'Multiply to find the rolls made, then subtract {s}.'])


@sel(UP, 6)
def s_up6(r, L, k):
    good, bad = [], []
    for _ in range(40):
        a, b = r.randint(10, 60), r.randint(10, 60); good.append(f'{a} + {b} is about {rnd(a, 10) + rnd(b, 10)}'); bad.append(f'{a} + {b} is about {rnd(a, 10) + rnd(b, 10) + r.choice([20, -20, 30])}')
    g, b = pick(r, good, bad, k)
    return ('up6_select_estimate', 'Round each number to the nearest 10. Select ALL the estimates that are correct.', g, b, ['Round each number to the nearest 10, then add.'])


@sel(PS, 1)
def s_ps1(r, L, k):
    p = r.choice([16, 20, 24, 28])
    good = [f'{a} by {p // 2 - a} rectangle' for a in range(1, p // 4 + 1)] + [f'square with {p // 4}-unit sides']
    bad = [f'{a} by {p // 2 - a + 1} rectangle' for a in range(1, 5)] + [f'square with {p // 4 + 1}-unit sides']
    g, b = pick(r, good, bad, k)
    return ('ps1_select_perimeter', f'Select ALL the shapes with a perimeter of {p} units.', g, b, ['Add all the side lengths of each shape.'])


@sel(PS, 2)
def s_ps2(r, L, k):
    P = r.choice([20, 24, 30]); good, bad = [], []
    for _ in range(60):
        a, b, c = r.randint(3, 9), r.randint(3, 9), r.randint(3, 9); d = P - a - b - c
        if d > 1:
            good.append(f'sides {a}, {b}, {c}; missing side {d}'); bad.append(f'sides {a}, {b}, {c}; missing side {d + r.choice([1, 2, -1])}')
    g, b = pick(r, good, bad, k)
    return ('ps2_select_missing_side', f'Each shape has 4 sides and a perimeter of {P} units. Select ALL the choices where the missing side is correct.', g, b, [f'The missing side is {P} minus the three known sides.'])


@sel(PS, 4)
def s_ps4(r, L, k):
    shape = r.choice(['square', 'rectangle', 'rhombus'])
    names = {'square': ['quadrilateral', 'rectangle', 'rhombus', 'parallelogram'], 'rectangle': ['quadrilateral', 'parallelogram', 'shape with 4 right angles'],
             'rhombus': ['quadrilateral', 'parallelogram', 'shape with 4 equal sides']}[shape]
    other = ['triangle', 'pentagon', 'hexagon', 'shape with 3 sides', 'trapezoid that is not a parallelogram', 'rhombus' if shape == 'rectangle' else 'rectangle' if shape == 'rhombus' else 'octagon']
    need(len(names) >= k)
    g, b = pick(r, names, [x for x in other if x not in names], k)
    return ('ps4_select_names', f'Select ALL the names that always describe a {shape}.', g, b, [f'A {shape} is a quadrilateral; check each name against its sides and angles.'])


@sel(PF, 1)
def s_pf1(r, L, k):
    a, b = r.randint(3, 9), r.randint(3, 9); need(a != b)
    good = [f'{b} × {a}', f'{a} × {b}', f'{a * b} × 1', f'1 × {a * b}']
    bad = [f'{a} + {b}', f'{b} × {a + 1}', f'{a * b} × 0', f'{a} × {b} × 0', f'{b} + {a} + {a}']
    g, bb = pick(r, good, bad, k)
    return ('pf1_select_same_product', f'Select ALL the expressions equal to {a} × {b}.', g, bb, [f'{a} × {b} = {a * b}; the order of the factors does not change the product.'])


@sel(PF, 2)
def s_pf2(r, L, k):
    a, b, c = r.randint(2, 5), r.randint(2, 5), r.randint(2, 5); v = a * b * c
    good = [f'({a} × {b}) × {c}', f'{a} × ({b} × {c})', f'({a} × {c}) × {b}', f'{a * b} × {c}', f'{a} × {b * c}']
    bad = [f'({a} + {b}) × {c}', f'{a} × {b} + {c}', f'{a * b} + {c}', f'{a} × ({b} + {c})', f'{a + b + c}']
    g, bb = pick(r, good, [x for x in bad if eval(x.replace('×', '*')) != v], k)
    return ('pf2_select_associative', f'Select ALL the expressions equal to {a} × {b} × {c}.', g, bb, [f'{a} × {b} × {c} = {v}; you can group the factors in any order.'])


@sel(PF, 3)
def s_pf3(r, L, k):
    a, b = r.randint(3, 9), r.randint(6, 9)
    good = [f'({a} × {s}) + ({a} × {b - s})' for s in range(1, b)]
    bad = [f'({a} × {s}) + ({a} × {b - s + 1})' for s in range(1, b - 1)] + [f'({a} + {s}) × {b - s}' for s in (2, 3)]
    g, bb = pick(r, good, [x for x in bad if eval(x.replace('×', '*')) != a * b], k)
    return ('pf3_select_break_apart', f'Select ALL the expressions equal to {a} × {b}.', g, bb, [f'Break {b} into two parts that add to {b}; multiply each by {a} and add.'])


@sel(PF, 4)
def s_pf4(r, L, k):
    a = r.randint(2, 9)
    good = [f'{a} × 1', f'1 × {a}', f'{a} ÷ 1', f'{a} + 0', f'{a} × 1 × 1']
    bad = [f'{a} × 0', f'0 ÷ {a}', f'{a} − {a}', f'{a} + 1', f'0 × {a}']
    g, bb = pick(r, good, bad, k)
    return ('pf4_select_equals_number', f'Select ALL the expressions equal to {a}.', g, bb, ['Any number times 1 or divided by 1 is that number; any number times 0 is 0.'])


@sel(PF, 5)
def s_pf5(r, L, k):
    t = r.choice([24, 36, 48, 42, 56, 54, 63, 72])
    good = [f'{a} × {t // a}' for a in range(3, 10) if t % a == 0 and t // a <= 10]
    bad = [f'{a} × {b}' for a in range(3, 10) for b in range(3, 10) if a * b != t and abs(a * b - t) <= 4]
    g, b = pick(r, good, bad, k)
    return ('pf5_select_fact_product', f'Select ALL the facts with a product of {t}.', g, b, ['Multiply each fact.'])


@sel(TM, 1)
def s_tm1(r, L, k):
    h, m = r.randint(1, 11), r.randint(10, 50); t0 = h * 60 + m
    good = [tm(t0 + d) for d in range(1, 15)]
    bad = [tm(t0 - d) for d in range(0, 10)] + [tm(t0 + d) for d in range(20, 60, 5)]
    g, b = pick(r, good, bad, k)
    return ('tm1_select_after_within', f'Select ALL the times that are later than {tm(t0)} but less than 15 minutes later.', g, b, [f'Count on from {tm(t0)}; {tm(t0 + 14)} is the latest.'])


@sel(TM, 2)
def s_tm2(r, L, k):
    d = r.choice([15, 20, 25, 30, 35, 40, 45]); good, bad = [], []
    for h in range(1, 12):
        m = r.randint(0, 55); s = h * 60 + m
        good.append(f'{tm(s)} to {tm(s + d)}'); bad.append(f'{tm(s)} to {tm(s + d + r.choice([5, 10, -5]))}')
    g, b = pick(r, good, bad, k)
    return ('tm2_select_elapsed', f'Select ALL the time spans that are exactly {d} minutes long.', g, b, ['Count the minutes from the start time to the end time.'])


@sel(TM, 5)
def s_tm5(r, L, k):
    t = r.choice([24, 30, 36, 40]); good = [f'{a} buckets of {t // a} liters' for a in range(2, 10) if t % a == 0 and t // a <= 12]
    bad = [f'{a} buckets of {b} liters' for a in range(2, 8) for b in range(2, 8) if a * b != t and abs(a * b - t) <= 4]
    g, b = pick(r, good, bad, k)
    return ('tm5_select_total_liters', f'Select ALL the ways to hold exactly {t} liters of water.', g, b, ['Multiply the buckets by the liters in each bucket.'])


@sel(UF, 1)
def s_uf1(r, L, k):
    d = r.choice([3, 4, 6, 8])
    good = [f'1 of {d} equal parts', f'one {fams.UNIT1[d]} of a whole', f'1 part when a whole is cut into {d} equal parts', f'1 of {d} equal slices']
    bad = [f'1 of {d} unequal parts', f'1 of {d + 1} equal parts', f'{d} of 1 equal part', f'2 of {d} equal parts', f'1 of {d - 1} equal parts']
    g, b = pick(r, good, bad, k)
    return ('uf1_select_unit_fraction', f'Select ALL that show 1/{d}.', g, b, [f'1/{d} is one of {d} equal parts of a whole.'])


@sel(UF, 2)
def s_uf2(r, L, k):
    d = r.choice([4, 6, 8]); a = r.randint(2, d - 1)
    good = [f'{a} copies of 1/{d}', ' + '.join([f'1/{d}'] * a) if a <= 4 else f'{a} × 1/{d}', f'{a} × 1/{d}', f'{a}/{d}']
    bad = [f'{a} copies of 1/{d + 1}' if d + 1 in (4, 6, 8) else f'{a + 1} copies of 1/{d}', f'{a - 1} copies of 1/{d}', f'{d} copies of 1/{a}', f'1/{a}', f'{a} copies of {d}']
    g, b = pick(r, list(dict.fromkeys(good)), bad, k)
    return ('uf2_select_copies', f'Select ALL that are equal to {a}/{d}.', g, b, [f'{a}/{d} is {a} copies of 1/{d}.'])


@sel(UF, 4)
def s_uf4(r, L, k):
    d = r.choice([2, 3, 4, 6, 8])
    good = [f'{x}/{d}' for x in range(d + 1, 3 * d)]; bad = [f'{x}/{d}' for x in range(1, d + 1)]
    g, b = pick(r, good, bad, k)
    return ('uf4_select_past_one', f'A number line from 0 to 3 is marked in {DNAME[d]}. Select ALL the fractions that are past 1.', g, b, [f'1 = {d}/{d}; a fraction is past 1 when its numerator is more than {d}.'])


def run(o):
    i = 0
    for u in UNITS:
        for skill in sorted({q['skillId'] for q in o.items(u)}):
            old = sorted([q for q in o.items(u) if q['skillId'] == skill and q['format'] == 'select-all'], key=lambda q: q['id'])
            if not old:
                continue
            if skill not in G:
                raise SystemExit('no select-all family for ' + skill)
            for q in old:
                li = ['cp2', 'cp1', 'honors'].index(q['level'])
                k = 2 + (i % 3); i += 1
                r = random.Random(f'g3-sel|{q["id"]}')
                for _ in range(2000):
                    try:
                        fam, prompt, good, bad, steps = G[skill](r, li, k)
                        break
                    except (Skip, ValueError, IndexError, ZeroDivisionError):
                        continue
                else:
                    raise SystemExit('no select-all item for ' + skill)
                opts = [{'text': t, 'correct': True} for t in good] + [{'text': t, 'correct': False} for t in bad]
                r.shuffle(opts)
                ans = [x['text'] for x in opts if x['correct']]
                steps = steps + ['Correct choices: ' + '; '.join(ans) + '. Not correct: ' + '; '.join(bad) + '.']
                o.edit(q['id'], prompt=prompt, answer=ans, options=opts, solutionSteps=steps, sourceNotes=NOTE.format(fam=fam, k=k))
                o.meta_set(q['id'], questionType='conceptual', tags=['select-all'], explanation=steps[0])
