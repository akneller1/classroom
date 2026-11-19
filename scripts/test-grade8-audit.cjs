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
/* #15 every skill has open-response items (the 23 skills that had none now have one per level) */
{
  const sk = [...new Set(Q.map((q) => q.skillId))];
  for (const s of sk) check({ id: s }, Q.some((q) => q.skillId === s && q.format === 'open-response' && q.parts.length >= 4), 'no open-response item');
  for (const q of Q.filter((q) => /-o01$/.test(q.id))) check(q, q.format === 'open-response' && q.parts.length >= 4 && q.solutionSteps.length === q.parts.length, 'new open-response item');
  assert.equal(Q.filter((q) => /-o01$/.test(q.id)).length, 69);
  const o = (id) => byId[id].parts.map((p) => p.answer);
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
  const H = Q.filter((q) => /-honors-h0\d$/.test(q.id));
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
