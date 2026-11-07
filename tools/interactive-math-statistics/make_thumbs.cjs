// Card thumbnails: screenshots of each tool's visualization (thumbs/<slug>.jpg, 720 × 450).
// Usage (repository root): node tools/interactive-math-statistics/make_thumbs.cjs   (needs python3 with Pillow)
const { chromium } = require('playwright'); const { execFileSync } = require('child_process');
const http = require('http'), fs = require('fs'), path = require('path');
const ROOT = path.resolve(__dirname, '../..'); const M = require('./manifest.json');
const T = { '.html': 'text/html', '.js': 'text/javascript', '.css': 'text/css' };
const PRE = {   // a few clicks so the thumbnail shows the idea, not just the opening state
  'statistics-sampling-distribution-lab': p => p.evaluate(() => { const n = document.getElementById('sl-sample-size'); n.value = 25; n.dispatchEvent(new Event('input')); [...document.querySelectorAll('button')].find(b => b.textContent === 'Draw 1,000').click(); [...document.querySelectorAll('button')].find(b => b.textContent.startsWith('Overlay')).click(); }),
  'statistics-confidence-interval-lab': p => p.evaluate(() => [...document.querySelectorAll('button')].find(b => b.textContent === 'Make 100').click()),
  'statistics-significance-power-explorer': p => p.evaluate(() => [...document.querySelectorAll('button.tab')][1].click()),
  'statistics-sampling-methods-lab': p => p.evaluate(() => { const b = t => [...document.querySelectorAll('button')].find(x => x.textContent === t).click(); b('Take 100 samples'); b('Take 100 samples'); }),
  'statistics-regression-influence-lab': p => p.evaluate(() => [...document.querySelectorAll('button')].find(b => b.textContent.startsWith('Add an extra')).click()),
  'statistics-random-assignment-lab': p => p.evaluate(() => { [...document.querySelectorAll('button.chip')].find(b => b.textContent === 'Students choose').click(); const b = t => [...document.querySelectorAll('button')].find(x => x.textContent === t).click(); b('Repeat 100 times'); b('Repeat 100 times'); })
};
const SHOT = { 'statistics-sampling-distribution-lab': ['svg[aria-label="Population"]', 'svg[aria-label="Distribution of the sample statistic"]'], 'statistics-confidence-interval-lab': 'svg[aria-label^="Confidence intervals"]', 'statistics-significance-power-explorer': 'svg[aria-label^="Sampling distribution"]',
  'statistics-sampling-methods-lab': 'svg[aria-label^="Seating"]', 'statistics-conditional-probability-explorer': 'svg[aria-label^="Tree"]', 'statistics-regression-influence-lab': 'svg[aria-label^="Scatterplot"]',
  'statistics-random-assignment-lab': ['svg[aria-label^="The 20 volunteers"]', 'svg[aria-label^="Distribution of differences"]'] };
(async () => {
  const srv = await new Promise(r => { const s = http.createServer((q, res) => { const u = decodeURIComponent(q.url.split('?')[0]); fs.readFile(path.join(ROOT, u), (e, d) => { if (e) { res.writeHead(404); res.end(); return; } res.writeHead(200, { 'Content-Type': T[path.extname(u)] || 'application/octet-stream' }); res.end(d); }); }); s.listen(0, () => r(s)); });
  const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 1280, height: 1000 }, deviceScaleFactor: 2 });
  for (const t of M.tools) {
    await p.goto(`http://localhost:${srv.address().port}/artifacts/${t.slug}/index.html?seed=20261108`); await p.waitForTimeout(150);
    if (PRE[t.slug]) { await PRE[t.slug](p); await p.waitForTimeout(250); }
    const sel = [].concat(SHOT[t.slug] || '.stage svg'), tmp = `/tmp/thumb-${t.slug}.png`, parts = [];
    for (let i = 0; i < sel.length; i++) { const part = `/tmp/thumb-${t.slug}-${i}.png`; await (await p.$(sel[i])).screenshot({ path: part }); parts.push(part); }
    /* several elements (e.g. population over sampling distribution) are stacked into one picture */
    execFileSync('python3', ['-c', `
from PIL import Image
ims = [Image.open(f).convert('RGB') for f in ${JSON.stringify(parts)}]
w = max(i.width for i in ims); out = Image.new('RGB', (w, sum(i.height for i in ims)), (255, 255, 255)); y = 0
for i in ims: out.paste(i, (0, y)); y += i.height
out.save('${tmp}')`]);
    execFileSync('python3', ['-c', `
from PIL import Image
im = Image.open('${tmp}').convert('RGB'); W, H = 720, 450
s = max(W / im.width, H / im.height) if im.width / im.height < 1.2 else min(W / im.width, H / im.height)
im = im.resize((round(im.width * s), round(im.height * s)), Image.LANCZOS)
bg = Image.new('RGB', (W, H), (255, 255, 255)); bg.paste(im, ((W - im.width) // 2, max(0, (H - im.height) // 2) if im.height <= H else 0) if im.height <= H else ((W - im.width) // 2, -min(im.height - H, int(im.height * 0.08))))
bg.save('${path.join(ROOT, 'thumbs', t.slug + '.jpg')}', quality=86)`]);
    console.log('thumb', t.slug);
  }
  await b.close(); srv.close();
})();
