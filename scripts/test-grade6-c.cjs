#!/usr/bin/env node
/* Grade 6 audit batch 6C (2026-11-19): #13 pacing guide, #14 practice tests and reference sheet, #16 labs.
   (#11 Graphing Practice and #12/#19 teaching notes and extension marks have their own tests: test-grade6-plot.cjs and
   test-grade6-notes.cjs.) */
'use strict';
const assert = require('assert');
const fs = require('fs');
const path = require('path');
const vm = require('vm');
const ROOT = path.join(__dirname, '..');
const rd = (p) => fs.readFileSync(path.join(ROOT, p), 'utf8');
const exists = (p) => fs.existsSync(path.join(ROOT, p));
const esc = (s) => String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');

const w = { console, Math, Date, JSON }; w.window = w; w.globalThis = w; vm.createContext(w);
vm.runInContext(rd('data.js'), w, { filename: 'data.js' });
const course = w.LIBRARY.courses.find((c) => c.id === 'math6');
const cards = (unit) => course.units.find((u) => u.id === unit).artifacts;

/* #16 labs: built pages, worksheets, keys, thumbnails and cards */
const M = JSON.parse(rd('tools/grade6-audit-20261119/labs/manifest.json'));
assert.deepStrictEqual(M.tools.map((t) => t.slug), ['grade6-fraction-cubes-lab', 'grade6-nets-lab']);
for (const t of M.tools) {
  const html = rd(`artifacts/${t.slug}/index.html`), src = rd(`tools/grade6-audit-20261119/labs/src/${t.slug}.js`);
  assert(html.includes(src.trim().slice(0, 200)) && html.includes('../interactive-math/lab.js'), t.slug + ' page is built from its source');
  for (const f of ['worksheet.pdf', 'teacher-key.pdf']) assert(fs.statSync(path.join(ROOT, 'artifacts', t.slug, f)).size > 20000, t.slug + ' ' + f);
  assert(exists(`thumbs/${t.slug}.jpg`), t.slug + ' thumbnail');
  const card = cards(t.unit).find((a) => a.path === `artifacts/${t.slug}/index.html`);
  assert(card && card.worksheet && card.answerKey && card.thumb && card.bankFormat === 'interactive-math', t.slug + ' card in ' + t.unit);
  assert.strictEqual((src.match(/\{ text: '/g) || []).length, 5, t.slug + ' has five challenges');
}
assert(/V = lwh/.test(M.tools[0].discovery) && /2lw \+ 2lh \+ 2wh/.test(M.tools[1].discovery), 'labs teach V = lwh with fraction edges and SA from nets');
assert(/function fr\(n, d\)/.test(rd('tools/grade6-audit-20261119/labs/src/grade6-fraction-cubes-lab.js')), 'the volume lab shows fractions and divisions stacked');
assert(rd('.github/workflows/interactive-math.yml').includes('tools/grade6-audit-20261119/labs/build.py'), 'CI rebuilds the Grade 6 labs');

/* #13 pacing guide: a Grade 6 entry with MCAS timing, extension standards per unit, and full coverage */
assert(/expectedStandalone=\[[^\]]*'grade-6-pacing\/'/.test(rd('scripts/test-public-site.cjs')), 'public-site test expects grade-6-pacing/');
const P = JSON.parse(require('child_process').execFileSync(process.execPath, ['--input-type=module', '-e', `
  import { geoPacingMain, planningPage, planningCourses } from './scripts/geo-planning.mjs';
  console.log(JSON.stringify({ html: geoPacingMain('math6', (t) => '#'), page: planningPage('math6'), has: planningCourses.includes('math6') }));`], { cwd: ROOT }));
assert(P.has && P.page === 'grade-6-pacing/', 'pacing page registered');
const text = P.html.replace(/<[^>]+>/g, ' ').replace(/\s+/g, ' ');
const days = [...text.matchAll(/Unit (\d+): [^0-9]+?(\d+)–(\d+) \((\d+)\)/g)].slice(0, 7).map((m) => ({ u: +m[1], a: +m[2], b: +m[3] }));
assert.strictEqual(days.length, 7, 'seven units in the full-year plan');
const mcas = text.match(/MCAS review and testing \(days (\d+)–(\d+)\)/);
assert(mcas && +mcas[1] === days[6].b + 1, 'MCAS review comes right after the last unit');
assert(+mcas[2] >= 140 && +mcas[2] <= 160, 'MCAS testing falls in spring (about days 140–160): ' + mcas[2]);
const post = text.match(/After the MCAS \(days (\d+)–(\d+)\)/);
assert(post && +post[1] === +mcas[2] + 1, 'post-test weeks follow the test');
assert(/Final review and exam \(days (\d+)–180\)/.test(text) && +text.match(/Final review and exam \(days (\d+)–180\)/)[1] === +post[2] + 1, 'the year ends with the final review and exam on day 180');
assert(/Practice Test A; Practice Test A review; Practice Test B/.test(text), 'review days use the two practice tests');
assert(/<th>Grade 7 extension standards<\/th>/.test(P.html) && /7\.EE\.B\.4b/.test(text) && /7\.SP\.B\.4/.test(text), 'units list their Grade 7 extension standards');
assert(/Solving One-Variable Inequalities \(extension\)/.test(text), 'extension lessons are marked in the plan');
const cov = text.match(/(\d+) of (\d+) standards have question-bank practice/);
assert(cov && cov[1] === cov[2] && +cov[2] === 42, 'all 42 Grade 6 standards have practice: ' + (cov && cov[0]));
const block = [...text.matchAll(/Final review and exam (\d+)/g)].pop();
assert(block && +block[1] <= 90, 'block plan fits in 90 days');

/* #14 practice tests and reference sheet */
const T = JSON.parse(rd('tools/grade6-audit-20261119/practice-tests.json'));
const bank = {};
for (const f of fs.readdirSync(path.join(ROOT, 'question-banks/math6')).filter((f) => f.endsWith('.json')))
  for (const q of JSON.parse(rd('question-banks/math6/' + f)).questions) bank[q.id] = q;
const A = T.tests.a, B = T.tests.b;
assert(A.length === 38 && B.length === 38 && !A.some((id) => B.includes(id)), '38 bank questions in each test, none shared');
for (const [ex, ids] of [['a', A], ['b', B]]) {
  const qs = ids.map((id) => bank[id]);
  assert(qs.every((q) => q && /^6\./.test(q.standards[0]) && ['cp1', 'honors'].includes(q.level)), ex + ': CP1/Honors items with a Grade 6 main standard');
  const count = (list, f) => list.filter((q) => q.format === f).length;
  for (const half of [qs.slice(0, 19), qs.slice(19)])
    assert(count(half, 'multiple-choice') === 12 && count(half, 'select-all') === 3 && count(half, 'short-answer') === 4, ex + ': item types per session');
  assert(qs.slice(0, 19).every((q) => /^6\.(NS|EE)/.test(q.standards[0])) && qs.slice(19).every((q) => /^6\.(RP|G|SP)/.test(q.standards[0])), ex + ': session domains');
  assert(new Set(qs.map((q) => q.skillId)).size >= 30, ex + ': spread over the skills');
  const exam = rd(`artifacts/grade6-practice-test-${ex}/exam.html`), key = rd(`artifacts/grade6-practice-test-${ex}/key.html`);
  for (const q of qs) assert(exam.includes(esc(q.prompt).slice(0, 60)), ex + ' prints ' + q.id);
  for (const q of qs.filter((q) => q.format === 'multiple-choice')) assert(key.includes(`(${'ABCD'[q.options.findIndex((o) => o.correct)]}) ${esc(q.answer)}`), ex + ' key for ' + q.id);
  assert(!/Calculator allowed|<td>Calculator/.test(exam) && /No calculator/.test(exam), ex + ': no calculator, as on the Grade 6 MCAS');
  assert(exam.includes('Grade 6 Mathematics Reference Sheet') && !key.includes('Grade 6 Mathematics Reference Sheet'), ex + ': reference sheet attached to the test');
  for (const f of ['exam.pdf', 'teacher-key.pdf']) assert(fs.statSync(path.join(ROOT, `artifacts/grade6-practice-test-${ex}/${f}`)).size > 40000, ex + ' ' + f);
  const card = cards('data-displays').find((a) => a.path === `artifacts/grade6-practice-test-${ex}/exam.pdf`);
  assert(card && card.answerKey === `artifacts/grade6-practice-test-${ex}/teacher-key.pdf` && exists(card.thumb), ex + ' card');
}
/* Constructed-response answers, recomputed */
const cr = (ex, i) => T.cr[ex][i].parts.map((p) => p[1]);
{ const a = cr('a', 0); assert(a[0] === 'c = 8w + 5' && a[2] === '$' + (8 * 7 + 5) && a[3] === (85 - 5) / 8 + ' walks', 'dog-walking business'); }
{ const a = cr('a', 1), white = 12 / 3 * 5, blue = 40 * 3 / 8; assert(a[0] === '3 : 8' && a[1] === white + ' cups' && a[2] === (3 / 8 * 100) + '%' && a[3] === blue + ' cups', 'paint mixture'); }
{ const a = cr('b', 0), gf = (5 - -6) * 10, fp = (4 - -3) * 10; assert(a[0] === gf + ' meters' && a[1] === fp + ' meters' && a[2] === '(−6, −4)' && a[3] === gf + fp + ' meters', 'park map'); }
{ const a = cr('b', 1), l = 2.5, w = 2, h = 1.5, mx = (x) => (Math.floor(x) ? Math.floor(x) + ' ' : '') + (x % 1 === 0.5 ? '1/2' : '').trim();
  assert(a[0] === mx(l * w * h) + ' cubic feet' && a[1] === l * w + ' square feet' && a[2] === mx(2 * (l * w + l * h + w * h)) + ' square feet' && a[3] === (l * 2) * (w * 2) * (h * 2) + ' cubes', 'storage box'); }
const ref = rd('artifacts/grade6-reference-sheet/index.html');
for (const s of ['A = lw', 'A = bh', 'V = lwh = Bh', 'IQR = Q3 − Q1', '1 mi = 5,280 ft', 'not the official MCAS reference sheet']) assert(ref.includes(s), 'reference sheet: ' + s);
assert(/class="fr"/.test(ref), 'reference-sheet fractions are stacked');
for (const u of ['ratios-rates-percent-proportions', 'geometry', 'data-displays'])
  assert(cards(u).some((a) => a.path === 'artifacts/grade6-reference-sheet/reference-sheet.pdf'), 'reference sheet card in ' + u);
assert(fs.statSync(path.join(ROOT, 'artifacts/grade6-reference-sheet/reference-sheet.pdf')).size > 20000, 'reference sheet PDF');

console.log(`PASS Grade 6 audit 6C: ${M.tools.length} labs, pacing guide (MCAS days ${mcas[1]}–${mcas[2]}, ${cov[1]}/${cov[2]} standards), 2 practice tests (76 bank questions + 4 constructed response), reference sheet`);
