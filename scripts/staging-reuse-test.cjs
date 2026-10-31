/* Verifies staging scope and no automatic publication. */
'use strict';
const assert=require('node:assert/strict'),fs=require('node:fs'),vm=require('node:vm'),path=require('node:path');
const env=require('../worksheet-generator/menu/tests/load.cjs')(['games/bank.js']);
for(const name of ['course-catalog.js','skill-crosswalk.js','legacy-crosswalk-audit.js','cross-course-difficulty.js','legacy-review-samples.js','staged-legacy-reuse.js'])
 vm.runInContext(fs.readFileSync(path.join(__dirname,'..',name),'utf8'),env,{filename:name});
const entries=env.MK_LEGACY_CROSSWALK_AUDIT.inspect(env.MK_SKILL_CROSSWALK,env.MKMENU);
const grant={eligibleForStaging:true,productionEnabled:false,scope:{courseId:'prealgebra7',topic:'evaluating-expressions',level:'cp1'}};
const output=env.MK_STAGED_REUSE.create(grant,entries,'prealgebra7','cp1','evaluating-expressions');
assert.equal(output.ready,true);
assert.ok(output.questions.length>0);
assert.ok(output.questions.every(q=>q.approved===false&&q.publishable===false));
assert.equal(env.MK_STAGED_REUSE.create(grant,entries,'prealgebra7','honors','evaluating-expressions').ready,false);
assert.equal(env.MK_STAGED_REUSE.create({...grant,productionEnabled:true},entries,'prealgebra7','cp1','evaluating-expressions').ready,false);
const authorize=require('./authorize-staging.cjs').authorize;
const crypto=require('node:crypto');
const fakeReview={schemaVersion:1,type:'legacy-question-review',approved:false,courseId:'prealgebra7',topic:'evaluating-expressions',level:'cp1',results:Array.from({length:6},(_,i)=>({sourceId:'q'+i,reviewKey:'evaluating-expressions|prealgebra7|standard|'+(i<3?2:3)+'|q'+i,tier:i<3?2:3,review:{status:'appropriate',note:'Reviewed grade scope'}}))};
const allow={schemaVersion:1,productionEnabled:false,entries:[{courseId:'prealgebra7',topic:'evaluating-expressions',level:'cp1',stagingEnabled:true,productionEnabled:false,reviewRequired:true,sourceSetId:'algebra1-expressions-equations',sourceSkillId:'evaluate',reviewDigest:crypto.createHash('sha256').update(JSON.stringify(fakeReview)).digest('hex')}]};
const settings={reviewer:'Curriculum Reviewer',confirmed:true};
assert.equal(authorize(fakeReview,settings,allow).stagingAuthorized,true);
assert.equal(authorize({...fakeReview,results:fakeReview.results.slice(0,5)},settings,allow).stagingAuthorized,false);
assert.equal(authorize(fakeReview,settings,{...allow,entries:[{...allow.entries[0],reviewDigest:'0'.repeat(64)}]}).stagingAuthorized,false);
assert.equal(authorize(fakeReview,settings,{...allow,entries:[{...allow.entries[0],sourceSkillId:''}]}).stagingAuthorized,false);
assert.equal(authorize(fakeReview,settings,{...allow,entries:[allow.entries[0],allow.entries[0]]}).stagingAuthorized,false);
console.log('PASS stage-only samples, source binding, unique scope and production restrictions');
