// Precalculus audit item #8: Graphing Practice items for four more units (adapted from tools/algebra2-plots-20261117).
// equations-inequalities (systems and inequalities), conics (parabolas and circles), sequences-series-limits
// (terms as points) and vectors (polar points and complex numbers in the complex plane).
// 8 plot items per level per unit (24 per unit). Every target is checked against the site's own
// grader (core/plot.js): the correct response passes and each wrong response gets its feedback code.
// Answer keys are drawn with the site's renderer (MK_PLOT.blank with the correct response) and saved as PNG.
// Usage: node tools/precalculus-audit-20261118/plots/build.cjs [--no-render]
'use strict';
const fs = require('node:fs'), path = require('node:path'), vm = require('node:vm'), assert = require('node:assert/strict');
const ROOT = path.resolve(__dirname, '../../..');
const ctx = {}; vm.createContext(ctx);
vm.runInContext(fs.readFileSync(path.join(ROOT, 'worksheet-generator/core/plot.js'), 'utf8'), ctx);
const P = ctx.MK_PLOT;
const NOTE = fam => `Original Claude-authored item (family: ${fam}). Target and feedback vectors checked against core/plot.js by tools/precalculus-audit-20261118/plots/build.cjs; answer recomputed from the printed problem by scripts/test-precalculus-plot-items.cjs. Teacher reviewed 2026-11-18.`;
const LEVELS = ['cp2', 'cp1', 'honors'];
const GRID = { xmin: -8, xmax: 8, ymin: -8, ymax: 8, step: 1, snap: 1 };

// ---------- small helpers
let seed = 20261118;
const rnd = () => { seed = (seed * 1103515245 + 12345) % 2147483648; return seed / 2147483648; };
const ri = (a, b) => a + Math.floor(rnd() * (b - a + 1));
const pick = a => a[Math.floor(rnd() * a.length)];
const gcd = (a, b) => b ? gcd(b, a % b) : Math.abs(a);
const frac = (n, d = 1) => { if (d < 0) { n = -n; d = -d; } const g = gcd(n, d) || 1; return [n / g, d / g]; };
const fs_ = ([n, d]) => d === 1 ? String(n) : `${n}/${d}`;
const minus = s => String(s).replace(/^-/, '−');
const coefText = ([n, d], v) => { if (n === 0) return ''; if (d === 1) return (n === 1 ? '' : n === -1 ? '−' : minus(n)) + v; return (n < 0 ? '−' : '') + `(${Math.abs(n)}/${d})` + v; };
const lineText = (m, b) => { const mx = coefText(m, 'x'); const bv = b; if (!mx) return minus(bv); return mx + (bv === 0 ? '' : bv > 0 ? ` + ${bv}` : ` − ${-bv}`); };
const yAt = (m, b, x) => m[0] * x / m[1] + b;
const inGrid = (x, y) => Number.isInteger(x) && Number.isInteger(y) && x >= -8 && x <= 8 && y >= -8 && y <= 8;
function gridPoints(m, b, avoid = []) {
  const pts = [];
  for (let x = -8; x <= 8; x++) { const y = yAt(m, b, x); if (inGrid(x, y) && !avoid.some(p => p[0] === x && p[1] === y)) pts.push([x, y]); }
  return pts;
}
const fam = {};

