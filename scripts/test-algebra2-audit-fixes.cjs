'use strict';
// Regression tests for the Algebra 2 audit of 2026-11-17 (doc: Algebra 2 audit — mrksclassroom.com).
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');
const ROOT = path.join(__dirname, '..');
const manifest = JSON.parse(fs.readFileSync(path.join(ROOT, 'question-banks/manifest.json'), 'utf8'));
const items = manifest.banks.filter(b => b.courseId === 'algebra2')
  .flatMap(b => JSON.parse(fs.readFileSync(path.join(ROOT, b.path), 'utf8')).questions);
const texts = q => [q.prompt, ...(Array.isArray(q.answer) ? q.answer : [q.answer]), ...(q.solutionSteps || []),
  ...(q.options || []).map(o => o.text), ...(q.parts || []).flatMap(p => [p.prompt, p.answer])].filter(s => typeof s === 'string');

// #8 a fraction written right before a variable, i, √ or ( reads two ways (1/2√x, 7/10i, 3/4x).
const ambiguous = [];
for (const q of items) for (const s of texts(q)) {
  const m = /(?<![\w)\]/(])\d+\/\d+(?=\s?[√∛]|i\b|[a-zπθ](?![a-z])|\()/.exec(s);
  if (m) ambiguous.push(q.id + ': ' + s.slice(Math.max(0, m.index - 12), m.index + 14));
}
assert.deepEqual(ambiguous, [], 'parenthesize fraction coefficients');
const division = items.filter(q => /\)\/\([^()]*\) ÷ \(?[^()]*\)?\//.test(q.prompt) && !/\(\([^()]*\)\/\([^()]*\)\) ÷/.test(q.prompt));
assert.deepEqual(division.map(q => q.id), [], 'bracket both fractions around ÷');

// #9 the answer to a short question should not be printed in it.
const giveaways = items.filter(q => /repeating every \d+ \w+\. What is the period/.test(q.prompt) || /How long until half remains/.test(q.prompt));
assert.deepEqual(giveaways.map(q => q.id), [], 'period and half-life prompts must not state the answer');
for (const q of items) {
  const m = /\n(\w+)'s answer: (.*)\n/.exec(q.prompt), problem = /:\s*(.+)\n\w+'s answer/.exec(q.prompt);
  if (m && problem) assert.notEqual(m[2].trim(), problem[1].trim().replace(/\.$/, ''), q.id + ': the student answer is the original expression');
}

// #17 decimal answers come with a rounding instruction (exact decimals and money from exact data excepted).
const ROUNDED = /nearest|round|decimal|tenth|hundredth|thousandth|approximat|≈|calculator|estimate|exact/i;
const unrounded = items.filter(q => q.format === 'short-answer' && typeof q.answer === 'string' && /≈|\.\d{3,}/.test(q.answer) && !ROUNDED.test(q.prompt));
assert.deepEqual(unrounded.map(q => q.id), [], 'say how to round');
assert(!items.some(q => typeof q.answer === 'string' && /=\s*-?\d+\.00\b/.test(q.answer)), 'whole-number values are not written with .00');

// #18 select-all includes items with one correct choice and items with every choice correct.
const multi = items.filter(q => q.format === 'select-all');
const counts = multi.map(q => q.options.filter(o => o.correct).length);
assert(counts.every(n => n >= 2), 'select-all keeps at least two correct choices (bank schema)');
assert(multi.filter((q, i) => counts[i] === q.options.length).length >= 15, 'some select-all items have every choice correct');
for (const q of multi) assert.deepEqual([...q.answer].sort(), q.options.filter(o => o.correct).map(o => o.text).sort(), q.id + ' key matches flags');

// #15 open-response stems say what the set is about.
assert(!items.some(q => q.prompt.trim() === 'Answer each part. Show your work.'), 'no generic open-response stem');

// #11 / #16 planner notes: every skill has notes; ellipse and hyperbola lessons are labelled enrichment.
const w = {}; w.window = w; vm.createContext(w);
for (const f of ['course-catalog.js', 'worksheet-generator/planner/notes-teach-algebra2.js']) vm.runInContext(fs.readFileSync(path.join(ROOT, f), 'utf8'), w);
const units = Object.keys(w.MK_COURSE_CATALOG.skills.algebra2);
const enrich = [];
for (const u of units) for (const s of w.MK_COURSE_CATALOG.getSkillRecords('algebra2', u)) {
  const meta = w.MKPLAN_TEACH_ALGEBRA2_META(s.id);
  assert(meta && meta.obj && meta.voc && meta.voc.length && meta.watch, 'teaching notes for ' + s.id);
  if (meta.enrich) enrich.push(s.id);
}
assert.deepEqual(enrich, ['conic-sections-skill-03', 'conic-sections-skill-04']);
const scope = fs.readFileSync(path.join(ROOT, 'worksheet-generator/planner/scope-algebra2.js'), 'utf8');
assert(/meta&&meta\.enrich\)title\+=' \(enrichment\)'/.test(scope), 'scope labels enrichment lessons');

// #12 the practice test honours ?course= when no unit is given.
const practice = fs.readFileSync(path.join(ROOT, 'worksheet-generator/practice/practice.js'), 'utf8');
assert(/get\('course'\)/.test(practice) && /indexOf\(prefix\)===0/.test(practice), 'practice test reads ?course=');

console.log('PASS Algebra 2 audit fixes: notation, giveaways, rounding, select-all counts, stems, planner notes, course default (' + items.length + ' items)');
