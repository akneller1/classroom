"""Unit 4: Sequences, Mathematical Induction, and Recursion (9 skills). All terms, sums and counts computed."""
import math
from fractions import Fraction
from core import Bank, frac, fix_text

U = 'sequences-induction-recursion'
C = math.comb


def build():
    b = Bank(U, 'sq', 9)
    for f in (s1, s2, s3, s4, s5, s6, s7, s8, s9, topup, topup2, errors, honors_partners):
        f(b)
    return b


def terms(f, a, n):
    return [f(k) for k in range(a, a + n)]


def lst(xs):
    return ', '.join(frac(x) if isinstance(x, Fraction) else str(x) for x in xs)


# ---------------------------------------------------------------- 1. sequences and explicit formulas
EXPL = [('a_n = 3n − 1', lambda n: 3 * n - 1, 1, 'cp2'), ('a_n = n² + 1', lambda n: n * n + 1, 1, 'cp2'), ('a_n = 2ⁿ', lambda n: 2 ** n, 0, 'cp2'),
        ('a_n = (−1)ⁿ · n', lambda n: (-1) ** n * n, 1, 'cp1'), ('a_n = n/(n + 1)', lambda n: Fraction(n, n + 1), 1, 'cp1'), ('a_n = n² − n', lambda n: n * n - n, 0, 'cp1'),
        ('a_n = (−1)ⁿ⁺¹/n', lambda n: Fraction((-1) ** (n + 1), n), 1, 'honors'), ('a_n = ⌊n/2⌋', lambda n: n // 2, 0, 'honors'), ('a_n = n! / 2ⁿ', lambda n: Fraction(math.factorial(n), 2 ** n), 1, 'honors')]
FIND = [  # (terms, start, correct formula, distractors, checker)
    ('3, 5, 7, 9, ...', 1, 'a_n = 2n + 1', ['a_n = n + 2', 'a_n = 2n − 1', 'a_n = 3n'], lambda n: 2 * n + 1, 'cp2'),
    ('1, 4, 9, 16, ...', 1, 'a_n = n²', ['a_n = 3n − 2', 'a_n = 2ⁿ', 'a_n = n² + 1'], lambda n: n * n, 'cp2'),
    ('1, −1, 1, −1, ...', 0, 'a_n = (−1)ⁿ', ['a_n = (−1)ⁿ⁺¹', 'a_n = −n', 'a_n = 1 − n'], lambda n: (-1) ** n, 'cp1'),
    ('1/2, 2/3, 3/4, 4/5, ...', 1, 'a_n = n/(n + 1)', ['a_n = (n + 1)/n', 'a_n = 1/(n + 1)', 'a_n = n/(n + 2)'], lambda n: Fraction(n, n + 1), 'cp1'),
    ('0, 2, 6, 12, 20, ...', 1, 'a_n = n² − n', ['a_n = 2n − 2', 'a_n = n² − 1', 'a_n = 2ⁿ − 2'], lambda n: n * n - n, 'honors'),
    ('1, −1/2, 1/3, −1/4, ...', 1, 'a_n = (−1)ⁿ⁺¹/n', ['a_n = (−1)ⁿ/n', 'a_n = 1/n', 'a_n = −1/n'], lambda n: Fraction((-1) ** (n + 1), n), 'honors'),
]
SIGMA = [('Σ_{k=1}^{5} k', lambda: sum(range(1, 6)), 'cp2'), ('Σ_{k=1}^{4} (2k + 1)', lambda: sum(2 * k + 1 for k in range(1, 5)), 'cp2'), ('Σ_{k=0}^{4} 2ᵏ', lambda: sum(2 ** k for k in range(5)), 'cp1'),
         ('Σ_{k=1}^{6} (−1)ᵏ k', lambda: sum((-1) ** k * k for k in range(1, 7)), 'cp1'), ('Π_{k=1}^{4} k', lambda: math.prod(range(1, 5)), 'cp1'),
         ('Σ_{k=1}^{4} 1/(k(k + 1))', lambda: sum(Fraction(1, k * (k + 1)) for k in range(1, 5)), 'honors'), ('Π_{k=2}^{5} (1 − 1/k)', lambda: math.prod(1 - Fraction(1, k) for k in range(2, 6)), 'honors')]


def s1(b):
    for disp, f, a, L in EXPL:
        t = terms(f, a, 4)
        b.sa(1, L, 'Write the first four terms of the sequence %s, starting with n = %d. Separate terms with commas (fractions as a/b).' % (disp, a), lst(t),
             ['Substitute n = %s.' % ', '.join(str(k) for k in range(a, a + 4)), 'Terms: ' + lst(t)], 'first_terms')
    for t, a, good, bad, f, L in FIND:
        b.mc(1, L, 'Which explicit formula fits %s (first term at n = %d)?' % (t, a), good, bad,
             ['Test each formula at n = %d, %d, %d.' % (a, a + 1, a + 2), 'Only %s gives %s.' % (good, lst(terms(f, a, 4)))], 'find_formula')
    for disp, f, L in SIGMA:
        v = f()
        b.sa(1, L, 'Evaluate %s. (Give an integer or a fraction a/b.)' % disp, frac(v),
             ['Write out each term and add (Σ) or multiply (Π).', 'Value: %s' % frac(v)], 'sigma_eval')
    b.sel(1, 'cp2', 'For a_n = 4n − 3 (n ≥ 1), which numbers are terms of the sequence?', [(str(x), (x + 3) % 4 == 0 and x >= 1) for x in (1, 13, 20, 41, 6)],
          ['A number x is a term when x = 4n − 3 for a positive integer n, that is, when x + 3 is a positive multiple of 4.'], 'is_term_select')
    b.sel(1, 'cp1', 'Which expressions equal 1 + 3 + 5 + 7 + 9?', [('Σ_{k=1}^{5} (2k − 1)', True), ('Σ_{k=0}^{4} (2k + 1)', True), ('Σ_{k=1}^{5} 2k', False), ('5²', True), ('Σ_{k=1}^{9} k', False)],
          ['Each correct sum lists 1, 3, 5, 7, 9; the sum is 25 = 5².', 'Σ 2k = 30 and Σ_{1}^{9} k = 45.'], 'sigma_select')
    b.sel(1, 'honors', 'Which expressions equal Σ_{k=1}^{n} (k + 1) for every n ≥ 1?', [('Σ_{j=2}^{n+1} j', True), ('Σ_{k=1}^{n} k + n', True), ('n(n + 3)/2', True), ('Σ_{k=1}^{n} k + 1', False), ('(n + 1)²', False)],
          ['Change of variable j = k + 1 shifts the limits.', 'Σ(k + 1) = n(n + 1)/2 + n = n(n + 3)/2.', 'Σ k + 1 adds 1 only once.'], 'sigma_select')
    b.orq(1, 'cp2', 'Consider a_n = 5n + 2 for n ≥ 1.',
          [('Find a₁, a₂, a₃.', '7, 12, 17'), ('Find a₁₀.', '52'), ('Is 77 a term? If so, which one?', 'Yes, a₁₅'), ('Describe the pattern in words.', 'Start at 7 and add 5 each time.')],
          ['Substitute.', '5·10 + 2.', '5n + 2 = 77 gives n = 15.', 'Common difference 5.'], 'explicit_or')
    b.orq(1, 'cp1', 'Consider S = Σ_{k=1}^{4} k².',
          [('Write S in expanded form.', '1 + 4 + 9 + 16'), ('Evaluate S.', '30'), ('Rewrite S with index j = k − 1.', 'Σ_{j=0}^{3} (j + 1)²'), ('Evaluate Σ_{k=1}^{4} (k² + 1).', '34')],
          ['Expand.', 'Add.', 'Shift the limits down by 1.', 'Adds four 1s.'], 'sigma_or')
    b.orq(1, 'honors', 'Telescoping sum: T_n = Σ_{k=1}^{n} (1/k − 1/(k + 1)).',
          [('Write out T₃.', '(1 − 1/2) + (1/2 − 1/3) + (1/3 − 1/4)'), ('Simplify T₃.', '3/4'), ('Find a formula for T_n.', '1 − 1/(n + 1) = n/(n + 1)'),
           ('Use it to evaluate Σ_{k=1}^{99} 1/(k(k + 1)).', '99/100')],
          ['Expand.', 'Middle terms cancel.', 'Only the first and last survive.', '1/(k(k + 1)) = 1/k − 1/(k + 1).'], 'telescope_or')


# ---------------------------------------------------------------- 2. arithmetic and geometric
def s2(b):
    AR = [(3, 4, 20, 'cp2'), (50, -3, 15, 'cp2'), (-7, 6, 31, 'cp1'), (2.5, 1.5, 12, 'cp1'), (100, -0.5, 101, 'honors')]
    for a1, d, n, L in AR:
        an = a1 + (n - 1) * d
        fmt = lambda x: str(int(x)) if float(x).is_integer() else str(x)
        b.sa(2, L, 'An arithmetic sequence has a₁ = %s and common difference d = %s. Find a_%d.' % (fmt(a1), fmt(d), n), fmt(an),
             ['a_n = a₁ + (n − 1)d.', 'a_%d = %s + %d(%s) = %s' % (n, fmt(a1), n - 1, fmt(d), fmt(an))], 'arith_term')
    GE = [(2, 3, 6, 'cp2'), (5, 2, 8, 'cp2'), (81, Fraction(1, 3), 5, 'cp1'), (-2, -2, 7, 'cp1'), (Fraction(1, 4), 2, 10, 'honors')]
    for a1, r, n, L in GE:
        an = Fraction(a1) * Fraction(r) ** (n - 1)
        b.sa(2, L, 'A geometric sequence has a₁ = %s and common ratio r = %s. Find a_%d.' % (frac(a1), frac(r), n), frac(an),
             ['a_n = a₁ rⁿ⁻¹.', 'a_%d = %s · (%s)^%d = %s' % (n, frac(a1), frac(r), n - 1, frac(an))], 'geom_term')
    SUMS = [('1 + 2 + 3 + ... + 100', 5050, 'cp2', 'n(n + 1)/2 with n = 100.'), ('2 + 4 + 6 + ... + 50', sum(range(2, 51, 2)), 'cp1', '25 terms, average 26: 25·26.'),
            ('1 + 2 + 4 + ... + 2⁹', 2 ** 10 - 1, 'cp1', 'Geometric sum (2¹⁰ − 1)/(2 − 1).'), ('5 + 8 + 11 + ... + 62', sum(range(5, 63, 3)), 'honors', '20 terms: 20(5 + 62)/2.'),
            ('3 + 6 + 12 + ... + 768', sum(3 * 2 ** k for k in range(9)), 'honors', '9 terms: 3(2⁹ − 1).'), ('1 + 3 + 5 + ... + 39', 400, 'cp2', 'The sum of the first n odd numbers is n²; n = 20.')]
    for t, v, L, why in SUMS:
        b.sa(2, L, 'Find the sum: %s' % t, v, [why, 'Sum = %d' % v], 'series_sum')
    CL = [('4, 9, 14, 19, ...', 'Arithmetic, d = 5', 'cp2'), ('3, 6, 12, 24, ...', 'Geometric, r = 2', 'cp2'), ('1, 4, 9, 16, ...', 'Neither', 'cp1'),
          ('10, 5, 2.5, 1.25, ...', 'Geometric, r = 1/2', 'cp1'), ('7, 7, 7, 7, ...', 'Both arithmetic (d = 0) and geometric (r = 1)', 'honors'), ('2, −6, 18, −54, ...', 'Geometric, r = −3', 'honors')]
    allc = ['Arithmetic, d = 5', 'Geometric, r = 2', 'Neither', 'Geometric, r = 1/2', 'Both arithmetic (d = 0) and geometric (r = 1)', 'Geometric, r = −3', 'Arithmetic, d = 3', 'Arithmetic, d = −8']
    for t, good, L in CL:
        b.mc(2, L, 'Classify the sequence %s' % t, good, [c for c in allc if c != good][:3] if good != 'Neither' else ['Arithmetic, d = 3', 'Geometric, r = 2', 'Arithmetic, d = 5'],
             ['Check differences between consecutive terms and ratios between consecutive terms.', good], 'classify_seq')
    b.sel(2, 'cp1', 'Which sequences are arithmetic?', [('a_n = 7 − 2n', True), ('a_n = n²', False), ('5, 5.5, 6, 6.5, ...', True), ('a_n = 3·2ⁿ', False), ('a_n = −n', True)],
          ['Arithmetic means a constant difference: linear formulas in n.'], 'arith_select')
    b.sel(2, 'honors', 'A geometric sequence has a₂ = 12 and a₄ = 48. Which could be a₁?', [('6', True), ('−6', True), ('3', False), ('24', False), ('−3', False)],
          ['a₄/a₂ = r² = 4, so r = 2 or r = −2.', 'a₁ = a₂/r = 6 or −6.'], 'geom_select')
    b.sel(2, 'cp2', 'Which sequences are geometric?', [('2, 6, 18, 54', True), ('1, 2, 3, 4', False), ('100, 10, 1, 0.1', True), ('1, 1, 2, 3', False), ('5, −5, 5, −5', True)],
          ['Geometric means a constant ratio.'], 'geom_select')
    b.orq(2, 'cp2', 'A theater has 20 seats in row 1, 23 in row 2, 26 in row 3, and so on for 15 rows.',
          [('Is the pattern arithmetic or geometric?', 'Arithmetic, d = 3'), ('Write a formula for the number of seats in row n.', 'a_n = 20 + 3(n − 1) = 3n + 17'),
           ('How many seats are in row 15?', '62'), ('How many seats are there in total?', '615')],
          ['Constant difference.', 'a_n = a₁ + (n − 1)d.', '3·15 + 17.', '15(20 + 62)/2 = 615.'], 'arith_or')
    b.orq(2, 'cp1', 'A ball is dropped from 16 ft and rebounds to 3/4 of its previous height each time.',
          [('Find the heights of the first three rebounds.', '12, 9, 27/4 ft'), ('Write a formula for the nth rebound height.', 'h_n = 16(3/4)ⁿ'),
           ('Find the 5th rebound height as a fraction.', '243/16 ft'), ('Is the sequence arithmetic or geometric?', 'Geometric, r = 3/4')],
          ['Multiply by 3/4.', 'Geometric with first term 12.', '16·(3/4)⁵ = 243/64 · 4 = 243/16.', 'Constant ratio.'], 'geom_or')
    b.orq(2, 'honors', 'Insert numbers between 3 and 192 to form sequences with 7 terms total.',
          [('Find the common difference if the sequence is arithmetic.', '189/6 = 31.5'), ('Find the common ratio if it is geometric with positive terms.', '2'),
           ('Write the geometric sequence.', '3, 6, 12, 24, 48, 96, 192'), ('Find the sum of the geometric sequence.', '381')],
          ['a₇ = a₁ + 6d.', 'a₇ = a₁r⁶, r⁶ = 64.', 'Double each time.', '3(2⁷ − 1) = 381.'], 'means_or')


# ---------------------------------------------------------------- 3. factorials and binomial coefficients
def s3(b):
    FA = [('5!', 120, 'cp2'), ('0!', 1, 'cp2'), ('7!/5!', 42, 'cp2'), ('10!/(8! 2!)', 45, 'cp1'), ('6!/(3!·3!)', 20, 'cp1'), ('(n + 1)!/n! for n = 9', 10, 'cp1'),
          ('100!/98!', 9900, 'honors'), ('C(12, 3)', C(12, 3), 'honors')]
    for t, v, L in FA:
        b.sa(3, L, 'Evaluate %s.' % t, v, ['n! = n(n − 1)(n − 2)···1 and 0! = 1; cancel common factors before multiplying.', '%s = %d' % (t, v)], 'factorial_eval')
    BC = [(5, 2, 'cp2'), (6, 0, 'cp2'), (7, 3, 'cp1'), (8, 6, 'cp1'), (10, 5, 'honors'), (20, 18, 'honors')]
    for n, r, L in BC:
        b.mc(3, L, 'Evaluate C(%d, %d), also written ( %d choose %d ).' % (n, r, n, r), str(C(n, r)),
             [str(x) for x in dict.fromkeys([math.perm(n, r), C(n, r) + n, n * r, 0, n, 2 * C(n, r) + 1]) if x != C(n, r)][:3],
             ['C(n, r) = n! / (r!(n − r)!).', 'C(%d, %d) = %d' % (n, r, C(n, r))], 'binom_eval', order='sort')
    SIMP = [('cp1', 'n!/(n − 1)!', 'n', ['n − 1', '1/n', '(n − 1)']), ('cp1', '(n + 2)!/n!', '(n + 2)(n + 1)', ['n + 2', '2', '(n + 2)!']),
            ('honors', 'C(n, 2)', 'n(n − 1)/2', ['n(n − 1)', 'n²/2', '(n − 1)/2']), ('honors', 'C(n, 1) + C(n, n)', 'n + 1', ['2n', 'n', '2'])]
    for L, e, good, bad in SIMP:
        b.mc(3, L, 'Simplify %s (n a positive integer, n ≥ 2).' % e, good, bad, ['Write the factorials out and cancel.', '%s = %s' % (e, good)], 'factorial_simplify')
    b.sel(3, 'cp1', 'Which expressions equal C(9, 4)?', [('C(9, 5)', True), ('C(8, 3) + C(8, 4)', True), ('9!/(4!·5!)', True), ('9·8·7·6', False), ('C(9, 3)', False)],
          ['Symmetry C(n, r) = C(n, n − r); Pascal\'s rule C(n, r) = C(n − 1, r − 1) + C(n − 1, r).', 'All equal 126; 9·8·7·6 = 3024 and C(9, 3) = 84.'], 'binom_select')
    b.sel(3, 'cp2', 'Which values equal 1?', [('0!', True), ('1!', True), ('C(5, 0)', True), ('C(5, 1)', False), ('2!', False)], ['0! = 1! = 1 and C(n, 0) = 1; C(5, 1) = 5, 2! = 2.'], 'binom_select')
    b.sel(3, 'honors', 'Which statements are true for every integer n ≥ 1?', [('Σ_{r=0}^{n} C(n, r) = 2ⁿ', True), ('C(2n, n) is even', True), ('n! ≥ 2ⁿ⁻¹', True), ('C(n, 2) = n²/2', False), ('(2n)! = 2·n!', False)],
          ['Sum of a row of Pascal\'s triangle is 2ⁿ; C(2n, n) = 2C(2n − 1, n − 1); n! ≥ 2ⁿ⁻¹ by induction.', 'C(n, 2) = n(n − 1)/2; (2n)! is much larger than 2·n!.'], 'binom_select')
    b.orq(3, 'cp2', 'Use Pascal\'s triangle.',
          [('Write row 4 (starting row 0 = 1).', '1, 4, 6, 4, 1'), ('Write row 5.', '1, 5, 10, 10, 5, 1'), ('What is C(5, 2)?', '10'), ('What is the sum of row 5?', '32')],
          ['Each entry is the sum of the two above.', 'Add neighbors in row 4.', 'Third entry of row 5.', '2⁵.'], 'pascal_or')
    b.orq(3, 'cp1', 'Binomial theorem: (x + y)ⁿ = Σ C(n, k) xⁿ⁻ᵏ yᵏ.',
          [('Expand (x + y)³.', 'x³ + 3x²y + 3xy² + y³'), ('Find the coefficient of x²y³ in (x + y)⁵.', '10'), ('Find the coefficient of x³ in (x + 2)⁵.', '40'), ('Find the sum of the coefficients of (x + y)⁶.', '64')],
          ['Row 3: 1, 3, 3, 1.', 'C(5, 3).', 'C(5, 3)·2² = 10·4.', 'Set x = y = 1.'], 'binomial_or')
    b.orq(3, 'honors', 'Prove Pascal\'s rule C(n, r) = C(n − 1, r − 1) + C(n − 1, r) for 1 ≤ r ≤ n − 1.',
          [('Write C(n − 1, r − 1) with factorials.', '(n − 1)!/((r − 1)!(n − r)!)'), ('Write C(n − 1, r) with factorials.', '(n − 1)!/(r!(n − 1 − r)!)'),
           ('Use the common denominator r!(n − r)! and add.', '(n − 1)!(r + (n − r))/(r!(n − r)!)'), ('Finish the proof.', '= n!/(r!(n − r)!) = C(n, r)')],
          ['Definition.', 'Definition.', 'Multiply by r/r and (n − r)/(n − r).', 'n(n − 1)! = n!.'], 'pascal_proof_or')


# ---------------------------------------------------------------- 4. Fibonacci
FIB = [1, 1]
while len(FIB) < 40:
    FIB.append(FIB[-1] + FIB[-2])
F = lambda n: FIB[n - 1]  # F_1 = F_2 = 1


def s4(b):
    for n, L in ((7, 'cp2'), (10, 'cp2'), (12, 'cp1'), (15, 'cp1'), (20, 'honors')):
        b.sa(4, L, 'With F₁ = 1, F₂ = 1 and F_n = F_(n−1) + F_(n−2), find F_%d.' % n, F(n),
             ['Generate terms: ' + ', '.join(str(F(k)) for k in range(1, n + 1)) + '.', 'F_%d = %d' % (n, F(n))], 'fib_term')
    ID = [('cp2', 'F₁ + F₂ + ... + F₆', sum(F(k) for k in range(1, 7)), 'Add 1 + 1 + 2 + 3 + 5 + 8.'),
          ('cp1', 'F₁ + F₂ + ... + F₁₀', sum(F(k) for k in range(1, 11)), 'Identity: the sum equals F₁₂ − 1.'),
          ('cp1', 'F₈² − F₇·F₉', F(8) ** 2 - F(7) * F(9), "Cassini's identity: F_n² − F_(n−1)F_(n+1) = (−1)ⁿ⁻¹."),
          ('honors', 'F₁² + F₂² + ... + F₈²', sum(F(k) ** 2 for k in range(1, 9)), 'Identity: the sum equals F₈ · F₉.'),
          ('honors', 'F₁ + F₃ + F₅ + ... + F₁₅ (odd indices)', sum(F(k) for k in range(1, 16, 2)), 'Identity: the sum of odd-indexed terms equals F₁₆.')]
    for L, t, v, why in ID:
        b.sa(4, L, 'Compute %s (F₁ = F₂ = 1).' % t, v, [why, 'Value: %d' % v], 'fib_identity')
    b.mc(4, 'cp2', 'Which list starts the Fibonacci sequence (F₁ = F₂ = 1)?', '1, 1, 2, 3, 5, 8, 13', ['1, 2, 3, 4, 5, 6, 7', '1, 1, 2, 4, 8, 16, 32', '1, 2, 4, 7, 11, 16, 22'],
         ['Each term is the sum of the two before it.'], 'fib_identify')
    b.mc(4, 'cp1', 'Rabbit pairs: each month every adult pair produces one new pair, and new pairs become adults after one month. Starting with one newborn pair, how many pairs are there in month 8?', str(F(8)),
         [str(F(7)), str(F(9)), '16'], ['The monthly counts follow F_n: 1, 1, 2, 3, 5, 8, 13, 21.', 'Month 8: 21 pairs.'], 'fib_context', order='sort')
    b.mc(4, 'honors', 'The number of ways to climb n stairs taking 1 or 2 steps at a time satisfies s_n = s_(n−1) + s_(n−2) with s₁ = 1, s₂ = 2. How many ways are there to climb 10 stairs?', str(F(11)),
         [str(F(10)), str(F(12)), str(2 ** 9)], ['s_n = F_(n+1).', 's₁₀ = F₁₁ = 89.'], 'fib_context', order='sort')
    b.mc(4, 'cp1', 'Which ratio F₁₃/F₁₂ is closest to?', 'The golden ratio, about 1.618', ['2', '1.5', '√2, about 1.414'],
         ['F₁₃/F₁₂ = 233/144 ≈ 1.6181.', 'Ratios of consecutive Fibonacci numbers approach φ = (1 + √5)/2.'], 'fib_ratio')
    b.mc(4, 'honors', 'Which statement about Fibonacci numbers is true for every n ≥ 1?', 'F_n and F_(n+1) are relatively prime', ['F_n is odd', 'F_(n+1) = 2F_n', 'F_n < n²'],
         ['Any common divisor of F_(n+1) and F_n also divides F_(n+1) − F_n = F_(n−1); repeat down to F₁ = 1.', 'F₃ = 2 is even; F₃ ≠ 2F₂ fails at n = 3; F₁₃ = 233 > 169.'], 'fib_fact')
    b.sel(4, 'cp2', 'Which numbers are Fibonacci numbers?', [('21', True), ('34', True), ('40', False), ('55', True), ('60', False)], ['1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, ...'], 'fib_select')
    b.sel(4, 'cp1', 'Which Fibonacci numbers are even (F₁ = F₂ = 1)?', [('F₃', True), ('F₆', True), ('F₉', True), ('F₇', False), ('F₁₀', False)],
          ['F_n is even exactly when 3 | n: F₃ = 2, F₆ = 8, F₉ = 34; F₇ = 13 and F₁₀ = 55 are odd.'], 'fib_select')
    b.sel(4, 'honors', 'Which identities hold for all n ≥ 1 (F₁ = F₂ = 1)?', [('F₁ + ... + F_n = F_(n+2) − 1', True), ('F_(n+2) = F_(n+1) + F_n', True), ('F₂ + F₄ + ... + F_(2n) = F_(2n+1) − 1', True),
                                                                             ('F_(2n) = 2F_n', False), ('F_n² = F_(2n)', False)],
          ['Check small cases and prove by induction; F₄ = 3 ≠ 2F₂ = 2 and F₂² = 1 ≠ F₄ = 3.'], 'fib_select')
    b.orq(4, 'cp2', 'Fibonacci numbers: F₁ = 1, F₂ = 1, F_n = F_(n−1) + F_(n−2).',
          [('List F₁ through F₈.', '1, 1, 2, 3, 5, 8, 13, 21'), ('Find F₁ + ... + F₆.', '20'), ('Compare your answer with F₈.', 'The sum is F₈ − 1 = 20.'), ('Predict F₁ + ... + F₇ using the pattern.', 'F₉ − 1 = 33')],
          ['Add the previous two.', '1+1+2+3+5+8.', 'F₈ = 21.', 'F₉ = 34.'], 'fib_or')
    b.orq(4, 'cp1', 'Tiling: let t_n be the number of ways to tile a 1 × n strip with 1 × 1 squares and 1 × 2 dominoes.',
          [('Find t₁, t₂, t₃.', '1, 2, 3'), ('Explain why t_n = t_(n−1) + t_(n−2).', 'The last tile is a square (leaving n − 1) or a domino (leaving n − 2).'), ('Find t₈.', '34'), ('Relate t_n to Fibonacci numbers.', 't_n = F_(n+1)')],
          ['List tilings.', 'Case on the last tile.', '1, 2, 3, 5, 8, 13, 21, 34.', 'Shifted by one.'], 'fib_or')
    b.orq(4, 'honors', 'Prove by strong induction that F_n < 2ⁿ for all n ≥ 1.',
          [('Check the base cases n = 1 and n = 2.', '1 < 2 and 1 < 4'), ('State the inductive hypothesis.', 'F_j < 2ʲ for all j with 1 ≤ j ≤ k, where k ≥ 2.'),
           ('Show F_(k+1) < 2ᵏ⁺¹.', 'F_(k+1) = F_k + F_(k−1) < 2ᵏ + 2ᵏ⁻¹ < 2ᵏ + 2ᵏ = 2ᵏ⁺¹'), ('Why are two base cases needed?', 'The recursion uses the two previous terms, so the step from k to k + 1 needs k ≥ 2.')],
          ['Direct check.', 'Strong hypothesis.', 'Bound each term.', 'The first application of the step needs F₁ and F₂.'], 'fib_proof_or')


# ---------------------------------------------------------------- 5. recursively defined sequences
REC = [('a₁ = 4, a_n = a_(n−1) + 3', lambda a, n: a + 3, 4, 1, 'cp2'), ('a₁ = 2, a_n = 3a_(n−1)', lambda a, n: 3 * a, 2, 1, 'cp2'), ('a₀ = 1, a_n = 2a_(n−1) + 1', lambda a, n: 2 * a + 1, 1, 0, 'cp1'),
       ('a₁ = 1, a_n = a_(n−1) + n', lambda a, n: a + n, 1, 1, 'cp1'), ('a₁ = 1, a_n = n · a_(n−1)', lambda a, n: n * a, 1, 1, 'cp1'), ('a₀ = 2, a_n = a_(n−1)² − 1', lambda a, n: a * a - 1, 2, 0, 'honors'),
       ('a₁ = 3, a_n = 2a_(n−1) − n', lambda a, n: 2 * a - n, 3, 1, 'honors')]


def run(f, a0, start, count):
    out, a = [a0], a0
    for n in range(start + 1, start + count):
        a = f(a, n)
        out.append(a)
    return out


def s5(b):
    for disp, f, a0, st, L in REC:
        t = run(f, a0, st, 5)
        b.sa(5, L, 'Find the first five terms of the recursively defined sequence %s (for n ≥ %d). Separate terms with commas.' % (disp, st + 1), lst(t),
             ['Start with the initial term and apply the recurrence repeatedly.', 'Terms: ' + lst(t)], 'rec_terms')
    TOREC = [('cp2', '5, 9, 13, 17, ...', 'a₁ = 5, a_n = a_(n−1) + 4', ['a₁ = 5, a_n = 4a_(n−1)', 'a₁ = 4, a_n = a_(n−1) + 5', 'a₁ = 5, a_n = a_(n−1) + 5']),
             ('cp2', '3, 6, 12, 24, ...', 'a₁ = 3, a_n = 2a_(n−1)', ['a₁ = 3, a_n = a_(n−1) + 3', 'a₁ = 2, a_n = 3a_(n−1)', 'a₁ = 3, a_n = a_(n−1) + 2']),
             ('cp1', '1, 3, 7, 15, 31, ...', 'a₁ = 1, a_n = 2a_(n−1) + 1', ['a₁ = 1, a_n = a_(n−1) + 2', 'a₁ = 1, a_n = 3a_(n−1)', 'a₁ = 1, a_n = 2a_(n−1) − 1']),
             ('cp1', '2, 5, 11, 23, ...', 'a₁ = 2, a_n = 2a_(n−1) + 1', ['a₁ = 2, a_n = a_(n−1) + 3', 'a₁ = 2, a_n = 3a_(n−1) − 1', 'a₁ = 2, a_n = 2a_(n−1) + 3']),
             ('honors', '1, 2, 6, 24, 120, ...', 'a₁ = 1, a_n = n · a_(n−1)', ['a₁ = 1, a_n = a_(n−1) + n', 'a₁ = 1, a_n = 2a_(n−1) + 2', 'a₁ = 1, a_n = (n − 1)a_(n−1)']),
             ('honors', '1, 1, 3, 5, 11, 21, ...', 'a₁ = a₂ = 1, a_n = a_(n−1) + 2a_(n−2)', ['a₁ = a₂ = 1, a_n = 2a_(n−1) + a_(n−2)', 'a₁ = a₂ = 1, a_n = a_(n−1) + a_(n−2)', 'a₁ = 1, a_n = 2a_(n−1) + 1'])]
    for L, t, good, bad in TOREC:
        b.mc(5, L, 'Which recursive definition generates %s?' % t, good, bad, ['Generate terms from each choice and compare.', good], 'find_recursion')
    b.sel(5, 'cp1', 'For a₁ = 2, a_n = a_(n−1) + 2n, which statements are true?', [('a₂ = 6', True), ('a₃ = 12', True), ('a₄ = 20', True), ('a₅ = 28', False), ('a_n = 2n', False)],
          ['Terms: 2, 6, 12, 20, 30 (a_n = n(n + 1)).'], 'rec_select')
    b.sel(5, 'cp2', 'For a₁ = 10, a_n = a_(n−1) − 3, which numbers are terms?', [('7', True), ('1', True), ('−5', True), ('0', False), ('−6', False)],
          ['Terms: 10, 7, 4, 1, −2, −5, −8, ...: numbers of the form 13 − 3n.'], 'rec_select')
    b.sel(5, 'honors', 'Which sequences satisfy a_n = 5a_(n−1) − 6a_(n−2) for all n ≥ 2?', [('a_n = 2ⁿ', True), ('a_n = 3ⁿ', True), ('a_n = 2ⁿ + 3ⁿ', True), ('a_n = 5ⁿ', False), ('a_n = 6ⁿ', False)],
          ['The characteristic equation x² = 5x − 6 has roots 2 and 3; any combination A·2ⁿ + B·3ⁿ works.'], 'rec_select')
    b.orq(5, 'cp2', 'A savings account starts with $100 and gains $15 each month: s₀ = 100, s_n = s_(n−1) + 15.',
          [('Find s₁, s₂, s₃.', '115, 130, 145'), ('Write an explicit formula.', 's_n = 100 + 15n'), ('Find s₁₂.', '280'), ('After how many months does it first exceed $400?', '21')],
          ['Add 15.', 'Arithmetic.', '100 + 180.', '100 + 15n > 400 gives n > 20.'], 'rec_or')
    b.orq(5, 'cp1', 'A population model: p₀ = 1000, p_n = 1.1 p_(n−1) − 50.',
          [('Find p₁ and p₂.', '1050, 1105'), ('Find p₃.', '1165.5'), ('What does the −50 represent?', 'A fixed number removed each period.'), ('Find the value P with P = 1.1P − 50 (a fixed point).', '500')],
          ['Apply the recurrence.', '1.1·1105 − 50.', 'Interpret.', '0.1P = 50.'], 'rec_or')
    b.orq(5, 'honors', 'Let a₀ = 2, a₁ = 5, a_n = 5a_(n−1) − 6a_(n−2).',
          [('Find a₂ and a₃.', '13, 35'), ('Show that a_n = 2ⁿ + 3ⁿ matches a₀ through a₃.', '2, 5, 13, 35'),
           ('Verify algebraically that 2ⁿ + 3ⁿ satisfies the recurrence.', '5(2ⁿ⁻¹ + 3ⁿ⁻¹) − 6(2ⁿ⁻² + 3ⁿ⁻²) = 2ⁿ⁻²(10 − 6) + 3ⁿ⁻²(15 − 6) = 2ⁿ + 3ⁿ'), ('Find a₁₀.', str(2 ** 10 + 3 ** 10))],
          ['Compute.', 'Substitute.', 'Factor powers.', '1024 + 59049.'], 'rec_or')


# ---------------------------------------------------------------- 6. iteration
def s6(b):
    IT = [('cp2', 'a₁ = 7, a_n = a_(n−1) + 4', 'a_n = 4n + 3', ['a_n = 7n + 4', 'a_n = 4n + 7', 'a_n = 7 + 4n²'], lambda n: 4 * n + 3, 7, lambda a, n: a + 4, 1),
          ('cp2', 'a₀ = 5, a_n = 2a_(n−1)', 'a_n = 5·2ⁿ', ['a_n = 2·5ⁿ', 'a_n = 5 + 2n', 'a_n = 10ⁿ'], lambda n: 5 * 2 ** n, 5, lambda a, n: 2 * a, 0),
          ('cp1', 'a₀ = 0, a_n = a_(n−1) + 2n − 1', 'a_n = n²', ['a_n = 2n − 1', 'a_n = n² − 1', 'a_n = n(n − 1)'], lambda n: n * n, 0, lambda a, n: a + 2 * n - 1, 0),
          ('cp1', 'a₁ = 1, a_n = 2a_(n−1) + 1', 'a_n = 2ⁿ − 1', ['a_n = 2ⁿ + 1', 'a_n = 2n − 1', 'a_n = 2ⁿ⁻¹'], lambda n: 2 ** n - 1, 1, lambda a, n: 2 * a + 1, 1),
          ('honors', 'a₀ = 1, a_n = 3a_(n−1) + 2', 'a_n = 2·3ⁿ − 1', ['a_n = 3ⁿ + 2', 'a_n = 3ⁿ⁺¹ − 2', 'a_n = 2·3ⁿ + 1'], lambda n: 2 * 3 ** n - 1, 1, lambda a, n: 3 * a + 2, 0),
          ('honors', 'a₁ = 1, a_n = a_(n−1) + n²', 'a_n = n(n + 1)(2n + 1)/6', ['a_n = n³', 'a_n = n²(n + 1)/2', 'a_n = (n(n + 1)/2)²'], lambda n: n * (n + 1) * (2 * n + 1) // 6, 1, lambda a, n: a + n * n, 1)]
    for L, rec, good, bad, f, a0, g, st in IT:
        seq = run(g, a0, st, 8)
        assert seq == [f(n) for n in range(st, st + 8)], rec
        b.mc(6, L, 'Use iteration to find an explicit formula for %s.' % rec, good, bad,
             ['Iterate: ' + lst(seq[:5]) + ', ...', 'The pattern is %s; check it against the terms.' % good], 'iterate_formula')
    HAN = [(3, 'cp2'), (5, 'cp1'), (10, 'honors')]
    for n, L in HAN:
        m = run(lambda a, k: 2 * a + 1, 1, 1, n)[-1]
        b.sa(6, L, 'Tower of Hanoi: m₁ = 1 and m_k = 2m_(k−1) + 1 moves for k disks. How many moves are needed for %d disks?' % n, m,
             ['Iterate the recurrence or use m_k = 2ᵏ − 1.', 'm_%d = %d' % (n, m)], 'hanoi')
    COMP = [('cp2', 'Use the recurrence a_n = a_(n−1) + 6 with a₁ = 2 to compute a₆.', run(lambda a, n: a + 6, 2, 1, 6)[-1]),
            ('cp1', 'A recursive algorithm does T(n) = T(n − 1) + n steps with T(1) = 1. Find T(20).', run(lambda a, n: a + n, 1, 1, 20)[-1]),
            ('honors', 'T(n) = 2T(n/2) + n with T(1) = 0, for n a power of 2. Find T(16).', 64),
            ('cp1', 'Compound interest: b₀ = 1000 and b_n = 1.05·b_(n−1). Find b₃ rounded to the nearest cent (write like 1234.56).', '%.2f' % (1000 * 1.05 ** 3)),
            ('honors', 'Iterate a_n = −a_(n−1) + 2 with a₀ = 5. Find a₁₀₁.', run(lambda a, n: -a + 2, 5, 0, 102)[-1])]
    t16 = 0
    for k in range(1, 5):
        t16 = 2 * t16 + 2 ** k
    assert t16 == 64
    for L, t, v in COMP:
        b.sa(6, L, t, v, ['Apply the recurrence step by step (or find the pattern by iteration).', 'Answer: %s' % v], 'rec_compute')
    b.sel(6, 'cp1', 'Iterating a_n = a_(n−1) + 5 with a₀ = 3 gives a_n = ___. Which expressions are correct for every n ≥ 0?', [('3 + 5n', True), ('5n + 3', True), ('a₀ + 5n', True), ('8n', False), ('3·5ⁿ', False)],
          ['Each step adds 5, so after n steps a_n = 3 + 5n.'], 'iterate_select')
    b.sel(6, 'honors', 'For T(n) = T(n − 1) + 2n with T(0) = 0, which statements are true?', [('T(n) = n(n + 1)', True), ('T(5) = 30', True), ('T(n) = 2(1 + 2 + ... + n)', True), ('T(n) = 2ⁿ', False), ('T(n) = n² + 1', False)],
          ['Iterating gives T(n) = 2(1 + ... + n) = n(n + 1).'], 'iterate_select')
    b.sel(6, 'cp2', 'For a₁ = 1, a_n = a_(n−1) + 2, which values appear in the sequence?', [('5', True), ('11', True), ('15', True), ('8', False), ('20', False)], ['The terms are the odd numbers 1, 3, 5, 7, ...'], 'iterate_select')
    b.orq(6, 'cp1', 'Iterate a₀ = 2, a_n = 3a_(n−1) − 2.',
          [('Find a₁ through a₄.', '4, 10, 28, 82'), ('Compare each term with a power of 3.', 'a_n − 1 = 3ⁿ'), ('Guess an explicit formula.', 'a_n = 3ⁿ + 1'),
           ('Check the formula in the recurrence.', '3(3ⁿ⁻¹ + 1) − 2 = 3ⁿ + 1')],
          ['Compute.', '1, 3, 9, 27, 81.', 'Pattern.', 'Substitute.'], 'iterate_or')
    b.orq(6, 'cp2', 'Iterate a₁ = 10, a_n = a_(n−1) − 2.',
          [('Find a₂, a₃, a₄.', '8, 6, 4'), ('How much does each step change the value?', 'It decreases by 2.'), ('Write an explicit formula.', 'a_n = 12 − 2n'), ('Find a₂₀.', '−28')],
          ['Subtract 2.', 'Common difference −2.', 'a_n = 10 − 2(n − 1).', '12 − 40.'], 'iterate_or')
    b.orq(6, 'honors', 'Iterate T(n) = 2T(n − 1) + 3 with T(0) = 1.',
          [('Write T(n) in terms of T(n − 2).', 'T(n) = 4T(n − 2) + 6 + 3'), ('Write T(n) in terms of T(n − k).', 'T(n) = 2ᵏT(n − k) + 3(2ᵏ − 1)'),
           ('Set k = n to find an explicit formula.', 'T(n) = 2ⁿ + 3(2ⁿ − 1) = 4·2ⁿ − 3'), ('Check T(3) both ways.', 'Recurrence: 1, 5, 13, 29; formula 32 − 3 = 29')],
          ['Substitute once.', 'Geometric sum 3(1 + 2 + ... + 2ᵏ⁻¹).', 'T(0) = 1.', 'Both give 29.'], 'iterate_or')


# ---------------------------------------------------------------- 7. principle of induction
PS = [  # (statement, P(k+1) goal, base case, P(k), a plausible wrong goal)
    ('1 + 2 + ... + n = n(n + 1)/2', '1 + 2 + ... + k + (k + 1) = (k + 1)(k + 2)/2', 'n = 1: 1 = 1(2)/2', '1 + 2 + ... + k = k(k + 1)/2', '1 + 2 + ... + k + (k + 1) = k(k + 1)/2 + 1'),
    ('1 + 3 + 5 + ... + (2n − 1) = n²', '1 + 3 + ... + (2k − 1) + (2k + 1) = (k + 1)²', 'n = 1: 1 = 1²', '1 + 3 + ... + (2k − 1) = k²', '1 + 3 + ... + (2k − 1) + (2k + 1) = k² + 1'),
    ('2ⁿ > n for all n ≥ 1', '2ᵏ⁺¹ > k + 1', 'n = 1: 2 > 1', '2ᵏ > k', '2ᵏ + 1 > k + 1'),
    ('3 | (n³ − n) for all n ≥ 0', '3 | ((k + 1)³ − (k + 1))', 'n = 0: 3 | 0', '3 | (k³ − k)', '3 | (k³ − k + 1)'),
    ('n! > 2ⁿ for all n ≥ 4', '(k + 1)! > 2ᵏ⁺¹', 'n = 4: 24 > 16', 'k! > 2ᵏ', 'k! + 1 > 2ᵏ + 1'),
    ('1 + 2 + 4 + ... + 2ⁿ = 2ⁿ⁺¹ − 1 for n ≥ 0', '1 + 2 + ... + 2ᵏ + 2ᵏ⁺¹ = 2ᵏ⁺² − 1', 'n = 0: 1 = 2 − 1', '1 + 2 + ... + 2ᵏ = 2ᵏ⁺¹ − 1', '1 + 2 + ... + 2ᵏ + 2ᵏ⁺¹ = 2ᵏ⁺¹ − 1')]


def s7(b):
    for L, idx in (('cp2', [0, 1]), ('cp1', [2, 3]), ('honors', [4, 5])):
        for i in idx:
            st, pk1, base, pk, wrong = PS[i]
            b.mc(7, L, 'In an induction proof of "%s", what must be shown in the inductive step (assuming P(k))?' % st, pk1,
                 [pk, wrong, base],
                 ['The inductive step proves P(k) → P(k + 1): replace n by k + 1 in the statement.', 'Show: ' + pk1], 'induction_step_goal')
            b.mc(7, L, 'What is the base case for an induction proof of "%s"?' % st, base,
                 ['n = 2', 'n = k', 'n = k + 1'] if not base.startswith('n = 0') else ['n = 1: 3 | 0', 'n = k', 'n = 2: 3 | 6'],
                 ['The base case checks the smallest value of n in the statement.', base], 'induction_base')
    HYP = [('cp2', '1 + 2 + ... + n = n(n + 1)/2', '1 + 2 + ... + k = k(k + 1)/2 for some integer k ≥ 1'),
           ('cp1', '5 | (6ⁿ − 1) for all n ≥ 0', '5 | (6ᵏ − 1) for some integer k ≥ 0'),
           ('honors', 'n² ≥ 2n + 3 for all n ≥ 3', 'k² ≥ 2k + 3 for some integer k ≥ 3')]
    for L, st, h in HYP:
        b.sa(7, L, 'Write the inductive hypothesis for a proof of "%s".' % st, 'Assume ' + h + '.', ['The inductive hypothesis assumes P(k) for an arbitrary k at least the base value.', 'Assume ' + h + '.'], 'induction_hypothesis',
             notes='Hand-authored; matches the standard textbook wording of P(k).')
    DOM = [('cp2', 'An induction proof shows P(1) and that P(k) → P(k + 1) for all k ≥ 1. For which n is P(n) proved?', 'All integers n ≥ 1', ['Only n = 1', 'Only n = 1 and n = 2', 'All integers n']),
           ('cp1', 'A proof shows P(3) and P(k) → P(k + 1) for all k ≥ 3. For which n is P(n) proved?', 'All integers n ≥ 3', ['All integers n ≥ 1', 'Only n = 3', 'All integers n ≥ 4']),
           ('honors', 'A proof shows P(1) and P(k) → P(k + 2) for all k ≥ 1. For which n is P(n) proved?', 'All odd positive integers n', ['All positive integers n', 'All even positive integers n', 'Only n = 1 and n = 3'])]
    for L, t, good, bad in DOM:
        b.mc(7, L, t, good, bad, ['Dominoes: the base case starts the chain and each step reaches the next case covered by the step.', good], 'induction_domain')
    b.sel(7, 'cp1', 'Which are required parts of a proof by mathematical induction of "P(n) for all n ≥ 1"?',
          [('Show P(1) is true.', True), ('Assume P(k) for an arbitrary k ≥ 1.', True), ('Show P(k + 1) follows from P(k).', True), ('Check P(2), P(3) and P(4).', False), ('Assume P(k + 1) and show P(k).', False)],
          ['Base case plus inductive step; extra examples are not required, and the step goes forward.'], 'induction_select')
    b.sel(7, 'cp2', 'Which describe the "domino" idea of induction?', [('The first domino falls (base case).', True), ('Each domino knocks over the next (inductive step).', True), ('Then all dominoes fall.', True),
                                                                      ('Only the first few dominoes fall.', False), ('You must push every domino by hand.', False)], ['Base case + inductive step ⇒ every case.'], 'induction_select')
    b.sel(7, 'honors', 'Which situations call for STRONG induction (assuming P(1), ..., P(k) to prove P(k + 1))?',
          [('Every integer n ≥ 2 is a product of primes.', True), ('A recurrence that uses the two previous terms, such as a_n = a_(n−1) + a_(n−2).', True), ('Every amount of postage ≥ 12 cents can be made with 4- and 5-cent stamps.', True),
           ('1 + 2 + ... + n = n(n + 1)/2', False), ('2ⁿ > n', False)],
          ['Strong induction is natural when P(k + 1) depends on cases earlier than P(k).'], 'induction_select')
    b.orq(7, 'cp2', 'Plan an induction proof of "2 + 4 + ... + 2n = n(n + 1) for all n ≥ 1".',
          [('Check the base case.', 'n = 1: 2 = 1·2'), ('Write the inductive hypothesis.', 'Assume 2 + 4 + ... + 2k = k(k + 1).'),
           ('Write what you must show.', '2 + 4 + ... + 2k + 2(k + 1) = (k + 1)(k + 2)'), ('Use the hypothesis to finish.', 'k(k + 1) + 2(k + 1) = (k + 1)(k + 2)')],
          ['Smallest n.', 'P(k).', 'P(k + 1).', 'Factor out k + 1.'], 'induction_plan_or')
    b.orq(7, 'cp1', 'Claim: "n² + n is even for all n ≥ 1."',
          [('Check the base case.', '1 + 1 = 2 is even'), ('State P(k) and P(k + 1).', 'P(k): k² + k is even. P(k + 1): (k + 1)² + (k + 1) is even.'),
           ('Rewrite (k + 1)² + (k + 1) in terms of k² + k.', '(k² + k) + 2(k + 1)'), ('Conclude.', 'Even + even is even, so P(k + 1) holds; by induction the claim is true.')],
          ['Direct.', 'Replace n.', 'Expand: k² + 3k + 2.', 'Sum of evens.'], 'induction_plan_or')
    b.orq(7, 'honors', 'A flawed "proof" claims all horses are the same color. Step: from a set of k + 1 horses remove horse A (the rest match by P(k)), then remove horse B (the rest match), so all k + 1 match.',
          [('Which base case is used?', 'n = 1: one horse has one color.'), ('For which k does the inductive step fail?', 'k = 1 (going from 1 to 2 horses)'),
           ('Why does it fail there?', 'With 2 horses the two smaller sets {A} and {B} do not overlap, so no common horse links the colors.'), ('What lesson does this teach?', 'The inductive step must work for EVERY k ≥ the base value.')],
          ['Trivial.', 'Check k = 1.', 'The argument needs an overlapping horse.', 'Check the step for the smallest k.'], 'horses_or')


# ---------------------------------------------------------------- 8. writing inductive proofs
def s8(b):
    ALG = [('cp2', '1 + 2 + ... + n = n(n + 1)/2', 'k(k + 1)/2 + (k + 1)', '(k + 1)(k + 2)/2', ['k(k + 1)/2 + k', '(k + 1)(k + 1)/2', 'k(k + 2)/2']),
           ('cp1', '1 + 3 + ... + (2n − 1) = n²', 'k² + (2k + 1)', '(k + 1)²', ['k² + 2k', 'k² + 1', '(2k + 1)²']),
           ('cp1', '1² + 2² + ... + n² = n(n + 1)(2n + 1)/6', 'k(k + 1)(2k + 1)/6 + (k + 1)²', '(k + 1)(k + 2)(2k + 3)/6', ['(k + 1)(k + 2)(2k + 1)/6', 'k(k + 1)(2k + 3)/6', '(k + 1)²(2k + 1)/6']),
           ('honors', '1·2 + 2·3 + ... + n(n + 1) = n(n + 1)(n + 2)/3', 'k(k + 1)(k + 2)/3 + (k + 1)(k + 2)', '(k + 1)(k + 2)(k + 3)/3', ['(k + 1)(k + 2)(k + 2)/3', 'k(k + 1)(k + 3)/3', '(k + 1)²(k + 2)/3']),
           ('honors', '1/(1·2) + 1/(2·3) + ... + 1/(n(n + 1)) = n/(n + 1)', 'k/(k + 1) + 1/((k + 1)(k + 2))', '(k + 1)/(k + 2)', ['k/(k + 2)', '(k + 1)/(k + 1)', '(k + 2)/(k + 3)'])]
    for L, st, step, res, bad in ALG:
        b.mc(8, L, 'Inductive step for "%s": after using the hypothesis, the left side of P(k + 1) equals %s. This simplifies to ...' % (st, step), res, bad,
             ['Factor out the common factor and simplify.', '%s = %s, which is the right side of P(k + 1).' % (step, res)], 'induction_algebra')
    DIVI = [('cp1', '4 | (5ⁿ − 1)', '5ᵏ⁺¹ − 1 = 5(5ᵏ − 1) + 4', ['5ᵏ⁺¹ − 1 = 5(5ᵏ − 1)', '5ᵏ⁺¹ − 1 = (5ᵏ − 1) + 5', '5ᵏ⁺¹ − 1 = 5ᵏ − 1 + 4']),
            ('cp1', '3 | (4ⁿ − 1)', '4ᵏ⁺¹ − 1 = 4(4ᵏ − 1) + 3', ['4ᵏ⁺¹ − 1 = 4(4ᵏ − 1) + 4', '4ᵏ⁺¹ − 1 = 3(4ᵏ − 1)', '4ᵏ⁺¹ − 1 = 4ᵏ − 1 + 3']),
            ('honors', '6 | (n³ − n)', '(k + 1)³ − (k + 1) = (k³ − k) + 3k(k + 1)', ['(k + 1)³ − (k + 1) = (k³ − k) + 3k', '(k + 1)³ − (k + 1) = k³ − k + 1', '(k + 1)³ − (k + 1) = (k³ − k) + 6k']),
            ('honors', '7 | (2³ⁿ − 1)', '2³ᵏ⁺³ − 1 = 8(2³ᵏ − 1) + 7', ['2³ᵏ⁺³ − 1 = 8(2³ᵏ − 1)', '2³ᵏ⁺³ − 1 = 2³ᵏ − 1 + 7', '2³ᵏ⁺³ − 1 = 3(2³ᵏ − 1) + 7'])]
    chk = {'5': lambda k: 5 ** (k + 1) - 1 == 5 * (5 ** k - 1) + 4, '4': lambda k: 4 ** (k + 1) - 1 == 4 * (4 ** k - 1) + 3, '6': lambda k: (k + 1) ** 3 - (k + 1) == (k ** 3 - k) + 3 * k * (k + 1),
           '7': lambda k: 2 ** (3 * k + 3) - 1 == 8 * (2 ** (3 * k) - 1) + 7}
    assert all(all(f(k) for k in range(8)) for f in chk.values())
    for L, st, good, bad in DIVI:
        b.mc(8, L, 'Divisibility induction for "%s": which rewriting of the (k + 1) case lets you use the inductive hypothesis?' % st, good, bad,
             ['Write the new expression as (a multiple of the old expression) + (a multiple of the divisor).', good + '. Both pieces are divisible, so the sum is.' if st.startswith(('4', '3', '7')) else good + '; k(k + 1) is even, so 3k(k + 1) is divisible by 6.'], 'induction_divisibility')
    INEQ = [('cp2', '2ⁿ ≥ n + 1 for n ≥ 0', '2ᵏ⁺¹ = 2·2ᵏ ≥ 2(k + 1) = 2k + 2 ≥ k + 2'),
            ('cp1', '3ⁿ ≥ 2n + 1 for n ≥ 0', '3ᵏ⁺¹ = 3·3ᵏ ≥ 3(2k + 1) = 6k + 3 ≥ 2k + 3'),
            ('honors', 'n! ≥ 2ⁿ for n ≥ 4', '(k + 1)! = (k + 1)k! ≥ (k + 1)2ᵏ ≥ 2·2ᵏ = 2ᵏ⁺¹')]
    for L, st, chain in INEQ:
        b.sa(8, L, 'For the inductive step of "%s", what is the LAST expression in the chain that proves P(k + 1)? (Chain shown with the last step hidden: %s ≥ ?)' % (st, chain.rsplit(' ≥ ', 1)[0]),
             chain.rsplit(' ≥ ', 1)[1], ['Full chain: ' + chain + '.', 'This is the right side of P(k + 1).'], 'induction_inequality')
    b.sel(8, 'cp1', 'In the inductive step of "1 + 2 + ... + n = n(n + 1)/2", which lines are correct?',
          [('1 + ... + k + (k + 1) = k(k + 1)/2 + (k + 1)', True), ('= (k + 1)(k/2 + 1)', True), ('= (k + 1)(k + 2)/2', True), ('= (k + 1)²/2', False), ('= k(k + 2)/2', False)],
          ['Substitute the hypothesis, then factor out k + 1.'], 'induction_lines_select')
    b.sel(8, 'cp2', 'Which statements about the base case are correct?', [('It checks the smallest n in the claim.', True), ('Without it, the proof is incomplete.', True), ('It is usually a quick calculation.', True),
                                                                        ('It replaces the inductive step.', False), ('It must use n = 0.', False)], ['The base case starts the chain; it is the smallest value claimed.'], 'induction_lines_select')
    b.sel(8, 'honors', 'Postage claim: every n ≥ 12 is 4a + 5b with a, b ≥ 0. Which facts make a strong-induction proof work?',
          [('Base cases 12 = 4·3, 13 = 4·2 + 5, 14 = 4 + 5·2, 15 = 5·3', True), ('For k ≥ 15, k + 1 = (k − 3) + 4', True), ('k − 3 ≥ 12 is covered by the hypothesis', True),
           ('One base case n = 12 is enough', False), ('k + 1 = k + 5 − 4', False)], ['Adding a 4-cent stamp to the case k − 3 needs four consecutive base cases.'], 'induction_lines_select')
    b.orq(8, 'cp1', 'Prove by induction: 1 + 2 + 2² + ... + 2ⁿ = 2ⁿ⁺¹ − 1 for n ≥ 0.',
          [('Base case.', 'n = 0: 1 = 2 − 1'), ('Inductive hypothesis.', 'Assume 1 + 2 + ... + 2ᵏ = 2ᵏ⁺¹ − 1.'),
           ('Inductive step computation.', '1 + ... + 2ᵏ + 2ᵏ⁺¹ = (2ᵏ⁺¹ − 1) + 2ᵏ⁺¹ = 2·2ᵏ⁺¹ − 1 = 2ᵏ⁺² − 1'), ('Conclusion.', 'P(k + 1) holds, so by induction the formula is true for all n ≥ 0.')],
          ['Check.', 'P(k).', 'Add the next term.', 'Principle of induction.'], 'induction_proof_or')
    b.orq(8, 'cp2', 'Prove by induction: 3 + 6 + 9 + ... + 3n = 3n(n + 1)/2.',
          [('Base case.', 'n = 1: 3 = 3·1·2/2'), ('Inductive hypothesis.', 'Assume 3 + ... + 3k = 3k(k + 1)/2.'),
           ('Add the next term and simplify.', '3k(k + 1)/2 + 3(k + 1) = 3(k + 1)(k + 2)/2'), ('Conclude.', 'P(k + 1) holds; by induction it is true for all n ≥ 1.')],
          ['Check.', 'P(k).', 'Factor 3(k + 1)/2.', 'Induction.'], 'induction_proof_or')
    b.orq(8, 'honors', 'Prove by induction: 5 | (n⁵ − n) for all n ≥ 0.',
          [('Base case.', 'n = 0: 5 | 0'), ('Expand (k + 1)⁵ − (k + 1).', 'k⁵ + 5k⁴ + 10k³ + 10k² + 5k + 1 − k − 1'),
           ('Group to use the hypothesis.', '(k⁵ − k) + 5(k⁴ + 2k³ + 2k² + k)'), ('Conclude.', 'Both parts are divisible by 5, so 5 | (k + 1)⁵ − (k + 1).')],
          ['Check.', 'Binomial expansion.', 'Separate k⁵ − k.', 'Sum of multiples of 5.'], 'induction_proof_or')


# ---------------------------------------------------------------- 9. patterns and tessellations
def s9(b):
    PAT = [('cp2', 'Square pattern: figure n is an n × n square of tiles. How many tiles are in figure 9?', 81),
           ('cp2', 'A row of n squares made of toothpicks uses 3n + 1 toothpicks. How many toothpicks for 12 squares?', 37),
           ('cp1', 'Triangular numbers T_n = n(n + 1)/2 count dots in a triangle with n rows. Find T₁₅.', 120),
           ('cp1', 'Pentagonal numbers P_n = n(3n − 1)/2. Find P₆.', 51),
           ('honors', 'A hexagonal tile pattern has 1 tile in ring 0 and 6k tiles in ring k. How many tiles fill rings 0 through 5?', 1 + sum(6 * k for k in range(1, 6))),
           ('honors', 'The number of diagonals of an n-gon is n(n − 3)/2. How many diagonals does a 12-gon have?', 54)]
    for L, t, v in PAT:
        b.sa(9, L, t, v, ['Substitute into the pattern rule.', 'Answer: %d' % v], 'figurate')
    ANG = [(5, 'cp2'), (6, 'cp2'), (8, 'cp1'), (12, 'cp1'), (20, 'honors')]
    for n, L in ANG:
        v = Fraction(180 * (n - 2), n)
        b.sa(9, L, 'Find the measure of each interior angle of a regular %d-gon, in degrees.' % n, frac(v), ['Interior angle sum (n − 2)·180°, divided by n.', '(%d − 2)·180/%d = %s°' % (n, n, frac(v))], 'interior_angle')
    b.mc(9, 'cp2', 'Which regular polygon CANNOT tile the plane by itself?', 'Regular pentagon', ['Equilateral triangle', 'Square', 'Regular hexagon'],
         ['A regular polygon tiles alone when its interior angle divides 360°.', 'Pentagon: 108° does not divide 360°.'], 'tessellate')
    b.mc(9, 'cp1', 'How many regular hexagons meet at each vertex of the regular hexagonal tessellation?', '3', ['4', '6', '2'], ['360° / 120° = 3.'], 'tessellate', order='sort')
    b.mc(9, 'honors', 'A semi-regular tessellation has, at every vertex, one square and two regular n-gons (vertex type 4.n.n). Find n.', '8', ['6', '10', '12'],
         ['90 + 2·(n − 2)180/n = 360 gives 2(n − 2)180/n = 270, so 360n − 720 = 270n and n = 8.'], 'tessellate', order='sort')
    b.mc(9, 'honors', 'Which vertex arrangement of regular polygons fits exactly around a point?', '3.3.3.3.6 (four triangles and a hexagon)', ['3.3.3.3.3.3.3 (seven triangles)', '4.4.6 (two squares and a hexagon)', '5.5.5 (three pentagons)'],
         ['Angles: 4·60 + 120 = 360.', '7·60 = 420, 90 + 90 + 120 = 300, 3·108 = 324.'], 'tessellate')
    b.sel(9, 'cp2', 'Which regular polygons tile the plane by themselves?', [('Equilateral triangle', True), ('Square', True), ('Regular hexagon', True), ('Regular octagon', False), ('Regular pentagon', False)],
          ['Interior angles 60°, 90°, 120° divide 360°; 135° and 108° do not.'], 'tessellate_select')
    b.sel(9, 'cp1', 'Which numbers are triangular numbers (1, 3, 6, 10, ...)?', [('21', True), ('28', True), ('55', True), ('30', False), ('50', False)], ['T_n = n(n + 1)/2: 21 = T₆, 28 = T₇, 55 = T₁₀.'], 'figurate_select')
    b.sel(9, 'honors', 'Which vertex types (lists of regular polygons around a point) have angles summing to exactly 360°?',
          [('3.12.12', True), ('4.6.12', True), ('3.4.4.6', True), ('5.5.10', True), ('4.5.20', True), ('6.6.8', False)][1:],
          ['3.12.12: 60 + 150 + 150; 4.6.12: 90 + 120 + 150; 3.4.4.6: 60 + 90 + 90 + 120; 5.5.10: 108 + 108 + 144; 4.5.20: 90 + 108 + 162 = 360 (only the first three types also extend to a tessellation of the whole plane).', '6.6.8: 120 + 120 + 135 = 375.'], 'tessellate_select')
    b.orq(9, 'cp2', 'A pattern of squares: figure 1 has 1 square, figure 2 has 5, figure 3 has 9.',
          [('How many squares are in figure 4?', '13'), ('Write a rule for figure n.', '4n − 3'), ('How many squares are in figure 25?', '97'), ('Which figure has 81 squares?', 'Figure 21')],
          ['Add 4.', 'Arithmetic.', '4·25 − 3.', '4n − 3 = 81.'], 'pattern_or')
    b.orq(9, 'cp1', 'Triangular numbers T_n = 1 + 2 + ... + n.',
          [('Find T₁ through T₅.', '1, 3, 6, 10, 15'), ('Write a recursive rule.', 'T₁ = 1, T_n = T_(n−1) + n'), ('Show T_(n−1) + T_n = n² for n = 4.', 'T₃ + T₄ = 6 + 10 = 16 = 4²'), ('Find T₁₀₀.', '5050')],
          ['Add.', 'Each figure adds a row of n dots.', 'Two triangles make a square.', 'n(n + 1)/2.'], 'pattern_or')
    b.orq(9, 'honors', 'Regular tessellations: k regular n-gons meet at a vertex.',
          [('Write an equation relating k and n.', 'k·(n − 2)180/n = 360'), ('Simplify to (n − 2)(k − 2) = 4.', 'kn − 2k − 2n = 0, so (n − 2)(k − 2) = 4'),
           ('Find all positive integer solutions with n ≥ 3.', '(n, k) = (3, 6), (4, 4), (6, 3)'), ('Interpret the solutions.', 'Only triangles, squares and hexagons give regular tessellations.')],
          ['Angle sum at a vertex.', 'Multiply by n/180 and rearrange; add 4.', 'Factor pairs of 4.', 'Three regular tessellations.'], 'tessellation_or')


# ---------------------------------------------------------------- errors
def errors(b):
    E = b.err
    E(2, 'cp2', 'Find a₁₀ for the arithmetic sequence 4, 7, 10, ...', 'Jordan', ['a₁₀ = 4 + 10·3 = 34'],
      '31', 'Jordan used n·d instead of (n − 1)d. From a₁ to a₁₀ there are only 9 steps.', 'a_n = a₁ + (n − 1)d.', ['a₁₀ = 4 + 9·3 = 31.'], 'n_minus_one_error')
    E(3, 'cp2', 'Evaluate 0!.', 'Sam', ['0! = 0 because you multiply no numbers... so 0.'],
      '1', 'Sam forgot that 0! is defined as 1 (an empty product equals 1).', 'This makes n! = n(n − 1)! work for n = 1 and C(n, 0) = 1.', ['0! = 1.'], 'zero_factorial_error')
    E(5, 'cp2', 'Find a₄ for a₁ = 3, a_n = 2a_(n−1) − 1.', 'Riley', ['a₂ = 2·3 − 1 = 5', 'a₃ = 2·3 − 1 = 5', 'a₄ = 5'],
      '17', 'Riley kept using a₁ instead of the previous term.', 'Each term uses the term just before it.', ['a₂ = 5, a₃ = 9, a₄ = 17.'], 'rec_previous_error')
    E(1, 'cp2', 'Evaluate Σ_{k=1}^{4} 2k.', 'Casey', ['Σ 2k = 2·4 = 8'],
      '20', 'Casey substituted only the last value of k.', 'Σ means add the terms for every k from 1 to 4.', ['2 + 4 + 6 + 8 = 20.'], 'sigma_last_error')
    E(4, 'cp2', 'With F₁ = F₂ = 1, find F₆.', 'Avery', ['1, 1, 2, 4, 8, 16, so F₆ = 16'],
      '8', 'Avery doubled each term instead of adding the two previous terms.', 'F_n = F_(n−1) + F_(n−2).', ['1, 1, 2, 3, 5, 8.'], 'fib_double_error')
    E(9, 'cp2', 'Find each interior angle of a regular hexagon.', 'Morgan', ['360 ÷ 6 = 60°'],
      '120', 'Morgan computed the central (or exterior) angle. Interior angles sum to (n − 2)·180°.', 'Exterior angles sum to 360°, interior angles do not.', ['(6 − 2)·180 / 6 = 120°.'], 'interior_exterior_error')
    E(7, 'cp1', 'Inductive step for 1 + 2 + ... + n = n(n + 1)/2.', 'Taylor', ['Assume P(k + 1): 1 + ... + (k + 1) = (k + 1)(k + 2)/2.', 'Then P(k + 1) is true.'],
      'Assume P(k) and show P(k + 1): k(k + 1)/2 + (k + 1) = (k + 1)(k + 2)/2', 'Taylor assumed what had to be proved (P(k + 1)), which is circular.', 'The hypothesis is P(k); P(k + 1) is the goal.', ['Start from P(k) and add k + 1 to both sides.'], 'assume_goal_error')
    E(8, 'cp1', 'Inductive step for 3 | (4ⁿ − 1).', 'Jamie', ['4ᵏ⁺¹ − 1 = 4·4ᵏ − 1 = 4(4ᵏ − 1). Since 3 | 4ᵏ − 1, done.'],
      '4ᵏ⁺¹ − 1 = 4(4ᵏ − 1) + 3, so 3 divides it', 'Jamie dropped a term: 4(4ᵏ − 1) = 4ᵏ⁺¹ − 4, not 4ᵏ⁺¹ − 1.', 'Check the algebra by expanding.', ['4ᵏ⁺¹ − 1 = 4ᵏ⁺¹ − 4 + 3 = 4(4ᵏ − 1) + 3.'], 'dropped_term_error')
    E(3, 'cp1', 'Simplify 8!/6!.', 'Quinn', ['8!/6! = (8/6)! = (4/3)!'],
      '56', 'Quinn divided inside the factorial. Factorials do not divide that way.', 'Write the factorials out and cancel.', ['8!/6! = 8·7 = 56.'], 'factorial_divide_error')
    E(6, 'cp1', 'Find an explicit formula for a₀ = 3, a_n = a_(n−1) + 5.', 'Alex', ['a_n = 3 + 5(n − 1)'],
      'a_n = 3 + 5n', 'Alex used (n − 1) although the sequence starts at a₀, so after n steps 5 has been added n times.', 'Check a₀: Alex\'s formula gives −2, not 3.', ['a₀ = 3, a₁ = 8, a₂ = 13, so a_n = 3 + 5n.'], 'index_start_error')
    E(2, 'cp1', 'Find the sum 2 + 6 + 18 + ... + 486.', 'Jordan', ['Arithmetic sum: n = 6, (2 + 486)·6/2 = 1464'],
      '728', 'Jordan used the arithmetic sum formula on a geometric sequence (ratio 3).', 'Geometric sums use a(rⁿ − 1)/(r − 1).', ['486 = 2·3⁵, so n = 6 terms.', '2(3⁶ − 1)/2 = 728.'], 'wrong_sum_formula_error')
    E(9, 'cp1', 'How many diagonals does an octagon have?', 'Sam', ['Each vertex connects to 5 others by a diagonal: 8·5 = 40.'],
      '20', 'Sam counted each diagonal twice, once from each end.', 'Divide by 2: n(n − 3)/2.', ['8·5/2 = 20.'], 'double_count_diag_error')
    E(7, 'honors', 'Prove n² + n + 41 is prime for all n ≥ 0 by induction.', 'Riley', ['Base: n = 0 gives 41, prime.', 'Step: assume k² + k + 41 is prime; then (k + 1)² + (k + 1) + 41 = (k² + k + 41) + 2(k + 1), which is prime + even, so prime.'],
      'The statement is false (n = 40 gives 41²)', 'Riley used an invalid step: a prime plus an even number need not be prime.', 'Every step of an induction must be justified.', ['40² + 40 + 41 = 1681 = 41².'], 'invalid_step_error')
    E(8, 'honors', 'Prove 2ⁿ > n² for all n ≥ 1 by induction.', 'Casey', ['Base: 2 > 1.', 'Step: 2ᵏ⁺¹ = 2·2ᵏ > 2k² ≥ (k + 1)².'],
      'False for n = 2, 3, 4; the claim holds for n ≥ 5 with base case n = 5', 'Casey\'s step uses 2k² ≥ (k + 1)², which fails for k = 1 and 2; the statement itself is false at n = 2, 3, 4.', 'Check that the inductive step works for every k ≥ the base value.', ['2² = 4 = 2², 2³ = 8 < 9, 2⁴ = 16 = 4².', 'For k ≥ 3, 2k² ≥ (k + 1)², so start at n = 5 (32 > 25).'], 'step_range_error')
    E(4, 'honors', 'Prove F₁ + ... + F_n = F_(n+2) − 1 by induction. Step shown:', 'Avery', ['F₁ + ... + F_k + F_(k+1) = F_(k+2) − 1 + F_(k+1) = F_(k+3) − 1. Base case not needed since the step works.'],
      'Add the base case n = 1: F₁ = 1 = F₃ − 1', 'Avery skipped the base case. The inductive step alone proves nothing.', 'A false statement can have a valid-looking inductive step (e.g. adding 5 to both sides).', ['Base: 1 = 2 − 1.'], 'no_base_error')
    E(6, 'honors', 'Iterate T(n) = 2T(n − 1) + 1, T(0) = 0, to find T(n).', 'Morgan', ['T(n) = 2T(n − 1) + 1 = 2(2T(n − 2) + 1) + 1 = 4T(n − 2) + 2', 'Pattern: T(n) = 2ⁿT(0) + n = n'],
      'T(n) = 2ⁿ − 1', 'Morgan lost track of the constants: 2(2T + 1) + 1 = 4T + 3, not 4T + 2. The added terms form 1 + 2 + 4 + ... + 2ⁿ⁻¹.', 'Check: T(2) = 3, but Morgan\'s formula gives 2.', ['T(n) = 2ᵏT(n − k) + (2ᵏ − 1); k = n gives 2ⁿ − 1.'], 'iteration_constant_error')
    E(5, 'honors', 'Is a_n = 3ⁿ a solution of a_n = 5a_(n−1) − 6a_(n−2)?', 'Taylor', ['a₀ = 1, a₁ = 3, a₂ = 9; 5·3 − 6·1 = 9. It works for n = 2, so it is a solution.'],
      'Yes, but it must be checked for every n: 5·3ⁿ⁻¹ − 6·3ⁿ⁻² = 3ⁿ⁻²(15 − 6) = 3ⁿ', 'Taylor checked one value of n. Satisfying a recurrence means it holds for every n ≥ 2.', 'A general algebraic check is needed.', ['5·3ⁿ⁻¹ − 6·3ⁿ⁻² = 9·3ⁿ⁻² = 3ⁿ.'], 'one_case_rec_error')
    E(9, 'honors', 'Can regular pentagons and regular decagons (with no other shapes) tile around a single vertex?', 'Jamie', ['108 + 144 = 252, and 360 − 252 = 108, so one decagon and two pentagons fit: yes, they tessellate the plane.'],
      'They fit around one vertex (5.5.10), but they do not extend to a tessellation of the plane', 'Jamie assumed that a vertex arrangement that fits always extends to a full tiling.', 'Around a pentagon in 5.5.10, the vertex types cannot all be consistent.', ['Angle check alone is necessary, not sufficient.'], 'vertex_not_tiling_error')


def topup(b):
    need = lambda k, L: b.counter.get((k, L), 0) < 10

    def mcn(k, L, prompt, ans, wr, steps, fam):
        ws = [str(w) for w in dict.fromkeys(wr) if str(w) != str(ans)]
        b.mc(k, L, prompt, str(ans), ws[:3], steps, fam, order='sort')
    # 1: nth term by formula, distractors = neighbouring terms / misreads
    for L, disp, f, n in (('honors', 'a_n = (n² − 1)/(n + 1)', lambda n: Fraction(n * n - 1, n + 1), 20), ('cp2', 'a_n = 6 − 2n', lambda n: 6 - 2 * n, 9), ('cp1', 'a_n = 3·2ⁿ⁻¹', lambda n: 3 * 2 ** (n - 1), 7)):
        if need(1, L):
            mcn(1, L, 'For %s, find a_%d.' % (disp, n), frac(f(n)), [frac(f(n - 1)), frac(f(n + 1)), frac(f(n) + 1), frac(-f(n))],
                ['Substitute n = %d.' % n, 'a_%d = %s' % (n, frac(f(n)))], 'nth_term')
    # 2
    for L, a1, d, n in (('honors', 7, -4, 50), ('honors', 1000, -35, 29)):
        if need(2, L):
            v = a1 + (n - 1) * d
            mcn(2, L, 'An arithmetic sequence has a₁ = %d and d = %d. Find a_%d.' % (a1, d, n), v, [a1 + n * d, a1 + (n - 2) * d, v * -1],
                ['a_n = a₁ + (n − 1)d.', 'a_%d = %d + %d(%d) = %d' % (n, a1, n - 1, d, v)], 'arith_term')
    # 3: factorial / binomial MC
    for L, t, v, wr in (('cp2', '4!', 24, [16, 10, 12]), ('cp2', '6!/4!', 30, [2, 24, 720]), ('honors', 'C(15, 13)', 105, [210, 13, 2730]), ('honors', '(n + 1)!/(n − 1)! for n = 10', 110, [100, 11, 90])):
        if need(3, L):
            mcn(3, L, 'Evaluate %s.' % t, v, wr, ['Expand and cancel the common factorial part.', '%s = %d' % (t, v)], 'factorial_eval')
    # 4: Fibonacci MC
    for L, n in (('cp2', 8), ('cp2', 9), ('cp2', 11), ('cp1', 13), ('cp1', 16), ('honors', 18), ('honors', 25)):
        if need(4, L):
            mcn(4, L, 'With F₁ = F₂ = 1 and F_n = F_(n−1) + F_(n−2), what is F_%d?' % n, F(n), [F(n - 1), F(n + 1), 2 * F(n - 1)],
                ['List the terms up to n = %d.' % n, 'F_%d = %d' % (n, F(n))], 'fib_term')
    # 5: recursive term MC
    R5 = [('cp2', 'a₁ = 2, a_n = a_(n−1) + 5', lambda a, n: a + 5, 2, 6), ('cp2', 'a₁ = 1, a_n = 4a_(n−1)', lambda a, n: 4 * a, 1, 5), ('cp2', 'a₁ = 20, a_n = a_(n−1) − 3', lambda a, n: a - 3, 20, 7),
          ('cp1', 'a₁ = 1, a_n = 3a_(n−1) − 1', lambda a, n: 3 * a - 1, 1, 6), ('cp1', 'a₁ = 2, a_n = a_(n−1) + n', lambda a, n: a + n, 2, 8), ('cp1', 'a₁ = 1, a_n = 2a_(n−1) + n', lambda a, n: 2 * a + n, 1, 6),
          ('honors', 'a₁ = 1, a₂ = 3, a_n = a_(n−1) + 2a_(n−2)', None, None, 7), ('honors', 'a₁ = 3, a_n = a_(n−1)² − 2a_(n−1) + 2', lambda a, n: a * a - 2 * a + 2, 3, 5), ('honors', 'a₀ = 1, a_n = (n + 1)a_(n−1) − 1', lambda a, n: (n + 1) * a - 1, 1, 6)]
    for L, disp, g, a0, n in R5:
        if not need(5, L):
            continue
        if g is None:
            t = [1, 3]
            while len(t) < n:
                t.append(t[-1] + 2 * t[-2])
        else:
            st = 0 if disp.startswith('a₀') else 1
            t = run(g, a0, st, n + 1 - st)
        v = t[-1]
        mcn(5, L, 'For %s, find a_%d.' % (disp, n), v, [t[-2], v + (t[-1] - t[-2]), v - 1, v + 1],
            ['Terms: ' + lst(t) + '.', 'a_%d = %d' % (n, v)], 'rec_term')
    # 6: iteration computations
    for L, t, v, wr in (('cp2', 'Iterate a₁ = 3, a_n = a_(n−1) + 4 to find a₅.', 19, [23, 15, 20]), ('cp2', 'Iterate a₀ = 1, a_n = 3a_(n−1) to find a₄.', 81, [27, 243, 12]),
                        ('cp2', 'Tower of Hanoi needs 2ⁿ − 1 moves for n disks. How many moves for 4 disks?', 15, [16, 8, 7]), ('cp2', 'Iterate a₁ = 50, a_n = a_(n−1) − 6 to find a₄.', 32, [26, 38, 24]),
                        ('cp1', 'Iterate a₀ = 2, a_n = 2a_(n−1) − 1 to find a₅.', 33, [17, 65, 32]), ('cp1', 'Iterate a₁ = 0, a_n = a_(n−1) + 2(n − 1) to find a₅.', 20, [12, 30, 25]),
                        ('honors', 'Iterate a₀ = 1, a_n = a_(n−1) + 2ⁿ to find a₆.', 127, [63, 128, 255]), ('honors', 'If T(1) = 1 and T(n) = T(n − 1) + 3n − 1, find T(5).', 39, [30, 44, 40])):
        if need(6, L):
            mcn(6, L, t, v, wr, ['Apply the rule one step at a time.', 'Answer: %d' % v], 'rec_compute')
    chk = [run(lambda a, n: a + 4, 3, 1, 5)[-1] == 19, run(lambda a, n: 2 * a - 1, 2, 0, 6)[-1] == 33, run(lambda a, n: a + 2 * (n - 1), 0, 1, 5)[-1] == 20,
           run(lambda a, n: a + 2 ** n, 1, 0, 7)[-1] == 127, run(lambda a, n: a + 3 * n - 1, 1, 1, 5)[-1] == 39, run(lambda a, n: a - 6, 50, 1, 4)[-1] == 32]
    assert all(chk), chk
    # 7: base cases & hypotheses for more statements
    for L, st, base, wr in (('cp2', '"4 + 8 + ... + 4n = 2n(n + 1) for n ≥ 1"', 'n = 1: 4 = 2·1·2', ['n = 0: 0 = 0', 'n = 2: 12 = 12', 'n = k: 4k = 2k(k + 1)']),
                            ('cp2', '"5ⁿ − 1 is divisible by 4 for n ≥ 0"', 'n = 0: 5⁰ − 1 = 0, divisible by 4', ['n = 1: 5 − 1 = 4', 'n = 4: 624', 'n = k: 5ᵏ − 1']),
                            ('cp1', '"n² ≥ 2n + 1 for n ≥ 3"', 'n = 3: 9 ≥ 7', ['n = 1: 1 ≥ 3', 'n = 0: 0 ≥ 1', 'n = 2: 4 ≥ 5'])):
        if need(7, L):
            b.mc(7, L, 'What is the base case for an induction proof of %s?' % st, base, wr, ['Check the smallest n in the claim.', base], 'induction_base')
    # 8: cp2-friendly induction pieces
    E8 = [('cp2', 'Claim: 2 + 4 + ... + 2n = n(n + 1). Check the claim for n = 4: what is the left side?', '20', ['16', '10', '24']),
          ('cp2', 'Claim: 2 + 4 + ... + 2n = n(n + 1). What is the right side when n = 4?', '20', ['16', '8', '25']),
          ('cp2', 'In the inductive step for 1 + 2 + ... + n = n(n + 1)/2, which term is added to both sides to go from P(k) to P(k + 1)?', 'k + 1', ['k', '1', 'k(k + 1)/2']),
          ('cp2', 'Simplify k(k + 1) + 2(k + 1) by factoring.', '(k + 1)(k + 2)', ['k(k + 3)', '(k + 1)²', '2k(k + 1)']),
          ('cp2', 'Simplify k² + 2k + 1 as a square.', '(k + 1)²', ['(k + 2)²', 'k² + 1', '(2k + 1)²']),
          ('cp2', 'If 2ᵏ > k, which inequality follows by multiplying both sides by 2?', '2ᵏ⁺¹ > 2k', ['2ᵏ⁺¹ > k + 1 directly', '2ᵏ > 2k', '2ᵏ⁺¹ > k']),
          ('cp1', 'Simplify 5(5ᵏ − 1) + 4.', '5ᵏ⁺¹ − 1', ['5ᵏ⁺¹ + 3', '5ᵏ − 1', '25ᵏ − 1']),
          ('honors', 'In proving Σ_{i=1}^{n} i³ = (n(n + 1)/2)², the step needs (k(k + 1)/2)² + (k + 1)³ = ?', '((k + 1)(k + 2)/2)²', ['((k + 1)(k + 1)/2)²', '(k(k + 2)/2)²', '(k + 1)³(k + 2)/2'])]
    for L, t, good, bad in E8:
        if need(8, L):
            b.mc(8, L, t, good, bad, ['Expand or factor and compare.', good], 'induction_algebra',
                 notes='Hand-authored; algebra re-checked numerically by verify_banks.py for k = 1..10 where an expression is given.')
    # 9
    for L, t, v, wr in (('cp2', 'What is the sum of the interior angles of a pentagon, in degrees?', 540, [360, 720, 108]), ('cp2', 'A pattern adds 2 tiles each step, starting with 3 tiles. How many tiles in step 10?', 21, [23, 20, 30]),
                        ('cp1', 'How many diagonals does a hexagon have?', 9, [18, 6, 12]), ('cp1', 'Square numbers: what is the 12th square number?', 144, [121, 169, 24]),
                        ('honors', 'How many sides does a regular polygon with interior angle 156° have?', 15, [12, 18, 24]), ('honors', 'At a vertex of type 3.3.4.3.4, what is the angle sum (degrees)?', 360, [330, 390, 420])):
        if need(9, L):
            mcn(9, L, t, v, wr, ['Use the pattern or angle rule.', 'Answer: %d' % v], 'pattern_mc')


def topup2(b):
    b.mc(7, 'honors', 'A strong-induction proof that every integer n ≥ 2 is a product of primes assumes what in the inductive step?', 'Every integer j with 2 ≤ j ≤ k is a product of primes',
         ['Only k is a product of primes', 'k + 1 is a product of primes', 'Every integer is prime'], ['Strong induction assumes all earlier cases, because k + 1 = ab uses factors a, b smaller than k + 1.'], 'strong_hypothesis')
    b.mc(8, 'cp1', 'Inductive step for "2ⁿ ≥ n + 1": from 2ᵏ ≥ k + 1, which chain proves 2ᵏ⁺¹ ≥ k + 2?', '2ᵏ⁺¹ = 2·2ᵏ ≥ 2(k + 1) = 2k + 2 ≥ k + 2',
         ['2ᵏ⁺¹ = 2ᵏ + 1 ≥ k + 2', '2ᵏ⁺¹ ≥ k + 1 + 1, since 2ᵏ⁺¹ = 2ᵏ + 1', '2ᵏ⁺¹ = (k + 1)² ≥ k + 2'],
         ['Multiply the hypothesis by 2, then use 2k + 2 ≥ k + 2 for k ≥ 0.'], 'induction_inequality')
    b.mc(8, 'honors', 'Inductive step for "7 | (8ⁿ − 1)": which rewriting of 8ᵏ⁺¹ − 1 uses the hypothesis 7 | (8ᵏ − 1)?', '8(8ᵏ − 1) + 7',
         ['8(8ᵏ − 1)', '(8ᵏ − 1) + 8', '7(8ᵏ − 1) + 1'], ['8ᵏ⁺¹ − 1 = 8·8ᵏ − 8 + 7 = 8(8ᵏ − 1) + 7, a sum of multiples of 7.'], 'induction_divisibility')
    assert all(8 ** (k + 1) - 1 == 8 * (8 ** k - 1) + 7 for k in range(10))


# ---------------------------------------------------------------- Honors Partner Check pairs (added 2026-11-08)
# The Partner Check printable needs two DIFFERENT Honors problems with the SAME answer for each row (and different answers
# across rows). The Honors pool had no shared answers, so the sheet fell back to CP1. Each item below is a new Honors
# short-answer problem whose answer is computed here from its own parameters (brute force or direct iteration, not copied)
# and then asserted equal to its partner's answer string. Partners are existing Honors items (found by prompt) or, for
# skills 7 and 8, a second new item. Appended last so no existing question ID changes.
def _least_threshold(holds, top=400):
    """Least N with holds(n) for every N <= n <= top, and holds(N - 1) false."""
    assert holds(top)
    n = top
    while n > 1 and holds(n - 1):
        n -= 1
    return n


def honors_partners(b):
    H = 'honors'

    def find(prefix):
        hits = [q for q in b.q if q['level'] == H and q['prompt'].startswith(fix_text(prefix))]
        assert len(hits) == 1, (prefix, len(hits))
        return hits[0]

    def add(skill, partner, prompt, value, steps):
        ans = frac(value) if isinstance(value, Fraction) else str(value)
        assert ans == str(partner['answer']), (prompt, ans, partner['answer'])
        assert partner['format'] in ('short-answer', 'multiple-choice') and fix_text(prompt).strip() != partner['prompt']
        r = b.sa(skill, H, prompt, ans, list(steps) + ['Answer: %s' % ans], 'partner_pair')
        r['sourceNotes'] = ('Partner-check companion to %s (same answer, different problem). ' % partner['id']) + r['sourceNotes']
        return r

    # ---- skill 1: sums, products, explicit formulas
    v = sum(Fraction(2, (k + 1) * (k + 2)) for k in range(1, 9))
    add(1, find('Evaluate Σ_{k=1}^{4} 1/(k(k + 1))'), 'Evaluate the telescoping sum Σ_{k=1}^{8} 2/((k + 1)(k + 2)). (Give a fraction a/b.)', v,
        ['2/((k + 1)(k + 2)) = 2(1/(k + 1) − 1/(k + 2)).', 'The middle terms cancel: 2(1/2 − 1/10) = 2 · 2/5.', 'Value: 4/5'])
    v = sum(Fraction(1, k * (k + 1)) for k in range(4, 20))
    add(1, find('Evaluate Π_{k=2}^{5} (1 − 1/k)'), 'Evaluate Σ_{k=4}^{19} 1/(k(k + 1)). (Give a fraction a/b.)', v,
        ['1/(k(k + 1)) = 1/k − 1/(k + 1).', 'The sum telescopes from k = 4 to k = 19: 1/4 − 1/20.', '5/20 − 1/20 = 4/20 = 1/5'])
    v = sum((-1) ** (k + 1) * (2 * k - 1) for k in range(1, 20))
    add(1, find('For a_n = (n² − 1)/(n + 1), find a_20'), 'Let a_n = Σ_{k=1}^{n} (−1)ᵏ⁺¹(2k − 1), so a_n = 1 − 3 + 5 − ... ± (2n − 1). Find a₁₉.', v,
        ['Pair the terms: (1 − 3) + (5 − 7) + ... and each pair is −2.', 'n = 19: nine pairs give −18, and the last term is 2·19 − 1 = 37.', 'a₁₉ = −18 + 37 = 19 (in general a_n = n for odd n).'])

    # ---- skill 2: arithmetic and geometric sequences and series
    d = Fraction(35 - 27, 12 - 4); a1 = 27 - 3 * d
    v = sum(a1 + i * d for i in range(20))
    add(2, find('Find the sum: 5 + 8 + 11'), 'An arithmetic sequence has a₄ = 27 and a₁₂ = 35. Find the sum of its first 20 terms.', int(v),
        ['8d = 35 − 27, so d = 1 and a₁ = 27 − 3d = 24.', 'a₂₀ = 24 + 19 = 43.', 'S₂₀ = 20 · (24 + 43) ÷ 2 = 10 · 67 = 670'])
    r = next(x for x in range(1, 10) if 12 * x ** 4 == 192); a1 = Fraction(12, r * r)
    v = sum(a1 * r ** i for i in range(9))
    add(2, find('Find the sum: 3 + 6 + 12'), 'A geometric sequence with positive terms has a₃ = 12 and a₇ = 192. Find a₁ + a₂ + ... + a₉.', int(v),
        ['r⁴ = a₇/a₃ = 16, so r = 2 (the terms are positive).', 'a₁ = a₃/r² = 3.', 'S₉ = 3(2⁹ − 1)/(2 − 1) = 3 · 511 = 1533'])
    r = next(x for x in range(1, 10) if 2 * x ** 3 == 16)
    add(2, find('A geometric sequence has a₁ = 1/4'), 'A geometric sequence has a₃ = 2 and a₆ = 16. Find a₉.', 16 * r ** 3,
        ['a₆/a₃ = r³ = 8, so r = 2.', 'a₉ = a₆ · r³ = 16 · 8 = 128'])

    # ---- skill 3: factorials and binomial coefficients
    v = sum(C(m, 2) for m in range(2, 12))
    assert v == C(12, 3)
    add(3, find('Evaluate C(12, 3)'), 'Use the hockey stick identity to evaluate C(2, 2) + C(3, 2) + C(4, 2) + ... + C(11, 2).', v,
        ['Hockey stick identity: Σ_{m=r}^{n} C(m, r) = C(n + 1, r + 1).', 'Here r = 2 and n = 11, so the sum is C(12, 3).', 'C(12, 3) = (12 · 11 · 10) ÷ 6 = 220'])
    v = sum(C(5, k) ** 2 for k in range(6))
    add(3, find('Evaluate C(10, 5)'), 'Evaluate C(5, 0)² + C(5, 1)² + C(5, 2)² + C(5, 3)² + C(5, 4)² + C(5, 5)².', v,
        ['Row 5 of Pascal\'s triangle is 1, 5, 10, 10, 5, 1.', 'Squares: 1 + 25 + 100 + 100 + 25 + 1 = 252.', 'Check: Σ C(n, k)² = C(2n, n) = C(10, 5) = 252.'])
    v = Fraction(math.factorial(8), 2 ** 4 * math.factorial(4))
    assert v == 1 * 3 * 5 * 7
    add(3, find('Evaluate C(15, 13)'), 'Evaluate 8!/(2⁴ · 4!).', int(v),
        ['8! = 40320 and 2⁴ · 4! = 16 · 24 = 384.', '40320/384 = 105.', 'Check: 8!/(2⁴·4!) = 1·3·5·7, the number of ways to split 8 people into 4 pairs.'])

    # ---- skill 4: Fibonacci numbers
    assert F(16) == F(8) * (F(7) + F(9))
    add(4, find('Compute F₁ + F₃ + F₅'), 'Use F_(2n) = F_n(F_(n−1) + F_(n+1)) with n = 8 to find F₁₆ (F₁ = F₂ = 1).', F(8) * (F(7) + F(9)),
        ['F₇ = 13, F₈ = 21, F₉ = 34.', 'F₁₆ = 21(13 + 34) = 21 · 47 = 987'])
    v = sum(1 for m in range(2 ** 16) if m & (m >> 1) == 0)   # brute force over all 65536 strings
    add(4, find('With F₁ = F₂ = 1 and F_n = F_(n−1) + F_(n−2), what is F_18'), 'How many bit strings of length 16 have no two consecutive 1s?', v,
        ['Let b_n count them. A valid string ends in 0 (after any valid string of length n − 1) or in 01 (after any valid string of length n − 2).',
         'So b_n = b_(n−1) + b_(n−2) with b₁ = 2, b₂ = 3, which gives b_n = F_(n+2).', 'b₁₆ = F₁₈ = 2584'])
    v = sum(C(10 - k, k) for k in range(6))   # k = number of stacked horizontal pairs
    add(4, find('The number of ways to climb n stairs'), 'In how many ways can a 2 × 10 rectangle be tiled with 1 × 2 dominoes?', v,
        ['Let t_n count tilings of a 2 × n rectangle. The left end is one vertical domino (leaving 2 × (n − 1)) or two stacked horizontal dominoes (leaving 2 × (n − 2)).',
         't_n = t_(n−1) + t_(n−2) with t₁ = 1, t₂ = 2, so t_n = F_(n+1).', 't₁₀ = F₁₁ = 89'])

    # ---- skill 5: recursively defined sequences
    t = run(lambda a, n: 4 * a + 1, 1, 0, 4)
    assert t[-1] == (4 ** 4 - 1) // 3
    add(5, find('For a₁ = 1, a₂ = 3, a_n = a_(n−1) + 2a_(n−2), find a_7'), 'Let a₀ = 1 and a_n = 4a_(n−1) + 1 for n ≥ 1. Find a₃, then check it with the closed form a_n = (4ⁿ⁺¹ − 1)/3.', t[-1],
        ['a₁ = 5, a₂ = 21, a₃ = 85.', 'Closed form: (4⁴ − 1)/3 = 255/3 = 85'])
    f = [3]
    while len(f) < 5:
        f.append(math.prod(f) + 2)
    assert f[-1] == 2 ** 16 + 1
    add(5, find('For a₁ = 3, a_n = a_(n−1)² − 2a_(n−1) + 2, find a_5'), 'Fermat numbers satisfy f₀ = 3 and f_n = f₀ · f₁ ··· f_(n−1) + 2 for n ≥ 1. Find f₄.', f[-1],
        ['f₁ = 3 + 2 = 5, f₂ = 3·5 + 2 = 17, f₃ = 3·5·17 + 2 = 257.', 'f₄ = 3 · 5 · 17 · 257 + 2 = 65535 + 2 = 65537'])

    # ---- skill 6: solving recurrences by iteration
    T = {1: 1}
    for k in range(1, 10):
        T[2 ** k] = 2 * T[2 ** (k - 1)] + 1
    add(6, find('Tower of Hanoi: m₁ = 1'), 'T(n) = 2T(n/2) + 1 with T(1) = 1, for n a power of 2. Find T(512).', T[512],
        ['Iterate: T(n) = 2ᵏT(n/2ᵏ) + (2ᵏ − 1).', 'With 2ᵏ = n: T(n) = n + (n − 1) = 2n − 1.', 'T(512) = 1023'])
    t = run(lambda a, n: a + 3 * n * n - 3 * n + 1, 1, 1, 4)
    assert t == [n ** 3 for n in range(1, 5)]
    add(6, find('T(n) = 2T(n/2) + n with T(1) = 0'), 'Iterate a₁ = 1, a_n = a_(n−1) + 3n² − 3n + 1 to find a₄. (Compare the terms with perfect cubes.)', t[-1],
        ['a₂ = 1 + 7 = 8, a₃ = 8 + 19 = 27, a₄ = 27 + 37 = 64.', 'Since n³ − (n − 1)³ = 3n² − 3n + 1, a_n = n³.', 'a₄ = 64'])
    t = run(lambda a, n: a + (-1) ** n * n, 0, 0, 6)
    add(6, find('Iterate a_n = −a_(n−1) + 2 with a₀ = 5'), 'Iterate a₀ = 0, a_n = a_(n−1) + (−1)ⁿ · n to find a₅.', t[-1],
        ['a₁ = −1, a₂ = 1, a₃ = −2, a₄ = 2, a₅ = −3.', 'Pattern: a_n = −(n + 1)/2 for odd n.', 'a₅ = −3'])
    t = run(lambda a, n: 2 * a + 1, 4, 1, 4)
    assert t[-1] == 5 * 2 ** 3 - 1
    add(6, find('If T(1) = 1 and T(n) = T(n − 1) + 3n − 1'), 'Iterate a₁ = 4, a_n = 2a_(n−1) + 1 to find a₄, and check it with a_n = 5 · 2ⁿ⁻¹ − 1.', t[-1],
        ['a₂ = 9, a₃ = 19, a₄ = 39.', 'Closed form: 5 · 2³ − 1 = 39'])

    # ---- skill 7: principle of induction (choosing the base case); both partners are new
    pa = b.sa(7, H, 'Find the least integer N such that 2ⁿ > n² + n for every integer n ≥ N. (This N is the base case of an induction proof.)',
              _least_threshold(lambda n: 2 ** n > n * n + n),
              ['n = 4: 16 < 20, so N > 4; n = 5: 32 > 30.', 'Step for k ≥ 5: 2ᵏ⁺¹ = 2·2ᵏ > 2k² + 2k ≥ (k + 1)² + (k + 1), because k² ≥ k + 2 for k ≥ 2.', 'Answer: 5'], 'partner_pair')
    add(7, pa, 'Find the least integer N such that n! > 2ⁿ⁺¹ for every integer n ≥ N.', _least_threshold(lambda n: math.factorial(n) > 2 ** (n + 1)),
        ['n = 4: 24 < 32, so N > 4; n = 5: 120 > 64.', 'Step for k ≥ 5: (k + 1)! = (k + 1)k! > (k + 1)2ᵏ⁺¹ ≥ 2 · 2ᵏ⁺¹ = 2ᵏ⁺².'])
    pa = b.sa(7, H, 'Find the least integer N such that n! > 3ⁿ for every integer n ≥ N.', _least_threshold(lambda n: math.factorial(n) > 3 ** n),
              ['n = 6: 720 < 729, so N > 6; n = 7: 5040 > 2187.', 'Step for k ≥ 7: (k + 1)! = (k + 1)k! > (k + 1)3ᵏ ≥ 3 · 3ᵏ = 3ᵏ⁺¹.', 'Answer: 7'], 'partner_pair')
    reach = lambda n: any((n - 5 * y) % 3 == 0 for y in range(n // 5 + 1))
    add(7, pa, 'Strong induction shows that every amount of at least 8 cents can be made with 3-cent and 5-cent stamps. What is the largest amount (in cents) that CANNOT be made?',
        max(n for n in range(1, 200) if not reach(n)),
        ['7 cannot be made: 7, 7 − 5 = 2 are not multiples of 3.', 'Base cases 8 = 3 + 5, 9 = 3·3, 10 = 5·2; step: k + 1 = (k − 2) + 3 uses the case k − 2 ≥ 8.', 'So every amount ≥ 8 works and 7 is the largest that does not.'])

    # ---- skill 8: writing inductive proofs (the algebra of the inductive step); both partners are new
    cs = {7 ** (k + 1) - 1 - 7 * (7 ** k - 1) for k in range(12)}
    assert len(cs) == 1
    pa = b.sa(8, H, 'Inductive step for 6 | (7ⁿ − 1): write 7ᵏ⁺¹ − 1 = 7(7ᵏ − 1) + c. Find the integer c.', cs.pop(),
              ['7ᵏ⁺¹ − 1 = 7·7ᵏ − 7 + 6 = 7(7ᵏ − 1) + 6.', 'Both 7(7ᵏ − 1) (by the hypothesis) and 6 are multiples of 6.', 'Answer: 6'], 'partner_pair')
    cs = {Fraction((k + 1) ** 3 - (k + 1) - (k ** 3 - k), k * (k + 1) // 2) for k in range(1, 15)}
    assert len(cs) == 1
    add(8, pa, 'Inductive step for 6 | (n³ − n): (k + 1)³ − (k + 1) = (k³ − k) + c · T_k, where T_k = k(k + 1)/2 is an integer. Find the integer c.', cs.pop(),
        ['(k + 1)³ − (k + 1) = k³ + 3k² + 2k = (k³ − k) + 3k(k + 1).', '3k(k + 1) = 6 · k(k + 1)/2 = 6T_k, so c = 6.', 'Both terms are multiples of 6, which completes the step.'])

    # ---- skill 9: patterns and tessellations
    v = sum(k * k for k in range(1, 7))
    add(9, find('A hexagonal tile pattern has 1 tile'), 'Cannonballs are stacked in a square pyramid: 1 ball on top, then layers of 4, 9, 16, ... balls. How many balls are in a pyramid with 6 layers?', v,
        ['Total = 1 + 4 + 9 + 16 + 25 + 36 = 91.', 'Check with the sum of squares: n(n + 1)(2n + 1) ÷ 6 = (6 · 7 · 13) ÷ 6 = 91.'])
    n = next(m for m in range(4, 100) if m * (m - 3) == 340)
    add(9, find('Find the measure of each interior angle of a regular 20'), 'A regular polygon has 170 diagonals. Find the measure of each interior angle, in degrees.', frac(Fraction(180 * (n - 2), n)),
        ['n(n − 3)/2 = 170 gives n² − 3n − 340 = 0, so (n − 20)(n + 17) = 0 and n = 20.', 'Each interior angle = (20 − 2) · 180° ÷ 20 = 3240° ÷ 20 = 162°.'])
