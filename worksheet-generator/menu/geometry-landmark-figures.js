/* Triangle-relationship figures (geo-tri) drawn from true geometry.

   mode 'angles'  : triangle ABC from its three interior angles (A bottom-left, B bottom-right, C top)
        angles:[A,B,C]            must sum to 180
        lab:{A:'x°', B:'62°'}     angle labels; a numeric label must equal the drawn angle (a symbol/expression is free text)
        sideLab:{AB:'', BC:'x+3'} optional side labels (text only; the picture is not scaled to them)
        ticks:['AC','BC']         equal-side marks; refused unless those sides really are equal
        ext:{ vertex:'B', lab:'115°' }   extends side AB beyond B and marks the exterior angle (checked = 180 - interior)
   mode 'sides'   : triangle from three side lengths [AB,BC,CA] with numeric labels checked, symbols free
   mode 'midseg'  : D, E midpoints of AB, AC; DE ∥ BC; lab:{DE:'x+3', BC:'30'}
   mode 'centroid': all three medians meeting at the centroid G; lab:{GM:'x+2', AM:'27'}
   mode 'perpbis' : segment AB, its perpendicular bisector through M, point P on it; lab:{PA:'x+4', PB:'11'}
   mode 'altitude': triangle ABC with altitude AD to line BC; obtuse:true puts D outside segment BC; lab:{BC:'12 cm', AD:'x'}
   Constructions are exact (midpoints, centroid at 2/3, perpendicular foot), so the marks are always true. */
