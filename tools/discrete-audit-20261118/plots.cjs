// Discrete Math audit #18 (2026-11-18): Graphing Practice for Linear Programming.
// 24 plot items (8 per level): graph one constraint (skill 02, region tool), plot every corner point of a feasible region
// (skill 03, points tool) and graph two boundary lines and mark the corner where they meet (skill 05, system tool).
// Grid: the first quadrant, 0 to 12. Every target is checked against the site's grader (core/plot.js); answer keys are
// drawn with the site's renderer. Usage: node tools/discrete-audit-20261118/plots.cjs [--no-render]
'use strict';
const fs = require('node:fs'), path = require('node:path'), vm = require('node:vm'), assert = require('node:assert/strict');
const ROOT = path.resolve(__dirname, '../..');
const ctx = {}; vm.createContext(ctx);
vm.runInContext(fs.readFileSync(path.join(ROOT, 'worksheet-generator/core/plot.js'), 'utf8'), ctx);
const P = ctx.MK_PLOT;
const NOTE = fam => `Original Claude-authored Discrete Math item (family: ${fam}). Target and feedback vectors checked against core/plot.js by tools/discrete-audit-20261118/plots.cjs (Discrete Math audit #18, 2026-11-18).`;
const LEVELS = ['cp2', 'cp1', 'honors'];
const GRID = { xmin: 0, xmax: 12, ymin: 0, ymax: 12, step: 1, snap: 1 };
let seed = 1811;
const rnd = () => { seed = (seed * 1103515245 + 12345) % 2147483648; return seed / 2147483648; };
const ri = (a, b) => a + Math.floor(rnd() * (b - a + 1));
const pick = a => a[Math.floor(rnd() * a.length)];
const minus = s => String(s).replace(/^-/, '−');
// constraint ax + by (op) c with a, b ≥ 0 written in standard form; boundary y = (c − ax)/b
const term = (k, v, first) => k === 0 ? '' : (first ? '' : ' + ') + (k === 1 ? v : k + v);
const std = (a, b, op, c) => `${term(a, 'x', true)}${term(b, 'y', a === 0)} ${op} ${c}`;
const lattice = (a, b, c) => { const pts = []; for (let x = 0; x <= 12; x++) { const y = (c - a * x) / b; if (Number.isInteger(y) && y >= 0 && y <= 12) pts.push([x, y]); } return pts; };
const slopeText = (a, b) => { const g = (x, y) => y ? g(y, x % y) : x, k = g(a, b); return (a ? '−' : '') + (b / k === 1 ? (a / k === 1 ? '' : a / k) : `${a / k}/${b / k}`); };
const fam = {};

