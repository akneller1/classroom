"""Question families for the 2nd Grade Math audit (2026-11-19).

S[skill](r) -> a Standard item: the skill's Support task with one added step (#7).
A[skill](r) -> an Advanced item: two steps, work backward or compare (#1, #19).
Each returns (family, prompt, answer, steps, wrong_answers). Numbers stay inside Grade 2 limits: facts within 20,
add and subtract within 100 (word problems) and 1,000 (with models), place value to 1,000, skip counting by 5s, 10s
and 100s, whole-number lengths in inches, feet, centimeters and meters, time to five minutes, coins under $1 and
whole-dollar bills, arrays up to 5 by 5. Every answer is computed here and recomputed independently by
scripts/test-grade2-audit.cjs."""
NAMES = ['Ava', 'Ben', 'Cora', 'Dev', 'Eli', 'Gabi', 'Hugo', 'Isla', 'Jada', 'Kai', 'Lena', 'Max', 'Nia', 'Omar', 'Pia', 'Raj', 'Sam', 'Tess', 'Uma', 'Zoe']
SINGULAR = {'inches': 'inch', 'feet': 'foot', 'centimeters': 'centimeter', 'meters': 'meter', 'stickers': 'sticker', 'shells': 'shell', 'cards': 'card',
            'books': 'book', 'apples': 'apple', 'pencils': 'pencil', 'beads': 'bead', 'marbles': 'marble', 'children': 'child', 'people': 'person',
            'seats': 'seat', 'pages': 'page', 'cubes': 'cube', 'squares': 'square', 'steps': 'step', 'blocks': 'block', 'minutes': 'minute', 'plants': 'plant', 'socks': 'sock', 'desks': 'desk', 'tickets': 'ticket', 'eggs': 'egg', 'dots': 'dot',
            'cans': 'can', 'votes': 'vote', 'pets': 'pet', 'students': 'student', 'balloons': 'balloon', 'crayons': 'crayon', 'points': 'point', 'hours': 'hour', 'units': 'unit'}


def qty(x, unit):
    return f'{x} {SINGULAR.get(unit, unit) if str(x) == "1" else unit}'


def n(x):
    return f'{x:,}'


def tm(m):
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


AF, AH, WP, PV, CC, AT, OE, ML, LN, TM, GD, SH = ('add-subtract-20', 'add-subtract-100', 'word-problems-100', 'place-value-1000', 'count-compare-1000',
                                                  'add-subtract-1000', 'odd-even-arrays', 'measuring-length', 'length-number-line', 'time-money',
                                                  'graphs-data', 'shapes-equal-shares')


def sk(u, i):
    return f'{u}-skill-{i:02d}'


THINGS = ['stickers', 'shells', 'cards', 'marbles', 'beads', 'pencils']

# =============================================================== add and subtract within 20


@std(sk(AF, 1))
def af1_s(r):
    a, b, c = r.randint(2, 9), r.randint(2, 9), r.randint(1, 5); need(a + b + c <= 20)
    return ('af1_add_then_more', f'Add {a} + {b}. Then add {c} more.', n(a + b + c), [f'{a} + {b} = {a + b}.', f'{a + b} + {c} = {a + b + c}.'],
            [n(a + b), n(a + b + c + 1), n(a + c)])


@adv(sk(AF, 1))
def af1_a(r):
    a, b = r.randint(5, 9), r.randint(5, 9); need(a + b > 11); t = r.choice(THINGS); p, q = r.sample(NAMES, 2)
    return ('af1_two_kids_total_compare', f'{p} has {a} {t}. {q} has {b} {t}. They put them together, then give away {a + b - 10}. How many are left?',
            qty(10, t), [f'{a} + {b} = {a + b}.', f'{a + b} − {a + b - 10} = 10.'], [qty(a + b, t), qty(a + b - 10, t), qty(9, t)])


@std(sk(AF, 2))
def af2_s(r):
    a, b, c = r.randint(11, 18), r.randint(2, 9), r.randint(1, 4); need(a - b - c >= 0)
    return ('af2_subtract_twice', f'Subtract {a} − {b}. Then take away {c} more.', n(a - b - c), [f'{a} − {b} = {a - b}.', f'{a - b} − {c} = {a - b - c}.'],
            [n(a - b), n(a - b + c), n(a - c)])


@adv(sk(AF, 2))
def af2_a(r):
    a, b = r.randint(11, 18), r.randint(3, 9); need(a - b >= 2); p = r.choice(NAMES)
    return ('af2_how_many_more_after', f'{p} had {a} crayons and gave {b} to a friend. How many more crayons does {p} need to have 20?',
            qty(20 - (a - b), 'crayons'), [f'{a} − {b} = {a - b} crayons left.', f'{a - b} + {20 - (a - b)} = 20, so {p} needs {20 - (a - b)} more.'],
            [qty(a - b, 'crayons'), qty(20 - a, 'crayons'), qty(20 - b, 'crayons')])


@std(sk(AF, 3))
def af3_s(r):
    a, b = r.randint(3, 9), r.randint(3, 9)
    return ('af3_fact_family_two', f'{a} + {b} = {a + b}. What is {a + b} − {a}? What is {a + b} − {b}?', f'{b}; {a}',
            [f'{a + b} − {a} = {b}, because {a} + {b} = {a + b}.', f'{a + b} − {b} = {a}.'], [f'{a}; {b}', f'{a + b}; {a}', f'{b}; {b}'])


@adv(sk(AF, 3))
def af3_a(r):
    a, b = r.randint(4, 9), r.randint(4, 9); need(a != b)
    return ('af3_which_not_in_family', f'Which equation is NOT in the fact family for {a}, {b} and {a + b}?', f'{a} − {b} = {a + b}' if a > b else f'{b} − {a} = {a + b}',
            [f'The family is {a} + {b} = {a + b}, {b} + {a} = {a + b}, {a + b} − {a} = {b} and {a + b} − {b} = {a}.', 'A subtraction fact starts with the whole.'],
            [f'{a + b} − {a} = {b}', f'{b} + {a} = {a + b}', f'{a + b} − {b} = {a}'])


@std(sk(AF, 4))
def af4_s(r):
    a, b, c = r.randint(2, 9), r.randint(2, 9), r.randint(2, 9); need(a + b - c > 0 and a + b <= 20)
    return ('af4_missing_both_sides', f'What number makes the equation true? {a} + {b} = {c} + ___', n(a + b - c), [f'{a} + {b} = {a + b}.', f'{c} + {a + b - c} = {a + b}.'],
            [n(a + b), n(a + b + c), n(c - a if c > a else a + b - c + 1)])


