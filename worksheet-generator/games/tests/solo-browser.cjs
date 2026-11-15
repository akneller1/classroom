/* Plays generated Connect 4 and Tic-Tac-Toe in a real browser, in both modes.
   Two teams: the existing game still works (wins, a miss passes the turn, steals in Tic-Tac-Toe).
   Solo vs. computer: the mode choice appears and is remembered, a miss gives no steal and hands the turn
   to the computer, the computer moves on its own, whole games finish, and the computer starts the next one.
   Needs a static server at BASE (default http://localhost:8765) serving the repository root.
   UNITS=systems,circles by default (folder prefixes). CHANNEL=chrome or msedge selects an installed browser. */
'use strict';
const assert = require('assert');
const { chromium } = require(process.env.PW || 'playwright');
const BASE = process.env.BASE || 'http://localhost:8765';
const UNITS = (process.env.UNITS || 'systems,circles').split(',');
let passed = 0;
function ok(m) { passed++; console.log('  ✓ ' + m); }

(async () => {
  const browser = await chromium.launch(process.env.CHANNEL ? { channel: process.env.CHANNEL } : {});
  for (const unit of UNITS) {
    const page = await browser.newPage({ viewport: { width: 1200, height: 900 } });
    const errors = [];
    page.on('pageerror', e => errors.push(e.message)); page.on('console', m => { if (m.type() === 'error') errors.push(m.text()); });
    const url = g => `${BASE}/artifacts/${unit}-${g}/index.html`;
    const st = () => page.evaluate(() => JSON.parse(JSON.stringify(MKGAMES._state(), (k, v) => (k === 'p' || k === 'it' ? undefined : v))));
    const ready = (sel, timeout) => page.waitForSelector(sel, { timeout: timeout || 60000 });
    const until = (fn, arg) => page.waitForFunction(fn, arg, { timeout: 60000 });
    async function visit(u) { await page.goto(u); await page.locator('dialog.teacher-skills').getByRole('button', { name: 'Continue', exact: true }).click(); }
    const opt = (expr, right) => page.evaluate(([e, r]) => { const S = MKGAMES._state(); const it = eval(e); return it.options.findIndex(o => !!o.ok === r); }, [expr, right]);
    async function fresh(game) { await page.goto(url(game)); await page.evaluate(() => localStorage.clear()); await visit(url(game)); }

    /* ---------- Connect 4, two teams (unchanged behaviour) ---------- */
    await fresh('connect-four'); await ready('#tGo');
    assert.equal(await page.locator('.gm-mode-btn[data-mode="teams"][aria-pressed="true"]').count(), 1, 'two teams is the default');
    assert.ok(await page.locator('#tSolo').isHidden());
    await page.click('#tGo'); await ready('.gm-opt');
    for (let move = 0; move < 7; move++) {
      await page.click(`.gm-opt[data-opt="${await opt('S.it', true)}"]`); await page.click('#c4Lock'); await ready('.c4-board.pick');
      await page.click(`.c4-hole[data-col="${move % 2 === 0 ? 0 : 1}"]`);
      if (move < 6) await page.click('#c4Next');
    }
    await ready('#c4Again'); let S = await st(); assert.equal(S.wins.L, 1); assert.equal(S.solo, false);
    await page.click('#c4Again'); await ready('#c4Lock');
    await page.click(`.gm-opt[data-opt="${await opt('S.it', false)}"]`); await page.click('#c4Lock'); await ready('#c4Steal');
    ok(unit + ' connect four, two teams: still the default; four in a row wins; a miss still offers the steal');

    /* ---------- Connect 4, solo ---------- */
    await visit(url('connect-four')); await ready('#tGo');
    await page.click('.gm-mode-btn[data-mode="solo"]');
    assert.ok(await page.locator('#tTeams').isHidden()); assert.ok(await page.locator('#tSolo').isVisible()); assert.ok(await page.locator('#tRulesSolo').isVisible());
    await page.fill('#tP', 'Ana'); await page.selectOption('#tAI', 'easy'); await page.click('#tGo'); await ready('.gm-opt');
    S = await st(); assert.equal(S.solo, true); assert.equal(S.ai, 'easy'); assert.equal(S.turn, 'L');
    assert.ok((await page.textContent('.tm-sides')).includes('Ana') && (await page.textContent('.tm-sides')).includes('Computer'));
    // a correct answer drops a disc, then the computer moves by itself
    await page.click(`.gm-opt[data-opt="${await opt('S.it', true)}"]`); await page.click('#c4Lock'); await ready('.c4-board.pick');
    await page.click('.c4-hole[data-col="3"]'); await page.click('#c4Next');
    await ready('.gm-spin-sm'); S = await st(); assert.equal(S.phase, 'cpu', 'the computer is thinking');
    assert.equal(await page.locator('.c4-board.pick').count(), 0, 'the board is locked while the computer thinks');
    await until(() => MKGAMES._state().phase === 'q' && MKGAMES._state().turn === 'L');
    S = await st(); const rDiscs = S.board.flat().filter(x => x === 'R').length;
    assert.ok(rDiscs === 1 ? /dropped a disc in column/.test(S.cpuMsg) : /missed its problem/.test(S.cpuMsg), 'the computer reports what it did');
    assert.equal(await page.locator('.gm-cpu').count(), 1, 'the computer move is shown to the student');
    if (rDiscs) assert.equal(await page.locator('.c4-hole.last').count(), 1, 'the computer disc is highlighted');
    // a wrong answer: no steal, no disc, the computer goes next
    await page.click(`.gm-opt[data-opt="${await opt('S.it', false)}"]`); await page.click('#c4Lock'); await ready('#c4Next');
    assert.equal(await page.locator('#c4Steal').count(), 0, 'no steal offer in solo mode');
    assert.equal(await page.locator('.gm-sol').count(), 1, 'the solution is shown after a miss');
    assert.ok((await page.textContent('.gm-msg')).includes('Computer'), 'next up: Computer');
    await page.click('#c4Next'); await until(() => MKGAMES._state().phase === 'q' && MKGAMES._state().turn === 'L');
    // play whole games: the student always answers correctly and plays a sensible column
    let games = 0, sawCpuWin = false, sawCpuStart = false;
    while (games < 2) {
      S = await st();
      if (S.phase === 'over') {
        games++; if (S.answerer === 'R' && S.win) { sawCpuWin = true; assert.ok((await page.textContent('h2')).includes('computer wins')); }
        await page.click('#c4Again');
        await until(() => ['q', 'cpu'].includes(MKGAMES._state().phase));
        if ((await st()).phase === 'cpu' || (await st()).board.flat().some(x => x === 'R') && games === 1) sawCpuStart = true;
        continue;
      }
      if (S.phase === 'q') {
        await page.click(`.gm-opt[data-opt="${await opt('S.it', true)}"]`); await page.click('#c4Lock'); await ready('.c4-board.pick');
        const col = await page.evaluate(() => MKSOLOAI.connectFourMove(MKGAMES._state().board, 'L', 'R', 'hard'));
        await page.click(`.c4-hole[data-col="${col}"]`);
        S = await st(); if (S.phase === 'resolved') await page.click('#c4Next');
      }
      await until(() => ['q', 'over'].includes(MKGAMES._state().phase));
    }
    assert.ok(sawCpuStart, 'the computer starts the second game');
    S = await st(); assert.ok(S.wins.L + S.wins.R >= 1, 'games are counted');
    await page.reload(); await page.locator('dialog.teacher-skills').getByRole('button', { name: 'Continue', exact: true }).click(); await ready('#tGo');
    assert.equal(await page.locator('.gm-mode-btn[data-mode="solo"][aria-pressed="true"]').count(), 1, 'solo is remembered');
    assert.equal(await page.inputValue('#tP'), 'Ana'); assert.equal(await page.inputValue('#tAI'), 'easy');
    ok(unit + ' connect four, solo: computer moves on its own, a miss passes to the computer with no steal, full games finish (wins ' + S.wins.L + '–' + S.wins.R + (sawCpuWin ? ', computer won one' : '') + '), settings remembered');

    /* ---------- Tic-Tac-Toe, two teams (unchanged behaviour) ---------- */
    await fresh('tic-tac-toe'); await ready('#tGo'); await page.click('#tGo'); await ready('.ttt-board');
    for (const sq of [0, 3, 1, 4, 2]) {
      await page.click(`[data-sq="${sq}"]`); await ready('.gm-modal .gm-opt');
      await page.click(`.gm-opt[data-opt="${await opt('S.quiz.it', true)}"]`); await page.click('#tLock'); await ready('#tCont'); await page.click('#tCont');
    }
    await ready('#tAgain'); S = await st(); assert.equal(S.wins.L, 1);
    await page.click('#tAgain'); await page.click('[data-sq="4"]'); await ready('.gm-modal .gm-opt');
    await page.click(`.gm-opt[data-opt="${await opt('S.quiz.it', false)}"]`); await page.click('#tLock'); await ready('.gm-steal');
    ok(unit + ' tic-tac-toe, two teams: three in a row wins; a miss still offers the steal');

    /* ---------- Tic-Tac-Toe, solo ---------- */
    await visit(url('tic-tac-toe')); await ready('#tGo'); await page.click('.gm-mode-btn[data-mode="solo"]'); await page.selectOption('#tAI', 'hard'); await page.click('#tGo'); await ready('.ttt-board');
    S = await st(); assert.equal(S.solo, true); assert.equal(S.turn, 'L');
    await page.click('[data-sq="4"]'); await ready('.gm-modal .gm-opt');
    await page.click(`.gm-opt[data-opt="${await opt('S.quiz.it', false)}"]`); await page.click('#tLock'); await ready('#tCont');
    assert.equal(await page.locator('.gm-steal').count(), 0, 'no steal in solo mode');
    assert.ok((await page.textContent('.gm-modal')).includes('computer goes next'));
    await page.click('#tCont'); await ready('.gm-spin-sm');
    assert.ok(await page.locator('[data-sq="0"]').isDisabled(), 'squares are locked while the computer thinks');
    await until(() => !MKGAMES._state().cpu && MKGAMES._state().turn === 'L');
    S = await st(); assert.ok(S.last >= 0 && /square/.test(S.cpuMsg));
    games = 0; let tttCpuStart = false;
    while (games < 2) {
      S = await st();
      if (S.over) {
        games++; if (S.over === 'R') assert.ok((await page.textContent('.gm-panel')).includes('computer wins'));
        await page.click('#tAgain'); await page.waitForTimeout(50);
        if ((await st()).cpu) tttCpuStart = true;
        await until(() => MKGAMES._state().over || (!MKGAMES._state().cpu && MKGAMES._state().turn === 'L'));
        continue;
      }
      const sq = await page.evaluate(() => MKSOLOAI.ticTacToeMove(MKGAMES._state().b, 'L', 'R', 'hard'));
      await page.click(`[data-sq="${sq}"]`); await ready('.gm-modal .gm-opt');
      await page.click(`.gm-opt[data-opt="${await opt('S.quiz.it', true)}"]`); await page.click('#tLock'); await ready('#tCont'); await page.click('#tCont');
      await until(() => MKGAMES._state().over || (!MKGAMES._state().cpu && MKGAMES._state().turn === 'L'));
    }
    assert.ok(tttCpuStart, 'the computer starts the second game');
    S = await st();
    ok(unit + ' tic-tac-toe, solo: a miss leaves the square open and the computer goes next, the computer moves on its own, full games finish (wins ' + S.wins.L + '–' + S.wins.R + ')');

    assert.deepEqual(errors.filter(e => !/Failed to load resource/.test(e)), [], 'no page errors');   // a missing favicon is not a game error
    await page.close();
  }
  await browser.close();
  console.log(passed + ' solo browser checks passed');
})().catch(e => { console.error(e); process.exit(1); });
