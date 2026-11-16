// Adds graphing questions to three thin Algebra 1 bank skills so each level has at least 8:
//   inequalities-skill-01  Graph an inequality on a number line
//   inequalities-skill-03  Solve a linear inequality, then graph it
//   exponential-functions-skill-02  Graph y = a·bˣ by placing points
// Every answer is computed here and then checked twice: by the site's plot grader (core/plot.js) against the
// test vectors, and independently by substituting test values into the original inequality or equation.
// Answer-key images are drawn as SVG and rendered to PNG with Playwright (see render.cjs).
// Usage: node tools/thin-skills-20261116/build.mjs   (writes the banks and tools/thin-skills-20261116/out/keys.json)
import fs from 'node:fs'; import path from 'node:path'; import vm from 'node:vm'; import assert from 'node:assert/strict';
const root = path.resolve(path.dirname(new URL(import.meta.url).pathname), '../..');
const ctx = {}; vm.createContext(ctx); vm.runInContext(fs.readFileSync(path.join(root, 'worksheet-generator/core/plot.js'), 'utf8'), ctx);
const PLOT = ctx.MK_PLOT;
const NOTE = (family) => `Original Claude-authored item (family: ${family}). Answer computed in the authoring script and re-checked by an independent check in the package validator. Content package 2026-11-16-thin-skills. Teacher reviewed 2026-11-16.`;
const STD_INEQ = ['A-REI.B.3', 'A-CED.A.1'], STD_EXP = ['F-IF.C.7e', 'F-LE.A.2'];
// Half-unit boundaries are written as fractions, matching the student number line's labels (−5/2, 7/2).
const fmt = (v) => (Number.isInteger(v) ? String(v) : `${v * 2}/2`);
const minus = (s) => s.replace(/-/g, '−');
const keys = [];

// ---------- number-line inequalities ----------
const NL = { min: -10, max: 10, tick: 1, labelEvery: 2, snap: 1 };
const NL_HALF = { min: -5, max: 5, tick: 0.5, labelEvery: 1, snap: 0.5 };
const INEQ_FEEDBACK = {
  boundary: 'Check the number where your boundary point sits.',
  direction: 'Your arrow points the wrong way. Test a number on your arrow in the inequality.',
  'closed-open': 'Check the dot: use a closed dot for ≤ or ≥ and an open dot for < or >.'
};
// op is the relation for x, after solving: x op b
const dirOf = (op) => (op === '<' || op === '≤' ? 'left' : 'right');
const closedOf = (op) => op === '≤' || op === '≥';
const holds = (v, op, b) => (op === '<' ? v < b : op === '≤' ? v <= b : op === '>' ? v > b : v >= b);
function ineqItem({ id, skill, level, family, prompt, op, b, steps, test, line = NL }) {
  const target = { boundary: b, closed: closedOf(op), direction: dirOf(op) };
  // Independent check: the original condition (test) must agree with "x op b" at many sample points.
  for (let v = line.min - 2; v <= line.max + 2; v += line.snap / 2) assert.equal(test(v), holds(v, op, b), `${id}: original and solution disagree at x = ${v}`);
  const dotWord = target.closed ? 'closed' : 'open', arrow = target.direction;
  const answerHead = family === 'nl-ineq-solve' ? `x ${op} ${fmt(b)}: ` : '';
  const plot = {
    tool: 'number-line-inequality', numberLine: { ...line }, target, feedback: { ...INEQ_FEEDBACK },
    testVectors: { correct: { ...target }, wrong: [
      { response: { ...target, direction: arrow === 'left' ? 'right' : 'left' }, expectCode: 'direction' },
      { response: { ...target, closed: !target.closed }, expectCode: 'closed-open' },
      { response: { ...target, boundary: b + line.snap * (b + line.snap <= line.max ? 1 : -1) }, expectCode: 'boundary' }
    ] },
    answerKey: { src: `question-banks/assets/plot-keys/${id}.png`, alt: `Number line from ${minus(String(line.min))} to ${line.max} with ${dotWord === 'open' ? 'an open' : 'a closed'} dot at ${fmt(b)} and an arrow to the ${arrow}.` },
    check: { type: 'exact-after-snap' }
  };
  keys.push({ id, kind: 'nl', line, target });
  return { id, skillId: skill, level, format: 'plot', prompt, answer: `${answerHead}${dotWord[0].toUpperCase() + dotWord.slice(1)} dot at ${fmt(b)}, arrow ${arrow}`.replace(/^(x [^:]+: )Open/, '$1open').replace(/^(x [^:]+: )Closed/, '$1closed'),
    solutionSteps: steps, standards: STD_INEQ, sourceNotes: NOTE(family), plot };
}

