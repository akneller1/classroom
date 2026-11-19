"""Grade 7 audit #4–#10 and #13 (2026-11-19): new items for the standards the bank did not really practice, with
figures where the problem is about a picture. Items are appended to their skill with ids pa7-<unit>-sNN-<level>-gNN.
  #4  7.G.A.2   triangles from given conditions: triangle inequality, how many triangles   (Constructions)
  #5  7.G.A.3   cross-sections of prisms, pyramids, cylinders and cones, with figures       (Space Figures)
  #6  7.RP.A.2  proportional relationships on graphs: test, k, meaning of (x, y) and (1, r),
      8.EE.B.5  and comparing two proportional relationships, with figures                   (Tables)
  #7  7.G.B.5   equations for unknown angles: vertical, adjacent, linear pair, with figures  (Angle Relationships)
  #8  7.RP.A.3  percent error, commission, tip with tax, successive percent changes
  #9  7.NS.A.1a opposites make 0; 7.NS.A.2c properties with rational numbers; 7.SP.C.8c simulations
  #10 8.G.A.3–4 dilations; 8.SP.A.4 two-way tables; 8.F.A.2 comparing functions; 8.F.B.5 qualitative graphs;
      8.EE.C.8c system word problems; 8.SP.A.2 judging a line of fit
Every answer is computed here and re-checked by verify_keys.py. Idempotent: earlier g-items are replaced."""
import os, random, re, sys
from fractions import Fraction as Fr
sys.path.insert(0, os.path.dirname(__file__))
import lib, figures

ASSETS = os.path.join(lib.ROOT, 'question-banks', 'assets', 'prealgebra7')
LV = ('cp2', 'cp1', 'honors')
NAMES = ['Maya', 'Leo', 'Priya', 'Diego', 'Ana', 'Owen', 'Nia', 'Raj', 'Zoe', 'Sam', 'Lena', 'Kai']


def fs(x):
    """Fraction or number as text: 5/2 → '5/2', 2.0 → '2', 2.5 → '2.5'."""
    if isinstance(x, Fr):
        return str(x.numerator) if x.denominator == 1 else f'{x.numerator}/{x.denominator}'
    return f'{x:g}' if isinstance(x, float) else str(x)


def dec(x):
    """Terminating fraction as a decimal (27/2 → '13.5'); other fractions stay as a/b."""
    x = Fr(x)
    d = x.denominator
    while d % 2 == 0:
        d //= 2
    while d % 5 == 0:
        d //= 5
    if d != 1:
        return fs(x)
    s = f'{float(x):.6f}'.rstrip('0').rstrip('.')
    return s


def money(x):
    return f'${x:,.2f}'


def half_up(x, places=2):
    q = Fr(10) ** places
    v = Fr(x) * q
    return Fr(int(v + Fr(1, 2)) if v >= 0 else -int(-v + Fr(1, 2)), 1) / q


class Out:
    def __init__(self):
        self.items = []

    def add(self, unit, skill, lv, fmt, prompt, answer, steps, std, tags, fam, wrong=None, fig=None, rng=None):
        h = lambda x: x.replace('−', '-')
        prompt, answer, steps, wrong = h(prompt), h(answer), [h(x) for x in steps], [h(w) for w in (wrong or [])]
        q = dict(skillId=f'{unit}-skill-{skill:02d}', level=lv, format=fmt, prompt=prompt, answer=answer, solutionSteps=steps,
                 standards=std, sourceNotes=lib.SOURCE.format(fam=fam) + ' Teacher review pending.')
        if fmt == 'multiple-choice':
            opts = [answer] + [w for w in wrong if w != answer][:3]
            assert len(set(opts)) == 4, (prompt, opts)
            rng.shuffle(opts)
            q['options'] = [{'text': t, 'correct': t == answer} for t in opts]
        self.items.append((unit, skill, lv, q, tags, fig))


def tri_ineq(o, rng):
    u, sk = 'spatial-thinking', 7
    for lv in LV:
        for k in range(2):
            if lv == 'cp2':
                a, b = rng.randint(3, 9), rng.randint(4, 12)
                c = rng.choice([a + b + rng.randint(1, 4), abs(a - b) + rng.randint(1, min(a, b) * 2 - 1)])
                s = sorted([a, b, c]); ok = s[0] + s[1] > s[2]
                o.add(u, sk, lv, 'short-answer', f'Can segments of length {a} cm, {b} cm and {c} cm form a triangle? Answer yes or no.', 'Yes' if ok else 'No',
                      ['Triangle inequality: the two shorter sides must add to more than the longest side.', f'{s[0]} + {s[1]} = {s[0] + s[1]}, and the longest side is {s[2]}.',
                       f'{s[0] + s[1]} {">" if ok else "≤"} {s[2]}, so {"yes" if ok else "no"}.'], ['7.G.A.2'], ['reasoning'], 'g7_triangle_inequality')
            elif lv == 'cp1':
                a, b = rng.randint(4, 10), rng.randint(5, 13)
                lo, hi = abs(a - b), a + b
                good = rng.randint(lo + 1, hi - 1)
                o.add(u, sk, lv, 'multiple-choice', f'Two sides of a triangle are {a} in. and {b} in. Which could be the length of the third side?', f'{good} in.',
                      [f'The third side must be more than {b} − {a} = {lo} and less than {a} + {b} = {hi}.' if b >= a else f'The third side must be more than {a} − {b} = {lo} and less than {a} + {b} = {hi}.',
                       f'Only {good} in. is between {lo} and {hi}.'], ['7.G.A.2'], ['reasoning'], 'g7_triangle_third_side',
                      wrong=[f'{hi} in.', f'{hi + rng.randint(1, 5)} in.', f'{lo} in.' if lo > 0 else '0 in.'], rng=rng)
            else:
                a, b = rng.randint(5, 12), rng.randint(6, 15)
                lo, hi = abs(a - b), a + b
                n = hi - lo - 1
                o.add(u, sk, lv, 'short-answer', f'Two sides of a triangle are {a} m and {b} m. The third side is a whole number of meters. How many different lengths are possible for the third side?',
                      str(n), [f'The third side x must satisfy {lo} < x < {hi}.', f'The whole numbers from {lo + 1} to {hi - 1}: {hi - 1} − {lo + 1} + 1 = {n}.', f'{n} lengths.'],
                      ['7.G.A.2'], ['multistep', 'reasoning'], 'g7_triangle_count')
    conds = {
        'cp2': [('three angles that measure 40°, 60° and 80°', 'more than one triangle', 'The angles add to 180°, so a triangle exists, but the same angles fit triangles of many sizes.'),
                ('three angles that measure 50°, 60° and 80°', 'no triangle', 'The angles add to 190°, not 180°, so no triangle has these angles.')],
        'cp1': [('sides of 5 cm, 7 cm and 9 cm', 'exactly one triangle', '5 + 7 > 9, so a triangle exists, and three given sides fix its shape and size (SSS).'),
                ('sides of 3 cm, 4 cm and 8 cm', 'no triangle', '3 + 4 = 7 is less than 8, so the sides cannot meet.')],
        'honors': [('two sides of 6 cm and 8 cm with a 50° angle between them', 'exactly one triangle', 'Two sides and the included angle fix the triangle (SAS).'),
                   ('angles of 95° and 90°', 'no triangle', '95° + 90° = 185° is already more than 180°.')],
    }
    for lv in LV:
        for c, ans, why in conds[lv]:
            o.add(u, sk, lv, 'multiple-choice', f'How many triangles can be drawn with {c}?', ans, [why, f'Answer: {ans}.'], ['7.G.A.2'], ['reasoning'], 'g7_how_many_triangles',
                  wrong=[x for x in ('no triangle', 'exactly one triangle', 'more than one triangle', 'exactly two triangles') if x != ans], rng=rng)


