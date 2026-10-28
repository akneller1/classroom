/* Data-driven similar-triangle figures.

   geo-sim: two similar triangles ABC and DEF. Triangle ABC is defined by ONE of
       sides:[AB, BC, CA]     angles:[A, B, C] (degrees)     sas:[AB, AC, angleA]
     and DEF is ABC scaled by k (k >= 1 or less), so the pair is similar by construction.
     show: names of sides (AB, BC, CA, DE, EF, FD) whose true length is printed (needs a sides/sas definition)
     lab : printed text replacing a side (an unknown such as 'x', or a number that must equal the true length)
     ang : { A:'x' | 65, ... } angle labels at A..F; a number is checked against the drawn angle
     marks: true draws matching arcs at corresponding vertices (1 arc at A/D, 2 at B/E, 3 at C/F)
   geo-tri-par: triangle ABC with D on AB, E on AC and DE parallel to BC
     v:{AD, DB, AE, EC}, plus BC:number (sides) or angA:degrees; show/lab as above; refused unless AD/DB = AE/EC.

   Truth is enforced: numeric labels must equal the drawn lengths/angles. A pair whose scale factor is
   too large to draw is limited to a 2.2:1 picture and marked "Not drawn to scale." */
(function (G) {
  'use strict';
  var NS = G.MKMENU = (G.MKMENU || {}), F = NS.geoFigures;
  if (!F || !F.extend) return;
  var H = F.h, W = H.W, INK = H.INK, r1 = H.r1, L = H.L, dot = H.dot;
  function T(x, y, s, anchor) { return H.T(x, y, s, anchor).replace('<text ', '<text stroke="#fff" stroke-width="4" paint-order="stroke" '); }
  var DEG = Math.PI / 180;

  /* triangle with vertices A (origin), B on the x-axis, C above; math coordinates (y up), unit scale */
  function build(spec) {
    var s;
    if (spec.sides) {
      var AB = spec.sides[0], BC = spec.sides[1], CA = spec.sides[2];
      if (!(AB > 0 && BC > 0 && CA > 0) || AB + BC <= CA + 1e-9 || BC + CA <= AB + 1e-9 || CA + AB <= BC + 1e-9) return null;
      var cx = (AB * AB + CA * CA - BC * BC) / (2 * AB), cy2 = CA * CA - cx * cx; if (cy2 <= 0) return null;
      s = { A: [0, 0], B: [AB, 0], C: [cx, Math.sqrt(cy2)], len: { AB: AB, BC: BC, CA: CA } };
    } else if (spec.sas) {
      var p = spec.sas[0], q = spec.sas[1], an = spec.sas[2] * DEG;
      if (!(p > 0 && q > 0 && spec.sas[2] > 0 && spec.sas[2] < 180)) return null;
      var C = [q * Math.cos(an), q * Math.sin(an)];
      s = { A: [0, 0], B: [p, 0], C: C, len: { AB: p, BC: Math.hypot(C[0] - p, C[1]), CA: q } };
    } else if (spec.angles) {
      var a = spec.angles[0], b = spec.angles[1], c = spec.angles[2];
      if (!(a > 0 && b > 0 && c > 0) || Math.abs(a + b + c - 180) > 1e-9) return null;
      var ca = Math.sin(b * DEG) / Math.sin(c * DEG);
      s = { A: [0, 0], B: [1, 0], C: [ca * Math.cos(a * DEG), ca * Math.sin(a * DEG)], len: null };
    } else return null;
    var angs = function (P, Q, R) { var u = [Q[0] - P[0], Q[1] - P[1]], v = [R[0] - P[0], R[1] - P[1]]; return Math.acos((u[0] * v[0] + u[1] * v[1]) / (Math.hypot(u[0], u[1]) * Math.hypot(v[0], v[1]))) / DEG; };
    s.ang = [angs(s.A, s.B, s.C), angs(s.B, s.C, s.A), angs(s.C, s.A, s.B)];
    return s;
  }
  function trueLen(spec, name) {          // true length of a named side of the pair, or null
    var t = build({ sides: spec.sides, sas: spec.sas, angles: spec.angles }), k = spec.k || 1;
    if (!t || !t.len) return null;
    var map = { AB: t.len.AB, BC: t.len.BC, CA: t.len.CA, AC: t.len.CA, DE: k * t.len.AB, EF: k * t.len.BC, FD: k * t.len.CA, DF: k * t.len.CA };
    return map[name] === undefined ? null : map[name];
  }
  function numOf(s) { var m = /^\s*(\d+(?:\.\d+)?)\s*(?:[a-z ]*)$/i.exec(String(s)); return m ? Number(m[1]) : null; }

  function checkSim(spec) {
    var t = build(spec); if (!t) return { ok: false, msg: 'not a valid triangle' };
    if (!(spec.k > 0)) return { ok: false, msg: 'scale factor must be positive' };
    var names = ['AB', 'BC', 'CA', 'AC', 'DE', 'EF', 'FD', 'DF'], k, n;
    (spec.show || []).forEach(function (nm) { /* checked below */ });
    for (var i = 0; i < (spec.show || []).length; i++) {
      var nm = spec.show[i];
      if (names.indexOf(nm) < 0) return { ok: false, msg: 'unknown side ' + nm };
      var tl = trueLen(spec, nm);
      if (tl === null) return { ok: false, msg: 'side lengths need a sides or sas definition' };
      if (Math.abs(tl - Math.round(tl * 1000) / 1000) > 1e-9 && !(spec.lab && spec.lab[nm] !== undefined)) return { ok: false, msg: 'side ' + nm + ' is not a clean number; label it' };
    }
    for (k in (spec.lab || {})) {
      if (names.indexOf(k) < 0) return { ok: false, msg: 'unknown side ' + k };
      n = numOf(spec.lab[k]);
      if (n === null && /\d/.test(spec.lab[k])) return { ok: false, msg: 'label mixes a number with other text' };
      if (n !== null) { var tv = trueLen(spec, k); if (tv === null || Math.abs(tv - n) > 1e-6) return { ok: false, msg: 'side ' + k + ' is labelled ' + spec.lab[k] + ' but drawn as ' + (tv === null ? 'unknown' : Math.round(tv * 100) / 100) }; }
    }
    var order = 'ABCDEF';
    for (k in (spec.ang || {})) {
      var ix = order.indexOf(k); if (ix < 0) return { ok: false, msg: 'unknown vertex ' + k };
      if (typeof spec.ang[k] === 'number' && Math.abs(spec.ang[k] - t.ang[ix % 3]) > 0.6) return { ok: false, msg: 'angle ' + k + ' is drawn as ' + Math.round(t.ang[ix % 3]) + '° not ' + spec.ang[k] + '°' };
    }
    return { ok: true };
  }
  function printedSim(spec) {
    var out = [], k;
    (spec.show || []).forEach(function (nm) { if (!(spec.lab && spec.lab[nm] !== undefined)) out.push([nm, Math.round(trueLen(spec, nm) * 1000) / 1000]); });
    for (k in (spec.lab || {})) { var n = numOf(spec.lab[k]); if (n !== null) out.push([k, n]); }
    for (k in (spec.ang || {})) if (typeof spec.ang[k] === 'number') out.push(['angle ' + k, spec.ang[k]]);
    return out;
  }
  F.printed = function (spec) { return spec && spec.kind === 'geo-sim' ? printedSim(spec) : spec && spec.kind === 'geo-tri-par' ? printedPar(spec) : null; };

  function arcAt(V, u1, u2, r) {
    var p = [V[0] + u1[0] * r, V[1] + u1[1] * r], q = [V[0] + u2[0] * r, V[1] + u2[1] * r], cr = u1[0] * u2[1] - u1[1] * u2[0];
    return '<path d="M' + r1(p[0]) + ' ' + r1(p[1]) + ' A' + r + ' ' + r + ' 0 0 ' + (cr > 0 ? 1 : 0) + ' ' + r1(q[0]) + ' ' + r1(q[1]) + '" stroke="' + INK + '" stroke-width="1.4" fill="none"/>';
  }
  function unit(a, b) { var d = Math.hypot(b[0] - a[0], b[1] - a[1]) || 1; return [(b[0] - a[0]) / d, (b[1] - a[1]) / d]; }

  function inside(P, c, b) {   // the label box corners must lie inside the triangle
    function sgn(p, q, r) { return (p[0] - r[0]) * (q[1] - r[1]) - (q[0] - r[0]) * (p[1] - r[1]); }
    return [[b[0], b[1]], [b[2], b[1]], [b[0], b[3]], [b[2], b[3]]].every(function (pt) {
      var d1 = sgn(pt, P[0], P[1]), d2 = sgn(pt, P[1], P[2]), d3 = sgn(pt, P[2], P[0]);
      return !((d1 < 0 || d2 < 0 || d3 < 0) && (d1 > 0 || d2 > 0 || d3 > 0));
    });
  }
  /* draw a triangle (screen vertices P[0..2]) with side labels, vertex letters, angle marks. names: 3 letters. */
  function drawTri(P, names, sideTxt, angTxt, arcs, sc) {
    var boxes = [];
    function bx(x, y, t) { var w = String(t).length * 7.8 + 6; return [x - w / 2, y - 9, x + w / 2, y + 9]; }
    function hit(b) { for (var q = 0; q < boxes.length; q++) { var c = boxes[q]; if (b[0] < c[2] && b[2] > c[0] && b[1] < c[3] && b[3] > c[1]) return true; } return false; }
    var o = '', cx = (P[0][0] + P[1][0] + P[2][0]) / 3, cy = (P[0][1] + P[1][1] + P[2][1]) / 3, i;
    o += L(P[0], P[1]) + L(P[1], P[2]) + L(P[2], P[0]);
    for (i = 0; i < 3; i++) o += dot(P[i], 3);
    for (i = 0; i < 3; i++) {                                      // vertex letters outside the corner
      var V = P[i], d = unit([cx, cy], V);
      o += T(V[0] + d[0] * 13, V[1] + d[1] * 13, names[i]); boxes.push(bx(V[0] + d[0] * 13, V[1] + d[1] * 13, names[i]));
    }
    for (i = 0; i < 3; i++) {                                      // side labels outside the middle of the side
      var txt = sideTxt[i]; if (!txt) continue;
      var Pa = P[i], Pb = P[(i + 1) % 3], m = [(Pa[0] + Pb[0]) / 2, (Pa[1] + Pb[1]) / 2], n = unit([cx, cy], m), tw = String(txt).length * 7.8 / 2;
      o += T(m[0] + n[0] * (10 + tw * Math.abs(n[0])), m[1] + n[1] * 13, txt); boxes.push(bx(m[0] + n[0] * (10 + tw * Math.abs(n[0])), m[1] + n[1] * 13, txt));
    }
    for (i = 0; i < 3; i++) {                                      // angle arcs / labels inside
      var A0 = P[i], u1 = unit(A0, P[(i + 1) % 3]), u2 = unit(A0, P[(i + 2) % 3]), hasTxt = angTxt[i] !== '' && angTxt[i] !== undefined;
      if (!hasTxt && !arcs[i]) continue;
      var cnt = arcs[i] || 1;
      for (var q = 0; q < cnt; q++) o += arcAt(A0, u1, u2, 15 + q * 4);
      if (hasTxt) {
        var bis = [u1[0] + u2[0], u1[1] + u2[1]], bm = Math.hypot(bis[0], bis[1]) || 1; bis = [bis[0] / bm, bis[1] / bm];
        var tw2 = String(angTxt[i]).length * 7.8 + 6, a = Math.acos(Math.max(-1, Math.min(1, u1[0] * u2[0] + u1[1] * u2[1]))), placed = false;
        var dmax = Math.min(120, 0.62 * Math.min(Math.hypot(A0[0] - P[(i + 1) % 3][0], A0[1] - P[(i + 1) % 3][1]), Math.hypot(A0[0] - P[(i + 2) % 3][0], A0[1] - P[(i + 2) % 3][1])));
        for (var d2 = 28; d2 <= dmax && !placed; d2 += 4) {
          var bb = bx(A0[0] + bis[0] * d2, A0[1] + bis[1] * d2, angTxt[i]);
          if (2 * d2 * Math.tan(a / 2) >= tw2 + 6 && !hit(bb) && inside(P, [A0[0] + bis[0] * d2, A0[1] + bis[1] * d2], bb)) { o += T(A0[0] + bis[0] * d2, A0[1] + bis[1] * d2, angTxt[i]); boxes.push(bb); placed = true; }
        }
        for (var d3 = 26; d3 <= dmax && !placed; d3 += 4) {
          var b3 = bx(A0[0] + bis[0] * d3, A0[1] + bis[1] * d3, angTxt[i]);
          if (2 * d3 * Math.tan(a / 2) >= tw2 + 2 && !hit(b3)) { o += T(A0[0] + bis[0] * d3, A0[1] + bis[1] * d3, angTxt[i]); boxes.push(b3); placed = true; }
        }
        if (!placed) {   // outside the corner, beyond the vertex letter, clear of every other label
          var tries = [34, 44, 54, 64], ox, oy, bo;
          for (var ti = 0; ti < tries.length && !placed; ti++) {
            ox = Math.max(20, Math.min(W - 20, A0[0] - bis[0] * (tries[ti] + tw2 / 2))); oy = A0[1] - bis[1] * (tries[ti] + tw2 / 2); bo = bx(ox, oy, angTxt[i]);
            if (!hit(bo) || ti === tries.length - 1) { var ap = [A0[0] + bis[0] * 15, A0[1] + bis[1] * 15], dl = unit([ox, oy], ap), st = [ox + dl[0] * (Math.abs(dl[0]) * tw2 / 2 + 6), oy + dl[1] * (Math.abs(dl[0]) * tw2 / 2 + 6)]; o += L(st, ap, 0.9) + T(ox, oy, angTxt[i]); boxes.push(bo); placed = true; }
          }
        }
      }
    }
    return o;
  }

  function renderSim(spec) {
    var t = build(spec), k = spec.k, kd = Math.max(1 / 2.2, Math.min(2.2, k)), note = kd !== k ? 'Not drawn to scale.' : '';
    var xs = [t.A[0], t.B[0], t.C[0]], ys = [t.A[1], t.B[1], t.C[1]], w = Math.max.apply(null, xs) - Math.min.apply(null, xs), h = Math.max.apply(null, ys) - Math.min.apply(null, ys);
    var big = Math.max(1, kd), s = Math.min(155 / (w * big), 112 / (h * big)), s1 = s * (kd >= 1 ? 1 : 1), s2 = s * kd;
    function place(sc, x0, y0) { var mnx = Math.min.apply(null, xs); return [t.A, t.B, t.C].map(function (p) { return [x0 + (p[0] - mnx) * sc, y0 - p[1] * sc]; }); }
    var baseY = 34 + Math.max(h * s1, h * s2);
    var P1 = place(s1, 14 + (155 - w * s1) / 2, baseY), P2 = place(s2, 258 + (155 - w * s2) / 2, baseY);
    var sd = [['AB', 'DE'], ['BC', 'EF'], ['CA', 'FD']];
    function sideText(nm) {
      var nm2 = nm === 'CA' ? ['CA', 'AC'] : nm === 'FD' ? ['FD', 'DF'] : [nm], v;
      for (var q = 0; q < nm2.length; q++) {
        if (spec.lab && spec.lab[nm2[q]] !== undefined) return spec.lab[nm2[q]];
        if ((spec.show || []).indexOf(nm2[q]) >= 0) { v = Math.round(trueLen(spec, nm2[q]) * 1000) / 1000; return String(v); }
      }
      return '';
    }
    function arcsFor(vs) { return vs.split('').map(function (c, i) { return spec.marks === true ? i + 1 : Array.isArray(spec.marks) && spec.marks.indexOf(c) >= 0 ? (spec.marks.indexOf(c) >= 0 && 'ABC'.indexOf(c) >= 0 ? i + 1 : i + 1) : 0; }); }
    function angTxt(vtx) { var a = (spec.ang || {})[vtx]; return a === undefined ? '' : typeof a === 'number' ? a + '°' : a; }
    var o = drawTri(P1, ['A', 'B', 'C'], [sideText('AB'), sideText('BC'), sideText('CA')], [angTxt('A'), angTxt('B'), angTxt('C')], arcsFor('ABC'));
    o += drawTri(P2, ['D', 'E', 'F'], [sideText('DE'), sideText('EF'), sideText('FD')], [angTxt('D'), angTxt('E'), angTxt('F')], arcsFor('DEF'));
    return H.wrap(o, Math.ceil(baseY + 48), 'Two similar triangles ABC and DEF', spec.note || note);
  }

  /* ---------- triangle proportionality: DE parallel to BC ---------- */
  function parTri(spec) {
    var v = spec.v, AB = v.AD + v.DB, AC = v.AE + v.EC, t;
    if (spec.schem) { AB = 10; AC = 11.5; }   // schematic: side lengths are NOT to scale, only the division ratio is
    var BCv = spec.schem ? Math.sqrt(AB * AB + AC * AC - 2 * AB * AC * Math.cos((spec.angA || 62) * DEG)) : spec.BC || Math.sqrt(AB * AB + AC * AC - 2 * AB * AC * Math.cos(spec.angA * DEG));
    var bx = (AB * AB + BCv * BCv - AC * AC) / (2 * BCv), by2 = AB * AB - bx * bx;
    if (by2 <= 0) return null;
    return { B: [0, 0], C: [BCv, 0], A: [bx, Math.sqrt(by2)], BC: BCv, AB: AB, AC: AC };
  }
  function checkPar(spec) {
    var v = spec.v, ks = ['AD', 'DB', 'AE', 'EC'], i;
    if (!v) return { ok: false, msg: 'missing lengths' };
    for (i = 0; i < 4; i++) if (!(v[ks[i]] > 0)) return { ok: false, msg: 'lengths must be positive' };
    if (Math.abs(v.AD * v.EC - v.DB * v.AE) > 1e-9) return { ok: false, msg: 'DE is not parallel to BC: AD/DB must equal AE/EC' };
    if (!spec.schem && !(spec.BC > 0) && !(spec.angA > 0 && spec.angA < 180)) return { ok: false, msg: 'need BC or angle A' };
    var t = parTri(spec); if (!t) return { ok: false, msg: 'not a valid triangle' };
    var show = spec.show || [], lab = spec.lab || {}, allowed = ['AD', 'DB', 'AE', 'EC', 'DE', 'BC'], k;
    for (i = 0; i < show.length; i++) {
      if (allowed.indexOf(show[i]) < 0) return { ok: false, msg: 'cannot show ' + show[i] };
      if ((show[i] === 'DE' || show[i] === 'BC') && !(lab[show[i]] !== undefined) && !(spec.BC > 0 && Math.abs(spec.BC - Math.round(spec.BC)) < 1e-9 && show[i] === 'BC') && show[i] === 'DE') return { ok: false, msg: 'DE must be labelled' };
    }
    for (k in lab) {
      if (allowed.indexOf(k) < 0) return { ok: false, msg: 'unknown segment ' + k };
      var n = numOf(lab[k]); if (n === null && /\d/.test(lab[k])) return { ok: false, msg: 'label mixes a number with other text' };
      if (n !== null && !spec.schem) { var tv = k === 'BC' ? t.BC : k === 'DE' ? t.BC * v.AD / (v.AD + v.DB) : v[k]; if (Math.abs(tv - n) > 1e-6) return { ok: false, msg: 'segment ' + k + ' is labelled ' + lab[k] + ' but drawn as ' + Math.round(tv * 100) / 100 }; }
    }
    return { ok: true };
  }
  function printedPar(spec) {
    var out = [], v = spec.v, t = parTri(spec);
    (spec.show || []).forEach(function (k) { if (!(spec.lab && spec.lab[k] !== undefined)) out.push([k, k === 'BC' ? Math.round(t.BC * 1000) / 1000 : v[k]]); });
    for (var k in (spec.lab || {})) { var n = numOf(spec.lab[k]); if (n !== null) out.push([k, n]); }
    return out;
  }
  function renderPar(spec) {
    var v = spec.v, t = parTri(spec), s = Math.min(300 / t.BC, 128 / t.A[1]), x0 = (W - t.BC * s) / 2, y0 = 30 + t.A[1] * s;
    function P(p) { return [x0 + p[0] * s, y0 - p[1] * s]; }
    var A = P(t.A), B = P(t.B), C = P(t.C), r = v.AD / (v.AD + v.DB), D = [A[0] + (B[0] - A[0]) * r, A[1] + (B[1] - A[1]) * r], E = [A[0] + (C[0] - A[0]) * r, A[1] + (C[1] - A[1]) * r];
    var cx = (A[0] + B[0] + C[0]) / 3, cy = (A[1] + B[1] + C[1]) / 3, o = L(A, B) + L(B, C) + L(C, A) + L(D, E) + dot(A, 3) + dot(B, 3) + dot(C, 3) + dot(D, 3) + dot(E, 3);
    function chev(p, q) {
      var m = [(p[0] + q[0]) / 2, (p[1] + q[1]) / 2], u = unit(p, q), nn = [-u[1], u[0]], c = '';
      c += '<path d="M' + r1(m[0] - 7 * u[0] + 5 * nn[0]) + ' ' + r1(m[1] - 7 * u[1] + 5 * nn[1]) + ' L' + r1(m[0]) + ' ' + r1(m[1]) + ' L' + r1(m[0] - 7 * u[0] - 5 * nn[0]) + ' ' + r1(m[1] - 7 * u[1] - 5 * nn[1]) + '" stroke="' + INK + '" stroke-width="1.6" fill="none"/>';
      return c;
    }
    o += chev(D, E).replace(/M/, 'M') + chev(B, C);
    var show = spec.show || [], lab = spec.lab || {};
    function txt(k, def) { return lab[k] !== undefined ? lab[k] : show.indexOf(k) >= 0 ? String(def) : ''; }
    function sl(p, q, text, away) { if (!text) return ''; var m = [(p[0] + q[0]) / 2, (p[1] + q[1]) / 2], n = unit(away, m), tw = text.length * 7.8 / 2; return T(m[0] + n[0] * (10 + tw * Math.abs(n[0])), m[1] + n[1] * 13, text); }
    var cen = [cx, cy], de = t.BC * v.AD / (v.AD + v.DB);
    o += sl(A, D, txt('AD', v.AD), cen) + sl(D, B, txt('DB', v.DB), cen) + sl(A, E, txt('AE', v.AE), cen) + sl(E, C, txt('EC', v.EC), cen) + sl(B, C, txt('BC', Math.round(t.BC * 1000) / 1000), cen);
    var deT = txt('DE', Math.round(de * 1000) / 1000); if (deT) o += T((D[0] + E[0]) / 2, D[1] + 15, deT);
    o += T(A[0], A[1] - 13, 'A') + T(B[0] - 12, B[1] + 8, 'B') + T(C[0] + 12, C[1] + 8, 'C') + T(D[0] - 12, D[1] - 2, 'D') + T(E[0] + 12, E[1] - 2, 'E');
    return H.wrap(o, Math.ceil(y0 + 26), 'Triangle ABC with segment DE parallel to BC', spec.note || '');
  }


  /* geo-shadow: indirect measurement. Two vertical objects and their ground shadows, joined by parallel sun rays.
     spec: { kind:'geo-shadow', h, s, H, S, names:['pole','tree'], unit:'ft', lab:{ H:'x' } }
     h,s = first object height/shadow; H,S = second. All four are TRUE values (so the picture is to scale);
     a lab entry replaces the printed text of one of them (the unknown). The checker requires h/s = H/S. */
  function checkShadow(spec) {
    var k, v = ['h', 's', 'H', 'S'];
    for (k = 0; k < 4; k++) if (!(spec[v[k]] > 0) || !isFinite(spec[v[k]])) return { ok: false, msg: 'heights and shadows must be positive' };
    if (Math.abs(spec.h * spec.S - spec.H * spec.s) > 1e-6) return { ok: false, msg: 'the two objects do not make similar triangles' };
    for (k in (spec.lab || {})) { if (v.indexOf(k) < 0) return { ok: false, msg: 'unknown label ' + k }; var n = numOf(spec.lab[k]); if (n !== null && Math.abs(n - spec[k]) > 1e-6) return { ok: false, msg: k + ' is labelled ' + spec.lab[k] + ' but is drawn as ' + spec[k] }; if (n === null && /\d/.test(spec.lab[k])) return { ok: false, msg: 'label mixes number and text' }; }
    return { ok: true };
  }
  function shadowText(spec, k) { var t = spec.lab && spec.lab[k] !== undefined ? spec.lab[k] : String(spec[k]); return /^\d/.test(t) && spec.unit ? t + ' ' + spec.unit : t; }
  function renderShadow(spec) {
    var gap = 40, sc = Math.min((W - 90 - gap) / (spec.s + spec.S), 118 / Math.max(spec.h, spec.H)), g0 = 36 + Math.max(spec.h, spec.H) * sc, x1 = 40, x2 = x1 + spec.s * sc + gap + 8, out = '', nm = spec.names || ['', ''];
    out += L([14, g0], [W - 14, g0], 2) ;
    function one(x, h, s, th, ts, name, side) {
      var top = [x, g0 - h * sc], foot = [x, g0], tip = [x + s * sc, g0], o = L(foot, top, 2.6) + L(top, tip, 1.8, true) + H.rightMark(foot, 90, 0, 9) + dot(top, 3) + dot(tip, 3);
      o += T(x - 8, (g0 + top[1]) / 2, th, 'end') + T((x + tip[0]) / 2, g0 + 16, ts);
      if (name) o += T(x, top[1] - 12, name);
      return o;
    }
    out += one(x1, spec.h, spec.s, shadowText(spec, 'h'), shadowText(spec, 's'), nm[0]) + one(x2, spec.H, spec.S, shadowText(spec, 'H'), shadowText(spec, 'S'), nm[1]);
    return H.wrap(out, Math.ceil(g0 + 28), 'Two vertical objects and their shadows on level ground, with parallel sun rays', spec.note || 'Sun rays are parallel.');
  }
  function printedShadow(spec) { var out = [], k; ['h', 's', 'H', 'S'].forEach(function (key) { if (!(spec.lab && spec.lab[key] !== undefined)) out.push([key, spec[key]]); }); for (k in (spec.lab || {})) { var n = numOf(spec.lab[k]); if (n !== null) out.push([k, n]); } return out; }
  var prevPrinted = F.printed; F.printed = function (spec) { return spec && spec.kind === 'geo-shadow' ? printedShadow(spec) : prevPrinted(spec); };
  F.extend('geo-shadow', { render: renderShadow, check: checkShadow });
  F.extend('geo-sim', { render: renderSim, check: checkSim });
  F.extend('geo-tri-par', { render: renderPar, check: checkPar });
})(typeof window !== 'undefined' ? window : globalThis);
