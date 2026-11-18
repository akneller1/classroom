"""Discrete Math audit 2026-11-18, batch B part 1 (#2 and #4).
#2 At most 4 one-line quick checks per skill and level; the rest are removed.
#4 Advanced items that reuse a Support template (new numbers only) move to Standard, and 64 new multi-step Advanced items
   (4 to 6 in each of the 16 skills that would otherwise fall below 8 Advanced items) take their place.
Run after batch_a.py."""
import re, random, itertools, math, sys, os, collections
from fractions import Fraction as Fr
sys.path.insert(0, os.path.dirname(__file__))
from lib import load, save, items, family
import elect as E

B = load()
NOTE = 'Original Claude-authored Discrete Math item (family: {}). Discrete Math audit 2026-11-18 (tools/discrete-audit-20261118): multi-step Advanced item; answer computed by the script.'
rng = random.Random(4)

# ---------------- #4 Advanced clones of Support templates move to Standard ----------------
def tmpl(s):
    s = re.sub(r'\{[^}]*\}', '{S}', s); s = re.sub(r'\[[^\]]*\]', '[W]', s)
    s = re.sub(r'\b(Kim|Lee|Ann|Ben|Ana|Bo|Cy|Sam|Jordan|Riley|Casey|Avery|Morgan|Taylor|Jamie|Quinn|Alex)\b', 'Nm', s)
    s = re.sub(r'[A-Z](?: > [A-Z])+', 'R', s)
    return re.sub(r'\d+(\.\d+)?', '#', s)


moved = 0
ids = {q['id'] for _, q in items(B)}
for u, d in B.items():
    cp2 = collections.defaultdict(set)
    for q in d['questions']:
        if q['level'] == 'cp2': cp2[q['skillId']].add(tmpl(q['prompt']))
    for q in d['questions']:
        if q['level'] == 'honors' and tmpl(q['prompt']) in cp2[q['skillId']]:
            q['level'] = 'cp1'
            new = q['id'].replace('-honors-', '-cp1-h')
            assert new not in ids; ids.add(new); q['id'] = new
            q['sourceNotes'] += ' Moved from Advanced to Standard by the Discrete Math audit 2026-11-18 (same template as a Support item).'
            moved += 1


# ---------------- #2 cap quick checks ----------------
removed = 0
for u, d in B.items():
    seen = collections.Counter(); keep = []
    for q in sorted(d['questions'], key=lambda q: q['id']):
        if family(q) == 'quick_check':
            k = (q['skillId'], q['level']); seen[k] += 1
            if seen[k] > 4:
                removed += 1; continue
        keep.append(q)
    order = {q['id']: i for i, q in enumerate(d['questions'])}
    d['questions'] = sorted(keep, key=lambda q: order[q['id']])

# ---------------- new multi-step Advanced items ----------------
def item(skill, fam, fmt, prompt, answer, steps, std, options=None):
    unit = skill.rsplit('-skill-', 1)[0]
    code = {'speaking-mathematically': 'sm', 'compound-statements-logic': 'lg', 'number-theory-proof': 'np', 'sequences-induction-recursion': 'sq',
            'set-theory': 'st', 'properties-relations': 'rl', 'counting-probability': 'cn', 'graphs-trees': 'gr', 'election-theory': 'el', 'linear-programming': 'lp'}[unit]
    s = int(skill.rsplit('-', 1)[1])
    k = 1
    while f'dm-{code}-s{s:02d}-honors-a{k:02d}' in ids: k += 1
    q = {'id': f'dm-{code}-s{s:02d}-honors-a{k:02d}', 'skillId': skill, 'level': 'honors', 'format': fmt, 'prompt': prompt, 'answer': answer,
         'solutionSteps': steps, 'sourceNotes': NOTE.format(fam), 'standards': std}
    if options is not None:
        opts = [{'text': answer, 'correct': True}] + [{'text': o, 'correct': False} for o in options if o != answer]
        seen = set(); q['options'] = [o for o in opts if not (o['text'] in seen or seen.add(o['text']))][:4]
        assert len(q['options']) == 4, (prompt, q['options'])
    ids.add(q['id'])
    B[unit]['questions'].append(q)
    return q


