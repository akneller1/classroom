// Statistics tools: displayed numbers vs. independent values (SciPy/NumPy reference values computed separately and
// pasted below), simulation results vs. theory with wide tolerances, edge cases, and layout at Chromebook/light and phone/dark sizes.
// Usage (repository root): node tools/interactive-math-statistics/tests/correctness.cjs
const { chromium } = require('playwright'); const http = require('http'), fs = require('fs'), path = require('path');
const ROOT = path.resolve(__dirname, '../../..'); const M = require('../manifest.json');
const T = { '.html': 'text/html', '.js': 'text/javascript', '.css': 'text/css' };
let pass = 0, fail = 0; const ok = (c, m) => { if (c) pass++; else { fail++; console.log('FAIL', m); } };
const w = p => p.waitForTimeout(70);
const slider = async (p, id, v) => { await p.evaluate(([id, v]) => { const e = document.getElementById('sl-' + id); e.value = v; e.dispatchEvent(new Event('input')); }, [id, v]); await w(p); };
const click = async (p, sel, t) => { await p.evaluate(([s, t]) => { const b = [...document.querySelectorAll(s)].find(b => b.textContent.trim() === t || b.textContent.trim().startsWith(t)); if (!b) throw new Error('no ' + t); b.click(); }, [sel, t]); await w(p); };
const btn = (p, t) => click(p, 'button', t), chip = (p, t) => click(p, 'button.chip', t), tab = (p, t) => click(p, 'button.tab', t);
const txt = (p, s) => p.evaluate(s => [...document.querySelectorAll(s)].map(e => e.textContent).join(' | '), s);
const kv = async p => p.evaluate(() => { const o = {}; document.querySelectorAll('.panel dl.kv dt, .lab-panel dl.kv dt, dl.kv dt').forEach(dt => { o[dt.textContent.trim()] = dt.nextElementSibling.textContent.trim(); }); return o; });
const cells = p => p.evaluate(() => [...document.querySelectorAll('table')].map(t => [...t.querySelectorAll('tr')].map(r => [...r.children].map(c => c.textContent.trim()))));
const num = s => parseFloat(String(s).replace(/[−–]/g, '-').replace(/[^0-9.\-eE]/g, ' ').trim().split(/\s+/)[0]);
(async () => {
  const srv = await new Promise(r => { const s = http.createServer((q, res) => { const u = decodeURIComponent(q.url.split('?')[0]); fs.readFile(path.join(ROOT, u), (e, d) => { if (e) { res.writeHead(404); res.end(); return; } res.writeHead(200, { 'Content-Type': T[path.extname(u)] || 'application/octet-stream' }); res.end(d); }); }); s.listen(0, () => r(s)); });
  const b = await chromium.launch(), base = `http://localhost:${srv.address().port}/artifacts/`;
  const open = async (slug, seed = 7, vp = { width: 1366, height: 900 }, scheme = 'light') => { const ctx = await b.newContext({ viewport: vp, colorScheme: scheme, hasTouch: vp.width < 500 }); const p = await ctx.newPage(); p._e = []; p.on('pageerror', e => p._e.push(e.message)); await p.goto(base + slug + '/index.html?seed=' + seed); await w(p); return p; };
  /* layout */
  for (const t of M.tools) for (const [vp, sc] of [[{ width: 1366, height: 768 }, 'light'], [{ width: 360, height: 740 }, 'dark']]) {
    const p = await open(t.slug, 7, vp, sc);
    const L = await p.evaluate(() => { const de = document.documentElement, small = [], clip = []; document.querySelectorAll('button, input').forEach(e => { const r = e.getBoundingClientRect(); if (r.width && r.height < 28) small.push(e.textContent.trim() || e.type); });
      document.querySelectorAll('.readout').forEach(e => { if (e.scrollWidth > e.clientWidth + 2) clip.push(e.textContent.slice(0, 40)); }); return { over: de.scrollWidth > de.clientWidth, small, clip, bg: getComputedStyle(document.body).backgroundColor }; });
    ok(!L.over, `${t.slug} ${vp.width}: sideways scroll`); ok(!L.small.length, `${t.slug} ${vp.width}: small controls ${L.small}`); ok(!L.clip.length, `${t.slug} ${vp.width}: clipped readout ${L.clip}`);
    if (sc === 'dark') ok(L.bg === 'rgb(14, 16, 36)', t.slug + ' dark background ' + L.bg); ok(!p._e.length, t.slug + ' errors ' + p._e); await p.context().close();
  }
  let p, t, k, c;
  /* sampling distributions: simulated center and spread near theory; theory formula */
  p = await open('statistics-sampling-distribution-lab');
  for (const [pop, n] of [['Strongly right-skewed', 25], ['Uniform', 4], ['Bimodal', 50]]) {
    await chip(p, pop); await slider(p, 'sample-size', n); await btn(p, 'Draw 1,000'); await btn(p, 'Draw 1,000'); await btn(p, 'Draw 1,000');
    c = (await cells(p))[0]; const mu = num(c[1][1].split('=')[1]), sig = num(c[1][2].split('=')[1]), simM = num(c[2][1]), simS = num(c[2][2]), th = num(c[3][2].split('=').pop());
    ok(Math.abs(th - sig / Math.sqrt(n)) < 0.002, `${pop}: theory SD = σ/√n (${th} vs ${sig}/√${n})`);
    ok(Math.abs(simM - mu) < 4 * th / Math.sqrt(3000) + 0.01, `${pop}: simulated mean ${simM} near μ ${mu}`); ok(Math.abs(simS / th - 1) < 0.08, `${pop}: simulated SD ${simS} near ${th}`);
  }
  await chip(p, 'Sample proportion p̂'); await slider(p, 'population-p', 0.3); await slider(p, 'sample-size', 50); for (let i = 0; i < 3; i++) await btn(p, 'Draw 1,000');
  c = (await cells(p))[0]; ok(Math.abs(num(c[3][2].split('=').pop()) - Math.sqrt(0.3 * 0.7 / 50)) < 0.0006, 'p̂ theory SD'); ok(Math.abs(num(c[2][2]) / Math.sqrt(0.21 / 50) - 1) < 0.08, 'p̂ simulated SD ' + c[2][2]);
  ok(/Both are at least 10/.test(await txt(p, '.lp-feedback')), 'Large Counts met at n=50, p=0.3');
  await slider(p, 'sample-size', 10); ok(/below 10/.test(await txt(p, '.lp-feedback')), 'Large Counts fails at n=10');
  await slider(p, 'population-p', 0.05); await slider(p, 'sample-size', 1); await btn(p, 'Draw 100'); ok(!p._e.length, 'n = 1 proportion runs'); await p.context().close();
  /* confidence intervals: coverage vs theory */
  p = await open('statistics-confidence-interval-lab', 11);
  for (let i = 0; i < 20; i++) await btn(p, 'Make 100');
  k = await kv(p); let cov = num(k['Captured'].split('(')[1]); ok(cov > 91 && cov < 97.5, 'p = 0.4, n = 40 Wald coverage ≈ 94%: ' + cov);
  await chip(p, 'Mean μ'); await slider(p, 'sample-size', 5); await chip(p, 'z* with s'); for (let i = 0; i < 30; i++) await btn(p, 'Make 100');
  k = await kv(p); cov = num(k['Captured'].split('(')[1]); ok(Math.abs(cov - 87.84) < 2, 'z* with s, n = 5: coverage ≈ 87.8% (P(|t₄| < 1.96)): ' + cov);
  await chip(p, 't* (df = n − 1)'); for (let i = 0; i < 30; i++) await btn(p, 'Make 100'); k = await kv(p); cov = num(k['Captured'].split('(')[1]); ok(Math.abs(cov - 95) < 1.5, 't*, n = 5: coverage ≈ 95%: ' + cov);
  t = await txt(p, '.readout'); ok(/t\* = 2\.776/.test(t) && /df = 4/.test(t), 't* = 2.776 for df = 4: ' + t.slice(0, 120));
  await chip(p, 'Proportion p'); await slider(p, 'true-p', 0.05); await slider(p, 'sample-size', 10); await btn(p, 'Make 100'); ok(!p._e.length && /Not met/.test(await txt(p, '.lp-feedback')), 'p̂ = 0 samples handled, condition flagged'); await p.context().close();
  /* significance and power vs SciPy */
  p = await open('statistics-significance-power-explorer');
  await slider(p, 'successes', 60); k = await kv(p); ok(Math.abs(num(k['p-value']) - 0.02275) < 0.0001, 'p-value 0.0228: ' + k['p-value']); ok(/reject H/.test(await txt(p, '.lp-feedback')) && !/fail to reject/.test(await txt(p, '.lp-feedback')), 'rejects at 0.05');
  await chip(p, 'p ≠ p₀'); k = await kv(p); ok(Math.abs(num(k['p-value']) - 0.0455) < 0.0001, 'two-sided 0.0455: ' + k['p-value']);
  await chip(p, 'p < p₀'); await slider(p, 'sample-size', 250); await slider(p, 'successes', 140); k = await kv(p); ok(Math.abs(num(k['p-value']) - 0.97111) < 0.0001, 'p < p0 with p̂ above p0: 0.9711 ' + k['p-value']);
  ok(/fail to reject/.test(await txt(p, '.lp-feedback')) && /not show that H/.test(await txt(p, '.lp-feedback')), 'fail-to-reject wording');
  await tab(p, 'Errors & power'); await chip(p, 'p > p₀'); await slider(p, 'sample-size', 150); await slider(p, 'true-p', 0.6); k = await kv(p); ok(Math.abs(num(k['Power']) - 0.79424) < 0.0002, 'power 0.7942: ' + k['Power']);
  await chip(p, 'p ≠ p₀'); await chip(p, 'α = 0.01'); await slider(p, 'null-p0', 0.3); await slider(p, 'sample-size', 200); await slider(p, 'true-p', 0.25); k = await kv(p); ok(Math.abs(num(k['Power']) - 0.13720) < 0.0002, 'two-sided power 0.1372: ' + k['Power']);
  await slider(p, 'null-p0', 0.1); await slider(p, 'sample-size', 10); await tab(p, 'p-value'); ok(/Large Counts fails/.test(await txt(p, '.lp-feedback')), 'Large Counts warning in test'); ok(!p._e.length, 'significance errors ' + p._e); await p.context().close();
  /* sampling methods: bias and variability ordering */
  p = await open('statistics-sampling-methods-lab', 3);
  for (const m of ['Simple random sample', 'Stratified by grade', 'Cluster (whole homerooms)', 'Convenience (nearest the door)', 'Systematic (every k-th seat)']) { await chip(p, m); for (let i = 0; i < 5; i++) await btn(p, 'Take 100 samples'); }
  await chip(p, '64'); await chip(p, 'Systematic (every k-th seat)'); await btn(p, 'Take 100 samples'); ok(!p._e.length, 'systematic n = 64 (k = 2.5) runs');
  const rows = Object.fromEntries((await cells(p))[0].slice(1).map(r => [r[0] + r[1], r]));
  const sd = m => num(rows[m + '16'][5]), bias = m => num(rows[m + '16'][4]);
  ok(Math.abs(bias('Simple random sample')) < 0.05 && Math.abs(bias('Stratified by grade')) < 0.05 && Math.abs(bias('Cluster')) < 0.08, 'random methods unbiased');
  ok(bias('Convenience') < -0.6, 'convenience biased low: ' + bias('Convenience')); ok(sd('Stratified by grade') < sd('Simple random sample'), 'stratified less variable'); ok(sd('Cluster') > sd('Simple random sample'), 'single-grade clusters more variable');
  ok(sd('Convenience') === 0, 'convenience has no randomness: SD 0'); await p.context().close();
  /* conditional probability vs Bayes */
  p = await open('statistics-conditional-probability-explorer');
  for (const [pi, prev, se, sp] of [[3, 0.01, 99, 99], [5, 0.05, 95, 95], [0, 0.001, 99.5, 98], [9, 0.5, 80, 60]]) {
    await slider(p, 'prevalence', pi); await slider(p, 'sensitivity', se); await slider(p, 'specificity', sp);
    const ppv = prev * se / 100 / (prev * se / 100 + (1 - prev) * (1 - sp / 100)); t = await txt(p, '.readout b');
    ok(Math.abs(num(t) - 100 * ppv) < 0.06, `PPV prev ${prev} ${se}/${sp}: ${t} vs ${(100 * ppv).toFixed(2)}%`);
  }
  c = (await cells(p))[0]; ok(c[3][3] === '100,000', 'two-way table total');
  await slider(p, 'sensitivity', 50); await slider(p, 'specificity', 50); ok(/independent/.test(await txt(p, '.lp-feedback')), 'independence detected');
  await chip(p, 'Spam filter'); ok(/flagged/.test(await txt(p, 'svg')), 'spam context labels'); await p.context().close();
  /* regression vs NumPy */
  p = await open('statistics-regression-influence-lab');
  t = await txt(p, '.readout'); ok(/ŷ = 51\.97 \+ 3\.706/.test(t), 'LSRL ŷ = 51.97 + 3.706x: ' + t.slice(0, 40));
  k = await kv(p); ok(Math.abs(num(k['r']) - 0.9543) < 0.0001 && Math.abs(num(k['s']) - 3.552) < 0.001, 'r and s: ' + k['r'] + ' ' + k['s']);
  await chip(p, 'minutes'); t = await txt(p, '.readout'); const k2 = await kv(p); ok(/0\.0618/.test(t) && k2['r'] === k['r'] && k2['r²'] === k['r²'], 'minutes: slope ÷ 60, r and r² unchanged: ' + t.slice(0, 40));
  await chip(p, 'hours'); await chip(p, 'Age and height (one child)'); ok(/curve/.test(await txt(p, '.lp-feedback')), 'curved data warning');
  for (let i = 1; i <= 9; i++) for (let j = 0; j < 20; j++) { await p.evaluate(l => [...document.querySelectorAll('[aria-label]')].find(e => e.getAttribute('aria-label') === l).focus(), 'Data point ' + i); await p.keyboard.press('ArrowLeft'); await p.waitForTimeout(30); }
  await w(p); ok(/All x-values are equal/.test(await txt(p, '.readout')), 'vertical stack: no LSRL, no crash'); ok(!p._e.length, 'regression errors ' + p._e); await p.context().close();
  /* random assignment: bias, balance, blocking, randomization test (theory from a 20,000-run NumPy simulation of the same model) */
  p = await open('statistics-random-assignment-lab', 21);
  const runRows = async () => Object.fromEntries((await cells(p))[0].slice(1).map(r => [r[0] + r[1], r]));
  for (const m of ['Students choose', 'Random assignment', 'Randomized pairs (matched on GPA)']) { await chip(p, m); for (let i = 0; i < 6; i++) await btn(p, 'Repeat 100 times'); }
  let rr = await runRows();
  ok(Math.abs(num(rr['Students choose+0'][3]) - 8.6) < 0.5, 'self-selection fakes ≈ +8.6: ' + rr['Students choose+0'][3]);
  ok(Math.abs(num(rr['Random assignment+0'][3])) < 0.5 && Math.abs(num(rr['Random assignment+0'][4]) - 3.06) < 0.35, 'random: centered at 0, SD ≈ 3.06: ' + rr['Random assignment+0'].join(' '));
  ok(Math.abs(num(rr['Randomized pairs+0'][4]) - 1.40) < 0.2, 'pairs SD ≈ 1.40: ' + rr['Randomized pairs+0'][4]);
  await slider(p, 'true-effect', 8); await chip(p, 'Random assignment'); for (let i = 0; i < 6; i++) await btn(p, 'Repeat 100 times'); rr = await runRows();
  ok(Math.abs(num(rr['Random assignment+8'][3]) - 8) < 0.5, 'random: centered at the true effect 8: ' + rr['Random assignment+8'][3]);
  await tab(p, 'Randomization test'); await slider(p, 'true-effect', 0); let small = 0;
  for (let i = 0; i < 40; i++) { await btn(p, 'Run a new experiment'); await btn(p, 'Re-randomize 1,000 times'); const t2 = await txt(p, '.readout'); const m = /(\d+) at least as large → p-value ≈ ([\d.]+)/.exec(t2.replace(/,/g, ''));
    ok(m && Math.abs(+m[1] / 1000 - +m[2]) < 0.0011, 'p-value = count / 1000: ' + (m && m.slice(1))); if (m && +m[2] < 0.05) small++; }
  ok(small <= 6, 'δ = 0: p < 0.05 in at most 6 of 40 experiments (expected ≈ 2): ' + small);
  await slider(p, 'true-effect', 12); let big = 0;
  for (let i = 0; i < 10; i++) { await btn(p, 'Run a new experiment'); await btn(p, 'Re-randomize 1,000 times'); const m = /p-value ≈ ([\d.]+)/.exec(await txt(p, '.readout')); if (m && +m[1] < 0.05) big++; }
  ok(big >= 9, 'δ = 12: p < 0.05 in at least 9 of 10 experiments: ' + big); ok(!p._e.length, 'random assignment errors ' + p._e); await p.context().close();
  await b.close(); srv.close(); console.log(`${pass} checks passed, ${fail} failed`); process.exit(fail ? 1 : 0);
})();
