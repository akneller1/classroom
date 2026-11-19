"""Question families for the 4th Grade Math audit (2026-11-19).

S[skill](r) -> a Standard item: the skill's Support task with one added step (#7).
A[skill](r) -> an Advanced item: multi-step, work backward or explain-why (#1).
Each returns (family, prompt, answer, steps, wrong_answers). Numbers stay inside Grade 4 limits: whole numbers to
1,000,000, one-digit divisors, products up to 4 digits by 1 digit or 2 digits by 2 digits, denominators 2, 3, 4, 5, 6,
8, 10, 12 and 100, decimals to hundredths, elapsed time within two hours. Every answer is computed here and
recomputed independently by scripts/test-grade4-audit.cjs."""
import math
from fractions import Fraction as Fr
from lib import F, frac, n

NAMES = ['Ava', 'Ben', 'Carmen', 'Dev', 'Eli', 'Femi', 'Grace', 'Hiro', 'Isla', 'Jonah', 'Kai', 'Lena', 'Mateo', 'Nora', 'Omar', 'Priya', 'Quinn', 'Rosa', 'Sam', 'Tessa', 'Uma', 'Wren', 'Yusuf', 'Zoe']
ORD = ['first', 'second', 'third', 'fourth', 'fifth', 'sixth', 'seventh', 'eighth', 'ninth', 'tenth', 'eleventh', 'twelfth']
PLACE = {1: 'ones', 10: 'tens', 100: 'hundreds', 1000: 'thousands', 10000: 'ten thousands', 100000: 'hundred thousands'}
PRIMES = [p for p in range(2, 101) if all(p % d for d in range(2, int(p ** .5) + 1))]


class Skip(Exception):
    pass


def need(c):
    if not c:
        raise Skip()


def rnd(x, u):
    return int(math.floor(x / u + 0.5)) * u


SINGULAR = {'feet': 'foot', 'inches': 'inch', 'yards': 'yard', 'miles': 'mile', 'pounds': 'pound', 'ounces': 'ounce', 'cups': 'cup', 'pints': 'pint',
            'quarts': 'quart', 'gallons': 'gallon', 'meters': 'meter', 'centimeters': 'centimeter', 'millimeters': 'millimeter', 'kilometers': 'kilometer',
            'grams': 'gram', 'kilograms': 'kilogram', 'liters': 'liter', 'milliliters': 'milliliter', 'minutes': 'minute', 'hours': 'hour', 'seconds': 'second',
            'days': 'day', 'seats': 'seat', 'vans': 'van', 'servings': 'serving', 'empty seats': 'empty seat'}


def qty(x, unit):
    """'1 foot', '3 feet', '1 1/2 feet'"""
    return f'{x} {SINGULAR.get(unit, unit) if str(x) == "1" else unit}'


def an(word):
    return ('an ' if word[0] in 'aeiou' else 'a ') + word


THING = {'inches': 'ribbon', 'feet': 'ribbon', 'yards': 'ribbon', 'centimeters': 'ribbon', 'millimeters': 'wire', 'meters': 'rope', 'kilometers': 'trail',
         'ounces': 'flour', 'pounds': 'flour', 'grams': 'flour', 'kilograms': 'flour', 'cups': 'juice', 'pints': 'juice', 'quarts': 'juice', 'gallons': 'juice',
         'milliliters': 'juice', 'liters': 'juice'}


def factors(k):
    return [d for d in range(1, k + 1) if k % d == 0]


S, A = {}, {}


def std(skill):
    def d(f):
        S.setdefault(skill, []).append(f); return f
    return d


def adv(skill):
    def d(f):
        A.setdefault(skill, []).append(f); return f
    return d


PV, AS, MS, DV, FM, FE, FD, MC, GA, DP = ('place-value-number-sense', 'multi-digit-addition-subtraction', 'multiplication-strategies', 'division-remainders',
                                          'factors-multiples-patterns', 'fractions-equivalent-fractions', 'fraction-operations-decimals',
                                          'measurement-unit-conversions', 'geometry-angles-symmetry', 'data-line-plots-word-problems')


def sk(u, i):
    return f'{u}-skill-{i:02d}'


# =============================================================== place value
@std(sk(PV, 1))
def pv1_s(r):
    num = r.randint(10000, 99999); s = str(num); i = r.randrange(len(s) - 1); d = int(s[i]); need(d and s.count(s[i]) == 1)
    v = d * 10 ** (len(s) - 1 - i)
    return ('pv1_value_times_ten', f'What is the value of the digit {d} in {n(num)}? What would its value be if it moved one place to the left?',
            f'{n(v)}; {n(v * 10)}', [f'The {d} is in the {PLACE[10 ** (len(s) - 1 - i)]} place, so its value is {n(v)}.', f'One place to the left is worth 10 times as much: {n(v)} × 10 = {n(v * 10)}.'],
            [f'{n(v)}; {n(v // 10) if v >= 10 else 1}', f'{n(v * 10)}; {n(v * 100)}', f'{d}; {d * 10}'])


