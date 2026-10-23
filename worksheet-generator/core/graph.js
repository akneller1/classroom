/* SVG coordinate planes and small HTML tables.
   A graph is described by a plain "spec" object, so the same spec can be drawn blank,
   with a pre-drawn line, or as an answer, and tests can re-read the drawn geometry.

   spec = { xmin, xmax, ymin, ymax, lines:[{kind:'line',m,b}|{kind:'vline',x}], points:[{x,y,open,label}] }
   Every drawn line is a <path class="gline"> whose endpoints can be mapped back to math
   coordinates with the data-* attributes on the root <svg>. */
(function (G) {
  'use strict';
  var NS = (G.MKWS = G.MKWS || {});
  var Fr = NS.frac.Fr, T = NS.tex;

  var CELL = 14, PAD = { l: 20, r: 18, t: 18, b: 20 };

  function r2(v) { return Math.round(v * 100) / 100; }

  /* Clip the infinite line to the window; returns [[x1,y1],[x2,y2]] in math coordinates or null. */
  function clipLine(line, w) {
    var p, d;
    if (line.kind === 'vline') { var xv = Fr.of(line.x).val(); p = [xv, 0]; d = [0, 1]; }
    else { var m = Fr.of(line.m).val(), b = Fr.of(line.b).val(); p = [0, b]; d = [1, m]; }
    var t0 = -Infinity, t1 = Infinity;
    function clip(pp, dd, lo, hi) {
      if (Math.abs(dd) < 1e-12) return pp >= lo - 1e-9 && pp <= hi + 1e-9;
      var a = (lo - pp) / dd, c = (hi - pp) / dd;
      if (a > c) { var t = a; a = c; c = t; }
      t0 = Math.max(t0, a); t1 = Math.min(t1, c);
      return t0 <= t1;
    }
    if (!clip(p[0], d[0], w.xmin, w.xmax)) return null;
    if (!clip(p[1], d[1], w.ymin, w.ymax)) return null;
    if (!isFinite(t0) || !isFinite(t1)) return null;
    return [[p[0] + t0 * d[0], p[1] + t0 * d[1]], [p[0] + t1 * d[0], p[1] + t1 * d[1]]];
  }

  function graph(spec, opts) {
    opts = opts || {};
    var xmin = spec.xmin === undefined ? -10 : spec.xmin, xmax = spec.xmax === undefined ? 10 : spec.xmax;
    var ymin = spec.ymin === undefined ? -10 : spec.ymin, ymax = spec.ymax === undefined ? 10 : spec.ymax;
    var widthIn = opts.widthIn || 2.8;
    var W = (xmax - xmin) * CELL, H = (ymax - ymin) * CELL;
    var vbW = W + PAD.l + PAD.r, vbH = H + PAD.t + PAD.b;
    function X(x) { return PAD.l + (x - xmin) * CELL; }
    function Y(y) { return PAD.t + (ymax - y) * CELL; }
    var lab = spec.labelEvery || ((xmax - xmin) > 12 ? 2 : 1);
    var o = [];
    o.push('<svg xmlns="http://www.w3.org/2000/svg" class="mkgraph" role="img" aria-label="coordinate plane"' +
      ' viewBox="0 0 ' + vbW + ' ' + vbH + '" width="' + r2(widthIn) + 'in" height="' + r2(widthIn * vbH / vbW) + 'in"' +
      ' data-xmin="' + xmin + '" data-xmax="' + xmax + '" data-ymin="' + ymin + '" data-ymax="' + ymax + '"' +
      ' data-cell="' + CELL + '" data-padl="' + PAD.l + '" data-padt="' + PAD.t + '">');
    o.push('<rect x="' + PAD.l + '" y="' + PAD.t + '" width="' + W + '" height="' + H + '" fill="#fff"/>');
    // grid
    var i;
    for (i = xmin; i <= xmax; i++) {
      var major = (i % 5 === 0);
      o.push('<line x1="' + X(i) + '" y1="' + PAD.t + '" x2="' + X(i) + '" y2="' + (PAD.t + H) + '" stroke="' + (major ? '#555d68' : '#88929d') + '" stroke-width="' + (major ? 1.2 : 0.85) + '"/>');
    }
    for (i = ymin; i <= ymax; i++) {
      var majorY = (i % 5 === 0);
      o.push('<line x1="' + PAD.l + '" y1="' + Y(i) + '" x2="' + (PAD.l + W) + '" y2="' + Y(i) + '" stroke="' + (majorY ? '#555d68' : '#88929d') + '" stroke-width="' + (majorY ? 1.2 : 0.85) + '"/>');
    }
    o.push('<rect x="' + PAD.l + '" y="' + PAD.t + '" width="' + W + '" height="' + H + '" fill="none" stroke="#303741" stroke-width="1.15"/>');
    // axes with arrows
    var ax = X(0), ay = Y(0), A = 6.5, AW = 3;
    o.push('<g stroke="#111" stroke-width="1.9" fill="#111">');
    o.push('<line x1="' + (PAD.l - 6) + '" y1="' + ay + '" x2="' + (PAD.l + W + 6) + '" y2="' + ay + '"/>');
    o.push('<line x1="' + ax + '" y1="' + (PAD.t + H + 6) + '" x2="' + ax + '" y2="' + (PAD.t - 6) + '"/>');
    o.push('<polygon stroke="none" points="' + (PAD.l + W + 6 + A) + ',' + ay + ' ' + (PAD.l + W + 6) + ',' + (ay - AW) + ' ' + (PAD.l + W + 6) + ',' + (ay + AW) + '"/>');
    o.push('<polygon stroke="none" points="' + (PAD.l - 6 - A) + ',' + ay + ' ' + (PAD.l - 6) + ',' + (ay - AW) + ' ' + (PAD.l - 6) + ',' + (ay + AW) + '"/>');
    o.push('<polygon stroke="none" points="' + ax + ',' + (PAD.t - 6 - A) + ' ' + (ax - AW) + ',' + (PAD.t - 6) + ' ' + (ax + AW) + ',' + (PAD.t - 6) + '"/>');
    o.push('<polygon stroke="none" points="' + ax + ',' + (PAD.t + H + 6 + A) + ' ' + (ax - AW) + ',' + (PAD.t + H + 6) + ' ' + (ax + AW) + ',' + (PAD.t + H + 6) + '"/>');
    o.push('</g>');
    // ticks + numbers
    var F = 'font-family="Atkinson Hyperlegible, Segoe UI, Arial, sans-serif" font-size="12" fill="#111"';
    var halo = ' stroke="#fff" stroke-width="3" paint-order="stroke" stroke-linejoin="round"';
    for (i = xmin; i <= xmax; i++) {
      if (i === 0) continue;
      o.push('<line x1="' + X(i) + '" y1="' + (ay - 2.6) + '" x2="' + X(i) + '" y2="' + (ay + 2.6) + '" stroke="#111" stroke-width="1"/>');
      if (i % lab === 0) o.push('<text x="' + X(i) + '" y="' + (ay + 12.5) + '" text-anchor="middle" ' + F + halo + '>' + T.plain(i) + '</text>');
    }
    for (i = ymin; i <= ymax; i++) {
      if (i === 0) continue;
      o.push('<line x1="' + (ax - 2.6) + '" y1="' + Y(i) + '" x2="' + (ax + 2.6) + '" y2="' + Y(i) + '" stroke="#111" stroke-width="1"/>');
      if (i % lab === 0) o.push('<text x="' + (ax - 5) + '" y="' + (Y(i) + 3.4) + '" text-anchor="end" ' + F + halo + '>' + T.plain(i) + '</text>');
    }
    o.push('<text x="' + (ax - 5) + '" y="' + (ay + 12.5) + '" text-anchor="end" ' + F + halo + '>0</text>');
    o.push('<text x="' + (PAD.l + W + 4) + '" y="' + (ay + 15) + '" ' + F.replace('font-size="12"', 'font-size="13" font-style="italic"') + '>x</text>');
    o.push('<text x="' + (ax + 6) + '" y="' + (PAD.t - 4) + '" ' + F.replace('font-size="12"', 'font-size="13" font-style="italic"') + '>y</text>');
    // Subtle hatch fill for solutions; SVG remains legible when printed in grayscale.
    if (spec.shade && spec.shade.m !== undefined) {
      var sh = spec.shade, mm = Number(sh.m), bb = Number(sh.b), yy1 = Math.max(ymin, Math.min(ymax, mm * xmin + bb)), yy2 = Math.max(ymin, Math.min(ymax, mm * xmax + bb));
      var fillY = sh.above ? PAD.t : PAD.t + H;
      o.push('<polygon points="' + X(xmin) + ',' + Y(yy1) + ' ' + X(xmax) + ',' + Y(yy2) + ' ' + X(xmax) + ',' + fillY + ' ' + X(xmin) + ',' + fillY + '" fill="#b2b9c2" fill-opacity="0.24"/>');
    }
    if (spec.shade && spec.shade.x !== undefined) {
      var boundX = Math.max(xmin, Math.min(xmax, Number(spec.shade.x)));
      var leftEdge = spec.shade.right ? X(boundX) : X(xmin);
      var rightEdge = spec.shade.right ? X(xmax) : X(boundX);
      o.push('<rect x="' + leftEdge + '" y="' + PAD.t + '" width="' + Math.max(0,rightEdge-leftEdge) + '" height="' + H + '" fill="#b2b9c2" fill-opacity="0.24"/>');
    }
    // lines
    (spec.lines || []).forEach(function (ln) {
      var seg = clipLine(ln, { xmin: xmin, xmax: xmax, ymin: ymin, ymax: ymax });
      if (!seg) return;
      var a = [X(seg[0][0]), Y(seg[0][1])], b = [X(seg[1][0]), Y(seg[1][1])];
      var dx = b[0] - a[0], dy = b[1] - a[1], len = Math.sqrt(dx * dx + dy * dy) || 1, ux = dx / len, uy = dy / len;
      var L = 8, Wd = 3.4;
      function head(tip, dir) {            // arrowhead with its tip at `tip`, pointing along `dir`
        var bx = tip[0] - dir * ux * L, by = tip[1] - dir * uy * L;
        return '<polygon fill="#111" points="' + r2(tip[0]) + ',' + r2(tip[1]) + ' ' + r2(bx - uy * Wd) + ',' + r2(by + ux * Wd) + ' ' + r2(bx + uy * Wd) + ',' + r2(by - ux * Wd) + '"/>';
      }
      o.push('<path class="gline" d="M' + r2(a[0]) + ' ' + r2(a[1]) + ' L' + r2(b[0]) + ' ' + r2(b[1]) + '" stroke="#111" stroke-width="2.6" fill="none" stroke-linecap="round"' + (ln.dashed ? ' stroke-dasharray="8 6"' : '') + '/>');
      if (!ln.dashed) { o.push(head(b, 1)); o.push(head(a, -1)); }
    });
    // points
    (spec.points || []).forEach(function (p) {
      var cx = X(Fr.of(p.x).val()), cy = Y(Fr.of(p.y).val());
      o.push('<circle class="gpt" cx="' + r2(cx) + '" cy="' + r2(cy) + '" r="3.6" fill="' + (p.open ? '#fff' : '#111') + '" stroke="#111" stroke-width="1.6"/>');
      if (p.label) {
        var txt = '(' + T.plain(p.x) + ', ' + T.plain(p.y) + ')';
        var right = Fr.of(p.x).val() <= xmax - 5, up = Fr.of(p.y).val() <= ymax - 2;
        o.push('<text x="' + r2(cx + (right ? 6 : -6)) + '" y="' + r2(cy + (up ? -6 : 13)) + '" text-anchor="' + (right ? 'start' : 'end') + '" ' + F.replace('font-size="12"', 'font-size="11" font-weight="700"') + halo + '>' + txt + '</text>');
      }
    });
    o.push('</svg>');
    return o.join('');
  }

  /* Table of values. rows = [{label:'x', cells:[numbers], blank:false}, ...]; blank rows show empty boxes. */
  function table(rows, blankAll) {
    var h = ['<table class="vt"><tbody>'];
    rows.forEach(function (r) {
      h.push('<tr><th>' + T.M(r.label) + '</th>');
      r.cells.forEach(function (c) {
        if (r.blank && !blankAll) h.push('<td class="blank">&nbsp;</td>');
        else h.push('<td>' + T.M(T.num(c)) + '</td>');
      });
      h.push('</tr>');
    });
    h.push('</tbody></table>');
    return h.join('');
  }

  NS.graph = graph;
  NS.table = table;
  NS.graphGeom = { CELL: CELL, PAD: PAD, clipLine: clipLine };
})(typeof window !== 'undefined' ? window : globalThis);
