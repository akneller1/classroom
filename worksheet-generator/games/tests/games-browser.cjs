/* Plays every generated game in a real browser.
   Needs a static server at BASE (default http://localhost:8765) serving the repository root.
   UNITS=relations-functions (folder prefix) by default; several can be given, comma-separated. */
'use strict';
const assert = require('assert');
const { chromium } = require(process.env.PW || 'playwright');
const BASE = process.env.BASE || 'http://localhost:8765';
const UNITS = (process.env.UNITS || "foundations-algebra,solving-equations,linear-inequalities,relations-functions,exponential-functions,factoring-zero-product,statistics-data-modeling,linear-functions,systems,exponents,polynomials,quadratic-practice").split(',');
let passed = 0;
function ok(m) { passed++; console.log('  ✓ ' + m); }

(async () => {
  const browser = await chromium.launch();
  for (const unit of UNITS) {
    const page = await browser.newPage({ viewport: { width: 1200, height: 900 } });
    const errors = [];
    page.on('pageerror', e => errors.push(e.message)); page.on('console', m => { if (m.type() === 'error') errors.push(m.text()); });
    const url = g => `${BASE}/artifacts/${unit}-${g}/index.html`;
    const st = () => page.evaluate(() => JSON.parse(JSON.stringify(MKGAMES._state(), (k, v) => (k === 'p' ? undefined : v))));
    const ready = sel => page.waitForSelector(sel, { timeout: 60000 });
    // the index of the correct option, read from the game's own state (never from the page)
    const rightOpt = expr => page.evaluate(e => { const S = MKGAMES._state(); const it = eval(e); return it.options.findIndex(o => o.ok); }, expr);
    const wrongOpt = expr => page.evaluate(e => { const S = MKGAMES._state(); const it = eval(e); return it.options.findIndex(o => !o.ok); }, expr);

    /* ---- flashcards ---- */
    await page.goto(url('flashcards')); await ready('#fcCard');
    let S = await st(); const nSkills = new Set(S.cards.map(c => c.skill)).size; assert.equal(S.cards.length % (3 * nSkills), 0, 'a CP1 deck has every skill at three difficulties'); assert.ok(S.cards.length >= 20); assert.ok(nSkills >= 3);
    assert.deepEqual([...new Set(S.cards.map(c => c.c))].sort(), [3, 4, 5]);
    assert.equal(await page.locator('.gm-sol').count(), 0, 'the answer is hidden on the question side');
    await page.keyboard.press(' '); await ready('.gm-sol');
    await page.keyboard.press('2'); S = await st(); assert.equal(Object.values(S.rate).filter(v => v === 'got').length, 1);
    await page.keyboard.press(' '); await page.keyboard.press('1'); S = await st(); assert.equal(Object.values(S.rate).filter(v => v === 'need').length, 1);
    await page.click('#fcMissed'); S = await st(); assert.equal(S.order.length, 1, 'practice missed shows only the missed card');
    await page.selectOption('#fcLevel', 'honors'); await ready('#fcCard'); S = await st();
    assert.deepEqual([...new Set(S.cards.map(c => c.c))].sort(), [5, 6, 7]);
    await page.reload(); await ready('#fcCard'); S = await st(); assert.equal(S.level, 'honors', 'the level is remembered');
    ok(unit + ' flashcards: ' + S.cards.length + ' verified cards per level, flip, rate, practice missed, level change');

    /* ---- showdown ---- */
    await page.goto(url('showdown')); await ready('.sd-cell[data-cell]');
    const cells = await page.locator('.sd-cell[data-cell]').count(), ncat = await page.locator('.sd-cat').count(); assert.equal(cells, 5 * ncat, 'board filled (' + cells + ')'); assert.ok(ncat >= 3);
    await page.click('.sd-cell[data-cell="0,4"]'); await ready('.sd-q');
    assert.equal(await page.locator('.gm-sol').count(), 0);
    await page.click('#sdOpts'); assert.equal(await page.locator('.gm-opt.right').count(), 0, 'choices do not give the answer away');
    await page.keyboard.press(' '); await ready('.gm-sol'); assert.equal(await page.locator('.gm-opt.right').count(), 1);
    await page.click('[data-aw="1"][data-s="1"]'); S = await st(); assert.equal(S.score[1], 500);
    await page.keyboard.press('Escape'); await ready('.sd-board');
    assert.ok(await page.locator('.sd-cell[data-cell="0,4"]').isDisabled(), 'a used value is closed');
    if (unit === UNITS[0]) {   // teams: add up to eight, then the button turns off
      for (let k = 0; k < 10; k++) if (!(await page.isDisabled('#sdAddT'))) await page.click('#sdAddT');
      assert.equal(await page.locator('.sd-team').count(), 8, 'up to eight teams'); assert.ok(await page.isDisabled('#sdAddT'));
      for (let k = 0; k < 6; k++) await page.click('#sdRemT');
    }
    ok(unit + ' showdown: ' + ncat + '×5 board by category, choices and answer on demand, scoring, used cells close');

    /* ---- connect four ---- */
    await page.goto(url('connect-four')); await page.click('#tGo'); await ready('.gm-opt');
    for (let move = 0; move < 7; move++) {
      const r = await rightOpt('S.it');
      await page.click(`.gm-opt[data-opt="${r}"]`); await page.click('#c4Lock'); await ready('.c4-board.pick');
      await page.click(`.c4-hole[data-col="${move % 2 === 0 ? 0 : 1}"]`);
      if (move < 6) await ready('#c4Lock');
    }
    await ready('#c4Again'); S = await st(); assert.equal(S.wins.L, 1, 'four in a column wins');
    assert.equal(await page.locator('.c4-hole.win').count(), 4);
    await page.click('#c4Again'); await ready('#c4Lock');
    let w = await wrongOpt('S.it'); await page.click(`.gm-opt[data-opt="${w}"]`); await page.click('#c4Lock'); await ready('#c4Next');
    assert.equal(await page.locator('.gm-opt.right').count(), 1); assert.equal(await page.locator('.gm-sol').count(), 1);
    await page.click('#c4Next'); await ready('#c4Lock'); S = await st(); assert.equal(S.turn, 'L', 'after a miss the turn passes (Right started this game)');
    ok(unit + ' connect four: correct answers drop discs, four in a row wins, a miss shows the solution and passes the turn');

    /* ---- tic-tac-toe ---- */
    await page.goto(url('tic-tac-toe')); await page.click('#tGo'); await ready('.ttt-board');
    for (const sq of [0, 3, 1, 4, 2]) {
      await page.click(`[data-sq="${sq}"]`); await ready('.gm-modal');
      const r = await rightOpt('S.quiz.it'); await page.click(`.gm-opt[data-opt="${r}"]`); await page.click('#tLock'); await ready('#tCont'); await page.click('#tCont');
    }
    await ready('#tAgain'); S = await st(); assert.equal(S.wins.L, 1, 'three in a row wins');
    await page.click('#tAgain'); await page.click('[data-sq="4"]'); await ready('.gm-modal');
    S = await st(); const nOpts = (await page.evaluate(() => MKGAMES._state().quiz.it.options.length));
    w = await wrongOpt('S.quiz.it'); await page.click(`.gm-opt[data-opt="${w}"]`); await page.click('#tLock');
    if (nOpts > 2) { await ready('.gm-steal'); assert.ok(await page.locator(`.gm-opt[data-opt="${w}"]`).isDisabled(), 'the wrong choice is crossed out for the steal');
      const r = await rightOpt('S.quiz.it'); await page.click(`.gm-opt[data-opt="${r}"]`); await page.click('#tLock'); await ready('#tCont');
      S = await st(); assert.equal(S.b[4], 'L', 'the other team stole the square'); }
    ok(unit + ' tic-tac-toe: squares by correct answers, three in a row wins, wrong answers open a steal');

    /* ---- picture reveal ---- */
    await page.goto(url('picture-reveal')); await ready('.pr-pic');
    S = await st(); assert.equal(S.items.length, 10);
    const typedCount = S.items.filter(i => i.typed).length; assert.ok(typedCount >= 6, 'most questions are typed (' + typedCount + ')');
    for (let k = 0; k < 10; k++) {
      await page.click(`[data-q="${k}"]`);
      const info = await page.evaluate(k => { const it = MKGAMES._state().items[k]; return { typed: it.typed, key: it.typed ? MKGAMES.keyTyped(it) : null, r: it.options.findIndex(o => o.ok), w: it.options.findIndex(o => !o.ok), wtyped: it.typed ? (it.typed === 'percent' ? it.options.find(o => !o.ok).a : MKGAMES.typedForm({ answer: it.options.find(o => !o.ok).a })) : null }; }, k);
      if (info.typed) {
        if (k === 0) { await page.fill('#prIn', info.wtyped); await page.click('#prCheck'); assert.match(await page.textContent('.gm-msg'), /Not quite/); }
        await page.fill('#prIn', info.key); await page.click('#prCheck');
      } else { await page.click(`.gm-opt[data-opt="${info.r}"]`); await page.click('#prCheck'); }
      assert.match(await page.textContent('.gm-msg'), /Correct/, 'question ' + (k + 1) + ' (' + (info.typed || 'choice') + ': ' + info.key + ')');
    }
    assert.equal(await page.locator('.pr-tile.gone').count(), 10, 'the whole picture is uncovered');
    ok(unit + ' picture reveal: 10 questions (' + typedCount + ' typed, checked by the verifier), wrong answers rejected, every piece uncovers');

    assert.deepEqual(errors, [], 'page errors: ' + errors.join('\n'));
    await page.close();
  }
  await browser.close();
  console.log('PASS: ' + passed + ' game checks');
})().catch(e => { console.error(e); process.exit(1); });
