/* Conservative, read-only difficulty policy for candidate cross-course reuse.
 * Difficulty is not a grade equivalence. Only explicit per-topic/per-course
 * policies can request legacy generation, and no policy activates publishing.
 */
(function(root){'use strict';
var ranges={
 math6:{remedial:[1,1],standard:[1,2],advanced:[2,3]},
 prealgebra7:{remedial:[1,2],standard:[2,3],advanced:[3,4]},
 prealgebra:{remedial:[2,3],standard:[3,4],advanced:[4,5]}
};
var restrictions={
 'equations-both-sides':{math6:false,prealgebra7:false,prealgebra:true},
 'systems-graphing':{math6:false,prealgebra7:true,prealgebra:true},
 'systems-substitution':{math6:false,prealgebra7:true,prealgebra:true},
 'systems-elimination':{math6:false,prealgebra7:false,prealgebra:true},
 'scientific-notation':{math6:false,prealgebra7:true,prealgebra:true},
 'pythagorean-theorem':{math6:false,prealgebra7:true,prealgebra:true},
 'slope':{math6:false,prealgebra7:true,prealgebra:true},
 'scatter-plots':{math6:false,prealgebra7:true,prealgebra:true}
};
function plan(entry,courseId,level){
 var levelName={cp2:'remedial',cp1:'standard',honors:'advanced'}[level]||level;
 if(!entry||!entry.curatedGenerator)return {eligible:false,reason:'No verified generator reference'};
 if(!entry.targets.some(function(t){return t&&t.courseId===courseId}))return {eligible:false,reason:'Not a mapped curriculum target'};
 if(!ranges[courseId]||!ranges[courseId][levelName])return {eligible:false,reason:'Unsupported course or level'};
 if(restrictions[entry.key]&&restrictions[entry.key][courseId]===false)return {eligible:false,reason:'Topic not appropriate for this course'};
 var bounds=ranges[courseId][levelName].slice();
 // Existing scatter-plot multiple-choice generator has no items at tier 4+.
 if(entry.key==='scatter-plots'){bounds[1]=Math.min(bounds[1],3);bounds[0]=Math.min(bounds[0],bounds[1]);}
 return {eligible:true,approved:false,publishable:false,source:entry.curatedGenerator,courseId:courseId,level:levelName,tiers:bounds.slice(),intOnly:true,reason:'Candidate only: verify mathematical scope, diagram rendering and generated samples before activation'};
}
root.MK_CROSS_COURSE_DIFFICULTY={version:1,plan:plan};
})(typeof window!=='undefined'?window:globalThis);
