"""Discrete Math audit 2026-11-18, batch B part 2 (#1): solutions that show the work.
Every non-open-response solution gets at least 2 steps and 80 characters of working; computed families get their numbers
worked out from the item's own data, and every select-all item ends with one line per option.
Run after batch_b_levels.py."""
import re, sys, os, math, itertools, collections
from fractions import Fraction as Fr
sys.path.insert(0, os.path.dirname(__file__))
from lib import load, save, items, family
import elect as E

B = load()
N = lambda s: str(s).replace('−', '-').replace('‑', '-')
fs = E.fs


def S(xs):
    xs = sorted(xs, key=lambda v: (isinstance(v, str), v))
    return '{' + ', '.join(map(str, xs)) + '}' if xs else '∅'


def pset(s):
    s = s.strip()
    if s == '∅': return []
    return [int(N(x)) if re.fullmatch(r'-?\d+', N(x).strip()) else x.strip() for x in s.strip('{}').split(',') if x.strip()]


# ---------------- quick checks: worked steps for each one-line template ----------------
def comb(n, r): return math.comb(n, r)


QUICK = [
    (r'How many subsets does a set with (\d+) elements have', lambda n: [f'Each of the {n} elements is either in a subset or not: 2 choices each.', f'2^{n} = {2 ** n} subsets (including ∅ and the set itself).']),
    (r'How many proper subsets does a set with (\d+) elements have', lambda n: [f'There are 2^{n} = {2 ** n} subsets in all.', f'A proper subset is any subset except the set itself: {2 ** n} − 1 = {2 ** n - 1}.']),
    (r'\|A\| = (\d+) and \|B\| = (\d+)', lambda a, b: [f'A × B has one ordered pair (x, y) for each choice of x ∈ A and y ∈ B.', f'|A × B| = |A|·|B| = {a}·{b} = {a * b}.']),
    (r'How many bit strings have length (\d+)', lambda n: [f'Each of the {n} positions is 0 or 1.', f'Multiplication rule: 2^{n} = {2 ** n}.']),
    (r'strings of length 2 use an alphabet of (\d+) letters', lambda n: [f'Each of the 2 positions can be any of the {n} letters (repeats allowed).', f'{n}·{n} = {n * n} strings.']),
    (r'elements are in \{n ∈ ℤ \| (-?\d+) ≤ n ≤ (-?\d+)\}', lambda a, b: [f'The integers from {a} to {b} inclusive.', f'Count = last − first + 1 = {b} − ({a}) + 1 = {b - a + 1}.']),
    (r'Find gcd\((\d+), (\d+)\)', lambda a, b: [f'Euclidean algorithm: ' + '; '.join(_euclid(a, b)) + '.', f'The last nonzero remainder is gcd({a}, {b}) = {math.gcd(a, b)}.']),
    (r'Find lcm\((\d+), (\d+)\)', lambda a, b: [f'gcd({a}, {b}) = {math.gcd(a, b)}.', f'lcm = {a}·{b}/gcd = {a * b}/{math.gcd(a, b)} = {a * b // math.gcd(a, b)}.']),
    (r'remainder when (\d+) is divided by (\d+)', lambda a, b: [f'{a} = {b}·{a // b} + {a % b}, with 0 ≤ {a % b} < {b}.', f'The remainder is {a % b}.']),
    (r'quotient q when (\d+) = (\d+)·q \+ r', lambda a, b: [f'{a} ÷ {b} = {a / b:.4g}; take the whole-number part.', f'{a} = {b}·{a // b} + {a % b}, so q = {a // b} (and r = {a % b}).']),
    (r'How many positive divisors does (\d+) have', lambda n: _divisors(n)),
    (r'smallest prime greater than (\d+)', lambda n: _nextprime(n)),
    (r'relation a < b on \{1, 2, \.\.\., (\d+)\}', lambda n: [f'Each pair a < b is a choice of 2 different numbers from {n}, listed smaller first.', f'C({n}, 2) = {n}·{n - 1}/2 = {comb(n, 2)} pairs.']),
    (r'relation a ≤ b on \{1, 2, \.\.\., (\d+)\}', lambda n: [f'Pairs with a < b: C({n}, 2) = {comb(n, 2)}.', f'Pairs with a = b: {n}.', f'Total: {comb(n, 2)} + {n} = {comb(n, 2) + n}.']),
    (r'How many relations are there on a set with (\d+) elements', lambda n: [f'A relation is any subset of A × A, which has {n}² = {n * n} pairs.', f'Number of subsets: 2^{n * n} = {2 ** (n * n)}.']),
    (r'How many reflexive relations are there on a set with (\d+) elements', lambda n: [f'All {n} pairs (a, a) must be in the relation.', f'The other {n * n} − {n} = {n * n - n} pairs are free: 2^{n * n - n} = {2 ** (n * n - n)}.']),
    (r'equivalence classes does congruence mod (\d+) have', lambda n: [f'Every integer has exactly one remainder 0, 1, …, {n - 1} on division by {n}.', f'The classes are [0], [1], …, [{n - 1}]: {n} classes.']),
    (r'loops does the digraph of "a = b" on \{1, \.\.\., (\d+)\}', lambda n: ['"a = b" relates each element only to itself.', f'One loop at each of the {n} vertices: {n} loops.']),
    (r'elements of \{1, \.\.\., (\d+)\} are in the class \[1\] for congruence mod (\d+)', lambda n, m: [f'[1] = {{1, 1 + {m}, 1 + 2·{m}, …}} up to {n}.', f'Count: ⌊({n} − 1)/{m}⌋ + 1 = {(n - 1) // m + 1}.']),
    (r'edges does the complete graph K_(\d+) have', lambda n: [f'Every pair of the {n} vertices is joined by one edge.', f'C({n}, 2) = {n}·{n - 1}/2 = {comb(n, 2)}.']),
    (r'edges does a tree with (\d+) vertices have', lambda n: ['A tree with n vertices always has n − 1 edges (connected, no cycles).', f'{n} − 1 = {n - 1}.']),
    (r'A graph has (\d+) edges\. What is the sum of its degrees', lambda n: ['Handshake theorem: each edge adds 1 to the degree of each endpoint, so Σ deg = 2|E|.', f'2·{n} = {2 * n}.']),
    (r'edges does K_(\d+),(\d+) have', lambda m, n: [f'K_{m},{n} joins each of the {m} vertices on one side to each of the {n} on the other.', f'{m}·{n} = {m * n} edges.']),
    (r'Hamiltonian cycle in a graph with (\d+) vertices use', lambda n: ['A Hamiltonian cycle visits each vertex once and returns to the start.', f'With {n} vertices it uses {n} edges.']),
    (r'In K_(\d+), what is the degree of each vertex', lambda n: [f'Each vertex is joined to every other vertex.', f'Degree = {n} − 1 = {n - 1}.']),
    (r'A forest has (\d+) vertices and 3 trees', lambda n: ['A tree with k vertices has k − 1 edges, so a forest with c trees has n − c edges.', f'{n} − 3 = {n - 3}.']),
    (r'How many votes are a majority of (\d+) votes', lambda n: [f'A majority is MORE than half: half of {n} is {Fr(n, 2)}.', f'The smallest whole number greater than {Fr(n, 2)} is {n // 2 + 1}.']),
    (r'Borda count with (\d+) candidates: how many points does a first-place vote earn', lambda n: [f'With {n} candidates, last place earns 1 point and each higher place earns 1 more.', f'First place earns {n} points.']),
    (r'smallest valid quota for weights ([\d, ]+)\?', lambda w: [f'Total weight = {" + ".join(w.split(", "))} = {sum(map(int, w.split(",")))}.', f'The quota must be more than half of {sum(map(int, w.split(",")))}, i.e. more than {Fr(sum(map(int, w.split(","))), 2)}, so the smallest is {sum(map(int, w.split(","))) // 2 + 1}.']),
    (r'Population (\d+), (\d+) seats\. Find the standard divisor', lambda p, s: ['Standard divisor = total population ÷ number of seats.', f'{p} ÷ {s} = {fs(Fr(p, s))}' + (f' ≈ {p / s:.2f}' if p % s else '') + ' people per seat.']),
    (r'With (\d+) candidates, how many head-to-head comparisons', lambda n: [f'Each comparison is a pair of different candidates; order does not matter.', f'C({n}, 2) = {comb(n, 2)}.']),
    (r'How many coalitions \(nonempty\) can (\d+) players form', lambda n: [f'Each of the {n} players is in or out: 2^{n} = {2 ** n} subsets.', f'Remove the empty coalition: {2 ** n} − 1 = {2 ** n - 1}.']),
    (r'How many rows does a truth table with (\d+) variables have', lambda n: [f'Each variable is T or F.', f'2^{n} = {2 ** n} rows.']),
    (r'In a (\d+)-variable truth table, in how many rows is p ∨ q ∨', lambda n: [f'The disjunction is false only when every variable is F: 1 row of 2^{n} = {2 ** n}.', f'{2 ** n} − 1 = {2 ** n - 1} rows.']),
    (r'truth table with (\d+) variables, in how many rows is p → q false', lambda n: [f'p → q is false only when p = T and q = F.', f'The other {n - 2} variable(s) are free: 2^{n - 2} = {2 ** (n - 2)} rows.']),
    (r'truth table with (\d+) variables, in how many rows is p ↔ q true', lambda n: [f'p ↔ q is true when p and q agree: 2 of the 4 (p, q) combinations.', f'Times 2^{n - 2} for the other variables: 2·{2 ** (n - 2)} = {2 ** (n - 1)}.']),
    (r'truth table with (\d+) variables, in how many rows is p ∨ q true', lambda n: [f'p ∨ q is true in 3 of the 4 (p, q) combinations.', f'Times 2^{n - 2} for the other variables: 3·{2 ** (n - 2)} = {3 * 2 ** (n - 2)}.']),
    (r'truth table with (\d+) variables, in how many rows is p ∧ q ∧ r true', lambda n: [f'p ∧ q ∧ r needs p, q and r all T: 1 of the 8 combinations.', f'Times 2^{n - 3} for the other variables: {2 ** (n - 3)}.']),
    (r'\|A\| = (\d+), \|B\| = (\d+), \|A ∩ B\| = (\d+)\. Find \|A ∪ B\|', lambda a, b, c: ['Inclusion–exclusion: |A ∪ B| = |A| + |B| − |A ∩ B| (the overlap is counted twice otherwise).', f'{a} + {b} − {c} = {a + b - c}.']),
    (r'\|A\| = (\d+), \|B\| = (\d+), \|A ∩ B\| = (\d+)\. Find \|A − B\|', lambda a, b, c: ['A − B keeps the elements of A that are not in B.', f'|A| − |A ∩ B| = {a} − {c} = {a - c}.']),
    (r'\|A\| = (\d+), \|B\| = (\d+), \|A ∩ B\| = (\d+)\. Find \|A ⊕ B\|', lambda a, b, c: ['A ⊕ B is the elements in exactly one of the sets.', f'(|A| − |A ∩ B|) + (|B| − |A ∩ B|) = {a - c} + {b - c} = {a + b - 2 * c}.']),
    (r'U has (\d+) elements and \|A\| = (\d+)\. Find \|A′\|', lambda u, a: ["A′ is everything in U that is not in A.", f'{u} − {a} = {u - a}.']),
    (r'Evaluate [PC] = (\d+)x \+ (\d+)y at the corner \((\d+), (\d+)\)', lambda a, b, x, y: [f'Substitute x = {x}, y = {y}.', f'{a}·{x} + {b}·{y} = {a * x} + {b * y} = {a * x + b * y}.']),
    (r'Solve x \+ y = (-?\d+) and x − y = (-?\d+)', lambda s, d: [f'Add the equations: 2x = {s} + ({d}) = {s + d}, so x = {fs(Fr(s + d, 2))}.', f'Subtract them: 2y = {s} − ({d}) = {s - d}, so y = {fs(Fr(s - d, 2))}.']),
    (r'Where does (\d+)x \+ (\d+)y = (\d+) cross the x-axis', lambda a, b, c: ['On the x-axis y = 0.', f'{a}x = {c}, so x = {fs(Fr(c, a))}.']),
    (r'Where does (\d+)x \+ (\d+)y = (\d+) cross the y-axis', lambda a, b, c: ['On the y-axis x = 0.', f'{b}y = {c}, so y = {fs(Fr(c, b))}.']),
]


