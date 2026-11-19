"""8th Grade Math audit follow-up (2026-11-19), batch E: finish #14.

Standard short-answer and multiple-choice items that reuse a Support template are rewritten in place (IDs, skill, level
and format kept) as a Standard item of the same skill with one added step. Items with a diagram, plot items, items another
audit fix rewrote, and select-all / error-analysis / open-response items are left alone. The new prompt must not reuse a
Support or Advanced template. Deterministic (seeded by item ID) and idempotent. Run from the repository root, then run
batch_b_steps.py."""
import math, os, random, re, sys, zlib
from fractions import Fraction as Fr

sys.path.insert(0, os.path.dirname(__file__))
from lib import load, save, family
from batch_c import F, par, sgn, lin, eqtxt, mc, mask

NOTE = ('Original Claude-authored item (family: {fam}). Rewritten from a Support template (was {old}) as a Standard item with an '
        'added step: 8th Grade Math audit follow-up 2026-11-19 (Standard, batch E); answer recomputed by scripts/test-grade8-audit.cjs.')
SKIP_NOTES = re.compile(r'audit #(5|8|9|13|14|15|16|17)\b|batch D\)')
SUP = str.maketrans('-0123456789', '⁻⁰¹²³⁴⁵⁶⁷⁸⁹')


class Skip(Exception):
    pass


def need(c):
    if not c:
        raise Skip()


def P(x, y):
    return f'({F(x)}, {F(y)})'


def sci(m, e):
    return f'{m:g} × 10{str(e).translate(SUP)}'


def nwrong(v, *alts):
    return [F(a) if isinstance(a, (int, Fr)) else a for a in alts]


G = {}


def gen(skill):
    def deco(f):
        G.setdefault(skill, []).append(f)
        return f
    return deco


TRIPLES = [(3, 4, 5), (6, 8, 10), (5, 12, 13), (8, 15, 17), (9, 12, 15), (7, 24, 25), (12, 16, 20), (15, 20, 25), (20, 21, 29), (10, 24, 26)]

# ---------------------------------------------------------------- congruence and similarity
@gen('congruence-similarity-skill-01')
def cgs1_reflect_translate(r):
    a, b, h = r.randint(-7, 7), r.randint(-7, 7), r.randint(2, 6); need(a and b)
    ax = r.choice(['x', 'y'])
    p1 = (a, -b) if ax == 'x' else (-a, b)
    p2 = (p1[0] - h, p1[1])
    return ('s1_reflect_then_translate', f'Point A{P(a, b)} is reflected over the {ax}-axis and then translated {h} units left. What are the coordinates of the final image of A?',
            P(*p2), [f'Reflect over the {ax}-axis: {P(*p1)}.', f'Translate {h} units left (subtract {h} from x): {P(*p2)}.'],
            [P(p1[0] + h, p1[1]), P(a - h, b), P(-p2[0], p2[1])])


@gen('congruence-similarity-skill-01')
def cgs1_length_kept(r):
    a, b, c = r.randint(-6, 6), r.randint(-6, 6), r.randint(-6, 6); need(b != c and a)
    rot = r.choice(['90° clockwise', '180°', '90° counterclockwise'])
    L = abs(c - b)
    return ('s1_rigid_length', f'Segment AB has endpoints A{P(a, b)} and B{P(a, c)}. It is rotated {rot} about the origin. How long is A′B′?',
            str(L), [f'AB is vertical, so AB = |{c} - {par(b)}| = {L}.', f'A rotation is a rigid transformation, so it keeps lengths: A′B′ = {L}.'],
            [str(L * 2), str(abs(b + c)) if abs(b + c) != L else str(L + 1), str(abs(a) + L)])


@gen('congruence-similarity-skill-02')
def cgs2_rotate_translate(r):
    x, y, h = r.randint(-7, 7), r.randint(-7, 7), r.randint(2, 6); need(x and y and abs(x) != abs(y))
    q = (y, -x)
    f = (q[0] + h, q[1])
    return ('s2_rotate_then_translate', f'Point P{P(x, y)} is rotated 90° clockwise about the origin, then translated {h} units right. Where does P end up?',
            P(*f), [f'90° clockwise: (x, y) → (y, -x), so P′ = {P(*q)}.', f'Add {h} to x: {P(*f)}.'], [P(-y + h, x), P(q[0] - h, q[1]), P(y, -x)])


@gen('congruence-similarity-skill-03')
def cgs3_two_axes(r):
    x, y = r.randint(-8, 8), r.randint(-8, 8); need(x and y)
    first = r.choice(['x', 'y'])
    p1 = (x, -y) if first == 'x' else (-x, y)
    other = 'y' if first == 'x' else 'x'
    return ('s3_reflect_both_axes', f'Point P{P(x, y)} is reflected over the {first}-axis, and then the image is reflected over the {other}-axis. What are the final coordinates?',
            P(-x, -y), [f'Over the {first}-axis: {P(*p1)}.', f'Over the {other}-axis: {P(-x, -y)}.'], [P(*p1), P(y, x), P(x, y)])


@gen('congruence-similarity-skill-04')
def cgs4_two_translations(r):
    x, y = r.randint(-6, 6), r.randint(-6, 6); a, b, c, d = r.randint(2, 7), r.randint(2, 7), r.randint(1, 5), r.randint(1, 5)
    f = (x + a - c, y + b - d); need(a != c and b != d)
    return ('s4_two_translations', f'Point P{P(x, y)} is translated {a} units right and {b} units up, and then {c} units left and {d} units down. What are the final coordinates?',
            P(*f), [f'First translation: {P(x + a, y + b)}.', f'Second translation: {P(*f)}.'], [P(x + a, y + b), P(x - a + c, y - b + d), P(x + a + c, y + b + d)])


@gen('congruence-similarity-skill-05')
def cgs5_dilate_translate(r):
    x, y, k, h = r.randint(-5, 5), r.randint(-5, 5), r.choice([2, 3]), r.randint(1, 6); need(x and y)
    f = (k * x, k * y - h)
    return ('s5_dilate_then_translate', f'Point P{P(x, y)} is dilated with scale factor {k} centered at the origin, then translated {h} units down. Where does P end up?',
            P(*f), [f'Dilate: multiply both coordinates by {k}: {P(k * x, k * y)}.', f'Move {h} units down: {P(*f)}.'], [P(k * x, k * y), P(k * x - h, k * y), P(k * (y - h), k * x)] if k * (y - h) != f[0] else [P(k * x, k * y), P(k * x - h, k * y), P(x, y - h)])


