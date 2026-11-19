// 4th Grade Math audit #9 (2026-11-19): Graphing Practice beyond line plots.
// 22 number-line items in the two fraction units: place a fraction equal to another, place fractions to order them,
// tenths as decimals, mixed numbers, a sum of like fractions and a whole number times a fraction. Every target and
// feedback vector is checked against the site's grader (core/plot.js); answer keys are drawn with the site's renderer.
// Writes tools/grade4-audit-20261119/plots.json (read by plots.py) and question-banks/assets/plot-keys/<id>.png.
// Usage: NODE_PATH=/opt/npm-tools/node_modules CHROME=/usr/bin/google-chrome node tools/grade4-audit-20261119/plots.cjs [--no-render]
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
// [unit, skill, level, family, prompt, number line {max, den}, target values [num] over den, answer text, steps, alt]
function nl(unit, skill, lv, fam, prompt, max, den, nums, steps) {
  const vals = nums.map((v) => `${v}/${den}`);
  const wrongVals = nums.map((v) => `${nums.every((x) => x + 1 <= max * den) ? v + 1 : v - 1}/${den}`);
  const plot = {
    tool: 'number-line-point', numberLine: { min: 0, max, tick: `1/${den}`, labelEvery: den, snap: `1/${den}` }, target: { values: vals },
    feedback: { position: 'Not quite. Count the equal parts from 0 and try again.', count: 'Check how many points you need to place.' },
    testVectors: { correct: { values: vals }, wrong: [{ response: { values: wrongVals }, expectCode: 'position' }, ...(nums.length > 1 ? [{ response: { values: vals.slice(1) }, expectCode: 'count' }] : [])] }
  };
  items.push({ unit, skill, lv, fam, prompt, plot, answer: nums.map((v) => show(v, den)).join(', '), steps,
    alt: `Number line from 0 to ${max} in ${NAME[den]}; ${nums.length > 1 ? 'dots' : 'a dot'} at ${nums.map((v) => show(v, den)).join(' and ')}.` });
}
const FE = 'fractions-equivalent-fractions', FD = 'fraction-operations-decimals';
// The site's number line labels every tick with its value, so only denominators with exact decimals are used
// (halves, fourths, fifths, eighths, tenths) and at most 12 ticks.
// Understanding equivalent fractions (skill 1): place points equal to given fractions
for (const [lv, fr, den] of [['cp2', [[1, 2]], 4], ['cp2', [[1, 2]], 8], ['cp1', [[3, 4]], 8], ['cp1', [[2, 5]], 10], ['honors', [[1, 2], [3, 4]], 8], ['honors', [[1, 5], [1, 2]], 10]])
  nl(FE, 1, lv, 'fe1_plot_equivalent', `The number line from 0 to 1 is split into ${NAME[den]}. Place ${fr.length > 1 ? 'a dot at each point' : 'the dot at the point'} equal to ${fr.map(([a, b]) => `${a}/${b}`).join(' and ')}.`, 1, den,
    fr.map(([a, b]) => a * den / b), [fr.map(([a, b]) => `${a}/${b} = ${a * den / b}/${den}`).join('; ') + ` (multiply the numerator and denominator by the same number).`, `Count ${NAME[den]} from 0.`]);
// Ordering fractions (skill 5): place two or three fractions on eighths
for (const [lv, fr] of [['cp2', [[1, 4], [5, 8]]], ['cp2', [[3, 8], [1, 2]]], ['cp1', [[3, 4], [5, 8]]], ['cp1', [[1, 8], [1, 4]]], ['honors', [[3, 4], [5, 8], [7, 8]]], ['honors', [[1, 2], [3, 8], [1, 4]]]])
  nl(FE, 5, lv, 'fe5_plot_order', `The number line from 0 to 1 is split into eighths. Place a dot at each fraction: ${fr.map(([a, b]) => `${a}/${b}`).join(', ')}. Then the dots show the order from least to greatest.`, 1, 8,
    fr.map(([a, b]) => a * 8 / b).sort((x, y) => x - y), [`In eighths: ${fr.map(([a, b]) => `${a}/${b} = ${a * 8 / b}/8`).join(', ')}.`, 'The dot farthest to the left is the least.']);