@adv(sk(AF, 4))
def af4_a(r):
    a, b, c = r.randint(11, 19), r.randint(2, 9), r.randint(2, 9); need(a - b - c > 0)
    return ('af4_missing_subtract_both', f'What number makes the equation true? {a} − {b} = {c} + ___', n(a - b - c), [f'{a} − {b} = {a - b}.', f'{c} + {a - b - c} = {a - b}.'],
            [n(a - b), n(a - b + c), n(a - c)])

# =============================================================== add and subtract within 100


@std(sk(AH, 1))
def ah1_s(r):
    a, b, c = r.randint(15, 45), r.randint(15, 40), r.randint(2, 9)
    return ('ah1_add_then_more', f'Add {a} + {b}. Then add {c}.', n(a + b + c), [f'{a} + {b} = {a + b}.', f'{a + b} + {c} = {a + b + c}.'], [n(a + b), n(a + b + c + 10), n(a + c)])


@adv(sk(AH, 1))
def ah1_a(r):
    a, b = r.randint(25, 60), r.randint(15, 39); need(a + b <= 100); p, q = r.sample(NAMES, 2)
    return ('ah1_sum_then_to_100', f'{p} scored {a} points and {q} scored {b} points. How many more points do they need together to reach 100?',
            qty(100 - a - b, 'points'), [f'{a} + {b} = {a + b}.', f'100 − {a + b} = {100 - a - b}.'], [qty(a + b, 'points'), qty(100 - a, 'points'), qty(100 - a - b + 10, 'points')])


@std(sk(AH, 2))
def ah2_s(r):
    a, b, c = r.randint(50, 99), r.randint(11, 39), r.randint(2, 9); need(a - b - c > 0)
    return ('ah2_subtract_then_more', f'Subtract {a} − {b}. Then subtract {c}.', n(a - b - c), [f'{a} − {b} = {a - b}.', f'{a - b} − {c} = {a - b - c}.'], [n(a - b), n(a - b + c), n(a - c)])


@adv(sk(AH, 2))
def ah2_a(r):
    a, b, c = r.randint(60, 99), r.randint(12, 30), r.randint(12, 30); need(a - b - c > 0)
    return ('ah2_two_take_aways', f'A box has {a} crayons. {r.choice(NAMES)} takes {b} and {r.choice(NAMES)} takes {c}. How many crayons are left?',
            qty(a - b - c, 'crayons'), [f'{b} + {c} = {b + c} taken.', f'{a} − {b + c} = {a - b - c}.'], [qty(a - b, 'crayons'), qty(a - b + c, 'crayons'), qty(b + c, 'crayons')])


@std(sk(AH, 3))
def ah3_s(r):
    a, b = r.randint(15, 60), r.randint(15, 39); need(a + b <= 99)
    return ('ah3_missing_then_check', f'What number makes the equation true? {a} + ___ = {a + b}. Then add the missing number to {a} to check.', n(b),
            [f'{a + b} − {a} = {b}.', f'{a} + {b} = {a + b}. It checks.'], [n(a + b), n(b + 10), n(b - 1)])


@adv(sk(AH, 3))
def ah3_a(r):
    a, b = r.randint(30, 90), r.randint(11, 29); need(a - b > 10)
    return ('ah3_missing_start', f'What number makes the equation true? ___ − {b} = {a - b}', n(a), [f'Think addition: {a - b} + {b} = {a}.', f'{a} − {b} = {a - b}.'],
            [n(a - 2 * b if a > 2 * b else a + 10), n(a - b), n(a + 10)])


@std(sk(AH, 4))
def ah4_s(r):
    a, b, c = r.randint(11, 30), r.randint(11, 30), r.randint(11, 30); x = r.randint(2, 9)
    return ('ah4_three_then_take', f'Add {a} + {b} + {c}. Then subtract {x}.', n(a + b + c - x), [f'{a} + {b} + {c} = {a + b + c}.', f'{a + b + c} − {x} = {a + b + c - x}.'],
            [n(a + b + c), n(a + b - x), n(a + b + c + x)])


@adv(sk(AH, 4))
def ah4_a(r):
    a, b, c, d = (r.randint(11, 30) for _ in range(4)); need(a + b + c + d <= 100)
    return ('ah4_four_addends_story', f'A class collected {a} cans on Monday, {b} on Tuesday, {c} on Wednesday and {d} on Thursday. How many cans is that in all?',
            qty(a + b + c + d, 'cans'), [f'{a} + {b} = {a + b}; {c} + {d} = {c + d}.', f'{a + b} + {c + d} = {a + b + c + d} cans.'],
            [qty(a + b + c, 'cans'), qty(a + b + c + d - 10, 'cans'), qty(a + b + c + d + 10, 'cans')])


@std(sk(AH, 5))
def ah5_s(r):
    a, b = r.randint(21, 58), r.randint(11, 39); need(a + b <= 99 and b % 10)
    t = b // 10 * 10; o = b % 10
    return ('ah5_break_apart', f'Add {a} + {b} by adding {t} first, then {o}. What is {a} + {t}, and what is the sum?', f'{a + t}; {a + b}',
            [f'{a} + {t} = {a + t}.', f'{a + t} + {o} = {a + b}.'], [f'{a + o}; {a + b}', f'{a + t}; {a + b + 1}', f'{a + 10}; {a + b}'])


@adv(sk(AH, 5))
def ah5_a(r):
    a, b = r.randint(21, 69), r.randint(18, 29); need(a + b <= 99 and b % 10 >= 8)
    up = 10 - b % 10
    return ('ah5_compensate', f'To find {a} + {b}, {r.choice(NAMES)} adds {a - up} + {b + up} instead. Is the sum the same? What is it?', f'yes; {a + b}',
            [f'{up} was moved from {a} to {b}, so the total does not change.', f'{a - up} + {b + up} = {a + b}.'], [f'no; {a + b + up}', f'yes; {a + b + up}', f'no; {a - up + b}'])

# =============================================================== word problems within 100


