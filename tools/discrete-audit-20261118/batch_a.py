"""Discrete Math audit 2026-11-18, batch A (Trivial/Small items).
#9 Relations on Finite and Infinite Sets uses infinite sets; #10 balanced MC answer positions; #12 fresh election data;
#13 no authoring notes or Python output in solutions; #14 money in dollars and cents; #15 template grammar;
#16 self-contained items; #17 LP binding-constraint item; #20 family tags on the 18 untagged list-count items.
Run once: python3 tools/discrete-audit-20261118/batch_a.py"""
import re, random, hashlib, itertools, sys, os, math
from fractions import Fraction as Fr
sys.path.insert(0, os.path.dirname(__file__))
from lib import load, save, items, family, set_family
import elect as E

B = load()
Q = {q['id']: q for _, q in items(B)}
NOTE = 'Discrete Math audit 2026-11-18 (tools/discrete-audit-20261118).'


def h(s):
    return int(hashlib.sha256(s.encode()).hexdigest()[:8], 16)


def opt(q, correct_text, distractors):
    """Rebuild MC options: correct first; positions are balanced at the end of the script."""
    seen, out = set(), []
    for t, c in [(correct_text, True)] + [(d, False) for d in distractors]:
        if t not in seen:
            seen.add(t); out.append({'text': t, 'correct': c})
    q['options'] = out[:4]
    q['answer'] = correct_text


# ---------------- #13 authoring notes and Python output ----------------
META = re.compile(r'^The other choices are near misses')
for q in Q.values():
    q['solutionSteps'] = [s for s in q['solutionSteps'] if not META.match(s)]
    q['solutionSteps'] = [re.sub(r"\{('[^']+': -?[\d/]+(?:, )?)+\}", lambda m: ', '.join(f'{a} {b}' for a, b in re.findall(r"'([^']+)': (-?[\d/]+)", m.group(0))), s)
                          for s in q['solutionSteps']]

# ---------------- #14 money in dollars and cents ----------------
def cents(x):
    x = Fr(x); v = round(x * 100) / 100
    s = f'{abs(v):.2f}'
    if s.endswith('.00'): s = s[:-3]
    return ('-' if v < 0 else '') + s


def money_text(t):
    return re.sub(r'(?<![\d/])(-?\d+)/(\d+)(?![\d/])', lambda m: cents(Fr(int(m.group(1)), int(m.group(2)))), t)


for q in Q.values():
    if family(q) != 'sealed_bids':
        continue
    frac = '/' in str(q['answer']) or any('/' in o['text'] for o in q.get('options', []))
    q['prompt'] = q['prompt'].replace(' (use a fraction a/b if needed)', ' (round to the nearest cent if needed)')
    if 'inherit one bike' in q['prompt'] and 'Answer in dollars.' in q['prompt']:
        q['prompt'] = q['prompt'].replace('Answer in dollars.', 'Answer in dollars and cents.')
    if not frac:
        continue
    if 'inherit one bike' in q['prompt']:
        a, b = map(int, re.search(r'bids \$(\d+), \w+ bids \$(\d+)', q['prompt']).groups())
        hi, lo = max(a, b), min(a, b); pay = Fr(lo, 2) + Fr(hi - lo, 4)
        opt(q, cents(pay), [cents(Fr(lo, 2)), cents(Fr(hi, 2)), cents(Fr(hi - lo, 2)), cents(pay + 1)])
        win, lose = ('Kim', 'Lee') if a > b else ('Lee', 'Kim')
        q['solutionSteps'] = [
            f'The higher bidder ({win}) gets the bike. Each heir\'s fair share is half of his or her own bid: {win} ${cents(Fr(hi, 2))}, {lose} ${cents(Fr(lo, 2))}.',
            f'{win} keeps a bike worth ${hi} to {win} but is entitled to only ${cents(Fr(hi, 2))}, so {win} first pays {lose} that fair share, ${cents(Fr(lo, 2))}.',
            f'Surplus = ${cents(Fr(hi, 2))} − ${cents(Fr(lo, 2))} = ${cents(Fr(hi - lo, 2))}; each heir gets half of it, ${cents(Fr(hi - lo, 4))}.',
            f'{win} pays {lose} ${cents(Fr(lo, 2))} + ${cents(Fr(hi - lo, 4))} = ${cents(pay)}.']
    else:
        q['answer'] = money_text(str(q['answer']))
        for o in q.get('options', []):
            o['text'] = money_text(o['text'])
        q['solutionSteps'] = [money_text(s) for s in q['solutionSteps']]
        q['solutionSteps'].append('Round only at the end: the exact amounts are thirds and ninths of a dollar.')

