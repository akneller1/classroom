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
  if(game==='rocket'||game==='laser'){
   await page.waitForFunction(()=>bankQuestion&&bankQuestion.options&&bankQuestion.options.length>=2,{timeout:20000});
   const correctIndex=await page.evaluate(()=>bankQuestion.options.findIndex(x=>x.ok));
   await page.locator('input[name="bankAnswer"]').nth(correctIndex).check();
  }else{
   const result=await page.evaluate(()=>({q:current,correct:answerFor(current),game:key}));
   for(let i=0;i<result.correct.length;i++){
    const el=page.locator('#f'+i),tag=await el.evaluate(e=>e.tagName),val=result.correct[i];
    if(tag==='SELECT')await el.selectOption(['≥','≤'].includes(val)?'Closed':'Open');
    else await el.fill(String(val));
   }
  }
  await page.locator('#action').click();
  assert.equal(await page.locator('#next').isVisible(),true,'Next button should appear in '+game);
  assert.deepEqual(failures,[],'Browser errors in '+game);
  await page.close();
 }
 console.log('PASS seven arcade routes, valid turns, interaction controls and no page errors');
 }finally{await browser.close();}
})().catch(e=>{console.error(e);process.exitCode=1});
