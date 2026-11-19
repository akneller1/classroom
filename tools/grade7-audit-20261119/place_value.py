"""Grade 7 audit #12 (2026-11-19): Place Value at grade level.

The 48 Place Value items (algebraic-expressions-integers-skill-01) wrote whole numbers in standard form and were tagged
only with Grade 5 standards. They are replaced in place (same ids, same formats) with place value as the bridge to
exponents: CP2 decimal place value and multiplying or dividing by powers of ten (review, 5.NBT.A.1–2, 6.EE.A.1);
CP1 powers of ten with negative exponents (8.EE.A.1); Honors comparisons with powers of ten (8.EE.A.3).
Each level keeps its error-analysis items and its multi-part item. Answers are computed with exact decimals."""
import os, random, re, sys
from decimal import Decimal as D, getcontext
sys.path.insert(0, os.path.dirname(__file__))
import lib

getcontext().prec = 40
SKILL = 'algebraic-expressions-integers-skill-01'
SUPS = str.maketrans('0123456789-', '⁰¹²³⁴⁵⁶⁷⁸⁹⁻')
PLACE = {2: 'hundreds', 1: 'tens', 0: 'ones', -1: 'tenths', -2: 'hundredths', -3: 'thousandths', -4: 'ten-thousandths', -5: 'hundred-thousandths'}
NAMES = ['Maya', 'Leo', 'Priya', 'Diego', 'Ana', 'Owen', 'Nia', 'Raj']


def fmt(x):
    """Exact decimal with thousands commas, no trailing zeros: 5020.07 → '5,020.07', 0.0700 → '0.07'."""
    x = D(x).normalize()
    s = format(x, 'f')
    if '.' in s:
        s = s.rstrip('0').rstrip('.')
    neg = s.startswith('-')
    s = s.lstrip('-')
    whole, _, frac = s.partition('.')
    whole = f'{int(whole):,}'
    return ('-' if neg else '') + whole + ('.' + frac if frac else '')


def p10(k):
    return '10' + str(k).translate(SUPS)


def number_with(rng, lo, hi):
    """A decimal with digits in places lo..hi (powers of ten), all digits distinct where possible."""
    digits = rng.sample(range(1, 10), hi - lo + 1) if hi - lo + 1 <= 9 else [rng.randint(1, 9) for _ in range(hi - lo + 1)]
    v = sum(D(dg) * D(10) ** k for dg, k in zip(digits, range(hi, lo - 1, -1)))
    return v, dict(zip(range(hi, lo - 1, -1), digits))


def digit_value(rng, lv):
    lo, hi = {'cp2': (-3, 1), 'cp1': (-4, 2), 'honors': (-5, 3)}[lv]
    v, d = number_with(rng, lo, hi)
    k = rng.choice([x for x in d if x < 0] if lv != 'cp2' else list(d))
    val = D(d[k]) * D(10) ** k
    ans = fmt(val)
    wrong = [fmt(val * 10), fmt(val / 10), str(d[k])]
    return dict(prompt=f'What is the value of the digit {d[k]} in {fmt(v)}?', answer=ans, wrong=wrong,
                steps=[f'The {d[k]} is in the {PLACE[k]} place.', f'Value = {d[k]} × {fmt(D(10) ** k)} = {ans}.'],
                std=['5.NBT.A.1', '8.EE.A.1'] if lv != 'cp2' else ['5.NBT.A.1', '5.NBT.A.3'], tags=[])


def expanded(rng, lv):
    lo, hi = {'cp2': (-2, 1), 'cp1': (-3, 3), 'honors': (-5, 2)}[lv]
    v, d = number_with(rng, lo, hi)
    keep = sorted(rng.sample(sorted(d), min(len(d), 4)), reverse=True)
    v = sum(D(d[k]) * D(10) ** k for k in keep)
    if lv == 'cp2':
        terms = ' + '.join(f'({d[k]} × {fmt(D(10) ** k)})' for k in keep)
    else:
        terms = ' + '.join(f'({d[k]} × {p10(k)})' if k not in (0,) else f'({d[k]} × 1)' for k in keep)
    ans = fmt(v)
    shifted = fmt(sum(D(d[k]) * D(10) ** (k + 1) for k in keep))
    squeezed = fmt(D(''.join(str(d[k]) for k in keep)) / D(10) ** max(0, -min(keep)))
    wrong = [shifted, squeezed if squeezed != ans else fmt(v * 100), fmt(v / 10)]
    return dict(prompt=f'Write the number in standard form: {terms}', answer=ans, wrong=wrong,
                steps=['Find the value of each term' + ('; a negative exponent means a decimal place (10⁻² = 0.01).' if lv != 'cp2' else '.'),
                       ' + '.join(fmt(D(d[k]) * D(10) ** k) for k in keep) + f' = {ans}.'],
                std=['5.NBT.A.3', '8.EE.A.1'] if lv != 'cp2' else ['5.NBT.A.3', '5.NBT.A.2'], tags=['multiple-representations'])


