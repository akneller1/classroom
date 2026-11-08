"""Unit 9: Election Theory (8 skills). Every tally, winner, power index, apportionment and fair-share is computed.
Conventions stated in prompts: Borda count gives n points for 1st place down to 1 point for last (n candidates); plurality with
elimination (instant runoff) removes the candidate with the fewest first-place votes each round; pairwise comparisons (Copeland)
give 1 point for a head-to-head win and 1/2 for a tie; a majority means MORE than half. Weighted systems are written [q: w1, w2, ...]."""
import itertools, math
from fractions import Fraction
from core import Bank, frac, seeded
import figs

U = 'election-theory'
BORDA = 'Borda count (n points for 1st place, n − 1 for 2nd, ..., 1 for last)'


def build():
    b = Bank(U, 'el', 8)
    for f in (s1, s2, s3, s4, s5, s6, s7, s8, topup, errors):
        f(b)
    return b


def num_mc(b, k, L, prompt, ans, wr, steps, fam):
    ws = [str(w) for w in dict.fromkeys(wr) if str(w) != str(ans)]
    return b.mc(k, L, prompt, str(ans), ws[:3], steps, fam, order='sort')


# ---------------------------------------------------------------- election engine
def schedule_text(S):
    return '\n'.join('%d voter%s: %s' % (n, '' if n == 1 else 's', ' > '.join(r)) for n, r in S)


def cands(S):
    return sorted(set(S[0][1]))


def first_counts(S, alive=None):
    alive = alive or cands(S)
    c = {x: 0 for x in alive}
    for n, r in S:
        top = next(x for x in r if x in alive)
        c[top] += n
    return c


def plurality(S):
    c = first_counts(S)
    m = max(c.values())
    w = [x for x in c if c[x] == m]
    return w[0] if len(w) == 1 else None, c


def borda(S):
    k = len(cands(S))
    pts = {x: 0 for x in cands(S)}
    for n, r in S:
        for i, x in enumerate(r):
            pts[x] += n * (k - i)
    m = max(pts.values())
    w = [x for x in pts if pts[x] == m]
    return (w[0] if len(w) == 1 else None), pts


def irv(S):
    alive = cands(S)
    rounds = []
    tot = sum(n for n, _ in S)
    while True:
        c = first_counts(S, alive)
        rounds.append(dict(c))
        top = max(c.values())
        if top * 2 > tot:
            return [x for x in c if c[x] == top][0], rounds
        low = min(c.values())
        losers = [x for x in c if c[x] == low]
        if len(losers) > 1:
            return None, rounds
        alive = [x for x in alive if x != losers[0]]


def head(S, a, c):
    av = sum(n for n, r in S if r.index(a) < r.index(c))
    return av, sum(n for n, _ in S) - av


def pairwise(S):
    pts = {x: Fraction(0) for x in cands(S)}
    for a, c in itertools.combinations(cands(S), 2):
        x, y = head(S, a, c)
        if x > y:
            pts[a] += 1
        elif y > x:
            pts[c] += 1
        else:
            pts[a] += Fraction(1, 2); pts[c] += Fraction(1, 2)
    m = max(pts.values())
    w = [x for x in pts if pts[x] == m]
    return (w[0] if len(w) == 1 else None), pts


def condorcet(S):
    for a in cands(S):
        if all(head(S, a, c)[0] > head(S, a, c)[1] for c in cands(S) if c != a):
            return a
    return None


SCHED = {
    'e1': [(14, ('A', 'B', 'C')), (10, ('C', 'B', 'A')), (8, ('B', 'C', 'A')), (3, ('C', 'A', 'B'))],
    'e2': [(8, ('A', 'B', 'C', 'D')), (6, ('B', 'C', 'D', 'A')), (5, ('C', 'D', 'B', 'A')), (3, ('D', 'C', 'B', 'A'))],
    'e3': [(8, ('A', 'C', 'B')), (6, ('B', 'C', 'A')), (5, ('C', 'B', 'A')), (2, ('C', 'A', 'B'))],
    'e4': [(10, ('A', 'B', 'C', 'D')), (8, ('B', 'C', 'D', 'A')), (6, ('C', 'B', 'D', 'A')), (4, ('D', 'C', 'B', 'A')), (3, ('D', 'B', 'C', 'A'))],
    'e5': [(5, ('A', 'B', 'C')), (4, ('B', 'C', 'A')), (2, ('C', 'A', 'B'))],
    'e6': [(9, ('P', 'Q', 'R')), (7, ('Q', 'R', 'P')), (6, ('R', 'Q', 'P')), (2, ('R', 'P', 'Q'))],
}
NAME = {'plurality': 'plurality', 'borda': BORDA, 'irv': 'plurality with elimination (instant runoff)', 'pairwise': 'pairwise comparisons (1 point per head-to-head win, 1/2 per tie)'}
METH = {'plurality': plurality, 'borda': borda, 'irv': irv, 'pairwise': pairwise}


def explain(method, S):
    w, data = METH[method](S)
    if method == 'irv':
        return w, ['Round %d first-place votes: %s' % (i + 1, ', '.join('%s %d' % kv for kv in r.items())) for i, r in enumerate(data)] + ['Winner: %s (majority of %d voters).' % (w, sum(n for n, _ in S))]
    if method == 'pairwise':
        lines = ['%s vs %s: %d–%d' % (a, c, *head(S, a, c)) for a, c in itertools.combinations(cands(S), 2)]
        return w, lines + ['Points: ' + ', '.join('%s %s' % (k, frac(v)) for k, v in data.items()) + '. Winner: %s.' % w]
    return w, [('First-place votes: ' if method == 'plurality' else 'Borda points: ') + ', '.join('%s %d' % kv for kv in data.items()) + '.', 'Winner: %s.' % w]


