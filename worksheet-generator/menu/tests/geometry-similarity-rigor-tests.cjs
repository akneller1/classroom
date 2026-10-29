/* Independent re-derivation of the Honors Similarity investigations from their printed text.
   Run: node worksheet-generator/menu/tests/geometry-similarity-rigor-tests.cjs */
'use strict';
const assert = require('node:assert');
const M = require('./load.cjs')().MKMENU;
const SET = 'geometry-similarity';
const plain = s => String(s).replace(/<[^>]+>/g, '').replace(/[⟨⟩]/g, '').replace(/−/g, '-');
const num = s => { const m = /=\s*(-?\d+(?:\.\d+)?)/.exec(plain(s)); return m ? Number(m[1]) : NaN; };
function ev(expr, vars) { const js = expr.replace(/−/g, '-').replace(/(\d)([a-z])/g, '$1*$2').replace(/\)\(/g, ')*('); return Function(...Object.keys(vars), 'return (' + js + ')')(...Object.values(vars)); }
function solve(lhs, rhs, v) { const f = t => ev(lhs, { [v]: t }) - ev(rhs, { [v]: t }), f0 = f(0), k = f(1) - f0; assert(k !== 0, 'degenerate ' + lhs + '=' + rhs); const x = -f0 / k; assert(Number.isInteger(x) && x > 0, 'bad solution ' + x + ' for ' + lhs + '=' + rhs); return x; }
const tri = (a, b, c) => a + b > c && a + c > b && b + c > a;
let n = 0;
function run(id, fn, count) {
  for (let c = 1; c <= 7; c++) for (let i = 0; i < count; i++) {
    const p = M.generateProblem(SET, 'similarity-investigation-' + id, c, { intOnly: true, level: 'honors' }, 'simr:' + id + ':' + c + ':' + i, null);
    assert(!p.failed, id + ' failed: ' + p.reason); assert.strictEqual(p.parts.length, 4);
    fn(p); n++;
  }
}
run('ratio', p => {
  const m = /DE to AB is (\d+) to (\d+)\. AB = ⟨([^⟩]+)⟩ and DE = ⟨([^⟩]+)⟩\. AC = ⟨([^⟩]+)⟩ and DF = ⟨([^⟩]+)⟩\. BC = (\d+)/.exec(p.prompt); assert(m);
  const P = +m[1], Q = +m[2], bc = +m[7];
  const x = solve(Q + '*(' + m[4] + ')', P + '*(' + m[3] + ')', 'x'), y = solve(Q + '*(' + m[6] + ')', P + '*(' + m[5] + ')', 'y');
  const ab = ev(m[3], { x }), de = ev(m[4], { x }), ac = ev(m[5], { y }), df = ev(m[6], { y });
  assert(de * Q === P * ab && df * Q === P * ac, 'ratio holds'); assert(tri(ab, ac, bc), 'real triangle');
  assert((P * bc) % Q === 0, 'EF integral'); const ef = P * bc / Q, per = de + df + ef;
  [x, y, ef, per].forEach((w, i) => assert.strictEqual(num(p.parts[i].answer), w, 'ratio part ' + i));
  assert(M.geoFigures.check(p.fig).ok, 'figure honest');
}, 60);
run('parallel', p => {
  const m = /AD = ⟨([^⟩]+)⟩ and DB = ⟨([^⟩]+)⟩\. AE = (\d+), EC = (\d+), and DE = (\d+)/.exec(p.prompt); assert(m);
  const ae = +m[3], ec = +m[4], de = +m[5], x = solve(ec + '*(' + m[1] + ')', ae + '*(' + m[2] + ')', 'x');
  const ad = ev(m[1], { x }), db = ev(m[2], { x }), ab = ad + db, ac = ae + ec;
  assert(ad * ec === db * ae, 'DE parallel to BC: AD/DB = AE/EC'); assert((de * ab) % ad === 0); const bc = de * ab / ad;
  assert(tri(ab, ac, bc), 'real triangle');
  [x, ab, bc, ab + ac + bc].forEach((w, i) => assert.strictEqual(num(p.parts[i].answer), w, 'parallel part ' + i));
  assert(M.geoFigures.check(p.fig).ok);
}, 60);
run('dilation', p => {
  const m = /A\((-?\d+), (-?\d+)\), B\((-?\d+), (-?\d+)\), and C\((-?\d+), (-?\d+)\)\. It is dilated about the origin by a scale factor of (\d+)/.exec(plain(p.prompt)); assert(m);
  const [ax, ay, bx, by, cx, cy, k] = m.slice(1).map(Number);
  assert(ay === by && bx === cx, 'right angle at B');
  const w = k * Math.abs(bx - ax), area = w * k * Math.abs(cy - by) / 2;
  [k * bx, k * cy, w, area].forEach((v, i) => assert.strictEqual(num(p.parts[i].answer), v, 'dilation part ' + i + ' ' + p.parts[i].answer));
}, 60);
run('altitude', p => {
  const m = /AD = ⟨([^⟩]+)⟩, DB = (\d+), and CD = (\d+)/.exec(p.prompt); assert(m);
  const db = +m[2], cd = +m[3], x = solve(db + '*(' + m[1] + ')', cd + '*' + cd, 'x'), ad = ev(m[1], { x });
  assert.strictEqual(ad * db, cd * cd, 'CD is the geometric mean'); const ab = ad + db;
  [x, ab, ad * ab, ab * cd / 2].forEach((w, i) => assert.strictEqual(num(p.parts[i].answer), w, 'altitude part ' + i));
  assert(M.geoFigures.check(p.fig).ok);
}, 60);
console.log('Similarity investigations: ' + n + ' problems re-derived from their printed text; every key, figure and relation agrees.');
