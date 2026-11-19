#!/usr/bin/env node
// Statistics audit S3 (2026-11-18): #4 teaching notes are wired into the Lesson Planner, #5 the pacing guide,
// #15 the Normal Curve and Chi-Square labs, #16 two AP Statistics practice exams, #17 Tables A–C and the formula sheet,
// and (follow-up to #1) the rule line that starts each expanded worked solution fits what the item asks.
'use strict';
const fs = require('fs'), vm = require('vm'), path = require('path'), assert = require('assert/strict');
const root = path.resolve(__dirname, '..'), rd = f => fs.readFileSync(path.join(root, f), 'utf8');
const ctx = { window: {} };
for (const file of ['data.js', 'student-game-share.js']) vm.runInNewContext(rd(file), ctx, { filename: file });
const courses = ctx.window.LIBRARY.courses, stat = courses.find(c => c.id === 'statistics');
const unit = id => stat.units.find(u => u.id === id);
const exists = f => fs.existsSync(path.join(root, f.split('?')[0])) && fs.statSync(path.join(root, f.split('?')[0])).size > 2000;

// Bank items by id
const items = {};
for (const f of fs.readdirSync(path.join(root, 'question-banks/statistics')).filter(f => f.endsWith('.json'))) {
  (function walk(o) {
    if (Array.isArray(o)) o.forEach(walk);
    else if (o && typeof o === 'object') { if (o.id && o.prompt) items[o.id] = o; Object.values(o).forEach(walk); }
  })(JSON.parse(rd('question-banks/statistics/' + f)));
}

// #4 teaching notes in the Lesson Planner
assert(rd('worksheet-generator/lesson-planner.html').includes('planner/notes-teach-statistics.js'), 'planner loads the Statistics notes');
assert.match(rd('worksheet-generator/planner/notes-teach.js'), /course\(\) === 'statistics'/);

