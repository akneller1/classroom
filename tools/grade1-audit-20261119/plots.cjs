// 1st Grade Math audit #15 (2026-11-19): picture graphs and bar graphs for data skills 2 and 3 (1.MD.C.4).
// 18 items, three per level in each skill: make a picture graph from a tally chart (skill 2) and a bar graph from a
// tally chart (skill 3). Every target and feedback vector is checked against core/plot.js; answer keys are drawn with
// the site's renderer. Writes plots.json (read by plots.py) and question-banks/assets/plot-keys/<id>.png.
// Usage: NODE_PATH=/opt/npm-tools/node_modules CHROME=/usr/bin/google-chrome node tools/grade1-audit-20261119/plots.cjs [--no-render]
'use strict';
const fs = require('node:fs'), path = require('node:path'), vm = require('node:vm'), assert = require('node:assert/strict');
const ROOT = path.resolve(__dirname, '../..');
const ctx = {}; vm.createContext(ctx);
vm.runInContext(fs.readFileSync(path.join(ROOT, 'worksheet-generator/core/plot.js'), 'utf8'), ctx);
const P = ctx.MK_PLOT;
const SETS = {
  2: [['cp2', 'Snacks We Like', ['Apples', 'Grapes', 'Pears'], [3, 5, 2]], ['cp2', 'Our Pets', ['Dogs', 'Cats', 'Fish'], [4, 2, 6]], ['cp2', 'Weather This Week', ['Sunny', 'Rainy', 'Cloudy'], [2, 1, 4]],
      ['cp1', 'Favorite Colors', ['Red', 'Blue', 'Green'], [6, 8, 3]], ['cp1', 'Shapes in a Bag', ['Circles', 'Squares', 'Triangles'], [7, 4, 9]], ['cp1', 'Lunch Choices', ['Pizza', 'Tacos', 'Soup'], [9, 5, 7]],
      ['honors', 'Books Read', ['Ana', 'Ben', 'Cruz'], [11, 7, 10]], ['honors', 'Bugs Found', ['Ants', 'Bees', 'Beetles'], [12, 8, 9]], ['honors', 'Games at Recess', ['Tag', 'Ball', 'Jump rope'], [10, 12, 6]]],
  3: [['cp2', 'Toys in the Bin', ['Cars', 'Balls', 'Blocks'], [4, 2, 5]], ['cp2', 'Fruit in a Bowl', ['Apples', 'Bananas', 'Pears'], [3, 6, 1]], ['cp2', 'Birds We Saw', ['Robins', 'Crows', 'Jays'], [5, 3, 2]],
      ['cp1', 'Votes for a Class Pet', ['Fish', 'Frog', 'Hamster'], [8, 5, 9]], ['cp1', 'Stickers', ['Stars', 'Hearts', 'Moons'], [6, 9, 4]], ['cp1', 'How We Get to School', ['Walk', 'Bus', 'Car'], [7, 10, 5]],
      ['honors', 'Pages Read', ['Mon', 'Tue', 'Wed'], [12, 9, 11]], ['honors', 'Shells Collected', ['Mia', 'Leo', 'Kai'], [10, 12, 7]], ['honors', 'Seeds That Grew', ['Beans', 'Corn', 'Peas'], [11, 8, 12]]]
};
const FB = { count: 'Check each row. Every row needs symbols, and no row can have more than the graph allows.', swapped: 'Two rows are switched. Check which row goes with each name.', 'off-by-one': 'One row has one symbol too many or too few. Count that row again.', position: 'Not quite. Use the tally chart to count each row again.' };
const out = [], keys = [], count = {};
for (const skill of [2, 3]) for (const [lv, title, cats, counts] of SETS[skill]) {
  const k = skill + lv; count[k] = (count[k] || 0) + 1;
  const id = `m1-dt-s0${skill}-${lv}-p${String(count[k]).padStart(3, '0')}`;
  const swap = counts.slice(); const i = counts.findIndex((v, j) => j < 2 && v !== counts[j + 1]); [swap[i], swap[i + 1]] = [swap[i + 1], swap[i]];
  const off = counts.slice(); off[0] = off[0] + 1 <= 12 ? off[0] + 1 : off[0] - 1;
  const source = { type: 'tally', categories: cats, counts };
  let plot;
  if (skill === 2) plot = { tool: 'picture-graph', title, orientation: 'horizontal', categories: cats, key: { symbol: 'circle', value: 1 }, maxSymbols: 12, allowHalf: false, source, target: { values: counts }, feedback: FB,
    testVectors: { correct: { symbols: counts }, wrong: [{ response: { symbols: counts.slice(0, 2) }, expectCode: 'count' }, { response: { symbols: swap }, expectCode: 'swapped' }, { response: { symbols: off }, expectCode: 'off-by-one' }] } };
  else plot = { tool: 'bar-graph', title, orientation: 'vertical', categories: cats, categoryLabel: 'Choice', valueAxis: { min: 0, max: 12, step: 1, labelEvery: 1, snap: 1, label: 'Number' }, source, target: { values: counts },
    feedback: { count: 'Every bar needs a height on the scale.', swapped: 'Two bars are switched. Check which bar goes with each label.', 'off-by-one': 'One bar is one space too high or too low. Read the scale again.', position: 'Not quite. Use the tally chart to set each bar again.' },
    testVectors: { correct: { values: counts }, wrong: [{ response: { values: counts.slice(0, 2) }, expectCode: 'count' }, { response: { values: swap }, expectCode: 'swapped' }, { response: { values: off }, expectCode: 'off-by-one' }] } };
  const list = cats.map((c, j) => `${c}: ${counts[j]}`).join('; ');
  plot.check = { type: 'exact-after-snap' };
  plot.answerKey = { src: `question-banks/assets/plot-keys/${id}.png`, alt: `${skill === 2 ? 'Picture graph' : 'Bar graph'} titled ${title}. ${list}.` };
  assert(P.valid(plot), id + ' valid');
  assert.equal(P.check(plot, plot.testVectors.correct).ok, true, id + ' correct');
  for (const w of plot.testVectors.wrong) { const r = P.check(plot, w.response); assert.equal(r.ok, false, id); assert.equal(r.code, w.expectCode, id + ' ' + r.code); }
  out.push({ id, unit: 'data', skillId: `data-skill-0${skill}`, level: lv, format: 'plot',
    prompt: skill === 2 ? 'Use the tally chart. Make a picture graph. Put one circle for each mark.' : 'Use the tally chart. Make a bar graph.', answer: list,
    solutionSteps: ['Count the tally marks in each row. A bundle of 5 has a line across it.', `Counts: ${list}.`, skill === 2 ? 'Draw one circle for each mark in each row.' : 'Make each bar end at its number on the scale.'],
    sourceNotes: `Original Claude-authored item (family: dt${skill}_plot_${skill === 2 ? 'picture' : 'bar'}_graph). 1st Grade Math audit 2026-11-19 (#15, Graphing Practice); target and feedback vectors checked against core/plot.js by tools/grade1-audit-20261119/plots.cjs.`, plot });
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
