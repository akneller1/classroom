"""Unit 1: Speaking Mathematically (7 skills)."""
import itertools
from core import Bank, fmt_set, fmt_el, seeded

U = 'speaking-mathematically'


def build():
    b = Bank(U, 'sm', 7)
    s1(b); s2(b); s3(b); s4(b); s5(b); s6(b); s7(b)
    extra567(b)
    errors(b)
    return b


# ---------------------------------------------------------------- skill 1: variables and statements
OPEN = [  # (display, predicate)
    ('n² − 3n = 10', lambda n: n * n - 3 * n == 10),
    ('n² = 2n + 8', lambda n: n * n == 2 * n + 8),
    ('3n − 4 > 5', lambda n: 3 * n - 4 > 5),
    ('n² < 10', lambda n: n * n < 10),
    ('2n + 1 is a multiple of 3', lambda n: (2 * n + 1) % 3 == 0),
    ('n² + n is even', lambda n: (n * n + n) % 2 == 0),
    ('n³ = n', lambda n: n ** 3 == n),
    ('|n − 2| ≤ 1', lambda n: abs(n - 2) <= 1),
    ('n² − 5n + 6 = 0', lambda n: n * n - 5 * n + 6 == 0),
    ('5 − n > n', lambda n: 5 - n > n),
]
DOMS = [list(range(-3, 6)), list(range(0, 8)), list(range(-4, 5)), list(range(1, 10))]

TRUTH_OF = {0: 'true', 1: 'false', 5: 'true', 6: 'false', 8: 'true', 11: 'false'}
STATEMENTS = [  # (sentence, is_statement, reason)
    ('17 is a prime number.', True, 'It is a declarative sentence that is true.'),
    ('12 is an odd number.', True, 'It is a declarative sentence that is false; false sentences are still statements.'),
    ('Is 91 prime?', False, 'A question is neither true nor false.'),
    ('Add 7 to both sides.', False, 'A command is neither true nor false.'),
    ('x + 5 = 9', False, 'Its truth depends on the value of x, so it is an open sentence (a predicate), not a statement.'),
    ('For every real number x, x + 0 = x.', True, 'The variable is quantified, so the sentence has a definite truth value (true).'),
    ('There is an integer n with 2n = 7.', True, 'The variable is quantified; the sentence is false because 7/2 is not an integer.'),
    ('n is divisible by 4', False, 'Its truth depends on n.'),
    ('The sum of two even integers is even.', True, 'It is a true declarative sentence (a theorem).'),
    ('This sentence is false.', False, 'It cannot consistently be true or false (the liar paradox).'),
    ('Please simplify 3(x + 2).', False, 'A request or command has no truth value.'),
    ('0 is greater than 1.', True, 'A false declarative sentence is a statement.'),
]

TRANSL = [  # (english, variable form, distractors)
    ('Is there a number whose square equals the number itself plus 6?',
     'Is there a number x such that x² = x + 6?',
     ['Is there a number x such that x² + 6 = 0?', 'For every number x, x² = x + 6.', 'Is there a number x such that 2x = x + 6?']),
    ('Every real number has a real number that is larger than it.',
     'For every real number x, there is a real number y such that y > x.',
     ['There is a real number y such that for every real number x, y > x.', 'For every real number x, x > y.', 'There is a real number x such that x > x.']),
    ('No integer is both even and odd.',
     'For every integer n, n is not both even and odd.',
     ['There is an integer n that is even and odd.', 'For every integer n, n is even and n is odd.', 'For every integer n, n is neither even nor odd.']),
    ('Given any positive number, there is a smaller positive number.',
     'For every positive number r, there is a positive number s such that s < r.',
     ['There is a positive number s such that s < r for every positive number r.', 'For every positive number r, r < 0.', 'There is a positive number r with r < r.']),
    ('Is there an integer that leaves remainder 1 when divided by 2 and by 3?',
     'Is there an integer n such that n mod 2 = 1 and n mod 3 = 1?',
     ['Is there an integer n such that n mod 6 = 2?', 'For every integer n, n mod 2 = 1 or n mod 3 = 1.', 'Is there an integer n such that n mod 2 = 1 or n mod 3 = 1?']),
    ('Every even integer greater than 2 can be written as a sum of two primes.',
     'For every even integer n > 2, there are primes p and q such that n = p + q.',
     ['There are primes p and q such that for every even integer n > 2, n = p + q.', 'For every integer n > 2, n = p + q.', 'There is an even integer n > 2 with n = p + q for primes p and q.']),
]


def s1(b):
    for L in ('cp2', 'cp1', 'honors'):
        # A. statement or not (MC, four-way classification)
        picks = {'cp2': [0, 2, 4, 3], 'cp1': [5, 7, 1, 10], 'honors': [9, 6, 8, 11]}[L]
        for i in picks[:3]:
            s, isst, why = STATEMENTS[i]
            hint = ' (A statement is a sentence that is true or false, but not both.)' if L == 'cp2' else ''
            if isst:
                truth = TRUTH_OF[i]
                good = 'A statement that is %s' % truth
            elif s.endswith('?') or s.startswith(('Add', 'Please')):
                good = 'Not a statement: it is a question or a command'
            elif 'false' in s:
                good = 'Not a statement: it cannot be consistently true or false'
            else:
                good = 'Not a statement: its truth depends on the value of a variable'
            allopts = ['A statement that is true', 'A statement that is false', 'Not a statement: it is a question or a command',
                       'Not a statement: its truth depends on the value of a variable', 'Not a statement: it cannot be consistently true or false']
            b.mc(1, L, 'Classify the sentence.%s\n"%s"' % (hint, s), good, [o for o in allopts if o != good][:3] if i != 9 else
                 ['A statement that is true', 'A statement that is false', 'Not a statement: its truth depends on the value of a variable'],
                 [why], 'statement_or_not')
        # B. solve an open sentence over a finite domain (short answer, computed)
        for k in {'cp2': [0, 3, 8], 'cp1': [1, 4, 6], 'honors': [5, 7, 9]}[L]:
            disp, f = OPEN[k]
            D = DOMS[k % len(DOMS)]
            sol = [n for n in D if f(n)]
            b.sa(1, L, 'Let the domain be D = %s. Find the truth set of the open sentence "%s", that is, the set of all n in D that make it true. Write the set in roster notation with elements in increasing order (write ∅ if empty).' % (fmt_set(D), disp),
                 fmt_set(sol),
                 ['Test each element of D: ' + '; '.join('n = %d → %s' % (n, 'true' if f(n) else 'false') for n in D) + '.',
                  'The truth set is %s.' % fmt_set(sol)], 'truth_set')
        # C. translate with variables (MC)
        for k in {'cp2': [0, 4], 'cp1': [1, 2], 'honors': [3, 5]}[L]:
            e, good, bad = TRANSL[k]
            b.mc(1, L, 'Which sentence uses variables to say the same thing as: "%s"' % e, good, bad,
                 ['Introduce a variable for each object being discussed and keep the quantifier words (every, there is) in the same order as the English sentence.',
                  'Correct form: ' + good], 'translate_variables')
        # D. select-all statements
        sets = {'cp2': [0, 1, 2, 4, 6], 'cp1': [3, 5, 6, 7, 9], 'honors': [5, 8, 9, 10, 11, 4]}[L]
        opts = [(STATEMENTS[i][0], STATEMENTS[i][1]) for i in sets]
        b.sel(1, L, 'Which of these sentences are statements (true or false, but not both)?', opts,
              ['%s → %s %s' % (STATEMENTS[i][0], 'statement.' if STATEMENTS[i][1] else 'not a statement.', STATEMENTS[i][2]) for i in sets],
              'statement_select')
        # E. open response (all levels; cp2 scaffolded)
        if L == 'cp2':
            D = list(range(0, 7)); f = lambda n: n * n - 6 * n + 8 == 0
            sol = [n for n in D if f(n)]
            b.orq(1, L, 'Consider the open sentence P(n): "n² − 6n + 8 = 0" with domain D = {0, 1, 2, 3, 4, 5, 6}.',
                  [('Is P(n) a statement? Explain in one sentence.', 'No. Its truth value depends on n, so it is an open sentence.'),
                   ('Is P(3) true or false? Show the substitution.', 'False: 9 − 18 + 8 = −1 ≠ 0'),
                   ('Find the truth set of P(n) in D.', fmt_set(sol)),
                   ('Write the statement "There is an n in D such that P(n)" and give its truth value.', 'True, because P(2) is true (also P(4)).')],
                  ['P(n) has a variable that is not quantified, so it is not yet a statement.', 'P(3): 9 − 18 + 8 = −1, false.',
                   'Testing 0 through 6 gives P(2) and P(4) true.', 'An existential statement is true when at least one element of D works.'],
                  'open_sentence_or')
        elif L == 'cp1':
            b.orq(1, L, 'A club rule says: "Every member has a partner who is in the same grade." Let M be the set of members.',
                  [('Rewrite the rule using variables x and y.', 'For every member x in M, there is a member y in M with y ≠ x such that y is in the same grade as x.'),
                   ('Why is "y ≠ x" needed?', 'Otherwise every member could be their own partner, and the rule would say nothing.'),
                   ('M has 5 members: grades 9, 9, 10, 11, 11. Is the rule true? Explain.', 'False: the grade-10 member has no other member in grade 10.'),
                   ('Change one member\'s grade so that the rule becomes true.', 'For example, change the grade-10 member to grade 9 (grades 9, 9, 9, 11, 11).')],
                  ['A rule about "every member" becomes "for every x"; "has a partner" becomes "there is a y".',
                   'Without y ≠ x the rule is automatically true because x is in the same grade as itself.',
                   'One counterexample (the only grade-10 member) makes a universal statement false.',
                   'Any change that leaves no grade with exactly one member works.'], 'rule_variables_or')
        else:
            b.orq(1, L, 'Let P(n) be "n² + n + 41 is prime", with domain the nonnegative integers.',
                  [('Find P(0), P(1), P(2) and P(3) (true or false).', 'All true: 41, 43, 47, 53 are prime.'),
                   ('Is P(40) true? Show a factorization.', 'False: 40² + 40 + 41 = 1681 = 41²'),
                   ('Is P(41) true? Factor 41² + 41 + 41.', 'False: 41² + 41 + 41 = 41·43 = 1763'),
                   ('Explain why checking P(0) through P(39) cannot prove "For every n ≥ 0, P(n)".', 'Examples never prove a universal statement over an infinite domain, and here the statement is false (n = 40 is a counterexample).')],
                  ['0+0+41=41, 1+1+41=43, 4+2+41=47, 9+3+41=53, all prime.', '1600+40+41=1681=41·41.',
                   '41²+41+41 = 41(41+1+1) = 41·43.', 'One counterexample disproves a universal statement; finitely many examples never prove one about infinitely many n.'],
                  'euler_poly_or')
        # F. extra truth-value-with-domain MC to reach 10
        extra = {'cp2': [(OPEN[8], list(range(0, 5)), 'exists')],
                 'cp1': [(OPEN[2], list(range(0, 4)), 'forall'), (OPEN[5], list(range(-3, 4)), 'forall')],
                 'honors': [(OPEN[6], list(range(-2, 3)), 'forall'), (OPEN[1], list(range(0, 4)), 'exists')]}[L]
        for (disp, f), D, q in extra:
            val = all(f(n) for n in D) if q == 'forall' else any(f(n) for n in D)
            word = 'For every' if q == 'forall' else 'There exists'
            st = '%s n in %s, %s.' % (word, fmt_set(D), disp)
            good_n = [n for n in D if f(n)]
            bad_n = [n for n in D if not f(n)]
            if q == 'forall':
                good = 'True: every element of the domain works' if val else 'False: n = %d is a counterexample' % bad_n[0]
                if good_n:
                    opts = ['True: it works for n = %d and n = %d' % tuple(good_n[:2]) if len(good_n) >= 2 else 'True: it works for n = %d' % good_n[0],
                            'False: n = %d is a counterexample' % good_n[0], 'Not a statement, because it contains the variable n']
                else:
                    opts = ['True: no counterexample is listed', 'False: only some elements fail', 'Not a statement, because it contains the variable n']
            else:
                good = 'True: n = %d is a witness' % good_n[0] if val else 'False: no element of the domain works'
                opts = ['False: n = %d does not work' % bad_n[0], 'True: n = %d is a witness' % bad_n[0], 'Not a statement, because it contains the variable n']
            b.mc(1, L, 'Is this statement true or false?\n%s' % st, good, opts,
                 ['Check every element of the finite domain: ' + ', '.join('%d→%s' % (n, 'T' if f(n) else 'F') for n in D) + '.',
                  ('A "for every" statement needs every element to work; examples alone are not enough. ' if q == 'forall' else 'A "there exists" statement needs just one element that works. ') +
                  'The variable n is quantified, so this is a statement.', good],
                 'domain_truth')
        while b.counter.get((1, L), 0) < 10:
            k = b.counter.get((1, L), 0)
            disp, f = OPEN[(k + 2) % len(OPEN)]
            D = list(range(-2, 4))
            b.sa(1, L, 'With domain D = %s, how many elements of D make "%s" true?' % (fmt_set(D), disp),
                 sum(1 for n in D if f(n)), ['Test each n: ' + ', '.join('%d→%s' % (n, 'T' if f(n) else 'F') for n in D) + '.',
                                             'Count the T values: %d.' % sum(1 for n in D if f(n))], 'truth_count')