SHAPE = {('prism', 'parallel'): 'rectangle', ('prism', 'perpendicular'): 'rectangle', ('pyramid', 'parallel'): 'square',
         ('pyramid', 'perpendicular'): 'triangle', ('cylinder', 'parallel'): 'circle', ('cylinder', 'perpendicular'): 'rectangle',
         ('cone', 'parallel'): 'circle', ('cone', 'perpendicular'): 'triangle'}
NAME = {'prism': 'rectangular prism', 'pyramid': 'square pyramid', 'cylinder': 'cylinder', 'cone': 'cone'}


def cross_sections(o, rng):
    u, sk = 'area-volume', 4
    plan = {'cp2': [('prism', 'parallel'), ('cylinder', 'parallel'), ('cone', 'parallel')],
            'cp1': [('pyramid', 'perpendicular'), ('cylinder', 'perpendicular'), ('pyramid', 'parallel')],
            'honors': [('cone', 'perpendicular'), ('prism', 'perpendicular')]}
    for lv in LV:
        for solid, cut in plan[lv]:
            how = 'parallel to its base' if cut == 'parallel' else 'perpendicular to its base' + (' through its top vertex' if solid in ('pyramid', 'cone') else ' through its center')
            ans = SHAPE[(solid, cut)]
            o.add(u, sk, lv, 'multiple-choice', f'The figure shows a {NAME[solid]} sliced by a plane {how}. What shape is the cross-section?', ans,
                  [f'A slice {how.split(" through")[0]} of a {NAME[solid]} cuts {"a copy of the base" if cut == "parallel" else "through the height"}.', f'The cross-section is a {ans}.'],
                  ['7.G.A.3'], ['multiple-representations'], 'g7_cross_section_shape',
                  wrong=[x for x in ('rectangle', 'triangle', 'circle', 'square', 'trapezoid') if x != ans][:3], rng=rng, fig=('slice', solid, cut))
    for lv, k in (('cp1', 1), ('honors', 2)):
        for _ in range(k):
            l, w, h = rng.randint(4, 12), rng.randint(3, 9), rng.randint(6, 15)
            o.add(u, sk, lv, 'short-answer', f'A rectangular prism is {l} cm long, {w} cm wide and {h} cm tall. It is sliced parallel to its {l} cm by {w} cm base. What is the area of the cross-section?',
                  f'{l * w} cm²', ['A slice parallel to the base is a rectangle the same size as the base.', f'Area = {l} × {w} = {l * w} cm².'], ['7.G.A.3', '7.G.B.6'], ['multistep'], 'g7_cross_section_area')
    r, h = rng.randint(2, 6), rng.randint(5, 12)
    o.add(u, sk, 'honors', 'short-answer', f'A cylinder has radius {r} cm and height {h} cm. It is sliced perpendicular to its base through the center of the base. What is the area of the cross-section?',
          f'{2 * r * h} cm²', ['The cross-section is a rectangle whose width is the diameter and whose height is the height of the cylinder.', f'Width = 2 × {r} = {2 * r} cm.', f'Area = {2 * r} × {h} = {2 * r * h} cm².'],
          ['7.G.A.3'], ['multistep'], 'g7_cross_section_area')


def prop_graphs(o, rng):
    u, sk = 'ratios-proportions-percentages', 10
    ctx = [('hours', 'miles', Fr(5, 2), 8, 20, 2), ('pounds', 'cost ($)', Fr(3), 8, 24, 4), ('minutes', 'pages', Fr(3, 2), 8, 12, 2), ('days', 'inches of growth', Fr(1, 2), 8, 4, 1)]
    for lv in LV:
        for k in range(2):
            xl, yl, kk, xm, ym, ys = ctx[(LV.index(lv) * 2 + k) % 4]
            x2 = 4 if (kk * 4).denominator == 1 else 2
            if lv == 'cp2' and k == 0:
                start = rng.choice([0, ys])
                pts = [(0, start), (x2, start + kk * x2)]
                prop = start == 0
                o.add(u, sk, lv, 'short-answer', f'Does the graph show a proportional relationship between {xl} and {yl}? Answer yes or no.', 'Yes' if prop else 'No',
                      ['A proportional relationship graphs as a straight line through the origin (0, 0).', f'This line {"passes through" if prop else "crosses the y-axis at (0, " + fs(start) + "), not"} the origin.', 'Yes.' if prop else 'No.'],
                      ['7.RP.A.2a'], ['multiple-representations'], 'g7_prop_graph_test', fig=('line', pts, xm, ym, xl, yl, ys, [(x2, float(start + kk * x2))]))
            elif lv == 'cp2' or (lv == 'cp1' and k == 0):
                pts = [(0, 0), (x2, kk * x2)]
                o.add(u, sk, lv, 'short-answer', f'The graph shows a proportional relationship between {xl} (x) and {yl} (y). What is the constant of proportionality?', fs(kk),
                      ['The constant of proportionality is k = y/x for any point on the line other than the origin.', f'Use ({x2}, {fs(kk * x2)}): k = {fs(kk * x2)}/{x2} = {fs(kk)}.'],
                      ['7.RP.A.2b'], ['multiple-representations'], 'g7_prop_graph_k', fig=('line', pts, xm, ym, xl, yl, ys, [(x2, float(kk * x2))]))
            elif lv == 'cp1':
                pts = [(0, 0), (x2, kk * x2)]
                ans = f'In {x2} {xl}, the {yl.replace(" ($)", "")} is {fs(kk * x2)}' + (' dollars.' if '$' in yl else '.')
                wrong = [f'In {fs(kk * x2)} {xl}, the {yl.replace(" ($)", "")} is {x2}' + (' dollars.' if '$' in yl else '.'),
                         f'The unit rate is {x2}.', f'The unit rate is {fs(kk * x2)}.']
                o.add(u, sk, lv, 'multiple-choice', f'The graph shows a proportional relationship between {xl} (x) and {yl} (y). What does the point ({x2}, {fs(kk * x2)}) mean?', ans,
                      ['A point (x, y) pairs an amount of x with the matching amount of y.', f'x = {x2} {xl} and y = {fs(kk * x2)}.', 'The unit rate is the y-value at x = 1, which is ' + fs(kk) + '.'],
                      ['7.RP.A.2d'], ['multiple-representations'], 'g7_prop_graph_point', wrong=wrong, rng=rng, fig=('line', pts, xm, ym, xl, yl, ys, [(x2, float(kk * x2))]))
            else:
                ka = kk; kb = kk + rng.choice([Fr(1, 2), Fr(1), Fr(3, 2)])
                pts = [(0, 0), (x2, ka * x2)]
                diff = kb - ka
                o.add(u, sk, lv, 'short-answer', f'The graph shows {yl.replace(" ($)", "")} for Plan A over {xl}. Plan B is described by y = {dec(kb)}x. How much greater is Plan B\'s unit rate than Plan A\'s? Give the difference in {yl.replace("cost ($)", "dollars").replace("inches of growth", "inches")} per {xl[:-1] if xl.endswith("s") else xl}.',
                      dec(diff), [f'Plan A: from the point ({x2}, {dec(ka * x2)}), k = {dec(ka * x2)}/{x2} = {dec(ka)}.', f'Plan B: k = {dec(kb)} (the coefficient in y = kx).', f'{dec(kb)} − {dec(ka)} = {dec(diff)}.'],
                      ['8.EE.B.5', '7.RP.A.2b'], ['multistep', 'multiple-representations'], 'g7_prop_compare', fig=('line', pts, xm, ym, xl, yl, ys, [(x2, float(ka * x2))]))
    for lv in ('cp1', 'honors'):
        xl, yl, kk = rng.choice([('tickets', 'cost', Fr(15, 2)), ('gallons', 'miles', Fr(28)), ('hours', 'earnings', Fr(27, 2))])
        o.add(u, sk, lv, 'short-answer', f'A proportional relationship between {xl} x and {yl} y passes through the point (1, {dec(kk)}). Write an equation for the relationship.', f'y = {dec(kk)}x',
              ['The point (1, r) shows the unit rate r.', f'k = {dec(kk)}, so y = {dec(kk)}x.'], ['7.RP.A.2c', '7.RP.A.2d'], ['multiple-representations'], 'g7_prop_equation')


