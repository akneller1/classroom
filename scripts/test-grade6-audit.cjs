#!/usr/bin/env node
// Grade 6 audit (2026-11-19). Batch 6A: #1 grading of the self-checked short answers, #3 error-analysis items, #9/#10 tags,
// #15 vocabulary, #20 text clean-up. (#2, the key checker, runs as python3 tools/grade6-audit-20261119/verify_keys.py.)
'use strict';
const fs = require('fs'), vm = require('vm'), path = require('path'), assert = require('assert/strict');
const ROOT = path.resolve(__dirname, '..'), rd = (f) => fs.readFileSync(path.join(ROOT, f), 'utf8');
const bank = (course) => fs.readdirSync(path.join(ROOT, 'question-banks', course)).filter((f) => f.endsWith('.json'))
  .flatMap((f) => JSON.parse(rd(`question-banks/${course}/${f}`)).questions || []);
const all = bank('math6');
const text = (q) => [q.prompt, typeof q.answer === 'string' ? q.answer : JSON.stringify(q.answer), ...(q.solutionSteps || []),
  ...(q.options || []).map((o) => o.text), ...(q.parts || []).flatMap((p) => [p.prompt, p.answer])].join(' ');

// #1 grading
const c = {}; c.window = c; vm.createContext(c);
for (const f of ['menu/mathcheck.js', 'practice/radical-grading.js', 'practice/exact-grading.js', 'practice/calculus-grading.js', 'practice/stat-grading.js', 'practice/grading.js'])
  vm.runInContext(rd('worksheet-generator/' + f), c, { filename: f });
const P = c.MKPRACTICE, g = (k, t, p) => P.gradeBank(k, t, p || '').status;
const Q = 'In which quadrant is the point (1, -8)?', CMP = 'Compare using <, >, or =: -12 ___ -1', MIX = 'Mix A uses 3 cups of juice for every 9 cups of water. Mix B uses 5 cups of juice for every 7 cups of water. Which mix is fruitier?';
const cases = [
  ['Quadrant IV', 'IV', Q, 'correct'], ['Quadrant IV', 'quadrant 4', Q, 'correct'], ['Quadrant IV', 'Q4', Q, 'correct'], ['Quadrant IV', 'Quadrant II', Q, 'incorrect'], ['Quadrant IV', 'down right', Q, 'invalid'],
  ['x-axis', 'x axis', 'Where is the point (5, 0)?', 'correct'], ['x-axis', 'y-axis', 'Where is the point (5, 0)?', 'incorrect'],
  ['<', '<', CMP, 'correct'], ['<', 'less than', CMP, 'correct'], ['<', '>', CMP, 'incorrect'], ['<', '-12', CMP, 'invalid'],
  ['Mix B', 'mix b', MIX, 'correct'], ['Mix B', 'Mix A', MIX, 'incorrect'],
  ['c = 12n', '12n = c', 'Write an equation for c in terms of n.', 'correct'], ['c = 12n', 'c=12*n', 'Write an equation for c in terms of n.', 'correct'],
  ['c = 12n', 'c = 12 + n', 'Write an equation for c in terms of n.', 'incorrect'], ['c = 12n', '12n', 'Write an equation for c in terms of n.', 'invalid'],
  ['c = 12n', '2c = 24n', 'Write an equation for c in terms of n.', 'incorrect'], ['11n = 605', '605 = 11n', 'Write an equation: 11 times a number n is 605.', 'correct'],
  ['10n - 15', '-15 + 10n', 'Write an algebraic expression for the phrase: “15 less than 10 times a number n.”', 'correct'],
  ['10n - 15', '15 - 10n', 'Write an algebraic expression for the phrase: “15 less than 10 times a number n.”', 'incorrect'],
  ['2n - 6', '2n-6', 'Use the Distributive Property to simplify 2(n - 3).', 'correct'], ['2n - 6', '2(n - 3)', 'Use the Distributive Property to simplify 2(n - 3).', 'invalid'],
  ['13k + 4', '7k + 4 + 6k', 'Simplify: 7k + 4 + 6k', 'invalid'], ['13k + 4', '4 + 13k', 'Simplify: 7k + 4 + 6k', 'correct'],
  ['-10 < -9; the diver', '-10<-9; diver', 'A fish is at -10 m and a diver is at -9 m relative to sea level.', 'correct'],
  ['-10 < -9; the diver', '-9 > -10; the diver', 'A fish is at -10 m and a diver is at -9 m relative to sea level.', 'incorrect'],
  ['-10 < -9; the diver', '-10 < -9; the fish', 'A fish is at -10 m and a diver is at -9 m relative to sea level.', 'incorrect'],
  ['Femi, $20', 'Femi, 20', "Jamal's account balance is -$18 and Femi's is -$38. Who owes more money, and how much more?", 'correct'],
  ['Femi, $20', 'Jamal, $20', "Jamal's account balance is -$18 and Femi's is -$38. Who owes more money, and how much more?", 'incorrect'],
  ['x = 5', '5', 'Solve: x + 2 = 7', 'correct'], ['y = 2x + 3', 'y = 3 + 2x', 'Write the equation of the line.', 'correct'], ['1 1/4', '5/4', '', 'correct'],
];
for (const [k, t, p, want] of cases) assert.equal(g(k, t, p), want, `key ${k}, typed ${t}`);
let auto = 0, sa = 0;
for (const q of all) if (q.format === 'short-answer' && typeof q.answer === 'string') {
  sa++;
  if (P.bankAnswer(q.answer, q.prompt) === null) continue;
  auto++; assert.equal(g(q.answer, q.answer, q.prompt), 'correct', q.id + ' key grades itself correct: ' + q.answer);
}
assert(auto / sa >= 0.98, `auto-graded share ${auto}/${sa}`);
// every other course's keys still grade themselves correct
for (const course of ['prealgebra', 'prealgebra7', 'algebra2', 'precalculus', 'calculus', 'statistics', 'discrete'])
  for (const q of bank(course)) if (q.format === 'short-answer' && typeof q.answer === 'string' && P.bankAnswer(q.answer, q.prompt) !== null)
    assert.equal(g(q.answer, q.answer, q.prompt), 'correct', q.id + ' key grades itself correct: ' + q.answer);
