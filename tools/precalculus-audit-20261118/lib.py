"""Load and save the Precalculus question banks without changing their formatting (indent=1, no trailing newline)."""
import json, glob, os

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
BANKS = os.path.join(ROOT, 'question-banks', 'precalculus')


def load():
    out = {}
    for f in sorted(glob.glob(os.path.join(BANKS, '*.json'))):
        raw = open(f, encoding='utf-8').read()
        out[f] = (json.loads(raw), raw)
    return {f: d for f, (d, _) in out.items()}


def save(banks):
    for f, d in banks.items():
        raw = open(f, encoding='utf-8').read()
        ind = 1 if raw.startswith('{\n "') else (2 if raw.startswith('{\n  "') else None)
        txt = json.dumps(d, ensure_ascii=False, indent=ind) + ('\n' if raw.endswith('\n') else '')
        if txt != raw:
            open(f, 'w', encoding='utf-8').write(txt)


def items(banks):
    for f, d in banks.items():
        for q in d['questions']:
            yield f, q