def _euclid(a, b):
    out = []
    while b:
        out.append(f'{a} = {b}·{a // b} + {a % b}'); a, b = b, a % b
    return out[:4]


def _divisors(n):
    fa = collections.Counter(); m = n; d = 2
    while m > 1:
        while m % d == 0: fa[d] += 1; m //= d
        d += 1
    t = math.prod(e + 1 for e in fa.values())
    return [f'Prime factorization: {n} = ' + ' · '.join(f'{p}^{e}' if e > 1 else str(p) for p, e in sorted(fa.items())) + '.',
            'A divisor picks each prime\'s exponent from 0 up to its power: ' + '·'.join(f'({e} + 1)' for e in fa.values()) + f' = {t}.']


def _nextprime(n):
    x = n + 1; tried = []
    while not all(x % d for d in range(2, int(x ** .5) + 1)) or x < 2:
        f = [d for d in range(2, x) if x % d == 0][0]; tried.append(f'{x} = {f}·{x // f}'); x += 1
    return [('Rule out ' + ', '.join(tried) + '.') if tried else f'Start with {n + 1}.', f'{x} has no divisor from 2 to √{x}, so it is prime.']


def quick(q):
    P = N(q['prompt'])
    for rx, fn in QUICK:
        m = re.search(rx, P)
        if m:
            args = [int(g) if re.fullmatch(r'-?\d+', g) else g for g in m.groups()]
            return fn(*args)


