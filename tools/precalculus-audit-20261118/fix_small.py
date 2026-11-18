"""Precalculus audit (2026-11-18), batch P6: notation, exact forms, rounding, option order, grammar and list formats.

#14 ambiguous inline fractions: sin(1/2x) → sin((1/2)x), f(1/2(x + 4)) → f((1/2)(x + 4)), ±9/16x → ±(9/16)x, 3/2π → (3/2)π
#15 nested radicals for 15° and 75° → the textbook forms (√6 ± √2)/4
#16 long unrounded decimal keys → "Round to the nearest hundredth." with rounded keys and options
#17 multiple-choice option order: the correct choice is put in a balanced, seeded position
#18 "1 rows / 1 columns / 1 successes / 1 inches / 1 weeks" → singular
#19 solution lists "x = a, b, c" → "x = a or x = b or x = c", the format used everywhere else in the bank
Idempotent: rerunning changes nothing.

Usage: python3 tools/precalculus-audit-20261118/fix_small.py
"""
import hashlib, re
from decimal import Decimal, ROUND_HALF_UP
from lib import load, save, items

B = load()
log = []


def fields(q):
    """(getter, setter) for every text field of an item."""
    out = [(lambda q=q: q['prompt'], lambda v, q=q: q.__setitem__('prompt', v))]
    if isinstance(q.get('answer'), str):
        out.append((lambda q=q: q['answer'], lambda v, q=q: q.__setitem__('answer', v)))
    elif isinstance(q.get('answer'), list):
        for i in range(len(q['answer'])):
            out.append((lambda q=q, i=i: q['answer'][i], lambda v, q=q, i=i: q['answer'].__setitem__(i, v)))
    for i in range(len(q.get('solutionSteps', []))):
        out.append((lambda q=q, i=i: q['solutionSteps'][i], lambda v, q=q, i=i: q['solutionSteps'].__setitem__(i, v)))
    for o in q.get('options', []):
        out.append((lambda o=o: o['text'], lambda v, o=o: o.__setitem__('text', v)))
    for p in q.get('parts', []):
        out.append((lambda p=p: p['prompt'], lambda v, p=p: p.__setitem__('prompt', v)))
        out.append((lambda p=p: p['answer'], lambda v, p=p: p.__setitem__('answer', v)))
    if q.get('plot', {}).get('answerKey', {}).get('alt'):
        a = q['plot']['answerKey']
        out.append((lambda a=a: a['alt'], lambda v, a=a: a.__setitem__('alt', v)))
    return out


def each_text(fn):
    n = 0
    for _, q in items(B):
        changed = False
        for get, put in fields(q):
            v = get()
            w = fn(v)
            if w != v:
                put(w)
                changed = True
        n += changed
    return n


# ---- #14 a fraction written right before a variable, i, π, √, a function name or "(" reads two ways
FRAC = re.compile(r'(?<![\w)\]/])(\d+/\d+)(?=\s?[√∛]|i\b|[a-zπθ](?![a-z])|\(|sin|cos|tan|sec|csc|cot|log|ln)')
log.append(f'#14 fractions parenthesized in {each_text(lambda s: FRAC.sub(lambda m: "(" + m.group(1) + ")", s))} items')

# ---- #15 nested radicals → textbook exact values
NEST = {'(√(√3 + 2))/2': '(√6 + √2)/4', '(-√(√3 + 2))/2': '-(√6 + √2)/4', '(√(2 + √3))/2': '(√6 + √2)/4',
        '(√(2 - √3))/2': '(√6 - √2)/4', '(-√(2 - √3))/2': '(√2 - √6)/4'}


def denest(s):
    for a, b in NEST.items():
        s = s.replace(a, b)
    return s


log.append(f'#15 nested radicals rewritten in {each_text(denest)} items')

