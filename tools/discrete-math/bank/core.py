"""Shared helpers for authoring the Discrete Math question banks.

Every question is built by a function that COMPUTES its answer (truth tables, set operations,
relation properties, counts, graph facts, election tallies, LP vertices) or is a hand-authored
conceptual item whose key was reviewed by hand. The helpers here only shape records to the
schema in schemas/question-bank.schema.json (no extra properties) and lint the text for the
site's math mini-syntax (core/math-display.js), which turns '-' into a minus sign, '/' into a
stacked fraction, '_' and '^' into sub/superscripts.
"""
import json, re, random, hashlib, itertools
from fractions import Fraction

COURSE = 'discrete'
LEVELS = ('cp2', 'cp1', 'honors')
NBH = '‑'  # non-breaking hyphen: shows as a hyphen, not a minus sign


def seeded(*parts):
    return random.Random(int(hashlib.sha256('|'.join(map(str, parts)).encode()).hexdigest()[:12], 16))


def fix_text(s):
    """Hyphen between two letters -> non-breaking hyphen so the renderer does not show a minus sign."""
    s = str(s)
    s = re.sub(r'\((\d)((?:-\d)+)\)', lambda m: '(' + m.group(0)[1:-1].replace('-', NBH) + ')', s)   # (3-2-1) point scales
    s = re.sub(r'(?<=[A-Za-z0-9])-(?=[A-Za-z])', NBH, s)
    return re.sub(r'(?<=[A-Za-z])-(?=[0-9])', NBH, s)


class DuplicatePrompt(Exception):
    pass