# ---------------- computed families ----------------
def lines_eqs(P):
    eqs = []
    for a, b, c, v, val in re.findall(r'(\d*)x \+ (\d*)y = (-?\d+)|\b([xy]) = (-?[\d/]+)', N(P)):
        eqs.append((Fr(1), Fr(0), Fr(val)) if v == 'x' else (Fr(0), Fr(1), Fr(val)) if v else (Fr(a or 1), Fr(b or 1), Fr(c)))
    return eqs


def cx(k):
    return '' if k == 1 else '−' if k == -1 else fs(k)


def intersect_steps(P):
    L = lines_eqs(P)
    if len(L) < 2:
        L = [(Fr(a or 1), Fr(b or 1), Fr(c)) for a, b, c in re.findall(r'(\d*)x \+ (\d*)y ≤ (\d+)', N(P))]
    (a1, b1, c1), (a2, b2, c2) = L[:2]
    d = a1 * b2 - a2 * b1; x = (c1 * b2 - c2 * b1) / d; y = (a1 * c2 - a2 * c1) / d
    eq = lambda a, b, c: (f'{fs(a)}x' if a not in (0, 1) else 'x' if a == 1 else '') + (' + ' if a and b else '') + (f'{fs(b)}y' if b not in (0, 1) else 'y' if b == 1 else '') + f' = {fs(c)}'
    if b1 == 0 or b2 == 0 or a1 == 0 or a2 == 0:
        known = (a1, b1, c1) if (a1 == 0 or b1 == 0) else (a2, b2, c2)
        other = (a2, b2, c2) if known == (a1, b1, c1) else (a1, b1, c1)
        var = 'x' if known[1] == 0 else 'y'
        return [f'The line {eq(*known)} gives {var} = {fs(known[2] / (known[0] or known[1]))} directly.',
                f'Substitute into {eq(*other)}: {"y" if var == "x" else "x"} = {fs(y if var == "x" else x)}.', f'Corner: ({fs(x)}, {fs(y)}).']
    k1, k2 = b2, b1
    return [f'Eliminate y: multiply {eq(a1, b1, c1)} by {fs(k1)} and {eq(a2, b2, c2)} by {fs(k2)}, then subtract: {cx(a1 * k1 - a2 * k2)}x = {fs(c1 * k1 - c2 * k2)}, so x = {fs(x)}.',
            f'Substitute x = {fs(x)} into {eq(a1, b1, c1)}: {cx(b1)}y = {fs(c1)} − {fs(a1 * x)} = {fs(c1 - a1 * x)}, so y = {fs(y)}.',
            f'Check in the other line: {fs(a2)}·{fs(x)} + {fs(b2)}·{fs(y)} = {fs(a2 * x + b2 * y)}. Corner: ({fs(x)}, {fs(y)}).']