(function (G) {
  'use strict';
  var NS = G.MKMENU = (G.MKMENU || {}), F = NS.geoFigures;
  if (!F || !F.extend) return;
  var H = F.h, W = H.W, INK = H.INK, r1 = H.r1, L = H.L, dot = H.dot, DEG = Math.PI / 180;
  function T(x, y, s, anchor) { return H.T(x, y, s, anchor).replace('<text ', '<text stroke="#fff" stroke-width="4" paint-order="stroke" '); }
  function unit(a, b) { var d = Math.hypot(b[0] - a[0], b[1] - a[1]) || 1; return [(b[0] - a[0]) / d, (b[1] - a[1]) / d]; }
  function lerp(p, q, t) { return [p[0] + (q[0] - p[0]) * t, p[1] + (q[1] - p[1]) * t]; }
  function numOf(s) { var m = /^\s*(\d+(?:\.\d+)?)\s*(?:°|cm|units|ft|m)?\s*$/i.exec(String(s)); return m ? Number(m[1]) : null; }
  function boxOf(x, y, t) { var w = String(t).length * 7.8 + 6; return [x - w / 2, y - 9, x + w / 2, y + 9]; }

  /* unit-scale triangle from angles: A=(0,0), B=(1,0), C above */
  function fromAngles(an) {
    var ca = Math.sin(an[1] * DEG) / Math.sin(an[2] * DEG);
    return [[0, 0], [1, 0], [ca * Math.cos(an[0] * DEG), ca * Math.sin(an[0] * DEG)]];
  }
  function fromSides(s) {
    var AB = s[0], BC = s[1], CA = s[2];
    if (!(AB > 0 && BC > 0 && CA > 0) || AB + BC <= CA || BC + CA <= AB || CA + AB <= BC) return null;
    var cx = (AB * AB + CA * CA - BC * BC) / (2 * AB), cy2 = CA * CA - cx * cx; if (cy2 <= 0) return null;
    return [[0, 0], [AB, 0], [cx, Math.sqrt(cy2)]];
  }
  function angleAt(P, i) { var A = P[i], u = unit(A, P[(i + 1) % 3]), v = unit(A, P[(i + 2) % 3]); return Math.acos(Math.max(-1, Math.min(1, u[0] * v[0] + u[1] * v[1]))) / DEG; }

  /* the generic apex triangle used by the segment constructions: B bottom-left, C bottom-right, A on top */
  function apex(spec) { return spec.obtuse ? [[0, 0], [1, 0], [-0.35, 0.75]] : [[0, 0], [1, 0], [0.36, 0.82]]; }   // B, C, A

  function checkTri(spec) {
    var mode = spec.mode, k, n, lab = spec.lab || {};
    if (['angles', 'sides', 'midseg', 'centroid', 'perpbis', 'altitude'].indexOf(mode) < 0) return { ok: false, msg: 'unknown mode' };
    for (k in lab) { n = numOf(lab[k]); if (n === null && /^\d/.test(String(lab[k]).trim()) && !/[a-z]/i.test(lab[k])) return { ok: false, msg: 'bad label ' + lab[k] }; }
    if (mode === 'angles') {
      var an = spec.angles;
      if (!an || an.length !== 3 || an.some(function (a) { return !(a > 0); }) || Math.abs(an[0] + an[1] + an[2] - 180) > 1e-6) return { ok: false, msg: 'angles must be positive and sum to 180' };
      var names = ['A', 'B', 'C'];
      for (k in lab) { var ix = names.indexOf(k); if (ix < 0) return { ok: false, msg: 'unknown vertex ' + k }; n = numOf(lab[k]); if (n !== null && Math.abs(n - an[ix]) > 0.6) return { ok: false, msg: 'angle ' + k + ' is drawn as ' + Math.round(an[ix]) + '° not ' + lab[k] }; }
      (spec.ticks || []).forEach(function () { });
      if (spec.ticks && spec.ticks.length) {
        var opp = { AB: 2, BC: 0, CA: 1, AC: 1 }, a0 = an[opp[spec.ticks[0]]];
        for (var i = 1; i < spec.ticks.length; i++) if (Math.abs(an[opp[spec.ticks[i]]] - a0) > 1e-6) return { ok: false, msg: 'tick marks claim ' + spec.ticks.join(' and ') + ' are equal' };
      }
      if (spec.ext) {
        var vi = names.indexOf(spec.ext.vertex); if (vi !== 1) return { ok: false, msg: 'exterior angle is drawn at vertex B' };
        n = numOf(spec.ext.lab); if (n !== null && Math.abs(n - (180 - an[1])) > 0.6) return { ok: false, msg: 'exterior angle is drawn as ' + Math.round(180 - an[1]) + '°' };
      }
    } else if (mode === 'sides') {
      if (!spec.sides || !fromSides(spec.sides)) return { ok: false, msg: 'not a valid triangle' };
      var sd = { AB: spec.sides[0], BC: spec.sides[1], CA: spec.sides[2], AC: spec.sides[2] };
      for (k in (spec.sideLab || {})) { if (sd[k] === undefined) return { ok: false, msg: 'unknown side ' + k }; n = numOf(spec.sideLab[k]); if (n !== null && Math.abs(n - sd[k]) > 1e-6) return { ok: false, msg: 'side ' + k + ' is labelled ' + spec.sideLab[k] + ' but drawn as ' + sd[k] }; }
    } else if (mode === 'perpbis') {
      var okk = ['PA', 'PB', 'AB']; for (k in lab) if (okk.indexOf(k) < 0) return { ok: false, msg: 'unknown segment ' + k };
    } else if (mode === 'midseg') { for (k in lab) if (['DE', 'BC', 'AD', 'DB', 'AE', 'EC'].indexOf(k) < 0) return { ok: false, msg: 'unknown segment ' + k }; }
    else if (mode === 'centroid') { for (k in lab) if (['GM', 'AG', 'AM'].indexOf(k) < 0) return { ok: false, msg: 'unknown segment ' + k }; }
    else if (mode === 'altitude') { for (k in lab) if (['BC', 'AD'].indexOf(k) < 0) return { ok: false, msg: 'unknown segment ' + k }; }
    return { ok: true };
  }
  F.printedTri = function (spec) {
    var out = [], k, n;
    ['lab', 'sideLab'].forEach(function (f) { for (k in (spec[f] || {})) { n = numOf(spec[f][k]); if (n !== null) out.push([k, n]); } });
    if (spec.ext) { n = numOf(spec.ext.lab); if (n !== null) out.push(['exterior', n]); }
    return out;
  };
  var prevPrinted = F.printed;
  F.printed = function (spec) { return spec && spec.kind === 'geo-tri' ? F.printedTri(spec) : prevPrinted ? prevPrinted(spec) : null; };

  /* ---------- drawing helpers (screen coordinates, y down) ---------- */
  function arc(V, u1, u2, r) {
    var p = [V[0] + u1[0] * r, V[1] + u1[1] * r], q = [V[0] + u2[0] * r, V[1] + u2[1] * r], cr = u1[0] * u2[1] - u1[1] * u2[0];
    return '<path d="M' + r1(p[0]) + ' ' + r1(p[1]) + ' A' + r + ' ' + r + ' 0 0 ' + (cr > 0 ? 1 : 0) + ' ' + r1(q[0]) + ' ' + r1(q[1]) + '" stroke="' + INK + '" stroke-width="1.4" fill="none"/>';
  }
  function tick(p, q, n) {
    var m = lerp(p, q, 0.5), u = unit(p, q), nn = [-u[1], u[0]], o = '';
    for (var j = 0; j < n; j++) { var c = [m[0] + u[0] * (j - (n - 1) / 2) * 5, m[1] + u[1] * (j - (n - 1) / 2) * 5]; o += '<path d="M' + r1(c[0] - nn[0] * 6) + ' ' + r1(c[1] - nn[1] * 6) + ' L' + r1(c[0] + nn[0] * 6) + ' ' + r1(c[1] + nn[1] * 6) + '" stroke="' + INK + '" stroke-width="1.7"/>'; }
    return o;
  }
  function rightAt(V, a, b, s) { var u = unit(V, a), v = unit(V, b), p = [V[0] + u[0] * s, V[1] + u[1] * s], q = [p[0] + v[0] * s, p[1] + v[1] * s], z = [V[0] + v[0] * s, V[1] + v[1] * s]; return '<path d="M' + r1(p[0]) + ' ' + r1(p[1]) + ' L' + r1(q[0]) + ' ' + r1(q[1]) + ' L' + r1(z[0]) + ' ' + r1(z[1]) + '" stroke="' + INK + '" stroke-width="1.5" fill="none"/>'; }
  function side(p, q, text, away, extra) {            // label outside the middle of segment p-q, away from point `away`
    if (!text) return '';
    var m = lerp(p, q, 0.5), n = unit(away, m), tw = String(text).length * 7.8 / 2, off = extra || 12;
    return T(m[0] + n[0] * (off + tw * Math.abs(n[0])), m[1] + n[1] * (off + 2), text);
  }
  function fit(pts, bw, bh) {            // scale/offset mapping math coords (y up) into a bw x bh box centred horizontally, bottom at yb
    var xs = pts.map(function (p) { return p[0]; }), ys = pts.map(function (p) { return p[1]; }), mnx = Math.min.apply(null, xs), mxx = Math.max.apply(null, xs), mny = Math.min.apply(null, ys), mxy = Math.max.apply(null, ys);
    var s = Math.min(bw / (mxx - mnx || 1), bh / (mxy - mny || 1)), x0 = (W - (mxx - mnx) * s) / 2 - mnx * s, y0 = 46 + (mxy) * s;
    return { map: function (p) { return [x0 + p[0] * s, y0 - p[1] * s]; }, h: (mxy - mny) * s + 46 + 38, s: s };
  }
  function inTri(p, T) { var s1 = (T[1][0] - T[0][0]) * (p[1] - T[0][1]) - (T[1][1] - T[0][1]) * (p[0] - T[0][0]), s2 = (T[2][0] - T[1][0]) * (p[1] - T[1][1]) - (T[2][1] - T[1][1]) * (p[0] - T[1][0]), s3 = (T[0][0] - T[2][0]) * (p[1] - T[2][1]) - (T[0][1] - T[2][1]) * (p[0] - T[2][0]); return (s1 >= 0 && s2 >= 0 && s3 >= 0) || (s1 <= 0 && s2 <= 0 && s3 <= 0); }
  function angleLabel(V, u1, u2, text, boxes, tri) {
    var o = arc(V, u1, u2, 18), bis = [u1[0] + u2[0], u1[1] + u2[1]], bm = Math.hypot(bis[0], bis[1]) || 1; bis = [bis[0] / bm, bis[1] / bm];
    var a = Math.acos(Math.max(-1, Math.min(1, u1[0] * u2[0] + u1[1] * u2[1]))), tw = String(text).length * 7.8 + 6;
    for (var d = 32; d <= 90; d += 4) {
      var c = [V[0] + bis[0] * d, V[1] + bis[1] * d], b = boxOf(c[0], c[1], text), bad = false;
      if (2 * d * Math.tan(a / 2) < tw + 18) continue;
      if (tri && !(inTri([b[0], b[1]], tri) && inTri([b[2], b[1]], tri) && inTri([b[0], b[3]], tri) && inTri([b[2], b[3]], tri))) continue;
      for (var q = 0; q < boxes.length; q++) { var z = boxes[q]; if (b[0] < z[2] && b[2] > z[0] && b[1] < z[3] && b[3] > z[1]) bad = true; }
      if (!bad) { boxes.push(b); return o + T(c[0], c[1], text); }
    }
    var oc = [V[0] - bis[0] * (22 + tw / 2), V[1] - bis[1] * (22 + tw / 2)]; boxes.push(boxOf(oc[0], oc[1], text)); return o + T(oc[0], oc[1], text);
  }

  function render(spec) {
    var mode = spec.mode, o = '', alt = 'A triangle', note = spec.note || '';
    if (mode === 'angles' || mode === 'sides') {
      var P0 = mode === 'angles' ? fromAngles(spec.angles) : fromSides(spec.sides), allp = P0.slice();
      if (spec.ext) allp.push([P0[1][0] + (P0[1][0] - P0[0][0]) * 0.45, P0[1][1]]);
      var f = fit(allp, 250, 112), P = P0.map(f.map), cen = [(P[0][0] + P[1][0] + P[2][0]) / 3, (P[0][1] + P[1][1] + P[2][1]) / 3], boxes = [], nm = ['A', 'B', 'C'];
      o += L(P[0], P[1]) + L(P[1], P[2]) + L(P[2], P[0]) + dot(P[0], 3) + dot(P[1], 3) + dot(P[2], 3);
      if (spec.ext) {
        var Bx = [P[1][0] + 0.45 * (P[1][0] - P[0][0]), P[1][1]];
        o += L(P[1], Bx);
        var uC = unit(P[1], P[2]), uE = [1, 0], tx = spec.ext.lab;
        o += arc(P[1], uE, uC, 20) + T(P[1][0] + 38, P[1][1] - 18, tx);
        boxes.push(boxOf(P[1][0] + 38, P[1][1] - 18, tx));
      }
      for (var i = 0; i < 3; i++) { var d = unit(cen, P[i]); o += T(P[i][0] + d[0] * 14, P[i][1] + d[1] * 14, nm[i]); boxes.push(boxOf(P[i][0] + d[0] * 14, P[i][1] + d[1] * 14, nm[i])); }
      for (i = 0; i < 3; i++) {
        var lt = (spec.lab || {})[nm[i]]; if (!lt) continue;
        o += angleLabel(P[i], unit(P[i], P[(i + 1) % 3]), unit(P[i], P[(i + 2) % 3]), lt, boxes, P);
      }
      var sl = spec.sideLab || {}, segs = [['AB', 0, 1], ['BC', 1, 2], ['CA', 2, 0]];
      segs.forEach(function (sg) { var t = sl[sg[0]] !== undefined ? sl[sg[0]] : (sg[0] === 'CA' ? sl.AC : undefined); if (t) o += side(P[sg[1]], P[sg[2]], t, cen, 12); });
      var tk = spec.ticks || [], mp = { AB: [0, 1], BC: [1, 2], CA: [2, 0], AC: [2, 0] }; tk.forEach(function (t) { o += tick(P[mp[t][0]], P[mp[t][1]], 1); });
      if (mode === 'sides' && !note) note = 'Not drawn to scale.';
      return H.wrap(o, Math.ceil(f.h + (spec.ext ? 6 : 0)), alt + ' ABC with its measures labelled', note);
    }
    var Q = apex(spec);                              // B, C, A in math coords
    if (mode === 'midseg' || mode === 'centroid' || mode === 'altitude') {
      var extraPts = Q.slice(); if (mode === 'altitude') { var dm = footOf(Q[2], Q[0], Q[1]); extraPts.push(dm); }
      var g = fit(extraPts, 270, 120), B = g.map(Q[0]), C = g.map(Q[1]), A = g.map(Q[2]), cenT = [(A[0] + B[0] + C[0]) / 3, (A[1] + B[1] + C[1]) / 3];
      var lb = spec.lab || {};
      o += L(B, C) + L(C, A) + L(A, B) + dot(A, 3) + dot(B, 3) + dot(C, 3);
      var vl = function (p, t, away) { var d = unit(away, p); return T(p[0] + d[0] * 14, p[1] + d[1] * 14, t); };
      o += vl(A, 'A', cenT) + vl(B, 'B', cenT) + vl(C, 'C', cenT);
      if (mode === 'midseg') {
        var D = lerp(A, B, 0.5), E = lerp(A, C, 0.5);
        o += L(D, E) + dot(D, 3) + dot(E, 3) + tick(A, D, 1) + tick(D, B, 1) + tick(A, E, 2) + tick(E, C, 2);
        o += vl(D, 'D', cenT) + vl(E, 'E', cenT);
        if (lb.DE) o += T((D[0] + E[0]) / 2, D[1] + 15, lb.DE);
        if (lb.BC) o += T((B[0] + C[0]) / 2, B[1] + 16, lb.BC);
        return H.wrap(o, Math.ceil(g.h), 'Triangle ABC with midsegment DE', note);
      }
      if (mode === 'centroid') {
        var M = lerp(B, C, 0.5), N1 = lerp(A, C, 0.5), N2 = lerp(A, B, 0.5), Gp = [(A[0] + B[0] + C[0]) / 3, (A[1] + B[1] + C[1]) / 3];
        o += L(A, M) + L(B, N1, 1.6, true) + L(C, N2, 1.6, true) + dot(M, 3) + dot(Gp, 4) + tick(B, M, 1) + tick(M, C, 1);
        o += T(M[0], M[1] + 16, 'M') + T(Gp[0] + 12, Gp[1] - 4, 'G', 'start');
        var gm = lerp(Gp, M, 0.5), am = lerp(A, M, 0.5);
        if (lb.GM) o += T(gm[0] - 4, gm[1], lb.GM, 'end');
        if (lb.AG) o += T(lerp(A, Gp, 0.5)[0] - 4, lerp(A, Gp, 0.5)[1], lb.AG, 'end');
        if (lb.AM) o += T(am[0] + 12, am[1] - 22, lb.AM, 'start');
        return H.wrap(o, Math.ceil(g.h), 'Triangle ABC with its medians meeting at the centroid G', note);
      }
      var Dd = g.map(footOf(Q[2], Q[0], Q[1]));
      if (spec.obtuse) o += L(Dd[0] < B[0] ? B : C, Dd, 1.8, true);
      o += L(A, Dd) + dot(Dd, 3) + rightAt(Dd, A, Dd[0] < B[0] ? B : C, 9) + T(Dd[0], Dd[1] + 16, 'D');
      if (lb.BC) o += T(B[0] + (C[0] - B[0]) * 0.74, B[1] + 16, lb.BC);
      if (lb.AD) o += T((A[0] + Dd[0]) / 2 + 12, (A[1] + Dd[1]) / 2, lb.AD, 'start');
      return H.wrap(o, Math.ceil(g.h), 'Triangle ABC with altitude AD', note);
    }
    // perpendicular bisector: A and B on a horizontal segment, P above the midpoint
    var pts = [[0, 0], [1, 0], [0.5, 0.72]], h = fit(pts, 240, 112), a = h.map([0, 0]), b = h.map([1, 0]), p = h.map([0.5, 0.72]), m = h.map([0.5, 0]), lbl = spec.lab || {};
    o += L(a, b) + L(p, a) + L(p, b) + L(p, m, 2.2, true) + dot(a, 3) + dot(b, 3) + dot(p, 3) + dot(m, 3) + tick(a, m, 1) + tick(m, b, 1) + rightAt(m, p, b, 9);
    o += T(a[0] - 13, a[1] + 4, 'A') + T(b[0] + 13, b[1] + 4, 'B') + T(p[0], p[1] - 14, 'P') + T(m[0], m[1] + 16, 'M');
    if (lbl.PA) o += T((p[0] + a[0]) / 2 - 12 - lbl.PA.length * 3, (p[1] + a[1]) / 2, lbl.PA);
    if (lbl.PB) o += T((p[0] + b[0]) / 2 + 12 + lbl.PB.length * 3, (p[1] + b[1]) / 2, lbl.PB);
    if (lbl.AB) o += T((a[0] + b[0]) / 2, a[1] + 32, lbl.AB);
    return H.wrap(o, Math.ceil(h.h), 'Segment AB with its perpendicular bisector through M and point P on it', note);
  }
  function footOf(P, Aa, Bb) {                       // foot of the perpendicular from P to line A-B (math coords)
    var d = [Bb[0] - Aa[0], Bb[1] - Aa[1]], t = ((P[0] - Aa[0]) * d[0] + (P[1] - Aa[1]) * d[1]) / (d[0] * d[0] + d[1] * d[1]);
    return [Aa[0] + d[0] * t, Aa[1] + d[1] * t];
  }

  F.extend('geo-tri', { render: render, check: checkTri });
})(typeof window !== 'undefined' ? window : globalThis);
