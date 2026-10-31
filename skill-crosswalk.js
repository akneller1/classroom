/* Curriculum crosswalk: candidate overlaps only. Does NOT approve or enable math generators. */
(function(root){
'use strict';
var catalog=root.MK_COURSE_CATALOG;
var definitions=[
 {key:'evaluating-expressions',source:['algebra','foundations-algebra','Order of Operations and Evaluating Expressions'],targets:[['math6','expressions-equations','Writing and Evaluating Algebraic Expressions'],['prealgebra7','algebraic-expressions-integers','Writing and Evaluating Expressions']]},
 {key:'distributive-property',source:['algebra','foundations-algebra','Distributive Property and Combining Like Terms'],targets:[['prealgebra7','one-step-equations-inequalities','The Distributive Property'],['prealgebra','equations-expressions','Solving equations using the distributive property']]},
 {key:'equations-both-sides',source:['algebra','expressions-equations','Equations with Variables on Both Sides'],targets:[['prealgebra7','solving-equations-inequalities','Solving Equations with Variables on Both Sides'],['prealgebra','equations-expressions','Solving equations with variables on both sides']]},
 {key:'systems-graphing',source:['algebra','systems-of-equations','Solving Systems by Graphing'],targets:[['prealgebra7','linear-functions-graphing','Solving Systems of Linear Equations by Graphing'],['prealgebra','systems-linear-equations','Solving systems by graphing']]},
 {key:'systems-substitution',source:['algebra','systems-of-equations','Solving Systems by Substitution'],targets:[['prealgebra7','linear-functions-graphing','Solving Systems of Linear Equations by Substitution'],['prealgebra','systems-linear-equations','Solving systems by substitution']]}
];
function find(tuple){
 var records=catalog.getSkillRecords(tuple[0],tuple[1]);
 var match=records.filter(function(x){return x.name.toLowerCase()===tuple[2].toLowerCase()});
 return match.length===1?{courseId:tuple[0],unitId:tuple[1],skillId:match[0].id,name:match[0].name}:null;
}
function matches(){
 return definitions.map(function(d){return {key:d.key,source:find(d.source),targets:d.targets.map(find),status:'candidate',enabled:false};});
}
function valid(){return matches().every(function(m){return !!m.source&&m.targets.every(Boolean)});}
root.MK_SKILL_CROSSWALK={version:1,matches:matches,valid:valid};
})(typeof window!=='undefined'?window:globalThis);
