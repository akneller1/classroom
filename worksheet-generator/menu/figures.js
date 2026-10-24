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
  function toRational(v) {   // nearest fraction with a small denominator (number lines only use these)
    for (var d = 1; d <= 12; d++) { var n = Math.round(v * d); if (Math.abs(n / d - v) < 1e-4) return [n, d]; }
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

  NS.fig = { numberLine: numberLine, readNumberLine: readNumberLine, windowFor: windowFor };
  NS.figHtml = function (spec) { return spec && spec.kind === 'numberline' ? '<div class="mm-fig">' + numberLine(spec) + '</div>' : ''; };
})(typeof window !== 'undefined' ? window : globalThis);
