"""Question families for the 1st Grade Math audit (2026-11-19).

S[skill](r) -> a Standard item: the skill's Support task with one added step (#7).
A[skill](r) -> an Advanced item: two steps, a missing part or a compare (#2, #18, #19).
Each returns (family, prompt, answer, steps, wrong_answers). Numbers stay inside Grade 1 limits: add and subtract within
20, add within 100 with a one-digit number or a multiple of 10, subtract multiples of 10, count to 120, time to the hour
and half hour. Every answer is computed here and recomputed independently by scripts/test-grade1-audit.cjs."""
NAMES = ['Ava', 'Ben', 'Cora', 'Dev', 'Eli', 'Gabi', 'Hugo', 'Isla', 'Jada', 'Kai', 'Lena', 'Max', 'Nia', 'Omar', 'Pia', 'Raj', 'Sam', 'Tess', 'Uma', 'Zoe']
THINGS = ['apples', 'shells', 'cubes', 'stickers', 'beads', 'books', 'balls', 'hats']
SINGULAR = {'apples': 'apple', 'shells': 'shell', 'cubes': 'cube', 'stickers': 'sticker', 'beads': 'bead', 'books': 'book', 'balls': 'ball', 'hats': 'hat',
            'crayons': 'crayon', 'cookies': 'cookie', 'birds': 'bird', 'fish': 'fish', 'cars': 'car', 'votes': 'vote', 'children': 'child', 'paper clips': 'paper clip', 'ducks': 'duck', 'marbles': 'marble',
            'grapes': 'grape', 'pets': 'pet', 'balloons': 'balloon', 'pages': 'page', 'stamps': 'stamp'}


def qty(x, unit):
    return f'{x} {SINGULAR.get(unit, unit) if str(x) == "1" else unit}'


def n(x):
    return str(x)


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


AT, AS, WP, EQ, CN, TO, CM, AH, ML, TT, DT, SH = ('add-subtract-10', 'add-subtract-20', 'word-problems-20', 'equal-sign', 'count-120', 'tens-ones',
                                                  'compare-numbers', 'add-subtract-100', 'measuring-length', 'telling-time', 'data', 'shapes-equal-shares')


def sk(u, i):
    return f'{u}-skill-{i:02d}'


def tens_ones(v):
    t, o = divmod(v, 10)
    return f'{t} {"ten" if t == 1 else "tens"} and {o} {"one" if o == 1 else "ones"}'

# =============================================================== within 10


@std(sk(AT, 1))
def at1_s(r):
    a, b, c = r.randint(1, 5), r.randint(1, 4), r.randint(1, 3); need(a + b + c <= 10)
    return ('at1_add_then_one_more', f'Add {a} + {b}. Then add {c} more.', n(a + b + c), [f'{a} + {b} = {a + b}.', f'{a + b} + {c} = {a + b + c}.'], [n(a + b), n(a + b + c + 1), n(a + c)])


@adv(sk(AT, 1))
def at1_a(r):
    a, b = r.randint(1, 6), r.randint(1, 4); need(a + b < 10); t = r.choice(THINGS); p, q = r.sample(NAMES, 2)
    return ('at1_how_many_more_to_10', f'{p} has {a} {t}. {q} gives {p} {b} more. How many more {t} does {p} need to have 10?', qty(10 - a - b, t),
            [f'{a} + {b} = {a + b}.', f'{a + b} + {10 - a - b} = 10.'], [qty(a + b, t), qty(10 - a, t), qty(10 - b, t)])


@std(sk(AT, 2))
def at2_s(r):
    a, b, c = r.randint(5, 10), r.randint(1, 3), r.randint(1, 3); need(a - b - c >= 0)
    return ('at2_take_away_twice', f'Take {b} away from {a}. Then take away {c} more. What is left?', n(a - b - c), [f'{a} − {b} = {a - b}.', f'{a - b} − {c} = {a - b - c}.'], [n(a - b), n(a - b + c), n(a - c)])


@adv(sk(AT, 2))
def at2_a(r):
    a, b = r.randint(5, 10), r.randint(1, 4); need(a - b > 0); t = r.choice(THINGS); p = r.choice(NAMES)
    return ('at2_start_unknown', f'{p} had some {t}. {p} gave away {b}. Now {p} has {a - b}. How many {t} did {p} have at first?', qty(a, t),
            [f'Think: ___ − {b} = {a - b}.', f'{a - b} + {b} = {a}.'], [qty(a - b, t), qty(a - 2 * b if a > 2 * b else a + 1, t), qty(b, t)])


@std(sk(AT, 3))
def at3_s(r):
    a = r.randint(1, 9); x = r.randint(1, 5)
    return ('at3_make_ten_then_more', f'What number goes with {a} to make 10? Then add {x} to that number.', n(10 - a + x), [f'{a} + {10 - a} = 10.', f'{10 - a} + {x} = {10 - a + x}.'], [n(10 - a), n(a + x), n(10 + x)])


