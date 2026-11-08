"""Unit 2: The Logic of Compound Statements (8 skills). Every truth value, column, equivalence and validity
claim is computed with logic.py."""
from core import Bank, seeded
import logic as LG

U = 'compound-statements-logic'
ORDER2 = 'standard row order (p, q) = TT, TF, FT, FF'
ORDER3 = 'standard row order (p, q, r) = TTT, TTF, TFT, TFF, FTT, FTF, FFT, FFF'


def tvs(env):
    return ', '.join('%s %s' % (k, 'T' if v else 'F') for k, v in env.items())


def build():
    b = Bank(U, 'lg', 8)
    for f in (s1, s2, s3, s4, s5, s6, s7, s8, topup, topup2, topup3, errors):
        f(b)
    return b


def wrongs(col, k=3):
    """Plausible wrong columns: flip one row, complement, and reverse."""
    out = []
    flip = lambda c, i: c[:i] + ('F' if c[i] == 'T' else 'T') + c[i + 1:]
    cands = [''.join('F' if ch == 'T' else 'T' for ch in col), col[::-1]] + [flip(col, i) for i in range(len(col))]
    for c in cands:
        if c != col and c not in out:
            out.append(c)
    return out[:k]


# ---------------------------------------------------------------- 1. negation, conjunction, disjunction
ENG = [  # (English with p,q defined, symbolic, distractors)
    ('p: "It is cold."  q: "It is windy."  Translate: "It is cold and not windy."', 'p ∧ ¬q', ['¬p ∧ q', 'p ∨ ¬q', '¬(p ∧ q)']),
    ('p: "I study."  q: "I pass."  Translate: "I study or I pass, but not both."', '(p ∨ q) ∧ ¬(p ∧ q)', ['p ∨ q', 'p ∧ q', '¬p ∨ ¬q']),
    ('p: "x > 5"  q: "x = 5"  Translate: "x ≥ 5".', 'p ∨ q', ['p ∧ q', '¬p ∨ q', 'p ∧ ¬q']),
    ('p: "The car is fast."  q: "The car is cheap."  Translate: "The car is neither fast nor cheap."', '¬p ∧ ¬q', ['¬p ∨ ¬q', '¬(p ∧ q)', '¬p ∧ q']),
    ('p: "x < 2"  q: "x > 7"  Translate: "2 ≤ x ≤ 7".', '¬p ∧ ¬q', ['¬p ∨ ¬q', 'p ∨ q', '¬(p ∧ q)']),
    ('p: "Sam is home."  q: "Kim is home."  Translate: "It is not true that both Sam and Kim are home."', '¬(p ∧ q)', ['¬p ∧ ¬q', '¬p ∧ q', 'p ∧ ¬q']),
    ('p: "The file is saved."  q: "The file is shared."  Translate: "The file is saved, but it is not shared."', 'p ∧ ¬q', ['p ∨ ¬q', '¬p ∧ q', '¬(p ∨ q)']),
    ('p: "n is even."  q: "n is prime."  r: "n > 2"  Translate: "n is even and prime, and n is not greater than 2."', '(p ∧ q) ∧ ¬r', ['p ∧ (q ∨ ¬r)', '(p ∨ q) ∧ ¬r', '¬(p ∧ q ∧ r)']),
    ('p: "The alarm sounds."  q: "There is smoke."  r: "There is heat."  Translate: "The alarm sounds, and there is smoke or heat."', 'p ∧ (q ∨ r)', ['(p ∧ q) ∨ r', 'p ∨ (q ∧ r)', 'p ∧ q ∧ r']),
]
VALS = [{'p': True, 'q': False}, {'p': False, 'q': True}, {'p': False, 'q': False}, {'p': True, 'q': True}]
FORM1 = {'cp2': ['¬p', 'p ∧ q', 'p ∨ q', '¬p ∨ q', 'p ∧ ¬q'],
         'cp1': ['¬(p ∨ q)', '¬p ∧ ¬q', '(p ∨ q) ∧ ¬p', '¬(p ∧ ¬q)', 'p ∨ (¬p ∧ q)'],
         'honors': ['¬(¬p ∨ q) ∨ (p ∧ ¬q)', '(p ∧ q) ∨ ¬(p ∨ q)', '¬(p ∧ (q ∨ ¬p))', '(p ∨ ¬q) ∧ (¬p ∨ q)', '¬(¬(p ∨ q) ∧ p)']}


def s1(b):
    for L, eng in (('cp2', [0, 3, 6]), ('cp1', [1, 2, 5]), ('honors', [4, 7, 8])):
        for i in eng:
            t, good, bad = ENG[i]
            b.mc(1, L, t, good, bad, ['Match each phrase to a connective: "and/but" → ∧, "or" → ∨ (inclusive), "not/neither" → ¬.', 'Answer: ' + good], 'translate_connectives')
        for k, f in enumerate(FORM1[L]):
            env = VALS[k % 4]
            v = LG.ev(LG.parse(f), env)
            if k < 3:
                b.mc(1, L, 'If %s, what is the truth value of %s?' % (tvs(env), f), 'True' if v else 'False',
                     ['False' if v else 'True', 'Cannot be determined without r', 'Both true and false'],
                     ['Substitute the given values and evaluate inside parentheses first, then ¬, then ∧, then ∨.', '%s is %s.' % (f, 'true' if v else 'false')], 'evaluate_compound')
            else:
                b.sa(1, L, 'Let %s. Find the truth value of %s. Answer T or F.' % (tvs(env), f), 'T' if v else 'F',
                     ['Evaluate step by step with p and q replaced by their values.', '%s = %s' % (f, 'T' if v else 'F')], 'evaluate_compound')
    b.sel(1, 'cp2', 'Suppose p is true and q is false. Which statements are TRUE?',
          [('p ∨ q', True), ('p ∧ q', False), ('¬q', True), ('¬p ∨ q', False), ('p ∧ ¬q', True)],
          ['p ∨ q: T. p ∧ q: F. ¬q: T. ¬p ∨ q: F ∨ F = F. p ∧ ¬q: T ∧ T = T.'], 'select_true')
    env = {'p': False, 'q': True, 'r': False}
    forms = ['p ∨ (q ∧ ¬r)', '¬p ∧ ¬q', '(p ∨ q) ∧ r', '¬(p ∧ r)', 'q ∧ ¬(p ∨ r)']
    b.sel(1, 'cp1', 'Suppose p is false, q is true and r is false. Which statements are TRUE?', [(f, LG.ev(LG.parse(f), env)) for f in forms],
          ['%s → %s' % (f, 'T' if LG.ev(LG.parse(f), env) else 'F') for f in forms], 'select_true')
    b.sel(1, 'honors', 'For which assignments (p, q) is the statement (p ∨ q) ∧ ¬(p ∧ q) TRUE?',
          [(a, LG.ev(LG.parse('(p ∨ q) ∧ ¬(p ∧ q)'), {'p': a[1] == 'T', 'q': a[4] == 'T'})) for a in ['(T, T)', '(T, F)', '(F, T)', '(F, F)']],
          ['This is exclusive or: true when exactly one of p, q is true.'], 'select_assignment')
    b.orq(1, 'cp2', 'Let p: "The store is open" and q: "The lights are on".',
          [('Write "The store is open and the lights are on" in symbols.', 'p ∧ q'), ('Write "The store is not open" in symbols.', '¬p'),
           ('Write ¬p ∨ q in words.', 'The store is not open or the lights are on.'), ('If p is T and q is F, is ¬p ∨ q true or false?', 'False')],
          ['"and" → ∧.', '"not" → ¬.', '∨ is "or".', '¬p = F and q = F, so F ∨ F = F.'], 'translate_or')
    b.orq(1, 'cp1', 'Let p: "x > 0", q: "x < 10" and r: "x is an integer".',
          [('Write "0 < x < 10" in symbols.', 'p ∧ q'), ('Write "x is an integer between 0 and 10 (exclusive)" in symbols.', 'p ∧ q ∧ r'),
           ('Find the truth value of p ∧ q ∧ r when x = 3.5.', 'F (r is false)'), ('Find the truth value of ¬p ∨ r when x = −2.', 'T (¬p is true)')],
          ['Both inequalities must hold.', 'Add r with ∧.', '3.5 is not an integer.', '−2 > 0 is false, so ¬p is true.'], 'inequality_or')
    b.orq(1, 'honors', 'Exclusive or is written p ⊕ q: "p or q, but not both".',
          [('Give the truth column of p ⊕ q in the %s.' % ORDER2, LG.colstr('p ⊕ q')), ('Write p ⊕ q using only ∧, ∨ and ¬.', '(p ∨ q) ∧ ¬(p ∧ q)'),
           ('Is p ⊕ q equivalent to ¬(p ↔ q)? Explain.', 'Yes; both are true exactly when p and q differ.'), ('Give the truth column of (p ⊕ q) ⊕ q.', LG.colstr('(p ⊕ q) ⊕ q'))],
          ['p ⊕ q is true when exactly one is true.', 'Inclusive or minus the both-true case.', 'p ↔ q is true when p and q agree.', '(p ⊕ q) ⊕ q ≡ p, so its column is TTFF.'], 'xor_or')


# ---------------------------------------------------------------- 2. truth tables
TT = {'cp2': ['¬p ∨ q', 'p ∧ ¬q', '¬(p ∨ q)', 'p ∨ ¬q'],
      'cp1': ['(p ∨ q) ∧ ¬p', '¬p ∧ (p ∨ q)', '(p ∧ q) ∨ ¬q', '¬(p ∧ q) ∨ p'],
      'honors': ['(p ∨ q) ∧ ¬r', 'p ∧ (q ∨ r)', '(p → q) ∧ (q → r)', '¬(p ∨ r) ∨ q']}


