"""Unit 5: Set Theory (8 skills). All set results computed with Python sets; every complement names its universe."""
import itertools
from core import Bank, fmt_set, seeded
import figs

U = 'set-theory'


def build():
    b = Bank(U, 'st', 8)
    for f in (s1, s2, s3, s4, s5, s6, s7, s8, topup, topup2, errors):
        f(b)
    return b


def wrong_sets(right, pool, rng, k=3):
    """Distractor sets built from typical mistakes: add/remove one element, or a related operation."""
    out = []
    right = set(right)
    for x in sorted(pool):
        if x not in right:
            out.append(right | {x})
            break
    for x in sorted(right):
        out.append(right - {x})
        break
    out.append(set(pool) - right)
    res = []
    for s in out:
        t = fmt_set(s)
        if t != fmt_set(right) and t not in res:
            res.append(t)
    return res


# ---------------------------------------------------------------- 1. equality and empty set
def s1(b):
    EQ = [('cp2', '{1, 2, 3}', '{3, 1, 2}', True, 'Order does not matter.'), ('cp2', '{a, b}', '{a, b, b}', True, 'Repeated listings do not add elements.'),
          ('cp2', '{0}', '∅', False, '{0} has one element; ∅ has none.'), ('cp1', '{x ∈ ℤ | x² = 4}', '{−2, 2}', True, 'The solutions of x² = 4 in ℤ are ±2.'),
          ('cp1', '∅', '{∅}', False, '{∅} has one element, namely ∅.'), ('cp1', '{n ∈ ℤ | 1 < n < 2}', '∅', True, 'No integer lies strictly between 1 and 2.'),
          ('honors', '{x ∈ ℝ | x² + 1 = 0}', '{x ∈ ℤ | x is even and odd}', True, 'Both are empty, and there is only one empty set.'),
          ('honors', '{{1}, {2}}', '{1, 2}', False, 'The left set contains sets; the right set contains numbers.'),
          ('honors', '{n ∈ ℤ | n = 2k for some k ∈ ℤ}', '{n ∈ ℤ | n = 2k − 2 for some k ∈ ℤ}', True, 'If n = 2k then n = 2(k + 1) − 2, and conversely; both are the even integers.')]
    for L, A, B, eq, why in EQ:
        b.mc(1, L, 'Are the sets %s and %s equal?' % (A, B), 'Yes: they have exactly the same elements' if eq else 'No: one set has an element the other does not',
             ['No: one set has an element the other does not' if eq else 'Yes: they have exactly the same elements', 'Yes: they have the same number of elements', 'No: they are written differently'],
             [why, 'Sets are equal when each is a subset of the other (same elements).'], 'set_equal')
    b.sel(1, 'cp2', 'Which sets are equal to ∅?', [('{n ∈ ℕ | n < 1}', True), ('{x ∈ ℝ | x ≠ x}', True), ('{0}', False), ('{∅}', False), ('{ }', True)],
          ['ℕ = {1, 2, 3, ...} has no element below 1; no x satisfies x ≠ x; { } is another way to write ∅.', '{0} and {∅} each have one element.'], 'empty_select')
    b.sel(1, 'cp1', 'Let A = {1, 2}, B = {2, 1, 1}, C = {x ∈ ℤ | 0 < x < 3}, D = {1, 2, 3}. Which statements are true?',
          [('A = B', True), ('A = C', True), ('B = D', False), ('A ⊆ D', True), ('D ⊆ A', False)], ['A, B and C all equal {1, 2}.'], 'equal_select')
    b.sel(1, 'honors', 'Which statements about the empty set are true?', [('∅ ⊆ A for every set A', True), ('∅ ∈ {∅}', True), ('∅ ⊆ ∅', True), ('∅ ∈ ∅', False), ('|{∅}| = 0', False)],
          ['The empty set is a subset of every set, including itself; ∅ is an element of {∅}; nothing is an element of ∅; |{∅}| = 1.'], 'empty_select')
    b.sa(1, 'cp2', 'How many elements does {2, 4, 4, 6, 2} have?', 3, ['Repeated elements count once: {2, 4, 6}.'], 'distinct_count')
    b.sa(1, 'cp1', 'How many elements does {∅, {∅}, {∅, {∅}}} have?', 3, ['Its elements are ∅, {∅} and {∅, {∅}}: three different sets.'], 'distinct_count')
    b.sa(1, 'honors', 'Let A = {x ∈ ℤ | x² < 10} and B = {x ∈ ℤ | −3 ≤ x ≤ 3}. List B − A in roster notation (∅ if empty).', '∅',
         ['A = {−3, −2, −1, 0, 1, 2, 3} because 9 < 10.', 'B is the same set, so B − A = ∅ and A = B.'], 'equal_check')
    b.orq(1, 'cp2', 'Let P = {letters in the word "BOOK"} and Q = {letters in the word "KOB"}.',
          [('List P.', '{B, K, O}'), ('List Q.', '{B, K, O}'), ('Is P = Q? Explain.', 'Yes; they have the same elements (order and repeats do not matter).'), ('How many elements does P have?', '3')],
          ['Each letter once.', 'Same letters.', 'Same elements.', 'Count.'], 'equal_or')
    b.orq(1, 'cp1', 'Compare ∅, {∅} and {0}.',
          [('How many elements does each have?', '0, 1, 1'), ('Is ∅ = {∅}?', 'No'), ('Is ∅ ⊆ {0}?', 'Yes'), ('Is ∅ ∈ {0}?', 'No')],
          ['∅ is empty; the others have one element each.', 'Different sizes.', 'The empty set is a subset of every set.', '{0} contains only 0.'], 'empty_or')
    b.orq(1, 'honors', 'Prove there is only one empty set.',
          [('Suppose ∅₁ and ∅₂ are both sets with no elements. Why is ∅₁ ⊆ ∅₂?', 'Vacuously: there is no element of ∅₁ that could fail to be in ∅₂.'), ('Why is ∅₂ ⊆ ∅₁?', 'Same reason.'),
           ('What do the two inclusions show?', '∅₁ = ∅₂'), ('Why does this justify writing "the" empty set?', 'Any two empty sets are equal, so there is exactly one.')],
          ['A conditional with false hypothesis is true.', 'Symmetric.', 'Set equality = mutual inclusion.', 'Uniqueness.'], 'empty_proof_or')


# ---------------------------------------------------------------- 2. union, intersection, difference
def rand_sets(rng, pool, ka, kb):
    pool = list(pool)
    A = set(rng.sample(pool, ka))
    B = set(rng.sample(pool, kb))
    return A, B


def s2(b):
    ops = [('∪', lambda A, B: A | B, 'union: elements in A or B (or both)'), ('∩', lambda A, B: A & B, 'intersection: elements in both A and B'),
           ('−', lambda A, B: A - B, 'difference: elements in A but not in B'), ('− (reversed)', lambda A, B: B - A, 'difference: elements in B but not in A')]
    for L, pool, ka, kb, nq in (('cp2', range(1, 10), 4, 4, 6), ('cp1', range(1, 16), 6, 5, 6), ('honors', range(-5, 13), 7, 6, 5)):
        rng = seeded('u5s2', L)
        for i in range(nq):
            A, B = rand_sets(rng, pool, ka, kb)
            sym, f, desc = ops[i % 4]
            expr = 'B − A' if sym == '− (reversed)' else 'A %s B' % sym
            R = f(A, B)
            if L == 'cp2' or i % 2 == 0:
                b.sa(2, L, 'Let A = %s and B = %s. Find %s. Write the set in roster notation, elements in increasing order (∅ if empty).' % (fmt_set(A), fmt_set(B), expr), fmt_set(R),
                     ['%s is the %s.' % (expr, desc), '%s = %s' % (expr, fmt_set(R))], 'set_op')
            else:
                b.mc(2, L, 'Let A = %s and B = %s. Find %s.' % (fmt_set(A), fmt_set(B), expr), fmt_set(R), wrong_sets(R, A | B, rng) + [fmt_set(A & B if sym != '∩' else A | B)],
                     ['%s is the %s.' % (expr, desc), '%s = %s' % (expr, fmt_set(R))], 'set_op')
    CTX = [('cp2', 'Soccer players S = {Ana, Ben, Cy, Dee} and band members M = {Ben, Dee, Eli}. Who is in both?', '{Ben, Dee}'),
           ('cp1', 'Students taking Spanish: {Ava, Bo, Cam, Dot}. Taking French: {Bo, Eve, Fay}. Who takes Spanish but not French?', '{Ava, Cam, Dot}'),
           ('honors', 'A = {multiples of 4 from 1 to 30}, B = {multiples of 6 from 1 to 30}. Find A ∩ B.', '{12, 24}')]
    for L, t, a in CTX:
        b.sa(2, L, t + ' Write the answer as a set in alphabetical/increasing order.', a, ['Identify the operation (both → ∩, but not → −).', a], 'set_context')
    b.sel(2, 'cp2', 'Let A = {1, 2, 3, 4} and B = {3, 4, 5}. Which statements are true?',
          [('A ∪ B = {1, 2, 3, 4, 5}', True), ('A ∩ B = {3, 4}', True), ('A − B = {1, 2}', True), ('B − A = {1, 2}', False), ('A ∩ B = {1, 2, 3, 4, 5}', False)],
          ['Compute each: B − A = {5}.'], 'set_op_select')
    b.sel(2, 'cp1', 'For ANY sets A and B, which statements are always true?', [('A ∩ B ⊆ A', True), ('A ⊆ A ∪ B', True), ('A − B ⊆ A', True), ('A ∪ B ⊆ A', False), ('A − B = B − A', False)],
          ['Intersection and difference shrink A; union grows it. A − B = B − A only when A = B.'], 'set_op_select')
    b.sel(2, 'honors', 'Let A = {n ∈ ℤ | n is a multiple of 2} and B = {n ∈ ℤ | n is a multiple of 3}. Which statements are true?',
          [('A ∩ B is the set of multiples of 6', True), ('9 ∈ B − A', True), ('6 ∈ A − B', False), ('A ∪ B contains 15', True), ('A ∪ B = ℤ', False)],
          ['lcm(2, 3) = 6; 9 is a multiple of 3 but not 2; 15 is a multiple of 3; 1 is in neither set.'], 'set_op_select')
    b.orq(2, 'cp2', 'Let A = {2, 4, 6, 8} and B = {1, 2, 3, 4}.',
          [('Find A ∪ B.', '{1, 2, 3, 4, 6, 8}'), ('Find A ∩ B.', '{2, 4}'), ('Find A − B.', '{6, 8}'), ('Find B − A.', '{1, 3}')],
          ['All elements.', 'Common.', 'In A only.', 'In B only.'], 'set_op_or')
    b.orq(2, 'cp1', 'Let A = {x ∈ ℤ | 0 ≤ x ≤ 6} and B = {x ∈ ℤ | 4 ≤ x ≤ 9}.',
          [('Find A ∩ B.', '{4, 5, 6}'), ('Find A − B.', '{0, 1, 2, 3}'), ('Find |A ∪ B|.', '10'), ('Check |A ∪ B| = |A| + |B| − |A ∩ B|.', '7 + 6 − 3 = 10')],
          ['Overlap.', 'In A only.', '0 through 9.', 'Inclusion-exclusion.'], 'set_op_or')
    b.orq(2, 'honors', 'Let A = [0, 5) and B = [3, 8] be intervals of real numbers.',
          [('Find A ∩ B.', '[3, 5)'), ('Find A ∪ B.', '[0, 8]'), ('Find A − B.', '[0, 3)'), ('Find B − A.', '[5, 8]')],
          ['Overlap from 3 up to (not including) 5.', 'Combine.', 'Remove [3, 8].', '5 is in B but not in A.'], 'interval_or')


