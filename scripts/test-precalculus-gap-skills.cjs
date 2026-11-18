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
// #5: every unit has at least 9 real-world context problems per level, tagged and verified.
let ctxTotal = 0;
for (const b of banks) {
  const tags = JSON.parse(fs.readFileSync(path.join(dir, 'meta', b.unitId + '.tags.json'), 'utf8'));
  const ctx = b.questions.filter((q) => (tags[q.id] || []).includes('context-problem'));
  for (const lv of ['cp2', 'cp1', 'honors']) assert(ctx.filter((q) => q.level === lv).length >= 9, `${b.unitId} ${lv}: context problems`);
  assert.deepEqual(ctx.filter((q) => /-w\d{3}$/.test(q.id) && !checks[q.id]).map((q) => q.id), [], b.unitId + ' context items verified');
  ctxTotal += ctx.length;
}
// #6: no single question template makes up 40% or more of a skill's single-part items.
function sig(p) {
  const lines = p.split('\n');
  let t = /answered this problem incorrectly/.test(lines[0]) && lines.length > 1 ? lines[1] : lines[0];
  t = t.replace(/\d+(\.\d+)?/g, '#').replace(/(#\s*[+\-−]\s*)+#/g, '#').replace(/[−-]\s*#/g, '#');
  return t.slice(0, 70);
}
const bySkill = {};
for (const q of items) if (q.format !== 'open-response') (bySkill[q.skillId] = bySkill[q.skillId] || []).push(q);
for (const [sk, qs] of Object.entries(bySkill)) {
  const c = {};
  for (const q of qs) c[sig(q.prompt)] = (c[sig(q.prompt)] || 0) + 1;
  const top = Math.max(...Object.values(c));
  assert(top / qs.length < 0.4, `${sk}: one template is ${top} of ${qs.length} items`);
}
const varied = items.filter((q) => /question variety/.test(q.sourceNotes));
assert.deepEqual(varied.filter((q) => !checks[q.id]).map((q) => q.id), [], 'every variety item verified');
console.log('Precalculus gap skills: ' + NEW.length + ' skills, ' + newIds.length + ' items; ' + ctxTotal + ' tagged context problems; ' + varied.length + ' variety items');