def std_of(skill):
    for _, q in items(B):
        if q['skillId'] == skill: return list(q['standards'])


def names(S): return ', '.join(f'P{i + 1}' for i in S)


# election-theory-skill-04: smallest quota giving P1 veto power
sk = 'election-theory-skill-04'
for w in ([9, 6, 4, 2], [10, 7, 5, 3], [8, 7, 6, 2], [12, 5, 4, 4], [7, 6, 3, 3], [11, 9, 4, 1]):
    T = sum(w); half = T // 2 + 1; others = T - w[0]; q0 = max(half, others + 1)
    item(sk, 'veto_quota', 'short-answer',
         f'Weights {", ".join(map(str, w))} (players P1, P2, …). A valid quota is more than half the total weight and at most the total. What is the smallest valid quota for which P1 has veto power?',
         str(q0), [f'Total weight = {T}, so a valid quota is at least {half} and at most {T}.',
                   f'P1 has veto power exactly when the other players together fall short of the quota: {" + ".join(map(str, w[1:]))} = {others} < q.',
                   f'So q ≥ {others + 1}; combined with q ≥ {half}, the smallest valid quota is {q0}.',
                   f'Check: in [{q0}: {", ".join(map(str, w))}] the others total {others} < {q0}, and with q = {q0 - 1} ' + ('they would reach it.' if q0 - 1 >= half and others >= q0 - 1 else 'the quota would not be valid.')],
         std_of(sk))

# number-theory-proof-skill-05: count integers divisible by a but not b, and gcd·lcm identity
sk = 'number-theory-proof-skill-05'
for (N, a, b) in ((500, 6, 4), (1000, 12, 18), (600, 8, 6), (900, 15, 10), (2026, 14, 21)):
    l = a * b // math.gcd(a, b); x, y = N // a, N // l
    item(sk, 'divisible_not', 'short-answer', f'How many integers from 1 to {N} are divisible by {a} but NOT by {b}?', str(x - y),
         [f'Multiples of {a} up to {N}: ⌊{N}/{a}⌋ = {x}.',
          f'A multiple of {a} that is also a multiple of {b} is a multiple of lcm({a}, {b}) = {a}·{b}/gcd({a}, {b}) = {a * b}/{math.gcd(a, b)} = {l}.',
          f'Multiples of {l} up to {N}: ⌊{N}/{l}⌋ = {y}.', f'Divisible by {a} but not {b}: {x} − {y} = {x - y}.'], std_of(sk))

# properties-relations-skill-03: transitive closure size
sk = 'properties-relations-skill-03'
for R in ([(1, 2), (2, 3), (3, 4)], [(1, 2), (2, 1), (3, 1)], [(1, 3), (3, 2), (2, 4), (4, 1)], [(2, 1), (3, 2), (4, 3), (1, 4)]):
    C = set(R)
    while True:
        add = {(a, d) for a, b in C for c, d in C if b == c} - C
        if not add: break
        C |= add
    fmtR = '{' + ', '.join(f'({a}, {b})' for a, b in R) + '}'
    added = sorted(C - set(R))
    item(sk, 'transitive_closure', 'short-answer',
         f'Let A = {{1, 2, 3, 4}} and R = {fmtR}. What is the smallest number of ordered pairs you must ADD so that R becomes transitive?', str(len(added)),
         ['Repeatedly look for chains a R b, b R c with (a, c) missing, and add (a, c).',
          'New pairs can create new chains, so keep going until no chain is missing its shortcut.',
          'Pairs added: ' + ', '.join(f'({a}, {b})' for a, b in added) + '.' if added else 'No pairs are needed.',
          f'The transitive closure has {len(C)} pairs, so {len(added)} pairs were added.'], std_of(sk))

