'use strict';
// Algebra 2 audit batch D: standards-gap skills, context problems and the A-REI.D.11 tag.
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');
const ROOT = path.join(__dirname, '..');
const dir = path.join(ROOT, 'question-banks/algebra2');
const banks = fs.readdirSync(dir).filter(f => f.endsWith('.json')).map(f => JSON.parse(fs.readFileSync(path.join(dir, f), 'utf8')));
const items = banks.flatMap(b => b.questions.map(q => ({ ...q, unit: b.unitId })));
const w = {}; w.window = w; vm.createContext(w);
vm.runInContext(fs.readFileSync(path.join(ROOT, 'course-catalog.js'), 'utf8'), w);
vm.runInContext(fs.readFileSync(path.join(ROOT, 'worksheet-generator/planner/notes-teach-algebra2.js'), 'utf8'), w);
const NEW = [
  ['functions-transformations', 9, 'Comparing functions in different representations', 'F-IF.C.9'],
  ['functions-transformations', 10, 'Parametric equations', 'F-IF.C.10'],
  ['linear-functions-systems', 8, 'Solving f(x) = g(x) with graphs and tables', 'A-REI.D.11'],
  ['exponential-logarithmic-functions', 9, 'Interpreting the structure of expressions', 'A-SSE.A.1a'],
  ['probability-statistics', 9, 'Simulation and evaluating models', 'S-IC.A.2'],
  ['probability-statistics', 10, 'Randomized experiments and comparing treatments', 'S-IC.B.5'],
  ['probability-statistics', 11, 'Evaluating reports based on data', 'S-IC.B.6'],
];
for (const [unit, n, name, std] of NEW) {
  const id = `${unit}-skill-${String(n).padStart(2, '0')}`;
  assert.equal(w.MK_COURSE_CATALOG.getSkills('algebra2', unit)[n - 1], name, id + ' name');
  const qs = items.filter(q => q.skillId === id);
  for (const lv of ['cp2', 'cp1', 'honors']) {
    const at = qs.filter(q => q.level === lv);
    assert(at.length >= 16, `${id} ${lv}: ${at.length}`);
    assert(at.filter(q => q.format === 'multiple-choice').length >= 6, `${id} ${lv} multiple choice`);
    assert(at.filter(q => /answered this problem incorrectly/.test(q.prompt)).length >= 2, `${id} ${lv} find the mistake`);
  }
  assert(qs.every(q => q.standards.includes(std)), id + ' tagged ' + std);
  assert(w.MKPLAN_TEACH_ALGEBRA2_META(id), id + ' teaching notes');
}
// #5: A-REI.D.11 only on the graph/table skill; the algebraic systems keep A-REI.C.6.
// (Graphing Practice items that solve a system by graphing keep it too: that is what A-REI.D.11 describes.)
assert.deepEqual([...new Set(items.filter(q => q.standards.includes('A-REI.D.11') && q.format !== 'plot').map(q => q.skillId))], ['linear-functions-systems-skill-08']);
assert(items.filter(q => q.skillId === 'linear-functions-systems-skill-04').every(q => q.standards.includes('A-REI.C.6')));
// #7: every unit has at least 8 real-world context problems per level.
const tags = Object.assign({}, ...fs.readdirSync(path.join(dir, 'meta')).map(f => JSON.parse(fs.readFileSync(path.join(dir, 'meta', f), 'utf8'))));
for (const b of banks) for (const lv of ['cp2', 'cp1', 'honors']) {
  const n = b.questions.filter(q => q.level === lv && (tags[q.id] || []).includes('context-problem')).length;
  assert(n >= 8, `${b.unitId} ${lv}: ${n} context problems`);
}
// Every batch D item names the verifier and passed it (verify.py runs in the workflow).
const batch = items.filter(q => /algebra2-gaps-20261117/.test(q.sourceNotes));
assert.equal(batch.length, 552);
assert(batch.every(q => Array.isArray(q.solutionSteps) && q.solutionSteps.length >= 2));
console.log(`PASS Algebra 2 gap skills: ${NEW.length} new skills, ${batch.length} items, context problems in all ${banks.length} units`);
