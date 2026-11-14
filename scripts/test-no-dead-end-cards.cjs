#!/usr/bin/env node
/* Blocking Chromium audit of rendered resource cards and static unit directories.
   Usage: node scripts/test-no-dead-end-cards.cjs _site */
'use strict';
const fs=require('node:fs'),path=require('node:path'),http=require('node:http');
const {chromium}=require('playwright');
const root=path.resolve(process.argv[2]||'_site');
const mime={'.html':'text/html','.js':'text/javascript','.mjs':'text/javascript','.json':'application/json','.css':'text/css','.svg':'image/svg+xml','.pdf':'application/pdf','.png':'image/png','.jpg':'image/jpeg','.woff2':'font/woff2'};
const server=http.createServer((req,res)=>{
 let pathname;try{pathname=decodeURIComponent(new URL(req.url,'http://localhost').pathname)}catch{res.writeHead(400).end();return;}
 let file=path.resolve(root,'.'+pathname);if(file!==root&&!file.startsWith(root+path.sep)){res.writeHead(403).end();return;}
 if(fs.existsSync(file)&&fs.statSync(file).isDirectory())file=path.join(file,'index.html');
 if(!fs.existsSync(file)){res.writeHead(404).end('Not found');return;}
 res.writeHead(200,{'content-type':mime[path.extname(file)]||'application/octet-stream'});fs.createReadStream(file).pipe(res);
});
function walk(dir){return fs.readdirSync(dir,{withFileTypes:true}).flatMap(e=>e.isDirectory()?walk(path.join(dir,e.name)):[path.join(dir,e.name)]);}
(async()=>{
 await new Promise(resolve=>server.listen(0,'127.0.0.1',resolve));
 const base='http://127.0.0.1:'+server.address().port+'/';
 let browser;const errors=[],links=new Set();let courses=0,units=0,checked=0;
 try{
  browser=await chromium.launch({headless:true});
  const page=await browser.newPage();
  page.on('pageerror',e=>errors.push('catalog: '+e.message));
  await page.goto(base,{waitUntil:'load'});
  await page.waitForFunction(()=>window.LIBRARY&&document.querySelector('#main h1'));
  const routes=await page.evaluate(()=>window.LIBRARY.courses.map(c=>({id:c.id,units:c.units.map(u=>u.id)})));
  courses=routes.length;
  for(const c of routes){
   for(const route of [c.id,...c.units.map(u=>c.id+'.'+u)]){
    await page.goto(base+'#'+route,{waitUntil:'load'});
    await page.waitForFunction(()=>!!document.querySelector('#main h1'));
    for(const href of await page.locator('.card a[href]').evaluateAll(as=>as.map(a=>a.href))){if(href.startsWith(base)&&!href.includes('mailto:'))links.add(href);}
    units+=route.includes('.')?1:0;
   }
  }
  // SEO unit pages also have resource links; collect them independently.
  for(const file of walk(path.join(root,'u')).filter(f=>f.endsWith('.html'))){
   const html=fs.readFileSync(file,'utf8'),url=new URL(path.relative(root,file).split(path.sep).join('/'),base);
   for(const list of html.matchAll(/<ul class="mk-items">([\s\S]*?)<\/ul>/g))for(const match of list[1].matchAll(/href="([^"<>]+)"/g)){
    const href=new URL(match[1].replace(/&amp;/g,'&'),url).href;if(href.startsWith(base))links.add(href);
   }
  }
  await page.close();
  const queue=[...links];
  const workers=Array.from({length:Number(process.env.CARD_AUDIT_WORKERS||6)},async()=>{
   const p=await browser.newPage();let current='';let failures=[];
   p.on('pageerror',e=>failures.push('page error: '+e.message));
   p.on('response',res=>{if(res.status()===404&&res.url().startsWith(base))failures.push('404: '+res.url().slice(base.length));});
   while(queue.length){
    current=queue.shift();failures=[];
    try{
     const pathname=new URL(current).pathname;
     if(/\.(?:pdf|png|jpe?g|svg|zip|docx?|pptx?|xlsx?|txt)$/i.test(pathname)){
      const response=await p.request.get(current);if(!response.ok())throw Error('HTTP '+response.status());
     }else{
      const response=await p.goto(current,{waitUntil:'load',timeout:30000});if(response&&response.status()>=400)throw Error('HTTP '+response.status());
      await p.waitForTimeout(150);
      const loading=/\bLoading[^\n]{0,80}(?:…|\.\.\.)/i;
      const deadline=Date.now()+10000;
      let text=await p.locator('body').innerText();
      while(loading.test(text)&&Date.now()<deadline){await p.waitForTimeout(200);text=await p.locator('body').innerText();}
      if(loading.test(text))failures.push('loading for more than 10 seconds');
      if(/\bnot available\b|unable to load|course outline unavailable|select a valid course and unit/i.test(text))failures.push('unavailable resource');
     }
    }catch(e){failures.push(e.message);}
    if(failures.length)errors.push(current.slice(base.length)+': '+[...new Set(failures)].join('; '));
    checked++;if(checked%100===0)console.log('Card audit: '+checked+'/'+links.size+' links; '+errors.length+' failures');
   }
   await p.close();
  });
  await Promise.all(workers);
  if(errors.length)throw Error(errors.length+' dead-end card failures:\n'+errors.join('\n'));
  console.log('PASS no dead-end cards: '+courses+' courses, '+units+' units, '+checked+' unique links');
 }finally{if(browser)await browser.close();server.close();}
})().catch(error=>{console.error(error.stack);process.exitCode=1;server.close();});
