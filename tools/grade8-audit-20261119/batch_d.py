"""8th Grade Math audit follow-up (2026-11-19), batch D: finish #3 for the other 37 skills.

For every skill not covered by batch C, count the Advanced short-answer and multiple-choice items that reuse a Support or
Standard template (select-all, error-analysis and open-response items share wording by design and are left alone). Write
that many new Advanced items (two multi-step or reverse-reasoning families per skill, IDs -h01, -h02, …) and move the
same number of reused items to Standard, IDs kept, short answer first, at least 6 Advanced multiple choice kept for games.
Deterministic and idempotent. Run from the repository root."""
import json, math, os, random, re, sys
from fractions import Fraction as Fr

sys.path.insert(0, os.path.dirname(__file__))
from lib import load, save, items, family
from batch_c import F, par, sgn, lin, eqtxt, mc, mask, MOVED

NOTE = ('Original Claude-authored item (family: {fam}). 8th Grade Math audit follow-up 2026-11-19 (Advanced, batch D); '
        'answer recomputed by scripts/test-grade8-audit.cjs.')
ABBR = {'real-numbers-exponents': 'rne', 'equations-expressions': 'eqx', 'linear-functional-relationships': 'lfr', 'systems-linear-equations': 'sys',
        'patterns-bivariate-data': 'biv', 'congruence-similarity': 'cgs', 'geometry-applications': 'geo'}


class Skip(Exception):
    pass


def need(c):
    if not c:
        raise Skip()


def P(p):
    return f'({F(p[0])}, {F(p[1])})'


def item(fam, prompt, ans, steps, opts=None):
    return (fam, 'multiple-choice' if opts else 'short-answer', prompt, ans, steps, opts)


R90 = {'90° counterclockwise': lambda p: (-p[1], p[0]), '180°': lambda p: (-p[0], -p[1]), '90° clockwise': lambda p: (p[1], -p[0])}
RULE = {'90° counterclockwise': '(x, y) → (-y, x)', '180°': '(x, y) → (-x, -y)', '90° clockwise': '(x, y) → (y, -x)'}

FAM = {}


def fam(skill):
    def deco(f):
        FAM.setdefault(skill, []).append(f)
        return f
    return deco


# ---------------------------------------------------------------- congruence and similarity
@fam('congruence-similarity-skill-02')
def cgs2_two_rotations(r):
    p = (r.randint(-7, 7), r.randint(-7, 7)); need(p[0] and p[1] and abs(p[0]) != abs(p[1]))
    a, b = r.sample(list(R90), 2)
    q = R90[b](R90[a](p))
    return item('s2_two_rotations', f'Point P{P(p)} is rotated {a} about the origin, then the image is rotated {b} about the origin. What are the final coordinates?',
                P(q), [f'First rotation, {RULE[a]}: {P(R90[a](p))}.', f'Second rotation, {RULE[b]}: {P(q)}.'])


@fam('congruence-similarity-skill-02')
def cgs2_undo(r):
    q = (r.randint(-8, 8), r.randint(-8, 8)); need(q[0] and q[1] and abs(q[0]) != abs(q[1]))
    a = r.choice(['90° clockwise', '90° counterclockwise'])
    back = {'90° clockwise': '90° counterclockwise', '90° counterclockwise': '90° clockwise'}[a]
    p = R90[back](q)
    wrong = [P(R90[a](q)), P((-q[0], -q[1])), P((q[1], q[0]))]
    return item('s2_original_from_image', f'After a rotation {a} about the origin, the image of point M is M′{P(q)}. Where was M before the rotation?',
                P(p), [f'Undo the rotation: rotate M′ {back}, {RULE[back]}.', f'M = {P(p)}. Check: rotating {P(p)} {a} gives {P(q)}.'], mc(P(p), wrong))


@fam('congruence-similarity-skill-03')
def cgs3_vertical_mirror(r):
    k = r.choice([-3, -2, -1, 1, 2, 3, 4]); p = (r.randint(-6, 6), r.randint(-6, 6)); need(p[0] != k)
    q = (2 * k - p[0], p[1])
    return item('s3_mirror_x_equals', f'Point P{P(p)} is reflected over the vertical line x = {k}. What are the coordinates of P′?',
                P(q), [f'P is {abs(p[0] - k)} units {"left" if p[0] < k else "right"} of x = {k}, so P′ is {abs(p[0] - k)} units on the other side.', f'x′ = 2({k}) - ({p[0]}) = {q[0]}; y stays {p[1]}: P′{P(q)}.'])


@fam('congruence-similarity-skill-03')
def cgs3_horizontal_mirror(r):
    k = r.choice([-4, -2, -1, 1, 2, 3]); p = (r.randint(-6, 6), r.randint(-6, 6)); need(p[1] != k)
    q = (p[0], 2 * k - p[1])
    return item('s3_mirror_y_equals', f'Point Q{P(p)} is reflected over the horizontal line y = {k}. What are the coordinates of Q′?',
                P(q), [f'Q is {abs(p[1] - k)} units {"below" if p[1] < k else "above"} y = {k}.', f'y′ = 2({k}) - ({p[1]}) = {q[1]}; x stays {p[0]}: Q′{P(q)}.'])


@fam('congruence-similarity-skill-04')
def cgs4_apply_found_rule(r):
    a = (r.randint(-5, 5), r.randint(-5, 5)); h, k = r.choice([-5, -4, -3, -2, 2, 3, 4, 5]), r.choice([-5, -4, -3, 3, 4, 5])
    b = (r.randint(-5, 5), r.randint(-5, 5)); need(a != b)
    a2, b2 = (a[0] + h, a[1] + k), (b[0] + h, b[1] + k)
    return item('s4_rule_then_apply', f'A translation maps A{P(a)} to A′{P(a2)}. Where does the same translation map B{P(b)}?',
                P(b2), [f'Rule: (x, y) → (x {sgn(h)}, y {sgn(k)}).', f'B′ = ({b[0]} {sgn(h)}, {b[1]} {sgn(k)}) = {P(b2)}.'])


@fam('congruence-similarity-skill-04')
def cgs4_reverse_composite(r):
    q = (r.randint(-6, 6), r.randint(-6, 6)); h = r.choice([2, 3, 4, 5]); k = r.choice([-3, -2, 2, 3])
    # P is translated h units left and k up, then reflected over the y-axis to Q
    t = (-q[0], q[1]); p = (t[0] + h, t[1] - k)
    return item('s4_reverse_then_reflect', f'Point P is translated {h} units left and {abs(k)} units {"up" if k > 0 else "down"}, then reflected over the y-axis. The final image is {P(q)}. Find P.',
                P(p), [f'Undo the reflection: {P(q)} → {P(t)}.', f'Undo the translation ({h} right, {abs(k)} {"down" if k > 0 else "up"}): P = {P(p)}.'])


