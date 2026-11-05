#!/usr/bin/env node
'use strict';
const {chromium}=require('playwright');
const assert=require('node:assert/strict');
(async()=>{
 const browser=await chromium.launch({headless:true});
 try{
 const cases=['rocket','inequality','laser','mirror','cannon','portal','catapult','equation-launch','lava-bridge','system-lasers','function-gates','tangent-cannon'];
 for(const game of cases){
  const page=await browser.newPage({viewport:{width:1024,height:800}});
  const failures=[];page.on('pageerror',e=>failures.push(e.message));
  await page.goto('http://127.0.0.1:8765/artifacts/math-arcade/index.html?game='+game,{waitUntil:'domcontentloaded'});
  await page.locator('#board').waitFor();
  assert.match(await page.locator('#heading').innerText(),/Rocket|Inequality|Laser|Mirror|Cannon|Portal|Catapult|Launch|Lava|Gates/);
  if(game==='rocket'||game==='inequality'){
    const math=await page.evaluate(()=>({
      fraction:renderArcadeMath(String.raw`Solve \\frac{x}{3}+3=4.`),
      choice:renderArcadeMath('⟨x=3⟩'),
      inequality:renderArcadeMath(String.raw`x \\geq 4`),
      katexLoaded:!!window.katex
    }));
    assert.ok(math.katexLoaded,'KaTeX must load for '+game);
    assert.ok(math.fraction.includes('katex'),'Fraction must be rendered as math');
    assert.ok(math.choice.includes('katex'),'Option must be rendered as math');
    assert.ok(math.inequality.includes('katex'),'Inequality must be rendered as math');
    assert.ok(!math.fraction.includes('\\\\frac'),'No raw TeX fraction in user-visible math');
  }
  if(game!=='catapult'){
    assert.equal(await page.locator('#fields').isVisible(),false,'Legacy fields should not appear with bank questions in '+game);
    assert.equal(await page.locator('#controls').innerText().then(x=>x.includes('Boundary x =')),false);
  }
  if(game==='catapult') {
    const answers=await page.evaluate(()=>answerFor(current));
    for(let i=0;i<answers.length;i++) await page.locator('#f'+i).fill(String(answers[i]));
  } else {
    await page.waitForFunction(()=>bankQuestion&&(bankQuestion.options?.length>=2||bankQuestion.typed!=null),{timeout:25000});
    const answer=await page.evaluate(()=>({
      idx:bankQuestion.options?.findIndex(x=>x.ok),
      typed:bankQuestion.typed==null?null:String(bankQuestion.typed),
      hasOptions:!!bankQuestion.options?.length
    }));
    if(answer.hasOptions) await page.locator('input[name="bankAnswer"]').nth(answer.idx).check();
    else await page.locator('#bankTyped').fill(answer.typed);
  }
  await page.locator('#action').click();
  assert.equal(await page.locator('#next').isVisible(),true,'Next button should appear in '+game);
  assert.deepEqual(failures,[],'Browser errors in '+game);
  await page.close();
 }
 console.log('PASS twelve arcade routes, valid turns, interaction controls and no page errors');
 }finally{await browser.close();}
})().catch(e=>{console.error(e);process.exitCode=1});
