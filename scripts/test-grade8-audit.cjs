#!/usr/bin/env node
/* 8th Grade Math audit (2026-11-19): regression checks for the fixes, with independent recomputation of new and
   rewritten items. Run: node scripts/test-grade8-audit.cjs */
'use strict';
const fs = require('fs'), path = require('path'), vm = require('vm'), assert = require('assert/strict');
const ROOT = path.resolve(__dirname, '..');
const UNITS = ['real-numbers-exponents', 'equations-expressions', 'linear-functional-relationships', 'systems-linear-equations',
  'patterns-bivariate-data', 'congruence-similarity', 'geometry-applications'];
const Q = [];
for (const u of UNITS) for (const q of JSON.parse(fs.readFileSync(path.join(ROOT, 'question-banks/prealgebra', u + '.json'), 'utf8')).questions) Q.push(Object.assign({ unit: u }, q));
const byId = Object.fromEntries(Q.map((q) => [q.id, q]));
const fails = [];
let checks = 0;
function check(q, ok, msg) { checks++; if (!ok) fails.push((q && q.id ? q.id + ': ' : '') + msg); }
const texts = (q) => [q.prompt, ...(Array.isArray(q.answer) ? q.answer : [String(q.answer)]), ...(q.options || []).map((o) => String(o.text)), ...(q.solutionSteps || [])];
const fam = (q) => ((q.sourceNotes || '').match(/family: ([a-z0-9_-]+)\)/) || [])[1] || '';
const gcd = (a, b) => (b ? gcd(b, a % b) : Math.abs(a));
const frac = (n, d) => { if (d < 0) { n = -n; d = -d; } const g = gcd(n, d); return d / g === 1 ? String(n / g) : n / g + '/' + d / g; };
const num = (s) => +String(s).replace(/[^\d.-]/g, '');

