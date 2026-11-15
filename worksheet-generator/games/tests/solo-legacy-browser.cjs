/* Plays the hand-built Algebra 2 Connect 4 and Tic-Tac-Toe pages (solo-legacy.js) in a real browser.
   Two teams still steal; solo mode has no steals, the computer moves by itself, and whole games finish.
   Needs a static server at BASE (default http://localhost:8765) serving the repository root.
   CHANNEL=chrome or msedge selects an installed browser. */
'use strict';
const assert = require('assert');
const { chromium } = require(process.env.PW || 'playwright');
const BASE = process.env.BASE || 'http://localhost:8765';
const UNITS = (process.env.UNITS || 'exponential-logarithmic-functions,functions-transformations,linear-functions-systems,quadratic-functions-complex-numbers').split(',');
let passed = 0;
function ok(m) { passed++; console.log('  ✓ ' + m); }

(async () => {
  const browser = await chromium.launch(process.env.CHANNEL ? { channel: process.env.CHANNEL } : {});
  for (const unit of UNITS) {
    const page = await browser.newPage({ viewport: { width: 1200, height: 900 } });
    const errors = [];
    page.on('pageerror', e => errors.push(e.message)); page.on('console', m => { if (m.type() === 'error') errors.push(m.text()); });
    const url = g => `${BASE}/artifacts/${unit}-${g}/index.html`;
    const until = (fn, arg) => page.waitForFunction(fn, arg, { timeout: 60000 });
    async function open(g) { await page.goto(url(g)); await page.evaluate(() => localStorage.clear()); await page.goto(url(g)); await page.locator('dialog.teacher-skills').getByRole('button', { name: 'Continue', exact: true }).click(); }

    /* ---------- Connect 4 ---------- */
    await open('connect-four'); await until(() => G.phase === 'question');
    const c4choice = right => page.evaluate(r => G.p.choices.findIndex(c => !!c.correct === r), right);
    assert.equal(await page.inputValue('#soloSel'), 'teams', 'two teams is the default');
    await page.click(`.choice[data-i="${await c4choice(false)}"]`); await until(() => G.phase === 'steal-offer');
    ok(unit + ' connect four, two teams: a miss still offers the steal');
    await page.selectOption('#soloSel', 'medium'); await until(() => G.phase === 'question' || G.phase === 'cpu');
    assert.ok(await page.locator('#name1').isDisabled()); assert.equal(await page.inputValue('#name1'), 'Computer');
    let missChecked = false, games = 0, cpuMoves = 0;
    while (games < 2) {
      const ph = await page.evaluate(() => G.phase);
      if (ph === 'over') { games++; await page.click('[data-act="again"]'); await until(() => ['question', 'cpu'].includes(G.phase)); continue; }
      if (ph === 'cpu') { cpuMoves++; await until(() => G.phase !== 'cpu'); continue; }
      if (ph === 'question') {
        if (!missChecked) {
          await page.click(`.choice[data-i="${await c4choice(false)}"]`);
          assert.equal(await page.evaluate(() => G.phase), 'resolved', 'no steal in solo');
          assert.equal(await page.locator('[data-act="steal"]').count(), 0);
          assert.ok((await page.textContent('#q')).includes('Computer'));
          missChecked = true; await page.click('[data-act="next"]'); continue;
        }
        await page.click(`.choice[data-i="${await c4choice(true)}"]`); await until(() => G.phase === 'drop');
        const col = await page.evaluate(() => MKSOLOAI.connectFourMove(G.board, 0, 1, 'hard'));
        await page.click(`#board .col[data-c="${col}"]`);
        if (await page.evaluate(() => G.phase) === 'resolved') await page.click('[data-act="next"]');
        continue;
      }
      await page.waitForTimeout(200);
    }
    assert.ok(cpuMoves > 3, 'the computer took turns');
    await page.reload(); await page.locator('dialog.teacher-skills').getByRole('button', { name: 'Continue', exact: true }).click();
    assert.equal(await page.inputValue('#soloSel'), 'medium', 'solo mode is remembered');
    const w = await page.evaluate(() => G.wins);
    ok(unit + ' connect four, solo: no steals, the computer moves on its own, 2 full games played, setting remembered');

    /* ---------- Tic-Tac-Toe ---------- */
    await open('tic-tac-toe'); await page.waitForSelector('#soloMode');
    const tttOpt = right => page.evaluate(r => quiz.q.options.findIndex(o => !!o.ok === r), right);
    await page.click('#start'); await page.click('.sq[data-i="4"]');
    await page.click(`.opt[data-k="${await tttOpt(false)}"]`); await page.click('#check');
    assert.ok(await page.locator('.steal').count() === 1, 'two teams: a miss offers the steal');
    ok(unit + ' tic-tac-toe, two teams: a miss still offers the steal');
    await page.click(`.opt[data-k="${await tttOpt(true)}"]`); await page.click('#check'); await page.click('#go');
    await page.click('#newsetup'); await page.selectOption('#soloMode', 'solo'); await page.selectOption('#soloAI', 'easy');
    assert.ok(await page.locator('#nb').isHidden());
    await page.click('#start'); assert.equal(await page.evaluate(() => G.names.B), 'Computer');
    await page.click('.sq[data-i="4"]'); await page.click(`.opt[data-k="${await tttOpt(false)}"]`); await page.click('#check');
    assert.equal(await page.locator('.steal').count(), 0, 'no steal in solo');
    assert.ok((await page.textContent('.res')).includes('computer goes next'));
    await page.click('#go');
    assert.ok((await page.textContent('.turn')).includes('computer is choosing'));
    await until(() => turn === 'A' || over);
    games = 0;
    while (games < 2) {
      if (await page.evaluate(() => over)) { games++; await page.click('#again'); await until(() => (turn === 'A' && !quiz) || over); continue; }
      const sq = await page.evaluate(() => MKSOLOAI.ticTacToeMove(B, 'A', 'B', 'hard'));
      await page.click(`.sq[data-i="${sq}"]`); await page.click(`.opt[data-k="${await tttOpt(true)}"]`); await page.click('#check'); await page.click('#go');
      await until(() => (turn === 'A' && !quiz) || over);
    }
    const sc = await page.evaluate(() => G.score);
    ok(unit + ' tic-tac-toe, solo: no steals, the computer moves on its own, 2 full games (you ' + sc.A + ', computer ' + sc.B + ', draws ' + sc.D + ')');
    assert.deepEqual(errors.filter(e => !/Failed to load resource/.test(e)), [], 'no page errors');
    await page.close();
  }
  await browser.close();
  console.log(passed + ' hand-built solo checks passed');
})().catch(e => { console.error(e); process.exit(1); });
