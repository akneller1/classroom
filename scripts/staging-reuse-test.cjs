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
console.log('PASS stage-only samples and scope restrictions');
