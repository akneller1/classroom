"""Discrete Math audit 2026-11-18, follow-up to #4: finish moving Advanced clones.
Batch B moved 140 Advanced items that reused a Support template but had to keep about 100 of them, because each skill needs
5 multiple-choice and 4 short-answer Advanced items for the Advanced game decks and Tarsia puzzles. This script writes one
new multi-step Advanced item for every remaining movable clone (same skill, same format; short prompts and answers so
Tarsia can use them), then moves the clones to Standard. Release-fixture items and partner-check targets keep their level.
Run once on the banks after batch C: python3 tools/discrete-audit-20261118/batch_d.py"""
import re, sys, os, math, itertools, collections, json, hashlib, random
from fractions import Fraction as Fr
sys.path.insert(0, os.path.dirname(__file__))
from lib import load, save, items, family, ROOT
import elect as E

B = load()
NOTE = 'Original Claude-authored Discrete Math item (family: {}). Discrete Math audit 2026-11-18 follow-up (tools/discrete-audit-20261118/batch_d.py): multi-step Advanced item; answer computed by the script.'
CODE = {'speaking-mathematically': 'sm', 'compound-statements-logic': 'lg', 'number-theory-proof': 'np', 'sequences-induction-recursion': 'sq',
        'set-theory': 'st', 'properties-relations': 'rl', 'counting-probability': 'cn', 'graphs-trees': 'gr', 'election-theory': 'el', 'linear-programming': 'lp'}
ids = {q['id'] for _, q in items(B)}
prompts = collections.defaultdict(set)
for u, q in items(B): prompts[u].add(q['prompt'])
fs = E.fs
S = lambda xs: '{' + ', '.join(str(x).replace('-', '−') for x in xs) + '}' if xs else '∅'


def near(a):
    """Numeric near misses for a whole-number or fraction answer."""
    v = Fr(a)
    if v.denominator == 1:
        n = v.numerator; c = [n + 1, n - 1, n + 2, 2 * n, n - 2]
        return [str(x) for x in c if x >= 0 and x != n]
    return [fs(v + Fr(1, v.denominator)), fs(v - Fr(1, v.denominator)) if v - Fr(1, v.denominator) > 0 else fs(v * 2), fs(Fr(v.numerator, v.denominator + 1)), fs(1 - v) if 0 < v < 1 else fs(v / 2)]


# ---------------- generators: g(k) -> (prompt, answer, steps, distractors) ----------------
def ev(f, env):
    return eval(f.replace('¬', ' not ').replace('∧', ' and ').replace('∨', ' or '), {}, env)


IMP = lambda a, b: (not a) or b
G = {}


def lg01(k):
    forms = [('(p ∨ q) → (r ∧ ¬q)', lambda p, q, r: IMP(p or q, r and not q)), ('¬(p ∧ r) ↔ (q ∨ ¬p)', lambda p, q, r: (not (p and r)) == (q or not p)),
             ('(p → q) ∧ (q → r)', lambda p, q, r: IMP(p, q) and IMP(q, r)), ('(¬p ∨ r) → (q ∧ p)', lambda p, q, r: IMP((not p) or r, q and p))]
    f, fn = forms[k % 4]; vals = [(True, False, True), (False, True, True), (True, True, False), (False, False, False)][k % 4]
    v = fn(*vals); tv = lambda b: 'T' if b else 'F'
    return (f'Let p be {tv(vals[0])}, q be {tv(vals[1])}, r be {tv(vals[2])}. Find the truth value of {f}. Answer T or F.', tv(v),
            ['Substitute the values, then work inside parentheses first: ¬, then ∧ and ∨, then → and ↔.',
             f'With p = {tv(vals[0])}, q = {tv(vals[1])}, r = {tv(vals[2])} each part evaluates in turn, and the main connective gives {tv(v)}.',
             'Remember: → is false only for T → F, and ↔ is true when both sides agree.'], ['T' if not v else 'F', 'Cannot be determined', 'Both T and F'])
G['compound-statements-logic-skill-01'] = lg01


def lg02(k):
    forms = ['(p → q) ∧ (q ∨ r)', '(p ↔ q) ∨ r', '¬(p ∧ q) ∧ (q → r)', '(p ∨ q) ∧ (p ∨ r) ∧ ¬(q ∧ r)']
    f = forms[k % 4]
    py = f.replace('¬', ' not ').replace('∧', ' and ').replace('∨', ' or ')
    rows = list(itertools.product([True, False], repeat=3))
    def val(p, q, r):
        g = py.replace('↔', '==')
        g = re.sub(r'\(([^()]*?) → ([^()]*?)\)', r'((not (\1)) or (\2))', g)
        return eval(g, {}, {'p': p, 'q': q, 'r': r})
    col = ''.join('T' if val(*rw) else 'F' for rw in rows); n = col.count('T')
    return (f'In how many of the 8 rows of its truth table is {f} true?', str(n),
            ['List the 8 rows (p, q, r) = TTT, TTF, …, FFF.', f'Evaluating row by row gives the column {col}.', f'It is true in {n} rows.'], near(n))
G['compound-statements-logic-skill-02'] = lg02


def lg05(k):
    cases = [('(p ∧ q) → r', 'p ∧ q ∧ ¬r', ['(p ∧ q) → ¬r', '¬p ∨ ¬q ∨ r', '¬r → ¬(p ∧ q)']),
             ('p → (q ∨ r)', 'p ∧ ¬q ∧ ¬r', ['p → ¬(q ∨ r)', '¬p ∨ q ∨ r', 'p ∧ (¬q ∨ ¬r)'])]
    a, ans, d = cases[k % 2]
    return (f'Which statement is equivalent to ¬({a})?', ans,
            ['¬(x → y) ≡ x ∧ ¬y: a conditional is false only when its hypothesis holds and its conclusion fails.',
             f'Here x = {a.split(" → ")[0]} and y = {a.split(" → ")[1]}; negate y with De Morgan\'s law.', f'Result: {ans}.'], d)
