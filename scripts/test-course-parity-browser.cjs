'use strict';
const {chromium}=require('playwright'),assert=require('node:assert/strict'),fs=require('node:fs'),vm=require('node:vm');
const base=process.env.MK_BASE_URL||'http://127.0.0.1:8765';
const ctx={window:{}};vm.runInNewContext(fs.readFileSync('data.js','utf8'),ctx);const library=ctx.window.LIBRARY;const published=require('../question-banks/manifest.json').banks;
(async()=>{
 const browser=await chromium.launch({headless:true}),page=await browser.newPage({viewport:{width:1180,height:820}}),errors=[],cases=[];
 page.on('pageerror',e=>errors.push(e.message));
 async function open(course,unit,game){await page.goto(base+'/worksheet-generator/'+(['detective','escape-room'].includes(game)?'course-activity':'course-game')+'.html?course='+course+'&unit='+unit+'&game='+game);await page.getByRole('button',{name:'Continue',exact:true}).click();}
 async function escape(course,unit){
  await open(course,unit,'escape-room');await page.locator('#activityStart').click();await page.getByRole('button',{name:'Begin',exact:true}).click();
  const room=await page.evaluate(()=>window.MK_ESCAPE_ROOM);assert.equal(room.stages.length,5);assert.ok(room.stages.some(s=>s.type==='cipher'));assert.ok(room.stages.some(s=>s.type==='order'));
  for(let i=0;i<5;i++){
   const stage=room.stages[i];await page.waitForFunction(i=>window.MK_ESCAPE_STATE().stage===i,i);
   if(stage.type==='fields'){
    if(stage.ui==='dial'){for(let n=0;n<stage.fields[0].answer;n++)await page.locator('.dialbox button').first().click();}
    else for(const [j,f] of stage.fields.entries())await page.locator('#f'+j).fill(String(f.answer));
    await page.locator('#go').click();
   }else if(stage.type==='cipher'){
    assert.equal(await page.locator('#shiftTools').isVisible(),false);
    const before=await page.evaluate(()=>window.MK_ESCAPE_STATE().t);
    if(stage.sourceChoices)await page.locator('[data-cipher-choice="'+stage.sourceCorrect+'"]').click();
    await page.locator('#shiftGuess').fill(String((stage.shift+1)%26));await page.getByRole('button',{name:/Lock shift/}).click();
    assert.equal(await page.locator('#shiftTools').isVisible(),false);const after=await page.evaluate(()=>window.MK_ESCAPE_STATE().t);assert.ok(before-after>=30&&before-after<=33,'Wrong shift must cost 30 seconds');
    await page.locator('#shiftGuess').fill(String(stage.shift));await page.getByRole('button',{name:/Lock shift/}).click();assert.equal(await page.locator('#shiftTools').isVisible(),true);
    await page.locator('#w').fill(stage.answer);await page.locator('#go').click();
   }else if(stage.type==='classify'){for(const [j,answer] of stage.answer.entries())await page.locator('#sw'+j+' button').nth(answer).click();await page.locator('#go').click();}
   else if(stage.type==='order'){
    for(let target=0;target<stage.steps.length;target++){let order=await page.evaluate(()=>window.MK_ESCAPE_STATE().st.ord);let index=order.indexOf(target);while(index>target){await page.locator('.ord').nth(index).getByRole('button',{name:'▲',exact:true}).click();index--;}}
    await page.locator('#go').click();
   }else{await page.locator('[data-choice="'+stage.answer+'"]').click();await page.locator('#go').click();}
  }
  await page.locator('#w').fill(room.word);await page.locator('#go').click();await page.getByRole('heading',{name:'You escaped!',exact:true}).waitFor();cases.push(course+'/'+unit+'/escape-complete');
 }
 async function mystery(course,unit){
  await open(course,unit,'detective');await page.locator('#activityStart').click();await page.locator('#start').click();const data=await page.evaluate(()=>window.MK_MYSTERY_CASE);
  assert.equal(data.questions.length,10);assert.ok(await page.getByRole('heading',{name:'Case board',exact:true}).isVisible());
  for(let i=0;i<10;i++){
   const answer=data.questions[i].answer.v;
   if(i===0){const wrong=(answer+1)%data.questions[i].options.length;for(let k=0;k<2;k++){await page.locator('[data-source-choice="'+wrong+'"]').click();await page.locator('#check').click();}await page.locator('#hint').click();assert.ok(await page.locator('.solution').isVisible());}
   await page.locator('[data-source-choice="'+answer+'"]').click();await page.locator('#check').click();await page.locator('#next').click();
  }
  for(const key of ['p','l','m'])await page.locator('button.card[data-t="'+key+'"][data-id="'+data.culprit[key]+'"]').click();
  await page.locator('#accuse').click();await page.getByRole('heading',{name:'Case closed!',exact:true}).waitFor();cases.push(course+'/'+unit+'/mystery-complete');
 }
 async function steal(course,unit){
  await open(course,unit,'connect-four');await page.locator('#tGo').click();
  let s=await page.evaluate(()=>window.MKGAMES._state());const correct=s.it.options.findIndex(o=>o.ok),wrong=s.it.options.findIndex(o=>!o.ok);const original=s.it.id;
  await page.locator('[data-opt="'+wrong+'"]').click();await page.locator('#c4Lock').click();assert.ok(await page.locator('#c4Steal').isVisible());assert.equal(await page.locator('.gm-sol').count(),0,'Solution must remain hidden before the steal');
  await page.locator('#c4Steal').click();assert.equal(await page.locator('[data-opt="'+wrong+'"]').isDisabled(),true);assert.equal(await page.evaluate(()=>window.MKGAMES._state().it.id),original);
  await page.locator('[data-opt="'+correct+'"]').click();await page.locator('#c4Lock').click();await page.locator('.c4-hole[data-col="1"]').first().click();
  s=await page.evaluate(()=>window.MKGAMES._state());assert.equal(s.board[5][1],'R');await page.locator('#c4Next').click();assert.equal(await page.evaluate(()=>window.MKGAMES._state().turn),'L');
  s=await page.evaluate(()=>window.MKGAMES._state());await page.locator('[data-opt="'+s.it.options.findIndex(o=>!o.ok)+'"]').click();await page.locator('#c4Lock').click();await page.locator('#c4Pass').click();await page.locator('#c4Next').click();assert.equal(await page.evaluate(()=>window.MKGAMES._state().turn),'R');
  s=await page.evaluate(()=>window.MKGAMES._state());const wrongs=s.it.options.map((o,i)=>o.ok?-1:i).filter(i=>i>=0);await page.locator('[data-opt="'+wrongs[0]+'"]').click();await page.locator('#c4Lock').click();await page.locator('#c4Steal').click();await page.locator('[data-opt="'+wrongs[1]+'"]').click();await page.locator('#c4Lock').click();await page.locator('#c4Next').click();assert.equal(await page.evaluate(()=>window.MKGAMES._state().turn),'L');cases.push(course+'/'+unit+'/steal-pass-miss');
 }
 try{
 for(const u of library.courses.find(c=>c.id==='algebra2').units){await mystery('algebra2',u.id);await escape('algebra2',u.id);}
 for(const [c,u] of [['algebra','foundations-algebra'],['geometry','foundations-geometry'],['algebra2','conic-sections']]){await steal(c,u);if(c!=='algebra2'){await mystery(c,u);await escape(c,u);}}
 for(const course of library.courses.filter(c=>['math6','prealgebra7','prealgebra'].includes(c.id)))for(const middleUnit of course.units){const unit=middleUnit.id,expected=published.some(b=>b.courseId===course.id&&b.unitId===unit&&b.approved);fs.mkdirSync('thumbs/previews/'+course.id,{recursive:true});for(const game of ['flashcards','connect-four','tic-tac-toe','picture-reveal','showdown','detective','escape-room']){await open(course.id,unit,game);if(!expected&&['detective','escape-room'].includes(game)){assert.match(await page.locator('#activityStatus').innerText(),/not available/);}else if(['connect-four','tic-tac-toe'].includes(game))assert.ok(await page.locator('#tGo').isVisible());else if(!expected)await page.getByRole('status').waitFor();assert.equal(await page.evaluate(c=>window.MK_QUESTION_BANKS.available(c,window.MK_COURSE_ACTIVITY_SOURCE.unit.id),course.id),expected);await page.screenshot({path:'thumbs/previews/'+course.id+'/'+unit+'-'+game+'.png'});cases.push(course.id+'/'+unit+'/'+game+(expected?'/bank-ready':'/empty-bank'));}}
 await page.goto(base+'/index.html#algebra2.conic-sections');await page.waitForFunction(()=>document.querySelectorAll('#algebra-games + .cards a[href*="course-"]').length>=6);
 const thumbs=await page.locator('#algebra-games + .cards .thumb img').evaluateAll(imgs=>imgs.map(i=>i.src));assert.equal(new Set(thumbs).size,thumbs.length);
 assert.deepEqual(errors,[]);fs.mkdirSync('test-results',{recursive:true});fs.writeFileSync('test-results/course-parity.json',JSON.stringify({cases,errors},null,2));console.log('PASS '+cases.length+' complete game and future-course parity scenarios');
 }catch(e){console.error(page.url());await page.screenshot({path:'test-results/course-parity-failure.png',fullPage:true});throw e}finally{await browser.close()}
})().catch(e=>{console.error(e);process.exitCode=1});
