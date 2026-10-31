#!/usr/bin/env node
'use strict';
const fs=require('node:fs'),vm=require('node:vm'),assert=require('node:assert/strict');
const html=fs.readFileSync('artifacts/slope-links-mini-golf/index.html','utf8');
const match=html.match(/<script>\s*\/\/ ===== Game core([\s\S]*?)<\/script>/);
assert(match,'Golf game logic found');
const code='// ===== Game core'+match[1];
new vm.Script(code,{filename:'slope-links-mini-golf'});
const core=code.slice(0,code.indexOf('const MAX_STROKES'));
const ctx={module:{exports:{}},Math,console};
vm.runInNewContext(core,ctx);
const {HOLES,simulate}=ctx.module.exports;
assert.equal(HOLES.length,9,'Nine-hole course');
for(const h of HOLES){
 assert.equal(h.ball.length,2);assert.equal(h.cup.length,2);
 assert.ok(h.clubs.length>=4);
 for(const m of [-2,-0.5,0,0.5,2]){
  for(const d of [-1,1]){
   const shot=simulate(h,h.ball,m,d,4,0);
   assert.ok(['stop','sink','water'].includes(shot.outcome),h.name);
   assert.ok(shot.path.length>0);
   assert.ok(shot.end.every(Number.isFinite),h.name);
  }
 }
}
assert.match(html,/data-mode="challenge"/);
assert.match(html,/id="power"/);
assert.match(html,/Championship complete/);
assert.match(html,/id="results"/);
console.log('Nine-hole golf gameplay logic and UI smoke tests passed');