// ---------- linear systems (system tool)
fam.system = L => {
  for (;;) {
    const sx = ri(-5, 5), sy = ri(-5, 5);
    const slopes = L === 0 ? [[1, 1], [-1, 1], [2, 1], [-2, 1], [3, 1], [-3, 1]] : [[1, 1], [-1, 1], [2, 1], [-2, 1], [1, 2], [-1, 2], [3, 1], [2, 3], [-2, 3], [-3, 2], [3, 2]];
    const m1 = pick(slopes), m2 = pick(slopes);
    if (m1[0] * m2[1] === m2[0] * m1[1]) continue;
    const b1 = sy - m1[0] * sx / m1[1], b2 = sy - m2[0] * sx / m2[1];
    if (!Number.isInteger(b1) || !Number.isInteger(b2) || Math.abs(b1) > 8 || Math.abs(b2) > 8) continue;
    const p1 = gridPoints(m1, b1), p2 = gridPoints(m2, b2);
    if (p1.length < 2 || p2.length < 2) continue;
    let t1 = `y = ${lineText(m1, b1)}`, t2 = `y = ${lineText(m2, b2)}`;
    let std = null;
    if (L === 2 && m2[1] === 1) { // write the second line in standard form: (-m)x + y = b → multiply to clear
      const A = -m2[0], B = 1, C = b2, k = pick([1, 2, 3]);
      std = `${A * k === 1 ? '' : A * k === -1 ? '−' : minus(A * k)}x ${B * k > 0 ? '+' : '−'} ${Math.abs(B * k) === 1 ? '' : Math.abs(B * k)}y = ${minus(C * k)}`.replace(/^0x \+ /, '');
      if (A === 0) continue;
      t2 = std;
    }
    const target = { lines: [{ m: fs_(m1), b: String(b1) }, { m: fs_(m2), b: String(b2) }], solution: [sx, sy] };
    const correct = { lines: [[p1[0], p1[p1.length - 1]], [p2[0], p2[p2.length - 1]]], solution: [sx, sy] };
    const wrong = [];
    if (sx !== sy) wrong.push({ response: { ...correct, solution: [sy, sx] }, expectCode: 'solution' });
    const off = gridPoints([m1[0], m1[1]], b1 + 1);
    if (off.length >= 2) wrong.push({ response: { lines: [[off[0], off[off.length - 1]], correct.lines[1]], solution: [sx, sy] }, expectCode: 'line-intercept' });
    const prompt = `Solve the system by graphing: ${t1} and ${t2}. Graph both lines, then mark the intersection point.`;
    const steps = [`Line 1: slope ${minus(fs_(m1))}, y-intercept ${minus(b1)}.`,
      std ? `Line 2: solve ${std} for y: y = ${lineText(m2, b2)} (slope ${minus(fs_(m2))}, y-intercept ${minus(b2)}).` : `Line 2: slope ${minus(fs_(m2))}, y-intercept ${minus(b2)}.`,
      `The lines cross at (${sx}, ${sy}).`, `Check: ${minus(sy)} = ${minus(fs_(m1))}·(${minus(sx)}) ${b1 < 0 ? '− ' + -b1 : '+ ' + b1} and ${minus(sy)} = ${minus(fs_(m2))}·(${minus(sx)}) ${b2 < 0 ? '− ' + -b2 : '+ ' + b2} ✓.`];
    return { skill: 4, prompt, answer: `(${sx}, ${sy})`, steps, plot: { tool: 'system', grid: GRID, target, feedback: { solution: 'Your lines are right. Check where they cross and enter that point.', 'line-intercept': 'Check the y-intercept of one of your lines.', 'line-slope-sign': 'One line slants the wrong way.', 'line-slope-reciprocal': 'One line uses run over rise.', 'line-slope': 'One of your lines has the wrong slope.', 'line-same-point': 'Place two different points on each line.' }, testVectors: { correct, wrong } },
      alt: `Two lines ${t1} and ${t2} crossing at (${sx}, ${sy}).`, stds: ['A-REI.C.6', 'A-REI.D.11'], fam: 'pc-plot-system', check: { kind: 'system', t1, t2, solution: [sx, sy] } };
  }
};

// ---------- linear inequalities (region tool)
fam.region = L => {
  for (;;) {
    const slopes = L === 0 ? [[1, 1], [-1, 1], [2, 1], [-2, 1], [3, 1]] : [[1, 1], [-1, 1], [2, 1], [-2, 1], [1, 2], [-1, 2], [2, 3], [-3, 2], [3, 4]];
    const m = pick(slopes), b = ri(-5, 5), op = pick(['<', '>', '≤', '≥']);
    const pts = gridPoints(m, b);
    if (pts.length < 2) continue;
    let shown = `y ${op} ${lineText(m, b)}`, rewrite = null;
    if (L > 0 && m[1] === 1 && rnd() < 0.7) {
      // ax + by op c with b negative half the time (dividing by a negative flips the sign)
      const k = pick([1, 2, -1, -2]);
      const A = -m[0] * k, B = k, C = b * k;
      const flip = { '<': '>', '>': '<', '≤': '≥', '≥': '≤' };
      const op2 = k > 0 ? op : flip[op];
      const term = (c, v, first) => { if (c === 0) return ''; const s = Math.abs(c) === 1 ? v : Math.abs(c) + v; return first ? (c < 0 ? '−' + s : s) : (c < 0 ? ' − ' + s : ' + ' + s); };
      shown = `${term(A, 'x', true)}${term(B, 'y', A === 0)} ${op2} ${minus(C)}`;
      rewrite = `Solve for y: ${k < 0 ? 'dividing by a negative number reverses the inequality, so ' : ''}y ${op} ${lineText(m, b)}.`;
    }
    const dashed = op === '<' || op === '>', shade = op === '>' || op === '≥' ? 'above' : 'below';
    const target = { m: fs_(m), b: String(b), op };
    const correct = { points: [pts[0], pts[pts.length - 1]], dashed, shade };
    const wrong = [{ response: { ...correct, dashed: !dashed }, expectCode: 'dashed-solid' }, { response: { ...correct, shade: shade === 'above' ? 'below' : 'above' }, expectCode: 'shade-side' }];
    const test = 0 > yAt(m, b, 0) ? 'above' : 'below';
    const steps = [rewrite, `Graph the boundary y = ${lineText(m, b)} (slope ${minus(fs_(m))}, y-intercept ${minus(b)}).`, `Use a ${dashed ? 'dashed' : 'solid'} line because the symbol is ${op}.`,
      b === 0 ? `Test (0, 1): ${1} ${op} ${0} is ${({ '<': 1 < 0, '>': 1 > 0, '≤': 1 <= 0, '≥': 1 >= 0 })[op]}, so shade ${shade}.` : `Test (0, 0): 0 ${op} ${b} is ${({ '<': 0 < b, '>': 0 > b, '≤': 0 <= b, '≥': 0 >= b })[op] ? 'true' : 'false'}, so shade the side ${(({ '<': 0 < b, '>': 0 > b, '≤': 0 <= b, '≥': 0 >= b })[op]) ? 'containing' : 'not containing'} (0, 0): ${shade} the line.`].filter(Boolean);
    void test;
    return { skill: 6, prompt: `Graph ${shown}.`, answer: `${dashed ? 'Dashed' : 'Solid'} boundary line y = ${lineText(m, b)}, shaded ${shade}`, steps,
      plot: { tool: 'region', grid: GRID, target, feedback: { 'boundary-line': 'Your boundary line is not the line in the inequality. Solve for y and graph it like y = mx + b.', 'dashed-solid': 'Use a dashed line for < or > and a solid line for ≤ or ≥.', 'shade-side': 'Shade the other side. Test (0, 0) or another point in the inequality.' }, testVectors: { correct, wrong } },
      alt: `Coordinate grid with a ${dashed ? 'dashed' : 'solid'} line y = ${lineText(m, b)} and the region ${shade} it shaded.`, stds: ['A-REI.D.12', 'A-CED.A.3'], fam: 'pc-plot-region', check: { kind: 'region', shown } };
  }
};

