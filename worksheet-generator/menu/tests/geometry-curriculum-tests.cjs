/* Guard against Geometry curriculum drift and accidental skill-bank substitution. */
'use strict';
const assert=require('node:assert/strict');
const fs=require('node:fs');
const vm=require('node:vm');
const env=require('./load.cjs')();
const menu=env.MKMENU;
const ctx={window:{}};vm.createContext(ctx);
vm.runInContext(fs.readFileSync('data.js','utf8'),ctx);
const published=ctx.window.LIBRARY.courses.find(c=>c.id==='geometry');
const catalog=menu.CATALOG.find(c=>c.course==='Geometry');
assert.equal(published.units.length,10,'Published Geometry should have ten units');
assert.equal(catalog.units.length,published.units.length,'Generator must list all published Geometry units');
const names=published.units.map(u=>u.name);
assert.deepEqual(Array.from(catalog.units,x=>x[1].replace(/^Unit \d+ · /,'')),names,'Generator unit names/order drift');
const supported=catalog.units.filter(([id])=>!!menu.skillSets[id]);
const unsupported=catalog.units.filter(([id])=>!menu.skillSets[id]);
assert.equal(supported.length,0,'Do not claim Geometry generator support before independent skill banks are registered');
assert.equal(unsupported.length,10,'All Geometry unit generators remain disabled until verified question banks are implemented');
assert.ok(!catalog.units.some(x=>x[0]==='geometry-coordinate-geometry-transformations'),
  'Legacy coordinate-geometry bank must not be passed off as standalone Transformations');
console.log('Geometry curriculum aligned: '+catalog.units.length+' units, '+supported.length+' with verified banks, '+unsupported.length+' explicitly unsupported.');