@adv(sk(AT, 3))
def at3_a(r):
    a, b = r.randint(1, 8), r.randint(1, 8); need(a + b < 10)
    return ('at3_two_to_make_ten', f'{a} + {b} + ___ = 10. What number is missing?', n(10 - a - b), [f'{a} + {b} = {a + b}.', f'{a + b} + {10 - a - b} = 10.'], [n(10 - a), n(10 - b), n(a + b)])


@std(sk(AT, 4))
def at4_s(r):
    w = r.randint(5, 10); a = r.randint(1, w - 1)
    return ('at4_partner_then_check', f'{w} is {a} and what number? Then add the two parts to check.', n(w - a), [f'{w} − {a} = {w - a}.', f'{a} + {w - a} = {w}. It checks.'], [n(w), n(a), n(w - a + 1)])


@adv(sk(AT, 4))
def at4_a(r):
    w = r.randint(6, 10); a, b = r.randint(1, 3), r.randint(1, 3); need(w - a - b > 0)
    return ('at4_three_parts', f'{w} is made of three parts. Two parts are {a} and {b}. What is the third part?', n(w - a - b), [f'{a} + {b} = {a + b}.', f'{w} − {a + b} = {w - a - b}.'], [n(w - a), n(a + b), n(w - b)])

# =============================================================== within 20


@std(sk(AS, 1))
def as1_s(r):
    a, b, c = r.randint(5, 9), r.randint(3, 9), r.randint(1, 3); need(a + b + c <= 20)
    return ('as1_add_then_more', f'Find the sum: {a} + {b}. Then add {c}.', n(a + b + c), [f'{a} + {b} = {a + b}.', f'{a + b} + {c} = {a + b + c}.'], [n(a + b), n(a + b + c + 1), n(a + c)])


@adv(sk(AS, 1))
def as1_a(r):
    a, b = r.randint(6, 9), r.randint(5, 9); need(10 < a + b <= 20); p, q = r.sample(NAMES, 2)
    return ('as1_make_ten_story', f'{p} has {a} stickers and {q} has {b}. To add, {p} moves {10 - a} of {q}\'s stickers to make 10. How many stickers are there in all?', qty(a + b, 'stickers'),
            [f'{a} + {10 - a} = 10, and {b} − {10 - a} = {b - 10 + a} are left.', f'10 + {a + b - 10} = {a + b}.'], [qty(a + b - 1, 'stickers'), qty(10, 'stickers'), qty(a + b + 1, 'stickers')])


@std(sk(AS, 2))
def as2_s(r):
    a, b, c = r.randint(11, 18), r.randint(2, 9), r.randint(1, 3); need(a - b - c >= 0)
    return ('as2_subtract_then_more', f'Subtract: {a} − {b}. Then take away {c} more.', n(a - b - c), [f'{a} − {b} = {a - b}.', f'{a - b} − {c} = {a - b - c}.'], [n(a - b), n(a - b + c), n(a - c)])


@adv(sk(AS, 2))
def as2_a(r):
    a, b = r.randint(11, 18), r.randint(3, 9); need(a - b > 0); p = r.choice(NAMES)
    need(b > a - 10)
    return ('as2_back_through_ten', f'{p} finds {a} − {b} by going back to 10 first. How many does {p} take away to reach 10, and what is {a} − {b}?', f'{a - 10}; {a - b}',
            [f'{a} − {a - 10} = 10.', f'Take away {b - (a - 10)} more: 10 − {b - (a - 10)} = {a - b}.'], [f'{a - 10}; {a - b + 1}', f'{b}; {a - b}', f'10; {a - b}'])


@std(sk(AS, 3))
def as3_s(r):
    a, b, c = r.randint(2, 9), r.randint(2, 9), r.randint(1, 3); need(a + b + c <= 20 and a + b != 10)
    return ('as3_three_then_order', f'What is {a} + {b} + {c}? Then what is {c} + {b} + {a}?', f'{a + b + c}; {a + b + c}', [f'{a} + {b} + {c} = {a + b + c}.', 'Adding in any order gives the same sum.'],
            [f'{a + b + c}; {a + b + c + 1}', f'{a + b}; {a + b + c}', f'{a + b + c + 1}; {a + b + c + 1}'])


@adv(sk(AS, 3))
def as3_a(r):
    a = r.randint(1, 9); b = 10 - a; c = r.randint(2, 9)
    return ('as3_find_the_ten', f'Add {c} + {a} + {b}. Which two numbers make 10, and what is the sum?', f'{a} and {b}; {10 + c}', [f'{a} + {b} = 10.', f'10 + {c} = {10 + c}.'],
            [f'{c} and {a}; {10 + c}', f'{a} and {b}; {10 + c + 1}', f'{c} and {b}; {c + 10}' if c != a else f'{a} and {b}; {c}'])


