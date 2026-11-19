"""Grade 6 audit (2026-11-19): item fixes.
#3  13 error-analysis items showed a "wrong" student answer equal to the key. Each now shows the answer its stated mistake
    really produces (numbers changed where the mistake and the correct method agree).
#2  Keys the new checker found wrong: 10 ÷ 3/8 bags of trail mix is 26 full bags, not 26 2/3; five bead-ratio items asked
    "how many more blue beads than red" when there are fewer blue beads.
#20 Unrealistic contexts: cars at 4-24 mph get car-like numbers or become a hiker or cyclist; cars at 2-14 miles per gallon
    become boats; "at least 17 years old to vote" becomes "to enter the contest"; a plant growing 17 feet a year is bamboo;
    juice boxes at $2-$9 each become smoothies; $3-$4 shirts become pairs of socks; a jacket that cost $51 before a $40
    discount becomes a $15 T-shirt with a $4 discount.
Idempotent: every edit checks the item's current text first."""
import os, re, sys
sys.path.insert(0, os.path.dirname(__file__))
import lib


def ea(prompt, answer, steps):
    return {'prompt': prompt, 'answer': answer, 'solutionSteps': steps}


FIX = {
 'm6-dd-s03-cp2-016': ea("Priya answered this problem incorrectly.\nFind the mode of the data: 20, 1, 23, 15, 16, 3, 22, 20\nPriya's answer: 18\nIdentify the mistake and give the correct answer.", '20',
    ['Mistake: Gave the median (the mean of the middle values 16 and 20).', 'Order the data: 1, 3, 15, 16, 20, 20, 22, 23.', 'Find the value that occurs most often.', 'The mode is 20.', 'The correct answer is 20, not 18.']),
 'm6-dd-s06-cp1-014': ea("Ben answered this problem incorrectly.\nFind the mode of the data: 3.1, 19.4, 3.3, 3.4, 13.4, 6.4, 3.4\nBen's answer: 19.4\nIdentify the mistake and give the correct answer.", '3.4',
    ['Mistake: Gave the greatest value.', 'Order the data: 3.1, 3.3, 3.4, 3.4, 6.4, 13.4, 19.4.', 'Find the value that occurs most often.', 'The mode is 3.4.', 'The correct answer is 3.4, not 19.4.']),
 'm6-exq-s03-cp2-016': ea("Quinn answered this problem incorrectly.\nEvaluate: 5 + 14 × 8\nQuinn's answer: 152\nIdentify the mistake and give the correct answer.", '117',
    ['Mistake: Worked left to right without following the order of operations: (5 + 14) × 8 = 152.', 'Multiply before adding: 14 × 8 = 112.', 'Then add: 5 + 112 = 117.', 'The correct answer is 117, not 152.']),
 'm6-exq-s07-cp2-014': ea("Rosa answered this problem incorrectly.\nA table shows items (n): 2, 5, 9 and dollars (c): 24, 60, 108. Write an equation for c in terms of n.\nRosa's answer: c = 24n\nIdentify the mistake and give the correct answer.", 'c = 12n',
    ['Mistake: Used the first y-value as the rate.', 'Look for how the dependent variable changes as the independent variable changes.', 'Each c-value is 12 times its n-value: 24 ÷ 2 = 12, 60 ÷ 5 = 12, 108 ÷ 9 = 12.', 'c = 12n.', 'The correct answer is c = 12n, not c = 24n.']),
 'm6-exq-s07-cp1-016': ea("Quinn answered this problem incorrectly.\nA table shows items (n): 3, 7, 9 and dollars (c): 18, 42, 54. Write an equation for c in terms of n.\nQuinn's answer: c = 18n\nIdentify the mistake and give the correct answer.", 'c = 6n',
    ['Mistake: Used the first y-value as the rate.', 'Look for how the dependent variable changes as the independent variable changes.', 'Each c-value is 6 times its n-value: 18 ÷ 3 = 6, 42 ÷ 7 = 6, 54 ÷ 9 = 6.', 'c = 6n.', 'The correct answer is c = 6n, not c = 18n.']),
 'm6-fdo-s01-cp2-014': ea("Ava answered this problem incorrectly.\nDivide. Write the answer in simplest form: 3/4 ÷ 1/2\nAva's answer: 3/8\nIdentify the mistake and give the correct answer.", '1 1/2',
    ['Mistake: Multiplied by 1/2 instead of by its reciprocal.', 'Keep 3/4, change ÷ to ×, and use the reciprocal of 1/2: 2.', '3/4 × 2 = 3/2.', 'Simplify (rename as a mixed number if needed).', 'Answer: 1 1/2.', 'The correct answer is 1 1/2, not 3/8.']),
 'm6-geo-s07-honors-016': ea("Jamal answered this problem incorrectly.\nFind the area of the rectangle with vertices (-4, 0), (4, 0), (4, 3), (-4, 3).\nJamal's answer: 22 units\nIdentify the mistake and give the correct answer.", '24 units²',
    ['Mistake: Found the perimeter instead of the area.', 'Width = 8, height = 3.', 'Area = w × h = 24.', 'The correct answer is 24 units², not 22 units.']),
 'm6-rat-s01-cp2-016': ea("Elena answered this problem incorrectly.\nWhat is the opposite of -6?\nElena's answer: -6\nIdentify the mistake and give the correct answer.", '6',
    ['Mistake: Gave the same number instead of its opposite.', 'Opposites are the same distance from 0 on opposite sides of 0.', 'The opposite of -6 is 6.', 'The correct answer is 6, not -6.']),
 'm6-rat-s01-cp1-016': ea("Vic answered this problem incorrectly.\nWhat is the opposite of -2?\nVic's answer: -2\nIdentify the mistake and give the correct answer.", '2',
    ['Mistake: Gave the same number instead of its opposite.', 'Opposites are the same distance from 0 on opposite sides of 0.', 'The opposite of -2 is 2.', 'The correct answer is 2, not -2.']),
 'm6-rrp-s05-cp2-014': ea("Nia answered this problem incorrectly.\nSolve the proportion: n/7 = 2/14\nNia's answer: n = 49\nIdentify the mistake and give the correct answer.", 'n = 1',
    ['Mistake: Multiplied the wrong pair of terms: 7 × 14 ÷ 2 = 49.', 'Cross products are equal: 14n = 7 × 2.', '14n = 14, so n = 1.', 'Check: 1/7 = 2/14.', 'The correct answer is n = 1, not n = 49.']),
 'm6-rrp-s05-honors-014': ea("Uma answered this problem incorrectly.\nSolve the proportion: n/12 = 18/24\nUma's answer: n = 16\nIdentify the mistake and give the correct answer.", 'n = 9',
    ['Mistake: Multiplied the wrong pair of terms: 12 × 24 ÷ 18 = 16.', 'Cross products are equal: 24n = 12 × 18.', '24n = 216, so n = 9.', 'Check: 9/12 = 3/4 = 18/24.', 'The correct answer is n = 9, not n = 16.']),
 'm6-rrp-s06-cp2-016': ea("Dev answered this problem incorrectly.\n80% of the seats in a theater are filled. If there are 250 in all, how many is that?\nDev's answer: 80\nIdentify the mistake and give the correct answer.", '200',
    ['Mistake: Gave the percent instead of the amount.', '80% = 80 per 100.', '80/100 × 250 = 200.', 'The correct answer is 200, not 80.']),
 'm6-rrp-s06-honors-016': ea("Lena answered this problem incorrectly.\n30% of the songs on a playlist are pop songs. If there are 300 in all, how many is that?\nLena's answer: 210\nIdentify the mistake and give the correct answer.", '90',
    ['Mistake: Found the other part (the 70% that are not pop).', '30% = 30 per 100.', '30/100 × 300 = 90.', 'The correct answer is 90, not 210.']),
 'm6-exq-s06-cp2-002': {'prompt': 'After a $4 discount, a T-shirt costs $11. Write and solve an equation to find c, the original price.', 'answer': 'c = 15',
    'solutionSteps': ['Equation: c - 4 = 11.', 'Use the inverse operation on both sides: add 4.', 'c = 15.'], 'options': ['c = 15', 'c = 11', 'c = 7', 'c = 44']},
}
FIX.update({
 'm6-exq-s06-cp2-003': {'prompt': 'A car travels at a constant speed and covers 84 miles in 2 hours. Write and solve an equation to find s, the speed in miles per hour.', 'answer': 's = 42',
    'solutionSteps': ['Equation: 2s = 84.', 'Use the inverse operation on both sides: divide by 2.', 's = 42.']},
 'm6-exq-s06-cp2-009': {'prompt': 'A car travels at a constant speed and covers 204 miles in 4 hours. Write and solve an equation to find s, the speed in miles per hour.', 'answer': 's = 51',
    'solutionSteps': ['Equation: 4s = 204.', 'Use the inverse operation on both sides: divide by 4.', 's = 51.']},
 'm6-exq-s06-cp1-012': {'prompt': 'A cyclist rides at a constant speed and covers 48 miles in 4 hours. Write and solve an equation to find s, the speed in miles per hour.', 'answer': 's = 12',
    'solutionSteps': ['Equation: 4s = 48.', 'Use the inverse operation on both sides: divide by 4.', 's = 12.']},
})
FIX['m6-fdo-s02-cp1-004'] = {'prompt': 'Carmen has 10 cups of trail mix. Each bag holds 3/8 cup. How many bags can Carmen fill?', 'answer': '26',
    'solutionSteps': ['Keep 10, change ÷ to ×, and use the reciprocal of 3/8: 8/3.', '10 × 8/3 = 80/3 = 26 2/3.', 'Only full bags count, so Carmen can fill 26 bags (with 2/3 of a bag of trail mix left over).', 'Answer: 26.']}