# ---------------------------------------------------------------- skill 2: universal and existential statements
QSTAT = [  # (statement, truth, explanation, negation)
    ('For every integer n, n² ≥ n.', True, 'If n ≤ 0 then n² ≥ 0 ≥ n; if n ≥ 1 then n² = n·n ≥ n.', 'There is an integer n such that n² < n.'),
    ('For every real number x, x² ≥ x.', False, 'Counterexample x = 1/2: (1/2)² = 1/4 < 1/2.', 'There is a real number x such that x² < x.'),
    ('There is a real number x such that x² = −1.', False, 'Squares of real numbers are never negative.', 'For every real number x, x² ≠ −1.'),
    ('There is an integer n such that n² = 2n.', True, 'n = 0 or n = 2 works.', 'For every integer n, n² ≠ 2n.'),
    ('For every positive integer n, n + 1 > n.', True, 'Adding 1 always makes a number larger.', 'There is a positive integer n such that n + 1 ≤ n.'),
    ('Every prime number is odd.', False, 'Counterexample: 2 is prime and even.', 'There is a prime number that is not odd.'),
    ('There is a positive integer that is less than every other positive integer.', True, '1 is the least positive integer.', 'For every positive integer m, there is another positive integer that is less than or equal to m.'),
    ('For every real number x, if x > 2 then x² > 4.', True, 'If x > 2 > 0 then x² > 2x > 4.', 'There is a real number x such that x > 2 and x² ≤ 4.'),
    ('For every real number x, if x² > 4 then x > 2.', False, 'Counterexample x = −3: x² = 9 > 4 but x < 2.', 'There is a real number x such that x² > 4 and x ≤ 2.'),
    ('There is an integer that is both even and prime.', True, '2 is even and prime.', 'Every integer is not even or not prime.'),
]

NEG_ITEMS = [  # (statement, correct negation, distractors)
    ('All dogs are friendly.', 'Some dog is not friendly.', ['No dogs are friendly.', 'All dogs are unfriendly.', 'Some dogs are friendly.']),
    ('Some students passed the test.', 'No student passed the test.', ['Some students did not pass the test.', 'All students passed the test.', 'Not all students passed the test.']),
    ('For every real number x, x² ≥ 0.', 'There is a real number x such that x² < 0.', ['For every real number x, x² < 0.', 'There is a real number x such that x² ≥ 0.', 'For every real number x, x² ≤ 0.']),
    ('There is an integer n such that n² = 5.', 'For every integer n, n² ≠ 5.', ['There is an integer n such that n² ≠ 5.', 'For every integer n, n² = 5.', 'There is no integer n such that n² ≠ 5.']),
    ('Every triangle has an angle of at least 60°.', 'There is a triangle in which every angle is less than 60°.', ['Every triangle has an angle less than 60°.', 'There is a triangle with an angle less than 60°.', 'No triangle has an angle of at least 60°.']),
    ('For every x in D, if P(x) then Q(x).', 'There is an x in D such that P(x) and not Q(x).', ['For every x in D, if P(x) then not Q(x).', 'There is an x in D such that if P(x) then not Q(x).', 'For every x in D, if not P(x) then not Q(x).']),
    ('For every integer m, there is an integer n with n > m.', 'There is an integer m such that for every integer n, n ≤ m.', ['For every integer m, there is an integer n with n ≤ m.', 'There is an integer m and an integer n with n ≤ m.', 'For every integer m and every integer n, n ≤ m.']),
    ('There is a person who likes every movie.', 'For every person, there is a movie that the person does not like.', ['There is a person who dislikes every movie.', 'Every person likes some movie.', 'There is a movie that no person likes.']),
]

# a small finite world for quantified statements: students and the clubs they joined
WORLD = {'Ana': {'chess', 'math'}, 'Ben': {'math'}, 'Cai': {'art', 'math'}, 'Dev': {'chess', 'art', 'math'}}
CLUBS = ['art', 'chess', 'math']
WSTAT = [  # (statement, function)
    ('Every student is in the math club.', lambda: all('math' in WORLD[s] for s in WORLD)),
    ('Some student is in exactly one club.', lambda: any(len(WORLD[s]) == 1 for s in WORLD)),
    ('Every club has at least two members.', lambda: all(sum(c in WORLD[s] for s in WORLD) >= 2 for c in CLUBS)),
    ('There is a student who is in every club.', lambda: any(all(c in WORLD[s] for c in CLUBS) for s in WORLD)),
    ('Every student in the chess club is in the art club.', lambda: all('art' in WORLD[s] for s in WORLD if 'chess' in WORLD[s])),
    ('For every club, there is a student not in that club.', lambda: all(any(c not in WORLD[s] for s in WORLD) for c in CLUBS)),
    ('There is a club that every student is in.', lambda: any(all(c in WORLD[s] for s in WORLD) for c in CLUBS)),
    ('For every student, there is a club the student is not in.', lambda: all(any(c not in WORLD[s] for c in CLUBS) for s in WORLD)),
]
WTXT = 'Club rosters: Ana: chess, math. Ben: math. Cai: art, math. Dev: chess, art, math.'


