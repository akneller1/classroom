#!/usr/bin/env node
// Statistics audit #9 (2026-11-18): Graphing Practice for Anticipating Patterns and Statistical Inference. Every generated
// item, at every level and skill, is graded correct by core/plot.js when the target is entered and wrong when a boundary
// moves, the shading flips or an endpoint changes; the numbers are recomputed here, and the page, router and unit map are wired.
'use strict';
const assert = require('assert');
const fs = require('fs');
const path = require('path');
const ROOT = path.join(__dirname, '..');
require(path.join(ROOT, 'worksheet-generator/core/plot.js'));
require(path.join(ROOT, 'worksheet-generator/plot-statistics.js'));
const { MK_PLOT: plot, MK_STAT_PLOT: S } = globalThis;

const units = ['anticipating-patterns', 'statistical-inference'];
assert.deepStrictEqual(S.units.slice().sort(), units.slice().sort());
// Φ used for the worked solutions agrees with a high-precision value
for (const [z, v] of [[0, 0.5], [1, 0.8413447], [1.96, 0.9750021], [-2.33, 0.0099031], [2.576, 0.9950025]]) assert(Math.abs(S.phi(z) - v) < 2e-7, 'phi ' + z);
const onGrid = (v, line) => Math.abs((v - line.min) / line.snap - Math.round((v - line.min) / line.snap)) < 1e-6 && v >= line.min - 1e-9 && v <= line.max + 1e-9;
let n = 0;
const kinds = {};
for (let round = 0; round < 20; round++) for (const u of units) for (const lv of ['cp2', 'cp1', 'honors']) for (const s of S.skills(u)) {
  const pool = S.pool(u, lv, s.id, 6);
  assert(pool.length >= 5, `${u} ${lv} ${s.id}: only ${pool.length} items`);
  for (const q of pool) {
    const p = q.plot, t = p.target, L = p.numberLine;
    assert(q.prompt && q.solutionSteps.length >= 3 && p.answerKey.svg.startsWith('data:image/svg+xml') && p.answerKey.alt, q.id + ' content');
    assert(!/NaN|undefined|Infinity|− −|\+ −/.test(q.prompt + q.solutionSteps.join(' ') + p.answerKey.alt), q.id + ' text: ' + q.prompt);
    assert(L.max > L.min && L.snap > 0 && L.tick > 0 && (L.max - L.min) / L.tick <= 40, q.id + ' number line');
    if (p.tool === 'number-line-point') {
      assert(t.values.length === 3 && t.values.every(v => onGrid(v, L)), q.id + ' points on grid');
      const [a, c, b] = t.values;
      assert(Math.abs((c - a) - (b - c)) < 1e-9 && b > a, q.id + ' symmetric about the center');
      assert(plot.check(p, { values: t.values.map(String) }).ok, q.id + ' correct graded wrong');
      assert(plot.check(p, { values: t.values.slice().reverse().map(String) }).ok, q.id + ' order should not matter');
      assert(!plot.check(p, { values: [a, c, c + (b - c) / 2].map(String) }).ok, q.id + ' one SD instead of two graded correct');
      // recompute the standard deviation from the prompt
      const m = q.prompt.match(/p = ([\d.]+)\. Random samples of n = (\d+)/), mx = q.prompt.match(/σ = ([\d.]+) .*n = (\d+)/);
      const sd = m ? Math.sqrt(+m[1] * (1 - +m[1]) / +m[2]) : +mx[1] / Math.sqrt(+mx[2]);
      assert(Math.abs((b - c) / 2 - sd) < 1e-9, q.id + ' standard deviation ' + sd);
      kinds.sampling = (kinds.sampling || 0) + 1;
    } else {
      assert.strictEqual(p.tool, 'number-line-inequality');
      if ('between' in t) {
        assert(onGrid(t.left.value, L) && onGrid(t.right.value, L) && t.left.value < t.right.value, q.id + ' endpoints on grid');
        assert(plot.check(p, JSON.parse(JSON.stringify(t))).ok, q.id + ' correct graded wrong');
        const flip = JSON.parse(JSON.stringify(t)); flip.between = !flip.between;
        assert.strictEqual(plot.check(p, flip).code, 'and-or', q.id + ' and/or feedback');
        const moved = JSON.parse(JSON.stringify(t)); moved.right.value = +(moved.right.value + L.snap).toFixed(6);
        if (moved.right.value <= L.max) assert.strictEqual(plot.check(p, moved).code, 'boundary', q.id + ' moved endpoint');
        const oc = JSON.parse(JSON.stringify(t)); oc.left.closed = !oc.left.closed;
        assert.strictEqual(plot.check(p, oc).code, 'closed-open', q.id + ' open/closed');
      } else {
        assert(onGrid(t.boundary, L), q.id + ' boundary on grid');
        assert(plot.check(p, { ...t }).ok, q.id + ' correct graded wrong');
        assert.strictEqual(plot.check(p, { ...t, direction: t.direction === 'right' ? 'left' : 'right' }).code, 'direction', q.id + ' direction');
        assert.strictEqual(plot.check(p, { ...t, closed: !t.closed }).code, 'closed-open', q.id + ' closed/open');
        assert.strictEqual(plot.check(p, { ...t, boundary: +(t.boundary + L.snap).toFixed(6) }).code, 'boundary', q.id + ' boundary');
      }
      for (const code of ['boundary', 'direction', 'closed-open', 'and-or']) assert(p.feedback[code], q.id + ' feedback ' + code);
      kinds[s.id] = (kinds[s.id] || 0) + 1;
    }
    // the probabilities in the worked solution follow Table A (z to two decimals)
    if (s.id === 'normal-area') {
      const m = q.prompt.match(/mean (−?[\d.]+) and standard deviation ([\d.]+)/), mu = +m[1].replace('−', '-'), sd = +m[2];
      const area = +q.solutionSteps[2].match(/(\d\.\d{4}) \(Table A\)\.$/)[1], T = z => Math.round(S.phi(Math.round(z * 100) / 100) * 1e4) / 1e4;
      let want;
      if ('between' in t) want = t.between ? T((t.right.value - mu) / sd) - T((t.left.value - mu) / sd) : T((t.left.value - mu) / sd) + 1 - T((t.right.value - mu) / sd);
      else want = t.direction === 'right' ? 1 - T((t.boundary - mu) / sd) : T((t.boundary - mu) / sd);
      assert(Math.abs(area - want) < 1.5e-4, q.id + ' area ' + area + ' vs ' + want);
    }
    if (s.id === 'confidence-interval' && /p̂ = /.test(q.prompt)) {
      const m = q.prompt.match(/sample of (\d+), p̂ = ([\d.]+)\..*z\* = ([\d.]+)/), nn = +m[1], ph = +m[2], z = +m[3];
      const me = Math.round(z * Math.sqrt(ph * (1 - ph) / nn) * 100) / 100;
      assert(Math.abs(t.left.value - (ph - me)) < 1e-9 && Math.abs(t.right.value - (ph + me)) < 1e-9, q.id + ' interval');
    }
    if (s.id === 'rejection-region') {
      const m = q.prompt.match(/p ([<>≠]) p₀ at significance level α = (\d*\.\d+)/), a = +m[2];
      const crit = Math.abs('between' in t ? t.right.value : t.boundary), tail = m[1] === '≠' ? a / 2 : a;
      assert(Math.abs(1 - S.phi(crit) - tail) < 6e-4, q.id + ' critical value ' + crit);
    }
    n++;
  }
}
assert(kinds.sampling > 50 && kinds['normal-area'] > 50 && kinds['confidence-interval'] > 50 && kinds['p-value-region'] > 50 && kinds['rejection-region'] > 50, JSON.stringify(kinds));
// wiring
const html = fs.readFileSync(path.join(ROOT, 'worksheet-generator/plot-practice.html'), 'utf8');
assert.match(html, /<script src="plot-statistics\.js\?v=[^"]+"><\/script>/);
assert.match(fs.readFileSync(path.join(ROOT, 'worksheet-generator/plot-practice.js'), 'utf8'), /courseId==='statistics'&&G\.MK_STAT_PLOT/);
const data = fs.readFileSync(path.join(ROOT, 'data.js'), 'utf8');
const map = data.match(/Reviewed graphing practice[^\n]*\n\(function\(G\)\{var units=(\{[^;]*\});/);
const unitsMap = JSON.parse(map[1]);
assert.deepStrictEqual(unitsMap.statistics.slice().sort(), ['exploring-data', ...units].sort());
console.log(`PASS Statistics graphing practice: ${n} generated items checked across ${units.length} units, 3 levels and ${units.reduce((s, u) => s + S.skills(u).length, 0)} skills`);
