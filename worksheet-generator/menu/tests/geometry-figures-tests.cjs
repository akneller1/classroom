/* Procedural Geometry figures: every generated figure is internally consistent, agrees with the answer key,
   renders to clean print-safe SVG, and deliberately wrong figures are refused.
   Run: node worksheet-generator/menu/tests/geometry-figures-tests.cjs */
'use strict';
const assert = require('node:assert/strict');
const env = require('./load.cjs')(), NS = env.MKMENU, F = NS.geoFigures, C = NS.check;
assert.ok(F, 'geometry-figures.js loaded');

// ---- negative cases: wrong figures are refused, never drawn
assert.equal(F.check({ kind: 'geo-quad', shape: 'parallelogram', ticks: [{ segs: ['AB', 'BC'], n: 1 }] }).ok, false, 'unequal sides cannot share a tick');
assert.equal(F.check({ kind: 'geo-quad', shape: 'parallelogram', diagonals: true, right: [['E', 'A', 'B']] }).ok, false, 'parallelogram diagonals are not perpendicular');
assert.equal(F.check({ kind: 'geo-quad', shape: 'rhombus', diagonals: true, right: [['E', 'A', 'B']] }).ok, true);
assert.equal(F.check({ kind: 'geo-quad', shape: 'trapezoid', parallel: [['AD', 'BC']] }).ok, false, 'trapezoid legs are not parallel');
assert.equal(F.check({ kind: 'geo-quad', shape: 'general', angles: [100, 100, 100, 100] }).ok, false, 'angles must sum to 360');
assert.equal(F.check({ kind: 'geo-transversal', marks: [{ pos: 2, text: 'a', deg: 70 }, { pos: 6, text: 'b', deg: 110 }] }).ok, false, 'corresponding angles cannot differ');
assert.equal(F.check({ kind: 'geo-transversal', marks: [{ pos: 3, text: 'a', deg: 70 }, { pos: 5, text: 'b', deg: 110 }] }).ok, true, 'same-side interior sum to 180');
assert.equal(F.check({ kind: 'geo-adjacent', relation: 'complement', parts: [{ text: 'a', deg: 40 }, { text: 'b', deg: 40 }] }).ok, false);
assert.equal(F.check({ kind: 'geo-cross', marks: [{ pos: 1, text: 'a', deg: 120 }, { pos: 3, text: 'b', deg: 60 }] }).ok, false);
assert.equal(F.render({ kind: 'geo-cross', marks: [{ pos: 1, text: 'a', deg: 120 }, { pos: 3, text: 'b', deg: 60 }] }), '', 'invalid figure renders nothing');
assert.equal(F.check({ kind: 'geo-plane', shape: 'triangle', v: { b: 6 } }).ok, false, 'missing height');
assert.equal(F.check({ kind: 'geo-plane', shape: 'rectangle', v: { w: -2, l: 5 } }).ok, false, 'negative side');
assert.equal(F.check({ kind: 'geo-solid', solid: 'cylinder', v: { r: 3, h: 5 }, lab: { r: '4 cm' } }).ok, false, 'override label may not contain a number');
assert.equal(F.check({ kind: 'geo-solid', solid: 'cone', v: { r: 3, h: 5 }, lab: { h: 'h' } }).ok, true);
assert.equal(F.check({ kind: 'geo-solid', solid: 'sphere', v: { r: 3, h: 9 }, show: ['h'] }).ok, false, 'a sphere has no height to show');
assert.ok(/<svg/.test(F.render({ kind: 'geo-solid', solid: 'prism', v: { l: 4, w: 3, h: 2 }, unit: 'cm' })), 'a valid solid renders');
// a figure that prints a number the question never states must fail verification
{ const M2 = NS; const bad = { variant: 'x', prompt: 'A rectangle has width 4 cm and length 9 cm.', parts: [{ answer: '36', check: { type: 'solve', eq: 'x=4*9', v: 'x' } }], fig: { kind: 'geo-plane', shape: 'rectangle', v: { w: 4, l: 7 }, unit: 'cm' } };
  const r = M2.verifyProblem(bad); assert.notEqual(r.status, 'verified', 'figure shows 7 but the question says 9'); }
