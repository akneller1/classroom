/* Function Matching Game (match-game.html) in a browser:
   • "Play online" in the printable Matching Card Sort opens exactly the printed cards (every supported unit, Version B);
   • every card in the game is a card of the printable, numbered the same;
   • drag with a mouse, press-and-hold drag on a touch screen, tap a card then a set, number keys, swap, back to tray;
   • Check locks only correct sets, Hint names a misplaced card, finishing shows the summary;
   • zoom window: coordinate read-out, compare panel and "Put in Set"; progress survives a reload.
   Needs Playwright + Chromium:   node worksheet-generator/menu/tests/match-game-browser.cjs */
'use strict';
const assert = require('node:assert/strict');
const http = require('http'), fs = require('fs'), path = require('path');
const pw = process.env.PW ? require(process.env.PW) : require('playwright');
const ROOT = path.resolve(__dirname, '..', '..', '..');
const TYPES = { '.html': 'text/html', '.js': 'text/javascript', '.css': 'text/css', '.svg': 'image/svg+xml', '.woff2': 'font/woff2', '.ttf': 'font/ttf', '.woff': 'font/woff', '.jpg': 'image/jpeg', '.png': 'image/png' };
const server = http.createServer((req, res) => {
  const f = path.join(ROOT, decodeURIComponent(req.url.split('?')[0]));
  if (!f.startsWith(ROOT) || !fs.existsSync(f) || fs.statSync(f).isDirectory()) { res.writeHead(404); return res.end(); }
  res.writeHead(200, { 'content-type': TYPES[path.extname(f)] || 'application/octet-stream' }); fs.createReadStream(f).pipe(res);
});
let n = 0; const ok = name => { n++; };
const UNITS = ['algebra1-linear-equations-slope', 'algebra1-exponential-functions', 'algebra1-quadratics', 'algebra2-functions-transformations', 'algebra2-linear-functions-systems',
  'algebra2-quadratic-functions-complex-numbers', 'algebra2-polynomial-functions', 'algebra2-radicals-rational-exponents', 'algebra2-exponential-logarithmic-functions', 'algebra2-rational-functions', 'algebra2-sequences-series'];
