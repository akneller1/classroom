/* Daily Lesson Planner in a browser for the six bank-based courses (Algebra 2, 6th Grade, Pre-Algebra 7 and 8,
   Precalculus, Calculus): the Course menu selects the course; every day renders in all three views with no script
   error, every problem comes from the course's approved bank (none missing or unverified), nothing scrolls sideways;
   #unit= opens each unit's first day; New problems changes the problems; the student PowerPoint downloads.
   Starts its own static server. Needs Playwright.   COURSES=calculus,precalculus limits the run. */
'use strict';
const http = require('http'), fs = require('fs'), path = require('path');
const { chromium } = require(process.env.PW || 'playwright');
const ROOT = path.resolve(__dirname, '..', '..', '..');
const TYPES = { '.html': 'text/html', '.js': 'text/javascript', '.css': 'text/css', '.svg': 'image/svg+xml', '.json': 'application/json', '.png': 'image/png', '.jpg': 'image/jpeg', '.woff2': 'font/woff2' };
const server = http.createServer((req, res) => {
  const f = path.join(ROOT, decodeURIComponent(req.url.split('?')[0]));
  if (!f.startsWith(ROOT) || !fs.existsSync(f) || fs.statSync(f).isDirectory()) { res.writeHead(404); return res.end(); }
  res.writeHead(200, { 'content-type': TYPES[path.extname(f)] || 'application/octet-stream' }); fs.createReadStream(f).pipe(res);
});
const ALL = ['algebra2', 'math6', 'prealgebra7', 'prealgebra', 'precalculus', 'calculus'];
const COURSES = process.env.COURSES ? process.env.COURSES.split(',') : ALL;
(async () => {
  await new Promise(r => server.listen(0, r));
  const BASE = 'http://localhost:' + server.address().port, PAGE = BASE + '/worksheet-generator/lesson-planner.html';
  const b = await chromium.launch();
  let checks = 0; const fails = [];
  const ok = (c, m) => { checks++; if (!c) fails.push(m); };
  for (const course of COURSES) {
    const ctx = await b.newContext({ acceptDownloads: true, viewport: { width: 1280, height: 900 } }), pg = await ctx.newPage();
    const errs = []; pg.on('pageerror', e => errs.push(e.message));
    await pg.goto(PAGE + '#course=' + course + '&day=1'); await pg.waitForSelector('.pl-htitle h1', { timeout: 120000 });
    ok(await pg.$eval('#plCourse', e => e.value) === course, course + ': Course menu does not show the course');
    const info = await pg.evaluate(() => ({ n: window.MKPLAN_SCOPE.days.length, units: window.MKPLAN_SCOPE.units.map(u => ({ start: u.start_day })), sets: window.MKPLAN_SKILLS.UNIT_SET, ids: window.MKPLAN_SKILLS.SETS }));
    ok(info.n > 20, course + ': scope has only ' + info.n + ' days');
    let days = 0, problems = 0;
    for (let d = 1; d <= info.n; d++) {
      const r = await pg.evaluate(async (d) => {
        const out = {};
        for (const v of ['plan', 'student', 'key']) {
          location.hash = location.hash.replace(/day=\d+.*$/, '') + 'day=' + d + '&level=' + ['cp2', 'cp1', 'honors'][d % 3] + '&view=' + v;
          await new Promise(r => setTimeout(r, 0));
          out[v] = { title: (document.querySelector('.pl-htitle h1') || {}).textContent || '', sheet: !!document.querySelector('.pl-sheet'), cards: document.querySelectorAll('.pl-card').length, missing: document.querySelectorAll('.pl-missing').length };
        }
        out.sum = window.MKPLAN.summary(window.MKPLAN.ui.plan);
        // a bank question's key is the approved bank's answer (status source-key); only failed or unkeyed problems count
        out.sum.unverified = window.MKPLAN.allItems(window.MKPLAN.ui.plan).filter(p => !p.failed && !(p.verify && (p.verify.status === 'verified' || (p.source === 'authored-bank' && p.verify.status === 'source-key')))).length;
        out.scroll = document.documentElement.scrollWidth <= innerWidth + 1;
        out.course = window.MKPLAN_COURSE;
        return out;
      }, d);
      days++; problems += r.sum.problems;
      ok(r.course === course, course + ' day ' + d + ': planner switched to ' + r.course);
      ok(r.plan.title.length > 3, course + ' day ' + d + ': no title');
      ok(r.student.sheet && r.key.sheet, course + ' day ' + d + ': handout or key missing');
      ok(r.plan.cards === r.sum.problems, course + ' day ' + d + ': ' + r.plan.cards + ' cards for ' + r.sum.problems + ' problems');
      ok(r.sum.problems > 0 || /Assessment/.test(r.plan.title), course + ' day ' + d + ': no problems');
      ok(!r.sum.failed && !r.sum.unverified && !r.student.missing, course + ' day ' + d + ': missing or unverified problems');
      ok(r.scroll, course + ' day ' + d + ': page scrolls sideways');
    }
    // #unit= opens each unit's first day
    for (const [num, key] of Object.entries(info.sets)) {
      const setId = info.ids[key], start = info.units[+num - 1].start;
      await pg.evaluate((id) => { location.hash = '#unit=' + id; }, setId);
      for (let t = 0; t < 40 && /#unit=/.test(pg.url()); t++) await pg.waitForTimeout(50);
      ok(new RegExp('day=' + start + '\\b').test(pg.url()), course + ': #unit=' + setId + ' did not open day ' + start + ' (' + pg.url() + ')');
    }
    // New problems
    await pg.evaluate(() => { location.hash = location.hash.replace(/#.*/, '') + '#day=1&view=plan'; }); await pg.waitForTimeout(100);
    const before = await pg.$$eval('.pl-card .pl-q', x => x.map(e => e.textContent).join('|'));
    await pg.click('#plNew'); await pg.waitForTimeout(150);
    ok(await pg.$$eval('.pl-card .pl-q', x => x.map(e => e.textContent).join('|')) !== before, course + ': New problems did not change the problems');
    // student PowerPoint
    const [dl] = await Promise.all([pg.waitForEvent('download', { timeout: 90000 }), pg.click('#plPptxStudent')]);
    ok(/\.pptx$/.test(dl.suggestedFilename()), course + ': PowerPoint file name ' + dl.suggestedFilename());
    ok(errs.length === 0, course + ': page errors: ' + errs.slice(0, 3).join(' | '));
    console.log('  ✓ ' + course + ': ' + days + ' days × 3 views, ' + problems + ' problems, ' + Object.keys(info.sets).length + ' unit links');
    await ctx.close();
  }
  await b.close(); server.close();
  if (fails.length) { console.log(fails.slice(0, 40).join('\n')); console.log('FAIL ' + fails.length + ' of ' + checks); process.exit(1); }
  console.log('planner courses browser: ' + checks + ' checks, 0 failures');
})().catch(e => { console.error(e); process.exit(1); });
