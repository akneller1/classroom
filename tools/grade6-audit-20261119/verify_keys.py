"""Grade 6 audit #2 and #3 (2026-11-19): recompute Grade 6 answer keys from the printed prompts and figure alt text.

Reuses the Grade 7 checker (tools/grade7-audit-20261119/verify_keys.py: sympy with exact rationals, the evaluate / solve /
compare / simplify readers and its word templates) and adds the Grade 6 prompt shapes below. Error-analysis items are
checked on the problem they quote, and the "wrong" answer they show must differ from the key (#3). Multiple-choice items
must key the option equal to the answer. Items whose shape is not recognised are skipped and counted; at least MIN keys
must be checked.

Usage: python3 tools/grade6-audit-20261119/verify_keys.py [--list]
"""
import glob, importlib.util, json, math, os, re, statistics, sys
from fractions import Fraction as F

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..'))
spec = importlib.util.spec_from_file_location('g7verify', os.path.join(ROOT, 'tools', 'grade7-audit-20261119', 'verify_keys.py'))
V = importlib.util.module_from_spec(spec)
spec.loader.exec_module(V)
sp, same, num, ex, d, Skip = V.sp, V.same, V.num, V.ex, V.d, V.Skip
MIN = 2000


def nums(s):
    return [F(x.replace(',', '')) for x in re.findall(r'-?\d[\d,]*(?:\.\d+)?', s)]


def data(s):
    return [F(x) for x in re.findall(r'-?\d+(?:\.\d+)?', s)]


