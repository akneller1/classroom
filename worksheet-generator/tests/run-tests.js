/* Mr. K's Classroom worksheet generator — automated math tests.
     node tests/run-tests.js            (1000 problems per sub-lesson, default)
     N=3000 node tests/run-tests.js     (more)
   Every problem is re-checked from what a student would SEE (the displayed text and the drawn
   SVG), using the independent parser in mini.js, not from the generator's internal values. */
'use strict';
const assert = require('assert');
const NS = require('./load.js');
const katex = require('../vendor/katex/katex.min.js');
const T = require('./mini.js');
const { q, Q, maths, stripMath } = T;

const N = +process.env.N || 1000;
const DIFFS = ['basic', 'standard', 'honors'], MODES = ['integers', 'preferred', 'fractions'];
const COMBOS = []; DIFFS.forEach(d => MODES.forEach(m => COMBOS.push({ difficulty: d, numberMode: m })));
const LESSONS = Object.keys(NS.registry.lessons).filter(id => !process.env.ONLY || id === process.env.ONLY);

const fail = (msg) => { throw new Error(msg); };
const eqQ = (a, b, what) => { if (!a.eq(b)) fail(`${what}: got ${a} expected ${b}`); };
const ansTex = (p, i = 0) => maths(p.answer)[i];
const num = s => T.parseNum(s);

/* ---------- drawn-graph helpers ---------- */
function checkSpec(spec, what) {
  const svg = NS.graph(spec, { widthIn: 2.5 }), r = T.readSvg(svg), g = r.g;
  if (r.lines.length !== (spec.lines || []).length) fail(`${what}: ${spec.lines.length} lines specified but ${r.lines.length} drawn (line clipped away?)`);
  (spec.lines || []).forEach((ln, i) => {
    const seg = r.lines[i];
    const exact = ln.kind === 'vline' ? { vert: q(ln.x.n, ln.x.d) } : { m: q(ln.m.n, ln.m.d), b: q(ln.b.n, ln.b.d) };
    if (!T.segmentMatches(seg, exact)) fail(`${what}: drawn segment does not lie on its line`);
    // each end of the segment must sit on the window boundary
    seg.a && [seg.a, seg.b].forEach(pt => {
      const onB = T.near(pt[0], g.xmin) || T.near(pt[0], g.xmax) || T.near(pt[1], g.ymin) || T.near(pt[1], g.ymax);
      if (!onB) fail(`${what}: segment end ${pt} not on window boundary`);
    });
  });
  if (r.points.length !== (spec.points || []).length) fail(`${what}: point count mismatch`);
  if (r.lines.length) r.points.forEach((pt, i) => {                 // marked points must lie ON a drawn line
    const hit = r.lines.some(seg => {
      const [x1, y1] = seg.a, [x2, y2] = seg.b;
      if (Math.abs(x2 - x1) < 0.03) return T.near(pt[0], x1);
      return T.near(pt[1], y1 + (y2 - y1) * (pt[0] - x1) / (x2 - x1));
    });
    if (!hit) fail(`${what}: marked point ${i} (${pt[0].toFixed(2)}, ${pt[1].toFixed(2)}) is not on any drawn line`);
  });
  (spec.points || []).forEach((p, i) => {
    if (!T.near(r.points[i][0], p.x.n === undefined ? p.x : p.x.n / p.x.d) || !T.near(r.points[i][1], p.y.n === undefined ? p.y : p.y.n / p.y.d)) fail(`${what}: point ${i} drawn in wrong place`);
  });
  return r;
}
const isBlank = spec => !(spec.lines && spec.lines.length) && !(spec.points && spec.points.length);
function drawnLine(spec) {                       // exact (m,b) or vert, read from the drawn segment only
  const r = T.readSvg(NS.graph(spec)); const seg = r.lines[0], sl = T.segLine(seg);
  if (sl.vert !== undefined) return { vert: q(Math.round(sl.vert)), r };
  const m = T.ratFromFloat(sl.mf);
  const [ax, ay] = seg.a, [bx, by] = seg.b;
  const y0 = ay + (by - ay) * (0 - ax) / (bx - ax);          // value of the drawn line at x = 0
  return { m, b: T.ratFromFloat(y0), r };
}
const sameLine = (a, b, what) => {
  if ((a.vert !== undefined) !== (b.vert !== undefined)) fail(`${what}: vertical vs non-vertical`);
  if (a.vert !== undefined) return eqQ(a.vert, b.vert, what + ' x=');
  eqQ(a.m, b.m, what + ' slope'); eqQ(a.b, b.b, what + ' intercept');
};
const slopeWord = ln => ln.vert !== undefined ? 'undefined' : ln.m.isZero() ? 'zero' : ln.m.n > 0 ? 'positive' : 'negative';
function latticeCount(ln, w) { let c = 0; for (let x = -w; x <= w; x++) { const y = ln.m.mul(q(x)).add(ln.b); if (y.isInt() && Math.abs(y.n) <= w) c++; } return c; }
/* point-slope form parser:  y-y1=m(x-x1) | y-y1=x-x1 | y-y1=-(x-x1) */
function parsePS(tex) {
  const t = tex.replace(/\\,|\s+/g, '').replace(/\\dfrac/g, '\\frac');
  const L = t.match(/^y(?:([+-])(\d+))?=(.*)$/); if (!L) fail('not point-slope: ' + tex);
  const y1 = L[1] ? q(+L[2]).mul(q(L[1] === '+' ? -1 : 1)) : q(0);
  let R = L[3], m, x1;
  let mm = R.match(/^(-?)(\\frac\{(\d+)\}\{(\d+)\}|\d+)?\(x(?:([+-])(\d+))?\)$/);
  if (mm) {
    const sign = mm[1] ? -1 : 1; let mag = q(1);
    if (mm[2]) mag = mm[3] ? q(+mm[3], +mm[4]) : q(+mm[2]);
    m = mag.mul(q(sign)); x1 = mm[5] ? q(+mm[6]).mul(q(mm[5] === '+' ? -1 : 1)) : q(0);
  } else {
    mm = R.match(/^x(?:([+-])(\d+))?$/); if (!mm) fail('bad point-slope right side: ' + tex);
    m = q(1); x1 = mm[2] ? q(+mm[2]).mul(q(mm[1] === '+' ? -1 : 1)) : q(0);
  }
  return { m, x1, y1 };
}
const isSlopeIntercept = tex => /^y=/.test(tex.replace(/\s+/g, '')) && !/y/.test(tex.replace(/\s+/g, '').slice(2));
const parseLetters = (eqTex, xl) => { const yl = eqTex.split('=')[0].trim(); return T.parseLine(eqTex, { [yl]: 'y', [xl]: 'x' }); };
const ints = s => (String(s).match(/\d+/g) || []).map(Number);