@fam('congruence-similarity-skill-05')
def cgs5_center(r):
    c = (r.randint(-3, 3), r.randint(-3, 3)); p = (r.randint(-5, 5), r.randint(-5, 5)); k = r.choice([2, 3, Fr(1, 2)])
    need(c != (0, 0) and p != c and all((v - w) * k == int((v - w) * k) for v, w in zip(p, c)))
    q = (c[0] + k * (p[0] - c[0]), c[1] + k * (p[1] - c[1]))
    return item('s5_center_not_origin', f'Point P{P(p)} is dilated with scale factor {F(k)} centered at C{P(c)}. What are the coordinates of P′?',
                P(q), [f'From C to P: ({p[0] - c[0]}, {p[1] - c[1]}).', f'Multiply by {F(k)}: ({F(k * (p[0] - c[0]))}, {F(k * (p[1] - c[1]))}); add to C: P′{P(q)}.'])


@fam('congruence-similarity-skill-05')
def cgs5_area(r):
    a = r.choice([6, 8, 10, 12, 18, 20, 24]); k = r.choice([2, 3, Fr(1, 2), Fr(3, 2)]); need((a * k * k).denominator == 1)
    return item('s5_area_scale', f'A triangle has area {a} square units. It is dilated with scale factor {F(k)}. What is the area of the image?',
                f'{F(a * k * k)} square units', [f'Lengths are multiplied by {F(k)}, so areas are multiplied by ({F(k)})² = {F(k * k)}.', f'{a} × {F(k * k)} = {F(a * k * k)} square units.'],
                mc(f'{F(a * k * k)} square units', [f'{F(a * k)} square units', f'{F(a + k)} square units', f'{F(a * k * k * k)} square units', f'{F(a * k * 2 + 1)} square units']))


@fam('congruence-similarity-skill-06')
def cgs6_two_mirrors(r):
    a, b = sorted(r.sample(range(-4, 6), 2)); need(b - a >= 2)
    return item('s6_parallel_mirrors', f'A figure is reflected over the line x = {a} and then over the line x = {b}. The result is a single translation. How many units right does every point move?',
                str(2 * (b - a)), ['Two reflections over parallel lines make a translation of twice the distance between the lines.', f'2 × ({b} - {par(a)}) = {2 * (b - a)} units right.'])


@fam('congruence-similarity-skill-07')
def cgs7_ratio(r):
    a, b, c = sorted(r.sample(range(1, 9), 3)); s = a + b + c; need(180 % s == 0)
    u = 180 // s
    return item('s7_angle_ratio', f'The angles of a triangle are in the ratio {a} : {b} : {c}. What is the largest angle?',
                f'{c * u}°', [f'{a if a > 1 else ""}k + {b}k + {c}k = 180, so {s}k = 180 and k = {u}.', f'Largest angle: {c} × {u} = {c * u}°.'])


@fam('congruence-similarity-skill-07')
def cgs7_exterior_multiple(r):
    k = r.choice([2, 3, 4, 5, 8, 9, 11])
    i = Fr(180, k + 1); need(i.denominator == 1)
    return item('s7_exterior_multiple', f'An exterior angle of a triangle is {k} times the interior angle next to it. Find the exterior angle.',
                f'{F(k * i)}°', [f'The exterior and adjacent interior angles form a linear pair: x + {k}x = 180.', f'x = {F(i)}, so the exterior angle is {k} × {F(i)} = {F(k * i)}°.'])


@fam('congruence-similarity-skill-09')
def cgs9_same_side(r):
    x = r.randint(10, 30); a, c = r.choice([2, 3, 4]), r.choice([1, 2, 3]); b = r.randint(-10, 20)
    d = 180 - (a * x + b) - c * x; need(0 < a * x + b < 180 and 0 < c * x + d < 180 and d != 0)
    return item('s9_same_side_find', f'Lines m and n are parallel. Same-side interior angles measure ({lin(a, b)})° and ({lin(c, d)})°. Find the larger angle.',
                f'{max(a * x + b, c * x + d)}°', [f'Same-side interior angles are supplementary: {lin(a, b)} + {lin(c, d)} = 180.', f'{a + c}x {sgn(b + d)} = 180, so x = {x}.',
                                                   f'The angles are {a * x + b}° and {c * x + d}°.'])


@fam('congruence-similarity-skill-09')
def cgs9_alt_ext_then_pair(r):
    x = r.randint(15, 40); a, c = r.choice([2, 3]), r.choice([4, 5]); b = r.randint(0, 30); d = (a - c) * x + b
    ang = a * x + b; need(20 < ang < 160)
    return item('s9_alternate_exterior_pair', f'Lines m and n are parallel (angles numbered as usual: ∠1 to ∠4 at m, ∠5 to ∠8 at n, upper left, upper right, lower left, lower right). ∠1 = ({lin(a, b)})° and ∠8 = ({lin(c, d)})°. Find ∠2.',
                f'{180 - ang}°', [f'∠1 and ∠8 are alternate exterior angles, so they are equal: x = {x}.', f'∠1 = {ang}°, and ∠2 forms a linear pair with ∠1: 180 - {ang} = {180 - ang}°.'])


# ---------------------------------------------------------------- equations and expressions
@fam('equations-expressions-skill-01')
def eqx1_cube_root_eq(r):
    m = r.randint(2, 5); a = r.choice([2, 3]); b = r.randint(-5, 9); need((m ** 3 - b) % a == 0)
    x = (m ** 3 - b) // a
    return item('s1_cube_root_equation', f'If ∛({lin(a, b)}) = {m}, what is x?', f'x = {x}', [f'Cube both sides: {lin(a, b)} = {m ** 3}.', f'{a}x = {m ** 3 - b}, so x = {x}.'])


@fam('equations-expressions-skill-03')
def eqx3_consecutive_even(r):
    n = r.randint(3, 4); start = 2 * r.randint(5, 30); s = sum(start + 2 * i for i in range(n))
    return item('s3_consecutive_even', f'The sum of {n} consecutive even integers is {s}. Write an equation and find the largest integer.',
                str(start + 2 * (n - 1)), [f'Let the integers be ' + ', '.join(f'x + {2 * i}' if i else 'x' for i in range(n)) + f': {n}x + {n * (n - 1)} = {s}.', f'x = {start}, so the largest is {start + 2 * (n - 1)}.'])


