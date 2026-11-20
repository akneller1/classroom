#!/usr/bin/env node
/* Grade 5 audit (2026-11-19), Classroom side of batch 5C.
   #7  the integration prefers the per-skill notes (worksheet-generator/grade5/skill-notes.js) when the source has them;
   #9, #15, #16  the practice tests, reference sheet, pacing guide and labs get cards, in the right sections;
   #1  Graphing Practice attaches to the Grade 5 units (the attach hook goes to the catalog the site loads);
   #19 the Grade 5 release is one setting (GRADE5_SOURCE_REF), and the deploy verifies the release before assembling it.
   With GRADE5_SOURCE_DIR, the per-skill notes are also built the way the integration builds them. */
'use strict';
const fs = require('fs'), vm = require('vm'), path = require('path'), assert = require('assert/strict');
const ROOT = path.resolve(__dirname, '..'), rd = (f) => fs.readFileSync(path.join(ROOT, f), 'utf8');
const integ = rd('scripts/integrate-approved-courses.mjs'), ci = rd('course-integrations.js');
assert.match(integ, /worksheet-generator\/grade5\/skill-notes\.js/, '#7 integration reads the per-skill notes');
assert.match(integ, /const own=\(skillNotes\[unit\.id\]\|\|\[\]\)\[i\];/, '#7 a skill uses its own note first');
assert.match(integ, /path\.join\(dst,"grade5-main-catalog\.js"\);fs\.appendFileSync/, '#1 attach hook appended to grade5/grade5-main-catalog.js');
assert.match(integ, /reference-sheet\/\.test\(item\.path\)\?'cheat-sheets'|cheat-sheet\|reference-sheet/, '#9 reference sheet is a study guide');
assert.match(integ, /practice-test-\[ab\]\\\/\/\.test\(item\.path\)\?'interactive-practice-test'/, '#9 practice tests are study guides');
assert.match(ci, /'decimal-operations':\['decimal-grid-lab'\]/); assert.match(ci, /'scaling-lab'\]/);
for (const p of ['math5-reference-sheet/reference-sheet.pdf', 'math5-pacing-guide/pacing-guide.pdf', "'math5-practice-test-'+x+'/exam.pdf'"]) assert.ok(ci.includes(p), 'course-integrations lists ' + p);
const deploy = rd('.github/workflows/deploy-site.yml');
assert.match(deploy, /\n  GRADE5_SOURCE_REF: [0-9a-f]{40}\n/, '#19 one Grade 5 release setting');
assert.match(deploy, /Check out approved Grade 5 course sources\n\s+uses: actions\/checkout@v4\n\s+with:\n\s+repository: akneller1\/FinancialAlgebra\n\s+ref: \$\{\{ env\.GRADE5_SOURCE_REF \}\}/, '#19 the Grade 5 checkout uses it');
assert.match(deploy, /verify\.py "\$PWD\/_course_sources\/grade5"\n\s+GRADE5_SOURCE_DIR=_course_sources\/grade5 node scripts\/test-grade5-audit\.cjs\n\s+node scripts\/test-grade5-plot\.cjs/, '#19 the deploy verifies the release');
assert.match(rd('.github/workflows/build-classroom-pages.yml'), /verify\.py "\$PWD\/grade5-source"/, '#19 the Classroom check runs the Grade 5 verifier');
let msg = 'static checks';
const src = path.resolve(process.env.GRADE5_SOURCE_DIR || path.join(ROOT, '..', 'FinancialAlgebra'));
const notesFile = path.join(src, 'worksheet-generator/grade5/skill-notes.js');
if (fs.existsSync(notesFile)) {
  const c = {}; c.window = c;
  vm.runInNewContext(fs.readFileSync(path.join(src, 'worksheet-generator/grade5/generators-content.js'), 'utf8'), c);
  vm.runInNewContext(fs.readFileSync(notesFile, 'utf8'), c);
  const units = Object.keys(c.G5_GENERATOR_CONTENT.units), ideas = new Set();
  for (const u of units) for (const n of c.G5_SKILL_NOTES[u] || []) { assert.ok(n.big && n.steps.length && n.watch.length === 2 && n.ask, u + ' note'); ideas.add(n.big); }
  assert.equal(units.length, 11); assert.equal(ideas.size, 55, 'a different key idea for each of the 55 skills');
  msg += '; 55 per-skill notes in the source';
} else msg += '; Grade 5 source without per-skill notes, note check skipped';
console.log('PASS Grade 5 audit 5C (Classroom): ' + msg);
