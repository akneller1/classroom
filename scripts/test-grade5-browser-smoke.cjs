#!/usr/bin/env node
/* Real Chromium coverage for the published Grade 5 course, all 101 game entries,
 * a teacher game, return navigation, and representative study/teacher tools.
 * Runs against the exact assembled _site over a local web server.
 * It checks load/initialization and DOM behavior, not independent math truth. */
'use strict';
const fs=require('node:fs');
const {chromium}=require('playwright');
const base=process.env.SMOKE_BASE_URL||'http://127.0.0.1:8765';
const manifest=JSON.parse(fs.readFileSync('_site/grade5/manifest.json','utf8'));
const units=manifest.banks.filter(e=>e.courseId==='math5').map(e=>e.unitId);
const games=['math-quest','treasure-trail','space-explorer','math-builders','picture-reveal',
 'math-race','math-soccer','connect-four','puzzle-masters'];
const report={passed:[],failed:[],consoleExceptions:[],missingAssets:[]};
const output='grade5-browser-results';
fs.mkdirSync(output,{recursive:true});
function record(label,ok,details){(ok?report.passed:report.failed).push({label,details:details||''});}
async function run(){
 const browser=await chromium.launch({headless:true,args:['--no-sandbox']});
 const ctx=await browser.newContext({viewport:{width:1280,height:830},deviceScaleFactor:1});
 const page=await ctx.newPage();page.setDefaultTimeout(10000);
 let current='';
 page.on('pageerror',e=>report.consoleExceptions.push({page:current,message:e.message}));
 page.on('response',r=>{if(r.url().startsWith(base)&&r.status()>=400)report.missingAssets.push({page:current,url:r.url(),status:r.status()});});
 const go=async target=>{
  current=target;
  const res=await page.goto(base+target,{waitUntil:'domcontentloaded',timeout:45000});
  if(!res||res.status()!==200)throw Error('HTTP '+(res?.status()||'no response'));
 };
 try{
  await go('/grade5/');
  await page.locator('#main .unit.algebra-unit-card').first().waitFor({timeout:15000});
  const count=await page.locator('#main .unit.algebra-unit-card').count();
  record('Course overview',count===11,'Rendered '+count+' unit cards');
  for(const unit of units){
   for(const game of games.concat((unit==='fraction-addition-subtraction'||unit==='fraction-multiplication-division')?['fraction-frenzy']:[])){
    const target='/grade5/worksheet-generator/grade5-games.html?unit='+unit+'&game='+game+'&student=1&level=cp1';
    const label=unit+' / '+game;
    try{
     await go(target);
     await page.locator('#app .g5-stage').waitFor({state:'attached',timeout:18000});
     await page.locator('#app .g5-q, #app .g5-grid-btns, #app .g5-board').first().waitFor({state:'attached',timeout:12000});
     const summary=(await page.locator('#app').innerText()).slice(0,500);
     if(/Oops!|Unable to load|No questions match|not enough short-answer|could not be found|not published yet/i.test(summary))throw Error(summary.slice(0,170));
     record(label,true,'Started a student game');
    }catch(e){record(label,false,e.message);}
   }
  }
  // A teacher should choose skills, start play, and return to the real Classroom homepage.
  try{
   await go('/grade5/worksheet-generator/grade5-games.html?unit=multi-digit-multiplication-division&game=math-race');
   await page.locator('.g5-home').waitFor({state:'visible'});
   const href=await page.locator('.g5-home').getAttribute('href');
   if(href!=='https://mrksclassroom.com/')throw Error('Incorrect return home: '+href);
   await page.locator('dialog.teacher-skills').waitFor({state:'visible',timeout:14000});
   await page.locator('dialog.teacher-skills button').filter({hasText:/^Continue$/}).click();
   await page.getByRole('button',{name:/Play/}).click();
   await page.locator('#app .g5-board svg').waitFor({state:'visible'});
   const carTransform=await page.locator('.g5-board svg text').filter({hasText:'🏎️'}).first().getAttribute('transform');
   if(!/scale\(-1 1\)/.test(carTransform||''))throw Error('Car no longer faces the finish line');
   record('Math Race teacher flow and navigation',true,'Skill selection, Play, rightward cars, main homepage URL');
  }catch(e){record('Math Race teacher flow and navigation',false,e.message);}
  // Old project return paths must resolve to the new unified Grade 5 course.
  try{
   await go('/grade5/math5-project-sports-stats-showdown/index.html');
   await page.locator('a.back').first().click();
   await page.waitForURL(/\/grade5\/index\.html#math5\./,{timeout:12000});
   await page.locator('#main .algebra-unit-layout').waitFor();
   record('Project → Grade 5 unit',true,'Legacy redirect retained unit anchor');
  }catch(e){record('Project → Grade 5 unit',false,e.message);}
  // Grade 5 generator and study-guide pages must open with working controls.
  const extras=[
   ['/grade5/worksheet-generator/grade5-generators.html?unit=multi-digit-multiplication-division&mode=worksheet','#config','Worksheet generator'],
   ['/grade5/worksheet-generator/grade5-flashcards.html?unit=decimal-operations','.fc-card','Flashcards'],
   ['/grade5/worksheet-generator/grade5-understanding-check.html?unit=decimal-operations&student=1&level=cp1','.g5-setup, .g5-q','Understanding Check'],
   ['/grade5/math5-area-model-explorer/index.html','main','Area Model Explorer']
  ];
  for(const [target,selector,label] of extras){
   try{await go(target);await page.locator(selector).first().waitFor({state:'attached',timeout:15000});
    const body=(await page.locator('body').innerText()).slice(0,300);
    if(/Oops!|Unable to load|Page not found|could not be found/i.test(body))throw Error(body);
    record(label,true,'Loaded controls');
   }catch(e){record(label,false,e.message);}
  }
  // Other integrated course navigation should lead to a real page, not #.
  try{
   await go('/financial-algebra/');
   await page.locator('.course-units-title').waitFor({state:'visible',timeout:15000});
   const home=await page.locator('.crumbs a').first().getAttribute('href');
   if(home!=='https://mrksclassroom.com/')throw Error('Financial Algebra home breadcrumb: '+home);
   await go('/financial-algebra/financial/games/index.html?unit=budgeting&game=showdown');
   const back=await page.locator('#courseBack').getAttribute('href');
   const resolved=new URL(back,page.url());
   if(resolved.pathname!=='/financial-algebra/index.html')throw Error('Financial Algebra game Back: '+resolved.pathname);
   record('Financial Algebra home/game navigation',true,'Home and game Back links resolve');
  }catch(e){record('Financial Algebra home/game navigation',false,e.message);}
 }finally{
  await ctx.close();await browser.close();
  report.consoleExceptions=[...new Map(report.consoleExceptions.map(x=>[x.page+'|'+x.message,x])).values()];
  report.missingAssets=[...new Map(report.missingAssets.map(x=>[x.url,x])).values()];
  fs.writeFileSync(output+'/report.json',JSON.stringify(report,null,2));
  let summary='# Grade 5 Chromium release audit\n\n';
  summary+='Passed: '+report.passed.length+'; failed: '+report.failed.length+
    '; browser exceptions: '+report.consoleExceptions.length+'; missing assets: '+report.missingAssets.length+'.\n\n';
  for(const bad of report.failed.slice(0,25))summary+='- FAIL '+bad.label+': '+bad.details+'\n';
  for(const bad of report.consoleExceptions.slice(0,12))summary+='- JS '+bad.page+': '+bad.message+'\n';
  for(const bad of report.missingAssets.slice(0,12))summary+='- HTTP '+bad.status+' '+bad.url+'\n';
  fs.writeFileSync(output+'/summary.md',summary);
  if(process.env.GITHUB_STEP_SUMMARY)fs.appendFileSync(process.env.GITHUB_STEP_SUMMARY,summary);
  console.log(JSON.stringify({passed:report.passed.length,failed:report.failed.length,
    failures:report.failed.slice(0,20),jsExceptions:report.consoleExceptions.slice(0,10),
    missingAssets:report.missingAssets.slice(0,10)},null,2));
  if(report.failed.length||report.consoleExceptions.length||report.missingAssets.length)process.exitCode=1;
 }
}
run().catch(e=>{console.error(e);process.exitCode=1});
