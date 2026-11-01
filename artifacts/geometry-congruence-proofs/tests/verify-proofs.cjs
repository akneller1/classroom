#!/usr/bin/env node
/* Independent checks for the triangle congruence proof generator.
 * Reads the generated sets and re-derives, from coordinates and the student-facing text only:
 *  - every Given is true in the drawing (congruence, parallel, perpendicular, midpoint, bisector);
 *  - the Prove statement is true; the named triangles are congruent in the stated vertex order;
 *  - each model row is true in the drawing and its reason is supported by a Given or by the figure;
 *  - the three support rows are corresponding parts and form the named postulate (own classifier);
 *  - every bank distractor is false or rejected, and mutated proofs are rejected by the checker;
 *  - diagrams are not degenerate (triangle angles >= 20 degrees, points well separated).
 * Usage: node verify-proofs.cjs [seeds]   (default 400 sets = 4,800 proofs) */
'use strict';
const P = require('../proofs.js');
const N = +(process.argv[2] || 400);
const errors = [];
let proofs = 0, mutations = 0, distractors = 0;
const tally = {};

const d = (a, b) => Math.hypot(a[0] - b[0], a[1] - b[1]);
const ang = (a, v, b) => { const u = [a[0] - v[0], a[1] - v[1]], w = [b[0] - v[0], b[1] - v[1]]; return Math.acos(Math.max(-1, Math.min(1, (u[0] * w[0] + u[1] * w[1]) / (Math.hypot(...u) * Math.hypot(...w))))) * 180 / Math.PI; };
const close = (x, y, t = 1e-6) => Math.abs(x - y) < t;

