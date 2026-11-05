#!/usr/bin/env node
'use strict';
const {chromium}=require('playwright'),assert=require('node:assert/strict');
const base=process.env.MK_BASE_URL||'http://127.0.0.1:8765';
(async()=>{
 const browser=await chromium.launch({headless:true});
 try{
 const page=await browser.newPage({viewport:{width:1200,height:900}});
 const errors=[];page.on('pageerror',e=>errors.push(e.message));
 const active=async()=>page.evaluate(()=>{
  const catalog=window.LIBRARY.courses.flatMap(c=>c.units.flatMap(u=>u.artifacts));
  return [...document.querySelectorAll('li.card[data-path]')].map(card=>{
   const a=catalog.find(x=>x.path===card.getAttribute('data-path'));
   return {title:card.querySelector('h3')?.textContent,type:a?.type,unitSpecific:a?.unitSpecific,tag:card.querySelector('.game-mode-tag')?.textContent};
  });
 });
 await page.goto(base+'/index.html#activities');
 await page.locator('#browse-category').selectOption('games');
 assert.equal(await page.locator('#browse-category').inputValue(),'games');
 const cards=await active();
 assert.ok(cards.length>0&&cards.every(c=>c.type==='Game'),'Games category displays other content: '+JSON.stringify(cards));
 const formats=await page.locator('#browse-format option').allTextContents();
 assert.ok(formats.some(s=>/topic-specific games/i.test(s)),'Topic-specific games are missing');
 assert.ok(!formats.some(s=>/worksheet|assessment|lesson planner|flashcard|cheat sheet|practice test/i.test(s)),'Non-game formats still shown: '+formats);
 assert.ok((await page.locator('#browse-gameMode option').allTextContents()).includes('Unit-specific'),'Missing Unit-specific option');
 await page.locator('#browse-format').selectOption('topic-games');
 await page.locator('#browse-category').selectOption('study-guides');
 assert.equal(await page.locator('#browse-format').inputValue(),'','Changing category did not reset activity type');
 assert.equal(await page.locator('#browse-gameMode').count(),0,'Game mode should be hidden outside Games');
 assert.ok((await active()).every(c=>c.type!=='Game'),'Study Guides includes Games');
 // results come 24 to a page: collect every page of unit-specific games
 const special=[];
 for(let p=1;p<=10;p++){
  await page.goto(base+'/index.html#activities?category=games&gameMode=Unit-specific'+(p>1?'&page='+p:''));
  await page.locator('li.card').first().waitFor();
  const got=await active();if(p>1&&special.some(x=>x.title===got[0]?.title))break;
  special.push(...got);if(got.length<24)break;
 }
 assert.ok(special.length>=57,'Expected at least 57 unit-specific games (13 earlier games and 44 bank games), found '+special.length);
 assert.ok(special.every(c=>c.type==='Game'&&c.unitSpecific===true&&c.tag==='Unit-specific'),'Missing or incorrect Unit-specific game tags: '+JSON.stringify(special));
 for(const title of ['Slope Links Mini Golf','Zombie Fence'])assert.ok(special.some(x=>x.title.includes(title)),title+' was not tagged');
 await page.goto(base+'/index.html#activities?subject=algebra&unit=algebra.linear-equations-slope&category=games&format=topic-games');
 const matching=await page.locator('li.card h3').allTextContents();
 assert.ok(matching.some(x=>/Matching Game/.test(x)),'Matching Game is missing from Games: '+matching);
 assert.deepEqual(errors,[],'Site browser errors: '+errors.join('; '));
 console.log('PASS Browse Activities: Games category, format options, Unit-specific tags and filter navigation');
 } finally{await browser.close();}
})().catch(e=>{console.error(e);process.exitCode=1;});