def angle_eqs(o, rng):
    u, sk = 'spatial-thinking', 2
    for lv in LV:
        for kind in ('vertical', 'right', 'linear'):
            if kind == 'vertical':
                x = rng.randint(8, 25); a, c = rng.choice([(3, 5), (2, 4), (4, 7), (6, 4)]); b = rng.randint(5, 30)
                d = a * x + b - c * x
                L, R = f'({a}x + {b})°', f'({c}x {"+" if d >= 0 else "−"} {abs(d)})°'
                eq = f'{a}x + {b} = {c}x {"+" if d >= 0 else "-"} {abs(d)}'; ang = a * x + b
                why = 'Vertical angles are congruent, so set the expressions equal.'
            elif kind == 'right':
                x = rng.randint(10, 25); a, b = rng.choice([(2, 1), (1, 2), (3, 1)]); c = rng.randint(0, 15)
                while a * x + b * x + c >= 90:
                    x -= 1
                c = 90 - a * x - b * x
                L, R = f'({a}x)°' if a > 1 else '(x)°', f'({b}x + {c})°' if b > 1 else f'(x + {c})°'
                eq = f'{a}x + {b}x + {c} = 90'; ang = max(a * x, b * x + c)
                why = 'The two adjacent angles make a right angle, so they are complementary: their sum is 90°.'
            else:
                x = rng.randint(15, 30); a, b = rng.choice([(4, 2), (3, 2), (5, 1)]); c = 180 - (a + b) * x
                if c <= 0:
                    x = 20; c = 180 - (a + b) * x
                L, R = f'({a}x)°', f'({b}x + {c})°'
                eq = f'{a}x + {b}x + {c} = 180'; ang = max(a * x, b * x + c)
                why = 'The two adjacent angles form a straight line, so they are supplementary: their sum is 180°.'
            if lv == 'cp2' and kind == 'linear':
                continue
            if lv == 'honors':
                prompt, ans = f'Use the figure. Find the measure of the larger angle.' if kind != 'vertical' else 'Use the figure. Find the measure of each angle.', f'{ang}°'
                steps = [why, f'{eq}.', f'x = {x}.', f'Substitute: the {"angle" if kind == "vertical" else "larger angle"} measures {ang}°.']
            else:
                prompt, ans = 'Use the figure. Find the value of x.', f'x = {x}'
                steps = [why, f'{eq}.', f'x = {x}.']
            o.add(u, sk, lv, 'short-answer', prompt, ans, steps, ['7.G.B.5', '7.EE.B.4a'], ['multistep'] if lv == 'honors' else [], 'g7_angle_equation',
                  fig=('angles', kind, [L, R]))


def percents(o, rng):
    u = 'ratios-proportions-percentages'
    PE = {'cp2': [('the number of students at a game', 180, 200), ('the number of pages in a book', 330, 300), ('the number of cars in a lot', 45, 50)],
          'cp1': [('the length of a hallway in meters', 12.6, 12), ('the mass of a backpack in kilograms', 4.5, 5), ('the time to walk to school in minutes', 13.5, 15)],
          'honors': [('the height of a tree in meters', 7.5, 7.2), ('the length of a kayak in meters', 3.9, 4.2), ('the time to run a mile in minutes', 8.25, 7.75)]}
    used_sales = rng.sample([(2400, 5), (850, 8), (12500, 3), (3600, 6.5), (980, 12)], 3)
    for lv in LV:
        for k, (item, est, act) in enumerate(rng.sample(PE[lv], 2)):
            err = abs(Fr(str(est)) - Fr(str(act))) / Fr(str(act)) * 100
            exact = err.denominator == 1 or dec(err) != fs(err)
            ans = dec(err) + '%' if (exact and len(dec(err)) <= 5) else dec(half_up(err, 1)) + '%'
            rnd = '' if ans == dec(err) + '%' else ' Round to the nearest tenth of a percent.'
            o.add(u, 8, lv, 'short-answer', f'{NAMES[k + 2 * LV.index(lv)]} estimated {item} as {est:g}. The actual value is {act:g}. What is the percent error?{rnd}',
                  ans, ['Percent error = (difference between the estimate and the actual value) ÷ actual × 100%.', f'|{est:g} − {act:g}| = {dec(abs(Fr(str(est)) - Fr(str(act))))}.',
                        f'{dec(abs(Fr(str(est)) - Fr(str(act))))} ÷ {act:g} × 100% = {ans}.'], ['7.RP.A.3'], ['connections'], 'g7_percent_error')
        sales, rate = used_sales[LV.index(lv)]
        pay = Fr(sales) * Fr(str(rate)) / 100
        if lv == 'honors':
            base = rng.choice([300, 450, 500])
            o.add(u, 7, lv, 'short-answer', f'A salesperson earns ${base} per week plus {"an" if str(rate).startswith("8") or str(rate).startswith("11") else "a"} {rate:g}% commission on sales. One week the sales are {money(sales)}. What are the total earnings?',
                  money(base + pay), [f'Commission = {rate:g}% of {money(sales)} = {Fr(str(rate)) / 100} × {sales} = {money(pay)}.', f'Total = {money(base)} + {money(pay)} = {money(base + pay)}.'],
                  ['7.RP.A.3'], ['connections', 'multistep'], 'g7_commission')
        else:
            o.add(u, 7, lv, 'short-answer', f'A salesperson earns {"an" if str(rate).startswith("8") or str(rate).startswith("11") else "a"} {rate:g}% commission on sales of {money(sales)}. How much commission is earned?', money(pay),
                  [f'Commission = {rate:g}% of {money(sales)}.', f'{rate:g}% = {fs(Fr(str(rate)) / 100)}, and {fs(Fr(str(rate)) / 100)} × {sales} = {money(pay)}.'], ['7.RP.A.3'], ['connections'], 'g7_commission')
        bill, tip, tax = rng.choice([(48, 20, 6), (36.5, 15, 5), (82, 18, 6.25), (24, 20, 7)])
        if lv == 'cp2':
            t = half_up(Fr(str(bill)) * tip / 100)
            o.add(u, 9, lv, 'short-answer', f'A meal costs {money(bill)}. You leave a {tip}% tip on the cost of the meal. How much is the tip?', money(t),
                  [f'Tip = {tip}% of {money(bill)} = {Fr(tip, 100)} × {bill:g}.', f'= {money(t)}.'], ['7.RP.A.3'], ['connections'], 'g7_tip')
        else:
            tx = half_up(Fr(str(bill)) * Fr(str(tax)) / 100); tp = half_up(Fr(str(bill)) * tip / 100); tot = Fr(str(bill)) + tx + tp
            o.add(u, 9, lv, 'short-answer', f'A meal costs {money(bill)} before tax. The sales tax is {tax:g}% and the tip is {tip}% of the cost before tax. What is the total, to the nearest cent?', money(tot),
                  [f'Tax = {tax:g}% of {money(bill)} = {money(tx)}.', f'Tip = {tip}% of {money(bill)} = {money(tp)}.', f'Total = {money(bill)} + {money(tx)} + {money(tp)} = {money(tot)}.'],
                  ['7.RP.A.3'], ['connections', 'multistep'], 'g7_tip_tax')
    for lv, (p1, p2) in (('cp1', (20, 20)), ('honors', (25, 20)), ('honors', (10, 10))):
        price = rng.choice([40, 60, 80, 120, 150])
        after = Fr(price) * (100 + p1) / 100 * (100 - p2) / 100
        ch = (after - price) / price * 100
        word = 'increase' if ch > 0 else 'decrease' if ch < 0 else 'no change'
        ans = f'{fs(abs(ch))}% {word}' if ch else 'no change'
        o.add(u, 8, lv, 'short-answer', f'A {money(price)} jacket\'s price is raised {p1}%. Later the new price is lowered {p2}%. What is the overall percent change from {money(price)}? Say whether it is an increase or a decrease.',
              ans, [f'After the {p1}% increase: {money(price)} × {fs(Fr(100 + p1, 100))} = {money(Fr(price) * (100 + p1) / 100)}.', f'After the {p2}% decrease: × {fs(Fr(100 - p2, 100))} = {money(after)}.',
                    f'Change = {money(after)} − {money(price)} = {money(after - price)}; {money(abs(after - price))} ÷ {money(price)} = {fs(abs(ch))}%.', f'{ans}. The percents do not cancel because they are taken of different amounts.'],
              ['7.RP.A.3'], ['multistep', 'misconception'], 'g7_successive_percent')


