#!/usr/bin/env node
'use strict';
const assert=require('node:assert/strict'),fs=require('node:fs'),vm=require('node:vm'),path=require('node:path');
const ctx={window:{}},root=path.resolve(__dirname,'..');
for(const file of ['course-catalog.js','skill-crosswalk.js'])vm.runInNewContext(fs.readFileSync(path.join(root,file),'utf8'),ctx,{filename:file});
const cross=ctx.window.MK_SKILL_CROSSWALK;
assert.equal(cross.valid(),true,'Every mapping must resolve to exactly one existing curriculum skill');
const m=cross.matches();assert.equal(m.length,5);
for(const entry of m){assert.equal(entry.status,'candidate');assert.equal(entry.enabled,false);assert.ok(entry.targets.length>=1);}
console.log('PASS '+m.length+' curriculum overlaps, all resolved; none enabled for question generation');
