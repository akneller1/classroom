#!/usr/bin/env node
// Grade 7 audit (2026-11-19), batch G1: #1 practice-test grading of mixed numbers, inequalities and repeating decimals,
// #11 standards tags that match the items, #12 Place Value at grade level, #19 vocabulary, #20 text clean-up.
// (#2, the key checker, runs as python3 tools/grade7-audit-20261119/verify_keys.py.)
'use strict';
const fs = require('fs'), vm = require('vm'), path = require('path'), assert = require('assert/strict');
const ROOT = path.resolve(__dirname, '..'), rd = f => fs.readFileSync(path.join(ROOT, f), 'utf8');
const bank = course => fs.readdirSync(path.join(ROOT, 'question-banks', course)).filter(f => f.endsWith('.json'))
  .flatMap(f => JSON.parse(rd(`question-banks/${course}/${f}`)).questions || []);
const all = bank('prealgebra7');
const text = q => [q.prompt, typeof q.answer === 'string' ? q.answer : JSON.stringify(q.answer), ...(q.solutionSteps || []),
  ...(q.options || []).map(o => o.text), ...(q.parts || []).flatMap(p => [p.prompt, p.answer])].join(' ');

// #1 grading
const c = {}; c.window = c; vm.createContext(c);
for (const f of ['menu/mathcheck.js', 'practice/radical-grading.js', 'practice/exact-grading.js', 'practice/calculus-grading.js', 'practice/stat-grading.js', 'practice/grading.js'])
  vm.runInContext(rd('worksheet-generator/' + f), c, { filename: f });
const P = c.MKPRACTICE, g = (a, t, p) => P.gradeBank(a, t, p || '').status;
const cases = [
  ['1 1/4', '5/4', 'correct'], ['1 1/4', '1.25', 'correct'], ['1 1/4', '1 1/4', 'correct'], ['1 1/4', '1/4', 'incorrect'], ['1 1/4', '0.25', 'incorrect'],
  ['-8 2/3', '-26/3', 'correct'], ['-8 2/3', '-16/3', 'incorrect'], ['5 1/2 in.', '5.5', 'correct'], ['5 1/2 in.', '11/2', 'correct'],
  ['w = 3 1/4', 'w = 13/4', 'correct'], ['w = 3 1/4', 'w = 3/4', 'incorrect'], ['10 4/15', '154/15', 'correct'], ['10 4/15', '40/15', 'incorrect'],
  ['x > -2', 'x>-2', 'correct'], ['x > -2', '-2<x', 'correct'], ['x > -2', 'x>=-2', 'incorrect'], ['x > -2', 'x<-2', 'incorrect'],
  ['m ≥ 23', 'm>=23', 'correct'], ['m ≥ 23', 'm>23', 'incorrect'], ['m ≥ 23', 'x>=23', 'incorrect'], ['k > 19', '19<k', 'correct'],
  ['0.8333… (3 repeats)', '5/6', 'correct'], ['0.8333… (3 repeats)', '0.8(3)', 'correct'], ['0.8333… (3 repeats)', '0.83̅', 'correct'],
  ['0.8333… (3 repeats)', '0.8333...', 'correct'], ['0.8333… (3 repeats)', '4/5', 'incorrect'], ['0.8333… (3 repeats)', '0.83', 'invalid'],
  ['0.7272… (72 repeats)', '8/11', 'correct'], ['0.7272… (72 repeats)', '0.(27)', 'incorrect'], ['1.583333… (3 repeats)', '19/12', 'correct'],
  ['3/4', '0.75', 'correct'], ['(3, -1)', '(3,-1)', 'correct'], ['$76.00', '76', 'correct']];