def s2(b):
    for L, idx in (('cp2', [0, 3, 5]), ('cp1', [1, 6, 7]), ('honors', [2, 8, 9])):
        for i in idx:
            st, t, why, _ = QSTAT[i]
            b.mc(2, L, 'True or false? %s' % st, 'True' if t else 'False', ['False' if t else 'True', 'Sometimes true and sometimes false, so it is not a statement', 'It cannot be decided without checking every value'],
                 [why, 'So the statement is %s.' % ('true' if t else 'false')], 'quantified_truth')
    for L, idx in (('cp2', [0, 1, 4]), ('cp1', [2, 3, 5]), ('honors', [5, 6, 7])):
        for i in idx:
            st, good, bad = NEG_ITEMS[i]
            b.mc(2, L, 'Which is the negation of "%s"?' % st, good, bad,
                 ['The negation of "for all x, P(x)" is "there exists x such that not P(x)"; the negation of "there exists x such that P(x)" is "for all x, not P(x)".',
                  'Negation: ' + good], 'negate_quantifier')
    for L, idx in (('cp2', [0, 1]), ('cp1', [2, 4]), ('honors', [5, 7])):
        for i in idx:
            st, f = WSTAT[i]
            v = f()
            b.mc(2, L, WTXT + '\nTrue or false: "%s"' % st, 'True' if v else 'False', ['False' if v else 'True', 'Cannot be determined from the rosters', 'True for some students only, so neither true nor false'],
                 ['Check the statement against each student/club in the rosters.', 'The statement is %s.' % ('true' if v else 'false')], 'world_quantifier')
    # select-all: which statements are true in the world
    for L, idx in (('cp2', [0, 1, 4, 5]), ('cp1', [2, 3, 4, 5, 6]), ('honors', [3, 4, 5, 6, 7])):
        opts = [(WSTAT[i][0], WSTAT[i][1]()) for i in idx]
        b.sel(2, L, WTXT + '\nWhich statements are true?', opts,
              ['%s → %s.' % (s, 'true' if c else 'false') for s, c in opts], 'world_select')
    # short answer: counterexample search over a finite domain (computed)
    CE = [('For every n in {1, 2, ..., 10}, n² + 1 is odd.', range(1, 11), lambda n: (n * n + 1) % 2 == 1, 'cp2'),
          ('For every n in {1, 2, ..., 10}, 2ⁿ > n².', range(1, 11), lambda n: 2 ** n > n * n, 'cp1'),
          ('For every n in {1, 2, ..., 12}, n² − n + 11 is prime.', range(1, 13), lambda n: isprime(n * n - n + 11), 'honors'),
          ('For every n in {1, 2, ..., 8}, 3n + 1 is not a perfect square.', range(1, 9), lambda n: int((3 * n + 1) ** .5) ** 2 != 3 * n + 1, 'cp1'),
          ('For every n in {2, 3, ..., 9}, n! < 3ⁿ.', range(2, 10), lambda n: fact(n) < 3 ** n, 'honors'),
          ('For every n in {1, 2, ..., 6}, n + 3 > 2n.', range(1, 7), lambda n: n + 3 > 2 * n, 'cp2')]
    for st, D, f, L in CE:
        bad = [n for n in D if not f(n)]
        b.sa(2, L, 'Find the SMALLEST counterexample to the statement, or write "none" if the statement is true.\n%s' % st,
             str(bad[0]) if bad else 'none',
             ['Test the values in order: ' + ', '.join('%d→%s' % (n, 'T' if f(n) else 'F') for n in D) + '.',
              ('The first failure is n = %d.' % bad[0]) if bad else 'Every value works, so there is no counterexample.'], 'smallest_counterexample')
    # open response
    b.orq(2, 'cp2', 'Use the club rosters. ' + WTXT,
          [('Is "Every student is in the math club" true?', 'True'),
           ('Write its negation.', 'Some student is not in the math club.'),
           ('Is "Some student is in the art club" true? Name a witness.', 'True; Cai (or Dev).'),
           ('Write the negation of "Some student is in the art club."', 'No student is in the art club.')],
          ['All four lists include math.', 'Not (for all) = there exists ... not.', 'Cai and Dev list art.', 'Not (there exists) = for all ... not.'], 'world_or')
    b.orq(2, 'cp1', 'Let D = {−2, −1, 0, 1, 2} and consider the statements S₁: "For every x in D, x² ≤ 4" and S₂: "There is an x in D such that x³ = x and x ≠ 0".',
          [('Is S₁ true? Explain.', 'True: the squares are 4, 1, 0, 1, 4.'),
           ('Write the negation of S₁.', 'There is an x in D such that x² > 4.'),
           ('Is S₂ true? Give a witness.', 'True: x = 1 (or x = −1).'),
           ('If D is changed to all integers, which statement changes truth value?', 'S₁ becomes false (x = 3); S₂ stays true.')],
          ['Check each element.', 'Negate the quantifier and the inequality.', '1³ = 1 and 1 ≠ 0.', 'Larger domains can create counterexamples for universal statements but cannot destroy witnesses.'], 'domain_or')
    b.orq(2, 'honors', 'Let P(x, y) be "x + y = 0", with x and y real numbers.',
          [('Write "∀x ∃y P(x, y)" in words and decide its truth value.', 'For every real x there is a real y with x + y = 0. True (y = −x).'),
           ('Write "∃y ∀x P(x, y)" in words and decide its truth value.', 'There is a real y such that x + y = 0 for every real x. False.'),
           ('Explain why swapping the quantifiers changed the truth value.', 'In the first, y may depend on x; in the second, one y must work for all x, but x = 0 needs y = 0 and x = 1 needs y = −1.'),
           ('Write the negation of "∀x ∃y P(x, y)" with no "not" in front of a quantifier.', '∃x ∀y, x + y ≠ 0.')],
          ['Choose y = −x.', 'A single y cannot satisfy x + y = 0 for two different x.', 'Order of quantifiers matters.', '¬∀x∃y P ≡ ∃x∀y ¬P.'], 'quantifier_order_or')


def isprime(n):
    if n < 2:
        return False
    return all(n % d for d in range(2, int(n ** .5) + 1))


def fact(n):
    r = 1
    for k in range(2, n + 1):
        r *= k
    return r


# ---------------------------------------------------------------- skill 3: conditional statements
COND = [  # (english, hypothesis, conclusion, negated hypothesis, negated conclusion)
    ('If it rains, then the game is canceled.', 'it rains', 'the game is canceled', 'it does not rain', 'the game is not canceled'),
    ('If a number is divisible by 6, then it is divisible by 3.', 'a number is divisible by 6', 'it is divisible by 3', 'a number is not divisible by 6', 'it is not divisible by 3'),
    ('You can vote only if you are registered.', 'you can vote', 'you are registered', 'you cannot vote', 'you are not registered'),
    ('The light turns on whenever the switch is up.', 'the switch is up', 'the light turns on', 'the switch is not up', 'the light does not turn on'),
    ('A passing grade is necessary for graduation.', 'a student graduates', 'the student has a passing grade', 'a student does not graduate', 'the student does not have a passing grade'),
    ('Scoring above 90 is sufficient for an A.', 'a student scores above 90', 'the student earns an A', 'a student does not score above 90', 'the student does not earn an A'),
    ('The program halts unless the input is negative.', 'the input is not negative', 'the program halts', 'the input is negative', 'the program does not halt'),
    ('x² = 9 if x = 3.', 'x = 3', 'x² = 9', 'x ≠ 3', 'x² ≠ 9'),
]
COND_TRUTH = [  # (statement, truth, reason)  conditional with numbers
    ('If 2 + 2 = 5, then 7 is even.', True, 'The hypothesis is false, so the conditional is vacuously true.'),
    ('If 3 is odd, then 3² is odd.', True, 'True hypothesis and true conclusion.'),
    ('If 4 is even, then 4 is prime.', False, 'True hypothesis, false conclusion: the only false case.'),
    ('If 9 is prime, then 9 is odd.', True, 'False hypothesis, so the conditional is true.'),
    ('If 1 > 2, then 1 > 0.', True, 'False hypothesis.'),
    ('If 10 is divisible by 5, then 10 is divisible by 4.', False, 'True hypothesis, false conclusion.'),
]


