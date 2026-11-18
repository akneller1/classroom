"""Precalculus audit #10: name the skill in every generic open-response stem. Idempotent."""
import json, subprocess, os
from lib import load, save, items, ROOT

names = json.loads(subprocess.run(['node', '-e', "require(process.argv[1]);const C=globalThis.MK_COURSE_CATALOG,o={};for(const u of require(process.argv[2]).banks.filter(b=>b.courseId==='precalculus'))C.getSkillRecords('precalculus',u.unitId).forEach(s=>o[s.id]=s.name);console.log(JSON.stringify(o))",
                                   os.path.join(ROOT, 'course-catalog.js'), os.path.join(ROOT, 'question-banks/manifest.json')], capture_output=True, text=True, check=True).stdout)
banks = load()
n = 0
for _, q in items(banks):
    if q['format'] == 'open-response' and q['prompt'].strip() == 'Answer each part. Show your work.':
        q['prompt'] = f"Practice set ({names[q['skillId']]}): answer each part and show your work."
        n += 1
save(banks)
print('stems', n)
