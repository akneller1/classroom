/* Regression for multi-lesson coverage and independent topic problem pools.
 * Run: node worksheet-generator/tests/planner-multi-lesson.cjs
 * Uses the REAL Algebra 1 scope, skill mapping and planner engine, with a deterministic
 * verified-problem stub. This tests selection and routing, not numerical verification
 * or browser/PowerPoint rendering.
 */
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');
const root = path.resolve(__dirname, '..');
const context = {
  MKWS: {},
  MKMENU: {
    LEVELS: { cp1: { id: 'cp1', tiers: [2,3,4], intOnly: false } },
    skillSets: {},
    generateProblem: (set,skill,c,policy,seed) => ({
      prompt: skill + ' ' + seed, answer: '1', verify: { status: 'verified' }, c
    })
  }
};
context.window = context;
vm.createContext(context);
for (const file of ['planner/scope-algebra1.js','planner/lesson-skills.js','planner/planner.js']) {
  vm.runInContext(fs.readFileSync(path.join(root,file),'utf8'),context,{filename:file});
}
const P = context.MKPLAN;
const days = context.MKPLAN_SCOPE.days.filter(d=>d.unit===5 && d.day_type==='Lesson').slice(0,2);
assert.equal(days.length,2,'Need two Unit 5 instructional lessons');
const ids = days.map(d=>d.lesson_id);
const plan = P.buildDay(days[0].day,{level:'cp1',seed:'regression',selectedDays:days.map(d=>d.day)});
assert.deepEqual(Array.from(plan.selectedDays),days.map(d=>d.day));
for (const name of ['examples','practice','exit']) {
  const sec = plan.sections.find(s=>s.id===name);
  const found = new Set(sec.groups.flatMap(g=>g.items.map(p=>p.lesson)));
  for (const id of ids) assert.ok(found.has(id),name+' missing '+id);
}
const copy = P.buildDay(days[0].day,{level:'cp1',seed:'regression'});
assert.equal(copy.selectedDays.length,1,'Single-lesson backwards compatibility');
for (const id of ids) assert.ok(P.entriesFor([id]).length,'Missing mapped skills for '+id);
console.log('PASS multi-lesson scope, example/practice/exit routing, single-lesson fallback');
