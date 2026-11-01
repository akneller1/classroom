/* Two-column congruence proof skills (missing reasons / statements / mixed / written / CPCTC).
   For every skill and difficulty: generate many proofs, then check from the PRINTED problem only
   (Given/Prove text, coordinates, table) with a reader written here, not the generator or verify.js:
     - every Given is true in the drawing and the Prove statement is true;
     - the completed key table is a valid proof (own justification rules and criterion classifier);
     - the figure's marks are honest (geo-cong check) and every blank has exactly one part;
   then check that verify.js rejects wrong answers (wrong criterion, SSA, wrong correspondence, unsupported
   "Given", wrong CPCTC part, swapped rows) and accepts loosely typed correct answers.
   Run: node worksheet-generator/menu/tests/geometry-proof-table-tests.cjs [count] */
'use strict';
const assert = require('node:assert');
const M = require('./load.cjs')().MKMENU;
const SET = 'geometry-triangles-congruence';
const SKILLS = ['congruence-proof-missing-reason', 'congruence-proof-reasons', 'congruence-proof-statements', 'congruence-proof-mixed', 'congruence-proof-write', 'congruence-proof-cpctc'];
const N = +(process.argv[2] || 60);
const clone = o => JSON.parse(JSON.stringify(o));
const d = (a, b) => Math.hypot(a[0] - b[0], a[1] - b[1]);
const ang = (a, v, b) => { const u = [a[0] - v[0], a[1] - v[1]], w = [b[0] - v[0], b[1] - v[1]]; return Math.acos(Math.max(-1, Math.min(1, (u[0] * w[0] + u[1] * w[1]) / (Math.hypot(...u) * Math.hypot(...w))))) * 180 / Math.PI; };
const close = (x, y, t = 1e-6) => Math.abs(x - y) < t;
const col = (a, b, c) => Math.abs((b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0])) < 1e-6 * (1 + d(a, b) * d(a, c));
function parse(t) {
  let m;
  if ((m = /^∠(\w{3}) and ∠(\w{3}) are right angles$/.exec(t))) return { t: 'right', a: m[1], b: m[2] };
  if ((m = /^△(\w{3}) ≅ △(\w{3})$/.exec(t))) return { t: 'tri', a: m[1], b: m[2] };
  if ((m = /^∠(\w{3}) ≅ ∠(\w{3})$/.exec(t))) return { t: 'ang', a: m[1], b: m[2] };
  if ((m = /^(\w{2}) ≅ (\w{2})$/.exec(t))) return { t: 'seg', a: m[1], b: m[2] };
  return null;
}
function truth(s, pt) {
  if (s.t === 'seg') return close(d(pt[s.a[0]], pt[s.a[1]]), d(pt[s.b[0]], pt[s.b[1]]));
  if (s.t === 'ang') return close(ang(pt[s.a[0]], pt[s.a[1]], pt[s.a[2]]), ang(pt[s.b[0]], pt[s.b[1]], pt[s.b[2]]), 1e-5);
  if (s.t === 'right') return close(ang(pt[s.a[0]], pt[s.a[1]], pt[s.a[2]]), 90, 1e-5) && close(ang(pt[s.b[0]], pt[s.b[1]], pt[s.b[2]]), 90, 1e-5);
  if (s.t === 'tri') { for (let i = 0; i < 3; i++) { const j = (i + 1) % 3, k = (i + 2) % 3; if (!close(d(pt[s.a[i]], pt[s.a[j]]), d(pt[s.b[i]], pt[s.b[j]])) || !close(ang(pt[s.a[j]], pt[s.a[i]], pt[s.a[k]]), ang(pt[s.b[j]], pt[s.b[i]], pt[s.b[k]]), 1e-5)) return false; } return true; }
  return false;
}
function givenTrue(t, pt) {
  let m; const s = parse(t); if (s) return truth(s, pt);
  if ((m = /^(\w)(\w) ∥ (\w)(\w)$/.exec(t))) { const u = [pt[m[2]][0] - pt[m[1]][0], pt[m[2]][1] - pt[m[1]][1]], w = [pt[m[4]][0] - pt[m[3]][0], pt[m[4]][1] - pt[m[3]][1]]; return Math.abs(u[0] * w[1] - u[1] * w[0]) < 1e-6 && !col(pt[m[1]], pt[m[2]], pt[m[3]]); }
  if ((m = /^(\w)(\w) ⊥ (\w)(\w)$/.exec(t))) { const u = [pt[m[2]][0] - pt[m[1]][0], pt[m[2]][1] - pt[m[1]][1]], w = [pt[m[4]][0] - pt[m[3]][0], pt[m[4]][1] - pt[m[3]][1]]; return Math.abs(u[0] * w[0] + u[1] * w[1]) < 1e-6; }
  if ((m = /^(\w) is the midpoint of (\w)(\w)$/.exec(t))) return d(pt[m[1]], [(pt[m[2]][0] + pt[m[3]][0]) / 2, (pt[m[2]][1] + pt[m[3]][1]) / 2]) < 1e-6;
  if ((m = /^(\w)(\w) bisects ∠(\w)(\w)(\w)$/.exec(t))) return m[1] === m[4] && close(ang(pt[m[3]], pt[m[1]], pt[m[2]]), ang(pt[m[2]], pt[m[1]], pt[m[5]]), 1e-5) && close(2 * ang(pt[m[3]], pt[m[1]], pt[m[2]]), ang(pt[m[3]], pt[m[1]], pt[m[5]]), 1e-5);
  return null;
}
function sameAngle(a, b, pt) {
  if (a[1] !== b[1]) return false;
  const V = pt[a[1]], dir = k => Math.atan2(pt[k][1] - V[1], pt[k][0] - V[0]), eq = (x, y) => Math.abs(Math.atan2(Math.sin(x - y), Math.cos(x - y))) < 1e-6;
  return (eq(dir(a[0]), dir(b[0])) && eq(dir(a[2]), dir(b[2]))) || (eq(dir(a[0]), dir(b[2])) && eq(dir(a[2]), dir(b[0])));
}
/* own justification rules: from the givens' text and coordinates */
function reasonOK(s, reason, G, pt) {
  const pg = G.map(parse);
  switch (reason) {
    case 'Given': return pg.some(g => g && g.t === s.t && ((sk(g.a) === sk(s.a) && sk(g.b) === sk(s.b)) || (sk(g.a) === sk(s.b) && sk(g.b) === sk(s.a)) || (s.t === 'ang' && ((sameAngle(g.a, s.a, pt) && sameAngle(g.b, s.b, pt)) || (sameAngle(g.a, s.b, pt) && sameAngle(g.b, s.a, pt))))));
    case 'Reflexive Property of Congruence': return s.t === 'seg' ? sk(s.a) === sk(s.b) : sameAngle(s.a, s.b, pt);
    case 'Vertical angles are congruent': return s.t === 'ang' && s.a[1] === s.b[1] && col(pt[s.a[0]], pt[s.a[1]], pt[s.b[0]]) && col(pt[s.a[2]], pt[s.a[1]], pt[s.b[2]]) && !sameAngle(s.a, s.b, pt);
    case 'Alternate interior angles are congruent':
    case 'Corresponding angles are congruent': return s.t === 'ang' && G.some(t => { const m = /^(\w)(\w) ∥ (\w)(\w)$/.exec(t); return m && ((m[1] + m[2]).includes(s.a[1]) && (m[3] + m[4]).includes(s.b[1]) || (m[1] + m[2]).includes(s.b[1]) && (m[3] + m[4]).includes(s.a[1]) || col(pt[m[1]], pt[m[2]], pt[s.a[1]]) && col(pt[m[3]], pt[m[4]], pt[s.b[1]])); });
    case 'Definition of midpoint': return s.t === 'seg' && G.some(t => { const m = /^(\w) is the midpoint of (\w)(\w)$/.exec(t); return m && s.a.includes(m[1]) && s.b.includes(m[1]) && [m[2], m[3]].every(e => (s.a + s.b).includes(e)); });
    case 'Definition of angle bisector': return s.t === 'ang' && G.some(t => { const m = /^(\w)(\w) bisects ∠(\w)(\w)(\w)$/.exec(t); return m && s.a[1] === m[1] && s.b[1] === m[1]; });
    case 'Definition of perpendicular lines': return (s.t === 'right' || s.t === 'ang') && G.some(t => / ⊥ /.test(t)) && truth({ t: 'right', a: s.a, b: s.b }, pt);
    case 'Segment Addition Postulate': return s.t === 'seg' && G.some(t => { const g = parse(t); return g && g.t === 'seg' && [...g.a, ...g.b, ...s.a, ...s.b].every(k => col(pt[g.a[0]], pt[g.a[1]], pt[k])); });
  }
  return false;
}
const sk = s => [...s].sort().join('');
function postulateOf(rows, tri, pt) {
  const A = tri.a, B = tri.b, sides = [], angles = [], rights = [];
  for (const s of rows) {
    if (s.t === 'seg') { for (const [i, j] of [[0, 1], [1, 2], [0, 2]]) { const sa = sk(A[i] + A[j]), sb = sk(B[i] + B[j]); if ((sk(s.a) === sa && sk(s.b) === sb) || (sk(s.a) === sb && sk(s.b) === sa)) sides.push([i, j]); } }
    else for (let i = 0; i < 3; i++) { const o = [0, 1, 2].filter(j => j !== i), pa = [A[o[0]], A[i], A[o[1]]], pb = [B[o[0]], B[i], B[o[1]]]; if ((sameAngle(s.a, pa, pt) && sameAngle(s.b, pb, pt)) || (sameAngle(s.a, pb, pt) && sameAngle(s.b, pa, pt))) (s.t === 'right' ? rights : angles).push(i); }
  }
  if (rights.length === 1 && sides.length === 2) return sides.filter(s => !s.includes(rights[0])).length === 1 ? 'HL' : '?';
  if (sides.length === 3) return 'SSS';
  if (sides.length === 2 && angles.length === 1) return sides[0].find(v => sides[1].includes(v)) === angles[0] ? 'SAS' : 'SSA';
  if (sides.length === 1 && angles.length === 2) return angles.every(a => sides[0].includes(a)) ? 'ASA' : 'AAS';
  return '?';
}
function keyRows(p) {
  const pr = p.fig.proof;
  if (pr.write) return p.parts[0].answer.split('; ').map(x => { const m = /^\d+\. (.*) — (.*)$/.exec(x); assert(m, 'written key row ' + x); return { s: m[1], r: m[2] }; });
  const rows = pr.rows.map(r => ({ s: r.s, r: r.r }));
  p.parts.forEach(q => { rows[q.check.row][q.check.field] = q.answer; });
  return rows;
}
function withRows(p, rows) {
  const q = clone(p);
  if (q.fig.proof.write) q.parts[0].answer = rows.map((r, i) => (i + 1) + '. ' + r.s + ' — ' + r.r).join('; ');
  else q.parts.forEach(x => { x.answer = rows[x.check.row][x.check.field]; });
  return q;
}
const verified = q => M.verifyProblem(q, { intOnly: true }).ok;
let n = 0, muts = 0, typed = 0; const tally = {};
for (const id of SKILLS) for (let c = 1; c <= 7; c++) for (let i = 0; i < N; i++) {
  const p = M.generateProblem(SET, id, c, { intOnly: c <= 5, level: c <= 3 ? 'cp2' : c <= 5 ? 'cp1' : 'honors' }, 'ptab:' + id + ':' + c + ':' + i, null);
  assert(!p.failed, id + ' c' + c + ' failed: ' + p.reason);
  n++; tally[id + ' ' + /^geo-proof-table-[a-z]+(?:-write)?-([a-z]+-[a-z0-9]+(?:-cpctc)?)/.exec(p.variant)[1]] = 1;
  const tag = id + ' c' + c + ' #' + i + ' ' + p.variant;
  assert(M.geoFigures.check(p.fig).ok, tag + ': figure marks are not honest');
  assert(/<table class="mm-proof-table/.test(M.figHtml(p.fig)), tag + ': proof table not rendered');
  const pt = p.fig.pts, m = /Given: (.+?)\. Prove: (.+?)\./.exec(p.prompt);
  assert(m, tag + ': Given/Prove not printed');
  const G = m[1].split('; ');
  G.forEach(g => assert.strictEqual(givenTrue(g, pt), true, tag + ': given not true: ' + g));
  const prove = parse(m[2]); assert(prove && truth(prove, pt), tag + ': prove false');
  // figure sanity: triangles not thin, labels distinct
  const tris = p.fig.tris; tris.forEach(t => { for (let k = 0; k < 3; k++) assert(ang(pt[t[(k + 1) % 3]], pt[t[k]], pt[t[(k + 2) % 3]]) > 20, tag + ': thin triangle'); });
  // blanks <-> parts
  const pr = p.fig.proof, labels = [];
  if (!pr.write) { pr.rows.forEach(r => { if (r.sb) labels.push(r.sb); if (r.rb) labels.push(r.rb); }); assert.strictEqual(labels.sort().join(), p.parts.map(q => q.label).sort().join(), tag + ': blanks and parts differ'); }
  if (id === 'congruence-proof-missing-reason') assert(p.parts.length === 1 && p.parts[0].check.field === 'r', tag + ': one reason blank');
  if (id === 'congruence-proof-statements') assert(p.parts.every(q => q.check.field === 's'), tag + ': statements only');
  if (id === 'congruence-proof-reasons') assert(p.parts.every(q => q.check.field === 'r'), tag + ': reasons only');
  if (id === 'congruence-proof-mixed' && !pr.write) assert(p.parts.some(q => q.check.field === 's') && p.parts.some(q => q.check.field === 'r'), tag + ': mixed blanks');
  if (id === 'congruence-proof-cpctc') assert(prove.t !== 'tri', tag + ': CPCTC proof must prove parts');
  // own re-check of the completed key table
  const rows = keyRows(p), parsed = rows.map(r => parse(r.s));
  parsed.forEach((s, k) => assert(s && truth(s, pt), tag + ': key row ' + (k + 1) + ' false: ' + rows[k].s));
  const cp = prove.t !== 'tri', nSup = rows.length - (cp ? 2 : 1);
  for (let k = 0; k < nSup; k++) assert(reasonOK(parsed[k], rows[k].r, G, pt), tag + ': reason not supported: ' + rows[k].s + ' / ' + rows[k].r);
  const tri = parsed[nSup]; assert.strictEqual(tri.t, 'tri');
  assert.strictEqual(postulateOf(parsed.slice(0, nSup), tri, pt), rows[nSup].r, tag + ': rows do not give ' + rows[nSup].r);
  if (cp) { assert.strictEqual(rows[nSup + 1].s, m[2], tag + ': last row is not the Prove statement'); assert.strictEqual(rows[nSup + 1].r, 'CPCTC'); }
  else assert.strictEqual(rows[nSup].s, m[2], tag + ': triangle row is not the Prove statement');
  assert(verified(withRows(p, rows)), tag + ': verifier rejects the key');
  // mutations the verifier must reject
  const mut = [];
  const T = rows.map(r => ({ ...r })); T[nSup].s = '△' + tri.a + ' ≅ △' + tri.b[0] + tri.b[2] + tri.b[1]; if (!truth(parse(T[nSup].s), pt)) mut.push(['correspondence', T]);
  const W = rows.map(r => ({ ...r })); W[nSup].r = ['SSS', 'SAS', 'ASA', 'AAS'].find(x => x !== rows[nSup].r && postulateOf(parsed.slice(0, nSup), tri, pt) !== x); mut.push(['criterion', W]);
  const S2 = rows.map(r => ({ ...r })); S2[nSup].r = 'SSA'; mut.push(['SSA', S2]);
  const k0 = rows.findIndex((r, k) => k < nSup && r.r !== 'Given'); if (k0 >= 0) { const U = rows.map(r => ({ ...r })); U[k0].r = 'Given'; mut.push(['unsupported Given', U]); }
  const k1 = rows.findIndex((r, k) => k < nSup && r.r === 'Given'); if (k1 >= 0) { const U = rows.map(r => ({ ...r })); U[k1].r = 'Vertical angles are congruent'; mut.push(['wrong reason for a given', U]); }
  const E = rows.map(r => ({ ...r })); E[0].s = 'AB ≅ AB'.replace(/A/g, tri.a[0]).replace(/B/g, tri.a[1]); E[0].r = 'Reflexive Property of Congruence'; mut.push(['irrelevant row', E]);
  if (cp) { const X = rows.map(r => ({ ...r })); X[nSup + 1].r = 'Given'; mut.push(['CPCTC reason', X]); const Y = rows.map(r => ({ ...r })); Y[nSup + 1].s = rows[0].s; mut.push(['CPCTC statement', Y]); }
  const Z = rows.map(r => ({ ...r })); [Z[nSup], Z[0]] = [Z[0], Z[nSup]]; mut.push(['triangle row first', Z]);
  mut.forEach(([name, R]) => {
    const q = withRows(p, R);
    // only mutations that touch a blank (or the whole written proof) are possible answers; others must still be invalid-checked
    const touches = pr.write || q.parts.some((x, j) => x.answer !== p.parts[j].answer);
    if (!touches) return;
    muts++; assert(!verified(q), tag + ': verifier accepted mutation "' + name + '"');
  });
  // loosely typed correct answers
  const loose = s => s.replace(/≅/g, ' is congruent to ').replace(/∠/g, 'angle ').replace(/△/g, 'triangle ').toLowerCase();
  const looseR = r => ({ 'Reflexive Property of Congruence': 'reflexive property', 'Vertical angles are congruent': 'vertical angles theorem', 'Alternate interior angles are congruent': 'alt. int. angles', 'Corresponding angles are congruent': 'corresponding angles postulate', 'Definition of midpoint': 'def. of midpoint', 'Definition of angle bisector': 'definition of an angle bisector', 'Definition of perpendicular lines': 'def of perpendicular', 'Segment Addition Postulate': 'segment addition', SAS: 'SAS postulate', SSS: 'side-side-side', ASA: 'ASA congruence', AAS: 'AAS theorem', HL: 'hypotenuse-leg', CPCTC: 'cpctc', Given: 'given' })[r] || r;
  const L = rows.map(r => ({ s: /right angles/.test(r.s) ? r.s : loose(r.s), r: looseR(r.r) }));
  typed++; assert(verified(withRows(p, L)), tag + ': loosely typed proof rejected ' + JSON.stringify(L));
  // a swapped congruence (CD ≅ AB) and reversed triangle order are still correct
  const F = rows.map(r => { const s = parse(r.s); return s && s.t !== 'right' && s.t !== 'tri' ? { s: r.s.split(' ≅ ').reverse().join(' ≅ '), r: r.r } : { ...r }; });
  typed++; assert(verified(withRows(p, F)), tag + ': reversed congruences rejected');
}
// a written proof in another valid order (support rows reordered) and with typed separators
for (let i = 0; i < 40; i++) {
  const p = M.generateProblem(SET, 'congruence-proof-write', 4, { intOnly: true, level: 'cp1' }, 'ord' + i, null);
  const rows = keyRows(p), nSup = rows.length - 1, sup = rows.slice(0, nSup).reverse();
  const q = clone(p); q.parts[0].answer = sup.concat(rows.slice(nSup)).map(r => r.s + ' | ' + r.r).join('\n');
  typed++; assert(verified(q), 'reordered written proof rejected: ' + q.parts[0].answer);
}
console.log('geometry proof tables: ' + n + ' proofs verified independently, ' + muts + ' wrong proofs rejected, ' + typed + ' typed variants accepted; ' + Object.keys(tally).length + ' skill/template/criterion combinations.');