// ---------- parabolas (conic-sections skill 02): (x − h)² = 4p(y − k)
fam.parabola = L => {
  for (;;) {
    const fp = L === 0 ? pick([1, 4, -4, 2]) : pick([1, 2, 4, -1, -2, -4]);
    const h = ri(-4, 4), k = ri(-4, 4);
    const sq = h === 0 ? 'x²' : `(x ${h > 0 ? '−' : '+'} ${Math.abs(h)})²`, rk = k === 0 ? 'y' : `(y ${k > 0 ? '−' : '+'} ${Math.abs(k)})`;
    const dx = 2, yb = k + dx * dx / fp;
    if (!inGrid(h + dx, yb)) continue;
    const a = frac(1, fp), pval = frac(fp, 4);
    let prompt;
    if (L === 2 && rnd() < 0.6) {
      const dir = fp > 0 ? 'above' : 'below';
      prompt = `Graph the parabola with vertex (${h}, ${k}) and focus (${h}, ${fs_(frac(4 * k + fp, 4))}). Drag the vertex first, then drag a second point on the parabola.`;
      void dir;
    } else prompt = `Graph ${sq} = ${fp === 1 ? '' : fp === -1 ? '−' : minus(fp)}${rk}. Drag the vertex first, then drag a second point on the parabola.`;
    const target = { a: fs_(a), h, k };
    const correct = { anchor: [h, k], point: [h + dx, yb] };
    const wrong = [];
    if (h !== 0) wrong.push({ response: { anchor: [-h, k], point: [-h + dx, yb] }, expectCode: 'h-sign' });
    if (k !== 0) wrong.push({ response: { anchor: [h, -k], point: [h + dx, -k + dx * dx / fp] }, expectCode: 'k-sign' });
    wrong.push({ response: { anchor: [h, k], point: [h + dx, k - dx * dx / fp] }, expectCode: 'a-sign' });
    const steps = [`Compare with (x − h)² = 4p(y − k): vertex (h, k) = (${h}, ${k}) and 4p = ${minus(fp)}, so p = ${minus(fs_(pval))}.`,
      `Solve for y: y = (1/(${minus(fp)}))(x − h)² + k, so y = ${coefText(a, '') || '1'}${a[0] < 0 && a[1] === 1 && a[0] === -1 ? '' : ''}·(x − h)² + k with a = ${minus(fs_(a))}; it opens ${fp > 0 ? 'up' : 'down'}.`,
      `Two units right of the vertex: y = ${k} + 2²/${minus(fp)} = ${yb}, so (${h + dx}, ${yb}) is on the parabola.`];
    if (prompt.includes('focus')) steps.unshift(`The focus is |p| = ${fs_(frac(Math.abs(fp), 4))} ${fp > 0 ? 'above' : 'below'} the vertex, so 4p = ${minus(fp)} and the equation is ${sq} = ${fp === 1 ? '' : fp === -1 ? '−' : minus(fp)}${rk}.`);
    steps[1 + (prompt.includes('focus') ? 1 : 0)] = `Solve for y: y = (1/${fp < 0 ? '(' + minus(fp) + ')' : fp})${h === 0 ? 'x²' : sq} ${k === 0 ? '' : (k > 0 ? '+ ' + k : '− ' + -k)}`.trim() + `, so a = ${minus(fs_(a))} and the parabola opens ${fp > 0 ? 'up' : 'down'}.`;
    return { skill: 2, prompt, answer: `vertex (${h}, ${k}); passes through (${h + dx}, ${yb}) and (${h - dx}, ${yb})`, steps,
      plot: { tool: 'parabola', grid: GRID, target, feedback: { anchor: 'Place the vertex first. In (x − h)² = 4p(y − k) the vertex is (h, k).', 'h-sign': 'Check the horizontal shift: (x − h) moves the graph h units to the RIGHT.', 'k-sign': 'Check the vertical shift: (y − k) moves the vertex k units up.', 'swapped-hk': 'You switched h and k. The vertex is (h, k).', 'same-x': 'Your second point must have a different x-value than the vertex.', 'a-sign': 'Your parabola opens the wrong way. When 4p is negative it opens down.', stretch: 'Check the width: y − k = (x − h)²/(4p).' }, testVectors: { correct, wrong } },
      alt: `Coordinate grid with the parabola ${prompt.match(/Graph (.*?)\. Drag|vertex .*? and focus .*?\)/)[0].replace(/^Graph /, '').replace(/\. Drag$/, '')}; vertex (${h}, ${k}) and the point (${h + dx}, ${yb}) marked.`, stds: ['G-GPE.A.2'], fam: 'pc-plot-parabola', check: { kind: 'parabola', h, k, fp, focus: prompt.includes('focus') } };
  }
};