# ---------------- #15 template grammar ----------------
def gram(t):
    t = re.sub(r'\b1 hours\b', '1 hour', t)
    t = re.sub(r'\bwith 1 elements\b', 'with 1 element', t)
    t = re.sub(r'\b1 of the options appear\b', '1 of the options appears', t)
    t = re.sub(r'(?<![\d.,/\w])1([xy])\b', r'\1', t)
    t = re.sub(r'\{1, 2, \.\.\., ([1-3])\}', lambda m: '{' + ', '.join(str(i) for i in range(1, int(m.group(1)) + 1)) + '}', t)
    return t


for q in Q.values():
    q['prompt'] = gram(q['prompt'])
    if isinstance(q['answer'], str): q['answer'] = gram(q['answer'])
    elif isinstance(q['answer'], list): q['answer'] = [gram(a) for a in q['answer']]
    q['solutionSteps'] = [gram(s) for s in q['solutionSteps']]
    for o in q.get('options', []): o['text'] = gram(o['text'])
    for p in q.get('parts', []) or []:
        p['prompt'] = gram(p['prompt']); p['answer'] = gram(p['answer'])

# An LP distractor was "x + y ≤ 15" next to the key "1x + 1y ≤ 15": the same inequality, so two options were correct.
for o in Q['dm-lp-s01-honors-007']['options']:
    if not o['correct'] and o['text'] == 'x + y ≤ 15':
        o['text'] = 'x ≤ 15 and y ≤ 15'
Q['dm-lp-s01-honors-007']['solutionSteps'] = ['Machine hours used = (hours per unit of A)·x + (hours per unit of B)·y = 1·x + 1·y.',
    'Both products share the same 15 hours, so the total must be at most 15: x + y ≤ 15.',
    'Separate limits (x ≤ 15 and y ≤ 15) would allow 15 + 15 = 30 hours.']

# ---------------- #16 self-contained items ----------------
Q['dm-cn-s08-cp1-006']['prompt'] = 'A bag has 3 red and 2 blue marbles. Two marbles are drawn WITHOUT replacement.'
Q['dm-cn-s08-cp1-006']['parts'][3]['prompt'] = 'Compare P(both red) with drawing WITH replacement, where P(both red) = (3/5)² = 9/25.'
Q['dm-cn-s08-cp1-006']['solutionSteps'] = [
    '(a) Unordered pairs from 5 marbles: C(5, 2) = 10.',
    '(b) Both red: C(3, 2) = 3 of the 10 pairs, so P = 3/10.',
    '(c) Both blue: C(2, 2) = 1 of the 10 pairs, so P = 1/10.',
    '(d) With replacement P(both red) = (3/5)(3/5) = 9/25; without replacement it is (3/5)(2/4) = 3/10, smaller because one red is gone before the second draw.']
q = Q['dm-gr-s07-honors-004']
q['prompt'] = 'A connected weighted graph has vertices A, B, C, D, E and edges AB 4, AC 2, BC 5, BD 10, CD 3, CE 8, DE 6. How many edges does any spanning tree of this graph have?'
q['solutionSteps'] = ['A spanning tree reaches all 5 vertices and has no cycle.', 'Every tree with n vertices has n − 1 edges.', '5 − 1 = 4 edges, whatever the weights.']
q = Q['dm-lp-s07-cp1-003']
q['prompt'] = 'A student makes bracelets (x, $4 profit each) and keychains (y, $3 profit each) with constraints x + y ≤ 20, 2x + y ≤ 30, x ≥ 0, y ≥ 0. What is the maximum profit (dollars)?'
q['solutionSteps'] = ['Corners: (0, 0), (0, 20), (15, 0) and the intersection of x + y = 20 with 2x + y = 30: subtract to get x = 10, y = 10.',
                      'Profit P = 4x + 3y at each corner: (0, 0) → 0, (0, 20) → 60, (10, 10) → 70, (15, 0) → 60.',
                      'The largest value is 70 at (10, 10): 10 bracelets and 10 keychains earn $70.']
