"""8th Grade Math audit (2026-11-19), batch A content fixes.

#5  rewrite the 90 Tarsia filler items as on-skill short items that differ by level
#6  vary the number of correct options in select-all items (2-4 instead of always 3; the bank schema needs at least 2)
#8  12 proportional-relationship items with graphs (skill 12 of Linear and Functional Relationships)
#11 fix the simplest-radical-form key; write the other exact distance in simplest form
#12 leftover generator wording (vertices, double spaces, "+ 0", "1x", "a 8-foot", "$10.9", ...)
#13 pi answers written (2048/3)π instead of 2048/3π
#16 replace the 7 exponential equations in "Solving x² = p and x³ = p equations"
#17 add the final computed step where the steps stop before the answer

Run from the repository root: python3 tools/grade8-audit-20261119/batch_a.py
Every change is idempotent: running the script twice leaves the banks unchanged the second time.
"""
import json, math, os, re, sys
from fractions import Fraction as Fr

sys.path.insert(0, os.path.dirname(__file__))
from lib import ROOT, load, save, items, byid, family, set_family

NOTE = ("Original Claude-authored item (family: {fam}). 8th Grade Math audit 2026-11-19; answer recomputed by "
        "scripts/test-grade8-audit.cjs.")


# ---------------------------------------------------------------- text helpers
def map_text(q, fn):
    """Apply fn to every student-facing string of an item, keeping MC / select-all keys consistent."""
    q['prompt'] = fn(q['prompt'])
    if isinstance(q.get('answer'), str):
        q['answer'] = fn(q['answer'])
    elif isinstance(q.get('answer'), list):
        q['answer'] = [fn(a) if isinstance(a, str) else a for a in q['answer']]
    for o in q.get('options') or []:
        if isinstance(o.get('text'), str):
            o['text'] = fn(o['text'])
    q['solutionSteps'] = [fn(s) for s in q.get('solutionSteps') or []]
    for p in q.get('parts') or []:
        for k in ('prompt', 'answer'):
            if isinstance(p.get(k), str):
                p[k] = fn(p[k])
    if q.get('diagram') and q['diagram'].get('spec', {}).get('alt'):
        q['diagram']['spec']['alt'] = fn(q['diagram']['spec']['alt'])


def wording(s):
    s = re.sub(r'(?<!vertices )\b((?:[A-Z]′?){3,4}) (?=[A-Z]′?\(-?\d)', r'\1 with vertices ', s)
    s = re.sub(r' {2,}', ' ', s)
    s = re.sub(r' \+ 0(?= ?(?:=|have\b|has\b|when\b|\)|[.,;]|$))', '', s)
    s = re.sub(r'(?<![\w.²³)⁰¹⁴-⁹])1\((?=[a-z])', '(', s)
    s = re.sub(r'(?<![\w.²³)⁰¹⁴-⁹/])1([a-z])(?![a-z\d(])', r'\1', s)
    s = re.sub(r'\b([Aa]) (8|11|18|8\d)(?=[- ])', r'\1n \2', s)
    s = re.sub(r'\$(\d+\.\d)(?!\d)', r'$\g<1>0', s)
    s = re.sub(r'There are 1 more (\w+?)s than (\w+)', r'There is 1 more \1 than there are \2', s)
    s = s.replace('Quadrilateral wxyz', 'Quadrilateral WXYZ')
    s = re.sub(r'(?<![\w(./)])(\d+)/(\d+)π', r'(\1/\2)π', s)
    return s


def fix_wording(banks):
    n = 0
    for _, q in items(banks):
        before = json.dumps(q, ensure_ascii=False)
        map_text(q, wording)
        if json.dumps(q, ensure_ascii=False) != before:
            n += 1
    return n


