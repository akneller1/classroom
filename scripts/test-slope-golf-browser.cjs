#!/usr/bin/env node
'use strict';
const {chromium}=require('playwright'),assert=require('node:assert/strict');
(async()=>{
 const browser=await chromium.launch({headless:true});
 try{
  const page=await browser.newPage({viewport:{width:1280,height:900}});
  const errors=[];page.on('pageerror',e=>errors.push(e.message));
  await page.goto('http://127.0.0.1:8765/artifacts/slope-links-mini-golf/index.html',{waitUntil:'domcontentloaded'});
  await page.waitForSelector('#scHead button',{timeout:20000});
  assert.equal(await page.locator('#scHead button').count(),9);
  assert.equal(await page.locator('#scHead button:disabled').count(),8);
  await page.locator('#mn').fill('1');await page.locator('#md').fill('2');
  await page.locator('#dirR').click();await page.locator('#clubs button').first().click();
  await page.locator('#power').fill('75');
  assert.equal(await page.locator('#powerLabel').innerText(),'75%');
  await page.locator('[data-mode=challenge]').click();
  assert.match(await page.locator('#modeHelp').innerText(),/no predicted trajectory/i);
  await page.locator('[data-mode=practice]').click();
  const canvas=page.locator('#cv');await canvas.click({position:{x:350,y:150}});
  assert.ok((await page.locator('#mn').inputValue()).length>0);
  await page.locator('#soundBtn').click();
  assert.equal(await page.locator('#soundBtn').getAttribute('aria-pressed'),'false');
  assert.deepEqual(errors,[],'Unexpected browser errors');
  console.log('PASS golf browser interaction and nine-hole progression');
 }finally{await browser.close();}
})().catch(e=>{console.error(e);process.exitCode=1;});
