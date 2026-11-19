"""Grade 6 audit #4 (2026-11-19): recompute the keys of the 106 new Honors items from their printed prompts, independently
of honors.py (which builds the prompts). Every item must be matched by one rule. Usage: python3 verify_honors.py"""
import math, os, re, sys
from fractions import Fraction as F
sys.path.insert(0, os.path.dirname(__file__))
import lib


def fr(s):
    s = s.replace('−', '-').replace(',', '').replace('$', '').strip()
    m = re.fullmatch(r'(-?)(\d+) (\d+)/(\d+)', s)
    if m:
        v = int(m.group(2)) + F(int(m.group(3)), int(m.group(4)))
        return -v if m.group(1) else v
    return F(s)


def ns(s):
    return [fr(x) for x in re.findall(r'-?\d+ \d+/\d+|-?\d[\d,]*(?:\.\d+)?(?:/\d+)?', s.replace('−', '-'))]


def med(xs):
    xs = sorted(xs); n = len(xs)
    return xs[n // 2] if n % 2 else (xs[n // 2 - 1] + xs[n // 2]) / 2


def mad(xs):
    m = F(sum(xs), len(xs)); return sum(abs(x - m) for x in xs) / len(xs)


def cents(x):
    return F(math.floor(x * 100 + F(1, 2)), 100)


def ceil(x):
    return -(-x.numerator // x.denominator)


def lst(s):
    return [fr(x) for x in s.split(', ')]


RULES = [
    (r'ratio of boys to girls is (\d+) : (\d+)\. There are (\d+) members', lambda g: F((int(g[0]) - int(g[1])) * int(g[2]), int(g[0]) + int(g[1]))),
    (r'Store A sells (\d+) pounds of apples for \$(\d+(?:\.\d+)?)\. Store B sells (\d+) pounds for \$(\d+(?:\.\d+)?)\. \w+ needs (\d+) pounds', lambda g: abs(fr(g[1]) / int(g[0]) - fr(g[3]) / int(g[2])) * int(g[4])),
    (r'mixes (\d+) cups of juice with (\d+) cups of sparkling water\. \w+ has (\d+) cups of juice', lambda g: fr(g[2]) + fr(g[2]) * int(g[1]) / int(g[0])),
    (r'Mix A uses (\d+) cups of blue paint for every (\d+) cups of white\. Mix B has (\d+) cups of blue and (\d+) cups of white', lambda g: F(int(g[0]) * int(g[3]), int(g[1])) - int(g[2])),
    (r'1 cm represents (\d+) km\. A road goes (\d+) cm .* and then (\d+) cm .* averages (\d+) km per hour', lambda g: F((int(g[1]) + int(g[2])) * int(g[0]), int(g[3]))),
    (r'A school has (\d+) students\. (\d+)% ride the bus\. Of the students who do not ride the bus, (\d+)% walk', lambda g: (int(g[0]) - F(int(g[0]) * int(g[1]), 100)) * int(g[2]) / 100),
    (r'won (\d+) of its first (\d+) games and (\d+) of its last (\d+) games', lambda g: F((int(g[0]) + int(g[2])) * 100, int(g[1]) + int(g[3]))),
    (r'uses ([\d /]+) cups of broth per batch\. \w+ makes (\d+) batches', lambda g: fr(g[0]) * int(g[1]) / 4),
    (r'path is ([\d /]+) mile long\. A marker stands at the start and then every ([\d/]+) mile', lambda g: fr(g[0]) / fr(g[1]) + 1),
    (r'has (\d+) cups of flour\. Each loaf uses ([\d/]+) cup\. After baking (\d+) loaves', lambda g: (int(g[0]) - int(g[2]) * fr(g[1])) / fr(g[1])),
    (r'A board is ([\d /]+) feet long\. \w+ cuts as many ([\d /]+)-foot shelves', lambda g: fr(g[0]) - (fr(g[0]) // fr(g[1])) * fr(g[1])),
    (r'(\d+) students are going on a field trip\. Each bus holds (\d+) students and costs \$(\d+)', lambda g: ceil(F(int(g[0]), int(g[1]))) * int(g[2])),
    (r'buys a book for \$(\d+(?:\.\d+)?), a game for \$(\d+(?:\.\d+)?) and a snack for \$(\d+(?:\.\d+)?), and pays with a \$(\d+) bill', lambda g: int(g[3]) - fr(g[0]) - fr(g[1]) - fr(g[2])),
    (r'Gas costs \$(\d+(?:\.\d+)?) per gallon\. A car goes (\d+) miles per gallon\. How much does the gas cost for a (\d+)-mile trip', lambda g: cents(fr(g[0]) * F(int(g[2]), int(g[1])))),
    (r'packs of (\d+) for \$(\d+(?:\.\d+)?)\. Buns come in packs of (\d+) for \$(\d+(?:\.\d+)?)', lambda g: (lambda L: L // int(g[0]) * fr(g[1]) + L // int(g[2]) * fr(g[3]))(math.lcm(int(g[0]), int(g[2])))),
    (r'buys (\d+) T-shirts at \$(\d+(?:\.\d+)?) each and \d+ hats at \$(\d+(?:\.\d+)?) each', lambda g: int(g[0]) * (fr(g[1]) + fr(g[2]))),
    (r'A diver is (\d+) m below sea level\. She rises (\d+) m and then dives down (\d+) m', lambda g: -int(g[0]) + int(g[1]) - int(g[2])),
    (r'temperature was −(\d+)°F\. By noon it was (\d+)°F, and by night it fell (\d+) degrees', lambda g: int(g[1]) - int(g[2]) + int(g[0])),
    (r'low temperatures for four days were (.+?)\. How many degrees warmer', lambda g: max(ns(g[0])) - min(ns(g[0]))),
    (r"balance is \$(-\d+) and Ben's is \$(\d+)\. What is the least whole number", lambda g: int(g[1]) - int(g[0]) + 1),
    (r'submarine is at −(\d+) m and a fish is at −(\d+) m', lambda g: int(g[0]) - int(g[1])),
    (r'owes \$(\d+) \(balance −\$\d+\) and Ben owes \$(\d+) \(balance −\$\d+\)\. \w+ then borrows \$(\d+) more', lambda g: abs(int(g[0]) + int(g[2]) - int(g[1]))),
    (r'Point P\((-?\d+), (-?\d+)\) is reflected across the x-axis to point Q\. How far apart', lambda g: 2 * abs(int(g[1]))),
    (r'robot starts at \((-?\d+), (-?\d+)\)\. It moves (\d+) units left and then (\d+) units down', lambda g: (int(g[0]) - int(g[2]), int(g[1]) - int(g[3]))),
    (r'walks from \((-?\d+), (-?\d+)\) to \((-?\d+), (-?\d+)\) and then to \((-?\d+), (-?\d+)\)', lambda g: abs(int(g[3]) - int(g[1])) + abs(int(g[4]) - int(g[2]))),
    (r'starts with (\d+) cells and doubles every hour\. .* after (\d+) hours', lambda g: int(g[0]) * 2 ** int(g[1])),
    (r'Plan A costs (\d+) \+ (\d+)g dollars and Plan B costs (\d+) \+ (\d+)g dollars .* for (\d+) gigabytes', lambda g: abs(int(g[0]) + int(g[1]) * int(g[4]) - int(g[2]) - int(g[3]) * int(g[4]))),
    (r'buys (\d+) boxes of (\d+) markers, gives away (\d+) markers, and shares the rest equally among (\d+) friends', lambda g: F(int(g[0]) * int(g[1]) - int(g[2]), int(g[3]))),
    (r'each (\d+) m wide\. One is \(x \+ (\d+)\) m long and the other is \(x \+ (\d+)\) m long\. .* when x = (\d+)', lambda g: int(g[0]) * (2 * int(g[3]) + int(g[1]) + int(g[2]))),
    (r'a \$(\d+) sign-up fee plus \$(\d+) per class\. \w+ paid \$(\d+) in all', lambda g: F(int(g[2]) - int(g[0]), int(g[1]))),
    (r'had \$(\d+)\. \w+ spent \$(\d+) on lunch and bought (\d+) books .* Now \w+ has \$(\d+)', lambda g: F(int(g[0]) - int(g[1]) - int(g[3]), int(g[2]))),
    (r'charges c = (\d+) \+ (\d+)h dollars for h hours\. .* a (\d+)-hour job cost than a (\d+)-hour job', lambda g: int(g[1]) * (int(g[2]) - int(g[3]))),
    (r'carry at most ([\d,]+) pounds\. \d+ people with a total weight of ([\d,]+) pounds get on\. .* greatest number of (\d+)-pound boxes', lambda g: (fr(g[0]) - fr(g[1])) // int(g[2])),
    (r'wants at least \$(\d+) for a bike\. \w+ has \$(\d+) and earns \$(\d+) per hour', lambda g: ceil(F(int(g[0]) - int(g[1]), int(g[2])))),
    (r'How many whole numbers from 1 to 20 are solutions of (\d+)x \+ (\d+) > (\d+)\?', lambda g: sum(1 for x in range(1, 21) if int(g[0]) * x + int(g[1]) > int(g[2]))),
    (r'temperature t \(°C\) with −(\d+) < t ≤ (\d+)', lambda g: sum(1 for x in range(-50, 51) if -int(g[0]) < x <= int(g[1]))),
    (r'tickets cost \$(\d+) each, plus one \$(\d+) service fee .* at most \$(\d+)', lambda g: (int(g[2]) - int(g[1])) // int(g[0])),
    (r'trapezoid with parallel sides (\d+) ft and (\d+) ft and height (\d+) ft\. One bag of seed covers (\d+) square feet', lambda g: ceil(F((int(g[0]) + int(g[1])) * int(g[2]), 2 * int(g[3])))),
    (r'right triangle with legs (\d+) ft and (\d+) ft\. The fabric costs \$(\d+(?:\.\d+)?) per square foot\. .* 2 sails', lambda g: int(g[0]) * int(g[1]) * fr(g[2])),
    (r'makes (\d+) triangular flags, each with a base of (\d+) in\. and a height of (\d+) in\.', lambda g: F(int(g[0]) * int(g[1]) * int(g[2]), 2)),
    (r'a (\d+) ft by (\d+) ft rectangle with a (\d+) ft by (\d+) ft corner cut out\. Carpet costs \$(\d+(?:\.\d+)?)', lambda g: (int(g[0]) * int(g[1]) - int(g[2]) * int(g[3])) * fr(g[4])),
    (r'fish tank is ([\d /]+) in\. long, (\d+) in\. wide and (\d+) in\. tall\. It is filled with water to 3/4', lambda g: fr(g[0]) * int(g[1]) * int(g[2]) * F(3, 4)),
    (r'corners \((-?\d+), (-?\d+)\), \((-?\d+), -?\d+\), \(-?\d+, (-?\d+)\) and .* Each unit is 10 m\. Fencing costs \$(\d+) per meter', lambda g: 2 * ((int(g[2]) - int(g[0])) + (int(g[3]) - int(g[1]))) * 10 * int(g[4])),
    (r'Rectangle 1 has corners \(0, 0\), \((\d+), 0\), \(\d+, (\d+)\) and .* Rectangle 2 has corners \(\d+, 0\), \((\d+), 0\), \(\d+, (\d+)\)', lambda g: int(g[0]) * int(g[1]) + (int(g[2]) - int(g[0])) * int(g[3])),
    (r'box (\d+) in\. long, (\d+) in\. wide and (\d+) in\. tall\. One bottle of paint covers (\d+) square inches', lambda g: (lambda l, w, h: ceil(F(2 * (l * w + l * h + w * h), int(g[3]))))(int(g[0]), int(g[1]), int(g[2]))),
    (r'collected 5 responses: ([\d, ]+)\. One more student answered (\d+)\. What is the mean of all 6', lambda g: F(sum(lst(g[0])) + int(g[1]), 6)),
    (r'minimum (\d+), lower quartile (\d+), median \d+, upper quartile (\d+) and maximum (\d+)\. How much greater is the range than the interquartile range', lambda g: int(g[3]) - int(g[0]) - (int(g[2]) - int(g[1]))),
    (r"five test scores are ([\d, ]+)\. The teacher drops the lowest score", lambda g: (lambda xs: F(sum(xs) - min(xs), 4))(lst(g[0]))),
    (r'^Data: ([\d, ]+)\. How much greater is the range than the interquartile range', lambda g: (lambda xs: (max(xs) - min(xs)) - (med(sorted(xs)[len(xs) // 2 + len(xs) % 2:]) - med(sorted(xs)[:len(xs) // 2])))(lst(g[0]))),
    (r'Class A scored ([\d, ]+) and Class B scored ([\d, ]+) on a quiz\. How much greater is the mean absolute deviation of Class B', lambda g: mad(lst(g[1])) - mad(lst(g[0]))),
    (r'Team A: ([\d, ]+)\. Team B: ([\d, ]+)\. How much greater is the larger median', lambda g: abs(med(lst(g[0])) - med(lst(g[1])))),
    (r'pets owned by 7 families is ([\d, ]+)\. .* How much greater is the mean than the median', lambda g: (lambda xs: F(math.floor((F(sum(xs), 7) - med(xs)) * 10 + F(1, 2)), 10))(lst(g[0]))),
    (r'^Data: ([\d, ]+)\. The value (\d+) is an outlier\. By how much does the mean decrease', lambda g: (lambda xs: F(sum(xs), len(xs)) - F(sum(xs) - int(g[1]), len(xs) - 1))(lst(g[0]))),
]


def main():
    bad = n = 0
    for u, q in lib.items(lib.load()):
        if not re.search(r'-honors-h\d{2}$', q['id']):
            continue
        n += 1
        hits = [(p, fn) for p, fn in RULES if re.search(p, q['prompt'])]
        if len(hits) != 1:
            print('RULES', len(hits), q['id'], q['prompt'][:90]); bad += 1; continue
        want = hits[0][1](re.search(hits[0][0], q['prompt']).groups())
        a = q['answer']
        if isinstance(want, tuple):
            ok = a == f'({want[0]}, {want[1]})'
        else:
            ok = abs(float(fr(a.rstrip('%'))) - float(want)) < 0.006 if re.search(r'\.\d', a) else fr(a.rstrip('%')) == want
        if not ok:
            print('MISMATCH', q['id'], q['prompt'][:100], a, want); bad += 1
    print(('FAIL' if bad or n != 106 else 'PASS'), f'{n} Grade 6 Honors keys recomputed from their prompts ({bad} problems)')
    sys.exit(1 if bad or n != 106 else 0)


if __name__ == '__main__':
    main()