# ---------------------------------------------------------------- #11
def fix_radicals(Q):
    q = Q['pa8-geo-s01-honors-001']
    q['answer'] = '2√10 cm'
    q['solutionSteps'] = ['c² = 6² + 2² = 36 + 4 = 40.', 'c = √40 = √(4 · 10) = 2√10 cm.']
    q = Q['pa8-geo-s04-honors-017']
    q['answer'] = '2√34 units'
    q['solutionSteps'] = ['d² = (-4 - 6)² + (-6 - 0)² = 100 + 36 = 136.', 'd = √136 = √(4 · 34) = 2√34 units.']


# ---------------------------------------------------------------- #16
EXP_REPLACE = {
    'pa8-eqx-s08-cp1-004': ('s8_cube_two_step', 'Solve: 2x³ = 54', 'x = 3', None,
                            ['Divide both sides by 2: x³ = 27.', 'Take the cube root: x = ∛27 = 3.']),
    'pa8-eqx-s08-cp1-008': ('s8_cube_two_step', 'Solve: x³ + 4 = 68', 'x = 4', ['x = 4', 'x = 64', 'x = 8', 'x = 4 or x = -4'],
                            ['Subtract 4 from both sides: x³ = 64.', 'Take the cube root: x = ∛64 = 4. A cube root has only one real value.']),
    'pa8-eqx-s08-cp1-012': ('s8_two_step', 'Solve: x² - 7 = 74', 'x = 9 or x = -9', None,
                            ['Add 7 to both sides: x² = 81.', 'Take the square root of both sides: x = ±√81, so x = 9 or x = -9.']),
    'pa8-eqx-s08-cp1-016': ('s8_two_step', 'Solve: 5x² = 80', 'x = 4 or x = -4', None,
                            ['Divide both sides by 5: x² = 16.', 'Take the square root of both sides: x = 4 or x = -4.']),
    'pa8-eqx-s08-honors-004': ('s8_shifted_cube', 'Solve: (x + 1)³ = -8', 'x = -3', None,
                               ['Take the cube root of both sides: x + 1 = ∛(-8) = -2.', 'Subtract 1: x = -3.']),
    'pa8-eqx-s08-honors-009': ('s8_shifted_square', 'Solve: (x - 3)² = 49', 'x = 10 or x = -4',
                               ['x = 10', 'x = 10 or x = -4', 'x = 52', 'x = 10 or x = -10'],
                               ['Take the square root of both sides: x - 3 = 7 or x - 3 = -7.', 'Add 3: x = 10 or x = -4.']),
    'pa8-eqx-s08-honors-014': ('s8_cube_two_step', 'Solve: 2x³ + 5 = -11', 'x = -2', None,
                               ['Subtract 5 from both sides: 2x³ = -16.', 'Divide by 2: x³ = -8.', 'Take the cube root: x = -2.']),
}


def fix_exponential(Q):
    for qid, (fam, prompt, ans, opts, steps) in EXP_REPLACE.items():
        q = Q[qid]
        q['prompt'], q['answer'], q['solutionSteps'] = prompt, ans, steps
        if opts:
            # keep the correct option's position: rotate so that the key lands where the old key was
            old = [o['correct'] for o in q['options']].index(True)
            wrong = [o for o in opts if o != ans]
            new = wrong[:]
            new.insert(old, ans)
            q['options'] = [{'text': t, 'correct': t == ans} for t in new]
        set_family(q, fam)
        q['sourceNotes'] = NOTE.format(fam=fam)