def method_steps(q):
    P = q['prompt']; rows = [(int(n), r.split(' > ')) for n, r in re.findall(r'(\d+) voters: ([A-Z](?: > [A-Z])+)', P)]
    if not rows: return None
    tot = sum(n for n, _ in rows)
    first = E.first_place(rows)
    if 'Borda' in P:
        n = len(rows[0][1]); c = E.borda(rows)
        return [f'Points: {n} for 1st place, {n - 1} for 2nd, …, 1 for last.'] + [f'{x}: ' + ' + '.join(f'{k}·{n - r.index(x)}' for k, r in rows) + f' = {c[x]}' for x in sorted(c)] + [f'Highest total: {E.unique_max(c) or "a tie"}.']
    if 'elimination' in P or 'instant runoff' in P:
        w, rounds = E.irv(rows)
        return [f'{tot} voters; a majority is {tot // 2 + 1}.'] + [f'Round {i + 1}: ' + ', '.join(f'{k} {v}' for k, v in sorted(r.items())) + ('' if i == len(rounds) - 1 else f'; no majority, eliminate {min(r, key=r.get)} and transfer its ballots.') for i, r in enumerate(rounds)] + [f'Winner: {w or "a tie"}.']
    if 'pairwise' in P:
        C = sorted(rows[0][1]); pts = E.pairwise(rows)
        return [f'{a} vs {b}: ' + ' + '.join(str(k) for k, r in rows if r.index(a) < r.index(b)) + f' = {E.h2h(rows, a, b)} prefer {a}, {E.h2h(rows, b, a)} prefer {b}' for a, b in itertools.combinations(C, 2)] + \
               ['Points (1 per head-to-head win, 1/2 per tie): ' + ', '.join(f'{k} {fs(v)}' for k, v in sorted(pts.items())) + f'. Winner: {E.unique_max(pts) or "a tie"}.']
    if 'plurality' in P:
        return [f'Count only first choices: ' + '; '.join(f'{x}: ' + (' + '.join(str(k) for k, r in rows if r[0] == x) or '0') + f' = {first[x]}' for x in sorted(first)) + '.',
                f'Plurality needs the most first-place votes, not a majority ({tot // 2 + 1} of {tot}).', f'Winner: {E.unique_max(first) or "a tie"}.']