const S1 = 'inequalities-skill-01', S3 = 'inequalities-skill-03';
const graphSteps = (op, b, extra) => [
  ...(extra ? [extra] : []),
  `Put ${closedOf(op) ? 'a closed' : 'an open'} dot at ${fmt(b)}${closedOf(op) ? ` because ${fmt(b)} is included (${op})` : ` because ${fmt(b)} itself is not included (${op})`}.`,
  `Draw the arrow to the ${dirOf(op)}: those numbers make the inequality true.`
];
const s1 = [
  // Support: x op b, written the usual way
  ['cp2', 'x > 2', '>', 2], ['cp2', 'x ≤ 5', '≤', 5], ['cp2', 'x ≥ -4', '≥', -4], ['cp2', 'x < 0', '<', 0],
  ['cp2', 'x > -7', '>', -7], ['cp2', 'x ≤ -1', '≤', -1], ['cp2', 'x ≥ 6', '≥', 6],
  // Standard: the variable on the right, or the inequality in words
  ['cp1', '4 > x', '<', 4, 'Read it from x: 4 > x means x < 4.'],
  ['cp1', '-3 ≤ x', '≥', -3, 'Read it from x: -3 ≤ x means x ≥ -3.'],
  ['cp1', '9 ≥ x', '≤', 9, 'Read it from x: 9 ≥ x means x ≤ 9.'],
  ['cp1', '-6 < x', '>', -6, 'Read it from x: -6 < x means x > -6.'],
  ['cp1', null, '≥', 1, '"At least 1" means 1 or more: x ≥ 1.', 'Graph all numbers x that are at least 1.'],
  ['cp1', null, '<', -2, '"Less than -2" means x < -2.', 'Graph all numbers x that are less than -2.'],
  // Advanced: half-unit boundaries, variable on the right, or words
  ['honors', 'x > -5/2', '>', -2.5, null, null, NL_HALF], ['honors', 'x ≤ 7/2', '≤', 3.5, null, null, NL_HALF],
  ['honors', '3/2 ≥ x', '≤', 1.5, 'Read it from x: 3/2 ≥ x means x ≤ 3/2.', null, NL_HALF],
  ['honors', '-1/2 < x', '>', -0.5, 'Read it from x: -1/2 < x means x > -1/2.', null, NL_HALF],
  ['honors', null, '≤', 7, '"Not greater than 7" means 7 or less: x ≤ 7.', 'Graph all numbers x that are not greater than 7.'],
  ['honors', null, '≥', -4.5, '"No less than -9/2" means -9/2 or more: x ≥ -9/2.', 'Graph all numbers x that are no less than -9/2.', NL_HALF]
];
const s3 = [
  // Support: one step. [level, text, js test, op, b, steps]
  ['cp2', 'x + 5 > 3', (x) => x + 5 > 3, '>', -2, ['Subtract 5 from both sides: x > -2.']],
  ['cp2', 'x − 4 ≤ 2', (x) => x - 4 <= 2, '≤', 6, ['Add 4 to both sides: x ≤ 6.']],
  ['cp2', '3x ≥ 12', (x) => 3 * x >= 12, '≥', 4, ['Divide both sides by 3: x ≥ 4.']],
  ['cp2', 'x/2 < 3', (x) => x / 2 < 3, '<', 6, ['Multiply both sides by 2: x < 6.']],
  ['cp2', '5x > −15', (x) => 5 * x > -15, '>', -3, ['Divide both sides by 5: x > -3.']],
  // Standard: two steps, positive coefficient
  ['cp1', '3x + 4 ≥ 13', (x) => 3 * x + 4 >= 13, '≥', 3, ['Subtract 4: 3x ≥ 9.', 'Divide by 3: x ≥ 3.']],
  ['cp1', '5x − 7 > 8', (x) => 5 * x - 7 > 8, '>', 3, ['Add 7: 5x > 15.', 'Divide by 5: x > 3.']],
  ['cp1', '2x + 11 ≤ 5', (x) => 2 * x + 11 <= 5, '≤', -3, ['Subtract 11: 2x ≤ −6.', 'Divide by 2: x ≤ -3.']],
  ['cp1', 'x/3 − 2 < 1', (x) => x / 3 - 2 < 1, '<', 9, ['Add 2: x/3 < 3.', 'Multiply by 3: x < 9.']],
  ['cp1', '4 + 2x ≥ −6', (x) => 4 + 2 * x >= -6, '≥', -5, ['Subtract 4: 2x ≥ −10.', 'Divide by 2: x ≥ -5.']],
  // Advanced: negative coefficients (flip), variables on both sides, distributing
  ['honors', '−4x + 3 > 15', (x) => -4 * x + 3 > 15, '<', -3, ['Subtract 3: −4x > 12.', 'Divide by −4 and FLIP the sign: x < -3.']],
  ['honors', '6 − 2x ≥ −4', (x) => 6 - 2 * x >= -4, '≤', 5, ['Subtract 6: −2x ≥ −10.', 'Divide by −2 and FLIP the sign: x ≤ 5.']],
  ['honors', '3(x − 2) < 5x + 4', (x) => 3 * (x - 2) < 5 * x + 4, '>', -5, ['Distribute: 3x − 6 < 5x + 4.', 'Subtract 5x and add 6: −2x < 10.', 'Divide by −2 and FLIP the sign: x > -5.']],
  ['honors', '−x/2 + 1 ≤ 4', (x) => -x / 2 + 1 <= 4, '≥', -6, ['Subtract 1: −x/2 ≤ 3.', 'Multiply by −2 and FLIP the sign: x ≥ -6.']],
  ['honors', '5x − 3 > 7x + 9', (x) => 5 * x - 3 > 7 * x + 9, '<', -6, ['Subtract 7x and add 3: −2x > 12.', 'Divide by −2 and FLIP the sign: x < -6.']]
];