# ---------------------------------------------------------------- #17
def final_step(q):
    a, p, fam = str(q['answer']), q['prompt'], family(q)
    if fam == 's5_measure':
        if 'perimeter' in p:
            P, k = re.search(r'perimeter (\d+) cm', p).group(1), re.search(r'scale factor (\S+?)\?', p).group(1)
            return f'{P} × {k} = {a}.'
        if 'area' in p:
            A, k = re.search(r'area (\d+)', p).group(1), re.search(r'scale factor (\S+?)\?', p).group(1)
            kk = Fr(k)
            return f'{A} × ({k})² = {A} × {kk * kk} = {a}.'
        return f'The matching angle still measures {a}.'
    if fam == 's8_no_real':
        return 'So the equation has 0 real solutions.'
    if fam == 's7_silo':
        tot = re.search(r'Total \(?(\d+)/3\)?π', ' '.join(q['solutionSteps'])).group(1)
        return f'With π ≈ 3.14: ({tot}/3)(3.14) ≈ {a}.'
    if fam == 's6_translate':
        return f'The new equation is {a}.'
    if fam == 's10_read_context':
        m = re.search(r'from t = (\d+) to t = (\d+)', ' '.join(q['solutionSteps']))
        if m:
            return f'{m.group(2)} - {m.group(1)} = {a}.'
        return f'The highest point is at {a} from camp.'
    if fam == 's11_from_story':
        return f'So the graph has {a}.'
    if fam == 's4_interpret':
        return f'Here: {a}'
    if fam == 's4_count_irr':
        irr = [s.split(':')[0] for s in q['solutionSteps'] if s.endswith('irrational.')]
        return f'Irrational: {", ".join(irr)}, so {a} numbers are irrational.'
    if fam == 's8_rewrite':
        expr = re.search(r'Rewrite (.+?) using', p).group(1)
        return f'{expr} = {a}.'
    if fam == 's10_context':
        expr = re.search(r'about (.+? × 10\S+)', p).group(1)
        return f'{expr} = {a}.'
    return f'So the answer is {a}.'


def fix_final_steps(banks):
    n = 0
    for _, q in items(banks):
        if q['format'] != 'short-answer':
            continue
        a, st = str(q['answer']), ' '.join(q.get('solutionSteps') or [])
        nums = re.findall(r'-?\d+(?:\.\d+)?(?:/\d+)?', a)
        if nums and not all(x.lstrip('-') in st for x in nums):
            q['solutionSteps'].append(final_step(q))
            n += 1
    return n