# counting-probability-skill-02: integers in a range divisible by a but not by b (fencepost + exclusion)
sk = 'counting-probability-skill-02'
for (lo, hi, a, b) in ((100, 999, 7, 5), (250, 750, 6, 4), (1000, 2026, 9, 6), (45, 450, 12, 8)):
    m = lambda d: hi // d - (lo - 1) // d
    l = a * b // math.gcd(a, b)
    item(sk, 'range_multiples_not', 'short-answer', f'How many integers from {lo} to {hi}, inclusive, are multiples of {a} but not multiples of {b}?', str(m(a) - m(l)),
         [f'Multiples of {a} from {lo} to {hi}: ⌊{hi}/{a}⌋ − ⌊{lo - 1}/{a}⌋ = {hi // a} − {(lo - 1) // a} = {m(a)}.',
          f'Those that are also multiples of {b} are the multiples of lcm({a}, {b}) = {l}: ⌊{hi}/{l}⌋ − ⌊{lo - 1}/{l}⌋ = {m(l)}.',
          f'Subtract: {m(a)} − {m(l)} = {m(a) - m(l)}.'], std_of(sk))

# election-theory-skill-01: minimum first-place votes for a plurality winner
sk = 'election-theory-skill-01'
for n, k in ((25, 4), (40, 3), (61, 5), (100, 6)):
    v = math.ceil((n + k - 1) / k)
    item(sk, 'min_plurality', 'short-answer',
         f'{n} voters choose among {k} candidates, and each voter casts one first-place vote. What is the smallest number of first-place votes a candidate can have and still be the UNIQUE plurality winner?', str(v),
         [f'If the winner has v votes, each of the other {k - 1} candidates has at most v − 1.',
          f'So the total is at most v + {k - 1}(v − 1) = {k}v − {k - 1}, and it must reach {n}: {k}v − {k - 1} ≥ {n}.',
          f'v ≥ ({n} + {k - 1})/{k} = {Fr(n + k - 1, k)}, so v = {v}.',
          f'Check: {v} + ' + ' + '.join(str(x) for x in ([v - 1] * (k - 1))) + f' = {v + (k - 1) * (v - 1)} ≥ {n}, and the extra votes can be removed from the others; {v - 1} votes would not be enough.'],
         std_of(sk))

# number-theory-proof-skill-01: smallest counterexample to a prime-generating conjecture
sk = 'number-theory-proof-skill-01'
def isp(n): return n > 1 and all(n % d for d in range(2, int(n ** .5) + 1))
for a, b, desc in ((1, 41, 'n² + n + 41'), (1, 17, 'n² + n + 17'), (-1, 41, 'n² − n + 41'), (1, 11, 'n² + n + 11')):
    n = 0
    while isp(n * n + a * n + b): n += 1
    v = n * n + a * n + b
    f = [p for p in range(2, v) if v % p == 0][0]
    item(sk, 'prime_poly_counterexample', 'short-answer', f'Conjecture: "{desc} is prime for every integer n ≥ 0." Find the smallest counterexample n.', str(n),
         [f'Test n = 0, 1, 2, … in order; every value below n = {n} gives a prime.',
          f'At n = {n}: {desc} = {v} = {f}·{v // f}, which is composite.',
          'One counterexample is enough to disprove a universal statement, however many cases worked before it.'], std_of(sk))

# properties-relations-skill-02: digraph of a rule
sk = 'properties-relations-skill-02'
for n, d in ((8, 3), (10, 2), (12, 4), (9, 5)):
    arcs = [(a, b) for a in range(1, n + 1) for b in range(1, n + 1) if a < b <= a + d]
    item(sk, 'digraph_rule_count', 'short-answer', f'R on {{1, 2, …, {n}}}: a R b if and only if a < b ≤ a + {d}. How many arrows does the directed graph of R have?', str(len(arcs)),
         [f'From vertex a there is an arrow to each of a + 1, …, a + {d} that is at most {n}.',
          f'Vertices 1 to {n - d} each have {d} arrows: {n - d}·{d} = {(n - d) * d}.',
          'The last vertices have fewer: ' + ' + '.join(str(n - a) for a in range(n - d + 1, n + 1)) + f' = {sum(n - a for a in range(n - d + 1, n + 1))}.',
          f'Total: {len(arcs)} arrows (no loops, since a < b).'], std_of(sk))

