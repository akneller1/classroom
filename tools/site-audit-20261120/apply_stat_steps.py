"""Site audit #19 (2026-11-20): fuller worked solutions for one-step Statistics items.
Hand-written steps live in stat-steps/b*.json as {id: [before, after]}; the bank's own step goes in between.
Error-analysis items get: locate the wrong step, the item's rule, then the fix. Re-running is a no-op."""
import json, glob, os, re
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(os.path.dirname(HERE))

CP1_CUT = 60  # cp1 term items shorter than this drop the closing restatement too (keeps the S2 level spacing)
S = {}
for f in sorted(glob.glob(os.path.join(HERE, 'stat-steps', 'b*.json'))): S.update(json.load(open(f)))
def dot(t): t = t.strip(); return t if re.search(r'[.!?”"]$', t) else t + '.'
changed = left = 0
for f in sorted(glob.glob(os.path.join(ROOT, 'question-banks/statistics/*.json'))):
    raw = open(f).read(); d = json.loads(raw); n = 0
    for q in d['questions']:
        s = q.get('solutionSteps') or []
        if len(s) > 1: continue
        if q['id'] in S:
            a, b = S[q['id']]
            if len(b) < 45 and len(q['prompt']) < {'cp2': 90, 'cp1': CP1_CUT}.get(q.get('level'), 0): b = ''  # short CP term items: the closing line only restates the answer
            new = [x for x in [a, *s, b] if x]
        elif q['prompt'].startswith('Error analysis'):
            ans = str(q['answer']); m = re.match(r'Step (\d+): ?(.*)', ans, re.S)
            body = q['prompt'].split('\n')
            if m:
                k = m.group(1); wrong = next((l for l in body if l.startswith(f'Step {k}:')), None)
                first = f'Check each step. Step {k} is wrong: “{wrong.split(":", 1)[1].strip()}”' if wrong else f'Check each step. The error is in Step {k}.'
                fix = m.group(2)
            else:
                claim = ' '.join(l for l in body[1:] if not l.startswith('Find and fix')).strip() or body[0].replace('Error analysis.', '').strip()
                first = f'Find the mistake in the student’s work: {dot(claim)}'; fix = ans
            new = [dot(first), *s, 'Fix: ' + dot(fix[0].upper() + fix[1:] if re.match('[a-z]', fix) else fix)]
        else:
            left += 1; continue
        q['solutionSteps'] = new; n += 1
        if q.get('level') == 'cp2' and not q.get('hint'):  # S2 rule: multi-step CP2 items carry a first-step hint
            h = new[0]; q['hint'] = 'First step: ' + (h[0].lower() + h[1:] if re.match('[A-Z][a-z ]', h) else h)
    if n:
        open(f, 'w').write(json.dumps(d, ensure_ascii=False, indent=1 if raw.startswith('{\n "') else 2) + ('\n' if raw.endswith('\n') else ''))
        changed += n
print('statistics steps added:', changed, 'still one step:', left)
