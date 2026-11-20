#!/usr/bin/env node
/* Whole-site audit (2026-11-20) checks. Run: node scripts/test-site-audit.cjs [_site]
   Repository checks always run; checks of the built site run when the folder is given and present. */
const fs = require('fs'), vm = require('vm'), path = require('path'), assert = require('assert');
const ROOT = path.join(__dirname, '..'), SITE = process.argv[2] ? path.resolve(process.argv[2]) : null;
const rd = (p) => fs.readFileSync(path.join(ROOT, p), 'utf8');
let checks = 0; const ok = (c, m) => { assert(c, m); checks++; };

/* #1-#4, #11: the practice-test grader */
const ctx = { console }; ctx.window = ctx; vm.createContext(ctx);
for (const f of ['core/frac.js', 'menu/mathcheck.js', 'practice/radical-grading.js', 'practice/exact-grading.js', 'practice/discrete-grading.js',
  'practice/calculus-grading.js', 'practice/stat-grading.js', 'practice/grade8-grading.js', 'practice/grading.js'])
  vm.runInContext(rd('worksheet-generator/' + f), ctx, { filename: f });
const P = ctx.MKPRACTICE;
const g = (course, key, typed, prompt = '') => { ctx.MK_PRACTICE_COURSE = course; return P.gradeBank(key, typed, prompt).status; };
const cases = [
  ['math6', '38 ft²', '38 ft^2', 'correct'], ['math6', '38 ft²', '38 ft2', 'correct'], ['prealgebra', '4y²', '4y^2', 'correct'], ['prealgebra', '4y²', '4y^3', 'incorrect'],
  ['statistics', '(280.07, 363.93)', '(280.07,363.93)', 'correct'], ['statistics', '(280.07, 363.93)', '(363.93,280.07)', 'incorrect'], ['grade5', '(45, 135)', '(45,135)', 'correct'],
  ['grade2', '$1.25', '125¢', 'correct'], ['grade2', '$1.25', '1 dollar 25 cents', 'correct'], ['grade2', '$1.25', '$1.52', 'incorrect'], ['grade2', '45¢', '$0.45', 'correct'], ['grade2', '45¢', '$4.50', 'incorrect'],
  ['grade1', '3 tens and 8 ones', '3 8', 'correct'], ['grade1', '3 tens and 8 ones', '38', 'correct'], ['grade1', '3 tens and 8 ones', '83', 'incorrect'],
  ['grade1', "5 o'clock", '5:00', 'correct'], ['grade1', 'half past 3', '3:30', 'correct'], ['grade1', "5 o'clock", '6:00', 'incorrect'],
  ['grade3', '4:30 p.m.', '4:30 pm', 'correct'], ['grade3', '4:30 p.m.', '4:30 am', 'incorrect'], ['grade2', 'greater', '>', 'correct'], ['grade2', 'greater', '<', 'incorrect'],
  ['grade4', '3/4', 'three fourths', 'correct'], ['grade4', '3/4', 'one fourth', 'incorrect'], ['grade1', '12', 'twelve', 'correct'], ['grade1', '12', 'eleven', 'incorrect']];
for (const [c, k, t, want] of cases) ok(g(c, k, t) === want, `${c}: ${k} / ${t} should be ${want}, got ${g(c, k, t)}`);
ok(P.sameAsKey('x² + 12x + 32', 'my work\nx^2+12x+32') && !P.sameAsKey('x² + 12x + 32', 'x^2+12x+31') && P.sameAsKey('ax + b', 'ax+b') && P.sameAsKey('7.5 × 10⁷', '7.5 x 10^7'), 'exact final answer on a self-scored item');
// every bank key still grades itself correct, in every course
let keys = 0;
for (const course of fs.readdirSync(path.join(ROOT, 'question-banks'))) {
  const dir = path.join(ROOT, 'question-banks', course);
  if (!fs.statSync(dir).isDirectory() || course === 'assets') continue;
  ctx.MK_PRACTICE_COURSE = course;
  for (const f of fs.readdirSync(dir).filter((x) => x.endsWith('.json'))) for (const q of JSON.parse(fs.readFileSync(path.join(dir, f))).questions) {
    if (q.format !== 'short-answer' || typeof q.answer !== 'string' || P.bankAnswer(q.answer, q.prompt) === null) continue;
    ok(P.gradeBank(q.answer, q.answer, q.prompt).status === 'correct', `${q.id}: key grades itself correct`); keys++;
  }
}
const prac = rd('worksheet-generator/practice/practice.js');
ok(/function autoSelfCheck\(q\)/.test(prac) && /selfCheck:Array\.isArray\(q\.selfCheck\)\?q\.selfCheck:autoSelfCheck\(q\)/.test(prac), '#5 self-check list for every written answer');
ok(/seenSig\['t:'\+tsig\]/.test(prac) && /sameAsKey\(q\.problem\.parts\[0\]\.answer,q\.response\)\)q\.correct=true/.test(prac), '#4 and #6 in practice.js');
ok(/practice\/grading\.js\?v=g5-audit-20261119-site-audit/.test(rd('worksheet-generator/practice-test.html')), 'grader cache version');

