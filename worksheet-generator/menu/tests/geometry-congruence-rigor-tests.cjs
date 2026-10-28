/* Independent re-derivation of the Triangle Congruence multi-step investigations.
   Each problem is re-solved from its PRINTED text (never from generator variables) and compared with every part's key.
   Run: node worksheet-generator/menu/tests/geometry-congruence-rigor-tests.cjs */
'use strict';
const assert = require('node:assert');
const M = require('./load.cjs')().MKMENU;
const SET = 'geometry-triangles-congruence';
const plain = s => String(s).replace(/<[^>]+>/g, '');
const num = s => { const m = /=\s*(-?\d+(?:\.\d+)?)/.exec(plain(s).replace(/[⟨⟩]/g, '').replace(/−/g, '-')); return m ? Number(m[1]) : NaN; };
// evaluate an expression like "3x-7" or "(4y-2)" at a variable value
function ev(expr, vars) {
  const js = expr.replace(/−/g, '-').replace(/(\d)([a-z])/g, '$1*$2').replace(/\)\(/g, ')*(');
  return Function(...Object.keys(vars), 'return (' + js + ')')(...Object.values(vars));
}
// solve a linear equation lhs=rhs in variable v by evaluating at two points
function solve(lhs, rhs, v) {
  const f = t => ev(lhs, { [v]: t }) - ev(rhs, { [v]: t }), f0 = f(0), f1 = f(1), k = f1 - f0;
  assert(k !== 0, 'degenerate equation ' + lhs + '=' + rhs);
  const x = -f0 / k; assert(Number.isInteger(x) && x > 0, 'non-integer or non-positive solution for ' + lhs + '=' + rhs + ': ' + x); return x;
}
const snips = t => (t.match(/⟨[^⟩]*⟩/g) || []).map(s => s.slice(1, -1));
let n = 0;
function run(id, fn, count) {
  for (let c = 3; c <= 7; c++) for (let i = 0; i < count; i++) {
    const p = M.generateProblem(SET, id, c, { intOnly: true, level: 'honors' }, 'rigor:' + id + ':' + c + ':' + i, null);
    assert(!p.failed, id + ' failed to generate: ' + p.reason);
    assert.strictEqual(p.parts.length, 4, 'four parts');
    fn(p); n++;
  }
}
/* 1 algebra chain */
run('congruence-investigation-algebra', p => {
  const t = plain(p.prompt), S = snips(p.prompt);
  const mAB = /AB = ⟨([^⟩]+)⟩ and DE = ⟨([^⟩]+)⟩/.exec(p.prompt), mBC = /BC = ⟨([^⟩]+)⟩ and EF = (\d+)/.exec(p.prompt), mAC = /AC = ⟨([^⟩]+)⟩/.exec(p.prompt);
  const mC = /angle C is ⟨\(([^⟩]+)\)⟩ degrees and the measure of angle F is ⟨\(([^⟩]+)\)⟩/.exec(p.prompt);
  assert(mAB && mBC && mAC && mC, 'printed givens not found');
  const x = solve(mAB[1], mAB[2], 'x');
  const y = solve(mBC[1].replace(/x/g, '(' + x + ')'), mBC[2], 'y');
  const ab = ev(mAB[1], { x }), bc = Number(mBC[2]), ac = ev(mAC[1], { x, y });
  const z = solve(mC[1], mC[2], 'z');
  assert(ab > 0 && bc > 0 && ac > 0, 'sides must be positive');
  assert(ac + ab > bc && ab + bc > ac && ac + bc > ab, 'triangle inequality');
  const want = [x, y, ab + bc + ac, z];
  want.forEach((w, i) => assert.strictEqual(num(p.parts[i].answer), w, 'algebra part ' + i + ' key ' + p.parts[i].answer + ' vs ' + w + '\n' + t));
  assert(ev(mC[1], { z }) > 0 && ev(mC[1], { z }) < 180, 'angle range');
}, 120);
/* 2 isosceles + median */
run('congruence-investigation-isosceles', p => {
  const m = /Angle BAD measures ⟨\(([^⟩]+)\)⟩ degrees and angle CAD measures (\d+) degrees/.exec(p.prompt);
  assert(m, 'givens');
  const x = solve(m[1], m[2], 'x'), half = Number(m[2]), vertex = 2 * half, base = (180 - vertex) / 2;
  assert(vertex < 180 && Number.isInteger(base) && base > 0);
  [x, vertex, base, 90].forEach((w, i) => assert.strictEqual(num(p.parts[i].answer), w, 'isosceles part ' + i));
  assert.strictEqual(p.fig.kind, 'geo-cong'); assert(M.geoFigures.check(p.fig).ok, 'figure honest');
}, 120);
/* 3 coordinate */
run('congruence-investigation-coordinate', p => {
  const m = /A\((-?\d+), (-?\d+)\), B\((-?\d+), (-?\d+)\), and C\((-?\d+), (-?\d+)\)\. Triangle DEF has vertices D\((-?\d+), (-?\d+)\), E\((-?\d+), (-?\d+)\), and F\(x, (-?\d+)\) with x less than (-?\d+)/.exec(plain(p.prompt).replace(/[⟨⟩]/g, ''));
  assert(m, 'vertices');
  const [ax, ay, bx, by, cx, cy, dx, dy, ex, ey, fy, lim] = m.slice(1).map(Number);
  const dist = (a, b) => Math.hypot(a[0] - b[0], a[1] - b[1]);
  const A = [ax, ay], B = [bx, by], C = [cx, cy], D = [dx, dy], E = [ex, ey];
  assert(ay === by && bx === cx && dx === ex && ey === fy && lim === ex, 'axis-aligned construction');
  const AB = dist(A, B), BC = dist(B, C), AC2 = Math.round(dist(A, C) ** 2), DE = dist(D, E);
  assert.strictEqual(DE, AB, 'DE must equal AB');
  const fx = ex - BC; assert(fx < lim);
  const F = [fx, fy];
  assert(Math.abs(dist(E, F) - BC) < 1e-9 && Math.abs(dist(D, F) - dist(A, C)) < 1e-9, 'SSS holds for the key F');
  assert(AB !== BC, 'legs differ so the correspondence matters');
  [AB, BC, AC2, fx].forEach((w, i) => assert.strictEqual(num(p.parts[i].answer), w, 'coordinate part ' + i + ' key ' + p.parts[i].answer));
}, 150);
/* 4 overlapping triangles */
run('congruence-investigation-overlap', p => {
  const m = /AB = ⟨([^⟩]+)⟩ and CD = ⟨([^⟩]+)⟩\. Angle ABD measures ⟨\(([^⟩]+)\)⟩ degrees and angle CDB measures (\d+) degrees\. Angle ADB measures ⟨\(([^⟩]+)\)⟩ degrees and angle CBD measures (\d+) degrees/.exec(p.prompt);
  assert(m, 'givens');
  const x = solve(m[1], m[2], 'x'), y = solve(m[3], m[4], 'y'), z = solve(m[5], m[6], 'z');
  const n1 = Number(m[4]), n2 = Number(m[6]), angA = 180 - n1 - n2;
  assert(angA > 0 && ev(m[1], { x }) > 0);
  [x, y, z, angA].forEach((w, i) => assert.strictEqual(num(p.parts[i].answer), w, 'overlap part ' + i));
  assert(M.geoFigures.check(p.fig).ok, 'figure honest (angles drawn as printed)');
}, 120);
console.log('Congruence investigations: ' + n + ' problems re-derived from their printed text; every key, figure and side/angle relation agrees.');
