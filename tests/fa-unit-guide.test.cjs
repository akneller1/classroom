'use strict';
// Financial Algebra unit pages get a teacher guide built from the unit's lesson plans (2026-11-16).
const test = require('node:test');
const assert = require('node:assert/strict');
const path = require('node:path');
const fs = require('node:fs');
const root = path.join(__dirname, '..');

test('teacher guide lists the hook, key ideas, mistakes and discussion questions', async () => {
  const { faUnitGuide, plain } = await import(path.join(root, 'scripts/fa-unit-guide.mjs'));
  const bank = { lessons: [
    { hook: 'Two offers: **$24/hour** or $48,000/year.', realWorld: 'Every paycheck.', notes: [{ h: 'Monthly rate', body: '[[APR || 12]]' }], misconceptions: [['A raise can lower take-home pay.', 'Only income in the higher bracket is taxed more.']], discussion: ['Which offer would you take?'] },
    { notes: [{ h: 'Monthly rate', body: 'duplicate heading is dropped' }, { h: 'FICA', body: '7.65% of gross' }], misconceptions: [], discussion: [] }
  ] };
  const html = faUnitGuide(bank, 'Careers & Income');
  assert.match(html, /<h2>Teaching Careers &amp; Income<\/h2>/);
  assert.match(html, /2 ready-to-teach lesson plans/);
  assert.match(html, /Two offers: \$24\/hour/);
  assert.match(html, /<strong>Monthly rate:<\/strong> APR ÷ 12/);
  assert.equal((html.match(/Monthly rate/g) || []).length, 1);
  assert.match(html, /<h2>Common mistakes to watch for<\/h2>/);
  assert.match(html, /<h2>Discussion questions<\/h2>/);
  assert.equal(faUnitGuide({ lessons: [] }, 'X'), '');
  assert.equal(plain('**a** [[1||2]]'), 'a 1 ÷ 2');
  assert.match(fs.readFileSync(path.join(root, 'scripts/build-integrated-unit-pages.mjs'), 'utf8'), /faUnitGuide\(readJson\(path\.join\(OUT, "financial", "banks"/);
});

test('course catalog and student links list the four new Financial Algebra skills', () => {
  const cat = fs.readFileSync(path.join(root, 'course-catalog.js'), 'utf8'), stu = fs.readFileSync(path.join(root, 'integrated-student-skills.js'), 'utf8');
  for (const [id, name] of [['banking-skill-05', 'Spot scams and protect your identity'], ['credit-skill-05', 'Understand credit scores and reports'], ['borrowing-skill-05', 'Calculate the total cost of car ownership'], ['housing-skill-05', 'Plan the costs of renting']]) {
    assert.ok(cat.includes('"' + name + '"'), name); assert.ok(stu.includes('"' + id + '"'), id);
  }
  const map = JSON.parse(fs.readFileSync(path.join(root, 'content-updates/2026-11-15/financial-algebra-standards.json'), 'utf8')).mapping;
  for (const id of ['banking-skill-05', 'credit-skill-05', 'borrowing-skill-05', 'housing-skill-05']) assert.ok(map[id] && map[id][0].startsWith('NSPFE.'), id);
});
