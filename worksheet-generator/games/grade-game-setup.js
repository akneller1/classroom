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
root.document.body.setAttribute('data-unit',source.setId);
root.document.body.setAttribute('data-skills',source.skillId);
root.document.body.setAttribute('data-game',game);
root.document.body.setAttribute('data-title',validCourses[course]+' · '+skill.name);
root.document.title=validCourses[course]+' · '+skill.name+' · '+game;
})(window);
