#!/usr/bin/env node
// Statistics audit batch S2 (2026-11-18): #2 free-response problems, #7 grading and self-check lists, #8 CP contexts,
// CP2 hints and level complexity, #9 diagrams, #20 at least 24 items per skill and level.
'use strict';
const fs = require('fs'), path = require('path'), vm = require('vm'), assert = require('assert');
const ROOT = path.resolve(__dirname, '..');
const UNITS = ['exploring-data', 'sampling-experimentation', 'anticipating-patterns', 'statistical-inference'];
const banks = Object.fromEntries(UNITS.map(u => [u, JSON.parse(fs.readFileSync(path.join(ROOT, 'question-banks/statistics', u + '.json'), 'utf8')).questions]));
const all = UNITS.flatMap(u => banks[u].map(q => ({ ...q, unit: u })));
const LEVELS = ['cp2', 'cp1', 'honors'];
const key = q => q.format === 'multiple-choice' ? q.options.find(o => o.correct).text : Array.isArray(q.answer) ? q.answer.join('; ') : String(q.answer);
const cells = new Map();
for (const q of all) { const k = q.skillId + '/' + q.level; if (!cells.has(k)) cells.set(k, []); cells.get(k).push(q); }
assert.strictEqual(cells.size, 123);

// #20 every skill and level has at least 24 items
for (const [k, qs] of cells) assert(qs.length >= 24, 'fewer than 24 items: ' + k);

// #2 one AP-style free-response problem per skill and level
const FOUR = new Set([3, 4, 7, 9, 10, 11, 12, 13, 14]);
let frqs = 0;
for (const [k, qs] of cells) {
  const f = qs.filter(q => q.format === 'open-response' && q.prompt.startsWith('Free response ('));
  assert.strictEqual(f.length, 1, 'one free-response problem: ' + k);
  const q = f[0];
  assert.deepStrictEqual(q.parts.map(p => p.label), ['a', 'b', 'c', 'd'], q.id + ' four labelled parts');
  assert(q.parts.every(p => p.prompt && String(p.answer).length > 0), q.id + ' part prompts and answers');
  assert(q.parts.some(p => /\b(Justify|justify|Explain|explain|Interpret|interpret)\b/.test(p.prompt)), q.id + ' a justify/explain part');
  let pts = 0;
  for (const lab of 'abcd') {
    const sc = q.solutionSteps.find(s => s.startsWith('(' + lab + ') Scoring, '));
    assert(sc && q.solutionSteps.some(s => s.startsWith('(' + lab + ') ') && !s.includes('Scoring,')), q.id + ' solution and scoring for part ' + lab);
    pts += +sc.match(/Scoring, (\d+) point/)[1];
  }
  assert.strictEqual(q.solutionSteps[q.solutionSteps.length - 1], `Total: ${pts} points.`, q.id + ' total');
  const sk = +q.skillId.match(/skill-(\d+)/)[1];
  if (q.unit === 'statistical-inference' && FOUR.has(sk))
    assert.deepStrictEqual(q.parts.map(p => p.prompt.split(':')[0]), ['State', 'Plan', 'Do', 'Conclude'], q.id + ' four-step inference problem');
  assert(!/NaN|undefined|Infinity|\+ −|− −|\ba a\b|\bthe a\b/.test(JSON.stringify(q)), q.id + ' text');
  frqs++;
}
assert(!all.some(q => q.prompt.startsWith('Answer each part. Show your work.')), 'generic mixed-review stems remain');
for (const lv of LEVELS) assert(all.filter(q => q.level === lv && q.format === 'open-response').length >= 41, 'open response at ' + lv);

// #7 grading: labelled numbers and number lists; self-check lists for everything else that is written
const c = {}; c.window = c; vm.createContext(c);
for (const f of ['menu/mathcheck.js', 'practice/radical-grading.js', 'practice/exact-grading.js', 'practice/calculus-grading.js', 'practice/stat-grading.js', 'practice/grading.js'])
  vm.runInContext(fs.readFileSync(path.join(ROOT, 'worksheet-generator', f), 'utf8'), c, { filename: f });
