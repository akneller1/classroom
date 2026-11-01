/* Verify vocabulary source coverage, entry points and shared player content modes for every published course. */
'use strict';
const fs=require('fs'),vm=require('vm'),path=require('path'),assert=require('assert/strict');
const root=path.resolve(__dirname,'..'),context={console,URLSearchParams,setTimeout,clearTimeout};context.window=context;context.globalThis=context;
context.fetch=async url=>({ok:true,json:async()=>JSON.parse(fs.readFileSync(path.resolve(root,'worksheet-generator',url),'utf8'))});vm.createContext(context);
const html=fs.readFileSync(path.join(root,'worksheet-generator/worksheet.html'),'utf8');
for(const m of html.matchAll(/<script[^>]*src="([^"?]+)[^"]*"[^>]*><\/script>/g)){
 const src=m[1];if(/vendor|math-display|menu\/app|approved-resource-preview/.test(src))continue;
 vm.runInContext(fs.readFileSync(path.resolve(root,'worksheet-generator',src),'utf8'),context,{filename:src});
}
context.MK_COURSE_BANKS_READY.then(async()=>{
 for(const file of ['vocabulary-data.js','games/vocabulary-flashcards.js'])vm.runInContext(fs.readFileSync(path.join(root,'worksheet-generator',file),'utf8'),context);
 let units=0,cards=0;
 for(const course of context.LIBRARY.courses.filter(c=>['algebra','geometry','algebra2','prealgebra'].includes(c.id)))for(const unit of course.units){
  let id=(course.id==='algebra'?'algebra1':course.id)+'-'+unit.id;
  const entry=unit.artifacts.find(a=>/flashcards/.test(a.path)&&a.path.startsWith('artifacts/'));
  if(entry&&['algebra','geometry'].includes(course.id)){
   const text=fs.readFileSync(path.join(root,entry.path),'utf8');id=text.match(/data-unit="([^"]+)"/)[1];
   assert(text.indexOf('vocabulary-flashcards.js')<text.indexOf('games/games.js'),'Vocabulary must load before player: '+id);
  }
  if(entry&&course.id==='algebra2')assert(fs.readFileSync(path.join(root,entry.path),'utf8').includes('course-game.html?'),'Legacy Algebra 2 flashcards must use shared player');
  const vocab=context.MK_VOCAB_FLASHCARDS.build(id);assert(vocab.length>=4,'Missing vocabulary '+id);assert.equal(new Set(vocab.map(c=>c.id)).size,vocab.length);cards+=vocab.length;
  const nodes={},node=id=>nodes[id]||(nodes[id]={innerHTML:'',addEventListener(){}});
  context.document={body:{getAttribute:k=>({'data-unit':id,'data-game':'flashcards','data-title':unit.name+' Flashcards'}[k]||''),hasAttribute:()=>context.MKMENU.skillSets[id].authoredBank===true},getElementById:node,querySelector:node,querySelectorAll:()=>[],addEventListener(){}};
  context.addEventListener=()=>{};context.localStorage={getItem:()=>null,setItem(){}};context.TeacherSkills={choose:(skills,start)=>start(skills.map(s=>s.id))};
  vm.runInContext(fs.readFileSync(path.join(root,'worksheet-generator/games/games.js'),'utf8'),context);
  const state=()=>context.MKGAMES._state();
  for(let i=0;i<100&&!nodes.app.innerHTML.includes('fcMode');i++)await new Promise(r=>setTimeout(r,20));
  assert(state().cards.some(c=>c.vocabulary),'Mixed mode lacks vocabulary '+id);
  nodes['#fcMode'].onchange.call({value:'vocabulary'});assert.equal(state().cards.length,vocab.length);assert(state().cards.every(c=>c.vocabulary));
  for(const c of state().cards){assert(!context.MKGAMES.ui.qHtml(c,true).includes(c.answer),'Front exposes definition '+id);assert(context.MKGAMES.ui.solHtml(c).includes('Answer'),'No answer side '+id);}
  nodes['#fcMode'].onchange.call({value:'skills'});for(let i=0;i<100&&!nodes.app.innerHTML.includes('fcMode');i++)await new Promise(r=>setTimeout(r,20));assert(state().cards.every(c=>!c.vocabulary),'Skill mode contains vocabulary '+id);units++;
 }
 console.log('PASS '+units+' units across four courses; '+cards+' vocabulary cards; mixed, vocabulary-only and skill-only modes');
}).catch(e=>{console.error(e);process.exitCode=1;});