/* ---------- per-lesson independent checkers; each returns a list of coverage tags ---------- */
const C = {};

C['lf-slope-two-points'] = p => {
  const [a, b] = maths(p.prompt).map(T.pointQ);
  const m = b[1].sub(a[1]).div(b[0].sub(a[0]));
  eqQ(num(ansTex(p).replace(/^m=/, '')), m, 'slope');
  // cross-check with a different formula orientation
  eqQ(a[1].sub(b[1]).div(a[0].sub(b[0])), m, 'slope (reversed)');
  return [m.n < 0 ? 'negative' : 'positive', m.isInt() ? 'integer' : 'fraction'];
};

C['lf-slope-graph'] = p => {
  const r = checkSpec(p.fig, 'fig'); if (r.labels.length) fail('figure shows coordinate labels (reveals answer)');
  if (r.lines.length !== 1 || r.points.length !== 2) fail('expected 1 line and 2 marked points');
  const pts = r.points.map(pt => { if (!T.near(pt[0], Math.round(pt[0])) || !T.near(pt[1], Math.round(pt[1]))) fail('marked point is not on a lattice point'); return [Math.round(pt[0]), Math.round(pt[1])]; });
  const m = q(pts[1][1] - pts[0][1], pts[1][0] - pts[0][0]);
  eqQ(m, T.ratFromFloat(T.segLine(r.lines[0]).mf), 'slope of drawn line vs marked points');
  eqQ(num(ansTex(p).replace(/^m=/, '')), m, 'slope');
  return [m.n < 0 ? 'negative' : 'positive', m.isInt() ? 'integer' : 'fraction'];
};

C['lf-slope-table'] = p => {
  const t = T.parseTable(p.prompt); if (!t.x || !t.y || t.x.length !== t.y.length || t.x.length < 4) fail('bad table');
  if (t.y.some(v => v === null)) fail('table has blanks');
  const slopes = t.x.slice(1).map((x, i) => t.y[i + 1].sub(t.y[i]).div(x.sub(t.x[i])));
  slopes.forEach(s => eqQ(s, slopes[0], 'table is linear'));
  eqQ(num(ansTex(p).replace(/^m=/, '')), slopes[0], 'slope');
  const gaps = new Set(t.x.slice(1).map((x, i) => x.sub(t.x[i]).toString()));
  return [slopes[0].n < 0 ? 'negative' : 'positive', slopes[0].isInt() ? 'integer' : 'fraction', gaps.size > 1 ? 'uneven-spacing' : 'even-spacing'];
};

C['lf-slope-missing-coordinate'] = p => {
  const ms = maths(p.prompt); const pa = T.parsePoint(ms[0]), pb = T.parsePoint(ms[1]);
  const m = num(ms[2]); const unknownVar = ms[3];
  let known, unk, ukIdx;
  const isVar = s => s === 'x' || s === 'y';
  if (pa.some(isVar)) { unk = pa; known = pb.map(num); } else { unk = pb; known = pa.map(num); }
  if (!unk.some(isVar) || (isVar(unk[0]) && isVar(unk[1]))) fail('expected exactly one unknown');
  let ans;
  if (isVar(unk[0])) { if (unk[0] !== unknownVar) fail('asked for the wrong variable'); const uy = num(unk[1]); ans = known[0].add(uy.sub(known[1]).div(m)); }
  else { if (unk[1] !== unknownVar) fail('asked for the wrong variable'); const ux = num(unk[0]); ans = known[1].add(m.mul(ux.sub(known[0]))); }
  eqQ(num(ansTex(p).replace(/^[xy]=/, '')), ans, 'missing coordinate');
  if (!ans.isInt()) fail('missing coordinate is not an integer');
  // plug back in
  const full = isVar(unk[0]) ? [ans, num(unk[1])] : [num(unk[0]), ans];
  eqQ(full[1].sub(known[1]).div(full[0].sub(known[0])), m, 'plug-back slope');
  return [unknownVar === 'x' ? 'unknown-x' : 'unknown-y', m.n < 0 ? 'negative' : 'positive', m.isInt() ? 'integer' : 'fraction'];
};

