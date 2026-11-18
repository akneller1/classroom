'use strict';
// Precalculus Graphing Practice (audit #8): every plot item in the four new units is graded correctly by
// core/plot.js, has an answer-key image, and its target is recomputed here from the printed prompt alone.
const assert = require('node:assert/strict');
const fs = require('node:fs'), path = require('node:path'), vm = require('node:vm');
const ROOT = path.join(__dirname, '..');
const ctx = {}; vm.createContext(ctx);
vm.runInContext(fs.readFileSync(path.join(ROOT, 'worksheet-generator/core/plot.js'), 'utf8'), ctx);
const P = ctx.MK_PLOT;
const UNITS = ['equations-inequalities', 'conics', 'sequences-series-limits', 'vectors'];

// exact rationals as [n, d]
const gcd = (a, b) => b ? gcd(b, a % b) : Math.abs(a);
const R = (n, d = 1) => { if (d < 0) { n = -n; d = -d; } const g = gcd(n, d) || 1; return [n / g, d / g]; };
const num = s => { s = s.replace(/−/g, '-').replace(/[()\s]/g, ''); const [a, b] = s.split('/'); return R(+a, b ? +b : 1); };
const eqR = (a, b) => a[0] * b[1] === b[0] * a[1];
const val = s => { const [n, d] = num(String(s)); return n / d; };
const norm = t => t.replace(/−/g, '-').replace(/\s+/g, '');

// "y = (2/3)x - 4", "y = -x", "y = 5"  →  [m, b]
function slopeIntercept(rhs) {
  const s = norm(rhs);
  const m = s.match(/^([+-]?(?:\(\d+\/\d+\)|\d+(?:\/\d+)?)?)x([+-]\d+)?$/);
  if (m) { const c = m[1] === '' || m[1] === '+' ? '1' : m[1] === '-' ? '-1' : m[1]; return [num(c), R(m[2] ? +m[2] : 0)]; }
  assert.match(s, /^[+-]?\d+$/, 'line ' + rhs);
  return [R(0), R(+s)];
}
// "-4x + 2y > -8" → slope-intercept with the inequality flipped when dividing by a negative
function standard(t) {
  const s = norm(t);
  let A, B, op, C;
  const k = v => v === '' || v === '+' ? 1 : v === '-' ? -1 : +v;
  const m1 = s.match(/^([+-]?\d*)x([+-]\d*)y(<|>|≤|≥|=)([+-]?\d+)$/), m2 = s.match(/^([+-]?\d*)y(<|>|≤|≥|=)([+-]?\d+)$/);
  if (m1) { A = k(m1[1]); B = k(m1[2]); op = m1[3]; C = +m1[4]; } else { assert(m2, 'standard form ' + t); A = 0; B = k(m2[1]); op = m2[2]; C = +m2[3]; }
  const flip = { '<': '>', '>': '<', '≤': '≥', '≥': '≤', '=': '=' };
  return { m: R(-A, B), b: R(C, B), op: B < 0 ? flip[op] : op };
}
function line(t) {
  const s = t.trim();
  if (/^y\s*[=<>≤≥]/.test(s)) { const op = s.match(/^y\s*([=<>≤≥])/)[1]; const [m, b] = slopeIntercept(s.replace(/^y\s*[=<>≤≥]\s*/, '')); return { m, b, op }; }
  return standard(s);
}
const sqTerm = (s, v) => { // "(x + 2)²" or "x²" → h
  s = norm(s);
  if (s === v + '²') return 0;
  const m = s.match(new RegExp('^\\(' + v + '([+-]\\d+)\\)²$')); assert(m, s); return -+m[1];
};

