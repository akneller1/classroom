/* Independent re-derivation of the Honors Area, Surface Area and Volume investigations from their printed text.
   Run: node worksheet-generator/menu/tests/geometry-measure-rigor-tests.cjs */
'use strict';
const assert = require('node:assert');
const M = require('./load.cjs')().MKMENU;
const plain = s => String(s).replace(/<[^>]+>/g, '').replace(/[⟨⟩]/g, '').replace(/−/g, '-');
const num = s => { const m = /=\s*(-?\d+)/.exec(plain(s)); return m ? Number(m[1]) : NaN; };
let n = 0;
function run(id, fn) {
  for (let c = 1; c <= 7; c++) for (let i = 0; i < 60; i++) {
    const p = M.generateProblem('geometry-area-surface-area-volume', 'measure-investigation-' + id, c, { intOnly: true, level: 'honors' }, 'mi:' + id + ':' + c + ':' + i, null);
    assert(!p.failed, id + ' failed: ' + p.reason); assert.strictEqual(p.parts.length, 4);
    fn(p.parts.map(q => num(q.answer)), plain(p.prompt), p.parts.map(q => plain(q.prompt))); n++;
  }
}
const nums = (re, t) => re.exec(t).slice(1).map(Number);
run('prism', (k, t, q) => {
  const [kk, w, h, V] = nums(/length \(x \+ (\d+)\) cm, width (\d+) cm, height (\d+) cm, and volume (\d+) cubic/, t), l = k[0] + kk;
  assert.strictEqual(l * w * h, V); assert.strictEqual(k[1], 2 * (l * w + l * h + w * h));
  const s = Number(/multiplied by (\d+)\. The original/.exec(q[2])[1]); assert.strictEqual(k[2], s ** 3 * V);
  assert.strictEqual(k[3], s * s * k[1]);
});
run('cylinder', (k, t, q) => {
  const [h, V] = nums(/height (\d+) cm and volume (\d+)π/, t); assert.strictEqual(k[0] * k[0] * h, V); assert(k[0] > 0);
  assert.strictEqual(k[1], 2 * k[0] * h); assert.strictEqual(k[2], k[1] + 2 * k[0] * k[0]);
  const h2 = Number(/height of (\d+) cm\. Its volume/.exec(q[3])[1]); assert.strictEqual(3 * k[3], k[0] * k[0] * h2);
});
run('sphere', (k, t, q) => {
  const sa = /surface area (\d+)π square/.exec(t), gc = /circumference (\d+)π/.exec(t), ga = /great circle with area (\d+)π/.exec(t);
  if (sa) assert.strictEqual(4 * k[0] * k[0], Number(sa[1])); else if (gc) assert.strictEqual(2 * k[0], Number(gc[1])); else assert.strictEqual(k[0] * k[0], Number(ga[1]));
  assert(k[0] > 0); assert.strictEqual(3 * k[1], 4 * (3 * k[0]) ** 3); assert.strictEqual(k[2], 3 * k[0] * k[0]); assert.strictEqual(k[3], 2 * k[0] ** 3);
});
run('trapezoid', (k, t, q) => {
  const [kk, b2, h, A] = nums(/sides \(x \+ (\d+)\) cm and (\d+) cm, a height of (\d+) cm, and an area of (\d+) square/, t), L = k[0] + kk;
  assert.strictEqual(h * (L + b2), 2 * A); assert.strictEqual(2 * k[1], L * h); assert.strictEqual(k[2], A - k[1]);
  const s = Number(/multiplied by (\d+)\. Use y/.exec(q[3])[1]); assert.strictEqual(k[3], s * s * k[1]);
});
console.log('Area/Surface Area/Volume investigations: ' + n + ' problems re-derived from their printed text; every key agrees.');