// A wrong response for the points tool: every point one unit up (or down), never the swapped set.
function shifted(pts) {
  const key = a => a.map(p => p.join(',')).sort().join(' ');
  const swap = key(pts.map(([x, y]) => [y, x]));
  for (const dy of [1, -1, 2]) { const s = pts.map(([x, y]) => [x, y + dy]); if (key(s) !== swap && key(s) !== key(pts)) return s; }
  throw new Error('no shifted response');
}

// ---------- circles (conic-sections skill 01): center and the four "compass" points
fam.circle = L => {
  for (;;) {
    const h = ri(-4, 4), k = ri(-4, 4), r = L === 0 ? pick([2, 3, 4]) : pick([2, 3, 4, 5]);
    const pts = [[h, k], [h, k + r], [h, k - r], [h + r, k], [h - r, k]];
    if (!pts.every(([x, y]) => inGrid(x, y))) continue;
    const sx = h === 0 ? 'x²' : `(x ${h > 0 ? '−' : '+'} ${Math.abs(h)})²`, sy = k === 0 ? 'y²' : `(y ${k > 0 ? '−' : '+'} ${Math.abs(k)})²`;
    let eqn = `${sx} + ${sy} = ${r * r}`, pre = null;
    if (L === 2 && rnd() < 0.6) {
      const D = -2 * h, E = -2 * k, Fc = h * h + k * k - r * r;
      const t = (c, v) => c === 0 ? '' : (c < 0 ? ` − ${Math.abs(c) === 1 ? '' : Math.abs(c)}${v}` : ` + ${c === 1 ? '' : c}${v}`);
      eqn = `x² + y²${t(D, 'x')}${t(E, 'y')}${Fc === 0 ? '' : Fc < 0 ? ` − ${-Fc}` : ` + ${Fc}`} = 0`;
      pre = `Complete the square: ${sx} + ${sy} = ${r * r}.`;
    }
    const target = { points: pts };
    const correct = { points: pts };
    const wrong = [{ response: { points: pts.map(([x, y]) => [y, x]) }, expectCode: h === k ? 'swapped-coordinates' : 'swapped-coordinates' }];
    if (h === k) wrong.length = 0;
    const rr = r * r <= 8 ? null : Math.round(r * r / 2);
    const bad = [[-h, -k], [-h, -k + r], [-h, -k - r], [-h + r, -k], [-h - r, -k]];
    void bad;
    wrong.push({ response: { points: shifted(pts) }, expectCode: 'position' });
    void rr;
    const steps = [pre, `Center (h, k) = (${h}, ${k}); r² = ${r * r}, so r = ${r}.`, `Move ${r} up, down, right and left from the center: (${h}, ${k + r}), (${h}, ${k - r}), (${h + r}, ${k}), (${h - r}, ${k}).`].filter(Boolean);
    return { skill: 1, prompt: `For the circle ${eqn}, plot the center and the four points on the circle directly above, below, right and left of the center.`,
      answer: `center (${h}, ${k}); points (${h}, ${k + r}), (${h}, ${k - r}), (${h + r}, ${k}), (${h - r}, ${k})`, steps,
      plot: { tool: 'points', grid: GRID, target, feedback: { position: 'Not quite. The center is (h, k) — watch the signs — and each point is r units from it.', 'swapped-coordinates': 'You switched x and y. Move across the x-axis first, then up or down.', count: 'Plot five points: the center and four points on the circle.' }, testVectors: { correct, wrong } },
      alt: `Coordinate grid with the center (${h}, ${k}) of the circle ${eqn} and the points (${h}, ${k + r}), (${h}, ${k - r}), (${h + r}, ${k}), (${h - r}, ${k}).`, stds: ['G-GPE.A.1'], fam: 'pc-plot-circle', check: { kind: 'circle', eqn } };
  }
};