# election-theory-skill-05: full Banzhaf distribution
sk = 'election-theory-skill-05'
for qq, w in ((13, [8, 6, 4, 2]), (11, [7, 5, 3, 2]), (15, [9, 7, 5, 1]), (10, [6, 5, 3, 3])):
    c = E.critical_counts(qq, w); T = sum(c); ans = ', '.join(E.fs(Fr(x, T)) for x in c)
    W = E.coalitions(qq, w)
    item(sk, 'banzhaf_all', 'short-answer', f'Find the Banzhaf power distribution of [{qq}: {", ".join(map(str, w))}]. Give the indices of P1, P2, P3, P4 in order, as fractions in lowest terms separated by commas.', ans,
         [f'Winning coalitions (total ≥ {qq}): ' + '; '.join(E.name(S) for S in W) + '.',
          'In each, a player is critical if the coalition loses without it: ' + '; '.join(E.name(S) + ' → ' + (names([i for i in S if sum(w[j] for j in S) - w[i] < qq]) or 'none') for S in W) + '.',
          'Critical counts: ' + ', '.join(f'P{i + 1} {x}' for i, x in enumerate(c)) + f'; total {T}.', f'Indices: {ans}.'], std_of(sk))

# properties-relations-skill-06: equivalence relations with k classes (Stirling numbers)
sk = 'properties-relations-skill-06'
def stir(n, k): return 1 if n == k else 0 if k == 0 or k > n else k * stir(n - 1, k) + stir(n - 1, k - 1)
for n, k in ((4, 2), (5, 2), (5, 3), (4, 3)):
    item(sk, 'count_equivalences', 'short-answer', f'How many different equivalence relations on {{1, 2, …, {n}}} have exactly {k} equivalence classes?', str(stir(n, k)),
         ['Equivalence relations on a set match its partitions: the classes are the blocks.',
          f'So count the partitions of a {n}-element set into {k} nonempty blocks, S({n}, {k}).',
          f'Use S(n, k) = k·S(n − 1, k) + S(n − 1, k − 1): element {n} joins one of the {k} blocks of a partition of the rest, or forms its own block.',
          f'S({n}, {k}) = {k}·{stir(n - 1, k)} + {stir(n - 1, k - 1)} = {stir(n, k)}.'], std_of(sk))

# set-theory-skill-01: set-builder with a quadratic inequality, to roster or ∅
sk = 'set-theory-skill-01'
for r1, r2, strict in ((-2, 3, False), (1, 5, True), (-4, -1, False), (2, 3, True)):
    b, c = -(r1 + r2), r1 * r2
    rel = '<' if strict else '≤'
    els = [x for x in range(r1 - 2, r2 + 3) if (x * x + b * x + c < 0 if strict else x * x + b * x + c <= 0)]
    co = lambda k: '' if k == 1 else str(k)
    poly = 'n²' + (f' − {co(-b)}n' if b < 0 else f' + {co(b)}n' if b > 0 else '') + (f' + {c}' if c > 0 else f' − {-c}' if c < 0 else '')
    ans = '{' + ', '.join(str(x).replace('-', '−') for x in els) + '}' if els else '∅'
    item(sk, 'builder_quadratic', 'short-answer', f'Write {{n ∈ ℤ | {poly} {rel} 0}} in roster notation (or ∅ if it is empty).', ans.replace('−', '-'),
         [f'Factor: {poly} = (n − ({r1}))(n − ({r2})).'.replace('− (-', '+ (').replace('(n + (', '(n + ').replace('− (', '− ').replace('))', ')'),
          f'The product is {"negative" if strict else "at most 0"} only between the roots {r1} and {r2}{" (excluding them)" if strict else " (including them)"}.',
          'The integers in that interval: ' + (', '.join(map(str, els)) if els else 'none') + '.', f'So the set is {ans.replace("−", "-")}.'], std_of(sk))

