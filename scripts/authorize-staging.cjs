#!/usr/bin/env node
/* Repository-side staging authorization. No browser input can activate production.
   A review is evidence only; the approved scope must also be declared in a
   checked-in allowlist reviewed through the normal repository process. */
'use strict';
const fs=require('node:fs'),path=require('node:path'),crypto=require('node:crypto');
const {assess}=require('./assess-legacy-authorization.cjs');
const VALID_COURSES=new Set(['math6','prealgebra7','prealgebra']);
const VALID_LEVELS=new Set(['cp2','cp1','honors']);
function authorize(review,settings,allowlist){
 const assessment=assess(review,{reviewer:settings?.reviewer,confirmed:settings?.confirmed===true});
 const issues=[...assessment.issues];
 const scope=assessment.scope;
 if(!VALID_COURSES.has(scope.courseId)||!VALID_LEVELS.has(scope.level))issues.push('Unsupported curriculum scope');
 const matching=(allowlist?.entries||[]).filter(e=>e.courseId===scope.courseId&&e.topic===scope.topic&&e.level===scope.level);
 if(matching.length!==1)issues.push('Expected one unique staging scope');
 const item=matching[0];
 if(item&&(!item.sourceSetId||!item.sourceSkillId))issues.push('Missing explicit generator reference');
 if(item){const digest=crypto.createHash('sha256').update(JSON.stringify(review)).digest('hex');if(item.reviewDigest!==digest)issues.push('Staging review digest mismatch');}
 if(item){
  try {
   const root=path.resolve(__dirname,'..');
   const vm=require('node:vm');
   const env=require('../worksheet-generator/menu/tests/load.cjs')();
   for(const name of ['course-catalog.js','skill-crosswalk.js','legacy-crosswalk-audit.js'])vm.runInContext(fs.readFileSync(path.join(root,name),'utf8'),env,{filename:name});
   const current=env.MK_LEGACY_CROSSWALK_AUDIT.inspect(env.MK_SKILL_CROSSWALK,env.MKMENU).find(e=>e.key===scope.topic);
   if(!current||!current.curatedGenerator||current.curatedGenerator.setId!==item.sourceSetId||current.curatedGenerator.skillId!==item.sourceSkillId)issues.push('Allowlist generator does not match actual curated source');
  }catch(error){issues.push('Unable to verify generator registration');}
 }
 if(!item||item.stagingEnabled!==true)issues.push('No repository staging allowlist entry');
 if(allowlist?.productionEnabled!==false)issues.push('Production must remain disabled');
 if(item&&(item.productionEnabled!==false||item.reviewRequired!==true))issues.push('Invalid staging allowlist flags');
 return {stagingAuthorized:issues.length===0,productionEnabled:false,scope,issues};
}
if(require.main===module){
 const [reviewFile,settingsFile,allowlistFile]=process.argv.slice(2);
 if(!reviewFile||!settingsFile||!allowlistFile){console.error('Usage: node scripts/authorize-staging.cjs review.json reviewer-confirmation.json staging-allowlist.json');process.exit(2)}
 const read=file=>JSON.parse(fs.readFileSync(path.resolve(file),'utf8'));
 const result=authorize(read(reviewFile),read(settingsFile),read(allowlistFile));
 console.log(JSON.stringify(result,null,2));if(!result.stagingAuthorized)process.exitCode=1;
}
module.exports={authorize};
