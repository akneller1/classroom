#!/usr/bin/env node
'use strict';
const { chromium } = require('playwright');
const assert = require('node:assert/strict');
const base = process.env.MK_BASE_URL || 'http://127.0.0.1:8765';
const qs = '?course=algebra2&unit=conic-sections';
const bank={
 schemaVersion:1, courseId:'algebra2', unitId:'conic-sections',
 questions:[
  {id:'browser-mc-1',skillId:'conic-sections-skill-01',level:'cp1',format:'multiple-choice',prompt:'Browser test: choose A',answer:'A',solutionSteps:['Fixture only'],options:[{text:'A',correct:true},{text:'B',correct:false}]},
  {id:'browser-short-1',skillId:'conic-sections-skill-01',level:'cp1',format:'short-answer',prompt:'Browser test: answer one',answer:'1',solutionSteps:['Fixture only']}
 ]
};
async function setup(page,filename){
 await page.route('**/question-banks/manifest.json',route=>route.fulfill({status:200,contentType:'application/json',body:JSON.stringify({version:1,banks:[{courseId:'algebra2',unitId:'conic-sections',path:'question-banks/algebra2/conic-sections.json',approved:true}]})}));
 await page.route('**/question-banks/algebra2/conic-sections.json',route=>route.fulfill({status:200,contentType:'application/json',body:JSON.stringify(bank)}));
 await page.goto(base+'/worksheet-generator/'+filename+qs);
}
async function run(){
 const browser=await chromium.launch({headless:true});
 try{
  const page=await browser.newPage({viewport:{width:1100,height:900}});
  const errors=[];page.on('pageerror',e=>errors.push(e.message));
  await setup(page,'approved-games.html');
  await page.locator('#agApp').waitFor({state:'visible'});
  assert.equal(await page.locator('.ag-cell').count(),9);
  await page.locator('.ag-cell').first().click();
  await page.getByText('Browser test: choose A').waitFor();
  await page.locator('#agOptions button').first().click();
  await page.locator('#agReveal').click();
  assert.equal(await page.locator('.ag-cell[data-owner="1"]').count(),1,'Correct MC should claim first square');
  await page.locator('.ag-cell').nth(1).click();
  await page.locator('#agReveal').click();
  await page.locator('#agWrong').click();
  assert.match(await page.locator('#agTurn').innerText(),/Incorrect/);
  await page.locator('#agGame').selectOption('connect-4');
  assert.equal(await page.locator('.ag-cell').count(),42);
  await page.locator('.ag-cell').first().click();
  await page.locator('#agOptions button').first().click();
  await page.locator('#agReveal').click();
  assert.equal(await page.locator('.ag-cell[data-owner="1"]').last().getAttribute('aria-label'),'Square 36 claimed','Connect 4 should drop to the bottom row');
  await page.locator('#agGame').selectOption('picture-reveal');
  assert.equal(await page.locator('.ag-cell').count(),16);
  await page.locator('.ag-cell').first().click();
  await page.locator('#agOptions button').first().click();
  await page.locator('#agReveal').click();
  assert.equal(await page.locator('.ag-cell[data-owner="revealed"]').count(),1);
  await page.locator('#agLevel').selectOption('honors');
  assert.equal(await page.locator('.ag-cell:enabled').count(),0,'No approved questions should disable board');
  await setup(page,'approved-flashcards.html');
  await page.locator('#afApp').waitFor({state:'visible'});
  assert.match(await page.locator('#afProgress').innerText(),/Card 1 of 2/);
  await page.locator('#afFlip').click();
  await page.getByText('Worked solution').waitFor();
  await page.locator('#afGot').click();
  assert.equal(errors.length,0,'Unexpected browser JavaScript errors: '+errors.join('; '));
  console.log('PASS browser interactions: loading, MC scoring, turn handoff, gravity, reveal tiles, empty bank, flashcard flip');
 }finally{await browser.close()}
}
run().catch(e=>{console.error(e);process.exitCode=1});
