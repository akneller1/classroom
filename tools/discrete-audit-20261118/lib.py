"""Discrete Math audit (2026-11-18): load and save the banks without changing their formatting (indent=1)."""
import json, os, re

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
BANKS = os.path.join(ROOT, 'question-banks', 'discrete')
UNITS = ['speaking-mathematically', 'compound-statements-logic', 'number-theory-proof', 'sequences-induction-recursion',
         'set-theory', 'properties-relations', 'counting-probability', 'graphs-trees', 'election-theory', 'linear-programming']


def path(unit):
    return os.path.join(BANKS, unit + '.json')


def load():
    return {u: json.load(open(path(u), encoding='utf-8')) for u in UNITS}


def save(banks):
    for u, d in banks.items():
        f = path(u)
        raw = open(f, encoding='utf-8').read()
        txt = json.dumps(d, ensure_ascii=False, indent=1) + ('\n' if raw.endswith('\n') else '')
        if txt != raw:
            open(f, 'w', encoding='utf-8').write(txt)


def items(banks):
    for u, d in banks.items():
        for q in d['questions']:
            yield u, q


def family(q):
    m = re.search(r'family: ([a-z0-9_-]+)\)', q.get('sourceNotes', ''))
    return m.group(1) if m else ''


def set_family(q, fam):
    note = q.get('sourceNotes', '')
    if 'family:' in note:
        q['sourceNotes'] = re.sub(r'family: [a-z0-9_]*\)', 'family: ' + fam + ')', note)
    else:
        q['sourceNotes'] = (note + ' ' if note else '') + '(family: ' + fam + ')'
