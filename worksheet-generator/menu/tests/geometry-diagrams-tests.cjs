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
for(const id of ['geometry-basics-reasoning','geometry-angles-parallel-lines','geometry-triangle-relationships']){
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

// Regression: assessment pools must never starve figure-backed Geometry skills.
// The previous FNV low-bit selector assigned entire skill families to one pool.
for(const id of ['geometry-basics-reasoning','geometry-angles-parallel-lines','geometry-triangle-relationships']) {
 const set=NS.skillSets[id];
 for(const skill of set.skills)for(const pool of ['formal','practice']) {
  for(const c of [3,4,5]) {
   const item=NS.generateProblem(id,skill.id,c,{intOnly:true,level:'cp1',questionPool:pool},'geo-pool-'+id+'-'+skill.id+'-'+c+'-'+pool,{keys:new Set(),sigs:new Set()});
   assert.equal(item.failed,undefined,'Pool starvation: '+id+'/'+skill.id+' '+pool+' c'+c+': '+item.reason);
   assert.equal(item.verify.status,'verified');
  }
 }
}
console.log('Both formal and practice pools supply verified Geometry questions, including SVG figures.');

console.log('Verified Geometry starter skills and SVG diagrams across CP2/CP1/Honors difficulty values.');


// Geometry choose-all must use three independently true equations and two false
// equations; never instruct students to solve an inequality.
for (const id of ['geometry-basics-reasoning','geometry-angles-parallel-lines','geometry-triangle-relationships']) {
  const set=NS.skillSets[id];
  for (const skill of set.skills) {
    const item=NS.generateProblem(id,skill.id,3,{intOnly:true,level:'cp1',questionPool:'formal'},'select-all-geometry-'+skill.id,{keys:new Set(),sigs:new Set()});
    assert.equal(item.failed,undefined,'Could not generate '+skill.id);
    const multi=NS.makeMultiSelect(item);
    assert.equal(multi.fail,undefined,'Could not make select-all for '+skill.id+': '+multi.fail);
    assert.equal(multi.keys.length,3,'Expected three correct Geometry statements');
    assert.equal(multi.opts.length,5,'Expected two distractors');
    assert.match(multi.direction,/Geometry problem/);
    const C=NS.check;
    const variable=item.parts[0].check.v||'x';
    const solved=C.solveLinear(item.parts[0].check.eq,variable);
    for(let k=0;k<multi.opts.length;k++) {
      const rel=C.parseRelation(multi.opts[k].slice(1,-1));
      const vars={};vars[variable]=solved.value;
      const trueStatement=C.evalNode(rel.lhs,vars).eq(C.evalNode(rel.rhs,vars));
      assert.equal(trueStatement,multi.keys.includes(k),'Incorrect Geometry select-all answer key');
    }
  }
}
console.log('Geometry choose-all key verification passed.');


for(const c of [1,3,5,7])for(let seed=1;seed<=25;seed++){
 const skill=NS.skillSets['geometry-basics-reasoning'].byId['coordinate-investigation'];
 const p=skill.generate({rng:new env.MKWS.rng.RNG(seed*103+c),c,intOnly:true});
 assert.equal(p.parts.length,4,'Open Response must have four related parts');
 assert.ok(p.parts.every(part=>part.prompt&&part.check&&part.check.type==='solve'),'Each part must be independently checked');
 assert.equal(NS.verifyProblem(p,{intOnly:true,level:'cp1'}).status,'verified','Coordinate investigation answer verification');
 assert.equal(NS.makeMcas({...p,verify:{status:'verified'}}).fail,undefined,'Four-part format should be supported');
}
console.log('Four-part Geometry coordinate response verified.');