@std(sk(WP, 2))
def wp2_s(r):
    a, b, c = r.randint(15, 40), r.randint(15, 40), r.randint(2, 9)
    return ('wp2_groups_then_more', f'There are {a} boys and {b} girls in the club. Then {c} more children join. How many children are in the club now?',
            qty(a + b + c, 'children'), [f'{a} + {b} = {a + b}.', f'{a + b} + {c} = {a + b + c}.'], [qty(a + b, 'children'), qty(a + b - c, 'children'), qty(a + c, 'children')])


@adv(sk(WP, 2))
def wp2_a(r):
    tot, a = r.randint(40, 99), r.randint(11, 35); x = r.randint(5, 15); need(tot - a - x > 0)
    return ('wp2_part_unknown_two_step', f'A basket has {tot} apples. {a} are red, {x} are yellow, and the rest are green. How many apples are green?',
            qty(tot - a - x, 'apples'), [f'{a} + {x} = {a + x} red and yellow.', f'{tot} − {a + x} = {tot - a - x} green.'], [qty(tot - a, 'apples'), qty(a + x, 'apples'), qty(tot - x, 'apples')])


@std(sk(WP, 4))
def wp4_s(r):
    a, b, c = r.randint(20, 50), r.randint(10, 30), r.randint(5, 20); need(a + b - c > 0)
    return ('wp4_on_then_off', f'A bus had {a} people. At the first stop, {b} people got on. At the next stop, {c} people got off. How many people are on the bus now?',
            qty(a + b - c, 'people'), [f'{a} + {b} = {a + b}.', f'{a + b} − {c} = {a + b - c}.'], [qty(a + b, 'people'), qty(a - b + c if a > b else a + c, 'people'), qty(a + b + c, 'people')])


@adv(sk(WP, 4))
def wp4_a(r):
    start, got, now = r.randint(20, 50), r.randint(10, 30), None; spent = r.randint(5, 25); now = start + got - spent; need(now > 0)
    p = r.choice(NAMES)
    return ('wp4_start_unknown', f'{p} had some stickers. {p} got {got} more and then gave away {spent}. Now {p} has {now} stickers. How many stickers did {p} have at first?',
            qty(start, 'stickers'), [f'Work backward: {now} + {spent} = {now + spent}.', f'{now + spent} − {got} = {start}.'], [qty(now, 'stickers'), qty(now + got - spent, 'stickers'), qty(now + spent, 'stickers')])

# =============================================================== place value to 1,000


@std(sk(PV, 1))
def pv1_s(r):
    t = r.randint(11, 99)
    return ('pv1_tens_then_hundreds', f'How many tens are in {t * 10}? How many whole hundreds?', f'{t}; {t // 10}',
            [f'{t * 10} is {t} tens.', f'10 tens make 1 hundred, so {t} tens is {t // 10} whole hundreds.'], [f'{t // 10}; {t}', f'{t}; {t}', f'{t * 10}; {t // 10}'])


@adv(sk(PV, 1))
def pv1_a(r):
    h, t = r.randint(1, 8), r.randint(10, 19); v = h * 100 + t * 10
    return ('pv1_regroup_tens', f'A number has {h} hundreds and {t} tens. What is the number?', n(v), [f'{t} tens = 1 hundred and {t - 10} tens.', f'{h + 1} hundreds and {t - 10} tens = {v}.'],
            [n(h * 100 + t), n((h + t) * 10), n(v + 100)])


@std(sk(PV, 2))
def pv2_s(r):
    h, t, o = r.randint(1, 9), r.randint(0, 9), r.randint(0, 9); x = r.choice([10, 100])
    v = h * 100 + t * 10 + o; need(v + x <= 999)
    return ('pv2_build_then_more', f'Build the number with {h} hundreds, {t} tens and {o} ones. Then add {x}. What number do you get?', n(v + x),
            [f'{h} hundreds, {t} tens and {o} ones is {v}.', f'{v} + {x} = {v + x}.'], [n(v), n(v + (110 - x)), n(h + t + o + x)])


@adv(sk(PV, 2))
def pv2_a(r):
    h, t, o = r.randint(2, 9), r.randint(1, 9), r.randint(10, 19); v = h * 100 + t * 10 + o; need(v <= 999)
    return ('pv2_regroup_ones', f'A number has {h} hundreds, {t} tens and {o} ones. What is the number?', n(v),
            [f'{o} ones = 1 ten and {o - 10} ones.', f'{h} hundreds, {t + 1} tens and {o - 10} ones = {v}.'], [n(h * 100 + t * 10 + o % 10), n(v + 90), n(v - 10)])


@std(sk(PV, 3))
def pv3_s(r):
    s = r.randint(1, 5) * 100; k = r.randint(3, 4)
    return ('pv3_count_hundreds_then', f'Start at {s} and count by hundreds {k} times. Then count back 10. Where do you end?', n(s + 100 * k - 10),
            [f'{s} + {k} hundreds = {s + 100 * k}.', f'{s + 100 * k} − 10 = {s + 100 * k - 10}.'], [n(s + 100 * k), n(s + 10 * k - 10), n(s + 100 * k + 10)])


@adv(sk(PV, 3))
def pv3_a(r):
    a = r.randint(2, 6); b = r.randint(a + 2, 9)
    return ('pv3_hundreds_between', f'How many hundreds do you count to get from {a * 100} to {b * 100}?', n(b - a), [f'Count {a * 100}, {(a + 1) * 100}, ... {b * 100}.', f'That is {b - a} hundreds.'],
            [n(b - a + 1), n(b), n((b - a) * 100)])


@std(sk(PV, 4))
def pv4_s(r):
    h, t, o = r.randint(1, 9), r.randint(1, 9), r.randint(1, 9); need(len({h, t, o}) == 3); v = h * 100 + t * 10 + o
    return ('pv4_expanded_then_value', f'Write {v} in expanded form. What is the value of the {t} in {v}?', n(t * 10),
            [f'{v} = {h * 100} + {t * 10} + {o}.', f'The {t} is in the tens place, so its value is {t * 10}.'], [n(t), n(t * 100), n(h * 100)])


@adv(sk(PV, 4))
def pv4_a(r):
    h, t, o = r.randint(1, 9), r.randint(0, 9), r.randint(1, 9); v = h * 100 + t * 10 + o
    parts = [f'{o}', f'{h * 100}'] + ([f'{t * 10}'] if t else [])
    r.shuffle(parts)
    return ('pv4_mixed_order_expanded', f'What number is {" + ".join(parts)}?', n(v), ['Put the parts in place-value order: hundreds, tens, ones.', f'{h * 100} + {t * 10} + {o} = {v}.'],
            [n(v + 90 if v + 90 <= 999 else v - 90), n(h * 100 + o * 10 + t), n(h + t + o)])

