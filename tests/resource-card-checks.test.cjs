'use strict';
const {test}=require('node:test'),assert=require('node:assert/strict'),fs=require('node:fs'),os=require('node:os'),path=require('node:path');
const {localTarget,browserSample}=require('../scripts/resource-card-checks.cjs');
test('Fast file checks resolve queries and directory indexes, reject missing files and external resources',()=>{
 const root=fs.mkdtempSync(path.join(os.tmpdir(),'resource-checks-'));
 try{fs.mkdirSync(path.join(root,'unit'));fs.writeFileSync(path.join(root,'unit/index.html'),'ok');
 assert.equal(localTarget(root,'http://localhost/unit/?game=maze#skills','http://localhost/'),path.join(root,'unit/index.html'));
 assert.throws(()=>localTarget(root,'/missing.html','http://localhost/'),/Missing resource/);
 assert.throws(()=>localTarget(root,'https://other.example/a','http://localhost/'),/Off-site/);
 }finally{fs.rmSync(root,{recursive:true,force:true});}
});
test('Routine browser sample covers courses and distinct game engines without scaling with units',()=>{
 const base='http://localhost/',links=[],courses=new Map();
 for(let c=0;c<16;c++)for(let unit=0;unit<12;unit++)for(const game of ['maze','match','quiz']){
 const href=base+'course-game.html?course=c'+c+'&unit='+unit+'&game='+game;links.push(href);courses.set(href,'c'+c);
 }
 const sample=browserSample(links,base,96,courses);
 assert(sample.length<=96);assert(sample.length<links.length/4);
 assert.equal(new Set(sample.map(h=>courses.get(h))).size,16);
 for(const game of ['maze','match','quiz'])assert(sample.some(h=>new URL(h).searchParams.get('game')===game));
 assert.deepEqual(browserSample(links,base,96,courses),sample);
});