let n = 0, keys = 0;
for (const unit of UNITS) {
  const bank = JSON.parse(fs.readFileSync(path.join(ROOT, 'question-banks/precalculus', unit + '.json'), 'utf8'));
  const plots = bank.questions.filter(q => q.format === 'plot');
  for (const lv of ['cp2', 'cp1', 'honors']) assert(plots.filter(q => q.level === lv).length >= 8, `${unit} ${lv} plot items`);
  for (const q of plots) {
    const p = q.plot, t = p.target, id = q.id;
    // the site's grader
    assert.equal(P.valid(p), true, id + ' valid');
    assert.equal(P.check(p, p.testVectors.correct).ok, true, id + ' correct response');
    for (const w of p.testVectors.wrong) { const r = P.check(p, w.response); assert.equal(r.ok, false, id); assert.equal(r.code, w.expectCode, id); }
    assert.equal(P.check(p, null).ok, false, id);
    assert(fs.existsSync(path.join(ROOT, p.answerKey.src)), id + ' answer key image');
    keys++;
    // independent recomputation from the prompt
    let m;
    if (p.tool === 'system') {
      m = q.prompt.match(/^Solve the system by graphing: (.+) and (.+)\. Graph both lines/); assert(m, id);
      const L1 = line(m[1]), L2 = line(m[2]);
      t.lines.forEach((l, i) => { const L = [L1, L2][i]; assert(eqR(num(l.m), L.m) && eqR(num(l.b), L.b), id + ' line ' + i); });
      const f = r => r[0] / r[1], X = (f(L2.b) - f(L1.b)) / (f(L1.m) - f(L2.m)), Y = f(L1.m) * X + f(L1.b);
      assert(Math.abs(X - t.solution[0]) < 1e-9 && Math.abs(Y - t.solution[1]) < 1e-9, id + ' intersection');
      assert.equal(q.answer, `(${t.solution[0]}, ${t.solution[1]})`);
    } else if (p.tool === 'region') {
      m = q.prompt.match(/^Graph (.+)\.$/); assert(m, id);
      const L = line(m[1]);
      assert(eqR(num(t.m), L.m) && eqR(num(t.b), L.b) && t.op === L.op, id + ' inequality');
    } else if (p.tool === 'parabola') {
      let h, k, fp;
      if ((m = q.prompt.match(/^Graph (.+?) = (.*?)(\(y [−+] \d+\)|y)\. Drag/))) {
        h = sqTerm(m[1], 'x'); fp = m[2] === '' ? 1 : m[2] === '−' ? -1 : val(m[2]);
        k = m[3] === 'y' ? 0 : -val(m[3].replace(/[()y\s]/g, ''));
      } else {
        m = q.prompt.match(/vertex \((-?\d+), (-?\d+)\) and focus \((-?\d+), (-?[\d/]+)\)/); assert(m, id);
        h = +m[1]; k = +m[2]; assert.equal(+m[3], h, id); fp = 4 * (val(m[4]) - k);
      }
      assert(Math.abs(val(t.a) - 1 / fp) < 1e-12 && t.h === h && t.k === k, id + ' parabola');
    } else if (p.tool === 'points' && unit === 'vectors' && /^Convert each polar point/.test(q.prompt)) {
      const pts = [...q.prompt.matchAll(/[ABC]\((−?)(\d*)(√2)?, ([^)]+)\)/g)].map(mm => {
        const r = (mm[1] ? -1 : 1) * (mm[3] ? (mm[2] ? +mm[2] : 1) * Math.SQRT2 : +mm[2]);
        const th = mm[4] === '0' ? 0 : mm[4] === 'π' ? Math.PI : (() => { const g = mm[4].match(/^(\d*)π\/(\d+)$/); assert(g, id + ' angle ' + mm[4]); return (g[1] ? +g[1] : 1) * Math.PI / +g[2]; })();
        return [Math.round(r * Math.cos(th) * 1e9) / 1e9, Math.round(r * Math.sin(th) * 1e9) / 1e9];
      });
      assert.equal(pts.length, 3, id);
      assert.deepEqual(t.points.map(a => a.join()).sort(), pts.map(a => a.map(v => v + 0).join()).sort(), id + ' polar points');
    } else if (p.tool === 'points' && unit === 'vectors') {
      m = q.prompt.match(/plot (z and its conjugate z̄|z, its conjugate z̄ and −z|z and iz) for z = (−?\d+) ([+−]) (\d*)i\.$/); assert(m, id);
      const a = val(m[2]), b = (m[3] === '−' ? -1 : 1) * (m[4] ? +m[4] : 1);
      const want = m[1].startsWith('z and its') ? [[a, b], [a, -b]] : m[1].startsWith('z, its') ? [[a, b], [a, -b], [-a, -b]] : [[a, b], [-b, a]];
      assert.deepEqual(t.points.map(x => x.join()).sort(), want.map(x => x.join()).sort(), id + ' complex points');
    } else if (p.tool === 'points' && unit === 'conics') {
      m = q.prompt.match(/^For the circle (.+?), plot the center/); assert(m, id);
      const e = norm(m[1]); let h, k, r2;
      const s = e.match(/^(.+?²)\+(.+?²)=(\d+)$/);
      if (s && /²$/.test(s[1]) && /²$/.test(s[2]) && !/x²\+y²[+-]/.test(e)) { h = sqTerm(s[1], 'x'); k = sqTerm(s[2], 'y'); r2 = +s[3]; }
      else {
        const g = e.match(/^x²\+y²(?:([+-]\d*)x)?(?:([+-]\d*)y)?([+-]\d+)?=0$/); assert(g, id + ' ' + e);
        const c = v => v === undefined ? 0 : v === '+' ? 1 : v === '-' ? -1 : +v;
        h = -c(g[1]) / 2; k = -c(g[2]) / 2; r2 = h * h + k * k - c(g[3]);
      }
      const r = Math.sqrt(r2); assert(Number.isInteger(r), id);
      const want = [[h, k], [h, k + r], [h, k - r], [h + r, k], [h - r, k]].map(a => a.join()).sort();
      assert.deepEqual(t.points.map(a => a.join()).sort(), want, id + ' circle points');
    } else if (p.tool === 'points') {
      m = q.prompt.match(/sequence (.+) as points/); assert(m, id);
      const d = norm(m[1]); let terms;
      let e;
      if ((e = d.match(/^aₙ=([+-]?\d*)n([+-]\d+)?$/))) { const a = e[1] === '' ? 1 : e[1] === '-' ? -1 : +e[1]; terms = [1, 2, 3, 4].map(n => a * n + (e[2] ? +e[2] : 0)); }
      else if ((e = d.match(/^aₙ=([+-]?\d*)(?:\(([^)]+)\)|·?(\d+))ⁿ⁻¹$/))) { const r = val(e[2] || e[3]), a = e[1] === '' ? 1 : e[1] === '-' ? -1 : +e[1]; terms = [0, 1, 2, 3].map(i => a * r ** i); }
      else if ((e = d.match(/^a₁=([+-]?\d+),aₙ=aₙ₋₁([+-]\d+)$/))) terms = [0, 1, 2, 3].map(i => +e[1] + i * +e[2]);
      else if ((e = d.match(/^a₁=([+-]?\d+),aₙ=\(?([^)·]+)\)?·aₙ₋₁$/))) { const r = val(e[2]); terms = [0, 1, 2, 3].map(i => +e[1] * r ** i); }
      else assert.fail(id + ' definition ' + d);
      assert.deepEqual(t.points, terms.map((v, i) => [i + 1, v]), id + ' terms');
    } else if (p.tool === 'histogram') {
      m = q.prompt.match(/: ([\d, ]+)\. Make a histogram with (?:bins of width (\d+) starting at (\d+)|one bar for each value from (\d+) to (\d+))/); assert(m, id);
      const data = m[1].split(',').map(Number);
      assert.deepEqual(t.data, data, id + ' data');
      const width = m[2] ? +m[2] : 1, start = m[2] ? +m[3] : +m[4];
      assert.equal(p.bins.width, width); assert.equal(p.bins.start, start);
      const counts = Array(p.bins.count).fill(0); data.forEach(v => counts[Math.floor((v - start) / width)]++);
      assert.deepEqual(p.testVectors.correct.counts, counts, id + ' counts');
      assert(counts.reduce((a, b) => a + b) === data.length, id + ' every value in a bin');
    } else assert.fail('unexpected tool ' + p.tool);
    n++;
  }
}
assert(n >= 96, 'plot items: ' + n);
// The four units are listed in the Graphing Practice units map.
const data = fs.readFileSync(path.join(ROOT, 'data.js'), 'utf8');
const map = JSON.parse(data.match(/var units=(\{.*?\});function attach/)[1]);
for (const u of UNITS) assert(map.precalculus.includes(u), u + ' in Graphing Practice map');
console.log(`PASS ${n} Precalculus plot items recomputed from their prompts; ${keys} answer keys; ${map.precalculus.length} units have Graphing Practice`);