@std(sk(AS, 4))
def as4_s(r):
    a, b = r.randint(3, 9), r.randint(3, 9); need(a + b > 10)
    return ('as4_family_two_facts', f'{a} + {b} = {a + b}. What is {a + b} − {a}? What is {a + b} − {b}?', f'{b}; {a}', [f'{a + b} − {a} = {b}.', f'{a + b} − {b} = {a}.'], [f'{a}; {b}', f'{a + b}; {a}', f'{b}; {b}'])


@adv(sk(AS, 4))
def as4_a(r):
    a, b = r.randint(3, 9), r.randint(3, 9); need(a != b and a + b > 10)
    return ('as4_missing_in_family', f'{a} + ___ = {a + b}. Use the fact family to write the missing number, then find {a + b} − ___ = {a}.', f'{b}; {b}',
            [f'{a + b} − {a} = {b}.', f'{a + b} − {b} = {a}, so the blank is {b}.'], [f'{b}; {a}', f'{a}; {a}', f'{a + b}; {b}'])

# =============================================================== equal sign


@std(sk(EQ, 1))
def eq1_s(r):
    a, b = r.randint(2, 9), r.randint(2, 9); c = r.randint(1, a + b - 1); d = a + b - c + r.choice([0, 1])
    return ('eq1_true_false_sum', f'Is {a} + {b} = {c} + {d} true or false?', 'true' if a + b == c + d else 'false', [f'{a} + {b} = {a + b}.', f'{c} + {d} = {c + d}.'], ['false' if a + b == c + d else 'true', 'both', 'cannot tell'])


@adv(sk(EQ, 1))
def eq1_a(r):
    a, b, x = r.randint(11, 18), r.randint(2, 9), r.randint(1, 9); need(x != b and a - b > 0)
    y = a - b + x + r.choice([0, 0, 1]); need(y <= 20)
    ans = 'true' if a - b == y - x else 'false'
    return ('eq1_true_false_diff', f'Is {a} − {b} = {y} − {x} true or false?', ans, [f'{a} − {b} = {a - b}.', f'{y} − {x} = {y - x}.'], ['false' if ans == 'true' else 'true', 'both', 'cannot tell'])


@std(sk(EQ, 2))
def eq2_s(r):
    a, b = r.randint(2, 9), r.randint(2, 9); x = r.randint(1, 3)
    return ('eq2_missing_then_more', f'{a} + ___ = {a + b}. What is the missing number? Then add {x} to it.', n(b + x), [f'{a + b} − {a} = {b}.', f'{b} + {x} = {b + x}.'], [n(b), n(a + b + x), n(a + x)])


@adv(sk(EQ, 2))
def eq2_a(r):
    a, b = r.randint(11, 19), r.randint(2, 9); need(a - b > 0)
    return ('eq2_missing_start', f'___ − {b} = {a - b}. What number is missing?', n(a), [f'Think addition: {a - b} + {b} = {a}.', f'{a} − {b} = {a - b}.'], [n(a - b), n(a - 2 * b if a > 2 * b else a + 2), n(a + 1)])


@std(sk(EQ, 3))
def eq3_s(r):
    a, b, c = r.randint(2, 9), r.randint(2, 9), r.randint(2, 9); need(a + b - c > 0 and a + b <= 20)
    return ('eq3_balance_missing', f'{a} + {b} = {c} + ___. What number makes both sides equal?', n(a + b - c), [f'{a} + {b} = {a + b}.', f'{c} + {a + b - c} = {a + b}.'], [n(a + b), n(a + b + c if a + b + c <= 20 else c), n(a + b - c + 1)])


@adv(sk(EQ, 3))
def eq3_a(r):
    a, b, c = r.randint(11, 19), r.randint(2, 9), r.randint(1, 9); need(a - b - c > 0)
    return ('eq3_balance_subtract', f'{a} − {b} = {c} + ___. What number makes both sides equal?', n(a - b - c), [f'{a} − {b} = {a - b}.', f'{c} + {a - b - c} = {a - b}.'], [n(a - b), n(a - b + c), n(c)])

# =============================================================== counting to 120


@adv(sk(CN, 1))
def cn1_a(r):
    b, e, x = r.randint(3, 9), r.randint(1, 9), r.randint(1, 9)
    return ('cn1_bags_plus_two', f'There are {b} bags with 10 crayons in each bag, {e} loose crayons, and then {x} more crayons. How many crayons are there?', qty(10 * b + e + x, 'crayons'),
            [f'{b} tens = {10 * b}; {10 * b} + {e} = {10 * b + e}.', f'{10 * b + e} + {x} = {10 * b + e + x}.'], [qty(10 * b + e, 'crayons'), qty(b + e + x, 'crayons'), qty(10 * b + e + x + 10, 'crayons')])


