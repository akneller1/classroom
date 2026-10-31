#!/usr/bin/env node
'use strict';
const assert=require('node:assert/strict');
const fs=require('node:fs'),vm=require('node:vm'),path=require('node:path');
const root=path.resolve(__dirname,'..');const ctx={window:{}};
for(const file of ['course-catalog.js','question-bank-adapter.js','resource-eligibility.js']){
 vm.runInNewContext(fs.readFileSync(path.join(root,file),'utf8'),ctx,{filename:file});
}
const {MK_COURSE_CATALOG:catalog,MK_QUESTION_BANKS:banks,MK_RESOURCE_ELIGIBILITY:resources}=ctx.window;
const courseId='algebra2',unitId='conic-sections',skillId=catalog.getSkillRecords(courseId,unitId)[0].id;
for(const activity of Object.keys(resources.formats)){
 const status=resources.describe(activity,courseId,unitId);
 assert.equal(status.ready,false,activity+' must remain gated without a bank');
 assert.equal(status.count,0);
}
const q={id:'test-q-1',skillId,level:'cp1',format:'short-answer',prompt:'Test fixture only',answer:'2',solutionSteps:['Fixture, not for production']};
const data={schemaVersion:1,courseId,unitId,questions:[q]};
assert.equal(banks.register(data).ok,true);
assert.equal(resources.describe('flashcards',courseId,unitId).ready,false,'Unverified banks must be gated');
const otherUnit='probability-statistics';
assert.equal(banks.register({...data,unitId:otherUnit,questions:[{...q,id:'test-q-2',skillId:catalog.getSkillRecords(courseId,otherUnit)[0].id}]},{verified:true}).ok,true);
assert.equal(resources.describe('flashcards',courseId,otherUnit,'cp1').ready,true);
assert.equal(resources.describe('flashcards',courseId,otherUnit,'honors').ready,false);
assert.equal(resources.describe('assessments',courseId,otherUnit,'cp1').count,1);
assert.equal(resources.describe('nonexistent',courseId,otherUnit).ready,false);
assert.equal(resources.describe('flashcards','math6',otherUnit,'cp1').ready,false);
console.log('PASS: eligibility gating, compatible question formats, course isolation, and difficulty filters');
