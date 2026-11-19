"""8th Grade Math audit (2026-11-19), batch C.

#3  The 17 skills whose Advanced items were mostly lower-level templates with new numbers each get 8 new Advanced items
    (two multi-step or reverse-reasoning families, four items each, IDs -h01 to -h08). For every new item, one Advanced
    clone of a Support/Standard template moves to Standard (its ID is kept; short-answer clones move first so the
    Advanced multiple-choice pool for games stays full).
#14 Standard items that only re-numbered a Support template get one added step in their family (see STANDARD below).
Idempotent. Run from the repository root."""
import json, math, os, re, sys
from fractions import Fraction as Fr

sys.path.insert(0, os.path.dirname(__file__))
from lib import ROOT, load, save, items, family

NOTE = ('Original Claude-authored item (family: {fam}). 8th Grade Math audit 2026-11-19 (#3, Advanced); answer recomputed '
        'by scripts/test-grade8-audit.cjs.')
MOVED = ' Moved from Advanced to Standard (8th Grade Math audit #3, 2026-11-19): same template as a Support or Standard item.'


def F(x):
    x = Fr(x)
    return str(x.numerator) if x.denominator == 1 else f'{x.numerator}/{x.denominator}'


def par(v):
    return f'({F(v)})' if Fr(v) < 0 or Fr(v).denominator != 1 else F(v)


def sgn(b):
    return f'+ {F(b)}' if b >= 0 else f'- {F(-b)}'


def lin(m, b, v='x'):
    m, b = Fr(m), Fr(b)
    ms = '' if m == 1 else '-' if m == -1 else (f'({F(m)})' if m.denominator != 1 else F(m))
    s = f'{ms}{v}' if m != 0 else ''
    if b != 0 or not s:
        s = (s + ' ' + sgn(b)) if s else F(b)
    return s


def eqtxt(a, b, c):
    """a·x + b·y = c, written the usual way."""
    xs = lin(a, 0)
    ys = 'y' if abs(b) == 1 else f'{abs(b)}y'
    return f'{xs} {"+" if b > 0 else "-"} {ys} = {c}'


def mc(ans, wrong):
    out, seen = [], set()
    for t in [ans] + wrong:
        if t not in seen:
            seen.add(t); out.append(t)
    assert len(out) >= 4, (ans, wrong)
    out = out[:4]
    k = sum(map(ord, ans)) % 4      # deterministic position of the key
    out.remove(ans); out.insert(k, ans)
    return out


G = {}   # skill -> list of (family, format, prompt, answer, steps, options|None)

# ---------------- patterns-bivariate-data-skill-01: constructing scatter plots
L = []
for xs, ys in [([1, 2, 4, 5, 7, 9], [2, 1, 6, 4, 9, 8]), ([2, 3, 5, 6, 8, 10], [3, 1, 6, 7, 6, 12]), ([0, 3, 4, 6, 7, 11], [1, 2, 5, 5, 9, 10]), ([1, 4, 5, 8, 9, 12], [3, 2, 7, 6, 11, 10])]:
    above = sum(1 for x, y in zip(xs, ys) if y > x)
    L.append(('s1_above_line', 'short-answer', f'The data x: {", ".join(map(str, xs))}; y: {", ".join(map(str, ys))} is graphed as a scatter plot with the line y = x. How many points lie above the line?',
              str(above), [f'Points: {", ".join(f"({x}, {y})" for x, y in zip(xs, ys))}.', 'A point is above y = x when its y-value is greater than its x-value.',
                           f'Above: {", ".join(f"({x}, {y})" for x, y in zip(xs, ys) if y > x)}, so {above} points.'], None))
for m, b, bad in [(2, 1, 3), (3, -2, 5), (-2, 20, 2), (-3, 25, 4)]:
    xs = [1, 2, 3, 4, 5, 6]
    ys = [m * x + b for x in xs]
    ys[bad] += 9 if m > 0 else -9
    pts = [f'({x}, {y})' for x, y in zip(xs, ys)]
    out = pts[bad]
    L.append(('s1_outlier_pattern', 'multiple-choice', f'Data: x: {", ".join(map(str, xs))}; y: {", ".join(map(str, ys))}. When the data is graphed as a scatter plot, which point does not follow the pattern of the others?',
              out, [f'The other points rise by {m} for each step of 1 in x (y = {lin(m, b)}).' if m > 0 else f'The other points fall by {-m} for each step of 1 in x (y = {lin(m, b)}).', f'{out} is 9 units off that pattern.'],
              mc(out, [p_ for i, p_ in enumerate(pts) if i != bad][::2])))
G['patterns-bivariate-data-skill-01'] = L

# ---------------- patterns-bivariate-data-skill-02: patterns, outliers, predictions
L = []
for (x1, y1), (x2, y2), xp in [((2, 14), (8, 32), 12), ((1, 40), (6, 25), 10), ((3, 9), (9, 27), 14), ((0, 50), (5, 35), 12)]:
    m = Fr(y2 - y1, x2 - x1)
    yp = y1 + m * (xp - x1)
    L.append(('s2_extend_trend', 'short-answer', f'The points of a scatter plot follow a straight-line trend through ({x1}, {y1}) and ({x2}, {y2}). Predict y when x = {xp}.',
              F(yp), [f'Rate of the trend: ({y2} - {y1}) ÷ ({x2} - {x1}) = {F(m)}.', f'From ({x2}, {y2}): {y2} + {F(m)} × {xp - x2} = {F(yp)}.'], None))
