// 8th Grade Math audit #9 (2026-11-19): Graphing Practice beyond lines and systems.
// 39 plot items: construct scatter plots (Patterns and Bivariate Data skill 1, points tool), plot the image of a triangle
// after a rotation, reflection, translation or dilation (Congruence and Similarity skills 2-5, points tool) and graph
// proportional relationships (Linear and Functional Relationships skill 12, line tool). Every target and feedback vector is
// checked against the site's grader (core/plot.js); answer keys are drawn with the site's renderer.
// Usage: NODE_PATH=/opt/npm-tools/node_modules node tools/grade8-audit-20261119/plots.cjs [--no-render]
'use strict';
const fs = require('node:fs'), path = require('node:path'), vm = require('node:vm'), assert = require('node:assert/strict');
const ROOT = path.resolve(__dirname, '../..');
const ctx = {}; vm.createContext(ctx);
vm.runInContext(fs.readFileSync(path.join(ROOT, 'worksheet-generator/core/plot.js'), 'utf8'), ctx);
const P = ctx.MK_PLOT;
const NOTE = (fam) => `Original Claude-authored item (family: ${fam}). 8th Grade Math audit 2026-11-19 (#9, Graphing Practice); target and feedback vectors checked against core/plot.js by tools/grade8-audit-20261119/plots.cjs.`;
const LEVELS = ['cp2', 'cp1', 'honors'];
const Q1 = { xmin: 0, xmax: 12, ymin: 0, ymax: 12, step: 1, snap: 1 };
const ALL = { xmin: -8, xmax: 8, ymin: -8, ymax: 8, step: 1, snap: 1 };
const pt = (p) => `(${p[0]}, ${p[1]})`;
const list = (ps) => ps.map(pt).join(', ');
const items = [];

