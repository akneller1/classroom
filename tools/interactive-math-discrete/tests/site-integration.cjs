// Site integration for the Discrete Math Interactive Math entries: every new or reused card appears in its unit's
// Interactive Math section with Explore, worksheet and teacher key; student-link controls are limited to
// individual games and study guides; the activity viewer loads the tool; the Interactive Math shortcut appears only where a unit has tools.
// Usage (repository root): node tools/interactive-math-discrete/tests/site-integration.cjs
const { chromium } = require('playwright'); const http = require('http'), fs = require('fs'), path = require('path'), vm = require('vm');
const ROOT = path.resolve(__dirname, '../../..');
const ctx = { window: {} }; vm.runInNewContext(fs.readFileSync(path.join(ROOT, 'data.js'), 'utf8'), ctx);
const entries = []; for (const c of ctx.window.LIBRARY.courses) for (const u of c.units) for (const a of u.artifacts) if (a.bankFormat === 'interactive-math' && a.added === '2026-11-09' && c.id === 'discrete') entries.push({ c: c.id, u: u.id, a });
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
    if (card) { ok(card.explore === 'Explore' && card.ws && card.key && !card.share, `${e.a.title}: card controls ${JSON.stringify(card)}`); ok(card.heads.some(h => /Interactive Math/.test(h)), `${e.a.title}: in Interactive Math section ${card.heads}`); }
    /* published course: the unit page has the generator shortcuts and an Interactive Math section */
    ok(await p.evaluate(() => !!document.querySelector('#algebra-interactive') && !!document.querySelector('a[href*="worksheet-generator/printables.html#unit=discrete-"]')), `${e.c}.${e.u}: Interactive Math section and generators`);
    ok(!card.share, `${e.a.title}: interactive tools do not offer student links`);
    /* activity viewer */
    const v = await context.newPage(); const ve = []; v.on('pageerror', x => ve.push(x.message)); await v.goto(`${base}/activity.html?path=${encodeURIComponent(e.a.path)}`); await v.waitForTimeout(700);
    const title = await v.evaluate(() => { const f = document.querySelector('iframe'); return f && f.contentDocument && f.contentDocument.querySelector('.lab-title') ? f.contentDocument.querySelector('.lab-title').textContent : null; });
    ok(title === e.a.title, `${e.a.title}: viewer shows tool (${title})`); ok(!ve.length && !errs.length, `${e.a.title}: errors ${ve} ${errs}`); await v.close(); await p.close();
  }
  /* course page and partner checks / cheat sheets */
  { const q = await context.newPage(); await q.goto(`${base}/index.html#discrete`); await q.waitForTimeout(800);
    ok(await q.evaluate(() => /10 units with (?:skills|lesson plans), generators, games, and study guides/.test(document.body.textContent) && !document.querySelector('.course-wip-label')), 'Discrete Math course page is published');
    await q.goto(`${base}/index.html#discrete.graphs-trees`); await q.waitForTimeout(900);
    for (const pth of ['artifacts/discrete-graphs-trees-cheat-sheet/worksheet.pdf', 'worksheet-generator/millionaire.html?course=discrete&unit=graphs-trees'])
      ok(await q.evaluate(p => !!document.querySelector('li.card[data-path="' + p + '"]'), pth), 'graphs-trees lists ' + pth);
    /* partner checks are listed under Printable Worksheets in Browse Activities (as for Algebra 2), not on unit pages */
    await q.goto(`${base}/index.html#activities?subject=discrete&category=worksheets`); await q.waitForTimeout(1200);
    ok(await q.evaluate(() => [...document.querySelectorAll('li.card')].filter(l => /discrete-.*-partner-check-[12]\/worksheet\.pdf/.test(l.dataset.path || '')).length === 20), 'Browse Activities lists all 20 Discrete Math partner checks');
    await q.close(); }
  await b.close(); srv.close(); console.log(`${pass} checks passed, ${fail} failed (${entries.length} entries)`); process.exit(fail ? 1 : 0);
})();
