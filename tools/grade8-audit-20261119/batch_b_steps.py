"""8th Grade Math audit #10 (2026-11-19): item-specific solution steps.

1. The ten families whose steps were only boilerplate get a step computed from the item itself.
2. Every select-all item gets a step that names the correct and the incorrect choices.
3. Every other item with a single step, or whose steps never reach the answer, gets a closing step with the answer.
Idempotent: a second run changes nothing. Run from the repository root."""
import math, os, re, sys
from fractions import Fraction as Fr

sys.path.insert(0, os.path.dirname(__file__))
from lib import load, save, items, family
from batch_a import map_text

MARK = 'Correct choices: '


def nums(s):
    return [Fr(x) for x in re.findall(r'-?\d+(?:\.\d+)?', s)]


def fmt(f):
    f = Fr(f)
    return str(f.numerator) if f.denominator == 1 else f'{f.numerator}/{f.denominator}'


def rigid(t):
    m = re.search(r'dilation with scale factor (\S+)', t)
    if m:
        k = Fr(m.group(1))
        return k == 1, f'a dilation with scale factor {m.group(1)} {"keeps" if k == 1 else "changes"} lengths'
    kind = re.match(r'(?:a |an )?(\w+)', t).group(1)
    return True, f'a {kind} is a rigid motion'


def step_cong(q):
    p = q['prompt']
    m = re.search(r'undergoes (.+?)(?:\. Is|\? )', p)
    parts = re.split(r', then ', m.group(1))
    res = [rigid(x) for x in parts]
    said = '; '.join(r[1] for r in res)
    allr = all(r[0] for r in res)
    ks = [Fr(k) for k in re.findall(r'dilation with scale factor (\S+) centered at the origin', p)]
    if len(ks) == 2 and len(parts) == 2:
        prod = ks[0] * ks[1]
        allr = prod == 1
        said = f'the two dilations have the same center, so together they multiply lengths by ({fmt(ks[0])})({fmt(ks[1])}) = {fmt(prod)}'
        if allr:
            said += ', which keeps every length'
        else:
            said += ', which changes lengths' 
    if family(q) == 's1_congruent':
        return f'Here {said}, so the image {"is" if allr else "is not"} always congruent: {q["answer"]}.'
    return f'Here {said}, so the final image is {"congruent" if allr else "similar but not congruent"}.'


POS = {1: ('m', 'above', 'left'), 2: ('m', 'above', 'right'), 3: ('m', 'below', 'left'), 4: ('m', 'below', 'right'),
       5: ('n', 'above', 'left'), 6: ('n', 'above', 'right'), 7: ('n', 'below', 'left'), 8: ('n', 'below', 'right')}


def step_angles(q):
    a, b = [int(x) for x in re.findall(r'∠(\d)', q['prompt'])[:2]]
    d = lambda k: f'∠{k} is {POS[k][1]} line {POS[k][0]}, {POS[k][2]} of t'
    return f'{d(a)}; {d(b)}. So they are {q["answer"]}.'


def step_function(q):
    out = []
    for o in q['options']:
        pairs = re.findall(r'\((-?\d+), (-?\d+)\)', o['text'])
        seen, bad = {}, None
        for x, y in pairs:
            if x in seen and seen[x] != y:
                bad = (x, seen[x], y)
                break
            seen[x] = y
        out.append(f'{o["text"]}: input {bad[0]} has outputs {bad[1]} and {bad[2]}, so not a function' if bad else f'{o["text"]}: no input repeats, so it is a function')
    return '; '.join(out) + '.'


def step_table(q):
    m = re.search(r'x: ([-\d, ]+); y: ([-\d, ]+)', q['prompt'])
    xs, ys = [int(v) for v in m.group(1).split(',')], [int(v) for v in m.group(2).split(',')]
    pts = sorted(zip(xs, ys))
    rates = [Fr(pts[i + 1][1] - pts[i][1], pts[i + 1][0] - pts[i][0]) for i in range(len(pts) - 1)]
    same = len(set(rates)) == 1
    return f'In order of x, the rates of change are {", ".join(fmt(r) for r in rates)}: {"constant, so linear" if same else "not constant, so nonlinear"}.'


def reason_eq(t):
    if '²' in t or '³' in t:
        return 'x is raised to a power'
    if re.search(r'/x|/\(x', t):
        return 'x is in a denominator'
    if 'ˣ' in t:
        return 'x is an exponent'
    if '√' in t:
        return 'x is under a root'
    if re.search(r'xy|x · y', t):
        return 'x and y are multiplied'
    return 'it can be written y = mx + b'


def step_equation(q):
    return '; '.join(f'{o["text"]}: {reason_eq(o["text"])}' for o in q['options']) + '.'


def step_story(q):
    alt = q['diagram']['spec']['alt']
    m = re.search(re.escape(q['answer']) + r': segments through ([^;]+)', alt)
    pts = re.findall(r'\((-?\d+), (-?\d+)\)', m.group(1))
    words = []
    for (x0, y0), (x1, y1) in zip(pts, pts[1:]):
        dy = int(y1) - int(y0)
        words.append('away from home' if dy > 0 else 'toward home' if dy < 0 else 'stopped')
    return f'{q["answer"]} goes ' + ', then '.join(words) + ', which matches the story.'


def is_square(n):
    r = math.isqrt(n)
    return r * r == n