CAR = {'m6-exq-s06-cp1-006': 'A hiker walks'}
# Wording swaps that keep every number and answer: the numbers fit a boat, a cyclist or bamboo, not a car or a voter.
SWAPS = [(r'\bA car travels (\d+) miles in (\d+) hours', lambda m: 25 <= int(m.group(1)) / int(m.group(2)) <= 80, 'A cyclist rides {1} miles in {2} hours'),
         (r'\bA car travels (\d+) miles on (\d+) gallons', lambda m: 15 <= int(m.group(1)) / int(m.group(2)) <= 50, 'A boat travels {1} miles on {2} gallons'),
         (r'\bA car uses (\d+) gallons of gas to go (\d+) miles', lambda m: 15 <= int(m.group(2)) / int(m.group(1)) <= 50, 'A boat uses {1} gallons of gas to go {2} miles'),
         (r'at least (\d+) years old to vote', lambda m: False, 'at least {1} years old to enter the contest'),
         (r'\bA plant grows (\d+) inches in a year', lambda m: int(m.group(1)) <= 60, 'A bamboo plant grows {1} inches in a year')]


def swap(t):
    for pat, ok, rep in SWAPS:
        t = re.sub(pat, lambda m: m.group(0) if ok(m) else rep.format(None, *m.groups()), t)
    return t


