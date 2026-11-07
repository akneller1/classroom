// Checks the fixes made to existing Interactive Math tools in this update (built from tools/interactive-math-20261105/src).
// Usage (repository root): node tools/interactive-math-20261107/tests/revised-tools.cjs
const { chromium } = require('playwright');
const http = require('http'), fs = require('fs'), path = require('path');
const ROOT = path.resolve(__dirname, '../../..');
const serve = () => new Promise(r => { const s = http.createServer((q, res) => { const u = decodeURIComponent(q.url.split('?')[0]); fs.readFile(path.join(ROOT, u), (e, d) => { if (e) { res.writeHead(404); res.end(); return; } res.writeHead(200, { 'Content-Type': u.endsWith('.html') ? 'text/html' : u.endsWith('.css') ? 'text/css' : 'text/javascript' }); res.end(d); }); }); s.listen(0, () => r(s)); });
let pass = 0, fail = 0; const ok = (c, m) => { if (c) pass++; else { fail++; console.log('FAIL', m); } };
const w = p => p.waitForTimeout(70);
const slider = async (p, id, v) => { await p.evaluate(([id, v]) => { const e = document.getElementById('sl-' + id); e.value = v; e.dispatchEvent(new Event('input')); }, [id, v]); await w(p); };
const click = async (p, sel, t) => { await p.evaluate(([s, t]) => { const b = [...document.querySelectorAll(s)].find(b => b.textContent.trim() === t || b.textContent.trim().startsWith(t)); if (!b) throw new Error('no ' + t); b.click(); }, [sel, t]); await w(p); };
const txt = (p, s) => p.evaluate(s => [...document.querySelectorAll(s)].map(e => e.textContent).join(' | '), s);
const done = p => p.evaluate(() => [...document.querySelectorAll('.challenges li')].map(l => l.classList.contains('done')));
const keys = async (p, label, k, n) => { for (let i = 0; i < n; i++) { await p.evaluate(l => [...document.querySelectorAll('[aria-label]')].find(e => e.getAttribute('aria-label') === l && e.getAttribute('tabindex') !== null).focus(), label); await p.keyboard.press(k); await p.waitForTimeout(30); } await w(p); };
(async () => {
  const srv = await serve(), port = srv.address().port, b = await chromium.launch();
  const open = async slug => { const p = await b.newPage({ viewport: { width: 1280, height: 900 } }); p._e = []; p.on('pageerror', e => p._e.push(e.message)); await p.goto(`http://localhost:${port}/artifacts/${slug}/index.html`); await w(p); return p; };
  let p;
  p = await open('algebra2-asymptote-hole-explorer');
  await slider(p, 'N0', 2); let t = (await txt(p, '.kv')).replace(/\s/g, ''); ok(/Holes\(2,1\)/.test(t) && /Verticalasymptotesnone/.test(t), 'simple hole at 2: ' + t);
  await p.evaluate(() => document.querySelectorAll('.chips')[3].querySelectorAll('button')[0].click()); await slider(p, 'D1', 2);
  t = (await txt(p, '.kv')).replace(/\s/g, ''); ok(/Holesnone/.test(t) && /Verticalasymptotesx=2/.test(t), '(x−2)/(x−2)² has an asymptote at 2, not a hole: ' + t);
  await p.evaluate(() => document.querySelectorAll('.chips')[1].querySelectorAll('button')[0].click()); await slider(p, 'N1', 2);
  t = (await txt(p, '.kv')).replace(/\s/g, ''); ok(/Holes\(2,1\)/.test(t), '(x−2)²/(x−2)² is 1 with a hole: ' + t);
  await p.evaluate(() => document.querySelectorAll('.chips')[3].querySelectorAll('button')[1].click()); await w(p);
  t = (await txt(p, '.kv')).replace(/\s/g, ''); ok(/Holes\(2,0\)/.test(t) && /x-interceptsnone/.test(t), '(x−2)²/(x−2): hole at (2, 0) is not an x-intercept: ' + t);
  ok(!p._e.length, 'asymptote errors'); await p.close();

  p = await open('algebra2-zeros-multiplicity-builder');
  ok(!(await done(p))[0], 'zeros: bounce not done at start'); await slider(p, 'z1', -3); t = await txt(p, '.kv');
  ok(/bounces/.test(t) && /multiplicity 2/.test(t), 'coincident zeros combine: ' + t); ok((await done(p))[0], 'zeros: bounce challenge'); await p.close();

  p = await open('algebra2-exponential-log-mirror');
  await slider(p, 'base', 1.4); ok(!(await done(p))[2], 'exp: needs both bases'); await slider(p, 'base', 1.45); ok((await done(p))[2], 'exp: bracketing bases challenge'); await p.close();

  p = await open('algebra2-discriminant-roots-explorer');
  ok(!(await done(p)).some(Boolean), 'discriminant: nothing done at start'); await slider(p, 'b', -5); await slider(p, 'c', 4); ok((await done(p))[0], 'discriminant: two roots with c > 0'); await p.close();

  p = await open('polynomials-factoring-area-model-multiplier');
  ok(!(await done(p)).some(Boolean), 'area model: nothing done at start'); await slider(p, 'b', 2); await slider(p, 'd', 3); ok((await done(p))[0], 'area model: (x+2)(x+3)'); await p.close();

  p = await open('algebra2-probability-simulation-lab');
  ok(!(await done(p)).some(Boolean), 'probability: nothing done at start');
  for (let i = 0; i < 60 && !(await done(p))[0]; i++) { await click(p, 'button', 'Start over'); await click(p, 'button', 'Flip 10'); }
  ok((await done(p))[0], 'probability: small-sample challenge');
  await click(p, 'button.tab', 'Sum of two dice'); for (let i = 0; i < 30 && !(await done(p))[2]; i++) await click(p, 'button', 'Roll 1,000');
  ok((await done(p))[2], 'probability: share of 7s within 0.01');
  await click(p, 'button.tab', 'Normal curve'); await click(p, 'button.chip', '2σ'); ok(!(await done(p))[4], 'probability: one σ is not enough'); await slider(p, 'sd', 12); ok((await done(p))[4], 'probability: 2σ with two σ values'); await p.close();

  p = await open('geometry-dilation-similarity-lab');
  /* the starting center may change between versions, so read it and move by the difference */
  const centerO = async () => { const t = (await txt(p, '.readout')).replace(/\s/g, '').replace(/−/g, '-'); const m = /centeredatO\((-?\d+),(-?\d+)\)/.exec(t); return m ? [+m[1], +m[2]] : [0, 0]; };
  const moveO = async (x, y) => { const o = await centerO(); if (x !== o[0]) await keys(p, 'Center O', x > o[0] ? 'ArrowRight' : 'ArrowLeft', Math.abs(x - o[0])); if (y !== o[1]) await keys(p, 'Center O', y > o[1] ? 'ArrowUp' : 'ArrowDown', Math.abs(y - o[1])); };
  await slider(p, 'k', 1.5); await moveO(-3, -2);
  t = (await txt(p, '.readout')).replace(/\s/g, ''); ok(t.indexOf('(x,y)→(−3+32(x+3),−2+32(y+2))') === 0 && /O\(−3,−2\)/.test(t), 'dilation rule about O(−3, −2): ' + t);
  ok(!/→ \(1.5x, 1.5y\)/.test(t), 'dilation: no origin-only rule');
  await moveO(2, 2); await slider(p, 'k', 0.5);
  ok((await done(p))[1], 'dilation: reduction inside the triangle');
  await moveO(10, 10); ok((await done(p))[4], 'dilation: image apart from original');
  await moveO(0, 0); t = (await txt(p, '.readout')).replace(/\s/g, ''); ok(t.indexOf('(x,y)→(12x,12y)') === 0 && /centeredattheorigin/.test(t), 'dilation at origin: ' + t);
  ok(!p._e.length, 'dilation errors ' + p._e); await p.close();

  p = await open('geometry-solids-volume-lab');
  ok(!(await done(p))[2], 'solids: scale not done at start'); await slider(p, 'k', 3); ok((await done(p))[2], 'solids: k = 3'); await p.close();

  p = await open('algebra2-unit-circle-sine-wave');
  ok(!(await done(p)).some(Boolean), 'unit circle: nothing done at start');
  await click(p, 'button.tab', 'What is a radian?'); await slider(p, 'radians', 1); ok((await done(p))[3], 'unit circle: 1 radian'); ok(/57\.3°/.test(await txt(p, '.readout')), '1 rad ≈ 57.3°');
  await slider(p, 'radius', 3); ok((await done(p))[4], 'unit circle: radius change'); t = await txt(p, '.kv'); ok(/3 × 1 = 3/.test(t), 'arc length s = rθ: ' + t);
  await click(p, 'button.tab', 'Transform the wave'); await slider(p, 'B', 2); await slider(p, 'A', 2); await slider(p, 'D', 1); ok((await done(p))[5], 'unit circle: period π, max 3');
  await click(p, 'button.tab', 'Unit circle to wave'); ok(await p.evaluate(() => !document.querySelector('svg[aria-label="Unit circle"]').closest('div').hidden), 'unit circle tab restores');
  ok(!p._e.length, 'unit circle errors ' + p._e); await p.close();
  await b.close(); srv.close(); console.log(pass + ' checks passed, ' + fail + ' failed'); process.exit(fail ? 1 : 0);
})();
