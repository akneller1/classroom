'use strict';
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const http = require('node:http');
const { promisify } = require('node:util');
const { execFile } = require('node:child_process');
const { chromium } = require('playwright');
const root = path.resolve(__dirname, '../../..');
const server = http.createServer((req, res) => {
  if (req.url === '/favicon.ico') { res.writeHead(204).end(); return; }
  const file = path.join(root, decodeURIComponent(req.url.split('?')[0]));
  if (!file.startsWith(root + path.sep)) { res.writeHead(403).end(); return; }
  fs.readFile(file, (err, data) => {
    if (err) { console.error('Missing test resource: ' + req.url); res.writeHead(404).end(); return; }
    res.setHeader('Content-Type', file.endsWith('.js') ? 'text/javascript' : file.endsWith('.css') ? 'text/css' : file.endsWith('.html') ? 'text/html' : 'application/octet-stream');
    res.end(data);
  });
});
function kind(s) {
  return s.includes('games/games.js') ? 'generated' : s.includes('const UNIT=') ? 'unit' : s.includes('const POOLS=') ? 'inequality' : s.includes('CFG.questions') ? 'cfg' : s.includes('const CATS =') ? 'cats' : /const Q\s*=\s*\[/.test(s) ? 'picture' : s.includes('const CARDS =') ? 'cards' : s.includes('const CASE=') ? 'case' : 'other';
}
(async () => {
  await new Promise(r => server.listen(0, '127.0.0.1', r));
  const base = `http://127.0.0.1:${server.address().port}`;
  const browser = await chromium.launch(process.env.CHANNEL ? { channel: process.env.CHANNEL } : {});
  let checks = 0;
  try {
    const entries = fs.readdirSync(path.join(root, 'artifacts')).filter(name => {
      const p = path.join(root, 'artifacts', name, 'index.html');
      return fs.existsSync(p) && fs.readFileSync(p, 'utf8').includes('games/skill-setup.js') && (!process.env.MATCH || name.includes(process.env.MATCH));
    });
    for (const name of entries) {
      const html = fs.readFileSync(path.join(root, 'artifacts', name, 'index.html'), 'utf8'), type = kind(html);
      const page = await browser.newPage();
      const errors = []; page.on('pageerror', e => errors.push(e.message));
      try {
        await page.goto(`${base}/artifacts/${name}/index.html`);
        const setup = page.locator('dialog.teacher-skills');
        await setup.waitFor();
        const boxes = setup.locator('input[type=checkbox]'), n = await boxes.count();
        assert(n > 0, name + ' has bank skills');
        assert.equal(await setup.locator('input:checked').count(), n, 'all selected by default');
        assert(!((await setup.locator('fieldset label').allTextContents()).some(x => !x.trim())), 'nonempty labels');
        await setup.getByRole('button', { name: 'Clear All', exact: true }).click();
        assert(await setup.getByRole('button', { name: 'Continue', exact: true }).isDisabled());
        await setup.getByRole('button', { name: 'Select All', exact: true }).click();
        assert.equal(await setup.locator('input:checked').count(), n);
        await setup.getByRole('button', { name: 'Clear All', exact: true }).click();
        const selectedId = await boxes.last().getAttribute('value');
        await boxes.last().check();
        const selectedName = (await setup.locator('label').last().textContent()).trim();
        if (process.env.SCREENSHOT && checks === 0) await page.screenshot({ path: process.env.SCREENSHOT });
        await setup.getByRole('button', { name: 'Continue', exact: true }).click();
        if (type === 'generated') {
          const game = /data-game="([^"]+)"/.exec(html)[1];
          if (['connect-four', 'tic-tac-toe'].includes(game)) await page.click('#tGo');
          await page.waitForFunction(() => MKGAMES._state && !document.querySelector('.gm-loading'), { timeout: 60000 });
          const skills = await page.evaluate(() => {
            const s = MKGAMES._state();
            const items = s.cards || s.items || (s.cells ? Object.values(s.cells).map(c => c.it) : s.it ? [s.it] : []);
            return items.map(i => i.skill);
          });
          // Tic-tac-toe draws only after a square is picked.
          if (game === 'tic-tac-toe') {
            await page.click('[data-sq="0"]'); await page.waitForSelector('.gm-opt');
            assert.equal(await page.evaluate(() => MKGAMES._state().quiz.it.skill), selectedId);
          } else {
            assert(skills.length, name + ' produces questions');
            assert(skills.every(id => id === selectedId), name + ' filters every item');
          }
          if (name === 'relations-functions-connect-four') {
            // A one-skill pile has only three initial slots; seven turns test
            // its refill as well as the win mechanics with a restricted bank.
            for (let move=0;move<7;move++) {
              assert.equal(await page.evaluate(() => MKGAMES._state().it.skill), selectedId);
              const right=await page.evaluate(() => MKGAMES._state().it.options.findIndex(o=>o.ok));
              await page.click(`.gm-opt[data-opt="${right}"]`);await page.click('#c4Lock');
              await page.click(`.c4-hole[data-col="${move%2}"]`);
              if(move<6)await page.waitForSelector('#c4Lock');
            }
            assert.equal(await page.evaluate(() => MKGAMES._state().wins.L), 1);
          }
        } else if (type === 'unit') {
          const data = await page.evaluate(() => ({ type: G.p.type, pools: Object.values(UNIT.pools).flat() }));
          assert.equal(data.type, selectedId); assert(data.pools.every(id => id === selectedId));
          // Exhaust repeated generations and test each difficulty and its fallback.
          await page.evaluate(id => { for (const level of ['1','2','3','mix']) for (let i=0;i<12;i++) { const p=makeProblem(level,null); if (!p || p.type!==id || p.choices.length!==4) throw Error('Invalid selected-skill question'); } }, selectedId);
        } else if (type === 'inequality') {
          assert.equal(await page.evaluate(() => TYPE_NAME[G.p.type]), selectedName);
          assert(await page.evaluate(name => Object.values(POOLS).flat().every(x=>TYPE_NAME[x]===name), selectedName));
        } else if (type === 'cfg') {
          assert(await page.evaluate(() => CFG.questions.length > 0));
          assert.equal(await page.evaluate(() => new Set(CFG.questions.map(q => { const e=document.createElement('div'); e.innerHTML=q.skill||q.instr; return e.textContent; })).size), 1);
          await page.click('#start'); await page.click('[data-i="0"].sq');
          await page.waitForSelector('.opt');
        } else if (type === 'cats') {
          assert.equal(await page.evaluate(() => CATS.length), 1);
          assert.equal(await page.evaluate(() => CATS[0].name), selectedName);
          await page.locator('.tile').first().click();
          if (name === 'functions-transformations-jeopardy') {
            await page.evaluate(() => { state.used['0-0']=true;save(); });
            await page.reload();
            await setup.getByRole('button',{name:'Clear All',exact:true}).click();
            await setup.locator('input[type=checkbox]').last().check();
            await setup.getByRole('button',{name:'Continue',exact:true}).click();
            assert(await page.evaluate(() => state.used['0-0']), 'same selection restores its board');
            await page.reload();
            await setup.getByRole('button',{name:'Continue',exact:true}).click();
            assert(!(await page.evaluate(() => state.used['0-0'])), 'all-skills board is independent');
            await page.evaluate(() => { state.used['0-0']=true;save(); });
            await page.reload();
            await setup.getByRole('button',{name:'Continue',exact:true}).click();
            assert(await page.evaluate(() => state.used['0-0']), 'default board progress survives reload');
          }
        } else if (type === 'picture') {
          assert(await page.evaluate(() => Q.length > 0 && new Set(Q.map(q=>q.skill)).size===1));
          // Solve every selected question to verify the picture completion count.
          await page.evaluate(() => { Q.forEach(q=>{solved[q.id]='test';}); render(); });
          assert.equal(await page.locator('.cover:not(.revealed)').count(), 0);
          assert(await page.locator('#completion').isVisible());
        } else if (type === 'cards') {
          assert(await page.evaluate(() => CARDS.length > 0 && new Set(CARDS.map(q=>q.skill)).size===1));
        } else if (type === 'case') {
          await page.evaluate(() => { S.phase='ask'; S.i=0; render(); });
          assert(await page.evaluate(() => S.phase==='ask' && teacherQuestions.has(CASE.questions[S.i])));
          await page.evaluate(() => { S.i=N;S.phase='ask';render(); });
          assert.equal(await page.evaluate(() => S.phase), 'accuse');
        }
        assert.deepEqual(errors, [], name + ' browser errors'); checks++;
        console.log('PASS ' + name);
      } catch (e) { throw new Error(name + ': ' + e.stack + '\nPage errors: ' + errors.join('; ')); }
      finally { await page.close(); }
    }
    console.log(`PASS ${checks} game pages: defaults, bulk selection, empty guard, one-skill filtering and startup`);
    const emptyPage = await browser.newPage();
    const emptyErrors=[];emptyPage.on('pageerror',e=>emptyErrors.push(e.message));
    await emptyPage.goto(`${base}/artifacts/foundations-algebra-connect-four/index.html`);
    await emptyPage.locator('dialog.teacher-skills').getByRole('button',{name:'Continue',exact:true}).click();
    await emptyPage.evaluate(() => { MKGAMES.buildDeck=(unit,slots,opts,done)=>done([]); });
    await emptyPage.click('#tGo');
    await emptyPage.getByRole('button',{name:'Choose skills again'}).waitFor();
    assert.deepEqual(emptyErrors,[]);
    await emptyPage.close();
    console.log('PASS unexpected empty deck: recovery message without a question crash');
    if (process.env.MECHANICS) {
      const { stdout } = await promisify(execFile)(process.execPath, [path.join(__dirname, 'games-browser.cjs')], {
        env: { ...process.env, BASE: base }, maxBuffer: 4 * 1024 * 1024
      });
      console.log(stdout);
    }
  } finally { await browser.close(); server.close(); }
})().catch(e => { console.error(e); server.close(); process.exitCode=1; });