# ---------------------------------------------------------------- 3. complements
def s3(b):
    for L, Up, ka, kb, nq in (('cp2', list(range(1, 11)), 4, 3, 5), ('cp1', list(range(1, 13)), 5, 5, 5), ('honors', list('abcdefghij'), 5, 4, 5)):
        rng = seeded('u5s3', L)
        Uset = set(Up)
        exprs = {'cp2': ["A'", "B'", "(A ∪ B)'", "A' ∩ B", "A ∩ B'"],
                 'cp1': ["(A ∩ B)'", "A' ∪ B'", "A' ∩ B'", "(A − B)'", "A' − B"],
                 'honors': ["(A ∪ B)' ∪ (A ∩ B)", "A' ∩ (A ∪ B)", "(A' ∪ B)'", "(A ∩ B') ∪ (A' ∩ B)", "((A ∩ B)' ∩ A)'"]}[L]
        for i in range(nq):
            A, B = rand_sets(rng, Up, ka, kb)
            c = lambda X: Uset - X
            ev = {"A'": lambda: c(A), "B'": lambda: c(B), "(A ∪ B)'": lambda: c(A | B), "A' ∩ B": lambda: c(A) & B, "A ∩ B'": lambda: A & c(B),
                  "(A ∩ B)'": lambda: c(A & B), "A' ∪ B'": lambda: c(A) | c(B), "A' ∩ B'": lambda: c(A) & c(B), "(A − B)'": lambda: c(A - B), "A' − B": lambda: c(A) - B,
                  "(A ∪ B)' ∪ (A ∩ B)": lambda: c(A | B) | (A & B), "A' ∩ (A ∪ B)": lambda: c(A) & (A | B), "(A' ∪ B)'": lambda: c(c(A) | B),
                  "(A ∩ B') ∪ (A' ∩ B)": lambda: (A & c(B)) | (c(A) & B), "((A ∩ B)' ∩ A)'": lambda: c(c(A & B) & A)}
            e = exprs[i]
            R = ev[e]()
            pre = 'Universe U = %s. Let A = %s and B = %s. ' % (fmt_set(Uset), fmt_set(A), fmt_set(B))
            if i % 2 == 0:
                b.sa(3, L, pre + 'Find %s (the complement is taken in U). Use roster notation, ordered, ∅ if empty.' % e, fmt_set(R),
                     ["X' = U − X.", 'Work inside parentheses first.', '%s = %s' % (e, fmt_set(R))], 'complement_op')
            else:
                b.mc(3, L, pre + 'Find %s (the complement is taken in U).' % e, fmt_set(R), wrong_sets(R, Uset, rng) + [fmt_set(A ^ B)],
                     ["X' = U − X.", '%s = %s' % (e, fmt_set(R))], 'complement_op')
    b.mc(3, 'cp2', 'Universe U = {1, 2, 3, 4, 5}. If A = {1, 2}, what is A\'?', '{3, 4, 5}', ['{1, 2}', '∅', '{1, 2, 3, 4, 5}'], ["A' = U − A."], 'complement_basic')
    b.mc(3, 'cp1', "Which expression is equal to (A ∪ B)' for all sets in a universe U?", "A' ∩ B'", ["A' ∪ B'", "A ∩ B", "(A ∩ B)'"], ["De Morgan's law for sets."], 'demorgan_sets')
    b.mc(3, 'honors', 'Let U = ℤ (all integers) and E = the even integers. Which set is E\'?', 'The odd integers', ['∅', 'The negative integers', 'The integers that are not divisible by 4'],
         ['The complement in ℤ of the evens is the odds.', 'The answer depends on the universe: in U = ℕ, E\' would be the positive odd numbers.'], 'complement_universe')
    b.sel(3, 'cp1', 'For any sets A, B in a universe U, which statements are always true?', [("(A')' = A", True), ("A ∩ A' = ∅", True), ("A ∪ A' = U", True), ("A − B = A ∩ B'", True), ("(A ∩ B)' = A' ∩ B'", False)],
          ["Double complement, complement laws, and the set-difference law hold; De Morgan gives (A ∩ B)' = A' ∪ B'."], 'complement_select')
    b.sel(3, 'cp2', 'Universe U = {a, b, c, d, e}, A = {a, c}. Which elements are in A\'?', [('b', True), ('d', True), ('e', True), ('a', False), ('c', False)], ["A' = {b, d, e}."], 'complement_select')
    b.sel(3, 'honors', 'Let U = ℝ, A = (−∞, 2] and B = (0, 5). Which numbers are in A\' ∩ B?', [('3', True), ('4.9', True), ('2.5', True), ('2', False), ('5', False)],
          ["A' = (2, ∞), so A' ∩ B = (2, 5)."], 'complement_select')
    b.orq(3, 'cp2', 'U = {1, 2, ..., 8}, A = {1, 3, 5, 7}, B = {1, 2, 3}.',
          [("Find A'.", '{2, 4, 6, 8}'), ("Find B'.", '{4, 5, 6, 7, 8}'), ("Find A' ∩ B'.", '{4, 6, 8}'), ("Find (A ∪ B)' and compare.", '{4, 6, 8}; it matches (De Morgan).')],
          ['U − A.', 'U − B.', 'Common.', 'A ∪ B = {1, 2, 3, 5, 7}.'], 'complement_or')
    b.orq(3, 'cp1', 'U = {students in a class of 30}. F = plays football (12 students), H = in honor roll (10), and 4 are in both.',
          [("Find |F'|.", '18'), ('Find |F ∪ H|.', '18'), ("Find |(F ∪ H)'|.", '12'), ("Describe (F ∪ H)' in words.", 'Students who neither play football nor are on the honor roll.')],
          ['30 − 12.', '12 + 10 − 4.', '30 − 18.', 'Neither.'], 'complement_or')
    b.orq(3, 'honors', 'Let U = ℤ, A = multiples of 2, B = multiples of 3.',
          [("Describe A' ∩ B'.", 'Integers divisible by neither 2 nor 3'), ("List the elements of A' ∩ B' between 1 and 20.", '1, 5, 7, 11, 13, 17, 19'),
           ("Describe (A ∩ B)'.", 'Integers that are not multiples of 6'), ("Is 9 in (A ∩ B)'? Is 9 in A' ∪ B'?", 'Yes and yes (De Morgan).')],
          ['Neither.', 'Check each.', 'Complement of multiples of 6.', '9 is odd.'], 'complement_or')


