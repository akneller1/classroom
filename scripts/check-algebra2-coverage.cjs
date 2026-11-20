#!/usr/bin/env node
'use strict';
const fs=require('node:fs'),assert=require('node:assert/strict'),path=require('node:path');
const root=path.resolve(__dirname,'..');
const manifest=JSON.parse(fs.readFileSync(path.join(root,'question-banks/manifest.json'),'utf8'));
const entries=manifest.banks.filter(x=>x.courseId==='algebra2');
assert.equal(entries.length,11,'Expected 11 published Algebra 2 banks');
let total=0;const skills=new Set();let imageCount=0;
for(const entry of entries){
 assert.equal(entry.path,'question-banks/algebra2/'+entry.unitId+'.json');
 const file=path.join(root,entry.path);
 const bank=JSON.parse(fs.readFileSync(file,'utf8'));
 assert.equal(bank.unitId,entry.unitId);assert.equal(bank.courseId,'algebra2');
 const counts=new Map(),levels=new Map(),errors=new Map();
 for(const q of bank.questions){
  total++;skills.add(entry.unitId+':'+q.skillId);
  counts.set(q.skillId,(counts.get(q.skillId)||0)+1);
  const lk=q.skillId+'|'+q.level;levels.set(lk,(levels.get(lk)||0)+1);
  if(/family: [^)]*_error\)/.test(q.sourceNotes||''))errors.set(lk,(errors.get(lk)||0)+1);
  if(q.diagram?.type==='image'){
   imageCount++;const src=q.diagram.spec?.src;
   assert.match(src,/^question-banks\/assets\/algebra2\/[a-z0-9/_-]+\.png$/i);
   assert.ok(fs.existsSync(path.join(root,src)),src+' image missing');
  }
 }
 for(const [skill,count] of counts)assert.ok(count>=48,skill+' has only '+count+' questions');
 // every skill has at least 16 questions at each level (CP2, CP1, Honors), 2 of them error-analysis items
 for(const skill of counts.keys())for(const lv of ['cp2','cp1','honors']){
  assert.ok((levels.get(skill+'|'+lv)||0)>=16,skill+' '+lv+' has only '+(levels.get(skill+'|'+lv)||0)+' questions');
  assert.ok((errors.get(skill+'|'+lv)||0)>=2,skill+' '+lv+' has fewer than 2 error-analysis questions');
 }
}
const additions=require('../tests/fixtures/content-20261115.json').filter(q=>q.course==='algebra2').length;
const functionAdditions=require('../tests/fixtures/function-graph-items.json').filter(q=>q.id.startsWith('a2-')).length;
const auditGapItems=48; // 2026-11-16: Binomial Theorem and Pascal's Triangle
const batchD=Object.keys(require('../tools/algebra2-gaps-20261117/out/checks.json')).length; // 2026-11-17: 7 standards-gap skills (336) + context problems (216)
assert.equal(batchD,552);
const plotItems=96;
const honorsStandards=Object.values(require('../tools/site-audit-20261120/honors_standards/out/checks.json')).filter(c=>c.course==='algebra2').length; // 2026-11-20 whole-site audit 2 #7: S-MD.B.6 and S-MD.B.7
assert.equal(honorsStandards,24); // 2026-11-17: Graphing Practice for linear systems, conics, sequences and probability (tools/algebra2-plots-20261117)
assert.equal(total,4667+additions+functionAdditions+auditGapItems+batchD+plotItems+honorsStandards); // Original bank plus reviewed November 15 additions
assert.equal(skills.size,95);
console.log('PASS 11 Algebra 2 banks, '+total+' questions, '+skills.size+' skills, every skill with 16+ questions per level, '+imageCount+' image references; human review not asserted');
