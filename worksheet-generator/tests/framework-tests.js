/* Framework-level tests: determinism, versions, duplicates, regenerate-one, answer-key pairing. */
'use strict';
const NS = require('./load.js');
const UNIT = 'algebra1-linear-functions';
const ids = Object.keys(NS.registry.lessons);
let checks = 0; const fails = [];
function ok(c, msg) { checks++; if (!c) fails.push(msg); }
const sig = ws => JSON.stringify(ws.versions.map(v => v.sections.map(s => s.problems.map(p => [p.prompt, p.answer, p.steps]))));
function mk(over) { const s = NS.defaultSettings(); Object.assign(s, over); return s; }

for (let t = 0; t < 40; t++) {
  const lessons = {}; ids.forEach((id, i) => { if ((i * 7 + t) % 3 !== 0) lessons[id] = 1 + ((i + t) % 5); });
  const base = { lessons, seed: 1000 + t, versions: 3, difficulty: ['basic', 'standard', 'honors'][t % 3], numberMode: ['integers', 'preferred', 'fractions'][(t >> 1) % 3], grids: t % 4 !== 0 };
  const ws1 = NS.buildWorksheet(mk(base), UNIT), ws2 = NS.buildWorksheet(mk(base), UNIT);
  // determinism
  ok(sig(ws1) === sig(ws2), `t${t}: same seed gave different worksheets`);
  // different seed differs
  ok(sig(ws1) !== sig(NS.buildWorksheet(mk(Object.assign({}, base, { seed: base.seed + 1 })), UNIT)), `t${t}: different seed gave identical worksheet`);
  // versions: same lessons, same counts, same order
  const shape = v => v.sections.map(s => s.lessonId + ':' + s.problems.length).join(',');
  ok(shape(ws1.versions[0]) === shape(ws1.versions[1]) && shape(ws1.versions[1]) === shape(ws1.versions[2]), `t${t}: versions differ in shape`);
  // expected counts equal request, in unit order
  const want = NS.orderedLessons(mk(base), UNIT).map(p => p.id + ':' + p.count).join(',');
  ok(shape(ws1.versions[0]) === want, `t${t}: counts/order mismatch`);
  // no repeated problems anywhere (fine key) and no repeated prompts+figures within a version
  const seen = new Set();
  ws1.versions.forEach(v => v.sections.forEach(s => s.problems.forEach(p => {
    ok(!seen.has(p.key), `t${t}: duplicate problem key ${p.key}`); seen.add(p.key);
    ok(p.answer !== undefined && p.prompt && Array.isArray(p.steps), `t${t}: malformed problem ${s.lessonId}`);
  })));
  // versions use different values: no two versions share an identical prompt+answer for the same slot
  ws1.versions[0].sections.forEach((s, si) => s.problems.forEach((p, pi) => {
    [1, 2].forEach(v => { const q = ws1.versions[v].sections[si].problems[pi]; ok(!(q.prompt === p.prompt && JSON.stringify(q.fig) === JSON.stringify(p.fig)), `t${t}: version ${v} repeats version A at ${s.lessonId}#${pi}`); });
  }));
  // regenerate one problem: only that problem changes
  const ws = NS.buildWorksheet(mk(base), UNIT);
  const before = JSON.parse(JSON.stringify(ws.versions.map(v => v.sections.map(s => s.problems.map(p => p.key)))));
  const vi = t % 3, si = t % ws.versions[vi].sections.length, pi = 0, old = ws.versions[vi].sections[si].problems[pi].key;
  NS.regenerateProblem(ws, vi, si, pi);
  const after = ws.versions.map(v => v.sections.map(s => s.problems.map(p => p.key)));
  let changed = 0;
  after.forEach((v, a) => v.forEach((s, b) => s.forEach((k, c) => { if (k !== before[a][b][c]) { changed++; ok(a === vi && b === si && c === pi, `t${t}: regenerate changed the wrong problem`); } })));
  ok(changed === 1, `t${t}: regenerate changed ${changed} problems (want 1)`);
  ok(after[vi][si][pi] !== old, `t${t}: regenerated problem identical to old`);
  // rebuilding from saved salts reproduces the regenerated worksheet and nothing else moves
  const rebuilt = NS.buildWorksheet(Object.assign(mk(base), { pinned: ws.settings.pinned }), UNIT);
  ok(sig(rebuilt) === sig(ws), `t${t}: rebuild from pinned problems differs from the regenerated worksheet`);
  // pins are ignored once difficulty changes
  const other = NS.buildWorksheet(Object.assign(mk(base), { pinned: ws.settings.pinned, difficulty: base.difficulty === 'basic' ? 'honors' : 'basic' }), UNIT);
  ok(sig(other) !== sig(ws), `t${t}: stale pins applied after difficulty change`);
  // appending more problems to one skill leaves the earlier ones alone
  const more = Object.assign({}, base, { lessons: Object.assign({}, lessons) }); const k0 = Object.keys(lessons)[0]; more.lessons[k0] = lessons[k0] + 2;
  const wm = NS.buildWorksheet(mk(more), UNIT), s0 = wm.versions[0].sections.find(s => s.lessonId === k0), o0 = ws1.versions[0].sections.find(s => s.lessonId === k0);
  o0.problems.forEach((p, i) => ok(s0.problems[i].key === p.key, `t${t}: adding problems changed existing problem ${k0}#${i}`));
}
// single lesson: 20 problems in one sheet have no duplicate keys, for every lesson and mode
ids.forEach(id => ['integers', 'fractions'].forEach(m => ['basic', 'honors'].forEach(d => {
  const ws = NS.buildWorksheet(mk({ lessons: { [id]: 12 }, versions: 1, seed: 9, numberMode: m, difficulty: d }), UNIT);
  const k = ws.versions[0].sections[0].problems.map(p => p.key);
  ok(new Set(k).size === k.length, `${id}/${m}/${d}: duplicates in 12 problems`);
})));
// answer key pairing: every problem has what the key renders
ids.forEach(id => { const p = NS.generateOne(id, { seed: 5 }); ok(typeof p.answer === 'string' && p.answer.length > 0, `${id}: empty answer`); });
// empty selection
ok(NS.buildWorksheet(mk({ lessons: {} }), UNIT).versions[0].sections.length === 0, 'empty selection should build empty worksheet');

console.log(`${checks} framework checks`);
if (fails.length) { console.log(fails.length + ' FAILED'); fails.slice(0, 25).forEach(f => console.log(' - ' + f)); process.exit(1); }
console.log('ALL FRAMEWORK CHECKS PASSED');