# ---------------------------------------------------------------- 4. Venn diagrams
def s4(b):
    # two-set diagram with element lists
    p1 = figs.venn(U, 'venn2_letters', {'AB': 'c, e', 'A': 'a, b', 'B': 'f, g', '': 'h'}, labels=('A', 'B'))
    for L, e, ans in (('cp2', 'A ∩ B', '{c, e}'), ('cp2', 'A', '{a, b, c, e}'), ('cp1', 'A − B', '{a, b}'), ('cp1', "(A ∪ B)'", '{h}')):
        r = b.sa(4, L, 'Use the Venn diagram (universe U is the rectangle). Find %s. List elements in alphabetical order.' % e, ans,
                 ['Read the regions: only A = {a, b}; both = {c, e}; only B = {f, g}; outside = {h}.', '%s = %s' % (e, ans)], 'venn_read')
        b.image(r, p1, 'Venn diagram: only A has a, b; both A and B have c, e; only B has f, g; outside both is h.')
    # three-set diagram with counts
    counts = {'ABC': 3, 'AB': 5, 'AC': 2, 'BC': 4, 'A': 8, 'B': 6, 'C': 7, '': 5}
    p2 = figs.venn(U, 'venn3_counts', counts, labels=('A', 'B', 'C'))
    tot = sum(counts.values())
    Q = [('cp2', 'How many elements are in A (all parts of circle A)?', counts['A'] + counts['AB'] + counts['AC'] + counts['ABC']),
         ('cp1', 'How many elements are in exactly one of the three sets?', counts['A'] + counts['B'] + counts['C']),
         ('cp1', 'How many elements are in A ∩ B?', counts['AB'] + counts['ABC']),
         ('honors', 'How many elements are in at least two of the sets?', counts['AB'] + counts['AC'] + counts['BC'] + counts['ABC']),
         ('honors', "How many elements are in (A ∪ B)' ∩ C?", counts['C']),
         ('honors', 'How many elements are in the universe?', tot)]
    for L, t, v in Q:
        r = b.sa(4, L, 'The Venn diagram shows the NUMBER of elements in each region. ' + t, v,
                 ['Region counts: A only 8, B only 6, C only 7, A∩B only 5, A∩C only 2, B∩C only 4, all three 3, outside 5.', 'Answer: %d' % v], 'venn_count')
        b.image(r, p2, 'Three-set Venn diagram with region counts: A only 8, B only 6, C only 7, A and B only 5, A and C only 2, B and C only 4, all three 3, outside 5.')
    # shaded region identification
    SH = [('cp2', ['A'], 'A − B', ['A ∩ B', 'B − A', "(A ∪ B)'"]), ('cp1', ['A', 'B'], 'A ⊕ B (in exactly one set)', ['A ∪ B', 'A ∩ B', "(A ∩ B)'"]),
          ('cp1', ['', 'AB'], "(A ∪ B)' ∪ (A ∩ B)", ["(A ∩ B)'", 'A ∪ B', "A' ∩ B'"]), ('cp2', ['B', ''], "A'", ["B'", 'B − A', "(A ∪ B)'"])]
    for k, (L, sh, good, bad) in enumerate(SH):
        keys = [('AB' if s == 'AB' else s) for s in sh]
        p = figs.venn(U, 'venn2_shade_%d' % k, {}, labels=('A', 'B'), shade=keys)
        r = b.mc(4, L, 'Which expression describes the shaded region of the Venn diagram (universe U is the rectangle)?', good, bad,
                 ['Shaded regions: ' + ', '.join({'A': 'A only', 'B': 'B only', 'AB': 'A and B', '': 'outside both'}[s] for s in sh) + '.', good], 'venn_shade')
        b.image(r, p, 'Two-set Venn diagram with shaded regions: ' + ', '.join({'A': 'A only', 'B': 'B only', 'AB': 'both A and B', '': 'outside both circles'}[s] for s in sh) + '.')
    SH3 = [('honors', ['AB', 'ABC', 'AC'], 'A ∩ (B ∪ C)', ['A ∪ (B ∩ C)', '(A ∩ B) ∪ C', 'A ∩ B ∩ C']), ('honors', ['C', 'AC', 'BC'], "C − (A ∩ B ∩ C)... no: C ∩ (A ∩ B)'", ['C − A', 'C − B', "C ∩ (A ∪ B)'"])]
    for k, (L, sh, good, bad) in enumerate(SH3):
        good = good.split('... no: ')[-1]
        p = figs.venn(U, 'venn3_shade_%d' % k, {}, labels=('A', 'B', 'C'), shade=sh)
        r = b.mc(4, L, 'Which expression describes the shaded region of the three-set Venn diagram?', good, bad,
                 ['Shaded: ' + ', '.join(sh) + ' regions.', good], 'venn_shade')
        b.image(r, p, 'Three-set Venn diagram with these regions shaded: ' + ', '.join({'AB': 'A and B only', 'ABC': 'all three', 'AC': 'A and C only', 'C': 'C only', 'BC': 'B and C only'}[s] for s in sh) + '.')
    # inclusion-exclusion word problems
    IE = [('cp2', 'In a class, 15 students like pizza, 12 like tacos, and 7 like both. How many like pizza or tacos?', 20),
          ('cp1', '40 students were surveyed: 22 play a sport, 18 play an instrument, and 9 do neither. How many do both?', 22 + 18 - (40 - 9)),
          ('honors', 'Of 100 people, 45 read news online, 38 watch TV news, 25 listen to radio news, 15 do online and TV, 10 online and radio, 8 TV and radio, and 4 all three. How many use none?', 100 - (45 + 38 + 25 - 15 - 10 - 8 + 4)),
          ('cp1', 'How many integers from 1 to 100 are divisible by 3 or 5?', len([n for n in range(1, 101) if n % 3 == 0 or n % 5 == 0])),
          ('honors', 'How many integers from 1 to 1000 are divisible by none of 2, 3, 5?', len([n for n in range(1, 1001) if n % 2 and n % 3 and n % 5]))]
    for L, t, v in IE:
        b.sa(4, L, t + ' (Draw a Venn diagram.)', v, ['Use |A ∪ B| = |A| + |B| − |A ∩ B| (and the three-set version).', 'Answer: %d' % v], 'inclusion_exclusion')
    b.sel(4, 'cp2', 'Using the two-set diagram with A only = {a, b}, both = {c, e}, B only = {f, g}, outside = {h}: which elements are in A ∪ B?',
          [('a', True), ('c', True), ('g', True), ('h', False)], ['A ∪ B is every element inside a circle.'], 'venn_select')
    b.orq(4, 'cp1', 'In a club of 50: 28 like chess (C), 20 like go (G), and 8 like both.',
          [('How many like only chess?', '20'), ('How many like only go?', '12'), ('How many like neither?', '10'), ('Describe where the 8 go in a Venn diagram.', 'In the overlap C ∩ G.')],
          ['28 − 8.', '20 − 8.', '50 − (20 + 12 + 8).', 'Both.'], 'venn_or')
    b.orq(4, 'honors', 'Survey of 60 students: 30 take Art (A), 25 Band (B), 20 Chorus (C); 10 A and B, 8 A and C, 6 B and C, 3 all three.',
          [('How many take A and B but not C?', '7'), ('How many take exactly one of the three?', str((30 - 10 - 8 + 3) + (25 - 10 - 6 + 3) + (20 - 8 - 6 + 3))),
           ('How many take none?', str(60 - (30 + 25 + 20 - 10 - 8 - 6 + 3))), ('Check that the eight region counts add to 60.', '15 + 12 + 9 + 7 + 5 + 3 + 3 + 6 = 60')],
          ['10 − 3.', 'A only 15, B only 12, C only 9.', 'Inclusion-exclusion: 54 in at least one.', 'Sum all regions.'], 'venn_or')
    b.orq(4, 'cp2', 'Use the two-set Venn diagram: A only {a, b}, both {c, e}, B only {f, g}, outside {h}.',
          [('List B.', '{c, e, f, g}'), ('List A ∩ B.', '{c, e}'), ('List B − A.', '{f, g}'), ('How many elements are in U?', '7')],
          ['Inside B.', 'Overlap.', 'B only.', 'Count every element.'], 'venn_or')


