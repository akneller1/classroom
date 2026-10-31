/* Printable Generators — Matching Card Sort engine (no DOM).
   Students sort cards into sets: the GRAPH, EQUATION, TABLE and DESCRIPTION of the same function.
   Only units that study families of functions offer it (PR.MATCH.UNITS); every other unit shows it greyed out.
   Every card is checked to fit exactly one set:
     - graphs: every other function differs by more than half a grid unit somewhere on the visible curve;
     - tables: every other function misses at least one row;
     - descriptions: every fact is true of its own function (computed from its parameters), and every other
       function fails at least one fact;
     - equations: no two functions are the same function.
   Needs: core/rng.js, menu/printables.js (PR namespace). */
(function (G) {
  'use strict';
  var NS = G.MKMENU, WS = G.MKWS, PR = NS.printables = NS.printables || {};
  var M = PR.MATCH = {};
  function rngOf() { return WS.rng.make(WS.rng.hash([].slice.call(arguments).join('|'))); }

  /* ---------------- units ---------------- */
  M.FAMILIES = {
    linear: 'Linear', quadratic: 'Quadratic', absolute: 'Absolute value', sqrt: 'Square root', exponential: 'Exponential',
    log: 'Logarithmic', rational: 'Rational (reciprocal)', cubic: 'Cubic polynomial', arith: 'Arithmetic sequence', geom: 'Geometric sequence'
  };
  M.UNITS = {
    'algebra1-linear-equations-slope': { fams: ['linear'], def: ['linear'] },
    'algebra1-exponential-functions': { fams: ['exponential', 'linear'], def: ['exponential'] },
    'algebra1-quadratics': { fams: ['quadratic'], def: ['quadratic'] },
    'algebra2-functions-transformations': { fams: ['quadratic', 'absolute', 'sqrt'], def: ['quadratic', 'absolute', 'sqrt'], a2: true, xform: true },
    'algebra2-linear-functions-systems': { fams: ['linear'], def: ['linear'], a2: true },
    'algebra2-quadratic-functions-complex-numbers': { fams: ['quadratic'], def: ['quadratic'], a2: true },
    'algebra2-polynomial-functions': { fams: ['cubic', 'quadratic'], def: ['cubic'], a2: true },
    'algebra2-radicals-rational-exponents': { fams: ['sqrt'], def: ['sqrt'], a2: true, ratexp: true },
    'algebra2-exponential-logarithmic-functions': { fams: ['exponential', 'log'], def: ['exponential', 'log'], a2: true },
    'algebra2-rational-functions': { fams: ['rational'], def: ['rational'], a2: true },
    'algebra2-sequences-series': { fams: ['arith', 'geom'], def: ['arith', 'geom'], a2: true }
  };
  M.supported = function (unitId) { return !!M.UNITS[unitId]; };
  M.familiesFor = function (unitId) { return M.UNITS[unitId] ? M.UNITS[unitId].fams.slice() : []; };
  M.defaultFamilies = function (unitId) { var o = {}; (M.UNITS[unitId] ? M.UNITS[unitId].fams : []).forEach(function (f) { o[f] = M.UNITS[unitId].def.indexOf(f) >= 0; }); return o; };
  M.TYPES = [{ id: 'graph', L: 'G', name: 'Graph' }, { id: 'eq', L: 'E', name: 'Equation' }, { id: 'table', L: 'T', name: 'Table' }, { id: 'desc', L: 'D', name: 'Description' }];

  /* ---------------- numbers ---------------- */
  var EPS = 1e-9;
  function near(a, b) { return Math.abs(a - b) < 1e-7; }
  function isInt(v) { return isFinite(v) && Math.abs(v - Math.round(v)) < 1e-9; }
  function gcd(a, b) { a = Math.abs(a); b = Math.abs(b); while (b) { var t = a % b; a = b; b = t; } return a || 1; }
  function Q(n, d) { d = d || 1; if (d < 0) { n = -n; d = -d; } var g = gcd(n, d); return { n: n / g, d: d / g, v: n / d }; }
  function toQ(v) { for (var d = 1; d <= 64; d++) { var n = Math.round(v * d); if (Math.abs(n / d - v) < 1e-9) return Q(n, d); } return null; }
  /* a number as TeX: integer, simple fraction, or a 2-place decimal */
  function nt(v) {
    if (isInt(v)) return String(Math.round(v));
    var q = toQ(v); if (q && q.d <= 32) return (q.n < 0 ? '-' : '') + '\\frac{' + Math.abs(q.n) + '}{' + q.d + '}';
    return String(Math.round(v * 100) / 100);
  }
  function nice(v) { var q = toQ(v); return !!q && q.d <= 4; }
  function pt(x, y) { return '(' + nt(x) + ', ' + nt(y) + ')'; }
  function m(s) { return '⟨' + s + '⟩'; }
  function coef(a) { return near(a, 1) ? '' : near(a, -1) ? '-' : nt(a); }   // a number in front of a factor
  function kTerm(k) { return near(k, 0) ? '' : k > 0 ? ' + ' + nt(k) : ' - ' + nt(-k); }
  function sh(h, v) { v = v || 'x'; return near(h, 0) ? v : h > 0 ? v + ' - ' + nt(h) : v + ' + ' + nt(-h); }
  function par(h) { return near(h, 0) ? 'x' : '(' + sh(h) + ')'; }
  function poly(terms) {   // [[coef, 'x^{2}'], ...]
    var out = '';
    terms.forEach(function (t) {
      var c = t[0], v = t[1]; if (near(c, 0)) return;
      var a = Math.abs(c), body = v && near(a, 1) ? v : nt(a) + (v || '');
      out += out ? (c < 0 ? ' - ' : ' + ') + body : (c < 0 ? '-' : '') + body;
    });
    return out || '0';
  }
  function feq(a, b) {
    if (a === null || a === undefined || b === null || b === undefined) return false;
    if (typeof a === 'number' || typeof b === 'number') return typeof a === 'number' && typeof b === 'number' && near(a, b);
    if (Array.isArray(a) || Array.isArray(b)) return Array.isArray(a) && Array.isArray(b) && a.length === b.length && a.every(function (x, i) { return feq(x, b[i]); });
    return a === b;
  }
  M.feq = feq;
  function pickW(rng, w) { var tot = 0, k; for (k in w) tot += w[k]; var r = rng.next() * tot; for (k in w) { r -= w[k]; if (r < 0) return k; } return Object.keys(w)[0]; }
  function inRange(lo, hi) { return function (v) { return v >= lo && v <= hi; }; }

  /* ---------------- graphs, tables ---------------- */
  /* Visible pieces of y = f(x), clipped to the window (breaks at vertical asymptotes). */
  function curves(f, w, breaks) {
    var out = [], cur = null, prev = null, step = (w.xmax - w.xmin) / 600;
    for (var i = 0; i <= 600; i++) {
      var x = w.xmin + i * step, y = f(x);
      if (prev && (breaks || []).some(function (b) { return b > prev[0] - EPS && b < x + EPS; })) { if (cur) out.push(cur); cur = null; prev = null; }
      var inside = isFinite(y) && y >= w.ymin && y <= w.ymax;
      if (inside) {
        if (!cur) { cur = []; if (prev && isFinite(prev[1])) cur.push(edge(prev, [x, y], w)); }
        cur.push([x, y]);
      } else if (cur) { if (isFinite(y)) cur.push(edge([x, y], cur[cur.length - 1], w)); out.push(cur); cur = null; }
      prev = [x, y];
    }
    if (cur) out.push(cur);
    return out.filter(function (c) { return c.length > 1; });
  }
  function edge(o, p, w) { var yb = o[1] > w.ymax ? w.ymax : w.ymin, t = (yb - p[1]) / (o[1] - p[1]); return [p[0] + t * (o[0] - p[0]), yb]; }
  function lattice(fn) {
    var w = fn.graph, out = [];
    for (var x = Math.ceil(w.xmin) + 1; x <= w.xmax - 1; x++) { var y = fn.f(x); if (isInt(y) && y > w.ymin + 0.4 && y < w.ymax - 0.4) out.push([x, Math.round(y)]); }
    return out;
  }
  /* a 12 × 12 window around the features that matter */
  function win(ylo, yhi) {
    var lo = Math.min(-2, Math.floor(ylo) - 1), hi = Math.max(2, Math.ceil(yhi) + 1);
    if (hi - lo > 12) return null;
    while (hi - lo < 12) { if (hi < 6 && (lo <= -6 || hi - 0 < 0 - lo)) hi++; else lo--; }
    return { xmin: -6, xmax: 6, ymin: lo, ymax: hi, xstep: 1, ystep: 1, lab: ['x', 'y'] };
  }
  function finishGraph(fn, breaks, dots, asym) {
    var w = fn.graph;
    w.curves = fn.discrete ? [] : curves(fn.f, w, breaks);
    var lat = lattice(fn);
    w.dots = (dots || []).filter(function (d) { return d[0] > w.xmin && d[0] < w.xmax && d[1] > w.ymin && d[1] < w.ymax; });
    w.asym = asym || [];
    return lat;
  }
  function tableOf(fn, xs) {
    var rows = xs.map(function (x) { return [x, fn.f(x)]; });
    if (!rows.every(function (r) { return isFinite(r[1]); })) return null;
    fn.table = { head: fn.discrete ? ['n', 'a_{n}'] : ['x', 'y'], rows: rows };
    return fn.table;
  }
  function tableNice(rows, allowFrac) { return rows.every(function (r) { return allowFrac ? nice(r[1]) && Math.abs(r[1]) < 1000 : isInt(r[1]) && Math.abs(r[1]) < 1000; }); }

  /* ---------------- facts ---------------- */
  function fact(key, val, text) { return { key: key, text: text, test: function (g) { return feq(g.feats[key], val); } }; }
  function ptFact(key, x, y, text) { return { key: key, text: text || 'It passes through ' + m(pt(x, y)) + '.', x: x, y: y, test: function (g) { var v = g.f(x); return isFinite(v) && near(v, y); } }; }
  /* points on the graph other than the ones already named */
  function ptFacts(fn, F, avoidX, rng, text) {
    var used = {}; (avoidX || []).forEach(function (x) { used[nt(x)] = 1; });
    var cand = rng.shuffle(lattice(fn).filter(function (p) { return !used[nt(p[0])] && Math.abs(p[0]) <= 5; }));
    cand.slice(0, 2).forEach(function (p, i) { F['pt' + i] = ptFact('pt' + i, p[0], p[1], text ? text(p) : null); });
  }
  function xintText(xs) {
    if (!xs.length) return 'It does not cross the ' + m('x') + '-axis.';
    if (xs.length === 1) return 'Its ' + m('x') + '-intercept is ' + m(pt(xs[0], 0)) + '.';
    return 'Its ' + m('x') + '-intercepts are ' + xs.map(function (x) { return m(pt(x, 0)); }).join(' and ') + '.';
  }
  function yintFact(fn) { var c = fn.f(0); return isFinite(c) && nice(c) ? fact('yint', c, 'Its ' + m('y') + '-intercept is ' + m(pt(0, c)) + '.') : null; }
  function xintsFact(fn) { var xs = fn.feats.xints; return Array.isArray(xs) && xs.every(nice) && xs.every(inRange(-9, 9)) ? fact('xints', xs, xintText(xs)) : null; }
  function rangeTex(r) { return r === 'all' ? '\\text{all real numbers}' : 'y ' + { ge: '\\ge', le: '\\le', gt: '>', lt: '<', ne: '\\ne' }[r[0]] + ' ' + nt(r[1]); }
  function domTex(d) { return d === 'all' ? '\\text{all real numbers}' : 'x ' + { ge: '\\ge', le: '\\le', gt: '>', lt: '<', ne: '\\ne' }[d[0]] + ' ' + nt(d[1]); }
  function base(fam) { return { fam: fam, feats: { fam: fam, yint: null, xints: null, mono: 'none', domain: 'all', range: 'all', vertex: null, opens: null, minmax: null, axis: null, slope: null, factor: null, growth: null, asymH: null, asymV: null, zeros: null, end: null, start: null, rslope: null, quads: null, diff: null, ratio: null, xform: null } }; }

  /* transformation wording (Functions & Transformations) */
  var PARENT = { quadratic: 'y = x^{2}', absolute: 'y = |x|', sqrt: 'y = \\sqrt{x}' };
  function xformText(fam, a, h, k) {
    var bits = [];
    if (a < 0) bits.push('reflected across the ' + m('x') + '-axis');
    if (!near(Math.abs(a), 1)) bits.push((Math.abs(a) > 1 ? 'stretched vertically by a factor of ' : 'compressed vertically by a factor of ') + m(nt(Math.abs(a))));
    if (!near(h, 0)) bits.push('shifted ' + m(nt(Math.abs(h))) + (near(Math.abs(h), 1) ? ' unit ' : ' units ') + (h > 0 ? 'right' : 'left'));
    if (!near(k, 0)) bits.push('shifted ' + m(nt(Math.abs(k))) + (near(Math.abs(k), 1) ? ' unit ' : ' units ') + (k > 0 ? 'up' : 'down'));
    if (!bits.length) return null;
    var last = bits.pop();
    return 'The graph of ' + m(PARENT[fam]) + ' ' + (bits.length ? bits.join(', ') + ' and ' + last : last) + '.';
  }

  /* ---------------- families ---------------- */
  var FAM = {};
  /* Each family: make(rng, L) -> params, twin(rng, L, p) -> similar params, build(p, L, rng) -> fn or null.
     fn: { fam, p, f, eq (TeX), feats, graph, table, facts {key: fact}, combos [[keys]], discrete? } */

  /* ---- linear: y = mx + b ---- */
  FAM.linear = {
    make: function (rng, L) {
      var S = [[1, 1], [2, 1], [3, 1], [-1, 1], [-2, 1], [-3, 1]];
      if (L.id !== 'cp2') S = S.concat([[1, 2], [-1, 2], [1, 3], [-1, 3], [2, 3], [-2, 3], [3, 2], [-3, 2], [4, 1], [-4, 1]]);
      if (L.id === 'honors') S = S.concat([[3, 4], [-3, 4], [4, 3], [-4, 3], [5, 2], [-5, 2], [0, 1]]);
      var s = rng.pick(S);
      return { m: Q(s[0], s[1]).v, b: rng.int(L.id === 'cp2' ? -4 : -5, L.id === 'cp2' ? 4 : 5) };
    },
    twin: function (rng, L, p) {
      var q = { m: p.m, b: p.b }, r = rng.next();
      if (r < 0.45) q.b = p.b + rng.pick([-3, -2, -1, 1, 2, 3]);
      else if (r < 0.8) q.m = -p.m || 1;
      else q.m = near(Math.abs(p.m), 1) ? 2 * p.m : 1 / p.m;
      if (Math.abs(q.b) > 5 || !nice(q.m)) return null;
      return q;
    },
    build: function (p, L, rng, U) {
      var mm = p.m, b = p.b, fn = base('linear');
      fn.p = p; fn.f = function (x) { return mm * x + b; };
      var qd = toQ(mm).d, lv = U.a2 ? (L.id === 'cp2' ? 'cp1' : 'honors') : L.id;
      var form = pickW(rng, lv === 'cp2' ? { si: 1 } : lv === 'cp1' ? { si: 7, std: 3 } : { si: 4, ps: 3, std: 3 });
      if (near(mm, 0)) form = 'si';
      if (form === 'si') fn.eq = 'y = ' + poly([[mm, 'x'], [b, '']]);
      else if (form === 'std') {
        var qm = toQ(mm), A = -qm.n, B = qm.d, C = qm.d * b; if (A < 0) { A = -A; B = -B; C = -C; }
        fn.eq = poly([[A, 'x'], [B, 'y']]) + ' = ' + C;
      } else {
        var xs = [-4, -3, -2, 2, 3, 4].filter(function (x) { return isInt(mm * x + b) && Math.abs(mm * x + b) <= 9; });
        if (!xs.length) fn.eq = 'y = ' + poly([[mm, 'x'], [b, '']]);
        else { var x1 = rng.pick(xs), y1 = mm * x1 + b; fn.eq = sh(y1, 'y') + ' = ' + (near(mm, 1) ? sh(x1) : near(mm, -1) ? '-(' + sh(x1) + ')' : nt(mm) + '(' + sh(x1) + ')'); }
      }
      var F = fn.feats; F.slope = mm; F.yint = b; F.xints = near(mm, 0) ? [] : [-b / mm]; F.mono = mm > 0 ? 'inc' : mm < 0 ? 'dec' : 'const'; F.range = near(mm, 0) ? ['eq', b] : 'all';
      fn.graph = win(-5, 5);
      var lat = finishGraph(fn, null, []);
      if (lat.length < 3) return null;
      var yl = lat.filter(function (q) { return q[0] === 0; })[0], far = lat.filter(function (q) { return q[0] !== 0; }).sort(function (a, c) { return Math.abs(c[0]) - Math.abs(a[0]); });
      fn.graph.dots = [yl || lat[0], far[Math.min(far.length - 1, 1)]].filter(Boolean);
      // table: x = multiples of the slope's denominator
      var step = qd * (L.id === 'honors' && qd === 1 && rng.next() < 0.4 ? 2 : 1), st = rng.pick([-2, -1, 0]);
      if (!tableOf(fn, [0, 1, 2, 3, 4].map(function (i) { return (st + i) * step; })) || !tableNice(fn.table.rows)) return null;
      var Fs = {};
      var sl = near(mm, 0) ? 'The slope is ' + m('0') + '.' : rng.pick(L.id === 'cp2' && isInt(mm) ? ['The slope is ' + m(nt(mm)) + '.', m('y') + (mm > 0 ? ' goes up ' : ' goes down ') + m(nt(Math.abs(mm))) + ' each time ' + m('x') + ' increases by ' + m('1') + '.'] : ['The slope is ' + m(nt(mm)) + '.', 'The rate of change is ' + m(nt(mm)) + '.']);
      Fs.slope = fact('slope', mm, sl);
      Fs.yint = fact('yint', b, rng.next() < 0.5 ? 'Its ' + m('y') + '-intercept is ' + m(pt(0, b)) + '.' : 'It crosses the ' + m('y') + '-axis at ' + m(pt(0, b)) + '.');
      if (!near(mm, 0) && b !== 0 && nice(-b / mm) && Math.abs(b / mm) <= 8) Fs.xints = fact('xints', [-b / mm], xintText([-b / mm]));
      ptFacts(fn, Fs, [0].concat(F.xints), rng);
      fn.facts = Fs;
      fn.combos = L.id === 'cp2' ? [['slope', 'yint'], ['slope', 'yint'], ['slope', 'pt0']] : [['slope', 'yint'], ['slope', 'pt0'], ['yint', 'pt0'], ['xints', 'yint'], ['pt0', 'pt1']];
      return fn;
    }
  };

  /* ---- quadratic: y = a(x - h)^2 + k ---- */
  FAM.quadratic = {
    make: function (rng, L, U) {
      var As = L.id === 'cp2' ? [1, -1] : L.id === 'cp1' ? [1, -1, 2, -2, 0.5, -0.5] : [1, -1, 2, -2, 0.5, -0.5, 3, -3];
      var a = rng.pick(As), lv = U.a2 && L.id === 'cp2' ? 'cp1' : L.id;
      var form = lv === 'cp2' ? 'v' : pickW(rng, { v: 4, s: 3, f: 3 });
      if (form === 'f') {   // integer roots
        var r1 = rng.int(-5, 4), r2 = r1 + rng.int(1, 6);
        if (!isInt(a) && (r2 - r1) % 2 === 0) r2++;
        return { a: a, h: (r1 + r2) / 2, k: -a * Math.pow((r2 - r1) / 2, 2), form: 'f', r: [r1, r2] };
      }
      return { a: a, h: rng.int(-3, 3), k: rng.int(-5, 5), form: form };
    },
    twin: function (rng, L, p) {
      var q = { a: p.a, h: p.h, k: p.k, form: p.form === 'f' ? 'v' : p.form }, r = rng.next();
      if (!isInt(p.h) || !isInt(p.k)) return null;
      if (r < 0.4) q.a = -p.a; else if (r < 0.65 && L.id !== 'cp2') q.a = near(Math.abs(p.a), 1) ? 2 * p.a : p.a / Math.abs(p.a); else if (r < 0.85) q.h = p.h + rng.pick([-2, -1, 1, 2]); else q.k = p.k + rng.pick([-3, -2, 2, 3]);
      if (Math.abs(q.h) > 3 || Math.abs(q.k) > 5) return null;
      return q;
    },
    build: function (p, L, rng, U) {
      var a = p.a, h = p.h, k = p.k, fn = base('quadratic');
      fn.p = p; fn.f = function (x) { return a * (x - h) * (x - h) + k; };
      if (p.form === 'v') { if (!isInt(h) || !isInt(k)) return null; fn.eq = 'y = ' + coef(a) + (near(h, 0) ? 'x^{2}' : '(' + sh(h) + ')^{2}') + kTerm(k); }
      else if (p.form === 's') fn.eq = 'y = ' + poly([[a, 'x^{2}'], [-2 * a * h, 'x'], [a * h * h + k, '']]);
      else fn.eq = 'y = ' + coef(a) + [p.r[0], p.r[1]].sort(function (x, y) { return (x === 0 ? -1 : 0) - (y === 0 ? -1 : 0); }).map(par).join('');
      var F = fn.feats, disc = -k / a;
      F.vertex = [h, k]; F.opens = a > 0 ? 'up' : 'down'; F.minmax = [a > 0 ? 'min' : 'max', k]; F.axis = h; F.yint = fn.f(0);
      F.xints = disc < -EPS ? [] : near(disc, 0) ? [h] : [h - Math.sqrt(disc), h + Math.sqrt(disc)];
      F.zeros = disc < -EPS ? [] : near(disc, 0) ? [[h, 2]] : F.xints.map(function (x) { return [x, 1]; });
      F.end = a > 0 ? 'uu' : 'dd'; F.range = [a > 0 ? 'ge' : 'le', k]; F.shape = near(Math.abs(a), 1) ? 'same' : Math.abs(a) > 1 ? 'narrow' : 'wide';
      if (U.xform) F.xform = 'quadratic|' + a + '|' + h + '|' + k;
      if (Math.abs(h) > 4.5 || Math.abs(k) > 6) return null;
      fn.graph = win(a > 0 ? k : k - 2, a > 0 ? k + 2 : k);
      if (!fn.graph) return null;
      var lat = finishGraph(fn, null, []);
      if (lat.length < 3) return null;
      fn.graph.dots = lat.filter(function (q) { return Math.abs(q[0] - h) <= 2; }).slice(0, 5);
      // table: five x-values around the vertex
      var stp = p.form === 'v' && !isInt(a) ? 2 : 1, c0 = Math.round(h) + (L.id === 'honors' ? rng.int(-1, 1) : 0), xs = [-2, -1, 0, 1, 2].map(function (i) { return c0 + i * stp; });
      if (!tableOf(fn, xs) || !tableNice(fn.table.rows)) return null;
      var Fs = {}, vInt = isInt(h) && isInt(k);
      if (vInt) Fs.vertex = fact('vertex', [h, k], 'Its vertex is ' + m(pt(h, k)) + '.');
      Fs.minmax = fact('minmax', F.minmax, 'Its ' + (a > 0 ? 'minimum' : 'maximum') + ' value is ' + m(nt(k)) + '.');
      Fs.axis = fact('axis', h, 'Its axis of symmetry is ' + m('x = ' + nt(h)) + '.');
      if (nice(F.yint)) Fs.yint = fact('yint', F.yint, 'Its ' + m('y') + '-intercept is ' + m(pt(0, F.yint)) + '.');
      if (F.xints.length === 2 && F.xints.every(isInt)) Fs.xints = fact('xints', F.xints, xintText(F.xints));
      ptFacts(fn, Fs, [h, 0].concat(F.xints), rng);
      var x = U.xform && vInt ? xformText('quadratic', a, h, k) : null; if (x) Fs.xform = fact('xform', F.xform, x);
      fn.facts = Fs;
      fn.combos = [['vertex', 'pt0'], near(h, 0) ? ['vertex', 'pt1'] : ['vertex', 'yint'], F.yint !== 0 ? ['xints', 'yint'] : ['xints', 'pt0'], ['xints', 'minmax'], near(h, 0) ? ['axis', 'minmax', 'pt0'] : ['axis', 'minmax', 'yint']];
      if (L.id === 'cp2') fn.combos = fn.combos.slice(0, 2);
      return fn;
    }
  };

  /* ---- absolute value: y = a|x - h| + k ---- */
  FAM.absolute = {
    make: function (rng, L) { return { a: rng.pick(L.id === 'cp2' ? [1, -1] : [1, -1, 2, -2, 0.5, -0.5]), h: rng.int(-3, 3), k: rng.int(-4, 4) }; },
    twin: function (rng, L, p) { var q = { a: p.a, h: p.h, k: p.k }, r = rng.next(); if (r < 0.4) q.a = -p.a; else if (r < 0.7) q.h = p.h + rng.pick([-2, -1, 1, 2]); else q.k = p.k + rng.pick([-2, -1, 1, 2]); return Math.abs(q.h) <= 3 && Math.abs(q.k) <= 5 ? q : null; },
    build: function (p, L, rng, U) {
      var a = p.a, h = p.h, k = p.k, fn = base('absolute');
      fn.p = p; fn.f = function (x) { return a * Math.abs(x - h) + k; };
      fn.eq = 'y = ' + coef(a) + '\\left|' + sh(h) + '\\right|' + kTerm(k);
      var F = fn.feats, d = -k / a;
      F.vertex = [h, k]; F.opens = a > 0 ? 'up' : 'down'; F.minmax = [a > 0 ? 'min' : 'max', k]; F.axis = h; F.yint = fn.f(0); F.rslope = a;
      F.xints = d < -EPS ? [] : near(d, 0) ? [h] : [h - d, h + d]; F.range = [a > 0 ? 'ge' : 'le', k];
      if (U.xform) F.xform = 'absolute|' + a + '|' + h + '|' + k;
      fn.graph = win(a > 0 ? k : k - 2, a > 0 ? k + 2 : k); if (!fn.graph) return null;
      var lat = finishGraph(fn, null, []); if (lat.length < 3) return null;
      fn.graph.dots = lat.filter(function (q) { return Math.abs(q[0] - h) <= 2; });
      var stp = isInt(a) ? 1 : 2, c0 = h + (L.id === 'honors' ? rng.int(-1, 1) : 0);
      if (!tableOf(fn, [-2, -1, 0, 1, 2].map(function (i) { return c0 + i * stp; })) || !tableNice(fn.table.rows)) return null;
      var Fs = {};
      Fs.vertex = fact('vertex', [h, k], 'Its vertex is ' + m(pt(h, k)) + '.');
      Fs.rslope = fact('rslope', a, 'To the right of the vertex, the graph has slope ' + m(nt(a)) + '.');
      Fs.minmax = fact('minmax', F.minmax, 'Its ' + (a > 0 ? 'minimum' : 'maximum') + ' value is ' + m(nt(k)) + '.');
      if (nice(F.yint)) Fs.yint = fact('yint', F.yint, 'Its ' + m('y') + '-intercept is ' + m(pt(0, F.yint)) + '.');
      ptFacts(fn, Fs, [h, 0], rng);
      var x = U.xform ? xformText('absolute', a, h, k) : null; if (x) Fs.xform = fact('xform', F.xform, x);
      fn.facts = Fs;
      fn.combos = [['vertex', 'pt0'], ['vertex', 'rslope'], near(h, 0) ? ['vertex', 'pt1'] : ['vertex', 'yint']];
      return fn;
    }
  };

  /* ---- square root: y = a√(x - h) + k ---- */
  FAM.sqrt = {
    make: function (rng, L) { return { a: rng.pick(L.id === 'cp2' ? [1, -1, 2] : [1, -1, 2, -2, 3, -3]), h: rng.int(-5, 1), k: rng.int(-4, 4) }; },
    twin: function (rng, L, p) { var q = { a: p.a, h: p.h, k: p.k }, r = rng.next(); if (r < 0.4) q.a = -p.a; else if (r < 0.6) q.a = p.a * 2; else if (r < 0.8) q.h = p.h + rng.pick([-2, -1, 1, 2]); else q.k = p.k + rng.pick([-2, -1, 1, 2]); return Math.abs(q.a) <= 4 && q.h >= -5 && q.h <= 2 && Math.abs(q.k) <= 5 ? q : null; },
    build: function (p, L, rng, U) {
      var a = p.a, h = p.h, k = p.k, fn = base('sqrt');
      fn.p = p; fn.f = function (x) { return x < h - EPS ? NaN : a * Math.sqrt(Math.max(0, x - h)) + k; };
      fn.eq = 'y = ' + coef(a) + (U.ratexp && (L.id !== 'cp2') && rng.next() < 0.5 ? par(h) + '^{\\frac{1}{2}}' : '\\sqrt{' + sh(h) + '}') + kTerm(k);
      var F = fn.feats, d = -k / a;
      F.start = [h, k]; F.domain = ['ge', h]; F.range = [a > 0 ? 'ge' : 'le', k]; F.mono = a > 0 ? 'inc' : 'dec';
      F.yint = h <= 0 ? fn.f(0) : null; F.xints = d < -EPS ? [] : [h + d * d];
      if (U.xform) F.xform = 'sqrt|' + a + '|' + h + '|' + k;
      fn.graph = win(a > 0 ? k : k - 4, a > 0 ? k + 4 : k); if (!fn.graph) return null;
      var dots = [0, 1, 4, 9].map(function (d2) { return [h + d2, k + a * Math.sqrt(d2)]; });
      finishGraph(fn, null, dots);
      if (fn.graph.dots.length < 3) return null;
      var ds = L.id === 'honors' ? [0, 1, 4, 9, 16] : [0, 1, 4, 9];
      if (!tableOf(fn, ds.map(function (d2) { return h + d2; })) || !tableNice(fn.table.rows)) return null;
      var Fs = {};
      Fs.start = fact('start', [h, k], 'Its graph starts at ' + m(pt(h, k)) + '.');
      Fs.domain = fact('domain', F.domain, 'Its domain is ' + m(domTex(F.domain)) + '.');
      Fs.range = fact('range', F.range, 'Its range is ' + m(rangeTex(F.range)) + '.');
      if (F.yint !== null && isInt(F.yint)) Fs.yint = fact('yint', F.yint, 'Its ' + m('y') + '-intercept is ' + m(pt(0, F.yint)) + '.');
      Fs.pt0 = ptFact('pt0', h + 1, k + a); Fs.pt1 = ptFact('pt1', h + 4, k + 2 * a);
      var x = U.xform ? xformText('sqrt', a, h, k) : null; if (x) Fs.xform = fact('xform', F.xform, x);
      fn.facts = Fs;
      fn.combos = [['start', 'pt0'], ['start', 'pt1'], ['domain', 'range', 'pt1']];
      return fn;
    }
  };

  /* ---- exponential: y = a·b^x + k ---- */
  FAM.exponential = {
    make: function (rng, L, U) {
      var Bs = L.id === 'cp2' ? [[2, 1], [3, 1], [1, 2]] : [[2, 1], [3, 1], [4, 1], [1, 2], [1, 3]];
      if (L.id === 'honors') Bs = Bs.concat([[3, 2], [2, 3], [1, 4]]);
      var b = rng.pick(Bs), As = L.id === 'cp2' ? [1, 2, 3, 4, 5] : [1, 2, 3, 4, 5, 6, 8];
      var a = rng.pick(As); if (L.id === 'honors' && rng.next() < 0.25) a = -a;
      var kp = L.id === 'cp2' ? 0 : L.id === 'cp1' ? (U.a2 ? 0.5 : 0.3) : 0.5;
      return { a: a, b: Q(b[0], b[1]).v, k: rng.next() < kp ? rng.pick([-3, -2, -1, 1, 2, 3]) : 0 };
    },
    twin: function (rng, L, p) {
      var q = { a: p.a, b: p.b, k: p.k }, r = rng.next();
      if (r < 0.4) q.a = p.a + rng.pick([-2, -1, 1, 2]); else if (r < 0.75) q.b = near(p.b, 2) ? rng.pick([3, 0.5]) : near(p.b, 0.5) ? rng.pick([2, 1 / 3]) : 2; else q.k = p.k + rng.pick([-2, -1, 1, 2]);
      return q.a !== 0 && Math.abs(q.k) <= 3 && (L.id !== 'cp2' || q.k === 0) ? q : null;
    },
    build: function (p, L, rng) {
      var a = p.a, b = p.b, k = p.k, fn = base('exponential'), qb = toQ(b);
      fn.p = p; fn.f = function (x) { return a * Math.pow(b, x) + k; };
      var bt = qb.d === 1 ? String(qb.n) : '\\left(\\frac{' + qb.n + '}{' + qb.d + '}\\right)';
      fn.eq = 'y = ' + (near(a, 1) ? (qb.d === 1 ? bt : bt) : near(a, -1) ? '-' + bt : nt(a) + (qb.d === 1 ? '(' + bt + ')' : bt)) + '^{x}' + kTerm(k);
      var F = fn.feats;
      F.yint = a + k; F.factor = b; F.growth = b > 1 ? 'growth' : 'decay'; F.asymH = k; F.range = [a > 0 ? 'gt' : 'lt', k];
      F.mono = (a > 0) === (b > 1) ? 'inc' : 'dec'; F.xints = -k / a > 0 ? [Math.log(-k / a) / Math.log(b)] : [];
      fn.graph = a > 0 ? win(k, k + 6) : win(k - 6, k); if (!fn.graph) return null;
      var lat = finishGraph(fn, null, [], k !== 0 ? [{ y: k }] : []);
      if (lat.length < 2) return null;
      fn.graph.dots = lat.slice(0, 4);
      // table: five consecutive x-values with whole-number y-values
      var starts = [-1, 0, -2, 1, -3].filter(function (s) { var rows = [0, 1, 2, 3, 4].map(function (i) { return fn.f(s + i); }); return rows.every(function (v) { return isInt(v) && Math.abs(v) <= 250; }); });
      if (!starts.length) return null;
      var s0 = L.id === 'honors' ? rng.pick(starts) : starts[0];
      tableOf(fn, [0, 1, 2, 3, 4].map(function (i) { return s0 + i; }));
      var Fs = {}, word = { 2: 'doubles', 3: 'triples' }[qb.n] && qb.d === 1 ? { 2: 'doubles', 3: 'triples' }[qb.n] : qb.n === 1 && qb.d === 2 ? 'is cut in half' : 'is multiplied by ' + m(nt(b));
      Fs.yint = fact('yint', F.yint, k === 0 && rng.next() < 0.5 && a > 0 ? 'Its initial value (when ' + m('x = 0') + ') is ' + m(nt(a)) + '.' : 'Its ' + m('y') + '-intercept is ' + m(pt(0, F.yint)) + '.');
      if (k === 0) Fs.factorY = { key: 'factorY', text: m('y') + ' ' + word + ' each time ' + m('x') + ' increases by ' + m('1') + '.', test: function (g) { return feq(g.feats.factor, b) && feq(g.feats.asymH, 0); } };
      Fs.factor = fact('factor', b, 'Its ' + (b > 1 ? 'growth' : 'decay') + ' factor is ' + m(nt(b)) + '.');
      Fs.asymH = fact('asymH', k, 'Its horizontal asymptote is ' + m('y = ' + nt(k)) + '.');
      Fs.range = fact('range', F.range, 'Its range is ' + m(rangeTex(F.range)) + '.');
      ptFacts(fn, Fs, [0], rng);
      fn.facts = Fs;
      fn.combos = k === 0 ? [['yint', 'factorY'], ['pt0', 'factorY'], ['yint', 'factorY']] : [['asymH', 'yint', 'factor'], ['asymH', 'pt0', 'factor'], ['range', 'yint', 'factor']];
      if (L.id === 'honors' && k === 0) fn.combos.push(['asymH', 'pt0', 'factor']);
      return fn;
    }
  };

  /* ---- logarithmic: y = log_b(x - h) + k ---- */
  FAM.log = {
    make: function (rng) { return { b: rng.pick([2, 2, 3]), h: rng.int(-4, 1), k: rng.int(-3, 3) }; },
    twin: function (rng, L, p) { var q = { b: p.b, h: p.h, k: p.k }, r = rng.next(); if (r < 0.35) q.b = p.b === 2 ? 3 : 2; else if (r < 0.7) q.k = p.k + rng.pick([-2, -1, 1, 2]); else q.h = p.h + rng.pick([-2, -1, 1, 2]); return q.h >= -5 && q.h <= 1 && Math.abs(q.k) <= 3 ? q : null; },
    build: function (p, L, rng) {
      var b = p.b, h = p.h, k = p.k, fn = base('log');
      fn.p = p; fn.f = function (x) { return x <= h + EPS ? NaN : Math.log(x - h) / Math.log(b) + k; };
      fn.eq = 'y = \\log_{' + b + '}' + par(h) + kTerm(k);
      var F = fn.feats;
      F.asymV = h; F.domain = ['gt', h]; F.mono = 'inc'; F.xints = [h + Math.pow(b, -k)]; F.yint = h < 0 ? fn.f(0) : null;
      fn.graph = win(k - 4, k + 3); if (!fn.graph) return null;
      finishGraph(fn, [h], [[h + 1, k], [h + b, k + 1], [h + b * b, k + 2]], [{ x: h }]);
      if (fn.graph.dots.length < 2) return null;
      var ds = b === 2 ? [0.5, 1, 2, 4, 8] : [1 / 3, 1, 3, 9];
      tableOf(fn, ds.map(function (d) { return h + d; }));
      var Fs = {};
      Fs.asymV = fact('asymV', h, 'Its vertical asymptote is ' + m('x = ' + nt(h)) + '.');
      Fs.domain = fact('domain', F.domain, 'Its domain is ' + m(domTex(F.domain)) + '.');
      if (nice(F.xints[0])) Fs.xints = fact('xints', F.xints, xintText(F.xints));
      Fs.pt0 = ptFact('pt0', h + 1, k); Fs.pt1 = ptFact('pt1', h + b, k + 1); Fs.pt2 = ptFact('pt2', h + 1 / b, k - 1);
      fn.facts = Fs;
      fn.combos = [['asymV', 'pt0', 'pt1'], ['domain', 'pt0', 'pt1'], ['asymV', 'pt1', 'pt2']];
      return fn;
    }
  };

  /* ---- rational: y = a/(x - h) + k ---- */
  FAM.rational = {
    make: function (rng, L) { return { a: rng.pick(L.id === 'cp2' ? [1, 2, -1, -2] : [1, 2, 3, 4, 6, -1, -2, -3, -4, -6]), h: rng.int(-3, 3), k: rng.int(-3, 3) }; },
    twin: function (rng, L, p) { var q = { a: p.a, h: p.h, k: p.k }, r = rng.next(); if (r < 0.4) q.a = -p.a; else if (r < 0.55) q.a = 2 * p.a; else if (r < 0.8) q.h = p.h + rng.pick([-2, -1, 1, 2]); else q.k = p.k + rng.pick([-2, -1, 1, 2]); return Math.abs(q.h) <= 3 && Math.abs(q.k) <= 3 && Math.abs(q.a) <= 6 ? q : null; },
    build: function (p, L, rng) {
      var a = p.a, h = p.h, k = p.k, fn = base('rational');
      fn.p = p; fn.f = function (x) { return near(x, h) ? NaN : a / (x - h) + k; };
      fn.eq = 'y = ' + (a < 0 ? '-' : '') + '\\frac{' + Math.abs(a) + '}{' + sh(h) + '}' + kTerm(k);
      var F = fn.feats;
      F.asymV = h; F.asymH = k; F.domain = ['ne', h]; F.range = ['ne', k]; F.yint = h !== 0 ? fn.f(0) : null; F.xints = k !== 0 ? [h - a / k] : []; F.quads = a > 0 ? '13' : '24';
      fn.graph = win(k - 4, k + 4); if (!fn.graph) return null;
      var lat = finishGraph(fn, [h], [], [{ x: h }, { y: k }]);
      if (lat.length < 2) return null;
      fn.graph.dots = lat.filter(function (q) { return Math.abs(q[0] - h) <= Math.abs(a); }).slice(0, 4);
      var ds = L.id === 'cp2' ? [-2, -1, 1, 2] : [-2, -1, 1, 2, Math.abs(a) > 2 ? Math.abs(a) : 4];
      if (!tableOf(fn, ds.map(function (d) { return h + d; })) || !tableNice(fn.table.rows, true)) return null;
      var Fs = {};
      Fs.asymV = fact('asymV', h, 'Its vertical asymptote is ' + m('x = ' + nt(h)) + '.');
      Fs.asymH = fact('asymH', k, 'Its horizontal asymptote is ' + m('y = ' + nt(k)) + '.');
      Fs.domain = fact('domain', F.domain, 'Its domain is all real numbers except ' + m('x = ' + nt(h)) + '.');
      Fs.range = fact('range', F.range, 'Its range is all real numbers except ' + m('y = ' + nt(k)) + '.');
      if (F.yint !== null && nice(F.yint)) Fs.yint = fact('yint', F.yint, 'Its ' + m('y') + '-intercept is ' + m(pt(0, F.yint)) + '.');
      Fs.pt0 = ptFact('pt0', h + 1, k + a); Fs.pt1 = ptFact('pt1', h - 1, k - a);
      fn.facts = Fs;
      fn.combos = [['asymV', 'asymH', 'pt0'], ['asymV', 'asymH', 'pt1'], ['domain', 'range', 'pt0'], ['asymV', 'asymH', 'yint']];
      return fn;
    }
  };

  /* ---- cubic: y = a(x - r1)(x - r2)(x - r3) ---- */
  FAM.cubic = {
    make: function (rng, L) {
      var a = rng.pick(L.id === 'cp2' ? [1, -1, 0.5, -0.5] : [1, -1, 0.5, -0.5, 0.25, -0.25]), r1 = rng.int(-4, 1), r2 = r1 + rng.int(1, 3), r3 = rng.next() < 0.3 ? r2 : r2 + rng.int(1, 3);
      if (rng.next() < 0.5) { var t = r1; r1 = r3; r3 = t; }
      return { a: a, r: [r1, r2, r3].sort(function (x, y) { return x - y; }), form: L.id === 'honors' && rng.next() < 0.4 ? 's' : 'f' };
    },
    twin: function (rng, L, p) { var q = { a: p.a, r: p.r.slice(), form: p.form }, r = rng.next(); if (r < 0.45) q.a = -p.a; else if (r < 0.65) q.a = p.a * 2; else { var i = rng.int(0, 2); q.r[i] += rng.pick([-1, 1]); q.r.sort(function (x, y) { return x - y; }); } return Math.abs(q.a) <= 2 ? q : null; },
    build: function (p, L, rng) {
      var a = p.a, r = p.r, fn = base('cubic');
      fn.p = p; fn.f = function (x) { return a * (x - r[0]) * (x - r[1]) * (x - r[2]); };
      var zs = []; r.forEach(function (x) { var z = zs.filter(function (q) { return q[0] === x; })[0]; if (z) z[1]++; else zs.push([x, 1]); });
      if (p.form === 's') { var s1 = r[0] + r[1] + r[2], s2 = r[0] * r[1] + r[0] * r[2] + r[1] * r[2], s3 = r[0] * r[1] * r[2]; fn.eq = 'y = ' + poly([[a, 'x^{3}'], [-a * s1, 'x^{2}'], [a * s2, 'x'], [-a * s3, '']]); }
      else fn.eq = 'y = ' + coef(a) + zs.slice().sort(function (x, y) { return (x[0] === 0 ? -1 : 0) - (y[0] === 0 ? -1 : 0); }).map(function (z) { return par(z[0]) + (z[1] > 1 ? '^{' + z[1] + '}' : ''); }).join('');
      var F = fn.feats;
      F.zeros = zs; F.xints = zs.map(function (z) { return z[0]; }); F.yint = fn.f(0); F.end = a > 0 ? 'du' : 'ud';
      // the turning points must be on the grid
      var big = 0; for (var x = r[0] - 0.5; x <= r[2] + 0.5; x += 0.05) big = Math.max(big, Math.abs(fn.f(x)));
      if (big > 6 || r[0] < -5 || r[2] > 5) return null;
      fn.graph = win(-big, big); if (!fn.graph) return null;
      var lat = finishGraph(fn, null, []);
      fn.graph.dots = lat.filter(function (q) { return q[1] === 0 || q[0] === 0; });
      if (lat.length < 4) return null;
      var c0 = Math.round((r[0] + r[2]) / 2), xs = [-2, -1, 0, 1, 2].map(function (i) { return c0 + i; });
      if (!tableOf(fn, xs) || !tableNice(fn.table.rows)) return null;
      var Fs = {}, cross = zs.filter(function (z) { return z[1] === 1; }), touch = zs.filter(function (z) { return z[1] === 2; });
      Fs.zeros = fact('zeros', zs, touch.length ? 'It touches the ' + m('x') + '-axis at ' + m('x = ' + touch[0][0]) + ' and crosses it at ' + m('x = ' + cross[0][0]) + '.' : 'Its zeros are ' + m(nt(r[0])) + ', ' + m(nt(r[1])) + ' and ' + m(nt(r[2])) + '.');
      if (nice(F.yint) && !near(F.yint, 0)) Fs.yint = fact('yint', F.yint, 'Its ' + m('y') + '-intercept is ' + m(pt(0, F.yint)) + '.');
      Fs.end = fact('end', F.end, a > 0 ? 'It falls to the left and rises to the right.' : 'It rises to the left and falls to the right.');
      ptFacts(fn, Fs, F.xints.concat([0]), rng);
      fn.facts = Fs;
      fn.combos = [['zeros', 'yint'], ['zeros', 'pt0'], ['zeros', 'end', 'pt0']];
      return fn;
    }
  };

  /* ---- sequences ---- */
  function seqWin(fn) {
    var vals = [1, 2, 3, 4, 5].map(fn.f), lo = Math.min(0, Math.min.apply(null, vals)), hi = Math.max(0, Math.max.apply(null, vals));
    var span = hi - lo, st = span <= 10 ? 1 : span <= 20 ? 2 : span <= 50 ? 5 : span <= 100 ? 10 : 25;
    lo = Math.floor(lo / st) * st - st; hi = Math.ceil(hi / st) * st + st;
    fn.graph = { xmin: -1, xmax: 7, ymin: lo, ymax: hi, xstep: 1, ystep: st, lab: ['n', 'a_{n}'] };
    fn.graph.curves = []; fn.graph.asym = [];
    fn.graph.dots = [1, 2, 3, 4, 5, 6].map(function (n) { return [n, fn.f(n)]; }).filter(function (d) { return d[1] >= lo && d[1] <= hi; });
    return fn.graph.dots.length >= 4;
  }
  function ordinal(n) { return n + (n === 1 ? 'st' : n === 2 ? 'nd' : n === 3 ? 'rd' : 'th'); }
  FAM.arith = {
    make: function (rng, L) { return { a1: rng.int(-5, 8), d: L.id === 'cp2' ? rng.int(1, 4) * (rng.next() < 0.25 ? -1 : 1) : rng.pick([-4, -3, -2, -1, 1, 2, 3, 4, 5]) }; },
    twin: function (rng, L, p) { var q = { a1: p.a1, d: p.d }; if (rng.next() < 0.5) q.a1 = p.a1 + rng.pick([-2, -1, 1, 2]); else q.d = -p.d; return q; },
    build: function (p, L, rng) {
      var a1 = p.a1, d = p.d, fn = base('arith');
      fn.p = p; fn.discrete = true; fn.f = function (n) { return isInt(n) && n >= 1 ? a1 + (n - 1) * d : NaN; };
      var form = pickW(rng, L.id === 'cp2' ? { ex: 3, si: 1 } : L.id === 'cp1' ? { ex: 2, si: 2, re: 1 } : { ex: 1, si: 2, re: 2 });
      fn.eq = form === 'ex' ? 'a_{n} = ' + a1 + (d > 0 ? ' + ' + d : ' - ' + (-d)) + '(n - 1)' : form === 'si' ? 'a_{n} = ' + poly([[d, 'n'], [a1 - d, '']]) : 'a_{1} = ' + a1 + ',\\; a_{n} = a_{n-1}' + kTerm(d);
      var F = fn.feats; F.diff = d; F.domain = 'n'; F.mono = d > 0 ? 'inc' : 'dec';
      if (!seqWin(fn)) return null;
      tableOf(fn, [1, 2, 3, 4, 5]);
      var Fs = {}, n = rng.int(3, 6);
      Fs.first = ptFact('first', 1, a1, 'The first term is ' + m(nt(a1)) + '.');
      Fs.term = ptFact('term', n, fn.f(n), 'The ' + ordinal(n) + ' term is ' + m(nt(fn.f(n))) + '.');
      Fs.diff = fact('diff', d, 'The common difference is ' + m(nt(d)) + '.');
      fn.facts = Fs; fn.combos = [['first', 'diff'], ['term', 'diff']];
      return fn;
    }
  };
  FAM.geom = {
    make: function (rng, L) { var r = rng.pick(L.id === 'cp2' ? [2, 3] : [2, 3, -2, 0.5]), a1 = r === 0.5 ? rng.pick([16, 32, 48]) : rng.pick(r === 3 ? [1, 2] : [1, 2, 3]); if (L.id !== 'cp2' && r !== 0.5 && rng.next() < 0.2) a1 = -a1; return { a1: a1, r: r }; },
    twin: function (rng, L, p) { var q = { a1: p.a1, r: p.r }; if (rng.next() < 0.5 && p.r !== 0.5) q.a1 = p.a1 + (p.a1 > 0 ? 1 : -1); else q.r = p.r === 2 ? 3 : p.r === 3 ? 2 : p.r === -2 ? 2 : 0.5; if (q.r === 0.5 && Math.abs(q.a1) < 16) return null; if (q.r === 3 && Math.abs(q.a1) > 2) return null; return q; },
    build: function (p, L, rng) {
      var a1 = p.a1, r = p.r, fn = base('geom'), qr = toQ(r);
      fn.p = p; fn.discrete = true; fn.f = function (n) { return isInt(n) && n >= 1 ? a1 * Math.pow(r, n - 1) : NaN; };
      var rt = qr.d === 1 ? (r < 0 ? '(' + r + ')' : String(r)) : '\\left(\\frac{' + qr.n + '}{' + qr.d + '}\\right)';
      var form = L.id === 'cp2' ? 'ex' : pickW(rng, L.id === 'cp1' ? { ex: 3, re: 1 } : { ex: 1, re: 1 });
      fn.eq = form === 'ex' ? 'a_{n} = ' + (a1 === 1 ? rt : a1 === -1 ? '-' + rt : a1 + (qr.d === 1 ? '(' + r + ')' : rt)) + '^{n-1}' : 'a_{1} = ' + a1 + ',\\; a_{n} = ' + coef(r) + 'a_{n-1}';
      if (form === 'ex' && a1 === 1 && qr.d === 1 && r > 0) fn.eq = 'a_{n} = ' + r + '^{n-1}';
      var F = fn.feats; F.ratio = r; F.domain = 'n'; F.mono = r < 0 ? 'none' : (a1 > 0) === (r > 1) ? 'inc' : 'dec';
      if (!seqWin(fn)) return null;
      tableOf(fn, [1, 2, 3, 4, 5]);
      if (!tableNice(fn.table.rows)) return null;
      var Fs = {}, n = rng.int(3, 5);
      Fs.first = ptFact('first', 1, a1, 'The first term is ' + m(nt(a1)) + '.');
      Fs.term = ptFact('term', n, fn.f(n), 'The ' + ordinal(n) + ' term is ' + m(nt(fn.f(n))) + '.');
      Fs.ratio = fact('ratio', r, 'The common ratio is ' + m(nt(r)) + '.');
      fn.facts = Fs; fn.combos = [['first', 'ratio'], ['term', 'ratio']];
      return fn;
    }
  };
  M.FAM = FAM;

  /* ---------------- checks (also used by the tests) ---------------- */
  /* g could be mistaken for f's graph: within half a grid unit wherever f is drawn (and at f's dots). */
  M.graphFits = function (f, g) {
    var w = f.graph, tol = 0.5 * (w.ystep || 1);
    if (f.discrete) return w.dots.every(function (d) { var v = g.f(d[0]); return isFinite(v) && Math.abs(v - d[1]) <= tol + EPS; }) && w.dots.length > 0;
    var seen = 0;
    for (var i = 0; i <= 240; i++) {
      var x = w.xmin + (w.xmax - w.xmin) * i / 240, y = f.f(x);
      if (!(isFinite(y) && y >= w.ymin && y <= w.ymax)) continue;
      var z = g.f(x); seen++;
      if (!isFinite(z) || Math.abs(z - y) > tol + EPS) return false;
    }
    return seen > 0;
  };
  M.tableFits = function (f, g) { return f.table.rows.every(function (r) { var v = g.f(r[0]); return isFinite(v) && near(v, r[1]); }); };
  M.descFits = function (f, g) { return f.desc.every(function (ft) { return ft.test(g); }); };
  M.sameFn = function (f, g) { for (var x = -6; x <= 6; x += 0.5) { var a = f.f(x), b = g.f(x); if (isFinite(a) !== isFinite(b) || (isFinite(a) && !near(a, b))) return false; } return true; };

  function chooseDesc(fn, fns, rng, U) {
    var combos = rng.shuffle(fn.combos.slice());
    if (U.xform && fn.facts.xform && rng.next() < 0.7) combos.unshift(['xform']);
    for (var i = 0; i < combos.length; i++) {
      var fs = combos[i].map(function (k) { return fn.facts[k]; });
      if (fs.some(function (x) { return !x; })) continue;
      if (!fs.every(function (x) { return x.test(fn); })) continue;   // never print a false fact
      if (fns.every(function (g) { return g === fn || !fs.every(function (x) { return x.test(g); }); })) return fs;
    }
    return null;
  }

  /* ---------------- build ---------------- */
  PR.buildMatch = function (cfg, vIdx) {
    var U = M.UNITS[cfg.unitId];
    if (!U) return { error: 'Matching is only available for units about graphing functions.' };
    var fams = U.fams.filter(function (f) { return cfg.families ? cfg.families[f] : U.def.indexOf(f) >= 0; });
    if (!fams.length) return { error: 'Choose at least one function type.' };
    var L = NS.LEVELS[cfg.level] || NS.LEVELS.cp1, N = Math.max(4, Math.min(10, cfg.sets | 0 || 6));
    var twinsWanted = L.id === 'cp2' ? 1 : L.id === 'cp1' ? Math.floor(N / 3) : Math.floor(N / 2);
    for (var attempt = 0; attempt < 40; attempt++) {
      var rng = rngOf(cfg.seed, vIdx, 'match', attempt), fns = [], twins = 0, order = rng.shuffle(fams.slice());
      for (var t = 0; t < 600 && fns.length < N; t++) {
        var fam = order[fns.length % order.length], F = FAM[fam], p = null;
        var sib = fns.filter(function (g) { return g.fam === fam; });
        if (sib.length && twins < twinsWanted && rng.next() < 0.6) { p = F.twin(rng, L, rng.pick(sib).p, U); if (p) p.twin = true; }
        if (!p) p = F.make(rng, L, U);
        var fn = F.build(p, L, rng, U);
        if (!fn) continue;
        if (fns.some(function (g) { return M.sameFn(fn, g) || g.eq === fn.eq || M.graphFits(fn, g) || M.graphFits(g, fn) || M.tableFits(fn, g) || M.tableFits(g, fn); })) continue;
        if (p.twin) twins++;
        fns.push(fn);
      }
      if (fns.length < N) continue;
      var bad = false;
      fns.forEach(function (fn) { if (bad) return; fn.desc = chooseDesc(fn, fns, rng, U); if (!fn.desc) bad = true; });
      if (bad) continue;
      // cards: each type numbered in its own shuffled order
      var ids = {};
      M.TYPES.forEach(function (ty) { var perm = rng.shuffle(fns.map(function (_, i) { return i; })); ids[ty.id] = []; perm.forEach(function (si, pos) { ids[ty.id][si] = pos + 1; }); });
      var blanks = {};
      if (cfg.blanks === 'some') {
        var rot = rng.shuffle(['graph', 'table', 'desc', 'eq']);
        rng.shuffle(fns.map(function (_, i) { return i; })).slice(0, Math.ceil(N / 3)).forEach(function (si, j) { blanks[si] = rot[j % rot.length]; });
      }
      return { kind: 'match', fns: fns, N: N, ids: ids, blanks: blanks, fams: fams };
    }
    return { error: 'Could not make ' + N + ' different sets for these function types and this level. Try fewer sets or more function types.' };
  };
})(typeof window !== 'undefined' ? window : globalThis);
