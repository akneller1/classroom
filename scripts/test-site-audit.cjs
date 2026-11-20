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
  ['math6', '38 ft²', '38 ft³', 'incorrect'], ['math6', '38 ft²', '38 sq ft', 'correct'], ['math6', '5 m', '5 cm', 'incorrect'], ['math6', '12 inches', '12 in.', 'correct'],
  ['prealgebra7', '22t', '22', 'incorrect'], ['prealgebra7', '22t', '22 t', 'correct'], ['calculus', '-60x²', '-60x^3', 'incorrect'], ['precalculus', '8i', '8', 'incorrect'],
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

/* #12, #13: text, thumbnails, legacy pages */
for (const t of ['budgeting', 'borrowing', 'investing']) ok(fs.existsSync(path.join(ROOT, `thumbs/financial-algebra/${t}-spreadsheet.svg`)), t + ' spreadsheet thumbnail');
ok(/Site audit #12[\s\S]*http-equiv="refresh"/.test(rd('scripts/build-site.mjs')), 'legacy course pages redirect to /u/');

/* game labels and student links: a cache tag in the URL is not the game */
const gw = { location: { href: 'https://mrksclassroom.com/' }, URL }; gw.window = gw; vm.createContext(gw); vm.runInContext(rd('game-capabilities.js'), gw);
const cap = (p, t, ty) => JSON.stringify(gw.MK_GAME_CAPABILITIES.get({ path: p, title: t, type: ty }));
ok(cap('worksheet-generator/course-game.html?course=algebra2&unit=x&game=flashcards&v=showdown-fix-20261031', 'X Flashcards', 'Study Guide') === '{"solo":true,"team":false}', 'flashcards are solo');
ok(cap('worksheet-generator/course-game.html?course=algebra2&unit=x&game=connect4&v=showdown-fix-20261031', 'X Connect 4', 'Game') === '{"solo":true,"team":true}', 'Connect 4 is solo or team');
ok(cap('worksheet-generator/course-game.html?course=algebra2&unit=x&game=showdown', 'X Showdown', 'Game') === '{"solo":false,"team":true}', 'Showdown stays team');
/* UX: pacing shortcuts, tolerant links */
const app = rd('app.js');
ok(/function isPrintable\(a\)/.test(app) && /category\('printables', 'Printables', isPrintable\)/.test(app) && /data-report-choices/.test(app) && !/Report a problem<span class="sr">/.test(app) && /function pageHits/.test(app), 'printables section, one report link per page, page search');
ok(/var PACING_PAGES = \{/.test(app) && /pacingShortcut\(c, compact\)/.test(app) && /COURSE_ALIASES/.test(app) && /short: 'Mazes & Puzzles'/.test(app), 'app.js UX changes');
for (const pg of ['grade-1-pacing', 'grade-6-pacing', 'algebra-1-pacing', 'calculus-pacing']) ok(new RegExp("'" + pg + "/'").test(app), pg + ' in the pacing map');

if (SITE && fs.existsSync(SITE)) {
  const n = {};
  for (const f of fs.readdirSync(path.join(SITE, 'question-banks/grade5')).filter((x) => x.endsWith('.json')))
    for (const q of JSON.parse(fs.readFileSync(path.join(SITE, 'question-banks/grade5', f))).questions)
      if (q.format === 'select-all') { const k = q.options.filter((o) => o.correct).length; n[k] = (n[k] || 0) + 1; }
  ok(n[2] >= 50 && n[3] >= 50, 'Grade 5 select-all counts vary ' + JSON.stringify(n));
  /* #10 select-all counts in Grades 6 and 7 */
  for (const c of ['math6', 'prealgebra7']) {
    const n = {};
    for (const f of fs.readdirSync(path.join(SITE, 'question-banks', c)).filter((x) => x.endsWith('.json')))
      for (const q of JSON.parse(fs.readFileSync(path.join(SITE, 'question-banks', c, f), 'utf8')).questions) if (q.format === 'select-all' && /matched with the correct answer/.test(q.prompt)) {
        const k = q.options.filter((o) => o.correct).length; n[k] = (n[k] || 0) + 1;
        ok(JSON.stringify(q.answer) === JSON.stringify(q.options.filter((o) => o.correct).map((o) => o.text)) && k >= 2 && k < q.options.length, q.id + ': answer list');
      }
    ok(n[2] >= 15 && n[3] >= 15 && n[4] >= 15, `${c}: select-all counts vary ${JSON.stringify(n)}`);
  }
  
  const all = fs.readdirSync(path.join(SITE, 'question-banks')).filter((c) => !/^grade[1-4]$/.test(c) && fs.statSync(path.join(SITE, 'question-banks', c)).isDirectory())
    .flatMap((c) => fs.readdirSync(path.join(SITE, 'question-banks', c)).filter((f) => f.endsWith('.json')).map((f) => fs.readFileSync(path.join(SITE, 'question-banks', c, f), 'utf8'))).join('\n');
  ok(!/(?<![\d.])\b1 (?:feet|inches|apples|cups|years)\b/.test(all.replace(/[-+=−×] 1 /g, '')) && !/\bthe the\b/.test(all), 'plural after 1 and doubled words');
  
  /* #20 picture descriptions no longer state the answer */
  let giveaways = 0;
  for (const c of fs.readdirSync(path.join(SITE, 'question-banks'))) {
    const dir = path.join(SITE, 'question-banks', c); if (!fs.statSync(dir).isDirectory()) continue;
    for (const f of fs.readdirSync(dir).filter((x) => x.endsWith('.json'))) for (const q of JSON.parse(fs.readFileSync(path.join(dir, f), 'utf8')).questions || []) {
      const alt = (q.diagram && q.diagram.spec && q.diagram.spec.alt) || '', a = typeof q.answer === 'string' ? q.answer.trim().toLowerCase().replace(/\.$/, '') : '';
      if (!alt || a.length < 2) continue;
      if (/\bname\b|what shape is this|which name matches|which equation matches the graph|solution of the system|solution to the system/i.test(q.prompt) && alt.toLowerCase().replace(/square (corners|faces)|rectangle faces/g, '').includes(a)) { giveaways++; if (giveaways < 4) console.log('  alt still gives the answer:', q.id, alt.slice(0, 80)); }
      if (/(which shape|is the shape) (is )?cut into (halves|fourths)/i.test(q.prompt) && /(un)?equal parts/.test(alt)) giveaways++;
    }
  }
  ok(giveaways === 0, giveaways + ' picture descriptions still state the answer');
  const si = path.join(SITE, 'standards-index.js');
  if (fs.existsSync(si)) {
    const sw = {}; sw.window = sw; vm.createContext(sw); vm.runInContext(fs.readFileSync(si, 'utf8'), sw); const SI = sw.MK_STANDARDS_INDEX;
    const bands = new Set(Object.values(SI.std).flat().map((x) => x[0].split('.')[0]));
    ok(['grade1', 'grade3', 'grade5', 'math6', 'prealgebra', 'algebra', 'geometry', 'calculus', 'statistics'].every((c) => bands.has(c)), 'standards index covers Grades 1-12');
    ok(SI.std['8.G.B.7'] && SI.std['8.G.B.7'].length >= 3 && Object.keys(SI.desc).length === Object.keys(SI.std).length, 'standards index: 8.G.B.7 and a description for every standard');
  }
  const g5p = path.join(SITE, 'grade-5-pacing/index.html');
  ok(fs.existsSync(g5p) && /34 of 34 standards have question-bank practice/.test(fs.readFileSync(g5p, 'utf8')) && /5th Grade Math Pacing Guide/.test(fs.readFileSync(g5p, 'utf8')), 'Grade 5 pacing page');
  const legacy = path.join(SITE, 'courses/precalculus.html');
  if (fs.existsSync(legacy)) ok(/http-equiv="refresh" content="0; url=https:\/\/mrksclassroom\.com\/u\/precalculus\/"/.test(fs.readFileSync(legacy, 'utf8')), 'Precalculus legacy page redirects');
}
// #19 worked solutions: every Financial Algebra item (repo export and pinned copies) has more than one step
if (SITE) for (const d of ['financial/banks', 'financial-algebra/financial/banks', 'financial-algebra/question-banks/financial-algebra', 'question-banks/financial-algebra'].map((x) => path.join(SITE, x)).filter((x) => fs.existsSync(x))) {
  for (const f of fs.readdirSync(d).filter((f) => f.endsWith('.json') && f !== 'index.json')) {
    const qs = JSON.parse(fs.readFileSync(path.join(d, f), 'utf8')).questions || [];
    ok(qs.every((q) => (q.solutionSteps || []).length > 1), 'Financial Algebra worked steps in ' + path.relative(SITE, d) + '/' + f);
  }
}
for (const c of ['financial-algebra', 'statistics']) for (const f of fs.readdirSync(path.join(ROOT, 'question-banks', c)).filter((f) => f.endsWith('.json'))) {
  const qs = JSON.parse(fs.readFileSync(path.join(ROOT, 'question-banks', c, f), 'utf8')).questions || [];
  ok(qs.every((q) => (q.solutionSteps || []).length > 1), 'worked steps in question-banks/' + c + '/' + f);
}
console.log(`PASS site audit: ${checks} checks (${keys} bank keys grade themselves correct)`);