assert.equal(F.check({ kind: 'geo-grid', shapes: [{ id: 'pre', pts: [[1, 2], [3, 1], [2, 4]] }, { id: 'img', of: 'pre', tx: { type: 'reflect-y' }, pts: [[-1, 2], [-3, 1], [-2, 4]] }] }).ok, true, 'correct image');
assert.equal(F.check({ kind: 'geo-grid', shapes: [{ id: 'pre', pts: [[1, 2], [3, 1], [2, 4]] }, { id: 'img', of: 'pre', tx: { type: 'reflect-y' }, pts: [[-1, 2], [-3, 1], [2, -4]] }] }).ok, false, 'one image vertex is wrong');
assert.equal(F.check({ kind: 'geo-grid', shapes: [{ id: 'pre', pts: [[1, 2]] }, { id: 'img', of: 'pre', tx: { type: 'translate', dx: 2, dy: -1 }, pts: [[3, 1]] }] }).ok, true);
assert.equal(F.check({ kind: 'geo-grid', shapes: [{ id: 'pre', pts: [[1, 2]] }, { id: 'img', of: 'pre', tx: { type: 'rotate-cw' }, pts: [[-2, 1]] }] }).ok, false, 'clockwise maps (1,2) to (2,-1)');
assert.equal(F.check({ kind: 'geo-grid', shapes: [{ id: 'pre', pts: [[40, 2]] }] }).ok, false, 'point off the grid');
assert.equal(F.check({ kind: 'geo-grid', shapes: [{ id: 'a', pts: [[1, 1]] }], lines: [{ x: 1, y: 2 }] }).ok, false, 'a mirror line is x=c or y=c');
assert.equal(F.check({ kind: 'geo-rt', v: { a: 5, b: 12 }, show: ['a', 'b', 'c'] }).ok, true, '5-12-13');
assert.equal(F.check({ kind: 'geo-rt', v: { a: 5, b: 12 }, lab: { c: '14' } }).ok, false, 'hypotenuse label 14 contradicts the legs');
assert.equal(F.check({ kind: 'geo-rt', v: { a: 4, b: 5 }, show: ['c'] }).ok, false, 'hypotenuse is irrational: must be labelled');
assert.equal(F.check({ kind: 'geo-rt', v: { a: 4, b: 5 }, lab: { c: 'x' } }).ok, true);
assert.equal(F.check({ kind: 'geo-rt', v: { a: 1, b: 1 }, ang: { B: 30 } }).ok, false, 'a 45-degree angle labelled 30');
assert.equal(F.check({ kind: 'geo-rt', v: { a: Math.sqrt(3), b: 1 }, ang: { B: 30, A: 60 } }).ok, true);
assert.equal(F.check({ kind: 'geo-rt', v: { a: 3, b: 4 }, lab: { b: '2 x' } }).ok, false, 'number mixed with text');
{ const bad = { variant: 'x', prompt: 'A right triangle has legs 5 and 12 units. Find the hypotenuse x.', parts: [{ answer: '13', check: { type: 'geo-pythagorean', kind: 'hyp', eq: 'x^2=5^2+12^2' } }], fig: { kind: 'geo-rt', v: { a: 5, b: 12 }, show: ['a', 'b'], lab: { c: 'x' } } };
  assert.notEqual(NS.verifyProblem(Object.assign({}, bad, { fig: Object.assign({}, bad.fig, { v: { a: 5, b: 13 } }) })).status, 'verified', 'figure shows 13 but the question says 12'); }
assert.equal(F.check({ kind: 'geo-sim', sides: [6, 8, 10], k: 2, show: ['AB', 'BC', 'DE'], lab: { EF: 'x' } }).ok, true, 'similar pair');
assert.equal(F.check({ kind: 'geo-sim', sides: [6, 8, 10], k: 2, lab: { DE: '13' } }).ok, false, 'DE must be 12');
assert.equal(F.check({ kind: 'geo-sim', sides: [3, 4, 9], k: 2 }).ok, false, 'triangle inequality');
assert.equal(F.check({ kind: 'geo-sim', angles: [40, 60, 80], k: 2, ang: { A: 40, F: 80 } }).ok, true);
assert.equal(F.check({ kind: 'geo-sim', angles: [40, 60, 80], k: 2, ang: { F: 70 } }).ok, false, 'angle F is 80');
assert.equal(F.check({ kind: 'geo-sim', angles: [40, 60, 80], k: 2, show: ['AB'] }).ok, false, 'no side lengths from angles alone');
assert.equal(F.check({ kind: 'geo-tri-par', v: { AD: 3, DB: 2, AE: 6, EC: 4 }, angA: 60 }).ok, true, 'AD/DB = AE/EC');
assert.equal(F.check({ kind: 'geo-tri-par', v: { AD: 3, DB: 2, AE: 6, EC: 5 }, angA: 60 }).ok, false, 'DE would not be parallel to BC');
assert.equal(F.check({ kind: 'geo-tri-par', v: { AD: 3, DB: 2, AE: 6, EC: 4 }, angA: 60, lab: { DE: '99' } }).ok, false, 'DE label must match the drawn length');
assert.equal(F.check({ kind: 'geo-circle', pts: { A: [1, 1] }, onCircle: ['A'] }).ok, false, 'point off the circle');
assert.equal(F.check({ kind: 'geo-circle', pts: { P: [1, 0], O2: [0.5, 0.5], T: [1, 1] }, right: [['P', 'O', 'T']] }).ok, true, 'radius to (1,0) is perpendicular to the vertical tangent');
assert.equal(F.check({ kind: 'geo-circle', pts: { P: [1, 0], T: [1.5, 1] }, right: [['P', 'O', 'T']] }).ok, false, 'tangent mark on a slanted segment');

