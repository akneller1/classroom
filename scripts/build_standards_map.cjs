#!/usr/bin/env node
/* Builds worksheet-generator/menu/standards-map.js: which standards each generator skill addresses.

   • Algebra 1 and Geometry skill sets: a skill gets the standards of every planner lesson that practices
     it (planner/lesson-skills*.js with cover 'full' or 'partial', standards from planner/scope-*.js).
   • Bank courses (Algebra 2, Pre-Algebra, Math 6, Precalculus, Calculus, Statistics, …): a skill gets the
     standards tagged on its approved bank questions (most common first). Each bank question also keeps
     its own tags, which the pages use for that exact question.

   Run after changing a scope, a lesson-skills map or a question bank:
     node scripts/build_standards_map.cjs            (writes the file)
     node scripts/build_standards_map.cjs --check    (fails if the file is out of date) */
'use strict';
const fs = require('fs'), path = require('path'), vm = require('vm');
const ROOT = path.resolve(__dirname, '..');
const OUT = path.join(ROOT, 'worksheet-generator/menu/standards-map.js');
const STD = require(path.join(ROOT, 'worksheet-generator/menu/standards.js'));   // shared normalizer

function load(rel) {
  const win = {}; win.window = win;
  const ctx = vm.createContext({ window: win, globalThis: win });
  vm.runInContext(fs.readFileSync(path.join(ROOT, rel), 'utf8'), ctx, { filename: rel });
  return win;
}
const map = {};
function put(set, skill, codes) {
  const s = (map[set] = map[set] || {});
  const cur = s[skill] = s[skill] || [];
  codes.forEach(c => { if (cur.indexOf(c) < 0) cur.push(c); });
}

/* ---------- Algebra 1 and Geometry: planner lessons ---------- */
const plans = [
  ['worksheet-generator/planner/scope-algebra1.js', 'MKPLAN_SCOPE', 'worksheet-generator/planner/lesson-skills.js', 'MKPLAN_SKILLS'],
  ['worksheet-generator/planner/scope-geometry.js', 'MKPLAN_SCOPE_GEOMETRY', 'worksheet-generator/planner/lesson-skills-geometry.js', 'MKPLAN_SKILLS_GEOMETRY']
];
plans.forEach(([scopeFile, scopeKey, skillFile, skillKey]) => {
  const scope = load(scopeFile)[scopeKey], skills = load(skillFile)[skillKey];
  const byLesson = {};
  scope.days.forEach(d => {
    if (!d.lesson_id || d.day_type !== 'Lesson') return;
    const codes = STD.content(STD.split(d.standards));
    if (codes.length) byLesson[d.lesson_id] = (byLesson[d.lesson_id] || []).concat(codes);
  });
  /* A skill used by several lessons collects their standards; rank them by how strongly the lessons use
     the skill (full coverage, wide difficulty range) and keep the top MAX so the key stays specific. */
  const weights = {};
  Object.keys(skills.lessons).sort((a, b) => a.localeCompare(b, 'en', { numeric: true })).forEach(id => {
    const L = skills.lessons[id];
    if (!L || L.cover === 'none' || !byLesson[id]) return;
    (L.skills || []).forEach(s => {
      const set = skills.SETS[s[0]]; if (!set) return;
      const span = (s[3] || 7) - (s[2] || 1) + 1, w = (L.cover === 'full' ? 2 : 1) + (span >= 4 ? 1 : 0);
      const k = set + '|' + s[1], W = weights[k] = weights[k] || { set, skill: s[1], codes: {}, order: [] };
      byLesson[id].forEach(c => { if (!(c in W.codes)) { W.codes[c] = 0; W.order.push(c); } W.codes[c] += w; });
    });
  });
  const MAX = 4;
  Object.values(weights).forEach(W => {
    const ranked = W.order.slice().sort((a, b) => W.codes[b] - W.codes[a] || W.order.indexOf(a) - W.order.indexOf(b));
    put(W.set, W.skill, ranked.slice(0, MAX));
  });
});

