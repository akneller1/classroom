"""Recomputes the numeric and set answers printed in the Discrete Math Explore & Reflect keys (worksheets_content.py)
and checks that each expected value appears in the key text. Usage (repository root):
    python3 tools/interactive-math-discrete/tests/worksheet-answers.py"""
import itertools, math, os, sys
from fractions import Fraction as Fr
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.dirname(HERE))
from worksheets_content import W
fails = 0; n = 0
def flat(w):
    out = []
    for k in ('predict', 'explore'): out += [a for _, a, _ in w[k]]
    for t in w['record']: out += [c for r in t['rows'] for c in r]
    out += [x for _, xs in w['rules'] for x in xs] + [w['explain'][1]] + [a for _, a in w['apply']] + [w['teacher']['varies']]
    return ' '.join(out)
def has(slug, *subs):
    global fails, n
    txt = flat(W[slug])
    for s in subs:
        n += 1
        if s not in txt: fails += 1; print('FAIL', slug, 'missing', repr(s))
def check(cond, msg):
    global fails, n
    n += 1
    if not cond: fails += 1; print('FAIL', msg)

# truth tables
def rows(k): return list(itertools.product([True, False], repeat=k))
imp = lambda a, b: (not a) or b
check(sum(imp(p, q) or imp(q, p) for p, q in rows(2)) == 4, 'tautology (p→q)∨(q→p)')
check(sum(imp(p and q, r) for p, q, r in rows(3)) == 7, '(p∧q)→r has 7 true rows')
check(sum(p == q for p, q in rows(2)) == 2, 'p↔q 2 true rows')
crit = lambda prem: [r for r in rows(3) if all(f(*r) for f in prem)]
check(len(crit([lambda p, q, r: imp(p, q), lambda p, q, r: p])) == 2, 'modus ponens: 1 critical row in p, q (2 with r free)')
check(len([r for r in rows(2) if imp(*r) and r[1]]) == 2 and len([r for r in rows(2) if imp(*r) and not r[0]]) == 2, 'converse/inverse errors: 2 critical rows')
c4 = [r for r in rows(3) if imp(r[0], r[1]) and imp(r[1], r[2])]; check(len(c4) == 4 and all(imp(r[0], r[2]) for r in c4), 'transitivity: 4 critical rows, valid')
check(all(imp(imp(p, q) and imp(q, r), imp(p, r)) for p, q, r in rows(3)), 'hypothetical syllogism tautology')
has('discrete-truth-table-lab', '8 rows for 3 variables', '16 rows for 4', 'p ∧ ~q')

# Euclid
def ext(a, b):
    T = [[a, None, 1, 0], [b, None, 0, 1]]
    while T[-1][0] > 0:
        p, c = T[-2], T[-1]; q = p[0] // c[0]; c[1] = q; T.append([p[0] - q * c[0], None, p[2] - q * c[2], p[3] - q * c[3]])
    return T[-2]
def steps(a, b):
    a, b = max(a, b), min(a, b); k = 0
    while b: a, b = b, a % b; k += 1
    return k