// ---- relationship table
assert.equal(F.relationship(2, 6), 'corresponding');
assert.equal(F.relationship(3, 6), 'alternate-interior');
assert.equal(F.relationship(1, 8), 'alternate-exterior');
assert.equal(F.relationship(4, 6), 'same-side-interior');

// ---- tampering a generated transversal figure must make the verifier reject the item
{
  const set = NS.skillSets['geometry-angles-parallel-lines'];
  const p = NS.generateProblem(set.id, 'alternate-interior', 6, { intOnly: true, level: 'test' }, 'tamper', { keys: new Set(), sigs: new Set() });
  assert.equal(p.verify.status, 'verified');
  const bad = JSON.parse(JSON.stringify(p));
  bad.fig.marks[1].pos = 5; bad.fig.marks[0].pos = 3;           // now a same-side pair: the equation must be supplementary
  assert.notEqual(NS.verifyProblem(bad, { intOnly: true, level: 'test' }).status, 'verified', 'figure that contradicts the equation is rejected');
}

// ---- every generated figure in every Geometry unit
const dirty = /NaN|undefined|Infinity|null/;
let checked = 0; const kinds = {};
for (const set of Object.values(NS.skillSets).filter(s => s.id.startsWith('geometry-'))) {
  for (const sk of set.skills) for (const c of [1, 3, 5, 7]) for (let i = 0; i < 12; i++) {
    const p = NS.generateProblem(set.id, sk.id, c, { intOnly: true, level: 'test' }, 'figs:' + sk.id + c + i, { keys: new Set(), sigs: new Set() });
    assert.equal(p.failed, undefined, set.id + '/' + sk.id + ': ' + p.reason);
    assert.equal(p.verify.status, 'verified', set.id + '/' + sk.id + ' ' + JSON.stringify(p.verify.issues));
    if (!p.fig || !F.owns(p.fig)) continue;
    checked++; kinds[p.fig.kind] = (kinds[p.fig.kind] || 0) + 1;
    assert.equal(F.check(p.fig).ok, true, sk.id + ' figure invalid');
    const html = NS.figHtml(p.fig);
    assert.match(html, /<svg[\s\S]*<\/svg>/, sk.id + ' did not render');
    assert.ok(!dirty.test(html), sk.id + ' svg has NaN/undefined: ' + (html.match(dirty) || [])[0]);
    assert.ok(!/#[0-9a-f]{3,6}/i.test(html.replace(/#111|#555|#bbb|#fff(?![0-9a-f])/gi, '')), sk.id + ' uses non-print-safe colours');
    // transversal / adjacent / cross: the labelled expression equals the true angle at the solved x
    const marks = Array.isArray(p.fig.marks) && p.fig.marks.length && typeof p.fig.marks[0] === 'object' ? p.fig.marks : p.fig.parts;
    if (marks && p.parts[0].check && p.parts[0].check.type === 'solve') {
      const sol = C.solveLinear(p.parts[0].check.eq, p.parts[0].check.v || 'x');
      const x = Number(sol.value.n) / Number(sol.value.d);
      for (const m of marks) {
        const mm = /^\(?(\d*)x(?:\+(\d+))?\)?°$/.exec(m.text);
        if (mm) assert.equal((mm[1] === '' ? 1 : Number(mm[1])) * x + Number(mm[2] || 0), m.deg, sk.id + ' label "' + m.text + '" does not equal its drawn angle ' + m.deg + ' at x=' + x);
        else { const nm = /^(\d+)°$/.exec(m.text); if (nm) assert.equal(Number(nm[1]), m.deg, sk.id + ' numeric label differs from its angle'); }
      }
    }
    // general quadrilateral: the drawn interior angles really are the labelled ones
    if (p.fig.shape === 'general') assert.equal(p.fig.angles.reduce((a, b) => a + b, 0), 360);
  }
}
assert.ok(checked > 800, 'expected many figures, got ' + checked);
console.log('Geometry figures: ' + checked + ' generated figures consistent with their answers (' + JSON.stringify(kinds) + '); wrong figures refused.');
