#!/usr/bin/env node
// Statistics audit 2026-11-18: regression checks for the fixes (batch S1: #1, #3, #6, #10, #11, #12, #13, #14, #18, #19).
'use strict';
const assert = require('node:assert/strict');
const fs = require('node:fs'), path = require('node:path'), vm = require('node:vm');
const ROOT = path.join(__dirname, '..');
const dir = path.join(ROOT, 'question-banks/statistics');
const items = fs.readdirSync(dir).filter(f => f.endsWith('.json')).flatMap(f => JSON.parse(fs.readFileSync(path.join(dir, f), 'utf8')).questions);
const keyText = q => q.format === 'multiple-choice' ? q.options.find(o => o.correct).text : Array.isArray(q.answer) ? q.answer.join('; ') : String(q.answer);
const fam = q => ((q.sourceNotes || '').match(/family: ([^)]+)\)/) || [])[1] || '';
const text = q => [q.prompt, keyText(q), ...q.solutionSteps, ...(q.options || []).map(o => o.text), ...(q.parts || []).flatMap(p => [p.prompt, p.answer])].join(' ');
const numeric = a => /\d/.test(a) && (a.match(/[A-Za-z]{3,}/g) || []).length <= 2 && a.length <= 40;

// #1 no computational item keeps a one-line solution
const oneStep = items.filter(q => ['short-answer', 'multiple-choice'].includes(q.format) && q.solutionSteps.length === 1 && numeric(keyText(q)) && !q.prompt.startsWith('Error analysis'));
assert.deepEqual(oneStep.map(q => q.id), [], 'one-step computational solutions');

// #3 every item carries objectives from the AP framework effective fall 2026, each with a description
const c = {}; c.window = c; vm.createContext(c);
vm.runInContext(fs.readFileSync(path.join(ROOT, 'worksheet-generator/menu/standards.js'), 'utf8'), c);
const STD = Object.values(c).find(v => v && typeof v.describe === 'function' && typeof v.framework === 'function');
const used = new Set(items.flatMap(q => q.standards));
for (const q of items) {
  assert(q.standards.length, q.id + ' has no standard');
  for (const s of q.standards) assert.match(s, /^APSTATS\.([1-5]\.\d+\.[A-F]|BEYOND\.[A-Z]+)$/, q.id + ' code ' + s);
}
for (const s of used) assert.match(STD.describe(s), s.includes('BEYOND') ? /beyond the course/ : /^AP Statistics [1-5]\.\d+\.[A-F]: [A-Z]/, 'description for ' + s);
assert(used.size >= 120, 'objectives in use: ' + used.size);
require(path.join(ROOT, 'course-catalog.js'));
const names = Object.fromEntries(['anticipating-patterns', 'statistical-inference'].flatMap(u => globalThis.MK_COURSE_CATALOG.getSkillRecords('statistics', u).map(s => [s.id, s.name])));
for (const id of ['anticipating-patterns-skill-08', 'statistical-inference-skill-11', 'statistical-inference-skill-12', 'statistical-inference-skill-14'])
  assert.match(names[id], /^Beyond AP: /, id + ' is labelled Beyond AP');
for (const q of items.filter(q => /statistical-inference-skill-(11|12|14)|anticipating-patterns-skill-08/.test(q.skillId))) assert(q.standards.every(s => s.includes('BEYOND')), q.id + ' retired topic tag');

// #6 sampling distributions of a difference (topics 3.9 and 4.6) at every level
for (const level of ['cp2', 'cp1', 'honors']) {
  const lv = items.filter(q => q.level === level);
  assert(lv.filter(q => q.standards.some(s => s.startsWith('APSTATS.3.9.'))).length >= 4, level + ' p̂₁ − p̂₂');
  assert(lv.filter(q => q.standards.some(s => s.startsWith('APSTATS.4.6.'))).length >= 4, level + ' x̄₁ − x̄₂');
  // #11 choosing the inference procedure
  assert(lv.filter(q => fam(q) === 'audit_choose_procedure').length >= 8, level + ' choose-the-procedure items');
}
const procs = new Set(items.filter(q => fam(q) === 'audit_choose_procedure').map(keyText));
assert(procs.size >= 10, 'procedures covered: ' + procs.size);

// #12 technology keys say so, and no step pairs a rounded z with a probability it does not give
for (const id of ['stat-u3-t3-012', 'stat-u3-t3-013', 'stat-u3-t3-014', 'stat-u3-t3-018', 'stat-u4-t2-014', 'stat-u4-t2-016']) {
  const q = items.find(x => x.id === id);
  assert.match(q.prompt, /Use technology \(normalcdf\)/, id); assert(q.solutionSteps.some(s => /Table A with z rounded/.test(s)), id + ' table note');
}

// #13 notation
for (const q of items) {
  const t = text(q);
  assert(!/^(Σ|X̄|Ŷ|Z|P₀|B|T\*|P̂|D̄|S) =? ?/.test(q.prompt) || /^(Z|S|B|P|T|D)[a-z]/.test(q.prompt), q.id + ' capitalized symbol: ' + q.prompt.slice(0, 20));
  assert(!/\(\d dp\)|\b\d dp\b/.test(t), q.id + ' "dp" shorthand');
  assert(!/\^\d/.test(t), q.id + ' caret exponent');
  assert(!/P-value/.test(t), q.id + ' P-value spelling');
}

// #14 no repeated text-only prompt inside a skill
const seen = new Map();
for (const q of items.filter(q => !q.diagram && q.format !== 'open-response')) {
  const k = q.skillId + '|' + q.prompt.trim().toLowerCase().replace(/\s+/g, ' ');
  assert(!seen.has(k), 'repeated prompt: ' + q.id + ' and ' + seen.get(k)); seen.set(k, q.id);
}

// #18 scope on the course card; #19 no fixed capture sentence
assert.match(fs.readFileSync(path.join(ROOT, 'data.js'), 'utf8'), /"blurb": "AP Statistics content \(2026 framework\)/);
assert(!items.some(q => /as expected over many samples/.test(text(q))), 'stock capture sentence');

// #10 the prompt-reading key checker runs in CI
assert.match(fs.readFileSync(path.join(ROOT, '.github/workflows/statistics-bank.yml'), 'utf8'), /statistics-audit-20261118\/verify_keys\.py/);
console.log(`PASS Statistics audit fixes: ${items.length} items, ${used.size} AP objectives, ${procs.size} procedures, no one-step computational solutions`);