def number_sense(o, rng):
    u = 'algebraic-expressions-integers'
    ctxs = [('A hiker climbs {a} ft up a trail and then walks {a} ft back down.', 'What is the hiker\'s net change in elevation, in feet?'),
            ('An atom has {a} protons, each with a charge of +1, and {a} electrons, each with a charge of -1.', 'What is the total charge of the atom?'),
            ('A store adds ${a} to a gift card and later takes ${a} off the card.', 'What is the net change in the card\'s balance, in dollars?')]
    for i, lv in enumerate(LV):
        a = rng.randint(6, 30) if i == 1 else rng.randint(40, 400)
        c, q = ctxs[i]
        o.add(u, 6, lv, 'short-answer', c.format(a=a) + ' ' + q, '0', [f'The two changes are {a} and -{a}, which are opposites.', f'{a} + (-{a}) = 0: opposites combine to make 0.'],
              ['7.NS.A.1a', '7.NS.A.1b'], ['connections'], 'g7_opposites_zero')
    for lv, (expr, steps, val) in (('cp2', ('-4 × (2.5 + 0.25)', ['Distributive property: -4 × 2.5 + (-4) × 0.25.', '= -10 + (-1) = -11.'], '-11')),
                                   ('cp1', ('-8 × 0.25 × (-5)', ['Commutative and associative properties: (-8 × (-5)) × 0.25.', '= 40 × 0.25 = 10.'], '10')),
                                   ('honors', ('(-3/4) × 12 + (-3/4) × (-8)', ['Distributive property in reverse: (-3/4) × (12 + (-8)).', '= (-3/4) × 4 = -3.'], '-3'))):
        o.add(u, 11, lv, 'short-answer', f'Use properties of operations to evaluate {expr}.', val, steps, ['7.NS.A.2c', '7.NS.A.2'], ['reasoning'], 'g7_rational_properties')
    u = 'data-analysis-probability'
    sims = {'cp2': ('A basketball player makes 50% of her free throws. Which simulation could estimate the probability that she makes both of her next 2 free throws?',
                    'Flip a coin twice, with heads for a make, and repeat many times.', ['Roll a number cube once and count a 1 or 2 as two makes.', 'Flip a coin once and count heads as two makes.', 'Ask her teammates to guess.']),
            'cp1': ('Each cereal box holds 1 of 6 different prizes, equally likely. Which simulation could estimate the probability of getting at least 2 different prizes in 3 boxes?',
                    'Roll a number cube 3 times, with each number standing for one prize, and repeat many times.', ['Roll a number cube once.', 'Flip a coin 3 times, with heads for a new prize.', 'Spin a spinner with 3 equal sections 6 times.']),
            'honors': ('About 30% of a town\'s adults have a library card. Which simulation could estimate the probability that at least 2 of 4 randomly chosen adults have a card?',
                       'Use random digits 0–9, with 0, 1 and 2 meaning "has a card"; take 4 digits per trial and repeat many times.',
                       ['Use random digits 0–9, with 0, 1 and 2 meaning "has a card"; take 1 digit per trial.', 'Flip a coin 4 times per trial, with heads meaning "has a card."', 'Roll a number cube 4 times, with 1, 2 and 3 meaning "has a card."'])}
    for lv, (p, ans, wrong) in sims.items():
        o.add(u, 7, lv, 'multiple-choice', p, ans, ['A simulation must give each outcome the right probability and use one random draw per person or trial in the event.', f'{ans}'],
              ['7.SP.C.8c'], ['reasoning'], 'g7_design_simulation', wrong=wrong, rng=rng)


