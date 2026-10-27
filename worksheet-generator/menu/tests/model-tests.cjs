/* Menu Assessment Generator — engine tests (menu rules, versions, pin/regenerate, editing, save/load).
   Run: node worksheet-generator/menu/tests/model-tests.cjs */
'use strict';
const assert = require('node:assert/strict');
const load = require('./load.cjs');
const env = load(['menu/render.js']), M = env.MKMENU, UNIT = 'algebra1-expressions-equations';
let n = 0; const test = (name, fn) => { fn(); n++; console.log('  ✓ ' + name); };
const J = o => JSON.parse(JSON.stringify(o));
// objects made inside the VM have another realm's prototypes, so compare them as JSON
const deq = (a, b, msg) => assert.equal(JSON.stringify(a), JSON.stringify(b), msg);
function cfg(over) { const c = M.defaultConfig(UNIT); c.seed = 12345; return Object.assign(c, over || {}); }
function allItems(st, v) { return st.versions[v].sections.flatMap(s => s.items); }
function snapshotOf(st) { return st.versions.map(v => v.sections.map(s => s.items.map(it => it.key + '|' + it.parts.map(p => p.answer).join(';')))); }

test('default menu: 6/6/3 offered, 4/4/2 required, 100 points, no errors', () => {
  const r = M.checkRules(cfg(), null);
  assert.equal(r.maxScore, 100); assert.equal(r.totalOffered, 15); assert.equal(r.totalRequired, 10); deq(r.errors, []);
});
test('maximum score follows any point system (not hardcoded to 100)', () => {
  const c = cfg(); c.sections[0].points = 3; c.sections[1].points = 7.5; c.sections[2].points = 12;
  assert.equal(M.checkRules(c, null).maxScore, 4 * 3 + 4 * 7.5 + 2 * 12);
  c.sections = c.sections.slice(0, 2); c.sections[0].required = 2;
  assert.equal(M.checkRules(c, null).maxScore, 2 * 3 + 4 * 7.5);
});
test('impossible requirements are reported', () => {
  const c = cfg(); c.sections[1].required = 7;
  assert.ok(M.checkRules(c, null).errors.some(e => /only 6 are offered/.test(e)));
  const c2 = cfg(); c2.sections[0].points = 0; assert.ok(M.checkRules(c2, null).errors.some(e => /points/.test(e)));
  const c3 = cfg(); c3.sections.forEach(s => { s.required = 1; }); // 3 picks, more categories than that
  assert.ok(M.checkRules(c3, null).errors.some(e => /cover \d+ skill categories/.test(e)));
  const c4 = cfg(); c4.sections = []; assert.ok(M.checkRules(c4, null).errors.length);
  const c5 = cfg(); c5.sections[2].skills = ['nonexistent']; assert.ok(M.checkRules(c5, null).errors.some(e => /no skills/.test(e)));
});
test('inconsistent rules are warned about', () => {
  const c = cfg(); c.sections[2].required = 3;   // no choice
  assert.ok(M.checkRules(c, null).warnings.some(w => /no choice/.test(w)));
  const c2 = cfg(); c2.sections[2].required = 0;
  assert.ok(M.checkRules(c2, null).warnings.some(w => /not count/.test(w)));
});
test('coverage feasibility uses the actual menu (max-flow over sections)', () => {
  const c = cfg(); c.coverage.tags = ['MODEL']; c.sections.forEach(s => { s.skills = s.id === 'spc' ? ['model'] : ['two-step']; });
  c.sections[2].required = 0;  // MODEL only offered where students pick nothing
  const st = M.newAssessment(c);
  assert.ok(M.checkRules(c, st).errors.some(e => /cannot cover/.test(e)), M.checkRules(c, st).errors.join('|'));
  c.sections[2].required = 1;
  deq(M.checkRules(c, st).errors, []);
});
test('"everyone must do" items beyond the section count are an error', () => {
  const c = cfg(); c.sections[2].required = 1; const st = M.newAssessment(c);
  st.versions[0].sections[2].items.slice(0, 2).forEach(it => M.setRequired(st, 0, it.uid, true));
  assert.ok(M.checkRules(c, st).errors.some(e => /must do this/.test(e)));
});
test('build: every slot verified, distinct, coverage satisfied', () => {
  const st = M.newAssessment(cfg());
  const items = allItems(st, 0);
  assert.equal(items.length, 15);
  items.forEach(it => { assert.ok(!it.failed, it.reason); assert.equal(it.verify.status, 'verified'); });
  assert.equal(new Set(items.map(i => i.key)).size, 15);
  const tags = new Set(items.map(i => i.tag)); assert.ok(tags.size >= 4, 'Expected a varied mix of at least four skill categories');
  const coverage = M.coverageTags(st.config, st); coverage.forEach(t => assert.ok(tags.has(t), 'missing configured coverage ' + t));
  deq(M.checkRules(st.config, st).errors, []);
});
test('levels change the mathematics: CP2 < CP1 < Honors difficulty per section', () => {
  const lv = { cp2: [1, 2, 3], cp1: [3, 4, 5], honors: [5, 6, 7] };
  Object.keys(lv).forEach(k => { const st = M.newAssessment(cfg({ level: k })); st.versions[0].sections.forEach((s, si) => s.items.forEach(it => assert.equal(it.c, lv[k][si]))); });
  const cp2 = M.newAssessment(cfg({ level: 'cp2' }));
  allItems(cp2, 0).forEach(it => it.verify.computed && it.verify.computed.forEach(x => x && assert.ok(!/frac/.test(x), 'CP2 fraction answer ' + x)));
});
test('versions: same skills, difficulty and structure; different problems; own keys', () => {
  const st = M.newAssessment(cfg({ versions: 3 }));
  assert.equal(st.versions.length, 3);
  for (let si = 0; si < 3; si++) st.versions[0].sections[si].items.forEach((a, i) => {
    const b = st.versions[1].sections[si].items[i], c = st.versions[2].sections[si].items[i];
    assert.equal(a.skill, b.skill); assert.equal(a.skill, c.skill); assert.equal(a.c, b.c); assert.equal(a.c, c.c); assert.equal(a.slot, b.slot);
    assert.notEqual(a.key, b.key); assert.notEqual(b.key, c.key); assert.notEqual(a.key, c.key);
  });
});
test('regenerate one problem: nothing else changes, pinned problems are kept', () => {
  const st = M.newAssessment(cfg({ versions: 2 }));
  const before = snapshotOf(st), target = st.versions[0].sections[1].items[2];
  const r = M.regenerate(st, 0, target.uid);
  assert.ok(r && !r.failed); assert.notEqual(r.key, target.key); assert.equal(r.skill, target.skill); assert.equal(r.c, target.c);
  const after = snapshotOf(st);
  after.forEach((v, vi) => v.forEach((s, si) => s.forEach((x, i) => { if (!(vi === 0 && si === 1 && i === 2)) assert.equal(x, before[vi][si][i]); })));
  // pin two, regenerate everything in version A
  const p1 = st.versions[0].sections[0].items[0], p2 = st.versions[0].sections[2].items[1];
  M.togglePin(st, 0, p1.uid); M.togglePin(st, 0, p2.uid);
  const k1 = p1.key + p1.parts[0].answer, k2 = p2.key + p2.parts.map(x => x.answer).join();
  const bB = J(snapshotOf(st)[1]);
  const res = M.regenerateAll(st, 0);
  assert.equal(res.kept, 2);
  assert.equal(st.versions[0].sections[0].items[0].key + st.versions[0].sections[0].items[0].parts[0].answer, k1);
  assert.equal(st.versions[0].sections[2].items[1].key + st.versions[0].sections[2].items[1].parts.map(x => x.answer).join(), k2);
  deq(snapshotOf(st)[1], bB, 'regenerating version A must not touch version B');
  allItems(st, 0).forEach(it => assert.equal(M.verifyProblem(it, M.policyOf(st.config)).status, 'verified'));
});
test('change difficulty / skill apply to the slot in every version', () => {
  const st = M.newAssessment(cfg({ versions: 2 })), it = st.versions[0].sections[0].items[1];
  M.setDifficulty(st, 0, it.uid, it.c + 2);
  assert.equal(st.versions[0].sections[0].items[1].c, it.c + 2); assert.equal(st.versions[1].sections[0].items[1].c, it.c + 2);
  M.changeSkill(st, 0, st.versions[0].sections[0].items[1].uid, 'proportion');
  assert.equal(st.versions[0].sections[0].items[1].skill, 'proportion'); assert.equal(st.versions[1].sections[0].items[1].skill, 'proportion');
  assert.equal(st.versions[0].sections[0].items[1].verify.status, 'verified');
});
test('move, reorder, delete, undo delete, add', () => {
  const st = M.newAssessment(cfg({ versions: 2 })), it = st.versions[0].sections[0].items[0], slot = it.slot;
  M.moveItem(st, 0, it.uid, 2);
  assert.equal(st.config.sections[0].offered, 5); assert.equal(st.config.sections[2].offered, 4);
  assert.equal(st.versions[1].sections[2].items[3].slot, slot);
  const d = st.versions[0].sections[1].items[0], info = M.deleteItem(st, 0, d.uid);
  assert.equal(st.versions[0].sections[1].items.length, 5); assert.equal(st.versions[1].sections[1].items.length, 5);
  M.undoDelete(st, info); assert.equal(st.versions[0].sections[1].items[0].uid, d.uid); assert.equal(st.config.sections[1].offered, 6);
  const a = M.addItem(st, 1, 'literal', 6);
  assert.equal(a.skill, 'literal'); assert.equal(a.c, 6); assert.equal(st.versions[1].sections[1].items.length, 7);
  const before = st.versions[0].sections[1].items.map(x => x.uid);
  M.reorder(st, 0, before[3], -1); assert.equal(st.versions[0].sections[1].items[2].uid, before[3]);
});
test('removing slots when "offered" is lowered keeps pinned and edited problems', () => {
  const st = M.newAssessment(cfg()); const items = st.versions[0].sections[0].items;
  M.togglePin(st, 0, items[5].uid); const keep = items[5].uid;
  st.config.sections[0].offered = 3; M.syncStructure(st);
  assert.equal(st.versions[0].sections[0].items.length, 3);
  assert.ok(st.versions[0].sections[0].items.some(x => x.uid === keep));
});
test('edited problems are re-verified from scratch (old answers are not trusted)', () => {
  const st = M.newAssessment(cfg()), it = st.versions[0].sections[1].items[0];
  // teacher changes the equation but leaves the old answer
  const e = M.applyEdit(st, 0, it.uid, { prompt: 'Solve ⟨3x+4=19⟩.', parts: [{ answer: '⟨x=7⟩', checkType: 'solve', checkMath: '3x+4=19', checkVar: 'x' }] });
  assert.equal(e.verify.status, 'mismatch'); assert.equal(e.approved, false); assert.equal(e.pinned, true);
  assert.equal(e.verify.computed[0], 'x=5');
  const e2 = M.applyEdit(st, 0, e.uid, { prompt: 'Solve ⟨3x+4=19⟩.', parts: [{ answer: '⟨x=5⟩', checkType: 'solve', checkMath: '3x+4=19', checkVar: 'x' }] });
  assert.equal(e2.verify.status, 'verified'); assert.equal(e2.approved, true);
  // a check that names math not printed in the question is rejected
  const e3 = M.applyEdit(st, 0, e2.uid, { prompt: 'Solve ⟨3x+4=19⟩.', parts: [{ answer: '⟨x=1⟩', checkType: 'solve', checkMath: '3x+4=7', checkVar: 'x' }] });
  assert.equal(e3.verify.status, 'invalid');
  // no automatic check: needs teacher approval, and the key flags it until approved
  const e4 = M.applyEdit(st, 0, e3.uid, { prompt: 'Explain the error in Dev’s work.', parts: [{ answer: 'He forgot to distribute.', checkType: 'none' }] });
  assert.equal(e4.verify.status, 'manual'); assert.equal(e4.approved, false);
  assert.ok(M.blockers(st).some(b => /approval/.test(b)));
  M.approve(st, 0, e4.uid, true); assert.ok(!M.blockers(st).some(b => /approval/.test(b)));
});
test('editing a word problem keeps its scenario check, which re-reads the edited numbers', () => {
  const c = cfg({ level: 'cp2' }); c.sections.forEach(s => { s.skills = ['model']; }); c.coverage.on = false;
  const st = M.newAssessment(c), it = st.versions[0].sections[0].items.find(x => /charges a \$/.test(x.prompt) && x.parts.length === 2);
  assert.ok(it, 'need a fee-rate problem');
  const parts = it.parts.map(p => ({ answer: p.answer, keepCheck: p.check }));
  const changed = it.prompt.replace(/A bill is \$(\d+)/, (m, d) => 'A bill is $' + (+d + it.prompt.match(/plus \$(\d+)/)[1] * 1));
  const e = M.applyEdit(st, 0, it.uid, { prompt: changed, parts });
  assert.equal(e.verify.status, 'mismatch', 'old answer must no longer match the edited numbers');
});
test('teacher-written problems are added to every version and verified', () => {
  const st = M.newAssessment(cfg({ versions: 2 }));
  const p = M.addManual(st, 2, { prompt: 'Solve ⟨\\frac{x}{3}+2=6⟩.', tag: 'SOLVE', parts: [{ answer: '⟨x=12⟩', checkType: 'solve', checkMath: '\\frac{x}{3}+2=6', checkVar: 'x' }] });
  assert.equal(p.verify.status, 'verified'); assert.equal(st.versions[1].sections[2].items.length, 4);
});
test('problem bank: preview with answers, then add one to the menu', () => {
  const st = M.newAssessment(cfg({ versions: 2 }));
  const r = M.fillBank(st, 'both-sides', 4, 10);
  assert.equal(r.made, 10); assert.equal(new Set(st.bank.items.map(b => b.key)).size, 10);
  st.bank.items.forEach(b => { assert.equal(b.verify.status, 'verified'); assert.ok(b.steps.length > 2); });
  const pick = st.bank.items[3];
  M.useBankItem(st, pick.uid, 1);
  const added = st.versions[0].sections[1].items[6];
  assert.equal(added.uid, pick.uid); assert.equal(added.pinned, true);
  assert.equal(st.versions[1].sections[1].items[6].skill, 'both-sides'); assert.equal(st.bank.items.length, 9);
});
test('rebuild after a level change keeps pinned/edited slots and re-levels the rest', () => {
  const st = M.newAssessment(cfg({ versions: 2 })), keep = st.versions[0].sections[1].items[0];
  M.togglePin(st, 0, keep.uid);
  st.config.level = 'honors'; M.rebuild(st);
  assert.equal(st.versions[0].sections[1].items[0].uid, keep.uid);
  assert.equal(st.versions[0].sections[1].items[1].c, 6); assert.equal(st.versions[0].sections[2].items[0].c, 7);
});
test('save → load round trip, and tampered keys are caught on load', () => {
  const st = M.newAssessment(cfg({ versions: 2 }));
  const txt = M.serialize(st), back = M.deserialize(txt);
  deq(snapshotOf(back), snapshotOf(st));
  const o = JSON.parse(txt); const it = o.versions[1].sections[1].items[0];
  it.parts[0].answer = it.parts[0].answer.replace(/(\d+)(?!.*\d)/, d => String(+d + 3));
  const bad = M.deserialize(o);
  assert.notEqual(bad.versions[1].sections[1].items[0].verify.status, 'verified');
  assert.ok(M.blockers(bad).length >= 1);
  assert.throws(() => M.deserialize('{"format":"other"}'));
  const dup = M.duplicate(st); assert.match(dup.config.title, /copy/);
});
test('generation failure is reported, never silently substituted', () => {
  const c = cfg(); c.sections = [{ id: 'x', name: 'Only', points: 5, offered: 40, required: 1, tier: 0, adjust: -5, skills: ['literal'] }]; c.coverage.on = false;
  c.level = 'cp2';
  const st = M.newAssessment(c), items = allItems(st, 0);
  const failed = items.filter(i => i.failed);
  items.filter(i => !i.failed).forEach(i => { assert.equal(i.skill, 'literal'); assert.equal(i.verify.status, 'verified'); });
  failed.forEach(f => { assert.match(f.reason, /Could not make a verified/); });
  if (failed.length) assert.ok(M.blockers(st).some(b => /no verified problem/.test(b)));
  console.log('      (' + failed.length + ' of 40 level-1 literal slots reported as unavailable instead of repeated)');
});
test('a generator that produces wrong keys is never used: the slot is flagged for the teacher', () => {
  M.registerSkillSet({ id: 'test-broken', title: 'Broken', unitName: 'Broken', tags: { SOLVE: 'Solve' }, gaps: [], skills: [
    { id: 'wrong-key', tag: 'SOLVE', name: 'Wrong key', generate: ctx => { const a = ctx.rng.int(1, 50); return { variant: 'w', prompt: 'Solve ⟨x+' + a + '=' + (a + 2) + '⟩.', parts: [{ answer: '⟨x=5⟩', check: { type: 'solve', eq: 'x+' + a + '=' + (a + 2), v: 'x' } }], steps: [{ t: '', m: 'x=5', w: 1 }] }; } }
  ] });
  const c = M.defaultConfig('test-broken'); c.coverage.on = false;
  const st = M.newAssessment(c), items = allItems(st, 0);
  assert.ok(items.length > 0);
  items.forEach(it => { assert.equal(it.failed, true); assert.match(it.reason, /verifier/); });
  assert.ok(M.blockers(st).some(b => /no verified problem/.test(b)));
});
test('rubric points always add up to the dish value', () => {
  const st = M.newAssessment(cfg({ level: 'honors' }));
  st.config.sections.forEach((s, si) => st.versions[0].sections[si].items.forEach(it => {
    [s.points, 7, 2.5, 1].forEach(pts => { const r = M.rubric ? M.rubric(it, pts) : null; if (r) assert.equal(r.reduce((a, b) => a + b.pts, 0), pts); });
  }));
});
console.log('PASS: ' + n + ' engine tests');