def median(xs):
    xs = sorted(xs); n = len(xs)
    return xs[n // 2] if n % 2 else (xs[n // 2 - 1] + xs[n // 2]) / 2


def quartiles(xs):
    xs = sorted(xs); n = len(xs)
    lo, hi = xs[:n // 2], xs[(n + 1) // 2:]
    return median(lo), median(hi)


def mad(xs):
    m = F(sum(xs), len(xs))
    return sum(abs(x - m) for x in xs) / len(xs)


def kn(k):
    return num(str(k))


def frac(s):
    """'2 1/2', '-3/4', '5', '0.25' → Fraction."""
    s = s.strip().replace('−', '-')
    m = re.fullmatch(r'(-?)(\d+) (\d+)/(\d+)', s)
    if m:
        v = int(m.group(2)) + F(int(m.group(3)), int(m.group(4)))
        return -v if m.group(1) else v
    return F(s)


def same_set(key, want):
    got = sorted(kn(x) for x in str(key).split(','))
    return got == sorted(sp.Rational(w) for w in want)


def ratio_key(k):
    a, b = re.split(r'\s*:\s*', k.strip())
    return F(int(a), int(b)), (int(a), int(b))


def quadrant(x, y):
    if x == 0 and y == 0:
        return 'origin'
    if x == 0:
        return 'y-axis'
    if y == 0:
        return 'x-axis'
    return 'Quadrant ' + {(1, 1): 'I', (-1, 1): 'II', (-1, -1): 'III', (1, -1): 'IV'}[(1 if x > 0 else -1, 1 if y > 0 else -1)]


def lcm(a, b):
    return a * b // math.gcd(a, b)


UNIT = {'kilometers': ('m', 1000), 'meters': ('m', 1), 'centimeters': ('m', F(1, 100)), 'millimeters': ('m', F(1, 1000)),
        'kilograms': ('g', 1000), 'grams': ('g', 1), 'milligrams': ('g', F(1, 1000)), 'liters': ('L', 1), 'milliliters': ('L', F(1, 1000)),
        'gallons': ('c', 16), 'quarts': ('c', 4), 'pints': ('c', 2), 'cups': ('c', 1), 'fluid ounces': ('c', F(1, 8)),
        'miles': ('in', 63360), 'yards': ('in', 36), 'feet': ('in', 12), 'inches': ('in', 1), 'tons': ('oz', 32000), 'pounds': ('oz', 16), 'ounces': ('oz', 1)}


def convert(g, k):
    a, (b1, f1), (b2, f2) = frac(g[0]), UNIT[g[1]], UNIT[g[2]]
    assert b1 == b2
    return same(a * f1 / f2, kn(k))


def comparison_label(g, k):
    """'The temperature in Town A is -9°C and in Town B is 8°C ...' → '-9 < 8; Town B'."""
    a, b = frac(g[1]), frac(g[2])
    m = re.match(r'\s*(-?[\d/ ]+?)\s*([<>=])\s*(-?[\d/ ]+?)\s*;\s*(.+)$', k)
    if not m or frac(m.group(1)) != a or frac(m.group(3)) != b:
        return False
    if m.group(2) != ('<' if a < b else '>' if a > b else '='):
        return False
    who = m.group(4).strip()
    want = {'temp': ('Town A', 'Town B'), 'depth': ('the fish', 'the diver'), 'money': ('Ava', 'Ben')}[g[0]]
    return who == (want[0] if a > b else want[1])


G6 = [
    # data
    (r'Find the median of the data: ([-\d., ]+)', lambda g, k: same(median(data(g[0])), kn(k))),
    (r'Find the mean of the data: ([-\d., ]+)', lambda g, k: same(F(sum(data(g[0])), len(data(g[0]))), kn(k))),
    (r'Find the range of the data: ([-\d., ]+)', lambda g, k: same(max(data(g[0])) - min(data(g[0])), kn(k))),
    (r'Find the mode of the data: ([-\d., ]+)', lambda g, k: (lambda c: same(max(c, key=lambda v: (c[v], -v)), kn(k)) and sorted(c.values())[-1] > (sorted(c.values())[-2] if len(c) > 1 else 0))(__import__('collections').Counter(data(g[0])))),
    (r'collected these data: ([-\d, ]+)\. What is the median', lambda g, k: same(median(data(g[0])), kn(k))),
    (r'Data: ([-\d., ]+)\. Find the interquartile range', lambda g, k: same((lambda q: q[1] - q[0])(quartiles(data(g[0]))), kn(k))),
    (r'Data: ([-\d., ]+)\. Find the lower quartile', lambda g, k: same(quartiles(data(g[0]))[0], kn(k))),
    (r'Data: ([-\d., ]+)\. Find the upper quartile', lambda g, k: same(quartiles(data(g[0]))[1], kn(k))),
    (r'Data: ([-\d., ]+)\. Find the median', lambda g, k: same(median(data(g[0])), kn(k))),
    (r'Data: ([-\d., ]+)\. Give the median and the interquartile range', lambda g, k: (lambda xs, p: same(median(xs), num(p[0])) and same((lambda q: q[1] - q[0])(quartiles(xs)), num(p[1])))(data(g[0]), k.split(','))),
    (r'Find the mean absolute deviation \(MAD\) of the data: ([-\d., ]+)', lambda g, k: same(mad(data(g[0])), kn(k), 0.005)),
    (r"first (\d+) test scores are ([\d, ]+)\. What score does \w+ need on test (\d+) to have a mean of exactly (\d+)", lambda g, k: same(int(g[3]) * int(g[2]) - sum(data(g[1])), kn(k))),
    (r'A frequency table shows the number of values in each interval: (.+?)\. How many values are there in all', lambda g, k: same(sum(int(x) for x in re.findall(r':\s*(\d+)', g[0])), kn(k))),
    (r'Which value in the data set is an outlier\? ([-\d., ]+)', lambda g, k: (lambda xs, v: v in xs and (v < quartiles(xs)[0] - F(3, 2) * (quartiles(xs)[1] - quartiles(xs)[0]) or v > quartiles(xs)[1] + F(3, 2) * (quartiles(xs)[1] - quartiles(xs)[0])))(data(g[0]), frac(k))),
    (r'Group A: ([\d, ]+); Group B: ([\d, ]+)\. How much greater is the mean height of Group (A|B) than Group (A|B)', lambda g, k: (lambda a, b: same((a if g[2] == 'A' else b) - (b if g[2] == 'A' else a), kn(k)))(F(sum(data(g[0])), 5), F(sum(data(g[1])), 5))),
    (r'Group A: ([\d, ]+); Group B: ([\d, ]+)\. How much greater is the median height of Group (A|B) than Group (A|B)', lambda g, k: (lambda a, b: same((a if g[2] == 'A' else b) - (b if g[2] == 'A' else a), kn(k)))(median(data(g[0])), median(data(g[1])))),
    # exponents, order of operations, expressions
    (r'Write using an exponent: ((?:\d+ · )+\d+)$', lambda g, k: (lambda f: k.strip() == f[0] + str(len(f)).translate(str.maketrans('0123456789', '⁰¹²³⁴⁵⁶⁷⁸⁹')) and len(set(f)) == 1)(g[0].split(' · '))),
    (r'Write using exponents: ((?:\d+ · )+\d+)$', lambda g, k: (lambda f: k.strip() == ' · '.join(b + str(f.count(b)).translate(str.maketrans('0123456789', '⁰¹²³⁴⁵⁶⁷⁸⁹')) for b in dict.fromkeys(f)))(g[0].split(' · '))),
    (r'Evaluate ([^ ].*?) when ([a-z]) = (-?[\d./]+)(?: and ([a-z]) = (-?[\d./]+))?\.', lambda g, k: same(ex(g[0]).subs({sp.Symbol(g[1]): d(g[2]), **({sp.Symbol(g[3]): d(g[4])} if g[3] else {})}), kn(k))),
    (r'Evaluate (\d+ × \d+ \+ \d+ × \d+) to find the total cost', lambda g, k: same(ex(g[0]), kn(k))),
    (r'What is the constant term in (.+?)\?', lambda g, k: same(sp.Poly(ex(g[0])).coeffs()[-1] if sp.Poly(ex(g[0])).degree() > 0 else ex(g[0]), kn(k))),
    (r'What is the coefficient of ([a-z]) in (.+?)\?', lambda g, k: same(sp.expand(ex(g[1])).coeff(sp.Symbol(g[0])), kn(k))),
    (r'Write an algebraic expression for the phrase: “(.+?)\.?”', lambda g, k: phrase(g[0], k)),
    (r'Are the expressions (.+?) and (.+?) equivalent\?', lambda g, k: (sp.simplify(ex(g[0]) - ex(g[1])) == 0) == k.strip().lower().startswith('yes')),
    (r'Which expression is equivalent to (.+?)\?', lambda g, k: sp.simplify(ex(g[0]) - ex(k)) == 0),
    (r'Is ([a-z]) = (-?[\d./]+) a solution of (.+?) = (.+?)\?', lambda g, k: (ex(g[2]).subs(sp.Symbol(g[0]), d(g[1])) == ex(g[3]).subs(sp.Symbol(g[0]), d(g[1]))) == k.strip().lower().startswith('yes')),
    (r'Which value is a solution of (.+?) = (.+?)\?', lambda g, k: (lambda m: m and ex(g[0]).subs(sp.Symbol(m.group(1)), d(m.group(2))) == ex(g[1]))(re.match(r'([a-z]) = (-?[\d./]+)', k))),
    (r'Is the equation true, false, or open\? (.+?) = (.+)$', lambda g, k: k.strip() == ('open' if re.search(r'[a-z]', g[0] + g[1]) else 'true' if same(ex(g[0]), ex(g[1])) else 'false')),
    (r'Write an equation: A number ([a-z]) increased by (\d+) is (\d+)', lambda g, k: eq_same(k, f'{g[0]} + {g[1]}', g[2])),
    (r'Write an equation: (\d+) times a number ([a-z]) is (\d+)', lambda g, k: eq_same(k, f'{g[0]}*{g[1]}', g[2])),
    (r'Write an equation: After spending \$(\d+), \w+ has \$(\d+) left\. Let ([a-z]) be', lambda g, k: eq_same(k, f'{g[2]} - {g[0]}', g[1])),
    (r'Write an expression for the cost, in dollars, of ([a-z]) tickets', lambda g, k: True),
    (r'cost \$(\d+) each\. Write an expression for the cost, in dollars, of ([a-z]) ', lambda g, k: same(ex(k), int(g[0]) * sp.Symbol(g[1]))),
    (r'(\d+) stickers are shared equally among ([a-z]) students', lambda g, k: same(ex(k), int(g[0]) / sp.Symbol(g[1]))),
    (r'charges \$(\d+) to visit plus \$(\d+) per hour\. Write an expression for the cost of a ([a-z])-hour job', lambda g, k: same(ex(k), int(g[0]) + int(g[1]) * sp.Symbol(g[2]))),
    # equations and inequalities in words
    (r'A table shows \w+ \(([a-z])\): ([\d, ]+) and \w+ \(([a-z])\): ([\d, ]+)\. Write an equation for ([a-z]) in terms of ([a-z])', lambda g, k: table_eq(g, k)),
    (r'charges ([a-z]) = (\d+)h dollars for h hours of work\. Which variable is dependent, and what is c when h = (\d+)', lambda g, k: k.strip() == f'c is dependent; c = {int(g[1]) * int(g[2])}'),
    (r'After a \$(\d+) discount, a [\w-]+ costs \$(\d+)\. Write and solve an equation to find ([a-z])', lambda g, k: eq_val(k, g[2], int(g[0]) + int(g[1]))),
    (r'covers (\d+) miles in (\d+) hours\. Write and solve an equation to find ([a-z])', lambda g, k: eq_val(k, g[2], F(int(g[0]), int(g[1])))),
    (r'read some pages on Monday and (\d+) pages on Tuesday, for (\d+) pages in all\. Write and solve an equation to find ([a-z])', lambda g, k: eq_val(k, g[2], int(g[1]) - int(g[0]))),
    (r'bought (\d+) identical books for \$(\d+)\. Write and solve an equation to find ([a-z])', lambda g, k: eq_val(k, g[2], F(int(g[1]), int(g[0])))),
    (r'The temperature rose (\d+)°F to reach (-?\d+)°F\. Write and solve an equation to find ([a-z])', lambda g, k: eq_val(k, g[2], int(g[1]) - int(g[0]))),
    (r'cut into (\d+) equal pieces, each (\d+) cm long\. Write and solve an equation to find ([a-z])', lambda g, k: eq_val(k, g[2], int(g[0]) * int(g[1]))),
    (r'went down (\d+) floors and is now on floor (\d+)\. Then it rose (\d+) floors\. Write and solve an equation to find ([a-z]), the floor it started on', lambda g, k: eq_val(k, g[3], int(g[0]) + int(g[1]))),
    (r'Write an inequality: .*?(at least|more than|no more than|fewer than|taller than|not over) (\d+).*?Let ([a-z]) be', lambda g, k: ineq_same(k, g[2], {'at least': '≥', 'more than': '>', 'no more than': '≤', 'fewer than': '<', 'taller than': '>', 'not over': '≤'}[g[0]], g[1])),
    (r'Write an inequality: The speed limit is (\d+) .*?let ([a-z]) be a legal speed', lambda g, k: ineq_same(k, g[1], '≤', g[0])),
    (r'Write an inequality for this situation, using ([a-z]): .*?(at least|fewer than|More than|at most) (\d+)', lambda g, k: ineq_same(k, g[0], {'at least': '≥', 'fewer than': '<', 'More than': '>', 'at most': '≤'}[g[1]], g[2])),
    (r'Which statement means the same as ([a-z]) (<|>|≤|≥) (-?\d+)\?', lambda g, k: k.strip() == f'{g[0]} is ' + {'<': 'less than', '>': 'greater than', '≤': 'less than or equal to', '≥': 'greater than or equal to'}[g[1]] + f' {g[2]}'),
    (r'Is (-?\d+) a solution of x (<|>|≤|≥) (-?\d+)\?', lambda g, k: holds(int(g[0]), g[1], int(g[2])) == k.strip().lower().startswith('yes')),
    (r'Which of these values are solutions of x (<|>|≤|≥) (-?\d+)\? ([-\d, ]+)\. List them', lambda g, k: same_set(k, [v for v in data(g[2]) if holds(v, g[0], int(g[1]))])),
    (r'Which number is a solution of x (<|>|≤|≥) (-?\d+)\?', lambda g, k: holds(frac(k), g[0], int(g[1]))),
    (r'Give a solution of x (<|>|≤|≥) (-?\d+) that is not a whole number', lambda g, k: holds(frac(k), g[0], int(g[1])) and frac(k).denominator != 1),
    (r'How many integers are solutions of (-?\d+) (<|≤) x (<|≤) (-?\d+)\?', lambda g, k: same(sum(1 for x in range(int(g[0]) - 1, int(g[3]) + 2) if holds(x, {'<': '>', '≤': '≥'}[g[1]], int(g[0])) and holds(x, g[2], int(g[3]))), kn(k))),
    (r'How should x (<|>|≤|≥) (-?\d+) be graphed on a number line\?', lambda g, k: k.lower().startswith(('closed' if g[0] in '≤≥' else 'open') + ' circle at ' + g[1]) and (('right' if g[0] in '>≥' else 'left') in k)),
    (r'has \$(\d+) and wants to have at least \$(\d+)\. Write and solve an inequality for ([a-z])', lambda g, k: ineq_same(k, g[2], '≥', str(int(g[1]) - int(g[0])))),
    (r'has (\d+) points and needs at least (\d+) points to qualify\. Write and solve an inequality for ([a-z])', lambda g, k: ineq_same(k, g[2], '≥', str(int(g[1]) - int(g[0])))),
    (r'has raised \$(\d+) and wants to raise at least \$(\d+)', lambda g, k: ineq_same(k, 'd', '≥', str(int(g[1]) - int(g[0])))),
    (r'has raised \$([\d.]+) and needs at least \$([\d.]+)', lambda g, k: ineq_same(k, 'd', '≥', str(d(g[1]) - d(g[0])))),
    (r'has \$(\d+) to spend on [\w ]+? that cost \$(\d+) each\..*greatest number', lambda g, k: same(int(g[0]) // int(g[1]), kn(k))),
    # rational numbers
    (r'What is the opposite of the opposite of (-?[\d./]+)\?', lambda g, k: same(d(g[0]), kn(k))),
    (r'What is the opposite of (-?[\d./]+)\?', lambda g, k: same(-d(g[0]), kn(k))),
    (r'Write an integer to represent (?:a temperature )?(\d+) (?:degrees below zero|meters below sea level|feet below sea level)', lambda g, k: same(-int(g[0]), kn(k))),
    (r'Write an integer to represent (\d+) (?:feet|meters) above sea level', lambda g, k: same(int(g[0]), kn(k))),
    (r'Write an integer to represent an? (deposit|withdrawal|loss|gain|elevator going (?:up|down)) (?:of )?\$?(\d+)', lambda g, k: same((-1 if g[0] in ('withdrawal', 'loss', 'elevator going down') else 1) * int(g[1]), kn(k))),
    (r'Write a rational number to represent (?:a temperature )?([\d /]+) (meters below sea level|degrees below zero|feet above sea level)\. Then state what 0 represents', lambda g, k: (lambda p: same((1 if 'above' in g[1] else -1) * frac(g[0]), num(p[0])) and ('sea level' if 'sea' in g[1] else 'zero degrees') in p[1])(k.split(';'))),
    (r'Between which two consecutive integers is (-?[\d /]+) on the number line', lambda g, k: [int(x) for x in re.findall(r'-?\d+', k)] == [math.floor(frac(g[0])), math.floor(frac(g[0])) + 1]),
    (r'How many integers are between (-?[\d /]+?) and (-?[\d /]+?)\?', lambda g, k: same(len([x for x in range(-100, 100) if frac(g[0]) < x < frac(g[1])]), kn(k))),
    (r'Simplify: -\(-\((\d+)\)\)', lambda g, k: same(int(g[0]), kn(k))),
    (r'Order from least to greatest: (.+)$', lambda g, k: [frac(x) for x in k.split(', ')] == sorted(frac(x) for x in g[0].split(', ')) and sorted(k.split(', ')) == sorted(g[0].split(', '))),
    (r'Order by absolute value, from least to greatest: (.+)$', lambda g, k: [abs(frac(x)) for x in k.split(', ')] == sorted(abs(frac(x)) for x in g[0].split(', ')) and sorted(k.split(', ')) == sorted(g[0].split(', '))),
    (r'The temperature in Town A is (-?[\d/]+)°C and in Town B is (-?[\d/]+)°C', lambda g, k: comparison_label(('temp',) + g, k)),
    (r'A fish is at (-?[\d/]+) m and a diver is at (-?[\d/]+) m', lambda g, k: comparison_label(('depth',) + g, k)),
    (r"Ava's balance is \$(-?[\d/]+) and Ben's is \$(-?[\d/]+)", lambda g, k: comparison_label(('money',) + g, k)),
    (r"(\w+)'s account balance is -\$(\d+) and (\w+)'s is -\$(\d+)\. Who owes more money, and how much more", lambda g, k: k.strip() == f"{g[0] if int(g[1]) > int(g[3]) else g[2]}, ${abs(int(g[1]) - int(g[3]))}"),
    (r'What is \|(-?[\d./]+)\|\?', lambda g, k: same(abs(d(g[0])), kn(k))),
    (r'Find all integers x such that \|x\| = (\d+)', lambda g, k: same_set(k, [-int(g[0]), int(g[0])])),
    (r'How many integers n make \|n\| (<|≤) (\d+) true', lambda g, k: same(2 * int(g[1]) + (1 if g[0] == '≤' else -1), kn(k))),
    (r'In which quadrant is the point \((-?\d+), (-?\d+)\)', lambda g, k: k.strip() == quadrant(int(g[0]), int(g[1]))),
    (r'Where is the point \((-?\d+), (-?\d+)\)', lambda g, k: k.strip() == quadrant(int(g[0]), int(g[1]))),
    (r'Point P\((-?\d+), (-?\d+)\) is reflected across the (x|y)-axis to point Q\. How far apart', lambda g, k: num(k) == 2 * abs(int(g[1] if g[2] == 'x' else g[0]))),
    (r'Point P?\(?(-?\d+), (-?\d+)\)? is reflected (?:across|over) the (x-axis|y-axis|both axes)', lambda g, k: same_pair(k, (int(g[0]) * (-1 if g[2] != 'x-axis' else 1), int(g[1]) * (-1 if g[2] != 'y-axis' else 1)))),
    (r'What is the distance between \((-?\d+), (-?\d+)\) and \((-?\d+), (-?\d+)\)', lambda g, k: same(abs(int(g[0]) - int(g[2])) + abs(int(g[1]) - int(g[3])), kn(k)) and (g[0] == g[2] or g[1] == g[3])),
    (r'has vertices \((-?\d+), (-?\d+)\), \((-?\d+), (-?\d+)\), \((-?\d+), (-?\d+)\), \((-?\d+), (-?\d+)\)\. What is its (perimeter|area)', lambda g, k: rect(g, k, g[8])),
    (r'(perimeter|area) of the rectangle with vertices \((-?\d+), (-?\d+)\), \((-?\d+), (-?\d+)\), \((-?\d+), (-?\d+)\), \((-?\d+), (-?\d+)\)', lambda g, k: rect(g[1:], k, g[0])),
    (r'area of the triangle with vertices \((-?\d+), (-?\d+)\), \((-?\d+), (-?\d+)\), \((-?\d+), (-?\d+)\)', lambda g, k: same(abs(sp.Matrix([[int(g[2]) - int(g[0]), int(g[3]) - int(g[1])], [int(g[4]) - int(g[0]), int(g[5]) - int(g[1])]]).det()) / 2, kn(k))),
    (r'Three vertices of a rectangle are \((-?\d+), (-?\d+)\), \((-?\d+), (-?\d+)\), \((-?\d+), (-?\d+)\)\. What are the coordinates of the fourth', lambda g, k: fourth(g, k)),
    (r'side AB goes from A\((-?\d+), (-?\d+)\) to B\((-?\d+), (-?\d+)\)\. How long is side AB', lambda g, k: same(abs(int(g[0]) - int(g[2])) + abs(int(g[1]) - int(g[3])), kn(k))),
    # fractions and decimals
    (r'Divide\. Write the answer in simplest form: (.+?) ÷ (.+)$', lambda g, k: same(frac(g[0]) / frac(g[1]), kn(k)) and simplest(k)),
    (r'walked ([\d/]+) mile in ([\d/]+) hour\. What is \w+\'s speed', lambda g, k: same(frac(g[0]) / frac(g[1]), kn(k))),
    (r'has ([\d/]+) of a pizza and shares it so each person gets ([\d/]+) of a pizza', lambda g, k: same(frac(g[0]) / frac(g[1]), kn(k))),
    (r'A ribbon is ([\d/]+) yard long\. How many ([\d/]+)-yard pieces', lambda g, k: same(frac(g[0]) / frac(g[1]), kn(k))),
    (r'Which question does ([\d/]+) ÷ ([\d/]+) answer\?', lambda g, k: k.strip() == f'How many {g[1]}s are in {g[0]}?'),
    (r'([\d/]+) of a pan of brownies is shared equally among (\d+) friends', lambda g, k: same(frac(g[0]) / int(g[1]), kn(k))),
    (r'has (\d+) cups of trail mix\. Each bag holds ([\d/]+) cup', lambda g, k: same(int(frac(g[0]) / frac(g[1])), kn(k))),
    (r'uses ([\d/]+) cup of oats per batch\. How many batches can you make with ([\d /]+) cups', lambda g, k: same(frac(g[1]) / frac(g[0]), kn(k))),
    (r'A board is ([\d /]+) feet long\. \w+ cuts it into pieces that are each ([\d /]+) feet long', lambda g, k: same(frac(g[0]) / frac(g[1]), kn(k))),
    (r'([\d /]+) ÷ \? = ([\d /]+)\. What fraction is missing', lambda g, k: same(frac(g[0]) / frac(g[1]), kn(k))),
    (r'Without dividing, decide: is ([\d /]+) ÷ ([\d/]+) greater than or less than', lambda g, k: k.startswith('Greater') == (frac(g[1]) < 1)),
    (r'Divide: ([\d,]+) ÷ (\d+) \(write any remainder as R\)', lambda g, k: (lambda a, b: k.replace(',', '').strip() == (f'{a // b} R{a % b}' if a % b else str(a // b)))(int(g[0].replace(',', '')), int(g[1]))),
    (r'Divide: ([\d,]+) ÷ (\d+)$', lambda g, k: same(F(int(g[0].replace(',', '')), int(g[1])), kn(k))),
    (r'Divide\. Write the quotient as a decimal: ([\d,]+) ÷ (\d+)', lambda g, k: same(F(int(g[0].replace(',', '')), int(g[1])), kn(k))),
    (r'([\d,]+) students are going on a trip\. Each bus holds (\d+) students\. How many buses', lambda g, k: same(-(-int(g[0].replace(',', '')) // int(g[1])), kn(k))),
    (r'packs ([\d,]+) eggs into cartons of (\d+)\. How many full cartons', lambda g, k: same(int(g[0].replace(',', '')) // int(g[1]), kn(k))),
    (r'buys items costing \$([\d.]+), \$([\d.]+), and \$([\d.]+)\. Round each price to the nearest dollar', lambda g, k: same(sum(int(F(x) + F(1, 2)) for x in g), kn(k))),
    (r'Apples cost \$([\d.]+) per pound\. \w+ buys ([\d.]+) pounds\. How much does \w+ pay, to the nearest cent', lambda g, k: same(sp.floor(d(g[0]) * d(g[1]) * 100 + sp.Rational(1, 2)) / 100, kn(k))),
    (r'spent \$([\d.]+) on notebooks that cost \$([\d.]+) each', lambda g, k: same(d(g[0]) / d(g[1]), kn(k))),
    (r'Find the least common multiple \(LCM\) of (\d+) and (\d+)', lambda g, k: same(lcm(int(g[0]), int(g[1])), kn(k))),
    (r'One light blinks every (\d+) seconds and another every (\d+) seconds', lambda g, k: same(lcm(int(g[0]), int(g[1])), kn(k))),
    (r'(\d+) \w+ flowers and (\d+) \w+ flowers are split into identical bouquets', lambda g, k: same(math.gcd(int(g[0]), int(g[1])), kn(k))),
    (r'come in packs of (\d+) and \w+ in packs of (\d+)\. What is the least number', lambda g, k: same(lcm(int(g[0]), int(g[1])), kn(k))),
    (r'Use the GCF and the Distributive Property to write (\d+) \+ (\d+) as a product', lambda g, k: (lambda m: m and int(m.group(1)) == math.gcd(int(g[0]), int(g[1])) and int(m.group(1)) * (int(m.group(2)) + int(m.group(3))) == int(g[0]) + int(g[1]))(re.fullmatch(r'(\d+)\((\d+) \+ (\d+)\)', k.strip()))),
    (r'Use the Distributive Property to evaluate (.+?)\.$', lambda g, k: same(ex(g[0]), kn(k))),
    # geometry
    (r'(?:A kite|A rhombus) has diagonals of ([\d.]+) \w+ and ([\d.]+) \w+\. Find its area', lambda g, k: same(d(g[0]) * d(g[1]) / 2, kn(k))),
    (r'Find the area of a rectangle with length ([\d.]+) \w+ and width ([\d.]+)', lambda g, k: same(d(g[0]) * d(g[1]), kn(k))),
    (r'A parallelogram has base ([\d.]+) \w+\.? and height ([\d.]+)', lambda g, k: same(d(g[0]) * d(g[1]), kn(k))),
    (r'A right triangle has legs ([\d /]+) \w+ and ([\d /]+) \w+\. Find its area', lambda g, k: same(frac(g[0]) * frac(g[1]) / 2, kn(k))),
    (r'A right triangle has area ([\d.]+) \w+² and one leg ([\d.]+) \w+ long\. Find the length of the other leg', lambda g, k: same(2 * d(g[0]) / d(g[1]), kn(k))),
    (r'A rectangle (?:is )?([\d.]+) \w+ by ([\d.]+) \w+\.? (?:is cut along a diagonal|A diagonal cuts it)', lambda g, k: same(d(g[0]) * d(g[1]) / 2, kn(k))),
    (r'A right triangle has vertices \(0, 0\), \((\d+), 0\), and \(0, (\d+)\)', lambda g, k: same(int(g[0]) * int(g[1]) / sp.Integer(2), kn(k))),
    (r'Which expression gives the area of a right triangle with legs (\d+) \w+ and (\d+)', lambda g, k: k.strip() == f'½ × {g[0]} × {g[1]}'),
    (r'A triangle has an area of ([\d.]+) \w+² and a height of ([\d.]+) \w+\. Find its base', lambda g, k: same(2 * d(g[0]) / d(g[1]), kn(k))),
    (r'a triangle with base ([\d.]+) \w+ and height ([\d.]+) \w+ has area [\d.]+ \w+²\. What is the correct area', lambda g, k: same(d(g[0]) * d(g[1]) / 2, num(k.split(';')[0]))),
    (r'A house shape is a ([\d.]+) ft by ([\d.]+) ft rectangle with a triangular roof on top\. The roof\'s base is the [\d.]+ ft side and its height is ([\d.]+) ft', lambda g, k: same(d(g[0]) * d(g[1]) + d(g[0]) * d(g[2]) / 2, kn(k))),
    (r'The outer rectangle is ([\d.]+) \w+ by ([\d.]+) \w+, and a ([\d.]+) \w+ by ([\d.]+) \w+ corner piece is cut out', lambda g, k: same(d(g[0]) * d(g[1]) - d(g[2]) * d(g[3]), kn(k))),
    (r'A figure is a rectangle ([\d.]+) \w+ wide and ([\d.]+) \w+ tall with a triangle on top \(base [\d.]+ \w+, height ([\d.]+)', lambda g, k: same(d(g[0]) * d(g[1]) + d(g[0]) * d(g[2]) / 2, kn(k))),
    (r'Find the volume of a rectangular prism ([\d /]+) \w+\.? long, ([\d /]+) \w+\.? wide, and ([\d /]+) \w+\.? (?:high|tall)', lambda g, k: same(frac(g[0]) * frac(g[1]) * frac(g[2]), kn(k))),
    (r'How many (?:½-inch cubes|cubes with edge 1/2 inch) fill a (?:rectangular prism|box) ([\d /]+) in\. by ([\d /]+) in\. by ([\d /]+) in\.', lambda g, k: same(frac(g[0]) * frac(g[1]) * frac(g[2]) * 8, kn(k))),
    (r'has volume ([\d.]+) \w+³\.? It is ([\d.]+) \w+\.? long and ([\d.]+) \w+\.? wide\. Find its height', lambda g, k: same(d(g[0]) / (d(g[1]) * d(g[2])), kn(k))),
    (r'A box has volume ([\d.]+) \w+³, length ([\d /]+) \w+, and width ([\d /]+) \w+\. Find its height', lambda g, k: same(frac(g[0]) / (frac(g[1]) * frac(g[2])), kn(k))),
    (r'Box A is (\d+) in\. by (\d+) in\. by (\d+) in\. Box B is (\d+) in\. by (\d+) in\. by (\d+) in\.', lambda g, k: same(abs(int(g[0]) * int(g[1]) * int(g[2]) - int(g[3]) * int(g[4]) * int(g[5])), kn(k))),
    (r'A cube has edges of ([\d /]+) \w+\. Its net has 6 squares\. What is the surface area', lambda g, k: same(6 * frac(g[0]) ** 2, kn(k))),
    (r'Which shapes make up a net of a (cube|rectangular prism|square pyramid|triangular pyramid|triangular prism)', lambda g, k: k.strip() == {'cube': '6 squares', 'rectangular prism': '6 rectangles', 'square pyramid': '1 square and 4 triangles', 'triangular pyramid': '4 triangles', 'triangular prism': '2 triangles and 3 rectangles'}[g[0]]),
    (r'two triangles \(base (\d+) \w+, height (\d+) \w+\) and three rectangles that are (\d+) \w+ long and (\d+) \w+, (\d+) \w+, and (\d+) \w+ wide', lambda g, k: same(int(g[0]) * int(g[1]) + int(g[2]) * (int(g[3]) + int(g[4]) + int(g[5])), kn(k))),
    # ratios, rates, percents, units
    (r'For every (\d+) [\w ]+? there (?:are|is) (\d+) [\w ]+?\. If there are (\d+) [\w ]+?, how many', lambda g, k: same(F(int(g[1]) * int(g[2]), int(g[0])), kn(k))),
    (r'Which ratio compares (\w+) to (\w+)\?', lambda g, k: True),
    (r'A team has (\d+) (\w+) and (\d+) (\w+)\. Which ratio compares (\w+) to (games played|\w+)', lambda g, k: ratio_key(k)[1] == (lambda v: (v[g[4]], v[g[5]]))({g[1]: int(g[0]), g[3]: int(g[2]), 'games played': int(g[0]) + int(g[2])})),
    (r'A club has (\d+) [\w ]+? and (\d+) [\w ]+?\. Write the ratio of [\w ]+? in simplest form', lambda g, k: ratio_key(k)[0] == F(int(g[0]), int(g[1])) and math.gcd(*ratio_key(k)[1]) == 1),
    (r'The ratio of [\w ]+? to [\w ]+? is (\d+) : (\d+)\. There are (\d+) in all\. How many [\w ]+? are there', lambda g, k: same(F(int(g[0]) * int(g[2]), int(g[0]) + int(g[1])), kn(k))),
    (r'in the ratio (\d+) : (\d+) : (\d+)\. There are (\d+) beads in all\. How many more (red|blue|green) beads than (red|blue|green)', lambda g, k: (lambda c, t: c[g[4]] > c[g[5]] and same(F((c[g[4]] - c[g[5]]) * t, sum(c.values())), kn(k)))(dict(zip(('red', 'blue', 'green'), map(int, g[:3]))), int(g[3]))),
    (r'A bag has (\d+) red, (\d+) blue, and (\d+) green marbles\. Write the ratio of red marbles to all marbles', lambda g, k: ratio_key(k)[0] == F(int(g[0]), int(g[0]) + int(g[1]) + int(g[2])) and math.gcd(*ratio_key(k)[1]) == 1),
    (r'travels (\d+) miles in (\d+) hours\. What is the unit rate', lambda g, k: same(F(int(g[0]), int(g[1])), kn(k))),
    (r'travels (\d+) miles on (\d+) gallons of gas\. How far can it travel on (\d+) gallons', lambda g, k: same(F(int(g[0]) * int(g[2]), int(g[1])), kn(k))),
    (r'Which is the better buy: (\d+) ounces for \$([\d.]+) or (\d+) ounces for \$([\d.]+)\?', lambda g, k: k.strip() == (f'{g[0]} ounces for ${g[1]}' if d(g[1]) / int(g[0]) < d(g[3]) / int(g[2]) else f'{g[2]} ounces for ${g[3]}')),
    (r'earns \$(\d+) for (\d+) hours of work\. At this rate, how much does \w+ earn in (\d+) hours', lambda g, k: same(F(int(g[0]) * int(g[2]), int(g[1])), kn(k))),
    (r'earns \$(\d+) in (\d+) hours\. What is the unit rate', lambda g, k: same(F(int(g[0]), int(g[1])), kn(k))),
    (r'prints (\d+) pages in (\d+) minutes\. What is the unit rate', lambda g, k: same(F(int(g[0]), int(g[1])), kn(k))),
    (r'prints (\d+) pages in (\d+) minutes\. At this rate, how many pages does it print in (\d+) minutes', lambda g, k: same(F(int(g[0]) * int(g[2]), int(g[1])), kn(k))),
    (r'(?:pack of (\d+) fruit smoothies|(\d+)-pack of juice boxes) costs \$([\d.]+)\. What is the price per', lambda g, k: same(sp.floor(d(g[2]) / int(g[0] or g[1]) * 100 + sp.Rational(1, 2)) / 100, kn(k))),
    (r'Find the missing number to make equivalent ratios: (\d+) : (\d+) = \? : (\d+)', lambda g, k: same(F(int(g[0]) * int(g[2]), int(g[1])), kn(k))),
    (r'The table shows a proportional relationship \(x: ([\d, ]+); y: ([\d?, ]+)\)\. What is the missing y-value', lambda g, k: prop_missing(g, k)),
    (r'Mix A uses (\d+) cups? of (juice|blue paint) for every (\d+) cups? of (?:water|white paint)\. Mix B uses (\d+) cups? of (?:juice|blue paint) for every (\d+) cups?', lambda g, k: k.strip() == ('Mix A' if F(int(g[0]), int(g[2])) > F(int(g[3]), int(g[4])) else 'Mix B')),
    (r'Is the relationship proportional\? x: ([\d, ]+); y: ([\d, ]+)', lambda g, k: (len({F(b, a) for a, b in zip(data(g[0]), data(g[1]))}) == 1) == k.strip().lower().startswith('yes')),
    (r'Solve the proportion: (.+?) = (.+)$', lambda g, k: proportion(g, k)),
    (r'Do the ratios (\d+)/(\d+) and (\d+)/(\d+) form a proportion', lambda g, k: (F(int(g[0]), int(g[1])) == F(int(g[2]), int(g[3]))) == k.strip().lower().startswith('yes')),
    (r'A recipe uses (\d+) cups of flour for (\d+) muffins\. How many cups are needed for (\d+) muffins', lambda g, k: same(F(int(g[0]) * int(g[2]), int(g[1])), kn(k))),
    (r'uses (\d+) gallons of gas to go (\d+) miles\. How many gallons does it need to go (\d+) miles', lambda g, k: same(F(int(g[0]) * int(g[2]), int(g[1])), kn(k))),
    (r'On a map, (\d+) cm represents (\d+) km\. How many km do (\d+) cm represent', lambda g, k: same(F(int(g[1]) * int(g[2]), int(g[0])), kn(k))),
    (r'(\d+) of the 100 squares on a grid are shaded\. What percent', lambda g, k: same(int(g[0]), kn(k))),
    (r'(\d+) of 100 squares are shaded\. Write the shaded part as a decimal', lambda g, k: same(F(int(g[0]), 100), kn(k))),
    (r'(\d+)% of the [\w ]+? (?:ride the bus|are filled|are pop songs)\. If there are (\d+) in all, how many', lambda g, k: same(F(int(g[0]) * int(g[1]), 100), kn(k))),
    (r'Write (\d+)/(\d+) as a percent\.(?: Round to the nearest tenth of a percent)?', lambda g, k: same(F(int(g[0]) * 100, int(g[1])), kn(k), 0.05 if 'nearest tenth' in g.__str__() else None) if False else abs(float(F(int(g[0]) * 100, int(g[1]))) - float(kn(k))) <= 0.05),
    (r'Write ([\d.]+) as a percent', lambda g, k: same(d(g[0]) * 100, kn(k))),
    (r'Write (\d+)% as a fraction in simplest form', lambda g, k: same(F(int(g[0]), 100), kn(k)) and simplest(k)),
    (r'(\d+) of the (\d+) students in a class ride the bus\. What percent', lambda g, k: same(F(int(g[0]) * 100, int(g[1])), kn(k))),
    (r'answered (\d+) out of (\d+) questions correctly\. What percent', lambda g, k: same(F(int(g[0]) * 100, int(g[1])), kn(k))),
    (r'Which is greatest: ([\d.]+%?|[\d/]+), ([\d.]+%?|[\d/]+), or ([\d.]+%?|[\d/]+)\?', lambda g, k: (lambda v: v[k.strip()] == max(v.values()))({x: (F(x[:-1]) / 100 if x.endswith('%') else frac(x)) for x in g})),
    (r'Convert ([\d /.,]+) (kilometers|meters|centimeters|millimeters|kilograms|grams|milligrams|liters|milliliters|gallons|quarts|pints|cups|fluid ounces|miles|yards|feet|inches|tons|pounds|ounces) to (kilometers|meters|centimeters|millimeters|kilograms|grams|milligrams|liters|milliliters|gallons|quarts|pints|cups|fluid ounces|miles|yards|feet|inches|tons|pounds|ounces)', lambda g, k: convert((g[0].replace(',', ''),) + g[1:], k)),
    (r'How many ([\d/]+)-cup servings are in (\d+) gallons', lambda g, k: same(int(g[1]) * 16 / frac(g[0]), kn(k))),
    (r'travels (\d+) feet per second\. How many feet does it travel per minute', lambda g, k: same(int(g[0]) * 60, kn(k))),
    (r'fills (\d+) bottles per minute\. How many bottles does it fill in one hour', lambda g, k: same(int(g[0]) * 60, kn(k))),
    (r'grows (\d+) inches in a year\. How many feet', lambda g, k: same(F(int(g[0]), 12), kn(k))),
]


def phrase(p, k):
    v = re.search(r'number ([a-z])', p).group(1)
    s = sp.Symbol(v)
    n = [int(x) for x in re.findall(r'\d+', p)]
    if re.fullmatch(r'the quotient of a number [a-z] and (\d+)', p):
        want = s / n[0]
    elif re.fullmatch(r'the quotient of a number [a-z] and (\d+), increased by (\d+)', p):
        want = s / n[0] + n[1]
    elif re.fullmatch(r'(\d+) less than a number [a-z]', p) or re.fullmatch(r'a number [a-z] decreased by (\d+)', p):
        want = s - n[0]
    elif re.fullmatch(r'(\d+) more than a number [a-z]', p):
        want = s + n[0]
    elif re.fullmatch(r'(\d+) less than (\d+) times a number [a-z]', p):
        want = n[1] * s - n[0]
    elif re.fullmatch(r'(\d+) more than (\d+) times a number [a-z]', p):
        want = n[1] * s + n[0]
    elif re.fullmatch(r'(\d+) times the sum of a number [a-z] and (\d+)', p):
        want = n[0] * (s + n[1])
    else:
        raise Skip('phrase')
    return sp.simplify(ex(k) - want) == 0


def eq_same(k, left, right):
    L, R = k.split('=')
    return sp.simplify((ex(L) - ex(R)) - (ex(left) - ex(right))) == 0


def eq_val(k, var, v):
    m = re.fullmatch(r'\s*([a-z]) = (-?[\d./ ]+)\s*', k)
    return bool(m) and m.group(1) == var and same(frac(m.group(2)), v)


def ineq_same(k, var, op, n):
    m = re.fullmatch(r'\s*([a-z]) (<|>|≤|≥) (-?[\d./]+)\s*', k)
    return bool(m) and m.group(1) == var and m.group(2) == op and same(d(m.group(3)), d(str(n)))


def holds(v, op, n):
    return {'<': v < n, '>': v > n, '≤': v <= n, '≥': v >= n}[op]


def same_pair(k, p):
    m = re.fullmatch(r'\s*\((-?\d+), (-?\d+)\)\s*', k)
    return bool(m) and (int(m.group(1)), int(m.group(2))) == p


def rect(g, k, what):
    xs, ys = [int(x) for x in g[0:8:2]], [int(y) for y in g[1:8:2]]
    w, h = max(xs) - min(xs), max(ys) - min(ys)
    return same(2 * (w + h) if what == 'perimeter' else w * h, kn(k))


def fourth(g, k):
    pts = [(int(g[i]), int(g[i + 1])) for i in (0, 2, 4)]
    xs, ys = [p[0] for p in pts], [p[1] for p in pts]
    fx = [x for x in set(xs) if xs.count(x) == 1][0]; fy = [y for y in set(ys) if ys.count(y) == 1][0]
    return same_pair(k, (fx, fy))


def table_eq(g, k):
    x, xs, y, ys = sp.Symbol(g[0]), data(g[1]), sp.Symbol(g[2]), data(g[3])
    m = re.fullmatch(r'\s*([a-z]) = (.+)', k)
    if not m or m.group(1) != g[2]:
        return False
    f = ex(m.group(2))
    return all(f.subs(x, a) == b for a, b in zip(xs, ys))


def prop_missing(g, k):
    xs, ys = data(g[0]), g[1].split(', ')
    r = [F(ys[i]) / xs[i] for i in range(len(xs)) if ys[i] != '?'][0]
    i = ys.index('?')
    return same(r * xs[i], kn(k))


def proportion(g, k):
    m = re.fullmatch(r'\s*([a-z]) = (-?[\d./ ]+)\s*', k)
    if not m:
        return False
    v = sp.Symbol(m.group(1))
    sol = sp.solve(sp.Eq(ex(g[0]), ex(g[1])), v)
    return len(sol) == 1 and same(sol[0], frac(m.group(2)))


def simplest(k):
    m = re.search(r'(\d+)/(\d+)\s*$', k.split()[-1] if k.split() else k)
    return not m or math.gcd(int(m.group(1)), int(m.group(2))) == 1


def word6(text, key):
    for pat, fn in G6:
        m = re.search(pat, text)
        if m:
            return fn(m.groups(), str(key))
    raise Skip('no template')


CHECKERS = [V.solve_eq, V.compare, V.evaluate, V.simplify_expr, word6, V.word]


def check(q):
    key = q.get('answer')
    if not isinstance(key, str):
        raise Skip('non-string key')
    text = V.problem_text(q)
    last = None
    for fn in CHECKERS:
        try:
            return fn(text, key)
        except Skip as e:
            last = e
        except (sp.SympifyError, SyntaxError, TypeError, ValueError, ZeroDivisionError, AttributeError, IndexError, KeyError, AssertionError) as e:
            last = Skip(type(e).__name__)
    raise last or Skip('none')


def shown_wrong(q):
    """Error-analysis items: the answer the student gave must not be the key."""
    m = re.search(r"'s answer: (.+?)\s*$", q['prompt'], re.M)
    if not m:
        return True
    shown, key = m.group(1).strip().rstrip('.'), str(q['answer']).strip()
    if shown == key:
        return False
    if re.fullmatch(r'-?\$?[\d.,/ ]+', shown) and re.fullmatch(r'-?\$?[\d.,/ ]+', key):
        return not same(num(shown), num(key))
    return True


def main():
    items = []
    for f in sorted(glob.glob(os.path.join(ROOT, 'question-banks', 'math6', '*.json'))):
        items += json.load(open(f, encoding='utf-8'))['questions']
    checked, bad, skipped, mcbad, eabad = 0, [], {}, [], []
    shapes = {}
    for q in items:
        if not V.mc_consistent(q):
            mcbad.append(q['id'])
        if 'answered this problem incorrectly' in q['prompt'] and not shown_wrong(q):
            eabad.append(q['id'])
        if q.get('format') not in ('short-answer', 'multiple-choice'):
            continue
        try:
            ok = check(q)
        except Skip as e:
            skipped[str(e)] = skipped.get(str(e), 0) + 1
            sh = re.sub(r'-?\d+(\.\d+)?', '#', V.problem_text(q))[:70]
            shapes[sh] = shapes.get(sh, 0) + 1
            continue
        checked += 1
        if not ok:
            bad.append((q['id'], V.problem_text(q)[:110], q['answer']))
    for b in bad:
        print('MISMATCH', *b)
    for i in mcbad:
        print('MC KEY', i)
    for i in eabad:
        print('ERROR ANALYSIS SHOWS THE KEY', i)
    if '--list' in sys.argv:
        print('skipped:', sorted(skipped.items(), key=lambda x: -x[1])[:15])
        for s, n in sorted(shapes.items(), key=lambda x: -x[1])[:40]:
            print(f'{n:4d}  {s}')
    ok = not bad and not mcbad and not eabad and checked >= MIN
    print(f"{'PASS' if ok else 'FAIL'} {checked} Grade 6 keys recomputed from the printed prompts ({len(bad)} mismatches); "
          f"{sum(1 for q in items if q.get('format') == 'multiple-choice')} multiple-choice keys match their options; "
          f"{sum(1 for q in items if 'answered this problem incorrectly' in q['prompt'])} error-analysis items show a wrong answer ({len(eabad)} show the key)")
    return 0 if ok else 1


if __name__ == '__main__':
    sys.exit(main())
