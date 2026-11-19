"""Grade 6 audit batch 6B: recompute every -gNN key from the prompt and the figure's alt text, independently of new_items.py.
Constructed-response tasks are recomputed from a separate table of formulas. Exit 1 on any mismatch."""
import json, os, re, sys
from fractions import Fraction as Fr
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
BANKS = os.path.join(ROOT, 'question-banks', 'math6')


def F(s):
    s = s.strip().replace('$', '').replace(',', '')
    m = re.fullmatch(r'(-?\d+) (\d+)/(\d+)', s)
    if m:
        return int(m[1]) + Fr(int(m[2]), int(m[3]))
    return Fr(s)


def nums(s):
    return [int(x) for x in re.findall(r'-?\d+', s)]


CR = {  # independent arithmetic for the four parts of each constructed-response task
    'smoothie': lambda: [Fr('4.80') / 16, Fr('6.48') / 24, None, 48 * Fr('6.48') / 24],
    'Store A sells': lambda: [Fr('6.25') / 5, Fr('9.60') / 8, 40 * (Fr('6.25') / 5 - Fr('9.60') / 8), int(50 / (Fr('9.60') / 8))],
    'carpenter': lambda: [None, int(F('8 1/4') / F('1 3/4')), F('8 1/4') - 4 * F('1 3/4'), (F('8 1/4') - 4 * F('1 3/4')) / F('1 3/4')],
    'oats': lambda: [int(F('5 1/2') / Fr(2, 3)), F('5 1/2') - 8 * Fr(2, 3), Fr(2, 3) - (F('5 1/2') - 8 * Fr(2, 3)), 12 * 8],
    'town map': lambda: [abs(5 - -4), abs(3 - -6), 9 + 9, None],
    'A rectangle has vertices': lambda: [3 - -6, 5 - -2, 2 * (9 + 7), None],
    'dog walker': lambda: [None, None, 8 * 6 + 5, Fr(93 - 5, 8)],
    'candle': lambda: [None, 24 - Fr('1.5') * 6, (24 - 9) / Fr('1.5'), 24 / Fr('1.5')],
    'van': lambda: [None, None, (1200 - 180) // 60, None],
    'Ana has': lambda: [None, Fr(200 - 45, 12), -(-(200 - 45) // 12), 45 + 12 * 13],
    'gift box': lambda: [10 * 6, 10 * 4, 2 * (60 + 40 + 24), 300 - 248],
    'planter': lambda: [F('3 1/2') * 2 * F('1 1/2'), F('3 1/2') * 2, 2 * F('3 1/2') * F('1 1/2') + 2 * 2 * F('1 1/2'), None],
    'ages of 8': lambda: [Fr(sum([12, 13, 13, 14, 14, 15, 16, 41]), 8), Fr(14 + 14, 2), 41, None],
    'Two classes took': lambda: [Fr(sum([6, 7, 7, 8, 8, 9, 10]), 7), sorted([4, 6, 8, 8, 9, 11, 10])[3], 11 - 4, (11 - 4) - (10 - 6)],
}


def num_of(a):
    a = re.sub(r'^(Class B, by|h ≥|b ≤)\s*', '', a.strip())
    a = re.sub(r'\s*(units|square units)$', '', a)
    return F(a)


def expect(q):
    p, alt = q['prompt'], ((q.get('diagram') or {}).get('spec') or {}).get('alt', '')
    if m := re.search(r'^(\d+) is (\d+)% of what number', p):
        return Fr(int(m[1]) * 100, int(m[2]))
    if '%' in p and q['id'].startswith('m6-rrp-s06'):
        pc, part = (int(x) for x in re.findall(r'(\d+)%', p)[:1] + [re.findall(r'\$?(\d+) (?:tickets|of the|gallons|left|games)|\$(\d+)\.', p)[0][0] or re.findall(r'\$(\d+)\.', p)[0]])
        left = bool(re.search(r'left|spending|off', p))
        return Fr(part * 100, 100 - pc if left else pc)
    if alt.startswith('Tape diagram'):
        (la, a), (lb, b) = re.findall(r'(\w+): (\d+) equal', alt)
        a, b, tot = int(a), int(b), int(re.search(r'total of (\d+)', alt)[1])
        u = Fr(tot, a + b)
        if 'How many more' in p:
            return abs(a - b) * u
        if 'new ratio' in p:
            add = int(re.search(r'Then (\d+) more', p)[1])
            r = Fr(a * u, b * u + add)
            return f'{r.numerator}:{r.denominator}'
        return a * u
    if alt.startswith('Double number line'):
        top, bot = [x.split(', ') for x in re.findall(r': ([^.]*)\.', alt)[:2]]
        rate = Fr(int(bot[1]), int(top[1]))
        if '?' in bot:
            return int(top[bot.index('?')]) * rate
        if m := re.search(r'go with (\d+)', p):
            return int(m[1]) * rate
        m = re.search(r'give ([\d /]+) ', p)
        return F(m[1]) / rate
    if alt.startswith('Fraction model'):
        d, s = int(re.search(r'into (\d+)', alt)[1]), int(re.search(r'(\d+) parts are shaded', alt)[1])
        g = int(re.search(r'groups of (\d+) parts', alt)[1])
        m = re.search(r'find (.+) ÷ (.+)\.$', p)
        assert F(m[1]) == Fr(s, d) and F(m[2]) == Fr(g, d), q['id'] + ' model and prompt disagree'
        return Fr(s, g)
    if alt.startswith('Dot plot'):
        return len(alt.split('Values:')[1].split(','))
    if alt.startswith('Net of'):
        l, w, h = nums(alt)
        S = 2 * (l * w + l * h + w * h)
        return S - l * w if 'no top' in p else S
    if alt.startswith('Coordinate grid'):
        pts = [tuple(map(int, t)) for t in re.findall(r'\((-?\d+), (-?\d+)\)', alt)]
        n = len(pts)
        area = abs(sum(pts[i][0] * pts[(i + 1) % n][1] - pts[(i + 1) % n][0] * pts[i][1] for i in range(n))) / Fr(2)
        if 'perimeter' in p:
            return sum(abs(pts[i][0] - pts[(i + 1) % n][0]) + abs(pts[i][1] - pts[(i + 1) % n][1]) for i in range(n))
        if 'area' in p:
            return area
        a, b = pts[0], pts[1]
        return abs(a[0] - b[0]) + abs(a[1] - b[1])
    if alt.startswith('Graph of a straight line'):
        (x0, y0), (x1, y1) = [tuple(map(int, t)) for t in re.findall(r'\((\d+), (\d+)\)', alt)[:2]] if '(0, ' in alt else [(0, 0)] + [tuple(map(int, t)) for t in re.findall(r'\((\d+), (\d+)\)', alt)[:1]]
        k = Fr(y1 - y0, x1 - x0)
        if m := re.search(r'for (\d+) ', p):
            return y0 + k * int(m[1])
        if 'Plan B' in p:
            k2 = int(re.search(r'= (\d+)[a-z]\.', p)[1])
            return next(x for x in range(1, 100) if k2 * x > y0 + k * x)
        if 'equation' in p:
            v = re.search(r'Write an equation for (\w) in terms of (\w)', p)
            return f'{v[1]} = {k}{v[2]}' if y0 == 0 else f'{v[1]} = {k}{v[2]} + {y0}'
        return None
    return None


def main():
    n = bad = 0
    for f in sorted(os.listdir(BANKS)):
        if not f.endswith('.json'):
            continue
        for q in json.load(open(os.path.join(BANKS, f), encoding='utf-8'))['questions']:
            if not re.search(r'-g\d{2}$', q['id']):
                continue
            if q.get('parts'):
                key = next(k for k in CR if k in q['prompt'])
                for part, want in zip(q['parts'], CR[key]()):
                    if want is None:
                        continue
                    n += 1
                    if num_of(part['answer']) != Fr(want):
                        bad += 1; print('MISMATCH', q['id'], part['prompt'], part['answer'], want)
                if q['answer'] != '; '.join(f'({"abcd"[i]}) {x["answer"]}' for i, x in enumerate(q['parts'])):
                    bad += 1; print('ANSWER/PARTS DISAGREE', q['id'])
                continue
            want = expect(q)
            if want is None:
                if q['format'] == 'multiple-choice' or re.search(r'expression|terms|which part|coefficient', q['prompt']):
                    continue  # conceptual and expression items are checked by verify_keys.py (word6 templates) and review
                bad += 1; print('NO CHECK', q['id'], q['prompt'][:80]); continue
            n += 1
            got = q['answer'] if isinstance(want, str) else num_of(q['answer'])
            if got != (want if isinstance(want, str) else Fr(want)):
                bad += 1; print('MISMATCH', q['id'], q['prompt'][:80], q['answer'], want)
    print(f"{'PASS' if not bad else 'FAIL'} Grade 6 6B new items: {n} keys recomputed, {bad} problems")
    sys.exit(1 if bad or n < 70 else 0)


if __name__ == '__main__':
    main()
