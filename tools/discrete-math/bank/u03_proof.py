"""Unit 3: Elementary Number Theory and Methods of Proof (8 skills).
Numeric keys (divisibility, quotient-remainder, gcd, primes, counterexamples) are computed. Proof items ask for
steps, setups, strategies, conclusions or counterexamples; no item claims to check a free-form proof."""
import math
from fractions import Fraction
from core import Bank, fmt_set

U = 'number-theory-proof'


def isprime(n):
    return n > 1 and all(n % d for d in range(2, int(n ** .5) + 1))


def build():
    b = Bank(U, 'np', 8)
    for f in (s1, s2, s3, s4, s5, s6, s7, s8, topup, topup2, topup3, topup4, errors):
        f(b)
    return b


# ---------------------------------------------------------------- 1. definitions, conjectures, counterexamples
DEFS = [
    ('An integer n is even', 'if and only if n = 2k for some integer k', ['if and only if n = 2k + 1 for some integer k', 'if and only if n/2 is a whole number greater than 0', 'if and only if n = k + 2 for some integer k']),
    ('An integer n is odd', 'if and only if n = 2k + 1 for some integer k', ['if and only if n = 2k for some integer k', 'if and only if n is not divisible by 3', 'if and only if n = 2k + 1 for every integer k']),
    ('A real number r is rational', 'if and only if r = a/b for some integers a and b with b ≠ 0', ['if and only if r has a finite decimal expansion', 'if and only if r = a/b for some real numbers a and b', 'if and only if r is a fraction less than 1']),
    ('For integers d and n with d ≠ 0, d divides n (d | n)', 'if and only if n = dk for some integer k', ['if and only if d = nk for some integer k', 'if and only if n/d < 1', 'if and only if d + n is even']),
    ('An integer n > 1 is prime', 'if and only if its only positive divisors are 1 and n', ['if and only if it is odd', 'if and only if it has exactly one positive divisor', 'if and only if it is not divisible by 2, 3 or 5']),
    ('An integer n > 1 is composite', 'if and only if n = rs for some integers r and s with 1 < r < n and 1 < s < n', ['if and only if n is even', 'if and only if n = rs for some integers r and s', 'if and only if n has at least one divisor']),
]
CONJ = [  # (conjecture over domain, domain, predicate, level, true?)
    ('For every integer n with 1 ≤ n ≤ 10, n² + n + 1 is prime.', range(1, 11), lambda n: isprime(n * n + n + 1), 'cp1'),
    ('For every integer n with 2 ≤ n ≤ 20, 2ⁿ − 1 is prime whenever n is prime.', range(2, 21), lambda n: (not isprime(n)) or isprime(2 ** n - 1), 'honors'),
    ('For every integer n with 1 ≤ n ≤ 12, n² − n + 41 is prime.', range(1, 13), lambda n: isprime(n * n - n + 41), 'cp1'),
    ('For every integer n with 1 ≤ n ≤ 8, the sum 1 + 3 + 5 + ... + (2n − 1) is a perfect square.', range(1, 9), lambda n: int(math.isqrt(n * n)) ** 2 == sum(range(1, 2 * n, 2)), 'cp2'),
    ('For every integer n with 0 ≤ n ≤ 6, 3ⁿ + 2 is prime.', range(0, 7), lambda n: isprime(3 ** n + 2), 'cp2'),
    ('For every integer n with 1 ≤ n ≤ 10, n³ − n is divisible by 6.', range(1, 11), lambda n: (n ** 3 - n) % 6 == 0, 'honors'),
]


def s1(b):
    for L, idx in (('cp2', [0, 1]), ('cp1', [2, 3]), ('honors', [4, 5])):
        for i in idx:
            t, good, bad = DEFS[i]
            b.mc(1, L, 'Complete the definition: %s ...' % t, good, bad, ['Definitions are biconditionals: they work in both directions.', '%s %s.' % (t, good)], 'definition')
    for st, D, f, L in CONJ:
        bad = [n for n in D if not f(n)]
        b.sa(1, L, 'Test the conjecture. Give the smallest counterexample n, or write "none" if it holds for every n in the stated range.\n%s' % st,
             str(bad[0]) if bad else 'none',
             ['Check each n in order: ' + ', '.join('%d→%s' % (n, 'T' if f(n) else 'F') for n in D) + '.',
              ('Smallest counterexample: n = %d.' % bad[0]) if bad else 'No counterexample in the range (a finite check, not a proof for all integers).'], 'conjecture_test')
    CLS = [('0', 'Even', 'cp2', '0 = 2·0.'), ('−7', 'Odd', 'cp2', '−7 = 2(−4) + 1.'), ('1', 'Neither prime nor composite', 'cp1', 'Primes and composites are integers greater than 1.'),
           ('91', 'Composite', 'cp1', '91 = 7 · 13.'), ('97', 'Prime', 'cp2', 'No prime up to √97 ≈ 9.8 divides 97.'), ('2', 'Prime', 'honors', '2 is the only even prime; its positive divisors are 1 and 2.'),
           ('221', 'Composite', 'honors', '221 = 13 · 17.')]
    for n, good, L, why in CLS:
        opts = ['Prime', 'Composite', 'Neither prime nor composite'] if good in ('Prime', 'Composite', 'Neither prime nor composite') else ['Even', 'Odd', 'Neither even nor odd']
        bad = [o for o in opts if o != good] + (['Both prime and composite'] if 'Prime' in opts else ['Both even and odd'])
        b.mc(1, L, 'Classify the integer %s.' % n, good, bad, [why], 'classify_integer')
    b.sel(1, 'cp2', 'Which numbers are counterexamples to "Every odd number is prime"?',
          [('9', True), ('15', True), ('7', False), ('2', False), ('21', True)], ['A counterexample must be odd AND not prime: 9, 15, 21.', '7 is prime; 2 is not odd.'], 'counterexample_select')
    b.sel(1, 'cp1', 'Which values of x are counterexamples to "For every real number x, x² > x"?',
          [('0', True), ('1', True), ('1/2', True), ('2', False), ('−1', False)], ['Need x² ≤ x: 0 ≤ 0, 1 ≤ 1, 1/4 ≤ 1/2.', '4 > 2 and 1 > −1, so 2 and −1 are not counterexamples.'], 'counterexample_select')
    pairs = [(4, 2), (9, 3), (4, 10), (3, 5), (5, 10)]
    isce = lambda a, bb: (bb * 6) % a == 0 and bb % a != 0 and 6 % a != 0
    b.sel(1, 'honors', 'Which pairs (a, b) of positive integers are counterexamples to "If a | bc, then a | b or a | c" when c = 6?',
          [('a = %d, b = %d' % p, isce(*p)) for p in pairs],
          ['A counterexample needs a | 6b, a ∤ b and a ∤ 6.'] + ['a = %d, b = %d: %d | %d is %s; %s' % (a, bb, a, 6 * bb, (6 * bb) % a == 0, 'counterexample' if isce(a, bb) else 'not a counterexample') for a, bb in pairs], 'counterexample_select')
    b.orq(1, 'cp2', 'Conjecture: "The sum of any two odd integers is odd."',
          [('Test 3 + 5. Is the result odd?', 'No, 8 is even.'), ('Is the conjecture true or false?', 'False'),
           ('What is 3 + 5 called with respect to the conjecture?', 'A counterexample'), ('Write a corrected conjecture.', 'The sum of any two odd integers is even.')],
          ['3 + 5 = 8.', 'One counterexample disproves it.', 'A counterexample makes the hypothesis true and the conclusion false.', '(2a+1) + (2b+1) = 2(a+b+1).'], 'conjecture_or')
    b.orq(1, 'cp1', 'Conjecture: "For every positive integer n, n² + 1 is not divisible by 3."',
          [('Test n = 1, 2, 3, 4.', '2, 5, 10, 17: none divisible by 3.'), ('What are the possible remainders of n when divided by 3?', '0, 1, 2'),
           ('Find n² + 1 mod 3 in each case.', 'n ≡ 0: 1; n ≡ 1: 2; n ≡ 2: 5 ≡ 2.'), ('Is the conjecture true? What kind of argument did part (c) give?', 'True; a proof by division into cases (not just examples).')],
          ['Compute.', 'Quotient-remainder theorem.', '(3k+r)² + 1 ≡ r² + 1 (mod 3).', 'Cases cover every integer.'], 'conjecture_or')
    b.orq(1, 'honors', 'Fermat conjectured that 2^(2ⁿ) + 1 is prime for every n ≥ 0.',
          [('Compute the values for n = 0, 1, 2, 3.', '3, 5, 17, 257'), ('Are those values prime?', 'Yes'),
           ('Euler found that 641 divides 2^32 + 1 = 4294967297. What does this show?', 'The conjecture is false; n = 5 is a counterexample.'),
           ('Why did checking n = 0 to 4 not prove the conjecture?', 'Examples cannot prove a statement about infinitely many n.')],
          ['2¹ + 1, 2² + 1, 2⁴ + 1, 2⁸ + 1.', '3, 5, 17, 257 are prime.', '4294967297 = 641 · 6700417.', 'A universal statement needs a general proof.'], 'conjecture_or')


