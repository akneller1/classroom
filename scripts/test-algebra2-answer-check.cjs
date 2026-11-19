'use strict';
// Algebra 2 practice tests grade short answers automatically when the key is a number, ordered pair, list of
// x-values or no solution / all real numbers (Algebra 2 audit, 2026-11-17, item 1). Expressions stay self-checked.
const assert = require('node:assert/strict');
const fs = require('node:fs'), path = require('node:path'), vm = require('node:vm');
const ROOT = path.join(__dirname, '..'), WG = path.join(ROOT, 'worksheet-generator');
const ctx = {}; ctx.window = ctx; vm.createContext(ctx);
for (const f of ['menu/mathcheck.js', 'practice/radical-grading.js', 'practice/grading.js']) vm.runInContext(fs.readFileSync(path.join(WG, f), 'utf8'), ctx, { filename: f });
const P = ctx.MKPRACTICE;
const manifest = JSON.parse(fs.readFileSync(path.join(ROOT, 'question-banks/manifest.json'), 'utf8'));
const shortAnswers = manifest.banks.filter(b => b.courseId === 'algebra2')
  .flatMap(b => JSON.parse(fs.readFileSync(path.join(ROOT, b.path), 'utf8')).questions).filter(q => q.format === 'short-answer');
let auto = 0, rejected = 0;
for (const q of shortAnswers) {
  if (P.bankAnswer(q.answer) === null) continue;
  auto++;
  assert.equal(P.gradeBank(q.answer, q.answer).status, 'correct', q.id + ' key grades as correct: ' + q.answer);
  const wrong = q.answer.replace(/(\d+)(?!.*\d)/, d => String(+d + 1));
  if (wrong !== q.answer) { assert.notEqual(P.gradeBank(q.answer, wrong).status, 'correct', q.id + ' rejects ' + wrong); rejected++; }
  if (/^-?\d/.test(q.answer.replace(/^x = /, '')) && !/or/.test(q.answer)) {
    const flipped = q.answer.replace(/^(x = )?(-?)/, (m, x, s) => (x || '') + (s ? '' : '-'));
    if (!/^(x = )?-?0(\.0*)?\b/.test(q.answer)) assert.notEqual(P.gradeBank(q.answer, flipped).status, 'correct', q.id + ' rejects sign flip');
  }
}
assert(auto >= 1100, 'at least 1,100 Algebra 2 short answers are graded automatically (got ' + auto + ')');
const cases = [
  ['24 years', '24', 'correct'], ['24 years', '24 years', 'correct'], ['24 years', '25', 'incorrect'],
  ['$1,647.01', '1647.01', 'correct'], ['$1,647.01', '$1,647.01', 'correct'], ['$1,647.01', '1647', 'incorrect'],
  ['40,320', '40320', 'correct'], ['x = 101/2', '50.5', 'correct'], ['x = 101/2', 'x = 50.5', 'correct'],
  ['(5, 2)', '(5,2)', 'correct'], ['(5, 2)', '(2, 5)', 'incorrect'],
  ['x = 1 or x = 5', 'x = 5 or x = 1', 'correct'], ['x = 1 or x = 5', 'x = 1', 'invalid'],
  ['no solution', 'No solution', 'correct'], ['1/4', '0.25', 'correct'], ['34%', '34', 'correct']];
for (const [key, typed, want] of cases) assert.equal(P.gradeBank(key, typed).status, want, key + ' / ' + typed);
// Never auto-grade expressions, approximations or prose: equivalence would accept an unfactored answer to "Factor ...".
for (const key of ['(x + 3)(x - 5)', '4x² + 2x - 2', 'y = 200(0.5)^x', 'x = ln 12 ≈ 2.485', 'parabola', '2 ft above the vertex',
  'center (1, 2); vertices (1, 2 ± √13)', 'x = -3 ± 4√3', 'y = 2']) assert.equal(P.bankAnswer(key), null, 'self-check for ' + key);
const practice = fs.readFileSync(path.join(WG, 'practice/practice.js'), 'utf8');
assert(/bankAnswer\(q\.answer(?:,q\.prompt)?\)!==null\?'auto'/.test(practice) && /q\.bank\?G\.MKPRACTICE\.gradeBank/.test(practice), 'practice test uses the bank grader');
console.log('PASS Algebra 2 short-answer auto-check: ' + auto + ' of ' + shortAnswers.length + ' short answers graded; ' + rejected + ' wrong variants rejected');