@fam('equations-expressions-skill-03')
def eqx3_age(r):
    y = r.randint(8, 15); k = r.choice([2, 3]); t = r.randint(3, 10); m = k * (y + t) - t
    return item('s3_age_equation', f'Maya is {m} years old and her cousin is c years old. In {t} years Maya will be {k} times as old as her cousin. Write an equation and find c.',
                f'c = {y}', [f'{m} + {t} = {k}(c + {t}).', f'{m + t} = {k}c + {k * t}, so c = {y}.'])


@fam('equations-expressions-skill-04')
def eqx4_fractions(r):
    b, d = r.sample([2, 3, 4, 5, 6], 2); x = r.randint(-12, 20); a = r.randint(1, 9)
    num = Fr(x + a, b) * d; c = x - num; need(c.denominator == 1 and c != 0 and (x + a) % b == 0)
    c = int(c)
    return item('s4_cross_multiply', f'Solve: (x + {a})/{b} = (x {sgn(-c)})/{d}', f'x = {x}',
                [f'Cross-multiply: {d}(x + {a}) = {b}(x {sgn(-c)}).', f'{d}x + {d * a} = {b}x {sgn(-b * c)}.', f'{d - b}x = {-b * c - d * a}, so x = {x}.'])


@fam('equations-expressions-skill-04')
def eqx4_decimals(r):
    a, b = r.choice([(0.4, 0.1), (1.5, 0.5), (0.8, 0.3), (2.5, 1.5), (0.6, 0.2)]); x = r.choice([4, 6, 10, -10, 20, 8, -5]); c = r.randint(1, 9)
    A, B = Fr(str(a)), Fr(str(b)); d = A * (x + c) - B * x; need(d.denominator * 10 % 10 == 0 or True)
    ds = sgn(0)[:1] + ' ' + f'{float(d):g}' if d >= 0 else '- ' + f'{float(-d):g}'
    return item('s4_decimal_distribute', f'Solve: {a}(x + {c}) = {b}x {ds}', f'x = {x}',
                [f'Distribute: {a}x + {float(A * c):g} = {b}x {ds}.', f'{"x" if A - B == 1 else f"{float(A - B):g}x"} = {float(d - A * c):g}, so x = {x}.'])


@fam('equations-expressions-skill-06')
def eqx6_triangle(r):
    x = r.randint(4, 15); a, b = r.randint(1, 9), r.randint(1, 6)
    s = [x, 2 * x + a, 3 * x - b]; need(min(s) > 0 and sum(s) - max(s) > max(s))
    return item('s6_triangle_perimeter', f'A triangle has sides x, 2x + {a} and 3x - {b}. Its perimeter is {sum(s)}. How long is the longest side?',
                str(max(s)), [f'Combine like terms: 6x {sgn(a - b)} = {sum(s)}.', f'x = {x}; the sides are {s[0]}, {s[1]} and {s[2]}.', f'The longest side is {max(s)}.'])


@fam('equations-expressions-skill-06')
def eqx6_odd(r):
    n = 4; start = 2 * r.randint(3, 40) + 1; s = sum(start + 2 * i for i in range(n))
    return item('s6_consecutive_odd', f'The sum of four consecutive odd integers is {s}. What is the smallest of them?', str(start),
                [f'x + (x + 2) + (x + 4) + (x + 6) = {s}, so 4x + 12 = {s}.', f'4x = {s - 12}, so x = {start}.'])


@fam('equations-expressions-skill-07')
def eqx7_identity_param(r):
    a = r.randint(2, 9); c = r.randint(2, 8)
    return item('s7_infinitely_many_param', f'For what value of k does k(x + {c}) = {a}x + {a * c} have infinitely many solutions?', f'k = {a}',
                [f'Distribute: kx + {c}k = {a}x + {a * c}.', f'Matching x-terms needs k = {a}; then {c}k = {a * c} also matches, so every x works.'])


# ---------------------------------------------------------------- geometry applications
@fam('geometry-applications-skill-01')
def geo1_classify(r):
    a, b, c = sorted([r.randint(4, 20) for _ in range(3)]); need(a + b > c and a * a + b * b != c * c)
    kind = 'acute' if a * a + b * b > c * c else 'obtuse'
    return item('s1_acute_obtuse', f'A triangle has sides {a}, {b} and {c}. Compare {a}² + {b}² with {c}². Is the triangle acute, right or obtuse?',
                kind, [f'{a}² + {b}² = {a * a + b * b} and {c}² = {c * c}.', f'{a * a + b * b} {">" if kind == "acute" else "<"} {c * c}, so the triangle is {kind}.'])


@fam('geometry-applications-skill-01')
def geo1_isosceles_right(r):
    s = r.randint(2, 12)
    return item('s1_isosceles_right', f'An isosceles right triangle has legs of length {s}. Find the exact length of the hypotenuse.',
                f'{s}√2', [f'c² = {s}² + {s}² = {2 * s * s}.', f'c = √{2 * s * s} = {s}√2.'])


@fam('geometry-applications-skill-02')
def geo2_ladder_slide(r):
    L, a, b = r.choice([(25, 7, 24), (13, 5, 12), (10, 6, 8), (17, 8, 15), (26, 10, 24)])
    for d in range(1, b):
        t = b - d; base = math.isqrt(L * L - t * t)
        if base * base == L * L - t * t and base > a:
            break
    else:
        raise Skip()
    return item('s2_ladder_slides', f'A {L}-ft ladder leans against a wall with its base {a} ft from the wall. The top slides down {d} ft. How far does the base slide out?',
                f'{base - a} ft', [f'Height at first: √({L}² - {a}²) = {b} ft; after sliding: {b - d} ft.', f'New base distance: √({L}² - {b - d}²) = {base} ft.', f'The base moves {base} - {a} = {base - a} ft.'])


@fam('geometry-applications-skill-02')
def geo2_rect_perimeter(r):
    a, b, c = r.choice([(3, 4, 5), (6, 8, 10), (5, 12, 13), (8, 15, 17), (9, 12, 15), (12, 16, 20)])
    return item('s2_diagonal_from_perimeter', f'A rectangle has perimeter {2 * (a + b)} cm and one side of {a} cm. How long is its diagonal?',
                f'{c} cm', [f'The other side is ({2 * (a + b)} - 2 · {a}) ÷ 2 = {b} cm.', f'Diagonal: √({a}² + {b}²) = {c} cm.'])


