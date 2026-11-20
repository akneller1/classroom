"""Recompute every key in content-updates/2026-11-20/grade5-levels.json from its printed prompt, independently of
build.py (whole-site audit 2 #3, Grade 5). Each rewrite must match exactly one rule; multiple-choice items must key the
option that equals the answer and no other. Usage: python3 tools/site-audit-20261120/grade5_levels/verify.py"""
import json, math, os, re, sys
from fractions import Fraction as F

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..'))
FILE = os.path.join(ROOT, 'content-updates', '2026-11-20', 'grade5-levels.json')


def n(s):
    s = s.replace(',', '').replace('$', '').strip()
    if ' ' in s:
        w, f = s.split(' ')
        return F(w) + F(f)
    return F(s)


I = r'(\d[\d,]*)'
D = r'(\d[\d,]*(?:\.\d+)?)'
M = r'(\d+(?: \d+/\d+)?(?:/\d+)?)'   # whole, fraction or mixed number
cents = lambda x: F(math.floor(x * 100 + F(1, 2)), 100)

RULES = [
    (r'^A triangle has angles of (\d+)° and (\d+)°\. Find the third angle, then classify', lambda g: (lambda c: ('w', 'right' if 90 in (int(g[0]), int(g[1]), c) else 'obtuse' if max(int(g[0]), int(g[1]), c) > 90 else 'acute'))(180 - int(g[0]) - int(g[1]))),
    (r'^A rectangle is (\d+) inches long\. Its width is (\d+) inches shorter than its length\. What is its perimeter', lambda g: 2 * (int(g[0]) + int(g[0]) - int(g[1]))),
    (r'^A square has sides of (\d+) cm\. A rectangle that is not a square has the same perimeter and is (\d+) cm long', lambda g: 2 * int(g[0]) - int(g[1])),
    (r'^Start at the origin\. Move (\d+) units right and (\d+) units up\. Then move (\d+) units? left and (\d+) units? up\.', lambda g: ('w', f'({int(g[0]) - int(g[2])}, {int(g[1]) + int(g[3])})')),
    (r'^A path goes from A\((\d+), (\d+)\) to B\((\d+), \d+\) and then to C\(\d+, (\d+)\)', lambda g: int(g[2]) - int(g[0]) + int(g[3]) - int(g[1])),
    (r'The points \((\d+), (\d+)\) and \((\d+), (\d+)\) are on the graph\. How many centimeters did the plant grow', lambda g: int(g[3]) - int(g[1])),
    (r'^The points \(0, (\d+)\), \(1, (\d+)\), .* what is y when x = (\d+)\?$', lambda g: int(g[0]) + (int(g[1]) - int(g[0])) * int(g[2])),
    (r'^Data: (.+)\. On a line plot, how many X marks are to the right of ' + M + r'\?$', lambda g: sum(1 for v in g[0].split(', ') if n(v) > n(g[1]))),
    (r'^Data: (.+)\. If the total is shared equally among the (\d+) values', lambda g: sum(n(v) for v in g[0].split(', ')) / int(g[1])),
    (r'sells (\d+) muffins for \$' + D + r' each\. They spent \$' + D + r' on ingredients and \$(\d+) on bags', lambda g: int(g[0]) * n(g[1]) - n(g[2]) - int(g[3])),
    (r'^Add and subtract from left to right: ' + D + r' \+ ' + D + ' − ' + D + '$', lambda g: n(g[0]) + n(g[1]) - n(g[2])),
    (r'buys (\d+) notebooks for \$' + D + r' each and pays with a \$(\d+) bill', lambda g: int(g[2]) - int(g[0]) * n(g[1])),
    (r'buys (\d+) notebooks for \$' + D + r' each and a backpack for \$(\d+)\. What is the total cost', lambda g: int(g[2]) + int(g[0]) * n(g[1])),
    (r'Find ' + D + ' × ' + D + r' \+ ' + D + r'\.$', lambda g: n(g[0]) * n(g[1]) + n(g[2])),
    (r'pays \$' + D + r' for (\d+) equal tickets plus a \$' + D + ' fee', lambda g: (n(g[0]) - n(g[2])) / int(g[1])),
    (r'^A ribbon is ' + D + r' meters long\. How many pieces that are each ' + D + ' meters long', lambda g: n(g[0]) / n(g[1])),
    (r'^Each sticker sheet costs \$' + D + r'\. \w+ buys (\d+) sheets and uses a \$(\d+) coupon', lambda g: int(g[1]) * n(g[0]) - int(g[2])),
    (r'^Find the least common denominator of 1/(\d+) and 1/(\d+), then add the fractions\.$', lambda g: F(1, int(g[0])) + F(1, int(g[1]))),
    (r'^Add: (\d+/\d+) \+ (\d+/\d+) \+ (\d+/\d+)$', lambda g: F(g[0]) + F(g[1]) + F(g[2])),
    (r'^Subtract: ' + M + r' − (\d+/\d+) − (\d+/\d+)$', lambda g: n(g[0]) - F(g[1]) - F(g[2])),
    (r'^Subtract: (\d+ \d+/\d+) − (\d+ \d+/\d+)$', lambda g: n(g[0]) - n(g[1])),
    (r'^Estimate (\d+/\d+) \+ (\d+/\d+)\. Is the sum closest to', lambda g: (lambda s_: min([F(0), F(1, 2), F(1), F(3, 2), F(2)], key=lambda x: (abs(s_ - x), x)))(F(g[0]) + F(g[1]))),
    (r'^In a garden, (\d+/\d+) is tomatoes, (\d+/\d+) is peppers and (\d+/\d+) is beans', lambda g: 1 - F(g[0]) - F(g[1]) - F(g[2])),
    (r'^(\d+) pounds of rice are shared equally among (\d+) families', lambda g: F(int(g[0]), int(g[1]))),
    (r'^Multiply: (\d+/\d+) × (\d+) × (\d+)$', lambda g: F(g[0]) * int(g[1]) * int(g[2])),
    (r'^Multiply: (\d+/\d+) × (\d+/\d+) × (\d+)$', lambda g: F(g[0]) * F(g[1]) * int(g[2])),
    (r'^How many tiles that are (\d+/\d+) foot by (\d+/\d+) foot are needed to cover a rectangle that is (\d+) feet by (\d+) feet', lambda g: int(g[2]) * int(g[3]) / (F(g[0]) * F(g[1]))),
    (r'^Without multiplying, is ' + M + r' × (\d+) greater than, less than, or equal to \d+\? Then find the product\.$',
     lambda g: (lambda f, k: ('w', ('less than' if f < 1 else 'greater than' if f > 1 else 'equal to') + '; ' + mx(f * k)))(n(g[0]), int(g[1]))),
    (r'^Divide, then multiply: (\d+/\d+) ÷ (\d+) × (\d+)$', lambda g: F(g[0]) / int(g[1]) * int(g[2])),
    (r'^(\d+) kids share (\d+/\d+) of a cake equally', lambda g: F(g[1]) / int(g[0])),
    (r'^Convert: (\d+) feet (\d+) inches = \? inches$', lambda g: 12 * int(g[0]) + int(g[1])),
    (r'^A tank holds (\d+) gallons and a jug holds (\d+) quarts', lambda g: 4 * int(g[0]) + int(g[1])),
    (r'^A bottle holds ' + D + r' liters\. \w+ pours out (\d+) milliliters', lambda g: n(g[0]) * 1000 - int(g[1])),
    (r'^A pitcher holds (\d+) liters of water\. \w+ fills (\d+) cups of (\d+) milliliters', lambda g: F(int(g[0]) * 1000, int(g[2])) - int(g[1])),
    (r'^Multiply, then add: (\d+) × (\d+) \+ (\d+)$', lambda g: int(g[0]) * int(g[1]) + int(g[2])),
    (r'^Estimate (\d+) × (\d+) by rounding \d+ to the nearest hundred and \d+ to the nearest ten', lambda g: round(int(g[0]), -2) * round(int(g[1]), -1)),
    (r'^Fill in the blank: ___ ÷ (\d+) = (\d+) R(\d+)$', lambda g: int(g[1]) * int(g[0]) + int(g[2])),
    (r'^Use the basic fact \d+ ÷ \d+ = \d+\. What is ' + I + r' ÷ (\d+)\?$', lambda g: F(n(g[0]), int(g[1]))),
    (r'^A florist has (\d+) roses\. Each bouquet uses (\d+) roses\. After making', lambda g: int(g[0]) % int(g[1])),
    (r'^Evaluate: (\d+) × \((\d+) \+ (\d+)\) − (\d+)$', lambda g: int(g[0]) * (int(g[1]) + int(g[2])) - int(g[3])),
    (r'^Write an expression for "add (\d+) and (\d+), then multiply by (\d+)"', lambda g: int(g[2]) * (int(g[0]) + int(g[1]))),
    (r'^In (\d+) × (\d+), \d+ is replaced by (\d+) and \d+ is replaced by (\d+)\. How many times as large', lambda g: F(int(g[2]) * int(g[3]), int(g[0]) * int(g[1]))),
    (r'^A pattern starts at (\d+)\. The rule is "Add (\d+)\." What is the sum of terms 1 and (\d+)\?$', lambda g: 2 * int(g[0]) + int(g[1]) * (int(g[2]) - 1)),
    (r'^Pattern A: start at 0, add (\d+)\. Pattern B: start at 0, add (\d+)\. For term (\d+), how much greater', lambda g: (int(g[1]) - int(g[0])) * (int(g[2]) - 1)),
    (r'^In a number, a (\d) is in the (thousands|hundreds|tens) place and another \d is in the (ones|tenths|hundredths) place',
     lambda g: F({'thousands': 1000, 'hundreds': 100, 'tens': 10}[g[1]]) / {'ones': 1, 'tenths': F(1, 10), 'hundredths': F(1, 100)}[g[2]]),
    (r'^' + I + ' ÷ ' + I + r' × 10 = \?$', lambda g: n(g[0]) / n(g[1]) * 10),
    (r'^What number is (\d) tens \+ (\d) ones \+ (\d) tenths \+ (\d) hundredths \+ (\d) thousandths\?$', lambda g: 10 * int(g[0]) + int(g[1]) + F(int(g[2]), 10) + F(int(g[3]), 100) + F(int(g[4]), 1000)),
    (r'^Order from least to greatest: (.+)$', lambda g: ('w', ', '.join(sorted(g[0].split(', '), key=n)))),
    (r'^Add ' + D + r' \+ ' + D + ' and round the sum to the nearest tenth', lambda g: F(math.floor((n(g[0]) + n(g[1])) * 10 + F(1, 2)), 10)),
    (r'Each layer is (\d+) cubes by (\d+) cubes, and there are (\d+) layers', lambda g: int(g[0]) * int(g[1]) * int(g[2])),
    (r'^A box holds (\d+) × (\d+) × (\d+) unit cubes when full\. (\d+) cubes are already inside', lambda g: int(g[0]) * int(g[1]) * int(g[2]) - int(g[3])),
    (r'^The base of a rectangular prism is (\d+) feet by (\d+) feet\. The height is (\d+) feet', lambda g: int(g[0]) * int(g[1]) * int(g[2])),
    (r'One is (\d+) by (\d+) by (\d+) feet\. The other is (\d+) by (\d+) by (\d+) feet\. How much greater', lambda g: abs(int(g[0]) * int(g[1]) * int(g[2]) - int(g[3]) * int(g[4]) * int(g[5]))),
    (r'^A sandbox is (\d+) feet long and (\d+) feet wide\. It holds (\d+) cubic feet', lambda g: F(int(g[2]), int(g[0]) * int(g[1]))),
]


