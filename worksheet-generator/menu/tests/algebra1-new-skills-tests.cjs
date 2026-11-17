/* Algebra 1 audit batch C (2026-11-17): error-analysis skills (#13), standards-gap skills (#10), word problems (#14)
   and the Statistics graphing items (#7). Every problem must verify, and a wrong answer must be caught. */
'use strict';
const assert = require('node:assert/strict');
const fs = require('fs'), vm = require('vm'), path = require('path');
const M = require('./load.cjs')().MKMENU;
const NEW = { 'algebra1-polynomials': ['poly-error'], 'algebra1-exponents-scientific-notation': ['pow-error'], 'algebra1-factoring-zero-product': ['factor-error', 'poly-zeros-graph'],
  'algebra1-systems-of-equations': ['sys-error', 'elim-replace'], 'algebra1-quadratics': ['quad-error', 'quad-maxmin'], 'algebra1-relations-functions': ['func-error', 'inverse-linear'],
  'algebra1-linear-equations-slope': ['graph-solution-set'], 'algebra1-exponential-functions': ['constant-rate'], 'algebra1-statistics-data-modeling': ['twoway-summarize'] };
const wrong = a => /Line \d+/.test(a) ? a.replace(/Line (\d+)/, (m, n) => 'Line ' + (+n === 1 ? 2 : 1))
  : /^(Yes|No)\b/.test(a) ? a.replace(/^(Yes|No)/, m => m === 'Yes' ? 'No' : 'Yes')
  : /Above|Below/.test(a) ? a.replace(/Above the x-axis: (.*) is positive/, 'Below the x-axis: $1 is negative').replace(/Below the x-axis: (.*) is negative/, 'Above the x-axis: $1 is positive')
  : /^Linear/.test(a) ? 'Exponential: it grows by the same factor.' : /=[^⟩]*\d/.test(a) ? a.replace(/=([^⟩\d-]*)(-?\d+)/, (m, pre, d) => '=' + pre + (+d + 1)) : a.replace(/(-?\d+)/, m => String(+m + 1));
let n = 0, caught = 0;
for (const [set, ids] of Object.entries(NEW)) for (const id of ids) for (const lv of ['cp2', 'cp1', 'honors']) for (const c of M.LEVELS[lv].tiers) for (let k = 0; k < 8; k++) {
  const pol = { intOnly: lv !== 'honors', level: lv };
  const p = M.generateProblem(set, id, c, pol, 'new:' + id + lv + c + k, { keys: new Set(), sigs: new Set() });
  assert.ok(!p.failed, set + ' ' + id + ' ' + lv + ' c' + c + ': ' + p.reason);
  assert.ok(M.verifyProblem(p, pol).ok, id + ' does not verify');
  assert.ok(p.steps.length >= 2, id + ' has a one-line solution');
  for (let i = 0; i < p.parts.length; i++) {
    const q = JSON.parse(JSON.stringify(p)), w = wrong(q.parts[i].answer); if (w === q.parts[i].answer) continue;
    q.parts[i].answer = w; q.edited = true; n++;
    if (!M.verifyProblem(q, pol).ok) caught++; else assert.fail(id + ' accepts a wrong answer: ' + w + ' (right: ' + p.parts[i].answer + ')');
  }
}
/* word problems at the top tiers of the Unit 1–2 core skills (#14) */
for (const [set, id, c] of [['algebra1-foundations', 'evaluate', 4], ['algebra1-expressions-equations', 'two-step', 4], ['algebra1-expressions-equations', 'multi-step', 5], ['algebra1-expressions-equations', 'both-sides', 6]]) {
  let ctx = 0; for (let k = 0; k < 40; k++) { const p = M.generateProblem(set, id, c, { intOnly: true, level: 'cp1' }, 'ctx:' + id + k, { keys: new Set(), sigs: new Set() }); assert.ok(!p.failed, p.reason); if (/^ctx/.test(p.variant)) ctx++; }
  assert.ok(ctx >= 6, id + ' has too few word problems: ' + ctx);
}
/* Statistics Graphing Practice items (#7): the key response passes the plot checker */
const w = {}; w.window = w; const cx = vm.createContext({ window: w, globalThis: w, console, Math, Set, Map, Array, Object, JSON, Number, String });
for (const f of ['../../core/plot.js', '../../plot-algebra.js']) vm.runInContext(fs.readFileSync(path.join(__dirname, f), 'utf8'), cx);
let plots = 0;
for (const lv of ['cp2', 'cp1', 'honors']) for (const s of w.MK_A1_PLOT.skills()) for (const q of w.MK_A1_PLOT.pool('statistics-data-modeling', lv, s.id, 8)) {
  const p = q.plot, alt = p.answerKey.alt, g = re => +alt.match(re)[1]; let r;
  if (p.tool === 'points') r = { points: p.target.points };
  else if (p.tool === 'line') { const m = q.prompt.match(/\((\d+), (\d+)\) and \((\d+), (\d+)\)\.$/); r = { points: [[+m[1], +m[2]], [+m[3], +m[4]]] }; }
  else if (p.tool === 'box-plot') r = { min: g(/minimum (-?[\d.]+)/), q1: g(/Q1 (-?[\d.]+)/), median: g(/median (-?[\d.]+)/), q3: g(/Q3 (-?[\d.]+)/), max: g(/maximum (-?[\d.]+)/), outliers: [] };
  else r = { counts: alt.match(/\d+/g).map(Number) };
  assert.ok(w.MK_PLOT.check(p, r).ok, 'Graphing item key fails: ' + q.prompt); plots++;
}
console.log('Algebra 1 new skills: ' + caught + ' of ' + n + ' wrong answers caught; ' + plots + ' graphing items checked.');
