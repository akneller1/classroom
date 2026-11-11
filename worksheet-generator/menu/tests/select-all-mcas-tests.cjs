/* Select-all must be genuine solution-set membership, never one-value trivia. */
'use strict';
const assert=require('node:assert/strict');
const env=require('./load.cjs')(['games/bank.js']);
const M=env.MKMENU, C=M.check;
let tested=0, propertyTested=0;
for(const unit of Object.keys(M.skillSets).filter(k=>k.startsWith('algebra1-'))) {
  assert.equal(M.multiUnitSupported(unit),unit==='algebra1-inequalities'||unit==='algebra1-foundations');
  for(const sk of M.skillSets[unit].skills.slice(0,25)) {
    for(const c of [2,4,6]) {
      const p=M.generateProblem(unit,sk.id,c,{intOnly:c<6,level:'cp1'},'multi-validation-'+c,null);
      if(p.failed)continue;
      const out=M.makeMultiSelect(p);
      if(unit!=='algebra1-inequalities' && !out.fail && p.parts[0].check.type!=='property-name') assert.equal(p.parts[0].check.type,'ineq','Only inequality or property-naming skills may produce choices');
      if(out.fail)continue;
      if(p.parts[0].check.type==='property-name'){   // choose-all from equations: every option's property re-derived by the verifier
        const P=M.propertyCheck, d=out.derived, target=P.of(p.parts[0].check.eq);
        assert.equal(out.opts.length,5); assert.ok(out.keys.length>=2&&out.keys.length<=3,'two or three true options');
        out.opts.forEach((o,i)=>assert.equal(P.of(o.slice(1,-1))===target,out.keys.includes(i),'wrong property option '+o));
        assert.ok(d&&M.verifyProblem(d,{intOnly:false}).ok,'derived choose-all question verifies');
        propertyTested++; continue;
      }
      const chk=p.parts[0].check;
      assert.equal(chk.type,'ineq');
      const cond=C.parseCondition(chk.ineq);
      assert.equal(out.opts.length,5);
      assert.equal(new Set(out.opts).size,5);
      assert.ok(out.keys.length>=2,'At least two solutions required');
      assert.ok(out.keys.length<5,'At least one non-solution required');
      out.opts.forEach((v,i)=>{
        const match=/^⟨[a-zA-Z]+=(-?\d+)⟩$/.exec(v);
        assert.ok(match,'Expected math-formatted equality, got '+v);
        const value=Number(match[1]);
        assert.equal(C.truth(cond,chk.v||'x',new C.Q(value)),out.keys.includes(i),'Wrong inequality choice '+v);
      });
      tested++;
    }
  }
}
assert.ok(tested>0,'No inequality choose-all problems available');
const p={prompt:'Solve ⟨2x=8⟩.',parts:[{answer:'⟨x=4⟩'}],verify:{status:'verified'}};
assert.ok(M.makeMultiSelect(p).fail,'Single-solution equation must be rejected');
assert.ok(propertyTested>0,'No property choose-all problems available');
console.log('Validated '+tested+' multiple-solution inequality items and '+propertyTested+' property choose-all items; all single-answer equations rejected.');