def power_op(rng, lv):
    a = D(rng.choice(['3.45', '72.5', '0.42', '5.1', '6.03', '0.817', '28.4', '0.096', '4.2']))
    k = rng.choice([2, 3, 4]) if lv != 'cp2' else rng.choice([1, 2, 3])
    mul = rng.random() < 0.5
    if lv == 'honors':
        k = rng.choice([-3, -2, 4, 5])
        mul = True
    res = a * D(10) ** k if mul else a / D(10) ** k
    if lv == 'cp2':
        expr = f'{fmt(a)} {"×" if mul else "÷"} {fmt(D(10) ** k)}'
    else:
        expr = f'{fmt(a)} {"×" if mul else "÷"} {p10(k)}'
    ans = fmt(res)
    shift = k if mul else -k
    return dict(prompt=f'Find the value: {expr}', answer=ans, wrong=[fmt(res * 10), fmt(res / 10), fmt(a * D(10) ** (-shift))],
                steps=[f'{"Multiplying" if shift > 0 else "Dividing"} by {fmt(D(10) ** abs(shift))} moves each digit {abs(shift)} place{"s" if abs(shift) != 1 else ""} '
                       f'{"left" if shift > 0 else "right"} (the decimal point moves {"right" if shift > 0 else "left"}).', f'{expr} = {ans}.'],
                std=['5.NBT.A.2', '8.EE.A.1'] if lv != 'cp2' else ['5.NBT.A.2', '6.EE.A.1'], tags=[])


def times(rng, lv):
    if lv == 'honors':
        a, b = rng.choice([(6, 2), (8, 4), (9, 3), (4, 8), (3, 6), (5, 2)])
        e1 = rng.randint(6, 9); e2 = e1 - rng.randint(2, 4)
        r = D(a) * D(10) ** e1 / (D(b) * D(10) ** e2)
        ans = fmt(r)
        return dict(prompt=f'How many times as large as {b} × {p10(e2)} is {a} × {p10(e1)}?', answer=ans,
                    wrong=[fmt(D(a) / D(b) * D(10) ** (e1 - e2 - 1)), fmt(D(10) ** (e1 - e2)), fmt(D(abs(a - b)) * D(10) ** (e1 - e2))],
                    steps=[f'Divide: ({a} × {p10(e1)}) ÷ ({b} × {p10(e2)}) = ({a} ÷ {b}) × {p10(e1)}⁻{str(e2).translate(SUPS)}.',
                           f'= {fmt(D(a) / D(b))} × {p10(e1 - e2)} = {ans}.'], std=['8.EE.A.3', '8.EE.A.1'], tags=['reasoning'])
    dg = rng.randint(2, 9)
    k1 = rng.choice([2, 1, 0]); k2 = k1 - (rng.choice([1, 2]) if lv == 'cp2' else rng.choice([3, 4, 5]))
    n1 = fmt(D(dg) * D(10) ** k1); n2 = fmt(D(dg) * D(10) ** k2)
    ans = fmt(D(10) ** (k1 - k2))
    return dict(prompt=f'The digit {dg} appears in {n1} and in {n2}. The value of the {dg} in {n1} is how many times the value of the {dg} in {n2}?',
                answer=ans, wrong=[fmt(D(10) ** (k1 - k2 - 1)), fmt(D(10) ** (k1 - k2 + 1)), str(k1 - k2)],
                steps=[f'In {n1} the {dg} is worth {n1}; in {n2} it is worth {n2}.',
                       f'Each place to the left is 10 times the place to its right, and the places are {k1 - k2} apart: 10 to the power {k1 - k2} = {ans}.'],
                std=['5.NBT.A.1', '8.EE.A.1'] if lv != 'cp2' else ['5.NBT.A.1', '5.NBT.A.2'], tags=['reasoning'])


