"""2nd Grade Math audit #8 (2026-11-19): on-skill select-all items with 2, 3 or 4 correct choices.

Before the audit all 142 Grade 2 select-all items used one template ("Select ALL the problems that are matched with
the correct answer") and had exactly 2 of 4 correct. Each is rewritten in place (ID, skill and level kept) by a family
that picks its correct and wrong choices from the skill itself: 5 choices, with the number correct cycling 2, 3, 4."""
import random
from lib import UNITS, n
import fams
from fams import Skip, need, tm

NOTE = ('Original Claude-authored item (family: {fam}). 2nd Grade Math audit 2026-11-19 (#8, select-all with {k} correct); '
        'every choice recomputed by scripts/test-grade2-audit.cjs.')
G = {}
AF, AH, WP, PV, CC, AT, OE, ML, LN, TM, GD, SH = (fams.AF, fams.AH, fams.WP, fams.PV, fams.CC, fams.AT, fams.OE, fams.ML, fams.LN, fams.TM, fams.GD, fams.SH)


def sel(unit, i):
    def d(f):
        G[f'{unit}-skill-{i:02d}'] = f; return f
    return d


def pick(r, good, bad, k):
    good, bad = list(dict.fromkeys(good)), [b for b in dict.fromkeys(bad) if b not in good]
    need(len(good) >= k and len(bad) >= 5 - k)
    return r.sample(good, k), r.sample(bad, 5 - k)


def sums_equal(r, t, lo, hi, k, sub=False):
    good, bad = [], []
    for _ in range(80):
        a = r.randint(lo, hi)
        if sub:
            if a + t <= 999 and a + t > a:
                good.append(f'{a + t} − {a}'); bad.append(f'{a + t + r.choice([1, -1, 10, -10])} − {a}')
        elif 0 < t - a:
            good.append(f'{a} + {t - a}'); bad.append(f'{a} + {t - a + r.choice([1, -1, 10, -10])}')
    return pick(r, good, bad, k)


@sel(AF, 1)
def s_af1(r, L, k):
    t = r.randint(11, 18); g, b = sums_equal(r, t, 2, 9, k)
    return ('af1_select_sum', f'Select ALL the facts with a sum of {t}.', g, b, [f'Add each fact and look for {t}.'])


@sel(AF, 2)
def s_af2(r, L, k):
    t = r.randint(3, 9); good = [f'{a} − {a - t}' for a in range(t + 1, 19)]; bad = [f'{a} − {a - t - 1}' for a in range(t + 2, 19)] + [f'{a} − {a - t + 1}' for a in range(t, 19) if a - t + 1 > 0]
    g, b = pick(r, good, bad, k)
    return ('af2_select_difference', f'Select ALL the facts with a difference of {t}.', g, b, [f'Subtract each fact and look for {t}.'])


@sel(AF, 3)
def s_af3(r, L, k):
    a, b = r.randint(3, 9), r.randint(3, 9); need(a != b); s = a + b
    good = [f'{a} + {b} = {s}', f'{b} + {a} = {s}', f'{s} − {a} = {b}', f'{s} − {b} = {a}']
    bad = [f'{a} − {b} = {s}', f'{s} + {a} = {b}', f'{a} + {s} = {b}', f'{b} − {a} = {s}', f'{s} − {a} = {a}']
    g, bb = pick(r, good, bad, k)
    return ('af3_select_family', f'Select ALL the facts in the fact family for {a}, {b} and {s}.', g, bb, [f'The family uses {a} + {b} = {s} and its related facts.'])


@sel(AF, 4)
def s_af4(r, L, k):
    x = r.randint(2, 9); good = [f'{a} + ___ = {a + x}' for a in range(2, 11)] + [f'___ + {a} = {a + x}' for a in range(2, 11)]
    bad = [f'{a} + ___ = {a + x + 1}' for a in range(2, 11)] + [f'{a + x} + ___ = {a}' for a in range(2, 4)]
    g, b = pick(r, good, [y for y in bad if not y.startswith(f'{x}')], k)
    return ('af4_select_missing_is', f'Select ALL the equations where the missing number is {x}.', g, b, [f'Put {x} in the blank and check.'])


