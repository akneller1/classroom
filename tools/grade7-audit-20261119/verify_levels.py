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
    m = re.fullmatch(r'\s*(?:[a-z] = )?(-?\$?[\d,]*\.?\d+(?:/\d+)?)(?: ?(?:%|°|in\.|ft²|cm²|cm³|in²|cm|ft|feet|miles|milliliters|hours|in\.|square meters|[°a-zA-Z][a-zA-Z.²³° ]*))?\s*', a.replace('−', '-'))
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
    (r'^"(\d+) less than (\d+) times a number is (-?\d+)\."', lambda g: F(int(g[2]) + int(g[0]), int(g[1]))),
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


# ---------------- More templates (variety follow-up); prompts are read with − as -
def _rnd(x, p=0):
    return F(math.floor(F(x) * 10 ** p + F(1, 2)), 10 ** p)


def _ratcount(items):
    sq = {k * k for k in range(1, 40)}
    return sum(1 for x in items if not (x == 'π' or (x.startswith('√') and int(x[1:]) not in sq)))


def _tan(a):
    return math.tan(math.radians(a))


def _mx(x):
    x = F(x)
    w, f = divmod(x.numerator, x.denominator)
    return str(w) if f == 0 else (f'{w} {f}/{x.denominator}' if w else f'{f}/{x.denominator}')