const snap = () => { const B = MKMATCHGAME.state().B; return JSON.stringify({ eq: B.fns.map(f => f.eq), ids: B.ids, desc: B.fns.map(f => f.desc.map(d => d.text)), t: B.fns.map(f => f.table.rows) }); };
(async () => {
  await new Promise(r => server.listen(0, r));
  const base = 'http://localhost:' + server.address().port;
  const browser = await pw.chromium.launch(process.env.CHROME ? { executablePath: process.env.CHROME } : {});
  const page = await browser.newPage({ viewport: { width: 1400, height: 900 } });
  const errs = []; page.on('pageerror', e => errs.push(e.message));

  /* 1. the printable's cards, in every supported unit */
  for (const unit of UNITS) {
    await page.goto(base + '/worksheet-generator/printables.html#unit=' + unit + '&kind=match');
    await page.waitForSelector('#prPlay', { timeout: 20000 });
    await page.selectOption('#prVer', '2'); await page.waitForSelector('[data-ver="1"]'); await page.click('[data-ver="1"]'); await page.waitForSelector('#prPlay');
    const printed = await page.evaluate(() => { const B = MKMENU.printables.app.built()[1]; return JSON.stringify({ eq: B.fns.map(f => f.eq), ids: B.ids, desc: B.fns.map(f => f.desc.map(d => d.text)), t: B.fns.map(f => f.table.rows) }); });
    await page.click('#prPlay'); await page.waitForSelector('#mgBoard .mg-row');
    assert.equal(await page.evaluate(snap), printed, unit + ': Play online opens the printed cards'); ok(unit);
    const counts = await page.evaluate(() => { const s = MKMATCHGAME.state(); return [Object.keys(s.cards).length, s.N, document.querySelectorAll('.mg-row').length]; });
    assert.equal(counts[0], 4 * counts[1]); assert.equal(counts[2], counts[1]); ok(unit + ' cards');
  }

  /* 2. playing */
  const url = base + '/worksheet-generator/match-game.html#unit=algebra1-quadratics&level=cp1&sets=6&fams=quadratic&seed=4242&eq=1&hints=1';
  await page.goto(url); await page.waitForSelector('#mgBoard .mg-row');
  await page.evaluate(() => { localStorage.clear(); }); await page.reload(); await page.waitForSelector('#mgHowOk'); await page.click('#mgHowOk');
  const info = await page.evaluate(() => { const s = MKMATCHGAME.state(); return { cards: s.cards, order: s.order }; });
  const of = (type, si) => Object.values(info.cards).find(c => c.type === type && c.si === si).key;
  const si0 = info.cards[info.order.eq[0]].si, si1 = info.cards[info.order.eq[1]].si;
  const place = () => page.evaluate(() => MKMATCHGAME.state().place);
  // mouse drag
  const g0 = of('graph', si0); await page.locator(`.mg-tray .mg-card[data-key="${g0}"]`).evaluate(e => e.scrollIntoView({ block: 'nearest' })); const src = await page.locator(`.mg-tray .mg-card[data-key="${g0}"]`).boundingBox(), dst = await page.locator('.mg-row[data-row="0"]').boundingBox();
  await page.mouse.move(src.x + 50, src.y + 60); await page.mouse.down(); await page.mouse.move(src.x + 80, src.y + 90, { steps: 4 }); await page.mouse.move(dst.x + 150, dst.y + 60, { steps: 10 });
  assert.ok(await page.$('.mg-ghost') && await page.$('.mg-row.drop-over'), 'drag shows a ghost and the drop target'); await page.mouse.up();
  assert.equal((await place())[g0], 0, 'mouse drag places the card'); ok('drag');
  // tap, then a number key
  const t0 = of('table', si0);
  await page.click('.mg-tab[data-tab="table"]'); await page.click(`.mg-tray .mg-card[data-key="${t0}"]`); await page.keyboard.press('1');
  assert.equal((await place())[t0], 0, 'number key places the selected card'); ok('key');
  // a wrong description by tapping the set
  const dW = of('desc', si1);
  await page.click('.mg-tab[data-tab="desc"]'); await page.click(`.mg-tray .mg-card[data-key="${dW}"]`); await page.click('.mg-row[data-row="0"] header');
  assert.equal((await place())[dW], 0, 'tap card, tap set'); ok('tap');
  await page.click('#mgCheck');
  assert.ok(await page.$('.mg-row[data-row="0"].bad'), 'a wrong set is flagged, not locked'); assert.equal(await page.evaluate(() => !!MKMATCHGAME.state().ok[0]), false); ok('check wrong');
  await page.click('#mgHint'); assert.match(await page.textContent('#mgToast'), new RegExp(info.cards[dW].label + ' does not belong in Set 1')); ok('hint');
  // swap the right description in from the zoom window
  const d0 = of('desc', si0);
  await page.locator(`.mg-tray .mg-card[data-key="${d0}"] .mg-zoom`).click(); await page.waitForSelector('.mg-modal');
  await page.click('.mg-modal [data-cmp="0"]'); assert.match(await page.textContent('.mg-modal [data-put]'), /swap with/); await page.click('.mg-modal [data-put]');
  let pl = await place(); assert.equal(pl[d0], 0); assert.equal(pl[dW], -1, 'the swapped card goes back to the tray'); ok('zoom put + swap');
  await page.click('#mgCheck'); assert.ok(await page.$('.mg-row[data-row="0"].ok.collapsed'), 'a correct set is matched and folds away'); ok('check right');
  // a graph zoom shows coordinates
  await page.click('.mg-tab[data-tab="graph"]'); await page.locator('.mg-tray .mg-card .mg-zoom').first().click();
  const svg = await page.locator('.mg-big svg').boundingBox(); await page.mouse.move(svg.x + svg.width * 0.5 + 1, svg.y + svg.height * 0.5 + 1);
  assert.equal(await page.textContent('.mg-big .mg-ctx'), '(0, 0)', 'read-out at the origin'); await page.keyboard.press('Escape'); assert.equal(await page.$('.mg-modal'), null); ok('zoom read-out');
  // progress survives a reload
  await page.reload(); await page.waitForSelector('#mgBoard .mg-row');
  assert.equal(await page.evaluate(() => !!MKMATCHGAME.state().ok[0]), true, 'saved progress'); ok('saved');
  // finish
  await page.evaluate(() => { const s = MKMATCHGAME.state(); Object.values(s.cards).forEach(c => { if (c.type !== 'eq') MKMATCHGAME.place(c.key, s.order.eq.findIndex(k => s.cards[k].si === c.si)); }); });
  await page.click('#mgCheck'); await page.waitForSelector('.mg-done'); assert.match(await page.textContent('.mg-done'), /All 6 sets matched/); ok('finish');
  // no equations in place: rows start empty and a full correct set still checks
  await page.goto(base + '/worksheet-generator/match-game.html#unit=algebra1-exponential-functions&level=honors&sets=8&fams=exponential,linear&seed=9&eq=0&hints=0');
  await page.waitForSelector('#mgBoard .mg-row');
  assert.equal(await page.$('#mgHint'), null, 'hints can be turned off');
  assert.equal(await page.evaluate(() => Object.values(MKMATCHGAME.state().place).every(r => r === -1)), true, 'every card starts in the tray');
  await page.evaluate(() => { const s = MKMATCHGAME.state(); ['graph', 'eq', 'table', 'desc'].forEach(t => MKMATCHGAME.place(s.order[t].find(k => s.cards[k].si === 3), 2)); });
  await page.click('#mgCheck'); assert.equal(await page.evaluate(() => !!MKMATCHGAME.state().ok[2]), true); ok('eq=0');
  // setup screen without a seed
  await page.goto(base + '/worksheet-generator/match-game.html#unit=algebra2-sequences-series');
  await page.waitForSelector('#suGo'); assert.equal(await page.$$eval('.mgFam', b => b.length), 2); await page.click('#suGo'); await page.waitForSelector('#mgBoard .mg-row');
  assert.match(page.url(), /seed=\d+/); ok('setup');

  /* 3. touch: press and hold, then drag */
  for (const dev of ['iPad (gen 7)', 'Pixel 5']) {
    const ctx = await browser.newContext({ ...pw.devices[dev] }), p = await ctx.newPage();
    p.on('pageerror', e => errs.push(dev + ': ' + e.message));
    await p.goto(url.replace('seed=4242', 'seed=77')); await p.waitForSelector('#mgBoard .mg-row');
    const st = await p.evaluate(() => { const s = MKMATCHGAME.state(); return { cards: s.cards, order: s.order }; });
    const k = Object.values(st.cards).find(c => c.type === 'graph' && c.si === st.cards[st.order.eq[0]].si).key;
    await p.locator('.mg-row[data-row="0"]').scrollIntoViewIfNeeded();
    const d = await p.locator('.mg-row[data-row="0"] .mg-slot[data-type="desc"]').boundingBox();
    await p.locator(`.mg-tray .mg-card[data-key="${k}"]`).evaluate(e => e.scrollIntoView({ block: 'nearest' }));
    const s = await p.locator(`.mg-tray .mg-card[data-key="${k}"]`).boundingBox();
    const cdp = await ctx.newCDPSession(p), tp = (type, x, y) => cdp.send('Input.dispatchTouchEvent', { type, touchPoints: type === 'touchEnd' ? [] : [{ x, y }] });
    const sx = s.x + s.width / 2, sy = s.y + s.height / 2;
    await tp('touchStart', sx, sy); await p.waitForTimeout(320);
    for (let i = 1; i <= 12; i++) { await tp('touchMove', sx + (d.x + 20 - sx) * i / 12, sy + (d.y + 20 - sy) * i / 12); await p.waitForTimeout(16); }
    await tp('touchEnd'); await p.waitForTimeout(80);
    assert.equal(await p.evaluate(key => MKMATCHGAME.state().place[key], k), 0, dev + ': press-and-hold drag'); ok(dev);
    await ctx.close();
  }
  assert.deepEqual(errs, []);
  await browser.close(); server.close();
  console.log('match game browser: ' + n + ' checks passed');
})().catch(e => { console.error(e); process.exit(1); });
