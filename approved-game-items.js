/* Approved-bank game question preparation. Existing legacy game engines stay separate. */
(function(root){
'use strict';
var eligibility=root.MK_RESOURCE_ELIGIBILITY;
var GAME_TYPES=['connect-4','tic-tac-toe','picture-reveal'];
function prepare(options){
 options=options||{};
 if(GAME_TYPES.indexOf(options.game)<0)return {ready:false,reason:'Unsupported game',items:[]};
 var result=eligibility.describe(options.game,options.courseId,options.unitId,options.level,options.skillIds);
 if(!result.ready)return {ready:false,reason:result.reason,items:[]};
 var items=result.questions.filter(function(q){
   if(q.diagram)return false; // diagrams must be handled by a renderer before gameplay
   if(q.format==='multiple-choice')return Array.isArray(q.options)&&q.options.length>=2&&q.options.filter(function(a){return a.correct===true}).length===1;
   return q.format==='short-answer'&&typeof q.answer==='string'&&q.answer.trim().length>0;
 }).map(function(q){
   var options=q.format==='multiple-choice'?q.options.map(function(o){return {text:o.text,correct:o.correct===true}}):[];
   return {id:q.id,skillId:q.skillId,prompt:q.prompt,answer:q.answer,options:options,solutionSteps:q.solutionSteps.slice()};
 });
 return {ready:items.length>0,reason:items.length?'':'No compatible approved text-only questions',items:items};
}
root.MK_APPROVED_GAME_ITEMS={version:1,prepare:prepare};
})(typeof window!=='undefined'?window:globalThis);
