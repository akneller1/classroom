#!/usr/bin/env node
'use strict';
// Validate the actual script order of every shared activity page, against the
// assembled manifest. A missing elementary catalog must not break other courses.
const fs=require('node:fs'),path=require('node:path'),vm=require('node:vm'),assert=require('node:assert/strict');
const site=path.resolve(process.argv[2]||'_site'),dir=path.join(site,'worksheet-generator');
const manifest=JSON.parse(fs.readFileSync(path.join(site,'question-banks/manifest.json'),'utf8'));
const banks=manifest.banks.filter(b=>b.approved===true||(b.courseId==='algebra2'&&b.teacherUse===true)).map(b=>({entry:b,bank:JSON.parse(fs.readFileSync(path.join(site,b.path),'utf8'))}));
let pages=0,validated=0;
for(const name of fs.readdirSync(dir).filter(n=>n.endsWith('.html'))){
 const html=fs.readFileSync(path.join(dir,name),'utf8');
 if(!html.includes('../course-catalog.js')||!/(?:algebra2-bank-native|approved-flashcards|approved-resource-bank)/.test(html))continue;
 const context={console,URL,URLSearchParams,setTimeout,clearTimeout};context.window=context;context.globalThis=context;vm.createContext(context);
 const scripts=[...html.matchAll(/<script\b[^>]*\bsrc=["']([^"']+)["'][^>]*>/g)].map(m=>m[1].split('?')[0]);
 const native=scripts.findIndex(s=>s==='algebra2-bank-native.js');
 const catalogScripts=scripts.filter((src,i)=>/(?:^|\/)(?:data|course-catalog|grade[1-5]-main-catalog|elementary-preload-catalog)\.js$/.test(src)&&(native<0||i<native));
 for(const src of catalogScripts)vm.runInContext(fs.readFileSync(path.resolve(dir,src),'utf8'),context,{filename:src,timeout:10000});
 vm.runInContext(fs.readFileSync(path.join(site,'question-bank-adapter.js'),'utf8'),context);
 for(const {entry,bank} of banks){
  const result=context.MK_QUESTION_BANKS.validate(bank);
  assert.ok(result.ok,name+' cannot validate '+entry.courseId+'/'+entry.unitId+': '+result.errors.slice(0,2).join('; '));
  validated++;
 }
 pages++;
}
assert.ok(pages>=9,'Expected shared games, practice and generator pages');
console.log('PASS shared activity catalogs: '+pages+' pages, '+validated+' bank validations in published script order.');
