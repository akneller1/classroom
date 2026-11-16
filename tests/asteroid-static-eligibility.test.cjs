// Static /u/ pages must not link Asteroid Blaster for units the app hides.
const test = require('node:test'), assert = require('node:assert/strict');

test('static pages only keep Asteroid cards for curated units', async () => {
  const { asteroidEligibleUnits, filterAsteroidItems } = await import('../scripts/asteroid-eligibility.mjs');
  const eligible = asteroidEligibleUnits(process.cwd());
  assert(eligible.has('algebra/linear-equations-slope'));
  assert(eligible.has('grade2/place-value-1000'));
  assert(!eligible.has('calculus/derivatives'));
  const card = { title: 'Asteroid Blaster', path: 'worksheet-generator/asteroid-blaster.html?course=calculus&unit=derivatives' };
  const other = { title: 'Millionaire', path: 'worksheet-generator/millionaire.html?course=calculus&unit=derivatives' };
  assert.deepEqual(filterAsteroidItems('calculus', 'derivatives', [card, other], eligible), [other]);
  const kept = { title: 'Asteroid Blaster', bankFormat: 'asteroid-blaster', path: 'worksheet-generator/asteroid-blaster.html?course=algebra&unit=linear-equations-slope' };
  assert.equal(filterAsteroidItems('algebra', 'linear-equations-slope', [kept], eligible).length, 1);
});

test('Asteroid Blaster reports an unsupported requested unit instead of switching', () => {
  const html = require('node:fs').readFileSync('worksheet-generator/asteroid-blaster.html', 'utf8');
  assert.match(html, /Asteroid Blaster is not available for '\+/);
  assert.match(html, /if\(rc&&ru\)\{/);
  assert.match(html, /S\.courseId!==q\.get\('course'\)\|\|S\.unit\.id!==q\.get\('unit'\)/);
});
