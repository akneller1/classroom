"""Algebra 2 audit (2026-11-17), batch A: notation, giveaways, rounding, find-the-mistake,
select-all answer counts and open-response stems. Idempotent: rerunning changes nothing."""
import re, json, os, sys
from lib import load, save, items, by_id, text_fields

B = load()
I = by_id(B)
log = []

# ---- #8 ambiguous inline fractions: 1/2√(x − 4) → (1/2)√(x − 4), 7/10i → (7/10)i, ±3/4x → ±(3/4)x
FRAC = re.compile(r'(?<![\w)\]/(])(\d+/\d+)(?=\s?[√∛]|i\b|[a-zπθ](?![a-z])|\()')


def fix_frac(s):
    return FRAC.sub(lambda m: '(' + m.group(1) + ')', s)


n8 = 0
for _, q in items(B):
    changed = False
    for get, put in text_fields(q):
        v = get()
        w = fix_frac(v)
        if w != v:
            put(w); changed = True
    n8 += changed
log.append(f'#8 fractions parenthesized in {n8} items')

# ÷ between two unbracketed fractions: (a)/(b) ÷ (c)/(d) → ((a)/(b)) ÷ ((c)/(d))
DIV = re.compile(r'(?<![(\w])(\([^()]*\)/\([^()]*\)|\([^()]*\)/\w+|\w+/\([^()]*\)) ÷ (\([^()]*\)/\([^()]*\)|\([^()]*\)/\w+|\w+/\([^()]*\))(?!\))')
n8b = 0
for _, q in items(B):
    v = q['prompt']
    w = DIV.sub(lambda m: '(' + m.group(1) + ') ÷ (' + m.group(2) + ')', v)
    if w != v:
        q['prompt'] = w; n8b += 1
log.append(f'#8 division prompts bracketed: {n8b}')

# ---- #9 giveaways
PER = re.compile(r'between (\d+) and (\d+) feet, repeating every (\d+) (hours|seconds)\. What is the period of the model\?')
n9 = 0
for _, q in items(B):
    m = PER.search(q['prompt'])
    if not m:
        continue
    lo, hi, P, unit = m.group(1), m.group(2), int(m.group(3)), m.group(4)
    t0, t1 = 2, 2 + P // 2
    q['prompt'] = q['prompt'].replace(m.group(0), f'between {lo} and {hi} feet. It is at its highest point at t = {t0} {unit} and at its next lowest point at t = {t1} {unit}. What is the period of the model?')
    steps = [f'From a highest point to the next lowest point is half of a cycle: {t1} - {t0} = {P // 2} {unit}.',
             f'A full cycle is twice as long: 2 · {P // 2} = {P} {unit}.']
    sm = re.search(r"(\w+)'s answer: (\d+) " + unit, q['prompt'])
    if sm:  # find-the-mistake: student used the half cycle as the period
        q['prompt'] = q['prompt'].replace(sm.group(0), f"{sm.group(1)}'s answer: {P // 2} {unit}")
        q['solutionSteps'] = ['Mistake: Used the time from a high point to the next low point, which is only half a cycle.'] + steps + [
            f'The correct answer is {P} {unit}, not {P // 2} {unit}.']
    else:
        q['solutionSteps'] = steps
    n9 += 1
q = I['a2-el-s08-cp1-013']
if 'one-eighth' not in q['prompt']:
    q['prompt'] = 'A substance has a half-life of 8 years. How long until one-eighth of it remains?'
    q['answer'] = '24 years'
    q['solutionSteps'] = ['After t years the fraction remaining is (1/2)^(t/8).', 'One-eighth is (1/2)³, so (1/2)^(t/8) = (1/2)³.',
                          'The exponents are equal: t/8 = 3.', 't = 24, so one-eighth remains after 24 years (three half-lives).']
    n9 += 1
q = I['a2-tf-s01-honors-005']
if '901' not in q['prompt']:
    q['prompt'] = 'Find the angle between 0° and 360° that is coterminal with 901°.'
    q['solutionSteps'] = ['Coterminal angles differ by a multiple of 360°.', '901° - 360° = 541°, which is still more than 360°.',
                          '541° - 360° = 181°.', '181° is between 0° and 360°, so the answer is 181°.']
    n9 += 1
