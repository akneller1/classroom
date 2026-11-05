#!/usr/bin/env node
'use strict';
const assert=require('node:assert/strict'),fs=require('node:fs'),vm=require('node:vm');
const data=fs.readFileSync('data.js','utf8');
const loader=fs.readFileSync('unit-specific-arcade.js','utf8');
const context={window:{}};vm.runInNewContext(data+'\n'+loader,context);
const activities=context.window.LIBRARY.courses.flatMap(c=>c.units.flatMap(u=>u.artifacts||[]));
const visible=activities.filter(a=>a.unitSpecific===true);
assert.deepEqual(Array.from(visible,a=>a.title).sort(),['Slope Links Mini Golf','Zombie Fence']);
assert.ok(!activities.some(a=>a.path.startsWith('artifacts/math-arcade/index.html?game=')));
for(const a of visible){
 assert.ok(fs.existsSync(a.path),a.title+' game missing');
 assert.ok(fs.existsSync(a.thumb),a.title+' thumbnail missing');
}
console.log('PASS only Mini Golf and Zombie Fence appear in the unit-specific game catalog');