fam.region = L => {
  for (;;) {
    const a = pick(L === 0 ? [1, 2] : [1, 2, 3, 1, 2]), b = pick(L === 0 ? [1] : [1, 2, 3]), c = ri(6, 12) * (L === 2 ? 1 : 1);
    const op = pick(L === 0 ? ['≤', '≤', '≥'] : ['≤', '≥', '<', '>']);
    const pts = lattice(a, b, c); if (pts.length < 2 || c % b) continue;
    const dashed = op === '<' || op === '>', shade = op === '>' || op === '≥' ? 'above' : 'below';
    const g = (x, y) => y ? g(y, x % y) : x, kk = g(a, b), m = a === 0 ? '0' : `-${a / kk}${b / kk === 1 ? '' : '/' + b / kk}`;
    const target = { m, b: String(c / b), op };
    const correct = { points: [pts[0], pts[pts.length - 1]], dashed, shade };
    const wrong = [{ response: { ...correct, dashed: !dashed }, expectCode: 'dashed-solid' }, { response: { ...correct, shade: shade === 'above' ? 'below' : 'above' }, expectCode: 'shade-side' }];
    const holds = { '≤': 0 <= c, '≥': 0 >= c, '<': 0 < c, '>': 0 > c }[op];
    return { skill: 2, prompt: L === 2 ? `A workshop makes x tables and y chairs. Each table takes ${a} hour${a > 1 ? 's' : ''} and each chair ${b} hour${b > 1 ? 's' : ''}, and the time used must be ${({ '≤': 'at most', '<': 'less than', '≥': 'at least', '>': 'more than' })[op]} ${c} hours. Write the constraint and graph it in the first quadrant.` : `Graph the constraint ${std(a, b, op, c)} in the first quadrant (x ≥ 0, y ≥ 0).`,
      answer: `${dashed ? 'Dashed' : 'Solid'} boundary ${std(a, b, '=', c)} through (0, ${c / b}) and (${Number.isInteger(c / a) ? c / a : c + '/' + a}, 0), shaded ${shade === 'below' ? 'toward' : 'away from'} the origin`,
      steps: [`Find the intercepts of ${std(a, b, '=', c)}: x = 0 gives y = ${c / b}; y = 0 gives x = ${Number.isInteger(c / a) ? c / a : c + '/' + a}.`, `In slope-intercept form the boundary is y = ${slopeText(a, b)}x + ${c / b}.`,
        `Use a ${dashed ? 'dashed' : 'solid'} line because the symbol is ${op}.`, `Test (0, 0): 0 ${op} ${c} is ${holds ? 'true' : 'false'}, so shade the side ${holds ? 'containing' : 'away from'} the origin (${shade} the line).`],
      plot: { tool: 'region', grid: GRID, target, feedback: { 'boundary-line': 'Your boundary line is not the line in the constraint. Find where it crosses each axis and draw through those points.', 'dashed-solid': 'Use a dashed line for < or > and a solid line for ≤ or ≥.', 'shade-side': 'Shade the other side. Test (0, 0) in the constraint.' }, testVectors: { correct, wrong } },
      alt: `First-quadrant grid with a ${dashed ? 'dashed' : 'solid'} boundary ${std(a, b, '=', c)} and the region ${shade} it shaded.`, stds: ['A-REI.D.12', 'DM.LP.2'], fam: 'lp_plot_region' };
  }
};

function corners(cons) { // cons: [a, b, c] meaning ax + by ≤ c; plus x, y ≥ 0
  const all = cons.concat([[-1, 0, 0], [0, -1, 0]]), out = new Map();
  for (let i = 0; i < all.length; i++) for (let j = i + 1; j < all.length; j++) {
    const [a1, b1, c1] = all[i], [a2, b2, c2] = all[j], d = a1 * b2 - a2 * b1; if (!d) continue;
    const x = (c1 * b2 - c2 * b1) / d, y = (a1 * c2 - a2 * c1) / d;
    if (x >= -1e-9 && y >= -1e-9 && cons.every(([a, b, c]) => a * x + b * y <= c + 1e-9)) out.set(x + ',' + y, [x, y]);
  }
  return [...out.values()].sort((p, q) => p[0] - q[0] || p[1] - q[1]);
}
const cText = ([a, b, c]) => a === 1 && b === 0 ? `x ≤ ${c}` : a === 0 && b === 1 ? `y ≤ ${c}` : std(a, b, '≤', c);