q = Q['dm-lp-s07-honors-003']
q['prompt'] = 'A farm grows x acres of corn ($300 profit/acre) and y acres of soy ($200/acre) with x + y ≤ 100 (land) and 2x + y ≤ 150 (labor), x ≥ 0, y ≥ 0. By how much is the labor constraint 2x + y ≤ 150 slack at the optimum?'
q['solutionSteps'] = ['Corners: (0, 0), (0, 100), (75, 0) and x + y = 100 ∩ 2x + y = 150, which gives x = 50, y = 50.',
                      'P = 300x + 200y: (0, 0) → 0, (0, 100) → 20000, (50, 50) → 25000, (75, 0) → 22500, so the optimum is (50, 50).',
                      'Labor used: 2·50 + 50 = 150 of 150, so the slack is 150 − 150 = 0 (the constraint is binding).']

# ---------------- #17 LP binding constraints ----------------
q = Q['dm-lp-s07-cp1-005']
q['prompt'] = 'At the optimal point (10, 20) of a problem with constraints x + y ≤ 30, x ≤ 15, 2x + y ≤ 50, which statements are true? Select ALL that apply.'
q['options'] = [{'text': 'x + y ≤ 30 is binding (it uses 30 of 30)', 'correct': True},
                {'text': '2x + y ≤ 50 is binding', 'correct': False},
                {'text': 'x ≤ 15 is binding', 'correct': False},
                {'text': '2x + y ≤ 50 has slack 10 (it uses 40 of 50)', 'correct': True},
                {'text': 'x ≤ 15 has slack 5 (it uses 10 of 15)', 'correct': True}]
q['answer'] = [o['text'] for o in q['options'] if o['correct']]
q['solutionSteps'] = ['Substitute (10, 20) into each constraint.', 'x + y = 30: equal to its limit, so it is binding (slack 0).',
                      '2x + y = 40: 10 below its limit of 50, so its slack is 10.', 'x = 10: 5 below its limit of 15, so its slack is 5.']

# ---------------- #20 family tags ----------------
for q in Q.values():
    if not family(q) and 'family:' not in q.get('sourceNotes', ''):
        P = q['prompt']
        f = 'multiples_count' if 'multiples of' in P else 'fencepost_check' if 'says the list' in P else 'step_list_count'
        set_family(q, f)

# ---------------- #12 fresh election data for repeated schedules and weighted systems ----------------
rng = random.Random(20261118)


def schedule_of(P):
    return [(int(n), r.split(' > ')) for n, r in re.findall(r'(\d+) voters: ([A-Z](?: > [A-Z])+)', P)]


def with_schedule(P, rows):
    head, _, rest = P.partition('Preference schedule:\n')
    lines = rest.split('\n'); k = sum(1 for l in lines if re.match(r'\d+ voters:', l))
    return head + 'Preference schedule:\n' + E.fmt_schedule(rows) + '\n' + '\n'.join(lines[k:])


def tally(c):
    return ', '.join(f'{k} {E.fs(v)}' for k, v in sorted(c.items()))


def solve_method(P, rows):
    """Return (winner, steps) for the method named in P, or (None, None) if there is no unique winner."""
    n = len(rows[0][1])
    if 'Borda' in P:
        c = E.borda(rows); w = E.unique_max(c)
        cand = sorted(c)[0]
        ex = ' + '.join(f'{k}·{n - r.index(cand)}' for k, r in rows)
        return w, [f'Points: {n} for 1st place down to 1 for last.', f'{cand}: {ex} = {c[cand]}.', f'Borda totals: {tally(c)}.', f'Winner: {w}.']
    if 'instant runoff' in P or 'elimination' in P:
        w, rounds = E.irv(rows); tot = sum(k for k, _ in rows)
        st = [f'{tot} voters, so a majority is {tot // 2 + 1}.'] + [f'Round {i + 1} first-place votes: {tally(r)}' + ('' if i == len(rounds) - 1 else f'; eliminate {min(r, key=r.get)}.') for i, r in enumerate(rounds)]
        return w, st + [f'Winner: {w} (a majority).']
    if 'pairwise' in P:
        C = sorted(rows[0][1]); st = []
        for a, b in itertools.combinations(C, 2):
            st.append(f'{a} vs {b}: {E.h2h(rows, a, b)}–{E.h2h(rows, b, a)}')
        c = E.pairwise(rows); w = E.unique_max(c)
        return w, ['; '.join(st) + '.', f'Points (1 per win, 1/2 per tie): {tally(c)}.', f'Winner: {w}.']
    c = E.first_place(rows); w = E.unique_max(c)
    tot = sum(k for k, _ in rows)
    return w, [f'Count only first-place votes: {tally(c)}.', f'{w} has the most ({c[w]} of {tot}); plurality needs the most votes, not a majority.', f'Winner: {w}.']