@fam('geometry-applications-skill-03')
def geo3_cube(r):
    s = r.randint(2, 12)
    return item('s3_cube_diagonal', f'A cube has edges of length {s} cm. Find the exact length of a space diagonal (corner to opposite corner through the cube).',
                f'{s}√3 cm', [f'd² = {s}² + {s}² + {s}² = {3 * s * s}.', f'd = √{3 * s * s} = {s}√3 cm.'])


@fam('geometry-applications-skill-03')
def geo3_missing_height(r):
    l, w, h, d = r.choice([(2, 3, 6, 7), (1, 4, 8, 9), (2, 6, 9, 11), (4, 4, 7, 9), (6, 6, 7, 11), (3, 4, 12, 13)])
    return item('s3_box_missing_edge', f'A box is {l} m by {w} m, and its space diagonal is {d} m. How tall is the box?',
                f'{h} m', [f'd² = l² + w² + h²: {d * d} = {l * l} + {w * w} + h².', f'h² = {h * h}, so h = {h} m.'])


@fam('geometry-applications-skill-06')
def geo6_r_from_hr(r):
    rr = r.randint(2, 6); k = r.choice([2, 3])
    v = k * rr ** 3
    return item('s6_height_multiple', f'A cylinder\'s height is {k} times its radius, and its volume is {v}π cubic cm. Find its radius.',
                f'{rr} cm', [f'V = πr²({k}r) = {k}πr³.', f'{k}r³ = {v}, so r³ = {rr ** 3} and r = {rr} cm.'])


@fam('geometry-applications-skill-06')
def geo6_cone_equal(r):
    rr, h = r.randint(2, 8), r.randint(3, 12)
    return item('s6_equal_volume_cone', f'A cylinder has radius {rr} cm and height {h} cm. A cone with the same radius has the same volume. How tall is the cone?',
                f'{3 * h} cm', [f'Cylinder: π({rr}²)({h}) = {rr * rr * h}π.', f'Cone: (1/3)π({rr}²)H = {rr * rr * h}π gives H = 3 × {h} = {3 * h} cm.'])


# ---------------------------------------------------------------- linear and functional relationships
@fam('linear-functional-relationships-skill-02')
def lfr2_point_on(r):
    m, b = r.choice([2, 3, -2, -3, 4]), r.randint(-6, 6); k = r.randint(-5, 6); y = m * k + b; need(k != 0)
    return item('s2_missing_coordinate', f'The point (k, {y}) lies on the graph of y = {lin(m, b)}. Find k.', f'k = {k}', [f'Substitute: {y} = {m}k {sgn(b)}.', f'{m}k = {y - b}, so k = {k}.'])


@fam('linear-functional-relationships-skill-02')
def lfr2_equal_outputs(r):
    a, c = r.choice([2, 3, 4]), r.choice([-1, -2, 1]); x = r.randint(-4, 6); b = r.randint(-8, 8); d = a * x + b - c * x
    need(a != c)
    return item('s2_equal_outputs', f'For f(x) = {lin(a, b)} and g(x) = {lin(c, d)}, find the x-value where f(x) = g(x).', f'x = {x}',
                [f'{lin(a, b)} = {lin(c, d)}.', f'{lin(a - c, 0)} = {d - b}, so x = {x}. Both functions equal {a * x + b} there.'])


@fam('linear-functional-relationships-skill-09')
def lfr9_catch_up(r):
    s1, r1 = r.randint(20, 60), r.randint(5, 10); r2 = r1 + r.randint(2, 6); t = r.randint(3, 12); s2 = s1 + (r1 - r2) * t
    need(s2 >= 0)
    return item('s9_when_equal', f'Tank A holds {s1} L and gains {r1} L per minute. Tank B holds {s2} L and gains {r2} L per minute. After how many minutes do they hold the same amount?',
                f'{t} minutes', [f'{s1} + {r1}t = {s2} + {r2}t.', f'{s1 - s2} = {r2 - r1}t, so t = {t}.'])


@fam('linear-functional-relationships-skill-09')
def lfr9_rate_difference(r):
    a = r.randint(8, 20); b = a + r.randint(2, 8); t = r.randint(5, 12); x1, x2 = 2, 5
    return item('s9_rate_gap', f'Printer A prints y = {a}x pages in x minutes. Printer B printed {b * x1} pages after {x1} minutes and {b * x2} pages after {x2} minutes, at a constant rate. How many more pages does B print in {t} minutes?',
                f'{(b - a) * t} pages', [f'B\'s rate: ({b * x2} - {b * x1}) ÷ ({x2} - {x1}) = {b} pages per minute.', f'Difference: ({b} - {a}) × {t} = {(b - a) * t} pages.'])


@fam('linear-functional-relationships-skill-10')
def lfr10_when_zero(r):
    rate = r.choice([40, 50, 60, 75, 80]); t = r.choice([2, 3, 4, 5, 6]); s = rate * t
    return item('s10_time_to_zero', f'D(t) = {s} - {rate}t gives a driver\'s distance (miles) from home after t hours. After how many hours does the driver reach home?',
                f'{t} hours', [f'Home means D(t) = 0: {s} - {rate}t = 0.', f't = {s} ÷ {rate} = {t} hours.'])


@fam('linear-functional-relationships-skill-10')
def lfr10_input_for_value(r):
    s = r.choice([1200, 1500, 1800, 2400]); m = r.choice([75, 100, 125, 150]); t = r.randint(2, 8); v = s - m * t; need(v > 0)
    return item('s10_input_for_value', f'V(t) = {s} - {m}t gives a laptop\'s value (dollars) after t years. After how many years is the value ${v}?',
                f'{t} years', [f'{s} - {m}t = {v}.', f'{m}t = {s - v}, so t = {t}.'])


@fam('linear-functional-relationships-skill-11')
def lfr11_sum(r):
    k = r.randint(-1, 3); a, b = r.choice([1, 2, -1]), r.randint(-3, 4); c = r.choice([-2, -3, 2]); d = a * k + b - c * k
    x1, x2 = k - r.randint(1, 4), k + r.randint(1, 4)
    v = (a * x1 + b) + (c * x2 + d)
    return item('s11_sum_of_pieces', f'f(x) = {lin(a, b)} for x < {k}, and f(x) = {lin(c, d)} for x ≥ {k}. Find f({x1}) + f({x2}).',
                str(v), [f'{x1} < {k}: f({x1}) = {a * x1 + b}.', f'{x2} ≥ {k}: f({x2}) = {c * x2 + d}.', f'Sum: {v}.'])


