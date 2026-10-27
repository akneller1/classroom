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
  assert.equal(p.parts.length,4,unit+' has three linked parts');
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

/* Force every new applied family, independent of random variant selection. */
let checkedApplied=0;
for (const unit of Object.keys(M.contextApplied)) for (const c of [2,4,6]) {
  const base=env.MKWS.rng.make('applied-'+unit+'-'+c);
  let first=true;
  const rng={next:()=>base.next(),pick:a=>base.pick(a),int:(lo,hi)=>{
    if(first){first=false;return 3;}
    return base.int(lo,hi);
  }};
  const p=M.makeContextProblem(unit,{rng,c,intOnly:true,level:'cp1'});
  assert.match(p.variant,/-applied$/,unit);
  assert.equal(p.parts.length,4);
  const v=M.verifyProblem(p,{intOnly:true,level:'cp1'});
  assert.ok(v.ok,unit+' applied: '+v.issues.join('; ')+' | '+p.prompt);
  for(const pt of p.parts) {
    const original=pt.answer;pt.answer=String(Number(original)+1);
    assert.ok(!M.verifyProblem(p,{intOnly:true,level:'cp1'}).ok,unit+' accepts wrong answer');
    pt.answer=original;
  }
  checkedApplied++;
}
console.log('Verified '+checkedApplied+' applied family samples and '+checkedApplied*3+' wrong answers.');

/* The worksheet preset must never print old labels or invalid Open Response items. */
for (const unit of units) {
  const cfg=M.defaultConfig(unit,'worksheet');
  cfg.seed=12345;cfg.sections=M.worksheetSections('mcas',cfg);
  cfg.sections[0].offered=2;cfg.sections[0].required=2;
  const st=M.newAssessment(cfg);
  assert.equal(st.config.sections[0].name,'Open Response');
  st.versions[0].sections[0].items.forEach((p)=>{
    assert.ok(!p.failed,unit+' failed to generate an Open Response item: '+(p.reason||''));
    assert.ok(p.parts.length>=4,unit+' generated fewer than four parts');
    assert.ok(M.verifyProblem(p,{intOnly:true}).ok,unit+' generated invalid response');
  });
  const saved=JSON.parse(M.serialize(st));
  saved.config.sections[0].name='MCAS Open Response';
  saved.versions[0].sections[0].items[0].parts.pop();
  const restored=M.deserialize(saved);
  assert.equal(restored.config.sections[0].name,'Open Response');
  assert.ok(restored.versions[0].sections[0].items[0].parts.length>=4,unit+' legacy item not repaired');
}
console.log('Verified two-item Open Response preset and legacy migration for all Algebra units.');

/* Exercise every new four-part reasoning scenario with positive and negative key mutations. */
let reasoningChecked=0;
for(const unit of Object.keys(M.contextReasoning)) for(const c of [2,4,6]) {
  const base=env.MKWS.rng.make('reason-'+unit+'-'+c);
  let first=true;
  const rng={next:()=>base.next(),pick:a=>base.pick(a),int:(lo,hi)=>{
    if(first){first=false;return 4;}
    return base.int(lo,hi);
  }};
  const p=M.makeContextProblem(unit,{rng,c,intOnly:true,level:'cp1'});
  assert.match(p.variant,/-reasoning$/);
  assert.equal(p.parts.length,4);
  const result=M.verifyProblem(p,{intOnly:true,level:'cp1'});
  assert.ok(result.ok,unit+' reasoning check: '+result.issues.join('; '));
  for(const part of p.parts) {
    const save=part.answer;part.answer=String(Number(save)+1);
    assert.ok(!M.verifyProblem(p,{intOnly:true,level:'cp1'}).ok,unit+' accepted wrong part');
    part.answer=save;
  }
  reasoningChecked++;
}
console.log('Verified '+reasoningChecked+' four-part reasoning cases and incorrect answers.');
