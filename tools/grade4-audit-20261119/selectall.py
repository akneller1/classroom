"""4th Grade Math audit #8 (2026-11-19): on-skill select-all items with 2, 3 or 4 correct choices.

Before the audit every Grade 4 select-all item used one template ("Select ALL the problems that are matched with the
correct answer") and had exactly 2 correct choices. Each family below picks its correct and wrong choices from the
skill itself; one item per skill and level, 5 choices, with the number correct cycling 2, 3, 4. IDs end in -s01."""
import random
from fractions import Fraction as Fr
from lib import ABBR, UNITS, F, n
import fams
from fams import PRIMES, factors, rnd, Skip, need

NOTE = ('Original Claude-authored item (family: {fam}). 4th Grade Math audit 2026-11-19 (#8, select-all with {k} correct); '
        'every choice recomputed by scripts/test-grade4-audit.cjs.')
G = {}


def sel(unit, i):
    def d(f):
        G[f'{unit}-skill-{i:02d}'] = f; return f
    return d


def pick(r, good, bad, k):
    good, bad = list(dict.fromkeys(good)), [b for b in dict.fromkeys(bad) if b not in good]
    need(len(good) >= k and len(bad) >= 5 - k)
    return r.sample(good, k), r.sample(bad, 5 - k)


@sel(fams.PV, 3)
def s_pv3(r, L, k):
    t = r.randint([1000, 10000, 100000][L], [9000, 90000, 900000][L])
    near = [t + d for d in (-1000, -100, -10, -1, 1, 10, 100, 1000, 9, 90)]
    g, b = pick(r, [n(x) for x in near if x > t], [n(x) for x in near if x < t], k)
    return ('pv3_select_greater', f'Select ALL the numbers greater than {n(t)}.', g, b, [f'Compare each number with {n(t)} place by place from the left.'])


