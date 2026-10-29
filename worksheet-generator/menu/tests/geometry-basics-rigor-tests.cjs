/* Independent re-derivation of the Honors Foundations of Geometry investigations from their printed text.
   Run: node worksheet-generator/menu/tests/geometry-basics-rigor-tests.cjs */
'use strict';
const assert = require('node:assert');
const M = require('./load.cjs')().MKMENU;
const SET = 'geometry-basics-reasoning';
const plain = s => String(s).replace(/<[^>]+>/g, '').replace(/[⟨⟩]/g, '').replace(/−/g, '-');
const num = s => { const m = /=\s*(-?\d+(?:\.\d+)?)/.exec(plain(s)); return m ? Number(m[1]) : NaN; };
function ev(expr, vars) { const js = expr.replace(/−/g, '-').replace(/(\d)([a-z])/g, '$1*$2').replace(/\)\(/g, ')*('); return Function(...Object.keys(vars), 'return (' + js + ')')(...Object.values(vars)); }
function solve(lhs, rhs, v) { const f = t => ev(lhs, { [v]: t }) - ev(rhs, { [v]: t }), f0 = f(0), k = f(1) - f0; assert(k !== 0, 'degenerate ' + lhs + '=' + rhs); const x = -f0 / k; assert(Number.isInteger(x) && x > 0, 'bad solution ' + x + ' for ' + lhs + '=' + rhs); return x; }
let n = 0;
function run(id, fn, count) {
  for (let c = 1; c <= 7; c++) for (let i = 0; i < count; i++) {
    const p = M.generateProblem(SET, 'basics-investigation-' + id, c, { intOnly: true, level: 'honors' }, 'bas:' + id + ':' + c + ':' + i, null);
    assert(!p.failed, id + ' failed: ' + p.reason); assert.strictEqual(p.parts.length, 4);
    fn(p); n++;
  }
}
run('segment', p => {
  const m = /AB = ⟨([^⟩]+)⟩, BC = ⟨([^⟩]+)⟩, and AC = ⟨([^⟩]+)⟩\. AD = (\d+)\./.exec(p.prompt); assert(m);
  const x = solve(m[3], '(' + m[1] + ')+(' + m[2] + ')', 'x'), ab = ev(m[1], { x }), bc = ev(m[2], { x }), ac = ev(m[3], { x }), ad = +m[4];
  assert(ab > 0 && bc > 0 && ac === ab + bc && ad > ac && ad % 2 === 0);
  [x, ac, ad - ac, ad / 2].forEach((w, i) => assert.strictEqual(num(p.parts[i].answer), w, 'segment part ' + i));
}, 60);
run('angle', p => {
  const m = /[Aa]ngle ABD measures ⟨\(([^⟩]+)\)⟩ degrees, angle DBC measures ⟨\(([^⟩]+)\)⟩ degrees, and angle ABC measures ⟨\(([^⟩]+)\)⟩ degrees/.exec(p.prompt); assert(m);
  const x = solve(m[3], '(' + m[1] + ')+(' + m[2] + ')', 'x'), abd = ev(m[1], { x }), dbc = ev(m[2], { x }), abc = ev(m[3], { x });
  assert(abc === abd + dbc && abc < 180 && abc % 2 === 0 && abd > abc / 2, 'bisector falls inside ABD');
  [x, abc, abc / 2, abd - abc / 2].forEach((w, i) => assert.strictEqual(num(p.parts[i].answer), w, 'angle part ' + i));
  assert(M.geoFigures.check(p.fig).ok);
}, 60);
run('coordinate', p => {
  const m = /Point A is at \((-?\d+), (-?\d+)\) and M is at \((-?\d+), (-?\d+)\)/.exec(plain(p.prompt)); assert(m);
  const [ax, ay, mx, my] = m.slice(1).map(Number), bx = 2 * mx - ax, by = 2 * my - ay, len2 = (bx - ax) ** 2 + (by - ay) ** 2, len = Math.sqrt(len2);
  assert(Number.isInteger(len));
  [bx, by, len, len / 2].forEach((w, i) => assert.strictEqual(num(p.parts[i].answer), w, 'coordinate part ' + i + ' ' + p.parts[i].answer));
}, 60);
run('lines', p => {
  const m = /[Aa]ngle AOC measures ⟨\(([^⟩]+)\)⟩ degrees and angle BOC measures ⟨\(([^⟩]+)\)⟩ degrees/.exec(p.prompt); assert(m);
  const x = solve('(' + m[1] + ')+(' + m[2] + ')', '180', 'x'), aoc = ev(m[1], { x }), boc = ev(m[2], { x });
  assert(aoc + boc === 180 && aoc > 0 && boc > 0 && boc % 2 === 0);
  [x, aoc, boc, boc / 2].forEach((w, i) => assert.strictEqual(num(p.parts[i].answer), w, 'lines part ' + i));
  assert(M.geoFigures.check(p.fig).ok);
}, 60);
console.log('Foundations investigations: ' + n + ' problems re-derived from their printed text; every key, figure and relation agrees.');
