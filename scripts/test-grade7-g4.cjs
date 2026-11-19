#!/usr/bin/env node
/* Grade 7 audit batch G4 (2026-11-19): the leftovers from G1–G3.
   - Grading: a key that is itself unsimplified on purpose ("Which is greater: √18 or 4.1?" → √18) grades itself correct,
     and every Grade 6, 7 and 8 short-answer key that the grader reads grades itself correct.
   - #9: 7.EE.A.2 is practiced in more than one skill.
   - #13: figures for polygons, congruence marks, circles, scale drawings and side-by-side dot plots.
   - #15: the Scale Drawings lab. (Keys of the new items: python3 tools/grade7-audit-20261119/verify_g4.py.) */
'use strict';
const assert = require('assert/strict');
const fs = require('fs'), path = require('path'), vm = require('vm');
const ROOT = path.join(__dirname, '..'), rd = (f) => fs.readFileSync(path.join(ROOT, f), 'utf8');
const bank = (course) => fs.readdirSync(path.join(ROOT, 'question-banks', course)).filter((f) => f.endsWith('.json'))
  .flatMap((f) => JSON.parse(rd(`question-banks/${course}/${f}`)).questions || []);

const c = {}; c.window = c; vm.createContext(c);
for (const f of ['menu/mathcheck.js', 'practice/radical-grading.js', 'practice/exact-grading.js', 'practice/calculus-grading.js', 'practice/stat-grading.js', 'practice/grading.js'])
  vm.runInContext(rd('worksheet-generator/' + f), c, { filename: f });
const P = c.MKPRACTICE, g = (k, t, p) => P.gradeBank(k, t, p || '').status;
for (const [k, t, want] of [['√18', '√18', 'correct'], ['√18', '3√2', 'correct'], ['2√50', '2√50', 'correct'], ['2√50', '√200', 'correct'], ['2√50', '10√2', 'correct'],
  ['√18', '√17', 'incorrect'], ['3√2', '√18', 'invalid'], ['7√3', '√147', 'invalid'], ['7√3', '7√3', 'correct'], ['(√2)/2', '1/√2', 'invalid']])
  assert.equal(g(k, t), want, `key ${k}, typed ${t}`);
let n = 0;
for (const course of ['math6', 'prealgebra7', 'prealgebra'])
  for (const q of bank(course)) if (q.format === 'short-answer' && typeof q.answer === 'string' && P.bankAnswer(q.answer) !== null) { n++; assert.equal(g(q.answer, q.answer, q.prompt), 'correct', q.id + ' key grades itself correct: ' + q.answer); }

const all = bank('prealgebra7'), fam = (q) => (/family: (\w+)/.exec(q.sourceNotes || '') || [])[1];
const ee2 = new Set(all.filter((q) => q.standards.includes('7.EE.A.2')).map((q) => q.skillId));
assert(ee2.size >= 4, '7.EE.A.2 is practiced in ' + ee2.size + ' skills');
const want = { g7_polygon_angle: 'spatial-thinking-skill-03', g7_polygon_algebra: 'spatial-thinking-skill-03', g7_congruent_marks: 'spatial-thinking-skill-05',
  g7_circle_figure: 'spatial-thinking-skill-06', g7_circle_area_figure: 'area-volume-skill-03', g7_scale_drawing_figure: 'ratios-proportions-percentages-skill-03', g7_dot_plot_compare: 'data-analysis-probability-skill-09' };
let figs = 0;
for (const [f, skill] of Object.entries(want)) {
  const qs = all.filter((q) => fam(q) === f);
  assert(qs.length >= 2 && qs.every((q) => q.skillId === skill), f + ' items in ' + skill);
  for (const q of qs) {
    const d = q.diagram && q.diagram.spec;
    assert(d && fs.statSync(path.join(ROOT, d.src)).size > 3000 && d.alt.length > 40, q.id + ' figure and alt text'); figs++;
    assert(!/\bx\b/.test(q.answer) || /^x = /.test(q.answer), q.id);
  }
}
for (const lv of ['cp2', 'cp1', 'honors']) for (const skill of new Set(Object.values(want)))
  assert(all.some((q) => q.skillId === skill && q.level === lv && q.diagram), skill + ' has a figure at ' + lv);

const M = JSON.parse(rd('tools/grade7-audit-20261119/labs/manifest.json')), t = M.tools.find((x) => x.slug === 'grade7-scale-drawing-lab');
assert(t && t.unit === 'ratios-proportions-percentages', 'scale lab in the manifest');
const html = rd('artifacts/grade7-scale-drawing-lab/index.html');
assert(html.includes(rd('tools/grade7-audit-20261119/labs/src/grade7-scale-drawing-lab.js').trim().slice(0, 200)), 'scale lab page is built from its source');
for (const f of ['worksheet.pdf', 'teacher-key.pdf']) assert(fs.statSync(path.join(ROOT, 'artifacts/grade7-scale-drawing-lab', f)).size > 20000, f);
assert(fs.existsSync(path.join(ROOT, 'thumbs/grade7-scale-drawing-lab.jpg')), 'thumbnail');
const w = { console }; w.window = w; vm.createContext(w); vm.runInContext(rd('data.js'), w);
const unit = w.LIBRARY.courses.find((x) => x.id === 'prealgebra7').units.find((u) => u.id === 'ratios-proportions-percentages');
assert(unit.artifacts.some((a) => a.path === 'artifacts/grade7-scale-drawing-lab/index.html' && a.worksheet && a.answerKey), 'scale lab card');
console.log(`PASS Grade 7 audit G4: radical grading (${n} Grade 6–8 keys grade themselves correct), 7.EE.A.2 in ${ee2.size} skills, ${figs} new figures, Scale Drawings lab`);
