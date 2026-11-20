"""Question families for the 3rd Grade Math audit (2026-11-19).

S[skill](r) -> a Standard item: the skill's Support task with one added step (#7).
A[skill](r) -> an Advanced item: two steps, work backward or compare (#1, #19).
Each returns (family, prompt, answer, steps, wrong_answers). Numbers stay inside Grade 3 limits: add and subtract
within 1,000, multiply and divide within 100 (divisors 2 to 10), one-digit numbers times multiples of 10, denominators
2, 3, 4, 6 and 8, elapsed time in minutes within one afternoon, liquid volume in liters and mass in grams or
kilograms without conversions. Every answer is computed here and recomputed independently by
scripts/test-grade3-audit.cjs."""
import math
from fractions import Fraction as Fr

NAMES = ['Ava', 'Ben', 'Cora', 'Dev', 'Eli', 'Gabi', 'Hugo', 'Isla', 'Jada', 'Kai', 'Lena', 'Max', 'Nia', 'Omar', 'Pia', 'Raj', 'Sam', 'Tess', 'Uma', 'Zoe']
DNAME = {2: 'halves', 3: 'thirds', 4: 'fourths', 6: 'sixths', 8: 'eighths'}
UNIT1 = {2: 'half', 3: 'third', 4: 'fourth', 6: 'sixth', 8: 'eighth'}
SINGULAR = {'liters': 'liter', 'grams': 'gram', 'kilograms': 'kilogram', 'minutes': 'minute', 'feet': 'foot', 'inches': 'inch', 'meters': 'meter',
            'centimeters': 'centimeter', 'units': 'unit', 'square units': 'square unit', 'square feet': 'square foot', 'square meters': 'square meter',
            'square centimeters': 'square centimeter', 'square inches': 'square inch', 'bags': 'bag', 'boxes': 'box', 'rows': 'row', 'pages': 'page',
            'stickers': 'sticker', 'cookies': 'cookie', 'apples': 'apple', 'cards': 'card', 'seeds': 'seed', 'books': 'book', 'beads': 'bead',
            'pencils': 'pencil', 'markers': 'marker', 'tables': 'table', 'teams': 'team', 'trays': 'tray', 'muffins': 'muffin', 'tiles': 'tile',
            'buckets': 'bucket', 'bottles': 'bottle', 'crates': 'crate', 'players': 'player', 'laps': 'lap', 'miles': 'mile', 'cups': 'cup', 'jugs': 'jug',
            'symbols': 'symbol', 'votes': 'vote', 'students': 'student', 'chairs': 'chair', 'shelves': 'shelf', 'plants': 'plant', 'eggs': 'egg',
            'cartons': 'carton', 'packs': 'pack', 'tickets': 'ticket', 'points': 'point', 'balloons': 'balloon', 'sides': 'side', 'pieces': 'piece'}


def qty(x, unit):
    return f'{x} {SINGULAR.get(unit, unit) if str(x) == "1" else unit}'


def n(x):
    return f'{x:,}'


def fr(a, b):
    return f'{a}/{b}'


def rnd(x, u):
    return int(math.floor(x / u + 0.5)) * u


