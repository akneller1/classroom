/* Geometry regression: every skill verifies at every tier, and repeated cards stay available. */
'use strict';
const assert = require('node:assert/strict');
const menu = require('./load.cjs')().MKMENU;
const units = Object.keys(menu.skillSets).filter(id => id.startsWith('geometry-'));
assert.equal(units.length, 10, 'Expected all ten Geometry units');
let checks = 0;
for (const unit of units) {
  for (const skill of menu.skillSets[unit].skills) {
    for (let c = 1; c <= 7; c++) {
      const used = {keys: new Set(), sigs: new Set()};
      const count = [1,3,5,7].includes(c) ? 12 : 1;
      for (let n = 0; n < count; n++) {
        const p = menu.generateProblem(unit, skill.id, c,
          {intOnly: true, level: 'game'},
          ['geometry-regression', unit, skill.id, c, n].join(':'), used);
        assert.ok(!p.failed, [unit, skill.id, 'tier '+c, 'card '+n, p.reason].join(' / '));
        assert.equal(p.verify.status, 'verified', unit + '/' + skill.id);
        checks++;
      }
    }
  }
}
console.log('Geometry generator regression passed: '+checks+' verified cards across '+units.length+' units.');