def grade8(o, rng):
    # 8.G.A.3–4 dilations (Similar Figures and Scale Drawings)
    u = 'ratios-proportions-percentages'
    for lv in LV:
        x, y = rng.randint(1, 6), rng.randint(1, 6)
        if lv == 'cp2':
            k = rng.choice([2, 3])
            o.add(u, 3, lv, 'short-answer', f'Point A({x}, {y}) is dilated by a scale factor of {k} with the center of dilation at the origin. What are the coordinates of A′?', f'({k * x}, {k * y})',
                  [f'A dilation centered at the origin multiplies both coordinates by the scale factor: (x, y) → ({k}x, {k}y).', f'A′ = ({k} × {x}, {k} × {y}) = ({k * x}, {k * y}).'], ['8.G.A.3'], [], 'g7_dilation_point')
        elif lv == 'cp1':
            k = Fr(rng.choice([1, 3]), 2) if rng.random() < 0.5 else Fr(1, 2)
            x, y = 2 * x, 2 * y
            o.add(u, 3, lv, 'short-answer', f'Point B({x}, {y}) is dilated by a scale factor of {fs(k)} with the center of dilation at the origin. What are the coordinates of B′?', f'({fs(k * x)}, {fs(k * y)})',
                  [f'Multiply both coordinates by {fs(k)}.', f'B′ = ({fs(k * x)}, {fs(k * y)}).', 'A scale factor less than 1 reduces the figure; greater than 1 enlarges it.'], ['8.G.A.3'], [], 'g7_dilation_point')
        else:
            k = Fr(rng.choice([3, 5]), 2)
            x, y = 2 * x, 2 * y
            o.add(u, 3, lv, 'short-answer', f'A dilation centered at the origin maps P({x}, {y}) to P′({fs(k * x)}, {fs(k * y)}). What is the scale factor?', fs(k),
                  ['Each image coordinate is the scale factor times the original coordinate.', f'{fs(k * x)} ÷ {x} = {fs(k)}, and {fs(k * y)} ÷ {y} = {fs(k)}.', f'Scale factor = {fs(k)}.'], ['8.G.A.3', '8.G.A.4'], ['reasoning'], 'g7_dilation_factor')
    for lv in ('cp1', 'honors'):
        a, b = rng.choice([(4, 6), (3, 5), (6, 8)]); k = Fr(rng.choice([3, 5, 7]), 2)
        c, d = k * a, k * b
        sim = lv == 'cp1' or rng.random() < 0.5
        if not sim:
            d = d + 1
        ans = (f'Yes; scale factor {dec(k)}' if sim else 'No')
        o.add(u, 3, lv, 'multiple-choice', f'Rectangle R is {a} cm by {b} cm. Rectangle S is {dec(c)} cm by {dec(d)} cm. Is S the image of R under a dilation?', ans,
              ['A dilation multiplies every length by the same scale factor.', f'{dec(c)} ÷ {a} = {dec(c / a)} and {dec(d)} ÷ {b} = {dec(d / b)}.', 'The ratios are equal.' if sim else 'The ratios are not equal, so S is not a dilation of R.'],
              ['8.G.A.4'], ['reasoning'], 'g7_dilation_similar', wrong=[x for x in (f'Yes; scale factor {dec(k)}', 'No', f'Yes; scale factor {fs(1 / k)}', f'Yes; scale factor {dec(c - a)}') if x != ans], rng=rng)
    # 8.SP.A.4 two-way tables (Frequency Tables)
    u = 'data-analysis-probability'
    for lv in LV:
        a, b, c, d = rng.randint(12, 40), rng.randint(8, 30), rng.randint(10, 35), rng.randint(15, 45)
        table = f'Two-way table of grade and lunch choice: 7th grade: {a} hot lunch, {b} packed lunch. 8th grade: {c} hot lunch, {d} packed lunch.'
        if lv == 'cp2':
            o.add(u, 1, lv, 'short-answer', table + ' How many students chose hot lunch in all?', str(a + c), ['Add the hot-lunch column.', f'{a} + {c} = {a + c}.'], ['8.SP.A.4'], ['multiple-representations'], 'g7_two_way_total')
        elif lv == 'cp1':
            f = Fr(a, a + b)
            o.add(u, 1, lv, 'short-answer', table + ' What fraction of the 7th graders chose hot lunch? Write a fraction in simplest form.', fs(f),
                  ['Use the 7th grade row only.', f'{a} of the {a + b} 7th graders chose hot lunch.', f'{a}/{a + b} = {fs(f)}.'], ['8.SP.A.4'], ['multiple-representations'], 'g7_two_way_row')
        else:
            p7, p8 = Fr(a, a + b), Fr(c, c + d)
            more = '7th graders' if p7 > p8 else '8th graders'
            hi, lo = (p7, p8) if p7 > p8 else (p8, p7)
            o.add(u, 1, lv, 'short-answer', table + ' Which grade has the greater relative frequency of hot lunch, and by how many percentage points? Round to the nearest whole percent first.',
                  f'{more}, by {int(half_up(hi * 100, 0)) - int(half_up(lo * 100, 0))} percentage points',
                  [f'7th grade: {a}/{a + b} ≈ {int(half_up(p7 * 100, 0))}%.', f'8th grade: {c}/{c + d} ≈ {int(half_up(p8 * 100, 0))}%.', f'{more} choose hot lunch more often, by {int(half_up(hi * 100, 0)) - int(half_up(lo * 100, 0))} percentage points.'],
                  ['8.SP.A.4'], ['multistep', 'multiple-representations'], 'g7_two_way_compare')
    # 8.F.A.2 comparing functions (Writing Rules for Linear Functions)
    u = 'linear-functions-graphing'
    for lv in LV:
        m1, b1 = rng.randint(2, 6), rng.randint(1, 9)
        m2 = m1 + rng.choice([-2, -1, 1, 2]); b2 = rng.randint(0, 9)
        xs = [0, 1, 2, 3]
        tab = ', '.join(f'({x}, {m2 * x + b2})' for x in xs)
        if lv == 'cp2':
            o.add(u, 4, lv, 'short-answer', f'Function A is y = {m1}x + {b1}. Function B has these (x, y) pairs: {tab}. What is the rate of change of Function B?', str(m2),
                  ['Rate of change = change in y ÷ change in x.', f'From (0, {b2}) to (1, {m2 + b2}): {m2} ÷ 1 = {m2}.'], ['8.F.A.2', '8.F.B.4'], ['multiple-representations'], 'g7_compare_rate')
        else:
            big = 'Function A' if m1 > m2 else 'Function B'
            ans = f'{big}, by {abs(m1 - m2)}'
            o.add(u, 4, lv, 'multiple-choice', f'Function A is y = {m1}x + {b1}. Function B has these (x, y) pairs: {tab}. Which function has the greater rate of change, and by how much?', ans,
                  [f'Function A: rate of change {m1} (the coefficient of x).', f'Function B: ({m2 + b2} − {b2}) ÷ 1 = {m2}.', f'{big} is greater by {abs(m1 - m2)}.'],
                  ['8.F.A.2'], ['multiple-representations'], 'g7_compare_functions',
                  wrong=[f'{"Function B" if big == "Function A" else "Function A"}, by {abs(m1 - m2)}', f'{big}, by {abs(b1 - b2) or abs(m1 - m2) + 1}', 'They have the same rate of change'], rng=rng)
    # 8.F.B.5 qualitative graphs (Relations and Functions)
    stories = [([(2, 2), (2, 0), (1, -2)], 'distance from home', 'Ana rides her bike away from home at a steady speed, stops at a friend\'s house for a while, then rides straight home faster.'),
               ([(1, 2.5), (2, 0.8), (2, 0)], 'height of a plant', 'A plant grows quickly at first, then grows more slowly, then stops growing.'),
               ([(2, 0), (1, -1.5), (2, 1.5)], 'water in a tank', 'The water level stays the same, drops when a valve is opened, then slowly rises back as the tank is refilled.')]
    wrongs = ['Ana rides her bike away from home, then rides home without stopping.', 'A plant grows slowly at first, then quickly.',
              'The water level rises steadily the whole time.', 'The speed stays the same the whole time.']
    for lv, (segs, yl, story) in zip(LV, stories):
        o.add(u, 1, lv, 'multiple-choice', 'Which situation best matches the graph?', story, ['Read the graph from left to right: rising means increasing, level means no change, falling means decreasing.', 'Steeper pieces show faster change.', story],
              ['8.F.B.5'], ['multiple-representations'], 'g7_qualitative_graph', wrong=[w for w in wrongs if w != story][:3], rng=rng, fig=('story', segs, yl))
    # 8.EE.C.8c system word problems (Substitution)
    for lv in LV:
        if lv == 'cp2':
            a = rng.randint(12, 30); b = rng.randint(5, 20)
            o.add(u, 7, lv, 'short-answer', f'The sum of two numbers is {a + b} and their difference is {a - b}. Write and solve a system to find the greater number.', str(a),
                  [f'x + y = {a + b} and x − y = {a - b}.', f'Substitute x = y + {a - b}: 2y + {a - b} = {a + b}, so y = {b}.', f'x = {a}.'], ['8.EE.C.8c', '8.EE.C.8b'], ['multistep'], 'g7_system_numbers')
        elif lv == 'cp1':
            fa, fb = rng.choice([(40, 25), (30, 20), (50, 35)]); ra, rb = rng.choice([(5, 8), (6, 9), (4, 7)])
            while (fa - fb) % (rb - ra):
                fa += 1
            n = (fa - fb) // (rb - ra)
            o.add(u, 7, lv, 'short-answer', f'Gym A charges ${fa} to join plus ${ra} per class. Gym B charges ${fb} to join plus ${rb} per class. After how many classes do the two gyms cost the same?', str(n),
                  [f'y = {fa} + {ra}x and y = {fb} + {rb}x.', f'Substitute: {fa} + {ra}x = {fb} + {rb}x, so {fa - fb} = {rb - ra}x.', f'x = {n} classes.'], ['8.EE.C.8c', '8.EE.C.8b'], ['multistep', 'connections'], 'g7_system_plans')
        else:
            n = rng.randint(20, 40); big = rng.randint(6, n - 6); pa, pb = rng.choice([(12, 8), (15, 9), (10, 6)])
            o.add(u, 7, lv, 'short-answer', f'A club sold {n} T-shirts and hats for ${pa * big + pb * (n - big)}. T-shirts cost ${pa} and hats cost ${pb}. Write and solve a system to find how many T-shirts were sold.', str(big),
                  [f't + h = {n} and {pa}t + {pb}h = {pa * big + pb * (n - big)}.', f'Substitute h = {n} − t: {pa}t + {pb}({n} − t) = {pa * big + pb * (n - big)}.', f'{pa - pb}t = {pa * big + pb * (n - big) - pb * n}, so t = {big}.'],
                  ['8.EE.C.8c', '8.EE.C.8b'], ['multistep', 'connections'], 'g7_system_mixture')
    # 8.SP.A.2 judging a line of fit (Scatter Plots)
    fits = {'cp2': ('Which line is the best fit for a scatter plot of 10 points?', 'A line with about half the points above it and half below, close to all of them.',
                    ['A line through the first and last points only.', 'A line with all 10 points above it.', 'A horizontal line through the highest point.']),
            'cp1': ('A trend line for a scatter plot has 8 points above it and 1 point below it. What is the best way to improve the fit?', 'Move the line up so the points are more balanced above and below.',
                    ['Move the line down.', 'Keep the line: a good fit can have most points on one side.', 'Remove the point below the line.']),
            'honors': ('Two trend lines are drawn for the same scatter plot. Line P has 5 points above and 5 below, mostly far from the line. Line Q has 4 above and 5 below, all close to the line. Which is the better fit?',
                       'Line Q, because the points are balanced and close to it.', ['Line P, because it has exactly half the points on each side.', 'Line P, because points far from a line do not matter.', 'Neither, because no point lies on either line.'])}
    for lv, (p, ans, wrong) in fits.items():
        o.add(u, 5, lv, 'multiple-choice', p, ans, ['A good line of fit follows the trend, with points balanced above and below and as close to the line as possible.', ans], ['8.SP.A.2'], ['reasoning'], 'g7_line_of_fit', wrong=wrong, rng=rng)


