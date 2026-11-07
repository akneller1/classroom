/* Riemann sums on [a, b] with n equal subintervals: left, right, midpoint, trapezoid.
   The definite integral is exact (from an antiderivative); the total geometric area ∫|f| is a numerical approximation. */
var FN = {
  up: { label: 'x²/4 + 1', f: function (x) { return x * x / 4 + 1; }, F: function (x) { return x * x * x / 12 + x; }, v: [-1, 6] },
  sin: { label: 'sin x', f: Math.sin, F: function (x) { return -Math.cos(x); }, v: [-1.6, 1.6] },
  cub: { label: 'x³/8 − x', f: function (x) { return x * x * x / 8 - x; }, F: function (x) { return Math.pow(x, 4) / 32 - x * x / 2; }, v: [-4, 4] },
  cap: { label: '4 − x²', f: function (x) { return 4 - x * x; }, F: function (x) { return 4 * x - x * x * x / 3; }, v: [-5, 5] }
};
var st = { fn: 'up', a: 0, b: 4, n: 4, m: 'left', seen: {} };
function F() { return FN[st.fn]; }
function riemann(m, n) {
  var f = F().f, a = st.a, b = st.b, dx = (b - a) / n, s = 0;
  for (var i = 0; i < n; i++) { var x0 = a + i * dx, x1 = x0 + dx;
    s += m === 'left' ? f(x0) * dx : m === 'right' ? f(x1) * dx : m === 'mid' ? f((x0 + x1) / 2) * dx : (f(x0) + f(x1)) / 2 * dx; }
  return s;
}
function exact() { return F().F(st.b) - F().F(st.a); }
function totalArea() { var f = F().f, a = st.a, b = st.b, N = 4000, dx = (b - a) / N, s = Math.abs(f(a)) + Math.abs(f(b)); for (var i = 1; i < N; i++) s += (i % 2 ? 4 : 2) * Math.abs(f(a + i * dx)); return s * dx / 3; }
var GO = { xmin: -4.5, xmax: 4.5, ymin: -1, ymax: 6, width: 620, height: 480, xstep: 0.5, xlabelStep: 1, label: 'Riemann sum rectangles' }, g = L.graph(P.stage, GO);
L.h('div', { class: 'legend', style: 'margin:6px' }, P.stage, '<span><i style="background:var(--blue)"></i>counts as positive (above the x-axis)</span><span><i style="background:var(--red)"></i>counts as negative (below)</span><span><i style="background:var(--orange)"></i>sample points</span>');
L.chips(P.panel, { label: 'Function f(x)', value: st.fn, options: Object.keys(FN).map(function (k) { return { value: k, label: FN[k].label }; }), onChange: function (v) { st.fn = v; draw(); } });
L.chips(P.panel, { label: 'Method', value: st.m, options: [{ value: 'left', label: 'Left' }, { value: 'right', label: 'Right' }, { value: 'mid', label: 'Midpoint' }, { value: 'trap', label: 'Trapezoid' }], onChange: function (v) { st.m = v; draw(); } });
var sA = L.slider(P.panel, { id: 'lower-limit-a', label: 'a (start)', min: -4, max: 4, step: 0.5, value: st.a, color: 'green', format: L.nice, onInput: function (v) { if (v >= st.b) { sA.set(st.a, true); fb.set('Keep a less than b.', 'warn'); return; } st.a = v; draw(); } });
var sB = L.slider(P.panel, { id: 'upper-limit-b', label: 'b (end)', min: -4, max: 4, step: 0.5, value: st.b, color: 'green', format: L.nice, onInput: function (v) { if (v <= st.a) { sB.set(st.b, true); fb.set('Keep b greater than a.', 'warn'); return; } st.b = v; draw(); } });
var sN = L.slider(P.panel, { id: 'subintervals-n', label: 'n (number of subintervals)', min: 1, max: 100, value: st.n, color: 'purple', format: L.num, onInput: function (v) { st.n = v; draw(); } });
var read = L.h('div', { class: 'readout small', 'aria-live': 'polite' }, P.panel);
var info = L.h('dl', { class: 'kv' }, P.panel);
var fb = L.feedback(P.panel);
var btns = L.h('div', { class: 'btn-row' }, P.panel);
L.reset(btns, function () { st.a = 0; st.b = 4; st.n = 4; sA.set(0, true); sB.set(4, true); sN.set(4, true); draw(); });
var ch = L.challenges(P.panel, [
  { text: 'For ' + L.V('x') + '²/4 + 1 on [0, 4], predict whether Left sums are too big or too small. Then make the Left sum within 0.1 of the exact integral.', check: function () { return st.seen.left05; } },
  { text: 'For 4 − ' + L.V('x') + '², find an interval where the <b>Left</b> sum is too big and the <b>Right</b> sum is too small. What is f doing there?', check: function () { return st.seen.underOver; } },
  { text: 'For sin ' + L.V('x') + ', choose an interval where the definite integral is 0 even though the total shaded area is more than 1.', check: function () { return st.seen.zeroInt; } },
  { text: 'Make the definite integral <b>negative</b> while the total area between the curve and the x-axis is more than 2.', check: function () { return st.seen.negInt; } },
  { text: 'With n = 4, make the Midpoint sum closer to the exact value than the Left sum with n = 20.', check: function () { return st.seen.mid4; } }
]);
L.notice(P.below, '<p><b>A Riemann sum adds f(sample point) × Δx over n subintervals.</b> As n grows, every method gets closer to the definite integral ∫<sub>a</sub><sup>b</sup> f(x) dx, which is the limit of the sums.</p>' +
  '<p>Rectangles below the x-axis count as <b>negative</b>, so the definite integral is <b>signed</b> area. It can be 0 or negative even when lots of area is shaded. Total geometric area adds |f| instead.</p>' +
  '<p>For an increasing function, left sums underestimate and right sums overestimate (and the reverse for a decreasing one). Midpoint and trapezoid sums are often much more accurate for the same n. A sum is an approximation; the integral is the exact limit.</p>');
