'use strict';
const fs=require('fs'),vm=require('vm'),assert=require('node:assert/strict');
const ctx={};vm.runInNewContext(fs.readFileSync('worksheet-generator/core/math-display.js','utf8'),ctx);const fmt=ctx.MK_MATH_DISPLAY;
for(const [source,want] of [['x²/100 + y²/64 = 1','[[x² ; 100]] + [[y² ; 64]] = 1'],['(x+1)/(x-2)','[[(x+1) ; (x-2)]]'],['f(x)/g(x)','[[f(x) ; g(x)]]'],['(x+1)^2/3','[[(x+1)^2 ; 3]]'],['1/2/3','[[[[1 ; 2]] ; 3]]'],['(x − 1)²/9 + (y + 2)²/4 = 1','[[(x − 1)² ; 9]] + [[(y + 2)² ; 4]] = 1'],['x/(x+1)²','[[x ; (x+1)²]]']])assert.equal(fmt.fractions(source),want);
assert.equal(fmt.fractions('10/31/2026'),'10/31/2026');assert.ok(fmt.html('x²/100 + y²/64 = 1').includes('class="fr"'));assert.ok(!fmt.html('1/2').includes('/2'));
assert.ok(!fmt.html('<img onerror="bad"> 1/2').includes('<img'));
const site={};const c={window:site};for(const f of ['data.js','thumbs/resource-previews.js','resource-standards.js'])vm.runInNewContext(fs.readFileSync(f,'utf8'),c);
for(const course of site.LIBRARY.courses)for(const unit of course.units){const games=unit.artifacts.filter(a=>a.originalPath&&/course-(game|activity)/.test(a.path));assert.equal(new Set(games.map(a=>a.bankFormat)).size,games.length,'Duplicate game formats '+unit.id);assert.equal(new Set(games.map(a=>a.thumb)).size,games.length,'Duplicate game thumbnails '+unit.id);for(const a of games){assert.ok(!a.title.includes('Skill Practice'));assert.ok(fs.existsSync(a.thumb),a.thumb);assert.ok(!a.description.includes('shared Algebra 2 question bank'));}}
console.log('PASS safe stacked fractions, preserved expression grouping, all-course names, routes, duplicate removal and distinct thumbnails');
