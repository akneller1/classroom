#!/usr/bin/env node
// Grade 6 audit #11 (2026-11-19): Graphing Practice for Ratios, Rates, Percent and Proportions, Expressions and Equations,
// and Geometry. Every generated item, at every level and skill, is graded correct by core/plot.js when its target is
// entered and wrong for common mistakes; the numbers are recomputed from the prompt; the page, router and cards are wired.
'use strict';
const assert = require('assert');
const fs = require('fs');
const path = require('path');
const ROOT = path.join(__dirname, '..');
require(path.join(ROOT, 'worksheet-generator/core/plot.js'));
require(path.join(ROOT, 'worksheet-generator/plot-grade6.js'));
const { MK_PLOT: plot, MK_G6_PLOT: S } = globalThis;
const units = ['ratios-rates-percent-proportions', 'expressions-equations', 'geometry'];
assert.deepStrictEqual(S.units.slice().sort(), units.slice().sort());
const num = s => +String(s).replace(/−/g, '-');
const pts = s => [...s.matchAll(/\((−?\d+), (−?\d+)\)/g)].map(m => [num(m[1]), num(m[2])]);
const F = s => s.includes('/') ? s.split('/')[0] / s.split('/')[1] : +s;
let n = 0;
for (let round = 0; round < 25; round++) for (const u of units) for (const lv of ['cp2', 'cp1', 'honors']) for (const s of S.skills(u)) {
  const pool = S.pool(u, lv, s.id, 6);
  assert(pool.length >= 5, `${u} ${lv} ${s.id}: only ${pool.length} items`);
  for (const q of pool) {
    const p = q.plot, t = p.target, P = q.prompt;
    assert(P && q.solutionSteps.length >= 2 && p.answerKey.svg.startsWith('data:image/svg+xml') && p.answerKey.alt, q.id + ' content');
    assert(!/NaN|undefined|Infinity|− −|\+ −/.test(P + q.solutionSteps.join(' ') + p.answerKey.alt), q.id + ' text: ' + P);
    if (p.tool === 'points') {
      const g = p.grid;
      assert(t.points.every(([x, y]) => Number.isInteger(x) && Number.isInteger(y) && x >= g.xmin && x <= g.xmax && y >= g.ymin && y <= g.ymax), q.id + ' points on grid');
      assert(plot.check(p, { points: t.points }).ok, q.id + ' correct graded wrong');
      assert(!plot.check(p, { points: t.points.map(([x, y], i) => i ? [x, y] : [x + 1, y]) }).ok, q.id + ' moved point graded correct');
      let want;
      if (s.id === 'ratio-table') {
        const tab = P.match(/\(x\): ([\d, ]+) and .* \(y\): ([\d, ]+)\./), rec = P.match(/ is (\d+) to (\d+)\. /);
        if (tab) { const xs = tab[1].split(', ').map(Number), ys = tab[2].split(', ').map(Number); want = xs.map((x, i) => [x, ys[i]]); }
        else { const a = +rec[1], b = +rec[2], k = +P.match(/with (\d+) equivalent/)[1]; want = Array.from({ length: k }, (_, i) => [a * (i + 1), b * (i + 1)]); }
        assert(want.every(([x, y]) => y * want[0][0] === x * want[0][1]), q.id + ' equivalent ratios');
      } else if (s.id === 'table-points') {
        const m = P.match(/= (\d*)([a-z])(?: \+ (\d+))? gives/), k = m[1] ? +m[1] : 1, b = m[3] ? +m[3] : 0;
        want = P.match(/for [a-z] = ([\d, ]+)\./)[1].split(', ').map(Number).map(x => [x, k * x + b]);
      } else if (s.id === 'draw-rectangle') {
        const A = pts(P)[0], w = +P.match(/PQ is (\d+) units/)[1], h = P.includes('area') ? +P.match(/area is (\d+)/)[1] / w : +P.match(/QR is (\d+) units/)[1];
        want = [[A[0] + w, A[1]], [A[0] + w, A[1] + h], [A[0], A[1] + h]];
      } else {
        const A = pts(P)[0], ax = P.match(/across the ([xy])-axis/)[1], B = ax === 'y' ? [-A[0], A[1]] : [A[0], -A[1]];
        want = P.includes('rectangle PQRS') ? [B, [-A[0], -A[1]], ax === 'y' ? [A[0], -A[1]] : [-A[0], A[1]]] : [B];
      }
      assert.deepStrictEqual(t.points, want, q.id + ' points recomputed from the prompt');
      if (u === 'geometry') assert(!/\b[ABCD]\b/.test(P), q.id + ' vertex names do not clash with the widget\'s point names A, B, C');
    } else {
      assert.strictEqual(p.tool, 'line');
      const m = F(t.m), b = +t.b;
      const x = [1, 2, 4].find(x => Number.isInteger(m * x));
      assert(plot.check(p, { points: [[0, b], [x, b + m * x]] }).ok, q.id + ' correct line graded wrong');
      assert.notStrictEqual(plot.check(p, { points: [[0, b + 1], [x, b + 1 + m * x]] }).ok, true, q.id + ' shifted line graded correct');
      if (m !== 1) assert.notStrictEqual(plot.check(p, { points: [[0, b], [m * x, b + x]] }).ok, true, q.id + ' reciprocal slope graded correct');
      let mm, bb = 0;
      if (s.id === 'unit-rate-line') {
        const e = P.match(/Graph y = (\d+)x/), r = P.match(/^(\d+) .* go with ([\d.]+) /);
        mm = e ? +e[1] : r[2] / r[1];
      } else {
        const e = P.match(/Graph y = (\d*)x(?: \+ (\d+))?,/), r = P.match(/starts at (\d+) when x = 0 and is (\d+) when x = (\d+),/);
        if (e) { mm = e[1] ? +e[1] : 1; bb = e[2] ? +e[2] : 0; } else { bb = +r[1]; mm = (r[2] - r[1]) / r[3]; }
      }
      assert(Math.abs(mm - m) < 1e-9 && bb === b, q.id + ' line recomputed from the prompt');
    }
    n++;
  }
}
const html = fs.readFileSync(path.join(ROOT, 'worksheet-generator/plot-practice.html'), 'utf8');
assert(/<script src="plot-grade6\.js\?v=[^"]+"><\/script>/.test(html), 'plot-practice.html loads plot-grade6.js');
assert(/courseId==='math6'&&G\.MK_G6_PLOT/.test(fs.readFileSync(path.join(ROOT, 'worksheet-generator/plot-practice.js'), 'utf8')), 'router sends Grade 6 units to MK_G6_PLOT');
const data = fs.readFileSync(path.join(ROOT, 'data.js'), 'utf8');
for (const u of units) assert(new RegExp('"math6": \\[[^\\]]*"' + u + '"').test(data), 'Graphing Practice card for ' + u);
console.log(`PASS Grade 6 graphing practice: ${n} generated items checked across ${units.length} units, 3 levels and ${units.reduce((a, u) => a + S.skills(u).length, 0)} skills`);