/* #11 simplest radical form */
{
  const sq = (n) => { for (let k = 2; k * k <= n; k++) if (n % (k * k) === 0) return false; return true; };
  for (const q of Q) if (/simplest radical form|Give the exact value/.test(q.prompt) && q.format === 'short-answer')
    for (const m of String(q.answer).matchAll(/√(\d+)/g)) check(q, sq(+m[1]), 'exact answer not in simplest radical form: ' + q.answer);
  assert.equal(byId['pa8-geo-s01-honors-001'].answer, '2√10 cm');
}
/* #12 leftover generator wording, #13 π coefficients */
for (const q of Q) for (const t of texts(q)) {
  check(q, !/\b(?:[A-Z]′?){3,4} [A-Z]′?\(-?\d/.test(t), 'vertices without "with vertices": ' + t.slice(0, 60));
  check(q, !/ {2,}/.test(t), 'double space');
  check(q, !/ \+ 0(?= ?(?:=|have\b|has\b|when\b|\)|[.,;]|$))/.test(t), '"+ 0" left in: ' + t.slice(0, 60));
  check(q, !/(?<![\w.²³)⁰¹⁴-⁹/])1[a-z](?![a-z\d(])/.test(t), 'coefficient 1 written: ' + t.slice(0, 60));
  check(q, !/\b[Aa] (?:8|11|18|8\d)(?=[- ])/.test(t), '"a 8"');
  check(q, !/\$\d+\.\d(?!\d)/.test(t), 'money with one decimal place');
  check(q, !/are 1 more|wxyz/.test(t), 'wording');
  check(q, !/(?<![\w(./)])\d+\/\d+π/.test(t), 'ambiguous π coefficient: ' + t.slice(0, 60));
}
/* #16 no exponential equations in the x² = p, x³ = p skill; the skills have their new names */
{
  for (const q of Q.filter((q) => q.skillId === 'equations-expressions-skill-08')) check(q, !/ˣ/.test(q.prompt), 'exponential equation in the x² = p skill');
  const cat = fs.readFileSync(path.join(ROOT, 'course-catalog.js'), 'utf8');
  assert(cat.includes('"Square and cube roots in expressions"') && cat.includes('"Solving x² = p and x³ = p equations"'), 'renamed skills');
  for (const id of ['pa8-eqx-s08-cp1-004', 'pa8-eqx-s08-cp1-008', 'pa8-eqx-s08-cp1-012', 'pa8-eqx-s08-cp1-016', 'pa8-eqx-s08-honors-004', 'pa8-eqx-s08-honors-009', 'pa8-eqx-s08-honors-014']) {
    const q = byId[id], m = /^Solve: (.+) = (-?\d+)$/.exec(q.prompt);
    const lhs = m[1].replace(/x²/g, 'x**2').replace(/x³/g, 'x**3').replace(/(\d)x/g, '$1*x').replace(/\)([²³])/g, (a, b) => ')**' + (b === '²' ? 2 : 3)).replace(/²/g, '**2').replace(/³/g, '**3');
    const f = new Function('x', 'return ' + lhs), want = +m[2];
    const sols = [...String(q.answer).matchAll(/x = (-?\d+)/g)].map((a) => +a[1]);
    for (const s of sols) check(q, f(s) === want, 'solution does not check: ' + s);
    const all = []; for (let x = -50; x <= 50; x++) if (f(x) === want) all.push(x);
    check(q, all.length === sols.length, 'missing or extra solutions ' + all);
  }
}
/* #17 every number in a short answer appears in the steps */
for (const q of Q) if (q.format === 'short-answer') {
  const st = (q.solutionSteps || []).join(' ');
  for (const n of String(q.answer).match(/-?\d+(?:\.\d+)?(?:\/\d+)?/g) || []) check(q, st.includes(n.replace(/^-/, '')), 'answer ' + n + ' never shown in the steps');
}
/* #5 Tarsia items: on-skill, recomputed, different by level, distinct answers, Tarsia-sized */
{
  const T = Q.filter((q) => /-tarsia-/.test(q.id));
  assert.equal(T.length, 90);
  const answers = {};
  for (const q of T) {
    const p = q.prompt, a = String(q.answer);
    check(q, p.length <= 110 && a.length <= 20 && !/\n/.test(p) && !q.diagram, 'not Tarsia-sized');
    check(q, !/athletes|ride a bike\? *$/.test(p) || /Simplify/.test(p), 'old filler item');
    let want = null, m;
    if ((m = /best-fit line is y = (-?[\d.]+)x \+ (\d+)\. Predict y when x = (\d+)/.exec(p))) want = String(+(m[1] * m[3] + +m[2]).toFixed(4));
    else if ((m = /best-fit line y = (\d+)x \+ (\d+) predicts y = (\d+)/.exec(p))) want = 'x = ' + (m[3] - m[2]) / m[1];
    else if ((m = /score = ([\d.]+)h \+ \d+ .* for (\d+) more hours/.exec(p))) want = +(m[1] * m[2]).toFixed(4) + ' points';
    else if ((m = /(\d+) grade 7 students play a sport and (\d+) do not\. What is the grade 7 row total/.exec(p))) want = String(+m[1] + +m[2]);
    else if ((m = /row totals (\d+) \(grade 7\) and (\d+) \(grade 8\)\. (\d+) students play a sport/.exec(p))) want = String(+m[1] + +m[2] - +m[3]);
    else if ((m = /Grade 7: (\d+) play a sport, \d+ do not\. Grade 8: x play, \d+ do not\. (\d+) play a sport in all/.exec(p))) want = 'x = ' + (m[2] - m[1]);
    else if ((m = /Of (\d+) grade 8 students, (\d+) ride a bike/.exec(p))) want = frac(+m[2], +m[1]);
    else if ((m = /(\d+) of (\d+) students have a pet/.exec(p))) want = (100 * m[1] / m[2]) + '%';
    else if ((m = /Grade 7: (\d+) of (\d+) ride a bus\. Grade 8: (\d+) of (\d+) ride a bus\. How many percentage points higher is (grade \d)/.exec(p))) {
      const p7 = 100 * m[1] / m[2], p8 = 100 * m[3] / m[4];
      want = String(Math.abs(p7 - p8));
      check(q, m[5] === (p7 > p8 ? 'grade 7' : 'grade 8'), 'wrong grade named');
    }
    check(q, want !== null, 'unrecognised Tarsia item');
    if (want !== null) check(q, want === a, 'key ' + a + ' but recomputed ' + want);
    const k = q.skillId + '|' + q.level;
    (answers[k] = answers[k] || []).push(a);
  }
  for (const [k, v] of Object.entries(answers)) check(null, new Set(v).size === v.length, 'repeated Tarsia answers in ' + k);
  for (const sk of ['04', '05', '06']) {
    const tmpl = (lv) => new Set(T.filter((q) => q.level === lv && q.skillId.endsWith(sk)).map((q) => q.prompt.replace(/-?\d+(\.\d+)?/g, '#')));
    const s2 = tmpl('cp2'), sh = tmpl('honors');
    check(null, [...sh].every((t) => !s2.has(t)), 'Advanced Tarsia items reuse Support templates in skill ' + sk);
  }
}
/* #6 select-all: the number of correct options varies */
{
  const SA = Q.filter((q) => q.format === 'select-all'), cnt = {};
  for (const q of SA) { const c = q.options.filter((o) => o.correct).length; cnt[c] = (cnt[c] || 0) + 1; check(q, c >= 2 && c <= 4, 'correct count ' + c); }
  assert(Object.keys(cnt).length >= 3 && cnt[3] / SA.length < 0.5, 'select-all correct counts ' + JSON.stringify(cnt));
}
/* #8 proportional relationships: graphs, select-all and recomputed keys */
{
  const S = Q.filter((q) => q.skillId === 'linear-functional-relationships-skill-12');
  assert(S.length >= 60, 'skill 12 has ' + S.length + ' items');
  for (const lv of ['cp2', 'cp1', 'honors']) {
    const L = S.filter((q) => q.level === lv);
    check(null, L.filter((q) => q.diagram).length >= 2 && L.some((q) => q.format === 'select-all'), 'skill 12 ' + lv + ' needs graphs and select-all');
  }
  for (const q of S.filter((q) => /prop_graph_rate|prop_graph_equation/.test(fam(q)))) {
    const m = /\((\d+), (\d+)\) marked/.exec(q.diagram.spec.alt), k = +m[2] / +m[1];
    check(q, fam(q) === 'prop_graph_rate' ? num(String(q.answer).split(' ')[0]) === k : q.answer === 'y = ' + k + 'x', 'graph unit rate ' + k);
    check(q, fs.existsSync(path.join(ROOT, q.diagram.spec.src)), 'image missing');
  }
  const mc = byId['pa8-lfr-s12-honors-020'], mm = /\((\d+), (\d+)\) and \(x, (\d+)\)/.exec(mc.prompt);
  check(mc, mc.answer === 'x = ' + mm[3] * mm[1] / mm[2], 'missing coordinate');
  const pr = byId['pa8-lfr-s12-honors-018'], r = 8 / 5;
  check(pr, pr.options.filter((o) => { const p = /\(([\d.]+), ([\d.]+)\)/.exec(o.text); return Math.abs(p[2] - r * p[1]) < 1e-9; }).length === 1 && pr.options.find((o) => o.correct).text === pr.answer, 'exactly one point on y = 1.6x');
  const pts = byId['pa8-lfr-s12-cp2-019'];
  for (const o of pts.options) { const p = /\((\d+), (\d+)\)/.exec(o.text); check(pts, o.correct === (+p[2] === 4 * p[1]), 'point ' + o.text); }
}
/* #18 scatter plots and marked points are not clipped at the edge of the grid */
{
  assert(/scatter\([^)]*clip_on=False/.test(fs.readFileSync(path.join(ROOT, 'tools/prealgebra-authoring/u5_bivariate.py'), 'utf8')), 'scatter points drawn unclipped');
  assert(/ms=7, zorder=5, clip_on=False/.test(fs.readFileSync(path.join(ROOT, 'tools/prealgebra-authoring/lib.py'), 'utf8')), 'marked points drawn unclipped');
}
/* #19 inline tables render as tables */
{
  const c = { console }; c.window = c; vm.createContext(c);
  vm.runInContext(fs.readFileSync(path.join(ROOT, 'worksheet-generator/core/math-display.js'), 'utf8'), c);
  const D = c.MK_MATH_DISPLAY, INLINE = /[^:;?!]{1,40}: (?:-?\d+(?:\.\d+)?|\?)(?:, (?:-?\d+(?:\.\d+)?|\?)){2,}; [^:;?!]{1,40}: (?:-?\d+(?:\.\d+)?|\?)(?:, (?:-?\d+(?:\.\d+)?|\?)){2,}/;
  const tbl = Q.filter((q) => INLINE.test(q.prompt));
  assert(tbl.length >= 200, 'inline-table prompts ' + tbl.length);
  for (const q of tbl) check(q, D.html(q.prompt).includes('mk-inline-table'), 'inline table not drawn');
  const h = D.html('Write a function rule for the table. x: 0, 1, 2, 3; y: 1, 4, 7, 10');
  assert(/<th scope="row"><i>x<\/i><\/th><td>0<\/td>/.test(h) && !/x<\/i>: 0/.test(h), 'table cells');
  assert.equal(D.layout('Solve 2x + 3 = 7.'), null);
}
/* #4 and #20 the practice test grades most short answers automatically */
{
  const c = {}; c.window = c; vm.createContext(c);
  for (const f of ['worksheet-generator/menu/mathcheck.js', 'worksheet-generator/practice/radical-grading.js', 'worksheet-generator/practice/exact-grading.js', 'worksheet-generator/practice/discrete-grading.js', 'worksheet-generator/practice/grade8-grading.js', 'worksheet-generator/practice/grading.js'])
    vm.runInContext(fs.readFileSync(path.join(ROOT, f), 'utf8'), c, { filename: f });
  c.MK_PRACTICE_COURSE = 'prealgebra';
  const P = c.MKPRACTICE, sa = Q.filter((q) => q.format === 'short-answer'), auto = sa.filter((q) => P.bankAnswer(String(q.answer), q.prompt) !== null);
  assert(auto.length / sa.length >= 0.9, 'auto-graded short answers ' + auto.length + '/' + sa.length);
  for (const q of auto) check(q, P.gradeBank(String(q.answer), String(q.answer), q.prompt).status === 'correct', 'key does not grade itself correct');
  for (const [k, t, want, prompt] of [['126°', '126', 'correct'], ['703.4 cubic inches', '703.4', 'correct'], ['192π cubic inches', '192pi', 'correct'],
    ['(2048/3)π cubic centimeters', '2048π/3', 'correct'], ['$105', '105', 'correct'], ['x = 10 or x = -10', 'x=±10', 'correct'], ['x = 10 or x = -10', 'x = 10', 'invalid'],
    ['7.1 × 10⁻³', '7.1e-3', 'correct'], ['7.1 × 10⁻³', '7.1 x 10^-3', 'correct'], ['7.1 × 10⁻³', '71 x 10^-4', 'incorrect'], ['7.1 × 10⁻³', '0.0071', 'invalid'],
    ['18a⁹', '18a^9', 'correct'], ['18a⁹', '18a^8', 'incorrect'], ['rational', 'Rational', 'correct'], ['rational', 'irrational', 'incorrect'], ['nonlinear', 'non-linear', 'correct'],
    ['8 and 9', '8, 9', 'correct'], ['8 and 9', '7 and 8', 'incorrect'], ['infinitely many solutions', 'infinite', 'correct'], ['no solution', 'one solution', 'incorrect'],
    ['y = 2x - 5', 'y=-5+2x', 'correct'], ['y = 2x - 5', 'y = 2(x-2.5)', 'invalid'], ['y = 2x - 5', 'y = 2x + 5', 'incorrect'], ['C = 14g + 24', 'C=24+14g', 'correct'],
    ['6x + 18', '18+6x', 'correct'], ['6x + 18', '6(x+3)', 'incorrect'], ['33 + 20c = 133', '20c + 33 = 133', 'correct'], ['33 + 20c = 133', '20c = 100', 'incorrect'],
    ['6 units', '6', 'correct'], ['49 miles per hour', '49 mph', 'correct'], ['slope -1, y-intercept 5', '-1, 5', 'correct'], ['from x = 1 to x = 6', '1 to 6', 'correct'],
    ['√18', '√18', 'correct', 'Which is greater: √18 or 4.1?'], ['√18', '4.1', 'incorrect', 'Which is greater: √18 or 4.1?'],
    ['2.2, √6, √18, 29/4', '2.2, √6, √18, 29/4', 'correct', 'Order from least to greatest: 2.2; √18; 29/4; √6.'],
    ['2.2, √6, √18, 29/4', '√6, 2.2, √18, 29/4', 'incorrect', 'Order from least to greatest: 2.2; √18; 29/4; √6.']])
    { const got = P.gradeBank(k, t, prompt || '').status; check(null, got === want, 'grading ' + k + ' ← ' + t + ': ' + got + ', expected ' + want); }
  c.MK_PRACTICE_COURSE = 'algebra2';
  assert.equal(P.gradeBank('rational', 'Rational', '').status, 'self', 'the Grade 8 grader is off in other courses');
  const html = fs.readFileSync(path.join(ROOT, 'worksheet-generator/practice-test.html'), 'utf8');
  assert(html.indexOf('practice/grade8-grading.js') > 0 && html.indexOf('practice/grade8-grading.js') < html.indexOf('practice/grading.js'), 'practice test loads the Grade 8 grader');
}
/* #10 item-specific steps: two or more steps (or one worked step that reaches the answer), at least one written for this item, select-all choices named; two dilations
   about the same center with scale factors 2 and 1/2 give a congruent image */
{
  const count = {};
  for (const q of Q) for (const st of new Set(q.solutionSteps || [])) count[st] = (count[st] || 0) + 1;
  for (const q of Q) {
    if (q.format === 'open-response') continue;
    const st0 = q.solutionSteps || [];
    check(q, st0.length >= 2 || (st0.length === 1 && count[st0[0]] < 10 && st0[0].includes(String(q.answer))), 'one generic step');
    check(q, q.solutionSteps.some((st) => count[st] < 10), 'only boilerplate steps');
    if (q.format === 'select-all') {
      const st = q.solutionSteps.find((x) => x.startsWith('Correct choices: '));
      check(q, st && q.options.every((o) => st.includes(o.text.replace(/\.$/, ''))), 'select-all steps name every choice');
    }
  }
  for (const q of Q.filter((q) => /dilation with scale factor .*then a dilation with scale factor/.test(q.prompt))) {
    const k = [...q.prompt.matchAll(/scale factor (\d+)(?:\/(\d+))?/g)].map((m) => +m[1] / (+m[2] || 1));
    check(q, q.answer === (Math.abs(k[0] * k[1] - 1) < 1e-9 ? 'congruent' : 'similar'), 'two dilations: ' + k.join(' × '));
  }
}
/* #15 every skill has open-response items at every level (23 skills in the first pass, 45 skill/levels in batch F) */
{
  const sk = [...new Set(Q.map((q) => q.skillId))];
  for (const s of sk) check({ id: s }, Q.some((q) => q.skillId === s && q.format === 'open-response' && q.parts.length >= 4), 'no open-response item');
  for (const q of Q.filter((q) => /-o01$/.test(q.id))) check(q, q.format === 'open-response' && q.parts.length >= 4 && q.solutionSteps.length === q.parts.length, 'new open-response item');
  assert.equal(Q.filter((q) => /-o01$/.test(q.id)).length, 114);
  const o = (id) => byId[id].parts.map((p) => p.answer);
  // batch F: every skill now has an open-response item at Support, Standard and Advanced
  for (const s of sk) for (const L of ['cp2', 'cp1', 'honors']) check({ id: s + '|' + L }, Q.some((q) => q.skillId === s && q.level === L && q.format === 'open-response' && q.parts.length >= 4), 'no open-response item at this level');
  assert.deepEqual(o('pa8-sys-s06-cp1-o01').slice(1, 3), ['a = 90', 's = 110']);
  assert.equal(8 * 90 + 5 * 110, 1270);
  assert.equal(o('pa8-rne-s06-cp1-o01')[2], '√50, 50/7, 7.2');
  assert(Math.sqrt(50) < 50 / 7 && 50 / 7 < 7.2);
  assert.equal(o('pa8-geo-s03-honors-o01')[1], '392π cubic cm');
  assert.equal((49 * 24) / 3, 392);
  assert.deepEqual(o('pa8-sys-s03-honors-o01').slice(1, 3), ['c = 25', 'a = 40']);
  assert.equal(12 * 40 + 8 * 25, 680);
  assert.equal(o('pa8-lfr-s09-honors-o01')[2], '450 minutes');
  assert(Math.abs((24 - 15) / (0.10 - 0.08) - 450) < 1e-6);
}
/* #9 Graphing Practice: plot items in four units, every target and wrong answer checked by the site's grader */
{
  const c = {}; vm.createContext(c);
  vm.runInContext(fs.readFileSync(path.join(ROOT, 'worksheet-generator/core/plot.js'), 'utf8'), c);
  const PL = c.MK_PLOT, plots = Q.filter((q) => q.format === 'plot');
  assert(plots.length >= 70, 'plot items ' + plots.length);
  assert(new Set(plots.map((q) => q.unit)).size >= 4, 'plot units');
  for (const q of plots) {
    check(q, PL.valid(q.plot) && PL.check(q.plot, q.plot.testVectors.correct).ok, 'plot target');
    for (const w of q.plot.testVectors.wrong) { const r = PL.check(q.plot, w.response); check(q, !r.ok && r.code === w.expectCode && (q.plot.feedback || {})[r.code], 'plot wrong vector ' + JSON.stringify(w)); }
    check(q, fs.existsSync(path.join(ROOT, q.plot.answerKey.src)), 'plot answer key image');
  }
  for (const q of plots.filter((q) => /plot_transform/.test(q.sourceNotes))) {
    const tri = [...q.prompt.matchAll(/[ABC]\((-?\d+), (-?\d+)\)/g)].map((m) => [+m[1], +m[2]]), w = q.prompt;
    const f = /180°/.test(w) ? ([x, y]) => [-x, -y] : /90° counterclockwise/.test(w) ? ([x, y]) => [-y, x] : /90° clockwise|270° counterclockwise/.test(w) ? ([x, y]) => [y, -x]
      : /over the x-axis/.test(w) ? ([x, y]) => [x, -y] : /over the y-axis/.test(w) ? ([x, y]) => [-x, y] : /line y = x/.test(w) ? ([x, y]) => [y, x] : /line y = -x/.test(w) ? ([x, y]) => [-y, -x]
      : /scale factor (\d+)\/(\d+)/.test(w) ? (([, a, b]) => ([x, y]) => [x * a / b, y * a / b])(/scale factor (\d+)\/(\d+)/.exec(w)) : /scale factor (\d+)/.test(w) ? (([, k]) => ([x, y]) => [x * k, y * k])(/scale factor (\d+)/.exec(w))
      : (() => { let dx = 0, dy = 0; for (const m of w.matchAll(/(\d+) units? (right|left) and (\d+) units? (up|down)/g)) { dx += (m[2] === 'right' ? 1 : -1) * m[1]; dy += (m[4] === 'up' ? 1 : -1) * m[3]; } for (const m of w.matchAll(/\(x ([+-]) (\d+), y ([+-]) (\d+)\)/g)) { dx += (m[1] === '+' ? 1 : -1) * m[2]; dy += (m[3] === '+' ? 1 : -1) * m[4]; } return ([x, y]) => [x + dx, y + dy]; })();
    const want = tri.map(f).map((p) => p.join()).sort().join(';'), got = q.plot.target.points.map((p) => p.map(Number).join()).sort().join(';');
    check(q, want === got, 'transformation image ' + want + ' vs ' + got);
  }
  const data = fs.readFileSync(path.join(ROOT, 'data.js'), 'utf8');
  assert(/"prealgebra": \["linear-functional-relationships", "systems-linear-equations", "patterns-bivariate-data", "congruence-similarity"\]/.test(data), 'Graphing Practice units');
}
/* #3 harder Advanced items in the 17 skills that were mostly re-numbered lower-level templates; #14 Standard items with an added step */
{
  const mask = (t) => t.replace(/-?\d+(\.\d+)?/g, '#');
  const H = Q.filter((q) => /-honors-h0\d$/.test(q.id) && !/batch D/.test(q.sourceNotes || ''));
  assert.equal(H.length, 136, 'new Advanced items');
  const skills = [...new Set(H.map((q) => q.skillId))];
  assert.equal(skills.length, 17);
  for (const sk of skills) {
    const lower = new Set(Q.filter((q) => q.skillId === sk && q.level !== 'honors').map((q) => mask(q.prompt)));
    const adv = Q.filter((q) => q.skillId === sk && q.level === 'honors' && q.format !== 'plot');
    for (const q of H.filter((q) => q.skillId === sk)) check(q, !lower.has(mask(q.prompt)), 'new Advanced item reuses a lower template');
    const clones = adv.filter((q) => lower.has(mask(q.prompt))).length;
    check({ id: sk }, clones / adv.length <= 0.6, 'Advanced clone share ' + clones + '/' + adv.length);
    check({ id: sk }, adv.filter((q) => q.format === 'multiple-choice').length >= 6, 'Advanced multiple choice for games');
    check({ id: sk }, Q.filter((q) => q.skillId === sk && /Moved from Advanced to Standard/.test(q.sourceNotes)).every((q) => q.level === 'cp1'), 'moved items are Standard');
  }
  // independent recomputation of the new Advanced items
  const R = (re, q) => re.exec(q.prompt);
  for (const q of H) {
    const f = fam(q), a = String(q.answer); let m, want = null;
    if (f === 's4_find_k' && (m = R(/between \((-?\d+), (-?\d+)\) and \(k, (-?\d+)\) is (\d+) units/, q))) want = 'k = ' + (+m[1] + Math.sqrt(m[4] ** 2 - (m[3] - m[2]) ** 2));
    if (f === 's4_equidistant' && (m = R(/from \(0, (\d+)\) as from \((\d+), 0\)/, q))) want = '(' + frac(m[2] ** 2 - m[1] ** 2, 2 * m[2]) + ', 0)';
    if (f === 's6_slope_from_point' && (m = R(/y = mx ([+-]) (\d+) passes through \((-?\d+), (-?\d+)\)/, q))) want = 'm = ' + frac(+m[4] - (m[1] === '+' ? 1 : -1) * m[2], +m[3]);
    if (f === 's8_perimeter_side' && (m = R(/perimeters (\d+) cm and (\d+) cm\. A side of the smaller triangle is (\d+) cm/, q))) want = frac(m[3] * m[2], +m[1]) + ' cm';
    if (f === 's8_nested_unknown' && (m = R(/BC = (\d+), BD = (\d+) and CE = (\d+)/, q))) want = 'x = ' + frac(m[2] * m[1], m[3] - m[2]);
    if (f === 's5_sphere_diameter' && (m = R(/diameter (\d+) cm/, q))) want = frac(4 * (m[1] / 2) ** 3, 3) + 'π cubic centimeters';
    if (f === 's5_cones_fill' && (m = R(/radius (\d+) ft and height (\d+) ft\. A cone-shaped bucket has radius (\d+) ft and height (\d+) ft/, q))) want = frac(3 * m[1] ** 2 * m[2], m[3] ** 2 * m[4]);
    if (f === 's7_pipe' && (m = R(/radius (\d+) cm and length (\d+) cm with a cylindrical hole of radius (\d+) cm/, q))) want = (m[1] ** 2 - m[3] ** 2) * m[2] + 'π cubic centimeters';
    if (f === 's6_coins' && (m = R(/has (\d+) coins, all dimes and quarters, worth \$(\d+)\.(\d\d)/, q))) want = String((+(m[2] + m[3]) - 10 * m[1]) / 15);
    if (f === 's1_function_value' && (m = /\((-?\d+), a\)/.exec(q.prompt))) want = 'a = ' + new RegExp('\\(' + m[1] + ', (-?\\d+)\\)').exec(q.prompt)[1];
    if (f === 's3_nth_digit' && (m = R(/^(\d+)\/(\d+) = .* What is the (\d+)th digit/, q))) { let r = +m[1] % +m[2], d = ''; for (let i = 0; i < +m[3]; i++) { r *= 10; d = String(Math.floor(r / m[2])); r %= +m[2]; } want = d; }
    if (f === 's1_above_line' && (m = R(/x: ([\d, ]+); y: ([\d, ]+) is graphed/, q))) { const xs = m[1].split(', ').map(Number), ys = m[2].split(', ').map(Number); want = String(xs.filter((x, i) => ys[i] > x).length); }
    if (want !== null) check(q, want === a, 'recomputed ' + want + ' but key ' + a);
  }
  assert(H.filter((q) => /s4_find_k|s4_equidistant|s6_slope_from_point|s8_perimeter_side|s8_nested_unknown|s5_sphere_diameter|s5_cones_fill|s7_pipe|s6_coins|s1_function_value|s3_nth_digit|s1_above_line/.test(fam(q))).length === 48, 'recomputed families');
  const S = Q.filter((q) => /audit #14/.test(q.sourceNotes));
  assert(S.length >= 50, 'Standard items with an added step ' + S.length);
  const cp2 = new Set(Q.filter((q) => q.level === 'cp2').map((q) => q.skillId + '|' + mask(q.prompt)));
  for (const q of S) check(q, q.level === 'cp1' && !cp2.has(q.skillId + '|' + mask(q.prompt)), 'Standard item still a Support template');
  for (const q of S.filter((q) => /Find y when x = (-?\d+)\.$/.test(q.prompt) && /x: /.test(q.prompt))) {
    const xs = /x: ([-\d, ]+);/.exec(q.prompt)[1].split(', ').map(Number), ys = /y: ([-\d/, ]+)\./.exec(q.prompt)[1].split(', ').map((v) => eval(v)), X = +/x = (-?\d+)\.$/.exec(q.prompt)[1];
    const m = (ys[1] - ys[0]) / (xs[1] - xs[0]), y = ys[0] + m * (X - xs[0]);
    check(q, Math.abs(eval(q.answer) - y) < 1e-9, 'table extension ' + y);
  }
  for (const q of S.filter((q) => /Find the perimeter of triangle DEF/.test(q.prompt))) {
    const m = /AB = (\d+), BC = (\d+), CA = (\d+), and (DE|EF|FD) = (\d+)/.exec(q.prompt), k = m[5] / { DE: m[1], EF: m[2], FD: m[3] }[m[4]];
    check(q, Math.abs(eval(q.answer) - k * (+m[1] + +m[2] + +m[3])) < 1e-9, 'perimeter');
  }
}
/* #3 follow-up (batch D): harder Advanced items in the other 37 skills, every key recomputed from the prompt */
{
  const mask = (t) => t.replace(/-?\d+(\.\d+)?/g, '#');
  const D = Q.filter((q) => /\(Advanced, batch D\)/.test(q.sourceNotes || ''));
  check(null, D.length >= 250, 'batch D Advanced items ' + D.length);
  const SUP = { '⁻': '-', '⁰': '0', '¹': '1', '²': '2', '³': '3', '⁴': '4', '⁵': '5', '⁶': '6', '⁷': '7', '⁸': '8', '⁹': '9' };
  const ev = (s) => { s = String(s).replace(/[()\s]/g, ''); const p = s.split('/'); return p.length === 2 ? +p[0] / +p[1] : +s; };
  const nums = (s) => (String(s).replace(/10([⁻⁰¹²³⁴⁵⁶⁷⁸⁹]+)/g, (m, e) => '10^' + [...e].map((c) => SUP[c]).join('')).match(/-?\d+(\.\d+)?(\/\d+)?/g) || []).map(ev);
  const lin = (s, v = 'x') => { let m = 0, b = 0; for (const t of s.replace(/\s+/g, '').split(/(?=[+-])/)) { if (!t) continue; if (t.includes(v)) { const c = t.replace(v, '').replace(/[()]/g, ''); m += c === '' || c === '+' ? 1 : c === '-' ? -1 : ev(c); } else b += ev(t); } return [m, b]; };
  const pt = (s) => /\((-?\d+), (-?\d+)\)/.exec(s).slice(1).map(Number);
  const sci = (v) => { const e = Math.floor(Math.log10(Math.abs(v)) + 1e-9); return [+(v / 10 ** e).toPrecision(12), 10, e]; };
  const rot = { '90° counterclockwise': ([x, y]) => [-y, x], '180°': ([x, y]) => [-x, -y], '90° clockwise': ([x, y]) => [y, -x] };
  const g = (re, s) => { const m = re.exec(s); if (!m) throw new Error('prompt shape: ' + re); return m; };
  const R = {
    s1_spread: (p) => { const v = nums(g(/least of (.*)\.$/, p)[1]); return [Math.max(...v) - Math.min(...v)]; },
    s1_part_of_way: (p) => { const m = g(/is (\S+) of the way from (\S+) to (\S+) on/, p); return [ev(m[2]) + ev(m[1]) * (ev(m[3]) - ev(m[2]))]; },
    s2_temperature_change: (p) => { const m = g(/was (-?[\d.]+)°C\. It dropped ([\d.]+)°C each hour for (\d+) hours, then rose ([\d.]+)/, p); return [+m[1] - m[2] * m[3] + +m[4]]; },
    s2_grouped_quotient: (p) => { const m = g(/\((\S+) \+ (\S+)\) ÷ \((\S+)\)/, p); return [(ev(m[1]) + ev(m[2])) / ev(m[3])]; },
    s4_make_rational: (p) => { const k = +g(/√\((\d+)n\)/, p)[1]; let n = 1; while (Math.sqrt(k * n) % 1) n++; return [n]; },
    s4_count_irrational_roots: (p) => { const n = +g(/from 1 to (\d+)/, p)[1]; return [n - Math.floor(Math.sqrt(n))]; },
    s5_conjugate_product: (p) => { const m = g(/\(√(\d+) \+ (\d+)\)/, p); return [m[1] - m[2] ** 2]; },
    s5_rational_product: (p) => { const m = g(/√(\d+) · √(\d+)/, p); return [Math.sqrt(m[1] * m[2])]; },
    s6_least_n_root: (p) => { const k = +g(/√n > ([\d.]+)/, p)[1]; return [Math.floor(+(k * k).toFixed(6)) + 1]; },
    s6_integers_between: (p) => { const m = g(/-√(\d+) and √(\d+)/, p); return [Math.floor(Math.sqrt(m[2])) + Math.floor(Math.sqrt(m[1])) + 1]; },
    s7_fraction_root: (p) => { const m = g(/area (\d+)\/(\d+)/, p); return [Math.sqrt(m[1]) / Math.sqrt(m[2])]; },
    s7_cube_edge_between: (p) => { const n = +g(/volume of (\d+)/, p)[1]; let k = 1; while ((k + 1) ** 3 < n) k++; return [k, k + 1]; },
    s10_normalize_small: (p) => { const m = nums(g(/Write (.*) in scientific/, p)[1]); return sci(m[0] * 10 ** m[2]); },
    s10_times_as_large: (p) => { const m = nums(g(/large is (.*) as (.*)\?/, p)[0].replace(/^How many times as large is /, '')); return [m[0] / m[3], 10, m[2] - m[5]]; },
    s11_light_distance: (p) => { const t = +g(/in (\d+) × 10² seconds/, p)[1]; return sci(3e5 * t * 100); },
    s1_cube_root_equation: (p) => { const m = g(/∛\((.*)\) = (\d+)/, p), [a, b] = lin(m[1]); return [(m[2] ** 3 - b) / a]; },
    s3_age_equation: (p) => { const m = g(/is (\d+) years old .* In (\d+) years Maya will be (\d+) times/, p); return [(+m[1] + +m[2]) / m[3] - m[2]]; },
    s3_consecutive_even: (p) => { const m = g(/sum of (\d+) consecutive even integers is (\d+)/, p), n = +m[1]; return [(m[2] - n * (n - 1)) / n + 2 * (n - 1)]; },
    s4_decimal_distribute: (p) => { const m = g(/Solve: ([\d.]+)\(x \+ (\d+)\) = ([\d.]+)x ([+-]) ([\d.]+)/, p), d = (m[4] === '-' ? -1 : 1) * m[5]; return [(d - m[1] * m[2]) / (m[1] - m[3])]; },
    s4_cross_multiply: (p) => { const m = g(/\(x \+ (\d+)\)\/(\d+) = \(x ([+-]) (\d+)\)\/(\d+)/, p), e = (m[3] === '-' ? -1 : 1) * m[4]; return [(m[2] * e - m[5] * m[1]) / (m[5] - m[2])]; },
    s6_consecutive_odd: (p) => [(g(/is (\d+)\./, p)[1] - 12) / 4],
    s6_triangle_perimeter: (p) => { const m = g(/sides x, 2x \+ (\d+) and 3x - (\d+)\. Its perimeter is (\d+)/, p), x = (m[3] - m[1] + +m[2]) / 6; return [Math.max(x, 2 * x + +m[1], 3 * x - m[2])]; },
    s7_infinitely_many_param: (p) => [+g(/= (\d+)x/, p)[1]],
    s2_equal_outputs: (p) => { const m = g(/f\(x\) = (.*) and g\(x\) = (.*), find/, p), [a, b] = lin(m[1]), [c, d] = lin(m[2]); return [(d - b) / (a - c)]; },
    s2_missing_coordinate: (p) => { const m = g(/\(k, (-?\d+)\) lies on the graph of y = (.*)\. Find/, p), [a, b] = lin(m[2]); return [(m[1] - b) / a]; },
    s9_rate_gap: (p) => { const m = g(/y = (\d+)x pages .* printed (\d+) pages after (\d+) minutes and (\d+) pages after (\d+) minutes.* in (\d+) minutes/, p); return [((m[4] - m[2]) / (m[5] - m[3]) - m[1]) * m[6]]; },
    s9_when_equal: (p) => { const m = g(/A holds (\d+) L and gains (\d+) L .* B holds (\d+) L and gains (\d+) L/, p); return [(m[1] - m[3]) / (m[4] - m[2])]; },
    s10_input_for_value: (p) => { const m = g(/V\(t\) = (\d+) - (\d+)t .* value \$(\d+)\?/, p); return [(m[1] - m[3]) / m[2]]; },
    s10_time_to_zero: (p) => { const m = g(/D\(t\) = (\d+) - (\d+)t/, p); return [m[1] / m[2]]; },
    s11_solve_piecewise: (p) => { const m = g(/f\(x\) = (.*) for x < (-?\d+), and f\(x\) = (.*) for x ≥ -?\d+\. Find every x with f\(x\) = (-?\d+)/, p), k = +m[2], y = +m[4], [a, b] = lin(m[1]), [c, d] = lin(m[3]);
      return [(y - b) / a, (y - d) / c].filter((x, i) => (i ? x >= k : x < k)).sort((u, v) => u - v); },
    s11_sum_of_pieces: (p) => { const m = g(/f\(x\) = (.*) for x < (-?\d+), and f\(x\) = (.*) for x ≥ -?\d+\. Find f\((-?\d+)\) \+ f\((-?\d+)\)/, p), f = (x) => { const [a, b] = lin(x < +m[2] ? m[1] : m[3]); return a * x + b; }; return [f(+m[4]) + f(+m[5])]; },
    s12_gap_over_time: (p) => { const m = g(/fills (\d+) gallons in (\d+) minutes; pump B fills y = (\d+)x .* After (\d+) minutes/, p); return [Math.abs(m[1] / m[2] - m[3]) * m[4]]; },
    s12_reverse_proportion: (p) => { const m = g(/y = (\S+) when x = (\d+)\. Find x when y = (\S+)\./, p); return [ev(m[3]) * m[2] / ev(m[1])]; },
    s1_parallel_then_value: (p) => { const m = g(/through \(0, (-?\d+)\) and is parallel to (.*) = -?\d+\. Find y on the line when x = (\d+)/, p); const [a] = lin(m[2].replace(/[+-]?\s*\d*y/, '')), b = lin(m[2].replace(/^.*?([+-]\s*\d*y)$/, '$1'), 'y')[0]; return [+m[1] - a / b * m[3]]; },
    s3_ages_system: (p) => { const m = g(/p \+ c = (\d+), and in (\d+) years the parent will be (\d+) times/, p); return [(+m[1] + +m[2] - m[3] * m[2]) / (+m[3] + 1)]; },
    s3_x_isolated: (p) => { const m = g(/x = (.*) and (.*) = (-?\d+)$/, p), [a, b] = lin(m[1], 'y'), c = lin(m[2].replace(/[+-]\s*\d*y$/, ''))[0], d = lin(m[2].replace(/^.*?([+-]\s*\d*y)$/, '$1'), 'y')[0]; const y = (m[3] - c * b) / (c * a + d); return [a * y + b, y]; },
    s5_infinite_parameter: (p) => { const m = g(/y = (.*) and (\d+)x - (\d+)y = k/, p), [, b] = lin(m[1]); return [-m[3] * b]; },
    s2_equal_total: (p) => { const m = g(/A: y = (\d+)x \+ (\d+)\. Plan B: y = (\d+)x \+ (\d+)\./, p), x = (m[4] - m[2]) / (m[1] - m[3]); return [m[1] * x + +m[2]]; },
    s2_intersection_parameter: (p) => { const m = g(/y = (.*) \+ k and y = (.*) intersect at a point with x = (-?\d+)/, p), [a] = lin(m[1]), [c, d] = lin(m[2]), x = +m[3]; return [c * x + d - a * x]; },
    s3_direction_from_data: (p) => { const y = nums(g(/y: (.*)\. Is/, p)[1]); return y[y.length - 1] > y[0] ? 'positive' : 'negative'; },
    s3_count_reversals: (p) => { const y = nums(g(/y: (.*?)\. The/, p)[1]); return [y.slice(1).filter((v, i) => v < y[i]).length]; },
    s4_reverse_prediction: (p) => { const m = g(/through \((\d+), (\d+)\) and \((\d+), (\S+)\)\. For what x does it predict y = (\S+)\?/, p), s = (ev(m[4]) - m[2]) / (m[3] - m[1]); return [+m[1] + (ev(m[5]) - m[2]) / s]; },
    s4_actual_minus_predicted: (p) => { const m = g(/y = (\d+)x \+ (\d+) models .* \((\d+), (\d+)\)/, p); return [m[4] - (m[1] * m[3] + +m[2])]; },
    s5_two_unknown_cells: (p) => { const m = g(/(\d+) walk, x take the bus\. Grade 8 — y walk, (\d+) take the bus\. (\d+) students walk and (\d+) take/, p); return [m[4] - m[2] + (m[3] - m[1])]; },
    s5_percent_cells: (p) => { const m = g(/Of (\d+) students, (\d+)% .* (\d+) grade 8 students play a sport, and (\d+) students/, p); return [m[1] - m[1] * m[2] / 100 - (m[4] - m[3])]; },
    s6_percentage_point_gap: (p) => { const m = g(/(\d+) of (\d+) students bring lunch\. Grade 8: (\d+) of (\d+)/, p); return [Math.abs(100 * m[1] / m[2] - 100 * m[3] / m[4])]; },
    s6_column_relative: (p) => { const m = g(/(\d+) are in grade 7 and (\d+) are in grade 8/, p); return [100 * m[2] / (+m[1] + +m[2])]; },
    s2_original_from_image: (p) => { const a = g(/rotation (90° (?:counter)?clockwise)/, p)[1], q = pt(p.split('M′')[1]); const back = a === '90° clockwise' ? rot['90° counterclockwise'] : rot['90° clockwise']; return back(q); },
    s2_two_rotations: (p) => { const m = g(/rotated (\S+(?: \S*clockwise)?) about the origin, then the image is rotated (\S+(?: \S*clockwise)?) about/, p); return rot[m[2]](rot[m[1]](pt(p))); },
    s3_mirror_y_equals: (p) => { const [x, y] = pt(p), k = +g(/y = (-?\d+)/, p)[1]; return [x, 2 * k - y]; },
    s3_mirror_x_equals: (p) => { const [x, y] = pt(p), k = +g(/x = (-?\d+)/, p)[1]; return [2 * k - x, y]; },
    s4_reverse_then_reflect: (p) => { const m = g(/translated (\d+) units left and (\d+) units (up|down)/, p), [x, y] = pt(p.split('final image is')[1]); return [-x + +m[1], y + (m[3] === 'up' ? -1 : 1) * m[2]]; },
    s4_rule_then_apply: (p) => { const [a, b] = pt(p.split('maps A')[1]), [c, d] = pt(p.split('to A′')[1]), [e, f] = pt(p.split('map B')[1]); return [e + c - a, f + d - b]; },
    s5_area_scale: (p) => { const m = g(/area (\d+) square units.* scale factor (\S+)\./, p); return [m[1] * ev(m[2]) ** 2]; },
    s5_center_not_origin: (p) => { const [x, y] = pt(p), k = ev(g(/scale factor (\S+) centered/, p)[1]), [cx, cy] = pt(p.split('centered at C')[1]); return [cx + k * (x - cx), cy + k * (y - cy)]; },
    s6_parallel_mirrors: (p) => { const m = g(/x = (-?\d+) and then over the line x = (-?\d+)/, p); return [2 * (m[2] - m[1])]; },
    s7_exterior_multiple: (p) => { const k = +g(/is (\d+) times/, p)[1]; return [180 * k / (k + 1)]; },
    s7_angle_ratio: (p) => { const m = g(/ratio (\d+) : (\d+) : (\d+)/, p); return [180 * Math.max(m[1], m[2], m[3]) / (+m[1] + +m[2] + +m[3])]; },
    s9_alternate_exterior_pair: (p) => { const m = g(/∠1 = \((.*)\)° and ∠8 = \((.*)\)°/, p), [a, b] = lin(m[1]), [c, d] = lin(m[2]), x = (d - b) / (a - c); return [180 - (a * x + b)]; },
    s9_same_side_find: (p) => { const m = g(/measure \((.*)\)° and \((.*)\)°/, p), [a, b] = lin(m[1]), [c, d] = lin(m[2]), x = (180 - b - d) / (a + c); return [Math.max(a * x + b, c * x + d)]; },
    s1_isosceles_right: (p) => [+g(/legs of length (\d+)/, p)[1], 2],
    s1_acute_obtuse: (p) => { const m = g(/sides (\d+), (\d+) and (\d+)\./, p); return m[1] ** 2 + m[2] ** 2 > m[3] ** 2 ? 'acute' : 'obtuse'; },
    s2_diagonal_from_perimeter: (p) => { const m = g(/perimeter (\d+) cm and one side of (\d+) cm/, p), b = m[1] / 2 - m[2]; return [Math.hypot(m[2], b)]; },
    s2_ladder_slides: (p) => { const m = g(/A (\d+)-ft ladder .* base (\d+) ft from the wall\. The top slides down (\d+) ft/, p), h = Math.sqrt(m[1] ** 2 - m[2] ** 2) - m[3]; return [Math.sqrt(m[1] ** 2 - h * h) - m[2]]; },
    s3_box_missing_edge: (p) => { const m = g(/(\d+) m by (\d+) m, and its space diagonal is (\d+) m/, p); return [Math.sqrt(m[3] ** 2 - m[1] ** 2 - m[2] ** 2)]; },
    s3_cube_diagonal: (p) => [+g(/length (\d+) cm/, p)[1], 3],
    s6_equal_volume_cone: (p) => [3 * g(/height (\d+) cm/, p)[1]],
    s6_height_multiple: (p) => { const m = g(/is (\d+) times its radius, and its volume is (\d+)π/, p); return [Math.round(Math.cbrt(m[2] / m[1]) * 1e9) / 1e9]; },
  };
  const close = (u, v) => u.length === v.length && u.every((x, i) => Math.abs(x - v[i]) < 1e-9);
  for (const q of D) {
    const f = fam(q), fn = R[f];
    check(q, !!fn, 'no recomputation for family ' + f);
    if (!fn) continue;
    let want; try { want = fn(q.prompt); } catch (e) { check(q, false, e.message); continue; }
    const a = String(q.answer);
    if (typeof want === 'string') check(q, a === want, 'recomputed ' + want + ' but key ' + a);
    else check(q, close(want, nums(a)), 'recomputed ' + want.join(', ') + ' but key ' + a);
    for (const s of q.solutionSteps) check(q, !/\+ -|- -|(?<![\d.])1[xy]\b|  /.test(s), 'step formatting: ' + s);
    if (q.options) check(q, q.options.filter((o) => o.correct).length === 1 && q.options.find((o) => o.correct).text === a && new Set(q.options.map((o) => o.text)).size === q.options.length, 'options');
  }
  for (const sk of new Set(D.map((q) => q.skillId))) {
    const lower = new Set(Q.filter((q) => q.skillId === sk && q.level !== 'honors').map((q) => mask(q.prompt)));
    const adv = Q.filter((q) => q.skillId === sk && q.level === 'honors' && q.format !== 'plot');
    for (const q of D.filter((q) => q.skillId === sk)) check(q, !lower.has(mask(q.prompt)), 'new Advanced item reuses a lower template');
    check({ id: sk }, adv.filter((q) => q.format === 'multiple-choice').length >= 6, 'Advanced multiple choice for games');
  }
  const all = Q.filter((q) => q.level === 'honors' && q.format !== 'plot');
  const lowerAll = new Set(Q.filter((q) => q.level !== 'honors').map((q) => q.skillId + '|' + mask(q.prompt)));
  const share = all.filter((q) => lowerAll.has(q.skillId + '|' + mask(q.prompt))).length / all.length;
  check(null, share <= 0.25, 'Advanced items reusing a lower template: ' + (100 * share).toFixed(1) + '%');
  check(null, Q.filter((q) => /batch D move/.test(q.sourceNotes || '')).every((q) => q.level === 'cp1'), 'batch D moved items are Standard');
}
/* #14 follow-up (batch E): Standard items rewritten from Support templates with an added step, every key recomputed */
{
  const mask = (t) => t.replace(/-?\d+(\.\d+)?/g, '#');
  const E = Q.filter((q) => /\(Standard, batch E\)/.test(q.sourceNotes || ''));
  check(null, E.length >= 400, 'batch E Standard items ' + E.length);
  const SUP = { '⁻': '-', '⁰': '0', '¹': '1', '²': '2', '³': '3', '⁴': '4', '⁵': '5', '⁶': '6', '⁷': '7', '⁸': '8', '⁹': '9' };
  const ev = (s) => { s = String(s).replace(/[()\s]/g, ''); const p = s.split('/'); return p.length === 2 ? +p[0] / +p[1] : +s; };
  const nums = (s) => (String(s).replace(/([x0-9])([⁻⁰¹²³⁴⁵⁶⁷⁸⁹]+)/g, (m, b, e) => b + '^' + [...e].map((c) => SUP[c]).join('')).match(/-?\d+(\.\d+)?(\/\d+)?/g) || []).map(ev);
  const lin = (s, v = 'x') => { let m = 0, b = 0; for (const t of s.replace(/\s+/g, '').split(/(?=[+-])/)) { if (!t) continue; if (t.includes(v)) { const c = t.replace(v, '').replace(/[()]/g, ''); m += c === '' || c === '+' ? 1 : c === '-' ? -1 : ev(c); } else b += ev(t); } return [m, b]; };
  const two = (s) => { const [l, r] = s.split(' = '), y = /([+-]?\s*\d*)y/.exec(l), a = lin(l.replace(/[+-]?\s*\d*y/, ''))[0]; const bs = y[1].replace(/\s/g, ''); return [a, bs === '' || bs === '+' ? 1 : bs === '-' ? -1 : +bs, +r]; };
  const pts = (s) => [...s.matchAll(/\((-?\d+), (-?\d+(?:\/\d+)?)\)/g)].map((m) => [+m[1], ev(m[2])]);
  const g = (re, s) => { const m = re.exec(s); if (!m) throw new Error('prompt shape: ' + re); return m; };
  const list = (s) => s.split(', ').map(Number);
  const R = {
    s1_integers_between_fractions: (p) => { const m = g(/between (\S+) and (\S+) on/, p); return [Math.floor(ev(m[2])) - Math.ceil(ev(m[1])) + 1]; },
    s2_order_of_operations: (p) => { const m = g(/Evaluate: (\S+) \+ (\S+) × \((\S+)\)/, p); return [ev(m[1]) + ev(m[2]) * ev(m[3])]; },
    s3_convert_then_add: (p) => { const m = g(/Write (\d+)\/(\d+) as a decimal, then add (\d+\.\d+)/, p); return [+(m[1] / m[2] + +m[3]).toFixed(10)]; },
    s4_count_irrational_list: (p) => [g(/irrational: (.*)\?$/, p)[1].split(', ').filter((t) => /π|√(8|50|12|20)\b|√2 \+ 1/.test(t)).length],
    s5_simplify_then_add: (p) => { const m = g(/√(\d+) · √(\d+) ([+-]) (\d+)/, p); return [Math.sqrt(m[1] * m[2]) + (m[3] === '-' ? -1 : 1) * m[4]]; },
    s7_area_to_perimeter: (p) => [4 * Math.sqrt(+g(/area of (\d+)/, p)[1])],
    s8_negative_plus_zero: (p) => { const m = nums(g(/Evaluate: (.*)$/, p)[1]); return [m[0] ** m[1] + 1]; },
    s10_normalize_large: (p) => { const m = nums(g(/Write (.*) in scientific/, p)[1]), v = m[0] * 10 ** m[2], e = Math.floor(Math.log10(v) + 1e-9); return [+(v / 10 ** e).toPrecision(10), 10, e]; },
    s11_divide_context: (p) => { const m = nums(g(/budget of (.*) dollars is shared equally by (.*) households/, p).slice(1).join(' ; ')); return [m[0] / m[3], 10, m[2] - m[5]]; },
    s2_power_then_product: (p) => { const m = g(/\((-?\d+)x\)(\S) · x(\S?)$/, p), e = +SUP[m[2]], f = m[3] ? +SUP[m[3]] : 1; return [(+m[1]) ** e, e + f]; },
    s3_sentence_then_solve: (p) => { const m = g(/^(\d+) (less|more) than (\d+) times a number is (\d+)/, p); return [(m[2] === 'less' ? +m[4] + +m[1] : m[4] - m[1]) / m[3]]; },
    s3_cost_then_solve: (p) => { const m = g(/\$(\d+) fee plus \$(\d+) per hour\. A family paid \$(\d+)/, p); return [(m[3] - m[1]) / m[2]]; },
    s4_distribute_both_sides: (p) => { const m = g(/Solve: (\d+)\(x - (\d+)\) ([+-]) (\d+) = (.*)$/, p), [d, e] = lin(m[5]), c = (m[3] === '-' ? -1 : 1) * m[4]; return [(e + m[1] * m[2] - c) / (m[1] - d)]; },
    s5_parentheses_two_step: (p) => { const m = g(/Solve: (\d+)\(x \+ (\d+)\) - (\d+) = (-?\d+)/, p); return [(+m[4] + +m[3]) / m[1] - m[2]]; },
    s6_distribute_then_combine: (p) => { const m = g(/Simplify: (-?\d+)\(x ([+-]) (\d+)\) ([+-]) (\d*)x - (\d+)/, p), a = +m[1], b = (m[2] === '-' ? -1 : 1) * m[3], c = (m[4] === '-' ? -1 : 1) * (m[5] === '' ? 1 : +m[5]); return [a + c, a * b - m[6]]; },
    s8_cube_two_step: (p) => { const m = g(/x³ - (\d+) = (-?\d+)/, p); return [Math.round(Math.cbrt(+m[2] + +m[1]))]; },
    s1_rule_then_evaluate: (p) => { const m = g(/y: (.*)\. Write a rule, then find y when x = (\d+)/, p), y = list(m[1]); return [y[0] + (y[1] - y[0]) * m[2]]; },
    s2_difference_of_values: (p) => { const m = g(/f\(x\) = (.*), find f\((-?\d+)\) - f\((-?\d+)\)/, p), [a] = lin(m[1]); return [a * (m[2] - m[3])]; },
    s3_complete_linear_table: (p) => { const y = g(/y: (.*)\. What/, p)[1].split(', '), k = y.indexOf('?'), i = k > 1 ? 0 : 2, j = k > 1 ? 1 : 3, d = (y[j] - y[i]) / (j - i); return [+y[i] + d * (k - i)]; },
    s4_slope_from_points: (p) => { const [[a, b], [c, d]] = pts(p); return [(d - b) / (c - a)]; },
    s5_equation_two_points: (p) => { const [[a, b], [c, d]] = pts(p), m = (d - b) / (c - a); return [m, b - m * a]; },
    s6_x_intercept_of_line: (p) => { const [m, b] = lin(g(/y = (.*)\.$/, p)[1]); return [-b / m, 0]; },
    s7_rule_from_two_values: (p) => { const m = g(/f\((\d+)\) = (-?\d+) and f\((\d+)\) = (-?\d+)/, p), s = (m[4] - m[2]) / (m[3] - m[1]); return [s, m[2] - s * m[1]]; },
    s8_max_on_interval: (p) => { const m = g(/f\(x\) = (.*) on the interval from x = (-?\d+) to x = (-?\d+)/, p), [a, b] = lin(m[1]); return [Math.max(a * m[2] + b, a * m[3] + b)]; },
    s9_initial_from_two: (p) => { const m = g(/had (\d+) gallons after (\d+) hours? and (\d+) gallons after (\d+) hours/, p), r = (m[3] - m[1]) / (m[4] - m[2]); return [m[1] - r * m[2]]; },
    s10_input_from_total: (p) => { const m = g(/C\(n\) = (\d+)n \+ (\d+) .* cost \$(\d+)\?/, p); return [(m[3] - m[2]) / m[1]]; },
    s11_value_at_boundary: (p) => { const m = g(/for x ≥ (-?\d+)\. Find/, p), k = +m[1], [c, d] = lin(g(/and f\(x\) = (.*) for x ≥/, p)[1]); return [c * k + d]; },
    s12_rate_then_predict: (p) => { const m = g(/travels (\d+) miles in (\d+) hours .* in (\d+) hours/, p); return [m[1] / m[2] * m[3]]; },
    s1_y_intercept_standard_form: (p) => { const [a, b, c] = two(g(/graph of (.*)\?$/, p)[1]); return [0, c / b]; },
    s3_isolate_then_substitute: (p) => { const m = g(/substitution: (.*) and (.*)$/, p), [a, b, c] = two(m[1]), [d, e, f] = two(m[2]), D = a * e - b * d; return [(c * e - b * f) / D, (a * f - c * d) / D]; },
    s4_add_to_eliminate: (p) => { const m = g(/elimination: (.*) and (.*)$/, p), [a, b, c] = two(m[1]), [d, e, f] = two(m[2]), D = a * e - b * d; return [(c * e - b * f) / D, (a * f - c * d) / D]; },
    s5_multiply_and_compare: (p) => { const m = g(/system (.*) and (.*) have/, p), [a, b, c] = two(m[1]), [d, e, f] = two(m[2]); return Math.abs(a * e - b * d) > 1e-9 ? 'one solution' : Math.abs(c * d - a * f) < 1e-9 ? 'infinitely many solutions' : 'no solution'; },
    s6_tickets_then_compare: (p) => { const m = g(/sold (\d+) tickets for \$(\d+)\. Adult tickets cost \$(\d+) and child tickets cost \$(\d+)/, p), A = (m[2] - m[4] * m[1]) / (m[3] - m[4]), C = m[1] - A; return [m[3] * A - m[4] * C]; },
    s2_count_two_conditions: (p) => { const m = g(/hours studied: (.*); test score: (.*)\. How many students studied more than (\d+) hours and scored above (\d+)/, p), x = list(m[1]), y = list(m[2]); return [x.filter((v, i) => v > +m[3] && y[i] > +m[4]).length]; },
    s3_change_and_direction: (p) => { const y = list(g(/y: (.*?)\. By how much/, p)[1]), d = y[y.length - 1] - y[0]; return d + ', ' + (d > 0 ? 'positive' : 'negative'); },
    s4_fit_line_equation: (p) => { const [[a, b], [c, d]] = pts(p), m = (d - b) / (c - a); return [m, b]; },
    s4_two_predictions: (p) => { const m = g(/y = (\d+)x \+ \d+\. How much greater is the prediction for x = (\d+) than the prediction for x = (\d+)/, p); return [m[1] * (m[2] - m[3])]; },
    s5_column_total_from_rows: (p) => { const m = g(/and (\d+) do not\. Grade 8 has (\d+) students, and (\d+) of them/, p); return [+m[1] + (m[2] - m[3])]; },
    s6_row_percent: (p) => { const m = g(/boys: (\d+) have a pet, (\d+) have no pet/, p); return [100 * m[1] / (+m[1] + +m[2])]; },
    s1_rigid_length: (p) => { const [[, b], [, c]] = pts(p); return [Math.abs(c - b)]; },
    s1_reflect_then_translate: (p) => { const [[x, y]] = pts(p), ax = g(/over the (x|y)-axis/, p)[1], h = +g(/translated (\d+) units left/, p)[1]; return ax === 'x' ? [x - h, -y] : [-x - h, y]; },
    s2_rotate_then_translate: (p) => { const [[x, y]] = pts(p), h = +g(/translated (\d+) units right/, p)[1]; return [y + h, -x]; },
    s3_reflect_both_axes: (p) => { const [[x, y]] = pts(p); return [-x, -y]; },
    s4_two_translations: (p) => { const [[x, y]] = pts(p), m = g(/translated (\d+) units right and (\d+) units up, and then (\d+) units left and (\d+) units down/, p); return [x + +m[1] - m[3], y + +m[2] - m[4]]; },
    s5_image_perimeter: (p) => { const m = g(/is (\d+) cm long and (\d+) cm wide\. It is dilated with scale factor (\S+)\./, p); return [2 * (+m[1] + +m[2]) * ev(m[3])]; },
    s5_dilate_then_translate: (p) => { const [[x, y]] = pts(p), m = g(/scale factor (\d+) centered at the origin, then translated (\d+) units down/, p); return [m[1] * x, m[1] * y - m[2]]; },
    s8_similar_two_sides: (p) => { const m = g(/sides (\d+), (\d+) and (\d+)\. A similar triangle DEF has shortest side (\S+)\./, p); return [m[3] * ev(m[4]) / m[1]]; },
    s1_legs_then_perimeter: (p) => { const m = g(/legs (\d+) \S+ and (\d+)/, p); return [+m[1] + +m[2] + Math.hypot(m[1], m[2])]; },
    s1_leg_then_area: (p) => { const m = g(/hypotenuse of (\d+) m and one leg of (\d+) m/, p); return [m[2] * Math.sqrt(m[1] ** 2 - m[2] ** 2) / 2]; },
    s2_shortcut_saved: (p) => { const m = g(/park is (\d+) m by (\d+) m/, p); return [+m[1] + +m[2] - Math.hypot(m[1], m[2])]; },
    s3_slant_then_volume: (p) => { const m = g(/radius (\d+) cm and slant height (\d+) cm/, p); return [m[1] ** 2 * Math.sqrt(m[2] ** 2 - m[1] ** 2) / 3]; },
    s4_perimeter_on_grid: (p) => { const [[a, b], [c], [, d]] = pts(p), u = c - a, v = d - b; return [u + v + Math.hypot(u, v)]; },
    s5_cylinder_from_diameter: (p) => { const m = g(/diameter of (\d+) inches and a height of (\d+)/, p); return [(m[1] / 2) ** 2 * m[2]]; },
    s5_cone_from_diameter: (p) => { const m = g(/diameter of (\d+) feet and a height of (\d+)/, p); return [(m[1] / 2) ** 2 * m[2] / 3]; },
    s6_cylinder_radius: (p) => { const m = g(/volume (\d+)π cubic cm and height (\d+)/, p); return [Math.sqrt(m[1] / m[2])]; },
    s6_cone_radius: (p) => { const m = g(/holds (\d+)π cubic cm and is (\d+) cm tall/, p); return [Math.sqrt(3 * m[1] / m[2])]; },
    s7_cylinder_minus_cone: (p) => { const m = g(/radius (\d+) cm and height (\d+) cm/, p); return [2 * m[1] ** 2 * m[2] / 3]; },
    s7_cone_with_scoop: (p) => { const m = g(/radius (\d+) cm, height (\d+) cm/, p); return [m[1] ** 2 * m[2] / 3 + 2 * m[1] ** 3 / 3]; },
    s9_alt_interior_pair: (p) => [180 - g(/∠3 = (\d+)°/, p)[1]],
    s9_corresponding_solve: (p) => { const m = g(/measure \((.*)\)° and \((.*)\)°/, p), [a, b] = lin(m[1]), [c, d] = lin(m[2]), x = (d - b) / (a - c); return [x, a * x + b]; },
  };
  const close = (u, v) => u.length === v.length && u.every((x, i) => Math.abs(x - v[i]) < 1e-6);
  const cp2 = new Set(Q.filter((q) => q.level === 'cp2').map((q) => q.skillId + '|' + mask(q.prompt)));
  const hon = new Set(Q.filter((q) => q.level === 'honors').map((q) => q.skillId + '|' + mask(q.prompt)));
  for (const q of E) {
    const f = fam(q), fn = R[f];
    check(q, !!fn, 'no recomputation for family ' + f);
    check(q, q.level === 'cp1' && !cp2.has(q.skillId + '|' + mask(q.prompt)) && !hon.has(q.skillId + '|' + mask(q.prompt)), 'batch E item reuses a Support or Advanced template');
    if (!fn) continue;
    let want; try { want = fn(q.prompt); } catch (e) { check(q, false, e.message); continue; }
    const a = String(q.answer);
    if (typeof want === 'string') check(q, a === want, 'recomputed ' + want + ' but key ' + a);
    else check(q, close(want, /^(s6_distribute_then_combine|s5_equation_two_points|s7_rule_from_two_values|s4_fit_line_equation)$/.test(f) ? lin(a.replace(/^y = /, '')) : nums(a)), 'recomputed ' + want.join(', ') + ' but key ' + a);
    for (const s of q.solutionSteps) check(q, !/\+ -|- -|(?<![\d.])1[xy]\b|  |\b1 (hours|minutes|weeks)\b/.test(s), 'step formatting: ' + s);
    if (q.options) check(q, q.options.filter((o) => o.correct).length === 1 && q.options.find((o) => o.correct).text === a && new Set(q.options.map((o) => o.text)).size === q.options.length, 'options');
  }
  const S = Q.filter((q) => q.level === 'cp1' && q.format !== 'plot');
  const share = S.filter((q) => cp2.has(q.skillId + '|' + mask(q.prompt))).length / S.length;
  check(null, share <= 0.15, 'Standard items reusing a Support template: ' + (100 * share).toFixed(1) + '%');
}
/* #1 the lesson planner has teaching notes for every 8th Grade Math skill */
{
  const w = { console, Math, Date, JSON }; w.window = w; w.globalThis = w; vm.createContext(w);
  for (const rel of ['data.js', 'course-catalog.js', 'worksheet-generator/menu/standards.js', 'worksheet-generator/menu/standards-map.js',
    'worksheet-generator/planner/notes-teach-prealgebra.js', 'worksheet-generator/planner/scope-algebra2.js'])
    vm.runInContext(fs.readFileSync(path.join(ROOT, rel), 'utf8'), w, { filename: rel });
  const N = w.MKPLAN_TEACH.prealgebra, course = w.LIBRARY.courses.find((c) => c.id === 'prealgebra');
  let skills = 0;
  for (const u of course.units) for (const s of w.MK_COURSE_CATALOG.getSkillRecords('prealgebra', u.id)) {
    skills++;
    const r = N[s.id];
    assert(r && r.obj && !/^work with /.test(r.obj) && r.idea.length > 40 && r.watch, 'teaching notes for ' + s.id);
    assert(Array.isArray(r.voc) && r.voc.length >= 3 && r.voc.every((v) => v[0] && v[1]), s.id + ' vocabulary');
    assert(r.cards.length >= 1 && r.cards.every((c) => c.h && c.big && c.steps.length >= 3 && c.steps.some((x) => /\{\{/.test(x))), s.id + ' card with blanks');
  }
  assert.equal(skills, 59);
  assert.equal(Object.keys(N).length, skills, 'no notes outside the catalog');
  const lessons = w.MKPLAN_SCOPE_PREALGEBRA.days.filter((d) => d.day_type === 'Lesson');
  assert.equal(lessons.length, skills);
  for (const d of lessons) assert(!/able to work with /.test(d.content_objective) && d.key_vocabulary && d.common_misconception, d.lesson_id + ' planner fields');
  const html = fs.readFileSync(path.join(ROOT, 'worksheet-generator/lesson-planner.html'), 'utf8');
  assert(html.indexOf('planner/notes-teach-prealgebra.js') > 0 && html.indexOf('planner/notes-teach-prealgebra.js') < html.indexOf('planner/scope-algebra2.js'), 'planner page loads the Grade 8 notes first');
  assert(/course\(\) === 'prealgebra'/.test(fs.readFileSync(path.join(ROOT, 'worksheet-generator/planner/notes-teach.js'), 'utf8')), 'notes-teach.js uses the Grade 8 vocabulary and key ideas');
}
/* #2 pacing guide and standards coverage page */
(async () => {
  const G = await import(path.join(ROOT, 'scripts/geo-planning.mjs'));
  assert(G.planningCourses.includes('prealgebra') && G.planningPage('prealgebra') === '8th-grade-math-pacing/', 'pacing page');
  const h = G.geoPacingMain('prealgebra', (t) => '#' + t);
  assert(/31 of 31 standards have question-bank practice/.test(h), 'every Grade 8 standard is practised');
  assert(/Day|days/.test(h) && /Final Exam|Final review/i.test(h), 'full-year plan');
  const ug = G.geoUnitGuide('Real Numbers and Exponents', 'prealgebra');
  assert(ug.includes('Teaching Unit 1') && !/Students work with/.test(ug) && ug.includes('A rational number can be written'), 'unit briefing uses the teaching notes');
  /* #7 labs for 8th-grade standards are listed in the Grade 8 units */
  const d = { console, document: { addEventListener() {}, querySelector() { return null; }, querySelectorAll() { return []; } }, location: { hash: '', search: '' }, localStorage: { getItem() { return null; }, setItem() {} } };
  d.window = d; d.self = d; d.globalThis = d; vm.createContext(d);
  for (const f of ['course-catalog.js', 'data.js']) vm.runInContext(fs.readFileSync(path.join(ROOT, f), 'utf8'), d, { filename: f });
  const course = d.LIBRARY.courses.find((c) => c.id === 'prealgebra'), has = (u, p) => course.units.find((x) => x.id === u).artifacts.some((a) => a.path === p);
  for (const [u, p] of [['congruence-similarity', 'artifacts/geometry-parallel-lines-transversal/index.html'], ['geometry-applications', 'artifacts/geometry-solids-volume-lab/index.html'],
    ['linear-functional-relationships', 'artifacts/prealgebra7-proportional-relationships/index.html'], ['linear-functional-relationships', 'artifacts/exponential-functions-linear-vs-exponential/index.html']])
    assert(has(u, p), u + ' lists ' + p);

  if (fails.length) { console.error(fails.length + ' failures:\n' + fails.slice(0, 60).join('\n')); process.exit(1); }
  console.log('PASS 8th Grade Math audit (' + checks + ' item checks)');
})().catch((e) => { console.error(e); process.exit(1); });