@fam('linear-functional-relationships-skill-11')
def lfr11_solve(r):
    k = 1; a, b = 1, r.randint(1, 4); c = r.choice([-2, -3]); d = a * k + b - c * k
    y = r.randint(b - 3, b - 1)
    xs = []
    x_left = y - b
    if x_left < k:
        xs.append(x_left)
    x_right = Fr(y - d, c)
    if x_right >= k and x_right.denominator == 1:
        xs.append(int(x_right))
    need(len(xs) == 2)
    xs.sort()
    return item('s11_solve_piecewise', f'f(x) = {lin(a, b)} for x < {k}, and f(x) = {lin(c, d)} for x ≥ {k}. Find every x with f(x) = {y}.',
                f'x = {xs[0]} or x = {xs[1]}', [f'Left piece: {lin(a, b)} = {y} gives x = {x_left}, and {x_left} < {k}, so it counts.', f'Right piece: {lin(c, d)} = {y} gives x = {F(x_right)}, and {F(x_right)} ≥ {k}, so it counts.'])


@fam('linear-functional-relationships-skill-12')
def lfr12_reverse(r):
    k = r.choice([Fr(3, 2), Fr(5, 2), Fr(4, 3), Fr(7, 4), 3, 6]); x = r.choice([2, 4, 6, 8, 12]); y = k * x; need(y.denominator == 1 if isinstance(y, Fr) else True)
    c = k * r.choice([10, 14, 18, 20, 24]); need(Fr(c).denominator == 1)
    return item('s12_reverse_proportion', f'y is proportional to x, and y = {F(y)} when x = {x}. Find x when y = {F(c)}.', f'x = {F(Fr(c) / k)}',
                [f'k = {F(y)} ÷ {x} = {F(k)}, so y = {lin(k, 0)}.', f'{F(c)} = {lin(k, 0)}, so x = {F(Fr(c) / k)}.'])


@fam('linear-functional-relationships-skill-12')
def lfr12_gap(r):
    a, b = r.randint(3, 12), r.randint(3, 12); need(a != b); t = r.randint(4, 15); w = r.randint(2, 5)
    return item('s12_gap_over_time', f'Pump A fills {a * w} gallons in {w} minutes; pump B fills y = {b}x gallons in x minutes. Both rates are constant. After {t} minutes, how many more gallons has the faster pump filled?',
                f'{abs(a - b) * t} gallons', [f'Pump A: {a * w} ÷ {w} = {a} gallons per minute.', f'Difference: |{a} - {b}| × {t} = {abs(a - b) * t} gallons.'])


# ---------------------------------------------------------------- patterns and bivariate data
@fam('patterns-bivariate-data-skill-03')
def biv3_count_breaks(r):
    xs = sorted(r.sample(range(1, 13), 6)); ys = [10 + 3 * i + r.choice([-4, 0, 0, 2]) for i in range(6)]
    breaks = sum(1 for i in range(5) if ys[i + 1] < ys[i]); need(0 < breaks < 3)
    return item('s3_count_reversals', f'Data: x: {", ".join(map(str, xs))}; y: {", ".join(map(str, ys))}. The overall association is positive. Between how many pairs of neighboring points (in order of x) does y go down?',
                str(breaks), ['Compare each y with the next one, in order of x.', f'y goes down {breaks} time{"s" if breaks > 1 else ""}; the trend is still positive overall.'])


@fam('patterns-bivariate-data-skill-03')
def biv3_classify_data(r):
    kind = r.choice(['positive', 'negative'])
    xs = [1, 2, 3, 4, 5, 6, 7]
    m = r.randint(2, 4) * (1 if kind == 'positive' else -1)
    ys = [30 + m * x + r.choice([-1, 0, 1]) for x in xs]
    return item('s3_direction_from_data', f'Data: x: {", ".join(map(str, xs))}; y: {", ".join(map(str, ys))}. Is the association positive, negative or none?',
                kind, [f'From x = 1 to x = 7, y goes from {ys[0]} to {ys[-1]}.', f'y tends to {"increase" if kind == "positive" else "decrease"} as x increases, so the association is {kind}.'])


@fam('patterns-bivariate-data-skill-04')
def biv4_signed_error(r):
    m, b = r.randint(2, 9), r.randint(10, 60); x = r.randint(2, 12); e = r.choice([-6, -4, -3, 3, 5, 7]); y = m * x + b + e
    return item('s4_actual_minus_predicted', f'The line y = {m}x + {b} models a set of data. One student\'s data point is ({x}, {y}). Find actual minus predicted for this point.',
                str(e), [f'Predicted: {m}({x}) + {b} = {m * x + b}.', f'Actual minus predicted: {y} - {m * x + b} = {e}.'])


@fam('patterns-bivariate-data-skill-04')
def biv4_reverse(r):
    (x1, y1), m = (r.randint(0, 4), r.randint(20, 50)), r.choice([2, 3, 4, 5, Fr(5, 2)])
    b = y1 - m * x1; x = r.randint(8, 16); y = m * x + b; need(Fr(y).denominator == 1)
    return item('s4_reverse_prediction', f'A line of fit passes through ({x1}, {y1}) and ({x1 + 4}, {F(y1 + 4 * m)}). For what x does it predict y = {F(y)}?',
                f'x = {x}', [f'Slope: ({F(y1 + 4 * m)} - {y1}) ÷ 4 = {F(m)}; equation y = {lin(m, b)}.', f'{lin(m, b)} = {F(y)}, so x = {x}.'])


@fam('patterns-bivariate-data-skill-05')
def biv5_percent(r):
    n = r.choice([60, 80, 100, 120, 200]); p8 = r.choice([40, 45, 55, 60, 75]); g8 = n * p8 // 100
    s8 = r.randint(5, g8 - 5); tot = s8 + r.randint(5, n - g8 - 5)
    return item('s5_percent_cells', f'Of {n} students, {p8}% are in grade 8 and the rest are in grade 7. {s8} grade 8 students play a sport, and {tot} students play a sport in all. How many grade 7 students do not play a sport?',
                str(n - g8 - (tot - s8)), [f'Grade 8: {p8}% of {n} = {g8}; grade 7: {n - g8}.', f'Grade 7 students who play: {tot} - {s8} = {tot - s8}.', f'Grade 7 who do not: {n - g8} - {tot - s8} = {n - g8 - (tot - s8)}.'])