# ---------------------------------------------------------------- #5 Tarsia items
def tarsia_items():
    """10 items per skill (04 lines of best fit, 05 constructing two-way tables, 06 interpreting two-way tables) and level,
    numbered 001-010, 011-020 and 021-030 as before. Answers are distinct inside each skill and level."""
    out = {}
    lv = ['cp2', 'cp1', 'honors']
    for L in lv:
        rows = []
        # skill 04: lines of best fit (8.SP.A.3)
        for i in range(10):
            if L == 'cp2':
                m, b, x = 2 + i % 4, 10 + 5 * i, 3 + i
                y = m * x + b
                rows.append(('04', f'A best-fit line is y = {m}x + {b}. Predict y when x = {x}.', str(y),
                             [f'Substitute x = {x} into y = {m}x + {b}.', f'y = {m * x} + {b} = {y}.'], ['8.SP.A.3']))
            elif L == 'cp1':
                if i < 5:
                    m, b, x = Fr(1, 2) + i, 20 + 4 * i, 4 + 2 * i
                    ms = f'{float(m):g}'
                    y = m * x + b
                    rows.append(('04', f'A best-fit line is y = {ms}x + {b}. Predict y when x = {x}.', f'{float(y):g}',
                                 [f'Substitute x = {x}: y = {ms}({x}) + {b}.', f'y = {float(m * x):g} + {b} = {float(y):g}.'], ['8.SP.A.3']))
                else:
                    m, b, x = -(2 + i % 3), 90 + 5 * i, 3 + i
                    y = m * x + b
                    rows.append(('04', f'A best-fit line is y = {m}x + {b}. Predict y when x = {x}.', str(y),
                                 [f'Substitute x = {x}: y = {m}({x}) + {b}.', f'y = {m * x} + {b} = {y}.'], ['8.SP.A.3']))
            else:
                if i < 6:
                    m, b, x = 3 + i % 3, 12 + 4 * i, 5 + i
                    y = m * x + b
                    rows.append(('04', f'A best-fit line y = {m}x + {b} predicts y = {y}. For what value of x?', f'x = {x}',
                                 [f'Solve {m}x + {b} = {y}.', f'{m}x = {y - b}, so x = {x}.'], ['8.SP.A.3']))
                else:
                    m, b = Fr(5 + 2 * (i - 6), 2), 40 + 3 * i
                    ms = f'{float(m):g}'
                    k = 4 + 2 * (i - 6)
                    rows.append(('04', f'Test score = {ms}h + {b} (h = hours studied). How much higher is the predicted score for {k} more hours?',
                                 f'{float(m * k):g} points',
                                 [f'The slope {ms} is the increase per hour.', f'{ms} × {k} = {float(m * k):g} points.'], ['8.SP.A.3']))
        # skill 05: constructing two-way tables (8.SP.A.4)
        for i in range(10):
            if L == 'cp2':
                a, b = 12 + i, 5 + 2 * i
                rows.append(('05', f'In a two-way table, {a} grade 7 students play a sport and {b} do not. What is the grade 7 row total?',
                             str(a + b), [f'A row total adds across the row.', f'{a} + {b} = {a + b}.'], ['8.SP.A.4']))
            elif L == 'cp1':
                r7, r8, sport = 24 + i, 30 + 2 * i, 31 + 2 * i
                g = r7 + r8
                rows.append(('05', f'A two-way table has row totals {r7} (grade 7) and {r8} (grade 8). {sport} students play a sport. How many do not?',
                             str(g - sport), [f'Grand total = {r7} + {r8} = {g}.', f'Do not play = {g} - {sport} = {g - sport}.'], ['8.SP.A.4']))
            else:
                a, b, c, tot = 10 + i, 8 + i, 12, 30 + 3 * i
                x = tot - a
                rows.append(('05', f'Grade 7: {a} play a sport, {b} do not. Grade 8: x play, {c} do not. {tot} play a sport in all. Find x.',
                             f'x = {x}', [f'The "play a sport" column total is {tot}.', f'{a} + x = {tot}, so x = {x}.'], ['8.SP.A.4']))
        # skill 06: interpreting two-way tables, relative frequency (8.SP.A.4)
        for i in range(10):
            if L == 'cp2':
                k, n = [(5, 20), (6, 30), (9, 24), (8, 28), (10, 25), (12, 44), (14, 21), (15, 36), (21, 28), (16, 36)][i]
                f = Fr(k, n)
                rows.append(('06', f'Of {n} grade 8 students, {k} ride a bike to school. What fraction ride a bike? Simplify.',
                             f'{f.numerator}/{f.denominator}' if f.denominator != 1 else str(f.numerator),
                             [f'Relative frequency = {k} ÷ {n} = {k}/{n}.', f'Simplified: {f.numerator}/{f.denominator}.'], ['8.SP.A.4']))
            elif L == 'cp1':
                n = [20, 25, 40, 50, 80, 20, 25, 40, 50, 80][i]
                pct = [15, 32, 45, 62, 85, 35, 72, 65, 18, 55][i]
                k = n * pct // 100
                rows.append(('06', f'In grade 7, {k} of {n} students have a pet. What percent of grade 7 students have a pet?',
                             f'{pct}%', [f'{k} ÷ {n} = {k / n:g}.', f'{k / n:g} = {pct}%.'], ['8.SP.A.4']))
            else:
                n7, p7, n8, p8 = [(20, 60, 25, 40), (25, 40, 40, 65), (40, 75, 50, 40), (50, 30, 20, 45), (20, 45, 40, 55),
                                  (25, 80, 20, 50), (40, 35, 25, 80), (50, 70, 40, 30), (20, 85, 40, 35), (25, 24, 50, 26)][i]
                k7, k8 = n7 * p7 // 100, n8 * p8 // 100
                d = abs(p7 - p8)
                hi = 'grade 7' if p7 > p8 else 'grade 8'
                rows.append(('06', f'Grade 7: {k7} of {n7} ride a bus. Grade 8: {k8} of {n8} ride a bus. How many percentage points higher is {hi}?',
                             str(d), [f'Grade 7: {k7} ÷ {n7} = {p7}%. Grade 8: {k8} ÷ {n8} = {p8}%.', f'{max(p7, p8)} - {min(p7, p8)} = {d} percentage points.'],
                             ['8.SP.A.4']))
        for j, (sk, prompt, ans, steps, std) in enumerate(rows):
            qid = f'pa8-biv-tarsia-{L}-{j + 1:03d}'
            out[qid] = dict(skill='patterns-bivariate-data-skill-' + sk, prompt=prompt, answer=ans, steps=steps, std=std)
    return out