for xs, ys, out in [([1, 2, 3, 4, 5, 6], [3, 5, 7, 25, 11, 13], 3), ([2, 4, 6, 8, 10, 12], [30, 26, 22, 18, 2, 10], 4), ([1, 3, 5, 7, 9, 11], [4, 7, 10, 13, 30, 19], 4), ([0, 2, 4, 6, 8, 10], [20, 17, 2, 11, 8, 5], 2)]:
    xm = sum(xs) / 6
    others = [(x, y) for i, (x, y) in enumerate(zip(xs, ys)) if i != out]
    m2 = Fr(others[-1][1] - others[0][1], others[-1][0] - others[0][0])
    L.append(('s2_outlier_mean', 'short-answer', f'Data: x: {", ".join(map(str, xs))}; y: {", ".join(map(str, ys))}. One point is an outlier. What is the mean of the y-values after removing it?',
              F(Fr(sum(y for _, y in others), 5)), [f'The other points change by {F(m2 * (xs[1] - xs[0]))} per step, so ({xs[out]}, {ys[out]}) is the outlier.',
                                                    f'Mean of the other five: ({" + ".join(str(y) for _, y in others)}) ÷ 5 = {F(Fr(sum(y for _, y in others), 5))}.'], None))
G['patterns-bivariate-data-skill-02'] = L

# ---------------- linear-functional-relationships-skill-08: increasing, decreasing, max, min
L = []
for pts in [[(-6, 2), (-3, -4), (1, 4), (3, 4), (7, -2)], [(-7, -3), (-4, 3), (-1, 1), (2, 7), (6, 0)], [(-5, 5), (-2, -1), (0, -1), (4, 7), (7, 1)], [(-8, 0), (-5, 6), (-1, -2), (3, 2), (6, 2)]]:
    inc = sum(b[0] - a[0] for a, b in zip(pts, pts[1:]) if b[1] > a[1])
    L.append(('s8_total_increasing', 'short-answer', f'A function is made of segments joining {", ".join(f"({x}, {y})" for x, y in pts)}. For how many units of x, in total, is it increasing?',
              f'{inc} units', ['Increasing pieces rise from left to right: ' + '; '.join(f'from x = {a[0]} to x = {b[0]}' for a, b in zip(pts, pts[1:]) if b[1] > a[1]) + '.',
                               ' + '.join(str(b[0] - a[0]) for a, b in zip(pts, pts[1:]) if b[1] > a[1]) + f' = {inc} units.'], None))
for pts in [[(0, 1), (2, 7), (5, 10), (6, 4)], [(-4, 0), (-2, 8), (3, 13), (5, 5)], [(0, 9), (3, 3), (4, 7), (8, 9)], [(-3, -5), (-1, 1), (5, 4), (7, -2)]]:
    rates = [Fr(b[1] - a[1], b[0] - a[0]) for a, b in zip(pts, pts[1:])]
    best = max(rates)
    L.append(('s8_greatest_rate', 'short-answer', f'A function is made of segments joining {", ".join(f"({x}, {y})" for x, y in pts)}. What is the greatest rate of increase on any segment?',
              F(best), ['Rates: ' + '; '.join(f'({b[1]} - {a[1]}) ÷ ({b[0]} - {a[0]}) = {F(r)}' for (a, b), r in zip(zip(pts, pts[1:]), rates)) + '.', f'The greatest is {F(best)}.'], None))
G['linear-functional-relationships-skill-08'] = L

# ---------------- linear-functional-relationships-skill-07: tables of linear functions
L = []
for xs, ys, ask in [([-3, 1, 9], [10, 4, None], 2), ([-6, -2, 10], [-7, -4, None], 2), ([4, 10, 22], [3, None, 13], 1), ([-5, 3, 7], [None, -6, -10], 0)]:
    known = [(x, y) for x, y in zip(xs, ys) if y is not None]
    m = Fr(known[1][1] - known[0][1], known[1][0] - known[0][0])
    val = known[0][1] + m * (xs[ask] - known[0][0])
    shown = ['?' if y is None else str(y) for y in ys]
    L.append(('s7_uneven_missing', 'short-answer', f'The table shows a linear function. x: {", ".join(map(str, xs))}; y: {", ".join(shown)}. Find the missing value.',
              F(val), [f'Rate from the two known pairs: ({known[1][1]} - {known[0][1]}) ÷ ({known[1][0]} - {known[0][0]}) = {F(m)}.', f'At x = {xs[ask]}: {known[0][1]} + {par(m)}({xs[ask]} - {par(known[0][0])}) = {F(val)}.'], None))
for m, b, xs, target in [(Fr(3, 2), -4, [2, 6, 10], 11), (Fr(-5, 2), 30, [0, 4, 8], -5), (Fr(2, 3), 1, [3, 9, 12], 13), (-3, 7, [1, 4, 6], -26)]:
    ys = [m * x + b for x in xs]
    xa = (target - b) / m
    L.append(('s7_solve_from_table', 'short-answer', f'The table shows a linear function. x: {", ".join(map(str, xs))}; y: {", ".join(F(y) for y in ys)}. For what x is y = {target}?',
              f'x = {F(xa)}', [f'Rate: ({F(ys[1])} - {F(ys[0])}) ÷ ({xs[1]} - {xs[0]}) = {F(m)}; rule y = {lin(m, b)}.', f'{lin(m, b)} = {target}, so x = {F(xa)}.'], None))
