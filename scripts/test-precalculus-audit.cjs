'use strict';
// Precalculus audit (2026-11-18): regression checks for the fixes.
const assert = require('node:assert/strict');
const fs = require('node:fs'), path = require('node:path'), vm = require('node:vm');
const ROOT = path.join(__dirname, '..');
const dir = path.join(ROOT, 'question-banks/precalculus');
const items = fs.readdirSync(dir).filter(f => f.endsWith('.json')).flatMap(f => JSON.parse(fs.readFileSync(path.join(dir, f), 'utf8')).questions);

// #2 the practice-test grader reads exact values, vectors, matrices, intervals and rounded answers, and insists on simplest form.
const c = {}; c.window = c; vm.createContext(c);
for (const f of ['worksheet-generator/menu/mathcheck.js', 'worksheet-generator/practice/radical-grading.js', 'worksheet-generator/practice/exact-grading.js', 'worksheet-generator/practice/grading.js'])
  vm.runInContext(fs.readFileSync(path.join(ROOT, f), 'utf8'), c, { filename: f });
const P = c.MKPRACTICE;
const sa = items.filter(q => q.format === 'short-answer');
const auto = sa.filter(q => P.bankAnswer(String(q.answer)) !== null);
assert(auto.length >= 2000, 'auto-graded Precalculus short answers: ' + auto.length);
for (const q of auto) assert.equal(P.gradeBank(String(q.answer), String(q.answer)).status, 'correct', q.id + ' key grades itself correct');
const cases = [
  ['(√3)/2', '√3/2', 'correct'], ['(√3)/2', '0.866', 'invalid'], ['7π/2', '3.5π', 'correct'], ['π/6', 'pi/6', 'correct'], ['(√3)/2', '(√3)/3', 'incorrect'],
  ['14 - 8i', '14-8i', 'correct'], ['14 - 8i', '(2+i)(4-6i)', 'invalid'], ['7√2', '√98', 'invalid'], ['(√2)/2', '1/√2', 'invalid'], ['2√6', '2√3·√2', 'invalid'],
  ['⟨1, -10⟩', '<1, -10>', 'correct'], ['⟨1, -10⟩', '⟨-10, 1⟩', 'incorrect'], ['[6, 5; 1, 1]', '[6,5;1,1]', 'correct'], ['[6, 5; 1, 1]', '[6,5;1,2]', 'incorrect'],
  ['(-∞, -4) ∪ (-4, ∞)', '(-∞,-4)∪(-4,∞)', 'correct'], ['(-∞, -4) ∪ (-4, ∞)', '(-∞,-4]∪(-4,∞)', 'incorrect'], ['[-9, ∞)', '[-9, ∞]', 'invalid'],
  ['x = π/6 or x = 7π/6', '7π/6, π/6', 'correct'], ['x = π/6 or x = 7π/6', 'π/6', 'incorrect'], ['x = 4 + 3i or x = 4 - 3i', 'x=4-3i or x=4+3i', 'correct'],
  ['x ≈ 4.489', '4.489', 'correct'], ['x ≈ 4.489', '4.49', 'incorrect'], ['≈ 12.2 km/h', '12.2', 'correct'], ['(√6 + √2)/4', '(√2+√6)/4', 'correct'],
];
for (const [key, typed, want] of cases) assert.equal(P.gradeBank(key, typed).status, want, key + ' ← ' + typed);
// Equations and expressions in x stay self-checked.
for (const k of ['y = 4cos(2x) - 1', 'x²/16 + y²/25 = 1', '-9x - 9', 'f⁻¹(x) = 2x - 12']) assert.equal(P.bankAnswer(k), null, k);

// #3 pacing page and unit briefings.
const plan = fs.readFileSync(path.join(ROOT, 'scripts/geo-planning.mjs'), 'utf8');
assert.match(plan, /precalculus: \{ name: "Precalculus", load: \(\) => bankScope\("precalculus", "PC"\)/);
assert.match(fs.readFileSync(path.join(ROOT, 'scripts/test-public-site.cjs'), 'utf8'), /'precalculus-pacing\/'/);

// #9 Dot Products and Projections has no magnitude-only items; N-CN.B.4 stays on complex numbers.
assert(!items.some(q => q.skillId === 'vectors-skill-08' && /moves straight from|Find the magnitude of v|Find \|v\|/.test(q.prompt)), 'off-topic dot-product items');
for (const q of items.filter(q => q.standards.includes('N-CN.B.4'))) assert.match(q.prompt + JSON.stringify(q.parts || []), /trigonometric \(polar\) form|(\d|\b)i\b/, q.id + ' N-CN.B.4 on a complex-number item');

// #7 every solution shows its work in at least two steps.
const thinSteps = items.filter(q => !Array.isArray(q.solutionSteps) || q.solutionSteps.length < 2);
assert.equal(thinSteps.length, 0, 'single-step solutions: ' + thinSteps.slice(0, 5).map(q => q.id).join(', '));

// #10 open-response stems name the skill.
assert(!items.some(q => q.format === 'open-response' && q.prompt.trim() === 'Answer each part. Show your work.'), 'generic open-response stem');

console.log(`PASS Precalculus audit fixes: ${auto.length} of ${sa.length} short answers auto-graded, pacing, dot-product items, polar tags, worked solutions, stems`);