@gen('congruence-similarity-skill-05')
def cgs5_rect_perimeter(r):
    l, w, k = r.randint(3, 12), r.randint(2, 9), r.choice([2, 3, Fr(1, 2), Fr(3, 2)]); need(l != w and (2 * (l + w) * k).denominator == 1)
    p = 2 * (l + w) * k
    return ('s5_image_perimeter', f'A rectangle is {l} cm long and {w} cm wide. It is dilated with scale factor {F(k)}. What is the perimeter of the image?',
            f'{F(p)} cm', [f'Image sides: {F(l * k)} cm and {F(w * k)} cm.', f'Perimeter: 2({F(l * k)} + {F(w * k)}) = {F(p)} cm.'],
            [f'{F(2 * (l + w))} cm', f'{F(p * k)} cm', f'{F(l * w * k)} cm'])


@gen('congruence-similarity-skill-08')
def cgs8_similar_side(r):
    a, b, c = r.choice(TRIPLES[:6]); k = r.choice([Fr(3, 2), 2, 3, Fr(5, 2)]); need((a * k).denominator == 1 and (c * k).denominator == 1)
    return ('s8_similar_two_sides', f'Triangle ABC has sides {a}, {b} and {c}. A similar triangle DEF has shortest side {F(a * k)}. How long is the longest side of triangle DEF?',
            F(c * k), [f'Scale factor: {F(a * k)} ÷ {a} = {F(k)}.', f'Longest side: {c} × {F(k)} = {F(c * k)}.'], [F(c + a * k - a), F(b * k), F(c * k + 1)])


@gen('congruence-similarity-skill-09')
def cgs9_alt_then_pair(r):
    a = r.choice([x for x in range(35, 150) if x != 90])
    return ('s9_alt_interior_pair', f'Lines m and n are parallel. ∠3 and ∠6 are alternate interior angles, and ∠6 and ∠5 form a linear pair. If ∠3 = {a}°, what is ∠5?',
            f'{180 - a}°', [f'Alternate interior angles are equal: ∠6 = {a}°.', f'A linear pair adds to 180°: ∠5 = 180 - {a} = {180 - a}°.'], [f'{a}°', f'{90 - a if a < 90 else a - 90}°', f'{360 - a}°'])


@gen('congruence-similarity-skill-09')
def cgs9_corresponding_x(r):
    x = r.randint(8, 40); a, c = r.choice([(2, 1), (3, 1), (3, 2), (4, 3), (5, 2)]); b = r.randint(0, 25); d = (a - c) * x + b
    need(10 < a * x + b < 170)
    return ('s9_corresponding_solve', f'Lines m and n are parallel. Two corresponding angles measure ({lin(a, b)})° and ({lin(c, d)})°. Find x and the angle measure.',
            f'x = {x}; {a * x + b}°', [f'Corresponding angles are equal: {lin(a, b)} = {lin(c, d)}.', f'{lin(a - c, 0)} = {d - b}, so x = {x}.', f'Angle: {a}({x}) {sgn(b)} = {a * x + b}°.'],
            [f'x = {x}; {180 - a * x - b}°', f'x = {x + 1}; {a * x + b}°', f'x = {d}; {a * x + b}°'])


# ---------------------------------------------------------------- equations and expressions
@gen('equations-expressions-skill-02')
def eqx2_power_product(r):
    a, m, n = r.choice([-2, 2, 3, -3]), r.choice([2, 3]), r.randint(1, 4)
    co = a ** m
    return ('s2_power_then_product', f'Simplify: ({a}x)^{m} · x^{n}'.replace('^2', '²').replace('^3', '³').replace('^1', '').replace('^4', '⁴'),
            f'{co}x{str(m + n).translate(SUP)}', [f'({a}x){str(m).translate(SUP)} = {co}x{str(m).translate(SUP)}.', f'Multiply by x{str(n).translate(SUP) if n > 1 else ""}: add exponents {m} + {n} = {m + n}.'],
            [f'{a * m}x{str(m + n).translate(SUP)}', f'{co}x{str(m * n).translate(SUP)}' if m * n != m + n else f'{co}x{str(m + n + 1).translate(SUP)}', f'{-co}x{str(m + n).translate(SUP)}'])