@sel(AH, 1)
def s_ah1(r, L, k):
    t = r.randint(50, 99); g, b = sums_equal(r, t, 11, t - 11, k)
    return ('ah1_select_sum', f'Select ALL the sums that equal {t}.', g, b, [f'Add each pair and look for {t}.'])


@sel(AH, 2)
def s_ah2(r, L, k):
    t = r.randint(15, 60); g, b = sums_equal(r, t, 11, 99 - t, k, sub=True)
    return ('ah2_select_difference', f'Select ALL the differences that equal {t}.', g, b, [f'Subtract each pair and look for {t}.'])


@sel(AH, 3)
def s_ah3(r, L, k):
    a, b = r.randint(15, 50), r.randint(11, 40); s = a + b; need(s <= 99)
    good = [f'{a} + {b} = {s}', f'{b} + {a} = {s}', f'{s} − {a} = {b}', f'{s} − {b} = {a}']
    bad = [f'{a} − {b} = {s}', f'{s} + {a} = {b}', f'{s} − {a} = {a}', f'{a} + {s} = {b}', f'{b} + {b} = {s}' if 2 * b != s else f'{a} + {a} = {s + 1}']
    g, bb = pick(r, good, bad, k)
    return ('ah3_select_related', f'Select ALL the true equations that use {a}, {b} and {s}.', g, bb, [f'{a} + {b} = {s}, so {s} − {a} = {b} and {s} − {b} = {a}.'])


@sel(AH, 4)
def s_ah4(r, L, k):
    t = r.randint(60, 99); good, bad = [], []
    for _ in range(60):
        a, b = r.randint(11, 30), r.randint(11, 30); c = t - a - b
        if 5 < c < 40:
            good.append(f'{a} + {b} + {c}'); bad.append(f'{a} + {b} + {c + r.choice([1, -1, 10, -10])}')
    g, bb = pick(r, good, bad, k)
    return ('ah4_select_three_sum', f'Select ALL the sums that equal {t}.', g, bb, [f'Add each set and look for {t}.'])


@sel(AH, 5)
def s_ah5(r, L, k):
    a, b = r.randint(21, 59), r.randint(21, 39); need(a + b <= 99); s = a + b
    good = [f'{b} + {a}', f'{a + 1} + {b - 1}', f'{a - 1} + {b + 1}', f'{a} + {b // 10 * 10} + {b % 10}', f'{a + 2} + {b - 2}']
    bad = [f'{a} + {b + 1}', f'{a + 10} + {b}', f'{a} + {b // 10} + {b % 10}', f'{a - 1} + {b - 1}', f'{a + 1} + {b + 1}']
    g, bb = pick(r, good, bad, k)
    return ('ah5_select_same_sum', f'Select ALL the ways that give the same sum as {a} + {b}.', g, bb, [f'{a} + {b} = {s}. Moving 1 or 2 from one addend to the other keeps the sum.'])


@sel(AT, 1)
def s_at1(r, L, k):
    t = r.randint(400, 900); g, b = sums_equal(r, t, 110, t - 110, k)
    return ('at1_select_sum', f'Select ALL the sums that equal {t}.', g, b, [f'Add each pair and look for {t}.'])


@sel(AT, 2)
def s_at2(r, L, k):
    good, bad = [], []
    for _ in range(80):
        a, b = r.randint(110, 480), r.randint(110, 480)
        (good if a % 10 + b % 10 >= 10 else bad).append(f'{a} + {b}')
    g, bb = pick(r, good, bad, k)
    return ('at2_select_new_ten', 'Select ALL the sums where you need to make a new ten from the ones.', g, bb, ['Add the ones digits; if they make 10 or more, you make a new ten.'])