@fam('patterns-bivariate-data-skill-05')
def biv5_two_missing(r):
    a, b, c, d = [r.randint(6, 30) for _ in range(4)]
    return item('s5_two_unknown_cells', f'A two-way table: Grade 7 — {a} walk, x take the bus. Grade 8 — y walk, {d} take the bus. {a + c} students walk and {b + d} take the bus. Find x + y.',
                str(b + c), [f'Walk column: {a} + y = {a + c}, so y = {c}.', f'Bus column: x + {d} = {b + d}, so x = {b}.', f'x + y = {b + c}.'])


@fam('patterns-bivariate-data-skill-06')
def biv6_column_percent(r):
    a, b = r.randint(10, 30), r.randint(10, 30); tot = a + b; need(100 * b % tot == 0)
    return item('s6_column_relative', f'Of the students who play a sport, {a} are in grade 7 and {b} are in grade 8. What percent of the students who play a sport are in grade 8?',
                f'{100 * b // tot}%', [f'Column total: {a} + {b} = {tot}.', f'{b} ÷ {tot} = {F(Fr(b, tot))} = {100 * b // tot}%.'])


@fam('patterns-bivariate-data-skill-06')
def biv6_points_gap(r):
    n7, n8 = r.choice([20, 25, 40, 50]), r.choice([20, 25, 40, 50]); p7, p8 = r.choice([20, 40, 60, 80]), r.choice([30, 50, 70, 90])
    k7, k8 = n7 * p7 // 100, n8 * p8 // 100; need(n7 * p7 % 100 == 0 and n8 * p8 % 100 == 0 and p7 != p8)
    return item('s6_percentage_point_gap', f'Grade 7: {k7} of {n7} students bring lunch. Grade 8: {k8} of {n8} students bring lunch. How many percentage points apart are the two grades?',
                str(abs(p7 - p8)), [f'Grade 7: {k7} ÷ {n7} = {p7}%. Grade 8: {k8} ÷ {n8} = {p8}%.', f'|{p7} - {p8}| = {abs(p7 - p8)} percentage points.'])


# ---------------------------------------------------------------- real numbers and exponents
@fam('real-numbers-exponents-skill-01')
def rne1_third(r):
    a, b = Fr(r.randint(-9, 5), r.choice([2, 3, 4])), Fr(r.randint(1, 9), r.choice([3, 5, 6])); need(a < b)
    k = r.choice([Fr(1, 3), Fr(2, 3), Fr(1, 4), Fr(3, 4)])
    v = a + k * (b - a)
    return item('s1_part_of_way', f'What rational number is {F(k)} of the way from {F(a)} to {F(b)} on a number line?', F(v),
                [f'Distance: {F(b)} - {par(a)} = {F(b - a)}.', f'{F(a)} + {F(k)} × {F(b - a)} = {F(v)}.'])


@fam('real-numbers-exponents-skill-01')
def rne1_range(r):
    vals = [Fr(r.randint(-12, 12), r.choice([2, 3, 4, 5])) for _ in range(4)]; need(len(set(vals)) == 4)
    return item('s1_spread', f'Find the difference between the greatest and the least of {", ".join(F(v) for v in vals)}.', F(max(vals) - min(vals)),
                [f'Greatest: {F(max(vals))}; least: {F(min(vals))}.', f'{F(max(vals))} - {par(min(vals))} = {F(max(vals) - min(vals))}.'])


@fam('real-numbers-exponents-skill-02')
def rne2_complex(r):
    a, b, c = Fr(r.randint(-5, 5), r.choice([2, 3])), Fr(r.randint(1, 5), r.choice([4, 6])), Fr(r.randint(-7, -1), r.choice([3, 5]))
    need(a + b != 0)
    v = (a + b) / c
    return item('s2_grouped_quotient', f'Evaluate: ({F(a)} + {F(b)}) ÷ ({F(c)})', F(v), [f'Inside the parentheses: {F(a)} + {F(b)} = {F(a + b)}.', f'Divide: {F(a + b)} ÷ {par(c)} = {F(v)}.'])


@fam('real-numbers-exponents-skill-02')
def rne2_temperature(r):
    s = r.choice([-4.5, -2.5, 1.5, 3.5]); d = r.choice([1.25, 0.75, 1.5]); h = r.randint(3, 8); u = r.choice([2.5, 3, 4.5])
    v = Fr(str(s)) - Fr(str(d)) * h + Fr(str(u))
    return item('s2_temperature_change', f'At 6 p.m. the temperature was {s}°C. It dropped {d}°C each hour for {h} hours, then rose {u}°C. What was the final temperature?',
                f'{float(v):g}°C', [f'Drop: {d} × {h} = {float(Fr(str(d)) * h):g}°C.', f'{s} - {float(Fr(str(d)) * h):g} + {u} = {float(v):g}°C.'])


@fam('real-numbers-exponents-skill-04')
def rne4_count(r):
    n = r.randint(20, 120); sq = math.isqrt(n)
    return item('s4_count_irrational_roots', f'For how many whole numbers n from 1 to {n} is √n irrational?', str(n - sq),
                [f'√n is rational only when n is a perfect square: 1, 4, …, {sq * sq} ({sq} of them).', f'{n} - {sq} = {n - sq} irrational square roots.'])


@fam('real-numbers-exponents-skill-04')
def rne4_smallest_multiplier(r):
    k = r.choice([12, 18, 20, 27, 28, 45, 50, 75, 8, 24])
    n = next(n for n in range(1, 100) if math.isqrt(k * n) ** 2 == k * n)
    return item('s4_make_rational', f'What is the smallest whole number n for which √({k}n) is rational?', str(n),
                [f'{k}n must be a perfect square.', f'{k} × {n} = {k * n} = {math.isqrt(k * n)}², so n = {n}.'])


@fam('real-numbers-exponents-skill-05')
def rne5_product(r):
    a = r.choice([2, 3, 5, 6, 7]); m = r.choice([2, 3, 4, 5]); b = a * m * m
    return item('s5_rational_product', f'Evaluate √{a} · √{b}. Is the result rational?', f'{a * m}', [f'√{a} · √{b} = √{a * b}.', f'{a * b} = {a * m}², so the product is {a * m}, which is rational.'])