const P = c.MKPRACTICE, S = c.MKSTAT;
const g = (a, t, p) => P.gradeBank(a, t, p || '').status;
const cases = [
  ['Min = 15, Q1 = 25, Median = 35, Q3 = 50, Max = 90', '15, 25, 35, 50, 90', 'correct'], ['Min = 15, Q1 = 25, Median = 35, Q3 = 50, Max = 90', 'min 15 q1 25 med 35 q3 50 max 90', 'correct'],
  ['Min = 15, Q1 = 25, Median = 35, Q3 = 50, Max = 90', '15, 25, 35, 55, 90', 'incorrect'], ['Min = 15, Q1 = 25, Median = 35, Q3 = 50, Max = 90', '15, 25, 35, 50', 'incorrect'],
  ['μ = 1.80, σ ≈ 1.208', 'mean 1.8, sd 1.208', 'correct'], ['μ = 1.80, σ ≈ 1.208', '1.80, 1.2083', 'correct'], ['μ = 1.80, σ ≈ 1.208', '1.80, 1.21', 'incorrect'], ['μ = 1.80, σ ≈ 1.208', '1.208, 1.80', 'incorrect'],
  ['z ≈ 2.40, p-value ≈ 0.0082; reject H₀', 'z = 2.40, p = 0.0082, reject H0', 'correct'], ['z ≈ 2.40, p-value ≈ 0.0082; reject H₀', 'z = 2.40, p = 0.0082, fail to reject', 'incorrect'],
  ['z ≈ -1.47, p-value ≈ 0.0708; fail to reject H₀', '-1.47, 0.0708, fail to reject H₀', 'correct'], ['z ≈ -1.47, p-value ≈ 0.0708; fail to reject H₀', '1.47, 0.0708, fail to reject H₀', 'incorrect'],
  ['Yes; upper fence = 34.50', 'yes, 34.5', 'correct'], ['Yes; upper fence = 34.50', 'no, 34.5', 'incorrect'], ['7/36 ≈ 0.1944', '0.1944', 'correct'], ['7/36 ≈ 0.1944', '7/36', 'correct'], ['7/36 ≈ 0.1944', '0.19', 'incorrect'],
  ['Mean 1,030; SD ≈ 106.30', '1030, 106.3', 'correct'], ['Fences 8 and 20; outlier: 30', '8, 20, 30', 'correct'], ['Fences 8 and 20; outlier: 30', '8, 20', 'incorrect'],
];
for (const [a, t, want] of cases) { assert(S.supports(a), 'supports ' + a); assert.strictEqual(g(a, t), want, a + ' / ' + t); }
assert.strictEqual(g('p̂ = 0.55; SE ≈ 0.0231; 99% CI ≈ (0.490, 0.610)', '0.55, 0.0231, 0.490, 0.610', 'A 99% confidence interval …'), 'correct', 'a number printed in the prompt may be left out');
for (const a of ['ŷ = 48.229 + 2.029x', 'Step 1: divide by √n: 12/4 = 3', 'The SD must use p₀ = 0.40, not p̂', 'Strong, positive, linear']) assert(!S.supports(a), 'should not grade ' + a);
const sa = all.filter(q => q.format === 'short-answer');
let auto = 0;
for (const q of sa) {
  const a = key(q), isAuto = P.bankAnswer(a) !== null;
  if (isAuto) { auto++; assert.strictEqual(g(a, a, q.prompt), 'correct', q.id + ' key does not grade itself correct: ' + a); assert(!q.selfCheck, q.id + ' auto-graded item has a self-check list'); }
  else { assert(Array.isArray(q.selfCheck) && q.selfCheck.length >= 2 && q.selfCheck.length <= 3 && q.selfCheck.every(s => typeof s === 'string' && s.length > 8), q.id + ' self-check list'); }
}
// The objective-gap items (gap_items.py, 2026-11-19) ask students to justify or explain, so most are self-checked with a
// list, checked item by item above; the S2 share target (#7) is measured on the rest of the bank, as when it was set.
const gapIds = new Set(JSON.parse(fs.readFileSync(path.join(ROOT, 'tools/statistics-audit-20261118/added-gaps.json'), 'utf8')));
const core = sa.filter(q => !gapIds.has(q.id)), coreAuto = core.filter(q => P.bankAnswer(key(q)) !== null).length;
assert.strictEqual(sa.length - core.length, gapIds.size, 'every objective-gap item is a short answer in the banks');
assert(coreAuto / core.length >= 0.75, 'auto-graded share ' + (coreAuto / core.length).toFixed(3));
const practice = fs.readFileSync(path.join(ROOT, 'worksheet-generator/practice/practice.js'), 'utf8'), html = fs.readFileSync(path.join(ROOT, 'worksheet-generator/practice-test.html'), 'utf8');
assert(/selfCheck:Array\.isArray\(q\.selfCheck\)/.test(practice) && /pt-selfcheck/.test(practice) && /pt-hint/.test(practice), 'practice test shows hints and self-check lists');
assert(/<script src="practice\/stat-grading\.js\?v=[^"]+"><\/script>\s*(?:<script src="practice\/grade8-grading\.js\?v=[^"]+"><\/script>\s*)?<script src="practice\/grading\.js/.test(html), 'stat-grading.js loads before grading.js');

