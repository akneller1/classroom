"""Grade 6 audit batch 6B (2026-11-19): new items for the gaps in the audit.
 #5  find the whole from a part and a percent (6.RP.A.3c)        #6  graphs of dependent and independent variables (6.EE.C.9)
 #7  tape diagrams, double number lines (6.RP.A.3a) and fraction-division models (6.NS.A.1)
 #8  6.SP.B.5a (number of observations), 6.SP.B.5b (attribute and units), 6.SP.A.3 (center vs variation)
 #9  expressions for an unknown in context (6.EE.B.6) and parts of an expression (6.EE.A.2b)
 #17 figures for nets (6.G.A.4) and polygons on the coordinate plane (6.G.A.3)
 #18 connected four-part constructed-response tasks, two per unit (CP1 and Honors)
New ids end in -gNN; figures go to question-banks/assets/math6/<unit>/<id>.png. Idempotent."""
import os, random, re, sys
from fractions import Fraction as Fr
sys.path.insert(0, os.path.dirname(__file__))
import lib
import figures

LV = ('cp2', 'cp1', 'honors')
NAMES = ['Maya', 'Leo', 'Priya', 'Diego', 'Ana', 'Owen', 'Nia', 'Raj', 'Zoe', 'Sam', 'Lena', 'Kai']


def mixed(x):
    x = Fr(x)
    w, r = divmod(abs(x.numerator), x.denominator)
    s = '-' if x < 0 else ''
    return s + (str(w) if r == 0 else (f'{w} {r}/{x.denominator}' if w else f'{r}/{x.denominator}'))


def money(x):
    x = Fr(x)
    v = x.numerator / x.denominator
    return f'${v:,.0f}' if x.denominator == 1 else f'${v:,.2f}'


class Out:
    def __init__(self):
        self.items = []

    def add(self, unit, skill, lv, fmt, prompt, answer, steps, std, tags, fam, wrong=None, fig=None, rng=None, parts=None):
        q = dict(skillId=f'{unit}-skill-{skill:02d}', level=lv, format=fmt, prompt=prompt, answer=answer, solutionSteps=steps,
                 standards=std, sourceNotes=lib.SOURCE.format(fam=fam) + ' Teacher review pending.')
        if fmt == 'multiple-choice':
            opts = [answer] + [w for w in wrong if w != answer][:3]
            assert len(set(opts)) == 4, (prompt, opts)
            rng.shuffle(opts)
            q['options'] = [{'text': t, 'correct': t == answer} for t in opts]
        if parts:
            q['parts'] = [{'prompt': p, 'answer': a} for p, a in parts]
        self.items.append((unit, skill, lv, q, tags, fig))


# ---------------------------------------------------------------------------------------------- #5 percent of a whole
def percent_whole(o, rng):
    U = 'ratios-rates-percent-proportions'
    plans = {
        'cp2': [(30, 18, None), (25, 12, None), (40, 26, None)],
        'cp1': [(60, 45, 'A theater has sold {p} tickets, which is {pc}% of all its tickets. How many tickets does the theater have in all?'),
                (15, 9, '{n} of the students in a club play chess. That is {pc}% of the club. How many students are in the club?'),
                (80, 52, 'A tank holds {p} gallons when it is {pc}% full. How many gallons does it hold when it is full?')],
        'honors': [(35, 91, 'After spending {pc}% of {pos} savings, {n} has ${p} left. How much did {pr} have at first?'),
                   (20, 48, 'A jacket is on sale for {pc}% off. The sale price is ${p}. What was the original price?'),
                   (65, 42, 'A team has played {pc}% of its season and has {p} games left. How many games are in the season?')],
    }
    for lv in LV:
        for i, (pc, p, ctx) in enumerate(plans[lv]):
            nm = NAMES[(i * 5 + LV.index(lv)) % len(NAMES)]
            sk = 6
            if lv == 'cp2':
                whole = Fr(p * 100, pc)
                o.add(U, sk, lv, 'short-answer', f'{p} is {pc}% of what number?', mixed(whole),
                      [f'{pc}% = {pc}/100, so {pc}/100 × w = {p}.', f'w = {p} × 100/{pc} = {mixed(whole)}.', f'Check: {pc}% of {mixed(whole)} = {p}.'], ['6.RP.A.3c'], ['percent'], 'g6_percent_whole')
            elif lv == 'cp1':
                whole = Fr(p * 100, pc)
                prompt = ctx.format(p=p, pc=pc, n=p)
                fmt = 'multiple-choice' if i == 1 else 'short-answer'
                wrong = [mixed(Fr(p * pc, 100)), mixed(p + pc), mixed(whole - p)]
                o.add(U, sk, lv, fmt, prompt, mixed(whole), [f'{p} is {pc}% of the whole: {pc}/100 × w = {p}.', f'w = {p} ÷ {pc}/100 = {p} × 100/{pc} = {mixed(whole)}.'],
                      ['6.RP.A.3c'], ['percent', 'context'], 'g6_percent_whole', wrong=wrong if fmt == 'multiple-choice' else None, rng=rng)
            else:
                rest = 100 - pc
                whole = Fr(p * 100, rest)
                pos, pr = ('her', 'she') if nm not in ('Leo', 'Diego', 'Owen', 'Raj', 'Sam', 'Kai') else ('his', 'he')
                prompt = ctx.format(p=p, pc=pc, n=nm, pos=pos, pr=pr)
                ans = money(whole) if '$' in prompt else mixed(whole)
                o.add(U, sk, lv, 'short-answer', prompt, ans,
                      [f'What is left is 100% − {pc}% = {rest}% of the whole.', f'{rest}/100 × w = {p}, so w = {p} × 100/{rest} = {mixed(whole)}.', f'Answer: {ans}.'],
                      ['6.RP.A.3c'], ['percent', 'context', 'multistep'], 'g6_percent_whole')