G['linear-functional-relationships-skill-07'] = L

# ---------------- systems-linear-equations-skill-06: applications
L = []
for n, cents, q in [(30, 510, 14), (24, 405, 11), (40, 580, 12), (35, 650, 20)]:
    d = n - q
    assert 10 * d + 25 * q == cents
    L.append(('s6_coins', 'short-answer', f'A jar has {n} coins, all dimes and quarters, worth ${cents / 100:.2f}. How many quarters are there?',
              str(q), [f'd + q = {n} and 10d + 25q = {cents} (in cents).', f'Substitute d = {n} - q: 10({n} - q) + 25q = {cents}, so 15q = {cents - 10 * n}.', f'q = {q} quarters.'], None))
for f1, r1, f2, r2 in [(30, 8, 12, 11), (45, 5, 15, 8), (20, 15, 60, 10), (100, 12, 40, 17)]:
    t = Fr(f2 - f1, r1 - r2)
    c = f1 + r1 * t
    L.append(('s6_equal_cost', 'short-answer', f'Plan A costs ${f1} plus ${r1} per month. Plan B costs ${f2} plus ${r2} per month. What is the total cost when the two plans cost the same?',
              f'${F(c)}', [f'{f1} + {r1}m = {f2} + {r2}m gives m = {F(t)} months.', f'Cost: {f1} + {r1}({F(t)}) = ${F(c)}.'], None))
G['systems-linear-equations-skill-06'] = L

# ---------------- systems-linear-equations-skill-04: elimination
L = []
for (a1, b1), (a2, b2), (x, y) in [((3, 2), (5, -3), (4, 2)), ((2, 5), (3, -4), (-2, 3)), ((4, 3), (6, 5), (1, -2)), ((5, -2), (3, 4), (2, 3))]:
    c1, c2 = a1 * x + b1 * y, a2 * x + b2 * y
    L.append(('s4_two_multipliers', 'short-answer', f'Solve by elimination, multiplying both equations first: {eqtxt(a1, b1, c1)} and {eqtxt(a2, b2, c2)}',
              f'({x}, {y})', [f'Multiply the first equation by {abs(b2)} and the second by {abs(b1)} so the y-terms are opposites (or equal).', f'Eliminate y and solve: x = {x}.', f'Substitute: y = {y}. Solution ({x}, {y}).'], None))
for (a1, c1), (a2, c2), (pa, pc) in [((3, 2), (2, 5), (9, 7)), ((4, 3), (2, 5), (12, 8)), ((5, 2), (3, 4), (8, 6)), ((2, 3), (4, 5), (15, 10))]:
    t1, t2 = a1 * pa + c1 * pc, a2 * pa + c2 * pc
    L.append(('s4_ticket_context', 'short-answer', f'{a1} adult tickets and {c1} child tickets cost ${t1}. {a2} adult tickets and {c2} child tickets cost ${t2}. What does one child ticket cost?',
              f'${pc}', [f'{a1}a + {c1}c = {t1} and {a2}a + {c2}c = {t2}.', f'Multiply to match the a-terms and subtract: c = {pc}.', f'One child ticket costs ${pc} (an adult ticket costs ${pa}).'], None))
G['systems-linear-equations-skill-04'] = L

# ---------------- linear-functional-relationships-skill-04: slope
L = []
for (x1, x2), d, m in [((1, 5), 3, 2), ((-2, 4), -1, Fr(1, 2)), ((0, 3), 6, -3), ((2, 8), 1, Fr(-1, 3))]:
    # line through (x1, k) and (x2, 2k + d) with slope m: (k + d) = m (x2 - x1)
    k = m * (x2 - x1) - d
    L.append(('s4_missing_k', 'short-answer', f'The line through ({x1}, k) and ({x2}, 2k {sgn(d)}) has slope {F(m)}. Find k.',
              f'k = {F(k)}', [f'Slope = (2k {sgn(d)} - k) ÷ ({x2} - {x1}) = (k {sgn(d)}) ÷ {x2 - x1}.', f'(k {sgn(d)}) ÷ {x2 - x1} = {F(m)}, so k {sgn(d)} = {F(m * (x2 - x1))} and k = {F(k)}.'], None))
for p, q, r in [((Fr(1, 2), 3), (Fr(5, 2), 7), 'fractions'), ((Fr(-3, 2), 1), (Fr(1, 2), -5), 'fractions'), ((Fr(1, 3), 2), (Fr(4, 3), 4), 'fractions'), ((Fr(-1, 4), -2), (Fr(3, 4), 1), 'fractions')]:
    m = Fr(q[1] - p[1]) / (q[0] - p[0])
    L.append(('s4_fraction_points', 'short-answer', f'Find the slope of the line through ({F(p[0])}, {p[1]}) and ({F(q[0])}, {q[1]}).',
              F(m), [f'Rise: {q[1]} - {p[1]} = {q[1] - p[1]}. Run: {F(q[0])} - {F(p[0])} = {F(q[0] - p[0])}.', f'Slope = {q[1] - p[1]} ÷ {par(q[0] - p[0])} = {F(m)}.'], None))
G['linear-functional-relationships-skill-04'] = L

