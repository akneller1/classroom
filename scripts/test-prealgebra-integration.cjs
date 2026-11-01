const fs=require('fs'),vm=require('vm'),path=require('path');
const root=path.resolve(__dirname,'..'),context={console,URLSearchParams,setTimeout,clearTimeout};context.window=context;context.globalThis=context;
context.fetch=async url=>({ok:true,json:async()=>JSON.parse(fs.readFileSync(path.resolve(root,'worksheet-generator',url),'utf8'))});
vm.createContext(context);
const html=fs.readFileSync(path.join(root,'worksheet-generator/worksheet.html'),'utf8');
for(const m of html.matchAll(/<script[^>]*src="([^"?]+)[^"]*"[^>]*><\/script>/g)){
 const src=m[1];if(/vendor|math-display|menu\/app|approved-resource-preview/.test(src))continue;
 try{vm.runInContext(fs.readFileSync(path.resolve(root,'worksheet-generator',src),'utf8'),context,{filename:src})}catch(e){console.error(src,e.message);throw e;}
}
context.MK_COURSE_BANKS_READY.then(()=>{const N=context.MKMENU,c=context.LIBRARY.courses.find(c=>c.id==='prealgebra');let n=0;for(const u of c.units){const id='prealgebra-'+u.id,set=N.skillSets[id];if(!set.authoredBank)throw Error(id+' not authored');for(const s of set.skills)for(const level of ['cp2','cp1','honors']){const p=N.generateProblem(id,s.id,4,{level,adjacentLevels:false},n++,{keys:new Set(),sigs:new Set()});if(p.failed||!p.sourceId.startsWith('pa8-'))throw Error(id+'/'+s.id+'/'+level+' failed');}}

for(const name of ['printables','printables-scenes','printables-cases','printables-match'])vm.runInContext(fs.readFileSync(path.join(root,'worksheet-generator/menu/'+name+'.js'),'utf8'),context);
let decks=0,printables=0;
for(const u of c.units){
 const id='prealgebra-'+u.id,set=N.skillSets[id];
 for(const level of ['cp2','cp1','honors']){
  context.document={body:{getAttribute:()=> 'connect-four'}};
  const slots=Array.from({length:20},(_,i)=>({skill:set.skills[i%set.skills.length].id,c:4,level}));
  context.MKGAMES.buildDeck(id,slots,{seed:'grade8-'+level},items=>{if(items.length!==20||new Set(items.map(x=>x.id)).size!==20)throw Error('Incomplete/duplicate '+id+' '+level+' deck');for(const item of items)if(!item.id.startsWith('pa8-')||item.options.filter(o=>o.ok).length!==1)throw Error('Invalid game choice');});decks++;
  for(const kind of ['color','partner','who','stations','error','tarsia','maze']){
   const cfg={unitId:id,level,answers:'auto',kind,seed:'grade8-'+level,skills:Object.fromEntries(set.skills.map(s=>[s.id,true])),stations:2,perStation:4,count:8};
   const built=N.printables.build(cfg,0);if(built.error)throw Error(id+'/'+level+'/'+kind+': '+built.error);if(kind==='error' && built.cases.some(cs=>!cs.authored || !cs.item.p.authoredErrorAnalysis))throw Error('Un-authored error case');
   if(kind==='tarsia' && (new Set(built.items.map(it=>it.key)).size!==built.items.length || built.items.some(it=>!it.p.sourceId.startsWith('pa8-'))))throw Error('Invalid Tarsia sources/keys');
   if(kind==='maze')for(const rm of built.rooms.filter(r=>!r.finish)){const doors=built.doors.filter(d=>[d.a,d.b].some(p=>p[0]===rm.r&&p[1]===rm.c));const accepted=doors.filter(d=>context.MKGAMES.answerOk(rm.item.p,0,d.label).ok);if(accepted.length!==(rm.step===null?0:1))throw Error('Ambiguous maze room');}
   printables++;
  }
 }
}


vm.runInContext(fs.readFileSync(path.join(root,'worksheet-generator/vocabulary-data.js'),'utf8'),context);
for(const u of c.units){const terms=context.MKVOCAB_BANKS['prealgebra-'+u.id].split(';');if(terms.length<7||terms.some(t=>!t.split('|')[1]))throw Error('Missing vocabulary '+u.id);}
for(const level of ['cp2','cp1','honors'])for(const seed of [1,71,905]){const cfg=N.printables.defaultConfig('prealgebra-linear-functional-relationships','match');Object.assign(cfg,{level,seed});const B=N.printables.build(cfg,0);if(B.error||B.fns.length!==6)throw Error('Matching failed '+level);for(let i=0;i<B.fns.length;i++)for(let j=0;j<B.fns.length;j++)if(context.MKMENU.printables.MATCH.tableFits(B.fns[i],B.fns[j])!==(i===j))throw Error('Ambiguous matching table');}
console.log('PASS seven vocabulary banks and nine Pre-Algebra matching card sorts');


vm.runInContext(fs.readFileSync(path.join(root,'worksheet-generator/games/vocabulary-flashcards.js'),'utf8'),context);
for(const u of c.units){
 const nodes={},node=id=>nodes[id]||(nodes[id]={innerHTML:'',addEventListener(){}});
 context.document={body:{getAttribute:k=>({'data-unit':'prealgebra-'+u.id,'data-game':'flashcards','data-title':u.name+' Flashcards'}[k]||''),hasAttribute:()=>true},getElementById:node,querySelector:node,querySelectorAll:()=>[],addEventListener(){}};
 context.addEventListener=()=>{};context.localStorage={getItem:()=>null,setItem(){}};context.TeacherSkills={choose:(skills,start)=>start(skills.map(s=>s.id))};
 vm.runInContext(fs.readFileSync(path.join(root,'worksheet-generator/games/games.js'),'utf8'),context);
 const state=()=>context.MKGAMES._state();
 if(!state().cards.some(c=>c.vocabulary)||!state().cards.some(c=>!c.vocabulary))throw Error('Mixed flashcards missing content '+u.id);
 nodes['#fcMode'].onchange.call({value:'vocabulary'});
 if(!state().cards.length||state().cards.some(c=>!c.vocabulary))throw Error('Vocabulary mode failed '+u.id);
 nodes['#fcMode'].onchange.call({value:'skills'});
 if(!state().cards.length||state().cards.some(c=>c.vocabulary))throw Error('Skill mode failed '+u.id);
}
console.log('PASS seven flashcard players in mixed, vocabulary-only, and skill-only modes');

context.location={hash:'#course=prealgebra'};
for(const name of ['scope-algebra2','course','planner'])vm.runInContext(fs.readFileSync(path.join(root,'worksheet-generator/planner/'+name+'.js'),'utf8'),context);
let plans=0;
for(const day of context.MKPLAN_SCOPE.days.filter(d=>d.day_type==='Lesson'))for(const level of ['cp2','cp1','honors']){
 const plan=context.MKPLAN.buildDay(day.day,{level,practice:4,seed:'integration'});
 const problems=plan.sections.flatMap(s=>s.groups.flatMap(g=>g.items||[]));
 if(!problems.length||problems.some(p=>p.failed||!p.sourceId.startsWith('pa8-')))throw Error('Grade 8 planner failed on '+day.title+' '+level);
 plans++;
}
console.log('PASS '+plans+' Grade 8 lesson plans');
console.log('PASS '+n+' Grade 8 skill/level selections, '+decks+' unique-choice game decks, '+printables+' printable builds');
}).catch(e=>{console.error(e);process.exitCode=1});