@sel(AT, 3)
def s_at3(r, L, k):
    t = r.randint(150, 500); g, b = sums_equal(r, t, 110, 999 - t, k, sub=True)
    return ('at3_select_difference', f'Select ALL the differences that equal {t}.', g, b, [f'Subtract each pair and look for {t}.'])


@sel(AT, 4)
def s_at4(r, L, k):
    good, bad = [], []
    for _ in range(80):
        a, b = r.randint(300, 999), r.randint(110, 299)
        (good if a % 10 < b % 10 else bad).append(f'{a} − {b}')
    g, bb = pick(r, good, bad, k)
    return ('at4_select_trade_ten', 'Select ALL the subtractions where you must trade a ten for 10 ones.', g, bb, ['Trade when the ones digit on top is smaller than the ones digit below.'])


@sel(CC, 1)
def s_cc1(r, L, k):
    a = r.randint(150, 900); good = [n(a + i) for i in range(1, 10)]; bad = [n(a - i) for i in range(0, 6)] + [n(a + 10 * i) for i in range(1, 4)]
    g, b = pick(r, good, bad, k)
    return ('cc1_select_between', f'Select ALL the numbers greater than {a} and less than {a + 10}.', g, b, [f'Count on from {a}.'])


@sel(CC, 2)
def s_cc2(r, L, k):
    step = [5, 10, 100][L]; s = r.randint(1, 5) * step + (r.randint(1, 4) if step == 10 else 0)
    good = [n(s + step * i) for i in range(1, 9) if s + step * i <= 1000]; bad = [n(s + step * i + d) for i in range(1, 6) for d in ((1, 3) if step != 100 else (10, 50)) if s + step * i + d <= 1000]
    g, b = pick(r, good, bad, k)
    return ('cc2_select_skip_hits', f'Skip count by {step}s from {s}. Select ALL the numbers you will say.', g, b, [f'Add {step} each time, starting at {s}.'])


@sel(CC, 3)
def s_cc3(r, L, k):
    t = r.randint(200, 800); near = [t + d for d in (-90, -50, -11, -10, -1, 1, 9, 10, 11, 50, 90, 100)]
    g, b = pick(r, [n(x) for x in near if x > t], [n(x) for x in near if x < t], k)
    return ('cc3_select_greater', f'Select ALL the numbers greater than {t}.', g, b, ['Compare hundreds, then tens, then ones.'])


@sel(CC, 4)
def s_cc4(r, L, k):
    a = r.randint(120, 880); x = r.choice([10, 100])
    good = [f'{a + x - y} + {y}' for y in (0, 10, 100) if a + x - y > 0][:1] + [f'{a} + {x}', f'{x} + {a}', f'{a + 2 * x} − {x}', f'{a + x + 10} − 10']
    bad = [f'{a} + {x + 1}', f'{a} − {x}', f'{a + x} + {x}', f'{a} + {x * 10}' if a + x * 10 <= 1000 else f'{a} + 1', f'{a + x} − {x}']
    g, bb = pick(r, good, bad, k)
    return ('cc4_select_equals_more', f'Select ALL the expressions equal to {x} more than {a}.', g, bb, [f'{x} more than {a} is {a + x}.'])


@sel(GD, 3)
def s_gd3(r, L, k):
    a, b, c = r.sample(range(3, 15), 3); names = ['apples', 'bananas', 'grapes']; v = dict(zip(names, [a, b, c]))
    stmts = {f'{x} has more votes than {y}': v[x] > v[y] for x in names for y in names if x != y}
    stmts.update({f'{x} and {y} have {v[x] + v[y]} votes together': True for x in names for y in names if x < y})
    stmts.update({f'{x} and {y} have {v[x] + v[y] + 1} votes together': False for x in names for y in names if x < y})
    g, bb = pick(r, [s for s, t in stmts.items() if t], [s for s, t in stmts.items() if not t], k)
    return ('gd3_select_true_graph', f'A bar graph shows apples {a}, bananas {b} and grapes {c}. Select ALL the true statements.', g, bb, ['Read each bar and check each statement.'])


