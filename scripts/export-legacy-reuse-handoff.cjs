#!/usr/bin/env node
/* Produce a deterministic reviewer handoff for existing shared-course generators.
 * Output is an audit only, not an approval or publication manifest. */
'use strict';
const fs=require('node:fs'),path=require('node:path'),vm=require('node:vm');
const env=require('../worksheet-generator/menu/tests/load.cjs')(['games/bank.js']);
for(const file of ['course-catalog.js','skill-crosswalk.js','legacy-crosswalk-audit.js','cross-course-difficulty.js','legacy-review-samples.js'])
 vm.runInContext(fs.readFileSync(path.join(__dirname,'..',file),'utf8'),env,{filename:file});
const entries=env.MK_LEGACY_CROSSWALK_AUDIT.inspect(env.MK_SKILL_CROSSWALK,env.MKMENU);
const report={schemaVersion:1,publicationApproved:false,topics:[]};
for(const entry of entries){
 const row={topic:entry.key,source:entry.curatedGenerator||null,targets:[]};
 for(const target of entry.targets){
  for(const level of ['cp2','cp1','honors']){
   const plan=env.MK_CROSS_COURSE_DIFFICULTY.plan(entry,target.courseId,level);
   if(!plan.eligible){row.targets.push({courseId:target.courseId,skill:target.name,level,status:'blocked',reason:plan.reason});continue;}
   const generated=env.MK_LEGACY_REVIEW_SAMPLES.sample(entry,target.courseId,level,'handoff',6);
   const questions=generated.questions.map(q=>({reviewKey:q.reviewKey,tier:q.tier,prompt:q.prompt,partPrompt:q.partPrompt,answer:q.answer,hasFigure:!!q.figure,options:q.options,reviewStatus:'unreviewed'}));
   row.targets.push({courseId:target.courseId,skill:target.name,level,status:questions.length?'requires-human-review':'no-samples',questions,errors:generated.errors});
  }
 }
 report.topics.push(row);
}
const output=path.resolve(process.argv[2]||'/tmp/legacy-reuse-handoff.json');
fs.mkdirSync(path.dirname(output),{recursive:true});fs.writeFileSync(output,JSON.stringify(report,null,2)+'\n');
const counts=report.topics.flatMap(t=>t.targets);
console.log('Created '+output+' with '+report.topics.length+' topics, '+counts.filter(x=>x.status==='requires-human-review').length+' candidate scopes, '+counts.reduce((n,x)=>n+(x.questions||[]).length,0)+' review samples; no approvals.');
