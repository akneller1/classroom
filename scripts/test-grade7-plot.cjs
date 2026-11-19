#!/usr/bin/env node
// Grade 7 audit #14 (2026-11-19): Graphing Practice for Algebraic Expressions and Integers, One-Step Equations and
// Inequalities, Ratios, Proportions and Percentages, and Spatial Thinking. Every generated item, at every level and skill,
// is graded correct by core/plot.js when its target is entered and wrong for the common mistakes; the numbers are
// recomputed from the prompt, and the page, router and unit map are wired.
'use strict';
const assert = require('assert');
const fs = require('fs');
const path = require('path');
const ROOT = path.join(__dirname, '..');
require(path.join(ROOT, 'worksheet-generator/core/plot.js'));
require(path.join(ROOT, 'worksheet-generator/plot-grade7.js'));
const { MK_PLOT: plot, MK_G7_PLOT: S } = globalThis;
const units = ['algebraic-expressions-integers', 'one-step-equations-inequalities', 'ratios-proportions-percentages', 'spatial-thinking'];
assert.deepStrictEqual(S.units.slice().sort(), units.slice().sort());
const num = s => +String(s).replace(/−/g, '-');
const pts = s => [...s.matchAll(/\((−?\d+), (−?\d+)\)/g)].map(m => [num(m[1]), num(m[2])]);
let n = 0;
for (let round = 0; round < 25; round++) for (const u of units) for (const lv of ['cp2', 'cp1', 'honors']) for (const s of S.skills(u)) {
  const pool = S.pool(u, lv, s.id, 6);
  assert(pool.length >= 5, `${u} ${lv} ${s.id}: only ${pool.length} items`);
  for (const q of pool) {
    const p = q.plot, t = p.target;
    assert(q.prompt && q.solutionSteps.length >= 2 && p.answerKey.svg.startsWith('data:image/svg+xml') && p.answerKey.alt, q.id + ' content');
    assert(!/NaN|undefined|Infinity|− −|\+ −/.test(q.prompt + q.solutionSteps.join(' ') + p.answerKey.alt), q.id + ' text: ' + q.prompt);
    if (p.tool === 'points') {
      const g = p.grid;
      assert(t.points.every(([x, y]) => Number.isInteger(x) && Number.isInteger(y) && x >= g.xmin && x <= g.xmax && y >= g.ymin && y <= g.ymax), q.id + ' points on grid');
      assert(plot.check(p, { points: t.points }).ok, q.id + ' correct graded wrong');
      const moved = t.points.map(([x, y], i) => i ? [x, y] : [x + 1, y]);
      assert(!plot.check(p, { points: moved }).ok, q.id + ' moved point graded correct');
      const key = ps => ps.map(String).sort().join(';');
      if (key(t.points) !== key(t.points.map(([x, y]) => [y, x]))) assert(!plot.check(p, { points: t.points.map(([x, y]) => [y, x]) }).ok, q.id + ' swapped coordinates graded correct');
      // recompute the image from the prompt
      const given = pts(q.prompt);
      if (s.id === 'translate') {
        const m = q.prompt.match(/(\d+) units (right|left) and (\d+) units (up|down)/), r = q.prompt.match(/\(x, y\) → \(x ([+−]) (\d+), y ([+−]) (\d+)\)/);
        const dx = m ? (m[2] === 'right' ? 1 : -1) * +m[1] : (r[1] === '+' ? 1 : -1) * +r[2], dy = m ? (m[4] === 'up' ? 1 : -1) * +m[3] : (r[3] === '+' ? 1 : -1) * +r[4];
        assert.deepStrictEqual(t.points, given.slice(0, 3).map(([x, y]) => [x + dx, y + dy]), q.id + ' translation');
      } else if (s.id === 'rotate') {
        const a = +q.prompt.match(/Rotate it (\d+)°/)[1], rot = ([x, y]) => a === 90 ? [-y, x] : a === 180 ? [-x, -y] : [y, -x];
        assert.deepStrictEqual(t.points.map(String), given.slice(0, 3).map(rot).map(String), q.id + ' rotation');
      } else if (s.id === 'fourth-corner') {
        const [A, B, C] = given; assert.deepStrictEqual(t.points, [[A[0], C[1]]], q.id + ' fourth corner');
      } else if (lv !== 'honors') assert.deepStrictEqual(t.points.map(String).sort(), given.map(String).sort(), q.id + ' plotted points');
    } else if (p.tool === 'line') {
      const k = t.m.includes('/') ? t.m.split('/')[0] / t.m.split('/')[1] : +t.m;
      assert(t.b === '0' && k > 0, q.id + ' proportional');
      const x = [1, 2, 4].find(x => Number.isInteger(k * x));
      assert(plot.check(p, { points: [[0, 0], [x, k * x]] }).ok, q.id + ' correct line graded wrong');
      assert.strictEqual(plot.check(p, { points: [[0, 1], [x, k * x + 1]] }).code, 'intercept', q.id + ' line not through the origin');
      if (k !== 1) assert.notStrictEqual(plot.check(p, { points: [[0, 0], [k * x, x]] }).ok, true, q.id + ' reciprocal slope graded correct');
      const tab = q.prompt.match(/x \([^)]*\): ([\d, ]+); y \([^)]*\): ([\d., ]+)/), rec = q.prompt.match(/(\d+) \w+ correspond to ([\d.]+)/), each = q.prompt.match(/gives (\d+) /);
      const kk = tab ? tab[2].split(', ')[0] / tab[1].split(', ')[0] : rec ? rec[2] / rec[1] : +each[1];
      assert(Math.abs(kk - k) < 1e-9, q.id + ' constant of proportionality from the prompt');
    } else {
      assert.strictEqual(p.tool, 'number-line-inequality');
      assert(plot.check(p, { ...t }).ok, q.id + ' correct graded wrong');
      assert.strictEqual(plot.check(p, { ...t, direction: t.direction === 'right' ? 'left' : 'right' }).code, 'direction', q.id);
      assert.strictEqual(plot.check(p, { ...t, closed: !t.closed }).code, 'closed-open', q.id);
      assert.strictEqual(plot.check(p, { ...t, boundary: t.boundary + 1 }).code, 'boundary', q.id);
      // solve the prompt's inequality: "Solve <a><v> <rel> <c>." or "<v> ± a <rel> c"
      const m = q.prompt.match(/Solve (−?\d*)([a-z])(?: ([+−]) (\d+))? (<|>|≤|≥) (−?\d+)\./);
      const coef = m[1] === '' ? 1 : m[1] === '−' ? -1 : num(m[1]), add = m[3] ? (m[3] === '+' ? 1 : -1) * +m[4] : 0, c = num(m[6]);
      const sol = ((c - add) / coef) || 0, rel = coef < 0 ? { '<': '>', '>': '<', '≤': '≥', '≥': '≤' }[m[5]] : m[5];
      assert.strictEqual(t.boundary, sol, q.id + ' boundary');
      assert.strictEqual(t.closed, rel === '≤' || rel === '≥', q.id + ' closed');
      assert.strictEqual(t.direction, rel === '>' || rel === '≥' ? 'right' : 'left', q.id + ' direction');
    }
    n++;
  }
}
const html = fs.readFileSync(path.join(ROOT, 'worksheet-generator/plot-practice.html'), 'utf8');
assert(/<script src="plot-grade7\.js\?v=[^"]+"><\/script>/.test(html), 'plot-practice.html loads plot-grade7.js');
assert(/courseId==='prealgebra7'&&G\.MK_G7_PLOT/.test(fs.readFileSync(path.join(ROOT, 'worksheet-generator/plot-practice.js'), 'utf8')), 'router sends Grade 7 units to MK_G7_PLOT');
const data = fs.readFileSync(path.join(ROOT, 'data.js'), 'utf8');
for (const u of units) assert(new RegExp('"prealgebra7": \\[[^\\]]*"' + u + '"').test(data), 'Graphing Practice card for ' + u);
console.log(`PASS Grade 7 graphing practice: ${n} generated items checked across ${units.length} units, 3 levels and ${units.reduce((a, u) => a + S.skills(u).length, 0)} skills`);