assert(/bankAnswer\(q\.answer,q\.prompt\)/.test(rd('worksheet-generator/practice/practice.js')), 'practice.js passes the prompt when choosing auto-grading');
assert(/practice\/grading\.js\?v=g6-audit-20261119/.test(rd('worksheet-generator/practice-test.html')), 'grader cache version bumped');

// #3 error analysis: the answer shown is never the key
for (const q of all.filter((q) => /answered this problem incorrectly/.test(q.prompt))) {
  const m = /'s answer: (.+?)\s*$/m.exec(q.prompt);
  if (m) assert.notEqual(m[1].trim().replace(/\.$/, ''), String(q.answer).trim(), q.id + ' shows the key as the mistake');
}
const byId = Object.fromEntries(all.map((q) => [q.id, q]));
assert.equal(byId['m6-exq-s03-cp2-016'].prompt.includes("Quinn's answer: 152"), true);
assert.equal(byId['m6-fdo-s02-cp1-004'].answer, '26', 'trail mix: full bags');

// #9 and #10 tags
const tags = (sk) => new Set(all.filter((q) => q.skillId === sk).flatMap((q) => q.standards));
assert(!all.some((q) => q.standards.includes('7.RP.A.2c')), 'no 7.RP.A.2c on Grade 6 proportion items');
assert(!all.some((q) => q.standards.includes('7.SP.B.3')), 'no 7.SP.B.3 on Grade 6 comparison items');
for (const s of ['6.EE.A.2a', '6.EE.A.2b', '6.EE.A.2c']) assert(tags('expressions-equations-skill-02').has(s), s);
assert(!tags('expressions-equations-skill-02').has('6.EE.A.2'), 'parent tag replaced by sub-standards');
assert(all.filter((q) => q.skillId === 'inequalities-skill-02' && !/-(g|h)\d{2}$/.test(q.id)).every((q) => q.standards.includes('7.EE.B.4b')), 'solving inequalities marked 7.EE.B.4b');

