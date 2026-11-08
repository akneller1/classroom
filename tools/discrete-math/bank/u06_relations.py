"""Unit 6: Properties of Relations (7 skills). Relations are sets of ordered pairs on a stated set A; directed graphs
are drawn with loops for (a, a). Every property is computed."""
import itertools
from core import Bank, fmt_set, seeded
import figs

U = 'properties-relations'


def build():
    b = Bank(U, 'rl', 7)
    for f in (s1, s2, s3, s4, s5, s6, s7, topup, errors):
        f(b)
    return b


def refl(R, A): return all((a, a) in R for a in A)
def sym(R): return all((b_, a) in R for a, b_ in R)
def trans(R): return all((a, d) in R for a, b_ in R for c, d in R if b_ == c)
def anti(R): return all(not ((b_, a) in R and a != b_) for a, b_ in R)
def inv(R): return {(b_, a) for a, b_ in R}
def props(R, A): return {'reflexive': refl(R, A), 'symmetric': sym(R), 'transitive': trans(R)}


def pairs(R):
    return fmt_set(R)


def closure_t(R):
    R = set(R)
    while True:
        new = {(a, d) for a, b_ in R for c, d in R if b_ == c} - R
        if not new:
            return R
        R |= new


def classes(R, A):
    out = []
    for a in sorted(A):
        c = {x for x in A if (a, x) in R}
        if c not in out:
            out.append(c)
    return out


RELS = {  # name: (A, R)
    'r1': ({1, 2, 3}, {(1, 1), (2, 2), (3, 3), (1, 2), (2, 1)}),
    'r2': ({1, 2, 3}, {(1, 2), (2, 3)}),
    'r3': ({1, 2, 3}, {(1, 1), (2, 2), (3, 3)}),
    'r4': ({1, 2, 3, 4}, {(1, 2), (2, 1), (1, 1), (2, 2), (3, 4), (4, 3)}),
    'r5': ({1, 2, 3}, {(1, 1), (1, 2), (2, 2), (1, 3), (2, 3), (3, 3)}),
    'r6': ({1, 2, 3}, {(1, 2), (2, 1)}),
    'r7': ({0, 1, 2, 3}, {(a, b) for a in range(4) for b in range(4) if (a - b) % 2 == 0}),
    'r8': ({1, 2, 3, 4}, {(1, 2), (2, 3), (1, 3), (3, 4), (2, 4), (1, 4)}),
    'r9': ({1, 2, 3}, set()),
    'r10': ({1, 2, 3}, {(a, b) for a in range(1, 4) for b in range(1, 4)}),
    'r11': ({1, 2, 3, 4}, {(1, 1), (2, 2), (3, 3), (4, 4), (1, 3), (3, 1)}),
    'r12': ({1, 2, 3}, {(1, 1), (2, 2), (1, 2), (2, 3)}),
}


# ---------------------------------------------------------------- 1. relations and inverses
def s1(b):
    for L, A, rule, f in (('cp2', [1, 2, 3, 4], 'a < b', lambda a, c: a < c), ('cp2', [1, 2, 3, 4, 6], 'a divides b and a ≠ b', lambda a, c: c % a == 0 and a != c),
                          ('cp1', [0, 1, 2, 3], 'a + b = 3', lambda a, c: a + c == 3), ('cp1', [1, 2, 3, 4, 5], 'b = 2a − 1', lambda a, c: c == 2 * a - 1),
                          ('honors', [-2, -1, 0, 1, 2], 'a² = b²', lambda a, c: a * a == c * c), ('honors', [1, 2, 3, 4, 5, 6], 'a ≡ b (mod 3) and a < b', lambda a, c: (a - c) % 3 == 0 and a < c)):
        R = {(a, c) for a in A for c in A if f(a, c)}
        b.sa(1, L, 'Let A = %s and define the relation R on A by a R b if and only if %s. List R as a set of ordered pairs, ordered by first then second coordinate.' % (fmt_set(A), rule), pairs(R),
             ['Test every ordered pair (a, b) in A × A.', 'R = %s' % pairs(R)], 'list_relation')
    for L, key in (('cp2', 'r2'), ('cp1', 'r12'), ('honors', 'r8')):
        A, R = RELS[key]
        b.sa(1, L, 'Let A = %s and R = %s. Find the inverse relation R⁻¹ (ordered by first coordinate).' % (fmt_set(A), pairs(R)), pairs(inv(R)),
             ['R⁻¹ = {(b, a) | (a, b) ∈ R}: reverse every pair.', 'R⁻¹ = %s' % pairs(inv(R))], 'inverse_relation')
    INV = [('cp2', 'R is "x is taller than y" on a set of people.', '"x is shorter than y"', ['"x is taller than y"', '"x is not taller than y"', '"x is the same height as y"']),
           ('cp1', 'R is "x divides y" on the positive integers.', '"x is a multiple of y"', ['"x divides y"', '"x does not divide y"', '"y is a multiple of x"']),
           ('honors', 'R is "x < y" on the real numbers.', '"x > y"', ['"x ≥ y"', '"x ≤ y"', '"x ≠ y"'])]
    for L, t, good, bad in INV:
        b.mc(1, L, '%s Describe R⁻¹.' % t, good, bad, ['x R⁻¹ y means y R x.', 'R⁻¹: ' + good], 'inverse_words')
    MEM = [('cp2', 'A = {1, 2, 3, 4}, R = {(a, b) | a + b is even}. Is (1, 3) ∈ R?', 'Yes', '1 + 3 = 4 is even.'),
           ('cp1', 'R on ℤ: m R n if and only if 4 | (m − n). Is 7 R (−5)?', 'Yes', '7 − (−5) = 12 is divisible by 4.'),
           ('cp1', 'R on ℝ: x R y if and only if x² + y² = 25. Is (3, −4) ∈ R?', 'Yes', '9 + 16 = 25.'),
           ('honors', 'R on ℤ: m R n if and only if m − n is odd. Is (5, 5) ∈ R?', 'No', '5 − 5 = 0 is even.'),
           ('honors', 'R on the set of strings over {0, 1}: s R t if and only if s and t have the same number of 1s. Is 0110 R 1001?', 'Yes', 'Both have two 1s.')]
    for L, t, a, why in MEM:
        b.mc(1, L, t, a, ['No' if a == 'Yes' else 'Yes', 'Only (3, 1) is in R', 'The question is meaningless for infinite sets'], [why], 'relation_member')
    b.sel(1, 'cp2', 'Let A = {1, 2, 3} and R = "a ≤ b". Which pairs are in R?', [('(1, 2)', True), ('(2, 2)', True), ('(1, 3)', True), ('(3, 1)', False), ('(3, 2)', False)], ['a ≤ b must hold.'], 'relation_select')
    b.sel(1, 'cp1', 'R = {(1, 2), (2, 3), (3, 3)}. Which pairs are in R⁻¹?', [('(2, 1)', True), ('(3, 2)', True), ('(3, 3)', True), ('(1, 2)', False), ('(2, 3)', False)], ['Reverse each pair.'], 'relation_select')
    b.sel(1, 'honors', 'For any relation R on a set A, which statements are true?', [('(R⁻¹)⁻¹ = R', True), ('R is symmetric if and only if R = R⁻¹', True), ('R⁻¹ ⊆ A × A', True), ('R ∩ R⁻¹ = ∅', False), ('R ∪ R⁻¹ = A × A', False)],
          ['Reversing twice returns R; symmetry means R contains each reversal.', 'R ∩ R⁻¹ contains (a, a) pairs, and R ∪ R⁻¹ need not be everything.'], 'relation_select')
    b.orq(1, 'cp2', 'A = {1, 2, 3, 4}. R: a R b if and only if b = a + 1.',
          [('List R.', '{(1, 2), (2, 3), (3, 4)}'), ('List R⁻¹.', '{(2, 1), (3, 2), (4, 3)}'), ('Describe R⁻¹ with a rule.', 'a R⁻¹ b if and only if b = a − 1'), ('How many pairs are in A × A that are NOT in R?', '13')],
          ['Check each a.', 'Reverse.', 'Swap roles.', '16 − 3.'], 'relation_or')
    b.orq(1, 'cp1', 'R on {1, 2, 3, 4, 6, 12}: a R b if and only if a | b.',
          [('How many pairs are in R?', str(sum(1 for a in [1, 2, 3, 4, 6, 12] for c in [1, 2, 3, 4, 6, 12] if c % a == 0))), ('Is (4, 6) ∈ R?', 'No'), ('List all b with 3 R b.', '3, 6, 12'), ('Describe R⁻¹.', 'a R⁻¹ b if and only if a is a multiple of b')],
          ['Count divisors.', '4 ∤ 6.', 'Multiples of 3.', 'Reverse.'], 'relation_or')
    b.orq(1, 'honors', 'Let R = {(x, y) ∈ ℝ × ℝ | y = x²}.',
          [('Is R a function from ℝ to ℝ?', 'Yes; each x has exactly one y.'), ('Describe R⁻¹.', '{(x, y) | x = y²}'), ('Is R⁻¹ a function from ℝ to ℝ? Explain.', 'No; (4, 2) and (4, −2) are both in R⁻¹, and negative x has no partner.'),
           ('Find R ∩ R⁻¹.', '{(0, 0), (1, 1)}')],
          ['Each input once.', 'Swap coordinates.', 'Fails vertical line test.', 'y = x² and x = y² give x = x⁴.'], 'relation_or')


