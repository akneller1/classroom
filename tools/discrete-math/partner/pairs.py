"""Matched A/B problem pairs for the Discrete Math partner checks.

Each family has two generators: gen_a(rng, level) and gen_b(rng, level). Each returns (problem text, answer), where the answer is
computed by that side's own solver from its own parameters. Pairs are formed only when the two independently computed answers are
identical strings and the problem texts differ; verify() recomputes every stored pair from its parameters before any PDF is built.
Answer conventions are printed on every sheet."""
import itertools, math, random
from fractions import Fraction as Fr
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'bank'))
import logic as LG

C = math.comb
LV = {'cp2': 0, 'cp1': 1, 'honors': 2}


def fs(s):
    s = sorted(s)
    return '{' + ', '.join(map(str, s)) + '}' if s else '∅'


def fr(x):
    x = Fr(x)
    return str(x.numerator) if x.denominator == 1 else '%d/%d' % (x.numerator, x.denominator)


def isprime(n):
    return n > 1 and all(n % d for d in range(2, int(n ** .5) + 1))


# ======================================================================= Unit 1
def u1_prod_a(r, L):
    m, n = r.randint(2, 4 + 2 * LV[L]), r.randint(2, 5 + 2 * LV[L])
    return ('A has %d elements and B has %d elements. How many ordered pairs are in A × B?' % (m, n), str(m * n), (m, n))


def u1_prod_b(r, L):
    m, n = r.randint(2, 6 + 2 * LV[L]), r.randint(2, 6)
    return ('A code is one letter from a set of %d letters followed by one digit from a set of %d digits. How many codes are possible?' % (m, n), str(m * n), (m, n))


def u1_sub_a(r, L):
    n = r.randint(2, 4 + 2 * LV[L])
    return ('How many subsets does a set with %d elements have (include ∅)?' % n, str(2 ** n), n)


def u1_sub_b(r, L):
    n = r.randint(2, 4 + 2 * LV[L])
    return ('How many bit strings of length %d are there?' % n, str(2 ** n), n)


PRED = [('n² < 10', lambda n: n * n < 10), ('|n| ≤ 3', lambda n: abs(n) <= 3), ('n² − n = 0', lambda n: n * n == n), ('n³ = n', lambda n: n ** 3 == n), ('2n + 1 > 4', lambda n: 2 * n + 1 > 4),
        ('n ≥ 2', lambda n: n >= 2), ('n is even', lambda n: n % 2 == 0), ('n² is even', lambda n: n * n % 2 == 0), ('n(n − 1) = 0', lambda n: n * (n - 1) == 0), ('n² = 1 or n = 0', lambda n: n * n == 1 or n == 0),
        ('n² > 3', lambda n: n * n > 3), ('|n| ≥ 2', lambda n: abs(n) >= 2), ('n + 2 > 3', lambda n: n + 2 > 3), ('n > 0', lambda n: n > 0)]
DOM1 = list(range(-3, 4))


def u1_truth_a(r, L):
    d, f = r.choice(PRED)
    return ('Domain D = {−3, −2, ..., 3}. Find the truth set of "%s".' % d, fs(n for n in DOM1 if f(n)), d)


u1_truth_b = u1_truth_a


def u1_pair_a(r, L):
    x, y = r.randint(1, 6), r.randint(1, 6)
    a = r.randint(2, 3)
    return ('Solve (%dx − %d, y + %d) = (%d, %d). Give (x, y).' % (a, a, 2, a * x - a, y + 2), '(%d, %d)' % (x, y), (x, y))


def u1_pair_b(r, L):
    x, y = r.randint(1, 6), r.randint(1, 6)
    return ('Solve (x + y, x − y) = (%d, %d). Give (x, y).' % (x + y, x - y), '(%d, %d)' % (x, y), (x, y))


def u1_card_a(r, L):
    a, c = sorted(r.sample(range(-5, 9), 2))
    return ('How many elements are in {n ∈ ℤ | %d ≤ n ≤ %d}?' % (a, c), str(c - a + 1), (a, c))


def u1_card_b(r, L):
    k = r.randint(2, 10)
    s = 3 * k
    return ('How many positive multiples of 3 are at most %d?' % s, str(k), k)


# ======================================================================= Unit 2
FORMS = ['p ∧ q', '¬(¬p ∨ ¬q)', 'p ∨ q', '¬(¬p ∧ ¬q)', '¬p → q', 'p → q', '¬p ∨ q', '¬q → ¬p', '¬(p ∧ ¬q)', 'p ↔ q', '(p → q) ∧ (q → p)', '¬(p ⊕ q)',
         'p ⊕ q', '(p ∨ q) ∧ ¬(p ∧ q)', '¬(p ↔ q)', 'p ∧ ¬q', '¬(p → q)', '¬(¬p ∨ q)', '¬p ∧ ¬q', '¬(p ∨ q)', 'q → p', 'p ∨ ¬q', '¬p → ¬q', 'p', 'p ∨ (p ∧ q)', 'p ∧ (p ∨ q)']
FORMS3 = ['p ∧ (q ∨ r)', '(p ∧ q) ∨ (p ∧ r)', 'p ∨ (q ∧ r)', '(p ∨ q) ∧ (p ∨ r)', '(p ∧ q) → r', 'p → (q → r)', '¬(p ∨ q) ∨ r', '(p ∨ q) → r', '(p → r) ∧ (q → r)', '¬r → ¬(p ∨ q)']


