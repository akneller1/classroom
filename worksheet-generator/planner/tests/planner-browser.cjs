/* Daily Lesson Planner in a browser: every day renders in all three views with no script error and no
   unverified problem; level, New problems, New problem and the unit links work. Needs a static server
   at BASE (default http://localhost:8765) and Playwright. */
'use strict';
const { chromium } = require(process.env.PW || 'playwright');
const BASE = process.env.BASE || 'http://localhost:8765';
const GEO = process.env.COURSE === 'geometry', CP = GEO ? '#course=geometry&' : '#';
const D0 = GEO ? 36 : 30, D1 = D0 + 1;
const PAGE = BASE + '/worksheet-generator/lesson-planner.html';
(async () => {
  const b = await chromium.launch(); const pg = await (await b.newContext({ acceptDownloads: true, viewport: { width: 1280, height: 900 } })).newPage();
  const errs = []; pg.on('pageerror', e => errs.push(e.message));
  let checks = 0, fails = [];
  const ok = (c, m) => { checks++; if (!c) fails.push(m); };
  await pg.goto(BASE + '/worksheet-generator/lesson-planner.html' + CP + 'day=1'); await pg.waitForSelector('.pl-htitle h1');
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
  await pg.goto(BASE + '/worksheet-generator/lesson-planner.html#unit=' + (GEO ? 'geometry-circles' : 'algebra1-quadratics')); await pg.waitForTimeout(200);
  ok((GEO ? /day=\d+/ : /day=141\b/).test(pg.url()), '#unit= did not open the unit\'s first day: ' + pg.url());
  // editable minutes (kept for the day type, problems unchanged), notes setting, PowerPoint download
  await pg.goto(BASE + '/worksheet-generator/lesson-planner.html' + CP + 'day=' + D0 + '&view=plan'); await pg.waitForSelector('.pl-mins');
  const q0 = await pg.$eval('.pl-card .pl-q', e => e.textContent);
  await pg.fill('.pl-mins[data-s="1"]', '22'); await pg.press('.pl-mins[data-s="1"]', 'Tab');
  ok(await pg.textContent('.pl-min[data-min="1"]') === '22 min', 'edited minutes not shown in the section header');
  ok(q0 === await pg.$eval('.pl-card .pl-q', e => e.textContent), 'editing minutes changed the problems');
  await pg.goto(BASE + '/worksheet-generator/lesson-planner.html' + CP + 'day=' + D1 + '&view=student'); await pg.waitForSelector('.pl-sheet');
  ok(/22 min/.test(await pg.textContent('.pl-s-notes .pl-shd')), 'edited minutes not kept for the next Lesson day');
  await pg.check('input[name=plNotes][value=filled]'); await pg.waitForTimeout(50);
  ok(await pg.$$eval('.pl-worked', x => x.length) >= 1 && await pg.$$eval('.pl-vocab.filled', x => x.length) === 1, 'pre-filled notes not shown');
  await pg.check('input[name=plNotes][value=fill]'); await pg.waitForTimeout(50);
  ok(await pg.$$eval('.pl-worked', x => x.length) === 0, 'fill-in notes still show worked examples');
  await pg.evaluate((h) => { location.hash = h; }, '#day=' + D1 + '&view=plan'); await pg.waitForSelector('#plResetMin');
  await pg.click('#plResetMin');
  ok(await pg.$eval('.pl-mins[data-s="1"]', e => e.value) === '15', 'reset did not restore the planned minutes');
  const [dl] = await Promise.all([pg.waitForEvent('download', { timeout: 60000 }), pg.click('#plPptxStudent')]);
  ok((GEO ? new RegExp('^Geometry-Day0' + D1 + '-.*-Student\\.pptx$') : new RegExp('^Algebra1-Day0' + D1 + '-.*-Student\\.pptx$')).test(dl.suggestedFilename()), 'PowerPoint file name: ' + dl.suggestedFilename());
  await pg.check('input[name=plNotes][value=lesson]');
  // editable notes: saved per lesson, used on the handout, reset restores the original
  await pg.evaluate((h) => { location.hash = h; }, CP + 'day=' + D0 + '&view=plan'); await pg.waitForSelector('.pl-noted');
  await pg.fill('.pl-noted textarea[data-n="idea"]', 'Edited key idea.');
  await pg.click('#plAddWord'); await pg.fill('.pl-noted input[data-n="w"]:last-of-type >> nth=-1', 'my word'); await pg.fill('.pl-noted textarea[data-n="d"] >> nth=-1', 'my meaning');
  await pg.fill('.pl-noted textarea[data-n="extra"]', 'Teacher note line.'); await pg.waitForTimeout(400);
  await pg.reload(); await pg.waitForSelector('.pl-noted');
  ok(await pg.$eval('.pl-noted textarea[data-n="idea"]', e => e.value) === 'Edited key idea.', 'edited key idea not kept after reload');
  await pg.check('input[name=plNotes][value=filled]'); await pg.click('.tab[data-view=student]');
  const hs = await pg.textContent('.pl-s-notes');
  ok(/Edited key idea\./.test(hs) && /my word/.test(hs) && /my meaning/.test(hs) && /Teacher note line/.test(hs), 'edited notes not on the handout');
  await pg.click('.tab[data-view=plan]'); await pg.click('#plNotesReset');
  ok(await pg.$eval('.pl-noted textarea[data-n="idea"]', e => e.value) !== 'Edited key idea.', 'reset did not restore the notes');
  await pg.check('input[name=plNotes][value=lesson]');
  await pg.setViewportSize({ width: 390, height: 844 }); await pg.waitForTimeout(100);
  ok(await pg.evaluate(() => document.documentElement.scrollWidth <= 391), 'phone width scrolls sideways');
  errs.forEach(e => fails.push('script error: ' + e));
  fails.slice(0, 30).forEach(f => console.log('FAIL', f));
  console.log('planner browser: ' + checks + ' checks on ' + n + ' days, ' + fails.length + ' failures');
  await b.close(); process.exit(fails.length ? 1 : 0);
})();