@fam('real-numbers-exponents-skill-05')
def rne5_conjugate(r):
    a, b = r.choice([2, 3, 5, 6, 7, 10]), r.randint(1, 4)
    return item('s5_conjugate_product', f'Evaluate (√{a} + {b})(√{a} - {b}).', str(a - b * b), [f'Multiply: (√{a})² - {b}².', f'{a} - {b * b} = {a - b * b}, a rational number even though both factors are irrational.'])


@fam('real-numbers-exponents-skill-06')
def rne6_count(r):
    a, b = r.randint(5, 60), r.randint(5, 80); need(math.isqrt(a) ** 2 != a and math.isqrt(b) ** 2 != b)
    lo, hi = -math.isqrt(a), math.isqrt(b)
    return item('s6_integers_between', f'How many integers are between -√{a} and √{b}?', str(hi - lo + 1),
                [f'-√{a} is between {-math.isqrt(a) - 1} and {-math.isqrt(a)}; √{b} is between {math.isqrt(b)} and {math.isqrt(b) + 1}.', f'The integers from {lo} to {hi}: {hi - lo + 1}.'])


@fam('real-numbers-exponents-skill-06')
def rne6_least_n(r):
    k = r.choice([5.5, 6.2, 7.1, 8.4, 9.3, 4.6]); n = math.floor(k * k) + 1
    return item('s6_least_n_root', f'What is the least whole number n with √n > {k}?', str(n), [f'√n > {k} means n > {k}² = {k * k:g}.', f'The least whole number greater than {k * k:g} is {n}.'])


@fam('real-numbers-exponents-skill-07')
def rne7_cube_between(r):
    n = r.randint(10, 990); c = round(n ** (1 / 3)); need(c ** 3 != n and (c - 1) ** 3 != n)
    lo = max(k for k in range(1, 11) if k ** 3 < n)
    return item('s7_cube_edge_between', f'A cube-shaped box has a volume of {n} cubic inches. Its edge length is between which two consecutive whole numbers of inches?', f'{lo} and {lo + 1}',
                [f'The edge is ∛{n}.', f'{lo}³ = {lo ** 3} and {lo + 1}³ = {(lo + 1) ** 3}; {lo ** 3} < {n} < {(lo + 1) ** 3}, so the edge is between {lo} and {lo + 1} inches.'])


@fam('real-numbers-exponents-skill-07')
def rne7_fraction_square(r):
    a, b = r.randint(1, 12), r.randint(2, 15); need(math.gcd(a, b) == 1 and a < b)
    return item('s7_fraction_root', f'A square has area {a * a}/{b * b} square meters. How long is each side?', f'{a}/{b} m', [f'Side = √({a * a}/{b * b}).', f'√{a * a} = {a} and √{b * b} = {b}, so the side is {a}/{b} m.'])


@fam('real-numbers-exponents-skill-10')
def rne10_normalize_negative(r):
    m = r.randint(11, 999); e = r.randint(-8, -3); digits = str(m)
    # write 0.00…m × 10^e  as a × 10^n
    lead = r.randint(1, 3); s = '0.' + '0' * lead + digits
    val = Fr(s) * Fr(10) ** e
    n = math.floor(math.log10(float(val)))
    a = val / Fr(10) ** n
    sup = str.maketrans('-0123456789', '⁻⁰¹²³⁴⁵⁶⁷⁸⁹')
    return item('s10_normalize_small', f'Write {s} × 10{str(e).translate(sup)} in scientific notation.', f'{float(a):g} × 10{str(n).translate(sup)}',
                [f'{s} = {float(a):g} × 10{str(-lead - 1).translate(sup)}.', f'Add the exponents: {-lead - 1} + ({e}) = {n}.'])


@fam('real-numbers-exponents-skill-10')
def rne10_how_many_times(r):
    a, b = r.randint(2, 9), r.randint(2, 9); m, n = r.randint(4, 12), r.randint(-6, 3); need(a % b == 0 and m > n)
    sup = str.maketrans('-0123456789', '⁻⁰¹²³⁴⁵⁶⁷⁸⁹')
    v = a // b * 10 ** (m - n)
    return item('s10_times_as_large', f'How many times as large is {a} × 10{str(m).translate(sup)} as {b} × 10{str(n).translate(sup)}? Write the answer in scientific notation.',
                f'{a // b} × 10{str(m - n).translate(sup)}', [f'Divide the first factors: {a} ÷ {b} = {a // b}.', f'Subtract the exponents: {m} - ({n}) = {m - n}, so the answer is {a // b} × 10{str(m - n).translate(sup)}.'])


@fam('real-numbers-exponents-skill-11')
def rne11_light(r):
    t = r.choice([2, 4, 5, 6, 8])
    return item('s11_light_distance', f'Light travels about 3 × 10⁵ km per second. About how far does it travel in {t} × 10² seconds? Write the answer in scientific notation.',
                f'{3 * t / 10:g} × 10⁸ km' if 3 * t >= 10 else f'{3 * t} × 10⁷ km', [f'(3 × 10⁵)({t} × 10²) = {3 * t} × 10⁷.', 'Normalize so the first factor is from 1 to 10.'])


# ---------------------------------------------------------------- systems of linear equations
@fam('systems-linear-equations-skill-01')
def sys1_parallel_value(r):
    a, b = r.choice([(2, -1), (4, -2), (3, -1), (6, -3), (1, 2), (2, 4)]); c = r.randint(-6, 6); y0 = r.randint(-5, 5); X = r.randint(2, 6)
    m = Fr(-a, b)
    return item('s1_parallel_then_value', f'A line passes through (0, {y0}) and is parallel to {eqtxt(a, b, c)}. Find y on the line when x = {X}.',
                F(m * X + y0), [f'Slope of {eqtxt(a, b, c)}: {F(m)}.', f'New line: y = {lin(m, y0)}; at x = {X}, y = {F(m * X + y0)}.'])


@fam('systems-linear-equations-skill-02')
def sys2_find_k(r):
    x0 = r.randint(-3, 4); m1, m2 = r.choice([1, 2, 3]), r.choice([-1, -2]); b2 = r.randint(-4, 6); y0 = m2 * x0 + b2; k = y0 - m1 * x0
    return item('s2_intersection_parameter', f'The lines y = {lin(m1, 0)} + k and y = {lin(m2, b2)} intersect at a point with x = {x0}. Find k.'.replace('y = x + k', 'y = x + k'),
                f'k = {k}', [f'At x = {x0} the second line gives y = {y0}.', f'{y0} = {m1}({x0}) + k, so k = {k}.'])