// #5 pacing guide
assert.match(rd('scripts/geo-planning.mjs'), /statistics: \{ name: "Statistics", load: \(\) => bankScope\("statistics", "ST", \{ ap: true, noReviewUnit: true/);
assert.match(rd('scripts/test-public-site.cjs'), /'statistics-pacing\/'/);

// #15 labs
const M = JSON.parse(rd('tools/statistics-audit-20261118/labs/manifest.json'));
assert.equal(M.tools.length, 2);
for (const t of M.tools) {
  for (const [c, u] of [[t.course, t.unit], ...(t.also || []).map(x => x.length === 1 ? [t.course, x[0]] : x)]) {
    const a = courses.find(x => x.id === c).units.find(x => x.id === u).artifacts.find(a => a.path === `artifacts/${t.slug}/index.html`);
    assert(a && a.bankFormat === 'interactive-math' && a.type === 'Interactive', 'placement ' + t.slug + ' in ' + u);
    for (const f of [a.path, a.worksheet, a.answerKey, a.thumb]) assert(f && exists(f), 'resource ' + f);
    assert.equal(ctx.window.TeacherGameShare.supports(a.path), false, 'a lab must not open a game skill picker');
  }
  const html = rd(`artifacts/${t.slug}/index.html`), src = rd(`tools/statistics-audit-20261118/labs/src/${t.slug}.js`);
  for (const r of ['../interactive-math/lab.js', '../interactive-math/lab-plus.js', '../interactive-math/lab.css']) assert(html.includes(r), 'runtime ' + r);
  assert(html.includes(src.trim().split('\n').slice(-3).join('\n')), 'page built from the current source: ' + t.slug);
  new vm.Script(src, { filename: t.slug + '.js' });
  assert.equal((src.match(/check: function/g) || []).length, 5, 'five challenges ' + t.slug);
}
assert(unit('statistical-inference').artifacts.some(a => a.path.includes('chi-square-lab')), 'chi-square lab in Statistical Inference');
assert(unit('exploring-data').artifacts.some(a => a.path.includes('normal-curve-lab')), 'Normal lab in Exploring Data');

// #16 practice exams
const strip = s => s.replace(/<[^>]+>/g, '').replace(/&amp;/g, '&').replace(/&lt;/g, '<').replace(/&gt;/g, '>').trim();
const mcOf = h => [...h.matchAll(/<li value="(\d+)"><div class="q">([\s\S]*?)<\/div>(?:<img[^>]*>)?<div class="choices">((?:<div><b>\([A-D]\)<\/b>[\s\S]*?<\/div>){4})<\/div>(?:<div class="ans">Answer: \(([A-D])\) ([\s\S]*?)<\/div>)?/g)]
  .map(m => ({ n: +m[1], q: strip(m[2]), opts: [...m[3].matchAll(/<b>\([A-D]\)<\/b>([\s\S]*?)<\/div>/g)].map(o => strip(o[1])), letter: m[4], ans: m[5] && strip(m[5]) }));
const sel = JSON.parse(rd('tools/statistics-audit-20261118/exams.json')), seen = {};
for (const ex of ['a', 'b']) {
  const dir = `artifacts/statistics-ap-practice-exam-${ex}/`, exam = rd(dir + 'exam.html'), key = rd(dir + 'key.html');
  const E = mcOf(exam), K = mcOf(key);
  assert.deepEqual(E.map(q => q.n), Array.from({ length: 42 }, (_, i) => i + 1), ex + ' numbering 1–42');
  assert.deepEqual(E.map(q => q.q + q.opts.join('|')), K.map(q => q.q + q.opts.join('|')), ex + ' key matches the exam');
  for (const q of K) {
    assert.equal(new Set(q.opts).size, 4, ex + q.n + ' four distinct options');
    assert.equal(q.opts['ABCD'.indexOf(q.letter)], q.ans, ex + q.n + ' keyed letter is the answer');
  }
  const pos = {}; K.forEach(q => { pos[q.letter] = (pos[q.letter] || 0) + 1; });
  assert(Object.values(pos).length === 4 && Object.values(pos).every(v => v >= 5), ex + ' answer positions ' + JSON.stringify(pos));
  const frq = [...key.matchAll(/<h3>Question (\d) · ([^<]*)<\/h3>/g)];
  assert.deepEqual(frq.map(m => +m[1]), [1, 2, 3, 4], ex + ' four free-response problems');
  assert.match(frq[2][2], /Inference/, ex + ' Question 3 is a complete inference problem');
  assert((key.match(/Scoring, \d+ points?:/g) || []).length >= 12, ex + ' scoring notes for the parts');
  assert.equal((exam.match(/Scoring|class="ans"/g) || []).length, 0, ex + ' student copy has no answers');
  assert.match(exam, /Section I · Multiple choice · 90 minutes/); assert.match(exam, /Section II · Free response · 90 minutes/);
  assert.match(exam, /Table A/); assert.match(key, /composite = /);
  for (const m of exam.matchAll(/src="\.\.\/\.\.\/([^"]+)"/g)) assert(exists(m[1]), 'image or script ' + m[1]);
  for (const f of ['exam.pdf', 'teacher-key.pdf']) assert(fs.statSync(path.join(root, dir, f)).size > 50000, ex + ' ' + f);
  // the printed questions are bank items: in the AP course, distinct across the two exams
  assert.equal(sel[ex].length, 46, ex + ' selection: 42 multiple choice and 4 free response');
  sel[ex].forEach((id, i) => {
    const q = items[id]; assert(q, 'bank item ' + id);
    assert(!(q.standards || []).some(s => /BEYOND/.test(s)), id + ' is in the AP course');
    assert(!seen[id], id + ' appears in both exams'); seen[id] = ex;
    if (i < 42) assert(K[i].q.startsWith(strip(q.prompt.replace(/\n/g, ' ')).slice(0, 40)), id + ' printed as question ' + (i + 1) + ' of exam ' + ex);
    else { assert.match(id, /-f01$/, id + ' is a free-response problem'); assert(key.includes(strip(q.prompt).replace(/^Free response \([^)]*\)\.\s*/, '').slice(0, 40)), id + ' printed in exam ' + ex); }
  });
  const card = unit('statistical-inference').artifacts.find(a => a.path === `artifacts/statistics-ap-practice-exam-${ex}/exam.pdf`);
  assert(card && card.answerKey && exists(card.answerKey) && exists(card.thumb), 'Statistical Inference card for exam ' + ex);
}

// #17 tables and formula sheet, in every unit
const tables = rd('artifacts/statistics-tables-formulas/index.html');
for (const s of ['Table A', 'Table B', 'Table C', 'Formula']) assert(tables.includes(s), 'tables page has ' + s);
assert.match(tables, /0\.9750/, 'Table A has Φ(1.96) = 0.9750'); assert.match(tables, /2\.262/, 'Table B has t* = 2.262 (df 9, 95%)'); assert.match(tables, />3\.84<[\s\S]*?>5\.99<[\s\S]*?>7\.81</, 'Table C has 3.84, 5.99 and 7.81 at p = 0.05');
for (const u of stat.units) assert(u.artifacts.some(a => a.path.startsWith('artifacts/statistics-tables-formulas/')), 'tables card in ' + u.id);

// #1 follow-up: the rule line that opens an expanded solution fits the question
const FIT = [
  [/^Conditional probability/, /P\([^)]*\|/], [/^Sample SD/, /sample (SD|standard deviation)|standard deviation of (the|these)/i],
  [/^Standard deviations of sampling distributions shrink/, /\bn\b|sample size|quadrupl|halve|half/i], [/^Large Counts/, /Normal approximation|approximately Normal|Large Counts|np|n\(1/i],
  [/^Linear transformation/, /bonus|°F|X\b|y = |every value|to every|new (SD|mean|values)|SD of y|E\(Y\)/], [/^Binomial: P\(X = k\)/, /binomial|exactly|at most|at least|P\(X = \d|n = \d+ and p|coins?|tosses|heads|tails/i],
  [/^Read each leaf/, /stem/i], [/^Add the counts/, /how many|in all|observations/i], [/^Range = /, /\brange\b|largest and smallest/i], [/^P\(Type I error\)/, /Type I\b|error|α/],
];
let ruled = 0; const misfit = [];
for (const q of Object.values(items)) {
  const s0 = (q.solutionSteps || [])[0];
  for (const [rule, need] of FIT) if (typeof s0 === 'string' && rule.test(s0)) { ruled++; if (!need.test(q.prompt)) misfit.push(q.id + ': "' + s0.slice(0, 40) + '" for: ' + q.prompt.slice(-90).replace(/\n/g, ' ')); }
}
assert.deepEqual(misfit, [], 'worked-step rule lines that do not fit their questions');
assert(!Object.values(items).some(q => (q.solutionSteps || []).some(s => typeof s === 'string' && /\(-\d|\+ \(-/.test(s))), 'negative numbers in worked steps use −');
assert.match(items['stat-u1-s01-honors-x09'].solutionSteps[0], /stem/);

console.log(`PASS Statistics audit S3: teaching notes, pacing guide, ${M.tools.length} labs, 2 practice exams (42 MC + 4 FRQ, ${Object.keys(seen).length} distinct AP items), tables in ${stat.units.length} units; ${ruled} worked-step rule lines fit their questions`);
