#!/usr/bin/env node
// Grade 5 audit #1 (2026-11-19): Graphing Practice for Coordinate Planes and Graphing and for Data, Line Plots, and
// Problem Solving. Every generated item, at every level and skill, is graded correct by core/plot.js when its target is
// entered and wrong for common mistakes; the numbers are recomputed from the prompt; the page, router and cards are wired.
'use strict';
const assert = require('assert');
const fs = require('fs');
const path = require('path');
const ROOT = path.join(__dirname, '..');
require(path.join(ROOT, 'worksheet-generator/core/plot.js'));
require(path.join(ROOT, 'worksheet-generator/plot-grade5.js'));
const { MK_PLOT: plot, MK_G5_PLOT: S } = globalThis;
const units = ['coordinate-plane-graphing', 'data-line-plots-problem-solving'];
assert.deepStrictEqual(S.units.slice().sort(), units.slice().sort());
const pts = (s) => [...s.matchAll(/\((\d+), (\d+)\)/g)].map((m) => [+m[1], +m[2]]);
// "1 3/4" -> 7/4 as [n, d]; "3/8" -> [3, 8]; "2" -> [2, 1]
const val = (s) => { const m = s.match(/^(?:(\d+) )?(\d+)\/(\d+)$/); if (!m) return [+s, 1]; return [(+(m[1] || 0)) * +m[3] + +m[2], +m[3]]; };
const eqv = (a, b) => { const x = val(a), y = val(b); return x[0] * y[1] === y[0] * x[1]; };
let n = 0;
for (let round = 0; round < 30; round++) for (const u of units) for (const lv of ['cp2', 'cp1', 'honors']) for (const s of S.skills(u)) {
  const pool = S.pool(u, lv, s.id, 6);
  assert(pool.length >= 5, `${u} ${lv} ${s.id}: only ${pool.length} items`);
  for (const q of pool) {
    const p = q.plot, t = p.target, P = q.prompt, txt = P + ' ' + q.solutionSteps.join(' ') + ' ' + p.answerKey.alt;
    assert(P && q.solutionSteps.length >= 2 && p.answerKey.svg.startsWith('data:image/svg+xml') && p.answerKey.alt, q.id + ' content');
    assert(!/NaN|undefined|Infinity|\b1 (yards|inches|liters|pounds|miles)\b|\/1\b/.test(txt), q.id + ' text: ' + txt);
    if (p.tool === 'points') {
      const g = p.grid;
      assert(t.points.every(([x, y]) => Number.isInteger(x) && Number.isInteger(y) && x >= g.xmin && x <= g.xmax && y >= g.ymin && y <= g.ymax), q.id + ' points on the first-quadrant grid');
      assert.strictEqual(new Set(t.points.map(String)).size, t.points.length, q.id + ' distinct points');
      assert(plot.check(p, { points: t.points }).ok, q.id + ' correct graded wrong');
      const asked = P.slice(P.lastIndexOf('Plot ')).match(/\b[A-Z]\b/g);
      if (s.id !== 'pattern-pairs') assert.deepStrictEqual(asked, ['A', 'B', 'C'].slice(0, t.points.length), q.id + ' asks for dots named as the widget names them: ' + P);
      assert(!plot.check(p, { points: t.points.map(([x, y], i) => (i ? [x, y] : [x + 1, y])) }).ok, q.id + ' moved point graded correct');
      let want;
      if (s.id === 'plot-points') {
        const given = pts(P);
        if (lv === 'honors') { const m = P.match(/B is (\d+) units to the right of A and (\d+) units up/); want = [given[0], [given[0][0] + +m[1], given[0][1] + +m[2]], given[1]]; }
        else want = given;
      } else if (s.id === 'pattern-pairs') {
        const a = +P.match(/Pattern A starts at 0 and adds (\d+)/)[1], b = +P.match(/Pattern B starts at 0 and adds (\d+)/)[1], k = /first 4/.test(P) ? 4 : 3;
        want = Array.from({ length: k }, (_, i) => [a * (i + 1), b * (i + 1)]);
        if (lv === 'honors') assert(q.solutionSteps.some((x) => x.includes(`is ${b / a} times`)), q.id + ' honors comparison');
      } else {
        const D = pts(P)[0], w = +P.match(/(?:It is (\d+) units wide|DC is (\d+) units long)/).slice(1).find(Boolean);
        const h = P.includes('area') ? +P.match(/area is (\d+)/)[1] / w : +P.match(/(\d+) units tall/)[1];
        const C = [D[0] + w, D[1]], all = [[D[0], D[1] + h], [D[0] + w, D[1] + h], C];
        want = lv === 'cp2' ? all.slice(0, 2) : all;
        if (lv === 'cp2') assert.deepStrictEqual(pts(P)[1], C, q.id + ' given C');
      }
      assert.deepStrictEqual(t.points, want, q.id + ' points recomputed from the prompt');
    } else {
      assert.strictEqual(p.tool, 'line-plot');
      const data = P.match(/: ([\d/ ,]+)\. Make a line plot/)[1].split(', ');
      assert.strictEqual(t.values.length, data.length, q.id + ' one X per measurement');
      const pool2 = t.values.slice();
      for (const d of data) { const i = pool2.findIndex((v) => eqv(v, d)); assert(i >= 0, q.id + ' value ' + d + ' in target'); pool2.splice(i, 1); }
      assert(plot.check(p, { marks: t.values }).ok, q.id + ' correct line plot graded wrong');
      assert(plot.check(p, { marks: t.values.slice().reverse() }).ok, q.id + ' order does not matter');
      assert.strictEqual(plot.check(p, { marks: t.values.slice(1) }).code, 'count', q.id + ' missing X');
      const den = +p.numberLine.snap.split('/')[1], lo = +p.numberLine.min, hi = +p.numberLine.max;
      const moved = t.values.slice(), v0 = val(moved[0]), up = (v0[0] * den / v0[1] + (v0[0] * den / v0[1] < hi * den ? 1 : -1));
      moved[0] = up + '/' + den;
      assert.strictEqual(plot.check(p, { marks: moved }).ok, false, q.id + ' X one tick off graded correct');
      assert(t.values.every((v) => { const [a, b] = val(v); return a * hi >= 0 && a * 1 <= hi * b && a >= lo * b && (a * den) % b === 0; }), q.id + ' values on the scale');
      if (lv === 'honors' && s.id === 'fraction-line-plot') {
        const tot = data.reduce((acc, d) => { const [a, b] = val(d); return acc + a / b; }, 0), last = q.solutionSteps[q.solutionSteps.length - 1];
        const each = last.match(/= ([\d/ ]+) (?:yard|inch|liter|pound)/)[1], [ea, eb] = val(each);
        assert(Math.abs(ea / eb - tot / data.length) < 1e-9, q.id + ' fair share recomputed: ' + last);
      }
      if (lv === 'honors' && s.id === 'mixed-line-plot') {
        const xs = data.map((d) => { const [a, b] = val(d); return a / b; }), last = q.solutionSteps[q.solutionSteps.length - 1];
        const [ea, eb] = val(last.match(/= ([\d/ ]+) (?:inch|mile|pound)/)[1]);
        assert(Math.abs(ea / eb - (Math.max(...xs) - Math.min(...xs))) < 1e-9, q.id + ' range recomputed: ' + last);
      }
    }
    n++;
  }
}
const html = fs.readFileSync(path.join(ROOT, 'worksheet-generator/plot-practice.html'), 'utf8');
assert(/<script src="plot-grade5\.js\?v=[^"]+"><\/script>/.test(html), 'plot-practice.html loads plot-grade5.js');
assert(/courseId==='grade5'&&G\.MK_G5_PLOT/.test(fs.readFileSync(path.join(ROOT, 'worksheet-generator/plot-practice.js'), 'utf8')), 'router sends Grade 5 units to MK_G5_PLOT');
const data = fs.readFileSync(path.join(ROOT, 'data.js'), 'utf8');
assert(/"grade5": \["data-line-plots-problem-solving","coordinate-plane-graphing"\]/.test(data), 'Graphing Practice cards for both Grade 5 units');
// The card must also be reachable: course-integrations.js adds Grade 5 after data.js attached the cards, so it attaches
// again; the unit pages list the 'plot' format under Study Guides; the graphing page loads the integrated courses.
assert(/MK_CONTENT_UPDATES\.attach\(\)/.test(fs.readFileSync(path.join(ROOT, 'course-integrations.js'), 'utf8')), 'Grade 5 cards attached after integration');
assert(/id: 'study-guides', name: 'Study Guides', formats: \[[^\]]*'plot'/.test(fs.readFileSync(path.join(ROOT, 'app.js'), 'utf8')), 'unit pages show Graphing Practice under Study Guides');
assert(/<script src="\.\.\/course-integrations\.js\?v=[^"]+"><\/script>/.test(html), 'plot-practice.html loads course-integrations.js');
console.log(`PASS Grade 5 graphing practice: ${n} generated items checked across ${units.length} units, 3 levels and ${units.reduce((a, u) => a + S.skills(u).length, 0)} skills`);