def s2(b):
    for L in ('cp2', 'cp1', 'honors'):
        for f in TT[L]:
            vs = LG.variables(f) if L == 'honors' else ['p', 'q']
            col = LG.colstr(f, vs)
            order = ORDER3 if len(vs) == 3 else ORDER2
            if L == 'cp2':
                b.sa(2, L, 'Complete the truth table for %s. Give the final column as a string of T and F in the %s.\nHint: first find ¬p or ¬q, then combine.' % (f, order), col,
                     ['Rows: ' + '; '.join('%s → %s' % (''.join('T' if r[v] else 'F' for v in vs), 'T' if LG.ev(LG.parse(f), r) else 'F') for r in LG.rows(vs)) + '.', 'Column: ' + col], 'tt_column')
            else:
                b.mc(2, L, 'Which is the truth column of %s in the %s?' % (f, order), col, wrongs(col),
                     ['Rows: ' + '; '.join('%s → %s' % (''.join('T' if r[v] else 'F' for v in vs), 'T' if LG.ev(LG.parse(f), r) else 'F') for r in LG.rows(vs)) + '.', 'Column: ' + col], 'tt_column')
        # number of rows
        for n, L2 in ((2, 'cp2'), (3, 'cp1'), (5, 'honors')):
            if L2 == L:
                b.sa(2, L, 'How many rows does a truth table need for a statement with %d different variables?' % n, 2 ** n,
                     ['Each variable can be T or F, independently.', '2^%d = %d rows.' % (n, 2 ** n)], 'tt_rows')
        # count true rows
        CT = {'cp2': 'p ∨ q', 'cp1': '(p ∧ q) ∨ (¬p ∧ r)', 'honors': '(p ∨ q) ∧ (q ∨ r) ∧ (r ∨ p)'}[L]
        vs = LG.variables(CT)
        n = sum(LG.column(CT, vs))
        b.sa(2, L, 'In how many rows of its truth table is %s true?' % CT, n,
             ['Build the table with %d rows.' % (2 ** len(vs)), 'True in %d rows: %s.' % (n, LG.colstr(CT, vs))], 'tt_count')
        # identify formula from column
        GIVEN = {'cp2': ('TFFF', 'p ∧ q', ['p ∨ q', '¬p ∧ ¬q', 'p ∧ ¬q']), 'cp1': ('FTTF', '(p ∨ q) ∧ ¬(p ∧ q)', ['p ∨ q', '¬(p ∧ q)', '¬p ∨ ¬q']),
                 'honors': ('TFTT', 'q ∨ ¬p', ['p ∨ ¬q', '¬p ∧ q', 'p ∨ q'])}[L]
        col, good, bad = GIVEN
        assert LG.colstr(good, ['p', 'q']) == col and all(LG.colstr(x, ['p', 'q']) != col for x in bad)
        b.mc(2, L, 'A statement form in p and q has truth column %s (%s). Which statement form is it?' % (col, ORDER2), good, bad,
             ['Compute the column of each choice and compare.', '%s has column %s.' % (good, col)], 'tt_identify')
    b.sel(2, 'cp1', 'Which statement forms have truth column FTTT (%s)?' % ORDER2,
          [(f, LG.colstr(f, ['p', 'q']) == 'FTTT') for f in ['¬p ∨ ¬q', '¬(p ∧ q)', 'p ∨ q', '¬p ∧ ¬q', 'q → ¬p']],
          ['¬p ∨ ¬q, ¬(p ∧ q) and q → ¬p are all false only when p and q are both true.'], 'tt_select')
    b.sel(2, 'honors', 'Which statement forms are TRUE in the row p = T, q = F, r = T?',
          [(f, LG.ev(LG.parse(f), {'p': True, 'q': False, 'r': True})) for f in ['p → q', 'q → r', '(p ∧ r) → q', '¬q ↔ r', 'p ⊕ r']],
          ['Evaluate each form at p = T, q = F, r = T.'], 'tt_select')
    b.sel(2, 'cp2', 'For the statement p ∧ ¬q, which rows (p, q) make it TRUE? Select all.',
          [('(T, F)', True), ('(T, T)', False), ('(F, T)', False), ('(F, F)', False), ('No row', False)][:4] + [('Exactly one row', True)],
          ['p ∧ ¬q needs p true and q false: only the row (T, F).'], 'tt_select')
    b.orq(2, 'cp2', 'Build the truth table for ¬p ∧ q.',
          [('List the four rows (p, q) in standard order.', 'TT, TF, FT, FF'), ('Give the column for ¬p.', 'FFTT'),
           ('Give the column for ¬p ∧ q.', LG.colstr('¬p ∧ q')), ('In words, when is ¬p ∧ q true?', 'Only when p is false and q is true.')],
          ['Standard order lists T before F.', '¬p reverses p.', 'Combine with q.', 'Read the T row.'], 'tt_or')
    b.orq(2, 'cp1', 'Consider S = (p ∨ q) ∧ ¬(p ∧ q).',
          [('Give the column of p ∨ q.', 'TTTF'), ('Give the column of ¬(p ∧ q).', 'FTTT'),
           ('Give the column of S.', LG.colstr('(p ∨ q) ∧ ¬(p ∧ q)')), ('Describe S in words.', 'Exactly one of p, q is true (exclusive or).')],
          ['Inclusive or.', 'Not both.', 'Combine row by row: S is FTTF.'], 'tt_or')
    b.orq(2, 'honors', 'Consider S = (p ∧ q) ∨ (¬p ∧ r).',
          [('How many rows does its truth table have?', '8'), ('Give the column of S in the %s.' % ORDER3, LG.colstr('(p ∧ q) ∨ (¬p ∧ r)', ['p', 'q', 'r'])),
           ('Explain S as a "selector": what does p decide?', 'When p is true, S has the value of q; when p is false, S has the value of r.'),
           ('Is S equivalent to (p → q) ∧ (¬p → r)? Justify by comparing columns.', 'Yes; both columns are ' + LG.colstr('(p → q) ∧ (¬p → r)', ['p', 'q', 'r']))],
          ['2³ = 8.', 'Evaluate each row.', 'p chooses between q and r.', 'Compute both columns and compare.'], 'tt_or')


# ---------------------------------------------------------------- 3. logical equivalence
EQ = [  # (A, B) candidate pairs; equivalence computed
    ('¬(p ∧ q)', '¬p ∨ ¬q'), ('¬(p ∨ q)', '¬p ∧ ¬q'), ('¬(p ∧ q)', '¬p ∧ ¬q'), ('p ∨ (p ∧ q)', 'p'), ('p ∧ (q ∨ r)', '(p ∧ q) ∨ (p ∧ r)'),
    ('p ∨ (q ∧ r)', '(p ∨ q) ∧ r'), ('¬(¬p)', 'p'), ('p ∧ (p ∨ q)', 'q'), ('(p ∨ q) ∧ ¬p', 'q ∧ ¬p'), ('p ∨ ¬p', 'q ∨ ¬q'),
    ('p → q', 'q → p'), ('(p ∧ q) ∨ (p ∧ ¬q)', 'p'),
]


