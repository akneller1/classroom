"""Whole-site audit #9 (2026-11-20): recompute the keys of the items levels.py rewrote, from their printed prompts and
independently of levels.py. Honors rewrites use verify_honors.py's rules; Standard rewrites use the rules below.
Every rewritten item must match exactly one rule. Usage: python3 verify_levels.py"""
import math, os, re, sys
from fractions import Fraction as F
sys.path.insert(0, os.path.dirname(__file__))
import lib
from verify_honors import RULES as HONORS, fr, ns, med, mad, lst

I = lambda s: int(s.replace(',', ''))
P = r'(-?\d+)'


def cents(x):
    return F(math.floor(x * 100 + F(1, 2)), 100)


RULES = [
    (r'ratio of red marbles to blue marbles is (\d+) : (\d+)\. There are (\d+) marbles in all', lambda g: F(I(g[2]) * I(g[1]), I(g[0]) + I(g[1]))),
    (r'earns \$(\d+) for (\d+) hours of work\. At the same rate, how many dollars does \w+ earn in (\d+) hours', lambda g: F(I(g[0]) * I(g[2]), I(g[1]))),
    (r'uses (\d+) scoops of mix for every (\d+) cups of water\. \w+ has (\d+) cups of water and (\d+) scoops', lambda g: I(g[3]) - F(I(g[2]), I(g[1])) * I(g[0])),
    (r'Store A sells (\d+) ounces of cereal for \$([\d.]+)\. Store B sells (\d+) ounces for \$([\d.]+)\. How many cents less', lambda g: abs(fr(g[1]) / I(g[0]) - fr(g[3]) / I(g[2])) * 100),
    (r'On a map, (\d+) inch(?:es)? represents? (\d+) miles\. Two towns are ([\d /]+) inches apart .* at (\d+) miles per hour', lambda g: fr(g[2]) * I(g[1]) / I(g[0]) / I(g[3])),
    (r'^(\d+)% of the (\d+) students at a school ride the bus\. How many students do not', lambda g: I(g[1]) - F(I(g[0]) * I(g[1]), 100)),
    (r'(\d+) out of (\d+) students chose pizza .* What percent of the students did not', lambda g: 100 - F(I(g[0]) * 100, I(g[1]))),
    (r'A ribbon is (\d+) feet long\. \w+ cuts it into pieces that are each (\d+) inches long', lambda g: F(I(g[0]) * 12, I(g[1]))),
    (r'Each jug holds (\d+)/(\d+) gallon of juice\. Each glass holds (\d+)/(\d+) gallon\. How many glasses can be filled from (\d+) full jugs', lambda g: I(g[4]) * F(I(g[0]), I(g[1])) / F(I(g[2]), I(g[3]))),
    (r'has (\d+) cups of flour\. Each batch of muffins needs (\d+)/(\d+) cup\. After making as many full batches', lambda g: (lambda w, c: w - (w // c) * c)(F(I(g[0])), F(I(g[1]), I(g[2])))),
    (r'A board is ([\d /]+) feet long\. \w+ cuts as many pieces as possible that are each ([\d /]+) feet long\. How many full pieces', lambda g: fr(g[0]) // fr(g[1])),
    (r'^(\d+) students and (\d+) teachers are going on a field trip\. Each bus holds (\d+) people', lambda g: -(-(I(g[0]) + I(g[1])) // I(g[2]))),
    (r'has \$([\d,.]+)\. \w+ buys a book for \$([\d.]+) and a backpack for \$([\d.]+)\. How much money', lambda g: fr(g[0]) - fr(g[1]) - fr(g[2])),
    (r'Gas costs \$([\d.]+) per gallon\. \w+ buys ([\d.]+) gallons and pays with a \$(\d+) bill', lambda g: I(g[2]) - cents(fr(g[0]) * fr(g[1]))),
    (r'Hot dogs come in packs of (\d+) and buns come in packs of (\d+)\. .* least number of packs of buns', lambda g: F(math.lcm(I(g[0]), I(g[1])), I(g[1]))),
    (r'Each of (\d+) students buys a notebook for \$([\d.]+) and a pen for \$([\d.]+)\.', lambda g: I(g[0]) * (fr(g[1]) + fr(g[2]))),
    (r'A diver is (\d+) feet below sea level\. She swims up (\d+) feet\.', lambda g: -I(g[0]) + I(g[1])),
    (r'point A is at (-\d+)\. Point B is (\d+) units to the right of A\. Point C is the opposite of B', lambda g: -(I(g[0]) + I(g[1]))),
    (r'low temperatures \(°F\) for five days were (.+?)\. How many degrees warmer', lambda g: max(ns(g[0])) - min(ns(g[0]))),
    (r'The low temperature was (-?\d+)°C in Town A and (-?\d+)°C in Town B\. Town C was (\d+) degrees colder than the warmer', lambda g: max(I(g[0]), I(g[1])) - I(g[2])),
    (r'^Evaluate: \|(-?\d+)\| \+ \|(-?\d+)\| − \|(-?\d+)\|$', lambda g: abs(I(g[0])) + abs(I(g[1])) - abs(I(g[2]))),
    (r'Three account balances are -\$(\d+), -\$(\d+) and \$(\d+)\. How many more dollars', lambda g: abs(I(g[0]) - I(g[1]))),
    (r'Point \(' + P + r', ' + P + r'\) is reflected across the x-axis, and then the image is reflected across the y-axis', lambda g: (-I(g[0]), -I(g[1]))),
    (r'A robot starts at \(' + P + r', ' + P + r'\)\. It moves (\d+) units left and then (\d+) units up\.', lambda g: (I(g[0]) - I(g[2]), I(g[1]) + I(g[3]))),
    (r'A rectangle has vertices \(' + P + ', ' + P + r'\), \(' + P + ', ' + P + r'\), \(' + P + ', ' + P + r'\) and \(-?\d+, -?\d+\)\. What is its area', lambda g: abs(I(g[2]) - I(g[0])) * abs(I(g[5]) - I(g[3]))),
    (r'^Evaluate: (\d+)² \+ (\d+)³$', lambda g: I(g[0]) ** 2 + I(g[1]) ** 3),
    (r'tickets cost \$(\d+) each, plus a \$(\d+) fee for the whole order\. .* cost in dollars of (\d+) tickets', lambda g: I(g[0]) * I(g[2]) + I(g[1])),
    (r'^Evaluate: \((\d+) \+ (\d+)\)² ÷ (\d+) − (\d+)$', lambda g: F((I(g[0]) + I(g[1])) ** 2, I(g[2])) - I(g[3])),
    (r'^Simplify: (\d+)\(x \+ (\d+)\) \+ (\d+)x$', lambda g: ('expr', I(g[0]) + I(g[2]), I(g[0]) * I(g[1]))),
    (r'Which value from the set \{(.+?)\} makes (\d+)x \+ (\d+) = (\d+) true', lambda g: [v for v in ns(g[0]) if I(g[1]) * v + I(g[2]) == I(g[3])][0]),
    (r'^Solve (\d+)x = (\d+)\. Then find the value of x \+ (\d+)\.', lambda g: F(I(g[1]), I(g[0])) + I(g[2])),
    (r'hours worked \(h\): 1, 2, 3 and pay in dollars \(p\): (\d+), \d+, \d+\. .* pay in dollars for (\d+) hours', lambda g: I(g[0]) * I(g[1])),
    (r'must be at least (\d+) inches tall\. \w+ is (\d+) inches tall\.', lambda g: I(g[0]) - I(g[1])),
    (r'^Solve (\d+)x ≤ (\d+)\. What is the greatest whole number', lambda g: I(g[1]) // I(g[0])),
    (r'How many whole numbers from 0 to (\d+) are solutions of x > (\d+)\?', lambda g: sum(1 for x in range(0, I(g[0]) + 1) if x > I(g[1]))),
    (r'has (an open|a closed) circle at (-?\d+) and an arrow pointing right\. What is the least integer', lambda g: I(g[1]) + (1 if g[0] == 'an open' else 0)),
    (r'can carry at most (\d+) pounds\. Each box weighs (\d+) pounds\.', lambda g: I(g[0]) // I(g[1])),
    (r'trapezoid has bases (\d+) cm and (\d+) cm and height (\d+) cm\. A parallelogram with base (\d+) cm', lambda g: F((I(g[0]) + I(g[1])) * I(g[2]), 2 * I(g[3]))),
    (r'Right triangle P has legs (\d+) ft and (\d+) ft\. Right triangle Q has legs (\d+) ft and (\d+) ft\.', lambda g: abs(F(I(g[0]) * I(g[1]) - I(g[2]) * I(g[3]), 2))),
    (r'triangular sail has a base of (\d+) ft and a height of (\d+) ft\. The fabric costs \$(\d+) per square foot', lambda g: F(I(g[0]) * I(g[1]) * I(g[2]), 2)),
    (r'garden is a (\d+) m by (\d+) m rectangle .* legs (\d+) m and (\d+) m\.', lambda g: I(g[0]) * I(g[1]) - F(I(g[2]) * I(g[3]), 2)),
    (r'fish tank is (\d+) in\. long, (\d+) in\. wide and (\d+) in\. tall\. It is filled with water to a depth of (\d+) in\.', lambda g: I(g[0]) * I(g[1]) * (I(g[2]) - I(g[3]))),
    (r'Three vertices of a rectangle are \(' + P + ', ' + P + r'\), \(' + P + ', ' + P + r'\) and \(' + P + ', ' + P + r'\)\. Find the fourth vertex, and then the perimeter',
     lambda g: 2 * (abs(I(g[2]) - I(g[0])) + abs(I(g[5]) - I(g[3])))),
    (r'A rectangle has vertices \(0, 0\), \((\d+), 0\), \(\d+, (\d+)\) and \(0, \d+\)\. A square has the same perimeter', lambda g: F(I(g[0]) + I(g[1]), 2) ** 2),
    (r'box with no top is (\d+) in\. long, (\d+) in\. wide and (\d+) in\. tall', lambda g: I(g[0]) * I(g[1]) + 2 * I(g[2]) * (I(g[0]) + I(g[1]))),
    (r'^Data: ([\d, ]+)\. A histogram uses the interval (\d+)–(\d+)\. What percent', lambda g: (lambda xs: F(sum(1 for x in xs if I(g[1]) <= x <= I(g[2])) * 100, len(xs)))(lst(g[0]))),
    (r"first four quiz scores are ([\d, ]+)\. \w+ scores (\d+) on the fifth quiz", lambda g: F(sum(lst(g[0])) + I(g[1]), 5)),
    (r'^Data: ([\d, ]+)\. How much greater is the range than the interquartile range\?$', lambda g: (lambda xs: (max(xs) - min(xs)) - (med(xs[4:]) - med(xs[:4])))(sorted(lst(g[0])))),
    (r'^Data set A: ([\d, ]+)\. Data set B: ([\d, ]+)\. How much greater is the larger mean absolute deviation', lambda g: abs(mad(lst(g[0])) - mad(lst(g[1])))),
    (r'Team A: ([\d, ]+); Team B: ([\d, ]+)\. How much greater is the larger range', lambda g: abs((max(lst(g[0])) - min(lst(g[0]))) - (max(lst(g[1])) - min(lst(g[1]))))),
    (r'^Data: ([\d, ]+)\. The data are skewed right\. How much greater is the mean than the median', lambda g: (lambda xs: F(sum(xs), len(xs)) - med(xs))(lst(g[0]))),
    (r'^Data: ([\d, ]+)\. The value (\d+) is an outlier\. By how much does the median change', lambda g: (lambda xs: abs(med(xs) - med([x for x in xs if x != I(g[1])])))(lst(g[0]))),
]


def check(a, want):
    a = a.replace('−', '-')
    if isinstance(want, tuple) and want and want[0] == 'expr':
        return a == f'{want[1]}x + {want[2]}'
    if isinstance(want, tuple):
        return a == f'({want[0]}, {want[1]})'
    a = a.rstrip('%')
    return abs(float(fr(a)) - float(want)) < 0.006 if re.search(r'\.\d', a) else fr(a) == want


def main():
    bad = n = 0
    for u, q in lib.items(lib.load()):
        if 'audit #9' not in q['sourceNotes']:
            continue
        n += 1
        rules = HONORS if q['level'] == 'honors' else RULES
        hits = [(p, fn) for p, fn in rules if re.search(p, q['prompt'])]
        if len(hits) != 1:
            print('RULES', len(hits), q['id'], q['prompt'][:100]); bad += 1; continue
        want = hits[0][1](re.search(hits[0][0], q['prompt']).groups())
        if not check(q['answer'], want):
            print('MISMATCH', q['id'], q['prompt'][:100], q['answer'], want); bad += 1
        if q['format'] == 'multiple-choice':
            c = [o['text'] for o in q['options'] if o['correct']]
            if c != [q['answer']] or len({o['text'] for o in q['options']}) != 4:
                print('OPTIONS', q['id'], q['options']); bad += 1
            elif any(check(o['text'], want) for o in q['options'] if not o['correct']):
                print('DISTRACTOR EQUALS KEY', q['id']); bad += 1
    print(('FAIL' if bad or n < 300 else 'PASS'), f'{n} rewritten Grade 6 keys recomputed from their prompts ({bad} problems)')
    sys.exit(1 if bad or n < 300 else 0)


if __name__ == '__main__':
    main()