seen_sched, seen_sys = set(), set()
FAM_S = {'method_winner', 'condorcet_check', 'first_place', 'head_to_head', 'borda_points'}
FAM_W = {'count_winning', 'banzhaf', 'shapley', 'veto'}
refreshed = 0
for q in sorted(Q.values(), key=lambda q: q['id']):
    f = family(q); P = q['prompt']
    rows = schedule_of(P)
    if rows and f in FAM_S and q['format'] in ('multiple-choice', 'short-answer'):
        key = tuple((n, tuple(r)) for n, r in rows)
        if key not in seen_sched:
            seen_sched.add(key); continue
        for _ in range(2000):
            new = E.random_schedule(rng, len(rows[0][1]), len(rows))
            nk = tuple((n, tuple(r)) for n, r in new)
            if nk in seen_sched: continue
            P2 = with_schedule(P, new)
            if f == 'method_winner':
                w, st = solve_method(P2, new)
                if not w: continue
                ans = w
            elif f == 'condorcet_check':
                if q['format'] == 'short-answer':  # "The plurality winner is A. Does A also win ...?"
                    pw = E.unique_max(E.first_place(new))
                    if pw != 'A': continue
                    ok = all(E.h2h(new, 'A', b) > E.h2h(new, b, 'A') for b in new[0][1] if b != 'A')
                    ans = 'Yes' if ok else 'No'
                    st = [f'A vs {b}: {E.h2h(new, "A", b)}–{E.h2h(new, b, "A")}' for b in sorted(new[0][1]) if b != 'A']
                    st = ['; '.join(st) + '.', f'A {"wins" if ok else "does not win"} every head-to-head comparison, so the answer is {ans}.']
                else:
                    c = E.condorcet(new); ans = f'Yes, {c}' if c else 'No Condorcet winner'
                    C = sorted(new[0][1])
                    st = [f'{a} vs {b}: {E.h2h(new, a, b)}–{E.h2h(new, b, a)}' for a, b in itertools.combinations(C, 2)]
                    st = st + [f'{c} beats every other candidate head-to-head.' if c else 'No candidate beats all the others head-to-head.']
            elif f == 'first_place':
                x = re.search(r'does ([A-Z]) receive', P).group(1); v = E.first_place(new)[x]
                ans = str(v); st = [f'Add the counts of the rows that rank {x} first: ' + ' + '.join(str(n) for n, r in new if r[0] == x) + f' = {v}.' if v else f'No row ranks {x} first, so {x} has 0 first-place votes.']
            elif f == 'head_to_head':
                a, b = re.search(r'prefer ([A-Z]) to ([A-Z])', P).groups(); v = E.h2h(new, a, b)
                ans = str(v); st = [f'Rows ranking {a} above {b}: ' + (' + '.join(str(n) for n, r in new if r.index(a) < r.index(b)) or '0') + f' = {v}.', f'{v} prefer {a}; {E.h2h(new, b, a)} prefer {b}.']
            elif f == 'borda_points':
                x = re.search(r"Find ([A-Z])'s total", P).group(1); c = E.borda(new); n = len(new[0][1])
                ans = str(c[x]); st = [f'Points: {n} for 1st place down to 1 for last.', f'{x}: ' + ' + '.join(f'{k}·{n - r.index(x)}' for k, r in new) + f' = {c[x]}.', f'All Borda totals: {tally(c)}.']
            if q['format'] == 'multiple-choice':
                texts = [o['text'] for o in q['options']]
                if f in ('first_place',):
                    v = int(ans); d = [str(v + 1), str(v + 2), str(v + 3) if v + 3 != sum(n for n, _ in new) else str(sum(n for n, _ in new))]
                    opt(q, ans, d)
                else:
                    if ans not in texts:
                        if f == 'condorcet_check':
                            texts = ['Yes, ' + c for c in sorted(new[0][1])][:3] + ['No Condorcet winner']
                        else: continue
                    q['options'] = [{'text': t, 'correct': t == ans} for t in texts]
                    if ans not in texts: continue
            seen_sched.add(nk); q['prompt'] = P2; q['answer'] = ans; q['solutionSteps'] = st; refreshed += 1
            break
    m = re.search(r'\[(\d+): ([\d, ]+)\]', P)
    if m and f in FAM_W and q['format'] in ('multiple-choice', 'short-answer') and '_error' not in f:
        key = m.group(0)
        if key not in seen_sys:
            seen_sys.add(key); continue
        n = len(m.group(2).split(','))
        for _ in range(2000):
            qq, w = E.random_system(rng, n); nk = f'[{qq}: ' + ', '.join(map(str, w)) + ']'
            if nk in seen_sys: continue
            P2 = P.replace(key, nk); cr = E.critical_counts(qq, w); W = E.coalitions(qq, w)
            if f == 'count_winning':
                ans = str(len(W)); d = [str(len(W) - 1), str(len(W) + 1), str(2 ** n - 1)]
                if len(set(d + [ans])) < 4 or len(W) - 1 < 1: continue
                st = [f'A coalition wins when its total weight is at least {qq}.', 'Winning coalitions: ' + ', '.join(E.name(S) + f' ({sum(w[i] for i in S)})' for S in W) + '.', f'{len(W)} winning coalitions.']
            elif f == 'banzhaf':
                ans = E.fs(Fr(cr[0], sum(cr))); d = [E.fs(Fr(w[0], sum(w))), '1/4', E.fs(Fr(cr[0] + 1, sum(cr) + 1)), E.fs(Fr(cr[1], sum(cr)))]
                d = [x for x in d if x != ans]
                if len(set(d)) < 3: continue
                st = ['Winning coalitions (critical players in brackets): ' + '; '.join(E.name(S) + ' [' + ', '.join(f'P{i + 1}' for i in S if sum(w[j] for j in S) - w[i] < qq) + ']' for S in W) + '.',
                      'Critical counts: ' + ', '.join(f'P{i + 1} {c}' for i, c in enumerate(cr)) + f' (total {sum(cr)}).', f'Banzhaf index of P1 = {cr[0]}/{sum(cr)} = {ans}.']
            elif f == 'shapley':
                pc = E.pivotal_counts(qq, w); tot = math.factorial(n); ans = E.fs(Fr(pc[0], tot))
                st = [f'There are {n}! = {tot} orderings; in each, the pivotal player is the one whose weight first brings the total to {qq} or more.',
                      'Pivotal counts: ' + ', '.join(f'P{i + 1} {c}' for i, c in enumerate(pc)) + '.', f'Shapley–Shubik index of P1 = {pc[0]}/{tot} = {ans}.']
            elif f == 'veto':
                v = [f'P{i + 1}' for i in range(n) if sum(w) - w[i] < qq]; ans = ', '.join(v) or 'none'
                st = [f'Total weight {sum(w)}. A player has veto power when the others together fall short of {qq}.',
                      '; '.join(f'without P{i + 1}: {sum(w) - w[i]}' for i in range(n)) + '.', f'Veto players: {ans}.']
            if q['format'] == 'multiple-choice':
                opt(q, ans, d)
            q['prompt'] = P2; q['answer'] = ans; q['solutionSteps'] = st; seen_sys.add(nk); refreshed += 1
            break

