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

/* Exercise the ACTUAL UI section-composition functions in a controlled VM.
 * We extract the function block so future changes to its implementation
 * are exercised, rather than reimplementing the behavior in this test. */
const uiSource = fs.readFileSync(path.join(root,'planner/planner-ui.js'),'utf8');
const start = uiSource.indexOf('  function configureSection(');
const finish = uiSource.indexOf('  var problemCounts =',start);
assert.ok(start >= 0 && finish > start,'Section composer must be present');
const composeSource = uiSource.slice(start,finish);
const sectionSequence = ['notes','practice','notes','practice','exit'];
const sectionChoices = { notes:true,practice:true,exit:true };
const sectionConfigs = {
  0:{lesson:ids[0]}, 1:{lesson:ids[0],count:5},
  2:{lesson:ids[1]}, 3:{lesson:ids[1],count:8},
  4:{count:3}
};
const compose = new Function('P','sectionConfigs','sectionSequence','sectionChoices','lsSet','KEY_SEQUENCE',
  composeSource+'\nreturn applySectionChoices;')(P,sectionConfigs,sectionSequence,sectionChoices,()=>{},'test');
function cloneSection(name) {
  return {id:name,title:name,groups:name==='notes'?[]:[{name:'',items:[{
    entry:P.entriesFor([ids[0]])[0],slot:name+'-initial',c:2,num:1
  }]}]};
}
const combined = {day:days[0],level:'cp1',seed:'regression',selectedDays:days.map(d=>d.day),
  used:{keys:new Set(),sigs:new Set()},sections:['notes','practice','exit'].map(cloneSection)};
compose(combined);
assert.deepEqual(combined.sections.map(s=>s.id),sectionSequence);
assert.deepEqual(combined.sections.map(s=>s.groups.reduce((n,g)=>n+g.items.length,0)),[0,5,0,8,3]);
assert.equal(combined.sections[0].lessonDay.lesson_id,ids[0]);
assert.equal(combined.sections[2].lessonDay.lesson_id,ids[1]);
for (const [sectionIndex,id] of [[1,ids[0]],[3,ids[1]]]) {
  assert.ok(combined.sections[sectionIndex].groups.flatMap(g=>g.items).every(p=>p.lesson===id),
    'Practice section must contain only topic '+id);
}
console.log('PASS repeated Notes/Practice order, lesson assignments and independent counts');

