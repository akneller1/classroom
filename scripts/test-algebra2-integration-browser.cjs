'use strict';
const {chromium}=require('playwright'),assert=require('node:assert/strict'),fs=require('node:fs');
const base=process.env.MK_BASE_URL||'http://127.0.0.1:8765';
const units=require('../question-banks/manifest.json').banks.filter(b=>b.courseId==='algebra2').map(b=>b.unitId);
(async()=>{
 const browser=await chromium.launch({headless:true}),page=await browser.newPage(),errors=[],cases=[];
 page.on('pageerror',e=>errors.push(e.message));
 page.on('response',r=>{if(r.status()>=400&&!r.url().includes('favicon'))errors.push(r.status()+' '+r.url())});
 fs.mkdirSync('test-results',{recursive:true});fs.mkdirSync('thumbs/previews/algebra2',{recursive:true});
 try{
 for(const unit of units){
  for(const tool of ['worksheet','menu-assessment']){
   await page.goto(base+'/worksheet-generator/'+tool+'.html#unit=algebra2-'+unit);
   await page.waitForURL('**/bank-printable.html?unit='+unit+'&mode='+(tool==='worksheet'?'worksheet':'assessment'));
   cases.push(unit+'/'+tool+'-entry');
  }
  await page.goto(base+'/index.html#algebra2.'+unit);
  await page.waitForFunction(()=>document.querySelectorAll('a[href*="course-game.html"],a[href*="course-activity.html"]').length>=7);
  assert.equal(await page.locator('.generator-shortcuts a').count(),4);
  for(const mode of ['lesson','worksheet','assessment']){
   await page.goto(base+'/worksheet-generator/bank-printable.html?unit='+unit+'&mode='+mode);
   await page.waitForFunction(()=>document.querySelector('#status').textContent==='Ready to generate.');
   assert.equal(await page.locator('#mode').inputValue(),mode);
   await page.locator('#build').click();await page.locator('#editor').waitFor({state:'visible'});
   assert.ok(await page.locator('#output .sheet:not(.key) .item').count()>0);
   assert.ok(!(await page.locator('#output .sheet:not(.key)').innerText()).includes('"answer":'),'Student output must not serialize answer fields');
   assert.equal(await page.locator('#output .sheet:not(.key) .item').count(),await page.locator('#output .key .item').count());
   cases.push(unit+'/'+mode);
  }
  await page.goto(base+'/worksheet-generator/algebra2-practice.html?unit='+unit);
  await page.locator('#start:not([disabled])').waitFor();await page.locator('#start').click();
  assert.ok(await page.locator('#questions .item').count()>0);cases.push(unit+'/practice');
  for(const game of ['flashcards','connect-four','tic-tac-toe','picture-reveal','showdown','detective','escape-room']){
   await page.goto(base+'/worksheet-generator/algebra2-game.html?unit='+unit+'&game='+game);
   await page.getByRole('button',{name:'Continue',exact:true}).click();
   if(['connect-four','tic-tac-toe'].includes(game))await page.locator('#tGo').click();
   if(game==='tic-tac-toe')await page.getByRole('button',{name:'Square 1',exact:true}).click();
   if(game==='flashcards'){await page.locator('#fcFlip').click();assert.ok(await page.locator('.gm-sol').count());}
   if(game==='connect-four')await page.locator('#c4Lock').waitFor();
   if(game==='picture-reveal')await page.locator('#prCheck').waitFor();
   if(game==='showdown')await page.locator('#sdNew').waitFor();
   if(game==='detective'||game==='escape-room'){await page.locator('#activityStart').click();if(game==='detective'){await page.locator('#start').click();await page.locator('#check').waitFor();}else{await page.getByRole('button',{name:'Begin',exact:true}).click();await page.locator('#go').waitFor();}}
   if(game==='tic-tac-toe')assert.ok(await page.locator('.gm-opts button').count()>=2);
   if(game==='flashcards')await page.locator('#fcCard').click();
   await page.screenshot({path:'thumbs/previews/algebra2/'+unit+'-'+game+'.png'});
   cases.push(unit+'/'+game);
  }
  await page.goto(base+'/worksheet-generator/printables.html#unit=algebra2-'+unit+'&kind=stations');
  await page.waitForFunction(()=>document.querySelector('#prPreview .page')||document.querySelector('#prPreview .mm-page'));
  assert.equal(await page.locator('#prUnit').inputValue(),'algebra2-'+unit);cases.push(unit+'/stations');
 }
 for(const tool of ['worksheet','menu-assessment']){
  await page.goto(base+'/worksheet-generator/'+tool+'.html');
  await page.locator('#mmUnitSel').selectOption('algebra2-probability-statistics');
  await page.waitForURL('**/bank-printable.html?unit=probability-statistics&mode='+(tool==='worksheet'?'worksheet':'assessment'));
  cases.push('global/'+tool+'-selector');
 }
 await page.goto(base+'/worksheet-generator/lesson-planner.html');
 await page.locator('#plCourse').selectOption('algebra2');await page.waitForURL('**/bank-printable.html?mode=lesson');cases.push('global/lesson-selector');
 assert.deepEqual(errors,[]);
 await page.screenshot({path:'test-results/algebra2-integration.png',fullPage:true});
 fs.writeFileSync('test-results/algebra2-browser-coverage.json',JSON.stringify({cases,errors},null,2));
 console.log('PASS '+cases.length+' browser routes across all 11 Algebra 2 units');
 }catch(e){console.error('At '+page.url());await page.screenshot({path:'test-results/algebra2-integration-failure.png',fullPage:true});throw e}finally{await browser.close()}
})().catch(e=>{console.error(e);process.exitCode=1});