# ---------------------------------------------------------------- 2. directed graphs
def s2(b):
    for k, (L, key) in enumerate((('cp2', 'r1'), ('cp2', 'r2'), ('cp1', 'r4'), ('cp1', 'r12'), ('honors', 'r8'), ('honors', 'r11'))):
        A, R = RELS[key]
        p = figs.graph(U, 'digraph_%s' % key, sorted(A), sorted(R), directed=True)
        alt = 'Directed graph on vertices %s with arrows: %s (a loop means (a, a)).' % (', '.join(map(str, sorted(A))), '; '.join('%s→%s' % e for e in sorted(R)))
        if k % 2 == 0:
            r = b.sa(2, L, 'The directed graph shows a relation R on A = %s (a loop at a vertex means (a, a) ∈ R). List R as a set of ordered pairs, ordered by first then second coordinate.' % fmt_set(A), pairs(R),
                     ['Each arrow from a to b is the pair (a, b); each loop at a is (a, a).', 'R = %s' % pairs(R)], 'read_digraph')
        else:
            pr = props(R, A)
            good = ', '.join(k2 for k2, v in pr.items() if v) or 'none of these'
            opts_all = ['reflexive', 'symmetric', 'transitive']
            r = b.sel(2, L, 'The directed graph shows a relation R on A = %s (loops mean (a, a) ∈ R). Which properties does R have?' % fmt_set(A),
                      [(p_, pr[p_]) for p_ in opts_all] + [('none of these three properties', not any(pr.values())), ('R is a function from A to A', all(sum(1 for x in R if x[0] == a) == 1 for a in A))],
                      ['Reflexive: a loop at every vertex. Symmetric: every arrow has a reverse arrow. Transitive: every two-step path a→b→c has a shortcut a→c.',
                       'Here: ' + ', '.join('%s %s' % (k2, 'yes' if v else 'no') for k2, v in pr.items())], 'digraph_props') if sum(pr.values()) + (not any(pr.values())) + all(sum(1 for x in R if x[0] == a) == 1 for a in A) >= 2 else \
                b.mc(2, L, 'The directed graph shows a relation R on A = %s (loops mean (a, a) ∈ R). How many ordered pairs are in R?' % fmt_set(A), str(len(R)), [str(len(R) - 1), str(len(R) + 1), str(len(R) + len(A))],
                     ['Count arrows and loops.', '%d pairs' % len(R)], 'read_digraph')
        b.image(r, p, alt)
    DRAW = [('cp2', 'How many loops appear in the directed graph of R = {(a, b) | a ≤ b} on A = {1, 2, 3}?', 3, 'Each (a, a) with a ≤ a gives a loop: 3.'),
            ('cp1', 'How many arrows (not counting loops) appear in the directed graph of R = {(a, b) | a divides b} on A = {1, 2, 3, 4, 6}?', sum(1 for a in [1, 2, 3, 4, 6] for c in [1, 2, 3, 4, 6] if c % a == 0 and a != c), 'Count pairs a | b with a ≠ b.'),
            ('honors', 'In the directed graph of R = {(a, b) | a − b is even} on A = {1, 2, 3, 4, 5}, how many arrows (not counting loops) are there?', sum(1 for a in range(1, 6) for c in range(1, 6) if (a - c) % 2 == 0 and a != c), 'Within {1, 3, 5}: 6 arrows; within {2, 4}: 2 arrows.')]
    for L, t, v, why in DRAW:
        b.sa(2, L, t, v, [why, 'Answer: %d' % v], 'digraph_count')
    b.mc(2, 'cp2', 'In the directed graph of a relation, what does a loop at vertex 4 mean?', '(4, 4) is in the relation', ['4 is not related to anything', '4 is related to every element', 'The relation is symmetric'],
         ['A loop is an arrow from 4 back to 4.'], 'digraph_meaning')
    b.mc(2, 'cp1', 'In a directed graph of a relation, an arrow from 2 to 5 but none from 5 to 2 shows the relation is NOT ...', 'symmetric', ['reflexive', 'transitive', 'a relation'],
         ['Symmetric requires (5, 2) whenever (2, 5).'], 'digraph_meaning')
    b.mc(2, 'honors', 'A directed graph has arrows 1→2 and 2→3 but no arrow 1→3. Which property fails?', 'Transitivity', ['Reflexivity', 'Symmetry', 'Antisymmetry'],
         ['Transitive requires (1, 3) whenever (1, 2) and (2, 3).'], 'digraph_meaning')
    b.orq(2, 'cp2', 'Draw (in words) the directed graph of R = {(1, 1), (1, 2), (2, 3), (3, 1)} on A = {1, 2, 3}.',
          [('How many vertices?', '3'), ('Which vertex has a loop?', '1'), ('List the arrows that are not loops.', '1→2, 2→3, 3→1'), ('Is R symmetric? Explain using the graph.', 'No; 1→2 has no reverse arrow 2→1.')],
          ['One per element.', '(1, 1).', 'Pairs with different coordinates.', 'Look for reverse arrows.'], 'digraph_or')
    b.orq(2, 'cp1', 'R on A = {1, 2, 3, 4}: a R b if and only if a < b.',
          [('How many arrows are in its directed graph?', '6'), ('Are there loops?', 'No'), ('Which property does the graph show it has: reflexive, symmetric or transitive?', 'Transitive'), ('Describe the graph of R⁻¹.', 'The same graph with every arrow reversed.')],
          ['C(4, 2).', 'a < a is false.', 'a < b < c gives a < c.', 'Reverse arrows.'], 'digraph_or')
    b.orq(2, 'honors', 'A relation R on A = {a, b, c, d} has directed graph a→b, b→c, c→d (no loops).',
          [('List the pairs needed to make the transitive closure.', '(a, c), (b, d), (a, d)'), ('How many pairs are in the transitive closure?', '6'), ('Is the closure symmetric?', 'No'),
           ('Describe the closure in words.', 'x is related to y exactly when y comes after x in the chain a, b, c, d.')],
          ['Add shortcuts for two-step paths, then repeat.', '3 + 3.', 'No reverse arrows.', 'A strict linear order.'], 'digraph_or')


