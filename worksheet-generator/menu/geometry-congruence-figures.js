/* Honest congruence-marking figures (geo-cong).

   spec: { kind:'geo-cong',
           pts:{A:[x,y],...}                 math coordinates (y up); every drawn point
           segs:[['A','B'],...]              segments to draw
           tris:[['A','B','C'],['D','E','F']] optional corresponding triangles (for the criterion derivation)
           sides:[{ s:[['A','B'],['D','E']], n:1 }]      equal-side tick groups
           angles:[{ a:[['B','A','C'],['E','D','F']], n:1 }]  equal-angle arc groups (vertex in the middle)
           right:[['A','B','C']]             right-angle marks (vertex in the middle)
           lab:{ AB:'x+3', DE:'25' }         segment label text (placed outside)
           note:'' }
   F.cong.derive(spec) -> 'SSS'|'SAS'|'ASA'|'AAS'|'HL'|'SSA'|'AAA'|'NONE' from the marks alone.
   F.cong.pair(kind, flip) / shared() / cross() build exact, consistent specs for the skills.
   The checker measures the drawn coordinates: every tick group must have equal lengths, every arc group equal
   angles, every right mark exactly 90 degrees. A marking the picture does not support is refused. */
(function (G) {
  'use strict';
  var NS = G.MKMENU = (G.MKMENU || {}), F = NS.geoFigures;
  if (!F || !F.extend) return;
  var H = F.h, W = H.W, INK = H.INK, r1 = H.r1, L = H.L, dot = H.dot, DEG = Math.PI / 180;
  function T(x, y, s, anchor) { return H.T(x, y, s, anchor).replace('<text ', '<text stroke="#fff" stroke-width="4" paint-order="stroke" '); }
  function d(p, q) { return Math.hypot(p[0] - q[0], p[1] - q[1]); }
  function unit(a, b) { var m = d(a, b) || 1; return [(b[0] - a[0]) / m, (b[1] - a[1]) / m]; }
  function ang(P, V, Q) { var u = unit(V, P), v = unit(V, Q); return Math.acos(Math.max(-1, Math.min(1, u[0] * v[0] + u[1] * v[1]))) / DEG; }
  function numOf(s) { var m = /^\s*(\d+(?:\.\d+)?)\s*(?:°|units|cm)?\s*$/i.exec(String(s)); return m ? Number(m[1]) : null; }

  function check(spec) {
    var P = spec.pts, i, j, g;
    if (!P || !Object.keys(P).length) return { ok: false, msg: 'no points' };
    function pt(n) { return P[n]; }
    for (i = 0; i < (spec.segs || []).length; i++) if (!pt(spec.segs[i][0]) || !pt(spec.segs[i][1])) return { ok: false, msg: 'segment uses an undefined point' };
    for (i = 0; i < (spec.sides || []).length; i++) {
      g = spec.sides[i]; if (!(g.n >= 1 && g.n <= 4) || g.s.length < 2) return { ok: false, msg: 'bad tick group' };
      var l0 = null;
      for (j = 0; j < g.s.length; j++) {
        if (!pt(g.s[j][0]) || !pt(g.s[j][1])) return { ok: false, msg: 'tick on an undefined segment' };
        var ln = d(pt(g.s[j][0]), pt(g.s[j][1])); if (l0 === null) l0 = ln; else if (Math.abs(ln - l0) > 1e-6 * Math.max(1, l0)) return { ok: false, msg: 'segments ' + g.s[0].join('') + ' and ' + g.s[j].join('') + ' are marked equal but are not' };
      }
    }
    for (i = 0; i < (spec.angles || []).length; i++) {
      g = spec.angles[i]; if (!(g.n >= 1 && g.n <= 4) || g.a.length < 2) return { ok: false, msg: 'bad arc group' };
      var a0 = null;
      for (j = 0; j < g.a.length; j++) {
        var t = g.a[j]; if (!pt(t[0]) || !pt(t[1]) || !pt(t[2])) return { ok: false, msg: 'arc on an undefined angle' };
        var av = ang(pt(t[0]), pt(t[1]), pt(t[2])); if (a0 === null) a0 = av; else if (Math.abs(av - a0) > 1e-6) return { ok: false, msg: 'angles ' + g.a[0].join('') + ' and ' + t.join('') + ' are marked equal but are not' };
      }
    }
    for (i = 0; i < (spec.right || []).length; i++) { var r = spec.right[i]; if (!pt(r[0]) || !pt(r[1]) || !pt(r[2]) || Math.abs(ang(pt(r[0]), pt(r[1]), pt(r[2])) - 90) > 1e-6) return { ok: false, msg: 'right-angle mark on a non-right angle' }; }
    for (var k in (spec.lab || {})) { var n = numOf(spec.lab[k]); if (n === null && !/[a-z]/i.test(String(spec.lab[k]))) return { ok: false, msg: 'bad label ' + spec.lab[k] }; }
    for (i = 0; i < (spec.angLab || []).length; i++) { var al = spec.angLab[i]; if (!pt(al.p) || !pt(al.v) || !pt(al.q)) return { ok: false, msg: 'angle label on an undefined angle' }; var an2 = numOf(al.text); if (an2 !== null && !spec.nts && Math.abs(an2 - ang(pt(al.p), pt(al.v), pt(al.q))) > 0.6) return { ok: false, msg: 'angle labelled ' + al.text + ' is drawn as ' + Math.round(ang(pt(al.p), pt(al.v), pt(al.q))) + '°' }; }
    return { ok: true };
  }

  /* criterion from the marks alone (tris = [[A,B,C],[D,E,F]]) */
  function derive(spec) {
    var tr = spec.tris; if (!tr) return 'NONE';
    var map = {}; tr[0].forEach(function (v, i) { map[v] = tr[1][i]; });
    var sides = {}, verts = {}, right = {}, i, j;
    (spec.sides || []).forEach(function (g) {
      g.s.forEach(function (a) { g.s.forEach(function (b) {
        if (a === b) return;
        var ka = a[0] + a[1], inT1 = tr[0].indexOf(a[0]) >= 0 && tr[0].indexOf(a[1]) >= 0 && tr[1].indexOf(b[0]) >= 0 && tr[1].indexOf(b[1]) >= 0;
        if (inT1 && ((map[a[0]] === b[0] && map[a[1]] === b[1]) || (map[a[0]] === b[1] && map[a[1]] === b[0]))) sides[[a[0], a[1]].sort().join('')] = true;
      }); });
    });
    (spec.angles || []).forEach(function (g) {
      g.a.forEach(function (a) { g.a.forEach(function (b) { if (a !== b && tr[0].indexOf(a[1]) >= 0 && map[a[1]] === b[1]) verts[a[1]] = true; }); });
    });
    (spec.right || []).forEach(function (r) { if (tr[0].indexOf(r[1]) >= 0) right[r[1]] = true; else if (tr[1].indexOf(r[1]) >= 0) right[tr[0][tr[1].indexOf(r[1])]] = true; });
    // a right angle needs to be marked in both triangles to count as a pair
    var bothRight = tr[0].filter(function (v) { return right[v] && (spec.right || []).some(function (r) { return r[1] === map[v]; }) && (spec.right || []).some(function (r) { return r[1] === v; }); });
    bothRight.forEach(function (v) { verts[v] = true; });
    var sk = Object.keys(sides), vk = Object.keys(verts);
    if (sk.length >= 3) return 'SSS';
    if (sk.length === 2) {
      var shared = sk[0].split('').filter(function (c) { return sk[1].indexOf(c) >= 0; })[0];
      if (shared && verts[shared]) return 'SAS';
      if (bothRight.length) {
        var rvv = bothRight[0], opp = tr[0].filter(function (v) { return v !== rvv; }).sort().join('');
        if (sk.indexOf(opp) >= 0) return 'HL';
      }
      return vk.length ? 'SSA' : 'NONE';
    }
    if (sk.length === 1) {
      if (vk.length >= 2) return sk[0].split('').every(function (c) { return verts[c]; }) ? 'ASA' : 'AAS';
      return 'NONE';
    }
    return vk.length >= 3 ? 'AAA' : 'NONE';
  }

  function render(spec) {
    var P = spec.pts, names = Object.keys(P), xs = names.map(function (n) { return P[n][0]; }), ys = names.map(function (n) { return P[n][1]; });
    var mnx = Math.min.apply(null, xs), mxx = Math.max.apply(null, xs), mny = Math.min.apply(null, ys), mxy = Math.max.apply(null, ys);
    var s = Math.min(330 / (mxx - mnx || 1), 120 / (mxy - mny || 1)), x0 = (W - (mxx - mnx) * s) / 2 - mnx * s, y0 = 46 + mxy * s;
    var S = {}; names.forEach(function (n) { S[n] = [x0 + P[n][0] * s, y0 - P[n][1] * s]; });
    var o = '', i, j, boxes = [];
    function box(x, y, t) { var w = String(t).length * 7.8 + 6, b = [x - w / 2, y - 9, x + w / 2, y + 9]; boxes.push(b); return b; }
    (spec.segs || []).forEach(function (sg) { o += L(S[sg[0]], S[sg[1]]); });
    var cen = {}, group = function (n) { var tt = (spec.tris || []).filter(function (t) { return t.indexOf(n) >= 0; })[0]; var pts = (tt || names).map(function (m) { return S[m]; }); return [pts.reduce(function (a, p) { return a + p[0]; }, 0) / pts.length, pts.reduce(function (a, p) { return a + p[1]; }, 0) / pts.length]; };
    names.forEach(function (n) { o += dot(S[n], 3); });
    names.forEach(function (n) { var c = group(n), u = unit(c, S[n]); var x = S[n][0] + u[0] * 14, y = S[n][1] + u[1] * 14; o += T(x, y, n); box(x, y, n); });
    function tick(p, q, n) {
      var m = [(p[0] + q[0]) / 2, (p[1] + q[1]) / 2], u = unit(p, q), nn = [-u[1], u[0]], r = '';
      for (var k = 0; k < n; k++) { var c = [m[0] + u[0] * (k - (n - 1) / 2) * 5, m[1] + u[1] * (k - (n - 1) / 2) * 5]; r += '<path d="M' + r1(c[0] - nn[0] * 6) + ' ' + r1(c[1] - nn[1] * 6) + ' L' + r1(c[0] + nn[0] * 6) + ' ' + r1(c[1] + nn[1] * 6) + '" stroke="' + INK + '" stroke-width="1.7"/>'; }
      return r;
    }
    (spec.sides || []).forEach(function (g) { g.s.forEach(function (sg) { o += tick(S[sg[0]], S[sg[1]], g.n); }); });
    function arc(V, u1, u2, r) { var p = [V[0] + u1[0] * r, V[1] + u1[1] * r], q = [V[0] + u2[0] * r, V[1] + u2[1] * r], cr = u1[0] * u2[1] - u1[1] * u2[0]; return '<path d="M' + r1(p[0]) + ' ' + r1(p[1]) + ' A' + r + ' ' + r + ' 0 0 ' + (cr > 0 ? 1 : 0) + ' ' + r1(q[0]) + ' ' + r1(q[1]) + '" stroke="' + INK + '" stroke-width="1.4" fill="none"/>'; }
    (spec.angles || []).forEach(function (g) { g.a.forEach(function (t) { var V = S[t[1]], u1 = unit(V, S[t[0]]), u2 = unit(V, S[t[2]]); for (var k = 0; k < g.n; k++) o += arc(V, u1, u2, 15 + k * 4); }); });
    (spec.right || []).forEach(function (r) { var V = S[r[1]], u = unit(V, S[r[0]]), v = unit(V, S[r[2]]), a = 10, p = [V[0] + u[0] * a, V[1] + u[1] * a], q = [p[0] + v[0] * a, p[1] + v[1] * a], z = [V[0] + v[0] * a, V[1] + v[1] * a]; o += '<path d="M' + r1(p[0]) + ' ' + r1(p[1]) + ' L' + r1(q[0]) + ' ' + r1(q[1]) + ' L' + r1(z[0]) + ' ' + r1(z[1]) + '" stroke="' + INK + '" stroke-width="1.5" fill="none"/>'; });
    (spec.angLab || []).forEach(function (al) {
      var V = S[al.v], u1 = unit(V, S[al.p]), u2 = unit(V, S[al.q]), bis = [u1[0] + u2[0], u1[1] + u2[1]], bm = Math.hypot(bis[0], bis[1]) || 1; bis = [bis[0] / bm, bis[1] / bm];
      var tw = String(al.text).length * 7.8 + 6, a = Math.acos(Math.max(-1, Math.min(1, u1[0] * u2[0] + u1[1] * u2[1]))), placed = false;
      for (var dd = 30; dd <= 80 && !placed; dd += 4) if (2 * dd * Math.tan(a / 2) >= tw + 4) { o += arc(V, u1, u2, 17) + T(V[0] + bis[0] * dd, V[1] + bis[1] * dd, al.text); placed = true; }
      if (!placed) o += arc(V, u1, u2, 17) + T(V[0] + bis[0] * 44, V[1] + bis[1] * 44, al.text);
    });
    for (var key in (spec.lab || {})) {
      var a = S[key[0]], b = S[key[1]]; if (!a || !b) continue;
      var m = [(a[0] + b[0]) / 2, (a[1] + b[1]) / 2], c = group(key[0]), u = unit(c, m), tw = String(spec.lab[key]).length * 7.8 / 2;
      o += T(m[0] + u[0] * (13 + tw * Math.abs(u[0])), m[1] + u[1] * 15, spec.lab[key]);
    }
    return H.wrap(o, Math.ceil(46 + (mxy - mny) * s + 40), 'Triangles with their congruent parts marked', spec.note || '');
  }

  F.printedCong = function (spec) { var out = [], k, n; for (k in (spec.lab || {})) { n = numOf(spec.lab[k]); if (n !== null) out.push([k, n]); } (spec.angLab || []).forEach(function (al) { n = numOf(al.text); if (n !== null) out.push(['angle ' + al.v, n]); }); return out; };
  var prev = F.printed; F.printed = function (spec) { return spec && spec.kind === 'geo-cong' ? F.printedCong(spec) : prev ? prev(spec) : null; };

  /* ---------- builders ---------- */
  function refl(p, X0) { return [X0 - p[0], p[1]]; }
  function pair(kind, flip) {
    var t1, t2;
    if (kind === 'hl') t1 = { A: [0, 0], B: [1.0, 0], C: [1.0, 0.78] };            // right angle at B
    else t1 = { A: [0, 0], B: [1.15, 0], C: [0.46, 0.82] };
    var names1 = ['A', 'B', 'C'], names2 = ['D', 'E', 'F'], P = {};
    if (kind === 'ssa') {                                                         // the ambiguous case: same AB, BC and angle A, different AC
      var al = 30 * DEG, c = 1, a = 0.62, dsc = Math.sqrt(a * a - Math.pow(c * Math.sin(al), 2)), b1 = c * Math.cos(al) + dsc, b2 = c * Math.cos(al) - dsc;
      t1 = { A: [0, 0], B: [c, 0], C: [b1 * Math.cos(al), b1 * Math.sin(al)] };
      var raw2 = { A: [0, 0], B: [c, 0], C: [b2 * Math.cos(al), b2 * Math.sin(al)] };
    }
    var raw = kind === 'ssa' ? raw2 : t1, scale = kind === 'aaa' ? 1.6 : 1;
    var mx = Math.max(t1.A[0], t1.B[0], t1.C[0]), shift = mx + 0.7;
    names1.forEach(function (n, i) {
      P[n] = t1[n];
      var q = [raw[n][0] * scale, raw[n][1] * scale];
      P[names2[i]] = flip ? [shift + (Math.max(raw.A[0], raw.B[0], raw.C[0]) * scale - q[0]), q[1]] : [shift + q[0], q[1]];
    });
    var sp = { kind: 'geo-cong', pts: P, segs: [['A', 'B'], ['B', 'C'], ['C', 'A'], ['D', 'E'], ['E', 'F'], ['F', 'D']], tris: [['A', 'B', 'C'], ['D', 'E', 'F']], sides: [], angles: [], right: [] };
    var S1 = function (a, b, n) { sp.sides.push({ s: [a, b], n: n }); }, A1 = function (v1, v2, n) { sp.angles.push({ a: [v1, v2], n: n }); };
    var ang = function (v) { var i = names1.indexOf(v), j = (i + 1) % 3, k = (i + 2) % 3; return [[names1[j], v, names1[k]], [names2[j], names2[i], names2[k]]]; };
    if (kind === 'sss') { S1(['A', 'B'], ['D', 'E'], 1); S1(['B', 'C'], ['E', 'F'], 2); S1(['C', 'A'], ['F', 'D'], 3); }
    else if (kind === 'sas') { S1(['A', 'B'], ['D', 'E'], 1); S1(['C', 'A'], ['F', 'D'], 2); var a1 = ang('A'); A1(a1[0], a1[1], 1); }
    else if (kind === 'asa') { var q1 = ang('A'), q2 = ang('B'); A1(q1[0], q1[1], 1); A1(q2[0], q2[1], 2); S1(['A', 'B'], ['D', 'E'], 1); }
    else if (kind === 'aas') { q1 = ang('A'); q2 = ang('B'); A1(q1[0], q1[1], 1); A1(q2[0], q2[1], 2); S1(['C', 'A'], ['F', 'D'], 1); }
    else if (kind === 'hl') { sp.right = [['A', 'B', 'C'], ['D', 'E', 'F']]; S1(['C', 'A'], ['F', 'D'], 1); S1(['A', 'B'], ['D', 'E'], 2); }
    else if (kind === 'ssa') { S1(['A', 'B'], ['D', 'E'], 1); S1(['B', 'C'], ['E', 'F'], 2); a1 = ang('A'); A1(a1[0], a1[1], 1); }
    else if (kind === 'aaa') { ['A', 'B', 'C'].forEach(function (v, i) { var q = ang(v); A1(q[0], q[1], i + 1); }); }
    return sp;
  }
  function shared() {   // triangles ABC and ABD share AB (C above, D below); AC = AD and BC = BD
    return { kind: 'geo-cong', pts: { A: [0, 0], B: [1.2, 0], C: [0.55, 0.8], D: [0.55, -0.8] }, segs: [['A', 'B'], ['B', 'C'], ['C', 'A'], ['A', 'D'], ['D', 'B']], tris: null,
      sides: [{ s: [['A', 'C'], ['A', 'D']], n: 1 }, { s: [['B', 'C'], ['B', 'D']], n: 2 }], angles: [], right: [] };
  }
  function cross() {    // AC and BD cross at O; AO = CO, BO = DO
    return { kind: 'geo-cong', pts: { A: [0, 0.7], C: [1.6, -0.7], B: [0.1, -0.75], D: [1.5, 0.75], O: [0.8, 0] }, segs: [['A', 'C'], ['B', 'D'], ['A', 'B'], ['C', 'D']], tris: null,
      sides: [{ s: [['A', 'O'], ['C', 'O']], n: 1 }, { s: [['B', 'O'], ['D', 'O']], n: 2 }], angles: [], right: [] };
  }
  /* proof diagrams: 'shared' = triangles ABC, ABD on common side AB with AC=AD and BC=BD marked; 'vertical' = AC, BD cross at O with AO=CO and BO=DO marked */
  function proofKind(spec) {
    function has(grp, a, b) { return (spec.sides || []).some(function (g) { var k = g.s.map(function (x) { return x.slice().sort().join(''); }); return k.indexOf(a) >= 0 && k.indexOf(b) >= 0 && k.length === 2 && g.s.length === 2; }); }
    var P = spec.pts || {};
    if (P.O && has(0, 'AO', 'CO') && has(0, 'BO', 'DO')) return 'vertical';
    if (!P.O && P.A && P.B && P.C && P.D && has(0, 'AC', 'AD') && has(0, 'BC', 'BD')) return 'shared';
    return null;
  }
  F.cong = { derive: derive, pair: pair, shared: shared, cross: cross, proofKind: proofKind };
  F.extend('geo-cong', { render: render, check: check });
})(typeof window !== 'undefined' ? window : globalThis);