def fix_tarsia(Q):
    new = tarsia_items()
    for qid, d in new.items():
        q = Q[qid]
        assert q['skillId'] == d['skill'], (qid, q['skillId'], d['skill'])
        assert len(d['prompt']) <= 110 and len(d['answer']) <= 20, (qid, len(d['prompt']), d['answer'])
        q['prompt'], q['answer'], q['solutionSteps'], q['standards'] = d['prompt'], d['answer'], d['steps'], d['std']
        q['sourceNotes'] = ('Compact Tarsia item (8th Grade Math audit 2026-11-19): short enough for Tarsia puzzles and checked '
                            'by scripts/test-grade8-audit.cjs.')
    # distinct answers per skill and level (Tarsia edges must not repeat)
    seen = {}
    for qid, d in new.items():
        k = (d['skill'], qid.split('-')[3])
        seen.setdefault(k, []).append(d['answer'])
    for k, v in seen.items():
        assert len(v) == len(set(v)), (k, v)


# ---------------------------------------------------------------- #6 select-all
def fix_select_all(banks):
    SA = [q for _, q in items(banks) if q['format'] == 'select-all']
    by_prompt = {}
    for q in SA:
        by_prompt.setdefault((q['skillId'], q['prompt']), []).append(q)
    plan = {}
    three = [q for q in SA if sum(o['correct'] for o in q['options']) == 3 and len(q['options']) == 6
             and 'selectall-audit' not in q.get('sourceNotes', '') and 'audit 2026-11-19' not in q.get('sourceNotes', '')]
    for i, q in enumerate(three):
        plan[q["id"]] = [2, 4, 3, 2, 4, 3, 2, 3][i % 8]   # the bank schema needs at least two correct options
    done = {1: 0, 2: 0, 3: 0, 4: 0}
    for q in three:
        k = plan[q['id']]
        steps = ' '.join(q['solutionSteps'])
        if k == 4:
            sibs = [s for s in by_prompt[(q['skillId'], q['prompt'])] if s is not q]
            have = {o['text'] for o in q['options']}
            extra = [o['text'] for s in sibs for o in s['options'] if o['correct'] and o['text'] not in have]
            wrong = [o for o in q['options'] if not o['correct'] and o['text'] not in steps]
            if extra and wrong:
                wrong[-1]['text'], wrong[-1]['correct'] = extra[0], True
            else:
                k = 2
        if k == 2:
            corr = [o for o in q['options'] if o['correct']]
            corr.sort(key=lambda o: o['text'] in steps)          # drop options the steps do not mention first
            for o in corr[:3 - k]:
                q['options'].remove(o)
        q['answer'] = [o['text'] for o in q['options'] if o['correct']]
        q['sourceNotes'] = q.get('sourceNotes', '') + ' Correct-option count varied (selectall-audit 2026-11-19).'
        done[k] += 1
    return done


