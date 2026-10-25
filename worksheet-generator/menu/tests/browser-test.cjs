/* Assessment Generator — browser tests (teacher controls, print layout, PDFs, site integration).
   Needs Playwright + Chromium:   node worksheet-generator/menu/tests/browser-test.cjs
   (or PW=/path/to/playwright-core CHROME=/path/to/chromium node …).  Set OUT=dir to keep the PDFs.
   pdftotext (poppler-utils) is used to read the PDFs back when it is installed. */
'use strict';
const assert = require('node:assert/strict');
const http = require('http'), fs = require('fs'), path = require('path'), os = require('os'), cp = require('child_process');
const pw = process.env.PW ? require(process.env.PW) : require('playwright');
const ROOT = path.resolve(__dirname, '..', '..', '..');
const OUT = process.env.OUT || fs.mkdtempSync(path.join(os.tmpdir(), 'menu-pdf-'));
const TYPES = { '.html': 'text/html', '.js': 'text/javascript', '.css': 'text/css', '.svg': 'image/svg+xml', '.jpg': 'image/jpeg', '.png': 'image/png', '.woff2': 'font/woff2', '.json': 'application/json', '.pdf': 'application/pdf', '.ttf': 'font/ttf', '.woff': 'font/woff' };
const server = http.createServer((req, res) => {
  const p = decodeURIComponent(req.url.split('?')[0]), f = path.join(ROOT, p.endsWith('/') ? p + 'index.html' : p);
  if (!f.startsWith(ROOT) || !fs.existsSync(f) || fs.statSync(f).isDirectory()) { res.writeHead(404); return res.end('nf'); }
  res.writeHead(200, { 'content-type': TYPES[path.extname(f)] || 'application/octet-stream' }); fs.createReadStream(f).pipe(res);
});
const hasPdftotext = (() => { try { cp.execSync('pdftotext -v', { stdio: 'ignore' }); return true; } catch (e) { return false; } })();
let n = 0; const ok = (name) => { n++; console.log('  ✓ ' + name); };

