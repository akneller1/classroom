'use strict';
// Browser regression for the reported tiny Tarsia labels and clipped Whodunnit D rows.
const assert = require('node:assert/strict');
const fs = require('node:fs'), path = require('node:path'), http = require('node:http');
const { chromium } = require('playwright');
const root = path.resolve(process.env.SITE_ROOT || path.join(__dirname, '..'));
const types = { '.html': 'text/html', '.js': 'text/javascript', '.css': 'text/css', '.svg': 'image/svg+xml', '.woff2': 'font/woff2', '.woff': 'font/woff', '.ttf': 'font/ttf', '.png': 'image/png' };
const server = http.createServer((req, res) => {
  const file = path.resolve(root, '.' + decodeURIComponent(req.url.split('?')[0]));
  if (!file.startsWith(root + path.sep) || !fs.existsSync(file) || fs.statSync(file).isDirectory()) { res.writeHead(404); return res.end(); }
  res.writeHead(200, { 'content-type': types[path.extname(file)] || 'application/octet-stream' });
  fs.createReadStream(file).pipe(res);
});
let browser;
(async () => {
  await new Promise(resolve => server.listen(0, '127.0.0.1', resolve));
  browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1360, height: 1000 } });
  await page.goto(`http://127.0.0.1:${server.address().port}/worksheet-generator/printables.html#unit=algebra1-expressions-equations&kind=tarsia`);
  await page.waitForSelector('.pr-tsvg', { timeout: 120000 });
  await page.evaluate(() => document.fonts.ready);
  for (const media of ['screen', 'print']) {
    await page.emulateMedia({ media });
    const result = await page.evaluate(() => {
      const PR = MKMENU.printables, failures = [];
      const units = ['algebra1-expressions-equations', 'algebra1-polynomials', 'algebra1-systems-of-equations'];
      // Include authored courses when running against the assembled public site.
      for (const prefix of ['grade1-', 'grade2-', 'grade3-', 'grade4-', 'grade5-', 'algebra2-', 'geometry-']) {
        const id = Object.keys(MKMENU.skillSets).find(id => id.startsWith(prefix));
        if (id) units.push(id);
      }
      const host = document.createElement('div'); host.style.cssText = 'position:absolute;left:-10000px;top:0'; document.body.append(host);
      const render = (cfg, B, key) => {
        host.replaceChildren(...PR.pageEls(cfg, B, 0, 1, key));
        PR.fitTarsiaLabels(host);
        return [...host.querySelectorAll('.pr-page')];
      };
      let puzzles = 0, cards = 0, references = 0;
      for (const unit of units) for (const level of ['cp2', 'cp1', 'honors']) {
        const cfg = PR.defaultConfig(unit, 'tarsia'); cfg.level = level; cfg.seed = 77;
        const B = PR.build(cfg, 0);
        if (!B.error) for (const layout of ['standard', 'large', 'compact']) for (const key of [false, true]) {
          cfg.tarsiaLayout = layout;
          render(cfg, B, key);
          const labels = [...host.querySelectorAll('.pr-tsvg foreignObject')];
          for (const fo of labels) {
            const scale = +fo.getAttribute('data-fit-scale');
            const pt = parseFloat(getComputedStyle(fo.querySelector('.pr-tt')).fontSize) * .75 * scale;
            if (pt < 6.5) failures.push(`${unit}/${level}/${layout}: tiny label ${fo.textContent} (${pt.toFixed(1)}pt)`);
            if (/^Problem \d+$/.test(fo.textContent)) references++;
          }
          puzzles++;
        }
        cfg.kind = 'who';
        const W = PR.build(cfg, 0);
        if (W.error) continue;
        // Stress a genuine card with a long word problem, plus its four real choices.
        const card = W.cards[0];
        card.item.p = { ...card.item.p, fig: null, authoredOptions: null, parts: [{ prompt: '' }],
          prompt: ('A school club compares two plans for a field trip. The first plan charges a fixed fee and a cost per student. ').repeat(7) + ' ' + card.item.p.prompt };
        const pages = render(cfg, W, false);
        for (const el of host.querySelectorAll('.pw-card')) {
          const body = el.closest('.mm-body').getBoundingClientRect();
          const rows = [...el.querySelectorAll('.pw-opts tr')];
          if (rows.length !== 4 || !/^D\./.test(rows[3].textContent)) failures.push(`${unit}: missing choice D`);
          for (const node of [...rows, el.querySelector('.pw-cf')]) {
            const rect = node.getBoundingClientRect();
            if (rect.bottom > body.bottom + 1 || rect.left < body.left - 1 || rect.right > body.right + 1) failures.push(`${unit}/${level}: clipped answer row or footer`);
          }
          cards++;
        }
        if (pages.filter(p => p.querySelector('.pw-card')).length < 5) failures.push(`${unit}: cards not paginated`);
        if (host.querySelector('.pw-card').parentElement.querySelectorAll('.pw-card').length !== 1) failures.push(`${unit}: long card should get its own page`);
      }
      host.remove();
      return { failures, puzzles, cards, references };
    });
    console.log(media, JSON.stringify(result));
    assert.deepEqual(result.failures, []);
    assert.ok(result.puzzles >= 36 && result.cards >= 30 && result.references > 0);
  }
  console.log('Printable layout regressions passed in screen and print media.');
})().catch(error => { console.error(error); process.exitCode = 1; }).finally(async () => {
  if (browser) await browser.close();
  server.close();
});