# ---------------------------------------------------------------- 1. terminology and preference data
def s1(b):
    for L, key in (('cp2', 'e5'), ('cp2', 'e1'), ('cp1', 'e2'), ('cp1', 'e3'), ('honors', 'e4'), ('honors', 'e6')):
        S = SCHED[key]
        tot = sum(n for n, _ in S)
        b.sa(1, L, 'Preference schedule (each row lists a ballot from most to least preferred):\n%s\nHow many voters are there, and how many votes is a MAJORITY? Answer as "voters, majority".' % schedule_text(S),
             '%d, %d' % (tot, tot // 2 + 1), ['Add the voter counts.', 'A majority is more than half: %d.' % (tot // 2 + 1)], 'voters_majority')
    for L, key, x in (('cp2', 'e1', 'C'), ('cp1', 'e2', 'B'), ('honors', 'e4', 'D')):
        S = SCHED[key]
        c = first_counts(S)[x]
        num_mc(b, 1, L, 'Preference schedule:\n%s\nHow many first-place votes does %s receive?' % (schedule_text(S), x), c, [c + 2, sum(n for n, r in S if x in r[:2]), max(first_counts(S).values())],
               ['Add the counts of ballots ranking %s first.' % x, '%d' % c], 'first_place')
    for L, key, a, c in (('cp2', 'e5', 'A', 'B'), ('cp1', 'e3', 'B', 'C'), ('honors', 'e4', 'B', 'C')):
        S = SCHED[key]
        x, y = head(S, a, c)
        b.sa(1, L, 'Preference schedule:\n%s\nIn a head-to-head comparison, how many voters prefer %s to %s?' % (schedule_text(S), a, c), x,
             ['Add the rows where %s is ranked above %s.' % (a, c), '%d prefer %s; %d prefer %s.' % (x, a, y, c)], 'head_to_head')
    TERM = [('cp2', 'What does a preference ballot record?', 'A voter\'s ranking of all the candidates', ['Only the voter\'s top choice', 'The number of voters', 'The winner of the election']),
            ('cp1', 'With 41 voters, how many votes make a majority?', '21', ['20', '20.5', '41']),
            ('honors', 'Which statement correctly distinguishes a majority from a plurality?', 'A majority is more than half the votes; a plurality is the most votes, which may be less than half', ['They mean the same thing', 'A plurality is more than half; a majority is the most votes', 'A majority requires all the votes'])]
    for L, t, good, bad in TERM:
        b.mc(1, L, t, good, bad, ['Majority: more than half. Plurality: more than any other candidate.', good], 'terminology')
    b.sel(1, 'cp2', 'Schedule: 5 voters A > B > C; 4 voters B > C > A; 3 voters C > A > B. Which statements are true?', [('There are 12 voters', True), ('A has 5 first-place votes', True), ('No candidate has a majority of first-place votes', True), ('B has a majority', False), ('C has 4 first-place votes', False)],
          ['12 voters; majority 7; first-place votes A 5, B 4, C 3.'], 'schedule_select')
    b.sel(1, 'cp1', 'Which are valid ways to present the same preference data?', [('A preference schedule with counts', True), ('A list of every individual ballot', True), ('A table of head-to-head results derived from the ballots', False), ('A bar graph of first-place votes only', False), ('Rows ordered by voter count instead of by ballot', True)],
          ['Head-to-head tables and first-place bar graphs lose information; reordering rows does not.'], 'schedule_select')
    b.sel(1, 'honors', 'For the preference schedule (10 A>B>C>D, 8 B>C>D>A, 6 C>B>D>A, 4 D>C>B>A, 3 D>B>C>A), which statements are true?', [('There are 31 voters', True), ('A is ranked last by 21 voters', True), ('B is ranked first or second by 27 voters', True), ('D has a majority of last-place votes', False), ('C has 10 first-place votes', False)],
          ['A last: 8 + 6 + 4 + 3 = 21. B in top two: 10 + 8 + 6 + 3 = 27. C first: 6.'], 'schedule_select')
    b.orq(1, 'cp2', 'Ballots: 6 voters rank Pizza > Tacos > Salad; 5 rank Tacos > Salad > Pizza; 2 rank Salad > Tacos > Pizza.',
          [('How many voters?', '13'), ('How many votes is a majority?', '7'), ('Does any food have a majority of first-place votes?', 'No'), ('How many voters prefer Tacos to Pizza?', '7')],
          ['6 + 5 + 2.', 'More than 6.5.', 'Pizza 6, Tacos 5, Salad 2.', '5 + 2.'], 'schedule_or')
    b.orq(1, 'cp1', 'Preference schedule: 8 A>C>B, 6 B>C>A, 5 C>B>A, 2 C>A>B.',
          [('Find the total number of voters.', '21'), ('Find each candidate\'s first-place votes.', 'A 8, B 6, C 7'), ('How many voters prefer C to A?', str(head(SCHED['e3'], 'C', 'A')[0])), ('Who wins the head-to-head between B and C?', 'C (%d to %d)' % head(SCHED['e3'], 'C', 'B'))],
          ['Add.', 'Top rows.', 'Rows with C above A.', 'Compare.'], 'schedule_or')
    b.orq(1, 'honors', 'An election has 4 candidates and every voter submits a complete ranking.',
          [('How many different rankings are possible?', '24'), ('If 50 voters vote, what is a majority?', '26'), ('What is the minimum number of first-place votes a plurality winner could have (no ties)?', '14'),
           ('Explain why a plurality winner may be opposed by most voters.', 'With 13 of 50 first-place votes, 37 voters ranked someone else first.')],
          ['4!.', 'More than 25.', 'If the winner has w votes and each other candidate at most w − 1, then w + 3(w − 1) ≥ 50, so w ≥ 13.25: w = 14 (14 + 12 + 12 + 12 = 50).', 'Plurality ≠ majority.'], 'schedule_or')


# ---------------------------------------------------------------- 2. comparing methods
def s2(b):
    plan = {'cp2': [('e5', 'plurality'), ('e1', 'plurality'), ('e5', 'borda'), ('e1', 'borda')],
            'cp1': [('e1', 'irv'), ('e2', 'borda'), ('e3', 'pairwise'), ('e2', 'plurality')],
            'honors': [('e4', 'irv'), ('e4', 'borda'), ('e6', 'pairwise'), ('e2', 'irv')]}
    for L, items in plan.items():
        for i, (key, m) in enumerate(items):
            S = SCHED[key]
            w, steps = explain(m, S)
            if w is None:
                continue
            if i % 2 == 0:
                b.mc(2, L, 'Preference schedule:\n%s\nWho wins by %s?' % (schedule_text(S), NAME[m]), w, [c for c in cands(S) if c != w] + ['There is a tie'], steps, 'method_winner')
            else:
                b.sa(2, L, 'Preference schedule:\n%s\nWho wins by %s? Answer with the letter.' % (schedule_text(S), NAME[m]), w, steps, 'method_winner')
    for L, key, x in (('cp2', 'e5', 'B'), ('cp1', 'e2', 'C'), ('honors', 'e4', 'B')):
        S = SCHED[key]
        p = borda(S)[1][x]
        b.sa(2, L, 'Preference schedule:\n%s\nFind %s\'s total using the %s.' % (schedule_text(S), x, BORDA), p, ['Multiply each row\'s count by the points for %s\'s position and add.' % x, 'Borda points: %s.' % borda(S)[1]], 'borda_points')
    b.sel(2, 'cp1', 'For the preference schedule (14 A>B>C, 10 C>B>A, 8 B>C>A, 3 C>A>B), which methods choose B?', [(NAME[m].split(' (')[0].capitalize(), METH[m](SCHED['e1'])[0] == 'B') for m in ('plurality', 'borda', 'irv', 'pairwise')] + [('None of the four methods', False)],
          [explain(m, SCHED['e1'])[1][-1] for m in ('plurality', 'borda', 'irv', 'pairwise')], 'method_select')
    b.sel(2, 'cp2', 'Which voting methods use the full ranking on each ballot (not just first choices)?', [('Borda count', True), ('Pairwise comparisons', True), ('Plurality with elimination, after the first round', True), ('Plurality', False), ('Counting first-place votes only', False)],
          ['Plurality looks only at first choices.'], 'method_select')
    b.sel(2, 'honors', 'Preference schedule:\n' + schedule_text(SCHED['e4']) + '\nWhich statements are true?', [('Plurality chooses A', plurality(SCHED['e4'])[0] == 'A'), ('The Borda winner is B', borda(SCHED['e4'])[0] == 'B'), ('A is the Condorcet loser (loses every head-to-head)', all(head(SCHED['e4'], 'A', c)[0] < head(SCHED['e4'], 'A', c)[1] for c in 'BCD')),
                                                                      ('Instant runoff chooses A', irv(SCHED['e4'])[0] == 'A'), ('Every method agrees', len({METH[m](SCHED['e4'])[0] for m in METH}) == 1)],
          [explain(m, SCHED['e4'])[1][-1] for m in ('plurality', 'borda', 'irv', 'pairwise')], 'method_select')
    b.orq(2, 'cp2', 'Preference schedule:\n' + schedule_text(SCHED['e5']),
          [('Plurality winner?', plurality(SCHED['e5'])[0]), ('Borda points for A, B, C (3-2-1)?', ', '.join('%s %d' % kv for kv in borda(SCHED['e5'])[1].items())), ('Borda winner?', borda(SCHED['e5'])[0] or 'tie'), ('Instant-runoff winner?', irv(SCHED['e5'])[0])],
          explain('plurality', SCHED['e5'])[1] + explain('borda', SCHED['e5'])[1] + explain('irv', SCHED['e5'])[1], 'methods_or')
    S = SCHED['e2']
    b.orq(2, 'cp1', 'Preference schedule:\n' + schedule_text(S),
          [('Plurality winner?', plurality(S)[0]), ('Borda winner (4-3-2-1)?', borda(S)[0]), ('Instant-runoff winner?', irv(S)[0]), ('Pairwise-comparison winner?', pairwise(S)[0])],
          explain('plurality', S)[1] + explain('borda', S)[1] + explain('irv', S)[1] + explain('pairwise', S)[1], 'methods_or')
    S = SCHED['e6']
    b.orq(2, 'honors', 'Preference schedule:\n' + schedule_text(S),
          [('Plurality winner?', plurality(S)[0]), ('Instant-runoff winner? Show the rounds.', irv(S)[0] + ' — ' + '; '.join(explain('irv', S)[1][:-1])), ('Is there a Condorcet winner?', condorcet(S) or 'No'),
           ('Explain how the plurality winner can lose under other methods.', 'P has the most first-place votes but most voters rank P last, so it loses head-to-head and when transfers happen.')],
          explain('irv', S)[1] + explain('pairwise', S)[1], 'methods_or')


# ---------------------------------------------------------------- 3. analyzing results (fairness criteria)
def s3(b):
    CR = [('cp2', 'The majority criterion says ...', 'A candidate with a majority of first-place votes should win', ['The candidate with the most first-place votes should win', 'A candidate who beats every other head-to-head should win', 'Removing a loser should not change the winner']),
          ('cp1', 'The Condorcet criterion says ...', 'A candidate who wins every head-to-head comparison should win', ['A candidate with a majority should win', 'Gaining support should never hurt a winner', 'Every voter should be a dictator']),
          ('cp1', 'The monotonicity criterion says ...', 'If a winner gains support (and nothing else changes), the winner should still win', ['The winner must have a majority', 'Removing a loser should not change the winner', 'Each candidate gets equal points']),
          ('honors', 'The independence of irrelevant alternatives (IIA) criterion says ...', 'If a losing candidate is removed and the ballots are recounted, the winner should not change', ['A candidate with a majority should win', 'Ties must be broken alphabetically', 'A Condorcet winner should win'])]
    for L, t, good, bad in CR:
        b.mc(3, L, t, good, bad, ['Know the statements of the four fairness criteria.', good], 'criterion_def')
    VIO = [('cp2', 'Which method can violate the MAJORITY criterion?', 'Borda count', ['Plurality', 'Plurality with elimination', 'Pairwise comparisons']),
           ('cp1', 'Which method always satisfies the Condorcet criterion?', 'Pairwise comparisons', ['Plurality', 'Borda count', 'Plurality with elimination']),
           ('honors', 'Which method can violate MONOTONICITY?', 'Plurality with elimination (instant runoff)', ['Plurality', 'Borda count', 'Pairwise comparisons'])]
    for L, t, good, bad in VIO:
        b.mc(3, L, t, good, bad, ['Borda can violate majority; plurality, Borda and IRV can violate Condorcet; IRV can violate monotonicity; all four can violate IIA.', good], 'criterion_method')
    # computed checks
    for L, key in (('cp1', 'e1'), ('honors', 'e4'), ('cp2', 'e5')):
        S = SCHED[key]
        cw = condorcet(S)
        b.mc(3, L, 'Preference schedule:\n%s\nIs there a Condorcet winner? If so, who?' % schedule_text(S), ('Yes, ' + cw) if cw else 'No Condorcet winner',
             ['No Condorcet winner'] + ['Yes, ' + c for c in cands(S) if c != cw][:3] if cw else ['Yes, ' + c for c in cands(S)][:3],
             ['%s vs %s: %d–%d' % (a, c, *head(S, a, c)) for a, c in itertools.combinations(cands(S), 2)] + ['A Condorcet winner must beat every other candidate head-to-head.'], 'condorcet_check')
    bord = [(3, ('A', 'B', 'C')), (2, ('B', 'C', 'A'))]
    S = bord
    b.mc(3, 'honors', 'Schedule: 3 voters A > B > C; 2 voters B > C > A. Under the %s, which criterion is violated?' % BORDA,
         'Majority criterion: A has a majority of first-place votes but B wins', ['Monotonicity criterion', 'No criterion is violated', 'Condorcet criterion only, because A wins'],
         ['Borda: A 3·3 + 2·1 = 11, B 3·2 + 2·3 = 12, C 3·1 + 2·2 = 7.', 'A has 3 of 5 first-place votes (a majority) but B wins.'], 'criterion_violation')
    assert borda(S)[0] == 'B' and first_counts(S)['A'] == 3
    S = SCHED['e1']
    b.sa(3, 'cp1', 'Preference schedule:\n%s\nThe plurality winner is A. Does A also win the head-to-head comparisons against both B and C? Answer Yes or No.' % schedule_text(S),
         'Yes' if all(head(S, 'A', c)[0] > head(S, 'A', c)[1] for c in 'BC') else 'No', ['A vs B: %d–%d; A vs C: %d–%d.' % (*head(S, 'A', 'B'), *head(S, 'A', 'C'))], 'condorcet_check')
    b.sel(3, 'cp2', 'Which fairness criteria are satisfied by every election decided by plurality?', [('Majority criterion', True), ('Monotonicity criterion', True), ('Condorcet criterion', False), ('Independence of irrelevant alternatives', False), ('Pareto (if everyone prefers X to Y, Y does not win)', True)],
          ['Plurality satisfies majority, monotonicity and Pareto; it can violate Condorcet and IIA.'], 'criterion_select')
    b.sel(3, 'cp1', 'Which statements are true?', [('A Condorcet winner, if one exists, is unique', True), ('A majority candidate is always a Condorcet winner', True), ('Some elections have no Condorcet winner', True), ('Borda always picks the majority candidate', False), ('Pairwise comparisons can violate the Condorcet criterion', False)],
          ['A majority candidate beats everyone head-to-head; cycles can prevent a Condorcet winner.'], 'criterion_select')
    b.sel(3, 'honors', 'Arrow\'s impossibility theorem says no ranked method with 3 or more candidates satisfies all of a set of fairness conditions. Which statements are consistent with it?', [('Every voting method can violate some reasonable fairness criterion', True), ('Choosing a method involves trade-offs', True), ('Pairwise comparisons can violate IIA', True), ('Borda count satisfies every criterion', False), ('The theorem applies to two-candidate elections', False)],
          ['With two candidates, majority rule is fair; with three or more, trade-offs are unavoidable.'], 'criterion_select')
    b.orq(3, 'cp1', 'Schedule: 4 A>B>C, 3 B>C>A, 2 C>B>A.',
          [('Plurality winner?', 'A'), ('Head-to-head A vs B and A vs C.', 'B beats A 5–4; C beats A 5–4'), ('Is there a Condorcet winner?', 'Yes, B (B beats C 7–2)'), ('Which criterion does plurality violate here?', 'The Condorcet criterion')],
          ['A has 4.', 'Count.', 'B beats both.', 'Condorcet winner B loses under plurality.'], 'criterion_or')
    S3 = [(4, ('A', 'B', 'C')), (3, ('B', 'C', 'A')), (2, ('C', 'B', 'A'))]
    assert plurality(S3)[0] == 'A' and condorcet(S3) == 'B'
    b.orq(3, 'cp2', 'A class votes: 10 students want Zoo first, 8 want Museum first, 3 want Park first.',
          [('Does any choice have a majority?', 'No; a majority is 11.'), ('Which choice wins by plurality?', 'Zoo'), ('If Park is removed and all 3 Park voters prefer Museum to Zoo, who wins?', 'Museum (11 to 10)'), ('Which criterion does this illustrate?', 'Independence of irrelevant alternatives can fail under plurality.')],
          ['21 voters.', 'Most first-place votes.', 'Transfer.', 'Removing a loser changed the winner.'], 'criterion_or')
    M1 = [(7, ('B', 'C', 'A')), (10, ('C', 'A', 'B')), (8, ('A', 'B', 'C'))]
    M2 = [(7, ('B', 'C', 'A')), (12, ('C', 'A', 'B')), (6, ('A', 'B', 'C'))]
    assert irv(M1)[0] == 'C' and irv(M2)[0] == 'B'
    b.orq(3, 'honors', 'Instant runoff and monotonicity. Original schedule: 7 B>C>A, 10 C>A>B, 8 A>B>C.',
          [('Find the instant-runoff winner. Show the rounds.', 'Round 1: B 7, C 10, A 8; B is eliminated and its 7 votes go to C; C wins 17–8.'),
           ('Two of the A>B>C voters change to C>A>B (they move the winner C to the top). Find the new instant-runoff winner.', 'Round 1: B 7, C 12, A 6; A is eliminated and its 6 votes go to B; B wins 13–12.'),
           ('Which fairness criterion is violated?', 'Monotonicity: C gained support and lost.'), ('Explain why this can happen under instant runoff.', 'Changing first-place votes changes which candidate is eliminated first, which changes where transferred votes go.')],
          ['Eliminate the fewest first-place votes and transfer.', 'Recount with the new ballots.', 'Monotonicity.', 'The elimination order changed.'], 'criterion_or')


# ---------------------------------------------------------------- 4. weighted voting
def winning(q, w, coal):
    return sum(w[i] for i in coal) >= q


def players_info(q, w):
    n = len(w)
    tot = sum(w)
    dictator = [i for i in range(n) if w[i] >= q]
    veto = [i for i in range(n) if tot - w[i] < q]
    crit = banzhaf_counts(q, w)
    dummy = [i for i in range(n) if crit[i] == 0]
    return dictator, veto, dummy


def banzhaf_counts(q, w):
    n = len(w)
    c = [0] * n
    for r in range(1, n + 1):
        for coal in itertools.combinations(range(n), r):
            if winning(q, w, coal):
                for i in coal:
                    if not winning(q, w, [j for j in coal if j != i]):
                        c[i] += 1
    return c


def shapley(q, w):
    n = len(w)
    c = [0] * n
    for perm in itertools.permutations(range(n)):
        s = 0
        for i in perm:
            s += w[i]
            if s >= q:
                c[i] += 1
                break
    return [Fraction(x, math.factorial(n)) for x in c]


def sys_txt(q, w):
    return '[%d: %s]' % (q, ', '.join(map(str, w)))


WS = [(6, [4, 3, 2]), (8, [5, 3, 2]), (10, [6, 4, 3, 1]), (12, [7, 5, 4, 2]), (9, [9, 3, 2]), (11, [5, 4, 3, 2]), (14, [8, 6, 4, 1]), (15, [8, 7, 3, 2])]


def s4(b):
    for L, (q, w) in (('cp2', WS[0]), ('cp2', WS[4]), ('cp1', WS[1]), ('cp1', WS[2]), ('honors', WS[3]), ('honors', WS[6])):
        d, v, dm = players_info(q, w)
        nm = lambda xs: ', '.join('P%d' % (i + 1) for i in xs) or 'none'
        b.sa(4, L, 'In the weighted voting system %s (players P1, P2, ... in order), list the players with VETO power (comma-separated, or "none").' % sys_txt(q, w), nm(v),
             ['A player has veto power when the other players together cannot reach the quota.', 'Total %d; veto players: %s; dictators: %s; dummies: %s.' % (sum(w), nm(v), nm(d), nm(dm))], 'veto')
    QR = [('cp2', [5, 4, 3], 'What is the smallest valid quota (more than half the total weight)?', 7), ('cp1', [7, 5, 4, 2], 'What is the smallest valid quota (more than half)?', 10),
          ('cp1', [7, 5, 4, 2], 'What is the largest possible quota?', 18), ('honors', [10, 6, 5, 3, 1], 'What is the smallest valid quota (more than half)?', 13)]
    for L, w, t, v in QR:
        b.sa(4, L, 'Weights: %s. %s' % (', '.join(map(str, w)), t), v, ['Total weight %d. A quota must be more than half the total and at most the total.' % sum(w), 'Answer: %d' % v], 'quota_range')
    for L, (q, w) in (('cp2', WS[0]), ('cp1', WS[5]), ('honors', WS[7])):
        n = sum(1 for r in range(1, len(w) + 1) for c in itertools.combinations(range(len(w)), r) if winning(q, w, c))
        num_mc(b, 4, L, 'How many winning coalitions does %s have?' % sys_txt(q, w), n, [n + 1, n - 1, 2 ** len(w) - 1],
               ['List coalitions with total weight ≥ quota.', '%d winning coalitions' % n], 'count_winning')
    b.sel(4, 'cp2', 'In [9: 9, 3, 2], which statements are true?', [('P1 is a dictator', True), ('P2 is a dummy', True), ('P3 is a dummy', True), ('P1 is the only player with veto power', True), ('P2 has veto power', False)],
          ['P1 alone meets the quota, so P2 and P3 are never critical.'], 'weighted_select')
    b.sel(4, 'cp1', 'Which weighted systems are VALID (quota more than half the total and at most the total)?', [('[6: 4, 3, 2]', True), ('[10: 5, 5, 4]', True), ('[4: 3, 2, 2]', False), ('[12: 5, 4, 2]', False), ('[8: 4, 4, 4, 2]', True)],
          ['[4: 3, 2, 2] has quota ≤ half of 7 (anarchy risk); [12: 5, 4, 2] has quota above the total 11.'], 'weighted_select')
    b.sel(4, 'honors', 'In [12: 7, 5, 4, 2], which statements are true?', [('P1 has veto power', 0 in players_info(12, [7, 5, 4, 2])[1]), ('P4 is a dummy', 3 in players_info(12, [7, 5, 4, 2])[2]), ('No player is a dictator', True), ('Every coalition containing P1 and P2 wins', True), ('P3 has veto power', False)],
          ['Without P1 the others total 11 < 12 → veto. {P1, P2} = 12 wins. P4 is never critical: every winning coalition with P4 still wins without it.'], 'weighted_select')
    b.orq(4, 'cp2', 'A club uses [7: 4, 3, 2, 1] for players A, B, C, D.',
          [('What is the total weight?', '10'), ('Does {A, B} win?', 'Yes, 7'), ('Does {B, C, D} win?', 'No, 6'), ('Does A have veto power? Explain.', 'Yes; without A the others total 6 < 7.')],
          ['Add.', '4 + 3 = 7.', '3 + 2 + 1 = 6.', 'Compare with quota.'], 'weighted_or')
    b.orq(4, 'cp1', 'Consider [q: 6, 4, 2].',
          [('Which quotas are valid?', '7 through 12'), ('For q = 7, does P1 have veto power?', 'Yes; 4 + 2 = 6 < 7'), ('For q = 6, what goes wrong?', 'q is not more than half of 12, so {P1} and {P2, P3} could both win.'), ('For q = 12, describe the system.', 'Unanimity: every player has veto power.')],
          ['More than 6, at most 12.', 'Others total 6.', 'Opposing coalitions both win.', 'All needed.'], 'weighted_or')
    b.orq(4, 'honors', 'A county board: [31: 17, 15, 9, 7, 3].',
          [('Is any player a dictator?', 'No'), ('Which players have veto power?', ', '.join('P%d' % (i + 1) for i in players_info(31, [17, 15, 9, 7, 3])[1]) or 'none'),
           ('Which players are dummies?', ', '.join('P%d' % (i + 1) for i in players_info(31, [17, 15, 9, 7, 3])[2]) or 'none'), ('Explain why weight does not equal power.', 'A small weight can still be critical in some coalitions, and a large weight can have limited extra influence.')],
          ['No weight ≥ 31.', 'Others total < 31.', 'Never critical.', 'Banzhaf power differs from weight.'], 'weighted_or')


# ---------------------------------------------------------------- 5. coalitions and power
def s5(b):
    for L, (q, w) in (('cp2', WS[0]), ('cp2', WS[1]), ('cp1', WS[2]), ('cp1', WS[5]), ('honors', WS[3]), ('honors', WS[7])):
        c = banzhaf_counts(q, w)
        T = sum(c)
        idx = ', '.join('P%d %s' % (i + 1, frac(Fraction(x, T))) for i, x in enumerate(c))
        b.sa(5, L, 'Find the Banzhaf power index of P1 in %s. Give a fraction in lowest terms.' % sys_txt(q, w), frac(Fraction(c[0], T)),
             ['List winning coalitions and count how often each player is critical (its removal makes the coalition lose).', 'Critical counts: %s (total %d).' % (', '.join('P%d %d' % (i + 1, x) for i, x in enumerate(c)), T), 'Banzhaf indices: ' + idx], 'banzhaf')
    for L, (q, w) in (('cp1', WS[0]), ('honors', WS[1]), ('honors', WS[2])):
        s = shapley(q, w)
        b.sa(5, L, 'Find the Shapley–Shubik power index of P1 in %s (fraction of orderings in which P1 is pivotal). Give a fraction in lowest terms.' % sys_txt(q, w), frac(s[0]),
             ['List all %d orderings and find the pivotal player in each.' % math.factorial(len(w)), 'Indices: ' + ', '.join('P%d %s' % (i + 1, frac(x)) for i, x in enumerate(s))], 'shapley')
    CR = [('cp2', 6, [4, 3, 2], (0, 1), 'P1 and P2'), ('cp1', 10, [6, 4, 3, 1], (0, 1, 3), 'P1 and P2'), ('honors', 12, [7, 5, 4, 2], (0, 2, 3), 'Every player in the coalition')]
    for L, q, w, coal, ans in CR:
        crit = [i for i in coal if not winning(q, w, [j for j in coal if j != i])]
        assert (', '.join('P%d' % (i + 1) for i in crit).replace(', ', ' and ') == ans) or (ans.startswith('Every') and len(crit) == len(coal)), (ans, crit)
        b.mc(5, L, 'In %s, the coalition {%s} wins. Which players are critical in it?' % (sys_txt(q, w), ', '.join('P%d' % (i + 1) for i in coal)), ans,
             [x for x in ['P1 only', 'P1 and P2', 'P1 and P3', 'Every player in the coalition', 'No player'] if x != ans][:3],
             ['A player is critical if removing it drops the total below the quota %d.' % q, 'Critical: ' + ans], 'critical')
    b.sel(5, 'cp1', 'In [8: 5, 3, 2], which coalitions are winning?', [(('{%s}' % ', '.join('P%d' % (i + 1) for i in c)), winning(8, [5, 3, 2], c)) for c in [(0, 1), (0, 2), (1, 2), (0, 1, 2), (0,)]],
          ['Totals: P1P2 8, P1P3 7, P2P3 5, all 10, P1 5.'], 'power_select')
    b.sel(5, 'cp2', 'Which statements about critical players are true?', [('A critical player\'s removal turns a winning coalition into a losing one', True), ('A dummy is never critical', True), ('A dictator is critical in every winning coalition', True), ('Every member of every winning coalition is critical', False), ('Critical players must have the largest weight', False)],
          ['Definitions of critical, dummy and dictator.'], 'power_select')
    c = banzhaf_counts(4, [2, 2, 1, 1])
    b.sel(5, 'honors', 'In [4: 2, 2, 1, 1], which statements are true?', [('P1 and P2 have equal Banzhaf power', c[0] == c[1]), ('P3 has positive Banzhaf power', c[2] > 0), ('P1 has exactly twice the power of P3', c[0] == 2 * c[2]), ('P3 is a dummy', c[2] == 0), ('All four players have equal power', len(set(c)) == 1)],
          ['Critical counts: ' + ', '.join('P%d %d' % (i + 1, x) for i, x in enumerate(c)) + '.'], 'power_select')
    b.orq(5, 'cp2', 'Weighted system [5: 3, 2, 1].',
          [('List the winning coalitions.', '{P1, P2}, {P1, P2, P3}'), ('Which players are critical in {P1, P2}?', 'P1 and P2'), ('Which players are critical in {P1, P2, P3}?', 'P1 and P2'), ('Is P3 a dummy?', 'Yes')],
          ['Totals ≥ 5: 3+2 and 3+2+1; 3+1 = 4 loses.', 'Both needed.', 'P3 can leave.', 'Never critical.'], 'power_or')
    assert banzhaf_counts(5, [3, 2, 1]) == [2, 2, 0]
    c = banzhaf_counts(6, [4, 3, 2])
    b.orq(5, 'cp1', 'Weighted system [6: 4, 3, 2].',
          [('List the winning coalitions.', '{P1, P2}, {P1, P3}, {P1, P2, P3}'), ('Count critical appearances for each player.', 'P1 %d, P2 %d, P3 %d' % tuple(c)), ('Find the Banzhaf indices.', ', '.join(frac(Fraction(x, sum(c))) for x in c)),
           ('Compare with the weights 4 : 3 : 2.', 'P2 and P3 have equal power despite different weights.')],
          ['Totals ≥ 6.', 'Removal test.', 'Divide by total.', 'Weight ≠ power.'], 'power_or')
    s = shapley(10, [6, 4, 3, 1])
    b.orq(5, 'honors', 'Weighted system [10: 6, 4, 3, 1].',
          [('How many orderings (sequential coalitions) are there?', '24'), ('Find each Shapley–Shubik index.', ', '.join('P%d %s' % (i + 1, frac(x)) for i, x in enumerate(s))),
           ('Find each Banzhaf index.', ', '.join('P%d %s' % (i + 1, frac(Fraction(x, sum(banzhaf_counts(10, [6, 4, 3, 1]))))) for i, x in enumerate(banzhaf_counts(10, [6, 4, 3, 1])))), ('Do the two indices always agree?', 'No; they measure power in different ways.')],
          ['4!.', 'Pivotal counts / 24.', 'Critical counts / total.', 'Different models.'], 'power_or')


# ---------------------------------------------------------------- 6. fair division
def knaster(bids):
    """bids: dict player -> list of bids per item. Returns final settlement (items, cash) per player."""
    P = list(bids)
    n = len(P)
    m = len(next(iter(bids.values())))
    winner = [max(P, key=lambda p: bids[p][j]) for j in range(m)]
    fair = {p: Fraction(sum(bids[p]), n) for p in P}
    got = {p: sum(bids[p][j] for j in range(m) if winner[j] == p) for p in P}
    first = {p: fair[p] - got[p] for p in P}  # positive = receives cash
    surplus = -sum(first.values())
    final = {p: first[p] + surplus / n for p in P}
    return winner, fair, first, surplus, final


def s6(b):
    KN = [('cp1', {'Ann': [300, 120], 'Ben': [240, 180]}, ['house', 'car']),
          ('honors', {'Ana': [600, 200, 90], 'Bo': [450, 300, 120], 'Cy': [500, 240, 60]}, ['cabin', 'boat', 'piano']),
          ('cp2', {'Kim': [80], 'Lee': [60]}, ['bike']),
          ('honors', {'P': [12000, 3000], 'Q': [10000, 5000], 'R': [9000, 4500]}, ['car', 'jewelry'])]
    for L, bids, items in KN:
        w, fair, first, surplus, final = knaster(bids)
        P = list(bids)
        p0 = P[0]
        fs = final[p0]
        desc = '\n'.join('%s bids: %s' % (p, ', '.join('%s $%d' % (items[j], bids[p][j]) for j in range(len(items)))) for p in P)
        b.sa(6, L, 'Method of sealed bids (Knaster), heirs share equally:\n%s\nAfter the surplus is split equally, how much cash does %s receive (positive) or pay (negative) in total? Answer in dollars, e.g. 45 or -30 (use a fraction a/b if needed).' % (desc, p0),
             frac(fs), ['Each item goes to the highest bidder; each fair share = (sum of own bids)/%d.' % len(P), 'Fair shares: ' + ', '.join('%s $%s' % (p, frac(fair[p])) for p in P) + '.',
                        'First settlement (fair share − value of items won): ' + ', '.join('%s %s' % (p, frac(first[p])) for p in P) + '; surplus $%s split equally.' % frac(surplus),
                        'Final cash: ' + ', '.join('%s %s' % (p, frac(final[p])) for p in P) + '.'], 'sealed_bids')
    DC = [('cp2', 'In the divider-chooser method for two people, who should divide?', 'Either person; the other chooses first', ['The person who values the item more', 'Both divide together', 'A third person always divides']),
          ('cp2', 'Why does the divider-chooser method give each person a fair share?', 'The divider makes two pieces worth exactly half to them; the chooser takes a piece worth at least half to them', ['Both pieces are physically equal', 'The chooser always gets more', 'The divider gets the bigger piece']),
          ('cp1', 'In the lone-divider method with 3 players, the divider cuts the cake into 3 pieces. What must be true for the divider?', 'Each piece is worth exactly 1/3 of the cake to the divider', ['The pieces are the same size', 'One piece is worth half', 'The choosers approve every piece']),
          ('cp1', 'The method of markers is designed for ...', 'Discrete items that can be lined up in a row and not cut', ['A cake that can be cut anywhere', 'Items with sealed cash bids', 'Two players only']),
          ('honors', 'A fair-division method is "proportional" with N players when ...', 'Each player receives a share worth at least 1/N of the total in their own opinion', ['Each player receives exactly the same physical amount', 'No player envies another player\'s share', 'The total value is maximized']),
          ('honors', 'Which method requires each player to have enough cash to pay for items?', 'Method of sealed bids', ['Method of markers', 'Divider-chooser', 'Lone divider'])]
    for L, t, good, bad in DC:
        b.mc(6, L, t, good, bad, ['Fair division: each player should receive a share they value at least 1/N of the total (their own values).', good], 'fair_division_concept')
    VAL = [('cp2', 'A cake is half chocolate, half vanilla. Ana values chocolate 3 times as much as vanilla (per amount). What percent of the whole cake (by Ana\'s values) is the chocolate half?', '75%'),
           ('cp1', 'A cake is half chocolate and half strawberry, worth $12 to Ben: he values chocolate twice as much as strawberry per amount. What is the chocolate half worth to Ben?', '$8'),
           ('honors', 'A $18 cake is 1/3 chocolate and 2/3 vanilla. Cara values chocolate 4 times as much as vanilla per amount. What is a piece containing all the vanilla worth to her?', '$6')]
    for L, t, a in VAL:
        b.sa(6, L, t, a, ['Set the value per unit amount of each part and scale so the total value is correct.', a], 'fair_values')
    assert Fraction(3 * 1, 3 * 1 + 1) == Fraction(3, 4) and 12 * Fraction(2, 3) == 8 and 18 * Fraction(2, 6) == 6
    b.sel(6, 'cp1', 'Which are discrete fair-division methods (items that cannot be cut)?', [('Method of sealed bids', True), ('Method of markers', True), ('Lone divider', False), ('Divider-chooser', False), ('Last diminisher', False)],
          ['Sealed bids and markers handle indivisible items; the others divide continuous objects.'], 'fair_select')
    b.sel(6, 'cp2', 'Ann and Ben share a pizza with divider-chooser; Ann divides. Which statements are true?', [('Ann cuts two pieces she values equally', True), ('Ben picks the piece he likes better', True), ('Each gets at least half by their own values', True), ('Ben must take the smaller piece', False), ('Ann chooses first', False)],
          ['Divider-chooser guarantees each a fair share.'], 'fair_select')
    b.sel(6, 'honors', 'In a sealed-bid division, which statements are always true?', [('Each item goes to its highest bidder', True), ('The surplus is nonnegative', True), ('Each player receives at least their fair share by their own bids', True), ('Each player gets at least one item', False), ('Cash payments always cancel to zero before the surplus', False)],
          ['The highest bidder rule makes the total value of items ≥ the sum of fair shares, giving a surplus ≥ 0.'], 'fair_select')
    w, fair, first, surplus, final = knaster({'Ann': [300, 120], 'Ben': [240, 180]})
    b.orq(6, 'cp1', 'Sealed bids for two heirs: Ann bids house $300 and car $120; Ben bids house $240 and car $180.',
          [('Who gets each item?', 'Ann gets the house; Ben gets the car.'), ('Find each fair share.', 'Ann $%s, Ben $%s' % (frac(fair['Ann']), frac(fair['Ben']))),
           ('Find the surplus.', '$' + frac(surplus)), ('State the final settlement.', 'Ann gets the house and pays $%s; Ben gets the car and $%s' % (frac(-final['Ann']), frac(final['Ben'])))],
          ['Highest bidder.', 'Sum of own bids / 2.', 'Cash left after first settlement.', 'Split surplus equally.'], 'fair_or')
    b.orq(6, 'cp2', 'Two friends share a sandwich with divider-chooser.',
          [('What does the divider try to do?', 'Cut two pieces that are equal in the divider\'s own opinion.'), ('What does the chooser do?', 'Takes the piece the chooser prefers.'), ('Why is the divider satisfied?', 'Either piece is worth half to the divider.'), ('Why is the chooser satisfied?', 'The chosen piece is worth at least half to the chooser.')],
          ['Divide.', 'Choose.', 'Equal halves.', 'Best of two.'], 'fair_or')
    b.orq(6, 'honors', 'Method of markers with 3 players and 9 items in a row; each player places 2 markers dividing the row into 3 segments they value equally.',
          [('What is the first step after markers are placed?', 'Find the leftmost first marker; that player gets the items left of it.'), ('What happens to that player\'s other markers?', 'They are removed.'),
           ('How are leftover items handled?', 'Items not given out are shared by lottery or another method.'), ('State one requirement of the method.', 'Many more items than players, and items that can be arranged in a row.')],
          ['Leftmost first marker.', 'Remove.', 'Leftovers.', 'Assumptions.'], 'fair_or')


# ---------------------------------------------------------------- 7. apportionment
def hamilton(pops, seats):
    tot = sum(pops)
    q = [Fraction(p * seats, tot) for p in pops]
    a = [math.floor(x) for x in q]
    left = seats - sum(a)
    order = sorted(range(len(pops)), key=lambda i: q[i] - a[i], reverse=True)
    for i in order[:left]:
        a[i] += 1
    return a, q


def divisor(pops, seats, kind):
    """Jefferson (D'Hondt), Webster (Sainte-Laguë) and Adams by priority values."""
    a = [1 if kind == 'adams' else 0] * len(pops)
    while sum(a) < seats:
        def pr(i):
            k = a[i]
            return Fraction(pops[i], {'jefferson': k + 1, 'webster': 2 * k + 1, 'adams': k}[kind] or 1) * (2 if kind == 'webster' else 1)
        i = max(range(len(pops)), key=lambda i: (pr(i), -i))
        a[i] += 1
    return a


APP = [('cp2', [450, 330, 220], 10, ['North', 'East', 'South']), ('cp1', [1320, 1055, 625], 30, ['A', 'B', 'C']), ('cp1', [5200, 3800, 1000], 20, ['P', 'Q', 'R']),
       ('honors', [2540, 3580, 1880], 25, ['X', 'Y', 'Z']), ('honors', [1646, 6936, 6238, 1180], 50, ['A', 'B', 'C', 'D'])]


def s7(b):
    for L, pops, seats, names in APP:
        sd = Fraction(sum(pops), seats)
        a, q = hamilton(pops, seats)
        txt = ', '.join('%s %d' % (n, p) for n, p in zip(names, pops))
        b.sa(7, L, 'Populations: %s; %d seats. Use Hamilton\'s method (floor the standard quotas, then give leftover seats by largest remainder). Give the apportionment in the order listed, e.g. 4, 3, 3.' % (txt, seats),
             ', '.join(map(str, a)), ['Standard divisor = %d/%d = %s.' % (sum(pops), seats, frac(sd)), 'Standard quotas: ' + ', '.join('%.3f' % float(x) for x in q) + '.', 'Apportionment: ' + ', '.join(map(str, a))], 'hamilton')
    for L, pops, seats, names, kind in (('cp1', APP[1][1], 30, APP[1][3], 'jefferson'), ('honors', APP[3][1], 25, APP[3][3], 'webster'), ('honors', APP[4][1], 50, APP[4][3], 'jefferson'), ('cp1', APP[2][1], 20, APP[2][3], 'webster'), ('honors', APP[3][1], 25, APP[3][3], 'adams')):
        a = divisor(pops, seats, kind)
        rule = {'jefferson': "Jefferson's method (round every modified quota DOWN)", 'webster': "Webster's method (round every modified quota to the nearest whole number)", 'adams': "Adams's method (round every modified quota UP)"}[kind]
        txt = ', '.join('%s %d' % (n, p) for n, p in zip(names, pops))
        b.sa(7, L, 'Populations: %s; %d seats. Use %s. Give the apportionment in the order listed.' % (txt, seats, rule), ', '.join(map(str, a)),
             ['Find a modified divisor so that the rounded quotas add to %d.' % seats, 'Apportionment (checked with the equivalent priority-value method): ' + ', '.join(map(str, a))], 'divisor_method')
    for L, pops, seats, names in APP[:3]:
        sd = Fraction(sum(pops), seats)
        b.sa(7, L, 'Populations: %s; %d seats. Find the standard divisor (total population ÷ seats). Give an exact number or fraction.' % (', '.join('%s %d' % (n, p) for n, p in zip(names, pops)), seats), frac(sd),
             ['Standard divisor = %d ÷ %d.' % (sum(pops), seats), frac(sd)], 'standard_divisor')
    b.sel(7, 'cp1', 'Which apportionment methods use a modified divisor?', [("Jefferson's method", True), ("Webster's method", True), ("Adams's method", True), ("Hamilton's method", False), ('Plurality', False)],
          ['Hamilton uses the standard divisor with largest remainders.'], 'apportion_select')
    b.sel(7, 'cp2', 'Standard quotas are 4.6, 3.2 and 2.2 (10 seats). Which statements are true?', [('Lower quotas are 4, 3, 2', True), ('One seat is left after the lower quotas', True), ("Hamilton gives the extra seat to the state with quota 4.6", True), ('Upper quotas are 4, 3, 2', False), ('Every state gets its upper quota', False)],
          ['4 + 3 + 2 = 9, one seat left; largest remainder 0.6.'], 'apportion_select')
    b.sel(7, 'honors', 'Which statements about apportionment methods are true?', [('Hamilton\'s method satisfies the quota rule', True), ('Jefferson\'s method can violate the upper quota', True), ('Adams\'s method can violate the lower quota', True), ('Webster\'s method never violates quota', False), ('Hamilton\'s method is free of the Alabama paradox', False)],
          ['Hamilton always gives lower or upper quota but suffers paradoxes; divisor methods avoid paradoxes but can violate quota.'], 'apportion_select')
    pops, seats = [450, 330, 220], 10
    a, q = hamilton(pops, seats)
    b.orq(7, 'cp2', 'Three towns with populations 450, 330, 220 share 10 seats.',
          [('Find the standard divisor.', '100'), ('Find the standard quotas.', '4.5, 3.3, 2.2'), ('Find the lower quotas and seats left over.', '4, 3, 2; 1 seat left'), ('Apportion with Hamilton\'s method.', ', '.join(map(str, a)))],
          ['1000/10.', 'Population ÷ 100.', 'Floors.', 'Largest remainder 0.5.'], 'apportion_or')
    pops = [1320, 1055, 625]
    b.orq(7, 'cp1', 'Populations 1320, 1055, 625; 30 seats.',
          [('Find the standard divisor.', '100'), ('Find the standard quotas.', '13.2, 10.55, 6.25'), ('Hamilton apportionment.', ', '.join(map(str, hamilton(pops, 30)[0]))), ('Jefferson apportionment.', ', '.join(map(str, divisor(pops, 30, 'jefferson'))))],
          ['3000/30.', 'Divide.', 'Largest remainders.', 'Modified divisor rounding down.'], 'apportion_or')
    pops = [2540, 3580, 1880]
    b.orq(7, 'honors', 'Populations 2540, 3580, 1880; 25 seats.',
          [('Standard quotas (3 decimals).', ', '.join('%.3f' % float(Fraction(p * 25, sum(pops))) for p in pops)), ('Hamilton.', ', '.join(map(str, hamilton(pops, 25)[0]))), ('Webster.', ', '.join(map(str, divisor(pops, 25, 'webster')))), ('Adams.', ', '.join(map(str, divisor(pops, 25, 'adams'))))],
          ['Standard divisor 320.', 'Largest remainder.', 'Round to nearest with a modified divisor.', 'Round up with a modified divisor.'], 'apportion_or')


# ---------------------------------------------------------------- 8. comparing fairness and outcomes
def s8(b):
    PAR = [('cp2', 'Increasing the total number of seats causes a state to LOSE a seat. This is the ...', 'Alabama paradox', ['Population paradox', 'New-states paradox', 'Quota rule']),
           ('cp1', 'State A grows faster than state B, yet A loses a seat to B. This is the ...', 'Population paradox', ['Alabama paradox', 'New-states paradox', 'Condorcet paradox']),
           ('cp1', 'Adding a new state with its fair share of seats changes the other states\' apportionments. This is the ...', 'New-states paradox', ['Alabama paradox', 'Population paradox', 'Majority paradox']),
           ('honors', 'An apportionment gives a state a number of seats that is neither its lower nor its upper quota. This violates the ...', 'Quota rule', ['Alabama paradox', 'Monotonicity criterion', 'Majority criterion'])]
    for L, t, good, bad in PAR:
        b.mc(8, L, t, good, bad, ['Know the three paradoxes and the quota rule.', good], 'paradox')
    # computed Alabama paradox example (found by search; checked here)
    pops = [130, 690, 410]
    a10, _ = hamilton(pops, 13)
    a11, _ = hamilton(pops, 14)
    lost = [i for i in range(3) if a11[i] < a10[i]]
    assert lost == [0]
    b.sa(8, 'honors', 'Populations: A 130, B 690, C 410. Hamilton gives %s with 13 seats. Find the Hamilton apportionment with 14 seats (order A, B, C).' % ', '.join(map(str, a10)), ', '.join(map(str, a11)),
         ['Recompute the standard quotas with 14 seats (divisor 1230/14) and apply largest remainders.', '14 seats: %s. State A loses a seat although the house grew: the Alabama paradox.' % ', '.join(map(str, a11))], 'alabama')
    b.mc(8, 'cp1', 'Populations A 130, B 690, C 410. Hamilton gives %s with 13 seats and %s with 14 seats. Which paradox occurs?' % (', '.join(map(str, a10)), ', '.join(map(str, a11))),
         'Alabama paradox', ['Population paradox', 'New-states paradox', 'No paradox'], ['Compare state by state: A drops from 2 to 1 when the number of seats increases.'], 'alabama')
    QV = [('cp2', 'Which method never violates the quota rule?', "Hamilton's method", ["Jefferson's method", "Adams's method", "Webster's method"]),
          ('cp1', 'Which methods are immune to the Alabama paradox?', 'All divisor methods (Jefferson, Adams, Webster)', ["Hamilton's method only", 'No method', 'Plurality']),
          ('honors', 'The Balinski–Young theorem says ...', 'No apportionment method both satisfies the quota rule and avoids all paradoxes', ['Hamilton\'s method is always best', 'Divisor methods always satisfy quota', 'Every method has the Alabama paradox'])]
    for L, t, good, bad in QV:
        b.mc(8, L, t, good, bad, ['Quota rule vs paradoxes: a trade-off (Balinski–Young).', good], 'method_tradeoff')
    # quota violation computed: Jefferson exceeding upper quota (found by search; checked here)
    pops = [5100, 1600, 1500, 1200]
    j = divisor(pops, 20, 'jefferson')
    q = [Fraction(p * 20, sum(pops)) for p in pops]
    viol = [i for i in range(4) if not (math.floor(q[i]) <= j[i] <= math.ceil(q[i]))]
    assert viol == [0] and j == [12, 3, 3, 2]
    b.sa(8, 'honors', 'Populations 5100, 1600, 1500, 1200; 20 seats. Jefferson\'s method gives %s. How many states receive a number of seats outside their lower/upper quota?' % ', '.join(map(str, j)), len(viol),
         ['Standard quotas: ' + ', '.join('%.3f' % float(x) for x in q) + '.', 'The largest state gets 12 seats although its upper quota is 11: one quota violation (Jefferson favors large states).'], 'quota_violation')
    CMP = [('cp2', 'Plurality chooses A, Borda chooses B. What does this show?', 'Different reasonable methods can produce different winners', ['One of the counts must contain an error', 'The election must be repeated', 'B must have a majority']),
           ('cp1', 'Why might a city choose instant runoff instead of plurality?', 'It ensures the winner has a majority of the remaining votes and reduces "spoiler" effects', ['It always chooses the Condorcet winner', 'It satisfies every fairness criterion', 'It is quicker to count by hand']),
           ('honors', 'Which statement best summarizes Arrow\'s theorem for ranked voting with 3 or more candidates?', 'No method satisfies all of a short list of fairness conditions at once', ['Plurality is the fairest method', 'Pairwise comparisons satisfy every criterion', 'Every method is a dictatorship'])]
    for L, t, good, bad in CMP:
        b.mc(8, L, t, good, bad, ['Methods trade off fairness criteria.', good], 'compare_outcomes')
    b.sel(8, 'cp1', 'Which are paradoxes of Hamilton\'s method?', [('Alabama paradox', True), ('Population paradox', True), ('New-states paradox', True), ('Quota rule violation', False), ('Condorcet paradox', False)],
          ['Hamilton satisfies quota but can show all three paradoxes.'], 'paradox_select')
    b.sel(8, 'cp2', 'Which statements about choosing a voting method are reasonable?', [('Different methods can give different winners', True), ('Each method can fail some fairness criterion', True), ('The method should be chosen before the votes are counted', True), ('The method with the most criteria always wins', False), ('Plurality never fails any criterion', False)],
          ['Choosing a method involves trade-offs and should be decided in advance.'], 'paradox_select')
    b.sel(8, 'honors', 'Which pairings of method and possible flaw are correct?', [('Jefferson — can violate upper quota', True), ('Adams — can violate lower quota', True), ('Hamilton — Alabama paradox', True), ('Webster — Alabama paradox', False), ('Borda — Condorcet criterion always satisfied', False)],
          ['Divisor methods avoid the Alabama paradox; Borda can violate Condorcet.'], 'paradox_select')
    a10, _ = hamilton([130, 690, 410], 13)
    a11, _ = hamilton([130, 690, 410], 14)
    b.orq(8, 'cp1', 'Populations A 130, B 690, C 410 (1230 total).',
          [('Hamilton with 13 seats.', ', '.join(map(str, a10))), ('Hamilton with 14 seats.', ', '.join(map(str, a11))), ('Which state lost a seat?', 'A'), ('Name the paradox.', 'Alabama paradox')],
          ['Standard quotas with divisor 1230/13: 1.374, 7.293, 4.333.', 'With divisor 1230/14: 1.480, 7.854, 4.667.', 'A: 2 → 1.', 'More seats, fewer for one state.'], 'paradox_or')
    b.orq(8, 'cp2', 'A school compares plurality and Borda for electing a class president.',
          [('What does plurality use from each ballot?', 'Only the first choice.'), ('What does Borda use?', 'The whole ranking.'), ('Give one advantage of plurality.', 'Simple to understand and count.'), ('Give one advantage of Borda.', 'It rewards broadly acceptable candidates.')],
          ['First choices.', 'Points for each rank.', 'Simplicity.', 'Consensus.'], 'compare_or')
    b.orq(8, 'honors', 'Evaluate the methods for this preference schedule:\n' + schedule_text(SCHED['e6']),
          [('Plurality winner and whether it is a Condorcet loser.', '%s; %s' % (plurality(SCHED['e6'])[0], 'yes' if all(head(SCHED['e6'], 'P', c)[0] < head(SCHED['e6'], 'P', c)[1] for c in 'QR') else 'no')),
           ('Borda winner.', borda(SCHED['e6'])[0]), ('Condorcet winner, if any.', condorcet(SCHED['e6']) or 'none'), ('Recommend a method and justify with a fairness criterion.', 'Pairwise or Borda here, because plurality elects a candidate most voters rank last (it fails Condorcet).')],
          explain('borda', SCHED['e6'])[1] + explain('pairwise', SCHED['e6'])[1], 'compare_or')


def topup(b):
    need = lambda k, L: b.counter.get((k, L), 0) < 10
    rng = seeded('u9top')
    orders = list(itertools.permutations('ABC'))
    for k in range(1, 9):
        for L in ('cp2', 'cp1', 'honors'):
            g = 0
            while need(k, L) and g < 40:
                g += 1
                S = [(rng.randint(2, 12), orders[i]) for i in rng.sample(range(6), 4)]
                if any(q['prompt'].find(schedule_text(S)) >= 0 for q in b.q):
                    continue
                if k in (1, 2, 3, 8):
                    m = {1: 'plurality', 2: rng.choice(['borda', 'irv', 'pairwise']), 3: 'pairwise', 8: rng.choice(['plurality', 'borda'])}[k]
                    w, steps = explain(m, S)
                    if w is None:
                        continue
                    if k == 3:
                        cw = condorcet(S)
                        good = ('Yes, ' + cw) if cw else 'No Condorcet winner'
                        b.mc(3, L, 'Preference schedule:\n%s\nIs there a Condorcet winner? If so, who?' % schedule_text(S), good, [x for x in ['Yes, A', 'Yes, B', 'Yes, C', 'No Condorcet winner'] if x != good],
                             ['%s vs %s: %d–%d' % (a, c, *head(S, a, c)) for a, c in itertools.combinations('ABC', 2)], 'condorcet_check')
                    else:
                        b.mc(k, L, 'Preference schedule:\n%s\nWho wins by %s?' % (schedule_text(S), NAME[m]), w, [c for c in 'ABC' if c != w] + ['There is a tie'], steps, 'method_winner')
                elif k in (4, 5):
                    w = sorted(rng.sample(range(1, 10), rng.choice([3, 4])), reverse=True)
                    q = sum(w) // 2 + 1 + rng.randint(0, 2)
                    if any(x == sys_txt(q, w) for x in [qq['prompt'][qq['prompt'].find('['):qq['prompt'].find(']') + 1] for qq in b.q]):
                        continue
                    if k == 4:
                        n = sum(1 for r in range(1, len(w) + 1) for c in itertools.combinations(range(len(w)), r) if winning(q, w, c))
                        num_mc(b, 4, L, 'How many winning coalitions does %s have?' % sys_txt(q, w), n, [n + 1, n - 1, 2 ** len(w) - 1], ['List coalitions meeting the quota.', '%d' % n], 'count_winning')
                    else:
                        c = banzhaf_counts(q, w)
                        if sum(c) == 0:
                            continue
                        b.mc(5, L, 'In %s, what is the Banzhaf power index of P1?' % sys_txt(q, w), frac(Fraction(c[0], sum(c))),
                             list(dict.fromkeys(x for x in [frac(Fraction(w[0], sum(w))), frac(Fraction(1, len(w))), frac(Fraction(c[0] + 1, sum(c) + 1)), frac(Fraction(c[0], sum(c) + 2))] if x != frac(Fraction(c[0], sum(c))))),
                             ['Critical counts: ' + ', '.join('P%d %d' % (i + 1, x) for i, x in enumerate(c)) + '.', 'Index = %d/%d.' % (c[0], sum(c))], 'banzhaf')
                elif k == 6:
                    x, y = rng.randint(2, 9) * 10, rng.randint(2, 9) * 10
                    if x == y:
                        continue
                    hi = max(x, y)
                    fair_k, fair_l = Fraction(x, 2), Fraction(y, 2)
                    winner = 'Kim' if x > y else 'Lee'
                    first_w = (fair_k if winner == 'Kim' else fair_l) - hi
                    first_o = fair_l if winner == 'Kim' else fair_k
                    surplus = -(first_w + first_o)
                    pay = -(first_w + surplus / 2)
                    b.sa(6, L, 'Kim and Lee inherit one bike and use sealed bids: Kim bids $%d, Lee bids $%d. After the surplus is shared equally, how much does the winner pay the other person? Answer in dollars.' % (x, y), frac(pay),
                         ['The higher bidder (%s) gets the bike. Fair shares: Kim $%s, Lee $%s.' % (winner, frac(fair_k), frac(fair_l)),
                          'First settlement: the winner owes the other person that person\'s fair share, $%s. Surplus = $%s, split equally.' % (frac(first_o), frac(surplus)),
                          'Payment = $%s + $%s = $%s.' % (frac(first_o), frac(surplus / 2), frac(pay))], 'sealed_bids')
                elif k == 7:
                    pops = [rng.randint(10, 90) * 10 for _ in range(3)]
                    seats = rng.choice([10, 12, 15])
                    a, qq = hamilton(pops, seats)
                    txt = ', '.join('%s %d' % (n, p) for n, p in zip('ABC', pops))
                    b.sa(7, L, 'Populations: %s; %d seats. Use Hamilton\'s method. Give the apportionment in the order A, B, C.' % (txt, seats), ', '.join(map(str, a)),
                         ['Standard quotas: ' + ', '.join('%.3f' % float(x) for x in qq) + '.', 'Floors then largest remainders: ' + ', '.join(map(str, a))], 'hamilton')


def errors(b):
    assert divisor([1320, 1055, 625], 30, 'jefferson') == [13, 11, 6]
    E = b.err
    S = SCHED['e5']
    E(1, 'cp2', 'With 24 voters, how many votes is a majority?', 'Jordan', ['Half of 24 is 12, so a majority is 12.'],
      '13', 'Jordan used half instead of MORE than half. 12 is a tie, not a majority.', 'Majority means more than half.', ['24/2 = 12, so 13.'], 'majority_half_error')
    E(2, 'cp2', 'Schedule: 5 A>B>C, 4 B>C>A, 3 C>A>B. Find A\'s Borda points (3-2-1).', 'Sam', ['A is first on 5 ballots: 5·3 = 15.'],
      str(borda(S)[1]['A']), 'Sam counted only first-place points. A also earns 1 point on the 4 B>C>A ballots and 2 points on the 3 C>A>B ballots.', 'Borda uses every position.', ['5·3 + 4·1 + 3·2 = 25.'], 'borda_first_only_error')
    E(2, 'cp2', 'Plurality winner of: 9 A>B>C, 8 B>C>A, 7 C>B>A.', 'Riley', ['B is ranked in the top two by everyone, so B wins plurality.'],
      'A', 'Riley used rankings beyond first place. Plurality counts only first-place votes.', 'A has 9 first-place votes, the most.', ['A 9, B 8, C 7.'], 'plurality_rank_error')
    E(4, 'cp2', 'In [6: 4, 3, 2], does P1 have veto power?', 'Casey', ['P1 has the largest weight, so P1 can veto.'],
      'Yes, because 3 + 2 = 5 < 6', 'Casey reached the right answer for the wrong reason. Veto power depends on whether the others can reach the quota without P1, not on size alone.', 'In [5: 4, 3, 2], P1 would have no veto.', ['Others total 5 < 6.'], 'veto_reason_error')
    E(7, 'cp2', 'Quotas 3.4, 4.3, 2.3 (10 seats). Apportion with Hamilton\'s method.', 'Avery', ['Round each: 3, 4, 2 = 9 seats. Done.'],
      '4, 4, 2', 'Avery stopped with 9 seats. Hamilton gives the leftover seat to the largest remainder (0.4).', 'All seats must be assigned.', ['Lower quotas 3, 4, 2; remainder 0.4 is largest.'], 'leftover_seat_error')
    E(6, 'cp2', 'Divider-chooser: Ann cuts; who chooses first?', 'Morgan', ['Ann cut, so Ann chooses first.'],
      'Ben (the chooser) picks first', 'Morgan reversed the roles. If the divider chose, the chooser could be left with a piece worth less than half.', 'The chooser\'s first pick protects the chooser.', ['Divider cuts, chooser picks.'], 'divider_choose_error')
    E(2, 'cp1', 'IRV winner of: 8 A>B>C, 7 B>C>A, 6 C>B>A.', 'Taylor', ['A has the most first-place votes, so A wins.'],
      irv([(8, ('A', 'B', 'C')), (7, ('B', 'C', 'A')), (6, ('C', 'B', 'A'))])[0], 'Taylor used plurality. No one has a majority (11), so C is eliminated and C\'s 6 votes go to B.', 'IRV continues until someone has a majority.', ['Round 2: A 8, B 13.'], 'irv_stop_error')
    E(5, 'cp1', 'In [5: 3, 2, 1], find P3\'s Banzhaf index.', 'Jamie', ['P3 is in the winning coalition {P1, P2, P3}, so P3 has some power: 1/5.'],
      '0', 'Jamie counted membership instead of being critical. Removing P3 from {P1, P2, P3} still leaves 5, a win.', 'Power = number of times critical.', ['P3 is never critical: a dummy.'], 'member_critical_error')
    E(3, 'cp1', 'Schedule: 4 A>B>C, 3 B>C>A, 2 C>B>A. Is A the Condorcet winner?', 'Quinn', ['A has the most first-place votes, so A is the Condorcet winner.'],
      'No; B is the Condorcet winner (B beats A 5–4 and C 7–2)', 'Quinn confused plurality with Condorcet. A Condorcet winner must win every head-to-head.', 'Compare pairs.', ['A vs B: 4–5.'], 'condorcet_plurality_error')
    E(7, 'cp1', 'Populations 1320, 1055, 625; 30 seats. Jefferson.', 'Alex', ['Standard quotas 13.2, 10.55, 6.25 round down to 13, 10, 6 = 29. Give the last seat to B (largest remainder).'],
      ', '.join(map(str, divisor([1320, 1055, 625], 30, 'jefferson'))), 'Alex mixed Hamilton\'s largest-remainder step into Jefferson\'s method. Jefferson lowers the divisor until the rounded-down quotas total 30.', 'Divisor methods change the divisor, not the remainders.', ['Try d = 96: 13.75, 10.99, 6.51 → 13, 10, 6 = 29; d = 94: 14.04, 11.22, 6.65 → 14, 11, 6 = 31; d = 95.5 gives 13.82, 11.05, 6.54 → 13, 11, 6 = 30.'], 'divisor_mix_error')
    d_, v_, dm_ = players_info(7, [5, 3, 1])
    assert d_ == [] and v_ == [0, 1] and dm_ == [2]
    E(4, 'cp1', 'In [7: 5, 3, 1], identify any dictator, veto players and dummies.', 'Jordan', ['P1 has the largest weight, so P1 is a dictator and the others have no power.'],
      'No dictator; P1 and P2 have veto power; P3 is a dummy', 'Jordan equated "largest weight" with "dictator". A dictator needs weight ≥ quota, and 5 < 7.', 'Check each definition against the quota.', ['Without P1: 4 < 7; without P2: 6 < 7, so both have veto.', 'P3 is never critical.'], 'dictator_def_error')
    E(6, 'cp1', 'Sealed bids, two heirs: Ann bids $300 on a car, Ben $240. Who gets the car and what is Ann\'s fair share?', 'Sam', ['Ben gets the car because his bid is cheaper. Ann\'s fair share is $300.'],
      'Ann gets the car; her fair share is $150', 'Sam gave the item to the lower bid and forgot to divide by the number of heirs.', 'Highest bid wins; fair share = own total bids ÷ number of heirs.', ['Ann: 300/2 = 150.'], 'sealed_bid_error')
    E(8, 'honors', 'With 10 seats Hamilton gives 3, 3, 3, 1; with 11 seats it gives 4, 4, 2, 1. Name the paradox.', 'Riley', ['The population paradox, because the third state lost a seat.'],
      'Alabama paradox', 'Riley named the wrong paradox. The populations did not change; the number of seats increased.', 'Alabama: more seats; population: population changes; new-states: a new state.', ['State C went from 3 to 2 when seats increased.'], 'paradox_name_error')
    E(2, 'honors', 'Pairwise comparisons: A beats B, B beats C, C beats A. Who wins?', 'Casey', ['A, because A beat B first.'],
      'Three-way tie (1 point each)', 'Casey used the order of comparisons. Each candidate has one win, so the method gives a tie and needs a stated tie-breaker.', 'Condorcet cycle.', ['Points: A 1, B 1, C 1.'], 'cycle_error')
    E(5, 'honors', 'In [10: 6, 4, 3, 1], find P4\'s Shapley–Shubik index.', 'Avery', ['P4 has weight 1 of 14, so 1/14.'],
      frac(shapley(10, [6, 4, 3, 1])[3]), 'Avery used the weight ratio. Shapley–Shubik counts orderings in which P4 is pivotal.', 'Weight is not power.', ['P4 is pivotal in ' + str(int(shapley(10, [6, 4, 3, 1])[3] * 24)) + ' of 24 orderings.'], 'shapley_weight_error')
    E(3, 'honors', 'Borda elects B though A has 3 of 5 first-place votes. Which criterion fails?', 'Morgan', ['The Condorcet criterion fails.'],
      'The majority criterion (A has a majority of first-place votes); A is also the Condorcet winner, so Condorcet fails too', 'Morgan named only the Condorcet criterion. A majority candidate is automatically a Condorcet winner, so the majority criterion is the primary violation.', 'Majority ⇒ Condorcet winner.', ['A beats every candidate head-to-head 3–2.'], 'criterion_name_error')
    E(7, 'honors', 'Webster\'s method: modified quotas 4.5, 3.49, 2.51 with 10 seats. Is the divisor correct?', 'Jamie', ['Round down: 4, 3, 2 = 9, so lower the divisor.'],
      'No: Webster rounds to the nearest whole number, giving 5, 3, 3 = 11 seats, so the divisor must be RAISED', 'Jamie used Jefferson\'s rounding. Webster rounds to the nearest whole number (4.5 → 5, 2.51 → 3), totaling 11, so the divisor must increase.', 'Use the rounding rule of the named method.', ['Nearest: 5 + 3 + 3 = 11 > 10.'], 'webster_round_error')
    E(6, 'honors', 'Lone divider with 3 players: the divider cuts pieces s1, s2, s3. Chooser 1 bids only s1; chooser 2 bids only s1. What happens?', 'Taylor', ['Chooser 1 gets s1 because they bid first; chooser 2 gets s2.'],
      'The divider takes s2 or s3; the other unwanted piece is returned to s1, and choosers 1 and 2 divide that combined piece by divider-chooser', 'Taylor gave chooser 2 a piece chooser 2 values at less than 1/3.', 'Both choosers value the combination of s1 with an unchosen piece at more than 2/3.', ['Standoff resolution in the lone-divider method.'], 'lone_divider_error')