@sel(GD, 4)
def s_gd4(r, L, k):
    a, b, c = r.sample(range(2, 12), 3)
    good = [f'the apple bar is {a} tall', f'the banana bar is {b} tall', f'the grape bar is {c} tall', f'the tallest bar is {max(a, b, c)} tall']
    bad = [f'the apple bar is {a + 1} tall', f'the banana bar is {b + 2} tall', f'the grape bar is {c - 1} tall', f'the tallest bar is {min(a, b, c)} tall', f'the apple bar is {b} tall' if a != b else f'the apple bar is {a + 3} tall']
    g, bb = pick(r, good, bad, k)
    return ('gd4_select_bar_heights', f'Data: apples {a}, bananas {b}, grapes {c}. Select ALL that are true of a correct bar graph.', g, bb, ['Each bar is as tall as its number.'])


@sel(LN, 1)
def s_ln1(r, L, k):
    t = r.randint(50, 99); g, b = sums_equal(r, t, 10, t - 10, k)
    return ('ln1_select_total_length', f'Select ALL the pairs of lengths (in meters) that make {t} meters together.', g, b, [f'Add each pair and look for {t}.'])


@sel(LN, 2)
def s_ln2(r, L, k):
    d = r.randint(8, 30); good = [f'from {a} to {a + d}' for a in range(0, 60, 7)]; bad = [f'from {a} to {a + d + r.choice([1, -1, 10])}' for a in range(3, 60, 7)]
    g, b = pick(r, good, bad, k)
    return ('ln2_select_length', f'Select ALL the lengths on a number line that are {d} units long.', g, b, ['Subtract the start from the end.'])


@sel(LN, 3)
def s_ln3(r, L, k):
    t = r.randint(30, 80); good, bad = [], []
    for _ in range(60):
        a, j = r.randint(10, 60), r.randint(5, 30)
        if a + j == t or a - j == t: continue
        bad.append(f'start at {a}, jump forward {j}')
    for a in range(t - 30, t, 4):
        if a > 0: good.append(f'start at {a}, jump forward {t - a}')
    for a in range(t + 4, min(t + 40, 100), 5): good.append(f'start at {a}, jump back {a - t}')
    g, b = pick(r, good, bad, k)
    return ('ln3_select_land_on', f'Select ALL the jumps that land on {t}.', g, b, [f'Add for a jump forward and subtract for a jump back; look for {t}.'])


@sel(ML, 1)
def s_ml1(r, L, k):
    good = ['line up one end with 0', 'keep the ruler straight along the object', 'read the mark at the other end', 'count the units from 0 to the end']
    bad = ['start at the 1 mark and read the end', 'leave gaps between rulers', 'tilt the ruler', 'count the marks before 0', 'read the end of the ruler instead of the object']
    g, b = pick(r, good, bad, k)
    return ('ml1_select_measure_right', 'Select ALL the right ways to measure with a ruler.', g, b, ['Line up 0 with one end and read the other end.'])


@sel(ML, 2)
def s_ml2(r, L, k):
    unit = r.choice(['inches', 'meters'])
    objs = {'inches': (['pencil', 'book', 'crayon', 'shoe', 'spoon'], ['soccer field', 'school hallway', 'road', 'swimming pool']),
            'meters': (['soccer field', 'school hallway', 'swimming pool', 'playground', 'bus'], ['crayon', 'paper clip', 'eraser', 'button'])}[unit]
    g, b = pick(r, objs[0], objs[1], k)
    return ('ml2_select_best_unit', f'Select ALL the things you would measure in {unit}.', g, b, [f'Use {unit} for things about the right size for that unit.'])