# ---------------------------------------------------------------------------------------------- #6 graphs, 6.EE.C.9
def dep_graphs(o, rng):
    U, sk = 'expressions-equations', 7
    plans = {
        'cp2': [('hours worked', 'dollars earned', 'h', 'd', 12, 0, 4, 48, 12), ('minutes', 'pages read', 'm', 'p', 2, 0, 8, 16, 2)],
        'cp1': [('tickets', 'total cost ($)', 't', 'c', 6, 0, 6, 36, 6), ('hours', 'miles walked', 'h', 'm', 3, 0, 8, 24, 3)],
        'honors': [('months', 'savings ($)', 'n', 's', 15, 30, 8, 150, 15), ('hours', 'cost ($)', 'h', 'c', 20, 40, 6, 160, 20)],
    }
    for lv in LV:
        for i, (xl, yl, xv, yv, k, b, xm, ym, ys) in enumerate(plans[lv]):
            pts = [(0, b), (2, b + 2 * k)]
            lab = [(x, b + k * x) for x in (2, 4)]
            fig = ('line', pts, xm, ym, xl, yl, ys, lab)
            eq = f'{yv} = {k}{xv}' + (f' + {b}' if b else '')
            if lv == 'cp2' and i == 0:
                x = 3
                o.add(U, sk, lv, 'short-answer', f'The graph shows {yl} y for {xl} x. Use the graph to find the {yl} for {x} {xl}.', str(b + k * x),
                      [f'The line goes up {2 * k} from x = 2 to x = 4, so it rises {k} for each 1 unit of x.', f'At x = {x}: y = {k} × {x} = {b + k * x}.'],
                      ['6.EE.C.9'], ['graph'], 'g6_dep_graph_read', fig=fig)
            elif lv == 'cp2':
                o.add(U, sk, lv, 'multiple-choice', f'The graph shows {yl} for {xl}. Which is the independent variable?', xl,
                      [f'The independent variable is on the horizontal axis and changes on its own: {xl}.', f'The {yl} depends on the {xl}.'],
                      ['6.EE.C.9'], ['graph', 'reasoning'], 'g6_dep_graph_var', wrong=[yl, 'both', 'neither'], rng=rng, fig=fig)
            elif lv == 'cp1':
                o.add(U, sk, lv, 'short-answer', f'The graph shows {yl} {yv} for {xl} {xv}. Write an equation for {yv} in terms of {xv}.', eq,
                      [f'The line passes through (0, 0) and ({lab[0][0]}, {lab[0][1]}).', f'{yv} increases by {k} for each 1 added to {xv}.', f'{eq}.'],
                      ['6.EE.C.9'], ['graph', 'multiple-representations'], 'g6_dep_graph_equation', fig=fig)
            else:
                k2, b2 = k + (5 if i == 0 else 10), 0
                x = next(x for x in range(1, 30) if b + k * x < k2 * x)
                o.add(U, sk, lv, 'short-answer', f'The graph shows Plan A: {yl} {yv} after {xl} {xv}. Plan B is {yv} = {k2}{xv}. After how many whole {xl} is Plan B greater than Plan A for the first time?',
                      str(x), [f'Plan A from the graph: {eq} (starts at {b} and rises {k} per unit).', f'Plan B: {yv} = {k2}{xv}. Plan B is greater when {k2}{xv} > {k}{xv} + {b}, so {k2 - k}{xv} > {b}.',
                               f'{xv} > {mixed(Fr(b, k2 - k))}, so the first whole number is {x}.'],
                      ['6.EE.C.9', '6.EE.B.8'], ['graph', 'multistep', 'context'], 'g6_dep_graph_compare', fig=fig)


