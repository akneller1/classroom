'use strict';
// Precalculus audit #4 (2026-11-18): standards-gap skills. Each has 16 items per level (6+ multiple choice,
// 2+ find-the-mistake), the right standard tags, teaching notes, and its standards appear in the standards map.
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');
const ROOT = path.join(__dirname, '..');
const dir = path.join(ROOT, 'question-banks/precalculus');
const banks = fs.readdirSync(dir).filter((f) => f.endsWith('.json')).map((f) => JSON.parse(fs.readFileSync(path.join(dir, f), 'utf8')));
const items = banks.flatMap((b) => b.questions.map((q) => ({ ...q, unit: b.unitId })));
const w = {}; w.window = w; vm.createContext(w);
for (const f of ['course-catalog.js', 'worksheet-generator/planner/notes-teach-precalculus.js']) vm.runInContext(fs.readFileSync(path.join(ROOT, f), 'utf8'), w);
const NEW = [
  ['functions', 19, 'Rational Expressions and Partial Fractions', 'A-APR.D.7'],
  ['functions', 20, 'Verifying Inverses and Restricting Domains', 'F-BF.B.4c'],
  ['vectors', 12, 'Complex Conjugates, Moduli, and Quotients', 'N-CN.A.3'],
  ['vectors', 13, 'Products, Powers, and Roots in Polar Form', 'N-CN.B.5'],
  ['vectors', 14, 'Limaçons and Cardioids', 'APPC.3.14'],
  ['sequences-series-limits', 6, 'The Binomial Theorem', 'A-APR.C.5'],
  ['sequences-series-limits', 7, 'Continuity and One-Sided Limits', 'F-IF.C.7d'],
];
for (const [unit, n, name, std] of NEW) {
  const id = `${unit}-skill-${String(n).padStart(2, '0')}`;
  assert.equal(w.MK_COURSE_CATALOG.getSkills('precalculus', unit)[n - 1], name, id + ' name');
  const qs = items.filter((q) => q.skillId === id);
  for (const lv of ['cp2', 'cp1', 'honors']) {
    const at = qs.filter((q) => q.level === lv);
    assert(at.length >= 16, `${id} ${lv}: ${at.length}`);
    assert(at.filter((q) => q.format === 'multiple-choice').length >= 6, `${id} ${lv} multiple choice`);
    assert(at.filter((q) => /answered this problem incorrectly/.test(q.prompt)).length >= 2, `${id} ${lv} find the mistake`);
  }
  assert(qs.every((q) => q.standards.includes(std)), id + ' tagged ' + std);
  assert(qs.every((q) => Array.isArray(q.solutionSteps) && q.solutionSteps.length >= 2), id + ' worked solutions');
  const single = qs.filter((q) => q.format !== 'open-response');
  assert(new Set(single.map((q) => q.prompt)).size === single.length, id + ' prompts are distinct');
  const notes = w.MKPLAN_TEACH.precalculus[id];
  assert(notes && notes.obj && notes.cards.length, id + ' teaching notes');
}
// The verifier recorded and passed every new item.
const checks = JSON.parse(fs.readFileSync(path.join(ROOT, 'tools/precalculus-audit-20261118/gaps/out/checks.json'), 'utf8'));
const newIds = items.filter((q) => NEW.some(([u, n]) => q.skillId === `${u}-skill-${String(n).padStart(2, '0')}`)).map((q) => q.id);
assert.deepEqual(newIds.filter((id) => !checks[id]), [], 'every new item has verifier check data');
// The standards map lists the new standards.
const map = fs.readFileSync(path.join(ROOT, 'worksheet-generator/menu/standards-map.js'), 'utf8');
for (const s of ['A-APR.D.7', 'F-BF.B.4b', 'F-BF.B.4c', 'F-BF.B.4d', 'N-CN.A.3', 'N-CN.B.5', 'A-APR.C.5']) assert(map.includes(s), 'standards map has ' + s);
console.log('Precalculus gap skills: ' + NEW.length + ' skills, ' + newIds.length + ' items');