/* ---------- skills no planner lesson maps (checked by hand against the CCSS-M) ---------- */
const MANUAL = {
  'algebra1-foundations': { percent: ['7.RP.A.3', 'N-Q.A.1'], 'expr-error': ['A-SSE.A.2', 'A-SSE.A.1a'] },
  'algebra1-expressions-equations': { 'eq-error': ['A-REI.A.1', 'A-REI.B.3'], 'expr-error': ['A-SSE.A.2', 'A-SSE.A.1a'], 'solve-equations-variables-both-sides': ['A-REI.B.3', 'A-REI.A.1'] },
  'algebra1-inequalities': { 'error-analysis': ['A-REI.A.1', 'A-REI.B.3'], 'graph-number-line': ['A-REI.B.3'] },
  'algebra1-relations-functions': { 'table-fill': ['F-IF.A.2'], 'arithmetic-explicit': ['F-BF.A.2', 'F-LE.A.2'], 'arithmetic-nth': ['F-IF.A.3', 'F-BF.A.2'], 'discrete-continuous': ['F-IF.B.5'] },
  'algebra1-exponential-functions': { 'exponential-graph-features': ['F-IF.C.7e', 'F-IF.B.4', 'F-IF.B.5'], 'exp-graph-hand': ['F-IF.C.7e'] },
  'algebra1-factoring-zero-product': { 'factor-by-grouping': ['A-SSE.A.2'] },
  'algebra1-statistics-data-modeling': { stdev: ['S-ID.A.2'], 'statistics-mean': ['S-ID.A.2', '6.SP.B.5c'], 'statistics-median': ['S-ID.A.2', '6.SP.B.5c'], 'statistics-mode': ['S-ID.A.2'] },
  'algebra1-linear-equations-slope': { 'direct-variation': ['A-CED.A.2', 'F-LE.A.2'], 'graph-slope-intercept': ['F-IF.C.7a', 'A-CED.A.2'], 'graph-from-points': ['F-IF.C.7a', 'A-CED.A.2'], 'graph-special-lines': ['A-CED.A.2'], 'graph-standard-form': ['A-CED.A.2', 'A-CED.A.4'] },
  'algebra1-systems-of-equations': { 'graph-coordinate-inequality': ['A-REI.D.12'], 'graph-dashed-inequality': ['A-REI.D.12'], 'graph-two-lines': ['A-REI.C.6', 'A-REI.D.11'] },
  'algebra1-exponents-scientific-notation': { 'simplify-radicals': ['N-RN.A.2'], 'rational-exponents': ['N-RN.A.1', 'N-RN.A.2'] },
  'algebra1-polynomials': { 'multiply-monomials-polynomials': ['A-APR.A.1'], 'multiply-binomials': ['A-APR.A.1'] },
  'algebra1-quadratics': { 'q-fit': ['S-ID.B.6a', 'A-CED.A.2'], 'quadratic-graphing': ['F-IF.C.7a'], 'quadratic-solve-factoring': ['A-REI.B.4b', 'A-SSE.B.3a'] },
  'geometry-basics-reasoning': { 'basics-investigation-segment': ['G-CO.A.1', 'A-CED.A.1'], 'basics-investigation-angle': ['G-CO.A.1', 'A-CED.A.1'], 'basics-investigation-coordinate': ['G-GPE.B.7', 'G-GPE.B.4'], 'basics-investigation-lines': ['G-CO.C.9', 'A-CED.A.1'] },
  'geometry-angles-parallel-lines': { 'angles-investigation-corresponding': ['G-CO.C.9', 'A-CED.A.1'], 'angles-investigation-alternate': ['G-CO.C.9', 'A-CED.A.1'], 'angles-investigation-relations': ['G-CO.C.9', 'A-CED.A.1'], 'angles-open-response-investigation': ['G-CO.C.9', 'A-CED.A.1'] },
  'geometry-triangle-relationships': { 'triangle-concurrency-name': ['G-C.A.3', 'G-CO.C.10'], 'triangle-circumcenter-incenter': ['G-C.A.3', 'G-CO.C.10'], 'triangle-investigation-midsegment': ['G-CO.C.10', 'A-CED.A.1'], 'triangle-investigation-exterior': ['G-CO.C.10', 'A-CED.A.1'], 'triangle-investigation-coordinate': ['G-CO.C.10', 'G-GPE.B.4'], 'triangle-investigation-bisector': ['G-CO.C.9', 'A-CED.A.1'] },
  'geometry-triangles-congruence': { 'congruence-rigid-motions': ['G-CO.B.7', 'G-CO.B.6'], 'congruence-investigation-algebra': ['G-CO.B.7', 'G-SRT.B.5'], 'congruence-investigation-isosceles': ['G-CO.C.10', 'G-SRT.B.5'], 'congruence-investigation-coordinate': ['G-CO.B.7', 'G-GPE.B.4'], 'congruence-investigation-overlap': ['G-SRT.B.5', 'G-CO.C.9'], 'congruence-investigation-kite': ['G-CO.B.8', 'G-SRT.B.5'], 'congruence-investigation-hl': ['G-CO.B.8', 'G-SRT.B.5'] },
  'geometry-quadrilaterals-polygons': { 'kite-isosceles-trapezoid': ['G-CO.C.11', 'G-SRT.B.5'], 'polygon-open-response-investigation': ['G-CO.C.11', 'G-CO.A.3'] },
  'geometry-similarity': { 'similarity-area-volume-ratio': ['G-SRT.A.2', 'G-GMD.A.3'], 'similarity-area-investigation': ['G-SRT.A.2', 'G-SRT.B.5'], 'similarity-investigation-ratio': ['G-SRT.A.2', 'G-SRT.B.5'], 'similarity-investigation-parallel': ['G-SRT.B.4', 'G-SRT.B.5'], 'similarity-investigation-dilation': ['G-SRT.A.1', 'G-SRT.A.2'], 'similarity-investigation-altitude': ['G-SRT.B.4', 'G-SRT.B.5'] },
  'geometry-right-triangles-trigonometry': { 'law-of-sines': ['G-SRT.D.10', 'G-SRT.D.11'], 'law-of-cosines': ['G-SRT.D.10', 'G-SRT.D.11'], 'right-investigation-pyth': ['G-SRT.C.8', 'G-SRT.B.4'], 'right-investigation-special': ['G-SRT.C.6', 'G-SRT.C.8'], 'right-investigation-converse': ['G-SRT.B.4', 'G-SRT.C.8'], 'right-investigation-coordinate': ['G-GPE.B.4', 'G-GPE.B.7'], 'right-trig-investigation': ['G-SRT.C.8', 'G-SRT.C.6'] },
  'geometry-transformations': { 'transformations-investigation-mirror': ['G-CO.A.5', 'G-CO.A.4'], 'transformations-investigation-center': ['G-SRT.A.1'], 'transformations-investigation-backward': ['G-CO.A.5', 'G-CO.B.6'], 'transformations-investigation-symmetry': ['G-CO.A.3'], 'transformations-open-response-investigation': ['G-CO.A.5', 'G-CO.B.6'] },
  'geometry-circles': { 'circles-investigation-angles': ['G-C.A.2'], 'circles-investigation-power': ['G-C.A.2'], 'circles-investigation-coordinate': ['G-GPE.A.1'], 'circles-investigation-sector': ['G-C.B.5'], 'circle-open-response-investigation': ['G-C.A.2', 'G-C.B.5'] },
  'geometry-area-surface-area-volume': { 'measure-pyramid-surface': ['G-MG.A.1', 'G-GMD.A.3'], 'measure-cone-surface': ['G-MG.A.1', 'G-GMD.A.3'], 'measure-composite-round': ['G-GMD.A.3', 'G-MG.A.1'], 'measure-unit-conversion': ['N-Q.A.1', 'G-MG.A.2'], 'measure-similar-solids': ['G-GMD.A.3', 'G-MG.A.1'], 'measure-rotate-solid': ['G-GMD.B.4', 'G-GMD.A.3'], 'measure-cross-section': ['G-GMD.B.4'], 'measure-investigation-prism': ['G-GMD.A.3', 'G-MG.A.3'], 'measure-investigation-cylinder': ['G-GMD.A.3'], 'measure-investigation-sphere': ['G-GMD.A.3'], 'measure-investigation-trapezoid': ['G-GMD.A.1', 'G-MG.A.3'], 'solids-open-response-investigation': ['G-GMD.A.3', 'G-MG.A.3'] }
};
/* Algebra 1 Unit 2 reuses the Unit 1 skills (same ids, same generators). */
const SHARED = { 'algebra1-expressions-equations': 'algebra1-foundations' };
Object.keys(MANUAL).forEach(set => Object.keys(MANUAL[set]).forEach(skill => {
  if (!(map[set] && map[set][skill])) put(set, skill, MANUAL[set][skill].map(STD.norm));
}));
Object.keys(SHARED).forEach(set => Object.keys(map[SHARED[set]] || {}).forEach(skill => {
  if (!(map[set] && map[set][skill])) put(set, skill, map[SHARED[set]][skill]);
}));
/* The multi-part Open Response scenario (mcas-context) draws on the whole unit: list the unit's most-used standards. */
Object.keys(map).filter(set => /^(algebra1|geometry)-/.test(set)).forEach(set => {
  const n = {};
  Object.keys(map[set]).forEach(k => map[set][k].forEach((c, i) => { n[c] = (n[c] || 0) + (i === 0 ? 2 : 1); }));
  const top = Object.keys(n).sort((a, b) => n[b] - n[a] || a.localeCompare(b, 'en', { numeric: true })).slice(0, 3);
  if (top.length && !map[set]['mcas-context']) put(set, 'mcas-context', top);
});