for a, b in [(84, 36), (91, 120), (72, 60), (89, 55)]:
    g, s, t = ext(a, b)[0], ext(a, b)[2], ext(a, b)[3]
    check(s * a + t * b == g, f'bezout {a},{b}')
    has('discrete-euclid-explorer', '?' + str(steps(a, b)) if False else str(steps(a, b)), str(a * b // g), f'{g} = ' + (f'({s})'.replace('-', '−') if s < 0 else str(s)) + f'·{a} + ' + (f'({t})'.replace('-', '−') if t < 0 else str(t)) + f'·{b}')
check(math.gcd(1071, 462) == 21 and 1071 * 462 // 21 == 23562 and 3 * 21 - 2 * 30 == 3 and -40 == 6 * -7 + 2 and steps(89, 55) == 9 and steps(55, 34) == 8, 'euclid apply')
has('discrete-euclid-explorer', '23562', 'gcd = 21', 'q = −4, r = 5')

# recursion
def seq(c, d, a1, n=15): a = [a1]; [a.append(c * a[-1] + d) for _ in range(n - 1)]; return a
check(seq(2, 1, 1)[4] == 31 and seq(2, 1, 1)[9] == 1023 and seq(2, 1, 4)[:4] == [4, 9, 19, 39], 'hanoi')
check(seq(1, 3, 5)[9] == 32 and seq(0.5, 3, 2)[:5] == [2, 4, 5, 5.5, 5.75] and all(abs(x - (6 - 4 * 0.5 ** i)) < 1e-12 for i, x in enumerate(seq(0.5, 3, 2))), 'arith / fixed point')
f = [1, 1]; [f.append(f[-1] + f[-2]) for _ in range(10)]; check(f[11] == 144 and sum(f[:10]) == 143, 'fibonacci')
check(seq(1, -6, 50, 20)[19] == -64 and abs(seq(1.05, 100, 1000)[2] - 1307.5) < 1e-9 and 5 * 3 ** 5 == 1215, 'recursion apply')
b = [1]; [b.append(b[-1] + 2 * (k - 1)) for k in range(2, 10)]; check(all(b[k - 1] == k * k - k + 1 for k in range(1, 10)), 'n^2 - n + 1')
has('discrete-recursion-explorer', '1023', '144', '143', '−64', '1307.50', '1215', '7, 11, 15, 19, 23', '2, 6, 18, 54, 162', '2, 4, 5, 5.5, 5.75')

# sets
U = set(range(1, 21)); A = {x for x in U if x % 2 == 0}; B = {x for x in U if x % 3 == 0}; C = {2, 3, 5, 7, 11, 13, 17, 19}
ros = lambda S: '{' + ', '.join(map(str, sorted(S))) + '}'
has('discrete-venn-explorer', ros(A & B), ros(U - (A | B)), ros(A - B), ros(A ^ B), ros({x for x in U if (x in A) + (x in B) + (x in C) == 1}))
check((A - (B - C)) != ((A - B) - C) and 2 in (A - (B - C)) - ((A - B) - C), 'A−(B−C) counterexample 2')
P, Q, U10 = {2, 3, 5, 7}, {1, 3, 5, 7, 9}, set(range(1, 11)); check(P - Q == {2} and U10 - (P | Q) == {4, 6, 8, 10}, 'venn apply 1')
has('discrete-venn-explorer', 'n(A ∪ B) = 55', 'n(A ⊕ B) = 45')

# relations
def props(R, S):
    return (all((a, a) in R for a in S), all((b, a) in R for a, b in R), all(a == b or (b, a) not in R for a, b in R), all((a, d) in R for a, b in R for c, d in R if b == c))
S4 = range(1, 5)
for rel, want in [(lambda a, b: a == b, (1, 1, 1, 1)), (lambda a, b: a < b, (0, 0, 1, 1)), (lambda a, b: b % a == 0, (1, 0, 1, 1)), (lambda a, b: (a - b) % 2 == 0, (1, 1, 0, 1))]:
    check(props({(a, b) for a in S4 for b in S4 if rel(a, b)}, S4) == tuple(map(bool, want)), 'relation props ' + str(want))
check(props({(1, 2), (2, 1)}, S4) == (False, True, False, False), '{(1,2),(2,1)}')
R = {(1, 2), (2, 3), (3, 4)}
while True:
    R2 = R | {(a, d) for a, b in R for c, d in R if b == c}
    if R2 == R: break
    R = R2
check(R - {(1, 2), (2, 3), (3, 4)} == {(1, 3), (2, 4), (1, 4)}, 'transitive closure adds 3')
check(3 ** 2 + 2 ** 2 == 13, 'partition pairs')

# counting
Cn = math.comb; Pn = math.perm
check([5 ** 3, Pn(5, 3), Cn(5, 3), Cn(7, 3)] == [125, 60, 10, 35] and Cn(6, 3) == 20 and Pn(10, 4) == 5040 and Cn(12, 3) == 220 and Pn(8, 3) == 336, 'counts')
check(Fr(sum(1 for o in itertools.product(range(6), repeat=2) if 0 in o), 36) == Fr(11, 36) and Fr(Cn(5, 2), 32) == Fr(5, 16) and Fr(4, 10) == Fr(2, 5), 'counting probabilities')
check([p for p in itertools.product(range(2, 8), range(1, 8)) if p[1] <= p[0] and Pn(*p) == 60] == [(5, 3)], 'only P(5,3) = 60 in range')
has('discrete-counting-explorer', '125', '60', '10', '35', '11/36', '5/16', '5040', '220', '336')

# voting
sched = [(14, 'ABC'), (10, 'CBA'), (8, 'BCA'), (3, 'CAB')]
borda = {c: sum(v * (3 - r.index(c)) for v, r in sched) for c in 'ABC'}; h = lambda x, y: sum(v for v, r in sched if r.index(x) < r.index(y))
check(borda == {'A': 66, 'B': 75, 'C': 69} and h('B', 'A') == 18 and h('B', 'C') == 22, 'schedule')
def banz(q, w):
    c = [0] * len(w)
    for m in range(1, 1 << len(w)):
        s = sum(x for i, x in enumerate(w) if m >> i & 1)
        if s >= q:
            for i, x in enumerate(w):
                if m >> i & 1 and s - x < q: c[i] += 1
    return c
for q, w, want in [(6, [4, 3, 2], [3, 1, 1]), (4, [3, 2, 2], [2, 2, 2]), (6, [4, 2, 1], [2, 2, 0]), (5, [5, 2, 1], [4, 0, 0]), (10, [6, 5, 4], [3, 1, 1])]:
    check(banz(q, w) == want, f'banzhaf {q} {w}')
def ham(p, n):
    T = sum(p); q = [x * n / T for x in p]; a = [math.floor(x) for x in q]
    for i in sorted(range(len(p)), key=lambda i: -(q[i] - a[i]))[:n - sum(a)]: a[i] += 1
    return a
check(ham([450, 330, 220], 10) == [5, 3, 2] and ham([130, 690, 410], 13) == [2, 7, 4] and ham([130, 690, 410], 14) == [1, 8, 5], 'hamilton / alabama')
jef = lambda p, d: [math.floor(x / d) for x in p]; ada = lambda p, d: [math.ceil(x / d) for x in p]
check(jef([450, 330, 220], 90) == [5, 3, 2] and sum(jef([450, 330, 220], 82.5)) == 11 and sum(jef([450, 330, 220], 90.01)) == 9, 'jefferson interval (82.5, 90]')
check(ada([450, 330, 220], 110) == [5, 3, 2] and sum(ada([450, 330, 220], 109.99)) > 10 and sum(ada([450, 330, 220], 112.5)) == 9, 'adams interval [110, 112.5)')
p4 = [5100, 1600, 1500, 1200]; check(jef(p4, 425) == [12, 3, 3, 2] and sum(jef(p4, 400)) > 20 and sum(jef(p4, 425.01)) == 19 and abs(5100 / 470 - 10.85) < 0.01, 'jefferson quota violation, interval (400, 425]')
check((300 + 120) / 2 == 210 and 300 - 210 - 30 == 60, 'sealed bids')
has('discrete-voting-explorer', 'A 66, B 75, C 69', '18–17', '22–13', '2, 7, 4', '1, 8, 5', '82.5 < d ≤ 90', '110 ≤ d < 112.5', '400 < d ≤ 425', '12, 3, 3, 2', '3/5, 1/5, 1/5')
print(f'{n - fails}/{n} worksheet answer checks passed'); sys.exit(1 if fails else 0)
