'use strict';const fs=require('node:fs'),path=require('node:path'),vm=require('node:vm'),assert=require('node:assert/strict');
const site=path.resolve(process.argv[2]||'_site'),G=require('../worksheet-generator/menu/tests/load.cjs')(['games/bank.js','menu/render.js']);
G.location={hash:'#course=grade1'};G.fetch=async url=>({ok:true,json:async()=>JSON.parse(fs.readFileSync(path.resolve(site,'worksheet-generator',url)))});
const run=f=>vm.runInContext(fs.readFileSync(path.join(site,f),'utf8'),G,{filename:f});
for(const f of ['data.js','course-integrations.js','course-catalog.js','grade5/grade5-main-catalog.js','grade4-main-catalog.js','grade3-main-catalog.js','grade2-main-catalog.js','grade1-main-catalog.js','question-bank-adapter.js','question-bank-loader.js','worksheet-generator/core/plot.js','worksheet-generator/algebra2-bank-native.js'])run(f);
(async()=>{await G.MK_COURSE_BANKS_READY;
for(const f of ['core/elementary/directions.js','menu/elementary-print.js','core/elementary/show-what-you-know.js','menu/show-what-you-know.js','menu/printables.js','menu/young-activities.js'])run('worksheet-generator/'+f);
const M=G.MKMENU,P=M.printables;let quizzes=0,activities=0,pictures=0;
for(const grade of ['grade1','grade2'])for(const unit of Object.keys(G.MK_SHOW_WHAT_YOU_KNOW.courses[grade])){
 const id=grade+'-'+unit,c=M.defaultConfig(id,'test');c.versions=2;M.applyShowWhatYouKnow(c);const st=M.newAssessment(c),reviewed=G.MK_SHOW_WHAT_YOU_KNOW.courses[grade][unit];
 const a=st.versions[0].sections.flatMap(s=>s.items),b=st.versions[1].sections.flatMap(s=>s.items);
 assert.deepEqual(Array.from(a,p=>p.sourceId),Array.from(reviewed.versions.A));assert.deepEqual(Array.from(b,p=>p.sourceId),Array.from(reviewed.versions.B));assert(!a.some(p=>b.some(q=>p.sourceId===q.sourceId)));
 for(const p of [...a,...b]){assert(!p.failed);if(p.mc)assert(M.checkChoices(p));if(p.fig)assert(fs.existsSync(path.join(site,p.fig.src)))}
 const before=a[1].sourceId;M.regenerate(st,0,a[1].uid);assert.notEqual(st.versions[0].sections[1].items[0].sourceId,before,'New problem must replace preset item');
 assert(!P.kindsFor(id).some(x=>['who','tarsia','vocabulary'].includes(x.id)));quizzes+=2;
}
for(const grade of [1,2])for(const kind of ['maze','color','roll-cover','cut-paste','number-bonds','spin-solve'])for(let seed=1;seed<=12;seed++){
 const id='grade'+grade+'-add-subtract-'+(grade===1?'10':'20'),cfg=P.defaultConfig(id,kind);cfg.seed=seed;const b=P.build(cfg,0);assert(!b.error,id+' '+kind+': '+b.error);
 if(b.items.length){assert.equal(new Set(b.items.map(x=>x.answer)).size,b.items.length);b.items.forEach(x=>assert(x.wrong>=0&&x.wrong!==x.answer));}
 if(b.bonds)b.bonds.forEach(x=>assert.equal(x.values[0],x.values[1]+x.values[2]));
 if(b.cards)b.cards.forEach(x=>assert.equal(x.group,grade===2?x.value%2:x.value===10?0:1));
 if(b.board){assert.equal(b.board.length,20);for(let n=2;n<=12;n++)assert(b.board.includes(n))}
 for(const key of [false,true]){const pages=P.youngPages(cfg,b,0,1,key);assert.equal(pages.length,1);assert(!pages[0].html.includes('undefined'));}
 activities++;
}
for(const grade of [2,3,4,5]){const dir=path.join(site,'question-banks/grade'+grade);for(const file of fs.readdirSync(dir)){const bank=JSON.parse(fs.readFileSync(path.join(dir,file)));for(const q of bank.questions){if(q.diagram?.spec?.src.includes('/kid-friendly/')){assert(fs.existsSync(path.join(site,q.diagram.spec.src)));assert(q.diagram.spec.alt);const native=path.join(site,'grade'+grade,grade===5?'math5':'question-banks/math'+grade,file);const copy=JSON.parse(fs.readFileSync(native)).questions.find(x=>x.id===q.id);assert(copy.diagram);assert(fs.existsSync(path.join(site,'grade'+grade,copy.diagram.spec.src)));pictures++}}}}
assert.equal(pictures,1195);console.log(`PASS ${quizzes} reviewed quizzes with replacements, ${activities} seeded activities, ${pictures} pictures and native copies.`);
})().catch(e=>{console.error(e);process.exitCode=1});
