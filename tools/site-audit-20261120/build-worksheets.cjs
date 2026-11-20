/* Builds the Explore & Reflect worksheet and teacher key (PDF) for each motion lab. Run: node tools/site-audit-20261120/build-worksheets.cjs */
const fs = require('fs'), path = require('path'), { chromium } = require('playwright');
const root = path.join(__dirname, '../..'), labs = JSON.parse(fs.readFileSync(path.join(__dirname, 'labs.json'), 'utf8'));
const esc = (s) => s.replace(/&/g, '&amp;').replace(/</g, '&lt;');
function page(lab, key) {
  return `<!doctype html><html><head><meta charset="utf-8"><style>
  @page{size:Letter;margin:0.6in} body{font-family:Arial,Helvetica,sans-serif;font-size:12pt;color:#14173a;line-height:1.4}
  .eyebrow{font-size:9pt;letter-spacing:.12em;text-transform:uppercase;color:#3547f5;font-weight:700} h1{font-size:19pt;margin:2px 0 6px}
  .meta{display:flex;gap:24px;margin:6px 0 14px;font-size:11pt} .meta span{flex:1;border-bottom:1px solid #9aa0c8;padding-bottom:2px}
  ol{padding-left:22px} li{margin:0 0 ${key ? 12 : 18}px} .lines{height:64px;border-bottom:1px solid #cfd3ea;background:repeating-linear-gradient(transparent 0 30px,#cfd3ea 30px 31px)}
  .ans{margin-top:5px;padding:6px 9px;background:#e2e6ff;border-radius:6px} .foot{margin-top:18px;font-size:9pt;color:#4a4f78}
  </style></head><body><div class="eyebrow">${esc(lab.course)} · Interactive Math</div><h1>${esc(lab.title)}${key ? ' — Teacher Key' : ''}</h1>
  ${key ? '' : '<div class="meta"><span>Name</span><span>Date</span><span>Period</span></div>'}
  <p>${key ? 'Sample answers. Accept equivalent reasoning in students’ own words.' : 'Open the animation. Play it, pause it and drag the slider to look closely. Record what you see, then explain the math in your own words.'}</p>
  <ol>${lab.q.map(([q, a]) => `<li>${esc(q)}${key ? `<div class="ans">${esc(a)}</div>` : '<div class="lines"></div>'}</li>`).join('')}</ol>
  ${key ? '' : '<p><b>Reflect:</b> In one or two sentences, explain what the animation shows and why it is true.</p><div class="lines"></div>'}
  <p class="foot">Mr. K's Classroom · mrksclassroom.com</p></body></html>`;
}
(async () => {
  const b = await chromium.launch(), p = await b.newPage();
  for (const lab of labs) for (const key of [false, true]) {
    await p.setContent(page(lab, key));
    await p.pdf({ path: path.join(root, 'artifacts', lab.slug, key ? 'teacher-key.pdf' : 'worksheet.pdf'), format: 'Letter', printBackground: true });
  }
  await b.close(); console.log('worksheets built for', labs.length, 'labs');
})();
