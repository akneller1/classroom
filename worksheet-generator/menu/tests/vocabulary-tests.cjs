'use strict';
const assert=require('node:assert/strict');
const env=require('./load.cjs')(['vocabulary-data.js','vocabulary-data-middle-grades.js','vocabulary-tasks.js','menu/vocabulary.js']);
const M=env.MKMENU,T=env.MK_VOCAB_TASKS;
const J=x=>JSON.parse(JSON.stringify(x));
let questions=0,units=0;
function config(unit,format,n=3){
 const c=M.defaultConfig(unit,'test');c.seed=123;c.versions=3;
 c.sections=[{id:'vocab',name:'Vocabulary',points:2,offered:n,required:n,tier:'ramp',adjust:0,skills:null,qformat:format}];return c;
}
for(const unit of Object.keys(env.MKVOCAB_BANKS)){
 if(T.terms(unit).length<3)continue;
 // Exercise both existing skill sets and courses registered after the async bank loader finishes.
 if(!M.skillSets[unit])M.registerSkillSet({id:unit,unitName:unit,tags:{X:'Math'},skills:[{id:'math',tag:'X',generate(){throw Error('Math generator must not be called for vocabulary')}}]});
 for(const level of ['cp2','cp1','honors'])for(const format of ['vocab_blank','vocab_match','vocab_draw','vocab_example']){
  const c=config(unit,format,format==='vocab_match'?1:Math.min(3,T.terms(unit).filter(t=>format!=='vocab_draw'||t.draw).length));c.level=level;
  if(!c.sections[0].offered) {assert(!M.formatAvailable(c,0,format));continue;}
  c.vocabularyWordBank=true;
  assert.equal(M.checkRules(c).errors.length,0,unit+' '+format);
  const state=M.newAssessment(c);
  assert.equal(M.blockers(state).length,0,unit+' '+format+' '+JSON.stringify(M.blockers(state)));
  for(const v of state.versions){
   assert.equal(v.sections[0].items.length,c.sections[0].offered);
   const seen=new Set();
   for(const p of v.sections[0].items){
    assert(!p.failed,unit+' '+p.reason);assert(M.verifyProblem(p,{}).ok);assert.equal(p.vocabulary.format,format);
    assert(!seen.has(p.key),'Duplicate within a version');seen.add(p.key);questions++;
    const wrong=J(p);wrong.parts[0].answer='WRONG';assert(!M.verifyProblem(wrong,{}).ok);
    const leak=J(p);leak.prompt+=' changed';assert(!M.verifyProblem(leak,{}).ok);
   }
  }
  const restored=M.deserialize(M.serialize(state));assert.equal(M.blockers(restored).length,0);
  const tampered=JSON.parse(M.serialize(state));tampered.versions[0].sections[0].items[0].parts[0].answer='WRONG';
  assert(M.blockers(M.deserialize(tampered)).length>0,'Tampered key must block printing');
 }
 units++;
}
const unit='algebra1-expressions-equations';
const c=config(unit,'vocab_blank',2);c.versions=1;c.vocabularyTerms=T.terms(unit).slice(0,3).map(t=>t.term);
let state=M.newAssessment(c);let before=state.versions[0].sections[0].items[0];
let next=M.regenerate(state,0,before.uid);assert(!next.failed);assert.notEqual(before.key,next.key);
const blank=J(c);blank.vocabularyTerms=[];assert(M.checkRules(blank).errors.length>0);
const excess=J(c);excess.sections[0].offered=10;assert(M.checkRules(excess).errors.length>0);
const normal=M.defaultConfig(unit,'test');assert(M.sectionSkills(normal,0).every(id=>!M.isVocabularyFormat(id)));
const menu=M.defaultConfig(unit);assert(!M.coverageTags(menu).includes('V'));assert.equal(M.checkRules(menu).errors.length,0);
const mixed=M.defaultConfig(unit,'test');mixed.versions=2;mixed.sections.push(c.sections[0]);state=M.newAssessment(mixed);assert.equal(M.blockers(state).length,0);
assert(state.versions.every(v=>v.sections[0].items.every(p=>!p.vocabulary)&&v.sections[2].items.every(p=>p.vocabulary)));
// Source wording is identical for creative Honors tasks in both makers.
const draw=T.terms(unit).find(t=>t.draw);if(draw){const cfg=config(unit,'vocab_draw',1);cfg.level='honors';cfg.vocabularyTerms=[draw.term];assert.equal(M.newAssessment(cfg).versions[0].sections[0].items[0].prompt,T.honorsTask(draw,'draw'));}
console.log(`PASS vocabulary assessment integration: ${units} units, ${questions} questions, all levels and 3 versions; keys, regeneration, saved files, tampering, limits and mixed math/vocabulary.`);
