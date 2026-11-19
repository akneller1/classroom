'use strict';
// Calculus audit #2 (2026-11-18): the practice-test grader reads expressions, antiderivatives (+ C), differential-equation
// families, implicit solutions and constants with e, ln and trig (worksheet-generator/practice/calculus-grading.js).
const assert = require('node:assert/strict');
const fs = require('node:fs'), path = require('node:path'), vm = require('node:vm');
const ROOT = path.join(__dirname, '..');
function load(withCalc) {
  const c = {}; c.window = c; vm.createContext(c);
  for (const f of ['worksheet-generator/menu/mathcheck.js', 'worksheet-generator/practice/radical-grading.js', 'worksheet-generator/practice/exact-grading.js']
    .concat(withCalc ? ['worksheet-generator/practice/calculus-grading.js'] : []).concat(['worksheet-generator/practice/grading.js']))
    vm.runInContext(fs.readFileSync(path.join(ROOT, f), 'utf8'), c, { filename: f });
  return c.MKPRACTICE;
}
const P = load(true), OLD = load(false);
const dir = path.join(ROOT, 'question-banks/calculus');
const items = fs.readdirSync(dir).filter(f => f.endsWith('.json')).flatMap(f => JSON.parse(fs.readFileSync(path.join(dir, f), 'utf8')).questions);
const sa = items.filter(q => q.format === 'short-answer'), auto = sa.filter(q => P.bankAnswer(String(q.answer)) !== null);
assert(auto.length >= 1800, 'auto-graded Calculus short answers: ' + auto.length);
for (const q of auto) assert.equal(P.gradeBank(String(q.answer), String(q.answer), q.prompt).status, 'correct', q.id + ' key grades itself correct');
// every wrong multiple-choice option and every find-the-mistake student answer is rejected
for (const q of items.filter(q => q.format === 'multiple-choice' && P.bankAnswer(String(q.answer)) !== null))
  for (const o of q.options) if (!o.correct) assert.notEqual(P.gradeBank(q.answer, o.text, q.prompt).status, 'correct', q.id + ' accepts ' + o.text);
for (const q of items.filter(q => /answered this problem incorrectly/.test(q.prompt) && P.bankAnswer(String(q.answer)) !== null)) {
  const s = /'s answer: (.*)$/m.exec(q.prompt)[1];
  assert.notEqual(P.gradeBank(q.answer, s, q.prompt).status, 'correct', q.id + ' accepts the student answer ' + s);
}
// other courses: every key the new grader takes still grades itself correct
const man = JSON.parse(fs.readFileSync(path.join(ROOT, 'question-banks/manifest.json'), 'utf8')).banks;
for (const b of man) for (const q of JSON.parse(fs.readFileSync(path.join(ROOT, b.path), 'utf8')).questions) {
  if (q.format !== 'short-answer') continue;
  const a = String(q.answer);
  if (P.bankAnswer(a) === null) continue;
  const was = OLD.bankAnswer(a) !== null ? OLD.gradeBank(a, a, q.prompt).status : 'self';
  if (was === 'correct') assert.equal(P.gradeBank(a, a, q.prompt).status, 'correct', q.id + ' key no longer grades itself correct');
}
const cases=[['x⁴ - 5x + C','x^4-5x+C','correct'],['x⁴ - 5x + C','x^4 - 5x + 7 + C','correct'],['x⁴ - 5x + C','x^4-5x','incorrect'],['x⁴ - 5x + C','x^4+5x+C','incorrect'],
['y = Ce^(5x)','y = Ae^(5x)','incorrect'],['y = Ce^(5x)','y=Ce^(5x)','correct'],['y = Ce^(5x)','y = e^(5x+C)','incorrect'],['y = Ce^(5x)','y = e^(5x) + C','incorrect'],
['2y² - x² = C','y^2 - x^2/2 = C','correct'],['2y² - x² = C','2y^2 + x^2 = C','incorrect'],['f′(x) = x⁴(-x + 5)e^(-x)','5x^4e^(-x) - x^5e^(-x)','correct'],['-1 + e⁴','e^4-1','correct'],['-1 + e⁴','53.598','invalid'],
['ln(4)','2ln(2)','correct'],['ln(4)','ln(3)','incorrect'],['128π cm³/s','128pi','correct'],['128π cm³/s','128π cm³/s','correct'],['-∞','-∞','correct'],['-∞','∞','incorrect'],['28 at x = 2','28 at x = 2','correct'],['28 at x = 2','28 at x = -2','incorrect'],
['x = 10 in; V = 16000 in³','x = 10; V = 16000','correct'],['y = 7x + 1','7x+1','correct'],['y = 7x + 1','y = 7x + 8','incorrect'],['-sin(2x)','-2sin(x)cos(x)','correct'],['-sin(2x)','sin(2x)','incorrect'],['Yes','yes','correct'],['Yes','No','incorrect'],
['12 m/s²','12','correct'],['-(2x + y)/(x + 2y)','(-2x-y)/(x+2y)','correct'],['-(2x + y)/(x + 2y)','-2x/(x+2y)','incorrect']];
for (const [k, t, w] of cases) assert.equal(P.gradeBank(k, t).status, w, k + ' <- ' + t);
assert.equal(P.gradeBank('(x - 5)(x - 3)', 'x² - 8x + 15', 'Factor completely: x² - 8x + 15').status, 'incorrect');
assert.equal(P.gradeBank('(x - 5)(x - 3)', '(x-3)(x-5)', 'Factor completely: x² - 8x + 15').status, 'correct');
assert.equal(P.gradeBank('48.6 dollars per item', '48.6 items per dollar').status, 'incorrect');
console.log(`PASS Calculus grading: ${auto.length} of ${sa.length} short answers auto-graded; keys, wrong options and student answers checked`);
