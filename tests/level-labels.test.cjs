// One public level vocabulary: Support / Standard / Advanced (CP codes only as a teacher hint).
const test = require('node:test'), assert = require('node:assert/strict'), fs = require('node:fs');
test('runtime and static labels use Support, Standard, Advanced', () => {
  const ll = fs.readFileSync('level-labels.js', 'utf8');
  assert.match(ll, /labels=\{cp2:'Support',cp1:'Standard',honors:'Advanced'\}/);
  for (const f of ['worksheet-generator/plot-practice.html', 'guide.html', 'unit-specific-arcade.js', 'student-share-cards.js', 'financial/games/vendor/games.js'])
    assert.doesNotMatch(fs.readFileSync(f, 'utf8'), /Level 1 · Warm-Up|Remedial|'On Level'/, f);
  assert.match(fs.readFileSync('worksheet-generator/menu/engine.js', 'utf8'), /long: 'Support \(CP2\)'/);
});
test('level-labels never rewrites an option that already shows its label (no MutationObserver loop)', () => {
  const ll = require('node:fs').readFileSync('level-labels.js', 'utf8');
  assert.match(ll, /if\(o\.textContent===text\)return;/);
  // The build rewrites the word "Remedial" site-wide, so it must not appear in matching patterns here.
  assert.doesNotMatch(ll, /Remedial/);
});
