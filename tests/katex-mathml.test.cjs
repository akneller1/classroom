// Screen readers need KaTeX's MathML; html-only output hides every equation.
const test = require('node:test'), assert = require('node:assert/strict'), fs = require('node:fs');
const files = ['worksheet-generator/core/math-display.js', 'worksheet-generator/core/render.js',
  'worksheet-generator/practice/practice.js', 'worksheet-generator/practice/math-preview.js', 'artifacts/math-arcade/index.html'];
test('shared math renderers emit MathML for assistive technology', () => {
  for (const f of files) {
    const s = fs.readFileSync(f, 'utf8');
    assert.doesNotMatch(s, /output\s*:\s*'html'/, f + ' renders html-only KaTeX');
    assert.match(s, /htmlAndMathml/, f);
  }
});
test('MathML stays visually hidden when katex.min.css is missing', () => {
  for (const f of files.slice(0, 4)) assert.match(fs.readFileSync(f, 'utf8'), /mk-katex-mathml/, f);
});
