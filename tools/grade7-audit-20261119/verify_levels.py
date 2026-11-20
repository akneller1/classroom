"""Whole-site audit 2 #3 (2026-11-20): recompute the keys of the Grade 7 Standard items that levels.py rewrote, from their
printed prompts and independently of levels.py. Every rewritten item must match exactly one rule, and multiple-choice
items must key the option equal to the answer. Usage: python3 tools/grade7-audit-20261119/verify_levels.py"""
import math, os, re, sys
from fractions import Fraction as F
sys.path.insert(0, os.path.dirname(__file__))
import lib

SUP = str.maketrans('⁰¹²³⁴⁵⁶⁷⁸⁹', '0123456789')


def n(s):
    s = s.replace('−', '-').replace(',', '').replace('$', '').strip()
    if ' ' in s and '/' in s:
        w, f = s.split(' ')
        return F(w) + F(f) * (1 if not w.startswith('-') else -1)
    return F(s)


def r1(x, p):
    return F(math.floor(x * 10 ** p + F(1, 2)), 10 ** p)


def same(a, b):
    """Compare a key with a computed value: numbers (units and labels around them are ignored), or exact text."""
    if isinstance(b, str):
        return a.strip() == b
    m = re.fullmatch(r'\s*(?:[a-z] = )?(-?\$?[\d,]*\.?\d+(?:/\d+)?)(?: ?(?:%|°|in\.|ft²|cm²|cm³|in²|cm|ft|feet|miles|milliliters|hours|in\.|square meters))?\s*', a.replace('−', '-'))
    return bool(m) and n(m.group(1)) == F(b)


def sci(a, v):
    m = re.fullmatch(r'([\d.]+) × 10([⁰¹²³⁴⁵⁶⁷⁸⁹]+)', a)
    return bool(m) and 1 <= F(m.group(1)) < 10 and F(m.group(1)) * 10 ** int(m.group(2).translate(SUP)) == v


I = r'(-?\d[\d,]*)'
D = r'(-?\d[\d,]*(?:\.\d+)?)'
Q = r'(-?\d+(?:/\d+)?)'


def lin(s):
    """'3x + 4', '−x − 2', 'x' -> (m, b)."""
    s = s.replace('−', '-').replace(' ', '')
    m = re.fullmatch(r'(-?\d*)x([+-]\d+)?', s)
    k = m.group(1)
    return (F(-1) if k == '-' else F(1) if k == '' else F(k)), F(m.group(2) or 0)