def s3(b):
    for L, idx in (('cp2', [0, 1, 3]), ('cp1', [2, 4, 7]), ('honors', [5, 6, 2])):
        for i in idx:
            e, h, c, nh, nc = COND[i]
            good = 'If %s, then %s.' % (h, c)
            wrong = ['If %s, then %s.' % (c, h), 'If %s, then %s.' % (nh, nc), '%s if and only if %s.' % (h[0].upper() + h[1:], c)]
            b.mc(3, L, 'Rewrite in "if p, then q" form: "%s"' % e, good, wrong,
                 ['Identify the hypothesis (sufficient condition) and the conclusion (necessary condition).',
                  {'only if': '"p only if q" means "if p, then q".', 'necessary': '"q is necessary for p" means "if p, then q".',
                   'sufficient': '"p is sufficient for q" means "if p, then q".', 'whenever': '"q whenever p" means "if p, then q".',
                   'unless': '"q unless r" means "if not r, then q".'}.get(next((k for k in ('only if', 'necessary', 'sufficient', 'whenever', 'unless') if k in e), ''), 'The sentence already states the hypothesis first.'),
                  good], 'if_then_form')
    for L, idx in (('cp2', [1, 2]), ('cp1', [0, 3, 5]), ('honors', [4, 0])):
        for i in idx:
            st, t, why = COND_TRUTH[i]
            b.mc(3, L, 'Find the truth value: "%s"' % st, 'True' if t else 'False', ['False' if t else 'True', 'Neither, the hypothesis is false', 'Neither, the parts are unrelated'],
                 [why, 'A conditional p → q is false only when p is true and q is false.'], 'conditional_truth')
    # hypothesis / conclusion short answer
    for L, i in (('cp2', 3), ('cp1', 2), ('honors', 4)):
        e, h, c, nh, nc = COND[i]
        b.sa(3, L, 'Identify the HYPOTHESIS of the conditional statement: "%s" (answer with the words of the hypothesis).' % e, h,
             ['Rewrite as "if p, then q": If %s, then %s.' % (h, c), 'The hypothesis is "%s".' % h], 'hypothesis_id')
    # truth table column of p → q (short answer)
    from logic import colstr
    for L, f in (('cp2', 'p → q'), ('cp1', '¬p → q'), ('honors', 'p → (q → p)')):
        b.sa(3, L, 'Give the truth-value column for %s in the standard row order (p, q) = TT, TF, FT, FF. Write it as four letters, for example TFFT.' % f,
             colstr(f), ['Evaluate row by row; p → q is false only when p is T and q is F.', 'Column: ' + colstr(f)], 'cond_column')
    # select-all for which situations make a conditional false
    b.sel(3, 'cp2', 'A teacher promises: "If you finish the review, then you get a homework pass." In which situations did the teacher break the promise?',
          [('You finished the review and did not get a pass.', True), ('You finished the review and got a pass.', False),
           ('You did not finish the review and got a pass.', False), ('You did not finish the review and did not get a pass.', False),
           ('You finished the review, and the teacher gave the pass to someone else instead of you.', True)],
          ['A conditional is broken (false) only when the hypothesis happens and the conclusion does not.'], 'promise_select')
    b.sel(3, 'cp1', 'Which statements are equivalent to "If a shape is a square, then it is a rectangle"?',
          [('A shape is a square only if it is a rectangle.', True), ('Being a rectangle is necessary for being a square.', True),
           ('Being a square is sufficient for being a rectangle.', True), ('A shape is a rectangle only if it is a square.', False),
           ('If a shape is a rectangle, then it is a square.', False)],
          ['"p only if q", "q is necessary for p" and "p is sufficient for q" all mean p → q.', 'The other two state the converse.'], 'necessary_sufficient_select')
    b.sel(3, 'honors', 'Let p: "n is divisible by 4" and q: "n is even" for integers n. Which statements are true for EVERY integer n?',
          [('p → q', True), ('q → p', False), ('¬q → ¬p', True), ('p is sufficient for q', True), ('p is necessary for q', False)],
          ['Every multiple of 4 is even, so p → q and its contrapositive ¬q → ¬p are true.', 'n = 2 is even but not divisible by 4, so q → p fails and p is not necessary for q.'], 'divisibility_conditional_select')
    b.orq(3, 'cp1', 'Consider the statement S: "If a whole number ends in 0, then it is divisible by 5."',
          [('Identify the hypothesis and conclusion.', 'Hypothesis: a whole number ends in 0. Conclusion: it is divisible by 5.'),
           ('Is S true? Explain.', 'True: a number ending in 0 is a multiple of 10, which is a multiple of 5.'),
           ('Write S using "only if".', 'A whole number ends in 0 only if it is divisible by 5.'),
           ('Give a number for which the hypothesis is false but the conclusion is true. Does it make S false?', 'For example 25. No: a false hypothesis never makes a conditional false.')],
          ['Read "if p, then q".', '10k = 5(2k).', 'p → q is "p only if q".', 'Only p true and q false would make S false.'], 'conditional_or')
    b.orq(3, 'honors', 'A store policy reads: "You may return an item only if you have a receipt, unless the item is defective."',
          [('Let r = "you may return the item", c = "you have a receipt", d = "the item is defective". Write the policy symbolically.', '¬d → (r → c)'),
           ('Rewrite it as one if-then sentence.', 'If the item is not defective and you may return it, then you have a receipt.'),
           ('A customer with no receipt returns a defective item. Is the policy violated?', 'No. When d is true the policy makes no requirement.'),
           ('Describe the only kind of situation that violates the policy.', 'An item that is not defective is returned without a receipt (d false, r true, c false).')],
          ['"q unless d" means "if not d, then q"; here q is "r only if c", that is r → c.',
           '¬d → (r → c) is equivalent to (¬d ∧ r) → c.', 'With d true, ¬d is false, so the conditional is true.', 'The statement is false only when ¬d is T and r → c is F.'], 'policy_or')
    b.orq(3, 'cp2', 'Statement: "If an animal is a fish, then it can swim."',
          [('What is the hypothesis?', 'An animal is a fish.'), ('What is the conclusion?', 'It can swim.'),
           ('A dog can swim. Does the dog make the statement false?', 'No; the hypothesis is false for a dog.'),
           ('What kind of animal would make the statement false?', 'A fish that cannot swim.')],
          ['The "if" part is the hypothesis.', 'The "then" part is the conclusion.', 'A false hypothesis never makes p → q false.', 'p → q is false only when p is true and q is false.'], 'fish_or')
    # top up
    extra = [('cp2', 'If 5 > 3, then 5 + 1 > 3 + 1.', True), ('cp1', 'If 0 is positive, then 0 is negative.', True), ('honors', 'If every prime is odd, then 2 is odd.', True)]
    for L, st, t in extra:
        b.mc(3, L, 'Find the truth value: "%s"' % st, 'True' if t else 'False', ['False', 'Neither', 'Cannot be determined'],
             ['Decide the truth value of the hypothesis and the conclusion.', 'The conditional is false only if the hypothesis is true and the conclusion is false; here it is %s.' % ('true' if t else 'false')], 'conditional_truth')


# ---------------------------------------------------------------- skill 4: set-roster and set-builder notation
BUILDER = [  # (description, roster python set, universe text)
    ('{n ∈ ℤ | −2 ≤ n < 3}', set(range(-2, 3))),
    ('{n ∈ ℕ | n is a factor of 12}', {1, 2, 3, 4, 6, 12}),
    ('{x ∈ ℤ | x² = 9}', {-3, 3}),
    ('{n ∈ ℤ⁺ | n < 20 and n is prime}', {2, 3, 5, 7, 11, 13, 17, 19}),
    ('{2k + 1 | k ∈ ℤ and 0 ≤ k ≤ 4}', {1, 3, 5, 7, 9}),
    ('{k² | k ∈ {−2, −1, 0, 1, 2}}', {0, 1, 4}),
    ('{x ∈ ℤ | x² < 0}', set()),
    ('{n ∈ ℤ | 3 divides n and |n| ≤ 7}', {-6, -3, 0, 3, 6}),
    ('{n ∈ ℤ⁺ | n² ≤ 30}', {1, 2, 3, 4, 5}),
    ('{3k − 1 | k ∈ ℤ and 1 ≤ k ≤ 5}', {2, 5, 8, 11, 14}),
]


def s4(b):
    note = ' (Here ℤ = integers, ℤ⁺ = positive integers, ℕ = {1, 2, 3, …}.)'
    for L, idx in (('cp2', [0, 1, 4, 8]), ('cp1', [2, 3, 5, 9]), ('honors', [6, 7, 5, 3])):
        for i in idx:
            d, s = BUILDER[i]
            b.sa(4, L, 'Write the set in roster notation, elements in increasing order (∅ if empty): %s%s' % (d, note if L != 'honors' else ''),
                 fmt_set(s), ['Read the set-builder notation: list every object that satisfies the condition.', 'Roster form: ' + fmt_set(s)], 'builder_to_roster')
    ROST = [  # (roster, correct builder, distractors)
        ('{2, 4, 6, 8, 10}', '{2k | k ∈ ℤ and 1 ≤ k ≤ 5}', ['{k + 2 | k ∈ ℤ and 0 ≤ k ≤ 8}', '{2k | k ∈ ℤ and 2 ≤ k ≤ 10}', '{n ∈ ℤ | n is even}']),
        ('{1, 4, 9, 16, 25}', '{n² | n ∈ ℤ and 1 ≤ n ≤ 5}', ['{n² | n ∈ ℤ and 1 ≤ n ≤ 25}', '{2n | n ∈ ℤ and 1 ≤ n ≤ 5}', '{n ∈ ℤ | 1 ≤ n ≤ 25}']),
        ('{−1, 1}', '{x ∈ ℝ | x² = 1}', ['{x ∈ ℝ | x = 1}', '{x ∈ ℝ | x² = −1}', '{x ∈ ℤ | −1 ≤ x ≤ 1}']),
        ('{5, 10, 15, 20, …}', '{5k | k ∈ ℤ⁺}', ['{k + 5 | k ∈ ℤ⁺}', '{5k | k ∈ ℤ}', '{n ∈ ℤ⁺ | n ≥ 5}']),
        ('{3, 7, 11, 15}', '{4k − 1 | k ∈ ℤ and 1 ≤ k ≤ 4}', ['{4k + 3 | k ∈ ℤ and 1 ≤ k ≤ 4}', '{3k + 4 | k ∈ ℤ and 0 ≤ k ≤ 3}', '{n ∈ ℤ | 3 ≤ n ≤ 15 and n is odd}']),
        ('{…, −4, −2, 0, 2, 4, …}', '{2k | k ∈ ℤ}', ['{2k | k ∈ ℤ⁺}', '{k + 2 | k ∈ ℤ}', '{k² | k ∈ ℤ}']),
    ]
    for L, idx in (('cp2', [0, 1]), ('cp1', [2, 3]), ('honors', [4, 5])):
        for i in idx:
            r, good, bad = ROST[i]
            b.mc(4, L, 'Which set-builder description equals %s?' % r, good, bad,
                 ['List a few elements of each choice and compare with the roster.', 'Only %s produces exactly %s.' % (good, r)], 'roster_to_builder')
    CARD = [('{1, 2, 2, 3, 3, 3}', 3, 'cp2', 'Repeated elements count once.'),
            ('{∅, {∅}}', 2, 'honors', 'The elements are ∅ and {∅}; they are different.'),
            ('{{1, 2}, {3}}', 2, 'cp1', 'The set has two elements, each of which is itself a set.'),
            ('{x ∈ ℤ | 0 < x < 1}', 0, 'cp1', 'No integer lies strictly between 0 and 1.'),
            ('{a, b, {a, b}}', 3, 'honors', 'a, b and the set {a, b} are three distinct elements.'),
            ('{0}', 1, 'cp2', '{0} has one element, the number 0. It is not empty.')]
    for s, n, L, why in CARD:
        b.mc(4, L, 'How many elements does the set %s have?' % s, str(n), [str(n + 1), str(max(0, n - 1)) if n else '1', str(n + 2), str(n * 2 + 3)],
             [why, 'Number of elements: %d.' % n], 'cardinality', order='sort')
    b.sel(4, 'cp2', 'Which sets are equal to {1, 2, 3}?',
          [('{3, 2, 1}', True), ('{1, 1, 2, 3}', True), ('{n ∈ ℤ | 1 ≤ n ≤ 3}', True), ('{1, 2, 3, 4}', False), ('{(1, 2, 3)}', False)],
          ['Order and repetition do not matter in a set.', '{(1, 2, 3)} has one element (an ordered triple).'], 'equal_rosters_select')
    b.sel(4, 'cp1', 'Which descriptions name the empty set?',
          [('{x ∈ ℝ | x² = −4}', True), ('{n ∈ ℤ | 2 < n < 3}', True), ('{0}', False), ('{∅}', False), ('{x ∈ ℝ | x + 1 = x}', True)],
          ['No real square is negative; no integer lies strictly between 2 and 3; x + 1 = x has no solution.', '{0} and {∅} each have one element.'], 'empty_select')
    b.sel(4, 'honors', 'Let A = {n ∈ ℤ | n = 4k + 1 for some integer k}. Which numbers are elements of A?',
          [('−3', True), ('1', True), ('13', True), ('7', False), ('−1', False)],
          ['n ∈ A exactly when n − 1 is divisible by 4.', '−3 − 1 = −4, 1 − 1 = 0, 13 − 1 = 12 are divisible by 4; 6 and −2 are not.'], 'member_builder_select')
    b.orq(4, 'cp1', 'Let A = {x ∈ ℤ | −3 < x ≤ 2} and B = {x² | x ∈ A}.',
          [('Write A in roster notation.', '{−2, −1, 0, 1, 2}'), ('Write B in roster notation.', '{0, 1, 4}'),
           ('How many elements do A and B have?', 'A has 5 elements; B has 3.'), ('Explain why B has fewer elements than A.', 'Different elements square to the same value (for example (−2)² = 2²), and repeats count once.')],
          ['−3 is excluded and 2 is included.', 'Square each element and list each value once.', 'Count distinct elements.', 'Squaring is not one-to-one on A.'], 'builder_or')
    b.orq(4, 'honors', 'Let S = {n ∈ ℤ | n² − 5n + 6 ≤ 0} and T = {n ∈ ℤ | 2 ≤ n ≤ 3}.',
          [('Factor n² − 5n + 6.', '(n − 2)(n − 3)'), ('Write S in roster notation.', '{2, 3}'),
           ('Explain why S = T.', 'Both have exactly the elements 2 and 3, and sets with the same elements are equal.'),
           ('Write a different set-builder description of the same set using "n² = 5n − 6".', '{n ∈ ℤ | n² = 5n − 6}')],
          ['(n − 2)(n − 3) ≤ 0 when 2 ≤ n ≤ 3.', 'Only integers 2 and 3 qualify.', 'Set equality means same elements.', 'n² − 5n + 6 = 0 has roots 2 and 3.'], 'builder_equal_or')
    b.orq(4, 'cp2', 'The set M is all positive multiples of 3 that are less than 20.',
          [('Write M in roster notation.', '{3, 6, 9, 12, 15, 18}'), ('Write M in set-builder notation.', '{3k | k ∈ ℤ and 1 ≤ k ≤ 6}'),
           ('Is 21 ∈ M? Explain.', 'No, 21 is not less than 20.'), ('How many elements does M have?', '6')],
          ['List 3, 6, 9, ... below 20.', 'Each element is 3k for k = 1 to 6.', 'Check the condition.', 'Count them.'], 'multiples_or')


