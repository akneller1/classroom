"""Load and save the Algebra 2 question banks without changing their formatting."""
import json, glob, os

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
BANKS = os.path.join(ROOT, 'question-banks', 'algebra2')


def load():
    out = {}
    for f in sorted(glob.glob(os.path.join(BANKS, '*.json'))):
        out[f] = json.load(open(f, encoding='utf-8'))
    return out


def save(banks):
    for f, d in banks.items():
        with open(f, 'w', encoding='utf-8') as fh:
            fh.write(json.dumps(d, ensure_ascii=False, indent=1))


def items(banks):
    for f, d in banks.items():
        for q in d['questions']:
            yield f, q


def by_id(banks):
    return {q['id']: q for _, q in items(banks)}


def text_fields(q):
    """(getter, setter) pairs for every student- or teacher-visible string of a question."""
    refs = []

    def ref(obj, key):
        refs.append((lambda: obj[key], lambda v: obj.__setitem__(key, v)))

    ref(q, 'prompt')
    if isinstance(q['answer'], str):
        ref(q, 'answer')
    elif isinstance(q['answer'], list):
        for i in range(len(q['answer'])):
            if isinstance(q['answer'][i], str):
                ref(q['answer'], i)
    for i in range(len(q.get('solutionSteps', []))):
        ref(q['solutionSteps'], i)
    for o in q.get('options', []):
        ref(o, 'text')
    for p in q.get('parts', []):
        if isinstance(p.get('prompt'), str):
            ref(p, 'prompt')
        if isinstance(p.get('answer'), str):
            ref(p, 'answer')
    return refs
