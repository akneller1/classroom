// Generator copy must match what each generator actually offers.
const test = require('node:test'), assert = require('node:assert/strict'), fs = require('node:fs');
const read = f => fs.readFileSync(f, 'utf8');
test('generator descriptions and course lists are consistent', () => {
  assert.doesNotMatch(read('worksheet-generator/lesson-planner.html'), /180 Algebra 1 or Geometry days/);
  assert.match(read('worksheet-generator/menu/app.js'), /multiUnitSupported\(c\.unitId\) \? 'choose all that apply, ' : ''/);
  const vocab = read('worksheet-generator/vocabulary.html');
  assert(vocab.indexOf('menu/course-order.js') > -1 && vocab.indexOf('menu/course-order.js') < vocab.indexOf('vocabulary-builder.js'), 'Vocabulary Builder sorts courses with the shared order');
  assert.match(vocab, /Financial Algebra vocabulary is on each Financial Algebra unit page/);
  assert.match(read('worksheet-generator/menu/printables-ui.js'), /Financial Algebra printables/);
  assert.doesNotMatch(read('data.js'), /'Build graphs, picture graphs and line plots;/);
  assert.match(read('worksheet-generator/vocabulary-builder.js'), /k===1\?' unit · ':' units · '/);
});
