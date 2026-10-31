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
const raw=html.match(/r2:\\(\\[([0-9,]+)\\]\\)\\[i\\]/);assert(raw,'Catapult rounds present');
const values=raw[1].split(',').map(Number);assert.equal(values.length,10);
const good=values.filter(r=>{const y=8*(r-8);return y>=2&&y<=18});
assert.equal(good.length,6,'Exactly six trajectories should hit the castle');
const misses=values.filter(r=>{const y=8*(r-8);return y<2||y>18});
assert.equal(misses.length,4,'Exactly four shots should miss');
console.log('PASS seven games, unit registrations, 6-hit castle sequence and script syntax');
