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
 const counts=new Map();
 for(const q of bank.questions){
  total++;skills.add(entry.unitId+':'+q.skillId);
  counts.set(q.skillId,(counts.get(q.skillId)||0)+1);
  if(q.diagram?.type==='image'){
   imageCount++;const src=q.diagram.spec?.src;
   assert.match(src,/^question-banks\/assets\/algebra2\/[a-z0-9/_-]+\.png$/i);
   assert.ok(fs.existsSync(path.join(root,src)),src+' image missing');
  }
 }
 for(const [skill,count] of counts)assert.ok(count>=30,skill+' has only '+count+' questions');
}
assert.equal(total,2717);assert.equal(skills.size,87);
console.log('PASS 11 Algebra 2 banks, 2,717 questions, 87 skills, '+imageCount+' image references; human review not asserted');
