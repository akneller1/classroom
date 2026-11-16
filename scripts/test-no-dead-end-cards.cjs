#!/usr/bin/env node
'use strict';
const fs=require('node:fs'),path=require('node:path'),http=require('node:http'),{chromium}=require('playwright');
const {localTarget,browserSample}=require('./resource-card-checks.cjs');
const full=process.argv.includes('--full');
const root=path.resolve(process.argv[2]||'_site');
const mime={'.html':'text/html','.js':'text/javascript','.mjs':'text/javascript','.json':'application/json','.css':'text/css','.svg':'image/svg+xml','.pdf':'application/pdf'};
const server=http.createServer((req,res)=>{const url=new URL(req.url,'http://localhost');let p;try{p=path.resolve(root,'.'+decodeURIComponent(url.pathname));}catch{res.writeHead(400).end();return;}if(p!==root&&!p.startsWith(root+path.sep)){res.writeHead(403).end();return;}if(fs.existsSync(p)&&fs.statSync(p).isDirectory())p=path.join(p,'index.html');if(!fs.existsSync(p)){res.writeHead(404).end('Not found');return;}res.setHeader('Content-Type',mime[path.extname(p)]||'application/octet-stream');fs.createReadStream(p).pipe(res);});
(async()=>{await new Promise(r=>server.listen(0,'127.0.0.1',r));const base='http://127.0.0.1:'+server.address().port+'/';const browser=await chromium.launch({headless:true});const errors=[];let count=0;const loading=/loading[^\n]{0,80}(?:…|\.\.\.)/i;
async function teacherSetupReady(p){const d=p.locator('dialog.teacher-skills[open]');return await d.isVisible()&&await d.locator('input[type="checkbox"]').count()>0&&await d.getByRole('button',{name:'Continue',exact:true}).isEnabled();}
try{
 const page=await browser.newPage();await page.goto(base);await page.waitForFunction(()=>window.LIBRARY?.courses?.length);
 const routes=await page.evaluate(()=>LIBRARY.courses.filter(c=>!c.comingSoon).flatMap(c=>[c.id,...c.units.map(u=>c.id+'.'+u.id)]));const links=new Set(),courseByHref=new Map();
 for(const route of routes){await page.goto(base+'#'+route);await page.waitForTimeout(30);for(const href of await page.locator('.card a[href]').evaluateAll(as=>as.map(a=>a.href)))if(href.startsWith(base)){links.add(href);courseByHref.set(href,route.split('.')[0]);}}
 await page.close();
 for(const href of links)localTarget(root,href,base);
 console.log('PASS file targets: '+links.size+' links across '+routes.length+' course/unit views.');
 const queue=full?[...links]:browserSample([...links],base,96,courseByHref),total=queue.length;
 console.log((full?'Full audit':'Release smoke check')+': browser-checking '+total+' representative links.');
 await Promise.all(Array.from({length:8},async()=>{const p=await browser.newPage();while(queue.length){const href=queue.shift();const faults=[];const onError=e=>faults.push(e.message);p.on('pageerror',onError);try{
 if(/\.(pdf|docx|pptx|zip)(?:[?#]|$)/i.test(href)){const r=await p.request.get(href);if(!r.ok())throw Error('HTTP '+r.status());}
 else{const response=await p.goto(href,{waitUntil:'load',timeout:30000});if(response&&response.status()>=400)throw Error('HTTP '+response.status());await p.waitForTimeout(150);let text=await p.locator('body').innerText();if(loading.test(text)&&!await teacherSetupReady(p)){await p.waitForFunction(()=>! /loading[^\n]{0,80}(?:…|\.\.\.)/i.test(document.body.innerText)||(()=>{const d=document.querySelector('dialog.teacher-skills[open]');return d&&d.querySelector('input[type="checkbox"]')&&[...d.querySelectorAll('button')].some(b=>b.textContent==='Continue'&&!b.disabled);})(),{},{timeout:10000});text=await p.locator('body').innerText();}if(/(?:this (?:game|activity|resource|course) is not available|activity (?:could )?not (?:be )?found|404 not found)/i.test(text))throw Error(text.slice(0,400));if(faults.length)throw Error(faults.join('; '));}
 count++;if(count%250===0)console.log('Checked '+count+' links');
 }catch(e){const failure={href:href.replace(base,'/'),error:e.message};errors.push(failure);console.error('FAIL '+JSON.stringify(failure));if(errors.length>=20)queue.length=0;}finally{p.off('pageerror',onError);}}await p.close();}));
 if(errors.length)throw Error(JSON.stringify(errors,null,2));console.log('PASS '+(full?'full resource audit':'release resource smoke check')+': '+count+' browser links; '+links.size+' file targets.');
}finally{await browser.close();server.close();}})().catch(e=>{console.error(e);process.exitCode=1;server.close();});