def as_power(rng, lv):
    k = {'cp2': rng.choice([3, 4, 5, 6]), 'cp1': rng.choice([-2, -3, -4]), 'honors': rng.choice([-3, -4, -5, -6])}[lv]
    n = fmt(D(10) ** k)
    q = f'Write {n} as a power of 10.' if lv != 'honors' else rng.choice([f'Write {n} as a power of 10.', f'Write 1/{fmt(D(10) ** -k)} as a power of 10.'])
    return dict(prompt=q, answer=p10(k), wrong=[p10(-k), p10(k + (1 if k < 0 else -1)), p10(k - (1 if k < 0 else -1))],
                steps=[f'{n} has {abs(k)} {"zeros after the 1" if k > 0 else "places after the decimal point, ending in 1"}.', f'{n} = {p10(k)}.'],
                std=['6.EE.A.1'] if lv == 'cp2' else ['8.EE.A.1'], tags=['multiple-representations'])


def context(rng, lv):
    if lv == 'cp2':
        bill, coin, word = rng.choice([('100', '0.01', 'pennies'), ('10', '0.10', 'dimes'), ('1', '0.01', 'pennies'), ('100', '0.10', 'dimes'), ('1,000', '0.01', 'pennies')])
        v = D(bill.replace(',', '')) / D(coin)
        n = fmt(v)
        return dict(prompt=f'How many {word} (${coin} each) have the same value as ${bill}?', answer=n,
                    wrong=[fmt(v / 10), fmt(v * 10), fmt(v / 100)], steps=[f'Divide the amount by the value of one coin: {bill} ÷ {coin}.', f'= {n}.'],
                    std=['5.NBT.A.2', '6.NS.B.3'], tags=['connections'])
    pairs = [('A grain of sand', 'a pebble', 'mass', 'g', (6, -5), (3, -1)), ('A dust mite', 'an ant', 'length', 'm', (3, -4), (6, -3)),
             ('A virus', 'a human hair', 'width', 'm', (1, -7), (8, -5)), ('A raindrop', 'a bucket of water', 'volume', 'L', (5, -5), (5, 1))]
    s, l, what, unit, (a, ea), (b, eb) = rng.choice(pairs)
    r = D(b) * D(10) ** eb / (D(a) * D(10) ** ea)
    ans = fmt(r)
    return dict(prompt=f'{s} has a {what} of about {a} × {p10(ea)} {unit}, and {l} has a {what} of about {b} × {p10(eb)} {unit}. About how many times as large is the {what} of {l.split(" ", 1)[1] if l.startswith(("a ", "an ")) else l}?',
                answer=ans, wrong=[fmt(r / 10), fmt(r * 10), fmt(D(10) ** (eb - ea))],
                steps=[f'Divide: ({b} × {p10(eb)}) ÷ ({a} × {p10(ea)}).', f'= {fmt(D(b) / D(a))} × {p10(eb - ea)} = {ans}.'],
                std=['8.EE.A.3', '8.EE.A.4'], tags=['connections'])


def order(rng, lv):
    if lv == 'honors':
        base = rng.randint(2, 8)
        vals = [(f'{base} × 10⁻²', D(base) / 100), (f'{fmt(D(base) / 100 + D("0.001"))}', D(base) / 100 + D('0.001')),
                (f'{base}.1 × 10⁻³', D(f'{base}.1') / 1000), (f'{fmt(D(base) / 10)}', D(base) / 10)]
    else:
        v, d = number_with(rng, -3 if lv == 'cp2' else -4, 0)
        a = D(rng.randint(1, 9)) / 10
        vals = [(fmt(a), a), (fmt(a + D('0.05')), a + D('0.05')), (fmt(a + D('0.005')), a + D('0.005')), (fmt(a * 10 + D('0.06')), a * 10 + D('0.06'))]
        if lv == 'cp1':
            vals[1] = (fmt(-(a + D('0.03'))), -(a + D('0.03')))
    rng.shuffle(vals)
    srt = sorted(vals, key=lambda t: t[1])
    ans = ', '.join(t[0] for t in srt)
    return dict(prompt='Order from least to greatest: ' + ', '.join(t[0] for t in vals), answer=ans,
                wrong=[', '.join(t[0] for t in reversed(srt)), ', '.join(t[0] for t in sorted(vals, key=lambda t: len(t[0]))), ', '.join(t[0] for t in vals)],
                steps=['Write each number as a decimal' + (' (10⁻² = 0.01, 10⁻³ = 0.001)' if lv == 'honors' else '') + ' and line up the place values.',
                       'Compare from the greatest place: ' + ans + '.'], std=['6.NS.C.7a', '8.EE.A.4'] if lv == 'honors' else ['5.NBT.A.3', '6.NS.C.7a'], tags=['misconception'])


