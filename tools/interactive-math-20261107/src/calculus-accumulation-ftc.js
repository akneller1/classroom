/* A(x) = ∫ from a to x of f(t) dt, computed exactly (antiderivatives; the piecewise-linear f is integrated piece by piece).
   The bottom graph shows A with its tangent line at x, whose slope is f(x). */
var PW = [[0, -1], [1, -1], [3, 2], [5, 2], [6, -1]];
function pwf(t) { for (var i = 0; i < PW.length - 1; i++) { var p = PW[i], q = PW[i + 1]; if (t <= q[0] + 1e-12) return p[1] + (q[1] - p[1]) * (t - p[0]) / (q[0] - p[0]); } return PW[PW.length - 1][1]; }
function pwF(x) { var s = 0; for (var i = 0; i < PW.length - 1; i++) { var p = PW[i], q = PW[i + 1]; if (x <= p[0]) break; var e = Math.min(x, q[0]); s += (pwf(p[0]) + pwf(e)) / 2 * (e - p[0]); } return s; }
var FN = {
  lin: { label: '2 − t', f: function (t) { return 2 - t; }, F: function (t) { return 2 * t - t * t / 2; }, v: [-4.5, 2.5], Av: [-6, 4] },
  wave: { label: '2 sin t', f: function (t) { return 2 * Math.sin(t); }, F: function (t) { return -2 * Math.cos(t); }, v: [-2.5, 2.5], Av: [-1, 5] },
  pw: { label: 'piecewise', f: pwf, F: pwF, v: [-1.8, 2.5], Av: [-3, 6] }
};
var st = { fn: 'lin', a: 0, x: 1, full: false, as: {}, seen: {} };
function F() { return FN[st.fn]; }
function A(x) { return F().F(x) - F().F(st.a); }
var GO = { xmin: -0.3, xmax: 6.3, ymin: -4.5, ymax: 2.5, width: 620, height: 300, xstep: 0.5, xlabelStep: 1, label: 'Rate f(t) with the accumulated area shaded' }, g = L.graph(P.stage, GO);
L.h('p', { class: 'sub', style: 'margin:0 6px' }, P.stage, 'Top: the rate f(' + L.V('t') + '). Blue area counts positive, red counts negative. Drag the purple point to move ' + L.V('x') + '.');
var GAO = { xmin: -0.3, xmax: 6.3, ymin: -6, ymax: 4, width: 620, height: 300, xstep: 0.5, xlabelStep: 1, label: 'Accumulation function A(x)' }, gA = L.graph(P.stage, GAO);
L.h('p', { class: 'sub', style: 'margin:0 6px' }, P.stage, 'Bottom: A(' + L.V('x') + ') = the signed area from ' + L.V('a') + ' to ' + L.V('x') + '. The green segment is its tangent line.');
L.chips(P.panel, { label: 'Rate function f(t)', value: st.fn, options: Object.keys(FN).map(function (k) { return { value: k, label: FN[k].label }; }), onChange: function (v) { st.fn = v; st.as = {}; draw(); } });
var read = L.h('div', { class: 'readout small', 'aria-live': 'polite' }, P.panel);
var sx = L.slider(P.panel, { id: 'upper-x', label: 'x (end of the area)', min: 0, max: 6, step: 0.1, value: st.x, color: 'purple', format: function (v) { return L.num(v, 1); }, onInput: function (v) { st.x = Math.max(v, st.a); if (v < st.a) sx.set(st.a, true); draw(); } });
var sa = L.slider(P.panel, { id: 'lower-a', label: 'a (where the area starts)', min: 0, max: 3, step: 0.5, value: st.a, color: 'green', format: L.nice, onInput: function (v) { st.a = v; if (st.x < v) { st.x = v; sx.set(v, true); } draw(); } });
var btns = L.h('div', { class: 'btn-row' }, P.panel);
var bF = L.button(btns, 'Show all of A', function () { st.full = !st.full; bF.textContent = st.full ? 'Hide the rest of A' : 'Show all of A'; draw(); }, true);
L.reset(btns, function () { st.a = 0; st.x = 1; st.full = false; sa.set(0, true); sx.set(1, true); bF.textContent = 'Show all of A'; draw(); });
var fb = L.feedback(P.panel);
var ch = L.challenges(P.panel, [
  { text: 'Predict where A(' + L.V('x') + ') is largest, then move ' + L.V('x') + ' there. What is f(' + L.V('x') + ') at that point?', check: function () { return st.seen.max; } },
  { text: 'Find an ' + L.V('x') + ' &gt; ' + L.V('a') + ' where A(' + L.V('x') + ') is back to 0. What happened to the areas?', check: function () { return st.seen.zero; } },
  { text: 'For 2 sin ' + L.V('t') + ', find where A is climbing with slope 2. Compare the slope of A with the height of f.', check: function () { return st.seen.slope2; } },
  { text: 'Try two different starting points ' + L.V('a') + ' with the same function and the same ' + L.V('x') + '. What changes in the graph of A, and what stays the same?', check: function () { return st.seen.twoA; } },
  { text: 'For the piecewise rate, find where A has its <b>minimum</b>. What does f do there?', check: function () { return st.seen.pwMin; } }
]);
L.notice(P.below, '<p><b>The accumulation function A(x) = ∫<sub>a</sub><sup>x</sup> f(t) dt adds up signed area.</b> When f &gt; 0 the area grows, so A increases; when f &lt; 0, A decreases.</p>' +
  '<p><b>Fundamental Theorem of Calculus:</b> the slope of A at x is the height of f at x: A′(x) = f(x). So A has a maximum or minimum where f changes sign.</p>' +
  '<p>Changing the start a slides the whole graph of A up or down (it adds a constant) but does not change its slope. Areas below the axis cancel areas above it, so A can return to 0.</p>');