fam.corners = L => {
  for (;;) {
    const n = L === 0 ? 2 : 2 + (rnd() < 0.5 ? 1 : 0);
    const pool = [[1, 1, ri(6, 11)], [2, 1, ri(8, 16)], [1, 2, ri(8, 16)], [1, 0, ri(3, 8)], [0, 1, ri(3, 8)], [3, 1, ri(12, 18)], [1, 3, ri(12, 18)]];
    const cons = []; while (cons.length < n) { const c = pick(pool); if (!cons.some(k => k[0] === c[0] && k[1] === c[1])) cons.push(c); }
    const pts = corners(cons);
    if (pts.length < 4 || pts.some(p => !Number.isInteger(p[0]) || !Number.isInteger(p[1]) || p[0] > 12 || p[1] > 12)) continue;
    if (cons.some(k => !pts.some(p => Math.abs(k[0] * p[0] + k[1] * p[1] - k[2]) < 1e-9 && (p[0] || p[1])))) continue; // no redundant constraint
    const target = { points: pts };
    const sw = pts.map(([x, y]) => [y, x]);
    const wrong = [{ response: { points: pts.slice(0, -1).concat([[pts[pts.length - 1][0], pts[pts.length - 1][1] === 0 ? 1 : pts[pts.length - 1][1] - 1]]) }, expectCode: 'position' }];
    if (JSON.stringify([...sw].sort()) !== JSON.stringify([...pts].sort())) wrong.push({ response: { points: sw }, expectCode: 'swapped-coordinates' });
    const list = cons.map(cText).join('; ');
    return { skill: 3, prompt: L === 2 ? `The feasible region is ${list}; x ≥ 0; y ≥ 0. Find each corner by solving the boundary equations two at a time, discard any intersection that breaks a constraint, and plot every corner point.` : `Plot every corner point of the feasible region ${list}; x ≥ 0; y ≥ 0.`, answer: pts.map(p => `(${p[0]}, ${p[1]})`).join(', '),
      steps: ['Corners are where two boundary lines meet and every constraint still holds.', ...cons.map(k => `${cText(k).replace('≤', '=')}: crosses the axes at ` + (k[0] && k[1] ? `(0, ${k[2] / k[1]}) and (${k[2] / k[0]}, 0)` : k[0] ? `x = ${k[2]}` : `y = ${k[2]}`) + '.'),
        'Keep only intersections that satisfy every constraint (an axis crossing beyond another boundary is not a corner).', `Corners: ${pts.map(p => `(${p[0]}, ${p[1]})`).join(', ')}.`],
      plot: { tool: 'points', grid: GRID, target, feedback: { position: 'Not quite. Each corner is where two boundary lines meet; check that it satisfies every constraint.', 'swapped-coordinates': 'You swapped x and y. Plot (x, y) with x across and y up.' }, testVectors: { correct: { points: pts }, wrong } },
      alt: `First-quadrant grid with the corner points ${pts.map(p => `(${p[0]}, ${p[1]})`).join(', ')} plotted.`, stds: ['A-REI.D.12', 'DM.LP.3'], fam: 'lp_plot_corners' };
  }
};

fam.system = L => {
  for (;;) {
    const sx = ri(1, 7), sy = ri(1, 7);
    const forms = L === 0 ? [[1, 1], [2, 1], [1, 2]] : [[1, 1], [2, 1], [1, 2], [3, 1], [1, 3], [3, 2], [2, 3]];
    const [a1, b1] = pick(forms), [a2, b2] = pick(forms); if (a1 * b2 === a2 * b1) continue;
    const c1 = a1 * sx + b1 * sy, c2 = a2 * sx + b2 * sy;
    if (c1 % b1 || c2 % b2) continue;
    const p1 = lattice(a1, b1, c1), p2 = lattice(a2, b2, c2); if (p1.length < 2 || p2.length < 2 || c1 / b1 > 12 || c2 / b2 > 12) continue;
    const m = (a, b) => { const g = (x, y) => y ? g(y, x % y) : x, k = g(a, b); return `-${a / k}${b / k === 1 ? '' : '/' + b / k}`; };
    const target = { lines: [{ m: m(a1, b1), b: String(c1 / b1) }, { m: m(a2, b2), b: String(c2 / b2) }], solution: [sx, sy] };
    const correct = { lines: [[p1[0], p1[p1.length - 1]], [p2[0], p2[p2.length - 1]]], solution: [sx, sy] };
    const wrong = []; if (sx !== sy) wrong.push({ response: { ...correct, solution: [sy, sx] }, expectCode: 'solution' });
    const t1 = std(a1, b1, '=', c1), t2 = std(a2, b2, '=', c2);
    return { skill: 5, prompt: L === 2 ? `A plan uses ${a1} hour${a1 > 1 ? 's' : ''} of labor per x and ${b1} per y (${c1} hours available), and ${a2} units of material per x and ${b2} per y (${c2} units available). Graph the two boundary lines (labor first) and mark the corner where both resources are used up.` : `The constraints ${std(a1, b1, '≤', c1)} and ${std(a2, b2, '≤', c2)} have boundary lines ${t1} and ${t2}. Graph both lines, then mark the corner point where they meet.`, answer: `(${sx}, ${sy})`,
      steps: [`${t1} crosses the axes at (0, ${c1 / b1}) and (${Number.isInteger(c1 / a1) ? c1 / a1 : c1 + '/' + a1}, 0).`, `${t2} crosses the axes at (0, ${c2 / b2}) and (${Number.isInteger(c2 / a2) ? c2 / a2 : c2 + '/' + a2}, 0).`,
        `Solve the system: the lines meet at (${sx}, ${sy}).`, `Check: ${a1}·${sx} + ${b1}·${sy} = ${c1} and ${a2}·${sx} + ${b2}·${sy} = ${c2} ✓.`],
      plot: { tool: 'system', grid: GRID, target, feedback: { solution: 'Your lines are right. Check where they cross and enter that point.', 'line-intercept': 'Check where one of your lines crosses the y-axis.', 'line-slope-sign': 'One line slants the wrong way.', 'line-slope-reciprocal': 'One line uses run over rise.', 'line-slope': 'One of your lines has the wrong slope.', 'line-same-point': 'Place two different points on each line.' }, testVectors: { correct, wrong } },
      alt: `First-quadrant grid with the lines ${t1} and ${t2} meeting at (${sx}, ${sy}).`, stds: ['A-REI.C.6', 'DM.LP.5'], fam: 'lp_plot_system' };
  }
};