for qid, wrong, expr, good in [('a2-pf-s02-honors-016', '(x + 2)(x² + 2x + 4)', 'x³ + 8', '(x + 2)(x² - 2x + 4)'),
                               ('a2-qc-s03-honors-015', '(x - 5)(x² - 5x + 25)', 'x³ - 125', '(x - 5)(x² + 5x + 25)')]:
    q = I[qid]
    old = re.search(r"(\w+)'s answer: (.*)\n", q['prompt'])
    if old.group(2).strip() == expr:
        q['prompt'] = q['prompt'].replace(old.group(0), f"{old.group(1)}'s answer: {wrong}\n")
        q['solutionSteps'] = ['Mistake: The middle term of the trinomial factor has the wrong sign.',
                              'Use a³ + b³ = (a + b)(a² - ab + b²) and a³ - b³ = (a - b)(a² + ab + b²): the middle sign is the opposite of the sign in the binomial.',
                              f'{expr} = {good}.', f'Check by multiplying: the x² and x terms cancel and only {expr} is left.',
                              f'The correct answer is {good}, not {wrong}.']
        n9 += 1
log.append(f'#9 giveaways rewritten: {n9}')

# ---- #17 rounding instructions and year conventions
ROUND = {
    'a2-el-s06-honors-002': ' Give the exact answer and a decimal to the nearest thousandth.',
    'a2-el-s06-honors-003': ' Give the exact answer and a decimal to the nearest thousandth.',
    'a2-el-s06-honors-004': ' Give the exact answer and a decimal to the nearest thousandth.',
    'a2-el-s07-cp1-002': ' Give the exact answer and a decimal to the nearest thousandth.',
    'a2-el-s08-cp1-012': ' Round to the nearest tenth of a year.',
    'a2-ls-s03-honors-005': ' Round to the nearest tenth of a minute.',
    'a2-ps-s05-cp1-019': ' Give a fraction and a decimal to four decimal places.',
    'a2-ps-s05-cp1-020': ' Give a fraction and a decimal to four decimal places.',
    'a2-ps-s05-cp1-021': ' Give a fraction and a decimal to four decimal places.',
    'a2-ps-s05-honors-005': ' Give a fraction and a decimal to four decimal places.',
    'a2-ps-s06-honors-001': ' Give the exact value as a decimal.',
    'a2-ps-s06-honors-002': ' Give the exact value and the amount to the nearest cent.',
    'a2-ps-s06-honors-005': ' Give the exact value and a decimal to the nearest hundredth.',
    'a2-ss-s08-cp1-005': ' Round to the nearest hundredth of a milligram.',
    'a2-ss-s08-honors-003': ' Round to the nearest hundredth of a milligram.',
}
for i in range(1, 9):
    ROUND[f'a2-el-s08-cp1-00{i}'] = ' Round to the nearest cent.'
n17 = 0
for qid, add in ROUND.items():
    q = I[qid]
    if add.strip() in q['prompt']:
        continue
    p = q['prompt']
    m = re.search(r"\n\w+'s answer:", p)
    if m:
        q['prompt'] = p[:m.start()] + add + p[m.start():]
    else:
        q['prompt'] = p.rstrip() + add
    n17 += 1
for qid in ('a2-tf-s09-cp1-003', 'a2-tf-s09-cp1-004', 'a2-tf-s09-cp1-005'):
    q = I[qid]
    w = re.sub(r'(-?\d+)\.00\b', r'\1', q['answer'])
    if w != q['answer']:
        q['answer'] = w; n17 += 1
        q['solutionSteps'] = [re.sub(r'(-?\d+)\.00\b', r'\1', s) for s in q['solutionSteps']]