# ---------------------------------------------------------------- Grade 7 audit G4 (2026-11-19)
# #9: 7.EE.A.2 beyond the one Rewriting Expressions skill; #13: figures for polygons, congruence, circles, scale drawings
# and side-by-side dot plots. Appended after the G2 families, so earlier ids do not change.

def rewrite_meaning(o, rng):
    U = 'one-step-equations-inequalities'
    items = {
        'cp2': [('Each of n students buys a notebook for $4 and a pen for $2. The total cost is 4n + 2n dollars. Rewrite it as one term. What does the new form show?',
                 '6n: each student spends $6', ['8n: each student spends $8', '6 + n: the total is $6 more than n', '42n: each student spends $42'],
                 ['Combine like terms: 4n + 2n = 6n.', 'The coefficient 6 is the cost for one student, $4 + $2.'], 3),
                ('A garden is 3 m wide. Its length is x + 5 m. Its area is 3(x + 5) square meters. Rewrite it as 3x + 15. What does 15 represent?',
                 'the area of the 3 m by 5 m part', ['the perimeter of the garden', 'the length of the garden', 'the area of the 3 m by x m part'],
                 ['3(x + 5) = 3x + 15: the garden splits into a 3 by x part and a 3 by 5 part.', 'The 15 square meters is the 3 m by 5 m part.'], 2)],
        'cp1': [('A team buys t T-shirts at $12 each and t hats at $8 each. Write the total cost as one term and explain what the coefficient means.',
                 '20t: the cost for one shirt and one hat together is $20', ['20t: the team buys 20 items', '96t: each shirt and hat cost $96', '20 + t: the cost is $20 plus the number of items'],
                 ['12t + 8t = 20t.', 'The coefficient 20 is $12 + $8, the cost of one shirt-and-hat set.'], 3),
                ('A pool fills from two hoses. One adds 7 gallons per minute and the other 5 gallons per minute. After m minutes the water added is 7m + 5m. Which form shows the combined rate?',
                 '12m', ['35m', '7(m + 5)', '12 + m'], ['7m + 5m = 12m.', 'The coefficient 12 gallons per minute is the combined rate.'], 3)],
        'honors': [('A rectangle has length 2w + 6 and width w. Its perimeter is 2(2w + 6) + 2w. Write the perimeter in the form a(w + b). What does the form show?',
                    '6(w + 2): the perimeter is 6 times (w + 2)', ['6w + 12: the perimeter is 12 more than 6w', '4(w + 3): the perimeter is 4 times (w + 3)', '6(w + 6): the perimeter is 6 times (w + 6)'],
                    ['2(2w + 6) + 2w = 4w + 12 + 2w = 6w + 12.', 'Factor out 6: 6(w + 2).'], 2),
                   ('Ana earns d dollars a week. She saves 15% and spends 30% on lunch. The rest is d − 0.15d − 0.3d. Rewrite it as one term. What fraction of her pay is left?',
                    '0.55d: 55% of her pay is left', ['0.45d: 45% of her pay is left', '0.55d: she spends 55% on lunch', 'd − 0.45: she has $0.45 less'],
                    ['d − 0.15d − 0.3d = (1 − 0.15 − 0.3)d = 0.55d.', '0.55 = 55%, so 55% of her pay is left.'], 3)],
    }
    for lv in LV:
        for prompt, ans, wrong, steps, sk in items[lv]:
            o.add(U, sk, lv, 'multiple-choice', prompt, ans, steps, ['7.EE.A.2', '7.EE.A.1'], ['reasoning', 'context'], 'g7_rewrite_meaning', wrong=wrong, rng=rng)
    for lv, (pct, kind) in zip(LV, [(25, 'off'), (15, 'off'), (35, 'markup')]):
        f = (100 - pct) if kind == 'off' else (100 + pct)
        expr = f'p − {pct / 100:g}p' if kind == 'off' else f'p + {pct / 100:g}p'
        o.add('ratios-proportions-percentages', 9, lv, 'multiple-choice',
              f'An item has price p. After a {pct}% {"discount" if kind == "off" else "markup"} the new price is {expr}. Which rewritten form shows that the new price is a percent of p, and what percent?',
              f'{f / 100:g}p, so {f}% of p',
              [f'{expr} = (1 {"−" if kind == "off" else "+"} {pct / 100:g})p = {f / 100:g}p.', f'{f / 100:g} = {f}%, so the new price is {f}% of the original.'],
              ['7.EE.A.2', '7.RP.A.3'], ['reasoning', 'context'], 'g7_rewrite_percent', wrong=[f'{pct / 100:g}p, so {pct}% of p', f'{(200 - f) / 100:g}p, so {200 - f}% of p', f'p {"−" if kind == "off" else "+"} {pct}, so ${pct} {"less" if kind == "off" else "more"}'], rng=rng)


def poly_angles(o, rng):
    U, sk = 'spatial-thinking', 3
    plans = {
        'cp2': [('triangle', [52, 71, None]), ('triangle', [38, 90, None])],
        'cp1': [('quadrilateral', [95, 70, 110, None]), ('pentagon', [100, 115, 120, 98, None])],
        'honors': [('quadrilateral', 'x 2x x+30 2x+30'.split()), ('pentagon', 'x x+10 x+20 x+30 x+40'.split())],
    }
    for lv in LV:
        for name, ang in plans[lv]:
            n = len(ang); total = (n - 2) * 180
            if lv != 'honors':
                x = total - sum(a for a in ang if a)
                labels = [f'{a}°' if a else 'x°' for a in ang]
                o.add(U, sk, lv, 'short-answer', f'Find x in the {name}.', f'x = {x}',
                      [f'The interior angles of a {name} add to ({n} − 2) · 180° = {total}°.', ' + '.join(str(a) for a in ang if a) + f' + x = {total}.', f'x = {total} − {sum(a for a in ang if a)} = {x}.'],
                      ['8.G.A.5', '7.G.B.5'], ['diagram'], 'g7_polygon_angle', fig=('polygon', labels, name))
            else:
                coef = sum(2 if a.startswith('2x') else 1 for a in ang)
                const = sum(int(a.split('+')[1]) if '+' in a else 0 for a in ang)
                x = (total - const) // coef; assert coef * x + const == total
                vals = [(2 if a.startswith('2x') else 1) * x + (int(a.split('+')[1]) if '+' in a else 0) for a in ang]
                labels = [a.replace('+', ' + ') + '°' if a != 'x' else 'x°' for a in ang]
                o.add(U, sk, lv, 'short-answer', f'Find the measure of the largest angle of the {name}.', f'{max(vals)}°',
                      [f'The interior angles add to ({n} − 2) · 180° = {total}°.', f'{coef}x + {const} = {total}, so x = {x}.', 'The angles are ' + ', '.join(f'{v}°' for v in vals) + f'; the largest is {max(vals)}°.'],
                      ['8.G.A.5', '7.EE.B.4a'], ['diagram', 'multistep'], 'g7_polygon_algebra', fig=('polygon', labels, name))


