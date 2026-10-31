/* Reuse authored Algebra 2 items in existing players. No question, diagram,
 * distractor, or worked solution is generated here. Source keys are not
 * independently verified mathematics. */
(function(G){'use strict';
const NS=G.MKMENU, GB=G.MKGAMES;
if(!NS||!GB||!G.MK_BANK_LOADER)return;
const prefix='algebra2-', registry=new Map(),isBank=id=>registry.has(id);
const raw=new Map();
function level(c,policy){return policy&&['cp2','cp1','honors'].includes(policy.level)?policy.level:c<=2?'cp2':c<=5?'cp1':'honors'}
function pool(id,skill,c,policy,formats){return G.MK_QUESTION_BANKS.select({courseId:registry.get(id).courseId,unitId:registry.get(id).unitId,skillIds:[skill],level:policy?.level==='mixed'?undefined:level(c,policy),formats:formats||['short-answer','multiple-choice','select-all','open-response']})}
function text(a){return typeof a==='object'?JSON.stringify(a):String(a)}
function figure(q){return q.diagram?.type==='image'?{kind:'authored-image',src:q.diagram.spec.src,alt:q.diagram.spec.alt}:null}
function problem(q,id,c){const parts=Array.isArray(q.parts)&&q.parts.length?q.parts.map((part,i)=>({answer:text(part.answer),prompt:part.prompt||'',label:String.fromCharCode(97+i)})):[{answer:text(Array.isArray(q.answer)?q.answer.join('; '):q.answer),prompt:''}];return {uid:q.id,sourceId:q.id,source:'authored-bank',authoredFormat:q.format,authoredOptions:q.options||[],approved:true,skill:q.skillId,c,tag:q.skillId,prompt:q.prompt,fig:figure(q),parts,steps:(q.solutionSteps||[]).map(t=>({t})),key:q.id,sig:q.id,verify:{status:'source-key',issues:[]}}}
function choose(items,seed,used){const rng=G.MKWS.rng.make(G.MKWS.rng.hash(String(seed)));return rng.shuffle(items).find(q=>!used?.keys?.has(q.id))}
const generate=NS.generateProblem;
NS.generateProblem=function(id,skill,c,policy,seed,used){
 if(!isBank(id))return generate.apply(this,arguments);
 const q=choose(pool(id,skill,c,policy,policy?.authoredFormats),seed,used);
 if(!q)return {failed:true,reason:'No unused authored questions match these skills and difficulty.'};
 used?.keys?.add(q.id);used?.sigs?.add(q.id);return problem(q,id,c);
};
const distractors=GB.distractors, answerOk=GB.answerOk, makeItems=GB.makeItems, has=GB.hasGameItems, deck=GB.buildDeck;
GB.distractors=function(p,k,rng,n){if(p.source!=='authored-bank')return distractors.apply(this,arguments);return (raw.get(p.sourceId)?.options||[]).filter(o=>!o.correct).map(o=>o.text).slice(0,n)};
GB.answerOk=function(p,k,answer){if(p.source!=='authored-bank')return answerOk.apply(this,arguments);return {ok:String(answer)===String(p.parts[k].answer),status:'source-key'}};
GB.hasGameItems=function(id,skill){return isBank(id)?pool(id,skill,4,{level:'cp1'},['multiple-choice','short-answer']).length>0:has.apply(this,arguments)};
function item(q,id,c){return {id:q.id,sourceId:q.id,p:problem(q,id,c),k:0,skill:q.skillId,skillName:NS.skillSets[id].byId[q.skillId].name,tag:q.skillId,tagName:NS.skillSets[id].byId[q.skillId].name,c,q:{prompt:q.prompt,fig:figure(q),ask:(q.format==='select-all'?'Select all that apply.\n':'')+(q.parts||[]).map((p,i)=>'('+String.fromCharCode(97+i)+') '+p.prompt).join('\n')},answer:text(q.answer),steps:q.solutionSteps.map(t=>({t})),options:(q.options||[]).map(o=>({a:o.text,ok:o.correct===true})),typed:null}}
GB.makeItems=function(id,skill,c,policy,seed,used){
 if(!isBank(id))return makeItems.apply(this,arguments);
 const q=choose(pool(id,skill,c,policy),seed,used);if(!q)return [];
 used?.keys?.add(q.id);return [item(q,id,c)];
};
// Keep each selected difficulty exact. Native procedural decks otherwise retry
// nearby tiers, which would cross authored CP2/CP1/Honors boundaries.
GB.buildDeck=function(id,slots,opts,done){
 if(!isBank(id))return deck.apply(this,arguments);
 opts=opts||{};const used={keys:new Set()},out=[];
 for(const [i,slot] of slots.entries()){
  const game=G.document?.body.getAttribute('data-game');
  const formats=game==='showdown'?['short-answer','multiple-choice','select-all','open-response']:game==='flashcards'?['short-answer','multiple-choice']:['multiple-choice'];
  const seed=(opts.seed||Date.now())+'|'+i;
  const q=slot.level==='mixed'?(choose(pool(id,slot.skill,slot.c,null,formats),seed,used)||choose(pool(id,slot.skill,slot.c,{level:'mixed'},formats),seed,used)):choose(pool(id,slot.skill,slot.c,slot.level?{level:slot.level}:null,formats),seed,used);
  if(q){used.keys.add(q.id);const it=item(q,id,slot.c);it.slot=slot;out.push(it)}
 }
 if(opts.progress)opts.progress(slots.length,slots.length);done(out);
};

// Preserve the native menu/worksheet/lesson-planner workflows for Algebra 2 while
// drawing only from the approved bank and its authored answer keys.
const nativeFormats={open:'short-answer',mc:'multiple-choice',multi:'select-all',mcas:'open-response'};
function sourceQuestion(p){return p&&p.source==='authored-bank'?raw.get(p.sourceId):null}
const makeChoices=NS.makeChoices,makeMulti=NS.makeMultiSelect,makeMcas=NS.makeMcas;
NS.makeChoices=function(p){
 const q=sourceQuestion(p);if(!q)return makeChoices.apply(this,arguments);
 const opts=q.options||[],correct=opts.map((o,i)=>o.correct===true?i:-1).filter(i=>i>=0);
 if(q.format!=='multiple-choice'||correct.length!==1||opts.length<2)return {fail:'This approved question is not a single-answer multiple-choice item.'};
 return {opts:opts.map(o=>o.text),key:correct[0],src:JSON.stringify([q.id,opts])};
};
NS.makeMultiSelect=function(p){
 const q=sourceQuestion(p);if(!q)return makeMulti.apply(this,arguments);
 const opts=q.options||[],keys=opts.map((o,i)=>o.correct===true?i:-1).filter(i=>i>=0);
 if(q.format!=='select-all'||keys.length<2||opts.length<4)return {fail:'This approved question is not a select-all item.'};
 return {opts:opts.map(o=>o.text),keys,direction:'Select all that apply.',src:JSON.stringify([q.id,opts])};
};
NS.makeMcas=function(p){
 const q=sourceQuestion(p);if(!q)return makeMcas.apply(this,arguments);
 return q.format==='open-response'&&(q.parts||[]).length>=4?{parts:q.parts.length}:{fail:'This approved question does not have four or more connected parts.'};
};
function authoredAvailable(id,skill,level,format){
 const item=registry.get(id);if(!item)return false;
 return G.MK_QUESTION_BANKS.select({courseId:item.courseId,unitId:item.unitId,skillIds:[skill],level:level,formats:[format]}).length>0;
}
const multiUnit=NS.multiUnitSupported,multiCap=NS.multiCapable,mcCap=NS.mcCapable,mcasCap=NS.mcasCapable,skillFmt=NS.skillFormatOk;
NS.multiUnitSupported=function(id){return isBank(id)?NS.skillSets[id].skills.some(s=>authoredAvailable(id,s.id,'cp1','select-all')):multiUnit.apply(this,arguments)};
NS.multiCapable=function(id,skill,c){return isBank(id)?['cp2','cp1','honors'].some(level=>authoredAvailable(id,skill,level,'select-all')):multiCap.apply(this,arguments)};
NS.mcCapable=function(id,skill,c){return isBank(id)?['cp2','cp1','honors'].some(level=>authoredAvailable(id,skill,level,'multiple-choice')):mcCap.apply(this,arguments)};
NS.mcasCapable=function(id,skill,c){return isBank(id)?['cp2','cp1','honors'].some(level=>authoredAvailable(id,skill,level,'open-response')):mcasCap.apply(this,arguments)};
NS.skillFormatOk=function(id,skill,format,c){
 if(!isBank(id))return skillFmt.apply(this,arguments);
 const bankFormat={open:'short-answer',mc:'multiple-choice',multi:'select-all',mcas:'open-response'}[format]||'short-answer';
 return ['cp2','cp1','honors'].some(level=>authoredAvailable(id,skill,level,bankFormat));
};
NS.authoredFormatForMenu=function(id,sectionFormat){
 return isBank(id)?[nativeFormats[sectionFormat]||'short-answer']:null;
};

const figHtml=NS.figHtml;
NS.figHtml=function(fig){
 if(fig?.kind!=='authored-image')return figHtml.apply(this,arguments);
 const esc=s=>String(s).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
 return '<img class="authored-bank-image" src="../'+esc(fig.src)+'" alt="'+esc(fig.alt)+'" style="display:block;max-width:100%;max-height:280px;object-fit:contain;margin:12px auto">';
};
var loadBanks=G.MK_APPROVED_RESOURCE_BANKS?G.MK_APPROVED_RESOURCE_BANKS.ready:G.MK_BANK_LOADER.loadFromSite('question-banks/manifest.json','../');
G.MK_ALGEBRA2_NATIVE_READY=loadBanks.then(function(){
 const course=G.LIBRARY.courses.find(c=>c.id==='algebra2');
 G.LIBRARY.courses.forEach(c=>{
  let group=NS.CATALOG.find(g=>g.course===c.name);if(!group){group={course:c.name,units:[]};NS.CATALOG.push(group)}
  if(c.id==='algebra2')group.units=c.units.map(u=>[c.id+'-'+u.id,u.name]);
  c.units.forEach(u=>{
   const id=(c.id==='algebra'?'algebra1-':c.id+'-')+u.id;
   if(!G.MK_QUESTION_BANKS.available(c.id,u.id))return;
   if(!group.units.some(item=>item[0]===id))group.units.push([id,u.name]);
   const records=G.MK_COURSE_CATALOG.getSkillRecords(c.id,u.id),tags={};records.forEach(s=>tags[s.id]=s.name);
   registry.set(id,{courseId:c.id,unitId:u.id});
   G.MK_QUESTION_BANKS.select({courseId:c.id,unitId:u.id}).forEach(q=>raw.set(q.id,q));
   NS.registerSkillSet({id,unitName:u.name,courseName:c.name,authoredBank:true,title:u.name+' Activities',tags,skills:records.map(s=>({id:s.id,name:s.name,tag:s.id,print:['maze','color','partner','who','stations'],generate:function(){throw Error('Authored bank selection required')}}))});
  });
 });
 // Preserve original levels while selecting authored banks by exact level.
 if(G.document?.body.hasAttribute('data-algebra2-game')) { GB.LEVELS.cp2.tiers=[1,1,1];GB.LEVELS.cp1.tiers=[4,4,4];GB.LEVELS.honors.tiers=[6,6,6]; }
 return course;
});
G.MK_COURSE_BANKS_READY=G.MK_ALGEBRA2_NATIVE_READY;
})(window);
