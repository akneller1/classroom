#!/usr/bin/env node
/* Run against the assembled release, not an isolated source catalog. */
'use strict';
const fs=require('node:fs'),path=require('node:path'),vm=require('node:vm'),assert=require('node:assert/strict');
const root=path.resolve(__dirname,'..'),site=path.resolve(process.argv[2]||'_site');
const G=require('../worksheet-generator/menu/tests/load.cjs')(['games/bank.js','menu/render.js']);
G.location={hash:'#course=grade5'};
G.fetch=async url=>({ok:true,json:async()=>JSON.parse(fs.readFileSync(path.resolve(site,'worksheet-generator',url),'utf8'))});
const run=f=>vm.runInContext(fs.readFileSync(path.join(site,f),'utf8'),G,{filename:f});
for(const f of ['data.js','course-integrations.js','course-catalog.js','grade5/grade5-main-catalog.js','grade4-main-catalog.js','grade3-main-catalog.js','grade2-main-catalog.js','question-bank-adapter.js','question-bank-loader.js','worksheet-generator/algebra2-bank-native.js'])run(f);
(async()=>{
 await G.MK_COURSE_BANKS_READY;
 const grade4=G.MKMENU.CATALOG.find(c=>c.course==='4th Grade Math');
 assert.ok(grade4,'Grade 4 missing from generator course selector');
 assert.equal(grade4.units.length,10,'Grade 4 generator units missing');
 for(const [id] of grade4.units){
  assert.ok(G.MKMENU.skillSets[id],id+' missing skill set');
  const c=G.MKMENU.defaultConfig(id,'worksheet');
  assert.equal(c.unitId,id,'Grade 4 generator reverted to another course');
  assert.ok(G.MK_QUESTION_BANKS.select({courseId:'grade4',unitId:id.slice(7)}).length>0,id+' bank unavailable');
 }
 const M=G.MKMENU,ids=Object.keys(M.skillSets).filter(id=>id.startsWith('grade5-'));
 assert.equal(ids.length,11);let papers=0,activities=0,lessons=0;
 for(const id of ids)for(const level of ['cp2','cp1','honors'])for(const mode of ['worksheet','test']){
  const c=M.defaultConfig(id,mode);c.level=level;c.versions=3;
  c.sections=[['mcas',2],['mc',5],['diagram',3]].map(([qformat,n],i)=>({...c.sections[0],id:'part'+i,name:'Part '+(i+1),qformat,offered:n,required:n,points:2}));
  const st=M.newAssessment(c);
  for(const v of st.versions){
   assert.deepEqual(Array.from(v.sections,s=>s.items.length),[2,5,3]);
   const items=v.sections.flatMap(s=>s.items);
   assert.ok(items.every(p=>!p.failed),id+' '+level+' '+mode+': missing question');
   assert.equal(new Set(items.map(p=>p.sourceId)).size,10,id+': repeat inside a version');
   assert.ok(v.sections[0].items.every(p=>p.authoredFormat==='open-response'));
   assert.ok(v.sections[1].items.every(p=>p.mc&&M.checkChoices(p)));
   assert.ok(v.sections[2].items.every(p=>p.fig?.kind==='authored-image'));
   for(const p of items){const q=G.MK_QUESTION_BANKS.select({courseId:'grade5',unitId:id.slice(7),level}).find(q=>q.id===p.sourceId);assert.ok(q,'wrong level or missing source');if(p.fig)assert.ok(fs.existsSync(path.join(site,p.fig.src)));}
   papers++;
  }
  const restored=M.deserialize(JSON.parse(M.serialize(st)));
  assert.equal(restored.versions.length,3);assert.equal(restored.versions[0].sections[2].items.length,3);
 }
 for(const f of ['menu/printables.js','menu/printables-scenes.js','menu/printables-cases.js','menu/printables-match.js'])run('worksheet-generator/'+f);
 run('worksheet-generator/menu/printables-projects.js');run('grade5/grade5-native-resources.js');
 for(const id of ids){assert.ok(G.MKVOCAB_BANKS[id].split(';').length>=6,id+' vocabulary missing');for(const p of M.printables.PROJECTS[id]){const f=M.printables.projectFiles(p);for(const lv of ['cp2','cp1','honors','teacher'])for(const url of Object.values(f[lv]))assert.ok(fs.existsSync(path.resolve(site,'worksheet-generator',url)),'missing project '+url);}}
 for(const id of ids)for(const level of ['cp2','cp1','honors'])for(const kind of ['maze','color','partner','error','stations','tarsia','who']){
  const c=M.printables.defaultConfig(id,kind);c.level=level;c.seed=42;
  const p=M.printables.build(c,0);assert.ok(!p.error,id+' '+level+' '+kind+': '+p.error);activities++;
 }
 for(const f of ['grade5/grade5-native-notes.js','worksheet-generator/planner/scope-algebra2.js','worksheet-generator/planner/course.js','worksheet-generator/planner/planner.js'])run(f);
 assert.equal(G.MKPLAN_COURSE,'grade5');
 for(const day of G.MKPLAN_SCOPE.days)for(const level of ['cp2','cp1','honors']){
  const plan=G.MKPLAN.buildDay(day.day,{level,seed:'elementary',practice:8});
  assert.equal(G.MKPLAN.summary(plan).failed,0,'lesson '+day.day+' '+level);
  if(day.day_type==='Lesson'){const sk=G.MKPLAN_SKILLS.lessons[day.lesson_id].skills[0][1];assert.ok(G.MKPLAN_TEACH.grade5[sk]?.cards.length);}
  lessons++;
 }
 for(const file of ['worksheet.html','menu-assessment.html','lesson-planner.html','printables.html'])assert.ok(fs.readFileSync(path.join(site,'worksheet-generator',file),'utf8').includes('grade5-main-catalog.js'));
 assert.ok(fs.readFileSync(path.join(site,'grade5/worksheet-generator/grade5-generators.html'),'utf8').includes("activity:'printables.html'"));
 console.log(`PASS elementary shared engines: ${papers} paper versions, ${activities} activities, ${lessons} lesson plans; bank levels, diagram assets, keys, no repeats, JSON restore and legacy routing.`);
})().catch(e=>{console.error(e);process.exitCode=1;});