# ---------------------------------------------------------------- 2. direct proof
DP = [  # (theorem, missing-step prompt, correct, distractors)
    ('The sum of two even integers is even.', 'Let m = 2a and n = 2b for integers a, b. Then m + n = ___.', '2(a + b), which is even because a + b is an integer',
     ['2a + 2b, which is even because 2a and 2b are even', '4ab, which is even', '2(ab), which is even because ab is an integer']),
    ('The product of two odd integers is odd.', 'Let m = 2a + 1 and n = 2b + 1. Then mn = 4ab + 2a + 2b + 1 = ___.', '2(2ab + a + b) + 1, which is odd',
     ['2(2ab + a + b), which is even', '4ab + 1, which is odd', '2(a + b) + 1, which is odd']),
    ('If n is odd, then n² is odd.', 'Let n = 2k + 1. Then n² = ___.', '4k² + 4k + 1 = 2(2k² + 2k) + 1', ['4k² + 1 = 2(2k²) + 1', '2k² + 1', '4k² + 2k + 1 = 2(2k² + k) + 1']),
    ('If a | b and b | c, then a | c.', 'b = ar and c = bs for integers r, s. Then c = ___.', 'a(rs), so a | c because rs is an integer', ['r(as), so r | c', 'a + rs, so a | c', 'b(rs), so b | c']),
    ('The sum of a rational number and an integer is rational.', 'Let r = a/b (b ≠ 0) and n an integer. Then r + n = ___.', '(a + nb)/b, a quotient of integers with b ≠ 0', ['(a + n)/b', '(a + n)/(b + 1)', 'a/b + n/1, which is a sum of fractions']),
    ('If n is an integer, then n² + n is even.', 'n² + n = ___.', 'n(n + 1), a product of consecutive integers, one of which is even', ['n(n + 1), which is even because n is even', '2n, which is even', 'n² + n, which is even because n² is even']),
]


def s2(b):
    for L, idx in (('cp2', [0, 2]), ('cp1', [1, 4]), ('honors', [3, 5])):
        for i in idx:
            th, step, good, bad = DP[i]
            b.mc(2, L, 'Theorem: %s\nFill in the missing step of the direct proof:\n%s' % (th, step), good, bad,
                 ['Substitute the definitions and rewrite the expression so the conclusion\'s definition is visible.', 'Correct step: ' + good], 'direct_step')
    ORDER = [('cp2', 'Put the steps of a direct proof of "If n is even, then 3n is even" in order: (A) So 3n = 2(3k). (B) Suppose n is even. (C) Since 3k is an integer, 3n is even. (D) Then n = 2k for some integer k. Answer with the letters, like ABCD.', 'BDAC'),
             ('cp1', 'Order the steps proving "The sum of two odd integers is even": (A) m + n = 2a + 2b + 2 = 2(a + b + 1). (B) Let m and n be odd integers. (C) Since a + b + 1 is an integer, m + n is even. (D) Write m = 2a + 1 and n = 2b + 1. Answer with letters.', 'BDAC'),
             ('honors', 'Order the steps proving "If a | b, then a | b²": (A) So a | b² since kb is an integer. (B) Suppose a | b. (C) Then b² = (ak)b = a(kb). (D) Then b = ak for some integer k. Answer with letters.', 'BDCA')]
    for L, t, a in ORDER:
        b.sa(2, L, t, a, ['A direct proof starts by assuming the hypothesis, uses definitions, does algebra, and ends with the conclusion.', 'Order: ' + a], 'order_steps')
    START = [('cp2', 'If n is odd, then n + 1 is even.', 'Suppose n is an odd integer.', ['Suppose n + 1 is even.', 'Suppose n is even.', 'Let n = 3.']),
             ('cp1', 'For all integers a and b, if a and b are even, then ab is even.', 'Let a and b be any even integers.', ['Let a = 2 and b = 4.', 'Suppose ab is even.', 'Suppose a and b are odd.']),
             ('honors', 'For every rational r, r² is rational.', 'Let r be any rational number, so r = a/b with integers a, b and b ≠ 0.', ['Let r = 1/2.', 'Suppose r² is rational.', 'Suppose r is irrational.'])]
    for L, th, good, bad in START:
        b.mc(2, L, 'How should a direct proof of "%s" begin?' % th, good, bad, ['A direct proof of ∀x (P(x) → Q(x)) starts with a particular but arbitrarily chosen x satisfying P(x).', 'Start: ' + good], 'direct_start')
    b.sel(2, 'cp2', 'Which statements are correct about a direct proof of "If P, then Q"?',
          [('You assume P is true.', True), ('You show Q follows by definitions and algebra.', True), ('You assume Q is true.', False),
           ('You test a few examples.', False), ('You end by stating Q.', True)], ['Assume the hypothesis, reason forward, conclude Q.'], 'direct_select')
    b.sel(2, 'cp1', 'A student writes n = 2k for an even integer n. Which further statements are justified?',
          [('3n = 2(3k), so 3n is even.', True), ('n + 2 = 2(k + 1), so n + 2 is even.', True), ('n² = 4k² = 2(2k²), so n² is even.', True),
           ('n + 1 = 2k + 1 = 2(k + 1), so n + 1 is even.', False), ('n/2 = k, so n/2 is even.', False)],
          ['2k + 1 is odd, not 2(k + 1); k need not be even.'], 'direct_select')
    b.sel(2, 'honors', 'Which are valid conclusions in a direct proof, given m = 2a + 1, n = 2b + 1 for integers a, b?',
          [('m − n = 2(a − b), so m − n is even.', True), ('m + n + 1 = 2(a + b + 1) + 1, so m + n + 1 is odd.', True),
           ('mn = 2(2ab + a + b) + 1, so mn is odd.', True), ('m + n = 2(a + b + 1) + 1, so m + n is odd.', False), ('m² = 2(2a² + 2a), so m² is even.', False)],
          ['Expand each expression carefully.', 'm + n = 2a + 2b + 2 = 2(a + b + 1), which is even; m² = 4a² + 4a + 1, which is odd.'], 'direct_select')
    b.orq(2, 'cp2', 'Prove: "If n is even, then n + 4 is even."',
          [('What do you assume?', 'n is an even integer.'), ('Write n using the definition of even.', 'n = 2k for some integer k.'),
           ('Rewrite n + 4 to show it is even.', 'n + 4 = 2k + 4 = 2(k + 2).'), ('Write the concluding sentence.', 'Since k + 2 is an integer, n + 4 is even.')],
          ['Assume the hypothesis.', 'Definition of even.', 'Factor out 2.', 'State why the result fits the definition.'], 'direct_or')
    b.orq(2, 'cp1', 'Prove: "The product of an even integer and any integer is even."',
          [('State the assumptions with variables.', 'Let m be even and n be any integer.'), ('Use the definition.', 'm = 2k for some integer k.'),
           ('Compute mn.', 'mn = 2kn = 2(kn).'), ('Conclude.', 'kn is an integer, so mn is even.')],
          ['Particular but arbitrary.', 'Even means 2k.', 'Associativity.', 'Closure of integers under multiplication.'], 'direct_or')
    b.orq(2, 'honors', 'Prove: "For all integers a, b, c, if a | b and a | c, then a | (2b − 3c)."',
          [('Translate the hypotheses.', 'b = ar and c = as for some integers r, s.'), ('Substitute into 2b − 3c.', '2b − 3c = 2ar − 3as.'),
           ('Factor.', '2b − 3c = a(2r − 3s).'), ('Conclude, citing the reason.', '2r − 3s is an integer, so a | (2b − 3c).')],
          ['Definition of divides.', 'Substitute.', 'Distributive law.', 'Integers are closed under subtraction and multiplication.'], 'direct_or')