@sel(ML, 3)
def s_ml3(r, L, k):
    f = r.randint(2, 5)
    good = [f'{f * 12} inches', f'{f} feet', f'{" + ".join(["12"] * f)} inches', f'{f - 1} feet and 12 inches']
    bad = [f'{f * 10} inches', f'{f + 12} inches', f'{f * 12} feet', f'{f} inches', f'{f + 1} feet']
    g, bb = pick(r, good, bad, k)
    return ('ml3_select_same_length', f'Select ALL the lengths equal to {f} feet. (1 foot = 12 inches)', g, bb, [f'{f} feet = {f} × 12 = {f * 12} inches.'])


@sel(ML, 5)
def s_ml5(r, L, k):
    t = r.randint(5, 25); good = [f'{a + t} cm and {a} cm' for a in range(5, 50, 6)]; bad = [f'{a + t + r.choice([1, -1, 5])} cm and {a} cm' for a in range(8, 50, 6)]
    g, b = pick(r, good, bad, k)
    return ('ml5_select_difference', f'Select ALL the pairs where the first length is {t} centimeters longer than the second.', g, b, ['Subtract the second length from the first.'])


@sel(OE, 1)
def s_oe1(r, L, k):
    want = r.choice(['even', 'odd']); xs = list(range(1, 21))
    g, b = pick(r, [str(x) for x in xs if (x % 2 == 0) == (want == 'even')], [str(x) for x in xs if (x % 2 == 0) != (want == 'even')], k)
    return ('oe1_select_parity', f'Select ALL the {want} numbers.', g, b, ['Even numbers end in 0, 2, 4, 6 or 8.'])


@sel(OE, 2)
def s_oe2(r, L, k):
    good = [str(2 * d) for d in range(2, 11)]; bad = [str(2 * d + 1) for d in range(1, 10)]
    g, b = pick(r, good, bad, k)
    return ('oe2_select_doubles', 'Select ALL the numbers that can be written as the sum of two equal addends.', g, b, ['A number is a double when it is even: it splits into two equal addends.'])


