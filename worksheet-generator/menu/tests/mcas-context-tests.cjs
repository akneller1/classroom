/* Verify each original Algebra 1 context has 3 correct, independently
   checked parts, and rejects deliberately corrupted answers. */
'use strict';
const assert=require('node:assert/strict'),load=require('./load.cjs');
const env=load(),M=env.MKMENU;
const units=Object.keys(M.contextScenes);
assert.equal(units.length,12,'A scenario family for every Algebra 1 unit');
let sampled=0;
for(const unit of units)for(const level of ['cp2','cp1','honors'])for(let i=0;i<12;i++){
  const c={cp2:2,cp1:4,honors:6}[level];
  const p=M.generateProblem(unit,'mcas-context',c,{intOnly:true,level},'context-'+level+'-'+i,null);
  assert.ok(!p.failed,unit+': '+(p.reason||'generation failed'));
  assert.equal(p.parts.length,3,unit+' has three linked parts');
  let v=M.verifyProblem(p,{intOnly:true,level});
  assert.ok(v.ok,unit+' failed verification: '+v.issues.join('; '));
  p.parts.forEach((part,j)=>{
    const original=part.answer;part.answer=String(Number(original)+1);
    const bad=M.verifyProblem(p,{intOnly:true,level});
    assert.ok(!bad.ok,unit+' part '+j+' accepts incorrect answer');
    part.answer=original;
  });
  sampled++;
}
console.log('Verified '+sampled+' original MCAS scenario instances and '+sampled*3+' incorrect-answer mutations across 12 units.');


/* Explicitly force the second family; random sampling alone might miss it. */
let alternatives=0;
for(const unit of units)for(const c of [2,4,6]){
  const original=env.MKWS.rng.make('extension-'+unit+'-'+c),rng={
    next:()=>original.next(),pick:a=>original.pick(a),
    int:(function(){let first=true;return function(lo,hi){
      if(first){first=false;return 1;}return original.int(lo,hi);
    };})()
  };
  const p=M.makeContextProblem(unit,{rng,c,intOnly:true,level:'cp1'});
  assert.match(p.variant,/-extension$/);
  const verdict=M.verifyProblem(p,{intOnly:true,level:'cp1'});
  assert.ok(verdict.ok,unit+' extension verifier: '+verdict.issues.join('; '));
  p.parts.forEach(part=>{
    const before=part.answer;part.answer=String(Number(before)+1);
    assert.ok(!M.verifyProblem(p,{intOnly:true,level:'cp1'}).ok,unit+' extension incorrect answer');
    part.answer=before;
  });
  alternatives++;
}
console.log('Verified '+alternatives+' explicit second-family samples with wrong-answer rejection.');
