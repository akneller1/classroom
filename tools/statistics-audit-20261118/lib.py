"""Load and save the Statistics question banks without changing their formatting (indent=1, trailing newline)."""
import json, os, re

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
BANKS = os.path.join(ROOT, 'question-banks', 'statistics')
UNITS = ['exploring-data', 'sampling-experimentation', 'anticipating-patterns', 'statistical-inference']


def path(unit):
    return os.path.join(BANKS, unit + '.json')


def load():
    return {u: json.load(open(path(u), encoding='utf-8')) for u in UNITS}


def save(banks):
    for u, d in banks.items():
        txt = json.dumps(d, ensure_ascii=False, indent=1) + '\n'
        if txt != open(path(u), encoding='utf-8').read():
            open(path(u), 'w', encoding='utf-8').write(txt)


def items(banks):
    for u, d in banks.items():
        for q in d['questions']:
            yield u, q


def family(q):
    m = re.search(r'family: ([^)]+)\)', q.get('sourceNotes', ''))
    if m:
        return m.group(1)
    m = re.search(r'skill: ([^.;]+)', q.get('sourceNotes', ''))
    return 'src:' + m.group(1) if m else None


def key_text(q):
    if q['format'] == 'multiple-choice':
        return [o['text'] for o in q['options'] if o['correct']][0]
    a = q['answer']
    return '; '.join(a) if isinstance(a, list) else str(a)
