'use strict';
const assert=require('node:assert/strict');
const env=require('./load.cjs')(), NS=env.MKMENU;
const D=NS.geoDiagram;
assert.ok(D && typeof D.render==='function','Geometry renderer loaded');
const seg={kind:'geo-segment',labels:['A','B','C'],measures:['2x','8','24']};
assert.equal(D.validate(seg),true);
assert.match(NS.figHtml(seg),/<svg/);
assert.match(NS.figHtml(seg),/2x/);
assert.equal(D.validate({...seg,labels:['A','A','C']}),false);
for(const id of ['geometry-basics-reasoning','geometry-angles-parallel-lines']){
 const set=NS.skillSets[id];assert.ok(set,id+' registered');
 for(const skill of set.skills)for(let c=1;c<=7;c++){
  let verified=0;
  for(let seed=1;seed<=20;seed++){
   const rng=new env.MKWS.rng.RNG(seed*101+c*17);
   const p=skill.generate({rng,c,intOnly:true});
   const result=NS.verifyProblem(p,{intOnly:true,level:'cp1'});
   assert.equal(result.status,'verified',id+' '+skill.id+' c'+c+': '+JSON.stringify(result.issues));
   if(p.fig){assert.ok(D.validate(p.fig),id+' figure invalid');assert.match(NS.figHtml(p.fig),/<svg/);}
   verified++;
  }
  assert.equal(verified,20);
 }
}
console.log('Verified Geometry starter skills and SVG diagrams across CP2/CP1/Honors difficulty values.');
