/* Regression: one verified inequality choice model for worksheets, tests and games.
   Exercises CP2, CP1 and Honors, including shaded graphs and point membership. */
'use strict';
const assert = require('node:assert/strict');
const load = require('./load.cjs');
const env = load(['games/bank.js', 'menu/render.js']);
const M = env.MKMENU, GB = env.MKGAMES;
const UNIT = 'algebra1-systems-of-equations';
const levels = {
  cp2: [1, 2, 3],
  cp1: [3, 4, 5],
  honors: [5, 6, 7]
};
let generated = 0, graphs = 0, points = 0, fullTests = 0;
function validateChoice(p, model, label) {
  assert.ok(model && model.opts && Number.isInteger(model.key), label + ': choices exist');
  assert.ok(model.key >= 0 && model.key < model.opts.length, label + ': valid key');
  if (model.inequalityMode === 'graph') {
    graphs++;
    assert.equal(model.graphs.length, 4, label + ': four graphs');
    assert.equal(new Set(model.graphs.map(g => JSON.stringify(g.halfplanes))).size, 4, label + ': distinct graphs');
    assert.equal(JSON.stringify(model.graphs[model.key]), JSON.stringify(p.parts[0].answerFig), label + ': key graph matches verified figure');
    for (const g of model.graphs) assert.match(M.figHtml(g), /<svg/, label + ': SVG graph renders');
  } else if (model.inequalityMode === 'point') {
    points++;
    assert.deepEqual([...model.opts], ['Yes', 'No'], label + ': simple Yes/No choices');
    assert.equal(model.key, /^Yes\b/.test(p.parts[0].answer) ? 0 : 1, label + ': key matches point verdict');
  }
  const m = M.makeChoices(p);
  assert.equal(m.inequalityMode, model.inequalityMode, label + ': assessment uses shared model');
  assert.equal(m.key, model.key, label + ': assessment key matches');
}
for (const [level, cs] of Object.entries(levels)) {
  for (const skill of ['graph-hand', 'sys-ineq', 'graph-coordinate-inequality', 'graph-dashed-inequality']) {
    for (const c of cs) for (let seed = 0; seed < 12; seed++) {
      const id = [level, skill, c, seed].join('-');
      const policy = {intOnly: level !== 'honors', level};
      const p = M.generateProblem(UNIT, skill, c, policy, 'inequality-parity-' + id, null);
      assert.ok(!p.failed && p.verify?.status === 'verified', id + ': generated and verified');
      generated++;
      const model = M.inequalityChoices(p);
      if (model) validateChoice(p, model, id);
      const items = GB.makeItems(UNIT, skill, c, policy, 'inequality-game-' + id, null);
      for (const it of items.filter(x => x.inequalityMode)) {
        assert.equal(it.options.filter(o => o.ok).length, 1, id + ': exactly one game key');
        if (it.inequalityMode === 'graph') {
          assert.equal(it.options.length, 4, id + ': four graph cards in game');
          for (const opt of it.options) assert.match(M.figHtml(opt.graph), /<svg/, id + ': graph card SVG');
        } else {
          assert.equal(it.options.map(o => o.a).join('|'), 'Yes|No', id + ': point buttons in game');
        }
      }
    }
  }
  for (let seed = 0; seed < 5; seed++) {
    const cfg = M.defaultConfig(UNIT, 'test');
    cfg.level = level; cfg.seed = 5000 + seed; cfg.versions = 1;
    const st = M.newAssessment(cfg);
    fullTests++;
    for (const sec of st.versions[0].sections) for (const p of sec.items) {
      assert.ok(!p.failed && p.verify.status === 'verified', level + ': assessment question verified');
      if (p.mc) {
        assert.ok(M.checkChoices(p), level + ': cached key validates');
        if (p.mc.inequalityMode === 'graph')
          assert.match(M.choicesHtml(p), /<svg/, level + ': printable answer graphs render');
      }
    }
  }
}
// Honors' two-part situation must become a Yes/No point check when converted to MC.
for (let seed = 0; seed < 20; seed++) {
  const p = M.generateProblem(UNIT, 'sys-ineq', 7,
    {intOnly:false, level:'honors'}, 'honors-scenario-' + seed, null);
  assert.ok(!p.failed && p.verify.status === 'verified', 'Honors situation verified');
  const m = M.makeChoices(p);
  assert.equal(m.inequalityMode, 'point', 'Honors multipart point check uses Yes/No');
  assert.ok(m.derived && m.derived.parts.length === 1, 'Honors multipart point question isolated');
}
assert.ok(graphs > 100 && points > 10, 'meaningful visual and point coverage');
console.log('PASS: ' + generated + ' generated problems, ' + graphs +
  ' graph questions, ' + points + ' point checks, ' + fullTests +
  ' complete unit assessments, 20 Honors multipart checks.');