// #20 text
const T = all.map(text).join('\n');
assert(!/years old to vote/.test(T), 'voting ages');
for (const m of T.matchAll(/car travels (\d+) miles in (\d+) hours/g)) assert(+m[1] / +m[2] >= 25, m[0]);
for (const m of T.matchAll(/car (?:uses (\d+) gallons of gas to go (\d+) miles|travels (\d+) miles on (\d+) gallons)/g)) { const mpg = m[1] ? +m[2] / +m[1] : +m[3] / +m[4]; assert(mpg >= 15, m[0]); }
for (const m of T.matchAll(/covers (\d+) miles in (\d+) hours/g)) assert(+m[1] / +m[2] <= 80, m[0]);
for (const m of T.matchAll(/(\d+)-pack of juice boxes costs \$([\d.]*\d)/g)) assert(+m[2] / +m[1] <= 2, m[0]);
assert(!/shirts that cost \$[1-4] each/.test(T), 'cheap shirts');

// #15 vocabulary
const w = {}; w.window = w; vm.createContext(w); vm.runInContext(rd('worksheet-generator/vocabulary-data-middle-grades.js'), w);
const V = w.MKVOCAB_BANKS, terms = (u) => V['math6-' + u].split(';').map((e) => e.split('|')[0].trim().toLowerCase());
for (const [u, t] of [['ratios-rates-percent-proportions', 'double number line'], ['fractions-decimals-operations', 'dividend'], ['rational-numbers', 'opposite'],
  ['expressions-equations', 'evaluate'], ['geometry', 'prism'], ['data-displays', 'measure of variability'], ['data-displays', 'quartile']]) assert(terms(u).includes(t), u + ': ' + t);
const n = Object.keys(V).filter((k) => k.startsWith('math6-')).reduce((a, k) => a + terms(k.slice(6)).length, 0);
assert(n >= 100, n + ' Grade 6 terms');

// 6B: #4 levels, #5-#9 new content, #17 figures, #18 constructed response
const H = all.filter((q) => /-honors-h\d{2}$/.test(q.id)), G = all.filter((q) => /-g\d{2}$/.test(q.id));
const skills = [...new Set(all.map((q) => q.skillId))];
assert.equal(skills.length, 53, 'skills');
for (const sk of skills) assert.equal(H.filter((q) => q.skillId === sk).length, 2, sk + ' has two Honors multi-step items');
assert(all.filter((q) => q.level === 'cp2' && (q.hint || '').startsWith('First step:')).length >= 600, 'CP2 first-step hints');
const has = (s) => G.filter((q) => q.standards.includes(s)).length;
for (const [s, n] of [['6.RP.A.3c', 9], ['6.EE.C.9', 8], ['6.RP.A.3a', 12], ['6.NS.A.1', 7], ['6.SP.B.5a', 3], ['6.SP.B.5b', 3], ['6.SP.A.3', 3], ['6.EE.B.6', 6], ['6.EE.A.2b', 3], ['6.G.A.4', 8], ['6.G.A.3', 6]])
  assert(has(s) >= n, `${s}: ${has(s)} new items`);
for (const q of G.filter((q) => q.diagram)) {
  assert(fs.existsSync(path.join(ROOT, q.diagram.spec.src)), q.id + ' figure file');
  assert(q.diagram.spec.alt.length > 30, q.id + ' alt text');
}
assert(G.filter((q) => q.diagram).length >= 35, 'new figures');
const CRs = G.filter((q) => q.format === 'open-response' && (q.parts || []).length === 4);
assert.equal(CRs.length, 14, 'two four-part constructed-response tasks per unit');
for (const u of ['rrp', 'fdo', 'rat', 'exq', 'ineq', 'geo', 'dd']) for (const lv of ['cp1', 'honors'])
  assert(CRs.some((q) => q.id.startsWith(`m6-${u}-`) && q.level === lv), `${u} ${lv} constructed response`);
for (const q of G) if (q.format === 'short-answer') assert.equal(g(q.answer, q.answer, q.prompt), 'correct', q.id + ' new key grades itself correct');

console.log(`PASS Grade 6 audit 6B: ${H.length} Honors multi-step items, ${G.length} new items (${CRs.length} constructed response)`);
console.log(`PASS Grade 6 audit 6A: ${cases.length} grading cases, ${auto}/${sa} short answers auto-graded; error analysis, tags, text, ${n} vocabulary terms`);
