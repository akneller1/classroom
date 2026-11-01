/* Triangle congruence proofs: generator and flexible checker.
 * Every diagram is built from exact construction rules (reflection, point symmetry,
 * parallelogram, isosceles, shared angle, translation), so the triangles in each proof
 * really are congruent and every given is true of the picture.
 * The checker reads what a student wrote, works out what each statement means in the
 * drawn figure, and decides whether the rows prove the claim (SSS, SAS, ASA, AAS, HL, CPCTC).
 * Usable in the browser (window.MK_PROOFS) and in Node (module.exports). */
(function (root) {
  'use strict';

  /* ------------------------------------------------------------ random numbers */
  function rng(seed) {
    var s = (seed >>> 0) || 1;
    function next() { s = (s + 0x6D2B79F5) >>> 0; var t = s; t = Math.imul(t ^ (t >>> 15), t | 1); t ^= t + Math.imul(t ^ (t >>> 7), t | 61); return ((t ^ (t >>> 14)) >>> 0) / 4294967296; }
    return {
      next: next,
      range: function (a, b) { return a + (b - a) * next(); },
      int: function (a, b) { return a + Math.floor(next() * (b - a + 1)); },
      pick: function (arr) { return arr[Math.floor(next() * arr.length)]; },
      shuffle: function (arr) { var a = arr.slice(); for (var i = a.length - 1; i > 0; i--) { var j = Math.floor(next() * (i + 1)); var t = a[i]; a[i] = a[j]; a[j] = t; } return a; }
    };
  }

  /* ------------------------------------------------------------ vocabulary */
  var REASONS = {
    given: 'Given',
    reflexive: 'Reflexive Property of Congruence',
    vertical: 'Vertical angles are congruent',
    altint: 'Alternate interior angles are congruent (parallel lines)',
    corresp: 'Corresponding angles are congruent (parallel lines)',
    midpoint: 'Definition of midpoint',
    bisector: 'Definition of angle bisector',
    perp: 'Definition of perpendicular lines',
    rightcong: 'All right angles are congruent',
    segadd: 'Segment Addition Postulate',
    SSS: 'SSS', SAS: 'SAS', ASA: 'ASA', AAS: 'AAS', HL: 'HL',
    SSA: 'SSA', AAA: 'AAA',
    cpctc: 'CPCTC'
  };
  var POSTULATES = ['SSS', 'SAS', 'ASA', 'AAS', 'HL'];

  /* typed reason -> key (order matters: CPCTC before "corresponding") */
  function reasonKey(text) {
    var t = String(text || '').toLowerCase().replace(/[.’']/g, '').replace(/\s+/g, ' ').trim();
    if (!t) return null;
    if (/cpctc|corresponding parts/.test(t)) return 'cpctc';
    var compact = t.replace(/[^a-z]/g, '');
    var words = { sss: 'SSS', sidesideside: 'SSS', sas: 'SAS', sideangleside: 'SAS', asa: 'ASA', anglesideangle: 'ASA', aas: 'AAS', angleangleside: 'AAS', saa: 'AAS',
      hl: 'HL', hypotenuseleg: 'HL', ssa: 'SSA', anglesideside: 'SSA', aaa: 'AAA', angleangleangle: 'AAA' };
    for (var w in words) { if (compact === w || compact === w + 'postulate' || compact === w + 'theorem' || compact === w + 'congruence' || compact === w + 'congruencepostulate' || compact === w + 'congruencetheorem') return words[w]; }
    if (/^given$/.test(t)) return 'given';
    if (/reflexive/.test(t)) return 'reflexive';
    if (/vertical/.test(t)) return 'vertical';
    if (/alternate interior|alt\.? ?int/.test(t)) return 'altint';
    if (/corresponding angle/.test(t)) return 'corresp';
    if (/midpoint/.test(t)) return 'midpoint';
    if (/bisect/.test(t)) return 'bisector';
    if (/right angles? (are|is)? ?congruent|all right angles|right angle congruence|right angles theorem/.test(t)) return 'rightcong';
    if (/perpendicular/.test(t)) return 'perp';
    if (/segment addition|addition postulate|segment subtraction|addition property/.test(t)) return 'segadd';
    return null;
  }

  /* ------------------------------------------------------------ geometry helpers */
  function sub(a, b) { return [a[0] - b[0], a[1] - b[1]]; }
  function len(v) { return Math.hypot(v[0], v[1]); }
  function dist(a, b) { return len(sub(a, b)); }
  function angleAt(P, V, Q) {
    var u = sub(P, V), w = sub(Q, V);
    var c = (u[0] * w[0] + u[1] * w[1]) / (len(u) * len(w));
    return Math.acos(Math.max(-1, Math.min(1, c))) * 180 / Math.PI;
  }
  function rot(p, t) { return [p[0] * Math.cos(t) - p[1] * Math.sin(t), p[0] * Math.sin(t) + p[1] * Math.cos(t)]; }
  var EPS = 1e-6;
  function minAng(P, a, b, c) { return Math.min(angleAt(P[b], P[a], P[c]), angleAt(P[a], P[b], P[c]), angleAt(P[a], P[c], P[b])); }

  /* ------------------------------------------------------------ statement objects
   seg: {t:'seg', a:[P,Q], b:[R,S]}   ang: {t:'ang', a:[P,V,Q], b:[R,W,S]}
   tri: {t:'tri', a:[P,Q,R], b:[S,T,U]}  right: {t:'right', a:[P,V,Q], b:[R,W,S]} (both are right angles) */
  var SYM = { cong: '≅', ang: '∠', tri: '△' };

  function show(st, L) {
    function m(x) { return L ? L[x] : x; }
    function seg(p) { return m(p[0]) + m(p[1]); }
    function ang(p) { return SYM.ang + m(p[0]) + m(p[1]) + m(p[2]); }
    if (st.t === 'seg') return seg(st.a) + ' ' + SYM.cong + ' ' + seg(st.b);
    if (st.t === 'ang') return ang(st.a) + ' ' + SYM.cong + ' ' + ang(st.b);
    if (st.t === 'tri') return SYM.tri + st.a.map(m).join('') + ' ' + SYM.cong + ' ' + SYM.tri + st.b.map(m).join('');
    if (st.t === 'right') return ang(st.a) + ' and ' + ang(st.b) + ' are right angles';
    return '';
  }

  /* ------------------------------------------------------------ templates
   Each returns roles -> coordinates, segments to draw, givens, facts, target triangles + correspondence. */
  function rotateAll(P, r) {
    var t = r.range(0, 2 * Math.PI), flip = r.next() < 0.5;
    var out = {};
    Object.keys(P).forEach(function (k) { var p = flip ? [-P[k][0], P[k][1]] : P[k]; out[k] = rot(p, t); });
    return out;
  }

  var TEMPLATES = {};

  /* Kite: triangles ABC and ADC share AC; D is the reflection of B over line AC. */
  TEMPLATES.kite = function (r, v) {
    var c, bx, by, P;
    for (var i = 0; i < 200; i++) {
      c = r.range(6, 8); bx = r.range(1.8, c - 1.6); by = r.range(2.2, 3.6);
      P = { A: [0, 0], C: [c, 0], B: [bx, by], D: [bx, -by] };
      var ab = dist(P.A, P.B), cb = dist(P.C, P.B);
      if (Math.abs(ab - cb) > 0.9 && angleAt(P.A, P.B, P.C) > 40 && angleAt(P.A, P.B, P.C) < 140 && minAng(P, 'A', 'B', 'C') > 24) break;
    }
    var T = { name: 'kite', points: P, segs: [['A', 'B'], ['B', 'C'], ['C', 'D'], ['D', 'A'], ['A', 'C']], tri: [['A', 'B', 'C'], ['A', 'D', 'C']] };
    var giv = [], facts = [], marks = [];
    var refl = { t: 'seg', a: ['A', 'C'], b: ['A', 'C'] };
    var bisA = { t: 'ang', a: ['B', 'A', 'C'], b: ['D', 'A', 'C'] }, bisC = { t: 'ang', a: ['B', 'C', 'A'], b: ['D', 'C', 'A'] };
    var sAB = { t: 'seg', a: ['A', 'B'], b: ['A', 'D'] }, sCB = { t: 'seg', a: ['C', 'B'], b: ['C', 'D'] };
    var angB = { t: 'ang', a: ['A', 'B', 'C'], b: ['A', 'D', 'C'] };
    if (v === 'SSS') { giv = [{ st: sAB }, { st: sCB }]; facts = [[sAB, 'given'], [sCB, 'given'], [refl, 'reflexive']]; }
    if (v === 'SAS') { giv = [{ st: sAB }, { txt: 'AC bisects ' + SYM.ang + 'BAD', mark: { bis: ['B', 'A', 'D', 'C'] } }]; facts = [[sAB, 'given'], [bisA, 'bisector'], [refl, 'reflexive']]; }
    if (v === 'ASA') { giv = [{ txt: 'AC bisects ' + SYM.ang + 'BAD', mark: { bis: ['B', 'A', 'D', 'C'] } }, { txt: 'AC bisects ' + SYM.ang + 'BCD', mark: { bis: ['B', 'C', 'D', 'A'] } }]; facts = [[bisA, 'bisector'], [refl, 'reflexive'], [bisC, 'bisector']]; }
    if (v === 'AAS') { giv = [{ st: angB }, { txt: 'AC bisects ' + SYM.ang + 'BAD', mark: { bis: ['B', 'A', 'D', 'C'] } }]; facts = [[angB, 'given'], [bisA, 'bisector'], [refl, 'reflexive']]; }
    T.givens = giv; T.facts = facts; T.post = v;
    T.cpctc = [{ t: 'seg', a: ['B', 'C'], b: ['D', 'C'] }, { t: 'ang', a: ['A', 'B', 'C'], b: ['A', 'D', 'C'] }, { t: 'ang', a: ['B', 'C', 'A'], b: ['D', 'C', 'A'] }, { t: 'seg', a: ['A', 'B'], b: ['A', 'D'] }];
    return T;
  };

  /* Bowtie: segments AD and BE cross at M; D and E are the images of A and B under a half-turn about M. */
  TEMPLATES.bowtie = function (r, v) {
    var P;
    for (var i = 0; i < 200; i++) {
      var a = r.range(3, 4.6), b = r.range(2.4, 4.2), t1 = r.range(2.3, 2.9), t2 = t1 + r.range(0.75, 1.5);
      var A = [a * Math.cos(t1), a * Math.sin(t1)], B = [b * Math.cos(t2), b * Math.sin(t2)];
      P = { M: [0, 0], A: A, B: B, D: [-A[0], -A[1]], E: [-B[0], -B[1]] };
      var ang = angleAt(P.A, P.M, P.B);
      if (ang > 45 && ang < 120 && Math.abs(a - b) > 0.6 && dist(A, B) > 2.2 && angleAt(P.M, P.A, P.B) > 30 && angleAt(P.M, P.B, P.A) > 30) break;
    }
    var T = { name: 'bowtie', points: P, segs: [['A', 'D'], ['B', 'E'], ['A', 'B'], ['D', 'E']], tri: [['A', 'M', 'B'], ['D', 'M', 'E']] };
    var vert = { t: 'ang', a: ['A', 'M', 'B'], b: ['D', 'M', 'E'] };
    var mA = { t: 'seg', a: ['A', 'M'], b: ['D', 'M'] }, mB = { t: 'seg', a: ['B', 'M'], b: ['E', 'M'] };
    var aiA = { t: 'ang', a: ['B', 'A', 'M'], b: ['E', 'D', 'M'] }, aiB = { t: 'ang', a: ['A', 'B', 'M'], b: ['D', 'E', 'M'] };
    var sAB = { t: 'seg', a: ['A', 'B'], b: ['D', 'E'] };
    var par = { txt: 'AB ∥ DE', mark: { par: [['A', 'B'], ['E', 'D']] } };
    if (v === 'SAS') { T.givens = [{ txt: 'M is the midpoint of AD', mark: { mid: ['A', 'M', 'D'] } }, { txt: 'M is the midpoint of BE', mark: { mid: ['B', 'M', 'E'] } }]; T.facts = [[mA, 'midpoint'], [vert, 'vertical'], [mB, 'midpoint']]; }
    if (v === 'ASA') { T.givens = [par, { txt: 'M is the midpoint of AD', mark: { mid: ['A', 'M', 'D'] } }]; T.facts = [[aiA, 'altint'], [mA, 'midpoint'], [vert, 'vertical']]; }
    if (v === 'AAS') { T.givens = [par, { st: sAB }]; T.facts = [[aiB, 'altint'], [vert, 'vertical'], [sAB, 'given']]; }
    T.post = v;
    T.cpctc = [sAB, aiA, aiB, mB, mA];
    return T;
  };

  /* Parallelogram ABCD with diagonal AC: triangles ABC and CDA. */
  TEMPLATES.para = function (r, v) {
    var P;
    for (var i = 0; i < 200; i++) {
      var w = r.range(5.5, 7.5), s = r.range(1.2, 2.6) * (r.next() < 0.5 ? 1 : -1), h = r.range(3.2, 4.4);
      P = { A: [0, 0], B: [w, 0], C: [w + s, h], D: [s, h] };
      if (Math.abs(dist(P.A, P.D) - w) > 1.2 && minAng(P, 'A', 'B', 'C') > 24) break;
    }
    var T = { name: 'para', points: P, segs: [['A', 'B'], ['B', 'C'], ['C', 'D'], ['D', 'A'], ['A', 'C']], tri: [['A', 'B', 'C'], ['C', 'D', 'A']] };
    var refl = { t: 'seg', a: ['A', 'C'], b: ['C', 'A'] };
    var ai1 = { t: 'ang', a: ['B', 'A', 'C'], b: ['D', 'C', 'A'] }, ai2 = { t: 'ang', a: ['B', 'C', 'A'], b: ['D', 'A', 'C'] };
    var sAB = { t: 'seg', a: ['A', 'B'], b: ['C', 'D'] }, sBC = { t: 'seg', a: ['B', 'C'], b: ['D', 'A'] };
    var p1 = { txt: 'AB ∥ DC', mark: { par: [['A', 'B'], ['D', 'C']] } }, p2 = { txt: 'AD ∥ BC', mark: { par2: [['A', 'D'], ['B', 'C']] } };
    if (v === 'SAS') { T.givens = [p1, { st: sAB }]; T.facts = [[sAB, 'given'], [ai1, 'altint'], [refl, 'reflexive']]; }
    if (v === 'ASA') { T.givens = [p1, p2]; T.facts = [[ai1, 'altint'], [refl, 'reflexive'], [ai2, 'altint']]; }
    if (v === 'SSS') { T.givens = [{ st: sAB }, { st: sBC }]; T.facts = [[sAB, 'given'], [sBC, 'given'], [refl, 'reflexive']]; }
    T.post = v;
    T.cpctc = [{ t: 'ang', a: ['A', 'B', 'C'], b: ['C', 'D', 'A'] }, sBC, ai2, sAB];
    return T;
  };

  /* Isosceles triangle ABC (AB = AC) with D the midpoint of BC, so AD is also the altitude and bisector. */
  TEMPLATES.iso = function (r, v) {
    var b = r.range(2.4, 3.6), h = r.range(3.8, 5.2);
    var P = { A: [0, h], B: [-b, 0], C: [b, 0], D: [0, 0] };
    var T = { name: 'iso', points: P, segs: [['A', 'B'], ['A', 'C'], ['B', 'C'], ['A', 'D']], tri: [['A', 'D', 'B'], ['A', 'D', 'C']] };
    var refl = { t: 'seg', a: ['A', 'D'], b: ['A', 'D'] };
    var sAB = { t: 'seg', a: ['A', 'B'], b: ['A', 'C'] }, sBD = { t: 'seg', a: ['B', 'D'], b: ['C', 'D'] };
    var bis = { t: 'ang', a: ['B', 'A', 'D'], b: ['C', 'A', 'D'] }, rt = { t: 'ang', a: ['A', 'D', 'B'], b: ['A', 'D', 'C'] };
    var mid = { txt: 'D is the midpoint of BC', mark: { mid: ['B', 'D', 'C'] } }, perp = { txt: 'AD ⊥ BC', mark: { right: ['A', 'D', 'C'] } };
    if (v === 'SSS') { T.givens = [{ st: sAB }, mid]; T.facts = [[sAB, 'given'], [sBD, 'midpoint'], [refl, 'reflexive']]; }
    if (v === 'SAS') { T.givens = [{ st: sAB }, { txt: 'AD bisects ' + SYM.ang + 'BAC', mark: { bis: ['B', 'A', 'C', 'D'] } }]; T.facts = [[sAB, 'given'], [bis, 'bisector'], [refl, 'reflexive']]; }
    if (v === 'SAS2') { T.givens = [perp, mid]; T.facts = [[sBD, 'midpoint'], [rt, 'perp|rightcong'], [refl, 'reflexive']]; v = 'SAS'; }
    if (v === 'HL') { T.givens = [perp, { st: sAB }]; T.facts = [[{ t: 'right', a: ['A', 'D', 'B'], b: ['A', 'D', 'C'] }, 'perp'], [sAB, 'given'], [refl, 'reflexive']]; }
    T.post = v;
    T.cpctc = [{ t: 'ang', a: ['A', 'B', 'D'], b: ['A', 'C', 'D'] }, sBD, bis];
    return T;
  };

  /* Shared angle: B, D on one ray from A and C, E on the other with AB = AC, AD = AE. Triangles ABE and ACD overlap. */
  TEMPLATES.shared = function (r, v) {
    var P;
    for (var i = 0; i < 200; i++) {
      var open = r.range(48, 72) * Math.PI / 180, base = r.range(-0.4, 0.4), p = r.range(6.5, 8), q = p * r.range(0.45, 0.6);
      var u1 = [Math.cos(base + open / 2), Math.sin(base + open / 2)], u2 = [Math.cos(base - open / 2), Math.sin(base - open / 2)];
      P = { A: [0, 0], B: [p * u1[0], p * u1[1]], D: [q * u1[0], q * u1[1]], C: [p * u2[0], p * u2[1]], E: [q * u2[0], q * u2[1]] };
      if (dist(P.B, P.C) > 3) break;
    }
    var T = { name: 'shared', points: P, segs: [['A', 'B'], ['A', 'C'], ['B', 'E'], ['C', 'D']], tri: [['A', 'B', 'E'], ['A', 'C', 'D']] };
    var sAB = { t: 'seg', a: ['A', 'B'], b: ['A', 'C'] }, sAE = { t: 'seg', a: ['A', 'E'], b: ['A', 'D'] };
    var refl = { t: 'ang', a: ['B', 'A', 'E'], b: ['C', 'A', 'D'] };
    T.givens = [{ st: sAB }, { st: sAE }];
    T.facts = [[sAB, 'given'], [refl, 'reflexive'], [sAE, 'given']];
    T.post = 'SAS';
    T.cpctc = [{ t: 'seg', a: ['B', 'E'], b: ['C', 'D'] }, { t: 'ang', a: ['A', 'B', 'E'], b: ['A', 'C', 'D'] }, { t: 'ang', a: ['A', 'E', 'B'], b: ['A', 'D', 'C'] }];
    return T;
  };

  /* Translation: A, B, C, D in order on a line with AB = CD; triangle BDF is triangle ACE slid along the line. */
  TEMPLATES.slide = function (r, v) {
    var P;
    for (var i = 0; i < 200; i++) {
      var t = r.range(1.6, 2.4), c = r.range(4.2, 5.4), ex = r.range(0.8, c - 0.8), ey = r.range(2.6, 3.6);
      P = { A: [0, 0], B: [t, 0], C: [c, 0], D: [c + t, 0], E: [ex, ey], F: [ex + t, ey] };
      if (angleAt(P.E, P.A, P.C) > 35 && angleAt(P.E, P.C, P.A) > 35) break;
    }
    var T = { name: 'slide', points: P, segs: [['A', 'D'], ['A', 'E'], ['E', 'C'], ['B', 'F'], ['F', 'D']], tri: [['A', 'C', 'E'], ['B', 'D', 'F']] };
    var sAC = { t: 'seg', a: ['A', 'C'], b: ['B', 'D'] };
    var cA = { t: 'ang', a: ['E', 'A', 'C'], b: ['F', 'B', 'D'] }, cC = { t: 'ang', a: ['E', 'C', 'A'], b: ['F', 'D', 'B'] };
    var sAE = { t: 'seg', a: ['A', 'E'], b: ['B', 'F'] }, sCE = { t: 'seg', a: ['C', 'E'], b: ['D', 'F'] };
    var gAB = { st: { t: 'seg', a: ['A', 'B'], b: ['C', 'D'] } };
    var pA = { txt: 'AE ∥ BF', mark: { par: [['A', 'E'], ['B', 'F']] } }, pC = { txt: 'CE ∥ DF', mark: { par2: [['C', 'E'], ['D', 'F']] } };
    if (v === 'SAS') { T.givens = [gAB, pA, { st: sAE }]; T.facts = [[sAC, 'segadd'], [cA, 'corresp'], [sAE, 'given']]; }
    if (v === 'ASA') { T.givens = [gAB, pA, pC]; T.facts = [[cA, 'corresp'], [sAC, 'segadd'], [cC, 'corresp']]; }
    if (v === 'SSS') { T.givens = [gAB, { st: sAE }, { st: sCE }]; T.facts = [[sAE, 'given'], [sCE, 'given'], [sAC, 'segadd']]; }
    T.post = v;
    T.cpctc = [sCE, cC, { t: 'ang', a: ['A', 'E', 'C'], b: ['B', 'F', 'D'] }, sAE];
    return T;
  };

  /* ------------------------------------------------------------ proof set */
  var LETTERS = 'ABCDEFGHJKLMNPQRSTUVWXYZ'.split('');
  /* Five stages: 1 drag statements, 2 drag reasons, 3 drag both, 4 write (no bank), 5 write CPCTC. */
  var PLAN = [
    { stage: 1, opts: [['kite', 'SSS'], ['para', 'SSS'], ['iso', 'SSS']] },
    { stage: 1, opts: [['bowtie', 'SAS'], ['iso', 'SAS']] },
    { stage: 1, opts: [['iso', 'HL']] },
    { stage: 2, opts: [['para', 'ASA'], ['kite', 'ASA']] },
    { stage: 2, opts: [['bowtie', 'ASA'], ['iso', 'SAS2'], ['kite', 'SAS']] },
    { stage: 3, opts: [['bowtie', 'AAS'], ['kite', 'AAS']] },
    { stage: 3, opts: [['shared', 'SAS'], ['slide', 'SSS']] },
    { stage: 3, opts: [['kite', 'SAS'], ['para', 'SAS']], cpctc: true },
    { stage: 4, opts: [['para', 'SAS'], ['bowtie', 'SAS'], ['kite', 'SSS']] },
    { stage: 4, opts: [['slide', 'ASA'], ['slide', 'SAS'], ['bowtie', 'AAS']] },
    { stage: 5, opts: [['bowtie', 'SAS'], ['para', 'ASA'], ['shared', 'SAS']], cpctc: true },
    { stage: 5, opts: [['iso', 'SAS'], ['slide', 'SAS'], ['kite', 'ASA']], cpctc: true }
  ];
  var STAGES = {
    1: { title: 'Drag the statements', how: 'The reasons are filled in. Drag (or tap) a statement from the bank into each row.' },
    2: { title: 'Drag the reasons', how: 'The statements are filled in. Drag (or tap) the reason that justifies each row.' },
    3: { title: 'Statements and reasons', how: 'Fill in every statement and every reason from the banks. Some bank items do not belong.' },
    4: { title: 'Write the proof', how: 'No word bank. Write each statement and its reason. The symbol buttons help you type ≅, ∠ and △.' },
    5: { title: 'Write a CPCTC proof', how: 'No word bank. Prove the triangles congruent, then use CPCTC to prove the final statement.' }
  };

  function relabel(T, r) {
    var roles = Object.keys(T.points);
    var letters = r.shuffle(LETTERS).slice(0, roles.length);
    var L = {};
    roles.forEach(function (k, i) { L[k] = letters[i]; });
    return L;
  }

  function mapSt(st, L) {
    var o = { t: st.t };
    ['a', 'b'].forEach(function (k) { o[k] = st[k].map(function (x) { return L[x]; }); });
    return o;
  }

  function txtMap(s, L) {
    return s.replace(/[A-Z]/g, function (ch) { return L[ch] || ch; });
  }

  function makeProof(index, seed) {
    var spec = PLAN[index];
    var r = rng(seed * 1009 + index * 7919 + 17);
    var choice = r.pick(spec.opts);
    var T = TEMPLATES[choice[0]](r, choice[1]);
    var L = relabel(T, r);
    var pts = {};
    var rotated = rotateAll(T.points, r);
    Object.keys(rotated).forEach(function (k) { pts[L[k]] = rotated[k]; });
    var givens = T.givens.map(function (g) {
      if (g.st) return { text: show(g.st, L), st: mapSt(g.st, L) };
      var m = {};
      if (g.mark) Object.keys(g.mark).forEach(function (k) { m[k] = JSON.parse(JSON.stringify(g.mark[k]), function (kk, val) { return typeof val === 'string' && L[val] ? L[val] : val; }); });
      return { text: txtMap(g.txt, L), mark: m };
    });
    var rows = T.facts.map(function (f) { return { st: mapSt(f[0], L), reasons: f[1].split('|') }; });
    var triSt = { t: 'tri', a: T.tri[0].map(function (x) { return L[x]; }), b: T.tri[1].map(function (x) { return L[x]; }) };
    rows.push({ st: triSt, reasons: [T.post] });
    var prove = triSt, cp = null;
    if (spec.cpctc) {
      cp = mapSt(r.pick(T.cpctc), L);
      rows.push({ st: cp, reasons: ['cpctc'] });
      prove = cp;
    }
    var proof = {
      n: index + 1, stage: spec.stage, template: T.name, postulate: T.post, cpctc: !!spec.cpctc,
      points: pts, segs: T.segs.map(function (s) { return [L[s[0]], L[s[1]]]; }),
      triangles: [triSt.a, triSt.b], givens: givens, prove: prove, proveText: show(prove), rows: rows
    };
    proof.bank = makeBank(proof, r);
    return proof;
  }

  function makeSet(seed) {
    var out = [];
    for (var i = 0; i < PLAN.length; i++) out.push(makeProof(i, seed));
    return out;
  }

  /* ------------------------------------------------------------ word banks */
  function makeBank(proof, r) {
    var stmts = proof.rows.map(function (row) { return show(row.st); });
    var reasons = proof.rows.map(function (row) { return REASONS[row.reasons[0]]; });
    var t = proof.triangles;
    var cands = [];
    var A = t[0], B = t[1];
    // wrong correspondence triangle statement
    cands.push(show({ t: 'tri', a: A, b: [B[0], B[2], B[1]] }));
    cands.push(show({ t: 'tri', a: A, b: [B[1], B[0], B[2]] }));
    // non-corresponding sides / angles
    cands.push(show({ t: 'seg', a: [A[0], A[1]], b: [B[1], B[2]] }));
    cands.push(show({ t: 'seg', a: [A[1], A[2]], b: [B[0], B[2]] }));
    cands.push(show({ t: 'ang', a: [A[1], A[0], A[2]], b: [B[0], B[1], B[2]] }));
    cands.push(show({ t: 'ang', a: [A[0], A[2], A[1]], b: [B[1], B[0], B[2]] }));
    var bad = [];
    r.shuffle(cands).forEach(function (s) {
      if (stmts.indexOf(s) >= 0 || bad.indexOf(s) >= 0) return;
      var parsed = parseStatement(s, proof);
      if (parsed.ok && !isTrue(parsed.st, proof)) bad.push(s);   // only statements that are false in the figure
    });
    bad = bad.slice(0, proof.stage === 3 ? 2 : 3);
    var usedR = {};
    proof.rows.forEach(function (row) { row.reasons.forEach(function (k) { usedR[k] = 1; }); });
    var rpool = ['SSA', 'AAA', 'vertical', 'midpoint', 'altint', 'bisector', 'corresp', 'SSS', 'SAS', 'ASA', 'AAS', 'reflexive'].filter(function (k) { return !usedR[k]; });
    var badR = r.shuffle(rpool).slice(0, proof.stage === 3 ? 2 : 3).map(function (k) { return REASONS[k]; });
    return { statements: r.shuffle(stmts.concat(bad)), reasons: r.shuffle(uniq(reasons).concat(badR)) };
  }
  function uniq(a) { return a.filter(function (x, i) { return a.indexOf(x) === i; }); }

  /* ------------------------------------------------------------ parsing what a student wrote */
  function normText(s) {
    return String(s || '')
      .replace(/\bis congruent to\b|≅|=~|~=|\bcongruent to\b|\bcong\b/gi, '≅')
      .replace(/\b[Tt]riangle\s*|\b[Tt]ri\s+|Δ|∆|△\s*/g, '△')
      .replace(/\b[Aa]ngle\s+(?=[A-Za-z]{1,3}\b)|m∠|<|∠\s*/g, '∠')
      .replace(/\b[Ss]eg(ment)?\s+(?=[A-Za-z]{2}\b)/g, '')
      .replace(/\s+/g, ' ').trim();
  }

  function parseStatement(text, proof) {
    var s = normText(text);
    if (!s) return { ok: false, msg: 'Write a statement.' };
    var labels = Object.keys(proof.points);
    function okLetters(str) { return str.split('').every(function (c) { return labels.indexOf(c) >= 0; }); }
    var m;
    if ((m = /^∠\s*([A-Z]{1,3}) and ∠\s*([A-Z]{1,3}) are right angles?\.?$/i.exec(s))) {
      var a1 = angleName(m[1].toUpperCase(), proof), a2 = angleName(m[2].toUpperCase(), proof);
      if (!a1 || !a2) return { ok: false, msg: 'Check the angle names: use three letters with the vertex in the middle.' };
      return { ok: true, st: { t: 'right', a: a1, b: a2 } };
    }
    var parts = s.split(/\s*[≅=]\s*/);
    if (parts.length !== 2) return { ok: false, msg: 'Write one congruence, for example AB ≅ CD.' };
    var L = parts[0].replace(/\s/g, ''), R = parts[1].replace(/\s/g, '').replace(/\.$/, '');
    if (/^△/.test(L) || /^△/.test(R)) {
      L = L.replace(/^△/, '').toUpperCase(); R = R.replace(/^△/, '').toUpperCase();
      if (L.length !== 3 || R.length !== 3 || !okLetters(L + R)) return { ok: false, msg: 'Name each triangle with three labeled points, for example △ABC ≅ △DEF.' };
      return { ok: true, st: { t: 'tri', a: L.split(''), b: R.split('') } };
    }
    if (/^∠/.test(L) || /^∠/.test(R)) {
      var x = angleName(L.replace(/^∠/, '').toUpperCase(), proof), y = angleName(R.replace(/^∠/, '').toUpperCase(), proof);
      if (!x || !y) return { ok: false, msg: 'Name each angle with three letters (vertex in the middle), or one letter when only one angle is at that vertex.' };
      return { ok: true, st: { t: 'ang', a: x, b: y } };
    }
    L = L.toUpperCase(); R = R.toUpperCase();
    if (L.length === 2 && R.length === 2 && okLetters(L + R) && L[0] !== L[1] && R[0] !== R[1]) {
      if (!isDrawnSeg(L, proof) || !isDrawnSeg(R, proof)) return { ok: false, msg: 'One of those segments is not in the diagram.' };
      return { ok: true, st: { t: 'seg', a: L.split(''), b: R.split('') } };
    }
    return { ok: false, msg: 'Could not read this statement. Use forms like AB ≅ CD, ∠ABC ≅ ∠DEF or △ABC ≅ △DEF.' };
  }

  function onSegment(P, Q, X) { var d = dist(P, X) + dist(X, Q) - dist(P, Q); return Math.abs(d) < 1e-6; }
  function isDrawnSeg(two, proof) {
    var P = proof.points[two[0]], Q = proof.points[two[1]];
    return proof.segs.some(function (s) { var a = proof.points[s[0]], b = proof.points[s[1]]; return onSegment(a, b, P) && onSegment(a, b, Q); });
  }
  /* rays from a vertex along drawn segments */
  function raysAt(V, proof) {
    var pv = proof.points[V], out = [];
    proof.segs.forEach(function (s) {
      var a = proof.points[s[0]], b = proof.points[s[1]];
      if (!onSegment(a, b, pv)) return;
      [a, b].forEach(function (e) { if (dist(e, pv) > 1e-6) { var d = Math.atan2(e[1] - pv[1], e[0] - pv[0]); if (!out.some(function (x) { return Math.abs(Math.atan2(Math.sin(x - d), Math.cos(x - d))) < 1e-6; })) out.push(d); } });
    });
    return out;
  }
  function angleName(str, proof) {
    if (str.length === 3) {
      if (!proof.points[str[0]] || !proof.points[str[1]] || !proof.points[str[2]]) return null;
      if (!isDrawnSeg(str[0] + str[1], proof) || !isDrawnSeg(str[1] + str[2], proof)) return null;
      return str.split('');
    }
    if (str.length === 1 && proof.points[str]) {
      var rays = raysAt(str, proof);
      if (rays.length !== 2) return null;   // ambiguous single-letter name
      // find labeled points along each ray
      var V = proof.points[str], ends = rays.map(function (d) {
        return Object.keys(proof.points).filter(function (k) { var p = proof.points[k]; if (k === str) return false; var a = Math.atan2(p[1] - V[1], p[0] - V[0]); return Math.abs(Math.atan2(Math.sin(a - d), Math.cos(a - d))) < 1e-6 && isDrawnSeg(str + k, proof); })[0];
      });
      if (!ends[0] || !ends[1]) return null;
      return [ends[0], str, ends[1]];
    }
    return null;
  }

  /* ------------------------------------------------------------ meaning in the figure */
  function segKey(p, proof) { return p.slice().sort().join(''); }
  function angKey(a, proof) {
    var V = proof.points[a[1]];
    var d = [a[0], a[2]].map(function (k) { var P = proof.points[k]; var t = Math.atan2(P[1] - V[1], P[0] - V[0]); return Math.round(((t + 2 * Math.PI) % (2 * Math.PI)) * 1e5); });
    d.sort(function (x, y) { return x - y; });
    return a[1] + ':' + d.join(',');
  }
  function partKey(t, p, proof) { return t === 'seg' ? 's:' + segKey(p, proof) : 'a:' + angKey(p, proof); }
  function factKey(st, proof) {
    if (st.t === 'right') { var k = [partKey('ang', st.a, proof), partKey('ang', st.b, proof)].sort(); return 'R|' + k.join('|'); }
    var t = st.t === 'seg' ? 'seg' : 'ang';
    var ks = [partKey(t, st.a, proof), partKey(t, st.b, proof)].sort();
    return ks.join('|');
  }
  function measure(t, p, proof) { return t === 'seg' ? dist(proof.points[p[0]], proof.points[p[1]]) : angleAt(proof.points[p[0]], proof.points[p[1]], proof.points[p[2]]); }
  function isTrue(st, proof) {
    if (st.t === 'seg') return Math.abs(measure('seg', st.a, proof) - measure('seg', st.b, proof)) < 1e-6;
    if (st.t === 'ang') return Math.abs(measure('ang', st.a, proof) - measure('ang', st.b, proof)) < 1e-4;
    if (st.t === 'right') return Math.abs(measure('ang', st.a, proof) - 90) < 1e-4 && Math.abs(measure('ang', st.b, proof) - 90) < 1e-4;
    if (st.t === 'tri') return triMatch(st.a, st.b, proof);
    return false;
  }
  function triMatch(a, b, proof) {
    for (var i = 0; i < 3; i++) {
      var j = (i + 1) % 3;
      if (Math.abs(dist(proof.points[a[i]], proof.points[a[j]]) - dist(proof.points[b[i]], proof.points[b[j]])) > 1e-6) return false;
    }
    return new Set(a).size === 3 && new Set(b).size === 3;
  }
  function factTable(proof) {
    var tab = {};
    proof.rows.forEach(function (row) {
      if (row.st.t === 'tri' || row.reasons[0] === 'cpctc') return;
      tab[factKey(row.st, proof)] = row.reasons;
    });
    proof.givens.forEach(function (g) { if (g.st) { var k = factKey(g.st, proof); tab[k] = (tab[k] || []).concat(['given']); } });
    return tab;
  }

  /* parts of the two triangles under a correspondence */
  function triParts(a, b, proof) {
    var sides = [[0, 1], [1, 2], [0, 2]].map(function (ix) { return { key: [partKey('seg', [a[ix[0]], a[ix[1]]], proof), partKey('seg', [b[ix[0]], b[ix[1]]], proof)], v: ix }; });
    var angs = [0, 1, 2].map(function (i) { var o = [0, 1, 2].filter(function (j) { return j !== i; }); return { key: [partKey('ang', [a[o[0]], a[i], a[o[1]]], proof), partKey('ang', [b[o[0]], b[i], b[o[1]]], proof)], v: i }; });
    return { sides: sides, angs: angs };
  }
  function matchPart(st, parts, proof) {
    if (st.t === 'seg' || st.t === 'ang') {
      var t = st.t, k1 = partKey(t, st.a, proof), k2 = partKey(t, st.b, proof);
      var list = t === 'seg' ? parts.sides : parts.angs;
      for (var i = 0; i < list.length; i++) { var p = list[i].key; if ((p[0] === k1 && p[1] === k2) || (p[0] === k2 && p[1] === k1)) return { kind: t === 'seg' ? 'S' : 'A', v: list[i].v }; }
      return null;
    }
    if (st.t === 'right') {
      var r1 = partKey('ang', st.a, proof), r2 = partKey('ang', st.b, proof);
      for (var j = 0; j < 3; j++) { var q = parts.angs[j].key; if ((q[0] === r1 && q[1] === r2) || (q[0] === r2 && q[1] === r1)) return { kind: 'R', v: j }; }
    }
    return null;
  }
  function classify(found) {
    var S = found.filter(function (f) { return f.kind === 'S'; }).map(function (f) { return f.v; });
    var A = found.filter(function (f) { return f.kind === 'A'; }).map(function (f) { return f.v; });
    var Rt = found.filter(function (f) { return f.kind === 'R'; }).map(function (f) { return f.v; });
    if (Rt.length === 1 && S.length === 2 && A.length === 0) {
      var rv = Rt[0], hyp = S.filter(function (s) { return s.indexOf(rv) < 0; });
      return hyp.length === 1 ? 'HL' : 'none';
    }
    if (S.length === 3) return 'SSS';
    if (S.length === 2 && A.length === 1) {
      var shared = S[0].filter(function (x) { return S[1].indexOf(x) >= 0; })[0];
      return shared === A[0] ? 'SAS' : 'SSA';
    }
    if (S.length === 1 && A.length === 2) return S[0].indexOf(A[0]) >= 0 && S[0].indexOf(A[1]) >= 0 ? 'ASA' : 'AAS';
    if (A.length === 3) return 'AAA';
    return 'none';
  }

  /* ------------------------------------------------------------ the checker
   rows: [{statement, reason}] in the student's order. Returns {ok, rows:[{ok, msg}], summary}. */
  function check(proof, rows) {
    var nSupport = proof.rows.length - (proof.cpctc ? 2 : 1);
    var res = rows.map(function () { return { ok: false, msg: '' }; });
    var table = factTable(proof);
    var parsed = rows.map(function (row) { return parseStatement(row.statement, proof); });
    var keys = rows.map(function (row) { return reasonKey(row.reason); });
    var triIdx = nSupport, cpIdx = proof.cpctc ? nSupport + 1 : -1;
    var supportFacts = [];
    // support rows
    for (var i = 0; i < nSupport; i++) {
      var p = parsed[i], k = keys[i];
      if (!rows[i].statement || !String(rows[i].statement).trim()) { res[i].msg = 'This row is empty.'; continue; }
      if (!p.ok) { res[i].msg = p.msg; continue; }
      if (p.st.t === 'tri') { res[i].msg = 'Prove three pairs of parts congruent before stating that the triangles are congruent.'; continue; }
      if (!isTrue(p.st, proof)) { res[i].msg = 'This congruence is not true in the figure.'; continue; }
      if (!rows[i].reason || !String(rows[i].reason).trim()) { res[i].msg = 'Add a reason.'; continue; }
      if (!k) { res[i].msg = 'This reason is not one of the standard reasons. Try Given, Reflexive Property, Vertical angles, Definition of midpoint, and so on.'; continue; }
      var allowed = table[factKey(p.st, proof)];
      if (!allowed) { res[i].msg = 'True in the picture, but it does not follow from the given information.'; continue; }
      if (allowed.indexOf(k) < 0) { res[i].msg = 'The statement is right, but this reason does not justify it.'; continue; }
      if (supportFacts.some(function (f) { return f.key === factKey(p.st, proof); })) { res[i].msg = 'This repeats an earlier row.'; continue; }
      res[i].ok = true;
      supportFacts.push({ key: factKey(p.st, proof), st: p.st, row: i });
    }
    // triangle row
    var tp = parsed[triIdx], tk = keys[triIdx], tri = null;
    if (!tp || !tp.ok) res[triIdx].msg = (tp && tp.msg) || 'Write the triangle congruence.';
    else if (tp.st.t !== 'tri') res[triIdx].msg = 'This row should state that the two triangles are congruent.';
    else {
      var want = proof.triangles.map(function (t) { return t.slice().sort().join(''); }).sort().join('|');
      var got = [tp.st.a.slice().sort().join(''), tp.st.b.slice().sort().join('')].sort().join('|');
      if (want !== got) res[triIdx].msg = 'These are not the two triangles in the Prove statement.';
      else if (!triMatch(tp.st.a, tp.st.b, proof)) res[triIdx].msg = 'The vertices are not in corresponding order. Match each vertex with its partner.';
      else {
        tri = tp.st;
        var parts = triParts(tri.a, tri.b, proof);
        var found = [], notPart = false;
        supportFacts.forEach(function (f) { var m = matchPart(f.st, parts, proof); if (m) found.push(m); else { notPart = true; res[f.row].ok = false; res[f.row].msg = 'True, but these are not corresponding parts of the two triangles in your congruence statement.'; } });
        var kind = classify(found);
        if (!tk) res[triIdx].msg = 'Name the congruence postulate or theorem (SSS, SAS, ASA, AAS or HL).';
        else if (supportFacts.length < nSupport || notPart) res[triIdx].msg = 'Fix the rows above first; they must give three pairs of corresponding parts.';
        else if (kind === 'SSA' || kind === 'AAA' || kind === 'none') res[triIdx].msg = 'These parts (' + kind + ') do not prove triangles congruent.';
        else if (tk !== kind) res[triIdx].msg = 'Your rows show ' + kind + ', not ' + (REASONS[tk] || tk) + '. Check the order of the parts.';
        else res[triIdx].ok = true;
      }
    }
    // CPCTC row
    if (cpIdx >= 0) {
      var cpp = parsed[cpIdx], ck = keys[cpIdx];
      if (!cpp || !cpp.ok) res[cpIdx].msg = (cpp && cpp.msg) || 'Write the statement you are proving.';
      else if (factKey(cpp.st, proof) !== factKey(proof.prove, proof)) res[cpIdx].msg = 'The last statement must be the Prove statement.';
      else if (ck !== 'cpctc') res[cpIdx].msg = 'Use CPCTC: corresponding parts of congruent triangles are congruent.';
      else if (!tri) res[cpIdx].msg = 'First state the triangle congruence correctly.';
      else if (!matchPart(cpp.st, triParts(tri.a, tri.b, proof), proof)) res[cpIdx].msg = 'These are not corresponding parts under your triangle congruence.';
      else res[cpIdx].ok = true;
    }
    var ok = res.every(function (x) { return x.ok; });
    return { ok: ok, rows: res, correct: res.filter(function (x) { return x.ok; }).length };
  }

  function modelRows(proof) {
    return proof.rows.map(function (row) { return { statement: show(row.st), reason: REASONS[row.reasons[0]] }; });
  }

  var API = { rng: rng, makeSet: makeSet, makeProof: makeProof, check: check, modelRows: modelRows, show: show, parseStatement: parseStatement,
    reasonKey: reasonKey, isTrue: isTrue, REASONS: REASONS, STAGES: STAGES, PLAN: PLAN, TEMPLATES: TEMPLATES, normText: normText };
  if (typeof module !== 'undefined' && module.exports) module.exports = API;
  root.MK_PROOFS = API;
})(typeof window !== 'undefined' ? window : globalThis);
