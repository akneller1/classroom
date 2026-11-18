'use strict';
// Calculus audit (2026-11-18): regression checks for the fixes. Batch C1: #1, #7, #8, #11, #12, #13, #14, #18, #19, #20.
const assert = require('node:assert/strict');
const fs = require('node:fs'), path = require('node:path'), vm = require('node:vm');
const ROOT = path.join(__dirname, '..');
const dir = path.join(ROOT, 'question-banks/calculus');
const items = fs.readdirSync(dir).filter(f => f.endsWith('.json')).flatMap(f => JSON.parse(fs.readFileSync(path.join(dir, f), 'utf8')).questions);
const text = q => [q.prompt, q.answer, ...(q.solutionSteps || []), ...(q.parts || []).flatMap(p => [p.prompt, p.answer]), ...(q.options || []).map(o => o.text)].join('\n');
const fam = q => (/family: ([^)]+)\)/.exec(q.sourceNotes || '') || [])[1] || '';

// #1 find-the-mistake items: a specific diagnosis, a student answer that differs from the key, no repeats.
const errs = items.filter(q => /answered this problem incorrectly/.test(q.prompt));
assert(errs.length >= 400, 'find-the-mistake items: ' + errs.length);
const VAGUE = /^Mistake: (Made a sign error\.|Made a sign error or missed a factor\.|Made an error with the rule\.|Applied the property incorrectly\.|Applied the rule incorrectly\.|Made a sign error or skipped a step\.|Made an arithmetic error\.|Made an algebra error\.|Made an error with the coefficient\.|Made an error with the degrees\.|Used the wrong endpoints\.|Doubled or misused the formula\.|Integrated incorrectly\.|Added x = 0 without reason\.)$/;
const seen = new Map();
for (const q of errs) {
  const m = /^(\w+)'s answer: (.*)$/m.exec(q.prompt);
  assert(m, q.id + ' student answer line');
  assert.notEqual(m[2].trim(), String(q.answer).trim(), q.id + ' student answer equals the key');
  const lab = q.solutionSteps.find(s => s.startsWith('Mistake: '));
  assert(lab && lab.length > 16, q.id + ' diagnosis');
  assert(!VAGUE.test(lab), q.id + ' vague diagnosis: ' + lab);
  assert(!/^Mistake: (?:Ava|Ben|Chloe|Hana|Kenji|Omar|Dev|Elena|Femi|Hiro|Isla|Kai|Lena|Marco|Nia|Priya|Quinn|Rosa|Sam|Tariq|Uma|Vic|Wren|Yusuf|Zoe|Jamal|Leah) /.test(lab), q.id + ' diagnosis names the student');
  assert(!/C-\d|C\dx|·1\/e/.test(m[2]), q.id + ' garbled student answer');
  assert.equal(q.solutionSteps[q.solutionSteps.length - 1], `The correct answer is ${q.answer}, not ${m[2]}.`, q.id + ' closing step');
  const key = q.prompt.split('\n')[1] + '|' + m[2];
  assert(!seen.has(key), q.id + ' repeats ' + seen.get(key)); seen.set(key, q.id);
}
// students' answers that contradict their diagnosis (audit examples)
const byId = Object.fromEntries(items.map(q => [q.id, q]));
assert.match(byId['cal-app-s02-cp2-014'].solutionSteps[0], /Missed x = 0/);
assert.match(byId['cal-apr-s02-honors-016'].solutionSteps[0], /quotient rule/);
assert.match(byId['cal-pcr-s03-cp2-016'].solutionSteps[0], /ln\(e\)/);

// no tank or reservoir ends with a negative amount
for (const q of items) if (/(tank|reservoir) holds/.test(q.prompt)) assert(!/^-/.test(String(q.answer)), q.id + ' negative amount');