def mistake(rng, lv, name):
    it = digit_value(rng, lv) if rng.random() < 0.6 else as_power(rng, lv)
    if 'power of 10' in it['prompt']:
        wrong = it['wrong'][1]
        why = 'Counted the zeros, not the decimal places, so the exponent is off by one.' if lv != 'cp2' else 'Miscounted the zeros.'
    else:
        wrong = it['wrong'][1]
        why = 'Counted the place one position too far right.'
    p = f'{name} answered this problem incorrectly.\n{it["prompt"]}\n{name}\'s answer: {wrong}\nIdentify the mistake and give the correct answer.'
    return dict(prompt=p, answer=it['answer'], wrong=[], steps=[f'Mistake: {why}'] + it['steps'] + [f'The correct answer is {it["answer"]}, not {wrong}.'],
                std=it['std'], tags=['error-analysis', 'misconception'])


def multipart(rng, lv):
    parts = [digit_value(rng, lv), power_op(rng, lv), as_power(rng, lv), expanded(rng, lv)]
    return dict(prompt='Answer each part. Show your work.', parts=[{'prompt': p['prompt'], 'answer': p['answer']} for p in parts],
                answer='; '.join(f'({c}) {p["answer"]}' for c, p in zip('abcd', parts)),
                steps=[f'({c}) ' + ' '.join(p['steps']) for c, p in zip('abcd', parts)], std=['5.NBT.A.1', '8.EE.A.1'] if lv != 'cp2' else ['5.NBT.A.1', '5.NBT.A.2'], tags=['multistep'])


SLOTS = [digit_value, expanded, power_op, times, as_power, digit_value, expanded, power_op, order, times, context, expanded, as_power, None, None, None]


def main():
    banks, tags = lib.load(), lib.load_tags()
    u = 'algebraic-expressions-integers'
    n = 0
    for lv_i, lv in enumerate(('cp2', 'cp1', 'honors')):
        rng = random.Random(f'g7-place-value-{lv}')
        seen = set()
        for q in [q for q in banks[u]['questions'] if q['skillId'] == SKILL and q['level'] == lv]:
            i = int(q['id'][-3:])
            for attempt in range(50):
                if q['format'] == 'open-response':
                    it = multipart(rng, lv)
                elif 'error-analysis' in tags[u].get(q['id'], []) or 'answered this problem incorrectly' in q['prompt']:
                    it = mistake(rng, lv, NAMES[(i + lv_i) % len(NAMES)])
                else:
                    it = SLOTS[(i - 1) % 13](rng, lv)
                if it['prompt'] not in seen and (q['format'] != 'multiple-choice' or len({it['answer'], *it['wrong']}) == 4):
                    break
            seen.add(it['prompt'])
            q['prompt'] = it['prompt']
            q['answer'] = it['answer']
            q['solutionSteps'] = it['steps']
            q['standards'] = it['std']
            q.pop('parts', None)
            if 'parts' in it:
                q['parts'] = it['parts']
            if q['format'] == 'multiple-choice':
                opts = [it['answer']] + it['wrong'][:3]
                rng.shuffle(opts)
                q['options'] = [{'text': t, 'correct': t == it['answer']} for t in opts]
            else:
                q.pop('options', None)
            q['sourceNotes'] = lib.SOURCE.format(fam='g7_place_value_' + lv) + ' Teacher review pending.'
            tags[u][q['id']] = it['tags']
            n += 1
    lib.save(banks)
    lib.save_tags(tags)
    print('place value items rewritten:', n)


if __name__ == '__main__':
    main()