# ---------------------------------------------------------------------------------------------- #7 visual models
def tape_models(o, rng):
    U = 'ratios-rates-percent-proportions'
    plans = {'cp2': [(3, 2, 'red', 'blue', 'marbles', 40), (4, 1, 'water', 'juice', 'cups', 25)],
             'cp1': [(5, 3, 'boys', 'girls', 'students', 32), (2, 7, 'cats', 'dogs', 'pets', 45)],
             'honors': [(7, 4, 'adults', 'children', 'people', 77), (3, 5, 'fiction', 'nonfiction', 'books', 64)]}
    for lv in LV:
        for i, (a, b, la, lb, what, tot) in enumerate(plans[lv]):
            unit = Fr(tot, a + b)
            fig = ('tape', [la, lb], [a, b], f'{tot} {what}', None)
            if lv == 'cp2':
                o.add(U, 1, lv, 'short-answer', f'The tape diagram shows the ratio of {la} to {lb} {what}. There are {tot} {what} in all. How many of the {what} are {la}?', mixed(a * unit),
                      [f'There are {a} + {b} = {a + b} equal boxes.', f'Each box is {tot} ÷ {a + b} = {mixed(unit)}.', f'{la.capitalize()}: {a} × {mixed(unit)} = {mixed(a * unit)}.'],
                      ['6.RP.A.3a', '6.RP.A.1'], ['diagram'], 'g6_tape_diagram', fig=fig)
            elif lv == 'cp1':
                o.add(U, 1, lv, 'short-answer', f'The tape diagram shows the ratio of {la} to {lb}. There are {tot} {what} in all. How many more {lb if b > a else la} than {la if b > a else lb} are there?', mixed(abs(a - b) * unit),
                      [f'Each box: {tot} ÷ {a + b} = {mixed(unit)}.', f'The difference is {abs(a - b)} boxes.', f'{abs(a - b)} × {mixed(unit)} = {mixed(abs(a - b) * unit)}.'],
                      ['6.RP.A.3a', '6.RP.A.1'], ['diagram', 'multistep'], 'g6_tape_diagram', fig=fig)
            else:
                add = a * 2
                newb = b * unit + add
                o.add(U, 1, lv, 'short-answer', f'The tape diagram shows the ratio of {la} to {lb}: {tot} {what} in all. Then {add} more {lb} arrive. What is the new ratio of {la} to {lb} in simplest form, as a:b?',
                      f'{Fr(int(a * unit), int(newb)).numerator}:{Fr(int(a * unit), int(newb)).denominator}',
                      [f'Each box: {tot} ÷ {a + b} = {mixed(unit)}; {la}: {mixed(a * unit)}, {lb}: {mixed(b * unit)}.', f'After {add} more {lb}: {mixed(newb)}.',
                       f'Ratio {mixed(a * unit)} : {mixed(newb)} = {Fr(int(a * unit), int(newb)).numerator}:{Fr(int(a * unit), int(newb)).denominator}.'],
                      ['6.RP.A.3a', '6.RP.A.1'], ['diagram', 'multistep'], 'g6_tape_diagram', fig=fig)