def s3(b):
    for L, idx in (('cp2', [0, 2, 6, 1]), ('cp1', [3, 7, 5, 8]), ('honors', [4, 9, 10, 11])):
        for i in idx:
            A, B = EQ[i]
            eq = LG.equivalent(A, B)
            vs = sorted(set(LG.variables(A)) | set(LG.variables(B)))
            ca, cb = LG.colstr(A, vs), LG.colstr(B, vs)
            b.mc(3, L, 'Are %s and %s logically equivalent?' % (A, B), 'Yes: their truth columns are identical' if eq else 'No: their truth columns differ in at least one row',
                 ['No: their truth columns differ in at least one row' if eq else 'Yes: their truth columns are identical',
                  'Yes: they use the same variables', 'No: they use different connectives'],
                 ['Columns over (%s): %s → %s; %s → %s.' % (', '.join(vs), A, ca, B, cb), 'Equivalent statements have identical columns in every row.'], 'equivalent_check')
    TAU = [('p ∨ ¬p', 'tautology'), ('p ∧ ¬p', 'contradiction'), ('(p ∧ q) → p', 'tautology'), ('p → q', 'neither'), ('(p → q) ∧ (p ∧ ¬q)', 'contradiction'),
           ('(p ∧ (p → q)) → q', 'tautology'), ('(p ∨ q) → p', 'neither'), ('¬(p ∨ ¬p)', 'contradiction'), ('((p → q) ∧ (q → r)) → (p → r)', 'tautology')]
    for f, kind in TAU:
        assert kind == ('tautology' if LG.tautology(f) else 'contradiction' if LG.contradiction(f) else 'neither'), f
    for L, idx in (('cp2', [0, 1, 3]), ('cp1', [2, 4, 6]), ('honors', [5, 7, 8])):
        for i in idx:
            f, kind = TAU[i]
            names = {'tautology': 'A tautology (always true)', 'contradiction': 'A contradiction (always false)', 'neither': 'Neither (true in some rows, false in others)'}
            vs = LG.variables(f)
            b.mc(3, L, 'Classify the statement form %s.' % f, names[kind], [v for k, v in names.items() if k != kind] + ['Not a statement form'],
                 ['Column over (%s): %s.' % (', '.join(vs), LG.colstr(f, vs)), names[kind] + '.'], 'tautology_classify')
    # De Morgan in words (short answer -> MC)
    DM = [('cp2', 'It is not true that Kim is tall and Lee is tall.', 'Kim is not tall or Lee is not tall.', ['Kim is not tall and Lee is not tall.', 'Kim is tall or Lee is tall.', 'Kim is tall and Lee is not tall.']),
          ('cp1', 'The number is not positive or not even... negate it: "The number is positive and even." Which sentence is its negation?', 'The number is not positive or it is not even.', ['The number is not positive and not even.', 'The number is negative and odd.', 'The number is positive or even.']),
          ('honors', '−1 < x ≤ 4. Which describes the negation (for real x)?', 'x ≤ −1 or x > 4', ['x ≤ −1 and x > 4', 'x < −1 or x ≥ 4', '−1 ≥ x ≥ 4'])]
    for L, t, good, bad in DM:
        b.mc(3, L, 'Use De Morgan\'s laws. %s' % t if L != 'cp1' else 'Use De Morgan\'s laws. Negate: "The number is positive and even."', good, bad,
             ['¬(p ∧ q) ≡ ¬p ∨ ¬q and ¬(p ∨ q) ≡ ¬p ∧ ¬q.', 'Answer: ' + good], 'demorgan_words')
    b.sel(3, 'cp2', 'Which statements are logically equivalent to ¬(p ∨ q)?',
          [(f, LG.equivalent(f, '¬(p ∨ q)')) for f in ['¬p ∧ ¬q', '¬p ∨ ¬q', '¬(q ∨ p)', '¬q ∧ ¬p', '¬p ∨ q']], ['Compare truth columns; ¬(p ∨ q) has column FFFT.'], 'equivalent_select')
    b.sel(3, 'cp1', 'Which statements are logically equivalent to p?',
          [(f, LG.equivalent(f, 'p')) for f in ['p ∨ (p ∧ q)', 'p ∧ (p ∨ q)', '¬¬p', 'p ∨ q', '(p ∧ q) ∨ ¬q']], ['Absorption: p ∨ (p ∧ q) ≡ p and p ∧ (p ∨ q) ≡ p; double negation ¬¬p ≡ p.'], 'equivalent_select')
    b.sel(3, 'honors', 'Which statements are logically equivalent to p ∧ (q ∨ r)?',
          [(f, LG.equivalent(f, 'p ∧ (q ∨ r)')) for f in ['(p ∧ q) ∨ (p ∧ r)', '(p ∧ q) ∨ r', '(q ∨ r) ∧ p', '¬(¬p ∨ (¬q ∧ ¬r))', 'p ∧ q ∨ p']],
          ['Distributive law, commutative law and De Morgan give the three equivalent forms; (p ∧ q) ∨ r is true when p is F and r is T.'], 'equivalent_select')
    b.sa(3, 'cp1', 'Simplify ¬(¬p ∧ q) using De Morgan\'s law and double negation. Write the result with ∨.', 'p ∨ ¬q',
         ['¬(¬p ∧ q) ≡ ¬¬p ∨ ¬q (De Morgan).', '≡ p ∨ ¬q (double negation).'], 'simplify')
    b.sa(3, 'honors', 'Simplify (p ∧ q) ∨ (p ∧ ¬q) to a single variable.', 'p',
         ['Distributive law: p ∧ (q ∨ ¬q).', 'q ∨ ¬q is a tautology t, and p ∧ t ≡ p.'], 'simplify')
    b.sa(3, 'cp2', 'Use De Morgan\'s law to rewrite ¬(p ∧ q) using ∨.', '¬p ∨ ¬q', ['Negate each part and change ∧ to ∨.', '¬p ∨ ¬q'], 'simplify')
    b.orq(3, 'cp2', 'Show that ¬(p ∨ q) ≡ ¬p ∧ ¬q.',
          [('Give the column of p ∨ q.', 'TTTF'), ('Give the column of ¬(p ∨ q).', 'FFFT'), ('Give the column of ¬p ∧ ¬q.', 'FFFT'),
           ('What do the matching columns show?', 'The two statements are logically equivalent (De Morgan\'s law).')],
          ['Or is false only in row FF.', 'Negate.', '¬p and ¬q are both true only in row FF.', 'Identical columns mean equivalent.'], 'demorgan_or')
    b.orq(3, 'cp1', 'Determine whether (p ∨ q) ∧ ¬p is equivalent to q.',
          [('Give the column of (p ∨ q) ∧ ¬p.', LG.colstr('(p ∨ q) ∧ ¬p')), ('Give the column of q.', 'TFTF'),
           ('Are they equivalent? Name a row where they differ if not.', 'No; row (T, T): the first is F but q is T.'), ('Simplify (p ∨ q) ∧ ¬p with laws.', '¬p ∧ q')],
          ['Evaluate.', 'q alternates.', 'Compare rows.', 'Distribute: (p ∧ ¬p) ∨ (q ∧ ¬p) ≡ c ∨ (q ∧ ¬p) ≡ ¬p ∧ q.'], 'equiv_or')
    b.orq(3, 'honors', 'Prove with laws (no truth table) that ¬(p ∨ (¬p ∧ q)) ≡ ¬p ∧ ¬q, naming each law.',
          [('Apply De Morgan to the outer negation.', '¬p ∧ ¬(¬p ∧ q)'), ('Apply De Morgan and double negation inside.', '¬p ∧ (p ∨ ¬q)'),
           ('Apply the distributive law.', '(¬p ∧ p) ∨ (¬p ∧ ¬q)'), ('Finish using the negation and identity laws.', 'c ∨ (¬p ∧ ¬q) ≡ ¬p ∧ ¬q')],
          ['¬(a ∨ b) ≡ ¬a ∧ ¬b.', '¬(¬p ∧ q) ≡ p ∨ ¬q.', 'a ∧ (b ∨ c) ≡ (a ∧ b) ∨ (a ∧ c).', '¬p ∧ p is a contradiction c, and c ∨ x ≡ x.'], 'law_proof_or')


# ---------------------------------------------------------------- 4. conditional statements and equivalent forms
def s4(b):
    COLS = {'cp2': ['p → q', 'q → p', '¬p → q'], 'cp1': ['p ↔ q', '¬p → ¬q', '(p → q) ∧ (q → p)'], 'honors': ['(p → q) → r', 'p → (q → r)', '(p ∧ q) → r']}
    for L, fs in COLS.items():
        for f in fs:
            vs = LG.variables(f)
            col = LG.colstr(f, vs)
            b.mc(4, L, 'Which is the truth column of %s in the %s?' % (f, ORDER3 if len(vs) == 3 else ORDER2), col, wrongs(col),
                 ['→ is false only when its left side is T and its right side is F; ↔ is true when both sides agree.', 'Column: ' + col], 'cond_column')
    EQV = [('cp2', 'p → q', '¬p ∨ q', ['p ∨ ¬q', '¬p ∧ q', 'q → p']),
           ('cp2', 'p ↔ q', '(p → q) ∧ (q → p)', ['(p → q) ∨ (q → p)', 'p ∧ q', '(p ∨ q) ∧ ¬(p ∧ q)']),
           ('cp1', '¬p → q', 'p ∨ q', ['¬p ∨ q', 'p ∧ q', '¬(p ∨ q)']),
           ('cp1', 'p → ¬q', '¬(p ∧ q)', ['¬p → q', 'p ∧ ¬q', '¬p ∧ ¬q']),
           ('honors', '(p ∧ q) → r', 'p → (q → r)', ['(p → q) → r', '(p → r) ∧ (q → r)', 'p ∧ (q → r)']),
           ('honors', '(p ∨ q) → r', '(p → r) ∧ (q → r)', ['(p → r) ∨ (q → r)', 'p ∨ (q → r)', '(p ∧ q) → r'])]
    for L, a, good, bad in EQV:
        assert LG.equivalent(a, good) and not any(LG.equivalent(a, x) for x in bad), a
        b.mc(4, L, 'Which statement form is logically equivalent to %s?' % a, good, bad,
             ['Compare truth columns: %s has column %s.' % (a, LG.colstr(a, sorted(set(LG.variables(a)) | set(LG.variables(good))))), 'Only %s matches.' % good], 'cond_equivalent')
    WORDS = [('cp2', '"If it snows, school closes" is equivalent to:', 'It does not snow, or school closes.', ['It snows, or school does not close.', 'It snows and school closes.', 'If school closes, then it snows.']),
             ('cp1', '"You get a refund if and only if you return the item within 30 days" means:', 'If you return the item within 30 days you get a refund, and if you get a refund you returned it within 30 days.',
              ['If you return the item within 30 days, you get a refund.', 'If you get a refund, you returned the item within 30 days.', 'You get a refund or you return the item within 30 days.']),
             ('honors', '"A triangle is equilateral only if it is isosceles" is equivalent to:', 'A triangle is not equilateral or it is isosceles.', ['A triangle is equilateral or it is not isosceles.', 'If a triangle is isosceles, then it is equilateral.', 'A triangle is equilateral if and only if it is isosceles.'])]
    for L, t, good, bad in WORDS:
        b.mc(4, L, t, good, bad, ['p → q ≡ ¬p ∨ q; p ↔ q ≡ (p → q) ∧ (q → p); "p only if q" is p → q.', 'Answer: ' + good], 'cond_words')
    b.sa(4, 'cp2', 'Rewrite p → q using only ¬ and ∨.', '¬p ∨ q', ['A conditional is false only when p is T and q is F, exactly like ¬p ∨ q.'], 'cond_rewrite')
    b.sa(4, 'cp1', 'Rewrite ¬p → (q ∨ r) using only ¬ and ∨, with no double negation. Write the variables in the order p, q, r.', 'p ∨ q ∨ r', ['¬p → s ≡ ¬¬p ∨ s ≡ p ∨ s.', 'So the statement is p ∨ q ∨ r.'], 'cond_rewrite')
    b.sa(4, 'honors', 'In how many of the 8 rows is (p → q) ∧ (q → r) ∧ (r → p) true?', sum(LG.column('(p → q) ∧ (q → r) ∧ (r → p)')),
         ['The cycle of conditionals forces p, q, r to have the same truth value.', 'True only in TTT and FFF: 2 rows.'], 'cond_count')
    b.sel(4, 'cp1', 'Which statements are logically equivalent to p → q?',
          [(f, LG.equivalent(f, 'p → q')) for f in ['¬p ∨ q', '¬q → ¬p', 'q → p', '¬(p ∧ ¬q)', '¬p → ¬q']], ['¬p ∨ q, the contrapositive ¬q → ¬p and ¬(p ∧ ¬q) match; the converse and inverse do not.'], 'cond_select')
    b.sel(4, 'cp2', 'Which rows (p, q) make p → q FALSE? (Select every correct description.)',
          [('p = T, q = F', True), ('p = F, q = T', False), ('p = F, q = F', False), ('Exactly one row', True), ('Every row with q false', False)],
          ['p → q is false only when p is T and q is F: exactly one row.'], 'cond_select')
    b.sel(4, 'honors', 'Let p: "n is divisible by 6" and q: "n is divisible by 2 and by 3" (n an integer). Which are TRUE for every integer n?',
          [('p → q', True), ('q → p', True), ('p ↔ q', True), ('p ↔ ¬q', False), ('p ⊕ q', False)],
          ['6 | n exactly when 2 | n and 3 | n (2 and 3 are relatively prime), so p ↔ q holds for every n.'], 'bicond_select')
    b.orq(4, 'cp1', 'Let p: "the switch is on" and q: "the lamp is lit".',
          [('Write p → q in words.', 'If the switch is on, then the lamp is lit.'), ('Write the equivalent ¬p ∨ q in words.', 'The switch is off or the lamp is lit.'),
           ('Write p ↔ q in words.', 'The switch is on if and only if the lamp is lit.'), ('Describe a situation where p → q is true but p ↔ q is false.', 'The switch is off and the lamp is lit (p = F, q = T).')],
          ['Conditional.', 'p → q ≡ ¬p ∨ q.', 'Biconditional.', 'Row FT: p → q is T but p ↔ q is F.'], 'cond_or')
    b.orq(4, 'honors', 'Show that p → (q → r) ≡ (p ∧ q) → r ("exportation").',
          [('Rewrite p → (q → r) using ¬ and ∨.', '¬p ∨ (¬q ∨ r)'), ('Rewrite (p ∧ q) → r using ¬ and ∨.', '¬(p ∧ q) ∨ r ≡ (¬p ∨ ¬q) ∨ r'),
           ('Explain why the two are equivalent.', 'Both equal ¬p ∨ ¬q ∨ r by associativity.'), ('In which single row are both false?', 'p = T, q = T, r = F')],
          ['Replace each a → b by ¬a ∨ b.', 'De Morgan.', 'Associative law.', 'Both are false only when p, q are true and r is false.'], 'exportation_or')
    b.orq(4, 'cp2', 'Consider "If you score 100, then you get a sticker."',
          [('Write it as ¬p ∨ q in words.', 'You do not score 100, or you get a sticker.'), ('Is it true if you score 90 and get a sticker?', 'Yes'),
           ('Is it true if you score 100 and get no sticker?', 'No'), ('Is it true if you score 90 and get no sticker?', 'Yes')],
          ['p → q ≡ ¬p ∨ q.', 'p = F: true.', 'p = T, q = F: false.', 'p = F: true.'], 'cond_or')