// ---------- sequences as points (n, aₙ)
const SUB = n => String(n).replace(/\d/g, d => '₀₁₂₃₄₅₆₇₈₉'[d]);
fam.arith = L => {
  for (;;) {
    const a1 = ri(-7, 7), d = pick([1, 2, 3, -1, -2, -3]);
    const terms = [1, 2, 3, 4].map(n => a1 + (n - 1) * d);
    if (!terms.every(t => Math.abs(t) <= 8)) continue;
    const c = a1 - d;
    let def = `aₙ = ${d === 1 ? '' : d === -1 ? '−' : minus(d)}n${c === 0 ? '' : c > 0 ? ` + ${c}` : ` − ${-c}`}`;
    if (L === 2 || (L === 1 && rnd() < 0.5)) def = `a₁ = ${minus(a1)}, aₙ = aₙ₋₁ ${d > 0 ? '+' : '−'} ${Math.abs(d)}`;
    return seqItem(1, def, terms, 'arithmetic', [`Each term ${d > 0 ? 'adds' : 'subtracts'} ${Math.abs(d)}: ${terms.join(', ')}.`]);
  }
};
fam.geom = L => {
  for (;;) {
    const [a1, r] = pick(L === 0 ? [[1, 2], [-1, 2], [8, 0.5], [2, 2], [-8, 0.5]] : [[1, 2], [-1, 2], [1, -2], [8, 0.5], [8, -0.5], [-1, -2], [2, -2], [-8, 0.5]]);
    const terms = [1, 2, 3, 4].map(n => a1 * r ** (n - 1));
    if (!terms.every(t => Number.isInteger(t) && Math.abs(t) <= 8)) continue;
    const rt = r === 0.5 ? '1/2' : r === -0.5 ? '−1/2' : minus(r);
    const lead = a1 === 1 ? '' : minus(a1), paren = r < 0 || String(rt).includes('/');
    let def = `aₙ = ${lead}${paren ? `(${rt})` : (lead ? '·' : '') + rt}ⁿ⁻¹`;
    if (L > 0 && rnd() < 0.5) def = `a₁ = ${minus(a1)}, aₙ = ${String(rt).includes('/') || r < 0 ? `(${rt})` : rt}·aₙ₋₁`;
    return seqItem(2, def, terms, 'geometric', [`Each term is multiplied by ${rt}: ${terms.join(', ')}.`]);
  }
};
function seqItem(skill, def, terms, kind, more) {
  const pts = terms.map((t, i) => [i + 1, t]);
  const wrong = [{ response: { points: pts.map(([x, y]) => [y, x]) }, expectCode: 'swapped-coordinates' }, { response: { points: shifted(pts) }, expectCode: 'position' }];
  if (terms.some((t, i) => t === i + 1) && terms.every((t, i) => t === i + 1)) wrong.shift();
  return { skill, prompt: `Graph the first four terms of the ${kind} sequence ${def} as points (n, aₙ).`, answer: pts.map(([n, t]) => `(${n}, ${t})`).join(', '),
    steps: [`a₁ = ${terms[0]}.`, ...more, `Plot (1, ${terms[0]}), (2, ${terms[1]}), (3, ${terms[2]}), (4, ${terms[3]}). The points ${kind === 'arithmetic' ? 'lie on a line' : 'do not lie on a line'}.`],
    plot: { tool: 'points', grid: GRID, target: { points: pts }, feedback: { position: 'Not quite. Plot each term as (n, aₙ): n = 1, 2, 3, 4 across, the term up or down.', 'swapped-coordinates': 'You switched the coordinates. n goes across (x) and the term aₙ goes up or down (y).', count: 'Plot exactly four points.' }, testVectors: { correct: { points: pts }, wrong } },
    alt: `Coordinate grid with the points ${pts.map(([n, t]) => `(${n}, ${t})`).join(', ')}.`, stds: ['F-BF.A.2', 'F-IF.A.3'], fam: `pc-plot-${kind}`, check: { kind, def, terms } };
}

