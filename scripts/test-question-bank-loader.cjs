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
  assert.ok(item.approved===true||(item.courseId==='algebra2'&&item.teacherUse===true));
  assert.ok(fs.existsSync(path.join(root,item.path)),'Missing approved bank: '+item.path);
 }
 assert.equal((await loader.load({version:1,banks:[{...entry,approved:false}]},()=>{throw Error('Should not fetch unapproved bank')})).length,0);
 assert.equal(banks.available(courseId,unitId),false);
 // Explicit teacher-use flag allows Algebra 2 without asserting human approval.
 assert.equal((await loader.load({version:1,banks:[{...entry,approved:false,teacherUse:false}]},()=>{throw Error('Disabled bank should not load')})).length,0);
 await assert.rejects(loader.load({version:1,banks:[entry]},async()=>({...bank,unitId:'wrong'})),/mismatch/);
 assert.equal(banks.available(courseId,unitId),false);
 const ids=await loader.load({version:1,banks:[entry]},async()=>bank);
 assert.equal(ids.length,1);
 assert.equal(banks.available(courseId,unitId),true);
 assert.equal(banks.select({courseId,unitId}).length,1);
 assert.throws(()=>loader.load({version:1,banks:[entry,entry]},async()=>bank),/Duplicate/);

 const calls=[],scopedRegistered=new Set();
 const manifest2={version:1,banks:[
  {courseId:'algebra',unitId:'systems-of-equations',path:'question-banks/algebra/systems-of-equations.json',approved:true},
  {courseId:'statistics',unitId:'exploring-data',path:'question-banks/statistics/exploring-data.json',approved:false}
 ]};
 const mockWindow={};
 mockWindow.MK_QUESTION_BANKS={
  available(c,u){return scopedRegistered.has(c+'/'+u)},
  validate(b){return {ok:b.schemaVersion===1,errors:[]}},
  register(b){scopedRegistered.add(b.courseId+'/'+b.unitId);return {ok:true,errors:[]}}
 };
 mockWindow.fetch=(url,opts)=>{
  calls.push({url,cache:opts.cache});
  const value=url==='question-banks/manifest.json'?manifest2:
   url==='question-banks/algebra/systems-of-equations.json'?
   {schemaVersion:1,courseId:'algebra',unitId:'systems-of-equations',questions:[]}:undefined;
  return Promise.resolve({ok:value!==undefined,json:async()=>value});
 };
 vm.runInNewContext(fs.readFileSync(path.join(root,'question-bank-loader.js'),'utf8'),{window:mockWindow,Promise});
 const lazy=mockWindow.MK_BANK_LOADER;
 await Promise.all([lazy.loadUnitFromSite('algebra','systems-of-equations'),lazy.loadUnitFromSite('algebra','systems-of-equations')]);
 assert.equal(calls.filter(c=>c.url==='question-banks/manifest.json').length,1);
 assert.equal(calls.filter(c=>c.url.endsWith('systems-of-equations.json')).length,1);
 assert.equal(scopedRegistered.size,1);
 assert.equal((await lazy.loadUnitFromSite('statistics','exploring-data')).length,0);
 assert.equal(calls.some(c=>c.url.endsWith('exploring-data.json')),false);
 assert.equal(calls[0].cache,'no-store');
 assert.equal(calls[1].cache,'default');
 await assert.rejects(lazy.loadUnitFromSite('../algebra','systems-of-equations'),/Invalid course or unit/);
 console.log('PASS lazy question-bank requests, approval gate, caching and deduplication');
 console.log('PASS approved manifest loading, unapproved gating, unit isolation and duplicate rejection');
}
main().catch(e=>{console.error(e);process.exitCode=1});
