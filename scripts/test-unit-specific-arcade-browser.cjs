#!/usr/bin/env node
'use strict';
const {chromium}=require('playwright');
const assert=require('node:assert/strict');
(async()=>{
 const browser=await chromium.launch({headless:true});
 try{
 const cases=['rocket','inequality','laser','mirror','cannon','portal','catapult'];
 for(const game of cases){
  const page=await browser.newPage({viewport:{width:1024,height:800}});
  const failures=[];page.on('pageerror',e=>failures.push(e.message));
  await page.goto('http://127.0.0.1:8765/artifacts/math-arcade/index.html?game='+game,{waitUntil:'domcontentloaded'});
  await page.locator('#board').waitFor();
  assert.match(await page.locator('#heading').innerText(),/Rocket|Inequality|Laser|Mirror|Cannon|Portal|Catapult/);
  await page.waitForFunction(()=>bankQuestion&&(bankQuestion.options?.length>=2||bankQuestion.typed!==null&&bankQuestion.typed!==undefined),{timeout:25000});
  const answer=await page.evaluate(()=>({idx:bankQuestion.options?.findIndex(x=>x.ok),typed:bankQuestion.typed}));
  if(answer.typed!==null&&answer.typed!==undefined)await page.locator('#bankTyped').fill(answer.typed);
  else await page.locator('input[name="bankAnswer"]').nth(answer.idx).check();
  await page.locator('#action').click();
  assert.equal(await page.locator('#next').isVisible(),true,'Next button should appear in '+game);
  assert.deepEqual(failures,[],'Browser errors in '+game);
  await page.close();
 }
 console.log('PASS seven arcade routes, valid turns, interaction controls and no page errors');
 }finally{await browser.close();}
})().catch(e=>{console.error(e);process.exitCode=1});
