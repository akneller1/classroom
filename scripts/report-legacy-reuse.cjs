#!/usr/bin/env node
/* Inventories actual legacy generators alongside curriculum crosswalk candidates. No publication. */
'use strict';
const fs=require('node:fs'),path=require('node:path'),vm=require('node:vm');
const root=path.resolve(__dirname,'..');
const load=require('../worksheet-generator/menu/tests/load.cjs');
const env=load();
for(const file of ['course-catalog.js','skill-crosswalk.js','legacy-crosswalk-audit.js'])vm.runInContext(fs.readFileSync(path.join(root,file),'utf8'),env,{filename:file});
const audit=env.MK_LEGACY_CROSSWALK_AUDIT.inspect(env.MK_SKILL_CROSSWALK,env.MKMENU);
const sets=env.MKMENU.skillSets;
const inventory=Object.keys(sets).map(id=>({setId:id,skills:(sets[id].skills||[]).map(s=>({id:s.id,name:s.name,hasGenerator:typeof s.generate==='function'}))}));
const result={generatedAt:null,summary:{curriculumMappings:audit.length,exactGeneratorCandidates:audit.filter(x=>x.legacyCandidates.length>0).length,curatedGeneratorReferences:audit.filter(x=>x.curatedGenerator).length,registeredSets:inventory.length,registeredGeneratorSkills:inventory.reduce((n,s)=>n+s.skills.filter(k=>k.hasGenerator).length,0),activatedMappings:0},audit:audit,inventory:inventory};
if(process.argv.includes('--json'))console.log(JSON.stringify(result,null,2));
else{
 console.log('Legacy banks: '+result.summary.registeredSets+' sets, '+result.summary.registeredGeneratorSkills+' registered generators.');
 console.log('Curriculum overlaps: '+audit.length+'; exact-name generator matches: '+result.summary.exactGeneratorCandidates+', curated generator IDs: '+result.summary.curatedGeneratorReferences+'. None activated.');
 audit.forEach(e=>console.log(e.key.padEnd(27)+' '+(e.curatedGenerator?e.curatedGenerator.setId+'/'+e.curatedGenerator.skillId:e.legacyCandidates.length?e.legacyCandidates.map(x=>x.setId+'/'+x.skillId).join(', '):'needs explicit skill-ID review')));
}