# ---------------------------------------------------------------- skill 5: subsets and membership
def s5(b):
    A = {1, 2, 3}
    MEM = [  # (claim, truth, reason, level, trap reasons for the wrong truth value)
        ('2 ∈ {1, 2, 3}', True, '2 is listed as an element.', 'cp2', ['2 is a number, and only sets can be elements', 'the symbol ∈ is only used with letters']),
        ('{2} ∈ {1, 2, 3}', False, 'the elements are the numbers 1, 2, 3; the set {2} is not one of them', 'cp1', ['2 is in the set, so {2} is too', '{2} is a subset, and every subset is an element']),
        ('{2} ⊆ {1, 2, 3}', True, 'every element of {2} (just 2) is in {1, 2, 3}', 'cp1', ['{2} is not listed in {1, 2, 3}', 'a subset must have at least two elements']),
        ('∅ ⊆ {1, 2, 3}', True, 'the empty set is a subset of every set', 'cp2', ['∅ is not listed in {1, 2, 3}', 'the empty set has nothing in common with {1, 2, 3}']),
        ('∅ ∈ {1, 2, 3}', False, '∅ is not listed as an element (∅ ⊆ {1, 2, 3} is true, but that is a different claim)', 'honors', ['the empty set is in every set', '∅ ⊆ {1, 2, 3}, so ∅ ∈ {1, 2, 3}']),
        ('{1, 2} ∈ {{1, 2}, 3}', True, '{1, 2} is listed as one of the two elements', 'honors', ['1 and 2 are not elements, so {1, 2} is not either', 'a set cannot be an element of another set']),
        ('{1, 2} ⊆ {{1, 2}, 3}', False, '1 is not an element of {{1, 2}, 3}; its elements are {1, 2} and 3', 'honors', ['{1, 2} appears inside the braces', 'every element of a set is also a subset of it']),
        ('{1, 2, 3} ⊆ {1, 2, 3}', True, 'every set is a subset of itself', 'cp2', ['a set cannot be a subset of itself', 'the sets are equal, so neither is a subset']),
        ('{1, 2, 3} ⊊ {1, 2, 3}', False, 'a proper subset must be missing at least one element of the larger set', 'cp1', ['every set is a subset of itself', 'the two sets have the same elements']),
        ('3 ⊆ {1, 2, 3}', False, '3 is a number, not a set, so it is not a subset; the true statements are 3 ∈ {1, 2, 3} and {3} ⊆ {1, 2, 3}', 'cp1', ['3 is in the set', '3 is one of the elements, so it is a subset']),
    ]
    for claim, t, why, L, traps in MEM:
        good = ('True: ' if t else 'False: ') + why
        bad = [('False: ' if t else 'True: ') + traps[0], ('False: ' if t else 'True: ') + traps[1], ('True: ' if t else 'False: ') + traps[0]]
        b.mc(5, L, 'Is the statement %s true or false? Choose the answer with the correct reason.' % claim, good, bad,
             [why[0].upper() + why[1:] + '.', '∈ means "is an element of"; ⊆ means "every element of the left set is in the right set".'], 'member_subset_truth')
    # counting subsets
    for n, L in ((3, 'cp2'), (4, 'cp1'), (6, 'honors')):
        S = list(range(1, n + 1))
        b.sa(5, L, 'How many subsets does %s have (include ∅ and the set itself)?' % fmt_set(S), 2 ** n,
             ['Each of the %d elements is either in or out of a subset.' % n, '2^%d = %d subsets.' % (n, 2 ** n)], 'count_subsets')
    for n, L in ((3, 'cp2'), (5, 'cp1')):
        b.sa(5, L, 'How many PROPER subsets does a set with %d elements have?' % n, 2 ** n - 1,
             ['There are 2^%d = %d subsets.' % (n, 2 ** n), 'All except the set itself are proper: %d.' % (2 ** n - 1)], 'count_proper')
    b.sa(5, 'honors', 'How many subsets of {1, 2, 3, 4, 5, 6} contain the element 1 but not the element 2?', 2 ** 4,
         ['1 is forced in and 2 is forced out.', 'Each of 3, 4, 5, 6 is free: 2⁴ = 16.'], 'count_subsets_constraint')
    b.sa(5, 'honors', 'List all subsets of {a, b, c} that have exactly two elements, separated by semicolons, in the order {a, b}; ... (alphabetical).', '{a, b}; {a, c}; {b, c}',
         ['Choose 2 of the 3 letters: C(3, 2) = 3 ways.', '{a, b}; {a, c}; {b, c}'], 'list_two_subsets')
    b.sel(5, 'cp2', 'Let A = {1, 2, 3, 4}. Which sets are subsets of A?',
          [('{1, 4}', True), ('∅', True), ('{2, 5}', False), ('{1, 2, 3, 4}', True), ('{0}', False)],
          ['Check that every element of the candidate is in A.', '5 and 0 are not in A.'], 'subset_select')
    b.sel(5, 'cp1', 'Let B = {0, {0}, {1, 2}}. Which statements are true?',
          [('0 ∈ B', True), ('{0} ∈ B', True), ('{0} ⊆ B', True), ('1 ∈ B', False), ('{1, 2} ⊆ B', False)],
          ['The elements of B are 0, {0} and {1, 2}.', '{0} ⊆ B because 0 ∈ B; {1, 2} ⊆ B is false because 1 ∉ B.'], 'nested_select')
    b.sel(5, 'honors', 'Let A ⊆ B and B ⊆ C, where A = {1, 2}. Which statements MUST be true?',
          [('A ⊆ C', True), ('1 ∈ C', True), ('C ⊆ A', False), ('B = C', False), ('{2} ⊆ B', True)],
          ['Subset is transitive, so A ⊆ C and 1, 2 ∈ B, C.', 'Nothing forces C ⊆ A or B = C.'], 'transitive_subset_select')
    b.orq(5, 'cp1', 'Let A = {2, 4, 6}, B = {n ∈ ℤ | n is even and 0 < n < 10}, C = {2, 4, 6, 8}.',
          [('Write B in roster form.', '{2, 4, 6, 8}'), ('Is A ⊆ B? Is A a proper subset of B?', 'Yes and yes: 8 ∈ B but 8 ∉ A.'),
           ('Is B = C? Explain.', 'Yes; they have the same elements.'), ('How many subsets of C contain all of A?', '2 ({2, 4, 6} and {2, 4, 6, 8})')],
          ['List the even integers between 0 and 10.', 'Each element of A is in B; B has an extra element.', 'Same elements means equal sets.', 'Only 8 is free to include or exclude: 2¹ = 2.'], 'subset_or')
    b.orq(5, 'honors', 'Let X = {1, 2, 3, 4, 5}.',
          [('How many subsets does X have?', '32'), ('How many subsets have exactly 2 elements?', '10'),
           ('How many subsets contain at least one even number?', '24'), ('Explain your method for the previous part.', 'Subsets with no even number are subsets of {1, 3, 5}: 2³ = 8. So 32 − 8 = 24.')],
          ['2⁵ = 32.', 'C(5, 2) = 10.', 'Use the complement: count subsets with no even number.', '32 − 8 = 24.'], 'subset_count_or')
    b.orq(5, 'cp2', 'Let S = {red, blue}.',
          [('List all subsets of S.', '∅, {red}, {blue}, {red, blue}'), ('How many subsets are there?', '4'),
           ('Which subsets are proper subsets?', '∅, {red}, {blue}'), ('Is red ∈ S or red ⊆ S? Explain.', 'red ∈ S; red is an element, not a set.')],
          ['Include the empty set and S itself.', '2² = 4.', 'Every subset except S itself.', '∈ is for elements.'], 'subsets_list_or')