# ---------------------------------------------------------------- 5. negating conditionals
NEGC = [  # (statement, correct negation, distractors)
    ('If it is sunny, then we go to the beach.', 'It is sunny and we do not go to the beach.', ['If it is sunny, then we do not go to the beach.', 'If it is not sunny, then we do not go to the beach.', 'It is not sunny and we go to the beach.']),
    ('If n is prime, then n is odd.', 'n is prime and n is not odd.', ['If n is prime, then n is even.', 'If n is not prime, then n is not odd.', 'n is not prime or n is odd.']),
    ('If a shape is a square, then it has four sides.', 'The shape is a square and it does not have four sides.', ['If a shape is not a square, it does not have four sides.', 'If a shape is a square, it does not have four sides.', 'The shape is not a square and has four sides.']),
    ('If x > 3, then x² > 9.', 'x > 3 and x² ≤ 9.', ['If x > 3, then x² ≤ 9.', 'x ≤ 3 and x² > 9.', 'If x ≤ 3, then x² ≤ 9.']),
    ('If Pat studies, then Pat passes or Pat is lucky.', 'Pat studies, and Pat does not pass and is not lucky.', ['Pat studies, and Pat does not pass or is not lucky.', 'If Pat studies, Pat fails and is unlucky.', 'Pat does not study, and Pat passes or is lucky.']),
    ('For every integer n, if n² is even then n is even.', 'There is an integer n such that n² is even and n is odd.', ['For every integer n, if n² is even then n is odd.', 'There is an integer n such that if n² is even then n is odd.', 'For every integer n, n² is odd and n is even.']),
]


def s5(b):
    for L, idx in (('cp2', [0, 2, 1]), ('cp1', [1, 3, 4]), ('honors', [4, 5, 3])):
        for i in idx:
            st, good, bad = NEGC[i]
            b.mc(5, L, 'Which is the negation of "%s"?' % st, good, bad,
                 ['¬(p → q) ≡ p ∧ ¬q: the negation of a conditional is NOT another conditional.', 'Negation: ' + good], 'negate_conditional')
    SYM = [('cp2', 'p → q', 'p ∧ ¬q'), ('cp2', '¬p → q', '¬p ∧ ¬q'), ('cp1', 'p → ¬q', 'p ∧ q'), ('cp1', '(p ∧ q) → r', 'p ∧ q ∧ ¬r'),
           ('honors', 'p → (q ∨ r)', 'p ∧ ¬q ∧ ¬r'), ('honors', '(p ∨ q) → ¬r', '(p ∨ q) ∧ r')]
    for L, f, neg in SYM:
        assert LG.equivalent('¬(' + f + ')', neg)
        b.sa(5, L, 'Write the negation of %s without using → (and with ¬ applied only to single letters). Keep the letters in alphabetical order.' % f, neg,
             ['¬(a → b) ≡ a ∧ ¬b.', 'Simplify with De Morgan if needed: %s.' % neg], 'negate_symbolic')
    TV = [('cp2', 'If 5 is odd, then 5 is prime.'), ('cp1', 'If 4 is odd, then 4 is prime.'), ('honors', 'If 9 is odd, then 9 is prime.')]
    for L, st in TV:
        p = '4' not in st
        q = '5' in st
        orig = (not p) or q
        b.mc(5, L, 'Determine the truth value of the NEGATION of "%s"' % st, 'True' if not orig else 'False', ['False' if not orig else 'True', 'Same truth value as the original', 'Cannot be determined'],
             ['The original is %s.' % ('true' if orig else 'false'), 'A negation always has the opposite truth value, so the negation is %s.' % ('false' if orig else 'true')], 'negation_truth')
    b.sel(5, 'cp1', 'Which statements are equivalent to the negation of "If the battery is charged, the phone turns on"?',
          [('The battery is charged and the phone does not turn on.', True), ('The phone does not turn on, but the battery is charged.', True),
           ('If the battery is charged, the phone does not turn on.', False), ('The battery is not charged or the phone turns on.', False),
           ('It is false that the battery being charged guarantees the phone turns on.', True)],
          ['¬(p → q) ≡ p ∧ ¬q; order of a conjunction does not matter.', '"not charged or turns on" is the original itself.'], 'negate_select')
    b.sel(5, 'cp2', 'Which statement forms are equivalent to ¬(p → q)?',
          [(f, LG.equivalent(f, '¬(p → q)')) for f in ['p ∧ ¬q', '¬q ∧ p', 'p → ¬q', '¬p → ¬q', '¬(¬p ∨ q)']], ['¬(p → q) ≡ ¬(¬p ∨ q) ≡ p ∧ ¬q.'], 'negate_select')
    b.sel(5, 'honors', 'Which are correct negations of "For every real x, if x > 0 then there is a real y with y² = x"?',
          [('There is a real x with x > 0 such that for every real y, y² ≠ x.', True), ('There is a real x such that x > 0 and no real y has y² = x.', True),
           ('For every real x, if x > 0 then no real y has y² = x.', False), ('There is a real x such that if x > 0 then y² ≠ x for every y.', False),
           ('For every real x, x ≤ 0 or some y has y² = x.', False)],
          ['Negate ∀x (P(x) → ∃y Q) as ∃x (P(x) ∧ ∀y ¬Q).', 'The last choice is equivalent to the original statement.'], 'negate_select')
    b.orq(5, 'cp2', 'Statement: "If Mia has a ticket, then Mia can enter."',
          [('Identify p and q.', 'p: Mia has a ticket; q: Mia can enter.'), ('Write the negation in symbols.', 'p ∧ ¬q'),
           ('Write the negation in words.', 'Mia has a ticket and Mia cannot enter.'), ('Explain why "If Mia has a ticket, then Mia cannot enter" is NOT the negation.', 'Both could be false at once (for example when Mia has no ticket); a negation must have the opposite truth value in every case.')],
          ['Hypothesis and conclusion.', '¬(p → q) ≡ p ∧ ¬q.', 'Translate.', 'p → ¬q and p → q are both true when p is false.'], 'negate_or')
    b.orq(5, 'cp1', 'Statement S: "If a number is divisible by 4, then it is divisible by 8."',
          [('Write ¬S in words.', 'A number is divisible by 4 and is not divisible by 8.'), ('Is S true for all integers?', 'No'),
           ('Give a number that makes ¬S true.', 'For example 4 (or 12, 20).'), ('Write the negation of "For every integer n, S(n)".', 'There is an integer n that is divisible by 4 and not divisible by 8.')],
          ['p ∧ ¬q.', '4 is a counterexample.', '4 is divisible by 4 but not 8.', '∃n (p(n) ∧ ¬q(n)).'], 'negate_or')
    b.orq(5, 'honors', 'Statement: "If a function f is differentiable, then f is continuous" (a true theorem).',
          [('Write its negation.', 'f is differentiable and f is not continuous.'), ('Write its converse.', 'If f is continuous, then f is differentiable.'),
           ('Write the negation of the converse.', 'f is continuous and f is not differentiable.'), ('The converse is false. Which statement in parts (a)–(c) is true for f(x) = |x|? Explain.', 'The negation of the converse: |x| is continuous but not differentiable at 0.')],
          ['¬(p → q) ≡ p ∧ ¬q.', 'Swap hypothesis and conclusion.', 'Apply the same rule to the converse.', '|x| has a corner at 0.'], 'negate_or')