# ---------------------------------------------------------------- 3. reflexive, symmetric, transitive
def s3(b):
    plan = {'cp2': ['r3', 'r6', 'r9', 'r1'], 'cp1': ['r2', 'r5', 'r12', 'r4'], 'honors': ['r8', 'r11', 'r7', 'r10']}
    for L, keys in plan.items():
        for j, key in enumerate(keys):
            A, R = RELS[key]
            pr = props(R, A)
            if j % 2 == 0:
                which = ['reflexive', 'symmetric', 'transitive'][j % 3]
                v = pr[which]
                b.mc(3, L, 'Let A = %s and R = %s. Is R %s?' % (fmt_set(A), pairs(R), which), 'Yes' if v else 'No', ['No' if v else 'Yes', 'Only if R is also symmetric', 'Cannot be determined from a finite list'],
                     [{'reflexive': 'Reflexive: (a, a) ∈ R for every a ∈ A.', 'symmetric': 'Symmetric: (a, b) ∈ R implies (b, a) ∈ R.', 'transitive': 'Transitive: (a, b), (b, c) ∈ R imply (a, c) ∈ R.'}[which],
                      ('Yes.' if v else 'No: ' + witness(R, A, which))], 'check_property')
            else:
                b.sel(3, L, 'Let A = %s and R = %s. Which properties does R have?' % (fmt_set(A), pairs(R)),
                      [('Reflexive', pr['reflexive']), ('Symmetric', pr['symmetric']), ('Transitive', pr['transitive']), ('An equivalence relation', all(pr.values())), ('None of reflexive, symmetric, transitive', not any(pr.values()))]
                      if sum(pr.values()) + all(pr.values()) + (not any(pr.values())) >= 2 else
                      [('Reflexive', pr['reflexive']), ('Symmetric', pr['symmetric']), ('Transitive', pr['transitive']), ('Not reflexive', not pr['reflexive']), ('Not symmetric', not pr['symmetric'])],
                      ['Check each definition; a single failing pair disproves a property.'] + ['%s: %s' % (k2, 'yes' if v else 'no (' + witness(R, A, k2) + ')') for k2, v in pr.items()], 'select_properties')
    INF = [('cp2', '"x = y" on ℝ', 'reflexive, symmetric and transitive'), ('cp2', '"x < y" on ℝ', 'transitive only'), ('cp1', '"x ≤ y" on ℝ', 'reflexive and transitive only'),
           ('cp1', '"x ≠ y" on ℤ', 'symmetric only'), ('honors', '"m − n is odd" on ℤ', 'symmetric only'), ('honors', '"x is a sibling of y" (sharing at least one parent; nobody is their own sibling)', 'symmetric only')]
    opts = ['reflexive, symmetric and transitive', 'transitive only', 'reflexive and transitive only', 'symmetric only', 'reflexive and symmetric only', 'none of the three']
    for L, rel, good in INF:
        b.mc(3, L, 'Which properties does the relation %s have?' % rel, good, [o for o in opts if o != good][:3],
             ['Test each definition with general elements, and look for counterexamples.',
              {'"x < y" on ℝ': 'Not reflexive (1 < 1 false), not symmetric (1 < 2 but not 2 < 1), transitive.',
               '"x ≤ y" on ℝ': 'Reflexive and transitive; 1 ≤ 2 but not 2 ≤ 1.', '"x ≠ y" on ℤ': 'Not reflexive; symmetric; not transitive (1 ≠ 2, 2 ≠ 1, but 1 = 1).',
               '"m − n is odd" on ℤ': 'Not reflexive (0 is even); symmetric; not transitive (1 − 2 and 2 − 3 odd, 1 − 3 even).',
               '"x = y" on ℝ': 'Equality is an equivalence relation.'}.get(rel, 'Siblings: symmetric; not reflexive; not transitive (A and B are siblings, B and A are siblings, but A is not A\'s sibling).')], 'infinite_properties')
    b.orq(3, 'cp1', 'Let A = {1, 2, 3} and R = {(1, 1), (2, 2), (1, 2), (2, 3)}.',
          [('Is R reflexive? Explain.', 'No; (3, 3) ∉ R.'), ('Is R symmetric? Explain.', 'No; (1, 2) ∈ R but (2, 1) ∉ R.'), ('Is R transitive? Explain.', 'No; (1, 2), (2, 3) ∈ R but (1, 3) ∉ R.'),
           ('Add the fewest pairs to make R reflexive and transitive.', '(3, 3) and (1, 3)')],
          ['Loops.', 'Reverse pairs.', 'Shortcut.', 'Then check all compositions again.'], 'properties_or')
    b.orq(3, 'cp2', 'Let A = {a, b} and R = {(a, a), (a, b)}.',
          [('Is R reflexive?', 'No; (b, b) is missing.'), ('Is R symmetric?', 'No; (b, a) is missing.'), ('Is R transitive?', 'Yes'), ('Which single pair would make R reflexive?', '(b, b)')],
          ['Every element needs a loop.', 'Reverse of (a, b).', 'Only compositions a→a→b give (a, b) ∈ R.', 'Add the missing loop.'], 'properties_or')
    b.orq(3, 'honors', 'Find relations on A = {1, 2, 3} with exactly the listed properties.',
          [('Reflexive and symmetric but not transitive.', 'For example {(1,1),(2,2),(3,3),(1,2),(2,1),(2,3),(3,2)}'), ('Symmetric and transitive but not reflexive.', 'For example {(1,1),(1,2),(2,1),(2,2)}'),
           ('Reflexive and transitive but not symmetric.', 'For example {(1,1),(2,2),(3,3),(1,2)}'), ('Explain why "symmetric and transitive implies reflexive" is false.', 'An element related to nothing (3 above) never gets a loop.')],
          ['Check each property.', 'Element 3 is unrelated.', 'One one-way pair.', 'The argument a R b ⇒ b R a ⇒ a R a needs some b.'], 'properties_or')