def main():
    banks = lib.load()
    n = 0
    for u, q in lib.items(banks):
        before = (q['prompt'], q['answer'], list(q['solutionSteps']), [o['text'] for o in q.get('options', [])])
        f = FIX.get(q['id'])
        if f:
            q['prompt'], q['answer'], q['solutionSteps'] = f['prompt'], f['answer'], list(f['solutionSteps'])
            if 'options' in f:
                order = [o['text'] for o in q['options']]
                old = before[1]
                # keep the position of the correct option and of each distractor slot
                new = [f['answer'] if t == old else None for t in order]
                rest = [t for t in f['options'] if t != f['answer']]
                q['options'] = [{'text': t if t is not None else rest.pop(0), 'correct': t is not None} for t in new]
        if q['id'] in CAR:
            q['prompt'] = re.sub(r'^A (?:car travels|jogger runs|cyclist rides|hiker walks)', CAR[q['id']], q['prompt'])
        q['prompt'] = swap(q['prompt'])
        for prt in q.get('parts', []):
            prt['prompt'] = swap(prt['prompt'])
        q['solutionSteps'] = [swap(x) for x in q['solutionSteps']]
        # "How many more blue beads than red beads" when there are fewer blue beads: ask about the larger color first.
        m = re.search(r'in the ratio (\d+) : (\d+) : (\d+)\..*How many more blue beads than red beads', q['prompt'])
        if m and int(m.group(1)) > int(m.group(2)):
            q['prompt'] = q['prompt'].replace('How many more blue beads than red beads', 'How many more red beads than blue beads')
        if re.search(r'-pack of juice boxes costs', q['prompt']):
            m = re.search(r'(\d+)-pack of juice boxes costs \$([\d.]*\d)', q['prompt'])
            if float(m.group(2)) / int(m.group(1)) > 2:
                q['prompt'] = re.sub(r'A (\d+)-pack of juice boxes costs', r'A pack of \1 fruit smoothies costs', q['prompt']).replace('price per juice box', 'price per smoothie')
                q['solutionSteps'] = [s.replace('per box', 'per smoothie') for s in q['solutionSteps']]
        if re.search(r'shirts that cost \$[34] each', q['prompt']):
            q['prompt'] = q['prompt'].replace('shirts that cost', 'pairs of socks that cost').replace('the number of shirts', 'the number of pairs of socks').replace('greatest number of shirts', 'greatest number of pairs of socks')
        if before != (q['prompt'], q['answer'], q['solutionSteps'], [o['text'] for o in q.get('options', [])]):
            n += 1
    lib.save(banks)
    print('items fixed:', n)


if __name__ == '__main__':
    main()
