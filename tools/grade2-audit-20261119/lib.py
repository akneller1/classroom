"""Shared helpers for the 2nd Grade Math audit (2026-11-19).

Grade 2 content comes from a pinned FinancialAlgebra release, so every fix here becomes a Classroom overlay:
content-updates/2026-11-19/grade2/<unit>.json holds guarded edits (from/to per field), new questions and their
player metadata. scripts/apply-grade2-audit.mjs applies it at deploy to both bank copies. The builders read the
assembled site (after apply-content-updates and apply-kid-friendly) from G2_BASE so every "from" value matches."""
import json, os, re
from fractions import Fraction as Fr

BASE = os.environ.get('G2_BASE', '/home/claude/site-base2')
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
OUT = os.path.join(ROOT, 'content-updates', '2026-11-19', 'grade2')
UNITS = ['add-subtract-20', 'add-subtract-100', 'word-problems-100', 'place-value-1000', 'count-compare-1000', 'add-subtract-1000',
         'odd-even-arrays', 'measuring-length', 'length-number-line', 'time-money', 'graphs-data', 'shapes-equal-shares']
ABBR = {'add-subtract-20': 'af', 'add-subtract-100': 'ah', 'word-problems-100': 'wp', 'place-value-1000': 'pv', 'count-compare-1000': 'cc',
        'add-subtract-1000': 'at', 'odd-even-arrays': 'oe', 'measuring-length': 'ml', 'length-number-line': 'ln', 'time-money': 'tm',
        'graphs-data': 'gd', 'shapes-equal-shares': 'sh'}


def load_base():
    banks = {u: json.load(open(os.path.join(BASE, 'question-banks', 'grade2', u + '.json'), encoding='utf-8')) for u in UNITS}
    meta = {u: json.load(open(os.path.join(BASE, 'grade2', 'question-banks', 'math2', 'meta', u + '.meta.json'), encoding='utf-8')) for u in UNITS}
    return banks, meta


def mask(s):
    return re.sub(r'-?\d+(?:,\d{3})*(?:\.\d+)?', '#', s)


def family(q):
    m = re.search(r'family: ([\w-]+)', q.get('sourceNotes', ''))
    return m.group(1) if m else ''


def F(x):
    x = Fr(x)
    if x.denominator == 1:
        return f'{x.numerator:,}'
    w, r = divmod(x.numerator, x.denominator)
    return f'{w} {r}/{x.denominator}' if w else f'{r}/{x.denominator}'


def frac(x):
    """a/b without converting to a mixed number"""
    x = Fr(x)
    return str(x.numerator) if x.denominator == 1 else f'{x.numerator}/{x.denominator}'


def n(x):
    return f'{x:,}'


def mc(ans, wrong, seed=0):
    out, seen = [], set()
    for t in [ans] + list(wrong):
        if t not in seen:
            seen.add(t); out.append(t)
    assert len(out) >= 4, (ans, wrong)
    out = out[:4]
    k = (sum(map(ord, ans)) + seed) % 4
    out.remove(ans); out.insert(k, ans)
    return [{'text': t, 'correct': t == ans} for t in out]


class Overlay:
    def __init__(self, banks, meta):
        self.banks, self.meta = banks, meta
        self.byid = {q['id']: (u, q) for u, b in banks.items() for q in b['questions']}
        self.edits = {u: {} for u in UNITS}
        self.adds = {u: [] for u in UNITS}
        self.newmeta = {u: {} for u in UNITS}

    def cur(self, qid, field):
        u, q = self.byid[qid]
        e = self.edits[u].get(qid, {})
        return e[field]['to'] if field in e else q.get(field)

    def edit(self, qid, **fields):
        u, q = self.byid[qid]
        e = self.edits[u].setdefault(qid, {})
        for k, v in fields.items():
            if k in e:
                e[k]['to'] = v
            else:
                e[k] = {'from': q.get(k), 'to': v}
            if e[k]['from'] == e[k]['to']:
                del e[k]
        if not e:
            del self.edits[u][qid]

    def meta_set(self, qid, **fields):
        """override player metadata (feedback, distractors) for an existing item whose content changed"""
        u, q = self.byid[qid]
        m = dict(self.newmeta[u].get(qid) or self.meta[u].get(qid) or {})
        m.update(fields)
        self.newmeta[u][qid] = m

    def add(self, unit, q, meta=None):
        assert q['id'] not in self.byid and all(x['id'] != q['id'] for x in self.adds[unit]), q['id']
        self.adds[unit].append(q)
        if meta:
            self.newmeta[unit][q['id']] = meta

    def items(self, unit=None):
        """current view of every question (base + edits + additions)"""
        for u in ([unit] if unit else UNITS):
            for q in self.banks[u]['questions']:
                e = self.edits[u].get(q['id'], {})
                yield dict(q, **{k: v['to'] for k, v in e.items()})
            for q in self.adds[u]:
                yield q

    def write(self, extra=None):
        os.makedirs(OUT, exist_ok=True)
        for u in UNITS:
            d = {'unit': u, 'edits': [{'id': k, 'changes': v} for k, v in sorted(self.edits[u].items())],
                 'additions': self.adds[u], 'meta': self.newmeta[u]}
            with open(os.path.join(OUT, u + '.json'), 'w', encoding='utf-8') as fh:
                json.dump(d, fh, ensure_ascii=False, indent=1)
                fh.write('\n')
        if extra:
            with open(os.path.join(OUT, 'course.json'), 'w', encoding='utf-8') as fh:
                json.dump(extra, fh, ensure_ascii=False, indent=1)
                fh.write('\n')
