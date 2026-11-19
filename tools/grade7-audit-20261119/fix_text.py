"""Grade 7 audit #20 (2026-11-19): text clean-up.
 * name/pronoun agreement ("Omar is 4 times as old as her cousin");
 * singular units after 1 ("1 units", "1 feet", "1 inches", "1 blocks");
 * the two parallelogram items filed under Area of Triangles and Trapezoids become triangle items (same numbers, the
   parallelogram answer becomes the forgot-the-half distractor);
 * "a 6 on a number cube and a 3 on a number cube" names two cubes;
 * one minus sign throughout: the bank writes negatives with "-", and 125 strings mixed in "−".
Idempotent."""
import re, sys, os
sys.path.insert(0, os.path.dirname(__file__))
import lib

SING = {'units': 'unit', 'feet': 'foot', 'inches': 'inch', 'blocks': 'block', 'meters': 'meter'}


def fix_str(s):
    s = s.replace('−', '-')
    s = re.sub(r'(?<![\d/.,-])1 (units|feet|inches|blocks|meters)\b', lambda m: '1 ' + SING[m.group(1)], s)
    return s


def walk(o):
    if isinstance(o, str):
        return fix_str(o)
    if isinstance(o, list):
        return [walk(x) for x in o]
    if isinstance(o, dict):
        return {k: (walk(v) if k not in ('id', 'skillId', 'level', 'format', 'standards', 'sourceNotes', 'src') else v) for k, v in o.items()}
    return o


TRIANGLE = {
    'pa7-arv-s02-cp2-003': (5, 8, ['40 m²', '13 m²', '20 m²', '26 m²']),
    'pa7-arv-s02-cp2-011': (15, 14, ['210 m²', '29 m²', '105 m²', '58 m²']),
}


def main():
    banks = lib.load()
    n = 0
    for u, q in lib.items(banks):
        before = repr(q)
        new = walk(q)
        q.clear(); q.update(new)
        q['prompt'] = re.sub(r'\b(Omar|Ben|Sam|Jamal|Yusuf|Dev|Kai|Leo|Hiro)( is \d+ times as old as )her( cousin)', r'\1\2his\3', q['prompt'])
        if q['id'] in TRIANGLE:
            b, h, opts = TRIANGLE[q['id']]
            area = b * h // 2 if (b * h) % 2 == 0 else b * h / 2
            q['prompt'] = f'Find the area of a triangle with base {b} m and height {h} m.'
            q['answer'] = f'{area} m²'
            q['options'] = [{'text': t, 'correct': t == q['answer']} for t in opts]
            q['solutionSteps'] = ['A triangle is half of a parallelogram with the same base and height.', 'A = ½bh.',
                                  f'A = ½ × {b} × {h} = {area} m².']
        q['prompt'] = re.sub(r'Find the probability of getting (an? [\w ]+?) on a number cube and (an? [\w ]+?) on a number cube\.',
                             r'Two number cubes are rolled. Find the probability of getting \1 on the first cube and \2 on the second.', q['prompt'])
        n += repr(q) != before
    lib.save(banks)
    print('text fixes:', n, 'items')


if __name__ == '__main__':
    main()