def witness(R, A, which):
    if which == 'reflexive':
        a = next(a for a in sorted(A) if (a, a) not in R)
        return '(%s, %s) ∉ R' % (a, a)
    if which == 'symmetric':
        a, c = next(x for x in sorted(R) if (x[1], x[0]) not in R)
        return '(%s, %s) ∈ R but (%s, %s) ∉ R' % (a, c, c, a)
    a, c, d = next((a, c, d) for a, c in sorted(R) for c2, d in sorted(R) if c == c2 and (a, d) not in R)
    return '(%s, %s), (%s, %s) ∈ R but (%s, %s) ∉ R' % (a, c, c, d, a, d)


# ---------------------------------------------------------------- 4. finite and infinite sets
def s4(b):
    INFQ = [('cp2', 'R on ℤ: m R n if and only if m + n is even. Is R reflexive?', 'Yes', 'm + m = 2m is even.'),
            ('cp2', 'R on ℝ: x R y if and only if x < y + 1. Is 3 R 3.5?', 'Yes', '3 < 4.5.'),
            ('cp1', 'R on ℤ: m R n if and only if m + n is even. Is R transitive?', 'Yes', 'm + n and n + p even ⇒ m + p = (m + n) + (n + p) − 2n is even.'),
            ('cp1', 'R on ℝ: x R y if and only if |x − y| < 1. Is R transitive?', 'No', '0 R 0.6 and 0.6 R 1.2, but |0 − 1.2| = 1.2 is not less than 1.'),
            ('honors', 'R on ℤ⁺: a R b if and only if gcd(a, b) > 1. Is R reflexive?', 'No', 'gcd(1, 1) = 1, so (1, 1) ∉ R.'),
            ('honors', 'R on ℝ: x R y if and only if x − y ∈ ℚ. Is R transitive?', 'Yes', '(x − y) + (y − z) = x − z, and a sum of rationals is rational.')]
    for L, t, a, why in INFQ:
        b.mc(4, L, t, a, ['No' if a == 'Yes' else 'Yes', 'Cannot be decided on an infinite set', 'Only for positive numbers'], [why, 'Infinite sets need a general argument or a single counterexample.'], 'infinite_check')
    COUNT = [('cp2', 'How many ordered pairs are in A × A if |A| = 4?', 16), ('cp1', 'How many different relations are there on a set with 3 elements?', 2 ** 9),
             ('cp1', 'How many reflexive relations are there on a set with 3 elements?', 2 ** 6), ('honors', 'How many symmetric relations are there on a set with 3 elements?', 2 ** 6),
             ('honors', 'How many relations on a 3-element set are both reflexive and symmetric?', 2 ** 3), ('cp2', 'How many ordered pairs are in the relation "a = b" on A = {1, 2, 3, 4, 5}?', 5)]
    for L, t, v in COUNT:
        b.sa(4, L, t, v, ['A relation is a subset of A × A; count the free choices.', {16: '4·4 = 16.', 512: '|A × A| = 9 pairs, each in or out: 2⁹.', 64: 'Forced or paired choices leave 6 free decisions: 2⁶.', 8: '3 loops forced; 3 pairs {a, b} chosen together: 2³.', 5: 'Only (a, a) pairs.'}[v]], 'count_relations')
    b.sel(4, 'cp2', 'R on ℤ: a R b if and only if a ≤ b. Which pairs are in R?', [('(−3, 0)', True), ('(5, 5)', True), ('(2, 7)', True), ('(4, 1)', False), ('(0, −1)', False)], ['Check a ≤ b.'], 'infinite_select')
    b.sel(4, 'cp1', 'R on ℤ: a R b if and only if 5 | (a − b). Which statements are true?', [('12 R 2', True), ('−3 R 7', True), ('R is symmetric', True), ('4 R 6', False), ('R is not transitive', False)],
          ['12 − 2 = 10, −3 − 7 = −10; 4 − 6 = −2.', 'Congruence mod 5 is an equivalence relation.'], 'infinite_select')
    b.sel(4, 'honors', 'Which relations on ℝ are transitive?', [('x ≤ y', True), ('x = y', True), ('x − y is an integer', True), ('|x − y| ≤ 1', False), ('xy > 0 or x = y = 0... (x and y have the same sign, 0 related only to 0)', True)][:5],
          ['|x − y| ≤ 1 fails: 0, 1, 2.', 'The others are orders or equivalence relations.'], 'infinite_select')
    b.orq(4, 'cp1', 'R on ℤ: m R n if and only if m − n is a multiple of 3.',
          [('Show R is reflexive.', 'm − m = 0 = 3·0.'), ('Show R is symmetric.', 'If m − n = 3k then n − m = 3(−k).'), ('Show R is transitive.', 'm − n = 3k and n − p = 3j give m − p = 3(k + j).'), ('Is 14 R (−1)?', 'Yes, 15 is a multiple of 3.')],
          ['Definition.', 'Negate.', 'Add.', 'Compute.'], 'infinite_or')
    b.orq(4, 'cp2', 'R on the positive integers: a R b if and only if a divides b.',
          [('Is 3 R 12?', 'Yes'), ('Is 12 R 3?', 'No'), ('Is R reflexive? Explain.', 'Yes; a = a·1.'), ('Is R symmetric? Explain.', 'No; 3 | 12 but 12 ∤ 3.')],
          ['12 = 3·4.', '3/12 is not an integer.', 'Every a divides itself.', 'Counterexample.'], 'infinite_or')
    b.orq(4, 'honors', 'R on ℝ²: (a, b) R (c, d) if and only if a² + b² = c² + d².',
          [('Is (3, 4) R (5, 0)?', 'Yes, both give 25.'), ('Prove R is an equivalence relation.', 'It is equality of the function f(a, b) = a² + b², which is reflexive, symmetric and transitive.'),
           ('Describe the equivalence class of (1, 0).', 'The unit circle x² + y² = 1.'), ('Describe all equivalence classes.', 'Circles centered at the origin, plus the single point (0, 0).')],
          ['Compute.', 'Relations defined by f(x) = f(y) are equivalence relations.', 'Distance 1.', 'Level sets.'], 'infinite_or')


# ---------------------------------------------------------------- 5. partitions and induced relations
def is_partition(blocks, A):
    seen = set()
    for bl in blocks:
        if not bl or seen & bl:
            return False
        seen |= bl
    return seen == A


