#!/usr/bin/env python3
"""Build every Discrete Math bank: python3 tools/discrete-math/bank/build_all.py [unit-module ...]
Writes question-banks/discrete/<unit>.json, validates against the repository schema and prints coverage."""
import sys, os, json, re, importlib, collections
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..', '..'))
sys.path.insert(0, HERE)
from core import write

MODULES = ['u01_speaking', 'u02_logic', 'u03_proof', 'u04_sequences', 'u05_sets', 'u06_relations',
           'u07_counting', 'u08_graphs', 'u09_election', 'u10_lp']


def lint(q):
    probs = []
    texts = [q['prompt']] + q['solutionSteps'] + [o['text'] for o in q.get('options', [])] + \
        [p['prompt'] + ' ' + str(p['answer']) for p in q.get('parts', [])] + [str(q['answer'])]
    for t in texts:
        for m in re.finditer(r'(rt|ov|sys|tbl|cbrt)\{', t):
            if m.start() == 0 or not t[m.start() - 1].isalpha():
                probs.append('mini-syntax trigger %r' % m.group(0))
        if re.search(r'(?<![A-Za-z])v\{', t):
            probs.append('v{ trigger')
        if '@{' in t:
            probs.append('@{ trigger')
    return probs


def _num_distractors(a):
    from fractions import Fraction
    t = a.replace('\u2212', '-')
    if re.fullmatch(r'-?\d+', t):
        n = int(t)
        c = [n + 1, n - 1, 2 * n if n not in (0, 1) else n + 2, n + 10 if abs(n) > 20 else n + 3]
        return [str(x) for x in c]
    if re.fullmatch(r'-?\d+/\d+', t):
        q = Fraction(t)
        c = [q + Fraction(1, q.denominator), 1 - q if 0 < q < 1 else q * 2, Fraction(q.numerator, q.denominator + 1), Fraction(q.numerator + 1, q.denominator + 1)]
        return [('%d/%d' % (x.numerator, x.denominator) if x.denominator != 1 else str(x.numerator)) for x in c]
    if re.fullmatch(r'\d+(, \d+){2,}', t):
        v = [int(x) for x in t.split(', ')]
        out = []
        for i in range(len(v)):
            for j in range(len(v)):
                if i != j and v[i] > 0:
                    w = v[:]; w[i] -= 1; w[j] += 1
                    out.append(', '.join(map(str, w)))
        return out
    if re.fullmatch(r'\{[^{}]*\}', t) and ',' in t:
        els = [x.strip() for x in t[1:-1].split(',')]
        out = ['{' + ', '.join(els[:-1]) + '}', '{' + ', '.join(els[1:]) + '}']
        if all(re.fullmatch(r'-?\d+', x) for x in els):
            out.append('{' + ', '.join(els + [str(int(els[-1]) + 1)]) + '}')
            out.append('{' + ', '.join([str(int(els[0]) - 1)] + els) + '}')
        return out
    return []


def ensure_mc(questions, need=4):
    """Convert (not copy) short-answer items with numeric, list or set answers into multiple choice where a skill/level has fewer
    than `need` MC items, so the exact-level game decks (multiple choice only) have enough items. Distractors are near misses
    (off-by-one counts, a seat moved between states, an element added or dropped) and are never equal to the key."""
    import collections, random
    by = collections.defaultdict(list)
    for q in questions:
        by[(q['skillId'], q['level'])].append(q)
    converted = 0
    for k, qs in sorted(by.items()):
        have = sum(q['format'] == 'multiple-choice' for q in qs)
        for q in qs:
            if have >= need:
                break
            if q['format'] != 'short-answer' or '_error)' in q['sourceNotes']:
                continue
            a = str(q['answer'])
            fam = (re.search(r'family: ([a-z0-9_]+)\)', q['sourceNotes']) or [None, ''])[1]
            if re.fullmatch(r'\d+(, \d+){2,}', a) and fam not in ('hamilton', 'divisor_method'):
                continue
            ds = [d for d in dict.fromkeys(_num_distractors(a)) if d != a.replace('\u2212', '-') and d != a]
            if len(ds) < 3:
                continue
            opts = [{'text': a, 'correct': True}] + [{'text': d, 'correct': False} for d in ds[:3]]
            random.Random(q['id']).shuffle(opts)
            q['format'] = 'multiple-choice'
            q['answer'] = a
            q['options'] = opts
            q['solutionSteps'] = q['solutionSteps'] + ['The other choices are near misses (an off-by-one count, one changed element or one moved seat).']
            have += 1
            converted += 1
    return converted


def main(mods):
    import jsonschema
    schema = json.load(open(os.path.join(ROOT, 'schemas/question-bank.schema.json')))
    os.makedirs(os.path.join(ROOT, 'question-banks/discrete'), exist_ok=True)
    catalog = open(os.path.join(ROOT, 'course-catalog.js')).read()
    total = 0
    report = {}
    for m in mods:
        mod = importlib.import_module(m)
        b = mod.build()
        from quick import add_quick
        add_quick(b)
        p = b.payload()
        seen, kept = set(), []
        for q in p['questions']:
            k = (q['prompt'], json.dumps(q.get('diagram')), q['format'])
            if k in seen:
                print('DROPPED DUPLICATE', q['id'], q['prompt'][:60].replace('\n', ' '))
                continue
            seen.add(k)
            kept.append(q)
        p['questions'] = kept
        n_conv = ensure_mc(p['questions'])
        if n_conv:
            print('converted %d short-answer items to multiple choice in %s' % (n_conv, b.unit))
        jsonschema.validate(p, schema)
        ids = [q['id'] for q in p['questions']]
        assert len(ids) == len(set(ids)), 'duplicate ids in ' + m
        for q in p['questions']:
            if q['format'] == 'multiple-choice':
                assert sum(o['correct'] for o in q['options']) == 1 and q['answer'] == [o['text'] for o in q['options'] if o['correct']][0], q['id']
                assert len({o['text'] for o in q['options']}) == len(q['options']), ('dup option', q['id'])
            if q['format'] == 'select-all':
                assert sorted(q['answer']) == sorted(o['text'] for o in q['options'] if o['correct']), q['id']
            for pr in lint(q):
                print('LINT', q['id'], pr)
        sig = collections.Counter((q['prompt'], json.dumps(q.get('diagram'))) for q in p['questions'])
        for k, v in sig.items():
            if v > 1:
                print('DUPLICATE PROMPT', v, k[0][:80])
        write(os.path.join(ROOT, 'question-banks/discrete/%s.json' % b.unit), p)
        cnt = collections.Counter((q['skillId'], q['level']) for q in p['questions'])
        fm = collections.Counter(q['format'] for q in p['questions'])
        err = collections.Counter(q['level'] for q in p['questions'] if '_error)' in q['sourceNotes'])
        thin = []
        for s in range(1, b.n_skills + 1):
            row = [cnt[(b.sid(s), L)] for L in ('cp2', 'cp1', 'honors')]
            if sum(row) < 30 or min(row) < 8:
                thin.append((s, row))
        print('%-32s %4d q  formats=%s  errors=%s' % (b.unit, len(p['questions']), dict(fm), dict(err)))
        for s in range(1, b.n_skills + 1):
            row = [cnt[(b.sid(s), L)] for L in ('cp2', 'cp1', 'honors')]
            print('   skill %02d  cp2=%2d cp1=%2d honors=%2d  total=%d%s' % (s, *row, sum(row), '  <-- THIN' if (s, row) in thin else ''))
        total += len(p['questions'])
    print('TOTAL', total)


if __name__ == '__main__':
    main(sys.argv[1:] or MODULES)