@gen('equations-expressions-skill-03')
def eqx3_sentence_solve(r):
    a, b, n = r.randint(2, 9), r.randint(2, 15), r.randint(3, 15)
    kind = r.choice(['less', 'more'])
    t = a * n - b if kind == 'less' else a * n + b
    eq = f'{a}n - {b} = {t}' if kind == 'less' else f'{a}n + {b} = {t}'
    return ('s3_sentence_then_solve', f'{b} {kind} than {a} times a number is {t}. Write an equation and find the number.',
            f'n = {n}', [f'Equation: {eq}.', f'{a}n = {a * n}, so n = {n}.'], [f'n = {n + 1}', f'n = {(t + b) // a if kind == "more" else max(1, (t - b) // a)}' if ((t + b) // a if kind == "more" else max(1, (t - b) // a)) != n else f'n = {n + 2}', f'n = {t - b}'])


@gen('equations-expressions-skill-03')
def eqx3_rental_hours(r):
    f, p, h = r.randint(10, 60), r.randint(5, 25), r.randint(2, 12)
    return ('s3_cost_then_solve', f'A kayak rental charges a ${f} fee plus ${p} per hour. A family paid ${f + p * h}. Write an equation and find the number of hours, h.',
            f'h = {h}', [f'{f} + {p}h = {f + p * h}.', f'{p}h = {p * h}, so h = {h}.'], [f'h = {h + 1}', f'h = {h - 1}', f'h = {(f + p * h) // p}' if (f + p * h) // p != h else f'h = {h + 2}'])


@gen('equations-expressions-skill-04')
def eqx4_distribute_both(r):
    a, b, c = r.choice([2, 3, 4, 5]), r.randint(1, 8), r.randint(1, 9); d = r.choice([x for x in range(-3, 7) if x not in (0, a)]); x = r.randint(-6, 9)
    e = a * (x - b) + c - d * x
    return ('s4_distribute_both_sides', f'Solve: {a}(x - {b}) {sgn(c)} = {lin(d, e)}', f'x = {x}',
            [f'Distribute: {a}x - {a * b} {sgn(c)} = {lin(d, e)}.', f'Collect x-terms: {lin(a - d, 0)} = {e + a * b - c}.', f'x = {x}.'],
            [f'x = {x + 1}', f'x = {-x}' if x else 'x = 1', f'x = {x - 2}'])


@gen('equations-expressions-skill-05')
def eqx5_two_step_paren(r):
    a, b, c, x = r.choice([2, 3, 4, 5, 6]), r.randint(1, 9), r.randint(1, 12), r.randint(-5, 10)
    t = a * (x + b) - c
    return ('s5_parentheses_two_step', f'Solve: {a}(x + {b}) - {c} = {t}', f'x = {x}',
            [f'Add {c}: {a}(x + {b}) = {t + c}.', f'Divide by {a}: x + {b} = {(t + c) // a}.', f'x = {x}.'], [f'x = {x + b}', f'x = {(t - c) // a - b}' if (t - c) // a - b != x else f'x = {x + 1}', f'x = {x - 1}'])


@gen('equations-expressions-skill-06')
def eqx6_distribute_combine(r):
    a, b, c, d = r.choice([2, 3, 4, -2]), r.randint(1, 9), r.choice([-5, -3, -1, 2, 4, 5]), r.randint(1, 9); need(a + c != 0)
    return ('s6_distribute_then_combine', f'Simplify: {a}(x {sgn(b)}) {sgn(c)}x - {d}'.replace(' + 1x', ' + x').replace(' - 1x', ' - x'),
            lin(a + c, a * b - d), [f'Distribute: {lin(a, a * b)} {sgn(c)}x - {d}.'.replace(' + 1x', ' + x').replace(' - 1x', ' - x'), f'Combine like terms: {lin(a + c, a * b - d)}.'],
            [lin(a + c, b - d), lin(a * c, a * b - d) if a * c != a + c else lin(a + c + 1, a * b - d), lin(a + c, a * b + d)])


@gen('equations-expressions-skill-08')
def eqx8_cube_two_step(r):
    x, c = r.randint(2, 6), r.randint(2, 30)
    return ('s8_cube_two_step', f'Solve: x³ - {c} = {x ** 3 - c}', f'x = {x}', [f'Add {c}: x³ = {x ** 3}.', f'Take the cube root: x = ∛{x ** 3} = {x}.'],
            [f'x = {x + 1}', f'x = {x ** 3}', f'x = {x - 1}'])


# ---------------------------------------------------------------- geometry applications
@gen('geometry-applications-skill-01')
def geo1_perimeter(r):
    a, b, c = r.choice(TRIPLES); k = r.choice(['m', 'cm', 'ft', 'in.'])
    return ('s1_legs_then_perimeter', f'A right triangle has legs {a} {k} and {b} {k}. Find the hypotenuse, then the perimeter of the triangle.',
            f'{a + b + c} {k}', [f'c = √({a}² + {b}²) = √{c * c} = {c} {k}.', f'Perimeter: {a} + {b} + {c} = {a + b + c} {k}.'], [f'{c} {k}', f'{a + b} {k}', f'{a * b // 2} {k}'])


@gen('geometry-applications-skill-01')
def geo1_leg_area(r):
    a, b, c = r.choice(TRIPLES)
    return ('s1_leg_then_area', f'A right triangle has a hypotenuse of {c} m and one leg of {a} m. Find the other leg, then the area of the triangle.',
            f'{a * b // 2 if a * b % 2 == 0 else F(Fr(a * b, 2))} square meters', [f'Other leg: √({c}² - {a}²) = {b} m.', f'Area: (1/2)({a})({b}) = {F(Fr(a * b, 2))} square meters.'],
            [f'{b} square meters', f'{a * b} square meters', f'{F(Fr(a * c, 2))} square meters'])


@gen('geometry-applications-skill-02')
def geo2_shortcut(r):
    a, b, c = r.choice(TRIPLES); k = r.choice([2, 4, 5, 10, 20])
    return ('s2_shortcut_saved', f'A rectangular park is {a * k} m by {b * k} m. Ana walks along two sides from one corner to the opposite corner; Ben walks straight across the diagonal. How many meters shorter is Ben\'s walk?',
            f'{(a + b - c) * k} m', [f'Ana: {a * k} + {b * k} = {(a + b) * k} m.', f'Ben: √({a * k}² + {b * k}²) = {c * k} m.', f'Difference: {(a + b - c) * k} m.'],
            [f'{c * k} m', f'{(a + b) * k} m', f'{(b - a) * k} m' if b != a else f'{k} m'])


@gen('geometry-applications-skill-03')
def geo3_cone_volume(r):
    rr, h, s = r.choice([(3, 4, 5), (5, 12, 13), (8, 15, 17), (12, 5, 13), (4, 3, 5), (15, 8, 17), (7, 24, 25), (24, 7, 25), (20, 21, 29), (21, 20, 29)]); k = r.choice([1, 2, 3]); rr, h, s = rr * k, h * k, s * k
    v = Fr(rr * rr * h, 3)
    return ('s3_slant_then_volume', f'A cone has radius {rr} cm and slant height {s} cm. Find its height, then its volume in terms of π.',
            f'{F(v)}π cubic centimeters', [f'Height: √({s}² - {rr}²) = {h} cm.', f'Volume: (1/3)π({rr}²)({h}) = {F(v)}π cubic centimeters.'],
            [f'{F(Fr(rr * rr * s, 3))}π cubic centimeters', f'{rr * rr * h}π cubic centimeters', f'{F(Fr(rr * h, 3))}π cubic centimeters'])


@gen('geometry-applications-skill-04')
def geo4_triangle_perimeter(r):
    a, b, c = r.choice(TRIPLES[:6]); x0, y0 = r.randint(-5, 3), r.randint(-5, 3)
    return ('s4_perimeter_on_grid', f'A triangle has vertices {P(x0, y0)}, {P(x0 + a, y0)} and {P(x0, y0 + b)}. What is its perimeter?',
            str(a + b + c), [f'The legs are {a} and {b} units long.', f'The third side is √({a}² + {b}²) = {c}.', f'Perimeter: {a} + {b} + {c} = {a + b + c}.'],
            [str(a + b), str(a + b + a + b), str(c)])


@gen('geometry-applications-skill-05')
def geo5_diameter_cylinder(r):
    d, h = 2 * r.randint(1, 8), r.randint(2, 15)
    return ('s5_cylinder_from_diameter', f'A cylinder has a diameter of {d} inches and a height of {h} inches. Find its volume in terms of π.',
            f'{(d // 2) ** 2 * h}π cubic inches', [f'Radius: {d} ÷ 2 = {d // 2} inches.', f'V = π({d // 2}²)({h}) = {(d // 2) ** 2 * h}π cubic inches.'],
            [f'{d * d * h}π cubic inches', f'{d * h}π cubic inches', f'{(d // 2) * h}π cubic inches'])


@gen('geometry-applications-skill-05')
def geo5_diameter_cone(r):
    d, h = 2 * r.randint(1, 8), 3 * r.randint(1, 6)
    v = Fr((d // 2) ** 2 * h, 3)
    return ('s5_cone_from_diameter', f'A cone has a diameter of {d} feet and a height of {h} feet. Find its volume in terms of π.',
            f'{F(v)}π cubic feet', [f'Radius: {d} ÷ 2 = {d // 2} feet.', f'V = (1/3)π({d // 2}²)({h}) = {F(v)}π cubic feet.'],
            [f'{(d // 2) ** 2 * h}π cubic feet', f'{F(Fr(d * d * h, 3))}π cubic feet', f'{F(Fr(d * h, 3))}π cubic feet'])


@gen('geometry-applications-skill-06')
def geo6_cyl_radius(r):
    rr, h = r.randint(2, 9), r.randint(2, 12)
    return ('s6_cylinder_radius', f'A cylinder has volume {rr * rr * h}π cubic cm and height {h} cm. What is its radius?',
            f'{rr} cm', [f'πr²({h}) = {rr * rr * h}π, so r² = {rr * rr}.', f'r = √{rr * rr} = {rr} cm.'], [f'{rr * rr} cm', f'{rr + 1} cm', f'{rr * h} cm'])


@gen('geometry-applications-skill-06')
def geo6_cone_radius(r):
    rr, h = r.randint(2, 9), 3 * r.randint(1, 5)
    v = rr * rr * h // 3
    return ('s6_cone_radius', f'A cone-shaped funnel holds {v}π cubic cm and is {h} cm tall. What is the radius of its opening?',
            f'{rr} cm', [f'(1/3)πr²({h}) = {v}π, so r² = {rr * rr}.', f'r = √{rr * rr} = {rr} cm.'], [f'{rr * rr} cm', f'{rr * 3} cm' if rr * 3 != rr else f'{rr + 2} cm', f'{rr + 1} cm'])


@gen('geometry-applications-skill-07')
def geo7_cone_hole(r):
    rr, h = r.randint(2, 6), 3 * r.randint(1, 5)
    v = 2 * rr * rr * h // 3
    return ('s7_cylinder_minus_cone', f'A cylinder has radius {rr} cm and height {h} cm. A cone with the same radius and height is cut out of it. What volume is left? Give your answer in terms of π.',
            f'{v}π cubic centimeters', [f'Cylinder: π({rr}²)({h}) = {rr * rr * h}π.', f'Cone: (1/3) of that = {rr * rr * h // 3}π.', f'Left: {rr * rr * h}π - {rr * rr * h // 3}π = {v}π cubic centimeters.'],
            [f'{rr * rr * h}π cubic centimeters', f'{rr * rr * h // 3}π cubic centimeters', f'{4 * rr * rr * h // 3}π cubic centimeters'])


@gen('geometry-applications-skill-07')
def geo7_cone_scoop(r):
    rr, h = 3 * r.randint(1, 3), r.randint(4, 12)
    cone, hemi = Fr(rr * rr * h, 3), Fr(2 * rr ** 3, 3)
    return ('s7_cone_with_scoop', f'An ice cream cone is a cone (radius {rr} cm, height {h} cm) filled level and topped with a hemisphere of ice cream with the same radius. Find the total volume in terms of π.',
            f'{F(cone + hemi)}π cubic centimeters', [f'Cone: (1/3)π({rr}²)({h}) = {F(cone)}π.', f'Hemisphere: (2/3)π({rr}³) = {F(hemi)}π.', f'Total: {F(cone + hemi)}π cubic centimeters.'],
            [f'{F(cone + 2 * hemi)}π cubic centimeters', f'{F(3 * cone + hemi)}π cubic centimeters', f'{F(cone)}π cubic centimeters'])


# ---------------------------------------------------------------- linear and functional relationships
@gen('linear-functional-relationships-skill-01')
def lfr1_table_then_value(r):
    m, b, X = r.choice([2, 3, -2, -3, 4, 5]), r.randint(-6, 8), r.randint(6, 12)
    ys = [m * x + b for x in range(4)]
    return ('s1_rule_then_evaluate', f'The table shows a function. x: 0, 1, 2, 3; y: {", ".join(map(str, ys))}. Write a rule, then find y when x = {X}.',
            str(m * X + b), [f'y starts at {b} and changes by {m} each time x goes up 1: y = {lin(m, b)}.', f'y = {m}({X}) {sgn(b)} = {m * X + b}.'],
            [str(m * X), str(ys[-1] + m), str(m * X - b) if b else str(m * X + 1)])


@gen('linear-functional-relationships-skill-02')
def lfr2_difference(r):
    m, b, a, c = r.choice([2, 3, -2, 4, -3, 5]), r.randint(-9, 9), r.randint(-4, 6), r.randint(-4, 6); need(a != c)
    return ('s2_difference_of_values', f'For f(x) = {lin(m, b)}, find f({a}) - f({c}).', str(m * (a - c)),
            [f'f({a}) = {m * a + b} and f({c}) = {m * c + b}.', f'{m * a + b} - {par(m * c + b)} = {m * (a - c)}.'], [str(m * (a + c)), str(m * (a - c) + b), str(m * (c - a))])


@gen('linear-functional-relationships-skill-03')
def lfr3_missing_value(r):
    a, m = r.randint(-10, 10), r.choice([2, 3, 4, -2, -3, -5, 6])
    k = r.randint(1, 3)
    ys = [str(a + m * i) for i in range(5)]; miss = ys[k]; ys[k] = '?'
    return ('s3_complete_linear_table', f'The table shows a linear function. x: 0, 1, 2, 3, 4; y: {", ".join(ys)}. What value replaces the ?',
            miss, [f'The y-values change by {m} each time x goes up 1.', f'Missing value: {a} {sgn(m * k)} = {miss}.'], [str(int(miss) + m), str(int(miss) - 1), str(a + m * (k + 1) * 2)])


@gen('linear-functional-relationships-skill-04')
def lfr4_slope_two_points(r):
    x1, y1 = r.randint(-6, 6), r.randint(-6, 6); dx, m = r.choice([1, 2, 3, 4]), r.choice([Fr(1, 2), 2, -3, Fr(-2, 3), 3, -1, Fr(3, 4)])
    dx = dx * Fr(m).denominator; x2, y2 = x1 + dx, y1 + m * dx
    return ('s4_slope_from_points', f'A line passes through {P(x1, y1)} and {P(x2, y2)}. What is its slope?', F(m),
            [f'Rise: {F(y2)} - {par(y1)} = {F(y2 - y1)}. Run: {x2} - {par(x1)} = {dx}.', f'Slope = {F(y2 - y1)} ÷ {dx} = {F(m)}.'], [F(1 / Fr(m)), F(-m), F(Fr(y2 + y1, dx)) if Fr(y2 + y1, dx) != m else F(m + 1)])


@gen('linear-functional-relationships-skill-05')
def lfr5_two_points_equation(r):
    m, b = r.choice([2, 3, -2, -1, 4, Fr(1, 2)]), r.randint(-6, 6); x1 = r.choice([1, 2, -2, 4]); x2 = x1 + 2 * r.randint(1, 3)
    return ('s5_equation_two_points', f'Write the equation in slope-intercept form of the line through {P(x1, m * x1 + b)} and {P(x2, m * x2 + b)}.',
            f'y = {lin(m, b)}', [f'Slope: ({F(m * x2 + b)} - {par(m * x1 + b)}) ÷ ({x2} - {par(x1)}) = {F(m)}.', f'b = {F(m * x1 + b)} - {par(m)}({x1}) = {b}.', f'y = {lin(m, b)}.'],
            [f'y = {lin(m, -b)}' if b else f'y = {lin(m, 1)}', f'y = {lin(-m, b)}', f'y = {lin(m, m * x1 + b)}' if m * x1 else f'y = {lin(m, b + 1)}'])


@gen('linear-functional-relationships-skill-06')
def lfr6_x_intercept(r):
    m, x0 = r.choice([2, 3, -2, -4, 5]), r.randint(-6, 6); b = -m * x0; need(b != 0)
    return ('s6_x_intercept_of_line', f'Find the x-intercept of the graph of y = {lin(m, b)}.', f'({x0}, 0)',
            [f'At the x-intercept, y = 0: 0 = {lin(m, b)}.', f'{lin(m, 0)} = {-b}, so x = {x0}. The x-intercept is ({x0}, 0).'], [f'(0, {b})', f'({-x0}, 0)', f'({b}, 0)'])


@gen('linear-functional-relationships-skill-07')
def lfr7_two_values(r):
    m, b = r.choice([2, 3, -2, 4, -3, 5, 6]), r.randint(-10, 15); a = r.randint(1, 4); c = a + r.randint(2, 5)
    return ('s7_rule_from_two_values', f'A linear function has f({a}) = {m * a + b} and f({c}) = {m * c + b}. Write its equation.', f'y = {lin(m, b)}',
            [f'Slope: ({m * c + b} - {par(m * a + b)}) ÷ ({c} - {a}) = {m}.', f'b = {m * a + b} - {par(m)}({a}) = {b}.', f'y = {lin(m, b)}.'],
            [f'y = {lin(m, m * a + b)}', f'y = {lin(-m, b)}', f'y = {lin(m, b + m)}'])


@gen('linear-functional-relationships-skill-08')
def lfr8_max_on_interval(r):
    m, b = r.choice([2, -2, 3, -3, Fr(1, 2), -1]), r.randint(-6, 6); a = r.randint(-6, -1); c = r.randint(1, 6)
    if Fr(m).denominator == 2:
        a, c = 2 * (a // 2), 2 * (c // 2 + 1)
    top = max(m * a + b, m * c + b)
    return ('s8_max_on_interval', f'f(x) = {lin(m, b)} on the interval from x = {a} to x = {c}. What is the maximum value of f?', F(top),
            [f'The slope is {F(m)}, so f is {"increasing" if m > 0 else "decreasing"}; the maximum is at x = {c if m > 0 else a}.', f'f({c if m > 0 else a}) = {F(top)}.'],
            [F(min(m * a + b, m * c + b)), F(b), F(top + 1)])


@gen('linear-functional-relationships-skill-09')
def lfr9_start_amount(r):
    rate, s = r.randint(3, 25), r.randint(10, 120); h1 = r.randint(1, 3); h2 = h1 + r.randint(2, 5)
    return ('s9_initial_from_two', f'A pool had {s + rate * h1} gallons after {h1} hours and {s + rate * h2} gallons after {h2} hours, filling at a constant rate. How many gallons were in it at the start?',
            f'{s} gallons', [f'Rate: ({s + rate * h2} - {s + rate * h1}) ÷ ({h2} - {h1}) = {rate} gallons per hour.', f'Start: {s + rate * h1} - {rate}({h1}) = {s} gallons.'],
            [f'{s + rate * h1} gallons', f'{rate} gallons', f'{s - rate} gallons' if s > rate else f'{s + rate} gallons'])


@gen('linear-functional-relationships-skill-10')
def lfr10_solve_for_input(r):
    p, f, n = r.randint(12, 40), r.randint(50, 200), r.randint(5, 30)
    return ('s10_input_from_total', f'C(n) = {p}n + {f} gives the cost, in dollars, of a trip for n students. For how many students is the cost ${p * n + f}?',
            f'{n} students', [f'{p}n + {f} = {p * n + f}.', f'{p}n = {p * n}, so n = {n}.'], [f'{n + 1} students', f'{(p * n + f) // p} students' if (p * n + f) // p != n else f'{n + 2} students', f'{n - 1} students'])


@gen('linear-functional-relationships-skill-11')
def lfr11_boundary(r):
    k = r.randint(-2, 3); a, b = r.choice([1, 2, -1, 3]), r.randint(-4, 5); c, d = r.choice([-2, -3, 2, 4]), r.randint(-4, 6); need(a * k + b != c * k + d)
    return ('s11_value_at_boundary', f'f(x) = {lin(a, b)} for x < {k}, and f(x) = {lin(c, d)} for x ≥ {k}. Find f({k}).', str(c * k + d),
            [f'x = {k} is not less than {k}, so it belongs to the piece for x ≥ {k}.', f'f({k}) = {c}({k}) {sgn(d)} = {c * k + d}.'], [str(a * k + b), str(c * k - d) if d else str(c * k + 1), str(c + d)])


@gen('linear-functional-relationships-skill-12')
def lfr12_unit_rate_predict(r):
    u, t, t2 = r.randint(30, 70), r.randint(2, 5), r.randint(6, 11)
    return ('s12_rate_then_predict', f'A car travels {u * t} miles in {t} hours at a constant speed. At this rate, how far does it travel in {t2} hours?',
            f'{u * t2} miles', [f'Unit rate: {u * t} ÷ {t} = {u} miles per hour.', f'{u} × {t2} = {u * t2} miles.'], [f'{u * t + t2} miles', f'{u * t * t2} miles', f'{u * (t2 - t)} miles'])


# ---------------------------------------------------------------- patterns and bivariate data
@gen('patterns-bivariate-data-skill-02')
def biv2_two_conditions(r):
    xs = [r.randint(0, 10) for _ in range(8)]; ys = [r.randint(50, 100) for _ in range(8)]; H, S = r.choice([4, 5, 6]), r.choice([70, 75, 80])
    n = sum(1 for x, y in zip(xs, ys) if x > H and y > S); need(n > 0)
    return ('s2_count_two_conditions', f'Data: hours studied: {", ".join(map(str, xs))}; test score: {", ".join(map(str, ys))}. How many students studied more than {H} hours and scored above {S}?',
            str(n), [f'Students who studied more than {H} hours: {", ".join(f"({x}, {y})" for x, y in zip(xs, ys) if x > H) or "none"}.', f'Of those, {n} scored above {S}.'],
            [str(sum(1 for x in xs if x > H)), str(sum(1 for y in ys if y > S)), str(n + 1)])


@gen('patterns-bivariate-data-skill-03')
def biv3_total_change(r):
    xs = sorted(r.sample(range(1, 15), 6)); m = r.choice([2, 3, -2, -3]); ys = [40 + m * x + r.choice([-2, 0, 1]) for x in xs]
    word = 'positive' if ys[-1] > ys[0] else 'negative'
    return ('s3_change_and_direction', f'Data: x: {", ".join(map(str, xs))}; y: {", ".join(map(str, ys))}. By how much does y change from the point with the least x to the point with the greatest x, and is the association positive or negative?',
            f'{ys[-1] - ys[0]}, {word}', [f'y goes from {ys[0]} to {ys[-1]}: a change of {ys[-1] - ys[0]}.', f'y tends to {"increase" if word == "positive" else "decrease"} as x increases, so the association is {word}.'],
            [f'{ys[0] - ys[-1]}, {word}', f'{ys[-1] - ys[0]}, {"negative" if word == "positive" else "positive"}', f'{xs[-1] - xs[0]}, {word}'])


@gen('patterns-bivariate-data-skill-04')
def biv4_prediction_gap(r):
    m, b, a = r.randint(2, 12), r.randint(10, 60), r.randint(1, 5); c = a + r.randint(2, 6)
    return ('s4_two_predictions', f'A line of best fit is y = {m}x + {b}. How much greater is the prediction for x = {c} than the prediction for x = {a}?',
            str(m * (c - a)), [f'Predictions: {m}({a}) + {b} = {m * a + b} and {m}({c}) + {b} = {m * c + b}.', f'{m * c + b} - {m * a + b} = {m * (c - a)}. (It is the slope times {c - a}.)'],
            [str(m * c + b), str(m), str(m * (c - a) + b)])


@gen('patterns-bivariate-data-skill-04')
def biv4_line_from_points(r):
    b, m, a = r.randint(5, 40), r.choice([2, 3, 4, 5, Fr(1, 2)]), r.choice([2, 4, 6, 8])
    return ('s4_fit_line_equation', f'A line of fit passes through (0, {b}) and ({a}, {F(b + m * a)}). Write its equation.', f'y = {lin(m, b)}',
            [f'Slope: ({F(b + m * a)} - {b}) ÷ {a} = {F(m)}.', f'The y-intercept is {b}: y = {lin(m, b)}.'], [f'y = {lin(1 / Fr(m), b)}', f'y = {lin(m, F(b + m * a))}', f'y = {lin(-m, b)}'])


@gen('patterns-bivariate-data-skill-05')
def biv5_total_no(r):
    a, b, c, t = r.randint(5, 30), r.randint(5, 30), r.randint(5, 30), r.randint(5, 30)
    return ('s5_column_total_from_rows', f'Grade 7: {a} students play a sport and {b} do not. Grade 8 has {c + t} students, and {c} of them play a sport. How many students in all do not play a sport?',
            str(b + t), [f'Grade 8 students who do not play: {c + t} - {c} = {t}.', f'Total who do not play: {b} + {t} = {b + t}.'], [str(t), str(a + c), str(b + c + t)])


@gen('patterns-bivariate-data-skill-06')
def biv6_row_percent(r):
    n = r.choice([20, 25, 40, 50]); p = r.choice([20, 40, 60, 80, 30, 70]); k = n * p // 100; need(n * p % 100 == 0)
    o = r.randint(10, 40)
    return ('s6_row_percent', f'Two-way table — boys: {k} have a pet, {n - k} have no pet. girls: {o} have a pet, {r.randint(10, 40)} have no pet. What percent of the boys have a pet?',
            f'{p}%', [f'Boys in all: {k} + {n - k} = {n}.', f'{k} ÷ {n} = {F(Fr(k, n))} = {p}%.'], [f'{100 - p}%', f'{round(100 * k / (k + o))}%' if round(100 * k / (k + o)) != p else f'{p + 5}%', f'{k}%' if k != p else f'{p + 10}%'])


# ---------------------------------------------------------------- real numbers and exponents
@gen('real-numbers-exponents-skill-01')
def rne1_count_between(r):
    a, b = Fr(-r.randint(5, 40), r.choice([3, 4, 6, 7])), Fr(r.randint(5, 40), r.choice([3, 5, 8, 9])); need(a.denominator > 1 and b.denominator > 1)
    lo, hi = math.ceil(a), math.floor(b)
    return ('s1_integers_between_fractions', f'How many integers are between {F(a)} and {F(b)} on a number line?', str(hi - lo + 1),
            [f'{F(a)} is between {lo - 1} and {lo}; {F(b)} is between {hi} and {hi + 1}.', f'The integers from {lo} to {hi}: {hi - lo + 1}.'], [str(hi - lo), str(hi - lo + 2), str(hi + lo)])


@gen('real-numbers-exponents-skill-02')
def rne2_two_operations(r):
    a, b, c = Fr(r.randint(-9, 9), r.choice([2, 3, 4])), Fr(r.randint(1, 7), r.choice([2, 3, 5])), Fr(r.randint(-6, -1), r.choice([3, 4, 7])); need(a != 0)
    v = a + b * c
    return ('s2_order_of_operations', f'Evaluate: {F(a)} + {F(b)} × ({F(c)})', F(v), [f'Multiply first: {F(b)} × ({F(c)}) = {F(b * c)}.', f'Add: {F(a)} + {par(b * c)} = {F(v)}.'],
            [F((a + b) * c), F(a - b * c), F(v + 1)])


@gen('real-numbers-exponents-skill-03')
def rne3_fraction_plus_decimal(r):
    a, b = r.choice([(1, 8), (3, 8), (5, 8), (1, 4), (3, 4), (2, 5), (3, 5), (7, 20), (9, 16)]); d = r.choice([1.25, 1.45, 1.6, 1.2, 2.35, 2.05, 3.5])
    v = Fr(a, b) + Fr(str(d))
    return ('s3_convert_then_add', f'Write {a}/{b} as a decimal, then add {d}. Give the answer as a decimal.', f'{float(v):g}',
            [f'{a}/{b} = {a / b:g}.', f'{a / b:g} + {d} = {float(v):g}.'], [f'{float(Fr(a + 0, b) * 10 + Fr(str(d))):g}' if False else f'{float(v) + 0.1:g}', f'{a / b:g}', f'{float(Fr(str(d)) - Fr(a, b)):g}' if Fr(str(d)) != Fr(a, b) * 2 else f'{float(v) - 0.1:g}'])


@gen('real-numbers-exponents-skill-04')
def rne4_count_irrational(r):
    pool = [('√4', 0), ('√8', 1), ('0.25', 0), ('π', 1), ('√(9/16)', 0), ('√50', 1), ('-√81', 0), ('2.7̄', 0), ('√2 + 1', 1), ('√36', 0), ('√12', 1), ('3/7', 0), ('√0.49', 0), ('√20', 1)]
    pick = r.sample(pool, 5); n = sum(i for _, i in pick); need(0 < n < 5)
    return ('s4_count_irrational_list', f'How many of these numbers are irrational: {", ".join(p for p, _ in pick)}?', str(n),
            [f'Irrational: {", ".join(p for p, i in pick if i)}.', f'The others are perfect-square roots, fractions or terminating/repeating decimals. Count: {n}.'], [str(n - 1) if n > 1 else '0', str(n + 1), str(5 - n) if 5 - n != n else '5'])


@gen('real-numbers-exponents-skill-05')
def rne5_product_plus(r):
    a, m, c = r.choice([2, 3, 5, 6, 7]), r.choice([2, 3, 4]), r.randint(-9, 9); need(c)
    v = a * m + c
    return ('s5_simplify_then_add', f'Simplify: √{a} · √{a * m * m} {sgn(c)}', str(v), [f'√{a} · √{a * m * m} = √{a * a * m * m} = {a * m}.', f'{a * m} {sgn(c)} = {v}.'],
            [f'{a * m}√{a} {sgn(c)}' if False else str(a * m * m + c), str(a * m), str(v + a)])


@gen('real-numbers-exponents-skill-07')
def rne7_area_perimeter(r):
    s = r.randint(4, 30)
    return ('s7_area_to_perimeter', f'A square garden has an area of {s * s} square meters. What is its perimeter?', f'{4 * s} meters',
            [f'Side: √{s * s} = {s} meters.', f'Perimeter: 4 × {s} = {4 * s} meters.'], [f'{s} meters', f'{2 * s} meters', f'{s * s // 4} meters' if s * s // 4 != 4 * s else f'{4 * s + 4} meters'])


@gen('real-numbers-exponents-skill-08')
def rne8_negative_zero(r):
    a, b, e = r.choice([2, 3, 4, 5]), r.choice([6, 7, 9, 10]), r.choice([2, 3]); need(a ** e <= 125)
    v = Fr(1, a ** e) + 1
    return ('s8_negative_plus_zero', f'Evaluate: {a}{str(-e).translate(SUP)} + {b}⁰', F(v), [f'{a}{str(-e).translate(SUP)} = 1/{a ** e} and {b}⁰ = 1.', f'1/{a ** e} + 1 = {F(v)}.'],
            [F(Fr(1, a ** e) + b), F(Fr(1, a ** e)), F(1 - Fr(a ** e))])


@gen('real-numbers-exponents-skill-10')
def rne10_normalize_big(r):
    m = Fr(r.randint(101, 989), 10); e = r.randint(2, 8)
    a = m / 10
    return ('s10_normalize_large', f'Write {float(m):g} × 10{str(e).translate(SUP)} in scientific notation.', sci(float(a), e + 1),
            [f'{float(m):g} = {float(a):g} × 10¹.', f'Add the exponents: 1 + {e} = {e + 1}.'], [sci(float(a), e - 1), sci(float(m), e), sci(float(a), e)])


@gen('real-numbers-exponents-skill-11')
def rne11_share(r):
    a, b, m, n = r.choice([6, 8, 9, 4]), r.choice([2, 3, 4]), r.randint(6, 9), r.randint(2, 4); need(a % b == 0)
    q = a // b
    return ('s11_divide_context', f'A city budget of {a} × 10{str(m).translate(SUP)} dollars is shared equally by {b} × 10{str(n).translate(SUP)} households. How many dollars is that per household? Use scientific notation.',
            sci(q, m - n) + ' dollars', [f'Divide the first factors: {a} ÷ {b} = {q}.', f'Subtract the exponents: {m} - {n} = {m - n}.'],
            [sci(q, m + n) + ' dollars', sci(a * b if a * b < 10 else a * b / 10, m - n if a * b < 10 else m - n + 1) + ' dollars', sci(q, m - n - 1) + ' dollars'])


# ---------------------------------------------------------------- systems of linear equations
@gen('systems-linear-equations-skill-01')
def sys1_intercept_standard(r):
    a, b = r.choice([(2, 1), (3, 1), (4, 2), (2, 4), (6, 3), (1, 2), (5, 5), (3, 3)]); k = r.randint(-5, 5); need(k)
    c = b * k
    return ('s1_y_intercept_standard_form', f'What is the y-intercept of the graph of {eqtxt(a, b, c)}?', f'(0, {k})',
            [f'At the y-intercept, x = 0: {b if b != 1 else ""}y = {c}.', f'y = {k}, so the y-intercept is (0, {k}).'], [f'(0, {c})' if c != k else f'(0, {-k})', f'({F(Fr(c, a))}, 0)', f'(0, {F(Fr(c, a))})' if Fr(c, a) != k else f'(0, {k + 1})'])


@gen('systems-linear-equations-skill-02')
def sys2_intersection(r):
    x, y = r.randint(-4, 5), r.randint(-6, 6); m1, m2 = r.sample([1, 2, 3, -1, -2, -3], 2)
    return ('s2_intersection_point', f'Without graphing, find the point where the graphs of y = {lin(m1, y - m1 * x)} and y = {lin(m2, y - m2 * x)} intersect.', P(x, y),
            [f'{lin(m1, y - m1 * x)} = {lin(m2, y - m2 * x)}, so {lin(m1 - m2, 0)} = {(y - m2 * x) - (y - m1 * x)} and x = {x}.', f'y = {m1}({x}) {sgn(y - m1 * x)} = {y}. The point is {P(x, y)}.'],
            [P(y, x), P(x, y + 1), P(-x, y) if x else P(1, y)])


@gen('systems-linear-equations-skill-03')
def sys3_isolate_first(r):
    x, y = r.randint(-5, 6), r.randint(-5, 6); a = r.choice([2, 3, -2, 4]); c = a * x + y; b, d = r.choice([(1, 2), (3, -2), (2, 3), (1, -3), (5, 2)]); e = b * x + d * y
    need(b + d * (-a) != 0)
    return ('s3_isolate_then_substitute', f'Solve by substitution: {eqtxt(a, 1, c)} and {eqtxt(b, d, e)}', P(x, y),
            [f'Solve the first equation for y: y = {lin(-a, c)}.', f'Substitute: {lin(b, 0)} {"+" if d > 0 else "-"} {abs(d) if abs(d) != 1 else ""}({lin(-a, c)}) = {e}, so x = {x}.', f'y = {-a}({x}) {sgn(c)} = {y}. Solution {P(x, y)}.'],
            [P(y, x) if x != y else P(x + 1, y), P(x, -y) if y else P(x, 1), P(-x, y) if x else P(2, y)])


@gen('systems-linear-equations-skill-04')
def sys4_add_to_eliminate(r):
    x, y = r.randint(-5, 6), r.randint(-5, 6); a, b, d = r.choice([1, 2, 3]), r.choice([2, 3, 4, 5]), r.choice([1, 2, 3, -1]); need(a + d != 0)
    c, e = a * x + b * y, d * x - b * y
    return ('s4_add_to_eliminate', f'Solve by elimination: {eqtxt(a, b, c)} and {eqtxt(d, -b, e)}', P(x, y),
            [f'Add the equations: the y-terms cancel, so {lin(a + d, 0)} = {c + e} and x = {x}.', f'Substitute: {a}({x}) + {b}y = {c}, so y = {y}. Solution {P(x, y)}.'],
            [P(y, x) if x != y else P(x + 1, y), P(x, -y) if y else P(x, 1), P(-x, y) if x else P(2, y)])


@gen('systems-linear-equations-skill-05')
def sys5_multiple_check(r):
    a, b, c = r.choice([1, 2, 3]), r.choice([1, 2, -1, 3]), r.randint(1, 9); k = r.choice([2, 3, -2]); same = r.random() < 0.5
    d = k * c if same else k * c + r.choice([1, 2, -3])
    ans = 'infinitely many solutions' if same else 'no solution'
    return ('s5_multiply_and_compare', f'How many solutions does the system {eqtxt(a, b, c)} and {eqtxt(k * a, k * b, d)} have?', ans,
            [f'Multiply the first equation by {k}: {eqtxt(k * a, k * b, k * c)}.', f'The left sides match; the right sides are {k * c} and {d}, so {"the equations are the same line" if same else "the lines are parallel"}: {ans}.'],
            ['one solution', 'no solution' if same else 'infinitely many solutions', 'two solutions'])


@gen('systems-linear-equations-skill-06')
def sys6_revenue_gap(r):
    a, c = r.choice([(6, 4), (8, 5), (10, 6), (12, 7), (9, 5)]); A, C = r.randint(10, 60), r.randint(10, 60); need(a * A > c * C)
    return ('s6_tickets_then_compare', f'A play sold {A + C} tickets for ${a * A + c * C}. Adult tickets cost ${a} and child tickets cost ${c}. How much more money came from adult tickets than from child tickets?',
            f'${a * A - c * C}', [f'a + c = {A + C} and {a}a + {c}c = {a * A + c * C} give a = {A} adult and c = {C} child tickets.', f'Adult: ${a * A}; child: ${c * C}; difference: ${a * A - c * C}.'],
            [f'${a * A}', f'${abs(A - C)}', f'${a * A - c * C + 10}'])


def targets(bank, cp2, hon):
    out = []
    for q in bank:
        if q['level'] != 'cp1' or q['format'] not in ('short-answer', 'multiple-choice') or 'diagram' in q or re.search(r'-p\d{3}$|-tarsia-', q['id']):
            continue
        notes = q.get('sourceNotes', '')
        if '(Standard, batch E)' in notes:
            out.append(q); continue
        if SKIP_NOTES.search(notes) or re.search(r'_(error|select|open)', family(q)) or q['skillId'] not in G:
            continue
        if (q['skillId'], mask(q['prompt'])) in cp2:
            out.append(q)
    return out


def run():
    banks = load()
    n = 0
    for unit, d in banks.items():
        bank = d['questions']
        cp2 = {(q['skillId'], mask(q['prompt'])) for q in bank if q['level'] == 'cp2'}
        hon = {(q['skillId'], mask(q['prompt'])) for q in bank if q['level'] == 'honors'}
        tg = targets(bank, cp2, hon)
        ids = {q['id'] for q in tg}
        seen = {q['prompt'] for q in bank if q['id'] not in ids}
        for q in tg:
            gens = G[q['skillId']]
            r = random.Random('g8-batch-e|' + q['id'])
            f = gens[zlib.crc32(q['id'].encode()) % len(gens)]
            old = re.search(r'\(was (\w+)\)', q['sourceNotes']).group(1) if '(Standard, batch E)' in q['sourceNotes'] else (family(q) or 'unnamed')
            for _ in range(3000):
                try:
                    fm, prompt, ans, steps, wrong = f(r)
                    opts = mc(ans, wrong) if q['format'] == 'multiple-choice' else None
                except (Skip, AssertionError, ZeroDivisionError):
                    continue
                key = (q['skillId'], mask(prompt))
                if prompt in seen or key in cp2 or key in hon:
                    continue
                break
            else:
                raise SystemExit('no item for ' + q['id'])
            seen.add(prompt)
            q['prompt'], q['answer'], q['solutionSteps'] = prompt, ans, steps
            if opts:
                q['options'] = [{'text': t, 'correct': t == ans} for t in opts]
            else:
                q.pop('options', None)
            q['sourceNotes'] = NOTE.format(fam=fm, old=old)
            q['prompt'] = re.sub(r'\b1 (hour|minute|week|day|year|second|month)s\b', r'1 \1', q['prompt'])
            q['solutionSteps'] = [re.sub(r'\b1 (hour|minute|week|day|year|second|month)s\b', r'1 \1', x) for x in q['solutionSteps']]
            n += 1
    save(banks)
    return n


if __name__ == '__main__':
    print('rewritten', run())