# ---------------- #9 Relations on Finite and Infinite Sets ----------------
import math
S3, S4, S1 = 'properties-relations-skill-03', 'properties-relations-skill-04', 'properties-relations-skill-01'
rel = B['properties-relations']['questions']
moved = removed = 0
keep = []
nxt = {}
for q in rel:
    if q['skillId'] != S4:
        keep.append(q); continue
    infinite = re.search(r'ℤ|ℝ|ℕ|ℚ|infinite|integers|real', q['prompt'])
    if infinite:
        keep.append(q); continue
    f = family(q)
    if f == 'quick_check':
        removed += 1; continue
    q['skillId'] = S1 if f == 'count_relations' else S3
    q['sourceNotes'] += ' Moved from skill 4 by ' + NOTE
    moved += 1; keep.append(q)
B['properties-relations']['questions'] = keep

# Relations on infinite sets: (name, domain, rule, reflexive, symmetric, transitive, counterexample notes)
RELS = [
    ('m R n if and only if m − n is divisible by 5', 'ℤ', (True, True, True), {'R': 'm − m = 0 = 5·0', 'S': 'if m − n = 5k then n − m = 5(−k)', 'T': 'if m − n = 5j and n − p = 5k then m − p = 5(j + k)'}),
    ('m R n if and only if m + n is odd', 'ℤ', (False, True, False), {'R': '1 + 1 = 2 is even, so 1 is not related to 1', 'S': 'm + n = n + m', 'T': '1 R 2 and 2 R 3, but 1 + 3 = 4 is even'}),
    ('a R b if and only if a divides b', 'ℤ⁺ (positive integers)', (True, False, True), {'R': 'a = a·1', 'S': '2 | 4 but 4 ∤ 2', 'T': 'if b = aj and c = bk then c = a(jk)'}),
    ('x R y if and only if |x − y| ≤ 1', 'ℝ', (True, True, False), {'R': '|x − x| = 0 ≤ 1', 'S': '|x − y| = |y − x|', 'T': '0 R 1 and 1 R 2, but |0 − 2| = 2 > 1'}),
    ('x R y if and only if x < y', 'ℝ', (False, False, True), {'R': '1 < 1 is false', 'S': '1 < 2 but 2 < 1 is false', 'T': 'x < y and y < z give x < z'}),
    ('x R y if and only if x² = y²', 'ℤ', (True, True, True), {'R': 'x² = x²', 'S': 'x² = y² gives y² = x²', 'T': 'x² = y² and y² = z² give x² = z²'}),
    ('x R y if and only if xy ≥ 0', 'ℤ', (True, True, False), {'R': 'x·x = x² ≥ 0', 'S': 'xy = yx', 'T': '−1 R 0 and 0 R 1, but (−1)(1) = −1 < 0'}),
    ('x R y if and only if x − y is an integer', 'ℝ', (True, True, True), {'R': 'x − x = 0 is an integer', 'S': 'y − x = −(x − y) is an integer', 'T': '(x − y) + (y − z) = x − z is a sum of integers'}),
    ('m R n if and only if m ≤ n + 1', 'ℤ', (True, False, False), {'R': 'm ≤ m + 1', 'S': '0 R 5 (0 ≤ 6) but 5 ≤ 0 + 1 is false', 'T': '2 R 1 (2 ≤ 2) and 1 R 0 (1 ≤ 1), but 2 ≤ 0 + 1 is false'}),
    ('A R B if and only if A ⊆ B', 'the power set of ℕ', (True, False, True), {'R': 'every set is a subset of itself', 'S': '∅ ⊆ {1} but {1} ⊄ ∅', 'T': 'A ⊆ B and B ⊆ C give A ⊆ C'}),
    ('m R n if and only if mn is a perfect square (m, n ≥ 1)', 'ℤ⁺', (True, True, True), {'R': 'm·m = m² is a square', 'S': 'mn = nm', 'T': 'if mn = a² and np = b² then mp·n² = (ab)², so mp is a square'}),
    ('x R y if and only if x + y = 0', 'ℝ', (False, True, False), {'R': '1 + 1 ≠ 0', 'S': 'x + y = y + x', 'T': '1 R −1 and −1 R 1, but 1 + 1 ≠ 0'}),
]
PROP = ['reflexive', 'symmetric', 'transitive']
new = []
lv_cycle = ['cp2', 'cp1', 'honors']
k = 0
for i, (rule, dom, props, why) in enumerate(RELS):
    for j, p in enumerate(PROP):
        k += 1
        lv = lv_cycle[(i + j) % 3]
        yes = props[j]
        key = 'RST'[j]
        q = {'id': f'dm-rl-s04-{lv}-i{k:02d}', 'skillId': S4, 'level': lv, 'format': 'multiple-choice',
             'prompt': f'R on {dom}: {rule}. Is R {p}?',
             'answer': ('Yes: ' if yes else 'No: ') + why[key],
             'solutionSteps': [
                 {'reflexive': 'Reflexive means every element is related to itself; check a general element, not a few examples.',
                  'symmetric': 'Symmetric means a R b always forces b R a; check a general pair.',
                  'transitive': 'Transitive means a R b and b R c always force a R c; check a general chain.'}[p],
                 ('It holds for every element: ' if yes else 'One counterexample is enough: ') + why[key] + '.',
                 'On an infinite set you cannot check every case one by one, so a property needs a general argument and fails with a single counterexample.'],
             'options': [], 'standards': ['MP.7', 'DM.RELATIONS'],
             'sourceNotes': 'Original Claude-authored Discrete Math item (family: infinite_property). ' + NOTE}
        wrong_why = [w for kk, w in why.items() if kk != key]
        fourth = 'No: it fails for some element because the set is infinite' if yes else 'Yes: it holds for 1, 2 and 3, so it holds for every element'
        q['options'] = [{'text': q['answer'], 'correct': True},
                        {'text': ('No: ' if yes else 'Yes: ') + why[key], 'correct': False},
                        {'text': 'It cannot be decided on an infinite set', 'correct': False},
                        {'text': fourth, 'correct': False}]
        new.append(q)