def congruence_marks(o, rng):
    U, sk = 'spatial-thinking', 5
    nm = ('ABC', 'DEF')
    # cp2: read a side and an angle across the tick marks
    o.add(U, sk, 'cp2', 'short-answer', '△ABC ≅ △DEF. The tick marks show matching sides. How long is DE?', '7 cm',
          ['Sides with one tick mark match: AB and DE.', 'AB = 7 cm, so DE = 7 cm.'], ['8.G.A.2'], ['diagram'], 'g7_congruent_marks', fig=('cong', nm, {(0, 0): '7 cm', (0, 1): '9 cm'}, {}))
    o.add(U, sk, 'cp2', 'short-answer', '△ABC ≅ △DEF. Find the measure of ∠E.', '64°',
          ['∠B matches ∠E (the second letters).', 'm∠B = 64°, so m∠E = 64°.'], ['8.G.A.2'], ['diagram'], 'g7_congruent_marks', fig=('cong', nm, {}, {(0, 1): '64°', (0, 0): '47°'}))
    o.add(U, sk, 'cp1', 'multiple-choice', '△ABC ≅ △DEF. Which side of △DEF has two tick marks, matching BC?', 'EF',
          ['Two tick marks are on BC in △ABC.', 'BC matches EF (second and third letters).'], ['8.G.A.2'], ['diagram'], 'g7_congruent_marks', wrong=['DE', 'DF', 'AC'], rng=rng, fig=('cong', nm, {}, {}))
    o.add(U, sk, 'cp1', 'short-answer', '△ABC ≅ △DEF. The side lengths are labelled. Find x.', 'x = 6',
          ['CA and FD both have three tick marks, so they are equal.', '2x + 3 = 15, so 2x = 12 and x = 6.'], ['8.G.A.2', '7.EE.B.4a'], ['diagram'], 'g7_congruent_algebra',
          fig=('cong', nm, {(0, 2): '2x + 3', (1, 2): '15'}, {}))
    o.add(U, sk, 'honors', 'short-answer', '△ABC ≅ △DEF. Find x, then the measure of ∠C.', 'x = 15; m∠C = 80°',
          ['∠A matches ∠D, so 3x + 5 = 50 and x = 15.', '∠B matches ∠E, so m∠B = 50°.', 'm∠C = 180° − 50° − 50° = 80°.'],
          ['8.G.A.2', '7.EE.B.4a'], ['diagram', 'multistep'], 'g7_congruent_algebra', fig=('cong', nm, {}, {(0, 0): '(3x + 5)°', (1, 0): '50°', (1, 1): '50°'}))
    o.add(U, sk, 'honors', 'short-answer', '△ABC ≅ △DEF. Use the labelled lengths to find the perimeter of △DEF.', '31 cm',
          ['Matching sides: DE = AB = 9 cm, EF = BC = 12 cm, and FD = 10 cm is given.', 'Perimeter of △DEF = 9 + 12 + 10 = 31 cm.'],
          ['8.G.A.2'], ['diagram', 'multistep'], 'g7_congruent_perimeter', fig=('cong', nm, {(0, 0): '9 cm', (0, 1): '12 cm', (1, 2): '10 cm'}, {}))


def circle_figs(o, rng):
    def t(x):  # nearest tenth, half up
        return f'{float(half_up(Fr(x).limit_denominator(10 ** 6) if not isinstance(x, Fr) else x, 1)):.1f}'
    P = Fr(314, 100)
    C = [('cp2', 'radius', 'r = 5 cm', 'Find the circumference. Use 3.14 for π and round to the nearest tenth.', P * 10, 'cm', ['C = 2πr = 2 · 3.14 · 5', 'C = 31.4 cm']),
         ('cp2', 'diameter', 'd = 12 in.', 'Find the circumference. Use 3.14 for π and round to the nearest tenth.', P * 12, 'in.', ['C = πd = 3.14 · 12', 'C = 37.68, which rounds to 37.7 in.']),
         ('cp1', 'semicircle', '10 m', 'Find the perimeter of the semicircle (the curved part and the diameter). Use 3.14 for π and round to the nearest tenth.', P * 5 + 10, 'm',
          ['Curved part: half of πd = 3.14 · 10 ÷ 2 = 15.7 m.', 'Add the diameter: 15.7 + 10 = 25.7 m.']),
         ('cp1', 'radius', 'r = 7 ft', 'A wheel has this radius. How far does it roll in 10 full turns? Use 3.14 for π and round to the nearest tenth.', P * 14 * 10, 'ft',
          ['One turn: C = 2 · 3.14 · 7 = 43.96 ft.', '10 turns: 439.6 ft.']),
         ('honors', 'quarter', '8 cm', 'Find the perimeter of the quarter circle. Use 3.14 for π and round to the nearest tenth.', P * 16 / 4 + 16, 'cm',
          ['Curved part: one quarter of 2πr = 2 · 3.14 · 8 ÷ 4 = 12.56 cm.', 'Add the two radii: 12.56 + 8 + 8 = 28.56, which rounds to 28.6 cm.']),
         ('honors', 'diameter', 'd = 24 in.', 'The circumference of a second circle is 3 times this circle\'s circumference. What is the second circle\'s radius?', None, 'in.',
          ['Circumference is proportional to the diameter, so the second diameter is 3 · 24 = 72 in.', 'Its radius is 72 ÷ 2 = 36 in.'])]
    for lv, kind, lab, q, v, unit, steps in C:
        ans = '36 in.' if v is None else f'{t(v)} {unit}'
        o.add('spatial-thinking', 6, lv, 'short-answer', q, ans, steps, ['7.G.B.4'], ['diagram'] + (['multistep'] if lv == 'honors' else []), 'g7_circle_figure', fig=('circle', kind, lab))
    A = [('cp2', 'radius', 'r = 6 cm', P * 36, 'cm²', ['A = πr² = 3.14 · 6²', 'A = 3.14 · 36 = 113.04, which rounds to 113.0 cm²']),
         ('cp2', 'diameter', 'd = 10 m', P * 25, 'm²', ['r = 10 ÷ 2 = 5 m.', 'A = 3.14 · 25 = 78.5 m²']),
         ('cp1', 'semicircle', '12 in.', P * 36 / 2, 'in.²', ['r = 6 in.', 'Half of πr²: 3.14 · 36 ÷ 2 = 56.52, which rounds to 56.5 in.²']),
         ('cp1', 'quarter', '4 ft', P * 16 / 4, 'ft²', ['One quarter of πr²: 3.14 · 16 ÷ 4 = 12.56', 'which rounds to 12.6 ft²']),
         ('honors', 'diameter', 'd = 16 cm', None, 'cm²', ['Doubling the diameter doubles the radius, so the area is multiplied by 2² = 4.', 'Old area 3.14 · 8² = 200.96 cm²; new area 4 · 200.96 = 803.84, which rounds to 803.8 cm².']),
         ('honors', 'semicircle', '20 m', None, 'm²', ['The semicircle has r = 10 m: area 3.14 · 100 ÷ 2 = 157 m².', 'A square on the diameter has area 20 · 20 = 400 m²; together 557 m².'])]
    Q = {None: None}
    for lv, kind, lab, v, unit, steps in A:
        if v is None and kind == 'diameter':
            q = 'A second circle has twice this diameter. Find the area of the second circle. Use 3.14 for π and round to the nearest tenth.'; ans = f'{t(P * 64 * 4)} {unit}'
        elif v is None:
            q = 'A window is a 20 m by 20 m square with this semicircle on top (its diameter is the top side of the square). Find the total area. Use 3.14 for π.'; ans = f'{t(P * 50 + 400)} {unit}'
        else:
            q = 'Find the area' + (' of the figure' if kind in ('semicircle', 'quarter') else '') + '. Use 3.14 for π and round to the nearest tenth.'; ans = f'{t(v)} {unit}'
        o.add('area-volume', 3, lv, 'short-answer', q, ans, steps, ['7.G.B.4'], ['diagram'] + (['multistep'] if lv == 'honors' else []), 'g7_circle_area_figure', fig=('circle', kind, lab))


