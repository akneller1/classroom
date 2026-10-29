/* Independent re-derivation of the Honors Angles and Parallel Lines investigations from their printed text.
   Run: node worksheet-generator/menu/tests/geometry-angles-rigor-tests.cjs */
'use strict';
const assert = require('node:assert');
const M = require('./load.cjs')().MKMENU;
const SET = 'geometry-angles-parallel-lines';
const plain = s => String(s).replace(/<[^>]+>/g, '').replace(/[⟨⟩]/g, '').replace(/−/g, '-');
const num = s => { const m = /=\s*(-?\d+(?:\.\d+)?)/.exec(plain(s)); return m ? Number(m[1]) : NaN; };
function ev(expr, vars) { const js = expr.replace(/−/g, '-').replace(/(\d)([a-z])/g, '$1*$2').replace(/\)\(/g, ')*('); return Function(...Object.keys(vars), 'return (' + js + ')')(...Object.values(vars)); }
function solve(lhs, rhs, v) { const f = t => ev(lhs, { [v]: t }) - ev(rhs, { [v]: t }), f0 = f(0), k = f(1) - f0; assert(k !== 0, 'degenerate ' + lhs + '=' + rhs); const x = -f0 / k; assert(Number.isInteger(x) && x > 0, 'bad solution ' + x + ' for ' + lhs + '=' + rhs); return x; }
let n = 0;
function run(id, fn, count) {
  for (let c = 1; c <= 7; c++) for (let i = 0; i < count; i++) {
    const p = M.generateProblem(SET, 'angles-investigation-' + id, c, { intOnly: true, level: 'honors' }, 'ang:' + id + ':' + c + ':' + i, null);
    assert(!p.failed, id + ' failed: ' + p.reason); assert.strictEqual(p.parts.length, 4);
    fn(p); n++;
  }
}
const pm = (txt, key) => { const m = new RegExp('marked ⟨\\(([^⟩]+)\\)⟩°').exec(txt); return m && m[1]; };
const marked = txt => (txt.match(/⟨\(([^⟩]+)\)⟩°/g) || []).map(s => /⟨\(([^⟩]+)\)⟩/.exec(s)[1]);
run('corresponding', p => {
  assert(p.fig && p.fig.kind === 'geo-transversal' && M.geoFigures.check(p.fig).ok, 'figure present and honest');
  const [eA, eB] = marked(p.parts[0].prompt), eC = marked(p.parts[1].prompt)[0], eD = marked(p.parts[2].prompt)[0];
  const x = solve(eA, eB, 'x'), phi = ev(eA, { x }); assert.strictEqual(ev(eB, { x }), phi);
  const y = solve('(' + eC + ')+' + phi, '180', 'y'), z = solve(eD, String(phi), 'z');
  assert(phi > 0 && phi < 180 && phi !== 90);
  [x, y, z, 180 - phi].forEach((w, i) => assert.strictEqual(num(p.parts[i].answer), w, 'corresponding part ' + i));
  const degs = p.fig.marks.map(m => m.deg), pos = p.fig.marks.map(m => m.pos);
  assert.strictEqual(JSON.stringify(pos), JSON.stringify([2, 6, 1, 7, 4]));
  assert.strictEqual(JSON.stringify(degs), JSON.stringify([phi, phi, 180 - phi, phi, 180 - phi]));
}, 60);
run('alternate', p => {
  assert(p.fig && M.geoFigures.check(p.fig).ok, 'figure present and honest');
  const [eA, eB] = marked(p.parts[0].prompt), eC = marked(p.parts[1].prompt)[0], eD = marked(p.parts[2].prompt)[0];
  const x = solve(eA, eB, 'x'), phi = ev(eA, { x }); assert.strictEqual(ev(eB, { x }), phi);
  const y = solve('(' + eC + ')+' + phi, '180', 'y'), oth = ev(eC, { y });
  assert.strictEqual(oth, 180 - phi); const z = solve(eD, String(oth), 'z');
  [x, y, z, phi].forEach((w, i) => assert.strictEqual(num(p.parts[i].answer), w, 'alternate part ' + i));
  assert.strictEqual(JSON.stringify(p.fig.marks.map(m => m.pos)), "[3,6,5,8,2]");
}, 60);
run('relations', p => {
  const m = /Angle 1 measures ⟨\(([^⟩]+)\)⟩ degrees and angle 2 measures ⟨\(([^⟩]+)\)⟩ degrees\. Angle 3 is supplementary to angle 1 and measures ⟨\(([^⟩]+)\)⟩ degrees\. Angle 4 is vertical to angle 3 and measures ⟨\(([^⟩]+)\)⟩ degrees/.exec(p.prompt); assert(m);
  const x = solve('(' + m[1] + ')+(' + m[2] + ')', '90', 'x'), a1 = ev(m[1], { x }), a2 = ev(m[2], { x });
  assert(a1 > 0 && a2 > 0 && a1 + a2 === 90);
  const y = solve('(' + m[3] + ')+' + a1, '180', 'y'), a3 = ev(m[3], { y }), z = solve(m[4], String(a3), 'z');
  [x, y, z, a3 - a2].forEach((w, i) => assert.strictEqual(num(p.parts[i].answer), w, 'relations part ' + i));
}, 60);
console.log('Angles investigations: ' + n + ' problems re-derived from their printed text; every key, figure and relation agrees.');