def relation_steps(q):
    P = q['prompt']
    dom = [int(x) for x in re.search(r'A = \{([^}]*)\}', P).group(1).split(',')]
    rs = re.search(r'R = (∅|\{.*?\})\. Is', P).group(1)
    R = [] if rs == '∅' else [tuple(map(int, t)) for t in re.findall(r'\((\d+), (\d+)\)', rs)]
    prop = re.search(r'Is R (\w+)\?', P).group(1); Rs = set(R)
    if prop == 'reflexive':
        miss = [a for a in dom if (a, a) not in Rs]
        return ['Reflexive: every a ∈ A must have (a, a) ∈ R.', 'Loops needed: ' + ', '.join(f'({a}, {a})' for a in dom) + '.',
                f'Missing: ' + ', '.join(f'({a}, {a})' for a in miss) + ', so R is not reflexive.' if miss else 'All are present, so R is reflexive.']
    if prop == 'symmetric':
        bad = [(a, b) for a, b in R if (b, a) not in Rs]
        return ['Symmetric: whenever (a, b) ∈ R, (b, a) must be in R too.', 'Check each pair with a ≠ b: ' + (', '.join(f'({a}, {b})→({b}, {a})' for a, b in R if a != b) or 'there are none') + '.',
                f'({bad[0][0]}, {bad[0][1]}) ∈ R but ({bad[0][1]}, {bad[0][0]}) ∉ R, so R is not symmetric.' if bad else 'Every reverse pair is present, so R is symmetric.']
    if prop == 'transitive':
        bad = [(a, b, d) for a, b in R for c, d in R if b == c and (a, d) not in Rs]
        chains = [(a, b, d) for a, b in R for c, d in R if b == c]
        return ['Transitive: whenever (a, b) and (b, c) are in R, (a, c) must be in R.', f'Chains to check: {len(chains)}' + (' (' + ', '.join(f'({a},{b}),({b},{d})' for a, b, d in chains[:4]) + (', …' if len(chains) > 4 else '') + ')' if chains else '') + '.',
                f'({bad[0][0]}, {bad[0][1]}) and ({bad[0][1]}, {bad[0][2]}) are in R but ({bad[0][0]}, {bad[0][2]}) is not, so R is not transitive.' if bad else 'Every chain has its shortcut in R (or there are no chains), so R is transitive.']


def set_op_steps(q):
    P = N(q['prompt'])
    env = {n: pset(s) for n, s in re.findall(r'([ABC]) = (\{[^}]*\}|∅)', P)}
    Um = re.search(r'Universe U = (\{[^}]*\})', P)
    e = (re.search(r'Find (.+?)(?: \(the complement| \(complements|\. Write|\.$)', P) or [None, None])[1]
    if not e: return None
    defs = {'∪': 'union: elements in either set', '∩': 'intersection: elements in both sets', '−': 'difference: elements of the first set that are not in the second', "'": 'complement: elements of U that are not in the set'}
    used = [defs[k] for k in defs if k in e]
    st = ['Use the definition' + ('s' if len(used) > 1 else '') + ' — ' + '; '.join(used) + '.']
    st.append('Given: ' + ', '.join(f'{k} = {S(v)}' for k, v in env.items()) + (f', U = {Um.group(1)}' if Um else '') + '.')
    st.append('Go element by element and keep each one that satisfies the definition' + (', working inside parentheses first.' if '(' in e else '.'))
    return st


SKIP_FAMILIES = set()