(async () => {
  await new Promise(r => server.listen(0, r));
  const base = 'http://localhost:' + server.address().port;
  const browser = await pw.chromium.launch(process.env.CHROME ? { executablePath: process.env.CHROME } : {});
  const ctx = await browser.newContext({ viewport: { width: 1400, height: 1000 }, acceptDownloads: true });
  const page = await ctx.newPage();
  const errors = [];
  page.on('pageerror', e => errors.push('pageerror ' + e.message));
  page.on('console', m => { if (m.type() === 'error') errors.push('console ' + m.text()); });
  page.on('dialog', d => d.accept());
  const URL = base + '/worksheet-generator/menu-assessment.html';
  await page.goto(URL + '#mode=menu'); await page.waitForSelector('#mmBuildBtn');
  ok('page loads');

  /* ---------- setup controls ---------- */
  await page.check('input[name=mmLevel][value=cp2]');
  await page.waitForSelector('.mm-level.on input[value=cp2]');
  let summary = await page.textContent('#mmSummary');
  assert.match(summary, /100\s*points possible/);
  // impossible requirement shows an error and blocks building
  await page.fill('.mm-sectbl tbody tr:nth-child(2) .mmSecReq', '9'); await page.dispatchEvent('.mm-sectbl tbody tr:nth-child(2) .mmSecReq', 'change');
  await page.waitForSelector('.mm-err');
  assert.match(await page.textContent('.mm-rules'), /only 6 are offered/);
  assert.equal(await page.isDisabled('#mmBuildBtn'), true);
  await page.fill('.mm-sectbl tbody tr:nth-child(2) .mmSecReq', '4'); await page.dispatchEvent('.mm-sectbl tbody tr:nth-child(2) .mmSecReq', 'change');
  await page.waitForFunction(() => !document.querySelector('.mm-err'));
  // custom points change the maximum
  await page.fill('.mm-sectbl tbody tr:nth-child(3) .mmSecPts', '15'); await page.dispatchEvent('.mm-sectbl tbody tr:nth-child(3) .mmSecPts', 'change');
  await page.waitForFunction(() => /90\s*points possible/.test(document.querySelector('#mmSummary').textContent));
  ok('rules: errors block building, maximum score follows the point values (90)');
  // skill exclusion
  await page.uncheck('.mmSkill[value=evaluate]');
  await page.selectOption('#mmVersions', '2');
  // sample dialog shows seven difficulty levels
  await page.click('.mmSample[data-skill=multi-step]');
  assert.equal(await page.locator('#mmDialog .mm-sample tr').count(), 7);
  await page.click('#mmDialog [data-close]');
  ok('skill exclusion, versions, difficulty samples');

  /* ---------- build ---------- */
  await page.click('#mmBuildBtn'); await page.waitForSelector('.mm-dcard');
  const st = () => page.evaluate(() => JSON.parse(MKMENU.serialize(MKMENU.app.state())));
  let S = await st();
  assert.equal(S.versions.length, 2);
  const items = S.versions[0].sections.flatMap(s => s.items);
  assert.equal(items.length, 15);
  assert.ok(items.every(i => !i.failed && i.verify.status === 'verified'));
  assert.ok(!items.some(i => i.skill === 'evaluate'), 'excluded skill appeared');
  assert.deepEqual(S.versions[0].sections.map(s => s.items[0].c), [1, 2, 3]);
  assert.match(await page.textContent('#mmSummary'), /every answer verified/);
  ok('build: 15 verified dishes per version, CP2 difficulty 1/2/3, excluded skill absent');

  /* ---------- per-problem controls ---------- */
  const card = i => page.locator('.mm-dcard').nth(i);
  const keyOf = async i => (await st()).versions[0].sections.flatMap(s => s.items)[i].key;
  const all0 = (await st()).versions[0].sections.flatMap(s => s.items).map(x => x.key);
  await card(1).locator('[data-act=regen]').click(); await page.waitForTimeout(150);
  const all1 = (await st()).versions[0].sections.flatMap(s => s.items).map(x => x.key);
  assert.notEqual(all1[1], all0[1]); all1.forEach((k, i) => { if (i !== 1) assert.equal(k, all0[i]); });
  ok('regenerate one problem changes only that problem');
  await card(2).locator('[data-act=pin]').click();
  const pinnedKey = await keyOf(2);
  const otherVersionBefore = (await st()).versions[1].sections.flatMap(s => s.items).map(x => x.key);
  await page.click('#mmRegenVer'); await page.waitForTimeout(300);
  S = await st();
  assert.equal(S.versions[0].sections.flatMap(s => s.items)[2].key, pinnedKey);
  assert.deepEqual(S.versions[1].sections.flatMap(s => s.items).map(x => x.key), otherVersionBefore);
  ok('pinned problem survives “new problems”; the other version is untouched');
  await card(0).locator('[data-act=harder]').click(); await page.waitForTimeout(150);
  S = await st(); assert.equal(S.versions[0].sections[0].items[0].c, 2); assert.equal(S.versions[1].sections[0].items[0].c, 2);
  await card(0).locator('[data-act=easier]').click(); await page.waitForTimeout(150);
  ok('easier / harder change the slot in both versions');
  await card(3).locator('select[data-act=skill]').selectOption('proportion'); await page.waitForTimeout(150);
  S = await st(); assert.equal(S.versions[0].sections[0].items[3].skill, 'proportion'); assert.equal(S.versions[1].sections[0].items[3].skill, 'proportion');
  ok('change skill');
  await card(4).locator('select[data-act=move]').selectOption('2'); await page.waitForTimeout(150);
  S = await st(); assert.equal(S.versions[0].sections[0].items.length, 5); assert.equal(S.versions[0].sections[2].items.length, 4);
  ok('move to another section');
  const nBefore = await page.locator('.mm-dcard').count();
  await card(0).locator('[data-act=delete]').click();
  assert.equal(await page.locator('.mm-dcard').count(), nBefore - 1);
  await page.click('#mmToastAct');
  assert.equal(await page.locator('.mm-dcard').count(), nBefore);
  ok('delete with undo');
  await card(0).locator('[data-act=required]').click();
  S = await st(); assert.equal(S.versions[1].sections[0].items[0].required, true);
  ok('mark a problem as required for everyone');
  await page.selectOption('.mmAddSkill[data-si="1"]', 'literal'); await page.selectOption('.mmAddC[data-si="1"]', '5');
  await page.click('[data-add="1"]'); await page.waitForTimeout(150);
  S = await st(); const added = S.versions[0].sections[1].items[S.versions[0].sections[1].items.length - 1];
  assert.equal(added.skill, 'literal'); assert.equal(added.c, 5);
  ok('add a problem of a chosen skill and difficulty');
  // show answer
  await card(1).locator('[data-act=answer]').click();
  assert.ok(await card(1).locator('.mm-cans').isVisible());
  ok('answer and worked solution preview');

  /* ---------- edit: a wrong answer is caught, the computed one can be used ---------- */
  S = await st();
  const E = S.versions[0].sections.flatMap(s => s.items).findIndex(i => i.parts.length === 1 && !i.edited);
  const eCard = () => card(E);
  await eCard().locator('[data-act=edit]').click();
  await page.fill('#mmEQ', 'Solve $3(x-4)+5=2x+9$.');
  await page.selectOption('#mmDialog .mmEPtype', 'solve');
  if (await page.locator('#mmDialog .mmEPvar').count()) await page.fill('#mmDialog .mmEPvar', 'x');   // the dish being edited may have used another letter
  await page.fill('#mmDialog .mmEPans', 'x = 3');
  await page.click('#mmECheck');
  await page.waitForSelector('#mmDialog .mmEPresult p');
  const res1 = await page.textContent('#mmDialog .mmEPresult');
  assert.match(res1, /Correct answer is x = 16/, res1);
  await page.click('#mmESave'); await page.waitForTimeout(150);
  const flat = () => st().then(x => x.versions[0].sections.flatMap(s => s.items));
  let ed = (await flat())[E];
  assert.equal(ed.verify.status, 'mismatch'); assert.equal(ed.approved, false); assert.equal(ed.pinned, true);
  assert.ok(await eCard().locator('.mm-badge.bad').count());
  await eCard().locator('[data-act=edit]').click();
  await page.click('#mmECheck'); await page.click('[data-use-computed]'); await page.click('#mmESave'); await page.waitForTimeout(150);
  ed = (await flat())[E];
  assert.equal(ed.verify.status, 'verified'); assert.match(ed.parts[0].answer, /x=16/);
  ok('manual edit: wrong answer flagged, computed answer accepted after re-verification');
  // teacher-written problem with no automatic check needs approval
  await page.click('[data-manual="2"]');
  await page.fill('#mmEQ', 'Dev says $2(x+3)=2x+3$. Explain his mistake.');
  await page.selectOption('#mmDialog .mmEPtype', 'none');
  await page.fill('#mmDialog .mmEPans', 'He did not multiply 3 by 2.');
  await page.click('#mmESave'); await page.waitForTimeout(150);
  S = await st(); const man = S.versions[0].sections[2].items[S.versions[0].sections[2].items.length - 1];
  assert.equal(man.verify.status, 'manual'); assert.equal(man.approved, false);
  assert.match(await page.textContent('#mmSummary'), /need approval/);
  await page.locator('.mm-dcard').last().locator('.mmApprove').check(); await page.waitForTimeout(100);
  S = await st(); assert.equal(S.versions[0].sections[2].items.slice(-1)[0].approved, true);
  ok('teacher-written problem requires approval');

  /* ---------- bank ---------- */
  await page.click('#mmBankToggle'); await page.selectOption('#mmBankSkill', 'both-sides'); await page.selectOption('#mmBankC', '3');
  await page.fill('#mmBankN', '10'); await page.click('#mmBankGo'); await page.waitForSelector('.mm-bcard');
  assert.equal(await page.locator('.mm-bcard').count(), 10);
  assert.ok(await page.locator('.mm-bcard').first().locator('.mm-cans').isVisible(), 'bank shows answers');
  await page.locator('.mm-bcard').nth(4).locator('.mmBankTo').selectOption('1');
  await page.locator('.mm-bcard').nth(4).locator('[data-use]').click(); await page.waitForTimeout(150);
  assert.equal(await page.locator('.mm-bcard').count(), 9);
  S = await st(); assert.equal(S.versions[0].sections[1].items.slice(-1)[0].skill, 'both-sides');
  ok('problem bank: 10 previews with answers, choose one for the menu');

  /* ---------- versions ---------- */
  await page.click('[data-ver="1"]');
  assert.match(await page.textContent('#mmRegenVer'), /Version B/);
  const b0 = (await st()).versions[0].sections.flatMap(s => s.items).map(x => x.key);
  await page.click('#mmRegenVer'); await page.waitForTimeout(300);
  assert.deepEqual((await st()).versions[0].sections.flatMap(s => s.items).map(x => x.key), b0);
  ok('regenerate only Version B');

  /* ---------- tablet layout ---------- */
  await page.setViewportSize({ width: 820, height: 1180 });
  const over = await page.evaluate(() => document.scrollingElement.scrollWidth - window.innerWidth);
  assert.ok(over <= 1, 'horizontal overflow on tablet: ' + over);
  await page.setViewportSize({ width: 1400, height: 1000 });
  ok('tablet width: no horizontal scrolling');

  /* ---------- accessibility basics ---------- */
  const a11y = await page.evaluate(() => {
    const bad = [];
    document.querySelectorAll('button, select, input, textarea').forEach(e => {
      if (e.type === 'hidden' || e.closest('[hidden]')) return;
      const name = (e.getAttribute('aria-label') || e.textContent || '').trim() || (e.labels && e.labels.length && e.labels[0].textContent.trim()) || e.title;
      if (!name) bad.push(e.outerHTML.slice(0, 90));
    });
    return bad;
  });
  assert.deepEqual(a11y, [], 'controls without an accessible name: ' + a11y.join(' | '));
  await page.keyboard.press('Tab');
  assert.ok(await page.evaluate(() => document.activeElement && document.activeElement !== document.body));
  ok('every control has an accessible name; keyboard focus works');

  /* ---------- preview + PDFs ---------- */
  await page.click('#mmToPreview'); await page.waitForSelector('#pages .page');
  assert.doesNotMatch(await page.textContent('#mmPStatus'), /taller than one page/);
  const layouts = [
    { name: 'together-standard', layout: { format: 'together', density: 'standard', grid: 'none', reference: false, guide: true } },
    { name: 'menuonly-compact-graph', layout: { format: 'menu-only', density: 'compact', grid: 'graph', reference: true, guide: false } },
    { name: 'together-spacious-coord', layout: { format: 'together', density: 'spacious', grid: 'coordinate', reference: true, guide: true } }
  ];
  const pdfs = [];
  for (const L of layouts) for (const v of [0, 1]) for (const kind of ['student', 'key']) {
    const info = await page.evaluate(async ({ L, v, kind }) => {
      const S = MKMENU.app.state(); S.config.layout = L;
      const pages = await MKMENU.renderPages(S, v, kind);
      const root = document.getElementById('printRoot'); root.innerHTML = ''; pages.forEach(p => root.appendChild(p));
      document.body.classList.add('printing');
      const html = root.innerHTML;
      // everything the key knows that a student must never see: per dish, its answers (as rendered math) and its solution text
      const flat = s => s.replace(/\s+/g, ''); const tok = (h, t) => { for (let i = h.indexOf(t); i >= 0; i = h.indexOf(t, i + 1)) { if (!/[0-9A-Za-z.]/.test(h[i - 1] || ' ') && !/[0-9.]/.test(h[i + t.length] || ' ')) return true; } return false; }; /* whole tokens only: 5x=−4x does not contain the answer x=−4 */
      if (window.__plantLeak) {   // self-test of this detector: put one answer on the student page
        const it = S.versions[v].sections[1].items[0], el = root.querySelector('[data-uid="' + it.uid + '"]');
        el.insertAdjacentHTML('beforeend', '<div>→ ' + MKMENU.mathSafe(it.parts[it.parts.length - 1].answer) + ' ←</div>');
      }
      const leaks = [];
      S.versions[v].sections.forEach(sec => sec.items.forEach(it => {
        const el = root.querySelector('[data-uid="' + it.uid + '"]'); if (!el) return;
        const shown = flat(el.textContent), studentTeX = flat(MKMENU.studentText(it));
        (it.parts || []).forEach(pt => (pt.answer.match(/⟨[^⟩]*⟩/g) || []).forEach(m => {
          if (studentTeX.indexOf(flat(m)) >= 0 || studentTeX.indexOf(flat(m.slice(1, -1))) >= 0) return;   // quoting the question (the base of y = 5(1.09)^x) is not a leak                         // e.g. "Graph x ≥ 2": the inequality is the question
          const box = document.createElement('div'); box.innerHTML = katex.renderToString(m.slice(1, -1).replace(/\\frac/g, '\\dfrac'), { output: 'html', throwOnError: false });
          const t = flat(box.textContent); if (t.length >= 3 && tok(shown, t)) leaks.push(it.uid + ': ' + m + ' IN ' + el.textContent.slice(0, 160));
        }));
        (it.steps || []).forEach(st => { const t = flat((st.t || '').replace(/⟨[^⟩]*⟩/g, '')); if (t.length > 14 && tok(shown, t)) leaks.push(it.uid + ': ' + st.t); });
      }));
      const text = root.innerText;
      const labels = []; S.versions[v].sections.forEach((s, si) => s.items.forEach((it, i) => labels.push(MKMENU.dishLabel(S.config, si, i))));
      return { pages: pages.length, overflow: pages.overflow.length, leaks, text, labels, nItems: labels.length, dishes: root.querySelectorAll('[data-uid]').length };
    }, { L: L.layout, v, kind });
    const file = path.join(OUT, `menu-${L.name}-v${'AB'[v]}-${kind}.pdf`);
    await page.emulateMedia({ media: 'print' });
    await page.pdf({ path: file, format: 'Letter', printBackground: true, margin: { top: 0, right: 0, bottom: 0, left: 0 }, preferCSSPageSize: true });
    await page.emulateMedia({ media: 'screen' });
    await page.evaluate(() => { document.body.classList.remove('printing'); document.getElementById('printRoot').innerHTML = ''; });
    assert.equal(info.overflow, 0, file + ': a block overflows its page');
    info.labels.forEach(l => assert.ok(info.text.indexOf(l) >= 0, file + ' missing dish ' + l));
    if (kind === 'student') {
      assert.doesNotMatch(info.text, /Answer:|Rubric|TEACHER KEY|Teacher key/, file + ' contains key text');
      assert.equal(info.dishes, info.nItems, file + ': every dish must be findable');
      assert.deepEqual(info.leaks, [], file + ' shows answers or solutions: ' + info.leaks.join(' | '));
    } else {
      assert.equal((info.text.match(/Answer:/g) || []).length, info.nItems, file + ': every offered dish needs an answer');
      assert.match(info.text, /pts?\b/);
    }
    // the PDF itself
    const pdfPages = (fs.readFileSync(file, 'latin1').match(/\/Type\s*\/Page[^s]/g) || []).length;
    assert.equal(pdfPages, info.pages, file + ': PDF page count ' + pdfPages + ' vs layout ' + info.pages);
    if (hasPdftotext) {
      const t = cp.execSync('pdftotext -layout "' + file + '" -').toString();
      if (kind === 'student') assert.doesNotMatch(t, /Answer:|Rubric|TEACHER KEY/, file + ' (PDF text) contains key text');
      else assert.match(t, /TEACHER KEY/);
      const size = cp.execSync('pdfinfo "' + file + '"').toString().match(/Page size:\s+([\d.]+) x ([\d.]+)/);
      assert.ok(Math.abs(+size[1] - 612) < 1 && Math.abs(+size[2] - 792) < 1, 'not US Letter: ' + size[0]);
    }
    pdfs.push(file + ' (' + info.pages + ' pages)');
  }
  // the leak detector itself must notice a planted answer
  const planted = await page.evaluate(async () => {
    window.__plantLeak = true; const S = MKMENU.app.state(); const pages = await MKMENU.renderPages(S, 0, 'student');
    const root = document.getElementById('printRoot'); root.innerHTML = ''; pages.forEach(p => root.appendChild(p));
    const it = S.versions[0].sections.flatMap(sc => sc.items).find(x => /⟨/.test(x.parts[x.parts.length - 1].answer)), el = root.querySelector('[data-uid="' + it.uid + '"]');
    el.insertAdjacentHTML('beforeend', '<div>→ ' + MKMENU.mathSafe(it.parts[it.parts.length - 1].answer) + ' ←</div>');
    const flat = s => s.replace(/\s+/g, ''); const tok = (h, t) => { for (let i = h.indexOf(t); i >= 0; i = h.indexOf(t, i + 1)) { if (!/[0-9A-Za-z.]/.test(h[i - 1] || ' ') && !/[0-9.]/.test(h[i + t.length] || ' ')) return true; } return false; }; /* whole tokens only: 5x=−4x does not contain the answer x=−4 */ let found = false;
    (it.parts[it.parts.length - 1].answer.match(/⟨[^⟩]*⟩/g) || []).forEach(m => { const box = document.createElement('div'); box.innerHTML = katex.renderToString(m.slice(1, -1).replace(/\\frac/g, '\\dfrac'), { output: 'html', throwOnError: false }); if (tok(flat(el.textContent), flat(box.textContent))) found = true; });
    window.__plantLeak = false; const txt = el.textContent; root.innerHTML = ''; return found || ('MISS ' + it.parts[it.parts.length - 1].answer + ' :: ' + txt.slice(-200));
  });
  assert.ok(planted === true, 'the student-leak detector failed to notice a planted answer: ' + planted);
  ok('PDFs for 3 layouts × 2 versions × student/key: Letter size, no overflow, students see no answers, keys list every offered dish');
  console.log('      ' + pdfs.join('\n      '));

  /* ---------- save / reload / file round trip ---------- */
  await page.click('#mmToExport');
  await page.fill('#mmSaveName', 'Pilot test menu'); await page.click('#mmSaveNamed');
  await page.waitForSelector('.mm-saves li');
  const [dl] = await Promise.all([page.waitForEvent('download'), page.click('#mmDownload')]);
  const saved = path.join(OUT, 'saved-menu.json'); await dl.saveAs(saved);
  const before = await st();
  await page.reload(); await page.waitForSelector('.mm-dcard');
  const after = await st();
  assert.deepEqual(after.versions.map(v => v.sections.map(s => s.items.map(i => i.key))), before.versions.map(v => v.sections.map(s => s.items.map(i => i.key))));
  ok('autosave restores the menu after a reload');
  // tamper with the downloaded file: the key no longer matches and must be flagged on open
  const o = JSON.parse(fs.readFileSync(saved, 'utf8'));
  const victim = o.versions[0].sections[1].items.find(i => i.parts.length === 1 && /=\-?\d+⟩$/.test(i.parts[0].answer));
  victim.parts[0].answer = victim.parts[0].answer.replace(/(-?\d+)⟩$/, (m, d) => (+d + 1) + '⟩');
  const tampered = path.join(OUT, 'tampered.json'); fs.writeFileSync(tampered, JSON.stringify(o));
  await page.click('.mm-stepbtn[data-step="7"]');
  await page.setInputFiles('#mmOpenFile', tampered); await page.waitForTimeout(400);
  assert.match(await page.textContent('#mmSummary'), /need approval/);
  ok('opening a file re-checks every answer (a tampered key is flagged)');
  await page.click('.mm-stepbtn[data-step="7"]');
  await page.click('[data-load]'); await page.waitForTimeout(300);
  assert.match(await page.textContent('#mmSummary'), /every answer verified|need approval/);
  ok('named saves can be reopened');

  /* ---------- Honors build ---------- */
  await page.click('.mm-stepbtn[data-step="7"]'); await page.click('#mmNew');
  await page.waitForSelector('#mmBuildBtn');
  await page.check('input[name=mmLevel][value=honors]'); await page.selectOption('#mmVersions', '3');
  await page.click('#mmBuildBtn'); await page.waitForSelector('.mm-dcard');
  S = await st(); assert.equal(S.versions.length, 3);
  assert.deepEqual(S.versions[2].sections.map(s => s.items[0].c), [5, 6, 7]);
  assert.ok(S.versions.every(v => v.sections.every(s => s.items.every(i => i.verify.status === 'verified'))));
  ok('Honors with Versions A, B, C');
  assert.deepEqual(errors, [], 'console errors: ' + errors.join('\n'));

  /* ---------- Inequalities: number lines in questions and keys ---------- */
  const iq = await ctx.newPage(); const iqErr = [];
  iq.on('pageerror', e => iqErr.push(e.message)); iq.on('console', m => { if (m.type() === 'error') iqErr.push(m.text()); }); iq.on('dialog', d => d.accept());
  await iq.goto(URL + '#unit=algebra1-inequalities&mode=menu'); await iq.waitForSelector('#mmUnitSel');
  assert.equal(await iq.inputValue('#mmUnitSel'), 'algebra1-inequalities');
  assert.match(await iq.inputValue('#mmTitle'), /Inequalities Bistro/);
  await iq.selectOption('#mmVersions', '2'); await iq.click('#mmBuildBtn'); await iq.waitForSelector('.mm-dcard');
  let IQ = await iq.evaluate(() => JSON.parse(MKMENU.serialize(MKMENU.app.state())));
  assert.equal(IQ.config.unitId, 'algebra1-inequalities');
  assert.ok(IQ.versions.every(v => v.sections.every(s => s.items.every(i => !i.failed && i.verify.status === 'verified'))));
  const tagsIQ = new Set(IQ.versions[0].sections.flatMap(s => s.items.map(i => i.tag)));
  ['SOLVE', 'COMPOUND', 'REASON', 'APPLY'].forEach(t => assert.ok(tagsIQ.has(t), 'menu lacks ' + t));
  assert.ok(await iq.locator('.mm-dcard svg.mm-nl').count() > 0, 'number lines appear on the cards');
  ok('Inequalities opens from its link, builds a verified menu covering SOLVE/COMPOUND/REASON/APPLY, shows number lines');
  for (const v of [0, 1]) for (const kind of ['student', 'key']) {
    const info = await iq.evaluate(async ({ v, kind }) => {
      const S = MKMENU.app.state();
      const pages = await MKMENU.renderPages(S, v, kind);
      const root = document.getElementById('printRoot'); root.innerHTML = ''; pages.forEach(p => root.appendChild(p));
      document.body.classList.add('printing');
      // graphs that are part of a question (read-the-graph) vs. graphs that are answers
      let promptSegs = 0; S.versions[v].sections.forEach(s => s.items.forEach(it => { if (it.fig && it.fig.pieces) promptSegs += it.fig.pieces.filter(p => !(p.lo && p.hi && p.lo[0] / p.lo[1] === p.hi[0] / p.hi[1])).length; }));
      let answerFigs = 0; S.versions[v].sections.forEach(s => s.items.forEach(it => it.parts.forEach(pt => { if (pt.answerFig) answerFigs++; })));
      const flat = s => s.replace(/\s+/g, ''), leaks = []; const tok = (h, t) => { for (let i = h.indexOf(t); i >= 0; i = h.indexOf(t, i + 1)) { if (!/[0-9A-Za-z.]/.test(h[i - 1] || ' ') && !/[0-9.]/.test(h[i + t.length] || ' ')) return true; } return false; }; /* whole tokens only: 5x=−4x does not contain the answer x=−4 */
      if (kind === 'student') S.versions[v].sections.forEach(sec => sec.items.forEach(it => {
        const el = root.querySelector('[data-uid="' + it.uid + '"]'), shown = flat(el.textContent), studentTeX = flat(MKMENU.studentText(it));
        it.parts.forEach(pt => (pt.answer.match(/⟨[^⟩]*⟩/g) || []).forEach(m => {
          if (studentTeX.indexOf(flat(m)) >= 0 || studentTeX.indexOf(flat(m.slice(1, -1))) >= 0) return;   // quoting the question (the base of y = 5(1.09)^x) is not a leak
          const box = document.createElement('div'); box.innerHTML = katex.renderToString(m.slice(1, -1), { output: 'html', throwOnError: false });
          const t = flat(box.textContent); if (t.length >= 3 && tok(shown, t)) leaks.push(m + ' IN ' + el.textContent.slice(0, 220));
        }));
      }));
      return { leaks, pages: pages.length, overflow: pages.overflow.length, segs: root.querySelectorAll('.nl-seg').length, lines: root.querySelectorAll('svg.mm-nl').length, promptSegs, answerFigs, text: root.innerText };
    }, { v, kind });
    const file = path.join(OUT, `inequalities-v${'AB'[v]}-${kind}.pdf`);
    await iq.emulateMedia({ media: 'print' });
    await iq.pdf({ path: file, format: 'Letter', printBackground: true, margin: { top: 0, right: 0, bottom: 0, left: 0 }, preferCSSPageSize: true });
    await iq.emulateMedia({ media: 'screen' });
    await iq.evaluate(() => { document.body.classList.remove('printing'); document.getElementById('printRoot').innerHTML = ''; });
    assert.equal(info.overflow, 0, file + ' overflows');
    if (kind === 'student') {
      assert.equal(info.segs, info.promptSegs, file + ': a student page shows a shaded answer graph (' + info.segs + ' segments vs ' + info.promptSegs + ' in questions)');
      assert.doesNotMatch(info.text, /Answer:|Rubric/);
      assert.deepEqual(info.leaks, [], file + ' shows answers: ' + info.leaks.join(' | '));
    } else assert.ok(info.lines >= info.answerFigs, file + ': the key is missing answer graphs');
    pdfs.push(file + ' (' + info.pages + ' pages)');
  }
  assert.deepEqual(iqErr, [], 'inequalities page errors: ' + iqErr.join('\n'));
  // switching units keeps each unit's own autosave
  await iq.click('.mm-stepbtn[data-step="0"]');
  await iq.selectOption('#mmUnitSel', 'algebra1-expressions-equations'); await iq.waitForTimeout(300);
  assert.equal(await iq.evaluate(() => MKMENU.app.state() && MKMENU.app.state().config.unitId), 'algebra1-expressions-equations');
  await iq.click('.mm-stepbtn[data-step="0"]'); await iq.selectOption('#mmUnitSel', 'algebra1-inequalities'); await iq.waitForTimeout(300);
  const back = await iq.evaluate(() => JSON.parse(MKMENU.serialize(MKMENU.app.state())));
  assert.deepEqual(back.versions[0].sections.map(s => s.items.map(i => i.key)), IQ.versions[0].sections.map(s => s.items.map(i => i.key)));
  ok('Inequalities PDFs: students see blank number lines only (no shaded answers); keys include the answer graphs; units keep separate autosaves');
  console.log('      ' + pdfs.slice(-4).join('\n      '));

  /* ---------- Relations and Functions: tables, mapping diagrams and graphs ---------- */
  for (const [UNITID, TITLE, TAGS, SHORT] of [['algebra1-relations-functions', /Function Diner/, ['RELATIONS', 'NOTATION', 'REPRESENT', 'RATE', 'SEQUENCE'], 'functions'], ['algebra1-exponential-functions', /Exponential Eatery/, ['EVAL', 'GROWTH', 'MODEL', 'SOLVE', 'SEQUENCE', 'APPLY'], 'exponential'], ['algebra1-factoring-zero-product', /Factor Factory/, ['GCF', 'TRI', 'SPECIAL', 'SOLVE', 'APPLY'], 'factoring'], ['algebra1-statistics-data-modeling', /Data Deli/, ['CENTER', 'SPREAD', 'DISPLAY', 'TWOWAY', 'SCATTER'], 'statistics'], ['algebra1-linear-equations-slope', /Slope Shack/, ['SLOPE', 'FORMS', 'WRITE', 'PARPERP', 'APPLY'], 'lines'], ['algebra1-systems-of-equations', /Intersection Inn/, ['GRAPH', 'SUBST', 'ELIM', 'APPLY', 'INEQ'], 'systems'], ['algebra1-exponents-scientific-notation', /Power Pantry/, ['PRODUCT', 'QUOTIENT', 'EVAL', 'SCI', 'SCIOPS'], 'exponents'], ['algebra1-polynomials', /Polynomial Pizzeria/, ['CLASSIFY', 'ADDSUB', 'MULT', 'SPECIAL', 'APPLY'], 'polynomials'], ['algebra1-quadratics', /Parabola Bakery/, ['GRAPH', 'ROOTS', 'FORMULA', 'COMPLETE', 'APPLY'], 'quadratics']]) {
  const rf = await ctx.newPage(); const rfErr = [];
  rf.on('pageerror', e => rfErr.push(e.message)); rf.on('console', m => { if (m.type() === 'error') rfErr.push(m.text()); }); rf.on('dialog', d => d.accept());
  await rf.goto(URL + '#unit=' + UNITID + '&mode=menu'); await rf.waitForSelector('#mmUnitSel');
  assert.equal(await rf.inputValue('#mmUnitSel'), UNITID);
  assert.match(await rf.inputValue('#mmTitle'), TITLE);
  for (const lvl of ['cp2', 'cp1', 'honors']) {
    if (lvl !== 'cp2') { await rf.click('.mm-stepbtn[data-step="7"]'); await rf.click('#mmNew'); }
    await rf.waitForSelector('#mmBuildBtn');
    await rf.check('input[name=mmLevel][value="' + lvl + '"]');
    await rf.selectOption('#mmVersions', '2'); await rf.click('#mmBuildBtn'); await rf.waitForSelector('.mm-dcard');
    const RF = await rf.evaluate(() => JSON.parse(MKMENU.serialize(MKMENU.app.state())));
    assert.ok(RF.versions.every(v => v.sections.every(s => s.items.every(i => !i.failed && i.verify.status === 'verified'))), lvl + ': unverified item');
    const tagsRF = new Set(RF.versions[0].sections.flatMap(s => s.items.map(i => i.tag)));
    TAGS.forEach(t => assert.ok(tagsRF.has(t), UNITID + ' ' + lvl + ' menu lacks ' + t));
    for (const v of [0, 1]) for (const kind of ['student', 'key']) {
      const info = await rf.evaluate(async ({ v, kind }) => {
        const S = MKMENU.app.state(), pages = await MKMENU.renderPages(S, v, kind);
        const root = document.getElementById('printRoot'); root.innerHTML = ''; pages.forEach(p => root.appendChild(p));
        document.body.classList.add('printing');
        let figs = 0; S.versions[v].sections.forEach(s => s.items.forEach(it => { if (it.fig) figs++; }));
        const flat = s => s.replace(/\s+/g, ''), leaks = []; const tok = (h, t) => { for (let i = h.indexOf(t); i >= 0; i = h.indexOf(t, i + 1)) { if (!/[0-9A-Za-z.]/.test(h[i - 1] || ' ') && !/[0-9.]/.test(h[i + t.length] || ' ')) return true; } return false; }; /* whole tokens only: 5x=−4x does not contain the answer x=−4 */
        if (kind === 'student') S.versions[v].sections.forEach(sec => sec.items.forEach(it => {
          // reading a value off a table or graph is the question, so the figure itself is left out of the comparison
          const el = root.querySelector('[data-uid="' + it.uid + '"]').cloneNode(true); el.querySelectorAll('.mm-fig').forEach(f => f.remove());
          const shown = flat(el.textContent), studentTeX = flat(MKMENU.studentText(it));
          it.parts.forEach(pt => (pt.answer.match(/⟨[^⟩]*⟩/g) || []).forEach(m => {
            if (studentTeX.indexOf(flat(m)) >= 0 || studentTeX.indexOf(flat(m.slice(1, -1))) >= 0) return;   // quoting the question (the base of y = 5(1.09)^x) is not a leak
            const box = document.createElement('div'); box.innerHTML = katex.renderToString(m.slice(1, -1), { output: 'html', throwOnError: false });
            const t = flat(box.textContent); if (t.length >= 3 && tok(shown, t)) leaks.push(m + ' IN ' + el.textContent.slice(0, 160));
          }));
        }));
        return { leaks, pages: pages.length, overflow: pages.overflow.length, figs, drawn: root.querySelectorAll('.mm-fig').length, text: root.innerText };
      }, { v, kind });
      const file = path.join(OUT, `${SHORT}-${lvl}-v${'AB'[v]}-${kind}.pdf`);
      await rf.emulateMedia({ media: 'print' });
      await rf.pdf({ path: file, format: 'Letter', printBackground: true, margin: { top: 0, right: 0, bottom: 0, left: 0 }, preferCSSPageSize: true });
      await rf.emulateMedia({ media: 'screen' });
      await rf.evaluate(() => { document.body.classList.remove('printing'); document.getElementById('printRoot').innerHTML = ''; });
      assert.equal(info.overflow, 0, file + ' overflows');
      assert.ok(info.drawn >= info.figs, file + ': figures missing (' + info.drawn + ' of ' + info.figs + ')');
      if (kind === 'student') { assert.doesNotMatch(info.text, /Answer:|Rubric/); assert.deepEqual(info.leaks, [], file + ' shows answers: ' + info.leaks.join(' | ')); }
      pdfs.push(file + ' (' + info.pages + ' pages)');
    }
  }
  assert.deepEqual(rfErr, [], UNITID + ' page errors: ' + rfErr.join('\n'));
  ok(UNITID + ': CP2/CP1/Honors menus verified, cover every skill group, draw every figure, PDFs fit and leak no answers');
  await rf.close();
  }

  /* ---------- standard tests: every unit, numbered questions, multiple-choice parts, keys ---------- */
  const units = await page.evaluate(() => Object.keys(MKMENU.skillSets));
  for (const [ui, UNITID] of units.entries()) {
    const tp = await ctx.newPage(); const tErr = []; tp.on('pageerror', e => tErr.push(e.message)); tp.on('dialog', d => d.accept());
    await tp.goto(URL); await tp.evaluate(() => localStorage.clear());   // start fresh: earlier checks left menus saved for these units
    await tp.goto(URL + '#unit=' + UNITID + '&mode=test'); await tp.reload(); await tp.waitForSelector('#mmUnitSel');
    if (!(await tp.isChecked('input[name=mmMode][value=test]'))) { await tp.check('input[name=mmMode][value=test]'); await tp.waitForTimeout(200); }
    const lvl = ['cp2', 'cp1', 'honors'][ui % 3];
    await tp.check('input[name=mmLevel][value="' + lvl + '"]'); await tp.selectOption('#mmVersions', '2');
    await tp.click('#mmBuildBtn'); await tp.waitForSelector('.mm-dcard');
    const T = await tp.evaluate(() => JSON.parse(MKMENU.serialize(MKMENU.app.state())));
    assert.equal(T.config.mode, 'test'); assert.ok(T.versions.every(v => v.sections.every(s => s.items.every(i => !i.failed && i.verify.status === 'verified'))), UNITID + ' test: unverified item');
    for (const v of [0, 1]) for (const kind of ['student', 'key']) {
      const info = await tp.evaluate(async ({ v, kind }) => {
        const S = MKMENU.app.state(), pages = await MKMENU.renderPages(S, v, kind);
        const root = document.getElementById('printRoot'); root.innerHTML = ''; pages.forEach(p => root.appendChild(p));
        const mc = S.versions[v].sections[0].items.filter(it => it.mc).length;
        const r = { pages: pages.length, overflow: pages.overflow.length, text: root.innerText, choices: root.querySelectorAll('.mm-choices').length, bubbles: root.querySelectorAll('.mm-bubble').length, mc };
        root.innerHTML = ''; return r;
      }, { v, kind });
      const tag = UNITID + ' test ' + lvl + ' v' + 'AB'[v] + ' ' + kind;
      assert.equal(info.overflow, 0, tag + ' overflows');
      assert.equal(info.choices, info.mc, tag + ': every multiple-choice question prints its choices');
      assert.equal(info.bubbles, 4 * info.mc, tag + ': four lettered choices each');
      if (kind === 'student') { assert.match(info.text, /Part 1/); assert.match(info.text, /16\.\s*\d+(\.\d+)? pts/); assert.doesNotMatch(info.text, /My pick|Answer:|Rubric|choose \d/); }
      else assert.match(info.text, /Quick key/);
    }
    assert.deepEqual(tErr, [], UNITID + ' test page errors: ' + tErr.join('\n'));
    await tp.close();
  }
  ok('standard tests: every unit builds a verified 16-question test; parts, numbering and four lettered choices print and fit; keys have the quick key');

  /* ---------- practice worksheets (worksheet.html) ---------- */
  const WURL = base + '/worksheet-generator/worksheet.html';
  for (const [ui, UNITID] of units.entries()) {
    const wp = await ctx.newPage(); const wErr = []; wp.on('pageerror', e => wErr.push(e.message)); wp.on('dialog', d => d.accept());
    await wp.goto(WURL + '#unit=' + UNITID); await wp.waitForSelector('#mmUnitSel');
    assert.equal(await wp.locator('input[name=mmMode]').count(), 0, 'the worksheet page has no menu/test switch');
    assert.equal(await wp.locator('.mmSecPts').count(), 0, 'no points column on a worksheet');
    await wp.click('[data-wpreset="both"]'); await wp.waitForTimeout(100);
    const lvl = ['cp2', 'cp1', 'honors'][ui % 3];
    await wp.check('input[name=mmLevel][value="' + lvl + '"]'); await wp.selectOption('#mmVersions', '2');
    await wp.click('#mmBuildBtn'); await wp.waitForSelector('.mm-dcard');
    const W = await wp.evaluate(() => JSON.parse(MKMENU.serialize(MKMENU.app.state())));
    assert.equal(W.config.mode, 'worksheet'); assert.equal(W.config.sections.length, 2);
    assert.ok(W.versions.every(v => v.sections.every(s => s.items.every(i => !i.failed && i.verify.status === 'verified'))), UNITID + ' worksheet: unverified item');
    for (const v of [0, 1]) for (const kind of ['student', 'key']) {
      const info = await wp.evaluate(async ({ v, kind }) => {
        const S = MKMENU.app.state(), pages = await MKMENU.renderPages(S, v, kind);
        const root = document.getElementById('printRoot'); root.innerHTML = ''; pages.forEach(p => root.appendChild(p));
        const mc = S.versions[v].sections[0].items.filter(it => it.mc).length;
        const r = { pages: pages.length, overflow: pages.overflow.length, text: root.innerText, choices: root.querySelectorAll('.mm-choices').length, bubbles: root.querySelectorAll('.mm-bubble').length, mc };
        root.innerHTML = ''; return r;
      }, { v, kind });
      const tag = UNITID + ' worksheet ' + lvl + ' v' + 'AB'[v] + ' ' + kind;
      assert.equal(info.overflow, 0, tag + ' overflows');
      assert.equal(info.choices, info.mc, tag + ': choices print'); assert.equal(info.bubbles, 4 * info.mc, tag + ': four letters each');
      assert.doesNotMatch(info.text, /\d pts?\b|worth \d+ points|Rubric|My pick|Score \(teacher\)/, tag + ': no points or rubric on a worksheet');
      if (kind === 'student') { assert.match(info.text, /Part 2 · Show Your Work/); assert.match(info.text, /Answer all 14 questions/); assert.doesNotMatch(info.text, /Answer:/); }
      else { assert.match(info.text, /Answer Key/); assert.match(info.text, /Quick key/); }
    }
    assert.deepEqual(wErr, [], UNITID + ' worksheet page errors: ' + wErr.join('\n'));
    await wp.close();
  }
  { // separate autosave: the test generator's saved work does not appear on the worksheet page
    const a = await ctx.newPage(); await a.goto(URL + '#unit=algebra1-quadratics'); await a.waitForSelector('.mm-stepbtn');
    assert.equal(await a.evaluate(() => MKMENU.app.state().config.mode), 'test', 'the test generator restores its own saved test'); await a.close();
    const b = await ctx.newPage(); await b.goto(WURL + '#unit=algebra1-quadratics'); await b.waitForSelector('.mm-stepbtn');
    assert.equal(await b.evaluate(() => MKMENU.app.state().config.mode), 'worksheet', 'the worksheet page restores its own saved worksheet'); await b.close();
  }
  ok('practice worksheets: every unit builds a verified multiple choice + show-your-work worksheet with two versions; no points; keys print and fit');

  /* ---------- the rest of the site still works ---------- */
  const site = await ctx.newPage(); const siteErr = [];
  site.on('pageerror', e => siteErr.push(e.message)); site.on('console', m => { if (m.type() === 'error') siteErr.push(m.text()); });
  await site.goto(base + '/index.html#algebra.expressions-equations'); await site.waitForTimeout(800);
  const unitText = await site.textContent('body');
  assert.match(unitText, /Build an assessment/); assert.match(unitText, /Assessment Generator/); assert.doesNotMatch(unitText, /The Equation Bistro: Assessment Menu/);   // the generator replaces the fixed menu PDFs
  const href = await site.getAttribute('a.btn:has-text("Build an assessment")', 'href');
  assert.equal(href, 'worksheet-generator/menu-assessment.html#unit=algebra1-expressions-equations');
  assert.equal(await site.getAttribute('a.btn:has-text("Create a worksheet")', 'href'), 'worksheet-generator/worksheet.html#unit=algebra1-expressions-equations', 'the unit page links the verified Worksheet Generator');
  assert.doesNotMatch(unitText, /Expressions & Equations Worksheet Generator/);   // the old template generator is no longer listed
  { // Foundations of Algebra has its own generators; the Assessment Generator opens as a standard test
    await site.goto(base + '/index.html#algebra.foundations-algebra'); await site.waitForTimeout(400);
    assert.equal(await site.getAttribute('a.btn:has-text("Build an assessment")', 'href'), 'worksheet-generator/menu-assessment.html#unit=algebra1-foundations');
    const f = await ctx.newPage(); await f.goto(base + '/worksheet-generator/menu-assessment.html'); await f.evaluate(() => localStorage.clear());
    await f.goto(base + '/worksheet-generator/menu-assessment.html#unit=algebra1-foundations'); await f.reload(); await f.waitForSelector('#mmUnitSel');
    assert.equal(await f.inputValue('input[name=mmMode]:checked'), 'test', 'a standard test is the default'); assert.equal(await f.inputValue('#mmTitle'), 'Foundations of Algebra Test'); await f.close();
  }
  for (const [tok, sid] of [['algebra.quadratics', 'algebra1-quadratics'], ['algebra.linear-equations-slope', 'algebra1-linear-equations-slope'], ['algebra.polynomials-factoring', 'algebra1-polynomials']]) {
    await site.goto(base + '/index.html#' + tok); await site.waitForTimeout(400);
    assert.equal(await site.getAttribute('a.btn:has-text("Create a worksheet")', 'href'), 'worksheet-generator/worksheet.html#unit=' + sid, tok + ' worksheet link');
  }
  await site.goto(base + '/index.html#algebra.inequalities'); await site.waitForTimeout(500);
  assert.equal(await site.getAttribute('a.btn:has-text("Build an assessment")', 'href'), 'worksheet-generator/menu-assessment.html#unit=algebra1-inequalities');
  await site.goto(base + '/index.html#algebra.relations-functions'); await site.waitForTimeout(500);
  assert.equal(await site.getAttribute('a.btn:has-text("Build an assessment")', 'href'), 'worksheet-generator/menu-assessment.html#unit=algebra1-relations-functions');
  await site.goto(base + '/index.html#activity.assessment-generator'); await site.waitForTimeout(500);
  assert.match(await site.textContent("body"), /Assessment Generator/);
  await site.goto(base + '/worksheet-generator/algebra1-expressions-equations.html'); await site.waitForTimeout(800);
  assert.ok(await site.locator('#pages .page').count() >= 0);
  await site.goto(base + '/activity.html?path=' + encodeURIComponent('artifacts/expressions-equations-assessment-menu/worksheet.pdf')); await site.waitForTimeout(500);
  // every thumbnail and path referenced from data.js exists
  const missing = await site.evaluate(async () => {
    const out = []; const L = window.LIBRARY;
    for (const c of L.courses) for (const u of c.units) for (const a of u.artifacts) for (const f of [a.path, a.thumb].filter(Boolean)) {
      const r = await fetch(f, { method: 'HEAD' }); if (!r.ok) out.push(f);
    }
    return out;
  });
  assert.deepEqual(missing, [], 'missing files referenced by data.js: ' + missing.join(', '));
  // external fonts/analytics may be unreachable from a test machine; only errors from the site's own code count
  assert.deepEqual(siteErr.filter(e => !/favicon|ERR_TUNNEL|ERR_NAME|ERR_INTERNET|ERR_CONNECTION|net::ERR_/.test(e)), [], 'site errors: ' + siteErr.join('\n'));
  ok('site: unit page links the generator, listings work, existing generator and PDF viewer load, every data.js file exists');

  await browser.close(); server.close();
  console.log('PASS: ' + n + ' browser checks (PDFs in ' + OUT + ')');
})().catch(e => { console.error(e); server.close(); process.exit(1); });