# ---------------------------------------------------------------- 5. power sets
def s5(b):
    for L, S in (('cp2', ['a', 'b']), ('cp1', [1, 2, 3]), ('honors', ['∅', 1])):
        P = [set(c) for r in range(len(S) + 1) for c in itertools.combinations(S, r)]
        disp = '{' + ', '.join(str(x) for x in S) + '}'
        listing = ', '.join('∅' if not p else '{' + ', '.join(str(x) for x in S if x in p) + '}' for p in P)
        b.sa(5, L, 'List the elements of P(%s), the power set. Write subsets by size, then in the original order, separated by commas, e.g. ∅, {a}, ...' % disp, listing,
             ['P(S) contains every subset of S, including ∅ and S.', 'P(%s) = {%s}' % (disp, listing)], 'list_power_set')
    for n, L in ((2, 'cp2'), (3, 'cp2'), (5, 'cp1'), (0, 'cp1'), (10, 'honors')):
        b.mc(5, L, 'A set has %d elements. How many elements does its power set have?' % n, str(2 ** n), [str(2 * n), str(n * n), str(2 ** n - 1)] if n != 2 else ['8', '3', '2'],
             ['|P(S)| = 2^|S|.', '2^%d = %d' % (n, 2 ** n)], 'power_set_size', order='sort')
    b.sa(5, 'honors', 'How many elements does P(P({1, 2})) have?', 16, ['|P({1, 2})| = 4.', '|P(P({1, 2}))| = 2⁴ = 16.'], 'power_set_size')
    b.sa(5, 'cp1', 'How many elements of P({1, 2, 3, 4}) contain the element 3?', 8, ['3 is fixed in; the other three elements are free: 2³ = 8.'], 'power_set_count')
    b.sa(5, 'honors', 'How many elements of P({1, 2, 3, 4, 5, 6}) have an even number of elements?', 32, ['C(6,0) + C(6,2) + C(6,4) + C(6,6) = 1 + 15 + 15 + 1 = 32 (half of 64).'], 'power_set_count')
    b.sel(5, 'cp2', 'Let S = {x, y}. Which are elements of P(S)?', [('∅', True), ('{x}', True), ('{x, y}', True), ('x', False), ('{y, z}', False)], ['Elements of P(S) are subsets of S.'], 'power_select')
    b.sel(5, 'cp1', 'Let A = {1, 2, 3}. Which statements are true?', [('{1, 3} ∈ P(A)', True), ('∅ ∈ P(A)', True), ('{∅} ⊆ P(A)', True), ('1 ∈ P(A)', False), ('{1, 4} ∈ P(A)', False)],
          ['{∅} ⊆ P(A) because ∅ ∈ P(A).', '1 is not a subset; {1, 4} is not a subset of A.'], 'power_select')
    b.sel(5, 'honors', 'For all sets A and B, which statements are true?', [('P(A ∩ B) = P(A) ∩ P(B)', True), ('P(A) ∪ P(B) ⊆ P(A ∪ B)', True), ('A ⊆ B implies P(A) ⊆ P(B)', True),
                                                                         ('P(A ∪ B) = P(A) ∪ P(B)', False), ('P(A − B) = P(A) − P(B)', False)],
          ['A counterexample for union: A = {1}, B = {2}: {1, 2} ∈ P(A ∪ B) but not in P(A) ∪ P(B).', 'For difference: ∅ ∈ P(A − B) but ∅ ∉ P(A) − P(B).'], 'power_select')
    b.orq(5, 'cp2', 'Let T = {red, blue, green}.',
          [('How many subsets does T have?', '8'), ('List the subsets with exactly one element.', '{red}, {blue}, {green}'), ('List the subsets with exactly two elements.', '{red, blue}, {red, green}, {blue, green}'), ('Which subsets are missing from your lists so far?', '∅ and T itself')],
          ['2³.', 'Singletons.', 'Pairs.', 'Size 0 and size 3.'], 'power_or')
    b.orq(5, 'cp1', 'Let A = {1, 2}.',
          [('Find P(A).', '{∅, {1}, {2}, {1, 2}}'), ('Find |P(A)|.', '4'), ('Find P(A) ∩ P({2, 3}).', '{∅, {2}}'), ('Is {1} ∈ P(A) or {1} ⊆ P(A)?', '{1} ∈ P(A); {1} ⊄ P(A) because 1 ∉ P(A).')],
          ['All subsets.', '2².', 'Common subsets.', 'Elements vs subsets.'], 'power_or')
    b.orq(5, 'honors', 'Prove |P(S)| = 2ⁿ for a set S with n elements.',
          [('Explain the binary-string correspondence.', 'List the elements s₁, ..., sₙ; a subset corresponds to the string with 1 in position i exactly when sᵢ is in it.'),
           ('Why is the correspondence one-to-one and onto?', 'Different subsets give different strings, and every string gives a subset.'), ('How many strings of length n are there?', '2ⁿ'),
           ('Give the inductive alternative.', 'Adding a new element doubles the count: each old subset appears with and without it.')],
          ['Indicator strings.', 'Bijection.', 'Multiplication rule.', 'Induction.'], 'power_proof_or')


# ---------------------------------------------------------------- 6. proving subset relations
def s6(b):
    STEP = [('cp2', 'Prove A ∩ B ⊆ A.', 'Let x ∈ A ∩ B. Then x ∈ A and x ∈ B, so in particular x ∈ A.', ['Let x ∈ A. Then x ∈ A ∩ B.', 'A ∩ B is smaller, so it is a subset.', 'Draw a Venn diagram; the overlap is inside A.']),
            ('cp2', 'Prove A ⊆ A ∪ B.', 'Let x ∈ A. Then "x ∈ A or x ∈ B" is true, so x ∈ A ∪ B.', ['Let x ∈ A ∪ B. Then x ∈ A.', 'A ∪ B contains everything, so A is inside.', 'Check A = {1}, B = {2}.']),
            ('cp1', 'Prove A − B ⊆ A ∩ B\' (complements in a universe U).', 'Let x ∈ A − B. Then x ∈ A and x ∉ B, so x ∈ A and x ∈ B\'; hence x ∈ A ∩ B\'.', ['Let x ∈ A ∩ B\'. Then x ∈ A − B.', 'Since A − B removes B, it equals A ∩ B\'.', 'Let x ∈ A. Then x ∈ B\'.']),
            ('cp1', 'Prove: if A ⊆ B, then A ∩ C ⊆ B ∩ C.', 'Let x ∈ A ∩ C. Then x ∈ A and x ∈ C. Since A ⊆ B, x ∈ B. So x ∈ B ∩ C.', ['Let x ∈ B ∩ C. Then x ∈ A ∩ C.', 'Let x ∈ A. Then x ∈ C.', 'A ⊆ B, so A ∩ C = B ∩ C.']),
            ('honors', 'Prove: if A ⊆ B and B ⊆ C, then A ⊆ C.', 'Let x ∈ A. Since A ⊆ B, x ∈ B; since B ⊆ C, x ∈ C. So A ⊆ C.', ['Let x ∈ C. Then x ∈ B, so x ∈ A.', 'Take A = {1}, B = {1, 2}, C = {1, 2, 3}.', 'A ⊆ C because A is smaller than C.']),
            ('honors', 'Prove: if A ⊆ B, then B\' ⊆ A\' (complements in U).', 'Let x ∈ B\'. Then x ∉ B. If x were in A, then x ∈ B since A ⊆ B, a contradiction. So x ∉ A, that is, x ∈ A\'.', ['Let x ∈ A\'. Then x ∈ B\'.', 'Complements reverse everything, so the inclusion reverses.', 'Let x ∈ A. Then x ∉ B\'.'])]
    for L, t, good, bad in STEP:
        b.mc(6, L, '%s Which is a correct element argument?' % t, good, bad,
             ['To prove X ⊆ Y, start with an arbitrary x ∈ X and show x ∈ Y using definitions.', good], 'element_argument')
    START = [('cp2', 'To prove X ⊆ Y with an element argument, the first line is ...', 'Let x be any element of X.', ['Let x be any element of Y.', 'Let X = {1, 2}.', 'Suppose X = Y.']),
             ('cp1', 'An element argument proving A ∩ (B ∪ C) ⊆ (A ∩ B) ∪ (A ∩ C) splits into which cases after "x ∈ A and x ∈ B ∪ C"?', 'Case 1: x ∈ B. Case 2: x ∈ C.', ['Case 1: x ∈ A. Case 2: x ∉ A.', 'Case 1: x ∈ A ∩ B. Case 2: x ∉ C.', 'No cases are needed.']),
             ('honors', 'To prove {n ∈ ℤ | 6 | n} ⊆ {n ∈ ℤ | 3 | n}, the key step is ...', 'If n = 6k for an integer k, then n = 3(2k) with 2k an integer.', ['6 and 3 are both multiples of 3.', 'Check n = 6, 12, 18.', 'If n = 3k, then n = 6(k/2).'])]
    for L, t, good, bad in START:
        b.mc(6, L, t, good, bad, ['Element arguments follow the definitions of the operations and of ⊆.', good], 'element_start')
    SUBQ = [('cp2', 'A = {2, 4}, B = {1, 2, 3, 4}', True), ('cp2', 'A = {1, 5}, B = {1, 2, 3, 4}', False), ('cp1', 'A = {n ∈ ℤ | 4 | n}, B = {n ∈ ℤ | 2 | n}', True),
            ('cp1', 'A = {x ∈ ℝ | x² < 4}, B = {x ∈ ℝ | x < 2}', True), ('honors', 'A = {x ∈ ℝ | x < 2}, B = {x ∈ ℝ | x² < 4}', False), ('honors', 'A = {n ∈ ℤ | n² is even}, B = {n ∈ ℤ | n is even}', True)]
    for L, d, t in SUBQ:
        b.mc(6, L, 'Is A ⊆ B? %s.' % d, 'Yes' if t else 'No', ['No' if t else 'Yes', 'Only if A = B', 'Cannot be determined'],
             ['Check whether every element of A is in B (or find one that is not).', 'Answer: ' + ('Yes' if t else 'No') + ('' if t else ' (find an element of A outside B, e.g. 5 or x = −3).')], 'is_subset')
    b.sel(6, 'cp1', 'Which subset relations hold for ALL sets A, B, C?', [('A ∩ B ⊆ A ∪ C', True), ('A − B ⊆ A', True), ('(A ∩ B) ∪ (A ∩ C) ⊆ A', True), ('A ∪ B ⊆ A ∩ B', False), ('A ⊆ A − B', False)],
          ['An element of A ∩ B is in A, hence in A ∪ C, etc.', 'A = {1}, B = {2} breaks the last two.'], 'subset_select')
    b.sel(6, 'cp2', 'Which sets are subsets of {1, 2, 3, 4, 5, 6}?', [('{2, 4, 6}', True), ('∅', True), ('{6}', True), ('{0, 1}', False), ('{7}', False)], ['Every element must be in the larger set.'], 'subset_select')
    b.sel(6, 'honors', 'Which lines belong in an element proof that A − (B ∪ C) ⊆ (A − B) ∩ (A − C)?',
          [('Let x ∈ A − (B ∪ C).', True), ('Then x ∈ A and x ∉ B ∪ C, so x ∉ B and x ∉ C.', True), ('So x ∈ A − B and x ∈ A − C.', True), ('Let x ∈ (A − B) ∩ (A − C).', False), ('So x ∈ B ∩ C.', False)],
          ['Start from the left set; x ∉ B ∪ C means x ∉ B and x ∉ C (De Morgan).'], 'subset_select')
    b.orq(6, 'cp2', 'Prove A ∩ B ⊆ B.',
          [('Write the first line.', 'Let x ∈ A ∩ B.'), ('Use the definition of ∩.', 'x ∈ A and x ∈ B.'), ('What follows?', 'x ∈ B.'), ('State the conclusion.', 'Every element of A ∩ B is in B, so A ∩ B ⊆ B.')],
          ['Arbitrary element.', 'Definition.', 'Specialization.', 'Definition of ⊆.'], 'subset_proof_or')
    b.orq(6, 'cp1', 'Prove: if A ⊆ B, then A ∪ C ⊆ B ∪ C.',
          [('First line.', 'Let x ∈ A ∪ C.'), ('Case x ∈ A.', 'Since A ⊆ B, x ∈ B, so x ∈ B ∪ C.'), ('Case x ∈ C.', 'Then x ∈ B ∪ C.'), ('Conclusion.', 'In every case x ∈ B ∪ C, so A ∪ C ⊆ B ∪ C.')],
          ['Arbitrary element.', 'Use the hypothesis.', 'Definition of ∪.', 'Division into cases.'], 'subset_proof_or')
    b.orq(6, 'honors', 'Prove {n ∈ ℤ | n ≡ 1 (mod 4)} ⊆ {n ∈ ℤ | n is odd}.',
          [('Write an arbitrary element of the left set.', 'n = 4k + 1 for some integer k.'), ('Rewrite to show it is odd.', 'n = 2(2k) + 1'), ('Why is 2k an integer?', 'Integers are closed under multiplication.'), ('Is the reverse inclusion true? Explain.', 'No; 3 is odd but 3 ≡ 3 (mod 4).')],
          ['Definition.', 'Odd form.', 'Closure.', 'Counterexample.'], 'subset_proof_or')