# ---------------------------------------------------------------- #8 proportional items with graphs
def prop_items():
    """(id, format, prompt, answer, options, steps, family, graph) ; graph = (lines, points, xmax, ymax, xlabel, ylabel)."""
    P = []
    # Support
    P.append(('cp2-017', 'short-answer', 'The graph shows the cost y (dollars) of x pounds of apples. What is the unit rate in dollars per pound?',
              '3 dollars per pound', None, ['The line passes through (0, 0) and (2, 6).', 'Unit rate = 6 ÷ 2 = 3 dollars per pound.'],
              'prop_graph_rate', ([(3, 'Apples')], [(2, 6)], 8, 24, 'pounds (x)', 'cost in dollars (y)')))
    P.append(('cp2-018', 'multiple-choice', 'Which equation represents the proportional relationship shown in the graph?',
              'y = 4x', ['y = 4x', 'y = x/4', 'y = x + 4', 'y = 8x'],
              ['The line passes through (0, 0) and (2, 8).', 'k = 8 ÷ 2 = 4, so y = 4x.'],
              'prop_graph_equation', ([(4, None)], [(2, 8)], 6, 24, 'x', 'y')))
    P.append(('cp2-019', 'select-all', 'Select ALL points on the graph of the proportional relationship y = 4x.',
              ['(1, 4)', '(3, 12)', '(0, 0)'], ['(1, 4)', '(4, 1)', '(3, 12)', '(2, 6)', '(0, 0)', '(5, 9)'],
              ['A point is on the graph when y = 4 × x.', '(1, 4), (3, 12) and (0, 0) work; (4, 1), (2, 6) and (5, 9) do not.'],
              'prop_points_select', None))
    P.append(('cp2-020', 'multiple-choice', 'Runner A is shown in the graph (x = minutes, y = laps). Runner B runs y = 2x laps in x minutes. Who runs faster?',
              'Runner A', ['Runner A', 'Runner B', 'They run at the same rate', 'It cannot be told'],
              ['Runner A: 6 laps in 2 minutes, so 3 laps per minute.', 'Runner B: 2 laps per minute. 3 > 2, so Runner A is faster.'],
              'prop_compare_graph', ([(3, 'Runner A')], [(2, 6)], 8, 24, 'minutes (x)', 'laps (y)')))
    # Standard
    P.append(('cp1-017', 'short-answer', 'The graph shows the distance y (miles) a cyclist rides in x hours. What is the unit rate in miles per hour?',
              '12.5 miles per hour', None, ['The line passes through (0, 0) and (4, 50).', 'Unit rate = 50 ÷ 4 = 12.5 miles per hour.'],
              'prop_graph_rate', ([(Fr(25, 2), 'Cyclist')], [(4, 50)], 8, 100, 'hours (x)', 'miles (y)')))
    P.append(('cp1-018', 'multiple-choice', 'The graph shows a proportional relationship. Which point on the graph shows the unit rate?',
              '(1, 2.5)', ['(1, 2.5)', '(2.5, 1)', '(0, 2.5)', '(2, 5)'],
              ['The line passes through (0, 0) and (2, 5), so the unit rate is 5 ÷ 2 = 2.5.', 'The unit rate is the y-value when x = 1: (1, 2.5).'],
              'prop_graph_unit_point', ([(Fr(5, 2), None)], [(2, 5)], 8, 20, 'x', 'y')))
    P.append(('cp1-019', 'select-all', 'The graph of a proportional relationship passes through (4, 6). Select ALL true statements.',
              ['The unit rate is 1.5.', 'The equation is y = 1.5x.', 'The graph passes through (0, 0).', 'The point (10, 15) is on the graph.'],
              ['The unit rate is 1.5.', 'The equation is y = 1.5x.', 'The graph passes through (0, 0).', 'The unit rate is 4/6.',
               'The point (10, 15) is on the graph.', 'The equation is y = x + 2.'],
              ['Unit rate = 6 ÷ 4 = 1.5, so y = 1.5x and the graph starts at (0, 0).', 'Check (10, 15): 1.5 × 10 = 15 ✓. 4/6 is x ÷ y, not y ÷ x; y = x + 2 is not proportional.'],
              'prop_statements_select', None))
    P.append(('cp1-020', 'short-answer', 'Pump A is shown in the graph (x = minutes, y = gallons). Pump B: x: 2, 5, 8; y: 9, 22.5, 36. How many more gallons per minute does the faster pump fill?',
              '0.5 gallons per minute', None,
              ['Pump A: 20 gallons in 5 minutes, so 4 gallons per minute.', 'Pump B: 9 ÷ 2 = 4.5 gallons per minute.', '4.5 - 4 = 0.5 gallons per minute (Pump B is faster).'],
              'prop_compare_graph_table', ([(4, 'Pump A')], [(5, 20)], 8, 32, 'minutes (x)', 'gallons (y)')))
    # Advanced
    P.append(('honors-017', 'short-answer', 'The graph shows two cars on a highway (x = hours, y = miles). How many more miles does Car A travel than Car B in 5 hours?',
              '50 miles', None,
              ['Car A: 130 miles in 2 hours, so 65 miles per hour. Car B: 110 miles in 2 hours, so 55 miles per hour.',
               'In 5 hours: 65 × 5 = 325 and 55 × 5 = 275.', '325 - 275 = 50 miles.'],
              'prop_two_graphs', ([(65, 'Car A'), (55, 'Car B')], [(2, 130), (2, 110)], 6, 400, 'hours (x)', 'miles (y)')))
    P.append(('honors-018', 'multiple-choice', 'The graph of a proportional relationship passes through (5, 8). Which point is also on the graph?',
              '(12.5, 20)', ['(12.5, 20)', '(8, 5)', '(10, 13)', '(6, 9)'],
              ['The unit rate is 8 ÷ 5 = 1.6, so y = 1.6x.', 'Check: 1.6 × 12.5 = 20 ✓. (10, 13) and (6, 9) add instead of multiply; (8, 5) swaps x and y.'],
              'prop_point_reason', None))
    P.append(('honors-019', 'select-all', 'Relationship A is shown in the graph. Relationship B is y = 2.5x. Select ALL true statements.',
              ['A has the greater unit rate.', 'Both graphs pass through (0, 0).'],
              ['A has the greater unit rate.', 'B has the greater unit rate.', 'Both graphs pass through (0, 0).',
               'At x = 6, A is 3 more than B.', 'The equation of A is y = 7x.'],
              ['A passes through (0, 0) and (3, 8), so its unit rate is 8/3 ≈ 2.67 > 2.5.',
               'At x = 6: A = 16 and B = 15, a difference of 1, not 3. y = 7x would pass through (1, 7), not (3, 8).'],
              'prop_compare_select', ([(Fr(8, 3), 'A')], [(3, 8)], 9, 24, 'x', 'y')))
    P.append(('honors-020', 'short-answer', 'The graph of a proportional relationship passes through (6, 15) and (x, 35). Find x.',
              'x = 14', None, ['The unit rate is 15 ÷ 6 = 2.5, so y = 2.5x.', '2.5x = 35, so x = 14.'], 'prop_missing_coordinate', None))
    return P


