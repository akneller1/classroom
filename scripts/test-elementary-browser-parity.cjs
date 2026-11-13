#!/usr/bin/env node
/* Elementary release browser gate: keeps the problems from the Grade 3/4 rollouts
   from being introduced again when adding Grades 1 and 2. Run against the
   assembled Classroom artifact rather than raw course source. */
'use strict';
const fs=require('node:fs'),path=require('node:path'),http=require('node:http'),assert=require('node:assert/strict');
const {chromium}=require('playwright');
const root=path.resolve(process.argv[2]||'_site');
const types={'.html':'text/html','.js':'text/javascript','.json':'application/json','.css':'text/css','.svg':'image/svg+xml','.png':'image/png','.jpg':'image/jpeg','.woff2':'font/woff2'};
const server=http.createServer((req,res)=>{
 let u;try{u=decodeURIComponent(new URL(req.url,'http://localhost').pathname)}catch{res.writeHead(400);res.end();return;}
 const file=path.resolve(root,'.'+u+(u.endsWith('/')?'index.html':''));
 if(!file.startsWith(root+path.sep)||!fs.existsSync(file)||!fs.statSync(file).isFile()){res.writeHead(404);res.end('not found');return;}
 res.writeHead(200,{'content-type':types[path.extname(file)]||'application/octet-stream'});fs.createReadStream(file).pipe(res);
});
(async()=>{
 await new Promise(resolve=>server.listen(0,'127.0.0.1',resolve));
 const base='http://127.0.0.1:'+server.address().port+'/';
 const browser=await chromium.launch({headless:true});
 const page=await browser.newPage();
 const errors=[];
 page.on('pageerror',e=>errors.push(e.message));
 try{
  await page.goto(base+'#grade3.multiplication-meaning',{waitUntil:'load'});
  await page.waitForSelector('[data-path*="grade3-games.html"]',{timeout:20000});
  const card=page.locator('[data-path*="grade3-games.html"]').first();
  const href=await card.locator('a[href*="grade3-games.html"]').first().getAttribute('href');
  assert.ok(href && /^grade3\/worksheet-generator\/grade3-games\.html\?/.test(href),'Grade 3 game card must link to the player directly, not activity.html');
  await card.locator('button.share-student').click();
  const dialog=page.locator('#integrated-skill-share-dialog');
  await dialog.waitFor({state:'visible',timeout:10000});
  const skillBoxes=dialog.locator('fieldset input[type=checkbox]');
  assert.ok(await skillBoxes.count()>=2,'Skill selector must show Grade 3 unit skills');
  await skillBoxes.nth(1).uncheck();
  await dialog.getByText('Generate student link',{exact:true}).click();
  const url=await dialog.locator('input[aria-label="Student link"]').inputValue();
  const destination=new URL(url);
  assert.equal(destination.searchParams.get('student'),'1');
  assert.equal(destination.searchParams.get('level'),'cp1');
  const skills=JSON.parse(destination.searchParams.get('skills'));
  assert.equal(skills.length,(await skillBoxes.count())-1);
  await dialog.getByText('Cancel',{exact:true}).click();
  const game=await browser.newPage();const gameErrors=[];
  game.on('pageerror',e=>gameErrors.push(e.message));
  await game.goto(new URL(href,base).href,{waitUntil:'load'});
  await game.waitForSelector('.el-setup, .el-stage, dialog.teacher-skills',{timeout:25000});
  assert.deepEqual(gameErrors,[],'Grade 3 game page errors');
  await game.close();
  const planner=await browser.newPage();
  await planner.goto(base+'worksheet-generator/lesson-planner.html#unit=grade3-multiplication-meaning',{waitUntil:'load'});
  await planner.waitForFunction(()=>window.MKPLAN_COURSE==='grade3',{timeout:25000});
  for(const grade of ['grade5','grade3']){
   await planner.evaluate(next=>{location.hash='#course='+next+'&day=1';},grade);
   await planner.waitForFunction(next=>window.MKPLAN_COURSE===next,grade,{timeout:25000});
  }
  await planner.close();
  assert.deepEqual(errors,[],'Homepage JS errors');
  console.log('PASS Grade 3: direct game routing, skill picker and filtered student link, game boot, planner Grade 3→5→3 switching');
 }finally{await page.close();await browser.close();server.close();}
})().catch(e=>{console.error(e);server.close();process.exitCode=1;});
