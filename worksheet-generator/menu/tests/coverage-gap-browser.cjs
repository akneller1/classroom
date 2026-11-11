/* Coverage-gap skills in the real worksheet page: each new skill is listed under its class → unit, builds verified
   worksheets in every format it supports (short answer, multiple choice, choose all that apply, Open Response),
   prints student copies without answers and keys with them, and fits the pages. Needs Playwright + Chromium.
   SHOTS=dir keeps screenshots of the printed pages. */
'use strict';
const assert = require('node:assert/strict');
const http = require('http'), fs = require('fs'), path = require('path');
const pw = process.env.PW ? require(process.env.PW) : require('playwright');
const ROOT = path.resolve(__dirname, '..', '..', '..');
const TYPES = { '.html': 'text/html', '.js': 'text/javascript', '.css': 'text/css', '.svg': 'image/svg+xml', '.json': 'application/json', '.png': 'image/png', '.woff2': 'font/woff2' };
const server = http.createServer((req, res) => {
  const p = decodeURIComponent(req.url.split('?')[0]), f = path.join(ROOT, p.endsWith('/') ? p + 'index.html' : p);
  if (!f.startsWith(ROOT) || !fs.existsSync(f) || fs.statSync(f).isDirectory()) { res.writeHead(404); return res.end('nf'); }
  res.writeHead(200, { 'content-type': TYPES[path.extname(f)] || 'application/octet-stream' }); fs.createReadStream(f).pipe(res);
});
// [unit, skill, level, formats]
const CASES = [
  ['algebra1-foundations', 'properties', 'cp2', ['mixed', 'mc', 'multi']], ['algebra1-foundations', 'properties', 'honors', ['mixed', 'mc', 'multi', 'mcas']],
  ['algebra1-foundations', 'real-number-operations', 'cp1', ['mixed', 'mc']], ['algebra1-foundations', 'interpret-expression', 'honors', ['mixed', 'mc']],
  ['algebra1-linear-equations-slope', 'direct-variation', 'cp1', ['mixed', 'mc']], ['algebra1-linear-equations-slope', 'direct-variation', 'honors', ['mcas']], ['algebra1-quadratics', 'table-model-type', 'cp1', ['mixed', 'mc']],
  ['geometry-angles-parallel-lines', 'angle-pairs-figure', 'cp1', ['mixed', 'mc', 'multi']], ['geometry-angles-parallel-lines', 'parallel-lines-converse', 'honors', ['mixed']],
  ['geometry-triangles-congruence', 'congruence-rigid-motions', 'cp1', ['mixed']], ['geometry-triangle-relationships', 'triangle-concurrency-name', 'cp1', ['mixed', 'mc']],
  ['geometry-triangle-relationships', 'triangle-circumcenter-incenter', 'honors', ['mixed', 'mc']], ['geometry-similarity', 'similarity-area-volume-ratio', 'cp1', ['mixed', 'mc']],
  ['geometry-similarity', 'similarity-area-investigation', 'honors', ['mcas']], ['geometry-right-triangles-trigonometry', 'law-of-sines', 'honors', ['mixed', 'mc']],
  ['geometry-right-triangles-trigonometry', 'law-of-cosines', 'honors', ['mixed']], ['geometry-quadrilaterals-polygons', 'kite-isosceles-trapezoid', 'cp1', ['mixed', 'mc']],
  ['geometry-transformations', 'transformation-sequence-congruence', 'honors', ['mixed']], ['geometry-area-surface-area-volume', 'measure-pyramid-surface', 'cp2', ['mixed', 'mc']],
  ['geometry-area-surface-area-volume', 'measure-cone-surface', 'honors', ['mixed']], ['geometry-area-surface-area-volume', 'measure-composite-round', 'cp1', ['mixed']],
  ['geometry-area-surface-area-volume', 'measure-unit-conversion', 'cp1', ['mixed', 'mc']], ['geometry-area-surface-area-volume', 'measure-similar-solids', 'honors', ['mixed', 'mc']]
];
(async () => {
  await new Promise(r => server.listen(0, r));
  const base = 'http://localhost:' + server.address().port, browser = await pw.chromium.launch(process.env.CHROME ? { executablePath: process.env.CHROME } : {});
  let built = 0;
  for (const [unit, skill, level, formats] of CASES) for (const fmt of formats) {
    const ctx = await browser.newContext({ viewport: { width: 1300, height: 1000 } }), page = await ctx.newPage(), errs = [];   // fresh storage: no restored worksheet
    page.on('pageerror', e => errs.push(e.message)); page.on('dialog', d => d.accept());
    await page.goto(base + '/worksheet-generator/worksheet.html#unit=' + unit); await page.waitForSelector('.mmSkill');
    const gaps = await page.textContent('.mm-gaps');
    if (unit === 'algebra1-foundations') assert.doesNotMatch(gaps, /Naming properties/, 'the properties gap warning is gone');
    await page.click('[data-wpreset="' + fmt + '"]'); await page.waitForTimeout(80);
    await page.check('input[name=mmLevel][value="' + level + '"]'); await page.waitForTimeout(80);
    const listed = await page.evaluate(async sk => { if (![...document.querySelectorAll('.mmSkill')].some(cb => cb.value === sk)) return false; for (let k = 0; k < 80; k++) { const cb = [...document.querySelectorAll('.mmSkill')].find(x => (x.value === sk) !== x.checked); if (!cb) break; cb.click(); await new Promise(r => setTimeout(r, 25)); } return true; }, skill);
    assert.ok(listed, unit + ': ' + skill + ' is listed under its unit');
    await page.waitForTimeout(80);
    await page.click('#mmBuildBtn'); await page.waitForSelector('.mm-dcard', { timeout: 60000 });
    const info = await page.evaluate(async ({ fmt }) => {
      const S = MKMENU.app.state(), items = [].concat(...S.versions[0].sections.map(s => s.items)), out = { n: items.length, skills: [...new Set(items.map(i => i.skill))], bad: [], fmtFail: [], keys: [], uniq: new Set(items.map(i => i.key + JSON.stringify((i.multi || i.mc || {}).opts || null))).size };
      items.forEach(i => { if (i.failed || !i.verify || i.verify.status !== 'verified') out.bad.push(i.reason || (i.verify && i.verify.issues.join(';'))); if (i.mcFail || i.multiFail || i.mcasFail) out.fmtFail.push(i.mcFail || i.multiFail || i.mcasFail);
        if (fmt === 'mc' && i.mc) out.keys.push(i.mc.opts.length); if (fmt === 'multi' && !i.multi) out.fmtFail.push('no choose-all'); if (fmt === 'mcas' && (i.parts || []).length < 4) out.fmtFail.push('fewer than four parts'); });
      const root = document.getElementById('printRoot'), res = {};
      for (const kind of ['student', 'key']) { const pages = await MKMENU.renderPages(S, 0, kind); root.innerHTML = ''; pages.forEach(p => root.appendChild(p)); res[kind] = { text: root.innerText, overflow: pages.overflow.length, pages: pages.length, svg: root.querySelectorAll('svg').length, upperAnd: /[a-z,] (AND|OR) [a-z]/.test(root.innerText) }; }
      root.innerHTML = ''; out.print = res; return out;
    }, { fmt });
    const tag = skill + ' ' + level + ' ' + fmt;
    assert.deepEqual(info.bad, [], tag + ': unverified items');
    assert.deepEqual(info.fmtFail, [], tag + ': format not honored');
    assert.equal(info.uniq, info.n, tag + ': every question is distinct');
    assert.ok(info.skills.length === 1 && info.skills[0] === skill, tag + ': only the requested skill (' + info.skills + ')');
    if (fmt === 'mc') assert.ok(info.keys.length === info.n && info.keys.every(k => k === 4), tag + ': four choices each');
    assert.equal(info.print.student.overflow, 0, tag + ': student pages fit'); assert.equal(info.print.key.overflow, 0, tag + ': key pages fit');
    assert.doesNotMatch(info.print.student.text, /Answer:|Answer Key|✓/, tag + ': no answers on the student copy');
    assert.match(info.print.key.text, /Answer Key/, tag + ': key printed');
    assert.ok(!info.print.student.upperAnd, tag + ': no uppercase AND/OR inside sentences');
    assert.deepEqual(errs, [], tag + ': page errors ' + errs.join('; '));
    if (process.env.SHOTS) { await page.evaluate(async () => { const S = MKMENU.app.state(), pages = await MKMENU.renderPages(S, 0, 'student'), root = document.getElementById('printRoot'); root.innerHTML = ''; pages.slice(0, 1).forEach(p => root.appendChild(p)); document.querySelectorAll('body > *:not(#printRoot)').forEach(e => e.style.display = 'none'); root.style.display = 'block'; });
      await page.screenshot({ path: path.join(process.env.SHOTS, skill + '-' + level + '-' + fmt + '.png'), fullPage: true }); }
    built++; await ctx.close();
  }
  console.log('Coverage-gap browser checks passed: ' + built + ' worksheets built, verified, printed and fitted.');
  await browser.close(); server.close();
})().catch(e => { console.error(e); process.exit(1); });
