/* Browser layout test (needs playwright-core + Chromium; see README). Usage:
     PW=/path/to/playwright-core CHROME=/opt/pw-browsers/chromium node tests/browser-test.js
   Builds many worksheets and answer keys in a real browser and checks the pagination. */
'use strict';
const path = require('path');
const { chromium } = require(process.env.PW || 'playwright-core');
const URL = 'file://' + path.join(__dirname, '..', 'algebra1-linear-functions.html');
(async () => {
  const b = await chromium.launch({ executablePath: process.env.CHROME, args: ['--no-sandbox'] });
  const p = await b.newPage({ viewport: { width: 1400, height: 900 } });
  const errs = []; p.on('pageerror', e => errs.push(e.message)); p.on('console', m => m.type() === 'error' && errs.push(m.text()));
  await p.goto(URL); await p.waitForSelector('.page');
  const result = await p.evaluate(async () => {
    const A = MKWS.app, st = A.state, ids = Object.keys(MKWS.registry.lessons);
    const fails = []; let sheets = 0, pagesTotal = 0, maxPages = 0;
    const diffs = ['basic', 'standard', 'honors'], modes = ['integers', 'preferred', 'fractions'], spaces = ['compact', 'standard', 'extended'];
    let seed = 1;
    async function check(tag, view) {
      const ws = st.ws;
      for (let v = 0; v < ws.versions.length; v++) {
        const pages = await A.getPages(v, view);
        sheets++; pagesTotal += pages.length; maxPages = Math.max(maxPages, pages.length);
        const stage = document.createElement('div'); stage.style.cssText = 'position:absolute;left:-9999px;top:0';
        pages.forEach(pg => stage.appendChild(pg.cloneNode(true))); document.body.appendChild(stage);
        const pgs = Array.from(stage.querySelectorAll('.page'));
        pgs.forEach((pg, i) => {
          const where = tag + ' ' + view + ' v' + v + ' p' + (i + 1);
          const body = pg.querySelector('.pg-body'), br = body.getBoundingClientRect(), pr = pg.getBoundingClientRect();
          if (!body.children.length) fails.push(where + ': blank page');
          Array.from(body.children).forEach(u => {
            const r = u.getBoundingClientRect();
            if (r.bottom > br.bottom + 1) fails.push(where + ': unit overflows page bottom by ' + (r.bottom - br.bottom).toFixed(1));
            if (r.right > br.right + 1) fails.push(where + ': unit wider than page body');
          });
          pg.querySelectorAll('.prob,.kprob,svg,table').forEach(e => {
            const r = e.getBoundingClientRect();
            if (r.width && (r.right > br.right + 2 || r.left < br.left - 8 || r.bottom > br.bottom + 1)) fails.push(where + ': clipped ' + e.tagName + '.' + (e.className.baseVal || e.className));
          });
          if (pg.querySelectorAll('.katex-error').length) fails.push(where + ': katex error');
          if (!/Page \d+ of \d+/.test(pg.querySelector('.pf-r').textContent)) fails.push(where + ': no page number');
          pg.querySelectorAll('.pbody,.kbody').forEach(e => { if (e.scrollWidth > e.clientWidth + 2) fails.push(where + ': horizontal overflow in problem text (+' + (e.scrollWidth - e.clientWidth) + 'px; body ' + e.clientWidth + 'px; ' + (e.querySelector('table.vt') ? 'table ' + Math.round(e.querySelector('table.vt').getBoundingClientRect().width) : 'no table') + ')'); });
        });
        const last = pgs[pgs.length - 1];
        if (pgs.length > 1 && last.querySelector('.pg-body').children.length === 0) fails.push(tag + ': trailing blank page');
        document.body.removeChild(stage);
      }
    }
    // 1) every lesson alone, every difficulty x mode (3 versions), student + key
    for (const id of ids) for (const d of diffs) for (const m of modes) {
      Object.assign(st.settings, { lessons: { [id]: 5 }, difficulty: d, numberMode: m, versions: 3, space: spaces[seed % 3], grids: seed % 5 !== 0, seed: seed++, salts: {}, keyMode: seed % 2 ? 'worked' : 'answers', answerKey: true, showNameDate: true });
      st.cache = {}; st.ws = MKWS.buildWorksheet(st.settings, 'algebra1-linear-functions');
      await check(id + '/' + d + '/' + m, 'student'); await check(id + '/' + d + '/' + m, 'key');
    }
    // 2) everything at once
    for (const sp of spaces) for (const km of ['answers', 'worked']) {
      const all = {}; ids.forEach(id => all[id] = 3);
      Object.assign(st.settings, { lessons: all, difficulty: 'standard', numberMode: 'fractions', versions: 3, space: sp, keyMode: km, grids: true, seed: 77 + seed++, salts: {} });
      st.cache = {}; st.ws = MKWS.buildWorksheet(st.settings, 'algebra1-linear-functions');
      await check('ALL/' + sp + '/' + km, 'student'); await check('ALL/' + sp + '/' + km, 'key');
    }
    const sum = {}; fails.forEach(f => { const k = f.split(' ')[0].split('/')[0] + ' :: ' + f.replace(/^.*? p\d+: /, ''); sum[k] = (sum[k] || 0) + 1; });
    return { summary: sum, example: fails.slice(0, 3), nfails: fails.length, sheets, pagesTotal, maxPages };
  });
  console.log(JSON.stringify(result, null, 1)); console.log('page errors:', JSON.stringify(errs));
  await b.close();
  process.exit(result.nfails || errs.length ? 1 : 0);
})();
