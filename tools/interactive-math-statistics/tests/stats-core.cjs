// Checks Lab.stats (artifacts/interactive-math/lab-stats.js) against published table values.
// Usage (repository root): node tools/interactive-math-statistics/tests/stats-core.cjs
const fs = require('fs'), vm = require('vm'), path = require('path');
const ctx = { window: { Lab: {}, location: { search: '' } }, Math }; ctx.window.window = ctx.window;
vm.runInNewContext(fs.readFileSync(path.resolve(__dirname, '../../../artifacts/interactive-math/lab-stats.js'), 'utf8'), ctx);
const S = ctx.window.Lab.stats; let f = 0, n = 0;
const near = (a, b, tol, m) => { n++; if (!(Math.abs(a - b) <= tol)) { f++; console.log('FAIL', m, a, 'expected', b); } };
near(S.normCdf(0), 0.5, 1e-7, 'Φ(0)'); near(S.normCdf(1.96), 0.9750021, 2e-7, 'Φ(1.96)'); near(S.normCdf(-1), 0.1586553, 2e-7, 'Φ(−1)'); near(S.normCdf(3), 0.9986501, 2e-7, 'Φ(3)'); near(S.normCdf(-4), 3.1671e-5, 1e-8, 'Φ(−4)');
for (const [p, z] of [[0.975, 1.959964], [0.95, 1.644854], [0.995, 2.575829], [0.9, 1.281552], [0.05, -1.644854], [0.001, -3.090232]]) near(S.invNorm(p), z, 2e-6, 'z for ' + p);
for (const [p, df, t] of [[0.975, 4, 2.776445], [0.975, 29, 2.045230], [0.95, 10, 1.812461], [0.995, 2, 9.924843], [0.975, 1, 12.706205], [0.9, 60, 1.295821], [0.025, 9, -2.262157], [0.995, 1, 63.656741], [0.9995, 500, 3.310091]]) near(S.invT(p, df), t, 2e-5, `t* p=${p} df=${df}`);
near(S.tCdf(2, 10), 0.963306, 2e-6, 'T10(2)'); near(S.tCdf(-1.5, 5), 0.0969518, 2e-6, 'T5(−1.5)'); near(S.tCdf(0, 7), 0.5, 1e-12, 'T7(0)');
near(S.sd([2, 4, 4, 4, 5, 5, 7, 9], true), 2, 1e-12, 'population sd'); near(S.sd([1, 2, 3, 4]), Math.sqrt(5 / 3), 1e-12, 'sample sd');
const r1 = S.rng(42), r2 = S.rng(42); near(r1(), r2(), 0, 'seeded rng repeats');
let s = 0, s2 = 0; const r = S.rng(7); for (let i = 0; i < 200000; i++) { const z = S.randNormal(r); s += z; s2 += z * z; }
near(s / 200000, 0, 0.01, 'normal mean'); near(Math.sqrt(s2 / 200000), 1, 0.01, 'normal sd');
console.log(`stats core: ${n - f}/${n} checks passed`); process.exit(f ? 1 : 0);