# counting-probability-skill-04: three-set inclusion–exclusion
sk = 'counting-probability-skill-04'
for N, (a, b, c) in ((300, (2, 3, 5)), (1000, (3, 5, 7)), (500, (4, 6, 9)), (720, (2, 5, 9))):
    L = lambda *xs: math.lcm(*xs)
    s1 = N // a + N // b + N // c; s2 = N // L(a, b) + N // L(a, c) + N // L(b, c); s3 = N // L(a, b, c)
    item(sk, 'inclusion_exclusion3', 'short-answer', f'How many integers from 1 to {N} are divisible by {a}, {b} or {c}?', str(s1 - s2 + s3),
         [f'Single sets: ⌊{N}/{a}⌋ + ⌊{N}/{b}⌋ + ⌊{N}/{c}⌋ = {N // a} + {N // b} + {N // c} = {s1}.',
          f'Pairs (lcm {L(a, b)}, {L(a, c)}, {L(b, c)}): {N // L(a, b)} + {N // L(a, c)} + {N // L(b, c)} = {s2}.',
          f'All three (lcm {L(a, b, c)}): {s3}.', f'Inclusion–exclusion: {s1} − {s2} + {s3} = {s1 - s2 + s3}.'], std_of(sk))

# counting-probability-skill-05: digit strings with conditions (brute force)
sk = 'counting-probability-skill-05'
for desc, test, how in (
        ('4-digit even numbers with all digits different', lambda s: s[0] != '0' and int(s[-1]) % 2 == 0 and len(set(s)) == 4, 'Split on the last digit: if it is 0, the first three places have 9·8·7 = 504 choices; if it is 2, 4, 6 or 8 (4 ways), the first digit cannot be 0 or the last digit (8 ways) and the middle two have 8·7: 4·8·8·7 = 1792.'),
        ('4-digit numbers with all digits different that are multiples of 5', lambda s: s[0] != '0' and s[-1] in '05' and len(set(s)) == 4, 'Last digit 0: 9·8·7 = 504. Last digit 5: the first digit cannot be 0 or 5 (8 ways), then 8·7: 8·8·7 = 448.'),
        ('3-digit numbers whose digits are all different and all odd', lambda s: len(set(s)) == 3 and all(int(x) % 2 for x in s), 'Only the 5 odd digits are allowed and none can repeat: 5·4·3.'),
        ('4-digit numbers that contain at least one 7', lambda s: s[0] != '0' and '7' in s, 'Complement: 4-digit numbers with no 7 have 8·9·9·9 = 5832 choices; subtract from 9000.')):
    dg = 3 if '3-digit' in desc else 4
    n = sum(1 for k in range(10 ** (dg - 1), 10 ** dg) if test(str(k)))
    item(sk, 'digit_conditions', 'short-answer', f'How many {desc} are there?', str(n),
         ['Fill the most restricted positions first (the first digit cannot be 0; the last digit is limited by the condition).', how, f'Total: {n}.'], std_of(sk))

# election-theory-skill-02: four-candidate instant runoff
sk = 'election-theory-skill-02'
made = 0
while made < 4:
    rows = E.random_schedule(rng, 4, 5, 3, 14); w, rounds = E.irv(rows)
    if not w or len(rounds) < 3 or E.unique_max(E.first_place(rows)) in (None, w): continue
    tot = sum(n for n, _ in rows)
    item(sk, 'irv_four', 'short-answer', 'Preference schedule:\n' + E.fmt_schedule(rows) + '\nWho wins by plurality with elimination (instant runoff)? Answer with the letter.', w,
         [f'{tot} voters, so a majority is {tot // 2 + 1}.'] +
         [f'Round {i + 1}: ' + ', '.join(f'{k} {v}' for k, v in sorted(r.items())) + ('' if i == len(rounds) - 1 else f' → no majority; eliminate {min(r, key=r.get)} and move its ballots to their next choice.') for i, r in enumerate(rounds)] +
         [f'{w} wins with a majority; note that the plurality leader {E.unique_max(E.first_place(rows))} does not.'], std_of(sk))
    made += 1

