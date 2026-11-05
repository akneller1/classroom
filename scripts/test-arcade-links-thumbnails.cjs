#!/usr/bin/env node
'use strict';
const assert=require('node:assert/strict'),fs=require('node:fs'),vm=require('node:vm');
const data=fs.readFileSync('data.js','utf8');
const loader=fs.readFileSync('unit-specific-arcade.js','utf8');
const app=fs.readFileSync('app.js','utf8');
const context={window:{}};vm.runInNewContext(data+'\n'+loader,context);
const names=['rocket','inequality','laser','catapult','mirror','cannon','portal','equation-launch','lava-bridge','system-lasers','function-gates','tangent-cannon'];
assert.equal(names.length,12);
for(const name of names){
 const path='artifacts/math-arcade/index.html?game='+name;
 const matches=context.window.LIBRARY.courses.flatMap(c=>c.units.flatMap(u=>(u.artifacts||[]).filter(a=>a.path===path).map(a=>({c,u,a}))));
 assert.equal(matches.length,1,name+' must belong to exactly one unit');
 const a=matches[0].a;
 assert.match(a.thumb,new RegExp('^thumbs/arcade-'+name+'\\.svg$'));
 assert.ok(fs.existsSync(a.thumb),name+' thumbnail missing');
 assert.ok(fs.readFileSync(a.thumb,'utf8').includes('<svg'),name+' invalid thumbnail');
}
assert.ok(app.includes('math-arcade\\/index\\.html\\?game='),'Homepage should link directly to arcade modes');
assert.ok(app.includes("return a.thumb || ''"),'Arcade cards must prioritize game-specific thumbnails');
const viewer=fs.readFileSync('activity.html','utf8');
assert.ok(viewer.includes('unit-specific-arcade.js'),'Activity viewer should recognize game registrations');
console.log('PASS all twelve arcade cards, unique thumbnails and valid direct launch routing');
