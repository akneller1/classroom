'use strict';
const fs=require('node:fs'),vm=require('node:vm'),assert=require('node:assert/strict'),path=require('node:path');
const site={};site.window=site;site.globalThis=site;site.setTimeout=setTimeout;site.Promise=Promise;
site.fetch=p=>Promise.resolve({ok:true,json:()=>Promise.resolve(JSON.parse(fs.readFileSync(path.resolve(__dirname,'..',String(p).replace(/^\.\.\//,'')),'utf8')))});
const ctx=vm.createContext(site);
for(const file of ['data.js','course-catalog.js','question-bank-adapter.js','question-bank-loader.js','worksheet-generator/core/rng.js','worksheet-generator/menu/mathcheck.js','worksheet-generator/menu/verify.js','worksheet-generator/menu/engine.js','worksheet-generator/games/bank.js','worksheet-generator/menu/printables.js','worksheet-generator/menu/printables-scenes.js','worksheet-generator/menu/printables-cases.js','worksheet-generator/algebra2-bank-native.js'])vm.runInContext(fs.readFileSync(path.resolve(__dirname,'..',file),'utf8'),ctx,{filename:file});
(async()=>{
 await site.MK_ALGEBRA2_NATIVE_READY;let checks=0;const report=[];
 for(const unit of site.LIBRARY.courses.find(c=>c.id==='algebra2').units){
  const id='algebra2-'+unit.id,set=site.MKMENU.skillSets[id];assert.ok(set);
  const unitBank=JSON.parse(fs.readFileSync(path.resolve(__dirname,'../question-banks/algebra2/'+unit.id+'.json')));
  for(const skill of set.skills)for(const [level,c] of [['cp2',1],['cp1',4],['honors',6]]){
   const items=site.MKGAMES.makeItems(id,skill.id,c,{level},'integration-test',{keys:new Set()});const expected=unitBank.questions.filter(q=>q.skillId===skill.id&&q.level===level&&q.format==='multiple-choice');if(!expected.length){assert.equal(items.length,0);continue}assert.ok(items.length);
   const q=unitBank.questions.find(q=>q.id===items[0].id);assert.ok(q);assert.equal(q.level,level);assert.equal(items[0].q.prompt,q.prompt);assert.equal(items[0].answer,String(q.answer));assert.deepEqual(JSON.parse(JSON.stringify(items[0].options)),q.options.map(o=>({a:o.text,ok:o.correct===true})));checks++;
  }
  const kinds=site.MKMENU.printables.KINDS.filter(k=>set.skills.some(s=>site.MKMENU.printables.capable(id,s.id,k.id))).map(k=>k.id);
  const builds={};for(const kind of kinds){const cfg=site.MKMENU.printables.defaultConfig(id,kind);cfg.seed='integration';const b=site.MKMENU.printables.build(cfg,0);builds[kind]=b.error||'PASS';assert.equal(builds[kind],'PASS',unit.id+'/'+kind+': '+b.error);}report.push({unitId:unit.id,skills:set.skills.length,kinds,builds});
 }
 site.document={body:{getAttribute:name=>name==='data-game'?'showdown':null}};
 let showdownCount=0;
 for(const unit of site.LIBRARY.courses.find(c=>c.id==='algebra2').units){
  const id='algebra2-'+unit.id,bank=JSON.parse(fs.readFileSync(path.resolve(__dirname,'../question-banks/algebra2/'+unit.id+'.json')));
  for(const skill of site.MKMENU.skillSets[id].skills){
   const slots=[2,3,3,4,5].map((c,row)=>({skill:skill.id,c,level:'cp1',row}));
   site.MKGAMES.buildDeck(id,slots,{wholeProblem:true,seed:'board-regression'},items=>{
    assert.equal(items.length,5,unit.id+'/'+skill.id+' Standard board must have all point values');assert.equal(new Set(items.map(i=>i.id)).size,5);
    for(const item of items){const q=bank.questions.find(q=>q.id===item.id);assert.equal(q.level,'cp1','100-point row must remain at selected Standard level');for(const p of q.parts||[])assert.ok(item.q.ask.includes(p.prompt),'Show every source part');showdownCount++;}
   });
  }
 }
 console.log('PASS '+showdownCount+' complete Standard Showdown cells; source levels, distinct questions and full parts retained');
 fs.mkdirSync('test-results',{recursive:true});fs.writeFileSync('test-results/algebra2-native-coverage.json',JSON.stringify(report,null,2));
 assert.deepEqual(Array.from(site.MKGAMES.LEVELS.cp1.tiers),[3,4,5],'Original game tiers preserved');
 console.log('PASS '+checks+' unit/skill/level native game selections, original prompts/choices/keys preserved');console.log(JSON.stringify(report));
})().catch(e=>{console.error(e);process.exitCode=1});