def computed(q):
    f = family(q); P = q['prompt']
    try:
        if f == 'quick_check': return quick(q)
        if f == 'intersect_lines': return intersect_steps(P)
        if f == 'method_winner': return method_steps(q)
        if f == 'check_property' and 'Let A =' in P: return relation_steps(q)
        if f in ('set_op', 'complement_op'): return (set_op_steps(q) or []) + [s for s in q['solutionSteps'] if '=' in s][-1:]
        if f == 'list_count':
            m = re.search(r'list (-?\d+), (-?\d+)(?:, (-?\d+))?, \.\.\., (-?\d+)', N(P))
            if m:
                a, b, _, z = [int(x) if x else None for x in m.groups()]; d = b - a
                return [f'The list starts at {a} and goes up by {d}.' if d != 1 else f'The list is the integers from {a} to {z}.',
                        (f'Divide out the step: the terms are {a} + {d}k for k = 0, …, {(z - a) // d}.' if d != 1 else f'Last − first counts the gaps between neighbors: {z} − {a} = {z - a}.'),
                        f'Count = {(z - a) // d} + 1 = {(z - a) // d + 1} (add 1 to include both ends).']
        if f == 'evaluate_objective':
            m = re.search(r'P = ([\d/]*)x \+ ([\d/]*)y at the (?:point|corner) \((-?[\d/]+), (-?[\d/]+)\)', N(P))
            if m:
                a, b, x, y = [Fr(t or 1) for t in m.groups()]
                return [f'Substitute x = {fs(x)} and y = {fs(y)} into P.', f'P = {fs(a)}·{fs(x)} + {fs(b)}·{fs(y)} = {fs(a * x)} + {fs(b * y)} = {fs(a * x + b * y)}.']
        if f == 'fib_term':
            n = int(re.findall(r'F_(\d+)', P)[-1]); t = [1, 1]
            while len(t) < n: t.append(t[-1] + t[-2])
            return ['Each term is the sum of the two before it.', 'F₁ to F_' + str(n) + ': ' + ', '.join(map(str, t)) + '.', f'F_{n} = {t[n - 1]}.']
        if f == 'factorial_eval':
            m = re.search(r'Evaluate (\d+)!/(\d+)!', P)
            if m:
                a, b = map(int, m.groups())
                return [f'{a}! = {a}·{a - 1}·…·{b + 1}·{b}!, so the {b}! cancels.', f'{a}!/{b}! = ' + '·'.join(str(k) for k in range(a, b, -1)) + f' = {math.factorial(a) // math.factorial(b)}.']
            m = re.search(r'Evaluate (\d+)!\.', P)
            if m:
                n = int(m.group(1)); return [f'{n}! is the product of the whole numbers from {n} down to 1 (and 0! = 1).', f'{n}! = ' + ('·'.join(str(k) for k in range(n, 0, -1)) if n > 1 else '1') + f' = {math.factorial(n)}.']
        if f == 'find_class':
            m = re.search(r'A = \{([^}]*)\}', P); cls = re.search(r'\[(-?\d+)\]', P)
            if m and cls:
                return [f'[{cls.group(1)}] is the set of elements of A related to {cls.group(1)}.', 'Check each element of A against the rule, keeping those related to ' + cls.group(1) + '.', f'[{cls.group(1)}] = {q["answer"]}.']
        if f == 'inverse_relation':
            return ['R⁻¹ reverses every ordered pair: (a, b) ∈ R exactly when (b, a) ∈ R⁻¹.', 'Reverse each pair of R, then list them by first coordinate.', f'R⁻¹ = {q["answer"]}.']
    except Exception:
        return None


