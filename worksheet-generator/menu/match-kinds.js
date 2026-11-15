/* Matching card sorts beyond functions: the shared core.
   A "kind" is one matching activity (for example Data Displays: dot plot ↔ histogram ↔ box plot ↔ summary).
   Each kind registers itself with MKMATCH.register({...}) from its own file and supplies:
     id, name (game title), noun (what one set is), blurb, tip (first hint),
     types: [{ id, L (card letter), name, plural }], anchor (type that can start in its set), anchorText,
     fams: { id: label } (optional sub-types the teacher can choose), units: { unitId: { fams, def, types } },
     gen(rng, level, cfg, unit, sets)  → one candidate set (or null),
     key(type, set) → a string that says what the card shows (two sets whose cards show the same thing clash),
     fits(type, a, b) (optional) → true when a's card of that type would also describe b,
     finish(sets, rng, level, cfg, unit) (optional) → choose cards that depend on the other sets (descriptions),
     face(set, type, mode, B) → HTML for the card (mode 'full' tray, 'mini' in a set, 'big' zoom, 'print').
   MKMATCH.build() makes the sets: every card is checked against every other set, both ways, so each card
   fits exactly one set. Everything is seeded: the same unit, level, options, seed and version give the same cards.
   Needs: core/rng.js. KaTeX for faces (window.katex). No DOM. */
