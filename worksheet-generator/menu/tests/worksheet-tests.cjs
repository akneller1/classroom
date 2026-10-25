/* Practice worksheets (worksheet.html, mode 'worksheet'): every unit, every preset, short answer or multiple choice.
   Run: node worksheet-generator/menu/tests/worksheet-tests.cjs   (SEEDS=n for more builds per unit) */
'use strict';
const assert = require('node:assert/strict');
const load = require('./load.cjs');
const env = load(['games/bank.js', 'menu/render.js']), M = env.MKMENU, GB = env.MKGAMES;
const SEEDS = +(process.env.SEEDS || 2);
let n = 0, checks = 0; const test = (name, fn) => { fn(); n++; console.log('  ✓ ' + name); };
const ok = (c, m) => { checks++; assert.ok(c, m); };
function build(unit, level, seed, preset, versions) {
  const c = M.defaultConfig(unit, 'worksheet'); c.level = level; c.seed = seed; c.versions = versions || 1;
  if (preset) c.sections = M.worksheetSections(preset, c);
  return M.newAssessment(c);
}

test('default worksheet: practice title, one short-answer part, no points rules', () => {
  const c = M.defaultConfig('algebra1-quadratics', 'worksheet'), set = M.skillSets['algebra1-quadratics'];
  ok(c.mode === 'worksheet' && M.isWorksheet(c) && M.isTest(c), 'worksheet mode, everyone answers everything');
  ok(c.title === set.unitName + ' Practice' && c.subtitle === 'Practice worksheet', 'default titles');
  ok(c.sections.length === 1 && c.sections[0].qformat === 'open' && c.sections[0].offered === 12, '12 short-answer questions');
  ok(!c.coverage.on, 'no menu coverage rule');
  const r = M.checkRules(c, null); ok(!r.errors.length && !r.warnings.length, 'no errors or point warnings: ' + r.errors.concat(r.warnings).join('; '));
});

let mcTotal = 0, flagged = 0;
test('every unit, level, preset and seed: verified questions; multiple choice is checked', () => {
  for (const unit of Object.keys(M.skillSets)) for (const level of ['cp2', 'cp1', 'honors']) for (const preset of ['mixed', 'mc', 'both', 'skill']) for (let s = 0; s < SEEDS; s++) {
    const st = build(unit, level, 500 + s, preset, preset === 'mc' ? 2 : 1), cfg = st.config, r = M.checkRules(cfg, st);
    ok(!r.errors.length, unit + ' ' + preset + ' rules: ' + r.errors.join('; '));
    ok(!r.warnings.length, unit + ' ' + preset + ' warnings: ' + r.warnings.join('; '));
    ok(cfg.sections.every(x => x.required === x.offered), 'every question is answered');
    if (preset === 'skill') {
      const chosen = M.skillSets[unit].skills.filter(k => cfg.skills[k.id]);
      ok(cfg.sections.length === chosen.length, unit + ': one part per skill');
      st.versions[0].sections.forEach((sec, si) => sec.items.forEach(it => ok(it.skill === cfg.sections[si].skills[0], unit + ': part ' + cfg.sections[si].name + ' only uses its skill')));
    }
    st.versions.forEach(v => v.sections.forEach((sec, si) => sec.items.forEach((it, i) => {
      ok(!it.failed, unit + ' ' + level + ' ' + preset + ': generated (' + (it.reason || '') + ')');
      ok(it.verify.status === 'verified', unit + ': answer verified');
      ok(it.c === M.itemC(cfg, si, i, sec.items.length), unit + ': easier → harder');
      if (M.sectionFormat(cfg, si) !== 'mc') { ok(!it.mc, 'short-answer questions have no choices'); return; }
      mcTotal++;
      if (!it.mc) { flagged++; return; }
      ok(it.mc.opts.length === 4 && new Set(it.mc.opts.map(o => o.replace(/\s/g, ''))).size === 4, unit + ': four different choices');
      ok(it.mc.opts[it.mc.key] === it.parts[0].answer, unit + ': key letter points at the verified answer');
      it.mc.opts.forEach((o, k) => ok(GB.answerOk(it, 0, o).ok === (k === it.mc.key), unit + ': only the key passes the verifier: ' + o));
    })));
  }
  console.log('    multiple-choice questions: ' + mcTotal + ', printed as short answer instead: ' + flagged);
  ok(flagged <= mcTotal * 0.02, 'at most 2% fall back to short answer (' + flagged + ' of ' + mcTotal + ')');
});
test('switching a part to multiple choice adds checked choices; back to short answer removes them', () => {
  const st = build('algebra1-linear-equations-slope', 'cp1', 42, 'mixed');
  st.config.sections[0].qformat = 'mc'; M.rebuild(st); M.ensureFormats(st);
  const items = st.versions[0].sections[0].items;
  ok(items.filter(x => x.mc).length >= items.length - 1 && items.every(x => !x.mc || M.checkChoices(x)), 'choices made and checked');
  st.config.sections[0].qformat = 'open'; M.ensureFormats(st);
  ok(st.versions[0].sections[0].items.every(x => !x.mc), 'short answer again');
});
test('an unchecked skill makes its one-skill part an error, not a silent empty part', () => {
  const c = M.defaultConfig('algebra1-polynomials', 'worksheet'); c.sections = M.worksheetSections('skill', c);
  const first = c.sections[0].skills[0]; c.skills[first] = false;
  const r = M.checkRules(c, null); ok(r.errors.some(e => /unchecked in step 4/.test(e)), 'error explains the unchecked skill');
});
test('save and load keep the worksheet mode', () => {
  const st = build('algebra1-inequalities', 'honors', 8, 'both'), back = M.deserialize(M.serialize(st));
  ok(back.config.mode === 'worksheet' && back.config.sections.length === 2, 'mode and parts kept');
  ok(back.versions[0].sections[0].items.every(x => !x.mc || M.checkChoices(x)), 'choices still check');
});
console.log(n + ' worksheet tests passed (' + checks + ' checks).');