# =============================================================== count and compare to 1,000


@std(sk(CC, 1))
def cc1_s(r):
    a = r.randint(100, 980); k = r.randint(2, 5)
    return ('cc1_count_on_k', f'Start at {a}. Count on {k} more by ones. What number do you say last?', n(a + k), [f'{a} + {k} = {a + k}.', f'You say {", ".join(str(a + i) for i in range(1, k + 1))}.'],
            [n(a + k - 1), n(a + k + 1), n(a + 10 * k)])


@adv(sk(CC, 1))
def cc1_a(r):
    a = r.randint(1, 9) * 100 - r.randint(1, 3); k = r.randint(4, 8); need(a + k <= 999)
    return ('cc1_count_over_hundred', f'Count on {k} by ones from {a}. What number do you end on?', n(a + k), [f'Crossing a hundred: {a}, {", ".join(str(a + i) for i in range(1, k + 1))}.', f'You end on {a + k}.'],
            [n(a + k - 100 if a + k - 100 > 0 else a + k + 1), n(a + k + 1), n(a + k - 1)])


@std(sk(CC, 2))
def cc2_s(r):
    step = r.choice([5, 10, 100]); a = r.randint(1, 15) * step if step != 100 else r.randint(1, 4) * 100; k = r.randint(3, 5)
    need(a + step * k <= 1000)
    return ('cc2_skip_k_times', f'Skip count by {step}s {k} times, starting at {a}. What number do you end on?', n(a + step * k),
            [f'Each jump adds {step}.', f'{a} + {k} × {step} = {a + step * k}.'], [n(a + step * (k - 1)), n(a + step * (k + 1)), n(a + k)])


