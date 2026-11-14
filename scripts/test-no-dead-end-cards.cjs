#!/usr/bin/env node
'use strict';
const fs=require('node:fs'),path=require('node:path'),http=require('node:http'),{chromium}=require('playwright');
const root=path.resolve(process.argv[2]||'_site');
const mime={'.html':'text/html','.js':'text/javascript','.mjs':'text/javascript','.json':'application/json','.css':'text/css','.svg':'image/svg+xml','.pdf':'application/pdf'};
const server=http.createServer((req,res)=>{const url=new URL(req.url,'http://localhost');let p;try{p=path.resolve(root,'.'+decodeURIComponent(url.pathname));}catch{res.writeHead(400).end();return;}if(p!==root&&!p.startsWith(root+path.sep)){res.writeHead(403).end();return;}if(fs.existsSync(p)&&fs.statSync(p).isDirectory())p=path.join(p,'index.html');if(!fs.existsSync(p)){res.writeHead(404).end('Not found');return;}res.setHeader('Content-Type',mime[path.extname(p)]||'application/octet-stream');fs.createReadStream(p).pipe(res);});
(async()=>{await new Promise(r=>server.listen(0,'127.0.0.1',r));const base='http://127.0.0.1:'+server.address().port+'/';const browser=await chromium.launch({headless:true});const errors=[];let count=0;
try{
 const page=await browser.newPage();await page.goto(base);await page.waitForFunction(()=>window.LIBRARY?.courses?.length);
 const routes=await page.evaluate(()=>LIBRARY.courses.filter(c=>!c.comingSoon).flatMap(c=>[c.id,...c.units.map(u=>c.id+'.'+u.id)]));const links=new Set();
 for(const route of routes){await page.goto(base+'#'+route);await page.waitForTimeout(30);for(const href of await page.locator('.card a[href]').evaluateAll(as=>as.map(a=>a.href)))if(href.startsWith(base))links.add(href);}
 await page.close();const queue=[...links];console.log('Checking '+routes.length+' course/unit views and '+queue.length+' unique card links.');
 await Promise.all(Array.from({length:8},async()=>{const p=await browser.newPage();while(queue.length){const href=queue.shift();const faults=[];const onError=e=>faults.push(e.message);p.on('pageerror',onError);try{
 if(/\.(pdf|docx|pptx|zip)(?:[?#]|$)/i.test(href)){const r=await p.request.get(href);if(!r.ok())throw Error('HTTP '+r.status());}
 else{const response=await p.goto(href,{waitUntil:'load',timeout:30000});if(response&&response.status()>=400)throw Error('HTTP '+response.status());await p.waitForTimeout(150);let text=await p.locator('body').innerText();if(/loading\s*(?:…|\.\.\.)/i.test(text)){await p.waitForFunction(()=>! /loading\s*(?:…|\.\.\.)/i.test(document.body.innerText),{},{timeout:10000});text=await p.locator('body').innerText();}if(/(?:this (?:game|activity|resource|course) is not available|activity (?:could )?not (?:be )?found|404 not found)/i.test(text))throw Error(text.slice(0,400));if(faults.length)throw Error(faults.join('; '));}
 count++;if(count%250===0)console.log('Checked '+count+' links');
 }catch(e){errors.push({href:href.replace(base,'/'),error:e.message});}finally{p.off('pageerror',onError);}}await p.close();}));
 if(errors.length)throw Error(JSON.stringify(errors,null,2));console.log('PASS no dead-end cards: '+count+' links');
}finally{await browser.close();server.close();}})().catch(e=>{console.error(e);process.exitCode=1;server.close();});
