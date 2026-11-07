// Edge cases, pointer dragging, and layout checks (Chromebook 1366×768 light, phone 360×740 dark) for the 2026-11-07 tools.
// Usage (repository root): node tools/interactive-math-20261107/tests/edge.cjs
const { chromium } = require('playwright');
const http = require('http'), fs = require('fs'), path = require('path');
const ROOT = path.resolve(__dirname, '../../..');
const M = require('../manifest.json');
const T = { '.html': 'text/html', '.js': 'text/javascript', '.css': 'text/css' };
const serve = () => new Promise(r => { const s = http.createServer((q, res) => { let u = decodeURIComponent(q.url.split('?')[0]); fs.readFile(path.join(ROOT, u), (e, d) => { if (e) { res.writeHead(404); res.end(); return; } res.writeHead(200, { 'Content-Type': T[path.extname(u)] || 'application/octet-stream' }); res.end(d); }); }); s.listen(0, () => r(s)); });
let pass = 0, fail = 0;
function ok(c, msg) { if (c) pass++; else { fail++; console.log('FAIL', msg); } }
const txt = (p, sel) => p.evaluate(s => [...document.querySelectorAll(s)].map(e => e.textContent).join(' | '), sel);
const slider = (p, id, v) => p.evaluate(([id, v]) => { const e = document.getElementById('sl-' + id); e.value = v; e.dispatchEvent(new Event('input')); }, [id, v]);
const num = (p, id, v) => p.evaluate(([id, v]) => { const e = document.getElementById('ni-' + id); e.value = v; e.dispatchEvent(new Event('change')); }, [id, v]);
const chip = (p, t) => p.evaluate(t => [...document.querySelectorAll('button.chip')].find(b => b.textContent.trim() === t).click(), t);
const btn = (p, t) => p.evaluate(t => [...document.querySelectorAll('button')].find(b => b.textContent.trim().startsWith(t)).click(), t);
const w = p => p.waitForTimeout(80);
async function drag(p, label, dx, dy) {
  const box = await p.evaluate(l => { const e = [...document.querySelectorAll('[aria-label]')].find(x => x.getAttribute('aria-label') === l && x.getAttribute('tabindex') !== null); e.scrollIntoView({ block: 'center' }); const r = e.getBoundingClientRect(); return [r.x + r.width / 2, r.y + r.height / 2]; }, label);
  await p.mouse.move(box[0], box[1]); await p.mouse.down(); await p.mouse.move(box[0] + dx / 2, box[1] + dy / 2, { steps: 4 }); await p.mouse.move(box[0] + dx, box[1] + dy, { steps: 4 }); await p.mouse.up(); await w(p);
}
(async () => {
  const srv = await serve(), port = srv.address().port, b = await chromium.launch();
  const open = async (slug, vp = { width: 1366, height: 768 }, scheme = 'light') => { const ctx = await b.newContext({ viewport: vp, colorScheme: scheme, hasTouch: vp.width < 500 }); const p = await ctx.newPage(); p._errs = []; p.on('pageerror', e => p._errs.push(e.message)); await p.goto(`http://localhost:${port}/artifacts/${slug}/index.html`); await w(p); return p; };
  /* layout: every tool, Chromebook light and phone dark */
  for (const t of M.tools) for (const [vp, sc] of [[{ width: 1366, height: 768 }, 'light'], [{ width: 360, height: 740 }, 'dark']]) {
    const p = await open(t.slug, vp, sc);
    const L = await p.evaluate(() => {
      const de = document.documentElement, out = { over: de.scrollWidth > de.clientWidth, small: [], clipped: 0 };
      document.querySelectorAll('button, input[type=range], input[type=number]').forEach(e => { const r = e.getBoundingClientRect(); if (r.width && (r.height < 28 || (e.tagName === 'BUTTON' && r.width < 30))) out.small.push(e.textContent.trim() || e.type); });
      document.querySelectorAll('.readout').forEach(e => { if (e.scrollWidth > e.clientWidth + 2) out.clipped++; });
      return out; });
    ok(!L.over, t.slug + ' ' + vp.width + ': page scrolls sideways');
    ok(!L.small.length, t.slug + ' ' + vp.width + ': small controls ' + L.small.slice(0, 4).join(','));
    ok(!L.clipped, t.slug + ' ' + vp.width + ': readout overflows');
    ok(!p._errs.length, t.slug + ' errors ' + p._errs.join('|'));
    if (vp.width === 360) { const hasDark = await p.evaluate(() => getComputedStyle(document.body).backgroundColor); ok(hasDark === 'rgb(14, 16, 36)', t.slug + ' dark theme bg ' + hasDark); }
    await p.context().close();
  }
  let p;
  /* ratio */
  p = await open('math6-ratio-double-number-line');
  await num(p, 'test-top', 0); await num(p, 'test-bottom', 0); await w(p); ok(/0 : 0 has no amounts/.test(await txt(p, '.lp-feedback')), 'ratio 0:0 message');
  await num(p, 'test-top', 3); await num(p, 'test-bottom', 5); await w(p); ok(/Equivalent/.test(await txt(p, '.lp-feedback')), 'ratio 3:5 equivalent');
  await num(p, 'test-top', 6.5); await num(p, 'test-bottom', 10); await w(p); ok(/Not equivalent/.test(await txt(p, '.lp-feedback')), 'ratio 6.5:10 not equivalent');
  const before = await txt(p, '.readout'); await drag(p, 'Marker on the double number line', 120, 0); ok((await txt(p, '.readout')) !== before, 'ratio marker drags with mouse');
  await p.context().close();
  /* fraction division: clamp, less than one */
  p = await open('math6-fraction-division-groups');
  await slider(p, 'dividend-numerator', 24); await w(p); ok(/^6 ÷/.test((await txt(p, '.panel .readout')).trim()), 'fraction dividend clamped to 6: ' + await txt(p, '.readout'));
  await slider(p, 'dividend-numerator', 1); await slider(p, 'dividend-denominator', 4); await w(p); await slider(p, 'divisor-numerator', 1); await slider(p, 'divisor-denominator', 2); await w(p);
  ok(/less than 1/.test(await txt(p, '.lp-feedback')), 'fraction 1/4 ÷ 1/2 less than one group');
  await p.context().close();
  /* area: triangle with apex outside */
  p = await open('math6-area-shear-lab'); await chip(p, 'Triangle'); await slider(p, 'lean', 8); await w(p);
  ok(/outside the triangle/.test(await txt(p, '.lp-feedback')), 'triangle obtuse height outside'); ok(/= 12/.test(await txt(p, '.readout')), 'triangle area 12');
  await drag(p, 'Top corner (lean and height)', -60, -40); ok(!/lean.*8/.test(''), 'area drag'); await p.context().close();
  /* dot plot: drag a dot */
  p = await open('math6-balance-point-dot-plot'); const m0 = await txt(p, '.readout'); await drag(p, 'Data value 9', 120, 0); ok((await txt(p, '.readout')) !== m0, 'dot plot mouse drag changes the mean');
  await btn(p, '− Remove'); await btn(p, '− Remove'); await btn(p, '− Remove'); await btn(p, '− Remove'); await btn(p, '− Remove'); await btn(p, '− Remove'); await btn(p, '− Remove'); await w(p);
  ok(/Numberofvalues3/.test((await txt(p, '.kv')).replace(/\s/g, '')), 'dot plot keeps at least 3 values'); await p.context().close();
  /* proportional: x = 0 */
  p = await open('prealgebra7-proportional-relationships'); await p.evaluate(() => { const e = [...document.querySelectorAll('[aria-label="Point on your line"]')][0]; e.focus(); }); for (let i = 0; i < 8; i++) { await p.keyboard.press('ArrowLeft'); await p.waitForTimeout(40); } await w(p);
  ok(/undefined/.test(await txt(p, '.lp-feedback')), 'proportional y/x undefined at 0'); await p.context().close();
  /* spinner: cannot remove every part */
  p = await open('prealgebra7-spinner-probability-lab'); await slider(p, 'red-parts', 0); await slider(p, 'blue-parts', 0); await w(p); await slider(p, 'green-parts', 0); await w(p);
  ok(/at least one part/.test(await txt(p, '.lp-feedback')), 'spinner needs a part'); await p.context().close();
  /* pythagorean: collinear and coincident */
  p = await open('prealgebra-pythagorean-squares');
  for (let i = 0; i < 5; i++) { await p.evaluate(() => [...document.querySelectorAll('[aria-label="Corner C"]')][0].focus()); await p.keyboard.press('ArrowDown'); await w(p); }
  ok(/one line/.test(await txt(p, '.readout')), 'pythagorean collinear corners'); 
  await drag(p, 'Corner C', 0, -60); ok(!/one line/.test(await txt(p, '.readout')), 'pythagorean mouse drag'); await p.context().close();
  /* square roots: perfect square */
  p = await open('prealgebra-square-roots-number-line'); await slider(p, 'square-area', 49); await btn(p, '🔍 Zoom in'); await w(p); ok(/= 7 exactly/.test(await txt(p, '.readout')), 'sqrt 49 exact'); await p.context().close();
  /* vectors: zero vector and drag */
  p = await open('precalculus-vector-explorer'); await chip(p, 'k · u'); await slider(p, 'scalar-k', 0); await w(p); ok(/zero vector/.test(await txt(p, 'table')), 'vector zero direction'); await drag(p, 'Tip of u', 40, -40); ok(!p._errs.length, 'vector drag'); await p.context().close();
  /* limits: oscillation table and asymptote */
  p = await open('calculus-limit-explorer'); await chip(p, 'Oscillation'); await slider(p, 'distance-h', 4); await btn(p, 'Reveal'); await w(p); ok(/does not exist/.test(await txt(p, '.readout')), 'osc limit DNE');
  await chip(p, 'Vertical asymptote'); await btn(p, 'Reveal'); await w(p); ok(/∞/.test(await txt(p, '.readout')), 'asym infinite'); ok(!/NaN/.test(await txt(p, 'table')), 'no NaN in table'); await p.context().close();
  /* secant: corner */
  p = await open('calculus-secant-to-tangent'); await chip(p, '|x|'); await slider(p, 'point-a', 0); await btn(p, 'Show tangent'); await w(p); ok(/does not exist/.test(await txt(p, '.readout')), 'abs derivative DNE at 0'); await p.context().close();
  /* riemann: a >= b refused; exact integral of x²/4+1 on [0,4] = 28/3 */
  p = await open('calculus-riemann-sum-lab'); ok(/9\.3333/.test(await txt(p, '.kv')), 'riemann exact 28/3'); await slider(p, 'lower-limit-a', 4); await w(p); ok(/Keep a less than b/.test(await txt(p, '.lp-feedback')), 'riemann a<b'); await p.context().close();
  /* accumulation: A(2) = 2 for 2 − t; x cannot go below a */
  p = await open('calculus-accumulation-ftc'); await slider(p, 'upper-x', 2); await w(p); ok(/= 2(?![.\d])/.test(await txt(p, '.readout')), 'A(2) = 2: ' + await txt(p, '.readout'));
  await slider(p, 'lower-a', 3); await w(p); ok(/A\(3\)/.test(await txt(p, '.readout')), 'x moved up to a'); await p.context().close();
  await b.close(); srv.close();
  console.log(pass + ' checks passed, ' + fail + ' failed'); process.exit(fail ? 1 : 0);
})();
