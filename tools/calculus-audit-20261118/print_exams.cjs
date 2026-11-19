// Calculus audit #17: prints artifacts/calculus-ap-practice-exam-{a,b}/exam.html and key.html to exam.pdf and teacher-key.pdf,
// and makes the card thumbnails from the first page. Usage (repository root):
//   python3 tools/calculus-audit-20261118/exams.py && node tools/calculus-audit-20261118/print_exams.cjs
const { chromium } = require('playwright'); const { execFileSync } = require('child_process');
const path = require('path'), fs = require('fs');
const ROOT = path.resolve(__dirname, '../..');
(async () => {
  const b = await chromium.launch(); const p = await b.newPage();
  for (const ex of ['a', 'b']) {
    const dir = path.join(ROOT, 'artifacts', 'calculus-ap-practice-exam-' + ex);
    for (const [src, out] of [['exam.html', 'exam.pdf'], ['key.html', 'teacher-key.pdf']]) {
      await p.goto('file://' + path.join(dir, src)); await p.waitForTimeout(300);
      const left = await p.evaluate(() => [...document.querySelectorAll('.q, .choices, .solution')].filter(e => /∫ from |lim \(|\d\/\d/.test(e.textContent) && !e.querySelector('.mk-math')).length);
      if (left) console.log('note:', left, 'blocks without stacked math in', ex, src);
      const buf = await p.pdf({ path: path.join(dir, out), format: 'Letter', printBackground: true, preferCSSPageSize: true });
      console.log(ex, out, (buf.toString('latin1').match(/\/Type\s*\/Page[^s]/g) || []).length, 'pages');
    }
    await p.setViewportSize({ width: 816, height: 1056 }); await p.goto('file://' + path.join(dir, 'exam.html')); await p.waitForTimeout(300);
    const tmp = path.join(require('os').tmpdir(), 'exam-thumb-' + ex + '.png'); await p.screenshot({ path: tmp, clip: { x: 0, y: 0, width: 816, height: 510 } });
    execFileSync('python3', ['-c', `from PIL import Image\nIm=Image.open('${tmp}').convert('RGB').resize((720,450),Image.LANCZOS)\nIm.save('${path.join(ROOT, 'thumbs', 'calculus-ap-practice-exam-' + ex + '.jpg')}',quality=86)`]);
  }
  await b.close();
})();
