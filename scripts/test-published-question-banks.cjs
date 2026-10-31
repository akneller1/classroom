#!/usr/bin/env node
'use strict';
// Verify every published bank is structurally valid and every referenced image exists.
const fs=require('node:fs'),path=require('node:path'),cp=require('node:child_process'),assert=require('node:assert/strict');
const root=path.resolve(__dirname,'..');
const manifest=JSON.parse(fs.readFileSync(path.join(root,'question-banks/manifest.json'),'utf8'));
assert.equal(manifest.version,1);assert.ok(Array.isArray(manifest.banks));
let total=0;const seen=new Set();
for(const entry of manifest.banks){
 assert.equal(entry.approved,true,'Manifest should only list explicitly approved banks');
 assert.match(entry.path,/^question-banks\/[a-z0-9/_-]+\.json$/);
 assert.equal(entry.path,'question-banks/'+entry.courseId+'/'+entry.unitId+'.json');
 const file=path.join(root,entry.path);
 assert.ok(fs.existsSync(file),'Missing bank: '+entry.path);
 const bank=JSON.parse(fs.readFileSync(file,'utf8'));
 assert.equal(bank.courseId,entry.courseId);assert.equal(bank.unitId,entry.unitId);
 const run=cp.spawnSync(process.execPath,[path.join(root,'scripts/check-question-bank.cjs'),file],{encoding:'utf8'});
 assert.equal(run.status,0,'Structural validation failed: '+entry.path+'\n'+run.stdout+'\n'+run.stderr);
 for(const q of bank.questions){
  assert.ok(!seen.has(q.id),'Duplicate question ID across banks: '+q.id);seen.add(q.id);
  if(q.diagram&&q.diagram.type==='image'){
   const src=q.diagram.spec&&q.diagram.spec.src;
   assert.match(src||'',/^question-banks\/assets\/[a-zA-Z0-9_/-]+\.(png|jpg|jpeg|webp)$/);
   assert.ok(!src.includes('..'));assert.ok(fs.existsSync(path.join(root,src)),'Missing image '+src+' for '+q.id);
  }
  total++;
 }
}
console.log('PASS '+manifest.banks.length+' approved banks; '+total+' unique questions; all local diagrams present. Math review not verified.');