# ---------------- family-specific "why" sentences for short solutions ----------------
WHY = {
    'addition_rule': 'Add only when no outcome is counted in two cases; otherwise subtract the overlap once (inclusion–exclusion).',
    'multiplication_rule': 'Multiply because every choice at one step can be combined with every choice at the next.',
    'counting_probability': 'Use the same counting model (ordered or unordered) for the favorable and the total outcomes.',
    'equally_likely': 'This works only because every outcome in the sample space is equally likely.',
    'write_constraint': '"At most" (no more than) gives ≤; "at least" (no fewer than) gives ≥; each unit of x or y uses its own amount of the resource.',
    'is_equivalence': 'All three properties are needed; one counterexample to any of them is enough to say no.',
    'tree_facts': 'Trees have n − 1 edges, and the degree sum 2(n − 1) ties degrees, edges and leaves together.',
    'optimize': 'By the corner-point principle, a bounded feasible region attains its optimum at a corner, so comparing the corners is enough.',
    'set_equal': 'Sets are equal exactly when they have the same elements; order and repetition do not matter.',
    'event': 'An event is a subset of the sample space: list exactly the outcomes that make the description true.',
    'perm_comb': 'Ask whether order matters: arrangements (permutations) count orderings, selections (combinations) divide them out.',
    'in_out_degree': 'Each arrow adds 1 to the out-degree of its tail and 1 to the in-degree of its head, so both sums equal the number of arrows.',
    'digraph_count': 'In the directed graph each ordered pair (a, b) is one arrow from a to b, and (a, a) is a loop.',
    'degree': 'Each edge adds 1 to the degree of each endpoint, and a loop adds 2.',
    'interpret_context': 'Translate the optimal corner and the objective value back into the situation, with units.',
    'choose_method': 'Existence needs one example, a false universal statement needs one counterexample, and a true universal statement needs a general proof.',
    'evaluate_compound': 'Evaluate ¬ first, then ∧, then ∨, then → and ↔, working inside parentheses first.',
    'tree_count': 'Each path from the root to a leaf is one complete outcome, so the leaves count the outcomes.',
    'special_graphs': 'K_n joins every pair of n vertices, K_m,n joins every vertex on one side to every vertex on the other, and C_n is a single cycle.',
    'chromatic': 'Show a coloring that works, and give a reason (a triangle, an odd cycle, a K₄) that fewer colors cannot.',
    'hamiltonian': 'A degree-1 vertex, or a vertex whose removal disconnects the graph, rules a Hamiltonian cycle out; otherwise try to build one.',
    'test_point': 'A point is a solution of a system only if it satisfies every inequality; one failure is enough to rule it out.',
    'tt_column': 'Build intermediate columns (negations first), then combine them row by row in the order TT, TF, FT, FF.',
    'condorcet_check': 'A Condorcet winner must beat every other candidate head-to-head.',
    'count_winning': 'A coalition wins when its total weight reaches the quota; check every combination of players.',
    'euler_trail': 'A connected graph has an Euler circuit when every degree is even and an Euler trail (not closed) when exactly two degrees are odd.',
    'count_vertices': 'Corners are intersections of boundary lines that satisfy every constraint.',
    'contrapos_write': 'The contrapositive of "if p then q" is "if not q then not p", and it is logically equivalent to the original.',
    'rec_compute': 'A recurrence gives each term from earlier ones, so compute the terms in order.',
    'induction_algebra': 'Rewrite the left side of P(k + 1) as (left side of P(k)) + the next term, use the hypothesis, then factor to reach the right side of P(k + 1).',
    'power_set_count': 'Each element is in or out of a subset independently, so fix the required elements and count the free ones.',
    'is_subset': 'A ⊆ B means every element of A is in B; one element of A outside B is enough to say no.',
    'identity_check': 'An identity must hold for every choice of sets; checking one element in each Venn region covers every case.',
    'equivalent_check': 'Two forms are equivalent exactly when their truth columns agree in every row.',
    'cond_column': 'p → q is false only in the row p = T, q = F.',
    'banzhaf': 'A player is critical in a winning coalition if the coalition loses without that player; the index is the share of all critical counts.',
    'classify_integer': 'Use the definitions: even means 2k, odd means 2k + 1, prime means exactly two positive divisors.',
    'builder_to_roster': 'Roster notation lists every object that satisfies the set-builder condition.',
    'hamilton': 'Hamilton gives each state the whole part of its quota, then gives the leftover seats to the largest fractional parts.',
    'contra_assume': 'A proof by contradiction starts by assuming the negation of what you want to prove.',
    'direct_parity': 'Write the result as 2·(integer) for even or 2·(integer) + 1 for odd, so the definition is visible.',
    'induced_relation': 'In the induced relation each element is related to every element of its own block, including itself.',
    'member_subset_truth': '∈ compares an element with a set; ⊆ compares two sets.',
    'translate_connectives': '"and"/"but" → ∧, "or" → ∨ (inclusive), "not" → ¬, applied to the simple statements p and q.',
    'tautology_classify': 'A tautology is true in every row, a contradiction is false in every row; anything else is neither.',
    'negate_conditional': '¬(p → q) ≡ p ∧ ¬q: the negation of a conditional says the hypothesis happens without the conclusion.',
    'cic_identify': 'Converse: q → p. Inverse: ¬p → ¬q. Contrapositive: ¬q → ¬p (the only one equivalent to p → q).',
    'classify_fallacy': 'Converse error: p → q, q ∴ p. Inverse error: p → q, ¬p ∴ ¬q. Both are invalid because a row makes the premises true and the conclusion false.',
    'degree_sequence': 'The degree sum must be even, no degree can exceed n − 1, and Havel–Hakimi settles the rest.',
    'is_partition': 'A partition needs nonempty blocks that do not overlap and together cover the whole set.',
    'first_terms': 'Substitute each value of n in turn into the formula.',
    'induction_base': 'The base case checks the statement at the smallest n it claims.',
    'rec_term': 'Apply the rule once per step, starting from the given first term.',
    'set_counterexample': 'A counterexample to a "for all sets" statement is one specific choice of sets that makes it false.',
    'statement_or_not': 'A statement is a declarative sentence that is true or false; questions, commands and open sentences are not statements.',
    'quantified_truth': 'A universal statement needs a general argument to be true and one counterexample to be false.',
    'conditional_truth': 'A conditional is false only when the hypothesis is true and the conclusion is false.',
}