// ---------- histograms of simulated results (skill 09) and of roughly normal data (skill 07)
fam.hist = (L, skill) => {
  for (;;) {
    const width = skill === 9 ? pick([1, 2]) : pick([5, 10]);
    const count = 5, start = skill === 9 ? (width === 1 ? ri(2, 4) : ri(0, 2) * 2) : pick([40, 50, 60, 140, 150]);
    const n = L === 0 ? 15 : 20;
    const weights = [1, 3, 5, 3, 1];
    const data = [];
    for (let i = 0; i < n; i++) {
      let u = rnd() * weights.reduce((a, b) => a + b), bin = 0;
      while (u > weights[bin]) { u -= weights[bin]; bin++; }
      data.push(start + bin * width + (width === 1 ? 0 : ri(0, width - 1)));
    }
    const counts = Array(count).fill(0); data.forEach(v => counts[Math.floor((v - start) / width)]++);
    if (Math.max(...counts) > 9 || counts[2] < 3) continue;
    if (width > 1 && !data.some(v => (v - start) % width === 0 && v > start)) continue; // at least one boundary value
    const label = skill === 9 ? pick([['Number of heads in 10 coin flips', 'Simulated Heads', 'heads'], ['Number of sixes in 30 die rolls', 'Simulated Sixes', 'sixes'], ['Number of red spins in 12 spins', 'Simulated Red Spins', 'red spins']])
      : pick([['Heights of a class of students (cm)', 'Student Heights', 'cm'], ['Scores on a 100-point test', 'Test Scores', 'points'], ['Weights of apples (g)', 'Apple Weights', 'g']]);
    if (skill === 7 && label[2] === 'cm' && start < 140) continue;
    if (skill === 7 && label[2] !== 'cm' && start >= 140) continue;
    const binsText = width === 1 ? `one bar for each value from ${start} to ${start + count - 1}` : `bins of width ${width} starting at ${start}. Each bin includes its left edge but not its right edge`;
    const intro = skill === 9 ? `A model was simulated ${n} times. ${label[0]} in each run: ${data.join(', ')}.` : `${label[0]}: ${data.join(', ')}.`;
    const names = counts.map((c, i) => width === 1 ? `${start + i}: ${c}` : `${start + i * width} to under ${start + (i + 1) * width}: ${c}`);
    const rc = Array(count).fill(0); data.forEach(v => { const j = Math.ceil((v - start) / width) - 1; if (j >= 0 && j < count) rc[j]++; else if (j < 0) rc[0]++; });
    const wrong = [{ response: { counts: counts.map((c, i) => i === 2 ? c + 1 : c) }, expectCode: 'total' }, { response: { counts: counts.slice(0, 4) }, expectCode: 'count' }];
    const shift = [[1, 2], [3, 2], [0, 2], [4, 2]].map(([up, down]) => counts.map((c, i) => i === up ? c + 1 : i === down ? c - 1 : c)).find(sh => sh.join() !== rc.join());
    wrong.push({ response: { counts: shift }, expectCode: 'position' });
    if (width > 1 && rc.join() !== counts.join() && rc.reduce((a, b) => a + b, 0) === n) wrong.unshift({ response: { counts: rc }, expectCode: 'boundary' });
    const top = counts.indexOf(Math.max(...counts)), topName = width === 1 ? `the bar for ${start + top}` : `the ${start + top * width} to under ${start + (top + 1) * width} bar`;
    return { skill, prompt: `${intro} Make a histogram with ${binsText}.`, answer: names.join('; '),
      steps: [width === 1 ? `Count how many times each value appears.` : `The bins are ${counts.map((_, i) => `[${start + i * width}, ${start + (i + 1) * width})`).join(', ')}; a value on a boundary goes in the bin that starts there.`,
        `Counts: ${names.join('; ')}. Check: they add to ${n}.`, skill === 9 ? `The tallest bar is ${topName}: those results are the most common under the model, and results in the short end bars are unusual.` : `The tallest bar is ${topName}; check whether the bars rise to one peak and fall off on both sides, as a normal model predicts.`],
      plot: { tool: 'histogram', title: label[1], bins: { start, width, count, closed: 'left' }, valueAxis: { label: 'Frequency', min: 0, max: 10, step: 1, snap: 1 }, categoryLabel: label[2], source: { type: 'list', values: data }, target: { data },
        feedback: { count: 'Every bar needs a height on the scale.', boundary: 'A value on a boundary goes in the bar that STARTS there. Each bar includes its left edge but not its right edge.', total: `Your bars add up to the wrong total. There are ${n} values.`, position: 'Not quite. Count how many values fall in each interval.' }, check: { type: 'exact' }, testVectors: { correct: { counts }, wrong } },
      alt: `Histogram titled ${label[1]}: ${names.join('; ')}.`, stds: skill === 9 ? ['S-IC.A.2', 'S-ID.A.4'] : ['S-ID.A.4'], fam: skill === 9 ? 'pc-plot-simulation-histogram' : 'pc-plot-normal-histogram', check: { kind: 'hist', data, start, width, count } };
  }
};