C['lf-slope-classify'] = p => {
  const word = stripMath(p.answer).trim().split(/\s+/)[0].toLowerCase();
  let ln, rep;
  if (p.fig) {
    const r = checkSpec(p.fig, 'fig'); rep = 'graph'; if (r.labels.length) fail('figure labels reveal answer');
    const sl = T.segLine(r.lines[0]); ln = sl.vert !== undefined ? { vert: q(Math.round(sl.vert)) } : { m: T.ratFromFloat(sl.mf), b: q(0) };
  } else {
    const ms = maths(p.prompt);
    if (ms.length === 2 && ms.every(s => s.startsWith('('))) {
      rep = 'points'; const [a, b] = ms.map(T.pointQ);
      ln = b[0].eq(a[0]) ? { vert: a[0] } : { m: b[1].sub(a[1]).div(b[0].sub(a[0])), b: q(0) };
    } else { rep = (/^y=/.test(ms[0]) || /^[xy]=-?\d+$/.test(ms[0])) ? 'eq' : 'std'; ln = T.parseLine(ms[0]); }
  }
  if (slopeWord(ln) !== word) fail(`classified ${word} but line is ${slopeWord(ln)}`);
  if (word !== 'undefined') { const mm = ms2m(p); if (mm && ln.m && !mm.eq(ln.m)) fail('slope value in answer wrong'); }
  return [word, rep];
};
function ms2m(p) { const a = maths(p.answer).find(s => /^\(?m=/.test(s)); return a ? num(a.replace(/^\(?m=/, '').replace(/\)$/, '')) : null; }

C['lf-graph-slope-intercept'] = p => {
  const ln = T.parseLine(maths(p.prompt)[0]); if (ln.vert !== undefined) fail('vertical');
  if (p.fig) { if (!isBlank(p.fig)) fail('student grid is not blank'); checkSpec(p.fig, 'blank grid'); }
  else if (p.figWhere !== 'none') fail('no-grid problem should have figWhere none');
  const r = checkSpec(p.answerFig, 'answer graph'); const d = drawnLine(p.answerFig);
  sameLine(d, ln, 'answer graph vs equation');
  if (r.points.length < 3) fail('answer graph needs >= 3 plotted points');
  r.points.forEach(pt => { const x = q(Math.round(pt[0])), y = q(Math.round(pt[1])); if (!T.near(pt[0], x.n) || !T.near(pt[1], y.n)) fail('plotted point off lattice'); if (!T.onLine(ln, x, y)) fail('plotted point not on the line'); });
  if (latticeCount(ln, 10) < 3) fail('fewer than 3 lattice points available');
  if (!ln.b.isInt()) fail('y-intercept not an integer');
  return [ln.m.n < 0 ? 'negative' : 'positive', ln.m.isInt() ? 'integer' : 'fraction', ln.b.isZero() ? 'b=0' : 'b!=0', p.fig ? 'grid' : 'no-grid'];
};

C['lf-graph-table'] = p => {
  const eq = T.parseEq(maths(p.prompt)[0]); const ln = T.lineOfEq(eq);
  const tb = T.parseTable(p.prompt), tk = T.parseTable(p.keyPrompt);
  if (tb.y.some(v => v !== null)) fail('student table y-row is not blank');
  tb.x.forEach((x, i) => {
    const y = eq.C.sub(eq.A.mul(x)).div(eq.B);                       // solve the displayed equation for y
    if (!y.isInt()) fail('table y not an integer');
    eqQ(tk.y[i], y, `key table y at x=${x}`);
  });
  eqQ(q(tb.x.length), q(5), 'table has 5 columns');
  if (p.fig && !isBlank(p.fig)) fail('student grid is not blank');
  const r = checkSpec(p.answerFig, 'answer graph'); sameLine(drawnLine(p.answerFig), ln, 'answer graph');
  if (r.points.length !== 5) fail('expected 5 plotted points');
  r.points.forEach(pt => { if (!T.onLine(ln, q(Math.round(pt[0])), q(Math.round(pt[1])))) fail('point off line'); });
  return [/y=/.test(maths(p.prompt)[0].split('=')[0]) && maths(p.prompt)[0].startsWith('y') ? 'slope-int-form' : 'standard-form', ln.m.isInt() ? 'integer' : 'fraction'];
};

C['lf-graph-intercepts'] = p => {
  const eq = T.parseEq(maths(p.prompt)[0]); const a = eq.C.div(eq.A), b = eq.C.div(eq.B);
  if (!a.isInt() || !b.isInt() || a.isZero() || b.isZero()) fail('intercepts must be nonzero integers');
  if (eq.A.n <= 0) fail('A must be positive');
  const ptsA = maths(p.answer).filter(s => /intercept/.test(s)).map(s => T.pointQ(s.replace(/^.*intercept: ?\}/, '')));
  if (ptsA.length !== 2) fail('answer should state both intercepts');
  eqQ(ptsA[0][0], a, 'x-intercept'); eqQ(ptsA[0][1], q(0), 'x-intercept y'); eqQ(ptsA[1][0], q(0), 'y-intercept x'); eqQ(ptsA[1][1], b, 'y-intercept');
  const ln = T.lineOfEq(eq); const r = checkSpec(p.answerFig, 'answer graph'); sameLine(drawnLine(p.answerFig), ln, 'answer graph');
  if (r.points.length !== 2) fail('expected two intercept points');
  if (p.fig && !isBlank(p.fig)) fail('student grid not blank');
  return [a.n < 0 ? 'x-int<0' : 'x-int>0', b.n < 0 ? 'y-int<0' : 'y-int>0'];
};

