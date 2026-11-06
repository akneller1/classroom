// Prints worksheet-html/*.html to artifacts/<slug>/worksheet.pdf and teacher-key.pdf, and reports page counts.
// Usage (repository root): node tools/interactive-math-20261105/print_pdfs.cjs [slug-prefix]
const { chromium } = require('playwright');
const fs = require('fs'), path = require('path');
const HERE = __dirname, ROOT = path.dirname(path.dirname(HERE));
const M = require(path.join(HERE, 'manifest.json'));
(async () => {
  const b = await chromium.launch(); const p = await b.newPage();
  const counts = {};
  const only = process.argv[2];  // optional: only tools whose slug starts with this
  for (const t of M.tools) {
    if (only && !t.slug.startsWith(only)) continue;
    for (const key of [false, true]) {
      const src = path.join(HERE, 'worksheet-html', t.slug + (key ? '-key' : '') + '.html');
      await p.goto('file://' + src); await p.evaluate(() => document.fonts.ready);
      const out = path.join(ROOT, 'artifacts', t.slug, key ? 'teacher-key.pdf' : 'worksheet.pdf');
      const buf = await p.pdf({ path: out, format: 'Letter', printBackground: true, preferCSSPageSize: true });
      const pages = (buf.toString('latin1').match(/\/Type\s*\/Page[^s]/g) || []).length;
      counts[t.slug + (key ? ':key' : '')] = pages;
    }
  }
  fs.writeFileSync(path.join(HERE, 'page-counts.json'), JSON.stringify(counts, null, 1));
  console.log(counts);
  await b.close();
})();