// ---------- polar points (vectors skill 09): convert (r, θ) to rectangular and plot
const PI_TXT = { 0: '0', 45: 'π/4', 90: 'π/2', 135: '3π/4', 180: 'π', 225: '5π/4', 270: '3π/2', 315: '7π/4' };
fam.polar = L => {
  for (;;) {
    const pts = [], shown = [], used = new Set();
    while (pts.length < 3) {
      const diag = L > 0 && rnd() < 0.5;
      const deg = diag ? pick([45, 135, 225, 315]) : pick([0, 90, 180, 270]);
      const k = ri(1, diag ? 5 : 7), neg = L === 2 && rnd() < 0.4 ? -1 : 1;
      const rad = deg * Math.PI / 180, r = neg * (diag ? k * Math.SQRT2 : k);
      const x = Math.round(r * Math.cos(rad)), y = Math.round(r * Math.sin(rad));
      const key = x + ',' + y;
      if (used.has(key) || (x === 0 && y === 0) || !inGrid(x, y)) continue;
      used.add(key); pts.push([x, y]);
      shown.push(`(${neg < 0 ? '−' : ''}${diag ? (k === 1 ? '' : k) + '√2' : k}, ${PI_TXT[deg]})`);
    }
    const names = ['A', 'B', 'C'];
    const prompt = `Convert each polar point to rectangular coordinates and plot it: ${shown.map((p, i) => names[i] + p).join(', ')}.`;
    const wrong = [{ response: { points: pts.map(([x, y]) => [y, x]) }, expectCode: 'swapped-coordinates' }, { response: { points: shifted(pts) }, expectCode: 'position' }];
    if (pts.every(([x, y]) => x === y)) wrong.shift();
    return { skill: 9, prompt, answer: pts.map(p => `(${p[0]}, ${p[1]})`).join(', '),
      steps: ['x = r cos θ and y = r sin θ.', ...shown.map((p, i) => `${names[i]}${p} → (${pts[i][0]}, ${pts[i][1]}).`), 'Plot the three rectangular points.'],
      plot: { tool: 'points', grid: GRID, target: { points: pts }, feedback: { position: 'Not quite. Use x = r cos θ and y = r sin θ; a negative r points the opposite way.', 'swapped-coordinates': 'You switched x and y. x = r cos θ goes across; y = r sin θ goes up or down.', count: 'Plot exactly three points.' }, testVectors: { correct: { points: pts }, wrong } },
      alt: `Coordinate grid with the points ${pts.map(p => `(${p[0]}, ${p[1]})`).join(', ')}.`, stds: ['APPC.3.13'], fam: 'pc-plot-polar', check: { kind: 'polar' } };
  }
};

// ---------- complex numbers in the complex plane (vectors skill 12): z, its conjugate and −z
fam.complex = L => {
  for (;;) {
    const a = ri(-7, 7), b = ri(-7, 7);
    if (a === 0 || b === 0 || Math.abs(a) === Math.abs(b)) continue;
    const z = `${minus(a)} ${b > 0 ? '+' : '−'} ${Math.abs(b) === 1 ? '' : Math.abs(b)}i`;
    const kind = L === 0 ? 'conj' : pick(['conj', 'neg', 'times-i']);
    let pts, what, rule;
    if (kind === 'conj') { pts = [[a, b], [a, -b]]; what = 'z and its conjugate z̄'; rule = 'z̄ = a − bi reflects z over the real axis.'; }
    else if (kind === 'neg') { pts = [[a, b], [a, -b], [-a, -b]]; what = 'z, its conjugate z̄ and −z'; rule = 'z̄ reflects z over the real axis; −z = −a − bi is the point opposite z through the origin.'; }
    else { pts = [[a, b], [-b, a]]; what = 'z and iz'; rule = 'iz = i(a + bi) = −b + ai: a quarter turn counterclockwise.'; }
    if (!pts.every(([x, y]) => inGrid(x, y))) continue;
    const prompt = `In the complex plane (real part across, imaginary part up), plot ${what} for z = ${z}.`;
    const wrong = [{ response: { points: pts.map(([x, y]) => [y, x]) }, expectCode: 'swapped-coordinates' }, { response: { points: shifted(pts) }, expectCode: 'position' }];
    return { skill: 12, prompt, answer: pts.map(p => `(${p[0]}, ${p[1]})`).join(', '),
      steps: [`z = ${z} is the point (${a}, ${b}).`, rule, `Plot ${pts.map(p => `(${p[0]}, ${p[1]})`).join(', ')}.`],
      plot: { tool: 'points', grid: GRID, target: { points: pts }, feedback: { position: 'Not quite. a + bi is the point (a, b): the real part across, the imaginary part up.', 'swapped-coordinates': 'You switched the parts. The real part goes across and the imaginary part goes up.', count: `Plot exactly ${pts.length} points.` }, testVectors: { correct: { points: pts }, wrong } },
      alt: `Complex plane with the points ${pts.map(p => `(${p[0]}, ${p[1]})`).join(', ')}.`, stds: ['N-CN.A.3', 'N-CN.B.4'], fam: 'pc-plot-complex', check: { kind: 'complex' } };
  }
};

