#!/usr/bin/env node
// Validate the assembled Grade 2 public release (source remains in FinancialAlgebra).
'use strict';
const fs=require('node:fs'),path=require('node:path'),vm=require('node:vm'),assert=require('node:assert/strict');
const root=path.resolve(process.argv[2]||'_site');
const file=p=>path.join(root,p),read=p=>fs.readFileSync(file(p),'utf8');
const manifest=JSON.parse(read('question-banks/manifest.json'));
const banks=manifest.banks.filter(x=>x.courseId==='grade2');
assert.equal(banks.length,12,'Expected exactly twelve published Grade 2 banks');
assert.equal(new Set(banks.map(x=>x.unitId)).size,12,'Duplicate Grade 2 unit');
let questions=0;
for(const entry of banks){
 assert(entry.approved===true&&entry.teacherUse===true,'Grade 2 native bank must be enabled for teachers');
 assert.equal(entry.path,'question-banks/grade2/'+entry.unitId+'.json');
 const bank=JSON.parse(read(entry.path));
 assert.equal(bank.courseId,'grade2');assert.equal(bank.unitId,entry.unitId);
 assert(Array.isArray(bank.questions)&&bank.questions.length>0);
 questions+=bank.questions.length;
 for(const q of bank.questions){
  const src=q.diagram?.spec?.src;
  if(src){assert(!src.includes('..')&&!src.startsWith('/'),'Unsafe diagram URL');assert(fs.existsSync(file(src)),'Missing diagram '+src);}
 }
}
assert.equal(questions,4770,'Practice bank total unexpectedly changed');
for(const item of ['grade2-main-catalog.js','grade2/index.html','grade2/manifest.json','grade2/worksheet-generator/grade2-games.html','grade2/worksheet-generator/grade2-flashcards.html','grade2/worksheet-generator/grade2-understanding-check.html','grade2/grade2-native-notes.js','grade2/grade2-native-resources.js']){
 assert(fs.existsSync(file(item)),'Missing Grade 2 resource '+item);
}
const courseManifest=JSON.parse(read('grade2/manifest.json'));
assert.equal(courseManifest.banks.length,12,'Separate Grade 2 player manifest missing units');
let checks=0;
for(const unit of banks.map(x=>x.unitId)){
 const item=JSON.parse(read('grade2/question-banks/math2/checks/'+unit+'.json'));
 assert.equal(item.courseId,'math2');assert.equal(item.unitId,unit);
 checks+=item.questions.length;
 assert(fs.existsSync(file('grade2/question-banks/math2/checks/meta/'+unit+'.meta.json')));
}
assert.equal(checks,318,'Dedicated Understanding Check count changed');
const context={window:{}};context.globalThis=context.window;
for(const p of ['data.js','course-catalog.js','grade4-main-catalog.js','grade3-main-catalog.js','grade2-main-catalog.js']){
 vm.runInNewContext(read(p),context,{filename:p,timeout:5000});
}
const courses=context.window.LIBRARY.courses.filter(c=>c.id==='grade2');
assert.equal(courses.length,1,'Grade 2 missing or duplicated');
const course=courses[0];
assert.equal(course.units.length,12);
assert.equal(course.units.reduce((sum,u)=>sum+context.window.MK_COURSE_CATALOG.getSkills('grade2',u.id).length,0),53);
for(const unit of course.units){
 for(const title of ['Lesson Plan Generator','Worksheet Generator','Activity Generator','Assessment Generator','Flashcards','Understanding Check','Cheat Sheet']){
  assert(unit.artifacts.some(x=>x.title===title),'Missing '+unit.id+' '+title);
 }
 assert(unit.artifacts.some(x=>x.type==='Game'&&x.path.startsWith('grade2/worksheet-generator/grade2-games.html?')),'Missing direct game route '+unit.id);
 for(const a of unit.artifacts){
  for(const key of ['path','thumb']){
   const p=String(a[key]||'').split(/[?#]/,1)[0];
   const full=path.resolve(root,p);
   assert(full.startsWith(root+path.sep),'Path escapes site: '+p);
   assert(fs.existsSync(full),'Missing '+key+' for '+unit.id+': '+p);
  }
 }
}
const home=read('index.html');
assert(home.includes('grade2-main-catalog.js'),'Homepage is not loading released Grade 2');
for(const p of ['worksheet-generator/lesson-planner.html','worksheet-generator/worksheet.html','worksheet-generator/menu-assessment.html','worksheet-generator/printables.html']){
 assert(read(p).includes('grade2-main-catalog.js'),'Generator cannot select Grade 2: '+p);
}
console.log('PASS Grade 2 public release: 12 units, 53 skills, 4,770 practice questions, 318 checks, native generators, direct games and all local resource/thumbnail paths.');
