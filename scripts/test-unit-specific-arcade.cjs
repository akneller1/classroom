#!/usr/bin/env node
'use strict';
const assert=require('node:assert/strict'),fs=require('node:fs'),vm=require('node:vm');
const html=fs.readFileSync('artifacts/math-arcade/index.html','utf8');
const script=html.match(/<script>([\s\S]*?)<\/script>/)[1];
new vm.Script(script,{filename:'math-arcade'});
const register=fs.readFileSync('unit-specific-arcade.js','utf8');
const expected=[['algebra','expressions-equations','rocket'],['algebra','inequalities','inequality'],['algebra','systems-of-equations','laser'],['algebra','quadratics','catapult'],['geometry','transformations','mirror'],['geometry','right-triangles-trigonometry','cannon'],['algebra2','functions-transformations','portal']];
for(const [course,unit,game] of expected){assert(register.includes("'"+course+"','"+unit+"','"+game+"'"),'Missing '+game+' registration');assert(html.includes(game+":")||html.includes("'"+game+"'")||html.includes(game+'{'),'Missing '+game+' mode')}
const data=fs.readFileSync('data.js','utf8');for(const [,unit] of expected)assert(data.includes('"id": "'+unit+'"'),'Unknown unit '+unit);
const raw={1:html.split('r2:([')[1]?.split('])')[0]};assert(raw[1],'Catapult rounds present');
const values=raw[1].split(',').map(Number);assert.equal(values.length,10);
for(const r of values){const answers=[0,r,r/2,r*r/4,8*(r-8)];assert.ok(answers.every(Number.isInteger),'All five catapult answers must be integers for quadratic coefficient '+r);}
assert.match(html,/standard form: h\(x\) = −x² \+ /,'Catapult must display expanded standard form');
assert.match(html,/CATAPULT/);assert.match(html,/ENEMY CASTLE/);
const good=values.filter(r=>{const y=8*(r-8);return y>=2&&y<=36});
assert.equal(good.length,6,'Exactly six trajectories should hit the castle');
const misses=values.filter(r=>{const y=8*(r-8);return y<2||y>36});
assert.equal(misses.length,4,'Exactly four shots should miss');
console.log('PASS seven games, unit registrations, 6-hit castle sequence and script syntax');
