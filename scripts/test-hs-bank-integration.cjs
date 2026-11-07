const COURSE=process.env.MG_COURSE||'precalculus',PREFIX=process.env.MG_PREFIX||'pc-';
const fs=require('fs'),vm=require('vm'),path=require('path');
const root=path.resolve(__dirname,'..'),context={console,URLSearchParams,setTimeout,clearTimeout};context.window=context;context.globalThis=context;
context.fetch=async url=>({ok:true,json:async()=>JSON.parse(fs.readFileSync(path.resolve(root,'worksheet-generator',url),'utf8'))});
vm.createContext(context);
const html=fs.readFileSync(path.join(root,'worksheet-generator/worksheet.html'),'utf8');
for(const m of html.matchAll(/<script[^>]*src="([^"?]+)[^"]*"[^>]*><\/script>/g)){
 const src=m[1];if(/vendor|math-display|menu\/app|approved-resource-preview/.test(src))continue;
 try{vm.runInContext(fs.readFileSync(path.resolve(root,'worksheet-generator',src),'utf8'),context,{filename:src})}catch(e){console.error(src,e.message);throw e;}
}
context.MK_COURSE_BANKS_READY.then(()=>{const N=context.MKMENU,c=context.LIBRARY.courses.find(c=>c.id===COURSE);let n=0;for(const u of c.units){const id=COURSE+'-'+u.id,set=N.skillSets[id];if(!set.authoredBank)throw Error(id+' not authored');for(const s of set.skills)for(const level of ['cp2','cp1','honors']){const p=N.generateProblem(id,s.id,4,{level,adjacentLevels:false},n++,{keys:new Set(),sigs:new Set()});if(p.failed||!p.sourceId.startsWith(PREFIX))throw Error(id+'/'+s.id+'/'+level+' failed');}}

if(COURSE==='statistics'){
 let failures=[];
 for(const u of c.units)for(const level of ['cp2','cp1','honors'])for(const mode of ['worksheet','test','menu']){
  const cfg=N.defaultConfig(COURSE+'-'+u.id,mode);cfg.level=level;cfg.versions=1;cfg.seed='statistics-default';
  const state=N.newAssessment(cfg);const items=state.versions.flatMap(v=>v.sections.flatMap(s=>s.items));
  const failed=items.filter(p=>p.failed);if(failed.length)failures.push(u.id+'/'+level+'/'+mode+': '+failed.length+' placeholders');
 }
 if(failures.length)throw Error(failures.join('\n'));
 console.log('PASS 36 Statistics default worksheets, tests and menu assessments');
}

for(const name of ['printables','printables-scenes','printables-cases','printables-match'])vm.runInContext(fs.readFileSync(path.join(root,'worksheet-generator/menu/'+name+'.js'),'utf8'),context);
let decks=0,printables=0;
for(const u of c.units){
 const id=COURSE+'-'+u.id,set=N.skillSets[id];
 for(const level of ['cp2','cp1','honors']){
  context.document={body:{getAttribute:()=> 'connect-four'}};
  const slots=Array.from({length:20},(_,i)=>({skill:set.skills[i%set.skills.length].id,c:4,level}));
  context.MKGAMES.buildDeck(id,slots,{seed:'mg-'+level},items=>{if(items.length!==20||new Set(items.map(x=>x.id)).size!==20)throw Error('Incomplete/duplicate '+id+' '+level+' deck');for(const item of items)if(!item.id.startsWith(PREFIX)||item.options.filter(o=>o.ok).length!==1)throw Error('Invalid game choice');});decks++;
  for(const kind of ['color','partner','who','stations','error','tarsia','maze']){
   const cfg={unitId:id,level,answers:'auto',kind,seed:'mg-'+level,skills:Object.fromEntries(set.skills.map(s=>[s.id,true])),stations:2,perStation:4,count:8};
   const built=N.printables.build(cfg,0);if(built.error){(globalThis.FAILS=globalThis.FAILS||[]).push(id+'/'+level+'/'+kind+': '+built.error.slice(0,90));continue;}if(kind==='error' && built.cases.some(cs=>!cs.authored || !cs.item.p.authoredErrorAnalysis))throw Error('Un-authored error case');
   if(kind==='partner' && COURSE==='statistics' && (built.rows.length<8 || built.rows.some(r=>!r.pairId || r.A.key!==r.B.key || r.A.p.prompt===r.B.p.prompt || r.A.skill!==r.B.skill)))throw Error('Invalid authored partner pairing '+id+'/'+level);
   if(kind==='tarsia' && (new Set(built.items.map(it=>it.key)).size!==built.items.length || built.items.some(it=>!it.p.sourceId.startsWith(PREFIX))))throw Error('Invalid Tarsia sources/keys');
   if(kind==='maze')for(const rm of built.rooms.filter(r=>!r.finish)){const doors=built.doors.filter(d=>[d.a,d.b].some(p=>p[0]===rm.r&&p[1]===rm.c));const accepted=doors.filter(d=>context.MKGAMES.answerOk(rm.item.p,0,d.label).ok);if(accepted.length!==(rm.step===null?0:1))throw Error('Ambiguous maze room');}
   printables++;
  }
 }
}

if(COURSE==='statistics'){
 let checked=0;
 for(const u of c.units){const id=COURSE+'-'+u.id,set=N.skillSets[id];
  for(const skill of set.skills)for(const level of ['cp2','cp1','honors']){
   const cfg={unitId:id,level,answers:'auto',seed:'single-skill',skills:{[skill.id]:true}};
   const partner=N.printables.build({...cfg,kind:'partner'},0);
   if(partner.error||partner.rows.length!==1||partner.rows.some(r=>!r.pairId||r.A.skill!==skill.id||r.B.skill!==skill.id||r.A.key!==r.B.key))throw Error('Single-skill partner '+id+'/'+skill.id+'/'+level);
   const error=N.printables.build({...cfg,kind:'error'},0);
   if(error.error||!error.cases.length||error.cases.some(cs=>!cs.authored||cs.item.skill!==skill.id))throw Error('Single-skill error '+id+'/'+skill.id+'/'+level);
   checked++;
  }
 }
 console.log('PASS '+checked+' individual skill/level partner and error-analysis selections');
}

vm.runInContext(fs.readFileSync(path.join(root,'worksheet-generator/vocabulary-data.js'),'utf8'),context);
vm.runInContext(fs.readFileSync(path.join(root,'worksheet-generator/vocabulary-data-middle-grades.js'),'utf8'),context);
for(const u of c.units){const terms=context.MKVOCAB_BANKS[COURSE+'-'+u.id].split(';');if(terms.length<8||terms.some(t=>!t.split('|')[1]))throw Error('Missing vocabulary '+u.id);}


vm.runInContext(fs.readFileSync(path.join(root,'worksheet-generator/games/vocabulary-flashcards.js'),'utf8'),context);
for(const u of c.units){
 const nodes={},node=id=>nodes[id]||(nodes[id]={innerHTML:'',addEventListener(){}});
 context.document={body:{getAttribute:k=>({'data-unit':COURSE+'-'+u.id,'data-game':'flashcards','data-title':u.name+' Flashcards'}[k]||''),hasAttribute:()=>true},getElementById:node,querySelector:node,querySelectorAll:()=>[],addEventListener(){}};
 context.addEventListener=()=>{};context.localStorage={getItem:()=>null,setItem(){}};context.TeacherSkills={choose:(skills,start)=>start(skills.map(s=>s.id))};
 vm.runInContext(fs.readFileSync(path.join(root,'worksheet-generator/games/games.js'),'utf8'),context);
 const state=()=>context.MKGAMES._state();
 if(!state().cards.some(c=>c.vocabulary)||!state().cards.some(c=>!c.vocabulary))throw Error('Mixed flashcards missing content '+u.id);
 nodes['#fcMode'].onchange.call({value:'vocabulary'});
 if(!state().cards.length||state().cards.some(c=>!c.vocabulary))throw Error('Vocabulary mode failed '+u.id);
 nodes['#fcMode'].onchange.call({value:'skills'});
 if(!state().cards.length||state().cards.some(c=>c.vocabulary))throw Error('Skill mode failed '+u.id);
}
console.log('PASS '+c.units.length+' flashcard players in mixed, vocabulary-only, and skill-only modes');


console.log('PASS '+c.units.length+' vocabulary banks with 8+ terms');

if((globalThis.FAILS||[]).length)throw Error(globalThis.FAILS.join('\n'));
console.log('PRINTABLE FAILURES '+(globalThis.FAILS||[]).length+'\n'+(globalThis.FAILS||[]).join('\n'));
context.location={hash:'#course='+COURSE+''};
for(const name of ['scope-algebra2','course','planner'])vm.runInContext(fs.readFileSync(path.join(root,'worksheet-generator/planner/'+name+'.js'),'utf8'),context);
let plans=0;
for(const day of context.MKPLAN_SCOPE.days.filter(d=>d.day_type==='Lesson'))for(const level of ['cp2','cp1','honors']){
 const plan=context.MKPLAN.buildDay(day.day,{level,practice:4,seed:'integration'});
 const problems=plan.sections.flatMap(s=>s.groups.flatMap(g=>g.items||[]));
 if(!problems.length||problems.some(p=>p.failed||!p.sourceId.startsWith(PREFIX)))throw Error(''+COURSE+' planner failed on '+day.title+' '+level);
 plans++;
}
console.log('PASS '+plans+' '+COURSE+' lesson plans');
console.log('PASS '+n+' '+COURSE+' skill/level selections, '+decks+' unique-choice game decks, '+printables+' printable builds');
}).catch(e=>{console.error(e);process.exitCode=1});