# ---------------------------------------------------------------- 7. set identities
IDS = [("A ∪ (B ∩ C)", "(A ∪ B) ∩ (A ∪ C)", True), ("A ∩ (B ∪ C)", "(A ∩ B) ∪ C", False), ("(A ∪ B)'", "A' ∩ B'", True), ("A − (B ∪ C)", "(A − B) ∩ (A − C)", True),
       ("A − (B ∩ C)", "(A − B) ∩ (A − C)", False), ("(A − B) ∪ (B − A)", "(A ∪ B) − (A ∩ B)", True), ("A ∪ (A ∩ B)", "A", True), ("(A ∪ B) − C", "A ∪ (B − C)", False),
       ("A ∩ (B − C)", "(A ∩ B) − (A ∩ C)", True)]


def set_eval(e, env, Uset):
    """Evaluate a set expression with ∪ ∩ − (left to right, equal precedence, parentheses), postfix ' (complement in U), ∅, U."""
    toks = [c for c in e.replace(' ', '')]
    pos = [0]

    def atom():
        t = toks[pos[0]]
        if t == '(':
            pos[0] += 1
            v = expr()
            assert toks[pos[0]] == ')'
            pos[0] += 1
        elif t == '∅':
            pos[0] += 1; v = set()
        else:
            pos[0] += 1; v = Uset if t == 'U' else env[t]
        while pos[0] < len(toks) and toks[pos[0]] == "'":
            pos[0] += 1; v = Uset - v
        return v

    def expr():
        v = atom()
        while pos[0] < len(toks) and toks[pos[0]] in '∪∩−':
            op = toks[pos[0]]; pos[0] += 1
            w = atom()
            v = v | w if op == '∪' else v & w if op == '∩' else v - w
        return v
    out = expr()
    assert pos[0] == len(toks), e
    return out


def ident_holds(l, r):
    """Check a set identity on a universe with one element per region of a three-set Venn diagram (complete test)."""
    Uset = set(range(8))
    env = {'A': {i for i in Uset if i & 1}, 'B': {i for i in Uset if i & 2}, 'C': {i for i in Uset if i & 4}}
    return set_eval(l, env, Uset) == set_eval(r, env, Uset)


def s7(b):
    for (l, r, t) in IDS:
        assert ident_holds(l, r) == t, (l, r)
    for L, idx in (('cp2', [2, 6, 1]), ('cp1', [0, 3, 4]), ('honors', [5, 7, 8])):
        for i in idx:
            l, r, t = IDS[i]
            b.mc(7, L, 'Is %s = %s an identity (true for ALL sets A, B, C in a universe U)?' % (l, r), 'Yes, it is an identity' if t else 'No, it fails for some sets',
                 ['No, it fails for some sets' if t else 'Yes, it is an identity', 'Yes, because both sides use the same letters', 'Only when A, B, C are disjoint'],
                 ['Check all eight regions of a three-set Venn diagram (one test element per region).', 'Result: ' + ('identity' if t else 'not an identity')], 'identity_check')
    NAME = [('cp2', "A ∪ ∅ = A", 'Identity law', ['Domination law', 'Idempotent law', 'Absorption law']), ('cp2', "(A ∩ B)' = A' ∪ B'", "De Morgan's law", ['Distributive law', 'Double complement law', 'Absorption law']),
            ('cp1', "A ∩ (B ∪ C) = (A ∩ B) ∪ (A ∩ C)", 'Distributive law', ['Associative law', "De Morgan's law", 'Commutative law']),
            ('cp1', "A ∪ (A ∩ B) = A", 'Absorption law', ['Idempotent law', 'Identity law', 'Distributive law']),
            ('honors', "A − B = A ∩ B'", 'Set difference law', ['Complement law', "De Morgan's law", 'Absorption law']), ('honors', "A ∩ A' = ∅", 'Complement law', ['Identity law', 'Domination law', 'Idempotent law'])]
    for L, idt, good, bad in NAME:
        b.mc(7, L, 'Name the law: %s' % idt, good, bad, ['Match the pattern to the standard list of set identities.', good], 'name_law')
    ALG = [('cp1', "Simplify (A ∪ B) ∩ A using laws.", 'A', ['A ∪ B', 'A ∩ B', 'B']), ('cp1', "Simplify (A')' ∩ (A ∪ B).", 'A', ['A ∪ B', "A'", 'B']),
           ('honors', "Simplify (A − B) ∪ (A ∩ B).", 'A', ['A ∪ B', 'A − B', 'B']), ('honors', "Simplify (A ∩ B') ∪ (A ∩ B) ∪ (A' ∩ B).", 'A ∪ B', ['A', 'A ∩ B', 'U']),
           ('cp2', "Simplify A ∩ A.", 'A', ['∅', 'U', "A'"])]
    for L, t, good, bad in ALG:
        lhs = t.split('Simplify ')[1].split(' using')[0].rstrip('.')
        assert ident_holds(lhs, good), t
        b.mc(7, L, t, good, bad, ['Apply distributive, absorption, complement and identity laws.', '= ' + good], 'simplify_sets')
    b.sel(7, 'cp1', 'Which statements are identities for all sets A, B in a universe U?', [("A ∪ A' = U", True), ("A ∩ U = A", True), ("A ∪ U = U", True), ("A − A = A", False), ("A ∩ ∅ = A", False)],
          ['Complement, identity and domination laws; A − A = ∅ and A ∩ ∅ = ∅.'], 'identity_select')
    b.sel(7, 'cp2', 'Which pairs are always equal?', [('A ∪ B and B ∪ A', True), ('A ∩ B and B ∩ A', True), ('A − B and B − A', False), ('(A\')\' and A', True), ('A ∪ B and A ∩ B', False)],
          ['Commutative laws and double complement hold; difference is not commutative.'], 'identity_select')
    b.sel(7, 'honors', 'Which identities hold for all sets A, B, C?', [(f'{l} = {r}', t) for l, r, t in [IDS[0], IDS[3], IDS[5], IDS[4], IDS[7]]],
          ['Checked on all eight Venn regions.'], 'identity_select')
    b.orq(7, 'cp2', "Show (A ∪ B)' = A' ∩ B' using U = {1, 2, 3, 4, 5}, A = {1, 2}, B = {2, 3}.",
          [("Find (A ∪ B)'.", '{4, 5}'), ("Find A'.", '{3, 4, 5}'), ("Find B'.", '{1, 4, 5}'), ("Find A' ∩ B' and compare.", "{4, 5}; equal, as De Morgan's law says (this is an example, not a proof).")],
          ['A ∪ B = {1, 2, 3}.', 'U − A.', 'U − B.', 'One example illustrates but does not prove an identity.'], 'identity_or')
    b.orq(7, 'cp1', "Prove A − (A − B) = A ∩ B with laws.",
          [('Rewrite each difference with complements.', "A ∩ (A ∩ B')'"), ("Apply De Morgan.", "A ∩ (A' ∪ B)"), ('Distribute.', "(A ∩ A') ∪ (A ∩ B)"), ('Finish.', '∅ ∪ (A ∩ B) = A ∩ B')],
          ["X − Y = X ∩ Y'.", "(A ∩ B')' = A' ∪ B.", 'Distributive law.', 'Complement and identity laws.'], 'identity_or')
    b.orq(7, 'honors', 'Prove A ∩ (B ∪ C) = (A ∩ B) ∪ (A ∩ C) by element arguments.',
          [('Show ⊆: let x ∈ A ∩ (B ∪ C).', 'x ∈ A and (x ∈ B or x ∈ C); case x ∈ B gives x ∈ A ∩ B; case x ∈ C gives x ∈ A ∩ C; so x is in the right side.'),
           ('Show ⊇: let x ∈ (A ∩ B) ∪ (A ∩ C).', 'In either case x ∈ A, and x ∈ B or x ∈ C, so x ∈ A ∩ (B ∪ C).'),
           ('Why are both directions needed?', 'Set equality means each set is a subset of the other.'), ('Which logic law mirrors this identity?', 'p ∧ (q ∨ r) ≡ (p ∧ q) ∨ (p ∧ r)')],
          ['Cases.', 'Cases.', 'Mutual inclusion.', 'Distributive law of logic.'], 'identity_or')


