// Grade 6 audit #14: prints the Grade 6 practice tests (exam.pdf, teacher-key.pdf) and the reference
// sheet (reference-sheet.pdf), and makes the card thumbnails from the first page. Usage (repository root):
//   python3 tools/grade6-audit-20261119/g6_print.py && node tools/grade6-audit-20261119/print_g6.cjs
const { chromium } = require('playwright'); const { execFileSync } = require('child_process');
const path = require('path');
const ROOT = path.resolve(__dirname, '../..');
const JOBS = [['grade6-practice-test-a', [['exam.html', 'exam.pdf'], ['key.html', 'teacher-key.pdf']]], ['grade6-practice-test-b', [['exam.html', 'exam.pdf'], ['key.html', 'teacher-key.pdf']]],
  ['grade6-reference-sheet', [['index.html', 'reference-sheet.pdf']]]];
(async () => {
  const b = await chromium.launch(); const p = await b.newPage();
  for (const [slug, files] of JOBS) {
    const dir = path.join(ROOT, 'artifacts', slug);
    for (const [src, out] of files) {
      await p.goto('file://' + path.join(dir, src)); await p.waitForTimeout(300);
      const buf = await p.pdf({ path: path.join(dir, out), format: 'Letter', printBackground: true, preferCSSPageSize: true });
      console.log(slug, out, (buf.toString('latin1').match(/\/Type\s*\/Page[^s]/g) || []).length, 'pages');
    }
    await p.setViewportSize({ width: 816, height: 1056 }); await p.goto('file://' + path.join(dir, files[0][0])); await p.waitForTimeout(300);
    const tmp = path.join(require('os').tmpdir(), 'thumb-' + slug + '.png'); await p.screenshot({ path: tmp, clip: { x: 0, y: 0, width: 816, height: 510 } });
    execFileSync('python3', ['-c', `from PIL import Image\nIm=Image.open('${tmp}').convert('RGB').resize((720,450),Image.LANCZOS)\nIm.save('${path.join(ROOT, 'thumbs', slug + '.jpg')}',quality=86)`]);
  }
  await b.close();
})();