def step_classify(q):
    e = re.search(r'Is (.+?) rational or irrational', q['prompt']).group(1)
    roots = re.findall(r'√\(?(\d+)(?:/(\d+))?\)?', e)
    if 'π' in e:
        return f'{e} contains π, which is irrational, so {e} is irrational.'
    cube = re.search(r'∛\(?(-?\d+)\)?', e)
    if cube:
        n = int(cube.group(1)); r = round(abs(n) ** (1 / 3))
        ok = r ** 3 == abs(n)
        return f'{abs(n)} {"is" if ok else "is not"} a perfect cube' + (f', so {e} = {"-" if n < 0 else ""}{r}' if ok else '') + f'. So {e} is {q["answer"]}.'
    if roots:
        bits = []
        for a, b in roots:
            sq = is_square(int(a)) and (not b or is_square(int(b)))
            frac = f'{a}/{b}' if b else a
            bits.append(f'{frac} {"is" if sq else "is not"} a perfect square' + (f', so √{"(" + frac + ")" if b else frac} = {fmt(Fr(math.isqrt(int(a)), math.isqrt(int(b)) if b else 1))}' if sq else ''))
        return '; '.join(bits) + f'. So {e} is {q["answer"]}.'
    return f'{e} can{"" if q["answer"] == "rational" else "not"} be written as a ratio of integers, so it is {q["answer"]}.'


def coeffs(side):
    """a, b, c for a·x + b·y + c written on one side."""
    a = b = c = Fr(0)
    for t in re.findall(r'[+-]?[^+-]+', side.replace(' ', '')):
        v = t[:-1] if t[-1] in 'xy' else t
        k = Fr(1 if v in ('', '+') else -1 if v == '-' else v)
        if t.endswith('x'):
            a += k
        elif t.endswith('y'):
            b += k
        else:
            c += k
    return a, b, c


def line(s):
    l, r = s.split('=')
    a1, b1, c1 = coeffs(l)
    a2, b2, c2 = coeffs(r)
    a, b, c = a1 - a2, b1 - b2, c1 - c2          # a·x + b·y + c = 0
    return -a / b, -c / b


def step_sys(q):
    a, b = re.search(r'does (.+?=.+?) and (.+?=.+?) have', q['prompt']).groups()
    (m1, b1), (m2, b2) = line(a), line(b)
    return f'Slopes {fmt(m1)} and {fmt(m2)}; y-intercepts {fmt(b1)} and {fmt(b2)}. So: {q["answer"]}.'


def step_interpret(q):
    m = re.search(r'y = (-?\d+)x \+ (\d+) models (.+?) \(y\) from (.+?) \(x\)', q['prompt'])
    k, b, yv, xv = m.groups()
    if 'slope' in q['prompt'].split('What does')[-1]:
        return f'Here the slope is {k}: the predicted {yv} changes by {k} for each 1 more {xv}.'
    return f'Here the y-intercept is {b}: the predicted {yv} when {xv} is 0.'


HANDLERS = {'s1_congruent': step_cong, 's6_cong_or_sim': step_cong, 's9_relationship': step_angles, 's1_which_function': step_function,
            's3_table': step_table, 's3_equation': step_equation, 's10_match_story': step_story, 's4_classify': step_classify,
            's5_classify_sa': step_sys, 's4_interpret': step_interpret}


KEYFIX = {   # dilations by 2 and 1/2 about the same center undo each other: the image is congruent
    'pa8-cgs-s06-cp2-014': 'congruent', 'pa8-cgs-s06-cp1-017': 'congruent'}
GENERIC = {'A sequence of rigid motions gives a congruent image.', 'Including a dilation (scale factor ≠ 1) gives a similar, not congruent, image.'}


def run():
    banks = load()
    for _, q in items(banks):
        if q['id'] in KEYFIX and q['answer'] != KEYFIX[q['id']]:
            q['answer'] = KEYFIX[q['id']]
            q['solutionSteps'] = [s for s in q['solutionSteps'] if s in GENERIC]
        map_text(q, lambda t: re.sub(r'\b(in|ft|yd|oz|lb|mi)\.\.', r'\1.', t))   # "15 in.." at the end of a sentence
    n = {'family': 0, 'select': 0, 'closing': 0}
    for _, q in items(banks):
        if q['format'] == 'open-response':
            continue
        st = q['solutionSteps']
        h = HANDLERS.get(family(q))
        if h and (q['skillId'].startswith(('congruence', 'linear-functional', 'real-numbers', 'systems', 'patterns'))):
            if family(q) == 's3_table' and not q['skillId'].startswith('linear-functional'):
                pass
            else:
                s = h(q)
                if s not in st:
                    st.append(s); n['family'] += 1
        if q['format'] == 'select-all':
            if not any(x.startswith(MARK) for x in st):
                good = [o['text'].rstrip('.') for o in q['options'] if o['correct']]
                bad = [o['text'].rstrip('.') for o in q['options'] if not o['correct']]
                st.append(MARK + '; '.join(good) + '. Not correct: ' + '; '.join(bad) + '.')
                n['select'] += 1
            continue
        a = str(q['answer'])
        if len(st) < 2 or a not in st[-1]:
            if not any(a in x for x in st[-1:]):
                st.append(f'So the answer is {a}.' if not a.endswith('.') else f'So the answer is: {a}')
                n['closing'] += 1
    save(banks)
    return n


if __name__ == '__main__':
    print(run())