def tm(m):
    """minutes after midnight -> h:mm on a 12-hour clock"""
    h = (m // 60 - 1) % 12 + 1
    return f'{h}:{m % 60:02d}'


class Skip(Exception):
    pass


def need(c):
    if not c:
        raise Skip()


S, A = {}, {}


def std(skill):
    def d(f):
        S.setdefault(skill, []).append(f); return f
    return d


def adv(skill):
    def d(f):
        A.setdefault(skill, []).append(f); return f
    return d


MM, DV, PF, UP, AS, UF, EC, TM, GD, AR, PS = ('multiplication-meaning', 'division-meaning', 'properties-fact-strategies', 'patterns-unknowns-two-step',
                                              'addition-subtraction-1000', 'understanding-fractions', 'equivalent-comparing-fractions', 'time-volume-mass',
                                              'graphs-measurement-data', 'area', 'perimeter-shapes')


def sk(u, i):
    return f'{u}-skill-{i:02d}'


GROUPS = [('bags', 'apples'), ('boxes', 'crayons'), ('plates', 'cookies'), ('vases', 'flowers'), ('packs', 'cards'), ('trays', 'muffins'), ('jars', 'marbles'), ('shelves', 'books')]

# =============================================================== multiplication meaning


@std(sk(MM, 1))
def mm1_s(r):
    g, k = r.randint(3, 9), r.randint(2, 9); c, t = r.choice(GROUPS); x = r.randint(2, 9)
    return ('mm1_groups_plus_more', f'There are {g} {c} with {k} {t} in each. {r.choice(NAMES)} adds {x} more {t}. How many {t} are there now?',
            qty(g * k + x, t), [f'{g} groups of {k}: {g} × {k} = {g * k}.', f'{g * k} + {x} = {g * k + x} {t}.'],
            [qty(g * k, t), qty(g + k + x, t), qty(g * (k + x), t)])


@adv(sk(MM, 1))
def mm1_a(r):
    g1, g2, k = r.randint(2, 6), r.randint(2, 6), r.randint(3, 9); need(g1 != g2); c, t = r.choice(GROUPS)
    return ('mm1_two_sets_of_groups', f'{r.choice(NAMES)} has {g1} {c} of {k} {t}. {r.choice(NAMES)} has {g2} {c} of {k} {t}. How many {t} do they have in all?',
            qty((g1 + g2) * k, t), [f'{g1} × {k} = {g1 * k} and {g2} × {k} = {g2 * k}.', f'{g1 * k} + {g2 * k} = {(g1 + g2) * k}, the same as ({g1} + {g2}) × {k}.'],
            [qty(g1 * k, t), qty(g1 + g2 + k, t), qty(abs(g1 - g2) * k, t)])


@std(sk(MM, 2))
def mm2_s(r):
    rows, cols, add = r.randint(3, 8), r.randint(3, 9), r.randint(1, 3)
    return ('mm2_array_add_rows', f'An array has {rows} rows of {cols} tiles. {add} more {"row" if add == 1 else "rows"} of {cols} {"is" if add == 1 else "are"} added. How many tiles are in the array now?',
            qty((rows + add) * cols, 'tiles'), [f'There are {rows} + {add} = {rows + add} rows.', f'{rows + add} × {cols} = {(rows + add) * cols} tiles.'],
            [qty(rows * cols, 'tiles'), qty(rows * cols + add, 'tiles'), qty((rows + add) * (cols + add), 'tiles')])


@adv(sk(MM, 2))
def mm2_a(r):
    rows, cols = r.randint(3, 9), r.randint(3, 9); hid = r.randint(1, rows - 1)
    return ('mm2_array_hidden_rows', f'An array has {cols} chairs in each row and {rows * cols} chairs in all. A curtain hides {hid} of the rows. How many chairs can you see?',
            qty((rows - hid) * cols, 'chairs'), [f'Rows in all: {rows * cols} ÷ {cols} = {rows}.', f'Rows you can see: {rows} − {hid} = {rows - hid}; {rows - hid} × {cols} = {(rows - hid) * cols} chairs.'],
            [qty(rows * cols - hid, 'chairs'), qty(hid * cols, 'chairs'), qty(rows - hid, 'chairs')])


@std(sk(MM, 3))
def mm3_s(r):
    f = r.choice([2, 5, 10]); a, b = r.randint(2, 9), r.randint(2, 9)
    return ('mm3_two_products_sum', f'Find {a} × {f} and {b} × {f}. What is the sum of the two products?',
            n(a * f + b * f), [f'{a} × {f} = {a * f} and {b} × {f} = {b * f}.', f'{a * f} + {b * f} = {a * f + b * f}.'],
            [n(a * f), n((a + b) + f), n(a * b * f)])


@adv(sk(MM, 3))
def mm3_a(r):
    k5, k10 = r.randint(2, 9), r.randint(2, 9)
    return ('mm3_coins_total', f'{r.choice(NAMES)} has {k10} dimes and {k5} nickels. A dime is 10 cents and a nickel is 5 cents. How many cents is that in all?',
            f'{k10 * 10 + k5 * 5} cents', [f'Dimes: {k10} × 10 = {k10 * 10} cents. Nickels: {k5} × 5 = {k5 * 5} cents.', f'{k10 * 10} + {k5 * 5} = {k10 * 10 + k5 * 5} cents.'],
            [f'{(k10 + k5) * 10} cents', f'{(k10 + k5) * 5} cents', f'{k10 + k5} cents'])


@adv(sk(MM, 4))
def mm4_a(r):
    k, p, g = r.randint(3, 9), r.randint(2, 9), r.randint(2, 5)
    return ('mm4_more_than_twice', f'A jug holds {k} liters. A tank holds as much as {p} jugs. A pool holds as much as {g} tanks. How many liters does the pool hold?',
            qty(k * p * g, 'liters'), [f'Tank: {p} × {k} = {p * k} liters.', f'Pool: {g} × {p * k} = {k * p * g} liters.'],
            [qty(k * p, 'liters'), qty(k + p + g, 'liters'), qty(k * p + g, 'liters')])

# =============================================================== division meaning


@std(sk(DV, 1))
def dv1_s(r):
    k, e = r.randint(2, 9), r.randint(2, 9); x = r.randint(1, 3); t = r.choice(['stickers', 'grapes', 'cards', 'beads'])
    tot = k * e
    return ('dv1_share_then_get_more', f'{k} friends share {tot} {t} equally. Then each friend gets {x} more. How many {t} does each friend have now?',
            qty(e + x, t), [f'{tot} ÷ {k} = {e} each.', f'{e} + {x} = {e + x} {t}.'], [qty(e, t), qty(tot + x, t), qty(e * x, t)])


@adv(sk(DV, 1))
def dv1_a(r):
    k1, k2 = r.choice([(2, 4), (3, 6), (2, 6), (4, 8), (2, 8), (3, 9), (5, 10), (2, 10)]); e2 = r.randint(2, 9); tot = k2 * e2
    need(tot % k1 == 0 and tot <= 100)
    return ('dv1_share_two_ways', f'{tot} crackers are shared equally among {k1} friends. The same number of crackers is shared equally among {k2} friends. How many more crackers does each friend get when there are {k1} friends?',
            qty(tot // k1 - tot // k2, 'crackers'), [f'{tot} ÷ {k1} = {tot // k1} and {tot} ÷ {k2} = {tot // k2}.', f'{tot // k1} − {tot // k2} = {tot // k1 - tot // k2}.'],
            [qty(tot // k1, 'crackers'), qty(k2 - k1, 'crackers'), qty(tot // k2, 'crackers')])


@std(sk(DV, 2))
def dv2_s(r):
    s, g = r.randint(2, 9), r.randint(2, 9); left = r.randint(1, g - 1) if g > 1 else 1
    return ('dv2_group_then_left', f'{s * g} chairs are set up in rows of {s}. Then {left} of the {"row is" if left == 1 else "rows are"} taken away. How many rows are left?',
            qty(g - left, 'rows'), [f'{s * g} ÷ {s} = {g} rows.', f'{g} − {left} = {g - left} rows.'], [qty(g, 'rows'), qty(s * g - left, 'rows'), qty(left, 'rows')])


@adv(sk(DV, 2))
def dv2_a(r):
    a, b = r.randint(2, 5), r.randint(6, 10); m = a * b * r.randint(1, 2); need(m <= 100 and m % a == 0 and m % b == 0)
    return ('dv2_two_bag_sizes', f'{r.choice(NAMES)} has {m} beads. Strings of {a} beads or strings of {b} beads can be made. How many more strings can be made with {a} beads on each string?',
            qty(m // a - m // b, 'strings'), [f'{m} ÷ {a} = {m // a} strings; {m} ÷ {b} = {m // b} strings.', f'{m // a} − {m // b} = {m // a - m // b}.'],
            [qty(m // a, 'strings'), qty(b - a, 'strings'), qty(m // b, 'strings')])


@std(sk(DV, 3))
def dv3_s(r):
    a, b = r.randint(2, 10), r.randint(2, 10); x = r.randint(2, 9)
    return ('dv3_unknown_then_add', f'Think {a} × ___ = {a * b} to find {a * b} ÷ {a}. Then add {x}. What number do you get?',
            n(b + x), [f'{a} × {b} = {a * b}, so {a * b} ÷ {a} = {b}.', f'{b} + {x} = {b + x}.'], [n(b), n(a * b + x), n(a + x)])


@adv(sk(DV, 3))
def dv3_a(r):
    a, b, c = r.randint(2, 9), r.randint(2, 9), r.randint(2, 9); need(a * b <= 100 and b * c <= 100)
    return ('dv3_chain_unknowns', f'{a} × □ = {a * b} and □ × △ = {b * c}. What number is △?',
            n(c), [f'{a * b} ÷ {a} = {b}, so □ = {b}.', f'{b} × △ = {b * c}, so △ = {b * c} ÷ {b} = {c}.'], [n(b), n(b * c - b), n(a * c)])


@std(sk(DV, 4))
def dv4_s(r):
    k, e = r.randint(2, 9), r.randint(2, 9); x = r.randint(2, 9); t = r.choice(['seeds', 'plants', 'tiles'])
    return ('dv4_rows_then_more', f'{r.choice(NAMES)} plants {k * e} {t} in {k} equal rows. Then {x} more {t} are added to one row. How many {t} are in that row now?',
            qty(e + x, t), [f'{k * e} ÷ {k} = {e} in each row.', f'{e} + {x} = {e + x}.'], [qty(e, t), qty(k * e + x, t), qty(k + x, t)])


@adv(sk(DV, 4))
def dv4_a(r):
    have, gave, k = r.randint(30, 80), r.randint(2, 20), r.randint(3, 9); rest = have - gave; need(rest % k == 0 and rest > 0)
    return ('dv4_take_away_then_share', f'{r.choice(NAMES)} had {have} stickers and gave away {gave}. The rest were shared equally into {k} albums. How many stickers are in each album?',
            qty(rest // k, 'stickers'), [f'{have} − {gave} = {rest} stickers left.', f'{rest} ÷ {k} = {rest // k} in each album.'],
            [qty(have // k if have % k == 0 else rest // k + 1, 'stickers'), qty(rest, 'stickers'), qty(rest // k + 1, 'stickers')])

# =============================================================== properties and fact strategies


@std(sk(PF, 1))
def pf1_s(r):
    a, b = r.randint(3, 9), r.randint(3, 9); need(a != b)
    return ('pf1_turn_around_then_double', f'{r.choice(NAMES)} knows {a} × {b} = {a * b}. What is {b} × {a}? Then what is double that product?',
            n(2 * a * b), [f'Turn-around fact: {b} × {a} = {a * b}.', f'Double {a * b} is {2 * a * b}.'], [n(a * b), n(a * b + 2), n(2 * (a + b))])


@adv(sk(PF, 1))
def pf1_a(r):
    a, b, c = r.randint(2, 9), r.randint(2, 9), r.randint(2, 9); need(a != b and a * b + c * b <= 100)
    return ('pf1_commute_and_add', f'Find {b} × {a} + {c} × {b}. (Hint: {b} × {a} = {a} × {b}.)',
            n(a * b + c * b), [f'{b} × {a} = {a * b} and {c} × {b} = {c * b}.', f'{a * b} + {c * b} = {a * b + c * b}.'], [n(a * b), n(b * (a + c) + b), n(a + b + c)])


@std(sk(PF, 2))
def pf2_s(r):
    a, b, c = r.choice([2, 5]), r.randint(2, 9), r.randint(2, 9); other = 5 if a == 2 else 2
    return ('pf2_group_to_ten', f'Find {a} × {b} × {other}. Hint: multiply {a} × {other} first. Then add {c}.',
            n(a * b * other + c), [f'{a} × {other} = 10, and 10 × {b} = {10 * b}.', f'{10 * b} + {c} = {10 * b + c}.'], [n(10 * b), n(a + b + other + c), n(a * b + other + c)])


@adv(sk(PF, 2))
def pf2_a(r):
    a, b, c = r.randint(2, 5), r.randint(2, 5), r.randint(2, 5); need(a * b * c <= 100)
    return ('pf2_three_factor_story', f'There are {a} shelves. Each shelf has {b} boxes. Each box has {c} toy cars. How many toy cars are there?',
            qty(a * b * c, 'toy cars'), [f'{a} × {b} = {a * b} boxes.', f'{a * b} × {c} = {a * b * c} toy cars.'], [qty(a * b, 'toy cars'), qty(a + b + c, 'toy cars'), qty(a * b + c, 'toy cars')])


@std(sk(PF, 3))
def pf3_s(r):
    a, b = r.randint(6, 9), r.randint(6, 9); s1 = 5; s2 = b - 5
    return ('pf3_break_apart_five', f'Find {a} × {b} by breaking {b} into 5 + {s2}. What is {a} × {s2}, and what is {a} × {b}?',
            f'{a * s2}; {a * b}', [f'{a} × 5 = {a * 5} and {a} × {s2} = {a * s2}.', f'{a * 5} + {a * s2} = {a * b}.'], [f'{a * s2}; {a * 5 + s2}', f'{a * 5}; {a * b}', f'{a + s2}; {a * b + 5}'])


@adv(sk(PF, 3))
def pf3_a(r):
    a, b = r.randint(6, 9), r.randint(6, 9); s = r.randint(2, b - 2)
    return ('pf3_two_part_area', f'A garden bed is {a} feet by {b} feet. It is split into {"an" if a == 8 else "a"} {a} by {s} part and {"an" if a == 8 else "a"} {a} by {b - s} part. What is the area of the larger part?',
            qty(a * max(s, b - s), 'square feet'), [f'{a} × {s} = {a * s} and {a} × {b - s} = {a * (b - s)}.', f'The larger part is {a * max(s, b - s)} square feet.'],
            [qty(a * min(s, b - s), 'square feet'), qty(a * b, 'square feet'), qty(a + max(s, b - s), 'square feet')])


@std(sk(PF, 4))
def pf4_s(r):
    a, b = r.randint(2, 99), r.randint(2, 9)
    return ('pf4_one_and_zero_sum', f'Find {a} × 1 + {b} × 0.', n(a), [f'{a} × 1 = {a}. Any number times 1 is that number.', f'{b} × 0 = 0, so the total is {a} + 0 = {a}.'],
            [n(a + b), '0', n(a + 1)])


@adv(sk(PF, 4))
def pf4_a(r):
    a, b, c = r.randint(2, 9), r.randint(2, 9), r.randint(2, 9)
    return ('pf4_zero_and_one_chain', f'Find (({a} × {b}) × 0) + ({c} × 1).', n(c), [f'Anything times 0 is 0, so ({a} × {b}) × 0 = 0.', f'{c} × 1 = {c}, and 0 + {c} = {c}.'],
            [n(a * b + c), '0', n(a * b * c)])


@std(sk(PF, 5))
def pf5_s(r):
    a, b = r.choice([3, 4, 6, 7, 8, 9]), r.randint(3, 9); x = r.randint(2, 9)
    return ('pf5_fact_then_add', f'Multiply {a} × {b}. Then add {x}.', n(a * b + x), [f'{a} × {b} = {a * b}.', f'{a * b} + {x} = {a * b + x}.'],
            [n(a * b), n(a * (b + x)), n(a + b + x)])


@adv(sk(PF, 5))
def pf5_a(r):
    a, b = r.choice([6, 7, 8, 9]), r.randint(6, 9)
    return ('pf5_known_fact_step', f'{r.choice(NAMES)} knows {a} × {b - 1} = {a * (b - 1)}. Use it to find {a} × {b}, then find {a} × {b} − {a} × {b - 2}.',
            n(2 * a), [f'{a} × {b} = {a * (b - 1)} + {a} = {a * b}.', f'{a} × {b - 2} = {a * (b - 2)}, and {a * b} − {a * (b - 2)} = {2 * a}.'],
            [n(a), n(a * b), n(b - (b - 2))])

# =============================================================== patterns, unknowns, two-step


@std(sk(UP, 1))
def up1_s(r):
    a, b, x = r.randint(2, 9), r.randint(2, 9), r.randint(2, 9)
    return ('up1_unknown_then_add', f'{a} × ? = {a * b}. Find the unknown, then add {x}.', n(b + x), [f'{a * b} ÷ {a} = {b}, so ? = {b}.', f'{b} + {x} = {b + x}.'],
            [n(b), n(a * b + x), n(a + x)])


@adv(sk(UP, 1))
def up1_a(r):
    a, b, c = r.randint(2, 9), r.randint(2, 9), r.randint(2, 9); need(b * c <= 100)
    return ('up1_two_equations', f'{a * b} ÷ {a} = □ and □ × {c} = △. What number is △?', n(b * c), [f'{a * b} ÷ {a} = {b}, so □ = {b}.', f'{b} × {c} = {b * c}, so △ = {b * c}.'],
            [n(b), n(a * c), n(b + c)])


@std(sk(UP, 2))
def up2_s(r):
    k, e, x = r.randint(3, 9), r.randint(3, 9), r.randint(2, 9)
    return ('up2_start_unknown_story', f'Some apples are packed in {k} bags with {e} apples in each bag. {x} apples are left over. How many apples were there?',
            qty(k * e + x, 'apples'), [f'{k} × {e} = {k * e} in bags.', f'{k * e} + {x} = {k * e + x} apples.'], [qty(k * e, 'apples'), qty(k + e + x, 'apples'), qty(k * (e + x), 'apples')])


@adv(sk(UP, 2))
def up2_a(r):
    k, e, x = r.randint(3, 9), r.randint(3, 9), r.randint(2, 9)
    return ('up2_backward_groups', f'{r.choice(NAMES)} had some markers and bought {x} more. Then the markers were put into {k} equal boxes with {e} in each box. How many markers were there at first?',
            qty(k * e - x, 'markers'), [f'In all: {k} × {e} = {k * e}.', f'Before buying {x} more: {k * e} − {x} = {k * e - x} markers.'], [qty(k * e, 'markers'), qty(k * e + x, 'markers'), qty(k + e - x, 'markers')])


@std(sk(UP, 3))
def up3_s(r):
    a, b = r.randint(2, 9), r.randint(2, 9) * 10; x = r.randint(1, 9) * 10
    return ('up3_tens_product_then_add', f'Multiply {a} × {b}. Then add {x}.', n(a * b + x), [f'{a} × {b} = {a} × {b // 10} tens = {a * b // 10} tens = {a * b}.', f'{a * b} + {x} = {a * b + x}.'],
            [n(a * b), n(a * (b + x)), n(a * b // 10 + x)])


@adv(sk(UP, 3))
def up3_a(r):
    a, b, c, d = r.randint(2, 9), r.randint(2, 9) * 10, r.randint(2, 9), r.randint(2, 9) * 10; need(a * b + c * d <= 1000)
    return ('up3_two_tens_products', f'A theater sells {a} rows of {b} seats on Friday and {c} rows of {d} seats on Saturday. How many seats is that in all?',
            qty(a * b + c * d, 'seats'), [f'{a} × {b} = {a * b} and {c} × {d} = {c * d}.', f'{a * b} + {c * d} = {a * b + c * d} seats.'],
            [qty(a * b, 'seats'), qty((a + c) * (b + d), 'seats'), qty(a * b + c * d - 10, 'seats')])


@std(sk(UP, 5))
def up5_s(r):
    k, e, s = r.randint(3, 9), r.randint(3, 9), r.randint(2, 9)
    tot = k * e; need(s < tot)
    return ('up5_groups_minus_sold', f'A baker makes {k} trays of {e} rolls. {s} rolls are sold. How many rolls are left?',
            qty(tot - s, 'rolls'), [f'{k} × {e} = {tot} rolls.', f'{tot} − {s} = {tot - s} rolls left.'], [qty(tot, 'rolls'), qty(tot + s, 'rolls'), qty(k + e - s if k + e > s else tot - s + 1, 'rolls')])


@adv(sk(UP, 5))
def up5_a(r):
    k, e, g = r.randint(3, 9), r.randint(3, 9), r.randint(2, 9); tot = k * e; extra = r.randint(2, 20); need((tot + extra) % g == 0)
    return ('up5_groups_add_share', f'There are {k} packs of {e} cards and {extra} loose cards. All the cards are shared equally among {g} players. How many cards does each player get?',
            qty((tot + extra) // g, 'cards'), [f'{k} × {e} + {extra} = {tot} + {extra} = {tot + extra} cards.', f'{tot + extra} ÷ {g} = {(tot + extra) // g} cards each.'],
            [qty(tot // g if tot % g == 0 else (tot + extra) // g + 1, 'cards'), qty(tot + extra, 'cards'), qty((tot + extra) // g - 1, 'cards')])


@std(sk(UP, 6))
def up6_s(r):
    p, c = r.randint(3, 9), r.randint(3, 9); x = r.randint(5, 30)
    who = r.choice(NAMES)
    return ('up6_cost_then_change', f'{who} buys {p} notebooks that cost ${c} each and pays with ${p * c + x}. How much change does {who} get?',
            f'${x}', [f'{p} × ${c} = ${p * c}.', f'${p * c + x} − ${p * c} = ${x}.'], [f'${p * c}', f'${x + c}', f'${p * c + x}'])


@adv(sk(UP, 6))
def up6_a(r):
    a, b, c, d = r.randint(3, 9), r.randint(3, 9), r.randint(3, 9), r.randint(3, 9); need(a * b != c * d)
    big, small = max(a * b, c * d), min(a * b, c * d)
    return ('up6_compare_two_products', f'The red team sold {a} boxes of {b} cookies. The blue team sold {c} boxes of {d} cookies. How many more cookies did the team that sold more sell?',
            qty(big - small, 'cookies'), [f'Red: {a} × {b} = {a * b}. Blue: {c} × {d} = {c * d}.', f'{big} − {small} = {big - small} cookies.'],
            [qty(big, 'cookies'), qty(abs((a + b) - (c + d)) or 1, 'cookies'), qty(big + small, 'cookies')])

# =============================================================== add and subtract within 1,000


@std(sk(AS, 1))
def as1_s(r):
    a, b = r.randint(11, 499), r.randint(11, 499)
    return ('as1_round_both_add', f'Round {a} and {b} to the nearest 10. Then add the rounded numbers.', n(rnd(a, 10) + rnd(b, 10)),
            [f'{a} rounds to {rnd(a, 10)} and {b} rounds to {rnd(b, 10)}.', f'{rnd(a, 10)} + {rnd(b, 10)} = {rnd(a, 10) + rnd(b, 10)}.'],
            [n(a + b), n(rnd(a, 10) + rnd(b, 10) + 10), n(rnd(a, 100) + rnd(b, 100))])


@adv(sk(AS, 1))
def as1_a(r):
    t = r.randint(3, 99) * 10
    return ('as1_how_many_round_to', f'How many whole numbers round to {t} when rounded to the nearest 10?', '10',
            [f'{t - 5}, {t - 4}, {t - 3}, {t - 2}, {t - 1}, {t}, {t + 1}, {t + 2}, {t + 3} and {t + 4} round to {t}.', 'That is 10 numbers.'], ['9', '11', '5'])


@std(sk(AS, 2))
def as2_s(r):
    a, b = r.randint(101, 899), r.randint(101, 899); need(a > b)
    return ('as2_round_both_subtract', f'Round {a} and {b} to the nearest 100. Then subtract the rounded numbers.', n(rnd(a, 100) - rnd(b, 100)),
            [f'{a} rounds to {rnd(a, 100)} and {b} rounds to {rnd(b, 100)}.', f'{rnd(a, 100)} − {rnd(b, 100)} = {rnd(a, 100) - rnd(b, 100)}.'],
            [n(a - b), n(rnd(a, 100) - rnd(b, 100) + 100), n(rnd(a, 10) - rnd(b, 10))])


@adv(sk(AS, 2))
def as2_a(r):
    t = r.randint(2, 9) * 100; which = r.choice(['greatest', 'least'])
    return ('as2_greatest_least_round', f'What is the {which} whole number that rounds to {t} when rounded to the nearest 100?',
            n(t + 49 if which == 'greatest' else t - 50), [f'Numbers from {t - 50} to {t + 49} round to {t}.', f'The {which} is {t + 49 if which == "greatest" else t - 50}.'],
            [n(t + 50 if which == 'greatest' else t - 49), n(t + 99 if which == 'greatest' else t - 99), n(t + 5 if which == 'greatest' else t - 5)])


@std(sk(AS, 3))
def as3_s(r):
    a, b, c = r.randint(100, 400), r.randint(100, 300), r.randint(10, 99); need(a + b + c <= 1000)
    return ('as3_three_addends', f'Add: {a} + {b} + {c}', n(a + b + c), [f'{a} + {b} = {a + b}.', f'{a + b} + {c} = {a + b + c}.'], [n(a + b), n(a + b + c + 10), n(a + b + c - 100)])


@adv(sk(AS, 3))
def as3_a(r):
    a, b, c = r.randint(100, 450), r.randint(100, 450), r.randint(20, 300); need(a + b <= 999 and a + b > c)
    return ('as3_two_days_then_more', f'A library lent {a} books on Monday and {b} books on Tuesday. On Wednesday it lent {c} fewer books than on Monday and Tuesday together. How many books did it lend on Wednesday?',
            qty(a + b - c, 'books'), [f'Monday and Tuesday: {a} + {b} = {a + b}.', f'Wednesday: {a + b} − {c} = {a + b - c} books.'], [qty(a + b, 'books'), qty(a + b + c, 'books'), qty(a - c if a > c else a + b - c + 10, 'books')])


@std(sk(AS, 4))
def as4_s(r):
    a, b = r.randint(400, 999), r.randint(100, 399); x = r.randint(10, 99)
    return ('as4_subtract_then_add', f'Subtract {a} − {b}. Then add {x}.', n(a - b + x), [f'{a} − {b} = {a - b}.', f'{a - b} + {x} = {a - b + x}.'], [n(a - b), n(a - b - x), n(a + b + x if a + b + x <= 999 else a - b + x + 100)])


@adv(sk(AS, 4))
def as4_a(r):
    a, b, c = r.randint(500, 999), r.randint(100, 300), r.randint(100, 300); need(a - b - c > 0)
    return ('as4_two_take_aways', f'A truck can carry {a} pounds. It already has boxes of {b} pounds and {c} pounds. How many more pounds can it carry?',
            qty(a - b - c, 'pounds'), [f'{b} + {c} = {b + c} pounds already on.', f'{a} − {b + c} = {a - b - c} pounds.'], [qty(a - b, 'pounds'), qty(a - b + c, 'pounds'), qty(b + c, 'pounds')])


@adv(sk(AS, 5))
def as5_a(r):
    a, b, c = r.randint(300, 700), r.randint(100, 300), r.randint(100, 300); need(a + b - c > 0)
    est = rnd(a, 100) + rnd(b, 100) - rnd(c, 100)
    return ('as5_estimate_two_step', f'A shop had {a} toys. It got {b} more and sold {c}. Round each number to the nearest 100 to estimate how many toys the shop has now.',
            qty(est, 'toys'), [f'{a} → {rnd(a, 100)}, {b} → {rnd(b, 100)}, {c} → {rnd(c, 100)}.', f'{rnd(a, 100)} + {rnd(b, 100)} − {rnd(c, 100)} = {est} toys.'],
            [qty(a + b - c, 'toys'), qty(est + 100, 'toys'), qty(rnd(a, 100) + rnd(b, 100), 'toys')])

# =============================================================== understanding fractions


@std(sk(UF, 1))
def uf1_s(r):
    d = r.choice([2, 3, 4, 6, 8]); u = r.randint(1, d - 1)
    return ('uf1_parts_left', f'A pan of cornbread is cut into {d} equal pieces. {u} {"piece is" if u == 1 else "pieces are"} eaten. What fraction of the pan is left?',
            fr(d - u, d), [f'There are {d} equal pieces, so each piece is 1/{d}.', f'{d} − {u} = {d - u} pieces are left: {d - u}/{d}.'], [fr(u, d), fr(d - u, d + 1), fr(1, d)])


@adv(sk(UF, 1))
def uf1_a(r):
    d = r.choice([3, 4, 6, 8]); a = r.randint(1, d - 2); b = r.randint(1, d - a - 1)
    return ('uf1_two_parts_rest', f'A garden is split into {d} equal parts. Beans grow in {a} {"part" if a == 1 else "parts"} and corn grows in {b} {"part" if b == 1 else "parts"}. Flowers grow in the rest. What fraction of the garden has flowers?',
            fr(d - a - b, d), [f'Beans and corn use {a} + {b} = {a + b} parts.', f'{d} − {a + b} = {d - a - b} parts have flowers: {d - a - b}/{d}.'], [fr(a + b, d), fr(d - a, d), fr(1, d)])


@std(sk(UF, 2))
def uf2_s(r):
    d = r.choice([3, 4, 6, 8]); k = r.randint(2, d - 1); x = r.randint(1, d - k)
    return ('uf2_copies_plus_more', f'Start with {k} copies of 1/{d}. Add {x} more {"copy" if x == 1 else "copies"} of 1/{d}. What fraction do you have?', fr(k + x, d),
            [f'{k} copies of 1/{d} is {k}/{d}.', f'{k} + {x} = {k + x} copies: {k + x}/{d}.'], [fr(k, d), fr(k + x, d + x), fr(k * x, d)])


@adv(sk(UF, 2))
def uf2_a(r):
    d = r.choice([4, 6, 8]); a = r.randint(2, d - 2); b = r.randint(1, a - 1)
    return ('uf2_copies_difference', f'{r.choice(NAMES)} ate {a}/{d} of a pizza. {r.choice(NAMES)} ate {b}/{d} of the same pizza. How many more copies of 1/{d} did the first person eat?',
            n(a - b), [f'{a}/{d} is {a} copies of 1/{d}; {b}/{d} is {b} copies.', f'{a} − {b} = {a - b}.'], [n(a), n(a + b), n(d - a)])


@std(sk(UF, 3))
def uf3_s(r):
    d = r.choice([3, 4, 6, 8]); k = r.randint(2, d - 1)
    return ('uf3_nth_mark', f'A ribbon that is 1 meter long is marked into {d} equal parts. Luis cuts at mark number {k}. How long is the piece from 0 to that mark?',
            f'{fr(k, d)} meter', [f'Each part is 1/{d} meter.', f'{k} parts is {k}/{d} meter.'], [f'{fr(1, d)} meter', f'{fr(k, d + 1)} meter', f'{fr(d - k if d > k else 1, d)} meter'])


@adv(sk(UF, 3))
def uf3_a(r):
    d = r.choice([3, 4, 6, 8]); a = r.randint(1, d - 2); b = r.randint(a + 1, d - 1)
    return ('uf3_between_marks', f'A trail from 0 to 1 mile has {d} equal parts. A bench is at {a}/{d} mile and a fountain is at {b}/{d} mile. How far is it from the bench to the fountain?',
            f'{fr(b - a, d)} mile', [f'Each part is 1/{d} mile.', f'From {a}/{d} to {b}/{d} is {b - a} parts: {b - a}/{d} mile.'], [f'{fr(b + a, d)} mile', f'{fr(b, d)} mile', f'{fr(1, d)} mile'])

# =============================================================== equivalent and comparing fractions


@std(sk(EC, 1))
def ec1_s(r):
    a, b = r.choice([(1, 2), (1, 3), (2, 3), (1, 4), (3, 4)]); k = 2
    return ('ec1_split_each_part', f'A strip shows {a}/{b} shaded. Each part is split into {k} equal pieces. How many pieces are shaded now, and what is the new fraction?',
            f'{a * k}; {a * k}/{b * k}', [f'Each of the {a} shaded parts becomes {k} pieces: {a} × {k} = {a * k}.', f'There are {b} × {k} = {b * k} pieces in all, so {a}/{b} = {a * k}/{b * k}.'],
            [f'{a + k}; {a + k}/{b + k}', f'{a * k}; {a * k}/{b}', f'{a}; {a}/{b * k}'])


@adv(sk(EC, 1))
def ec1_a(r):
    a, b = r.choice([(1, 2), (1, 3), (2, 3), (1, 4), (3, 4), (1, 2)]); k = r.choice([2, 4] if b <= 2 else [2])
    big = b * k; need(big <= 8)
    p, q = r.sample(NAMES, 2)
    return ('ec1_same_amount_pieces', f'{p} cut a pan into {b} equal pieces and ate {a}. {q} cut the same size pan into {big} equal pieces. How many pieces must {q} eat to eat the same amount?',
            qty(a * k, 'pieces'), [f'Each of the {b} pieces matches {k} of the smaller pieces.', f'{a} × {k} = {a * k} pieces, because {a}/{b} = {a * k}/{big}.'],
            [qty(a, 'pieces'), qty(a + k, 'pieces'), qty(big - a, 'pieces')])


@std(sk(EC, 2))
def ec2_s(r):
    a, b = r.choice([(1, 2), (1, 3), (2, 3), (1, 4), (3, 4), (1, 2)]); c = r.choice([x for x in (4, 6, 8) if x % b == 0 and x > b])
    m = a * c // b
    return ('ec2_missing_then_check', f'Find n: {a}/{b} = n/{c}. Then write the equivalent fraction.', f'{m}/{c}',
            [f'{b} × {c // b} = {c}, so multiply the numerator by {c // b} too.', f'n = {a} × {c // b} = {m}, so {a}/{b} = {m}/{c}.'], [f'{a}/{c}', f'{m + 1}/{c}', f'{a + c - b}/{c}'])


@adv(sk(EC, 2))
def ec2_a(r):
    a, b = r.choice([(1, 2), (1, 4), (3, 4), (1, 2)]); c1, c2 = (4, 8) if b <= 4 else (8, 8)
    need(c1 % b == 0)
    return ('ec2_two_equivalents', f'Write two fractions equal to {a}/{b}: one in {DNAME[c1]} and one in {DNAME[c2]}.',
            f'{a * c1 // b}/{c1}, {a * c2 // b}/{c2}', [f'{a}/{b} = {a * c1 // b}/{c1} (multiply top and bottom by {c1 // b}).', f'{a}/{b} = {a * c2 // b}/{c2} (multiply top and bottom by {c2 // b}).'],
            [f'{a}/{c1}, {a}/{c2}', f'{a + 1}/{c1}, {a + 3}/{c2}', f'{a * c1 // b}/{c2}, {a * c2 // b}/{c1}'])


@std(sk(EC, 3))
def ec3_s(r):
    w, d = r.randint(2, 6), r.choice([2, 3, 4, 6])
    return ('ec3_wholes_to_parts', f'How many {DNAME[d]} make {w} wholes? Write the fraction.', f'{w * d}/{d}',
            [f'1 whole is {d}/{d}.', f'{w} wholes is {w} × {d} = {w * d} {DNAME[d]}: {w * d}/{d}.'], [f'{w}/{d}', f'{w + d}/{d}', f'{d}/{w}'])


@adv(sk(EC, 3))
def ec3_a(r):
    d = r.choice([2, 3, 4, 6]); w1, w2 = r.randint(1, 4), r.randint(1, 4)
    return ('ec3_whole_sum', f'What whole number is {w1 * d}/{d} + {w2 * d}/{d}?', n(w1 + w2),
            [f'{w1 * d}/{d} = {w1} and {w2 * d}/{d} = {w2}.', f'{w1} + {w2} = {w1 + w2}.'], [n((w1 + w2) * d), n(w1 * w2), n(w1 + w2 + 1)])


@std(sk(EC, 4))
def ec4_s(r):
    d = r.choice([4, 6, 8]); xs = r.sample(range(1, d), 3)
    return ('ec4_order_three', f'Order from least to greatest: {", ".join(f"{x}/{d}" for x in xs)}', ', '.join(f'{x}/{d}' for x in sorted(xs)),
            ['The denominators are the same, so compare the numerators.', ', '.join(f'{x}/{d}' for x in sorted(xs)) + '.'],
            [', '.join(f'{x}/{d}' for x in sorted(xs, reverse=True)), ', '.join(f'{x}/{d}' for x in xs), ', '.join(f'{x}/{d}' for x in [sorted(xs)[1], sorted(xs)[0], sorted(xs)[2]])])


@adv(sk(EC, 4))
def ec4_a(r):
    d = r.choice([4, 6, 8]); a, b = r.sample(range(1, d), 2); p, q = r.sample(NAMES, 2)
    win = p if a > b else q
    return ('ec4_who_more_by', f'{p} ran {a}/{d} mile. {q} ran {b}/{d} mile on the same track. Who ran farther, and by how many {DNAME[d]}?',
            f'{win}, by {abs(a - b)}', [f'Same denominators: compare {a} and {b}.', f'{win} ran farther, by {max(a, b)} − {min(a, b)} = {abs(a - b)} {DNAME[d]}.'],
            [f'{q if win == p else p}, by {abs(a - b)}', f'{win}, by {a + b}', f'{win}, by {max(a, b)}'])


@std(sk(EC, 5))
def ec5_s(r):
    a = r.randint(1, 3); ds = r.sample([x for x in (2, 3, 4, 6, 8) if x > a], 3) if a < 2 else r.sample([x for x in (3, 4, 6, 8) if x > a], 3)
    return ('ec5_order_same_numerator', f'Order from greatest to least: {", ".join(f"{a}/{x}" for x in ds)}', ', '.join(f'{a}/{x}' for x in sorted(ds)),
            ['The numerators are the same, so the fraction with fewer, bigger parts is greater.', ', '.join(f'{a}/{x}' for x in sorted(ds)) + '.'],
            [', '.join(f'{a}/{x}' for x in sorted(ds, reverse=True)), ', '.join(f'{a}/{x}' for x in ds), ', '.join(f'{a}/{x}' for x in [sorted(ds)[1], sorted(ds)[0], sorted(ds)[2]])])


@adv(sk(EC, 5))
def ec5_a(r):
    a = r.randint(1, 3); d1, d2 = r.sample([x for x in (2, 3, 4, 6, 8) if x > a], 2); p, q = r.sample(NAMES, 2)
    win = p if d1 < d2 else q
    return ('ec5_same_numerator_story', f'{p} ate {a}/{d1} of a sandwich. {q} ate {a}/{d2} of a sandwich of the same size. Who ate more?',
            win, [f'Both ate {a} pieces. {DNAME[min(d1, d2)].capitalize()} are bigger pieces than {DNAME[max(d1, d2)]}.', f'{win} ate more.'],
            [q if win == p else p, 'They ate the same amount', 'You cannot tell'])

# =============================================================== time, volume and mass


@std(sk(TM, 1))
def tm1_s(r):
    h, m = r.randint(1, 11), r.randint(1, 11) * 5 + r.choice([1, 2, 3, 4]); need(m < 60); x = r.randint(5, 20)
    t0 = h * 60 + m
    return ('tm1_read_then_later', f'A clock shows {tm(t0)}. What time will it show {x} minutes later?', tm(t0 + x),
            [f'Start at {tm(t0)}.', f'{x} minutes later is {tm(t0 + x)}.'], [tm(t0 + x + 5), tm(t0 - x), tm(t0 + x - 1)])


@adv(sk(TM, 1))
def tm1_a(r):
    h = r.randint(1, 11); b = r.randint(3, 25)
    t0 = (h + 1) * 60 - b
    return ('tm1_minutes_before', f'Which time is {b} minutes before {h + 1 if h < 12 else 1}:00?', tm(t0),
            [f'{h + 1}:00 is the same as {h}:60.', f'{h}:60 − {b} minutes = {tm(t0)}.'], [tm((h + 1) * 60 + b), tm(h * 60 + b), tm(t0 + 10)])


@std(sk(TM, 2))
def tm2_s(r):
    h = r.randint(1, 10); m = r.randint(0, 45); a, b = r.randint(10, 30), r.randint(10, 25)
    t0 = h * 60 + m
    who = r.choice(NAMES)
    return ('tm2_two_activities_end', f'{who} starts reading at {tm(t0)} and reads for {a} minutes. Then {who} draws for {b} minutes. What time does {who} finish?',
            tm(t0 + a + b), [f'{a} + {b} = {a + b} minutes in all.', f'{tm(t0)} + {a + b} minutes = {tm(t0 + a + b)}.'], [tm(t0 + a), tm(t0 + a + b + 10), tm(t0 + b)])


@adv(sk(TM, 2))
def tm2_a(r):
    h = r.randint(1, 10); m = r.randint(0, 50); d1, d2 = r.randint(15, 50), r.randint(15, 50); need(d1 != d2)
    t0 = h * 60 + m; p, q = r.sample(NAMES, 2); win = q if d2 > d1 else p
    return ('tm2_who_longer', f'{p} practiced from {tm(t0)} to {tm(t0 + d1)}. {q} practiced from {tm(t0)} to {tm(t0 + d2)}. Who practiced longer, and by how many minutes?',
            f'{win}, by {abs(d1 - d2)} minutes', [f'{p}: {d1} minutes. {q}: {d2} minutes.', f'{win} practiced {abs(d1 - d2)} minutes longer.'],
            [f'{q if win == p else p}, by {abs(d1 - d2)} minutes', f'{win}, by {d1 + d2} minutes', f'{win}, by {max(d1, d2)} minutes'])


@std(sk(TM, 4))
def tm4_s(r):
    k, w, x = r.randint(2, 9), r.choice([10, 20, 50, 100]), r.choice([5, 10, 20])
    return ('tm4_weights_plus', f'A balance scale is level. One side has a box. The other side has {k} weights of {w} grams each and one {x}-gram weight. What is the mass of the box?',
            qty(k * w + x, 'grams'), [f'{k} × {w} = {k * w} grams.', f'{k * w} + {x} = {k * w + x} grams.'], [qty(k * w, 'grams'), qty(k + w + x, 'grams'), qty(k * (w + x), 'grams')])


@adv(sk(TM, 4))
def tm4_a(r):
    a, b = r.randint(100, 500), r.randint(100, 400); k = r.randint(2, 4); need(k * a > b and k * a <= 1000)
    return ('tm4_total_then_compare', f'A melon has a mass of {a} grams. A bag of apples has a mass of {b} grams. A box holds {k} melons. How many grams heavier is the box of melons than the bag of apples?',
            qty(k * a - b, 'grams'), [f'{k} × {a} = {k * a} grams of melons.', f'{k * a} − {b} = {k * a - b} grams.'], [qty(a - b if a > b else b - a, 'grams'), qty(k * a + b, 'grams'), qty(k * a, 'grams')])


@std(sk(TM, 5))
def tm5_s(r):
    k, e, x = r.randint(2, 9), r.randint(2, 9), r.randint(2, 9)
    return ('tm5_buckets_plus', f'{k} buckets each hold {e} liters of water. {x} more liters are poured into the tub with them. How many liters is that in all?',
            qty(k * e + x, 'liters'), [f'{k} × {e} = {k * e} liters.', f'{k * e} + {x} = {k * e + x} liters.'], [qty(k * e, 'liters'), qty(k + e + x, 'liters'), qty(k * (e + x), 'liters')])


@adv(sk(TM, 5))
def tm5_a(r):
    tot, used, k = r.randint(20, 90), r.randint(2, 20), r.randint(2, 9); rest = tot - used; need(rest > 0 and rest % k == 0)
    return ('tm5_use_then_share', f'A tank has {tot} liters of water. {used} liters are used to wash a car. The rest is poured equally into {k} buckets. How many liters are in each bucket?',
            qty(rest // k, 'liters'), [f'{tot} − {used} = {rest} liters left.', f'{rest} ÷ {k} = {rest // k} liters in each bucket.'], [qty(tot // k if tot % k == 0 else rest // k + 1, 'liters'), qty(rest, 'liters'), qty(rest // k + 2, 'liters')])

# =============================================================== graphs and measurement data


@std(sk(GD, 3))
def gd3_s(r):
    s = r.choice([2, 5, 10]); a, b = r.randint(2, 9) * s, r.randint(2, 9) * s; need(a != b)
    return ('gd3_symbols_for_two', f'In a picture graph, each symbol stands for {s}. Apples got {a} votes and pears got {b} votes. How many symbols are drawn in all for apples and pears?',
            qty((a + b) // s, 'symbols'), [f'Apples: {a} ÷ {s} = {a // s}. Pears: {b} ÷ {s} = {b // s}.', f'{a // s} + {b // s} = {(a + b) // s} symbols.'],
            [qty(a + b, 'symbols'), qty(a // s, 'symbols'), qty((a + b) // s + 1, 'symbols')])


@adv(sk(GD, 3))
def gd3_a(r):
    s = r.choice([2, 5, 10]); a = r.randint(2, 8); b = r.randint(2, 8); need(a != b)
    return ('gd3_more_from_symbols', f'In a picture graph, each symbol stands for {s} books. Ana has {a} symbols and Ben has {b} symbols. How many more books does the reader with more symbols have?',
            qty(abs(a - b) * s, 'books'), [f'{max(a, b)} − {min(a, b)} = {abs(a - b)} more symbols.', f'{abs(a - b)} × {s} = {abs(a - b) * s} books.'],
            [qty(abs(a - b), 'books'), qty(max(a, b) * s, 'books'), qty((a + b) * s, 'books')])


@adv(sk(GD, 4))
def gd4_a(r):
    w = r.randint(1, 6); q1, q2 = r.choice([(1, 2), (1, 4), (3, 4)]), r.choice([(1, 2), (1, 4), (3, 4)])
    a = Fr(w) + Fr(*q1); b = a + Fr(1, 4) * r.randint(1, 3)
    def mixed(x): return f'{x.numerator // x.denominator} {x - x.numerator // x.denominator}' if x.denominator > 1 else str(x.numerator)
    d = b - a
    return ('gd4_quarter_inch_difference', f'One ribbon is {mixed(a)} inches long. Another ribbon is {mixed(b)} inches long. How many quarter inches longer is the second ribbon?',
            n(int(d * 4)), [f'{mixed(b)} − {mixed(a)} = {d} inch.', f'{d} inch is {int(d * 4)} quarter inches.'], [n(int(d * 4) + 1), n(int(d * 2) or 2), n(int(d * 4) * 2)])

# =============================================================== area


@std(sk(AR, 1))
def ar1_s(r):
    a, b = r.randint(5, 30), r.randint(5, 30)
    return ('ar1_two_shapes_total', f'Shape A is covered by {a} unit squares with no gaps or overlaps. Shape B is covered by {b} unit squares of the same size. What is the total area of both shapes?',
            qty(a + b, 'square units'), [f'Area A is {a} square units and area B is {b} square units.', f'{a} + {b} = {a + b} square units.'], [qty(abs(a - b), 'square units'), qty(a * b, 'square units'), qty(a + b, 'units')])


@adv(sk(AR, 1))
def ar1_a(r):
    l, w = r.randint(3, 9), r.randint(3, 9); have = r.randint(5, l * w - 2)
    return ('ar1_squares_still_needed', f'{r.choice(NAMES)} wants to cover a rectangle that is {l} units long and {w} units wide with unit squares. {have} squares are already placed. How many more squares are needed?',
            qty(l * w - have, 'squares'), [f'The rectangle needs {l} × {w} = {l * w} unit squares.', f'{l * w} − {have} = {l * w - have} more squares.'], [qty(l * w, 'squares'), qty(l + w - have if l + w > have else 2 * (l + w), 'squares'), qty(l * w - have + 1, 'squares')])


@std(sk(AR, 2))
def ar2_s(r):
    a, b = r.randint(5, 40), r.randint(5, 40); u = r.choice(['centimeter', 'meter', 'inch', 'foot'])
    units = {'centimeter': 'square centimeters', 'meter': 'square meters', 'inch': 'square inches', 'foot': 'square feet'}[u]
    return ('ar2_count_two_parts', f'One part of a shape is covered with {a} squares and the other part with {b} squares. Each square is 1 {u} long on each side. What is the area of the whole shape?',
            qty(a + b, units), [f'{a} + {b} = {a + b} squares.', f'Each square is 1 square {u}, so the area is {a + b} {units}.'], [qty(a + b, units.replace("square ", "")), qty(a * b, units), qty(abs(a - b), units)])


@adv(sk(AR, 2))
def ar2_a(r):
    a, b = r.randint(10, 40), r.randint(10, 40); need(a != b); u = r.choice(['centimeter', 'inch'])
    units = {'centimeter': 'square centimeters', 'inch': 'square inches'}[u]
    return ('ar2_compare_counts', f'Card A is covered by {a} squares and card B by {b} squares. Each square is 1 {u} on each side. How much greater is the area of the larger card?',
            qty(abs(a - b), units), [f'Areas: {a} and {b} {units}.', f'{max(a, b)} − {min(a, b)} = {abs(a - b)} {units}.'], [qty(a + b, units), qty(abs(a - b), units.replace("square ", "")), qty(max(a, b), units)])


@std(sk(AR, 3))
def ar3_s(r):
    l, w, x = r.randint(3, 9), r.randint(3, 9), r.randint(1, 3)
    return ('ar3_longer_rectangle', f'A rectangle is {l} feet by {w} feet. It is made {x} {"foot" if x == 1 else "feet"} longer on the {l}-foot side. What is the new area?',
            qty((l + x) * w, 'square feet'), [f'New side: {l} + {x} = {l + x} feet.', f'{l + x} × {w} = {(l + x) * w} square feet.'], [qty(l * w, 'square feet'), qty(l * w + x, 'square feet'), qty((l + x) * (w + x), 'square feet')])


@adv(sk(AR, 3))
def ar3_a(r):
    l, w = r.randint(3, 9), r.randint(3, 9); l2 = r.randint(2, 10); need(l * w % l2 == 0 and l2 != l and l * w // l2 <= 10)
    return ('ar3_same_area_side', f'Rug A is {l} feet by {w} feet. Rug B has the same area and one side is {l2} feet. How long is the other side of rug B?',
            qty(l * w // l2, 'feet'), [f'Area of rug A: {l} × {w} = {l * w} square feet.', f'{l * w} ÷ {l2} = {l * w // l2} feet.'], [qty(l * w, 'feet'), qty(l * w - l2, 'feet'), qty(l + w - l2 if l + w > l2 else 1, 'feet')])

# =============================================================== perimeter and shapes


@adv(sk(PS, 1))
def ps1_a(r):
    l, w = r.randint(3, 20), r.randint(3, 20); need(l != w); g = r.randint(1, 4)
    return ('ps1_fence_minus_gate', f'A garden is {l} feet long and {w} feet wide. A gate {g} {"foot" if g == 1 else "feet"} wide needs no fence. How many feet of fence are needed?',
            qty(2 * (l + w) - g, 'feet'), [f'Perimeter: {l} + {w} + {l} + {w} = {2 * (l + w)} feet.', f'{2 * (l + w)} − {g} = {2 * (l + w) - g} feet.'], [qty(2 * (l + w), 'feet'), qty(l * w - g, 'feet'), qty(l + w - g, 'feet')])


@std(sk(PS, 3))
def ps3_s(r):
    l, w = r.randint(2, 9), r.randint(2, 9); need(l != w)
    return ('ps3_area_and_perimeter', f'A rectangle is {l} by {w}. Find its perimeter and its area.', f'{2 * (l + w)} units; {l * w} square units',
            [f'Perimeter: 2 × ({l} + {w}) = {2 * (l + w)} units.', f'Area: {l} × {w} = {l * w} square units.'],
            [f'{l * w} units; {2 * (l + w)} square units', f'{l + w} units; {l * w} square units', f'{2 * (l + w)} units; {2 * l * w} square units'])


@adv(sk(PS, 3))
def ps3_a(r):
    P = r.choice([12, 14, 16, 18, 20, 24]); s = P // 2
    best = max(a * (s - a) for a in range(1, s))
    return ('ps3_greatest_area', f'A rectangle with whole-number sides has a perimeter of {P} feet. What is the greatest area it can have?',
            qty(best, 'square feet'), [f'The length and width add to {P} ÷ 2 = {s}.', f'The closest sides give the greatest area: {s // 2} × {s - s // 2} = {best} square feet.'],
            [qty(s - 1, 'square feet'), qty(P, 'square feet'), qty(best - 2, 'square feet')])


@adv(sk(PS, 4))
def ps4_a(r):
    shapes = [('triangle', 3), ('square', 4), ('rectangle', 4), ('pentagon', 5), ('hexagon', 6), ('octagon', 8), ('trapezoid', 4), ('rhombus', 4)]
    (s1, n1), (s2, n2) = r.sample(shapes, 2); k1, k2 = r.randint(2, 4), r.randint(2, 4)
    pl = lambda s, k: s + ('es' if s.endswith('s') else 's') if k > 1 else s
    return ('ps4_count_sides', f'How many sides are on {k1} {pl(s1, k1)} and {k2} {pl(s2, k2)} in all?', n(k1 * n1 + k2 * n2),
            [f'{k1} × {n1} = {k1 * n1} and {k2} × {n2} = {k2 * n2}.', f'{k1 * n1} + {k2 * n2} = {k1 * n1 + k2 * n2} sides.'], [n(k1 * n1), n((k1 + k2) * 4), n(k1 + k2 + n1 + n2)])


@std(sk(PS, 5))
def ps5_s(r):
    tot = r.choice([12, 16, 18, 20, 24, 30, 36]); p = r.choice([d for d in (2, 3, 4, 6) if tot % d == 0]); x = r.randint(1, p - 1)
    return ('ps5_parts_shaded_squares', f'A rectangle made of {tot} unit squares is split into {p} parts with equal area. {x} {"part is" if x == 1 else "parts are"} shaded. How many unit squares are shaded?',
            n(tot // p * x), [f'Each part has {tot} ÷ {p} = {tot // p} unit squares.', f'{x} × {tot // p} = {tot // p * x} unit squares.'], [n(tot // p), n(x), n(tot - x)])
