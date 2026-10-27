/* Regression checks for selectable-answer and multipart Algebra 1 banks. */
'use strict';
const assert = require('node:assert/strict');
const load = require('./load.cjs');
const M = load(['games/bank.js']).MKMENU;
let total = 0, multipart = 0;
function numeric(a) {
  a = String(a).trim().replace(/^⟨|⟩$/g, '');
  const m = /^(-?\d+)(?:\/(\d+))?$/.exec(a);
  if (m) return +m[1] / +(m[2] || 1);
  return /^-?\d+\.\d+$/.test(a) ? +a : null;
}
function truth(statement, n) {
  let m;
  if ((m = /answer (?:equals|does not equal) (.+)\.$/.exec(statement))) {
    const v = numeric(m[1]); assert.notEqual(v, null);
    return statement.includes('does not') ? n !== v : n === v;
  }
  if ((m = /answer is (greater than|less than|at least|at most) (-?\d+(?:\.\d+)?)\.$/.exec(statement))) {
    const v = +m[2]; return {'greater than': n > v, 'less than': n < v, 'at least': n >= v, 'at most': n <= v}[m[1]];
  }
  throw Error('Unrecognized statement: ' + statement);
}
for (const unit of Object.keys(M.skillSets).filter(x => x.startsWith('algebra1-'))) {
  let found = 0, countMulti = 0;
  const skills = M.skillSets[unit].skills;
  for (const sk of skills.slice(0, 18)) for (const c of [2, 4, 6]) {
    const p = M.generateProblem(unit, sk.id, c, {intOnly:false,level:'honors'}, 'select-bank-' + c, null);
    if (p.failed) continue;
    const m = M.makeMultiSelect(p);
    if (!m.fail) {
      const q = m.derived || p, n = numeric(q.parts[0].answer);
      assert.notEqual(n, null, unit + ':' + sk.id);
      assert.equal(m.opts.length, 5);
      assert.equal(new Set(m.opts).size, 5);
      assert.ok(m.keys.length >= 2);
      assert.ok(m.keys.length <= 3);
      m.opts.forEach((opt,i) => assert.equal(truth(opt,n), m.keys.includes(i), unit + ':' + sk.id + ': ' + opt));
      found++; total++;
    }
    if (!M.makeMcas(p).fail) countMulti++;
  }
  assert.ok(found > 0, unit + ' has no numeric select-all bank questions');
  console.log(unit + ': select-all ' + found + ', multi-part ' + countMulti);
  if (countMulti) multipart++;
}
assert.ok(total >= 20, 'Need a substantive bank of selectable questions');
console.log('Verified select-all samples: ' + total + '; units with existing multi-part bank: ' + multipart);


/* Regression: ordinary 'Solve ...' items with x=number answers must
   produce actual checkbox choices, not a printed format error. */
for (const answer of ['⟨x=-3⟩', '⟨x=4⟩', '⟨x=\\frac{3}{2}⟩']) {
  const p={prompt:'Solve ⟨2x+6=0⟩.',parts:[{answer}],verify:{status:'verified'}};
  const m=M.makeMultiSelect(p);
  assert.ok(!m.fail,'select-all needs choices for '+answer+': '+m.fail);
  assert.equal(m.opts.length,5);
  assert.ok(m.keys.length>=2 && m.keys.length<=3);
  assert.equal(new Set(m.opts).size,5);
}
console.log('Verified select-all scalar solution regression cases.');