function main() {
  const render = !process.argv.includes('--no-render');
  const file = path.join(ROOT, 'question-banks/discrete/linear-programming.json'), raw = fs.readFileSync(file, 'utf8'), bank = JSON.parse(raw);
  if (bank.questions.some(q => q.format === 'plot')) { console.log('already has plot items'); return; }
  const used = new Set(bank.questions.map(q => q.prompt)), out = [], keys = [], mix = [fam.region, fam.corners, fam.system];
  for (const [L, lv] of LEVELS.entries()) {
    const n = {};
    for (let i = 0; i < 8; i++) {
      let it, tries = 0;
      do { it = mix[i % 3](L); tries++; } while (used.has(it.prompt) && tries < 500);
      assert(!used.has(it.prompt)); used.add(it.prompt);
      const sid = String(it.skill).padStart(2, '0'); n[sid] = (n[sid] || 0) + 1;
      const id = `dm-lp-s${sid}-${lv}-p${String(n[sid]).padStart(3, '0')}`;
      const plot = { ...it.plot, answerKey: { src: `question-banks/assets/plot-keys/${id}.png`, alt: it.alt }, check: { type: 'exact-after-snap' } };
      assert(P.valid(plot), id + ' valid');
      assert.equal(P.check(plot, plot.testVectors.correct).ok, true, id + ' correct');
      for (const w of plot.testVectors.wrong) { const r = P.check(plot, w.response); assert.equal(r.ok, false, id); assert.equal(r.code, w.expectCode, id + ' ' + JSON.stringify(w)); }
      const stds = it.stds.map(s => s === 'DM.LP.2' || s === 'DM.LP.3' || s === 'DM.LP.5' ? s : s);
      out.push({ id, skillId: `linear-programming-skill-${sid}`, level: lv, format: 'plot', prompt: it.prompt, answer: it.answer, solutionSteps: it.steps, standards: [stds[1], stds[0]], sourceNotes: NOTE(it.fam), plot });
      keys.push({ id, svg: P.blank(plot, plot.testVectors.correct).replace(/<text[^>]*>[A-Z]<\/text>/g, '') });
    }
  }
  bank.questions.push(...out);
  fs.writeFileSync(file, JSON.stringify(bank, null, 1) + (raw.endsWith('\n') ? '\n' : ''));
  console.log('linear-programming +', out.length, 'plot items');
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
Promise.resolve(main()).catch(e => { console.error(e); process.exit(1); });
