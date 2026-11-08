"""Short "quick check" items: one-line prompts (≤ 110 characters) with short numeric answers, so every unit and level has enough
distinct short answers for the Tarsia, maze and whodunnit printables. All answers are computed."""
import math, itertools
from fractions import Fraction
from core import seeded, frac

C = math.comb


def tarsia_ok(q):
    return q['format'] in ('short-answer', 'multiple-choice') and isinstance(q['answer'], (str, int)) and len(str(q['answer'])) <= 20 and \
        len(q['prompt']) <= 110 and '\n' not in q['prompt'] and 'diagram' not in q and '_error)' not in q['sourceNotes']


def gen(unit, L, i):
    """Return (skill, prompt, answer, steps) for the i-th quick item of a unit/level; numbers vary with i and level."""
    k = {'cp2': 0, 'cp1': 1, 'honors': 2}[L]
    r = seeded(unit, L, i)
    if unit == 'speaking-mathematically':
        n = 3 + (i // 6) % 10 + k
        opts = [
            (5, 'How many subsets does a set with %d elements have?' % n, 2 ** n, ['2^%d.' % n]),
            (6, 'If |A| = %d and |B| = %d, find |A × B|.' % (n, n + 2 + k), n * (n + 2 + k), ['%d · %d.' % (n, n + 2 + k)]),
            (7, 'How many bit strings have length %d?' % n, 2 ** n, ['Two choices per position.']),
            (7, 'How many strings of length 2 use an alphabet of %d letters (repeats allowed)?' % (n + 3), (n + 3) ** 2, ['%d².' % (n + 3)]),
            (5, 'How many proper subsets does a set with %d elements have?' % n, 2 ** n - 1, ['2^%d − 1.' % n]),
            (4, 'How many elements are in {n ∈ ℤ | %d ≤ n ≤ %d}?' % (-n, n + k), 2 * n + k + 1, ['Count the integers from %d to %d.' % (-n, n + k)]),
        ]
    elif unit == 'number-theory-proof':
        a, c = r.randint(2, 15) * (2 + k), r.randint(2, 15) * (2 + k)
        n = r.randint(20, 400)
        d = 2 + (i % 7)
        opts = [
            (5, 'Find gcd(%d, %d).' % (a, c), math.gcd(a, c), ['Euclidean algorithm.']),
            (5, 'Find lcm(%d, %d).' % (a, c), a * c // math.gcd(a, c), ['ab / gcd(a, b).']),
            (4, 'Find the remainder when %d is divided by %d.' % (n, d), n % d, ['%d = %d·%d + %d.' % (n, d, n // d, n % d)]),
            (4, 'Find the quotient q when %d = %d·q + r with 0 ≤ r < %d.' % (n, d, d), n // d, ['%d = %d·%d + %d.' % (n, d, n // d, n % d)]),
            (5, 'How many positive divisors does %d have?' % n, sum(1 for x in range(1, n + 1) if n % x == 0), ['Count the divisors.']),
            (1, 'What is the smallest prime greater than %d?' % n, next(m for m in range(n + 1, 2 * n + 3) if all(m % x for x in range(2, int(m ** .5) + 1))), ['Test successive integers.']),
        ]
    elif unit == 'properties-relations':
        n = 3 + (i // 7) % 9 + k
        m = 1 + (i // 7) % 5
        opts = [
            (4, 'How many ordered pairs are in the relation a < b on {1, 2, ..., %d}?' % n, C(n, 2), ['C(%d, 2).' % n]),
            (4, 'How many ordered pairs are in the relation a ≤ b on {1, 2, ..., %d}?' % n, C(n, 2) + n, ['C(%d, 2) + %d.' % (n, n)]),
            (4, 'How many relations are there on a set with %d elements?' % m, 2 ** (m * m), ['2^(%d²).' % m]),
            (4, 'How many reflexive relations are there on a set with %d elements?' % m, 2 ** (m * m - m), ['Loops forced; the other pairs are free.']),
            (7, 'How many equivalence classes does congruence mod %d have on ℤ?' % (n + 2), n + 2, ['One class per remainder.']),
            (2, 'How many loops does the digraph of "a = b" on {1, ..., %d} have?' % (n + 5), n + 5, ['One loop per element.']),
            (7, 'How many elements of {1, ..., %d} are in the class [1] for congruence mod %d?' % (6 * n, n), 6, ['1, 1 + %d, ..., six of them.' % n]),
        ]
    elif unit == 'graphs-trees':
        n = 4 + (i // 8) % 9 + 2 * k
        opts = [
            (3, 'How many edges does the complete graph K_%d have?' % n, C(n, 2), ['C(%d, 2).' % n]),
            (7, 'How many edges does a tree with %d vertices have?' % (n + 3), n + 2, ['n − 1.']),
            (1, 'A graph has %d edges. What is the sum of its degrees?' % (n + 7), 2 * (n + 7), ['Handshake theorem.']),
            (3, 'How many edges does K_%d,%d have?' % (n - 2, n), (n - 2) * n, ['mn.']),
            (6, 'How many edges does a Hamiltonian cycle in a graph with %d vertices use?' % (n + 1), n + 1, ['One edge per vertex.']),
            (1, 'In K_%d, what is the degree of each vertex?' % (n + 4), n + 3, ['n − 1.']),
            (7, 'A forest has %d vertices and 3 trees. How many edges?' % (n + 10), n + 7, ['n − (number of trees).']),
        ]
    elif unit == 'election-theory':
        N = 15 + 3 * i + 10 * k
        w = [5 + (i % 4), 3 + k, 2]
        opts = [
            (1, 'How many votes are a majority of %d votes?' % N, N // 2 + 1, ['More than half.']),
            (2, 'Borda count with %d candidates: how many points does a first-place vote earn?' % (3 + i % 5), 3 + i % 5, ['n points for first.']),
            (4, 'What is the smallest valid quota for weights %s?' % ', '.join(map(str, w + [i + 1])), sum(w + [i + 1]) // 2 + 1, ['More than half of the total.']),
            (7, 'Population %d, %d seats. Find the standard divisor.' % (N * 100, N // 5 + 2), frac(Fraction(N * 100, N // 5 + 2)), ['Population ÷ seats.']),
            (2, 'With %d candidates, how many head-to-head comparisons are there?' % (3 + i % 6), C(3 + i % 6, 2), ['C(n, 2).']),
            (5, 'How many coalitions (nonempty) can %d players form?' % (3 + i % 4), 2 ** (3 + i % 4) - 1, ['2ⁿ − 1.']),
        ]
    elif unit == 'compound-statements-logic':
        n = 2 + (i // 6) % 8 + k % 2
        opts = [
            (1, 'How many rows does a truth table with %d variables have?' % n, 2 ** n, ['2^%d.' % n]),
            (2, 'In a %d-variable truth table, in how many rows is p ∨ q ∨ ... (all %d variables) true?' % (n, n), 2 ** n - 1, ['Only the all-false row fails.']),
            (2, 'In a truth table with %d variables, in how many rows is p → q false?' % (n + 1), 2 ** (n - 1), ['Only when p is T and q is F; the other variables are free.']),
            (2, 'In a truth table with %d variables, in how many rows is p ↔ q true?' % (n + 1), 2 ** n, ['Half of the rows.']),
            (2, 'In a truth table with %d variables, in how many rows is p ∨ q true?' % (n + 1), 3 * 2 ** (n - 1), ['Three of every four rows.']),
            (2, 'In a truth table with %d variables, in how many rows is p ∧ q ∧ r true?' % (n + 2), 2 ** (n - 1), ['p, q, r fixed; the rest free.']),
        ]
    elif unit == 'set-theory':
        a, c = 10 + 3 * i + 5 * k, 6 + 2 * i + k
        both = 2 + (i % 5)
        U = a + c + 12 + i
        opts = [
            (3, '|A| = %d, |B| = %d, |A ∩ B| = %d. Find |A ∪ B|.' % (a, c, both), a + c - both, ['Inclusion-exclusion.']),
            (3, 'U has %d elements and |A| = %d. Find |A′|.' % (U, a), U - a, ['|U| − |A|.']),
            (5, 'How many subsets does a set with %d elements have?' % (2 + (i % 9)), 2 ** (2 + (i % 9)), ['2ⁿ.']),
            (3, '|A| = %d, |B| = %d, |A ∩ B| = %d. Find |A − B|.' % (a, c, both), a - both, ['|A| − |A ∩ B|.']),
            (3, '|A| = %d, |B| = %d, |A ∩ B| = %d. Find |A ⊕ B|.' % (a, c, both), a + c - 2 * both, ['|A ∪ B| − |A ∩ B|.']),
            (6, '|A| = %d and |B| = %d. Find |A × B|.' % (2 + i % 7, 3 + k + i % 5), (2 + i % 7) * (3 + k + i % 5), ['Multiply.']),
        ]
    elif unit == 'linear-programming':
        x, y = 1 + (i % 7), 2 + (i % 5) + k
        pa, pb = 3 + (i % 6) + k, 2 + (i % 4)
        opts = [
            (4, 'Evaluate P = %dx + %dy at the corner (%d, %d).' % (pa, pb, x, y), pa * x + pb * y, ['Substitute.']),
            (3, 'Solve x + y = %d and x − y = %d. Give the corner as (x, y).' % (x + y, x - y), '(%d, %d)' % (x, y), ['Add the equations.']),
            (2, 'Where does %dx + %dy = %d cross the x-axis? Give x.' % (pb, pa, pb * pa * x), pa * x, ['Set y = 0.']),
            (4, 'Evaluate C = %dx + %dy at the corner (%d, %d).' % (pb + 4, pa + 1, y, x), (pb + 4) * y + (pa + 1) * x, ['Substitute.']),
            (2, 'Where does %dx + %dy = %d cross the y-axis? Give y.' % (pa, pb, pa * pb * y), pa * y, ['Set x = 0.']),
        ]
    else:
        return None
    sk, p, a, steps = opts[i % len(opts)]
    return sk, p, a, steps


def add_quick(b, target=32):
    for L in ('cp2', 'cp1', 'honors'):
        have = {str(q['answer']) for q in b.q if q['level'] == L and tarsia_ok(q)}
        prompts = {q['prompt'] for q in b.q}
        i = 0
        while len(have) < target and i < 400:
            g = gen(b.unit, L, i)
            i += 1
            if g is None:
                return
            sk, p, a, steps = g
            if str(a) in have or p in prompts or len(p) > 110:
                continue
            if i % 2:
                b.sa(sk, L, p, a, steps + ['Answer: %s' % a], 'quick_check')
            else:
                b.mc(sk, L, p, str(a), [], steps + ['Answer: %s' % a], 'quick_check', order='sort') if str(a).lstrip('-').isdigit() else b.sa(sk, L, p, a, steps + ['Answer: %s' % a], 'quick_check')
            have.add(str(a)); prompts.add(p)
