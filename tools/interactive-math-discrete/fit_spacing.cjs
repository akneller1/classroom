// Chooses, for each worksheet, the largest writing-space level (0–4) whose worksheet AND key still print on exactly 2 pages.
// Writes spacing.json, which build_worksheets.py reads. Usage (repository root): node tools/interactive-math-discrete/fit_spacing.cjs
const { chromium } = require('playwright'); const { execFileSync } = require('child_process');
const fs = require('fs'), path = require('path'); const HERE = __dirname; const M = require('./manifest.json');
(async () => {
  const b = await chromium.launch(); const p = await b.newPage(); const out = {};
  const pages = async f => { await p.goto('file://' + f); await p.evaluate(() => document.fonts.ready); const buf = await p.pdf({ format: 'Letter', printBackground: true, preferCSSPageSize: true }); return (buf.toString('latin1').match(/\/Type\s*\/Page[^s]/g) || []).length; };
  for (const t of M.tools) {
    let best = 0;
    for (const lv of [4, 3, 2, 1, 0]) {
      execFileSync('python3', [path.join(HERE, 'build_worksheets.py'), t.slug, String(lv)]);
      const a = await pages(path.join(HERE, 'worksheet-html', t.slug + '.html')), k = await pages(path.join(HERE, 'worksheet-html', t.slug + '-key.html'));
      if (a === 2 && k === 2) { best = lv; break; }
    }
    out[t.slug] = best; console.log(t.slug, best);
  }
  fs.writeFileSync(path.join(HERE, 'spacing.json'), JSON.stringify(out, null, 1)); await b.close();
})();
