#!/usr/bin/env node
'use strict';
const assert=require('node:assert/strict'),fs=require('node:fs'),vm=require('node:vm'),path=require('node:path');
const env={window:{}};vm.createContext(env);
for(const f of ['course-catalog.js','skill-crosswalk.js','legacy-crosswalk-audit.js','cross-course-difficulty.js'])vm.runInContext(fs.readFileSync(path.resolve(__dirname,'..',f),'utf8'),env,{filename:f});
const x=env.window.MK_SKILL_CROSSWALK.matches(),policy=env.window.MK_CROSS_COURSE_DIFFICULTY;
const fake={skillSets:{}};
for(const e of x){if(e.key==='evaluating-expressions')fake.skillSets['algebra1-expressions-equations']={skills:[{id:'evaluate',name:'Evaluate expressions',generate(){}}]};}
const entries=env.window.MK_LEGACY_CROSSWALK_AUDIT.inspect(env.window.MK_SKILL_CROSSWALK,fake);
const selected=entries.find(e=>e.key==='evaluating-expressions');
assert.equal(policy.plan(selected,'math6','cp2').eligible,true);
assert.equal(policy.plan(selected,'math6','cp2').approved,false);
assert.equal(policy.plan(selected,'math6','cp2').publishable,false);
assert.deepEqual(Array.from(policy.plan(selected,'math6','cp2').tiers),[1,1]);
assert.deepEqual(Array.from(policy.plan(selected,'prealgebra7','honors').tiers),[3,4]);
assert.equal(policy.plan(selected,'algebra','cp1').eligible,false);
assert.equal(policy.plan(selected,'math6','random').eligible,false);
const missing=entries.find(e=>e.key==='systems-elimination');
assert.equal(policy.plan(missing,'prealgebra','cp2').eligible,false);
const scatter=entries.find(e=>e.key==='scatter-plots');
// Curated reference is required; no approval implied by these bounds.
assert.equal(policy.plan(scatter,'prealgebra','honors').eligible,false);
console.log('PASS middle-school tier constraints, candidate gating and unsupported targets');
