#!/usr/bin/env node
'use strict';
const assert=require('node:assert/strict'),fs=require('node:fs'),vm=require('node:vm'),path=require('node:path');
const env=require('../worksheet-generator/menu/tests/load.cjs')(['games/bank.js']);
for(const file of ['course-catalog.js','skill-crosswalk.js','legacy-crosswalk-audit.js','cross-course-difficulty.js','legacy-review-samples.js'])
 vm.runInContext(fs.readFileSync(path.join(__dirname,'..',file),'utf8'),env,{filename:file});
const entries=env.MK_LEGACY_CROSSWALK_AUDIT.inspect(env.MK_SKILL_CROSSWALK,env.MKMENU);
let checked=0;
for(const entry of entries){
 if(!entry.curatedGenerator)continue;
 const target=entry.targets.find(t=>env.MK_CROSS_COURSE_DIFFICULTY.plan(entry,t.courseId,'cp1').eligible);
 if(!target)continue;
 const output=env.MK_LEGACY_REVIEW_SAMPLES.sample(entry,target.courseId,'cp1','review-regression',3);
 assert.equal(output.ready,true,entry.key+': no candidate question generated');
 assert.ok(output.questions.length<=3);
 for(const q of output.questions){
  assert.equal(q.approved,false);assert.equal(q.publishable,false);
  assert.ok(q.prompt);assert.ok(q.options.some(x=>x.correct));
  checked++;
 }
}
const missing=entries.find(e=>e.key==='circle-area');
assert.equal(env.MK_LEGACY_REVIEW_SAMPLES.sample(missing,'prealgebra7','cp1','a',1).ready,false);
assert.ok(checked>=25,'Too few verified review candidates');
console.log('PASS '+checked+' verifier-checked review samples, bounded counts, explicit no-publication guarantees');
