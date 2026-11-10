#!/usr/bin/env node
'use strict';
/* Read-only curriculum question-bank audit.
 * A shared question stem is NOT a duplicate when its answers, diagrams,
 * answer choices, parts, or levels differ.
 * This script does not certify mathematical correctness.
 */
const fs=require('node:fs'),path=require('node:path'),vm=require('node:vm');
const ROOT=path.resolve(__dirname,'..');
const OUTPUT=path.join(ROOT,'question-bank-audit-results');
fs.mkdirSync(OUTPUT,{recursive:true});
const load=p=>JSON.parse(fs.readFileSync(path.join(ROOT,p),'utf8'));
const catalogContext={window:{}};
vm.runInNewContext(fs.readFileSync(path.join(ROOT,'course-catalog.js'),'utf8'),catalogContext,{filename:'course-catalog.js'});
vm.runInNewContext(fs.readFileSync(path.join(ROOT,'question-bank-adapter.js'),'utf8'),catalogContext,{filename:'question-bank-adapter.js'});
const catalog=catalogContext.window.MK_COURSE_CATALOG,adapter=catalogContext.window.MK_QUESTION_BANKS;
const manifest=load('question-banks/manifest.json');
// Mathematical superscripts, subscripts and other notation are meaningful: NFKC
// would collapse 2ⁿ and 2n into the same distractor, producing false positives.
const normalize=x=>String(x===undefined||x===null?'':x).normalize('NFC').replace(/\s+/g,' ').trim().toLowerCase();
const stable=x=>JSON.stringify(x,(_,v)=>v&&typeof v==='object'&&!Array.isArray(v)
  ?Object.fromEntries(Object.keys(v).sort().map(k=>[k,v[k]])):v);
