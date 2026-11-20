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
    (r'^How many tiles that are (\d+/\d+) foot by (\d+/\d+) foot are needed to cover a rectangle that is (\d+) feet by (\d+) (?:feet|foot)', lambda g: int(g[2]) * int(g[3]) / (F(g[0]) * F(g[1]))),
    (r'^Without multiplying, is ' + M + r' × (\d+) greater than, less than, or equal to \d+\? Then find the product\.$',
     lambda g: (lambda f, k: ('w', ('less than' if f < 1 else 'greater than' if f > 1 else 'equal to') + '; ' + mx(f * k)))(n(g[0]), int(g[1]))),
    (r'^Divide, then multiply: (\d+/\d+) ÷ (\d+) × (\d+)$', lambda g: F(g[0]) / int(g[1]) * int(g[2])),
    (r'^(\d+) kids share (\d+/\d+) of a cake equally', lambda g: F(g[1]) / int(g[0])),
    (r'^Convert: (\d+) feet (\d+) inche?s? = \? inches$', lambda g: 12 * int(g[0]) + int(g[1])),
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


# ---------------- Advanced (honors) rewrites
ADV = [
    (r'^An art kit has (\d+) triangles, (\d+) pentagons and (\d+) octagons\.', lambda g: 3 * int(g[0]) + 5 * int(g[1]) + 8 * int(g[2])),
    (r'^In a right triangle, one acute angle measures (\d+)°\.', lambda g: 90 - int(g[0])),
    (r'square with sides of (\d+) cm\. Then \w+ adds (\d+) cm of wire and bends all of it into an equilateral triangle', lambda g: F(4 * int(g[0]) + int(g[1]), 3)),
    (r'^A rectangle is (\d+) m by (\d+) m\. A square has the same perimeter\.', lambda g: F(int(g[0]) + int(g[1]), 2)),
    (r'^Point P is at \((\d+), (\d+)\)\. Point Q has an x-coordinate (\d+) times as large as P and the same y-coordinate', lambda g: (int(g[2]) - 1) * int(g[0])),
    (r'^A rectangle has corners at \((\d+), (\d+)\), \((\d+), \d+\), \(\d+, (\d+)\) and', lambda g: 2 * ((int(g[2]) - int(g[0])) + (int(g[3]) - int(g[1])))),
    (r'saved dollars \(y\) after weeks \(x\) passes through \(0, 0\), \((\d+), (\d+)\) and \(\d+, \d+\)\. At the same rate, how many dollars are saved after (\d+) weeks', lambda g: F(int(g[1]), int(g[0])) * int(g[2])),
    (r'^Points \(0, (\d+)\), \(1, (\d+)\), \(2, \d+\), … follow a pattern\. For which x is y = (\d+)\?$', lambda g: F(int(g[2]) - int(g[0]), int(g[1]) - int(g[0]))),
    (r'^Ribbon lengths in feet: (.+)\. What is the total length of the pieces that are at least 2 feet long\?$', lambda g: sum(n(v) for v in g[0].split(', ') if n(v) >= 2)),
    (r'^Four beakers hold (.+) liters\. All the water is poured together and shared equally among the 4 beakers', lambda g: sum(n(v) for v in g[0].split(', ')) / 4),
    (r'^A class sold (\d+) muffins at \$' + D + r' each and spent \$' + D + r' on ingredients\. They want a profit of at least \$(\d+)\.', lambda g: math.ceil((int(g[3]) - (int(g[0]) * n(g[1]) - n(g[2]))) / n(g[1]))),
    (r'had \$' + D + r', earned \$' + D + r' and then spent \$' + D + r'\. How much money is left', lambda g: n(g[0]) + n(g[1]) - n(g[2])),
    (r'^Apples cost \$' + D + r' per pound\. \w+ buys ' + D + r' pounds\. What is the cost to the nearest cent', lambda g: cents(n(g[0]) * n(g[1]))),
    (r'garden bed is ' + D + ' m long and ' + D + r' m wide\. It is covered with soil ' + D + ' m deep', lambda g: n(g[0]) * n(g[1]) * n(g[2])),
    (r'^(\d+) friends split a \$' + D + r' bill equally\. \w+ also leaves a \$' + D + ' tip', lambda g: n(g[1]) / int(g[0]) + n(g[2])),
    (r'^A ' + D + '-meter rope is cut into as many ' + D + r'-meter pieces as possible\. How many meters are left over', lambda g: n(g[0]) - (n(g[0]) // n(g[1])) * n(g[1])),
    (r'^Pack A has (\d+) bars for \$' + D + r'\. Pack B has (\d+) bars for \$' + D + r'\. How many cents per bar', lambda g: F(math.floor(abs(n(g[1]) / int(g[0]) - n(g[3]) / int(g[2])) * 1000 + F(1, 2)), 10)),
    (r'^Rewrite (\d+)/(\d+) and (\d+)/(\d+) with their least common denominator\. What is the sum of the two new numerators', lambda g: (lambda l: int(g[0]) * l // int(g[1]) + int(g[2]) * l // int(g[3]))(math.lcm(int(g[1]), int(g[3])))),
    (r'walked (\d+/\d+) mile to school, (\d+/\d+) mile to the library and (\d+) miles? home', lambda g: F(g[0]) + F(g[1]) + int(g[2])),
    (r'^A jar was (\d+/\d+) full of rice\. \w+ used (\d+/\d+) of a jar and then added (\d+/\d+) of a jar', lambda g: F(g[0]) - F(g[1]) + F(g[2])),
    (r'^A board is ' + M + r' ft long\. \w+ adds a ' + M + r' ft board, then cuts off ' + M + ' ft', lambda g: n(g[0]) + n(g[1]) - n(g[2])),
    (r'^Estimate (\d+/\d+) \+ (\d+/\d+) \+ (\d+/\d+) to the nearest half', lambda g: (lambda s_: min([F(k, 2) for k in range(7)], key=lambda x: (abs(s_ - x), x)))(F(g[0]) + F(g[1]) + F(g[2]))),
    (r'read (\d+/\d+) of a book on Monday and (\d+/\d+) of it on Tuesday\. On Wednesday \w+ read half of what was left', lambda g: (1 - F(g[0]) - F(g[1])) / 2),
    (r'^(\d+) cups of soup are poured equally into (\d+) pots\. Then ' + M + ' (?:cups are|cup is) taken out of each pot', lambda g: F(int(g[0]), int(g[1])) - n(g[2])),
    (r'^A class has (\d+) students\. (\d+/\d+) of them walk to school\. How many students do not walk', lambda g: int(g[0]) - math.floor(F(g[1]) * int(g[0]))),
    (r'^A rectangle is (\d+/\d+) m by (\d+/\d+) m\. \w+ makes (\d+) of them', lambda g: F(g[0]) * F(g[1]) * int(g[2])),
    (r'^Garden A is ' + M + ' m by ' + M + r' m\. Garden B is ' + M + ' m by ' + M + r' m\. How many more square meters', lambda g: abs(n(g[0]) * n(g[1]) - n(g[2]) * n(g[3]))),
    (r'^Without multiplying, ' + M + r' × (\d+) is greater than ' + M + r' × \d+ because .* How much greater is it\?$', lambda g: (n(g[0]) - n(g[2])) * int(g[1])),
    (r'^(\d+/\d+) of a pan of brownies is shared equally by (\d+) friends\. If every friend always gets that same amount', lambda g: int(g[1]) / F(g[0])),
    (r'^A (\d+)-foot board is cut into pieces that are 1/(\d+) foot long\. \w+ uses (\d+) pieces', lambda g: F(int(g[0]) * int(g[1]) - int(g[2]), int(g[1]))),
    (r'^A rope is (\d+) ft (\d+) in\. long\. \w+ cuts off (\d+) inches\. How long is the rope now, in feet and inches', lambda g: (lambda t_: ('w', f'{t_ // 12} ft {t_ % 12} in.'))(12 * int(g[0]) + int(g[1]) - int(g[2]))),
    (r'packs (\d+) cans that weigh (\d+) ounces each\. What is the total weight in pounds and ounces', lambda g: (lambda t_: ('w', f'{t_ // 16} lb {t_ % 16} oz'))(int(g[0]) * int(g[1]))),
    (r'^A bag holds (\d+) kg (\d+) g of flour\. It is split equally into (\d+) containers\.', lambda g: round(F(int(g[0]) * 1000 + int(g[1]), int(g[2])))),
    (r'^(\d+) pitchers each hold (\d+) liters\. How many full (\d+)-milliliter cups', lambda g: int(g[0]) * int(g[1]) * 1000 // int(g[2])),
    (r'^A theater has (\d+) seats in each section\. Section A is sold out on (\d+) nights and section B on (\d+) nights', lambda g: int(g[0]) * (int(g[1]) + int(g[2]))),
    (r'^Estimate (\d+) × (\d+) by rounding each factor to its greatest place value, then find the exact product\.', lambda g: (lambda a, b: abs(round(a, -(len(str(a)) - 1)) * round(b, -(len(str(b)) - 1)) - a * b))(int(g[0]), int(g[1]))),
    (r'^' + I + r' stickers are put into packs of (\d+)\. How many full packs', lambda g: int(g[0].replace(',', '')) // int(g[1])),
    (r'^' + I + r' students ride buses that each hold (\d+) students', lambda g: -(-int(g[0].replace(',', '')) // int(g[1]))),
    (r'^(\d+) yards of ribbon are shared equally by (\d+) friends\. How many feet', lambda g: F(3 * int(g[0]), int(g[1]))),
    (r'^Evaluate: (\d+) × \[(\d+) \+ \((\d+) − (\d+)\)\] \+ (\d+)$', lambda g: int(g[0]) * (int(g[1]) + int(g[2]) - int(g[3])) + int(g[4])),
    (r'^Write an expression for "(half|one third|one fourth) of the difference of (\d+) and (\d+)"', lambda g: F(int(g[1]) - int(g[2]), {'half': 2, 'one third': 3, 'one fourth': 4}[g[0]])),
    (r'^(\d+) \+ (\d+) = ' + I + r'\. Use this, without adding again, to find (\d+) × \(\d+ \+ \d+\)\.$', lambda g: int(g[3]) * (int(g[0]) + int(g[1]))),
    (r'^A pattern starts at (\d+)\. The rule is "Multiply by (\d+)\." What is the sum of the first (\d+) terms\?$', lambda g: sum(int(g[0]) * int(g[1]) ** i for i in range(int(g[2])))),
    (r'^Pattern A: start at 0, add (\d+)\. Pattern B: start at 0, add (\d+)\. When the A term is (\d+), what is the B term', lambda g: F(int(g[2]) * int(g[1]), int(g[0]))),
    (r'^One number has a (\d) in the (\w+) place\. Another has a \d in the (\w+) place\.', lambda g: (lambda v: v[g[1]] / v[g[2]])({'thousands': F(1000), 'hundreds': F(100), 'tens': F(10), 'ones': F(1), 'tenths': F(1, 10), 'hundredths': F(1, 100)})),
    (r'^' + D + r' × ' + I + r' ÷ (\d+) = \?$', lambda g: n(g[0]) * n(g[1]) / int(g[2])),
    (r'^In (\d)(\d)\d(?:\.(\d)\d*)?, how much greater is the value of the hundreds digit than the value of the tenths digit', lambda g: int(g[0]) * 100 - F(int(g[2] or 0), 10)),
    (r'^Four runners finished in (.+) minutes\. What is the difference between the fastest and slowest', lambda g: (lambda xs: max(xs) - min(xs))([n(v) for v in g[0].split(', ')])),
    (r'^Round ' + D + ' and ' + D + r' to the nearest whole number, then add\. How far', lambda g: abs(round(n(g[0])) + round(n(g[1])) - n(g[0]) - n(g[1]))),
    (r'^A box is (\d+) cubes long, (\d+) cubes wide and (\d+) cubes tall\. A second box has (\d+) times as many layers', lambda g: int(g[0]) * int(g[1]) * int(g[2]) * (1 + int(g[3]))),
    (r'^A box holds (\d+) × (\d+) × (\d+) unit cubes when full\. (\d+) full layers are already packed', lambda g: int(g[0]) * int(g[1]) * (int(g[2]) - int(g[3]))),
    (r'^A rectangular prism has a volume of (\d+) cubic inches\. Its length is (\d+) inches and its height is (\d+) inches', lambda g: F(int(g[0]), int(g[1]) * int(g[2]))),
    (r'^A shelf unit is (\d+) boxes that are (\d+) by (\d+) by (\d+) cm and one box that is (\d+) by (\d+) by (\d+) cm', lambda g: int(g[0]) * int(g[1]) * int(g[2]) * int(g[3]) + int(g[4]) * int(g[5]) * int(g[6])),
    (r'^A fish tank is (\d+) in\. long, (\d+) in\. wide and (\d+) in\. tall\. It is filled to (\d+) in\. below the top', lambda g: int(g[0]) * int(g[1]) * (int(g[2]) - int(g[3]))),
]
RULES = RULES + ADV


def mx(v):
    w, r = divmod(v.numerator, v.denominator)
    return str(w) if r == 0 else (f'{w} {r}/{v.denominator}' if w else f'{r}/{v.denominator}')


def right(text, want):
    if isinstance(want, tuple):
        return text == want[1]
    m = re.fullmatch(r'(\$?)(\d+ \d+/\d+|\d+/\d+|[\d,]+(?:\.\d+)?)(?: [a-z ]+|°)?', text)
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
