// Generator pages must fit a 360px phone: the parts table scrolls in its own box.
const test = require('node:test'), assert = require('node:assert/strict'), fs = require('node:fs');
test('generator CSS keeps wide tables and grids inside the phone viewport', () => {
  const css = fs.readFileSync('worksheet-generator/menu/menu.css', 'utf8');
  assert.match(css, /\.mm-tablewrap\{overflow-x:auto;position:relative\}/);
  assert.match(css, /@media \(max-width:640px\)\{[\s\S]*\.topbar\{flex-wrap:wrap/);
  assert.match(css, /\.pr-app>\*,#prControls\{min-width:0/);
  for (const f of ['worksheet', 'menu-assessment', 'printables'])
    assert.match(fs.readFileSync('worksheet-generator/' + f + '.html', 'utf8'), /menu\/menu\.css\?v=mobile-fit-20261116/, f);
});
