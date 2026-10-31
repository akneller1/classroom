#!/usr/bin/env node
'use strict';
const {chromium}=require('playwright');
const assert=require('node:assert/strict');
(async()=>{
 const browser=await chromium.launch({headless:true});
 try{
  const page=await browser.newPage({viewport:{width:1180,height:900},acceptDownloads:true});
  const errors=[];page.on('pageerror',e=>errors.push(e.message));
  await page.goto((process.env.MK_BASE_URL||'http://127.0.0.1:8765')+'/worksheet-generator/legacy-review.html');
  await page.waitForFunction(() => document.querySelector('#reviewTopic').options.length > 0);
  assert.ok(await page.locator('#reviewTopic option').count()>0);
  await page.locator('#reviewLoad').click();
  await page.locator('#reviewStatus').waitFor();
  assert.match(await page.locator('#reviewStatus').innerText(),/generated samples|Unavailable/);
  await page.locator('#reviewCourse').selectOption('prealgebra7');
  await page.locator('#reviewTopic').selectOption('evaluating-expressions');
  await page.locator('#reviewLevel').selectOption('cp1');
  await page.locator('#reviewLoad').click();
  assert.match(await page.locator('#reviewStatus').innerText(),/generated samples/);
  assert.ok(await page.locator('.review-card').count()>0);
  await page.locator('#stageCheck').click();
  assert.match(await page.locator('#stageStatus').innerText(),/Review at least six|Every question needs/);
  assert.ok(await page.locator('#stagePanel').isVisible());
  await page.locator('.review-card details').first().locator('summary').click();
  assert.ok(await page.locator('.review-card .answer').first().isVisible());
  await page.locator('.review-card select').first().selectOption('revise');
  await page.locator('.review-card input').first().fill('Check grade-level arithmetic.');
  const download=page.waitForEvent('download');await page.locator('#reviewExport').click();
  const file=await download;assert.equal(file.suggestedFilename(),'legacy-reuse-review.json');
  const path=await file.path();const data=JSON.parse(require('node:fs').readFileSync(path,'utf8'));
  assert.equal(data.approved,false);
  assert.equal(data.results[0].review.status,'revise');
  assert.equal(data.results[0].review.note,'Check grade-level arithmetic.');
  await page.goto((process.env.MK_BASE_URL||'http://127.0.0.1:8765')+'/worksheet-generator/grade-practice.html');
  await page.locator('#course').selectOption('prealgebra7');
  await page.locator('#topic').selectOption('evaluating-expressions');
  await page.locator('#generate').click();
  assert.match(await page.locator('#status').innerText(),/draft questions generated/);
  assert.ok(await page.locator('#practice button').count()>1);
  await page.setViewportSize({width:375,height:812});
  assert.ok(await page.locator('#course').isVisible());
  assert.equal(errors.length,0,errors.join('; '));
  console.log('PASS real browser course/skill selection, generated questions, reviewer notes, JSON download and mobile viewport');
 }finally{await browser.close()}
})().catch(e=>{console.error(e);process.exitCode=1});