C['lf-graph-horizontal-vertical'] = p => {
  const eqs = maths(p.prompt).filter(s => /^[xy]=-?\d+$/.test(s)).map(s => ({ v: s[0], c: q(+s.slice(2)) }));
  if (!eqs.length) fail('no equation found');
  const r = checkSpec(p.answerFig, 'answer graph');
  if (r.lines.length !== eqs.length) fail('wrong number of drawn lines');
  eqs.forEach(e => {
    const ok = r.lines.some(seg => e.v === 'x' ? T.segmentMatches(seg, { vert: e.c }) : T.segmentMatches(seg, { m: q(0), b: e.c }));
    if (!ok) fail(`line ${e.v}=${e.c} not drawn correctly`);
  });
  if (eqs.length === 1) {
    const text = stripMath(p.answer) + maths(p.answer).join(' ');
    if (eqs[0].v === 'y' && !/=0/.test(maths(p.answer)[0] || '')) fail('horizontal slope should be 0');
    if (eqs[0].v === 'x' && !/undefined/.test(p.answer)) fail('vertical slope should be undefined');
  } else {
    const h = eqs.find(e => e.v === 'x').c, k = eqs.find(e => e.v === 'y').c;
    const pt = T.pointQ(maths(p.answer).find(s => s.startsWith('(')));
    eqQ(pt[0], h, 'intersection x'); eqQ(pt[1], k, 'intersection y');
  }
  if (p.fig && !isBlank(p.fig)) fail('student grid not blank');
  return [eqs.length === 2 ? 'both' : eqs[0].v === 'y' ? 'horizontal' : 'vertical'];
};

C['lf-write-from-graph'] = p => {
  const r = checkSpec(p.fig, 'fig'); if (r.labels.length) fail('figure labels reveal the answer');
  if (r.lines.length !== 1 || r.points.length !== 2) fail('expected 1 line and 2 marked points');
  const ans = ansTex(p), sl = T.segLine(r.lines[0]);
  const pts = r.points.map(pt => { if (!T.near(pt[0], Math.round(pt[0])) || !T.near(pt[1], Math.round(pt[1]))) fail('marked point off lattice'); return [q(Math.round(pt[0])), q(Math.round(pt[1]))]; });
  if (sl.vert !== undefined) {
    const ln = T.parseLine(ans); if (ln.vert === undefined || !ln.vert.eq(q(Math.round(sl.vert)))) fail('vertical line equation wrong');
    pts.forEach(pt => eqQ(pt[0], ln.vert, 'marked pt on vertical'));
    return ['vertical'];
  }
  const m = T.ratFromFloat(sl.mf), ln = T.parseLine(ans);
  if (!isSlopeIntercept(ans)) fail('answer not in slope-intercept form');
  eqQ(ln.m, m, 'slope read from drawn line'); pts.forEach(pt => { if (!T.onLine(ln, pt[0], pt[1])) fail('marked point not on answer line'); });
  const yint = q(0).sub(q(0)); if (!ln.b.isInt()) fail('y-intercept not integer');
  return [m.isZero() ? 'horizontal' : m.n < 0 ? 'negative' : 'positive', m.isInt() ? 'integer' : 'fraction', ln.b.isZero() ? 'b=0' : 'b!=0'];
};

C['lf-write-two-points'] = p => {
  const [a, b] = maths(p.prompt).map(T.pointQ); const ans = ansTex(p), ln = T.parseLine(ans);
  if (!T.onLine(ln, a[0], a[1]) || !T.onLine(ln, b[0], b[1])) fail('a given point is not on the answer line');
  if (ln.vert === undefined && !isSlopeIntercept(ans)) fail('not slope-intercept form');
  if (ln.vert === undefined) eqQ(ln.m, b[1].sub(a[1]).div(b[0].sub(a[0])), 'slope'); else eqQ(a[0], b[0], 'vertical needs equal x');
  const tag = ln.vert !== undefined ? 'vertical' : ln.m.isZero() ? 'horizontal' : ln.m.n < 0 ? 'negative' : 'positive';
  return [tag, ln.vert === undefined && !ln.m.isInt() ? 'fraction-slope' : 'int-slope', ln.vert === undefined && !ln.b.isInt() ? 'fraction-intercept' : 'int-intercept'];
};

C['lf-write-slope-point'] = p => {
  const ms = maths(p.prompt); const m = num(ms[0].replace(/^m=/, '')), pt = T.pointQ(ms[1]);
  const ans = ansTex(p), ln = T.parseLine(ans);
  if (!isSlopeIntercept(ans)) fail('not slope-intercept form');
  eqQ(ln.m, m, 'slope'); if (!T.onLine(ln, pt[0], pt[1])) fail('point not on answer line');
  return [m.isZero() ? 'zero-slope' : m.n < 0 ? 'negative' : 'positive', m.isInt() ? 'integer' : 'fraction', ln.b.isInt() ? 'int-intercept' : 'fraction-intercept'];
};