@adv(sk(CC, 2))
def cc2_a(r):
    step = r.choice([5, 10]); a = r.randint(2, 20) * step; b = a + step * r.randint(4, 9)
    return ('cc2_jumps_between', f'How many jumps of {step} does it take to skip count from {a} to {b}?', n((b - a) // step), [f'{b} − {a} = {b - a}.', f'{b - a} is {(b - a) // step} jumps of {step}.'],
            [n((b - a) // step + 1), n(b - a), n((b - a) // step - 1)])


@std(sk(CC, 3))
def cc3_s(r):
    xs = r.sample(range(101, 999), 3)
    return ('cc3_order_three', f'Order from least to greatest: {", ".join(map(str, xs))}', ', '.join(map(str, sorted(xs))),
            ['Compare hundreds, then tens, then ones.', ', '.join(map(str, sorted(xs))) + '.'], [', '.join(map(str, sorted(xs, reverse=True))), ', '.join(map(str, xs)), ', '.join(map(str, [sorted(xs)[1], sorted(xs)[0], sorted(xs)[2]]))])


@adv(sk(CC, 3))
def cc3_a(r):
    h = r.randint(2, 8); t = r.randint(1, 8); a, b = h * 100 + t * 10 + r.randint(0, 9), h * 100 + (t + 1) * 10 + r.randint(0, 9)
    x = r.randint(10, 40)
    return ('cc3_compare_after_change', f'Compare {a} + {x} ___ {b}. Write >, =, or <.', '>' if a + x > b else '<' if a + x < b else '=',
            [f'{a} + {x} = {a + x}.', f'Compare {a + x} and {b}.'], [c for c in '<>=' if c != ('>' if a + x > b else '<' if a + x < b else '=')])


@adv(sk(CC, 3))
def cc3_a2(r):
    h = r.randint(2, 9); xs = r.sample(range(h * 100, h * 100 + 100), 4); which = r.choice(['greatest', 'least'])
    ans = max(xs) if which == 'greatest' else min(xs)
    return ('cc3_greatest_same_hundreds', f'Which number is the {which}: {", ".join(map(str, xs))}?', str(ans),
            ['All have the same hundreds, so compare the tens, then the ones.', f'The {which} is {ans}.'], [str(x) for x in xs if x != ans])


@std(sk(CC, 4))
def cc4_s(r):
    a = r.randint(120, 880); x, y = r.choice([(100, 10), (10, 100)])
    return ('cc4_two_changes', f'Start at {a}. Add {x}, then subtract {y}. What number do you get?', n(a + x - y), [f'{a} + {x} = {a + x}.', f'{a + x} − {y} = {a + x - y}.'],
            [n(a + x), n(a - y), n(a + x + y)])


@adv(sk(CC, 4))
def cc4_a(r):
    a = r.randint(150, 850); k = r.randint(2, 4); x = r.choice([10, 100]); need(a + k * x <= 999)
    return ('cc4_backward_change', f'A number is {k} × {x} more than another number. The bigger number is {a + k * x}. What is the other number?', n(a),
            [f'{k} × {x} = {k * x}.', f'{a + k * x} − {k * x} = {a}.'], [n(a + 2 * k * x), n(a + k * x - x), n(a + k)])

# =============================================================== add and subtract within 1,000


@std(sk(AT, 1))
def at1_s(r):
    a, h, t, o = r.randint(110, 500), r.randint(1, 3), r.randint(1, 5), r.randint(1, 9)
    return ('at1_hundreds_tens_ones_jumps', f'Start at {a}. Add {h * 100}, then add {t * 10}, then add {o}. Then add 10 more. Where do you end?', n(a + h * 100 + t * 10 + o + 10),
            [f'{a} + {h * 100} + {t * 10} + {o} = {a + h * 100 + t * 10 + o}.', f'Plus 10 more: {a + h * 100 + t * 10 + o + 10}.'],
            [n(a + h * 100 + t * 10 + o), n(a + h * 100 + o + 10), n(a + h + t + o + 10)])


@adv(sk(AT, 1))
def at1_a(r):
    a, b, c = r.randint(100, 400), r.randint(100, 300), r.randint(100, 200); need(a + b + c <= 999)
    return ('at1_three_three_digit', f'Add {a} + {b} + {c}.', n(a + b + c), [f'{a} + {b} = {a + b}.', f'{a + b} + {c} = {a + b + c}.'], [n(a + b), n(a + b + c + 100), n(a + b + c - 10)])


@std(sk(AT, 2))
def at2_s(r):
    a, b = r.randint(150, 480), r.randint(150, 450); x = r.randint(10, 50); need(a + b + x <= 999 and (a % 10 + b % 10 >= 10))
    return ('at2_regroup_then_more', f'A store sold {a} pencils in May and {b} pencils in June. In July it sold {x} pencils. How many pencils did it sell in the three months?',
            qty(a + b + x, 'pencils'), [f'{a} + {b} = {a + b} (make a new ten).', f'{a + b} + {x} = {a + b + x}.'], [qty(a + b, 'pencils'), qty(a + b + x - 10, 'pencils'), qty(a + b - x, 'pencils')])


@adv(sk(AT, 2))
def at2_a(r):
    a, b = r.randint(250, 480), r.randint(250, 480); need(a + b <= 999 and a % 10 + b % 10 >= 10 and a // 10 % 10 + b // 10 % 10 >= 9)
    return ('at2_new_ten_and_hundred', f'Add {a} + {b}. How many hundreds are in the sum?', f'{(a + b) // 100}', [f'{a} + {b} = {a + b}.', f'{a + b} has {(a + b) // 100} hundreds.'],
            [f'{a // 100 + b // 100}', f'{(a + b) // 100 + 1}', f'{(a + b) // 10}'])


@std(sk(AT, 3))
def at3_s(r):
    a, b = r.randint(500, 900), r.randint(150, 450); x = r.randint(10, 90)
    return ('at3_subtract_then_add', f'Subtract {a} − {b}. Then add {x}.', n(a - b + x), [f'{a} − {b} = {a - b}.', f'{a - b} + {x} = {a - b + x}.'], [n(a - b), n(a - b - x), n(a + b + x if a + b + x < 1000 else a - b + x + 100)])


@adv(sk(AT, 3))
def at3_a(r):
    b = r.randint(150, 450); up1 = (100 - b % 100) % 100 or 100; a = r.randint(b + 150, 950)
    return ('at3_count_up_difference', f'Count up to find {a} − {b}. First count up to {b + up1}. How far is that, and what is {a} − {b}?', f'{up1}; {a - b}',
            [f'{b} + {up1} = {b + up1}.', f'From {b + up1} to {a} is {a - b - up1}; {up1} + {a - b - up1} = {a - b}.'], [f'{up1}; {a - b + 10}', f'{a - b - up1}; {a - b}', f'{up1}; {a + b - 1000 if a + b > 1000 else a - b - 100}'])


@std(sk(AT, 4))
def at4_s(r):
    a, b = r.randint(400, 999), r.randint(100, 399); need(a % 10 < b % 10); x = r.randint(10, 50)
    return ('at4_regroup_then_less', f'Subtract {a} − {b}. Then subtract {x} more.', n(a - b - x), [f'{a} − {b} = {a - b} (trade a ten for 10 ones).', f'{a - b} − {x} = {a - b - x}.'],
            [n(a - b), n(a - b + x), n(a - b - x + 10)])


@adv(sk(AT, 4))
def at4_a(r):
    a = r.choice([300, 400, 500, 600, 700, 800, 900]); b, c = r.randint(100, 250), r.randint(50, 150); need(a - b - c > 0)
    return ('at4_across_zeros_two', f'A school has {a} stickers. It gives {b} to one class and {c} to another. How many stickers are left?',
            qty(a - b - c, 'stickers'), [f'{b} + {c} = {b + c}.', f'{a} − {b + c} = {a - b - c} (regroup across the zeros).'], [qty(a - b, 'stickers'), qty(a - b - c + 100, 'stickers'), qty(b + c, 'stickers')])

# =============================================================== odd, even and arrays


@std(sk(OE, 1))
def oe1_s(r):
    a, b = r.randint(1, 10), r.randint(1, 10)
    s = a + b
    return ('oe1_sum_odd_even', f'Find {a} + {b}. Is the sum odd or even?', 'even' if s % 2 == 0 else 'odd', [f'{a} + {b} = {s}.', f'{s} {"can" if s % 2 == 0 else "cannot"} be split into two equal groups, so it is {"even" if s % 2 == 0 else "odd"}.'],
            ['odd' if s % 2 == 0 else 'even', 'both', 'neither'])


@adv(sk(OE, 1))
def oe1_a(r):
    lo = r.randint(1, 10); hi = lo + r.randint(5, 9)
    ev = sum(1 for x in range(lo, hi + 1) if x % 2 == 0)
    return ('oe1_count_even_between', f'How many even numbers are there from {lo} to {hi}?', n(ev), [f'The even numbers are {", ".join(str(x) for x in range(lo, hi + 1) if x % 2 == 0)}.', f'That is {ev}.'],
            [n(hi - lo + 1 - ev), n(ev + 1), n(hi - lo)])


@std(sk(OE, 2))
def oe2_s(r):
    d = r.randint(2, 10)
    return ('oe2_double_then_even', f'Write {2 * d} as a sum of two equal addends. What is each addend?', n(d), [f'{d} + {d} = {2 * d}.', f'Each addend is {d}, so {2 * d} is even.'],
            [n(2 * d), n(d + 1), n(d - 1)])


@adv(sk(OE, 2))
def oe2_a(r):
    d = r.randint(3, 10); x = r.choice([1, 3])
    return ('oe2_doubles_plus', f'{r.choice(NAMES)} has {d} + {d} + {x} blocks. How many blocks is that, and is it odd or even?', f'{2 * d + x}; odd',
            [f'{d} + {d} = {2 * d}, an even number.', f'{2 * d} + {x} = {2 * d + x}. Even plus odd is odd.'], [f'{2 * d + x}; even', f'{2 * d}; even', f'{d + x}; odd'])


@std(sk(OE, 3))
def oe3_s(r):
    rows, cols = r.randint(2, 5), r.randint(2, 5); x = r.randint(1, 5)
    return ('oe3_array_plus_dots', f'An array has {rows} rows of {cols} dots. {x} more dots are drawn below it. How many dots are there in all?', qty(rows * cols + x, 'dots'),
            [f'{" + ".join([str(cols)] * rows)} = {rows * cols}.', f'{rows * cols} + {x} = {rows * cols + x}.'], [qty(rows * cols, 'dots'), qty(rows + cols + x, 'dots'), qty(rows * (cols + x), 'dots')])


@adv(sk(OE, 3))
def oe3_a(r):
    a, b, c, d = r.randint(2, 5), r.randint(2, 5), r.randint(2, 5), r.randint(2, 5); need(a * b != c * d)
    return ('oe3_two_arrays_compare', f'Array A has {a} rows of {b}. Array B has {c} rows of {d}. How many more dots does the bigger array have?', n(abs(a * b - c * d)),
            [f'A: {a * b}. B: {c * d}.', f'{max(a * b, c * d)} − {min(a * b, c * d)} = {abs(a * b - c * d)}.'], [n(a * b + c * d), n(abs((a + b) - (c + d))), n(max(a * b, c * d))])


@std(sk(OE, 4))
def oe4_s(r):
    rows, cols = r.randint(2, 5), r.randint(2, 5); x = r.randint(1, rows * cols - 1)
    return ('oe4_seats_minus', f'A room has {rows} rows of seats with {cols} seats in each row. {x} children are sitting. How many seats are empty?', qty(rows * cols - x, 'seats'),
            [f'{rows} rows of {cols} is {rows * cols} seats.', f'{rows * cols} − {x} = {rows * cols - x}.'], [qty(rows * cols, 'seats'), qty(rows + cols - x if rows + cols > x else rows * cols - x + 1, 'seats'), qty(rows * cols + x, 'seats')])


@adv(sk(OE, 4))
def oe4_a(r):
    rows, cols = r.randint(2, 5), r.randint(2, 5); add = r.randint(1, 2)
    return ('oe4_add_rows', f'A garden has {rows} rows with {cols} plants in each row. {add} more {"row is" if add == 1 else "rows are"} planted the same way. How many plants are there now?',
            qty((rows + add) * cols, 'plants'), [f'{rows} + {add} = {rows + add} rows.', f'{" + ".join([str(cols)] * (rows + add))} = {(rows + add) * cols}.'],
            [qty(rows * cols, 'plants'), qty(rows * cols + add, 'plants'), qty((rows + add) * (cols + add), 'plants')])

# =============================================================== measuring length


@std(sk(ML, 3))
def ml3_s(r):
    m = r.randint(2, 9); x = r.randint(10, 90)
    return ('ml3_meters_to_cm_plus', f'A table is {m} meters long. 1 meter = 100 centimeters. A bench is {x} centimeters longer than the table. How long is the bench in centimeters?',
            qty(m * 100 + x, 'centimeters'), [f'{m} meters = {m * 100} centimeters.', f'{m * 100} + {x} = {m * 100 + x} centimeters.'], [qty(m * 100, 'centimeters'), qty(m + x, 'centimeters'), qty(m * 10 + x, 'centimeters')])


@adv(sk(ML, 3))
def ml3_a(r):
    f = r.randint(2, 6)
    return ('ml3_feet_to_inches', f'A rug is {f} feet long. 1 foot = 12 inches. How many inches long is the rug? Use repeated addition.', qty(f * 12, 'inches'),
            [f'{" + ".join(["12"] * f)}.', f'= {f * 12} inches.'], [qty(f + 12, 'inches'), qty(f * 10, 'inches'), qty(f * 12 - 12, 'inches')])


@std(sk(ML, 4))
def ml4_s(r):
    k = r.randint(4, 9); a = r.randint(2, 3)
    return ('ml4_estimate_then_compare', f'A paper clip is about 1 inch long. A pencil is about {k} paper clips long and a crayon is about {a} paper clips long. About how many inches longer is the pencil?',
            qty(k - a, 'inches'), [f'Pencil: about {k} inches. Crayon: about {a} inches.', f'{k} − {a} = {k - a} inches.'], [qty(k + a, 'inches'), qty(k, 'inches'), qty(a, 'inches')])


@adv(sk(ML, 4))
def ml4_a(r):
    s = r.randint(5, 9); k = r.randint(3, 8)
    return ('ml4_steps_two_rooms', f'One long step is about 1 meter. A hallway is about {s} steps long and a classroom is about {k} steps long. About how many meters is that in all?',
            qty(s + k, 'meters'), [f'Hallway: about {s} meters. Classroom: about {k} meters.', f'{s} + {k} = {s + k} meters.'], [qty(abs(s - k) or 1, 'meters'), qty(s * k, 'meters'), qty(s + k + 1, 'meters')])


@std(sk(ML, 5))
def ml5_s(r):
    a, b = r.randint(20, 60), r.randint(10, 40); need(a > b); u = r.choice(['inches', 'centimeters'])
    return ('ml5_longer_then_double', f'A ribbon is {a} {u} long. A string is {b} {u} long. How much longer is the ribbon? Then how long are the ribbon and string together?',
            f'{a - b} {u}; {a + b} {u}', [f'{a} − {b} = {a - b}.', f'{a} + {b} = {a + b}.'], [f'{a + b} {u}; {a - b} {u}', f'{a - b} {u}; {a - b + 10} {u}', f'{b} {u}; {a + b} {u}'])


@adv(sk(ML, 5))
def ml5_a(r):
    a, b, c = r.randint(30, 70), r.randint(10, 30), r.randint(10, 30); need(a - b - c > 0)
    return ('ml5_cut_two_pieces', f'A rope is {a} inches long. {r.choice(NAMES)} cuts off {b} inches and then {c} inches. How long is the rope now?', qty(a - b - c, 'inches'),
            [f'{b} + {c} = {b + c} inches cut off.', f'{a} − {b + c} = {a - b - c} inches.'], [qty(a - b, 'inches'), qty(b + c, 'inches'), qty(a - b - c + 10, 'inches')])

# =============================================================== length and the number line


@std(sk(LN, 1))
def ln1_s(r):
    a, b, c = r.randint(10, 35), r.randint(10, 35), r.randint(10, 25); need(a + b + c <= 100)
    return ('ln1_three_parts', f'A path has three parts. They are {a} meters, {b} meters and {c} meters long. How long is the path?', qty(a + b + c, 'meters'),
            [f'{a} + {b} = {a + b}.', f'{a + b} + {c} = {a + b + c} meters.'], [qty(a + b, 'meters'), qty(a + b + c - 10, 'meters'), qty(a + b + c + 10, 'meters')])


@adv(sk(LN, 1))
def ln1_a(r):
    tot, a, b = r.randint(60, 99), r.randint(15, 30), r.randint(15, 30); need(tot - a - b > 0)
    return ('ln1_missing_part', f'A fence is {tot} feet long. It has three parts. Two parts are {a} feet and {b} feet. How long is the third part?', qty(tot - a - b, 'feet'),
            [f'{a} + {b} = {a + b}.', f'{tot} − {a + b} = {tot - a - b} feet.'], [qty(tot - a, 'feet'), qty(a + b, 'feet'), qty(tot + a + b if tot + a + b < 100 else tot - b, 'feet')])


@std(sk(LN, 2))
def ln2_s(r):
    a, b = r.randint(5, 40), r.randint(5, 40); need(a < b)
    return ('ln2_from_to', f'A length starts at {a} on the number line and ends at {b}. How many units long is it?', qty(b - a, 'units'), [f'Count from {a} to {b}.', f'{b} − {a} = {b - a} units.'],
            [qty(b, 'units'), qty(a + b, 'units'), qty(b - a + 1, 'units')])


@adv(sk(LN, 2))
def ln2_a(r):
    a, d = r.randint(10, 60), r.randint(5, 30)
    return ('ln2_end_from_start', f'A length is {d} units long and starts at {a} on the number line. Where does it end? Then where would it end if it were 10 units longer?', f'{a + d}; {a + d + 10}',
            [f'{a} + {d} = {a + d}.', f'{a + d} + 10 = {a + d + 10}.'], [f'{a + d}; {a + d + 1}', f'{a - d if a > d else d}; {a + d + 10}', f'{d}; {d + 10}'])


@std(sk(LN, 3))
def ln3_s(r):
    a, b, c = r.randint(20, 50), r.randint(10, 30), r.randint(5, 15)
    return ('ln3_two_jumps', f'Start at {a} on a number line. Jump forward {b}, then jump back {c}. Where do you land?', n(a + b - c), [f'{a} + {b} = {a + b}.', f'{a + b} − {c} = {a + b - c}.'],
            [n(a + b), n(a - b + c if a > b else a + c), n(a + b + c)])


@adv(sk(LN, 3))
def ln3_a(r):
    a, end = r.randint(10, 40), r.randint(50, 95)
    return ('ln3_jump_size', f'Start at {a} and make one jump forward to land on {end}. Then jump back the same amount. Where do you land?', n(a),
            [f'The jump is {end} − {a} = {end - a}.', f'{end} − {end - a} = {a}.'], [n(end - a), n(end + end - a if end + end - a <= 100 else a + 10), n(end)])

# =============================================================== time and money


@std(sk(TM, 1))
def tm1_s(r):
    k = r.randint(1, 11); x = r.choice([5, 10, 15]); need(k * 5 + x < 60)
    return ('tm1_minute_hand_later', f'The minute hand points to the {k}. How many minutes after the hour is it? How many minutes after the hour will it be {x} minutes later?',
            f'{k * 5} minutes; {k * 5 + x} minutes', [f'{k} × 5 = {k * 5} minutes.', f'{k * 5} + {x} = {k * 5 + x} minutes.'],
            [f'{k} minutes; {k + x} minutes', f'{k * 5} minutes; {k * 5 + 5} minutes', f'{k * 10} minutes; {k * 10 + x} minutes'])


@adv(sk(TM, 1))
def tm1_a(r):
    h, m = r.randint(1, 11), r.randint(1, 10) * 5; x = r.choice([15, 20, 25, 30, 35])
    t0 = h * 60 + m
    return ('tm1_time_later', f'A clock shows {tm(t0)}. What time will it show {x} minutes later?', tm(t0 + x), [f'Count on by 5s from {tm(t0)}.', f'{x} minutes later is {tm(t0 + x)}.'],
            [tm(t0 + x - 5), tm(t0 + x + 10), tm(t0 - x)])


@std(sk(TM, 2))
def tm2_s(r):
    h = r.randint(7, 11); m = r.randint(0, 11) * 5; x = r.choice([1, 2, 3])
    return ('tm2_am_hours_later', f'School starts at {h}:{m:02d} AM. Lunch is {x} {"hour" if x == 1 else "hours"} later. What time is lunch?',
            f'{(h + x - 1) % 12 + 1}:{m:02d} {"AM" if h + x < 12 else "PM"}', [f'{h}:{m:02d} + {x} {"hour" if x == 1 else "hours"}.', f'It is {(h + x - 1) % 12 + 1}:{m:02d} {"AM" if h + x < 12 else "PM"}; after 12:00 noon it is PM.'],
            [f'{(h + x - 1) % 12 + 1}:{m:02d} {"PM" if h + x < 12 else "AM"}', f'{h}:{m:02d} AM', f'{(h + x) % 12 + 1}:{m:02d} {"AM" if h + x < 12 else "PM"}'])


@adv(sk(TM, 2))
def tm2_a(r):
    a, b = r.randint(6, 11), r.randint(1, 9)
    return ('tm2_am_to_pm_hours', f'Ana wakes up at {a}:00 AM and eats dinner at {b}:00 PM the same day. How many hours apart are those times?', qty(12 - a + b, 'hours'),
            [f'{a}:00 AM to 12:00 noon is {12 - a} hours.', f'12:00 noon to {b}:00 PM is {b} hours: {12 - a} + {b} = {12 - a + b}.'], [qty(abs(b - a), 'hours'), qty(a + b, 'hours'), qty(12 - a + b + 1, 'hours')])


COINS = {'quarter': 25, 'dime': 10, 'nickel': 5, 'penny': 1}
PL = {'quarter': 'quarters', 'dime': 'dimes', 'nickel': 'nickels', 'penny': 'pennies'}


def coins_text(cs):
    return ', '.join(f'{k} {c if k == 1 else PL[c]}' for c, k in cs if k)


@std(sk(TM, 3))
def tm3_s(r):
    cs = [('quarter', r.randint(0, 2)), ('dime', r.randint(1, 4)), ('nickel', r.randint(0, 3)), ('penny', r.randint(1, 4))]
    v = sum(COINS[c] * k for c, k in cs); x = r.randint(5, 20); need(v + x < 100)
    return ('tm3_count_then_add', f'{r.choice(NAMES)} has {coins_text(cs)}. Then finds {x}¢ more. How much money is that now?', f'{v + x}¢',
            [f'The coins are {v}¢.', f'{v}¢ + {x}¢ = {v + x}¢.'], [f'{v}¢', f'{v + x + 5}¢', f'{sum(k for _, k in cs) + x}¢'])


@adv(sk(TM, 3))
def tm3_a(r):
    cs = [('quarter', r.randint(1, 3)), ('dime', r.randint(1, 3)), ('penny', r.randint(1, 4))]
    v = sum(COINS[c] * k for c, k in cs); need(v < 100)
    return ('tm3_more_to_dollar', f'{r.choice(NAMES)} has {coins_text(cs)}. How many more cents are needed to make $1?', f'{100 - v}¢',
            [f'The coins are {v}¢.', f'100¢ − {v}¢ = {100 - v}¢.'], [f'{v}¢', f'{100 - v + 10}¢', f'{100 - v - 1}¢'])


@adv(sk(TM, 4))
def tm4_a(r):
    t, f, o = r.randint(0, 2), r.randint(1, 3), r.randint(1, 4); v = 20 * t + 5 * f + o; need(t + f + o > 2); cost = r.randint(5, v - 1)
    bills = ', '.join(x for x in [f'{t} $20 bill{"s" if t > 1 else ""}' if t else '', f'{f} $5 bill{"s" if f > 1 else ""}', f'{o} $1 bill{"s" if o > 1 else ""}'] if x)
    return ('tm4_bills_minus_cost', f'{r.choice(NAMES)} has {bills}. A game costs ${cost}. How much money is left after buying it?', f'${v - cost}',
            [f'The bills are ${v}.', f'${v} − ${cost} = ${v - cost}.'], [f'${v}', f'${cost}', f'${v - cost + 5}'])

# =============================================================== shapes and equal shares


@std(sk(SH, 1))
def sh1_s(r):
    (s1, n1), (s2, n2) = r.sample([('triangle', 3), ('quadrilateral', 4), ('pentagon', 5), ('hexagon', 6)], 2)
    return ('sh1_sides_two_shapes', f'How many sides do a {s1} and a {s2} have in all?', n(n1 + n2), [f'A {s1} has {n1} sides and a {s2} has {n2}.', f'{n1} + {n2} = {n1 + n2}.'],
            [n(n1), n(n1 + n2 + 1), n(n1 * n2)])


@adv(sk(SH, 1))
def sh1_a(r):
    s, k = r.choice([('triangle', 3), ('quadrilateral', 4), ('pentagon', 5), ('hexagon', 6)]), r.randint(2, 4)
    return ('sh1_angles_many', f'How many angles do {k} {s[0]}s have in all?', n(k * s[1]), [f'A {s[0]} has {s[1]} angles.', f'{" + ".join([str(s[1])] * k)} = {k * s[1]}.'],
            [n(s[1]), n(k + s[1]), n(k * s[1] + s[1])])


@std(sk(SH, 2))
def sh2_s(r):
    k = r.choice([3, 4, 5, 6]); name = {3: 'triangle', 4: 'quadrilateral', 5: 'pentagon', 6: 'hexagon'}[k]
    return ('sh2_draw_name_angles', f'{r.choice(NAMES)} draws a closed shape with {k} straight sides. What kind of shape is it, and how many angles does it have?', f'{name}; {k}',
            [f'A closed shape with {k} sides is a {name}.', f'It has {k} angles.'], [f'{name}; {k + 1}', f'{"hexagon" if k != 6 else "pentagon"}; {k}', f'{name}; {k * 2}'])


@adv(sk(SH, 2))
def sh2_a(r):
    a, b = r.sample([3, 4, 5, 6], 2); names = {3: 'triangle', 4: 'quadrilateral', 5: 'pentagon', 6: 'hexagon'}
    return ('sh2_more_sides', f'Lena draws a {names[a]} and Omar draws a {names[b]}. How many more sides does the shape with more sides have?', n(abs(a - b)),
            [f'{names[a].capitalize()}: {a}. {names[b].capitalize()}: {b}.', f'{max(a, b)} − {min(a, b)} = {abs(a - b)}.'], [n(a + b), n(max(a, b)), n(abs(a - b) + 1)])


@std(sk(SH, 3))
def sh3_s(r):
    k = r.randint(2, 5); x = r.randint(1, 5)
    return ('sh3_faces_minus', f'{r.choice(NAMES)} puts one sticker on every face of {k} cubes. {x} {"sticker falls" if x == 1 else "stickers fall"} off. How many stickers are still on?', qty(6 * k - x, 'stickers'),
            [f'A cube has 6 faces: {k} × 6 = {6 * k}.', f'{6 * k} − {x} = {6 * k - x}.'], [qty(6 * k, 'stickers'), qty(4 * k - x, 'stickers'), qty(6 * k + x, 'stickers')])


@adv(sk(SH, 3))
def sh3_a(r):
    s = r.randint(12, 36); need(s % 6 == 0)
    return ('sh3_cubes_from_stickers', f'{r.choice(NAMES)} used {s} stickers to cover every face of some cubes, one sticker on each face. How many cubes are there?', qty(s // 6, 'cubes'),
            ['A cube has 6 faces.', f'{" + ".join(["6"] * (s // 6))} = {s}, so there are {s // 6} cubes.'], [qty(s // 4, 'cubes'), qty(s, 'cubes'), qty(s // 6 + 1, 'cubes')])


@std(sk(SH, 4))
def sh4_s(r):
    rows, cols = r.randint(2, 5), r.randint(2, 5); x = r.randint(1, rows * cols - 1)
    return ('sh4_squares_minus_shaded', f'A rectangle is split into {rows} rows of {cols} same-size squares. {x} squares are shaded. How many squares are not shaded?', n(rows * cols - x),
            [f'{rows} rows of {cols} = {rows * cols} squares.', f'{rows * cols} − {x} = {rows * cols - x}.'], [n(rows * cols), n(x), n(rows + cols - x if rows + cols > x else rows * cols + x)])


@adv(sk(SH, 4))
def sh4_a(r):
    rows, cols = r.randint(2, 4), r.randint(2, 5); add = r.randint(1, 2)
    return ('sh4_more_rows_columns', f'A rectangle has {rows} rows of {cols} same-size squares. {r.choice(NAMES)} adds {add} more {"column" if add == 1 else "columns"}. How many squares are there now?',
            n(rows * (cols + add)), [f'Each row now has {cols} + {add} = {cols + add} squares.', f'{rows} rows of {cols + add} = {rows * (cols + add)}.'], [n(rows * cols), n((rows + add) * cols), n(rows * cols + add)])
