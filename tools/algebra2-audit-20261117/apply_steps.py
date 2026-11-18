"""Algebra 2 audit item 2: replace one-line or fragmentary solutions with full worked steps.

usage: python3 apply_steps.py steps/<unit>.json [...]
Each file maps question id → list of steps written for that question. A step list is only applied when it has at
least two steps and its final steps state the key (or, for multi-part and select-all items, every part / correct
choice); otherwise the id is reported and left unchanged. Idempotent.
"""
import json, re, sys, unicodedata
from lib import load, save, by_id

def norm(s):
    s = unicodedata.normalize('NFKC', str(s)).replace('−', '-').replace('–', '-')
    return re.sub(r'\s+', ' ', s).strip().rstrip('.').lower()

def states(steps, key):
    text = norm(' '.join(steps))
    k = norm(key)
    if k in text:
        return True
    # numbers of the key must all appear in the steps (handles "x = 4" vs "4", "$1,647.01" vs "1647.01")
    nums = re.findall(r'-?\d+(?:[.,/]\d+)*', k.replace(',', ''))
    if nums:
        return all(n in text.replace(',', '') for n in nums)
    # a worded key: most of its content words must appear in the steps
    words = [w for w in re.findall(r'[a-z]{4,}', k)]
    return bool(words) and sum(w in text for w in words) >= 0.6 * len(words)

B = load()
I = by_id(B)
bad, done = [], 0
for path in sys.argv[1:]:
    for qid, steps in json.load(open(path, encoding='utf-8')).items():
        q = I[qid]
        if not isinstance(steps, list) or len(steps) < 2 or not all(isinstance(s, str) and s.strip() for s in steps):
            bad.append((qid, 'needs at least two steps')); continue
        if q.get('parts'):
            keys = [p['answer'] for p in q['parts'] if isinstance(p.get('answer'), str)]
        elif q['format'] == 'select-all':
            keys = list(q['answer'])
        elif isinstance(q['answer'], str):
            keys = [q['answer']]
        else:
            keys = []
        missing = [k for k in keys if not states(steps, k)]
        if missing:
            bad.append((qid, 'steps never state ' + '; '.join(missing))); continue
        if q['solutionSteps'] != steps:
            q['solutionSteps'] = steps; done += 1
save(B)
print('applied', done)
for b in bad:
    print('SKIPPED', *b)
sys.exit(1 if bad else 0)
