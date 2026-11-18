"""Load and save the Calculus question banks without changing their formatting (indent=1)."""
import json, glob, os, re

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
BANKS = os.path.join(ROOT, 'question-banks', 'calculus')
UNITS = ['precalculus-review', 'limits-continuity', 'derivatives', 'applications-derivatives',
         'antiderivatives-definite-integrals', 'fundamental-theorem-calculus', 'applications-integrals',
         'differential-equations', 'ap-review']


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
    m = re.search(r'family: ([^)]+)\)', q.get('sourceNotes', ''))
    return m.group(1) if m else None


def tags():
    return {u: json.load(open(os.path.join(BANKS, 'meta', u + '.tags.json'), encoding='utf-8')) for u in UNITS}