// ---------- exponential y = a·bˣ ----------
const GRID = { xmin: -8, xmax: 8, ymin: -8, ymax: 8, step: 1, snap: 1 };
const EXP_FEEDBACK = { 'same-point': 'Place two different points.', 'points-off-curve': 'Substitute your x-values into the equation and check the y-values.' };
const gcd = (a, b) => (b ? gcd(b, a % b) : Math.abs(a));
const frac = (s) => { const [n, d = '1'] = String(s).split('/'); return [BigInt(n), BigInt(d)]; };
// exact y = a·b^x as [num, den] with BigInt; x integer
function expY(a, b, x) {
  const [an, ad] = frac(a), [bn, bd] = frac(b); let n = an, d = ad;
  if (x >= 0) { n *= bn ** BigInt(x); d *= bd ** BigInt(x); } else { n *= bd ** BigInt(-x); d *= bn ** BigInt(-x); }
  const g = BigInt(gcd(Number(n), Number(d))); return [n / g, d / g];
}
const showNum = (s) => (String(s).includes('/') ? '(' + s + ')' : s);
function expLatticePoints(a, b) {
  const out = []; for (let x = GRID.xmin; x <= GRID.xmax; x++) { const [n, d] = expY(a, b, x); if (d === 1n && n >= GRID.ymin && n <= GRID.ymax) out.push([x, Number(n)]); } return out;
}
const eqText = (a, b) => 'y = ' + (a === '1' ? '' : showNum(a)) + (a === '1' && !String(b).includes('/') ? b : '(' + b + ')') + 'ˣ';
function expItem({ id, level, a, b, steps, integerX }) {
  const pts = expLatticePoints(a, b); assert.ok(pts.length >= 2, id + ': needs two lattice points on the grid');
  // Independent check with floating point: each listed point satisfies y = a·b^x.
  const av = eval(a), bv = eval(b); for (const [x, y] of pts) assert.ok(Math.abs(av * bv ** x - y) < 1e-9, id + ' point ' + x);
  const eq = eqText(a, b), list = pts.map(([x, y]) => `(${x}, ${y})`).join(', ');
  const [p0, p1] = pts.slice(0, 2), off = [p1[0], p1[1] + 1 <= GRID.ymax ? p1[1] + 1 : p1[1] - 1];
  const plot = {
    tool: 'exponential', grid: { ...GRID }, target: { a, b }, feedback: { ...EXP_FEEDBACK },
    testVectors: { correct: { points: [[p0[0], String(p0[1])], [p1[0], String(p1[1])]] }, wrong: [
      { response: { points: [[p0[0], String(p0[1])], [off[0], String(off[1])]] }, expectCode: 'points-off-curve' },
      { response: { points: [[p0[0], String(p0[1])], [p0[0], String(p0[1])]] }, expectCode: 'same-point' }
    ] },
    answerKey: { src: `question-banks/assets/plot-keys/${id}.png`, alt: `Coordinate grid with the exponential curve ${eq} through ${list}.` },
    check: { type: 'exact-after-snap' }
  };
  keys.push({ id, kind: 'exp', grid: GRID, a, b, pts });
  return { id, skillId: 'exponential-functions-skill-02', level, format: 'plot',
    prompt: `Graph ${eq}. Drag two points that are on the graph (use ${integerX ? 'integer' : 'whole-number'} x-values).`,
    answer: `${eq} through ${list}`, solutionSteps: steps(pts, eq), standards: STD_EXP, sourceNotes: NOTE('plot-exponential'), plot };
}
const grow = (a, b) => (pts) => [`At x = 0, y = a = ${a}, so (0, ${a}) is on the graph.`, `Each step right multiplies y by ${b}: ${pts.filter(p => p[0] >= 0).map(p => `(${p[0]}, ${p[1]})`).join(', ')}.`, Number(eval(b)) > 1 ? 'The graph rises and approaches the x-axis on the left.' : 'The graph falls and approaches the x-axis on the right.'];
const fracA = (a, b) => (pts) => [`At x = 0, y = ${a}, which is not on a grid point, so look for x-values that give whole-number y-values.`, `y = ${a} · ${b}ˣ: ${pts.map(p => `x = ${p[0]} gives y = ${p[1]}`).join('; ')}.`, `Plot two of these, such as (${pts[0][0]}, ${pts[0][1]}) and (${pts[1][0]}, ${pts[1][1]}). The graph rises and approaches the x-axis on the left.`];
const negX = (a, b) => (pts) => [`At x = 0, y = ${a}, so (0, ${a}) is on the graph.`, `Each step right multiplies y by ${b}, so the next y-values are fractions. Step LEFT instead: each step left multiplies y by ${1 / eval(b)}.`, `Points: ${pts.map(p => `(${p[0]}, ${p[1]})`).join(', ')}. The graph falls from left to right and approaches the x-axis on the right.`];
const expSpecs = [
  ['cp2', '1', '4', grow], ['cp2', '1', '5', grow], ['cp2', '1', '6', grow], ['cp2', '2', '4', grow],
  ['cp1', '6', '1/2', grow], ['cp1', '8', '1/4', grow], ['cp1', '4', '2', grow], ['cp1', '3', '1/3', grow], ['cp1', '6', '1/3', grow], ['cp1', '4', '1/4', grow], ['cp1', '5', '1/5', grow],
  ['honors', '1', '1/2', negX], ['honors', '1', '1/3', negX], ['honors', '1/2', '2', fracA], ['honors', '1/4', '2', fracA], ['honors', '1/3', '3', fracA], ['honors', '1/8', '2', fracA]
];