C['lf-write-parallel-perpendicular'] = p => {
  const ms = maths(p.prompt), text = stripMath(p.prompt);
  if (/Line 1:/.test(p.prompt)) {
    const l1 = T.parseLine(ms[0]), l2 = T.parseLine(ms[1]);
    const rel = l1.m.eq(l2.m) ? (l1.b.eq(l2.b) ? 'same' : 'parallel') : l1.m.mul(l2.m).eq(q(-1)) ? 'perpendicular' : 'neither';
    if (rel === 'same') fail('the two lines are identical');
    if (rel !== stripMath(p.answer).trim().toLowerCase()) fail(`classified ${stripMath(p.answer).trim()} but they are ${rel}`);
    return ['classify-' + rel, /\dy|y[+-]|x[+-]\d*y/.test(ms[0] + ms[1]) && !/^y=/.test(ms[1]) ? 'standard-form' : 'slope-int'];
  }
  const given = T.parseLine(ms[0]), pt = T.pointQ(ms[1]), ans = ansTex(p), ln = T.parseLine(ans);
  if (!isSlopeIntercept(ans)) fail('answer not slope-intercept');
  const perp = /perpendicular/.test(text);
  if (perp) { if (!ln.m.mul(given.m).eq(q(-1))) fail('slopes are not negative reciprocals'); } else if (!ln.m.eq(given.m)) fail('slopes differ for a parallel line');
  if (!T.onLine(ln, pt[0], pt[1])) fail('answer line misses the point');
  if (ln.m.eq(given.m) && ln.b.eq(given.b)) fail('answer is the given line');
  if (!ln.b.isInt()) fail('intercept not an integer');
  return [perp ? 'perpendicular' : 'parallel', /\d*y/.test(ms[0].replace(/^y=/, '')) || !/^y=/.test(ms[0]) ? 'standard-form' : 'slope-int', ln.m.isInt() ? 'int-slope' : 'fraction-slope'];
};

C['lf-identify-slope-intercept'] = p => {
  const ln = T.parseLine(maths(p.prompt)[0]); const ms = maths(p.answer);
  eqQ(num(ms[0].replace(/^m=/, '')), ln.m, 'slope'); eqQ(num(ms[1].replace(/^b=/, '')), ln.b, 'y-intercept');
  const t = maths(p.prompt)[0];
  return [/^f\(x\)/.test(t) ? 'function-notation' : ln.m.isZero() ? 'horizontal' : ln.b.isZero() ? 'b=0' : /^y=-?\d+(\\frac)?[^x]*[+-]/.test(t) && !/x/.test(t.split('=')[1].split(/[+-]/)[0]) ? 'commuted' : 'plain', ln.m.isInt() ? 'int-slope' : 'fraction-slope', ln.b.isInt() ? 'int-b' : 'fraction-b'];
};

C['lf-std-to-slope-intercept'] = p => {
  const eq = T.parseEq(maths(p.prompt)[0]), ln = T.lineOfEq(eq); const ans = ansTex(p);
  if (!isSlopeIntercept(ans)) fail('answer not in y = mx + b form'); sameLine(T.parseLine(ans), ln, 'converted equation');
  // numeric spot check: points of the original satisfy the answer
  [-3, 0, 2, 5].forEach(x => { const xq = q(x), y = eq.C.sub(eq.A.mul(xq)).div(eq.B); if (!T.onLine(T.parseLine(ans), xq, y)) fail('spot-check failed at x=' + x); });
  return [eq.B.n === 1 ? 'B=1' : eq.B.n === -1 ? 'B=-1' : 'B>1', ln.m.isInt() ? 'int-slope' : 'fraction-slope', ln.b.isInt() ? 'int-b' : 'fraction-b'];
};

C['lf-slope-intercept-to-std'] = p => {
  const ln = T.parseLine(maths(p.prompt)[0]); const eq = T.parseEq(ansTex(p));
  if (![eq.A, eq.B, eq.C].every(v => v.isInt())) fail('standard form coefficients are not integers');
  if (eq.A.n <= 0) fail('A must be positive'); if (T.gcd(T.gcd(eq.A.n, eq.B.n), eq.C.n) !== 1) fail('coefficients share a common factor');
  sameLine(T.lineOfEq(eq), ln, 'converted equation');
  [-4, 0, 3, 7].forEach(x => { const xq = q(x), y = ln.m.mul(xq).add(ln.b); if (!eq.A.mul(xq).add(eq.B.mul(y)).eq(eq.C)) fail('spot check failed'); });
  const hadFrac = !ln.m.isInt() || !ln.b.isInt();
  return [hadFrac ? 'clear-fractions' : 'integers-only', eq.B.n < 0 ? 'B<0' : 'B>0'];
};