# ---------------- geometry-applications-skill-07: composite solids
L = []
for r, h in [(3, 10), (2, 7), (4, 5), (5, 12)]:
    v = Fr(r * r * h) + Fr(4, 3) * r ** 3
    L.append(('s7_capsule', 'short-answer', f'A capsule is a cylinder (radius {r} cm, length {h} cm) with a hemisphere on each end. Find its volume in terms of π.',
              f'({F(v)})π cubic centimeters' if v.denominator != 1 else f'{F(v)}π cubic centimeters', [f'Cylinder: π({r}²)({h}) = {r * r * h}π.', f'Two hemispheres make one sphere: (4/3)π({r}³) = {par(Fr(4, 3) * r ** 3)}π.',
                                                                                           f'Total: {par(v)}π cubic centimeters.'], None))
for R, r, h in [(5, 3, 10), (4, 2, 9), (6, 5, 8), (7, 4, 6)]:
    v = (R * R - r * r) * h
    L.append(('s7_pipe', 'short-answer', f'A pipe is a cylinder of radius {R} cm and length {h} cm with a cylindrical hole of radius {r} cm through its center. Find the volume of material in terms of π.',
              f'{v}π cubic centimeters', [f'Outer cylinder: π({R}²)({h}) = {R * R * h}π.', f'Hole: π({r}²)({h}) = {r * r * h}π.', f'Material: {R * R * h}π - {r * r * h}π = {v}π cubic centimeters.'], None))
G['geometry-applications-skill-07'] = L

# ---------------- real-numbers-exponents-skill-03: fractions and decimals
L = []
for a, b, f in [('0.2333…', '3', Fr(7, 30)), ('0.1666…', '6', Fr(1, 6)), ('0.8333…', '3', Fr(5, 6)), ('0.4111…', '1', Fr(37, 90))]:
    L.append(('s3_mixed_repeat', 'short-answer', f'In {a}, only the digit {b} repeats; the digit before it does not. Write the number as a fraction in simplest form.',
              F(f), [f'Let n = {a}. Then 100n - 10n removes the repeating part: 90n = {F(f * 90)}.', f'n = {F(f * 90)}/90 = {F(f)}.'], None))