# ---------------------------------------------------------------- 8. disproving
def s8(b):
    e = frozenset
    CE = [('cp2', 'For all sets A and B, A − B = B − A.', lambda A, B, C: A - B != B - A, [({1}, set()), ({1}, {1}), (set(), set()), ({1, 2}, {1, 2})]),
          ('cp2', 'For all sets A and B, A ∪ B = A.', lambda A, B, C: (A | B) != A, [(set(), {1}), ({1}, set()), ({1}, {1}), ({1, 2}, {2})]),
          ('cp1', 'For all sets A, B, C, if A ∩ C = B ∩ C then A = B.', lambda A, B, C: (A & C) == (B & C) and A != B, [({1}, {2}, set()), ({1}, {1}, {2}), ({1}, {1}, {1}), ({1, 2}, {1}, {1, 2})]),
          ('cp1', 'For all sets A, B, (A ∪ B) − B = A.', lambda A, B, C: (A | B) - B != A, [({1}, {1}), ({1}, {2}), (set(), {1}), ({1, 2}, {3})]),
          ('honors', 'For all sets A, B, C, A − (B − C) = (A − B) − C.', lambda A, B, C: A - (B - C) != (A - B) - C, [({1}, {1}, {1}), ({1}, set(), set()), ({1}, {2}, {3}), (set(), set(), set())]),
          ('honors', 'For all sets A, B, C, A ∩ (B ∪ C) = (A ∩ B) ∪ C.', lambda A, B, C: A & (B | C) != (A & B) | C, [(set(), set(), {1}), ({1}, {1}, set()), ({1}, set(), {1}), ({1, 2}, {2}, {2})])]
    for L, st, broken, cands in CE:
        names = 'ABC'
        txt = lambda c: ', '.join('%s = %s' % (names[i], fmt_set(x)) for i, x in enumerate(c))
        full = lambda c: tuple(list(c) + [set()] * (3 - len(c)))
        assert broken(*full(cands[0])) and not any(broken(*full(c)) for c in cands[1:]), st
        b.mc(8, L, 'Which choice is a counterexample to the false statement "%s"?' % st, txt(cands[0]), [txt(c) for c in cands[1:]],
             ['A counterexample must make the statement fail for those specific sets; the other choices satisfy it.', 'With %s the two sides differ.' % txt(cands[0])], 'set_counterexample')
    TF = [('cp2', 'For all sets A, B: A ∩ B ⊆ A.', True, 'If x ∈ A ∩ B then x ∈ A.'), ('cp2', 'For all sets A, B: A ⊆ A ∩ B.', False, 'A = {1}, B = ∅: A ∩ B = ∅ does not contain 1.'),
          ('cp1', 'For all sets A, B: if A ⊆ B then A ∪ B = B.', True, 'Every element of A ∪ B is in A or B, hence in B; and B ⊆ A ∪ B.'),
          ('cp1', 'For all sets A, B, C: A ∪ (B − C) = (A ∪ B) − (A ∪ C).', False, 'A = {1}, B = C = ∅: the left side is {1}, the right side is ∅.'),
          ('honors', 'For all sets A, B: P(A) ⊆ P(B) implies A ⊆ B.', True, 'A ∈ P(A) ⊆ P(B), so A ∈ P(B), meaning A ⊆ B.'),
          ('honors', 'For all sets A, B, C: (A − B) ∪ (B − C) = A − C.', False, 'A = C = ∅, B = {1}: the left side is {1}, the right side is ∅.')]
    for L, st, t, why in TF:
        b.mc(8, L, 'Prove or disprove: %s' % st, 'True: it can be proved for all sets' if t else 'False: a counterexample exists',
             ['False: a counterexample exists' if t else 'True: it can be proved for all sets', 'True: it works for A = {1}, B = {1, 2}', 'It is neither true nor false'],
             [why, 'An example that works never proves a "for all sets" statement; one counterexample disproves it.'], 'prove_disprove')
    SAQ = [('cp2', 'Find a set B so that {1, 2} ∪ B ≠ {1, 2}. Give the smallest such B using the number 3.', '{3}'),
           ('cp1', 'Disprove "A ∩ B = ∅ implies A = ∅" with A = {1}. Give a set B that works, using the number 2.', '{2}'),
           ('honors', 'Disprove "(A ∩ B) ∪ C = A ∩ (B ∪ C)" with A = ∅ and B = ∅. Give the smallest set C using the number 1.', '{1}')]
    for L, t, a in SAQ:
        b.sa(8, L, t, a, ['Check that the chosen sets make the two sides different.', a], 'build_counterexample')
    b.sel(8, 'cp1', 'Which statements are FALSE for some sets (so they can be disproved)?', [('A − B = A', True), ('A ∪ B = A ∩ B', True), ('A ∩ (A ∪ B) = A', False), ('A ⊆ A ∪ B', False), ('(A − B) ∩ B = ∅', False)],
          ['A = B = {1} breaks the first; A = {1}, B = ∅ breaks the second; the last three are identities.'], 'disprove_select')
    b.sel(8, 'cp2', 'Statement: "For all sets A and B, A ∪ B = B." Which choices are counterexamples?', [('A = {1}, B = ∅', True), ('A = {1, 2}, B = {2}', True), ('A = ∅, B = {5}', False), ('A = {3}, B = {3, 4}', False), ('A = {7}, B = {8}', True)],
          ['A counterexample needs A ⊄ B.'], 'disprove_select')
    b.sel(8, 'honors', 'Statement: "For all sets A, B, C, if A ∪ C = B ∪ C, then A = B." Which are counterexamples?', [('A = {1}, B = ∅, C = {1}', True), ('A = {1, 2}, B = {2}, C = {1}', True), ('A = {1}, B = {1}, C = {2}', False), ('A = {1}, B = {2}, C = ∅', False), ('A = ∅, B = {3}, C = {3}', True)],
          ['Need A ∪ C = B ∪ C but A ≠ B.'], 'disprove_select')
    b.orq(8, 'cp2', 'Claim: "For all sets A and B, A − B = A."',
          [('Test A = {1, 2}, B = {3}.', 'A − B = {1, 2} = A; works here.'), ('Test A = {1, 2}, B = {2}.', 'A − B = {1} ≠ A.'), ('Is the claim true or false?', 'False'), ('When is A − B = A?', 'Exactly when A ∩ B = ∅.')],
          ['Compute.', 'Compute.', 'One counterexample.', 'Nothing is removed.'], 'disprove_or')
    b.orq(8, 'cp1', 'Claim: "For all sets A, B, C, A ∪ (B ∩ C) = (A ∪ B) ∩ C."',
          [('Test A = {1}, B = C = ∅.', 'Left: {1}; right: ∅.'), ('Is the claim true?', 'No'), ('Write the correct distributive law.', 'A ∪ (B ∩ C) = (A ∪ B) ∩ (A ∪ C)'), ('Under what condition does the claim hold?', 'When A ⊆ C.')],
          ['Compute.', 'Counterexample.', 'Distributive law.', 'Then (A ∪ B) ∩ C = (A ∩ C) ∪ (B ∩ C) = A ∪ (B ∩ C).'], 'disprove_or')
    b.orq(8, 'honors', 'Claim: "For all sets A and B, P(A − B) = P(A) − P(B)."',
          [('Is ∅ an element of P(A − B)?', 'Yes'), ('Is ∅ an element of P(A) − P(B)?', 'No, because ∅ ∈ P(B).'), ('Conclude.', 'The claim is false for every A and B.'), ('Is P(A − B) ⊆ P(A)? Explain.', 'Yes; A − B ⊆ A, so every subset of A − B is a subset of A.')],
          ['∅ is a subset of everything.', 'Removed.', 'The sets always differ.', 'Monotonicity of P.'], 'disprove_or')


