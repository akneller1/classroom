"""Shared helpers for the 3rd Grade Math audit (2026-11-19).

Grade 3 content comes from a pinned FinancialAlgebra release, so every fix here becomes a Classroom overlay:
content-updates/2026-11-19/grade3/<unit>.json holds guarded edits (from/to per field), new questions and their
player metadata. scripts/apply-grade3-audit.mjs applies it at deploy to both bank copies. The builders read the
assembled site (after apply-content-updates and apply-kid-friendly) from G3_BASE so every "from" value matches."""
import json, os, re
from fractions import Fraction as Fr

BASE = os.environ.get('G3_BASE', '/home/claude/site-base3')
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
OUT = os.path.join(ROOT, 'content-updates', '2026-11-19', 'grade3')
UNITS = ['multiplication-meaning', 'division-meaning', 'properties-fact-strategies', 'patterns-unknowns-two-step',
         'addition-subtraction-1000', 'understanding-fractions', 'equivalent-comparing-fractions', 'time-volume-mass',
         'graphs-measurement-data', 'area', 'perimeter-shapes']
ABBR = {'multiplication-meaning': 'mm', 'division-meaning': 'dv', 'properties-fact-strategies': 'pf', 'patterns-unknowns-two-step': 'up',
        'addition-subtraction-1000': 'as', 'understanding-fractions': 'uf', 'equivalent-comparing-fractions': 'ec', 'time-volume-mass': 'tm',
        'graphs-measurement-data': 'gd', 'area': 'ar', 'perimeter-shapes': 'ps'}


def load_base():
    banks = {u: json.load(open(os.path.join(BASE, 'question-banks', 'grade3', u + '.json'), encoding='utf-8')) for u in UNITS}
    meta = {u: json.load(open(os.path.join(BASE, 'grade3', 'question-banks', 'math3', 'meta', u + '.meta.json'), encoding='utf-8')) for u in UNITS}
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
