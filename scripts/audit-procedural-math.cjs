#!/usr/bin/env node
/* Read-only sampled procedural-math audit for Algebra 1 and Geometry.
 * Uses the browser's independent printed-problem verifier, not generator
 * answer trust. Generates 1 question for each registered skill at CP2, CP1
 * and Honors; records failures instead of altering any question bank.
 */
'use strict';
const fs=require('node:fs'),path=require('node:path');
const {chromium}=require('playwright');
const dest='procedural-math-audit-results';
fs.mkdirSync(dest,{recursive:true});
const origin=process.env.SMOKE_BASE_URL||'http://127.0.0.1:8765';
const out={createdAt:new Date().toISOString(),generator:'Menu Assessment',units:[],issues:[],totalAttempts:0,passed:0,failed:0};
async function main(){
 const browser=await chromium.launch({headless:true,args:['--no-sandbox']});
 try{
  const page=await browser.newPage();
  const exceptions=[];
  page.on('pageerror',e=>exceptions.push(e.message));
  await page.goto(origin+'/worksheet-generator/menu-assessment.html',{waitUntil:'domcontentloaded',timeout:60000});
  await page.waitForFunction(()=>window.MKMENU?.generateProblem&&
    window.MKMENU?.verifyProblem&&Object.keys(window.MKMENU.skillSets||{}).length>20,
    null,{timeout:120000});
  const unitIds=await page.evaluate(()=>{
   const ns=window.MKMENU;
   return ns.CATALOG.filter(c=>c.course==='Algebra 1'||c.course==='Geometry')
    .flatMap(c=>c.units.map(u=>({course:c.course,id:u[0],name:u[1]})));
  });
  for(const entry of unitIds){
   const unit=await page.evaluate(function(entry){
    const ns=window.MKMENU,set=ns.skillSets[entry.id];
    const data={course:entry.course,unit:entry.id,title:entry.name,skills:set?.skills.length||0,checked:0,passed:0,failed:0,issues:[]};
    if(!set){data.issues.push({type:'missing-generator-skill-set'});return data}
    for(const [level,c] of [['cp2',2],['cp1',4],['honors',6]]){
     const policy={level,intOnly:level!=='honors',compact:false};
     for(const sk of set.skills){
      const seed='independent-audit-20261110-'+entry.id+'-'+sk.id+'-'+level;
      data.checked++;
      try{
       const item=ns.generateProblem(entry.id,sk.id,c,policy,seed);
       if(!item||item.failed){
        data.failed++;
        data.issues.push({type:'generation-failed',level,skill:sk.id,reason:item?.reason||'No item'});
        continue;
       }
       const result=ns.verifyProblem(item,policy);
       if(result.status!=='verified'||!result.ok){
        data.failed++;
        data.issues.push({type:'independent-verifier-rejection',level,skill:sk.id,
          reason:(result.issues||[]).slice(0,6).join(' | '),status:result.status});
        continue;
       }
       if(item.parts?.some(p=>p.answer===undefined||p.answer===null||String(p.answer).trim()==='')){
        data.failed++;data.issues.push({type:'missing-part-answer',level,skill:sk.id});
        continue;
       }
       data.passed++;
      }catch(e){
       data.failed++;data.issues.push({type:'exception',level,skill:sk.id,reason:e.message});
      }
     }
    }
    return data;
   },entry);
   out.units.push({...unit,issues:undefined});
   out.totalAttempts+=unit.checked;out.passed+=unit.passed;out.failed+=unit.failed;
   for(const issue of unit.issues)out.issues.push({course:unit.course,unit:unit.unit,...issue});
   console.log(unit.unit+': '+unit.passed+'/'+unit.checked+' verified, '+unit.issues.length+' flags');
  }
  out.pageExceptions=exceptions;
 }finally{await browser.close()}
 fs.writeFileSync(dest+'/report.json',JSON.stringify(out,null,2));
 let md='# Procedural math audit: Algebra 1 and Geometry\n\n';
 md+='One seeded question per skill per difficulty, checked against the independent printed-problem verifier. This does not certify every possible randomized variant.\n\n';
 md+='**'+out.passed+'/'+out.totalAttempts+' sample questions verified**, '+out.failed+' flagged.\n\n';
 md+='| Course | Unit | Checked | Passed | Flags |\n|---|---|---:|---:|---:|\n';
 for(const u of out.units)md+='| '+u.course+' | '+u.unit+' | '+u.checked+' | '+u.passed+' | '+u.failed+' |\n';
 md+='\n## Flagged issues\n\n';
 for(const f of out.issues.slice(0,300))md+='- '+f.unit+' / '+(f.skill||'unit')+' / '+(f.level||'all')+': '+f.type+' — '+(f.reason||'')+'\n';
 md+='\nBrowser JavaScript exceptions: '+(out.pageExceptions||[]).length+'.\n';
 fs.writeFileSync(dest+'/summary.md',md);
 if(process.env.GITHUB_STEP_SUMMARY)fs.appendFileSync(process.env.GITHUB_STEP_SUMMARY,md);
 console.log(JSON.stringify({checked:out.totalAttempts,passed:out.passed,failed:out.failed,exceptions:out.pageExceptions?.slice(0,8)},null,2));
}
main().catch(e=>{console.error(e);process.exitCode=1});