for num, den, k in [(3, 7, 20), (2, 7, 15), (5, 11, 25), (4, 13, 30)]:
    digs = ''
    rem = num % den
    while len(digs) < 60:
        rem *= 10; digs += str(rem // den); rem %= den
    period = next(p for p in range(1, 13) if all(digs[i] == digs[i + p] for i in range(30)))
    d = digs[k - 1]
    L.append(('s3_nth_digit', 'short-answer', f'{num}/{den} = 0.{digs[:period]}… with the block {digs[:period]} repeating. What is the {k}th digit after the decimal point?',
              d, [f'The block has {period} digits.', f'{k} ÷ {period} leaves remainder {k % period or period}, so the digit is digit {k % period or period} of the block: {d}.'], None))
G['real-numbers-exponents-skill-03'] = L

# ---------------- linear-functional-relationships-skill-03: linear or nonlinear
L = []
for xs, ys in [([0, 2, 5, 6], [1, 5, 11, 13]), ([-1, 1, 4, 5], [7, 3, -3, -5]), ([0, 1, 3, 6], [2, 3, 7, 14]), ([2, 3, 5, 8], [1, 4, 8, 14])]:
    rates = [Fr(ys[i + 1] - ys[i], xs[i + 1] - xs[i]) for i in range(3)]
    ans = 'linear' if len(set(rates)) == 1 else 'nonlinear'
    L.append(('s3_uneven_steps', 'short-answer', f'Does the table represent a linear or nonlinear function? x: {", ".join(map(str, xs))}; y: {", ".join(map(str, ys))}',
              ans, [f'The x-steps are not all 1, so compare Δy ÷ Δx: {", ".join(F(r) for r in rates)}.', f'The rates are {"all equal" if ans == "linear" else "not all equal"}, so the function is {ans}.'], None))
for xs, m, b, miss in [([0, 3, 4, 8], 2, -1, 2), ([1, 2, 6, 7], -3, 10, 2), ([-2, 0, 5, 6], Fr(1, 2), 4, 2), ([-4, -1, 2, 8], Fr(-2, 3), 1, 1)]:
    ys = [m * x + b for x in xs]
    shown = [F(y) if i != miss else '?' for i, y in enumerate(ys)]
    L.append(('s3_complete_uneven', 'short-answer', f'The table is meant to show a linear function. x: {", ".join(map(str, xs))}; y: {", ".join(shown)}. What value of ? makes it linear?',
              F(ys[miss]), [f'Rate from two known pairs: {F(m)}.', f'At x = {xs[miss]}: y = {F(m)}({xs[miss]}) {sgn(b)} = {F(ys[miss])}.'], None))
G['linear-functional-relationships-skill-03'] = L

# ---------------- linear-functional-relationships-skill-01: functions
L = []
for m, b, x0, add in [(3, -5, 2, 12), (4, 1, -1, 20), (-2, 7, 3, -8), (5, -3, 0, 15)]:
    xa = Fr(m * x0 + add, m)
    L.append(('s1_reverse_eval', 'short-answer', f'For f(x) = {lin(m, b)}, find the value of x for which f(x) = f({x0}) {sgn(add)}.',
              f'x = {F(xa)}', [f'f({x0}) = {m * x0 + b}, so f(x) = {m * x0 + b + add}.', f'{lin(m, b)} = {m * x0 + b + add}, so x = {F(xa)}.'], None))
for pairs, ans in [([(1, 4), (3, 'a'), (5, 8), (3, 7)], 7), ([(-2, 'a'), (0, 5), (4, 1), (-2, -6)], -6), ([(2, 9), (6, 'a'), (6, 3), (8, 0)], 3), ([(7, 1), (4, 'a'), (1, 1), (4, -2)], -2)]:
    rel = '{' + ', '.join(f'({x}, {y})' for x, y in pairs) + '}'
    L.append(('s1_function_value', 'short-answer', f'The relation {rel} is a function. What is the value of a?',
              f'a = {ans}', ['In a function each input has exactly one output.', f'The input {next(x for x, y in pairs if y == "a")} also appears with output {ans}, so a = {ans}.'], None))
G['linear-functional-relationships-skill-01'] = L

# ---------------- congruence-similarity-skill-01: identifying transformations
L = []
for A, B, kind in [((2, 3), (5, 1), 'r90'), ((-1, 4), (3, 2), 'r270'), ((2, -5), (4, 1), 'yx'), ((3, 1), (-2, 4), 'r180')]:
    f = {'r90': lambda p: (-p[1], p[0]), 'r270': lambda p: (p[1], -p[0]), 'yx': lambda p: (p[1], p[0]), 'r180': lambda p: (-p[0], -p[1])}[kind]
    name = {'r90': 'rotation 90° counterclockwise about the origin', 'r270': 'rotation 90° clockwise about the origin', 'yx': 'reflection over the line y = x', 'r180': 'rotation 180° about the origin'}[kind]
    rule = {'r90': '(x, y) → (-y, x)', 'r270': '(x, y) → (y, -x)', 'yx': '(x, y) → (y, x)', 'r180': '(x, y) → (-x, -y)'}[kind]
    L.append(('s1_rule_from_two_points', 'multiple-choice', f'A transformation maps A{A} to A′{f(A)} and B{B} to B′{f(B)}. Which single transformation is it?',
              name, [f'Compare coordinates: A{A} → A′{f(A)} and B{B} → B′{f(B)}.', f'Both follow {rule}, so it is a {name}.'],
              mc(name, ['rotation 90° counterclockwise about the origin', 'rotation 90° clockwise about the origin', 'reflection over the line y = x', 'rotation 180° about the origin', 'reflection over the x-axis'])))
for k, A in [(3, (2, -1)), (Fr(1, 2), (6, 4)), (2, (-3, 5)), (Fr(3, 2), (4, -2))]:
    img = (k * A[0], k * A[1])
    L.append(('s1_dilation_or_not', 'short-answer', f'A transformation maps every point (x, y) to ({F(k)}x, {F(k)}y). Point A{A} maps to A′({F(img[0])}, {F(img[1])}). Is the image congruent to the original? Answer yes or no.',
              'no', [f'The rule multiplies both coordinates by {F(k)}: a dilation with scale factor {F(k)} centered at the origin.', f'A scale factor other than 1 changes lengths, so the image is similar but not congruent: no.'], None))
G['congruence-similarity-skill-01'] = L

# ---------------- linear-functional-relationships-skill-05: equations of lines
L = []
for (a, b, c), (px, py) in [((2, -3, 6), (3, -1)), ((4, 2, 10), (-1, 5)), ((1, -2, 8), (4, 0)), ((3, 4, 12), (-4, 2))]:
    m = Fr(-a, b)
    bb = py - m * px
    L.append(('s5_same_rate_point', 'short-answer', f'Write, in slope-intercept form, the line through ({px}, {py}) with the same rate of change as {eqtxt(a, b, c)}.',
              f'y = {lin(m, bb)}', [f'Solve the given equation for y: the slope is {F(m)}.', f'{py} = {F(m)}({px}) + b, so b = {F(bb)}.', f'y = {lin(m, bb)}.'], None))
for (m1, c1), (m2, c2) in [((3, 115), (8, 240)), ((5, 62), (12, 97)), ((2, 31), (10, 47)), ((6, 84), (15, 120))]:
    m = Fr(c2 - c1, m2 - m1)
    b = c1 - m * m1
    L.append(('s5_two_points_context', 'short-answer', f'A tank\'s water level (cm) is a linear function of time t (minutes). It is {c1} cm after {m1} minutes and {c2} cm after {m2} minutes. Write an equation for the level L.',
              f'L = {lin(m, b, "t")}', [f'Rate: ({c2} - {c1}) ÷ ({m2} - {m1}) = {F(m)} cm per minute.', f'Starting level: {c1} - {F(m)}({m1}) = {F(b)}.', f'L = {lin(m, b, "t")}.'], None))
G['linear-functional-relationships-skill-05'] = L

# ---------------- geometry-applications-skill-05: volume
L = []
for d in [12, 18, 6, 24]:
    r = d // 2
    v = Fr(4, 3) * r ** 3
    L.append(('s5_sphere_diameter', 'short-answer', f'A sphere has diameter {d} cm. Find its volume in terms of π.',
              f'{F(v)}π cubic centimeters', [f'Radius = {d} ÷ 2 = {r} cm.', f'V = (4/3)π({r}³) = {F(v)}π cubic centimeters.'], None))
for (R, H), (r, h) in [((6, 10), (2, 5)), ((4, 9), (2, 3)), ((9, 8), (3, 4)), ((10, 12), (5, 6))]:
    n = Fr(R * R * H * 3, r * r * h)
    L.append(('s5_cones_fill', 'short-answer', f'A cylindrical tank has radius {R} ft and height {H} ft. A cone-shaped bucket has radius {r} ft and height {h} ft. How many full buckets fill the tank?',
              F(n), [f'Tank: π({R}²)({H}) = {R * R * H}π.', f'Bucket: (1/3)π({r}²)({h}) = {par(Fr(r * r * h, 3))}π.', f'{R * R * H}π ÷ {par(Fr(r * r * h, 3))}π = {F(n)} buckets.'], None))
G['geometry-applications-skill-05'] = L

# ---------------- congruence-similarity-skill-08: similar triangles
L = []
for p1, p2, s in [(24, 36, 10), (30, 45, 8), (20, 50, 6), (18, 27, 12)]:
    t = Fr(s * p2, p1)
    L.append(('s8_perimeter_side', 'short-answer', f'Two similar triangles have perimeters {p1} cm and {p2} cm. A side of the smaller triangle is {s} cm. How long is the matching side of the larger triangle?',
              f'{F(t)} cm', [f'Scale factor = {p2} ÷ {p1} = {F(Fr(p2, p1))}.', f'{s} × {F(Fr(p2, p1))} = {F(t)} cm.'], None))
for bc, bd, ce in [(6, 4, 10), (9, 6, 15), (4, 3, 7), (10, 8, 18)]:
    x = Fr(bd * bc, ce - bd)
    L.append(('s8_nested_unknown', 'short-answer', f'In triangle ACE, BD is parallel to CE with B on AC and D on AE. AB = x, BC = {bc}, BD = {bd} and CE = {ce}. Find x.',
              f'x = {F(x)}', ['Triangle ABD ~ triangle ACE (AA), so AB/AC = BD/CE.', f'x/(x + {bc}) = {bd}/{ce}, so {ce}x = {bd}x + {bd * bc}.', f'{ce - bd}x = {bd * bc}, so x = {F(x)}.'], None))
G['congruence-similarity-skill-08'] = L

# ---------------- linear-functional-relationships-skill-06: graphs, intercepts
L = []
for a, b, c in [(3, -4, 18), (5, 2, 30), (-2, 7, 14), (6, -5, -24)]:
    xi, yi = Fr(c, a), Fr(c, b)
    area = abs(xi) * abs(yi) / 2
    L.append(('s6_intercept_triangle', 'short-answer', f'The graph of {eqtxt(a, b, c)} and the two axes form a triangle. Find its area.',
              f'{F(area)} square units', [f'x-intercept: set y = 0, so {a}x = {c} and x = {F(xi)}.', f'y-intercept: set x = 0, so {b}y = {c} and y = {F(yi)}.',
                                        f'The legs are {F(abs(xi))} and {F(abs(yi))}: area = (1/2)({F(abs(xi))})({F(abs(yi))}) = {F(area)} square units.'], None))
for bb, (px, py) in [(4, (6, -2)), (-3, (4, 5)), (1, (-2, 9)), (-5, (3, -1))]:
    m = Fr(py - bb, px)
    L.append(('s6_slope_from_point', 'short-answer', f'The graph of y = mx {sgn(bb)} passes through ({px}, {py}). Find m.',
              f'm = {F(m)}', [f'Substitute: {py} = m({px}) {sgn(bb)}.', f'{px}m = {py - bb}, so m = {F(m)}.'], None))
G['linear-functional-relationships-skill-06'] = L

# ---------------- geometry-applications-skill-04: distance
L = []
for (x1, y1), y2, d in [((1, 2), 6, 5), ((-2, 3), -9, 13), ((0, -4), 4, 10), ((3, 1), 9, 17)]:
    dy = y2 - y1
    dx = math.isqrt(d * d - dy * dy)
    k = x1 + dx
    L.append(('s4_find_k', 'short-answer', f'The distance between ({x1}, {y1}) and (k, {y2}) is {d} units, and k > {x1}. Find k.',
              f'k = {k}', [f'Vertical leg: |{y2} - {y1}| = {abs(dy)}.', f'Horizontal leg: √({d}² - {abs(dy)}²) = {dx}.', f'k = {x1} + {dx} = {k}.'], None))
for a, b in [(4, 8), (6, 8), (2, 6), (10, 4)]:
    # point (x, 0) equidistant from (0, a) and (b, 0): x² + a² = (b - x)²  =>  x = (b² - a²) / (2b)
    x = Fr(b * b - a * a, 2 * b)
    L.append(('s4_equidistant', 'short-answer', f'Find the point on the x-axis that is the same distance from (0, {a}) as from ({b}, 0).',
              f'({F(x)}, 0)', [f'For (x, 0): x² + {a}² = ({b} - x)².', f'x² + {a * a} = {b * b} - {2 * b}x + x², so {2 * b}x = {b * b - a * a}.', f'x = {F(x)}; the point is ({F(x)}, 0).'], None))
G['geometry-applications-skill-04'] = L

TARGETS = list(G)


def mask(s):
    return re.sub(r'-?\d+(\.\d+)?', '#', s)


def run():
    banks = load()
    unit_of = {sk: sk.rsplit('-skill-', 1)[0] for sk in TARGETS}
    abbr = {'real-numbers-exponents': 'rne', 'equations-expressions': 'eqx', 'linear-functional-relationships': 'lfr', 'systems-linear-equations': 'sys',
            'patterns-bivariate-data': 'biv', 'congruence-similarity': 'cgs', 'geometry-applications': 'geo'}
    added = moved = 0
    for sk in TARGETS:
        unit = unit_of[sk]
        bank = banks[unit]['questions']
        n = sk.rsplit('-skill-', 1)[1]
        new = G[sk]
        assert len(new) == 8, sk
        lower = {mask(q['prompt']) for q in bank if q['skillId'] == sk and q['level'] in ('cp2', 'cp1')}
        for i, (fam, fmt, prompt, ans, steps, opts) in enumerate(new):
            qid = f'pa8-{abbr[unit]}-s{n}-honors-h{i + 1:02d}'
            q = {'id': qid, 'skillId': sk, 'level': 'honors', 'format': fmt, 'prompt': prompt, 'answer': ans}
            if opts:
                q['options'] = [{'text': t, 'correct': t == ans} for t in opts]
            std = next(x['standards'] for x in bank if x['skillId'] == sk)
            q.update({'solutionSteps': steps, 'standards': std, 'sourceNotes': NOTE.format(fam=fam)})
            assert mask(prompt) not in lower, (qid, prompt)
            old = next((x for x in bank if x['id'] == qid), None)
            if old:
                old.clear(); old.update(q)
            else:
                idx = max(j for j, x in enumerate(bank) if x['skillId'] == sk and x['level'] == 'honors')
                bank.insert(idx + 1, q); added += 1
        # move the same number of Advanced clones to Standard (short answer first; keep at least 6 Advanced multiple choice)
        already = sum(1 for q in bank if q['skillId'] == sk and MOVED.strip() in q.get('sourceNotes', ''))
        need = len(new) - already
        if need <= 0:
            continue
        clones = [q for q in bank if q['skillId'] == sk and q['level'] == 'honors' and mask(q['prompt']) in lower and q['format'] in ('short-answer', 'multiple-choice')
                  and not re.search(r'_(error|select|open)', family(q)) and '-h' not in q['id'][-4:]]
        clones.sort(key=lambda q: (q['format'] != 'short-answer', q['id']))
        mcs = sum(1 for q in bank if q['skillId'] == sk and q['level'] == 'honors' and q['format'] == 'multiple-choice')
        for q in clones:
            if need <= 0:
                break
            if q['format'] == 'multiple-choice':
                if mcs <= 6:
                    continue
                mcs -= 1
            q['level'] = 'cp1'
            q['sourceNotes'] = q.get('sourceNotes', '') + MOVED
            need -= 1; moved += 1
    save(banks)
    return added, moved


# ======================================================================= #14 Standard: one added step
STD_NOTE = ' Standard version with an added step (8th Grade Math audit #14, 2026-11-19).'


def table_of(p):
    m = re.search(r'x: ([-\d, ]+); y: ([-\d?, ]+)', p)
    xs = [int(v) for v in m.group(1).split(',')]
    ys = [None if v.strip() == '?' else int(v) for v in m.group(2).split(',')]
    return xs, ys


def keyed(q, ans, wrong):
    q['answer'] = ans
    if q['format'] == 'multiple-choice':
        q['options'] = [{'text': t, 'correct': t == ans} for t in mc(ans, wrong)]


def std_s7_missing(q):
    xs, ys = table_of(q['prompt'])
    k = [(x, y) for x, y in zip(xs, ys) if y is not None]
    m = Fr(k[1][1] - k[0][1], k[1][0] - k[0][0]); b = k[0][1] - m * k[0][0]
    ys = [m * x + b for x in xs]
    X = xs[-1] + 2 * (xs[1] - xs[0])
    Y = m * X + b
    q['prompt'] = f'The table shows a linear function. x: {", ".join(map(str, xs))}; y: {", ".join(F(y) for y in ys)}. Find y when x = {X}.'
    q['solutionSteps'] = [f'Rate of change: ({F(ys[1])} - {par(ys[0])}) ÷ ({xs[1]} - {par(xs[0])}) = {F(m)}.', f'Rule: y = {lin(m, b)}.', f'At x = {X}: y = {F(Y)}.']
    keyed(q, F(Y), [F(Y + m), F(Y - m), F(-Y)])


def std_s6_graph(q):
    m_ = re.search(r'at \(0, (-?\d+)\) and passing through \((-?\d+), (-?\d+)\)', q['diagram']['spec']['alt'])
    b, x1, y1 = map(int, m_.groups())
    m = Fr(y1 - b, x1)
    X = 4 * m.denominator if 4 * m.denominator != x1 else 6 * m.denominator
    Y = m * X + b
    q['prompt'] = f'Use the graphed line to find the value of y when x = {X}.'
    q['solutionSteps'] = [f'y-intercept: (0, {b}).', f'From (0, {b}) to ({x1}, {y1}): slope {F(m)}, so y = {lin(m, b)}.', f'At x = {X}: y = {par(m)}({X}) {sgn(b)} = {F(Y)}.']
    keyed(q, F(Y), [F(Y - 2 * b), F(-m * X + b), F(X + b)])


def std_s8_perimeter(q):
    m_ = re.search(r'AB = (\d+), BC = (\d+), CA = (\d+), and (DE|EF|FD) = (\d+)\. Find x = (\w+)\.', q['prompt'])
    ab, bc, ca, nm, v, _ = m_.groups()
    ab, bc, ca, v = int(ab), int(bc), int(ca), int(v)
    k = Fr(v, {'DE': ab, 'EF': bc, 'FD': ca}[nm])
    per = k * (ab + bc + ca)
    q['prompt'] = q['prompt'].replace(m_.group(0), f'AB = {ab}, BC = {bc}, CA = {ca}, and {nm} = {v}. Find the perimeter of triangle DEF.')
    q['solutionSteps'] = [f'Scale factor = {nm} ÷ {({"DE": "AB", "EF": "BC", "FD": "CA"})[nm]} = {F(k)}.', f'Perimeter of ABC: {ab} + {bc} + {ca} = {ab + bc + ca}.', f'Perimeter of DEF: {F(k)} × {ab + bc + ca} = {F(per)}.']
    keyed(q, F(per), [str(ab + bc + ca), F(per + k), F(per - ab)])


def std_two_points(q):
    pts = [(int(a), int(b)) for a, b in re.findall(r'\((-?\d+), (-?\d+)\)', q['prompt'])[:2]]
    (x1, y1), (x2, y2) = pts
    m = Fr(y2 - y1, x2 - x1); b = y1 - m * x1
    X = 4 if 4 not in (x1, x2) else 5
    Y = m * X + b
    q['prompt'] = f'A line passes through ({x1}, {y1}) and ({x2}, {y2}). Find the y-value of the point on the line with x = {X}.'
    q['solutionSteps'] = [f'Slope: ({y2} - {par(y1)}) ÷ ({x2} - {par(x1)}) = {F(m)}.', f'y-intercept: {y1} - {par(m)} · {par(x1)} = {F(b)}, so y = {lin(m, b)}.', f'At x = {X}: y = {F(Y)}.']
    keyed(q, F(Y), [F(-m * X + b), F(m * X - b) if b else F(Y + 1), F(Y + m)])


def std_rate_after(q):
    m_ = re.search(r'(\$?)(\d+)( miles)? after (\d+) (\w+?)s? and \$?(\d+)(?: miles)? after (\d+)', q['prompt'])
    dol, a, _, t1, unit, b2, t2 = m_.groups()
    a, t1, b2, t2 = int(a), int(t1), int(b2), int(t2)
    r = Fr(b2 - a, t2 - t1)
    N = t2 + 3
    amt = b2 + r * 3
    fmt = (lambda v: f'${F(v)}') if dol else (lambda v: f'{F(v)} miles')
    q['prompt'] = re.sub(r'Find the .*$', f'How much will it be after {N} {unit}s?' if dol else f'How far will it have traveled after {N} {unit}s?', q['prompt'])
    q['solutionSteps'] = [f'Rate = ({b2} - {a}) ÷ ({t2} - {t1}) = {F(r)} per {unit}.', f'After {N} {unit}s: {b2} + {F(r)} × {N - t2} = {F(amt)}.']
    keyed(q, fmt(amt), [fmt(r * N), fmt(b2 + r * N), fmt(amt - r)])


def std_distribute(q):
    m_ = re.search(r'rewrite (\d+)\(x ([+-]) (\d+)\)', q['prompt'])
    a, op, c = int(m_.group(1)), m_.group(2), int(m_.group(3))
    c = c if op == '+' else -c
    k = 2 if a > 3 else -1
    co, const = a - k, a * c
    q['prompt'] = f'Use the distributive property to rewrite {a}(x {op} {abs(c)}) - {k}x, then combine like terms.'.replace('- -1x', '+ x')
    q['solutionSteps'] = [f'Distribute: {a}x {sgn(const)} - {k}x.'.replace('- -1x', '+ x'), f'Combine the x-terms: {a}x - ({k}x) = {co}x.'.replace('- (-1x)', '+ x'), f'Result: {lin(co, const)}.']
    keyed(q, lin(co, const), [lin(a, const), lin(co, c), lin(a + k, const)])


STANDARD = {('linear-functional-relationships-skill-07', 's7_missing'): std_s7_missing,
            ('linear-functional-relationships-skill-06', 's6_equation_from_graph'): std_s6_graph,
            ('congruence-similarity-skill-08', 's8_missing_side'): std_s8_perimeter,
            ('linear-functional-relationships-skill-05', 's5_two_points'): std_two_points,
            ('linear-functional-relationships-skill-04', 's4_slope_points'): std_two_points,
            ('linear-functional-relationships-skill-09', 's9_from_two'): std_rate_after,
            ('equations-expressions-skill-05', 's5_distribute'): std_distribute}


def standard():
    banks = load()
    n = 0
    for unit, d in banks.items():
        qs = d['questions']
        cp2 = {(q['skillId'], mask(q['prompt'])) for q in qs if q['level'] == 'cp2'}
        for q in qs:
            fn = STANDARD.get((q['skillId'], family(q)))
            if not fn or q['level'] != 'cp1' or STD_NOTE.strip() in q.get('sourceNotes', '') or (q['skillId'], mask(q['prompt'])) not in cp2:
                continue
            try:
                before = json.dumps(q)
                fn(q)
            except (AttributeError, ValueError, ZeroDivisionError):
                q.clear(); q.update(json.loads(before)); continue    # a prompt this family's parser does not read
            q['sourceNotes'] = q.get('sourceNotes', '') + STD_NOTE
            n += 1
        for q in qs:   # "after 1 hours" → "after 1 hour"
            for k in ('prompt',):
                q[k] = re.sub(r'\b1 (hour|minute|week|day|year|second|month)s\b', r'1 \1', q[k])
            q['solutionSteps'] = [re.sub(r'\b1 (hour|minute|week|day|year|second|month)s\b', r'1 \1', x) for x in q['solutionSteps']]
    save(banks)
    return n


if __name__ == '__main__':
    print('added, moved', run())
    print('standard rewritten', standard())