def plot_prop(path, lines, points, xmax, ymax, xl, yl):
    import importlib.util
    os.environ.setdefault('PA8_OUT', '/tmp/pa8')
    spec = importlib.util.spec_from_file_location('pa8_authoring_lib', os.path.join(ROOT, 'tools', 'prealgebra-authoring', 'lib.py'))
    A = importlib.util.module_from_spec(spec)
    sys.path.insert(0, os.path.join(ROOT, 'tools', 'prealgebra-authoring'))
    spec.loader.exec_module(A)
    sys.path.pop(0)
    p = A.plt()
    fig, ax = A.new_fig(6.0, 4.8)
    ystep = {24: 4, 20: 2, 32: 4, 100: 10, 400: 50}[ymax]
    A.data_axes(ax, (0, xmax), (0, ymax), 1, ystep, xl, yl)
    for i, (m, lab) in enumerate(lines):
        ax.plot([0, xmax], [0, float(m) * xmax], color=A.COLORS[i], lw=2.4, ls='-' if i == 0 else '--', label=lab, clip_on=True)
    for j, (x, y) in enumerate(points):
        ax.plot([x], [y], 'o', color='black', ms=7, zorder=5, clip_on=False)
        ax.annotate(f'({x}, {y})', (x, y), textcoords='offset points', xytext=(-10, 10) if j == 0 else (10, -18),
                    ha='right' if j == 0 else 'left', fontsize=12, fontweight='bold')
    if any(l for _, l in lines):
        ax.legend(loc='upper left', fontsize=11, framealpha=0.95)
    A.save(fig, path)