C['lf-write-point-slope'] = p => {
  const ms = maths(p.prompt);
  const a1 = parsePS(ansTex(p));
  if (/^m=/.test(ms[0])) {
    eqQ(a1.m, num(ms[0].replace(/^m=/, '')), 'slope'); const pt = T.pointQ(ms[1]); eqQ(a1.x1, pt[0], 'x1'); eqQ(a1.y1, pt[1], 'y1');
    return ['slope-point', a1.m.isInt() ? 'int-slope' : 'fraction-slope', a1.m.n < 0 ? 'negative' : 'positive'];
  }
  const [P, Q2] = ms.map(T.pointQ); const m = Q2[1].sub(P[1]).div(Q2[0].sub(P[0]));
  eqQ(a1.m, m, 'slope'); eqQ(a1.x1, P[0], 'x1 (first listed point)'); eqQ(a1.y1, P[1], 'y1');
  const a2 = parsePS(maths(p.answer)[1]); eqQ(a2.m, m, 'alt slope'); eqQ(a2.x1, Q2[0], 'alt x1'); eqQ(a2.y1, Q2[1], 'alt y1');
  return ['two-points', m.isInt() ? 'int-slope' : 'fraction-slope', m.n < 0 ? 'negative' : 'positive'];
};

C['lf-point-slope-to-slope-intercept'] = p => {
  const ps = parsePS(maths(p.prompt)[0]); const ans = ansTex(p), ln = T.parseLine(ans);
  if (!isSlopeIntercept(ans)) fail('answer not slope-intercept');
  eqQ(ln.m, ps.m, 'slope'); eqQ(ln.b, ps.y1.sub(ps.m.mul(ps.x1)), 'intercept');
  return [ps.m.eq(q(1)) ? 'm=1' : ps.m.eq(q(-1)) ? 'm=-1' : 'other', ps.m.isInt() ? 'int-slope' : 'fraction-slope', ln.b.isInt() ? 'int-b' : 'fraction-b'];
};

C['lf-interpret-slope-intercept'] = p => {
  const ms = maths(p.prompt), eqTex = ms[0], xl = ms[1];
  const ln = parseLetters(eqTex, xl); const am = maths(p.answer);
  eqQ(num(am[0].replace(/^m=/, '')), ln.m, 'slope'); eqQ(num(am[1].replace(/^b=/, '')), ln.b, 'intercept');
  const txt = stripMath(p.answer);
  if (!txt.includes(String(Math.abs(ln.m.n)))) fail('slope meaning does not mention the rate');
  if (!txt.includes(String(ln.b.n))) fail('intercept meaning does not mention the starting amount');
  if (ln.m.n < 0 && !/negative|decreas|shorter|drops|left/.test(txt)) fail('negative slope meaning missing');
  return [ln.m.n < 0 ? 'decreasing' : 'increasing'];
};

C['lf-word-problems'] = p => {
  const stem = p.prompt.split('<div class="parts">')[0], partsHtml = p.prompt.split('<div class="parts">')[1];
  const part = (html, k) => { const m = html.match(new RegExp('<b>\\(' + k + '\\)</b>([\\s\\S]*?)</div>')); return m ? m[1] : ''; };
  const ansPart = k => { const m = p.answer.match(new RegExp('<b>\\(' + k + '\\)</b>([^<]*)')); return m ? m[1] : ''; };
  if (/Assume the relationship is linear/.test(stem)) {
    const n = ints(stripMath(stem.split('Assume')[0])); if (n.length !== 4) fail('expected two data points, got ' + n);
    const [x1, y1, x2, y2] = n.map(v => q(v)); const m = y2.sub(y1).div(x2.sub(x1)); if (!m.isInt()) fail('slope not whole'); const b = y1.sub(m.mul(x1));
    eqQ(num(ansPart('a').replace(/^\s*\u27E8m=/, '').replace(/\u27E9\s*$/, '')), m, 'rate of change');
    const xl = maths(part(partsHtml, 'b'))[1], eqT = maths(ansPart('b'))[0]; const ln = parseLetters(eqT, xl);
    eqQ(ln.m, m, 'equation slope'); eqQ(ln.b, b, 'equation intercept');
    const x3 = num(maths(part(partsHtml, 'c')).find(s => /=\d/.test(s)).split('=')[1]);
    const val = num(maths(ansPart('c'))[0].split('=')[1]); eqQ(val, m.mul(x3).add(b), 'prediction');
    if (val.n <= 0) fail('prediction not positive');
    return ['two-points', m.n < 0 ? 'decreasing' : 'increasing'];
  }
  const n = ints(stripMath(stem)); if (n.length !== 2) fail('scenario should have 2 numbers, got ' + n);
  const [b0, m0] = n.map(v => q(v)); const dec = /burns down|drained|drops/.test(stem);
  const xl = maths(part(partsHtml, 'a'))[1], eqT = maths(ansPart('a'))[0]; const ln = parseLetters(eqT, xl);
  eqQ(ln.b, b0, 'starting amount'); eqQ(ln.m, dec ? m0.neg() : m0, 'rate');
  const xA = q(ints(stripMath(part(partsHtml, 'b')))[0]); const yAns = q(ints(ansPart('b'))[0]); eqQ(yAns, ln.m.mul(xA).add(ln.b), 'evaluated value');
  const yT = q(ints(stripMath(part(partsHtml, 'c')))[0]); const xAns = q(ints(ansPart('c'))[0]); eqQ(ln.m.mul(xAns).add(ln.b), yT, 'solved input gives the target');
  if (yT.n <= 0 || yAns.n <= 0) fail('non-positive quantity');
  return ['forward', dec ? 'decreasing' : 'increasing'];
};