# ---------------------------------------------------------------- skill 6: Cartesian products and ordered pairs
def s6(b):
    PAIRS = [({1, 2}, {'a', 'b'}, 'cp2'), ({'x', 'y', 'z'}, {0, 1}, 'cp2'), ({1, 2, 3}, {3, 4}, 'cp1'), ({0, 1}, {0, 1}, 'cp1')]
    for A, B, L in PAIRS:
        P = sorted(itertools.product(sorted(A, key=str), sorted(B, key=str)))
        b.sa(6, L, 'Let A = %s and B = %s. List A × B in roster notation, ordered first by the first coordinate, then by the second.' % (fmt_set(A), fmt_set(B)),
             '{' + ', '.join('(%s, %s)' % p for p in P) + '}',
             ['A × B = {(a, b) | a ∈ A and b ∈ B}; the first coordinate comes from A.', 'There are %d · %d = %d pairs.' % (len(A), len(B), len(P))], 'list_product')
    for m, n, k, L in ((3, 4, None, 'cp2'), (5, 2, None, 'cp1'), (2, 3, 4, 'honors'), (4, 4, None, 'cp1')):
        if k is None:
            b.sa(6, L, 'If |A| = %d and |B| = %d, how many ordered pairs are in A × B?' % (m, n), m * n,
                 ['|A × B| = |A| · |B|.', '%d · %d = %d' % (m, n, m * n)], 'product_size')
        else:
            b.sa(6, L, 'If |A| = %d, |B| = %d and |C| = %d, how many elements does A × B × C have?' % (m, n, k), m * n * k,
                 ['Each element is an ordered triple (a, b, c).', '%d · %d · %d = %d' % (m, n, k, m * n * k)], 'triple_size')
    TF = [('(1, 2) = (2, 1)', False, 'ordered pairs are equal only when corresponding coordinates are equal', 'cp2', ['they contain the same numbers', 'order does not matter in pairs']),
          ('{1, 2} = {2, 1}', True, 'sets ignore order', 'cp2', ['the elements are listed in a different order', 'sets are ordered lists']),
          ('If A = {1} and B = {2}, then A × B = B × A.', False, 'A × B = {(1, 2)} but B × A = {(2, 1)}', 'cp1', ['both products have exactly one element', 'multiplication is commutative']),
          ('A × ∅ = ∅ for every set A.', True, 'there is no second coordinate to choose, so there are no ordered pairs', 'honors', ['A × ∅ = A because ∅ acts like 1', 'A × ∅ = {∅}']),
          ('(a, b) = (c, d) exactly when a = c and b = d.', True, 'this is the definition of equality of ordered pairs', 'cp1', ['it is enough that {a, b} = {c, d}', 'it is enough that a + b = c + d']),
          ('If A × B = B × A, then A = B.', False, 'A = ∅ and B = {1} give A × B = B × A = ∅, but A ≠ B', 'honors', ['equal products force equal first coordinates', 'it works for A = B = {1}'])]
    for st, t, why, L, traps in TF:
        good = ('True: ' if t else 'False: ') + why
        bad = [('False: ' if t else 'True: ') + traps[0], ('False: ' if t else 'True: ') + traps[1], ('True: ' if t else 'False: ') + traps[1]]
        b.mc(6, L, 'Is this statement true or false? Choose the answer with the correct reason.\n%s' % st, good, bad,
             [why[0].upper() + why[1:] + '.'], 'ordered_pair_truth')
    b.sa(6, 'cp1', 'Solve for x and y: (2x − 1, y + 3) = (7, 2x). Answer as an ordered pair (x, y).', '(4, 5)',
         ['Equal ordered pairs have equal coordinates: 2x − 1 = 7 and y + 3 = 2x.', 'x = 4, then y + 3 = 8, so y = 5.'], 'pair_equation')
    b.sa(6, 'honors', 'Solve for all real x: (x², x) = (4, −2). Answer as a single number.', '-2',
         ['x² = 4 gives x = 2 or x = −2.', 'The second coordinate requires x = −2, so only x = −2 works.'], 'pair_equation')
    b.sel(6, 'cp2', 'Let A = {1, 2} and B = {5, 6}. Which ordered pairs are elements of A × B?',
          [('(1, 5)', True), ('(2, 6)', True), ('(5, 1)', False), ('(2, 5)', True), ('(1, 2)', False)],
          ['The first coordinate must come from A and the second from B.'], 'product_member_select')
    b.sel(6, 'cp1', 'Let A = {0, 1}. Which are elements of A × A × A?',
          [('(0, 0, 1)', True), ('(1, 1, 1)', True), ('(0, 1)', False), ('(1, 0, 2)', False), ('(1, 0, 0)', True)],
          ['Elements are ordered triples with every coordinate in A.'], 'triple_member_select')
    b.sel(6, 'honors', 'Let A = {1, 2, 3}. Which subsets of A × A describe the relation "first coordinate < second coordinate"? Select every TRUE statement.',
          [('It contains exactly 3 ordered pairs.', True), ('It contains (1, 3).', True), ('It contains (2, 2).', False), ('It is a subset of A × A.', True), ('It contains (3, 1).', False)],
          ['The pairs are (1, 2), (1, 3), (2, 3).', 'Any relation on A is a subset of A × A.'], 'product_subset_select')
    b.orq(6, 'cp2', 'A sandwich shop offers breads B = {wheat, rye} and fillings F = {ham, egg, tuna}.',
          [('Write two elements of B × F.', 'For example (wheat, ham) and (rye, tuna).'), ('How many elements does B × F have?', '6'),
           ('Is (ham, wheat) in B × F? Explain.', 'No; the first coordinate must be a bread.'), ('What does an element of B × F represent?', 'One sandwich choice: a bread and a filling.')],
          ['Pair each bread with a filling.', '2 · 3 = 6.', 'Order matters in ordered pairs.', 'Each ordered pair is one bread-filling combination.'], 'product_context_or')
    b.orq(6, 'cp1', 'Let A = {1, 2, 3} and B = {a, b}.',
          [('List B × A.', '{(a, 1), (a, 2), (a, 3), (b, 1), (b, 2), (b, 3)}'), ('Find |A × B| and |B × A|.', 'Both are 6.'),
           ('Is A × B = B × A? Explain.', 'No. (1, a) ∈ A × B but (1, a) ∉ B × A.'), ('How many subsets does A × B have?', '64')],
          ['First coordinates from B.', '3 · 2 = 6 either way.', 'Same size, different elements.', '2⁶ = 64.'], 'product_or')
    b.orq(6, 'honors', 'Let A = {1, 2}, B = {2, 3} and C = {3}.',
          [('Find A × (B ∩ C).', '{(1, 3), (2, 3)}'), ('Find (A × B) ∩ (A × C).', '{(1, 3), (2, 3)}'),
           ('Find A × (B ∪ C) and its size.', '{(1, 2), (1, 3), (2, 2), (2, 3)}; size 4'),
           ('State the identity suggested by the first two parts.', 'A × (B ∩ C) = (A × B) ∩ (A × C).')],
          ['B ∩ C = {3}.', 'A × B = {(1,2),(1,3),(2,2),(2,3)}, A × C = {(1,3),(2,3)}.', 'B ∪ C = {2, 3}.', 'The product distributes over intersection.'], 'product_identity_or')