def s5(b):
    A = {1, 2, 3, 4, 5, 6}
    PT = [('cp2', [{1, 2}, {3, 4}, {5, 6}]), ('cp2', [{1, 2, 3}, {3, 4, 5, 6}]), ('cp2', [{1, 2}, {4, 5, 6}]), ('cp1', [{1}, {2, 3, 4, 5, 6}]), ('cp1', [{1, 3, 5}, {2, 4, 6}, set()]),
          ('cp1', [{1, 6}, {2, 5}, {3, 4}]), ('honors', [{1, 2, 3, 4, 5, 6}]), ('honors', [{1}, {2}, {3}, {4}, {5}, {6}]), ('honors', [{1, 4}, {2, 5}, {3}, {6, 4}])]
    for L, blocks in PT:
        ok = is_partition(blocks, A)
        why = 'The blocks are nonempty, do not overlap, and cover A.' if ok else (
            'It contains the empty set.' if any(not x for x in blocks) else 'Some element is in two blocks.' if sum(len(x) for x in blocks) > len(set().union(*blocks)) else 'Some element of A is in no block.')
        b.mc(5, L, 'Is {%s} a partition of A = {1, 2, 3, 4, 5, 6}?' % ', '.join(fmt_set(x) for x in blocks), 'Yes' if ok else 'No: ' + why[0].lower() + why[1:-1],
             ['No: some element is in two blocks', 'No: some element of A is in no block', 'No: it contains the empty set', 'Yes'] if ok else
             ['Yes', 'No: the blocks have different sizes', 'No: a partition must have exactly two blocks'],
             [why], 'is_partition')
    IND = [('cp2', [{1, 2}, {3}]), ('cp1', [{1, 3}, {2, 4}]), ('honors', [{1}, {2, 3, 4}])]
    for L, blocks in IND:
        R = {(x, y) for bl in blocks for x in bl for y in bl}
        AA = set().union(*blocks)
        b.sa(5, L, 'Find the relation induced by the partition {%s} of %s: x R y if and only if x and y are in the same block. List R ordered by first then second coordinate.' % (', '.join(fmt_set(x) for x in blocks), fmt_set(AA)), pairs(R),
             ['Pair every element with every element of its own block (including itself).', 'R = %s (%d pairs)' % (pairs(R), len(R))], 'induced_relation')
    CNT = [('cp1', 'How many ordered pairs are in the relation induced by the partition {{1, 2, 3}, {4, 5}} of {1, 2, 3, 4, 5}?', 9 + 4),
           ('honors', 'How many partitions does the set {1, 2, 3} have?', 5), ('honors', 'How many partitions of {1, 2, 3, 4} have exactly two blocks?', 7), ('cp2', 'How many ordered pairs are in the relation induced by {{a, b}, {c}}?', 5)]
    for L, t, v in CNT:
        b.sa(5, L, t, v, ['Each block of size k contributes k² pairs; count partitions by listing.', 'Answer: %d' % v], 'partition_count')
    b.sel(5, 'cp2', 'Which collections are partitions of {a, b, c, d}?', [('{{a, b}, {c, d}}', True), ('{{a}, {b, c, d}}', True), ('{{a, b}, {b, c, d}}', False), ('{{a, b}, {c}}', False), ('{{a}, {b}, {c}, {d}}', True)],
          ['Blocks must be nonempty, disjoint and cover the set.'], 'partition_select')
    b.sel(5, 'cp1', 'Which partitions of ℤ are correct?', [('{evens, odds}', True), ('{negatives, {0}, positives}', True), ('{multiples of 3, numbers ≡ 1 (mod 3), numbers ≡ 2 (mod 3)}', True),
                                                          ('{multiples of 2, multiples of 3, the rest}', False), ('{positives, negatives}', False)],
          ['6 is a multiple of 2 and 3 (overlap); 0 is neither positive nor negative.'], 'partition_select')
    b.sel(5, 'honors', 'The relation induced by a partition is always ...', [('reflexive', True), ('symmetric', True), ('transitive', True), ('antisymmetric', False), ('empty', False)],
          ['Being in the same block is an equivalence relation (Theorem: induced relations are equivalence relations).'], 'partition_select')
    b.orq(5, 'cp1', 'Partition of A = {1, 2, 3, 4, 5}: {{1, 4}, {2, 3, 5}}.',
          [('Is 2 R 5 in the induced relation?', 'Yes'), ('Is 1 R 2?', 'No'), ('How many pairs does R have?', '13'), ('Why is R symmetric?', 'If x and y are in the same block, so are y and x.')],
          ['Same block.', 'Different blocks.', '2² + 3².', 'Same block is a symmetric condition.'], 'partition_or')
    b.orq(5, 'cp2', 'Students are grouped by birth month.',
          [('Explain why the groups form a partition of the class.', 'Each student is in exactly one month group (empty months are not used as blocks).'), ('What is the induced relation?', 'x R y if and only if x and y have the same birth month.'),
           ('Is every student related to themselves?', 'Yes'), ('What is the largest possible number of blocks?', '12')],
          ['Disjoint and covering.', 'Same block.', 'Reflexive.', 'One per month.'], 'partition_or')
    b.orq(5, 'honors', 'Let A = {1, 2, 3, 4}.',
          [('How many partitions of A have exactly 3 blocks?', '6'), ('How many partitions have exactly one block?', '1'), ('Find the total number of partitions (Bell number B₄).', '15'),
           ('How many equivalence relations are there on A? Why?', '15; partitions and equivalence relations correspond one-to-one.')],
          ['Choose the pair that shares a block: C(4, 2).', 'All together.', '1 + 7 + 6 + 1.', 'Fundamental correspondence.'], 'partition_or')