def u2_col_a(r, L):
    f = r.choice(FORMS3 if L == 'honors' else [x for x in FORMS if L == 'cp1' or not any(c in x for c in '⊕↔')])
    vs = ['p', 'q', 'r'] if L == 'honors' else ['p', 'q']
    return ('Give the truth column of %s (standard row order, T/F string).' % f, LG.colstr(f, vs), f)


u2_col_b = u2_col_a


def u2_count_a(r, L):
    f = r.choice(FORMS3 + FORMS)
    vs = LG.variables(f) if len(LG.variables(f)) == 3 else ['p', 'q']
    return ('In how many rows of its truth table (variables %s) is %s true?' % (', '.join(vs), f), str(sum(LG.column(f, vs))), f)


u2_count_b = u2_count_a


def u2_rows_a(r, L):
    n = r.randint(2, 5)
    return ('How many rows does a truth table with %d variables have?' % n, str(2 ** n), n)


def u2_rows_b(r, L):
    n = r.randint(2, 5)
    f = ' ∧ '.join('pqrst'[:n]) if n > 1 else 'p'
    return ('How many rows does the truth table for %s have?' % f, str(2 ** n), f)


ARGS = [(['p → q', 'q'], 'p'), (['p → q', '¬p'], '¬q'), (['p ∨ q', 'p'], '¬q'), (['p → q', 'q → r'], 'r → p'), (['p ∨ q', 'q'], 'p'), (['p → r', 'q → r', 'r'], 'p'),
        (['p → q', 'r'], 'q'), (['¬p ∨ q', 'q'], 'p'), (['q → p', 'p'], 'q'), (['p ∧ q → r', 'r'], 'p'), (['p ↔ q', 'r'], 'p'), (['p → q', 'q → r', '¬p'], '¬r'), (['¬q → ¬p', '¬p'], '¬q'), (['p ∨ r', 'q'], 'p ∧ q')]


def cx_rows(prem, conc):
    vs = sorted(set().union(*[set(LG.variables(x)) for x in prem + [conc]]))
    out = []
    for r in LG.rows(vs):
        if all(LG.ev(LG.parse(p), r) for p in prem) and not LG.ev(LG.parse(conc), r):
            out.append('(' + ', '.join('%s = %s' % (v, 'T' if r[v] else 'F') for v in vs) + ')')
    return out


def u2_cx_a(r, L):
    prem, conc = r.choice(ARGS)
    rows = cx_rows(prem, conc)
    if len(rows) != 1:
        return None
    return ('Premises: %s. Conclusion: %s. Give the only row that makes every premise true and the conclusion false.' % ('; '.join(prem), conc), rows[0], (tuple(prem), conc))


u2_cx_b = u2_cx_a


# ======================================================================= Unit 3
def u3_gcd_a(r, L):
    a, c = r.randint(2, 12) * r.randint(2, 6), r.randint(2, 12) * r.randint(2, 6)
    return ('Find gcd(%d, %d).' % (a, c), str(math.gcd(a, c)), (a, c))


u3_gcd_b = u3_gcd_a


def u3_rem_a(r, L):
    n, d = r.randint(20, 150 * (1 + LV[L])), r.randint(3, 9)
    return ('Find the remainder r when %d = %d·q + r, 0 ≤ r < %d.' % (n, d, d), str(n % d), (n, d))


def u3_rem_b(r, L):
    n, d = -r.randint(5, 60), r.randint(3, 9)
    return ('Find the remainder r when %d = %d·q + r, 0 ≤ r < %d.' % (n, d, d), str(n % d), (n, d))


def u3_div_a(r, L):
    n = r.randint(6, 60 * (1 + LV[L]))
    return ('How many positive divisors does %d have?' % n, str(sum(1 for d in range(1, n + 1) if n % d == 0)), n)


u3_div_b = u3_div_a


CONJ3 = [('n² + n + 11 is prime', lambda n: isprime(n * n + n + 11)), ('n² − n + 41 is prime', lambda n: isprime(n * n - n + 41)), ('2ⁿ + 1 is prime', lambda n: isprime(2 ** n + 1)),
         ('n² + 1 is prime', lambda n: isprime(n * n + 1)), ('3n + 2 is prime', lambda n: isprime(3 * n + 2)), ('n! + 1 is prime', lambda n: isprime(math.factorial(n) + 1)),
         ('2n + 3 is prime', lambda n: isprime(2 * n + 3)), ('n² + 4 is prime', lambda n: isprime(n * n + 4)), ('6n − 1 is prime', lambda n: isprime(6 * n - 1)), ('n² + n + 1 is prime', lambda n: isprime(n * n + n + 1))]


def u3_ce_a(r, L):
    d, f = r.choice(CONJ3)
    ce = next(n for n in range(1, 60) if not f(n))
    return ('Find the smallest positive integer n that is a counterexample to "for all n ≥ 1, %s".' % d, str(ce), d)


u3_ce_b = u3_ce_a


def u3_frac_a(r, L):
    a, b = r.randint(1, 8), r.randint(2, 9)
    q = Fr(a, b)
    if q.denominator in (1,) or any(q.denominator % p == 0 for p in (3, 7, 9, 11)):
        return None
    return ('Write %s as a fraction in lowest terms.' % ('%g' % float(q)), fr(q), q)


