#!/usr/bin/env node
/* Grade 5 audit (2026-11-19), Classroom side of batch 5A: #2 and #3, the shared practice-test grader on Grade 5 answers.
   Fixed cases always run. When GRADE5_SOURCE_DIR (or ../FinancialAlgebra) holds the Grade 5 source, every Grade 5 short-answer
   key must also be auto-graded and grade itself correct; every other course's keys must still grade themselves correct. */
'use strict';
const fs = require('fs'), vm = require('vm'), path = require('path'), assert = require('assert/strict');
const ROOT = path.resolve(__dirname, '..'), rd = (f) => fs.readFileSync(path.join(ROOT, f), 'utf8');
const c = {}; c.window = c; vm.createContext(c);
for (const f of ['menu/mathcheck.js', 'practice/radical-grading.js', 'practice/exact-grading.js', 'practice/calculus-grading.js', 'practice/stat-grading.js', 'practice/grading.js'])
  vm.runInContext(rd('worksheet-generator/' + f), c, { filename: f });
const P = c.MKPRACTICE, g = (k, t, p) => P.gradeBank(k, t, p || '').status;
const SIMP = 'Write 10/15 in simplest form.', SIX = 'Write 6/4 in simplest form.', TRI = 'Classify the triangle by its angles: acute, right, or obtuse?';
const cases = [
  ['2/3', '4/6', SIMP, 'invalid'], ['2/3', '2/3', SIMP, 'correct'], ['2/3', '0.6', SIMP, 'incorrect'], ['1 1/2', '3/2', SIX, 'correct'], ['1 1/2', '6/4', SIX, 'invalid'], ['1 1/2', '1 2/4', SIX, 'invalid'],
  ['4 1/4', '17/4', 'Write the answer as a mixed number.', 'invalid'], ['4 1/4', '4 1/4', 'Write the answer as a mixed number.', 'correct'],
  ['greater than', '>', 'Is 3/4 + 5/12 greater than 1 or less than 1?', 'correct'], ['greater than 1', '> 1', 'Is 3/5 + 4/7 greater than 1 or less than 1?', 'correct'],
  ['less than', 'greater than', '', 'incorrect'], ['<', 'less than', 'Which symbol makes 0.4 ___ 0.45 true?', 'correct'],
  ['90 R 2', '90 remainder 2', 'Find the quotient and remainder: 452 ÷ 5.', 'correct'], ['90 R 2', '90 r 2', '', 'correct'], ['90 R 2', '90 R 3', '', 'incorrect'], ['90 R 2', '90', '', 'invalid'],
  ['5 feet 3 inches', '5 ft 3 in', '', 'correct'], ['5 feet 3 inches', '5 feet 4 inches', '', 'incorrect'], ['5 feet 3 inches', '63 inches', '', 'invalid'],
  ['32 cubic units', '32', '', 'correct'], ['32 cubic units', '32 cu units', '', 'correct'], ['32 cubic units', '32 square units', '', 'incorrect'], ['32 cubic units', '33', '', 'incorrect'],
  ['acute', 'Acute', TRI, 'correct'], ['acute', 'right', TRI, 'incorrect'], ['rhombus', 'square', 'What is the most specific name for this quadrilateral?', 'incorrect'],
  ['the x‑axis', 'x axis', 'On which axis does the point (4, 0) lie?', 'correct'], ['the x‑axis', 'y-axis', 'On which axis does the point (4, 0) lie?', 'incorrect'],
  ['point D', 'D', 'Which point is at (2, 3)?', 'correct'], ['point D', 'point C', 'Which point is at (2, 3)?', 'incorrect'],
  ['1 1/2 inches', '3/2', 'What is the longest length?', 'correct'], ['1 1/2 inches', '1 1/2 feet', 'What is the longest length?', 'incorrect']];
for (const [k, t, p, want] of cases) assert.equal(g(k, t, p), want, `key ${k}, typed ${t}, prompt ${p}`);
assert(/practice\/grading\.js\?v=g5-audit-20261119/.test(rd('worksheet-generator/practice-test.html')), 'grader cache version bumped');

const bank = (dir) => fs.readdirSync(dir).filter((f) => f.endsWith('.json')).flatMap((f) => JSON.parse(fs.readFileSync(path.join(dir, f), 'utf8')).questions || []);
let other = 0;
for (const course of fs.readdirSync(path.join(ROOT, 'question-banks')).filter((d) => fs.statSync(path.join(ROOT, 'question-banks', d)).isDirectory() && d !== 'assets'))
  for (const q of bank(path.join(ROOT, 'question-banks', course)))
    if (q.format === 'short-answer' && typeof q.answer === 'string' && P.bankAnswer(q.answer, q.prompt) !== null) {
      other++; assert.equal(g(q.answer, q.answer, q.prompt), 'correct', q.id + ' key grades itself correct: ' + q.answer);
    }
let msg = `${cases.length} cases; ${other} keys in the other courses still grade themselves correct`;
const src = path.resolve(process.env.GRADE5_SOURCE_DIR || path.join(ROOT, '..', 'FinancialAlgebra'));
if (fs.existsSync(path.join(src, 'math5'))) {
  let sa = 0;
  for (const q of bank(path.join(src, 'math5'))) if (q.format === 'short-answer') {
    sa++;
    assert.notEqual(P.bankAnswer(q.answer, q.prompt), null, q.id + ' is auto-graded: ' + q.answer);
    assert.equal(g(q.answer, q.answer, q.prompt), 'correct', q.id + ' key grades itself correct: ' + q.answer);
  }
  msg += `; all ${sa} Grade 5 short answers auto-graded`;
} else msg += '; Grade 5 source not present, bank sweep skipped';
console.log('PASS Grade 5 audit grading: ' + msg);
