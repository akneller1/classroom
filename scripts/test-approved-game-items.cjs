#!/usr/bin/env node
'use strict';
const assert=require('node:assert/strict'),fs=require('node:fs'),vm=require('node:vm'),path=require('node:path');
const root=path.resolve(__dirname,'..'),ctx={window:{}};
for(const f of ['course-catalog.js','question-bank-adapter.js','resource-eligibility.js','approved-game-items.js'])
 vm.runInNewContext(fs.readFileSync(path.join(root,f),'utf8'),ctx,{filename:f});
const g=ctx.window,unitId='conic-sections',courseId='algebra2';
const skill=g.MK_COURSE_CATALOG.getSkillRecords(courseId,unitId)[0].id;
const req={game:'connect-4',courseId,unitId,level:'cp2'};
assert.equal(g.MK_APPROVED_GAME_ITEMS.prepare(req).ready,false);
const bank={schemaVersion:1,courseId,unitId,questions:[
 {id:'q1',skillId:skill,level:'cp2',format:'multiple-choice',prompt:'Fixture only',answer:'A',solutionSteps:['Fixture'],options:[{text:'A',correct:true},{text:'B',correct:false}]},
 {id:'q2',skillId:skill,level:'cp1',format:'short-answer',prompt:'Fixture two',answer:'3',solutionSteps:['Fixture']},
 {id:'q3',skillId:skill,level:'cp2',format:'short-answer',prompt:'Needs diagram',answer:'1',solutionSteps:['Fixture'],diagram:{type:'geometry-figure',spec:{}}}
]};
assert.equal(g.MK_QUESTION_BANKS.register(bank,{verified:true}).ok,true);
for(const game of ['connect-4','tic-tac-toe','picture-reveal']){
 const output=g.MK_APPROVED_GAME_ITEMS.prepare({...req,game});
 assert.equal(output.ready,true);
 assert.equal(output.items.length,1,'Diagram-dependent items must remain excluded');
 assert.equal(output.items[0].options.filter(x=>x.correct).length,1);
}
assert.equal(g.MK_APPROVED_GAME_ITEMS.prepare({...req,level:'honors'}).ready,false);
assert.equal(g.MK_APPROVED_GAME_ITEMS.prepare({...req,courseId:'math6'}).ready,false);
assert.equal(g.MK_APPROVED_GAME_ITEMS.prepare({...req,game:'other'}).ready,false);
console.log('PASS: three game adapters, difficulty and course isolation, diagram safety');