def double_lines(o, rng):
    U, sk = 'ratios-rates-percent-proportions', 3
    plans = {'cp2': [('cups of flour', 'muffins', 2, 12, 3), ('dollars', 'stickers', 3, 10, 4)],
             'cp1': [('miles', 'minutes', 4, 30, 5), ('liters', 'kilometers', 5, 60, 6)],
             'honors': [('ounces', 'calories', 3, 45, 7), ('cups of rice', 'servings', 2, 5, 9)]}
    for lv in LV:
        for i, (tl, bl, a, b, ask) in enumerate(plans[lv]):
            top = [str(a * j) for j in range(5)]; bottom = [str(b * j) for j in range(5)]
            if lv == 'cp2':
                q_i = 3; bottom[q_i] = '?'
                o.add(U, sk, lv, 'short-answer', f'The double number line shows {tl} and {bl}. What number belongs at the question mark?', str(b * q_i),
                      [f'{a} {tl} match {b} {bl}.', f'{a * q_i} {tl} is {q_i} times as much, so {b} × {q_i} = {b * q_i} {bl}.'], ['6.RP.A.3a'], ['diagram'], 'g6_double_number_line',
                      fig=('dnl', tl.capitalize(), top, bl.capitalize(), bottom))
            elif lv == 'cp1':
                o.add(U, sk, lv, 'short-answer', f'The double number line shows {tl} and {bl}. Extend it: how many {bl} go with {a * ask} {tl}?', str(b * ask),
                      [f'The unit pattern: {a} {tl} ↔ {b} {bl}.', f'{a * ask} ÷ {a} = {ask} groups.', f'{ask} × {b} = {b * ask} {bl}.'], ['6.RP.A.3a'], ['diagram'], 'g6_double_number_line',
                      fig=('dnl', tl.capitalize(), top, bl.capitalize(), bottom))
            else:
                target = b * ask + Fr(b, 2)
                o.add(U, sk, lv, 'short-answer', f'The double number line shows {tl} and {bl}. How many {tl} give {mixed(target)} {bl}?', mixed(target * a / b),
                      [f'Unit rate: {a} ÷ {b} = {mixed(Fr(a, b))} {tl} per one of the {bl}.', f'{mixed(target)} × {mixed(Fr(a, b))} = {mixed(target * a / b)}.'],
                      ['6.RP.A.3a', '6.RP.A.3b'], ['diagram', 'multistep'], 'g6_double_number_line', fig=('dnl', tl.capitalize(), top, bl.capitalize(), bottom))


def fraction_models(o, rng):
    U = 'fractions-decimals-operations'
    plans = {'cp2': [(2, 4, 8, 2), (1, 6, 6, 2)], 'cp1': [(2, 3, 5, 2), (2, 4, 6, 3)], 'honors': [(3, 4, 10, 3), (3, 6, 14, 4)]}
    for lv in LV:
        for i, (W, D, S, G) in enumerate(plans[lv]):
            dividend, divisor = Fr(S, D), Fr(G, D)
            q = dividend / divisor
            sk = 1 if lv != 'cp2' or i == 0 else 2
            fig = ('bars', W, D, S, G)
            o.add(U, sk, lv, 'short-answer', f'The model shows {mixed(dividend)} shaded, with brackets marking groups of {mixed(divisor)}. Use it to find {mixed(dividend)} ÷ {mixed(divisor)}.', mixed(q),
                  [f'Each whole is cut into {D} parts, so {mixed(dividend)} = {S} parts and {mixed(divisor)} = {G} parts.', f'{S} ÷ {G}: there are {S // G} full groups' + (f' and {S % G} part{"s" if S % G > 1 else ""} left, which is {S % G}/{G} of a group.' if S % G else '.'),
                   f'{mixed(dividend)} ÷ {mixed(divisor)} = {mixed(q)}.'], ['6.NS.A.1'], ['diagram'], 'g6_fraction_model', fig=fig)


