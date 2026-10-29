/* Independent re-derivation of the Honors Right Triangle investigations from their printed text,
   plus a tamper test: a wrong answer in any part must be rejected by the verifier.
   Run: node worksheet-generator/menu/tests/geometry-righttriangle-rigor-tests.cjs */
'use strict';
const assert = require('node:assert');
const M = require('./load.cjs')().MKMENU;
const SET = 'geometry-right-triangles-trigonometry';
const plain = s => String(s).replace(/<[^>]+>/g, '').replace(/[⟨⟩]/g, '').replace(/−/g, '-');
const num = s => { const m = /=\s*(-?\d+(?:\.\d+)?)/.exec(plain(s)); return m ? Number(m[1]) : NaN; };
function ev(expr, vars) { const js = expr.replace(/−/g, '-').replace(/(\d)([a-z])/g, '$1*$2').replace(/\)\(/g, ')*('); return Function(...Object.keys(vars), 'return (' + js + ')')(...Object.values(vars)); }
function solve(lhs, rhs, v) { const f = t => ev(lhs, { [v]: t }) - ev(rhs, { [v]: t }), f0 = f(0), k = f(1) - f0; assert(k !== 0); const x = -f0 / k; assert(Number.isInteger(x) && x > 0, 'bad solution ' + x + ' for ' + lhs + '=' + rhs); return x; }
const isq = n => { const r = Math.round(Math.sqrt(n)); assert(r * r === n, n + ' is not a perfect square'); return r; };
let n = 0, tampered = 0;
function run(id, fn, count) {
  for (let c = 1; c <= 7; c++) for (let i = 0; i < count; i++) {
    const p = M.generateProblem(SET, 'right-investigation-' + id, c, { intOnly: true, level: 'honors' }, 'rt:' + id + ':' + c + ':' + i, null);
    assert(!p.failed, id + ' failed: ' + p.reason); assert.strictEqual(p.parts.length, 4);
    fn(p); n++;
    if (i < 3) for (let k = 0; k < 4; k++) {   // tamper: change one key by 1
      const q = JSON.parse(JSON.stringify(p)), a = q.parts[k].answer, v = num(a); q.parts[k].answer = a.replace(String(v), String(v + 1));
      const r = M.verifyProblem(q, { intOnly: true, level: 'honors' }); assert.notStrictEqual(r.status, 'verified', id + ' part ' + k + ' accepted a wrong answer'); tampered++;
    }
  }
}
run('pyth', p => {
  const m = /AB = (\d+) and BC = (\d+)\. .*DE = (\d+) and EF = ⟨([^⟩]+)⟩/.exec(p.prompt); assert(m);
  const a = +m[1], b = +m[2], mm = +m[3], H = isq(a * a + b * b), v = isq(H * H - mm * mm), x = solve(m[4], String(v), 'x');
  assert(a !== mm && b !== mm || a * a + b * b === mm * mm + v * v, 'both triangles have hypotenuse ' + H);
  [H, v, x, mm * v / 2].forEach((w, i) => assert.strictEqual(num(p.parts[i].answer), w, 'pyth part ' + i));
  assert(M.geoFigures.check(p.fig).ok);
}, 40);
run('special', p => {
  const m = /BC = ⟨([^⟩]+)⟩ and the hypotenuse AB = ⟨([^⟩]+)⟩/.exec(p.prompt); assert(m);
  const x = solve(m[2], '2*(' + m[1] + ')', 'x'), s = ev(m[1], { x }), h = ev(m[2], { x });
  assert.strictEqual(h, 2 * s);
  [x, s, h, h * h - s * s].forEach((w, i) => assert.strictEqual(num(p.parts[i].answer), w, 'special part ' + i));
  assert(M.geoFigures.check(p.fig).ok);
}, 40);
run('converse', p => {
  const m = /PQ = (\d+), QR = (\d+), and PR = ⟨([^⟩]+)⟩/.exec(p.prompt); assert(m);
  const a = +m[1], b = +m[2], h = isq(a * a + b * b), x = solve(m[3], String(h), 'x');
  [a * a + b * b, h, x, a + b + h].forEach((w, i) => assert.strictEqual(num(p.parts[i].answer), w, 'converse part ' + i));
  assert(M.geoFigures.check(p.fig).ok);
}, 40);
run('coordinate', p => {
  const m = /A\((-?\d+), (-?\d+)\), B\((-?\d+), (-?\d+)\), and C\((-?\d+), (-?\d+)\)/.exec(plain(p.prompt)); assert(m);
  const [ax, ay, bx, by, cx, cy] = m.slice(1).map(Number);
  assert(ay === by && bx === cx, 'right angle at B'); const s = bx - ax, t = cy - by, h = isq(s * s + t * t); assert(h % 2 === 0);
  [s, t, h, h / 2].forEach((w, i) => assert.strictEqual(num(p.parts[i].answer), w, 'coordinate part ' + i));
}, 40);
console.log('Right triangle investigations: ' + n + ' problems re-derived from their printed text; ' + tampered + ' tampered answers rejected.');