@sel(fams.PV, 4)
def s_pv4(r, L, k):
    u = [10, 100, 1000][L]; t = r.randint(20, 90) * u
    near = [t + d for d in range(-u, u + 1, max(1, u // 10))]
    g, b = pick(r, [n(x) for x in near if rnd(x, u) == t], [n(x) for x in near if rnd(x, u) != t], k)
    return ('pv4_select_rounds_to', f'Select ALL the numbers that round to {n(t)} when rounded to the nearest {fams.PLACE[u][:-1]}.', g, b,
            [f'Numbers from {n(t - u // 2)} up to {n(t + u // 2 - 1)} round to {n(t)}.'])


@sel(fams.MS, 2)
def s_ms2(r, L, k):
    a, b = r.randint(2, 9), r.randint(2, 9); p = [10, 100, 1000][L]; v = a * b * p
    good = [f'{a} × {n(b * p)}', f'{b} × {n(a * p)}', f'{n(a * b)} × {n(p)}', f'{a * 10} × {n(b * p // 10)}' if p >= 100 else f'{a * b} × {p}']
    bad = [f'{a} × {n(b * p * 10)}', f'{a + b} × {n(p)}', f'{a} × {b} × {n(p * 10)}', f'{b} × {n(a * p // 10)}' if p >= 100 else f'{a} × {b + p}']
    g, bd = pick(r, good, bad, k)
    return ('ms2_select_equal_products', f'Select ALL the expressions equal to {n(v)}.', g, bd, [f'{a} × {b} = {a * b}, and {n(v)} = {a * b} × {n(p)}.'])


@sel(fams.DV, 4)
def s_dv4(r, L, k):
    d = r.randint(3, 9); rem = r.randint(1, d - 1); lo = [10, 30, 100][L]
    good = [f'{d * q + rem} ÷ {d}' for q in r.sample(range(lo, lo * 3), 6)]
    bad = [f'{d * q + (rem + j) % d} ÷ {d}' for q in r.sample(range(lo, lo * 3), 6) for j in (1, 2) if (rem + j) % d != rem]
    g, b = pick(r, good, bad, k)
    return ('dv4_select_remainder', f'Select ALL the divisions that have a remainder of {rem}.', g, b, [f'Divide each one and look at what is left over after the last multiple of {d}.'])


@sel(fams.FM, 1)
def s_fm1(r, L, k):
    num = r.choice([[12, 16, 18, 20], [24, 30, 36, 40], [48, 60, 72, 84, 90]][L]); fs = [x for x in factors(num) if 1 < x < num]
    g, b = pick(r, [str(x) for x in fs], [str(x) for x in range(2, num) if num % x], k)
    return ('fm1_select_factors', f'Select ALL the factors of {num}.', g, b, [f'The factors of {num} are {", ".join(map(str, factors(num)))}.'])


@sel(fams.FM, 2)
def s_fm2(r, L, k):
    m = r.choice([[3, 4, 5], [6, 7, 8], [9, 11, 12]][L]); top = m * 12
    g, b = pick(r, [str(m * i) for i in range(2, 13)], [str(x) for x in range(m + 1, top) if x % m], k)
    return ('fm2_select_multiples', f'Select ALL the multiples of {m}.', g, b, [f'A multiple of {m} divides by {m} with no remainder.'])


@sel(fams.FM, 3)
def s_fm3(r, L, k):
    lo, hi = [(2, 30), (20, 60), (50, 100)][L]
    g, b = pick(r, [str(p) for p in PRIMES if lo <= p <= hi], [str(c) for c in range(max(lo, 4), hi) if c not in PRIMES and c % 2], k)
    return ('fm3_select_primes', 'Select ALL the prime numbers.', g, b, ['A prime number has exactly two factors, 1 and itself.'])


@sel(fams.FE, 2)
def s_fe2(r, L, k):
    b = r.choice([2, 3, 4, 5, 6][: 3 + L]); a = r.randint(1, b - 1); need(fams.math.gcd(a, b) == 1)
    good = [f'{a * m}/{b * m}' for m in range(2, 13) if b * m <= 12 or b * m == 100 or (L == 2 and b * m <= 24)]
    bad = [f'{a * m + 1}/{b * m}' for m in range(2, 7) if b * m <= 12] + [f'{a + m}/{b + m}' for m in range(1, 5)] + [f'{b}/{a}' if a > 1 else f'{b}/{a + 1}']
    g, bd = pick(r, good, [x for x in bad if Fr(x) != Fr(a, b)], k)
    return ('fe2_select_equivalent', f'Select ALL the fractions equivalent to {a}/{b}.', g, bd, [f'Multiply the numerator and denominator of {a}/{b} by the same number.'])


@sel(fams.FE, 4)
def s_fe4(r, L, k):
    cands = [f'{a}/{b}' for b in [3, 4, 5, 6, 8, 10, 12] for a in range(1, b) if 2 * a != b]
    g, b = pick(r, [c for c in cands if Fr(c) > Fr(1, 2)], [c for c in cands if Fr(c) < Fr(1, 2)], k)
    return ('fe4_select_greater_half', 'Select ALL the fractions greater than 1/2.', g, b, ['A fraction is greater than 1/2 when its numerator is more than half its denominator.'])


@sel(fams.FD, 4)
def s_fd4(r, L, k):
    b = r.choice([3, 4, 5, 6, 8, 10]); a = r.randint(1, b - 1); m = r.randint(3, [4, 6, 9][L])
    good = [f'{m * a}/{b}', f'{m * a} × 1/{b}', ' + '.join([f'{a}/{b}'] * m)] + ([F(Fr(m * a, b))] if m * a > b else [])
    bad = [f'{m * a}/{m * b}', f'{m + a}/{b}', f'{a}/{m * b}', ' + '.join([f'{a}/{b}'] * (m - 1))]
    g, bd = pick(r, good, bad, k)
    return ('fd4_select_equal_product', f'Select ALL the expressions equal to {m} × {a}/{b}.', g, bd, [f'{m} × {a}/{b} = {m * a}/{b}' + (f' = {F(Fr(m * a, b))}' if m * a > b else '') + '.'])


@sel(fams.FD, 5)
def s_fd5(r, L, k):
    v = r.randint(11, 99); need(v % 10)
    good = [f'0.{v:02d}', f'{v}/100', f'{v // 10}/10 + {v % 10}/100', f'{v // 10 * 10}/100 + {v % 10}/100']
    bad = [f'{v}/10', f'0.{v % 10}{v // 10}', f'{v // 10}.{v % 10}', f'{v // 10}/100 + {v % 10}/10']
    g, b = pick(r, good, bad, k)
    return ('fd5_select_equal_decimal', f'Select ALL the numbers equal to {v} hundredths.', g, b, [f'{v} hundredths = {v}/100 = 0.{v:02d} = {v // 10} tenths + {v % 10} hundredths.'])


@sel(fams.FD, 6)
def s_fd6(r, L, k):
    t = r.randint(2, 8); x = f'0.{t}'
    good = [f'0.{t}{d}' for d in range(1, 10)] + [f'0.{t + 1}', f'0.{t + 1}{r.randint(0, 9)}']
    bad = [f'0.{t - 1}{d}' for d in range(1, 10)] + [f'0.0{t}', f'0.{t - 1}']
    g, b = pick(r, good, bad, k)
    return ('fd6_select_greater_decimal', f'Select ALL the decimals greater than {x}.', g, b, [f'{x} = 0.{t}0. Compare the tenths first, then the hundredths.'])


@sel(fams.MC, 1)
def s_mc1(r, L, k):
    ft = r.choice([3, 6, 9, 12][L:L + 2])
    good = [f'{ft * 12} inches', f'{ft // 3} yard{"s" if ft // 3 > 1 else ""}', f'{ft - 1} feet 12 inches', f'{ft - 2} feet 24 inches']
    bad = [f'{ft * 10} inches', f'{ft * 3} yards', f'{ft} yards', f'{ft * 12 + 12} inches']
    g, b = pick(r, good, bad, k)
    return ('mc1_select_equal_length', f'Select ALL the lengths equal to {ft} feet.', g, b, [f'1 foot = 12 inches and 1 yard = 3 feet, so {ft} feet = {ft * 12} inches = {ft // 3} yard{"s" if ft // 3 > 1 else ""}.'])


@sel(fams.MC, 5)
def s_mc5(r, L, k):
    A = r.choice([[12, 18, 20, 24], [24, 30, 36, 40], [48, 60, 72]][L]); pairs = [(a, A // a) for a in factors(A) if a <= A // a]
    good = [f'{a} ft by {b} ft' for a, b in pairs]
    bad = [f'{a} ft by {b + 1} ft' for a, b in pairs] + [f'{a + 1} ft by {b} ft' for a, b in pairs if (a + 1) * b != A]
    g, bd = pick(r, good, [x for x in bad if x not in good], k)
    return ('mc5_select_area', f'Select ALL the rectangles with an area of {A} square feet.', g, bd, [f'Area = length × width; the pairs whose product is {A} work.'])


@sel(fams.GA, 1)
def s_ga1(r, L, k):
    kind = r.choice(['acute', 'obtuse'])
    angs = list(range(5, 180, 5))
    good = [f'{a}°' for a in angs if (a < 90 if kind == 'acute' else a > 90)]
    bad = [f'{a}°' for a in angs if (a > 90 if kind == 'acute' else a < 90)] + ['90°']
    g, b = pick(r, good, bad, k)
    return ('ga1_select_angle_type', f'Select ALL the measures of {kind} angles.', g, b, [f'An {kind} angle is {"less" if kind == "acute" else "greater"} than 90°' + ('.' if kind == 'acute' else ' and less than 180°.')])


@sel(fams.GA, 4)
def s_ga4(r, L, k):
    shape, good, bad = r.choice([('a square', ['rectangle', 'rhombus', 'parallelogram', 'quadrilateral'], ['trapezoid', 'triangle', 'pentagon']),
                                 ('a rectangle that is not a square', ['parallelogram', 'quadrilateral'], ['rhombus', 'square', 'trapezoid', 'triangle']),
                                 ('a rhombus that is not a square', ['parallelogram', 'quadrilateral'], ['rectangle', 'square', 'trapezoid', 'triangle'])])
    need(len(good) >= k)
    g, b = pick(r, good, bad, k)
    return ('ga4_select_names', f'Select ALL the names that describe {shape}.', g, b, ['Check the sides, the parallel sides and the angles each name needs.'])


@sel(fams.GA, 5)
def s_ga5(r, L, k):
    shapes = {'square': 4, 'rectangle (not a square)': 2, 'equilateral triangle': 3, 'regular hexagon': 6, 'isosceles triangle (not equilateral)': 1,
              'rhombus (not a square)': 2, 'parallelogram (not a rectangle or rhombus)': 0, 'regular pentagon': 5, 'scalene triangle': 0, 'circle': 'many'}
    t = r.choice([1, 2, 3])
    good = [s for s, v in shapes.items() if v != 'many' and v != 0 and v >= t]
    bad = [s for s, v in shapes.items() if v == 0 or (v != 'many' and v < t)]
    g, b = pick(r, good, bad, k)
    return ('ga5_select_symmetry', f'Select ALL the shapes that have at least {t} line{"s" if t > 1 else ""} of symmetry.', g, b,
            ['; '.join(f'{s}: {v}' for s, v in shapes.items() if v != 'many') + '.'])


@sel(fams.FE, 3)
def s_fe3(r, L, k):
    b = r.choice([6, 8, 10, 12]); a = r.randint(3, b - 2)
    good = [f'{x}/{b}' for x in range(1, a)] + [f'{a}/{b + m}' for m in (1, 2, 4)]
    bad = [f'{x}/{b}' for x in range(a + 1, b)] + [f'{a}/{b - m}' for m in (1, 2) if b - m > a]
    g, bd = pick(r, good, bad, k)
    return ('fe3_select_less', f'Select ALL the fractions less than {a}/{b}.', g, bd, [f'Same denominator: a smaller numerator is less. Same numerator: a larger denominator is less.'])


@sel(fams.DP, 4)
def s_dp4(r, L, k):
    a, b, c = r.randint(3, 9), r.randint(5, [12, 25, 60][L]), r.randint(2, 20)
    v = a * b + c
    good = [f'{a} × {b} + {c}', f'{c} + {a} × {b}', f'{b} × {a} + {c}', f'{a * b} + {c}']
    bad = [f'{a} × ({b} + {c})', f'{a} + {b} × {c}', f'{a} × {b} − {c}', f'{a + b} + {c}']
    g, bd = pick(r, good, [x for x in bad if eval(x.replace('×', '*').replace('−', '-')) != v], k)
    return ('dp4_select_expression', f'Kai has {a} bags with {b} marbles in each and {c} loose marbles. Select ALL the expressions for the total number of marbles.', g, bd, [f'The total is {a} × {b} + {c} = {v}; order of the factors and the addends can change.'])


def run(o):
    i = 0
    for u in UNITS:
        for skill in sorted(x for x in G if x.startswith(u + '-skill-')):
            items = [q for q in o.items(u) if q['skillId'] == skill]
            std = max((q['standards'] for q in items), key=lambda s: sum(1 for q in items if q['standards'] == s))
            for li, L in enumerate(['cp2', 'cp1', 'honors']):
                k = 2 + (i % 3); i += 1
                r = random.Random(f'g4-sel|{skill}|{L}')
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
                ans = [o_['text'] for o_ in opts if o_['correct']]
                steps = steps + ['Correct choices: ' + '; '.join(ans) + '. Not correct: ' + '; '.join(t for t in bad) + '.']
                qid = f'm4-{ABBR[u]}-s{skill[-2:]}-{L}-s01'
                q = {'id': qid, 'skillId': skill, 'level': L, 'format': 'select-all', 'prompt': prompt, 'answer': ans, 'options': opts,
                     'solutionSteps': steps, 'standards': std, 'sourceNotes': NOTE.format(fam=fam, k=k)}
                o.add(u, q, {'questionType': 'conceptual', 'tags': ['select-all'], 'explanation': steps[0]})
