"""Shared helpers for the Grade 6 audit scripts (2026-11-19). Banks are saved exactly as the repository stores them:
indent 1, Unicode kept as is, and the trailing newline each file already has; tags files use indent 0."""
import glob, json, os, re

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
BANKS = os.path.join(ROOT, 'question-banks', 'math6')
HERE = os.path.dirname(os.path.abspath(__file__))
UNITS = ['ratios-rates-percent-proportions', 'fractions-decimals-operations', 'rational-numbers', 'expressions-equations',
         'inequalities', 'geometry', 'data-displays']
ABBR = {'ratios-rates-percent-proportions': 'rrp', 'fractions-decimals-operations': 'fdo', 'rational-numbers': 'rat',
        'expressions-equations': 'exq', 'inequalities': 'ineq', 'geometry': 'geo', 'data-displays': 'dd'}
_NL = {}


def path(unit):
    return os.path.join(BANKS, unit + '.json')


def load():
    out = {}
    for u in UNITS:
        raw = open(path(u), encoding='utf-8').read()
        _NL[u] = raw.endswith('\n')
        out[u] = json.loads(raw)
    return out


def save(banks):
    for u, b in banks.items():
        txt = json.dumps(b, indent=1, ensure_ascii=False) + ('\n' if _NL.get(u, True) else '')
        open(path(u), 'w', encoding='utf-8').write(txt)


def items(banks):
    for u in UNITS:
        for q in banks[u]['questions']:
            yield u, q


def load_tags():
    return {u: json.load(open(os.path.join(BANKS, 'meta', u + '.tags.json'), encoding='utf-8')) for u in UNITS}


def save_tags(tags):
    for u, t in tags.items():
        open(os.path.join(BANKS, 'meta', u + '.tags.json'), 'w', encoding='utf-8').write(json.dumps(t, indent=0, ensure_ascii=False))


def skill_names():
    m = json.load(open(os.path.join(ROOT, 'docs', 'math6', 'SKILL_MANIFEST.json'), encoding='utf-8'))
    return {s['skillId']: s['name'] for u in m['units'] for s in u['skills']}


def skill_no(q):
    return int(q['skillId'].rsplit('-', 1)[1])


SOURCE = ('Original Claude-authored item (Grade 6 audit 2026-11-19, family: {fam}). Answer computed in the authoring script '
          'and re-checked from the printed prompt by tools/grade6-audit-20261119/verify_keys.py.')
