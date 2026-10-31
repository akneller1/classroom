/* Read-only inspection of actual legacy game generators for curriculum crosswalk.
 * A mapped topic does not imply a verified or reusable generator.
 */
(function(root){
'use strict';
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
  return {key:entry.key,source:source,targets:entry.targets,legacyCandidates:matching,
    ready:false,reason:matching.length?'Generator candidate found; grade bounds and math verification pending':'No exact-name generator match; manual skill ID mapping needed'};
 });
}
root.MK_LEGACY_CROSSWALK_AUDIT={version:1,inspect:inspect};
})(typeof window!=='undefined'?window:globalThis);
