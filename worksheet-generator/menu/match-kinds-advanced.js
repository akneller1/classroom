/* Matching kinds for Algebra 2, Precalculus and Calculus:
     trig   Sinusoids: graph ↔ equation y = a sin(b(x − c)) + d ↔ key-point table ↔ features
     deriv  A function and its derivatives: graph of f ↔ graph of f′ ↔ graph of f″ ↔ behavior of f
     conic  Conic sections: graph ↔ standard form ↔ general form ↔ features
   Each set is built from exact parameters; features and tables are computed from them and every fact is tested
   on every other set in the activity, so each card fits exactly one set.
   Needs: menu/match-kinds.js. */
(function (G) {
  'use strict';
  var MK = G.MKMATCH, U = MK.util, SV = MK.svg, k = U.k, kd = U.kd;
  var PI = Math.PI;
  /* a rational multiple of π as TeX */
  function piTex(q) {
    var r = U.toQ(q, 48); if (!r) return String(q);
    if (r.n === 0) return '0';
    var n = Math.abs(r.n), s = r.n < 0 ? '-' : '';
    if (r.d === 1) return s + (n === 1 ? '' : n) + '\\pi';
    return s + '\\frac{' + (n === 1 ? '' : n) + '\\pi}{' + r.d + '}';
  }
  function chooseFacts(set, sets, rng, F, make) {   // F: list of fact ids; make(set, id) → {text, test(other)} | null
    var made = {}; F.forEach(function (id) { var f = make(set, id); if (f && f.test(set)) made[id] = f; });
    var ids = Object.keys(made);
    for (var t = 0; t < 120; t++) {
      var pick = rng.shuffle(ids).slice(0, rng.pick([2, 2, 3])), fs = pick.map(function (id) { return made[id]; });
      if (fs.length < 2) return null;
      if (sets.every(function (o) { return o === set || !fs.every(function (f) { return f.test(o); }); })) return fs;
    }
    for (var t2 = 0; t2 < 60; t2++) { var p3 = rng.shuffle(ids).slice(0, 4), fs3 = p3.map(function (id) { return made[id]; }); if (sets.every(function (o) { return o === set || !fs3.every(function (f) { return f.test(o); }); })) return fs3; }
    return null;
  }
  function facesOfFacts(fs) { return '<div class="mk-txt left">' + fs.map(function (f) { return '<p>' + U.mt(f.text) + '</p>'; }).join('') + '</div>'; }
  function sameOn(f, g, lo, hi) { for (var i = 0; i <= 200; i++) { var x = lo + (hi - lo) * i / 200; if (Math.abs(f(x) - g(x)) > 1e-6) return false; } return true; }

  /* ======================= SINUSOIDS ======================= */
  MK.register({
    id: 'trig', name: 'Sinusoid Matching', short: 'Sine & Cosine Graphs', noun: 'sinusoid', anchor: 'eq',
    anchorText: 'Start with each equation already in its set', anchorHint: 'Recommended: students read the amplitude, period and midline from each equation.',
    blurb: 'Match each sinusoid’s <b>equation</b> to its <b>graph</b>, a <b>table</b> of key points (one period in quarters) and its <b>features</b> (amplitude, period, midline, maximum and minimum). Look-alikes share an amplitude or a midline.',
    tip: 'For y = a sin(b(x − c)) + d: the amplitude is |a|, the period is 2π/b, the midline is y = d, and the graph is shifted c to the right. Cosine starts at a maximum; sine starts on the midline going up.',
    types: [{ id: 'eq', L: 'E', name: 'Equation', plural: 'Equations' }, { id: 'graph', L: 'G', name: 'Graph', plural: 'Graphs' }, { id: 'table', L: 'T', name: 'Table', plural: 'Tables' }, { id: 'feat', L: 'D', name: 'Features', plural: 'Features' }],
    units: { 'precalculus-trigonometric-functions': {}, 'algebra2-trigonometric-functions': {} },
    gen: function (rng, L, cfg, Un, sets) {
      var fn = rng.pick(['sin', 'cos']), a = rng.pick(L === 'cp2' ? [1, 2, 3, 0.5] : [1, 2, 3, 0.5, -1, -2]), b = rng.pick(L === 'cp2' ? [1] : L === 'cp1' ? [1, 2, 0.5] : [1, 2, 0.5, 3]);
      var d = rng.int(L === 'cp2' ? -1 : -2, L === 'cp2' ? 1 : 2), j = L === 'honors' ? rng.pick([0, 0, 1, 2, -1]) : 0;
      if (Math.abs(a) + Math.abs(d) > 4) return null;
      var P = 2 * PI / b, c = j * P / 4, cq = j / (2 * b);   // c = cq·π
      var f = function (x) { return a * Math[fn](b * (x - c)) + d; };
      var inner = (b === 1 ? '' : U.tex(b)) + (j === 0 ? 'x' : (b === 1 ? 'x ' + (cq > 0 ? '- ' : '+ ') + piTex(Math.abs(cq)) : '\\left(x ' + (cq > 0 ? '- ' : '+ ') + piTex(Math.abs(cq)) + '\\right)'));
      var aT = a === 1 ? '' : a === -1 ? '-' : U.tex(a);
      var eq = 'y = ' + aT + '\\' + fn + (j === 0 && b === 1 ? ' x' : j === 0 ? '(' + inner + ')' : '\\left(' + inner + '\\right)') + (d ? (d > 0 ? ' + ' : ' - ') + Math.abs(d) : '');
      // table: one period in quarter steps, starting at the shift
      var base = fn === 'sin' ? [0, 1, 0, -1, 0] : [1, 0, -1, 0, 1], rows = [0, 1, 2, 3, 4].map(function (i) { return [cq + i / (2 * b), a * base[i] + d]; });
      if (!rows.every(function (r) { return U.near(f(r[0] * PI), r[1]); })) return null;   // independent check
      var span = Math.max(2, 2 / b), lo = 0, hi = span * PI, den = b === 2 ? 4 : 2;
      return { fn: fn, a: a, b: b, c: c, cq: cq, d: d, P: P, f: f, eq: eq, rows: rows, w: { lo: lo, hi: hi, den: den } };
    },
    finish: function (sets, rng) {
      var F = ['amp', 'per', 'mid', 'max', 'min', 'yint', 'peak'];
      for (var i = 0; i < sets.length; i++) { sets[i].facts = chooseFacts(sets[i], sets, rng, F, trigFact); if (!sets[i].facts) return false; }
      return true;
    },
    fits: function (t, a, b) {
      if (t === 'eq' || t === 'graph') return sameOn(a.f, b.f, 0, 4 * PI);
      if (t === 'table') return a.rows.every(function (r) { return U.near(b.f(r[0] * PI), r[1]); });
      return !!a.facts && a.facts.every(function (f) { return f.test(b); });
    },
    face: function (s, t, mode) {
      if (t === 'eq') return U.bigTex(s.eq);
      if (t === 'table') return '<table class="mk-tt"><tr><th>' + k('x') + '</th><th>' + k('y') + '</th></tr>' + s.rows.map(function (r) { return '<tr><td>' + k(piTex(r[0])) + '</td><td>' + k(U.tex(r[1])) + '</td></tr>'; }).join('') + '</table>';
      if (t === 'feat') return facesOfFacts(s.facts);
      var w = { xmin: s.w.lo, xmax: s.w.hi, ymin: -5, ymax: 5 };
      return SV.plane({ xmin: w.xmin, xmax: w.xmax, ymin: -5, ymax: 5, xstep: PI / s.w.den, ystep: 1, xpi: s.w.den, xticks: SV.piTicks(w.xmin, w.xmax, s.w.den), xtickEvery: s.w.den === 4 || s.w.hi > 2.1 * PI ? 2 : 1, ylabEvery: 1, items: [{ kind: 'curve', pieces: SV.sample(s.f, w, { n: 400 }) }] }, { big: mode === 'big', w: 380, h: 300 });
    },
    summary: function (s) { return k(s.eq); }
  });
  function trigFact(s, id) {
    var A = Math.abs(s.a);
    if (id === 'amp') return { text: 'Amplitude: ' + U.m(U.tex(A)), test: function (o) { return U.near(Math.abs(o.a), A); } };
    if (id === 'per') return { text: 'Period: ' + U.m(piTex(2 / s.b)), test: function (o) { return U.near(o.P, s.P); } };
    if (id === 'mid') return { text: 'Midline: ' + U.m('y = ' + s.d), test: function (o) { return o.d === s.d; } };
    if (id === 'max') return { text: 'Maximum value: ' + U.m(U.tex(s.d + A)), test: function (o) { return U.near(o.d + Math.abs(o.a), s.d + A); } };
    if (id === 'min') return { text: 'Minimum value: ' + U.m(U.tex(s.d - A)), test: function (o) { return U.near(o.d - Math.abs(o.a), s.d - A); } };
    if (id === 'yint') { var y0 = s.f(0); if (!U.isInt(y0 * 2)) return null; return { text: U.m('y') + '-intercept: ' + U.m('(0,\\ ' + U.tex(Math.round(y0 * 2) / 2) + ')'), test: function (o) { return U.near(o.f(0), y0); } }; }
    // first maximum at or to the right of x = 0
    var best = null; for (var i = 0; i < 5; i++) { var x = s.rows[i][0]; if (U.near(s.rows[i][1], s.d + A)) { var xq = x; while (xq < -1e-9) xq += 2 / s.b; while (xq >= 2 / s.b - 1e-9) xq -= 2 / s.b; best = xq; break; } }
    if (best === null) return null;
    return { text: 'First maximum to the right of the ' + U.m('y') + '-axis at ' + U.m('x = ' + piTex(best)), test: function (o) { var v = o.f(best * PI); if (!U.near(v, o.d + Math.abs(o.a))) return false; for (var x2 = 0; x2 < best * PI - 1e-6; x2 += 0.01) if (U.near(o.f(x2), o.d + Math.abs(o.a), 1e-4)) return false; return true; } };
  }

  /* ======================= f, f′, f″ ======================= */
  function polyMul(p, q) { var r = new Array(p.length + q.length - 1).fill(0); p.forEach(function (a, i) { q.forEach(function (b, j) { r[i + j] += a * b; }); }); return r; }   // coefficients, constant first
  function polyEval(p, x) { var v = 0; for (var i = p.length - 1; i >= 0; i--) v = v * x + p[i]; return v; }
  function polyInt(p, C) { return [C].concat(p.map(function (a, i) { return a / (i + 1); })); }
  function polyDer(p) { return p.slice(1).map(function (a, i) { return a * (i + 1); }); }
  function signChanges(p, lo, hi) {   // x-values where p changes sign in (lo, hi), from a fine scan refined to 1/4
    var out = [], prev = polyEval(p, lo), step = 1 / 64;
    for (var x = lo + step; x <= hi + 1e-9; x += step) { var v = polyEval(p, x); if (prev !== 0 && v !== 0 && (prev < 0) !== (v < 0)) out.push(Math.round((x - step / 2) * 4) / 4); if (v !== 0) prev = v; }
    return out;
  }
  function interval(lo, hi) { return '(' + (lo === -Infinity ? '-\\infty' : U.tex(lo)) + ',\\ ' + (hi === Infinity ? '\\infty' : U.tex(hi)) + ')'; }
  function signIntervals(p, pts, want) {   // intervals between pts where p has sign want (+1/−1)
    var cuts = [-Infinity].concat(pts).concat([Infinity]), out = [];
    for (var i = 0; i < cuts.length - 1; i++) { var a = cuts[i], b = cuts[i + 1], m = a === -Infinity ? b - 1 : b === Infinity ? a + 1 : (a + b) / 2; if (Math.sign(polyEval(p, m)) === want) out.push([a, b]); }
    return out;
  }
  function autoWin(p, lo, hi) {
    var ys = []; for (var i = 0; i <= 160; i++) ys.push(polyEval(p, lo + (hi - lo) * i / 160));
    var mn = Math.min.apply(null, ys), mx = Math.max.apply(null, ys); if (mx - mn < 1) { mn -= 2; mx += 2; }
    var steps = [0.5, 1, 2, 5, 10, 20, 25, 50, 100], st = steps.filter(function (s) { return (mx - mn) / s <= 9; })[0] || 200;
    var y0 = Math.floor(mn / st) * st - st, y1 = Math.ceil(mx / st) * st + st;
    if (y0 > -st) y0 = -st; if (y1 < st) y1 = st;
    return { xmin: lo, xmax: hi, ymin: y0, ymax: y1, xstep: 1, ystep: st, ylabEvery: (y1 - y0) / st > 10 ? 2 : 1 };
  }
  MK.register({
    id: 'deriv', name: 'Function and Derivative Matching', short: 'f, f′ and f″', noun: 'function', anchor: 'f',
    anchorText: 'Start with each graph of f already in its set', anchorHint: 'Recommended: students find the graphs of f′ and f″ and the description for each f.',
    blurb: 'Match each <b>graph of f</b> to the <b>graph of f′</b>, the <b>graph of f″</b> and a description of how <b>f behaves</b> (increasing or decreasing, local extrema, concavity, inflection points). Look-alike sets share critical points or an inflection point.',
    tip: 'Where f has a local maximum or minimum, f′ crosses zero. Where f is increasing, f′ is above the axis. Where f is concave up, f″ is above the axis, and an inflection point of f is where f″ changes sign.',
    types: [{ id: 'f', L: 'F', name: 'Graph of f', plural: 'f' }, { id: 'fp', L: 'D', name: 'Graph of f′', plural: 'f′' }, { id: 'fpp', L: 'S', name: 'Graph of f″', plural: 'f″' }, { id: 'beh', L: 'B', name: 'Behavior of f', plural: 'Behavior' }],
    units: { 'calculus-derivatives': { types: ['f', 'fp', 'fpp', 'beh'] }, 'calculus-applications-derivatives': {}, 'calculus-ap-review': {} },
    maxSets: 8, setOptions: [4, 6, 8],
    gen: function (rng, L, cfg, Un, sets) {
      var deg = U.wpick(rng, L === 'cp2' ? { 1: 1, 2: 3 } : L === 'cp1' ? { 1: 1, 2: 3, 3: 1 } : { 1: 1, 2: 3, 3: 2 }) | 0;
      var roots = [], used = sets.length && rng.next() < 0.4 ? rng.pick(sets).roots : null;
      for (var i = 0; i < deg; i++) roots.push(used && used[i] !== undefined && rng.next() < 0.7 ? used[i] : rng.int(-3, 3));
      roots.sort(function (a, b) { return a - b; });
      if (deg === 3 && roots[0] === roots[2]) return null;
      var a = rng.pick(deg === 3 ? [0.25, -0.25, 0.5, -0.5] : deg === 2 ? [1, -1, 0.5, -0.5] : [1, -1, 2, -2]);
      var fp = [a]; roots.forEach(function (r) { fp = polyMul(fp, [-r, 1]); });
      var f0 = polyInt(fp, 0), mid = (function () { var ys = []; for (var x = -4; x <= 4; x += 0.1) ys.push(polyEval(f0, x)); return (Math.max.apply(null, ys) + Math.min.apply(null, ys)) / 2; })();
      var f = polyInt(fp, -Math.round(mid)), fpp = polyDer(fp);
      var crit = signChanges(fp, -6, 6), infl = signChanges(fpp, -6, 6);
      if (crit.some(function (x) { return Math.abs(x) > 3.5; }) || infl.some(function (x) { return Math.abs(x) > 3.5; })) return null;
      if (!infl.every(function (x) { return Math.abs(polyEval(fpp, x)) < 1e-9; }) || !crit.every(function (x) { return Math.abs(polyEval(fp, x)) < 1e-9; })) return null;   // printed x-values are exact
      var sig = function (p) { return p.length + ':' + signChanges(p, -6, 6).join(',') + ':' + Math.sign(p[p.length - 1]); };
      return { roots: roots, a: a, f: f, fp: fp, fpp: fpp, crit: crit, infl: infl, sig: { f: sig(fp) + '|' + sig(fpp), fp: sig(fp) + '|' + sig(fpp), fpp: sig(fpp) + (fpp.length === 1 ? ':' + fpp[0] : '') } };
    },
    finish: function (sets, rng) {
      for (var i = 0; i < sets.length; i++) { sets[i].facts = chooseFacts(sets[i], sets, rng, ['inc', 'dec', 'max', 'min', 'cup', 'cdn', 'ip', 'none'], derivFact); if (!sets[i].facts) return false; }
      return true;
    },
    fits: function (t, a, b) {
      if (t === 'beh') return !!a.facts && a.facts.every(function (f) { return f.test(b); });
      return a.sig[t] === b.sig[t];
    },
    face: function (s, t, mode) {
      if (t === 'beh') return facesOfFacts(s.facts);
      var p = t === 'f' ? s.f : t === 'fp' ? s.fp : s.fpp, w = autoWin(p, -4, 4);
      return SV.plane({ xmin: -4, xmax: 4, ymin: w.ymin, ymax: w.ymax, xstep: 1, ystep: w.ystep, ylabEvery: w.ylabEvery, lab: ['x', t === 'f' ? 'y = f(x)' : t === 'fp' ? 'y = f′(x)' : 'y = f″(x)'], items: [{ kind: 'curve', pieces: SV.sample(function (x) { return polyEval(p, x); }, w, { n: 300 }), color: t === 'f' ? SV.colors.blue : t === 'fp' ? SV.colors.orange : SV.colors.purple }] }, { big: mode === 'big' });
    },
    summary: function (s) { return s.crit.length ? 'critical points at ' + k('x = ' + s.crit.map(U.tex).join(',\\ ')) : 'no critical points'; }
  });
  function derivFact(s, id) {
    var list = function (iv) { return iv.map(function (r) { return interval(r[0], r[1]); }).join(' \\text{ and } '); };
    var same = function (a, b) { return JSON.stringify(a) === JSON.stringify(b); };
    var maxs = s.crit.filter(function (x) { return polyEval(s.fp, x - 0.01) > 0 && polyEval(s.fp, x + 0.01) < 0; }), mins = s.crit.filter(function (x) { return polyEval(s.fp, x - 0.01) < 0 && polyEval(s.fp, x + 0.01) > 0; });
    var M = function (o) { return o.crit.filter(function (x) { return polyEval(o.fp, x - 0.01) > 0 && polyEval(o.fp, x + 0.01) < 0; }); }, Mn = function (o) { return o.crit.filter(function (x) { return polyEval(o.fp, x - 0.01) < 0 && polyEval(o.fp, x + 0.01) > 0; }); };
    if (id === 'inc') { var iv = signIntervals(s.fp, s.crit, 1); if (!iv.length) return null; return { text: U.m('f') + ' is increasing on ' + U.m(list(iv)) + '.', test: function (o) { return same(signIntervals(o.fp, o.crit, 1), iv); } }; }
    if (id === 'dec') { var dv = signIntervals(s.fp, s.crit, -1); if (!dv.length) return null; return { text: U.m('f') + ' is decreasing on ' + U.m(list(dv)) + '.', test: function (o) { return same(signIntervals(o.fp, o.crit, -1), dv); } }; }
    if (id === 'max') { if (!maxs.length) return { text: U.m('f') + ' has no local maximum.', test: function (o) { return !M(o).length; } }; return { text: U.m('f') + ' has a local maximum at ' + U.m('x = ' + maxs.map(U.tex).join(' \\text{ and } x = ')) + '.', test: function (o) { return same(M(o), maxs); } }; }
    if (id === 'min') { if (!mins.length) return { text: U.m('f') + ' has no local minimum.', test: function (o) { return !Mn(o).length; } }; return { text: U.m('f') + ' has a local minimum at ' + U.m('x = ' + mins.map(U.tex).join(' \\text{ and } x = ')) + '.', test: function (o) { return same(Mn(o), mins); } }; }
    if (id === 'cup') { var cu = s.fpp.length === 1 ? (s.fpp[0] > 0 ? [[-Infinity, Infinity]] : []) : signIntervals(s.fpp, s.infl, 1); if (!cu.length) return null; return { text: U.m('f') + ' is concave up on ' + U.m(list(cu)) + '.', test: function (o) { return same(o.fpp.length === 1 ? (o.fpp[0] > 0 ? [[-Infinity, Infinity]] : []) : signIntervals(o.fpp, o.infl, 1), cu); } }; }
    if (id === 'cdn') { var cd = s.fpp.length === 1 ? (s.fpp[0] < 0 ? [[-Infinity, Infinity]] : []) : signIntervals(s.fpp, s.infl, -1); if (!cd.length) return null; return { text: U.m('f') + ' is concave down on ' + U.m(list(cd)) + '.', test: function (o) { return same(o.fpp.length === 1 ? (o.fpp[0] < 0 ? [[-Infinity, Infinity]] : []) : signIntervals(o.fpp, o.infl, -1), cd); } }; }
    if (id === 'ip') { if (!s.infl.length) return { text: U.m('f') + ' has no inflection points.', test: function (o) { return !o.infl.length; } }; return { text: U.m('f') + ' has an inflection point at ' + U.m('x = ' + s.infl.map(U.tex).join(' \\text{ and } x = ')) + '.', test: function (o) { return same(o.infl, s.infl); } }; }
    if (id === 'none' && !s.crit.length) return { text: U.m("f'") + ' never changes sign, so ' + U.m('f') + ' has no local maximum or minimum.', test: function (o) { return !o.crit.length; } };
    return null;
  }

  /* ======================= CONIC SECTIONS ======================= */
  function rad(n) {   // √n in simplest radical form, as TeX
    if (n < 0) return null; var out = 1, inn = n;
    for (var f = 2; f * f <= inn; f++) while (inn % (f * f) === 0) { inn /= f * f; out *= f; }
    return inn === 1 ? String(out) : (out === 1 ? '' : out) + '\\sqrt{' + inn + '}';
  }
  function shiftTex(v, h) { return h === 0 ? v + '^2' : '(' + v + (h > 0 ? ' - ' + h : ' + ' + (-h)) + ')^2'; }
  function pt(x, y) { return '(' + x + ',\\ ' + y + ')'; }
  function genTex(c) {   // Ax² + Cy² + Dx + Ey + F = 0
    var g = c.reduce(function (a, b) { return U.gcd(a, Math.round(b)); }, 0) || 1, lead = c.find(function (v) { return v !== 0; }) < 0 ? -1 : 1;
    var v = c.map(function (x) { return Math.round(x) / g * lead; }), names = ['x^2', 'y^2', 'x', 'y', ''], s = '';
    v.forEach(function (a, i) { if (!a) return; var abs = Math.abs(a), body = (abs === 1 && names[i] ? '' : abs) + names[i]; s += s ? (a < 0 ? ' - ' : ' + ') + body : (a < 0 ? '-' : '') + body; });
    return s + ' = 0';
  }
  MK.register({
    id: 'conic', name: 'Conic Section Matching', short: 'Conic Sections', noun: 'conic', anchor: 'std',
    anchorText: 'Start with each standard-form equation already in its set', anchorHint: 'Recommended: students graph each conic and complete the square to match the general form.',
    blurb: 'Match each conic’s <b>standard-form equation</b> to its <b>graph</b>, its <b>general-form equation</b> and its <b>features</b> (center or vertex, radius, vertices, foci, directrix). Look-alikes share a center or swap the axes.',
    tip: 'Complete the square in the general form to find the center (h, k). For an ellipse a² is the larger denominator; for a hyperbola the positive term tells the direction. Foci: c² = a² − b² (ellipse), c² = a² + b² (hyperbola).',
    fams: { circle: 'Circles', parabola: 'Parabolas', ellipse: 'Ellipses', hyperbola: 'Hyperbolas' }, famLabel: 'Conic types',
    types: [{ id: 'std', L: 'E', name: 'Standard form', plural: 'Standard form' }, { id: 'graph', L: 'G', name: 'Graph', plural: 'Graphs' }, { id: 'gen', L: 'Q', name: 'General form', plural: 'General form' }, { id: 'feat', L: 'D', name: 'Features', plural: 'Features' }],
    units: { 'precalculus-conics': { fams: ['circle', 'parabola', 'ellipse', 'hyperbola'], def: ['circle', 'parabola', 'ellipse', 'hyperbola'] }, 'algebra2-conic-sections': { fams: ['circle', 'parabola', 'ellipse', 'hyperbola'], def: ['circle', 'parabola', 'ellipse', 'hyperbola'] } },
    maxSets: 8, setOptions: [4, 6, 8],
    gen: function (rng, L, cfg, Un, sets) {
      var fam = rng.pick(cfg.fams), twin = sets.length && rng.next() < 0.4 ? rng.pick(sets) : null;
      var h = twin ? twin.h : rng.int(-3, 3), kk = twin ? twin.k : rng.int(-3, 3), c = { fam: fam, h: h, k: kk }, sq = [1, 4, 9, 16, 25];
      if (fam === 'circle') { c.r = rng.int(1, 5); c.std = shiftTex('x', h) + ' + ' + shiftTex('y', kk) + ' = ' + c.r * c.r; c.gen = [1, 1, -2 * h, -2 * kk, h * h + kk * kk - c.r * c.r]; c.sig = 'C' + h + ',' + kk + ',' + c.r; }
      else if (fam === 'parabola') {
        c.vert = rng.next() < 0.5; c.p = rng.pick(L === 'cp2' ? [1, -1, 2, -2] : [0.25, -0.25, 0.5, -0.5, 1, -1, 2, -2]); var fp = 4 * c.p;
        c.std = c.vert ? shiftTex('x', h) + ' = ' + (fp === 1 ? '' : fp === -1 ? '-' : U.tex(fp)) + (kk ? '(y ' + (kk > 0 ? '- ' + kk : '+ ' + -kk) + ')' : 'y') : shiftTex('y', kk) + ' = ' + (fp === 1 ? '' : fp === -1 ? '-' : U.tex(fp)) + (h ? '(x ' + (h > 0 ? '- ' + h : '+ ' + -h) + ')' : 'x');
        c.gen = c.vert ? [1, 0, -2 * h, -fp, h * h + fp * kk] : [0, 1, -fp, -2 * kk, kk * kk + fp * h]; c.sig = 'P' + c.vert + h + ',' + kk + ',' + c.p;
      } else {
        var A = rng.pick(L === 'cp2' ? [4, 9, 16] : sq), B = rng.pick(L === 'cp2' ? [1, 4, 9] : sq); if (A === B) return null;
        c.A = A; c.B = B; c.horiz = fam === 'ellipse' ? A > B : rng.next() < 0.5;
        if (fam === 'ellipse') { c.std = '\\frac{' + shiftTex('x', h) + '}{' + A + '} + \\frac{' + shiftTex('y', kk) + '}{' + B + '} = 1'; c.gen = [B, A, -2 * B * h, -2 * A * kk, B * h * h + A * kk * kk - A * B]; }
        else if (c.horiz) { c.std = '\\frac{' + shiftTex('x', h) + '}{' + A + '} - \\frac{' + shiftTex('y', kk) + '}{' + B + '} = 1'; c.gen = [B, -A, -2 * B * h, 2 * A * kk, B * h * h - A * kk * kk - A * B]; }
        else { c.std = '\\frac{' + shiftTex('y', kk) + '}{' + A + '} - \\frac{' + shiftTex('x', h) + '}{' + B + '} = 1'; c.gen = [-A, B, 2 * A * h, -2 * B * kk, B * kk * kk - A * h * h - A * B]; }
        if (Math.sqrt(Math.max(A, B)) + Math.max(Math.abs(h), Math.abs(kk)) > 7.5) return null;
        c.sig = fam[0] + c.horiz + h + ',' + kk + ',' + A + ',' + B;
      }
      // independent check: points of the curve satisfy both printed forms
      var pts = conicPoints(c);
      if (!pts.length || !pts.every(function (p) { return U.near(c.gen[0] * p[0] * p[0] + c.gen[1] * p[1] * p[1] + c.gen[2] * p[0] + c.gen[3] * p[1] + c.gen[4], 0, 1e-6); })) return null;
      c.attr = conicAttr(c);
      return c;
    },
    finish: function (sets, rng) {
      for (var i = 0; i < sets.length; i++) { sets[i].facts = chooseFacts(sets[i], sets, rng, Object.keys(sets[i].attr), function (s, id) { var a = s.attr[id]; return a ? { text: a.text, test: function (o) { return !!o.attr[id] && o.attr[id].val === a.val; } } : null; }); if (!sets[i].facts) return false; }
      return true;
    },
    fits: function (t, a, b) { if (t === 'feat') return !!a.facts && a.facts.every(function (f) { return f.test(b); }); return a.sig === b.sig; },
    face: function (s, t, mode) {
      if (t === 'std') return U.bigTex(s.std, true);
      if (t === 'gen') return U.bigTex(genTex(s.gen));
      if (t === 'feat') return facesOfFacts(s.facts);
      var items = conicPieces(s).map(function (pc) { return { kind: 'curve', pts: pc }; });
      if (s.fam === 'hyperbola') { var sl = s.horiz ? Math.sqrt(s.B / s.A) : Math.sqrt(s.A / s.B); [sl, -sl].forEach(function (m) { items.push({ kind: 'curve', pieces: SV.sample(function (x) { return s.k + m * (x - s.h); }, { xmin: -8, xmax: 8, ymin: -8, ymax: 8 }, { n: 40 }), color: '#64748b', w: 1.6, dash: '6 5' }); }); }
      return SV.plane({ xmin: -8, xmax: 8, ymin: -8, ymax: 8, xstep: 1, ystep: 1, items: items }, { big: mode === 'big' });
    },
    summary: function (s) { return k(s.std); }
  });
  function conicPoints(c) {
    var out = [];
    for (var i = 0; i < 24; i++) {
      var t = i / 24 * 2 * PI, u = (i - 12) / 6;
      if (c.fam === 'circle') out.push([c.h + c.r * Math.cos(t), c.k + c.r * Math.sin(t)]);
      else if (c.fam === 'ellipse') out.push([c.h + Math.sqrt(c.A) * Math.cos(t), c.k + Math.sqrt(c.B) * Math.sin(t)]);
      else if (c.fam === 'parabola') out.push(c.vert ? [c.h + u * 3, c.k + u * u * 9 / (4 * c.p)] : [c.h + u * u * 9 / (4 * c.p), c.k + u * 3]);
      else { var ch = Math.cosh(u), sh = Math.sinh(u), sg = i % 2 ? 1 : -1; out.push(c.horiz ? [c.h + sg * Math.sqrt(c.A) * ch, c.k + Math.sqrt(c.B) * sh] : [c.h + Math.sqrt(c.B) * sh, c.k + sg * Math.sqrt(c.A) * ch]); }
    }
    return out;
  }
  function conicPieces(c) {
    var clip = function (pts) { var out = [], cur = []; pts.forEach(function (p) { if (Math.abs(p[0]) <= 8.05 && Math.abs(p[1]) <= 8.05) cur.push(p); else if (cur.length) { out.push(cur); cur = []; } }); if (cur.length) out.push(cur); return out.filter(function (x) { return x.length > 1; }); };
    var N = 240, i, pts = [];
    if (c.fam === 'circle' || c.fam === 'ellipse') { var rx = c.fam === 'circle' ? c.r : Math.sqrt(c.A), ry = c.fam === 'circle' ? c.r : Math.sqrt(c.B); for (i = 0; i <= N; i++) { var t = i / N * 2 * PI; pts.push([c.h + rx * Math.cos(t), c.k + ry * Math.sin(t)]); } return clip(pts); }
    if (c.fam === 'parabola') { for (i = 0; i <= N; i++) { var u = -10 + 20 * i / N; pts.push(c.vert ? [c.h + u, c.k + u * u / (4 * c.p)] : [c.h + u * u / (4 * c.p), c.k + u]); } return clip(pts); }
    var a = Math.sqrt(c.A), b = Math.sqrt(c.B), br = [[], []];
    for (i = 0; i <= N; i++) { var v = -3.2 + 6.4 * i / N, ch = Math.cosh(v), sh = Math.sinh(v); if (c.horiz) { br[0].push([c.h + a * ch, c.k + b * sh]); br[1].push([c.h - a * ch, c.k + b * sh]); } else { br[0].push([c.h + b * sh, c.k + a * ch]); br[1].push([c.h + b * sh, c.k - a * ch]); } }
    return clip(br[0]).concat(clip(br[1]));
  }
  /* features of a conic: { id: { text, val } } — val is compared across sets */
  function conicAttr(c) {
    var o = {}, h = c.h, kk = c.k, P = function (x, y) { return U.m(pt(x, y)); };
    if (c.fam === 'circle') { o.type = { text: 'Circle', val: 'circle' }; o.center = { text: 'Center ' + P(h, kk), val: h + ',' + kk }; o.r = { text: 'Radius ' + U.m(c.r), val: 'r' + c.r }; o.top = { text: 'Highest point ' + P(h, kk + c.r), val: 'top' + h + ',' + (kk + c.r) }; return o; }
    if (c.fam === 'parabola') {
      var p = c.p, fx = c.vert ? h : h + p, fy = c.vert ? kk + p : kk;
      o.type = { text: 'Parabola that opens ' + (c.vert ? (p > 0 ? 'up' : 'down') : (p > 0 ? 'right' : 'left')), val: 'par' + c.vert + (p > 0) };
      o.vertex = { text: 'Vertex ' + P(h, kk), val: 'v' + h + ',' + kk };
      o.focus = { text: 'Focus ' + U.m(pt(U.tex(fx), U.tex(fy))), val: 'f' + fx + ',' + fy };
      o.dir = { text: 'Directrix ' + U.m(c.vert ? 'y = ' + U.tex(kk - p) : 'x = ' + U.tex(h - p)), val: 'd' + c.vert + (c.vert ? kk - p : h - p) };
      return o;
    }
    var A = c.A, B = c.B, a = Math.sqrt(Math.max(A, B)), cc = c.fam === 'ellipse' ? Math.abs(A - B) : A + B, horiz = c.fam === 'ellipse' ? A > B : c.horiz;
    var ax = c.fam === 'ellipse' ? a : Math.sqrt(A);
    o.type = { text: c.fam === 'ellipse' ? 'Ellipse with a ' + (horiz ? 'horizontal' : 'vertical') + ' major axis' : 'Hyperbola that opens ' + (horiz ? 'left and right' : 'up and down'), val: c.fam + horiz };
    o.center = { text: 'Center ' + P(h, kk), val: h + ',' + kk };
    o.verts = { text: 'Vertices ' + (horiz ? P(h - ax, kk) + ' and ' + P(h + ax, kk) : P(h, kk - ax) + ' and ' + P(h, kk + ax)), val: 'V' + horiz + (horiz ? (h - ax) + ',' + (h + ax) + ',' + kk : (kk - ax) + ',' + (kk + ax) + ',' + h) };
    var r = rad(cc), fs = horiz ? [pt(h + ' - ' + r, kk), pt(h + ' + ' + r, kk)] : [pt(h, kk + ' - ' + r), pt(h, kk + ' + ' + r)];
    if (/sqrt/.test(r) === false) fs = horiz ? [pt(h - Math.sqrt(cc), kk), pt(h + Math.sqrt(cc), kk)] : [pt(h, kk - Math.sqrt(cc)), pt(h, kk + Math.sqrt(cc))];
    o.foci = { text: 'Foci ' + U.m(fs[0]) + ' and ' + U.m(fs[1]), val: 'F' + horiz + h + ',' + kk + ',' + cc };
    if (c.fam === 'hyperbola') { var m = horiz ? rad(B) + '/' + rad(A) : rad(A) + '/' + rad(B), sl = horiz ? Math.sqrt(B / A) : Math.sqrt(A / B); o.asym = { text: 'Asymptote slopes ' + U.m('\\pm ' + U.tex(sl)), val: 'S' + sl.toFixed(5) }; }
    else { o.minor = { text: 'Length of the minor axis ' + U.m(U.tex(2 * Math.sqrt(Math.min(A, B)))), val: 'm' + Math.min(A, B) }; }
    return o;
  }
})(typeof window !== 'undefined' ? window : globalThis);
