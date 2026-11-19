/* Fraction Cubes lab (6.G.A.2): a right rectangular prism with edges in halves is packed with small cubes of edge 1, 1/2
   or 1/4. The number of small cubes times the volume of one small cube equals l × w × h, so V = lwh also works when the
   edges are fractions. The prism is drawn in an oblique view with every small cube on the three visible faces. */
var st = { l: 2, w: 1.5, h: 1, e: 0.5, seen: {}, edges: {} };
var g = L.graph(P.stage, { xmin: 0, xmax: 1, ymin: 0, ymax: 1, width: 660, height: 340, label: 'Prism packed with small cubes', noGrid: true, noLabels: true });
var cap = L.h('p', { class: 'sub', style: 'margin:0 6px' }, P.stage, '');
// division and fractions are shown stacked
function fr(n, d) { return '<span style="display:inline-flex;flex-direction:column;vertical-align:middle;text-align:center;line-height:1.05;margin:0 2px;font-size:.92em"><span style="border-bottom:1.5px solid currentColor;padding:0 3px">' + n + '</span><span>' + d + '</span></span>'; }
function gcd(a, b) { return b ? gcd(b, a % b) : a; }
// a multiple of 1/64 as a mixed number: HTML (stacked) or plain text (for SVG labels)
function mixed(x, plain) {
  var n = Math.round(x * 64), d = 64, w = Math.floor(n / d), r = n - w * d, c = gcd(r, d);
  if (!r) return String(w);
  var f = plain ? (r / c) + '/' + (d / c) : fr(r / c, d / c);
  return w ? w + (plain ? ' ' : '') + f : f;
}
var fmt = function (v) { return mixed(v, true); };
var cu = function (v) { return Math.abs(v - 1) < 1e-9 ? 'cubic unit' : 'cubic units'; };
var sl = L.slider(P.panel, { id: 'l', label: 'Length l', min: 0.5, max: 4, step: 0.5, value: st.l, color: 'blue', format: fmt, onInput: function (v) { st.l = v; draw(); } });
var sw = L.slider(P.panel, { id: 'w', label: 'Width w', min: 0.5, max: 3, step: 0.5, value: st.w, color: 'orange', format: fmt, onInput: function (v) { st.w = v; draw(); } });
var sh = L.slider(P.panel, { id: 'h', label: 'Height h', min: 0.5, max: 3, step: 0.5, value: st.h, color: 'green', format: fmt, onInput: function (v) { st.h = v; draw(); } });
L.chips(P.panel, { label: 'Edge of each small cube', value: String(st.e), options: [{ value: '1', label: '1 unit' }, { value: '0.5', label: '1/2 unit' }, { value: '0.25', label: '1/4 unit' }], onChange: function (v) { st.e = +v; draw(); } });
var read = L.h('div', { class: 'readout small', 'aria-live': 'polite' }, P.panel);
var btns = L.h('div', { class: 'btn-row' }, P.panel);
L.reset(btns, function () { st.l = 2; st.w = 1.5; st.h = 1; sl.set(2, true); sw.set(1.5, true); sh.set(1, true); draw(); });
var fb = L.feedback(P.panel);
var ch = L.challenges(P.panel, [
  { text: 'Pack a prism 2 by 1 1/2 by 1 with cubes of edge 1/2. How many small cubes fit? What is the volume?', check: function () { return st.seen.c1; } },
  { text: 'Make a prism 3 by 2 by 1 and pack it with 1-unit cubes, then with 1/2-unit cubes. How many 1/2-unit cubes make one 1-unit cube?', check: function () { return st.edges.one && st.edges.half; } },
  { text: 'Make a prism 2 1/2 by 2 by 1 1/2. Find its volume by counting cubes and with V = lwh.', check: function () { return st.seen.c3; } },
  { text: 'Build a prism with a volume of exactly 3 1/2 cubic units.', check: function () { return st.seen.c4; } },
  { text: 'Pack a 1 by 1 by 1 cube with cubes of edge 1/4. How many small cubes is that?', check: function () { return st.seen.c5; } }
]);
L.notice(P.below, '<p><b>Counting cubes:</b> along an edge of length l there are l ÷ e small cubes of edge e. The number of cubes is (l ÷ e)(w ÷ e)(h ÷ e).</p>' +
  '<p><b>Volume:</b> each small cube has volume e × e × e. Number of cubes × the volume of one cube = l × w × h, so <b>V = lwh</b> works for fraction edges too. ' +
  'Eight cubes of edge 1/2 make one unit cube, and 64 cubes of edge 1/4 make one unit cube.</p>');
