"""4th Grade Math audit #4 (2026-11-19): a context-based open-response item for every skill at every level.

Each item is one situation with three computed parts and an explain-your-thinking part. Explanation answers begin
"Sample answer:", which the Grade 4 players self-check (any written answer counts; the sample is shown after).
IDs end in -o01 (for example m4-fe-s03-cp1-o01). Numbers grow with the level; Advanced adds a reverse or
comparison step."""
import random, re
from fractions import Fraction as Fr
from lib import ABBR, UNITS, F, n
import fams
from fams import NAMES, PRIMES, factors, rnd, Skip, need, qty, THING

NOTE = ('Original Claude-authored item (family: {fam}). 4th Grade Math audit 2026-11-19 (#4, open response); answers '
        'recomputed by scripts/test-grade4-audit.cjs; the explanation part is self-checked.')
O = {}


def orq(unit, i):
    def d(f):
        O[f'{unit}-skill-{i:02d}'] = f; return f
    return d


PV, AS, MS, DV, FM, FE, FD, MC, GA, DP = fams.PV, fams.AS, fams.MS, fams.DV, fams.FM, fams.FE, fams.FD, fams.MC, fams.GA, fams.DP
S = 'Sample answer: '


@orq(PV, 1)
def o_pv1(r, L):
    d = r.randint(2, 9); p = [100, 1000, 10000][L]
    a, b = d * p, d * p * 10
    return ('pv1_open_two_towns', f'Town A has {n(a)} people. Town B has 10 times as many people as Town A.', [
        ('How many people live in Town B?', n(b), f'{n(a)} × 10 = {n(b)}.'),
        (f'What is the value of the digit {d} in the population of Town B?', n(b), f'The {d} is in the {fams.PLACE[p * 10]} place, so it is worth {n(b)}.'),
        (f'How many people would Town C have if it had 1/10 as many people as Town A?', n(a // 10), f'{n(a)} ÷ 10 = {n(a // 10)}.'),
        ('Explain how the value of a digit changes when it moves one place to the left.', S + 'It becomes 10 times as much, because each place is worth 10 times the place to its right.', 'Each place to the left is worth 10 times as much.')])


@orq(PV, 2)
def o_pv2(r, L):
    num = r.randint([1000, 10000, 100000][L], [9999, 99999, 999999][L]); s = str(num)
    parts = [int(c) * 10 ** (len(s) - 1 - i) for i, c in enumerate(s) if c != '0']
    return ('pv2_open_check', f'A check is written for ${n(num)}.', [
        ('Write the amount in expanded form.', ' + '.join(n(x) for x in parts), 'Write the value of each nonzero digit.'),
        ('How many thousands are in the amount? (Count whole thousands.)', n(num // 1000), f'{n(num)} has {n(num // 1000)} whole thousands.'),
        ('What number is 1,000 more?', n(num + 1000), f'{n(num)} + 1,000 = {n(num + 1000)}.'),
        ('Explain what happens to the digits when you add 1,000.', S + 'Adding 1,000 adds 1 to the thousands digit; if that digit is 9, it becomes 0 and 1 is regrouped into the ten thousands place.', 'Think about regrouping 10 thousands as 1 ten thousand.')])


@orq(PV, 3)
def o_pv3(r, L):
    base = [3000, 40000, 300000][L]; xs = sorted({base + r.randint(100, base // 3) for _ in range(3)}); need(len(xs) == 3)
    names = r.sample(['Oak Park', 'Hill Stadium', 'River Arena', 'Bay Field'], 3)
    data = dict(zip(names, r.sample(xs, 3)))
    srt = sorted(data.items(), key=lambda x: x[1])
    return ('pv3_open_stadiums', 'Seats: ' + '; '.join(f'{k} {n(v)}' for k, v in data.items()) + '.', [
        ('Which place has the most seats?', srt[-1][0], f'Compare from the greatest place: {n(srt[-1][1])} is greatest.'),
        ('Write the numbers of seats from least to greatest.', ', '.join(n(v) for _, v in srt), 'Line up the digits by place value and compare from the left.'),
        ('How many more seats does the largest place have than the smallest?', n(srt[-1][1] - srt[0][1]), f'{n(srt[-1][1])} − {n(srt[0][1])} = {n(srt[-1][1] - srt[0][1])}.'),
        ('Explain how you compared two of the numbers.', S + 'I lined up the digits and compared from the left; the first place where the digits differ decides which number is greater.', 'Compare place by place from the left.')])


@orq(PV, 4)
def o_pv4(r, L):
    x = r.randint([1000, 10000, 100000][L], [9999, 99999, 999999][L]); u = [100, 1000, 10000][L]
    lo, hi = (x // u) * u, (x // u + 1) * u
    return ('pv4_open_round', f'A stadium sold {n(x)} tickets.', [
        (f'Between which two multiples of {n(u)} is {n(x)}? Give the lower one.', n(lo), f'{n(x)} is between {n(lo)} and {n(hi)}.'),
        (f'What number is halfway between them?', n(lo + u // 2), f'Halfway is {n(lo + u // 2)}.'),
        (f'Round {n(x)} to the nearest {fams.PLACE[u][:-1]}.', n(rnd(x, u)), f'{n(x)} is {"at or past" if x >= lo + u // 2 else "before"} the halfway point, so it rounds to {n(rnd(x, u))}.'),
        ('Explain how the halfway number helps you round.', S + 'If the number is at or past halfway it rounds up; if it is less than halfway it rounds down.', 'Compare with the halfway point.')])


@orq(AS, 1)
def o_as1(r, L):
    a, b = (r.randint([1000, 10000, 100000][L], [4999, 49999, 499999][L]) for _ in range(2))
    return ('as1_open_two_days', f'A museum had {n(a)} visitors on Saturday and {n(b)} visitors on Sunday.', [
        ('How many visitors came in all?', n(a + b), f'{n(a)} + {n(b)} = {n(a + b)}.'),
        (f'Estimate the total by rounding each number to the nearest {"thousand" if L else "hundred"}.', n(rnd(a, 1000 if L else 100) + rnd(b, 1000 if L else 100)), f'{n(rnd(a, 1000 if L else 100))} + {n(rnd(b, 1000 if L else 100))} = {n(rnd(a, 1000 if L else 100) + rnd(b, 1000 if L else 100))}.'),
        ('How many more visitors came on the busier day?', n(abs(a - b)), f'{n(max(a, b))} − {n(min(a, b))} = {n(abs(a - b))}.'),
        ('Explain how the estimate shows your exact total is reasonable.', S + 'The estimate is close to the exact total, so the exact answer makes sense.', 'Compare the estimate with the exact answer.')])


@orq(AS, 2)
def o_as2(r, L):
    a = r.randint([5000, 50000, 500000][L], [9999, 99999, 999999][L]); b = r.randint(a // 4, a // 2); c = r.randint(a // 10, a // 5)
    return ('as2_open_fundraiser', f'A school wants to raise ${n(a)}. It has raised ${n(b)} so far.', [
        ('How much more does it need?', f'${n(a - b)}', f'{n(a)} − {n(b)} = {n(a - b)}.'),
        (f'It raises ${n(c)} more this week. How much more does it need now?', f'${n(a - b - c)}', f'{n(a - b)} − {n(c)} = {n(a - b - c)}.'),
        ('Use addition to check your last answer. What total do you get?', f'${n(a)}', f'{n(a - b - c)} + {n(c)} + {n(b)} = {n(a)}.'),
        ('Explain why addition can check subtraction.', S + 'Subtraction finds a missing part; adding the parts back together should give the whole.', 'Addition and subtraction are inverse operations.')])


@orq(AS, 3)
def o_as3(r, L):
    z = [1000, 10000, 100000][L]; b = r.randint(z // 5, z - z // 10)
    return ('as3_open_goal', f'A reading club has a goal of {n(z)} pages. Members have read {n(b)} pages.', [
        ('How many pages are left?', n(z - b), f'{n(z)} − {n(b)} = {n(z - b)}.'),
        (f'Show {n(z)} regrouped so you can subtract. How many hundreds does it have after regrouping? (Count the hundreds digit.)', '9', f'{n(z)} = {n(z - 1000) if z > 1000 else "0"} + 9 hundreds + 9 tens + 10 ones.'),
        (f'Check: what is {n(z - b)} + {n(b)}?', n(z), f'{n(z - b)} + {n(b)} = {n(z)}.'),
        ('Explain another way to find the difference without regrouping across zeros.', S + f'Subtract from {n(z - 1)} instead and then add 1 back.', f'{n(z - 1)} − {n(b)} needs no regrouping.')])


@orq(AS, 4)
def o_as4(r, L):
    a, b = (r.randint([1000, 10000, 100000][L], [4499, 44999, 449999][L]) for _ in range(2)); u = [100, 1000, 10000][L]
    est = rnd(a, u) + rnd(b, u)
    return ('as4_open_estimate', f'A store sold {n(a)} items in March and {n(b)} items in April.', [
        (f'Estimate the total by rounding each to the nearest {fams.PLACE[u][:-1]}.', n(est), f'{n(rnd(a, u))} + {n(rnd(b, u))} = {n(est)}.'),
        ('Find the exact total.', n(a + b), f'{n(a)} + {n(b)} = {n(a + b)}.'),
        ('How far is the estimate from the exact total?', n(abs(est - a - b)), f'The difference between {n(est)} and {n(a + b)} is {n(abs(est - a - b))}.'),
        ('Explain when an estimate is good enough.', S + 'When you only need to know about how many, such as deciding if something is enough, an estimate is good enough.', 'Think about what the answer is used for.')])


@orq(AS, 5)
def o_as5(r, L):
    a = r.randint([1000, 10000, 100000][L], [5000, 50000, 500000][L]); b = r.randint(a // 5, a // 2); c = r.randint(a // 5, a // 2)
    return ('as5_open_points', f'A team had {n(a)} points. It earned {n(b)} points and then lost {n(c)} points.', [
        ('Write an expression for the points now.', f'{n(a)} + {n(b)} − {n(c)}', 'Add the points earned, then subtract the points lost.'),
        ('How many points does the team have now?', n(a + b - c), f'{n(a)} + {n(b)} = {n(a + b)}; {n(a + b)} − {n(c)} = {n(a + b - c)}.'),
        ('Did the team end with more or fewer points than it started with?', 'more' if b > c else 'fewer', f'It earned {n(b)} and lost {n(c)}, so it ended with {"more" if b > c else "fewer"}.'),
        ('Explain how you know your answer is reasonable.', S + 'It earned and lost similar amounts, so the total should be close to where it started.', 'Use estimation.')])


@orq(MS, 1)
def o_ms1(r, L):
    a = r.randint(2, [9, 15, 25][L]); k = r.randint(2, [6, 9, 12][L])
    return ('ms1_open_times_as_many', f'Rosa has {a} shells. Ben has {k} times as many shells as Rosa.', [
        ('Write an equation for the number of Ben\'s shells, b.', f'b = {k} × {a}', 'Times as many means multiply.'),
        ('How many shells does Ben have?', str(a * k), f'{k} × {a} = {a * k}.'),
        ('How many more shells does Ben have than Rosa?', str(a * k - a), f'{a * k} − {a} = {a * k - a}.'),
        ('Explain the difference between "times as many" and "more than".', S + '"Times as many" means multiply; "more than" means add.', 'Compare multiplying with adding.')])


@orq(MS, 2)
def o_ms2(r, L):
    a = r.randint(2, 9); p = [10, 100, 1000][L]; k = r.randint(2, 9)
    return ('ms2_open_boxes', f'Each box holds {n(a * p)} paper clips. A store has {k} boxes.', [
        ('How many paper clips are there?', n(a * p * k), f'{k} × {n(a * p)} = {k} × {a} × {n(p)} = {n(a * p * k)}.'),
        ('Which basic fact helps you?', f'{k} × {a} = {k * a}', f'{k} × {a} = {k * a}.'),
        (f'How many paper clips are in 10 boxes?', n(a * p * 10), f'10 × {n(a * p)} = {n(a * p * 10)}.'),
        ('Explain how the basic fact and place value give the product.', S + f'Multiply {k} × {a}, then multiply by {n(p)} by writing the zeros.', 'Use the basic fact, then place value.')])


@orq(MS, 3)
def o_ms3(r, L):
    a = r.randint([12, 105, 1001][L], [99, 999, 2499][L]); k = r.randint(3, 9)
    t, o = a // 10 * 10, a % 10
    return ('ms3_open_partial', f'A farm packs {n(a)} eggs each day for {k} days.', [
        ('Write the partial products for the tens-and-ones split.' if L == 0 else 'Find the product using partial products. What is the first partial product (place-value part times ' + str(k) + ')?', n(k * t), f'{k} × {n(t)} = {n(k * t)}.'),
        ('What is the second partial product?', n(k * o), f'{k} × {o} = {n(k * o)}.'),
        ('How many eggs are packed in all?', n(k * a), f'{n(k * t)} + {n(k * o)} = {n(k * a)}.'),
        ('Explain why the partial products add to the full product.', S + f'{n(a)} = {n(t)} + {o}, so {k} groups of {n(a)} are {k} groups of {n(t)} plus {k} groups of {o}.', 'Use the distributive property.')])


@orq(MS, 4)
def o_ms4(r, L):
    a, b = r.randint(11, [29, 59, 99][L]), r.randint(11, [29, 59, 99][L]); need(a % 10 and b % 10)
    at, ao, bt, bo = a // 10 * 10, a % 10, b // 10 * 10, b % 10
    return ('ms4_open_area_model', f'A rectangular floor is {a} feet by {b} feet. Use an area model with {at} + {ao} and {bt} + {bo}.', [
        ('What are the four partial products? Give their sum.', n(a * b), f'{at}×{bt} = {at * bt}, {at}×{bo} = {at * bo}, {ao}×{bt} = {ao * bt}, {ao}×{bo} = {ao * bo}; sum {n(a * b)}.'),
        ('What is the area of the floor?', f'{n(a * b)} square feet', f'{a} × {b} = {n(a * b)}.'),
        ('Estimate the area by rounding each side to the nearest ten.', f'{n(rnd(a, 10) * rnd(b, 10))} square feet', f'{rnd(a, 10)} × {rnd(b, 10)} = {n(rnd(a, 10) * rnd(b, 10))}.'),
        ('Explain how the area model shows the product.', S + 'The rectangle is split into four smaller rectangles; their areas add up to the whole area.', 'Each part is a partial product.')])


@orq(MS, 5)
def o_ms5(r, L):
    p = r.randint(6, [15, 30, 60][L]); k = r.randint(12, [25, 40, 60][L]); b = r.choice([200, 500, 1000, 2000][L:L + 2])
    need(p * k != b)
    return ('ms5_open_trip', f'A trip costs ${p} per student. {k} students are going. The class has ${n(b)}.', [
        ('Estimate the total cost by rounding each number to the nearest ten.', f'${n(rnd(p, 10) * rnd(k, 10))}', f'{rnd(p, 10)} × {rnd(k, 10)} = {n(rnd(p, 10) * rnd(k, 10))}.'),
        ('Find the exact cost.', f'${n(p * k)}', f'{p} × {k} = {n(p * k)}.'),
        (f'How much money is left over, or how much more is needed? Give the amount.', f'${n(abs(b - p * k))}', f'{n(b)} − {n(p * k)}: {"left" if b > p * k else "short"} by ${n(abs(b - p * k))}.'),
        ('Explain whether the class has enough money.', S + ('Yes, the cost is less than the money they have.' if b >= p * k else 'No, the cost is more than the money they have.'), 'Compare the cost with the money.')])


@orq(DV, 1)
def o_dv1(r, L):
    d, q = r.randint(2, 9), r.randint(2, 9); p = [1, 10, 100][L]
    return ('dv1_open_share', f'{n(d * q * p)} stickers are shared equally among {d} friends.', [
        ('How many stickers does each friend get?', n(q * p), f'{n(d * q * p)} ÷ {d} = {n(q * p)}.'),
        ('Write the related multiplication fact.', f'{d} × {n(q * p)} = {n(d * q * p)}', 'Divisor × quotient = dividend.'),
        (f'If the stickers were shared among {q} friends instead, how many would each get?', n(d * p), f'{n(d * q * p)} ÷ {q} = {n(d * p)}.'),
        ('Explain how multiplication helps you divide.', S + 'Dividing asks what number times the divisor makes the dividend, so a multiplication fact gives the answer.', 'Division and multiplication are related.')])


@orq(DV, 2)
def o_dv2(r, L):
    d = r.randint(3, 9); a, b = r.choice([[10, 20], [100, 200], [100, 300]][L]), r.randint(2, [9, 30, 60][L]); total = d * (a + b)
    need(total < 10000)
    return ('dv2_open_partial_quotients', f'Use partial quotients to divide {n(total)} by {d}.', [
        (f'Subtract {d} × {a} first. What is left?', n(total - d * a), f'{n(total)} − {n(d * a)} = {n(total - d * a)}.'),
        (f'How many groups of {d} are in what is left?', str(b), f'{n(total - d * a)} ÷ {d} = {b}.'),
        ('What is the quotient?', str(a + b), f'{a} + {b} = {a + b}.'),
        ('Explain why you can add the partial quotients.', S + 'Each partial quotient counts some of the groups of ' + str(d) + '; together they count all the groups.', 'Add the groups you took away.')])


@orq(DV, 3)
def o_dv3(r, L):
    d = r.randint(3, 9); q = r.randint([12, 105, 1001][L], [99, 999, 1111][L]); total = d * q; need(total < 10000)
    return ('dv3_open_rows', f'{n(total)} chairs are set up in {d} equal rows.', [
        ('How many chairs are in each row?', n(q), f'{n(total)} ÷ {d} = {n(q)}.'),
        ('Check your answer with multiplication. What product do you get?', n(total), f'{n(q)} × {d} = {n(total)}.'),
        (f'If {d} more chairs are added, one to each row, how many chairs are in each row?', n(q + 1), f'{n(q)} + 1 = {n(q + 1)}.'),
        ('Explain how you decided where to put the first digit of the quotient.', S + 'If the first digit of the dividend is less than the divisor, I use the first two digits, so the quotient starts one place to the right.', 'Compare the leading digits with the divisor.')])


@orq(DV, 4)
def o_dv4(r, L):
    d = r.randint(3, 9); q = r.randint([5, 20, 100][L], [12, 99, 999][L]); rem = r.randint(1, d - 1); total = d * q + rem
    need(total < 10000)
    return ('dv4_open_remainder', f'{n(total)} marbles are put into bags of {d}.', [
        ('Write the quotient and remainder.', f'{q} R {rem}', f'{n(total)} ÷ {d} = {q} R {rem}.'),
        ('How many full bags are there?', str(q), f'The quotient {q} is the number of full bags.'),
        ('How many more marbles would fill one more bag?', str(d - rem), f'{d} − {rem} = {d - rem}.'),
        ('Explain why the remainder must be less than ' + str(d) + '.', S + f'If {d} or more were left, they would make another full bag.', 'Compare the remainder with the divisor.')])


@orq(DV, 5)
def o_dv5(r, L):
    per = r.randint(4, 9); g = r.randint([3, 10, 40][L], [9, 30, 120][L]); rem = r.randint(1, per - 1); total = per * g + rem
    return ('dv5_open_vans', f'{total} people are going on a trip. Each van holds {per} people.', [
        ('Divide. Write the quotient and remainder.', f'{g} R {rem}', f'{total} ÷ {per} = {g} R {rem}.'),
        ('How many vans are needed?', str(g + 1), f'The {rem} extra people need one more van: {g + 1}.'),
        ('How many vans are completely full?', str(g), f'{g} vans are full.'),
        ('Explain why you round up for the number of vans.', S + 'Every person needs a seat, so the people left over need one more van.', 'Think about the people left over.')])


@orq(FM, 1)
def o_fm1(r, L):
    k = r.choice([[12, 16, 18, 20], [24, 30, 36, 40, 42], [48, 60, 72, 84, 90, 96]][L]); fs = factors(k)
    return ('fm1_open_garden', f'A gardener has {k} plants to arrange in a rectangle with equal rows.', [
        ('List all the factor pairs.', '; '.join(f'{a} × {k // a}' for a in fs if a * a <= k), 'Find pairs of numbers that multiply to ' + str(k) + '.'),
        ('How many factors does ' + str(k) + ' have?', str(len(fs)), f'{", ".join(map(str, fs))}.'),
        ('Which arrangement is closest to a square? Give the number of rows (the smaller number).', str(max(a for a in fs if a * a <= k)), 'Choose the pair with the closest numbers.'),
        ('Explain how you know you found every factor pair.', S + 'I tested each number from 1 up until the factors started to repeat.', 'Stop when the pairs repeat.')])


@orq(FM, 2)
def o_fm2(r, L):
    a, b = r.choice([[(2, 3), (2, 5), (3, 4)], [(4, 6), (3, 5), (6, 8)], [(6, 9), (8, 12), (6, 10)]][L])
    l = a * b // fams.math.gcd(a, b)
    return ('fm2_open_packs', f'Hot dogs come in packs of {a}. Buns come in packs of {b}.', [
        (f'List the first five multiples of {a}.', ', '.join(str(a * i) for i in range(1, 6)), 'Count by ' + str(a) + '.'),
        (f'List the first five multiples of {b}.', ', '.join(str(b * i) for i in range(1, 6)), 'Count by ' + str(b) + '.'),
        ('What is the least number of hot dogs and buns that match exactly?', str(l), f'{l} is the first number on both lists.'),
        ('Explain how factors and multiples are related here.', S + f'{l} is a multiple of both {a} and {b}, so {a} and {b} are both factors of {l}.', 'A number is a multiple of each of its factors.')])


@orq(FM, 3)
def o_fm3(r, L):
    lo = [2, 20, 50][L]; hi = lo + [10, 15, 20][L]; ps = [p for p in PRIMES if lo <= p <= hi]; c = next(x for x in range(lo, hi) if x not in ps and x > 1)
    return ('fm3_open_sort', f'Look at the whole numbers from {lo} to {hi}.', [
        ('List the prime numbers.', ', '.join(map(str, ps)), 'A prime has exactly two factors.'),
        ('How many of the numbers are composite?', str(sum(1 for x in range(lo, hi + 1) if x > 1 and x not in ps)), 'Count the numbers that are not prime (1 is neither).'),
        (f'Show that {c} is composite: give a factor of {c} other than 1 and {c}.', str(next(d for d in range(2, c) if c % d == 0)), f'{c} = {next(d for d in range(2, c) if c % d == 0)} × {c // next(d for d in range(2, c) if c % d == 0)}.'),
        ('Explain why 2 is the only even prime number.', S + 'Every other even number has 2 as a factor, so it has more than two factors.', 'Think about the factor 2.')])


@orq(FM, 4)
def o_fm4(r, L):
    s, a = r.randint(1, 10), r.randint(2, [5, 9, 15][L]); k = [6, 8, 12][L]
    seq = [s + a * i for i in range(5)]
    odd = all(x % 2 for x in seq)
    return ('fm4_open_rule', f'A pattern starts at {s} and follows the rule "add {a}."', [
        ('Write the first five numbers.', ', '.join(map(str, seq)), f'Start at {s} and add {a} each time.'),
        (f'What is the {fams.ORD[k - 1]} number?', str(s + a * (k - 1)), f'{s} + {k - 1} × {a} = {s + a * (k - 1)}.'),
        ('Is ' + str(s + a * 20) + ' in the pattern? Answer yes or no.', 'yes', f'{s + a * 20} = {s} + 20 × {a}.'),
        ('Describe a feature of the pattern that the rule does not say.', S + ('The numbers alternate between odd and even.' if a % 2 else ('All the numbers are odd.' if s % 2 else 'All the numbers are even.')), 'Look at odd and even numbers or the ones digits.')])


@orq(FM, 5)
def o_fm5(r, L):
    s, a = r.randint(2, 6), r.randint(2, [3, 4, 5][L]); k = [6, 10, 15][L]
    return ('fm5_open_tiles', f'Figure 1 has {s} tiles. Each figure has {a} more tiles than the one before.', [
        ('How many tiles are in Figure 4?', str(s + 3 * a), f'{s} + 3 × {a} = {s + 3 * a}.'),
        (f'How many tiles are in Figure {k}?', str(s + (k - 1) * a), f'{s} + {k - 1} × {a} = {s + (k - 1) * a}.'),
        ('Which figure has ' + str(s + 7 * a) + ' tiles?', 'Figure 8', f'({s + 7 * a} − {s}) ÷ {a} = 7 steps after Figure 1.'),
        ('Explain how you can find the number of tiles in any figure.', S + f'Start with {s} and add {a} for each figure after Figure 1.', 'Use the rule.')])


@orq(FE, 1)
def o_fe1(r, L):
    b = r.choice([2, 3, 4, 6]); a = r.randint(1, b - 1); k = r.choice([2, 3, 4, 6]); need(b * k <= 12)
    return ('fe1_open_brownies', f'A pan of brownies is cut into {b} equal pieces, and {a} {"is" if a == 1 else "are"} eaten. Each piece is then cut into {k} smaller equal pieces.', [
        ('What fraction of the pan was eaten, in the first pieces?', f'{a}/{b}', f'{a} of {b} pieces.'),
        ('How many small pieces is that?', str(a * k), f'{a} × {k} = {a * k}.'),
        ('Write the eaten amount using the small pieces.', f'{a * k}/{b * k}', f'There are {b * k} small pieces in all.'),
        ('Explain why the two fractions are equal.', S + 'The same amount of the pan is eaten; it is just cut into more, smaller pieces.', 'The number and the size of the pieces both change.')])


@orq(FE, 2)
def o_fe2(r, L):
    b = r.choice([2, 3, 4, 5, 6]); a = r.randint(1, b - 1); ks = [k for k in (2, 3, 4) if b * k <= 12]; need(len(ks) >= 2)
    return ('fe2_open_equivalents', f'Hana says {a}/{b} = {a * ks[0]}/{b * ks[0]}.', [
        ('What number were the numerator and denominator multiplied by?', str(ks[0]), f'{b} × {ks[0]} = {b * ks[0]}.'),
        (f'Write another fraction equal to {a}/{b} with denominator {b * ks[1]}.', f'{a * ks[1]}/{b * ks[1]}', f'Multiply by {ks[1]}.'),
        (f'Write {a * ks[0]}/{b * ks[0]} in simplest form.', f'{a}/{b}', f'Divide by {ks[0]}.'),
        ('Explain why multiplying the top and bottom by the same number keeps the value.', S + 'It is the same as multiplying by 1, like 2/2; the parts get smaller but there are more of them.', 'n/n = 1.')])


@orq(FE, 3)
def o_fe3(r, L):
    a1, a2 = r.sample(range(1, 7), 2); b = r.choice([8, 10, 12]); c = r.randint(1, 4); b1, b2 = r.sample([3, 4, 5, 6, 8], 2); need(c < min(b1, b2))
    return ('fe3_open_compare', f'Liam ate {a1}/{b} of a pizza and Mei ate {a2}/{b} of the same pizza. Ana ate {c}/{b1} of a cake and Sam ate {c}/{b2} of the same size cake.', [
        ('Who ate more pizza?', 'Liam' if a1 > a2 else 'Mei', 'Same denominator: compare numerators.'),
        ('Who ate more cake?', 'Ana' if b1 < b2 else 'Sam', 'Same numerator: fewer pieces means bigger pieces.'),
        ('Write <, > or = to compare ' + f'{c}/{b1} ___ {c}/{b2}.', '>' if b1 < b2 else '<', 'Compare the size of the pieces.'),
        ('Explain why you can only compare these fractions when the wholes are the same size.', S + 'A fraction of a bigger whole can be more than the same fraction of a smaller whole.', 'The whole matters.')])


@orq(FE, 4)
def o_fe4(r, L):
    def pick(big):
        while True:
            b = r.choice([3, 4, 5, 6, 8, 10, 12]); a = r.randint(1, b - 1)
            if (2 * a > b) == big and 2 * a != b:
                return a, b
    (a1, b1), (a2, b2) = pick(True), pick(False)
    return ('fe4_open_benchmark', f'Femi ran {a1}/{b1} mile. Grace ran {a2}/{b2} mile.', [
        (f'Is {a1}/{b1} greater than or less than 1/2?', 'greater', f'{a1} is more than half of {b1}.'),
        (f'Is {a2}/{b2} greater than or less than 1/2?', 'less', f'{a2} is less than half of {b2}.'),
        ('Who ran farther?', 'Femi', 'More than 1/2 is greater than less than 1/2.'),
        ('Explain how the benchmark 1/2 helped.', S + 'One fraction is more than 1/2 and the other is less, so I did not need common denominators.', 'Compare each with 1/2.')])


@orq(FE, 5)
def o_fe5(r, L):
    fs = set()
    while len(fs) < 3:
        b = r.choice([2, 3, 4, 6, 12]); fs.add(Fr(r.randint(1, b - 1), b))
    fs = sorted(fs); shown = [f'{x.numerator * (12 // x.denominator) // (12 // x.denominator)}/{x.denominator}' for x in fs]
    names = r.sample(NAMES, 3); data = list(zip(names, fs)); r.shuffle(data)
    return ('fe5_open_order', 'Juice drunk: ' + '; '.join(f'{nm} {x.numerator}/{x.denominator} cup' for nm, x in data) + '.', [
        ('Write each amount in twelfths, in the order given.', ', '.join(f'{x.numerator * 12 // x.denominator}/12' for _, x in data), 'Multiply to make the denominator 12.'),
        ('Order the people from least to most juice.', ', '.join(nm for nm, x in sorted(data, key=lambda t: t[1])), 'Compare the twelfths.'),
        ('How much more did the person who drank the most drink than the person who drank the least? Write twelfths.', f'{(fs[-1] - fs[0]) * 12}/12', f'{fs[-1] * 12}/12 − {fs[0] * 12}/12 = {(fs[-1] - fs[0]) * 12}/12.'),
        ('Explain why twelfths work for all three fractions.', S + '12 is a multiple of each denominator, so each fraction can be written in twelfths.', 'Use a common denominator.')])


@orq(FD, 1)
def o_fd1(r, L):
    b = r.choice([5, 6, 8, 10]); a = r.randint(3, b - 1)
    return ('fd1_open_decompose', f'A recipe needs {a}/{b} cup of milk. Uma uses a 1/{b} cup scoop.', [
        ('How many scoops does Uma need?', str(a), f'{a}/{b} = {a} × 1/{b}.'),
        (f'Write {a}/{b} as a sum of unit fractions.', ' + '.join([f'1/{b}'] * a), f'{a} copies of 1/{b}.'),
        (f'Write {a}/{b} as a sum of two fractions, one of them 1/{b}.', f'1/{b} + {a - 1}/{b}', f'{a} = 1 + {a - 1}.'),
        ('Explain why there is more than one way to decompose a fraction.', S + 'The numerator can be split into different whole-number parts that add to it.', 'Split the numerator.')])


@orq(FD, 2)
def o_fd2(r, L):
    b = r.choice([6, 8, 10, 12]); x, y = r.randint(1, b // 2), r.randint(1, b // 2); need(x + y < b)
    return ('fd2_open_paint', f'A fence is split into {b} equal parts. Kai paints {x}/{b} of it in the morning and {y}/{b} in the afternoon.', [
        ('How much of the fence is painted?', f'{x + y}/{b}', f'{x}/{b} + {y}/{b} = {x + y}/{b}.'),
        ('How much is left to paint?', f'{b - x - y}/{b}', f'1 = {b}/{b}; {b}/{b} − {x + y}/{b} = {b - x - y}/{b}.'),
        ('How much more did Kai paint in the ' + ('morning' if x >= y else 'afternoon') + '?', f'{abs(x - y)}/{b}', f'{max(x, y)}/{b} − {min(x, y)}/{b} = {abs(x - y)}/{b}.'),
        ('Explain why the denominator does not change when you add.', S + 'The pieces stay the same size; you are only counting how many pieces.', 'Same-size parts.')])


@orq(FD, 3)
def o_fd3(r, L):
    b = r.choice([4, 6, 8]); w1, a1, w2, a2 = r.randint(1, 4), r.randint(1, b - 1), r.randint(1, 3), r.randint(1, b - 1)
    s_ = Fr(w1 * b + a1, b) + Fr(w2 * b + a2, b)
    return ('fd3_open_trail', f'Ava hikes {w1} {a1}/{b} miles on Saturday and {w2} {a2}/{b} miles on Sunday.', [
        ('How far does she hike in all?', f'{F(s_)} miles', f'{w1 + w2} {a1 + a2}/{b}' + (f' = {F(s_)}' if a1 + a2 >= b else '') + '.'),
        ('How much farther does she hike on the longer day?', qty(F(abs(Fr(w1 * b + a1, b) - Fr(w2 * b + a2, b))), 'miles'), 'Subtract the shorter distance from the longer one.'),
        ('Write the total as a fraction greater than 1.', f'{s_.numerator}/{b}' if s_.denominator == b else f'{s_.numerator * (b // s_.denominator)}/{b}', f'Wholes × {b} + numerator.'),
        ('Explain how you added the mixed numbers.', S + 'I added the whole numbers, added the fractions, and regrouped if the fractions made more than 1.', 'Wholes and parts.')])


@orq(FD, 4)
def o_fd4(r, L):
    b = r.choice([3, 4, 6, 8]); a = r.randint(1, b - 1); k = r.randint(3, [6, 9, 12][L])
    p = Fr(a * k, b)
    return ('fd4_open_recipe', f'One batch of muffins uses {a}/{b} cup of sugar. Ravi makes {k} batches.', [
        ('Write a multiplication expression.', f'{k} × {a}/{b}', f'{k} groups of {a}/{b}.'),
        ('How much sugar does Ravi use, as a fraction?', f'{a * k}/{b}', f'{k} × {a} = {a * k}, so {a * k}/{b}.'),
        ('Write the amount as a whole or mixed number.', F(p), f'{a * k}/{b} = {F(p)}.'),
        ('Explain why ' + f'{k} × {a}/{b}' + ' is the same as ' + f'{a * k} × 1/{b}.', S + f'Each batch is {a} copies of 1/{b}, so {k} batches are {a * k} copies of 1/{b}.', 'Count unit fractions.')])


@orq(FD, 5)
def o_fd5(r, L):
    t, h = r.randint(2, 9), r.randint(1, 9)
    v = t * 10 + h
    return ('fd5_open_grid', f'On a hundred grid, {t} columns of 10 and {h} more squares are shaded.', [
        ('What fraction of the grid is shaded? Use denominator 100.', f'{v}/100', f'{t} × 10 + {h} = {v} squares.'),
        ('Write the shaded part as a decimal.', f'0.{v:02d}', f'{v} hundredths = 0.{v:02d}.'),
        ('Write the shaded columns alone as tenths.', f'{t}/10', f'{t} columns = {t} tenths.'),
        ('Explain why 0.' + str(t) + ' and 0.' + str(t) + '0 are equal.', S + f'{t} tenths is the same amount as {t * 10} hundredths, so 0.{t} = 0.{t}0.', 'Tenths and hundredths.')])


@orq(FD, 6)
def o_fd6(r, L):
    xs = sorted(r.sample(range(11, 99), 3)); need(all(x % 10 for x in xs))
    names = r.sample(NAMES, 3); data = list(zip(names, xs)); r.shuffle(data)
    return ('fd6_open_jumps', 'Long jumps, in meters: ' + '; '.join(f'{nm} 2.{x:02d}' for nm, x in data) + '.', [
        ('Who jumped the farthest?', max(data, key=lambda t: t[1])[0], 'Compare the tenths, then the hundredths.'),
        ('Order the jumps from shortest to longest.', ', '.join(f'2.{x:02d}' for x in xs), 'Compare place by place.'),
        ('How much farther was the longest jump than the shortest? Write a decimal.', f'0.{xs[2] - xs[0]:02d}', f'{xs[2]} − {xs[0]} = {xs[2] - xs[0]} hundredths.'),
        ('Explain why 2.5 is greater than 2.45.', S + '2.5 = 2.50, and 50 hundredths is more than 45 hundredths.', 'Write both in hundredths.')])


@orq(MC, 1)
def o_mc1(r, L):
    big, small, k = r.choice([('feet', 'inches', 12), ('yards', 'feet', 3), ('pounds', 'ounces', 16), ('gallons', 'quarts', 4)]); a = r.randint(2, 6); b = r.randint(1, k - 1)
    return ('mc1_open_table', f'Make a table that converts {big} to {small}.', [
        (f'1 {SING(big)} = ___ {small}', str(k), f'1 {SING(big)} = {k} {small}.'),
        (f'{a} {big} = ___ {small}', str(a * k), f'{a} × {k} = {a * k}.'),
        (f'{a} {big} {b} {small} = ___ {small}', str(a * k + b), f'{a * k} + {b} = {a * k + b}.'),
        ('Explain why the number of ' + small + ' is greater than the number of ' + big + '.', S + f'A {SING(small)} is a smaller unit, so it takes more of them to measure the same amount.', 'Smaller units, more of them.')])


def SING(u):
    return fams.SINGULAR.get(u, u)


@orq(MC, 2)
def o_mc2(r, L):
    big, small, k = r.choice([('meters', 'centimeters', 100), ('kilometers', 'meters', 1000), ('kilograms', 'grams', 1000), ('liters', 'milliliters', 1000)]); a = r.randint(2, 6); c = r.randint(k // 10, k // 2)
    return ('mc2_open_convert', f'Rosa has {a} {big} of {THING[small]}.', [
        (f'How many {small} is that?', f'{n(a * k)} {small}', f'{a} × {n(k)} = {n(a * k)}.'),
        (f'She uses {n(c)} {small}. How many {small} are left?', f'{n(a * k - c)} {small}', f'{n(a * k)} − {n(c)} = {n(a * k - c)}.'),
        (f'Write what is left as {big} and {small}.', f'{qty((a * k - c) // k, big)} {(a * k - c) % k} {small}' if (a * k - c) % k else qty((a * k - c) // k, big), f'{n(a * k - c)} = {(a * k - c) // k} × {n(k)} + {(a * k - c) % k}.'),
        ('Explain how you convert from a larger metric unit to a smaller one.', S + f'Multiply by {n(k)}, because each {SING(big)} is {n(k)} {small}.', 'Metric units go by 10, 100 and 1,000.')])


@orq(MC, 3)
def o_mc3(r, L):
    h = r.randint(1, 10); m = r.choice([5, 15, 20, 35, 40, 50]); d = r.choice([25, 40, 45, 55, 70, 85][L * 2:L * 2 + 2] or [45])
    e = h * 60 + m + d; eh, em = divmod(e, 60); need(eh <= 12)
    return ('mc3_open_movie', f'A show starts at {h}:{m:02d} and lasts {d} minutes.', [
        ('What time does it end? (Same morning or afternoon.)', f'{eh}:{em:02d}', f'{h}:{m:02d} + {d} minutes.'),
        ('How many minutes is it from the start to the next hour?', str(60 - m), f'60 − {m} = {60 - m}.'),
        ('Write the length of the show in hours and minutes.' if d >= 60 else 'How many seconds long is the show?', f'1 hour {d - 60} minutes' if d >= 60 else f'{d * 60} seconds', f'{d} minutes = 1 hour {d - 60} minutes.' if d >= 60 else f'{d} × 60 = {d * 60}.'),
        ('Explain how a number line helps you find elapsed time.', S + 'I jump to the next hour, then jump the rest of the minutes, and add the jumps.', 'Jump to friendly times.')])


@orq(MC, 4)
def o_mc4(r, L):
    p1, p2 = 5 * r.randint(40, 300), 5 * r.randint(40, 300); paid = 2000 if p1 + p2 < 2000 else 5000
    return ('mc4_open_shopping', f'Isla buys a kite for ${p1 / 100:.2f} and a ball for ${p2 / 100:.2f}. She pays with a ${paid // 100} bill.', [
        ('What is the total cost?', f'${(p1 + p2) / 100:.2f}', f'{p1 / 100:.2f} + {p2 / 100:.2f}.'),
        ('How much change does she get?', f'${(paid - p1 - p2) / 100:.2f}', f'{paid // 100}.00 − {(p1 + p2) / 100:.2f}.'),
        ('How much more does the more expensive item cost?', f'${abs(p1 - p2) / 100:.2f}', 'Subtract the prices.'),
        ('Explain how you can check the change.', S + 'Add the change to the total cost; it should equal the amount paid.', 'Count up.')])


@orq(MC, 5)
def o_mc5(r, L):
    l, w = r.randint(4, [12, 20, 30][L]), r.randint(3, [10, 15, 25][L]); need(l != w)
    w2s = [x for x in range(2, l * w) if (l * w) % x == 0 and x not in (l, w) and l * w // x not in (l, w) and x < l * w // x]; need(w2s); w2 = r.choice(w2s)
    return ('mc5_open_garden', f'A rectangular garden is {l} feet long and {w} feet wide.', [
        ('What is the area?', f'{l * w} square feet', f'{l} × {w} = {l * w}.'),
        ('How much fence goes around it?', f'{2 * (l + w)} feet', f'2 × ({l} + {w}) = {2 * (l + w)}.'),
        (f'A second garden has the same area and a width of {w2} feet. How long is it?', f'{l * w // w2} feet', f'{l * w} ÷ {w2} = {l * w // w2}.'),
        ('Explain the difference between area and perimeter.', S + 'Area counts the square units inside; perimeter is the distance around the outside.', 'Inside versus around.')])


@orq(GA, 1)
def o_ga1(r, L):
    a = r.choice([30, 45, 60, 120, 135, 150])
    return ('ga1_open_clock', f'Two rays meet at a point and make an angle of {a}°.', [
        ('Is the angle acute, right or obtuse?', 'acute' if a < 90 else 'obtuse', f'{a}° is {"less" if a < 90 else "more"} than 90°.'),
        ('What angle would make a straight angle with it?', f'{180 - a}°', f'180° − {a}° = {180 - a}°.'),
        ('Is that second angle acute, right or obtuse?', 'acute' if 180 - a < 90 else 'obtuse', f'{180 - a}° compared with 90°.'),
        ('Explain the difference between a line and a ray.', S + 'A line goes on forever in both directions; a ray has one endpoint and goes on in one direction.', 'Endpoints.')])


@orq(GA, 2)
def o_ga2(r, L):
    a, b = r.randint(10, 80), r.randint(90, 170)
    return ('ga2_open_protractor', f'On a protractor, ray QR passes through {a}° and ray QS passes through {b}° on the same scale.', [
        ('What is the measure of angle RQS?', f'{b - a}°', f'{b} − {a} = {b - a}.'),
        ('Is angle RQS acute, right or obtuse?', 'acute' if b - a < 90 else 'right' if b - a == 90 else 'obtuse', 'Compare with 90°.'),
        ('How many one-degree angles make up angle RQS?', str(b - a), f'An angle of n° is n one-degree angles.'),
        ('Explain why you subtract the two readings.', S + 'The angle is the turn between the rays, so it is the difference between where each ray points.', 'Neither ray is at 0°.')])


@orq(GA, 3)
def o_ga3(r, L):
    a, b = r.randint(20, 70), r.randint(20, 70)
    return ('ga3_open_split', f'Angle ABC is split by ray BD into angle ABD = {a}° and angle DBC = {b}°.', [
        ('What is angle ABC?', f'{a + b}°', f'{a} + {b} = {a + b}.'),
        ('Write an equation for angle ABC.', f'{a} + {b} = {a + b}', 'The parts add to the whole.'),
        (f'If angle ABC were a right angle and angle ABD were {a}°, what would angle DBC be?', f'{90 - a}°', f'90 − {a} = {90 - a}.'),
        ('Explain why angle measure is additive.', S + 'An angle split into parts without overlap has the same total turn as the parts together.', 'Parts and whole.')])


@orq(GA, 4)
def o_ga4(r, L):
    a, b = r.randint(25, 80), r.randint(25, 80); c = 180 - a - b; need(c > 0 and c != 90)
    return ('ga4_open_triangle', f'A triangle has angles of {a}° and {b}°.', [
        ('What is the third angle?', f'{c}°', f'180 − {a} − {b} = {c}.'),
        ('Classify the triangle by its angles.', 'acute' if max(a, b, c) < 90 else 'obtuse', f'Largest angle {max(a, b, c)}°.'),
        ('Can a triangle have two obtuse angles? Answer yes or no.', 'no', 'Two obtuse angles would be more than 180°.'),
        ('Explain how you classified the triangle.', S + 'I looked at the largest angle: less than 90° is acute, exactly 90° is right, more than 90° is obtuse.', 'Look at the largest angle.')])


@orq(GA, 5)
def o_ga5(r, L):
    sh = r.choice([('square', 4), ('rectangle', 2), ('equilateral triangle', 3), ('regular hexagon', 6)])
    half = r.randint(10, [20, 40, 80][L])
    return ('ga5_open_fold', f'Tessa folds a paper {sh[0]} along a line of symmetry.', [
        (f'How many lines of symmetry does {fams.an(sh[0])} have?', str(sh[1]), 'Count the folds that make matching halves.'),
        (f'One half has an area of {half} square inches. What is the area of the whole shape?', f'{2 * half} square inches', f'2 × {half} = {2 * half}.'),
        ('How many lines of symmetry does the letter A have?', '1', 'A vertical line through the top.'),
        ('Explain how you can test whether a line is a line of symmetry.', S + 'Fold along the line; if the two halves match exactly, it is a line of symmetry.', 'Fold and match.')])


@orq(DP, 1)
def o_dp1(r, L):
    vals = [Fr(r.choice([2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]), 4) for _ in range(8)]
    c = {}
    for v in vals:
        c[v] = c.get(v, 0) + 1
    mode = max(c, key=lambda v: (c[v], v))
    need(list(c.values()).count(c[mode]) == 1)
    return ('dp1_open_line_plot', 'Leaf lengths, in inches: ' + ', '.join(F(v) for v in vals) + '.', [
        ('How many X marks go on the line plot?', str(len(vals)), 'One X for each measurement.'),
        ('Which length has the most X marks?', qty(F(mode), 'inches'), 'Count each value.'),
        ('What is the difference between the longest and the shortest leaf?', qty(F(max(vals) - min(vals)), 'inches'), f'{F(max(vals))} − {F(min(vals))}.'),
        ('Explain how you placed the X marks for ' + F(vals[0]) + '.', S + f'I found {F(vals[0])} on the number line, counting quarter-inch tick marks, and stacked one X for each time it appears.', 'Find the value, then stack.')])


@orq(DP, 2)
def o_dp2(r, L):
    vals = [Fr(r.choice([1, 2, 3, 4, 5, 6, 7, 8]), 8) for _ in range(7)]
    return ('dp2_open_line_plot', 'Ribbon pieces, in feet: ' + ', '.join(F(v) for v in vals) + '.', [
        ('What is the total length of all the pieces?', qty(F(sum(vals)), 'feet'), 'Add the measurements.'),
        ('How much longer is the longest piece than the shortest?', qty(F(max(vals) - min(vals)), 'feet'), 'Subtract.'),
        (f'How many pieces are longer than 1/2 foot?', str(sum(1 for v in vals if v > Fr(1, 2))), 'Compare each with 4/8.'),
        ('Explain how a line plot makes these questions easier.', S + 'The X marks show each value and how often it appears, so you can find the largest, smallest and totals quickly.', 'See all the data at once.')])


@orq(DP, 3)
def o_dp3(r, L):
    a, b = r.randint(3, 8), r.randint(12, [25, 50, 99][L]); c = r.randint(5, 30); g = r.randint(3, 6)
    tot = a * b + c; need(tot % g == 0)
    return ('dp3_open_party', f'A class buys {a} packs of {b} balloons and {c} single balloons, then shares them equally among {g} tables.', [
        ('How many balloons are there?', str(tot), f'{a} × {b} + {c} = {tot}.'),
        ('How many balloons does each table get?', str(tot // g), f'{tot} ÷ {g} = {tot // g}.'),
        ('Write one expression for the balloons at each table.', f'({a} × {b} + {c}) ÷ {g}', 'Total, then share.'),
        ('Explain how you know your answer is reasonable.', S + f'About {a} × {rnd(b, 10)} + {c} is near {a * rnd(b, 10) + c}, and that shared among {g} is close to my answer.', 'Estimate.')])


@orq(DP, 4)
def o_dp4(r, L):
    k, per, extra = r.randint(3, 8), r.randint(12, [25, 45, 90][L]), r.randint(5, 30)
    t = k * per + extra
    return ('dp4_open_cards', f'Noah has {k} packs of cards with the same number in each pack, and {extra} loose cards. He has {t} cards in all.', [
        ('Write an equation using c for the cards in each pack.', f'{k} × c + {extra} = {t}', 'Packs times cards plus loose cards.'),
        ('How many cards are in each pack?', str(per), f'{t} − {extra} = {t - extra}; {t - extra} ÷ {k} = {per}.'),
        ('Check: what is ' + f'{k} × {per} + {extra}?', str(t), f'{k * per} + {extra} = {t}.'),
        ('Explain how you solved for c.', S + 'I took away the loose cards, then divided what was left equally among the packs.', 'Undo the steps.')])


def run(o):
    for u in UNITS:
        for skill in sorted(k for k in O if k.startswith(u + '-skill-')):
            items = [q for q in o.items(u) if q['skillId'] == skill]
            std = max((q['standards'] for q in items), key=lambda s: sum(1 for q in items if q['standards'] == s))
            for li, L in enumerate(['cp2', 'cp1', 'honors']):
                r = random.Random(f'g4-open|{skill}|{L}')
                for _ in range(500):
                    try:
                        fam, prompt, parts = O[skill](r, li)
                        break
                    except (Skip, StopIteration, ValueError, ZeroDivisionError):
                        continue
                else:
                    raise SystemExit('no open item for ' + skill)
                assert len(parts) == 4
                # equations, expressions and lists of pairs have more than one right form: the players self-check them
                parts = [(p, a if a.startswith(S) or not re.search(r'[=×+−]|; ', a) else S + a, st) for p, a, st in parts]
                qid = f'm4-{ABBR[u]}-s{skill[-2:]}-{L}-o01'
                q = {'id': qid, 'skillId': skill, 'level': L, 'format': 'open-response', 'prompt': prompt,
                     'parts': [{'prompt': p, 'answer': a} for p, a, _ in parts],
                     'answer': '; '.join(f'({chr(97 + i)}) {a}' for i, (_, a, _) in enumerate(parts)),
                     'solutionSteps': [f'({chr(97 + i)}) {s}' for i, (_, _, s) in enumerate(parts)], 'standards': std,
                     'sourceNotes': NOTE.format(fam=fam)}
                o.add(u, q, {'questionType': 'explain', 'tags': ['open-response'], 'explanation': parts[2][2]})
