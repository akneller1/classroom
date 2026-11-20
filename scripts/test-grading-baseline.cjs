'use strict';
// Cross-course grading guard. Each course's practice-test grader (Grades 5-8, Calculus, Statistics, Discrete Math, ...)
// shares worksheet-generator/practice/grading.js, so a change made for one course can change grading in another.
// This loads the graders exactly as practice-test.html does, with each bank's course set as practice.js sets it, and
// compares every published bank question with tests/fixtures/grading-baseline.json:
//   - a key that graded itself correct must still grade itself correct;
//   - a wrong multiple-choice option or a find-the-mistake student answer must not become accepted.
// Grading more keys automatically is allowed (reported, not failed). Questions whose key or prompt changed are compared
// only for newly accepted wrong answers.
// After an intended grading change, record it:  node scripts/test-grading-baseline.cjs --update
const fs = require('fs'), path = require('path'), vm = require('vm'), crypto = require('crypto');
const ROOT = path.resolve(__dirname, '..');
const BASE = path.join(ROOT, 'tests/fixtures/grading-baseline.json');
const update = process.argv.includes('--update');

const page = fs.readFileSync(path.join(ROOT, 'worksheet-generator/practice-test.html'), 'utf8');
const files = ['worksheet-generator/menu/mathcheck.js']
  .concat([...page.matchAll(/src="(practice\/[a-z0-9-]*grading\.js)/g)].map(m => 'worksheet-generator/' + m[1]));
const graders = {};
function grader(course) {
  if (graders[course]) return graders[course];
  const c = {}; c.window = c; vm.createContext(c); c.MK_PRACTICE_COURSE = course;
  for (const f of files) vm.runInContext(fs.readFileSync(path.join(ROOT, f), 'utf8'), c, { filename: f });
  return (graders[course] = c.MKPRACTICE);
}
const h = s => crypto.createHash('sha1').update(s).digest('hex').slice(0, 10);

const correct = new Set(), accepted = new Set(), byHash = new Map();
let items = 0;
const manifest = JSON.parse(fs.readFileSync(path.join(ROOT, 'question-banks/manifest.json'), 'utf8')).banks;
for (const b of manifest) {
  const P = grader(b.courseId);
  for (const q of JSON.parse(fs.readFileSync(path.join(ROOT, b.path), 'utf8')).questions) {
    if (q.format !== 'short-answer' && q.format !== 'multiple-choice') continue;
    items++;
    const key = String(q.answer), prompt = q.prompt || '';
    const id = h(b.courseId + '|' + q.id + '|' + key + '|' + prompt);
    byHash.set(id, b.courseId + ' ' + q.id + ' ' + JSON.stringify(key));
    if (P.gradeBank(key, key, prompt).status === 'correct') correct.add(id);
    const wrong = (q.options || []).filter(o => !o.correct).map(o => o.text);
    const m = /'s answer: (.*)$/m.exec(prompt);
    if (m) wrong.push(m[1]);
    for (const t of wrong) {
      if (String(t).trim() === key.trim()) continue;
      if (P.gradeBank(key, t, prompt).status === 'correct') {
        const w = h(id + '|' + t);
        accepted.add(w);
        byHash.set(w, b.courseId + ' ' + q.id + ' key ' + JSON.stringify(key) + ' accepts ' + JSON.stringify(t));
      }
    }
  }
}

if (update || !fs.existsSync(BASE)) {
  fs.writeFileSync(BASE, JSON.stringify({ note: 'Written by scripts/test-grading-baseline.cjs --update', items,
    correct: [...correct].sort().join(' '), accepted: [...accepted].sort().join(' ') }) + '\n');
  console.log(`grading baseline written: ${items} questions, ${correct.size} keys graded correct, ${accepted.size} accepted wrong answers`);
  process.exit(0);
}
const base = JSON.parse(fs.readFileSync(BASE, 'utf8'));
const baseCorrect = new Set(base.correct.split(' ').filter(Boolean)), baseAccepted = new Set(base.accepted.split(' ').filter(Boolean));
const allIds = new Set(byHash.keys());
const lost = [...baseCorrect].filter(id => allIds.has(id) && !correct.has(id));
const newlyAccepted = [...accepted].filter(w => !baseAccepted.has(w));
const gained = [...correct].filter(id => !baseCorrect.has(id)).length;
for (const id of lost.slice(0, 20)) console.error('NO LONGER CORRECT: ' + byHash.get(id));
for (const w of newlyAccepted.slice(0, 20)) console.error('NEWLY ACCEPTED: ' + byHash.get(w));
if (lost.length || newlyAccepted.length) {
  console.error(`FAIL grading changed in a way that hurts students: ${lost.length} key(s) no longer grade correct, ` +
    `${newlyAccepted.length} wrong answer(s) newly accepted. If this is intended, run: node scripts/test-grading-baseline.cjs --update`);
  process.exit(1);
}
console.log(`PASS grading baseline: ${items} questions in ${manifest.length} banks; no key stopped grading correct, ` +
  `no wrong answer newly accepted; ${gained} key(s) newly auto-graded since the baseline`);
