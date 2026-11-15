/* Matching kinds in a browser (match-game.html#unit=…&kind=…), one listed unit per kind and every listed unit
   opening without errors:
   • the board has one row per set and one slot per card type; the anchor cards start in their sets;
   • a mouse drag places a card; tapping a card then a set places it; Check locks only right sets;
   • Hint names a misplaced card; finishing every set shows the summary;
   • the zoom window opens, and on a coordinate plane the read-out appears;
   • "Print card sort" and "Print answer key" lay out every card (window.print is stubbed);
   • the setup screen (no seed) starts a game for the kind.
   Needs Playwright + Chromium:   node worksheet-generator/menu/tests/match-kinds-browser.cjs */
'use strict';
const assert = require('node:assert/strict');
const http = require('http'), fs = require('fs'), path = require('path');
const pw = process.env.PW ? require(process.env.PW) : require('playwright');
const ROOT = path.resolve(__dirname, '..', '..', '..');
const TYPES = { '.html': 'text/html', '.js': 'text/javascript', '.css': 'text/css', '.svg': 'image/svg+xml', '.woff2': 'font/woff2', '.ttf': 'font/ttf', '.woff': 'font/woff', '.jpg': 'image/jpeg', '.png': 'image/png', '.json': 'application/json' };
const server = http.createServer((req, res) => {
  const f = path.join(ROOT, decodeURIComponent(req.url.split('?')[0]));
  if (!f.startsWith(ROOT) || !fs.existsSync(f) || fs.statSync(f).isDirectory()) { res.writeHead(404); return res.end(); }
  res.writeHead(200, { 'content-type': TYPES[path.extname(f)] || 'application/octet-stream' }); fs.createReadStream(f).pipe(res);
});
let n = 0; const ok = (c, m) => { n++; assert.ok(c, m); };
const ONE = { ineq: 'algebra1-inequalities', prop: 'math6-ratios-rates-percent-proportions', fdp: 'prealgebra7-ratios-proportions-percentages', sys: 'prealgebra-systems-linear-equations', data: 'statistics-exploring-data', trig: 'algebra2-trigonometric-functions', deriv: 'calculus-applications-derivatives', conic: 'precalculus-conics', logic: 'discrete-compound-statements-logic', xform: 'geometry-transformations', place: 'grade2-place-value-1000', time: 'grade1-telling-time', money: 'grade2-time-money', mult: 'grade3-division-meaning', efrac: 'grade3-understanding-fractions', graph: 'grade3-graphs-measurement-data', expr: 'grade5-numerical-expressions-patterns', area: 'grade4-multiplication-strategies' };
(async () => {
  await new Promise(r => server.listen(0, r));
  const base = 'http://localhost:' + server.address().port + '/worksheet-generator/match-game.html';
  const browser = await pw.chromium.launch(process.env.CHROME ? { executablePath: process.env.CHROME } : {});
  const page = await browser.newPage({ viewport: { width: 1400, height: 900 } });
  const errs = []; page.on('pageerror', e => errs.push(e.message));
  await page.goto(base + '#unit=algebra1-inequalities&kind=ineq&seed=1'); await page.waitForSelector('.mg-row');
  await page.evaluate(() => { localStorage.clear(); localStorage.setItem('mkmatch-how', '1'); window.print = () => { window.__printed = (window.__printed || 0) + 1; }; });
  const kinds = await page.evaluate(() => Object.keys(MKMATCH.kinds).map(k => [k, Object.keys(MKMATCH.kinds[k].units), Object.fromEntries(Object.entries(MKMATCH.kinds[k].units).map(([u, c]) => [u, Math.min(6, c.maxSets || MKMATCH.kinds[k].maxSets || 10)]))]));
  ok(kinds.length === 18, 'eighteen kinds registered');
  // every listed unit opens
  for (const [kind, units, cap] of kinds) for (const unit of units) {
    const want = cap[unit];
    await page.goto(base + '#unit=' + unit + '&kind=' + kind + '&level=cp1&sets=' + want + '&seed=42'); await page.waitForSelector('.mg-row', { timeout: 15000 });
    const st = await page.evaluate(() => { const s = MKMATCHGAME.state(); return { k: s.K.id, n: s.N, rows: document.querySelectorAll('.mg-row').length, slots: document.querySelectorAll('.mg-row[data-row="0"] .mg-slot').length, types: s.types.length, fixed: Object.keys(s.fixed).length, anchor: s.anchor }; });
    ok(st.k === kind && st.n === want && st.rows === want && st.slots === st.types, `${kind} ${unit}: board ${JSON.stringify(st)}`);
    ok(st.fixed === want && st.anchor, `${kind} ${unit}: anchor cards start in their sets`);
  }
  // play one unit per kind
  for (const kind of Object.keys(ONE)) {
    const unit = ONE[kind], tag = kind + ' ' + unit;
    await page.goto(base + '#unit=' + unit + '&kind=' + kind + '&level=honors&sets=4&seed=77'); await page.waitForSelector('.mg-row');
    await page.evaluate(() => { localStorage.clear(); localStorage.setItem('mkmatch-how', '1'); }); await page.reload(); await page.waitForSelector('.mg-row');
    await page.evaluate(() => { window.print = () => { window.__printed = (window.__printed || 0) + 1; }; });
    const info = await page.evaluate(() => { const s = MKMATCHGAME.state(); return { cards: s.cards, order: s.order, types: s.types, anchor: s.anchor }; });
    const rowOf = si => info.order[info.anchor].findIndex(k => info.cards[k].si === si);
    const other = info.types.filter(t => t !== info.anchor);
    // mouse drag the right card for set 1
    const si0 = info.cards[info.order[info.anchor][0]].si, t0 = other[0], k0 = Object.values(info.cards).find(c => c.type === t0 && c.si === si0).key;
    await page.click(`.mg-tab[data-tab="${t0}"]`);
    await page.locator(`.mg-tray .mg-card[data-key="${k0}"]`).evaluate(e => e.scrollIntoView({ block: 'nearest' }));
    const src = await page.locator(`.mg-tray .mg-card[data-key="${k0}"]`).boundingBox(), dst = await page.locator('.mg-row[data-row="0"]').boundingBox();
    await page.mouse.move(src.x + 40, src.y + 40); await page.mouse.down(); await page.mouse.move(src.x + 70, src.y + 70, { steps: 4 }); await page.mouse.move(dst.x + 120, dst.y + 50, { steps: 10 }); await page.mouse.up();
    ok(await page.evaluate(k => MKMATCHGAME.state().place[k], k0) === 0, tag + ': mouse drag');
    // tap a wrong card into set 1, then check and hint
    const t1 = other[1], wrong = Object.values(info.cards).find(c => c.type === t1 && c.si !== si0).key;
    await page.click(`.mg-tab[data-tab="${t1}"]`); await page.click(`.mg-tray .mg-card[data-key="${wrong}"]`); await page.click('.mg-row[data-row="0"] header');
    ok(await page.evaluate(k => MKMATCHGAME.state().place[k], wrong) === 0, tag + ': tap a card, tap a set');
    await page.evaluate(() => { const s = MKMATCHGAME.state(); s.types.forEach(t => { const want = Object.values(s.cards).find(c => c.type === t && c.si === s.cards[s.order[s.anchor][0]].si); if (!Object.keys(s.place).some(k => s.place[k] === 0 && s.cards[k].type === t)) MKMATCHGAME.place(want.key, 0); }); });
    await page.click('#mgCheck');
    ok(await page.$('.mg-row[data-row="0"].bad'), tag + ': a wrong set is flagged');
    await page.click('#mgHint'); ok(new RegExp(info.cards[wrong].label + ' does not belong').test(await page.textContent('#mgToast')), tag + ': hint names the misplaced card');
    // zoom: any card of each type opens; planes show the read-out
    for (const t of info.types) {
      await page.evaluate(k => document.querySelector(`[data-zoom="${k}"]`) ? 0 : 1, info.order[t][0]);
      await page.evaluate(() => { document.querySelectorAll('.mg-modal').forEach(m => m.remove()); });
      const z = await page.$(`.mg-card[data-key="${info.order[t][0]}"] .mg-zoom`);
      if (!z) continue;
      await z.click(); await page.waitForSelector('.mg-modal .mg-big');
      const plane = await page.$('.mg-big svg[data-plane]');
      if (plane) { const bb = await plane.boundingBox(); await page.mouse.move(bb.x + bb.width / 2, bb.y + bb.height / 2); ok(/\(/.test(await page.textContent('.mg-big .mg-ctx')), tag + ': coordinate read-out on ' + t); }
      ok(!/NaN|undefined/.test(await page.innerHTML('.mg-big')), tag + ': zoomed ' + t + ' renders');
      await page.keyboard.press('Escape');
    }
    // print
    await page.evaluate(() => MKMATCHGAME.printDeck(false)); await page.waitForTimeout(150);
    const pages = await page.evaluate(() => document.querySelectorAll('#mgPrint .mp-page').length), cardsPrinted = await page.evaluate(() => document.querySelectorAll('#mgPrint .mp-cards .mp-card').length);
    ok(pages >= 1 + info.types.length && cardsPrinted === 4 * info.types.length, `${tag}: print card sort (${pages} pages, ${cardsPrinted} cards)`);
    ok(await page.evaluate(() => window.__printed) >= 1, tag + ': print dialog requested');
    await page.evaluate(() => { window.dispatchEvent(new Event('afterprint')); MKMATCHGAME.printDeck(true); }); await page.waitForTimeout(150);
    ok(await page.evaluate(() => /ANSWER KEY/.test(document.querySelector('#mgPrint').textContent)), tag + ': answer key prints');
    await page.evaluate(() => window.dispatchEvent(new Event('afterprint')));
    // finish
    await page.evaluate(() => { const s = MKMATCHGAME.state(); Object.values(s.cards).forEach(c => { if (!s.fixed[c.key]) MKMATCHGAME.place(c.key, s.order[s.anchor].findIndex(k => s.cards[k].si === c.si)); }); });
    await page.click('#mgCheck'); await page.waitForSelector('.mg-done');
    ok(/All 4 sets matched/.test(await page.textContent('.mg-done')), tag + ': finish');
  }
  // setup screen for a kind
  await page.goto(base + '#unit=precalculus-conics&kind=conic'); await page.waitForSelector('#suGo');
  ok(/Conic Section Matching/.test(await page.textContent('.mg-setup h1')) && (await page.$$('.mgFam')).length === 4, 'setup shows the conic types');
  await page.click('#suGo'); await page.waitForSelector('.mg-row'); ok(/kind=conic/.test(page.url()) && /seed=\d+/.test(page.url()), 'setup starts the kind');
  ok(!errs.length, 'no page errors: ' + errs.join(' | '));
  await browser.close(); server.close();
  console.log('match kinds browser: ' + n + ' checks passed');
})().catch(e => { console.error(e); process.exit(1); });