# ---------------------------------------------------------------- 6. converse, inverse, contrapositive
CIC = [  # (p, q, not p, not q)
    ('it is raining', 'the ground is wet', 'it is not raining', 'the ground is not wet'),
    ('a number is a multiple of 10', 'it ends in 0', 'a number is not a multiple of 10', 'it does not end in 0'),
    ('you are in Boston', 'you are in Massachusetts', 'you are not in Boston', 'you are not in Massachusetts'),
    ('x = 2', 'x² = 4', 'x ≠ 2', 'x² ≠ 4'),
    ('a quadrilateral is a rhombus', 'its diagonals are perpendicular', 'a quadrilateral is not a rhombus', 'its diagonals are not perpendicular'),
    ('n is odd', 'n² is odd', 'n is not odd', 'n² is not odd'),
]


def s6(b):
    kinds = ['converse', 'inverse', 'contrapositive']
    plan = {'cp2': [(0, 'converse'), (2, 'contrapositive'), (1, 'inverse')], 'cp1': [(3, 'contrapositive'), (4, 'converse'), (1, 'contrapositive')],
            'honors': [(5, 'contrapositive'), (4, 'inverse'), (3, 'converse')]}
    for L, items in plan.items():
        for i, kind in items:
            p, q, np_, nq = CIC[i]
            forms = {'converse': 'If %s, then %s.' % (q, p), 'inverse': 'If %s, then %s.' % (np_, nq), 'contrapositive': 'If %s, then %s.' % (nq, np_)}
            other = [forms[k] for k in kinds if k != kind] + ['If %s, then %s.' % (p, nq)]
            b.mc(6, L, 'Statement: "If %s, then %s." Which is its %s?' % (p, q, kind.upper()), forms[kind], other,
                 ['Converse: q → p. Inverse: ¬p → ¬q. Contrapositive: ¬q → ¬p.', 'The %s is: %s' % (kind, forms[kind])], 'cic_identify')
    TRUTH = [  # (p→q text, truth of statement, converse, inverse, contrapositive)
        ('If a number is a multiple of 4, then it is even.', True, False, False, True),
        ('If x = 2, then x² = 4.', True, False, False, True),
        ('If a number is even and prime, then it equals 2.', True, True, True, True),
        ('If a polygon has 4 sides, then it is a square.', False, True, True, False),
    ]
    for L, i in (('cp2', 0), ('cp1', 1), ('cp1', 3), ('honors', 2)):
        st, t, c, inv, cp = TRUTH[i]
        b.sel(6, L, 'Statement: "%s" Which of the following are TRUE? Select all that apply.' % st,
              [('The statement', t), ('Its converse', c), ('Its inverse', inv), ('Its contrapositive', cp), ('The statement and its converse have the same truth value', t == c)] if (t + c + inv + cp + (t == c)) >= 2 and (t + c + inv + cp + (t == c)) < 5 else
              [('The statement', t), ('Its converse', c), ('Its inverse', inv), ('Its contrapositive', cp), ('The inverse is false', not inv)],
              ['A statement and its contrapositive always share a truth value; the converse and inverse always share one with each other.',
               'Statement %s, converse %s, inverse %s, contrapositive %s.' % tuple('T' if x else 'F' for x in (t, c, inv, cp))], 'cic_truth_select')
    SYMS = [('cp2', 'p → q', 'contrapositive', '¬q → ¬p'), ('cp2', 'p → q', 'converse', 'q → p'), ('cp1', '¬p → q', 'contrapositive', '¬q → p'),
            ('cp1', 'p → ¬q', 'inverse', '¬p → q'), ('honors', '(p ∧ q) → r', 'contrapositive', '¬r → (¬p ∨ ¬q)'), ('honors', 'p → (q ∨ r)', 'converse', '(q ∨ r) → p')]
    for L, f, kind, ans in SYMS:
        b.sa(6, L, 'Write the %s of %s in symbols (simplify ¬¬ to the letter itself; use De Morgan where needed).' % (kind, f), ans,
             ['Converse swaps the sides; inverse negates both; contrapositive swaps and negates.', '%s of %s: %s' % (kind.capitalize(), f, ans)], 'cic_symbolic')
    b.mc(6, 'cp2', 'Which statement is ALWAYS logically equivalent to "If p, then q"?', 'Its contrapositive', ['Its converse', 'Its inverse', 'Its negation'],
         ['p → q ≡ ¬q → ¬p.', 'The converse and inverse are equivalent to each other, not to the original.'], 'cic_equivalent')
    b.mc(6, 'cp1', 'The converse of a statement is false. Which other form must also be false?', 'The inverse', ['The contrapositive', 'The original statement', 'The negation of the inverse'],
         ['The inverse ¬p → ¬q is the contrapositive of the converse q → p, so they have the same truth value.'], 'cic_equivalent')
    b.mc(6, 'honors', 'Statement S is true and its converse is false. What is the truth value of the biconditional p ↔ q (the "if and only if" form of S)?', 'False',
         ['True', 'It depends on p', 'True whenever S is true'], ['p ↔ q ≡ (p → q) ∧ (q → p).', 'The second conjunct (the converse) is false, so the biconditional is false.'], 'cic_bicond')
    b.orq(6, 'cp1', 'Statement: "If a triangle is equilateral, then it is isosceles."',
          [('Write the converse and give its truth value.', 'If a triangle is isosceles, then it is equilateral. False.'),
           ('Write the inverse and give its truth value.', 'If a triangle is not equilateral, then it is not isosceles. False.'),
           ('Write the contrapositive and give its truth value.', 'If a triangle is not isosceles, then it is not equilateral. True.'),
           ('Give a triangle that shows the converse is false.', 'A triangle with sides 5, 5, 3.')],
          ['Swap.', 'Negate both.', 'Swap and negate.', 'Isosceles but not equilateral.'], 'cic_or')
    b.orq(6, 'honors', 'Let S: "For every integer n, if n² is even, then n is even."',
          [('Write the contrapositive of the conditional inside S.', 'If n is odd, then n² is odd.'), ('Prove the contrapositive.', 'If n = 2k + 1, then n² = 4k² + 4k + 1 = 2(2k² + 2k) + 1, which is odd.'),
           ('Why does this prove S?', 'A conditional and its contrapositive are logically equivalent.'), ('Write the converse of the conditional. Is it true?', 'If n is even, then n² is even. True.')],
          ['Swap and negate; "not even" is "odd".', 'Square 2k + 1.', 'Equivalent forms have the same truth value.', '(2k)² = 2(2k²).'], 'cic_proof_or')
    b.orq(6, 'cp2', 'Statement: "If an animal is a cat, then it has whiskers."',
          [('Write the converse.', 'If an animal has whiskers, then it is a cat.'), ('Is the converse true? Give a reason.', 'No; dogs have whiskers.'),
           ('Write the contrapositive.', 'If an animal does not have whiskers, then it is not a cat.'), ('Which form has the same truth value as the statement?', 'The contrapositive')],
          ['Swap hypothesis and conclusion.', 'A counterexample shows it is false.', 'Swap and negate.', 'Contrapositive ≡ original.'], 'cic_or')


# ---------------------------------------------------------------- 7. rules of inference
ARG = [  # (premises, conclusion, rule name if valid)
    (['p → q', 'p'], 'q', 'modus ponens'), (['p → q', '¬q'], '¬p', 'modus tollens'), (['p → q', 'q → r'], 'p → r', 'transitivity (hypothetical syllogism)'),
    (['p ∨ q', '¬p'], 'q', 'elimination (disjunctive syllogism)'), (['p'], 'p ∨ q', 'generalization'), (['p ∧ q'], 'p', 'specialization'),
    (['p → q', 'q'], 'p', None), (['p → q', '¬p'], '¬q', None), (['p ∨ q', 'p'], '¬q', None),
    (['p ∨ q', 'p → r', 'q → r'], 'r', 'proof by division into cases'), (['¬p → c'], 'p', 'contradiction rule'),
]
NAMES = ['modus ponens', 'modus tollens', 'transitivity (hypothetical syllogism)', 'elimination (disjunctive syllogism)', 'generalization', 'specialization',
         'proof by division into cases', 'contradiction rule']
ENGARG = [  # english arguments with symbolic forms (validity computed)
    ('If the alarm rings, I wake up. The alarm rang. Therefore I woke up.', ['p → q', 'p'], 'q'),
    ('If it is a holiday, the bank is closed. The bank is open. Therefore it is not a holiday.', ['p → q', '¬q'], '¬p'),
    ('If you run a red light, you get a ticket. You got a ticket. Therefore you ran a red light.', ['p → q', 'q'], 'p'),
    ('Either the key is in my coat or in my car. It is not in my coat. So it is in my car.', ['p ∨ q', '¬p'], 'q'),
    ('If n is divisible by 6, then n is even. n is not divisible by 6. So n is not even.', ['p → q', '¬p'], '¬q'),
    ('If I save, I can buy a bike. If I can buy a bike, I ride to school. So if I save, I ride to school.', ['p → q', 'q → r'], 'p → r'),
    ('If the program is correct, the tests pass. If the tests pass, we release. We did not release. So the program is not correct.', ['p → q', 'q → r', '¬r'], '¬p'),
    ('Pat is in Paris or Rome. If Pat is in Paris, Pat is in Europe. If Pat is in Rome, Pat is in Europe. So Pat is in Europe.', ['p ∨ q', 'p → r', 'q → r'], 'r'),
]