var draw = L.scheduler(function () {
  var l = st.l, w = st.w, h = st.h, e = st.e;
  // a small cube must divide every edge
  var fits = function (x) { return Math.abs(x / e - Math.round(x / e)) < 1e-9; };
  var ok = fits(l) && fits(w) && fits(h);
  var nl = Math.round(l / e), nw = Math.round(w / e), nh = Math.round(h / e), N = nl * nw * nh, V = l * w * h;
  // oblique view: depth goes up and to the right
  var kx = 0.55, ky = 0.42, W = l + kx * w, H = h + ky * w, pad = 0.6;
  var span = Math.max(W + 2 * pad, (H + 2 * pad) * 660 / 340, 4.2);
  var x0 = (W - span) / 2, y0 = (H - span * 340 / 660) / 2;
  g.clear(); g.setView({ xmin: x0, xmax: x0 + span, ymin: y0, ymax: y0 + span * 340 / 660 });
  var P0 = function (x, y, z) { return [x + kx * z, y + ky * z]; };
  g.poly([P0(0, 0, 0), P0(l, 0, 0), P0(l, h, 0), P0(0, h, 0)], { fill: 'blue', opacity: 0.16, stroke: 'ink', width: 2.5 });
  g.poly([P0(0, h, 0), P0(l, h, 0), P0(l, h, w), P0(0, h, w)], { fill: 'orange', opacity: 0.18, stroke: 'ink', width: 2.5 });
  g.poly([P0(l, 0, 0), P0(l, 0, w), P0(l, h, w), P0(l, h, 0)], { fill: 'green', opacity: 0.16, stroke: 'ink', width: 2.5 });
  if (ok) {
    var thin = { color: 'ink-soft', width: e < 0.3 ? 0.8 : 1.4 }, i, a, b;
    for (i = 1; i < nl; i++) { a = P0(i * e, 0, 0); b = P0(i * e, h, 0); g.line(a[0], a[1], b[0], b[1], thin); a = P0(i * e, h, w); g.line(b[0], b[1], a[0], a[1], thin); }
    for (i = 1; i < nh; i++) { a = P0(0, i * e, 0); b = P0(l, i * e, 0); g.line(a[0], a[1], b[0], b[1], thin); a = P0(l, i * e, w); g.line(b[0], b[1], a[0], a[1], thin); }
    for (i = 1; i < nw; i++) { a = P0(0, h, i * e); b = P0(l, h, i * e); g.line(a[0], a[1], b[0], b[1], thin); a = P0(l, 0, i * e); g.line(b[0], b[1], a[0], a[1], thin); }
  }
  var lab = function (x, y, s, c, o) { g.text(x, y, s, Object.assign({ anchor: 'middle', color: c, size: 14, weight: 700 }, o || {})); };
  lab(l / 2, 0, 'l = ' + mixed(l, true), 'blue', { dy: 20 });
  var q = P0(l, 0, w / 2); lab(q[0], q[1], 'w = ' + mixed(w, true), 'orange', { dx: 10, dy: 14, anchor: 'start' });
  lab(0, h / 2, 'h = ' + mixed(h, true), 'green', { dx: -10, anchor: 'end' });
  cap.textContent = ok ? 'Each small cube has edge ' + mixed(e, true) + '. Count the cubes along each edge, then multiply.' : 'Cubes of edge ' + mixed(e, true) + ' do not fit exactly along every edge. Choose a smaller cube.';
  read.innerHTML = 'Prism: ' + mixed(l) + ' × ' + mixed(w) + ' × ' + mixed(h) +
    (ok ? '<div style="margin-top:6px">Cubes along each edge: ' + fr(mixed(l), mixed(e)) + ' = ' + nl + ', ' + fr(mixed(w), mixed(e)) + ' = ' + nw + ', ' + fr(mixed(h), mixed(e)) + ' = ' + nh + '</div>' +
      '<div>Number of cubes: ' + nl + ' × ' + nw + ' × ' + nh + ' = <b>' + N + '</b></div>' +
      '<div>Volume of one small cube: ' + mixed(e) + ' × ' + mixed(e) + ' × ' + mixed(e) + ' = ' + mixed(e * e * e) + '</div>' +
      '<div>V = ' + N + ' × ' + mixed(e * e * e) + ' = <b>' + mixed(V) + '</b> ' + cu(V) + '</div>' : '') +
    '<div style="margin-top:6px">V = lwh = ' + mixed(l) + ' × ' + mixed(w) + ' × ' + mixed(h) + ' = <b>' + mixed(V) + '</b> ' + cu(V) + '</div>';
  var same = function (a, b, c) { var s = [l, w, h].slice().sort(), t = [a, b, c].sort(); return s[0] === t[0] && s[1] === t[1] && s[2] === t[2]; };
  if (ok && e === 0.5 && same(2, 1.5, 1)) st.seen.c1 = true;
  if (same(3, 2, 1)) { if (e === 1) st.edges.one = true; if (e === 0.5) st.edges.half = true; }
  if (same(2.5, 2, 1.5)) st.seen.c3 = true;
  if (Math.abs(V - 3.5) < 1e-9) st.seen.c4 = true;
  if (ok && e === 0.25 && same(1, 1, 1)) st.seen.c5 = true;
  fb.set(ok && e < 1 ? N + ' small cubes × ' + mixed(e * e * e, true) + ' = ' + mixed(V, true) + ' ' + cu(V) + ', the same as l × w × h.' : '', '');
  ch.update();
});
draw();
