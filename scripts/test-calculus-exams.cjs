#!/usr/bin/env node
// Calculus audit #17 (2026-11-18): two AP Calculus AB-style practice exams. Each has 30 + 15 multiple-choice questions
// and 2 + 4 free-response problems, each multiple-choice question has four distinct options with the keyed answer among
// them, no question is in both exams, the key matches the student copy, and both are placed in AP Review with PDFs.
'use strict';
const fs = require('fs'), vm = require('vm'), path = require('path'), assert = require('assert/strict');
const root = path.resolve(__dirname, '..');
const strip = s => s.replace(/<[^>]+>/g, '').replace(/&amp;/g, '&').replace(/&lt;/g, '<').replace(/&gt;/g, '>');
const prompts = {};
for (const ex of ['a', 'b']) {
  const dir = path.join(root, 'artifacts', 'calculus-ap-practice-exam-' + ex);
  const exam = fs.readFileSync(path.join(dir, 'exam.html'), 'utf8'), key = fs.readFileSync(path.join(dir, 'key.html'), 'utf8');
  const mc = h => [...h.matchAll(/<li value="(\d+)"><div class="q">([\s\S]*?)<\/div>[\s\S]*?<div class="choices">([\s\S]*?)<\/div><\/div>(?:<div class="ans">Answer: \(([A-D])\) ([\s\S]*?)<\/div>)?/g)]
    .map(m => ({ n: +m[1], q: strip(m[2]), opts: [...m[3].matchAll(/<span class="choices-t">([\s\S]*?)<\/span>/g)].map(o => strip(o[1])), letter: m[4], ans: m[5] && strip(m[5]) }));
  const E = mc(exam), K = mc(key);
  assert.deepEqual(E.map(q => q.n), Array.from({ length: 45 }, (_, i) => i + 1), ex + ' numbering 1–45');
  assert.deepEqual(E.map(q => q.q + q.opts.join('|')), K.map(q => q.q + q.opts.join('|')), ex + ' key matches the exam');
  for (const q of K) {
    assert.equal(q.opts.length, 4, ex + q.n + ' four options');
    assert.equal(new Set(q.opts).size, 4, ex + q.n + ' distinct options');
    assert.equal(q.opts['ABCD'.indexOf(q.letter)], q.ans, ex + q.n + ' keyed letter is the answer');
  }
  const pos = {}; K.forEach(q => { pos[q.letter] = (pos[q.letter] || 0) + 1; }); assert(Object.values(pos).every(v => v >= 6), ex + ' answer positions ' + JSON.stringify(pos));
  const frq = [...key.matchAll(/<h3>Question (\d)<\/h3>/g)].map(m => +m[1]);
  assert.deepEqual(frq, [1, 2, 3, 4, 5, 6], ex + ' six free-response problems');
  assert.equal((key.match(/Scoring, \d+ points?:/g) || []).length, 24, ex + ' scoring notes for every part');
  assert.equal((exam.match(/Scoring|class="ans"/g) || []).length, 0, ex + ' student copy has no answers');
  assert.match(exam, /Section I, Part A[^<]*No calculator[^<]*60 minutes/); assert.match(exam, /Section II, Part B[^<]*No calculator[^<]*60 minutes/);
  assert.match(key, /composite = 1\.2 × \(multiple-choice points\)/);
  for (const f of ['exam.pdf', 'teacher-key.pdf']) assert(fs.statSync(path.join(dir, f)).size > 50000, ex + ' ' + f);
  prompts[ex] = new Set(E.map(q => q.q + q.opts.join('|')));
  for (const m of exam.matchAll(/src="\.\.\/\.\.\/([^"]+)"/g)) assert(fs.existsSync(path.join(root, m[1].split('?')[0])), 'image or script ' + m[1]);
}
assert.equal([...prompts.a].filter(p => prompts.b.has(p)).length, 0, 'no question in both exams');
const ctx = { window: {} }; vm.runInNewContext(fs.readFileSync(path.join(root, 'data.js'), 'utf8'), ctx);
const unit = ctx.window.LIBRARY.courses.find(c => c.id === 'calculus').units.find(u => u.id === 'ap-review');
for (const ex of ['a', 'b']) {
  const a = unit.artifacts.find(a => a.path === `artifacts/calculus-ap-practice-exam-${ex}/exam.pdf`);
  assert(a && a.answerKey && fs.existsSync(path.join(root, a.thumb)), 'AP Review card for exam ' + ex);
}
console.log('PASS Calculus AP practice exams: 2 × (45 multiple choice + 6 free response), keys match, no shared questions, cards in AP Review');