var draw = L.scheduler(function () {
  var fn = F(), f = fn.f, a = st.a, b = st.b, n = st.n, dx = (b - a) / n;
  L.setNiceView(g, GO, { ymin: fn.v[0], ymax: fn.v[1] }, 8); g.clear();
  for (var i = 0; i < n; i++) {
    var x0 = a + i * dx, x1 = x0 + dx, xs = st.m === 'left' ? x0 : st.m === 'right' ? x1 : (x0 + x1) / 2;
    if (st.m === 'trap') { var y0 = f(x0), y1 = f(x1), avg = (y0 + y1) / 2;
      g.poly([[x0, 0], [x0, y0], [x1, y1], [x1, 0]], { fill: avg >= 0 ? 'blue' : 'red', opacity: 0.28, stroke: avg >= 0 ? 'blue' : 'red', width: n > 40 ? 0.5 : 1.5, layer: g.layer }); }
    else { var y = f(xs); g.rect(x0, Math.min(0, y), dx, Math.abs(y), { fill: y >= 0 ? 'blue' : 'red', opacity: 0.28, stroke: y >= 0 ? 'blue' : 'red', width: n > 40 ? 0.5 : 1.5 });
      if (n <= 30) g.dot(xs, y, { color: 'orange', r: 4 }); }
  }
  g.fn(f, { color: 'ink', width: 3 });
  g.line(a, fn.v[0], a, fn.v[1], { color: 'green', width: 1.5, dash: '4 5' }); g.line(b, fn.v[0], b, fn.v[1], { color: 'green', width: 1.5, dash: '4 5' });
  var S = riemann(st.m, n), E = exact(), T = totalArea();
  var name = { left: 'Left', right: 'Right', mid: 'Midpoint', trap: 'Trapezoid' }[st.m];
  read.innerHTML = name + ' sum with ' + L.V('n') + ' = ' + n + ': <b>' + L.num(S, 4) + '</b><div class="sub" style="margin-top:4px">Δ' + L.V('x') + ' = ' + L.frac(L.nice(b) + ' − ' + (a < 0 ? '(' + L.nice(a) + ')' : L.nice(a)), n) + ' = ' + L.num(dx, 4) + '</div>';
  info.innerHTML = '<dt>Definite integral (exact)</dt><dd>' + L.num(E, 4) + (Math.abs(E - Math.round(E * 1000) / 1000) > 1e-9 ? '…' : '') + '</dd><dt>Sum − integral</dt><dd>' + L.num(S - E, 4) + ' (' + (Math.abs(S - E) < 5e-5 ? 'equal to 4 decimal places' : S > E ? 'overestimate' : 'underestimate') + ')</dd>' +
    '<dt>Total area ∫|f|</dt><dd>≈ ' + L.num(T, 3) + '</dd>';
  fb.set(Math.abs(T - Math.abs(E)) > 1e-3 ? 'Part of the graph is below the x-axis: those pieces subtract, so the integral (' + L.num(E, 3) + ') is not the total area (≈ ' + L.num(T, 3) + ').' : 'The graph does not cross the x-axis on [' + L.nice(a) + ', ' + L.nice(b) + '], so the integral equals the area' + (E < 0 ? ' with a minus sign' : '') + '.', '');
  if (st.fn === 'up' && a === 0 && b === 4 && st.m === 'left' && Math.abs(S - E) < 0.1) st.seen.left05 = true;
  var Lf = riemann('left', n), Rt = riemann('right', n);
  if (st.fn === 'cap' && n >= 2 && Lf > E + 1e-9 && Rt < E - 1e-9) st.seen.underOver = true;
  if (st.fn === 'sin' && Math.abs(E) < 1e-9 && T > 1) st.seen.zeroInt = true;
  if (E < -1e-9 && T > 2) st.seen.negInt = true;
  if (st.m === 'mid' && n === 4 && Math.abs(S - E) < Math.abs(riemann('left', 20) - E)) st.seen.mid4 = true;
  ch.update();
});
draw();