function parse(text) {   // own reader of the canonical statement text
  let m;
  if ((m = /^∠(\w{3}) and ∠(\w{3}) are right angles$/.exec(text))) return { t: 'right', a: m[1], b: m[2] };
  if ((m = /^△(\w{3}) ≅ △(\w{3})$/.exec(text))) return { t: 'tri', a: m[1], b: m[2] };
  if ((m = /^∠(\w{3}) ≅ ∠(\w{3})$/.exec(text))) return { t: 'ang', a: m[1], b: m[2] };
  if ((m = /^(\w{2}) ≅ (\w{2})$/.exec(text))) return { t: 'seg', a: m[1], b: m[2] };
  return null;
}
function truth(s, pt) {
  if (s.t === 'seg') return close(d(pt[s.a[0]], pt[s.a[1]]), d(pt[s.b[0]], pt[s.b[1]]));
  if (s.t === 'ang') return close(ang(pt[s.a[0]], pt[s.a[1]], pt[s.a[2]]), ang(pt[s.b[0]], pt[s.b[1]], pt[s.b[2]]), 1e-5);
  if (s.t === 'right') return close(ang(pt[s.a[0]], pt[s.a[1]], pt[s.a[2]]), 90, 1e-5) && close(ang(pt[s.b[0]], pt[s.b[1]], pt[s.b[2]]), 90, 1e-5);
  if (s.t === 'tri') {   // all three sides AND all three angles correspond
    for (let i = 0; i < 3; i++) {
      const j = (i + 1) % 3, k = (i + 2) % 3;
      if (!close(d(pt[s.a[i]], pt[s.a[j]]), d(pt[s.b[i]], pt[s.b[j]]))) return false;
      if (!close(ang(pt[s.a[j]], pt[s.a[i]], pt[s.a[k]]), ang(pt[s.b[j]], pt[s.b[i]], pt[s.b[k]]), 1e-5)) return false;
    }
    return true;
  }
  return false;
}
const collinear = (a, b, c) => Math.abs((b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0])) < 1e-6 * (1 + d(a, b) * d(a, c));
function givenTrue(g, pt) {
  let m;
  const s = parse(g.text);
  if (s) return truth(s, pt);
  if ((m = /^(\w)(\w) ∥ (\w)(\w)$/.exec(g.text))) { const u = [pt[m[2]][0] - pt[m[1]][0], pt[m[2]][1] - pt[m[1]][1]], w = [pt[m[4]][0] - pt[m[3]][0], pt[m[4]][1] - pt[m[3]][1]]; return Math.abs(u[0] * w[1] - u[1] * w[0]) < 1e-6 && !collinear(pt[m[1]], pt[m[2]], pt[m[3]]); }
  if ((m = /^(\w)(\w) ⊥ (\w)(\w)$/.exec(g.text))) { const u = [pt[m[2]][0] - pt[m[1]][0], pt[m[2]][1] - pt[m[1]][1]], w = [pt[m[4]][0] - pt[m[3]][0], pt[m[4]][1] - pt[m[3]][1]]; return Math.abs(u[0] * w[0] + u[1] * w[1]) < 1e-6; }
  if ((m = /^(\w) is the midpoint of (\w)(\w)$/.exec(g.text))) return d(pt[m[1]], [(pt[m[2]][0] + pt[m[3]][0]) / 2, (pt[m[2]][1] + pt[m[3]][1]) / 2]) < 1e-6;
  if ((m = /^(\w)(\w) bisects ∠(\w)(\w)(\w)$/.exec(g.text))) { const V = m[4], R = m[1] === V ? m[2] : m[2] === V ? m[1] : null; return !!R && close(ang(pt[m[3]], pt[V], pt[R]), ang(pt[R], pt[V], pt[m[5]]), 1e-5) && close(ang(pt[m[3]], pt[V], pt[R]) * 2, ang(pt[m[3]], pt[V], pt[m[5]]), 1e-5); }
  return null;
}
/* reason supported? (own rules, from the givens' text and the coordinates) */
function reasonOK(s, reason, proof) {
  const pt = proof.points, G = proof.givens.map(g => g.text);
  switch (reason) {
    case 'Given': return G.some(t => { const g = parse(t); return g && g.t === s.t && ((g.a === s.a && g.b === s.b) || (g.a === s.b && g.b === s.a)); });
    case 'Reflexive Property of Congruence':
      if (s.t === 'seg') return [...s.a].sort().join('') === [...s.b].sort().join('');
      return sameAngle(s.a, s.b, pt);
    case 'Vertical angles are congruent': return s.t === 'ang' && s.a[1] === s.b[1] && collinear(pt[s.a[0]], pt[s.a[1]], pt[s.b[0]]) && collinear(pt[s.a[2]], pt[s.a[1]], pt[s.b[2]]) && !sameAngle(s.a, s.b, pt);
    case 'Alternate interior angles are congruent (parallel lines)':
    case 'Corresponding angles are congruent (parallel lines)': return s.t === 'ang' && G.some(t => / ∥ /.test(t) && t.replace(/[^A-Z]/g, '').split('').some(ch => s.a.includes(ch)));
    case 'Definition of midpoint': return s.t === 'seg' && G.some(t => { const m = /^(\w) is the midpoint of (\w)(\w)$/.exec(t); return m && s.a.includes(m[1]) && s.b.includes(m[1]) && [m[2], m[3]].every(e => (s.a + s.b).includes(e)); });
    case 'Definition of angle bisector': return s.t === 'ang' && G.some(t => { const m = /^(\w)(\w) bisects ∠(\w)(\w)(\w)$/.exec(t); if (!m) return false; const V = m[4], R = m[1] === V ? m[2] : m[1]; return (m[1] === V || m[2] === V) && s.a[1] === V && s.b[1] === V && (s.a + s.b).includes(R); });
    case 'Definition of perpendicular lines': return (s.t === 'right' || s.t === 'ang') && G.some(t => / ⊥ /.test(t));
    case 'Segment Addition Postulate': return s.t === 'seg' && G.some(t => { const g = parse(t); return g && g.t === 'seg'; }) && collinear(pt[s.a[0]], pt[s.a[1]], pt[s.b[0]]) && collinear(pt[s.a[0]], pt[s.a[1]], pt[s.b[1]]);
  }
  return false;
}
function sameAngle(a, b, pt) {   // same vertex and same two rays
  if (a[1] !== b[1]) return false;
  const V = pt[a[1]], dir = k => Math.atan2(pt[k][1] - V[1], pt[k][0] - V[0]);
  const ra = [dir(a[0]), dir(a[2])], rb = [dir(b[0]), dir(b[2])];
  const eq = (x, y) => Math.abs(Math.atan2(Math.sin(x - y), Math.cos(x - y))) < 1e-6;
  return (eq(ra[0], rb[0]) && eq(ra[1], rb[1])) || (eq(ra[0], rb[1]) && eq(ra[1], rb[0]));
}
function postulateOf(rows, tri, pt) {   // own classifier using measured parts
  const A = tri.a, B = tri.b, sides = [], angles = [], rights = [];
  for (const s of rows) {
    if (s.t === 'seg') {
      for (const [i, j] of [[0, 1], [1, 2], [0, 2]]) {
        const sa = [A[i], A[j]].sort().join(''), sb = [B[i], B[j]].sort().join('');
        const x = [...s.a].sort().join(''), y = [...s.b].sort().join('');
        if ((x === sa && y === sb) || (x === sb && y === sa)) sides.push([i, j]);
      }
    } else {
      for (let i = 0; i < 3; i++) {
        const o = [0, 1, 2].filter(j => j !== i);
        const pa = [A[o[0]], A[i], A[o[1]]], pb = [B[o[0]], B[i], B[o[1]]];
        if ((sameAngle(s.a, pa, pt) && sameAngle(s.b, pb, pt)) || (sameAngle(s.a, pb, pt) && sameAngle(s.b, pa, pt))) (s.t === 'right' ? rights : angles).push(i);
      }
    }
  }
  if (rights.length === 1 && sides.length === 2) return sides.filter(s => !s.includes(rights[0])).length === 1 ? 'HL' : '?';
  if (sides.length === 3) return 'SSS';
  if (sides.length === 2 && angles.length === 1) { const sh = sides[0].find(v => sides[1].includes(v)); return sh === angles[0] ? 'SAS' : 'SSA'; }
  if (sides.length === 1 && angles.length === 2) return angles.every(a => sides[0].includes(a)) ? 'ASA' : 'AAS';
  return '?';
}