def u3_frac_b(r, L):
    a, b = r.randint(1, 8), r.randint(2, 9)
    q = Fr(a, b)
    return ('Simplify %d/%d to lowest terms.' % (q.numerator * 3, q.denominator * 3), fr(q), q)


# ======================================================================= Unit 4
def u4_ar_a(r, L):
    a1, d, n = r.randint(-5, 10), r.randint(2, 6), r.randint(5, 12 + 4 * LV[L])
    return ('Arithmetic sequence: a₁ = %d, d = %d. Find a_%d.' % (a1, d, n), str(a1 + (n - 1) * d), (a1, d, n))


def u4_ar_b(r, L):
    a1, d, n = r.randint(-5, 10), r.randint(2, 6), r.randint(5, 16)
    return ('a₁ = %d and a_n = a_(n−1) + %d. Find a_%d.' % (a1, d, n), str(a1 + (n - 1) * d), (a1, d, n))


def u4_binom_a(r, L):
    n = r.randint(4, 8 + 2 * LV[L])
    k = r.randint(1, n - 1)
    return ('Evaluate C(%d, %d).' % (n, k), str(C(n, k)), (n, k))


def u4_binom_b(r, L):
    n = r.randint(4, 10)
    return ('How many 2-element subsets does a %d-element set have?' % n, str(C(n, 2)), n)