# ---------------------------------------------------------------------------------------------- #8 statistics sub-standards
def stats_subs(o, rng):
    U, sk = 'data-displays', 8
    data = {'cp2': [3, 4, 4, 5, 5, 5, 6, 7], 'cp1': [1, 2, 2, 3, 3, 3, 3, 4, 5, 6, 8], 'honors': [10, 12, 12, 13, 14, 14, 14, 15, 17, 18, 19, 22]}
    for lv in LV:
        d = data[lv]
        o.add(U, sk, lv, 'short-answer', 'The dot plot shows how many hours some students practiced an instrument last week. How many observations are in the data set?', str(len(d)),
              ['Each dot is one observation.', f'Count the dots: {len(d)}.'], ['6.SP.B.5a'], ['diagram'], 'g6_observations', fig=('dot', d, min(d), max(d), 'hours practiced'))
    attr = {'cp2': ('A student records how long, in minutes, each classmate takes to get to school: 12, 5, 20, 8, 15.', 'time to get to school, in minutes',
                    ['the number of classmates, in students', 'distance to school, in miles', 'time to get to school, in hours']),
            'cp1': ('A coach records the height of each player, in inches: 58, 61, 60, 63, 59, 62.', 'player height, in inches',
                    ['player weight, in pounds', 'the number of players, in players', 'player height, in feet']),
            'honors': ('A scientist records the mass of 8 apples from one tree, in grams: 150, 162, 148, 171, 155, 160, 158, 149.', 'apple mass, in grams',
                       ['apple mass, in kilograms', 'the number of apples, in apples', 'tree height, in meters'])}
    for lv in LV:
        p, a, w = attr[lv]
        o.add(U, sk, lv, 'multiple-choice', p + ' What attribute is measured, and in what units?', a,
              ['The attribute is what is measured for each individual.', f'Here: {a}.'], ['6.SP.B.5b'], ['reasoning'], 'g6_attribute_units', wrong=w, rng=rng)
    a3 = {'cp2': ('Which statement describes a measure of center?', 'It summarizes all the values with one typical number.',
                  ['It tells how far apart the values are.', 'It is the largest value minus the smallest value.', 'It counts how many values there are.']),
          'cp1': ('Two classes have the same median test score, 80, but Class A\'s scores range from 60 to 100 and Class B\'s range from 75 to 85. What does this show?',
                  'The centers are the same, but the variation is different.', ['The variation is the same, but the centers are different.', 'Class A has the higher median.', 'Both the centers and the variation are the same.']),
          'honors': ('A data set has mean 12 and mean absolute deviation 0.5. Another has mean 12 and MAD 4. Which statement is true?',
                     'Both have the same center, and the second data set\'s values vary much more.', ['The second data set has a greater mean.', 'Both data sets vary the same amount.',
                                                                                                  'The first data set\'s values vary more because its MAD is smaller.'])}
    for lv in LV:
        p, a, w = a3[lv]
        o.add(U, 1 if lv == 'cp2' else sk, lv, 'multiple-choice', p, a, ['A measure of center gives one typical value; a measure of variation describes how the values spread.', f'So: {a}'],
              ['6.SP.A.3'], ['reasoning'], 'g6_center_variation', wrong=w, rng=rng)


# ---------------------------------------------------------------------------------------------- #9 expressions
def expr_unknowns(o, rng):
    U, sk = 'expressions-equations', 2
    plans = {'cp2': [('Each pack has 8 crayons. Write an expression for the number of crayons in p packs.', '8p'),
                     ('Leo is 3 years older than his sister, who is s years old. Write an expression for Leo\'s age.', 's + 3')],
             'cp1': [('A pizza costs $11 and each topping costs $2. Write an expression for the cost of a pizza with t toppings.', '11 + 2t'),
                     ('A rope n feet long is cut into 4 equal pieces. Write an expression for the length of one piece, in feet.', 'n/4')],
             'honors': [('Tickets cost $9 each and there is a $4 fee per order. Write an expression for the cost of an order of x tickets for each of 3 friends.', '27x + 4'),
                        ('A rectangle is w cm wide and 5 cm longer than it is wide. Write an expression for its perimeter in centimeters.', '4w + 10')]}
    for lv in LV:
        for p, a in plans[lv]:
            o.add(U, sk, lv, 'short-answer', p, a, ['Let the variable stand for the unknown number.', f'Expression: {a}.'], ['6.EE.B.6', '6.EE.A.2a'], ['context'], 'g6_expression_unknown')
    parts = {'cp2': ('How many terms are in the expression 4x + 7y + 2?', '3', ['Terms are separated by + or − signs.', '4x, 7y and 2: 3 terms.']),
             'cp1': ('In the expression 2(8 + 7), which part is a sum?', '8 + 7', ['A sum is the result of adding.', '8 + 7 is a sum; 2 is a factor of the product.']),
             'honors': ('In the expression 5x + 3(x − 2), what is the coefficient of x after you simplify?', '8', ['5x + 3x − 6 = 8x − 6.', 'The coefficient of x is 8.'])}
    for lv in LV:
        p, a, st = parts[lv]
        o.add(U, sk, lv, 'short-answer', p, a, st, ['6.EE.A.2b'], ['vocabulary'], 'g6_expression_parts')


