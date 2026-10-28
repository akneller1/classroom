/* Integration coverage: actual Algebra 1 problem generators and independent verifier.
 * Run: node worksheet-generator/tests/planner-real-problems.cjs
 * This executes the same math engine, skill banks, and planner scope as the browser.
 * It intentionally does not test browser layout or PPTX presentation.
 */
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');
const assert = require('node:assert/strict');
const root = path.resolve(__dirname,'..');
const g = { console, setTimeout, clearTimeout };
g.window = g;
vm.createContext(g);
const scripts = [
 'core/rng.js','core/frac.js','core/tex.js','core/graph.js',
 'core/framework.js','menu/mathcheck.js','menu/figures.js',
 'menu/verify.js','menu/engine.js','menu/skills/kit.js',
 'menu/skills/algebra1-linear-equations-slope.js',
 'planner/scope-algebra1.js','planner/lesson-skills.js','planner/planner.js'
];
scripts.forEach(file => vm.runInContext(fs.readFileSync(path.join(root,file),'utf8'),g,{filename:file}));
const P = g.MKPLAN;
const lessonDays = g.MKPLAN_SCOPE.days.filter(d => d.unit===5 && d.day_type==='Lesson').slice(0,2);
assert.equal(lessonDays.length,2);
const ids = lessonDays.map(d => d.lesson_id);
for (const level of ['cp2','cp1','honors']) {
  for (const seed of ['integration-A','integration-B']) {
    const plan = P.buildDay(lessonDays[0].day,{level,seed,selectedDays:lessonDays.map(d=>d.day),include:{challenge:true}});
    for (const sectionId of ['examples','practice','exit']) {
      const section = plan.sections.find(s=>s.id===sectionId);
      assert.ok(section,sectionId+' missing');
      const problems = section.groups.flatMap(x=>x.items);
      assert.ok(problems.length,sectionId+' empty');
      for (const id of ids) assert.ok(problems.some(p=>p.lesson===id),sectionId+' missing '+id);
      for (const p of problems) {
        assert.ok(!p.failed,sectionId+' could not generate '+p.skill+' ('+level+'/'+seed+'): '+p.reason);
        assert.equal(p.verify && p.verify.status,'verified',sectionId+' answer not verified: '+p.skill);
      }
    }
    // Verify that the repeated section composer keeps problem sources and counts.
    const text = fs.readFileSync(path.join(root,'planner/planner-ui.js'),'utf8');
    const start = text.indexOf('  function configureSection('), end = text.indexOf('  var problemCounts =',start);
    assert.ok(start>=0 && end>start);
    const sequence=['notes','practice','notes','practice','exit'];
    const choices={notes:true,practice:true,exit:true};
    const cfg={0:{lesson:ids[0]},1:{lesson:ids[0],count:5},2:{lesson:ids[1]},3:{lesson:ids[1],count:8},4:{count:3}};
    const compose = new Function('P','sectionConfigs','sectionSequence','sectionChoices','lsSet','KEY_SEQUENCE',text.slice(start,end)+'\nreturn applySectionChoices;')(P,cfg,sequence,choices,()=>{},'test');
    compose(plan);
    assert.deepEqual(Array.from(plan.sections.map(s=>s.id)),sequence);
    assert.deepEqual(Array.from(plan.sections.map(s=>s.groups.flatMap(g=>g.items).length)),[0,5,0,8,3]);
    for (const [i,id] of [[1,ids[0]],[3,ids[1]]]) {
      for (const p of plan.sections[i].groups.flatMap(g=>g.items)) {
        assert.equal(p.lesson,id,'Wrong lesson in repeated Practice');
        assert.ok(!p.failed,'Repeated Practice generation failed: '+p.reason);
        assert.equal(p.verify && p.verify.status,'verified','Unverified repeated Practice answer');
      }
    }
  }
}
console.log('PASS real problem generation, independent verification, and repeated section routing (CP2, CP1, Honors)');
