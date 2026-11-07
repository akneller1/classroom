// Site integration for the Statistics Interactive Math entries (the active course lists tools alongside bank-driven resources): every new or reused card appears in its unit's
// Interactive Math section with Explore, worksheet, teacher key and Copy student link; the activity viewer loads the tool;
// the copied student link opens the tool; the Interactive Math shortcut appears only where a unit has tools.
// Usage (repository root): node tools/interactive-math-statistics/tests/site-integration.cjs
const { chromium } = require('playwright'); const http = require('http'), fs = require('fs'), path = require('path'), vm = require('vm');
const ROOT = path.resolve(__dirname, '../../..');
const ctx = { window: {} }; vm.runInNewContext(fs.readFileSync(path.join(ROOT, 'data.js'), 'utf8'), ctx);
const entries = []; for (const c of ctx.window.LIBRARY.courses) for (const u of c.units) for (const a of u.artifacts) if (a.bankFormat === 'interactive-math' && a.added === '2026-11-08' && c.id === 'statistics') entries.push({ c: c.id, u: u.id, a });
const T = { '.html': 'text/html', '.js': 'text/javascript', '.css': 'text/css', '.json': 'application/json', '.svg': 'image/svg+xml', '.jpg': 'image/jpeg', '.png': 'image/png', '.pdf': 'application/pdf' };
let pass = 0, fail = 0; const ok = (c, m) => { if (c) pass++; else { fail++; console.log('FAIL', m); } };
(async () => {
  const srv = await new Promise(r => { const s = http.createServer((q, res) => { let u = decodeURIComponent(q.url.split('?')[0].split('#')[0]); if (u === '/') u = '/index.html'; fs.readFile(path.join(ROOT, u), (e, d) => { if (e) { res.writeHead(404); res.end(); return; } res.writeHead(200, { 'Content-Type': T[path.extname(u)] || 'application/octet-stream' }); res.end(d); }); }); s.listen(0, '127.0.0.1', () => r(s)); });
  const base = 'http://127.0.0.1:' + srv.address().port, b = await chromium.launch();
  const context = await b.newContext({ viewport: { width: 1366, height: 768 }, permissions: ['clipboard-read', 'clipboard-write'] });
  for (const e of entries) {
    for (const f of ['path', 'thumb', 'worksheet', 'answerKey']) ok(fs.existsSync(path.join(ROOT, e.a[f])), e.a.title + ' missing ' + e.a[f]);
    const p = await context.newPage(); const errs = []; p.on('pageerror', x => errs.push(x.message));
    await p.goto(`${base}/index.html#${e.c}.${e.u}`); await p.waitForTimeout(900);
    const card = await p.evaluate(path => { const li = document.querySelector('li.card[data-path="' + path + '"]'); if (!li) return null;
      let sec = li.closest('section') || li.parentElement; const heads = []; let n = li; while (n && !heads.length) { n = n.parentElement; if (n) n.querySelectorAll(':scope > h2, :scope > h3, :scope > header h2').forEach(h => heads.push(h.textContent.trim())); }
      return { explore: (li.querySelector('.btn-open') || {}).textContent, ws: !!li.querySelector('a[href$="worksheet.pdf"]'), key: !!li.querySelector('a[href$="teacher-key.pdf"]'), share: !!li.querySelector('.share-student'), heads };
    }, e.a.path);
    ok(card, `${e.c}.${e.u}: card for ${e.a.title}`);
    if (card) { ok(card.explore === 'Explore' && card.ws && card.key && card.share, `${e.a.title}: card controls ${JSON.stringify(card)}`); ok(card.heads.some(h => /Interactive Math/.test(h)), `${e.a.title}: in Interactive Math section ${card.heads}`); }
    /* Active Statistics units retain the Interactive Math section alongside generators. */
    ok(await p.evaluate(() => !!document.querySelector('#algebra-interactive')), `${e.c}.${e.u}: Interactive Math section`);
    /* copy student link from the card, then open it */
    await p.evaluate(path => { window.__copied = ''; navigator.clipboard.writeText = t => { window.__copied = t; return Promise.resolve(); }; window.prompt = (m, t) => { window.__copied = t; }; document.querySelector('li.card[data-path="' + path + '"] .share-student').click(); }, e.a.path); await p.waitForTimeout(150);
    const link = await p.evaluate(() => window.__copied);
    ok(link && link.includes(e.a.path.replace(/\/index\.html$/, '')), `${e.a.title}: student link copied (${link})`);
    if (link) { const s = await context.newPage(); const se = []; s.on('pageerror', x => se.push(x.message)); await s.goto(link.replace(/^https?:\/\/[^/]+(\/classroom)?/, base)); await s.waitForTimeout(500);
      const ok2 = await s.evaluate(() => { const f = document.querySelector('iframe'); const d = f ? f.contentDocument : document; return !!(d && d.querySelector('.lab-title')); }); ok(ok2 && !se.length, `${e.a.title}: student link opens the tool ${se}`); await s.close(); }
    /* activity viewer */
    const v = await context.newPage(); const ve = []; v.on('pageerror', x => ve.push(x.message)); await v.goto(`${base}/activity.html?path=${encodeURIComponent(e.a.path)}`); await v.waitForTimeout(700);
    const title = await v.evaluate(() => { const f = document.querySelector('iframe'); return f && f.contentDocument && f.contentDocument.querySelector('.lab-title') ? f.contentDocument.querySelector('.lab-title').textContent : null; });
    ok(title === e.a.title, `${e.a.title}: viewer shows tool (${title})`); ok(!ve.length && !errs.length, `${e.a.title}: errors ${ve} ${errs}`); await v.close(); await p.close();
  }
  /* Statistics remains active; Discrete Math remains an outline. */
  { const q = await context.newPage(); await q.goto(`${base}/index.html#statistics.statistical-inference`); await q.waitForTimeout(800);
    ok(await q.evaluate(() => !!document.querySelector('#algebra-interactive') && !!document.querySelector('a[href*="lesson-planner.html"]')), 'Statistics unit page: generators plus Interactive Math');
    await q.goto(`${base}/index.html#statistics`); await q.waitForTimeout(800); ok(await q.evaluate(() => /4 units with skills, generators, games, and study guides/.test(document.body.textContent)), 'Statistics course page note');
    await q.goto(`${base}/index.html#discrete`); await q.waitForTimeout(800); ok(await q.evaluate(() => /course outline · activities coming soon/.test(document.body.textContent) && !/Interactive Math in/.test(document.body.textContent)), 'Discrete Math planned page unchanged');
    await q.goto(`${base}/index.html#discrete.${ctx.window.LIBRARY.courses.find(c => c.id === 'discrete').units[0].id}`); await q.waitForTimeout(800);
    ok(await q.evaluate(() => /Activities coming soon/.test(document.querySelector('.band-meta').textContent) && !document.querySelector('#algebra-interactive')), 'Discrete Math unit page unchanged'); await q.close(); }
  /* shortcut only where tools exist */
  const p = await context.newPage(); await p.goto(`${base}/index.html#math6.rational-numbers`); await p.waitForTimeout(800);
  ok(!(await p.evaluate(() => [...document.querySelectorAll('a.resource-shortcut')].some(a => /category=interactive/.test(a.href)))), 'no Interactive Math shortcut in a unit without tools');
  await p.goto(`${base}/index.html#algebra.quadratics`); await p.waitForTimeout(800); ok(await p.evaluate(() => !!document.querySelector('li.card[data-path="artifacts/quadratics-parabola-explorer/index.html"]')), 'existing Algebra 1 tool still listed');
  await b.close(); srv.close(); console.log(`${pass} checks passed, ${fail} failed (${entries.length} entries)`); process.exit(fail ? 1 : 0);
})();
