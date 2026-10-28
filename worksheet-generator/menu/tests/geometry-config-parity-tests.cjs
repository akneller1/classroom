/* Verify Algebra 1 and Geometry use identical menu/test/worksheet configuration
   controls; the only expected differences are curriculum IDs, names and skills. */
'use strict';
const assert=require('node:assert/strict');
const M=require('./load.cjs')().MKMENU;
const algebra=M.CATALOG.find(c=>c.course==='Algebra 1').units.filter(([id])=>M.skillSets[id]);
const geometry=M.CATALOG.find(c=>c.course==='Geometry').units;
assert.equal(geometry.length,10);
assert.ok(algebra.length>0);
const baseline=M.defaultConfig(algebra[0][0]);
const normalized=c=>({
 mode:c.mode,level:c.level,answers:c.answers,versions:c.versions,
 layout:JSON.stringify(c.layout),coverage:JSON.stringify(c.coverage),
 sectionOptions:c.sections.map(s=>[s.offered,s.required,s.points,s.tier,s.adjust,s.qformat||null]),
 levels:JSON.stringify(M.LEVELS),formats:JSON.stringify(M.FORMATS)
});
let count=0;
for(const [unit] of geometry){
 assert.ok(M.skillSets[unit],'Missing Geometry bank '+unit);
 for(const mode of ['menu','test','worksheet']){
  const a=M.defaultConfig(algebra[0][0],mode);
  const g=M.defaultConfig(unit,mode);
  assert.deepEqual(normalized(g),normalized(a),'Config parity failure: '+unit+' '+mode);
  for(const level of ['cp2','cp1','honors']){
   g.level=level;a.level=level;
   assert.deepEqual(g.sections.map((_,i)=>M.sectionC(g,i)),a.sections.map((_,i)=>M.sectionC(a,i)),
     'Difficulty parity failure: '+unit+' '+mode+' '+level);
  }
  count++;
 }
}
console.log('Shared menu configuration parity: '+count+' Geometry unit/mode comparisons passed.');