def mx(v):
    w, r = divmod(v.numerator, v.denominator)
    return str(w) if r == 0 else (f'{w} {r}/{v.denominator}' if w else f'{r}/{v.denominator}')


def right(text, want):
    if isinstance(want, tuple):
        return text == want[1]
    m = re.fullmatch(r'(\$?)(\d+ \d+/\d+|\d+/\d+|[\d,]+(?:\.\d+)?)(?: [a-z ]+)?', text)
    if not m:
        return False
    if m.group(1) == '$' and not re.fullmatch(r'\$[\d,]+\.\d\d', text):
        return False
    try:
        return n(m.group(2)) == F(want)
    except Exception:
        return False


def main():
    items = json.load(open(FILE, encoding='utf-8'))['items']
    errors = []
    for qid, e in items.items():
        q = e['to']
        hits = [(rx, fn) for rx, fn in RULES if re.search(rx, q['prompt'])]
        if len(hits) != 1:
            errors.append(f'{qid}: {len(hits)} rules match: {q["prompt"][:90]}')
            continue
        rx, fn = hits[0]
        want = fn(re.search(rx, q['prompt']).groups())
        if not right(q['answer'], want):
            errors.append(f'{qid}: key {q["answer"]!r}, computed {want!r}: {q["prompt"][:90]}')
        if 'options' in q:
            keys = [o['text'] for o in q['options'] if o['correct']]
            if keys != [q['answer']] or len({o['text'] for o in q['options']}) != 4:
                errors.append(f'{qid}: options')
            for o in q['options']:
                if not o['correct'] and right(o['text'], want):
                    errors.append(f'{qid}: distractor {o["text"]!r} is also right')
        if e['from']['prompt'] == q['prompt']:
            errors.append(f'{qid}: not rewritten')
    for x in errors[:40]:
        print(x)
    print(f'Grade 5 levels: {len(items)} rewritten keys checked, {len(errors)} errors')
    sys.exit(1 if errors or len(items) < 200 else 0)


if __name__ == '__main__':
    main()