@fam('systems-linear-equations-skill-02')
def sys2_cost_equal(r):
    f1, r1 = r.randint(20, 60), r.randint(5, 12); r2 = r1 + r.randint(2, 6); t = r.randint(3, 10); f2 = f1 + (r1 - r2) * t; need(f2 >= 0)
    return item('s2_equal_total', f'Plan A: y = {r1}x + {f1}. Plan B: y = {r2}x + {f2}. The graphs cross where the plans cost the same. What is that cost?',
                f'${r1 * t + f1}', [f'{r1}x + {f1} = {r2}x + {f2} gives x = {t}.', f'Cost: {r1}({t}) + {f1} = ${r1 * t + f1}.'])


@fam('systems-linear-equations-skill-03')
def sys3_x_solved(r):
    x, y = r.randint(-6, 8), r.randint(-5, 6); a = r.choice([2, 3]); b = x - a * y; c, d = r.choice([(3, -4), (2, 5), (4, -3), (5, 2)]); e = c * x + d * y
    return item('s3_x_isolated', f'Solve by substitution: x = {lin(a, b, "y")} and {eqtxt(c, d, e)}', P((x, y)),
                [f'Substitute: {c}({lin(a, b, "y")}) {sgn(d)}y = {e}.', f'{c * a + d}y {sgn(c * b)} = {e}, so y = {y}.', f'x = {a}({y}) {sgn(b)} = {x}. Solution {P((x, y))}.'])


@fam('systems-linear-equations-skill-03')
def sys3_ages(r):
    c = r.randint(6, 15); k = r.choice([2, 3]); t = r.randint(2, 8); p = k * (c + t) - t
    return item('s3_ages_system', f'A parent is p years old and a child is c years old. p + c = {p + c}, and in {t} years the parent will be {k} times as old as the child. How old is the child now?',
                f'{c} years old', [f'p = {p + c} - c and p + {t} = {k}(c + {t}).', f'{p + c} - c + {t} = {k}c + {k * t}, so {k + 1}c = {p + c + t - k * t} and c = {c}.'])


@fam('systems-linear-equations-skill-05')
def sys5_param(r):
    m, b = r.choice([2, 3, 4]), r.randint(-5, 5); a = r.choice([2, 3])
    return item('s5_infinite_parameter', f'For what value of k does the system y = {lin(m, b)} and {a * m}x - {a}y = k have infinitely many solutions?', f'k = {-a * b}',
                [f'Multiply y = {lin(m, b)} by {a} and rearrange: {a * m}x - {a}y = {-a * b}.', f'The equations are the same line when k = {-a * b}.'])


def movable(bank, sk, lower):
    return [q for q in bank if q['skillId'] == sk and q['level'] == 'honors' and mask(q['prompt']) in lower and q['format'] in ('short-answer', 'multiple-choice')
            and not re.search(r'_(error|select|open)', family(q)) and not re.search(r'-h\d\d$', q['id'])]


def run():
    banks = load()
    added = moved = 0
    report = {}
    for sk, fams in FAM.items():
        unit = sk.rsplit('-skill-', 1)[0]
        bank = banks[unit]['questions']
        n = sk.rsplit('-skill-', 1)[1]
        lower = {mask(q['prompt']) for q in bank if q['skillId'] == sk and q['level'] in ('cp2', 'cp1') and not re.search(r'-h\d\d$', q['id'])}
        mine = [q for q in bank if q['skillId'] == sk and re.search(r'-honors-h\d\d$', q['id']) and 'batch D' in q.get('sourceNotes', '')]
        target = len(movable(bank, sk, lower)) + sum(1 for q in mine)
        if mine:   # already run: rebuild the same items
            target = len(mine)
        target = min(target, 12)
        if target == 0:
            continue
        r = random.Random('g8-batch-d|' + sk)
        out, seen, tries = [], {q['prompt'] for q in bank if 'batch D' not in q.get('sourceNotes', '') or 'batch D move' in q.get('sourceNotes', '')}, 0
        while len(out) < target and tries < 5000:
            tries += 1
            f = fams[tries % len(fams)]
            try:
                it = f(r)
            except (Skip, AssertionError, ZeroDivisionError, StopIteration, ValueError):
                continue
            if it[2] in seen or mask(it[2]) in lower:
                continue
            seen.add(it[2]); out.append(it)
        assert len(out) == target, (sk, len(out), target)
        start = max([int(re.search(r'-h(\d\d)$', q['id']).group(1)) for q in bank if q['skillId'] == sk and re.search(r'-honors-h\d\d$', q['id']) and 'batch D' not in q.get('sourceNotes', '')] or [0])
        std = next(q['standards'] for q in bank if q['skillId'] == sk)
        for i, (fm, fmt, prompt, ans, steps, opts) in enumerate(out):
            qid = f'pa8-{ABBR[unit]}-s{n}-honors-h{start + i + 1:02d}'
            q = {'id': qid, 'skillId': sk, 'level': 'honors', 'format': fmt, 'prompt': prompt, 'answer': ans}
            if opts:
                q['options'] = [{'text': t, 'correct': t == ans} for t in opts]
            q.update({'solutionSteps': steps, 'standards': std, 'sourceNotes': NOTE.format(fam=fm)})
            old = next((x for x in bank if x['id'] == qid), None)
            if old:
                old.clear(); old.update(q)
            else:
                idx = max(j for j, x in enumerate(bank) if x['skillId'] == sk and x['level'] == 'honors')
                bank.insert(idx + 1, q); added += 1
        need_ = target - sum(1 for q in bank if q['skillId'] == sk and 'batch D move' in q.get('sourceNotes', ''))
        cands = movable(bank, sk, lower)
        cands.sort(key=lambda q: (q['format'] != 'short-answer', q['id']))
        mcs = sum(1 for q in bank if q['skillId'] == sk and q['level'] == 'honors' and q['format'] == 'multiple-choice')
        for q in cands:
            if need_ <= 0:
                break
            if q['format'] == 'multiple-choice':
                if mcs <= 6:
                    continue
                mcs -= 1
            q['level'] = 'cp1'
            q['sourceNotes'] = q.get('sourceNotes', '') + MOVED + ' (batch D move)'
            need_ -= 1; moved += 1
        report[sk] = target
    save(banks)
    return added, moved, report


if __name__ == '__main__':
    a, m, rep = run()
    print('added', a, 'moved', m, 'skills', len(rep))