def scale_figs(o, rng):
    U, sk = 'ratios-proportions-percentages', 3
    plans = [('cp2', 'Kitchen', '4.5 in.', '3 in.', '1 in. : 4 ft', 'How long is the actual kitchen?', '18 ft', ['Each inch is 4 ft.', '4.5 · 4 = 18 ft.']),
             ('cp2', 'Garden', '6 cm', '2.5 cm', '1 cm : 2 m', 'How wide is the actual garden (the shorter side)?', '5 m', ['Each centimeter is 2 m.', '2.5 · 2 = 5 m.']),
             ('cp1', 'Bedroom', '3 in.', '2.5 in.', '1 in. : 4 ft', 'Find the actual area of the bedroom.', '120 square feet',
              ['Actual length 3 · 4 = 12 ft; actual width 2.5 · 4 = 10 ft.', 'Area = 12 · 10 = 120 square feet.']),
             ('cp1', 'Patio', '5 cm', '3 cm', '1 cm : 1.5 m', 'Find the actual perimeter of the patio.', '24 m',
              ['Actual sides 5 · 1.5 = 7.5 m and 3 · 1.5 = 4.5 m.', 'Perimeter = 2(7.5 + 4.5) = 24 m.']),
             ('honors', 'Classroom', '6 in.', '4 in.', '1 in. : 5 ft', 'The room is redrawn with the scale 1 in. : 8 ft. How long is the longer side on the new drawing?', '3.75 in.',
              ['Actual length: 6 · 5 = 30 ft.', 'New drawing: 30 ÷ 8 = 3.75 in.']),
             ('honors', 'Park', '8 cm', '5 cm', '1 cm : 25 m', 'Find the actual area of the park in square meters.', '25,000 square meters',
              ['Actual sides: 8 · 25 = 200 m and 5 · 25 = 125 m.', 'Area = 200 · 125 = 25,000 square meters (the drawing area 40 cm² times 25² = 625).'])]
    for lv, title, wl, hl, sc, q, ans, steps in plans:
        o.add(U, sk, lv, 'short-answer', f'The scale drawing shows a {title.lower()}. {q}', ans, steps, ['7.G.A.1'], ['diagram'] + (['multistep'] if lv != 'cp2' else []), 'g7_scale_drawing_figure', fig=('plan', wl, hl, sc, title))


def dotplot_figs(o, rng):
    U, sk = 'data-analysis-probability', 9
    base = [2, 3, 3, 4, 4, 4, 4, 5, 5, 6]          # mean 4, MAD 0.8, median 4, range 4
    wide = [1, 2, 3, 4, 4, 4, 4, 5, 6, 7]          # mean 4, MAD 1.2, median 4, range 6
    plans = [('cp2', base, [x + 3 for x in base], 'How much greater is the median for Class B than for Class A?', '3',
              ['Median of A: 4 (the 5th and 6th values are 4 and 4).', 'Median of B: 7. Difference: 7 − 4 = 3.']),
             ('cp2', base, wide, 'Which class has the greater range, and by how much?', 'Class B, by 2',
              ['Range A: 6 − 2 = 4.', 'Range B: 7 − 1 = 6. Class B by 2.']),
             ('cp1', base, [x + 2 for x in base], 'Find the difference of the means.', '2',
              ['Mean A: 40 ÷ 10 = 4.', 'Mean B: 60 ÷ 10 = 6. Difference: 2.']),
             ('cp1', base, wide, 'The means are equal. Which class has the greater mean absolute deviation (MAD)? Give both MADs.', 'Class B; MAD A = 0.8, MAD B = 1.2',
              ['Mean of each class is 4.', 'MAD A = (2 + 1 + 1 + 0 + 0 + 0 + 0 + 1 + 1 + 2) ÷ 10 = 0.8; MAD B = (3 + 2 + 1 + 0 + 0 + 0 + 0 + 1 + 2 + 3) ÷ 10 = 1.2.']),
             ('honors', base, [x + 3 for x in base], 'Both classes have MAD 0.8. The difference of the means is how many MADs?', '3.75',
              ['Means: 4 and 7; difference 3.', '3 ÷ 0.8 = 3.75 MADs.']),
             ('honors', base, [x + 4 for x in base], 'Both classes have MAD 0.8. Express the difference of the means as a multiple of the MAD. Is the overlap large or small?', '5 MADs; small overlap',
              ['Means: 4 and 8; difference 4.', '4 ÷ 0.8 = 5, a large difference compared with the spread, so the overlap is small.'])]
    for i, (lv, a, b, q, ans, steps) in enumerate(plans):
        lo, hi = min(a + b), max(a + b)
        o.add(U, sk, lv, 'short-answer', f'The dot plots show the number of books read by students in two classes. {q}', ans, steps, ['7.SP.B.3', '7.SP.B.4'],
              ['diagram'] + (['multistep'] if lv == 'honors' else []), 'g7_dot_plot_compare', fig=('dots', a, b, ('Class A', 'Class B'), lo, hi, 'books read'))


def draw(fig, path):
    kind = fig[0]
    if kind == 'slice':
        return figures.slice_fig(path, fig[1], fig[2])
    if kind == 'angles':
        return figures.angles(path, fig[1], fig[2])
    if kind == 'line':
        _, pts, xm, ym, xl, yl, ys, lab = fig
        return figures.line_graph(path, [(float(a), float(b)) for a, b in pts], xm, ym, xl, yl, 1, ys, lab)
    if kind == 'story':
        return figures.story_graph(path, fig[1], fig[2])
    if kind == 'polygon':
        return figures.polygon(path, fig[1], fig[2])
    if kind == 'cong':
        return figures.congruent_triangles(path, fig[1], fig[2], fig[3])
    if kind == 'circle':
        return figures.circle_fig(path, fig[1], fig[2])
    if kind == 'plan':
        return figures.floor_plan(path, fig[1], fig[2], fig[3], title=fig[4])
    if kind == 'dots':
        return figures.dot_plots(path, *fig[1:])
    raise ValueError(kind)


FAMILIES = [tri_ineq, cross_sections, prop_graphs, angle_eqs, percents, number_sense, grade8,
            rewrite_meaning, poly_angles, congruence_marks, circle_figs, scale_figs, dotplot_figs]
GID = re.compile(r'-g\d{2}$')


def build(o):
    for fam in FAMILIES:
        fam(o, random.Random('g7-' + fam.__name__))


def main(extra=()):
    banks, tags = lib.load(), lib.load_tags()
    for u in lib.UNITS:
        for q in banks[u]['questions']:
            if GID.search(q['id']) and q.get('diagram'):
                p = os.path.join(lib.ROOT, q['diagram']['spec']['src'])
                if os.path.exists(p):
                    os.remove(p)
        banks[u]['questions'] = [q for q in banks[u]['questions'] if not GID.search(q['id'])]
        tags[u] = {k: v for k, v in tags[u].items() if not GID.search(k)}
    o = Out()
    build(o)
    for fn in extra:
        fn(o)
    count = {}
    for unit, skill, lv, q, tg, fig in o.items:
        key = (unit, skill, lv)
        count[key] = count.get(key, 0) + 1
        qid = f'pa7-{lib.ABBR[unit]}-s{skill:02d}-{lv}-g{count[key]:02d}'
        q = dict(id=qid, **q)
        if fig:
            rel = f'question-banks/assets/prealgebra7/{unit}/{qid}.png'
            alt = draw(fig, os.path.join(lib.ROOT, rel))
            q['diagram'] = {'type': 'image', 'spec': {'src': rel, 'alt': alt}}
        qs = banks[unit]['questions']
        last = max(i for i, x in enumerate(qs) if x['skillId'] == q['skillId'] and x['level'] == lv)
        qs.insert(last + 1, q)
        tags[unit][qid] = tg
    lib.save(banks)
    lib.save_tags(tags)
    print('new items:', len(o.items), '; with figures:', sum(1 for x in o.items if x[5]))


if __name__ == '__main__':
    main()