# ---------------------------------------------------------------- 6. equivalence relations
def s6(b):
    EQ = [('cp2', '"has the same birthday as" on people', True, 'Equality of a feature is reflexive, symmetric and transitive.'),
          ('cp2', '"is taller than" on people', False, 'Not reflexive (no one is taller than themselves).'),
          ('cp1', 'm R n if and only if m ≡ n (mod 4), on ℤ', True, 'Congruence mod n is an equivalence relation.'),
          ('cp1', 'x R y if and only if |x − y| ≤ 2, on ℤ', False, 'Not transitive: 0 R 2 and 2 R 4 but not 0 R 4.'),
          ('honors', 's R t if and only if strings s and t have the same length, on bit strings', True, 'Equality of length.'),
          ('honors', 'a R b if and only if a | b, on ℤ⁺', False, 'Not symmetric: 2 | 4 but 4 ∤ 2.'),
          ('cp1', 'L₁ R L₂ if and only if lines L₁ and L₂ are parallel or equal, on lines in the plane', True, 'Parallel-or-equal is reflexive, symmetric and transitive.'),
          ('honors', 'L₁ R L₂ if and only if L₁ ⊥ L₂, on lines in the plane', False, 'Not reflexive and not transitive.')]
    for L, rel, t, why in EQ:
        b.mc(6, L, 'Is %s an equivalence relation?' % rel, 'Yes' if t else 'No', ['No' if t else 'Yes', 'Only on finite sets', 'Yes, because it is symmetric'],
             ['An equivalence relation is reflexive, symmetric and transitive.', why], 'is_equivalence')
    for L, key in (('cp2', 'r3'), ('cp1', 'r4'), ('honors', 'r12')):
        A, R = RELS[key]
        pr = props(R, A)
        t = all(pr.values())
        b.mc(6, L, 'Is R = %s an equivalence relation on A = %s?' % (pairs(R), fmt_set(A)), 'Yes' if t else 'No', ['No' if t else 'Yes', 'Only if A is infinite', 'It is symmetric, so yes'],
             ['Check all three properties: ' + ', '.join('%s %s' % (k2, 'yes' if v else 'no') for k2, v in pr.items()) + '.'], 'is_equivalence')
    MISS = [('cp1', {1, 2, 3}, {(1, 1), (2, 2), (3, 3), (1, 2)}), ('honors', {1, 2, 3}, {(1, 1), (2, 2), (3, 3), (1, 2), (2, 1), (2, 3), (3, 2)}), ('cp2', {1, 2}, {(1, 2), (2, 1)})]
    for L, A, R in MISS:
        full = closure_t(R | inv(R) | {(a, a) for a in A})
        miss = full - R
        b.sa(6, L, 'Find the smallest set of ordered pairs to ADD to R = %s so that R becomes an equivalence relation on %s. List the added pairs in order.' % (pairs(R), fmt_set(A)), pairs(miss),
             ['Add missing loops, reverse pairs, and shortcuts until nothing changes.', 'Add %s.' % pairs(miss)], 'equivalence_closure')
    b.sel(6, 'cp2', 'Which relations are equivalence relations?', [('"is the same age as" on students', True), ('"=" on numbers', True), ('"lives in the same town as" (each person lives in one town)', True), ('"is a friend of"', False), ('"is older than"', False)],
          ['Same-feature relations are equivalences; friendship need not be transitive; "older than" is not reflexive.'], 'equivalence_select')
    b.sel(6, 'cp1', 'R: a R b if and only if a ≡ b (mod 5), on ℤ. Which statements are true?', [('R is reflexive', True), ('R is symmetric', True), ('R is transitive', True), ('3 R 13', True), ('2 R 9', False)],
          ['Congruence mod 5; 9 − 2 = 7 is not a multiple of 5.'], 'equivalence_select')
    b.sel(6, 'honors', 'Which relations on ℝ are equivalence relations?', [('x R y ⟺ x − y ∈ ℤ', True), ('x R y ⟺ ⌊x⌋ = ⌊y⌋', True), ('x R y ⟺ x² = y²', True), ('x R y ⟺ xy ≥ 0', False), ('x R y ⟺ |x − y| < 1', False)],
          ['xy ≥ 0 fails transitivity: 1 R 0 and 0 R −1 but not 1 R −1.', '|x − y| < 1 fails transitivity.'], 'equivalence_select')
    b.orq(6, 'cp2', 'R on {1, 2, 3, 4}: a R b if and only if a and b have the same parity.',
          [('List the pairs related to 1.', '(1, 1), (1, 3)'), ('Is R reflexive?', 'Yes'), ('Is R symmetric and transitive?', 'Yes'), ('Is R an equivalence relation?', 'Yes')],
          ['Odd numbers.', 'Same parity as itself.', 'Same-feature relation.', 'All three hold.'], 'equivalence_or')
    b.orq(6, 'cp1', 'Prove that R on ℤ, a R b if and only if a² ≡ b² (mod 3), is an equivalence relation.',
          [('Reflexive.', 'a² − a² = 0 is divisible by 3.'), ('Symmetric.', 'If 3 | a² − b² then 3 | b² − a².'), ('Transitive.', '3 | a² − b² and 3 | b² − c² imply 3 | a² − c².'), ('Is 2 R 4? Is 3 R 5?', '2 R 4 (4 and 16 both ≡ 1); 3 not R 5 (0 vs 1).')],
          ['Zero.', 'Negate.', 'Add.', 'Squares mod 3.'], 'equivalence_or')
    b.orq(6, 'honors', 'R on ℤ × (ℤ − {0}): (a, b) R (c, d) if and only if ad = bc.',
          [('Show R is reflexive and symmetric.', 'ab = ba; ad = bc gives cb = da.'), ('Show R is transitive.', 'ad = bc and cf = de ⇒ adf = bcf = bde ⇒ af = be (since d ≠ 0).'),
           ('Is (2, 4) R (3, 6)?', 'Yes; 12 = 12.'), ('What do the equivalence classes represent?', 'Rational numbers: (a, b) represents a/b.')],
          ['Commutativity.', 'Multiply and cancel d.', 'Cross-multiply.', 'Equal fractions.'], 'equivalence_or')


# ---------------------------------------------------------------- 7. equivalence classes
def s7(b):
    CL = [('cp2', {1, 2, 3, 4, 5, 6}, lambda a, c: (a - c) % 2 == 0, 'a − b is even', 3), ('cp2', {1, 2, 3, 4, 5, 6}, lambda a, c: (a - c) % 3 == 0, 'a ≡ b (mod 3)', 4),
          ('cp1', set(range(0, 12)), lambda a, c: (a - c) % 4 == 0, 'a ≡ b (mod 4)', 7), ('cp1', {'cat', 'dog', 'emu', 'ox', 'yak', 'ant'}, lambda a, c: len(a) == len(c), 'a and b have the same number of letters', 'ox'),
          ('honors', set(range(-4, 5)), lambda a, c: a * a == c * c, 'a² = b²', -3), ('honors', set(range(1, 13)), lambda a, c: (a % 5) == (c % 5), 'a and b leave the same remainder when divided by 5', 10)]
    for L, A, f, rule, x in CL:
        cls = {y for y in A if f(x, y)}
        b.sa(5 + 2, L, 'On A = %s, the equivalence relation R is "%s". Find the equivalence class [%s]. Write it in roster notation, ordered.' % (fmt_set(A), rule, x), fmt_set(cls),
             ['[x] = {y ∈ A | x R y}.', '[%s] = %s' % (x, fmt_set(cls))], 'find_class')
    NUM = [('cp2', 'How many distinct equivalence classes does congruence mod 5 have on ℤ?', 5), ('cp1', 'R on {1, ..., 10}: a R b if and only if a ≡ b (mod 3). How many elements are in [1]?', 4),
           ('cp1', 'R on bit strings of length 3: s R t if and only if s and t have the same number of 1s. How many equivalence classes are there?', 4),
           ('honors', 'R on bit strings of length 6: same number of 1s. How many strings are in the class of 110100?', 15),
           ('honors', 'R on {1, ..., 30}: a R b if and only if a and b have the same remainder mod 7. How many classes have exactly 5 elements?', sum(1 for r in range(7) if len([n for n in range(1, 31) if n % 7 == r]) == 5))]
    for L, t, v in NUM:
        b.sa(7, L, t, v, ['Identify what the class of an element looks like and count.', 'Answer: %d' % v], 'class_count')
    for L, key in (('cp2', 'r11'), ('cp1', 'r4'), ('honors', 'r7')):
        A, R = RELS[key]
        cl = classes(R, A)
        good = '{' + ', '.join(fmt_set(c) for c in cl) + '}'
        wrongs = ['{' + ', '.join(fmt_set(c) for c in cl[:-1]) + '}', '{' + fmt_set(A) + '}', '{' + ', '.join(fmt_set({a}) for a in sorted(A)) + '}']
        b.mc(7, L, 'R = %s is an equivalence relation on A = %s. Which is the set of distinct equivalence classes?' % (pairs(R), fmt_set(A)), good, [w for w in wrongs if w != good] + ['{' + fmt_set(A) + ', ∅}'],
             ['[a] = {b | a R b}. Equal classes are listed once.', 'Classes: ' + good], 'list_classes')
    b.sel(7, 'cp2', 'For congruence mod 3 on ℤ, which numbers are in [2]?', [('5', True), ('−1', True), ('11', True), ('6', False), ('3', False)], ['[2] = {..., −1, 2, 5, 8, 11, ...}.'], 'class_select')
    b.sel(7, 'cp1', 'For any equivalence relation on A, which statements are true?', [('Every element is in its own class.', True), ('Two classes are either equal or disjoint.', True), ('The classes form a partition of A.', True),
                                                                                       ('Classes always have equal size.', False), ('Some class may be empty.', False)], ['a ∈ [a]; classes partition A; sizes can differ.'], 'class_select')
    b.sel(7, 'honors', 'R on ℝ: x R y if and only if x − y ∈ ℤ. Which numbers are in [0.25]?', [('1.25', True), ('−0.75', True), ('100.25', True), ('0.5', False), ('−0.25', False)],
          ['[0.25] = {0.25 + n | n ∈ ℤ}; −0.25 − 0.25 = −0.5 is not an integer.'], 'class_select')
    b.orq(7, 'cp1', 'R on A = {0, 1, ..., 9}: a R b if and only if a ≡ b (mod 4).',
          [('Find [0].', '{0, 4, 8}'), ('Find [1] and [5]. What do you notice?', '{1, 5, 9} both; they are the same class.'), ('List all distinct classes.', '{0, 4, 8}, {1, 5, 9}, {2, 6}, {3, 7}'), ('Do the classes form a partition of A?', 'Yes')],
          ['Multiples of 4.', '1 R 5.', 'Four remainders.', 'Disjoint and covering.'], 'class_or')
    b.orq(7, 'cp2', 'Students are related if they are in the same homeroom: H1 = {Ana, Bo}, H2 = {Cy, Di, Ed}.',
          [('Find [Ana].', '{Ana, Bo}'), ('Find [Di].', '{Cy, Di, Ed}'), ('How many classes are there?', '2'), ('Is Bo R Ed?', 'No')],
          ['Same homeroom.', 'Same homeroom.', 'One per homeroom.', 'Different homerooms.'], 'class_or')
    b.orq(7, 'honors', 'R on ℤ × ℤ: (a, b) R (c, d) if and only if a + d = b + c.',
          [('Show (3, 1) R (5, 3).', '3 + 3 = 1 + 5'), ('Describe [(3, 1)].', '{(a, b) | a − b = 2}'), ('Which integer does each class represent?', 'The difference a − b.'), ('How many classes are there?', 'Infinitely many, one for each integer.')],
          ['Check.', 'a + d = b + c ⟺ a − b = c − d.', 'Construction of ℤ from pairs.', 'One per integer.'], 'class_or')