VAR = [
    (r'^The temperature was (-?\d+)°F at 6 a\.m\. It fell (\d+)°F by noon and then rose (\d+)°F by evening\.', lambda g: int(g[0]) - int(g[1]) + int(g[2])),
    (r'^A diver is at -(\d+) ft\. She rises (\d+) ft, then dives (\d+) ft deeper\.', lambda g: int(g[0]) - int(g[1]) + int(g[2])),
    (r'^A savings plan starts with \$(\d+) in week 1 and adds \$(\d+) each week after that\. In which week does the total first go over \$(\d+)\?', lambda g: next(k for k in range(1, 999) if int(g[0]) + (k - 1) * int(g[1]) > int(g[2]))),
    (r'^Figure 1 uses (\d+) squares, and each new figure adds (\d+) squares\. How many squares are in Figure (\d+)\?', lambda g: int(g[0]) + (int(g[2]) - 1) * int(g[1])),
    (r'^Figure 1 of a dot pattern has (\d+) dots, and each new figure adds (\d+)\. How many dots do Figure (\d+) and Figure (\d+) have together\?', lambda g: 2 * int(g[0]) + (int(g[2]) + int(g[3]) - 2) * int(g[1])),
    (r'^A triangular sail has base (\d+) m and height (\d+) m\. Sailcloth costs \$(\d+) per square meter\.', lambda g: F(int(g[0]) * int(g[1]), 2) * int(g[2])),
    (r'^A lot is a rectangle (\d+) m by (\d+) m\. A right triangle with legs (\d+) m and (\d+) m is cut off', lambda g: int(g[0]) * int(g[1]) - F(int(g[2]) * int(g[3]), 2)),
    (r'^A round table top has diameter (\d+) ft and a square table top has sides of (\d+) ft\. Use 3\.14', lambda g: F(314, 100) * F(int(g[0]), 2) ** 2 - int(g[1]) ** 2),
    (r'^A cylindrical can has radius (\d+) cm and height (\d+) cm\. Use 3\.14 for π \(1 cm³ = 1 mL\)\. How many full cans can be filled from a (\d+)-liter jug\?', lambda g: int(1000 * int(g[2]) // (F(314, 100) * int(g[0]) ** 2 * int(g[1])))),
    (r'^A menu has (\d+) appetizers, (\d+) main dishes and (\d+) desserts\. A meal is one of each\. If (\d+) of the main dishes are sold out, how many fewer', lambda g: int(g[0]) * int(g[3]) * int(g[2])),
    (r'^A spinner landed on blue (\d+) times in (\d+) spins\. Using the experimental probability, how many times would you expect blue in (\d+) spins\?', lambda g: F(int(g[0]), int(g[1])) * int(g[2])),
    (r'^In a random sample of (\d+) shoppers, (\d+) paid with cash\. The store has (\d+) shoppers a day\.', lambda g: F(int(g[0]) - int(g[1]), int(g[0])) * int(g[2])),
    (r'^Estimate ' + D + ' × ' + D + ' - ' + D + r' by rounding each number to the nearest whole number\.$', lambda g: _rnd(n(g[0])) * _rnd(n(g[1])) - _rnd(n(g[2]))),
    (r'buys ' + D + r' pounds of grapes at \$' + D + ' per pound and ' + D + r' pounds of cherries at \$' + D + r' per pound\. Estimate', lambda g: _rnd(n(g[0])) * _rnd(n(g[1])) + _rnd(n(g[2])) * _rnd(n(g[3]))),
    (r'^A cyclist rides ' + D + ' miles in ' + D + r' hours\. At the same rate, how many hours will ' + D + r' miles take\?', lambda g: n(g[2]) * n(g[1]) / n(g[0])),
    (r'has \$' + D + r'\. \w+ buys (\d+) books for \$' + D + r' each and then earns \$' + D + r'\. Write and solve an equation for the final balance b\.', lambda g: n(g[0]) - int(g[1]) * n(g[2]) + n(g[3])),
    (r'^Use the prime factorizations of (\d+) and (\d+) to find their least common multiple\.$', lambda g: math.lcm(int(g[0]), int(g[1]))),
    (r'^A class has (\d+) students and (\d+) are wearing blue\. What fraction of the class is not wearing blue\?', lambda g: ('frac', F(int(g[0]) - int(g[1]), int(g[0])))),
    (r'^(\d+) of (\d+) seeds sprouted\. Write the fraction that did not sprout in simplest form\. At that rate, how many of (\d+) seeds', lambda g: F(int(g[1]) - int(g[0]), int(g[1])) * int(g[2])),
    (r'^Five morning temperatures \(°C\) were (.+)\. How many degrees warmer was the warmest morning than the coldest\?', lambda g: (lambda xs: max(xs) - min(xs))([n(x) for x in g[0].split(', ')])),
    (r'^How many of these numbers are rational: (.+)\?$', lambda g: _ratcount(g[0].split(', '))),
    (r'^A gym charges \$(\d+) to join and \$(\d+) per month\. Write a rule for the total cost y after x months, then find the cost for (\d+) months\.', lambda g: int(g[0]) + int(g[1]) * int(g[2])),
    (r'^A trend line for plant height y \(cm\) after x weeks is y = ' + D + r'x \+ (\d+)\. A plant measured ' + D + r' cm at week (\d+)\.', lambda g: abs(n(g[2]) - (n(g[0]) * int(g[3]) + int(g[1])))),
    (r'^A farm stand sold (\d+) pies and cakes for \$(\d+)\. Pies cost \$(\d+) and cakes cost \$(\d+)\.', lambda g: F(int(g[2]) * int(g[0]) - int(g[1]), int(g[2]) - int(g[3]))),
    (r'^For the arithmetic sequence (\d+), (\d+), \d+, …, which term number has the value (\d+)\?$', lambda g: F(int(g[2]) - int(g[0]), int(g[1]) - int(g[0])) + 1),
    (r'^One paper cup is (\d+) cm tall, and each cup added to a stack adds (\d+) cm\. How many cups make a stack (\d+) cm tall\?$', lambda g: F(int(g[2]) - int(g[0]), int(g[1])) + 1),
    (r'^A ball is dropped from (\d+) ft\. Its height after t seconds is h = \d+ - 16t² feet\. How many feet does it fall between t = (\d+) and t = (\d+)\?$', lambda g: 16 * (int(g[2]) ** 2 - int(g[1]) ** 2)),
    (r'^A town of ' + I + r' people grows (\d+)% each year\. What is its population after 2 years\?', lambda g: _rnd(n(g[0]) * F(100 + int(g[1]), 100) ** 2)),
    (r'invests \$' + I + r' at (\d+)% interest compounded once a year\. How much more is the account worth after 3 years than after 2 years\?', lambda g: _rnd(n(g[0]) * F(100 + int(g[1]), 100) ** 2 * F(int(g[1]), 100), 2)),
    (r'^A box has length x \+ (\d+), width x and height (\d+)\. Write its volume as a polynomial, then find the volume when x = (\d+)\.$', lambda g: int(g[1]) * int(g[2]) * (int(g[2]) + int(g[0]))),
    (r'^A square garden is x m by x m\. It is made (\d+) m longer and (\d+) m narrower\. Write the new area as a polynomial, then find it when x = (\d+)\.$', lambda g: (int(g[2]) + int(g[0])) * (int(g[2]) - int(g[1]))),
    (r'^A jar has (\d+) nickels and dimes worth \$' + D + r'\. How many nickels are there\?$', lambda g: F(10 * int(g[0]) - 100 * n(g[1]), 5)),
    (r'^A bank holds quarters and nickels\. There are (\d+) more nickels than quarters, and the coins are worth \$' + D + r'\.', lambda g: (100 * n(g[1]) - 5 * int(g[0])) / 30),
    (r'started with \$(\d+) and paid (\d+) equal bills\. \w+ now has \$(\d+)\.', lambda g: F(int(g[0]) - int(g[2]), int(g[1]))),
    (r'^Two whole numbers have a difference of (\d+) and a product of (\d+)\. Guess, check and revise', lambda g: next(x for x in range(1, 999) if x * (x - int(g[0])) == int(g[1]))),
    (r'^Write (\d+)/(\d+) as a decimal, then add ' + D + r'\.$', lambda g: F(int(g[0]), int(g[1])) + n(g[2])),
    (r'^A recipe needs (\d+) cups of flour\. \w+ has (\d+ \d+/\d+) cups\. How many more cups are needed\? Write the answer as a decimal\.$', lambda g: int(g[0]) - n(g[1])),
    (r'^Simplify: (\d+ \d+/\d+|\d+) - (\d+/\d+) \+ (\d+/\d+)\. Write the answer as a mixed number', lambda g: ('mixed', n(g[0]) - F(g[1]) + F(g[2]))),
    (r'^A board is (\d+(?: \d+/\d+)?) ft long\. \w+ cuts off (\d+(?: \d+/\d+)?) ft and then (\d+(?: \d+/\d+)?) ft\. Write and solve an equation', lambda g: ('mixedx', n(g[0]) - n(g[1]) - n(g[2]))),
    (r'^Find x so that (\d+)/(\d+) = (\d+)/x, then find 2x\.$', lambda g: 2 * F(int(g[1]) * int(g[2]), int(g[0]))),
    (r'^A recipe uses ' + D + r' cups of rice for (\d+) people\. How many cups are needed for (\d+) people, and how many more', lambda g: n(g[0]) * int(g[2]) / int(g[1]) - n(g[0])),
    (r'^A map scale is 1 cm : (\d+) km\. Two towns are ' + D + r' cm apart on the map\. A car drives at (\d+) km/h\.', lambda g: n(g[1]) * int(g[0]) / int(g[2])),
    (r'^Write (\d+)/(\d+) as a percent, then find that percent of (\d+)\.$', lambda g: F(int(g[0]), int(g[1])) * int(g[2])),
    (r'^Three stores take (\d+/\d+) off, ' + D + r' off and (\d+)% off a \$(\d+) item\.', lambda g: max(F(g[0]), n(g[1]), F(int(g[2]), 100)) * int(g[3])),
    (r'^A shirt is (\d+)% off, and then an extra (\d+)% is taken off the sale price\. What single percent', lambda g: 100 - F((100 - int(g[0])) * (100 - int(g[1])), 100)),
    (r'^Write and solve an equation: ' + D + r' is (\d+)% of what number\?$', lambda g: n(g[0]) * 100 / int(g[1])),
    (r'^A store marks up a \$(\d+) jacket by (\d+)%, and then (\d+)% sales tax is added\.', lambda g: _rnd(int(g[0]) * F(100 + int(g[1]), 100) * F(100 + int(g[2]), 100), 2)),
    (r'^A price of \$(\d+) falls (\d+)% and then the new price rises (\d+)%\. What is the final price\?$', lambda g: int(g[0]) * F(100 - int(g[1]), 100) * F(100 + int(g[2]), 100)),
    (r'^A town of ' + I + r' people grows (\d+)% one year and (\d+)% the next year\.', lambda g: _rnd(n(g[0]) * F(100 + int(g[1]), 100) * F(100 + int(g[2]), 100))),
    (r'^A meal costs \$' + D + r'\. Sales tax of (\d+)% is added, and a (\d+)% tip is figured on the price before tax\.', lambda g: _rnd(n(g[0]) * F(100 + int(g[1]) + int(g[2]), 100), 2)),
    (r'^A store buys a bike for \$(\d+) and marks it up (\d+)%\. During a sale it takes (\d+)% off the marked price\.', lambda g: int(g[0]) * F(100 + int(g[1]), 100) * F(100 - int(g[2]), 100) - int(g[0])),
    (r'^A table shows gallons of gas x: ([\d, ]+) and cost y: (.+)\. Show the relationship is proportional, then find the cost of (\d+) gallons\.$', lambda g: (lambda xs, ys: (ys[0] / xs[0]) * int(g[2]) if all(y / x == ys[0] / xs[0] for x, y in zip(xs, ys)) else None)([int(x) for x in g[0].split(', ')], [n(y) for y in g[1].split(', ')])),
    (r'^A price p is discounted (\d+)%\. Write the sale price p - ' + D + r'p as a single term, and use it to find the sale price when p = \$' + D, lambda g: _rnd(n(g[2]) * F(100 - int(g[0]), 100), 2)),
    (r'^A TV screen is (\d+) in\. wide and (\d+) in\. tall\. How much longer is its diagonal than its width\?$', lambda g: F(math.isqrt(int(g[0]) ** 2 + int(g[1]) ** 2)) - int(g[0]) if math.isqrt(int(g[0]) ** 2 + int(g[1]) ** 2) ** 2 == int(g[0]) ** 2 + int(g[1]) ** 2 else None),
    (r'^A pump fills (\d+) liters in (\d+) minutes\. At the same rate, how many minutes does it take to fill a (\d+)-liter tank\?$', lambda g: F(int(g[2]) * int(g[1]), int(g[0]))),
    (r'^A (\d+)-ft pole casts a (\d+)-ft shadow\. At the same time, a tree casts a (\d+)-ft shadow\.', lambda g: F(int(g[0]) * int(g[2]), int(g[1])) - int(g[0])),
    (r'^In a 45°-45°-90° triangle, each leg is (\d+)\. What is the hypotenuse\?$', lambda g: f'{g[0]}√2'),
    (r'^An equilateral triangle has sides of (\d+) cm\. Using a 30°-60°-90° triangle, what is its height\?$', lambda g: f'{int(g[0]) // 2}√3 cm' if int(g[0]) % 2 == 0 else None),
    (r'^A kite string is (\d+) ft long and makes a (\d+)° angle with the ground\. How high is the kite\? Round to the nearest tenth', lambda g: _rnd(F(int(g[0]) * math.sin(math.radians(int(g[1])))), 1)),
    (r'^A ladder makes a (\d+)° angle with the ground and reaches (\d+) ft up a wall\. How far is the base', lambda g: _rnd(F(int(g[1]) / _tan(int(g[0]))), 1)),
    (r'^From the top of a (\d+)-ft lighthouse, the angle of depression to a boat is (\d+)°\. Later it is (\d+)°\.', lambda g: _rnd(F(int(g[0]) / _tan(int(g[1])) - int(g[0]) / _tan(int(g[2]))))),
    (r'^A taxi charges \$' + D + r' plus \$' + D + r' per mile\. \w+\'s fare was \$' + D + r'\.', lambda g: (n(g[2]) - n(g[0])) / n(g[1])),
    (r'^"The sum of (\d+) times a number and (\d+) is (-?\d+)\." Write the equation and solve for the number\.$', lambda g: F(int(g[2]) - int(g[1]), int(g[0]))),
    (r'\'s sister is (\d+) years older than \w+\. The sum of their ages is (\d+)\.', lambda g: F(int(g[1]) - int(g[0]), 2)),
    (r'^Solve A = \(1/2\)bh for h\. Then find the height of a triangle with area ' + D + r' cm² and base (\d+) cm\.$', lambda g: 2 * n(g[0]) / int(g[1])),
    (r'borrows \$' + I + r' at ' + D + r'% simple interest per year for (\d+) years\. How much interest is paid\?$', lambda g: n(g[0]) * n(g[1]) / 100 * int(g[2])),
    (r'^\$' + I + r' is invested at (\d+)% interest compounded once a year for 2 years\. How much interest is earned\?', lambda g: _rnd(n(g[0]) * F(100 + int(g[1]), 100) ** 2 - n(g[0]), 2)),
    (r'^Two angles are complementary\. One measures \(3x \+ (\d+)\)° and the other \(2x \+ (\d+)\)°\.', lambda g: (lambda x: max(3 * x + int(g[0]), 2 * x + int(g[1])))(F(90 - int(g[0]) - int(g[1]), 5))),
    (r'^Each interior angle of a regular polygon measures (\d+)°\. How many sides does the polygon have\?$', lambda g: F(360, 180 - int(g[0]))),
    (r'^A square garden has sides of (\d+) m\. Posts go at each corner and every (\d+) m along the sides\.', lambda g: F(4 * int(g[0]), int(g[1]))),
    (r'^Two sides of a triangle are (\d+) cm and (\d+) cm\. The third side is a whole number of centimeters\.', lambda g: sum(1 for c in range(1, 99) if abs(int(g[0]) - int(g[1])) < c < int(g[0]) + int(g[1]))),
    (r'^Point A\((-?\d+), (-?\d+)\) is rotated 180° about the origin\. What are the coordinates of A′\?$', lambda g: ('pair', -int(g[0]), -int(g[1]))),
    (r'^Point A\((-?\d+), (-?\d+)\) is reflected over the x-axis and then translated (\d+) units right\.', lambda g: ('pair', int(g[0]) + int(g[2]), -int(g[1]))),
]
RULES = RULES + VAR


def check(a, want):
    a = a.replace('−', '-')
    if isinstance(want, tuple):
        if want[0] == 'lin':
            return a == (f'{want[1]}x + {want[2]}' if want[2] >= 0 else f'{want[1]}x - {-want[2]}')
        if want[0] == 'pair':
            return a == f'({want[1]}, {want[2]})'
        if want[0] == 'sci':
            return sci(a.replace('-', '−'), want[1])
        if want[0] == 'frac':
            return a == (str(want[1].numerator) if want[1].denominator == 1 else f'{want[1].numerator}/{want[1].denominator}')
        if want[0] == 'mixed':
            return a == _mx(want[1])
        if want[0] == 'mixedx':
            return a == f'x = {_mx(want[1])} ft'
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
        if 'audit 2 #3' not in q.get('sourceNotes', '') or (q['level'] != 'cp1' and 'multistep2' not in q['sourceNotes']):
            continue   # other Advanced rewrites come from honors.py, the generators of the Advanced h-items (verify_keys.py)
        n_ += 1
        P = re.sub(r'\b([Aa])n (?=\d)', r'\1 ', q['prompt'].replace('−', '-'))   # 'an 8-ft' reads as 'a 8-ft'
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
    print(f'Grade 7 levels: {n_} rewritten Standard items and new-template Advanced items checked, {len(errors)} errors')
    sys.exit(1 if errors or n_ < 300 else 0)


if __name__ == '__main__':
    main()
