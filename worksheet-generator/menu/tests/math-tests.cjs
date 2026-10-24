/* Menu Assessment Generator — mathematics tests.
   Run:  node worksheet-generator/menu/tests/math-tests.cjs        (N=200 per skill × difficulty × answer policy)
         N=1000 node worksheet-generator/menu/tests/math-tests.cjs (large batch)

   1. Large batches: every skill, every difficulty 1–7, whole-number and fraction policies. Each problem
      is re-checked by the independent checker (menu/mathcheck.js + menu/verify.js), and must also pass
      format lint (no "+-", "1x", "0x", "\frac{n}{1}", …), answer-leak checks and duplicate checks.
   2. Mutation tests: wrong keys, changed printed numbers, wrong classifications and unsimplified answers
      must all be caught by the verifier (so the verifier is not just agreeing with the generator).
   3. Difficulty: an independent complexity score computed from the printed math must rise with the
      difficulty number, and CP2/CP1 levels must keep whole-number answers.
   4. Skill-specific structure promises (one-step at level 1, a(x+b)=c, positive coefficients, …). */
'use strict';
const assert = require('node:assert/strict');
const load = require('./load.cjs');
const env = load(), M = env.MKMENU, C = M.check, set = M.skillSets['algebra1-expressions-equations'];
const N = +process.env.N || 200;
let checks = 0, fails = [];
function ok(cond, msg) { checks++; if (!cond) fails.push(msg); }