def topup(b):
    need = lambda k, L: b.counter.get((k, L), 0) < 10
    rng = seeded('u6top')
    A = [1, 2, 3, 4]
    allp = [(a, c) for a in A for c in A]
    SEEN5 = set()
    for k in (1, 2, 3, 4, 5, 6, 7):
        for L in ('cp2', 'cp1', 'honors'):
            guard = 0
            while need(k, L) and guard < 12:
                guard += 1
                R = set(rng.sample(allp, rng.randint(4, 9)))
                if k in (1, 2):
                    if k == 1:
                        if sym(R):
                            continue
                        b.mc(1, L, 'Let A = {1, 2, 3, 4} and R = %s. Which set is R⁻¹?' % pairs(R), pairs(inv(R)), [pairs(R), pairs(inv(R) - {sorted(inv(R))[0]}), pairs(set(allp) - R)],
                             ['Reverse every pair.', 'R⁻¹ = %s' % pairs(inv(R))], 'inverse_relation')
                    else:
                        v = sum(1 for a in A if (a, a) in R)
                        b.mc(2, L, 'How many loops does the directed graph of R = %s on {1, 2, 3, 4} have?' % pairs(R), str(v), [], ['A loop is a pair (a, a).', '%d loops' % v], 'digraph_count')
                elif k in (3, 4):
                    which = ['reflexive', 'symmetric', 'transitive'][guard % 3]
                    R2 = closure_t(R) if which == 'transitive' and guard % 2 else (R | inv(R) if which == 'symmetric' and guard % 2 else R)
                    pr = props(R2, set(A))
                    v = pr[which]
                    b.mc(k, L, 'Let A = {1, 2, 3, 4} and R = %s. Is R %s?' % (pairs(R2), which), 'Yes' if v else 'No', ['No' if v else 'Yes', 'Only if R is also reflexive', 'Cannot be determined from a list'],
                         ['Check the definition of %s on every relevant pair.' % which, 'Yes.' if v else 'No: ' + witness(R2, set(A), which)], 'check_property')
                elif k == 5:
                    blocks = [set(rng.sample(A, rng.choice([1, 2, 3])))]
                    rest = [x for x in A if x not in blocks[0]]
                    blocks.append(set(rest))
                    Rr = {(x, y) for bl in blocks for x in bl for y in bl}
                    sig = tuple(sorted(tuple(sorted(x)) for x in blocks))
                    if sig in SEEN5:
                        continue
                    SEEN5.add(sig)
                    b.mc(5, L, 'How many ordered pairs are in the relation induced by the partition {%s} of {1, 2, 3, 4}?' % ', '.join(fmt_set(x) for x in blocks), str(len(Rr)), ['4', '16', '6'],
                         ['Each block of size k contributes k² pairs.', '%d pairs' % len(Rr)], 'induced_relation')
                elif k == 6:
                    E = closure_t(R | inv(R) | {(a, a) for a in A})
                    t = E == R
                    b.mc(6, L, 'Is R = %s an equivalence relation on {1, 2, 3, 4}?' % pairs(R), 'Yes' if t else 'No', ['No' if t else 'Yes', 'Only if A is infinite', 'Yes, because it contains loops'],
                         ['Check reflexive, symmetric and transitive: ' + ', '.join('%s %s' % (kk, 'yes' if vv else 'no') for kk, vv in props(R, set(A)).items()) + '.'], 'is_equivalence')
                elif k == 7:
                    m = rng.choice([3, 4, 5, 6])
                    x = rng.randint(0, 20)
                    cls = [n for n in range(0, 25) if (n - x) % m == 0]
                    b.sa(7, L, 'Congruence mod %d on A = {0, 1, ..., 24}. List the equivalence class [%d] in increasing order, separated by commas inside braces.' % (m, x), fmt_set(cls),
                         ['[x] = {y | y ≡ x (mod %d)}.' % m, fmt_set(cls)], 'find_class')