G['compound-statements-logic-skill-05'] = lg05


def cn01(k):
    s = [9, 11, 8, 12][k % 4]; n = sum(1 for t in itertools.product(range(1, 7), repeat=3) if sum(t) == s)
    return (f'Three distinguishable dice are rolled. How many ordered outcomes have sum {s}?', str(n),
            ['Outcomes are ordered triples (a, b, c) with each value 1 to 6.', f'List the multisets that add to {s} and count the orders of each (6 if all different, 3 if two match, 1 if all match).', f'Total: {n} outcomes.'], near(n))
G['counting-probability-skill-01'] = cn01


def cn02(k):
    lo, hi, a, b = [(200, 900, 9, 6), (1, 2026, 12, 8), (300, 800, 14, 4), (50, 950, 15, 9)][k % 4]
    m = lambda d: hi // d - (lo - 1) // d; l = math.lcm(a, b); n = m(a) - m(l)
    return (f'How many integers from {lo} to {hi} are multiples of {a} but not of {b}?', str(n),
            [f'Multiples of {a}: ⌊{hi}/{a}⌋ − ⌊{lo - 1}/{a}⌋ = {m(a)}.', f'Also multiples of {b} means multiples of lcm({a}, {b}) = {l}: {m(l)}.', f'{m(a)} − {m(l)} = {n}.'], near(n))
G['counting-probability-skill-02'] = cn02


def cn03(k):
    w, l = [(3, 3), (3, 2), (4, 2), (2, 3)][k % 4]
    def seqs(a, b):
        if a == w or b == l: return 1
        return seqs(a + 1, b) + seqs(a, b + 1)
    n = seqs(0, 0)
    return (f'A team plays until it has {w} wins or {l} losses. How many win–loss sequences are possible?', str(n),
            ['Draw the possibility tree: each game branches W or L, and a branch stops as soon as either target is reached.',
             f'Count the leaves: sequences ending on the {w}th win plus sequences ending on the {l}th loss.', f'Total: {n} sequences.'], near(n))
G['counting-probability-skill-03'] = cn03


def cn04(k):
    N, (a, b, c) = [(600, (2, 3, 7)), (1200, (4, 5, 6)), (900, (3, 4, 10)), (2026, (2, 7, 11))][k % 4]
    L = math.lcm; s1 = N // a + N // b + N // c; s2 = N // L(a, b) + N // L(a, c) + N // L(b, c); s3 = N // L(a, b, c); n = s1 - s2 + s3
    return (f'How many integers from 1 to {N} are divisible by {a}, {b} or {c}?', str(n),
            [f'Singles: {N // a} + {N // b} + {N // c} = {s1}.', f'Pairs (lcm {L(a, b)}, {L(a, c)}, {L(b, c)}): {s2}; all three (lcm {L(a, b, c)}): {s3}.', f'{s1} − {s2} + {s3} = {n}.'], near(n))
G['counting-probability-skill-04'] = cn04


def cn05(k):
    cases = [('4-digit odd numbers with all digits different', 4, lambda s: s[0] != '0' and int(s[-1]) % 2 and len(set(s)) == 4, 'Last digit odd (5 ways), first digit not 0 or the last (8 ways), middle 8·7: 5·8·8·7.'),
             ('3-digit numbers with all digits different and greater than 500', 3, lambda s: int(s) > 500 and len(set(s)) == 3, 'First digit 5–9 (5 ways), then 9 and 8 choices for the other places (500 itself repeats a digit): 5·9·8.'),
             ('4-digit numbers whose digits are all different and in increasing order', 4, lambda s: s[0] != '0' and all(s[i] < s[i + 1] for i in range(3)), 'An increasing number is just a choice of 4 different digits from 1–9 (0 cannot be first): C(9, 4).'),
             ('4-digit numbers with no repeated digit and no 0', 4, lambda s: '0' not in s and len(set(s)) == 4, 'Choose from the 9 nonzero digits without repetition: 9·8·7·6.')]
    d, dg, test, how = cases[k % 4]; n = sum(1 for x in range(10 ** (dg - 1), 10 ** dg) if test(str(x)))
    return (f'How many {d} are there?', str(n), ['Fill the most restricted place first and multiply the choices.', how, f'Total: {n}.'], near(n))
G['counting-probability-skill-05'] = cn05


def cn06(k):
    b, g, t, mg = [(7, 5, 4, 2), (6, 6, 5, 3), (8, 4, 4, 1), (5, 7, 4, 3)][k % 4]
    n = sum(math.comb(g, i) * math.comb(b, t - i) for i in range(mg, t + 1))
    return (f'A {t}-person committee is chosen from {b} boys and {g} girls. How many have at least {mg} girls?', str(n),
            [f'Split into cases by the number of girls i = {mg}, …, {t}; order does not matter, so use combinations.',
             ' + '.join(f'C({g}, {i})·C({b}, {t - i})' for i in range(mg, t + 1)) + f' = {n}.', 'Cases do not overlap, so the addition rule applies.'], near(n))
G['counting-probability-skill-06'] = cn06