# ---------------------------------------------------------------- skill 7: strings and notation
def s7(b):
    for n, k, L in ((2, 3, 'cp2'), (2, 4, 'cp2'), (3, 2, 'cp1'), (4, 3, 'cp1'), (26, 2, 'honors')):
        alph = ['0, 1', '0, 1', 'a, b, c', 'A, C, G, T', 'a, b, ..., z'][[(2, 3), (2, 4), (3, 2), (4, 3), (26, 2)].index((n, k))]
        b.sa(7, L, 'How many strings of length %d can be formed over the alphabet {%s}? (Characters may repeat.)' % (k, alph), n ** k,
             ['Each of the %d positions has %d choices.' % (k, n), '%d^%d = %d' % (n, k, n ** k)], 'count_strings')
    for n, L in ((3, 'cp2'), (4, 'cp1')):
        strings = [''.join(p) for p in itertools.product('01', repeat=n)]
        exact = [s for s in strings if s.count('1') == 2]
        b.sa(7, L, 'How many bit strings of length %d contain exactly two 1s?' % n, len(exact),
             ['List them: ' + ', '.join(exact) + '.', 'Count: %d (this is C(%d, 2)).' % (len(exact), n)], 'count_bits')
    b.sa(7, 'honors', 'How many bit strings of length 5 do NOT contain two consecutive 1s?', sum(1 for p in itertools.product('01', repeat=5) if '11' not in ''.join(p)),
         ['Let a_n be the count for length n: a₁ = 2, a₂ = 3, and a_n = a_(n−1) + a_(n−2) (end in 0, or end in 01).', 'a₃ = 5, a₄ = 8, a₅ = 13.'], 'no_11_strings')
    b.sa(7, 'cp1', 'Let s = "abba" and t = "cab". What is the concatenation st?', 'abbacab', ['Concatenation writes s followed by t.', 'st = abbacab'], 'concatenate')
    b.sa(7, 'cp2', 'What is the length of the string 0110100?', 7, ['Count the characters.', '7'], 'string_length')
    b.sa(7, 'honors', 'Let λ be the empty string and s = "ab". What is the length of λsλs?', 4, ['The empty string adds no characters.', 'λsλs = abab, length 4.'], 'empty_string')
    b.mc(7, 'cp2', 'Which statement about strings is true?', '"ab" and "ba" are different strings', ['"ab" and "ba" are the same string', 'A string cannot repeat a character', 'The empty string has length 1'],
         ['Order matters in a string; repetition is allowed; the empty string has length 0.'], 'string_facts')
    b.mc(7, 'cp1', 'Over the alphabet Σ = {0, 1}, how many strings have length AT MOST 3 (including the empty string)?', '15', ['14', '8', '16'],
         ['Lengths 0, 1, 2, 3 give 1 + 2 + 4 + 8.', '1 + 2 + 4 + 8 = 15.'], 'strings_at_most')
    b.mc(7, 'honors', 'In a programming language, an identifier is 1 to 3 characters long, the first character a letter (26 choices) and any later character a letter or a digit (36 choices). How many identifiers are there?',
         str(26 + 26 * 36 + 26 * 36 * 36), [str(26 * 36 * 36), str(36 + 36 ** 2 + 36 ** 3), str(26 ** 3)],
         ['Add the counts for lengths 1, 2 and 3 (addition rule).', '26 + 26·36 + 26·36² = 26 + 936 + 33,696 = %d.' % (26 + 936 + 33696)], 'identifier_count')
    b.mc(7, 'cp1', 'Σ* denotes the set of all strings over Σ. If Σ = {a}, which string is NOT in Σ*?', 'ab', ['λ (the empty string)', 'a', 'aaaa'],
         ['Σ* contains every finite string of characters from Σ, including λ.', '"ab" uses b, which is not in Σ.'], 'sigma_star')
    b.sel(7, 'cp2', 'Which strings over {0, 1} have length 4?', [('0101', True), ('1111', True), ('101', False), ('00000', False), ('0000', True)],
          ['Count the characters in each string.'], 'length_select')
    b.sel(7, 'cp1', 'Which bit strings of length 4 are palindromes (read the same backward)?', [('0110', True), ('1001', True), ('1100', False), ('0000', True), ('0100', False)],
          ['Reverse each string and compare.'], 'palindrome_select')
    b.sel(7, 'honors', 'Let L be the set of bit strings that start with 1 and have an even number of 0s. Which strings are in L?',
          [('1', True), ('100', True), ('1010', True), ('0110', False), ('10', False)],
          ['Check the first character and count the 0s.', '1 has zero 0s (even); 100 has two; 1010 has two; 0110 starts with 0; 10 has one 0.'], 'language_select')
    b.orq(7, 'cp2', 'A lock code is a string of 3 digits (0–9). Digits may repeat.',
          [('Give two different codes that use the same digits.', 'For example 123 and 321.'), ('How many codes are possible?', '1000'),
           ('How many codes start with 9?', '100'), ('Is 042 a valid code of length 3?', 'Yes; leading zeros count as characters.')],
          ['Order matters in a string.', '10³ = 1000.', 'The first digit is fixed: 10² = 100.', 'Each position is a character.'], 'lock_or')
    b.orq(7, 'cp1', 'Let Σ = {a, b}.',
          [('List all strings in Σ² (length 2).', 'aa, ab, ba, bb'), ('How many strings are in Σ⁴?', '16'),
           ('How many strings of length 4 start and end with a?', '4'), ('How many strings of length 4 contain at least one b?', '15')],
          ['Every position is a or b.', '2⁴ = 16.', 'The middle two positions are free: 2² = 4.', 'Complement: 16 − 1 (aaaa) = 15.'], 'sigma_or')
    b.orq(7, 'honors', 'Let a_n be the number of bit strings of length n with no two consecutive 0s.',
          [('Find a₁ and a₂.', 'a₁ = 2, a₂ = 3'), ('Explain why a_n = a_(n−1) + a_(n−2) for n ≥ 3.', 'A valid string ends in 1 (any valid string of length n − 1 then 1) or in 10 (any valid string of length n − 2 then 10).'),
           ('Find a₅.', '13'), ('How many bit strings of length 5 DO contain two consecutive 0s?', '19')],
          ['Length 2: 01, 10, 11.', 'Split by the last characters.', 'a₃ = 5, a₄ = 8, a₅ = 13.', '32 − 13 = 19.'], 'no_00_or')


# ---------------------------------------------------------------- error analysis (6 per level)
def errors(b):
    E = b.err
    E(2, 'cp2', 'Write the negation of "All of my friends like pizza."', 'Jordan', ['Negation: "None of my friends like pizza."'],
      'Some of my friends do not like pizza.', 'Jordan negated "all" as "none". "None" is the negation of "some", not of "all".',
      'One friend who does not like pizza is enough to make the original false.', ['¬(for all x, P(x)) ≡ there exists x with ¬P(x).'], 'neg_all_error')
    E(5, 'cp2', 'Let A = {1, 2, 3}. True or false: {1} ∈ A.', 'Sam', ['{1} contains 1, and 1 is in A, so {1} ∈ A is true.'],
      'False', 'Sam confused ∈ with ⊆. {1} ⊆ A is true, but {1} is not one of the listed elements of A.', 'The elements of A are the numbers 1, 2, 3.', ['{1} ∈ A would require {1} to be listed in A.'], 'member_subset_error')
    E(6, 'cp2', 'Let A = {1, 2} and B = {x}. List A × B.', 'Riley', ['A × B = {(x, 1), (x, 2)}'],
      '{(1, x), (2, x)}', 'Riley reversed the coordinates. In A × B the first coordinate comes from A.', 'Ordered pairs are ordered.', ['Pair each a ∈ A with each b ∈ B as (a, b).'], 'product_order_error')
    E(3, 'cp2', 'Is "If 3 is even, then 3 is greater than 10" true or false?', 'Casey', ['The conclusion is false, so the conditional is false.'],
      'True', 'Casey ignored the hypothesis. The hypothesis "3 is even" is false, so the conditional is vacuously true.', 'p → q is false only when p is T and q is F.', ['p = F, q = F, so p → q = T.'], 'vacuous_error')
    E(4, 'cp2', 'How many elements are in {2, 2, 4, 4, 4}?', 'Avery', ['Count the numbers: 5 elements.'],
      '2', 'Avery counted repeated listings. A set contains each element once.', 'Repetition does not create new elements.', ['{2, 2, 4, 4, 4} = {2, 4}.'], 'repeat_count_error')
    E(7, 'cp2', 'How many strings of length 3 can be made from {a, b}?', 'Morgan', ['3 positions × 2 letters = 6.'],
      '8', 'Morgan added/multiplied the wrong numbers. Each position has 2 choices, so the choices multiply: 2·2·2.', 'Multiplication rule: one factor per position.', ['2³ = 8.'], 'string_count_error')
    E(2, 'cp1', 'Negate "For every real number x, if x > 0 then x² > 0."', 'Taylor', ['Negation: "For every real number x, if x > 0 then x² ≤ 0."'],
      'There is a real number x such that x > 0 and x² ≤ 0.', 'Taylor kept "for every" and kept the if-then. The negation of ∀x (P → Q) is ∃x (P ∧ ¬Q).', 'A negated universal statement becomes existential, and ¬(P → Q) ≡ P ∧ ¬Q.',
      ['Switch ∀ to ∃.', 'Replace P → Q by P ∧ ¬Q.'], 'neg_univ_cond_error')
    E(5, 'cp1', 'How many subsets does {a, b, c, d} have?', 'Jamie', ['There are 4 one-element subsets, so 4 subsets... plus ∅, so 5.'],
      '16', 'Jamie counted only the empty set and single elements. Subsets can have 0, 1, 2, 3 or 4 elements.', 'Each element is in or out: 2⁴.', ['1 + 4 + 6 + 4 + 1 = 16.'], 'subset_count_error')
    E(1, 'cp1', 'With domain D = {−2, −1, 0, 1, 2}, find the truth set of "n² = n".', 'Quinn', ['Divide both sides by n: n = 1. Truth set {1}.'],
      '{0, 1}', 'Quinn divided by n, which is not allowed when n = 0, and lost the solution n = 0.', 'Dividing by a variable can discard solutions.', ['n² − n = 0, n(n − 1) = 0, n = 0 or n = 1.', 'Both are in D.'], 'divide_by_variable_error')
    E(3, 'cp1', 'Rewrite "You pass only if you study" in if-then form.', 'Alex', ['If you study, then you pass.'],
      'If you pass, then you study.', 'Alex wrote the converse. "p only if q" means p → q, so the "only if" part is the conclusion.', 'Studying is necessary, not sufficient.', ['p: you pass; q: you study; p → q.'], 'only_if_error')
    E(4, 'cp1', 'Write {n ∈ ℤ | −1 < n ≤ 3} in roster notation.', 'Jordan', ['{−1, 0, 1, 2, 3}'],
      '{0, 1, 2, 3}', 'Jordan included −1, but the strict inequality −1 < n excludes it.', 'Read each inequality symbol carefully.', ['n must satisfy −1 < n and n ≤ 3.'], 'strict_inequality_error')
    E(6, 'cp1', 'Solve (x + y, x − y) = (8, 2).', 'Sam', ['(x + y, x − y) = (8, 2) means x + y = 2 and x − y = 8, so x = 5, y = −3.'],
      '(5, 3)', 'Sam matched the coordinates in the wrong order. First coordinate equals first coordinate.', 'Equal ordered pairs: a = c and b = d.', ['x + y = 8 and x − y = 2.', '2x = 10, x = 5, y = 3.'], 'pair_match_error')
    E(2, 'honors', 'Prove or disprove: "For every real number x, there is a real number y with xy = 1."', 'Riley', ['Take y = 1/x. Then xy = 1. So the statement is true.'],
      'False (counterexample x = 0)', 'Riley divided by x without checking x ≠ 0. For x = 0, xy = 0 for every y.', 'One counterexample disproves a universal statement.', ['For x = 0, 0·y = 0 ≠ 1 for every real y.'], 'universal_reciprocal_error')
    E(2, 'honors', 'Negate "There is a student who has read every book on the list."', 'Casey', ['Negation: "There is a student who has not read every book on the list."'],
      'Every student has failed to read at least one book on the list.', 'Casey did not change the existential quantifier. ¬∃s ∀b R(s, b) ≡ ∀s ∃b ¬R(s, b).', 'Each quantifier flips when a negation passes through it.', ['∃s → ∀s, ∀b → ∃b, R → ¬R.'], 'nested_neg_error')
    E(1, 'honors', 'Is "For every n ∈ ℤ⁺, n² + n + 41 is prime" true? Justify.', 'Avery', ['n = 1: 43, n = 2: 47, n = 3: 53, n = 4: 61, n = 5: 71, all prime. The pattern holds, so it is true.'],
      'False (n = 40 gives 1681 = 41²)', 'Avery treated examples as a proof of a universal statement.', 'Finitely many examples never prove a statement about all positive integers.', ['40² + 40 + 41 = 1681 = 41 · 41.'], 'examples_not_proof_error')
    E(5, 'honors', 'Let A = {∅}. How many subsets does A have, and what are they?', 'Morgan', ['A is empty, so its only subset is ∅. 1 subset.'],
      '2: ∅ and {∅}', 'Morgan treated {∅} as the empty set. {∅} has one element (namely ∅), so it has 2¹ = 2 subsets.', '∅ has no elements; {∅} has one.', ['Subsets of {∅}: ∅ and {∅}.'], 'empty_set_error')
    E(6, 'honors', 'Prove or disprove: A × B = B × A for all sets A and B.', 'Taylor', ['|A × B| = |A|·|B| = |B|·|A| = |B × A|, so the sets are equal.'],
      'False; for example A = {1}, B = {2}: A × B = {(1, 2)} but B × A = {(2, 1)}', 'Taylor showed only that the sets have the same size. Same size does not mean the same elements.', 'Set equality requires the same elements.',
      ['Use a counterexample with A ≠ B and both nonempty.'], 'product_commute_error')
    E(7, 'honors', 'How many bit strings of length 6 contain at least one 1?', 'Jamie', ['Choose where the 1 goes: 6 ways. The other 5 bits are free: 2⁵ = 32. Total 6 · 32 = 192.'],
      '63', 'Jamie overcounted: a string with several 1s is counted once for each 1. Also 192 > 2⁶ = 64, which is impossible.', 'Use the complement rule instead.', ['All strings: 2⁶ = 64. Strings with no 1: 1.', '64 − 1 = 63.'], 'at_least_one_error')


