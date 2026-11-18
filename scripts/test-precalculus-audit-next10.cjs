'use strict';
// Precalculus audit (2026-11-18), items #12–#20: level differentiation, select-all, notation, exact forms,
// rounding, option order, grammar, list formats and lab headers. (#11, the answer checker, runs as its own CI step.)
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const ROOT = path.join(__dirname, '..');
const dir = path.join(ROOT, 'question-banks/precalculus');
const items = fs.readdirSync(dir).filter((f) => f.endsWith('.json')).flatMap((f) => JSON.parse(fs.readFileSync(path.join(dir, f), 'utf8')).questions);
const texts = (q) => [q.prompt, ...(Array.isArray(q.answer) ? q.answer : [q.answer]), ...(q.solutionSteps || []),
  ...(q.options || []).map((o) => o.text), ...(q.parts || []).flatMap((p) => [p.prompt, p.answer])].filter((s) => typeof s === 'string');
function sig(p) {
  const lines = p.split('\n');
  let t = /answered this problem incorrectly/.test(lines[0]) && lines.length > 1 ? lines[1] : lines[0];
  return t.replace(/\d+(\.\d+)?/g, '#').replace(/(#\s*[+\-−]\s*)+#/g, '#').replace(/[−-]\s*#/g, '#').slice(0, 70);
}

// #12 in every skill, Advanced has at least one question type that Support does not.
const types = {};
for (const q of items) if (['short-answer', 'multiple-choice'].includes(q.format)) {
  const s = (types[q.skillId] = types[q.skillId] || { cp2: new Set(), honors: new Set() });
  if (s[q.level]) s[q.level].add(sig(q.prompt));
}
const same = Object.entries(types).filter(([, s]) => ![...s.honors].some((t) => !s.cp2.has(t))).map(([k]) => k);
assert.deepEqual(same, [], 'Advanced differs in kind from Support');

// #13 select-all items include property questions, with varied numbers of correct choices (at least 2).
const sa = items.filter((q) => q.format === 'select-all');
const counts = sa.map((q) => q.options.filter((o) => o.correct).length);
assert(counts.every((n) => n >= 2), 'select-all needs at least two correct choices');
assert(new Set(counts).size >= 4, 'select-all correct-choice counts vary: ' + [...new Set(counts)]);
assert(sa.filter((q) => !/matched with the correct answer/.test(q.prompt)).length >= 27, 'property select-all items');
for (const q of sa) assert.deepEqual([...q.answer].sort(), q.options.filter((o) => o.correct).map((o) => o.text).sort(), q.id + ' key matches flags');

// #14 a fraction written right before a variable, i, π, √, a function or "(" reads two ways.
const FRAC = /(?<![\w)\]/])\d+\/\d+(?=\s?[√∛]|i\b|[a-zπθ](?![a-z])|\(|sin|cos|tan|sec|csc|cot|log|ln)/;
const amb = [];
for (const q of items) for (const s of texts(q)) { const m = FRAC.exec(s); if (m) amb.push(q.id + ': ' + s.slice(Math.max(0, m.index - 10), m.index + 10)); }
assert.deepEqual(amb, [], 'parenthesize fraction coefficients');

// #15 15° and 75° values use the textbook forms (√6 ± √2)/4.
assert(!items.some((q) => texts(q).some((s) => /√\(\s*√3 \+ 2\)|√\(2 [+-] √3\)/.test(s))), 'no nested radicals');

// #16 decimal keys come with a rounding instruction.
const ROUNDED = /nearest|round|decimal|tenth|hundredth|thousandth|approximat|≈|calculator|estimate|exact/i;
const unrounded = items.filter((q) => ['short-answer', 'multiple-choice'].includes(q.format) && typeof q.answer === 'string' && /≈|\.\d{3,}/.test(q.answer) && !ROUNDED.test(q.prompt));
assert.deepEqual(unrounded.map((q) => q.id), [], 'say how to round');

// #17 the correct choice is spread evenly over the positions.
const mc = items.filter((q) => q.format === 'multiple-choice');
const pos = [0, 0, 0, 0];
for (const q of mc) pos[q.options.findIndex((o) => o.correct)]++;
for (const n of pos) assert(n / mc.length > 0.21 && n / mc.length < 0.29, 'correct-choice positions ' + pos);

// #18 no "1 rows", "1 successes" and the like.
assert(!items.some((q) => texts(q).some((s) => /(?<![\d.\-/−])\b1 (rows|columns|successes|inches|weeks)\b/.test(s))), 'singular after 1');

// #19 solution lists use "x = a or x = b".
assert(!items.some((q) => typeof q.answer === 'string' && /^x = [^,;]+(, [^,;]+)+$/.test(q.answer)), 'solution lists joined with "or"');

// #20 the Algebra 2 labs listed in Precalculus say Precalculus in their header.
const data = fs.readFileSync(path.join(ROOT, 'data.js'), 'utf8');
const pcLabs = [...data.matchAll(/\{"course": ?"precalculus", ?"unit": ?"[^"]+", ?"a": ?\{"title": ?"[^"]+", ?"path": ?"(artifacts\/algebra2-[^"]+)"/g)].map((m) => m[1]);
assert(pcLabs.length >= 6, 'shared labs listed');
for (const p of pcLabs) assert(/\?course=Precalculus&unit=/.test(p), p + ' opens with the Precalculus header');
const lab = fs.readFileSync(path.join(ROOT, 'artifacts/interactive-math/lab.js'), 'utf8');
assert(/q\.get\('course'\)/.test(lab) && /o\.course = q\.get\('course'\)/.test(lab), 'lab.js reads ?course=');

console.log(`PASS Precalculus audit #12–#20: ${sa.length} select-all, correct positions ${pos.join('/')}, ${mc.length} multiple choice`);
