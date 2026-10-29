/* Independent re-derivation of the Honors Circles investigations from their printed text.
   Run: node worksheet-generator/menu/tests/geometry-circles-rigor-tests.cjs */
'use strict';
const assert = require('node:assert');
const M = require('./load.cjs')().MKMENU;
const plain = s => String(s).replace(/<[^>]+>/g, '').replace(/[⟨⟩]/g, '').replace(/−/g, '-');
const num = s => { const m = /=\s*(-?\d+)/.exec(plain(s)); return m ? Number(m[1]) : NaN; };
let n = 0;
function run(id, fn) {
  for (let c = 1; c <= 7; c++) for (let i = 0; i < 60; i++) {
    const p = M.generateProblem('geometry-circles', 'circles-investigation-' + id, c, { intOnly: true, level: 'honors' }, 'ci:' + id + ':' + c + ':' + i, null);
    assert(!p.failed, id + ' failed: ' + p.reason); assert.strictEqual(p.parts.length, 4);
    fn(p, p.parts.map(q => num(q.answer)), plain(p.prompt), p.parts.map(q => plain(q.prompt))); n++;
  }
}
run('angles', (p, k, t, q) => {
  const [, a, m, b] = /\(x \+ (\d+)\)° and intercepts an arc measuring \((\d)x - (\d+)\)°/.exec(t).map(Number);
  assert.strictEqual(2 * (k[0] + a), m * k[0] - b); assert.strictEqual(k[1], m * k[0] - b); assert.strictEqual(k[2], 360 - k[1]); assert.strictEqual(2 * k[3], k[1]);
  assert(p.fig && p.fig.kind === 'geo-circle', 'figure present');
});
run('power', (p, k, t, q) => {
  const [, a, kk, b, c2] = /PA = (\d+), PB = \(x \+ (\d+)\), PC = (\d+), and PD = (\d+)/.exec(q[0]).map(Number);
  assert.strictEqual(a * (k[0] + kk), b * c2); assert.strictEqual(k[1], a + k[0] + kk);
  const e = Number(/external segment of (\d+)\. Find the internal/.exec(q[2])[1]), f = Number(/external segment of (\d+)\. Using/.exec(q[3])[1]);
  assert.strictEqual(e * (k[2] + e), k[1] * k[1]); assert.strictEqual(f * k[3], k[1] * k[1]);
  assert(p.fig && p.fig.kind === 'geo-circle', 'figure present');
});
run('coordinate', (p, k, t, q) => {
  const m = /X² ([+-]) (\d+)X \+ Y² ([+-]) (\d+)Y ([+-]) (\d+) = 0/.exec(t), s = (g, v) => (g === '-' ? -1 : 1) * Number(v);
  const lx = s(m[1], m[2]), ly = s(m[3], m[4]), cs = s(m[5], m[6]);
  assert.strictEqual(k[0], -lx / 2); assert.strictEqual(k[1], -ly / 2);
  assert.strictEqual(k[2] * k[2], k[0] * k[0] + k[1] * k[1] - cs); assert(k[2] > 0); assert.strictEqual(k[3], k[2] * k[2]);
});
run('sector', (p, k, t, q) => {
  const [, rad, aa, b] = /radius (\d+) cm has a central angle of \((\d)x \+ (\d+)\)°/.exec(t).map(Number);
  const kk = Number(/so (\d+) times the angle/.exec(q[0])[1]);
  assert.strictEqual(kk * (aa * k[0] + b), 360); assert.strictEqual(k[1], aa * k[0] + b);
  assert.strictEqual(360 * k[2], 2 * rad * k[1]); assert.strictEqual(360 * k[3], rad * rad * k[1]);
  assert(p.fig && p.fig.kind === 'geo-circle', 'figure present');
});
console.log('Circles investigations: ' + n + ' problems re-derived from their printed text; every key and figure agrees.');