@std(sk(CN, 2))
def cn2_s(r):
    a = r.randint(20, 115); k = r.randint(2, 4); need(a + k <= 120)
    return ('cn2_count_on_k', f'Start at {a}. Count on {k} more. What number do you say last?', n(a + k), [f'Count {", ".join(str(a + i) for i in range(1, k + 1))}.', f'You end on {a + k}.'], [n(a + k - 1), n(a + k + 1), n(a + 10)])


@adv(sk(CN, 2))
def cn2_a(r):
    a = r.choice([97, 98, 99, 107, 108, 109, 87, 88, 89]); k = r.randint(3, 6); need(a + k <= 120)
    return ('cn2_count_over_ten', f'Count on {k} from {a}. What number do you end on?', n(a + k), [f'Crossing a ten: {", ".join(str(a + i) for i in range(1, k + 1))}.', f'You end on {a + k}.'], [n(a + k - 10), n(a + k + 1), n(a + k - 1)])


@std(sk(CN, 3))
def cn3_s(r):
    v = r.randint(21, 99); W = ['', 'one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine']; T = ['', '', 'twenty', 'thirty', 'forty', 'fifty', 'sixty', 'seventy', 'eighty', 'ninety']
    need(v % 10)
    return ('cn3_name_then_next', f'The number {T[v // 10]}-{W[v % 10]} is written how? Then what number comes next?', f'{v}; {v + 1}', [f'{T[v // 10]}-{W[v % 10]} is {v}.', f'{v} + 1 = {v + 1}.'],
            [f'{v}; {v - 1}', f'{v // 10}{v % 10 + 1}; {v + 2}' if v % 10 < 8 else f'{v + 10}; {v + 11}', f'{(v % 10) * 10 + v // 10}; {(v % 10) * 10 + v // 10 + 1}'])


@adv(sk(CN, 3))
def cn3_a(r):
    v = r.randint(101, 119)
    return ('cn3_hundred_and', f'How do you write one hundred {["", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten", "eleven", "twelve", "thirteen", "fourteen", "fifteen", "sixteen", "seventeen", "eighteen", "nineteen"][v - 100]} in numbers?', n(v),
            [f'One hundred is 100.', f'100 + {v - 100} = {v}.'], [n(1000 + v - 100), n(10 * (v - 100)), n(v + 10)])


@std(sk(CN, 4))
def cn4_s(r):
    a = r.randint(20, 110); k, j = r.randint(2, 5), r.randint(1, 3); need(a + k <= 120 and k != j)
    return ('cn4_on_then_back', f'Start at {a}. Count on {k}, then count back {j}. Where do you end?', n(a + k - j), [f'{a} + {k} = {a + k}.', f'{a + k} − {j} = {a + k - j}.'], [n(a + k), n(a - j), n(a + k + j)])


@adv(sk(CN, 4))
def cn4_a(r):
    a, b = r.randint(20, 110), r.randint(3, 8); need(a + b <= 120)
    return ('cn4_how_many_counted', f'{r.choice(NAMES)} counts on from {a} and stops at {a + b}. How many numbers did {r.choice(["they", "the child"])} count on?', n(b), [f'Count {", ".join(str(a + i) for i in range(1, b + 1))}.', f'That is {b} numbers: {a + b} − {a} = {b}.'], [n(b + 1), n(a + b), n(b - 1)])

# =============================================================== tens and ones


@adv(sk(TO, 1))
def to1_a(r):
    t, x = r.randint(2, 8), r.randint(1, 9)
    return ('to1_tens_plus_ones', f'How many ones are in {t} tens and {x} ones?', n(10 * t + x), [f'{t} tens = {10 * t} ones.', f'{10 * t} + {x} = {10 * t + x} ones.'], [n(t + x), n(10 * t), n(10 * x + t)])


@std(sk(TO, 2))
def to2_s(r):
    o = r.randint(1, 9); x = r.randint(1, 9 - o) if o < 9 else 0; need(x > 0)
    return ('to2_teen_then_more', f'What number is 1 ten and {o} ones? Then add {x} more ones.', n(10 + o + x), [f'1 ten and {o} ones is {10 + o}.', f'{10 + o} + {x} = {10 + o + x}.'], [n(10 + o), n(1 + o + x), n(10 + o + 10)])


@std(sk(TO, 3))
def to3_s(r):
    a = r.randint(2, 9); k = r.randint(2, 4); need(a + 10 * k <= 120)
    return ('to3_tens_jumps', f'Start at {a}. Count by tens {k} times. What number do you end on?', n(a + 10 * k), [f'Each count adds 10.', f'{a} + {k} tens = {a + 10 * k}.'], [n(a + k), n(a + 10 * (k - 1)), n(a + 10 * (k + 1))])