def s7(b):
    for L, idx in (('cp2', [0, 1, 5]), ('cp1', [2, 3, 4]), ('honors', [9, 10, 2])):
        for i in idx:
            prem, conc, rule = ARG[i]
            ok, _ = LG.valid([p.replace('c', '(p ∧ ¬p)') for p in prem], conc)
            assert ok and rule
            b.mc(7, L, 'Name the rule of inference%s:\n' % (' (c denotes a contradiction, a statement that is always false)' if i == 10 else '') + '\n'.join(prem) + '\n∴ ' + conc, rule.capitalize(), [n.capitalize() for n in NAMES if n != rule][:3] if i != 1 else ['Modus ponens', 'Converse error', 'Transitivity (hypothetical syllogism)'],
                 ['Match the pattern of the premises and conclusion to a known valid form.', 'This is %s.' % rule], 'name_rule')
    for L, idx in (('cp2', [0, 2, 3]), ('cp1', [1, 4, 5]), ('honors', [6, 7, 4])):
        for i in idx:
            t, prem, conc = ENGARG[i]
            ok, cx = LG.valid(prem, conc)
            b.mc(7, L, 'Is the argument valid?\n%s' % t, 'Valid' if ok else 'Invalid',
                 ['Invalid' if ok else 'Valid', 'Valid, because the conclusion is true', 'Invalid, because one premise could be false'],
                 ['Symbolic form: ' + ', '.join(prem) + ' ∴ ' + conc + '.',
                  'An argument is valid when every row that makes all premises true also makes the conclusion true.' +
                  ('' if ok else ' Row %s makes the premises true and the conclusion false.' % ', '.join('%s=%s' % (k, 'T' if v else 'F') for k, v in cx.items()))], 'english_valid')
    COMPLETE = [('cp2', ['If it rains, the game is canceled.', 'It is raining.'], 'The game is canceled.'),
                ('cp1', ['If the store is open, the lights are on.', 'The lights are not on.'], 'The store is not open.'),
                ('honors', ['If x > 5, then x² > 25.', 'If x² > 25, then x² ≠ 16.'], 'If x > 5, then x² ≠ 16.')]
    for L, prem, conc in COMPLETE:
        b.sa(7, L, 'Write the conclusion that follows by a valid rule of inference:\n' + '\n'.join(prem) + '\n∴ ?', conc,
             ['Identify the form of the premises.', 'Conclusion: ' + conc], 'complete_argument',
             notes='Hand-authored; the symbolic form was checked valid with logic.py.')
    b.sel(7, 'cp1', 'Which argument forms are VALID?',
          [(' ; '.join(p) + ' ∴ ' + c, LG.valid(p, c)[0]) for p, c in [(['p → q', 'p'], 'q'), (['p → q', 'q'], 'p'), (['p → q', '¬q'], '¬p'), (['p ∨ q', 'p'], '¬q'), (['p ∧ q'], 'q')]],
          ['Check each with a truth table: valid forms never have all premises T and the conclusion F.'], 'valid_select')
    b.sel(7, 'honors', 'Premises: p → q, ¬r → ¬q, ¬r. Which conclusions follow validly?',
          [(c, LG.valid(['p → q', '¬r → ¬q', '¬r'], c)[0]) for c in ['¬q', '¬p', 'p → r', 'q', 'r']],
          ['From ¬r → ¬q and ¬r: ¬q (modus ponens). From p → q and ¬q: ¬p (modus tollens). p → r also follows (q → r is the contrapositive of ¬r → ¬q).'], 'valid_select')
    b.sel(7, 'cp2', 'Premises: "If Ada studies, Ada passes" and "Ada studies." Which conclusions follow?',
          [('Ada passes.', True), ('Ada studies or Ada is tired.', True), ('Ada does not pass.', False), ('Ada studies and passes.', True), ('If Ada passes, Ada studied.', False)],
          ['Modus ponens gives "Ada passes"; generalization gives "Ada studies or ..."; conjunction gives "Ada studies and passes". The last choice is the converse.'], 'valid_select')
    b.orq(7, 'cp1', 'Premises: (1) If it is Saturday, Lin works. (2) If Lin works, Lin eats out. (3) Lin did not eat out.',
          [('Write the premises in symbols with s, w, e.', 's → w, w → e, ¬e'), ('What follows from (2) and (3)? Name the rule.', '¬w, modus tollens'),
           ('What follows from (1) and the previous result? Name the rule.', '¬s, modus tollens'), ('State the final conclusion in words.', 'It is not Saturday.')],
          ['Translate.', 'w → e and ¬e give ¬w.', 's → w and ¬w give ¬s.', '¬s.'], 'chain_or')
    b.orq(7, 'honors', 'Knights always tell the truth and knaves always lie. A says: "B is a knave." B says: "A and I are the same type."',
          [('If A is a knight, what is B? Is B\'s statement then true or false?', 'B is a knave; B\'s statement ("same type") is false, consistent with B lying.'),
           ('If A is a knave, what is B? Check B\'s statement.', 'B is a knight; but then "A and I are the same type" is false, which a knight cannot say. Contradiction.'),
           ('What are A and B?', 'A is a knight and B is a knave.'), ('Which rule of inference eliminated the second case?', 'Contradiction rule / elimination: the case A knave leads to a contradiction.')],
          ['Assume each case and check every statement.', 'A knight cannot say a false sentence.', 'Only case 1 is consistent.', 'Division into cases plus contradiction.'], 'knights_or')
    b.orq(7, 'cp2', 'Premises: "If Ben finishes his homework, he plays outside." "Ben finished his homework."',
          [('Write the premises with p and q.', 'p → q, p'), ('What can you conclude?', 'Ben plays outside.'), ('Name the rule.', 'Modus ponens'),
           ('If instead you know "Ben did not play outside", what can you conclude?', 'Ben did not finish his homework (modus tollens).')],
          ['Translate.', 'p → q and p give q.', 'Modus ponens.', 'p → q and ¬q give ¬p.'], 'mp_or')


# ---------------------------------------------------------------- 8. fallacies and contradictions
FALL = [  # (argument, correct label)
    ('If it snows, school closes. School closed. So it snowed.', 'Converse error (affirming the conclusion)'),
    ('If it snows, school closes. It did not snow. So school did not close.', 'Inverse error (denying the hypothesis)'),
    ('If it snows, school closes. It snowed. So school closed.', 'Valid (modus ponens)'),
    ('If it snows, school closes. School did not close. So it did not snow.', 'Valid (modus tollens)'),
    ('If a number is divisible by 4, it is even. 10 is even. So 10 is divisible by 4.', 'Converse error (affirming the conclusion)'),
    ('If a shape is a square, it is a rectangle. This shape is not a square. So it is not a rectangle.', 'Inverse error (denying the hypothesis)'),
    ('Either the TV is broken or the remote is dead. The remote is dead. So the TV is not broken.', 'Invalid: "or" is inclusive, so both could be true'),
    ('If Kai is late, Kai misses the bus. Kai missed the bus. So Kai was late.', 'Converse error (affirming the conclusion)'),
]
LABELS = ['Converse error (affirming the conclusion)', 'Inverse error (denying the hypothesis)', 'Valid (modus ponens)', 'Valid (modus tollens)', 'Invalid: "or" is inclusive, so both could be true']
FORMS = {FALL[0][0]: (['p → q', 'q'], 'p'), FALL[1][0]: (['p → q', '¬p'], '¬q'), FALL[2][0]: (['p → q', 'p'], 'q'), FALL[3][0]: (['p → q', '¬q'], '¬p'),
         FALL[4][0]: (['p → q', 'q'], 'p'), FALL[5][0]: (['p → q', '¬p'], '¬q'), FALL[6][0]: (['p ∨ q', 'q'], '¬p'), FALL[7][0]: (['p → q', 'q'], 'p')}


