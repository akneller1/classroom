#!/usr/bin/env node
'use strict';
const assert=require('node:assert/strict');
const {chromium}=require('playwright');
(async()=>{
 const browser=await chromium.launch({headless:true});
 try{
  const page=await browser.newPage();
  const errors=[];page.on('pageerror',e=>errors.push(e.message));
  const base=process.env.MK_BASE_URL||'http://127.0.0.1:8765';
  await page.goto(base+'/worksheet-generator/bank-printable.html?unit=functions-transformations');
  await page.waitForFunction(()=>document.querySelector('#status').textContent.includes('Ready to generate.'),{timeout:20000});
  assert.equal(await page.locator('#sectionList .section-config').count(),8);
  await page.locator('#sectionList .section-config').first().getByRole('button',{name:'Duplicate'}).click();
  assert.equal(await page.locator('#sectionList .section-config').count(),9);
  await page.locator('#sectionList .section-config').first().getByRole('button',{name:'↓'}).click();
  await page.locator('#sectionList .section-config').first().locator('input[aria-label^="Section"]').fill('Warm-up');
  await page.locator('#count').fill('20');
  await page.locator('#versions').fill('2');
  await page.locator('#build').click();
  await page.locator('#editor').waitFor({state:'visible'});
  assert.equal(await page.locator('#output .sheet:not(.key)').count(),2);
  assert.equal(await page.locator('#output .sheet.key').count(),2);
  assert.ok(await page.locator('#output .section-print h3').count()>=9);
  const first=page.locator('#editItems textarea').first();
  await first.fill('Temporary edited question');
  await page.locator('#resetEdits').click();
  assert.equal(await page.locator('#output .sheet:not(.key) .item').count()>0,true);
  assert.equal(await page.locator('#output .sheet.key .item').count()>0,true);
  await page.locator('#currentVersion').selectOption('1');
  await page.locator('#refreshVersion').click();
  assert.equal(await page.locator('#output .sheet:not(.key)').count(),2);
  assert.deepEqual(errors,[]);
  console.log('PASS Algebra 2 generator browser: sections, duplication, ordering, versions, edits, reset, keys');
 }finally{await browser.close()}
})().catch(e=>{console.error(e);process.exitCode=1});
