/* Configure the original Algebra/Geometry game engine using an existing mapped skill. */
(function(root){'use strict';
var p=new URLSearchParams(root.location.search);
var course=p.get('course'),topic=p.get('topic'),game=p.get('game')||'tic-tac-toe';
var validCourses={math6:'Grade 6 Math',prealgebra7:'Grade 7 Pre-Algebra',prealgebra:'Grade 8 Pre-Algebra'};
var validGames={'tic-tac-toe':true,'connect-four':true,'picture-reveal':true,flashcards:true,showdown:true};
var entries=root.MK_LEGACY_CROSSWALK_AUDIT.inspect(root.MK_SKILL_CROSSWALK,root.MKMENU);
var entry=entries.find(function(x){return x.key===topic&&x.targets.some(function(t){return t&&t.courseId===course})});
var source=entry&&entry.curatedGenerator;
var plan=entry&&root.MK_CROSS_COURSE_DIFFICULTY.plan(entry,course,'cp1');
if(!validCourses[course]||!validGames[game]||!source||!plan||!plan.eligible){
 root.document.getElementById('app').textContent='This topic does not currently have a supported game.';
 root.document.body.setAttribute('data-unit','unavailable');
 return;
}
var set=root.MKMENU.skillSets[source.setId],skill=set&&set.byId[source.skillId];
if(!skill){root.document.getElementById('app').textContent='Question generator unavailable.';return;}
// Keep legacy game labels, but use course-specific curriculum tiers.
var levels={cp2:'cp2',cp1:'cp1',honors:'honors'};
var tierPlans={};
Object.keys(levels).forEach(function(level){
 var policy=root.MK_CROSS_COURSE_DIFFICULTY.plan(entry,course,level);
 if(policy&&policy.eligible) {
  var tiers=[];
  for(var c=policy.tiers[0];c<=policy.tiers[1];c++)tiers.push(c);
  tierPlans[level]=tiers;
 }
});
if(!tierPlans.cp1||!tierPlans.cp1.length){
 root.document.getElementById('app').textContent='No standard-level questions are available for this topic.';
 return;
}
root.MK_GRADE_GAME_TIERS=tierPlans;
// Limit retry attempts in middle-school games to curriculum-approved tiers.
// This wrapper is installed only on the middle-school game page; Algebra 1
// and Geometry use the original shared game bank unchanged.
var originalMakeItems=root.MKGAMES.makeItems;
var allowedTiers=Object.keys(tierPlans).reduce(function(all,level){return all.concat(tierPlans[level]);},[]);
root.MKGAMES.makeItems=function(setId,skillId,c,policy,seed,used){
 if(allowedTiers.indexOf(c)<0)return [];
 return originalMakeItems(setId,skillId,c,policy,seed,used);
};
Object.keys(tierPlans).forEach(function(level){
 if(root.MKGAMES.LEVELS[level])root.MKGAMES.LEVELS[level].tiers=tierPlans[level].slice();
});
root.document.body.setAttribute('data-unit',source.setId);
root.document.body.setAttribute('data-skills',source.skillId);
root.document.body.setAttribute('data-game',game);
root.document.body.setAttribute('data-title',validCourses[course]+' · '+skill.name);
root.document.title=validCourses[course]+' · '+skill.name+' · '+game;
})(window);