def errors(b):
    E = b.err
    E(1, 'cp2', 'R = {(1, 2), (3, 4)}. Find R⁻¹.', 'Jordan', ['R⁻¹ = {(−1, −2), (−3, −4)}'],
      '{(2, 1), (4, 3)}', 'Jordan treated "inverse" as negating numbers. The inverse relation reverses each pair.', 'R⁻¹ = {(b, a) | (a, b) ∈ R}.', ['Swap coordinates.'], 'inverse_negate_error')
    E(3, 'cp2', 'A = {1, 2, 3}, R = {(1, 1), (2, 2)}. Is R reflexive?', 'Sam', ['Yes, R has loops (1, 1) and (2, 2).'],
      'No', 'Sam checked only some elements. Reflexive needs (a, a) for EVERY a ∈ A, and (3, 3) is missing.', 'All loops are required.', ['(3, 3) ∉ R.'], 'partial_reflexive_error')
    E(3, 'cp2', 'R = {(1, 2), (2, 1), (1, 1)} on {1, 2}. Is R transitive?', 'Riley', ['(1, 2) and (2, 1) give (1, 1), which is in R. So R is transitive.'],
      'No', 'Riley checked one composition. (2, 1) and (1, 2) require (2, 2), which is missing.', 'Every chain a R b, b R c must be checked.', ['(2, 1), (1, 2) ∈ R but (2, 2) ∉ R.'], 'one_chain_error')
    E(5, 'cp2', 'Is {{1, 2}, {2, 3}} a partition of {1, 2, 3}?', 'Casey', ['Yes, every element appears.'],
      'No', 'Casey forgot the blocks must be disjoint; 2 is in both blocks.', 'Partitions: nonempty, disjoint, covering.', ['{1, 2} ∩ {2, 3} = {2} ≠ ∅.'], 'overlap_partition_error')
    E(2, 'cp2', 'Draw the digraph of R = {(1, 2)} on {1, 2}. Does it have an arrow from 2 to 1?', 'Avery', ['Yes, an arrow connects 1 and 2 in both directions.'],
      'No; only the arrow 1 → 2', 'Avery drew an undirected edge. Directed graphs of relations show the direction of each pair.', '(1, 2) does not imply (2, 1).', ['Draw one arrow from 1 to 2.'], 'undirected_error')
    E(7, 'cp2', 'Congruence mod 3 on {0, ..., 8}. Find [1].', 'Morgan', ['[1] = {1}'],
      '{1, 4, 7}', 'Morgan listed only the element itself. The class contains everything related to 1.', '[a] = {b | a R b}.', ['1, 4, 7 leave remainder 1.'], 'class_singleton_error')
    E(6, 'cp1', 'Is "x ≤ y" on ℝ an equivalence relation?', 'Taylor', ['It is reflexive and transitive, so yes.'],
      'No; it is not symmetric (1 ≤ 2 but 2 ≰ 1)', 'Taylor skipped symmetry. All three properties are required.', 'Check every property.', ['Counterexample to symmetry: (1, 2).'], 'skip_symmetry_error')
    E(3, 'cp1', 'R = ∅ on A = {1, 2}. Which properties hold?', 'Jamie', ['R is empty, so it has no properties.'],
      'Symmetric and transitive (vacuously), but not reflexive', 'Jamie missed vacuous truth. With no pairs, the conditions for symmetry and transitivity are never violated.', 'Reflexive fails because (1, 1) is missing.', ['Symmetric: no (a, b) to check. Transitive: no chains.'], 'vacuous_relation_error')
    E(4, 'cp1', 'R on ℝ: x R y ⟺ |x − y| < 1. Is R transitive?', 'Quinn', ['0 R 0.5 and 0.5 R 0.9 and 0 R 0.9. It works, so yes.'],
      'No; 0 R 0.6 and 0.6 R 1.2 but not 0 R 1.2', 'Quinn checked one example. A property of an infinite relation needs a proof; one counterexample disproves it.', 'Examples do not prove transitivity.', ['|0 − 1.2| = 1.2 ≥ 1.'], 'example_property_error')
    E(5, 'cp1', 'How many pairs are in the relation induced by {{1, 2, 3}, {4}}?', 'Alex', ['Block {1, 2, 3} gives 3 pairs, block {4} gives 1 pair: 4.'],
      '10', 'Alex counted elements instead of ordered pairs. A block of size k gives k² pairs.', 'Include (x, x) and both orders.', ['3² + 1² = 10.'], 'block_pairs_error')
    E(1, 'cp1', 'A = {1, 2, 3}, R: a R b ⟺ a + b = 4. List R.', 'Jordan', ['R = {(1, 3), (2, 2)}'],
      '{(1, 3), (2, 2), (3, 1)}', 'Jordan listed each sum once. Ordered pairs (1, 3) and (3, 1) are different.', 'Check every ordered pair in A × A.', ['3 + 1 = 4 too.'], 'missing_order_error')
    E(7, 'cp1', 'Mod 4 on ℤ: how many distinct classes?', 'Sam', ['Infinitely many, since [0], [1], [2], ... are all classes.'],
      '4', 'Sam did not notice repeated classes: [4] = [0], [5] = [1], and so on.', 'Distinct classes correspond to remainders 0, 1, 2, 3.', ['[n] = [n mod 4].'], 'repeat_class_error')
    E(6, 'honors', 'Prove "symmetric and transitive implies reflexive": a R b ⇒ b R a ⇒ a R a.', 'Riley', ['Take any a, choose b with a R b; then b R a, so a R a. Therefore R is reflexive.'],
      'False claim; R = {(1, 1)} on {1, 2} is symmetric and transitive but not reflexive', 'Riley assumed every a is related to some b. An element related to nothing never gets a loop.', 'The argument fails for isolated elements.', ['2 has no partner, so (2, 2) is never forced.'], 'isolated_element_error')
    E(3, 'honors', 'R on ℤ: a R b ⟺ a − b is odd. Is R transitive?', 'Casey', ['If a − b and b − c are odd, then a − c = (a − b) + (b − c) is odd + odd, which is odd.'],
      'No; odd + odd is even (e.g. 1 R 2, 2 R 3, but 1 − 3 = −2 is even)', 'Casey claimed odd + odd is odd.', 'Parity arithmetic: odd + odd = even.', ['Counterexample a = 1, b = 2, c = 3.'], 'parity_sum_error')
    E(7, 'honors', 'x R y ⟺ x² = y² on ℤ. Find [−3].', 'Avery', ['[−3] = {−3}'],
      '{−3, 3}', 'Avery forgot 3² = (−3)².', 'The class contains every y with y² = 9.', ['y = ±3.'], 'class_square_error')
    E(4, 'honors', 'How many symmetric relations are on a 2-element set {a, b}?', 'Morgan', ['A × A has 4 pairs, so 2⁴ = 16.'],
      '8', 'Morgan counted all relations. In a symmetric relation, (a, b) and (b, a) must be chosen together.', 'Free choices: (a, a), (b, b), and the pair {(a, b), (b, a)}: 2³.', ['2³ = 8.'], 'count_symmetric_error')
    E(5, 'honors', 'Is {{n ∈ ℤ | n > 0}, {n ∈ ℤ | n < 0}} a partition of ℤ?', 'Taylor', ['Yes, positives and negatives do not overlap.'],
      'No; 0 is in neither block', 'Taylor checked disjointness but not coverage.', 'Every element must be in some block.', ['Add {0} as a third block.'], 'coverage_error')
    E(2, 'honors', 'Digraph: arrows 1→2, 2→3, 1→3, 3→1 (no loops). Is the relation transitive?', 'Jamie', ['1→2→3 has shortcut 1→3. So it is transitive.'],
      'No; 1→3→1 requires the loop 1→1 (also 3→1→2 requires 3→2)', 'Jamie checked only one two-step path.', 'Check every two-step path, including ones that return to the start.', ['(1, 3), (3, 1) ∈ R but (1, 1) ∉ R.'], 'path_check_error')
