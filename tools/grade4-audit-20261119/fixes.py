"""4th Grade Math audit 2026-11-19: the small content fixes.

#11 4.OA.A.3.a is not a Common Core code: retag 4.OA.A.3.
#14 numbers past 1,000,000 (4.NBT.A) and two-digit divisors (4.NBT.B.6): new numbers.
#15 story nouns that do not fit ("A baker makes 40 golf balls"); these packing problems also divided by 10, 11, 12 and 24.
#16 duplicate items: the second of each pair gets a different key.
#18 elapsed times longer than two hours (course outline: within two adjacent hours)."""
from lib import mc

ERR_NOTE = None


def run(o):
    # 11
    for q in list(o.items()):
        if '4.OA.A.3.a' in (q.get('standards') or []):
            o.edit(q['id'], standards=[('4.OA.A.3' if s == '4.OA.A.3.a' else s) for s in q['standards']])

    # 14: past 1,000,000
    o.edit('m4-as-s01-honors-027',
           prompt='Tessa solved this problem.\nFind the missing addend: 211,456 + ___ = 772,833\nTessa answered: 984,289\nFind the mistake. What is the correct answer?',
           answer='561,377',
           solutionSteps=['Mistake: added the two numbers instead of subtracting.', 'Subtract the known addend from the sum.',
                          '772,833 − 211,456 = 561,377.', 'The correct answer is 561,377, not 984,289.'])
    o.meta_set('m4-as-s01-honors-027', explanation='The correct answer is 561,377, not 984,289.', shown=['984,289'],
               distractors={'984,289': 'added the two numbers instead of subtracting', '561,477': 'made a regrouping mistake', '661,377': 'made a subtraction fact mistake'})
    o.edit('m4-as-s04-honors-003',
           prompt='Noah says that 556,654 + 212,209 = 668,863. Use estimation to decide: is the answer reasonable?',
           answer='No. An estimate is 560,000 + 210,000 = 770,000, which is not close to 668,863.',
           options=[{'text': t, 'correct': c} for t, c in [
               ('Yes. An estimate is 560,000 + 210,000 = 770,000, which is close to 668,863.', False),
               ('No. The sum of two 6-digit numbers must have 7 digits.', False),
               ('No. An estimate is 560,000 + 210,000 = 770,000, which is not close to 668,863.', True),
               ('Yes. The answer has the same last digit as the exact answer.', False)]],
           solutionSteps=['Round each number to the nearest ten thousand: 560,000 + 210,000 = 770,000.',
                          '668,863 is about 100,000 less than 770,000, so the answer is not reasonable. (The exact sum is 768,863.)'])
    o.edit('m4-as-s04-honors-004',
           prompt='To estimate 392,215 + 477,767, Hana rounds each number to the nearest hundred thousand and gets 400,000 + 500,000 = 900,000. Is the estimate greater than or less than the exact sum?',
           solutionSteps=['392,215 rounds up to 400,000 and 477,767 rounds up to 500,000.', 'Both numbers were rounded up, so the estimate is greater than the exact sum (869,982).'])
    o.edit('m4-as-s04-honors-010',
           prompt='To estimate 386,073 + 437,040, Liam rounds each number to the nearest ten thousand and gets 390,000 + 440,000 = 830,000. Is the estimate greater than or less than the exact sum?',
           solutionSteps=['386,073 rounds up to 390,000 and 437,040 rounds up to 440,000.', 'Both numbers were rounded up, so the estimate is greater than the exact sum (823,113).'])
    o.edit('m4-as-s04-honors-025',
           prompt='Noah solved this problem.\nEstimate the sum by rounding each number to the nearest hundred thousand: 481,910 + 291,671\nNoah answered: 773,581\nFind the mistake. What is the correct answer?',
           answer='800,000',
           solutionSteps=['Mistake: found the exact sum instead of estimating.', '481,910 rounds to 500,000 and 291,671 rounds to 300,000.',
                          '500,000 + 300,000 = 800,000.', 'The correct answer is 800,000, not 773,581.'])
    o.meta_set('m4-as-s04-honors-025', explanation='The correct answer is 800,000, not 773,581.', shown=['773,581'],
               distractors={'773,581': 'found the exact sum instead of estimating', '700,000': 'rounded 481,910 down', '770,000': 'rounded to the nearest ten thousand'})
    o.edit('m4-as-s05-honors-001',
           prompt='Hana scored 377,547 points in the first game and 407,545 points in the second game. Then Hana lost 604,156 points in a bonus round. How many points does Hana have now?',
           solutionSteps=['First add: 377,547 + 407,545 = 785,092.', 'Then subtract: 785,092 − 604,156 = 180,936 points.'])
    o.edit('m4-as-s05-honors-028',
           prompt='True or false? A warehouse had 192,910 boxes. A truck delivered 511,257 more boxes. Then 561,690 boxes were shipped out. How many boxes are in the warehouse now?\nAnswer shown: 704,167 boxes\nChoose the best response.',
           answer='False. The correct answer is 142,477 boxes.',
           options=[{'text': t, 'correct': c} for t, c in [
               ('False. The correct answer is 142,477 boxes.', True), ('False. The correct answer is 68,780 boxes.', False),
               ('False. The correct answer is 242,477 boxes.', False), ('True. 704,167 boxes is the correct answer.', False)]],
           solutionSteps=['First add: 192,910 + 511,257 = 704,167.', 'Then subtract: 704,167 − 561,690 = 142,477 boxes.',
                          'The answer 704,167 boxes stops after the first step; it should be 142,477 boxes.'])
    o.edit('m4-pv-s01-honors-004', prompt='Fill in the blank: 925,000 ÷ 10 = ___', answer='92,500',
           solutionSteps=['Dividing by 10 moves each digit one place to the right.', '925,000 ÷ 10 = 92,500.'])
    o.meta_set('m4-pv-s01-honors-004', explanation='925,000 ÷ 10 = 92,500.', distractors={'9,250': 'divided by 100', '9,250,000': 'multiplied by 10', '925': 'divided by 1,000'})
    o.edit('m4-pv-s02-honors-026',
           prompt='Sam solved this problem.\nWrite in standard form: 800,000 + 40,000 + 7,000 + 20 + 1\nSam answered: 84,721\nFind the mistake. What is the correct answer?',
           solutionSteps=['Mistake: left out the 0 in the hundreds place.', 'Each part tells the value of one digit: 8 hundred thousands, 4 ten thousands, 7 thousands, 0 hundreds, 2 tens, 1 one.',
                          'Add the parts: 847,021.', 'The correct answer is 847,021, not 84,721.'])
    o.meta_set('m4-pv-s02-honors-026', explanation='The correct answer is 847,021, not 84,721.', shown=['84,721'], misconception='left out the 0 that holds the hundreds place')

    # 14: two-digit divisors in the Division unit
    for qid, who, things, total, k, per in [('m4-dv-s01-cp1-006', 'Zoe', ('pencils', 'tables'), 96, 8, 12), ('m4-dv-s01-cp1-017', 'Rosa', ('marbles', 'bags'), 44, 4, 11),
                                             ('m4-dv-s01-honors-006', 'Isla', ('stickers', 'friends'), 990, 9, 110), ('m4-dv-s01-honors-017', 'Dev', ('muffins', 'boxes'), 1200, 6, 200)]:
        assert total == k * per
        tot = f'{total:,}'
        o.edit(qid, prompt=f'{who} shares {tot} {things[0]} equally among {k} {things[1]}. How many {things[0]} does each of the {k} {things[1]} get?',
               answer=f'{per} {things[0]}', solutionSteps=[f'Equal sharing means divide: {tot} ÷ {k}.', f'{tot} ÷ {k} = {per} {things[0]}.'])
        o.meta_set(qid, explanation=f'{tot} ÷ {k} = {per}.', distractors={str(per + 1): 'counted one too many', str(per * 10): 'misplaced a digit', str(total - k): 'subtracted instead of dividing'})
    o.edit('m4-dv-s01-cp1-009', prompt='Which multiplication fact can help you solve 30 ÷ 5?', answer='5 × 6 = 30',
           options=mc('5 × 6 = 30', ['5 + 6 = 30', '30 × 5 = 6', '5 × 7 = 30']),
           solutionSteps=['Division and multiplication are related: divisor × quotient = dividend.', '5 × 6 = 30, so 30 ÷ 5 = 6.'])
    o.edit('m4-dv-s01-honors-019', prompt='Find the missing number: ___ ÷ 9 = 7', answer='63', options=mc('63', ['16', '72', '56']),
           solutionSteps=['Multiply the quotient by the divisor.', '7 × 9 = 63, so 63 ÷ 9 = 7.'])

    # 15: packing problems (also had divisors 10, 11, 12 and 24)
    for qid, total, things, k, add in [('m4-dp-s03-cp2-002', 54, 'oranges', 6, 3), ('m4-dp-s03-cp2-009', 40, 'golf balls', 5, 3),
                                        ('m4-dp-s03-cp2-016', 84, 'golf balls', 7, 2), ('m4-dp-s03-cp2-023', 54, 'candles', 9, 3),
                                        ('m4-dp-s03-cp2-026', 44, 'bars of soap', 4, 3), ('m4-dp-s03-cp1-002', 96, 'oranges', 8, 3)]:
        per = total // k
        assert per * k == total
        base = (f'A shop has {total} {things} and packs them equally into {k} boxes. Then a worker adds {add} more to each box. '
                f'How many {things} are in each box now?')
        steps = [f'{total} ÷ {k} = {per} in each box.', f'{per} + {add} = {per + add} {things}.']
        if qid.endswith('cp2-026'):
            o.edit(qid, prompt='Tessa solved this problem.\n' + base + f'\nTessa answered: {per} {things}\nFind the mistake. What is the correct answer?',
                   answer=f'{per + add} {things}', solutionSteps=['Mistake: stopped after dividing.'] + steps + [f'The correct answer is {per + add} {things}, not {per} {things}.'])
            o.meta_set(qid, explanation=f'The correct answer is {per + add} {things}, not {per} {things}.', shown=[f'{per} {things}'])
            continue
        fields = dict(prompt=base, answer=f'{per + add} {things}', solutionSteps=steps)
        if o.cur(qid, 'options'):
            fields['options'] = mc(f'{per + add} {things}', [f'{per} {things}', f'{per + add + k} {things}', f'{total + add} {things}'])
        o.edit(qid, **fields)
        o.meta_set(qid, explanation=f'{total} ÷ {k} = {per}, and {per} + {add} = {per + add}.',
                   distractors={f'{per} {things}': 'stopped after dividing', f'{total + add} {things}': 'added before dividing', f'{per * add} {things}': 'multiplied instead of adding'})

    # 16: duplicate pairs
    o.edit('m4-fm-s03-cp2-008', answer='21', options=mc('21', ['17', '7', '13']),
           solutionSteps=['A composite number has more than two factors.', '21 = 3 × 7, so 21 is composite. 17, 7 and 13 are prime.'])
    o.edit('m4-fe-s02-cp2-024', answer='2/5', options=mc('2/5', ['2/8', '3/6', '4/10']),
           solutionSteps=['A fraction is in simplest form when 1 is the only common factor of the numerator and the denominator.',
                          '2 and 5 have no common factor except 1, so 2/5 is in simplest form. 2/8, 3/6 and 4/10 can all be simplified.'])
    o.edit('m4-ga-s04-cp2-015', prompt='A quadrilateral has 2 pairs of parallel sides, 4 right angles, and 4 sides of equal length. What is the most specific name for it?',
           answer='square', options=mc('square', ['rectangle', 'rhombus', 'parallelogram']),
           solutionSteps=['4 right angles make it a rectangle, and 4 equal sides make it a rhombus.', 'A shape that is both is a square, the most specific name.'])
    o.edit('m4-ga-s04-cp1-029', prompt='A quadrilateral has exactly 1 pair of parallel sides. What is the most specific name for it?',
           answer='trapezoid', options=mc('trapezoid', ['rhombus', 'rectangle', 'parallelogram']),
           solutionSteps=['A parallelogram, rectangle and rhombus all have 2 pairs of parallel sides.', 'A quadrilateral with exactly 1 pair of parallel sides is a trapezoid.'])

    # 18: elapsed time within two hours
    for qid, start, end, ans, wrong in [('m4-mc-s03-cp2-009', '10:00 AM', '11:50 AM', '1 hour 50 minutes', ['2 hours 50 minutes', '1 hour 10 minutes', '50 minutes']),
                                         ('m4-mc-s03-cp1-001', '3:45 PM', '4:50 PM', '1 hour 5 minutes', ['1 hour 55 minutes', '5 minutes', '2 hours 5 minutes']),
                                         ('m4-mc-s03-honors-008', '5:16 PM', '7:07 PM', '1 hour 51 minutes', ['51 minutes', '2 hours 51 minutes', '1 hour 9 minutes'])]:
        kind = o.cur(qid, 'prompt').split(' starts')[0]
        hh, mm = ans.split(' hour')[0], ans.split(' ')[-2]
        h0, m0 = start.split(':'); h1 = int(h0) + 1 if int(h0) < 12 else 1
        mid = f'{h1}:{m0.split()[0]} {start.split()[1] if h1 != 12 else "PM"}'
        o.edit(qid, prompt=f'{kind} starts at {start} and ends at {end}. How long does it last?', answer=ans, options=mc(ans, wrong),
               solutionSteps=[f'Count 1 whole hour from {start}: that takes you to {mid}.', f'Then count {mm} more minutes to {end}. Total: {ans}.'])

    # #14 (found by the recompute test): four more two-digit divisors; swap the divisor and the quotient.
    for qid, who, total, k, things in [('m4-dp-s03-cp1-010', None, 246, 6, 'cupcakes'), ('m4-dp-s03-cp1-018', None, 116, 4, 'muffins'), ('m4-dp-s03-cp1-026', 'Lena', 364, 7, 'cupcakes')]:
        per = total // k
        assert per * k == total
        base = f'A baker makes {total} {things} and packs them equally into {k} boxes. Then the baker adds 1 more to each box. How many {things} are in each box now?'
        steps = [f'{total} ÷ {k} = {per} in each box.', f'{per} + 1 = {per + 1} {things}.']
        if who:
            o.edit(qid, prompt=f'{who} solved this problem.\n{base}\n{who} answered: {per} {things}\nFind the mistake. What is the correct answer?',
                   answer=f'{per + 1} {things}', solutionSteps=['Mistake: stopped after dividing.'] + steps + [f'The correct answer is {per + 1} {things}, not {per} {things}.'])
        else:
            fields = dict(prompt=base, answer=f'{per + 1} {things}', solutionSteps=steps)
            if qid.endswith('010'):
                fields['options'] = mc(f'{per + 1} {things}', [f'{total + 1} {things}', f'{per} {things}', f'{per + 2} {things}'])
            o.edit(qid, **fields)
        o.meta_set(qid, explanation=f'{total} ÷ {k} = {per}, then {per} + 1 = {per + 1}.', distractors={f'{per} {things}': 'stopped after dividing', f'{total + 1} {things}': 'added before dividing', f'{per + 2} {things}': 'added one too many'})
    o.edit('m4-dv-s01-cp1-012', prompt='Ava shares 88 beads equally among 8 bracelets. How many beads does each of the 8 bracelets get?', answer='11 beads',
           options=mc('11 beads', ['12 beads', '704 beads', '80 beads']), solutionSteps=['Equal sharing means divide: 88 ÷ 8.', '88 ÷ 8 = 11 beads.'])
    o.meta_set('m4-dv-s01-cp1-012', explanation='88 ÷ 8 = 11.', distractors={'12 beads': 'counted one too many', '704 beads': 'multiplied instead of dividing', '80 beads': 'subtracted instead of dividing'})

    # #14 (found by the recompute test): Advanced estimation items whose sums go past 1,000,000. The number-line pictures stay right,
    # so these ask for the estimated difference instead; the table item asks about two days whose total stays under 1,000,000.
    for qid, a, b, ra, rb, place, thing, ctx in [('m4-as-s04-honors-001', 875285, 683940, 880000, 680000, 'ten thousand', None, None),
                                                 ('m4-as-s04-honors-013', 692161, 439233, 700000, 400000, 'hundred thousand', None, None),
                                                 ('m4-as-s04-honors-017', 860045, 670239, 900000, 700000, 'hundred thousand', 'muffins', 'A bakery sold {a} muffins in March and {b} muffins in April.'),
                                                 ('m4-as-s04-honors-021', 994483, 420478, 990000, 420000, 'ten thousand', 'muffins', 'A bakery sold {a} muffins in March and {b} muffins in April.'),
                                                 ('m4-as-s04-honors-024', 755103, 302760, 760000, 300000, 'ten thousand', 'cans', 'A school collected {a} cans in the fall and {b} cans in the spring.')]:
        d = ra - rb
        if ctx:
            prompt = ctx.format(a=f'{a:,}', b=f'{b:,}') + f' Round each number to the nearest {place}. About how many more {thing} is the first number than the second?'
            ans = f'{d:,} {thing}'
        else:
            prompt = f'Estimate the difference by rounding each number to the nearest {place}: {a:,} − {b:,}'
            ans = f'{d:,}'
        o.edit(qid, prompt=prompt, answer=ans, solutionSteps=[f'{a:,} rounds to {ra:,} and {b:,} rounds to {rb:,}.', f'{ra:,} − {rb:,} = {ans}.'])
        sfx = f' {thing}' if thing else ''
        u = 10000 if place == 'ten thousand' else 100000
        o.meta_set(qid, explanation=f'{ra:,} − {rb:,} = {d:,}.', distractors={f'{a - b:,}{sfx}': 'found the exact difference', f'{ra + rb:,}{sfx}': 'added instead of subtracting', f'{d + u:,}{sfx}': 'rounded one number the wrong way'})
    o.edit('m4-as-s04-honors-030', parts=[{'prompt': 'Estimate the sum by rounding each number to the nearest hundred thousand: 719,369 + 280,626', 'answer': '1,000,000'},
                                          {'prompt': 'Estimate the sum by rounding each number to the nearest ten thousand: 604,659 + 378,964', 'answer': '980,000'},
                                          {'prompt': 'Estimate the sum by rounding each number to the nearest ten thousand: 248,158 + 215,263', 'answer': '470,000'},
                                          {'prompt': 'Estimate the difference by rounding each number to the nearest hundred thousand: 915,884 − 769,665', 'answer': '100,000'}],
           answer='(a) 1,000,000; (b) 980,000; (c) 470,000; (d) 100,000',
           solutionSteps=['(a) 719,369 rounds to 700,000 and 280,626 rounds to 300,000. 700,000 + 300,000 = 1,000,000.',
                          '(b) 604,659 rounds to 600,000 and 378,964 rounds to 380,000. 600,000 + 380,000 = 980,000.',
                          '(c) 248,158 rounds to 250,000 and 215,263 rounds to 220,000. 250,000 + 220,000 = 470,000.',
                          '(d) 915,884 rounds to 900,000 and 769,665 rounds to 800,000. 900,000 − 800,000 = 100,000.'])
    o.edit('m4-as-s05-honors-004', prompt='The table shows the number of pages printed each day. How many pages were printed on Tuesday and Wednesday combined?',
           answer='689,330', solutionSteps=['Add the two days: 497,691 + 191,639 = 689,330.'])
    o.meta_set('m4-as-s05-honors-004', explanation='497,691 + 191,639 = 689,330.', distractors={'1,136,598': 'used Thursday instead of Wednesday', '306,052': 'subtracted instead of adding', '679,330': 'forgot to regroup'})
