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
})(typeof window !== 'undefined' ? window : globalThis);