def errors(b):
    E = b.err
    E(2, 'cp2', 'A = {1, 2, 3}, B = {3, 4}. Find A ∪ B.', 'Jordan', ['A ∪ B = {1, 2, 3, 3, 4}, which has 5 elements.'],
      '{1, 2, 3, 4}', 'Jordan listed 3 twice and counted it twice. Each element of a set appears once.', 'Union combines the elements without repeats.', ['{1, 2, 3, 4} has 4 elements.'], 'union_repeat_error')
    E(2, 'cp2', 'A = {a, b, c}, B = {b, d}. Find A − B.', 'Sam', ['A − B = {a, c, d}'],
      '{a, c}', 'Sam included d, which is in B but not in A. A − B only contains elements of A.', 'Difference removes; it never adds.', ['Remove b from A.'], 'difference_add_error')
    E(3, 'cp2', 'A = {2, 4}. Find A\'.', 'Riley', ['A\' = all numbers except 2 and 4.'],
      'Cannot be found until the universe is stated (e.g., in U = {1, ..., 5}, A\' = {1, 3, 5})', 'Riley did not specify a universe. A complement depends on U.', 'Different universes give different complements.', ['State U first, then A\' = U − A.'], 'no_universe_error')
    E(5, 'cp2', 'How many subsets does {a, b, c} have?', 'Casey', ['{a}, {b}, {c}, {a, b}, {a, c}, {b, c}: 6 subsets.'],
      '8', 'Casey forgot ∅ and the set itself.', 'Every set has ∅ and itself as subsets.', ['2³ = 8.'], 'missing_subsets_error')
    E(4, 'cp1', '25 students like math, 20 like art, 8 like both. How many like math or art?', 'Avery', ['25 + 20 = 45'],
      '37', 'Avery counted the 8 students in both groups twice.', 'Inclusion-exclusion subtracts the overlap.', ['25 + 20 − 8 = 37.'], 'double_count_error')
    E(1, 'cp2', 'Is {1, 2} = {1, 2, 2}?', 'Morgan', ['No, the second set has 3 elements.'],
      'Yes', 'Morgan counted the repeated 2. Both sets have exactly the elements 1 and 2.', 'Repetition does not change a set.', ['Same elements ⇒ equal.'], 'repeat_equal_error')
    E(3, 'cp1', "Use De Morgan to rewrite (A ∩ B)'.", 'Taylor', ["(A ∩ B)' = A' ∩ B'"],
      "A' ∪ B'", 'Taylor complemented each set but kept ∩. De Morgan switches ∩ to ∪.', "An element outside A ∩ B only needs to miss one of the sets.", ["(A ∩ B)' = A' ∪ B'."], 'set_demorgan_error')
    E(6, 'cp1', 'Prove A ∩ B ⊆ A ∪ B.', 'Jamie', ['Let x ∈ A ∪ B. Then x ∈ A or x ∈ B, so x ∈ A ∩ B.'],
      'Let x ∈ A ∩ B; then x ∈ A, so x ∈ A ∪ B', 'Jamie started from the wrong set (proving the false reverse inclusion) and used "or" as "and".', 'To show X ⊆ Y, start with x ∈ X.', ['x ∈ A ∩ B ⇒ x ∈ A ⇒ x ∈ A ∪ B.'], 'wrong_direction_error')
    E(7, 'cp1', 'Prove (A ∪ B)\' = A\' ∩ B\'.', 'Quinn', ['Take U = {1, 2, 3}, A = {1}, B = {2}. Both sides equal {3}. So the identity is proved.'],
      'Use an element argument (or a membership table) for arbitrary sets', 'Quinn checked one example. An example cannot prove a statement about all sets.', 'Identities need a general argument.', ["x ∉ A ∪ B ⟺ x ∉ A and x ∉ B ⟺ x ∈ A' ∩ B'."], 'example_identity_error')
    E(5, 'cp1', 'Is {1} ∈ P({1, 2})? Is 1 ∈ P({1, 2})?', 'Alex', ['Both are true because 1 is in {1, 2}.'],
      '{1} ∈ P({1, 2}) is true; 1 ∈ P({1, 2}) is false', 'Alex treated elements of the set as elements of its power set. P(S) contains subsets, not elements.', 'Elements of P(S) are sets.', ['P({1, 2}) = {∅, {1}, {2}, {1, 2}}.'], 'power_element_error')
    E(8, 'cp1', 'Disprove "For all A, B: A ∩ B = A".', 'Jordan', ['Take A = {1}, B = {1, 2}. Then A ∩ B = {1}... so it is false.'],
      'A = {1}, B = ∅ gives A ∩ B = ∅ ≠ A', 'Jordan\'s example satisfies the statement, so it is not a counterexample.', 'A counterexample must make the statement false.', ['Choose B missing an element of A.'], 'non_counterexample_error')
    E(4, 'cp2', 'Venn diagram: A only has 4 elements, both has 3, B only has 5. How many are in A?', 'Sam', ['A has 4 elements.'],
      '7', 'Sam counted only the "A only" region. Circle A also includes the overlap.', 'A = A only + both.', ['4 + 3 = 7.'], 'venn_region_error')
    E(7, 'honors', 'Simplify (A ∪ B) ∩ (A ∪ B\').', 'Riley', ['(A ∪ B) ∩ (A ∪ B\') = A ∪ (B ∩ B\') = A ∪ U = U'],
      'A', 'Riley used B ∩ B\' = U; in fact B ∩ B\' = ∅.', 'Complement laws: B ∩ B\' = ∅ and B ∪ B\' = U.', ['A ∪ (B ∩ B\') = A ∪ ∅ = A.'], 'complement_law_error')
    E(8, 'honors', 'Prove or disprove: A − (B − C) = (A − B) ∪ (A ∩ C).', 'Casey', ['With A = {1}, B = {2}, C = {3}: left {1}, right {1}. The sides are equal for one example, so it is false? No — the claim fails because the formula looks different.'],
      'True (it is an identity)', 'Casey judged the claim by appearance. It is an identity: A − (B ∩ C\') = A ∩ (B\' ∪ C) = (A ∩ B\') ∪ (A ∩ C).', 'Check all eight Venn regions or use laws.', ["A − (B − C) = A ∩ (B ∩ C')' = A ∩ (B' ∪ C)."], 'appearance_error')
    E(6, 'honors', 'Prove: if A ⊆ B then P(A) ⊆ P(B).', 'Avery', ['Let x ∈ A. Then x ∈ B. So P(A) ⊆ P(B).'],
      'Let X ∈ P(A), so X ⊆ A ⊆ B; hence X ∈ P(B)', 'Avery took an element of A instead of an element of P(A). Elements of P(A) are subsets of A.', 'Start with an arbitrary element of the left set, P(A).', ['X ⊆ A and A ⊆ B give X ⊆ B by transitivity.'], 'power_proof_error')
    E(2, 'honors', 'A = [1, 4], B = (2, 6). Find A − B.', 'Morgan', ['A − B = [1, 2)'],
      '[1, 2]', 'Morgan removed 2, but 2 ∉ B because B = (2, 6) is open at 2.', 'Endpoints matter for intervals.', ['2 ∈ A and 2 ∉ B, so 2 ∈ A − B.'], 'interval_endpoint_error')
    E(1, 'honors', 'Is {n ∈ ℤ | n² = n} equal to {0, 1}? Is ∅ equal to {∅}?', 'Taylor', ['Both pairs are equal.'],
      'The first pair is equal; ∅ ≠ {∅}', 'Taylor treated {∅} as empty. {∅} has one element.', '|∅| = 0 but |{∅}| = 1.', ['n² = n gives n = 0 or 1.'], 'empty_brace_error')
    E(3, 'honors', 'U = ℕ = {1, 2, 3, ...}, E = even naturals. Find E\'.', 'Jamie', ['E\' = all odd integers, including −1, −3, ....'],
      'The positive odd integers {1, 3, 5, ...}', 'Jamie used ℤ as the universe. The complement is taken in U = ℕ.', 'Elements outside the universe are never in a complement.', ['E\' = ℕ − E.'], 'wrong_universe_error')