class Bank:
    def __init__(self, unit_id, abbr, n_skills):
        self.unit = unit_id
        self.abbr = abbr
        self.n_skills = n_skills
        self.q = []
        self.counter = {}
        self.family_seen = {}

    def sid(self, n):
        assert 1 <= n <= self.n_skills, n
        return '%s-skill-%02d' % (self.unit, n)

    def _id(self, skill, level):
        k = (skill, level)
        self.counter[k] = self.counter.get(k, 0) + 1
        return 'dm-%s-s%02d-%s-%03d' % (self.abbr, skill, level, self.counter[k])

    def _base(self, skill, level, fmt, prompt, answer, steps, family, notes=None):
        assert level in LEVELS, level
        if getattr(self, 'strict_unique', False) and any(q['prompt'] == fix_text(prompt).strip() for q in self.q):
            raise DuplicatePrompt(prompt)
        assert isinstance(steps, (list, tuple)) and steps, 'steps required'
        rec = {
            'id': self._id(skill, level),
            'skillId': self.sid(skill),
            'level': level,
            'format': fmt,
            'prompt': fix_text(prompt).strip(),
            'answer': answer,
            'solutionSteps': [fix_text(s) for s in steps],
            'sourceNotes': 'Original Claude-authored Discrete Math item (family: %s). %s' % (
                family, notes or 'Answer computed by the authoring script (tools/discrete-math/bank) and re-checked by verify_banks.py.'),
        }
        return rec

    def sa(self, skill, level, prompt, answer, steps, family, notes=None):
        a = str(answer)
        if isinstance(a, str) and family.endswith('_error'):
            a = fix_text(a)
        elif isinstance(a, str):
            assert not re.search(r'[A-Za-z]-[A-Za-z]', a), 'avoid letter hyphen in typed answer: ' + a
        r = self._base(skill, level, 'short-answer', prompt, a, steps, family, notes)
        self.q.append(r)
        return r

    def mc(self, skill, level, prompt, correct, distractors, steps, family, notes=None, order=None):
        correct = fix_text(correct)
        ds = []
        for d in distractors:
            d = fix_text(d)
            if d != correct and d not in ds:
                ds.append(d)
        if len(ds) < 3 and re.fullmatch(r'-?\d+', correct):
            n = int(correct)
            for x in (n + 1, n - 1, n + 2, 2 * n + 1, n + 10):
                if str(x) != correct and str(x) not in ds and len(ds) < 3:
                    ds.append(str(x))
        assert len(ds) >= 3, ('need 3 distinct distractors', prompt, correct, distractors)
        ds = ds[:3] if len(ds) > 3 and order is None else ds
        opts = [{'text': correct, 'correct': True}] + [{'text': d, 'correct': False} for d in ds]
        rng = seeded(self.unit, skill, level, prompt)
        if order == 'keep':
            pass
        elif order == 'sort':
            opts.sort(key=lambda o: _sortkey(o['text']))
        else:
            rng.shuffle(opts)
        r = self._base(skill, level, 'multiple-choice', prompt, correct, steps, family, notes)
        r['options'] = opts
        self.q.append(r)
        return r

    def sel(self, skill, level, prompt, options, steps, family, notes=None, shuffle=True):
        """options: list of (text, bool)."""
        opts = [{'text': fix_text(t), 'correct': bool(c)} for t, c in options]
        texts = [o['text'] for o in opts]
        assert len(set(texts)) == len(texts), ('duplicate options', prompt)
        n = sum(o['correct'] for o in opts)
        assert n >= 2 and len(opts) - n >= 1 and len(opts) >= 4, ('select-all needs >=2 correct, >=1 wrong', prompt)
        if shuffle:
            seeded(self.unit, skill, level, prompt).shuffle(opts)
        prompt = prompt if 'Select ALL' in prompt or 'Select all' in prompt else prompt + ' Select ALL that apply.'
        r = self._base(skill, level, 'select-all', prompt, [o['text'] for o in opts if o['correct']], steps, family, notes)
        r['options'] = opts
        self.q.append(r)
        return r

    def orq(self, skill, level, prompt, parts, steps, family, notes=None, answer=None):
        assert len(parts) >= 4, 'open response needs 4+ parts'
        ps = [{'prompt': fix_text(p), 'answer': a if isinstance(a, (int, float)) else fix_text(a)} for p, a in parts]
        ans = answer or ' | '.join('(%s) %s' % (chr(97 + i), p['answer']) for i, p in enumerate(ps))
        r = self._base(skill, level, 'open-response', prompt, fix_text(ans), steps, family, notes)
        r['parts'] = ps
        self.q.append(r)
        return r

    def err(self, skill, level, problem, student, work, correct, mistake, explanation, fix_steps, family,
            ask=None):
        """Error analysis item in the site's existing authored format: a short-answer record whose prompt shows
        the student's incorrect work, whose answer is the corrected result, whose first solution step starts
        with 'Mistake:', and whose sourceNotes family ends in _error (worksheet-generator/algebra2-bank-native.js)."""
        assert family.endswith('_error')
        lines = [problem, '%s\'s work:' % student] + ['  ' + w for w in work]
        lines.append(ask or '(a) Identify the error and explain why it is wrong. (b) Correct the work and give the correct answer.')
        steps = ['Mistake: ' + mistake, 'Why it matters: ' + explanation] + list(fix_steps) + ['Correct answer: %s' % correct]
        return self.sa(skill, level, '\n'.join(lines), correct, steps, family,
                       notes='Intentional error checked by verify_banks.py: the student\'s result differs from the computed key.')

    def image(self, rec, src, alt):
        rec['diagram'] = {'type': 'image', 'spec': {'src': src, 'alt': fix_text(alt)}}
        return rec

    def payload(self):
        return {'schemaVersion': 1, 'courseId': COURSE, 'unitId': self.unit, 'questions': self.q}


def _sortkey(t):
    try:
        return (0, float(str(t).replace('−', '-')), t)
    except ValueError:
        return (1, 0, t)


# ---------------------------------------------------------------- formatting helpers
def fmt_set(s, empty='∅'):
    s = list(s)
    if not s:
        return empty
    try:
        s = sorted(s)
    except TypeError:
        s = sorted(s, key=str)
    return '{' + ', '.join(fmt_el(x) for x in s) + '}'


def fmt_el(x):
    if isinstance(x, tuple):
        return '(' + ', '.join(fmt_el(y) for y in x) + ')'
    if isinstance(x, frozenset):
        return fmt_set(x)
    return str(x)


def fmt_pairs(R):
    return fmt_set(R)


def frac(x):
    x = Fraction(x)
    return str(x.numerator) if x.denominator == 1 else '%d/%d' % (x.numerator, x.denominator)


def tv(b):
    return 'T' if b else 'F'


def ordinal(n):
    return '%d%s' % (n, 'th' if 10 <= n % 100 <= 20 else {1: 'st', 2: 'nd', 3: 'rd'}.get(n % 10, 'th'))


def write(path, payload):
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(payload, f, ensure_ascii=False, indent=1)
        f.write('\n')
