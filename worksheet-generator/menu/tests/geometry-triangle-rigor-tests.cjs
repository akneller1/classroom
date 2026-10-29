/* Independent re-derivation of the Honors Triangle Relationships investigations from their printed text.
   Run: node worksheet-generator/menu/tests/geometry-triangle-rigor-tests.cjs */
'use strict';
const assert = require('node:assert');
const M = require('./load.cjs')().MKMENU;
const SET = 'geometry-triangle-relationships';
const plain = s => String(s).replace(/<[^>]+>/g, '').replace(/[⟨⟩]/g, '').replace(/−/g, '-');
const num = s => { const m = /=\s*(-?\d+(?:\.\d+)?)/.exec(plain(s)); return m ? Number(m[1]) : NaN; };
function ev(expr, vars) { const js = expr.replace(/−/g, '-').replace(/(\d)([a-z])/g, '$1*$2').replace(/\)\(/g, ')*('); return Function(...Object.keys(vars), 'return (' + js + ')')(...Object.values(vars)); }
function solve(lhs, rhs, v) { const f = t => ev(lhs, { [v]: t }) - ev(rhs, { [v]: t }), f0 = f(0), k = f(1) - f0; assert(k !== 0, 'degenerate ' + lhs + '=' + rhs); const x = -f0 / k; assert(Number.isInteger(x) && x > 0, 'bad solution ' + x + ' for ' + lhs + '=' + rhs); return x; }
let n = 0;
function run(id, fn, count) {
  for (let c = 1; c <= 7; c++) for (let i = 0; i < count; i++) {
    const p = M.generateProblem(SET, 'triangle-investigation-' + id, c, { intOnly: true, level: 'honors' }, 'trig:' + id + ':' + c + ':' + i, null);
    assert(!p.failed, id + ' failed: ' + p.reason); assert.strictEqual(p.parts.length, 4);
    fn(p, p.prompt.replace(/⟨([^⟩]*)⟩/g, '⟨$1⟩')); n++;
  }
}
const tri = (a, b, c) => a + b > c && a + c > b && b + c > a;
run('midsegment', p => {
  const m = /DE = ⟨([^⟩]+)⟩ and BC = ⟨([^⟩]+)⟩\. AD = ⟨([^⟩]+)⟩ and DB = ⟨([^⟩]+)⟩\. AC = (\d+)\./.exec(p.prompt); assert(m);
  const x = solve(m[2], '2*(' + m[1] + ')', 'x'), y = solve(m[3], m[4], 'y');
  const de = ev(m[1], { x }), bc = ev(m[2], { x }), ad = ev(m[3], { y }), ac = Number(m[5]);
  assert(de > 0 && bc === 2 * de && ad === ev(m[4], { y }) && ac % 2 === 0 && tri(2 * ad, bc, ac), 'real triangle');
  const per = 2 * ad + bc + ac;
  [x, y, per, per / 2].forEach((w, i) => assert.strictEqual(num(p.parts[i].answer), w, 'midsegment part ' + i));
  assert(M.geoFigures.check(p.fig).ok);
}, 80);
run('exterior', p => {
  const m = /angle ACD measures ⟨\(([^⟩]+)\)⟩ degrees, angle B measures ⟨\(([^⟩]+)\)⟩ degrees, and angle A measures (\d+) degrees/.exec(p.prompt); assert(m);
  const m2 = /PQ = PR = ⟨([^⟩]+)⟩ cm and QR = ⟨([^⟩]+)⟩ cm\. Its perimeter is (\d+) cm/.exec(p.parts[3].prompt); assert(m2);
  const A = Number(m[3]), x = solve(m[1], A + '+(' + m[2] + ')', 'x'), B = ev(m[2], { x }), ext = ev(m[1], { x });
  assert.strictEqual(A + 2 * B, 180, 'isosceles angle sum'); assert.strictEqual(ext, 180 - B, 'exterior = supplement');
  const y = solve('2*(' + m2[1] + ')+(' + m2[2] + ')', m2[3], 'y'), leg = ev(m2[1], { y }), base = ev(m2[2], { y });
  assert(tri(leg, leg, base), 'second triangle is real');
  [x, B, B, y].forEach((w, i) => assert.strictEqual(num(p.parts[i].answer), w, 'exterior part ' + i));
  assert(M.geoFigures.check(p.fig).ok, 'figure honest');
}, 80);
run('coordinate', p => {
  const m = /A\((-?\d+), (-?\d+)\), B\((-?\d+), (-?\d+)\), and C\((-?\d+), (-?\d+)\)/.exec(plain(p.prompt)); assert(m);
  const [ax, ay, bx, by, cx, cy] = m.slice(1).map(Number);
  assert(by === cy && ax === (bx + cx) / 2, 'AM vertical');
  const mx = (bx + cx) / 2, my = (by + cy) / 2, L = Math.abs(ay - my), gy = my + L / 3;
  assert(Number.isInteger(gy) && L > 0 && bx !== cx);
  [mx, my, L, gy].forEach((w, i) => assert.strictEqual(num(p.parts[i].answer), w, 'coordinate part ' + i + ' ' + p.parts[i].answer));
}, 60);
run('bisector', p => {
  const m = /PA = ⟨([^⟩]+)⟩ and PB = ⟨([^⟩]+)⟩\. AM = ⟨([^⟩]+)⟩ and MB = ⟨([^⟩]+)⟩/.exec(p.prompt); assert(m);
  const x = solve(m[1], m[2], 'x'), y = solve(m[3], m[4], 'y'), pa = ev(m[1], { x }), am = ev(m[3], { y });
  assert(pa > am, 'hypotenuse PA must exceed leg AM'); assert(pa === ev(m[2], { x }) && am === ev(m[4], { y }));
  [x, pa, y, 2 * pa + 2 * am].forEach((w, i) => assert.strictEqual(num(p.parts[i].answer), w, 'bisector part ' + i));
  assert(M.geoFigures.check(p.fig).ok);
}, 80);
console.log('Triangle relationship investigations: ' + n + ' problems re-derived from their printed text; every key, figure and relation agrees.');