for (let seed = 1; seed <= N; seed++) {
  const set = P.makeSet(seed);
  if (set.length < 10) errors.push(`seed ${seed}: only ${set.length} proofs`);
  const stages = set.map(p => p.stage);
  if (stages.join('') !== [...stages].sort().join('')) errors.push(`seed ${seed}: stages not increasing`);
  if (!set.slice(-2).every(p => p.cpctc)) errors.push(`seed ${seed}: last two proofs are not CPCTC`);
  set.forEach(proof => {
    proofs++;
    const id = `seed ${seed} proof ${proof.n}`;
    const pt = proof.points, labels = Object.keys(pt);
    tally[proof.template + ' ' + proof.postulate + (proof.cpctc ? ' +CPCTC' : '')] = (tally[proof.template + ' ' + proof.postulate + (proof.cpctc ? ' +CPCTC' : '')] || 0) + 1;
    if (new Set(labels).size !== labels.length) errors.push(id + ': repeated labels');
    // geometry sanity
    const span = Math.max(...labels.map(a => Math.max(...labels.map(b => d(pt[a], pt[b])))));
    labels.forEach((a, i) => labels.slice(i + 1).forEach(b => { if (d(pt[a], pt[b]) < 0.12 * span) errors.push(`${id}: points ${a} and ${b} too close`); }));
    proof.triangles.forEach(t => { for (let i = 0; i < 3; i++) { const x = ang(pt[t[(i + 1) % 3]], pt[t[i]], pt[t[(i + 2) % 3]]); if (x < 20) errors.push(`${id} (${proof.template}): thin triangle angle ${x.toFixed(1)}`); } });
    // givens
    proof.givens.forEach(g => { const v = givenTrue(g, pt); if (v !== true) errors.push(`${id}: given not true or unreadable: ${g.text}`); });
    // prove statement
    const pv = parse(proof.proveText);
    if (!pv || !truth(pv, pt)) errors.push(`${id}: prove statement false: ${proof.proveText}`);
    // model rows
    const model = P.modelRows(proof);
    const parsed = model.map(r => parse(r.statement));
    const nSup = model.length - (proof.cpctc ? 2 : 1);
    parsed.forEach((s, i) => { if (!s || !truth(s, pt)) errors.push(`${id}: row ${i + 1} false: ${model[i].statement}`); });
    for (let i = 0; i < nSup; i++) if (!reasonOK(parsed[i], model[i].reason, proof)) errors.push(`${id}: reason not supported: ${model[i].statement} / ${model[i].reason}`);
    const tri = parsed[nSup];
    const post = postulateOf(parsed.slice(0, nSup), tri, pt);
    if (post !== model[nSup].reason) errors.push(`${id}: rows give ${post}, model says ${model[nSup].reason}`);
    if (proof.cpctc) {
      const last = parsed[nSup + 1];
      if (model[nSup + 1].statement !== proof.proveText) errors.push(id + ': CPCTC row is not the prove statement');
      if (postulateOf([last], tri, pt) === '?' && !isCorresponding(last, tri, pt)) errors.push(`${id}: CPCTC parts not corresponding`);
    } else if (model[nSup].statement !== proof.proveText) errors.push(id + ': triangle row is not the prove statement');
    // the shipped checker accepts the model
    if (!P.check(proof, model).ok) errors.push(id + ': checker rejects the model proof');
    // mutations the checker must reject
    const muts = [];
    const swapTri = model.map(r => ({ ...r }));
    swapTri[nSup].statement = `△${tri.a} ≅ △${tri.b[0]}${tri.b[2]}${tri.b[1]}`;
    if (!truth(parse(swapTri[nSup].statement), pt)) muts.push(['wrong correspondence', swapTri]);
    const wrongPost = model.map(r => ({ ...r }));
    wrongPost[nSup].reason = ['SSS', 'SAS', 'ASA', 'AAS'].find(x => x !== model[nSup].reason);
    muts.push(['wrong postulate', wrongPost]);
    const wrongReason = model.map(r => ({ ...r }));
    const k = model.findIndex((r, i) => i < nSup && r.reason !== 'Given');
    if (k >= 0) { wrongReason[k].reason = 'Given'; muts.push(['unsupported Given', wrongReason]); }
    const dropped = model.map(r => ({ ...r }));
    dropped[0] = { statement: '', reason: '' };
    muts.push(['missing row', dropped]);
    const ssa = model.map(r => ({ ...r }));
    ssa[nSup].reason = 'SSA';
    muts.push(['SSA', ssa]);
    if (proof.cpctc) { const c = model.map(r => ({ ...r })); c[nSup + 1].reason = 'Given'; muts.push(['CPCTC reason', c]); }
    muts.forEach(([name, rows]) => { mutations++; if (P.check(proof, rows).ok) errors.push(`${id}: checker accepted mutation "${name}"`); });
    // bank distractors are wrong wherever they go
    if (proof.stage <= 3) {
      const correctS = new Set(model.map(r => r.statement)), correctR = new Set(model.map(r => r.reason));
      proof.bank.statements.filter(s => !correctS.has(s)).forEach(s => {
        distractors++;
        const st = parse(s);
        model.forEach((r, i) => { const rows = model.map(x => ({ ...x })); rows[i].statement = s; if (P.check(proof, rows).ok) errors.push(`${id}: distractor statement accepted in row ${i + 1}: ${s}`); });
        if (st && st.t !== 'tri' && truth(st, pt)) errors.push(`${id}: distractor is a true statement: ${s}`);
      });
      proof.bank.reasons.filter(s => !correctR.has(s)).forEach(s => {
        distractors++;
        model.forEach((r, i) => { const rows = model.map(x => ({ ...x })); rows[i].reason = s; if (P.check(proof, rows).ok) errors.push(`${id}: distractor reason accepted in row ${i + 1}: ${s}`); });
      });
      if (model.some(r => proof.stage !== 2 && !proof.bank.statements.includes(r.statement))) errors.push(id + ': statement bank missing a needed statement');
      if (model.some(r => proof.stage !== 1 && !proof.bank.reasons.includes(r.reason))) errors.push(id + ': reason bank missing a needed reason');
    }
  });
}
function isCorresponding(s, tri, pt) {
  if (s.t === 'seg') return [[0, 1], [1, 2], [0, 2]].some(([i, j]) => { const a = [tri.a[i], tri.a[j]].sort().join(''), b = [tri.b[i], tri.b[j]].sort().join(''), x = [...s.a].sort().join(''), y = [...s.b].sort().join(''); return (x === a && y === b) || (x === b && y === a); });
  return [0, 1, 2].some(i => { const o = [0, 1, 2].filter(j => j !== i); const pa = [tri.a[o[0]], tri.a[i], tri.a[o[1]]], pb = [tri.b[o[0]], tri.b[i], tri.b[o[1]]]; return (sameAngle(s.a, pa, pt) && sameAngle(s.b, pb, pt)) || (sameAngle(s.a, pb, pt) && sameAngle(s.b, pa, pt)); });
}

// flexible typing accepted by the checker (spot checks on one set)
const one = P.makeSet(12345);
const loose = s => s.replace(/≅/g, ' = ').replace(/∠/g, 'angle ').replace(/△/g, 'triangle ');
one.forEach(p => {
  if (p.rows.some(r => r.st.t === 'right')) return;
  const rows = P.modelRows(p).map(r => ({ statement: loose(r.statement).toLowerCase(), reason: r.reason.toLowerCase().replace(/ \(parallel lines\)/, '') }));
  if (!P.check(p, rows).ok) errors.push(`typed variants rejected for set 12345 proof ${p.n}: ${JSON.stringify(rows)}`);
});

console.log(`Checked ${proofs} proofs (${N} sets), ${mutations} mutations, ${distractors} bank distractors.`);
console.log(Object.entries(tally).sort().map(([k, v]) => `  ${k}: ${v}`).join('\n'));
if (errors.length) { console.log(`FAIL ${errors.length} problems`); errors.slice(0, 400).forEach(e => console.log(' - ' + e)); process.exit(1); }
console.log('PASS: givens, diagrams, model proofs, postulates, CPCTC, distractors and mutations verified independently.');
