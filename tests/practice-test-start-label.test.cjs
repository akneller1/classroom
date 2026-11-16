// The Practice Test primary button starts the interactive test; it must say so.
const test = require('node:test'), assert = require('node:assert/strict'), fs = require('node:fs');
test('Practice Test start button is labelled for what it does', () => {
  const s = fs.readFileSync('worksheet-generator/practice/practice.js', 'utf8');
  assert.match(s, /<button id="pt-build">Start practice test<\/button>/);
  assert.doesNotMatch(s, /Generate printable assessment/);
  assert.match(s, /Print \/ Save Test as PDF/, 'printing stays available inside the test');
});