# ---------------------------------------------------------------------------------------------- #17 nets and coordinate polygons
def nets_polys(o, rng):
    U = 'geometry'
    nets = {'cp2': [(4, 3, 2), (5, 5, 5)], 'cp1': [(6, 4, 3), (8, 5, 2)], 'honors': [(10, 6, 4), (7, 3, 5)]}
    for lv in LV:
        for i, (l, w, h) in enumerate(nets[lv]):
            S = 2 * (l * w + l * h + w * h)
            fig = ('net', l, w, h, 'cm')
            if lv == 'honors' and i == 0:
                o.add(U, 8, lv, 'short-answer', 'The net folds into a box with no top. How many square centimeters of cardboard does the open box use?', str(S - l * w),
                      [f'Full surface area: 2({l}×{w} + {l}×{h} + {w}×{h}) = {S} cm².', f'No top: subtract one {l} by {w} face: {S} − {l * w} = {S - l * w} cm².'], ['6.G.A.4'], ['diagram', 'multistep'], 'g6_net_area', fig=fig)
            else:
                o.add(U, 8, lv, 'short-answer', 'The net folds into a rectangular prism. Find its surface area in square centimeters.', str(S),
                      [f'The net has two {l} by {w}, two {l} by {h} and two {w} by {h} rectangles.', f'2({l * w} + {l * h} + {w * h}) = {S} cm².'], ['6.G.A.4'], ['diagram'], 'g6_net_area', fig=fig)
    polys = {'cp2': [([(-3, -2), (4, -2), (4, 3), (-3, 3)], 'ABCD', 'side AB'), ([(-5, 1), (2, 1), (2, 5)], 'PQR', 'side PQ')],
             'cp1': [([(-4, -3), (3, -3), (3, 2), (-4, 2)], 'ABCD', 'perimeter'), ([(-2, -4), (-2, 3), (4, 3)], 'XYZ', 'area')],
             'honors': [([(-5, -4), (1, -4), (1, 0), (4, 0), (4, 4), (-5, 4)], 'ABCDEF', 'area'), ([(-4, -5), (5, -5), (5, -1), (-4, 3)], 'KLMN', 'side MN length?')]}
    for lv in LV:
        for pts, nm, ask in polys[lv]:
            fig = ('poly', pts, list(nm))
            if ask.startswith('side') and '?' not in ask:
                a, b = pts[0], pts[1]
                o.add(U, 6, lv, 'short-answer', f'Find the length of {ask} of polygon {nm}.', f'{abs(a[0] - b[0]) + abs(a[1] - b[1])} units',
                      [f'{ask[-2]}({a[0]}, {a[1]}) and {ask[-1]}({b[0]}, {b[1]}) have the same {"y" if a[1] == b[1] else "x"}-coordinate.', f'Length: |{a[0] if a[1] == b[1] else a[1]} − {b[0] if a[1] == b[1] else b[1]}| = {abs(a[0] - b[0]) + abs(a[1] - b[1])} units.'],
                      ['6.G.A.3'], ['diagram'], 'g6_coord_polygon', fig=fig)
            elif ask == 'perimeter':
                w, h = pts[1][0] - pts[0][0], pts[2][1] - pts[1][1]
                o.add(U, 6, lv, 'short-answer', f'Find the perimeter of rectangle {nm}.', f'{2 * (w + h)} units',
                      [f'Width: {pts[1][0]} − ({pts[0][0]}) = {w}; height: {pts[2][1]} − ({pts[1][1]}) = {h}.', f'Perimeter: 2({w} + {h}) = {2 * (w + h)} units.'], ['6.G.A.3'], ['diagram'], 'g6_coord_polygon', fig=fig)
            elif ask == 'area' and len(pts) == 3:
                b_, h_ = abs(pts[2][0] - pts[1][0]), abs(pts[1][1] - pts[0][1])
                o.add(U, 7, lv, 'short-answer', f'Find the area of right triangle {nm}.', f'{mixed(Fr(b_ * h_, 2))} square units',
                      [f'Legs: {h_} (vertical) and {b_} (horizontal).', f'Area: ½ × {b_} × {h_} = {mixed(Fr(b_ * h_, 2))} square units.'], ['6.G.A.3', '6.G.A.1'], ['diagram'], 'g6_coord_polygon', fig=fig)
            elif ask == 'area':
                A = 6 * 4 + 9 * 4
                o.add(U, 7, lv, 'short-answer', f'Find the area of polygon {nm}.', f'{A} square units',
                      ['Split it with a horizontal line at y = 0.', 'Bottom rectangle: 6 by 4 = 24. Top rectangle: 9 by 4 = 36.', f'Area: 24 + 36 = {A} square units.'], ['6.G.A.3', '6.G.A.1'], ['diagram', 'multistep'], 'g6_coord_polygon', fig=fig)
            else:
                o.add(U, 6, lv, 'short-answer', f'Polygon {nm} is a trapezoid. Find its area by splitting it into a rectangle and a triangle.', '54 square units',
                      ['Rectangle from y = −5 to y = −1: 9 by 4 = 36.', 'Triangle on top: base 9, height 4: ½ × 9 × 4 = 18.', 'Area: 36 + 18 = 54 square units.'], ['6.G.A.3', '6.G.A.1'], ['diagram', 'multistep'], 'g6_coord_polygon', fig=fig)