def cn08(k):
    r, bl, d, x = [(5, 4, 3, 2), (6, 3, 3, 1), (4, 6, 4, 2), (7, 5, 3, 3)][k % 4]
    p = Fr(math.comb(r, x) * math.comb(bl, d - x), math.comb(r + bl, d))
    return (f'A bag has {r} red and {bl} blue marbles. {d} are drawn without replacement. Find P(exactly {x} red).', fs(p),
            [f'Total unordered draws: C({r + bl}, {d}) = {math.comb(r + bl, d)}.', f'Favorable: C({r}, {x})·C({bl}, {d - x}) = {math.comb(r, x) * math.comb(bl, d - x)}.', f'P = {math.comb(r, x) * math.comb(bl, d - x)}/{math.comb(r + bl, d)} = {fs(p)}.'], near(fs(p)))
G['counting-probability-skill-08'] = cn08


def el01(k):
    n, c = [(31, 4), (50, 3), (77, 5), (120, 7)][k % 4]; v = math.ceil((n + c - 1) / c)
    return (f'{n} voters, {c} candidates: what is the fewest first-place votes a unique plurality winner can have?', str(v),
            [f'If the winner has v votes, each rival has at most v − 1, so {c}v − {c - 1} ≥ {n}.', f'v ≥ ({n} + {c - 1})/{c} = {fs(Fr(n + c - 1, c))}, so v = {v}.', f'{v - 1} votes would leave too many votes for the rivals to all stay below the winner.'], near(v))
G['election-theory-skill-01'] = el01

_r = random.Random(77)


def el02(k):
    while True:
        rows = E.random_schedule(_r, 4, 5, 3, 14); w, rounds = E.irv(rows)
        if w and len(rounds) >= 3: break
    tot = sum(n for n, _ in rows)
    return ('Preference schedule:\n' + E.fmt_schedule(rows) + '\nWho wins by plurality with elimination (instant runoff)?', w,
            [f'{tot} voters; a majority is {tot // 2 + 1}.'] + [f'Round {i + 1}: ' + ', '.join(f'{a} {b}' for a, b in sorted(r.items())) + ('' if i == len(rounds) - 1 else f'; eliminate {min(r, key=r.get)}.') for i, r in enumerate(rounds)] + [f'Winner: {w}.'],
            [x for x in 'ABCD' if x != w])
G['election-theory-skill-02'] = el02