C['lf-compare-functions'] = p => {
  const panels = [...p.prompt.matchAll(/<div class="panel"><div class="ph">Function ([AB])<\/div>([\s\S]*?)<\/div>(?=<div class="panel">|<\/div><div class="parts">)/g)];
  if (panels.length !== 2) fail('expected two panels, got ' + panels.length);
  const L = panels.map(pn => {
    const body = pn[2];
    if (/\[\[fig:(\d)\]\]/.test(body)) {
      const idx = +body.match(/\[\[fig:(\d)\]\]/)[1]; const r = checkSpec(p.figs[idx], 'fig' + idx); if (r.labels.length) fail('graph labels reveal answer');
      const d = drawnLine(p.figs[idx]); if (r.points.length !== 2) fail('graph needs 2 marked points'); r.points.forEach(pt => { if (!T.near(pt[0], Math.round(pt[0])) || !T.near(pt[1], Math.round(pt[1]))) fail('graph pt off lattice'); });
      // slope from the two marked points must equal the drawn line
      const a = r.points.map(pt => [q(Math.round(pt[0])), q(Math.round(pt[1]))]); const m = a[1][1].sub(a[0][1]).div(a[1][0].sub(a[0][0]));
      eqQ(m, d.m, 'marked points vs drawn line'); return { kind: 'graph', m: d.m, b: d.b };
    }
    if (/<table/.test(body)) {
      const t = T.parseTable(body); const m = t.y[1].sub(t.y[0]).div(t.x[1].sub(t.x[0])); const b = t.y[0].sub(m.mul(t.x[0]));
      t.x.forEach((x, i) => eqQ(t.y[i], m.mul(x).add(b), 'table linear')); return { kind: 'table', m, b, hasZero: t.x.some(x => x.isZero()) };
    }
    const ln = T.parseLine(maths(body)[0]); return { kind: 'eq', m: ln.m, b: ln.b };
  });
  if (L[0].m.eq(L[1].m) || L[0].b.eq(L[1].b)) fail('functions tie on slope or intercept');
  const ans = p.answer; const pick = k => (ans.match(new RegExp('<b>\\(' + k + '\\)</b> Function ([AB])')) || [])[1];
  const gm = L[0].m.sub(L[1].m).n > 0 ? 'A' : 'B', gb = L[0].b.sub(L[1].b).n > 0 ? 'A' : 'B';
  if (pick('a') !== gm) fail('wrong function for greater slope'); if (pick('b') !== gb) fail('wrong function for greater intercept');
  if (/\(c\)/.test(p.prompt)) {
    const x0 = num(maths(p.prompt.split('(c)')[1])[0].replace(/^x=/, ''));
    const vA = L[0].m.mul(x0).add(L[0].b), vB = L[1].m.mul(x0).add(L[1].b); if (vA.eq(vB)) fail('values tie');
    if (pick('c') !== (vA.sub(vB).n > 0 ? 'A' : 'B')) fail('wrong function for greater value');
  }
  return [L.map(l => l.kind).join('+'), gm === gb ? 'same-winner' : 'split-winner'];
};