# membership on infinite sets
MEM = [('ℤ', 'a R b if and only if 7 divides a − b', lambda a, b: (a - b) % 7 == 0, [(23, 2), (-5, 9), (40, -2), (100, 2)]),
       ('ℤ', 'a R b if and only if a² + b² is even', lambda a, b: (a * a + b * b) % 2 == 0, [(17, -3), (8, 11), (-6, 40), (15, 0)]),
       ('ℝ', 'x R y if and only if x − y ≥ 2', lambda a, b: a - b >= 2, [(5.5, 3.5), (2, 1), (-1, -4), (0, 0)])]
for i, (dom, rule, fn, pairs) in enumerate(MEM):
    for j, (a, b) in enumerate(pairs):
        k += 1; lv = lv_cycle[(i + j) % 3]; yes = fn(a, b)
        fa = lambda x: str(x).replace('-', '−')
        q = {'id': f'dm-rl-s04-{lv}-i{k:02d}', 'skillId': S4, 'level': lv, 'format': 'short-answer',
             'prompt': f'R on {dom}: {rule}. Is ({fa(a)}, {fa(b)}) ∈ R? Answer Yes or No.',
             'answer': 'Yes' if yes else 'No',
             'solutionSteps': [f'Substitute a = {fa(a)} and b = {fa(b)} into the rule.',
                               {0: f'a − b = {fa(a - b)}; {"7 divides it" if yes else "7 does not divide it"}.',
                                1: f'a² + b² = {a * a} + {b * b} = {a * a + b * b}, which is {"even" if yes else "odd"}.',
                                2: f'x − y = {fa(a - b)}, which is {"at least 2" if yes else "less than 2"}.'}[i],
                               f'So ({fa(a)}, {fa(b)}) {"is" if yes else "is not"} in R.'],
             'standards': ['MP.7', 'DM.RELATIONS'],
             'sourceNotes': 'Original Claude-authored Discrete Math item (family: infinite_member). ' + NOTE}
        new.append(q)
B['properties-relations']['questions'] += new

# ---------------- #10 balanced MC answer positions ----------------
mc = sorted((q for _, q in items(B) if q['format'] == 'multiple-choice'), key=lambda q: q['id'])
for i, q in enumerate(mc):
    n = len(q['options']); target = (i + h(q['skillId'])) % n
    c = [o for o in q['options'] if o['correct']][0]; rest = [o for o in q['options'] if not o['correct']]
    q['options'] = rest[:target] + [c] + rest[target:]

save(B)
print('elections/weighted refreshed', refreshed, '| relations moved', moved, 'removed', removed, 'added', len(new))
