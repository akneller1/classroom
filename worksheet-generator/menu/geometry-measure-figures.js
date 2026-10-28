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

  /* geo-net: the cross-shaped net of a rectangular prism, drawn to scale from the true l, w, h.
       spec: { kind:'geo-net', l, w, h, unit:'cm' }   (all three dimensions are printed on the net)
     geo-stack: two rectangular prisms, the second centred on top of the first, in an oblique view.
       spec: { kind:'geo-stack', a:{l,w,h}, b:{l,w,h}, unit:'cm' }   b must be strictly smaller than a in length and width
     Every dimension is printed from the data, so the picture and the labels cannot disagree. */
  function pos(spec, keys) { for (var i = 0; i < keys.length; i++) if (!(spec[keys[i]] > 0) || !isFinite(spec[keys[i]])) return false; return true; }
  function checkNet(spec) { return pos(spec, ['l', 'w', 'h']) && spec.l <= 40 && spec.w <= 40 && spec.h <= 40 ? { ok: true } : { ok: false, msg: 'net dimensions must be positive numbers' }; }
  function dim(spec, v) { return v + (spec.unit ? ' ' + spec.unit : ''); }
  function renderNet(spec) {
    var l = spec.l, w = spec.w, h = spec.h, sc = Math.min((W - 90) / (2 * l + 2 * w), 150 / (2 * w + h)), x0 = (W - (2 * l + 2 * w) * sc) / 2 + 14, y0 = 22, out = '';
    function R(x, y, ww, hh) { return '<rect x="' + r1(x0 + x * sc) + '" y="' + r1(y0 + y * sc) + '" width="' + r1(ww * sc) + '" height="' + r1(hh * sc) + '" fill="#fff" stroke="' + H.INK + '" stroke-width="2"/>'; }
    out += R(0, 0, l, w) + R(0, w, l, h) + R(l, w, w, h) + R(l + w, w, l, h) + R(2 * l + w, w, w, h) + R(0, w + h, l, w);
    out += T(x0 + l * sc / 2, y0 - 8, dim(spec, l)) + T(x0 + l * sc + 8, y0 + w * sc / 2, dim(spec, w), 'start') + T(x0 - 8, y0 + (w + h / 2) * sc, dim(spec, h), 'end');
    return H.wrap(out, Math.ceil(y0 + (2 * w + h) * sc + 18), 'The net of a rectangular prism with its three dimensions labelled', 'Net of a closed rectangular prism.');
  }
  function checkStack(spec) {
    var a = spec.a, b = spec.b; if (!a || !b || !pos(a, ['l', 'w', 'h']) || !pos(b, ['l', 'w', 'h'])) return { ok: false, msg: 'both prisms need l, w and h' };
    if (!(b.l < a.l) || !(b.w < a.w)) return { ok: false, msg: 'the top prism must sit inside the footprint of the bottom prism' };
    return { ok: true };
  }
  function renderStack(spec) {
    var a = spec.a, b = spec.b, kx = 0.4, ky = 0.25, tw = a.l + kx * a.w, th = a.h + b.h + ky * a.w, sc = Math.min(300 / tw, 125 / th), x0 = 62, y0 = 22 + th * sc, out = '';
    function P(x, y, z) { return [x0 + (x + kx * z) * sc, y0 - (y + ky * z) * sc]; }
    function poly(pts) { return '<path d="M' + pts.map(function (q) { return r1(q[0]) + ' ' + r1(q[1]); }).join(' L') + ' Z" fill="#fff" stroke="' + H.INK + '" stroke-width="2" stroke-linejoin="round"/>'; }
    function box(ox, oy, oz, bx) { var x = ox, X = ox + bx.l, y = oy, Y = oy + bx.h, z = oz, Z = oz + bx.w; return poly([P(X, y, z), P(X, y, Z), P(X, Y, Z), P(X, Y, z)]) + poly([P(x, Y, z), P(X, Y, z), P(X, Y, Z), P(x, Y, Z)]) + poly([P(x, y, z), P(X, y, z), P(X, Y, z), P(x, Y, z)]); }
    var bx = (a.l - b.l) / 2, bz = (a.w - b.w) / 2;
    out += box(0, 0, 0, a) + box(bx, a.h, bz, b);
    var q;
    q = P(a.l / 2, 0, 0); out += T(q[0], q[1] + 16, dim(spec, a.l));
    q = P(0, a.h / 2, 0); out += T(q[0] - 8, q[1], dim(spec, a.h), 'end');
    q = P(a.l, 0, a.w / 2); out += T(q[0] + 10, q[1] + 8, dim(spec, a.w), 'start');
    q = P(bx + b.l / 2, a.h + b.h, bz + b.w); out += T(q[0], q[1] - 11, dim(spec, b.l));
    q = P(bx, a.h + b.h / 2, bz); out += T(q[0] - 8, q[1], dim(spec, b.h), 'end');
    q = P(bx + b.l, a.h + b.h / 2, bz + b.w / 2); out += T(q[0] + 10, q[1] + 2, dim(spec, b.w), 'start');
    return H.wrap(out, Math.ceil(y0 + 28), 'Two rectangular prisms stacked, with every dimension labelled', 'Not drawn to scale.');
  }

  /* geo-rotate: a shaded region beside a dashed axis, to be rotated about it.
       spec: { kind:'geo-rotate', shape:'rect'|'tri'|'semi', a, b, unit:'cm' }
       rect: a wide, b tall, one side on the axis      tri: right triangle, legs a (across) and b (along the axis)
       semi: half-disk of radius a, diameter on the axis (b is not used)
     The picture is drawn to scale from the numbers and prints them; it never names the solid. */
  function checkRotate(spec) {
    if (!/^(rect|tri|semi)$/.test(spec.shape) || !pos(spec, ['a']) || spec.a > 30) return { ok: false, msg: 'rotate figure needs shape rect|tri|semi and a positive a' };
    if (spec.shape !== 'semi' && (!pos(spec, ['b']) || spec.b > 40)) return { ok: false, msg: 'rect and tri need a positive b' };
    return { ok: true };
  }
  function renderRotate(spec) {
    var a = spec.a, semi = spec.shape === 'semi', b = semi ? 2 * a : spec.b, sc = Math.min(130 / b, 160 / a), x0 = 96, y0 = 40, w = a * sc, h = b * sc, out = '';
    if (spec.shape === 'rect') out += '<rect x="' + x0 + '" y="' + y0 + '" width="' + r1(w) + '" height="' + r1(h) + '" fill="#bbb" stroke="' + H.INK + '" stroke-width="2"/>';
    else if (spec.shape === 'tri') out += '<path d="M' + x0 + ' ' + y0 + ' L' + x0 + ' ' + r1(y0 + h) + ' L' + r1(x0 + w) + ' ' + r1(y0 + h) + ' Z" fill="#bbb" stroke="' + H.INK + '" stroke-width="2" stroke-linejoin="round"/>';
    else out += '<path d="M' + x0 + ' ' + y0 + ' A' + r1(h / 2) + ' ' + r1(h / 2) + ' 0 0 1 ' + x0 + ' ' + r1(y0 + h) + ' Z" fill="#bbb" stroke="' + H.INK + '" stroke-width="2"/>' +
      '<line x1="' + x0 + '" y1="' + r1(y0 + h / 2) + '" x2="' + r1(x0 + w) + '" y2="' + r1(y0 + h / 2) + '" stroke="' + H.INK + '" stroke-width="1.5"/>';
    out += '<line x1="' + x0 + '" y1="' + r1(y0 - 20) + '" x2="' + x0 + '" y2="' + r1(y0 + h + 20) + '" stroke="#555" stroke-width="2" stroke-dasharray="6 4"/>' + T(x0, y0 - 30, 'axis');
    if (semi) out += T(x0 + w + 8, y0 + h / 2 + 4, 'radius ' + dim(spec, a), 'start');
    else {
      out += T(x0 + w / 2, y0 + h + 36, dim(spec, a));
      out += spec.shape === 'rect' ? T(x0 + w + 8, y0 + h / 2 + 4, dim(spec, b), 'start') : T(x0 - 8, y0 + h / 2 + 4, dim(spec, b), 'end');
    }
    return H.wrap(out, Math.ceil(y0 + h + 52), 'A shaded flat region next to a dashed line, the axis of rotation, with its lengths labelled', 'Drawn to scale. The dashed line is the axis of rotation.');
  }
  F.extend('geo-rotate', { render: renderRotate, check: checkRotate });
  F.extend('geo-net', { render: renderNet, check: checkNet });
  F.extend('geo-stack', { render: renderStack, check: checkStack });
  F.extend('geo-plane', { render: plane, check: function (spec) { return baseCheck(spec, NEED.plane, 'shape'); } });
  F.extend('geo-solid', { render: solid, check: function (spec) { return baseCheck(spec, NEED.solid, 'solid'); } });
})(typeof window !== 'undefined' ? window : globalThis);
