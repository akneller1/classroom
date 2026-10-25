/* Standard tests (Format: Standard test): every student answers every question; multiple-choice parts.
   Run: node worksheet-generator/menu/tests/test-mode-tests.cjs   (SEEDS=n for more builds per unit) */
'use strict';
const assert = require('node:assert/strict');
const load = require('./load.cjs');
const env = load(['games/bank.js', 'menu/render.js']), M = env.MKMENU, GB = env.MKGAMES;
const SEEDS = +(process.env.SEEDS || 3);
let n = 0, checks = 0; const test = (name, fn) => { fn(); n++; console.log('  ✓ ' + name); };
const ok = (c, m) => { checks++; assert.ok(c, m); };
function build(unit, level, seed, versions) { const c = M.defaultConfig(unit, 'test'); c.level = level; c.seed = seed; c.versions = versions || 1; return M.newAssessment(c); }
function mcItems(st) { const out = []; st.versions.forEach((v, vi) => v.sections.forEach((s, si) => { if (M.sectionFormat(st.config, si) === 'mc') s.items.forEach(it => out.push({ it, vi, si })); })); return out; }

let flagged = 0, mcTotal = 0;
test('every unit, level and seed: a full test with checked multiple-choice questions', () => {
  for (const unit of Object.keys(M.skillSets)) for (const level of ['cp2', 'cp1', 'honors']) for (let s = 0; s < SEEDS; s++) {
    const st = build(unit, level, 1000 + s, 2), cfg = st.config, r = M.checkRules(cfg, st);
    ok(!r.errors.length, unit + ' rules: ' + r.errors.join('; '));
    ok(r.maxScore === 100 && r.totalOffered === 16 && r.totalRequired === 16, unit + ': 16 questions, 100 points, all required');
    st.versions.forEach(v => v.sections.forEach((sec, si) => sec.items.forEach((it, i) => {
      ok(!it.failed, unit + ' ' + level + ': every question generated (' + (it.reason || '') + ')');
      ok(it.c === M.itemC(cfg, si, i, sec.items.length), unit + ': difficulty follows the easier → harder ramp');
      ok(it.verify.status === 'verified', unit + ': every answer verified');
    })));
    mcItems(st).forEach(({ it }) => {
      mcTotal++;
      if (!it.mc) { flagged++; return; }
      ok(it.parts.length === 1, unit + ': multiple choice has one answer');
      ok(it.mc.opts.length === 4 && new Set(it.mc.opts.map(o => o.replace(/\s/g, ''))).size === 4, unit + ': four different choices');
      ok(it.mc.opts[it.mc.key] === it.parts[0].answer, unit + ': the key letter points at the verified answer');
      it.mc.opts.forEach((o, k) => ok(GB.answerOk(it, 0, o).ok === (k === it.mc.key), unit + ': only the key is accepted by the verifier: ' + o));
      ok(M.checkChoices(it), unit + ': stored choices re-check');
    });
  }
  console.log('    multiple-choice questions: ' + mcTotal + ', printed as short answer instead: ' + flagged);
  ok(flagged <= mcTotal * 0.02, 'at most 2% of multiple-choice slots fall back to short answer (' + flagged + ' of ' + mcTotal + ')');
});
test('versions reshuffle the letters and use different numbers', () => {
  const st = build('algebra1-systems-of-equations', 'cp1', 77, 3), keys = st.versions.map(v => v.sections[0].items.map(it => it.mc ? it.mc.key : -1).join(''));
  ok(new Set(keys).size > 1, 'the answer letters differ between versions');
  const sig = it => it.prompt + JSON.stringify(it.fig || null); ok(sig(st.versions[0].sections[0].items[0]) !== sig(st.versions[1].sections[0].items[0]), 'different problems');
});
test('moving a question between parts changes its format', () => {
  const st = build('algebra1-polynomials', 'cp1', 5, 1), mcQ = st.versions[0].sections[0].items[0], saQ = st.versions[0].sections[1].items[0];
  ok(!!mcQ.mc && !saQ.mc, 'starts as multiple choice / short answer');
  M.moveItem(st, 0, mcQ.uid, 1); ok(!M.find(st, 0, mcQ.uid).item.mc, 'moved to short answer: no choices');
  M.moveItem(st, 0, saQ.uid, 0); const moved = M.find(st, 0, saQ.uid).item; ok(!!moved.mc || !!moved.mcFail, 'moved to multiple choice: choices made (or flagged)');
  if (moved.mc) ok(M.checkChoices(moved), 'the new choices check');
  ok(st.config.sections.every(s => s.required === s.offered), 'everyone still answers everything');
});
test('editing a multiple-choice question rebuilds and re-checks its choices', () => {
  const st = build('algebra1-exponents-scientific-notation', 'cp1', 9, 1), it = st.versions[0].sections[0].items.find(x => x.mc && x.parts[0].check && x.parts[0].check.type === 'pow-simplify');
  if (!it) return;
  const p = M.applyEdit(st, 0, it.uid, { prompt: it.prompt, parts: [{ label: '', prompt: '', answer: it.parts[0].answer, keepCheck: it.parts[0].check }], steps: it.steps });
  ok(p.verify.status === 'verified', 'edited problem re-verified');
  ok(!!p.mc && M.checkChoices(p), 'choices rebuilt for the edited problem');
});
test('a save file with a tampered key letter is caught and the choices are rebuilt', () => {
  const st = build('algebra1-quadratics', 'cp1', 3, 1), it = st.versions[0].sections[0].items.find(x => x.mc);
  const o = JSON.parse(M.serialize(st)), t = o.versions[0].sections[0].items.find(x => x.uid === it.uid); t.mc.key = (t.mc.key + 1) % 4;
  const back = M.deserialize(o), b = back.versions[0].sections[0].items.find(x => x.uid === it.uid);
  ok(!!b.mc && M.checkChoices(b) && b.mc.opts[b.mc.key] === b.parts[0].answer, 'choices rebuilt with the right key');
});
test('switching the format back to a menu restores the menu sections', () => {
  const c = M.defaultConfig('algebra1-inequalities', 'test'); ok(c.mode === 'test' && c.sections.length === 2 && !c.coverage.on, 'test defaults');
  M.setMode(c, 'menu'); ok(c.mode === 'menu' && c.sections.length === 3 && c.coverage.on && c.sections[2].required === 2, 'menu defaults');
});
console.log('PASS: ' + n + ' standard-test tests (' + checks + ' checks)');