def s8(b):
    for L, idx in (('cp2', [0, 1, 2]), ('cp1', [3, 4, 5]), ('honors', [6, 7, 1])):
        for i in idx:
            t, lab = FALL[i]
            prem, conc = FORMS[t]
            assert LG.valid(prem, conc)[0] == lab.startswith('Valid')
            b.mc(8, L, 'Classify the argument:\n%s' % t, lab, [x for x in LABELS if x != lab][:3],
                 ['Symbolic form: %s ∴ %s.' % (', '.join(prem), conc), lab + '.'], 'classify_fallacy')
    CON = [('cp2', 'p ∧ ¬p'), ('cp1', '(p → q) ∧ p ∧ ¬q'), ('honors', '(p ∨ q) ∧ ¬p ∧ ¬q'), ('cp1', '¬(p → p)'), ('honors', '(p ↔ q) ∧ (p ⊕ q)'), ('cp2', 'q ∧ ¬q')]
    for L, f in CON:
        assert LG.contradiction(f)
        b.mc(8, L, 'Is %s a contradiction (false in every row)?' % f, 'Yes', ['No, it is a tautology', 'No, it is true in exactly one row', 'No, it is true in exactly two rows'],
             ['Column: %s.' % LG.colstr(f), 'Every entry is F, so it is a contradiction.'], 'contradiction_check')
    b.sa(8, 'cp2', 'An argument has premises p → q and q and concludes p. Give the row (p, q) that shows it is invalid, written like (T, F).', '(F, T)',
         ['We need both premises true and the conclusion false.', 'p = F, q = T: p → q = T, q = T, but p = F.'], 'counter_row')
    b.sa(8, 'cp1', 'An argument has premises p → q and ¬p and concludes ¬q. Give the row (p, q) that shows it is invalid, written like (T, F).', '(F, T)',
         ['Premises true, conclusion false: p = F (so ¬p = T and p → q = T) and q = T (so ¬q = F).'], 'counter_row')
    b.sa(8, 'honors', 'The argument p ∨ q, p → r ∴ r is invalid. Give the row (p, q, r) that makes the premises true and the conclusion false, written like (T, F, T).', '(F, T, F)',
         ['r must be F; then p → r forces p = F; then p ∨ q forces q = T.', 'Row (F, T, F).'], 'counter_row')
    b.sel(8, 'cp1', 'Which arguments commit the CONVERSE error?',
          [(FALL[0][0], True), (FALL[4][0], True), (FALL[1][0], False), (FALL[3][0], False), (FALL[7][0], True)],
          ['The converse error has the form p → q, q ∴ p.'], 'fallacy_select')
    b.sel(8, 'cp2', 'Which arguments are VALID?', [(FALL[2][0], True), (FALL[3][0], True), (FALL[0][0], False), (FALL[1][0], False), (FALL[5][0], False)],
          ['Modus ponens and modus tollens are valid; the converse and inverse errors are not.'], 'fallacy_select')
    b.sel(8, 'honors', 'Which statements about invalid arguments are correct?',
          [('An invalid argument can have a true conclusion.', True), ('An invalid argument can have all true premises and a true conclusion.', True),
           ('If the conclusion is true, the argument is valid.', False), ('A valid argument with true premises has a true conclusion.', True),
           ('A valid argument always has true premises.', False)],
          ['Validity is about form: it guarantees a true conclusion only when all premises are true.', 'Converse-error arguments often have true conclusions by luck.'], 'fallacy_select')
    b.orq(8, 'cp2', 'Argument: "If an animal is a dog, it has four legs. My pet has four legs. So my pet is a dog."',
          [('Write the form with p and q.', 'p → q, q ∴ p'), ('Name the error.', 'Converse error'), ('Give an example that shows the conclusion need not follow.', 'A cat has four legs but is not a dog.'),
           ('Change the second premise to make a valid argument.', 'My pet is a dog. (Then it has four legs, by modus ponens.)')],
          ['Translate.', 'Affirming the conclusion.', 'Counterexample.', 'Use modus ponens.'], 'fallacy_or')
    b.orq(8, 'cp1', 'Show that p → q, ¬p ∴ ¬q is invalid.',
          [('Which row (p, q) makes both premises true?', '(F, T) and (F, F)'), ('In which of those rows is the conclusion false?', '(F, T)'),
           ('What is this error called?', 'Inverse error'), ('Give an everyday example of the error.', 'If it rains, the road is wet. It did not rain. So the road is not wet (but a sprinkler could wet it).')],
          ['p must be F.', '¬q is F when q is T.', 'Denying the hypothesis.', 'Any example works.'], 'fallacy_or')
    b.orq(8, 'honors', 'Proof by contradiction uses the rule: if ¬p → c, where c is a contradiction, then p.',
          [('Explain why ¬p → c forces p to be true.', 'c is always false, so ¬p → c is true only if ¬p is false.'),
           ('Verify that (¬p → (q ∧ ¬q)) → p is a tautology. Give its column (p, q order).', LG.colstr('(¬p → (q ∧ ¬q)) → p')),
           ('Suppose "√2 is rational" leads to "a/b is in lowest terms and a, b are both even." Identify c.', 'c: "a and b have no common factor and a, b are both even" — a contradiction.'),
           ('What conclusion follows?', '√2 is irrational.')],
          ['A true conditional with a false conclusion has a false hypothesis.', 'All T.', 'The derived statement cannot be true.', 'Contradiction rule.'], 'contradiction_or')


# ---------------------------------------------------------------- errors
def errors(b):
    E = b.err
    E(1, 'cp2', 'Let p be T and q be F. Find the truth value of p ∨ q.', 'Jordan', ['p ∨ q means both must be true. q is F, so p ∨ q is F.'],
      'T', 'Jordan treated ∨ like ∧. In logic, "or" is inclusive: p ∨ q is true when at least one part is true.', '∨ needs only one true part.', ['p is T, so p ∨ q is T.'], 'or_as_and_error')
    E(3, 'cp2', 'Use De Morgan\'s law to negate "Lee is tall and Kim is short."', 'Sam', ['Negation: "Lee is not tall and Kim is not short."'],
      'Lee is not tall or Kim is not short.', 'Sam negated each part but kept "and". De Morgan changes ∧ to ∨.', '¬(p ∧ q) ≡ ¬p ∨ ¬q.', ['Negate each part and switch "and" to "or".'], 'demorgan_and_error')
    E(6, 'cp2', 'Write the contrapositive of "If it is a dog, then it barks."', 'Riley', ['Contrapositive: "If it is not a dog, then it does not bark."'],
      'If it does not bark, then it is not a dog.', 'Riley wrote the inverse (negated both parts without swapping).', 'The contrapositive swaps AND negates.', ['¬q → ¬p.'], 'inverse_for_contra_error')
    E(2, 'cp2', 'Give the truth column of p → q (order TT, TF, FT, FF).', 'Casey', ['p → q: T, F, F, F (true only when both are true).'],
      'TFTT', 'Casey treated → like ∧. A conditional is false only when p is T and q is F.', 'Rows with p false make p → q true.', ['TT → T, TF → F, FT → T, FF → T.'], 'cond_as_and_error')
    E(8, 'cp2', 'If it rains, the grass is wet. The grass is wet. What can you conclude?', 'Avery', ['It rained.'],
      'Nothing definite: the argument p → q, q ∴ p is invalid', 'Avery made the converse error; the grass could be wet for another reason.', 'Affirming the conclusion is invalid.', ['Row p = F, q = T makes the premises true and "it rained" false.'], 'converse_error_error')
    E(5, 'cp2', 'Negate "If I win, I celebrate."', 'Morgan', ['Negation: "If I win, I do not celebrate."'],
      'I win and I do not celebrate.', 'Morgan wrote another conditional. ¬(p → q) is p ∧ ¬q.', 'Both "If I win, I celebrate" and "If I win, I do not celebrate" are true when I do not win, so one is not the negation of the other.', ['¬(p → q) ≡ p ∧ ¬q.'], 'neg_cond_error')
    E(3, 'cp1', 'Decide whether ¬(p ∧ q) and ¬p ∧ ¬q are equivalent.', 'Taylor', ['Row TT: both F. Row FF: both T. They match, so they are equivalent.'],
      'Not equivalent (they differ in rows TF and FT)', 'Taylor checked only two rows. Equivalence requires matching in EVERY row.', 'Row TF: ¬(p ∧ q) = T but ¬p ∧ ¬q = F.', ['Columns: FTTT versus FFFT.'], 'partial_rows_error')
    E(4, 'cp1', 'Rewrite p → q using ¬ and ∨.', 'Jamie', ['p → q ≡ p ∨ ¬q.'],
      '¬p ∨ q', 'Jamie negated the wrong part. p ∨ ¬q is equivalent to q → p, the converse.', 'p → q is false only in row TF, like ¬p ∨ q.', ['Check row TF: ¬p ∨ q = F ∨ F = F.'], 'cond_rewrite_error')
    E(7, 'cp1', 'Premises: p → q and ¬q. Conclude and name the rule.', 'Quinn', ['From ¬q we get ¬p by modus ponens.'],
      '¬p, by modus tollens', 'Quinn named the wrong rule. Modus ponens uses p to get q; denying the conclusion is modus tollens.', 'Rule names describe the form.', ['p → q, ¬q ∴ ¬p is modus tollens.'], 'rule_name_error')
    E(6, 'cp1', 'Statement: "If x = 3, then x² = 9" is true. Is its converse true?', 'Alex', ['A statement and its converse are equivalent, so the converse is true.'],
      'No; x = −3 gives x² = 9 but x ≠ 3', 'Alex confused the converse with the contrapositive. Only the contrapositive is always equivalent.', 'The converse can be false when the statement is true.', ['Converse: if x² = 9, then x = 3. Counterexample x = −3.'], 'converse_equiv_error')
    E(2, 'cp1', 'How many rows does a truth table for (p ∧ q) ∨ (r ∧ s) need?', 'Jordan', ['There are 2 operations joined by ∨, so 2 · 2 = 4 rows.'],
      '16', 'Jordan counted operations instead of variables. Each of the 4 variables doubles the number of rows.', 'Rows = 2^(number of variables).', ['2⁴ = 16.'], 'row_count_error')
    E(8, 'cp1', 'Is p → q, ¬p ∴ ¬q valid?', 'Sam', ['Yes. If p causes q, then without p there is no q.'],
      'Invalid (inverse error)', 'Sam assumed p is the only way to get q. Row p = F, q = T makes both premises true and ¬q false.', 'Denying the hypothesis is a fallacy.', ['Counterexample row (F, T).'], 'inverse_error_error')
    E(3, 'honors', 'Simplify ¬(p → q) ∨ q.', 'Riley', ['¬(p → q) ≡ ¬p → ¬q, so the statement is (¬p → ¬q) ∨ q ≡ (p ∨ ¬q) ∨ q, which is a tautology.'],
      'p ∨ q', 'Riley negated the conditional incorrectly. ¬(p → q) ≡ p ∧ ¬q, not ¬p → ¬q.', 'The negation of a conditional is a conjunction.', ['(p ∧ ¬q) ∨ q ≡ (p ∨ q) ∧ (¬q ∨ q) ≡ p ∨ q.'], 'neg_cond_simplify_error')
    E(7, 'honors', 'Premises: p ∨ q, p → r, q → s. Does r follow?', 'Casey', ['Use the first case: p, so r by modus ponens. Therefore r.'],
      'No; only r ∨ s follows (constructive dilemma)', 'Casey used only one case of the disjunction. If q is the true part, we get s, not r.', 'Division into cases must handle every case.', ['Case p gives r; case q gives s; so r ∨ s.', 'Row p = F, q = T, r = F, s = T shows r does not follow.'], 'one_case_error')
    E(5, 'honors', 'Negate "For every x, if x is a square then x is a rectangle."', 'Avery', ['There exists x such that if x is a square, then x is not a rectangle.'],
      'There exists x such that x is a square and x is not a rectangle.', 'Avery negated the quantifier correctly but kept a conditional.', '¬∀x(P → Q) ≡ ∃x(P ∧ ¬Q).', ['Change ∀ to ∃ and P → Q to P ∧ ¬Q.'], 'neg_quant_cond_error')
    E(6, 'honors', 'Find the contrapositive of (p ∧ q) → r.', 'Morgan', ['¬r → (¬p ∧ ¬q)'],
      '¬r → (¬p ∨ ¬q)', 'Morgan negated p ∧ q as ¬p ∧ ¬q. By De Morgan, ¬(p ∧ q) ≡ ¬p ∨ ¬q.', 'The contrapositive negates the whole hypothesis.', ['¬r → ¬(p ∧ q) ≡ ¬r → (¬p ∨ ¬q).'], 'contra_demorgan_error')
    E(1, 'honors', 'Translate "x is between 2 and 5, inclusive, or x is negative" with p: x ≥ 2, q: x ≤ 5, r: x < 0.', 'Taylor', ['p ∨ q ∨ r'],
      '(p ∧ q) ∨ r', 'Taylor joined the two inequalities with ∨. "Between" needs both inequalities: p ∧ q.', 'x = 100 satisfies p ∨ q ∨ r but is not between 2 and 5 or negative.', ['Between 2 and 5 inclusive: p ∧ q.', 'Then add "or r".'], 'between_error')
    E(8, 'honors', 'Prove "there is no largest integer" by contradiction.', 'Jamie', ['Suppose there is a largest integer N. Then N = 1,000,000 is very large. 1,000,001 is larger, so the claim is false. Contradiction.'],
      'Assume a largest integer N exists; N + 1 is an integer greater than N, contradicting that N is largest.', 'Jamie replaced the arbitrary N with a specific number. The contradiction must be reached for any N, not for one example.', 'A specific example does not refute the assumption.', ['Let N be any supposed largest integer.', 'N + 1 > N and N + 1 is an integer.'], 'specific_contradiction_error')


