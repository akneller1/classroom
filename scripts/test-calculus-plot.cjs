#!/usr/bin/env node
// Calculus audit #15 (2026-11-18): Graphing Practice for Calculus. Every generated item, at every level and skill,
// is graded correct by core/plot.js when the target is entered, wrong for nearby or swapped answers, stays on the
// grid, has an answer key and worked steps, and is wired into plot-practice and the Calculus unit cards.
'use strict';
const assert = require('assert');
const fs = require('fs');
const path = require('path');
const ROOT = path.join(__dirname, '..');
require(path.join(ROOT, 'worksheet-generator/core/plot.js'));
require(path.join(ROOT, 'worksheet-generator/plot-calculus.js'));
const { MK_PLOT: plot, MK_CAL_PLOT: C } = globalThis;

const units = ['derivatives', 'applications-derivatives', 'fundamental-theorem-calculus', 'applications-integrals', 'differential-equations'];
assert.deepStrictEqual(C.units.slice().sort(), units.slice().sort());
let n = 0;
const fr = v => plot.number(v);
for (let round = 0; round < 15; round++) for (const u of units) for (const lv of ['cp2', 'cp1', 'honors']) for (const s of C.skills(u)) {
  const pool = C.pool(u, lv, s.id, 6);
  assert(pool.length >= 5, `${u} ${lv} ${s.id}: only ${pool.length} items`);
  for (const q of pool) {
    const p = q.plot;
    assert(q.prompt && q.solutionSteps.length >= 2 && p.answerKey.svg.startsWith('data:image/svg+xml') && p.answerKey.alt, q.id + ' content');
    assert(!/NaN|undefined|Infinity|\+ −|− −|\b1x|\b0x/.test(q.prompt + q.solutionSteps.join(' ') + p.answerKey.alt), q.id + ' text: ' + q.prompt);
    if (p.tool === 'points') {
      const P = p.target.points;
      assert(P.every(([x, y]) => Number.isInteger(x) && Number.isInteger(y) && Math.abs(x) <= 8 && Math.abs(y) <= 8), q.id + ' on grid');
      assert(plot.check(p, { points: P.map(a => a.slice()) }).ok, q.id + ' correct answer graded wrong');
      assert(plot.check(p, { points: P.slice().reverse().map(a => a.slice()) }).ok, q.id + ' order of points should not matter');
      const moved = P.map((a, i) => i ? a.slice() : [a[0], a[1] + 1]);
      assert(!plot.check(p, { points: moved }).ok, q.id + ' moved point graded correct');
      const sw = P.map(([x, y]) => [y, x]);
      if (P.some(([x, y]) => x !== y)) assert(!plot.check(p, { points: sw }).ok, q.id + ' swapped graded correct');
    } else {
      assert.strictEqual(p.tool, 'line');
      const m = fr(p.target.m), b = fr(p.target.b);
      assert(Number.isInteger(m) && Number.isInteger(b) && Math.abs(b) <= 8 && Math.abs(m + b) <= 8, q.id + ' line on grid');
      assert(plot.check(p, { points: [[0, b], [1, m + b]] }).ok, q.id + ' tangent line graded wrong');
      assert(!plot.check(p, { points: [[0, b + 1], [1, m + b + 1]] }).ok, q.id + ' shifted line graded correct');
      if (m) assert.strictEqual(plot.check(p, { points: [[0, b], [1, b - m]] }).code, 'slope-sign', q.id + ' slope sign feedback');
      assert(p.feedback[plot.check(p, { points: [[0, b + 1], [1, m + b + 1]] }).code], q.id + ' feedback for a shifted line');
    }
    n++;
  }
}
// spot-check the mathematics of a few makers against hand computation
const one = (u, s, lv) => C.pool(u, lv, s, 1)[0];
for (let i = 0; i < 40; i++) {
  const q = one('derivatives', 'tangent', 'cp1');
  const f = q.prompt.match(/f\(x\) = (.*) at x = (−?\d+)/);
  const coef = {}; f[1].replace(/−/g, '-').replace(/ /g, '').replace(/([+-]?\d*)(x([²³⁴])?)?/g, (all, c, xx, pw) => {
    if (!all) return ''; const k = xx ? ({ '²': 2, '³': 3, '⁴': 4 }[pw] || 1) : 0; coef[k] = (coef[k] || 0) + (c === '' || c === '+' ? 1 : c === '-' ? -1 : +c); return '';
  });
  const a = +f[2].replace('−', '-'), F = x => Object.entries(coef).reduce((s, [k, c]) => s + c * x ** k, 0);
  const slope = (F(a + 1e-6) - F(a - 1e-6)) / 2e-6;
  assert(Math.abs(slope - fr(q.plot.target.m)) < 1e-4 && Math.abs(F(a) - (fr(q.plot.target.m) * a + fr(q.plot.target.b))) < 1e-9, q.prompt);
}
// wiring: the page loads the module, routes Calculus units to it, and the units carry a Graphing Practice card
const html = fs.readFileSync(path.join(ROOT, 'worksheet-generator/plot-practice.html'), 'utf8');
assert.match(html, /<script src="plot-calculus\.js\?v=[^"]+"><\/script>/);
assert.match(fs.readFileSync(path.join(ROOT, 'worksheet-generator/plot-practice.js'), 'utf8'), /courseId==='calculus'&&G\.MK_CAL_PLOT/);
const data = fs.readFileSync(path.join(ROOT, 'data.js'), 'utf8');
const map = data.match(/Reviewed graphing practice[^\n]*\n\(function\(G\)\{var units=(\{[^;]*\});/);
const unitsMap = JSON.parse(map[1]);
assert.deepStrictEqual((unitsMap.calculus || []).slice().sort(), units.slice().sort());
console.log(`PASS Calculus graphing practice: ${n} generated items checked across ${units.length} units, 3 levels and ${units.reduce((s, u) => s + C.skills(u).length, 0)} skills`);