// Tenths as decimals (skill 5) and mixed numbers (skill 3), sums (skill 2), whole number times a fraction (skill 4)
for (const [lv, t] of [['cp2', 7], ['cp1', 4]])
  nl(FD, 5, lv, 'fd5_plot_decimal', `The number line from 0 to 1 is split into tenths. Drag the dot to 0.${t}.`, 1, 10, [t], [`0.${t} = ${t}/10.`, `Count ${t} tenths from 0.`]);
for (const [lv, w, a, den] of [['cp2', 1, 1, 4], ['cp1', 2, 3, 4], ['honors', 2, 1, 2]])
  nl(FD, 3, lv, 'fd3_plot_mixed', `The number line from 0 to 3 is split into ${NAME[den]}. Drag the dot to ${w} ${a}/${den}.`, 3, den, [w * den + a], [`${w} ${a}/${den} = ${w * den + a}/${den}.`, `Count ${w} whole${w > 1 ? 's' : ''} and then ${a} more ${a > 1 ? NAME[den] : NAME[den].replace(/s$/, '').replace('halve', 'half')}.`]);
for (const [lv, a, b, den, max] of [['cp2', 3, 2, 8, 1], ['cp1', 3, 4, 4, 2], ['honors', 3, 4, 5, 2]])
  nl(FD, 2, lv, 'fd2_plot_sum', `Start at ${a}/${den} and jump ${b}/${den} more. The number line from 0 to ${max} is split into ${NAME[den]}. Drag the dot to where you land.`, max, den, [a + b], [`${a}/${den} + ${b}/${den} = ${a + b}/${den}${a + b > den ? ' = ' + show(a + b, den) : ''}.`, `Count ${a + b} ${NAME[den]} from 0.`]);
for (const [lv, k, a, den] of [['cp1', 3, 2, 5], ['honors', 3, 3, 4]])
  nl(FD, 4, lv, 'fd4_plot_product', `The number line from 0 to 3 is split into ${NAME[den]}. Drag the dot to ${k} × ${a}/${den}.`, 3, den, [k * a], [`${k} × ${a}/${den} = ${k * a}/${den}${k * a > den ? ' = ' + show(k * a, den) : ''}.`, `Count ${k * a} ${NAME[den]} from 0.`]);
assert.equal(items.length, 22);

const ABBR = { [FE]: 'fe', [FD]: 'fd' };
const out = [], keys = [], count = {};
for (const it of items) {
  const k = ABBR[it.unit] + it.skill + it.lv; count[k] = (count[k] || 0) + 1;
  const id = `m4-${ABBR[it.unit]}-s${String(it.skill).padStart(2, '0')}-${it.lv}-p${String(count[k]).padStart(3, '0')}`;
  const plot = { ...it.plot, answerKey: { src: `question-banks/assets/plot-keys/${id}.png`, alt: it.alt }, check: { type: 'exact-after-snap' } };
  assert(P.valid(plot), id + ' valid');
  assert.equal(P.check(plot, plot.testVectors.correct).ok, true, id + ' correct');
  for (const w of plot.testVectors.wrong) { const r = P.check(plot, w.response); assert.equal(r.ok, false, id); assert.equal(r.code, w.expectCode, id); assert(plot.feedback[r.code], id); }
  out.push({ id, unit: it.unit, skillId: `${it.unit}-skill-${String(it.skill).padStart(2, '0')}`, level: it.lv, format: 'plot', prompt: it.prompt, answer: it.answer, solutionSteps: it.steps,
    sourceNotes: `Original Claude-authored item (family: ${it.fam}). 4th Grade Math audit 2026-11-19 (#9, Graphing Practice); target and feedback vectors checked against core/plot.js by tools/grade4-audit-20261119/plots.cjs.`, plot });
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
