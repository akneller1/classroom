'use strict';
const assert=require('node:assert/strict'),fs=require('node:fs'),path=require('node:path'),http=require('node:http'),vm=require('node:vm');
const {chromium}=require('playwright');
const root=path.resolve(__dirname,'../../..');
const context={window:{}};vm.runInNewContext(fs.readFileSync(path.join(root,'data.js'),'utf8'),context);
const entries=[];
for(const course of context.window.LIBRARY.courses)for(const unit of course.units)for(const a of unit.artifacts){
 const types=Array.isArray(a.type)?a.type:[a.type];
 if(a.path.endsWith('/index.html') && !/escape-room|jeopardy|showdown|connect-four|inequality-four|tic-tac-toe/.test(a.path) && (types.includes('Game')||/flashcards/.test(a.path))) {
  assert(fs.readFileSync(path.join(root,a.path),'utf8').includes('games/skill-setup.js'),'Missing share setup: '+a.path);
  if(!entries.some(e=>e.path===a.path))entries.push({...a,course:course.id,unit:unit.id});
 }
}
const server=http.createServer((req,res)=>{
 if(req.url==='/favicon.ico'){res.writeHead(204).end();return;}
 const file=path.join(root,decodeURIComponent(req.url.split('?')[0]));
 if(!file.startsWith(root+path.sep)){res.writeHead(403).end();return;}
 fs.readFile(file,(e,data)=>{if(e){res.writeHead(404).end();return;}res.setHeader('Content-Type',file.endsWith('.js')?'text/javascript':file.endsWith('.css')?'text/css':file.endsWith('.html')?'text/html':'application/octet-stream');res.end(data);});
});
(async()=>{
 await new Promise(r=>server.listen(0,'127.0.0.1',r));const base=`http://127.0.0.1:${server.address().port}`;
 const browser=await chromium.launch(process.env.CHANNEL?{channel:process.env.CHANNEL}:{});
 try{
  let count=0;
  for(const entry of entries.filter(e=>!process.env.MATCH||e.path.includes(process.env.MATCH))){
   const page=await browser.newPage(),errors=[];page.on('pageerror',e=>errors.push(e.message));
   try{
    await page.goto(`${base}/activity.html?path=${encodeURIComponent(entry.path)}`);
    await page.click('#share-student');
    assert.equal(await page.locator('#game-student-link').count(),0,'no generic link before skill selection');
    const setup=page.frameLocator('#game-share-dialog iframe'),dialog=setup.locator('dialog.teacher-skills');
    await dialog.waitFor();await dialog.getByRole('button',{name:'Clear All',exact:true}).click();
    assert(await dialog.getByRole('button',{name:'Generate student link',exact:true}).isDisabled());
    await dialog.locator('input[type=checkbox]').last().check();
    const id=await dialog.locator('input:checked').getAttribute('value');
    const selectedLabel=(await dialog.locator('label').last().textContent()).trim();
    await dialog.getByRole('button',{name:'Generate student link',exact:true}).click();
    const input=page.locator('#game-student-link');await input.waitFor();const link=await input.inputValue(),url=new URL(link);
    assert.equal(url.searchParams.get('path'),entry.path);assert.equal(url.searchParams.get('student'),'1');assert.deepEqual(JSON.parse(url.searchParams.get('skills')),[id]);
    await page.goto(link);
    await page.waitForFunction(()=>{const f=document.querySelector('.activity-frame');return f&&f.contentWindow.TeacherSkills&&!f.contentDocument.querySelector('.gm-loading');});
    const frame=page.frames().find(f=>f.url().includes('/artifacts/'));
    assert.equal(await frame.locator('dialog.teacher-skills').count(),0,'student bypasses teacher picker');
    const skills=await frame.evaluate(()=>{
      if(typeof MKGAMES!=='undefined'&&MKGAMES._state){const s=MKGAMES._state();return (s.cards||s.items||[]).map(q=>q.skill);}
      if(typeof Q!=='undefined'&&Array.isArray(Q))return Q.map(q=>q.skill);
      if(typeof CARDS!=='undefined')return CARDS.map(q=>q.skill);
      if(typeof CASE!=='undefined')return Array.from(teacherQuestions).map(q=>TeacherSkills.questionLabel(q));
      if(typeof levels!=='undefined')return levels.map(L=>L.challenge);
      if(typeof LEVELS!=='undefined')return LEVELS.map(L=>L.tip);
      if(typeof HOLES!=='undefined')return ['Slope'];
      return [];
    });
    assert(skills.length,entry.path+' has student questions/levels');assert.equal(new Set(skills).size,1,entry.path+' restricts all student questions');
    const isGenerated=fs.readFileSync(path.join(root,entry.path),'utf8').includes('games/games.js');
    if(isGenerated)assert(skills.every(s=>s===id));
    else {
      const names=await frame.evaluate(items=>items.map(name=>{const e=document.createElement('div');e.innerHTML=name;return e.textContent.replace(/\s+/g,' ').trim();}),skills);
      assert(names.every(name=>name===selectedLabel),'student bank matches chosen label');
    }
    await page.reload();await page.waitForFunction(()=>{const f=document.querySelector('.activity-frame');return f&&f.contentWindow.TeacherSkills&&!f.contentDocument.querySelector('.gm-loading');});
    assert.equal(await page.frameLocator('.activity-frame').locator('dialog.teacher-skills').count(),0,'reload keeps assignment');
    assert.deepEqual(errors,[],entry.path+' browser errors');count++;console.log('PASS '+entry.path);
   }finally{await page.close();}
  }
  console.log('PASS '+count+' individual games: share picker → configured link → filtered student game → reload');
 }finally{await browser.close();server.close();}
})().catch(e=>{console.error(e);server.close();process.exitCode=1;});
