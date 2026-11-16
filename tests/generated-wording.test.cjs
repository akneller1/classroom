// Generated prompts read naturally: no "project leader for an investigation" framing,
// and no equation boilerplate on one-step circle measurements.
const test = require('node:test'), assert = require('node:assert/strict'), fs = require('node:fs');
test('open-response framing and circle measurement prompts', () => {
  const ctx = fs.readFileSync('worksheet-generator/menu/mcas-context-bank.js', 'utf8');
  assert.doesNotMatch(ctx, /Present your findings to/);
  assert.match(ctx, /Answer all four parts\. '\+frame\.trim\(\)/);
  const circles = fs.readFileSync('worksheet-generator/menu/skills/geometry-circles.js', 'utf8');
  assert.match(circles, /\/\^geo-circle-\(diameter\|radius\)-\/\.test\(id\)\?'':' Set up and solve an equation for x\.'/);
  assert.match(circles, /Find its diameter x, in centimeters\./);
});