/* ---------- generic checks that apply to every problem ---------- */
function katexOk(tex, what) {
  try { katex.renderToString(tex.replace(/\\frac/g, '\\dfrac'), { throwOnError: true, output: 'html' }); }
  catch (e) { fail(`KaTeX error in ${what}: ${JSON.stringify(tex)} — ${e.message}`); }
}
function generic(p, id, S) {
  ['prompt', 'answer'].forEach(k => { if (typeof p[k] !== 'string' || !p[k].trim()) fail('missing ' + k); });
  const all = [p.prompt, p.keyPrompt || '', p.answer].concat(p.steps || []);
  all.forEach((s, i) => {
    const opens = (s.match(/\u27E8/g) || []).length, closes = (s.match(/\u27E9/g) || []).length;
    if (opens !== closes) fail('unbalanced math markers in ' + s);
    maths(s).forEach(t => {
      if (!t.trim()) fail('empty math segment');
      katexOk(t, 'segment ' + i);
      if (/[*^]/.test(t)) fail('raw programming syntax in math: ' + t);
      if (/\//.test(t)) fail('slash in math (use stacked fractions): ' + t);
      if (/NaN|undefined|Infinity|null|\[object/.test(t)) fail('bad value in math: ' + t);
      if (/\}\{0\}/.test(t) && !(id === 'lf-slope-classify' && i >= 3)) fail('division by zero shown: ' + t);
    });
    const text = stripMath(s).replace(/\b(is|an|Slope is|slope is) undefined\b|^\s*Undefined\b|\bundefined slope\b|\bundefined\)/gi, '');
    if (/NaN|undefined|Infinity|\[object|\bnull\b/.test(text)) fail('bad value in text: ' + text);
  });
  [p.fig, p.answerFig].concat(p.figs || []).forEach((spec, i) => { if (spec) { checkSpec(spec, 'spec' + i); } });
  if (p.fig && p.fig.points) p.fig.points.forEach(pt => { if (pt.label) fail('student figure labels a point'); });
  if (S.numberMode === 'integers') {
    if (/\\frac/.test(p.answer)) fail('fraction in answer under integers-only: ' + p.answer);
    if (/\\frac/.test(p.prompt) && id !== 'lf-write-parallel-perpendicular') fail('fraction in prompt under integers-only: ' + p.prompt);
  }
  if (S.difficulty === 'basic') {
    const big = [...p.prompt.matchAll(/-?\d+/g)].map(m => Math.abs(+m[0])).filter(n => n > 200);
    if (big.length) fail('basic problem contains a large number');
  }
}

/* ---------- run ---------- */
let totalFail = 0, totalProblems = 0; const t0 = Date.now(); const covAll = {};
const CHECKED = LESSONS.filter(id => C[id]);
const missing = LESSONS.filter(id => !C[id]);
if (missing.length) { console.log('NO CHECKER for', missing.join(', ')); totalFail++; }

console.log(`Testing ${LESSONS.length} sub-lessons x ${N} problems (difficulty x number-mode matrix, grids on/off, all slots)\n`);
LESSONS.forEach((id, li) => {
  const errs = [], cov = {}; let attempts = 0, maxAttempts = 0;
  for (let i = 0; i < N; i++) {
    const S = Object.assign({}, COMBOS[i % COMBOS.length], { grids: i % 5 !== 0, seed: 700000 + li * 100003 + i * 7919, slot: i % 12 });
    let p;
    try { p = NS.generateOne(id, S); } catch (e) { errs.push({ i, S, msg: 'GENERATION FAILED: ' + e.message }); continue; }
    attempts += p.attempts; maxAttempts = Math.max(maxAttempts, p.attempts);
    try { generic(p, id, S); const tags = C[id](p, S) || []; tags.forEach(t => { cov[t] = (cov[t] || 0) + 1; }); }
    catch (e) { if (process.env.STACK) console.log(e.stack); errs.push({ i, S, msg: e.message, prompt: stripMath(p.prompt).slice(0, 120) + ' | ' + maths(p.prompt).join(' ; ').slice(0, 140), answer: maths(p.answer).join(' ; ').slice(0, 100) }); }
  }
  totalProblems += N; totalFail += errs.length;
  const tagStr = Object.keys(cov).sort().map(k => `${k}:${cov[k]}`).join(' ');
  console.log(`${errs.length ? 'FAIL' : ' ok '}  ${id.padEnd(36)} ${N - errs.length}/${N}  avg tries ${(attempts / N).toFixed(1)} max ${maxAttempts}`);
  console.log(`        coverage: ${tagStr}`);
  covAll[id] = cov;
  errs.slice(0, 4).forEach(e => console.log(`        ✗ #${e.i} [${e.S.difficulty}/${e.S.numberMode}/slot ${e.S.slot}] ${e.msg}\n          ${e.prompt || ''}\n          ans: ${e.answer || ''}`));
});

/* ---------- required edge-case coverage ---------- */
console.log('\nEdge-case coverage requirements');
const need = (id, tag, min0) => { const min = Math.ceil(min0 * N / 1000); const n = (covAll[id] || {})[tag] || 0; const ok = n >= min; if (!ok) totalFail++; console.log(`  ${ok ? ' ok ' : 'FAIL'}  ${id} / ${tag}: ${n} (need >= ${min})`); };
['positive', 'negative', 'zero', 'undefined'].forEach(t => need('lf-slope-classify', t, 160));
need('lf-slope-two-points', 'negative', 250); need('lf-slope-two-points', 'fraction', 100);
need('lf-slope-table', 'uneven-spacing', 30);
need('lf-slope-missing-coordinate', 'unknown-x', 330); need('lf-slope-missing-coordinate', 'unknown-y', 330);
need('lf-write-from-graph', 'horizontal', 20); need('lf-write-from-graph', 'vertical', 15); need('lf-write-from-graph', 'b=0', 10);
need('lf-write-two-points', 'horizontal', 15); need('lf-write-two-points', 'vertical', 15); need('lf-write-two-points', 'fraction-intercept', 10);
need('lf-write-slope-point', 'zero-slope', 15);
need('lf-graph-horizontal-vertical', 'horizontal', 100); need('lf-graph-horizontal-vertical', 'vertical', 100); need('lf-graph-horizontal-vertical', 'both', 100);
need('lf-graph-slope-intercept', 'no-grid', 100); need('lf-graph-slope-intercept', 'b=0', 10); need('lf-graph-slope-intercept', 'fraction', 100);
need('lf-graph-table', 'standard-form', 20);
need('lf-write-parallel-perpendicular', 'perpendicular', 100); need('lf-write-parallel-perpendicular', 'parallel', 50); need('lf-write-parallel-perpendicular', 'classify-neither', 30); need('lf-write-parallel-perpendicular', 'standard-form', 20);
need('lf-identify-slope-intercept', 'function-notation', 50); need('lf-identify-slope-intercept', 'horizontal', 15); need('lf-identify-slope-intercept', 'b=0', 30);
need('lf-std-to-slope-intercept', 'B=-1', 20); need('lf-std-to-slope-intercept', 'B>1', 100);
need('lf-slope-intercept-to-std', 'clear-fractions', 100);
need('lf-point-slope-to-slope-intercept', 'm=-1', 5); need('lf-point-slope-to-slope-intercept', 'm=1', 5);
need('lf-interpret-slope-intercept', 'decreasing', 100); need('lf-word-problems', 'decreasing', 100); need('lf-word-problems', 'two-points', 100);

console.log(`\n${totalProblems} problems checked in ${((Date.now() - t0) / 1000).toFixed(1)}s — ${totalFail === 0 ? 'ALL CHECKS PASSED' : totalFail + ' FAILURE(S)'}`);
process.exitCode = totalFail ? 1 : 0;
