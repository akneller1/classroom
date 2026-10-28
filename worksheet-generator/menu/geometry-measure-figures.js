/* Geometry figures for Unit 10: plane shapes (geo-plane) and solids (geo-solid).
   Specs carry the TRUE numbers (v) the question uses; the picture is scaled from them and the labels are
   printed from them, so a label can never disagree with the answer.

   geo-plane: { kind, shape: 'rectangle'|'triangle'|'parallelogram'|'trapezoid', v:{...}, unit:'cm', show:[keys], lab:{key:'x'} }
       rectangle v:{w,l}   triangle v:{b,h}   parallelogram v:{b,h}   trapezoid v:{a,b,h} (a, b are the bases)
   geo-solid: { kind, solid: 'prism'|'cylinder'|'pyramid'|'cone'|'sphere', v:{...}, unit:'cm', show:[keys], lab:{key:'x'} }
       prism v:{l,w,h}   pyramid v:{l,w,h}   cylinder v:{r,h}   cone v:{r,h}   sphere v:{r}
   "show" lists the dimensions to print (default: all). "lab" replaces a dimension's printed text with an
   unknown such as 'x' (non-numeric only). Solids are always marked "Not drawn to scale." */
(function (G) {
  'use strict';
  var NS = G.MKMENU = (G.MKMENU || {}), F = NS.geoFigures;
  if (!F || !F.extend) return;
  var H = F.h, W = H.W, L = H.L, dot = H.dot, r1 = H.r1;

  /* labels get a white halo so a line passing behind them never cuts the digits */
  function T(x, y, s, anchor) { return H.T(x, y, s, anchor).replace('<text ', '<text stroke="#fff" stroke-width="4" paint-order="stroke" '); }
  var NEED = {
    plane: { rectangle: ['w', 'l'], triangle: ['b', 'h'], parallelogram: ['b', 'h'], trapezoid: ['a', 'b', 'h'] },
    solid: { prism: ['l', 'w', 'h'], pyramid: ['l', 'w', 'h'], cylinder: ['r', 'h'], cone: ['r', 'h'], sphere: ['r'] }
  };

  function baseCheck(spec, table, key) {
    var need = table[spec[key]];
    if (!need) return { ok: false, msg: 'unknown ' + key + ' ' + spec[key] };
    for (var i = 0; i < need.length; i++) {
      var n = spec.v && spec.v[need[i]];
      if (typeof n !== 'number' || !(n > 0) || !isFinite(n)) return { ok: false, msg: 'dimension ' + need[i] + ' must be a positive number' };
    }
    if (spec.shape === 'trapezoid' && spec.v.a === spec.v.b && false) return { ok: false, msg: '' };
    var show = spec.show || need;
    for (var j = 0; j < show.length; j++) if (need.indexOf(show[j]) < 0) return { ok: false, msg: 'cannot show ' + show[j] };
    var lab = spec.lab || {};
    for (var k in lab) if (/\d/.test(lab[k])) return { ok: false, msg: 'a replacement label must not contain a number (it could contradict the data)' };
    if (spec.unit && !/^[a-z ]{1,12}$/i.test(spec.unit)) return { ok: false, msg: 'bad unit' };
    return { ok: true };
  }
  function label(spec, key) {
    if (spec.lab && spec.lab[key] !== undefined) return spec.lab[key];
    return spec.v[key] + (spec.unit ? ' ' + spec.unit : '');
  }
  function shown(spec, key) { var need = NEED[spec.kind === 'geo-plane' ? 'plane' : 'solid'][spec.shape || spec.solid]; return (spec.show || need).indexOf(key) >= 0; }
  function mid(p, q) { return [(p[0] + q[0]) / 2, (p[1] + q[1]) / 2]; }
  function poly(pts, dash) { var o = ''; for (var i = 0; i < pts.length; i++) o += L(pts[i], pts[(i + 1) % pts.length], 2.4, dash); return o; }
  function ell(cx, cy, rx, ry, half, dash) {   // half: 'front' (lower), 'back' (upper) or null (full)
    var d = half === 'front' ? 'M' + r1(cx - rx) + ' ' + r1(cy) + ' A' + r1(rx) + ' ' + r1(ry) + ' 0 0 0 ' + r1(cx + rx) + ' ' + r1(cy)
      : half === 'back' ? 'M' + r1(cx - rx) + ' ' + r1(cy) + ' A' + r1(rx) + ' ' + r1(ry) + ' 0 0 1 ' + r1(cx + rx) + ' ' + r1(cy) : '';
    if (!half) return '<ellipse cx="' + r1(cx) + '" cy="' + r1(cy) + '" rx="' + r1(rx) + '" ry="' + r1(ry) + '" fill="none" stroke="' + H.INK + '" stroke-width="2.4"/>';
    return '<path d="' + d + '" fill="none" stroke="' + H.INK + '" stroke-width="' + (dash ? 1.8 : 2.4) + '"' + (dash ? ' stroke-dasharray="6 4"' : '') + '/>';
  }
  function clampPx(n, lo) { return n < lo ? lo : n; }

  /* ---------- plane shapes ---------- */
  function plane(spec) {
    var v = spec.v, shp = spec.shape, BW = 250, BH = 112, note = '', pts, ext, hline = null, extra = '', lbl = '';
    var wU, hU;                                    // drawn extent in data units
    if (shp === 'rectangle') { wU = v.l; hU = v.w; }
    else if (shp === 'triangle') { wU = v.b; hU = v.h; }
    else if (shp === 'parallelogram') { wU = v.b * 1.3; hU = v.h; }
    else { wU = Math.max(v.a, v.b); hU = v.h; }
    var k = Math.min(BW / wU, BH / hU), clamped = false;
    function px(n) { var d = n * k; if (d < 34) { clamped = true; return 34; } return d; }
    var x0 = (W - Math.min(BW, wU * k)) / 2 + 0, y0 = 150;   // bottom-left of the shape
    if (shp === 'rectangle') {
      var rw = px(v.l), rh = px(v.w); x0 = (W - rw) / 2; pts = [[x0, y0], [x0 + rw, y0], [x0 + rw, y0 - rh], [x0, y0 - rh]];
      extra += H.rightMark([x0, y0], 90, 0, 10) + H.rightMark([x0 + rw, y0], 90, 180, 10) + H.rightMark([x0 + rw, y0 - rh], 270, 180, 10) + H.rightMark([x0, y0 - rh], 270, 0, 10);
      if (shown(spec, 'l')) lbl += T(x0 + rw / 2, y0 + 15, label(spec, 'l'));
      if (shown(spec, 'w')) lbl += T(x0 + rw + 8, y0 - rh / 2, label(spec, 'w'), 'start');
    } else if (shp === 'triangle') {
      var tb = px(v.b), th = px(v.h), ta = tb * 0.32; x0 = (W - tb) / 2; pts = [[x0, y0], [x0 + tb, y0], [x0 + ta, y0 - th]];
      extra += L([x0 + ta, y0 - th], [x0 + ta, y0], 1.8, true) + H.rightMark([x0 + ta, y0], 90, 0, 10);
      if (shown(spec, 'b')) lbl += T(x0 + tb / 2, y0 + 15, label(spec, 'b'));
      if (shown(spec, 'h')) lbl += T(x0 + ta + 6, y0 - th * 0.22, label(spec, 'h'), 'start');
    } else if (shp === 'parallelogram') {
      var pb = px(v.b), ph = px(v.h), ps = pb * 0.3; x0 = (W - pb - ps) / 2; pts = [[x0, y0], [x0 + pb, y0], [x0 + pb + ps, y0 - ph], [x0 + ps, y0 - ph]];
      extra += L([x0 + ps, y0 - ph], [x0 + ps, y0], 1.8, true) + H.rightMark([x0 + ps, y0], 90, 0, 10);
      if (shown(spec, 'b')) lbl += T(x0 + pb / 2, y0 + 15, label(spec, 'b'));
      if (shown(spec, 'h')) lbl += T(x0 + ps + 6, y0 - ph / 2, label(spec, 'h'), 'start');
    } else {
      var big = Math.max(v.a, v.b), small = Math.min(v.a, v.b), tbw = px(big), tsw = Math.min(px(small), tbw - 12), tth = px(v.h), off = (tbw - tsw) / 2; x0 = (W - tbw) / 2;
      pts = [[x0, y0], [x0 + tbw, y0], [x0 + off + tsw, y0 - tth], [x0 + off, y0 - tth]];
      extra += L([x0 + off, y0 - tth], [x0 + off, y0], 1.8, true) + H.rightMark([x0 + off, y0], 90, 0, 10);
      var bigKey = v.b >= v.a ? 'b' : 'a', smallKey = bigKey === 'b' ? 'a' : 'b';
      if (shown(spec, bigKey)) lbl += T(x0 + tbw / 2, y0 + 15, label(spec, bigKey));
      if (shown(spec, smallKey)) lbl += T(x0 + off + tsw / 2, y0 - tth - 11, label(spec, smallKey));
      if (shown(spec, 'h')) lbl += T(x0 + off + 6, y0 - tth / 2, label(spec, 'h'), 'start');
    }
    var out = poly(pts) + extra + lbl;
    return H.wrap(out, 182, 'A ' + shp + ' with its dimensions labelled', clamped || (wU / hU > 4.5 || hU / wU > 4.5) ? 'Not drawn to scale.' : '');
  }

  /* ---------- solids ---------- */
  function solid(spec) {
    var v = spec.v, s = spec.solid, out = '', cx = W / 2;
    function sc(maxW, maxH, wU, hU) { return Math.min(maxW / wU, maxH / hU); }
    if (s === 'prism' || s === 'pyramid') {
      var depthU = v.w * 0.55, k = sc(220, 104, v.l + depthU * 0.9, v.h + depthU * 0.5 + (s === 'pyramid' ? 0 : 0));
      var FW = clampPx(v.l * k, s === 'pyramid' ? 90 : 50), FH = clampPx(v.h * k, 36), dx = clampPx(v.w * k * 0.55, s === 'pyramid' ? 44 : 26) * 0.9, dy = clampPx(v.w * k * 0.55, s === 'pyramid' ? 44 : 26) * 0.5;
      if (s === 'pyramid') FH = clampPx(v.h * k, 44);
      var x0 = (W - FW - dx) / 2, y0 = 40 + FH + dy + (s === 'pyramid' ? 0 : 0);
      var F0 = [x0, y0 + 0], F1 = [x0 + FW, y0], B0 = [x0 + dx, y0 - dy], B1 = [x0 + FW + dx, y0 - dy];
      if (s === 'prism') {
        var F3 = [x0, y0 - FH], F2 = [x0 + FW, y0 - FH], B3 = [x0 + dx, y0 - dy - FH], B2 = [x0 + FW + dx, y0 - dy - FH];
        out += poly([F0, F1, F2, F3]) + L(F3, B3) + L(F2, B2) + L(B3, B2) + L(F1, B1) + L(B2, B1) + L(B0, F0, 1.8, true) + L(B0, B1, 1.8, true) + L(B0, B3, 1.8, true);
        if (shown(spec, 'l')) out += T(x0 + FW / 2, y0 + 15, label(spec, 'l'));
        if (shown(spec, 'w')) out += T(x0 + FW + dx / 2 + 8, y0 - dy / 2 + 12, label(spec, 'w'), 'start');
        if (shown(spec, 'h')) out += T(x0 - 7, y0 - FH / 2, label(spec, 'h'), 'end');
      } else {
        var C = [(F0[0] + B1[0]) / 2, (F0[1] + B1[1]) / 2], A = [C[0], C[1] - FH];
        out += L(F0, F1) + L(F1, B1) + L(A, F0) + L(A, F1) + L(A, B1) + L(B0, F0, 1.8, true) + L(B0, B1, 1.8, true) + L(A, B0, 1.8, true) + L(A, C, 1.8, true) + dot(C, 2.5) + H.rightMark(C, 90, 0, 8);
        if (shown(spec, 'l')) out += T(x0 + FW / 2, y0 + 15, label(spec, 'l'));
        if (shown(spec, 'w')) out += T(x0 + FW + dx / 2 + 8, y0 - dy / 2 + 12, label(spec, 'w'), 'start');
        if (shown(spec, 'h')) out += T(C[0] + 7, C[1] - FH * 0.45, label(spec, 'h'), 'start');
      }
      return H.wrap(out, Math.ceil(y0 + 28), 'A rectangular ' + s + ' with its dimensions labelled', 'Not drawn to scale.');
    }
    if (s === 'cylinder' || s === 'cone') {
      var kk = sc(210, 100, 2 * v.r, v.h + 0.64 * v.r), R = clampPx(v.r * kk, 28), Hh = clampPx(v.h * kk, 40), ry = Math.max(9, R * 0.3);
      var yt = 36 + ry, yb = yt + Hh;
      if (s === 'cylinder') {
        out += ell(cx, yt, R, ry) + L([cx - R, yt], [cx - R, yb]) + L([cx + R, yt], [cx + R, yb]) + ell(cx, yb, R, ry, 'front') + ell(cx, yb, R, ry, 'back', true);
        out += L([cx, yt], [cx + R, yt], 1.8) + dot([cx, yt], 2.5);
        if (shown(spec, 'r')) out += T(cx + R / 2, yt - ry - 9, label(spec, 'r'));
        if (shown(spec, 'h')) out += T(cx + R + 8, (yt + yb) / 2, label(spec, 'h'), 'start');
      } else {
        out += L([cx, yt - ry * 0.0], [cx - R, yb]) + L([cx, yt], [cx + R, yb]) + ell(cx, yb, R, ry, 'front') + ell(cx, yb, R, ry, 'back', true);
        out += L([cx, yt], [cx, yb], 1.8, true) + L([cx, yb], [cx + R, yb], 1.8) + dot([cx, yb], 2.5) + H.rightMark([cx, yb], 90, 0, 8);
        if (shown(spec, 'r')) out += T(cx + R / 2, yb + ry + 11, label(spec, 'r'));
        if (shown(spec, 'h')) out += T(cx + R / 2 + 8, (yt + yb) / 2, label(spec, 'h'), 'start');
      }
      return H.wrap(out, Math.ceil(yb + ry + 30), 'A right circular ' + s + ' with its dimensions labelled', 'Not drawn to scale.');
    }
    var R2 = 54, cy = 30 + R2;
    out += '<circle cx="' + cx + '" cy="' + cy + '" r="' + R2 + '" fill="none" stroke="' + H.INK + '" stroke-width="2.4"/>' + ell(cx, cy, R2, R2 * 0.3, 'front') + ell(cx, cy, R2, R2 * 0.3, 'back', true) + L([cx, cy], [cx + R2, cy], 1.8) + dot([cx, cy], 2.5);
    if (shown(spec, 'r')) out += T(cx + R2 * 0.36, cy - R2 * 0.3 - 12, label(spec, 'r'));
    return H.wrap(out, cy + R2 + 20, 'A sphere with its radius labelled', 'Not drawn to scale.');
  }

  F.extend('geo-plane', { render: plane, check: function (spec) { return baseCheck(spec, NEED.plane, 'shape'); } });
  F.extend('geo-solid', { render: solid, check: function (spec) { return baseCheck(spec, NEED.solid, 'solid'); } });
})(typeof window !== 'undefined' ? window : globalThis);