@adv(sk(TO, 3))
def to3_a(r):
    a = r.randint(2, 9); b = a + 10 * r.randint(3, 8); need(b <= 120)
    return ('to3_how_many_tens_counted', f'How many tens do you count to get from {a} to {b}?', n((b - a) // 10), [f'Count {", ".join(str(x) for x in range(a + 10, b + 1, 10))}.', f'That is {(b - a) // 10} tens.'], [n((b - a) // 10 + 1), n(b - a), n((b - a) // 10 - 1)])


@std(sk(TO, 4))
def to4_s(r):
    v = r.randint(21, 98); need(v % 10)
    return ('to4_tens_ones_then_ten_more', f'What number has {v // 10} tens and {v % 10} ones? What number is 1 more ten?', f'{v}; {v + 10}', [f'{v // 10} tens and {v % 10} ones is {v}.', f'{v} + 10 = {v + 10}.'],
            [f'{v}; {v + 1}', f'{(v % 10) * 10 + v // 10}; {(v % 10) * 10 + v // 10 + 10}', f'{v + 1}; {v + 10}'])


@adv(sk(TO, 4))
def to4_a(r):
    t, o = r.randint(2, 8), r.randint(10, 15)
    return ('to4_regroup_ones', f'A number has {t} tens and {o} ones. What is the number?', n(10 * t + o), [f'{o} ones = 1 ten and {o - 10} ones.', f'{t + 1} tens and {o - 10} ones = {10 * t + o}.'], [n(10 * t + o % 10), n(t + o), n(10 * t + o + 10)])

# =============================================================== comparing


@std(sk(CM, 1))
def cm1_s(r):
    a, b = r.sample(range(11, 99), 2); x = r.randint(1, 9)
    need(max(a, b) + x <= 120)
    return ('cm1_greater_then_more', f'Which is greater, {a} or {b}? Then add {x} to it.', n(max(a, b) + x), [f'{max(a, b)} is greater.', f'{max(a, b)} + {x} = {max(a, b) + x}.'], [n(min(a, b) + x), n(max(a, b)), n(max(a, b) + x + 1)])


@adv(sk(CM, 1))
def cm1_a(r):
    xs = r.sample(range(11, 99), 3)
    return ('cm1_order_three', f'Write the numbers from least to greatest: {", ".join(map(str, xs))}', ', '.join(map(str, sorted(xs))),
            ['Compare the tens first, then the ones.', ', '.join(map(str, sorted(xs))) + '.'], [', '.join(map(str, sorted(xs, reverse=True))), ', '.join(map(str, xs)), ', '.join(map(str, [sorted(xs)[1], sorted(xs)[0], sorted(xs)[2]]))])


@std(sk(CM, 2))
def cm2_s(r):
    a, b = r.sample(range(11, 99), 2); x = r.choice([1, 10])
    return ('cm2_symbol_after_change', f'Write >, =, or <: {a} + {x} ___ {b}', '>' if a + x > b else '<' if a + x < b else '=', [f'{a} + {x} = {a + x}.', f'Compare {a + x} and {b}.'],
            [c for c in '<>=' if c != ('>' if a + x > b else '<' if a + x < b else '=')])


@adv(sk(CM, 2))
def cm2_a(r):
    t1, o1 = r.randint(2, 9), r.randint(0, 9); t2, o2 = r.randint(2, 9), r.randint(0, 9)
    a, b = 10 * t1 + o1, 10 * t2 + o2; need(a != b)
    return ('cm2_tens_ones_compare', f'Write >, =, or <: {t1} tens and {o1} ones ___ {t2} tens and {o2} ones', '>' if a > b else '<', [f'{t1} tens and {o1} ones = {a}; {t2} tens and {o2} ones = {b}.', f'{a} {">" if a > b else "<"} {b}.'],
            ['<' if a > b else '>', '='])


@std(sk(CM, 3))
def cm3_s(r):
    t, o = r.randint(2, 9), r.randint(1, 8)
    return ('cm3_digit_to_make_greater', f'Which is the greatest digit that makes this true? {t}? < {10 * t + o}', n(o - 1), [f'Both numbers have {t} tens.', f'The ones digit must be less than {o}, so the greatest is {o - 1}.'], [n(o), n(o + 1), n(9)])


@adv(sk(CM, 3))
def cm3_a(r):
    a = r.randint(20, 80); b = a + r.randint(5, 15)
    cnt = b - a - 1
    return ('cm3_count_between', f'How many whole numbers are greater than {a} and less than {b}?', n(cnt), [f'They are {a + 1} to {b - 1}.', f'{b - 1} − {a + 1} + 1 = {cnt}.'], [n(cnt + 1), n(b - a), n(cnt - 1)])

# =============================================================== within 100


@std(sk(AH, 1))
def ah1_s(r):
    a = r.randint(15, 80); need(a + 20 <= 120)
    return ('ah1_ten_more_twice', f'What is 10 more than {a}? Then what is 10 more than that?', f'{a + 10}; {a + 20}', [f'{a} + 10 = {a + 10}.', f'{a + 10} + 10 = {a + 20}.'], [f'{a + 1}; {a + 2}', f'{a + 10}; {a + 11}', f'{a + 20}; {a + 30}'])


@adv(sk(AH, 1))
def ah1_a(r):
    a = r.randint(25, 95); k = r.randint(2, 3)
    need(a - 10 * k > 0)
    return ('ah1_ten_less_k_times', f'Start at {a}. Take away 10, {k} times. What number do you end on?', n(a - 10 * k), [f'{k} tens = {10 * k}.', f'{a} − {10 * k} = {a - 10 * k}.'], [n(a - k), n(a - 10 * (k - 1)), n(a - 10 * k - 1)])


@std(sk(AH, 2))
def ah2_s(r):
    a, b, c = r.randint(1, 5) * 10 + r.randint(1, 9), r.randint(1, 3) * 10, r.randint(1, 3) * 10; need(a + b + c <= 99)
    return ('ah2_add_two_tens', f'Add: {a} + {b} + {c}', n(a + b + c), [f'{b} + {c} = {b + c}.', f'{a} + {b + c} = {a + b + c}.'], [n(a + b), n(a + b + c + 1), n(a + (b + c) // 10)])


@adv(sk(AH, 2))
def ah2_a(r):
    a, b = r.randint(5, 9) * 10, r.randint(1, 4) * 10; c = r.randint(1, 3) * 10; need(a - b + c <= 90 and a > b and b != c)
    return ('ah2_tens_sub_then_add', f'Find {a} − {b} + {c}.', n(a - b + c), [f'{a} − {b} = {a - b}.', f'{a - b} + {c} = {a - b + c}.'], [n(a - b - c), n(a + b + c if a + b + c <= 120 else a - b), n(a - b)])


@std(sk(AH, 3))
def ah3_s(r):
    a, b, c = r.randint(21, 80), r.randint(1, 8), r.randint(1, 5); need((a % 10) + b + c <= 9)
    return ('ah3_add_ones_twice', f'Add {a} + {b}. Then add {c}.', n(a + b + c), [f'{a} + {b} = {a + b}.', f'{a + b} + {c} = {a + b + c}.'], [n(a + b), n(a + 10 * b + c), n(a + b + c + 10)])


@adv(sk(AH, 3))
def ah3_a(r):
    a, b = r.randint(21, 89), r.randint(2, 9); need(a % 10 + b <= 9)
    return ('ah3_missing_tens_ones', f'{a} + ___ = {a + b + 10}. What number makes this true?', n(b + 10), [f'From {a} to {a + b + 10} is 1 ten and {b} ones.', f'10 + {b} = {b + 10}.'], [n(b), n(b + 1), n(a + b)])


@std(sk(AH, 4))
def ah4_s(r):
    a, b = r.randint(21, 79), r.randint(2, 9); need(a % 10 + b >= 10); x = r.choice([10, 20])
    return ('ah4_new_ten_then_tens', f'What is {a} + {b}? Then add {x}.', n(a + b + x), [f'{a} + {b} = {a + b} (make a new ten).', f'{a + b} + {x} = {a + b + x}.'], [n(a + b), n(a + b + x - 10), n(a + x)])


@adv(sk(AH, 4))
def ah4_a(r):
    a, b = r.randint(21, 89), r.randint(2, 9); need(a % 10 + b >= 10)
    up = 10 - a % 10
    return ('ah4_break_to_ten', f'To add {a} + {b}, {r.choice(NAMES)} breaks {b} into {up} and {b - up}. What is {a} + {up}, and what is {a} + {b}?', f'{a + up}; {a + b}',
            [f'{a} + {up} = {a + up}.', f'{a + up} + {b - up} = {a + b}.'], [f'{a + up}; {a + b - 1}', f'{a + b - up}; {a + b}', f'{a + up}; {a + up}'])


@std(sk(AH, 5))
def ah5_s(r):
    a, b = r.randint(21, 59), r.randint(11, 39); need(a + b <= 99)
    return ('ah5_tens_then_ones', f'Add {a} + {b} by adding tens, then ones. What are the tens, and what is the sum?', f'{a // 10 * 10 + b // 10 * 10}; {a + b}',
            [f'{a // 10 * 10} + {b // 10 * 10} = {a // 10 * 10 + b // 10 * 10}.', f'Ones: {a % 10} + {b % 10} = {a % 10 + b % 10}; total {a + b}.'], [f'{a // 10 + b // 10}; {a + b}', f'{a // 10 * 10 + b // 10 * 10}; {a + b - 10}', f'{a + b}; {a + b}'])


@adv(sk(AH, 5))
def ah5_a(r):
    a, b, c = r.randint(11, 40), r.randint(11, 30), r.randint(1, 9); need(a + b + c <= 99)
    return ('ah5_two_digit_plus_more', f'A class read {a} pages on Monday and {b} pages on Tuesday. On Wednesday they read {c} more. How many pages is that in all?', f'{a + b + c} pages',
            [f'{a} + {b} = {a + b}.', f'{a + b} + {c} = {a + b + c}.'], [f'{a + b} pages', f'{a + b + c + 10} pages', f'{a + c} pages'])

# =============================================================== telling time


def clock(h, m):
    return f'{h}:{m:02d}'


@std(sk(TT, 1))
def tt1_s(r):
    h = r.randint(1, 11); x = r.randint(1, 3)
    return ('tt1_hours_later', f'It is {h}:00. What time will it be in {x} {"hour" if x == 1 else "hours"}?', clock((h + x - 1) % 12 + 1, 0), [f'Count {x} {"hour" if x == 1 else "hours"} on from {h}:00.', f'It will be {(h + x - 1) % 12 + 1}:00.'],
            [clock(h, 0), clock((h + x) % 12 + 1, 0), clock(h, 30)])


@adv(sk(TT, 1))
def tt1_a(r):
    h = r.randint(4, 12); x = r.randint(1, 3)
    return ('tt1_hours_before', f'A clock shows {(h + x - 1) % 12 + 1}:00. What time was it {x} {"hour" if x == 1 else "hours"} ago?', clock(h, 0), [f'Count back {x} from {(h + x - 1) % 12 + 1}.', f'It was {h}:00.'],
            [clock((h + 2 * x - 1) % 12 + 1, 0), clock((h + x - 1) % 12 + 1, 0), clock(h, 30)])


@std(sk(TT, 2))
def tt2_s(r):
    h = r.randint(1, 11)
    return ('tt2_half_hour_later', f'It is {h}:00. What time will it be in half an hour? Then in one more half hour?', f'{h}:30; {h + 1}:00', [f'{h}:00 + 30 minutes = {h}:30.', f'{h}:30 + 30 minutes = {h + 1}:00.'],
            [f'{h}:30; {h}:00', f'{h + 1}:00; {h + 1}:30', f'{h}:30; {h + 1}:30'])


@adv(sk(TT, 2))
def tt2_a(r):
    h = r.randint(1, 10)
    return ('tt2_half_hour_before', f'A clock shows {h + 1}:00. What time was it half an hour ago?', clock(h, 30), [f'Half an hour before {h + 1}:00 is half past {h}.', f'That is {h}:30.'],
            [clock(h + 1, 30), clock(h, 0), clock(h - 1 if h > 1 else 12, 30)])


@std(sk(TT, 3))
def tt3_s(r):
    h = r.randint(1, 11); m = r.choice([0, 30])
    words = f'half past {h}' if m else f'{h} o\'clock'
    return ('tt3_words_then_later', f'Write {words} with numbers. Then what time is it one hour later?', f'{clock(h, m)}; {clock(h % 12 + 1, m)}', [f'{words} is {clock(h, m)}.', f'One hour later is {clock(h % 12 + 1, m)}.'],
            [f'{clock(h, m)}; {clock(h, 30 - m)}', f'{clock(h % 12 + 1, m)}; {clock(h % 12 + 1, m)}', f'{clock(h, 30 - m)}; {clock(h % 12 + 1, 30 - m)}'])


@adv(sk(TT, 3))
def tt3_a(r):
    h = r.randint(1, 10); p, q = r.sample(NAMES, 2); a, b = r.choice([(0, 30), (30, 0)])
    t1, t2 = h * 60 + a, (h + (1 if b == 0 and a == 30 else 0)) * 60 + b
    need(t1 != t2)
    first = p if t1 < t2 else q
    return ('tt3_who_first', f'{p} eats lunch at {clock(h, a)}. {q} eats lunch at {clock(h + (1 if b == 0 and a == 30 else 0), b)}. Who eats lunch first?', first,
            [f'{clock(h, a)} and {clock(h + (1 if b == 0 and a == 30 else 0), b)}.', f'The earlier time is {first}\'s.'], [q if first == p else p, 'They eat at the same time', 'You cannot tell'])

# =============================================================== data, shapes, words


@adv(sk(DT, 1))
def dt1_a(r):
    a, b = r.randint(6, 19), r.randint(3, 15); need(a != b)
    return ('dt1_tally_difference', f'The tally chart shows {a} votes for cats and {b} votes for dogs. How many more votes did the pet with more votes get?', qty(abs(a - b), 'votes'),
            [f'Cats: {a}. Dogs: {b}.', f'{max(a, b)} − {min(a, b)} = {abs(a - b)}.'], [qty(a + b, 'votes'), qty(max(a, b), 'votes'), qty(abs(a - b) + 1, 'votes')])


@std(sk(DT, 2))
def dt2_s(r):
    b, m = r.randint(1, 3), r.randint(1, 4); x = r.randint(1, 4)
    return ('dt2_tally_then_more', f'A tally row has {b} {"bundle" if b == 1 else "bundles"} of 5 and {m} more marks. Then {x} more {"vote is" if x == 1 else "votes are"} added. What number is that now?', n(5 * b + m + x),
            [f'{b} × 5 = {5 * b}; {5 * b} + {m} = {5 * b + m}.', f'{5 * b + m} + {x} = {5 * b + m + x}.'], [n(5 * b + m), n(b + m + x), n(5 * b + m + x + 1)])


@adv(sk(DT, 3))
def dt3_a(r):
    a, b, c = r.sample(range(3, 15), 3)
    return ('dt3_total_and_compare', f'A table shows circles {a}, squares {b} and triangles {c}. How many shapes are there in all?', n(a + b + c), [f'{a} + {b} = {a + b}.', f'{a + b} + {c} = {a + b + c}.'], [n(a + b), n(a + b + c + 1), n(max(a, b, c))])


@adv(sk(SH, 1))
def sh1_a(r):
    s = r.choice([('triangle', 3), ('square', 4), ('rectangle', 4), ('hexagon', 6)]); k = r.randint(2, 3)
    return ('sh1_corners_many', f'How many corners do {k} {s[0]}s have in all?', n(k * s[1]), [f'A {s[0]} has {s[1]} corners.', f'{" + ".join([str(s[1])] * k)} = {k * s[1]}.'], [n(s[1]), n(k + s[1]), n(k * s[1] + 1)])


@adv(sk(SH, 2))
def sh2_a(r):
    (a, x), (b, y) = r.sample([('triangle', 3), ('square', 4), ('hexagon', 6), ('rectangle', 4)], 2)
    return ('sh2_sides_two_shapes', f'How many sides do a {a} and a {b} have together?', n(x + y), [f'A {a} has {x} sides and a {b} has {y}.', f'{x} + {y} = {x + y}.'], [n(x), n(x + y + 1), n(abs(x - y))])


@adv(sk(SH, 3))
def sh3_a(r):
    k = r.randint(2, 4)
    return ('sh3_triangles_to_squares', f'Two triangles can make one square. How many triangles do you need to make {k} squares?', n(2 * k), [f'Each square uses 2 triangles.', f'{" + ".join(["2"] * k)} = {2 * k}.'], [n(k), n(2 * k + 1), n(k + 2)])


@std(sk(SH, 4))
def sh4_s(r):
    m = r.choice([2, 4]); e = r.randint(1, m - 1)
    return ('sh4_shares_left', f'A sandwich is cut into {"halves" if m == 2 else "fourths"}. {e} {"share is" if e == 1 else "shares are"} eaten. How many shares are left?', n(m - e), [f'{"Halves" if m == 2 else "Fourths"} make {m} equal shares.', f'{m} − {e} = {m - e}.'], [n(m), n(e), n(m + e)])


@std(sk(SH, 5))
def sh5_s(r):
    m = r.choice([2, 4]); k = r.randint(2, 3)
    return ('sh5_shares_many', f'{k} pizzas are each cut into {"halves" if m == 2 else "fourths"}. How many shares are there in all?', n(k * m), [f'Each pizza has {m} shares.', f'{" + ".join([str(m)] * k)} = {k * m}.'], [n(m), n(k + m), n(k * m + 1)])


@adv(sk(WP, 1))
def wp1_a(r):
    a, b, c = r.randint(8, 15), r.randint(2, 6), r.randint(1, 5); need(a + b - c > 0 and a + b <= 20)
    return ('wp1_in_then_out', f'{a} birds were on a wire. {b} more came. Then {c} flew away. How many birds are on the wire now?', qty(a + b - c, 'birds'),
            [f'{a} + {b} = {a + b}.', f'{a + b} − {c} = {a + b - c}.'], [qty(a + b, 'birds'), qty(a - b + c if a > b else a + c, 'birds'), qty(a + b + c if a + b + c <= 20 else a - c, 'birds')])


@adv(sk(WP, 2))
def wp2_a(r):
    t, a = r.randint(12, 20), r.randint(3, 9); b = r.randint(1, 5); need(t - a - b > 0)
    return ('wp2_three_colors', f'A jar has {t} crayons. {a} are red, {b} are blue, and the rest are green. How many crayons are green?', qty(t - a - b, 'crayons'),
            [f'{a} + {b} = {a + b} red and blue.', f'{t} − {a + b} = {t - a - b} green.'], [qty(t - a, 'crayons'), qty(a + b, 'crayons'), qty(t - b, 'crayons')])