def extra567(b):
    # skill 5: choose the symbol (computed from Python sets)
    SYM = [('4', {2, 4, 6}, 'cp2'), ('{4}', {2, 4, 6}, 'cp2'), ('{2, 6}', {2, 4, 6}, 'cp2'), ('7', {2, 4, 6}, 'cp1'), ('{2, 4, 6}', {2, 4, 6}, 'honors')]
    for x, S, L in SYM:
        if x.startswith('{'):
            X = {int(t) for t in x.strip('{}').split(',')}
            ans = '=' if X == S else '⊊' if X < S else '⊄'
        else:
            ans = '∈' if int(x) in S else '∉'
        b.mc(5, L, 'Which symbol makes this statement true?  %s ☐ %s  (⊊ means "is a proper subset of", ⊄ means "is not a subset of")' % (x, fmt_set(S)),
             ans, [y for y in ['∈', '∉', '⊊', '=', '⊄'] if y != ans][:4],
             ['Decide first whether the left side is an element (a number) or a set.', 'Elements use ∈ or ∉; sets use ⊆, ⊊ or =.', 'Answer: %s %s %s' % (x, ans, fmt_set(S))], 'choose_symbol')
    # skill 5: is A a subset of B for builder sets (computed on a window of integers)
    SUB = [('A = {n ∈ ℤ | n is a multiple of 6}', lambda n: n % 6 == 0, 'B = {n ∈ ℤ | n is a multiple of 3}', lambda n: n % 3 == 0, 'cp1', 'Every multiple of 6 is 6k = 3(2k), a multiple of 3.'),
           ('A = {n ∈ ℤ | n is a multiple of 3}', lambda n: n % 3 == 0, 'B = {n ∈ ℤ | n is a multiple of 6}', lambda n: n % 6 == 0, 'cp2', '3 is in A but not in B.'),
           ('A = {x ∈ ℤ | x² < 9}', lambda n: n * n < 9, 'B = {x ∈ ℤ | |x| ≤ 2}', lambda n: abs(n) <= 2, 'honors', 'x² < 9 for an integer x means x ∈ {−2, −1, 0, 1, 2}, so A = B and A ⊆ B.')]
    for a, fa, bb, fb, L, why in SUB:
        win = range(-60, 61)
        t = all(fb(n) for n in win if fa(n))
        b.mc(5, L, 'Let %s and %s. Is A ⊆ B?' % (a, bb), 'Yes' if t else 'No', ['No' if t else 'Yes', 'Only if A = B', 'Cannot be decided'], [why], 'builder_subset')
    # skill 6
    b.sa(6, 'cp2', 'A coin (H or T) is tossed and then a die (1 to 6) is rolled. Each outcome is an ordered pair. How many outcomes are in {H, T} × {1, 2, 3, 4, 5, 6}?', 12,
         ['|{H, T}| · |{1, ..., 6}| = 2 · 6.', '12 outcomes.'], 'product_context')
    b.mc(6, 'cp2', 'Which ordered pair is in {1, 2, 3} × {a, b}?', '(3, b)', ['(b, 3)', '(4, a)', '(a, b)'],
         ['The first coordinate must be 1, 2 or 3 and the second must be a or b.'], 'product_member')
    b.mc(6, 'honors', 'If |A × B| = 15 and A has 3 elements, how many elements does B × B × A have?', '75', ['45', '30', '225'],
         ['|B| = 15 / 3 = 5.', '|B × B × A| = 5 · 5 · 3 = 75.'], 'product_size_reverse')
    b.mc(6, 'honors', 'How many ordered pairs (x, y) in {1, 2, 3, 4, 5} × {1, 2, 3, 4, 5} satisfy x + y = 6?', str(sum(1 for x in range(1, 6) for y in range(1, 6) if x + y == 6)), ['4', '10', '6'],
         ['List them: (1, 5), (2, 4), (3, 3), (4, 2), (5, 1).', 'Order matters, so (1, 5) and (5, 1) are different: 5 pairs.'], 'product_condition')
    b.sa(6, 'honors', 'How many elements of {0, 1}³ (= {0, 1} × {0, 1} × {0, 1}) have coordinates that add to 2?', 3,
         ['The triples are (1, 1, 0), (1, 0, 1), (0, 1, 1).', '3'], 'product_condition')
    # skill 7
    b.sa(7, 'cp2', 'Using only the letters A and B, how many 2-letter strings can be made? (Letters may repeat.)', 4, ['AA, AB, BA, BB.', '2² = 4'], 'count_strings')
    b.mc(7, 'cp2', 'What is the reverse of the string "STOP"?', 'POTS', ['SPOT', 'TOPS', 'STOP'], ['Write the characters in the opposite order.', 'POTS'], 'reverse_string')
    b.mc(7, 'cp1', 'How many bit strings of length 6 begin with 1 and end with 0?', '16', ['64', '32', '12'], ['The first and last bits are fixed.', 'The middle 4 bits are free: 2⁴ = 16.'], 'count_bits_fixed')
    b.sa(7, 'cp1', 'How many 4-character PINs use only the digits 0 to 9 with NO digit repeated?', 10 * 9 * 8 * 7, ['10 choices, then 9, then 8, then 7.', '10 · 9 · 8 · 7 = 5040'], 'count_no_repeat')
    b.mc(7, 'honors', 'How many bit strings of length 8 have more 1s than 0s?', str(sum(1 for p in itertools.product('01', repeat=8) if p.count('1') > 4)), ['128', '256', '70'],
         ['By symmetry, strings with more 1s and strings with more 0s are equally common.', 'Exactly four 1s: C(8, 4) = 70. So (256 − 70) / 2 = 93.'], 'count_bits_majority')
    b.sa(7, 'honors', 'A string over {a, b, c} has length 4. How many such strings contain at least one a?', 3 ** 4 - 2 ** 4, ['Complement: strings with no a use only b and c: 2⁴ = 16.', '3⁴ − 2⁴ = 81 − 16 = 65.'], 'count_complement')
    b.mc(7, 'honors', 'Which description matches the set {λ, 0, 00, 000, ...} where λ is the empty string?', 'All strings over {0} (that is, {0}*)', ['All bit strings', 'All strings of positive length over {0}', 'The set {0}'],
         ['It contains λ and every finite run of 0s.', 'That is exactly Σ* for Σ = {0}.'], 'sigma_star')