@adv(sk(PV, 1))
def pv1_a(r):
    a = r.randint(2, 9); p1, p2 = r.choice([(10000, 100), (100000, 1000), (1000, 10), (10000, 10), (100000, 100)])
    digits = ['0'] * 6
    num = a * p1 + a * p2 + r.choice([1, 2, 3, 4, 5, 6, 7, 8]) * (10 if p2 != 10 and p1 != 10 else 1)
    need(num < 1000000 and str(num).count(str(a)) == 2)
    return ('pv1_how_many_times_far', f'In {n(num)}, the digit {a} appears twice. The value of the {a} in the {PLACE[p1]} place is how many times the value of the {a} in the {PLACE[p2]} place?',
            n(p1 // p2), [f'The first {a} is worth {n(a * p1)}; the second is worth {n(a * p2)}.', f'{n(a * p1)} ÷ {n(a * p2)} = {n(p1 // p2)}. Each place to the left multiplies the value by 10.'],
            [n(p1 // p2 // 10), n(p1 // p2 * 10), str(len(str(p1)) - len(str(p2)))])


@std(sk(PV, 2))
def pv2_s(r):
    parts = [r.randint(1, 9) * 10 ** k for k in (5, 4, 3, 2, 1, 0) if r.random() < 0.75]
    need(len(parts) >= 4 and parts[0] >= 1000)
    total = sum(parts); k = r.choice([10, 100, 1000])
    return ('pv2_expanded_then_more', f'Write {" + ".join(n(p) for p in parts)} in standard form. Then write the number that is {n(k)} more.',
            n(total + k), [f'Standard form: {n(total)}.', f'{n(k)} more: {n(total)} + {n(k)} = {n(total + k)}.'],
            [n(total), n(total + k * 10), n(total - k)])


@adv(sk(PV, 2))
def pv2_a(r):
    th, h, t, o = r.randint(12, 95), r.randint(11, 19), r.randint(2, 9), r.randint(1, 9)
    v = th * 1000 + h * 100 + t * 10 + o
    return ('pv2_regroup_units', f'A number has {th} thousands, {h} hundreds, {t} tens and {o} ones. Write it in standard form.',
            n(v), [f'{h} hundreds = 1 thousand and {h - 10} hundreds, so there are {th + 1} thousands.', f'{th + 1} thousands + {h - 10} hundreds + {t} tens + {o} ones = {n(v)}.'],
            [n(th * 1000 + (h - 10) * 100 + t * 10 + o), n(v + 100), n(v + 900)])


@std(sk(PV, 3))
def pv3_s(r):
    base = r.randint(100, 999) * 1000; nums = sorted({base + r.randint(0, 999) for _ in range(4)}); need(len(nums) == 4)
    r.shuffle(nums); srt = sorted(nums)
    return ('pv3_order_then_difference', f'Order from least to greatest: {", ".join(n(x) for x in nums)}. Then find the difference between the greatest and the least.',
            n(srt[-1] - srt[0]), [f'They share the same thousands, so compare the hundreds, tens and ones: {", ".join(n(x) for x in srt)}.', f'{n(srt[-1])} − {n(srt[0])} = {n(srt[-1] - srt[0])}.'],
            [n(srt[-1] - srt[1]), n(srt[-2] - srt[0]), n(srt[-1] + srt[0])])


@adv(sk(PV, 3))
def pv3_a(r):
    d = [r.randint(1, 9) for _ in range(6)]; need(len(set(d)) >= 5)
    big = int(''.join(sorted(map(str, d), reverse=True))); small_digits = sorted(map(str, d)); need(small_digits[0] != '0')
    small = int(''.join(small_digits))
    return ('pv3_digit_cards', f'Use each digit card once: {", ".join(map(str, d))}. What is the difference between the greatest and the least 6-digit numbers you can make?',
            n(big - small), [f'Greatest: digits from greatest to least, {n(big)}. Least: digits from least to greatest, {n(small)}.', f'{n(big)} − {n(small)} = {n(big - small)}.'],
            [n(big), n(big - small + 9), n(big + small)])


@std(sk(PV, 4))
def pv4_s(r):
    a, b = r.randint(10000, 99999), r.randint(10000, 99999); u = r.choice([100, 1000])
    return ('pv4_round_then_add', f'Round {n(a)} and {n(b)} to the nearest {PLACE[u][:-1]}. Then add the rounded numbers.',
            n(rnd(a, u) + rnd(b, u)), [f'{n(a)} rounds to {n(rnd(a, u))} and {n(b)} rounds to {n(rnd(b, u))}.', f'{n(rnd(a, u))} + {n(rnd(b, u))} = {n(rnd(a, u) + rnd(b, u))}.'],
            [n(rnd(a + b, u * 10)), n(a + b), n(rnd(a, u) + rnd(b, u) + u)])


@adv(sk(PV, 4))
def pv4_a(r):
    t = r.randint(12, 98) * 1000; u = r.choice([1000, 100])
    if u == 100:
        t = r.randint(120, 980) * 100
    lo, hi = t - u // 2, t + u // 2 - 1
    return ('pv4_rounding_range', f'A whole number rounds to {n(t)} when rounded to the nearest {PLACE[u][:-1]}. What is the difference between the greatest and the least numbers it could be?',
            n(hi - lo), [f'Least: {n(lo)} (exactly halfway rounds up). Greatest: {n(hi)} (one more rounds up to {n(t + u)}).', f'{n(hi)} − {n(lo)} = {n(hi - lo)}.'],
            [n(u), n(u // 2), n(u // 2 - 1)])


# =============================================================== addition and subtraction
@std(sk(AS, 1))
def as1_s(r):
    a, b = r.randint(10000, 499999), r.randint(10000, 499999); c = r.randint(1000, 99999)
    return ('as1_add_then_check', f'Add {n(a)} + {n(b)}. Then add {n(c)} to the sum.', n(a + b + c),
            [f'{n(a)} + {n(b)} = {n(a + b)}.', f'{n(a + b)} + {n(c)} = {n(a + b + c)}.'], [n(a + b), n(a + b + c - 10), n(a + b + c + 1000)])


@adv(sk(AS, 1))
def as1_a(r):
    a = r.randint(100000, 499999); s = r.randint(a + 100000, 999999); b = s - a; c = r.randint(1000, 9999)
    return ('as1_missing_then_more', f'{n(a)} + ___ = {n(s)}. What number is {n(c)} more than the missing addend?', n(b + c),
            [f'Missing addend: {n(s)} − {n(a)} = {n(b)}.', f'{n(b)} + {n(c)} = {n(b + c)}.'], [n(b), n(s + c), n(b - c)])


@std(sk(AS, 2))
def as2_s(r):
    a = r.randint(200000, 999999); b = r.randint(10000, a - 10000)
    return ('as2_subtract_then_check', f'Subtract {n(a)} − {n(b)}. Which addition checks your answer? Give the difference.', n(a - b),
            [f'{n(a)} − {n(b)} = {n(a - b)}.', f'Check: {n(a - b)} + {n(b)} = {n(a)}.'], [n(a + b), n(a - b + 1000), n(a - b - 10)])


@adv(sk(AS, 2))
def as2_a(r):
    a = r.randint(300000, 999999); b = r.randint(10000, 150000); c = r.randint(10000, 150000); need(a - b - c > 0)
    return ('as2_two_subtractions', f'A city had {n(a)} visitors this year. {n(b)} came in spring and {n(c)} came in summer. How many came the rest of the year?', n(a - b - c),
            [f'Spring and summer: {n(b)} + {n(c)} = {n(b + c)}.', f'{n(a)} − {n(b + c)} = {n(a - b - c)} visitors.'], [n(a - b), n(a - b + c), n(a + b + c)])


@std(sk(AS, 3))
def as3_s(r):
    z = r.choice([10000, 20000, 50000, 100000, 300000, 600000, 1000000]); b = r.randint(z // 10, z - 1); c = r.randint(100, 999)
    return ('as3_across_zeros_then_add', f'Subtract {n(z)} − {n(b)}. Then add {n(c)} to the difference.', n(z - b + c),
            [f'Regroup across the zeros: {n(z)} − {n(b)} = {n(z - b)}.', f'{n(z - b)} + {n(c)} = {n(z - b + c)}.'], [n(z - b), n(z - b - c), n(z - b + c + 10)])


@adv(sk(AS, 3))
def as3_a(r):
    z = r.choice([5000, 10000, 40000, 100000, 500000]); x = r.randint(z // 5, z - 1)
    return ('as3_unknown_start', f'Kai subtracted a number from {n(z)} and got {n(z - x)}. Which number did Kai subtract? Check by adding.', n(x),
            [f'{n(z)} − ___ = {n(z - x)}, so the number is {n(z)} − {n(z - x)}.', f'Regroup across the zeros: {n(x)}. Check: {n(z - x)} + {n(x)} = {n(z)}.'], [n(z - x), n(x + 1000), n(x - 10)])


@std(sk(AS, 4))
def as4_s(r):
    a, b = r.randint(1000, 9999), r.randint(1000, 9999)
    e = rnd(a, 100) + rnd(b, 100)
    return ('as4_estimate_then_compare', f'Estimate {n(a)} + {n(b)} by rounding each number to the nearest hundred. How far is the estimate from the exact sum?',
            n(abs(e - (a + b))), [f'Estimate: {n(rnd(a, 100))} + {n(rnd(b, 100))} = {n(e)}. Exact: {n(a + b)}.', f'The difference is {n(abs(e - (a + b)))}.'],
            [n(e), n(a + b), n(abs(e - (a + b)) + 100)])


@adv(sk(AS, 4))
def as4_a(r):
    cost = r.choice([9500, 12000, 15000, 20000]); a, b, c = (r.randint(2100, 5900) for _ in range(3))
    est = rnd(a, 1000) + rnd(b, 1000) + rnd(c, 1000); exact = a + b + c
    need((est >= cost) != (exact >= cost))
    ans = 'yes' if exact >= cost else 'no'
    return ('as4_estimate_misleads', f'A school needs ${n(cost)}. It raised ${n(a)}, ${n(b)} and ${n(c)}. Rounding to the nearest thousand gives an estimate of ${n(est)}. Did the school really raise enough? Answer yes or no.',
            ans, [f'Exact total: {n(a)} + {n(b)} + {n(c)} = {n(exact)}.', f'${n(exact)} is {"at least" if ans == "yes" else "less than"} ${n(cost)}, so the answer is {ans}, even though the estimate says {"no" if ans == "yes" else "yes"}.'],
            ['yes' if ans == 'no' else 'no', 'cannot tell without more information', 'only if the estimate is exact'])


@std(sk(AS, 5))
def as5_s(r):
    nm = r.choice(NAMES); a = r.randint(10000, 90000); b = r.randint(1000, 9000); c = r.randint(1000, a + b - 1000)
    return ('as5_two_step_steps', f'{nm} had {n(a)} points, earned {n(b)} more, and then spent {n(c)} points on prizes. How many points are left?', n(a + b - c),
            [f'{n(a)} + {n(b)} = {n(a + b)}.', f'{n(a + b)} − {n(c)} = {n(a + b - c)} points.'], [n(a + b), n(a - b - c) if a - b - c > 0 else n(a + b + c), n(a - c)])


@adv(sk(AS, 5))
def as5_a(r):
    x = r.randint(20000, 90000); b = r.randint(5000, 20000); c = r.randint(5000, 20000); end = x + b - c; need(end > 0)
    nm = r.choice(NAMES)
    return ('as5_start_unknown_two_step', f'A library got {n(b)} new books and gave away {n(c)} old books. Now it has {n(end)} books. How many books did it have at first?', n(x),
            [f'Work backward: add back the books given away, {n(end)} + {n(c)} = {n(end + c)}.', f'Take away the new books: {n(end + c)} − {n(b)} = {n(x)}.'], [n(end + b - c), n(end + b + c), n(end - b + c + 10)])


# =============================================================== multiplication
@std(sk(MS, 1))
def ms1_s(r):
    a, k, m = r.randint(3, 12), r.randint(2, 9), r.randint(3, 15)
    nm1, nm2 = r.sample(NAMES, 2)
    return ('ms1_times_then_more', f'{nm1} has {a} stickers. {nm2} has {k} times as many. How many stickers do they have together?', str(a + a * k),
            [f'{nm2}: {k} × {a} = {a * k}.', f'Together: {a} + {a * k} = {a + a * k}.'], [str(a * k), str(a + k), str(a * k + k)])


@adv(sk(MS, 1))
def ms1_a(r):
    s, k = r.randint(4, 15), r.randint(3, 9)
    return ('ms1_difference_known', f'A red rope is {k} times as long as a blue rope. The red rope is {s * (k - 1)} feet longer than the blue rope. How long is the blue rope?', f'{s} feet',
            [f'The red rope is {k} parts and the blue rope is 1 part, so the difference is {k - 1} parts.', f'{k - 1} parts = {s * (k - 1)} feet, so 1 part = {s * (k - 1)} ÷ {k - 1} = {s} feet.'],
            [f'{s * (k - 1) // k if s * (k - 1) % k == 0 else s + 1} feet', f'{s * k} feet', f'{s * (k - 1) - k} feet'])


@std(sk(MS, 2))
def ms2_s(r):
    a, p = r.randint(2, 9), r.choice([10, 100, 1000]); b, q = r.randint(2, 9), r.choice([10, 100])
    return ('ms2_two_products', f'Find {a} × {n(p)} and {b} × {n(q)}. What is the sum of the two products?', n(a * p + b * q),
            [f'{a} × {n(p)} = {n(a * p)} and {b} × {n(q)} = {n(b * q)}.', f'{n(a * p)} + {n(b * q)} = {n(a * p + b * q)}.'], [n(a * p * b * q) if a * p * b * q < 10 ** 6 else n(a * b), n(a * p), n(a * p + b)])


@adv(sk(MS, 2))
def ms2_a(r):
    a, b = r.randint(2, 9), r.randint(2, 9); p = r.choice([10, 100]); total = a * p * b
    need(total < 1000000)
    return ('ms2_missing_multiple', f'{a} × ___ = {n(total)}. The missing number is a multiple of {p}. What is it?', n(b * p),
            [f'Think {a} × {b} = {a * b}.', f'{n(total)} is {a * b} × {n(p)}, so the missing number is {b} × {n(p)} = {n(b * p)}.'], [str(b), n(b * p * 10), n(b * p // 10) if p > 10 else str(b + 1)])


@std(sk(MS, 3))
def ms3_s(r):
    a, b, c = r.randint(105, 2499), r.randint(3, 9), r.randint(10, 99)
    nm = r.choice(['boxes', 'crates', 'packs'])
    return ('ms3_product_then_add', f'A shop has {b} {nm} with {n(a)} beads in each and {c} loose beads. How many beads are there in all?', n(a * b + c),
            [f'{b} × {n(a)} = {n(a * b)}.', f'{n(a * b)} + {c} = {n(a * b + c)} beads.'], [n(a * b), n(a * (b + c)) if a * (b + c) < 10 ** 6 else n(a + b + c), n(a * b - c)])


@adv(sk(MS, 3))
def ms3_a(r):
    a, b = r.randint(1201, 2999), r.randint(3, 9); p = r.randint(2, 9)
    need(a * b > (b + 1) * (a - p * 100))
    return ('ms3_compare_two_products', f'Theater A sold {b} shows with {n(a)} seats each. Theater B sold {b + 1} shows with {n(a - p * 100)} seats each. How many more seats did Theater A sell?',
            n(a * b - (b + 1) * (a - p * 100)), [f'A: {b} × {n(a)} = {n(a * b)}. B: {b + 1} × {n(a - p * 100)} = {n((b + 1) * (a - p * 100))}.', f'{n(a * b)} − {n((b + 1) * (a - p * 100))} = {n(a * b - (b + 1) * (a - p * 100))}.'],
            [n(p * 100 * b), n(a * b), n(abs(a * b - (b + 1) * (a - p * 100)) + 100)])


@std(sk(MS, 4))
def ms4_s(r):
    a, b = r.randint(12, 49), r.randint(12, 49); c = r.randint(50, 400); need(a * b > c)
    return ('ms4_product_then_subtract', f'There are {a} rows with {b} chairs in each row. {c} chairs are taken. How many chairs are empty?', n(a * b - c),
            [f'{a} × {b} = {n(a * b)} chairs.', f'{n(a * b)} − {c} = {n(a * b - c)} empty chairs.'], [n(a * b), n(a * b + c), n((a - 1) * b - c)])


@adv(sk(MS, 4))
def ms4_a(r):
    a, b, c, d = r.randint(11, 39), r.randint(11, 39), r.randint(11, 39), r.randint(11, 39)
    return ('ms4_two_area_models', f'Garden A is {a} feet by {b} feet. Garden B is {c} feet by {d} feet. What is the total area of the two gardens?', f'{n(a * b + c * d)} square feet',
            [f'A: {a} × {b} = {n(a * b)}. B: {c} × {d} = {n(c * d)}.', f'Total: {n(a * b)} + {n(c * d)} = {n(a * b + c * d)} square feet.'],
            [f'{n(a * b)} square feet', f'{n(2 * (a + b + c + d))} square feet', f'{n((a + c) * (b + d))} square feet'])


@std(sk(MS, 5))
def ms5_s(r):
    a, b = r.randint(21, 89), r.randint(21, 89); need(a % 10 and b % 10)
    e = rnd(a, 10) * rnd(b, 10)
    return ('ms5_estimate_then_exact', f'Estimate {a} × {b} by rounding each factor to the nearest ten. Then find the exact product. How far apart are they?',
            n(abs(e - a * b)), [f'Estimate: {rnd(a, 10)} × {rnd(b, 10)} = {n(e)}. Exact: {a} × {b} = {n(a * b)}.', f'Difference: {n(abs(e - a * b))}.'], [n(e), n(a * b), n(abs(e - a * b) + 100)])


@adv(sk(MS, 5))
def ms5_a(r):
    p, k, b = r.randint(12, 48), r.randint(12, 30), r.choice([500, 600, 700, 800, 900, 1000])
    cost = p * k; need(cost != b)
    ans = f'${n(abs(b - cost))} {"left" if b > cost else "short"}'
    return ('ms5_budget', f'A class has ${n(b)}. Tickets cost ${p} each, and {k} students need tickets. How much money is left over, or how much more is needed?', ans,
            [f'Cost: {k} × ${p} = ${n(cost)}.', f'${n(b)} − ${n(cost)}: {"$" + n(b - cost) + " left" if b > cost else "they are $" + n(cost - b) + " short"}.'],
            [f'${n(cost)} {"left" if b > cost else "short"}', f'${n(abs(b - cost))} {"short" if b > cost else "left"}', f'${n(abs(b - cost) + p)} {"left" if b > cost else "short"}'])


# =============================================================== division
@std(sk(DV, 1))
def dv1_s(r):
    d, q, p = r.randint(2, 9), r.randint(2, 9), r.choice([10, 100])
    return ('dv1_fact_then_extend', f'You know {d} × {q} = {d * q}. Use it to find {n(d * q * p)} ÷ {d}. Then find {n(d * q * p)} ÷ {q}.', f'{n(q * p)}; {n(d * p)}',
            [f'{n(d * q * p)} is {d * q} {PLACE[p]}, so {n(d * q * p)} ÷ {d} = {q} {PLACE[p]} = {n(q * p)}.', f'In the same way, {n(d * q * p)} ÷ {q} = {d} {PLACE[p]} = {n(d * p)}.'],
            [f'{q}; {d}', f'{n(q * p * 10)}; {n(d * p * 10)}', f'{n(d * p)}; {n(q * p)}'])


@adv(sk(DV, 1))
def dv1_a(r):
    d, q, p = r.randint(3, 9), r.randint(3, 9), 100; k = r.randint(2, 5)
    total = d * q * p; need((q * p) % k == 0)
    return ('dv1_share_then_group', f'{n(total)} beads are shared equally among {d} bins. Each bin\'s beads are then split equally into {k} bags. How many beads go in each bag?',
            n(q * p // k),
            [f'{n(total)} ÷ {d} = {n(q * p)} in each bin.', f'{n(q * p)} ÷ {k} = {n(q * p // k)} in each bag.'], [n(q * p), n(total // k), n(q * p // k * 10)])


@std(sk(DV, 2))
def dv2_s(r):
    d = r.randint(3, 9); q1, q2 = r.choice([10, 20, 30, 40, 50]), r.randint(2, 9); total = d * (q1 + q2)
    return ('dv2_partial_quotients_full', f'Use partial quotients to find {total} ÷ {d}: first take away {d} × {q1}. What is left, and what is the quotient?', f'{d * q2}; {q1 + q2}',
            [f'{d} × {q1} = {d * q1}, and {total} − {d * q1} = {d * q2}.', f'{d * q2} ÷ {d} = {q2}, so the quotient is {q1} + {q2} = {q1 + q2}.'],
            [f'{d * q2}; {q2}', f'{d * q1}; {q1 + q2}', f'{d * q2}; {q1 + q2 + 1}'])


@adv(sk(DV, 2))
def dv2_a(r):
    d = r.randint(3, 9); a1, a2 = r.choice([100, 200, 300]), r.choice([10, 20, 40, 60]); a3 = r.randint(2, 9); total = d * (a1 + a2 + a3)
    need(total < 10000)
    return ('dv2_area_model_three', f'An area model for {n(total)} ÷ {d} has a side of {d} and three sections with areas {n(d * a1)}, {n(d * a2)} and {d * a3}. What is the quotient?', n(a1 + a2 + a3),
            [f'Divide each area by {d}: {a1}, {a2} and {a3}.', f'{a1} + {a2} + {a3} = {a1 + a2 + a3}.'], [n(a1 + a2), n(d * (a1 + a2 + a3)), n(a1 + a2 + a3 + 10)])


@std(sk(DV, 3))
def dv3_s(r):
    d, q = r.randint(3, 9), r.randint(112, 999); total = d * q; need(total < 10000)
    return ('dv3_divide_then_check', f'Divide {n(total)} ÷ {d}. Then check by multiplying. What is the quotient?', n(q),
            [f'Divide one place at a time: {n(total)} ÷ {d} = {n(q)}.', f'Check: {n(q)} × {d} = {n(total)}.'], [n(q + 1), n(q * 10) if q * 10 < 10000 else n(q - 10), n(q - 1)])


@adv(sk(DV, 3))
def dv3_a(r):
    d, q, k = r.randint(3, 9), r.randint(105, 950), r.randint(2, 6); total = d * q; need(total < 10000 and q % (k + 1) == 0)
    return ('dv3_divide_then_compare', f'A farm packed {n(total)} apples into bags of {d}. It sold {k} times as many bags on Saturday as on Sunday, and every bag was sold on those two days. How many bags were sold on Sunday?',
            n(q // (k + 1)),
            [f'Bags: {n(total)} ÷ {d} = {n(q)}.', f'Sunday is 1 part and Saturday is {k} parts: {k + 1} parts = {n(q)}, so Sunday = {n(q)} ÷ {k + 1} = {n(q // (k + 1))} bags.'],
            [n(q), n(q // k) if q % k == 0 else n(q // (k + 1) + 1), n(q // (k + 1) * k)])


@std(sk(DV, 4))
def dv4_s(r):
    d = r.randint(3, 9); q = r.randint(12, 299); rem = r.randint(1, d - 1); total = d * q + rem
    return ('dv4_remainder_then_check', f'Divide {n(total)} ÷ {d}. Write the answer as a quotient and remainder, and check by multiplying and adding.', f'{q} R {rem}',
            [f'{n(total)} ÷ {d} = {q} R {rem}.', f'Check: {q} × {d} + {rem} = {n(total)}.'], [f'{q} R {rem + 1}', f'{q + 1} R {rem}', f'{q - 1} R {rem + d}'])


@adv(sk(DV, 4))
def dv4_a(r):
    d = r.randint(4, 9); q = r.randint(20, 120); rem = r.randint(1, d - 1); k = d - rem
    return ('dv4_least_to_add', f'What is the least number you can add to {n(d * q + rem)} so that it divides by {d} with no remainder?', str(k),
            [f'{n(d * q + rem)} ÷ {d} = {q} R {rem}.', f'The next multiple of {d} is {n(d * (q + 1))}, so add {n(d * (q + 1))} − {n(d * q + rem)} = {k}.'], [str(rem), str(d), str(k + 1)])


@std(sk(DV, 5))
def dv5_s(r):
    per, groups = r.randint(4, 9), r.randint(6, 25); rem = r.randint(1, per - 1); total = per * groups + rem
    return ('dv5_round_up_then_spare', f'{total} students ride vans that hold {per} students each. How many vans are needed, and how many empty seats are in the last van?', f'{groups + 1} vans; {qty(per - rem, "empty seats")}',
            [f'{total} ÷ {per} = {groups} R {rem}.', f'The {rem} extra students need one more van: {groups + 1} vans. That van has {per} − {rem} = {per - rem} empty seats.'],
            [f'{groups} vans; {qty(rem, "empty seats")}', f'{groups + 1} vans; {qty(rem, "empty seats")}' if rem != per - rem else f'{groups + 2} vans; {qty(rem, "empty seats")}', f'{groups} vans; {qty(per - rem, "empty seats")}'])


@adv(sk(DV, 5))
def dv5_a(r):
    per, price = r.randint(4, 8), r.randint(3, 9); groups = r.randint(8, 30); rem = r.randint(1, per - 1); total = per * groups + rem
    return ('dv5_cost_with_remainder', f'Juice boxes come in packs of {per}. Each pack costs ${price}. A class needs {total} juice boxes. What is the least it can spend?', f'${n((groups + 1) * price)}',
            [f'{total} ÷ {per} = {groups} R {rem}, so {groups + 1} packs are needed.', f'{groups + 1} × ${price} = ${n((groups + 1) * price)}.'],
            [f'${n(groups * price)}', f'${n(total * price)}', f'${n((groups + 2) * price)}'])


# =============================================================== factors, multiples, patterns
@std(sk(FM, 1))
def fm1_s(r):
    k = r.choice([12, 16, 18, 20, 24, 28, 30, 32, 36, 40, 42, 45, 48, 50, 54, 56, 60, 63, 64, 72, 75, 80, 84, 90, 96, 100])
    fs = factors(k)
    return ('fm1_count_and_sum_pairs', f'List the factor pairs of {k}. How many factors does {k} have?', str(len(fs)),
            [f'Factor pairs: {"; ".join(f"{a} × {k // a}" for a in fs if a * a <= k)}.', f'The factors are {", ".join(map(str, fs))}: {len(fs)} factors.'], [str(len(fs) - 1), str(len(fs) // 2), str(len(fs) + 1)])


@adv(sk(FM, 1))
def fm1_a(r):
    k = r.choice([24, 30, 36, 40, 48, 60, 72, 84, 90, 96]); lo = r.randint(3, 6)
    good = [d for d in factors(k) if lo <= d <= k // lo]
    return ('fm1_rows_range', f'{k} chairs are set up in equal rows with no chairs left over. Each row must have at least {lo} chairs, and there must be at least {lo} rows. How many different numbers of rows are possible?', str(len(good)),
            [f'The number of rows must be a factor of {k}, with {k} ÷ rows also at least {lo}.', f'Possible rows: {", ".join(map(str, good))}. That is {len(good)}.'], [str(len(factors(k))), str(len(good) + 1), str(max(1, len(good) - 1))])


@std(sk(FM, 2))
def fm2_s(r):
    a, b = r.sample([2, 3, 4, 5, 6, 8, 9, 10], 2); lim = r.choice([40, 50, 60, 80, 100])
    both = [x for x in range(1, lim + 1) if x % a == 0 and x % b == 0]; need(len(both) >= 1)
    return ('fm2_common_multiples', f'How many numbers from 1 to {lim} are multiples of both {a} and {b}?', str(len(both)),
            [f'Multiples of {a} that are also multiples of {b}: {", ".join(map(str, both))}.', f'There are {len(both)}.'], [str(lim // a), str(lim // b), str(len(both) + 1)])


@adv(sk(FM, 2))
def fm2_a(r):
    a, b = r.choice([(4, 6), (6, 8), (3, 4), (5, 6), (4, 10), (6, 9), (8, 12), (2, 3), (3, 5), (4, 5), (5, 8), (6, 10), (10, 15), (9, 12), (12, 15), (3, 8)])
    l = a * b // math.gcd(a, b)
    return ('fm2_both_schedules', f'Bus A leaves every {a} minutes and Bus B every {b} minutes. Both leave at 8:00. After how many minutes do they next leave together?', f'{l} minutes',
            [f'Multiples of {a}: {", ".join(str(a * i) for i in range(1, l // a + 1))}.', f'The first one that is also a multiple of {b} is {l}, so {l} minutes.'], [f'{a * b} minutes' if a * b != l else f'{l + a} minutes', f'{a + b} minutes', f'{max(a, b)} minutes'])


@std(sk(FM, 3))
def fm3_s(r):
    lo = r.randint(10, 60); hi = lo + r.randint(8, 20); hi = min(hi, 100)
    ps = [p for p in PRIMES if lo < p < hi]; cs = [c for c in range(lo + 1, hi) if c not in ps]
    return ('fm3_count_composite', f'How many composite numbers are between {lo} and {hi}?', str(len(cs)),
            [f'Primes between {lo} and {hi}: {", ".join(map(str, ps)) or "none"}.', f'There are {hi - lo - 1} numbers between them, so {hi - lo - 1} − {len(ps)} = {len(cs)} are composite.'], [str(len(ps)), str(hi - lo - 1), str(len(cs) + 1)])


@adv(sk(FM, 3))
def fm3_a(r):
    p, q = r.sample([p for p in PRIMES if p < 15], 2); k = p * q; need(k <= 100)
    return ('fm3_prime_pair_product', f'A number between 1 and 100 is the product of two different prime numbers, {p} and another prime. It is {k}. How many factors does {k} have, and is it prime or composite?', '4 factors; composite',
            [f'{k} = {p} × {q}.', f'Its factors are 1, {min(p, q)}, {max(p, q)} and {k}: 4 factors, so it is composite.'], ['2 factors; prime', '3 factors; composite', f'{k} factors; composite'])


@std(sk(FM, 4))
def fm4_s(r):
    s, a = r.randint(3, 30), r.randint(3, 12); k = r.randint(6, 9)
    seq = [s + a * i for i in range(4)]
    return ('fm4_rule_then_term', f'A pattern starts {", ".join(map(str, seq))}, ... What is the rule, and what is the {ORD[k - 1]} number?', f'add {a}; {s + a * (k - 1)}',
            [f'Each number is {a} more than the one before: add {a}.', f'The {ORD[k - 1]} number is {s} + {k - 1} × {a} = {s + a * (k - 1)}.'], [f'add {a}; {s + a * k}', f'add {a}; {s + a * (k - 2)}', f'multiply by {a}; {s + a * (k - 1)}'])


@adv(sk(FM, 4))
def fm4_a(r):
    s, a = r.randint(2, 20), r.randint(3, 9); t = r.randint(60, 200)
    k = next(i for i in range(1, 100) if s + a * (i - 1) > t)
    return ('fm4_first_over', f'A pattern starts at {s} and adds {a} each time. Which number in the pattern is the first one greater than {t}? Give the number.', str(s + a * (k - 1)),
            [f'The numbers are {s}, {s + a}, {s + 2 * a}, ... (start plus a multiple of {a}).', f'{s + a * (k - 2)} is not greater than {t}, but {s + a * (k - 1)} is.'], [str(s + a * (k - 2)), str(t + 1), str(s + a * k)])


@std(sk(FM, 5))
def fm5_s(r):
    shapes = r.sample(['circle', 'square', 'triangle', 'star', 'heart', 'hexagon'], 3); unit = shapes + [shapes[r.randrange(3)]]
    k = r.randint(15, 40); cnt = sum(1 for i in range(k) if unit[i % 4] == shapes[0])
    return ('fm5_count_in_first', f'A pattern repeats {", ".join(unit)}. How many {shapes[0]}s are in the first {k} shapes?', str(cnt),
            [f'Each repeat has 4 shapes with {unit.count(shapes[0])} {shapes[0]}{"s" if unit.count(shapes[0]) > 1 else ""}. {k} shapes = {k // 4} full repeats and {k % 4} more.',
             f'{k // 4} × {unit.count(shapes[0])} = {k // 4 * unit.count(shapes[0])}, plus {cnt - k // 4 * unit.count(shapes[0])} in the extra shapes: {cnt}.'], [str(k // 4), str(cnt + 1), str(k // 3)])


@adv(sk(FM, 5))
def fm5_a(r):
    s, a = r.randint(3, 8), r.randint(2, 5); k = r.randint(10, 20)
    return ('fm5_tiles_total', f'Figure 1 has {s} tiles, and each figure has {a} more tiles than the one before. How many tiles are used to build Figures 1 through 5 together?', str(5 * s + 10 * a),
            [f'The figures have {", ".join(str(s + a * i) for i in range(5))} tiles.', f'Add them: {5 * s + 10 * a} tiles.'], [str(s + 4 * a), str(5 * s + 15 * a), str(5 * s)])


# =============================================================== equivalent fractions
DEN = [2, 3, 4, 5, 6, 8, 10, 12]


@std(sk(FE, 1))
def fe1_s(r):
    b = r.choice([2, 3, 4, 5, 6]); a = r.randint(1, b - 1); k = r.choice([2, 3, 4]); need(b * k <= 12 or b * k == 100)
    return ('fe1_split_then_name', f'A bar shows {a}/{b} shaded. Each part is split into {k} equal pieces. How many pieces are shaded now, and what fraction is that?', f'{a * k}; {a * k}/{b * k}',
            [f'Each of the {a} shaded parts becomes {k} pieces: {a} × {k} = {a * k}.', f'There are {b} × {k} = {b * k} pieces in all, so the fraction is {a * k}/{b * k}.'],
            [f'{a * k}; {a * k}/{b}', f'{a + k}; {a + k}/{b + k}', f'{a}; {a}/{b * k}'])


@adv(sk(FE, 1))
def fe1_a(r):
    b = r.choice([2, 3, 4, 6]); a = r.randint(1, b - 1); k1, k2 = r.sample([2, 3, 4], 2); need(b * k1 <= 12 and b * k2 <= 12)
    nm1, nm2 = r.sample(NAMES, 2)
    return ('fe1_same_amount_different_pieces', f'{nm1} cut a pan of bars into {b * k1} equal pieces and ate {a * k1}. {nm2} cut the same size pan into {b * k2} equal pieces. How many pieces must {nm2} eat to eat the same amount?', str(a * k2),
            [f'{a * k1}/{b * k1} = {a}/{b}.', f'{a}/{b} = {a * k2}/{b * k2}, so {nm2} must eat {a * k2} pieces.'], [str(a * k1), str(a), str(a * k2 + 1)])


@std(sk(FE, 2))
def fe2_s(r):
    b = r.choice([2, 3, 4, 5, 6]); a = r.randint(1, b - 1); k = r.choice([2, 3, 4]); need(b * k <= 12)
    m = r.choice([k2 for k2 in (2, 3, 4) if k2 != k and b * k2 <= 12] or [0]); need(m)
    return ('fe2_two_equivalents', f'Write two fractions equivalent to {a}/{b}: one with denominator {b * k} and one with denominator {b * m}.', f'{a * k}/{b * k}, {a * m}/{b * m}',
            [f'Multiply the numerator and denominator by {k}: {a * k}/{b * k}.', f'Multiply them by {m}: {a * m}/{b * m}.'], [f'{a + k}/{b * k}, {a + m}/{b * m}', f'{a * k}/{b * k}, {a * k}/{b * m}', f'{a}/{b * k}, {a}/{b * m}'])


@adv(sk(FE, 2))
def fe2_a(r):
    b = r.choice([2, 3, 4, 5, 6]); a = r.randint(1, b - 1); k = r.choice([2, 3, 4, 5, 6]); need(math.gcd(a, b) == 1 and b * k <= 12)
    s = a * k + b * k
    return ('fe2_from_sum', f'A fraction is equivalent to {a}/{b}. Its numerator and denominator add up to {s}. What is the fraction?', f'{a * k}/{b * k}',
            [f'Fractions equal to {a}/{b} look like {a}×k / {b}×k, and the parts add to {a + b}×k.', f'{a + b} × k = {s}, so k = {k} and the fraction is {a * k}/{b * k}.'], [f'{a * (k + 1)}/{b * (k + 1)}', f'{a}/{s - a}', f'{b * k}/{a * k}'])


@std(sk(FE, 3))
def fe3_s(r):
    b = r.choice([5, 6, 8, 10, 12]); xs = r.sample(range(1, b), 3)
    srt = sorted(xs)
    return ('fe3_three_like', f'Order from least to greatest: {", ".join(f"{x}/{b}" for x in xs)}. Then find the difference between the greatest and the least.', f'{srt[2] - srt[0]}/{b}',
            [f'Same denominator: compare numerators. {", ".join(f"{x}/{b}" for x in srt)}.', f'{srt[2]}/{b} − {srt[0]}/{b} = {srt[2] - srt[0]}/{b}.'], [f'{srt[2] - srt[1]}/{b}', f'{srt[2] + srt[0]}/{b}', f'{srt[2] - srt[0]}/{b * 2}'])


DNAME = {2: 'halves', 3: 'thirds', 4: 'fourths', 5: 'fifths', 6: 'sixths', 8: 'eighths', 10: 'tenths', 12: 'twelfths'}


@adv(sk(FE, 3))
def fe3_a(r):
    a = r.randint(2, 5); b1, b2 = r.sample([3, 4, 5, 6, 8, 10, 12], 2); need(a < min(b1, b2))
    nm1, nm2 = r.sample(NAMES, 2)
    big, small = (nm1, nm2) if b1 < b2 else (nm2, nm1)
    return ('fe3_same_numerator_story', f'{nm1} ate {a}/{b1} of a pizza. {nm2} ate {a}/{b2} of a pizza of the same size. Who ate more, and why?',
            f'{big}, because {DNAME[min(b1, b2)]} are bigger pieces than {DNAME[max(b1, b2)]}',
            [f'Both ate {a} pieces, so compare the size of the pieces.', f'A whole cut into {min(b1, b2)} parts has bigger parts than one cut into {max(b1, b2)}, so {big} ate more.'],
            [f'{small}, because {max(b1, b2)} is greater than {min(b1, b2)}', 'They ate the same amount, because the numerators are equal', f'{small}, because the pizza was cut into more pieces'])


@std(sk(FE, 4))
def fe4_s(r):
    def pick():
        b = r.choice([3, 4, 5, 6, 8, 10, 12]); a = r.randint(1, b - 1); need(2 * a != b); return a, b
    (a1, b1), (a2, b2) = pick(), pick(); need((2 * a1 > b1) != (2 * a2 > b2))
    sym = '>' if Fr(a1, b1) > Fr(a2, b2) else '<'
    return ('fe4_benchmark_explain', f'Use 1/2 to compare {a1}/{b1} and {a2}/{b2}. Write <, > or = for {a1}/{b1} ___ {a2}/{b2}.', sym,
            [f'{a1}/{b1} is {"more" if 2 * a1 > b1 else "less"} than 1/2 because {a1} is {"more" if 2 * a1 > b1 else "less"} than half of {b1}.',
             f'{a2}/{b2} is {"more" if 2 * a2 > b2 else "less"} than 1/2, so {a1}/{b1} {sym} {a2}/{b2}.'], ['<' if sym == '>' else '>', '=', 'cannot tell'])


@adv(sk(FE, 4))
def fe4_a(r):
    fs = []
    while len(fs) < 5:
        b = r.choice([3, 4, 5, 6, 8, 10, 12]); a = r.randint(1, b - 1)
        if Fr(a, b) != Fr(1, 2) and f'{a}/{b}' not in fs:
            fs.append(f'{a}/{b}')
    more = [f for f in fs if Fr(f) > Fr(1, 2)]; need(1 <= len(more) <= 4)
    return ('fe4_count_more_than_half', f'How many of these fractions are greater than 1/2: {", ".join(fs)}?', str(len(more)),
            ['A fraction is greater than 1/2 when its numerator is more than half its denominator.', f'Greater than 1/2: {", ".join(more)}. That is {len(more)}.'], [str(x) for x in range(6) if x != len(more)])


@std(sk(FE, 5))
def fe5_s(r):
    fs = set()
    while len(fs) < 3:
        b = r.choice([2, 3, 4, 6, 12]); a = r.randint(1, b - 1); fs.add((a, b))
    fs = list(fs); need(len({Fr(a, b) for a, b in fs}) == 3)
    srt = sorted(fs, key=lambda x: Fr(*x))
    return ('fe5_order_using_twelfths', f'Order from least to greatest by writing each fraction in twelfths: {", ".join(f"{a}/{b}" for a, b in fs)}.', ', '.join(f'{a}/{b}' for a, b in srt),
            [f'In twelfths: {", ".join(f"{a}/{b} = {a * 12 // b}/12" for a, b in fs)}.', f'Least to greatest: {", ".join(f"{a}/{b}" for a, b in srt)}.'],
            [', '.join(f'{a}/{b}' for a, b in perm) for perm in __import__('itertools').permutations(srt) if list(perm) != srt])


@adv(sk(FE, 5))
def fe5_a(r):
    b1, b2 = r.sample([2, 3, 4, 6], 2); a1, a2 = r.randint(1, b1 - 1), r.randint(1, b2 - 1)
    x, y = Fr(a1, b1), Fr(a2, b2); need(x != y)
    lo, hi = min(x, y), max(x, y)
    between = [k for k in range(1, 12) if lo < Fr(k, 12) < hi]; need(between)
    return ('fe5_twelfths_between', f'How many fractions with denominator 12 are greater than {a1}/{b1} and less than {a2}/{b2}?' if x < y else f'How many fractions with denominator 12 are greater than {a2}/{b2} and less than {a1}/{b1}?',
            str(len(between)), [f'In twelfths: {a1}/{b1} = {a1 * 12 // b1}/12 and {a2}/{b2} = {a2 * 12 // b2}/12.', f'Between them: {", ".join(f"{k}/12" for k in between)}. That is {len(between)}.'],
            [str(x) for x in (len(between) + 1, len(between) + 2, len(between) - 1, len(between) + 3) if x >= 0])


# =============================================================== fraction operations and decimals
@std(sk(FD, 1))
def fd1_s(r):
    b = r.choice([4, 5, 6, 8, 10, 12]); a = r.randint(3, b - 1); x = r.randint(1, a - 2)
    return ('fd1_three_part_sum', f'Fill in the blank: {a}/{b} = {x}/{b} + 1/{b} + ___', f'{a - x - 1}/{b}',
            [f'{x}/{b} + 1/{b} = {x + 1}/{b}.', f'{a}/{b} − {x + 1}/{b} = {a - x - 1}/{b}.'], [f'{a - x}/{b}', f'{a + x + 1}/{b}', f'{a - x - 1}/{b * 2}'])


@adv(sk(FD, 1))
def fd1_a(r):
    b = r.choice([5, 6, 8, 10]); w = r.randint(1, 2); a = r.randint(1, b - 1)
    total = w * b + a
    return ('fd1_mixed_unit_count', f'{w} {a}/{b} is how many copies of 1/{b}? Write {w} {a}/{b} as a sum of a whole-number fraction and {a}/{b}.', f'{total}; {w * b}/{b} + {a}/{b}',
            [f'1 whole = {b}/{b}, so {w} wholes = {w * b}/{b}.', f'{w * b}/{b} + {a}/{b} = {total}/{b}: {total} copies of 1/{b}.'], [f'{w + a}; {w}/{b} + {a}/{b}', f'{total}; {w}/{b} + {a}/{b}', f'{w * a}; {w * b}/{b} + {a}/{b}'])


@std(sk(FD, 2))
def fd2_s(r):
    b = r.choice([5, 6, 8, 10, 12]); x, y = r.randint(1, b - 2), r.randint(1, b - 2); z = r.randint(1, x + y - 1); need(0 < x + y - z < b)
    nm = r.choice(NAMES)
    return ('fd2_add_then_subtract', f'{nm} had {x}/{b} of a jug of juice and added {y}/{b} of a jug more. Then {nm} poured out {z}/{b} of a jug. How much of the jug is full now?', f'{x + y - z}/{b}',
            [f'{x}/{b} + {y}/{b} = {x + y}/{b}.', f'{x + y}/{b} − {z}/{b} = {x + y - z}/{b}.'], [f'{x + y}/{b}', f'{x + y + z}/{b}', f'{x + y - z}/{3 * b}'])


@adv(sk(FD, 2))
def fd2_a(r):
    b = r.choice([6, 8, 10, 12]); x, y = r.randint(1, b // 2), r.randint(1, b // 2); need(x + y < b)
    left = b - x - y
    return ('fd2_rest_of_whole', f'A garden is split into {b} equal beds. {x}/{b} of the garden is beans and {y}/{b} is corn. The rest is flowers. What fraction of the garden is flowers?', f'{left}/{b}',
            [f'The whole garden is {b}/{b}.', f'{b}/{b} − {x}/{b} − {y}/{b} = {left}/{b}.'], [f'{x + y}/{b}', f'{left}/{b * 2}', f'{left + 1}/{b}'])


@std(sk(FD, 3))
def fd3_s(r):
    b = r.choice([3, 4, 5, 6, 8]); w1, w2 = r.randint(1, 5), r.randint(1, 4); a1, a2 = r.randint(1, b - 1), r.randint(1, b - 1); need(a1 + a2 > b)
    s = Fr(w1 * b + a1 + w2 * b + a2, b)
    return ('fd3_add_with_regroup', f'Add {w1} {a1}/{b} + {w2} {a2}/{b}. Regroup so the fraction part is less than 1.', F(s),
            [f'Add the wholes and the parts: {w1 + w2} {a1 + a2}/{b}.', f'{a1 + a2}/{b} = 1 {a1 + a2 - b}/{b}, so the sum is {F(s)}.'], [f'{w1 + w2} {a1 + a2}/{b}', f'{w1 + w2} {a1 + a2 - b}/{b}', F(s + 1)])


@adv(sk(FD, 3))
def fd3_a(r):
    b = r.choice([4, 6, 8, 10]); total = r.randint(6, 12); w1, a1 = r.randint(1, 3), r.randint(1, b - 1); w2, a2 = r.randint(1, 3), r.randint(1, b - 1)
    used = Fr(w1 * b + a1, b) + Fr(w2 * b + a2, b); need(used < total)
    return ('fd3_two_cuts_left', f'A board is {total} feet long. Rosa cuts off {w1} {a1}/{b} feet and then {w2} {a2}/{b} feet. How long is the board now?', qty(F(total - used), 'feet'),
            [f'Cut off in all: {w1} {a1}/{b} + {w2} {a2}/{b} = {F(used)} feet.', f'{total} − {F(used)} = {F(total - used)} feet.'], [qty(F(used), 'feet'), qty(F(total - used + 1), 'feet'), qty(F(total - Fr(w1 * b + a1, b)), 'feet')])


@std(sk(FD, 4))
def fd4_s(r):
    b = r.choice([3, 4, 5, 6, 8, 10, 12]); a = r.randint(1, b - 1); k = r.randint(3, 9); need(a * k > b)
    p = Fr(a * k, b); ans = str(a * k // b) if (a * k) % b == 0 else f'{(a * k) // b} {(a * k) % b}/{b}'
    return ('fd4_multiply_then_mixed', f'Multiply {k} × {a}/{b}. Write the product as a whole number or a mixed number.', ans,
            [f'{k} × {a}/{b} = {a * k}/{b}.', f'{a * k}/{b} = {ans}.'], [f'{a * k}/{b * k}', f'{k + a}/{b}', str(a * k // b + 1)])


@adv(sk(FD, 4))
def fd4_a(r):
    b = r.choice([3, 4, 8]); a = r.randint(1, b - 1); k = r.randint(4, 12); have = r.randint(2, 6)
    need_ = Fr(a * k, b); need(need_ > have)
    short = need_ - have
    return ('fd4_enough', f'A recipe uses {a}/{b} cup of oats for each batch. Jonah makes {k} batches and has {have} cups of oats. How many more cups of oats does Jonah need?', f'{F(short)} cups' if short != 1 else '1 cup',
            [f'Oats needed: {k} × {a}/{b} = {a * k}/{b} = {F(need_)} cups.', f'{F(need_)} − {have} = {F(short)}.'], [f'{F(need_)} cups', f'{F(short + 1)} cups', f'{F(Fr(a, b) * (k - have)) if k > have else F(short + Fr(1, b))} cups'])


@std(sk(FD, 5))
def fd5_s(r):
    t, h = r.randint(1, 9), r.randint(1, 9)
    v = Fr(t, 10) + Fr(h, 100)
    return ('fd5_tenths_plus_hundredths', f'Add {t}/10 + {h}/100. Write the sum as a fraction with denominator 100 and as a decimal.', f'{t * 10 + h}/100; {float(v):.2f}',
            [f'{t}/10 = {t * 10}/100, so {t * 10}/100 + {h}/100 = {t * 10 + h}/100.', f'{t * 10 + h}/100 = {float(v):.2f}.'], [f'{t + h}/100; 0.{t + h:02d}' if t + h < 100 else f'{t + h}/110; 0.{t + h}', f'{t + h}/110; {float(v):.2f}', f'{t * 10 + h}/100; {t}.{h}'])


@adv(sk(FD, 5))
def fd5_a(r):
    d, p = r.randint(1, 8), r.randint(11, 19); v = 10 * d + p; need(v < 100)
    nm = r.choice(NAMES)
    return ('fd5_coins_decimal', f'{nm} has {d} dimes and {p} pennies. A dime is 1/10 of a dollar and a penny is 1/100 of a dollar. What decimal part of a dollar does {nm} have?', f'0.{v:02d}',
            [f'{d} dimes = {d}/10 = {10 * d}/100. {p} pennies = {p}/100.', f'{10 * d}/100 + {p}/100 = {v}/100 = 0.{v:02d}.'], [f'0.{d + p:02d}', f'{d}.{p}', f'0.{v + 10:02d}' if v + 10 < 100 else f'0.{v - 10:02d}'])


@std(sk(FD, 6))
def fd6_s(r):
    xs = sorted({r.randint(1, 99) for _ in range(4)}); need(len(xs) == 4)
    ds = [f'0.{x:02d}' if x % 10 else f'0.{x // 10}' for x in xs]
    r.shuffle(ds); srt = sorted(ds, key=float)
    return ('fd6_order_four', f'Order from least to greatest: {", ".join(ds)}.', ', '.join(srt),
            ['Write each decimal in hundredths so they are easy to compare.', f'Least to greatest: {", ".join(srt)}.'], [', '.join(srt[::-1]), ', '.join(sorted(ds, key=len)), ', '.join(sorted(ds))] if ', '.join(sorted(ds)) != ', '.join(srt) else [', '.join(srt[::-1]), ', '.join(sorted(ds, key=len)), ', '.join(srt[1:] + srt[:1])])


@adv(sk(FD, 6))
def fd6_a(r):
    v = sorted(r.sample(range(30, 96), 3)); need(v[2] - v[0] >= 5)
    forms = [f'{v[0] / 100:.2f}', f'{v[1]}/100', f'{v[2] // 10}/10 + {v[2] % 10}/100' if v[2] % 10 else f'{v[2] // 10}/10']
    who = r.sample(NAMES, 3); order = list(range(3)); r.shuffle(order)
    text = '; '.join(f'{who[i]} ran {forms[k]} mile' for i, k in enumerate(order))
    return ('fd6_mixed_forms_difference', f'Three runners: {text}. How much farther did the one who ran the farthest run than the one who ran the shortest? Write a decimal.', f'{(v[2] - v[0]) / 100:.2f}',
            [f'Write each as hundredths: {v[0] / 100:.2f}, {v[1] / 100:.2f} and {v[2] / 100:.2f}.', f'{v[2] / 100:.2f} − {v[0] / 100:.2f} = {(v[2] - v[0]) / 100:.2f} mile.'],
            [f'{(v[2] - v[1]) / 100:.2f}', f'{(v[1] - v[0]) / 100:.2f}', f'{(v[2] + v[0]) / 100:.2f}' if v[2] + v[0] < 100 else f'{(v[2] - v[0]) / 10:.1f}'])

# =============================================================== measurement
CONV = [('feet', 'inches', 12), ('yards', 'feet', 3), ('yards', 'inches', 36), ('pounds', 'ounces', 16), ('gallons', 'quarts', 4), ('quarts', 'pints', 2), ('pints', 'cups', 2), ('hours', 'minutes', 60), ('minutes', 'seconds', 60), ('days', 'hours', 24)]
METRIC = [('meters', 'centimeters', 100), ('kilometers', 'meters', 1000), ('centimeters', 'millimeters', 10), ('kilograms', 'grams', 1000), ('liters', 'milliliters', 1000)]


@std(sk(MC, 1))
def mc1_s(r):
    big, small, k = r.choice(CONV[:7]); a, b = r.randint(2, 9), r.randint(1, k - 1); c = r.randint(1, a * k // 2)
    nm = r.choice(NAMES)
    return ('mc1_mixed_then_use', f'{nm} has {a} {big} {b} {small} of {THING[small]} and uses {c} {small}. How many {small} are left?', f'{a * k + b - c} {small}',
            [f'{a} {big} {b} {small} = {a} × {k} + {b} = {a * k + b} {small}.', f'{a * k + b} − {c} = {a * k + b - c} {small}.'], [f'{a * k + b} {small}', f'{a + b - c if a + b > c else a * k - c} {small}', f'{a * k - c} {small}'])


@adv(sk(MC, 1))
def mc1_a(r):
    big, small, k = r.choice(CONV[:7]); a = r.randint(3, 9); p = r.choice([2, 3, 4, 6]); need((a * k) % p == 0)
    return ('mc1_convert_then_share', f'{a} {big} of {THING[small]} is shared equally into {p} parts. How many {small} is each part?', f'{a * k // p} {small}',
            [f'{a} {big} = {a} × {k} = {a * k} {small}.', f'{a * k} ÷ {p} = {a * k // p} {small}.'], [f'{a * k} {small}', f'{F(Fr(a, p))} {small}', f'{a * k // p + k} {small}'])


@std(sk(MC, 2))
def mc2_s(r):
    big, small, k = r.choice(METRIC); a, b = r.randint(2, 9), r.randint(1, k - 1)
    c = r.randint(1, (a * k + b) // 2)
    return ('mc2_convert_then_subtract', f'A shop has {a} {big} {b} {small} of {THING[small]}. {c} {small} are used. How many {small} are left?', f'{n(a * k + b - c)} {small}',
            [f'{a} {big} {b} {small} = {n(a * k)} + {b} = {n(a * k + b)} {small}.', f'{n(a * k + b)} − {c} = {n(a * k + b - c)} {small}.'], [f'{n(a * k + b)} {small}', f'{n(a * k - c)} {small}', f'{n(a + b - c) if a + b > c else n(a * k + b + c)} {small}'])


@adv(sk(MC, 2))
def mc2_a(r):
    big, small, k = r.choice(METRIC[:2] + METRIC[3:]); a = r.randint(2, 6); laps = r.randint(3, 8); per = r.randint(100, 900) if k == 1000 else r.randint(20, 90)
    need(a * k > laps * per)
    return ('mc2_how_much_more', f'Nora needs {a} {big} of {THING[small]}. She has {laps} pieces that are each {per} {small}. How many more {small} does she need?', f'{n(a * k - laps * per)} {small}',
            [f'She has {laps} × {per} = {n(laps * per)} {small}. She needs {a} × {n(k)} = {n(a * k)} {small}.', f'{n(a * k)} − {n(laps * per)} = {n(a * k - laps * per)} {small}.'],
            [f'{n(laps * per)} {small}', f'{n(a * k)} {small}', f'{n(a * k - per)} {small}'])


@std(sk(MC, 3))
def mc3_s(r):
    h = r.randint(1, 10); m = r.choice([5, 10, 15, 20, 25, 35, 40, 50]); d1, d2 = r.choice([15, 20, 25, 30]), r.choice([10, 15, 20, 25])
    t = h * 60 + m + d1 + d2; hh, mm = divmod(t, 60); hh = hh if hh <= 12 else hh - 12
    return ('mc3_two_activities', f'Femi starts reading at {h}:{m:02d}. Femi reads for {d1} minutes and then practices piano for {d2} minutes. What time does Femi finish? (Same morning or afternoon.)', f'{hh}:{mm:02d}',
            [f'{d1} + {d2} = {d1 + d2} minutes in all.', f'{h}:{m:02d} + {d1 + d2} minutes = {hh}:{mm:02d}.'], [f'{(h * 60 + m + d1) // 60}:{(h * 60 + m + d1) % 60:02d}', f'{hh}:{(mm + 10) % 60:02d}', f'{h + 1}:{m:02d}'])


@adv(sk(MC, 3))
def mc3_a(r):
    eh, em = r.randint(2, 11), r.choice([0, 10, 20, 30, 40, 50]); d = r.randint(65, 100); bt = r.choice([10, 15, 20])
    start = eh * 60 + em - d - bt; need(start > 60 and d + bt <= 120)
    sh, sm = divmod(start, 60)
    return ('mc3_backward_with_break', f'A game ended at {eh}:{em:02d}. It had {d} minutes of play and a {bt}-minute break. What time did it start? (Same morning or afternoon.)',
            f'{sh}:{sm:02d}', [f'Total time: {d} + {bt} = {d + bt} minutes = 1 hour {d + bt - 60} minutes.', f'Count back 1 hour {d + bt - 60} minutes from {eh}:{em:02d}: {sh}:{sm:02d}.'],
            [f'{(eh * 60 + em - d) // 60}:{(eh * 60 + em - d) % 60:02d}', f'{sh}:{(sm + 10) % 60:02d}', f'{sh + 1}:{sm:02d}'])


@std(sk(MC, 4))
def mc4_s(r):
    p1, p2 = 5 * r.randint(25, 190), 5 * r.randint(25, 190); paid = r.choice([20, 25])
    need(p1 + p2 < paid * 100)
    ch = paid * 100 - p1 - p2
    return ('mc4_two_items_change', f'Kai buys a book for ${p1 / 100:.2f} and a pen for ${p2 / 100:.2f}. Kai pays with a ${paid} bill. How much change does Kai get?', f'${ch / 100:.2f}',
            [f'Total: ${p1 / 100:.2f} + ${p2 / 100:.2f} = ${(p1 + p2) / 100:.2f}.', f'${paid}.00 − ${(p1 + p2) / 100:.2f} = ${ch / 100:.2f}.'], [f'${(p1 + p2) / 100:.2f}', f'${(paid * 100 - p1) / 100:.2f}', f'${(ch + 100) / 100:.2f}'])


@adv(sk(MC, 4))
def mc4_a(r):
    big, small, k = r.choice([('liters', 'milliliters', 1000), ('kilograms', 'grams', 1000), ('pounds', 'ounces', 16), ('gallons', 'cups', 16)])
    a = r.randint(2, 5); per = r.choice([125, 200, 250, 500]) if k == 1000 else r.choice([2, 4, 8])
    need((a * k) % per == 0)
    return ('mc4_how_many_servings', f'A {"jug" if THING[small] == "juice" else "bag"} holds {a} {big} of {THING[small]}. Each serving uses {per} {small}. How many servings can be made?', f'{a * k // per} servings',
            [f'{a} {big} = {n(a * k)} {small}.', f'{n(a * k)} ÷ {per} = {a * k // per} servings.'], [f'{a * per} servings', f'{a * k // per // 2} servings', f'{a * k // per + a} servings'])


@std(sk(MC, 5))
def mc5_s(r):
    l, w = r.randint(4, 20), r.randint(2, 15); need(l != w); k = r.choice([2, 3])
    return ('mc5_scaled_area', f'A rectangle is {l} meters long and {w} meters wide. A second rectangle is {k} times as long and just as wide. What is the area of the second rectangle?', f'{l * k * w} square meters',
            [f'The second rectangle is {k} × {l} = {k * l} meters long and {w} meters wide.', f'Area: {k * l} × {w} = {k * l * w} square meters.'], [f'{l * w} square meters', f'{2 * (k * l + w)} square meters', f'{k * l * k * w} square meters'])


@adv(sk(MC, 5))
def mc5_a(r):
    w = r.randint(3, 12); l = r.randint(w + 1, 20); P = 2 * (l + w)
    return ('mc5_area_from_perimeter', f'A rectangle has a perimeter of {P} feet. Its width is {w} feet. What is its area?', f'{l * w} square feet',
            [f'Length + width = {P} ÷ 2 = {P // 2}, so length = {P // 2} − {w} = {l} feet.', f'Area: {l} × {w} = {l * w} square feet.'], [f'{P * w} square feet', f'{(P - w) * w} square feet', f'{l * w + w} square feet'])


# =============================================================== geometry
@std(sk(GA, 1))
def ga1_s(r):
    a = r.choice([20, 35, 45, 60, 75, 90, 105, 120, 135, 150, 170])
    t = 'acute' if a < 90 else 'right' if a == 90 else 'obtuse'
    b = 180 - a; tb = 'acute' if b < 90 else 'right' if b == 90 else 'obtuse'
    return ('ga1_angle_and_partner', f'Two angles together make a straight angle. One is {a}°. Name the type of the other angle.', tb,
            [f'The other angle is 180° − {a}° = {b}°.', f'{b}° is {"less than" if b < 90 else "exactly" if b == 90 else "greater than"} 90°, so it is {tb}.'], [x for x in ['acute', 'right', 'obtuse', 'straight'] if x != tb])


@adv(sk(GA, 1))
def ga1_a(r):
    a = r.choice([x for x in range(25, 160, 5) if x != 90]); b = 180 - a
    return ('ga1_crossing_lines', f'Two lines cross and make four angles. One angle measures {a}°. Going around the point from that angle, what are the other three angles?', f'{b}°, {a}°, {b}°',
            [f'Angles next to each other along a line add to 180°: 180° − {a}° = {b}°.', f'Angles across from each other are equal, so the angles go {a}°, {b}°, {a}°, {b}°.'],
            [f'{a}°, {a}°, {a}°', f'{b}°, {b}°, {b}°', f'{90 - a if a < 90 else a - 90}°, {a}°, {90 - a if a < 90 else a - 90}°'])

@std(sk(GA, 2))
def ga2_s(r):
    a, b = r.randint(10, 80), r.randint(90, 170); need(b - a > 20)
    return ('ga2_protractor_offset_type', f'On a protractor, one ray of an angle passes through {a}° and the other through {b}°. What is the measure of the angle, and what type is it?', f'{b - a}°, {"acute" if b - a < 90 else "right" if b - a == 90 else "obtuse"}',
            [f'Subtract the readings: {b} − {a} = {b - a}°.', f'{b - a}° is {"less than" if b - a < 90 else "equal to" if b - a == 90 else "greater than"} 90°.'],
            [f'{b}°, obtuse', f'{180 - (b - a)}°, {"acute" if 180 - (b - a) < 90 else "obtuse"}', f'{b + a}°, obtuse' if b + a < 360 else f'{a}°, acute'])


@adv(sk(GA, 2))
def ga2_a(r):
    k = r.choice([3, 4, 5, 6, 8, 9, 10, 12]); m = r.randint(2, k + 2)
    return ('ga2_turn_parts', f'A wheel turns through 1/{k} of a full circle, {m} times in a row. What is the total angle it has turned?', f'{360 * m // k}°',
            [f'1/{k} of 360° is {360 // k}°.', f'{m} × {360 // k}° = {360 * m // k}°.'], [f'{360 // k}°', f'{360 // k + m}°', f'{360 * (m + 1) // k}°'])

@std(sk(GA, 3))
def ga3_s(r):
    a, b = r.randint(15, 70), r.randint(15, 70); need(a + b < 170)
    return ('ga3_two_parts_then_straight', f'Angles A and B fit together without overlap and measure {a}° and {b}°. Together they make angle C. Angle C and angle D form a straight angle. What is angle D?', f'{180 - a - b}°',
            [f'C = {a}° + {b}° = {a + b}°.', f'D = 180° − {a + b}° = {180 - a - b}°.'], [f'{a + b}°', f'{90 - a if a < 90 else 180 - a}°', f'{360 - a - b}°'])


@adv(sk(GA, 3))
def ga3_a(r):
    k = r.randint(3, 6); a = r.randint(10, 30); need(k * a < 180)
    rest = 180 - k * a
    return ('ga3_equal_parts_and_rest', f'{k} equal angles of {a}° and one more angle fit together along a straight line without gaps. What is the measure of the last angle?', f'{rest}°',
            [f'The {k} equal angles make {k} × {a}° = {k * a}°.', f'A straight angle is 180°: 180° − {k * a}° = {rest}°.'], [f'{k * a}°', f'{360 - k * a}°', f'{180 - a}°'])


@std(sk(GA, 4))
def ga4_s(r):
    a, b = r.randint(20, 85), r.randint(20, 85); c = 180 - a - b; need(c > 0 and len({a, b, c}) == 3)
    t = 'acute' if max(a, b, c) < 90 else 'right' if max(a, b, c) == 90 else 'obtuse'
    return ('ga4_third_angle_then_classify', f'Two angles of a triangle are {a}° and {b}°. Find the third angle and classify the triangle by its angles.', f'{c}°, {t}',
            [f'180° − {a}° − {b}° = {c}°.', f'The largest angle is {max(a, b, c)}°, so the triangle is {t}.'],
            [f'{c}°, {"acute" if t != "acute" else "obtuse"}', f'{a + b}°, obtuse' if a + b < 180 else f'{c + 10}°, {t}', f'{180 - a}°, {t}'])


@adv(sk(GA, 4))
def ga4_a(r):
    opts = [('a square', 'It has 4 right angles and 4 equal sides, so it is also a rectangle and a rhombus.'),
            ('a rectangle', 'It has 4 right angles, but its sides are not all equal, so it is not a square.')]
    choice, why = r.choice(opts)
    l, w = (r.randint(3, 9),) * 2 if choice == 'a square' else tuple(r.sample(range(3, 10), 2))
    names = 'square, rectangle, rhombus, parallelogram' if choice == 'a square' else 'rectangle, parallelogram'
    return ('ga4_all_names', f'A quadrilateral has 4 right angles and sides {l}, {w}, {l} and {w} units long. List every name that fits it: square, rectangle, rhombus, parallelogram, trapezoid (exactly one pair of parallel sides).', names,
            [f'Opposite sides are parallel and equal, and every angle is a right angle.', why], ['rectangle' if choice == 'a square' else 'rectangle, rhombus', 'square, rhombus' if choice == 'a square' else 'square, rectangle', 'parallelogram, trapezoid'])


@std(sk(GA, 5))
def ga5_s(r):
    shapes = [('square', 4), ('rectangle that is not a square', 2), ('equilateral triangle', 3), ('regular hexagon', 6), ('isosceles triangle that is not equilateral', 1), ('rhombus that is not a square', 2), ('regular pentagon', 5), ('regular octagon', 8)]
    a, b = r.sample(shapes, 2)
    return ('ga5_two_shapes_total', f'How many lines of symmetry does {an(a[0])} have? {an(b[0]).capitalize()}? Give the total.', str(a[1] + b[1]),
            [f'{an(a[0]).capitalize()} has {a[1]}; {an(b[0])} has {b[1]}.', f'Total: {a[1]} + {b[1]} = {a[1] + b[1]}.'], [str(a[1]), str(a[1] + b[1] + 1), str(a[1] * b[1]) if a[1] * b[1] != a[1] + b[1] else str(a[1] + b[1] - 1)])


@adv(sk(GA, 5))
def ga5_a(r):
    half = r.randint(12, 60); side = r.randint(3, 12)
    return ('ga5_half_shape_perimeter', f'A line of symmetry splits a figure into two matching halves. One half has an area of {half} square inches, and the line of symmetry is {side} inches long. What is the area of the whole figure?', f'{2 * half} square inches',
            ['The two halves match, so they have equal areas.', f'{half} + {half} = {2 * half} square inches. (The length of the line does not change the area.)'], [f'{half} square inches', f'{half + side} square inches', f'{half * side} square inches'])


# =============================================================== data and word problems
@std(sk(DP, 3))
def dp3_s(r):
    a, b, c = r.randint(3, 9), r.randint(12, 48), r.randint(5, 40); nm = r.choice(NAMES)
    return ('dp3_groups_plus_extra_minus', f'{nm} has {a} boxes with {b} crayons each and {c} loose crayons. {nm} gives away {b} crayons. How many crayons are left?', str(a * b + c - b),
            [f'{a} × {b} + {c} = {a * b + c} crayons.', f'{a * b + c} − {b} = {a * b + c - b}.'], [str(a * b + c), str(a * b - c), str((a - 1) * b)])


@adv(sk(DP, 3))
def dp3_a(r):
    seats, buses = r.randint(30, 48), r.randint(2, 5); students = r.randint(seats * buses + 10, seats * buses + 60); van = r.choice([7, 8, 9])
    rest = students - seats * buses; vans = -(-rest // van)
    return ('dp3_buses_then_vans', f'{students} students go on a trip. {buses} buses each hold {seats} students. The rest ride in vans that hold {van} students each. How many vans are needed?', f'{vans} vans',
            [f'Buses: {buses} × {seats} = {seats * buses}. Rest: {students} − {seats * buses} = {rest}.', f'{rest} ÷ {van} = {rest // van} R {rest % van}, so {vans} vans.' if rest % van else f'{rest} ÷ {van} = {vans} vans.'],
            [f'{rest // van} vans' if rest % van else f'{vans + 1} vans', f'{rest} vans', f'{-(-students // van)} vans'])


@std(sk(DP, 4))
def dp4_s(r):
    a, b, c = r.randint(3, 9), r.randint(12, 60), r.randint(10, 99); total = a * b + c
    nm = r.choice(NAMES)
    return ('dp4_letter_then_check', f'{nm} buys {a} games for ${b} each and a ${c} controller. Let t be the total cost. Write an equation and find t.', f't = {a} × {b} + {c}; t = ${total}',
            [f'Equation: t = {a} × {b} + {c}.', f'{a} × {b} = {a * b}, and {a * b} + {c} = {total}, so t = ${total}.'],
            [f't = {a} + {b} + {c}; t = ${a + b + c}', f't = {a} × ({b} + {c}); t = ${a * (b + c)}', f't = {a} × {b} − {c}; t = ${a * b - c}'])


@adv(sk(DP, 4))
def dp4_a(r):
    k, per, total = r.randint(3, 8), r.randint(12, 45), 0; extra = r.randint(5, 40); total = k * per + extra
    return ('dp4_solve_for_per', f'{k} equal packs of cards and {extra} loose cards make {total} cards. Let c be the number of cards in each pack, so {k} × c + {extra} = {total}. What is c?', str(per),
            [f'Take away the loose cards: {total} − {extra} = {total - extra}.', f'{total - extra} ÷ {k} = {per}, so c = {per}.'], [str((total + extra) // k), str(total // k), str(total - extra)])


# =============================================================== second families for the skills with the most reused templates
@std(sk(PV, 1))
def pv1_s2(r):
    d = r.randint(2, 9); p = r.choice([10, 100, 1000]); k = r.choice([10, 100])
    v = d * p * k; need(v <= 1000000)
    return ('pv1_ten_times_chain', f'What number is {k} times as much as {n(d * p)}? Write the value of the digit {d} in your answer.', f'{n(v)}',
            [f'{k} times as much: {n(d * p)} × {k} = {n(v)}.', f'The digit {d} moved {"one place" if k == 10 else "two places"} to the left; its value is {n(v)}.'], [n(d * p * 10 if k == 100 else d * p * 100), n(d * p), n(v * 10)])


@std(sk(AS, 1))
def as1_s2(r):
    a, b = r.randint(100000, 400000), r.randint(100000, 400000); c = r.randint(1000, 50000)
    return ('as1_sum_minus', f'A store sold {n(a)} items in May and {n(b)} items in June. In July it sold {n(c)} fewer than in May and June together. How many items did it sell in July?', n(a + b - c),
            [f'May and June: {n(a)} + {n(b)} = {n(a + b)}.', f'{n(a + b)} − {n(c)} = {n(a + b - c)}.'], [n(a + b), n(a + b + c), n(a - c)])


@std(sk(AS, 2))
def as2_s2(r):
    a = r.randint(400000, 900000); b = r.randint(100000, a - 100000); c = r.randint(10000, 90000)
    return ('as2_difference_then_more', f'Lake A has {n(a)} fish and Lake B has {n(b)} fish. How many more fish does Lake A have? Then {n(c)} fish are added to Lake B. How many more does Lake A have now?', n(a - b - c),
            [f'{n(a)} − {n(b)} = {n(a - b)} more.', f'Adding {n(c)} to Lake B closes the gap: {n(a - b)} − {n(c)} = {n(a - b - c)}.'], [n(a - b), n(a - b + c), n(a - c)]) if a - b - c > 0 else (_ for _ in ()).throw(Skip())


@std(sk(AS, 3))
def as3_s2(r):
    z = r.choice([1000, 2000, 5000, 10000, 20000]); a, b = r.randint(100, z // 3), r.randint(100, z // 3)
    return ('as3_two_from_round', f'A goal is {n(z)} steps. Uma walks {n(a)} steps in the morning and {n(b)} in the afternoon. How many steps are left to reach the goal?', n(z - a - b),
            [f'Steps walked: {n(a)} + {n(b)} = {n(a + b)}.', f'{n(z)} − {n(a + b)} = {n(z - a - b)} steps.'], [n(z - a), n(z - a + b), n(a + b)])


@std(sk(DV, 1))
def dv1_s2(r):
    d, q = r.randint(2, 9), r.randint(2, 9); p = r.choice([10, 100])
    return ('dv1_unit_form_then_number', f'Fill in the blank: {d * q} {PLACE[p]} ÷ {d} = ___ {PLACE[p]}. Then write the quotient as a number.', n(q * p),
            [f'{d * q} ÷ {d} = {q}, so {d * q} {PLACE[p]} ÷ {d} = {q} {PLACE[p]}.', f'{q} {PLACE[p]} = {n(q * p)}.'], [str(q), n(d * q * p), n(q * p * 10)])


@std(sk(DV, 3))
def dv3_s2(r):
    d, q = r.randint(3, 9), r.randint(105, 999); total = d * q; need(total < 10000); k = r.randint(2, 20)
    return ('dv3_divide_then_subtract', f'{n(total)} seeds are planted equally in {d} rows. Then {k} seeds in one row do not grow. How many seeds grow in that row?', n(q - k),
            [f'{n(total)} ÷ {d} = {n(q)} seeds in each row.', f'{n(q)} − {k} = {n(q - k)} seeds.'], [n(q), n(total - k), n(q + k)])


@std(sk(DV, 4))
def dv4_s2(r):
    d = r.randint(3, 9); q = r.randint(10, 99); rem = r.randint(1, d - 1); total = d * q + rem
    return ('dv4_which_quotient', f'{total} pencils are put into boxes of {d}. How many boxes are full, and how many pencils are left over? Write it as a quotient and remainder.', f'{q} R {rem}',
            [f'{total} ÷ {d}: {d} × {q} = {d * q}.', f'{total} − {d * q} = {rem} left over, so {q} R {rem}.'], [f'{q + 1} R {rem}', f'{q} R {d - rem}' if d - rem != rem else f'{q} R {rem + 1}', f'{q - 1} R {rem}'])


@std(sk(FM, 4))
def fm4_s2(r):
    s, a = r.randint(80, 200), r.randint(3, 12); k = r.randint(5, 8)
    return ('fm4_subtract_rule_term', f'A pattern starts at {s} and subtracts {a} each time. What is the {ORD[k - 1]} number?', str(s - a * (k - 1)),
            [f'The {ORD[k - 1]} number is {k - 1} steps after the first.', f'{s} − {k - 1} × {a} = {s} − {a * (k - 1)} = {s - a * (k - 1)}.'], [str(s - a * k), str(s - a * (k - 2)), str(s + a * (k - 1))])


@std(sk(FE, 2))
def fe2_s2(r):
    b = r.choice([2, 3, 4, 5, 6]); a = r.randint(1, b - 1); k = r.choice([2, 3, 4, 5, 6]); need(b * k <= 12)
    return ('fe2_missing_then_check', f'Find the missing numerator: {a}/{b} = ___/{b * k}. What number did you multiply the numerator and denominator by?', f'{a * k}/{b * k}; {k}',
            [f'{b} × {k} = {b * k}, so multiply by {k}.', f'{a} × {k} = {a * k}: {a}/{b} = {a * k}/{b * k}.'], [f'{a + k}/{b * k}; {k}', f'{a * k}/{b * k}; {k + 1}', f'{a}/{b * k}; 1'])


@std(sk(FE, 3))
def fe3_s2(r):
    a = r.randint(1, 5); b1, b2, b3 = sorted(r.sample([2, 3, 4, 5, 6, 8, 10, 12], 3)); need(a < b1)
    return ('fe3_same_numerator_three', f'Order from greatest to least: {a}/{b2}, {a}/{b1}, {a}/{b3}.', f'{a}/{b1}, {a}/{b2}, {a}/{b3}',
            ['The numerators are the same, so compare the size of the pieces.', f'Fewer pieces in the whole means bigger pieces: {a}/{b1}, {a}/{b2}, {a}/{b3}.'], [f'{a}/{b3}, {a}/{b2}, {a}/{b1}', f'{a}/{b2}, {a}/{b1}, {a}/{b3}', f'{a}/{b1}, {a}/{b3}, {a}/{b2}'])


@std(sk(FE, 4))
def fe4_s2(r):
    b = r.choice([3, 4, 5, 6, 8, 10, 12]); a = r.randint(1, b - 1); need(2 * a != b)
    side = 'greater' if 2 * a > b else 'less'
    return ('fe4_half_then_closest', f'Is {a}/{b} greater than or less than 1/2? Use the numerator and half the denominator.', side,
            [f'Half of {b} is {F(Fr(b, 2))}.', f'{a} is {"more" if side == "greater" else "less"} than {F(Fr(b, 2))}, so {a}/{b} is {side} than 1/2.'], ['less' if side == 'greater' else 'greater', 'equal', 'cannot tell'])


@std(sk(FD, 1))
def fd1_s2(r):
    b = r.choice([5, 6, 8, 10]); a = r.randint(4, b - 1); x = r.randint(1, a - 1)
    return ('fd1_two_ways', f'Write {a}/{b} as a sum of two fractions with denominator {b}. One of them is {x}/{b}. What is the other?', f'{a - x}/{b}',
            [f'The numerators must add to {a}.', f'{a} − {x} = {a - x}, so {a}/{b} = {x}/{b} + {a - x}/{b}.'], [f'{a + x}/{b}', f'{a - x}/{b * 2}', f'{x}/{b}' if x != a - x else f'{a}/{b}'])


@std(sk(GA, 2))
def ga2_s2(r):
    a = r.choice(range(10, 171, 5)); need(a != 90)
    return ('ga2_reading_both_scales', f'One ray of an angle is on 0° of the outer scale of a protractor, and the other ray passes through {a}° on that scale. The inner scale reads {180 - a}° there. What is the measure of the angle?', f'{a}°',
            ['Use the scale that starts at 0° on the first ray: the outer scale.', f'The angle measures {a}°, not {180 - a}°.'], [f'{180 - a}°', f'{a + 90}°' if a + 90 < 180 else f'{a - 90}°', '180°'])


@std(sk(MS, 2))
def ms2_s2(r):
    a, p = r.randint(2, 9), r.choice([10, 100]); b, q = r.randint(2, 9), r.choice([10, 100])
    return ('ms2_product_of_tens', f'Multiply {a * p} × {b * q}. Use the fact {a} × {b} = {a * b}.', n(a * p * b * q),
            [f'{a * p} × {b * q} = {a} × {b} × {p} × {q}.', f'{a * b} × {n(p * q)} = {n(a * b * p * q)}.'], [n(a * b * max(p, q)), n(a * b * p * q * 10), n(a * p + b * q)])


@std(sk(DP, 4))
def dp4_s2(r):
    a, b, c = r.randint(3, 9), r.randint(15, 60), r.randint(5, 40)
    return ('dp4_value_with_letter', f'Find the value of n: n = {a} × {b} − {c}', str(a * b - c),
            [f'Multiply first: {a} × {b} = {a * b}.', f'Then subtract: {a * b} − {c} = {a * b - c}.'], [str(a * (b - c)), str(a * b + c), str(a + b - c)]) if a * b > c and b > c else (_ for _ in ()).throw(Skip())


@adv(sk(PV, 3))
def pv3_a2(r):
    a = r.randint(100, 899) * 1000 + r.randint(0, 999); b = a + r.randint(1, 9) * 1000
    lo, hi = sorted([a, b])
    k = len([x for x in range(lo + 1, hi) if x % 1000 == 0])
    return ('pv3_thousands_between', f'How many multiples of 1,000 are greater than {n(lo)} and less than {n(hi)}?', str(k),
            [f'The first multiple of 1,000 after {n(lo)} is {n((lo // 1000 + 1) * 1000)}.', f'Count by thousands up to {n((hi - 1) // 1000 * 1000)}: {k}.'], [str(k + 1), str(max(0, k - 1)), str((hi - lo) // 100)])


@adv(sk(AS, 1))
def as1_a2(r):
    a, b, c = (r.randint(100000, 300000) for _ in range(3)); t = a + b + c
    return ('as1_three_with_check', f'Three towns have {n(a)}, {n(b)} and {n(c)} people. A fourth town has as many people as the three together. How many people live in all four towns?', n(2 * t),
            [f'Three towns: {n(a)} + {n(b)} + {n(c)} = {n(t)}.', f'The fourth town also has {n(t)}, so all four have {n(t)} + {n(t)} = {n(2 * t)}.'], [n(t), n(t + a), n(3 * t) if 3 * t < 10 ** 6 else n(t + b)]) if 2 * t <= 1000000 else (_ for _ in ()).throw(Skip())


@adv(sk(AS, 3))
def as3_a2(r):
    z = r.choice([10000, 50000, 100000]); a = r.randint(z // 4, z // 2); b = r.randint(z // 10, z // 4)
    return ('as3_compare_two_gaps', f'Two classes each have a goal of {n(z)} points. Class A has {n(a)} points and Class B has {n(a + b)} points. How many more points does Class A need than Class B?', n(b),
            [f'Class A needs {n(z)} − {n(a)} = {n(z - a)}. Class B needs {n(z)} − {n(a + b)} = {n(z - a - b)}.', f'{n(z - a)} − {n(z - a - b)} = {n(b)}.'], [n(z - a), n(z - a - b), n(z - b)])


@adv(sk(FM, 3))
def fm3_a2(r):
    lo = r.randint(20, 70); hi = lo + r.randint(10, 25); hi = min(hi, 100)
    ps = [p for p in PRIMES if lo < p < hi]; need(len(ps) >= 2)
    return ('fm3_sum_of_primes', f'What is the sum of all the prime numbers between {lo} and {hi}?', str(sum(ps)),
            [f'Test each number for factors other than 1 and itself.', f'The primes are {", ".join(map(str, ps))}; their sum is {sum(ps)}.'], [str(sum(ps) - ps[-1]), str(sum(ps) + 2), str(len(ps))])


@adv(sk(FE, 2))
def fe2_a2(r):
    b = r.choice([2, 3, 4]); a = r.randint(1, b - 1); ks = [k for k in range(2, 7) if b * k <= 12]
    return ('fe2_count_equivalents', f'How many fractions equal to {a}/{b} have a denominator of 12 or less? Count {a}/{b} itself.', str(1 + len(ks)),
            [f'Multiply {a}/{b} by {"/".join(f"{k}/{k}" for k in ks)}: {", ".join(f"{a * k}/{b * k}" for k in ks)}.', f'With {a}/{b} itself that is {1 + len(ks)} fractions.'], [str(len(ks)), str(len(ks) + 2), str(len(ks) + 3)])


@adv(sk(FE, 4))
def fe4_a2(r):
    b1, b2 = r.sample([3, 4, 5, 6, 8, 10, 12], 2); a1, a2 = r.randint(1, b1 - 1), r.randint(1, b2 - 1)
    x, y = Fr(a1, b1), Fr(a2, b2); need(x != y and min(x, y) > Fr(1, 2) and abs(x - y) > Fr(1, 30))
    big = f'{a1}/{b1}' if x > y else f'{a2}/{b2}'
    return ('fe4_both_above_half', f'Both {a1}/{b1} and {a2}/{b2} are greater than 1/2, so the benchmark 1/2 does not decide. Compare how far each is from 1. Which fraction is greater?', big,
            [f'{a1}/{b1} is {b1 - a1}/{b1} away from 1, and {a2}/{b2} is {b2 - a2}/{b2} away from 1.', f'The fraction with the smaller gap to 1 is greater: {big}.'], [f'{a2}/{b2}' if big == f'{a1}/{b1}' else f'{a1}/{b1}', 'They are equal', '1/2'])


@adv(sk(FD, 1))
def fd1_a2(r):
    b = r.choice([5, 6, 8]); a = r.randint(4, b)
    ways = a // 2   # unordered pairs x + y = a with x, y >= 1
    return ('fd1_count_two_part', f'In how many ways can {a}/{b} be written as a sum of two fractions with denominator {b} and whole-number numerators of at least 1? (1/{b} + {a - 1}/{b} and {a - 1}/{b} + 1/{b} count as one way.)', str(ways),
            [f'The two numerators must add to {a}: {", ".join(f"{x} + {a - x}" for x in range(1, a // 2 + 1))}.', f'That is {ways} ways.'], [str(a - 1), str(ways + 1), str(a)])


@adv(sk(FD, 3))
def fd3_a2(r):
    b = r.choice([4, 6, 8]); w1, a1 = r.randint(3, 6), r.randint(1, b - 2); w2, a2 = r.randint(1, 2), r.randint(a1 + 1, b - 1)
    d = Fr(w1 * b + a1, b) - Fr(w2 * b + a2, b)
    return ('fd3_subtract_rename', f'Subtract {w1} {a1}/{b} − {w2} {a2}/{b}. You will need to rename {w1} {a1}/{b} first.', F(d),
            [f'{w1} {a1}/{b} = {w1 - 1} {a1 + b}/{b}.', f'{w1 - 1} {a1 + b}/{b} − {w2} {a2}/{b} = {F(d)}.'], [f'{w1 - w2} {a2 - a1}/{b}', F(d + 1), F(d - Fr(1, b)) if d > Fr(1, b) else F(d + Fr(1, b))])


@adv(sk(FD, 6))
def fd6_a2(r):
    a = r.randint(11, 89); need(a % 10)
    t = a // 10
    return ('fd6_round_tenths', f'Which tenth is 0.{a} closest to? Write it as a decimal.', f'{(t + (1 if a % 10 >= 5 else 0)) / 10:.1f}' if not (t == 9 and a % 10 >= 5) else '1.0',
            [f'0.{a} is between 0.{t} and {(t + 1) / 10:.1f}.', f'0.{a} is {a % 10} hundredths past 0.{t}, so it is closer to {(t + (1 if a % 10 >= 5 else 0)) / 10:.1f}.'],
            [f'0.{t}' if a % 10 >= 5 else f'{(t + 1) / 10:.1f}', f'0.{a % 10}', f'{a / 10:.1f}']) if a % 10 != 5 else (_ for _ in ()).throw(Skip())


@adv(sk(DV, 1))
def dv1_a2(r):
    d = r.randint(3, 9); q = r.randint(3, 9); p = 100
    return ('dv1_missing_dividend', f'___ ÷ {d} = {n(q * p)}. What is the missing number? Explain with a basic fact.', n(d * q * p),
            [f'Basic fact: {d} × {q} = {d * q}.', f'{d} × {n(q * p)} = {n(d * q * p)}, so {n(d * q * p)} ÷ {d} = {n(q * p)}.'], [n(q * p), n(d * q * 10), n(d + q * p)])


@adv(sk(DV, 3))
def dv3_a2(r):
    d = r.randint(3, 9); q = r.randint(101, 999); total = d * q; need(total < 10000 and '0' in str(q))
    return ('dv3_zero_in_quotient', f'Divide {n(total)} ÷ {d}. Watch for a place where the quotient needs a 0. What is the quotient?', f'{n(q)}',
            [f'Divide one place at a time: {n(total)} ÷ {d} = {n(q)}.', 'At one step the part left to divide was less than ' + str(d) + ', so that place gets a 0.'], [n(int(str(q).replace('0', ''))), n(q + 10), n(q * 10) if q * 10 < 10000 else n(q - 1)])


@adv(sk(DV, 4))
def dv4_a2(r):
    d = r.randint(4, 9); q = r.randint(30, 150); rem = r.randint(1, d - 1); k = r.randint(2, 4)
    total = d * q + rem
    return ('dv4_greatest_with_remainder', f'What is the greatest number less than {n(total + d * k)} that leaves a remainder of {rem} when divided by {d}?', n(d * (q + k - 1) + rem) if d * (q + k - 1) + rem < total + d * k else n(d * (q + k) + rem),
            [f'Numbers with remainder {rem}: {d} × (a whole number) + {rem}.', f'The greatest below {n(total + d * k)} is {d} × {q + k - (0 if d * (q + k) + rem < total + d * k else 1)} + {rem}.'], [n(total), n(total + d * k - 1), n(d * (q + k) )])


@adv(sk(GA, 4))
def ga4_a2(r):
    a = r.randint(20, 70); b = r.randint(20, 160 - a)
    c = 180 - a - b; need(c > 0 and c != 90 and a != b != c)
    t = 'acute' if max(a, b, c) < 90 else 'obtuse'
    return ('ga4_exterior_then_classify', f'A triangle has angles of {a}° and {b}°. Find the third angle. Can this triangle be a right triangle? Classify it by its angles.', f'{c}°; {t}',
            [f'180° − {a}° − {b}° = {c}°.', f'No angle is 90°; the largest is {max(a, b, c)}°, so it is {t}.'], [f'{c}°; right', f'{a + b}°; obtuse', f'{c}°; {"obtuse" if t == "acute" else "acute"}'])


@adv(sk(MS, 2))
def ms2_a2(r):
    a, b = r.randint(2, 9), r.randint(2, 9); p, q = r.choice([10, 100]), r.choice([10, 100]); prod = a * b * p * q; need(prod <= 1000000)
    z = len(str(prod)) - len(str(prod).rstrip('0')); zp = len(str(p * q)) - 1
    return ('ms2_zeros_count', f'How many zeros are at the end of the product {n(a * p)} × {n(b * q)}?', str(z),
            [f'{a} × {b} = {a * b}, and {n(p)} × {n(q)} = {n(p * q)}, so the product is {n(prod)}.', f'{n(prod)} ends in {z} zero{"s" if z != 1 else ""}' + (f' (one more than the {zp} zeros in the factors, because {a} × {b} = {a * b} ends in 0).' if z > zp else '.')],
            [str(x) for x in (zp, zp + 1, zp + 2, zp - 1) if x != z and x >= 0])