def el04(k):
    w = [[8, 6, 5, 2], [11, 7, 4, 3], [9, 8, 4, 1], [12, 6, 6, 3], [10, 9, 2, 2], [7, 7, 5, 4]][k % 6]
    T = sum(w); q0 = max(T // 2 + 1, T - w[1] + 1)
    return (f'Weights {", ".join(map(str, w))}. Smallest valid quota that gives P2 veto power?', str(q0),
            [f'Valid quotas run from {T // 2 + 1} to {T}.', f'P2 has veto power when the others fall short: {T - w[1]} < q, so q ≥ {T - w[1] + 1}.', f'Smallest valid quota: {q0}.'], near(q0))
G['election-theory-skill-04'] = el04


def el05(k):
    qq, w, who = [(13, [8, 5, 4, 3], 2), (15, [9, 6, 5, 2], 3), (11, [6, 5, 4, 2], 4), (16, [9, 8, 5, 3], 2)][k % 4]
    c = E.critical_counts(qq, w); T = sum(c); a = fs(Fr(c[who - 1], T))
    return (f'Find the Banzhaf power index of P{who} in [{qq}: {", ".join(map(str, w))}].', a,
            [f'Winning coalitions: ' + '; '.join(E.name(S2) for S2 in E.coalitions(qq, w)) + '.', 'Critical counts: ' + ', '.join(f'P{i + 1} {x}' for i, x in enumerate(c)) + f' (total {T}).', f'Index = {c[who - 1]}/{T} = {a}.'],
            [fs(Fr(c[who - 1] + 1, T)), fs(Fr(w[who - 1], sum(w))), fs(Fr(c[0], T)), fs(Fr(1, 4))])
G['election-theory-skill-05'] = el05


def el06(k):
    bids = [{'Ann': (360, 150), 'Ben': (300, 210), 'Cal': (330, 180)}, {'Ann': (420, 90), 'Ben': (390, 150), 'Cal': (450, 120)}][k % 2]
    items_ = ('house', 'car'); n = 3
    won = {p: 0 for p in bids}
    for j in range(2):
        w = max(bids, key=lambda p: bids[p][j]); won[w] += bids[w][j]
    fair = {p: Fr(sum(b), n) for p, b in bids.items()}; first = {p: fair[p] - won[p] for p in bids}; sur = -sum(first.values())
    ans = first['Ann'] + sur / n; c = lambda x: f'{float(x):.2f}'.rstrip('0').rstrip('.')
    return ('Sealed bids, three heirs: ' + '; '.join(f'{p} bids house ${b[0]}, car ${b[1]}' for p, b in bids.items()) + '. Ann\'s total cash (+ receives, − pays)?', c(ans),
            ['Each item goes to its highest bidder; each fair share is the sum of one\'s own bids ÷ 3.', 'Fair shares: ' + ', '.join(f'{p} ${c(v)}' for p, v in fair.items()) + '.',
             'First settlement (fair share − value won): ' + ', '.join(f'{p} {c(v)}' for p, v in first.items()) + f'; surplus ${c(sur)} split three ways.', f'Ann: {c(first["Ann"])} + {c(sur / n)} = {c(ans)}.'], None)
G['election-theory-skill-06'] = el06


def divisor(pops, S2, mode):
    a = [1 if mode == 'up' else 0 for _ in pops]
    pri = lambda i: Fr(pops[i], a[i] + 1) if mode == 'down' else Fr(pops[i], a[i]) if mode == 'up' else Fr(2 * pops[i], 2 * a[i] + 1)
    while sum(a) < S2:
        b = max(range(len(pops)), key=pri); a[b] += 1
    return a


def el07(k):
    pops, S2, mode, nm = [([2210, 1460, 830, 500], 25, 'down', 'Jefferson'), ([2210, 1460, 830, 500], 25, 'up', 'Adams'), ([3400, 2150, 1270, 680], 30, 'near', 'Webster')][k % 3]
    a = divisor(pops, S2, mode); h = E.fs  # noqa
    ham = [math.floor(p * S2 / sum(pops)) for p in pops]
    return (f'{nm}\'s method: populations {", ".join(map(str, pops))}; {S2} seats. Apportionment in order?', ', '.join(map(str, a)),
            [f'Standard divisor {sum(pops)}/{S2} = {sum(pops) / S2:.2f}.', f'{nm} rounds modified quotas {"down" if mode == "down" else "up" if mode == "up" else "to the nearest whole number"}; adjust the divisor until they add to {S2}.', 'Apportionment: ' + ', '.join(map(str, a)) + '.'],
            [', '.join(map(str, divisor(pops, S2, m2))) for m2 in ('down', 'up', 'near') if m2 != mode] + [', '.join(map(str, ham))])
G['election-theory-skill-07'] = el07


def hamilton(pops, S2):
    T = sum(pops); q = [Fr(p * S2, T) for p in pops]; a = [math.floor(x) for x in q]
    for i in sorted(range(len(pops)), key=lambda i: -(q[i] - a[i]))[:S2 - sum(a)]: a[i] += 1
    return a


_r8 = random.Random(8)
_al = []
while len(_al) < 4:
    pops = [_r8.randint(100, 900) for _ in range(3)]; S2 = _r8.randint(8, 20)
    a, b = hamilton(pops, S2), hamilton(pops, S2 + 1)
    lose = [i for i in range(3) if b[i] < a[i]]
    if lose: _al.append((pops, S2, lose[0], a, b))


def el08(k):
    pops, S2, i, a, b = _al[k % 4]; nm = 'ABC'
    return (f'Populations A {pops[0]}, B {pops[1]}, C {pops[2]}. Hamilton with {S2} and then {S2 + 1} seats: which state loses a seat?', nm[i],
            [f'{S2} seats: ' + ', '.join(map(str, a)) + '.', f'{S2 + 1} seats: ' + ', '.join(map(str, b)) + '.', f'State {nm[i]} goes from {a[i]} to {b[i]}: the Alabama paradox.'],
            [x for x in ['A', 'B', 'C', 'No state loses a seat'] if x != nm[i]])
G['election-theory-skill-08'] = el08


def gr01(k):
    spec = [((3, 4), (5, 2)), ((2, 5), (4, 3), (2, 1)), ((6, 3), (4, 2)), ((1, 6), (6, 1), (3, 2))][k % 4]
    tot = sum(a * b for a, b in spec)
    return ('A graph has ' + ', '.join(f'{a} vertices of degree {b}' for a, b in spec) + '. How many edges?', str(tot // 2),
            ['Handshake theorem: the degree sum is twice the number of edges.', 'Degree sum: ' + ' + '.join(f'{a}·{b}' for a, b in spec) + f' = {tot}.', f'Edges: {tot}/2 = {tot // 2}.'], near(tot // 2))
G['graphs-trees-skill-01'] = gr01


def gr04(k):
    n = [5, 6, 7, 8][k % 4]; chi = 3 if n % 2 == 0 else 4
    return (f'A wheel graph has a hub joined to every vertex of a {n}-cycle. What is its chromatic number?', str(chi),
            ['The hub is adjacent to every rim vertex, so it needs a color of its own.', f'The rim is a {n}-cycle: {"even, so 2 colors" if n % 2 == 0 else "odd, so 3 colors"}.', f'Total: {chi} colors.'], ['2', '3', '4', '5', str(n)])
G['graphs-trees-skill-04'] = gr04


def gr06(k):
    m, n = [(4, 6), (3, 5), (2, 8), (4, 5)][k % 4]; yes = m % 2 == 0 and n % 2 == 0
    ans = 'Yes: every degree is even' if yes else 'No: some vertices have odd degree'
    return (f'Does K_{m},{n} have an Euler circuit?', ans,
            [f'In K_{m},{n} each of the {m} vertices has degree {n} and each of the {n} vertices has degree {m}.', 'A connected graph has an Euler circuit exactly when every degree is even.', ans + '.'],
            ['No: some vertices have odd degree' if yes else 'Yes: every degree is even', 'Yes: it is connected', 'No: bipartite graphs never have Euler circuits'])
G['graphs-trees-skill-06'] = gr06


def lp02(k):
    a, b, c = [(2, 3, 12), (1, 2, 8), (3, 2, 12), (1, 1, 6)][k % 4]
    n = sum(1 for x in range(c + 1) for y in range(c + 1) if a * x + b * y <= c)
    return (f'How many points (x, y) with whole-number coordinates satisfy x ≥ 0, y ≥ 0, {a}x + {b}y ≤ {c}?'.replace('1x', 'x').replace('1y', 'y'), str(n),
            ['For each x from 0 up, count the whole-number y with 0 ≤ y ≤ (c − ax)/b.', ' + '.join(str((c - a * x) // b + 1) for x in range(c // a + 1)) + f' = {n}.', 'Each term counts one column of lattice points in the region.'], near(n))
G['linear-programming-skill-02'] = lp02


def lp03(k):
    cons = [[(1, 1, 10), (1, 0, 6), (0, 1, 7)], [(2, 1, 14), (1, 2, 16), (1, 0, 6)], [(1, 1, 9), (2, 1, 14), (0, 1, 7)], [(3, 1, 18), (1, 1, 8), (1, 3, 18)]][k % 4]
    allc = cons + [(-1, 0, 0), (0, -1, 0)]; pts = set()
    for (a1, b1, c1), (a2, b2, c2) in itertools.combinations(allc, 2):
        d = a1 * b2 - a2 * b1
        if d == 0: continue
        x, y = Fr(c1 * b2 - c2 * b1, d), Fr(a1 * c2 - a2 * c1, d)
        if x >= 0 and y >= 0 and all(a * x + b * y <= c for a, b, c in cons): pts.add((x, y))
    t = lambda a, b, c: (f'{a}x' if a > 1 else 'x' if a else '') + (' + ' if a and b else '') + (f'{b}y' if b > 1 else 'y' if b else '') + f' ≤ {c}'
    return ('How many corner points does the region ' + ', '.join(t(*c) for c in cons) + ', x ≥ 0, y ≥ 0 have?', str(len(pts)),
            ['Corners are intersections of two boundary lines that satisfy every constraint.', 'Corners: ' + ', '.join(f'({fs(x)}, {fs(y)})' for x, y in sorted(pts)) + '.', f'Count: {len(pts)}.'], near(len(pts)))
G['linear-programming-skill-03'] = lp03


def lp04(k):
    a, b, p, q, r = [(3, 2, 2, 5, 4), (5, 4, 4, 1, 0), (2, 7, 7, 1, 0), (4, 3, 3, 4, 6)][k % 4]
    y = Fr(a * p + b * q - a * r, b)
    return (f'P = {a}x + {b}y. The points ({p}, {q}) and ({r}, y) lie on the same level line. Find y.', fs(y),
            [f'At ({p}, {q}): P = {a}·{p} + {b}·{q} = {a * p + b * q}.', f'Same level line: {a}·{r} + {b}y = {a * p + b * q}, so {b}y = {a * p + b * q - a * r}.', f'y = {fs(y)}.'], near(fs(y)))
G['linear-programming-skill-04'] = lp04


def isp(n): return n > 1 and all(n % d for d in range(2, int(n ** .5) + 1))


def np01(k):
    f, fn = [('n² + n + 11', lambda n: n * n + n + 11), ('2n² + 29', lambda n: 2 * n * n + 29), ('n² − n + 17', lambda n: n * n - n + 17), ('n² + 21n + 1', lambda n: n * n + 21 * n + 1)][k % 4]
    n = 0
    while isp(fn(n)): n += 1
    v = fn(n); fac = [p for p in range(2, v) if v % p == 0][0]
    return (f'Smallest n ≥ 0 that is a counterexample to "{f} is always prime"?', str(n),
            [f'Check n = 0, 1, 2, …: each value before n = {n} is prime.', f'n = {n}: {f} = {v} = {fac}·{v // fac}.', 'One counterexample disproves the universal claim.'], near(n))
G['number-theory-proof-skill-01'] = np01


def np04(k):
    a, rep, txt = [(Fr(1, 10), 63, '0.1636363…'), (Fr(2, 10), 45, '0.2454545…'), (Fr(0), 285714, '0.285714285714…'), (Fr(3, 10), 18, '0.3181818…')][k % 4]
    if k % 4 == 2: v = Fr(2, 7)
    else: v = a + Fr(rep, 99 * 10)
    return (f'Write {txt} as a fraction in lowest terms.', fs(v),
            ['Let x be the decimal; multiply by a power of 10 so the repeating block lines up, then subtract.', f'The difference removes the repeating part and leaves a whole number over a multiple of 9.', f'Simplify: x = {fs(v)}.'], near(fs(v)))
G['number-theory-proof-skill-04'] = np04


def np05(k):
    N, a, b = [(1500, 15, 6), (800, 9, 12), (2000, 18, 24), (999, 21, 14), (1200, 16, 10)][k % 5]
    l = math.lcm(a, b); n = N // a - N // l
    return (f'How many integers from 1 to {N} are divisible by {a} but not by {b}?', str(n),
            [f'Multiples of {a}: ⌊{N}/{a}⌋ = {N // a}.', f'Divisible by both means divisible by lcm({a}, {b}) = {l}: ⌊{N}/{l}⌋ = {N // l}.', f'{N // a} − {N // l} = {n}.'], near(n))
G['number-theory-proof-skill-05'] = np05


def rl01(k):
    R = [[(1, 2), (2, 3), (3, 1), (2, 1)], [(1, 1), (1, 3), (3, 1), (2, 3), (3, 2)], [(1, 2), (2, 1), (2, 3), (4, 1)], [(1, 3), (3, 4), (4, 1), (1, 4)]][k % 4]
    inv = {(b, a) for a, b in R}; both = sorted(set(R) & inv)
    return ('R = {' + ', '.join(f'({a}, {b})' for a, b in R) + '}. How many pairs are in R ∩ R⁻¹?', str(len(both)),
            ['R⁻¹ reverses every pair of R.', 'A pair is in both when it and its reverse are in R: ' + (', '.join(f'({a}, {b})' for a, b in both) or 'none') + '.', f'Count: {len(both)}.'], near(len(both)))
G['properties-relations-skill-01'] = rl01


def rl02(k):
    n, d = [(10, 3), (12, 2), (9, 4), (15, 5)][k % 4]
    arcs = [(a, b) for a in range(1, n + 1) for b in range(1, n + 1) if a != b and b % a == 0 and b // a <= d]
    rule = 'b = 2a' if d == 2 else f'b = ka for some whole k with 2 ≤ k ≤ {d}'
    return (f'R on {{1, …, {n}}}: a R b iff {rule}. How many arrows?', str(len(arcs)),
            [f'From each a there is an arrow to 2a, 3a, …, {d}a that is at most {n}.', 'Count per vertex: ' + ' + '.join(str(min(d, n // a) - 1 if n // a >= 2 else 0) for a in range(1, n + 1)) + '.', f'Total: {len(arcs)} arrows.'], near(len(arcs)))
G['properties-relations-skill-02'] = rl02


def rl03(k):
    R = [[(1, 2), (2, 3), (3, 4), (4, 5)], [(1, 3), (3, 2), (2, 1)], [(1, 2), (3, 1), (4, 3)], [(2, 4), (4, 1), (1, 3), (5, 2)]][k % 4]
    C = set(R)
    while True:
        add = {(a, d) for a, b in C for c, d in C if b == c} - C
        if not add: break
        C |= add
    n = len(C) - len(R)
    return ('R = {' + ', '.join(f'({a}, {b})' for a, b in R) + '}. Fewest pairs to add to make R transitive?', str(n),
            ['Repeatedly add (a, c) whenever (a, b) and (b, c) are in R; new pairs can create new chains.', 'Added: ' + ', '.join(f'({a}, {b})' for a, b in sorted(C - set(R))) + '.', f'{n} pairs.'], near(n))
G['properties-relations-skill-03'] = rl03


def rl04(k):
    rule, fn, a, b = [('a R b iff 9 | (a² − b²)', lambda a, b: (a * a - b * b) % 9 == 0, 14, -5), ('a R b iff a·b > 0', lambda a, b: a * b > 0, -7, -12), ('a R b iff a − b is a multiple of 6', lambda a, b: (a - b) % 6 == 0, 41, -13), ('a R b iff a² ≤ b + 4', lambda a, b: a * a <= b + 4, -3, 4)][k % 4]
    y = fn(a, b); f = lambda x: str(x).replace('-', '−')
    return (f'R on ℤ: {rule}. Is ({f(a)}, {f(b)}) ∈ R? Answer Yes or No.', 'Yes' if y else 'No',
            [f'Substitute a = {f(a)}, b = {f(b)} into the rule.', f'The condition is {"true" if y else "false"} for this pair.', f'So ({f(a)}, {f(b)}) {"is" if y else "is not"} in R.'], None)
G['properties-relations-skill-04'] = rl04


def rl05(k):
    blocks = [[3, 2, 2], [4, 1, 3], [2, 2, 2, 1], [5, 3]][k % 4]; n = sum(b * b for b in blocks)
    return ('A partition of a set has blocks of sizes ' + ', '.join(map(str, blocks)) + '. How many ordered pairs are in the relation it induces?', str(n),
            ['The induced relation pairs every element with every element of its own block, itself included.', 'A block of size m gives m² pairs: ' + ' + '.join(f'{b}²' for b in blocks) + '.', f'Total: {n}.'], near(n))
G['properties-relations-skill-05'] = rl05


def stir(n, k): return 1 if n == k else 0 if k == 0 or k > n else k * stir(n - 1, k) + stir(n - 1, k - 1)


def rl06(k):
    n, c = [(6, 2), (5, 4), (6, 3), (4, 2)][k % 4]
    return (f'How many equivalence relations on a {n}-element set have exactly {c} classes?', str(stir(n, c)),
            ['Equivalence relations correspond to partitions; count partitions into nonempty blocks.', f'S({n}, {c}) = {c}·S({n - 1}, {c}) + S({n - 1}, {c - 1}) = {c}·{stir(n - 1, c)} + {stir(n - 1, c - 1)}.', f'= {stir(n, c)}.'], near(stir(n, c)))
G['properties-relations-skill-06'] = rl06


def rl07(k):
    N, m, a = [(100, 7, 3), (250, 9, 5), (500, 12, 7), (365, 7, 1)][k % 4]
    cnt = sum(1 for x in range(1, N + 1) if (x - a) % m == 0)
    return (f'Congruence mod {m} on {{1, …, {N}}}. How many elements are in [{a}]?', str(cnt),
            [f'[{a}] = {{{a}, {a + m}, {a + 2 * m}, …}} up to {N}.', f'Count: ⌊({N} − {a})/{m}⌋ + 1 = {(N - a) // m} + 1.', f'= {cnt}.'], near(cnt))
G['properties-relations-skill-07'] = rl07


def sq02(k):
    i, ai, j, aj, n = [(3, 12, 7, 28, 20), (2, 5, 9, 33, 15), (4, -2, 10, 22, 30), (5, 40, 12, 5, 25)][k % 4]
    d = Fr(aj - ai, j - i); a1 = ai - (i - 1) * d; an = a1 + (n - 1) * d
    return (f'An arithmetic sequence has a_{i} = {ai} and a_{j} = {aj}. Find a_{n}.'.replace('-', '−'), fs(an).replace('-', '−') if False else fs(an),
            [f'd = (a_{j} − a_{i})/({j} − {i}) = ({aj} − {ai})/{j - i} = {fs(d)}.', f'a₁ = a_{i} − {i - 1}d = {fs(a1)}.', f'a_{n} = a₁ + {n - 1}d = {fs(an)}.'], near(fs(an)) if an >= 0 else [fs(an + d), fs(an - d), fs(an + 1), fs(-an)])
G['sequences-induction-recursion-skill-02'] = sq02


def sq04(k):
    m = [8, 10, 7, 9][k % 4]; F = [1, 1]
    while len(F) < 2 * m + 2: F.append(F[-1] + F[-2])
    s = sum(F[2 * i] for i in range(m))  # F1 + F3 + … + F_(2m−1)
    return (f'Find F₁ + F₃ + F₅ + … + F_{2 * m - 1} (F₁ = F₂ = 1).', str(s),
            ['Each odd-index term can be rewritten as F_(2i+1) = F_(2i+2) − F_(2i), so the sum telescopes.', f'F₁ + F₃ + … + F_{2 * m - 1} = F_{2 * m}.', f'F_{2 * m} = {F[2 * m - 1]}.'], near(s))
G['sequences-induction-recursion-skill-04'] = sq04


def st01(k):
    r1, r2, strict = [(-3, 2, True), (0, 4, False), (-1, 5, True), (-4, 1, False)][k % 4]
    els = [x for x in range(r1 - 2, r2 + 3) if ((x - r1) * (x - r2) < 0 if strict else (x - r1) * (x - r2) <= 0)]
    b, c = -(r1 + r2), r1 * r2; co = lambda v: '' if v == 1 else str(v)
    poly = 'n²' + (f' − {co(-b)}n' if b < 0 else f' + {co(b)}n' if b > 0 else '') + (f' + {c}' if c > 0 else f' − {-c}' if c < 0 else '')
    ans = S(els)
    wrong = [S([x for x in range(r1, r2 + 1)]) if strict else S(els[1:-1]), S(els[:-1]), S([r1, r2])]
    return (f'Which set equals {{n ∈ ℤ | {poly} {"<" if strict else "≤"} 0}}?', ans,
            [f'{poly} = (n − ({r1}))(n − ({r2})).', f'The product is {"negative" if strict else "at most 0"} between {r1} and {r2}{"" if strict else ", endpoints included"}.', f'Integers there: {ans}.'], wrong)
G['set-theory-skill-01'] = st01


def st03(k):
    U = list(range(1, 13)); A = [2, 4, 6, 8, 10, 12]; Bm = [3, 6, 9, 12]; C = [1, 2, 3, 5, 7, 11]
    ex = ["(A ∩ B)′ − C", "(A ∪ C)′", "A′ ∩ (B ∪ C)", "(A − B)′ ∩ C"][k % 4]
    env = {'A': set(A), 'B': set(Bm), 'C': set(C)}; Us = set(U)
    py = ex
    val = {"(A ∩ B)′ − C": (Us - (env['A'] & env['B'])) - env['C'], "(A ∪ C)′": Us - (env['A'] | env['C']), "A′ ∩ (B ∪ C)": (Us - env['A']) & (env['B'] | env['C']), "(A − B)′ ∩ C": (Us - (env['A'] - env['B'])) & env['C']}[ex]
    ans = S(sorted(val))
    wrong = [S(sorted(val | {1})), S(sorted(val - {min(val)})) if val else '{1}', S(sorted(Us - val))[:60]]
    return (f'U = {{1, …, 12}}, A = evens, B = multiples of 3, C = {S(C)}. Find {ex}.', ans,
            ['Complements are taken in U; work inside parentheses first.', 'A = {2, 4, 6, 8, 10, 12}, B = {3, 6, 9, 12}.', f'{ex} = {ans}.'], wrong)
G['set-theory-skill-03'] = st03


def st05(k):
    n, inc, exc = [(7, 1, 1), (8, 2, 1), (6, 1, 2), (9, 2, 2)][k % 4]; v = 2 ** (n - inc - exc)
    return (f'How many subsets of {{1, …, {n}}} contain {", ".join(map(str, range(1, inc + 1)))} but not {", ".join(map(str, range(n - exc + 1, n + 1)))}?', str(v),
            [f'The {inc} required element(s) are always in and the {exc} forbidden one(s) always out.', f'The other {n - inc - exc} elements are free: in or out.', f'2^{n - inc - exc} = {v}.'], near(v))
G['set-theory-skill-05'] = st05


def sm04(k):
    cond, fn, lab = [('n² < 30 and n is odd', lambda n: n * n < 30 and n % 2, ''), ('n² ≤ 20 and n ≥ −2', lambda n: n * n <= 20 and n >= -2, ''), ('|n − 2| < 4 and n is even', lambda n: abs(n - 2) < 4 and n % 2 == 0, ''), ('n³ ≤ 30 and n² ≥ 4', lambda n: n ** 3 <= 30 and n * n >= 4, '')][k % 4]
    els = [x for x in range(-10, 11) if fn(x)]; ans = S(els)
    return (f'Which is {{n ∈ ℤ | {cond}}} in roster notation?', ans,
            ['Find the integers meeting the first condition, then keep those meeting the second.', 'Check boundary values carefully (squares of negatives, strict vs. non-strict inequalities).', f'Result: {ans}.'],
            [S(els[1:]), S(els + [els[-1] + 1]), S([x for x in els if x >= 0]) if any(x < 0 for x in els) else S(els[:-1])])
G['speaking-mathematically-skill-04'] = sm04


def sm05(k):
    a, n = [(2, 6), (3, 8), (1, 5), (2, 9)][k % 4]; v = 2 ** (n - a)
    return (f'How many sets X satisfy {{1, …, {a}}} ⊆ X ⊆ {{1, …, {n}}}?'.replace('{1, …, 1}', '{1}'), str(v),
            [f'X must contain 1 to {a} and may contain any of {a + 1} to {n}.', f'Each of the {n - a} optional elements is in or out.', f'2^{n - a} = {v}.'], near(v))
G['speaking-mathematically-skill-05'] = sm05


def sm06(k):
    n = [6, 8, 10, 7][k % 4]
    return (f'A = {{1, …, {n}}}. How many pairs (x, y) in A × A have x < y?', str(math.comb(n, 2)),
            [f'A × A has {n}² = {n * n} pairs; {n} have x = y.', f'The remaining {n * n - n} split evenly between x < y and x > y.', f'{n * n - n}/2 = {math.comb(n, 2)}.'], [str(n * n), str(n * n - n), str(math.comb(n, 2) + n)])
G['speaking-mathematically-skill-06'] = sm06


def sm07(k):
    n = [7, 8, 9, 10][k % 4]; a, b = 2, 3
    for _ in range(n - 2): a, b = b, a + b
    return (f'How many bit strings of length {n} have no two consecutive 1s?', str(b),
            ['Let s_n count them: a valid string ends in 0 (any valid string of length n − 1) or in 01 (any of length n − 2).', 's_n = s_(n−1) + s_(n−2), with s_1 = 2 and s_2 = 3.', f's_{n} = {b}.'], near(b))
G['speaking-mathematically-skill-07'] = sm07


# ---------------- which clones remain, and the new items they need ----------------
def tmpl(s):
    s = re.sub(r'\{[^}]*\}', '{S}', s); s = re.sub(r'\[[^\]]*\]', '[W]', s)
    s = re.sub(r'\b(Kim|Lee|Ann|Ben|Ana|Bo|Cy|Sam|Jordan|Riley|Casey|Avery|Morgan|Taylor|Jamie|Quinn|Alex)\b', 'Nm', s)
    s = re.sub(r'[A-Z](?: > [A-Z])+', 'R', s)
    return re.sub(r'\d+(\.\d+)?', '#', s)


FIXED = {m.group(1) for _, q in items(B) for m in [re.match(r'Partner-check companion to (\S+) ', q.get('sourceNotes', ''))] if m}
FIXED |= {e['id'] for e in json.load(open(os.path.join(ROOT, 'tests/fixtures/content-20261115.json'))) if e.get('course') == 'discrete'}
cp2 = collections.defaultdict(set)
for u, q in items(B):
    if q['level'] == 'cp2': cp2[q['skillId']].add(tmpl(q['prompt']))
clones = [(u, q) for u, q in items(B) if q['level'] == 'honors' and tmpl(q['prompt']) in cp2[q['skillId']] and q['id'] not in FIXED]
need = collections.Counter((q['skillId'], q['format']) for _, q in clones)

made = 0; done = collections.Counter()
for (sk, fmt), n in sorted(need.items()):
    unit = sk.rsplit('-skill-', 1)[0]; gen = G[sk]
    std = next(q['standards'] for _, q in items(B) if q['skillId'] == sk)
    k = 0
    while done[(sk, fmt)] < n:
        prompt, ans, steps, wrong = gen(k)
        k += 1
        assert k < 60, (sk, fmt)
        if prompt in prompts[unit]: continue
        if fmt == 'multiple-choice' and not wrong: fmt_use = 'short-answer'
        else: fmt_use = fmt
        s = int(sk.rsplit('-', 1)[1]); j = 1
        while f'dm-{CODE[unit]}-s{s:02d}-honors-d{j:02d}' in ids: j += 1
        q = {'id': f'dm-{CODE[unit]}-s{s:02d}-honors-d{j:02d}', 'skillId': sk, 'level': 'honors', 'format': fmt_use, 'prompt': prompt, 'answer': ans,
             'solutionSteps': steps, 'sourceNotes': NOTE.format(gen.__name__ + '_adv'), 'standards': list(std)}
        if fmt_use == 'multiple-choice':
            opts = [ans] + [w for w in dict.fromkeys(wrong) if w != ans]
            if len(opts) < 4 and re.fullmatch(r'\d+(, \d+)+', ans):   # apportionment lists: one seat moved
                v = [int(x) for x in ans.split(', ')]
                for i, j in itertools.permutations(range(len(v)), 2):
                    w = v[:]; w[i] += 1; w[j] -= 1; t2 = ', '.join(map(str, w))
                    if w[j] >= 0 and t2 not in opts: opts.append(t2)
                    if len(opts) >= 4: break
            if len(opts) < 4: continue
            opts = opts[:4]; t = int(hashlib.sha256(q['id'].encode()).hexdigest()[:6], 16) % 4
            others = opts[1:]; order = others[:t] + [ans] + others[t:]
            q['options'] = [{'text': o, 'correct': o == ans} for o in order]
        ids.add(q['id']); prompts[unit].add(prompt); B[unit]['questions'].append(q)
        done[(sk, fmt)] += 1; made += 1

moved = 0
for u, q in clones:
    q['level'] = 'cp1'
    q['sourceNotes'] += ' Moved from Advanced to Standard by the Discrete Math audit 2026-11-18 follow-up (same template as a Support item).'
    moved += 1
# Keep the quick-check cap (#2): at most 4 per skill and level after the moves.
capped = 0
for u, d in B.items():
    seen = collections.Counter(); keep = []
    for q in d['questions']:
        if family(q) == 'quick_check' and q['id'] not in FIXED:
            key = (q['skillId'], q['level']); seen[key] += 1
            if seen[key] > 4: capped += 1; continue
        keep.append(q)
    d['questions'] = keep
save(B)
print('new Advanced items', made, '| clones moved to Standard', moved, '| extra quick checks removed', capped)
