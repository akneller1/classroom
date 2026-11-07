// Card thumbnails: screenshots of each tool's visualization (thumbs/<slug>.jpg, 720 × 450).
// Usage (repository root): node tools/interactive-math-20261107/make_thumbs.cjs   (needs python3 with Pillow)
const { chromium } = require('playwright'); const { execFileSync } = require('child_process');
const http = require('http'), fs = require('fs'), path = require('path');
const ROOT = path.resolve(__dirname, '../..'); const M = require('./manifest.json');
const T = { '.html': 'text/html', '.js': 'text/javascript', '.css': 'text/css' };
const PRE = {   // a few clicks so the thumbnail shows the idea, not just the opening state
  'math6-area-shear-lab': p => p.evaluate(() => { const e = document.getElementById('sl-lean'); e.value = 3; e.dispatchEvent(new Event('input')); [...document.querySelectorAll('button')].find(b => b.textContent.includes('cut & slide')).click(); }),
  'math6-balance-point-dot-plot': p => p.evaluate(() => [...document.querySelectorAll('button')].find(b => b.textContent.includes('distances')).click()),
  'prealgebra7-percent-change-bar': p => p.evaluate(() => { [...document.querySelectorAll('button.chip')].find(b => b.textContent === 'Then decrease').click(); }),
  'prealgebra7-spinner-probability-lab': p => p.evaluate(() => [...document.querySelectorAll('button')].find(b => b.textContent === 'Spin 100').click()),
  'prealgebra-square-roots-number-line': p => p.evaluate(() => { const b = [...document.querySelectorAll('button')].find(b => b.textContent.includes('Zoom in')); b.click(); b.click(); }),
  'calculus-riemann-sum-lab': p => p.evaluate(() => { [...document.querySelectorAll('button.chip')].find(b => b.textContent === 'sin x').click(); const a = document.getElementById('sl-lower-limit-a'); a.value = -3; a.dispatchEvent(new Event('input')); const n = document.getElementById('sl-subintervals-n'); n.value = 12; n.dispatchEvent(new Event('input')); [...document.querySelectorAll('button.chip')].find(b => b.textContent === 'Midpoint').click(); }),
  'calculus-secant-to-tangent': p => p.evaluate(() => { [...document.querySelectorAll('button')].find(b => b.textContent.includes('tangent line')).click(); }),
  'calculus-accumulation-ftc': p => p.evaluate(() => { const e = document.getElementById('sl-upper-x'); e.value = 3.4; e.dispatchEvent(new Event('input')); })
};
const SHOT = { 'calculus-secant-to-tangent': 'svg[aria-label^="Graph of f"]', 'calculus-accumulation-ftc': 'svg[aria-label^="Rate"]', 'prealgebra7-spinner-probability-lab': 'svg[aria-label="Spinner and results"]', 'math6-ratio-double-number-line': 'svg[aria-label="Double number line"]', 'prealgebra-square-roots-number-line': 'svg[aria-label^="Square and"]', 'prealgebra7-percent-change-bar': 'svg[aria-label="Percent bar model"]', 'math6-fraction-division-groups': 'svg[aria-label^="Bar model"]', 'math6-balance-point-dot-plot': 'svg[aria-label="Dot plot"]' };
(async () => {
  const srv = await new Promise(r => { const s = http.createServer((q, res) => { const u = decodeURIComponent(q.url.split('?')[0]); fs.readFile(path.join(ROOT, u), (e, d) => { if (e) { res.writeHead(404); res.end(); return; } res.writeHead(200, { 'Content-Type': T[path.extname(u)] || 'application/octet-stream' }); res.end(d); }); }); s.listen(0, () => r(s)); });
  const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 1280, height: 1000 }, deviceScaleFactor: 2 });
  for (const t of M.tools) {
    await p.goto(`http://localhost:${srv.address().port}/artifacts/${t.slug}/index.html`); await p.waitForTimeout(150);
    if (PRE[t.slug]) { await PRE[t.slug](p); await p.waitForTimeout(250); }
    const el = await p.$(SHOT[t.slug] || '.stage svg');
    const tmp = `/tmp/thumb-${t.slug}.png`; await el.screenshot({ path: tmp });
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
