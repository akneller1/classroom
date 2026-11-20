// 3rd Grade Math audit #13 (2026-11-19): number-line graphing for equivalent and comparing fractions.
// 9 number-line items in the equivalent and comparing fractions unit: place the fraction equal to another (3.NF.A.3.a),
// a whole number as a fraction (3.NF.A.3.c) and two fractions to compare (3.NF.A.3.d), three per level. Every target and
// feedback vector is checked against the site's grader (core/plot.js); answer keys are drawn with the site's renderer.
// Writes tools/grade3-audit-20261119/plots.json (read by plots.py) and question-banks/assets/plot-keys/<id>.png.
// Usage: NODE_PATH=/opt/npm-tools/node_modules CHROME=/usr/bin/google-chrome node tools/grade3-audit-20261119/plots.cjs [--no-render]
'use strict';
const fs = require('node:fs'), path = require('node:path'), vm = require('node:vm'), assert = require('node:assert/strict');
const ROOT = path.resolve(__dirname, '../..');
const ctx = {}; vm.createContext(ctx);
vm.runInContext(fs.readFileSync(path.join(ROOT, 'worksheet-generator/core/plot.js'), 'utf8'), ctx);
const P = ctx.MK_PLOT;
const NAME = { 2: 'halves', 3: 'thirds', 4: 'fourths', 5: 'fifths', 6: 'sixths', 8: 'eighths', 10: 'tenths', 12: 'twelfths' };
const gcd = (a, b) => (b ? gcd(b, a % b) : a);
const show = (n, d) => { const g = gcd(n, d); n /= g; d /= g; if (d === 1) return String(n); return n > d ? `${Math.floor(n / d)} ${n % d}/${d}` : `${n}/${d}`; };
const items = [];
function nl(unit, skill, lv, fam, prompt, max, den, nums, steps) {
  const vals = nums.map((v) => `${v}/${den}`);
  const wrongVals = nums.map((v) => `${nums.every((x) => x + 1 <= max * den) ? v + 1 : v - 1}/${den}`);
  const plot = {
    tool: 'number-line-point', numberLine: { min: 0, max, tick: `1/${den}`, labelEvery: den, snap: `1/${den}` }, target: { values: vals },
    feedback: { position: 'Not quite. Count the equal parts from 0 and try again.', count: 'Check how many points you need to place.' },
    testVectors: { correct: { values: vals }, wrong: [{ response: { values: wrongVals }, expectCode: 'position' }, ...(nums.length > 1 ? [{ response: { values: vals.slice(1) }, expectCode: 'count' }] : [])] }
  };
  items.push({ unit, skill, lv, fam, prompt, plot, answer: nums.map((v) => `${v}/${den}`).join(', '), steps,
    alt: `Number line from 0 to ${max} in ${NAME[den]}; ${nums.length > 1 ? 'dots' : 'a dot'} at ${nums.map((v) => `${v}/${den}`).join(' and ')}.` });
}
const EC = 'equivalent-comparing-fractions';
// The site's number line labels every tick with its value, so only halves, fourths and eighths are used.
// Equivalent fractions (skill 1): place the point in smaller parts that names the same amount
for (const [lv, a, b, den] of [['cp2', 1, 2, 4], ['cp1', 1, 4, 8], ['honors', 3, 4, 8]])
  nl(EC, 1, lv, 'ec1_plot_equivalent', `The number line from 0 to 1 is split into ${NAME[den]}. Drag the dot to the fraction in ${NAME[den]} that equals ${a}/${b}.`, 1, den, [a * den / b],
    [`Each 1/${b} is ${den / b} ${NAME[den]}.`, `${a}/${b} = ${a * den / b}/${den}.`]);
// Whole numbers as fractions (skill 3)
for (const [lv, w, den] of [['cp2', 1, 2], ['cp1', 2, 4], ['honors', 3, 4]])
  nl(EC, 3, lv, 'ec3_plot_whole', `The number line from 0 to 3 is split into ${NAME[den]}. Drag the dot to ${w * den}/${den}.`, 3, den, [w * den],
    [`${w * den}/${den} is ${w * den} ${NAME[den]}.`, `${w * den} ${NAME[den]} = ${w} whole${w > 1 ? 's' : ''}.`]);
// Comparing with the same denominator (skill 4): place both, the one farther right is greater
for (const [lv, den, a, b] of [['cp2', 4, 1, 3], ['cp1', 8, 5, 2], ['honors', 8, 7, 3]])
  nl(EC, 4, lv, 'ec4_plot_compare', `The number line from 0 to 1 is split into ${NAME[den]}. Place a dot at ${a}/${den} and a dot at ${b}/${den}. The dot farther to the right is the greater fraction.`, 1, den,
    [a, b].sort((x, y) => x - y), [`Count ${a} and ${b} ${NAME[den]} from 0.`, `${Math.max(a, b)}/${den} is farther right, so ${Math.max(a, b)}/${den} > ${Math.min(a, b)}/${den}.`]);
assert.equal(items.length, 9);

const ABBR = { [EC]: 'ec' };
const out = [], keys = [], count = {};
for (const it of items) {
  const k = ABBR[it.unit] + it.skill + it.lv; count[k] = (count[k] || 0) + 1;
  const id = `m3-${ABBR[it.unit]}-s${String(it.skill).padStart(2, '0')}-${it.lv}-p${String(count[k]).padStart(3, '0')}`;
  const plot = { ...it.plot, answerKey: { src: `question-banks/assets/plot-keys/${id}.png`, alt: it.alt }, check: { type: 'exact-after-snap' } };
  assert(P.valid(plot), id + ' valid');
  assert.equal(P.check(plot, plot.testVectors.correct).ok, true, id + ' correct');
  for (const w of plot.testVectors.wrong) { const r = P.check(plot, w.response); assert.equal(r.ok, false, id); assert.equal(r.code, w.expectCode, id); assert(plot.feedback[r.code], id); }
  out.push({ id, unit: it.unit, skillId: `${it.unit}-skill-${String(it.skill).padStart(2, '0')}`, level: it.lv, format: 'plot', prompt: it.prompt, answer: it.answer, solutionSteps: it.steps,
    sourceNotes: `Original Claude-authored item (family: ${it.fam}). 3rd Grade Math audit 2026-11-19 (#13, Graphing Practice); target and feedback vectors checked against core/plot.js by tools/grade3-audit-20261119/plots.cjs.`, plot });
  keys.push({ id, svg: P.blank(plot, plot.testVectors.correct) });
}
fs.writeFileSync(path.join(__dirname, 'plots.json'), JSON.stringify(out, null, 1) + '\n');
console.log('plot items', out.length);
if (!process.argv.includes('--no-render')) (async () => {
  const { chromium } = require('playwright');
  const browser = await chromium.launch(process.env.CHROME ? { executablePath: process.env.CHROME } : {});
  const page = await browser.newPage({ deviceScaleFactor: 1 });
  for (const k of keys) {
    await page.setContent(`<!doctype html><html><body style="margin:0;background:white;font-family:Inter,Arial,sans-serif"><div id="k" style="display:inline-block;width:480px">${k.svg}</div></body></html>`);
    await page.locator('#k').screenshot({ path: path.join(ROOT, 'question-banks/assets/plot-keys', k.id + '.png') });
  }
  await browser.close();
  console.log('rendered', keys.length, 'answer keys');
})().catch((e) => { console.error(e); process.exit(1); });