# ---- #16 rounding instructions
ROUNDED = re.compile(r'nearest|round|decimal|tenth|hundredth|thousandth|approximat|≈|calculator|estimate|exact', re.I)
NUM = re.compile(r'^-?\d+\.\d{3,}$')


def r2(t):
    return '≈ ' + str(Decimal(t).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP))


def add_to_prompt(q, add):
    p = q['prompt']
    m = re.search(r"\n\w+'s answer:", p)
    q['prompt'] = (p[:m.start()] + add + p[m.start():]) if m else p.rstrip() + add


n16 = 0
for _, q in items(B):
    if q['format'] not in ('short-answer', 'multiple-choice') or not isinstance(q['answer'], str) or ROUNDED.search(q['prompt']):
        continue
    if NUM.match(q['answer']):
        opts = [o['text'] for o in q.get('options', [])]
        if opts and (not all(re.match(r'^-?\d+(\.\d+)?$', t) for t in opts) or len({r2(t) for t in opts}) < len(opts)):
            continue
        add_to_prompt(q, ' Round to the nearest hundredth.')
        old = q['answer']
        q['answer'] = r2(old)
        for o in q.get('options', []):
            o['text'] = r2(o['text'])
        q['solutionSteps'].append(f'{old} ≈ {q["answer"][2:]} to the nearest hundredth.')
        n16 += 1
    elif re.search(r'mean = -?\d+\.\d{3,}', q['answer']):
        add_to_prompt(q, ' Give exact values.')
        n16 += 1
log.append(f'#16 rounding instructions added to {n16} items')

# ---- #18 singular nouns after 1
SING = {'rows': 'row', 'columns': 'column', 'successes': 'success', 'inches': 'inch', 'weeks': 'week'}
G = re.compile(r'(?<![\d.\-/−])\b1 (rows|columns|successes|inches|weeks)\b')
log.append(f'#18 plurals fixed in {each_text(lambda s: G.sub(lambda m: "1 " + SING[m.group(1)], s))} items')

# ---- #19 "x = a, b, c" → "x = a or x = b or x = c"
LIST = re.compile(r'^x = ([^,;]+(?:, [^,;]+)+)$')


def or_list(s):
    m = LIST.match(s.strip())
    if not m:
        return s
    return ' or '.join('x = ' + p.strip() for p in m.group(1).split(','))


n19 = 0
for _, q in items(B):
    if q['skillId'] != 'trigonometric-functions-skill-14':
        continue
    before = q['answer']
    q['answer'] = or_list(q['answer'])
    for o in q.get('options', []):
        o['text'] = or_list(o['text'])
    q['prompt'] = re.sub(r"(\n\w+'s answer: )(x = [^\n]+)", lambda m: m.group(1) + or_list(m.group(2)), q['prompt'])
    q['solutionSteps'] = [re.sub(r'x = [^,;.]+(?:, [^,;.]+)+(?=\.?$)', lambda m: or_list(m.group(0)), s) for s in q['solutionSteps']]
    for p in q.get('parts', []):
        p['answer'] = or_list(p['answer'])
    if q['format'] == 'open-response':
        q['answer'] = '; '.join(f'({"abcd"[i]}) {p["answer"].rstrip(".")}' for i, p in enumerate(q['parts']))
    n19 += q['answer'] != before
log.append(f'#19 solution lists rewritten with "or" in {n19} items')

# ---- #17 balanced option order: put the correct choice at a seeded position, keep the others in order
n17 = 0
for _, q in items(B):
    if q['format'] != 'multiple-choice':
        continue
    opts = q['options']
    want = int(hashlib.sha256(q['id'].encode()).hexdigest(), 16) % len(opts)
    cur = [o['correct'] for o in opts].index(True)
    if cur == want:
        continue
    right = opts[cur]
    rest = [o for o in opts if o is not right]
    q['options'] = rest[:want] + [right] + rest[want:]
    n17 += 1
log.append(f'#17 option order changed in {n17} multiple-choice items')

save(B)
print('\n'.join(log))
