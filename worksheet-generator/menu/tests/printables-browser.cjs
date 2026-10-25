/* Printable Generators in a browser: every unit × printable × level draws student and key pages that fit
   (nothing runs past the page, a room, a door or a problem box), and the teacher controls work.
   Needs Playwright + Chromium:   node worksheet-generator/menu/tests/printables-browser.cjs */
'use strict';
const assert = require('node:assert/strict');
const http = require('http'), fs = require('fs'), path = require('path');
const pw = process.env.PW ? require(process.env.PW) : require('playwright');
const ROOT = path.resolve(__dirname, '..', '..', '..');
const TYPES = { '.html': 'text/html', '.js': 'text/javascript', '.css': 'text/css', '.svg': 'image/svg+xml', '.woff2': 'font/woff2', '.ttf': 'font/ttf', '.woff': 'font/woff', '.jpg': 'image/jpeg', '.png': 'image/png' };
const server = http.createServer((req, res) => {
  const f = path.join(ROOT, decodeURIComponent(req.url.split('?')[0]));
  if (!f.startsWith(ROOT) || !fs.existsSync(f) || fs.statSync(f).isDirectory()) { res.writeHead(404); return res.end(); }
  res.writeHead(200, { 'content-type': TYPES[path.extname(f)] || 'application/octet-stream' }); fs.createReadStream(f).pipe(res);
});
let n = 0; const ok = name => { n++; console.log('  ✓ ' + name); };
(async () => {
  await new Promise(r => server.listen(0, r));
  const base = 'http://localhost:' + server.address().port;
  const browser = await pw.chromium.launch(process.env.CHROME ? { executablePath: process.env.CHROME } : {});
  const page = await browser.newPage({ viewport: { width: 1350, height: 950 } });
  const errors = []; page.on('pageerror', e => errors.push(e.message)); page.on('console', m => { if (m.type() === 'error' && !/Failed to load resource/.test(m.text())) errors.push(m.text()); });   // offline fonts are not errors
  await page.goto(base + '/worksheet-generator/printables.html#unit=algebra1-systems-of-equations&kind=maze');
  await page.evaluate(() => { try { localStorage.clear(); } catch (e) { /* ignore */ } }); await page.reload();
  await page.waitForSelector('.pr-page', { timeout: 60000 });
  // controls: kind, level, versions, key tab
  assert.match(await page.textContent('#prCrumb'), /Maze/);
  await page.check('input[name=prKind][value=partner]'); await page.waitForSelector('.pr-who', { timeout: 60000 });
  assert.match(await page.evaluate(() => location.hash), /kind=partner/);
  await page.check('input[name=prLevel][value=honors]'); await page.waitForSelector('.pr-page', { timeout: 60000 });
  await page.selectOption('#prVer', '2'); await page.waitForSelector('[data-ver="1"]', { timeout: 60000 });
  await page.click('[data-doc=key]'); await page.waitForSelector('.mm-keytag');
  await page.click('[data-ver="1"]'); assert.match(await page.textContent('.pr-pages'), /Version B/);
  assert.equal(await page.isDisabled('#prPrintS'), false);
  ok('controls: printable, level, versions, student/key preview and print buttons');
  // every unit × kind × level fits
  const bad = await page.evaluate(async () => {
    const PR = MKMENU.printables, out = [];
    for (const unit of Object.keys(MKMENU.skillSets)) for (const kind of PR.KINDS.map(k => k.id)) for (const level of ['cp2', 'cp1', 'honors']) {
      const cfg = PR.defaultConfig(unit, kind); cfg.level = level; cfg.seed = 77;
      const B = PR.build(cfg, 0);
      if (B.error) { if (!(unit === 'algebra1-statistics-data-modeling' && kind === 'tarsia')) out.push(unit + ' ' + kind + ' ' + level + ': ' + B.error); continue; }
      for (const key of [false, true]) {
        const els = PR.pageEls(cfg, B, 0, 1, key), r = document.createElement('div'); r.style.cssText = 'position:absolute;left:-9999px;top:0'; document.body.appendChild(r); els.forEach(e => r.appendChild(e));
        els.forEach((e, i) => {
          const bd = e.querySelector('.mm-body'); if (bd.scrollHeight > bd.clientHeight + 2) out.push(unit + ' ' + kind + ' ' + level + (key ? ' key' : '') + ' page ' + (i + 1) + ' runs past the page');
          e.querySelectorAll('.pr-door,.pr-room,.pr-pbox,.pr-ea-l').forEach(x => { if (x.scrollHeight > x.clientHeight + 5 || x.scrollWidth > x.clientWidth + 5) out.push(unit + ' ' + kind + ' ' + level + (key ? ' key' : '') + ': text runs past a ' + x.className); });
          if (/NaN|\[object|\bundefined\b(?! \(a vertical)/.test(e.textContent)) out.push(unit + ' ' + kind + ' ' + level + ': bad text on page ' + (i + 1));
          if (!key && /Answer key|TEACHER KEY/.test(e.textContent)) out.push(unit + ' ' + kind + ': key text on a student page');
        });
        r.remove();
      }
    }
    return out;
  });
  if (bad.length) console.log(bad.join('\n')); assert.deepEqual(bad, []);
  ok('every unit, printable and level: student and key pages fit, nothing runs past a room, door or box');
  // site: a unit page links each generator straight to printables.html
  await page.goto(base + '/index.html#algebra.quadratics'); await page.waitForTimeout(700);
  const links = await page.evaluate(() => [...document.querySelectorAll('a')].map(a => a.getAttribute('href')).filter(h => /printables\.html/.test(h || '')));
  ['maze', 'color', 'tarsia', 'error', 'partner'].forEach(k => assert.ok(links.includes('worksheet-generator/printables.html#unit=algebra1-quadratics&kind=' + k), 'unit page links the ' + k + ' generator'));
  assert.doesNotMatch(await page.textContent('body'), /Solving Quadratics Maze|Quadratics Color By Number/);
  ok('site: unit pages link the five printable generators and no longer list the fixed PDFs');
  assert.deepEqual(errors, []);
  await browser.close(); server.close();
  console.log('PASS: ' + n + ' printable browser checks');
})().catch(e => { console.error(e); process.exit(1); });
