/* Matching Card Sort (printables.html#kind=match): every supported unit × level × set count, checked
   independently of the builder's own filtering.
   Run: node worksheet-generator/menu/tests/printables-match-tests.cjs   (SEEDS=n for more builds) */
'use strict';
const assert = require('node:assert/strict');
const load = require('./load.cjs');
const env = load(['games/bank.js', 'menu/printables.js', 'menu/printables-match.js']), M = env.MKMENU, PR = M.printables, MT = PR.MATCH;
const SEEDS = +(process.env.SEEDS || 4);
let checks = 0, builds = 0; const ok = (c, m) => { checks++; assert.ok(c, m); };
const near = (a, b) => Math.abs(a - b) < 1e-7;

/* sampled independently: g fits f's graph if it stays within half a grid unit of every drawn curve point and dot */
function graphConfusable(f, g) {
  const w = f.graph, tol = 0.5 * w.ystep;
  const pts = [].concat(...w.curves).concat(w.dots);
  if (!pts.length) return true;
  return pts.every(([x, y]) => { const v = g.f(x); return isFinite(v) && Math.abs(v - y) <= tol; });
}

for (const unit of Object.keys(MT.UNITS)) {
  const U = MT.UNITS[unit];
  const famSets = [U.def].concat(U.fams.length > 1 ? [U.fams] : []);
  for (const fams of famSets) for (const level of ['cp2', 'cp1', 'honors']) for (const sets of [4, 6, 8, 10]) for (let s = 0; s < SEEDS; s++) {
    const cfg = { unitId: unit, kind: 'match', level, sets, seed: 1000 + s * 7919 + sets, blanks: s % 2 ? 'some' : 'none', families: Object.fromEntries(U.fams.map(f => [f, fams.includes(f)])) };
    const tag = `${unit} ${fams.join('+')} ${level} ${sets} sets seed ${cfg.seed}`;
    const B = PR.build(cfg, 0); builds++;
    ok(!B.error, tag + ': ' + B.error);
    ok(B.fns.length === sets, tag + ': right number of sets');
    B.fns.forEach((f, i) => {
      ok(fams.includes(f.fam), tag + ': only the chosen function types');
      // every value printed on a card is the function's own value
      f.table.rows.forEach(([x, y]) => ok(near(f.f(x), y), tag + ': table row is on the function'));
      f.graph.dots.forEach(([x, y]) => ok(near(f.f(x), y), tag + ': graph dot is on the function'));
      f.graph.curves.forEach(c => c.forEach(([x, y]) => ok(y >= f.graph.ymin - 1e-6 && y <= f.graph.ymax + 1e-6, tag + ': curve stays in the window')));
      ok(f.graph.curves.length || f.discrete, tag + ': graph has a curve');
      ok(f.desc.length >= 1 && f.desc.length <= 3, tag + ': 1–3 description facts');
      f.desc.forEach(ft => ok(ft.test(f), tag + ': description fact is true: ' + ft.text));
      ok(!/NaN|undefined|Infinity/.test(f.eq + f.desc.map(d => d.text).join('')), tag + ': clean text ' + f.eq);
      B.fns.forEach((g, j) => {
        if (i === j) return;
        ok(!MT.sameFn(f, g), tag + ': different functions');
        ok(f.eq !== g.eq, tag + ': different equations');
        ok(!graphConfusable(f, g), tag + `: graph ${i} could also be ${g.eq}`);
        ok(!f.table.rows.every(([x, y]) => near(g.f(x), y)), tag + `: table ${i} also fits ${g.eq}`);
        ok(!f.desc.every(ft => ft.test(g)), tag + `: description of ${f.eq} also fits ${g.eq}`);
      });
    });
    MT.TYPES.forEach(t => ok(new Set(B.ids[t.id]).size === sets && B.ids[t.id].every(n => n >= 1 && n <= sets), tag + ': card numbers 1..N'));
    if (cfg.blanks === 'some') ok(Object.keys(B.blanks).length === Math.ceil(sets / 3), tag + ': blank cards');
    else ok(Object.keys(B.blanks).length === 0, tag + ': no blank cards');
  }
}
// greyed out everywhere else
for (const unit of Object.keys(M.skillSets)) if (!MT.UNITS[unit]) ok(PR.build({ unitId: unit, kind: 'match', level: 'cp1', seed: 1 }, 0).error, unit + ': matching is unavailable');
console.log('printables-match: ' + builds + ' builds, ' + checks + ' checks passed');
