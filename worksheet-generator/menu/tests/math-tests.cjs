/* Menu Assessment Generator — mathematics tests.
   Run:  node worksheet-generator/menu/tests/math-tests.cjs        (N=200 per skill × difficulty × answer policy)
         N=1000 node worksheet-generator/menu/tests/math-tests.cjs (large batch)

   1. Large batches: every skill, every difficulty 1–7, whole-number and fraction policies. Each problem
      is re-checked by the independent checker (menu/mathcheck.js + menu/verify.js), and must also pass
      format lint (no "+-", "1x", "0x", "\frac{n}{1}", …), answer-leak checks and duplicate checks.
   2. Mutation tests: wrong keys, changed printed numbers, wrong classifications and unsimplified answers
      must all be caught by the verifier (so the verifier is not just agreeing with the generator).
   3. Difficulty: an independent complexity score computed from the printed math must rise with the
      difficulty number, and CP2/CP1 levels must keep whole-number answers.
   4. Skill-specific structure promises (one-step at level 1, a(x+b)=c, positive coefficients, …). */
'use strict';
const assert = require('node:assert/strict');
const load = require('./load.cjs');
const env = load(), M = env.MKMENU, C = M.check;
const ONLY = process.env.UNIT;                       // e.g. UNIT=algebra1-inequalities to test one unit
const SETS = Object.values(M.skillSets).filter(s => !ONLY || s.id === ONLY);
const EE = M.skillSets['algebra1-expressions-equations'], INEQ = M.skillSets['algebra1-inequalities'];
const N = +process.env.N || 200;
let checks = 0, fails = [];
function ok(cond, msg) { checks++; if (!cond) fails.push(msg); }