// #7 pacing guide and unit briefings
const plan = fs.readFileSync(path.join(ROOT, 'scripts/geo-planning.mjs'), 'utf8');
assert.match(plan, /calculus: \{ name: "Calculus", load: \(\) => bankScope\("calculus", "CA", \{ ap: true/);
assert.match(fs.readFileSync(path.join(ROOT, 'scripts/test-public-site.cjs'), 'utf8'), /'calculus-pacing\/'/);

// #8 skills practice what they name
const conv = items.filter(q => q.skillId === 'antiderivatives-definite-integrals-skill-04');
assert(!conv.some(q => /Approximate ∫/.test(text(q))), 'finite Riemann sums in Converting Riemann Sums to Integral Notation');
assert(conv.filter(q => /lim \(n → ∞\) Σ/.test(text(q))).length >= 45, 'conversion items');
const acc = items.filter(q => q.skillId === 'fundamental-theorem-calculus-skill-03');
assert(!acc.some(q => /^s2_/.test(fam(q))), 'skill-02 items in Analyzing Functions Defined by Integrals');
assert(items.filter(q => q.skillId === 'antiderivatives-definite-integrals-skill-03' && /Rₙ/.test(q.prompt)).length >= 12, 'limit-of-sum items');

// #11 every AP code has its own description; tags match the objectives
const c = {}; c.window = c; vm.createContext(c);
vm.runInContext(fs.readFileSync(path.join(ROOT, 'worksheet-generator/menu/standards.js'), 'utf8'), c);
for (const code of new Set(items.flatMap(q => q.standards).filter(s => /^AP /.test(s))))
  assert.match(c.MKSTD.describe(code), new RegExp('^AP Calculus ' + code.slice(3).replace('.', '\\.') + ': '), code);
assert(!items.some(q => q.standards.includes('AP CHA-5.D')), 'CHA-5.D is the BC polar-area objective');

// #12 open-response stems name the skill
assert(!items.some(q => q.format === 'open-response' && q.prompt.trim() === 'Answer each part. Show your work.'), 'generic open-response stem');

// #13 notation
const BAD = [[/(?<![\d.\w/)⁰-⁹^′″])-?1(?=[a-zA-Z])(?!n\))/, 'written coefficient 1'], [/(?<![\w)(/.√])\d+\/\d+e\^/, 'fraction coefficient before e^'],
  [/common factor is \(x [-+] 0\)/, '(x - 0)'], [/\b(sin|cos|tan|sec)\(x\)[²³⁴⁵⁶⁷⁸⁹]/, 'cos(x)ⁿ'], [/√\(-x² \+ \d+\)/, '√(-x² + c)'], [/quadrant none/, 'quadrant none'],
  [/ - -\d/, '- -'], [/[a-z] \+ -\d/, 'x + -n']];
for (const q of items) for (const [re, what] of BAD) assert(!re.test(text(q)), q.id + ' ' + what + ': ' + (re.exec(text(q)) || [''])[0]);

// #14 AP Review skills
const just = items.filter(q => q.skillId === 'ap-review-skill-06');
assert(just.filter(q => /^just_/.test(fam(q))).length >= 30, 'justification items');
assert(!items.some(q => q.skillId === 'ap-review-skill-07' && /^cal_s7_props/.test(fam(q))), 'integral-property computations in Calculus Notation and Written Explanations');

// #18 Euler's method is marked as a BC topic
for (const q of items) if (/Euler's method/.test(q.prompt)) assert.match(text(q), /Euler's method \(a BC topic\)/, q.id);

// #19 IVT wording and motion units
for (const q of items) assert(!/least number of solutions|At least 0\./.test(text(q)), q.id + ' IVT wording');
for (const q of items) if (/position s\(t\) = .* for t ≥ 0\. Find the (velocity|acceleration) at/.test(q.prompt)) {
  assert.match(q.prompt, /meters at time t seconds/, q.id);
  assert.match(String(q.answer), /m\/s²?$/, q.id + ' units');
}

// #20 the independent key checker runs in CI
const wf = fs.readFileSync(path.join(ROOT, '.github/workflows/precalculus-calculus-bank-integration.yml'), 'utf8');
assert.match(wf, /verify_keys\.py/);

console.log(`PASS Calculus audit fixes: ${errs.length} find-the-mistake items with specific diagnoses, pacing, on-skill items, AP objectives, stems, notation, AP Review, Euler marked BC, IVT wording and units`);