/* ---------- scatter plots (8.SP.A.1) ---------- */
const SCATTER = [
  // [level, x name, y name, xs, ys, honors prose names]
  ['cp2', 'minutes practiced', 'free throws made', [1, 3, 5, 7, 9], [2, 4, 5, 8, 9]],
  ['cp2', 'hours of sleep', 'quiz score (out of 12)', [5, 6, 7, 8, 9], [6, 7, 9, 10, 11]],
  ['cp2', 'temperature (tens of °F)', 'cups of cocoa sold', [3, 4, 5, 6, 8], [11, 9, 8, 5, 2]],
  ['cp2', 'age of a phone (years)', 'value (tens of dollars)', [0, 1, 2, 4, 5], [12, 10, 8, 4, 3]],
  ['cp1', 'hours studied', 'points gained', [0, 2, 3, 5, 6, 8], [1, 3, 4, 7, 7, 10]],
  ['cp1', 'number of workers', 'hours to finish', [1, 2, 3, 4, 6, 8], [12, 10, 7, 6, 4, 3]],
  ['cp1', 'shoe size', 'spelling score', [4, 6, 7, 9, 10, 12], [9, 2, 11, 5, 8, 3]],
  ['cp1', 'laps run', 'minutes of rest needed', [2, 3, 5, 6, 9, 11], [1, 2, 3, 5, 6, 8]],
  ['honors', 'hours of practice', 'goals scored', [9, 2, 6, 11, 4, 7, 1], [10, 3, 6, 12, 5, 8, 1], ['Ana', 'Ben', 'Cy', 'Dee', 'Eli', 'Fay', 'Gus']],
  ['honors', 'days since planting', 'height (cm)', [10, 4, 8, 2, 6, 12, 0], [9, 4, 7, 2, 5, 10, 1], ['Plant A', 'Plant B', 'Plant C', 'Plant D', 'Plant E', 'Plant F', 'Plant G']],
  ['honors', 'price (dollars)', 'number sold (tens)', [3, 8, 5, 10, 1, 6, 12], [10, 5, 8, 3, 12, 7, 1], ['Item 1', 'Item 2', 'Item 3', 'Item 4', 'Item 5', 'Item 6', 'Item 7']],
  ['honors', 'outside temperature (tens of °F)', 'heating cost (tens of dollars)', [9, 2, 5, 7, 3, 8, 4], [1, 11, 6, 3, 10, 2, 8], ['Week 1', 'Week 2', 'Week 3', 'Week 4', 'Week 5', 'Week 6', 'Week 7']],
];
for (const [lv, xn, yn, xs, ys, names] of SCATTER) {
  const pts = xs.map((x, i) => [x, ys[i]]);
  const assoc = (() => { const n = xs.length, mx = xs.reduce((a, b) => a + b) / n, my = ys.reduce((a, b) => a + b) / n; let sxy = 0, sxx = 0, syy = 0; xs.forEach((x, i) => { sxy += (x - mx) * (ys[i] - my); sxx += (x - mx) ** 2; syy += (ys[i] - my) ** 2; }); const r = sxy / Math.sqrt(sxx * syy); return r > 0.6 ? 'positive' : r < -0.6 ? 'negative' : 'no clear'; })();
  const prompt = names
    ? `Each pair is (${xn}, ${yn}): ${names.map((n, i) => `${n} ${xs[i]} and ${ys[i]}`).join('; ')}. Plot a scatter plot with ${xn} on the x-axis.`
    : `Data: ${xn}: ${xs.join(', ')}; ${yn}: ${ys.join(', ')}. Plot the scatter plot with ${xn} on the x-axis and ${yn} on the y-axis.`;
  const bySize = xs.map((x, i) => [x, [...ys].sort((a, b) => a - b)[i]]);
  const wrong = [];
  if (JSON.stringify(pts.map(([x, y]) => [y, x]).sort()) !== JSON.stringify([...pts].sort())) wrong.push({ response: { points: pts.map(([x, y]) => [y, x]) }, expectCode: 'swapped-coordinates' });
  if (JSON.stringify(bySize.sort()) !== JSON.stringify([...pts].sort())) wrong.push({ response: { points: bySize }, expectCode: 'position' });
  items.push({ unit: 'patterns-bivariate-data', skill: '01', lv, fam: 'plot_scatter', prompt, answer: list(pts),
    steps: [`Pair the values in order: ${names ? 'each name gives one point' : 'the first value of each list makes one point'}.`, `Points: ${list(pts)}.`,
      `The plot shows ${assoc === 'no clear' ? 'no clear association' : `a ${assoc} association`} between ${xn} and ${yn}.`],
    plot: { tool: 'points', grid: Q1, target: { points: pts },
      feedback: { position: 'Not quite. Pair the values in order: the first x-value goes with the first y-value.', 'swapped-coordinates': `You swapped the axes. Put ${xn} across (x) and ${yn} up (y).` },
      testVectors: { correct: { points: pts }, wrong } },
    alt: `First-quadrant grid with the points ${list(pts)} plotted.` });
}