/* ---------- bank courses: tags on the approved questions ---------- */
const manifest = JSON.parse(fs.readFileSync(path.join(ROOT, 'question-banks/manifest.json'), 'utf8'));
(manifest.banks || []).forEach(b => {
  const file = path.join(ROOT, b.path);
  if (!fs.existsSync(file)) return;
  const bank = JSON.parse(fs.readFileSync(file, 'utf8'));
  const set = (b.courseId === 'algebra' ? 'algebra1' : b.courseId) + '-' + b.unitId;
  const counts = {};
  (bank.questions || []).forEach(q => {
    if (!q.skillId) return;
    const c = counts[q.skillId] = counts[q.skillId] || {};
    STD.split(q.standards).forEach(code => { c[code] = (c[code] || 0) + 1; });
  });
  Object.keys(counts).sort().forEach(skill => {
    const c = counts[skill];
    const all = Object.keys(c).sort((x, y) => c[y] - c[x] || x.localeCompare(y, 'en', { numeric: true }));
    const codes = STD.content(all).length ? STD.content(all) : all;   // practice-only tags (e.g. MP.1) when that is all there is
    if (codes.length) put(set, skill, codes);
  });
});

const sorted = {};
Object.keys(map).sort().forEach(set => { sorted[set] = {}; Object.keys(map[set]).sort().forEach(k => { sorted[set][k] = map[set][k]; }); });
const body = '/* Generated by scripts/build_standards_map.cjs. Do not edit by hand.\n   Skill-set id → skill id → standards the skill addresses (most relevant first). */\n' +
  '(function (G) { (G.MKSTD_SKILLS = G.MKSTD_SKILLS || {}); var M = ' + JSON.stringify(sorted) + ';\n' +
  '  Object.keys(M).forEach(function (k) { G.MKSTD_SKILLS[k] = M[k]; });\n})(typeof window !== \'undefined\' ? window : globalThis);\n';

const unknown = new Set();
Object.values(sorted).forEach(s => Object.values(s).forEach(list => list.forEach(c => { if (!STD.describe(c)) unknown.add(c); })));
if (process.argv.includes('--check')) {
  const cur = fs.existsSync(OUT) ? fs.readFileSync(OUT, 'utf8') : '';
  if (cur !== body) { console.error('standards-map.js is out of date: run node scripts/build_standards_map.cjs'); process.exit(1); }
} else fs.writeFileSync(OUT, body);
const n = Object.values(sorted).reduce((a, s) => a + Object.keys(s).length, 0);
console.log('standards-map.js: ' + Object.keys(sorted).length + ' skill sets, ' + n + ' skills' + (unknown.size ? '; no description for: ' + [...unknown].join(', ') : '; every standard has a description'));
