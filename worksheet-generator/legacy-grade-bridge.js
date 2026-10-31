/* Grade 6–8 legacy generator bridge for existing flashcards and games.
 * Isolated from the independently verified question-bank registry.
 */
(function(root){'use strict';
var grades=['math6','prealgebra7','prealgebra'];
var framePromise=null;
function isGrade(courseId){return grades.indexOf(courseId)>=0;}
function load(){
 if(framePromise)return framePromise;
 framePromise=new Promise(function(resolve,reject){
  var f=document.createElement('iframe');f.hidden=true;f.setAttribute('aria-hidden','true');
  f.src='grade-practice.html';f.title='Shared mathematics question engine';
  f.addEventListener('load',function(){
   try{var w=f.contentWindow;if(!w.MK_LEGACY_CROSSWALK_AUDIT||!w.MK_LEGACY_REVIEW_SAMPLES)throw Error('Question engine missing');resolve(w)}
   catch(e){reject(e)}
  },{once:true});
  f.addEventListener('error',function(){reject(Error('Question engine failed to load'))},{once:true});
  document.body.appendChild(f);
 });return framePromise;
}
function matching(w,courseId,unitId,skillId){
 return w.MK_LEGACY_CROSSWALK_AUDIT.inspect(w.MK_SKILL_CROSSWALK,w.MKMENU).filter(function(entry){
  return entry.targets.some(function(t){return t&&t.courseId===courseId&&t.unitId===unitId&&(!skillId||t.skillId===skillId)});
 });
}
function prepare(w,options){
 var entries=matching(w,options.courseId,options.unitId,options.skillId),list=[];
 entries.forEach(function(entry){
  var target=entry.targets.find(function(t){return t&&t.courseId===options.courseId&&t.unitId===options.unitId&&(!options.skillId||t.skillId===options.skillId)});
  var result=w.MK_LEGACY_REVIEW_SAMPLES.sample(entry,options.courseId,options.level,'grade-native-'+entry.key,12);
  result.questions.filter(function(q){return !q.figure}).forEach(function(q){
   list.push({id:q.reviewKey,skillId:target.skillId,level:options.level,format:'multiple-choice',
    prompt:[q.prompt,q.partPrompt].filter(Boolean).join('\n'),answer:String(q.answer),
    options:q.options.map(function(o){return {text:String(o.text),correct:o.correct===true}}),
    solutionSteps:Array.isArray(q.steps)?q.steps.map(String):q.steps?[String(q.steps)]:[],
    verified:false,source:'existing-legacy-generator'});
  });
 });
 return list;
}
root.MK_GRADE_LEGACY_BRIDGE={isGrade:isGrade,load:load,prepare:prepare};
})(window);