# ---------------------------------------------------------------------------------------------- #18 constructed response
CR = {
 ('ratios-rates-percent-proportions', 2): {
  'cp1': ('A smoothie shop sells a 16-ounce smoothie for $4.80 and a 24-ounce smoothie for $6.48.',
          [('What is the price per ounce of the 16-ounce smoothie?', '$0.30'), ('What is the price per ounce of the 24-ounce smoothie?', '$0.27'),
           ('Which size is the better buy?', '24-ounce'), ('How much would 48 ounces cost at the better unit price?', '$12.96')]),
  'honors': ('Store A sells 5 pounds of rice for $6.25. Store B sells 8 pounds for $9.60. A school kitchen needs 40 pounds.',
             [('Find the price per pound at Store A.', '$1.25'), ('Find the price per pound at Store B.', '$1.20'),
              ('How much does the kitchen save by buying all 40 pounds at the cheaper store?', '$2.00'), ('At the cheaper store, how many whole pounds can the kitchen buy for $50?', '41')])},
 ('fractions-decimals-operations', 3): {
  'cp1': ('A carpenter has a board 8 1/4 feet long. She cuts shelves that are each 1 3/4 feet long.',
          [('Write a division expression for the number of shelves.', '8 1/4 ÷ 1 3/4'), ('How many full shelves can she cut?', '4'),
           ('How many feet of board are left over?', '1 1/4'), ('What fraction of another shelf is the leftover piece?', '5/7')]),
  'honors': ('A recipe uses 2/3 cup of oats per batch. Jo has 5 1/2 cups of oats.',
             [('How many full batches can Jo make?', '8'), ('How many cups of oats are left after the full batches?', '1/6'),
              ('How many more cups of oats does Jo need to make one more batch?', '1/2'), ('If each batch makes 12 bars, how many bars do the full batches make?', '96')])},
 ('rational-numbers', 9): {
  'cp1': ('On a town map, the library is at (-4, 3), the school is at (5, 3) and the park is at (5, -6). Each unit is 1 block.',
          [('How many blocks is it from the library to the school?', '9'), ('How many blocks is it from the school to the park?', '9'),
           ('How many blocks is the walk library → school → park?', '18'), ('In which quadrant is the park?', 'Quadrant IV')]),
  'honors': ('A rectangle has vertices A(-6, -2), B(3, -2), C(3, 5) and D(-6, 5).',
             [('Find the length of side AB.', '9'), ('Find the length of side BC.', '7'),
              ('Find the perimeter of the rectangle.', '32'), ('The rectangle is reflected across the x-axis. What are the coordinates of the image of C?', '(3, -5)')])},
 ('expressions-equations', 7): {
  'cp1': ('A dog walker charges $8 per walk plus a one-time $5 sign-up fee.',
          [('Write an equation for the total cost c of w walks.', 'c = 8w + 5'), ('Which variable is independent?', 'w'),
           ('What is the cost of 6 walks?', '$53'), ('How many walks can a customer get for $93?', '11')]),
  'honors': ('A candle is 24 cm tall and burns 1.5 cm per hour.',
             [('Write an equation for the height h after t hours.', 'h = 24 - 1.5t'), ('What is the height after 6 hours?', '15'),
              ('After how many hours is the candle 9 cm tall?', '10'), ('After how many hours does the candle burn out?', '16')])},
 ('inequalities', 5): {
  'cp1': ('A van can carry at most 1,200 pounds. The driver weighs 180 pounds. Each box weighs 60 pounds.',
          [('Write an inequality for the number of boxes b.', '180 + 60b ≤ 1200'), ('Solve the inequality.', 'b ≤ 17'),
           ('What is the greatest number of boxes?', '17'), ('Is 18 boxes allowed?', 'No')]),
  'honors': ('Ana has $45 and wants to have at least $200 for a trip. She earns $12 per hour.',
             [('Write an inequality for the hours h she must work.', '45 + 12h ≥ 200'), ('Solve the inequality.', 'h ≥ 12 11/12'),
              ('What is the least whole number of hours?', '13'), ('How much money will she have after that many hours?', '$201')])},
 ('geometry', 8): {
  'cp1': ('A gift box is 10 in. long, 6 in. wide and 4 in. tall.',
          [('What is the area of the top face?', '60'), ('What is the area of one 10 in. by 4 in. side?', '40'),
           ('What is the surface area of the box?', '248'), ('Wrapping paper comes in 300-square-inch sheets. How many square inches are left from one sheet?', '52')]),
  'honors': ('A planter box is 3 1/2 ft long, 2 ft wide and 1 1/2 ft tall, with no top.',
             [('What is the volume of the planter?', '10 1/2'), ('What is the area of the bottom?', '7'),
              ('What is the total area of the four sides?', '16 1/2'), ('How many square feet of wood are needed (bottom and sides)?', '23 1/2')])},
 ('data-displays', 8): {
  'cp1': ('The ages of 8 people at a party are 12, 13, 13, 14, 14, 15, 16 and 41.',
          [('What is the mean age?', '17.25'), ('What is the median age?', '14'),
           ('Which value is an outlier?', '41'), ('Which measure better describes a typical age, the mean or the median?', 'median')]),
  'honors': ('Two classes took a quiz. Class A: 6, 7, 7, 8, 8, 9, 10. Class B: 4, 6, 8, 8, 9, 11, 10.',
             [('What is the mean of Class A?', '7 6/7'), ('What is the median of Class B?', '8'),
              ('What is the range of Class B?', '7'), ('Which class has the greater range, and by how much?', 'Class B, by 3')])},
}


