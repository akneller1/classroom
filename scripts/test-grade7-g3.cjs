#!/usr/bin/env node
/* Grade 7 audit batch G3 (2026-11-19): #15 labs, #17 pacing guide and #18 practice tests and reference sheet.
   (#14 Graphing Practice and #16 teaching notes have their own tests: test-grade7-plot.cjs and test-grade7-notes.cjs.) */
'use strict';
const assert = require('assert');
const fs = require('fs');
const path = require('path');
const vm = require('vm');
const ROOT = path.join(__dirname, '..');
const rd = (p) => fs.readFileSync(path.join(ROOT, p), 'utf8');
const exists = (p) => fs.existsSync(path.join(ROOT, p));

const w = { console, Math, Date, JSON }; w.window = w; w.globalThis = w; vm.createContext(w);
vm.runInContext(rd('data.js'), w, { filename: 'data.js' });
const course = w.LIBRARY.courses.find((c) => c.id === 'prealgebra7');
const cards = (unit) => course.units.find((u) => u.id === unit).artifacts;

/* #15 labs: built pages, worksheets, keys, thumbnails and cards in the right units */
const M = JSON.parse(rd('tools/grade7-audit-20261119/labs/manifest.json'));
assert.deepStrictEqual(M.tools.map((t) => t.slug), ['grade7-integer-chips-lab', 'grade7-circles-lab', 'grade7-scale-drawing-lab']); // the third lab came in batch G4
for (const t of M.tools) {
  const html = rd(`artifacts/${t.slug}/index.html`), src = rd(`tools/grade7-audit-20261119/labs/src/${t.slug}.js`);
  assert(html.includes(src.trim().slice(0, 200)) && html.includes('../interactive-math/lab.js'), t.slug + ' page is built from its source');
  for (const f of ['worksheet.pdf', 'teacher-key.pdf']) assert(fs.statSync(path.join(ROOT, 'artifacts', t.slug, f)).size > 20000, t.slug + ' ' + f);
  assert(exists(`thumbs/${t.slug}.jpg`), t.slug + ' thumbnail');
  const card = cards(t.unit).find((a) => a.path === `artifacts/${t.slug}/index.html`);
  assert(card && card.worksheet && card.answerKey && card.thumb && card.bankFormat === 'interactive-math', t.slug + ' card in ' + t.unit);
  assert.strictEqual((src.match(/\{ text: '/g) || []).length, 5, t.slug + ' has five challenges');
}
assert(/a − b = a \+ \(−b\)/.test(M.tools[0].discovery) && /πr²/.test(M.tools[1].discovery), 'labs teach integer operations and circle area');
assert(rd('.github/workflows/interactive-math.yml').includes('tools/grade7-audit-20261119/labs/build.py'), 'CI rebuilds the Grade 7 labs');

/* #17 pacing guide: a Grade 7 entry with MCAS timing, Grade 7 and 8 standards per unit, and full coverage */
const site = rd('scripts/test-public-site.cjs');
assert(/expectedStandalone=\[[^\]]*'grade-7-pacing\/'/.test(site), 'public-site test expects grade-7-pacing/');
const run = require('child_process').execFileSync(process.execPath, ['--input-type=module', '-e', `
  import { geoPacingMain, planningPage, planningCourses } from './scripts/geo-planning.mjs';
  console.log(JSON.stringify({ html: geoPacingMain('prealgebra7', (t) => '#'), page: planningPage('prealgebra7'), has: planningCourses.includes('prealgebra7') }));`], { cwd: ROOT });
const P = JSON.parse(run);
assert(P.has && P.page === 'grade-7-pacing/', 'pacing page registered');
const text = P.html.replace(/<[^>]+>/g, ' ').replace(/\s+/g, ' ');
const days = [...text.matchAll(/Unit (\d+): [^0-9]+?(\d+)–(\d+) \((\d+)\)/g)].slice(0, 13).map((m) => ({ u: +m[1], a: +m[2], b: +m[3] }));
assert.strictEqual(days.length, 13, 'thirteen units in the full-year plan');
const mcas = text.match(/MCAS review and testing \(days (\d+)–(\d+)\)/);
assert(mcas && +mcas[1] === days[11].b + 1 && days[12].a === +mcas[2] + 1, 'MCAS review and testing come between units 12 and 13');
assert(+mcas[2] >= 140 && +mcas[2] <= 165, 'MCAS testing falls in May (about days 140–165): ' + mcas[2]);
assert(/Final review and exam \(days \d+–180\)/.test(text), 'the year ends on day 180');
assert(/Practice Test A; Practice Test A review; Practice Test B/.test(text), 'review days use the two practice tests');
assert(/<th>Grade 7 and 8 standards<\/th>/.test(P.html) && /7\.RP\.A\.3/.test(text), 'each unit lists its Grade 7 and 8 standards');
const cov = text.match(/(\d+) of (\d+) standards have question-bank practice/);
assert(cov && cov[2] === '68' && cov[1] === '68', 'all 68 Grade 7 and Grade 8 standards have practice: ' + (cov && cov[0]));
const block = [...text.matchAll(/Final review and exam (\d+)/g)].pop();
assert(block && +block[1] <= 90, 'block plan fits in 90 days');

/* #18 practice tests and reference sheet */
const T = JSON.parse(rd('tools/grade7-audit-20261119/practice-tests.json'));
const bank = {};
for (const f of fs.readdirSync(path.join(ROOT, 'question-banks/prealgebra7')).filter((f) => f.endsWith('.json')))
  for (const q of JSON.parse(rd('question-banks/prealgebra7/' + f)).questions) bank[q.id] = q;
const A = T.tests.a, B = T.tests.b;
assert(A.length === 38 && B.length === 38 && !A.some((id) => B.includes(id)), '38 bank questions in each test, none shared');
for (const [ex, ids] of [['a', A], ['b', B]]) {
  const qs = ids.map((id) => bank[id]);
  assert(qs.every((q) => q && /^7\./.test(q.standards[0]) && ['cp1', 'honors'].includes(q.level)), ex + ': CP1/Honors items with a Grade 7 main standard');
  const fmt = (q) => q.format, count = (list, f) => list.filter((q) => fmt(q) === f).length;
  for (const half of [qs.slice(0, 19), qs.slice(19)])
    assert(count(half, 'multiple-choice') === 12 && count(half, 'select-all') === 3 && count(half, 'short-answer') === 4, ex + ': item types per session');
  assert(qs.slice(0, 19).every((q) => /^7\.(NS|EE)/.test(q.standards[0])) && qs.slice(19).every((q) => /^7\.(RP|G|SP)/.test(q.standards[0])), ex + ': session domains');
  assert(new Set(qs.map((q) => q.skillId)).size >= 34, ex + ': spread over the skills');
  const exam = rd(`artifacts/grade7-practice-test-${ex}/exam.html`), key = rd(`artifacts/grade7-practice-test-${ex}/key.html`);
  for (const q of qs) assert(exam.includes(q.prompt.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').slice(0, 60)), ex + ' prints ' + q.id);
  for (const q of qs.filter((q) => q.format === 'multiple-choice')) {
    const k = 'ABCD'[q.options.findIndex((o) => o.correct)];
    assert(key.includes(`(${k}) ${String(q.answer).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;')}`), ex + ' key for ' + q.id);
  }
  assert(exam.includes('Grade 7 Mathematics Reference Sheet') && !key.includes('Grade 7 Mathematics Reference Sheet'), ex + ': reference sheet attached to the test');
  for (const f of ['exam.pdf', 'teacher-key.pdf']) assert(fs.statSync(path.join(ROOT, `artifacts/grade7-practice-test-${ex}/${f}`)).size > 40000, ex + ' ' + f);
  const card = cards('data-analysis-probability').find((a) => a.path === `artifacts/grade7-practice-test-${ex}/exam.pdf`);
  assert(card && card.answerKey === `artifacts/grade7-practice-test-${ex}/teacher-key.pdf` && exists(card.thumb), ex + ' card');
}
/* Constructed-response answers, recomputed */
const cr = (ex, i) => T.cr[ex][i].parts.map((p) => p[1]);
const money = (x) => '$' + x.toFixed(2);
{ const w8 = (120 - 40) / (25 - 15), wk = Math.floor((300 - 40) / 25) + 1; const a = cr('a', 0);
  assert(a[1].endsWith('w = ' + w8) && a[2] === '$' + (120 + 15 * w8) && 40 + 25 * w8 === 120 + 15 * w8 && a[3].endsWith(wk + ' weeks') && 40 + 25 * (wk - 1) <= 300, 'saving plans'); }
{ const sell = 48 * 1.75, sale = sell * 0.8, tot = Math.round(sale * 1.0625 * 100) / 100; const a = cr('a', 1);
  assert(a[0] === '$' + sell && a[1] === money(sale) && a[2] === money(tot) && a[3] === (Math.round((tot - 48) / 48 * 1000) / 10) + '%', 'markup, sale and tax'); }
{ const noon = -9 + 6 * 4, four = noon - 4 * 3; const a = cr('b', 0);
  assert(a[0] === noon + '°F' && a[1] === four + '°F' && a[2].endsWith('= ' + (four + 9) + '°F') && a[3].endsWith('= ' + (noon + 9) + '°F'), 'temperature changes'); }
{ const pi = 3.14, g = pi * 36, outer = pi * 64; const a = cr('b', 1);
  assert(a[0] === g.toFixed(2) + ' square feet' && a[1] === (outer - g).toFixed(2) + ' square feet' && a[2] === (2 * pi * 8).toFixed(2) + ' feet' && a[3] === (16 / 4) + ' inches', 'circular garden'); }
const ref = rd('artifacts/grade7-reference-sheet/index.html');
for (const s of ['A = πr<sup>2</sup>', 'C = πd = 2πr', 'V = Bh', 'I = Prt', '1 mi = 5,280 ft', 'not the official MCAS reference sheet']) assert(ref.includes(s), 'reference sheet: ' + s);
assert(/class="fr"/.test(ref), 'reference-sheet fractions are stacked');
for (const u of ['ratios-proportions-percentages', 'spatial-thinking', 'area-volume', 'data-analysis-probability'])
  assert(cards(u).some((a) => a.path === 'artifacts/grade7-reference-sheet/reference-sheet.pdf'), 'reference sheet card in ' + u);
assert(fs.statSync(path.join(ROOT, 'artifacts/grade7-reference-sheet/reference-sheet.pdf')).size > 20000, 'reference sheet PDF');

console.log(`PASS Grade 7 audit G3: ${M.tools.length} labs, pacing guide (MCAS days ${mcas[1]}–${mcas[2]}, ${cov[1]}/${cov[2]} standards), 2 practice tests (76 bank questions + 4 constructed response), reference sheet`);
