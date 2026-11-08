'use strict';
const fs=require('node:fs'),vm=require('node:vm'),path=require('node:path'),assert=require('node:assert/strict');
const root=path.resolve(__dirname,'..'),g={window:{}};
for(const p of ['data.js','course-catalog.js','question-bank-adapter.js'])vm.runInNewContext(fs.readFileSync(path.join(root,p),'utf8'),g);
const course=g.window.LIBRARY.courses.find(c=>c.id==='statistics');assert(course&&!course.planned&&!course.comingSoon);
const allIds=new Set();let total=0,cells=0,partnerPairs=0,errorItems=0;
for(const unit of course.units){
 const bank=JSON.parse(fs.readFileSync(path.join(root,'question-banks/statistics',unit.id+'.json'),'utf8'));
 const check=g.window.MK_QUESTION_BANKS.validate(bank);assert(check.ok,check.errors.join('\n'));
 for(const q of bank.questions){assert(!allIds.has(q.id),'Duplicate ID '+q.id);allIds.add(q.id);total++;
  if(q.format==='multiple-choice'){assert.equal(q.options.filter(o=>o.correct).length,1);assert.equal(String(q.answer),q.options.find(o=>o.correct).text,'Key mismatch '+q.id);}
  if(q.diagram?.type==='image')assert(fs.existsSync(path.join(root,q.diagram.spec.src)),'Missing figure '+q.id);
 }
 const pairs=new Map();
 for(const q of bank.questions){
  if(/family: [^)]*_error\)/.test(q.sourceNotes||''))errorItems++;
  const m=/Partner Check pair (\S+) \((A|B)\)/.exec(q.sourceNotes||'');if(!m)continue;
  if(!pairs.has(m[1]))pairs.set(m[1],{});assert(!pairs.get(m[1])[m[2]],'Duplicate pair side');pairs.get(m[1])[m[2]]=q;
 }
 for(const [id,pair] of pairs){assert(pair.A&&pair.B,'Incomplete pair '+id);assert.equal(pair.A.answer,pair.B.answer);assert.equal(pair.A.skillId,pair.B.skillId);assert.equal(pair.A.level,pair.B.level);assert.notEqual(pair.A.prompt,pair.B.prompt);partnerPairs++;}
 for(const level of ['cp2','cp1','honors']){
  const qs=bank.questions.filter(q=>q.level===level),mc=qs.filter(q=>q.format==='multiple-choice');assert(mc.length>=25,'Insufficient whole-unit game pool '+unit.id+'/'+level);
  for(const skill of g.window.MK_COURSE_CATALOG.getSkillRecords('statistics',unit.id)){assert(qs.filter(q=>q.skillId===skill.id).length>=8,'Thin skill '+skill.id+'/'+level);cells++;}
  // Escape room needs one integer cipher and a separate substantive multi-step question.
  const pool=qs.filter(q=>['multiple-choice','short-answer'].includes(q.format));
  const cipher=pool.find(q=>{const m=/^(?:[A-Za-z]\s*=\s*)?([+-]?\d+(?:\.0+)?)$/.exec(String(q.answer).replace(/−/g,'-'));return m&&+m[1]>=1&&+m[1]<=25;});
  assert(cipher,'No cipher candidate '+unit.id+'/'+level);
  assert(pool.some(q=>q.id!==cipher.id&&q.solutionSteps.length>=4),'No separate 4-step sorting question '+unit.id+'/'+level);
 }
 const kinds=unit.artifacts.map(a=>(/kind=([a-z]+)/.exec(a.path)||[])[1]);
 assert(kinds.includes('partner')&&kinds.includes('error'),'Partner Check and Error Analysis must be linked');
 for(const kind of ['color','who'])assert(kinds.includes(kind),'Missing expanded printable '+kind);
}
assert.equal(partnerPairs,114);assert.equal(errorItems,140);assert.equal(total,1931);assert.equal(cells,114);assert.equal(g.window.LIBRARY.courses.find(c=>c.id==='discrete').units.length,10,'Discrete outline must be preserved');
console.log('PASS 1,931 Statistics questions, all 114 topic/level cells, figure assets, answer keys, whole-unit game pools, and supported resource links');