def add_prop_items(banks):
    bank = banks['linear-functional-relationships']
    have = {q['id'] for q in bank['questions']}
    tags = json.load(open(os.path.join(ROOT, 'question-banks', 'prealgebra', 'meta', 'linear-functional-relationships.tags.json'), encoding='utf-8'))
    added = 0
    for (suffix, fmt, prompt, ans, opts, steps, fam, graph) in prop_items():
        qid = 'pa8-lfr-s12-' + suffix
        level = suffix.split('-')[0]
        q = {'id': qid, 'skillId': 'linear-functional-relationships-skill-12', 'level': level, 'format': fmt, 'prompt': prompt, 'answer': ans}
        if fmt == 'multiple-choice':
            q['options'] = [{'text': t, 'correct': t == ans} for t in opts]
        if fmt == 'select-all':
            q['options'] = [{'text': t, 'correct': t in ans} for t in opts]
        q['solutionSteps'] = steps
        q['standards'] = ['8.EE.B.5']
        q['sourceNotes'] = NOTE.format(fam=fam)
        if graph:
            rel = f'question-banks/assets/prealgebra/linear-functional-relationships/{qid}.png'
            plot_prop(os.path.join(ROOT, rel), *graph)
            names = ' and '.join(f'{l or "a line"} through (0, 0) and ({x}, {y})' for (_, l), (x, y) in zip(graph[0], graph[1]))
            q['diagram'] = {'type': 'image', 'spec': {'src': rel, 'alt': f'First-quadrant graph, x from 0 to {graph[2]} ({graph[4]}), y from 0 to {graph[3]} ({graph[5]}): {names}; the point{"s" if len(graph[1]) > 1 else ""} {", ".join(f"({x}, {y})" for x, y in graph[1])} marked.'}}
        if qid in have:
            old = next(x for x in bank['questions'] if x['id'] == qid)
            old.clear(); old.update(q)
        else:
            # insert after the last item of the same skill and level
            idx = max(i for i, x in enumerate(bank['questions']) if x['skillId'] == q['skillId'] and x['level'] == level)
            bank['questions'].insert(idx + 1, q)
            added += 1
        tags[qid] = ['graph', 'multiple-representations'] if graph else ['reasoning']
    with open(os.path.join(ROOT, 'question-banks', 'prealgebra', 'meta', 'linear-functional-relationships.tags.json'), 'w', encoding='utf-8') as fh:
        json.dump(tags, fh, ensure_ascii=False, indent=0)
    return added


def check_keys(banks):
    for _, q in items(banks):
        o = q.get('options') or []
        if q['format'] == 'multiple-choice':
            c = [x['text'] for x in o if x['correct']]
            assert len(c) == 1 and c[0] == q['answer'], q['id']
        if q['format'] == 'select-all':
            assert sorted(x['text'] for x in o if x['correct']) == sorted(q['answer']), q['id']
            assert 1 <= len(q['answer']) <= 4, q['id']
        t = [str(x.get('text')) for x in o]
        assert len(t) == len(set(t)), (q['id'], t)


if __name__ == '__main__':
    banks = load()
    Q = byid(banks)
    print('wording', fix_wording(banks))
    fix_radicals(Q)
    fix_exponential(Q)
    print('final steps', fix_final_steps(banks))
    fix_tarsia(Q)
    print('select-all', fix_select_all(banks))
    print('proportional added', add_prop_items(banks))
    check_keys(banks)
    save(banks)
