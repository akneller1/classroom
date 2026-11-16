// Verify actual native student gameplay, speech controls, keypad input and earned rewards.
const fs=require('node:fs'),path=require('node:path'),http=require('node:http'),assert=require('node:assert/strict'),{chromium}=require('playwright');
const root=path.resolve(process.argv[2]||'_site'),types={'.html':'text/html','.js':'text/javascript','.json':'application/json','.css':'text/css','.svg':'image/svg+xml','.png':'image/png','.woff2':'font/woff2'};
const server=http.createServer((req,res)=>{const f=path.resolve(root,'.'+decodeURIComponent(req.url.split('?')[0]));if(!f.startsWith(root+path.sep)||!fs.existsSync(f)||!fs.statSync(f).isFile()){res.writeHead(404).end();return}res.setHeader('Content-Type',types[path.extname(f)]||'application/octet-stream');fs.createReadStream(f).pipe(res)});
(async()=>{await new Promise(r=>server.listen(0,'127.0.0.1',r));const browser=await chromium.launch();const base='http://127.0.0.1:'+server.address().port+'/';try{
 for(let grade=1;grade<=5;grade++){
  const unit=fs.readdirSync(path.join(root,'question-banks','grade'+grade)).find(f=>f.endsWith('.json')).replace('.json','');
  const page=await browser.newPage({viewport:{width:390,height:844}}),errors=[];page.on('pageerror',e=>errors.push(e.message));
  await page.goto(base+'grade'+grade+'/worksheet-generator/grade'+grade+'-games.html?unit='+unit+'&level=cp1&student=1');
  await page.locator('.kid-play .kid-big-play').waitFor();assert.equal(await page.locator('.el-q,.g5-q').count(),0,'Questions must wait for Play');
  await page.evaluate(()=>{const k=window.MKEL||window.G5,card=k.card;k.card=function(host,p,opts){window.currentQuestion=p;return card(host,p,opts)}});
  await page.locator('.kid-play .kid-big-play').click();
  await page.locator('.el-q,.g5-q').waitFor();await page.locator('.el-read-aloud').waitFor();
  for(let round=0;round<100&&!await page.locator('.kid-finish').count();round++){
   const q=await page.evaluate(()=>window.currentQuestion);
   if(q.kind==='mc')await page.locator('.el-choice,.g5-choice').nth(q.options.findIndex(o=>o.correct)).click();
   else if(q.kind==='sel'){for(let i=0;i<q.options.length;i++)if(q.options[i].correct)await page.locator('.el-choice,.g5-choice').nth(i).click();await page.getByRole('button',{name:'Check',exact:true}).click()}
   else if(q.kind==='sa'){
    const input=page.getByRole('textbox',{name:'Your answer',exact:true});
    if(grade<=2&&await page.locator('.kid-pad').count()){
     const answer=String(q.answer).replace(/,(?=\d{3})/g,'');const kind=await page.evaluate(()=>MKKid.kind(currentQuestion.answer));const target=kind==='number-unit'?answer.match(/^\d+/)[0]:answer;
     const keys=target.replace(/ and /g,'|and|').replace(/\s*(AM|PM)$/,'|$1|').split('|').flatMap(x=>['and','AM','PM'].includes(x)?[x]:[...x]);
     for(const key of keys)await page.locator('.kid-pad').getByRole('button',{name:({' ':'Space','<':'less than','>':'greater than','=':'equals','/':'fraction bar'}[key]||key),exact:true}).click();
     await page.locator('.kid-pad').getByRole('button',{name:'Check',exact:true}).click();
    }else{await input.fill(String(q.answer));await page.getByRole('button',{name:'Check',exact:true}).click()}
   }else throw Error('Unexpected multipart in solo game');
   await page.locator('.el-q-tools button,.g5-q-tools button').filter({hasText:/Keep going|Next|Continue/}).last().click();
  }
  await page.locator('.kid-finish').waitFor();assert(await page.locator('.kid-sticker').getAttribute('src').then(x=>x.endsWith('trophy.svg')),'Perfect round earns a trophy');
  assert(await page.locator('.kid-book img').count()>0);assert.deepEqual(errors,[],'Grade '+grade+' player errors');
  assert.equal(await page.evaluate(()=>document.documentElement.scrollWidth>innerWidth+1),false,'Mobile horizontal overflow');
  for(const img of await page.locator('.kid-finish img').all())assert(await img.evaluate(i=>i.complete&&i.naturalWidth>0),'Reward image loads');
  console.log('PASS Grade '+grade+' student Play → questions → trophy, mobile layout and read-aloud');await page.close();
 }
 const paper=await browser.newPage();
 for(const grade of [1,2]){
  await paper.goto(base+'worksheet-generator/printables.html#course=grade'+grade);
  await paper.waitForFunction(()=>window.MK_COURSE_BANKS_READY&&window.MKMENU?.printables?.youngPages);await paper.evaluate(()=>MK_COURSE_BANKS_READY);
  const reports=await paper.evaluate(async grade=>{
   const P=MKMENU.printables,id='grade'+grade+'-add-subtract-'+(grade===1?'10':'20'),reports=[];
   for(const kind of ['maze','color','roll-cover','cut-paste','number-bonds','spin-solve'])for(const key of [false,true]){
    const cfg=P.defaultConfig(id,kind);cfg.seed=11215;const built=P.build(cfg,0);if(built.error)throw Error(built.error);
    const pages=P.pageEls(cfg,built,0,1,key);for(const page of pages){document.body.appendChild(page);await Promise.all([...page.querySelectorAll('img')].map(i=>i.decode()));const body=page.querySelector('.mm-body');if(body&&body.scrollHeight>body.clientHeight+2)throw Error('Clipped '+id+' '+kind+' key='+key);page.remove()}
    reports.push(kind+':'+key);
   }return reports;
  },grade);assert.equal(reports.length,12);console.log('PASS Grade '+grade+' six activity layouts and teacher keys');
 }
 await paper.close();
}finally{await browser.close();server.close()}})().catch(e=>{console.error(e);process.exitCode=1;server.close()});
