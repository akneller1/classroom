/* Geometry coordinate-plane figures (geo-grid) for Transformations.
   spec: { kind:'geo-grid',
           shapes:[{ id:'pre', pts:[[x,y]...], labels:['A','B','C'], dash:false, of:'pre', tx:{...} }],
           lines:[{ x:2 } | { y:-1 }]   // dashed mirror lines (the axes are always drawn)
           note: 'text' }
   A shape that has "of" and "tx" is the IMAGE of an earlier shape under the transformation tx; the checker
   recomputes every image vertex from the preimage and refuses a figure whose drawn image disagrees.
   tx: {type:'reflect-x'|'reflect-y'|'reflect-line'(line:{x:c}|{y:c})|'translate'(dx,dy)|'rotate-cw'|'rotate-ccw'|'rotate-180'|'dilate'(k)}
   The grid range is chosen from the points; one grid square is drawn as a square. */
(function (G) {
  'use strict';
  var NS = G.MKMENU = (G.MKMENU || {}), F = NS.geoFigures;
  if (!F || !F.extend) return;
  var H = F.h, W = H.W, INK = H.INK, r1 = H.r1, esc = H.esc;

  function apply(tx, p) {
    var x = p[0], y = p[1];
    switch (tx.type) {
      case 'reflect-x': return [x, -y];
      case 'reflect-y': return [-x, y];
      case 'reflect-line': return tx.line.x !== undefined ? [2 * tx.line.x - x, y] : [x, 2 * tx.line.y - y];
      case 'translate': return [x + tx.dx, y + tx.dy];
      case 'rotate-cw': return [y, -x];
      case 'rotate-ccw': return [-y, x];
      case 'rotate-180': return [-x, -y];
      case 'dilate': return [tx.k * x, tx.k * y];
    }
    return null;
  }
  F.grid = { apply: apply };

  function isPt(p) { return Array.isArray(p) && p.length === 2 && isFinite(p[0]) && isFinite(p[1]) && Math.abs(p[0]) <= 15 && Math.abs(p[1]) <= 15; }
  function check(spec) {
    var sh = spec.shapes || [], byId = {}, i, j;
    if (!sh.length) return { ok: false, msg: 'no shapes' };
    for (i = 0; i < sh.length; i++) {
      var s = sh[i];
      if (!s.id || byId[s.id]) return { ok: false, msg: 'shape ids must be unique' };
      if (!Array.isArray(s.pts) || !s.pts.length) return { ok: false, msg: 'shape without points' };
      for (j = 0; j < s.pts.length; j++) if (!isPt(s.pts[j])) return { ok: false, msg: 'point out of range' };
      if (s.labels && s.labels.length !== s.pts.length) return { ok: false, msg: 'one label per vertex' };
      if (s.of) {
        var src = byId[s.of];
        if (!src || !s.tx) return { ok: false, msg: 'image needs its preimage and a transformation' };
        if (src.pts.length !== s.pts.length) return { ok: false, msg: 'image and preimage differ in vertex count' };
        for (j = 0; j < s.pts.length; j++) {
          var e = apply(s.tx, src.pts[j]);
          if (!e || Math.abs(e[0] - s.pts[j][0]) > 1e-9 || Math.abs(e[1] - s.pts[j][1]) > 1e-9) return { ok: false, msg: 'drawn image is not the ' + s.tx.type + ' of the preimage' };
        }
      }
      byId[s.id] = s;
    }
    var ln = spec.lines || [];
    for (i = 0; i < ln.length; i++) if (!((typeof ln[i].x === 'number') !== (typeof ln[i].y === 'number'))) return { ok: false, msg: 'a mirror line is x=c or y=c' };
    return { ok: true };
  }

  function txt(x, y, s, o) {
    o = o || {};
    return '<text x="' + r1(x) + '" y="' + r1(y + (o.size || 14) * 0.35) + '" text-anchor="' + (o.anchor || 'middle') + '" font-family="Arial,sans-serif" font-size="' + (o.size || 14) + '" fill="' + (o.fill || INK) + '"' + (o.halo ? ' stroke="#fff" stroke-width="4" paint-order="stroke"' : '') + '>' + esc(s) + '</text>';
  }

  function render(spec) {
    var sh = spec.shapes, xs = [0], ys = [0], i, j;
    sh.forEach(function (s) { s.pts.forEach(function (p) { xs.push(p[0]); ys.push(p[1]); }); });
    var X = Math.max(3, Math.ceil(Math.max.apply(null, xs.map(Math.abs))) + 1), Y = Math.max(3, Math.ceil(Math.max.apply(null, ys.map(Math.abs))) + 1);
    var xmin = -X, xmax = X, ymin = -Y, ymax = Y;
    var nx = xmax - xmin, ny = ymax - ymin, cell = Math.max(10, Math.min(28, Math.floor(380 / nx), Math.floor(240 / ny)));
    var ox = (W - nx * cell) / 2 - xmin * cell, oy = 14 + ymax * cell, hh = ny * cell + 28;
    function gx(x) { return ox + x * cell; } function gy(y) { return oy - y * cell; }
    var o = '', step = nx > 14 || ny > 12 ? 2 : 1;
    for (i = xmin; i <= xmax; i++) o += '<path d="M' + r1(gx(i)) + ' ' + r1(gy(ymax)) + ' L' + r1(gx(i)) + ' ' + r1(gy(ymin)) + '" stroke="#bbb" stroke-width="1"/>';
    for (j = ymin; j <= ymax; j++) o += '<path d="M' + r1(gx(xmin)) + ' ' + r1(gy(j)) + ' L' + r1(gx(xmax)) + ' ' + r1(gy(j)) + '" stroke="#bbb" stroke-width="1"/>';
    o += '<path d="M' + r1(gx(xmin)) + ' ' + r1(gy(0)) + ' L' + r1(gx(xmax)) + ' ' + r1(gy(0)) + '" stroke="' + INK + '" stroke-width="2"/>';
    o += '<path d="M' + r1(gx(0)) + ' ' + r1(gy(ymax)) + ' L' + r1(gx(0)) + ' ' + r1(gy(ymin)) + '" stroke="' + INK + '" stroke-width="2"/>';
    for (i = xmin; i <= xmax; i++) if (i !== 0 && i % step === 0) o += txt(gx(i), gy(0) + 10, String(i).replace('-', '−'), { size: 10, fill: '#555' });
    for (j = ymin; j <= ymax; j++) if (j !== 0 && j % step === 0) o += txt(gx(0) - 8, gy(j), String(j).replace('-', '−'), { size: 10, fill: '#555', anchor: 'end' });
    o += txt(gx(xmax) + 1, gy(0) - 9, 'x', { size: 12, anchor: 'end', halo: true }) + txt(gx(0) + 9, gy(ymax) + 8, 'y', { size: 12, anchor: 'start', halo: true });
    (spec.lines || []).forEach(function (l) {
      var a = l.x !== undefined ? [gx(l.x), gy(ymax)] : [gx(xmin), gy(l.y)], b = l.x !== undefined ? [gx(l.x), gy(ymin)] : [gx(xmax), gy(l.y)];
      o += '<path d="M' + r1(a[0]) + ' ' + r1(a[1]) + ' L' + r1(b[0]) + ' ' + r1(b[1]) + '" stroke="' + INK + '" stroke-width="2.2" stroke-dasharray="8 5"/>';
      if (l.text) o += l.x !== undefined ? txt(a[0] + 5, a[1] + 8, l.text, { anchor: 'start', size: 12, halo: true }) : txt(b[0] - 3, b[1] - 9, l.text, { anchor: 'end', size: 12, halo: true });
    });
    /* vertex labels: collision-aware (other labels, every vertex dot, axis numbers) and kept inside the picture */
    var dots = [], tickBoxes = [], placed = [], hits = function (A, B) { return A[0] < B[2] && B[0] < A[2] && A[1] < B[3] && B[1] < A[3]; };
    for (i = xmin; i <= xmax; i++) if (i !== 0 && i % step === 0) tickBoxes.push([gx(i) - 9, gy(0) + 3, gx(i) + 9, gy(0) + 17]);
    for (j = ymin; j <= ymax; j++) if (j !== 0 && j % step === 0) tickBoxes.push([gx(0) - 22, gy(j) - 7, gx(0) - 2, gy(j) + 7]);
    tickBoxes.push([gx(xmax) - 12, gy(0) - 18, gx(xmax) + 2, gy(0) - 2], [gx(0) + 2, gy(ymax) - 2, gx(0) + 16, gy(ymax) + 16]);
    (spec.lines || []).forEach(function (l) { if (l.text) tickBoxes.push(l.x !== undefined ? [gx(l.x) + 3, gy(ymax) + 1, gx(l.x) + 3 + l.text.length * 7, gy(ymax) + 15] : [gx(xmax) - 3 - l.text.length * 7, gy(l.y) - 16, gx(xmax) - 3, gy(l.y) - 2]); });
    sh.forEach(function (s) { s.pts.forEach(function (p) { dots.push([gx(p[0]), gy(p[1])]); }); });
    sh.forEach(function (s) {
      var P = s.pts.map(function (p) { return [gx(p[0]), gy(p[1])]; }), cx = 0, cy = 0;
      P.forEach(function (p) { cx += p[0]; cy += p[1]; }); cx /= P.length; cy /= P.length;
      if (P.length >= 2) {
        var d = 'M' + P.map(function (p) { return r1(p[0]) + ' ' + r1(p[1]); }).join(' L') + (P.length > 2 ? ' Z' : '');
        o += '<path d="' + d + '" fill="none" stroke="' + INK + '" stroke-width="2.4" stroke-linejoin="round"' + (s.dash ? ' stroke-dasharray="7 4"' : '') + '/>';
      }
      P.forEach(function (p, k) {
        o += '<circle cx="' + r1(p[0]) + '" cy="' + r1(p[1]) + '" r="3.6" fill="' + INK + '"/>';
        if (s.labels && s.labels[k]) {
          var vx = p[0] - cx, vy = p[1] - cy, m = Math.hypot(vx, vy);
          if (m < 1) { vx = 1; vy = -1; m = Math.SQRT2; }
          var lab = s.labels[k], w = lab.length * 7.5 + 4, base = Math.atan2(vy, vx), best = null, order = [0, 1, -1, 2, -2, 3, -3, 4], q, e, ex;
          for (e = 0; e < 3 && !best; e++) for (q = 0; q < order.length && !best; q++) {
            var th = base + order[q] * Math.PI / 4, ux = Math.cos(th), uy = Math.sin(th), dd = 7 + e * 9 + Math.abs(ux) * w / 2 + Math.abs(uy) * 8,
              lx = p[0] + ux * dd, ly = p[1] + uy * dd, bx = [lx - w / 2, ly - 8, lx + w / 2, ly + 8], bad = false;
            if (bx[0] < 2 || bx[2] > W - 2 || bx[1] < 2 || bx[3] > hh - 2) bad = true;
            placed.forEach(function (z) { if (hits(bx, z)) bad = true; });
            tickBoxes.forEach(function (z) { if (hits(bx, z)) bad = true; });
            dots.forEach(function (z) { if (z[0] > bx[0] - 4 && z[0] < bx[2] + 4 && z[1] > bx[1] - 4 && z[1] < bx[3] + 4) bad = true; });
            if (!bad) best = { x: lx, y: ly, b: bx };
          }
          if (!best) { ex = 7 + Math.abs(Math.cos(base)) * w / 2 + Math.abs(Math.sin(base)) * 8; best = { x: Math.max(w / 2 + 2, Math.min(W - w / 2 - 2, p[0] + Math.cos(base) * ex)), y: p[1] + Math.sin(base) * ex, b: [0, 0, 0, 0] }; best.b = [best.x - w / 2, best.y - 8, best.x + w / 2, best.y + 8]; }
          placed.push(best.b);
          o += txt(best.x, best.y, lab, { halo: true });
        }
      });
    });
    return H.wrap(o, hh, spec.alt || 'A coordinate plane showing ' + sh.length + ' figure' + (sh.length > 1 ? 's' : ''), spec.note || '');
  }

  F.extend('geo-grid', { render: render, check: check });
})(typeof window !== 'undefined' ? window : globalThis);
