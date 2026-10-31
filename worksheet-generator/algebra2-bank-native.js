/* Reuse authored Algebra 2 items in existing players. No question, diagram,
 * distractor, or worked solution is generated here. Source keys are not
 * independently verified mathematics. */
(function(G){'use strict';
const NS=G.MKMENU, GB=G.MKGAMES;
if(!NS||!GB||!G.MK_BANK_LOADER)return;
const prefix='algebra2-', registry=new Map(),isBank=id=>registry.has(id);
const raw=new Map();
function level(c,policy){return policy&&['cp2','cp1','honors'].includes(policy.level)?policy.level:c<=2?'cp2':c<=5?'cp1':'honors'}
function pool(id,skill,c,policy,formats){return G.MK_QUESTION_BANKS.select({courseId:registry.get(id).courseId,unitId:registry.get(id).unitId,skillIds:[skill],level:level(c,policy),formats:formats||['multiple-choice']})}
function text(a){return typeof a==='object'?JSON.stringify(a):String(a)}
function figure(q){return q.diagram?.type==='image'?{kind:'authored-image',src:q.diagram.spec.src,alt:q.diagram.spec.alt}:null}
function problem(q,id,c){return {uid:q.id,sourceId:q.id,source:'authored-bank',authoredOptions:q.options||[],skill:q.skillId,c,tag:q.skillId,prompt:q.prompt,fig:figure(q),parts:[{answer:text(q.answer),prompt:''}],steps:q.solutionSteps.map(t=>({t})),key:q.id,sig:q.id,verify:{status:'source-key',issues:[]}}}
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
function item(q,id,c){return {id:q.id,sourceId:q.id,p:problem(q,id,c),k:0,skill:q.skillId,skillName:NS.skillSets[id].byId[q.skillId].name,tag:q.skillId,tagName:NS.skillSets[id].byId[q.skillId].name,c,q:{prompt:q.prompt,fig:figure(q),ask:''},answer:text(q.answer),steps:q.solutionSteps.map(t=>({t})),options:(q.options||[]).map(o=>({a:o.text,ok:o.correct===true})),typed:null}}
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
  const formats=G.document?.body.getAttribute('data-game')==='flashcards'?['short-answer','multiple-choice']:['multiple-choice'];
  const q=choose(pool(id,slot.skill,slot.c,null,formats),(opts.seed||Date.now())+'|'+i,used);
  if(q){used.keys.add(q.id);const it=item(q,id,slot.c);it.slot=slot;out.push(it)}
 }
 if(opts.progress)opts.progress(slots.length,slots.length);done(out);
};
const figHtml=NS.figHtml;
NS.figHtml=function(fig){
 if(fig?.kind!=='authored-image')return figHtml.apply(this,arguments);
 const esc=s=>String(s).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
 return '<img class="authored-bank-image" src="../'+esc(fig.src)+'" alt="'+esc(fig.alt)+'" style="display:block;max-width:100%;max-height:280px;object-fit:contain;margin:12px auto">';
};
G.MK_ALGEBRA2_NATIVE_READY=G.MK_BANK_LOADER.loadFromSite('question-banks/manifest.json','../').then(function(){
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
   NS.registerSkillSet({id,unitName:u.name,courseName:c.name,title:u.name+' Activities',tags,skills:records.map(s=>({id:s.id,name:s.name,tag:s.id,print:['maze','color','partner','who','stations'],generate:function(){throw Error('Authored bank selection required')}}))});
  });
 });
 // Preserve original levels while selecting authored banks by exact level.
 if(G.document?.body.hasAttribute('data-algebra2-game')) { GB.LEVELS.cp2.tiers=[1,1,1];GB.LEVELS.cp1.tiers=[4,4,4];GB.LEVELS.honors.tiers=[6,6,6]; }
 G.MK_COURSE_BANKS_READY=G.MK_ALGEBRA2_NATIVE_READY;return course;
});
})(window);