def topup(b):
    need = lambda k, L: b.counter.get((k, L), 0) < 10
    W = range(-30, 31)
    # 1: equality of builder-defined sets on integers (complete within the stated finite universe)
    EQ = [('cp2', '{n ∈ ℤ | 0 < n < 4}', lambda n: 0 < n < 4, '{1, 2, 3}', lambda n: n in (1, 2, 3)),
          ('cp2', '{n ∈ ℤ | n² = 9}', lambda n: n * n == 9, '{3}', lambda n: n == 3),
          ('cp2', '{x ∈ ℤ | x + 2 = 5}', lambda n: n + 2 == 5, '{3}', lambda n: n == 3),
          ('cp1', '{n ∈ ℤ | n² < 5}', lambda n: n * n < 5, '{n ∈ ℤ | |n| ≤ 2}', lambda n: abs(n) <= 2),
          ('cp1', '{n ∈ ℤ | n is a multiple of 2 and of 3}', lambda n: n % 6 == 0, '{n ∈ ℤ | n is a multiple of 6}', lambda n: n % 6 == 0),
          ('cp1', '{n ∈ ℤ | n² = n}', lambda n: n * n == n, '{1}', lambda n: n == 1),
          ('cp1', '{n ∈ ℤ | n is a multiple of 4 or of 6}', lambda n: n % 4 == 0 or n % 6 == 0, '{n ∈ ℤ | n is a multiple of 2}', lambda n: n % 2 == 0),
          ('honors', '{n ∈ ℤ | n³ = n}', lambda n: n ** 3 == n, '{−1, 0, 1}', lambda n: n in (-1, 0, 1)),
          ('honors', '{n ∈ ℤ | n² − 5n + 6 < 0}', lambda n: n * n - 5 * n + 6 < 0, '∅', lambda n: False),
          ('honors', '{n ∈ ℤ | 12 | n}', lambda n: n % 12 == 0, '{n ∈ ℤ | 3 | n and 4 | n}', lambda n: n % 3 == 0 and n % 4 == 0)]
    for L, A, fa, B, fb in EQ:
        if not need(1, L):
            continue
        eq = all(fa(n) == fb(n) for n in W)
        diff = next((n for n in W if fa(n) != fb(n)), None)
        b.mc(1, L, 'Are the sets %s and %s equal?' % (A, B), 'Yes: they have exactly the same elements' if eq else 'No: one set has an element the other does not',
             ['No: one set has an element the other does not' if eq else 'Yes: they have exactly the same elements', 'Yes: both are described by a condition on n', 'No: they are written differently'],
             ['Compare the elements of both sets.', 'They are equal.' if eq else 'They differ: %d belongs to exactly one of them.' % diff], 'set_equal')
    # 2, 3: extra computed operations
    rng = seeded('u5top')
    for k, L in ((2, 'cp1'), (2, 'honors'), (2, 'honors'), (3, 'cp2'), (3, 'cp1'), (3, 'honors')):
        if not need(k, L):
            continue
        Up = list(range(1, 13))
        A, B = rand_sets(rng, Up, 5, 5)
        C = set(rng.sample(Up, 4))
        if k == 2:
            R = ((A & B) | C) if L == 'honors' else A - B
            e = '(A ∩ B) ∪ C' if L == 'honors' else 'A − B'
            pre = 'Let A = %s, B = %s, C = %s. ' % (fmt_set(A), fmt_set(B), fmt_set(C))
        else:
            Uset = set(Up)
            R = Uset - (A & B) if L != 'honors' else (Uset - A) & (B | C)
            e = "(A ∩ B)'" if L != 'honors' else "A' ∩ (B ∪ C)"
            pre = 'Universe U = %s. Let A = %s, B = %s, C = %s. Complements are taken in U. ' % (fmt_set(Uset), fmt_set(A), fmt_set(B), fmt_set(C))
        b.mc(k, L, pre + 'Find %s.' % e, fmt_set(R), wrong_sets(R, set(Up), rng) + [fmt_set(A ^ B)], ['Work inside parentheses first.', '%s = %s' % (e, fmt_set(R))], 'set_op' if k == 2 else 'complement_op')
    # 4: inclusion-exclusion counts (computed by brute force)
    IE = [('cp2', 'How many integers from 1 to 30 are even or multiples of 5?', lambda n: n % 2 == 0 or n % 5 == 0, 30),
          ('honors', 'How many integers from 1 to 200 are divisible by 4 or 6 but not by 5?', lambda n: (n % 4 == 0 or n % 6 == 0) and n % 5, 200),
          ('cp2', 'How many integers from 1 to 20 are multiples of 2 or 3?', lambda n: n % 2 == 0 or n % 3 == 0, 20)]
    for L, t, f, N in IE:
        if need(4, L):
            v = sum(1 for n in range(1, N + 1) if f(n))
            b.sa(4, L, t, v, ['Use inclusion-exclusion on the divisibility sets (or count directly).', 'Answer: %d' % v], 'inclusion_exclusion')
    # 5: power-set counting (enumerated)
    PS = [('cp2', 'How many subsets of {1, 2, 3} have exactly 2 elements?', [1, 2, 3], lambda s: len(s) == 2),
          ('cp2', 'How many subsets of {a, b, c, d} contain a?', 'abcd', lambda s: 'a' in s),
          ('cp2', 'How many subsets of {1, 2, 3, 4} have at most one element?', [1, 2, 3, 4], lambda s: len(s) <= 1),
          ('cp2', 'How many elements does P({x}) have?', ['x'], lambda s: True),
          ('cp1', 'How many subsets of {1, 2, 3, 4, 5} contain no even number?', [1, 2, 3, 4, 5], lambda s: all(x % 2 for x in s)),
          ('cp1', 'How many subsets of {1, 2, 3, 4, 5} contain both 1 and 2?', [1, 2, 3, 4, 5], lambda s: 1 in s and 2 in s),
          ('cp1', 'How many subsets of {1, ..., 6} have a sum of exactly 6?', [1, 2, 3, 4, 5, 6], lambda s: sum(s) == 6),
          ('honors', 'How many subsets of {1, ..., 8} contain at least one of 1 and 2?', list(range(1, 9)), lambda s: 1 in s or 2 in s),
          ('honors', 'How many subsets of {1, ..., 7} contain no two consecutive integers?', list(range(1, 8)), lambda s: all(x + 1 not in s for x in s)),
          ('honors', 'How many subsets of {1, ..., 6} have an odd sum?', list(range(1, 7)), lambda s: sum(s) % 2 == 1)]
    for L, t, S, f in PS:
        if need(5, L):
            v = sum(1 for r in range(len(S) + 1) for c in itertools.combinations(S, r) if f(set(c)))
            b.mc(5, L, t, str(v), [], ['Count by fixing the required elements and letting the others be free (or list them).', 'Answer: %d (checked by listing all subsets).' % v], 'power_set_count')
    # 6: subset checks on integers (computed on a window, with reasoning)
    SB = [('cp2', '{3, 6}', lambda n: n in (3, 6), '{n ∈ ℤ | n is a multiple of 3}', lambda n: n % 3 == 0),
          ('cp2', '{1, 2, 3}', lambda n: n in (1, 2, 3), '{n ∈ ℤ | n is odd}', lambda n: n % 2 == 1),
          ('cp2', '∅', lambda n: False, '{7}', lambda n: n == 7),
          ('cp1', '{n ∈ ℤ | n is a multiple of 10}', lambda n: n % 10 == 0, '{n ∈ ℤ | n is a multiple of 5}', lambda n: n % 5 == 0),
          ('cp1', '{n ∈ ℤ | n is a multiple of 3}', lambda n: n % 3 == 0, '{n ∈ ℤ | n is a multiple of 9}', lambda n: n % 9 == 0),
          ('honors', '{n ∈ ℤ | n ≡ 3 (mod 6)}', lambda n: n % 6 == 3, '{n ∈ ℤ | n is odd and a multiple of 3}', lambda n: n % 2 == 1 and n % 3 == 0),
          ('honors', '{n ∈ ℤ | n² is a multiple of 4}', lambda n: n * n % 4 == 0, '{n ∈ ℤ | n is a multiple of 4}', lambda n: n % 4 == 0)]
    for L, A, fa, B, fb in SB:
        if need(6, L):
            t = all(fb(n) for n in W if fa(n))
            bad = next((n for n in W if fa(n) and not fb(n)), None)
            b.mc(6, L, 'Let A = %s and B = %s. Is A ⊆ B?' % (A, B), 'Yes' if t else 'No', ['No' if t else 'Yes', 'Only if A = B', 'Cannot be determined'],
                 ['Every element of A must be in B.', 'Yes.' if t else 'No: %d ∈ A but %d ∉ B.' % (bad, bad)], 'is_subset')
    # 7: more identities (complete Venn-region check)
    MORE = [('cp2', 'A ∩ B', 'B ∩ A'), ('cp2', 'A ∪ (B ∪ C)', '(A ∪ B) ∪ C'), ('cp2', 'A − B', 'B − A'), ('cp2', "(A')'", 'A'),
            ('honors', "(A ∩ B)'", "A' ∩ B'"), ('cp1', "A ∩ (A' ∪ B)", 'A ∩ B')]
    for L, l, r in MORE:
        if need(7, L):
            t = ident_holds(l, r)
            b.mc(7, L, 'Is %s = %s an identity (true for ALL sets A, B, C in a universe U)?' % (l, r), 'Yes, it is an identity' if t else 'No, it fails for some sets',
                 ['No, it fails for some sets' if t else 'Yes, it is an identity', 'Yes, because both sides use the same letters', 'Only when A, B, C are disjoint'],
                 ['Check every region of a Venn diagram.', 'Result: ' + ('identity' if t else 'not an identity (e.g. A = {1}, B = ∅)')], 'identity_check')
    # 8: more counterexample construction (short answers checked by evaluation)
    SA8 = [('cp2', 'Disprove "A ∪ B = B for all A, B": with B = ∅, give the smallest A using the number 1.', '{1}', lambda A: A | set() != set()),
           ('cp2', 'Disprove "A ∩ B = A for all A, B": with A = {1, 2} and B = {1}, what is A ∩ B?', '{1}', None),
           ('cp1', 'Disprove "A − B = ∅ implies A = B": with A = ∅, give the smallest B using the number 1.', '{1}', None),
           ('honors', 'Disprove "A × B = B × A for all A, B": with A = {1}, give the smallest B using the number 2.', '{2}', None)]
    for L, t, a, _ in SA8:
        if need(8, L):
            b.sa(8, L, t, a, ['Check that the sets make the statement false.', a], 'build_counterexample')


def topup2(b):
    b.sa(5, 'honors', 'How many elements of P({1, 2, 3, 4, 5}) are subsets of {1, 2, 3} or of {3, 4, 5}?', 2 ** 3 + 2 ** 3 - 2 ** 1,
         ['Inclusion-exclusion on power sets: |P(X) ∪ P(Y)| = |P(X)| + |P(Y)| − |P(X ∩ Y)|.', '8 + 8 − 2 = 14 (X ∩ Y = {3}).'], 'power_set_count')
    for L, st, cands, broken in (('cp2', 'For all sets A, B: A ∩ B = ∅.', [({1}, {1}), ({1}, {2}), (set(), {1}), ({1}, set())], lambda A, B: (A & B) != set()),
                                 ('cp1', 'For all sets A, B: A ∪ B = A ∪ (B − A) ∪ (A ∩ B) − B.', None, None),
                                 ('honors', 'For all sets A, B: (A ∪ B) − A = B.', [({1}, {1}), ({1}, {2}), (set(), {2}), ({2}, {3})], lambda A, B: (A | B) - A != B)):
        if cands is None:
            cands = [({1}, {2}), ({1}, {1}), ({1, 2}, {2}), (set(), set())]
            broken = lambda A, B: ((A - B) | B) != A
            st = 'For all sets A, B: (A − B) ∪ B = A.'
        txt = lambda c: 'A = %s, B = %s' % (fmt_set(c[0]), fmt_set(c[1]))
        assert broken(*cands[0]) and not any(broken(*c) for c in cands[1:]), st
        b.mc(8, L, 'Which choice is a counterexample to the false statement "%s"?' % st, txt(cands[0]), [txt(c) for c in cands[1:]],
             ['A counterexample must make the statement fail; the other choices satisfy it.', 'With %s the two sides differ.' % txt(cands[0])], 'set_counterexample')
