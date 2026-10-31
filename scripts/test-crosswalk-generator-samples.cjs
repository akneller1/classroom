#!/usr/bin/env node
/* Smoke-test curated legacy generator reuse with the EXISTING verifier.
   Does not enable cross-course use or establish mathematical editorial approval. */
'use strict';
const fs=require('node:fs'),vm=require('node:vm'),path=require('node:path'),assert=require('node:assert/strict');
const load=require('../worksheet-generator/menu/tests/load.cjs');
const env=load(['games/bank.js']),root=path.resolve(__dirname,'..');
for(const file of ['course-catalog.js','skill-crosswalk.js','legacy-crosswalk-audit.js'])vm.runInContext(fs.readFileSync(path.join(root,file),'utf8'),env,{filename:file});
const audit=env.MK_LEGACY_CROSSWALK_AUDIT.inspect(env.MK_SKILL_CROSSWALK,env.MKMENU);
const summary=[];
for(const mapped of audit){
 if(!mapped.curatedGenerator)continue;
 const g=mapped.curatedGenerator,tiers=[1,2,3],samples=[];
 for(const c of tiers){
  let count=0;
  for(let i=0;i<4;i++){
   const items=env.MKGAMES.makeItems(g.setId,g.skillId,c,{intOnly:true,level:'test'},'shared-reuse|'+mapped.key+'|'+c+'|'+i,null);
   for(const item of items){
    assert.equal(item.options.filter(o=>o.ok).length,1,mapped.key+' has invalid MC key count');
    for(const option of item.options)assert.equal(env.MKGAMES.answerOk(item.p,item.k,option.a).ok,option.ok,mapped.key+' distractor verification mismatch');
    count++;
   }
  }
  samples.push(count);
 }
 summary.push({topic:mapped.key,samples});
 console.log(mapped.key+': verified game MC items by tier 1/2/3 = '+samples.join('/'));
}
assert.equal(summary.length,14,'The curated crosswalk has changed; review the generator candidates before sharing');
const total=summary.reduce((n,x)=>n+x.samples.reduce((a,b)=>a+b,0),0);
assert.ok(total>0,'No sample questions found');
console.log('PASS '+summary.length+' curated generator references inspected; '+total+' generated MC items checked against the existing answer verifier; no cross-course publication');
