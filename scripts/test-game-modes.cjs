/* Real released engines: student assignments, both board games, all elementary classes. */
const {chromium}=require('playwright'),fs=require('fs'),path=require('path'),http=require('http'),assert=require('node:assert/strict');
const root=path.resolve(process.argv[2]||'_site');
const server=http.createServer((req,res)=>{const f=path.join(root,decodeURIComponent(new URL(req.url,'http://localhost').pathname));if(!fs.existsSync(f)||fs.statSync(f).isDirectory()){res.writeHead(404);return res.end();}res.setHeader('Content-Type',f.endsWith('.js')?'text/javascript':f.endsWith('.json')?'application/json':f.endsWith('.css')?'text/css':'text/html');fs.createReadStream(f).pipe(res);});
(async()=>{await new Promise(r=>server.listen(0,'127.0.0.1',r));const base='http://127.0.0.1:'+server.address().port;const browser=await chromium.launch({headless:true});let checks=0;
try{
 for(let grade=1;grade<=5;grade++){
  const folder=path.join(root,'question-banks','grade'+grade),unit=fs.readdirSync(folder).find(f=>f.endsWith('.json')).replace('.json','');
  for(const game of [grade<5?'four-in-a-row':'connect-four','tic-tac-toe']){
   const page=await browser.newPage(),errors=[];page.on('pageerror',e=>errors.push(e.message));
   // Capture the question supplied by the real bank adapter; answer via its visible controls.
   await page.addInitScript(()=>{document.addEventListener('DOMContentLoaded',()=>{const K=window.MKEL||window.G5;if(!K)return;const original=K.card;K.card=function(host,p,o){window.__question=p;return original(host,p,o);};});});
   await page.goto(`${base}/grade${grade}/worksheet-generator/grade${grade}-games.html?unit=${unit}&game=${game}&student=1&level=cp1&mode=class2`);
   await page.locator('.kid-play .kid-big-play').click();
   const prefix=grade<5?'el':'g5';await page.waitForSelector('.'+prefix+'-stage');
   await page.waitForFunction(()=>!!window.__question);
   assert.match(await page.locator('.'+prefix+'-hud').innerText(),/Computer/,'Student URL must override a team mode');
   // Computer always succeeds for a deterministic turn-transition check.
   await page.evaluate(()=>{MKSOLOAI.answers=()=>true;});
   const right=await page.evaluate(()=>__question.options.findIndex(o=>o.correct));
   await page.locator('.'+prefix+'-choice').nth(right).click();
   const board=page.locator('.'+prefix+'-board button:enabled');assert.ok(await board.count()>0,'Correct answer unlocks board');
   await board.first().click();await page.waitForFunction(()=>document.body.textContent.includes('The computer played'));
   assert.equal(await page.locator('.'+prefix+'-board button').filter({hasText:game==='tic-tac-toe'?'O':'●'}).count(),game==='tic-tac-toe'?1:2);
   // Wrong answers pass to CPU without claiming a square or offering a steal.
   const wrong=await page.evaluate(()=>__question.options.findIndex(o=>!o.correct));await page.locator('.'+prefix+'-choice').nth(wrong).click();
   assert.equal(await page.locator('.'+prefix+'-board button:enabled').count(),0);
   await page.getByRole('button',{name:'Continue →',exact:true}).click();await page.waitForFunction(()=>document.body.textContent.includes('The computer played'));
   assert.deepEqual(errors,[]);checks++;await page.close();
  }
  const page=await browser.newPage();await page.goto(`${base}/grade${grade}/worksheet-generator/grade${grade}-games.html?unit=${unit}&game=${grade<5?'rocket-race':'math-race'}&student=1&level=cp1`);
  await page.locator('.kid-play .kid-big-play').click();
  await page.getByText('This game requires teams.',{exact:false}).waitFor();assert.equal(await page.locator('.el-stage,.g5-stage').count(),0);await page.close();
 }
 console.log('PASS: '+checks+' elementary board games; correct answers, misses, automatic computer turns, and team-only student-link rejection.');
}finally{await browser.close();server.close();}})().catch(e=>{console.error(e);server.close();process.exitCode=1;});