def topup(b):
    def need(sk, L):
        return b.counter.get((sk, L), 0) < 10
    rows3 = ['p, q, r'] 
    # skill 2: three-variable columns (short answer)
    for L, f in (('honors', '(p ∨ q) → r'), ('honors', '¬p ∧ (q ↔ r)'), ('cp2', 'p ∨ (p ∧ q)')):
        if need(2, L):
            vs = LG.variables(f)
            b.sa(2, L, 'Give the truth column of %s as a string of T and F in the %s.' % (f, ORDER3 if len(vs) == 3 else ORDER2), LG.colstr(f, vs),
                 ['Evaluate the inner parts first in each row.', 'Column: ' + LG.colstr(f, vs)], 'tt_column')
    # skill 4: biconditional evaluation
    for L, f, env in (('cp2', 'p ↔ q', {'p': True, 'q': False}), ('honors', '(p → q) ↔ (¬q → ¬p)', {'p': True, 'q': False}), ('honors', '(p ↔ q) → r', {'p': False, 'q': False, 'r': False})):
        if need(4, L):
            v = LG.ev(LG.parse(f), env)
            b.mc(4, L, 'If %s, what is the truth value of %s?' % (tvs(env), f), 'True' if v else 'False', ['False' if v else 'True', 'Neither, because a biconditional needs both parts true', 'Cannot be determined'],
                 ['p ↔ q is true when p and q have the same truth value; a → b is false only when a is T and b is F.', 'Value: %s.' % ('T' if v else 'F')], 'bicond_eval')
    # skill 5: truth value of a negated conditional at given values
    for L, f, env in (('cp2', '¬(p → q)', {'p': True, 'q': False}), ('cp1', '¬(p → q)', {'p': False, 'q': False}), ('cp1', '¬(¬p → q)', {'p': False, 'q': False}),
                      ('honors', '¬((p ∧ q) → r)', {'p': True, 'q': True, 'r': False}), ('cp2', '¬(p → q)', {'p': True, 'q': True})):
        if need(5, L):
            v = LG.ev(LG.parse(f), env)
            b.sa(5, L, 'Let %s. Find the truth value of %s. Answer T or F.' % (tvs(env), f), 'T' if v else 'F',
                 ['¬(a → b) ≡ a ∧ ¬b, so it is true only when a is T and b is F.', 'Value: %s.' % ('T' if v else 'F')], 'neg_cond_eval')
    # skill 6: identify the form
    for L, given, kind in (('cp2', '¬q → ¬p', 'contrapositive'), ('honors', '¬p → ¬q', 'inverse'), ('cp1', 'q → p', 'converse')):
        if need(6, L):
            b.mc(6, L, 'Relative to the statement p → q, what is %s?' % given, 'Its ' + kind, ['Its ' + k for k in ('converse', 'inverse', 'contrapositive', 'negation') if k != kind],
                 ['Converse q → p, inverse ¬p → ¬q, contrapositive ¬q → ¬p, negation p ∧ ¬q.', given + ' is the ' + kind + '.'], 'cic_name')
    # skill 7: symbolic validity
    for L, prem, conc in (('cp2', ['p ∧ q'], 'q'), ('cp1', ['p → q', 'r → q'], 'p → r'), ('honors', ['(p ∧ q) → r', 'p', '¬r'], '¬q')):
        if need(7, L):
            ok, cx = LG.valid(prem, conc)
            b.mc(7, L, 'Is this argument form valid?\n' + '\n'.join(prem) + '\n∴ ' + conc, 'Valid' if ok else 'Invalid',
                 ['Invalid' if ok else 'Valid', 'Valid only if the premises are true', 'It depends on the meaning of p, q and r'],
                 ['Look for a row with every premise true and the conclusion false.', 'No such row exists, so it is valid.' if ok else
                  'Row %s is such a row, so it is invalid.' % ', '.join('%s=%s' % (k, 'T' if v else 'F') for k, v in cx.items())], 'symbolic_valid')
    # skill 8: counterexample rows (computed)
    for L, prem, conc in (('cp2', ['p → q', 'q'], 'p'), ('cp1', ['p ∨ q', 'q'], '¬p'), ('honors', ['p → r', 'q → r', 'r'], 'p ∨ q')):
        if need(8, L):
            ok, cx = LG.valid(prem, conc)
            assert not ok
            vs = sorted(cx)
            b.sa(8, L, 'Show the argument is invalid: give a row (%s) that makes every premise true and the conclusion false. Premises: %s. Conclusion: %s. Write the row like %s.' %
                 (', '.join(vs), ', '.join(prem), conc, '(' + ', '.join(['T'] * len(vs)) + ')'),
                 '(' + ', '.join('T' if cx[v] else 'F' for v in vs) + ')',
                 ['Make the conclusion false first, then choose the remaining values so every premise is true.',
                  'Row: (' + ', '.join('T' if cx[v] else 'F' for v in vs) + ').'], 'counter_row',
                 notes='The key is the first counterexample row in standard order (computed by logic.valid); verify_banks.py accepts any counterexample row only for this family.')


def topup2(b):
    NEW5 = [('cp1', 'If the bus is late, then I take a taxi.', 'The bus is late and I do not take a taxi.', ['If the bus is late, then I do not take a taxi.', 'The bus is not late and I take a taxi.', 'If the bus is not late, then I take a taxi.']),
            ('honors', 'If a function is linear, then its graph is a line or it is undefined somewhere.', 'The function is linear, its graph is not a line, and it is defined everywhere.',
             ['The function is linear, and its graph is not a line or it is defined everywhere.', 'If the function is not linear, then its graph is not a line and it is defined everywhere.', 'The function is not linear, or its graph is a line.']),
            ('honors', 'For all integers n, if n² is divisible by 4, then n is divisible by 4.', 'There is an integer n such that n² is divisible by 4 and n is not divisible by 4 (for example n = 2).',
             ['For all integers n, if n² is divisible by 4, then n is not divisible by 4.', 'There is an integer n such that n² is not divisible by 4 and n is divisible by 4.', 'For all integers n, n² is divisible by 4 and n is not divisible by 4.'])]
    for L, st, good, bad in NEW5:
        b.mc(5, L, 'Which is the negation of "%s"?' % st, good, bad, ['¬(p → q) ≡ p ∧ ¬q; with a quantifier, ¬∀x(P → Q) ≡ ∃x(P ∧ ¬Q); ¬(a ∨ b) ≡ ¬a ∧ ¬b.', 'Negation: ' + good], 'negate_conditional')
    b.mc(8, 'honors', 'Classify the argument:\nIf the program has a bug, the test fails. If the test fails, the build stops. The build stopped. So the program has a bug.',
         'Converse error (affirming the conclusion)', ['Valid (modus ponens)', 'Valid (modus tollens)', 'Inverse error (denying the hypothesis)'],
         ['Form: p → q, q → r, r ∴ p. Row p = F, q = T, r = T makes every premise true and the conclusion false.', 'Converse error.'], 'classify_fallacy')
    assert not LG.valid(['p → q', 'q → r', 'r'], 'p')[0]


def topup3(b):
    b.mc(2, 'cp2', 'How many rows are in the truth table for p ∧ q?', '4', ['2', '3', '8'], ['Two variables: 2² = 4 rows (TT, TF, FT, FF).'], 'tt_rows', order='sort')
