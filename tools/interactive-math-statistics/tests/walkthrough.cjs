// Automated walkthrough of the 2026-11-07 Interactive Math tools: opens each tool through the normal page,
// drives the real controls (sliders, chips, buttons, number boxes, keyboard on draggable points), and checks that
// every "Try this" challenge turns green, that no challenge is already done at the start, and that there are no errors.
// Usage (repository root): node tools/interactive-math-statistics/tests/walkthrough.cjs [slug]
const { chromium } = require('playwright');
const http = require('http'), fs = require('fs'), path = require('path');
const ROOT = path.resolve(__dirname, '../../..');
const T = { '.html': 'text/html', '.js': 'text/javascript', '.css': 'text/css', '.json': 'application/json', '.svg': 'image/svg+xml', '.jpg': 'image/jpeg', '.png': 'image/png', '.pdf': 'application/pdf' };
const serve = () => new Promise(r => { const s = http.createServer((q, res) => { let u = decodeURIComponent(q.url.split('?')[0].split('#')[0]); if (u.endsWith('/')) u += 'index.html'; fs.readFile(path.join(ROOT, u), (e, d) => { if (e) { res.writeHead(404); res.end(); return; } res.writeHead(200, { 'Content-Type': T[path.extname(u)] || 'application/octet-stream' }); res.end(d); }); }); s.listen(0, () => r(s)); });
const pause = p => p.waitForTimeout(40);
const H = {
  slider: async (p, id, v) => { await p.evaluate(([id, v]) => { const e = document.getElementById('sl-' + id); e.value = v; e.dispatchEvent(new Event('input')); }, [id, v]); await pause(p); },
  num: async (p, id, v) => { await p.evaluate(([id, v]) => { const e = document.getElementById('ni-' + id); e.value = v; e.dispatchEvent(new Event('change')); }, [id, v]); await pause(p); },
  btn: async (p, text) => { await p.evaluate(t => { const b = [...document.querySelectorAll('button')].find(b => b.textContent.trim() === t || b.textContent.trim().startsWith(t)); if (!b) throw new Error('no button ' + t); b.click(); }, text); await pause(p); },
  chip: async (p, text) => { await p.evaluate(t => { const b = [...document.querySelectorAll('button.chip')].find(b => b.textContent.trim() === t); if (!b) throw new Error('no chip ' + t); b.click(); }, text); await pause(p); },
  tab: async (p, text) => { await p.evaluate(t => { const b = [...document.querySelectorAll('button.tab')].find(b => b.textContent.trim() === t); if (!b) throw new Error('no tab ' + t); b.click(); }, text); await pause(p); },
  keys: async (p, label, key, n = 1) => { for (let i = 0; i < n; i++) { await p.evaluate(l => { const e = [...document.querySelectorAll('[aria-label]')].find(x => x.getAttribute('aria-label') === l && x.getAttribute('tabindex') !== null); if (!e) throw new Error('no handle ' + l); e.focus(); }, label); await p.keyboard.press(key); await p.waitForTimeout(25); } },
  done: p => p.evaluate(() => [...document.querySelectorAll('.challenges li')].map(li => li.classList.contains('done'))),
  wait: p => p.waitForTimeout(60)
};
const S = require('./scripts.cjs');
(async () => {
  const srv = await serve(), port = srv.address().port, b = await chromium.launch();
  let fails = 0, total = 0;
  for (const slug of Object.keys(S)) {
    if (process.argv[2] && slug !== process.argv[2]) continue;
    const p = await b.newPage({ viewport: { width: 1280, height: 900 } }); const errs = [];
    p.on('pageerror', e => errs.push(e.message)); p.on('console', m => { if (m.type() === 'error' && !/ERR_|Failed to load resource/.test(m.text())) errs.push(m.text()); });
    await p.goto(`http://localhost:${port}/artifacts/${slug}/index.html?seed=${process.env.SEED || 20261108}`); await H.wait(p);
    const start = await H.done(p);
    const steps = S[slug];
    const res = [];
    for (let i = 0; i < steps.length; i++) {
      try { await steps[i](p, H); await H.wait(p); } catch (e) { errs.push('step ' + (i + 1) + ': ' + e.message); }
      const d = await H.done(p); res.push(d[i]);
    }
    const n = (await H.done(p)).length;
    const ok = res.every(Boolean) && !start.some(Boolean) && !errs.length && n === steps.length;
    total++; if (!ok) fails++;
    console.log((ok ? 'PASS ' : 'FAIL ') + slug + `  challenges ${res.filter(Boolean).length}/${n}` + (start.some(Boolean) ? '  (some done at start!)' : '') + (errs.length ? '  errors: ' + errs.join(' | ') : ''));
    if (!ok) console.log('   per-step:', res.map((x, i) => (i + 1) + (x ? '✓' : '✗')).join(' '));
    await p.close();
  }
  await b.close(); srv.close();
  console.log(`${total - fails}/${total} tools passed`); process.exit(fails ? 1 : 0);
})();