var draw = L.scheduler(function () {
  var fn = F(), f = fn.f, a = st.a, x = st.x, Ax = A(x), fx = f(x);
  L.setNiceView(g, GO, { ymin: fn.v[0], ymax: fn.v[1] }, 6); g.clear();
  L.setNiceView(gA, GAO, { ymin: fn.Av[0], ymax: fn.Av[1] }, 6); gA.clear();
  /* shaded signed area from a to x, split at sign changes by sampling */
  var N = Math.max(2, Math.round((x - a) * 60));
  for (var i = 0; i < N; i++) { var t0 = a + (x - a) * i / N, t1 = a + (x - a) * (i + 1) / N, y0 = f(t0), y1 = f(t1), pos = y0 + y1 >= 0;
    g.poly([[t0, 0], [t0, y0], [t1, y1], [t1, 0]], { fill: pos ? 'blue' : 'red', opacity: 0.3 }); }
  g.fn(f, { color: 'ink', width: 3, from: 0, to: 6 });
  g.line(a, fn.v[0], a, fn.v[1], { color: 'green', width: 2, dash: '5 5' });
  g.line(x, 0, x, fx, { color: 'purple', width: 3 });
  g.text(x, fx, 'f(x) = ' + L.num(fx, 2), { dx: 8, dy: fx >= 0 ? -10 : 18, color: 'purple', size: 14 });
  g.handle(x, 0, { color: 'purple', snap: 0.1, label: 'x on the t-axis', onDrag: function (nx) { st.x = Math.max(a, Math.min(6, L.round(nx, 1))); sx.set(st.x, true); draw(); } });
  /* A graph */
  if (st.full) gA.fn(A, { color: 'ghost', width: 3, dash: '7 6', from: 0, to: 6 });
  gA.fn(A, { color: 'blue', width: 4, from: a, to: x });
  gA.line(x - 0.6, Ax - 0.6 * fx, x + 0.6, Ax + 0.6 * fx, { color: 'green', width: 4 });
  gA.dot(a, 0, { color: 'green', r: 6 });
  gA.dot(x, Ax, { color: 'purple', r: 8, stroke: 'ink', strokeWidth: 2 });
  gA.text(x, Ax, 'A(x) = ' + L.num(Ax, 2), { dx: 10, dy: -12, color: 'purple', size: 14 });
  read.innerHTML = 'A(' + L.num(x, 1) + ') = ∫<sub>' + L.nice(a) + '</sub><sup>' + L.num(x, 1) + '</sup> f(' + L.V('t') + ') d' + L.V('t') + ' = ' + L.num(Ax, 3) +
    '<div class="sub" style="margin-top:6px">slope of A at ' + L.V('x') + ' = ' + L.num(fx, 3) + ' = f(' + L.num(x, 1) + ')</div>';
  fb.set(Math.abs(fx) < 0.05 ? 'f(x) ≈ 0: A has a horizontal tangent here. Check whether f changes sign.' : fx > 0 ? 'f(x) > 0: area is being added, so A is increasing.' : 'f(x) < 0: area below the axis is being added, so A is decreasing.', '');
  /* challenge bookkeeping */
  var best = -Infinity, bx = a; for (var t = a; t <= 6 + 1e-9; t += 0.1) { var v = A(t); if (v > best + 1e-12) { best = v; bx = t; } }
  if (x > a + 0.05 && Math.abs(Ax - best) < 0.02 && Math.abs(x - bx) <= 0.11 && bx > a + 0.05 && bx < 6 - 0.05) st.seen.max = true;
  if (x > a + 0.15 && Math.abs(Ax) < 0.05) st.seen.zero = true;
  if (st.fn === 'wave' && Math.abs(fx - 2) < 0.05) st.seen.slope2 = true;
  st.as[st.fn + ':' + L.num(x, 1)] = st.as[st.fn + ':' + L.num(x, 1)] || {}; st.as[st.fn + ':' + L.num(x, 1)][a] = true;
  if (Object.keys(st.as[st.fn + ':' + L.num(x, 1)]).length >= 2) st.seen.twoA = true;
  if (st.fn === 'pw' && a < 5 / 3 && Math.abs(x - 5 / 3) <= 0.07) st.seen.pwMin = true;
  ch.update();
});
draw();