RULES = [
    (r'^In the number (\d+)\.(\d+), what is the value of the digit in the (\w[\w-]*) place, multiplied by 1,000\?$',
     lambda g: F(int(g[1][{'hundredths': 1, 'thousandths': 2, 'ten-thousandths': 3}[g[2]]]), 10 ** ({'hundredths': 2, 'thousandths': 3, 'ten-thousandths': 4}[g[2]])) * 1000),
    (r'^Evaluate: \((\d+) \+ (\d+)\) × (\d+) - (\d+)²$', lambda g: (int(g[0]) + int(g[1])) * int(g[2]) - int(g[3]) ** 2),
    (r'temperature was -(\d+)°F\. It rose (\d+)°F by noon and then fell (\d+)°F', lambda g: -int(g[0]) + int(g[1]) - int(g[2])),
    (r'^Find the value: -(\d+) - \(-(\d+)\) - (\d+)$', lambda g: -int(g[0]) + int(g[1]) - int(g[2])),
    (r'^The pattern ([\d, ]+), … continues by adding the same number\. What is the (\d+)th term\?$', lambda g: (lambda xs: xs[0] + (xs[1] - xs[0]) * (int(g[1]) - 1))([int(x) for x in g[0].split(', ')])),
    (r'Figure 1 uses (\d+) tiles, and each new figure uses (\d+) more tiles .* no more than (\d+) tiles', lambda g: max(k for k in range(1, 500) if int(g[0]) + int(g[1]) * (k - 1) <= int(g[2]))),
    (r'descended (\d+) feet in (\d+) equal stages, then rose (\d+) feet', lambda g: -int(g[0]) + int(g[2])),
    (r'^A point starts at \(' + I + ', ' + I + r'\)\. It moves (\d+) units (left|right) and (\d+) units (up|down)\.',
     lambda g: (lambda X, Y: 'Quadrant ' + ('I' if X > 0 and Y > 0 else 'II' if X < 0 < Y else 'III' if X < 0 and Y < 0 else 'IV'))(int(g[0]) + int(g[2]) * (1 if g[3] == 'right' else -1), int(g[1]) + int(g[4]) * (1 if g[5] == 'up' else -1))),
    (r'rewrites (\d+) \+ (\d+) \+ (\d+) as', lambda g: int(g[0]) + int(g[1]) + int(g[2])),
    (r'rewrites \((\d+) × (\d+)\) × (\d+) as', lambda g: int(g[0]) * int(g[1]) * int(g[2])),
    (r'garden is (\d+) m wide\. Its length is (\d+) m of lettuce plus (\d+) m', lambda g: int(g[0]) * (int(g[1]) + int(g[2]))),
    (r'^Simplify: (\d+)\(x \+ (\d+)\) \+ (\d+)x - (\d+)$', lambda g: ('lin', int(g[0]) + int(g[2]), int(g[0]) * int(g[1]) - int(g[3]))),
    (r'^Is the equation true, false, or open\? (\d+) \+ (\d+) = (\d+) - (\d+)$', lambda g: 'true' if int(g[0]) + int(g[1]) == int(g[2]) - int(g[3]) else 'false'),
    (r'temperature rose (\d+)°F and then fell (\d+)°F, ending at (\d+)°F', lambda g: int(g[2]) - int(g[0]) + int(g[1])),
    (r'ribbon into (\d+) equal pieces of (\d+) cm and had (\d+) cm left over', lambda g: int(g[0]) * int(g[1]) + int(g[2])),
    (r'Adult tickets cost \$(\d+) and child tickets cost \$(\d+)\. A group bought (\d+) tickets for \$(\d+)\. How many child',
     lambda g: int(g[2]) - F(int(g[3]) - int(g[1]) * int(g[2]), int(g[0]) - int(g[1]))),
    (r'speed limit is (\d+) miles per hour and \w+ is driving (\d+) mph under it', lambda g: int(g[0])),
    (r'has \$(\d+) and wants at least \$(\d+)\. \w+ saves \$(\d+) each week', lambda g: -(-(int(g[1]) - int(g[0])) // int(g[2]))),
    (r'has \$(\d+) to spend on shirts that cost \$(\d+) each, plus a one-time \$(\d+) shipping fee', lambda g: (int(g[0]) - int(g[2])) // int(g[1])),
    (r'^Add ' + D + r' \+ ' + D + r', then round the sum to the nearest tenth\.$', lambda g: r1(n(g[0]) + n(g[1]), 1)),
    (r'^Estimate ' + D + ' × ' + D + r' \+ ' + D + ' by rounding', lambda g: r1(n(g[0]), 0) * r1(n(g[1]), 0) + r1(n(g[2]), 0)),
    (r'^Data: ([\d., ]+)\. How much greater is the mean than the median\?', lambda g: (lambda xs: r1(sum(xs) / len(xs) - sorted(xs)[len(xs) // 2], 2))([n(x) for x in g[0].split(', ')])),
    (r'drives (\d+) miles per hour for (\d+) hours and then (\d+) miles per hour for (\d+) hours', lambda g: int(g[0]) * int(g[1]) + int(g[2]) * int(g[3])),
    (r'^Solve: n \+ ' + D + ' - ' + D + ' = ' + D + '$', lambda g: n(g[2]) - n(g[0]) + n(g[1])),
    (r'Solve ' + D + r'g - (\d+) = ' + D + ' to find g', lambda g: (n(g[2]) + int(g[1])) / n(g[0])),
    (r'^A jug holds ' + D + r' liters and a bottle holds (\d+) milliliters', lambda g: n(g[0]) * 1000 + int(g[1])),
    (r'^How many whole numbers from (\d+) to (\d+) are divisible by both (\d+) and (\d+)\?$', lambda g: sum(1 for x in range(int(g[0]), int(g[1]) + 1) if x % int(g[2]) == 0 and x % int(g[3]) == 0)),
    (r'^Use the prime factorizations of (\d+) and (\d+) to find their greatest common factor\.$', lambda g: math.gcd(int(g[0]), int(g[1]))),
    (r'answered (\d+) of (\d+) questions correctly\..*Give the fraction incorrect\.$', lambda g: F(int(g[1]) - int(g[0]), int(g[1]))),
    (r'^How many of these numbers are integers: (.+)\?$', lambda g: sum(1 for x in g[0].split(', ') if re.fullmatch(r'-?\d+', x))),
    (r'^How many of these numbers are irrational: (.+)\?$', lambda g: sum(1 for x in g[0].split(', ') if x.startswith('√') and math.isqrt(int(x[1:])) ** 2 != int(x[1:]))),
    (r'^Add ' + D + r' × 10([⁰¹²³⁴⁵⁶⁷⁸⁹]+) and ' + D + r' × 10([⁰¹²³⁴⁵⁶⁷⁸⁹]+)\. Write the sum in scientific notation\.$',
     lambda g: ('sci', n(g[0]) * 10 ** int(g[1].translate(SUP)) + n(g[2]) * 10 ** int(g[3].translate(SUP)))),
    (r'^Evaluate: ∛(\d+) \+ √(\d+)$', lambda g: round(int(g[0]) ** (1 / 3)) + math.isqrt(int(g[1]))),
    (r'^Order from least to greatest: (.+)$', lambda g: ', '.join(sorted(g[0].split(', '), key=lambda x: F(x)))),
    (r'^Write (\d+) (\d+)/(\d+) as a decimal\.$', lambda g: int(g[0]) + F(int(g[1]), int(g[2]))),
    (r'^Simplify: ' + Q + r' \+ ' + Q + ' - ' + Q + r'\. Write', lambda g: F(g[0]) + F(g[1]) - F(g[2])),
    (r'^Simplify: ' + Q + ' × ' + Q + ' ÷ ' + Q + r'\. Write', lambda g: F(g[0]) * F(g[1]) / F(g[2])),
    (r'^Solve: m \+ ' + Q + ' - ' + Q + ' = ' + Q + '$', lambda g: F(g[2]) - F(g[0]) + F(g[1])),
    (r'has read ' + Q + r' of a book and has (\d+) pages left', lambda g: int(g[1]) / (1 - F(g[0]))),
    (r'^Evaluate: \((\d+)/(\d+)\)([⁰¹²³⁴⁵⁶⁷⁸⁹]+) × (\d+)\. Write', lambda g: F(int(g[0]), int(g[1])) ** int(g[2].translate(SUP)) * int(g[3])),
    (r'Store A sells (\d+) ounces for \$' + D + r' and Store B sells (\d+) ounces for \$' + D + r'\. How many cents per ounce', lambda g: r1(abs(n(g[1]) / int(g[0]) - n(g[3]) / int(g[2])) * 100, 1)),
    (r'^Find x so that (\d+)/(\d+) = x/(\d+), then find x \+ (\d+)\.$', lambda g: F(int(g[0]) * int(g[2]), int(g[1])) + int(g[3])),
    (r'small one has sides (\d+) cm and (\d+) cm\. The longer of those sides on the large triangle is (\d+) cm', lambda g: (int(g[0]) + int(g[1])) * F(int(g[2]), max(int(g[0]), int(g[1])))),
    (r'^Change (\d+)% to a decimal, then use the decimal to find \d+% of (\d+)\.$', lambda g: F(int(g[0]) * int(g[1]), 100)),
    (r'^(\d+) students, which is (\d+)% of the grade, signed up for band\. How many students in the grade did not', lambda g: int(g[0]) * F(100, int(g[1])) - int(g[0])),
    (r'^Write and solve an equation: What number is (\d+)% more than (\d+)\?$', lambda g: int(g[1]) * F(100 + int(g[0]), 100)),
    (r'^A price of \$(\d+) rises (\d+)% and then the new price falls (\d+)%', lambda g: int(g[0]) * F(100 + int(g[1]), 100) * F(100 - int(g[2]), 100)),
    (r'^A \$' + D + r' item is on sale for (\d+)% off\. Sales tax of ' + D + '% is added', lambda g: r1(n(g[0]) * F(100 - int(g[1]), 100) * (100 + n(g[2])) / 100, 2)),
    (r'^y is proportional to x\. When x = (\d+), y = (\d+)\..* when x = (\d+)\.$', lambda g: F(int(g[1]), int(g[0])) * int(g[2])),
    (r'^Factor out the greatest common factor: (\d+)x \+ (\d+)$', lambda g: (lambda a, b, gg: f'{gg}({"" if a // gg == 1 else a // gg}x + {b // gg})')(int(g[0]), int(g[1]), math.gcd(int(g[0]), int(g[1])))),
    (r'taxi charges \$(\d+) plus \$(\d+) per mile\. \w+ also gave a \$(\d+) tip and paid \$(\d+)', lambda g: F(int(g[3]) - int(g[0]) - int(g[2]), int(g[1]))),
    (r'^Solve: (\d+)\(' + D + r't \+ ' + D + r'\) = ' + D + '$', lambda g: (n(g[3]) / int(g[0]) - n(g[2])) / n(g[1])),
    (r'^"(\d+) less than (\d+) times a number is (\d+)\."', lambda g: F(int(g[2]) + int(g[0]), int(g[1]))),
    (r'drives (\d+) miles at (\d+) mph, then (\d+) miles at (\d+) mph\. How many hours', lambda g: F(int(g[0]), int(g[1])) + F(int(g[2]), int(g[3]))),
    (r'deposits \$' + D + r' at ' + D + r'% simple interest per year\. What is the balance after (\d+) years', lambda g: n(g[0]) * (1 + n(g[1]) / 100 * int(g[2]))),
    (r'^For the line y = (.+?), find the y-intercept and the x-intercept\. Give the x-intercept\.$', lambda g: (lambda mb: -mb[1] / mb[0])(lin(g[0]))),
    (r'candle is (\d+) cm tall and burns (\d+) cm per hour\..* height after (\d+) hours', lambda g: int(g[0]) - int(g[1]) * int(g[2])),
    (r'trend line .* is y = ' + D + r'x \+ (\d+)\. About how many hours of practice predict (\d+) points', lambda g: r1((int(g[2]) - int(g[1])) / n(g[0]), 1)),
    (r'^Solve the system: y = (.+?) and y = (.+?)\. Write the solution as an ordered pair\.$',
     lambda g: (lambda a, b: (lambda x: ('pair', x, a[0] * x + a[1]))((b[1] - a[1]) / (a[0] - b[0])))(lin(g[0]), lin(g[1]))),
    (r'^Is the point \(' + I + ', ' + I + r'\) a solution of y < (.+?)\? Answer yes or no\.$', lambda g: (lambda mb: 'yes' if int(g[1]) < mb[0] * int(g[0]) + mb[1] else 'no')(lin(g[2]))),
    (r'There are (\d+) points, and no three lie on the same line\. How many triangles', lambda g: math.comb(int(g[0]), 3)),
    (r'One angle measures (\d+)°\. Find its vertical angle plus twice an adjacent angle', lambda g: int(g[0]) + 2 * (180 - int(g[0]))),
    (r'interior angles that add to (\d+)°\. How many sides', lambda g: int(g[0]) // 180 + 2),
    (r'yard is (\d+) feet by (\d+) feet\. A fence post stands at every corner and every (\d+) feet', lambda g: 2 * (int(g[0]) + int(g[1])) // int(g[2])),
    (r'^A circle has diameter (\d+) in\. Find its circumference\. Use 3\.14', lambda g: F(314, 100) * int(g[0])),
    (r'^Point A\(' + I + ', ' + I + r'\) is rotated 90° counterclockwise about the origin', lambda g: ('pair', -int(g[1]), int(g[0]))),
    (r'parallelogram has base (\d+) in\. and height (\d+) in\. A second parallelogram has the same height and (\d+) times the base', lambda g: int(g[0]) * int(g[1]) * int(g[2])),
    (r'trapezoid has bases (\d+) ft and (\d+) ft and height (\d+) ft\. A rectangle has the same area and width (\d+) ft', lambda g: F((int(g[0]) + int(g[1])) * int(g[2]), 2 * int(g[3]))),
    (r'between circles of radius (\d+) cm and (\d+) cm', lambda g: r1(F(314, 100) * (int(g[0]) ** 2 - int(g[1]) ** 2), 1)),
    (r'bases that are (\d+)-sided polygons\..*Give the number of edges', lambda g: 3 * int(g[0])),
    (r'square pyramid has base edge (\d+) ft and slant height (\d+) ft\. How many square feet of material cover only its four triangular faces', lambda g: 2 * int(g[0]) * int(g[1])),
    (r'square pyramid has base edge (\d+) cm and height (\d+) cm\. A prism with the same base and height holds how many more', lambda g: F(2 * int(g[0]) ** 2 * int(g[1]), 3)),
    (r'^Which whole number is closest to √(\d+)\? Use the perfect squares just below and above \d+\.$', lambda g: min(range(1, 100), key=lambda k: abs(k * k - int(g[0])) + (0 if k * k <= int(g[0]) else 0))),
    (r'^A (\d+)-foot ladder leans against a wall with its base (\d+) feet from the wall', lambda g: math.isqrt(int(g[0]) ** 2 - int(g[1]) ** 2)),
    (r'^Find the perimeter of the right triangle with vertices \(' + I + ', ' + I + r'\), \(' + I + ', ' + I + r'\) and \(' + I + ', ' + I + r'\)\.$',
     lambda g: (lambda a, b: a + b + math.isqrt(a * a + b * b))(abs(int(g[2]) - int(g[0])), abs(int(g[5]) - int(g[3])))),
    (r'machine makes (\d+) parts in (\d+) minutes\..* how many minutes does it need for (\d+) parts', lambda g: F(int(g[2]) * int(g[1]), int(g[0]))),
    (r'30°-60°-90° triangle, the shorter leg is (\d+)\. Find the hypotenuse and the longer leg\. Give the hypotenuse', lambda g: 2 * int(g[0])),
    (r'∠C is the right angle, BC = (\d+) and AC = (\d+)\. Find AB, then tan A', lambda g: F(int(g[0]), int(g[1]))),
    (r"eyes are (\d+) ft above the ground\. From (\d+) ft away, the angle of elevation to the top of a tree is (\d+)°", lambda g: round(int(g[1]) * math.tan(math.radians(int(g[2]))) + int(g[0]))),
    (r'shows: 1–5: (\d+); 6–10: (\d+); 11–15: (\d+); 16–20: (\d+)\. What percent of the values are greater than 10', lambda g: round(100 * (int(g[2]) + int(g[3])) / (int(g[0]) + int(g[1]) + int(g[2]) + int(g[3])))),
    (r'^Data: ([\d, ]+)\. Find the interquartile range\.$', lambda g: (lambda xs: F(xs[6] + xs[7], 2) - F(xs[1] + xs[2], 2))(sorted(int(x) for x in g[0].split(', ')))),
    (r'bag has (\d+) red and (\d+) blue marbles\. You draw one marble, do not replace it', lambda g: F(int(g[0]) * (int(g[0]) - 1), (int(g[0]) + int(g[1])) * (int(g[0]) + int(g[1]) - 1))),
    (r'1st, 2nd and 3rd place be awarded among (\d+) runners', lambda g: int(g[0]) * (int(g[0]) - 1) * (int(g[0]) - 2)),
    (r'^In (\d+) trials, the bus was late (\d+) times\..* in (\d+) trips', lambda g: F(int(g[1]) * int(g[2]), int(g[0]))),
    (r'Class A has a mean of (\d+) push-ups and Class B a mean of (\d+)\. Both have a mean absolute deviation of (\d+)', lambda g: F(int(g[1]) - int(g[0]), int(g[2]))),
    (r'^For the arithmetic sequence (\d+), (\d+), \d+, …, find term (\d+), then add it to the first term\.$', lambda g: 2 * int(g[0]) + (int(g[1]) - int(g[0])) * (int(g[2]) - 1)),
    (r'^For f\(x\) = (\d+)x², find f\((\d+)\) and f\((\d+)\)\. How many times larger', lambda g: F(int(g[2]) ** 2, int(g[1]) ** 2)),
    (r'^A \$' + D + r' item loses (\d+)% of its value each year\. How much value does it lose in total over (\d+) years', lambda g: r1(n(g[0]) * (1 - F(100 - int(g[1]), 100) ** int(g[2])), 2)),
    (r'^Multiply and simplify: \(x \+ (\d+)\)\(x ([+-]) (\d+)\) ([+-]) (\d+)x$', lambda g: ('quad', int(g[0]) + (int(g[2]) if g[1] == '+' else -int(g[2])) + (int(g[4]) if g[3] == '+' else -int(g[4])), int(g[0]) * (int(g[2]) if g[1] == '+' else -int(g[2])))),
    (r'jar has (\d+) quarters and dimes worth \$' + D + r'\. How many dimes', lambda g: int(g[0]) - (n(g[1]) * 100 - 10 * int(g[0])) / 15),
]


def check(a, want):
    a = a.replace('−', '-')
    if isinstance(want, tuple):
        if want[0] == 'lin':
            return a == (f'{want[1]}x + {want[2]}' if want[2] >= 0 else f'{want[1]}x - {-want[2]}')
        if want[0] == 'pair':
            return a == f'({want[1]}, {want[2]})'
        if want[0] == 'sci':
            return sci(a.replace('-', '−'), want[1])
        if want[0] == 'quad':
            b, c = want[1], want[2]
            t = 'x²' + ('' if b == 0 else f' + {b}x' if b > 0 else f' - {-b}x').replace(' 1x', ' x') + (f' + {c}' if c > 0 else f' - {-c}' if c < 0 else '')
            return a == t
    if isinstance(want, str):
        return a == want
    return same(a, want)


def main():
    banks = lib.load()
    errors, n_ = [], 0
    for u, q in lib.items(banks):
        if 'audit 2 #3' not in q.get('sourceNotes', ''):
            continue
        n_ += 1
        P = q['prompt'].replace('−', '-')
        hits = [(rx, fn) for rx, fn in RULES if re.search(rx, P)]
        if len(hits) != 1:
            errors.append(f'{q["id"]}: {len(hits)} rules match: {q["prompt"][:90]}')
            continue
        rx, fn = hits[0]
        want = fn(re.search(rx, P).groups())
        if not check(str(q['answer']), want):
            errors.append(f'{q["id"]}: key {q["answer"]!r}, computed {want!r}: {q["prompt"][:90]}')
        if q['format'] == 'multiple-choice':
            right = [o['text'] for o in q['options'] if o['correct']]
            if right != [q['answer']] or len({o['text'] for o in q['options']}) != len(q['options']):
                errors.append(f'{q["id"]}: options')
            for o in q['options']:
                if not o['correct'] and check(o['text'], want):
                    errors.append(f'{q["id"]}: distractor {o["text"]!r} is also right')
    for e in errors[:50]:
        print(e)
    print(f'Grade 7 levels: {n_} rewritten Standard items checked, {len(errors)} errors')
    sys.exit(1 if errors or n_ < 300 else 0)


if __name__ == '__main__':
    main()
