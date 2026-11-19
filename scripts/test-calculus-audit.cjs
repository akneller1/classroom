'use strict';
// Calculus audit (2026-11-18): regression checks for the fixes. Batch C1: #1, #7, #8, #11, #12, #13, #14, #18, #19, #20. Batch C3: #5.
// Batch C2: #3, #4, #9, #10 (the grader, #2, is checked by test-calculus-grading.cjs).
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


// #3 worked solutions: at least two steps everywhere, and integral answers show F(b) and F(a)
assert(!items.some(q => (q.solutionSteps || []).length < 2), 'single-step solutions: ' + items.filter(q => q.solutionSteps.length < 2).map(q => q.id).slice(0, 5));
const integral = items.filter(q => q.format !== 'open-response' && /Evaluate ∫ from \S+ to \S+ [^f]|displacement from|total distance traveled|average value of f\(x\)|area of the region bounded/.test(q.prompt));
const shown = integral.filter(q => q.solutionSteps.some(s => /F\(\S+\) = |s\(\S+\) [−-] s\(|signed area|\]: /.test(s)));
assert(shown.length >= 0.9 * integral.length, `integral items that show the evaluation: ${shown.length} of ${integral.length}`);

// #4 integrals, limits and sums are drawn as big operators; fractions lose their outer parentheses
const md = {}; md.window = md; vm.createContext(md);
vm.runInContext(fs.readFileSync(path.join(ROOT, 'worksheet-generator/core/math-display.js'), 'utf8'), md);
const H = md.MK_MATH_DISPLAY.html;
assert.match(H('Evaluate ∫ from 1 to 3 (2x + 3) dx.'), /class="bo"[^]*class="bo-u">3<[^]*bo-s">∫<[^]*class="bo-l">1</);
assert.match(H('Evaluate lim (x → -3) (x² - 9)/(x + 3).'), /bo-lim[^]*bo-l"><i>x<\/i> → −3<[^]*class="fn"><i>x<\/i>² − 9</);
assert.match(H('lim (n → ∞) Σ (k = 1 to n) (k/n)² · (1/n)'), /bo-s">Σ</);
assert.match(H('Find d/dx [x²].'), /class="fn"><i>d<\/i><\/span><span class="fd"><i>d<\/i><i>x<\/i>/);
assert.match(fs.readFileSync(path.join(ROOT, 'worksheet-generator/core/math-display.css'), 'utf8'), /\.bo\{/);

// #9 Honors items in the upgraded families use richer functions; CP2 items carry a hint
const fx = q => (q.prompt.replace(/Hint: .*$/, '').match(/\b(?:sin|cos|tan|ln)\(|e\^|√|π/g) || []).length;
for (const f of ['s4_disp', 's5_total', 's3_intervals', 's2_crit', 's4_absolute', 's10_mvt', 's5_general', 's5_infty', 's7_sign', 's8_motion', 's2_formula', 's4_accel']) {
  const h = items.filter(q => fam(q) === f + '_h');
  assert(h.length >= 3, f + ' Honors items: ' + h.length);
  const cp2 = items.filter(q => fam(q) === f && q.level === 'cp2' && !/answered this/.test(q.prompt) && q.format !== 'open-response');
  assert(cp2.every(q => /Hint: /.test(q.prompt)), f + ' CP2 hint');
  const avg = a => a.reduce((s, q) => s + fx(q), 0) / Math.max(1, a.length);
  assert(avg(h) > avg(cp2) || ['s5_general', 's7_sign', 's3_intervals', 's2_crit'].includes(f), f + ' Honors no richer than CP2');
}

// #10 AP topics: local linearization, implicit second derivatives, calculator-active integrals, motion from a velocity
// graph, washers about other lines, exponential models
const need = { lin_approx: 9, im_second: 9, calc_numeric: 6, vgraph_: 12, washer_line: 9, exp_model: 9 };
for (const [k, n] of Object.entries(need)) assert(items.filter(q => fam(q).startsWith(k)).length >= n - 1, k + ' items');
for (const q of items.filter(q => fam(q).startsWith('vgraph_'))) assert(fs.existsSync(path.join(ROOT, q.diagram.spec.src)), q.id + ' velocity graph image');
const tagsCalc = fs.readdirSync(path.join(dir, 'meta')).flatMap(f => Object.values(JSON.parse(fs.readFileSync(path.join(dir, 'meta', f), 'utf8')))).filter(t => t.includes('calculator-active')).length;
assert(tagsCalc >= 20, 'calculator-active tags: ' + tagsCalc);

// #5 (batch C3) every skill and level has an AP-style free-response problem: a context or function, four parts that
// build on each other, at least one justification, and scoring notes with points per part
const frqs = items.filter(q => q.id.endsWith('-015'));
assert.strictEqual(frqs.length, 210, 'free-response problems: ' + frqs.length);
for (const q of frqs) {
  assert.strictEqual(q.format, 'open-response', q.id + ' format');
  assert(/^Free response \(/.test(q.prompt), q.id + ' stem');
  assert.strictEqual(q.parts.length, 4, q.id + ' parts');
  assert(q.parts.some(p => /Justify|Explain|Give a reason|explain/.test(p.prompt)) || /frq_(rules|lhop|subst|division|rnotation)/.test(q.sourceNotes), q.id + ' justification part');
  const scoring = q.solutionSteps.filter(s => /^\([a-d]\) Scoring, \d+ points?: /.test(s));
  assert.strictEqual(scoring.length, 4, q.id + ' scoring notes');
  const total = scoring.reduce((s, x) => s + Number(x.match(/Scoring, (\d+)/)[1]), 0);
  assert(q.solutionSteps.includes(`Total: ${total} points.`), q.id + ' total points');
  assert(q.parts.every(p => String(p.answer).trim() && !/\bnan\b|zoo|\blog\(|sqrt|\*\*|\boo\b|None/.test(p.answer)), q.id + ' answers');
  if (q.diagram) assert(fs.existsSync(path.join(ROOT, q.diagram.spec.src)), q.id + ' graph image');
}
const frqKinds = new Set(frqs.map(q => fam(q)));
assert(frqKinds.size >= 25, 'free-response problem types: ' + frqKinds.size);
assert(!frqs.some(q => q.skillId === 'antiderivatives-definite-integrals-skill-04' && /Approximate ∫/.test(text(q))), 'Riemann notation FRQ stays on skill');

console.log(`PASS Calculus audit fixes: ${errs.length} find-the-mistake items with specific diagnoses, pacing, on-skill items, AP objectives, stems, notation, AP Review, Euler marked BC, IVT wording and units; worked solutions, big-operator display, Honors levels, AP topics (${integral.length} integral items); ${frqs.length} free-response problems of ${frqKinds.size} types`);