def u4_sum_a(r, L):
    n = r.randint(4, 20)
    return ('Evaluate 1 + 2 + ... + %d.' % n, str(n * (n + 1) // 2), n)


def u4_sum_b(r, L):
    n = r.randint(4, 20)
    return ('Evaluate Σ_{k=1}^{%d} k.' % n, str(n * (n + 1) // 2), n)


def u4_rec_a(r, L):
    a0, m, c, n = r.randint(1, 3), 2, r.randint(-1, 2), r.randint(3, 5)
    a = a0
    for _ in range(n):
        a = m * a + c
    return ('a₀ = %d, a_n = 2a_(n−1) %s %d. Find a_%d.' % (a0, '+' if c >= 0 else '−', abs(c), n), str(a), (a0, c, n))


def u4_rec_b(r, L):
    n = r.randint(4, 12)
    return ('How many moves does the Tower of Hanoi need for %d disks (m_k = 2m_(k−1) + 1, m₁ = 1)?' % n, str(2 ** n - 1), n)


def u4_fac_a(r, L):
    n, k = r.randint(5, 10), r.randint(1, 3)
    return ('Evaluate %d!/%d!.' % (n, n - k), str(math.perm(n, k)), (n, k))


def u4_fac_b(r, L):
    n, k = r.randint(5, 10), r.randint(1, 3)
    return ('How many ways can %d different medals be given to %d of %d runners?' % (k, k, n), str(math.perm(n, k)), (n, k))


# ======================================================================= Unit 5
UN = list(range(1, 11))


def u5_op_a(r, L):
    A, B = set(r.sample(UN, 5)), set(r.sample(UN, 5))
    op = r.choice(['∪', '∩', '−'])
    R = A | B if op == '∪' else A & B if op == '∩' else A - B
    return ('A = %s, B = %s. Find A %s B.' % (fs(A), fs(B), op), fs(R), (A, B, op))


def u5_op_b(r, L):
    A, B = set(r.sample(UN, 5)), set(r.sample(UN, 4))
    R = set(UN) - (A | B) if L != 'cp2' else B - A
    e = "(A ∪ B)'" if L != 'cp2' else 'B − A'
    return ('U = {1, ..., 10}, A = %s, B = %s. Find %s.' % (fs(A), fs(B), e), fs(R), (A, B, e))


def u5_ie_a(r, L):
    a, c, both = r.randint(8, 30), r.randint(8, 30), r.randint(1, 7)
    return ('|A| = %d, |B| = %d, |A ∩ B| = %d. Find |A ∪ B|.' % (a, c, both), str(a + c - both), (a, c, both))


def u5_ie_b(r, L):
    x, y, z = r.randint(3, 20), r.randint(3, 20), r.randint(1, 8)
    return ('A Venn diagram has %d in A only, %d in B only and %d in both. How many are in A ∪ B?' % (x, y, z), str(x + y + z), (x, y, z))


def u5_pow_a(r, L):
    n = r.randint(1, 6)
    return ('How many elements does the power set of a %d-element set have?' % n, str(2 ** n), n)


def u5_pow_b(r, L):
    n = r.randint(2, 7)
    return ('How many subsets of {1, ..., %d} contain the element 1?' % n, str(2 ** (n - 1)), n)


# ======================================================================= Unit 6
def u6_lt_a(r, L):
    n = r.randint(3, 8)
    return ('How many ordered pairs are in "a < b" on {1, ..., %d}?' % n, str(C(n, 2)), n)


def u6_lt_b(r, L):
    n = r.randint(3, 8)
    return ('How many ordered pairs are in "a > b" on {1, ..., %d}?' % n, str(n * (n - 1) // 2), n)


def u6_cls_a(r, L):
    m, x = r.randint(3, 5), r.randint(0, 4)
    return ('Congruence mod %d on {0, 1, ..., 12}. Find [%d].' % (m, x), fs(y for y in range(13) if (y - x) % m == 0), (m, x))


def u6_cls_b(r, L):
    m, x = r.randint(3, 5), r.randint(0, 4)
    return ('On {0, ..., 12}, a R b ⟺ a and b have the same remainder mod %d. List all b with %d R b.' % (m, x), fs(y for y in range(13) if y % m == x % m), (m, x))


def u6_ind_a(r, L):
    sizes = [r.randint(1, 4) for _ in range(r.randint(2, 3))]
    return ('A partition of a set has blocks of sizes %s. How many ordered pairs are in the induced relation?' % ', '.join(map(str, sizes)), str(sum(s * s for s in sizes)), tuple(sizes))


u6_ind_b = u6_ind_a


def u6_refl_a(r, L):
    n = r.randint(2, 3)
    return ('How many reflexive relations are there on a %d-element set?' % n, str(2 ** (n * n - n)), n)


def u6_refl_b(r, L):
    n = r.randint(2, 3)
    return ('How many symmetric relations are there on a %d-element set?' % n, str(2 ** (n * (n + 1) // 2)), n)


# ======================================================================= Unit 7
def u7_mult_a(r, L):
    a, b_, c = r.randint(2, 6), r.randint(2, 6), r.randint(1, 4)
    return ('%d shirts, %d pants and %d hats: how many outfits (one of each)?' % (a, b_, c), str(a * b_ * c), (a, b_, c))


u7_mult_b = u7_mult_a


def u7_perm_a(r, L):
    n, k = r.randint(4, 8), r.randint(2, 3)
    return ('How many ways can %d of %d people fill %d different offices?' % (k, n, k), str(math.perm(n, k)), (n, k))


def u7_perm_b(r, L):
    n, k = r.randint(4, 8), r.randint(2, 3)
    return ('How many %d-letter strings with no repeated letter use letters from a %d-letter alphabet?' % (k, n), str(math.perm(n, k)), (n, k))


def u7_comb_a(r, L):
    n, k = r.randint(4, 10), r.randint(2, 4)
    return ('How many %d-person committees can be chosen from %d people?' % (k, n), str(C(n, k)), (n, k))


def u7_comb_b(r, L):
    n, k = r.randint(4, 10), r.randint(2, 4)
    return ('How many bit strings of length %d have exactly %d ones?' % (n, k), str(C(n, k)), (n, k))


def u7_dice_a(r, L):
    s = r.randint(2, 12)
    return ('Two fair dice: find P(sum = %d).' % s, fr(Fr(sum(1 for a in range(1, 7) for c in range(1, 7) if a + c == s), 36)), s)


def u7_dice_b(r, L):
    k, n = r.randint(1, 6), r.choice([6, 12, 18, 36])
    return ('A bag has %d red and %d blue marbles. Find P(red).' % (k, n - k), fr(Fr(k, n)), (k, n))


def u7_list_a(r, L):
    m, n = r.randint(5, 40), r.randint(50, 120)
    return ('How many integers are in the list %d, %d, ..., %d?' % (m, m + 1, n), str(n - m + 1), (m, n))


u7_list_b = u7_list_a


# ======================================================================= Unit 8
def u8_kn_a(r, L):
    n = r.randint(3, 9)
    return ('How many edges does K_%d have?' % n, str(C(n, 2)), n)


def u8_kn_b(r, L):
    n = r.randint(3, 9)
    return ('At a party, each of %d people shakes hands once with every other person. How many handshakes?' % n, str(C(n, 2)), n)


def u8_tree_a(r, L):
    n = r.randint(4, 20)
    return ('How many edges does a tree with %d vertices have?' % n, str(n - 1), n)


def u8_tree_b(r, L):
    m = r.randint(4, 20)
    return ('A graph has degree sum %d. How many edges does it have?' % (2 * m), str(m), m)


def u8_deg_a(r, L):
    degs = [r.randint(1, 5) for _ in range(r.randint(4, 6))]
    if sum(degs) % 2:
        degs[0] += 1
    return ('A graph has degrees %s. How many edges?' % ', '.join(map(str, degs)), str(sum(degs) // 2), tuple(degs))


def u8_deg_b(r, L):
    n, d = r.randint(4, 10), r.choice([2, 4])
    return ('Every vertex of a graph with %d vertices has degree %d. How many edges?' % (n, d), str(n * d // 2), (n, d))


def u8_chi_a(r, L):
    n = r.randint(3, 9)
    return ('What is the chromatic number of the cycle C_%d?' % n, str(2 if n % 2 == 0 else 3), n)


def u8_chi_b(r, L):
    n = r.randint(2, 5)
    return ('What is the chromatic number of K_%d?' % n, str(n), n)


def u8_kmn_a(r, L):
    m, n = r.randint(2, 6), r.randint(2, 6)
    return ('How many edges does K_%d,%d have?' % (m, n), str(m * n), (m, n))


def u8_kmn_b(r, L):
    n = r.randint(3, 12)
    return ('How many edges does a Hamiltonian cycle in a graph with %d vertices use?' % n, str(n), n)


# ======================================================================= Unit 9
def u9_maj_a(r, L):
    n = r.randint(11, 61)
    return ('How many votes are a majority of %d votes?' % n, str(n // 2 + 1), n)


def u9_maj_b(r, L):
    w = [r.randint(1, 9) for _ in range(r.randint(3, 4))]
    return ('Weights %s: what is the smallest quota that is more than half the total?' % ', '.join(map(str, w)), str(sum(w) // 2 + 1), tuple(w))


def u9_borda_a(r, L):
    n = r.randint(3, 4)
    v = r.randint(3, 12)
    return ('%d voters rank X first among %d candidates (Borda: n points for 1st). How many points does X get from them?' % (v, n), str(v * n), (v, n))


def u9_banz_a(r, L):
    w = sorted([r.randint(1, 8) for _ in range(3)], reverse=True)
    q = sum(w) // 2 + 1
    c = [0] * 3
    for m in range(1, 8):
        s = sum(w[i] for i in range(3) if m >> i & 1)
        if s >= q:
            for i in range(3):
                if m >> i & 1 and s - w[i] < q:
                    c[i] += 1
    return ('In [%d: %d, %d, %d], how many times is P1 critical (over all winning coalitions)?' % (q, *w), str(c[0]), (q, tuple(w)))


u9_banz_b = u9_banz_a


def u9_sd_a(r, L):
    seats = r.randint(5, 25)
    d = r.randint(10, 90) * 10
    return ('Total population %d, %d seats. Find the standard divisor.' % (d * seats, seats), str(d), (d, seats))


u9_sd_b = u9_sd_a


# ======================================================================= Unit 10
def lp_vertices(cons):
    allc = list(cons) + [(-1, 0, 0), (0, -1, 0)]
    pts = set()
    for (a1, b1, c1), (a2, b2, c2) in itertools.combinations(allc, 2):
        det = a1 * b2 - a2 * b1
        if det == 0:
            continue
        x, y = Fr(c1 * b2 - c2 * b1, det), Fr(a1 * c2 - a2 * c1, det)
        if x >= 0 and y >= 0 and all(a * x + b * y <= c for a, b, c in cons):
            pts.add((x, y))
    return pts


def ctx(cons):
    return ', '.join('%sx + %sy ≤ %d' % ('' if a == 1 else a, '' if b == 1 else b, c) for a, b, c in cons) + ', x, y ≥ 0'


def u10_max_a(r, L):
    cons = [(r.randint(1, 3), r.randint(1, 3), r.randint(6, 18)), (r.randint(1, 3), r.randint(1, 3), r.randint(6, 18))]
    obj = (r.randint(1, 5), r.randint(1, 5))
    V = lp_vertices(cons)
    if not V:
        return None
    best = max(obj[0] * x + obj[1] * y for x, y in V)
    return ('Maximize P = %dx + %dy subject to %s. Give the maximum value.' % (obj[0], obj[1], ctx(cons)), fr(best), (tuple(cons), obj))


u10_max_b = u10_max_a


def u10_int_a(r, L):
    x, y = r.randint(1, 6), r.randint(1, 6)
    a1, b1, a2, b2 = r.randint(1, 3), r.randint(1, 3), r.randint(1, 3), r.randint(1, 3)
    if a1 * b2 == a2 * b1:
        return None
    return ('Find the corner where %dx + %dy = %d meets %dx + %dy = %d.' % (a1, b1, a1 * x + b1 * y, a2, b2, a2 * x + b2 * y), '(%d, %d)' % (x, y), (x, y, a1, b1, a2, b2))


u10_int_b = u10_int_a


def u10_eval_a(r, L):
    p, q, x, y = r.randint(1, 9), r.randint(1, 9), r.randint(0, 8), r.randint(0, 8)
    return ('Evaluate P = %dx + %dy at (%d, %d).' % (p, q, x, y), str(p * x + q * y), (p, q, x, y))


u10_eval_b = u10_eval_a


def u10_slack_a(r, L):
    a, b, c, x, y = r.randint(1, 4), r.randint(1, 4), r.randint(20, 40), r.randint(0, 4), r.randint(0, 4)
    if a * x + b * y > c:
        return None
    return ('At (%d, %d), how much slack does %dx + %dy ≤ %d have?' % (x, y, a, b, c), str(c - a * x - b * y), (a, b, c, x, y))


u10_slack_b = u10_slack_a


UNITS = {
    'speaking-mathematically': [('u1_prod', 'Cartesian products'), ('u1_sub', 'Subsets and strings'), ('u1_truth', 'Truth sets'), ('u1_pair', 'Ordered pairs'), ('u1_card', 'Set-builder counts')],
    'compound-statements-logic': [('u2_col', 'Truth columns'), ('u2_count', 'True rows'), ('u2_cx', 'Counterexample rows'), ('u2_rows', 'Table size')],
    'number-theory-proof': [('u3_gcd', 'Greatest common divisor'), ('u3_rem', 'Quotient-remainder'), ('u3_div', 'Counting divisors'), ('u3_ce', 'Counterexamples'), ('u3_frac', 'Rational numbers')],
    'sequences-induction-recursion': [('u4_ar', 'Arithmetic and recursive terms'), ('u4_binom', 'Binomial coefficients'), ('u4_sum', 'Sums'), ('u4_rec', 'Recursion and iteration'), ('u4_fac', 'Factorials')],
    'set-theory': [('u5_op', 'Set operations'), ('u5_ie', 'Inclusion-exclusion'), ('u5_pow', 'Power sets')],
    'properties-relations': [('u6_lt', 'Counting pairs'), ('u6_cls', 'Equivalence classes'), ('u6_ind', 'Induced relations'), ('u6_refl', 'Counting relations')],
    'counting-probability': [('u7_mult', 'Multiplication rule'), ('u7_perm', 'Permutations'), ('u7_comb', 'Combinations'), ('u7_dice', 'Probability'), ('u7_list', 'Lists')],
    'graphs-trees': [('u8_kn', 'Complete graphs'), ('u8_tree', 'Trees and degree sums'), ('u8_deg', 'Handshake theorem'), ('u8_chi', 'Coloring'), ('u8_kmn', 'Bipartite graphs and cycles')],
    'election-theory': [('u9_maj', 'Majorities and quotas'), ('u9_banz', 'Critical players'), ('u9_sd', 'Standard divisors')],
    'linear-programming': [('u10_max', 'Optimal values'), ('u10_int', 'Corner points'), ('u10_eval', 'Objective values'), ('u10_slack', 'Slack')],
}
# replace the awkward Borda B generator with a clean second-place version
def u9_borda_b(r, L):
    v, n = r.randint(3, 12), r.randint(3, 4)
    return ('%d voters rank X second among %d candidates (Borda: n points for 1st). How many points does X get from them?' % (v, n + 1), str(v * n), (v, n))


UNITS['election-theory'].insert(1, ('u9_borda', 'Borda points'))


def make_pairs(unit, level, set_no, want=6):
    fams = UNITS[unit]
    g = globals()
    rng = random.Random('%s|%s|%s' % (unit, level, set_no))
    pairs, used_answers, used_prompts = [], set(), set()
    fams = [f for f in fams if not (f[0] == 'u2_rows' and level != 'cp2') and not (f[0] == 'u2_cx' and level == 'cp2')]
    order = fams[set_no - 1:] + fams[:set_no - 1]
    for rnd in range(60):
        for fam, title in order:
            if len(pairs) >= want:
                break
            if sum(1 for p in pairs if p['family'] == fam) > rnd // len(order) + (1 if len(order) < want else 0):
                continue
            A = [g[fam + '_a'](rng, level) for _ in range(80)]
            B = [g[fam + '_b'](rng, level) for _ in range(80)]
            A = [x for x in A if x]
            B = [x for x in B if x]
            byB = {}
            for t, a, prm in B:
                byB.setdefault(a, []).append((t, prm))
            rng.shuffle(A)
            for t, a, prm in A:
                if a in used_answers or t in used_prompts or a not in byB:
                    continue
                cands = [x for x in byB[a] if x[0] != t and x[0] not in used_prompts]
                if not cands:
                    continue
                tb, pb = rng.choice(cands)
                pairs.append({'family': fam, 'title': title, 'A': t, 'B': tb, 'answer': a})
                used_answers.add(a); used_prompts.update([t, tb])
                break
        if len(pairs) >= want:
            break
    assert len(pairs) >= want, (unit, level, set_no, len(pairs))
    rng.shuffle(pairs)
    return pairs


def verify(pairs, unit, level):
    """Independent re-check: parse each printed problem back through a family-specific solver (different code path from the
    generators: the solvers read numbers from the TEXT) and confirm both partners' answers equal the stored key."""
    import re
    def nums(t):
        return [int(x) for x in re.findall(r'(?<![A-Za-z_₀-₉])-?\d+', t.replace('−', '-'))]
    for p in pairs:
        for side in ('A', 'B'):
            t = p[side]
            sol = solve_text(t)
            if sol is not None:
                assert sol == p['answer'], (unit, level, side, t, sol, p['answer'])
                p.setdefault('checked', 0)
                p['checked'] += 1
    return pairs


def solve_text(t):
    """Text-level solvers for the families (return None when a text form is not handled)."""
    import re
    T = t.replace('−', '-')
    n = [int(x) for x in re.findall(r'(?<![A-Za-z_])\d+', T)]
    m = re.search(r'truth column of (.+) \(standard', t)
    if m:
        f = m.group(1)
        return LG.colstr(f, ['p', 'q', 'r'] if 'r' in f else ['p', 'q'])
    m = re.search(r'variables ([pqr, ]+)\) is (.+) true', t)
    if m:
        return str(sum(LG.column(m.group(2), [v.strip() for v in m.group(1).split(',')])))
    if 'ordered pairs are in A × B' in t or t.startswith('A code is one letter'):
        return str(n[0] * n[1])
    if 'subsets does a set with' in t or 'bit strings of length' in t and 'exactly' not in t or 'power set of a' in t:
        return str(2 ** n[0])
    if t.startswith('Find gcd('):
        return str(math.gcd(n[0], n[1]))
    if 'positive divisors does' in t:
        return str(sum(1 for d in range(1, n[0] + 1) if n[0] % d == 0))
    if 'Evaluate C(' in t:
        return str(C(n[0], n[1]))
    mk = re.search(r'How many edges does K_(\d+) have', t)
    if mk:
        return str(C(int(mk.group(1)), 2))
    if 'shakes hands once with every other' in t:
        return str(C(n[0], 2))
    if 'edges does a tree with' in t:
        return str(n[0] - 1)
    if 'majority of' in t:
        return str(n[0] // 2 + 1)
    if t.startswith('Evaluate P ='):
        return str(n[0] * n[2] + n[1] * n[3])
    if 'list' in t and 'integers are in the list' in t:
        return str(n[-1] - n[0] + 1)
    sets = [set(int(x) for x in g.split(', ')) if g else set() for g in re.findall(r'\{([\d, ]*)\}', T)]
    if re.match(r'A = \{', t) and 'Find A' in t:
        A, B = sets[0], sets[1]
        op = re.search(r'Find A (.) B', t).group(1)
        return fs(A | B if op == '∪' else A & B if op == '∩' else A - B)
    if t.startswith('U = {1, ..., 10}'):
        A, B = sets[0], sets[1]
        return fs(set(range(1, 11)) - (A | B)) if "(A ∪ B)'" in t else fs(B - A)
    if t.startswith('Domain D'):
        d = re.search(r'"(.+)"', t).group(1)
        return fs(x for x in range(-3, 4) if dict(PRED)[d](x))
    m = re.search(r'Solve \((\d)x − (\d+), y \+ (\d+)\) = \((-?\d+), (-?\d+)\)', t)
    if m:
        a, c, k, u, v = map(int, m.groups())
        return '(%d, %d)' % ((u + c) // a, v - k)
    m = re.search(r'Solve \(x \+ y, x − y\) = \((-?\d+), (-?\d+)\)', t)
    if m:
        u, v = int(m.group(1)), int(m.group(2))
        return '(%d, %d)' % ((u + v) // 2, (u - v) // 2)
    m = re.search(r'\{n ∈ ℤ \| (-?\d+) ≤ n ≤ (-?\d+)\}', T)
    if m:
        return str(int(m.group(2)) - int(m.group(1)) + 1)
    if 'positive multiples of 3 are at most' in t:
        return str(n[-1] // 3)
    m = re.search(r'remainder r when (-?\d+) = (\d+)·q', T)
    if m:
        return str(int(m.group(1)) % int(m.group(2)))
    m = re.search(r'counterexample to "for all n ≥ 1, (.+)"', t)
    if m:
        f = dict(CONJ3)[m.group(1)]
        return str(next(k for k in range(1, 60) if not f(k)))
    m = re.search(r'Simplify (\d+)/(\d+)', t)
    if m:
        return fr(Fr(int(m.group(1)), int(m.group(2))))
    m = re.search(r'a₁ = (-?\d+), d = (\d+)\. Find a_(\d+)', T) or re.search(r'a₁ = (-?\d+) and a_n = a_\(n-1\) \+ (\d+)\. Find a_(\d+)', T)
    if m:
        a1, d, k = map(int, m.groups())
        return str(a1 + (k - 1) * d)
    m2 = re.search(r'2-element subsets does a (\d+)-element set', t)
    if m2:
        return str(C(int(m2.group(1)), 2))
    m = re.search(r'1 \+ 2 \+ \.\.\. \+ (\d+)', t) or re.search(r'Σ_\{k=1\}\^\{(\d+)\} k', t)
    if m:
        k = int(m.group(1)); return str(k * (k + 1) // 2)
    m = re.search(r'a₀ = (\d+), a_n = 2a_\(n-1\) ([+-]) (\d+)\. Find a_(\d+)', T)
    if m:
        a, sg, c, k = int(m.group(1)), m.group(2), int(m.group(3)), int(m.group(4))
        c = c if sg == '+' else -c
        for _ in range(k):
            a = 2 * a + c
        return str(a)
    if 'Tower of Hanoi' in t:
        return str(2 ** n[0] - 1)
    m = re.search(r'Evaluate (\d+)!/(\d+)!', t)
    if m:
        return str(math.factorial(int(m.group(1))) // math.factorial(int(m.group(2))))
    m = re.search(r'How many ways can (\d+) different medals be given to \d+ of (\d+)', t) or re.search(r'How many ways can (\d+) of (\d+) people fill', t)
    if m:
        return str(math.perm(int(m.group(2)), int(m.group(1))))
    m = re.search(r'How many (\d+)-letter strings with no repeated letter use letters from a (\d+)-letter', t)
    if m:
        return str(math.perm(int(m.group(2)), int(m.group(1))))
    m = re.search(r'How many (\d+)-person committees can be chosen from (\d+)', t)
    if m:
        return str(C(int(m.group(2)), int(m.group(1))))
    m = re.search(r'bit strings of length (\d+) have exactly (\d+) ones', t)
    if m:
        return str(C(int(m.group(1)), int(m.group(2))))
    m = re.search(r'P\(sum = (\d+)\)', t)
    if m:
        k = int(m.group(1)); return fr(Fr(sum(1 for a in range(1, 7) for c in range(1, 7) if a + c == k), 36))
    m = re.search(r'(\d+) red and (\d+) blue marbles', t)
    if m:
        return fr(Fr(int(m.group(1)), int(m.group(1)) + int(m.group(2))))
    m = re.search(r'(\d+) shirts, (\d+) pants and (\d+) hats', t)
    if m:
        return str(int(m.group(1)) * int(m.group(2)) * int(m.group(3)))
    m = re.search(r'\|A\| = (\d+), \|B\| = (\d+), \|A ∩ B\| = (\d+)', t)
    if m:
        return str(int(m.group(1)) + int(m.group(2)) - int(m.group(3)))
    m = re.search(r'(\d+) in A only, (\d+) in B only and (\d+) in both', t)
    if m:
        return str(sum(map(int, m.groups())))
    m = re.search(r'subsets of \{1, \.\.\., (\d+)\} contain the element 1', t)
    if m:
        return str(2 ** (int(m.group(1)) - 1))
    m = re.search(r'"a [<>] b" on \{1, \.\.\., (\d+)\}', t)
    if m:
        return str(C(int(m.group(1)), 2))
    m = re.search(r'Congruence mod (\d+) on \{0, 1, \.\.\., 12\}\. Find \[(\d+)\]', t) or re.search(r'same remainder mod (\d+)\. List all b with (\d+) R b', t)
    if m:
        md, x = int(m.group(1)), int(m.group(2)); return fs(y for y in range(13) if (y - x) % md == 0)
    m = re.search(r'blocks of sizes ([\d, ]+)\.', t)
    if m:
        return str(sum(int(x) ** 2 for x in m.group(1).split(', ')))
    m = re.search(r'How many (reflexive|symmetric) relations are there on a (\d+)-element', t)
    if m:
        k = int(m.group(2)); return str(2 ** (k * k - k) if m.group(1) == 'reflexive' else 2 ** (k * (k + 1) // 2))
    m = re.search(r'degree sum (\d+)', t)
    if m:
        return str(int(m.group(1)) // 2)
    m = re.search(r'A graph has degrees ([\d, ]+)\.', t)
    if m:
        return str(sum(int(x) for x in m.group(1).split(', ')) // 2)
    m = re.search(r'graph with (\d+) vertices has degree (\d+)', t)
    if m:
        return str(int(m.group(1)) * int(m.group(2)) // 2)
    m = re.search(r'chromatic number of the cycle C_(\d+)', t)
    if m:
        return '2' if int(m.group(1)) % 2 == 0 else '3'
    m = re.search(r'chromatic number of K_(\d+)', t)
    if m:
        return m.group(1)
    m = re.search(r'edges does K_(\d+),(\d+)', t)
    if m:
        return str(int(m.group(1)) * int(m.group(2)))
    m = re.search(r'Hamiltonian cycle in a graph with (\d+) vertices', t)
    if m:
        return m.group(1)
    m = re.search(r'Weights ([\d, ]+): what is the smallest quota', t)
    if m:
        return str(sum(int(x) for x in m.group(1).split(', ')) // 2 + 1)
    m = re.search(r'(\d+) voters rank X (first|second) among (\d+) candidates', t)
    if m:
        v, pos, k = int(m.group(1)), m.group(2), int(m.group(3)); return str(v * (k if pos == 'first' else k - 1))
    m = re.search(r'In \[(\d+): (\d+), (\d+), (\d+)\], how many times is P1 critical', t)
    if m:
        q, *w = map(int, m.groups()); cnt = 0
        for mm in range(1, 8):
            s_ = sum(w[i] for i in range(3) if mm >> i & 1)
            if s_ >= q and mm & 1 and s_ - w[0] < q:
                cnt += 1
        return str(cnt)
    m = re.search(r'Total population (\d+), (\d+) seats', t)
    if m:
        return fr(Fr(int(m.group(1)), int(m.group(2))))
    m = re.search(r'where (\d)x \+ (\d)y = (\d+) meets (\d)x \+ (\d)y = (\d+)', t)
    if m:
        a1, b1, c1, a2, b2, c2 = map(int, m.groups()); det = a1 * b2 - a2 * b1
        return '(%s, %s)' % (fr(Fr(c1 * b2 - c2 * b1, det)), fr(Fr(a1 * c2 - a2 * c1, det)))
    m = re.search(r'At \((\d+), (\d+)\), how much slack does (\d)x \+ (\d)y ≤ (\d+)', t)
    if m:
        x, y, a, b_, c = map(int, m.groups()); return str(c - a * x - b_ * y)
    m = re.search(r'Maximize P = (\d)x \+ (\d)y subject to (.+)\. Give', t)
    if m:
        p, q = int(m.group(1)), int(m.group(2)); cons = []
        for part in re.findall(r'(\d*)x \+ (\d*)y ≤ (\d+)', m.group(3)):
            cons.append((int(part[0] or 1), int(part[1] or 1), int(part[2])))
        V = lp_vertices(cons)
        return fr(max(p * x + q * y for x, y in V))
    m = re.search(r'Premises: (.+)\. Conclusion: (.+)\. Give the only row', t)
    if m:
        rows = cx_rows(m.group(1).split('; '), m.group(2))
        return rows[0] if len(rows) == 1 else 'AMBIGUOUS'
    m = re.search(r'truth table with (\d+) variables', t)
    if m:
        return str(2 ** int(m.group(1)))
    m = re.search(r'truth table for (.+) have\?', t)
    if m:
        return str(2 ** len(set(re.findall(r'[a-z]', m.group(1)))))
    m = re.search(r'Write ([\d.]+) as a fraction', t)
    if m:
        return fr(Fr(m.group(1)).limit_denominator(100))
    return None


if __name__ == '__main__':
    tot = 0
    for u in UNITS:
        for L in ('cp2', 'cp1', 'honors'):
            for s in (1, 2):
                P = verify(make_pairs(u, L, s), u, L)
                tot += len(P)
    print('pairs', tot)