(function (G) {
  'use strict';
  var WS = G.MKWS;
  var MK = G.MKMATCH = G.MKMATCH || { kinds: {} };
  MK.register = function (K) { MK.kinds[K.id] = K; return K; };
  MK.LEVELS = ['cp2', 'cp1', 'honors'];

  /* ---------------- numbers ---------------- */
  var U = MK.util = {};
  U.rngOf = function () { return WS.rng.make(WS.rng.hash([].slice.call(arguments).join('|'))); };
  U.near = function (a, b, e) { return Math.abs(a - b) < (e || 1e-7); };
  U.isInt = function (v) { return isFinite(v) && Math.abs(v - Math.round(v)) < 1e-9; };
  U.gcd = function (a, b) { a = Math.abs(a); b = Math.abs(b); while (b) { var t = a % b; a = b; b = t; } return a || 1; };
  U.toQ = function (v, maxD) { for (var d = 1; d <= (maxD || 200); d++) { var n = Math.round(v * d); if (Math.abs(n / d - v) < 1e-9) return { n: n, d: d }; } return null; };
  U.round = function (v, p) { var m = Math.pow(10, p || 0); return Math.round(v * m) / m; };
  /* a number as TeX: integer, simple fraction, or decimal */
  U.tex = function (v, opts) {
    opts = opts || {};
    if (U.isInt(v)) return String(Math.round(v));
    var q = U.toQ(v, 64);
    if (q && !opts.decimal && q.d <= (opts.maxD || 32)) return (q.n < 0 ? '-' : '') + (opts.mixed && Math.abs(q.n) > q.d ? Math.floor(Math.abs(q.n) / q.d) + '\\tfrac{' + (Math.abs(q.n) % q.d) + '}{' + q.d + '}' : '\\frac{' + Math.abs(q.n) + '}{' + q.d + '}');
    return String(U.round(v, opts.places === undefined ? 2 : opts.places));
  };
  /* a number as plain text for SVG labels (true minus sign) */
  U.txt = function (v) {
    if (U.isInt(v)) return (v < 0 ? '−' : '') + Math.abs(Math.round(v));
    var q = U.toQ(v, 16); if (q && q.d <= 8) return (q.n < 0 ? '−' : '') + Math.abs(q.n) + '/' + q.d;
    return (v < 0 ? '−' : '') + String(U.round(Math.abs(v), 2));
  };
  U.esc = function (s) { return String(s === undefined || s === null ? '' : s).replace(/[&<>"']/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]; }); };
  U.k = function (s) { try { return G.katex ? G.katex.renderToString(String(s), { throwOnError: false }) : U.esc(s); } catch (e) { return U.esc(s); } };
  U.kd = function (s) { return U.k('\\displaystyle ' + s); };
  /* a big formula card: shrink long formulas so they stay on one line */
  U.bigTex = function (s, display) { var n = String(s).replace(/\\(left|right|displaystyle|text|frac|tfrac|sqrt)|[{}\s\\]/g, '').length, cls = n > 34 ? ' xl' : n > 24 ? ' l' : n > 16 ? ' m' : ''; return '<div class="mk-txt mk-big' + cls + '">' + (display ? U.kd(s) : U.k(s)) + '</div>'; };
  /* text with ⟨math⟩ snippets */
  U.mt = function (t) { return String(t).split(/(⟨[^⟩]*⟩)/).map(function (p) { return /^⟨/.test(p) ? U.k(p.slice(1, -1)) : U.esc(p); }).join(''); };
  U.m = function (s) { return '⟨' + s + '⟩'; };
  U.wpick = function (rng, w) { var tot = 0, k; for (k in w) tot += w[k]; var r = rng.next() * tot; for (k in w) { r -= w[k]; if (r < 0) return k; } return Object.keys(w)[0]; };
  U.lvl = function (L, a, b, c) { return L === 'cp2' ? a : L === 'cp1' ? b : c; };
  /* whole numbers as words: 345 → "three hundred forty-five", 305472 → "three hundred five thousand, four hundred seventy-two" */
  var ONES = ['zero', 'one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine', 'ten', 'eleven', 'twelve', 'thirteen', 'fourteen', 'fifteen', 'sixteen', 'seventeen', 'eighteen', 'nineteen'], TENS = ['', '', 'twenty', 'thirty', 'forty', 'fifty', 'sixty', 'seventy', 'eighty', 'ninety'];
  function under1000(n) { var h = Math.floor(n / 100), r = n % 100, out = h ? ONES[h] + ' hundred' : ''; if (r) out += (out ? ' ' : '') + (r < 20 ? ONES[r] : TENS[Math.floor(r / 10)] + (r % 10 ? '-' + ONES[r % 10] : '')); return out; }
  U.words = function (n) {
    if (n === 0) return 'zero';
    var parts = [], m = Math.floor(n / 1e6), th = Math.floor(n / 1000) % 1000, r = n % 1000;
    if (m) parts.push(under1000(m) + ' million'); if (th) parts.push(under1000(th) + ' thousand'); if (r) parts.push(under1000(r));
    return parts.join(', ');
  };
  U.median = function (s) { var n = s.length; return n % 2 ? s[(n - 1) / 2] : (s[n / 2 - 1] + s[n / 2]) / 2; };

  /* ---------------- SVG ---------------- */
  var S = MK.svg = {};
  var INK = '#16202e', GRID = '#c7cfdb', BLUE = '#1d4ed8', ORANGE = '#c2410c', FONT = 'font-family="Arial,sans-serif"';
  S.colors = { ink: INK, grid: GRID, blue: BLUE, orange: ORANGE, green: '#15803d', purple: '#7c3aed', shade: '#bfdbfe' };
  function t(x, y, s, o) { o = o || {}; return '<text x="' + (+x).toFixed(1) + '" y="' + (+y).toFixed(1) + '" text-anchor="' + (o.a || 'middle') + '" font-size="' + (o.fs || 12) + '" ' + (o.it ? 'font-style="italic" font-family="Georgia,serif"' : FONT) + (o.bold ? ' font-weight="700"' : '') + ' fill="' + (o.fill || '#222') + '"' + (o.halo === false ? '' : ' stroke="#fff" stroke-width="3" paint-order="stroke"') + '>' + s + '</text>'; }
  S.text = t;
  /* visible pieces of y = f(x) inside a window, broken at asymptotes / jumps */
  S.sample = function (f, w, opts) {
    opts = opts || {};
    var out = [], cur = null, N = opts.n || 500, lo = opts.lo !== undefined ? opts.lo : w.xmin, hi = opts.hi !== undefined ? opts.hi : w.xmax, step = (hi - lo) / N, ylo = w.ymin - (w.ymax - w.ymin) * 0.02, yhi = w.ymax + (w.ymax - w.ymin) * 0.02;
    for (var i = 0; i <= N; i++) {
      var x = lo + i * step, y = f(x), ok = isFinite(y) && y >= ylo && y <= yhi;
      if (ok) { if (!cur) cur = []; cur.push([x, Math.max(w.ymin, Math.min(w.ymax, y))]); }
      else if (cur) { out.push(cur); cur = null; }
    }
    if (cur) out.push(cur);
    return out.filter(function (c) { return c.length > 1; });
  };
  /* coordinate plane. spec: xmin,xmax,ymin,ymax,xstep,ystep, xticks [{v,s}] (optional, e.g. multiples of π),
     lab ['x','y'], items: curve {pts|pieces, color, w, dash} · dot {x,y,color,open,r} · poly {pts, labels, color, fill, dash}
     · vline {x,dash} · hline {y,dash} · seg {a,b,color,w}. opts: { big, w (viewBox width), h } */
  S.plane = function (spec, opts) {
    opts = opts || {};
    var W = opts.w || 320, H = opts.h || W, P = 22, big = !!opts.big;
    var sx = (W - 2 * P) / (spec.xmax - spec.xmin), sy = (H - 2 * P) / (spec.ymax - spec.ymin);
    var X = function (x) { return P + (x - spec.xmin) * sx; }, Y = function (y) { return P + (spec.ymax - y) * sy; };
    var meta = { xmin: spec.xmin, xmax: spec.xmax, ymin: spec.ymin, ymax: spec.ymax, xstep: spec.xstep, ystep: spec.ystep, pad: P, w: W, h: H, xpi: spec.xpi || 0 };
    var h = '<svg class="mg-svg mk-plane" viewBox="0 0 ' + W + ' ' + H + '" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="' + U.esc(opts.label || 'graph') + '" data-plane=\'' + JSON.stringify(meta) + '\'>';
    h += '<rect width="' + W + '" height="' + H + '" fill="#fff"/>';
    var gx, gy, e = 1e-9;
    for (gx = Math.ceil(spec.xmin / spec.xstep - e) * spec.xstep; gx <= spec.xmax + e; gx += spec.xstep) h += '<path d="M' + X(gx).toFixed(1) + ' ' + Y(spec.ymin).toFixed(1) + 'V' + Y(spec.ymax).toFixed(1) + '" stroke="' + GRID + '" stroke-width="1"/>';
    for (gy = Math.ceil(spec.ymin / spec.ystep - e) * spec.ystep; gy <= spec.ymax + e; gy += spec.ystep) h += '<path d="M' + X(spec.xmin).toFixed(1) + ' ' + Y(gy).toFixed(1) + 'H' + X(spec.xmax).toFixed(1) + '" stroke="' + GRID + '" stroke-width="1"/>';
    var y0 = Math.min(Math.max(0, spec.ymin), spec.ymax), x0 = Math.min(Math.max(0, spec.xmin), spec.xmax);
    h += '<path d="M' + X(spec.xmin).toFixed(1) + ' ' + Y(y0).toFixed(1) + 'H' + X(spec.xmax).toFixed(1) + '" stroke="' + INK + '" stroke-width="1.8"/><path d="M' + X(x0).toFixed(1) + ' ' + Y(spec.ymin).toFixed(1) + 'V' + Y(spec.ymax).toFixed(1) + '" stroke="' + INK + '" stroke-width="1.8"/>';
    var lab = spec.lab || ['x', 'y'];
    h += t(X(spec.xmax) + 2, Y(y0) - 5, lab[0], { a: 'end', fs: 13, it: true }) + t(X(x0) + 6, Y(spec.ymax) + 11, lab[1], { a: 'start', fs: 13, it: true });
    var fs = big ? 10 : 13;
    var nx = (spec.xmax - spec.xmin) / spec.xstep, ny = (spec.ymax - spec.ymin) / spec.ystep;
    var lx = spec.xlabEvery || (nx > 8 && !big ? 2 : 1), ly = spec.ylabEvery || (ny > 8 && !big ? 2 : 1);
    if (spec.xticks) spec.xticks.forEach(function (tk, i) { if ((big || i % (spec.xtickEvery || 1) === 0) && Math.abs(tk.v) > e && tk.v > spec.xmin && tk.v < spec.xmax) h += t(X(tk.v), Y(y0) + fs + 2, tk.s, { fs: fs }); });
    else for (gx = Math.ceil(spec.xmin / (spec.xstep * lx) - e) * spec.xstep * lx; gx <= spec.xmax + e; gx += spec.xstep * lx) if (Math.abs(gx) > e && gx > spec.xmin + e && gx < spec.xmax - e) h += t(X(gx), Y(y0) + fs + 2, U.txt(gx), { fs: fs });
    for (gy = Math.ceil(spec.ymin / (spec.ystep * ly) - e) * spec.ystep * ly; gy <= spec.ymax + e; gy += spec.ystep * ly) if (Math.abs(gy) > e && gy > spec.ymin + e && gy < spec.ymax - e) h += t(X(x0) - 4, Y(gy) + fs / 3, U.txt(gy), { a: 'end', fs: fs });
    (spec.items || []).forEach(function (it) {
      var col = it.color || BLUE, dash = it.dash ? ' stroke-dasharray="' + (it.dash === true ? '7 5' : it.dash) + '"' : '';
      if (it.kind === 'curve') (it.pieces || [it.pts]).forEach(function (c) { if (c && c.length > 1) h += '<polyline fill="none" stroke="' + col + '" stroke-width="' + (it.w || 3.2) + '" stroke-linejoin="round" stroke-linecap="round"' + dash + ' points="' + c.map(function (p) { return X(p[0]).toFixed(1) + ',' + Y(p[1]).toFixed(1); }).join(' ') + '"/>'; });
      else if (it.kind === 'dot') h += '<circle cx="' + X(it.x).toFixed(1) + '" cy="' + Y(it.y).toFixed(1) + '" r="' + (it.r || 4.6) + '" fill="' + (it.open ? '#fff' : col) + '" stroke="' + (it.open ? col : '#fff') + '" stroke-width="' + (it.open ? 2.2 : 1.2) + '"/>';
      else if (it.kind === 'vline') h += '<path d="M' + X(it.x).toFixed(1) + ' ' + Y(spec.ymin).toFixed(1) + 'V' + Y(spec.ymax).toFixed(1) + '" stroke="' + (it.color || '#475569') + '" stroke-width="2"' + (dash || ' stroke-dasharray="7 5"') + '/>';
      else if (it.kind === 'hline') h += '<path d="M' + X(spec.xmin).toFixed(1) + ' ' + Y(it.y).toFixed(1) + 'H' + X(spec.xmax).toFixed(1) + '" stroke="' + (it.color || '#475569') + '" stroke-width="2"' + (dash || ' stroke-dasharray="7 5"') + '/>';
      else if (it.kind === 'seg') h += '<path d="M' + X(it.a[0]).toFixed(1) + ' ' + Y(it.a[1]).toFixed(1) + 'L' + X(it.b[0]).toFixed(1) + ' ' + Y(it.b[1]).toFixed(1) + '" stroke="' + col + '" stroke-width="' + (it.w || 2.5) + '"' + dash + '/>';
      else if (it.kind === 'poly') {
        h += '<polygon points="' + it.pts.map(function (p) { return X(p[0]).toFixed(1) + ',' + Y(p[1]).toFixed(1); }).join(' ') + '" fill="' + (it.fill || 'none') + '" fill-opacity="0.35" stroke="' + col + '" stroke-width="2.6"' + dash + '/>';
        var cx = it.pts.reduce(function (s, p) { return s + p[0]; }, 0) / it.pts.length, cy = it.pts.reduce(function (s, p) { return s + p[1]; }, 0) / it.pts.length;
        (it.labels || []).forEach(function (L, i) {
          var p = it.pts[i], dx = p[0] - cx, dy = p[1] - cy, d = Math.hypot(dx, dy) || 1;
          h += '<circle cx="' + X(p[0]).toFixed(1) + '" cy="' + Y(p[1]).toFixed(1) + '" r="3" fill="' + col + '"/>' + t(X(p[0]) + dx / d * 11, Y(p[1]) - dy / d * 11 + 4, L, { fs: big ? 11 : 13, bold: true, fill: col });
        });
      }
    });
    if (big) h += '<g class="mg-cross" visibility="hidden"><circle r="6" fill="none" stroke="#dc2626" stroke-width="2.4"/><rect class="mg-cbg" rx="4" height="22" fill="#16202e"/><text class="mg-ctx" font-size="14" font-family="Arial,sans-serif" font-weight="700" fill="#fff"></text></g>';
    return h + '</svg>';
  };
  /* tick labels at multiples of π/den between lo and hi */
  S.piTicks = function (lo, hi, den) {
    var out = [];
    for (var k = Math.ceil(lo * den / Math.PI - 1e-9); k * Math.PI / den <= hi + 1e-9; k++) {
      var q = U.toQ(k / den, 64), s;
      if (k === 0) s = '0';
      else { var n = Math.abs(q.n), d = q.d; s = (k < 0 ? '−' : '') + (n === 1 ? '' : n) + 'π' + (d > 1 ? '/' + d : ''); }
      out.push({ v: k * Math.PI / den, s: s });
    }
    return out;
  };
  /* number line. spec: lo, hi, step, labelEvery, parts [{lo,loC,hi,hiC}] (±Infinity allowed) */
  S.numberLine = function (spec, opts) {
    opts = opts || {};
    var W = 340, H = 86, P = 22, Y0 = 50, sx = (W - 2 * P) / (spec.hi - spec.lo), X = function (x) { return P + (x - spec.lo) * sx; };
    var h = '<svg class="mg-svg mk-nl" viewBox="0 0 ' + W + ' ' + H + '" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="number line">';
    h += '<rect width="' + W + '" height="' + H + '" fill="#fff"/>';
    h += '<path d="M' + (P - 14) + ' ' + Y0 + 'H' + (W - P + 14) + '" stroke="' + INK + '" stroke-width="2"/><path d="M' + (P - 16) + ' ' + Y0 + 'l9 -6v12z" fill="' + INK + '"/><path d="M' + (W - P + 16) + ' ' + Y0 + 'l-9 -6v12z" fill="' + INK + '"/>';
    var every = spec.labelEvery || 1, i = 0;
    for (var v = spec.lo; v <= spec.hi + 1e-9; v += spec.step, i++) {
      h += '<path d="M' + X(v).toFixed(1) + ' ' + (Y0 - 6) + 'V' + (Y0 + 6) + '" stroke="' + INK + '" stroke-width="1.5"/>';
      if (i % every === 0) h += t(X(v), Y0 + 26, U.txt(v), { fs: 15, halo: false });
    }
    (spec.parts || []).forEach(function (p) {
      var a = Math.max(spec.lo - 0.6 * spec.step, p.lo), b = Math.min(spec.hi + 0.6 * spec.step, p.hi);
      var xa = isFinite(p.lo) ? X(a) : P - 14, xb = isFinite(p.hi) ? X(b) : W - P + 14;
      h += '<path d="M' + xa.toFixed(1) + ' ' + Y0 + 'H' + xb.toFixed(1) + '" stroke="' + BLUE + '" stroke-width="6" stroke-linecap="butt"/>';
      if (!isFinite(p.lo)) h += '<path d="M' + (P - 18) + ' ' + Y0 + 'l12 -9v18z" fill="' + BLUE + '"/>';
      if (!isFinite(p.hi)) h += '<path d="M' + (W - P + 18) + ' ' + Y0 + 'l-12 -9v18z" fill="' + BLUE + '"/>';
      if (isFinite(p.lo)) h += '<circle cx="' + X(p.lo).toFixed(1) + '" cy="' + Y0 + '" r="7" fill="' + (p.loC ? BLUE : '#fff') + '" stroke="' + BLUE + '" stroke-width="3"/>';
      if (isFinite(p.hi) && !(p.hi === p.lo)) h += '<circle cx="' + X(p.hi).toFixed(1) + '" cy="' + Y0 + '" r="7" fill="' + (p.hiC ? BLUE : '#fff') + '" stroke="' + BLUE + '" stroke-width="3"/>';
    });
    return h + '</svg>';
  };
  /* statistics displays share one axis per activity: { lo, hi, step } */
  function axisSvg(ax, X, y, fs) {
    var h = '<path d="M' + X(ax.lo).toFixed(1) + ' ' + y + 'H' + X(ax.hi).toFixed(1) + '" stroke="' + INK + '" stroke-width="1.8"/>';
    for (var v = ax.lo; v <= ax.hi + 1e-9; v += ax.step) {
      h += '<path d="M' + X(v).toFixed(1) + ' ' + (y - 4) + 'V' + (y + 4) + '" stroke="' + INK + '" stroke-width="1.3"/>';
      if (Math.round((v - ax.lo) / ax.step) % (ax.labelEvery || 1) === 0) h += t(X(v), y + fs + 4, U.txt(v), { fs: fs, halo: false });
    }
    return h;
  }
  S.dotPlot = function (vals, ax, opts) {
    opts = opts || {};
    var cnt = {}; vals.forEach(function (v) { cnt[v] = (cnt[v] || 0) + 1; });
    var maxc = Math.max.apply(null, Object.keys(cnt).map(function (k) { return cnt[k]; }).concat([4]));
    var W = 340, P = 18, r = Math.min(7, (W - 2 * P) / (ax.hi - ax.lo) * 0.42), H = Math.max(110, 40 + maxc * (2 * r + 2) + 10), base = H - 34;
    var X = function (x) { return P + (x - ax.lo) * (W - 2 * P) / (ax.hi - ax.lo); };
    var h = '<svg class="mg-svg mk-stat" viewBox="0 0 ' + W + ' ' + H + '" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="dot plot"><rect width="' + W + '" height="' + H + '" fill="#fff"/>';
    h += axisSvg(ax, X, base, 13);
    Object.keys(cnt).forEach(function (k) { for (var i = 0; i < cnt[k]; i++) h += '<circle cx="' + X(+k).toFixed(1) + '" cy="' + (base - r - 3 - i * (2 * r + 2)).toFixed(1) + '" r="' + r.toFixed(1) + '" fill="' + BLUE + '"/>'; });
    if (opts.title) h += t(W / 2, 14, opts.title, { fs: 12, bold: true, halo: false });
    return h + '</svg>';
  };
  S.histogram = function (edges, counts, ax, ymax, opts) {
    opts = opts || {};
    var W = 340, H = 190, P = 34, top = 14, base = H - 32;
    var X = function (x) { return P + (x - ax.lo) * (W - P - 14) / (ax.hi - ax.lo); }, Y = function (c) { return base - c * (base - top) / ymax; };
    var h = '<svg class="mg-svg mk-stat" viewBox="0 0 ' + W + ' ' + H + '" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="histogram"><rect width="' + W + '" height="' + H + '" fill="#fff"/>';
    var ys = ymax <= 6 ? 1 : ymax <= 12 ? 2 : 5;
    for (var c = 0; c <= ymax; c += ys) h += '<path d="M' + P + ' ' + Y(c).toFixed(1) + 'H' + (W - 14) + '" stroke="' + GRID + '" stroke-width="1"/>' + t(P - 5, Y(c) + 4, c, { a: 'end', fs: 11, halo: false });
    counts.forEach(function (n, i) { if (n) h += '<rect x="' + X(edges[i]).toFixed(1) + '" y="' + Y(n).toFixed(1) + '" width="' + (X(edges[i + 1]) - X(edges[i])).toFixed(1) + '" height="' + (base - Y(n)).toFixed(1) + '" fill="' + S.colors.shade + '" stroke="' + BLUE + '" stroke-width="2"/>'; });
    h += '<path d="M' + P + ' ' + top + 'V' + base + '" stroke="' + INK + '" stroke-width="1.5"/>';
    h += '<path d="M' + X(ax.lo).toFixed(1) + ' ' + base + 'H' + X(ax.hi).toFixed(1) + '" stroke="' + INK + '" stroke-width="1.8"/>';
    edges.forEach(function (e) { h += '<path d="M' + X(e).toFixed(1) + ' ' + (base - 3) + 'V' + (base + 4) + '" stroke="' + INK + '"/>' + t(X(e), base + 17, U.txt(e), { fs: 12, halo: false }); });
    h += '<text x="10" y="' + ((top + base) / 2) + '" font-size="10" ' + FONT + ' fill="#46536a" transform="rotate(-90 10 ' + ((top + base) / 2) + ')" text-anchor="middle">Frequency</text>';
    return h + '</svg>';
  };
  S.boxPlot = function (five, ax) {
    var W = 340, H = 110, P = 18, mid = 42, bh = 34;
    var X = function (x) { return P + (x - ax.lo) * (W - 2 * P) / (ax.hi - ax.lo); };
    var h = '<svg class="mg-svg mk-stat" viewBox="0 0 ' + W + ' ' + H + '" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="box plot"><rect width="' + W + '" height="' + H + '" fill="#fff"/>';
    for (var v = ax.lo; v <= ax.hi + 1e-9; v += ax.step) h += '<path d="M' + X(v).toFixed(1) + ' 10V' + (H - 30) + '" stroke="#e5e9f0" stroke-width="1"/>';
    h += '<path d="M' + X(five[0]).toFixed(1) + ' ' + mid + 'H' + X(five[1]).toFixed(1) + 'M' + X(five[3]).toFixed(1) + ' ' + mid + 'H' + X(five[4]).toFixed(1) + '" stroke="' + INK + '" stroke-width="2.2"/>';
    h += '<path d="M' + X(five[0]).toFixed(1) + ' ' + (mid - 10) + 'V' + (mid + 10) + 'M' + X(five[4]).toFixed(1) + ' ' + (mid - 10) + 'V' + (mid + 10) + '" stroke="' + INK + '" stroke-width="2.2"/>';
    h += '<rect x="' + X(five[1]).toFixed(1) + '" y="' + (mid - bh / 2) + '" width="' + (X(five[3]) - X(five[1])).toFixed(1) + '" height="' + bh + '" fill="' + S.colors.shade + '" stroke="' + BLUE + '" stroke-width="2.4"/>';
    h += '<path d="M' + X(five[2]).toFixed(1) + ' ' + (mid - bh / 2) + 'V' + (mid + bh / 2) + '" stroke="' + BLUE + '" stroke-width="3"/>';
    h += axisSvg(ax, X, H - 30, 13);
    return h + '</svg>';
  };
  /* 10 × 10 hundred grids (one per whole), n shaded hundredths */
  S.hundredGrids = function (n) {
    var grids = Math.max(1, Math.ceil(n / 100)), sz = 120, gap = 14, W = grids * sz + (grids - 1) * gap, H = sz, c = sz / 10;
    var h = '<svg class="mg-svg mk-model" viewBox="-2 -2 ' + (W + 4) + ' ' + (H + 4) + '" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="hundred grid model">';
    for (var g = 0; g < grids; g++) {
      var ox = g * (sz + gap);
      for (var i = 0; i < 100; i++) { var on = g * 100 + i < n, col = i % 10, row = Math.floor(i / 10); h += '<rect x="' + (ox + col * c).toFixed(1) + '" y="' + (row * c).toFixed(1) + '" width="' + c.toFixed(1) + '" height="' + c.toFixed(1) + '" fill="' + (on ? '#60a5fa' : '#fff') + '" stroke="#94a3b8" stroke-width="0.6"/>'; }
      h += '<rect x="' + ox + '" y="0" width="' + sz + '" height="' + sz + '" fill="none" stroke="' + INK + '" stroke-width="1.6"/>';
    }
    return h + '</svg>';
  };
  /* fraction strips: whole bars cut into d equal parts, n parts shaded */
  S.bars = function (n, d) {
    var bars = Math.max(1, Math.ceil(n / d)), W = 300, bh = 34, gap = 10, H = bars * bh + (bars - 1) * gap, c = W / d;
    var h = '<svg class="mg-svg mk-model" viewBox="-2 -2 ' + (W + 4) + ' ' + (H + 4) + '" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="fraction strip model">';
    for (var b = 0; b < bars; b++) {
      var oy = b * (bh + gap);
      for (var i = 0; i < d; i++) h += '<rect x="' + (i * c).toFixed(1) + '" y="' + oy + '" width="' + c.toFixed(1) + '" height="' + bh + '" fill="' + (b * d + i < n ? '#60a5fa' : '#fff') + '" stroke="' + INK + '" stroke-width="1.4"/>';
    }
    return h + '</svg>';
  };

  /* ---------------- building ---------------- */
  MK.typesOf = function (K, unitId) { var u = K.units[unitId] || {}; return (u.types || K.types.map(function (x) { return x.id; })).slice(); };
  MK.unitOf = function (K, unitId) { return K.units[unitId] || null; };
  function clash(K, types, a, b) {
    for (var i = 0; i < types.length; i++) {
      var ty = types[i];
      if (K.fits) { if (K.fits(ty, a, b) || K.fits(ty, b, a)) return ty; }
      else { var ka = K.key(ty, a), kb = K.key(ty, b); if (ka !== null && ka !== undefined && ka === kb) return ty; }
    }
    return null;
  }
  MK.clash = clash;
  /* cfg: { unit, level, sets, seed, fams[] } → { N, sets, ids{type:[card number per set]}, types } or { error } */
  MK.build = function (kindId, cfg, vIdx) {
    var K = MK.kinds[kindId], Un = K && K.units[cfg.unit];
    if (!K || !Un) return { error: 'This matching activity is not available for this unit.' };
    var types = MK.typesOf(K, cfg.unit), N = Math.max(3, Math.min(Un.maxSets || K.maxSets || 10, cfg.sets | 0 || 6)), L = MK.LEVELS.indexOf(cfg.level) >= 0 ? cfg.level : 'cp1';
    var fams = (cfg.fams && cfg.fams.length ? cfg.fams : (Un.def || [])).filter(function (f) { return !Un.fams || Un.fams.indexOf(f) >= 0; });
    if (Un.fams && !fams.length) return { error: 'Choose at least one type.' };
    var c2 = { unit: cfg.unit, level: L, sets: N, seed: cfg.seed, fams: fams, types: types };
    for (var attempt = 0; attempt < 60; attempt++) {
      var rng = U.rngOf(cfg.seed, vIdx || 0, kindId, cfg.unit, attempt), sets = [], ctx = K.context ? K.context(rng, L, c2, Un) : {};
      if (ctx === null) continue;
      c2.ctx = ctx;
      for (var tries = 0; tries < 900 && sets.length < N; tries++) {
        var s = K.gen(rng, L, c2, Un, sets);
        if (!s) continue;
        var bad = false;
        for (var j = 0; j < sets.length && !bad; j++) if (clash(K, K.genTypes || types, s, sets[j])) bad = true;
        if (!bad) sets.push(s);
      }
      if (sets.length < N) continue;
      if (K.finish && !K.finish(sets, rng, L, c2, Un)) continue;
      var ok = true;   // every card of every type, against every other set, both ways
      for (var a = 0; a < N && ok; a++) for (var b = a + 1; b < N && ok; b++) if (clash(K, types, sets[a], sets[b])) ok = false;
      if (!ok) continue;
      var ids = {}, r2 = U.rngOf(cfg.seed, vIdx || 0, kindId, 'ids');
      types.forEach(function (ty) { var perm = r2.shuffle(sets.map(function (_, i) { return i; })); ids[ty] = []; perm.forEach(function (si, pos) { ids[ty][si] = pos + 1; }); });
      return { kind: kindId, N: N, sets: sets, ids: ids, types: types, ctx: ctx, level: L, fams: fams };
    }
    return { error: 'Could not make ' + N + ' different sets with these choices. Try fewer sets or more types.' };
  };
})(typeof window !== 'undefined' ? window : globalThis);