const sha=x=>require('node:crypto').createHash('sha256').update(x).digest('hex').slice(0,16);
const issues=[],units=[],rows=[],globalIds=new Map();
const add=(severity,code,course,unit,detail,qid='')=>issues.push({severity,code,course,unit,qid,detail});
if(manifest.version!==1||!Array.isArray(manifest.banks))throw Error('Manifest is not version 1 with a bank list');
const manifestKeys=new Set();
for(const entry of manifest.banks){
 const course=entry.courseId,unit=entry.unitId,key=course+'/'+unit,p=entry.path;
 if(manifestKeys.has(key)){add('error','manifest-duplicate',course,unit,'Duplicate manifest entry');continue}
 manifestKeys.add(key);
 if(!/^[a-z0-9-]+$/.test(course)||!/^[a-z0-9-]+$/.test(unit)||p!=='question-banks/'+key+'.json'){
  add('error','manifest-path',course,unit,'Invalid or mismatched manifest path: '+p);continue;
 }
 if(!fs.existsSync(path.join(ROOT,p))){add('error','missing-file',course,unit,p);continue}
 let bank;
 try{bank=load(p)}catch(e){add('error','invalid-json',course,unit,e.message);continue}
 const shape=adapter.validate(bank);
 if(!shape.ok)add('error','schema',course,unit,shape.errors.slice(0,20).join(' | ')+(shape.errors.length>20?' + more':''));
 if(bank.courseId!==course||bank.unitId!==unit)add('error','bank-identity',course,unit,'Course or unit ID differs from manifest');
 const list=Array.isArray(bank.questions)?bank.questions:[];
 const skills=catalog.getSkillRecords(course,unit),skillIds=new Set(skills.map(s=>s.id));
 const skillCounts=Object.fromEntries(skills.map(s=>[s.id,{cp2:0,cp1:0,honors:0}]));
 const levels={cp2:0,cp1:0,honors:0},formats={},exact=new Map(),stemCount=new Map();
 let imageCount=0,mcIssues=0,exactCount=0,stemRepeats=0,wrongChoices=0,blankAnswer=0,missingSteps=0;
 for(const q of list){
  if(!q||typeof q!=='object')continue;
  const id=String(q.id||''),level=q.level,skill=q.skillId;
  if(globalIds.has(id))add('review','id-reused-across-banks',course,unit,'Also in '+globalIds.get(id),id);
  else globalIds.set(id,p);
  if(skillCounts[skill]&&skillCounts[skill][level]!==undefined)skillCounts[skill][level]++;
  else add('error','unknown-skill-or-level',course,unit,skill+' / '+level,id);
  levels[level]=(levels[level]||0)+1;formats[q.format]=(formats[q.format]||0)+1;
  if(q.answer===undefined||q.answer===null||normalize(q.answer)===''){blankAnswer++;add('error','blank-answer',course,unit,'Answer missing or blank',id)}
  if(!Array.isArray(q.solutionSteps)||q.solutionSteps.length===0||q.solutionSteps.every(x=>!normalize(x))){
   missingSteps++;add('error','missing-steps',course,unit,'No worked solution steps',id);
  }
  if(q.diagram?.type==='image'){
   imageCount++;
   const src=q.diagram.spec?.src;
   if(!src||!src.startsWith('question-banks/assets/')||!fs.existsSync(path.join(ROOT,src)))
    add('error','missing-diagram',course,unit,'Referenced image missing: '+src,id);
  }
  // Each distinct question is defined by its full instructional content.
  const fingerprint=sha(stable({skill,level,format:q.format,prompt:q.prompt,answer:q.answer,
    options:q.options,parts:q.parts,diagram:q.diagram,solutionSteps:q.solutionSteps}));
  if(exact.has(fingerprint)){
   exactCount++;
   add('review','exact-duplicate',course,unit,'Identical complete question to '+exact.get(fingerprint),id);
  }else exact.set(fingerprint,id);
  const stem=skill+'|'+normalize(q.prompt);
  if(stemCount.has(stem))stemRepeats++;else stemCount.set(stem,id);
  if(['multiple-choice','select-all'].includes(q.format)){
   const opts=Array.isArray(q.options)?q.options:[],correct=opts.filter(o=>o?.correct===true);
   if(opts.length<2||(q.format==='multiple-choice'&&correct.length!==1)||(q.format==='select-all'&&correct.length<2)){
    mcIssues++;add('error','choice-cardinality',course,unit,'Incorrect number of choices or correct options',id);
   }
   const texts=opts.map(o=>normalize(o?.text)),seen=new Set();
   for(const text of texts){
    if(text&&seen.has(text)){wrongChoices++;add('review','identical-choice-text',course,unit,'Repeated answer-choice text: '+text.slice(0,70),id);break}
    seen.add(text);
   }
   // Treat answer/choice disagreements as review-only: equivalent math may use different notation.
   if(q.format==='multiple-choice'&&correct.length===1
      &&typeof q.answer==='string'&&typeof correct[0].text==='string'
      &&normalize(q.answer)!==normalize(correct[0].text)){
    add('review','answer-choice-text-differs',course,unit,
      'Stored answer differs textually from marked correct option',id);
   }
  }
 }
 const zero=Object.entries(skillCounts).flatMap(([skill,byLevel])=>
  Object.entries(byLevel).filter(([,count])=>count===0).map(([level])=>skill+'/'+level));
 const sparse=Object.entries(skillCounts).flatMap(([skill,byLevel])=>
  Object.entries(byLevel).filter(([,count])=>count>0&&count<5).map(([level,count])=>skill+'/'+level+'('+count+')'));
 if(zero.length)add('review','missing-skill-level',course,unit,zero.slice(0,40).join(', ')+(zero.length>40?'…':''));
 if(sparse.length)add('review','thin-skill-level',course,unit,sparse.slice(0,40).join(', ')+(sparse.length>40?'…':''));
 const summary={course,unit,path:p,questions:list.length,skills:skills.length,
  cp2:levels.cp2,cp1:levels.cp1,honors:levels.honors,
  formats,images:imageCount,exactDuplicates:exactCount,repeatedPromptStems:stemRepeats,
  emptySkillLevels:zero.length,thinSkillLevels:sparse.length,
  choiceIssues:mcIssues,identicalChoiceTexts:wrongChoices,blankAnswers:blankAnswer,missingSteps,
  eligibility:entry.approved===true?'approved':entry.teacherUse===true?'teacher-use':'unapproved'};
 units.push(summary);rows.push(summary);
}
const grouped={};
for(const u of units){
 const g=grouped[u.course]??={banks:0,questions:0,skills:0,exactDuplicates:0,emptySkillLevels:0,thinSkillLevels:0,cp2:0,cp1:0,honors:0};
 g.banks++;g.questions+=u.questions;g.skills+=u.skills;g.exactDuplicates+=u.exactDuplicates;
 g.emptySkillLevels+=u.emptySkillLevels;g.thinSkillLevels+=u.thinSkillLevels;
 g.cp2+=u.cp2;g.cp1+=u.cp1;g.honors+=u.honors;
}
const total=units.reduce((x,u)=>x+u.questions,0);
const summary={
 generatedAt:new Date().toISOString(),scope:'manifest-listed JSON banks only; excludes procedural Algebra 1 and Geometry generators',
 manifestEntries:manifest.banks.length,readableBanks:units.length,questions:total,
 courseTotals:grouped,issuesBySeverity:issues.reduce((x,i)=>(x[i.severity]=(x[i.severity]||0)+1,x),{}),
 issueTypes:issues.reduce((x,i)=>(x[i.code]=(x[i.code]||0)+1,x),{})
};
fs.writeFileSync(path.join(OUTPUT,'report.json'),JSON.stringify({summary,units,issues},null,2));
const escCSV=x=>'"'+String(x===undefined?'':x).replaceAll('"','""')+'"';
const columns=['course','unit','questions','skills','cp2','cp1','honors','exactDuplicates','repeatedPromptStems','emptySkillLevels','thinSkillLevels','choiceIssues','identicalChoiceTexts','images','eligibility'];
fs.writeFileSync(path.join(OUTPUT,'unit-coverage.csv'),columns.join(',')+'\n'+rows.map(u=>columns.map(k=>escCSV(u[k])).join(',')).join('\n')+'\n');
fs.writeFileSync(path.join(OUTPUT,'review-issues.csv'),['severity','code','course','unit','qid','detail'].join(',')+'\n'+issues.map(i=>['severity','code','course','unit','qid','detail'].map(k=>escCSV(i[k])).join(',')).join('\n')+'\n');
let md='# Question-bank audit\n\n';
md+='*Read-only analysis. Exact text repetitions are not automatically duplicates; mathematical correctness is not certified.*\n\n';
md+='**'+units.length+' banks, '+total.toLocaleString()+' questions** across '+Object.keys(grouped).length+' courses. Algebra 1 and Geometry use separate generators.\n\n';
md+='| Course | Banks | Questions | CP2 | CP1 | Honors | Exact duplicates | Empty skill × level |\n|---|---:|---:|---:|---:|---:|---:|---:|\n';
for(const [name,g] of Object.entries(grouped))md+='| '+name+' | '+g.banks+' | '+g.questions+' | '+g.cp2+' | '+g.cp1+' | '+g.honors+' | '+g.exactDuplicates+' | '+g.emptySkillLevels+' |\n';
md+='\n## Issue counts\n\n';
for(const [code,count] of Object.entries(summary.issueTypes).sort((a,b)=>b[1]-a[1]))md+='- '+code+': '+count+'\n';
md+='\n## Highest-priority bank review\n\n';
for(const u of units.slice().sort((a,b)=>(b.emptySkillLevels*50+b.exactDuplicates*4+b.choiceIssues*10)-(a.emptySkillLevels*50+a.exactDuplicates*4+a.choiceIssues*10)).slice(0,20)){
 md+='- '+u.course+'/'+u.unit+': '+u.questions+' questions; '+u.emptySkillLevels+' missing skill-level cells; '+u.exactDuplicates+' exact duplicates; '+u.choiceIssues+' invalid choices\n';
}
md+='\nSource: question-banks/manifest.json and course-catalog.js. Verify suspected mathematical errors manually before editing banks.\n';
fs.writeFileSync(path.join(OUTPUT,'summary.md'),md);
if(process.env.GITHUB_STEP_SUMMARY)fs.appendFileSync(process.env.GITHUB_STEP_SUMMARY,md);
console.log(JSON.stringify(summary,null,2));
console.log('Audit reports written to '+OUTPUT);