/* #7, #8: printable generators and the Vocabulary Builder listed in every unit */
const w = {}; w.window = w; vm.createContext(w); vm.runInContext(rd('data.js'), w);
const course = (id) => w.LIBRARY.courses.find((c) => c.id === id);
for (const id of ['algebra', 'geometry', 'algebra2']) for (const u of course(id).units)
  ok(u.artifacts.some((a) => /kind=vocabulary/.test(a.path)), `${id}/${u.id}: Vocabulary Builder`);
for (const u of course('algebra2').units) for (const k of [/error analysis/i, /tarsia/i, /\bmaze\b/i, /color by number/i, /whodunnit|\(printable\)/i])
  ok(u.artifacts.some((a) => k.test(a.title)), `algebra2/${u.id}: ${k}`);

/* #10 select-all counts in Grades 6 and 7 */
for (const c of ['math6', 'prealgebra7']) {
  const n = {};
  for (const f of fs.readdirSync(path.join(ROOT, 'question-banks', c)).filter((x) => x.endsWith('.json')))
    for (const q of JSON.parse(rd(`question-banks/${c}/${f}`)).questions) if (q.format === 'select-all' && /matched with the correct answer/.test(q.prompt)) {
      const k = q.options.filter((o) => o.correct).length; n[k] = (n[k] || 0) + 1;
      ok(JSON.stringify(q.answer) === JSON.stringify(q.options.filter((o) => o.correct).map((o) => o.text)) && k >= 2 && k < q.options.length, q.id + ': answer list');
    }
  ok(n[2] >= 15 && n[3] >= 15 && n[4] >= 15, `${c}: select-all counts vary ${JSON.stringify(n)}`);
}

/* #12, #13: text, thumbnails, legacy pages */
const all = fs.readdirSync(path.join(ROOT, 'question-banks')).filter((c) => fs.statSync(path.join(ROOT, 'question-banks', c)).isDirectory())
  .flatMap((c) => fs.readdirSync(path.join(ROOT, 'question-banks', c)).filter((f) => f.endsWith('.json')).map((f) => rd(`question-banks/${c}/${f}`))).join('\n');
ok(!/(?<![\d.])\b1 (?:feet|inches|apples|cups|years)\b/.test(all.replace(/[-+=−×] 1 /g, '')) && !/\bthe the\b/.test(all), 'plural after 1 and doubled words');
for (const t of ['budgeting', 'borrowing', 'investing']) ok(fs.existsSync(path.join(ROOT, `thumbs/financial-algebra/${t}-spreadsheet.svg`)), t + ' spreadsheet thumbnail');
ok(/Site audit #12[\s\S]*http-equiv="refresh"/.test(rd('scripts/build-site.mjs')), 'legacy course pages redirect to /u/');

if (SITE && fs.existsSync(SITE)) {
  const n = {};
  for (const f of fs.readdirSync(path.join(SITE, 'question-banks/grade5')).filter((x) => x.endsWith('.json')))
    for (const q of JSON.parse(fs.readFileSync(path.join(SITE, 'question-banks/grade5', f))).questions)
      if (q.format === 'select-all') { const k = q.options.filter((o) => o.correct).length; n[k] = (n[k] || 0) + 1; }
  ok(n[2] >= 50 && n[3] >= 50, 'Grade 5 select-all counts vary ' + JSON.stringify(n));
  const legacy = path.join(SITE, 'courses/precalculus.html');
  if (fs.existsSync(legacy)) ok(/http-equiv="refresh" content="0; url=https:\/\/mrksclassroom\.com\/u\/precalculus\/"/.test(fs.readFileSync(legacy, 'utf8')), 'Precalculus legacy page redirects');
}
console.log(`PASS site audit: ${checks} checks (${keys} bank keys grade themselves correct)`);
