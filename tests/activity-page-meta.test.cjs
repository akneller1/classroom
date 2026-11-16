// Activity pages get a descriptive title, a description and a canonical; projects are indexable in every grade.
const test = require('node:test'), assert = require('node:assert/strict');
test('activity page metadata', async () => {
  const { applyMeta, pageTitle, isSlugTitle } = await import('../scripts/activity-page-meta.mjs');
  assert(isSlugTitle('G6 Fdp Oddout')); assert(!isSlugTitle('Exponents Connect Four'));
  assert.equal(pageTitle('G6 Fdp Oddout', { title: 'Fraction · Decimal · Percent Odd One Out' }, '6th Grade Math'),
    "Fraction · Decimal · Percent Odd One Out · 6th Grade Math | Mr. K's Classroom");
  assert.equal(pageTitle("Riemann Sum Lab · Mr. K's Classroom", { title: 'x' }, 'Calculus'), "Riemann Sum Lab · Mr. K's Classroom");
  const html = '<!doctype html><html><head><meta charset="utf-8"><meta name="robots" content="noindex"><title>Farm Story Problems · 1st Grade Math Project</title></head><body></body></html>';
  const out = applyMeta(html, { url: 'https://mrksclassroom.com/artifacts/math1-project-farm-stories/index.html', item: { title: 'Farm Stories', description: 'Students write farm story problems.' }, courseName: '1st Grade Math', unitName: 'Word Problems' });
  assert.match(out, /<title>Farm Story Problems · 1st Grade Math Project \| Mr\. K&#39;s Classroom<\/title>/);
  assert.match(out, /<meta charset="utf-8"><meta name="description" content="Students write farm story problems\.">/);
  assert.match(out, /<link rel="canonical" href="https:\/\/mrksclassroom\.com\/artifacts\/math1-project-farm-stories\/index\.html">/);
  assert.doesNotMatch(out, /noindex/);
  assert.equal(applyMeta(out, { url: 'https://mrksclassroom.com/artifacts/math1-project-farm-stories/index.html', item: { title: 'Farm Stories' }, courseName: '1st Grade Math', unitName: 'Word Problems' }), out, 'idempotent');
  const legacy = applyMeta('<html><head><meta name="robots" content="noindex"><title>Old</title></head></html>', { url: 'https://mrksclassroom.com/artifacts/old-flashcards/index.html', item: { title: 'Old' }, courseName: 'Algebra 1', unitName: 'U' });
  assert.match(legacy, /noindex/, 'legacy duplicates keep noindex');
});
test('game wrappers set a descriptive title', () => {
  const fs = require('node:fs');
  assert.match(fs.readFileSync('worksheet-generator/games/course-source.js', 'utf8'), /\/\^Classroom Activities\\b\/\.test\(G\.document\.title\)/);
  assert.match(fs.readFileSync('worksheet-generator/games/course-activity.js', 'utf8'), /source\.course\.name:''\)\+" \| Mr\. K's Classroom"/);
});