@sel(OE, 3)
def s_oe3(r, L, k):
    t = r.choice([6, 8, 10, 12, 15, 16, 20]); good = [f'{a} rows of {t // a}' for a in range(1, 6) if t % a == 0 and t // a <= 5] + [f'{" + ".join([str(t // a)] * a)}' for a in range(2, 5) if t % a == 0 and t // a <= 5]
    bad = [f'{a} rows of {b}' for a in range(2, 6) for b in range(2, 6) if a * b != t and abs(a * b - t) <= 3]
    g, b = pick(r, good, bad, k)
    return ('oe3_select_array_total', f'Select ALL that show {t} in all.', g, b, ['Add the rows, or add the same number again and again.'])


@sel(OE, 4)
def s_oe4(r, L, k):
    t = r.choice([8, 10, 12, 15, 20])
    good = [f'{a} rows of {t // a} seats' for a in range(2, 6) if t % a == 0 and 2 <= t // a <= 5] + [' + '.join([str(t // a)] * a) for a in range(2, 6) if t % a == 0 and 2 <= t // a <= 5]
    bad = [f'{a} rows of {b} seats' for a in range(2, 6) for b in range(2, 6) if a * b != t and abs(a * b - t) <= 3] + [' + '.join([str(b)] * a) for a in range(2, 5) for b in range(2, 6) if a * b != t and abs(a * b - t) <= 2]
    g, b = pick(r, good, bad, k)
    return ('oe4_select_rooms', f'Select ALL that show a room with {t} seats.', g, b, ['Add the seats in each row.'])


@sel(PV, 1)
def s_pv1(r, L, k):
    t = r.randint(2, 9) * 100
    good = [f'{t // 10} tens', f'{t // 100} hundreds', f'{t // 100 - 1} hundreds and 10 tens', f'{t // 100} hundreds and 0 tens']
    bad = [f'{t // 100} tens', f'{t // 10} hundreds', f'{t // 100 + 1} hundreds', f'{t // 10 + 1} tens', f'{t // 100} hundreds and 10 tens']
    g, bb = pick(r, good, bad, k)
    return ('pv1_select_same_number', f'Select ALL the ways to make {t}.', g, bb, [f'{t} is {t // 100} hundreds, which is {t // 10} tens.'])


@sel(PV, 2)
def s_pv2(r, L, k):
    h, t, o = r.randint(1, 8), r.randint(1, 8), r.randint(1, 8); v = h * 100 + t * 10 + o
    good = [f'{h} hundreds, {t} tens, {o} ones', f'{h} hundreds, {t - 1} tens, {o + 10} ones', f'{h - 1} hundreds, {t + 10} tens, {o} ones', f'{h * 10 + t} tens, {o} ones']
    bad = [f'{t} hundreds, {h} tens, {o} ones', f'{h} hundreds, {o} tens, {t} ones', f'{h} hundreds, {t + 1} tens, {o} ones', f'{h} hundreds, {t} tens, {o + 1} ones', f'{h + t + o} ones']
    g, bb = pick(r, [x for x in good if '0 hundreds' not in x or h > 1], [x for x in bad if x not in good], k)
    return ('pv2_select_ways_to_make', f'Select ALL the ways to make {v}.', g, bb, [f'Find the value of each choice and look for {v}.'])


@sel(PV, 3)
def s_pv3(r, L, k):
    good = [n(x * 100) for x in range(1, 11)]; bad = [n(x * 100 + d) for x in range(1, 9) for d in (10, 50)]
    g, b = pick(r, good, bad, k)
    return ('pv3_select_hundreds', 'Select ALL the numbers you say when you count by hundreds from 100.', g, b, ['Counting by hundreds: 100, 200, 300, ...'])


@sel(PV, 4)
def s_pv4(r, L, k):
    h, t, o = r.randint(1, 9), r.randint(1, 9), r.randint(1, 9); v = h * 100 + t * 10 + o
    good = [f'{h * 100} + {t * 10} + {o}', f'{o} + {t * 10} + {h * 100}', f'{h * 100} + {t * 10 + o}', f'{h * 100 + t * 10} + {o}']
    bad = [f'{h} + {t} + {o}', f'{h * 100} + {t} + {o}', f'{h * 10} + {t * 10} + {o}', f'{h * 100} + {o * 10} + {t}', f'{t * 100} + {h * 10} + {o}']
    g, bb = pick(r, good, [x for x in bad if x not in good and eval(x) != v], k)
    return ('pv4_select_expanded', f'Select ALL that equal {v}.', g, bb, [f'{v} = {h * 100} + {t * 10} + {o}.'])


@sel(SH, 1)
def s_sh1(r, L, k):
    sides = r.choice([3, 4, 5, 6]); names = {3: ['triangle'], 4: ['square', 'rectangle', 'rhombus', 'trapezoid', 'quadrilateral'], 5: ['pentagon'], 6: ['hexagon']}
    good = names[sides] + ([f'any shape with {sides} angles'] if sides != 4 else []) + ([f'a closed shape with {sides} sides'] if sides != 4 else [])
    bad = [x for kk, v in names.items() if kk != sides for x in v]
    g, b = pick(r, good, bad, k)
    return ('sh1_select_sides', f'Select ALL the shapes that have {sides} sides.', g, b, ['Count the sides of each shape.'])


@sel(SH, 2)
def s_sh2(r, L, k):
    good = ['a square', 'a rectangle', 'a rhombus', 'a trapezoid', 'a quadrilateral']; bad = ['a triangle', 'a pentagon', 'a hexagon', 'a circle', 'an octagon']
    g, b = pick(r, good, bad, k)
    return ('sh2_select_four_angles', 'Select ALL the shapes you could draw with exactly 4 angles.', g, b, ['A shape with 4 angles has 4 sides: a quadrilateral.'])


@sel(SH, 3)
def s_sh3(r, L, k):
    good = ['6 faces', '12 edges', '8 vertices', 'square faces', 'all faces the same size']; bad = ['4 faces', '8 edges', '6 vertices', 'triangle faces', 'a curved face']
    g, b = pick(r, good, bad, k)
    return ('sh3_select_cube', 'Select ALL that are true about a cube.', g, b, ['A cube has 6 square faces, 12 edges and 8 vertices.'])


@sel(SH, 4)
def s_sh4(r, L, k):
    t = r.choice([12, 24] if k == 4 else [12, 16, 18, 20, 24]); good = [f'{a} rows of {t // a} squares' for a in range(2, 9) if t % a == 0 and t // a <= 8]
    bad = [f'{a} rows of {b} squares' for a in range(2, 9) for b in range(2, 9) if a * b != t and abs(a * b - t) <= 3]
    g, b = pick(r, good, bad, k)
    return ('sh4_select_rectangle_squares', f'Select ALL the rectangles that are split into {t} same-size squares.', g, b, ['Add the squares in each row.'])


@sel(SH, 5)
def s_sh5(r, L, k):
    name, m, one = r.choice([('halves', 2, 'one half'), ('thirds', 3, 'one third'), ('fourths', 4, 'one fourth')])
    good = [f'there are {m} equal shares', f'{m} {name} make the whole', f'each share is {one}', 'the shares are the same size']
    bad = [f'there are {m + 1} equal shares', f'{m} {name} make half the whole', 'the shares can be different sizes', f'each share is {"one half" if m != 2 else "one third"}', f'{m - 1} {name} make the whole']
    g, b = pick(r, good, bad, k)
    return ('sh5_select_shares', f'A circle is cut into {name}. Select ALL that are true.', g, b, [f'{name.capitalize()} are {m} equal shares of the whole.'])


@sel(SH, 6)
def s_sh6(r, L, k):
    good = ['one half of a pizza is bigger than one fourth of the same pizza', 'two halves make one whole', 'three thirds make one whole', 'four fourths make one whole',
            'one third of a pizza is bigger than one fourth of the same pizza']
    bad = ['one fourth is bigger than one half of the same whole', 'three halves make one whole', 'two fourths make one whole', 'more shares means bigger shares', 'one third is smaller than one fourth of the same whole']
    g, b = pick(r, good, bad, k)
    return ('sh6_select_true_shares', 'Select ALL the true statements about equal shares.', g, b, ['More equal shares of the same whole means each share is smaller.'])


@sel(TM, 1)
def s_tm1(r, L, k):
    h = r.randint(1, 11); m0 = r.randint(1, 8) * 5; t0 = h * 60 + m0
    good = [tm(t0 + d) for d in (5, 10, 15, 20, 25)]; bad = [tm(t0 - d) for d in (5, 10, 15)] + [tm(t0 + d) for d in (35, 40, 45)]
    g, b = pick(r, good, bad, k)
    return ('tm1_select_within_half_hour', f'It is {tm(t0)}. Select ALL the times that are later but less than 30 minutes away.', g, b, ['Count on by 5s from the time shown.'])


@sel(TM, 2)
def s_tm2(r, L, k):
    good = ['eating breakfast', 'waking up for school', 'the morning bus ride', 'brushing teeth before school', 'morning recess']
    bad = ['eating dinner', 'watching the sunset', 'going to bed', 'after-school soccer', 'reading a bedtime story']
    g, b = pick(r, good, bad, k)
    return ('tm2_select_am', 'Select ALL the things that usually happen in the AM.', g, b, ['AM is from midnight to noon: the morning.'])


@sel(TM, 3)
def s_tm3(r, L, k):
    t = r.choice([30, 35, 40, 45, 50, 55, 60, 65, 70, 75])
    combos = []
    for q in range(0, 4):
        for d in range(0, 8):
            for ni in range(0, 4):
                v = 25 * q + 10 * d + 5 * ni
                if v and q + d + ni <= 6:
                    combos.append((v, ', '.join(x for x in [f'{q} quarter{"s" if q > 1 else ""}' if q else '', f'{d} dime{"s" if d > 1 else ""}' if d else '', f'{ni} nickel{"s" if ni > 1 else ""}' if ni else ''] if x)))
    g, b = pick(r, [c for v, c in combos if v == t], [c for v, c in combos if v != t and abs(v - t) <= 15], k)
    return ('tm3_select_coins_make', f'Select ALL the groups of coins that make {t}¢.', g, b, ['Quarters are 25¢, dimes 10¢ and nickels 5¢. Count each group.'])


@sel(TM, 4)
def s_tm4(r, L, k):
    t = r.choice([15, 17, 20, 25]); good, bad = [], []
    for ten in range(0, 4):
        for five in range(0, 6):
            for one in range(0, 8):
                v = 10 * ten + 5 * five + one
                txt = ', '.join(x for x in [f'{ten} $10 bill{"s" if ten > 1 else ""}' if ten else '', f'{five} $5 bill{"s" if five > 1 else ""}' if five else '', f'{one} $1 bill{"s" if one > 1 else ""}' if one else ''] if x)
                if txt and ten + five + one <= 8:
                    (good if v == t else bad if abs(v - t) <= 5 else []).append(txt)
    g, b = pick(r, good, bad, k)
    return ('tm4_select_bills_make', f'Select ALL the groups of bills that make ${t}.', g, b, ['Count each group of bills.'])


@sel(TM, 5)
def s_tm5(r, L, k):
    have = r.choice([50, 60, 75, 80, 90]); items = [10, 15, 20, 25, 30, 35, 40, 45]
    good, bad = [], []
    for i in range(len(items)):
        for j in range(i + 1, len(items)):
            txt = f'a {items[i]}¢ toy and a {items[j]}¢ toy'
            (good if items[i] + items[j] <= have else bad).append(txt)
    g, b = pick(r, good, bad, k)
    return ('tm5_select_can_buy', f'Ava has {have}¢. Select ALL the pairs of toys she can buy.', g, b, [f'Add the two prices; the total must be {have}¢ or less.'])


@sel(WP, 1)
def s_wp1(r, L, k):
    t = r.randint(20, 60); good, bad = [], []
    for _ in range(40):
        a = r.randint(10, 50); b = t - a
        if b > 0: good.append(f'{a} birds, then {b} more come')
        a2 = r.randint(t + 5, 90); good.append(f'{a2} birds, then {a2 - t} fly away')
        bad.append(f'{a} birds, then {abs(b) + r.choice([1, 5, 10])} more come')
    g, bb = pick(r, good, bad, k)
    return ('wp1_select_stories_end', f'Select ALL the stories that end with {t} birds.', g, bb, ['Add for more coming; subtract for flying away.'])


@sel(WP, 2)
def s_wp2(r, L, k):
    t = r.randint(30, 80); g, b = sums_equal(r, t, 10, t - 10, k)
    return ('wp2_select_parts_whole', f'A club has {t} children. Select ALL the pairs (girls + boys) that could be right.', g, b, [f'The two parts must add to {t}.'])


@sel(WP, 3)
def s_wp3(r, L, k):
    d = r.randint(5, 20); good = [f'Eli {a}, Lena {a + d}' for a in range(10, 60, 7)]; bad = [f'Eli {a}, Lena {a + d + r.choice([1, -1, 10])}' for a in range(12, 60, 7)]
    g, b = pick(r, good, bad, k)
    return ('wp3_select_compare', f'Lena has {d} more cards than Eli. Select ALL the pairs that could be right.', g, b, [f'Lena’s number minus Eli’s number must be {d}.'])


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
                r = random.Random(f'g2-sel|{q["id"]}')
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