/* ---------- transformations (8.G.A.1, 8.G.A.3) ---------- */
const rot = { 90: ([x, y]) => [-y, x], 180: ([x, y]) => [-x, -y], 270: ([x, y]) => [y, -x] };
const T = [
  // [skill, level, triangle, kind, arg, words, rule text, wrong rule]
  ['02', 'cp2', [[1, 2], [4, 2], [4, 6]], (p) => rot[180](p), 'a rotation 180° about the origin', '(x, y) → (-x, -y)', (p) => [-p[0], p[1]]],
  ['02', 'cp2', [[-3, 1], [-1, 4], [2, 1]], (p) => rot[180](p), 'a rotation 180° about the origin', '(x, y) → (-x, -y)', (p) => [p[0], -p[1]]],
  ['02', 'cp1', [[1, 1], [5, 2], [3, 6]], (p) => rot[90](p), 'a rotation 90° counterclockwise about the origin', '(x, y) → (-y, x)', (p) => rot[270](p)],
  ['02', 'cp1', [[-2, 3], [2, 5], [1, 1]], (p) => rot[90](p), 'a rotation 90° counterclockwise about the origin', '(x, y) → (-y, x)', (p) => rot[270](p)],
  ['02', 'honors', [[2, -1], [6, 1], [3, 4]], (p) => rot[270](p), 'a rotation 90° clockwise about the origin', '(x, y) → (y, -x)', (p) => rot[90](p)],
  ['02', 'honors', [[-4, -2], [-1, -5], [1, -1]], (p) => rot[270](p), 'a rotation 270° counterclockwise about the origin', '(x, y) → (y, -x)', (p) => rot[90](p)],
  ['03', 'cp2', [[1, 2], [5, 3], [2, 6]], (p) => [p[0], -p[1]], 'a reflection over the x-axis', '(x, y) → (x, -y)', (p) => [-p[0], p[1]]],
  ['03', 'cp2', [[-5, 1], [-2, 2], [-4, 5]], (p) => [-p[0], p[1]], 'a reflection over the y-axis', '(x, y) → (-x, y)', (p) => [p[0], -p[1]]],
  ['03', 'cp1', [[2, -1], [6, -3], [3, -6]], (p) => [-p[0], p[1]], 'a reflection over the y-axis', '(x, y) → (-x, y)', (p) => [p[0], -p[1]]],
  ['03', 'cp1', [[-3, -2], [1, -5], [2, -1]], (p) => [p[0], -p[1]], 'a reflection over the x-axis', '(x, y) → (x, -y)', (p) => [-p[0], p[1]]],
  ['03', 'honors', [[1, 4], [2, 7], [5, 6]], (p) => [p[1], p[0]], 'a reflection over the line y = x', '(x, y) → (y, x)', (p) => [-p[1], -p[0]]],
  ['03', 'honors', [[-1, 3], [-4, 5], [-3, 1]], (p) => [-p[1], -p[0]], 'a reflection over the line y = -x', '(x, y) → (-y, -x)', (p) => [p[1], p[0]]],
  ['04', 'cp2', [[1, 1], [4, 1], [2, 4]], (p) => [p[0] + 3, p[1] + 2], 'a translation 3 units right and 2 units up', '(x, y) → (x + 3, y + 2)', (p) => [p[0] + 2, p[1] + 3]],
  ['04', 'cp2', [[-2, 3], [1, 5], [0, 1]], (p) => [p[0] - 4, p[1] - 3], 'a translation 4 units left and 3 units down', '(x, y) → (x - 4, y - 3)', (p) => [p[0] + 4, p[1] + 3]],
  ['04', 'cp1', [[-3, -2], [0, -1], [-1, 2]], (p) => [p[0] + 5, p[1] - 4], 'the translation (x, y) → (x + 5, y - 4)', '(x, y) → (x + 5, y - 4)', (p) => [p[0] - 4, p[1] + 5]],
  ['04', 'cp1', [[2, -3], [5, -1], [3, 1]], (p) => [p[0] - 6, p[1] + 2], 'the translation (x, y) → (x - 6, y + 2)', '(x, y) → (x - 6, y + 2)', (p) => [p[0] + 2, p[1] - 6]],
  ['04', 'honors', [[-4, 1], [-1, 3], [-2, -2]], (p) => [p[0] + 5, p[1] - 1], 'a translation 2 units right and 3 units down, followed by a translation 3 units right and 2 units up', '(x, y) → (x + 5, y - 1)', (p) => [p[0] + 2, p[1] - 3]],
  ['04', 'honors', [[1, 2], [4, 4], [3, -1]], (p) => [p[0] - 6, p[1] + 1], 'a translation 1 unit left and 4 units up, followed by a translation 5 units left and 3 units down', '(x, y) → (x - 6, y + 1)', (p) => [p[0] - 1, p[1] + 4]],
  ['05', 'cp2', [[1, 1], [3, 1], [1, 3]], (p) => [2 * p[0], 2 * p[1]], 'a dilation with scale factor 2 centered at the origin', '(x, y) → (2x, 2y)', (p) => [p[0] + 2, p[1] + 2]],
  ['05', 'cp1', [[2, -4], [6, 2], [-4, 6]], (p) => [p[0] / 2, p[1] / 2], 'a dilation with scale factor 1/2 centered at the origin', '(x, y) → ((1/2)x, (1/2)y)', (p) => [2 * p[0], 2 * p[1]]],
  ['05', 'honors', [[-2, 2], [2, 4], [4, -2]], (p) => [1.5 * p[0], 1.5 * p[1]], 'a dilation with scale factor 3/2 centered at the origin', '(x, y) → ((3/2)x, (3/2)y)', (p) => [p[0] + 1.5, p[1] + 1.5]],
];
const L3 = ['A', 'B', 'C'];
for (const [sk, lv, tri, f, words, rule, bad] of T) {
  const img = tri.map(f), wrongImg = tri.map(bad);
  assert(img.every((p) => p.every((v) => Number.isInteger(v) && Math.abs(v) <= 8)), words);
  const named = tri.map((p, i) => `${L3[i]}${pt(p)}`).join(', ');
  const code = (r) => P.check({ tool: 'points', grid: ALL, target: { points: img } }, { points: r }).code;
  const wrong = [{ response: { points: tri }, expectCode: code(tri) }];
  if (wrongImg.every((p) => p.every((v) => Number.isInteger(v) && Math.abs(v) <= 8))) wrong.push({ response: { points: wrongImg }, expectCode: code(wrongImg) });
  items.push({ unit: 'congruence-similarity', skill: sk, lv, fam: 'plot_transform', prompt: `Triangle ABC has vertices ${named}. Plot the vertices of its image A′B′C′ after ${words}.`,
    answer: img.map((p, i) => `${L3[i]}′${pt(p)}`).join(', '),
    steps: [`Rule: ${rule}.`, ...tri.map((p, i) => `${L3[i]}${pt(p)} → ${L3[i]}′${pt(img[i])}.`)],
    plot: { tool: 'points', grid: ALL, target: { points: img },
      feedback: { position: `Not quite. Apply ${rule} to each vertex.`, 'swapped-coordinates': 'Check the order of the coordinates: plot (x, y) with x across and y up.' },
      testVectors: { correct: { points: img }, wrong } },
    alt: `Coordinate grid with the image vertices ${img.map((p, i) => `${L3[i]}′${pt(p)}`).join(', ')} plotted.` });
}

