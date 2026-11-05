#!/usr/bin/env node
'use strict';
const assert=require('node:assert/strict'),fs=require('node:fs'),vm=require('node:vm');
const html=fs.readFileSync('artifacts/math-arcade/index.html','utf8');
const script=html.match(/<script>([\s\S]*?)<\/script>/)[1];
new vm.Script(script,{filename:'math-arcade'});
const register=fs.readFileSync('unit-specific-arcade.js','utf8');
const expected=[['algebra','expressions-equations','rocket'],['algebra','inequalities','inequality'],['algebra','systems-of-equations','laser'],['algebra','quadratics','catapult'],['geometry','transformations','mirror'],['geometry','right-triangles-trigonometry','cannon'],['algebra2','functions-transformations','portal'],];
// bank games for the newer courses: one per unit, defined in MK_UNIT_GAMES
const ctx={};vm.runInNewContext(register,{window:ctx});const UG=ctx.MK_UNIT_GAMES;
assert.equal(Object.keys(UG).length,44,'44 bank games (every unit of 6th Grade, both Pre-Algebras, Precalculus and Calculus)');
const engines=['rocket','inequality','laser','mirror','cannon','portal'];
for(const [id,g] of Object.entries(UG)){assert(engines.includes(g.engine),id+' engine');assert(fs.existsSync('question-banks/'+g.bank.course+'/'+g.bank.unit+'.json'),id+' bank');assert(g.title&&g.intro&&g.levels.length===3,id+' text');}
assert.equal(new Set(Object.values(UG).map(g=>g.bank.course+'/'+g.bank.unit)).size,44,'one game per unit');
const checkHtml=html.includes('MK_UNIT_GAMES')&&html.includes('unit-specific-arcade.js');assert(checkHtml,'arcade page loads the bank games');
for(const [course,unit,game] of expected){assert(register.includes("'"+course+"','"+unit+"','"+game+"'"),'Missing '+game+' registration');assert(html.includes(game+":")||html.includes("'"+game+"'")||html.includes(game+'{'),'Missing '+game+' mode')}
const data=fs.readFileSync('data.js','utf8');for(const [,unit] of expected)assert(data.includes('"id": "'+unit+'"'),'Unknown unit '+unit);
const source=html.match(/catapult:\s*(\[\[.*?\]\])\.map\(/s);
assert(source,'Catapult root-pair list should exist');
const pairs=JSON.parse(source[1]);
assert.equal(pairs.length,10);
let hits=0,misses=0,nonzero=0;
for(const pair of pairs){
  const [r1,r2]=pair;
  const vertex=(r1+r2)/2;
  const height=-(vertex-r1)*(vertex-r2);
  const castleHeight=-(8-r1)*(8-r2);
  const constant=-r1*r2;
  assert.ok([r1,r2,vertex,height,castleHeight].every(Number.isInteger),'Every catapult answer must be an integer');
  if(constant!==0)nonzero++;
  if(castleHeight>=2&&castleHeight<=36)hits++;else misses++;
}
assert.equal(hits,6,'Six trajectories should hit');
assert.equal(misses,4,'Four trajectories should miss');
assert.ok(nonzero>=5,'Most questions need nonzero constant terms');
assert.match(html,/standard form: h\(x\) = −x²/);
assert.match(html,/ENEMY CASTLE/);
console.log('PASS 51 games (7 original + 44 bank games), unit registrations, 6-hit castle sequence and script syntax');
