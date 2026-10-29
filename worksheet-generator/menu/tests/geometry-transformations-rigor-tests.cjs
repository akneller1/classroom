/* Independent re-derivation of the Honors Transformations investigations from their printed text.
   Run: node worksheet-generator/menu/tests/geometry-transformations-rigor-tests.cjs */
'use strict';
const assert = require('node:assert');
const M = require('./load.cjs')().MKMENU;
const SET = 'geometry-transformations';
const plain = s => String(s).replace(/<[^>]+>/g, '').replace(/[⟨⟩]/g, '').replace(/−/g, '-');
const num = s => { const m = /=\s*(-?\d+)/.exec(plain(s)); return m ? Number(m[1]) : NaN; };
const pts = t => [...plain(t).matchAll(/\((-?\d+), (-?\d+)\)/g)].map(m => [Number(m[1]), Number(m[2])]);
let n = 0;
function run(id, fn) {
  for (let c = 1; c <= 7; c++) for (let i = 0; i < 60; i++) {
    const p = M.generateProblem(SET, 'transformations-investigation-' + id, c, { intOnly: true, level: 'honors' }, 'tr:' + id + ':' + c + ':' + i, null);
    assert(!p.failed, id + ' failed: ' + p.reason); assert.strictEqual(p.parts.length, 4);
    const key = p.parts.map(q => num(q.answer)); fn(p, key, plain(p.prompt), p.parts.map(q => plain(q.prompt))); n++;
  }
}
run('mirror', (p, k, t, q) => {
  const [P, P2] = pts(t), m = (P[0] + P2[0]) / 2; assert.strictEqual(P[1], P2[1]); assert.strictEqual(k[0], m);
  const Q = pts(q[1])[0]; assert.strictEqual(k[1], 2 * m - Q[0]);
  const sh = /translated (\d+) units (right|left) and (\d+) units (up|down)/.exec(q[2]); const dx = (sh[2] === 'right' ? 1 : -1) * Number(sh[1]);
  assert.strictEqual(k[2], k[1] + dx);
  assert.strictEqual(k[3], 2 * Math.abs(m - P[0]));
  assert(p.fig && p.fig.kind === 'geo-grid' && p.fig.shapes[0].pts[0][0] === P[0] && p.fig.shapes[0].pts[0][1] === P[1], 'figure shows P');
});
run('center', (p, k, t, q) => {
  const [C, P] = pts(t), a2 = Number(/whose x-coordinate is (-?\d+)/.exec(t)[1]);
  assert.strictEqual(k[0] * (P[0] - C[0]), a2 - C[0]);
  const qx = Number(/x-coordinate (-?\d+)\./.exec(q[1])[1]); assert.strictEqual(k[1], C[0] + k[0] * (qx - C[0]));
  assert.strictEqual(k[2], k[0] * Number(/length (\d+) units/.exec(q[2])[1]));
  assert.strictEqual(k[3], k[0] * k[0] * Number(/area (\d+) square/.exec(q[3])[1]));
});
run('backward', (p, k, t, q) => {
  const [A, A2] = pts(t); assert.strictEqual(k[0], A2[0] + A[1]); assert.strictEqual(k[1], A2[1] - A[0]);
  const B = pts(q[2])[0]; assert.strictEqual(k[2], -B[1] + k[0]);
  const gx = Number(/ends with x-coordinate (-?\d+)/.exec(q[3])[1]); assert.strictEqual(-k[3] + k[0], gx);
});
run('symmetry', (p, k, t, q) => {
  const d = Number(/by (\d+)°/.exec(t)[1]); assert.strictEqual(k[0] * d, 360);
  assert.strictEqual(k[1], (k[0] - 2) * 180); assert.strictEqual(k[2] * k[0], k[1]);
  assert.strictEqual(k[3], k[0] * Number(/is (\d+) units long/.exec(q[3])[1]));
});
console.log('Transformations investigations: ' + n + ' problems re-derived from their printed text; every key and figure agrees.');