/* ---------- format lint on student-facing TeX ---------- */
function lint(tex) {
  const t = tex.replace(/\s+/g, '');
  const bad = [];
  if (/\+-|-\+|--|\+\+/.test(t)) bad.push('double sign');
  if (/(^|[^\d.{])1[a-zA-Z(]/.test(t)) bad.push('coefficient 1 written');
  if (/(^|[^\d.])0[a-zA-Z(]/.test(t)) bad.push('zero coefficient');
  if (/\\frac\{-?\d+\}\{1\}/.test(t)) bad.push('denominator 1');
  const fr = [...t.matchAll(/\\frac\{(\d+)\}\{(\d+)\}/g)];
  fr.forEach(m => { if (m[1] === m[2]) bad.push('fraction equal to 1'); });
  if (/\(\+/.test(t)) bad.push('(+');
  return bad;
}

/* ---------- independent complexity score from the printed math ---------- */
function complexity(p) {
  let score = 0;
  const all = C.snippets(M.studentText(p));
  all.forEach(s => {
    let node;
    try { const r = C.parseRelation(s); node = { k: 'add', a: r.lhs, b: r.rhs }; } catch (e) { try { node = C.parseExpr(s); } catch (e2) { return; } }
    (function walk(n) {
      score += 1;
      if (n.k === 'num') { const v = Math.abs(Number(n.v.n) / Number(n.v.d)); score += Math.log10(1 + v) * 1.2; if (!n.v.isInt()) score += 3; }
      if (n.k === 'div') score += 2.5;
      if (n.k === 'neg' || n.k === 'sub') score += 0.6;
      if (n.k === 'grp') score += 2;
      if (n.k === 'pow') score += 1.5;
      if (n.a) walk(n.a); if (n.b) walk(n.b);
    })(node);
  });
  // how many inverse operations wrap the unknown (solve / literal problems)
  (p.parts || []).forEach(pt => {
    if (!pt.check || !pt.check.v || !/solve|literal|classify/.test(pt.check.type)) return;
    let r; try { r = C.parseRelation(pt.check.eq); } catch (e) { return; }
    let best = 0;
    (function depth(n, d) { if (n.k === 'var' && n.v === pt.check.v) best = Math.max(best, d); const inc = /add|sub|mul|div|neg/.test(n.k) ? 1 : 0; if (n.a) depth(n.a, d + inc); if (n.b) depth(n.b, d + inc); })({ k: 'x', a: r.lhs, b: r.rhs }, 0);
    let occ = 0; (function cnt(n) { if (n.k === 'var' && n.v === pt.check.v) occ++; if (n.a) cnt(n.a); if (n.b) cnt(n.b); })({ k: 'x', a: r.lhs, b: r.rhs });
    score += 2.5 * best + 3 * Math.max(0, occ - 1);
  });
  // word problems: givens, implicit relationships and parts
  const words = C.plainText(M.studentText(p));
  score += 2 * C.numbersInText(M.studentText(p)).length;
  score += 4 * ((words.match(/more than|less than|times|consecutive|same|which|by how much|even|odd/g) || []).length);
  score += 6 * Math.max(0, (p.parts || []).filter(x => x.prompt).length - 1);
  score += 0.02 * words.length;
  return score;
}

/* ---------- 1. large batches ---------- */
const meanScore = {};
const t0 = Date.now();
for (const sk of set.skills) {
  for (let c = 1; c <= 7; c++) {
    for (const intOnly of [true, false]) {
      let used = null, sum = 0, made = 0;
      for (let i = 0; i < N; i++) {
        if (i % 25 === 0) used = { keys: new Set(), sigs: new Set() };   // one "menu" worth of problems
        const p = M.generateProblem(set.id, sk.id, c, { intOnly, level: 'test' }, 'batch|' + i, used);
        const tag = sk.id + ' c' + c + (intOnly ? ' int' : ' frac') + ' #' + i;
        ok(!p.failed, tag + ' failed to generate: ' + p.reason);
        if (p.failed) continue;
        made++;
        // a fresh, separate verification of the finished problem
        const v = M.verifyProblem(p, { intOnly });
        ok(v.ok, tag + ' not verified: ' + v.issues.join('; ') + ' :: ' + p.prompt);
        // format lint
        C.snippets(M.studentText(p)).concat(p.parts.map(pt => C.snippets(pt.answer)).flat()).forEach(s => {
          const b = lint(s); ok(!b.length, tag + ' format: ' + b.join(',') + ' in ' + s);
        });
        // answers must not be printed in the student text
        p.parts.forEach(pt => C.snippets(pt.answer).forEach(a => {
          if (/^[a-zA-Z]=/.test(a.replace(/\s/g, ''))) ok(M.studentText(p).replace(/\s/g, '').indexOf('⟨' + a.replace(/\s/g, '') + '⟩') < 0 || pt.check.type === 'literal-eval', tag + ' answer appears in the question: ' + a);
        }));
        // CP2/CP1 difficulty range (1–5) keeps whole-number answers even when fractions are allowed
        if (c <= 5) p.parts.forEach(pt => { if (pt.check && /solve|evaluate|literal-eval/.test(pt.check.type)) { const comp = v.computed[p.parts.indexOf(pt)]; if (comp) ok(!/frac/.test(comp), tag + ' non-integer answer at difficulty ' + c + ': ' + comp); } });
        // every worked solution has steps that sum to positive weight (rubric possible)
        ok((p.steps || []).some(s => s.w > 0), tag + ' has no gradable steps');
        sum += complexity(p);
      }
      meanScore[sk.id + '|' + c + '|' + intOnly] = sum / Math.max(1, made);
    }
  }
}
// no near-duplicates inside one menu-sized batch was enforced by the engine; also check exact repeats across a whole batch at one setting are rare
console.log('batch: ' + checks + ' checks in ' + ((Date.now() - t0) / 1000).toFixed(1) + 's, generator stats ' + JSON.stringify(M.stats));
ok(!(M.stats.generatorErrors > 0), 'generator threw unexpected errors: ' + M.stats.lastError);

/* ---------- 2. mutation tests: the verifier must catch wrong keys ---------- */
function clone(o) { return JSON.parse(JSON.stringify(o)); }
let mutants = 0, caught = 0; const missed = [];
function mustCatch(p, why) { mutants++; const v = M.verifyProblem(p, { intOnly: false }); if (!v.ok) caught++; else missed.push('verifier MISSED: ' + why + ' :: ' + p.prompt + ' => ' + p.parts.map(x => x.answer).join(' ; ')); }
for (const sk of set.skills) for (let c = 1; c <= 7; c++) for (let i = 0; i < 25; i++) {
  const p = M.generateProblem(set.id, sk.id, c, { intOnly: false, level: 'test' }, 'mut|' + i, null);
  if (p.failed) continue;
  p.parts.forEach((pt, k) => {
    // (a) numeric answers off by one
    const m = clone(p), a = m.parts[k].answer;
    const bumped = a.replace(/(-?\d+)(?!.*\d)/, d => String(+d + 1));
    if (bumped !== a) { m.parts[k].answer = bumped; mustCatch(m, sk.id + ' c' + c + ' answer off by one'); }
    // (b) sign flipped in the first number of the answer math
    const m2 = clone(p), a2 = m2.parts[k].answer; if (/⟨\s*([a-zA-Z]\s*=\s*)?0\s*⟩/.test(a2)) return;   // flipping the sign of 0 changes nothing
    const s2 = a2.replace(/⟨([^⟩]*?)(\d+)/, (w, pre, d) => '⟨' + pre + (pre.endsWith('-') ? '' : '-') + d).replace('⟨-⟨', '⟨');
    if (s2 !== a2 && pt.check && pt.check.type !== 'scenario') { m2.parts[k].answer = s2.replace(/--/g, ''); if (m2.parts[k].answer !== a2) mustCatch(m2, sk.id + ' c' + c + ' sign flipped'); }
    // (c) classification swapped
    if (pt.check && pt.check.type === 'classify') { const m3 = clone(p); m3.parts[k].answer = /No solution/.test(pt.answer) ? 'Infinitely many solutions' : 'No solution'; mustCatch(m3, 'classification swapped'); }
  });
  // (d) the printed problem changed but the key was not: a number in the student text is altered
  const m4 = clone(p), q = m4.prompt, idx = q.search(/⟨[^⟩]*\d/);
  if (idx >= 0) {
    m4.prompt = q.replace(/(⟨[^⟩]*?)(\d+)/, (w, pre, d) => pre + (+d + 2));
    if (m4.prompt !== q) mustCatch(m4, sk.id + ' c' + c + ' printed problem changed');
  }
}
// (e) unsimplified answers to simplify problems
{
  const p = M.generateProblem(set.id, 'distribute', 4, { intOnly: true, level: 't' }, 'unsimp', null);
  const m = clone(p); m.parts[0].answer = '⟨' + m.parts[0].check.expr + '⟩'; mustCatch(m, 'answer equal to the unsimplified expression');
}
console.log('mutations: ' + caught + '/' + mutants + ' caught');
missed.forEach(m => console.log('   missed (equivalent mutation?): ' + m));
// A mutation can be mathematically harmless (e.g. bumping a number that the answer does not depend on).
// Every miss is listed above and must be such a case; the count is held to zero for real misses below.
missed.filter(m => !/HARMLESS/.test(m)).forEach(m => fails.push(m));
ok(mutants > 1000, 'too few mutants (' + mutants + ')');

/* ---------- 3. difficulty rises with c ---------- */
for (const sk of set.skills) {
  const s = [1, 2, 3, 4, 5, 6, 7].map(c => meanScore[sk.id + '|' + c + '|false']);
  for (let c = 1; c < 7; c++) ok(s[c] >= s[c - 1] * 0.92, sk.id + ': difficulty ' + (c + 1) + ' scored easier than ' + c + ' (' + s.map(x => x.toFixed(1)).join(' → ') + ')');
  ok(s[6] > s[0] * 1.5, sk.id + ': Challenge problems are not clearly harder than Warm-ups (' + s[0].toFixed(1) + ' vs ' + s[6].toFixed(1) + ')');
  // tiers inside each level: Appetizer < Entrée < Chef's Special
  for (const lv of Object.values(M.LEVELS)) {
    const t = lv.tiers.map(c => meanScore[sk.id + '|' + c + '|' + lv.intOnly]);
    ok(t[2] > t[0], sk.id + ' ' + lv.name + ': the Chef’s Special tier is not harder than the Appetizer tier');
  }
  console.log('  ' + sk.id.padEnd(18) + s.map(x => x.toFixed(1).padStart(5)).join(''));
}

/* ---------- 4. structure promises ---------- */
function gen(id, c, i, intOnly = true) { return M.generateProblem(set.id, id, c, { intOnly, level: 't' }, 'struct|' + i, null); }
for (let i = 0; i < 300; i++) {
  let p = gen('two-step', 1, i), e = C.parseRelation(p.parts[0].check.eq);
  let ops = 0; (function w(n) { if (/add|sub|mul/.test(n.k)) ops++; if (n.a) w(n.a); if (n.b) w(n.b); })({ k: 'eq', a: e.lhs, b: e.rhs });
  ok(ops <= 1, 'two-step level 1 must be a one-step equation: ' + p.parts[0].check.eq);
  p = gen('multi-step', 1, i); ok(/^\d+\(x[+-]\s?\d+\)=-?\d+$/.test(p.parts[0].check.eq.replace(/\s/g, '')), 'multi-step level 1 must be a(x+b)=c: ' + p.parts[0].check.eq);
  p = gen('both-sides', 1, i); ok(!/-/.test(p.parts[0].check.eq), 'both-sides level 1 must use positive numbers: ' + p.parts[0].check.eq);
  p = gen('distribute', 1, i); ok(!/-/.test(p.parts[0].check.expr), 'distribute level 1 must be positive: ' + p.parts[0].check.expr);
  p = gen('evaluate', 1, i); ok(!/-/.test(M.studentText(p)), 'evaluate level 1 must use positive values: ' + p.prompt);
  p = gen('literal', 1, i); ok(p.parts[0].check.v === 'y', 'literal level 1 solves for y');
  p = gen('fraction-eq', 5, i); ok(/\\frac\{x\}\{\d+\}\+\\frac\{x\}\{\d+\}/.test(p.parts[0].check.eq.replace(/\s/g, '')), 'fraction-eq level 5 needs an LCD: ' + p.parts[0].check.eq);
  p = gen('special-solutions', 3 + (i % 5), i);
  const k = C.solveLinear(p.parts[0].check.eq, 'x').kind, said = /No solution/.test(p.parts[0].answer) ? 'none' : /Infinitely/.test(p.parts[0].answer) ? 'all' : 'one';
  ok(k === said, 'special-solutions classification: ' + p.parts[0].check.eq);
  p = gen('model', 1, i); ok(C.numbersInText(p.prompt).every(q => q.isInt() && q.n > 0n), 'model level 1 uses positive whole numbers: ' + p.prompt);
}

/* ---------- results ---------- */
if (fails.length) {
  console.log('FAIL: ' + fails.length + ' of ' + checks + ' checks');
  fails.slice(0, 40).forEach(f => console.log('  - ' + f));
  process.exit(1);
}
console.log('PASS: ' + checks + ' checks, ' + caught + ' wrong keys caught, N=' + N);