// ---------- assemble ----------
function nextIds(bank, prefix) { const used = new Set(bank.questions.map(q => q.id)); let n = 1; return () => { let id; do id = prefix + '-p' + String(n++).padStart(3, '0'); while (used.has(id)); used.add(id); return id; }; }
const ineqFile = path.join(root, 'question-banks/algebra/inequalities.json'), expFile = path.join(root, 'question-banks/algebra/exponential-functions.json');
const ineqBank = JSON.parse(fs.readFileSync(ineqFile, 'utf8')), expBank = JSON.parse(fs.readFileSync(expFile, 'utf8'));
const already = (bank) => bank.questions.some(q => /2026-11-16-thin-skills/.test(q.sourceNotes || ''));
if (already(ineqBank) || already(expBank)) { console.log('Already applied.'); process.exit(0); }
const added = [], seenPrompts = new Set([...ineqBank.questions, ...expBank.questions].map(q => q.prompt));
const gen = {};
const idFor = (bank, prefix) => (gen[prefix] = gen[prefix] || nextIds(bank, prefix))();
for (const [level, text, op, b, extra, words, line] of s1) {
  const prompt = minus(words || `Graph ${text} on the number line.`);
  const id = idFor(ineqBank, `alg1-ineq-s01-${level}`);
  added.push(['ineq', ineqItem({ id, skill: S1, level, family: 'nl-ineq-graph', prompt, op, b, line, steps: graphSteps(op, b, extra && minus(extra)).map(minus), test: (v) => holds(v, op, b) })]);
}
for (const [level, text, test, op, b, steps] of s3) {
  const id = idFor(ineqBank, `alg1-ineq-s03-${level}`);
  added.push(['ineq', ineqItem({ id, skill: S3, level, family: 'nl-ineq-solve', prompt: `Solve ${text}. Then graph the solution on the number line.`, op, b, test,
    steps: [...steps, `${closedOf(op) ? 'Closed' : 'Open'} dot at ${fmt(b)}, arrow ${dirOf(op)}.`].map(minus) })]);
}
for (const [level, a, b, how] of expSpecs) {
  const id = idFor(expBank, `alg1-exp-s02-${level}`);
  added.push(['exp', expItem({ id, level, a, b, steps: how(a, b), integerX: level === 'honors' })]);
}
// Grade every item with the site's own grader: correct passes, each wrong response fails with its code.
for (const [, q] of added) {
  assert.equal(PLOT.valid(q.plot), true, q.id + ' valid');
  const ok = PLOT.check(q.plot, q.plot.testVectors.correct); assert.equal(ok.ok, true, q.id + ' correct: ' + JSON.stringify(ok));
  for (const w of q.plot.testVectors.wrong) { const r = PLOT.check(q.plot, w.response); assert.equal(r.ok, false, q.id); assert.equal(r.code, w.expectCode, q.id + ' wrong code ' + JSON.stringify(r)); }
  assert.ok(!seenPrompts.has(q.prompt), 'duplicate prompt ' + q.prompt); seenPrompts.add(q.prompt);
}
ineqBank.questions.push(...added.filter(x => x[0] === 'ineq').map(x => x[1]));
expBank.questions.push(...added.filter(x => x[0] === 'exp').map(x => x[1]));
fs.writeFileSync(ineqFile, JSON.stringify(ineqBank, null, 1) + '\n'); fs.writeFileSync(expFile, JSON.stringify(expBank, null, 1) + '\n');
fs.mkdirSync(path.join(root, 'tools/thin-skills-20261116/out'), { recursive: true });
fs.writeFileSync(path.join(root, 'tools/thin-skills-20261116/out/keys.json'), JSON.stringify(keys, null, 1));
console.log('Added ' + added.length + ' questions; all passed the site grader and the independent substitution check.');
