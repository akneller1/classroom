/* Read-only inspection of actual legacy game generators for curriculum crosswalk.
 * A mapped topic does not imply a verified or reusable generator.
 */
(function(root){
'use strict';
var curated={
  "evaluating-expressions": [
    "algebra1-expressions-equations",
    "evaluate"
  ],
  "distributive-property": [
    "algebra1-expressions-equations",
    "distribute"
  ],
  "equations-both-sides": [
    "algebra1-expressions-equations",
    "both-sides"
  ],
  "systems-graphing": [
    "algebra1-systems-of-equations",
    "sys-graph"
  ],
  "systems-substitution": [
    "algebra1-systems-of-equations",
    "sys-subst"
  ],
  "scientific-notation": [
    "algebra1-exponents-scientific-notation",
    "sci-convert"
  ],
  "mean-median-mode": [
    "algebra1-statistics-data-modeling",
    "center"
  ],
  "scatter-plots": [
    "algebra1-statistics-data-modeling",
    "scatter"
  ],
  "pythagorean-theorem": [
    "geometry-right-triangles-trigonometry",
    "right-pythagorean-hypotenuse"
  ],
  "transformations-translations": [
    "geometry-transformations",
    "translate-horizontal"
  ],
  "transformations-rotations": [
    "geometry-transformations",
    "rotate-90-clockwise"
  ],
  "transformations-reflections": [
    "geometry-transformations",
    "reflect-x-axis"
  ],
  "slope": [
    "algebra1-linear-equations-slope",
    "slope"
  ],
  "systems-elimination": [
    "algebra1-systems-of-equations",
    "sys-elim"
  ]
};
function inspect(crosswalk,legacy){
 var entries=crosswalk.matches();
 return entries.map(function(entry){
  var source=entry.source;
  var sets=legacy&&legacy.skillSets||{};
  var matching=[];
  Object.keys(sets).forEach(function(setId){
   var set=sets[setId];
   (set.skills||[]).forEach(function(skill){
    if(!source||!skill||typeof skill.generate!=='function')return;
    var label=String(skill.name||'').trim().toLowerCase();
    if(label===source.name.toLowerCase())matching.push({setId:setId,skillId:skill.id,name:skill.name});
   });
  });
  var explicit=curated[entry.key];
  var selected=null;
  if(explicit){var set=sets[explicit[0]],sk=set&&(set.skills||[]).filter(function(x){return x.id===explicit[1]&&typeof x.generate==='function'})[0];if(sk)selected={setId:explicit[0],skillId:sk.id,name:sk.name};}
  return {key:entry.key,source:source,targets:entry.targets,legacyCandidates:matching,curatedGenerator:selected,
    ready:false,reason:matching.length?'Generator candidate found; grade bounds and math verification pending':'No exact-name generator match; manual skill ID mapping needed'};
 });
}
root.MK_LEGACY_CROSSWALK_AUDIT={version:1,inspect:inspect};
})(typeof window!=='undefined'?window:globalThis);