# ---------------------------------------------------------------- 3. existential and universal statements
def s3(b):
    EX = [('cp2', 'There is an even integer that is a perfect square. Which number is a witness?', '16', ['9', '10', '25']),
          ('cp2', 'There is a prime number between 20 and 25. Which number proves it?', '23', ['21', '22', '25']),
          ('cp1', 'There is an integer n such that n² + 3n + 2 = 0. Which value is a witness?', '−1', ['1', '2', '0']),
          ('cp1', 'There are positive integers a, b with a² + b² = 25. Which pair is a witness?', 'a = 3, b = 4', ['a = 2, b = 3', 'a = 5, b = 5', 'a = 1, b = 5']),
          ('honors', 'There is an integer n > 1 that can be written as a sum of two positive cubes in two different ways. Which is a witness?', '1729 = 1³ + 12³ = 9³ + 10³', ['1000 = 10³ + 0³ = 5³ + 5³', '91 = 3³ + 4³', '1729 = 12³ + 1³ only']),
          ('honors', 'There is a rational number between 3/7 and 4/7 whose denominator is 14. Which is a witness?', '7/14', ['1/14', '3/14', '8/14'])]
    checks = {'16': 16 % 2 == 0, '23': isprime(23), '−1': 1 - 3 + 2 == 0, 'a = 3, b = 4': 9 + 16 == 25, '1729 = 1³ + 12³ = 9³ + 10³': 1 + 1728 == 729 + 1000 == 1729, '7/14': Fraction(3, 7) < Fraction(7, 14) < Fraction(4, 7)}
    assert all(checks.values())
    for L, t, good, bad in EX:
        b.mc(3, L, t, good, bad, ['An existential statement is proved by one example (a constructive proof).', 'Witness: ' + good], 'witness')
    METH = [('cp2', '"Every multiple of 4 is even."', 'A general proof for an arbitrary multiple of 4', ['Checking 4, 8 and 12', 'Finding one multiple of 4 that is even', 'Finding one multiple of 4 that is odd']),
            ('cp2', '"Some multiple of 4 is greater than 100."', 'One example, such as 104', ['A general proof for every multiple of 4', 'Checking every multiple of 4', 'A counterexample']),
            ('cp1', 'Disprove: "Every prime is odd."', 'One counterexample: 2', ['A general argument that primes are odd', 'Three examples of odd primes', 'Show that 9 is odd and not prime']),
            ('cp1', 'Disprove: "There is an integer n with n² = 2."', 'A general argument that no integer works', ['One example such as n = 1', 'A counterexample n = 3', 'Checking n = 1, 2, 3']),
            ('honors', '"For every integer n, n² − n is even" over the finite domain {1, 2, 3, 4}.', 'The method of exhaustion: check all four values, or give a general proof', ['One example is enough', 'It cannot be proved over a finite domain', 'A counterexample']),
            ('honors', 'Disprove: "For every real x, there is a real y with y² = x."', 'One counterexample: x = −1', ['A general proof for all x', 'An example x = 4 with y = 2', 'Show that y = √x for every x'])]
    for L, st, good, bad in METH:
        b.mc(3, L, 'What kind of argument is needed? %s' % st, good, bad,
             ['Prove ∀ with a general argument (or exhaustion on a finite domain); prove ∃ with an example. Disprove ∀ with a counterexample; disprove ∃ with a general argument.'], 'method_choice')
    EXH = [('cp2', 'For every n in {1, 2, 3, 4, 5}, n² + n is even.', range(1, 6), lambda n: (n * n + n) % 2 == 0),
           ('cp1', 'For every n in {2, 3, 4, 5, 6, 7}, 2ⁿ > 2n.', range(2, 8), lambda n: 2 ** n > 2 * n),
           ('honors', 'For every n in {1, 2, ..., 9}, n² mod 4 is 0 or 1.', range(1, 10), lambda n: n * n % 4 in (0, 1)),
           ('cp1', 'For every n in {1, 2, 3, 4, 5, 6}, n³ + 2n is divisible by 3.', range(1, 7), lambda n: (n ** 3 + 2 * n) % 3 == 0)]
    for L, st, D, f in EXH:
        bad = [n for n in D if not f(n)]
        b.sa(3, L, 'Use the method of exhaustion. Is the statement true? If false, give the first counterexample; if true, write "true".\n%s' % st, 'true' if not bad else str(bad[0]),
             ['Check every element: ' + ', '.join('%d→%s' % (n, 'T' if f(n) else 'F') for n in D) + '.', 'true' if not bad else 'First counterexample: %d.' % bad[0]], 'exhaustion')
    b.sel(3, 'cp2', 'Which statements can be PROVED by giving one example?',
          [('There is an odd perfect square.', True), ('Some prime is even.', True), ('Every square is even.', False), ('All primes are odd.', False), ('There is a number equal to its own square.', True)],
          ['Existential statements are proved by one example.'], 'method_select')
    b.sel(3, 'cp1', 'Which statements can be DISPROVED by one counterexample?',
          [('Every integer is positive.', True), ('For all real x, x² ≥ x.', True), ('There is an integer n with 2n = 5.', False), ('All squares are rectangles.', False), ('Every prime is less than 100.', True)],
          ['Only false universal statements are disproved by a counterexample; "All squares are rectangles" is true.'], 'method_select')
    b.sel(3, 'honors', 'A student proves "For all integers n, if n is a multiple of 6 then n is even" by writing n = 6k = 2(3k). Which features make this a valid general proof?',
          [('k is an arbitrary integer, not a specific value', True), ('6k = 2(3k) holds for every integer k', True), ('3k is an integer', True),
           ('The proof checked n = 6 and n = 12', False), ('The converse was also proved', False)],
          ['Generalizing from the generic particular: an arbitrary k makes the argument cover every case.'], 'method_select')
    b.orq(3, 'cp2', 'Statement: "There is an integer n such that 3n + 1 = 16."',
          [('Is this a universal or an existential statement?', 'Existential'), ('Find a witness.', '5'),
           ('Check your witness.', '3·5 + 1 = 16'), ('How many examples are needed to prove it?', 'One')],
          ['"There is" is existential.', 'Solve 3n = 15.', 'Substitute.', 'One witness suffices.'], 'existential_or')
    b.orq(3, 'cp1', 'Let S: "For every integer n, n² ≥ n" and T: "There is an integer n such that n² = n."',
          [('Is S true? Explain.', 'True: for n ≤ 0, n² ≥ 0 ≥ n; for n ≥ 1, n² ≥ n.'), ('Is T true? Give a witness.', 'True: n = 0 or n = 1.'),
           ('Is "For every real x, x² ≥ x" true?', 'False: x = 1/2 is a counterexample.'), ('Explain why the domain matters.', 'The real numbers include values between 0 and 1, which integers do not.')],
          ['Divide into cases.', 'One witness.', '(1/2)² = 1/4 < 1/2.', 'Changing the domain changes truth values.'], 'domain_or')
    b.orq(3, 'honors', 'Prove or disprove each statement about integers.',
          [('"There exist integers m, n with 6m + 9n = 1."', 'False: 6m + 9n = 3(2m + 3n) is a multiple of 3, never 1.'),
           ('"There exist integers m, n with 6m + 9n = 3."', 'True: m = −1, n = 1.'),
           ('"For every integer k, there exist integers m, n with 6m + 9n = 3k."', 'True: m = −k, n = k.'),
           ('What do parts (a)–(c) suggest about the values of 6m + 9n?', 'They are exactly the multiples of gcd(6, 9) = 3.')],
          ['Factor out 3.', 'Check −6 + 9 = 3.', 'Scale the witness by k.', 'Bezout-type reasoning.'], 'prove_disprove_or')


# ---------------------------------------------------------------- 4. integers and rationals
def s4(b):
    RAT = [('0.375', '3/8', 'cp2'), ('2.4', '12/5', 'cp2'), ('0.333... (repeating)', '1/3', 'cp1'), ('0.454545... (45 repeating)', '5/11', 'cp1'),
           ('1.2333... (3 repeating)', '37/30', 'honors'), ('0.142857142857... (142857 repeating)', '1/7', 'honors')]
    for d, f, L in RAT:
        b.sa(4, L, 'Write %s as a fraction a/b in lowest terms.' % d, f,
             ['For a repeating decimal x, multiply by a power of 10 to line up the repeating part and subtract.' if 'repeat' in d else 'Write over a power of 10 and reduce.',
              '%s = %s' % (d, f)], 'decimal_to_fraction')
    CLOS = [('cp2', 'The sum of two rational numbers is ...', 'always rational', ['always irrational', 'sometimes rational', 'always an integer']),
            ('cp1', 'The sum of a rational number and an irrational number is ...', 'always irrational', ['always rational', 'sometimes rational', 'always an integer']),
            ('cp1', 'The product of two irrational numbers is ...', 'sometimes rational and sometimes irrational', ['always irrational', 'always rational', 'never an integer']),
            ('honors', 'The product of a nonzero rational number and an irrational number is ...', 'always irrational', ['always rational', 'sometimes rational', 'irrational only if the rational number is an integer']),
            ('cp2', 'The quotient a/b of integers with b ≠ 0 is ...', 'always rational', ['always an integer', 'sometimes irrational', 'always less than 1']),
            ('honors', 'The sum of two irrational numbers is ...', 'sometimes rational and sometimes irrational', ['always irrational', 'always rational', 'rational only if they are equal'])]
    for L, t, good, bad in CLOS:
        b.mc(4, L, t, good, bad, ['Rationals are closed under +, −, ×, and ÷ by nonzero numbers.',
                                  {'always irrational': 'If r + s were rational for rational r and irrational s, then s = (r + s) − r would be rational, a contradiction.' if 'sum' in t else 'If rs = q were rational with r ≠ 0, then s = q/r would be rational.',
                                   'sometimes rational and sometimes irrational': '√2·√2 = 2 is rational but √2·√3 = √6 is not; √2 + (−√2) = 0 is rational but √2 + √2 is not.',
                                   'always rational': 'a/b + c/d = (ad + bc)/(bd).'}[good]], 'closure')
    QR = [(17, 5, 'cp2'), (100, 7, 'cp2'), (-17, 5, 'cp1'), (54, 4, 'cp1'), (-1, 3, 'honors'), (2026, 9, 'honors')]
    for n, d, L in QR:
        q, r = divmod(n, d)
        b.sa(4, L, 'Use the quotient-remainder theorem: find q and r with %d = %d·q + r and 0 ≤ r < %d. Answer as "q = __, r = __".' % (n, d, d), 'q = %d, r = %d' % (q, r),
             ['%d = %d·%d + %d.' % (n, d, q, r), 'The remainder must satisfy 0 ≤ r < %d%s.' % (d, ', so for a negative n the quotient is more negative' if n < 0 else '')], 'quotient_remainder')
    b.sel(4, 'cp2', 'Which numbers are rational?', [('0.25', True), ('−3', True), ('√9', True), ('√2', False), ('π', False)], ['0.25 = 1/4, −3 = −3/1, √9 = 3.', '√2 and π are irrational.'], 'rational_select')
    b.sel(4, 'cp1', 'Which numbers are irrational?', [('√5', True), ('2 + √3', True), ('√16', False), ('0.121212...', False), ('3π', True)], ['A repeating decimal is rational; √16 = 4.', '2 + √3 and 3π are irrational (rational plus/times irrational).'], 'rational_select')
    b.sel(4, 'honors', 'Let r and s be rational with s ≠ 0, and let x be irrational. Which MUST be rational?',
          [('r + s', True), ('r/s', True), ('rs + 1', True), ('r + x', False), ('x²', False)], ['Rationals are closed under +, ×, ÷ by nonzero.', 'x² may be rational (√2) or not (∛2·∛2).'], 'rational_select')
    b.orq(4, 'cp2', 'Let x = 0.777... (7 repeating).',
          [('Write 10x.', '7.777...'), ('Subtract 10x − x.', '9x = 7'), ('Solve for x.', 'x = 7/9'), ('Is x rational? Explain.', 'Yes; it is a quotient of integers with nonzero denominator.')],
          ['Shift the decimal.', 'The repeating parts cancel.', 'Divide by 9.', 'Definition of rational.'], 'repeating_or')
    b.orq(4, 'cp1', 'Prove that the average of two rational numbers is rational.',
          [('Write the two rationals with variables.', 'r = a/b, s = c/d with integers a, b, c, d and b, d ≠ 0.'), ('Write (r + s)/2 as one fraction.', '(ad + bc)/(2bd)'),
           ('Why is the denominator nonzero?', 'b ≠ 0 and d ≠ 0, so 2bd ≠ 0.'), ('Conclude.', 'ad + bc and 2bd are integers, so the average is rational.')],
          ['Definition.', 'Common denominator.', 'Zero product property.', 'Closure of integers.'], 'rational_or')
    b.orq(4, 'honors', 'Use the quotient-remainder theorem with d = 4.',
          [('List the four forms every integer n can take.', '4q, 4q + 1, 4q + 2, 4q + 3'), ('Find n² mod 4 for each form.', '0, 1, 0, 1'),
           ('Conclude a fact about squares.', 'Every perfect square leaves remainder 0 or 1 when divided by 4.'), ('Use it to show 4k + 3 is never a sum of two squares.', 'A sum of two squares leaves remainder 0, 1 or 2 mod 4, never 3.')],
          ['n = 4q + r with r ∈ {0, 1, 2, 3}.', 'Square each and reduce.', 'Division into cases.', '0+0, 0+1, 1+1 give 0, 1, 2.'], 'qr_cases_or')


