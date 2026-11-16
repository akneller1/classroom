// Course and unit pages carry breadcrumbs and a LearningResource that names skills and standards.
const test = require('node:test'), assert = require('node:assert/strict');
const parse = (html) => JSON.parse(html.match(/<script type="application\/ld\+json">([\s\S]*?)<\/script>/)[1]);
test('JSON-LD for course and unit pages', async () => {
  const { courseJsonLd, unitJsonLd, unitStandards } = await import('../scripts/structured-data.mjs');
  const c = parse(courseJsonLd({ siteUrl: 'https://mrksclassroom.com/', courseName: 'Algebra 1', courseUrl: 'https://mrksclassroom.com/u/algebra/', description: 'd' }));
  assert.deepEqual(c['@graph'].map((x) => x['@type']), ['BreadcrumbList', 'Course']);
  const std = unitStandards(process.cwd(), 'math6', 'geometry');
  assert(std.length > 0 && std.every((s) => /^6\.|^5\./.test(s)), 'Grade 6 geometry standards come from its bank');
  const u = parse(unitJsonLd({ siteUrl: 'https://mrksclassroom.com/', courseName: '6th Grade Math', courseUrl: 'https://mrksclassroom.com/u/math6/', unitName: 'Geometry', unitUrl: 'https://mrksclassroom.com/u/math6/geometry/', description: 'd', skills: ['Area of Right Triangles'], standards: std, resourceCount: 12 }));
  const [crumbs, res] = u['@graph'];
  assert.equal(crumbs.itemListElement.length, 3);
  assert.equal(res['@type'], 'LearningResource');
  assert.deepEqual(res.teaches, ['Area of Right Triangles']);
  assert.equal(res.educationalAlignment[0].educationalFramework, 'Common Core State Standards for Mathematics');
  assert.doesNotMatch(unitJsonLd({ siteUrl: '', courseName: '</script>', courseUrl: '', unitName: 'x', unitUrl: '', description: '' }), /<\/script>.*<\/script>/s);
});
test('activity pages get Open Graph link previews', async () => {
  const { applyMeta } = await import('../scripts/activity-page-meta.mjs');
  const out = applyMeta('<html><head><meta charset="utf-8"><title>Exponents Connect Four</title></head></html>', { url: 'https://mrksclassroom.com/artifacts/x/index.html', item: { title: 'Exponents Connect Four', description: 'Two teams.' }, courseName: 'Algebra 1', unitName: 'Exponents', image: 'https://mrksclassroom.com/thumbs/x.jpg' });
  assert.match(out, /<meta property="og:title" content="Exponents Connect Four · Algebra 1">/);
  assert.match(out, /<meta property="og:image" content="https:\/\/mrksclassroom\.com\/thumbs\/x\.jpg">/);
  assert.match(out, /<meta name="twitter:card" content="summary_large_image">/);
});
