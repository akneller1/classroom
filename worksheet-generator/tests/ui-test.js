/* UI interaction test (playwright-core + Chromium). Exercises the controls the way a teacher would. */
'use strict';
const path = require('path');
const { chromium } = require(process.env.PW || 'playwright-core');
const URL = 'file://' + path.join(__dirname, '..', 'algebra1-linear-functions.html');
let n = 0; const bad = [];
const ok = (c, m) => { n++; if (!c) bad.push(m); };
(async () => {
  const b = await chromium.launch({ executablePath: process.env.CHROME, args: ['--no-sandbox'] });
  const ctx = await b.newContext({ viewport: { width: 1400, height: 900 } });
  const p = await ctx.newPage(); const errs = [];
  p.on('pageerror', e => errs.push(e.message)); p.on('console', m => m.type() === 'error' && errs.push(m.text()));
  await p.goto(URL); await p.waitForSelector('.page');
  const probs = () => p.locator('#pages .prob').count();
  const status = () => p.textContent('#status');
  const settle = async () => { await p.waitForTimeout(700); };
  const text = async () => (await p.locator('#pages .prob .q').allTextContents()).join('|');

  ok(await probs() === 15, 'default shows 15 problems');
  // clear all then select category B
  await p.click('#clrAll'); await settle(); ok(await p.isVisible('#empty'), 'empty message when nothing selected');
  ok(await p.isDisabled('#btnPrint'), 'print disabled when empty');
  await p.click('.cat[data-cat="graphing"] [data-act="all"]'); await settle();
  ok(await probs() === 16, 'category select-all gives 4 skills x 4 problems, got ' + await probs());
  await p.click('.cat[data-cat="graphing"] [data-act="none"]'); await settle();
  // single skill + count stepper
  await p.check('.lrow[data-id="lf-slope-two-points"] input[type=checkbox]'); await settle();
  await p.click('.lrow[data-id="lf-slope-two-points"] [data-d="1"]'); await p.click('.lrow[data-id="lf-slope-two-points"] [data-d="1"]'); await settle();
  ok(await probs() === 6, 'stepper to 6 problems, got ' + await probs());
  await p.fill('.lrow[data-id="lf-slope-two-points"] input[type=number]', '3'); await p.dispatchEvent('.lrow[data-id="lf-slope-two-points"] input[type=number]', 'change'); await settle();
  ok(await probs() === 3, 'typed count 3');
  // bulk apply
  await p.check('.lrow[data-id="lf-slope-classify"] input[type=checkbox]'); await p.fill('#bulkN', '2'); await p.click('#applyN'); await settle();
  ok(await probs() === 4, 'apply-to-all sets every checked skill to 2');
  // title, name line
  await p.fill('#optTitle', 'Quiz 4.2'); await settle();
  ok((await p.textContent('.ws-title')) === 'Quiz 4.2', 'custom title shown');
  await p.uncheck('#optNameDate'); await settle(); ok(await p.locator('.ws-name').count() === 0, 'name line removed');
  await p.check('#optNameDate');
  // versions
  await p.check('#versions-3', { force: true }).catch(() => {}); await p.click('label[for="versions-3"]'); await settle();
  ok(await p.locator('#verTabs .tab').count() === 3, 'three version tabs');
  const tA = await text(); await p.click('#verTabs .tab[data-v="1"]'); await settle(); const tB = await text();
  ok(tA !== tB, 'version B differs from A'); ok(/Version B/.test(await p.textContent('.vtag')), 'version tag B');
  await p.click('label[for="versions-1"]'); await settle(); ok(await p.locator('#verTabs').isHidden(), 'version tabs hidden for single');
  // answer key
  await p.click('#viewKey'); await settle(); ok(await p.locator('#pages .kprob').count() === 4, 'key has one entry per problem');
  await p.click('label[for="keyMode-answers"]'); await settle(); ok(await p.locator('#pages .ksteps').count() === 0, 'final-answers key has no steps');
  await p.click('label[for="keyMode-worked"]'); await settle(); ok(await p.locator('#pages .ksteps').count() > 0, 'worked key has steps');
  await p.uncheck('#optKey'); await settle(); ok(await p.locator('#viewKey').isHidden(), 'key controls hidden when key off'); ok(await p.locator('#pages .kprob').count() === 0, 'back on worksheet');
  await p.check('#optKey'); await settle();
  // regenerate one problem only
  await p.click('#viewStudent'); await settle();
  const before = (await p.locator('#pages .prob .q').allTextContents());
  await p.locator('#pages .prob').nth(1).hover(); await p.locator('#pages .prob .regen').nth(1).click(); await settle();
  const after = (await p.locator('#pages .prob .q').allTextContents());
  const diff = before.map((t, i) => t !== after[i]).filter(Boolean).length;
  ok(diff === 1 && before[1] !== after[1], 'regenerate changes exactly the clicked problem (changed ' + diff + ')');
  // survives reload (localStorage) and rebuild
  await p.reload(); await p.waitForSelector('.page', { timeout: 8000 }).catch(e => { console.log('RELOAD FAIL errs=' + JSON.stringify(errs)); throw e; }); await settle();
  const reloaded = (await p.locator('#pages .prob .q').allTextContents());
  ok(JSON.stringify(reloaded) === JSON.stringify(after), 'worksheet identical after reload');
  ok((await p.inputValue('#optTitle')) === 'Quiz 4.2', 'title remembered');
  // New problems changes everything
  await p.click('#btnNew'); await settle(); const fresh = (await p.locator('#pages .prob .q').allTextContents());
  ok(JSON.stringify(fresh) !== JSON.stringify(after), 'new problems differ');
  // difficulty / mode / workspace
  await p.click('label[for="difficulty-honors"]'); await settle(); ok(/Honors|Larger|fractions/i.test(await p.textContent('#hint-difficulty')), 'difficulty hint updates');
  const h1 = await p.evaluate(() => document.querySelector('#pages .work').style.height);
  await p.click('label[for="space-extended"]'); await settle();
  const h2 = await p.evaluate(() => document.querySelector('#pages .work').style.height);
  ok(parseFloat(h2) > parseFloat(h1), 'extended workspace taller than standard (' + h1 + ' -> ' + h2 + ')');
  // print path produces pages in printRoot with afterprint cleanup (stub window.print)
  await p.evaluate(() => { window.__printed = 0; window.print = () => { window.__printed = document.querySelectorAll('#printRoot .page').length; setTimeout(() => window.dispatchEvent(new Event('afterprint')), 10); }; });
  await p.click('#btnPrint'); await settle();
  ok(await p.evaluate(() => window.__printed) > 0, 'print puts pages in the print root');
  ok(await p.evaluate(() => document.getElementById('printRoot').children.length === 0 && !document.body.classList.contains('printing')), 'print root cleaned up');
  // tablet layout: no horizontal page scroll
  await p.setViewportSize({ width: 820, height: 1100 }); await settle();
  ok(await p.evaluate(() => document.documentElement.scrollWidth <= window.innerWidth + 1), 'tablet portrait: no horizontal scroll');
  await p.screenshot({ path: process.env.SHOT || '/tmp/ui-tablet.png' });
  await p.setViewportSize({ width: 1180, height: 820 }); await settle();
  ok(await p.evaluate(() => document.documentElement.scrollWidth <= window.innerWidth + 1), 'tablet landscape: no horizontal scroll');
  ok(errs.length === 0, 'no console/page errors: ' + errs.join(' ; '));
  console.log(n + ' UI checks'); if (bad.length) { console.log(bad.length + ' FAILED'); bad.forEach(x => console.log(' - ' + x)); } else console.log('ALL UI CHECKS PASSED');
  await b.close(); process.exit(bad.length ? 1 : 0);
})();
