/* Data-driven right-triangle figures (geo-rt) for Right Triangles and Trigonometry.
   spec: { kind:'geo-rt',
           v:{ a, b },               // true leg lengths: a = horizontal leg, b = vertical leg (the right angle sits at C)
           show:['a','b','c'],       // sides whose true length is printed (default: none)
           lab:{ a:'x', c:'13' },    // printed text replaces the true value (an unknown, or a given with its unit)
           ang:{ B:30, A:'θ' },      // number = degrees, checked against the drawn angle; string = a symbol
           unit:'ft', flip:false, scene:'plain'|'depression', note:'' }
   The picture is scaled from v, so a numeric label that disagrees with the true triangle makes the figure invalid. */
(function (G) {
  'use strict';
  var NS = G.MKMENU = (G.MKMENU || {}), F = NS.geoFigures;
  if (!F || !F.extend) return;
  var H = F.h, W = H.W, INK = H.INK, r1 = H.r1, L = H.L, dot = H.dot;

  function T(x, y, s, anchor) { return H.T(x, y, s, anchor).replace('<text ', '<text stroke="#fff" stroke-width="4" paint-order="stroke" '); }
  function num(s) { var m = /^\s*(\d+(?:\.\d+)?)\s*(?:[a-z ]*)$/i.exec(String(s)); return m ? Number(m[1]) : null; }
  function hyp(v) { return Math.sqrt(v.a * v.a + v.b * v.b); }
  function clean(n) { return Math.abs(n - Math.round(n * 1000) / 1000) < 1e-9; }

  function check(spec) {
    var v = spec.v;
    if (!v || !(v.a > 0) || !(v.b > 0) || !isFinite(v.a) || !isFinite(v.b)) return { ok: false, msg: 'legs must be positive numbers' };
    var c = hyp(v), lab = spec.lab || {}, i, k;
    var show = spec.show || [];
    for (i = 0; i < show.length; i++) {
      k = show[i];
      if (['a', 'b', 'c'].indexOf(k) < 0) return { ok: false, msg: 'cannot show ' + k };
      if (lab[k] === undefined && k === 'c' && !clean(c)) return { ok: false, msg: 'hypotenuse is not a clean number; label it' };
    }
    for (k in lab) {
      if (['a', 'b', 'c'].indexOf(k) < 0) return { ok: false, msg: 'unknown side ' + k };
      var n = num(lab[k]), tv = k === 'c' ? c : v[k];
      if (n !== null && Math.abs(n - tv) > 1e-6) return { ok: false, msg: 'side ' + k + ' is labelled ' + lab[k] + ' but is drawn as ' + r1(tv) };
      if (n === null && /\d/.test(lab[k])) return { ok: false, msg: 'label ' + lab[k] + ' mixes a number with other text' };
    }
    var angB = Math.atan2(v.b, v.a) * 180 / Math.PI, ang = spec.ang || {};
    if (typeof ang.B === 'number' && Math.abs(ang.B - angB) > 0.6) return { ok: false, msg: 'angle B is drawn as ' + Math.round(angB) + '° not ' + ang.B + '°' };
    if (typeof ang.A === 'number' && Math.abs(ang.A - (90 - angB)) > 0.6) return { ok: false, msg: 'angle A is drawn as ' + Math.round(90 - angB) + '° not ' + ang.A + '°' };
    if (spec.scene && ['plain', 'depression'].indexOf(spec.scene) < 0) return { ok: false, msg: 'unknown scene' };
    return { ok: true };
  }

  function sideText(spec, k) {
    var lab = spec.lab || {};
    if (lab[k] !== undefined) return lab[k];
    if ((spec.show || []).indexOf(k) < 0) return '';
    var n = k === 'c' ? Math.round(hyp(spec.v) * 1000) / 1000 : spec.v[k];
    return n + (spec.unit ? ' ' + spec.unit : '');
  }
  function angText(x) { return typeof x === 'number' ? x + '°' : (x || ''); }
  function unit(a, b) { var d = Math.hypot(b[0] - a[0], b[1] - a[1]) || 1; return [(b[0] - a[0]) / d, (b[1] - a[1]) / d]; }
  function arc(V, u1, u2, r) {
    var p = [V[0] + u1[0] * r, V[1] + u1[1] * r], q = [V[0] + u2[0] * r, V[1] + u2[1] * r], cross = u1[0] * u2[1] - u1[1] * u2[0];
    return '<path d="M' + r1(p[0]) + ' ' + r1(p[1]) + ' A' + r + ' ' + r + ' 0 0 ' + (cross > 0 ? 1 : 0) + ' ' + r1(q[0]) + ' ' + r1(q[1]) + '" stroke="' + INK + '" stroke-width="1.5" fill="none"/>';
  }
  /* label an angle at V between unit vectors u1, u2: inside the wedge when it is wide enough, otherwise just outside the vertex */
  function angleMark(V, u1, u2, text, outward, maxD) {
    var out = arc(V, u1, u2, 22);
    if (!text) return out;
    var bis = [u1[0] + u2[0], u1[1] + u2[1]], m = Math.hypot(bis[0], bis[1]) || 1; bis = [bis[0] / m, bis[1] / m];
    var tw = String(text).length * 7.8 + 6, dot_ = Math.max(-1, Math.min(1, u1[0] * u2[0] + u1[1] * u2[1])), a = Math.acos(dot_);
    for (var d = 36; d <= 70; d += 6) if (2 * d * Math.tan(a / 2) >= tw + 8 && d + tw / 2 <= (maxD || 90)) return out + T(V[0] + bis[0] * d, V[1] + bis[1] * d, text);
    var o = outward || bis, dd = 20 + tw / 2 + 4;
    return out + T(V[0] + o[0] * dd, V[1] + o[1] * dd, text);
  }

  function render(spec) {
    var v = spec.v, flip = !!spec.flip, dep = spec.scene === 'depression', clamped = false;
    var s = Math.min(230 / v.a, 112 / v.b);
    function px(n) { var d = n * s; if (d < 44) { clamped = true; return 44; } return d; }
    var pa = px(v.a), pb = px(v.b), ex = flip ? -1 : 1, x0 = (W - pa) / 2, y0 = 52 + pb;
    var C = [flip ? x0 + pa : x0, y0], B = [C[0] + ex * pa, y0], A = [C[0], y0 - pb], out = '';
    out += L(C, B) + L(C, A) + L(A, B) + H.rightMark(C, 90, flip ? 180 : 0, 10) + dot(A, 3) + dot(B, 3) + dot(C, 3);
    var ang = spec.ang || {}, ta = sideText(spec, 'a'), tb = sideText(spec, 'b'), tc = sideText(spec, 'c');
    if (ta) out += T((C[0] + B[0]) / 2, y0 + 15, ta);
    if (tb) out += T(C[0] - ex * 8, (C[1] + A[1]) / 2, tb, flip ? 'start' : 'end');
    if (tc) {
      var mid = [(A[0] + B[0]) / 2, (A[1] + B[1]) / 2], nrm = [-(B[1] - A[1]), B[0] - A[0]], nl = Math.hypot(nrm[0], nrm[1]);
      nrm = [nrm[0] / nl, nrm[1] / nl]; if (nrm[1] > 0 || (Math.abs(nrm[1]) < 1e-6 && nrm[0] * ex < 0)) nrm = [-nrm[0], -nrm[1]];
      var tw = String(tc).length * 7.8 / 2;
      out += T(mid[0] + nrm[0] * (10 + tw * Math.abs(nrm[0])), mid[1] + nrm[1] * 15, tc);
    }
    var uCB = unit(B, C), uAB = unit(B, A), uCA = unit(A, C), uBA = unit(A, B);
    if (angText(ang.B) && !dep) out += angleMark(B, uCB, uAB, angText(ang.B), [ex, 0], pa * 0.85);
    if (dep) {
      var hz = [ex, 0];                                   // horizontal ray from the observer at A, dashed
      out += L(A, [A[0] + ex * (pa + 26), A[1]], 1.8, true) + angleMark(A, hz, uBA, angText(ang.A !== undefined ? ang.A : ang.B), [ex, 0]);
    } else if (angText(ang.A)) out += angleMark(A, uCA, uBA, angText(ang.A), [0, -1], pb * 0.85);
    return H.wrap(out, Math.ceil(y0 + 28), 'A right triangle with its sides and angles labelled', spec.note || (clamped ? 'Not drawn to scale.' : ''));
  }

  F.extend('geo-rt', { render: render, check: check });

  /* Oblique triangles for the Law of Sines and Law of Cosines (geo-oblique).
     spec: { kind:'geo-oblique', A:deg, B:deg, lab:{ a:'12', b:'?' }, ang:{ A:'40°', C:'?' } }
     The shape is drawn from the true angles A and B (C = 180 − A − B); side a is opposite A, and so on.
     A numeric side label must agree with the Law of Sines ratios of the drawn triangle, and a numeric angle label with its angle. */
  function oblShape(spec) {
    var A = spec.A * Math.PI / 180, B = spec.B * Math.PI / 180, Cr = Math.PI - A - B, c = 1, b = c * Math.sin(B) / Math.sin(Cr), a = c * Math.sin(A) / Math.sin(Cr);
    return { a: a, b: b, c: c, P: { A: [0, 0], B: [c, 0], C: [b * Math.cos(A), b * Math.sin(A)] } };
  }
  function oblCheck(spec) {
    if (!(spec.A > 0 && spec.B > 0 && spec.A + spec.B < 180)) return { ok: false, msg: 'angles must form a triangle' };
    var sh = oblShape(spec), lab = spec.lab || {}, ang = spec.ang || {}, k = null, key, n;
    for (key in lab) {
      if (['a', 'b', 'c'].indexOf(key) < 0) return { ok: false, msg: 'unknown side ' + key };
      n = num(lab[key]); if (n === null) continue;
      if (k === null) k = n / sh[key]; else if (Math.abs(n / sh[key] - k) > 0.006 * k) return { ok: false, msg: 'side labels disagree with the angles' };
    }
    var trueAng = { A: spec.A, B: spec.B, C: 180 - spec.A - spec.B };
    for (key in ang) { if (!trueAng[key]) return { ok: false, msg: 'unknown angle ' + key }; n = num(String(ang[key]).replace('°', '')); if (n !== null && Math.abs(n - trueAng[key]) > 0.05) return { ok: false, msg: 'angle label disagrees with the drawing' }; }
    return { ok: true };
  }
  function oblRender(spec) {
    var sh = oblShape(spec), P = sh.P, xs = [P.A[0], P.B[0], P.C[0]], ys = [P.A[1], P.B[1], P.C[1]];
    var minX = Math.min.apply(null, xs), maxX = Math.max.apply(null, xs), maxY = Math.max.apply(null, ys);
    var sc = Math.min(300 / (maxX - minX), 150 / maxY), ox = (W - (maxX - minX) * sc) / 2 - minX * sc, top = 30, y0 = top + maxY * sc;
    var X = function (q) { return [ox + q[0] * sc, y0 - q[1] * sc]; }, A = X(P.A), B = X(P.B), Cp = X(P.C), G = [(A[0] + B[0] + Cp[0]) / 3, (A[1] + B[1] + Cp[1]) / 3];
    var out = L(A, B) + L(B, Cp) + L(Cp, A);
    var away = function (q, d) { var v = [q[0] - G[0], q[1] - G[1]], l = Math.hypot(v[0], v[1]) || 1; return [q[0] + v[0] / l * d, q[1] + v[1] / l * d + 5]; };
    [['A', A], ['B', B], ['C', Cp]].forEach(function (pv) { var t = away(pv[1], 16); out += H.T(t[0], t[1], pv[0], 'middle', true); });
    var lab = spec.lab || {}, ang = spec.ang || {}, side = { a: [B, Cp], b: [Cp, A], c: [A, B] };
    Object.keys(lab).forEach(function (k) { if (!lab[k]) return; var s2 = side[k], m = [(s2[0][0] + s2[1][0]) / 2, (s2[0][1] + s2[1][1]) / 2], t = away(m, 18 + (String(lab[k]).length + 4) * 3); out += T(t[0], t[1], k + ' = ' + lab[k], 'middle'); });
    var V = { A: A, B: B, C: Cp };
    var NB = { A: [B, Cp], B: [Cp, A], C: [A, B] };
    Object.keys(ang).forEach(function (k) {   // on the angle bisector, far enough from both sides to stay clear of them
      var q = V[k], u1 = [NB[k][0][0] - q[0], NB[k][0][1] - q[1]], u2 = [NB[k][1][0] - q[0], NB[k][1][1] - q[1]], l1 = Math.hypot(u1[0], u1[1]), l2 = Math.hypot(u2[0], u2[1]);
      u1 = [u1[0] / l1, u1[1] / l1]; u2 = [u2[0] / l2, u2[1] / l2];
      var bis = [u1[0] + u2[0], u1[1] + u2[1]], lb = Math.hypot(bis[0], bis[1]) || 1, half = Math.acos(Math.max(-1, Math.min(1, u1[0] * u2[0] + u1[1] * u2[1]))) / 2;
      var d = Math.max(22, Math.min(Math.min(l1, l2) * 0.6, 15 / Math.max(Math.sin(half), 0.2)));
      out += T(q[0] + bis[0] / lb * d, q[1] + bis[1] / lb * d + 4, String(ang[k]), 'middle');
    });
    return H.wrap(out, Math.ceil(y0 + 34), 'A triangle ABC with its given sides and angles labelled', '');
  }
  F.extend('geo-oblique', { render: oblRender, check: oblCheck });
  /* ---------- coverage additions: composite plane figures, two transversals between parallel lines, a protractor ---------- */
  function pts2(P) { return P.map(function (q) { return r1(q[0]) + ',' + r1(q[1]); }).join(' '); }
  function poly(P, dash) { return '<polygon points="' + pts2(P) + '" fill="none" stroke="' + INK + '" stroke-width="2"' + (dash ? ' stroke-dasharray="5 4"' : '') + '/>'; }
  function lab(x, y, s) { return T(x, y, s, 'middle'); }
  /* geo-comp: { shape:'L'|'rect-semi'|'house'|'hole', d:{…}, unit } — drawn to scale from d */
  function compCheck(spec) {
    var d = spec.d || {}, pos = function (k) { return typeof d[k] === 'number' && d[k] > 0; };
    if (spec.shape === 'L') return pos('w') && pos('h') && pos('a') && pos('b') && d.a < d.w && d.b < d.h ? { ok: true } : { ok: false, msg: 'bad L-shape' };
    if (spec.shape === 'rect-semi' || spec.shape === 'house') return pos('w') && pos('h') && (spec.shape === 'rect-semi' || pos('t')) ? { ok: true } : { ok: false, msg: 'bad composite figure' };
    if (spec.shape === 'hole') return pos('W') && pos('H') && pos('s') && d.s < Math.min(d.W, d.H) ? { ok: true } : { ok: false, msg: 'bad figure with a hole' };
    return { ok: false, msg: 'unknown composite shape' };
  }
  function compRender(spec) {
    var d = spec.d, u = spec.unit ? ' ' + spec.unit : '', out = '', w = d.w || d.W, h = d.h || d.H, extra = spec.shape === 'rect-semi' ? w / 2 : spec.shape === 'house' ? d.t : 0;
    var sc = Math.min(260 / w, 140 / (h + extra)), x0 = (W - w * sc) / 2, y0 = 20 + (h + extra) * sc, X = function (x) { return x0 + x * sc; }, Y = function (y) { return y0 - y * sc; };
    if (spec.shape === 'L') { out += poly([[X(0), Y(0)], [X(w), Y(0)], [X(w), Y(h - d.b)], [X(w - d.a), Y(h - d.b)], [X(w - d.a), Y(h)], [X(0), Y(h)]]);
      out += lab(X(w / 2), Y(0) + 18, w + u) + T(X(0) - 8, Y(h / 2) + 4, h + u, 'end') + lab(X(w - d.a / 2), Y(h - d.b) - 8, d.a + u) + T(X(w - d.a) - 6, Y(h - d.b / 2) + 4, d.b + u, 'end'); }
    else if (spec.shape === 'hole') { var s = d.s; out += poly([[X(0), Y(0)], [X(w), Y(0)], [X(w), Y(h)], [X(0), Y(h)]]) + poly([[X((w - s) / 2), Y((h - s) / 2)], [X((w + s) / 2), Y((h - s) / 2)], [X((w + s) / 2), Y((h + s) / 2)], [X((w - s) / 2), Y((h + s) / 2)]]);
      out += lab(X(w / 2), Y(0) + 18, w + u) + T(X(0) - 8, Y(h / 2) + 4, h + u, 'end') + lab(X(w / 2), Y((h + s) / 2) - 6, s + u); }
    else { out += L([X(0), Y(h)], [X(0), Y(0)]) + L([X(0), Y(0)], [X(w), Y(0)]) + L([X(w), Y(0)], [X(w), Y(h)]) + L([X(0), Y(h)], [X(w), Y(h)], 1.4, true);
      if (spec.shape === 'rect-semi') { var R = w / 2 * sc; out += '<path d="M' + r1(X(0)) + ' ' + r1(Y(h)) + ' A' + r1(R) + ' ' + r1(R) + ' 0 0 1 ' + r1(X(w)) + ' ' + r1(Y(h)) + '" fill="none" stroke="' + INK + '" stroke-width="2"/>'; }
      else { out += L([X(0), Y(h)], [X(w / 2), Y(h + d.t)]) + L([X(w / 2), Y(h + d.t)], [X(w), Y(h)]) + L([X(w / 2), Y(h)], [X(w / 2), Y(h + d.t)], 1.2, true) + T(X(w / 2) + 6, Y(h + d.t / 2) + 4, d.t + u, 'start'); }
      out += lab(X(w / 2), Y(0) + 18, w + u) + T(X(w) + 8, Y(h / 2) + 4, h + u, 'start'); }
    return H.wrap(out, Math.ceil(y0 + 28), 'A composite figure with its dimensions labelled', spec.shape === 'rect-semi' ? 'The curved part is a semicircle.' : spec.shape === 'house' ? 'The top is a triangle; the dashed segment is its height.' : spec.shape === 'hole' ? 'The square in the middle is cut out.' : '');
  }
  F.extend('geo-comp', { render: compRender, check: compCheck });
  /* geo-two-trans: two parallel lines; transversals from P on the top line to Q and R on the bottom line.
     a = interior angle at Q, b = interior angle at R; labels at Q, R, PL (= a), PR (= b), PM (= 180 − a − b). */
  function ttVals(spec) { return { Q: spec.a, R: spec.b, PL: spec.a, PR: spec.b, PM: 180 - spec.a - spec.b }; }
  function ttCheck(spec) {
    if (!(spec.a > 10 && spec.b > 10 && spec.a + spec.b < 170)) return { ok: false, msg: 'angles must form a triangle' };
    var v = ttVals(spec), lab2 = spec.lab || {};
    for (var k in lab2) { if (v[k] === undefined) return { ok: false, msg: 'bad label position' }; var n = num(String(lab2[k]).replace('°', '')); if (n !== null && Math.abs(n - v[k]) > 0.01) return { ok: false, msg: 'angle label disagrees with the figure' }; }
    return { ok: true };
  }
  function ttRender(spec) {
    var yT = 34, yB = 150, hgt = yB - yT, a = spec.a * Math.PI / 180, b = spec.b * Math.PI / 180, Px = 215, Q = [Px - hgt / Math.tan(a), yB], R = [Px + hgt / Math.tan(b), yB], P = [Px, yT], out = '';
    var lo = Math.min(Q[0], 40) - 10, hi = Math.max(R[0], 390) + 10;
    out += L([lo, yT], [hi, yT]) + L([lo, yB], [hi, yB]) + L(P, [Q[0] - (P[0] - Q[0]) * 0.18, yB + hgt * 0.18]) + L(P, [R[0] + (R[0] - P[0]) * 0.18, yB + hgt * 0.18]);
    out += T(lo + 6, yT - 6, 'm', 'start', true) + T(lo + 6, yB - 6, 'n', 'start', true) + T(P[0], yT - 8, 'P', 'middle', true) + T(Q[0] - 10, yB + 16, 'Q', 'middle', true) + T(R[0] + 10, yB + 16, 'R', 'middle', true);
    out += '<path d="M' + r1(lo + 20) + ' ' + (yT - 3) + ' l8 3 l-8 3" fill="none" stroke="' + INK + '"/><path d="M' + r1(lo + 20) + ' ' + (yB - 3) + ' l8 3 l-8 3" fill="none" stroke="' + INK + '"/>';
    var lab2 = spec.lab || {}, at = { Q: [Q[0] + 30, yB - 10], R: [R[0] - 30, yB - 10], PL: [P[0] - 34, yT + 14], PR: [P[0] + 34, yT + 14], PM: [P[0], yT + 34] };
    Object.keys(lab2).forEach(function (k) { out += T(at[k][0], at[k][1], String(lab2[k]), 'middle'); });
    return H.wrap(out, yB + 40, 'Two parallel lines m and n with two transversals meeting at P', 'Lines m and n are parallel (marked >). Not drawn to scale.');
  }
  F.extend('geo-two-trans', { render: ttRender, check: ttCheck });
  /* geo-protractor: rays OA and OB through the a° and b° marks of a protractor (0° on the right) */
  function prCheck(spec) { return spec.a >= 0 && spec.a <= 180 && spec.b >= 0 && spec.b <= 180 && spec.a !== spec.b && spec.a % 5 === 0 && spec.b % 5 === 0 ? { ok: true } : { ok: false, msg: 'bad protractor readings' }; }
  function prRender(spec) {
    var cx = 215, cy = 150, R = 120, out = '<path d="M' + (cx - R) + ' ' + cy + ' A' + R + ' ' + R + ' 0 0 1 ' + (cx + R) + ' ' + cy + ' Z" fill="none" stroke="' + INK + '" stroke-width="1.6"/>';
    for (var t = 0; t <= 180; t += 5) { var c = Math.cos(t * Math.PI / 180), s = Math.sin(t * Math.PI / 180), len = t % 10 ? 6 : 11; out += L([cx + R * c, cy - R * s], [cx + (R - len) * c, cy - (R - len) * s], 1); if (t % 30 === 0) out += '<text x="' + r1(cx + (R - 22) * c) + '" y="' + r1(cy - (R - 22) * s + 4) + '" font-size="10" text-anchor="middle">' + t + '</text>'; }
    [['A', spec.a], ['B', spec.b]].forEach(function (q) { var c = Math.cos(q[1] * Math.PI / 180), s = Math.sin(q[1] * Math.PI / 180); out += L([cx, cy], [cx + (R + 18) * c, cy - (R + 18) * s], 2.2) + T(cx + (R + 30) * c, cy - (R + 30) * s + 4, q[0], 'middle', true); });
    out += dot([cx, cy], 3) + T(cx, cy + 16, 'O', 'middle', true);
    return H.wrap(out, cy + 28, 'A protractor with rays OA and OB', 'Read each ray where it crosses the scale.');
  }
  F.extend('geo-protractor', { render: prRender, check: prCheck });


})(typeof window !== 'undefined' ? window : globalThis);