q = I['a2-el-s08-honors-004']
if q['parts'][3]['answer'] == '2036':
    q['parts'][3]['answer'] = '2035'
    q['answer'] = q['answer'].replace('(d) 2036', '(d) 2035')
    q['parts'][3]['prompt'] = 'In what year will it reach 30,000? (t = 0 is the start of 2015.)'
    q['solutionSteps'][3] = '12000(1.25)^(t/5) = 30000 → (1.25)^(t/5) = 2.5 → t = 5·log 2.5/log 1.25 ≈ 20.5, which is partway through 2035.'
    n17 += 1
log.append(f'#17 rounding/convention fixes: {n17}')

# ---- #18 select-all answer counts: some items with exactly one correct choice, some with every choice correct
# One-correct select-all items were tried and dropped: the bank schema (question-bank-adapter.js) requires
# at least two correct choices for select-all, so only every-choice-correct items are added.
ONE = []
_UNUSED = ['a2-el-s07-cp1-011', 'a2-ls-s06-honors-006', 'a2-pf-s01-cp1-012', 'a2-pf-s01-cp1-013', 'a2-pf-s01-cp1-015',
       'a2-pf-s02-cp1-021', 'a2-pf-s02-cp1-023', 'a2-qc-s04-cp1-013', 'a2-qc-s07-cp1-009', 'a2-qc-s07-cp1-010',
       'a2-qc-s07-honors-009', 'a2-rf-s04-honors-005', 'a2-rf-s05-cp1-008', 'a2-rf-s05-cp1-010', 'a2-rf-s05-cp1-011',
       'a2-tf-s07-cp1-009', 'a2-tf-s04-cp1-007', 'a2-tf-s04-cp1-011', 'a2-tf-s04-cp1-015', 'a2-tf-s07-cp1-016',
       'a2-tf-s07-honors-009', 'a2-tf-s08-cp1-018']
n18 = 0
for qid in ONE:
    q = I[qid]
    corr = [o for o in q['options'] if o['correct']]
    if len(corr) != 2:
        continue
    steps = ' '.join(q['solutionSteps'])
    drop = [o for o in corr if o['text'] not in steps][0]
    keep = [o for o in corr if o is not drop][0]
    q['options'] = [o for o in q['options'] if o is not drop]
    q['answer'] = [a for a in q['answer'] if a != drop['text']]
    q['solutionSteps'] = [s for s in q['solutionSteps'] if 'commutative' not in s and not s.startswith('Both ')]
    q['solutionSteps'].append(f'Of the choices, only {keep["text"]} is correct; select just that one.')
    n18 += 1
ALL = ['a2-cs-s01-honors-001', 'a2-cs-s04-cp1-015', 'a2-cs-s05-cp1-013', 'a2-cs-s03-cp1-019', 'a2-cs-s07-honors-008', 'a2-el-s05-honors-001', 'a2-el-s02-cp1-020', 'a2-ft-s07-honors-005', 'a2-ls-s06-cp1-010', 'a2-pf-s06-cp1-016', 'a2-ps-s05-cp1-008', 'a2-ps-s05-cp1-016', 'a2-qc-s05-cp1-009', 'a2-rr-s05-cp1-020', 'a2-rf-s07-cp1-012', 'a2-ss-s01-honors-004', 'a2-ss-s05-cp1-011', 'a2-tf-s03-honors-004', 'a2-tf-s05-cp1-020', 'a2-tf-s06-cp1-013']
for q in [I[x] for x in ALL]:
    if len(q['options']) != 6:
        continue
    q['options'] = [o for o in q['options'] if o['correct']]
    q['solutionSteps'].append('Every choice is correct, so select all four.')
    n18 += 1
log.append(f'#18 select-all items now with one correct choice or all correct: {n18}')

# ---- #15 generic open-response stems → name the skill
names = json.load(open(os.path.join(os.path.dirname(__file__), 'skill-names.json')))
n15 = 0
for _, q in items(B):
    if q['format'] == 'open-response' and q['prompt'].strip() == 'Answer each part. Show your work.':
        nm = names[q['skillId']]
        q['prompt'] = f'Practice set ({nm}): answer each part and show your work.'
        n15 += 1
log.append(f'#15 open-response stems named: {n15}')

save(B)
print('\n'.join(log))