for (const [a, t, want] of cases) assert.equal(g(a, t), want, `${a} ← ${t}`);
assert.equal(g('2 1/3', '7/3', 'Write 7/3 as a mixed number.'), 'invalid', 'a mixed number is required when the question asks for one');
assert.equal(g('2 1/3', '2 1/3', 'Write 7/3 as a mixed number.'), 'correct');
const sa = all.filter(q => q.format === 'short-answer' && typeof q.answer === 'string');
let auto = 0;
for (const q of sa) if (P.bankAnswer(q.answer) !== null) { auto++; assert.equal(g(q.answer, q.answer, q.prompt), 'correct', q.id + ' key grades itself correct: ' + q.answer); }
assert(auto / sa.length >= 0.93, 'auto-graded share ' + (auto / sa.length).toFixed(3));
for (const q of sa.filter(q => /(^|[\s=(])-?\d+ \d+\/\d+/.test(q.answer) && P.bankAnswer(q.answer) !== null)) {
  const m = /(-?)(\d+) (\d+)\/(\d+)/.exec(q.answer), improper = `${m[1]}${+m[2] * +m[4] + +m[3]}/${m[4]}`, times = `${m[1]}${+m[2] * +m[3]}/${m[4]}`;
  const typed = q.answer.replace(m[0], improper);
  if (!/mixed number/i.test(q.prompt)) assert.equal(g(q.answer, typed, q.prompt), 'correct', q.id + ' improper form of ' + q.answer);
  if (times !== improper) assert.notEqual(g(q.answer, q.answer.replace(m[0], times), q.prompt), 'correct', q.id + ' whole × fraction is not the mixed number');
}
for (const course of ['math6', 'prealgebra']) for (const q of bank(course)) {
  if (q.format !== 'short-answer' || typeof q.answer !== 'string' || P.bankAnswer(q.answer) === null || /^\d*√/.test(q.answer)) continue;
  assert.equal(g(q.answer, q.answer, q.prompt), 'correct', q.id + ' key grades itself correct: ' + q.answer);
}
assert.match(rd('worksheet-generator/practice-test.html'), /practice\/grading\.js\?v=g7-audit-20261119/);

// #20 text
for (const q of all) {
  const t = text(q);
  assert(!/(?<![\d/.,-])1 (units|feet|inches|blocks|meters)\b/.test(t), q.id + ' singular unit after 1');
  assert(!t.includes('−'), q.id + ' uses "-" for negatives like the rest of the bank');
  assert(!/\b(Omar|Ben|Sam|Jamal|Yusuf|Dev|Kai|Leo|Hiro) is \d+ times as old as her\b/.test(q.prompt), q.id + ' pronoun');
  assert(!/on a number cube and (a|an) [\w ]+ on a number cube/.test(q.prompt), q.id + ' names two number cubes');
  if (q.skillId === 'area-volume-skill-02') assert(!/parallelogram/i.test(q.prompt), q.id + ' is in Triangles and Trapezoids');
}

// #12 Place Value
const pv = all.filter(q => q.skillId === 'algebraic-expressions-integers-skill-01');
assert.equal(pv.length, 48);
assert(!pv.some(q => /standard form: (one|two|three|four|five|six|seven|eight|nine)\b/i.test(q.prompt)), 'no whole-number word forms');
assert(pv.filter(q => q.standards.some(s => /^[678]\./.test(s))).length >= 30, 'Place Value items carry grade 6–8 standards');
for (const lv of ['cp1', 'honors']) assert(pv.filter(q => q.level === lv && q.standards.some(s => /^8\.EE\.A/.test(s))).length >= 14, lv + ' Place Value is about powers of ten');
assert(pv.filter(q => q.level === 'honors' && /× 10[⁻⁰-⁹¹²³]/.test(q.prompt)).length >= 6, 'Honors compares with powers of ten');

// #11 tags
const by = id => all.filter(q => q.skillId === id);
assert(!by('spatial-thinking-skill-07').some(q => q.standards.includes('7.G.A.2') && !/triangle/i.test(text(q))), '7.G.A.2 only on triangle items');
assert(!by('area-volume-skill-04').some(q => q.standards.includes('7.G.A.3') && !/cross.section|slice/i.test(text(q))), '7.G.A.3 only on cross-sections');
for (const q of by('spatial-thinking-skill-02')) if (/transversal|parallel/i.test(q.prompt)) assert(q.standards.includes('8.G.A.5') && !q.standards.includes('7.G.B.5'), q.id);
for (const q of by('data-analysis-probability-skill-08')) if (/sampling method/i.test(q.prompt)) assert.deepEqual(q.standards, ['7.SP.A.1'], q.id);
assert(by('solving-equations-inequalities-skill-05').some(q => q.standards.includes('8.EE.C.7a')), '8.EE.C.7a tagged');
const ctx = { window: {} }; ctx.globalThis = ctx;
vm.runInNewContext(rd('worksheet-generator/menu/standards.js') + '\n' + rd('worksheet-generator/menu/standards-map.js'), ctx);
for (const q of all) for (const s of q.standards) assert(ctx.window.MKSTD.describe(s), 'description for ' + s);

// #19 vocabulary
const v = { window: {} }; v.window = v; vm.createContext(v);
for (const f of ['vocabulary-data.js', 'vocabulary-data-middle-grades.js']) vm.runInContext(rd('worksheet-generator/' + f), v);
const terms = Object.keys(v.MKVOCAB_BANKS).filter(k => k.startsWith('prealgebra7-')).flatMap(k => v.MKVOCAB_BANKS[k].split(';').filter(Boolean).map(r => r.split('|')));
for (const r of terms) assert(r.length >= 3 && r.length <= 4 && r[1].trim(), 'vocabulary row ' + r[0]);
for (const t of ['constant of proportionality', 'proportional relationship', 'scale factor', 'scale drawing', 'cross-section', 'simulation', 'compound event',
  'population', 'inference', 'additive inverse', 'percent error', 'dilation'])
  assert(terms.some(r => r[0].trim().toLowerCase() === t), 'vocabulary: ' + t);

console.log(`PASS Grade 7 audit G1: ${cases.length} grading cases, ${auto}/${sa.length} short answers auto-graded; text clean-up; Place Value at grade level; standards tags; ${terms.length} vocabulary terms`);