def constructed(o, rng):
    for (u, sk), lv_map in CR.items():
        for lv, (stem, parts) in lv_map.items():
            ans = '; '.join(f'({"abcd"[i]}) {a}' for i, (_, a) in enumerate(parts))
            o.add(u, sk, lv, 'open-response', stem + ' Answer each part. Show your work.', ans,
                  [f'({"abcd"[i]}) {p} → {a}' for i, (p, a) in enumerate(parts)], STD_CR[u], ['multistep', 'context'], 'g6_constructed_response', parts=parts)


STD_CR = {'ratios-rates-percent-proportions': ['6.RP.A.3b'], 'fractions-decimals-operations': ['6.NS.A.1'], 'rational-numbers': ['6.NS.C.8', '6.NS.C.6b'],
          'expressions-equations': ['6.EE.C.9', '6.EE.B.7'], 'inequalities': ['6.EE.B.8', '7.EE.B.4b'], 'geometry': ['6.G.A.4', '6.G.A.2'], 'data-displays': ['6.SP.B.5c', '6.SP.B.5d']}


def draw(fig, path):
    k = fig[0]
    if k == 'line':
        _, pts, xm, ym, xl, yl, ys, lab = fig
        return figures.line_graph(path, [(float(a), float(b)) for a, b in pts], xm, ym, xl, yl, 1, ys, lab)
    if k == 'tape':
        return figures.tape_diagram(path, fig[1], fig[2], fig[3], fig[4])
    if k == 'dnl':
        return figures.double_number_line(path, *fig[1:])
    if k == 'bars':
        return figures.fraction_bars(path, *fig[1:])
    if k == 'dot':
        return figures.dot_plot(path, *fig[1:])
    if k == 'net':
        return figures.prism_net(path, *fig[1:])
    if k == 'poly':
        return figures.coord_polygon(path, fig[1], fig[2])
    raise ValueError(k)


FAMILIES = [percent_whole, dep_graphs, tape_models, double_lines, fraction_models, stats_subs, expr_unknowns, nets_polys, constructed]
GID = re.compile(r'-g\d{2}$')


def main():
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
    for fam in FAMILIES:
        fam(o, random.Random('g6-' + fam.__name__))
    count = {}
    for unit, skill, lv, q, tg, fig in o.items:
        key = (unit, skill, lv)
        count[key] = count.get(key, 0) + 1
        qid = f'm6-{lib.ABBR[unit]}-s{skill:02d}-{lv}-g{count[key]:02d}'
        q = dict(id=qid, **q)
        if fig:
            rel = f'question-banks/assets/math6/{unit}/{qid}.png'
            os.makedirs(os.path.dirname(os.path.join(lib.ROOT, rel)), exist_ok=True)
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
