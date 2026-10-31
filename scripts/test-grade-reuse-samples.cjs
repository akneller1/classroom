#!/usr/bin/env node
/* All candidate grade/course/level combinations, actual generated items, and legacy verifier. */
'use strict';
const fs=require('fs'),path=require('path'),vm=require('vm'),assert=require('assert').strict;
const load=require('../worksheet-generator/menu/tests/load.cjs'),env=load(['games/bank.js']);
for(const file of ['course-catalog.js','skill-crosswalk.js','legacy-crosswalk-audit.js','cross-course-difficulty.js'])vm.runInContext(fs.readFileSync(path.join(__dirname,'..',file),'utf8'),env,{filename:file});
const entries=env.MK_LEGACY_CROSSWALK_AUDIT.inspect(env.MK_SKILL_CROSSWALK,env.MKMENU),policy=env.MK_CROSS_COURSE_DIFFICULTY,report=[];
for(const entry of entries)for(const target of entry.targets)for(const level of ['cp2','cp1','honors']){
 const p=policy.plan(entry,target.courseId,level);
 if(!p.eligible){report.push({topic:entry.key,course:target.courseId,level,status:'restricted',reason:p.reason});continue}
 const counts=[],failures=[];
 for(let tier=p.tiers[0];tier<=p.tiers[1];tier++){
  let valid=0;
  for(let i=0;i<6;i++){
   const seed='grade-compat|'+entry.key+'|'+target.courseId+'|'+level+'|'+tier+'|'+i;
   try {
    const items=env.MKGAMES.makeItems(p.source.setId,p.source.skillId,tier,{intOnly:p.intOnly,level:'test'},seed,null);
    for(const item of items){
     assert.equal(item.options.filter(o=>o.ok).length,1);
     for(const o of item.options)assert.equal(!!env.MKGAMES.answerOk(item.p,item.k,o.a).ok,o.ok);
     valid++;
    }
   }catch(e){failures.push('tier '+tier+': '+e.message)}
  }
  counts.push({tier,valid});
 }
 report.push({topic:entry.key,course:target.courseId,level,status:failures.length?'verification-failed':counts.some(x=>x.valid===0)?'insufficient-samples':'sampled',counts,failures,approved:false});
}
const sampled=report.filter(x=>x.status==='sampled'),incomplete=report.filter(x=>x.status==='insufficient-samples');
console.log(JSON.stringify({summary:{combinations:report.length,sampled:sampled.length,incomplete:incomplete.length,failed:report.filter(x=>x.status==='verification-failed').length,restricted:report.filter(x=>x.status==='restricted').length,approved:0},gaps:incomplete,failures:report.filter(x=>x.failures&&x.failures.length)},null,2));
if(report.some(x=>x.status==='verification-failed'))process.exitCode=1;