// #8 CP items in context, CP2 hints, complexity rising with level
const BARE = /^(?:[A-Za-zμσΣχ][̂̄]?[₀-₉ₓ_A-Za-z]{0,3}(?:\([^)]*\))?\*? ?(?:=|≤) ?[−\d(.]|X is N\(|Mean \d|Q1 =|Binomial with|One-sample t|Two-sample t|Two-sided|One-sided|Pool |Independent X|Find the (?:mean|median|range|sample standard deviation) of \d|\d+% confidence,|Power |Group 1 mean|Paired differences|Slope |A regression uses n|To halve|By what factor|Var\(|SD\(|E\(|A data set has|\d+ (?:brands|factors|fertilizers|treatments) |\d+ × |Of \d+ \w+, \d+ \w+\.)/;
const bare = all.filter(q => q.level !== 'honors' && ['short-answer', 'multiple-choice'].includes(q.format) && /\d/.test(key(q)) && BARE.test(q.prompt));
assert.deepStrictEqual(bare.map(q => q.id), [], 'CP drills without context');
const cp2 = all.filter(q => q.level === 'cp2' && q.format !== 'open-response' && q.solutionSteps.length >= 2);
const hinted = cp2.filter(q => q.hint);
assert(hinted.length / cp2.length >= 0.9, 'CP2 hints ' + hinted.length + '/' + cp2.length);
for (const q of hinted) { assert(q.hint.startsWith('First step: ') && q.hint.length > 20, q.id + ' hint'); const k = key(q).trim(); if (k.length > 2) assert(!q.hint.includes(k), q.id + ' hint gives the answer away'); }
assert(!all.some(q => q.level !== 'cp2' && q.hint), 'hints are for CP2 only');
const score = q => q.solutionSteps.length + (q.prompt.match(/\d+(?:\.\d+)?/g) || []).length / 3 + q.prompt.length / 100;
for (const u of UNITS) {
  const m = LEVELS.map(lv => { const qs = banks[u].filter(q => q.level === lv && q.format !== 'open-response'); return qs.reduce((s, q) => s + score(q), 0) / qs.length; });
  assert(m[1] - m[0] >= 0.1 && m[2] - m[1] >= 0.1, u + ' complexity should rise with level: ' + m.map(v => v.toFixed(2)).join(' < '));
}

// #9 design diagrams and shaded Normal curves
const figs = all.filter(q => q.diagram && /assets\/statistics\/audit\//.test(q.diagram.spec.src));
for (const q of figs) { const f = path.join(ROOT, q.diagram.spec.src); assert(fs.existsSync(f) && fs.statSync(f).size > 3000 && fs.statSync(f).size < 120000, q.id + ' figure file'); assert(q.diagram.spec.alt.length > 40, q.id + ' alt text'); }
assert(figs.filter(q => q.unit === 'sampling-experimentation' && /Design diagram/.test(q.diagram.spec.alt)).length >= 12, 'design diagrams');
assert(figs.filter(q => /standard Normal curve/.test(q.diagram.spec.alt)).length >= 3, 'shaded Normal curves');
const onDisk = fs.readdirSync(path.join(ROOT, 'question-banks/assets/statistics/audit'));
assert.strictEqual(onDisk.length, figs.length, 'no unused figure files');

console.log(`PASS Statistics audit S2: ${frqs} free-response problems; ${auto}/${sa.length} short answers auto-graded, the rest with self-check lists; ${hinted.length} CP2 hints; ${figs.length} new figures; every skill and level has at least 24 items`);
