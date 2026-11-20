"""Statistics audit batch S2 (2026-11-18): add the free-response problems (#2), the design diagrams and shaded-Normal items (#9)
and the items that bring every skill-and-level set to at least 24 (#20).
The nine "Answer each part. Show your work." mixed-review items (Inference skills 12–14) are replaced in place by that skill's
free-response problem, so their ids stay. Every other item is new and listed in added-s2.json. Rerunning removes the batch's
items first and rebuilds them, so the result is deterministic."""
import json, os, random, re, shutil, subprocess, sys
sys.path.insert(0, os.path.dirname(__file__))
import lib
import s2diagrams
from s2common import LEVELS, UNIT_NO, UNIT_OF, NOTE, item, mc
from s2fill import FAM
from s2frq import T

TARGET = 24
HERE = os.path.dirname(__file__)
GENERIC = {f'stat-u4-s{k}-{lv}-015' for k in (12, 13, 14) for lv in LEVELS}
TAG = 'batch S2'


def skill_names():
    js = ('const fs=require("fs"),vm=require("vm");const g={window:{}};for(const p of ["data.js","course-catalog.js"])vm.runInNewContext(fs.readFileSync(p,"utf8"),g);'
          'const C=g.window.MK_COURSE_CATALOG,o={};for(const u of %s)for(const s of C.getSkillRecords("statistics",u))o[s.id]=s.name;console.log(JSON.stringify(o))') % json.dumps(lib.UNITS)
    return json.loads(subprocess.run(['node', '-e', js], cwd=lib.ROOT, capture_output=True, text=True, check=True).stdout)


def frq_item(qid, unit_no, k, lv, name, rng):
    stem, parts, codes, _ = T[(unit_no, k)](rng, lv)
    labels = 'abcd'
    assert len(parts) == 4, (unit_no, k)
    assert any(re.search(r'\b(Justify|Explain|explain|justify|Interpret|interpret)\b', p[0]) for p in parts), (unit_no, k)
    steps, total = [], 0
    for lab, (pr, ans, sol, pts, score) in zip(labels, parts):
        steps.append(f'({lab}) {sol}')
        steps.append(f'({lab}) Scoring, {pts} point{"s" if pts > 1 else ""}: {score}')
        total += pts
    steps.append(f'Total: {total} points.')
    q = {'id': qid, 'skillId': f'{UNIT_OF[unit_no]}-skill-{k:02d}', 'level': lv, 'format': 'open-response',
         'prompt': f'Free response ({name}). {stem}',
         'answer': '; '.join(f'({lab}) {p[1]}' for lab, p in zip(labels, parts)),
         'parts': [{'label': lab, 'prompt': p[0], 'answer': p[1]} for lab, p in zip(labels, parts)],
         'solutionSteps': steps, 'standards': ['APSTATS.' + c for c in codes],
         'sourceNotes': NOTE.format(fam=f'frq_{T[(unit_no, k)].__name__}')}
    return q


def main():
    banks = lib.load()
    names = skill_names()
    shutil.rmtree(os.path.join(lib.ROOT, s2diagrams.REL), ignore_errors=True)
    # remove this batch's earlier output (rebuild in place)
    for u in lib.UNITS:
        # also drop the objective-gap items (gap_items.py runs next and writes them again), so the fill to TARGET
        # always counts the same items and a rerun reproduces the banks exactly
        banks[u]['questions'] = [q for q in banks[u]['questions'] if (TAG not in q.get('sourceNotes', '') or q['id'] in GENERIC)
                                 and 'objective gaps 2026-11-19' not in q.get('sourceNotes', '')]
    # the nine replaced-in-place items are rebuilt below, so their current text does not count as taken
    prompts = {(q['skillId'], q['prompt']) for _, q in lib.items(banks) if q['id'] not in GENERIC}
    allp = {q['prompt'] for _, q in lib.items(banks) if q['id'] not in GENERIC}
    added = []
    for u in lib.UNITS:
        un = UNIT_NO[u]
        qs = banks[u]['questions']
        idx = {q['id']: i for i, q in enumerate(qs)}
        ks = sorted({int(re.search(r'skill-(\d+)', q['skillId']).group(1)) for q in qs})
        for k in ks:
            sid = f'{u}-skill-{k:02d}'
            for lv in LEVELS:
                # ---- #2 free response
                rng = random.Random(f'frq-{un}-{k}-{lv}')
                old = f'stat-u{un}-s{k}-{lv}-015'
                qid = old if old in GENERIC else f'stat-u{un}-s{k:02d}-{lv}-f01'
                for _ in range(50):
                    q = frq_item(qid, un, k, lv, names[sid], rng)
                    if (sid, q['prompt']) not in prompts:
                        break
                prompts.add((sid, q['prompt'])); allp.add(q['prompt'])
                if qid in idx:
                    qs[idx[qid]] = q
                else:
                    qs.append(q); added.append(qid)
                # ---- #20 fill to TARGET
                have = sum(1 for x in qs if x['skillId'] == sid and x['level'] == lv)
                fams = FAM.get((un, k), [])
                rng = random.Random(f'fill-{un}-{k}-{lv}')
                n, tries = 0, 0
                while have < TARGET:
                    assert fams and tries < 3000, (sid, lv, have)
                    tries += 1
                    fn = fams[(n + tries) % len(fams)]
                    r = fn(rng, lv)
                    if not r or (sid, r['prompt']) in prompts or r['prompt'] in allp:
                        continue
                    n += 1
                    qid = f'stat-u{un}-s{k:02d}-{lv}-g{n:02d}'
                    diagram = None
                    if r.get('design'):
                        diagram = s2diagrams.design(qid, r['design'])
                    elif r.get('normal'):
                        diagram = s2diagrams.normal(qid, r['normal'])
                    q = item(qid, un, k, lv, r['fmt'], r['prompt'], r['answer'], r['steps'], r['codes'], 's2_' + fn.__name__, rng=rng, wrong=r.get('wrong'), diagram=diagram)
                    qs.append(q); added.append(qid)
                    prompts.add((sid, r['prompt'])); allp.add(r['prompt'])
                    have += 1
    lib.save(banks)
    json.dump(sorted(added), open(os.path.join(HERE, 'added-s2.json'), 'w'), indent=1)
    open(os.path.join(HERE, 'added-s2.json'), 'a').write('\n')
    print('S2 items:', len(added), 'new;', len(GENERIC), 'replaced in place')


if __name__ == '__main__':
    main()
