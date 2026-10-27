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
assert.equal(JSON.stringify(Array.from(catalog.units,x=>x[1].replace(/^Unit \d+ · /,''))),JSON.stringify(names),'Generator unit names/order drift');
const supported=catalog.units.filter(([id])=>!!menu.skillSets[id]);
const unsupported=catalog.units.filter(([id])=>!menu.skillSets[id]);
assert.equal(supported.length,2,'Only the two verified starter Geometry question banks may be enabled');
assert.equal(unsupported.length,8,'The other eight Geometry units must stay disabled until verified banks exist');
assert.ok(!catalog.units.some(x=>x[0]==='geometry-coordinate-geometry-transformations'),
  'Legacy coordinate-geometry bank must not be passed off as standalone Transformations');
console.log('Geometry curriculum aligned: '+catalog.units.length+' units, '+supported.length+' with verified banks, '+unsupported.length+' explicitly unsupported.');
