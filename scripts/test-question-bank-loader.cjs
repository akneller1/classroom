#!/usr/bin/env node
'use strict';
const assert=require('node:assert/strict'),fs=require('node:fs'),vm=require('node:vm'),path=require('node:path');
const root=path.resolve(__dirname,'..'),g={};const context={window:g,Promise};
for(const file of ['course-catalog.js','question-bank-adapter.js','question-bank-loader.js'])vm.runInNewContext(fs.readFileSync(path.join(root,file),'utf8'),context,{filename:file});
const loader=g.MK_BANK_LOADER,banks=g.MK_QUESTION_BANKS;
const unitId='conic-sections',courseId='algebra2',skillId=g.MK_COURSE_CATALOG.getSkillRecords(courseId,unitId)[0].id;
const bank={schemaVersion:1,courseId,unitId,questions:[{id:'test-1',skillId,level:'cp2',format:'short-answer',prompt:'Fixture only',answer:'1',solutionSteps:['Fixture']}]};
const entry={path:'question-banks/algebra2/conic-sections.json',courseId,unitId,approved:true};
async function main(){
 const manifest=JSON.parse(fs.readFileSync(path.join(root,'question-banks/manifest.json'),'utf8'));
 assert.equal(manifest.version,1);
 assert.ok(Array.isArray(manifest.banks));
 for(const item of manifest.banks){
  assert.equal(item.path,'question-banks/'+item.courseId+'/'+item.unitId+'.json');
  assert.equal(item.approved,true);
  assert.ok(fs.existsSync(path.join(root,item.path)),'Missing approved bank: '+item.path);
 }
 assert.equal((await loader.load({version:1,banks:[{...entry,approved:false}]},()=>{throw Error('Should not fetch unapproved bank')})).length,0);
 assert.equal(banks.available(courseId,unitId),false);
 await assert.rejects(loader.load({version:1,banks:[entry]},async()=>({...bank,unitId:'wrong'})),/mismatch/);
 assert.equal(banks.available(courseId,unitId),false);
 const ids=await loader.load({version:1,banks:[entry]},async()=>bank);
 assert.equal(ids.length,1);
 assert.equal(banks.available(courseId,unitId),true);
 assert.equal(banks.select({courseId,unitId}).length,1);
 assert.throws(()=>loader.load({version:1,banks:[entry,entry]},async()=>bank),/Duplicate/);
 console.log('PASS approved manifest loading, unapproved gating, unit isolation and duplicate rejection');
}
main().catch(e=>{console.error(e);process.exitCode=1});
