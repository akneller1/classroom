#!/usr/bin/env python3
"""Add partner-check companion questions to the approved question banks.

Each companion is a NEW short-answer item whose answer string is copied from an existing item (its partner)
at the same level, so the Partner Check generator can pair two different problems with the same answer.
Existing questions, IDs, answers, diagrams and manifest approval flags are never modified.

    python3 tools/partner-check-companions-20261107/apply.py          # check + write
    python3 tools/partner-check-companions-20261107/apply.py --check  # check only
"""
import json, re, sys, pathlib, collections
ROOT = pathlib.Path(__file__).resolve().parents[2]
sys.path.insert(0, str(pathlib.Path(__file__).parent))
import companions_a2, companions_other
ITEMS = companions_a2.ITEMS + companions_other.ITEMS
NOTE = ('Partner-check companion to {p} (same answer, different problem). Claude-authored 2026-11-07; '
        'answer re-derived independently in tools/partner-check-companions-20261107. Awaiting human review.')

def plain(s): return re.sub(r'\\[a-zA-Z]+', '', s)

def main(write):
    by_bank = collections.defaultdict(list)
    for it in ITEMS: by_bank[it['bank']].append(it)
    errors, added = [], 0
    for bank, items in by_bank.items():
        path = ROOT / 'question-banks' / (bank + '.json')
        text = path.read_text(encoding='utf8')
        data = json.loads(text)
        indent = 2 if text.startswith('{\n  "') else 1
        qs = data['questions']; ids = {q['id']: q for q in qs}
        prompts = {q['prompt'].strip().lower() for q in qs if not q['id'].count('-pc')}
        counters = collections.Counter()
        for q in qs:
            m = re.match(r'(.*)-pc(\d+)$', q['id'])
            if m: counters[m.group(1)] = max(counters[m.group(1)], int(m.group(2)))
        for it in items:
            p = ids.get(it['partner'])
            if not p: errors.append(f"{bank}: missing partner {it['partner']}"); continue
            if p['format'] not in ('short-answer', 'multiple-choice'): errors.append(f"{it['partner']}: partner is {p['format']}")
            if not it['check'](): errors.append(f"{bank}: check failed for companion of {it['partner']}: {it['prompt']}")
            if it['prompt'].strip().lower() in prompts: errors.append(f"{it['partner']}: prompt repeats an existing question")
            if len(plain(it['prompt'])) > 170: errors.append(f"{it['partner']}: prompt too long for a partner-check box")
            ans = p['answer'] if isinstance(p['answer'], str) else None
            if ans is None or len(plain(ans)) > 40: errors.append(f"{it['partner']}: unsuitable answer")
            skill = it.get('skill', p['skillId'])
            sn = re.search(r'skill-(\d+)$', skill).group(1)
            stem = re.sub(r'-s\d+-', f'-s{sn}-', p['id'].rsplit('-', 1)[0])
            std = it.get('standards') or (p['standards'] if skill == p['skillId'] else
                   next(q['standards'] for q in qs if q['skillId'] == skill and q['level'] == p['level']))
            existing = [q for q in qs if q.get('sourceNotes', '').startswith(f"Partner-check companion to {p['id']} ") and q['prompt'] == it['prompt']]
            if existing: continue                      # already applied (idempotent)
            counters[stem] += 1
            nid = f"{stem}-pc{counters[stem]:02d}"
            if nid in ids: errors.append(f'duplicate id {nid}'); continue
            q = {'id': nid, 'skillId': skill, 'level': p['level'], 'format': 'short-answer', 'prompt': it['prompt'],
                 'answer': ans, 'solutionSteps': it['steps'], 'standards': std, 'sourceNotes': NOTE.format(p=p['id'])}
            qs.append(q); ids[nid] = q; prompts.add(it['prompt'].strip().lower()); added += 1
        if write and not errors:
            out = json.dumps(data, indent=indent, ensure_ascii=False) + ('\n' if text.endswith('\n') else '')
            path.write_text(out, encoding='utf8')
    if errors:
        print('\n'.join(errors)); sys.exit(1)
    print(f'OK {len(ITEMS)} companions checked; {added} new questions ' + ('written' if write else '(not written)'))

if __name__ == '__main__':
    main('--check' not in sys.argv)
