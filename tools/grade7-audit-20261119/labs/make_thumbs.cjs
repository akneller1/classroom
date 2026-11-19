// Card thumbnails: screenshots of each tool's visualization (thumbs/<slug>.jpg, 720 × 450).
// Grade 7 audit labs (#15). Usage (repository root): node tools/grade7-audit-20261119/labs/make_thumbs.cjs   (needs python3 with Pillow)
const { chromium } = require('playwright'); const { execFileSync } = require('child_process');
const http = require('http'), fs = require('fs'), path = require('path');
const ROOT = path.resolve(__dirname, '../../..'); const M = require('./manifest.json');
const T = { '.html': 'text/html', '.js': 'text/javascript', '.css': 'text/css' };
const PRE = {
  'grade7-integer-chips-lab': p => p.evaluate(() => { const e = document.getElementById('sl-a'); e.value = 6; e.dispatchEvent(new Event('input')); const f = document.getElementById('sl-b'); f.value = -9; f.dispatchEvent(new Event('input')); }),
  'grade7-circles-lab': p => p.evaluate(() => { [...document.querySelectorAll('button')].find(b => b.textContent.trim() === '16').click(); [...document.querySelectorAll('button')].find(b => b.textContent.trim().startsWith('Area')).click(); })
};
const SHOT = { 'grade7-integer-chips-lab': 'svg[aria-label="Integer chips"]', 'grade7-circles-lab': 'svg[aria-label="Circle model"]' };
(async () => {
  const srv = await new Promise(r => { const s = http.createServer((q, res) => { const u = decodeURIComponent(q.url.split('?')[0]); fs.readFile(path.join(ROOT, u), (e, d) => { if (e) { res.writeHead(404); res.end(); return; } res.writeHead(200, { 'Content-Type': T[path.extname(u)] || 'application/octet-stream' }); res.end(d); }); }); s.listen(0, () => r(s)); });
  const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 1280, height: 1000 }, deviceScaleFactor: 2 });
  for (const t of M.tools) {
    await p.route(/fonts\.(googleapis|gstatic)/, r => r.abort()); await p.goto(`http://localhost:${srv.address().port}/artifacts/${t.slug}/index.html`); await p.waitForTimeout(150);
    if (PRE[t.slug]) { await PRE[t.slug](p); await p.waitForTimeout(250); }
    const el = await p.$(SHOT[t.slug] || '.stage svg');
    const tmp = `/tmp/thumb-${t.slug}.png`; await el.screenshot({ path: tmp });
    execFileSync('python3', ['-c', `
from PIL import Image
im = Image.open('${tmp}').convert('RGB'); W, H = 720, 450
s = min(W / im.width, H / im.height)  # contain: show the whole picture
im = im.resize((round(im.width * s), round(im.height * s)), Image.LANCZOS)
bg = Image.new('RGB', (W, H), (255, 255, 255)); bg.paste(im, ((W - im.width) // 2, max(0, (H - im.height) // 2) if im.height <= H else 0) if im.height <= H else ((W - im.width) // 2, -min(im.height - H, int(im.height * 0.08))))
bg.save('${path.join(ROOT, 'thumbs', t.slug + '.jpg')}', quality=86)`]);
    console.log('thumb', t.slug);
  }
  await b.close(); srv.close();
})();
