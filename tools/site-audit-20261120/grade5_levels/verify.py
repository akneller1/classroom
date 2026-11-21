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


# ---------------- More templates (variety follow-up)
def _ld(s):
    """Lowest common denominator of a list of whole numbers."""
    out = 1
    for x in s:
        out = out * int(x) // math.gcd(out, int(x))
    return out


def _round(x, places):
    q = F(1, 10 ** places)
    return F(math.floor(x / q + F(1, 2))) * q


def _ratio_digits(num, d):
    s = num.replace(',', '')
    point = s.index('.') if '.' in s else len(s)
    pos = [i for i, ch in enumerate(s) if ch == d]
    place = lambda i: (point - i - 1) if i < point else (point - i)
    return F(10) ** (place(pos[0]) - place(pos[1]))


def _ceil(x):
    return math.ceil(x)


def _r10(v):
    return int(F(v, 10) + F(1, 2)) * 10


VAR = [
    # classifying two-dimensional figures
    (r'^A rectangle has a perimeter of (\d+) cm\. Its length is (\d+) cm\. What is its width\?$', lambda g: F(int(g[0]), 2) - int(g[1])),
    (r'^\w+ walks around a rectangular park that is (\d+) m long and (\d+) m wide\. \w+ goes around (\d+) times\.', lambda g: 2 * (int(g[0]) + int(g[1])) * int(g[2])),
    (r'^An equilateral triangle has sides of (\d+) cm\. A square has the same perimeter\.', lambda g: F(3 * int(g[0]), 4)),
    (r'^A square and a rectangle have the same perimeter\. The square has sides of (\d+) m\. The rectangle is (\d+) m long\.', lambda g: int(g[0]) ** 2 - int(g[1]) * (2 * int(g[0]) - int(g[1]))),
    (r'^A regular hexagon has sides of (\d+) cm\. A regular pentagon has the same perimeter\.', lambda g: F(6 * int(g[0]), 5)),
    # coordinate plane
    (r'^Point A is at \((\d+), (\d+)\)\. Point B is (\d+) units to the right of A and (\d+) units below A\.', lambda g: ('w', f'({int(g[0]) + int(g[2])}, {int(g[1]) - int(g[3])})')),
    (r'^Start at \((\d+), (\d+)\)\. Move (\d+) units up, then (\d+) units right, then (\d+) units down\. Where do you end\?$', lambda g: ('w', f'({int(g[0]) + int(g[3])}, {int(g[1]) + int(g[2]) - int(g[4])})')),
    (r'^Point A is at \((\d+), (\d+)\) and point B is at \(\d+, (\d+)\)\. Point C is (\d+) units to the right of B\.', lambda g: abs(int(g[2]) - int(g[1])) + int(g[3])),
    (r'^Points A\((\d+), (\d+)\) and B\((\d+), \d+\) are on a horizontal line\. Point M', lambda g: ('w', f'({(int(g[0]) + int(g[2])) // 2}, {g[1]})')),
    (r'^A bug walks from \((\d+), \d+\) to \((\d+), \d+\), then back to \((\d+), \d+\)\.', lambda g: abs(int(g[1]) - int(g[0])) + abs(int(g[1]) - int(g[2]))),
    (r'^A square has corners at \((\d+), \d+\), \((\d+), \d+\), \(\d+, \d+\) and \(\d+, \d+\)\. What is its area', lambda g: (int(g[1]) - int(g[0])) ** 2),
    (r'^A graph shows the cost in dollars \(y\) of x pounds of apples\. It passes through \(0, 0\) and \((\d+), (\d+)\)\. At the same rate, how many dollars do (\d+) pounds cost', lambda g: F(int(g[1]), int(g[0])) * int(g[2])),
    (r'^Line A passes through \(0, 0\) and \(1, (\d+)\)\. Line B passes through \(0, 0\) and \(1, (\d+)\)\. At x = (\d+), how far apart', lambda g: abs(int(g[1]) - int(g[0])) * int(g[2])),
    (r'^The points \(0, (\d+)\), \(2, (\d+)\), \(4, \d+\) follow a pattern\. If the pattern continues, what is y when x = (\d+)\?$', lambda g: int(g[0]) + F(int(g[1]) - int(g[0]), 2) * int(g[2])),
    (r'^Rule: y is (\d+) times x, plus (\d+)\. What point on the graph has x = (\d+)\?$', lambda g: ('w', f'({g[2]}, {int(g[0]) * int(g[2]) + int(g[1])})')),
    (r'^Pattern A has points \(0, (\d+)\), \(1, (\d+)\), .* Pattern B has points \(0, (\d+)\), \(1, (\d+)\), .* For which x do both', lambda g: F(int(g[0]) - int(g[2]), (int(g[3]) - int(g[2])) - (int(g[1]) - int(g[0])))),
    (r'^Rule: y is (\d+) times x, plus (\d+)\. What is the sum of the y-values for x = 1, 2, 3 and 4\?$', lambda g: sum(int(g[0]) * x + int(g[1]) for x in range(1, 5))),
    # data
    (r'^Plant heights in inches: (.+)\. How much more is the total of the 3 tallest plants than the total of the 3 shortest\?$', lambda g: (lambda s: sum(s[3:]) - sum(s[:3]))(sorted(n(v) for v in g[0].split(', ')))),
    (r'^A club buys (\d+) bracelet kits for \$' + D + r' each and sells \d+ bracelets for \$' + D + ' each', lambda g: int(g[0]) * (n(g[2]) - n(g[1]))),
    (r'^A class sells cookies for \$' + D + r' each and brownies for \$' + D + r' each\. They sold (\d+) cookies and (\d+) brownies and spent \$' + D, lambda g: int(g[2]) * n(g[0]) + int(g[3]) * n(g[1]) - n(g[4])),
    # decimals
    (r'^\w+ has \$' + D + r'\. A book costs \$' + D + r' and a pen costs \$' + D + r'\.', lambda g: n(g[0]) - n(g[1]) - n(g[2])),
    (r'^\w+ ran ' + D + ' km on Monday, ' + D + ' km on Tuesday and ' + D + r' km on Wednesday\. How many more kilometers does \w+ need to reach a goal of (\d+) km', lambda g: int(g[3]) - n(g[0]) - n(g[1]) - n(g[2])),
    (r'^Gas costs \$' + D + r' per gallon\. \w+ buys (\d+) gallons of gas and a \$' + D + ' snack', lambda g: n(g[0]) * int(g[1]) + n(g[2])),
    (r'^Cheddar costs \$' + D + r' per pound and Swiss costs \$' + D + r' per pound\. \w+ buys ' + D + ' pounds of cheddar and ' + D + ' pounds of Swiss', lambda g: cents(n(g[0]) * n(g[2]) + n(g[1]) * n(g[3]))),
    (r'^A rectangle is ' + D + ' m long and ' + D + r' m wide\. A second rectangle has the same width and is twice as long\.', lambda g: 2 * n(g[0]) * n(g[1])),
    (r'^A tile is ' + D + ' m by ' + D + r' m\. How many square meters do (\d+) tiles cover', lambda g: n(g[0]) * n(g[1]) * int(g[2])),
    (r'^A wall is ' + D + ' m long and ' + D + r' m high\. A window that is ' + D + ' m by ' + D + ' m is not painted', lambda g: n(g[0]) * n(g[1]) - n(g[2]) * n(g[3])),
    (r'^A rectangle is ' + D + ' m long and ' + D + r' m wide\. Its length grows by ' + D + ' m', lambda g: n(g[1]) * n(g[2])),
    (r'^(\d+) friends share the cost of a \$' + D + r' gift and a \$' + D + ' card equally', lambda g: (n(g[1]) + n(g[2])) / int(g[0])),
    (r'^A 12-pack of juice costs \$' + D + r' and a 6-pack costs \$' + D + r'\. How many cents cheaper per can', lambda g: (n(g[1]) / 6 - n(g[0]) / 12) * 100),
    (r'^A ' + D + '-meter ribbon is cut into pieces that are each ' + D + r' meters long\. \w+ uses (\d+) pieces\.', lambda g: n(g[0]) / n(g[1]) - int(g[2])),
    (r'^\w+ walks ' + D + r' km each day\. How many days does it take \w+ to walk at least (\d+) km', lambda g: _ceil(int(g[1]) / n(g[0]))),
    (r'^A ' + D + r'-meter board is cut into (\d+) pieces that are 0\.5 m long\. How many 0\.25-m pieces', lambda g: (n(g[0]) - F(int(g[1]), 2)) * 4),
    (r'^\w+ earns \$' + D + r' per hour and works (\d+) hours\. Then \w+ spends \$' + D, lambda g: n(g[0]) * int(g[1]) - n(g[2])),
    (r'^Store A sells a 3-pack of markers for \$' + D + r'\. Store B sells single markers for \$' + D + r' each\. \w+ needs 6 markers', lambda g: abs(6 * n(g[1]) - 2 * n(g[0]))),
    # fraction addition and subtraction
    (r'^Find the least common denominator of (\d+/\d+) and (\d+/\d+), then subtract the smaller fraction from the larger\.$', lambda g: abs(F(g[0]) - F(g[1]))),
    (r'^What is the least common denominator of 1/(\d+), 1/(\d+) and 1/(\d+)\?$', lambda g: _ld(g)),
    (r'^\w+ drank (\d+/\d+) liter of water in the morning and (\d+/\d+) liter in the afternoon\.', lambda g: F(g[0]) + F(g[1])),
    (r'^A recipe uses (\d+/\d+) cup of sugar\. It uses (\d+/\d+) cup more flour than sugar\.', lambda g: 2 * F(g[0]) + F(g[1])),
    (r'^\w+ had ' + M + r' yards of ribbon\. \w+ used (\d+/\d+) yard for a bow and (\d+/\d+) yard for a card\.', lambda g: n(g[0]) - F(g[1]) - F(g[2])),
    (r'^A tank of water is drained until it is (\d+/\d+) full\. Then (\d+/\d+) of a tank is added\.', lambda g: 1 - F(g[0]) - F(g[1])),
    (r'^A trail is ' + M + r' miles long\. \w+ has hiked ' + M + ' miles', lambda g: n(g[0]) - n(g[1])),
    (r'^Add ' + M + r' \+ ' + M + r', then subtract ' + M + r'\.$', lambda g: n(g[0]) + n(g[1]) - n(g[2])),
    (r'^\w+ needs ' + M + r' feet of trim\. \w+ has two pieces, ' + M + ' feet and ' + M + ' feet long', lambda g: n(g[0]) - n(g[1]) - n(g[2])),
    (r'^A room is ' + M + ' feet long and ' + M + r' feet wide\. What is its perimeter', lambda g: 2 * (n(g[0]) + n(g[1]))),
    (r'^Estimate (\d+/\d+) − (\d+/\d+)\. Is the difference closest to 0, 1/2 or 1\?$', lambda g: min([F(0), F(1, 2), F(1)], key=lambda v: abs(F(g[0]) - F(g[1]) - v))),
    (r'^Estimate ' + M + r' \+ ' + M + r' to the nearest whole number\.$', lambda g: math.floor(n(g[0]) + n(g[1]) + F(1, 2))),
    # fraction multiplication and division
    (r'^(\d+) pounds of nuts are put equally into (\d+) bags\. How many pounds are in 2 of the bags', lambda g: F(2 * int(g[0]), int(g[1]))),
    (r'^(\d+) liters of juice are shared equally by (\d+) kids, and (\d+) liters are shared equally by (\d+) adults\.', lambda g: F(int(g[2]), int(g[3])) - F(int(g[0]), int(g[1]))),
    (r'^\w+ has (\d+) stickers and gives away (\d+/\d+) of them\.', lambda g: int(g[0]) * (1 - F(g[1]))),
    (r'^A farm has (\d+) animals\. (\d+/\d+) of them are cows\. (\d+/\d+) of the rest are goats\.', lambda g: int(g[0]) * (1 - F(g[1])) * F(g[2])),
    (r'^(\d+/\d+) of a class are girls\. (\d+/\d+) of the girls wear glasses\. What fraction of the class are girls who do not', lambda g: F(g[0]) * (1 - F(g[1]))),
    (r'^A field is (\d+/\d+) km long and (\d+/\d+) km wide\. Half of it is planted', lambda g: F(g[0]) * F(g[1]) / 2),
    (r'^Two square tiles each have sides of ' + M + r' inches\. What is their total area', lambda g: 2 * n(g[0]) ** 2),
    (r'^A rectangle has an area of ' + M + r' square feet and a width of (\d+/\d+) foot\. What is its perimeter', lambda g: 2 * (n(g[0]) / F(g[1]) + F(g[1]))),
    (r'^\w+ shrinks a (\d+)-inch drawing to (\d+/\d+) of its size\.', lambda g: ('w', f'{"shorter" if F(g[1]) < 1 else "longer"}; {mx(int(g[0]) * F(g[1]))} inches')),
    (r'^A recipe uses (\d+) cups of flour\. \w+ multiplies every amount by ' + M + r'\. How many more cups', lambda g: int(g[0]) * (n(g[1]) - 1)),
    (r'^\w+ has (\d+) dollars\. \w+ spends (\d+/\d+) of it on a book and (\d+/\d+) of what is left on lunch\.', lambda g: int(g[0]) * (1 - F(g[1])) * (1 - F(g[2]))),
    (r'^(\d+) cups of trail mix are split into bags that each hold 1/(\d+) cup\. \w+ gives away (\d+) bags\.', lambda g: int(g[0]) * int(g[1]) - int(g[2])),
    (r'^1/(\d+) liter of juice is shared equally by (\d+) kids\. How much of a liter do (\d+) of the kids get together', lambda g: F(int(g[2]), int(g[0]) * int(g[1]))),
    (r'^A (\d+)-meter ribbon is cut in half\. \w+ cuts one half into pieces that are 1/(\d+) meter long\.', lambda g: F(int(g[0]), 2) * int(g[1])),
    (r'^(\d+) kids share (\d+/\d+) of a pizza equally\. What fraction of the whole pizza do 2 of the kids eat', lambda g: 2 * F(g[1]) / int(g[0])),
    (r'^(\d+/\d+) of a pan of lasagna is cut into (\d+) equal pieces\. (\d+) of the pieces (?:is|are) eaten\.', lambda g: F(g[0]) * (int(g[1]) - int(g[2])) / int(g[1])),
    # measurement
    (r'^Convert: (\d+) inches = \? feet \? inches$', lambda g: ('w', f'{int(g[0]) // 12} ft {int(g[0]) % 12} in.')),
    (r'^\w+ is (\d+) feet (\d+) inche?s? tall\. \w+\'s brother is (\d+) inches taller\.', lambda g: 12 * int(g[0]) + int(g[1]) + int(g[2])),
    (r'^A board is (\d+) ft (\d+) in\. long\. It is cut into (\d+) equal pieces\.', lambda g: F(12 * int(g[0]) + int(g[1]), int(g[2]))),
    (r'^A jug holds (\d+) gallons of water\. \w+ pours out (\d+) pints\.', lambda g: 8 * int(g[0]) - int(g[1])),
    (r'^\w+ buys (\d+) pounds? (\d+) ounces? of cheese and (\d+) pounds? (\d+) ounces? of ham\.', lambda g: 16 * (int(g[0]) + int(g[2])) + int(g[1]) + int(g[3])),
    (r'^A rope is (\d+) meters long\. \w+ cuts off (\d+) centimeters\.', lambda g: 100 * int(g[0]) - int(g[1])),
    (r'^(\d+) boxes each weigh (\d+) grams\. What is their total weight in kilograms', lambda g: F(int(g[0]) * int(g[1]), 1000)),
    (r'^A (\d+)-liter bottle of water fills (\d+) glasses that each hold (\d+) milliliters\.', lambda g: 1000 * int(g[0]) - int(g[1]) * int(g[2])),
    (r'^Juice comes in (\d+)-milliliter cans\. How many cans are needed to fill a (\d+)-liter punch bowl', lambda g: _ceil(F(1000 * int(g[1]), int(g[0])))),
    # multi-digit multiplication and division
    (r'^\w+ buys (\d+) boxes of pencils with (\d+) pencils in each box\. \w+ already had (\d+) pencils\.', lambda g: int(g[0]) * int(g[1]) + int(g[2])),
    (r'^A school orders (\d+) packs of paper for each of (\d+) classrooms\. Each pack has (\d+) sheets\.', lambda g: int(g[0]) * int(g[1]) * int(g[2])),
    (r'^Estimate (\d+) × (\d+) by rounding each factor to the nearest ten\.$', lambda g: _r10(int(g[0])) * _r10(int(g[1]))),
    (r'^Round (\d+) and (\d+) to the nearest ten and multiply\. What is the difference between that estimate and the exact product', lambda g: abs(_r10(int(g[0])) * _r10(int(g[1])) - int(g[0]) * int(g[1]))),
    (r'^Divide: ' + I + r' ÷ (\d+)\. Write the quotient and the remainder\.$', lambda g: ('w', f'{int(g[0].replace(",", "")) // int(g[1])} R{int(g[0].replace(",", "")) % int(g[1])}')),
    (r'^\w+ has ' + I + r' cards and puts them in rows of (\d+)\. How many more cards', lambda g: (lambda rem: int(g[1]) - rem if rem else 0)(int(g[0].replace(',', '')) % int(g[1]))),
    (r'^A factory makes ' + I + r' toys\. They are packed (\d+) to a box, and (\d+) boxes fit in a crate\.', lambda g: _ceil(F(_ceil(F(int(g[0].replace(',', '')), int(g[1]))), int(g[2])))),
    (r'^A baker has (\d+) eggs\. Each cake uses (\d+) eggs\. After making as many cakes as possible, how many more eggs', lambda g: (lambda rem: int(g[1]) - rem if rem else 0)(int(g[0]) % int(g[1]))),
    (r'^(\d+) gallons of paint are shared equally among (\d+) rooms\. How many quarts', lambda g: F(4 * int(g[0]), int(g[1]))),
    # expressions and patterns
    (r'^Evaluate: \((\d+) \+ (\d+)\) × (\d+) − (\d+) ÷ (\d+)$', lambda g: (int(g[0]) + int(g[1])) * int(g[2]) - F(int(g[3]), int(g[4]))),
    (r'^Evaluate: (\d+) − \[(\d+) × \((\d+) − (\d+)\)\] ÷ (\d+)$', lambda g: int(g[0]) - F(int(g[1]) * (int(g[2]) - int(g[3])), int(g[4]))),
    (r'^Write an expression for "subtract (\d+) from (\d+), then multiply by (\d+)"', lambda g: (int(g[1]) - int(g[0])) * int(g[2])),
    (r'^Write an expression for "(\d+) times the sum of (\d+) and (\d+), minus (\d+)"', lambda g: int(g[0]) * (int(g[1]) + int(g[2])) - int(g[3])),
    (r'^(\d+) × (\d+) = ' + I + r'\. Use this, without multiplying again, to find \d+ × (\d+)\.$', lambda g: int(g[0]) * int(g[3])),
    (r'^(\d+) − (\d+) = (\d+)\. Use this, without subtracting again, to find (\d+) × \(\d+ − \d+\) \+ (\d+)\.$', lambda g: int(g[3]) * (int(g[0]) - int(g[1])) + int(g[4])),
    (r'^Without finding either value, decide which is greater: (\d+) × \((\d+) \+ (\d+)\) or \d+ × \d+ \+ \d+\.', lambda g: (int(g[0]) - 1) * int(g[2])),
    (r'^A pattern starts at (\d+)\. The rule is "Subtract (\d+)\." What is term (\d+)\?$', lambda g: int(g[0]) - (int(g[2]) - 1) * int(g[1])),
    (r'^A pattern starts at (\d+)\. The rule is "Add (\d+)\." Which term is the first one greater than (\d+)\?$', lambda g: ('w', f'term {next(k for k in range(1, 999) if int(g[0]) + (k - 1) * int(g[1]) > int(g[2]))}')),
    (r'^Pattern A: start at 0, add (\d+)\. Pattern B: start at 0, add (\d+)\. Make ordered pairs \(A term, B term\)\. What is the sixth ordered pair\?$', lambda g: ('w', f'({5 * int(g[0])}, {5 * int(g[1])})')),
    (r'^Pattern A: start at (\d+), add (\d+)\. Pattern B: start at (\d+), add (\d+)\. Which term number is the same in both patterns\?$', lambda g: ('w', f'term {next(k for k in range(1, 999) if int(g[0]) + (k - 1) * int(g[1]) == int(g[2]) + (k - 1) * int(g[3]))}')),
    # place value
    (r'^In ([\d.,]+), the digit (\d) appears twice\. How many times as large is the value of the left', lambda g: _ratio_digits(g[0], g[1])),
    (r'^What is 1/10 of 1/10 of ' + I + r'\?$', lambda g: F(int(g[0].replace(',', '')), 100)),
    (r'^' + D + r' × 10([²³]) = \?$', lambda g: n(g[0]) * 10 ** (2 if g[1] == '²' else 3)),
    (r'^A stack of 1,000 sheets of paper is (\d+) mm tall\. How tall is a stack of 100 sheets', lambda g: F(int(g[0]), 10)),
    (r'^What number is (\d) × 100 \+ (\d) × 1 \+ (\d) × \(1/10\) \+ (\d) × \(1/1000\)\?$', lambda g: 100 * int(g[0]) + int(g[1]) + F(int(g[2]), 10) + F(int(g[3]), 1000)),
    (r'^What number is (\d) hundreds more and (\d) tenths less than ' + D + r'\?$', lambda g: n(g[2]) + 100 * int(g[0]) - F(int(g[1]), 10)),
    (r'^Order from greatest to least: (.+)$', lambda g: ('w', ', '.join(sorted(g[0].split(', '), key=n, reverse=True)))),
    (r'^Compare ' + D + ' and ' + D + r'\. How much greater is the greater number\?$', lambda g: abs(n(g[0]) - n(g[1]))),
    (r'^Four long jumps measured (.+) meters\. What is the total of the two longest jumps\?$', lambda g: sum(sorted(n(v) for v in g[0].split(', '))[2:])),
    (r'^Subtract ' + D + ' − ' + D + r' and round the difference to the nearest tenth\.$', lambda g: _round(n(g[0]) - n(g[1]), 1)),
    (r'^Round ' + D + ' to the nearest hundredth and ' + D + r' to the nearest tenth, then add', lambda g: _round(n(g[0]), 2) + _round(n(g[1]), 1)),
    # volume
    (r'^Each layer of a box holds (\d+) × (\d+) unit cubes\. The full box holds (\d+) unit cubes\.', lambda g: F(int(g[2]), int(g[0]) * int(g[1]))),
    (r'^Box A holds (\d+) × (\d+) × (\d+) unit cubes\. Box B holds (\d+) × (\d+) × (\d+) unit cubes\.', lambda g: abs(int(g[0]) * int(g[1]) * int(g[2]) - int(g[3]) * int(g[4]) * int(g[5]))),
    (r'^A box holds (\d+) × (\d+) × (\d+) unit cubes when full\. It is filled halfway to the top\.', lambda g: F(int(g[0]) * int(g[1]) * int(g[2]), 2)),
    (r'^A box is (\d+) cubes long, (\d+) cubes wide and \d+ cubes tall\. It has (\d+) unit cubes inside, packed layer by layer\.', lambda g: (lambda L: L - int(g[2]) % L)(int(g[0]) * int(g[1]))),
    (r'^A rectangular prism has a base area of (\d+) square centimeters and a height of (\d+) centimeters\. What is the volume of 2', lambda g: 2 * int(g[0]) * int(g[1])),
    (r'^Cubes with edges of (\d+) inches are packed into a box that is (\d+) in\. by (\d+) in\. by (\d+) in\.', lambda g: F(int(g[1]) * int(g[2]) * int(g[3]), int(g[0]) ** 3)),
    (r'^A figure is made of two rectangular prisms that do not overlap\. One is (\d+) by (\d+) by (\d+) cm and the other is (\d+) by (\d+) by (\d+) cm', lambda g: int(g[0]) * int(g[1]) * int(g[2]) + int(g[3]) * int(g[4]) * int(g[5])),
    (r'^A (\d+) by (\d+) by (\d+) cm block has a (\d+) by (\d+) by (\d+) cm box-shaped hole', lambda g: int(g[0]) * int(g[1]) * int(g[2]) - int(g[3]) * int(g[4]) * int(g[5])),
    (r'^A pool is (\d+) m long, (\d+) m wide and \d+ m deep\. Water fills it to a depth of (\d+) m\.', lambda g: int(g[0]) * int(g[1]) * int(g[2])),
    (r'^Box A is (\d+) by (\d+) by (\d+) inches\. Box B has the same volume and a base that is (\d+) by (\d+) inches\.', lambda g: F(int(g[0]) * int(g[1]) * int(g[2]), int(g[3]) * int(g[4]))),
    (r'^A sandbox is (\d+) ft long, (\d+) ft wide and (\d+) ft deep\. Sand costs \$' + D + ' per cubic foot', lambda g: int(g[0]) * int(g[1]) * int(g[2]) * n(g[3])),
]
RULES = RULES + VAR


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
        q = dict(e['to'], prompt=re.sub(r'\b([Aa])n (?=\d)', r'\1 ', e['to']['prompt']))  # 'an 8-meter' reads as 'a 8-meter'
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
    sys.exit(1 if errors or len(items) < 1200 else 0)


if __name__ == '__main__':
    main()
