/* Cheat sheet builder: every cheat sheet on the site in one style (scripts/cheat-sheets/style.cjs, the newest
   unit-pack style; Andrey 2026-10-25).
   Usage: node scripts/cheat-sheets/build.cjs <name> [<name> …]   or   all
   A content file is scripts/cheat-sheets/content/<name>.cjs:
     { name, course, unitNo, unitName, focus, morefocus, front: [6 sections], back: [6 sections], checks: [...] }
   It writes artifacts/<name>-cheat-sheet/worksheet.pdf (2 letter pages) and thumbs/<name>-cheat-sheet.jpg (720 × 450).
   Before writing, every entry in `checks` is verified ({num: 'js expression', is: value}, {expr: 'js in x, y', is: 'js'},
   {list: [...], is: [...]}), and any page whose content runs past the page stops the build.
   CHECK_ONLY=1 checks the content and the page fit without writing anything (used by menu/tests/run-all.sh).
   Unit-pack sheets (scripts/unit-packs/) use the same style module; content/<prefix>.cjs wrappers include them in `all`.
   Needs Playwright + Chromium. */
'use strict';
const fs = require('fs'), path = require('path');
const S = require('./style.cjs');
const ROOT = S.ROOT, DIR = path.join(__dirname, 'content');

let checks = 0;
function fail(m) { console.error('CHECK FAILED: ' + m); process.exit(1); }
function num(e) { return Function('return (' + e + ')')(); }
function same(a, b) {
  const f = Function('x', 'y', 'return (' + a + ')'), g = Function('x', 'y', 'return (' + b + ')');
  return [[1.3, 0.7], [-2.1, 1.9], [0.4, -3.3], [5.2, 2.6]].every(p => Math.abs(f(p[0], p[1]) - g(p[0], p[1])) < 1e-9 * (1 + Math.abs(g(p[0], p[1]))));
}
function verify(c, where) {
  checks++;
  if (c.num !== undefined && Math.abs(num(c.num) - c.is) > 1e-6 * (1 + Math.abs(c.is))) fail(where + ': ' + c.num + ' = ' + num(c.num) + ', not ' + c.is);
  if (c.expr !== undefined && !same(c.expr, c.is)) fail(where + ': ' + c.expr + ' is not ' + c.is);
  if (c.list !== undefined) { const a = c.list.map(x => typeof x === 'number' ? x : num(x)).sort((p, q) => p - q), b = c.is.slice().sort((p, q) => p - q); if (a.length !== b.length || a.some((v, i) => Math.abs(v - b[i]) > 1e-9)) fail(where + ': list ' + a + ' is not ' + b); }
  if (c.true !== undefined && !num(c.true)) fail(where + ': ' + c.true + ' is false');
}

const names = process.argv[2] === 'all' ? fs.readdirSync(DIR).filter(f => f.endsWith('.cjs')).map(f => f.slice(0, -4)).sort() : process.argv.slice(2);
if (!names.length) { console.error('usage: node scripts/cheat-sheets/build.cjs <name>… | all'); process.exit(1); }
const sheets = names.map(n => {
  const C = require(path.join(DIR, n + '.cjs'));
  ['name', 'course', 'unitNo', 'unitName', 'focus', 'morefocus'].forEach(k => { if (C[k] === undefined) fail(n + ': missing ' + k); });
  if (C.front.length !== 6 || C.back.length !== 6) fail(n + ': each side needs 6 sections (' + C.front.length + ' + ' + C.back.length + ')');
  (C.checks || []).forEach((c, i) => verify(c, n + ' check ' + (i + 1)));
  C.front.concat(C.back).forEach((s, i) => { (s.check ? [].concat(s.check) : []).forEach(c => verify(c, n + ' section ' + (i + 1) + ' (' + s.title + ')')); try { S.secHtml(s, 1); } catch (e) { fail(n + ' section "' + s.title + '": ' + e.message); } });
  return C;
});
console.log(checks + ' checks passed');

(async () => {
  const pw = require('playwright');
  const browser = await pw.chromium.launch();
  const page = await browser.newPage();
  const problems = [];
  for (const C of sheets) {
    const html = S.cheatSheetHtml(C);
    const rel = 'artifacts/' + C.name + '-cheat-sheet/worksheet.pdf', f = path.join(ROOT, rel);
    fs.mkdirSync(path.dirname(f), { recursive: true });
    const tmp = path.join(path.dirname(f), '_tmp.html'); fs.writeFileSync(tmp, html);
    await page.goto('file://' + tmp); await page.evaluate(() => document.fonts.ready);
    const over = await page.evaluate(() => {
      const out = [];
      document.querySelectorAll('.pg').forEach((p, i) => { if (p.scrollHeight > p.clientHeight + 2) out.push('page ' + (i + 1)); });
      document.querySelectorAll('.sec').forEach(s => { if (s.scrollHeight > s.clientHeight + 2 || s.scrollWidth > s.clientWidth + 2) out.push('section "' + s.querySelector('h2').textContent.slice(1) + '"'); });
      return out;
    });
    if (over.length) { problems.push(C.name + ': content runs past ' + over.join(', ')); if (!process.env.FORCE) { fs.unlinkSync(tmp); continue; } }
    if (process.env.CHECK_ONLY) { fs.unlinkSync(tmp); console.log('ok ' + C.name); continue; }
    await page.pdf({ path: f, format: 'Letter', printBackground: true, margin: { top: 0, bottom: 0, left: 0, right: 0 } });
    fs.unlinkSync(tmp);
    const thumbs = path.join(ROOT, 'thumbs'), t2 = path.join(thumbs, '_t.html'); fs.writeFileSync(t2, html);
    const p2 = await browser.newPage({ viewport: { width: 816, height: 510 }, deviceScaleFactor: 720 / 816 });
    await p2.goto('file://' + t2); await p2.waitForTimeout(300);
    await p2.screenshot({ path: path.join(thumbs, C.name + '-cheat-sheet.jpg'), type: 'jpeg', quality: 85 }); await p2.close(); fs.unlinkSync(t2);
    console.log('wrote ' + rel);
  }
  await browser.close();
  console.log('cheat sheets: ' + sheets.length + (process.env.CHECK_ONLY ? ' checked' : ' built') + ', ' + checks + ' example checks, ' + problems.length + ' overflow problems');
  if (problems.length) { console.error('OVERFLOW:\n  ' + problems.join('\n  ')); process.exit(2); }
})();