/* ---------- proportional relationships (8.EE.B.5) ---------- */
const PROP = [
  ['cp2', 'Graph the proportional relationship y = 3x.', '3', [[0, 0], [2, 6]], 'The line passes through (0, 0) with slope 3: from the origin go up 3, right 1.'],
  ['cp2', 'A store sells pencils for $2 each. Graph the cost y (dollars) of x pencils.', '2', [[0, 0], [5, 10]], 'Cost = 2 × number of pencils, so y = 2x: a line through (0, 0) with slope 2.'],
  ['cp1', 'A printer prints 5 pages every 2 minutes. Graph the pages y printed in x minutes.', '5/2', [[0, 0], [4, 10]], 'The unit rate is 5 ÷ 2 = 2.5 pages per minute, so y = (5/2)x.'],
  ['cp1', 'A proportional relationship has a unit rate of 3/4. Graph it.', '3/4', [[0, 0], [8, 6]], 'y = (3/4)x: from (0, 0) go up 3, right 4.'],
  ['honors', 'The graph of a proportional relationship passes through (4, 6). Graph it.', '3/2', [[0, 0], [4, 6]], 'Proportional means the line passes through (0, 0); the unit rate is 6 ÷ 4 = 3/2.'],
  ['honors', 'Runner A runs y = 3x meters in x seconds. Runner B runs 1 meter per second faster. Graph Runner B.', '4', [[0, 0], [3, 12]], 'Runner B: 3 + 1 = 4 meters per second, so y = 4x.'],
];
for (const [lv, prompt, m, pts, step] of PROP) {
  const mm = m.includes('/') ? m.split('/').map(Number) : [Number(m), 1];
  const wrong = [{ response: { points: [[0, 1], [pts[1][0], pts[1][1] + 1]] }, expectCode: 'intercept' }];
  if (mm[0] !== mm[1] && pts[1][1] <= 12) wrong.push({ response: { points: [[0, 0], [pts[1][1], pts[1][0]]] }, expectCode: 'slope-reciprocal' });
  items.push({ unit: 'linear-functional-relationships', skill: '12', lv, fam: 'plot_proportional', prompt: prompt + ' Drag two points on the line.', answer: `y = ${m.includes('/') ? '(' + m + ')' : m}x, through ${list(pts)}`,
    steps: [step, `Plot ${pt(pts[0])} and ${pt(pts[1])}.`, `The graph is the line y = ${m.includes('/') ? '(' + m + ')' : m}x through the origin.`],
    plot: { tool: 'line', grid: Q1, target: { m, b: '0' },
      feedback: { 'same-point': 'Place two different points.', intercept: 'Your slope is right, but a proportional relationship passes through (0, 0).', 'slope-sign': 'Your line slants the wrong way.',
        'slope-reciprocal': 'You used x ÷ y. The unit rate is y ÷ x (rise over run).', slope: 'Start at (0, 0), then use the unit rate as rise over run.' },
      testVectors: { correct: { points: pts }, wrong } },
    alt: `First-quadrant grid with the line y = ${m}x through ${list(pts)}.` });
}