const as = (f, skill, stds) => L => ({ ...f(L), skill, ...(stds ? { stds } : {}) });
const PLAN = {
  'equations-inequalities': { prefix: 'pc-eqi', mix: [as(fam.system, 8), as(fam.region, 7)] },
  'conics': { prefix: 'pc-con', mix: [as(fam.parabola, 2), as(fam.circle, 1)] },
  'sequences-series-limits': { prefix: 'pc-ssl', mix: [as(fam.arith, 1), as(fam.geom, 1)] },
  'vectors': { prefix: 'pc-vec', mix: [fam.polar, fam.complex] },
};


function main() {
  const render = !process.argv.includes('--no-render');
  const keys = [];
  for (const [unit, { prefix, mix }] of Object.entries(PLAN)) {
    const file = path.join(ROOT, 'question-banks/precalculus', unit + '.json');
    const raw = fs.readFileSync(file, 'utf8'), bank = JSON.parse(raw);
    if (bank.questions.some(q => q.format === 'plot')) { console.log('skip', unit); continue; }
    seed = [...unit].reduce((a, c) => (a * 31 + c.charCodeAt(0)) % 2147483647, 7);
    const used = new Set(bank.questions.map(q => q.prompt));
    const out = [];
    for (const [L, lv] of LEVELS.entries()) {
      const n = {};
      for (let i = 0; i < 8; i++) {
        let it, tries = 0;
        do { it = mix[i % 2](L); tries++; } while (used.has(it.prompt) && tries < 500);
        assert(!used.has(it.prompt), 'could not make a new ' + unit + ' item');
        used.add(it.prompt);
        const sid = String(it.skill).padStart(2, '0');
        n[sid] = (n[sid] || 0) + 1;
        const id = `${prefix}-s${sid}-${lv}-p${String(n[sid]).padStart(3, '0')}`;
        const plot = { ...it.plot, answerKey: { src: `question-banks/assets/plot-keys/${id}.png`, alt: it.alt } };
        if (!plot.check) plot.check = { type: 'exact-after-snap' };
        // The site's grader must accept the key and reject every wrong vector with the expected code.
        assert(P.valid(plot), id + ' valid');
        assert.equal(P.check(plot, plot.testVectors.correct).ok, true, id + ' correct');
        for (const w of plot.testVectors.wrong) { const r = P.check(plot, w.response); assert.equal(r.ok, false, id); assert.equal(r.code, w.expectCode, id + ' ' + JSON.stringify(w)); }
        out.push({ id, skillId: `${unit}-skill-${sid}`, level: lv, format: 'plot', prompt: it.prompt, answer: it.answer, solutionSteps: it.steps, standards: it.stds, sourceNotes: NOTE(it.fam), plot });
        // The widget letters each dragged point (A, B, …); an answer key does not need them.
        let svg = P.blank(plot, plot.testVectors.correct).replace(/<text[^>]*>[A-Z]<\/text>/g, '');
        if (it.check.kind === 'circle') { // draw the circle itself (same grid mapping as core/plot.js: 420 × 342 px for −8…8)
          const [[h, k], [, top]] = plot.target.points, X = v => 38 + (v + 8) / 16 * 420, Y = v => 20 + (8 - v) / 16 * 342;
          svg = svg.replace('</svg>', `<ellipse cx="${X(h)}" cy="${Y(k)}" rx="${(top - k) / 16 * 420}" ry="${(top - k) / 16 * 342}" fill="none" stroke="#1f5fa8" stroke-width="3"/></svg>`);
        }
        keys.push({ id, svg, tool: plot.tool });
      }
    }
    bank.questions.push(...out);
    fs.writeFileSync(file, JSON.stringify(bank, null, 1) + (raw.endsWith('\n') ? '\n' : ''));
    const tp = path.join(ROOT, 'question-banks/precalculus/meta', unit + '.tags.json'), traw = fs.readFileSync(tp, 'utf8'), tags = JSON.parse(traw);
    for (const q of out) tags[q.id] = ['graph'];
    fs.writeFileSync(tp, formatLike(traw, tags));
    console.log(unit, '+', out.length, 'plot items');
  }
  fs.mkdirSync(path.join(__dirname, 'out'), { recursive: true });
  fs.writeFileSync(path.join(__dirname, 'out/keys.json'), JSON.stringify(keys));
  if (render && keys.length) return renderKeys(keys);
}

function formatLike(raw, obj) {
  // tags files use json.dump(indent=0): one value per line
  const ind = raw.startsWith('{\n "') ? 1 : raw.startsWith('{\n  "') ? 2 : 0;
  let s = JSON.stringify(obj, null, ind === 0 ? '\u0000' : ind).replace(/\u0000/g, '');
  return s + (raw.endsWith('\n') ? '\n' : '');
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