# ---------------------------------------------------------------- 5. divisibility
def s5(b):
    DIV = [(7, 91, 'cp2'), (6, 84, 'cp2'), (8, 100, 'cp2'), (12, 144, 'cp1'), (-3, 21, 'cp1'), (15, 0, 'honors'), (4, 2026, 'honors')]
    for d, n, L in DIV:
        t = n % d == 0
        b.mc(5, L, 'True or false: %d | %d (that is, %d divides %d).' % (d, n, d, n), 'True' if t else 'False', ['False' if t else 'True', 'Undefined', 'True only if %d < %d' % (d, n)],
             ['d | n means n = dk for some integer k.', '%d = %d · %s' % (n, d, str(n // d)) if t else '%d / %d is not an integer.' % (n, d)], 'divides_check')
    GCD = [(24, 36, 'cp2'), (84, 120, 'cp1'), (391, 299, 'honors'), (1001, 143, 'cp1'), (210, 462, 'honors')]
    for a, c, L in GCD:
        b.sa(5, L, 'Find gcd(%d, %d).' % (a, c), math.gcd(a, c), ['Use prime factorizations or the Euclidean algorithm.', 'gcd = %d' % math.gcd(a, c)], 'gcd')
    PF = [(84, 'cp2'), (360, 'cp1'), (1001, 'honors')]
    for n, L in PF:
        f, m, p = [], n, 2
        while m > 1:
            while m % p == 0:
                f.append(p)
                m //= p
            p += 1
        from collections import Counter
        c = Counter(f)
        ans = ' · '.join(('%d^%d' % (k, v) if v > 1 else str(k)) for k, v in sorted(c.items()))
        b.sa(5, L, 'Write the prime factorization of %d in standard form (primes in increasing order, exponents with ^, factors separated by " · ").' % n, ans,
             ['Divide by the smallest prime repeatedly.', '%d = %s' % (n, ans)], 'prime_factor')
    NDIV = [(36, 'cp2'), (72, 'cp1'), (360, 'honors')]
    for n, L in NDIV:
        k = sum(1 for d in range(1, n + 1) if n % d == 0)
        b.sa(5, L, 'How many positive divisors does %d have?' % n, k, ['From n = p₁^a₁ ··· p_k^a_k, the count is (a₁ + 1)···(a_k + 1).', '%d positive divisors.' % k], 'count_divisors')
    b.sel(5, 'cp2', 'Which numbers divide 60?', [('4', True), ('12', True), ('15', True), ('8', False), ('9', False)], ['60 = 4·15 = 12·5 = 15·4; 60/8 and 60/9 are not integers.'], 'divides_select')
    b.sel(5, 'cp1', 'Suppose a | b and a | c for integers a, b, c. Which MUST be true?',
          [('a | (b + c)', True), ('a | (3b − c)', True), ('a | bc', True), ('b | c', False), ('a | (b + 1)', False)], ['Linear combinations: a | (xb + yc).', 'b | c need not hold (a = 1, b = 2, c = 3).'], 'divides_select')
    b.sel(5, 'honors', 'Which statements are true for ALL integers n?',
          [('2 | n(n + 1)', True), ('3 | n(n + 1)(n + 2)', True), ('6 | n³ − n', True), ('4 | n² + 2', False), ('5 | n⁵ − 1', False)],
          ['Among k consecutive integers one is divisible by k; n³ − n = (n − 1)n(n + 1).', 'n² + 2 is never divisible by 4; n = 5 shows 5 ∤ n⁵ − 1.'], 'divides_select')
    b.orq(5, 'cp1', 'Use the Euclidean algorithm to find gcd(252, 198).',
          [('Divide 252 by 198.', '252 = 198·1 + 54'), ('Divide 198 by 54.', '198 = 54·3 + 36'), ('Continue until the remainder is 0.', '54 = 36·1 + 18; 36 = 18·2 + 0'), ('State the gcd.', '18')],
          ['gcd(a, b) = gcd(b, a mod b).', 'Keep dividing.', 'Stop at remainder 0.', 'The last nonzero remainder is the gcd.'], 'euclid_or')
    b.orq(5, 'cp2', 'Consider 7 | 63.',
          [('What equation shows that 7 divides 63?', '63 = 7·9'), ('Does 63 divide 7?', 'No'), ('Does 7 divide 0? Explain.', 'Yes, 0 = 7·0.'), ('List the positive divisors of 63.', '1, 3, 7, 9, 21, 63')],
          ['d | n means n = dk.', '7 = 63k has no integer solution.', '0 = 7·0.', 'Pair divisors.'], 'divides_or')
    b.orq(5, 'honors', 'Prove the divisibility test: an integer n is divisible by 9 exactly when the sum of its digits is.',
          [('Write a 3-digit number n with digits a, b, c.', 'n = 100a + 10b + c'), ('Rewrite n − (a + b + c).', '99a + 9b = 9(11a + b)'),
           ('Why does this prove the test for 3-digit numbers?', 'n and its digit sum differ by a multiple of 9, so 9 divides one exactly when it divides the other.'), ('Check with 4,815.', 'Digit sum 18; 4815 = 9·535.')],
          ['Place value.', 'Subtract.', 'If 9 | x − y then 9 | x ⟺ 9 | y.', 'Verify.'], 'divisibility_test_or')


# ---------------------------------------------------------------- 6. contradiction
CONTRA = [
    ('There is no greatest integer.', 'Suppose there is a greatest integer N.', ['Suppose every integer is less than N.', 'Suppose N + 1 is the greatest integer.', 'Let N = 1,000,000.']),
    ('√2 is irrational.', 'Suppose √2 is rational, so √2 = a/b in lowest terms.', ['Suppose √2 is irrational.', 'Suppose √2 = 1.414.', 'Suppose a² = 2b² for all integers a, b.']),
    ('There is no least positive rational number.', 'Suppose there is a least positive rational number r.', ['Suppose every rational number is positive.', 'Suppose r = 1/2 is the least.', 'Suppose there is a greatest rational number.']),
    ('The sum of a rational number and an irrational number is irrational.', 'Suppose r is rational, x is irrational, and r + x is rational.', ['Suppose r + x is irrational.', 'Suppose r and x are both rational.', 'Let r = 1 and x = √2.']),
    ('There are infinitely many primes.', 'Suppose there are only finitely many primes p₁, p₂, ..., pₙ.', ['Suppose there are infinitely many primes.', 'Suppose every integer is prime.', 'Suppose 2, 3, 5 are the only primes.']),
    ('No integer is both even and odd.', 'Suppose some integer n is both even and odd.', ['Suppose every integer is even.', 'Suppose n is neither even nor odd.', 'Let n = 2.']),
]


def s6(b):
    for L, idx in (('cp2', [0, 5]), ('cp1', [2, 3]), ('honors', [1, 4])):
        for i in idx:
            th, good, bad = CONTRA[i]
            b.mc(6, L, 'A proof by contradiction of "%s" begins with which assumption?' % th, good, bad,
                 ['Assume the negation of the statement and derive a contradiction.', 'Start: ' + good], 'contra_start')
    FIN = [('cp2', 'Proof that there is no greatest integer: Suppose N is the greatest integer. Then N + 1 is an integer and N + 1 > N. What is the contradiction?', 'N + 1 is greater than the greatest integer N',
            ['N + 1 is not an integer', 'N is negative', 'N + 1 = N']),
           ('cp1', 'Proof that √2 is irrational: √2 = a/b in lowest terms gives a² = 2b², so a is even; a = 2k gives b² = 2k², so b is even. What is the contradiction?', 'a and b are both even, so a/b was not in lowest terms',
            ['a² = 2b² has no solutions', 'b is odd', 'a = b']),
           ('honors', 'Proof that there are infinitely many primes: Let N = p₁p₂···pₙ + 1. Some prime p divides N. Why is this a contradiction?', 'p must be one of p₁, ..., pₙ, but then p divides N − p₁···pₙ = 1, which is impossible',
            ['N is prime, so it is a new prime', 'N is even', 'N is less than pₙ']),
           ('cp1', 'Proof that there is no least positive rational: Suppose r is least. Then r/2 is positive and rational. What is the contradiction?', 'r/2 < r, so r was not the least positive rational', ['r/2 is not rational', 'r/2 > r', 'r is negative'])]
    for L, t, good, bad in FIN:
        b.mc(6, L, t, good, bad, ['A contradiction is a statement that conflicts with an assumption or a known fact.', good], 'contra_finish')
    NEGS = [('cp2', '"n is even"', '"n is odd"'), ('cp1', '"x is irrational"', '"x is rational"'), ('cp2', '"there is no largest even number"', '"there is a largest even number"'),
            ('honors', '"for every integer n, n² + 2 is not divisible by 4"', '"there is an integer n such that n² + 2 is divisible by 4"'),
            ('cp1', '"there are no integers a, b with 6a + 4b = 1"', '"there are integers a, b with 6a + 4b = 1"'),
            ('honors', '"if a² is even then a is even" (as a statement about all integers a)', '"there is an integer a with a² even and a odd"')]
    for L, st, neg in NEGS:
        b.sa(6, L, 'To prove %s by contradiction, what do you assume? Write the assumption in quotation marks.' % st, neg,
             ['Assume the negation of what you want to prove.', 'Assume ' + neg + '.'], 'contra_assume')
    b.sel(6, 'cp1', 'Which are valid "contradictions" that could end a proof by contradiction?',
          [('An integer that is both even and odd', True), ('A fraction in lowest terms whose numerator and denominator are both even', True),
           ('A number that is greater than the greatest number', True), ('A large number', False), ('An example that does not work', False)],
          ['A contradiction must be logically impossible (or conflict with an assumption).'], 'contra_select')
    b.sel(6, 'cp2', 'Which statements are true about proof by contradiction?',
          [('You assume the statement is false.', True), ('You reason until you reach something impossible.', True), ('You test several examples.', False),
           ('The impossibility shows the assumption was wrong.', True), ('You assume the conclusion is true.', False)], ['Assume ¬S, derive c, conclude S.'], 'contra_select')
    b.sel(6, 'honors', 'In proving "√3 is irrational" by contradiction with √3 = a/b in lowest terms, which steps are correct?',
          [('a² = 3b²', True), ('3 | a², so 3 | a', True), ('a = 3k gives 3k² = b², so 3 | b', True), ('a² = 3b² means a is even', False), ('3 | a² does not imply 3 | a', False)],
          ['Because 3 is prime, 3 | a² implies 3 | a.', 'Then 3 divides both a and b, contradicting lowest terms.'], 'contra_select')
    b.orq(6, 'cp2', 'Prove by contradiction: "No odd integer can be written as 2k for an integer k."',
          [('What do you assume?', 'Some odd integer n can be written as 2k.'), ('Write n using the definition of odd.', 'n = 2m + 1 for some integer m.'),
           ('Set the expressions equal and simplify.', '2k = 2m + 1, so 2(k − m) = 1, so k − m = 1/2.'), ('What is the contradiction?', 'k − m is an integer but equals 1/2.')],
          ['Negate the statement.', 'Definition.', 'Solve.', 'Integers are closed under subtraction.'], 'contra_or')
    b.orq(6, 'cp1', 'Prove by contradiction: "If 3n + 2 is odd, then n is odd" (for integers n).',
          [('What do you assume?', '3n + 2 is odd and n is even.'), ('Write n with the definition.', 'n = 2k'), ('Compute 3n + 2.', '6k + 2 = 2(3k + 1), which is even'),
           ('State the contradiction and conclusion.', '3n + 2 is both odd and even, impossible; so n is odd.')],
          ['¬(p → q) ≡ p ∧ ¬q.', 'Even.', 'Factor 2.', 'No integer is both even and odd.'], 'contra_or')
    b.orq(6, 'honors', 'Prove by contradiction: "There are no integers a and b with 18a + 6b = 1."',
          [('What do you assume?', 'There are integers a, b with 18a + 6b = 1.'), ('Factor the left side.', '6(3a + b) = 1'),
           ('What does this say about 1?', '6 divides 1, or 3a + b = 1/6.'), ('State the contradiction.', '3a + b is an integer but equals 1/6 (or 6 ∤ 1).')],
          ['Negate.', 'Common factor 6.', 'Rewrite.', 'Closure of integers.'], 'contra_or')


# ---------------------------------------------------------------- 7. contraposition
CPOS = [
    ('If n² is even, then n is even.', 'If n is odd, then n² is odd.'),
    ('If 3n + 1 is even, then n is odd.', 'If n is even, then 3n + 1 is odd.'),
    ('If n² is odd, then n is odd.', 'If n is even, then n² is even.'),
    ('If xy is irrational, then x or y is irrational.', 'If x and y are both rational, then xy is rational.'),
    ('If a + b ≥ 20, then a ≥ 10 or b ≥ 10.', 'If a < 10 and b < 10, then a + b < 20.'),
    ('If n² − 6n + 5 is even, then n is odd.', 'If n is even, then n² − 6n + 5 is odd.'),
]


def s7(b):
    for L, idx in (('cp2', [0, 2]), ('cp1', [1, 3]), ('honors', [4, 5])):
        for i in idx:
            st, cp = CPOS[i]
            h, c = st[3:].split(', then ')
            conv = 'If %s, then %s' % (c.rstrip('.'), h) + '.'
            b.mc(7, L, 'A proof by contraposition of "%s" proves which statement directly?' % st, cp,
                 [conv, 'If ' + cp[3:].split(', then ')[1].rstrip('.') + ', then ' + cp[3:].split(', then ')[0] + '.', st.replace('If ', 'It is false that if ', 1)],
                 ['Contraposition proves ¬q → ¬p, which is logically equivalent to p → q.', 'Prove: ' + cp], 'contrapos_statement')
    WHY = [('cp2', 'Why does proving "If n is odd, then n² is odd" also prove "If n² is even, then n is even"?', 'They are contrapositives, so they are logically equivalent',
            ['They are converses, so they are equivalent', 'Odd and even are opposites, so any statement about one proves the other', 'It does not; the second needs its own proof']),
           ('cp1', 'A student proves the CONVERSE of "If n² is even, then n is even" instead of the contrapositive. Why does this not prove the statement?', 'A statement and its converse are not logically equivalent',
            ['The converse is false', 'The converse needs a contradiction proof', 'The converse is the same statement']),
           ('honors', 'When is contraposition usually easier than a direct proof?', 'When the negated conclusion gives a usable equation (such as n = 2k + 1) and the hypothesis does not',
            ['When the statement is existential', 'When a counterexample exists', 'When the hypothesis is already an equation'])]
    for L, t, good, bad in WHY:
        b.mc(7, L, t, good, bad, ['p → q ≡ ¬q → ¬p.', good], 'contrapos_why')
    WRITE = [('cp2', 'If 5n + 3 is even, then n is odd.', 'If n is even, then 5n + 3 is odd.'), ('cp1', 'If n³ is even, then n is even.', 'If n is odd, then n³ is odd.'),
             ('honors', 'If ab is even, then a is even or b is even.', 'If a is odd and b is odd, then ab is odd.'), ('cp1', 'If x² < 1, then x < 1.', 'If x ≥ 1, then x² ≥ 1.'),
             ('honors', 'If n is not divisible by 3, then n² is not divisible by 3.', 'If n² is divisible by 3, then n is divisible by 3.'),
             ('cp2', 'If a number is not even, then it is not divisible by 4.', 'If a number is divisible by 4, then it is even.')]
    for L, st, cp in WRITE:
        b.sa(7, L, 'Write the contrapositive of: "%s"' % st, cp, ['Swap the hypothesis and conclusion and negate both (use De Morgan for "or"/"and").', cp], 'contrapos_write',
             notes='Hand-authored contrapositive; checked by hand for correct negation of each part.')
    b.sel(7, 'cp2', 'Which statements are logically equivalent to "If it is a fish, then it swims"?',
          [('If it does not swim, then it is not a fish.', True), ('It is not a fish, or it swims.', True), ('If it swims, then it is a fish.', False),
           ('If it is not a fish, then it does not swim.', False), ('It is a fish only if it swims.', True)], ['Contrapositive, ¬p ∨ q and "only if" are equivalent; converse and inverse are not.'], 'contrapos_select')
    b.sel(7, 'cp1', 'To prove "If n² is a multiple of 3, then n is a multiple of 3" by contraposition, which steps belong?',
          [('Assume n is not a multiple of 3.', True), ('Write n = 3k + 1 or n = 3k + 2.', True), ('Show n² = 3(3k² + 2k) + 1 or 3(3k² + 4k + 1) + 1.', True),
           ('Assume n² is a multiple of 3.', False), ('Check n = 3, 6, 9.', False)], ['Assume ¬q, derive ¬p: n² leaves remainder 1, so it is not a multiple of 3.'], 'contrapos_select')
    b.sel(7, 'honors', 'Which statements could be proved naturally by contraposition?',
          [('If n² is odd, then n is odd.', True), ('If a·b is not divisible by 5, then neither a nor b is divisible by 5.', True), ('If x + y is irrational, then x or y is irrational.', True),
           ('There is an even prime.', False), ('The sum of two even integers is even.', False)], ['Contraposition fits statements whose negated conclusion gives an easy equation.', 'The last two are best proved by example and directly.'], 'contrapos_select')
    b.orq(7, 'cp2', 'Prove by contraposition: "If n + 5 is odd, then n is even."',
          [('Write the contrapositive.', 'If n is odd, then n + 5 is even.'), ('Assume the new hypothesis with the definition.', 'n = 2k + 1'),
           ('Compute n + 5.', '2k + 6 = 2(k + 3), which is even'), ('Why does this prove the original?', 'A statement and its contrapositive are logically equivalent.')],
          ['Swap and negate.', 'Odd.', 'Factor.', 'Equivalence.'], 'contrapos_or')
    b.orq(7, 'cp1', 'Prove by contraposition: "If x is irrational, then x/3 is irrational" (x real).',
          [('Write the contrapositive.', 'If x/3 is rational, then x is rational.'), ('Assume x/3 = a/b with b ≠ 0.', 'x/3 = a/b'),
           ('Solve for x.', 'x = 3a/b'), ('Conclude.', '3a and b are integers with b ≠ 0, so x is rational; therefore the original holds.')],
          ['Swap and negate.', 'Definition of rational.', 'Multiply by 3.', 'Equivalence.'], 'contrapos_or')
    b.orq(7, 'honors', 'Prove by contraposition: "For integers a and b, if a + b is odd, then exactly one of a, b is odd."',
          [('Write the contrapositive.', 'If a and b are both odd or both even, then a + b is even.'), ('Case: both even. Show a + b is even.', '2m + 2n = 2(m + n)'),
           ('Case: both odd. Show a + b is even.', '(2m + 1) + (2n + 1) = 2(m + n + 1)'), ('Explain why the cases are exhaustive.', '"Not exactly one odd" means zero or two are odd.')],
          ['Negate "exactly one".', 'Even plus even.', 'Odd plus odd.', 'Division into cases.'], 'contrapos_or')


# ---------------------------------------------------------------- 8. choosing a strategy
STRAT = [
    ('There is an integer n with n² = n + 6.', 'Constructive proof (give a witness)', 'n = 3 works.'),
    ('For every integer n, n² + n is even.', 'Direct proof (possibly with cases n even, n odd)', 'n(n + 1) is a product of consecutive integers.'),
    ('√5 is irrational.', 'Proof by contradiction', 'Assume √5 = a/b in lowest terms and show 5 divides both a and b.'),
    ('If n² is even, then n is even.', 'Proof by contraposition', 'The contrapositive "if n is odd, then n² is odd" has an easy direct proof.'),
    ('Every prime is odd.', 'Counterexample (it is false)', '2 is prime and even.'),
    ('For every n in {1, 2, 3}, n³ < 3ⁿ⁺¹.', 'Method of exhaustion', 'Check the three values.'),
    ('There are infinitely many primes.', 'Proof by contradiction', 'Assume finitely many and build p₁···pₙ + 1.'),
    ('If a | b and b | c, then a | c.', 'Direct proof', 'Substitute b = ar and c = bs.'),
]
METHODS = ['Direct proof', 'Proof by contradiction', 'Proof by contraposition', 'Counterexample (it is false)', 'Constructive proof (give a witness)', 'Method of exhaustion',
           'Direct proof (possibly with cases n even, n odd)']


def s8(b):
    for L, idx in (('cp2', [0, 4, 5]), ('cp1', [1, 3, 7]), ('honors', [2, 6, 3])):
        for i in idx:
            st, m, why = STRAT[i]
            bad = [x for x in METHODS if x != m and not (m.startswith('Direct') and x.startswith('Direct'))][:3]
            b.mc(8, L, 'Which method is the most natural way to handle this statement?\n"%s"' % st, m, bad, [why], 'choose_method',
                 notes='Hand-authored strategy item: the key names the standard textbook approach; other valid approaches are mentioned in the solution where relevant.')
    TFQ = [('cp2', 'A proof by contradiction assumes the conclusion is false and the hypothesis is true.', 'True', 'For p → q, contradiction assumes p ∧ ¬q.'),
           ('cp1', 'Every statement that can be proved by contraposition can also be proved by contradiction.', 'True', 'Assume p and ¬q, then run the contrapositive argument to get ¬p, contradicting p.'),
           ('honors', 'A universal statement over an infinite domain can be proved by checking enough examples.', 'False', 'Examples never cover every element of an infinite domain.')]
    for L, st, a, why in TFQ:
        b.mc(8, L, 'True or false: %s' % st, a, ['False' if a == 'True' else 'True', 'Only for statements about primes', 'Only when the statement is existential'], [why], 'strategy_fact')
    PIECE = [('cp2', 'A student wants to show "Some perfect squares are odd." What is enough?', 'Show 9 = 3² is odd', ['Show 4 = 2² is even', 'Prove every square is odd', 'Assume no square is odd and find a contradiction using 4']),
             ('cp1', 'To DISPROVE "For all integers a, b, if a² = b² then a = b", what is enough?', 'One pair such as a = 2, b = −2', ['A general proof', 'Show 3² = 3²', 'A proof by contraposition']),
             ('honors', 'To disprove "There is a largest prime", what is needed?', 'A general argument (for example Euclid\'s proof) that for every prime there is a larger one', ['One large prime', 'A counterexample prime', 'Checking primes below 1000'])]
    for L, t, good, bad in PIECE:
        b.mc(8, L, t, good, bad, ['Prove ∃ by example; disprove ∀ by counterexample; disprove ∃ by a general argument.'], 'strategy_piece')
    b.sel(8, 'cp2', 'Which statements can be settled with ONE example or counterexample?',
          [('"All rectangles are squares" (disprove)', True), ('"There is an even prime" (prove)', True), ('"All even numbers are divisible by 2" (prove)', False),
           ('"No integer is both even and odd" (prove)', False), ('"Every odd number is greater than 1" (disprove)', True)], ['Existential claims and false universal claims need one example.'], 'strategy_select')
    b.sel(8, 'cp1', 'Which methods could prove "If n² is odd, then n is odd"?',
          [('Contraposition', True), ('Contradiction', True), ('Checking n = 1, 3, 5', False), ('Direct proof by cases on whether n is even or odd', True), ('One counterexample', False)],
          ['Contraposition and contradiction are standard; a case split (if n were even, n² would be even) also works.'], 'strategy_select')
    b.sel(8, 'honors', 'For which statements is proof by contradiction a natural choice?',
          [('"There is no rational r with r² = 3"', True), ('"There is no largest real number less than 1"', True), ('"7 is prime"', False), ('"The set of primes is infinite"', True), ('"2 + 3 = 5"', False)],
          ['Negative statements ("there is no ...") and infinitude statements suit contradiction.', '7 is prime by exhaustion; 2 + 3 = 5 by computation.'], 'strategy_select')
    b.orq(8, 'cp1', 'For each statement, name a strategy and give the key first step.',
          [('"There is an integer n with 2ⁿ = n²."', 'Witness: n = 2 (or 4).'), ('"For every odd n, n² − 1 is divisible by 8."', 'Direct proof: n = 2k + 1, n² − 1 = 4k(k + 1).'),
           ('"√7 is irrational."', 'Contradiction: assume √7 = a/b in lowest terms.'), ('"For all integers n, n² + 1 is prime."', 'Counterexample: n = 3 gives 10.')],
          ['∃ → example.', 'k(k + 1) is even, so 8 | 4k(k + 1).', 'Contradiction.', 'False universal → counterexample.'], 'strategy_or')
    b.orq(8, 'cp2', 'Statement: "Every multiple of 10 is even."',
          [('Is it universal or existential?', 'Universal'), ('Is it true?', 'True'), ('Which method fits?', 'Direct proof'), ('Write the proof in one line.', 'If n = 10k, then n = 2(5k), so n is even.')],
          ['"Every" is universal.', 'Multiples of 10 end in 0.', 'Assume and compute.', 'Factor 2.'], 'strategy_or')
    b.orq(8, 'honors', 'Statement S: "For every integer n, if n² is divisible by 4, then n is even."',
          [('Write the contrapositive of the conditional.', 'If n is odd, then n² is not divisible by 4.'), ('Prove the contrapositive.', 'n = 2k + 1 gives n² = 4(k² + k) + 1, remainder 1 when divided by 4.'),
           ('Is the converse "if n is even, then 4 | n²" true? Prove or disprove.', 'True: n = 2k gives n² = 4k².'), ('State S together with its converse as a biconditional.', 'For every integer n, 4 | n² if and only if n is even.')],
          ['Swap and negate.', 'Remainder 1.', 'Direct.', 'Both directions proved.'], 'strategy_or')


# ---------------------------------------------------------------- errors
def errors(b):
    E = b.err
    E(1, 'cp2', 'Is "The sum of two primes is even" true?', 'Jordan', ['3 + 5 = 8, 5 + 7 = 12, 11 + 13 = 24. All even, so it is true.'],
      'False (2 + 3 = 5 is odd)', 'Jordan used examples as a proof and missed the even prime 2.', 'One counterexample disproves a universal statement.', ['2 + 3 = 5 is odd.'], 'examples_proof_error')
    E(2, 'cp2', 'Prove: the sum of two even integers is even.', 'Sam', ['Let m = 2k and n = 2k. Then m + n = 4k = 2(2k), which is even.'],
      'Let m = 2a, n = 2b; m + n = 2(a + b), which is even', 'Sam used the same variable k for both numbers, so the proof only covers m = n.', 'Different numbers need different variables.', ['Use m = 2a and n = 2b.'], 'same_variable_error')
    E(4, 'cp2', 'Find q and r with −13 = 4q + r and 0 ≤ r < 4.', 'Riley', ['−13 ÷ 4 = −3 remainder −1, so q = −3 and r = −1.'],
      'q = -4, r = 3', 'Riley allowed a negative remainder. The remainder must satisfy 0 ≤ r < 4.', '−13 = 4(−4) + 3.', ['Choose the quotient so the remainder is between 0 and 3.'], 'negative_remainder_error')
    E(5, 'cp2', 'Does 6 divide 3?', 'Casey', ['3 = 6 · ½, so 6 | 3.'],
      'No', 'Casey used a non-integer multiplier. d | n requires n = dk for an INTEGER k.', '½ is not an integer.', ['3 = 6k has no integer solution.'], 'divides_integer_error')
    E(6, 'cp2', 'Start a proof by contradiction of "There is no largest even integer."', 'Avery', ['Suppose there is no largest even integer.'],
      'Suppose there is a largest even integer N', 'Avery assumed the statement itself instead of its negation.', 'Contradiction starts from the negation.', ['Negate "there is no" to "there is".'], 'contra_assume_error')
    E(7, 'cp2', 'Write the contrapositive of "If n is a multiple of 4, then n is even."', 'Morgan', ['If n is even, then n is a multiple of 4.'],
      'If n is not even, then n is not a multiple of 4.', 'Morgan wrote the converse, which is not equivalent (6 is even but not a multiple of 4).', 'Contrapositive = swap and negate.', ['¬q → ¬p.'], 'contrapos_converse_error')
    E(2, 'cp1', 'Prove: if n is odd, then n² is odd.', 'Taylor', ['Let n = 2k + 1. Then n² = 4k² + 1 = 2(2k²) + 1, which is odd.'],
      'n² = 4k² + 4k + 1 = 2(2k² + 2k) + 1, which is odd', 'Taylor squared incorrectly: (2k + 1)² ≠ 4k² + 1; the middle term 4k is missing.', 'The conclusion is right, but the proof is invalid.', ['(2k + 1)² = 4k² + 4k + 1.'], 'square_binomial_error')
    E(3, 'cp1', 'Prove: "For every integer n, n² − n is even."', 'Jamie', ['n = 3: 9 − 3 = 6 is even. Since 3 was arbitrary, the statement is proved.'],
      'n² − n = n(n − 1), a product of consecutive integers, so it is even', 'Jamie chose a specific value and called it arbitrary. A generic particular must be a variable.', 'Checking n = 3 proves only the case n = 3.', ['Factor n² − n = n(n − 1); one of n, n − 1 is even.'], 'fake_generic_error')
    E(4, 'cp1', 'Is the product of two irrational numbers always irrational?', 'Quinn', ['√2 · √3 = √6 is irrational, so yes.'],
      'No; √2 · √2 = 2 is rational', 'Quinn generalized from one example. One counterexample (√2·√2 = 2) disproves "always".', 'Irrationals are not closed under multiplication.', ['√2·√2 = 2.'], 'irrational_product_error')
    E(5, 'cp1', 'Find gcd(48, 18) with the Euclidean algorithm.', 'Alex', ['48 = 18·2 + 12', '18 = 12·1 + 6', '12 = 6·2 + 0', 'gcd = 0'],
      '6', 'Alex reported the last remainder (0) instead of the last NONZERO remainder.', 'The gcd is the divisor in the final step.', ['The last nonzero remainder is 6.'], 'euclid_last_error')
    E(6, 'cp1', 'Prove √2 is irrational. Suppose √2 = a/b. Then a² = 2b², so a is even, a = 2k, and b² = 2k², so b is even.', 'Jordan', ['Both a and b are even. That is a contradiction.'],
      'The contradiction appears only if a/b was assumed to be in lowest terms', 'Jordan never assumed a/b is in lowest terms, so "both even" contradicts nothing.', 'The contradiction must conflict with an assumption.', ['Assume gcd(a, b) = 1 at the start; then both even contradicts it.'], 'lowest_terms_error')
    E(8, 'cp1', 'Prove or disprove: "There is an integer n with n² = 2n."', 'Sam', ['Suppose n² = 2n. Divide by n: n = 2. Checking all integers is impossible, so it cannot be proved.'],
      'True; n = 2 (or n = 0) is a witness', 'Sam chose the wrong strategy. An existential statement is proved by one witness, and Sam had already found one.', 'Prove ∃ by example.', ['2² = 4 = 2·2.'], 'existential_strategy_error')
    E(7, 'honors', 'Prove: "If n² is even, then n is even" by contraposition.', 'Riley', ['Assume n is even, n = 2k. Then n² = 4k² = 2(2k²) is even. Done.'],
      'Assume n is odd, n = 2k + 1; then n² = 2(2k² + 2k) + 1 is odd', 'Riley proved the converse (if n even then n² even), not the contrapositive.', 'The converse is not equivalent to the statement.', ['Contrapositive: if n is odd then n² is odd.'], 'converse_proof_error')
    E(6, 'honors', 'Prove the sum of a rational r and an irrational x is irrational.', 'Casey', ['Suppose r + x is irrational. Then r + x ≠ a/b. Therefore it is irrational.'],
      'Assume r + x is rational; then x = (r + x) − r is rational, contradicting that x is irrational', 'Casey assumed the conclusion (circular reasoning).', 'A contradiction proof assumes the negation of the conclusion.', ['Assume r + x = c/d is rational.', 'Then x = c/d − a/b = (cb − ad)/(db) is rational.'], 'circular_error')
    E(5, 'honors', 'Prove: if a | bc then a | b or a | c.', 'Avery', ['bc = ak, so a divides bc, so a divides one of the factors.'],
      'False; a = 6, b = 2, c = 3 is a counterexample', 'Avery assumed a property that holds for primes only. A composite a can divide bc without dividing b or c.', 'Euclid\'s lemma requires a to be prime.', ['6 | 6 = 2·3, but 6 ∤ 2 and 6 ∤ 3.'], 'euclid_lemma_error')
    E(1, 'honors', 'Disprove: "For every positive integer n, n² + n + 17 is prime."', 'Morgan', ['n = 3: 9 + 3 + 17 = 29 is prime, so the statement is false.'],
      'n = 16 gives 289 = 17² (n = 17 also works)', 'Morgan gave an example that SUPPORTS the statement, not a counterexample.', 'A counterexample must make the conclusion false.', ['16² + 16 + 17 = 289 = 17².'], 'wrong_counterexample_error')
    E(8, 'honors', 'Prove: "For every real x, if x² > 4, then x > 2."', 'Taylor', ['By contraposition: if x ≤ 2 then x² ≤ 4. Since x ≤ 2, x² ≤ 2² = 4.'],
      'False; x = −3 is a counterexample', 'Taylor squared an inequality with possibly negative x; x ≤ 2 does not imply x² ≤ 4. The statement is false.', 'Check whether a statement is true before choosing a proof method.', ['(−3)² = 9 > 4 but −3 < 2.'], 'false_statement_error')
    E(3, 'honors', 'Prove: "There is a rational number between any two distinct rational numbers r < s."', 'Jamie', ['Take r = 1 and s = 2. Then 1.5 is between them and is rational.'],
      'For any r < s, (r + s)/2 is rational and r < (r + s)/2 < s', 'Jamie proved one case. The statement is universal in r and s, so the witness must depend on arbitrary r and s.', 'A universal-existential statement needs a general construction.', ['(r + s)/2 is rational by closure.', 'r < (r + s)/2 < s since r < s.'], 'specific_case_error')


def topup(b):
    need = lambda k, L: b.counter.get((k, L), 0) < 10
    # 1: classify integers (computed)
    for n, L in ((51, 'cp2'), (53, 'cp1'), (87, 'cp1'), (143, 'honors'), (-4, 'cp2'), (199, 'honors')):
        if not need(1, L):
            continue
        if n < 0:
            good, opts = 'Even', ['Odd', 'Neither even nor odd', 'Both even and odd']
            why = '%d = 2(%d).' % (n, n // 2)
        else:
            good = 'Prime' if isprime(n) else 'Composite'
            opts = [o for o in ['Prime', 'Composite', 'Neither prime nor composite', 'Both prime and composite'] if o != good]
            d = next((k for k in range(2, n) if n % k == 0), None)
            why = 'No prime up to √%d divides it.' % n if d is None else '%d = %d · %d.' % (n, d, n // d)
        b.mc(1, L, 'Classify the integer %d.' % n, good, opts, [why], 'classify_integer')
    # 2: parity of an expression (rewrites checked numerically)
    PAR = [('cp2', 'n is even, n = 2k', 'n + 6', '2(k + 3)', 'even', lambda k: 2 * k + 6, lambda k: 2 * (k + 3)),
           ('cp2', 'n is odd, n = 2k + 1', 'n + 2', '2(k + 1) + 1', 'odd', lambda k: 2 * k + 3, lambda k: 2 * (k + 1) + 1),
           ('cp2', 'n is odd, n = 2k + 1', '3n', '2(3k + 1) + 1', 'odd', lambda k: 3 * (2 * k + 1), lambda k: 2 * (3 * k + 1) + 1),
           ('cp1', 'n is odd, n = 2k + 1', 'n² + n', '2(2k² + 3k + 1)', 'even', lambda k: (2 * k + 1) ** 2 + 2 * k + 1, lambda k: 2 * (2 * k * k + 3 * k + 1)),
           ('cp1', 'n is even, n = 2k', 'n² + 3', '2(2k² + 1) + 1', 'odd', lambda k: 4 * k * k + 3, lambda k: 2 * (2 * k * k + 1) + 1),
           ('cp1', 'n is odd, n = 2k + 1', '5n + 3', '2(5k + 4)', 'even', lambda k: 5 * (2 * k + 1) + 3, lambda k: 2 * (5 * k + 4)),
           ('honors', 'n is odd, n = 2k + 1', 'n³', '2(4k³ + 6k² + 3k) + 1', 'odd', lambda k: (2 * k + 1) ** 3, lambda k: 2 * (4 * k ** 3 + 6 * k * k + 3 * k) + 1),
           ('honors', 'm = 2a + 1 and n = 2b are integers', 'm² + n²', '2(2a² + 2a + 2b²) + 1', 'odd', lambda a: (2 * a + 1) ** 2 + 4 * a * a, lambda a: 2 * (2 * a * a + 2 * a + 2 * a * a) + 1),
           ('honors', 'n is odd, n = 2k + 1', 'n² − 1', '4k(k + 1) = 8·[k(k + 1)/2]', 'divisible by 8', lambda k: (2 * k + 1) ** 2 - 1, lambda k: 4 * k * (k + 1)),
           ('cp1', 'n is even, n = 2k', 'n² − n', '2(2k² − k)', 'even', lambda k: 4 * k * k - 2 * k, lambda k: 2 * (2 * k * k - k))]
    for L, given, expr, form, kind, f, g in PAR:
        assert all(f(k) == g(k) for k in range(-6, 7)), expr
        if not need(2, L):
            continue
        good = '%s = %s, so it is %s' % (expr, form, kind)
        alt = 'odd' if kind == 'even' else 'even'
        bad = ['%s = %s, so it is %s' % (expr, form, alt), '%s is %s because n is %s' % (expr, alt, 'odd' if 'odd' in given else 'even'), 'It cannot be decided without a value of k']
        b.mc(2, L, 'In a direct proof, suppose %s. Which line correctly finishes the argument about %s?' % (given, expr), good, bad,
             ['Substitute and factor so the definition of even (2·integer) or odd (2·integer + 1) is visible.', good + '.'], 'direct_parity',
             notes='The rewritten form was checked equal to the expression for k = −6..6 by the authoring script.')
    # 3: smallest witness (computed by search)
    WIT = [('cp2', 'n² > 50', lambda n: n * n > 50), ('cp2', '3n − 7 > 20', lambda n: 3 * n - 7 > 20), ('cp1', '2ⁿ > n³', lambda n: 2 ** n > n ** 3 and n > 1),
           ('cp1', 'n! > 1000', lambda n: math.factorial(n) > 1000), ('honors', 'n² + 1 is divisible by 5 and n > 5', lambda n: (n * n + 1) % 5 == 0 and n > 5), ('cp2', 'n² − 4n = 12', lambda n: n * n - 4 * n == 12)]
    for L, cond, f in WIT:
        if not need(3, L):
            continue
        w = next(n for n in range(1, 200) if f(n))
        b.sa(3, L, 'Prove the existential statement "There is a positive integer n such that %s" by finding the SMALLEST witness n.' % cond, w,
             ['Test n = 1, 2, 3, ... until the condition holds.', 'Smallest witness: n = %d.' % w], 'smallest_witness')
    # 4: rational arithmetic closure (computed with Fraction)
    RA = [('cp2', Fraction(1, 2), Fraction(1, 3), '+'), ('cp1', Fraction(2, 3), Fraction(-5, 4), '×'), ('honors', Fraction(7, 6), Fraction(-3, 10), '−'), ('cp1', Fraction(5, 8), Fraction(3, 4), '÷')]
    for L, x, y, op in RA:
        if not need(4, L):
            continue
        r = {'+': x + y, '−': x - y, '×': x * y, '÷': x / y}[op]
        fs = lambda q: '%d/%d' % (q.numerator, q.denominator) if q.denominator != 1 else str(q.numerator)
        b.sa(4, L, 'Rationals are closed under %s. Compute %s %s %s and write the result as a fraction a/b in lowest terms.' % ({'+': 'addition', '−': 'subtraction', '×': 'multiplication', '÷': 'division by a nonzero number'}[op], fs(x), op, '(' + fs(y) + ')' if y < 0 else fs(y)), fs(r),
             ['Use a common denominator (or multiply numerators and denominators).', 'Result: %s, again a quotient of integers.' % fs(r)], 'rational_arith')
    # 5: lcm and divides (computed)
    for L, a, c in (('cp2', 6, 8), ('cp1', 18, 30), ('honors', 84, 90), ('cp2', 9, 12)):
        if need(5, L):
            l = a * c // math.gcd(a, c)
            b.sa(5, L, 'Find lcm(%d, %d).' % (a, c), l, ['lcm(a, b) = ab / gcd(a, b).', '%d·%d / %d = %d' % (a, c, math.gcd(a, c), l)], 'lcm')
    # 6: more contradiction setups (assume statements)
    MORE6 = [('cp2', '"there is no smallest positive real number"', '"there is a smallest positive real number"'),
             ('cp2', '"7 is not a perfect square"', '"7 is a perfect square"'),
             ('cp1', '"no integer is both a multiple of 4 and odd"', '"some integer is both a multiple of 4 and odd"'),
             ('honors', '"log₂ 3 is irrational"', '"log₂ 3 is rational"'),
             ('honors', '"for all integers a, b, a² − 4b ≠ 2"', '"there are integers a, b with a² − 4b = 2"')]
    for L, st, neg in MORE6:
        if need(6, L):
            b.sa(6, L, 'To prove %s by contradiction, what do you assume? Write the assumption in quotation marks.' % st, neg, ['Assume the negation of the statement.', 'Assume ' + neg + '.'], 'contra_assume')
    # 7: more contrapositives
    MORE7 = [('cp2', 'If it is a weekend, then I sleep late.', 'If I do not sleep late, then it is not a weekend.'),
             ('cp2', 'If n is a multiple of 6, then n is a multiple of 3.', 'If n is not a multiple of 3, then n is not a multiple of 6.'),
             ('cp1', 'If x + y > 10, then x > 5 or y > 5.', 'If x ≤ 5 and y ≤ 5, then x + y ≤ 10.'),
             ('cp1', 'If n² + 1 is odd, then n is even.', 'If n is odd, then n² + 1 is even.'),
             ('honors', 'If a and b are rational, then a + b is rational.', 'If a + b is irrational, then a is irrational or b is irrational.'),
             ('cp1', 'If 4 ∤ n², then n is odd.', 'If n is even, then 4 | n².')]
    for L, st, cp in MORE7:
        if need(7, L):
            b.sa(7, L, 'Write the contrapositive of: "%s"' % st, cp, ['Swap and negate both parts.', cp], 'contrapos_write', notes='Hand-authored contrapositive; negations checked by hand.')
    # 8: more method choices
    MORE8 = [('cp2', 'There is a multiple of 7 between 50 and 60.', 'Constructive proof (give a witness)', '56 = 7·8.'),
             ('cp2', 'For every n in {2, 4, 6}, n² is even.', 'Method of exhaustion', 'Check 4, 16, 36.'),
             ('cp1', 'Every square number is either a multiple of 3 or one more than a multiple of 3.', 'Direct proof (possibly with cases n even, n odd)', 'Cases n = 3k, 3k + 1, 3k + 2.'),
             ('cp1', 'If n³ is odd, then n is odd.', 'Proof by contraposition', 'If n is even, n³ = 8k³ is even.'),
             ('honors', 'There is no integer solution to x² − y² = 10.', 'Proof by contradiction', '(x − y)(x + y) = 10 forces factors of equal parity, but 10 = 2·5 has one even and one odd factor in every factorization.'),
             ('cp2', 'All prime numbers are less than 1000.', 'Counterexample (it is false)', '1009 is prime.')]
    for L, st, m, why in MORE8:
        if need(8, L):
            bad = [x for x in METHODS if x != m and not (m.startswith('Direct') and x.startswith('Direct'))][:3]
            b.mc(8, L, 'Which method is the most natural way to handle this statement?\n"%s"' % st, m, bad, [why], 'choose_method',
                 notes='Hand-authored strategy item: the key names the standard approach.')


def topup2(b):
    b.mc(2, 'honors', 'Theorem: "If a | b and a | c, then a² | bc." After writing b = ar and c = as, which line completes a direct proof?',
         'bc = (ar)(as) = a²(rs), and rs is an integer', ['bc = a(r + s), so a² | bc', 'bc = a²rs only when r = s', 'bc = ar + as = a(r + s)'],
         ['Multiply the two expressions.', 'bc = a²(rs) with rs an integer, so a² | bc.'], 'direct_step')
    b.sa(3, 'honors', 'Prove "There exist distinct positive integers a < b with aᵇ = bᵃ" by giving the witness with the smallest a. Answer as "a = __, b = __".', 'a = 2, b = 4',
         ['Search small pairs: 2⁴ = 16 = 4².', 'a = 2, b = 4 (this is the only such pair of distinct positive integers).'], 'smallest_witness')
    b.sa(4, 'honors', 'Find q and r with 7 = (−3)q + r and 0 ≤ r < 3 (the divisor is −3, so the remainder rule is 0 ≤ r < |−3|). Answer as "q = __, r = __".', 'q = -2, r = 1',
         ['7 = (−3)(−2) + 1.', 'The remainder 1 satisfies 0 ≤ r < 3.'], 'quotient_remainder')
    b.sa(7, 'honors', 'Write the contrapositive of: "If n is prime and n > 2, then n is odd."', 'If n is even, then n is not prime or n ≤ 2.',
         ['¬(p ∧ q) ≡ ¬p ∨ ¬q.', 'If n is even, then n is not prime or n ≤ 2.'], 'contrapos_write', notes='Hand-authored contrapositive; negations checked by hand.')
    b.mc(8, 'honors', 'Which method is the most natural way to handle this statement?\n"For every integer n ≥ 1, the number n⁵ − n is divisible by 5."', 'Direct proof (possibly with cases n even, n odd)',
         ['Counterexample (it is false)', 'Method of exhaustion', 'Constructive proof (give a witness)'],
         ['A direct proof by cases on n mod 5 (n = 5k, 5k ± 1, 5k ± 2), or factoring n⁵ − n = n(n − 1)(n + 1)(n² + 1).', 'Exhaustion cannot cover infinitely many n.'], 'choose_method',
         notes='Hand-authored strategy item; the case split is on remainders mod 5.')


def topup3(b):
    b.mc(8, 'honors', 'Which method is the most natural way to handle this statement?\n"There is no integer n such that n² ≡ 2 (mod 3)."', 'Direct proof (possibly with cases n even, n odd)',
         ['Counterexample (it is false)', 'Constructive proof (give a witness)', 'Method of exhaustion'],
         ['Check the three cases n ≡ 0, 1, 2 (mod 3): n² ≡ 0, 1, 1. A finite case split on remainders covers every integer (the statement is about infinitely many n, so plain exhaustion of examples does not work).'], 'choose_method',
         notes='Hand-authored strategy item; the case split is on remainders mod 3.')


def topup4(b):
    M6 = [('cp2', 'A proof by contradiction of "√5 is irrational" reaches the line "a and b are both divisible by 5". Why does that finish the proof?', 'It contradicts the assumption that a/b is in lowest terms',
           ['It shows √5 = 5', 'It proves a = b', 'It is a counterexample']),
          ('honors', 'To prove "there is no integer n with n² = 4n + 2" by contradiction, which assumption starts the proof?', 'Suppose some integer n satisfies n² = 4n + 2',
           ['Suppose no integer n satisfies n² = 4n + 2', 'Let n = 2', 'Suppose n² = 4n + 2 for every integer n'])]
    for L, t, good, bad in M6:
        b.mc(6, L, t, good, bad, ['Contradiction: assume the negation and derive an impossibility.', good], 'contra_mc')
    M7 = [('cp2', 'Which statement is the contrapositive of "If n is a multiple of 10, then n is even"?', 'If n is not even, then n is not a multiple of 10',
           ['If n is even, then n is a multiple of 10', 'If n is not a multiple of 10, then n is not even', 'n is a multiple of 10 and n is not even']),
          ('cp1', 'Which statement is the contrapositive of "If x² ≠ 9, then x ≠ 3"?', 'If x = 3, then x² = 9', ['If x ≠ 3, then x² ≠ 9', 'If x² = 9, then x = 3', 'If x = 3, then x² ≠ 9']),
          ('honors', 'Which statement is the contrapositive of "If ab is odd, then a and b are both odd"?', 'If a is even or b is even, then ab is even',
           ['If a and b are both even, then ab is even', 'If a and b are both odd, then ab is odd', 'If ab is even, then a or b is even'])]
    for L, t, good, bad in M7:
        b.mc(7, L, t, good, bad, ['Swap and negate; De Morgan turns "both odd" into "a is even or b is even".', good], 'contrapos_mc')
