/* Daily Lesson Planner in a browser: every day renders in all three views with no script error and no
   unverified problem; level, New problems, New problem and the unit links work. Needs a static server
   at BASE (default http://localhost:8765) and Playwright. */
'use strict';
const { chromium } = require(process.env.PW || 'playwright');
const BASE = process.env.BASE || 'http://localhost:8765';
(async () => {
  const b = await chromium.launch(); const pg = await b.newPage({ viewport: { width: 1280, height: 900 } });
  const errs = []; pg.on('pageerror', e => errs.push(e.message));
  let checks = 0, fails = [];
  const ok = (c, m) => { checks++; if (!c) fails.push(m); };
  await pg.goto(BASE + '/worksheet-generator/lesson-planner.html#day=1'); await pg.waitForSelector('.pl-htitle h1');
  const n = await pg.evaluate(() => window.MKPLAN_SCOPE.days.length);
  for (let d = 1; d <= n; d++) {
    const r = await pg.evaluate(async (d) => {
      const out = {};
      for (const v of ['plan', 'student', 'key']) {
        location.hash = '#day=' + d + '&level=' + ['cp2', 'cp1', 'honors'][d % 3] + '&view=' + v;
        await new Promise(r => setTimeout(r, 0));
        out[v] = { title: document.querySelector('.pl-htitle h1').textContent, sheet: !!document.querySelector('.pl-sheet'), cards: document.querySelectorAll('.pl-card').length, missing: document.querySelectorAll('.pl-missing').length };
      }
      out.sum = window.MKPLAN.summary(window.MKPLAN.ui.plan);
      out.scroll = document.documentElement.scrollWidth <= innerWidth + 1;
      return out;
    }, d);
    ok(r.plan.title.length > 3, 'day ' + d + ': no title');
    ok(r.student.sheet && r.key.sheet, 'day ' + d + ': handout or key missing');
    ok(r.plan.cards === r.sum.problems, 'day ' + d + ': ' + r.plan.cards + ' cards for ' + r.sum.problems + ' problems');
    ok(!r.sum.failed && !r.sum.unverified && !r.student.missing, 'day ' + d + ': unverified problems');
    ok(r.scroll, 'day ' + d + ': page scrolls sideways');
  }
  // controls
  await pg.evaluate(() => { location.hash = '#day=17&view=plan'; }); await pg.waitForTimeout(100);
  const before = await pg.$eval('.pl-card .pl-q', e => e.textContent);
  await pg.click('#plNew'); await pg.waitForTimeout(100);
  ok(await pg.$eval('.pl-card .pl-q', e => e.textContent) !== before, 'New problems did not change the problems');
  const one = await pg.$eval('.pl-card .pl-q', e => e.textContent);
  await pg.click('.pl-regen'); await pg.waitForTimeout(50);
  ok(await pg.$eval('.pl-card .pl-q', e => e.textContent) !== one, 'New problem did not change the problem');
  await pg.check('input[value=honors]'); await pg.waitForTimeout(50);
  ok(/level=honors/.test(pg.url()), 'level not in the URL');
  await pg.goto(BASE + '/worksheet-generator/lesson-planner.html#unit=algebra1-quadratics'); await pg.waitForTimeout(200);
  ok(/day=141\b/.test(pg.url()), '#unit= did not open the unit\'s first day: ' + pg.url());
  await pg.setViewportSize({ width: 390, height: 844 }); await pg.waitForTimeout(100);
  ok(await pg.evaluate(() => document.documentElement.scrollWidth <= 391), 'phone width scrolls sideways');
  errs.forEach(e => fails.push('script error: ' + e));
  fails.slice(0, 30).forEach(f => console.log('FAIL', f));
  console.log('planner browser: ' + checks + ' checks on ' + n + ' days, ' + fails.length + ' failures');
  await b.close(); process.exit(fails.length ? 1 : 0);
})();