# election-theory-skill-03: does plurality violate the Condorcet criterion?
sk = 'election-theory-skill-03'
made = 0
while made < 4:
    rows = E.random_schedule(rng, 3 + made % 2, 4, 2, 15); c = E.condorcet(rows); p = E.unique_max(E.first_place(rows))
    if not c or not p or (made % 2 == 0) != (c != p): continue
    ans = 'Yes' if c != p else 'No'
    item(sk, 'condorcet_violation', 'multiple-choice', 'Preference schedule:\n' + E.fmt_schedule(rows) + '\nDoes the plurality method violate the Condorcet criterion in this election?',
         ans + (f': {c} beats every rival head-to-head but {p} wins plurality' if ans == 'Yes' else f': {c} is both the Condorcet and the plurality winner'),
         [f'Plurality: ' + ', '.join(f'{k} {v}' for k, v in sorted(E.first_place(rows).items())) + f', so {p} wins.',
          'Head-to-head: ' + '; '.join(f'{a} vs {b} {E.h2h(rows, a, b)}–{E.h2h(rows, b, a)}' for a, b in itertools.combinations(sorted(rows[0][1]), 2)) + '.',
          f'{c} beats every other candidate, so {c} is the Condorcet winner.',
          'The criterion is violated only when a Condorcet winner exists and the method picks someone else.'],
         std_of(sk), options=['Yes' + (f': {c} beats every rival head-to-head but {p} wins plurality' if ans == 'No' else f': {c} is both the Condorcet and the plurality winner'),
                              'No: plurality always satisfies the Condorcet criterion', 'It cannot be decided without the Borda count', 'Yes: there is no Condorcet winner'])
    made += 1

# set-theory-skill-02: three-set expressions
sk = 'set-theory-skill-02'
U = list(range(1, 13))
for expr in ('(A − B) ∪ (B ∩ C)', '(A ∪ C) − (A ∩ B)', 'A − (B ∪ C)', '(A ∩ B) ∪ (C − A)'):
    A = sorted(rng.sample(U, 6)); Bs = sorted(rng.sample(U, 6)); Cs = sorted(rng.sample(U, 5))
    env = {'A': set(A), 'B': set(Bs), 'C': set(Cs)}
    py = expr.replace('−', '-').replace('∪', '|').replace('∩', '&')
    val = sorted(eval(py, {}, env))
    inner = re.search(r'\(([^()]+)\)', expr).group(1)
    iv = sorted(eval(inner.replace('−', '-').replace('∪', '|').replace('∩', '&'), {}, env))
    S = lambda xs: '{' + ', '.join(map(str, xs)) + '}' if xs else '∅'
    item(sk, 'three_set_expr', 'short-answer', f'A = {S(A)}, B = {S(Bs)}, C = {S(Cs)}. Find {expr}. Write the set in roster notation, elements in increasing order (∅ if empty).', S(val),
         [f'Work inside the parentheses first: {inner} = {S(iv)}.', f'Then apply the remaining operation to get {expr} = {S(val)}.',
          '∪ keeps elements in either set, ∩ keeps elements in both, and − keeps elements of the first set that are not in the second.'], std_of(sk))

# set-theory-skill-06: subset relations between sets of multiples
sk = 'set-theory-skill-06'
for a, b in ((12, 4), (6, 4), (30, 10), (9, 6)):
    yes = a % b == 0
    item(sk, 'multiples_subset', 'multiple-choice', f'A = {{n ∈ ℤ | n is a multiple of {a}}} and B = {{n ∈ ℤ | n is a multiple of {b}}}. Is A ⊆ B?',
         f'Yes: if n = {a}k then n = {b}({a // b}k), so every element of A is in B' if yes else f'No: {a} ∈ A but {a} ∉ B because {b} does not divide {a}',
         ['To prove A ⊆ B, take an arbitrary element of A and show it is in B; to disprove it, find one element of A that is not in B.',
          (f'Let n ∈ A, so n = {a}k for some integer k. Then n = {b}·({a // b}k) and {a // b}k is an integer, so n ∈ B.' if yes else f'{a} is in A (k = 1), but {a}/{b} is not an integer, so {a} ∉ B.'),
          'So A ⊆ B.' if yes else 'One counterexample shows A ⊄ B.'], std_of(sk),
         options=[f'No: {a} ∈ A but {a} ∉ B because {b} does not divide {a}' if yes else f'Yes: if n = {a}k then n = {b}({Fr(a, b)}k), so every element of A is in B',
                  'Yes: both sets are infinite, so they are equal', f'No: B has more elements than A' if yes else f'Yes: {a} > {b}, so the multiples of {a} are among the multiples of {b}',
                  'It cannot be decided for infinite sets'])

save(B)
print('quick checks removed', removed, '| Advanced → Standard', moved, '| new Advanced items', sum(1 for _, q in items(B) if '-honors-a' in q['id']))
