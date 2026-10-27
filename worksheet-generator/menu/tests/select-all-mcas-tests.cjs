/* Select-all must be genuine solution-set membership, never one-value trivia. */
'use strict';
const assert=require('node:assert/strict');
const env=require('./load.cjs')(['games/bank.js']);
const M=env.MKMENU, C=M.check;
let tested=0;
for(const unit of Object.keys(M.skillSets).filter(k=>k.startsWith('algebra1-'))) {
  assert.equal(M.multiUnitSupported(unit),unit==='algebra1-inequalities');
  for(const sk of M.skillSets[unit].skills.slice(0,25)) {
    for(const c of [2,4,6]) {
      const p=M.generateProblem(unit,sk.id,c,{intOnly:c<6,level:'cp1'},'multi-validation-'+c,null);
      if(p.failed)continue;
      const out=M.makeMultiSelect(p);
      if(unit!=='algebra1-inequalities' && !out.fail) assert.equal(p.parts[0].check.type,'ineq','Only inequality skill may produce choices');
      if(out.fail)continue;
      const chk=p.parts[0].check;
      assert.equal(chk.type,'ineq');
      const cond=C.parseCondition(chk.ineq);
      assert.equal(out.opts.length,5);
      assert.equal(new Set(out.opts).size,5);
      assert.ok(out.keys.length>=2,'At least two solutions required');
      assert.ok(out.keys.length<5,'At least one non-solution required');
      out.opts.forEach((v,i)=>{
        const value=Number(v.split(' = ')[1]);
        assert.equal(C.truth(cond,chk.v||'x',new C.Q(value)),out.keys.includes(i),'Wrong inequality choice '+v);
      });
      tested++;
    }
  }
}
assert.ok(tested>0,'No inequality choose-all problems available');
const p={prompt:'Solve ⟨2x=8⟩.',parts:[{answer:'⟨x=4⟩'}],verify:{status:'verified'}};
assert.ok(M.makeMultiSelect(p).fail,'Single-solution equation must be rejected');
console.log('Validated '+tested+' multiple-solution inequality items; all single-answer equations rejected.');
