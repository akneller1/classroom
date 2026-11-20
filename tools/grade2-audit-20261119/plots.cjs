// 2nd Grade Math audit #15 (2026-11-19): line plots of whole-number measurements (2.MD.D.9) in Graphing Practice.
// 9 line-plot items for measuring-length skill 6, three per level. Every target and feedback vector is checked against
// the site's grader (core/plot.js); answer keys are drawn with the site's renderer.
// Writes tools/grade2-audit-20261119/plots.json (read by plots.py) and question-banks/assets/plot-keys/<id>.png.
// Usage: NODE_PATH=/opt/npm-tools/node_modules CHROME=/usr/bin/google-chrome node tools/grade2-audit-20261119/plots.cjs [--no-render]
'use strict';
const fs = require('node:fs'), path = require('node:path'), vm = require('node:vm'), assert = require('node:assert/strict');
const ROOT = path.resolve(__dirname, '../..');
const ctx = {}; vm.createContext(ctx);
vm.runInContext(fs.readFileSync(path.join(ROOT, 'worksheet-generator/core/plot.js'), 'utf8'), ctx);
const P = ctx.MK_PLOT;
const UNIT = 'measuring-length', SKILL = 'measuring-length-skill-06';
// [level, what, unit, min, max, data]
const SETS = [
  ['cp2', 'pencils', 'inches', 2, 7, [3, 4, 4, 5, 5, 5]], ['cp2', 'crayons', 'inches', 1, 6, [2, 3, 3, 3, 4, 4]], ['cp2', 'leaves', 'centimeters', 3, 8, [4, 5, 5, 6, 6, 7]],
  ['cp1', 'ribbons', 'inches', 4, 10, [5, 6, 6, 7, 7, 7, 8, 9]], ['cp1', 'shoes', 'inches', 5, 11, [6, 7, 7, 8, 8, 8, 9, 10]], ['cp1', 'sticks', 'centimeters', 10, 16, [11, 12, 12, 13, 13, 13, 14, 15]],
  ['honors', 'plants', 'centimeters', 12, 20, [13, 14, 14, 15, 15, 15, 16, 16, 18, 19]], ['honors', 'jumps', 'feet', 2, 9, [3, 4, 4, 5, 5, 5, 5, 6, 7, 8]], ['honors', 'paper strips', 'inches', 6, 14, [7, 8, 8, 9, 9, 9, 10, 10, 12, 13]]
];
const out = [], keys = [], count = {};
for (const [lv, what, unit, min, max, data] of SETS) {
  count[lv] = (count[lv] || 0) + 1;
  const id = `m2-ml-s06-${lv}-p${String(count[lv]).padStart(3, '0')}`;
  const list = data.slice(); for (let i = list.length - 1; i > 0; i--) { const j = (i * 7 + count[lv]) % (i + 1); [list[i], list[j]] = [list[j], list[i]]; }
  const vals = list.map(String);
  const tally = [...new Set(data)].sort((a, b) => a - b).map((v) => `${v}: ${data.filter((x) => x === v).length} X`).join('; ');
  const title = `Lengths of ${what[0].toUpperCase() + what.slice(1)}`;
  const shift = vals.map((v) => String(+v + 1 <= max ? +v + 1 : +v - 1));
  const plot = {
    tool: 'line-plot', title, units: unit, numberLine: { min: String(min), max: String(max), tick: '1', labelEvery: 1, snap: '1' },
    source: { type: 'list', values: vals }, target: { values: vals },
    feedback: { count: `Put one X for each measurement. There are ${vals.length} measurements.`, 'wrong-tick': 'At least one X is on the tick next to where it belongs. Count the ticks again.', position: 'Not quite. Find each length on the number line and check your X marks.' },
    testVectors: { correct: { marks: vals }, wrong: [{ response: { marks: vals.slice(1) }, expectCode: 'count' }, { response: { marks: [shift[0], ...vals.slice(1)] }, expectCode: 'wrong-tick' }] },
    check: { type: 'exact-after-snap' }, answerKey: { src: `question-banks/assets/plot-keys/${id}.png`, alt: `Line plot titled ${title} in ${unit}. ${tally}.` }
  };
  assert(P.valid(plot), id + ' valid');
  assert.equal(P.check(plot, plot.testVectors.correct).ok, true, id + ' correct');
  for (const w of plot.testVectors.wrong) { const r = P.check(plot, w.response); assert.equal(r.ok, false, id); assert.equal(r.code, w.expectCode, id + ' ' + r.code); assert(plot.feedback[r.code], id); }
  out.push({ id, unit: UNIT, skillId: SKILL, level: lv, format: 'plot', prompt: `The ${what} measured (${unit}): ${vals.join(', ')}. Make a line plot. Put one X for each measurement.`,
    answer: tally, solutionSteps: [`There are ${vals.length} measurements, so the line plot needs ${vals.length} X marks.`, `Stack an X above each length every time it appears: ${tally}.`],
    sourceNotes: 'Original Claude-authored item (family: ml6_plot_line_plot). 2nd Grade Math audit 2026-11-19 (#15, Graphing Practice); target and feedback vectors checked against core/plot.js by tools/grade2-audit-20261119/plots.cjs.', plot });
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