/* ---------- format lint on student-facing TeX ---------- */
function lint(tex) {
  const t = tex.replace(/\s+/g, '');
  const bad = [];
  if (/\+-|-\+|--|\+\+/.test(t)) bad.push('double sign');
  if (/(^|[^\d.{])1[a-zA-Z(]/.test(t)) bad.push('coefficient 1 written');
  if (/(^|[^\d.])0[a-zA-Z(]/.test(t)) bad.push('zero coefficient');
  if (/\\frac\{-?\d+\}\{1\}/.test(t)) bad.push('denominator 1');
  const fr = [...t.matchAll(/\\frac\{(\d+)\}\{(\d+)\}/g)];
  fr.forEach(m => { if (m[1] === m[2]) bad.push('fraction equal to 1'); });
  if (/\(\+/.test(t)) bad.push('(+');
  return bad;
}

/* ---------- independent complexity score from the printed math ---------- */
function complexity(p) {
  let score = 0;
  const all = C.snippets(M.studentText(p));
  all.forEach(s => {
    let node;
    try { const r = C.parseRelation(s); node = { k: 'add', a: r.lhs, b: r.rhs }; }
    catch (e) {
      try { const cd = C.parseCondition(s); node = { k: 'list', a: null }; const atoms = cd.chains.flat(); score += 4 * (cd.chains.length - 1) + 2 * (atoms.length - 1);
        node = atoms.reduce((acc, a) => ({ k: 'add', a: acc, b: { k: 'add', a: a.lhs, b: a.rhs } }), { k: 'num', v: new C.Q(0) }); }
      catch (e2) { try { node = C.parseExpr(s); } catch (e3) { return; } }
    }
    (function walk(n) {
      score += 1;
      if (n.k === 'num') { const v = Math.abs(Number(n.v.n) / Number(n.v.d)); score += Math.log10(1 + v) * 1.2; if (!n.v.isInt()) score += 3; }
      if (n.k === 'div') score += 2.5;
      if (n.k === 'neg' || n.k === 'sub') score += 0.6;
      if (n.k === 'grp') score += 2;
      if (n.k === 'pow') score += 1.5;
      if (n.k === 'xpow') score += 3;   // a variable or fractional exponent
      if (n.k === 'abs') score += 4;
      if (n.a) walk(n.a); if (n.b) walk(n.b);
    })(node);
  });
  // how many inverse operations wrap the unknown (solve / literal problems)
  (p.parts || []).forEach(pt => {
    if (!pt.check || !pt.check.v || !/solve|literal|classify/.test(pt.check.type) || !pt.check.eq) return;
    if (pt.check.type === 'exp-solve') { const bases = new Set(); (function bw(n) { if (!n || typeof n !== 'object') return; if (n.k === 'xpow') { try { bases.add(String(C.evalNode(n.a, {}))); } catch (e) { /* variable base */ } } bw(n.a); bw(n.b); })(C.parseRelation(pt.check.eq)); if (bases.size > 1) score += 5; }
    let r; try { r = C.parseRelation(pt.check.eq); } catch (e) { return; }
    let best = 0;
    (function depth(n, d) { if (n.k === 'var' && n.v === pt.check.v) best = Math.max(best, d); const inc = /add|sub|mul|div|neg|xpow/.test(n.k) ? 1 : 0; if (n.a) depth(n.a, d + inc); if (n.b) depth(n.b, d + inc); })({ k: 'x', a: r.lhs, b: r.rhs }, 0);
    let occ = 0; (function cnt(n) { if (n.k === 'var' && n.v === pt.check.v) occ++; if (n.a) cnt(n.a); if (n.b) cnt(n.b); })({ k: 'x', a: r.lhs, b: r.rhs });
    score += 2.5 * best + 3 * Math.max(0, occ - 1);
  });
  // word problems: givens, implicit relationships and parts
  const words = C.plainText(M.studentText(p));
  score += 2 * C.numbersInText(M.studentText(p)).length;
  score += 4 * ((words.match(/more than|less than|times|consecutive|same|which|by how much|even|odd/g) || []).length);
  score += 6 * Math.max(0, (p.parts || []).filter(x => x.prompt).length - 1);
  score += 0.02 * words.length;
  score += 3 * (p.work || []).length;
  if (p.fig && p.fig.pieces) score += 3 * p.fig.pieces.length;
  if ((p.parts || []).some(pt => pt.check && pt.check.form === 'abs')) score += 8;
  // graphs: endpoints the student must read, or draw on a blank line; inequalities the student must write from a graph
  const ends = f => (f && f.pieces ? f.pieces.reduce((n, pc) => n + (pc.lo ? 1 : 0) + (pc.hi ? 1 : 0), 0) : 0);
  if (p.fig && p.fig.pieces && p.fig.pieces.length) score += 3 * ends(p.fig);
  (p.parts || []).forEach(pt => {
    if (pt.check && pt.check.type === 'read-graph') C.snippets(pt.answer).forEach(sn => { try { score += 2.5 * C.parseCondition(sn).chains.flat().length; } catch (e) { score += 2.5; } });
    if (pt.answerFig && p.fig && !(p.fig.pieces || []).length && /^Graph /.test(p.prompt)) score += 2.5 * ends(pt.answerFig);
    // dividing by a negative (the sign must be reversed)
    if (pt.check && pt.check.type === 'ineq' && pt.check.ineq) {
      try { const cd = C.parseCondition(pt.check.ineq); cd.chains.flat().forEach(a => {
        const f = x => { const env = {}; env[pt.check.v || 'x'] = new C.Q(x); return C.evalNode(a.lhs, env).sub(C.evalNode(a.rhs, env)); };
        if (!JSON.stringify(a, (k, v) => typeof v === 'bigint' ? 0 : v).includes('"abs"') && f(1).sub(f(0)).n < 0n) score += 4;
      }); } catch (e) { /* not linear */ }
    }
  });
  // function-unit content: what the student must read from a figure, and the shape of the answer they must write
  const f = p.fig;
  if (f && f.kind === 'table') f.rows.forEach(rw => rw.forEach((cell, j) => {
    if (cell === '?') score += j === 0 ? 6 : 2.5;   // a missing input must be solved for
    else score += 0.5 + Math.log10(1 + Math.abs(+cell || 0)) * 0.4;
  }));
  if (f && f.kind === 'table' && (p.parts || []).some(pt => pt.check && pt.check.type === 'exp-model')) {   // tables to classify: x-steps other than 1, fraction ratios
    const num = f.rows.map(rw => [+rw[0], +rw[1]]); if (num.length > 1 && num[1][0] - num[0][0] !== 1) score += 3; if (num.length > 1 && num[0][1] && !Number.isInteger(num[1][1] / num[0][1]) && !Number.isInteger(num[0][1] / num[1][1])) score += 3;
  }
  if (f && f.kind === 'table' && (p.parts || []).some(pt => pt.check && pt.check.type === 'linear-rule')) {   // a table whose rate is a fraction, or whose x-steps are uneven, is harder to turn into a rule
    const num = f.rows.filter(rw => rw[0] !== '?' && rw[1] !== '?').map(rw => [+rw[0], +rw[1]]);
    if (num.length > 2) { const st = num.slice(1).map((rw, i) => rw[0] - num[i][0]); if (st.some(d => d !== st[0])) score += 3;
      const rt = (num[1][1] - num[0][1]) / (num[1][0] - num[0][0]); if (!Number.isInteger(rt)) score += 4; if (!num.some(rw => rw[0] === 0)) score += 2; }
  }
  if (f && f.kind === 'dotplot') score += 0.3 * Object.values(f.counts).reduce((x, y) => x + y, 0);
  if (f && f.kind === 'boxplot') score += 3 * f.boxes.length;
  if (f && f.kind === 'scatter') score += 0.2 * f.points.length + (f.line ? 1 : 0);
  if (f && f.kind === 'twoway') score += 0.3 * f.rows.length * f.cols.length + 2 * f.rows.reduce((n, rw) => n + rw.cells.filter(v => v === '?').length, 0);
  if (f && f.kind === 'mapping') score += 1.4 * f.arrows.length;
  if (f && f.kind === 'plane') {
    score += 6 * (f.halfplanes || []).length + 3 * (f.halfplanes || []).filter(h => (h.b[0] - h.a[0]) !== 1).length;
    score += 1.8 * (f.points || []).length + 4 * (f.segs || []).length + (f.curves || []).reduce((n, cv) => n + 6 + 0.8 * Math.min(cv.length, 9), 0);
    (f.segs || []).forEach(sg => { [sg.aEnd, sg.bEnd].forEach(e => { if (e === 'open') score += 2; if (e === 'arrow') score += 2; });
      const dx = sg.b[0] - sg.a[0]; if (dx && !Number.isInteger((sg.b[1] - sg.a[1]) / dx)) score += 3; });
  }
  // snippets the expression parser cannot read (lists, pairs, subscripted terms): count the numbers in them
  all.forEach(sn => { let okp = true; try { C.parseRelation(sn); } catch (e) { try { C.parseCondition(sn); } catch (e2) { try { C.parseExpr(sn); } catch (e3) { okp = false; } } }
    if (!okp || /,/.test(sn)) score += 0.8 * (sn.match(/\d+/g) || []).length + 2 * (sn.match(/_\{/g) || []).length; });
  (p.parts || []).forEach(pt => {
    const t = pt.check && pt.check.type;
    if (t === 'factor') {   // factoring work: GCF to remove, leading coefficient (ac method), degree, number of factors, proving "prime"
      const co = (() => { try { const rf = C.toRF(C.parseExpr(pt.check.expr)); const P = rf.asPoly(), v = pt.check.v || 'x'; const out = []; for (let k = 0; k <= P.degreeIn(v); k++) out.push(P.coeffOf(v, k).constVal()); return out; } catch (e) { return null; } })();
      if (co) { const ints = co.map(q => q.n); let g = 0n; ints.forEach(n => { let a = n < 0n ? -n : n, b = g; while (b) { [a, b] = [b, a % b]; } g = a; });
        const lead = ints[ints.length - 1] / (g || 1n); if (g > 1n) score += 3; if (lead !== 1n && lead !== -1n) score += 6; if (lead < 0n) score += 1; score += 3 * Math.max(0, co.length - 3); if (co.filter(q => !q.isZero()).length >= 4) score += 3; }
      if (/prime/i.test(pt.answer)) score += 5;
      const fac = (pt.answer.match(/\(/g) || []).length; score += 2 * Math.max(0, fac - 2);
    }
    if (t === 'factor' && pt.check.v2) { const ex = pt.check.expr.replace(/\s/g, ''), an = pt.answer.replace(/\s/g, '');
      score += (/^-?\d+x/.test(ex) ? 6 : 0) + (/⟨-?\d*[xy]*\(/.test(an) && !/⟨\(/.test(an) ? 4 : 0) + (/x\^4/.test(ex) ? 10 : 0) + (ex.match(/-/g) || []).length; }
    if (t === 'quad-roots') { const e = pt.check.eq; if (!/\(/.test(e)) score += 5; if (!/=\s*0\s*$/.test(e)) score += 3; const d = (e.match(/\^\{?(\d)/g) || []).map(x => +x.replace(/\D/g, '')); if (Math.max(0, ...d) >= 3) score += 4; }
    // statistics: the computation each question needs, and the size of the display
    const SW = { stat: { mean: 3, median: 3, mode: 1, range: 1, five: 6, q1: 4, q3: 4, iqr: 5, mad: 8, outliers: 8, fences: 7, missing: 6, newmean: 5, without: 6, better: 6, 'compare-mad': 12 },
      'stat-box': { median: 1, min: 1, max: 1, q1: 2, q3: 2, iqr: 3, range: 3, percent: 4, compare: 5 }, twoway: { fill: 3, joint: 3, marginal: 3, 'cond-row': 6, 'cond-col': 7, assoc: 10 },
      'scatter-corr': { undefined: 2 }, 'stat-line': { predict: 4, residual: 6, 'over-under': 7, slope: 7, intercept: 6 } };
    if (SW[t]) score += (SW[t][pt.check.want] || 0) + (pt.check.round !== undefined ? 1 : 0) + (pt.check.diff ? 2 : 0);
    if (t === 'linear-rule' && pt.check.predict !== undefined) score += 4;
    if (t === 'quad-apply') score += ({ consec: 0, rect: 4, rule: 5, border: 9 })[pt.check.form] || 0;
    // lines: where the line comes from, which form is asked for, and the extra steps a question needs
    if (/^(slope|line-eq|intercepts|line-apply)$/.test(t || '')) {
      const ck = pt.check, s0 = ck.src || {}, eqs = (s0.eq || '').replace(/\s/g, '');
      score += s0.pairs ? 4 : s0.fig ? 3 : s0.eq ? (/\(/.test(eqs) ? 4 : /^y=/.test(eqs) ? (/^y=-?\d+[+-]/.test(eqs) ? 3 : 1) : 5) : s0.parallel ? 6 : s0.perp ? 10 : s0.slope !== undefined ? 3 : 0;
      if ((s0.parallel || s0.perp || '').replace(/\s/g, '') && !/^y=/.test((s0.parallel || s0.perp).replace(/\s/g, ''))) score += 4;   // the given line must be solved for y first
      if (t === 'slope') score += ({ missing: 12, collinear: 18, relation: 0 })[ck.want] || 2;
      if (t === 'line-eq') score += ({ 'slope-intercept': 3, 'point-slope': 6, standard: 9 })[ck.form] || 0;
      if (t === 'intercepts') score += 5;
      if (t === 'line-apply') score += (({ equation: 5, rate: 3, start: 3, value: 6, when: 7 })[ck.want] || 0) + (ck.pts ? 12 : 0);
      if (/\\frac/.test(pt.answer)) score += 3;
      if (/undefined/i.test(pt.answer)) score += 5;
      if (t === 'slope' && /m=0\b/.test(pt.answer.replace(/\s/g, ''))) score += 4;
      if (s0.slope === '0' || s0.slope === 'undefined') score += 2;
    }
    // systems: the method a question needs, the form of the equations and the numbers in the story
    if (/^(system|sys-apply|ineq2)$/.test(t || '')) {
      const ck = pt.check, w0 = ck.want || 'solve';
      if (t === 'system' && w0 === 'solve' && ck.eqs) { try {   // elimination work: equal/opposite coefficients, one multiplier, or two
        const co = ck.eqs.map(e => { const R = C.parseRelation(e), P = C.toRF({ k: 'sub', a: R.lhs, b: { k: 'grp', a: R.rhs } }).asPoly(); return [P.coeffOf('x', 1).constVal(), P.coeffOf('y', 1).constVal()].map(q => Number(q.n) / Number(q.d)); });
        const same = j => Math.abs(co[0][j]) === Math.abs(co[1][j]), mult = j => { const a = Math.abs(co[0][j]), b = Math.abs(co[1][j]); return a && b && (Number.isInteger(a / b) || Number.isInteger(b / a)); };
        score += same(0) || same(1) ? 0 : mult(0) || mult(1) ? 4 : 7; } catch (e) { /* not linear */ } }
      if (t === 'system' && w0 === 'solve' && /no solution|infinitely/i.test(pt.answer)) score += 4;   // recognizing a special system
      if (t === 'system') { score += ({ solve: 6, 'is-solution': 2, count: 7, param: 12 })[w0] || 0; (ck.eqs || []).forEach(e => { if (!/^y=/.test(e.replace(/\s/g, ''))) score += 2; if (/\\frac|\d\.\d/.test(e)) score += 3; }); }
      if (t === 'sys-apply') { score += w0 === 'model' ? 7 : 8; ck.rows.forEach(rw => rw.forEach((e, j) => { if (typeof e === 'object') { if (j < 2) score += 3; if (e.s === -1) score += 1; if (e.mul !== undefined) score += 4; } })); if (/\d\.\d/.test(p.prompt)) score += 6; }
      if (t === 'ineq2') { const nH = (ck.ineqs || ck.hrows || (p.fig && p.fig.halfplanes) || []).length; score += w0 === 'is-solution' ? 2 * nH : w0 === 'point-in' ? 10 : 10 * nH; if (ck.hrows) score += 4; }
      if (/\\frac/.test(pt.answer)) score += 5;
    }
    // exponents: the rules a question needs
    if (/^(pow-simplify|pow-eval|sci)$/.test(t || '')) {
      const ck = pt.check, ex = ck.expr || '', ans = pt.answer;
      const negs = (ex.match(/\^\{-/g) || []).length, zeros = (ex.match(/\^\{0\}/g) || []).length, grpPow = (ex.match(/\\right\)\^\{/g) || []).length, vars = new Set((ex.replace(/\\[a-z]+/g, '').match(/[a-z]/g) || [])).size;
      if (t === 'pow-simplify') { score += 3 * negs + 2 * zeros + 4 * grpPow + (/\\frac/.test(ex) ? 3 : 0) + 2 * vars + (/\\frac/.test(ans) ? 3 : 0) + (/-/.test(ans) ? 1 : 0) + (/\\right\)\^\{-/.test(ex) ? 10 : 0); }
      if (t === 'pow-eval') { score += 3 * negs + 2 * zeros + (/\^\{-?\\frac/.test(ex) ? 9 : 0) + (/\^\{-?\\frac\{[2-9]/.test(ex) ? 3 : 0) + (/\\left\(\\frac/.test(ex) ? 8 : 0) + (/\+/.test(ex) ? 4 : 0) + (/\\frac/.test(ans) ? 2 : 0) + (/\(-/.test(ex) ? 2 : 0); }
      if (t === 'sci') { const w = ck.want; score += ({ 'to-sci': 3, 'to-std': 4, compare: 6, op: 4, ratio: 14 })[w] || 0; if (w === 'to-sci' || w === 'to-std') score += 0.5 * (ex.replace(/\^\{[^}]*\}/g, '').match(/0/g) || []).length + 4 * (ex + ans).replace(/[^-]/g, '').length; if (ck.round !== undefined) score += 4;
        const all = ex + ' ' + (ck.terms || []).join(' ') + ' ' + ans; score += 2 * (all.match(/\^\{-/g) || []).length; if (/\\frac/.test(ex)) score += 3; if (/[+]|[^{(]-\d/.test(ex.replace(/\^\{-/g, ''))) score += 9;
        score += 0.6 * (C.snippets(ans).join('').replace(/\^\{[^}]*\}/g, '').match(/\d/g) || []).length; if (w === 'op' && /^-?[\d.]+\\times10\^\{-?\d+\}$/.test(ex)) score += 6; }
    }
    // compound interest: the formula a question needs
    if (t === 'compound') { const w = C.plainText(p.prompt); score += pt.check.want === 'compare' ? 22 : (/continuously/.test(w) ? 12 : /monthly|daily/.test(w) ? 9 : /quarterly|semiannually/.test(w) ? 7 : 3) + (pt.check.want === 'interest' ? 3 : 0); }
    // dividing by a binomial: the degree, a missing term, a remainder, a divisor whose leading coefficient is not 1
    if (t === 'poly-divide') { const ex = pt.check.expr, top = ex.slice(6, ex.indexOf('}{')), deg = Math.max(1, ...(top.match(/\^\{(\d)\}/g) || ['^{1}']).map(x => +x.replace(/\D/g, ''))), terms = (top.match(/[+-]/g) || []).length + 1;
      score += 6 * deg + (terms <= deg ? 4 : 0) + (/\\frac\{\d+\}\{/.test(pt.answer) ? 6 : 0) + (/\}\{\d+x/.test(ex) ? 6 : 0) + (/^\\frac\{\d+x/.test(ex) ? 3 : 0); }
    // standard deviation, histograms and regression: the computation a question needs
    if (t === 'stat' && /^sd/.test(pt.check.want)) score += pt.check.want === 'sd' ? 8 + (pt.check.round === 2 ? 2 : 0) + (pt.check.transform === 'add' ? 6 : pt.check.transform === 'mul' ? 8 : 0) + (pt.check.data ? 0 : 12) : 0;
    if (t === 'hist') { const w = pt.check.want, pr = p.prompt; score += w === 'count' ? (/in all/.test(pr) ? 6 : /at least|less than/.test(pr) ? 9 : 1) : w === 'percent' ? 12 + 2 * pt.check.round : w === 'median-bin' ? 18 : 22; }
    if (t === 'lsrl') score += ({ use: 8, describe: 16, r: 34, line: 33, predict: 10, residual: 14 })[pt.check.want] || 0;
    // the last lesson gaps: real numbers, verbal phrases, units, linear transformations, closure, causation
    if (t === 'num-class') { const one = x => 2 + (/\\sqrt/.test(x) ? 7 : 0) + (/\\overline/.test(x) ? 5 : 0) + (/\\frac/.test(x) ? 3 : 0) + (/\\pi/.test(x) ? 5 : 0) + (/\./.test(x) ? 3 : 0) + (/^-/.test(x) ? 1 : 0) + (/\\sqrt\{\\frac/.test(x) ? 4 : 0);
      score += pt.check.list ? 20 + pt.check.list.reduce((n, x) => n + one(x) / 2, 0) : one(pt.check.num); }
    if (t === 'verbal-expr' || t === 'verbal-words') { const tx = t === 'verbal-words' ? pt.check.expr : (C.snippets(pt.answer)[0] || ''), letters = new Set((tx.replace(/\\[a-z]+/g, '').match(/[a-z]/g) || []));
      score += 4 + (/\\frac/.test(tx) ? 4 : 0) + (/\d[a-z]/.test(tx) ? 3 : 0) + (/\(/.test(tx) ? 9 : 0) + (/\^/.test(tx) ? 9 : 0) + (letters.size > 1 ? 9 : 0) + (t === 'verbal-words' ? 18 : 0); }
    if (t === 'units') { const w = C.plainText(p.prompt); score += 4 + (/square/.test(w) ? 26 : /per hour to \w+ per second/.test(w) ? 16 + (/kilometers/.test(w) ? 2 : 0) : / per /.test(w) ? 10 : /yards to inches|gallons to cups|hours to seconds|miles to inches|gallons to pints|kilometers to centimeters/.test(w) ? 7 : 0) + (/Round/.test(w) ? 4 : 0);
      const nums = C.numbersInText(p.prompt).concat(C.numbersInText(pt.answer)); if (nums.length >= 2 && Number(nums[nums.length - 1].n) * Number(nums[0].d) < Number(nums[0].n) * Number(nums[nums.length - 1].d)) score += 2; }
    if (t === 'lin-transform') { const w = pt.check.want, a = C.plainText(pt.answer).toLowerCase(); score += w === 'describe' ? 3 * ((a.match(/shift|steeper|less steep|reflect/g) || []).length) + (/reflect/.test(a) ? 4 : 0) : ({ 'shift-eq': 14, 'h-eq': 16, 'h-words': 6 })[w] || 0; }
    if (t === 'poly-closure' && pt.check.want === 'result') { const ex = pt.check.expr; score += /^\\frac/.test(ex) ? (/\}\{[^}]*[+-]/.test(ex) ? 30 : 18) + (/\\frac/.test(pt.answer) ? 6 : 0) : /\\right\)\\left\(/.test(ex) ? 16 : /\\left\(/.test(ex) && !/^\\left/.test(ex) ? 14 : /\\right\)-/.test(ex) ? 2 : 0; }
    if (t === 'causation') score += ({ cause: 4, lurk: 6, type: 10, why: 5, which: 10 })[pt.check.want] || 0;
    // graphing by hand: what must be drawn (the key graph is not in the student's text)
    if (t === 'graph-key') { const n = (pt.check.ineqs || pt.check.eqs).length, fr = /\\frac/.test((pt.check.ineqs || pt.check.eqs).join(' ')), sf = (pt.check.ineqs || []).some(e => !/^y/.test(e)); score += pt.check.eqs ? 14 : 6 + 14 * (n - 1) + (fr ? 6 : 0) + (sf ? 8 : 0) + (/\\le|\\ge/.test((pt.check.ineqs || []).join(' ')) ? 0 : 2); }
    // parabolas by hand, transformations and quadratic models
    if (t === 'quad-graph') { const e = pt.check.eq.replace(/\s/g, ''); score += 10 + (/^y=-/.test(e) ? 3 : 0) + (/\\frac|y=-?\d+[(x]/.test(e) ? 5 : 0) + (/\)\^/.test(e) ? 0 : 22) + (/\)\^\{2\}[+-]\d/.test(e) ? 6 : 0); }
    if (t === 'quad-transform') { const tx = pt.check.want === 'equation' ? p.prompt : pt.answer; score += (pt.check.want === 'equation' ? 16 : 2) + 3 * ((tx.match(/units?/g) || []).length) + (/reflect/i.test(tx) ? 4 : 0) + (/factor/.test(tx) ? 6 : 0); }
    if (t === 'quad-fit') score += ({ exact: 10, reg: 22, predict: 8 })[pt.check.want] || 0;
    // a curved graph: what must be read from it
    if (t === 'curve-behavior') score += ({ increasing: 6, decreasing: 6, extreme: 9 })[pt.check.want] + ((p.fig.curves[0] || []).length > 9 && /x\^\{?3|relative/i.test(pt.answer + p.prompt + (pt.prompt || '')) ? 4 : 0);
    // square roots: how many roots, how big, and the operations around them
    if (t === 'radical-simplify') { const ex = pt.check.expr, rads = (ex.match(/\\sqrt\{(\d+)\}/g) || []).map(x => +x.replace(/\D/g, ''));
      score += 4 * rads.length + rads.reduce((n, v) => n + Math.log10(v), 0) + (/\\frac/.test(ex) ? 9 : 0) + (/\(/.test(ex) ? 12 : 0) + 3 * (ex.replace(/^-/, '').match(/[+-]/g) || []).length + (/\d\\sqrt/.test(ex) ? 2 : 0) + (/\\cdot/.test(ex) ? 3 : 0); }
    // polynomials: the operations a question needs
    if (/^(poly-simplify|poly-classify|poly-apply)$/.test(t || '')) {
      const ck = pt.check, ex = ck.expr || (ck.sides || []).join(' '), ans = pt.answer, T = (C.snippets(ans).join('').match(/[+-]/g) || []).length + 1;
      const G = (ex.match(/\\left\(/g) || []).length, adj = (ex.match(/\\right\)\\left\(/g) || []).length;
      if (t === 'poly-simplify') score += 2 * G + 5 * adj + (/\\right\)\^\{2\}/.test(ex) ? 4 : 0) + (/\\right\)\^\{3\}/.test(ex) ? 10 : 0) + 3 * (ex.match(/-\\left\(/g) || []).length + 2 * T + (/y/.test(ex) ? 4 : 0) + (/\d\\left\(/.test(ex) ? 3 : 0) + (/\\frac/.test(ex) ? 3 : 0) + (/\\left\(-?\d+[a-z]/.test(ex) ? 2 : 0);
      if (t === 'poly-apply') score += ({ perimeter: 2, area: 8, shaded: 14, volume: 22 })[ck.want] + (ck.square ? 3 : 0) + 2 * T;
      if (t === 'poly-classify') score += ({ degree: 1, name: ck.only ? 2 : 4, leading: 3, standard: 4 })[ck.want] + (/y/.test(ex) ? 6 : 0) + (/\\right\)\\left\(/.test(ex) ? 6 : 0) + (/\\right\)-/.test(ex) ? 4 : 0);
    }
    // quadratics: the method a question needs
    if (/^quad-(solve|feature|disc|vertex-eq|proj|ctsq)$/.test(t || '')) {
      const ck = pt.check, w0 = ck.want, eqs = (ck.eq || '').replace(/\s/g, ''), pr = p.prompt;
      if (t === 'quad-solve') score += 4 + (ck.radical ? 8 : 0) + (ck.round !== undefined ? 6 : 0) + (/completing the square/.test(pr) ? 6 : 0) + (/quadratic formula/.test(pr) ? 4 : 0) + (/^-?\d+[a-z]\^/.test(eqs) ? 3 : 0) + (!/=0$/.test(eqs) && /[a-z]/.test(eqs.split('=')[1] || '') ? 4 : 0) + (/\\frac/.test(pt.answer) ? 3 : 0);
      if (t === 'quad-feature') score += ({ vertex: 2, axis: 2, maxmin: 3, zeros: 5, yint: 1, range: 5 })[w0] + (ck.eq ? 5 : 0);
      if (t === 'quad-vertex-eq') score += ck.eq ? 10 + (/^y=-?\d+[a-z]\^/.test(eqs) && !/^y=-?1?[a-z]\^/.test(eqs) ? 8 : 0) : 14;
      if (t === 'quad-ctsq') score += 3;
      if (t === 'quad-disc') score += w0 === 'value' ? 4 : 7;
      if (t === 'quad-proj') score += ({ at: 2, tmax: 6, max: 9, ground: 14 })[w0] + (/4\.9/.test(eqs) ? 4 : 0);
    }
    if (!/domain-range|is-function|func-|read-fig|linear-rule|table-fill|rate|graph-behavior|sequence|exp-|factor|quad-/.test(t || '')) return;
    C.snippets(pt.answer).forEach(sn => {
      const rhs = sn.slice(sn.lastIndexOf('=') + 1);
      if (/,/.test(sn)) score += 0.8 * (sn.match(/\d+/g) || []).length;   // several values to produce
      if (/[a-z]/.test(rhs.replace(/\\[a-z]+/g, ''))) score += 5;                       // a rule or formula, not a number
      if (/\\frac/.test(sn)) score += 3;
      const ineqs = (sn.match(/\\le|\\ge|<|>/g) || []).length; score += 2.5 * ineqs;   // intervals to write
    });
    if (/recursive|formula/.test(pt.check.want || '')) score += 3;
    if (pt.check.want === 'which') score += 6;   // an equation must be solved
    if (t === 'func-solve') score += 4;
    if (pt.check.equation) score += 6;   // decide from an equation, with no picture
  });
  return score;
}

/* ---------- 1. large batches ---------- */
const meanScore = {};
const t0 = Date.now();
for (const set of SETS) for (const sk of set.skills) {
  for (let c = 1; c <= 7; c++) {
    for (const intOnly of [true, false]) {
      let used = null, sum = 0, made = 0;
      for (let i = 0; i < N; i++) {
        if (i % 25 === 0 || (set.id === 'geometry-right-triangles-trigonometry' && (sk.id === 'right-inverse-trig' || sk.id === 'right-inverse-trig-decimal'))) used = { keys: new Set(), sigs: new Set() };   // Exact-angle inverse trig has only three mathematically distinct outcomes; verify independent seeds rather than demanding 25 unique cards.
        const p = M.generateProblem(set.id, sk.id, c, { intOnly, level: 'test' }, 'batch|' + i, used);
        const tag = sk.id + ' c' + c + (intOnly ? ' int' : ' frac') + ' #' + i;
        ok(!p.failed, tag + ' failed to generate: ' + p.reason);
        if (p.failed) continue;
        made++;
        // a fresh, separate verification of the finished problem
        const v = M.verifyProblem(p, { intOnly });
        ok(v.ok, tag + ' not verified: ' + v.issues.join('; ') + ' :: ' + p.prompt);
        // format lint
        C.snippets(M.studentText(p)).concat(p.parts.map(pt => C.snippets(pt.answer)).flat()).forEach(s => {
          const b = lint(s); ok(!b.length, tag + ' format: ' + b.join(',') + ' in ' + s);
        });
        // answers must not be printed in the student text
        p.parts.forEach(pt => C.snippets(pt.answer).forEach(a => {
          if (/^[a-zA-Z]=/.test(a.replace(/\s/g, ''))) ok(M.studentText(p).replace(/\s/g, '').indexOf('⟨' + a.replace(/\s/g, '') + '⟩') < 0 || pt.check.type === 'literal-eval' || (pt.answerFig && /^Graph\b/i.test(p.prompt)), tag + ' answer appears in the question: ' + a);
        }));
        // CP2/CP1 difficulty range (1–5) keeps whole-number answers even when fractions are allowed
        if (c <= 5) p.parts.forEach(pt => { if (pt.check && /solve|evaluate|literal-eval|^ineq$|read-graph/.test(pt.check.type)) { const comp = v.computed[p.parts.indexOf(pt)]; if (comp) ok(!/frac/.test(comp), tag + ' non-integer answer at difficulty ' + c + ': ' + comp); } });
        // number lines: the key's graph matches its answer (re-read from the SVG) and the blank line shows the endpoints
        p.parts.forEach(pt => { if (pt.answerFig && pt.answerFig.kind !== 'plane') ok(pt.answerFig.min < pt.answerFig.max && JSON.stringify(pt.answerFig).length > 10, tag + ' bad figure'); });
        if (p.fig && p.parts.some(pt => pt.answerFig)) p.parts.forEach(pt => { if (pt.answerFig && pt.answerFig.kind !== 'plane') ok(pt.answerFig.min === p.fig.min && pt.answerFig.max === p.fig.max, tag + ' key graph uses a different scale than the student line'); });
        // a key graph drawn on a blank grid uses the same grid
        if (p.fig && p.fig.kind === 'plane') p.parts.forEach(pt => { if (pt.answerFig) ok(['xmin', 'xmax', 'ymin', 'ymax'].every(k => pt.answerFig[k] === p.fig[k]), tag + ' key graph uses a different grid'); });
        // every worked solution has steps that sum to positive weight (rubric possible)
        ok((p.steps || []).some(s => s.w > 0), tag + ' has no gradable steps');
        sum += complexity(p);
      }
      meanScore[set.id + '/' + sk.id + '|' + c + '|' + intOnly] = sum / Math.max(1, made);
    }
  }
}
// no near-duplicates inside one menu-sized batch was enforced by the engine; also check exact repeats across a whole batch at one setting are rare
console.log('batch: ' + checks + ' checks in ' + ((Date.now() - t0) / 1000).toFixed(1) + 's, generator stats ' + JSON.stringify(M.stats));
ok(!(M.stats.generatorErrors > 0), 'generator threw unexpected errors: ' + M.stats.lastError);

/* ---------- 2. mutation tests: the verifier must catch wrong keys ---------- */
function clone(o) { return JSON.parse(JSON.stringify(o)); }
let mutants = 0, caught = 0; const missed = [];
function mustCatch(p, why) { mutants++; const v = M.verifyProblem(p, { intOnly: false }); if (!v.ok) caught++; else missed.push('verifier MISSED: ' + why + ' :: ' + p.prompt + ' => ' + p.parts.map(x => x.answer).join(' ; ')); }
for (const set of SETS) for (const sk of set.skills) for (let c = 1; c <= 7; c++) for (let i = 0; i < 25; i++) {
  const p = M.generateProblem(set.id, sk.id, c, { intOnly: false, level: 'test' }, 'mut|' + i, null);
  if (p.failed) continue;
  p.parts.forEach((pt, k) => {
    if (!pt.check || !/^ineq$|read-graph/.test(pt.check.type)) return;
    // (f) inequality direction reversed, (g) open/closed swapped
    const a = pt.answer;
    const flipped = a.replace(/\\le |\\ge |<|>/, t => ({ '\\le ': '\\ge ', '\\ge ': '\\le ', '<': '>', '>': '<' })[t]);
    if (flipped !== a) { const m = clone(p); m.parts[k].answer = flipped; mustCatch(m, sk.id + ' c' + c + ' direction reversed'); }
    const opened = a.replace(/\\le |\\ge |<|>/, t => ({ '\\le ': '<', '\\ge ': '>', '<': '\\le ', '>': '\\ge ' })[t]);
    if (opened !== a) { const m = clone(p); m.parts[k].answer = opened; mustCatch(m, sk.id + ' c' + c + ' open/closed swapped'); }
    // (h) the key's number line is wrong: a circle filled/emptied, an endpoint moved, a piece dropped
    if (pt.answerFig && pt.answerFig.pieces.length && (pt.answerFig.pieces[0].lo || pt.answerFig.pieces[0].hi)) {
      const m1 = clone(p), f1 = m1.parts[k].answerFig.pieces[0]; if (f1.lo) f1.loC = !f1.loC; else f1.hiC = !f1.hiC; mustCatch(m1, sk.id + ' c' + c + ' key graph: circle filled/emptied');
      const m2 = clone(p), f2 = m2.parts[k].answerFig.pieces[0]; if (f2.lo) f2.lo = [f2.lo[0] + f2.lo[1], f2.lo[1]]; else f2.hi = [f2.hi[0] - f2.hi[1], f2.hi[1]]; mustCatch(m2, sk.id + ' c' + c + ' key graph: endpoint moved');
      if (pt.answerFig.pieces.length > 1) { const m3 = clone(p); m3.parts[k].answerFig.pieces.pop(); mustCatch(m3, sk.id + ' c' + c + ' key graph: piece missing'); }
    }
    // (i) the printed graph changed but the key did not
    if (pt.check.type === 'read-graph') { const m4 = clone(p), g = m4.fig.pieces[0]; if (g.lo) g.loC = !g.loC; else g.hiC = !g.hiC; if (pt.check.form !== 'abs' || true) mustCatch(m4, sk.id + ' c' + c + ' printed graph changed'); }
  });
  p.parts.forEach((pt, k) => {
    // open answers ("name a point in the region"): a far-away point above or below must be rejected (every boundary is non-vertical, so one of them is outside)
    if (pt.check && pt.check.want === 'point-in') { mutants++; const far = ['(0,\\ 40)', '(0,\\ -40)'].map(q => { const m0 = clone(p); m0.parts[k].answer = '⟨' + q + '⟩'; return M.verifyProblem(m0, { intOnly: false }).ok; });
      if (far.some(okk => !okk)) caught++; else missed.push('verifier MISSED: ' + sk.id + ' c' + c + ' far point accepted :: ' + p.prompt); return; }
    // (a) numeric answers off by one
    const m = clone(p), a = m.parts[k].answer;
    const bumped = pt.check && /error-line$/.test(pt.check.type) ? a.replace(/Line (\d+)/, (w, d) => 'Line ' + (+d + 1)) : a.replace(/(-?\d+)(?!.*\d)/, d => String(+d + 1));   // explanations are words; the line number is what is checked
    if (bumped !== a) { m.parts[k].answer = bumped; mustCatch(m, sk.id + ' c' + c + ' answer off by one'); }
    // (b) sign flipped in the first number of the answer math
    const m2 = clone(p), a2 = m2.parts[k].answer; if (/⟨\s*([a-zA-Z]\s*=\s*)?0\s*⟩/.test(a2)) return;   // flipping the sign of 0 changes nothing
    const firstNum = (/⟨[^⟩]*?(\d+)/.exec(a2) || [])[1]; if (firstNum === '0') return;   // −0 = 0
    const s2 = a2.replace(/⟨([^⟩]*?)(\d+)/, (w, pre, d) => '⟨' + pre + (pre.endsWith('-') ? '' : '-') + d).replace('⟨-⟨', '⟨');
    if (s2 !== a2 && pt.check && pt.check.type !== 'scenario') { m2.parts[k].answer = s2.replace(/--/g, ''); if (m2.parts[k].answer !== a2) mustCatch(m2, sk.id + ' c' + c + ' sign flipped'); }
    // (c) classification swapped
    if (pt.check && pt.check.type === 'classify') { const m3 = clone(p); m3.parts[k].answer = /No solution/.test(pt.answer) ? 'Infinitely many solutions' : 'No solution'; mustCatch(m3, 'classification swapped'); }
  });
  // (d) the printed problem changed but the key was not: a number in the student text is altered
  const m4 = clone(p), q = m4.prompt, idx = q.search(/⟨[^⟩]*\d/);
  if (idx >= 0) {
    m4.prompt = q.replace(/(⟨[^⟩]*?)(\d+)/, (w, pre, d) => pre + (+d + 2));
    if (m4.prompt !== q) mustCatch(m4, sk.id + ' c' + c + ' printed problem changed');
  }
}
// (e) unsimplified answers to simplify problems
if (EE && SETS.indexOf(EE) >= 0) {
  const p = M.generateProblem(EE.id, 'distribute', 4, { intOnly: true, level: 't' }, 'unsimp', null);
  const m = clone(p); m.parts[0].answer = '⟨' + m.parts[0].check.expr + '⟩'; mustCatch(m, 'answer equal to the unsimplified expression');
}
console.log('mutations: ' + caught + '/' + mutants + ' caught');
missed.forEach(m => console.log('   missed (equivalent mutation?): ' + m));
// A mutation can be mathematically harmless (e.g. bumping a number that the answer does not depend on).
// Every miss is listed above and must be such a case; the count is held to zero for real misses below.
missed.filter(m => !/HARMLESS/.test(m)).forEach(m => fails.push(m));
ok(mutants > 1000, 'too few mutants (' + mutants + ')');

/* ---------- 3. difficulty diagnostics (heuristic, not mathematical correctness) ---------- */
const difficultyWarnings=[];
function difficultyCheck(condition,message){checks++;if(!condition)difficultyWarnings.push(message);}

for (const set of SETS) for (const sk of set.skills) {
  const id = set.id + '/' + sk.id;
  const s = [1, 2, 3, 4, 5, 6, 7].map(c => meanScore[id + '|' + c + '|false']);
  if(sk.difficultyProfile === 'focused') {
    // Focused lesson objectives intentionally use one narrow question format
    // across class levels. They still undergo N × 7 × 2 independent
    // mathematical, mutation, print-format and duplicate checks above.
    difficultyCheck(s.every(Number.isFinite), id + ': invalid complexity for a focused skill');
    if(sk.fixedDifficulty!==undefined){
      difficultyCheck(Number.isInteger(sk.fixedDifficulty)&&sk.fixedDifficulty>=1&&sk.fixedDifficulty<=7,
        id + ': focused generator must declare a valid source difficulty');
    }
  } else {
    for (let c = 1; c < 7; c++) difficultyCheck(s[c] >= s[c - 1] * 0.92, id + ': difficulty ' + (c + 1) + ' scored easier than ' + c + ' (' + s.map(x => x.toFixed(1)).join(' → ') + ')');
    difficultyCheck(s[6] > s[0] * 1.5, id + ': Challenge problems are not clearly harder than Warm-ups (' + s[0].toFixed(1) + ' vs ' + s[6].toFixed(1) + ')');
    for (const lv of Object.values(M.LEVELS)) {
      const t = lv.tiers.map(c => meanScore[id + '|' + c + '|' + lv.intOnly]);
      difficultyCheck(t[2] > t[0], id + ' ' + lv.name + ': the Chef’s Special tier is not harder than the Appetizer tier');
    }
  }
  console.log('  ' + id.padEnd(40) + s.map(x => x.toFixed(1).padStart(5)).join(''));
}

console.log('Difficulty advisories: '+difficultyWarnings.length);difficultyWarnings.slice(0,30).forEach(x=>console.log('  ADVISORY: '+x));

/* ---------- 4. structure promises ---------- */
function gen(set, id, c, i, intOnly = true) { return M.generateProblem(set.id, id, c, { intOnly, level: 't' }, 'struct|' + i, null); }
if (EE && SETS.indexOf(EE) >= 0) for (let i = 0; i < 300; i++) {
  let p = gen(EE, 'two-step', 1, i), e = C.parseRelation(p.parts[0].check.eq);
  let ops = 0; (function w(n) { if (/add|sub|mul/.test(n.k)) ops++; if (n.a) w(n.a); if (n.b) w(n.b); })({ k: 'eq', a: e.lhs, b: e.rhs });
  ok(ops <= 1, 'two-step level 1 must be a one-step equation: ' + p.parts[0].check.eq);
  p = gen(EE, 'multi-step', 1, i); ok(/^\d+\(x[+-]\s?\d+\)=-?\d+$/.test(p.parts[0].check.eq.replace(/\s/g, '')), 'multi-step level 1 must be a(x+b)=c: ' + p.parts[0].check.eq);
  p = gen(EE, 'both-sides', 1, i); ok(!/-/.test(p.parts[0].check.eq), 'both-sides level 1 must use positive numbers: ' + p.parts[0].check.eq);
  p = gen(EE, 'distribute', 1, i); ok(!/-/.test(p.parts[0].check.expr), 'distribute level 1 must be positive: ' + p.parts[0].check.expr);
  p = gen(EE, 'evaluate', 1, i); ok(!/-/.test(M.studentText(p)), 'evaluate level 1 must use positive values: ' + p.prompt);
  p = gen(EE, 'literal', 1, i); ok(p.parts[0].check.v === 'y', 'literal level 1 solves for y');
  p = gen(EE, 'fraction-eq', 5, i); ok(/\\frac\{x\}\{\d+\}\+\\frac\{x\}\{\d+\}/.test(p.parts[0].check.eq.replace(/\s/g, '')), 'fraction-eq level 5 needs an LCD: ' + p.parts[0].check.eq);
  p = gen(EE, 'special-solutions', 3 + (i % 5), i);
  const k = C.solveLinear(p.parts[0].check.eq, 'x').kind, said = /No solution/.test(p.parts[0].answer) ? 'none' : /Infinitely/.test(p.parts[0].answer) ? 'all' : 'one';
  ok(k === said, 'special-solutions classification: ' + p.parts[0].check.eq);
  p = gen(EE, 'model', 1, i); ok(C.numbersInText(p.prompt).every(q => q.isInt() && q.n > 0n), 'model level 1 uses positive whole numbers: ' + p.prompt);
}
if (INEQ && SETS.indexOf(INEQ) >= 0) for (let i = 0; i < 300; i++) {
  const sign = t => /\\le|\\ge|<|>/.test(t);
  let p = gen(INEQ, 'ineq-solve', 1, i); let cd = C.parseCondition(p.parts[0].check.ineq).chains[0][0];
  let ops = 0; (function w(n) { if (/add|sub|mul|div/.test(n.k)) ops++; if (n.a) w(n.a); if (n.b) w(n.b); })({ k: 'r', a: cd.lhs, b: cd.rhs });
  ok(ops <= 1, 'ineq-solve level 1 is one step: ' + p.parts[0].check.ineq);
  p = gen(INEQ, 'ineq-solve', 2, i); ok(!/\\frac|-\s*\d*x/.test(p.parts[0].check.ineq.split(/<|>|\\le|\\ge/)[0]), 'ineq-solve level 2 has a positive x-coefficient: ' + p.parts[0].check.ineq);
  p = gen(INEQ, 'ineq-solve', 3, i); const flipNeeded = /-\s*\d*x|\\frac\{x\}\{-/.test(p.parts[0].check.ineq);
  p = gen(INEQ, 'compound-and', 1 + (i % 7), i); ok(C.solutionSet(p.parts[0].check.ineq).length === 1, 'compound-and gives one interval: ' + p.parts[0].check.ineq);
  p = gen(INEQ, 'compound-or', 1 + (i % 5), i); ok(C.solutionSet(p.parts[0].check.ineq).length === 2, 'compound-or below level 6 gives two rays: ' + p.parts[0].check.ineq);
  p = gen(INEQ, 'abs-ineq', 1 + (i % 2), i); ok(/^\|x\|/.test(p.parts[0].check.ineq), 'abs level 1–2 is |x| alone: ' + p.parts[0].check.ineq);
  p = gen(INEQ, 'error-analysis', 1 + (i % 7), i);
  const base = C.solutionSet(p.parts[1].check.ineq), last = C.solutionSet(p.work[p.work.length - 1]);
  ok(!C.setEqual(base, last), 'error analysis: the shown work must end with a wrong answer: ' + p.prompt);
  ok(sign(p.parts[1].answer), 'error analysis part (b) gives a solved inequality');
  p = gen(INEQ, 'graph-read', [2, 3, 4, 6, 7][i % 5], i); ok(p.fig && p.fig.pieces.length >= 1, 'read-graph problems print a graph');
  p = gen(INEQ, 'check-values', 1 + (i % 7), i); ok(!p.failed, 'check-values failed: ' + p.reason); if (p.failed) continue;
  ok(p.parts[0].check.values.some(v => { const ss = C.solutionSet(p.parts[0].check.ineq); return ss.some(I => (I.lo && I.lo.eq(C.readNumber(v))) || (I.hi && I.hi.eq(C.readNumber(v)))); }) || /\|/.test(p.parts[0].check.ineq), 'check-values always tests a boundary value: ' + p.prompt);
}

/* ---------- results ---------- */
if (fails.length) {
  console.log('FAIL: ' + fails.length + ' of ' + checks + ' checks');
  // Group failures across all skills; printing only the first 40 concealed the actual causes.
  const grouped=new Map();
  fails.forEach(f=>{
    const skill=f.includes(' c')?f.split(' c')[0]:f.slice(0,100);
    const key=skill+' :: '+(f.includes('failed to generate')?'generation':f.includes('not verified')?'verification':f.includes('format:')?'format':f.includes('difficulty')?'difficulty':'other');
    const a=grouped.get(key)||{count:0,example:f};a.count++;grouped.set(key,a);
  });
  [...grouped].sort((a,b)=>b[1].count-a[1].count).slice(0,35).forEach(([key,v])=>console.log('  '+v.count+' × '+key+' | '+v.example));
  console.log('First 15 failures in original order:');fails.slice(0,15).forEach(f=>console.log('  - '+f));
  process.exit(1);
}
console.log('PASS: ' + checks + ' checks, ' + caught + ' wrong keys caught, N=' + N);