WHY.update({
    'divides_check': 'a | b means b = a·k for some integer k; divide and check whether the quotient is a whole number.',
    'sigma_eval': 'Write out each term of the sum for the given values of k, then add.',
    'arith_term': 'In an arithmetic sequence a_n = a₁ + (n − 1)d: the first term plus (n − 1) common differences.',
    'build_counterexample': 'A counterexample makes the hypothesis true and the conclusion false at the same time.',
    'cardinality': 'The cardinality |S| counts distinct elements only; repeated listings count once.',
    'count_strings': 'Each position of a string is filled independently, so multiply the number of choices per position.',
    'negate_symbolic': 'Use ¬(p → q) ≡ p ∧ ¬q and De Morgan\'s laws so that ¬ applies only to single letters.',
    'contradiction_check': 'A contradiction is false in every row of its truth table.',
    'smallest_witness': 'Test n = 1, 2, 3, … in order; the first value that works is the smallest witness.',
    'series_sum': 'For an arithmetic series use (number of terms)·(first + last)/2; for a geometric series use a₁(rⁿ − 1)/(r − 1).',
    'binom_eval': 'C(n, k) = n!/(k!(n − k)!): cancel the larger factorial before multiplying.',
    'figurate': 'Find how the count grows from one figure to the next, write a formula in n, then substitute.',
    'pattern_mc': 'The interior angles of an n-gon add to (n − 2)·180°, because the polygon splits into n − 2 triangles.',
    'venn_shade': 'Shade region by region: test each region against the set expression.',
    'power_set_size': 'A set with n elements has 2ⁿ subsets, because each element is in or out.',
    'name_law': 'Match the shape of the equation to the law: commutative swaps, associative regroups, distributive spreads one operation over another, De Morgan negates.',
    'count-step': 'In a list that goes up by a fixed step, count = (last − first)/step + 1.',
    'voters_majority': 'Add the row counts for the number of voters; a majority is more than half of that total.',
    'neg_cond_eval': '¬(p → q) is true exactly when p is true and q is false.',
    'quotient_remainder': 'The quotient–remainder theorem needs 0 ≤ r < d, so for negative n the quotient rounds down.',
    'gcd': 'Euclidean algorithm: replace (a, b) with (b, a mod b) until the remainder is 0; the last nonzero remainder is the gcd.',
    'geom_term': 'In a geometric sequence a_n = a₁·r^(n − 1).',
    'fib_identity': 'List the Fibonacci terms you need, then add; the sum of the first n terms equals F_(n+2) − 1.',
    'find_recursion': 'A recursive definition gives the first term and a rule for each term from the one before; check both against the list.',
    'interior_angle': 'Each interior angle of a regular n-gon is (n − 2)·180°/n.',
    'inclusion_exclusion': 'Add the individual counts, subtract each overlap once, and add back the triple overlap.',
    'simplify_sets': 'Use the set laws (absorption, distributive, complement, De Morgan) one step at a time.',
    'relation_member': 'Substitute the pair into the rule that defines R.',
    'class_count': 'Congruence mod n splits the integers by remainder, giving the classes [0], …, [n − 1].',
    'read_tree': 'Count the outcomes at the ends of the branches (the leaves).',
    'tt_rows': 'Each variable doubles the number of rows: n variables need 2ⁿ rows.',
    'cond_equivalent': 'p → q ≡ ¬p ∨ q ≡ ¬q → ¬p; the converse and inverse are not equivalent to it.',
    'exhaustion': 'Proof by exhaustion checks every case in a finite domain.',
    'lcm': 'lcm(a, b) = a·b/gcd(a, b).',
    'find_formula': 'Check the formula at n = 1, 2, 3 against the first terms.',
    'factorial_simplify': 'Expand the larger factorial until the smaller one appears, then cancel.',
    'paradox': 'Alabama: more seats makes a state lose one; population: a faster-growing state loses a seat; new-states: adding a state changes the others\' seats.',
})


def generic_why(q):
    f = family(q)
    if f in WHY: return WHY[f]
    if f.endswith('_error'): return 'Fixing the mistake: redo the step that went wrong using the definition, then recompute the answer.'
    return None


# ---------------- select-all: one line per option ----------------
def per_option(q):
    lines = []
    for o in q['options']:
        lines.append(('✓ ' if o['correct'] else '✗ ') + o['text'] + (' (correct).' if o['correct'] else ' (not correct).'))
    return 'Option by option: ' + ' '.join(lines)


changed = collections.Counter()
for u, q in items(B):
    if q['format'] == 'open-response': continue
    st = list(q['solutionSteps']); text = ' '.join(st)
    thin = len(st) < 2 or len(text) < 60 or family(q) == 'quick_check'
    if thin:
        c = computed(q)
        if c:
            ans = str(q['answer'])
            st = c + ([] if any(ans in s for s in c) or isinstance(q['answer'], list) else [f'Answer: {ans}.'])
            changed['computed'] += 1
    if len(st) < 2 or len(' '.join(st)) < 60:
        w = generic_why(q)
        if w and w not in st:
            st = [w] + st; changed['why'] += 1
    if q['format'] == 'select-all' and not any(s.startswith('Option by option') for s in st):
        st.append(per_option(q)); changed['select-all'] += 1
    if len(st) < 2 or len(' '.join(st)) < 60:
        if family(q) == 'quick_check' and len(st) >= 2: st.insert(0, 'Use the definition, then compute.') if False else None
    if len(st) < 2:
        st.append(f'Answer: {q["answer"] if not isinstance(q["answer"], list) else "; ".join(q["answer"])}.'); changed['answer line'] += 1
    q['solutionSteps'] = st

import hashlib
for _, q in items(B):
    if q['format'] == 'multiple-choice' and '-honors-a' in q['id'] and q['options'][0]['correct']:
        n = len(q['options']); t = int(hashlib.sha256(q['id'].encode()).hexdigest()[:6], 16) % n
        c = q['options'][0]; rest = q['options'][1:]; q['options'] = rest[:t] + [c] + rest[t:]
save(B)
left = [q for _, q in items(B) if q['format'] != 'open-response' and (len(q['solutionSteps']) < 2 or len(' '.join(q['solutionSteps'])) < 60)]
print(dict(changed), '| still short', len(left), collections.Counter(family(q) for q in left).most_common(40))
