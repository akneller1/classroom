/* Menu Assessment Generator — figures drawn from plain data specs (no DOM needed).

   numberLine(spec) -> SVG string
     spec = { kind:'numberline', min, max, step?, pieces:[{lo:[n,d]|null, loC, hi:[n,d]|null, hiC}] }
     A piece with lo = hi is a single point. pieces:[] gives a blank number line for students.
   readNumberLine(svg) -> {min, max, set}   reads the DRAWN geometry back (circles, segments, arrows),
     so tests and the verifier check the picture itself, not the spec it came from. */
(function (G) {
  'use strict';
  var NS = (G.MKMENU = G.MKMENU || {});
  var W = 460, X0 = 34, X1 = 426, Y = 30;

  function val(q) { return q === null || q === undefined ? null : Array.isArray(q) ? q[0] / q[1] : +q; }
  function label(q) {
    if (Array.isArray(q) && q[1] !== 1) return (q[0] < 0 ? '−' : '') + Math.abs(q[0]) + '/' + q[1];
    var v = val(q); return (v < 0 ? '−' : '') + Math.abs(v);
  }
  function numberLine(spec) {
    var min = spec.min, max = spec.max, unit = (X1 - X0) / (max - min);
    var step = spec.step || (max - min <= 20 ? 1 : max - min <= 40 ? 2 : 5);
    var px = function (v) { return +(X0 + (v - min) * unit).toFixed(3); };
    var h = ['<svg class="mm-nl" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 ' + W + ' 62" width="3.5in" role="img" aria-label="' + (spec.pieces && spec.pieces.length ? 'number line graph' : 'blank number line') + '" data-min="' + min + '" data-max="' + max + '" data-x0="' + X0 + '" data-unit="' + unit.toFixed(6) + '">'];
    h.push('<path d="M10 ' + Y + 'H' + (W - 10) + '" stroke="#111" stroke-width="1.6"/>');
    h.push('<path d="M10 ' + Y + 'l8 -4.5v9z M' + (W - 10) + ' ' + Y + 'l-8 -4.5v9z" fill="#111"/>');
    for (var t = Math.ceil(min / step) * step; t <= max + 1e-9; t += step) {
      var x = px(t);
      h.push('<path d="M' + x + ' ' + (Y - 6) + 'v12" stroke="#111" stroke-width="1.1"/><text x="' + x + '" y="' + (Y + 21) + '" text-anchor="middle" font-size="11" font-family="Arial,sans-serif" fill="#111">' + (t < 0 ? '−' : '') + Math.abs(t) + '</text>');
    }
    (spec.pieces || []).forEach(function (p) {
      var lo = val(p.lo), hi = val(p.hi);
      var xa = lo === null ? 14 : px(lo), xb = hi === null ? W - 14 : px(hi);
      if (lo === null || hi === null || lo !== hi) {
        h.push('<path class="nl-seg" d="M' + xa + ' ' + Y + 'H' + xb + '" stroke="#1d4ed8" stroke-width="4.5"/>');
        if (lo === null) h.push('<path class="nl-arrow" data-dir="left" d="M8 ' + Y + 'l11 -7v14z" fill="#1d4ed8"/>');
        if (hi === null) h.push('<path class="nl-arrow" data-dir="right" d="M' + (W - 8) + ' ' + Y + 'l-11 -7v14z" fill="#1d4ed8"/>');
      }
      [[lo, p.loC, p.lo], [hi, p.hiC, p.hi]].forEach(function (e, k) {
        if (e[0] === null || (k === 1 && lo === hi)) return;
        h.push('<circle class="nl-end" cx="' + px(e[0]) + '" cy="' + Y + '" r="5.5" stroke="#1d4ed8" stroke-width="2.2" fill="' + (e[1] ? '#1d4ed8' : '#fff') + '"/>');
        if (Array.isArray(e[2]) && e[2][1] !== 1) h.push('<text x="' + px(e[0]) + '" y="' + (Y - 11) + '" text-anchor="middle" font-size="10" font-family="Arial,sans-serif" fill="#1d4ed8">' + label(e[2]) + '</text>');
      });
    });
    h.push('</svg>');
    return h.join('');
  }

  /* ---------- reading a drawn number line back ---------- */
  function attr(tag, name) { var m = new RegExp('\\s' + name + '="([^"]*)"').exec(tag); return m ? m[1] : null; }
  function toRational(v, tol) {   // nearest fraction with a small denominator (figures only use these)
    tol = tol || 1e-4;
    for (var d = 1; d <= 12; d++) { var n = Math.round(v * d); if (Math.abs(n / d - v) < tol) return [n, d]; }
    return null;
  }
  function readNumberLine(svg) {
    var root = /<svg[^>]*>/.exec(svg)[0];
    var min = +attr(root, 'data-min'), max = +attr(root, 'data-max'), x0 = +attr(root, 'data-x0'), unit = +attr(root, 'data-unit');
    var toVal = function (x) { return toRational((x - x0) / unit + min); };
    var circles = (svg.match(/<circle[^>]*class="nl-end"[^>]*>/g) || []).map(function (c) { return { x: +attr(c, 'cx'), closed: attr(c, 'fill') !== '#fff' }; });
    var segs = (svg.match(/<path[^>]*class="nl-seg"[^>]*>/g) || []).map(function (s) { var m = /M([\d.]+) [\d.]+H([\d.]+)/.exec(attr(s, 'd')); return { a: +m[1], b: +m[2] }; });
    var arrows = (svg.match(/<path[^>]*class="nl-arrow"[^>]*>/g) || []).map(function (a) { return attr(a, 'data-dir'); });
    var near = function (x) { return circles.filter(function (c) { return Math.abs(c.x - x) < 0.6; })[0]; };
    var pieces = [], used = {};
    segs.forEach(function (s) {
      var left = s.a < X0 - 1, right = s.b > X1 + 1;
      if (left && arrows.indexOf('left') < 0) throw new Error('segment reaches the left edge without an arrow');
      if (right && arrows.indexOf('right') < 0) throw new Error('segment reaches the right edge without an arrow');
      var ca = left ? null : near(s.a), cb = right ? null : near(s.b);
      if (!left && !ca) throw new Error('segment end without an endpoint circle');
      if (!right && !cb) throw new Error('segment end without an endpoint circle');
      if (ca) used[ca.x] = 1; if (cb) used[cb.x] = 1;
      pieces.push({ lo: left ? null : toVal(s.a), loC: ca ? ca.closed : false, hi: right ? null : toVal(s.b), hiC: cb ? cb.closed : false });
    });
    circles.forEach(function (c) { if (!used[c.x]) { if (!c.closed) throw new Error('an open circle by itself shows nothing'); pieces.push({ lo: toVal(c.x), loC: true, hi: toVal(c.x), hiC: true }); } });
    pieces.sort(function (p, q) { return (p.lo ? p.lo[0] / p.lo[1] : -Infinity) - (q.lo ? q.lo[0] / q.lo[1] : -Infinity); });
    return { min: min, max: max, pieces: pieces };
  }

  /* Choose a window that shows every endpoint with room around it. */
  function windowFor(points, pad) {
    pad = pad === undefined ? 3 : pad;
    var vs = points.map(val).filter(function (v) { return v !== null; });
    if (!vs.length) vs = [0];
    var lo = Math.floor(Math.min.apply(null, vs)) - pad, hi = Math.ceil(Math.max.apply(null, vs)) + pad;
    if (hi - lo < 10) { var add = 10 - (hi - lo); lo -= Math.floor(add / 2); hi += Math.ceil(add / 2); }
    if (hi - lo > 20 && hi - lo <= 40) { if (lo % 2) lo--; if (hi % 2) hi++; }
    return { min: lo, max: hi };
  }


  /* ---------- coordinate plane ----------
     spec = { kind:'plane', xmin, xmax, ymin, ymax,
              points:[{x, y, open}], segs:[{a:[x,y], b:[x,y], aEnd, bEnd}], curves:[[[x,y], …]] }
     ends: 'closed' | 'open' | 'arrow' | 'none'.  Coordinates are plain numbers. */
  var PW = 300, PAD = 22;
  function numTxt(v) { return (v < 0 ? '−' : '') + Math.abs(v); }
  function plane(spec) {
    var xmin = spec.xmin, xmax = spec.xmax, ymin = spec.ymin, ymax = spec.ymax;
    var unit = (PW - 2 * PAD) / Math.max(xmax - xmin, ymax - ymin);
    var W = Math.round((xmax - xmin) * unit + 2 * PAD), H = Math.round((ymax - ymin) * unit + 2 * PAD);
    var X = function (x) { return +(PAD + (x - xmin) * unit).toFixed(2); }, Y = function (y) { return +(PAD + (ymax - y) * unit).toFixed(2); };
    var step = Math.max(1, Math.ceil((xmax - xmin) / 12));
    var h = ['<svg class="mm-plane-fig" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 ' + W + ' ' + H + '" width="' + (W / 96 * 0.78).toFixed(2) + 'in" role="img" aria-label="coordinate graph" data-xmin="' + xmin + '" data-ymax="' + ymax + '" data-pad="' + PAD + '" data-unit="' + unit.toFixed(6) + '">'];
    for (var gx = xmin; gx <= xmax; gx++) h.push('<path d="M' + X(gx) + ' ' + Y(ymin) + 'V' + Y(ymax) + '" stroke="#d6d6d6" stroke-width="0.8"/>');
    for (var gy = ymin; gy <= ymax; gy++) h.push('<path d="M' + X(xmin) + ' ' + Y(gy) + 'H' + X(xmax) + '" stroke="#d6d6d6" stroke-width="0.8"/>');
    if (ymin <= 0 && ymax >= 0) h.push('<path d="M' + (X(xmin) - 6) + ' ' + Y(0) + 'H' + (X(xmax) + 6) + '" stroke="#111" stroke-width="1.4"/><text x="' + (X(xmax) + 4) + '" y="' + (Y(0) - 5) + '" font-size="11" font-style="italic" font-family="Georgia,serif">x</text>');
    if (xmin <= 0 && xmax >= 0) h.push('<path d="M' + X(0) + ' ' + (Y(ymin) + 6) + 'V' + (Y(ymax) - 6) + '" stroke="#111" stroke-width="1.4"/><text x="' + (X(0) + 5) + '" y="' + (Y(ymax) - 4) + '" font-size="11" font-style="italic" font-family="Georgia,serif">y</text>');
    for (var tx = Math.ceil(xmin / step) * step; tx <= xmax; tx += step) if (tx !== 0) h.push('<text x="' + X(tx) + '" y="' + (Math.min(Math.max(Y(0), Y(ymax)), Y(ymin)) + 12) + '" text-anchor="middle" font-size="8.5" font-family="Arial,sans-serif" fill="#333">' + numTxt(tx) + '</text>');
    for (var ty = Math.ceil(ymin / step) * step; ty <= ymax; ty += step) if (ty !== 0) h.push('<text x="' + (Math.max(Math.min(X(0), X(xmax)), X(xmin)) - 4) + '" y="' + (Y(ty) + 3) + '" text-anchor="end" font-size="8.5" font-family="Arial,sans-serif" fill="#333">' + numTxt(ty) + '</text>');
    /* half-planes: { a:[x,y], b:[x,y], dashed, side:[x,y] } — the boundary line through a and b across the window,
       shading on the side that contains "side" */
    (spec.halfplanes || []).forEach(function (hp, k) {
      var col = ['#1d4ed8', '#c2410c'][k % 2], ax = hp.a[0], ay = hp.a[1], bx = hp.b[0], by = hp.b[1];
      var f = function (x, y) { return (bx - ax) * (y - ay) - (by - ay) * (x - ax); }, sg = f(hp.side[0], hp.side[1]) > 0 ? 1 : -1;
      var poly = [[xmin, ymin], [xmax, ymin], [xmax, ymax], [xmin, ymax]], out = [];
      poly.forEach(function (P, i) { var Q2 = poly[(i + 1) % poly.length], fp = sg * f(P[0], P[1]), fq = sg * f(Q2[0], Q2[1]);
        if (fp >= 0) out.push(P); if ((fp > 0 && fq < 0) || (fp < 0 && fq > 0)) { var t = fp / (fp - fq); out.push([P[0] + t * (Q2[0] - P[0]), P[1] + t * (Q2[1] - P[1])]); } });
      var ends = []; poly.forEach(function (P, i) { var Q2 = poly[(i + 1) % poly.length], fp = f(P[0], P[1]), fq = f(Q2[0], Q2[1]);
        if (fp === 0) ends.push(P); else if ((fp > 0 && fq < 0) || (fp < 0 && fq > 0)) { var t = fp / (fp - fq); ends.push([P[0] + t * (Q2[0] - P[0]), P[1] + t * (Q2[1] - P[1])]); } });
      h.push('<g class="pl-hp"><polygon class="pl-shade" points="' + out.map(function (P) { return X(P[0]) + ',' + Y(P[1]); }).join(' ') + '" fill="' + col + '" fill-opacity="0.14" stroke="none"/>' +
        (ends.length >= 2 ? '<path class="pl-bline" d="M' + X(ends[0][0]) + ' ' + Y(ends[0][1]) + 'L' + X(ends[1][0]) + ' ' + Y(ends[1][1]) + '" stroke="' + col + '" stroke-width="2.4"' + (hp.dashed ? ' stroke-dasharray="7 5"' : '') + '/>' : '') + '</g>');
    });
    (spec.curves || []).forEach(function (c) { h.push('<polyline class="pl-curve" fill="none" stroke="#1d4ed8" stroke-width="2.4" points="' + c.map(function (p) { return X(p[0]) + ',' + Y(p[1]); }).join(' ') + '"/>'); });
    (spec.segs || []).forEach(function (sg) {
      h.push('<path class="pl-seg" d="M' + X(sg.a[0]) + ' ' + Y(sg.a[1]) + 'L' + X(sg.b[0]) + ' ' + Y(sg.b[1]) + '" stroke="#1d4ed8" stroke-width="2.6"/>');
      [['a', sg.a, sg.aEnd, sg.b], ['b', sg.b, sg.bEnd, sg.a]].forEach(function (e) {
        if (e[2] === 'closed' || e[2] === 'open') h.push('<circle class="pl-end" data-at="' + e[0] + '" cx="' + X(e[1][0]) + '" cy="' + Y(e[1][1]) + '" r="4" stroke="#1d4ed8" stroke-width="2" fill="' + (e[2] === 'closed' ? '#1d4ed8' : '#fff') + '"/>');
        if (e[2] === 'arrow') {
          var dx = X(e[1][0]) - X(e[3][0]), dy = Y(e[1][1]) - Y(e[3][1]), L = Math.sqrt(dx * dx + dy * dy), ux = dx / L, uy = dy / L, tx2 = X(e[1][0]), ty2 = Y(e[1][1]);
          h.push('<path class="pl-arrow" data-at="' + e[0] + '" d="M' + (tx2 + ux * 7).toFixed(2) + ' ' + (ty2 + uy * 7).toFixed(2) + 'L' + (tx2 - uy * 5).toFixed(2) + ' ' + (ty2 + ux * 5).toFixed(2) + 'L' + (tx2 + uy * 5).toFixed(2) + ' ' + (ty2 - ux * 5).toFixed(2) + 'Z" fill="#1d4ed8"/>');
        }
      });
    });
    (spec.points || []).forEach(function (pt) { h.push('<circle class="pl-pt" cx="' + X(pt.x) + '" cy="' + Y(pt.y) + '" r="4.2" stroke="#1d4ed8" stroke-width="2" fill="' + (pt.open ? '#fff' : '#1d4ed8') + '"/>'); });
    h.push('</svg>');
    return h.join('');
  }
  function readPlane(svg, raw) {   // raw: plain decimal coordinates (for curves through irrational points)
    var root = /<svg[^>]*>/.exec(svg)[0];
    var xmin = +attr(root, 'data-xmin'), ymax = +attr(root, 'data-ymax'), pad = +attr(root, 'data-pad'), unit = +attr(root, 'data-unit');
    var tol = 0.012 / unit * 2, conv = raw ? function (v) { return v; } : function (v) { return toRational(v, tol); };
    var vx = function (px) { return conv((px - pad) / unit + xmin); }, vy = function (py) { return conv(ymax - (py - pad) / unit); };
    var pts = (svg.match(/<circle[^>]*class="pl-pt"[^>]*>/g) || []).map(function (c) { return { x: vx(+attr(c, 'cx')), y: vy(+attr(c, 'cy')), open: attr(c, 'fill') === '#fff' }; });
    var ends = (svg.match(/<circle[^>]*class="pl-end"[^>]*>/g) || []).map(function (c) { return { px: +attr(c, 'cx'), py: +attr(c, 'cy'), open: attr(c, 'fill') === '#fff' }; });
    var arrows = (svg.match(/<path[^>]*class="pl-arrow"[^>]*>/g) || []).map(function (a) { var m = /M([-\d.]+) ([-\d.]+)/.exec(attr(a, 'd')); return { px: +m[1], py: +m[2] }; });
    var segs = (svg.match(/<path[^>]*class="pl-seg"[^>]*>/g) || []).map(function (sg) {
      var m = /M([-\d.]+) ([-\d.]+)L([-\d.]+) ([-\d.]+)/.exec(attr(sg, 'd')), a = [+m[1], +m[2]], b = [+m[3], +m[4]];
      function endAt(p, q) {
        var e = ends.filter(function (c) { return Math.abs(c.px - p[0]) < 0.6 && Math.abs(c.py - p[1]) < 0.6; })[0];
        if (e) return e.open ? 'open' : 'closed';
        var L = Math.sqrt(Math.pow(p[0] - q[0], 2) + Math.pow(p[1] - q[1], 2));
        var ar = arrows.filter(function (t) { return Math.abs(Math.sqrt(Math.pow(t.px - p[0], 2) + Math.pow(t.py - p[1], 2)) - 7) < 0.8 && Math.sqrt(Math.pow(t.px - q[0], 2) + Math.pow(t.py - q[1], 2)) > L; })[0];
        return ar ? 'arrow' : 'none';
      }
      return { a: [vx(a[0]), vy(a[1])], b: [vx(b[0]), vy(b[1])], aEnd: endAt(a, b), bEnd: endAt(b, a) };
    });
    var curves = (svg.match(/<polyline[^>]*class="pl-curve"[^>]*>/g) || []).map(function (c) { return attr(c, 'points').split(' ').map(function (p) { var xy = p.split(','); return [vx(+xy[0]), vy(+xy[1])]; }); });
    var hps = (svg.match(/<g class="pl-hp">.*?<\/g>/g) || []).map(function (g) {
      var poly = attr(/<polygon[^>]*>/.exec(g)[0], 'points').split(' ').map(function (p) { var xy = p.split(','); return [+xy[0], +xy[1]]; });
      var cx = poly.reduce(function (s0, p) { return s0 + p[0]; }, 0) / poly.length, cy = poly.reduce(function (s0, p) { return s0 + p[1]; }, 0) / poly.length;
      var bl = /<path[^>]*class="pl-bline"[^>]*>/.exec(g); if (!bl) return null;
      var m = /M([-\d.]+) ([-\d.]+)L([-\d.]+) ([-\d.]+)/.exec(attr(bl[0], 'd'));
      return { a: [vx(+m[1]), vy(+m[2])], b: [vx(+m[3]), vy(+m[4])], dashed: /stroke-dasharray/.test(bl[0]), inside: [(cx - pad) / unit + xmin, ymax - (cy - pad) / unit] };
    }).filter(Boolean);
    return { xmin: xmin, ymax: ymax, points: pts, segs: segs, curves: curves, halfplanes: hps };
  }

  /* ---------- function tables ---------- */
  function table(spec) {
    var vertical = spec.vertical;
    var cell = function (v) { return typeof v === 'number' ? numTxt(v) : String(v).replace(/[<>&]/g, ''); };
    if (vertical) return '<table class="mm-ftable v"><thead><tr><th>' + spec.head[0] + '</th><th>' + spec.head[1] + '</th></tr></thead><tbody>' + spec.rows.map(function (r) { return '<tr><td>' + cell(r[0]) + '</td><td>' + cell(r[1]) + '</td></tr>'; }).join('') + '</tbody></table>';
    return '<table class="mm-ftable"><tbody><tr><th>' + spec.head[0] + '</th>' + spec.rows.map(function (r) { return '<td>' + cell(r[0]) + '</td>'; }).join('') + '</tr><tr><th>' + spec.head[1] + '</th>' + spec.rows.map(function (r) { return '<td>' + cell(r[1]) + '</td>'; }).join('') + '</tr></tbody></table>';
  }
  function readTable(html) {
    var nums = function (s) { return s.replace(/−/g, '-').trim(); };
    var rows = (html.match(/<tr>[\s\S]*?<\/tr>/g) || []).map(function (tr) { return (tr.match(/<td>([^<]*)<\/td>/g) || []).map(function (td) { return nums(td.replace(/<\/?td>/g, '')); }); }).filter(function (r) { return r.length; });
    if (/class="mm-ftable v"/.test(html)) return rows.map(function (r) { return [r[0], r[1]]; });
    return rows[0].map(function (x, i) { return [x, rows[1][i]]; });
  }

  /* ---------- mapping diagrams ---------- */
  function mapping(spec) {
    var n = Math.max(spec.left.length, spec.right.length), H = 40 + n * 30, LX = 70, RX = 230;
    var ly = function (i) { return 34 + i * 30 + (n - spec.left.length) * 15; }, ry = function (j) { return 34 + j * 30 + (n - spec.right.length) * 15; };
    var h = ['<svg class="mm-map" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 300 ' + H + '" width="2.6in" role="img" aria-label="mapping diagram">',
      '<defs><marker id="mmah" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto"><path d="M0 0L8 4L0 8z" fill="#1d4ed8"/></marker></defs>',
      '<ellipse cx="' + LX + '" cy="' + (H / 2 + 2) + '" rx="34" ry="' + (H / 2 - 8) + '" fill="none" stroke="#111" stroke-width="1.4"/>',
      '<ellipse cx="' + RX + '" cy="' + (H / 2 + 2) + '" rx="34" ry="' + (H / 2 - 8) + '" fill="none" stroke="#111" stroke-width="1.4"/>',
      '<text x="' + LX + '" y="12" text-anchor="middle" font-size="11" font-family="Arial,sans-serif" font-weight="700">' + (spec.labels ? spec.labels[0] : 'Input') + '</text>',
      '<text x="' + RX + '" y="12" text-anchor="middle" font-size="11" font-family="Arial,sans-serif" font-weight="700">' + (spec.labels ? spec.labels[1] : 'Output') + '</text>'];
    spec.left.forEach(function (v, i) { h.push('<text class="mp-l" x="' + LX + '" y="' + (ly(i) + 4) + '" text-anchor="middle" font-size="13" font-family="Arial,sans-serif">' + numTxt(v) + '</text>'); });
    spec.right.forEach(function (v, j) { h.push('<text class="mp-r" x="' + RX + '" y="' + (ry(j) + 4) + '" text-anchor="middle" font-size="13" font-family="Arial,sans-serif">' + numTxt(v) + '</text>'); });
    spec.arrows.forEach(function (a) { h.push('<line class="mp-arrow" x1="' + (LX + 16) + '" y1="' + ly(a[0]) + '" x2="' + (RX - 18) + '" y2="' + ry(a[1]) + '" stroke="#1d4ed8" stroke-width="1.6" marker-end="url(#mmah)"/>'); });
    h.push('</svg>'); return h.join('');
  }
  function readMapping(svg) {
    var col = function (cls) { return (svg.match(new RegExp('<text class="' + cls + '"[^>]*>[^<]*</text>', 'g')) || []).map(function (t) { return { y: +attr(t, 'y') - 4, v: t.replace(/<[^>]+>/g, '').replace(/−/g, '-') }; }); };
    var L = col('mp-l'), R = col('mp-r');
    var pick = function (list, y) { return list.filter(function (e) { return Math.abs(e.y - y) < 1; })[0]; };
    var pairs = (svg.match(/<line class="mp-arrow"[^>]*>/g) || []).map(function (l) { return [pick(L, +attr(l, 'y1')).v, pick(R, +attr(l, 'y2')).v]; });
    return { left: L.map(function (e) { return e.v; }), right: R.map(function (e) { return e.v; }), pairs: pairs };
  }


  /* ---------- statistics displays: dot plots, box plots, scatter plots, two-way tables ----------
     Every display is drawn from a spec and can be read back from the drawing. */
  var FONT = 'font-family="Arial,sans-serif"';
  function axis(h, x0, x1, y, min, max, step, X) {
    h.push('<path d="M' + x0 + ' ' + y + 'H' + x1 + '" stroke="#111" stroke-width="1.4"/>');
    for (var t = min; t <= max + 1e-9; t += step) {
      var tv = Math.round(t * 1000) / 1000;
      h.push('<path d="M' + X(tv) + ' ' + (y - 4) + 'V' + (y + 4) + '" stroke="#111" stroke-width="1.2"/><text x="' + X(tv) + '" y="' + (y + 16) + '" text-anchor="middle" font-size="10" ' + FONT + '>' + numTxt(tv) + '</text>');
    }
  }
  function dotplot(spec) {
    var W = 400, L = 24, R = W - 24, maxc = 0, vals = Object.keys(spec.counts).map(Number);
    vals.forEach(function (v) { maxc = Math.max(maxc, spec.counts[v]); });
    var unit = (R - L) / (spec.max - spec.min), X = function (v) { return +(L + (v - spec.min) * unit).toFixed(2); }, H = 40 + maxc * 13, base = H - 26;
    var h = ['<svg class="mm-dot" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 ' + W + ' ' + H + '" width="4in" role="img" aria-label="dot plot" data-min="' + spec.min + '" data-l="' + L + '" data-unit="' + unit.toFixed(6) + '">'];
    axis(h, L - 10, R + 10, base, spec.min, spec.max, spec.step || 1, X);
    vals.forEach(function (v) { for (var i = 0; i < spec.counts[v]; i++) h.push('<circle class="dp-dot" cx="' + X(v) + '" cy="' + (base - 9 - i * 12) + '" r="5" fill="#1d4ed8"/>'); });
    if (spec.label) h.push('<text x="' + (W / 2) + '" y="' + (H - 1) + '" text-anchor="middle" font-size="10.5" ' + FONT + '>' + spec.label + '</text>');
    h.push('</svg>'); return h.join('');
  }
  function readDotplot(svg) {
    var root = /<svg[^>]*>/.exec(svg)[0], min = +attr(root, 'data-min'), L = +attr(root, 'data-l'), unit = +attr(root, 'data-unit');
    return (svg.match(/<circle class="dp-dot"[^>]*>/g) || []).map(function (c) { return Math.round(((+attr(c, 'cx') - L) / unit + min) * 100) / 100; }).sort(function (a, b) { return a - b; });
  }
  function boxplot(spec) {
    var W = 400, L = 60, R = W - 20, n = spec.boxes.length, H = 34 + n * 46, unit = (R - L) / (spec.max - spec.min), X = function (v) { return +(L + (v - spec.min) * unit).toFixed(2); }, base = H - 22;
    var h = ['<svg class="mm-box" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 ' + W + ' ' + H + '" width="4in" role="img" aria-label="box plot" data-min="' + spec.min + '" data-l="' + L + '" data-unit="' + unit.toFixed(6) + '">'];
    axis(h, L - 8, R + 6, base, spec.min, spec.max, spec.step || 1, X);
    spec.boxes.forEach(function (b, i) {
      var cy = 22 + i * 46, q = b.q;
      h.push('<g class="bp" data-label="' + String(b.label || '').replace(/"/g, '') + '">');
      if (b.label) h.push('<text x="' + (L - 8) + '" y="' + (cy + 4) + '" text-anchor="end" font-size="11" font-weight="700" ' + FONT + '>' + b.label + '</text>');
      h.push('<path class="bp-whisker" d="M' + X(q[0]) + ' ' + cy + 'H' + X(q[1]) + 'M' + X(q[3]) + ' ' + cy + 'H' + X(q[4]) + '" stroke="#111" stroke-width="1.6"/>');
      h.push('<path class="bp-end" d="M' + X(q[0]) + ' ' + (cy - 8) + 'V' + (cy + 8) + '" stroke="#111" stroke-width="1.6"/><path class="bp-end" d="M' + X(q[4]) + ' ' + (cy - 8) + 'V' + (cy + 8) + '" stroke="#111" stroke-width="1.6"/>');
      h.push('<rect class="bp-boxr" x="' + X(q[1]) + '" y="' + (cy - 14) + '" width="' + (X(q[3]) - X(q[1])).toFixed(2) + '" height="28" fill="#dbe7ff" stroke="#111" stroke-width="1.6"/>');
      h.push('<path class="bp-med" d="M' + X(q[2]) + ' ' + (cy - 14) + 'V' + (cy + 14) + '" stroke="#111" stroke-width="2.4"/></g>');
    });
    h.push('</svg>'); return h.join('');
  }
  function readBoxplot(svg) {
    var root = /<svg[^>]*>/.exec(svg)[0], min = +attr(root, 'data-min'), L = +attr(root, 'data-l'), unit = +attr(root, 'data-unit');
    var v = function (px) { return Math.round(((px - L) / unit + min) * 100) / 100; };
    return (svg.match(/<g class="bp"[\s\S]*?<\/g>/g) || []).map(function (g) {
      var ends = (g.match(/<path class="bp-end" d="M([-\d.]+)/g) || []).map(function (m) { return v(+/M([-\d.]+)/.exec(m)[1]); });
      var rect = /<rect class="bp-boxr"[^>]*>/.exec(g)[0], x = +attr(rect, 'x'), w = +attr(rect, 'width');
      var med = v(+/<path class="bp-med" d="M([-\d.]+)/.exec(g)[1]);
      return { label: attr(/<g class="bp"[^>]*>/.exec(g)[0], 'data-label'), q: [Math.min.apply(null, ends), v(x), med, v(x + w), Math.max.apply(null, ends)] };
    });
  }
  function scatter(spec) {
    var W = 360, H = 300, L = 46, B = H - 38, T = 12, R = W - 14;
    var ux = (R - L) / (spec.xmax - spec.xmin), uy = (B - T) / (spec.ymax - spec.ymin), X = function (x) { return +(L + (x - spec.xmin) * ux).toFixed(2); }, Y = function (y) { return +(B - (y - spec.ymin) * uy).toFixed(2); };
    var h = ['<svg class="mm-scatter" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 ' + W + ' ' + H + '" width="3.4in" role="img" aria-label="scatter plot" data-xmin="' + spec.xmin + '" data-ymin="' + spec.ymin + '" data-l="' + L + '" data-b="' + B + '" data-ux="' + ux.toFixed(6) + '" data-uy="' + uy.toFixed(6) + '">'];
    for (var gx = spec.xmin; gx <= spec.xmax + 1e-9; gx += spec.xstep) h.push('<path d="M' + X(gx) + ' ' + T + 'V' + B + '" stroke="#ddd"/><text x="' + X(gx) + '" y="' + (B + 13) + '" text-anchor="middle" font-size="9.5" ' + FONT + '>' + numTxt(gx) + '</text>');
    for (var gy = spec.ymin; gy <= spec.ymax + 1e-9; gy += spec.ystep) h.push('<path d="M' + L + ' ' + Y(gy) + 'H' + R + '" stroke="#ddd"/><text x="' + (L - 5) + '" y="' + (Y(gy) + 3) + '" text-anchor="end" font-size="9.5" ' + FONT + '>' + numTxt(gy) + '</text>');
    h.push('<path d="M' + L + ' ' + T + 'V' + B + 'H' + R + '" stroke="#111" stroke-width="1.4" fill="none"/>');
    if (spec.xlabel) h.push('<text x="' + ((L + R) / 2) + '" y="' + (H - 4) + '" text-anchor="middle" font-size="10.5" ' + FONT + '>' + spec.xlabel + '</text>');
    if (spec.ylabel) h.push('<text transform="translate(11 ' + ((T + B) / 2) + ') rotate(-90)" text-anchor="middle" font-size="10.5" ' + FONT + '>' + spec.ylabel + '</text>');
    if (spec.line) { var a = spec.line; h.push('<path class="sc-line" d="M' + X(a[0][0]) + ' ' + Y(a[0][1]) + 'L' + X(a[1][0]) + ' ' + Y(a[1][1]) + '" stroke="#e04848" stroke-width="2" stroke-dasharray="6 4"/>'); }
    spec.points.forEach(function (p) { h.push('<circle class="sc-pt" cx="' + X(p[0]) + '" cy="' + Y(p[1]) + '" r="4" fill="#1d4ed8"/>'); });
    h.push('</svg>'); return h.join('');
  }
  function readScatter(svg) {
    var root = /<svg[^>]*>/.exec(svg)[0], g = function (n) { return +attr(root, n); };
    return (svg.match(/<circle class="sc-pt"[^>]*>/g) || []).map(function (c) { return [Math.round(((+attr(c, 'cx') - g('data-l')) / g('data-ux') + g('data-xmin')) * 100) / 100, Math.round(((g('data-b') - +attr(c, 'cy')) / g('data-uy') + g('data-ymin')) * 100) / 100]; });
  }
  function twoway(spec) {
    var cell = function (v) { return typeof v === 'number' ? numTxt(v) : String(v).replace(/[<>&]/g, ''); };
    return '<table class="mm-ftable mm-twoway"><thead><tr><th>' + cell(spec.corner || '') + '</th>' + spec.cols.map(function (c) { return '<th>' + cell(c) + '</th>'; }).join('') + '</tr></thead><tbody>' +
      spec.rows.map(function (r) { return '<tr><th>' + cell(r.label) + '</th>' + r.cells.map(function (v) { return '<td>' + cell(v) + '</td>'; }).join('') + '</tr>'; }).join('') + '</tbody></table>';
  }
  function readTwoway(html) {
    var txt = function (s) { return s.replace(/<[^>]+>/g, '').replace(/−/g, '-').trim(); };
    var head = (/<thead>[\s\S]*?<\/thead>/.exec(html)[0].match(/<th>[^<]*<\/th>/g) || []).map(txt).slice(1);
    var rows = (/<tbody>[\s\S]*?<\/tbody>/.exec(html)[0].match(/<tr>[\s\S]*?<\/tr>/g) || []).map(function (tr) { return { label: txt(/<th>[^<]*<\/th>/.exec(tr)[0]), cells: (tr.match(/<td>[^<]*<\/td>/g) || []).map(txt) }; });
    return { cols: head, rows: rows };
  }

  NS.fig = { numberLine: numberLine, readNumberLine: readNumberLine, windowFor: windowFor, plane: plane, readPlane: readPlane, table: table, readTable: readTable, mapping: mapping, readMapping: readMapping, dotplot: dotplot, readDotplot: readDotplot, boxplot: boxplot, readBoxplot: readBoxplot, scatter: scatter, readScatter: readScatter, twoway: twoway, readTwoway: readTwoway };
  NS.figHtml = function (spec) {
    if (!spec) return '';
    var inner = spec.kind === 'numberline' ? numberLine(spec) : spec.kind === 'plane' ? plane(spec) : spec.kind === 'table' ? table(spec) : spec.kind === 'mapping' ? mapping(spec) : spec.kind === 'dotplot' ? dotplot(spec) : spec.kind === 'boxplot' ? boxplot(spec) : spec.kind === 'scatter' ? scatter(spec) : spec.kind === 'twoway' ? twoway(spec) : '';
    return inner ? '<div class="mm-fig mm-fig-' + spec.kind + '">' + inner + '</div>' : '';
  };
})(typeof window !== 'undefined' ? window : globalThis);
