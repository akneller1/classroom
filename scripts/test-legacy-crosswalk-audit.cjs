#!/usr/bin/env node
'use strict';
const fs=require('node:fs'),vm=require('node:vm'),path=require('node:path'),assert=require('node:assert/strict');
const context={window:{}};
for(const file of ['course-catalog.js','skill-crosswalk.js','legacy-crosswalk-audit.js'])vm.runInNewContext(fs.readFileSync(path.join(__dirname,'..',file),'utf8'),context,{filename:file});
const cross=context.window.MK_SKILL_CROSSWALK,audit=context.window.MK_LEGACY_CROSSWALK_AUDIT;
assert.equal(cross.valid(),true);
const source=cross.matches()[0].source;
const legacy={skillSets:{example:{skills:[{id:'real-existing-id',name:source.name,generate:function(){}},{id:'not-a-generator',name:source.name}]}}};
const result=audit.inspect(cross,legacy);
assert.equal(result.length,15);
assert.equal(result[0].legacyCandidates.length,1);
assert.equal(result[0].legacyCandidates[0].skillId,'real-existing-id');
assert.equal(result[0].ready,false,'Never automatically approve merely because generator exists');
assert.equal(result[1].legacyCandidates.length,0);
assert.equal(audit.inspect(cross,null).filter(x=>x.ready).length,0);
console.log('PASS 15 cross-course legacy audits, exact-name candidate detection, no auto-approval');