function main() {
  const render = !process.argv.includes('--no-render');
  const banks = {}, keys = [], count = {};
  for (const it of items) {
    const file = path.join(ROOT, 'question-banks/prealgebra', it.unit + '.json');
    if (!banks[it.unit]) { const raw = fs.readFileSync(file, 'utf8'); banks[it.unit] = { file, raw, bank: JSON.parse(raw) }; }
    const B = banks[it.unit].bank, abbr = { 'patterns-bivariate-data': 'biv', 'congruence-similarity': 'cgs', 'linear-functional-relationships': 'lfr' }[it.unit];
    const k = abbr + it.skill + it.lv; count[k] = (count[k] || 0) + 1;
    const id = `pa8-${abbr}-s${it.skill}-${it.lv}-p${String(count[k]).padStart(3, '0')}`;
    const skillId = `${it.unit}-skill-${it.skill}`;
    const plot = { ...it.plot, answerKey: { src: `question-banks/assets/plot-keys/${id}.png`, alt: it.alt }, check: { type: 'exact-after-snap' } };
    assert(P.valid(plot), id + ' valid');
    assert.equal(P.check(plot, plot.testVectors.correct).ok, true, id + ' correct');
    for (const w of plot.testVectors.wrong) { const r = P.check(plot, w.response); assert.equal(r.ok, false, id); assert.equal(r.code, w.expectCode, id + ' ' + JSON.stringify(w)); assert(plot.feedback[r.code], id + ' feedback for ' + r.code); }
    const std = B.questions.find((q) => q.skillId === skillId).standards;
    const q = { id, skillId, level: it.lv, format: 'plot', prompt: it.prompt, answer: it.answer, solutionSteps: it.steps, standards: std, sourceNotes: NOTE(it.fam), plot };
    const at = B.questions.findIndex((x) => x.id === id);
    if (at >= 0) B.questions[at] = q;
    else { const idx = B.questions.map((x, i) => [x, i]).filter(([x]) => x.skillId === skillId && x.level === it.lv).pop()[1]; B.questions.splice(idx + 1, 0, q); }
    keys.push({ id, svg: P.blank(plot, plot.testVectors.correct).replace(/<text[^>]*>[A-Z]<\/text>/g, '') });
  }
  for (const { file, raw, bank } of Object.values(banks)) fs.writeFileSync(file, JSON.stringify(bank, null, 1) + (raw.endsWith('\n') ? '\n' : ''));
  console.log('plot items', items.length);
  if (render) return renderKeys(keys);
}
async function renderKeys(keys) {
  const { chromium } = require(process.env.PLAYWRIGHT || 'playwright');
  const browser = await chromium.launch(process.env.CHROME ? { executablePath: process.env.CHROME } : {});
  const page = await browser.newPage({ deviceScaleFactor: 1 });
  for (const k of keys) {
    await page.setContent(`<!doctype html><html><body style="margin:0;background:white;font-family:Inter,Arial,sans-serif"><div id="k" style="display:inline-block;width:480px">${k.svg}</div></body></html>`);
    await page.locator('#k').screenshot({ path: path.join(ROOT, 'question-banks/assets/plot-keys', k.id + '.png') });
  }
  await browser.close();
  console.log('rendered', keys.length, 'answer keys');
}
Promise.resolve(main()).catch((e) => { console.error(e); process.exit(1); });
