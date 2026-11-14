// Verify the assembled release, including the same eligibility checks used by the game.
const fs=require('node:fs'),path=require('node:path'),vm=require('node:vm'),assert=require('node:assert/strict');
(async()=>{
 const root=path.resolve(process.argv[2]||'_site');
 const {loadSiteCatalog}=await import('./load-site-catalog.mjs');
 const {library}=loadSiteCatalog(root);
 const {asteroidUnits}=await import('./asteroid-resources.mjs');
 const expected={...asteroidUnits,grade5:['place-value-number-sense','multi-digit-multiplication-division','decimal-operations']};
 const html=fs.readFileSync(path.join(root,'worksheet-generator/asteroid-blaster.html'),'utf8');
 const helpers=html.slice(html.indexOf('function shuffle(a)'),html.indexOf('const esc='));
 const eligibility=html.slice(html.indexOf('function quickAnswer(q)'),html.indexOf('function selectedSkills()'));
 const manifest=JSON.parse(fs.readFileSync(path.join(root,'question-banks/manifest.json')));
 let checks=0;
 for(const [courseId,units] of Object.entries(expected)){
  const course=library.courses.find(c=>c.id===courseId);assert(course,courseId+' released catalog missing');
  const actual=course.units.filter(u=>u.artifacts.some(a=>a.bankFormat==='asteroid-blaster'));
  assert.deepEqual(Array.from(actual,u=>u.id).sort(),units.slice().sort(),courseId+' curated placement');
  assert(actual.length<=3);
  for(const unit of actual){
   const cards=unit.artifacts.filter(a=>a.bankFormat==='asteroid-blaster');assert.equal(cards.length,1);
   const url=new URL(cards[0].path,'https://mrksclassroom.com/');assert.equal(url.searchParams.get('course'),courseId);assert.equal(url.searchParams.get('unit'),unit.id);
   assert(fs.existsSync(path.join(root,url.pathname)));
   const entry=manifest.banks.find(b=>b.courseId===courseId&&b.unitId===unit.id);assert(entry?.approved);
   const bank=JSON.parse(fs.readFileSync(path.join(root,entry.path)));
   const G={};G.window=G;
   vm.createContext(G);vm.runInContext(helpers+eligibility+';this.usable=usable;this.norm=norm;',G);
   if(courseId==='grade5')vm.runInContext(fs.readFileSync(path.join(root,'worksheet-generator/games/asteroid-grade5-bank.js'),'utf8'),G);
   for(const level of ['cp2','cp1','honors']){
    const items=courseId==='grade5'?G.MK_ASTEROID_GRADE5.select(unit.id,level,G.MK_ASTEROID_GRADE5.records(unit.id).map(s=>s.id),10000):bank.questions.filter(q=>q.level===level);
    const valid=items.filter(q=>G.usable(q));
    const distinct=new Set(valid.map(q=>G.norm(q.prompt)+'|'+G.norm(q.options.find(o=>o.correct).text)));
    assert(distinct.size>=8,`${courseId}/${unit.id}/${level}: only ${distinct.size} playable questions`);
    for(const q of valid)assert.equal(G.norm(q.answer),G.norm(q.options.find(o=>o.correct).text),'answer key mismatch '+q.id);
    console.log(`${courseId}/${unit.id}/${level}: ${distinct.size} distinct quick-answer MC questions`);checks++;
   }
  }
 }
 assert(!library.courses.find(c=>c.id==='grade1')?.units.some(u=>u.artifacts.some(a=>a.bankFormat==='asteroid-blaster')));
 console.log(`Elementary Asteroid release audit passed (${checks} unit/level checks).`);
})().catch(e=>{console.error(e);process.exit(1)});
