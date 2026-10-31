#!/usr/bin/env node
/* Validate incoming Claude-authored question-bank JSON before integrating it.
   Usage: node scripts/check-question-bank.cjs path/to/questions.json
   Structure checks supplement (never replace) independent mathematical verification. */
'use strict';
const fs=require('node:fs'),vm=require('node:vm'),path=require('node:path');
const root=path.resolve(__dirname,'..');const file=process.argv[2];if(!file){console.error('Usage: node scripts/check-question-bank.cjs QUESTION_BANK.json');process.exit(2)}
const ctx={window:{}};vm.runInNewContext(fs.readFileSync(path.join(root,'data.js'),'utf8'),ctx);vm.runInNewContext(fs.readFileSync(path.join(root,'course-catalog.js'),'utf8'),ctx);
const bank=JSON.parse(fs.readFileSync(path.resolve(file),'utf8'));
const errors=[];const fail=x=>errors.push(x);
if(bank.schemaVersion!==1)fail('Unsupported schemaVersion');const course=ctx.window.LIBRARY.courses.find(c=>c.id===bank.courseId);if(!course)fail('Unknown courseId: '+bank.courseId);
const unit=course&&course.units.find(u=>u.id===bank.unitId);if(!unit)fail('Unknown unitId: '+bank.unitId);
const skills=unit?ctx.window.MK_COURSE_CATALOG.getSkills(bank.courseId,bank.unitId):[];
const known=new Set(ctx.window.MK_COURSE_CATALOG.getSkillRecords(bank.courseId,bank.unitId).map(s=>s.id));const ids=new Set();
if(!Array.isArray(bank.questions))fail('questions must be an array');
for(const [i,q] of (bank.questions||[]).entries()){
 const x='questions['+i+']';if(!q||typeof q!=='object'){fail(x+' invalid');continue}
 if(!q.id||ids.has(q.id))fail(x+' missing or duplicate id');ids.add(q.id);
 if(!known.has(q.skillId))fail(x+' unknown skillId '+q.skillId+' (see handoff docs)');
 if(!['cp2','cp1','honors'].includes(q.level))fail(x+' unknown level');
 if(!['short-answer','multiple-choice','select-all','open-response'].includes(q.format))fail(x+' unknown format');
 if(typeof q.prompt!=='string'||!q.prompt.trim())fail(x+' missing prompt');
 if(q.answer==null)fail(x+' missing answer');
 if(!Array.isArray(q.solutionSteps)||!q.solutionSteps.length)fail(x+' missing solution steps');
 if(q.format==='multiple-choice'||q.format==='select-all'){
  if(!Array.isArray(q.options)||q.options.length<2)fail(x+' missing choices');else {
   const n=q.options.filter(a=>a.correct===true).length;
   if(q.format==='multiple-choice'&&n!==1)fail(x+' multiple-choice requires exactly one correct answer');
   if(q.format==='select-all'&&n<2)fail(x+' select-all requires at least two correct answers');
  }
 }
 if(q.format==='open-response'&&(!Array.isArray(q.parts)||q.parts.length<4))fail(x+' open-response requires at least four parts');
 if(q.diagram&&(!q.diagram.type||!q.diagram.spec))fail(x+' incomplete diagram specification');
}
console.log('Checked '+(bank.questions||[]).length+' questions for '+bank.courseId+'/'+bank.unitId);
if(errors.length){errors.forEach(x=>console.error('- '+x));process.exitCode=1;}else console.log('PASS structural question-bank checks; math correctness NOT verified');
