#!/usr/bin/env node
// Calculus audit #15 and #16 (2026-11-18), in a browser: the Related Rates and Particle Motion labs run without errors,
// their readouts give the exact rates, every challenge can be completed, and Calculus Graphing Practice works at
// phone width and grades a correct graph as correct. Usage: node scripts/test-calculus-labs-browser.cjs [site-root, default _site]
'use strict';
const { chromium } = require('playwright'), http = require('http'), fs = require('fs'), path = require('path'), assert = require('assert/strict');
const root = path.resolve(process.argv[2] || '_site');
const mime = { '.js': 'text/javascript', '.css': 'text/css', '.json': 'application/json', '.png': 'image/png', '.svg': 'image/svg+xml', '.html': 'text/html', '.jpg': 'image/jpeg' };
(async () => {
  const server = http.createServer((req, res) => { const p = path.resolve(root, '.' + decodeURIComponent(req.url.split('?')[0])); if (!p.startsWith(root + path.sep)) { res.writeHead(403).end(); return; } try { res.setHeader('content-type', mime[path.extname(p)] || 'application/octet-stream'); res.end(fs.readFileSync(p)); } catch (e) { res.statusCode = 404; res.end(); } }).listen(0);
  let browser;
  try {
    browser = await chromium.launch({ headless: true });
    const page = await browser.newPage({ viewport: { width: 1280, height: 900 } }), errors = [];
    await page.route(/fonts\.(googleapis|gstatic)\.com/, r => r.abort());
    page.on('pageerror', e => errors.push(e.message));
    const base = 'http://localhost:' + server.address().port + '/';
    const set = (id, v) => page.evaluate(([id, v]) => { const e = document.getElementById(id); e.value = v; e.dispatchEvent(new Event('input')); }, [id, v]);
    const chip = label => page.evaluate(l => [...document.querySelectorAll('button.chip')].find(b => b.textContent === l).click(), label);
    const found = () => page.textContent('.challenges-head');
    const read = () => page.textContent('.readout');
    const wait = () => page.waitForTimeout(60);

    await page.goto(base + 'artifacts/calculus-related-rates-lab/index.html'); await page.waitForSelector('.readout');
    await set('sl-foot-x', 5); await wait();
    assert.match(await read(), /y = 12 ft/); assert.match(await read(), /−0\.833 ft\/s/);
    await set('sl-foot-x', 12); await wait(); assert.match(await read(), /−4\.8 ft\/s/);
    for (const x of [11.6, 9.2, 12.9]) { await set('sl-foot-x', x); await wait(); }
    await set('sl-rate', 3); await wait(); await set('sl-foot-x', 9.2); await wait(); await set('sl-rate', 2); await wait();
    await set('sl-foot-x', 5); await wait();
    assert.match(await found(), /5 of 5 found/, 'related rates challenges');
    await chip('10 ft'); await set('sl-rate', 1); await set('sl-foot-x', 6); await wait(); assert.match(await read(), /−0\.75 ft\/s/);
    console.log('PASS Related Rates lab');

    await page.goto(base + 'artifacts/calculus-particle-motion-lab/index.html'); await page.waitForSelector('.readout');
    await set('sl-time-t', 6); await wait();
    let r = await read(); assert.match(r, /x\(6\) = 6 m/); assert.match(r, /displacement[^·]*= 6 m/); assert.match(r, /total distance[^=]*= 15 m/);
    for (const t of [1, 2]) { await set('sl-time-t', t); await wait(); }
    await chip('4 − 2t'); await set('sl-time-t', 4); await wait(); r = await read(); assert.match(r, /x\(4\) = 0 m/); assert.match(r, /total distance[^=]*= 8 m/);
    await set('sl-start-x0', 2); await wait();
    assert.match(await found(), /5 of 5 found/, 'particle motion challenges');
    console.log('PASS Particle Motion lab');

    await page.setViewportSize({ width: 375, height: 812 });
    for (const u of ['derivatives', 'applications-derivatives', 'fundamental-theorem-calculus', 'applications-integrals', 'differential-equations']) {
      await page.goto(base + 'worksheet-generator/plot-practice.html?course=calculus&unit=' + u); await page.waitForSelector('#graph svg');
      assert(await page.evaluate(() => document.documentElement.scrollWidth <= innerWidth), 'mobile overflow ' + u);
      const ok = await page.evaluate(() => { const q = MK_CAL_PLOT.pool(new URLSearchParams(location.search).get('unit'), 'cp1', null, 1)[0], p = q.plot;
        const resp = p.tool === 'line' ? { points: [[0, MK_PLOT.number(p.target.b)], [1, MK_PLOT.number(p.target.m) + MK_PLOT.number(p.target.b)]] } : { points: p.target.points };
        const w = MK_PLOT.create(document.getElementById('graph'), p, { response: resp }); return MK_PLOT.check(p, w.getResponse()).ok; });
      assert(ok, 'graded correct ' + u);
      await page.click('#reveal'); assert(await page.locator('#key-image').evaluate(img => img.complete && img.naturalWidth > 0), 'answer key image ' + u);
      console.log('PASS Calculus graphing practice', u);
    }
    assert.deepEqual(errors, []);
  } finally { if (browser) await browser.close(); server.close(); }
})().catch(e => { console.error(e); process.exitCode = 1; });
